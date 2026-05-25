import { lockScroll, unlockScroll } from './scroll-lock.js';

let _abortCtrl = null;

export function initMobileNav() {
  if (_abortCtrl) _abortCtrl.abort();
  _abortCtrl = new AbortController();
  const { signal } = _abortCtrl;

  const burgerBtn = document.getElementById('burger-btn');
  const mobileNav = document.getElementById('mobile-nav');
  const closeBtn = document.getElementById('mobile-nav-close');
  const overlay = document.getElementById('mobile-nav-overlay');

  if (!burgerBtn || !mobileNav) return;

  function openNav() {
    mobileNav.classList.add('is-open');
    mobileNav.setAttribute('aria-hidden', 'false');
    burgerBtn.classList.add('is-active');
    burgerBtn.setAttribute('aria-expanded', 'true');
    lockScroll();
    closeBtn?.focus();
  }

  function closeNav() {
    mobileNav.classList.remove('is-open');
    mobileNav.setAttribute('aria-hidden', 'true');
    burgerBtn.classList.remove('is-active');
    burgerBtn.setAttribute('aria-expanded', 'false');
    unlockScroll();
  }

  burgerBtn.addEventListener('click', openNav, { signal });
  closeBtn?.addEventListener('click', closeNav, { signal });
  overlay?.addEventListener('click', closeNav, { signal });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && mobileNav.classList.contains('is-open')) {
      closeNav();
    }
  }, { signal });

  mobileNav.querySelectorAll('.mobile-nav__link, .mobile-nav__cta').forEach(link => {
    link.addEventListener('click', closeNav, { signal });
  });
}
