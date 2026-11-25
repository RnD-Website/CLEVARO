/* CLEVARO — inner.js
   Entrance + scroll motion for the inner pages (about.html, services.html).
   Mirrors the homepage choreography: masked split-text, guide lines, parallax, staggered reveals. */
(function () {
  var reduce = window.CLEVARO && CLEVARO.reduceMotion;
  var splitEls = document.querySelectorAll('[data-split]');
  function showAll() { splitEls.forEach(function (el) { el.classList.add('is-split'); }); }

  /* newsletter (client-side confirmation only) — works with or without motion */
  var nl = document.querySelector('[data-newsletter]');
  if (nl) {
    nl.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = nl.querySelector('input');
      var msg = document.querySelector('.newsletter__msg');
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
      msg.textContent = ok ? 'Thanks — you’re on the list.' : 'Please enter a valid email address.';
      if (ok) nl.reset();
    });
  }

  /* services: highlight the sub-nav chip for the section in view */
  var chips = [].slice.call(document.querySelectorAll('.subnav a'));
  if (chips.length && 'IntersectionObserver' in window) {
    var map = {};
    chips.forEach(function (a) { var t = document.querySelector(a.getAttribute('href')); if (t) map[a.getAttribute('href')] = t; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        chips.forEach(function (a) { a.classList.toggle('is-active', map[a.getAttribute('href')] === en.target); });
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    Object.keys(map).forEach(function (k) { io.observe(map[k]); });
  }

  if (reduce || typeof gsap === 'undefined' || typeof SplitText === 'undefined') { showAll(); return; }

  gsap.registerPlugin(ScrollTrigger, SplitText);
  gsap.defaults({ ease: 'power3.out' });
  var q = function (s, c) { return (c || document).querySelector(s); };
  var qa = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };

  function splitReveal(el, kind, opts) {
    opts = opts || {};
    var type = kind === 'lines' ? 'lines,words' : 'words';
    return SplitText.create(el, {
      type: type, mask: kind === 'lines' ? 'lines' : 'words', autoSplit: true,
      wordsClass: 'gsap_split_word', linesClass: 'gsap_split_line',
      onSplit: function (self) {
        el.classList.add('is-split');
        var vars = { yPercent: 140, duration: 1.1, ease: 'expo.out', stagger: kind === 'lines' ? 0.12 : 0.07, delay: opts.delay || 0 };
        if (!opts.now) vars.scrollTrigger = { trigger: el, start: 'top 88%', once: true };
        return gsap.from(kind === 'lines' ? self.lines : self.words, vars);
      }
    });
  }

  /* guide lines */
  qa('.section-lines').forEach(function (wrap) {
    gsap.from(qa('span', wrap), {
      scaleY: 0, transformOrigin: 'top center', duration: 1.6, ease: 'expo.out', stagger: 0.12,
      scrollTrigger: { trigger: wrap.parentElement, start: 'top 85%', once: true }
    });
  });

  /* header + page hero */
  gsap.from('[data-anim="header"]', { y: -30, opacity: 0, duration: 1.2, delay: 0.3 });
  gsap.fromTo('.phero__bg', { scale: 1.2 }, { scale: 1, duration: 2.4, ease: 'expo.out' });
  gsap.to('.phero__bg', { yPercent: 9, ease: 'none', scrollTrigger: { trigger: '.phero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.from('.crumbs', { y: 20, opacity: 0, duration: 1, delay: 0.5 });
  var title = q('.phero__title');
  if (title) splitReveal(title, 'lines', { now: true, delay: 0.4 });
  gsap.from('.phero__side > *', { y: 40, opacity: 0, duration: 1.1, stagger: 0.12, delay: 0.9 });
  gsap.from('.subnav', { y: 30, opacity: 0, duration: 1, delay: 1.3 });

  /* split headings */
  splitEls.forEach(function (el) {
    if (el.closest('.phero')) return;
    splitReveal(el, el.getAttribute('data-split'));
  });

  /* eyebrows + generic fade-up blocks */
  qa('.pg-head .eyebrow').forEach(function (el) {
    gsap.from(el, { y: 20, opacity: 0, duration: 1, scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });
  qa('[data-r]').forEach(function (el) {
    gsap.from(el, { y: 50, opacity: 0, duration: 1.2, scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });
  // staggered groups
  qa('[data-r-group]').forEach(function (group) {
    gsap.from(group.children, {
      y: 70, opacity: 0, duration: 1.2, stagger: 0.12,
      scrollTrigger: { trigger: group, start: 'top 85%', once: true }
    });
  });

  /* image reveals: clip-path wipe + slow zoom, like the homepage about section */
  qa('[data-r-img]').forEach(function (wrap) {
    var img = q('img', wrap);
    var tl = gsap.timeline({ scrollTrigger: { trigger: wrap, start: 'top 88%', once: true } });
    tl.fromTo(wrap, { clipPath: 'inset(100% 0 0 0 round 24px)' }, { clipPath: 'inset(0% 0 0 0 round 24px)', duration: 1.5, ease: 'expo.out' })
      .fromTo(img, { scale: 1.3 }, { scale: 1, duration: 1.8, ease: 'expo.out' }, 0);
  });

  /* counting stats */
  qa('[data-count]').forEach(function (el) {
    var end = parseFloat(el.getAttribute('data-count'));
    var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
    var suffix = el.getAttribute('data-suffix') || '';
    var o = { v: 0 };
    gsap.to(o, {
      v: end, duration: 2, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onUpdate: function () { el.textContent = o.v.toFixed(dec) + suffix; }
    });
  });

  /* quote + band parallax */
  qa('.quote__wrap, .band__wrap').forEach(function (w) {
    gsap.from(w, { clipPath: 'inset(8% 5% round 40px)', duration: 1.6, ease: 'expo.out', scrollTrigger: { trigger: w, start: 'top 88%', once: true } });
  });

  /* footer */
  gsap.fromTo('.footer__bg', { yPercent: -8 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'bottom bottom', scrub: true } });
  gsap.from('.footer__cta .btn-wrap', { y: 40, opacity: 0, duration: 1.1, scrollTrigger: { trigger: '.footer__cta', start: 'top 75%', once: true } });
  gsap.from('[data-footer-card]', { y: 120, opacity: 0, duration: 1.5, scrollTrigger: { trigger: '[data-footer-card]', start: 'top 95%', once: true } });
  gsap.from('.footer__col', { y: 30, opacity: 0, duration: 1, stagger: 0.1, scrollTrigger: { trigger: '[data-footer-card]', start: 'top 80%', once: true } });

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  setTimeout(showAll, 3500);
})();
