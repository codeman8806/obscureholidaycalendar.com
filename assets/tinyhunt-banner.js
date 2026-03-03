// Tinyhunt launch banner injector (sitewide)
// Shows Mar 3–9, 2026 local time; hides starting Mar 10.
(function(){
  try {
    var start = new Date(2026, 2, 3); // Mar 3, 2026
    var endExclusive = new Date(2026, 2, 10); // Mar 10, 2026
    var now = new Date();
    if (now < start || now >= endExclusive) return;
    if (document.getElementById('th-banner')) return; // already present (e.g., homepage)
    if (localStorage.getItem('th_banner_dismissed') === '1') return;

    var header = document.querySelector('.site-header');
    if (!header) return;

    var banner = document.createElement('div');
    banner.id = 'th-banner';
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', 'Launch banner');
    banner.style.cssText = 'background:#111;color:#fff;padding:10px 14px;display:flex;align-items:center;gap:12px;';

    var strong = document.createElement('strong');
    strong.textContent = 'We\u2019re live on Tinyhunt today';
    strong.style.cssText = 'font:600 14px/1.2 system-ui';
    banner.appendChild(strong);

    var link = document.createElement('a');
    link.href = '/go/tinyhunt/';
    link.textContent = 'Check it out';
    link.style.cssText = 'background:#ffd24d;color:#111;padding:6px 10px;border-radius:6px;text-decoration:none;';
    banner.appendChild(link);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Dismiss banner');
    btn.textContent = '×';
    btn.style.cssText = 'margin-left:auto;background:transparent;border:0;color:#fff;font-size:18px;cursor:pointer;';
    btn.addEventListener('click', function(){
      try { localStorage.setItem('th_banner_dismissed','1'); } catch (e) {}
      banner.remove();
    });
    banner.appendChild(btn);

    header.parentNode.insertBefore(banner, header);

    if (window.gtag && link) {
      link.addEventListener('click', function(){
        try { gtag('event', 'tinyhunt_click', {source_page: location.pathname, placement: 'banner_sitewide'}); } catch (e) {}
      });
    }
  } catch (e) {
    // fail silent
  }
})();

