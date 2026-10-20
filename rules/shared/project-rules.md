---
name: project-rules
description: >
  Standing engineering rules that apply to every project planned or built with the project-planner skill. Read this file before writing phase documents and apply the rules in every phase. These are starter defaults; edit them to match your own preferences.
---

# Project Rules

These rules apply to every project. A phase document must follow them without restating them in full. When a phase needs an exception, the document names the rule and gives the reason.

## Precedence

- An existing codebase's conventions win over these rules. In a brownfield project, match what is there and note the difference in the phase document.
- A rule in the source spec wins over these rules when the two conflict and the spec's rule is explicit.
- These rules win over the planner's own defaults.

## Stack and Dependencies

- Prefer established, widely used technology over new tools.
- Add a third-party dependency only when writing the code yourself would take more than a day or carry real risk (cryptography, date handling, parsing standard formats).
- Pin dependency versions with a lockfile.
- Check that a dependency is actively maintained before adding it.

## Code Style

- Use the formatter and linter standard for the language. Run both in CI and fail the build on violations.
- Keep functions small and single-purpose.
- Name things for what they are, not how they work.
- Do not leave dead code, commented-out code, or unused imports.
- Add a comment only when the reason for the code is not obvious from the code itself.

## Error Handling

- Never swallow an error silently. Handle it, return it, or log it with context.
- Validate input at the boundary of the system. Trust data inside the boundary.
- Return errors in one consistent shape across the project. The first phase defines that shape.
- Do not expose internal details (stack traces, SQL, file paths) to end users.

## Testing

- Every behavior change ships with tests in the same PR.
- Follow the testing pyramid: many unit tests, fewer integration tests, few end-to-end tests.
- Tests run offline and deterministically. Mock the clock, the network, and randomness.
- A bug fix starts with a failing test that reproduces the bug.
- The full test suite must pass before a PR merges.

## Security Baseline

- Never commit secrets. Read them from environment variables or a secrets manager.
- Check authorization on the server for every protected action. Never rely on the client alone.
- Use parameterized queries. Never build SQL from user input.
- Hash passwords with a standard algorithm built for passwords (argon2, bcrypt, scrypt).
- Log no secrets and no personal data.

## Data and Migrations

- Every schema change is a migration file that can be applied to an empty database and to the previous version.
- Make migrations backward compatible with the previous release when possible. Split a breaking change into add, backfill, switch, and remove steps across releases.
- State the rollback plan for every migration.

## Git and Pull Requests

- One phase lands as one PR.
- Keep commits small and focused. Write messages that explain why, not only what.
- Do not merge a PR with failing checks.
- Do not commit generated files or build output unless the project requires it.

## Documentation

- Keep a README that explains how to install, run, test, and deploy the project.
- Update the docs in the same PR that changes the behavior they describe.
- Record each non-obvious architectural decision with its reason and the alternative considered.

## Working Rules for Coding Agents

- Read the phase document and the files it references before changing code.
- If the code does not match what the phase document describes, stop and ask. Do not guess.
- Do not make changes outside the phase's scope. Note anything out of scope instead of fixing it.
- Do not claim work is done until the phase's tests pass and each acceptance criterion is checked.
