/* CLEVARO — smooth-scroll.js
   Lenis smooth scrolling, driven by the GSAP ticker so ScrollTrigger stays in sync. */
(function () {
  gsap.registerPlugin(ScrollTrigger);

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.CLEVARO = window.CLEVARO || {};
  CLEVARO.reduceMotion = reduce;

  if (reduce || typeof Lenis === 'undefined') return;

  var lenis = new Lenis({
    duration: 1.5,
    easing: function (t) { return 1 - Math.pow(1 - t, 3); },
    smoothWheel: true,
    syncTouch: false
  });
  CLEVARO.lenis = lenis;

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
  gsap.ticker.lagSmoothing(0);

  // in-page anchor links glide with Lenis
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href');
    if (id.length < 2) { if (id === '#') e.preventDefault(); return; }
    var target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    lenis.scrollTo(target, { offset: 0, duration: 1.6 });
    history.replaceState(null, '', id);
  });
})();
