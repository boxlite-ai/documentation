#!/usr/bin/env python3
"""Documentation lint for the BoxLite docs tree.

Currently enforces STYLE_GUIDE §12: no soft promises. "Not supported" is a fact a
reader can act on; "coming soon" is a promise nobody dated.

Usage:
    python3 scripts/lint-docs.py <docs_dir>

Exits non-zero on any violation, so it can gate CI.

The checker is fence-aware and inline-code-aware: a banned phrase inside a code
block or inline `code` span is a quoted SDK error message, not prose, and is
skipped. Prose exceptions are listed in ALLOWED_LINES.
"""

import re
import sys
from pathlib import Path

# §12.2 — banned in prose. Each entry: (regex, suggested replacement)
BANNED = [
    (r"\bcoming soon\b", "Not supported"),
    (r"\bnot yet supported\b", "not supported"),
    (r"\bnot currently supported\b", "not supported"),
    (r"\bplanned\b", "not supported"),
    (r"\bon the roadmap\b", "not supported"),
    (r"\bnot yet implemented\b", "not enforced / not implemented"),
    (r"\bnot yet enforced\b", "not enforced"),
    (r"\bdoes not yet\b", "does not"),
    (r"\bwill be supported\b", "state the current behaviour instead"),
    (r"\beventually\b", "state the current behaviour instead"),
    (r"\bwe plan\b", "state the current behaviour instead"),
    (r"\bin a future release\b", "state the current behaviour instead"),
    (r"\bstay tuned\b", "state the current behaviour instead"),
    (r"\bTBD\b", "state the current behaviour instead"),
]

# Agent-instruction files, which necessarily quote the banned phrases in order to
# ban them. Skipped only at the tree root — a nested README.md is a content page.
SKIP_FILES = {"CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "STYLE_GUIDE.md"}

# §12.3 — legitimate "not yet": a point-in-time state, not a future promise.
ALLOWED_LINES = [
    "VM not yet started",              # lifecycle state
    "Box not yet created",             # real SDK error message
    "the box is not yet ready",        # transient state
    "have not yet built a mental model",  # prose addressed to the reader
]


# Exact product statuses approved in the subscription design, not general promises.
SUBSCRIPTION_STATUS_LINES = {
    "| API key usage limits | — | — | Coming soon |",
    "| Enterprise SSO | — | — | Coming soon |",
}

def strip_inline_code(line: str) -> str:
    """Blank out `inline code` spans so quoted error strings are not flagged."""
    return re.sub(r"`[^`]*`", "``", line)


def check(path: Path) -> list[tuple[int, str, str, str]]:
    violations = []
    in_fence = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if any(allowed in raw for allowed in ALLOWED_LINES):
            continue
        if path.parts[-2:] == ("cloud", "plans.mdx") and raw.strip() in SUBSCRIPTION_STATUS_LINES:
            continue
        prose = strip_inline_code(raw)
        for pattern, suggestion in BANNED:
            match = re.search(pattern, prose, re.I)
            if match:
                violations.append((number, match.group(0), suggestion, raw.strip()))
    return violations


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2

    total = 0
    pages = sorted(
        p for p in [*root.rglob("*.md"), *root.rglob("*.mdx")]
        # Skip repo meta only at the root: a nested README.md is a content page.
        if not (p.parent == root and p.name in SKIP_FILES)
        and "scripts" not in p.parts
        and ".git" not in p.parts
    )
    for path in pages:
        for number, found, suggestion, line in check(path):
            total += 1
            print(f"{path}:{number}: soft promise {found!r} -> use {suggestion!r}")
            print(f"    {line[:120]}")

    if total:
        print(f"\n{total} violation(s). See STYLE_GUIDE.md §12.")
        return 1
    print(f"{root}: {len(pages)} pages checked, no soft promises")
    return 0


if __name__ == "__main__":
    sys.exit(main())
