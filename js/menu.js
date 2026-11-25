/* CLEVARO — menu.js
   Full-screen navigation overlay. Reveals with a clip-path wipe and staggers the links. */
(function () {
  /* sticky header: pin to the top, switch to a dark glass bar once the page has scrolled */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', (window.pageYOffset || document.documentElement.scrollTop) > 40); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var menu = document.getElementById('menu');
  if (!menu) return;
  var openBtn = document.querySelector('[data-menu-open]');
  var closeBtn = menu.querySelector('[data-menu-close]');
  var links = menu.querySelectorAll('.menu__link');
  var isOpen = false;
  var tl;

  function lock(state) {
    var l = window.CLEVARO && CLEVARO.lenis;
    if (l) state ? l.stop() : l.start();
    document.body.style.overflow = state ? 'hidden' : '';
  }

  function open() {
    if (isOpen) return;
    isOpen = true;
    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    openBtn.setAttribute('aria-expanded', 'true');
    lock(true);
    if (tl) tl.kill();
    tl = gsap.timeline({ onComplete: function () { closeBtn.focus(); } });
    tl.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 0.8, ease: 'power4.inOut' })
      .fromTo(links, { yPercent: 110 }, { yPercent: 0, duration: 0.9, ease: 'power4.out', stagger: 0.08 }, '-=0.35')
      .fromTo(menu.querySelectorAll('.menu__foot, .menu__top'), { opacity: 0 }, { opacity: 1, duration: 0.5 }, '-=0.6');
  }

  function close(after) {
    if (!isOpen) return;
    isOpen = false;
    openBtn.setAttribute('aria-expanded', 'false');
    if (tl) tl.kill();
    tl = gsap.timeline({
      onComplete: function () {
        menu.classList.remove('is-open');
        menu.setAttribute('aria-hidden', 'true');
        lock(false);
        if (typeof after === 'function') after(); else openBtn.focus();
      }
    });
    tl.to(links, { yPercent: -110, duration: 0.45, ease: 'power3.in', stagger: 0.04 })
      .to(menu, { clipPath: 'inset(100% 0 0 0)', duration: 0.7, ease: 'power4.inOut' }, '-=0.25');
  }

  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  menu.querySelectorAll('[data-menu-link]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.charAt(0) !== '#') return;            // real page link (about.html, index.html#plans…): let the browser navigate
      var target = id.length > 1 ? document.querySelector(id) : null;
      e.preventDefault();
      e.stopPropagation();
      close(function () {
        var l = window.CLEVARO && CLEVARO.lenis;
        if (id === '#top') { l ? l.scrollTo(0, { duration: 1.4 }) : window.scrollTo(0, 0); return; }
        if (target) { l ? l.scrollTo(target, { duration: 1.6 }) : target.scrollIntoView(); }
      });
    });
  });
})();
