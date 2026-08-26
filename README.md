# AmazeBase — landing page

The public marketing site. Static HTML/CSS/JS, no build step, no backend.

```
index.html        the whole page
css/              base, variables, navigation, hero, sections, responsive, dashboard
js/main.js        scroll reveal + small UI behaviour
assets/img/       optimised images used by the page
Images/           the four hero curve PNGs
```

Only external dependency: Google Fonts (Inter), loaded via `<link>` in `index.html`.

## Editing locally

Open `index.html` in a browser. Nothing to build or install.

## Deployment

Served as a static site. The builder detects `index.html` in the repo root and
serves the directory with Caddy. There is no `railway.json`, `Procfile` or
`package.json` — but there **is** a `Caddyfile`, which overrides the builder's
default config to send stricter security headers, including the site's CSP.
Delete it and the site still serves; it just loses the hardened headers.

## Note for future edits

`css/dashboard.css` has `.dash{ display:none; }` near the top, marked TEMPORARY.
**Leave it.** The hero deliberately uses the screenshot `assets/img/dashboard.jpg`
instead of the older HTML dashboard; removing the rule makes both appear at once.

Full-resolution source artwork is kept outside this repo — only the files the
page actually loads are committed here.

## Machine-readable signals

`robots.txt`, `sitemap.xml`, the `<!-- SEO:START -->` block in every page's
`<head>` (canonical, Open Graph, Twitter Card, JSON-LD) and the static article
list inside `resources.html` are all **generated**. Do not hand-edit them:

```
python3 tools/seo.py        # rebuilds all of the above from data/resources.json
python3 tools/build_og.py   # rebuilds assets/img/og/*.jpg share images
```

Both are idempotent — run them again after adding an article or changing a
page's `<title>` / `<meta name="description">`, and commit the result.

Two things worth knowing:

- The Knowledge Hub renders in JavaScript from `data/resources.json`. The
  static list `tools/seo.py` writes into `resources.html` is what a crawler
  that does not run JS actually sees; `js/hub.js` clears that container and
  rebuilds it, so a browser never shows both.
- `tools/` is hidden in the `Caddyfile` so the build scripts are not served.

---

Internal deployment and handover notes live in `_docs/`, which is deliberately
untracked so it is never published with the site.
