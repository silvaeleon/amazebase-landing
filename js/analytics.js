/* ==========================================================================
   FILE: js/analytics.js -- WRITTEN BY tools/analytics.py. Edit that, not this:
   `python tools/analytics.py --check` compares this file byte for byte and
   the pre-push hook fails if they differ.

   Every page loads gtag.js and then this file. The config lines live in a
   file rather than inline because the CSP carries exactly one sha256 hash and
   we are keeping it that way -- see tools/analytics.py for the whole story.

   CONSENT
   Nothing is granted by default. A first-time visitor is measured with every
   storage type DENIED, which under Consent Mode means Google counts the visit
   but writes no cookie and keeps no identifier, until they answer the banner
   in js/consent.js. That file is loaded at the bottom of this one.

   A RETURNING visitor's stored answer is read below and becomes the DEFAULT,
   not an update. This matters: an update arriving after the config commands
   would leave the first page view of every session measured under the wrong
   consent state. Reading it here closes that gap.

   WHAT IS CONFIGURED
       G-M8R4ZTFM6H     Google Analytics 4, property "amazebase.pro"
       AW-11127271562   Google Ads, for the "Waitlist signup" conversion that
                        js/waitlist.js fires once the server accepts a signup
========================================================================== */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

var abConsent = null;
try {
  var abRaw = window.localStorage.getItem('ab_consent_v1');
  if (abRaw) {
    var abSaved = JSON.parse(abRaw);
    if (abSaved && typeof abSaved.analytics === 'boolean'
        && typeof abSaved.ads === 'boolean' && abSaved.at
        && (Date.now() - abSaved.at) < 31536000000) {
      abConsent = abSaved;
    }
  }
} catch (e) {
  abConsent = null;
}

gtag('consent', 'default', {
  analytics_storage:  abConsent && abConsent.analytics ? 'granted' : 'denied',
  ad_storage:         abConsent && abConsent.ads ? 'granted' : 'denied',
  ad_user_data:       abConsent && abConsent.ads ? 'granted' : 'denied',
  ad_personalization: abConsent && abConsent.ads ? 'granted' : 'denied',
  wait_for_update: 500
});

gtag('set', 'url_passthrough', true);
gtag('set', 'ads_data_redaction', true);

gtag('js', new Date());
gtag('config', 'G-M8R4ZTFM6H');
gtag('config', 'AW-11127271562');

(function () {
  var s = document.createElement('script');
  s.src = '/js/consent.js';
  s.defer = true;
  (document.head || document.documentElement).appendChild(s);
})();
