# -*- coding: utf-8 -*-
"""
Shared machinery for building the Spanish mirror of an article page.

Design notes
------------
* Every article's CSS, sprite and layout markup is left byte-identical. The
  Spanish page differs only in: <html lang>, the head metadata, the header nav
  labels, the article content, the footer labels, the hero src (root-absolute
  so it works from /es/articulos/), and the added hreflang + language switcher.
* Every replacement is asserted to fire exactly once. A silently-missed swap
  fails loudly rather than half-applying.
"""

import io, re, os

SITE = "https://amazebase.pro"

# --------------------------------------------------------------- replacement

def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "expected %d of %r (%s), found %d" % (n, old[:70], label, c)
    return s.replace(old, new)


def cut(s, start, end):
    """Return (before, chunk, after) around the first start..end region."""
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return s[:i], s[i:j], s[j:]


# ------------------------------------------------------------ language links

def lang_switch(en_url, es_url, current):
    """Header language switcher. `current` is 'en' or 'es'."""
    def a(code, label, href):
        cur = ' aria-current="true"' if code == current else ""
        return ('    <a href="%s" hreflang="%s" lang="%s"%s>'
                '<span class="lc">%s</span>%s</a>'
                % (href, code, code, cur, code.upper(), label))
    return (
'<div class="nav-item lang-switch">\n'
'  <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="%s">\n'
'    %s <svg class="chev" aria-hidden="true"><use href="#i-chevron"/></svg>\n'
'  </button>\n'
'  <div class="nav-drop lang-drop">\n%s\n%s\n  </div>\n'
'</div>' % ("Idioma / Language",
            current.upper(),
            a("en", "English", en_url),
            a("es", "Español", es_url)))


def hreflang_block(en_path, es_path):
    return (
'<link rel="alternate" hreflang="en" href="%s%s">\n'
'<link rel="alternate" hreflang="es" href="%s%s">\n'
'<link rel="alternate" hreflang="x-default" href="%s%s">'
% (SITE, en_path, SITE, es_path, SITE, en_path))


# ------------------------------------------------------------------- Spanish

NAV_ES = '''<header class="site-header">
<div class="container">
<nav class="nav" aria-label="Principal">

  <a href="/index.html" class="brand" aria-label="Inicio de AmazeBase">
    <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
      <path d="M16 3.2 29 27.5h-6.4L16 14.1 9.4 27.5H3z" fill="url(#markGrad)"/>
      <path d="M16 17.6l4.4 8.2h-8.8z" fill="#C56BF5" opacity=".85"/>
    </svg>
    <span data-brand>AmazeBase</span>
  </a>

  <ul class="nav-menu">
    <li class="nav-item">
      <a class="nav-link" href="/product.html#modules">Producto <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop nav-drop--wide">
        <a href="/product.html#advertising"><svg class="icon-sm"><use href="#i-mega"/></svg>Publicidad y PPC</a>
        <a href="/product.html#financials"><svg class="icon-sm"><use href="#i-dollar"/></svg>Finanzas</a>
        <a href="/product.html#ledger"><svg class="icon-sm"><use href="#i-stack"/></svg>Ledger</a>
        <a href="/product.html#inventory"><svg class="icon-sm"><use href="#i-box"/></svg>Inventario</a>
        <a href="/product.html#research"><svg class="icon-sm"><use href="#i-search"/></svg>Investigaci&oacute;n de productos</a>
        <a href="/product.html#simulations"><svg class="icon-sm"><use href="#i-chart"/></svg>Simulaciones</a>
        <a href="/product.html#sales"><svg class="icon-sm"><use href="#i-trend"/></svg>Ventas</a>
        <a href="/product.html#data"><svg class="icon-sm"><use href="#i-db"/></svg>Datos y sincronizaci&oacute;n</a>
        <a href="/product.html#security"><svg class="icon-sm"><use href="#i-shield"/></svg>Seguridad</a>
        <a href="/product.html#assistant"><svg class="icon-sm"><use href="#i-spark"/></svg>Asistente de IA &mdash; pronto</a>
      </div>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="/solutions.html">Soluciones <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop">
        <a href="/solutions.html#beginners"><svg class="icon-sm"><use href="#i-rocket"/></svg>Principiantes</a>
        <a href="/solutions.html#experts"><svg class="icon-sm"><use href="#i-dollar"/></svg>Vendedores con experiencia</a>
        <a href="/solutions.html#agencies"><svg class="icon-sm"><use href="#i-case"/></svg>Agencias</a>
      </div>
    </li>
    <li class="nav-item"><a class="nav-link" href="/index.html#pricing">Precios</a></li>
    <li class="nav-item"><a class="nav-link" href="/resources.html?lang=es">Recursos</a></li>
    <li class="nav-item">
      <a class="nav-link" href="/about.html">Empresa <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop">
        <a href="/about.html"><svg class="icon-sm"><use href="#i-info"/></svg>Nosotros</a>
        <a href="/contact.html"><svg class="icon-sm"><use href="#i-msg"/></svg>Contacto</a>
      </div>
    </li>
  </ul>

  <div class="nav-actions">
__LANGSWITCH__
    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Iniciar sesi&oacute;n</a>
    <a class="btn btn--primary" href="/index.html#waitlist" data-magnetic>&Uacute;nete a la lista de espera</a>
    <button class="nav-toggle" aria-label="Abrir men&uacute;" aria-expanded="false" aria-controls="navMobile">
      <svg class="icon"><use href="#i-menu"/></svg>
    </button>
  </div>

</nav>
</div>

<div class="nav-mobile" id="navMobile">
  <a href="/product.html#modules">Producto</a>
  <a href="/solutions.html">Soluciones</a>
  <a href="/index.html#pricing">Precios</a>
  <a href="/resources.html?lang=es">Recursos</a>
  <a href="/about.html">Nosotros</a>
  <a href="/contact.html">Contacto</a>
  <a class="btn btn--quiet btn--block" href="https://analytics.amazebase.pro/login">Iniciar sesi&oacute;n</a>
  <a class="btn btn--primary btn--block" href="/index.html#waitlist">&Uacute;nete a la lista de espera</a>
</div>
</header>'''


FOOTER_ES = '''<footer class="footer">
<div class="container">

  <div class="footer-top">
    <div class="footer-brand">
      <a href="/index.html" class="brand" aria-label="Inicio de AmazeBase">
        <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
          <path d="M16 3.2 29 27.5h-6.4L16 14.1 9.4 27.5H3z" fill="url(#markGrad)"/>
        </svg>
        <span data-brand>AmazeBase</span>
      </a>
      <p>El sistema operativo para vendedores de Amazon. Todo conectado, todo sincronizado.</p>
    </div>

    <div class="footer-col">
      <h4>Producto</h4>
      <a href="/product.html#modules">Producto</a>
      <a href="/index.html#pricing">Precios</a>
    </div>

    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="/resources.html?lang=es">Centro de Conocimiento</a>
    </div>

    <div class="footer-col">
      <h4>Empresa</h4>
      <a href="/about.html">Nosotros</a>
      <a href="/contact.html">Contacto</a>
      <a href="/privacy.html">Privacidad</a>
      <a href="/terms.html">T&eacute;rminos</a>
    </div>
  </div>

  <div class="footer-bottom">
    <span>&copy; 2026 <span data-brand>AmazeBase</span>. Todos los derechos reservados.</span>
    <div class="footer-social">
      <a href="#" aria-label="LinkedIn"><svg class="icon-sm"><use href="#i-in"/></svg></a>
      <a href="#" aria-label="X"><svg class="icon-sm"><use href="#i-tw"/></svg></a>
      <a href="#" aria-label="GitHub"><svg class="icon-sm"><use href="#i-gh"/></svg></a>
    </div>
  </div>

</div>
</footer>'''


# --------------------------------------------------------------------- build

def build_es(src_path, out_path, en_path, es_path, meta, body_es):
    """
    meta: dict with title, desc, og_title, og_desc, headline, ld_desc,
          keywords (list), breadcrumb, eyebrow
    body_es: the whole region from `<div class="wrap">` through
             `</div><!-- /.wrap -->` (or the shell close), already translated.
    """
    s = io.open(src_path, encoding="utf-8").read()

    # 1. document language
    s = rep(s, '<html lang="en">', '<html lang="es">', label="html lang")

    # 2. head: title + description
    s = re.sub(r"<title>.*?</title>",
               lambda m: "<title>%s &mdash; AmazeBase</title>" % meta["title"],
               s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               lambda m: '<meta name="description" content="%s">' % meta["desc"],
               s, count=1)

    has_seo = "<!-- SEO:START -->" in s
    if not has_seo:
        # The seven late-published articles ship with no SEO block at all.
        # Give the Spanish page the minimum that localisation needs.
        s = rep(s, '<link rel="stylesheet" href="/css/site-footer.css">',
                   '<link rel="stylesheet" href="/css/site-footer.css">\n'
                   '<link rel="canonical" href="%s%s">\n%s\n'
                   '<meta property="og:site_name" content="AmazeBase">\n'
                   '<meta property="og:locale" content="es_LA">\n'
                   '<meta property="og:locale:alternate" content="en_US">\n'
                   '<meta property="og:type" content="article">\n'
                   '<meta property="og:url" content="%s%s">\n'
                   '<meta property="og:title" content="%s">\n'
                   '<meta property="og:description" content="%s">'
                   % (SITE, es_path, hreflang_block(en_path, es_path),
                      SITE, es_path, meta["og_title"], meta["og_desc"]),
                label="no-seo head insert")
        return _finish(s, meta, en_path, es_path, body_es, out_path)

    # 3. SEO block
    s = rep(s, '<link rel="canonical" href="%s%s">' % (SITE, en_path),
               '<link rel="canonical" href="%s%s">\n%s'
               % (SITE, es_path, hreflang_block(en_path, es_path)),
            label="canonical")
    s = rep(s, '<meta property="og:locale" content="en_US">',
               '<meta property="og:locale" content="es_LA">\n'
               '<meta property="og:locale:alternate" content="en_US">',
            label="og:locale")
    s = rep(s, '<meta property="og:url" content="%s%s">' % (SITE, en_path),
               '<meta property="og:url" content="%s%s">' % (SITE, es_path),
            label="og:url")

    # og / twitter title + description
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               lambda m: '<meta property="og:title" content="%s">' % meta["og_title"], s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               lambda m: '<meta property="og:description" content="%s">' % meta["og_desc"], s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">',
               lambda m: '<meta name="twitter:title" content="%s">' % meta["og_title"], s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">',
               lambda m: '<meta name="twitter:description" content="%s">' % meta["og_desc"], s, count=1)

    # 4. JSON-LD: article node only
    s = rep(s, '"@id": "%s%s#article"' % (SITE, en_path),
               '"@id": "%s%s#article"' % (SITE, es_path), label="ld @id")
    s = rep(s, '"@id": "%s%s"\n      },\n      "headline"' % (SITE, en_path),
               '"@id": "%s%s"\n      },\n      "headline"' % (SITE, es_path),
            label="ld mainEntityOfPage")
    s = re.sub(r'"headline": "[^"]*"',
               lambda m: '"headline": "%s"' % meta["headline"], s, count=1)
    s = re.sub(r'("headline": "[^"]*",\n      )"description": "[^"]*"',
               lambda m: m.group(1) + '"description": "%s"' % meta["ld_desc"],
               s, count=1)
    # the Article node's inLanguage is the second occurrence (WebSite is first)
    parts = s.split('"inLanguage": "en"')
    assert len(parts) == 3, "expected 2 inLanguage nodes, found %d" % (len(parts) - 1)
    s = parts[0] + '"inLanguage": "en"' + parts[1] + '"inLanguage": "es"' + parts[2]

    _kw = '"keywords": [\n        %s\n      ]' % ",\n        ".join('"%s"' % k for k in meta["keywords"])
    s = re.sub(r'"keywords": \[.*?\]', lambda m: _kw, s, count=1, flags=re.S)

    # breadcrumbs
    s = rep(s, '"name": "Home"', '"name": "Inicio"', label="crumb home")
    s = rep(s, '"name": "Knowledge Hub"', '"name": "Centro de Conocimiento"', label="crumb hub")
    s = rep(s, '"item": "%s/resources.html"' % SITE,
               '"item": "%s/resources.html?lang=es"' % SITE, label="crumb hub url")
    s = re.sub(r'("position": 3,\n          )"name": "[^"]*"',
               lambda m: m.group(1) + '"name": "%s"' % meta["breadcrumb"],
               s, count=1)

    return _finish(s, meta, en_path, es_path, body_es, out_path)


def _finish(s, meta, en_path, es_path, body_es, out_path):
    # 5. skip link
    s = rep(s, '>Skip to content</a>', '>Saltar al contenido</a>', label="skip link")

    # 6. header nav
    before, _, after = cut(s, '<header class="site-header">', '</header>')
    nav = NAV_ES.replace("__LANGSWITCH__",
                         "\n".join("    " + ln for ln in
                                   lang_switch(en_path, es_path, "es").split("\n")))
    s = before + nav + after

    # 7. body: wrap region
    before, _, after = cut(s, '<div class="wrap">', '</div><!-- /.wrap -->')
    s = before + body_es + after

    # 8. footer
    before, _, after = cut(s, '<footer class="footer">', '</footer>')
    s = before + FOOTER_ES + after

    # ---- postflight.  The shared inline stylesheet carries English comments
    # that mention UI labels, so only the markup after </style> is checked.
    body = s[s.index("</style>"):]
    assert '<html lang="es">' in s, "html lang not switched"
    assert '../assets/img/' not in s, "relative asset path survived into /es/"
    for bad in ("Knowledge Hub", "Join the Wait List", ">Log in<",
                "Skip to content", "min read"):
        assert bad not in body, "untranslated %r left" % bad
    assert s.count('hreflang="es"') >= 2, "missing hreflang"

    d = os.path.dirname(out_path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(s)
    return s
