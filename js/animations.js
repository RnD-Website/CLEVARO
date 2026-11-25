/* CLEVARO — animations.js
   Entrance + scroll choreography (GSAP, ScrollTrigger, SplitText).
   Sections, in page order: header → hero → video → about → services → how it works →
   call to action → categories → gallery → testimonials → blog → footer. */
(function () {
  var reduce = window.CLEVARO && CLEVARO.reduceMotion;
  var splitEls = document.querySelectorAll('[data-split]');

  function showAll() { splitEls.forEach(function (el) { el.classList.add('is-split'); }); }
  if (reduce || typeof gsap === 'undefined' || typeof SplitText === 'undefined') { showAll(); return; }

  gsap.registerPlugin(ScrollTrigger, SplitText);
  gsap.defaults({ ease: 'power3.out' });

  var q = function (s, c) { return (c || document).querySelector(s); };
  var qa = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- text reveals ---------- */
  // kind: 'words' | 'lines' | 'chars'. Re-splits automatically on resize.
  function splitReveal(el, kind, opts) {
    opts = opts || {};
    var type = kind === 'lines' ? 'lines,words' : kind === 'chars' ? 'words,chars' : 'words';
    return SplitText.create(el, {
      type: type,
      mask: kind === 'lines' ? 'lines' : 'words',
      autoSplit: true,
      wordsClass: 'gsap_split_word',
      linesClass: 'gsap_split_line',
      charsClass: 'gsap_split_char',
      onSplit: function (self) {
        el.classList.add('is-split');
        var targets = kind === 'lines' ? self.lines : kind === 'chars' ? self.chars : self.words;
        var vars = {
          yPercent: 140,
          duration: kind === 'chars' ? 0.9 : 1.1,
          ease: 'expo.out',
          stagger: kind === 'chars' ? 0.018 : kind === 'lines' ? 0.12 : 0.07,
          delay: opts.delay || 0
        };
        if (!opts.now) {
          vars.scrollTrigger = { trigger: el, start: 'top 88%', once: true };
        }
        return gsap.from(targets, vars);
      }
    });
  }

  /* ---------- 0. section guide lines ---------- */
  qa('.section-lines').forEach(function (wrap) {
    var inHero = !!wrap.closest('.hero');
    gsap.from(qa('span', wrap), {
      scaleY: 0,
      transformOrigin: 'top center',
      duration: 1.6,
      ease: 'expo.out',
      stagger: 0.12,
      delay: inHero ? 0.2 : 0,
      scrollTrigger: inHero ? null : { trigger: wrap.parentElement, start: 'top 85%', once: true }
    });
  });

  /* ---------- 1. header + hero intro ---------- */
  var header = q('[data-anim="header"]');
  gsap.from(header, { y: -30, opacity: 0, duration: 1.2, delay: 0.3 });

  gsap.fromTo('.hero__bg', { scale: 1.2 }, { scale: 1, duration: 2.4, ease: 'expo.out' });

  var heroTop = q('.hero__top-text');
  if (heroTop) splitReveal(heroTop, 'words', { now: true, delay: 0.5 });
  var heroTitle = q('.hero__title');
  if (heroTitle) splitReveal(heroTitle, 'lines', { now: true, delay: 0.35 });

  gsap.from('[data-anim="hero-btn"]', { y: 40, opacity: 0, duration: 1.1, delay: 1.0 });
  gsap.from('[data-anim="hero-card"]', { y: 80, opacity: 0, duration: 1.3, delay: 1.1 });
  gsap.from('[data-anim="shape"]', { scale: 0.4, opacity: 0, duration: 1.8, delay: 0.6, ease: 'expo.out' });
  gsap.to('[data-anim="shape"]', { y: 24, x: -12, duration: 4.2, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 2 });

  // hero background parallax
  gsap.to('.hero__bg', {
    yPercent: 9, ease: 'none',
    scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
  });
  // hero content drifts up slightly as it leaves
  gsap.to('.hero__row', {
    yPercent: -6, opacity: 0.2, ease: 'none',
    scrollTrigger: { trigger: '.hero', start: 'center top', end: 'bottom top', scrub: true }
  });

  /* ---------- generic reveals ---------- */
  // headings that live inside .section-head: eyebrow slides in
  qa('[data-reveal="head"] .eyebrow').forEach(function (el) {
    gsap.from(el, { y: 20, opacity: 0, duration: 1, scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });

  // split headings
  qa('[data-split]').forEach(function (el) {
    if (el.closest('.hero')) return;
    splitReveal(el, el.getAttribute('data-split'));
  });

  /* ---------- 1b. video: pill grows to full container width ---------- */
  var vidStage = q('[data-vid-stage]');
  if (vidStage) {
    var small = window.innerWidth < 768;
    var from = small ? 'inset(16% 7% 16% 7% round 160px)' : 'inset(15% 19% 15% 19% round 260px)';
    gsap.fromTo(vidStage, { clipPath: from }, {
      clipPath: 'inset(0% 0% 0% 0% round 24px)', ease: 'none',
      scrollTrigger: { trigger: vidStage, start: 'top 88%', end: 'top 18%', scrub: 0.6, invalidateOnRefresh: true }
    });
    gsap.fromTo('.vid__media', { scale: 1.3 }, {
      scale: 1, ease: 'none',
      scrollTrigger: { trigger: vidStage, start: 'top 88%', end: 'top 18%', scrub: 0.6 }
    });
    gsap.from('.vid__play, .vid__caption', { opacity: 0, y: 20, duration: 1, stagger: 0.1, scrollTrigger: { trigger: vidStage, start: 'top 85%', once: true } });
  }

  /* ---------- 2. about ---------- */
  qa('[data-reveal="image"]').forEach(function (wrap) {
    var img = q('img', wrap);
    var tl = gsap.timeline({ scrollTrigger: { trigger: wrap, start: 'top 88%', once: true } });
    tl.fromTo(wrap, { clipPath: 'inset(100% 0 0 0 round 24px)', y: 100 }, { clipPath: 'inset(0% 0 0 0 round 24px)', y: 0, duration: 1.5, ease: 'expo.out' })
      .fromTo(img, { scale: 1.3 }, { scale: 1, duration: 1.8, ease: 'expo.out' }, 0);
    gsap.to(img, { yPercent: -6, ease: 'none', scrollTrigger: { trigger: wrap, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  qa('[data-reveal="stack"]').forEach(function (stack) {
    gsap.from(stack.children, {
      y: 50, opacity: 0, duration: 1.2, stagger: 0.14, delay: 0.15,
      scrollTrigger: { trigger: stack, start: 'top 85%', once: true }
    });
  });

  /* ---------- 3. services: stacked sticky cards ----------
     Each card pins just below the header and the next one slides up over it, one by one.
     No fades or darkening: the covered card only eases back slightly so the stack reads as layers. */
  var mm = gsap.matchMedia();
  mm.add('(min-width: 768px)', function () {
    var items = qa('.service__item');
    items.forEach(function (item, i) {
      item.style.top = (100 + i * 18) + 'px';           // each pinned card peeks out a little above the next
      var card = q('.service__card', item);
      var next = items[i + 1];
      if (!next) return;
      gsap.to(card, {
        scale: 0.94, ease: 'none',
        scrollTrigger: { trigger: next, start: 'top 85%', end: 'top ' + (100 + (i + 1) * 18) + 'px', scrub: true }
      });
    });
    return function () { items.forEach(function (item) { item.style.top = ''; }); };
  });

  /* ---------- 4. how it works ---------- */
  var cards = qa('.work__card');
  mm.add('(min-width: 992px)', function () {
    var tl = gsap.timeline({
      defaults: { ease: 'power2.out' },
      scrollTrigger: { trigger: '.work__wrap', start: 'top 60%', end: 'bottom-=520 bottom', scrub: 1 }
    });
    gsap.set(cards, { y: window.innerHeight * 1.1, opacity: 0 });
    cards.forEach(function (card, i) {
      tl.to(card, { y: 0, opacity: 1, duration: 1, ease: 'power3.out' }, i * 0.55);
    });
    tl.to({}, { duration: 0.6 });
    return function () { gsap.set(cards, { clearProps: 'transform,opacity' }); };
  });
  mm.add('(max-width: 991px)', function () {
    cards.forEach(function (card) {
      gsap.from(card, { y: 60, opacity: 0, duration: 1.1, scrollTrigger: { trigger: card, start: 'top 90%', once: true } });
    });
  });

  /* ---------- 5. call to action ---------- */
  qa('[data-parallax="cta"]').forEach(function (bg) {
    gsap.fromTo(bg, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: '.cta__wrap', start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  gsap.from('.cta__wrap', {
    clipPath: 'inset(8% 6% round 40px)', duration: 1.6, ease: 'expo.out',
    scrollTrigger: { trigger: '.cta__wrap', start: 'top 85%', once: true }
  });
  var ctaCards = qa('[data-reveal="card"]');
  gsap.from(ctaCards, {
    y: 70, opacity: 0, duration: 1.2, stagger: 0.15,
    scrollTrigger: { trigger: '.cta__row', start: 'top 80%', once: true }
  });
  var wordmark = q('[data-anim="wordmark"]');
  if (wordmark) {
    gsap.from(wordmark, {
      clipPath: 'inset(0 100% 0 0)', x: -60, opacity: 0, duration: 2, ease: 'expo.out',
      scrollTrigger: { trigger: '.cta__row', start: 'top 70%', once: true }
    });
  }

  /* ---------- 6. categories ---------- */
  var cats = qa('[data-reveal="cat"]');
  gsap.set(cats, { opacity: 0, y: 90, scale: 0.96 });
  ScrollTrigger.batch(cats, {
    start: 'top 90%', once: true,
    onEnter: function (batch) { gsap.to(batch, { opacity: 1, y: 0, scale: 1, duration: 1.3, stagger: 0.14, overwrite: true }); }
  });

  /* ---------- 6b. gallery ---------- */
  var galCols = qa('[data-reveal="gal-col"]');
  if (galCols.length) {
    gsap.set(galCols, { opacity: 0, y: 110 });
    ScrollTrigger.create({
      trigger: '.gallery__grid', start: 'top 85%', once: true,
      onEnter: function () { gsap.to(galCols, { opacity: 1, y: 0, duration: 1.5, stagger: 0.12, ease: 'power3.out' }); }
    });
    // endless auto-scroll: duplicate each track once, slide it by exactly one set, repeat.
    // Neighbouring columns run in opposite directions at slightly different speeds.
    galCols.forEach(function (col, i) {
      var track = q('.gallery__track', col);
      Array.prototype.slice.call(track.children).forEach(function (li) {
        var clone = li.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        track.appendChild(clone);
      });
      var up = i % 2 === 0;
      var tween = gsap.fromTo(track, { yPercent: up ? 0 : -50 }, {
        yPercent: up ? -50 : 0, duration: 72 + i * 6, ease: 'none', repeat: -1, paused: true
      });
      ScrollTrigger.create({
        trigger: col, start: 'top bottom', end: 'bottom top',
        onToggle: function (self) { self.isActive ? tween.play() : tween.pause(); }
      });
      col.addEventListener('mouseenter', function () { gsap.to(tween, { timeScale: 0.25, duration: 0.6 }); });
      col.addEventListener('mouseleave', function () { gsap.to(tween, { timeScale: 1, duration: 0.6 }); });
    });
  }

  /* ---------- 7. testimonials ---------- */
  qa('[data-float]').forEach(function (leaf, i) {
    gsap.to(leaf, { y: i ? -18 : 26, rotation: i ? -8 : 7, duration: 3.6 + i, ease: 'sine.inOut', yoyo: true, repeat: -1 });
    gsap.from(leaf, { opacity: 0, scale: 0.6, duration: 1.8, scrollTrigger: { trigger: leaf.parentElement, start: 'top 75%', once: true } });
  });
  gsap.from('.slider', { y: 70, opacity: 0, duration: 1.3, scrollTrigger: { trigger: '.slider', start: 'top 85%', once: true } });

  /* ---------- 8. blog ---------- */
  var posts = qa('[data-reveal="post"]');
  gsap.set(posts, { opacity: 0, y: 90 });
  ScrollTrigger.batch(posts, {
    start: 'top 90%', once: true,
    onEnter: function (batch) { gsap.to(batch, { opacity: 1, y: 0, duration: 1.3, stagger: 0.16, overwrite: true }); }
  });

  /* ---------- 9. footer ---------- */
  gsap.fromTo('.footer__bg', { yPercent: -8 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'bottom bottom', scrub: true } });
  gsap.from('.footer__cta .btn-wrap', { y: 40, opacity: 0, duration: 1.1, scrollTrigger: { trigger: '.footer__cta', start: 'top 75%', once: true } });
  gsap.from('[data-footer-card]', { y: 120, opacity: 0, duration: 1.5, scrollTrigger: { trigger: '[data-footer-card]', start: 'top 95%', once: true } });
  gsap.from('.footer__col', { y: 30, opacity: 0, duration: 1, stagger: 0.1, scrollTrigger: { trigger: '[data-footer-card]', start: 'top 80%', once: true } });

  /* ---------- newsletter (client-side confirmation only) ---------- */
  var form = q('[data-newsletter]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = q('input', form);
      var msg = q('.newsletter__msg');
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
      msg.textContent = ok ? 'Thanks — you’re on the list.' : 'Please enter a valid email address.';
      if (ok) form.reset();
    });
  }

  /* ---------- keep trigger positions right ---------- */
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });

  // safety net: never leave headings hidden
  setTimeout(showAll, 3500);
})();
