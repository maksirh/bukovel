import { lockScroll, unlockScroll } from './scroll-lock.js';

export function initModal() {
  const root = document.getElementById('modal-root');
  if (!root) return;

  const modal = root.querySelector('.modal');
  if (!modal) return;

  if (modal.dataset.modalInit) return;
  modal.dataset.modalInit = '1';

  function closeModal() {
    modal.classList.remove('is-open');
    unlockScroll();
    setTimeout(() => { root.innerHTML = ''; }, 300);
  }

  modal.querySelector('[data-modal-close]')?.addEventListener('click', closeModal);
  modal.querySelector('.modal__overlay')?.addEventListener('click', closeModal);

  document.addEventListener('keydown', function onKey(e) {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
      document.removeEventListener('keydown', onKey);
    }
  });

  lockScroll();

  const firstFocusable = modal.querySelector('button, input, select, textarea, [href], [tabindex]:not([tabindex="-1"])');
  firstFocusable?.focus();
}
