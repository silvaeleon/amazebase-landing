/* ==========================================================================
   FILE: js/main.js
   Nav state · mobile menu · scroll reveal · counters · magnetic CTAs ·
   dashboard tilt · back to top.
   No dependencies. No inline handlers.
========================================================================== */

(function () {
  "use strict";

  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------- HEADER */

  const header = $(".site-header");
  const toTop  = $(".to-top");

  const onScroll = () => {
    const y = window.scrollY;
    if (header) header.classList.toggle("is-stuck", y > 12);
    if (toTop)  toTop.classList.toggle("is-on", y > 700);
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  }

  /* ---------------------------------------------------------- MOBILE MENU */

  const toggle = $(".nav-toggle");
  const drawer = $(".nav-mobile");

  if (toggle && drawer) {
    toggle.addEventListener("click", () => {
      const open = drawer.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    drawer.addEventListener("click", (e) => {
      if (e.target.closest("a")) {
        drawer.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* --------------------------------------------------------- SCROLL REVEAL */

  const revealables = $$("[data-reveal], [data-reveal-stagger]");

  if (revealables.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      revealables.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
      );
      revealables.forEach((el) => io.observe(el));
    }
  }

  /* -------------------------------------------------------------- COUNTERS */

  const formatValue = (raw, value) => {
    // Preserves the prefix/suffix authored in the markup, e.g. "$2B+", "200K+"
    const prefix = (raw.match(/^[^\d]*/) || [""])[0];
    const suffix = (raw.match(/[^\d]*$/) || [""])[0];
    return prefix + value.toLocaleString("en-US") + suffix;
  };

  const runCounter = (el) => {
    const target = Number(el.dataset.counter);
    if (!Number.isFinite(target)) return;

    const raw = el.textContent.trim();
    const duration = 1500;
    const start = performance.now();

    const step = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = formatValue(raw, Math.round(target * eased));
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = formatValue(raw, target);
    };

    requestAnimationFrame(step);
  };

  const counters = $$("[data-counter]");

  if (counters.length && !reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          runCounter(entry.target);
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => io.observe(el));
  }

  /* ------------------------------------------------------ MAGNETIC BUTTONS */

  if (!reduced && window.matchMedia("(pointer: fine)").matches) {
    $$("[data-magnetic]").forEach((el) => {
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.16;
        const y = (e.clientY - r.top - r.height / 2) * 0.28;
        el.style.translate = `${x}px ${y}px`;
      });
      el.addEventListener("mouseleave", () => {
        el.style.translate = "0px 0px";
      });
    });
  }

  /* -------------------------------------------------------- DASHBOARD TILT */

  const dash = $("[data-tilt]");

  if (dash && !reduced && window.matchMedia("(min-width: 1121px)").matches) {
    const base = "perspective(2200px)";
    let frame = null;

    dash.addEventListener("mousemove", (e) => {
      if (frame) return;
      frame = requestAnimationFrame(() => {
        const r = dash.getBoundingClientRect();
        const rx = ((r.height / 2 - (e.clientY - r.top)) / (r.height / 2)) * 3;
        const ry = (((e.clientX - r.left) - r.width / 2) / (r.width / 2)) * 4 - 3;
        dash.style.transform = `${base} rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) translateY(-6px)`;
        frame = null;
      });
    });

    dash.addEventListener("mouseleave", () => {
      dash.style.transform = "";
    });
  }

  /* ------------------------------------------------------- LIVE DASH VALUES */

  const bars = $$("[data-live-bar]");

  if (bars.length && !reduced) {
    setInterval(() => {
      bars.forEach((bar) => {
        bar.style.height = 30 + Math.random() * 62 + "%";
      });
    }, 3000);
  }

  /* ---------------------------------------------------------- ANCHOR OFFSET */

  $$('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const id = link.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.getElementById(id.slice(1));
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    });
  });

  /* ------------------------------------------------------ DEEP LINK ON LOAD */
  /* The handler above only fires on click, so opening /product.html#simulations
     cold left the page at the top with the target still at opacity:0 — every
     anchor in the Product menu is a URL people copy and share. Reveal the
     target and everything above it first, so the landing position is stable
     and scrolling back up isn't a wall of invisible sections. */

  if (location.hash.length > 1) {
    const target = document.getElementById(
      decodeURIComponent(location.hash.slice(1))
    );

    if (target) {
      revealables.forEach((el) => {
        const atOrInside =
          el === target || el.contains(target) || target.contains(el);
        const above =
          el.compareDocumentPosition(target) & Node.DOCUMENT_POSITION_FOLLOWING;
        if (atOrInside || above) el.classList.add("is-in");
      });

      requestAnimationFrame(() => {
        target.scrollIntoView({ behavior: "auto", block: "start" });
      });
    }
  }
})();
