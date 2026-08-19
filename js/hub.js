/* ==========================================================================
   FILE: js/hub.js
   Knowledge Hub — reads data/resources.json and builds the whole page from it.

   Every count, filter, tab and search result is derived from that file. There
   are no hardcoded numbers anywhere: an empty resources array renders honest
   empty states rather than an impressive-looking lie.

   No dependencies. No inline handlers. No innerHTML — every element is built
   with createElement and filled with textContent, so a resource title
   containing markup can never become markup.
========================================================================== */

(function () {
  "use strict";

  var DATA_URL = "data/resources.json";
  var API      = "https://amz-analytics-production.up.railway.app";

  var $ = function (s, r) { return (r || document).querySelector(s); };

  var state = {
    all: [],
    categories: [],
    formats: [],
    levels: [],
    languages: [],
    category: null,     // active category id, null = all
    format: null,       // active format id, null = all
    level: null,        // active level id, null = all
    language: null,     // active language id, null = all
    topic: null,        // active topic, null = all
    query: "",
    sort: "latest"
  };

  /* ------------------------------------------------------------ DOM HELPERS */

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = String(text);
    return n;
  }

  function icon(id, cls) {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", cls || "icon-sm");
    svg.setAttribute("aria-hidden", "true");
    var use = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use.setAttribute("href", "#" + id);
    svg.appendChild(use);
    return svg;
  }

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function plural(n, one, many) {
    return n + " " + (n === 1 ? one : many);
  }

  function formatDate(iso) {
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d)) return iso;
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  }

  function labelFor(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i].label;
    return id;
  }

  function iconFor(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i].icon;
    return "i-report";
  }

  /* A resource may belong to more than one category. `categories` (array) wins
     if present; `category` (string) is the original single-value form and is
     still supported, so no existing entry needs rewriting. Everything that
     reads a category goes through this — filtering, counting and search. */
  function catsOf(r) {
    if (r.categories && r.categories.length) return r.categories;
    return r.category ? [r.category] : [];
  }

  function inCat(r, id) {
    return catsOf(r).indexOf(id) !== -1;
  }

  /* ---------------------------------------------------------------- FILTER */

  function visible() {
    var q = state.query.trim().toLowerCase();
    return state.all.filter(function (r) {
      if (state.category && !inCat(r, state.category)) return false;
      if (state.format   && r.format   !== state.format)   return false;
      if (state.level    && r.level    !== state.level)    return false;
      if (state.language && r.language !== state.language) return false;
      if (state.topic && (r.topics || []).indexOf(state.topic) === -1) return false;
      if (!q) return true;
      var catNames = catsOf(r).map(function (c) {
                       return labelFor(state.categories, c);
                     });
      var hay = [r.title, r.summary, r.author].concat(catNames)
                  .concat(r.topics || []).join(" ").toLowerCase();
      return hay.indexOf(q) !== -1;
    }).sort(function (a, b) {
      if (state.sort === "reading") {
        return (a.minutes || 999) - (b.minutes || 999);
      }
      return String(b.published).localeCompare(String(a.published));
    });
  }

  /* Any active narrowing? The Featured block is only meaningful when the
     visitor is browsing everything — once they filter, a "Featured" strip
     showing items outside the filter directly contradicts what they clicked. */
  function filtering() {
    return !!(state.category || state.format || state.level ||
              state.language || state.topic || state.query.trim());
  }

  function activeLabel() {
    if (state.query.trim()) return "Results";
    if (state.topic) return state.topic;
    if (state.category) return labelFor(state.categories, state.category);
    if (state.format) return labelFor(state.formats, state.format);
    if (state.level) return labelFor(state.levels, state.level);
    if (state.language) return labelFor(state.languages, state.language);
    return "Latest Resources";
  }

  function countIn(pred) {
    var n = 0;
    for (var i = 0; i < state.all.length; i++) if (pred(state.all[i])) n++;
    return n;
  }

  /* ------------------------------------------------------------- RENDERERS */

  function renderCategories() {
    var wrap = $("[data-hub-categories]");
    clear(wrap);
    state.categories.forEach(function (c) {
      var n = countIn(function (r) { return inCat(r, c.id); });
      var b = el("button", "hub-cat" + (state.category === c.id ? " is-on" : ""));
      b.type = "button";
      b.setAttribute("aria-pressed", state.category === c.id ? "true" : "false");

      var ico = el("span", "hub-cat-ico tint-" + (c.tint || "violet"));
      ico.appendChild(icon(c.icon, "icon"));
      b.appendChild(ico);

      var txt = el("span", "hub-cat-txt");
      txt.appendChild(el("span", "hub-cat-label", c.label));
      txt.appendChild(el("span", "hub-cat-count", plural(n, "resource", "resources")));
      b.appendChild(txt);

      b.addEventListener("click", function () {
        state.category = state.category === c.id ? null : c.id;
        renderAll();
      });
      wrap.appendChild(b);
    });
  }

  function renderFormats() {
    var ul = $("[data-hub-formats]");
    clear(ul);

    function row(id, label, iconId, n, on) {
      var li = el("li");
      var b = el("button", "hub-fmt" + (on ? " is-on" : ""));
      b.type = "button";
      b.appendChild(icon(iconId));
      b.appendChild(el("span", "hub-fmt-label", label));
      b.appendChild(el("span", "hub-fmt-n", n));
      b.addEventListener("click", function () {
        state.format = id;
        renderAll();
      });
      li.appendChild(b);
      return li;
    }

    ul.appendChild(row(null, "All Resources", "i-grid", state.all.length, state.format === null));
    state.formats.forEach(function (f) {
      var n = countIn(function (r) { return r.format === f.id; });
      ul.appendChild(row(f.id, f.label, f.icon, n, state.format === f.id));
    });
  }

  /* Level and language are independent axes, not extra categories. They get
     their own compact pill rails so a visitor can narrow by category, format,
     level and language all at once without the four competing for one control. */
  function renderPills(sel, list, active, set) {
    var ul = $(sel);
    if (!ul) return;
    clear(ul);

    function pill(id, label, n, on) {
      var li = el("li");
      var b  = el("button", "hub-pill" + (on ? " is-on" : ""));
      b.type = "button";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.appendChild(el("span", "hub-pill-label", label));
      b.appendChild(el("span", "hub-pill-n", n));
      b.addEventListener("click", function () {
        set(id);
        renderAll();
      });
      li.appendChild(b);
      return li;
    }

    ul.appendChild(pill(null, "All", state.all.length, active === null));
    list.forEach(function (o) {
      var n = countIn(function (r) { return r[o.field] === o.id; });
      ul.appendChild(pill(o.id, o.label, n, active === o.id));
    });
  }

  function withField(list, field) {
    return list.map(function (o) {
      return { id: o.id, label: o.label, field: field };
    });
  }

  function renderLevels() {
    renderPills("[data-hub-levels]", withField(state.levels, "level"),
                state.level, function (id) { state.level = id; });
  }

  function renderLanguages() {
    renderPills("[data-hub-languages]", withField(state.languages, "language"),
                state.language, function (id) { state.language = id; });
  }

  function renderTopics() {
    var card = $("[data-hub-topics-card]");
    var ul   = $("[data-hub-topics]");
    var tally = {};
    state.all.forEach(function (r) {
      (r.topics || []).forEach(function (t) { tally[t] = (tally[t] || 0) + 1; });
    });
    var topics = Object.keys(tally).sort(function (a, b) { return tally[b] - tally[a]; }).slice(0, 10);

    card.hidden = topics.length === 0;
    clear(ul);
    topics.forEach(function (t) {
      var li = el("li");
      var b = el("button", "hub-topic" + (state.topic === t ? " is-on" : ""), t);
      b.type = "button";
      b.addEventListener("click", function () {
        state.topic = state.topic === t ? null : t;
        renderAll();
      });
      li.appendChild(b);
      ul.appendChild(li);
    });
  }

  /* Card artwork. `src` is whichever of hero/thumb suits the size being drawn,
     and the alt is empty on purpose: the title sits right beside it inside the
     same link, so describing the picture again only makes a screen reader read
     every card twice. w/h are the real pixel dimensions so the box is reserved
     before the file lands and the list does not jump while it loads. */
  function art(src, cls, w, h, eager) {
    var span = el("span", cls);
    var img  = el("img");
    img.src = src;
    img.alt = "";
    img.width = w; img.height = h;
    img.loading = eager ? "eager" : "lazy";
    img.decoding = "async";
    span.appendChild(img);
    return span;
  }

  function card(r, big) {
    var a = el("a", "hub-feat" + (big ? " is-big" : ""));
    a.href = r.url || "#";
    if (/^https?:/.test(r.url || "")) { a.target = "_blank"; a.rel = "noopener noreferrer"; }

    /* The big card is above the fold and is drawn wide, so it gets the full
       hero. The two stacked cards are small - the 480px thumb is already more
       than they can show. Either may be absent; the card still renders. */
    var pic = big ? (r.hero || r.thumb) : (r.thumb || r.hero);
    if (pic) a.appendChild(art(pic, "hub-feat-art", big ? 1672 : 480, big ? 941 : 270, big));

    var badge = el("span", "hub-badge", labelFor(state.formats, r.format).replace(/s$/, ""));
    a.appendChild(badge);

    a.appendChild(el(big ? "h3" : "h4", "hub-feat-h", r.title));
    if (big && r.summary) a.appendChild(el("p", "hub-feat-p", r.summary));

    var meta = el("div", "hub-feat-meta");
    if (r.author) meta.appendChild(el("span", null, r.author));
    meta.appendChild(el("span", null, formatDate(r.published)));
    if (r.minutes) meta.appendChild(el("span", null, r.minutes + " min"));
    a.appendChild(meta);
    return a;
  }

  function renderFeatured() {
    var sec  = $("[data-hub-featured-sec]");
    var wrap = $("[data-hub-featured]");

    if (filtering()) {           // was: featured ignored filters entirely
      if (sec) sec.hidden = true;
      clear(wrap);
      return;
    }
    if (sec) sec.hidden = false;
    clear(wrap);
    var feat = state.all.filter(function (r) { return r.featured; })
                        .sort(function (a, b) { return String(b.published).localeCompare(String(a.published)); });

    if (!feat.length) {
      wrap.appendChild(emptyState(
        "Nothing featured yet",
        "Mark a resource with “featured” in data/resources.json and it will appear here."
      ));
      return;
    }
    wrap.appendChild(card(feat[0], true));
    if (feat.length > 1) {
      var stack = el("div", "hub-feat-stack");
      feat.slice(1, 3).forEach(function (r) { stack.appendChild(card(r, false)); });
      wrap.appendChild(stack);
    }
  }

  function emptyState(title, body) {
    var d = el("div", "hub-empty");
    d.appendChild(icon("i-stack", "icon"));
    d.appendChild(el("p", "hub-empty-h", title));
    d.appendChild(el("p", "hub-empty-p", body));
    return d;
  }

  function renderList() {
    var wrap = $("[data-hub-list]");
    var out  = visible();
    clear(wrap);

    var countEl = $("[data-hub-count]");
    if (!state.all.length) {
      countEl.textContent = "";
      wrap.appendChild(emptyState(
        "No resources published yet",
        "This hub is built and ready. Add entries to data/resources.json and they appear here — counts, filters and search all follow automatically."
      ));
      return;
    }

    countEl.textContent = filtering()
      ? plural(out.length, "resource", "resources") + " match"
      : plural(out.length, "resource", "resources");

    if (!out.length) {
      wrap.appendChild(emptyState(
        "Nothing matches those filters",
        "Try a different category, format or search term."
      ));
      return;
    }

    out.forEach(function (r) {
      var a = el("a", "hub-row");
      a.href = r.url || "#";
      if (/^https?:/.test(r.url || "")) { a.target = "_blank"; a.rel = "noopener noreferrer"; }

      /* With a thumb, the format icon rides on the picture as a small chip:
         the row keeps its three columns, and the format stays readable at
         640px and below where .hub-row-tag is hidden for space. Without a
         thumb the icon renders on its own exactly as it did before. */
      var ico = el("span", "hub-row-ico");
      ico.appendChild(icon(iconFor(state.formats, r.format)));
      if (r.thumb) {
        var th = art(r.thumb, "hub-row-thumb", 480, 270, false);
        th.appendChild(ico);
        a.appendChild(th);
      } else {
        a.appendChild(ico);
      }

      var body = el("div", "hub-row-body");
      body.appendChild(el("h4", "hub-row-h", r.title));
      if (r.summary) body.appendChild(el("p", "hub-row-p", r.summary));
      var meta = el("div", "hub-row-meta");
      meta.appendChild(el("span", null, formatDate(r.published)));
      if (r.minutes) meta.appendChild(el("span", null, r.minutes + " min"));
      body.appendChild(meta);
      a.appendChild(body);

      a.appendChild(el("span", "hub-row-tag", labelFor(state.formats, r.format).replace(/s$/, "")));
      wrap.appendChild(a);
    });
  }

  function renderTestimonials(list) {
    var sec = $("[data-hub-testimonials-sec]");
    var wrap = $("[data-hub-testimonials]");
    if (!list || !list.length) { sec.hidden = true; return; }
    sec.hidden = false;
    clear(wrap);
    list.forEach(function (t) {
      var q = el("figure", "hub-quote");
      q.appendChild(el("blockquote", null, t.quote));
      var cap = el("figcaption");
      cap.appendChild(el("span", "hub-quote-name", t.name));
      if (t.role) cap.appendChild(el("span", "hub-quote-role", t.role));
      q.appendChild(cap);
      wrap.appendChild(q);
    });
  }

  function renderChrome() {
    var head  = $("[data-hub-list-heading]");
    var clr   = $("[data-hub-clear]");
    if (head) head.textContent = activeLabel();
    if (clr)  clr.hidden = !filtering();
  }

  function renderAll() {
    renderCategories();
    renderFormats();
    renderTopics();
    renderLevels();
    renderLanguages();
    renderFeatured();
    renderList();
    renderChrome();
  }

  var clearBtnEl = $("[data-hub-clear]");
  if (clearBtnEl) {
    clearBtnEl.addEventListener("click", function () {
      state.category = null;
      state.format   = null;
      state.level    = null;
      state.language = null;
      state.topic    = null;
      state.query    = "";
      var inp = $("[data-hub-search]");
      if (inp) inp.value = "";
      var x = $("[data-hub-search-clear]");
      if (x) x.hidden = true;
      renderAll();
    });
  }

  /* ---------------------------------------------------------------- SEARCH */

  var input = $("[data-hub-search]");
  var clearBtn = $("[data-hub-search-clear]");

  if (input) {
    input.addEventListener("input", function () {
      state.query = input.value;
      clearBtn.hidden = !input.value;
      renderFeatured();
      renderList();
      renderChrome();
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      input.value = ""; state.query = ""; clearBtn.hidden = true;
      renderFeatured(); renderList(); renderChrome(); input.focus();
    });
  }

  var tabs = $("[data-hub-tabs]");
  if (tabs) {
    tabs.addEventListener("click", function (e) {
      var b = e.target.closest("[data-sort]");
      if (!b) return;
      state.sort = b.getAttribute("data-sort");
      Array.prototype.forEach.call(tabs.querySelectorAll("[data-sort]"), function (t) {
        var on = t === b;
        t.classList.toggle("is-on", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      renderList();
    });
  }

  /* ------------------------------------------------- REQUEST CONTENT DIALOG */

  (function requestDialog() {
    var dlg = document.getElementById("request");
    if (!dlg || typeof dlg.showModal !== "function") return;

    var form = dlg.querySelector("form");
    var done = dlg.querySelector("[data-request-done]");
    var err  = dlg.querySelector("[data-request-error]");
    var btn  = dlg.querySelector("[data-request-submit]");
    var sending = false;

    function showErr(m) { err.textContent = m || ""; err.hidden = !m; }

    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-request-open]")) {
        e.preventDefault();
        showErr(""); form.hidden = false; done.hidden = true;
        dlg.showModal();
        var t = form.querySelector("#rq-topic"); if (t) t.focus();
      }
      if (e.target.closest("[data-request-close]")) { e.preventDefault(); dlg.close(); }
    });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending) return;

      var topic = form.elements.topic.value.trim();
      var email = form.elements.email.value.trim();
      if (topic.length < 5) return showErr("Tell us a little more about what you'd like.");
      if (email && (email.indexOf("@") < 1 || email.indexOf(".") === -1)) {
        return showErr("That email address doesn't look right.");
      }

      sending = true; showErr(""); btn.disabled = true; btn.textContent = "Sending…";

      fetch(API + "/content-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic,
          email: email,
          company_website: form.elements.company_website.value
        })
      })
        .then(function (res) {
          if (res.ok) return;
          if (res.status === 429) throw new Error("Too many requests just now. Please try again later.");
          throw new Error("We couldn't send that. Please try again.");
        })
        .then(function () { form.hidden = true; done.hidden = false; })
        .catch(function (ex) { showErr(ex && ex.message ? ex.message : "Something went wrong."); })
        .then(function () {
          sending = false; btn.disabled = false; btn.textContent = "Send request";
        });
    });
  })();

  /* ------------------------------------------------------------------ BOOT */

  fetch(DATA_URL, { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error("Could not load " + DATA_URL + " (HTTP " + r.status + ")");
      return r.json();
    })
    .then(function (d) {
      state.categories = d.categories || [];
      state.levels     = d.levels     || [];
      state.languages  = d.languages  || [];
      state.formats    = d.formats || [];
      state.all        = d.resources || [];
      renderAll();
      renderTestimonials(d.testimonials);
    })
    .catch(function (ex) {
      var wrap = $("[data-hub-list]");
      clear(wrap);
      wrap.appendChild(emptyState("Couldn't load the resource list", String(ex.message || ex)));
      renderCategories();
      renderFormats();
      renderFeatured();
    });
})();
