# -*- coding: utf-8 -*-
"""
Localise js/hub.js so one script serves both /resources.html and
/es/recursos.html.

Nothing is hard-coded to Spanish. The script reads <html lang>, looks the
string up in a table, and falls back to the English literal it had before, so
the English hub behaves byte-identically. Taxonomy labels come from
data/resources.json via a `label_es` field alongside the existing `label`.
"""

import io, os

SRC = "/mnt/user-data/uploads/amazebase-landing/js/hub.js"
OUT = "/home/claude/esout3/js/hub.js"


def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "expected %d of %r (%s), found %d" % (n, old[:60], label, c)
    return s.replace(old, new)


STRINGS = '''
  /* ------------------------------------------------------------- LANGUAGE */

  /* The hub exists at /resources.html and /es/recursos.html and is driven by
     one script and one data file. Every user-facing string goes through T(),
     which falls back to the English literal, so adding a language means adding
     a column here and a `label_xx` beside each `label` in resources.json. */
  var LANG = (document.documentElement.lang || "en").slice(0, 2).toLowerCase();

  var STR = {
    es: {
      "All Resources":        "Todos los recursos",
      "All":                  "Todas",
      "Results":              "Resultados",
      "Latest Resources":     "Lo m\\u00e1s reciente",
      "resource":             "recurso",
      "resources":            "recursos",
      " match":               " coinciden",
      "Nothing featured yet": "Todav\\u00eda no hay destacados",
      "Mark a resource with \\u201cfeatured\\u201d in data/resources.json and it will appear here.":
        "Marca un recurso como \\u00abfeatured\\u00bb en data/resources.json y aparecer\\u00e1 aqu\\u00ed.",
      "No resources published yet": "Todav\\u00eda no hay recursos publicados",
      "This hub is built and ready. Add entries to data/resources.json and they appear here \\u2014 counts, filters and search all follow automatically.":
        "El centro est\\u00e1 listo. Agrega entradas en data/resources.json y aparecer\\u00e1n aqu\\u00ed: los conteos, los filtros y la b\\u00fasqueda se actualizan solos.",
      "Nothing matches those filters": "Nada coincide con esos filtros",
      "Try a different category, format or search term.":
        "Prueba con otra categor\\u00eda, otro formato u otro t\\u00e9rmino de b\\u00fasqueda.",
      "Couldn't load the resource list": "No pudimos cargar la lista de recursos",
      " min":                 " min",
      "Sending\\u2026":         "Enviando\\u2026",
      "Tell us a little more about what you'd like.":
        "Cu\\u00e9ntanos un poco m\\u00e1s sobre lo que te gustar\\u00eda.",
      "That email address doesn't look right.":
        "Esa direcci\\u00f3n de correo no parece v\\u00e1lida.",
      "Too many requests just now. Please try again later.":
        "Demasiadas solicitudes por ahora. Vuelve a intentarlo m\\u00e1s tarde.",
      "We couldn't send that. Please try again.":
        "No pudimos enviarlo. Int\\u00e9ntalo de nuevo.",
      "Something went wrong.": "Algo sali\\u00f3 mal."
    }
  };

  function T(s) {
    var t = STR[LANG];
    return (t && t[s]) || s;
  }

'''


def run():
    s = io.open(SRC, encoding="utf-8").read()
    assert "function T(" not in s, "hub.js already localised"

    # data lives at the root; /es/recursos.html must not ask for /es/data/...
    s = rep(s, 'var DATA_URL = "data/resources.json";',
               'var DATA_URL = "/data/resources.json";', label="DATA_URL")

    s = rep(s, 'return n + " " + (n === 1 ? one : many);',
               'return n + " " + T(n === 1 ? one : many);', label="plural")

    s = rep(s, 'return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });',
               'return d.toLocaleDateString(LANG === "es" ? "es-ES" : "en-GB",\n'
               '                            { day: "numeric", month: "short", year: "numeric" });',
            label="date locale")

    # taxonomy labels: label_es beside label, English as the fallback
    s = rep(s, 'for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i].label;',
               'for (var i = 0; i < list.length; i++) {\n'
               '      if (list[i].id !== id) continue;\n'
               '      return list[i]["label_" + LANG] || list[i].label;\n'
               '    }', label="labelFor")

    # the format list and every pill row render a label directly
    s = rep(s, 'ul.appendChild(row(null, "All Resources", "i-grid", state.all.length, state.format === null));',
               'ul.appendChild(row(null, T("All Resources"), "i-grid", state.all.length, state.format === null));',
            label="all resources")
    s = rep(s, 'ul.appendChild(pill(null, "All", state.all.length, active === null));',
               'ul.appendChild(pill(null, T("All"), state.all.length, active === null));',
            label="all pill")

    for lit in ('"Results"', '"Latest Resources"', '"Nothing featured yet"',
                '"No resources published yet"', '"Nothing matches those filters"',
                '"Try a different category, format or search term."',
                '"Tell us a little more about what you\'d like."',
                '"That email address doesn\'t look right."',
                '"Too many requests just now. Please try again later."',
                '"We couldn\'t send that. Please try again."',
                '"Something went wrong."'):
        s = rep(s, lit, "T(%s)" % lit, label="literal " + lit[:28])

    s = rep(s, '"Mark a resource with “featured” in data/resources.json and it will appear here."',
               'T("Mark a resource with “featured” in data/resources.json and it will appear here.")',
            label="featured empty body")
    s = rep(s, '"This hub is built and ready. Add entries to data/resources.json and they appear here — counts, filters and search all follow automatically."',
               'T("This hub is built and ready. Add entries to data/resources.json and they appear here — counts, filters and search all follow automatically.")',
            label="empty body")
    s = rep(s, '+ " match"', '+ T(" match")', label="match suffix")
    s = rep(s, 'el("span", null, r.minutes + " min")',
               'el("span", null, r.minutes + T(" min"))', n=2, label="min suffix")
    s = rep(s, 'btn.textContent = "Sending…";', 'btn.textContent = T("Sending…");',
            label="sending")
    s = rep(s, '"Couldn\'t load the resource list"', 'T("Couldn\'t load the resource list")',
            label="load error")

    # A Spanish page shows Spanish resources by default; ?lang= still wins.
    s = rep(s, '''    var want = null;
    try { want = new URLSearchParams(location.search).get("lang"); } catch (e) { return; }
    if (!want) return;''',
            '''    var want = null;
    try { want = new URLSearchParams(location.search).get("lang"); } catch (e) { want = null; }
    /* On a Spanish page the Spanish resources are the point, so preselect
       them. An explicit ?lang= in the URL still wins over the default. */
    if (!want && LANG !== "en") want = LANG;
    if (!want) return;''', label="default language")

    # The table goes in LAST: inserting it earlier would make its own Spanish
    # values match the literal replacements below and double-wrap them.
    anchor = "  function plural(n, one, many) {"
    s = rep(s, anchor, STRINGS.lstrip("\n") + anchor, label="string table")

    d = os.path.dirname(OUT)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)

    # postflight
    for never in ('"Latest Resources"', '"All Resources"', '+ " match"'):
        assert ('T(%s)' % never) in s or never not in s.replace('T(%s)' % never, ''), never
    print("hub.js localised: %d bytes -> %d" % (
        os.path.getsize(SRC), os.path.getsize(OUT)))


if __name__ == "__main__":
    run()
