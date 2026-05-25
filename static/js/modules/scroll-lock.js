let _scrollY = 0;

export function lockScroll() {
  _scrollY = window.scrollY;
  document.documentElement.style.setProperty('--scroll-y', `${_scrollY}px`);
  document.body.classList.add('modal-open');
}

export function unlockScroll() {
  document.body.classList.remove('modal-open');
  document.documentElement.style.removeProperty('--scroll-y');
  window.scrollTo({ top: _scrollY, behavior: 'instant' });
}
