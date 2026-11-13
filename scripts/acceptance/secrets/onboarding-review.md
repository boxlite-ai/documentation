# Cloud Secrets onboarding review

## Primary documentation reviewed

- Daytona: https://www.daytona.io/docs/en/secrets/ — introduces the credential boundary before setup and includes explicit verification guidance. Its organization-scoped secrets and response scrubbing are product-specific; neither is assumed for BoxLite.
- Modal: https://modal.com/docs/guide/sandbox-secret-injection — separates policy definition, attachment, matching, TLS trust, and limitations. Its runtime policy-update API is not a BoxLite capability claim.
- Modal: https://modal.com/docs/guide/secrets — presents conventional secret storage and attachment. Environment-variable delivery should not be confused with outbound header injection.

## BoxLite design choices

Lead with a real LLM inference request and its visible reply, with complete Python, TypeScript, and CLI + REST tabs for Cloud and local runtimes. Explain header injection after the working example. Keep the fake-token echo diagnostic in an optional accordion near the end. State the existing-header requirement and avoid claims about a standalone vault or live rotation.

## Verification, 2026-11-13

Installed the published Python SDK in an isolated virtual environment. Executed the onboarding script against https://api.boxlite.ai with the existing authorized Cloud credential supplied by an in-process getpass override; no credential was saved in this report or the example.

- Created disposable python:alpine box ToFuPBTEN81O.
- Guest environment was nonempty and did not contain the synthetic value.
- HTTPS header echo returned the exact injected Authorization value.
- TLS verification remained enabled using the system CA bundle.
- Removed the test box in finally.

Earlier acceptance also covered custom headers, nonmatching hosts, missing headers, and stop/start persistence. Dashboard actions and live rotation are not claimed as tested.

## Multi-language acceptance

All six creation/request/cleanup paths passed with synthetic credentials:

| Runtime | Client | Test box | Result |
|---|---|---|---|
| Cloud | Python | ToFuPBTEN81O | PASS |
| Cloud | TypeScript | tWBRaM6du5eT | PASS |
| Cloud | Bash REST create + CLI exec | T42liNSCcCoG | PASS |
| Local | Python | 8jjCq9hZX3Lv | PASS |
| Local | TypeScript | 0hOo6z19UELC | PASS |
| Local serve | Bash REST create + CLI exec | rrMCu5q12uOX | PASS |

Local CLI 0.12.0 rejected the headers field with HTTP 422. Installed the current official CLI 0.13.1 into a temporary directory, restarted the isolated local server, and the local shell example passed. No user's default CLI was overwritten.

Public docs do not encode release versions; they require current clients and explain the old-server error. Python and Node examples use their own APIs; shell examples explicitly use REST because the CLI has no Secret creation flag.

## Real inference golden path

Extracted all six golden-path code blocks from the documentation and ran them with the previously authorized OpenAI-compatible provider. Changed the destination host, model, and provider-specific generation options (disabled thinking, 128 output tokens). No real credentials are included in documentation or this report. The default OpenAI endpoint and model were not tested with an OpenAI credential.

| Runtime | Client | Observed model reply | Cleanup |
|---|---|---|---|
| cloud | python | Hello! | Removed |
| cloud | typescript | Hello! How can I assist you today? | Removed |
| cloud | bash | Hello! How can I help you today? | Removed |
| local | python | Hello! How can I assist you today? | Removed |
| local | typescript | Hello! | Removed |
| local | bash | Hello! How can I help you today? | Removed |

One Cloud Python attempt returned empty model text despite exit 0; a repeat produced Hello. The local TypeScript image pull initially failed at Docker Hub authentication; a repeat succeeded. The first provider attempt used the wrong regional endpoint and returned 401; correcting it to the endpoint specified with the authorized credential resolved authentication. These failed attempts are not counted as successful inference.
