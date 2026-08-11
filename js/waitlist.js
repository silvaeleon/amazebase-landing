/* ==========================================================================
   FILE: js/waitlist.js
   Wait-list dialog — open/close, validation, submit.
   No dependencies. No inline handlers. No innerHTML.

   Every string that reaches the DOM goes through textContent, so a hostile
   response body can never become markup. Matches the XSS/CSP discipline the
   app itself is held to.
========================================================================== */

(function () {
  "use strict";

  /* The app that owns the waitlist table. Same-origin in local dev, the
     production app in the wild. Cross-origin, so the app must list this
     site in ALLOWED_ORIGINS or the browser blocks the POST. */
  var API = "https://amz-analytics-production.up.railway.app";

  var dialog = document.getElementById("waitlist");
  if (!dialog || typeof dialog.showModal !== "function") return;

  var form    = dialog.querySelector("form");
  var done    = dialog.querySelector("[data-waitlist-done]");
  var errorEl = dialog.querySelector("[data-waitlist-error]");
  var submit  = dialog.querySelector("[data-waitlist-submit]");
  var sourceField = "hero";
  var sending = false;
  /* When the dialog was opened. A human takes seconds to fill three fields;
     a script takes milliseconds. Sent with the submission so the app can
     reject the impossibly fast ones. */
  var openedAt = 0;

  /* ------------------------------------------------------------- OPEN/CLOSE */

  function open(source) {
    sourceField = source || "unknown";
    openedAt = Date.now();
    showError("");
    form.hidden = false;
    done.hidden = true;
    dialog.showModal();
    var first = form.querySelector("#wl-name");
    if (first) first.focus();
  }

  function close() {
    if (dialog.open) dialog.close();
  }

  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-waitlist-open]");
    if (opener) {
      e.preventDefault();
      open(opener.getAttribute("data-source"));
      return;
    }
    /* Fallback: ANY link pointing at the waitlist opens the dialog, even if
       whoever authored it forgot data-waitlist-open. Before this, a forgotten
       attribute silently cost a signup — the link just scrolled the page. */
    var link = e.target.closest('a[href$="#waitlist"]');
    if (link) {
      e.preventDefault();
      open(link.getAttribute("data-source") || "link");
      return;
    }
    if (e.target.closest("[data-waitlist-close]")) {
      e.preventDefault();
      close();
    }
  });

  /* Arriving with #waitlist in the URL opens the form. This is what makes the
     cross-page CTAs work: pages without the dialog (about, contact, privacy,
     terms, resources) link to index.html#waitlist and the form opens on
     arrival, instead of dumping the visitor at the pricing table. */
  if (window.location.hash === "#waitlist") open("deep-link");

  /* Click on the backdrop (the dialog element itself, not the panel) closes. */
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) close();
  });

  /* --------------------------------------------------------------- HELPERS */

  function showError(msg) {
    errorEl.textContent = msg || "";
    errorEl.hidden = !msg;
  }

  function validEmail(v) {
    var at = v.indexOf("@");
    if (at < 1 || at !== v.lastIndexOf("@")) return false;
    var domain = v.slice(at + 1);
    return domain.indexOf(".") > 0 && !/\s/.test(v) && v.length <= 254;
  }

  /* ---------------------------------------------------------------- SUBMIT */

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (sending) return;

    var name   = form.elements.name.value.trim();
    var email  = form.elements.email.value.trim();
    var market = form.elements.marketplace.value;

    if (!name)             return showError("Please tell us your name.");
    if (!validEmail(email)) return showError("That email address doesn't look right.");
    if (!market)           return showError("Please choose your main marketplace.");

    sending = true;
    showError("");
    submit.disabled = true;
    submit.textContent = "Joining…";

    fetch(API + "/waitlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name,
        email: email,
        marketplace: market,
        source: sourceField,
        elapsed_ms: openedAt ? Date.now() - openedAt : null,
        company_website: form.elements.company_website.value,
        referral_code: form.elements.referral_code
          ? form.elements.referral_code.value
          : ""
      })
    })
      .then(function (res) {
        if (res.ok) return res.json().catch(function () { return {}; });
        /* Read the server's message, but only ever as text. 429 gets its own
           wording because "too many requests" is meaningless to a visitor. */
        if (res.status === 429) {
          throw new Error("Too many attempts just now. Please try again in a little while.");
        }
        return res.json().then(
          function (b) { throw new Error(b && b.detail ? String(b.detail) : "Something went wrong."); },
          function ()  { throw new Error("Something went wrong."); }
        );
      })
      .then(function () {
        form.hidden = true;
        done.hidden = false;
        var closeBtn = done.querySelector("[data-waitlist-close]");
        if (closeBtn) closeBtn.focus();
      })
      .catch(function (err) {
        showError(err && err.message
          ? err.message
          : "We couldn't reach the server. Please try again.");
      })
      .then(function () {
        sending = false;
        submit.disabled = false;
        submit.textContent = "Join the wait list";
      });
  });
})();
