/* HYDRA — consent banner.
 *
 * Sovereign by construction: no third-party CMP, no external request, no cookie.
 * The choice lives in localStorage on the visitor's own machine.
 *
 * Consent Mode v2 defaults are set INLINE in each page <head>, before gtag.js
 * loads — this file only renders the banner and pushes the 'update'. Google
 * requires all four signals for EEA traffic since 2024-03-06; without them
 * remarketing audiences and conversion modelling are switched off.
 */
(function () {
  'use strict';

  var KEY = 'hydra-consent';
  var CS = (document.documentElement.lang || 'en').slice(0, 2) === 'cs';

  var T = CS ? {
    body: 'Měříme návštěvnost a vyhodnocujeme reklamu. Bez tvého souhlasu se nespustí nic — ' +
          'volba zůstává u tebe v prohlížeči, neposíláme ji nikam.',
    ok: 'Přijmout',
    no: 'Odmítnout',
    label: 'Souhlas s měřením'
  } : {
    body: 'We measure traffic and attribute advertising. Nothing runs before you agree — ' +
          'your choice stays in your own browser and is never sent anywhere.',
    ok: 'Accept',
    no: 'Decline',
    label: 'Measurement consent'
  };

  function grant(granted) {
    var v = granted ? 'granted' : 'denied';
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        ad_storage: v,
        ad_user_data: v,
        ad_personalization: v,
        analytics_storage: v
      });
    }
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  if (stored === 'granted' || stored === 'denied') return;   // already decided

  var css = [
    '#hydra-consent{position:fixed;left:0;right:0;bottom:0;z-index:9999;',
    'background:#0a0a12;border-top:1px solid #2a1a1e;',
    'box-shadow:0 -18px 44px rgba(0,0,0,.55);',
    'font-family:"JetBrains Mono",ui-monospace,monospace;',
    'transform:translateY(100%);transition:transform .28s ease}',
    '#hydra-consent.in{transform:translateY(0)}',
    '#hydra-consent .wrap{max-width:1100px;margin:0 auto;padding:18px 24px;',
    'display:flex;gap:22px;align-items:center;flex-wrap:wrap}',
    '#hydra-consent .lbl{color:#c41e1e;font-size:10px;letter-spacing:.22em;',
    'text-transform:uppercase;flex:0 0 100%;margin-bottom:-6px}',
    '#hydra-consent p{margin:0;color:#8a8580;font-size:12.5px;line-height:1.65;',
    'flex:1 1 380px;font-family:Inter,system-ui,sans-serif}',
    '#hydra-consent .btns{display:flex;gap:10px;flex:0 0 auto}',
    '#hydra-consent button{font:400 12px/1 "JetBrains Mono",monospace;',
    'letter-spacing:.08em;padding:11px 20px;border-radius:3px;cursor:pointer;',
    'border:1px solid #2a2a3a;background:transparent;color:#8a8580;',
    'transition:all .15s ease}',
    '#hydra-consent button:hover{color:#ebe8e3;border-color:#555048}',
    '#hydra-consent button.ok{background:#c41e1e;border-color:#c41e1e;color:#fff}',
    '#hydra-consent button.ok:hover{background:#d92222;border-color:#d92222;color:#fff}',
    '@media(max-width:620px){#hydra-consent .wrap{padding:16px}',
    '#hydra-consent .btns{flex:1 1 100%}#hydra-consent button{flex:1}}'
  ].join('');

  function show() {
    var st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);

    var bar = document.createElement('div');
    bar.id = 'hydra-consent';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', T.label);

    var wrap = document.createElement('div');
    wrap.className = 'wrap';

    var lbl = document.createElement('div');
    lbl.className = 'lbl';
    lbl.textContent = T.label;

    var p = document.createElement('p');
    p.textContent = T.body;

    var btns = document.createElement('div');
    btns.className = 'btns';

    var no = document.createElement('button');
    no.textContent = T.no;
    var ok = document.createElement('button');
    ok.className = 'ok';
    ok.textContent = T.ok;

    function close(granted) {
      grant(granted);
      bar.classList.remove('in');
      setTimeout(function () { if (bar.parentNode) bar.parentNode.removeChild(bar); }, 300);
    }
    no.addEventListener('click', function () { close(false); });
    ok.addEventListener('click', function () { close(true); });

    btns.appendChild(no);
    btns.appendChild(ok);
    wrap.appendChild(lbl);
    wrap.appendChild(p);
    wrap.appendChild(btns);
    bar.appendChild(wrap);
    document.body.appendChild(bar);
    requestAnimationFrame(function () { bar.classList.add('in'); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', show);
  } else {
    show();
  }
})();
