---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD uses behavior failures to guide implementation. This reference covers useful assertions, test boundaries and the limits of the red → green loop when environment setup is expensive. Choose the tools and implementation route; the evidence must distinguish a real behavior failure from a broken test environment.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test at agreed seams.** Reuse boundaries and acceptance criteria already established by the user or approved spec. Ask only when a missing product or acceptance decision matters; choosing test mechanics within that contract does not require renewed approval.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Untested assumptions at scale**: writing a large test suite against guessed interfaces, asset facts or behavior commits to a fixture before knowing whether it can observe the system. A small representative path can resolve that uncertainty. For established behavior and stable interfaces, authoring several scenarios, collecting their failures together and fixing them as a group is valid; choose the granularity from feedback cost and what remains unknown.

## Feedback cost and evidence

- **Cheap, isolated behavior:** use a small red → green cycle. The failing assertion must expose the intended behavior gap; compilation errors, missing objects and broken setup do not establish that red. Avoid speculative features and tests that merely repeat the implementation.
- **Expensive integration or UE/PIE:** cost includes compilation, editor startup, assets and teardown, not only assertion runtime. One test does not require one rebuild or restart. A representative path can establish that the fixture stimulates and observes the right system; known scenarios can then share an environment run. Keep separate results for each scenario. Batching execution does not justify writing all tests against imagined behavior or deferring an unresolved dependency until the end. Choose batch size and timing from uncertainty, risk and resource cost.
- **Fixture validity:** incorrect actor positions, guessed enum values, invalid references after cancellation, and observers retaining an old world can produce false failures or crashes. Establish the facts needed by the scenario from current interfaces/assets and account for observation and teardown. A failing fixture is not a reason to change the product contract.
- **Persistence:** an in-memory readback cannot prove a new asset-writing method survives saving and reload. Use independent persistence evidence for that method before relying on it more broadly; already applicable evidence need not trigger a full editor restart for every property.
- **Completion:** preserve the behavior result and the source/assets/environment it exercised. A blocked or unrun check is not a pass. Low-impact wiring or configuration with no independent behavior assertion may need a proportional check instead of a ceremonial test.

Internal refactoring is allowed when it supports the current behavior and remains covered; it need not wait for a separate role. Shared editor and build resources follow the project's actual constraints. Existing fixture, test and reporting tools are available means, not a mandated implementation recipe.
