# BoxLite Documentation Site

## Project Overview

This is the official documentation site for **BoxLite** — a local-first micro-VM sandbox for AI agents. Stateful, lightweight, hardware-level isolation, no daemon required. The site is built with [Mintlify](https://mintlify.com) and deployed automatically on push to `main`.

- **BoxLite repo**: https://github.com/boxlite-ai/boxlite
- **SDKs**: Python, Node.js, Rust, Go, C, plus a built-in REST API (`boxlite serve`)
- **Platforms**: macOS (Apple Silicon), Linux (KVM), Windows (WSL2)

## Authoring Principles (must follow)

These two rules override convenience. Documentation that violates them ships incorrect information and erodes trust faster than missing content does.

### 1. Ground every claim in real code — never hallucinate

The source of truth is the BoxLite repository at https://github.com/boxlite-ai/boxlite, **not** prior conversations, training data, or memory. Before writing or editing any factual statement (API name, parameter, default, return type, error class, platform support, performance number, behavior under edge conditions):

- **Open the code first.** Verify against `sdks/{python,nodejs,rust,c,go}/`, `src/boxlite/`, `src/cli/`, `examples/`, the public README, and the latest tagged release notes. If the repo is not cloned locally, fetch the relevant file via `WebFetch` or `gh api repos/boxlite-ai/boxlite/contents/...`.
- **Cite specifically when behavior is non-obvious.** In your working notes (not necessarily in the published page) record the exact path you verified against, e.g. *"verified `disk_size_gb` default in `sdks/python/src/box_options.rs`"*. This makes review and future code-drift checks tractable.
- **Refuse to write what you cannot verify.** If you cannot find a feature in the code, do not document it — flag it for engineering instead. Conversely, if the code clearly does something the docs do not yet describe, raise that as a content gap, do not paper over it.
- **Watch for stale knowledge.** API surfaces evolve; assume any signature you "remember" is wrong until re-checked against the current default branch (or the version the docs target). Capability claims older than ~30 days deserve re-verification.
- **Mark uncertainty explicitly.** If a behavior is partially confirmed (e.g., works on macOS but Linux unchecked), say so in the page rather than generalizing.

### 1a. Stay strictly in the user's SDK frame — never quote or link to internal source

The published documentation describes BoxLite **as the user calls it** — SDK class and function names, options, return shapes, error strings. Internal implementation paths, Rust source files, line numbers, internal struct definitions, build scripts, and any artefact that lives below the SDK boundary do **not** belong in user-facing pages.

- Do **not** write `src/boxlite/...`, `sdks/python/src/...`, `src/deps/...`, `wire.go:81`, internal trait or struct names that the SDK does not export, or links into `github.com/boxlite-ai/boxlite/blob/main/src/...`.
- Do **not** paste Rust struct definitions, `pub` keywords, `Vec<...>`, `Option<...>`, lifetime annotations, or any other syntax that only appears in the runtime's source. If a user-facing concept needs a structured shape, render it as a **field table** or as a snippet in the user's actual SDK language.
- It is fine to link to the SDK module path users `import` (`github.com/boxlite-ai/boxlite/sdks/go`, `pip install boxlite`, `npm install @boxlite-ai/boxlite`), to the BoxLite README, to the OpenAPI spec, and to the upstream `examples/` directory — those are user-facing artefacts.
- Code-grounding still applies: every fact must be verified against the real source. The verification footprint goes into the internal `content-design/architecture-design/stage2-validation-log.md` (gitignored), never into the published page.

If a fact can only be expressed by pointing at internal source, it is the wrong fact for a user-facing page — either rephrase it in user terms, escalate it to engineering, or drop it.

### 2. Every demo code block must be end-to-end validated

A code block in the published docs is a contract: copy-paste, run, get the stated result. If a snippet has not been executed, it must not ship in a Tutorial or Quick Start. Do this before declaring a page complete:

- **Install the real SDK** at the version the docs target (`pip install boxlite` / `npm install boxlite` / `cargo add boxlite` / `go get …` / link `libboxlite`).
- **Run the snippet end-to-end** in a clean environment that matches the page's stated prerequisites (OS, Python/Node version, KVM availability). Capture actual stdout/stderr; the page's expected output must match what you saw.
- **Verify the failure modes you describe.** If the page says "exit code 137 on OOM" or "raises `BoxTimeoutError`", trigger the path and confirm the observation. Do not paraphrase plausible-sounding behavior.
- **Test multi-language tabs symmetrically.** A snippet behind every Tab must have been run in that language — not transliterated from one tab into another and shipped untested.
- **Re-run on bumps.** When pinning to a new SDK version or after a code change in the BoxLite repo, re-run the affected snippets. The CHANGELOG is not enough — APIs change in patch releases.
- **If you cannot run it, do not ship it as runnable.** Either get the prerequisites and run it, or downgrade the page from Tutorial / Quick Start to a Concept page that frames the snippet as illustrative pseudocode (and label it as such). Never publish unverified code under a tutorial heading.

When a code-grounded check or end-to-end run reveals a discrepancy with the existing docs, fix the docs in the same change — don't leave the contradiction in place "for later".

## Tech Stack

- **Mintlify** — documentation platform (config in `docs.json`)
- **MDX** — Markdown + JSX for page content
- **GitHub App** — auto-deploys to production on push to `main`

## Directory Structure

```
docs.json              # Mintlify config: navigation, theme, colors, logo
index.mdx              # Home page
faq.mdx                # FAQ & troubleshooting
getting-started/       # Installation + quickstarts + core concepts + design principles
concepts/              # Primitive deep-dives (lifecycle, execution, filesystem, network, snapshot)
tutorials/             # Step-by-step task tutorials
guides/                # How-to guides (production patterns) + changelog
reference/             # SDK API reference (python/, nodejs/, rust/, c/, go/, rest/)
architecture/          # Architecture, components, security, networking
development/           # Internal docs (CLI, Rust style guide) — files exist but currently hidden from navigation
snippets/              # Reusable MDX snippets (e.g., prerequisites.mdx)
images/                # Static images (hero, screenshots)
logo/                  # Light/dark SVG logos
.github/workflows/     # GitHub Actions (docs sync automation)
```

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
- All navigation is defined in `docs.json` under `navigation.tabs`
- 1 user-facing tab **BoxLite** with 8 groups: Introduction, Get Started, Concepts, Tutorials, How-to Guides, SDK Reference, Architecture, Resources. (`development/*.mdx` files are still in the repo but intentionally not in navigation right now.)
- **Never add a page to navigation without creating the file first**
- **Never remove a page without checking for inbound links**
- Placeholder pages have `placeholder: true` in frontmatter; treat them as not-yet-shipped content (Phase 2 will fill the bodies)

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

### Snippets
- Reusable content goes in `snippets/` and is included with `<Snippet file="filename.mdx" />`
- Currently: `snippets/prerequisites.mdx` (system requirements)

## Important Files

| File | Purpose |
|------|---------|
| `docs.json` | Mintlify config — navigation structure, theme, colors, logo, links |
| `index.mdx` | Home page — hero section, feature cards, entry points |
| `snippets/prerequisites.mdx` | Shared system requirements snippet |
| `.mintignore` | Files excluded from Mintlify build |
| `.github/workflows/sync-from-boxlite.yml` | Auto-syncs docs when BoxLite SDK PRs merge |

## Terminology

Use these terms consistently across all documentation:

| Term | Usage |
|------|-------|
| BoxLite | Local-first micro-VM sandbox (capital B, capital L) |
| LiteBox | The VM instance type (capital L, capital B) |
| box | Generic reference to a sandbox instance (lowercase) |
| SimpleBox / CodeBox / BrowserBox / ComputerBox / InteractiveBox | Specialized box types (Python and Node.js SDKs only) |
| Guest Agent | The agent running inside the VM |
| Jailer | The security isolation component |
| ShimController | Process lifecycle manager |
