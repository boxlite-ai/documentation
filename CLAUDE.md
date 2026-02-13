# BoxLite Documentation Site

## Project Overview

This is the official documentation site for **BoxLite** — a local-first micro-VM sandbox for AI agents. Stateful, lightweight, hardware-level isolation, no daemon required. The site is built with [Mintlify](https://mintlify.com) and deployed automatically on push to `main`.

- **BoxLite repo**: https://github.com/boxlite-ai/boxlite
- **BoxRun repo**: https://github.com/boxlite-ai/boxrun
- **Current versions**: BoxLite Python v0.5.11 (stable), Node.js v0.2.8, C v0.5.11; BoxRun latest
- **Platforms**: macOS (Apple Silicon), Linux (KVM), Windows (WSL2)

## Tech Stack

- **Mintlify** — documentation platform (config in `docs.json`)
- **MDX** — Markdown + JSX for page content
- **GitHub App** — auto-deploys to production on push to `main`

## Directory Structure

```
docs.json              # Mintlify config: navigation, theme, colors, logo
index.mdx              # Home page
faq.mdx                # FAQ & troubleshooting
getting-started/       # Quickstart guides (Python, Node.js, Rust, C)
architecture/          # Architecture, components, security, networking
reference/             # SDK API reference (python/, nodejs/, rust/, c/)
boxrun/                # BoxRun platform docs (CLI, Python SDK, REST API, config)
guides/                # How-to guides (build, examples, AI integration, etc.)
development/           # Internal docs (CLI, Rust style guide)
snippets/              # Reusable MDX snippets (e.g., prerequisites.mdx)
images/                # Static images (hero, screenshots)
logo/                  # Light/dark SVG logos
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
- 4 tabs: Documentation, SDK Reference, Guides, Development
- **Never add a page to navigation without creating the file first**
- **Never remove a page without checking for inbound links**

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
