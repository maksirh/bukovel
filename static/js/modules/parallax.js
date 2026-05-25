/**
 * Parallax backgrounds
 *
 * Usage: add data-parallax (and optionally data-parallax-speed="0.4") to any
 * element that contains a child with data-parallax-bg attribute.
 *
 * Works on iOS Safari via transform: translateY() — not background-attachment: fixed.
 * Automatically disabled when prefers-reduced-motion is set.
 */

let _rafId      = null;
let _fixedRafId = null;

export function initParallax() {
  if (_rafId !== null)      { cancelAnimationFrame(_rafId);      _rafId      = null; }
  if (_fixedRafId !== null) { cancelAnimationFrame(_fixedRafId); _fixedRafId = null; }

  document.querySelectorAll('.parallax-bg[data-bg]').forEach(el => {
    const url = el.dataset.bg;
    if (url) el.style.backgroundImage = `url("${url}")`;
  });

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // --- Fixed-position backgrounds: parallax relative to raw scrollY ---
  // Works correctly on iOS Safari — uses transform, not background-attachment:fixed.
  const fixedBgs = [...document.querySelectorAll('[data-parallax-fixed]')];
  if (fixedBgs.length) {
    let lastFixed = -1;

    function tickFixed() {
      const scrollY = window.scrollY;

      if (scrollY !== lastFixed) {
        lastFixed = scrollY;

        fixedBgs.forEach(bg => {
          const speed = parseFloat(bg.dataset.parallaxFixedSpeed ?? '0.15');
          bg.style.transform = `translateY(${(-scrollY * speed).toFixed(2)}px)`;
        });
      }

      _fixedRafId = requestAnimationFrame(tickFixed);
    }

    _fixedRafId = requestAnimationFrame(tickFixed);
  }

  // --- Section-relative parallax (absolute-positioned backgrounds) ---
  const sections = [...document.querySelectorAll('[data-parallax]')];
  if (!sections.length) return;

  let lastScroll = -1;

  function tick() {
    const scrollY = window.scrollY;

    if (scrollY !== lastScroll) {
      lastScroll = scrollY;

      sections.forEach(section => {
        const bg = section.querySelector('[data-parallax-bg]');
        if (!bg) return;

        const rect = section.getBoundingClientRect();
        if (rect.bottom < -200 || rect.top > window.innerHeight + 200) return;

        const speed = parseFloat(section.dataset.parallaxSpeed ?? '0.3');
        const sectionMid = rect.top + rect.height / 2;
        const viewportMid = window.innerHeight / 2;
        const offset = (sectionMid - viewportMid) * speed;

        bg.style.transform = `translateY(${offset.toFixed(2)}px)`;
      });
    }

    _rafId = requestAnimationFrame(tick);
  }

  _rafId = requestAnimationFrame(tick);
}
