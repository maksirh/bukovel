export function initSliders() {
  document.querySelectorAll('[data-slider]').forEach(wrapper => {
    if (wrapper.dataset.sliderInit) return;
    wrapper.dataset.sliderInit = '1';
    initSlider(wrapper);
  });
}

function initSlider(wrapper) {
  const track = wrapper.querySelector('[data-slider-track]');
  const prevBtn = wrapper.querySelector('[data-slider-prev]');
  const nextBtn = wrapper.querySelector('[data-slider-next]');
  const counterEl = wrapper.querySelector('[data-slider-counter]');
  const dotsContainer = wrapper.querySelector('[data-slider-dots]');

  if (!track) return;

  const slides = track.querySelectorAll('[data-slider-slide]');
  if (!slides.length) return;

  const dotClass = wrapper.dataset.sliderDotClass || 'slider__dot';
  const dotActiveClass = `${dotClass}--active`;

  let current = 0;
  let dots = [];
  let scrollSyncTimer = null;

  if (dotsContainer) {
    const dotLabel = wrapper.dataset.sliderDotLabel || 'Slide';
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = dotClass;
      dot.setAttribute('aria-label', `${dotLabel} ${i + 1}`);
      dot.addEventListener('click', () => { current = i; scrollTo(current); });
      dotsContainer.appendChild(dot);
      dots.push(dot);
    });
  }

  function scrollTo(index) {
    track.scrollTo({ left: track.offsetWidth * index, behavior: 'smooth' });
    updateUI(index);
  }

  function updateUI(index) {
    if (counterEl) {
      counterEl.textContent = `${index + 1} / ${slides.length}`;
    }
    dots.forEach((dot, i) => {
      dot.classList.toggle(dotActiveClass, i === index);
    });
  }

  prevBtn?.addEventListener('click', () => {
    current = (current - 1 + slides.length) % slides.length;
    scrollTo(current);
  });

  nextBtn?.addEventListener('click', () => {
    current = (current + 1) % slides.length;
    scrollTo(current);
  });

  let startX = 0;
  track.addEventListener('touchstart', e => {
    startX = e.touches[0].clientX;
  }, { passive: true });

  track.addEventListener('touchend', e => {
    if (!e.changedTouches.length) return;
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      current = diff > 0
        ? (current + 1) % slides.length
        : (current - 1 + slides.length) % slides.length;
      scrollTo(current);
    }
  }, { passive: true });

  // Sync dots when user scrolls track natively (mouse drag, trackpad, keyboard)
  track.addEventListener('scroll', () => {
    clearTimeout(scrollSyncTimer);
    scrollSyncTimer = setTimeout(() => {
      const index = Math.round(track.scrollLeft / track.offsetWidth);
      if (index !== current && index >= 0 && index < slides.length) {
        current = index;
        updateUI(current);
      }
    }, 80);
  }, { passive: true });

  updateUI(current);
}
