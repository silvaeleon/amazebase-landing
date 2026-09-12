/* ==========================================================================
   FILE: js/consent.js
   The cookie banner. Loaded by js/analytics.js, which every page loads.

   WHAT IT IS FOR
   Google Analytics and Google Ads are configured in js/analytics.js with
   Consent Mode, and Microsoft Clarity is loaded from here on an analytics
   yes. Until a visitor answers this banner every storage type is
   DENIED, which means Google still counts the visit but writes no cookie and
   keeps no identifier. This file is what turns that "denied" into the
   visitor's actual answer, and remembers it.

   WHY THE ANSWER LIVES IN localStorage AND NOT A COOKIE
   A cookie that records "no cookies please" is its own small joke, and it
   would travel to the server on every request for no reason. localStorage is
   per-browser, never sent anywhere, and is exactly as durable as we need.
   Every read and write is wrapped: a private window or blocked site data
   throws, and the correct behaviour there is to show the banner again, not to
   break the page.

   WHY IT RE-ASKS AFTER A YEAR
   Consent is not forever. The stored answer carries the moment it was given
   and is treated as absent once it is older than 365 days.

   STYLING
   The styles are injected from here rather than added to css/, because the
   178 pages do not all link the same stylesheets -- article pages skip
   base.css. Every custom property is used with a literal fallback
   (var(--text, #EEF1F8)) so the banner looks native where the design tokens
   are loaded and correct where they are not. Injected <style> is allowed by
   the CSP because style-src carries 'unsafe-inline'; script-src does not,
   which is why this is a file and not an inline block.

   REOPENING IT
   Anything with a data-consent-open attribute reopens the chooser, and
   window.amazebaseConsent.open() does the same from the console. The legal
   pages carry such a link so a visitor can change their mind.
========================================================================== */
(function () {
  "use strict";

  if (window.amazebaseConsent) return;

  var KEY = "ab_consent_v1";
  var MAX_AGE = 365 * 24 * 60 * 60 * 1000;
  var CLARITY_ID = "yh4nta35du";

  /* ------------------------------------------------------------- LANGUAGE */
  /* The page declares its own language; everything else is a guess. */
  var lang = (document.documentElement.getAttribute("lang") || "en")
    .slice(0, 2).toLowerCase();
  if (lang !== "es" && lang !== "pt") lang = "en";

  var COPY = {
    en: {
      title: "A quick word about cookies",
      body: "AmazeBase uses Google Analytics to see which articles get read and roughly where readers are. Until you decide, we count your visit without cookies — nothing is stored on your device and you are not identified.",
      accept: "Accept",
      reject: "Decline",
      choose: "Let me choose",
      save: "Save choices",
      analyticsLabel: "Analytics",
      analyticsHelp: "Which pages you read, and roughly where you are.",
      adsLabel: "Advertising",
      adsHelp: "Lets us measure our ads and show them to people like you.",
      privacy: "Privacy Policy",
      privacyHref: "/privacy.html",
      close: "Close",
      region: "You can change this at any time."
    },
    es: {
      title: "Sobre las cookies, en corto",
      body: "AmazeBase usa Google Analytics para ver qué artículos se leen y aproximadamente desde dónde. Hasta que decidas, contamos tu visita sin cookies: no se guarda nada en tu dispositivo y no se te identifica.",
      accept: "Aceptar",
      reject: "Rechazar",
      choose: "Quiero elegir",
      save: "Guardar",
      analyticsLabel: "Analítica",
      analyticsHelp: "Qué páginas lees y aproximadamente dónde estás.",
      adsLabel: "Publicidad",
      adsHelp: "Nos permite medir nuestros anuncios y mostrarlos a personas como tú.",
      privacy: "Política de Privacidad",
      privacyHref: "/es/privacidad.html",
      close: "Cerrar",
      region: "Puedes cambiarlo cuando quieras."
    },
    pt: {
      title: "Sobre os cookies, em resumo",
      body: "A AmazeBase usa o Google Analytics para ver quais artigos são lidos e aproximadamente de onde. Até você decidir, contamos sua visita sem cookies: nada é gravado no seu dispositivo e você não é identificado.",
      accept: "Aceitar",
      reject: "Recusar",
      choose: "Quero escolher",
      save: "Salvar",
      analyticsLabel: "Análise",
      analyticsHelp: "Quais páginas você lê e aproximadamente onde você está.",
      adsLabel: "Publicidade",
      adsHelp: "Permite medir nossos anúncios e mostrá-los a pessoas como você.",
      privacy: "Política de Privacidade",
      privacyHref: "/pt/privacidade.html",
      close: "Fechar",
      region: "Você pode mudar isso quando quiser."
    }
  };
  var t = COPY[lang];

  /* -------------------------------------------------------------- STORAGE */

  function read() {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return null;
      var p = JSON.parse(raw);
      if (!p || typeof p.analytics !== "boolean" || typeof p.ads !== "boolean") return null;
      if (!p.at || (Date.now() - p.at) > MAX_AGE) return null;
      return p;
    } catch (e) {
      return null;
    }
  }

  function write(analytics, ads) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify({
        analytics: analytics, ads: ads, at: Date.now()
      }));
    } catch (e) {
      /* Private window, or the visitor blocks site data. The choice still
         applies to this page view; they are asked again next time, which is
         the safe direction to fail in. */
    }
  }

  /* Microsoft Clarity records what a visitor does on the page, so it is
     ANALYTICS consent that gates it, and it is simply never loaded for
     somebody who declined. The load is one-way on purpose: a script cannot be
     unloaded, so the only honest implementation is to not fetch it at all
     until there is a yes.

     Clarity's own snippet is an inline <script>, which this site's CSP
     refuses. This is the same bootstrap written out so it can live in a file
     the policy already allows. The CSP still has to name www.clarity.ms and
     the hosts Clarity reports to -- see the Caddyfile. */
  var clarityLoaded = false;

  function loadClarity() {
    if (clarityLoaded || !CLARITY_ID) return;
    clarityLoaded = true;
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    var c = document.createElement("script");
    c.async = true;
    c.src = "https://www.clarity.ms/tag/" + CLARITY_ID;
    (document.head || document.documentElement).appendChild(c);
  }

  function apply(analytics, ads) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        analytics_storage:  analytics ? "granted" : "denied",
        ad_storage:         ads ? "granted" : "denied",
        ad_user_data:       ads ? "granted" : "denied",
        ad_personalization: ads ? "granted" : "denied"
      });
    }
    if (analytics) loadClarity();
  }

  /* --------------------------------------------------------------- STYLES */

  var CSS =
    '.abc-bar{position:fixed;left:0;right:0;bottom:0;z-index:var(--z-top,1000);' +
      'display:flex;justify-content:center;padding:12px;pointer-events:none;}' +
    '.abc-card{pointer-events:auto;width:min(100%,760px);box-sizing:border-box;' +
      'background:var(--surface-solid,#0A1224);color:var(--text,#EEF1F8);' +
      'border:1px solid var(--line-strong,rgba(255,255,255,.14));' +
      'border-radius:var(--r-md,16px);box-shadow:var(--sh-2,0 18px 40px rgba(0,0,0,.42));' +
      'font-family:var(--font,"Inter",system-ui,sans-serif);font-size:var(--t-body,15px);' +
      'line-height:1.55;padding:20px 22px;' +
      'transform:translateY(12px);opacity:0;transition:transform .28s cubic-bezier(.22,.61,.36,1),opacity .28s cubic-bezier(.22,.61,.36,1);}' +
    '.abc-card.abc-in{transform:none;opacity:1;}' +
    '.abc-title{margin:0 0 6px;font-size:16px;font-weight:600;color:var(--text,#EEF1F8);}' +
    '.abc-body{margin:0 0 16px;color:var(--text-2,#98A2B8);max-width:62ch;}' +
    '.abc-body a{color:var(--violet-soft,#A971F7);}' +
    '.abc-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;}' +
    '.abc-btn{font:inherit;font-weight:600;cursor:pointer;border-radius:var(--r-sm,12px);' +
      'padding:10px 20px;border:1px solid transparent;transition:opacity .18s,border-color .18s;}' +
    '.abc-btn:hover{opacity:.86;}' +
    '.abc-primary{background:var(--violet,#8B3BF1);color:#fff;}' +
    '.abc-secondary{background:transparent;color:var(--text,#EEF1F8);' +
      'border-color:var(--line-strong,rgba(255,255,255,.14));}' +
    '.abc-link{background:none;border:0;padding:10px 4px;font:inherit;cursor:pointer;' +
      'color:var(--text-2,#98A2B8);text-decoration:underline;text-underline-offset:3px;}' +
    '.abc-link:hover{color:var(--text,#EEF1F8);}' +
    '.abc-spacer{flex:1 1 auto;}' +
    '.abc-opts{margin:4px 0 16px;display:none;flex-direction:column;gap:12px;' +
      'border-top:1px solid var(--line,rgba(255,255,255,.07));padding-top:16px;}' +
    '.abc-opts.abc-on{display:flex;}' +
    '.abc-opt{display:flex;gap:12px;align-items:flex-start;}' +
    '.abc-opt input{margin:3px 0 0;width:18px;height:18px;flex:none;' +
      'accent-color:var(--violet,#8B3BF1);cursor:pointer;}' +
    '.abc-opt label{cursor:pointer;}' +
    '.abc-opt b{display:block;font-weight:600;color:var(--text,#EEF1F8);}' +
    '.abc-opt span{color:var(--text-2,#98A2B8);font-size:var(--t-micro,13px);}' +
    '.abc-note{color:var(--text-3,#616C84);font-size:var(--t-micro,13px);margin:12px 0 0;}' +
    '.abc-card :focus-visible{outline:2px solid var(--violet-soft,#A971F7);outline-offset:3px;}' +
    '@media (max-width:520px){' +
      '.abc-card{padding:18px;}' +
      '.abc-row{flex-direction:column;align-items:stretch;}' +
      '.abc-spacer{display:none;}' +
      '.abc-btn,.abc-link{width:100%;}' +
    '}' +
    '@media (prefers-reduced-motion:reduce){' +
      '.abc-card{transition:none;transform:none;opacity:1;}' +
    '}';

  function injectStyles() {
    if (document.getElementById("abc-style")) return;
    var s = document.createElement("style");
    s.id = "abc-style";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  /* ------------------------------------------------------------------ UI */

  var bar = null;

  function close() {
    if (!bar) return;
    bar.remove();
    bar = null;
  }

  function open(existing) {
    if (bar) return;
    injectStyles();

    bar = document.createElement("div");
    bar.className = "abc-bar";

    var card = document.createElement("div");
    card.className = "abc-card";
    card.setAttribute("role", "dialog");
    card.setAttribute("aria-live", "polite");
    card.setAttribute("aria-label", t.title);

    var h = document.createElement("p");
    h.className = "abc-title";
    h.textContent = t.title;

    var p = document.createElement("p");
    p.className = "abc-body";
    p.textContent = t.body + " ";
    var a = document.createElement("a");
    a.href = t.privacyHref;
    a.textContent = t.privacy;
    p.appendChild(a);

    /* -- the granular pair, hidden until asked for ------------------------ */
    var opts = document.createElement("div");
    opts.className = "abc-opts";

    function optRow(id, labelText, helpText, checked) {
      var row = document.createElement("div");
      row.className = "abc-opt";
      var box = document.createElement("input");
      box.type = "checkbox";
      box.id = id;
      box.checked = checked;
      var lab = document.createElement("label");
      lab.htmlFor = id;
      var b = document.createElement("b");
      b.textContent = labelText;
      var sp = document.createElement("span");
      sp.textContent = helpText;
      lab.appendChild(b);
      lab.appendChild(sp);
      row.appendChild(box);
      row.appendChild(lab);
      opts.appendChild(row);
      return box;
    }

    var prev = existing || { analytics: false, ads: false };
    var boxA = optRow("abc-analytics", t.analyticsLabel, t.analyticsHelp, prev.analytics);
    var boxD = optRow("abc-ads", t.adsLabel, t.adsHelp, prev.ads);

    /* -- buttons ---------------------------------------------------------- */
    var row = document.createElement("div");
    row.className = "abc-row";

    var accept = document.createElement("button");
    accept.type = "button";
    accept.className = "abc-btn abc-primary";
    accept.textContent = t.accept;

    var reject = document.createElement("button");
    reject.type = "button";
    reject.className = "abc-btn abc-secondary";
    reject.textContent = t.reject;

    var choose = document.createElement("button");
    choose.type = "button";
    choose.className = "abc-link";
    choose.textContent = t.choose;

    var save = document.createElement("button");
    save.type = "button";
    save.className = "abc-btn abc-primary";
    save.textContent = t.save;
    save.hidden = true;

    var spacer = document.createElement("div");
    spacer.className = "abc-spacer";

    row.appendChild(accept);
    row.appendChild(reject);
    row.appendChild(spacer);
    row.appendChild(choose);
    row.appendChild(save);

    var note = document.createElement("p");
    note.className = "abc-note";
    note.textContent = t.region;

    card.appendChild(h);
    card.appendChild(p);
    card.appendChild(opts);
    card.appendChild(row);
    card.appendChild(note);
    bar.appendChild(card);
    document.body.appendChild(bar);

    requestAnimationFrame(function () { card.classList.add("abc-in"); });

    function decide(analytics, ads) {
      write(analytics, ads);
      apply(analytics, ads);
      close();
    }

    accept.addEventListener("click", function () { decide(true, true); });
    reject.addEventListener("click", function () { decide(false, false); });
    save.addEventListener("click", function () { decide(boxA.checked, boxD.checked); });

    choose.addEventListener("click", function () {
      opts.classList.add("abc-on");
      choose.hidden = true;
      accept.hidden = true;
      reject.hidden = true;
      save.hidden = false;
      boxA.focus();
    });

    /* The banner never traps focus and never blocks the page: it is a strip
       at the bottom, not a modal. Somebody who wants to read first can. */
    accept.focus({ preventScroll: true });
  }

  /* --------------------------------------------------------------- BOOT */

  var saved = read();
  if (saved) {
    apply(saved.analytics, saved.ads);
  } else if (document.body) {
    open(null);
  } else {
    document.addEventListener("DOMContentLoaded", function () { open(null); });
  }

  document.addEventListener("click", function (e) {
    var el = e.target.closest && e.target.closest("[data-consent-open]");
    if (!el) return;
    e.preventDefault();
    open(read());
  });

  window.amazebaseConsent = {
    open: function () { open(read()); },
    get: function () { return read(); }
  };
})();
