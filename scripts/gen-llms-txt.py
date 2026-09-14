#!/usr/bin/env python3
"""Generate llms.txt from docs.json and each page's own frontmatter.

Why generated rather than hand-maintained: llms.txt duplicates two facts that
already live elsewhere — the navigation tree (docs.json) and each page's title
and description (its frontmatter). Maintaining a third copy by hand means it
silently rots. When this script was written the committed llms.txt had five
dead links (`manage-sandbox/configuration`, `guides/production-best-practices`,
`guides/building-from-source`, `guides/macos-sandbox-debugging`,
`architecture/internals` — all renamed, moved, or deleted in earlier passes),
group names from a superseded IA, and no BoxLite Cloud section at all.

Usage:
    python3 scripts/gen-llms-txt.py            # write llms.txt
    python3 scripts/gen-llms-txt.py --check    # exit 1 if llms.txt is stale

The --check mode is what CI should run: it makes staleness a build failure
instead of something a reader discovers.

Links use the `.md` suffix, not `.mdx`. Mintlify serves raw markdown at
`/route.md` and the rendered page at `/route`, but `/route.mdx` is a 404 —
which is what every link in the previously hand-maintained llms.txt pointed
at, so the whole index was dead for its only audience.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION_LIMIT = 140  # keep one entry to one readable line

HEADER = """# BoxLite Documentation

> BoxLite is an embeddable microVM sandbox for AI agents — stateful, sub-second boot, hardware-level isolation, no daemon required.
"""


def frontmatter(route: str) -> tuple[str, str]:
    """(title, description) from a page's own frontmatter — the single source."""
    path = ROOT / f"{route}.mdx"
    if not path.exists():
        raise FileNotFoundError(f"docs.json lists {route} but {path.name} is missing")
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return route, ""
    block = text.split("---", 2)[1]
    def field(name: str) -> str:
        m = re.search(rf'^{name}:\s*"(.*)"\s*$', block, re.M)
        return (m.group(1) if m else "").replace('\\"', '"')
    title = field("title") or route
    description = field("description")
    if len(description) > DESCRIPTION_LIMIT:
        description = description[:DESCRIPTION_LIMIT].rstrip() + "…"
    return title, description


def build() -> str:
    nav = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))["navigation"]
    out = [HEADER]
    for tab in nav["tabs"]:
        out.append(f"## {tab['tab']}\n")
        for group in tab["groups"]:
            out.append(f"### {group['group']}")
            routes = ([group["root"]] if "root" in group else []) + group["pages"]
            for route in routes:
                title, description = frontmatter(route)
                suffix = f": {description}" if description else ""
                out.append(f"- [{title}](/{route}.md){suffix}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    generated = build()
    target = ROOT / "llms.txt"
    if "--check" in sys.argv:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != generated:
            print("llms.txt is stale. Run: python3 scripts/gen-llms-txt.py")
            return 1
        print("llms.txt is up to date.")
        return 0
    target.write_text(generated, encoding="utf-8")
    entries = generated.count("\n- [")
    print(f"wrote llms.txt: {entries} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
