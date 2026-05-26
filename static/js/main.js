import { initReveal } from './modules/reveal.js';
import { initHeader } from './modules/header.js';
import { initMobileNav } from './modules/nav.js';
import { initSliders } from './modules/slider.js';
import { initForms } from './modules/form.js';
import { initLightbox } from './modules/lightbox.js';
import { initModal } from './modules/modal.js';
import { initParallax } from './modules/parallax.js';
import { initLangSwitcher, syncPageShell } from './modules/lang-switcher.js';

function init() {
  initLangSwitcher();
  initHeader();
  initReveal();
  initMobileNav();
  initSliders();
  initForms();
  initLightbox();
  initParallax();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Sync title, body class and page-specific CSS before HTMX swaps content.
// Only applies to full-page boost navigations (target = #main-content).
// Partial swaps (modals, forms) must NOT trigger this — they have no <head>
// and would otherwise clear the page title, body classes and page CSS.
document.addEventListener('htmx:beforeSwap', (e) => {
  if (e.detail.target?.id !== 'main-content') return;

  const text = e.detail.xhr?.responseText;
  if (!text) return;

  const parser = new DOMParser();
  const newDoc = parser.parseFromString(text, 'text/html');

  syncPageShell(newDoc);

  // Update page title
  document.title = newDoc.title;

  // Update body class (e.g. has-hero)
  document.body.className = newDoc.body.className;

  // Sync page-specific CSS (files under /css/pages/)
  const isPageCSS = (href) => href && href.includes('/css/pages/');

  const currentLinks = [...document.querySelectorAll('link[rel="stylesheet"]')]
    .filter(l => isPageCSS(l.getAttribute('href') || l.href));

  const incomingLinks = [...newDoc.querySelectorAll('link[rel="stylesheet"]')]
    .filter(l => isPageCSS(l.getAttribute('href')));

  // Remove CSS no longer needed
  currentLinks.forEach(l => {
    const path = l.getAttribute('href') || new URL(l.href).pathname;
    const stillNeeded = incomingLinks.some(nl => nl.getAttribute('href') === path);
    if (!stillNeeded) l.remove();
  });

  // Inject new CSS (synchronous injection; browser starts loading in parallel with swap)
  incomingLinks.forEach(nl => {
    const href = nl.getAttribute('href');
    const alreadyLoaded = document.querySelector(`link[href="${href}"], link[href$="${href.split('/').pop()}"]`);
    if (alreadyLoaded) return;
    const el = document.createElement('link');
    el.rel = 'stylesheet';
    el.href = href;
    document.head.appendChild(el);
  });
});

// Re-init page modules after HTMX boost navigation (target = #main-content only).
// Partial swaps (modals, form results) must NOT re-init all modules —
// it would cancel running RAF loops, re-create observers, and reset state.
document.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target?.id !== 'main-content') return;

  // Keep lang-switcher "next" inputs in sync with the current URL
  document.querySelectorAll('input[name="next"]').forEach(input => {
    input.value = window.location.pathname + window.location.search;
  });

  initLangSwitcher();
  initHeader();
  initReveal();
  initMobileNav();
  initSliders();
  initForms();
  initLightbox();
  initParallax();
});

// Init modal and forms after HTMX settles swapped content
document.addEventListener('htmx:afterSettle', () => {
  initForms();
  initModal();
});

// Pass the current CSRF token from cookie with every HTMX request.
// Reads from cookie on each request so the value is always fresh,
// even after session rotation or hx-boost navigation.
document.addEventListener('htmx:configRequest', (evt) => {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  if (match) evt.detail.headers['X-CSRFToken'] = decodeURIComponent(match[1]);
});
