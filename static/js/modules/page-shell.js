import { syncPageShell } from './lang-switcher.js';

const PAGE_CSS_PATH = '/css/pages/';

function hrefPath(href) {
  if (!href) return '';
  try {
    return href.startsWith('http') ? new URL(href).pathname : href.split('?')[0];
  } catch {
    return href;
  }
}

/** Whitenoise hash: home.abc123def.css → home.css */
export function pageStylesheetKey(href) {
  const file = hrefPath(href).split('/').pop() || '';
  return file.replace(/\.[a-f0-9]{8,12}(?=\.css$)/i, '');
}

function pageStylesheetLinks(doc) {
  return [...doc.querySelectorAll('link[rel="stylesheet"]')].filter((link) => {
    const href = link.getAttribute('href') || '';
    return href.includes(PAGE_CSS_PATH);
  });
}

export function syncPageStylesFromDoc(newDoc) {
  const incoming = pageStylesheetLinks(newDoc);
  const incomingKeys = new Set(
    incoming.map((link) => pageStylesheetKey(link.getAttribute('href'))),
  );

  pageStylesheetLinks(document).forEach((link) => {
    const key = pageStylesheetKey(link.getAttribute('href') || link.href);
    if (!incomingKeys.has(key)) {
      link.remove();
    }
  });

  const currentKeys = new Set(
    pageStylesheetLinks(document).map((link) => pageStylesheetKey(link.getAttribute('href') || link.href)),
  );

  incoming.forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;

    const key = pageStylesheetKey(href);
    if (currentKeys.has(key)) return;

    const el = document.createElement('link');
    el.rel = 'stylesheet';
    el.href = href;
    document.head.appendChild(el);
  });
}

const BODY_CLASS_PRESERVE = ['modal-open'];

export function syncBodyClassFromDoc(newDoc) {
  const preserved = BODY_CLASS_PRESERVE.filter((cls) => document.body.classList.contains(cls));
  document.body.className = newDoc.body.className;
  preserved.forEach((cls) => document.body.classList.add(cls));

  ['data-i18n-close', 'data-i18n-prev', 'data-i18n-next', 'data-i18n-view'].forEach((attr) => {
    const value = newDoc.body.getAttribute(attr);
    if (value != null) {
      document.body.setAttribute(attr, value);
    }
  });
}

export function applyPageShell(newDoc) {
  if (!newDoc) return;

  document.documentElement.lang = newDoc.documentElement.lang;
  syncPageShell(newDoc);
  syncPageStylesFromDoc(newDoc);
  syncBodyClassFromDoc(newDoc);
  document.title = newDoc.title;

  const description = newDoc.querySelector('meta[name="description"]');
  if (description) {
    const current = document.querySelector('meta[name="description"]');
    if (current) {
      current.setAttribute('content', description.getAttribute('content') || '');
    }
  }
}

let resyncInFlight = null;

export async function resyncPageShellFromServer() {
  if (resyncInFlight) return resyncInFlight;

  resyncInFlight = (async () => {
    const response = await fetch(window.location.href, {
      credentials: 'same-origin',
      headers: { Accept: 'text/html' },
    });
    if (!response.ok) return null;

    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    applyPageShell(doc);
    return doc;
  })();

  try {
    return await resyncInFlight;
  } finally {
    resyncInFlight = null;
  }
}
