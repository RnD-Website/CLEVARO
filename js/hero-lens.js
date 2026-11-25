/* Hero lens: a glass circle that eases after the mouse pointer and can also be grabbed and dragged.
   As soon as it moves (with the mouse or by dragging) the clean, un-overlaid photo shows inside the circle. */
(function () {
  var hero = document.querySelector('.hero');
  var lens = document.querySelector('.hero__shape');
  var clean = document.querySelector('.hero__clean');
  if (!hero || !lens || !clean) return;

  var inView = true, settled = false, revealed = false, dragging = false;
  var offX = 0, offY = 0;            // grab offset while dragging
  var px = null, py = null;          // last mouse position (viewport)
  var x = 0, y = 0;                  // lens top-left inside the hero

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { inView = e[0].isIntersecting; }, { threshold: 0 }).observe(hero);
  }

  function clamp(v, max) { return Math.max(0, Math.min(max, v)); }
  function bounds() { var h = hero.getBoundingClientRect(), s = lens.offsetWidth; return { h: h, s: s, mx: h.width - s, my: h.height - s }; }
  function put() { lens.style.left = x + 'px'; lens.style.top = y + 'px'; }

  // first interaction: stop the idle float and bake its offset into left/top
  function settle() {
    if (settled) return; settled = true;
    var h = hero.getBoundingClientRect(), r = lens.getBoundingClientRect();
    if (window.gsap) { gsap.killTweensOf(lens); gsap.set(lens, { x: 0, y: 0, scale: 1, opacity: 1 }); }
    x = r.left - h.left; y = r.top - h.top; put();
  }
  function reveal() {
    settle();
    if (revealed) return; revealed = true;
    lens.classList.add('is-dragged'); clean.classList.add('is-on');
  }

  function clip() {
    var h = hero.getBoundingClientRect(), r = lens.getBoundingClientRect(), rad = r.width / 2;
    clean.style.clipPath = 'circle(' + rad.toFixed(1) + 'px at ' + (r.left - h.left + rad).toFixed(1) + 'px ' + (r.top - h.top + rad).toFixed(1) + 'px)';
  }

  function frame() {
    if (inView) {
      if (settled && px !== null) {
        var b = bounds(), tx, ty;
        if (dragging) { tx = px - b.h.left - offX; ty = py - b.h.top - offY; }
        else { tx = px - b.h.left - b.s / 2; ty = py - b.h.top - b.s / 2; }
        tx = clamp(tx, b.mx); ty = clamp(ty, b.my);
        var k = dragging ? 0.6 : 0.11;           // snappy while dragging, soft glide while following
        x += (tx - x) * k; y += (ty - y) * k;
        if (Math.abs(tx - x) < 0.1) x = tx;
        if (Math.abs(ty - y) < 0.1) y = ty;
        put();
        lens.setAttribute('aria-valuenow', String(Math.round(((x + b.s / 2) / b.h.width) * 100)));
      }
      clip();
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  // follow the mouse (mouse only; touch just drags)
  window.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse' && !dragging) return;
    px = e.clientX; py = e.clientY;
    if (!settled && e.pointerType === 'mouse') {
      var h = hero.getBoundingClientRect();
      if (py >= h.top && py <= h.bottom && px >= h.left && px <= h.right) reveal();   // moving with the mouse shows the clean photo
    }
  });

  lens.addEventListener('pointerdown', function (e) {
    reveal();
    var h = hero.getBoundingClientRect();
    px = e.clientX; py = e.clientY;
    offX = e.clientX - h.left - x; offY = e.clientY - h.top - y;
    dragging = true; lens.classList.add('is-dragging');
    lens.setPointerCapture(e.pointerId); e.preventDefault();
  });
  function end(e) {
    if (!dragging) return;
    dragging = false; lens.classList.remove('is-dragging');
    try { lens.releasePointerCapture(e.pointerId); } catch (_) {}
    if (e.pointerType !== 'mouse') px = null;      // touch: stay where dropped
  }
  lens.addEventListener('pointerup', end);
  lens.addEventListener('pointercancel', end);

  lens.addEventListener('keydown', function (e) {
    var d = { ArrowLeft: [-24, 0], ArrowRight: [24, 0], ArrowUp: [0, -24], ArrowDown: [0, 24] }[e.key];
    if (!d) return;
    e.preventDefault(); reveal(); px = null;
    var b = bounds(); x = clamp(x + d[0], b.mx); y = clamp(y + d[1], b.my); put();
  });
  window.addEventListener('resize', function () { if (!settled) return; var b = bounds(); x = clamp(x, b.mx); y = clamp(y, b.my); put(); });
})();
