/* CLEVARO — slider.js
   Testimonial slider: autoplay, prev/next arrows and keyboard-safe controls. */
(function () {
  var root = document.querySelector('[data-slider]');
  if (!root) return;
  var track = root.querySelector('.slider__track');
  var slides = root.querySelectorAll('.slider__slide');
  var index = 0, timer;

  function go(i) {
    index = (i + slides.length) % slides.length;
    track.style.transform = 'translateX(' + (-index * 100) + '%)';
    slides.forEach(function (s, n) {
      s.setAttribute('aria-hidden', n === index ? 'false' : 'true');
      s.querySelectorAll('button').forEach(function (b) { b.tabIndex = n === index ? 0 : -1; });
    });
  }
  function start() {
    if (window.CLEVARO && CLEVARO.reduceMotion) return;
    stop();
    timer = setInterval(function () { go(index + 1); }, 6500);
  }
  function stop() { clearInterval(timer); }

  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-go],[data-prev],[data-next]');
    if (!b) return;
    if (b.hasAttribute('data-prev')) go(index - 1);
    else if (b.hasAttribute('data-next')) go(index + 1);
    else go(parseInt(b.dataset.go, 10));
    start();
  });
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);
  root.addEventListener('focusin', stop);
  root.addEventListener('focusout', start);

  go(0);
  start();
})();
