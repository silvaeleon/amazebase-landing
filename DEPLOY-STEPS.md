# Deploying the landing page

Two parts. **Part 1** you hand to Claude Code. **Part 2** you click yourself in
the Railway dashboard, because the Chrome extension can't reach it (§3).

Nothing here touches `amz_v2`, `server_v2.py`, or your live app service.

---

## Part 1 — Publish to GitHub (Claude Code does this)

Upload **`CLAUDE-CODE-PROMPT.md`** (in this same folder) to Claude Code and
tell it to follow it.

That prompt already tells it to:

- refuse to touch the `amz_v2` repo
- refuse to add `railway.json` / `Procfile` / `package.json` / a `Caddyfile`
- run read-only pre-checks first and abort on any mismatch
- print **raw command output**, not a summary

**When it reports back, paste the raw output to me.** Per §2 doctrine, a "done"
or a summary instead of raw evidence is a red flag — I'll check the actual
bytes before you go near Railway.

What you're looking for in its output:

- `origin` = `silvaeleon/amazebase-landing` — **not** `amz-analytics`
- `## main...origin/main` with nothing ahead
- `amz_v2` HEAD commit unchanged

If it says the GitHub CLI isn't authenticated, it will stop and ask you to
create an empty repo at https://github.com/new named `amazebase-landing`
(no README, no .gitignore, no licence). Do that, then run it again.

---

## Part 2 — Create the Railway service (you click)

1. Go to **https://railway.com/dashboard** and sign in.

2. Click **New Project** — a *new* project, not the one running your app.
   Keeps billing, variables and environments separate from production.

3. Choose **Deploy from GitHub repo**.

4. First time only: Railway asks to install its GitHub app. Click
   **Configure GitHub App**, and when GitHub asks which repositories,
   **make sure `amazebase-landing` is ticked**. Save.

5. Pick **`amazebase-landing`**.

6. It builds immediately. In the **Deploy Logs** you want to see it detect a
   **static site** and build with **Caddy** — roughly a minute.

   - Do **not** set a Root Directory. The repo root is the site.
   - Do **not** set a Start Command.
   - Change no build settings at all.

   If the logs mention Python, uvicorn, or Nixpacks — stop and send them to me.
   That would mean it picked the wrong builder.

7. Deploy green → open the service → **Settings → Networking →
   Public Networking → Generate Domain**. Leave the port field default.

8. Click the `*.up.railway.app` URL.

---

## Part 3 — Check it

- [ ] Loads with **no login screen** — this service has no auth at all
- [ ] Open in an **incognito window** — proves it's genuinely public
- [ ] Hero shows the dashboard screenshot with the glow curves behind it
- [ ] Scroll the whole page — feature icons and partner logos all render,
      no broken-image boxes
- [ ] **No purple "⚙ Editor" button** bottom-left
- [ ] `https://amz-analytics-production.up.railway.app/health` still returns
      `build="phase1-v3"`, `db_backend=postgresql` — proves the app is untouched

Send me the URL and anything that looks wrong.

---

## After it's proven live

Per §0, the work isn't finished until `PROJECT_STATE.md` records it. Once the
site is up I'll write the CHANGELOG entry and a new section covering: the repo,
the Railway service, the zero-config Caddy setup, and the commit SHA — with the
evidence, not a "done".

---

## Later

**Custom domain:** Railway → service → Settings → Networking → Custom Domain.
It gives you a CNAME to add wherever you buy the domain. HTTPS is automatic.

**Signup wiring:** when the signup button needs to reach the app, the page will
POST to `amz-analytics-production.up.railway.app`. That needs a CORS allowance
for this origin on the FastAPI side, and `PROVISIONING_ENABLED` is currently
`false` (§3), so `/auth/register` returns 403 today. Separate concern, separate
chat — §7 ownership rules apply.

---

## Making changes from now on

Edit files in `C:\Users\HP\Desktop\amazebase-landing`, then have Claude Code
commit and push to `main`. Railway redeploys itself in a minute or two. No
build step, no `verify_v3.py` gate — that rule is for `amz_v2`'s v3 front-end,
not this repo.

> The old working folder `amz_v2\Landing Page` still has the dev tools and the
> 34 MB of source artwork. Fine to keep designing there — but only changes made
> in `amazebase-landing` go live.
