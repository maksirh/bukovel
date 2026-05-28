/**
 * Перемикач мов — звичайні посилання (/ ↔ /en/), без HTMX і без POST.
 */
export function initLangSwitcher() {
  document.querySelectorAll('.lang-switcher a.lang-switcher__btn').forEach((link) => {
    link.setAttribute('hx-boost', 'false');
  });
}

/**
 * Оновлює header/footer/mobile-nav з повної HTML-відповіді HTMX boost.
 */
export function syncPageShell(newDoc) {
  if (!newDoc) return;

  ['#site-header', '#site-footer', '#mobile-nav'].forEach((selector) => {
    const incoming = newDoc.querySelector(selector);
    const current = document.querySelector(selector);
    if (incoming && current) {
      current.replaceWith(document.importNode(incoming, true));
    }
  });
}
