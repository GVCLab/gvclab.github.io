document.addEventListener('DOMContentLoaded', function () {
  var carousel = document.querySelector('[data-project-carousel]');
  if (!carousel) return;
  var slides = Array.prototype.slice.call(carousel.querySelectorAll('[data-project-slide]'));
  var dots = Array.prototype.slice.call(carousel.querySelectorAll('[data-project-dot]'));
  var previous = carousel.querySelector('[data-project-prev]');
  var next = carousel.querySelector('[data-project-next]');
  var pause = carousel.querySelector('[data-project-pause]');
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var current = 0;
  var timer;
  var hovered = false;
  var focused = false;
  var paused = motion.matches;
  if (paused) { carousel.classList.add('is-paused'); pause.textContent = 'Play'; pause.setAttribute('aria-label', 'Play automatic slideshow'); }

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach(function (slide, i) { slide.hidden = i !== current; });
    dots.forEach(function (dot, i) { dot.setAttribute('aria-current', i === current ? 'true' : 'false'); });
  }
  function stop() { window.clearInterval(timer); timer = null; }
  function start() {
    stop();
    if (slides.length > 1 && !paused && !hovered && !focused && !document.hidden) {
      timer = window.setInterval(function () { show(current + 1); }, 6000);
    }
  }
  previous.addEventListener('click', function () { show(current - 1); start(); });
  next.addEventListener('click', function () { show(current + 1); start(); });
  pause.addEventListener('click', function () {
    paused = !paused;
    carousel.classList.toggle('is-paused', paused);
    pause.textContent = paused ? 'Play' : 'Pause';
    pause.setAttribute('aria-label', paused ? 'Play automatic slideshow' : 'Pause automatic slideshow');
    start();
  });
  dots.forEach(function (dot, index) { dot.addEventListener('click', function () { show(index); start(); }); });
  carousel.addEventListener('mouseenter', function () { hovered = true; stop(); });
  carousel.addEventListener('mouseleave', function () { hovered = false; start(); });
  carousel.addEventListener('focusin', function () { focused = true; stop(); });
  carousel.addEventListener('focusout', function (event) {
    if (!carousel.contains(event.relatedTarget)) { focused = false; start(); }
  });
  document.addEventListener('visibilitychange', start);
  if (motion.addEventListener) motion.addEventListener('change', function () {
    if (motion.matches) { paused = true; carousel.classList.add('is-paused'); pause.textContent = 'Play'; pause.setAttribute('aria-label', 'Play automatic slideshow'); }
    start();
  });
  show(0);
  start();
});
