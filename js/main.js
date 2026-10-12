/* Progressive enhancement: all reviews and merchant links exist in the HTML. */
(() => {
  'use strict';
  const nav = document.querySelector('#navigation');
  const toggle = document.querySelector('#menu-toggle');
  const mobile = window.matchMedia('(max-width: 1000px)');
  if (nav && toggle) {
    const setMenu = (open, restoreFocus = false) => {
      nav.hidden = mobile.matches && !open;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.firstChild.textContent = open ? 'Cerrar ' : 'Menú ';
      if (restoreFocus) toggle.focus();
    };
    const syncMenu = () => {
      const focusInNav = nav.contains(document.activeElement);
      toggle.hidden = !mobile.matches;
      setMenu(!mobile.matches, mobile.matches && focusInNav);
    };
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && mobile.matches && !nav.hidden) setMenu(false, true);
    });
    document.addEventListener('click', event => {
      if (mobile.matches && !nav.hidden && !event.target.closest('.header')) setMenu(false, nav.contains(document.activeElement));
    });
    nav.addEventListener('click', event => { if (mobile.matches && event.target.closest('a')) setMenu(false); });
    mobile.addEventListener('change', syncMenu);
    syncMenu();
  }

  const form = document.querySelector('#filters');
  const cards = Array.from(document.querySelectorAll('[data-product]'));
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  if (form && cards.length) {
    const search = form.elements.namedItem('q');
    const category = form.elements.namedItem('category');
    const store = form.elements.namedItem('store');
    const status = document.querySelector('#result-count');
    const empty = document.querySelector('#empty-results');
    const searchable = cards.map(card => normalize(card.dataset.search));
    const filter = () => {
      const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach((card, index) => {
        const match = words.every(word => searchable[index].includes(word)) &&
          (!category.value || card.dataset.category === category.value) &&
          (!store.value || card.dataset.stores.split('|').includes(store.value));
        card.hidden = !match;
        if (match) count += 1;
      });
      status.textContent = `${count} ${count === 1 ? 'producto' : 'productos'} de ${cards.length}`;
      empty.hidden = count !== 0;
    };
    form.addEventListener('submit', event => { event.preventDefault(); filter(); });
    let timer;
    search.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(filter, 120); });
    form.addEventListener('change', filter);
    form.addEventListener('reset', () => { clearTimeout(timer); setTimeout(() => { filter(); search.focus(); }, 0); });
    const revealHash = () => {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const card = document.getElementById(id);
      if (!card || !card.matches('[data-product]')) return;
      clearTimeout(timer);
      search.value = ''; category.value = ''; store.value = ''; filter();
      const review = card.querySelector('details');
      if (review) review.open = true;
      card.scrollIntoView({ block: 'start' });
    };
    form.hidden = false;
    filter();
    // A direct product link takes priority over a restored browser filter value.
    if (location.hash) revealHash();
    window.addEventListener('hashchange', revealHash);
  }

  // Analytics loads only after an explicit choice. No search text is collected.
  const consentKey = 'recomiendatop-analytics-v1';
  const panel = document.querySelector('#consent');
  const preferences = document.querySelector('#privacy-preferences');
  let choice = null;
  let loaded = false;
  let returnFocus = null;
  try { choice = localStorage.getItem(consentKey); } catch { /* Browsing still works. */ }
  const loadAnalytics = () => {
    if (loaded || choice !== 'accepted') return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-W4BPKXL4';
    document.head.append(script);
  };
  if (panel && preferences) {
    preferences.hidden = false;
    panel.hidden = choice === 'accepted' || choice === 'rejected';
    preferences.addEventListener('click', () => {
      returnFocus = preferences;
      panel.hidden = false;
      panel.querySelector('button').focus();
    });
    panel.addEventListener('click', event => {
      const button = event.target.closest('[data-consent]');
      if (!button) return;
      choice = button.dataset.consent;
      let saved = true;
      try { localStorage.setItem(consentKey, choice); } catch { saved = false; }
      if (choice === 'rejected' && loaded) {
        if (saved) { location.reload(); return; }
        document.querySelector('#consent-status').textContent = 'El navegador no permite guardar tu elección. Cierra esta pestaña para detener las etiquetas que ya se cargaron.';
        return;
      }
      panel.hidden = true;
      loadAnalytics();
      // Move focus out of the hidden preference panel.
      (returnFocus || document.querySelector('#contenido')).focus({ preventScroll: true });
    });
    loadAnalytics();
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-store]');
    if (!link || choice !== 'accepted' || !loaded) return;
    window.dataLayer.push({event:'affiliate_click',product_id:link.closest('[data-product]')?.id || '',store:link.dataset.store,page_path:location.pathname});
  });
})();
