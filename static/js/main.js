import { initReveal } from './modules/reveal.js';
import { initHeader } from './modules/header.js';
import { initMobileNav } from './modules/nav.js';
import { initSliders } from './modules/slider.js';
import { initForms } from './modules/form.js';
import { initLightbox } from './modules/lightbox.js';
import { initModal } from './modules/modal.js';
import { initParallax } from './modules/parallax.js';
import { initLangSwitcher } from './modules/lang-switcher.js';
import { applyPageShell, resyncPageShellFromServer } from './modules/page-shell.js';

function initShellModules() {
  initLangSwitcher();
  initHeader();
  initMobileNav();
}

function initPageModules() {
  initShellModules();
  initReveal();
  initSliders();
  initForms();
  initLightbox();
  initParallax();
}

function init() {
  initPageModules();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Sync head/body shell before HTMX boost swaps #main-content.
document.addEventListener('htmx:beforeSwap', (e) => {
  if (e.detail.target?.id !== 'main-content') return;

  const text = e.detail.xhr?.responseText;
  if (!text) return;

  const newDoc = new DOMParser().parseFromString(text, 'text/html');
  applyPageShell(newDoc);
  initShellModules();
});

// HTMX history snapshot restores content but not per-page CSS / body class.
document.addEventListener('htmx:historyRestore', () => {
  resyncPageShellFromServer().then(() => initPageModules());
});

// Browser bfcache (Back/Forward) bypasses HTMX handlers.
window.addEventListener('pageshow', (event) => {
  if (!event.persisted) return;
  resyncPageShellFromServer().then(() => initPageModules());
});

document.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target?.id !== 'main-content') return;
  initPageModules();
});

document.addEventListener('htmx:afterSettle', () => {
  initForms();
  initModal();
});

document.addEventListener('htmx:configRequest', (evt) => {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  if (match) evt.detail.headers['X-CSRFToken'] = decodeURIComponent(match[1]);
});
