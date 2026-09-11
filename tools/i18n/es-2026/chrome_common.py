# -*- coding: utf-8 -*-
"""
Spanish mirrors of the four chrome pages: product, solutions, about, contact.

Unlike the article pages, these four reference their CSS, JS and each other
with RELATIVE paths (css/base.css, js/main.js, about.html). At /es/producto.html
those resolve to /es/css/base.css and 404, so every relative reference is
rewritten root-absolute. That rewrite is asserted, not assumed.

The header, footer and waitlist dialog are byte-identical across all four
English pages, so there is exactly one Spanish version of each.
"""

import io, os, re

SITE = "https://amazebase.pro"

# English path -> Spanish path, for both the nav and the href rewrite
PAGES = {
    "/product.html":    "/es/producto.html",
    "/solutions.html":  "/es/soluciones.html",
    "/about.html":      "/es/nosotros.html",
    "/contact.html":    "/es/contacto.html",
}


def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "expected %d of %r (%s), found %d" % (n, old[:70], label, c)
    return s.replace(old, new)


def cut(s, start, end):
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return s[:i], s[i:j], s[j:]


def lang_switch(en_url, es_url, current):
    def a(code, label, href):
        cur = ' aria-current="true"' if code == current else ""
        return ('    <a href="%s" hreflang="%s" lang="%s"%s>'
                '<span class="lc">%s</span>%s</a>'
                % (href, code, code, cur, code.upper(), label))
    return (
'<div class="nav-item lang-switch">\n'
'  <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Idioma / Language">\n'
'    %s <svg class="chev" aria-hidden="true"><use href="#i-chevron"/></svg>\n'
'  </button>\n'
'  <div class="nav-drop lang-drop">\n%s\n%s\n  </div>\n'
'</div>' % (current.upper(), a("en", "English", en_url), a("es", "Español", es_url)))


def hreflang_block(en_path, es_path):
    return ('<link rel="alternate" hreflang="en" href="%s%s">\n'
            '<link rel="alternate" hreflang="es" href="%s%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s%s">'
            % (SITE, en_path, SITE, es_path, SITE, en_path))


# ------------------------------------------------------------------ root-abs

REL_OK = re.compile(r"^(https?:|//|#|/|mailto:|tel:|data:)")


def rootify(s, label=""):
    """Rewrite every relative href/src to root-absolute. Returns (s, n)."""
    n = [0]

    def sub(m):
        attr, url = m.group(1), m.group(2)
        if REL_OK.match(url):
            return m.group(0)
        n[0] += 1
        return '%s="/%s"' % (attr, url)

    s = re.sub(r'\b(href|src|poster)="([^"]+)"', sub, s)

    # srcset is a comma-separated list and contains "src" without 'src="', so
    # the pattern above never saw it. A <picture> commits to the first <source>
    # whose type matches and does NOT fall back to the <img> when that 404s, so
    # one missed srcset breaks the image completely.
    def sub_set(m):
        parts = []
        for cand in m.group(2).split(","):
            cand = cand.strip()
            if not cand:
                continue
            bits = cand.split()
            if not REL_OK.match(bits[0]):
                bits[0] = "/" + bits[0]
                n[0] += 1
            parts.append(" ".join(bits))
        return '%s="%s"' % (m.group(1), ", ".join(parts))

    s = re.sub(r'\b(srcset|imagesrcset)="([^"]+)"', sub_set, s)

    left = [u for u in re.findall(r'\b(?:href|src|poster)="([^"]+)"', s)
            if not REL_OK.match(u)]
    for setattr_ in re.findall(r'\b(?:srcset|imagesrcset)="([^"]+)"', s):
        for cand in setattr_.split(","):
            cand = cand.strip()
            if cand and not REL_OK.match(cand.split()[0]):
                left.append(cand)
    assert not left, "%s: relative refs survived: %s" % (label, left[:5])
    return s, n[0]


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
      <a class="nav-link" href="/es/producto.html#modules">Producto <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop nav-drop--wide">
        <a href="/es/producto.html#advertising"><svg class="icon-sm"><use href="#i-mega"/></svg>Publicidad y PPC</a>
        <a href="/es/producto.html#financials"><svg class="icon-sm"><use href="#i-dollar"/></svg>Finanzas</a>
        <a href="/es/producto.html#ledger"><svg class="icon-sm"><use href="#i-stack"/></svg>Ledger</a>
        <a href="/es/producto.html#inventory"><svg class="icon-sm"><use href="#i-box"/></svg>Inventario</a>
        <a href="/es/producto.html#research"><svg class="icon-sm"><use href="#i-search"/></svg>Investigaci&oacute;n de productos</a>
        <a href="/es/producto.html#simulations"><svg class="icon-sm"><use href="#i-chart"/></svg>Simulaciones</a>
        <a href="/es/producto.html#sales"><svg class="icon-sm"><use href="#i-trend"/></svg>Ventas</a>
        <a href="/es/producto.html#data"><svg class="icon-sm"><use href="#i-db"/></svg>Datos y sincronizaci&oacute;n</a>
        <a href="/es/producto.html#security"><svg class="icon-sm"><use href="#i-shield"/></svg>Seguridad</a>
        <a href="/es/producto.html#assistant"><svg class="icon-sm"><use href="#i-spark"/></svg>Asistente de IA &mdash; pronto</a>
      </div>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="/es/soluciones.html">Soluciones <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop">
        <a href="/es/soluciones.html#beginners"><svg class="icon-sm"><use href="#i-rocket"/></svg>Principiantes</a>
        <a href="/es/soluciones.html#experts"><svg class="icon-sm"><use href="#i-dollar"/></svg>Vendedores con experiencia</a>
        <a href="/es/soluciones.html#agencies"><svg class="icon-sm"><use href="#i-case"/></svg>Agencias</a>
      </div>
    </li>
    <li class="nav-item"><a class="nav-link" href="/index.html#pricing">Precios</a></li>
    <li class="nav-item"><a class="nav-link" href="/resources.html?lang=es">Recursos</a></li>
    <li class="nav-item">
      <a class="nav-link" href="/es/nosotros.html">Empresa <svg class="chev"><use href="#i-chevron"/></svg></a>
      <div class="nav-drop">
        <a href="/es/nosotros.html"><svg class="icon-sm"><use href="#i-info"/></svg>Nosotros</a>
        <a href="/es/contacto.html"><svg class="icon-sm"><use href="#i-msg"/></svg>Contacto</a>
      </div>
    </li>
  </ul>

  <div class="nav-actions">
__LANGSWITCH__
    <a class="btn btn--quiet" href="https://analytics.amazebase.pro/login">Iniciar sesi&oacute;n</a>
    <a class="btn btn--primary" href="__WAITLIST__" data-magnetic>&Uacute;nete a la lista de espera</a>
    <button class="nav-toggle" aria-label="Abrir men&uacute;" aria-expanded="false" aria-controls="navMobile">
      <svg class="icon"><use href="#i-menu"/></svg>
    </button>
  </div>

</nav>
</div>

<div class="nav-mobile" id="navMobile">
  <a href="/es/producto.html#modules">Producto</a>
  <a href="/es/soluciones.html">Soluciones</a>
  <a href="/index.html#pricing">Precios</a>
  <a href="/resources.html?lang=es">Recursos</a>
  <a href="/es/nosotros.html">Nosotros</a>
  <a href="/es/contacto.html">Contacto</a>
  <a class="btn btn--quiet btn--block" href="https://analytics.amazebase.pro/login">Iniciar sesi&oacute;n</a>
  <a class="btn btn--primary btn--block" href="__WAITLIST__">&Uacute;nete a la lista de espera</a>
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
      <a href="/es/producto.html#modules">Producto</a>
      <a href="/index.html#pricing">Precios</a>
    </div>

    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="/resources.html?lang=es">Centro de Conocimiento</a>
    </div>

    <div class="footer-col">
      <h4>Empresa</h4>
      <a href="/es/nosotros.html">Nosotros</a>
      <a href="/es/contacto.html">Contacto</a>
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


# The dialog carries its own copy AND its own error strings, as data-msg-*
# attributes read by js/waitlist.js. Field names, option values, the two
# honeypot names and every data-waitlist-* hook are untouched: the app keys
# off them and renaming company_website silently disables the bot trap.
DIALOG_ES = '''<dialog class="wl" id="waitlist" aria-labelledby="wl-title"
        data-msg-name="Dinos tu nombre, por favor."
        data-msg-email="Esa direcci&oacute;n de correo no parece v&aacute;lida."
        data-msg-market="Elige tu marketplace principal."
        data-msg-sending="Enviando&hellip;"
        data-msg-rate="Demasiados intentos por ahora. Vuelve a probar en un rato."
        data-msg-generic="Algo sali&oacute; mal."
        data-msg-network="No pudimos conectar con el servidor. Int&eacute;ntalo de nuevo.">
  <form class="wl-panel" method="dialog" novalidate>

    <button class="wl-x" type="button" data-waitlist-close aria-label="Cerrar">
      <svg class="icon-sm"><use href="#i-x"/></svg>
    </button>

    <span class="eyebrow">Acceso anticipado</span>
    <h2 class="wl-title" id="wl-title">&Uacute;nete a la lista de espera</h2>
    <p class="wl-sub">Te escribimos en cuanto abramos tu marketplace. Sin spam y sin datos de pago.</p>

    <div class="wl-field">
      <label for="wl-name">Nombre</label>
      <input id="wl-name" name="name" type="text" autocomplete="name"
             maxlength="120" required placeholder="Ana Garc&iacute;a">
    </div>

    <div class="wl-field">
      <label for="wl-email">Correo de trabajo</label>
      <input id="wl-email" name="email" type="email" autocomplete="email"
             maxlength="254" required placeholder="ana@empresa.com">
    </div>

    <div class="wl-field">
      <label for="wl-market">Marketplace principal</label>
      <select id="wl-market" name="marketplace" required>
        <option value="" selected disabled>&iquest;D&oacute;nde vendes m&aacute;s?</option>
        <optgroup label="Norteam&eacute;rica">
          <option value="US">Amazon.com &mdash; Estados Unidos</option>
          <option value="CA">Amazon.ca &mdash; Canad&aacute;</option>
          <option value="MX">Amazon.com.mx &mdash; M&eacute;xico</option>
          <option value="BR">Amazon.com.br &mdash; Brasil</option>
        </optgroup>
        <optgroup label="Europa">
          <option value="UK">Amazon.co.uk &mdash; Reino Unido</option>
          <option value="DE">Amazon.de &mdash; Alemania</option>
          <option value="FR">Amazon.fr &mdash; Francia</option>
          <option value="IT">Amazon.it &mdash; Italia</option>
          <option value="ES">Amazon.es &mdash; Espa&ntilde;a</option>
          <option value="NL">Amazon.nl &mdash; Pa&iacute;ses Bajos</option>
          <option value="SE">Amazon.se &mdash; Suecia</option>
          <option value="PL">Amazon.pl &mdash; Polonia</option>
          <option value="BE">Amazon.com.be &mdash; B&eacute;lgica</option>
          <option value="IE">Amazon.ie &mdash; Irlanda</option>
          <option value="TR">Amazon.com.tr &mdash; Turqu&iacute;a</option>
        </optgroup>
        <optgroup label="Medio Oriente e India">
          <option value="AE">Amazon.ae &mdash; Emiratos &Aacute;rabes Unidos</option>
          <option value="SA">Amazon.sa &mdash; Arabia Saudita</option>
          <option value="EG">Amazon.eg &mdash; Egipto</option>
          <option value="IN">Amazon.in &mdash; India</option>
        </optgroup>
        <optgroup label="Asia-Pac&iacute;fico">
          <option value="JP">Amazon.co.jp &mdash; Jap&oacute;n</option>
          <option value="AU">Amazon.com.au &mdash; Australia</option>
          <option value="SG">Amazon.sg &mdash; Singapur</option>
        </optgroup>
        <option value="OTHER">En otro lugar</option>
      </select>
    </div>

    <!-- Honeypots. Nunca renombrar company_website ni referral_code sin cambiar
         primero la app: la trampa dejar&iacute;a de funcionar en silencio. -->
    <div class="wl-hp" aria-hidden="true">
      <label for="wl-company-website">Sitio web de la empresa</label>
      <input id="wl-company-website" name="company_website" type="text"
             tabindex="-1" autocomplete="off">
      <label for="wl-referral-code">C&oacute;digo de referido</label>
      <input id="wl-referral-code" name="referral_code" type="text"
             tabindex="-1" autocomplete="off">
    </div>

    <p class="wl-error" data-waitlist-error hidden></p>

    <button class="btn btn--primary btn--lg btn--block wl-submit" type="submit"
            data-waitlist-submit>&Uacute;nete a la lista de espera</button>

    <p class="wl-legal">
      Al unirte aceptas que te escribamos sobre AmazeBase. Guardamos tu nombre,
      correo y marketplace solo con ese fin, y puedes pedirnos que los borremos
      cuando quieras. Consulta nuestra <a href="/privacy.html">Pol&iacute;tica de
      Privacidad</a>.
    </p>

  </form>

  <div class="wl-panel wl-done" data-waitlist-done hidden>
    <div class="wl-tick"><svg class="icon-sm"><use href="#i-checkc"/></svg></div>
    <h2 class="wl-title">Ya est&aacute;s en la lista.</h2>
    <p class="wl-sub">Gracias &mdash; te escribimos en cuanto abramos tu marketplace.</p>
    <button class="btn btn--ghost btn--lg btn--block" type="button" data-waitlist-close>Cerrar</button>
  </div>
</dialog>'''


# --------------------------------------------------------------------- build

def build(src_path, out_path, en_path, es_path, meta, main_es):
    s = io.open(src_path, encoding="utf-8").read()

    s = rep(s, '<html lang="en">', '<html lang="es">', label="html lang")

    s = re.sub(r"<title>.*?</title>",
               lambda m: "<title>%s &mdash; AmazeBase</title>" % meta["title"],
               s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               lambda m: '<meta name="description" content="%s">' % meta["desc"],
               s, count=1)

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
    for pat, val in [(r'<meta property="og:title" content="[^"]*">',
                      '<meta property="og:title" content="%s">' % meta["og_title"]),
                     (r'<meta property="og:description" content="[^"]*">',
                      '<meta property="og:description" content="%s">' % meta["og_desc"]),
                     (r'<meta name="twitter:title" content="[^"]*">',
                      '<meta name="twitter:title" content="%s">' % meta["og_title"]),
                     (r'<meta name="twitter:description" content="[^"]*">',
                      '<meta name="twitter:description" content="%s">' % meta["og_desc"])]:
        s = re.sub(pat, lambda m, v=val: v, s, count=1)

    # JSON-LD breadcrumbs
    s = rep(s, '"name": "Home"', '"name": "Inicio"', label="crumb home")
    s = rep(s, '"name": "%s"\n' % meta["crumb_en"],
               '"name": "%s"\n' % meta["crumb_es"], label="crumb page")

    s = rep(s, '>Skip to content</a>', '>Saltar al contenido</a>', label="skip link")
    s = rep(s, 'aria-label="Back to top"', 'aria-label="Volver arriba"', label="to-top")

    # header
    before, _, after = cut(s, '<header class="site-header">', '</header>')
    nav = (NAV_ES
           .replace("__LANGSWITCH__",
                    "\n".join("    " + ln for ln in
                              lang_switch(en_path, es_path, "es").split("\n")))
           .replace("__WAITLIST__", meta["waitlist_href"]))
    s = before + nav + after

    # main
    before, _, after = cut(s, '<main id="main">', '</main>')
    s = before + main_es + after

    # footer
    before, _, after = cut(s, '<footer class="footer">', '</footer>')
    s = before + FOOTER_ES + after

    # waitlist dialog
    before, _, after = cut(s, '<dialog class="wl"', '</dialog>')
    s = before + DIALOG_ES + after

    # every relative path becomes root-absolute
    s, n = rootify(s, es_path)
    assert n >= 10, "%s: only %d relative refs rewritten" % (es_path, n)

    # ---- postflight
    body = s[s.index("</head>"):]
    for bad in ("Skip to content", "Join the Wait List", "Join the wait list",
                ">Log in<", "Knowledge Hub", "All rights reserved"):
        assert bad not in body, "%s: untranslated %r left" % (es_path, bad)
    for keep in ('name="company_website"', 'name="referral_code"',
                 'name="marketplace"', 'data-waitlist-submit', 'data-waitlist-done'):
        assert keep in s, "%s: lost %s" % (es_path, keep)
    assert s.count('hreflang="es"') >= 2
    assert '<html lang="es">' in s

    d = os.path.dirname(out_path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(s)
    return s, n
