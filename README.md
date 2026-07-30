# AmazeBase — landing page

The public marketing site. Static HTML/CSS/JS, no build step, no backend.

## What's here

```
index.html        the whole page
css/              base, variables, navigation, hero, sections, responsive, dashboard
js/main.js        scroll reveal + small UI behaviour
assets/img/       optimised images used by the page
Images/           the four hero curve PNGs
```

Only external dependency: Google Fonts (Inter), loaded via `<link>` in `index.html`.

## Editing locally

Open `index.html` in a browser. That's it — there is nothing to build or install.

## Deployment

Deployed on Railway as its own service, separate from the app.

Railway's builder (Railpack) sees `index.html` in the repo root, recognises this
as a static site, and serves it with Caddy. **No config file is needed** — that
is why there is no `railway.json`, `Procfile`, or `package.json` here. Adding one
would change how it builds.

Push to `main` → Railway rebuilds and redeploys automatically.

## Notes for future edits

- `css/dashboard.css` has `.dash{ display:none; }` near the top, marked
  TEMPORARY. **Leave it.** The hero deliberately uses the screenshot
  `assets/img/dashboard.jpg` instead of the old HTML dashboard. Removing the
  rule makes both appear at once.
- The full-resolution source artwork (~34 MB) lives in the main `amz_v2` repo
  under `Landing Page/Images/` and is deliberately not committed here — only the
  files the page actually loads ship to production.
- This repo is intentionally standalone. When the signup flow is wired up it
  will call the app over the network; it does not need to share a repo with it.
