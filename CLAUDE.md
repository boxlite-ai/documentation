# BoxLite Documentation Site

## Project Overview

This is the official documentation site for **BoxLite** — a local-first micro-VM sandbox for AI agents. Stateful, lightweight, hardware-level isolation, no daemon required. The site is built with [Mintlify](https://mintlify.com) and deployed automatically on push to `main`.

- **BoxLite repo**: https://github.com/boxlite-ai/boxlite
- **BoxRun repo**: https://github.com/boxlite-ai/boxrun
- **Current versions**: BoxLite Python v0.10.0, Node.js v0.10.0, Rust crate v0.10.0, Go v0.10.0. The Node darwin-arm64 native package is published only up to v0.9.7, so `npm install @boxlite-ai/boxlite@latest` fails to load on Apple Silicon — see the Node quickstart troubleshooting.
- **Platforms**: macOS (Apple Silicon), Linux (KVM), Windows (WSL2)

## Tech Stack

- **Mintlify** — documentation platform (config in `docs.json`)
- **MDX** — Markdown + JSX for page content
- **GitHub App** — auto-deploys to production on push to `main`

## Directory Structure

```
docs.json              # Mintlify config: navigation groups, redirects, theme
llms.txt               # Machine-readable route index — regenerate when navigation changes
index.mdx              # Home page
faq.mdx                # FAQ & troubleshooting
getting-started/       # Install + one quickstart per language
manage-sandbox/        # Box lifecycle, configuration, resources, volumes, network, secrets
agent-tools/           # Capabilities an agent calls: exec, PTY, browser, desktop, MCP, git
agent-in-box/          # An agent living inside the box (Claude Code, tool loops, REST)
human-tools/           # Handing a running box to a person (desktop, browser)
use-cases/             # End-to-end scenario guides (one complete deliverable per page)
guides/                # Production practices, build, deployment, error handling, registry
architecture/          # Overview + internals (components, security, networking, storage)
reference/             # SDK reference — ONE page per language, plus the CLI
development/           # Contributor docs (CLI dev, local E2E, Rust style, investigations)
legal/                 # CLA
assets/diagrams/       # Rendered architecture diagrams (SVG)
scripts/               # Tooling, not docs content (see .mintignore)
.github/workflows/     # GitHub Actions, including docs sync automation
```

### Which directory does a new page belong in?

The distinction that keeps this site free of duplication:

| Layer | Directories | Answers | Owns |
|---|---|---|---|
| **Capability page** | `manage-sandbox/` `agent-tools/` `human-tools/` | "What does this API do, what are its parameters?" | **The parameter tables** |
| **Scenario guide** | `use-cases/` | "How do I ship X end to end?" | The scenario, architecture, trust boundary |

A use-case guide must combine **two or more capabilities** toward a business outcome, and must **link** to capability pages instead of restating their parameter tables. If a proposed guide only re-teaches one capability, it belongs on that capability page instead.

One fact lives on exactly one page. Everything else links to it. When you find the same default value, error string, or parameter table on two pages, delete the copy and link.

### BoxLite Cloud (dual-product docs)

BoxLite Cloud ships in this repo and this `docs.json` as the `BoxLite Cloud` tab, with every page under `cloud/`. Keep it that way:

- **One repo, one `docs.json`.** Never split Cloud into a separate repo or a second Mintlify project. Parallel doc surfaces drift — this project has direct evidence of it (`docs.json` + `mkdocs.yml` + README + homepage nav table previously drifted on 7 of 14 shared labels).
- **All Cloud content lives under `cloud/`.** Nested folders flatten to routes automatically, so however many Cloud pages ship, the repo root only ever grows by that one directory — not a dozen new top-level ones.
- **Three layers, not a duplicated tree:**

  | Layer | Owner | Content |
  |---|---|---|
  | Product shell | Per product line, duplication intentional | Auth, getting a runtime handle, limits, billing, ops |
  | Shared body | Single file, linked from both tabs | Box concepts, agent tools, use cases, SDK reference |
  | Seam | Contract, not content | Shared pages must never assume how the runtime handle was obtained |

- **Concepts are shared, code is not.** Local (`SimpleBox(...)`) and remote (`Boxlite.rest(...)`) have different call shapes — different `exec` signature, different teardown, host bind mounts ignored over REST. A shared page gets runtime-switchable code blocks (local / remote); it never claims one code sample works for both.
- **Every Cloud difference lives on `cloud/vs-opensource`.** Other pages link there instead of restating differences.
- Capability gaps are facts, not promises: "Disabled — the hosted service reports `snapshots_enabled` as false," never "not yet supported."

#### Verifying Cloud facts

Cloud has no public source tree of its own, so a claim about it must rest on one of these, in this order of preference:

1. **The `boxlite` source at `origin/main`** for anything the SDK, CLI, or REST client does — including the Cloud-facing API surface (`apps/api/`) and the preview proxy (`apps/proxy/`). `apps/API.md` catalogues the platform routes.
2. **The live console**, operated in a browser, for anything only the product shows — plans, limits, dialog defaults, console wording.
3. **Unauthenticated route probes** to tell a real route from a missing one: an existing route answers `401`, a missing one `404`. Always probe a deliberately nonexistent route in the same run as a control, or the inference is worthless.

Two public endpoints report Cloud's own configuration and need no credentials: `GET /api/v1/config` returns capability flags, and `GET /api/config` returns client configuration. Prefer them over assumptions about what Cloud enables.

There are **two customer-facing API surfaces**, and pages must not blur them: the SDK REST API under `/v1/...` (bearer `blk_live_...` key, what `Boxlite.rest(...)` drives) and the platform API under `/api/...` (preview URLs, the public flag). Routes guarded by a platform admin role are not customer APIs — do not document them.

## Common Tasks

```bash
# Preview locally
mint dev               # → http://localhost:3000

# Check for broken links
mint broken-links

# Update Mintlify CLI
mint update
```

## Key Conventions

### Page Structure
- Every `.mdx` page must have frontmatter with `title` and `description`
- Use `sidebarTitle` in frontmatter when the nav title should differ from the page title
- Start with introductory context before diving into steps

### Navigation
- All navigation is defined in `docs.json` under `navigation.groups`
- **Never add a page to navigation without creating the file first**
- **Never delete or rename a page without adding a `redirects` entry** in `docs.json` — every route that has ever shipped must keep resolving
- Regenerate `llms.txt` whenever navigation changes

### Writing Style
- Active voice, second person ("you")
- Sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for: file names, commands, paths, code references
- One idea per sentence

### MDX Components
- Use Mintlify built-in components (`Card`, `CardGroup`, `Note`, `Warning`, `Tip`, `Tabs`, `Tab`, `Snippet`, etc.)
- Prefer MDX components over raw HTML
- Code blocks: always include language identifier, add `filename.ext` title when relevant
- Use realistic parameter values, not `foo`/`bar` placeholders

### Theming & design system
The site uses an **ASCII / terminal** design language mirroring the BoxLite console
restyle ([boxlite-ai/boxlite#829](https://github.com/boxlite-ai/boxlite/pull/829)).
Tokens are split across two files:
- `docs.json` → `colors` (`primary` `#00B0F0`), `appearance.default: dark`,
  `fonts` (heading `IBM Plex Mono`, body `Inter`), `background.color`,
  `styling.codeblocks` (github theme).
- `custom.css` → everything Mintlify config can't express: square corners (radius 0),
  bordered card/code surfaces, terminal-dark code panel, cyan step markers, uppercase
  sidebar labels, recolored callouts. Mintlify auto-loads any root `custom.css`.

| Token | Dark | Light |
|-------|------|-------|
| accent (brand) | `#00B0F0` | `#00B0F0` |
| page bg | `#13161B` | `#FFFFFF` |
| card | `#1A1D24` | `#F3F4F6` |
| code panel | `#0D0F13` | `#F7F9FC` |
| border | `#2A2F3A` | `#E2E5EA` |

When adding CSS, target stable Mintlify hooks (`.card`, `.code-block`, `.callout`,
`.steps`, `.sidebar-title`, `table.table`) — utility classes are unstable. Verify both
themes with `mint dev`; mind that Mintlify ships some rules `!important`, so overrides
may need higher specificity (see the code-panel block in `custom.css`).

## Important Files

| File | Purpose |
|------|---------|
| `docs.json` | Mintlify config — navigation structure, theme, colors, logo, links |
| `custom.css` | Terminal/ASCII design system — square corners, surfaces, code panel, accents |
| `index.mdx` | Home page — hero section, feature cards, entry points |
| `.mintignore` | Files excluded from Mintlify build |
| `.github/workflows/sync-from-boxlite.yml` | Auto-syncs docs when BoxLite SDK PRs merge |

## Terminology

Use these terms consistently across all documentation:

| Term | Usage |
|------|-------|
| BoxLite | Local-first micro-VM sandbox (capital B, capital L) |
| BoxRun | Sandbox management platform (capital B, capital R) |
| LiteBox | The VM instance type (capital L, capital B) |
| box | Generic reference to a sandbox instance (lowercase) |
| SimpleBox / CodeBox / BrowserBox | Python/Node.js SDK box types |
| BoxHandle | BoxRun SDK handle to a specific box |
| BoxRunClient | BoxRun Python SDK client class |
| Guest Agent | The agent running inside the VM |
| Jailer | The security isolation component |
| ShimController | Process lifecycle manager |

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

`scripts/lint-docs.py` enforces this in CI. Run it before opening a PR:

```bash
python3 scripts/lint-docs.py .
```

### MDX parser hazards

`.mdx` is JSX-flavoured. In prose (outside code fences), these break the build:

- `<SOMETHING>` is parsed as a JSX tag. Wrap placeholders in backticks: `` `<YOUR_API_KEY>` ``, never bare.
- `{...}` is parsed as a JavaScript expression. Wrap paths and objects in backticks: `` `GET /executions/{id}` ``.

Inside fenced code blocks both are safe. Placeholders use the `<YOUR_THING>` form — angle brackets, not square brackets, since `[...]` is link syntax.
