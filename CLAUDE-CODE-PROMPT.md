# Paste this whole file into Claude Code

---

You are publishing a **new, standalone static site repo**. Read every
constraint before acting.

## Context

`C:\Users\HP\Desktop\amazebase-landing` is the AmazeBase marketing landing
page. It is a **separate repo from `amz-analytics`** and must stay that way.
It is already a git repository on branch `main`, working tree clean,
38 tracked files, ~6.2 MB.

It is 100% static: `index.html` + `css/` + `js/main.js` + `assets/img/` +
`Images/` (4 curve PNGs). No Python, no build step, no backend, no npm.

**Do NOT touch `C:\Users\HP\Desktop\amz_v2` in this task.** Not the code, not
`server_v2.py`, not its git repo, not its Railway service. Different repo,
different service. If you find yourself running git inside `amz_v2`, stop.

**Do NOT add** `railway.json`, `Procfile`, `runtime.txt`, `package.json`,
`Dockerfile`, `Staticfile`, or a `Caddyfile`. Railway's builder (Railpack)
detects `index.html` in the repo root, classifies it as a static site, and
serves it with Caddy. Adding any of those files changes detection and is a
regression. Zero config is the design.

## Project doctrine that applies to you here

From `amz_v2\PROJECT_STATE.md` §0 and §2:

- Leon is non-technical. Show him plain English; show ME raw evidence.
- **Never report success without raw output.** A summary instead of raw bytes
  is a red flag. Print the actual command output, unedited.
- All-or-nothing: if any pre-check below fails, **write nothing, change
  nothing, and report the failure**. Do not "fix it and continue".
- One concern per run. Your concern is: publish this repo to GitHub. Nothing
  else.

## Step 1 — Pre-checks (read-only, must all pass)

Run these from `C:\Users\HP\Desktop\amazebase-landing` and **print the raw
output of each**:

```
git -C "C:\Users\HP\Desktop\amazebase-landing" rev-parse --show-toplevel
git -C "C:\Users\HP\Desktop\amazebase-landing" status --short --branch
git -C "C:\Users\HP\Desktop\amazebase-landing" log --oneline
git -C "C:\Users\HP\Desktop\amazebase-landing" ls-files | find /c /v ""
git -C "C:\Users\HP\Desktop\amazebase-landing" remote -v
```

Required results:

- toplevel is `C:/Users/HP/Desktop/amazebase-landing` — **not** anything under
  `amz_v2`
- branch is `main`, working tree clean
- at least 3 commits present
- exactly 38 tracked files
- **no remote named `origin` yet** — if one exists, STOP and report it

Then confirm no dev-only files leaked in:

```
git -C "C:\Users\HP\Desktop\amazebase-landing" ls-files | findstr /i "hero-editor _measure preview-standalone curve-color-test curve-glow"
```

This must return **nothing**. If it returns any line, STOP and report.

## Step 2 — Create the GitHub repo and push

Target: a **new** repo `amazebase-landing` under the `silvaeleon` account.
It must NOT be pushed into `silvaeleon/amz-analytics`.

Check whether the GitHub CLI is available and authenticated:

```
gh auth status
```

**If `gh` is available and authenticated**, create and push in one go:

```
cd /d "C:\Users\HP\Desktop\amazebase-landing"
gh repo create amazebase-landing --private --source=. --remote=origin --push
```

**If `gh` is NOT available or not authenticated**, do not try to install it and
do not attempt to authenticate. Instead, stop and tell Leon in plain English
to create an empty repo at https://github.com/new named `amazebase-landing`
(no README, no .gitignore, no licence), and report back. Then on the next run:

```
cd /d "C:\Users\HP\Desktop\amazebase-landing"
git remote add origin https://github.com/silvaeleon/amazebase-landing.git
git push -u origin main
```

## Step 3 — Prove it (raw output required)

```
git -C "C:\Users\HP\Desktop\amazebase-landing" remote -v
git -C "C:\Users\HP\Desktop\amazebase-landing" log --oneline -1
git -C "C:\Users\HP\Desktop\amazebase-landing" status --short --branch
git -C "C:\Users\HP\Desktop\amazebase-landing" ls-remote --heads origin
```

Then confirm, and print the raw evidence for each:

1. `origin` points at `silvaeleon/amazebase-landing` — **not** `amz-analytics`
2. status shows `## main...origin/main` with nothing ahead or behind
3. `ls-remote` shows `refs/heads/main` at the same SHA as your local HEAD

Finally, verify you did not disturb the app repo — print this raw:

```
git -C "C:\Users\HP\Desktop\amz_v2" status --short --branch
git -C "C:\Users\HP\Desktop\amz_v2" log --oneline -1
```

The `amz_v2` HEAD commit must be unchanged and no new commits made by you.

## Report back

Give Leon:

- one plain-English line: published or not
- the repo URL
- the HEAD SHA on GitHub
- confirmation that `amz_v2` was untouched, with the raw `git log -1` line

Do not proceed to Railway. Leon does that part himself in the dashboard.
