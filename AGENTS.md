# BoxLite Documentation — Agent Instructions

This is the official documentation site for **BoxLite**, built with Mintlify. BoxLite is a local-first micro-VM sandbox for AI agents — stateful, lightweight, hardware-level isolation, no daemon required.

## Project Structure

- `docs.json` — Mintlify config: navigation groups, redirects, theme. Check before any structural change.
- `llms.txt` — machine-readable route index. Regenerate when navigation changes.
- `index.mdx` — home page · `faq.mdx` — FAQ and troubleshooting
- `getting-started/` — install plus one quickstart per language
- `manage-sandbox/` — box lifecycle, configuration, resources, volumes, network, secrets
- `agent-tools/` — capabilities an agent calls: exec, PTY, browser, desktop, MCP, git
- `agent-in-box/` — an agent living inside the box (Claude Code, tool loops, REST)
- `human-tools/` — handing a running box to a person (desktop, browser)
- `use-cases/` — end-to-end scenario guides, one complete deliverable per page
- `guides/` — production practices, build, deployment, error handling, registry
- `architecture/` — overview plus internals (components, security, networking, storage)
- `reference/` — SDK reference, **one page per language**, plus the CLI
- `development/` — contributor docs · `legal/` — CLA
- `assets/diagrams/` — rendered architecture diagrams (SVG)
- `scripts/` — tooling, not docs content (see `.mintignore`)

### Which directory does a new page belong in?

| Layer | Directories | Answers | Owns |
|---|---|---|---|
| **Capability page** | `manage-sandbox/` `agent-tools/` `human-tools/` | "What does this API do, what are its parameters?" | **The parameter tables** |
| **Scenario guide** | `use-cases/` | "How do I ship X end to end?" | The scenario, architecture, trust boundary |

A use-case guide must combine **two or more capabilities** toward a business outcome, and must **link** to capability pages instead of restating their parameter tables. If a proposed guide only re-teaches one capability, it belongs on that capability page instead.

One fact lives on exactly one page. Everything else links to it. When the same default value, error string, or parameter table appears on two pages, delete the copy and link.

### BoxLite Cloud (dual-product docs)

BoxLite Cloud ships in this repo and this `docs.json` as the `BoxLite Cloud` tab, with every page under `cloud/`. Keep it that way:

- One repo, one `docs.json` — never a separate repo or a second Mintlify project (parallel doc surfaces drift; this project has already lost 7 of 14 shared labels to it once).
- All Cloud content lives under `cloud/` — nested folders flatten to routes automatically, so the repo root grows by exactly one directory regardless of how many Cloud pages ship.
- Three layers: **product shell** (per product line, duplication intentional: auth, runtime handle, limits, billing, ops) · **shared body** (single file, linked from both tabs: box concepts, agent tools, use cases, SDK reference) · **seam** (shared pages must never assume how the runtime handle was obtained).
- Concepts are shared, code is not — local (`SimpleBox(...)`) and remote (`Boxlite.rest(...)`) have different `exec` signatures and teardown, and host bind mounts are ignored over REST. Shared pages get runtime-switchable code blocks, never one sample claimed to work for both.
- Every Cloud-versus-open-source difference lives on `cloud/vs-opensource`; other pages link there.
- Capability gaps are facts, not promises: "Disabled — the hosted service reports `snapshots_enabled` as false," never "not yet supported."

**Verifying a Cloud fact.** Cloud has no public source tree of its own, so a claim rests on one of these, preferred in this order: (1) the `boxlite` source at `origin/main`, including the Cloud API in `apps/api/` and the preview proxy in `apps/proxy/` — `apps/API.md` catalogues the platform routes; (2) the live console in a browser, for what only the product shows (plans, limits, dialog defaults, console wording); (3) unauthenticated route probes, where an existing route answers `401` and a missing one `404` — always probe a deliberately nonexistent route in the same run as a control. `GET /api/v1/config` (capability flags) and `GET /api/config` (client configuration) are public and need no credentials.

**Two customer-facing API surfaces, never blurred**: the SDK REST API under `/v1/...` (bearer `blk_live_...`, driven by `Boxlite.rest(...)`) and the platform API under `/api/...` (preview URLs, the public flag). Routes guarded by a platform admin role are not customer APIs — do not document them.

## Development Commands

```bash
mint dev              # Local preview at http://localhost:3000
mint broken-links     # Check for broken links
mint update           # Update Mintlify CLI
```

## Navigation

Navigation is defined in `docs.json` under `navigation.tabs` with 4 tabs:
1. **Documentation** — Getting Started, Architecture, FAQ
2. **SDK Reference** — Python, Node.js, Rust, C SDK reference pages
3. **Guides** — How-to guides
4. **Development** — CLI docs, Rust style guide

Rules:
- Never add a page to navigation without creating the `.mdx` file first
- Never remove a page without checking for inbound links from other pages
- Navigation order in `docs.json` determines sidebar order

## Writing Conventions

### Frontmatter (required on every page)
```yaml
---
title: "Page Title"
description: "One-line description for SEO and navigation"
sidebarTitle: "Short Nav Title"  # optional, if nav title differs
---
```

### Style
- Active voice, second person ("you")
- Sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for: file names, commands, paths, code references
- One idea per sentence
- Lead instructions with the goal, not the action

### Code Blocks
- Always include language identifier: ` ```python `, ` ```bash `, etc.
- Add filename title when relevant: ` ```python main.py `
- Use realistic parameter values, not `foo`/`bar`
- Include error handling in API examples

### MDX Components
Use Mintlify's built-in components — prefer them over raw HTML:
- `<Card>`, `<CardGroup>` — navigation cards
- `<Note>`, `<Warning>`, `<Tip>`, `<Info>` — callout boxes
- `<Tabs>`, `<Tab>` — tabbed content (e.g., platform-specific instructions)
- Full reference: https://mintlify.com/docs/components

## Terminology

Use these terms consistently:
- **BoxLite** — product name (capital B, capital L)
- **LiteBox** — the VM instance type
- **box** — generic reference to a sandbox instance (lowercase)
- **SimpleBox / CodeBox / BrowserBox** — Python SDK box types
- **Guest Agent** — agent running inside the VM
- **Jailer** — security isolation component
- **ShimController** — process lifecycle manager

## What to Avoid

- Don't edit `docs.json` without understanding the full navigation structure
- Don't use HTML when an MDX component exists for the same purpose
- Don't add pages to navigation that don't have corresponding `.mdx` files
- Don't alternate between synonyms for the same concept (pick one term, stick with it)

---

## Automated Documentation Sync

This section is for the Claude Code agent running in the `sync-from-boxlite` GitHub Actions workflow. When a PR merges in `boxlite-ai/boxlite`, this agent analyzes the diff and updates documentation accordingly.

### Source-to-docs mapping

Use this table to determine which documentation files to update based on changed source files in the boxlite repo.

| BoxLite source path | Documentation files to check |
|---|---|
| `sdks/python/**` | `reference/python.mdx`, `getting-started/quickstart-python.mdx` |
| `sdks/node/**` | `reference/nodejs.mdx`, `getting-started/quickstart-nodejs.mdx` |
| `src/boxlite/**` (public API) | `reference/rust.mdx`, `getting-started/quickstart-rust.mdx` |
| `sdks/c/include/boxlite.h` | `reference/c.mdx`, `getting-started/quickstart-c.mdx` |
| `src/boxlite/src/vmm/**`, `src/shim/**` | `architecture/core-components.mdx`, `architecture/security-and-isolation.mdx` |
| `src/boxlite/src/net/**` | `architecture/networking.mdx` |
| `src/boxlite/src/{rootfs,volumes,images}/**` | `architecture/storage.mdx` |
| `src/guest/**` | `architecture/core-components.mdx` |
| `README.md`, `CHANGELOG.md` | `guides/changelog.mdx`, `index.mdx` |
| `examples/**` | `use-cases/*.mdx`, `agent-tools/*.mdx` |
| `Cargo.toml`, `pyproject.toml`, `package.json` | Check for dependency or feature changes that affect quickstarts |

### Decision framework

Decide whether to update docs based on the nature of the change:

**Update docs when:**
- Public API added, changed, or removed (new methods, changed parameters, renamed types)
- New SDK feature or capability (new box type, new configuration option)
- Behavior change that affects users (default values changed, error handling updated)
- New examples or tutorials added upstream
- Installation or setup process changed
- New platform support or requirements changed

**Skip docs update when:**
- Internal refactoring with no public API change
- Test-only changes
- CI/CD pipeline changes in boxlite repo
- Code comments or internal documentation changes
- Performance optimizations with no API/behavior change
- Dependency bumps with no user-facing effect

**When unsure:** Create the PR anyway with a note explaining what changed and why you're unsure whether docs need updating. Let the human reviewer decide.

### PR and commit conventions

- **Branch name**: `docs-sync/boxlite-pr-{N}` where `{N}` is the source PR number
- **Commit message**: `docs: update {area} from boxlite PR #{N}` (e.g., `docs: update Python SDK reference from boxlite PR #142`)
- **PR title**: `docs: sync from boxlite PR #{N}`
- **PR body**: Include a link to the source PR and a summary of what changed and why
- **No version numbers**: Never add version numbers anywhere in documentation. Always describe features as current behavior.

### Do not write soft promises

**If something is unsupported, say "not supported".** Never write `coming soon`, `planned`, `not yet supported`, or `not currently supported`.

A `coming soon` makes a promise nobody dated: the reader waits, or chooses BoxLite on the assumption it will land, and gets burned. "Not supported" is a fact they can act on today — they pick an ARM64 Mac or Linux and move on. A capability list is a statement of fact, not a roadmap; roadmaps live in release notes and issues.

The word **`yet`** is the signal. Delete it and the sentence is usually correct.

| Do not write | Write instead |
|---|---|
| `coming soon` / `planned` / `on the roadmap` | `Not supported` |
| `not yet supported` / `not currently supported` | `not supported` |
| `not yet implemented` / `not yet enforced` | `accepted but not enforced` |
| `does not yet guarantee` | `does not guarantee` |

Legitimate exceptions — these describe a point-in-time state, not a future promise, and must not be rewritten: real SDK error strings (`Error: Box not yet created...`), lifecycle descriptions ("VM not yet started"), transient states ("the box is not yet ready"), and prose addressed to the reader ("if you have not yet read...").

The subscription design explicitly labels API key usage limits and Enterprise SSO as `Coming soon`. Only these two exact status rows in `cloud/plans.mdx` are allowed; the page must also state that they are not available entitlements. Do not extend this exception to other capabilities or prose.

`scripts/lint-docs.py` enforces this in CI. Run it before opening a PR:

```bash
python3 scripts/lint-docs.py .
```

### MDX parser hazards

`.mdx` is JSX-flavoured. In prose (outside code fences), these break the build:

- `<SOMETHING>` is parsed as a JSX tag. Wrap placeholders in backticks: `` `<YOUR_API_KEY>` ``, never bare.
- `{...}` is parsed as a JavaScript expression. Wrap paths and objects in backticks: `` `GET /executions/{id}` ``.

Inside fenced code blocks both are safe. Placeholders use the `<YOUR_THING>` form — angle brackets, not square brackets, since `[...]` is link syntax.
