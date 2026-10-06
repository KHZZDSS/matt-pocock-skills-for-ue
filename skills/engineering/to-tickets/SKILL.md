---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into **tickets**: tracer-bullet vertical slices with explicit dependencies, acceptance evidence and any shared-resource constraints that affect scheduling. Describe the result and known failure boundaries; leave the implementation route and tools to the executing agent.

Use the configured issue tracker and triage vocabulary. If these are missing, `/setup-matt-pocock-skills` is available; a missing publishing destination does not prevent drafting the breakdown.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Include prefactoring only where it removes a concrete implementation obstacle; it is not a prerequisite for every feature.

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- A necessary prefactor has an explicit dependent behavior; avoid standalone speculative cleanup

</vertical-slice-rules>

Give each ticket its **blocking edges** and the condition that satisfies each one. A published, fixed interface can unblock source work before upstream runtime acceptance; an unavailable asset or unresolved behavior cannot. Distinguish implementation readiness, integrated-but-unverified work and accepted work. Do not close a ticket merely to unlock its dependents.

For work sharing an editor, PIE session, build output or asset, include the actual resource constraint and ownership needed to avoid interference. Functional independence alone does not make two editor operations concurrent. Record only constraints relevant to the ticket, not a prescribed agent hierarchy, per-ticket worktree or test script. The project provides capacity and tool entrypoints; the executor chooses scheduling within those limits.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which dependency conditions (if any) must be satisfied before work starts
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Resolve material decisions with the user. An already approved breakdown remains approved; formatting tickets or selecting execution mechanics does not require repeating that approval.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. If the source was an existing issue, make each ticket its sub-issue (tracker doc's operation). Apply the `ready-for-agent` triage label unless instructed otherwise; the tickets are agent-grabbable by construction.

Work the **frontier** whose stated start conditions are satisfied and whose required resources are available. Acceptance still requires each ticket's evidence.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** ticket references and the specific conditions needed to start, or "None".

**Execution context (if relevant):** shared resource or file/asset ownership constraints, current-fact/tool pointers, and what evidence acceptance needs. Omit when the criteria below suffice.

**Status:** ready-for-agent

- [ ] Acceptance criterion 1, with observable evidence
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket and the condition needed to start, or "None". Native edges may replace references but must not discard partial-readiness conditions.

## Execution context (if relevant)

Shared resource or file/asset ownership constraints, current-fact/tool pointers, and evidence needs not already covered by acceptance criteria. Omit when unnecessary.

</issue-template>

Use precise file, asset and tool pointers when they prevent repeated discovery; identify the inspected revision or state when freshness matters. Pointers are navigation, not proof that facts are unchanged. Keep implementation recipes out of tickets unless they encode an actual approved constraint. A prototype snippet may capture a decision more precisely than prose; cite its source and retain only the decision-bearing part.
