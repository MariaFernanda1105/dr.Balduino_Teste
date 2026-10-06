document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
    window.setTimeout(function () {
      if (alert && alert.parentNode) alert.remove();
    }, 6000);
  });

  const mainNav = document.getElementById('mainNav');
  const syncNavState = function () {
    if (mainNav) mainNav.classList.toggle('is-scrolled', window.scrollY > 12);
  };
  syncNavState();
  window.addEventListener('scroll', syncNavState, { passive: true });

  const navCollapse = document.getElementById('navbarNav');
  document.querySelectorAll('#navbarNav .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      if (navCollapse && navCollapse.classList.contains('show') && window.bootstrap) {
        const collapse = window.bootstrap.Collapse.getOrCreateInstance(navCollapse);
        collapse.hide();
      }
    });
  });

  const heroCarousel = document.getElementById('heroCarousel');
  const respectsReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (heroCarousel && window.bootstrap && !respectsReducedMotion) {
    const interval = Number(heroCarousel.dataset.autoplay) || 7000;
    const carousel = window.bootstrap.Carousel.getOrCreateInstance(heroCarousel, {
      interval: false,
      pause: false,
      touch: true,
      wrap: true
    });
    let autoplayTimer;
    let paused = false;

    const scheduleNext = function () {
      window.clearTimeout(autoplayTimer);
      if (paused || document.hidden) return;
      autoplayTimer = window.setTimeout(function () {
        carousel.next();
        scheduleNext();
      }, interval);
    };
    const pauseAutoplay = function () {
      paused = true;
      window.clearTimeout(autoplayTimer);
    };
    const resumeAutoplay = function () {
      paused = false;
      scheduleNext();
    };

    heroCarousel.addEventListener('mouseenter', pauseAutoplay);
    heroCarousel.addEventListener('mouseleave', resumeAutoplay);
    heroCarousel.addEventListener('focusin', pauseAutoplay);
    heroCarousel.addEventListener('focusout', function (event) {
      if (!heroCarousel.contains(event.relatedTarget)) resumeAutoplay();
    });
    heroCarousel.querySelectorAll('[data-bs-slide], [data-bs-slide-to]').forEach(function (control) {
      control.addEventListener('click', function () {
        window.setTimeout(scheduleNext, 250);
      });
    });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) window.clearTimeout(autoplayTimer);
      else scheduleNext();
    });
    scheduleNext();
  }
});
