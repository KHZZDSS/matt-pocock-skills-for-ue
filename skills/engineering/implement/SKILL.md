---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use the adapted `tdd` skill for behavior tests at agreed seams. Existing user-approved criteria remain valid; ask only for a missing decision that changes the intended behavior or acceptance.

Choose validation by the risk and actual feedback cost. Compilation, fixture readiness, asset persistence and runtime behavior prove different things. A fixture or setup failure is not a production-test red. Use the project's available tools and resource constraints; avoid repeating full builds or editor starts merely to finish each small test cycle. Preserve per-scenario outcomes and the source, asset and environment version exercised. Run earlier when an unknown or changed interface blocks further work.

Use `code-review` to review production changes before the final expensive acceptance run; necessary early validation can proceed independently. Include subsequent fixes in the relevant review and regression evidence. An implementation awaiting runtime checks is not accepted work.

Commit the task's changes to the intended branch, preserving unrelated work, and report the evidence and any unmet criteria. Choose the implementation method and tools; this skill does not require separate agents, worktrees or a fixed sequence of handoffs.
