/* CLEVARO — extra.js
   Small interactions for the blog, article, FAQ, pricing and contact pages.
   Everything here is progressive enhancement and fails safe: with JS off the content is still all there. */
(function () {
  var qa = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var q = function (s, c) { return (c || document).querySelector(s); };

  /* ---------- blog: topic filter ---------- */
  var grid = q('[data-blog-grid]');
  if (grid) {
    var btns = qa('[data-filter]');
    var empty = q('[data-blog-empty]');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter'), shown = 0;
        btns.forEach(function (x) { var on = x === b; x.classList.toggle('is-active', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        qa('.bcard', grid).forEach(function (c) {
          var ok = f === 'all' || c.getAttribute('data-cat') === f;
          c.hidden = !ok; if (ok) shown++;
        });
        if (empty) empty.hidden = shown > 0;
        if (window.ScrollTrigger) setTimeout(function () { ScrollTrigger.refresh(); }, 50);
      });
    });
  }

  /* ---------- article: share + copy link + contents highlight ---------- */
  var share = qa('[data-share]');
  if (share.length) {
    var url = encodeURIComponent(location.href), title = encodeURIComponent(document.title);
    var map = {
      facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + url,
      x: 'https://twitter.com/intent/tweet?url=' + url + '&text=' + title,
      pinterest: 'https://pinterest.com/pin/create/button/?url=' + url + '&description=' + title
    };
    share.forEach(function (a) { a.href = map[a.getAttribute('data-share')]; a.target = '_blank'; a.rel = 'noopener'; });
  }
  var copy = q('[data-copy-link]');
  if (copy) {
    copy.addEventListener('click', function () {
      var done = function () { var t = copy.textContent; copy.textContent = 'Link copied'; setTimeout(function () { copy.textContent = t; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(location.href).then(done, done); else done();
    });
  }
  var toc = qa('.art__toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var tmap = {};
    toc.forEach(function (a) { var t = q(a.getAttribute('href')); if (t) tmap[a.getAttribute('href')] = t; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        toc.forEach(function (a) { a.classList.toggle('is-active', tmap[a.getAttribute('href')] === en.target); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(tmap).forEach(function (k) { io.observe(tmap[k]); });
  }

  /* ---------- FAQ: live search ---------- */
  var search = q('[data-faq-search]');
  if (search) {
    var groups = qa('[data-faq-group]');
    var count = q('[data-faq-count]');
    var none = q('[data-faq-empty]');
    var base = new Map();
    qa('.qa').forEach(function (d) { base.set(d, d.hasAttribute('open')); });
    var run = function () {
      var term = search.value.trim().toLowerCase(), total = 0;
      groups.forEach(function (g) {
        var hits = 0;
        qa('.qa', g).forEach(function (d) {
          var ok = !term || d.textContent.toLowerCase().indexOf(term) > -1;
          d.hidden = !ok;
          if (ok) { hits++; if (term) d.open = true; else d.open = base.get(d); }
        });
        g.hidden = hits === 0; total += hits;
      });
      if (count) count.textContent = term ? total + (total === 1 ? ' result' : ' results') : '';
      if (none) none.hidden = !term || total > 0;
      if (window.ScrollTrigger) setTimeout(function () { ScrollTrigger.refresh(); }, 50);
    };
    search.addEventListener('input', run);
  }

  /* ---------- pricing: prices follow the chosen home size ---------- */
  var plans = q('[data-plans]');
  if (plans) {
    var REGULAR = { s: 89, m: 119, l: 149, xl: 189 }; // keep in step with js/booking.js
    var radios = qa('input[name="psize"]');
    var update = function () {
      var size = (radios.filter(function (r) { return r.checked; })[0] || {}).value || 'm';
      qa('.plan', plans).forEach(function (p) {
        var off = parseFloat(p.getAttribute('data-off')) || 0;
        var out = q('[data-plan-price]', p);
        if (out) out.textContent = '$' + Math.round(REGULAR[size] * (1 - off / 100));
        var b = q('[data-book]', p); if (b) b.setAttribute('data-size', size);
      });
    };
    radios.forEach(function (r) { r.addEventListener('change', update); });
    update();
  }

  /* ---------- contact form ---------- */
  var form = q('[data-contact-form]');
  if (form) {
    var ok = q('[data-contact-ok]');
    var CONTACT_ENDPOINT = ''; // e.g. a Formspree / Netlify Forms / your own API URL. Empty = confirm on the page only.
    var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var setErr = function (name, msg) {
      var el = q('[data-err="' + name + '"]', form), f = form.elements[name];
      if (el) el.textContent = msg || '';
      if (f) { if (msg) f.setAttribute('aria-invalid', 'true'); else f.removeAttribute('aria-invalid'); }
    };
    form.addEventListener('input', function (e) { if (e.target.name) setErr(e.target.name, ''); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = {}; ['name', 'email', 'phone', 'topic', 'message'].forEach(function (k) { d[k] = (form.elements[k].value || '').trim(); });
      var bad = false, first = null;
      var fail = function (k, m) { setErr(k, m); if (!first) first = form.elements[k]; bad = true; };
      if (d.name.length < 2) fail('name', 'Please enter your name.'); else setErr('name', '');
      if (!emailRe.test(d.email)) fail('email', 'Please enter a valid email address.'); else setErr('email', '');
      if (!d.topic) fail('topic', 'Please choose a topic.'); else setErr('topic', '');
      if (d.message.length < 10) fail('message', 'Please tell us a little more (10+ characters).'); else setErr('message', '');
      if (bad) { first.focus(); return; }
      var finish = function () {
        q('[data-ok-name]', ok).textContent = d.name.split(' ')[0];
        q('[data-ok-email]', ok).textContent = d.email;
        form.hidden = true; ok.hidden = false; ok.focus();
        document.dispatchEvent(new CustomEvent('clevaro:contact', { detail: d }));
      };
      if (CONTACT_ENDPOINT) {
        fetch(CONTACT_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(d) })
          .then(function (r) { if (!r.ok) throw new Error(r.status); finish(); })
          .catch(function () { setErr('message', 'Sorry, that did not send. Please try again or email hello@clevaro.com.'); });
      } else finish();
    });
    var again = q('[data-contact-again]');
    if (again) again.addEventListener('click', function () { form.reset(); form.hidden = false; ok.hidden = true; form.elements.name.focus(); });
  }
})();
