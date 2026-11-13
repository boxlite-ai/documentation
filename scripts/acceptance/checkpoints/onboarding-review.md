# Checkpoint onboarding acceptance

Date: 2026-11-13. Target: app production environment via https://api.boxlite.ai. Source contract reviewed at boxlite origin/main 81a85fa5d and the user-supplied checkpoint brief. Credentials remained in the host process and are omitted here.

## Editorial research

- Modal: https://modal.com/docs/guide/sandbox-snapshots — useful concrete write/capture/restore/read example. Adopt visible output verification, not Modal's retention or memory behavior.
- E2B: https://docs.e2b.dev/sandbox/snapshots — distinguishes one-to-many snapshots from resuming a single sandbox, then covers create, restore, list, and delete. Adopt the distinction; BoxLite checkpoints require a stopped source and omit memory.
- Daytona: https://www.daytona.io/docs/en/snapshots/ — separates snapshot sources and types, with multiple client examples and readiness guidance. Keep BoxLite's one capture path and its own restrictions.

The initial golden path wrote a small Python program into a source box, captures it, and runs the same program in a new box. Expected output is 42. No provider account, model credential, dependency download inside the guest, or application scaffold is needed. Follow with reuse, inheritance, independence, cleanup, and recovery. Keep local snapshot APIs distinct from Cloud checkpoints.

## Live acceptance

The configuration endpoint reported checkpoints_enabled=true. Checkpoint list initially contained no entries.

| Check | Observed result |
|---|---|
| Running source | Rejected with the stopped-and-idle requirement |
| Capture | creating transitioned to ready with a nonzero archive size |
| Lookup | Name and ID resolved to the same checkpoint |
| Configuration override | Explicit cpus rejected even when equal to the source value |
| Immutable disk | Source changed after capture; restored file retained the captured value |
| Source deletion | Two boxes restored after the source was deleted |
| Environment and identity | Original PROJECT value retained; BOXLITE_BOX_ID matched each new box |
| Worker isolation | Changing worker 1 did not alter worker 2 |
| Checkpoint deletion | Already restored worker still executed its saved program |
| Secret attachment | Capture rejected for a stopped box with a synthetic Secret |
| Cleanup | Test boxes removed; checkpoint list returned to zero |

The initial exploratory test relied on implicit startup and received exec exit -1 with empty output. Re-running with explicit start passed. All documented examples use explicit start and were tested separately.

## Initial onboarding examples

Python and TypeScript were run with the installed published SDKs. CLI used the installed official binary; only the locally saved context name changed from app to default for this account. Credentials were supplied through an in-process getpass override for Python and a host environment variable for TypeScript.

### python

Exit code: 0

```text
Source: KD4Qa5WrB2kk
Checkpoint: 5e7ab7c1-436f-4257-8e3a-5d357d374637
Worker: n8KXnrn6XK9C
Restored result: 42
Removed demo boxes and checkpoint
```

### typescript

Exit code: 0

```text
Source: sXinHF6FwvsL
Checkpoint: 89250f53-e839-4cf5-92a9-b5ca292fac1e
Worker: q3uaf1ovYrPj
Restored result: 42
Removed demo boxes and checkpoint
```

### cli

Exit code: 0

```text
Source: l8cUuWGp0Xno
Checkpoint: 208e9a86-7f69-406f-9481-587c5e3e1fe0
Worker: 3MAWO6H7YdsX
42
3MAWO6H7YdsX
l8cUuWGp0Xno
208e9a86-7f69-406f-9481-587c5e3e1fe0
Removed demo boxes and checkpoint
```

## Verification boundaries

Volume rejection, all configuration inheritance fields, name grammar, delete locking, and local-runtime availability were checked against current source and the supplied brief; not every branch was exercised live. No load, quota-exhaustion, pagination-scale, cross-region, dashboard, or timing benchmark acceptance is claimed.

Document lint, navigation/MDX structure, generated llms index, Mintlify build, and broken-link checks passed. Browser review verified the single Checkpoints navigation entry, rendered flow diagram, and Python/TypeScript/CLI tabs.

## Guided onboarding revision

Replaced the single-script introduction with four numbered steps: prepare a baseline, capture, restore, and create an independent second worker. Cleanup is a separate fifth step. The CLI is executable step by step in one terminal; Python and TypeScript step snippets explain complete runnable programs provided in collapsed sections. Neither SDK program deletes resources automatically. Test automation cleans them up separately after checking results.

Expected final output is branch-a for worker 1 and baseline for worker 2. The tested SDK files exactly match the full code blocks in the page. CLI acceptance uses the documented commands, replaces only the saved account context, and polls the documented status commands until stopped/ready.

Python and TypeScript completed successfully. The first CLI attempt encountered a server-side wait-for-start timeout during restoration; the target box ID was returned and cleaned up with the source and checkpoint. This is not recorded as a pass.

The intermediate REPL-based draft was discarded after finding poor multiline-paste ergonomics; it is not the published workflow. Its exploratory Python restore also encountered a server timeout. All identified exploratory resources were removed.

Mintlify build, broken links, lint, structure, and llms checks passed. Browser review verified numbered steps, CLI as the initial language, and expandable complete SDK examples.

The second CLI attempt restored worker 1 but its subsequent execution hit a WebSocket TLS handshake EOF. It was recorded as a failure and its resources were cleaned up; it is not an example syntax failure or a pass.

The third CLI attempt captured successfully, restored two workers, read baseline from worker 1, then changed worker 1 to branch-a. Reading worker 2 failed on an API network connection. Therefore the revised CLI walkthrough is not claimed as a clean end-to-end pass in this revision; Python and TypeScript are. Every resource from all three CLI attempts was subsequently deleted successfully.

- final-report.json: Python, exit 0; cleanup exit codes: [0, 0, 0, 0].
- final-report.json: TypeScript, exit 0; cleanup exit codes: [0, 0, 0, 0].
- final-report.json: CLI, exit 1; cleanup exit codes: [0, 1, 0].
- cli-retry-report.json: CLI, exit 1; cleanup exit codes: [0, 0, 0].
- cli-final-report.json: CLI, exit 1; cleanup exit codes: [0, 0, 0, 0].
