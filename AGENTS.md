# BoxLite Documentation — Agent Instructions

This is the official documentation site for **BoxLite**, built with Mintlify. BoxLite is a lightweight, embeddable VM runtime for secure, isolated code execution.

## Project Structure

- `docs.json` — Mintlify config (navigation, theme, colors, logo). Check before making structural changes.
- `index.mdx` — Home page
- `getting-started/` — Quickstart guides (Python, Node.js, Rust, C)
- `architecture/` — Architecture deep dives (components, security, networking)
- `reference/` — SDK API reference (`python/`, `nodejs/`, `rust/`, `c/`)
- `guides/` — How-to guides (build from source, examples, AI integration, etc.)
- `development/` — Internal docs (CLI, Rust style guide)
- `snippets/` — Reusable MDX snippets (included via `<Snippet file="..." />`)
- `images/`, `logo/` — Static assets

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
- `<Snippet file="filename.mdx" />` — reusable content from `snippets/`
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
