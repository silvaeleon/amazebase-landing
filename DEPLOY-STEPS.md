# Deploying the landing page — click-by-click

Everything on your side is already prepared. The folder
`C:\Users\HP\Desktop\amazebase-landing` is a git repository with one commit
containing 36 files. You do two things: publish it to GitHub, then point
Railway at it.

**Time: about 10 minutes. Nothing here can affect your existing app.**

---

## Part 1 — Publish to GitHub (GitHub Desktop)

1. Open **GitHub Desktop**.
2. Menu bar → **File → Add local repository…**
3. Click **Choose…** and pick `C:\Users\HP\Desktop\amazebase-landing`,
   then click **Add repository**.
   - It should open straight to the repo. If it warns the folder is not a
     repository, something went wrong — stop and tell me.
4. You should see **"No local changes"** and one commit in the History tab.
   That is correct — the commit is already made.
5. Click the blue **Publish repository** button at the top.
6. In the dialog:
   - **Name:** `amazebase-landing`
   - **Description:** optional
   - **Keep this code private** — your choice. Either works; Railway can read
     private repos once connected. Private is fine and is the safer default.
   - Click **Publish repository**.
7. Wait for the upload (~6 MB, should take under a minute).

Done. The code is on GitHub.

---

## Part 2 — Create the Railway service

1. Go to **https://railway.com/dashboard** and sign in.

2. **Create a NEW project** — do not add this to the project that runs your
   app. Click **New Project** (top right).

   > Why a new project: it keeps billing, variables and environments for the
   > marketing site completely separate from the product. If you'd rather keep
   > one project, you can instead open the existing project and click
   > **+ Create → GitHub Repo**; the rest of the steps are identical. A new
   > project is cleaner.

3. Choose **Deploy from GitHub repo**.

4. If this is the first time, Railway will ask to install its GitHub app.
   Click **Configure GitHub App**, and when GitHub asks which repositories to
   grant access to, **make sure `amazebase-landing` is selected**, then Save.
   - If you already granted "All repositories", it will just appear in the list.

5. Pick **`amazebase-landing`** from the list.

6. Railway starts building immediately. Watch the **Deploy Logs**.
   You are looking for it to detect a **static site** and build with **Caddy**.
   It should finish in roughly a minute.

   - You do **not** need to set a Root Directory. The repo root is the site.
   - You do **not** need to set a Start Command. Leave every build setting alone.

7. When the deploy goes green, open the service → **Settings → Networking →
   Public Networking** → click **Generate Domain**.
   - Leave the port field empty/default if it asks. Railway detects it.

8. Click the generated `*.up.railway.app` URL. The site should load with no
   login prompt.

---

## Part 3 — Check it (do this, it takes a minute)

- [ ] Page loads, no login screen, no password prompt
- [ ] Open it in a **private/incognito window** — proves it is genuinely public
- [ ] Hero section shows the dashboard screenshot with the glow curves behind it
- [ ] Scroll the whole page — feature icons and the partner logos all appear,
      no broken-image icons
- [ ] **No purple "⚙ Editor" button** in the bottom-left corner
- [ ] Your app at its own Railway URL still works exactly as before

If any image is missing, tell me which section and I will fix the path.

---

## Later: your own domain

Railway → service → **Settings → Networking → Custom Domain → + Add Domain**.
Railway shows you a CNAME record; you add it at whoever sells you the domain.
HTTPS is automatic. Say the word when you have a domain and I'll walk you
through it.

## Later: wiring up signup

When the signup button needs to talk to the app, the landing page will POST to
your app's domain. That needs a CORS allowance on the FastAPI side for the
landing page's origin. Separate job — ping me when you get there.

---

## Making changes from now on

Edit files in `C:\Users\HP\Desktop\amazebase-landing`, open GitHub Desktop,
write a summary, **Commit to main**, then **Push origin**. Railway redeploys by
itself within a minute or two. There is no build step to run.

> Note: the original working folder `amz_v2\Landing Page` still holds the dev
> tools and the 34 MB of source artwork. Keep using it for design work if you
> like — but the deployed site is `amazebase-landing`, and only changes made
> there go live.
