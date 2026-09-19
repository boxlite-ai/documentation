# Contribute to the BoxLite documentation

This repo is the docs site at **https://docs.boxlite.ai**. It is built with
[Mintlify](https://mintlify.com): `docs.json` holds the navigation and theme,
every page is an `.mdx` file, and **a push to `main` deploys production**.

This guide covers how to ship a change. The rules for *what to write* live in
`AGENTS.md` / `CLAUDE.md` at the repo root — read those before your first page.

---

## Step 0 — find out what access you have

This decides your whole workflow, so check it before anything else:

```bash
gh api repos/boxlite-ai/documentation --jq .permissions
```

| What it prints | What you can do |
|---|---|
| `"push": true` | Create branches directly on `boxlite-ai/documentation` |
| `"push": false` | **Fork the repo.** You cannot push a branch here, so `npm run deploy:preview` will fail |

Most new joiners start at `read` (`"push": false`). That is normal — take
**Path B** below. Ask an admin (currently @DorianZheng) if you need write.

---

## Setup (once)

```bash
git clone https://github.com/boxlite-ai/documentation.git
cd documentation
npm i -g mint    # Mintlify CLI (Node 18+)
brew install gh  # GitHub CLI
```

If you are on Path B, also fork on GitHub and add your fork as a remote:

```bash
gh repo fork boxlite-ai/documentation --remote=false
git remote add fork https://github.com/<YOUR_GITHUB_USER>/documentation.git
```

---

## The lifecycle

### Path A — you have write access

```
①  git switch -c docs/your-change     branch from an up-to-date main
②  edit pages
③  npm run dev                        local preview, http://localhost:3000
④  git commit -am "docs: ..."
⑤  npm run check                      mint validate && mint broken-links
⑥  python3 scripts/lint-docs.py .     the same check CI runs
⑦  python3 scripts/gen-llms-txt.py    regenerate if you touched nav OR frontmatter
⑧  npm run deploy:preview             push + open PR; Mintlify builds a preview
⑨  review the *.mintlify.app link     light/dark, desktop/mobile
⑩  gh pr merge <PR#> --squash --delete-branch
                                      main updates → production deploys (~1 min)
```

### Path B — you have read access

Identical, except you push to your fork and open the PR across:

```bash
git switch -c docs/your-change
# ... edit, preview, check, commit ...
git push -u fork docs/your-change
gh pr create --repo boxlite-ai/documentation --base main \
  --head <YOUR_GITHUB_USER>:docs/your-change --fill
```

Mintlify posts the preview link on the PR either way. You will need a
maintainer to merge.

### No clone at all

For a typo: open the page on github.com, click the pencil icon — GitHub forks
for you — and open a PR. Mintlify still builds a preview.

---

## What the robots check

`.github/workflows/docs-lint.yml` runs on every PR **and** on every push to
`main`. Two steps, both of which you can run locally in a second:

| CI step | Local command | What it rejects |
|---|---|---|
| No soft promises | `python3 scripts/lint-docs.py .` | `coming soon`, `planned`, `not yet supported` — see the soft-promises section in `AGENTS.md` |
| llms.txt in sync | `python3 scripts/gen-llms-txt.py --check` | An `llms.txt` that no longer matches `docs.json` and page frontmatter |

`npm run check` (`mint validate && mint broken-links`) is **not** in CI. Run it
yourself — a broken link ships happily without it.

### The trap: the deploy does not wait for CI

Mintlify's GitHub App and GitHub Actions are independent. A push to `main` with
a **failing** lint still deploys. This is not theoretical — commits `f48f6d9`
and `4598403` shipped correct pages to production while `Docs lint` was red for
a full day, because `llms.txt` had gone stale and nobody was looking at the
Actions tab.

So: **a correct site is not evidence of a green repo.** After anything lands on
`main`, check it:

```bash
gh run list --repo boxlite-ai/documentation --workflow docs-lint.yml --limit 3
```

---

## Rules of the road

- **Do not push to `main` directly.** Production is "merge the PR". Note that
  this is *team policy, not a guardrail* — the `main` ruleset only blocks
  deletion and force-pushes, so nothing stops a direct push. Do not rely on
  GitHub to catch you.
- **Preview = PR.** Mintlify builds a preview when a PR is opened against
  `main`, not on a bare branch push, and rebuilds on every push to that PR.
- **Never delete or rename a page without a `redirects` entry** in `docs.json`.
  Every route that has ever shipped must keep resolving.
- **Never add a page to navigation before the file exists.**
- **There is no `mint deploy`.** Mintlify only publishes what lands on `main`.

---

## Writing: the short version

The full rules are in `AGENTS.md` / `CLAUDE.md`. These are the ones that get
violated most often:

- **Verify, then write.** Every factual claim rests on source you read, output
  you ran, or a live probe you made. Never on recall and never on "it should
  be". If you cannot verify it, do not publish it.
- **One fact lives on exactly one page.** Everything else links to it. When the
  same default value or parameter table appears twice, delete the copy.
- **If something is unsupported, write "not supported".** Never `coming soon`.
  The word `yet` is the signal — delete it and the sentence is usually right.
- **Active voice, second person, one idea per sentence.**
- **Code blocks must be runnable as-is** — imports, initialization, and error
  handling included. Placeholders look like `<YOUR_API_KEY>`.
- **MDX is JSX-flavoured.** Outside code fences, a bare `<SOMETHING>` is parsed
  as a tag and a bare `{...}` as an expression. Wrap both in backticks.

### Verifying a claim about Cloud

Cloud has no public source tree, so a claim rests on one of these, in order:

1. The `boxlite` source at `origin/main` for anything the SDK, CLI, or REST
   client does.
2. The live console, for anything only the product shows.
3. **Route probes with a control.** An existing route answers `401`, a missing
   one `404`. Always probe a deliberately nonexistent route in the same run —
   without the control the inference is worthless.

```bash
curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' \
  https://api.boxlite.ai/v1/boxes                 # 401 → route exists
curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' \
  https://api.boxlite.ai/v1/definitely-not-real   # 404 → control
```

`GET /api/config` and `GET /api/v1/config` report Cloud's own configuration and
need no credentials. Prefer them over assumptions.

---

## Traps that have actually bitten us

Each of these cost real time. They are here so they cost you none.

| Trap | What happened | What to do |
|---|---|---|
| **`llms.txt` stales on *frontmatter* edits** | A page title changed, nobody regenerated, `main` went red for a day | Run `gen-llms-txt.py` after editing a title or description, not just after nav changes |
| **A find-and-replace breaks the prose explaining it** | Replacing a base URL left two troubleshooting rows blaming "the missing `/api` suffix" for a failure that could no longer happen | After any bulk replace, grep the prose around every hit |
| **Published ≠ correct** | Cloud pages taught one API host and the SDK reference taught another, for months | Treat existing pages as claims to verify, not as sources |
| **Your DNS can lie** | A local VPN resolved every host to a `198.18.0.x` fake IP, making a live host look dead | Cross-check with DNS-over-HTTPS: `curl -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=api.boxlite.ai&type=A'` |
| **Environment limits are not doc bugs** | Some failures are your laptop, not the product | Reproduce a second way before filing it as a defect |

---

## Where things live

| Path | What it is |
|---|---|
| `docs.json` | Navigation, redirects, theme |
| `AGENTS.md` / `CLAUDE.md` | The content rules |
| `custom.css` | The terminal/ASCII design system |
| `llms.txt` | Generated route index — never hand-edit |
| `scripts/` | Tooling, excluded from the build by `.mintignore` |
| `cloud/` | Everything BoxLite Cloud. Keep it that way |
| `reference/` | One page per language, plus the CLI |
| `use-cases/` | End-to-end guides — one complete deliverable per page |
