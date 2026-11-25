/* CLEVARO — video.js: "Play" opens the intro video in a lightbox dialog. */
(function () {
  var modal = document.getElementById('vid-modal');
  var open = document.querySelector('[data-vid-open]');
  if (!modal || !open || typeof modal.showModal !== 'function') return;
  var video = modal.querySelector('video');
  var preview = document.querySelector('.vid__media');

  function lenis(fn) { var l = window.CLEVARO && CLEVARO.lenis; if (l) l[fn](); }

  open.addEventListener('click', function () {
    if (preview) preview.pause();
    video.currentTime = 0;
    modal.showModal();
    lenis('stop');
    var p = video.play(); if (p && p.catch) p.catch(function () {});
  });
  function close() { if (modal.open) modal.close(); }
  modal.querySelector('[data-vid-close]').addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });   // backdrop
  modal.addEventListener('close', function () {
    video.pause(); lenis('start');
    if (preview) { var p = preview.play(); if (p && p.catch) p.catch(function () {}); }
  });
})();
