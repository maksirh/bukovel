/**
 * Перемикач мов: завжди повне перезавантаження сторінки (не HTMX boost).
 */
export function initLangSwitcher() {
  document.querySelectorAll('.lang-switcher form').forEach((form) => {
    if (form.dataset.langInit === '1') return;
    form.dataset.langInit = '1';
    form.setAttribute('hx-boost', 'false');

    form.addEventListener('submit', (event) => {
      event.stopImmediatePropagation();
    }, true);
  });
}

/**
 * Оновлює header/footer/mobile-nav з повної HTML-відповіді HTMX boost.
 */
export function syncPageShell(newDoc) {
  if (!newDoc) return;

  document.documentElement.lang = newDoc.documentElement.lang;

  ['data-i18n-close', 'data-i18n-prev', 'data-i18n-next', 'data-i18n-view'].forEach((attr) => {
    const value = newDoc.body.getAttribute(attr);
    if (value != null) {
      document.body.setAttribute(attr, value);
    }
  });

  ['#site-header', '#site-footer', '#mobile-nav'].forEach((selector) => {
    const incoming = newDoc.querySelector(selector);
    const current = document.querySelector(selector);
    if (incoming && current) {
      current.replaceWith(document.importNode(incoming, true));
    }
  });
}
