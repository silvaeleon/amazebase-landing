/* ==========================================================================
   FILE: js/analytics.js -- WRITTEN BY tools/analytics.py. Edit that, not this:
   `python tools/analytics.py --check` compares this file byte for byte and
   the pre-push hook fails if they differ.

   Every page loads gtag.js and then this file. The config lines live in a
   file rather than inline because the CSP carries exactly one sha256 hash and
   we are keeping it that way -- see tools/analytics.py for the whole story.

   CONSENT
   Consent Mode v2 defaults are set below, before any measurement command.
   gtag.js processes the dataLayer queue in order, so it sees consent first
   whichever of the two scripts finishes loading first. Advertising storage is
   denied everywhere. Analytics storage is denied in the EEA, the UK and
   Switzerland -- those visits are still counted, cookielessly and modelled --
   and granted everywhere else. There is no cookie banner on the site; if one
   is added it calls gtag('consent', 'update', ...) on accept and nothing here
   changes.

   WHAT IS CONFIGURED
       G-M8R4ZTFM6H     Google Analytics 4, property "amazebase.pro"
       AW-11127271562   Google Ads, for the "Waitlist signup" conversion that
                        js/waitlist.js fires once the server accepts a signup
========================================================================== */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'granted',
  wait_for_update: 500
});
gtag('consent', 'default', {
  region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU',
           'IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES',
           'SE','IS','LI','NO','GB','CH'],
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500
});
gtag('set', 'url_passthrough', true);
gtag('set', 'ads_data_redaction', true);

gtag('js', new Date());
gtag('config', 'G-M8R4ZTFM6H');
gtag('config', 'AW-11127271562');
