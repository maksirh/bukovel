import { lockScroll, unlockScroll } from './scroll-lock.js';

export function initLightbox() {
  document.querySelectorAll('[data-lightbox]').forEach(el => {
    if (el.dataset.lightboxInit) return;
    el.dataset.lightboxInit = '1';
    el.style.cursor = 'zoom-in';

    el.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopImmediatePropagation(); // prevent any other handler (incl. HTMX boost) on this element
      const group = el.dataset.lightboxGroup;
      if (group) {
        const all = [...document.querySelectorAll(
          `[data-lightbox][data-lightbox-group="${group}"]`
        )];
        openLightboxGallery(all, all.indexOf(el));
      } else {
        openLightboxGallery([el], 0);
      }
    });
  });
}

function getMediaData(el) {
  if (el.tagName === 'A') {
    const img = el.querySelector('img');
    return {
      src: el.href,
      alt: img?.alt || el.getAttribute('aria-label') || '',
    };
  }
  return { src: el.src, alt: el.alt || '' };
}

function getI18n() {
  const d = document.body.dataset;
  return {
    close: d.i18nClose || 'Close',
    prev:  d.i18nPrev  || 'Previous photo',
    next:  d.i18nNext  || 'Next photo',
    view:  d.i18nView  || 'View photo',
  };
}

function openLightboxGallery(elements, startIndex) {
  let current = startIndex;
  const total = elements.length;
  const hasNav = total > 1;
  const i18n = getI18n();

  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');

  // Buttons are direct children of .lightbox — outside content's stacking context
  lb.innerHTML = `
    <div class="lightbox__overlay"></div>
    <div class="lightbox__content">
      <img src="" alt="" class="lightbox__img">
    </div>
    <button class="lightbox__close" aria-label="${i18n.close}">&times;</button>
    ${hasNav ? `
      <button class="lightbox__prev" aria-label="${i18n.prev}">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <button class="lightbox__next" aria-label="${i18n.next}">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </button>
      <div class="lightbox__counter" aria-live="polite" aria-atomic="true"></div>
    ` : ''}
  `;

  document.body.appendChild(lb);
  lockScroll();

  const imgEl     = lb.querySelector('.lightbox__img');
  const counterEl = lb.querySelector('.lightbox__counter');
  const prevBtn   = lb.querySelector('.lightbox__prev');
  const nextBtn   = lb.querySelector('.lightbox__next');

  function revealImg() {
    imgEl.classList.add('is-loaded');
  }

  imgEl.addEventListener('load', revealImg);

  function show(index) {
    current = ((index % total) + total) % total;
    const { src, alt } = getMediaData(elements[current]);

    imgEl.classList.remove('is-loaded');
    imgEl.src = src;
    imgEl.alt = alt;
    lb.setAttribute('aria-label', alt || i18n.view);
    if (counterEl) counterEl.textContent = `${current + 1} / ${total}`;

    // Fallback: cached images don't always fire load event
    if (imgEl.complete && imgEl.naturalWidth > 0) {
      revealImg();
    }
  }

  show(current);
  requestAnimationFrame(() => lb.classList.add('is-open'));

  function close() {
    lb.classList.remove('is-open');
    unlockScroll();
    document.removeEventListener('keydown', onKeydown);
    setTimeout(() => lb.remove(), 300);
  }

  function onKeydown(e) {
    if (e.key === 'Escape')     close();
    if (e.key === 'ArrowRight') hasNav && show(current + 1);
    if (e.key === 'ArrowLeft')  hasNav && show(current - 1);
  }

  lb.querySelector('.lightbox__overlay').addEventListener('click', close);
  lb.querySelector('.lightbox__close').addEventListener('click', close);
  prevBtn?.addEventListener('click', () => show(current - 1));
  nextBtn?.addEventListener('click', () => show(current + 1));
  document.addEventListener('keydown', onKeydown);

  let touchStartX = 0;
  lb.addEventListener('touchstart', e => {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });
  lb.addEventListener('touchend', e => {
    if (!e.changedTouches.length) return;
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (hasNav && Math.abs(diff) > 50) {
      show(diff > 0 ? current + 1 : current - 1);
    }
  }, { passive: true });
}
