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
serves the directory with Caddy — **no config file is needed**. That is why
there is no `railway.json`, `Procfile`, `package.json`, or `Caddyfile` here.
Adding one changes how it builds.

## Note for future edits

`css/dashboard.css` has `.dash{ display:none; }` near the top, marked TEMPORARY.
**Leave it.** The hero deliberately uses the screenshot `assets/img/dashboard.jpg`
instead of the older HTML dashboard; removing the rule makes both appear at once.

Full-resolution source artwork is kept outside this repo — only the files the
page actually loads are committed here.

---

Internal deployment and handover notes live in `_docs/`, which is deliberately
untracked so it is never published with the site.
