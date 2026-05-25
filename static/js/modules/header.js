let _abortCtrl = null;

export function initHeader() {
  if (_abortCtrl) _abortCtrl.abort();
  _abortCtrl = new AbortController();

  const header = document.getElementById('site-header');
  if (!header) return;

  const SCROLL_THRESHOLD = 1;
  const isHeroPage = document.body.classList.contains('has-hero');

  function onScroll() {
    const scrolled = window.scrollY > SCROLL_THRESHOLD;
    header.classList.toggle('is-scrolled', scrolled);

    if (isHeroPage) {
      header.classList.toggle('header--solid', scrolled);
    }
  }

  window.addEventListener('scroll', onScroll, {
    passive: true,
    signal: _abortCtrl.signal,
  });

  onScroll();
}
