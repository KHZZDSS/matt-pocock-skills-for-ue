"""Read-only provenance check; optional comparison with a fetched upstream ref."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    )
    return result.stdout.decode("utf-8").strip()


def safe_path(value, prefix="skills/"):
    if not isinstance(value, str) or not value.startswith(prefix):
        raise ValueError(f"Invalid skill path: {value!r}")
    if "\\" in value or ":" in value or ".." in PurePosixPath(value).parts:
        raise ValueError(f"Invalid skill path: {value!r}")
    if not (ROOT / value).resolve().is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {value}")
    return value


def tree(commit, path):
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}:{path}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def files_at(commit, path):
    rows = git("ls-tree", "-r", "-z", f"{commit}:{path}").split("\0")
    return {row.split("\t", 1)[1]: row.split()[2] for row in rows if row}


def working_files(path):
    names = git("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", path)
    result = {}
    for name in set(names.split("\0")) - {""}:
        file = ROOT / name
        if file.is_file():
            relative = PurePosixPath(name).relative_to(path).as_posix()
            # Respect Git's clean filters so CRLF checkouts compare correctly.
            result[relative] = git("hash-object", "--path", name, "--", name)
    return result


def check(manifest):
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema")
    seen, names, active = set(), set(), set()
    errors = []
    for item in manifest["skills"]:
        path = safe_path(item["local_path"])
        name, status = item["name"], item["status"]
        if path in seen or name in names:
            errors.append(f"Duplicate skill entry: {name} / {path}")
        seen.add(path)
        names.add(name)
        if status not in {"unmodified", "adapted", "new", "removed"}:
            errors.append(f"{name}: invalid status {status}")
        if not item.get("rationale") or not item.get("validation"):
            errors.append(f"{name}: rationale and actual validation required")
        if status in {"adapted", "new"} and not item.get("principles"):
            errors.append(f"{name}: record applicable UE principle IDs")
        if any(p not in {f"P{i}" for i in range(1, 9)} for p in item["principles"]):
            errors.append(f"{name}: unknown principle ID")
        if status == "removed":
            if (ROOT / path).exists():
                errors.append(f"{name}: removed directory still exists")
        else:
            active.add(path)
            entry = ROOT / path / "SKILL.md"
            if not entry.is_file():
                errors.append(f"{name}: SKILL.md missing")
            else:
                content = entry.read_text(encoding="utf-8")
                match = re.search(r"(?m)^name:\s*['\"]?([^\s'\"]+)", content)
                if not match or match[1] != name:
                    errors.append(f"{name}: frontmatter name mismatch")
        if status == "new":
            if any(item.get(k) is not None for k in
                   ("upstream_path", "base_commit", "base_tree", "last_reviewed_commit")):
                errors.append(f"{name}: new skill must not claim an upstream baseline")
            continue
        upstream_path = safe_path(item["upstream_path"])
        for key in ("base_commit", "last_reviewed_commit"):
            sha = item[key]
            if not re.fullmatch(r"[0-9a-f]{40}", sha or ""):
                raise ValueError(f"{name}: {key} must be an exact commit SHA")
            git("cat-file", "-e", f"{sha}^{{commit}}")
        declared_tree = item["base_tree"]
        actual_tree = tree(item["base_commit"], upstream_path)
        if (not re.fullmatch(r"[0-9a-f]{40}", declared_tree or "")
                or actual_tree is None
                or actual_tree != declared_tree
                or git("cat-file", "-t", actual_tree) != "tree"):
            errors.append(f"{name}: baseline tree mismatch or missing object")
            continue
        if status == "unmodified":
            expected = files_at(item["base_commit"], upstream_path)
            actual = working_files(path)
            changed = sorted(k for k in expected.keys() | actual.keys()
                             if expected.get(k) != actual.get(k))
            if changed:
                errors.append(f"{name}: unmodified claim is false: {', '.join(changed)}")
    discovered = {p.parent.relative_to(ROOT).as_posix()
                  for p in (ROOT / "skills").rglob("SKILL.md")}
    for path in sorted(discovered - active):
        errors.append(f"Unregistered skill: {path}")
    return errors


def compare(manifest, ref):
    candidate = git("rev-parse", "--verify", f"{ref}^{{commit}}")
    print(f"Candidate upstream commit: {candidate}")
    known = set()
    changed = 0
    for item in manifest["skills"]:
        if item["status"] == "new":
            continue
        path = item["upstream_path"]
        known.add(path)
        before = tree(item["last_reviewed_commit"], path)
        after = tree(candidate, path)
        if before != after:
            changed += 1
            result = "MISSING (check rename/removal)" if after is None else "CHANGED"
            print(f"{result}: {item['name']} [{item['status']}] {path}")
    paths = git("ls-tree", "-r", "--name-only", candidate, "--", "skills").splitlines()
    added = sorted({str(PurePosixPath(p).parent) for p in paths
                    if p.endswith("/SKILL.md")} - known)
    for path in added:
        print(f"UNTRACKED UPSTREAM SKILL: {path}")
    print(f"Upstream differences: {changed} registered, {len(added)} untracked; no files changed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-ref", help="Fetched ref to compare; never fetches or writes")
    args = parser.parse_args()
    try:
        manifest = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
        errors = check(manifest)
        if errors:
            print("\n".join(f"FAIL: {error}" for error in errors), file=sys.stderr)
            return 1
        print(f"PASS: {len(manifest['skills'])} skill records, provenance and unmodified content.")
        if args.upstream_ref:
            compare(manifest, args.upstream_ref)
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}. Check the manifest and fetch any missing baseline objects.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
