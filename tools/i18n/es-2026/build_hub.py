# -*- coding: utf-8 -*-
"""
/es/recursos.html — the Knowledge Hub in Spanish.

Built from resources.html by replacing the static chrome, so the layout, the
data hooks and the no-JS fallback structure stay identical. Two things need
care:

  * every path in resources.html is RELATIVE (css/base.css, articles/x.html),
    which would resolve under /es/ and 404. All of them are made root-absolute
    and the rewrite is asserted.
  * the page ships a static list of cards for crawlers and for no-JS, which
    hub.js replaces on load. The Spanish page needs its own, generated from the
    Spanish entries in resources.json. The English one is regenerated at the
    same time because it still lists 44 articles, not 51.
"""

import io, os, re, json, datetime

import chrome_common as C
from chrome_common import rep, lang_switch, hreflang_block, SITE

SRC = "/mnt/user-data/uploads/amazebase-landing"
OUT = "/home/claude/esout3"

EN_PATH = "/resources.html"
ES_PATH = "/es/recursos.html"

MES = ["ene", "feb", "mar", "abr", "may", "jun",
       "jul", "ago", "sep", "oct", "nov", "dic"]
MONTH = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]


def out_path(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    return p


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))


def fallback(resources, taxo, lang, root_absolute):
    """The static card list hub.js replaces on load."""
    fmt = {o["id"]: (o.get("label_" + lang) or o["label"]) for o in taxo["formats"]}
    # the pill label is plural ("Articles"); a single card wants the singular
    ONE = {"es": {"Artículos": "Artículo", "Podcasts": "Podcast", "Videos": "Video",
                  "Webinars": "Webinar", "Guías y ebooks": "Guía",
                  "Plantillas": "Plantilla", "Casos de estudio": "Caso de estudio"},
           "en": {"Articles": "Article", "Podcasts": "Podcast", "Videos": "Video",
                  "Webinars": "Webinar", "Guides & Ebooks": "Guide",
                  "Templates": "Template", "Case Studies": "Case Study"}}[lang]

    rows = [r for r in resources if r.get("language") == lang]
    rows.sort(key=lambda r: r.get("published", ""), reverse=True)

    out = ["<!-- SEO:HUB-FALLBACK:START -->"]
    for r in rows:
        d = r.get("published", "")
        try:
            y, m, dd = (int(x) for x in d.split("-"))
            human = ("%d de %s de %d" % (dd, MES[m - 1], y) if lang == "es"
                     else "%d %s %d" % (dd, MONTH[m - 1], y))
        except Exception:
            human = d
        href = ("/" if root_absolute else "") + r["url"]
        thumb = r.get("thumb")
        parts = ['  <a class="hub-row" href="%s">' % href]
        if thumb:
            parts.append('    <span class="hub-row-thumb"><img src="%s%s" alt="" '
                         'width="480" height="270" loading="lazy" decoding="async"></span>'
                         % ("/" if root_absolute else "", thumb))
        parts += [
            '    <div class="hub-row-body">',
            '      <h4 class="hub-row-h">%s</h4>' % esc(r["title"]),
            '      <p class="hub-row-p">%s</p>' % esc(r["summary"]),
            '      <div class="hub-row-meta"><span><time datetime="%s">%s</time></span>%s</div>'
            % (d, human, ("<span>%d min</span>" % r["minutes"]) if r.get("minutes") else ""),
            "    </div>",
            '    <span class="hub-row-tag">%s</span>'
            % esc(ONE.get(fmt.get(r.get("format"), ""), fmt.get(r.get("format"), ""))),
            "  </a>",
        ]
        out.append("\n".join(parts))
    out.append("<!-- SEO:HUB-FALLBACK:END -->")
    return "\n".join(out), len(rows)


# ------------------------------------------------------------- static chrome

MAIN_FIX = [
    ('<span class="eyebrow">Knowledge Hub</span>',
     '<span class="eyebrow">Centro de Conocimiento</span>'),
    ('<h1 class="hub-h1">Amazon Seller<br><span class="grad">Knowledge Hub</span></h1>',
     '<h1 class="hub-h1">Centro de Conocimiento<br><span class="grad">para vendedores de Amazon</span></h1>'),
    ('''    Actionable insights, proven strategies and expert guidance to help you
    grow a more profitable Amazon business.''',
     '''    Ideas accionables, estrategias probadas y criterio experto para que
    construyas un negocio m&aacute;s rentable en Amazon.'''),
    ('<label class="sr-only" for="hub-q">Search resources</label>',
     '<label class="sr-only" for="hub-q">Buscar recursos</label>'),
    ('placeholder="Search articles, guides, videos, podcasts&hellip;"',
     'placeholder="Busca art&iacute;culos, gu&iacute;as, videos, podcasts&hellip;"'),
    ('aria-label="Clear search"', 'aria-label="Borrar la b&uacute;squeda"'),
    ('<h2 class="hub-card-h">Browse by Format</h2>',
     '<h2 class="hub-card-h">Explorar por formato</h2>'),
    ('<h2 class="hub-card-h">Experience Level</h2>',
     '<h2 class="hub-card-h">Nivel de experiencia</h2>'),
    ('<h2 class="hub-card-h">Language</h2>',
     '<h2 class="hub-card-h">Idioma</h2>'),
    ('<h2 class="hub-card-h">Popular Topics</h2>',
     '<h2 class="hub-card-h">Temas populares</h2>'),
    ('<h2 class="hub-card-h">Can&rsquo;t find what you need?</h2>',
     '<h2 class="hub-card-h">&iquest;No encuentras lo que buscas?</h2>'),
    ('<p>Request a topic or ask our experts to create content on what matters to you.</p>',
     '<p>Pide un tema o cu&eacute;ntanos qu&eacute; te gustar&iacute;a que escribi&eacute;ramos.</p>'),
    ('        Request Content\n', '        Pedir contenido\n'),
    ('<h2 class="hub-sec-h">Featured</h2>', '<h2 class="hub-sec-h">Destacados</h2>'),
    ('<h2 class="hub-sec-h" data-hub-list-heading>Latest Resources</h2>',
     '<h2 class="hub-sec-h" data-hub-list-heading>Lo m&aacute;s reciente</h2>'),
    ('aria-selected="true">Latest</button>', 'aria-selected="true">Recientes</button>'),
    ('aria-selected="false">Quickest reads</button>',
     'aria-selected="false">Lecturas r&aacute;pidas</button>'),
    ('data-hub-clear hidden>Clear filters</button>',
     'data-hub-clear hidden>Limpiar filtros</button>'),
    ('<h2 class="hub-sec-h">From the Seller Community</h2>',
     '<h2 class="hub-sec-h">De la comunidad de vendedores</h2>'),
    ('<h2>Ready to put these insights into action?</h2>',
     '<h2>&iquest;Listo para poner esto en pr&aacute;ctica?</h2>'),
    ('<p>Join the wait list and be first in when we open your marketplace.</p>',
     '<p>&Uacute;nete a la lista de espera y entra de primero cuando abramos tu marketplace.</p>'),
    ('href="index.html#waitlist">Join the Wait List</a>',
     'href="/index.html#waitlist">&Uacute;nete a la lista de espera</a>'),
]

DIALOG_FIX = [
    ('aria-label="Close">', 'aria-label="Cerrar">'),
    ('<span class="eyebrow">Request content</span>',
     '<span class="eyebrow">Pedir contenido</span>'),
    ('<h2 class="wl-title" id="rq-title">What should we write about?</h2>',
     '<h2 class="wl-title" id="rq-title">&iquest;Sobre qu&eacute; deber&iacute;amos escribir?</h2>'),
    ('<p class="wl-sub">Tell us the problem you&rsquo;re trying to solve and we&rsquo;ll put it on the list.</p>',
     '<p class="wl-sub">Cu&eacute;ntanos el problema que est&aacute;s tratando de resolver y lo ponemos en la lista.</p>'),
    ('<label for="rq-topic">Topic or question</label>',
     '<label for="rq-topic">Tema o pregunta</label>'),
    ('placeholder="e.g. How do I work out true profit after FBA storage fees?"',
     'placeholder="p.&nbsp;ej. &iquest;C&oacute;mo calculo mi utilidad real despu&eacute;s de las tarifas de almacenamiento de FBA?"'),
    ('<label for="rq-email">Your email <span class="wl-opt">(optional &mdash; so we can tell you when it&rsquo;s up)</span></label>',
     '<label for="rq-email">Tu correo <span class="wl-opt">(opcional &mdash; para avisarte cuando est&eacute; publicado)</span></label>'),
    ('placeholder="jane@company.com"', 'placeholder="ana@empresa.com"'),
    ('<label for="rq-company-website">Company website</label>',
     '<label for="rq-company-website">Sitio web de la empresa</label>'),
    ('      Send request\n', '      Enviar solicitud\n'),
    ('''      If you give us your email we&rsquo;ll use it only to tell you when this
      content is published. See our <a href="privacy.html">Privacy Policy</a>.''',
     '''      Si nos dejas tu correo lo usamos solo para avisarte cuando publiquemos
      este contenido. Consulta nuestra <a href="/privacy.html">Pol&iacute;tica de
      Privacidad</a>.'''),
    ('<h2 class="wl-title">Request received.</h2>',
     '<h2 class="wl-title">Solicitud recibida.</h2>'),
    ('<p class="wl-sub">Thanks &mdash; that goes straight onto our list.</p>',
     '<p class="wl-sub">Gracias &mdash; va directo a nuestra lista.</p>'),
    ('type="button" data-request-close>Close</button>',
     'type="button" data-request-close>Cerrar</button>'),
]


def run():
    s = io.open(os.path.join(SRC, "resources.html"), encoding="utf-8").read()
    taxo = json.load(io.open(os.path.join(OUT, "data", "resources.json"), encoding="utf-8"))

    # ---------------------------------------------- the English page's fallback
    # The English hub already shipped with the language switcher (round one),
    # so build on that version, not on the pre-Spanish original.
    en = io.open("/home/claude/esout/resources.html", encoding="utf-8").read()
    blk, n_en = fallback(taxo["resources"], taxo, "en", root_absolute=False)
    a = en.index("<!-- SEO:HUB-FALLBACK:START -->")
    b = en.index("<!-- SEO:HUB-FALLBACK:END -->") + len("<!-- SEO:HUB-FALLBACK:END -->")
    old_n = en[a:b].count('<a class="hub-row"')
    en = en[:a] + blk + en[b:]
    # the English hub's language button now has a real Spanish hub to point at
    en = rep(en, 'href="/resources.html?lang=es" hreflang="es" lang="es"',
                 'href="%s" hreflang="es" lang="es"' % ES_PATH, label="en switch")
    en = rep(en, '<link rel="canonical" href="%s%s">' % (SITE, EN_PATH),
                 '<link rel="canonical" href="%s%s">\n%s' % (SITE, EN_PATH, hreflang_block(EN_PATH, ES_PATH)),
             label="en canonical")
    io.open(out_path("/resources.html"), "w", encoding="utf-8", newline="\n").write(en)
    print("resources.html  fallback %d -> %d rows, hreflang added" % (old_n, n_en))

    # ---------------------------------------------------------- the Spanish page
    s = rep(s, '<html lang="en">', '<html lang="es">', label="html lang")
    s = re.sub(r"<title>.*?</title>", lambda m:
               "<title>Centro de Conocimiento para vendedores de Amazon &mdash; AmazeBase</title>",
               s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', lambda m:
               '<meta name="description" content="Art&iacute;culos, gu&iacute;as y podcasts '
               'para vendedores de Amazon: inventario, publicidad, utilidad, flujo de caja e '
               'investigaci&oacute;n de productos. 51 recursos en espa&ntilde;ol.">',
               s, count=1)

    s = rep(s, '<link rel="canonical" href="%s%s">' % (SITE, EN_PATH),
               '<link rel="canonical" href="%s%s">\n%s' % (SITE, ES_PATH, hreflang_block(EN_PATH, ES_PATH)),
            label="es canonical")
    s = rep(s, '<meta property="og:locale" content="en_US">',
               '<meta property="og:locale" content="es_LA">\n'
               '<meta property="og:locale:alternate" content="en_US">', label="og:locale")
    s = rep(s, '<meta property="og:url" content="%s%s">' % (SITE, EN_PATH),
               '<meta property="og:url" content="%s%s">' % (SITE, ES_PATH), label="og:url")
    for pat, val in [
        (r'<meta property="og:title" content="[^"]*">',
         '<meta property="og:title" content="Centro de Conocimiento para vendedores de Amazon">'),
        (r'<meta property="og:description" content="[^"]*">',
         '<meta property="og:description" content="51 art&iacute;culos, gu&iacute;as y podcasts en espa&ntilde;ol sobre inventario, publicidad, utilidad y flujo de caja en Amazon.">'),
        (r'<meta name="twitter:title" content="[^"]*">',
         '<meta name="twitter:title" content="Centro de Conocimiento para vendedores de Amazon">'),
        (r'<meta name="twitter:description" content="[^"]*">',
         '<meta name="twitter:description" content="51 art&iacute;culos, gu&iacute;as y podcasts en espa&ntilde;ol sobre inventario, publicidad, utilidad y flujo de caja en Amazon.">'),
        (r'<meta property="og:image:alt" content="[^"]*">',
         '<meta property="og:image:alt" content="Un dial de control oscuro en el centro de una mesa dividida: datos de publicidad de un lado, &oacute;rdenes de compra, flete, inventario y efectivo del otro.">'),
        (r'<meta name="twitter:image:alt" content="[^"]*">',
         '<meta name="twitter:image:alt" content="Un dial de control oscuro en el centro de una mesa dividida: datos de publicidad de un lado, &oacute;rdenes de compra, flete, inventario y efectivo del otro.">'),
    ]:
        s = re.sub(pat, lambda m, v=val: v, s, count=1)

    s = rep(s, '"name": "Home"', '"name": "Inicio"', n=s.count('"name": "Home"'), label="crumb home")
    s = rep(s, '"name": "Knowledge Hub"', '"name": "Centro de Conocimiento"',
            n=s.count('"name": "Knowledge Hub"'), label="crumb hub")
    # resources.html is the one page with no skip link. Not adding one here:
    # that is an accessibility gap on the English page too, and fixing it in
    # Spanish only would make the pair inconsistent.
    if ">Skip to content</a>" in s:
        s = rep(s, ">Skip to content</a>", ">Saltar al contenido</a>", label="skip")

    # header + footer
    a, b = s.index('<header class="site-header">'), None
    b = s.index("</header>", a) + len("</header>")
    nav = (C.NAV_ES
           .replace("__LANGSWITCH__", "\n".join("    " + ln for ln in
                    lang_switch(EN_PATH, ES_PATH, "es").split("\n")))
           .replace("__WAITLIST__", "/index.html#waitlist")
           .replace('href="/resources.html?lang=es"', 'href="%s"' % ES_PATH))
    s = s[:a] + nav + s[b:]

    a = s.index('<footer class="footer">')
    b = s.index("</footer>", a) + len("</footer>")
    s = s[:a] + C.FOOTER_ES.replace('href="/resources.html?lang=es"', 'href="%s"' % ES_PATH) + s[b:]

    for old, new in MAIN_FIX + DIALOG_FIX:
        s = rep(s, old, new, label=old[:44])

    # Spanish fallback rows, root-absolute
    blk, n_es = fallback(taxo["resources"], taxo, "es", root_absolute=True)
    a = s.index("<!-- SEO:HUB-FALLBACK:START -->")
    b = s.index("<!-- SEO:HUB-FALLBACK:END -->") + len("<!-- SEO:HUB-FALLBACK:END -->")
    s = s[:a] + blk + s[b:]

    s, n = C.rootify(s, ES_PATH)

    # ---- postflight
    body = s[s.index("</head>"):]
    for bad in ("Knowledge Hub", "Join the Wait List", ">Log in<", "Skip to content",
                "Browse by Format", "Clear filters", "Request Content", "Featured<",
                "Latest Resources", "Quickest reads", "All rights reserved"):
        assert bad not in body, "untranslated %r" % bad
    assert '<html lang="es">' in s
    assert s.count('hreflang="es"') >= 2
    assert n_es == 51, n_es
    io.open(out_path(ES_PATH), "w", encoding="utf-8", newline="\n").write(s)
    print("es/recursos.html  %d relative refs made root-absolute, %d fallback rows"
          % (n, n_es))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run()
