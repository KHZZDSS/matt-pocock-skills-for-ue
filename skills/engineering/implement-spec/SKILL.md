---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

Deliver the spec on one **integration branch**, with evidence for the acceptance criteria and tickets resolved through the configured tracker. Read the spec, tickets and the project's execution and validation constraints. If tracker configuration is missing, `/setup-matt-pocock-skills` is available; this does not block independent implementation work.

Choose the implementation route, delegation and tools for the actual task. The constraints below describe failure boundaries and completion evidence; they do not require a fixed cast of agents or a handoff for every operation.

## Dependencies and resources

Tickets form a **task graph**. A dependency on a stable interface may permit implementation before the upstream ticket's runtime acceptance; a dependency on an actual asset or unresolved behavior still needs that evidence. Record the interface/version being relied on. Starting dependent work does not close the upstream ticket.

Parallel work must have compatible file ownership and resource use. Read the project's actual editor, PIE and build capacity: a single shared editor cannot execute conflicting operations for several workers at once. Source work, investigation and review need not wait for that resource. Give delegates the spec/ticket pointers, relevant facts, ownership, available tools and required evidence; let them choose how to produce the result. Keep communication to new facts, blockers and decisions.

Worktrees are an isolation tool, not a per-ticket requirement. A worktree starts from a commit, so uncommitted source, configuration and assets are absent unless explicitly included in the baseline. Do not reset unknown changes to make a baseline match. Copying a full UE environment for every source task wastes dependencies and build caches; a stable integration validation workspace is an available alternative when its inputs can be identified. Shared-directory cleanup can affect other workspaces: use the project's preparation and cleanup tools within their documented limits.

## Integration and validation

Use the adapted `tdd` skill for behavior tests at the agreed seams; it distinguishes cheap feedback from expensive environment runs. Preparation or fixture failures are not evidence of a production behavior failure.

An integrated change awaiting verification is not an accepted ticket. Validation evidence must identify the source revision or explicit local diff, relevant assets and environment, and the build/module actually exercised. A build in one workspace does not prove an editor running another version is correct. Existing evidence is reusable only where those inputs and assertion premises remain applicable; report its original version.

Use `code-review` for independent review of the integrated production changes before the final expensive acceptance run. Early tests that settle uncertainty or unblock work should not wait for that review. Review and environment preparation can overlap if their resources allow it. Route findings to the owner of the affected decision or implementation; a local correction does not require restarting unrelated roles. Review and regression coverage must include fixes made after the reviewed version.

## Completion

Close a ticket only when its acceptance evidence is satisfied; keep unrun or blocked requirements visible. A branch merge or available interface is not acceptance. If the authorized tracker flow uses PRs, a draft can be opened once there are changes; mark it ready only after the required review, fixes and validation. External updates follow the user's authorization.

Report the integration branch, evidence and unresolved requirements. Retire task worktrees only when they are no longer needed and required ignored files have been preserved, using the project's cleanup mechanism.
