/* CLEVARO — booking.js
   Booking popup. One source of truth for every page: the dialog markup is built here and any
   element with [data-book] opens it.

     <button data-book>                     opens on step 1
     <button data-book="deep">              pre-selects a service (regular | deep | move | office)
     <button data-book="deep" data-focus="Kitchen">   …and pre-fills "Focus area: Kitchen"
     #book in the URL                       opens it on page load

   Sending: set BOOKING_ENDPOINT to a form service URL (Formspree, Basin, your own API…) and the
   request is POSTed there as JSON. While it is empty the form only confirms on the page. */
(function () {
  var BOOKING_ENDPOINT = '';

  var SERVICES = {
    regular: { name: 'Regular Cleaning',   recurring: true },
    deep:    { name: 'Deep Cleaning',      recurring: false },
    move:    { name: 'Move-In / Move-Out', recurring: false },
    office:  { name: 'Office Cleaning',    recurring: true }
  };
  var SIZES = [
    { id: 's', label: 'Studio / 1 bedroom' },
    { id: 'm', label: '2 bedrooms' },
    { id: 'l', label: '3 bedrooms' },
    { id: 'xl', label: '4+ bedrooms' }
  ];
  // starting prices (USD) — keep in step with the table on services.html
  var PRICES = {
    regular: { s: 89,  m: 119, l: 149, xl: 189 },
    deep:    { s: 159, m: 209, l: 269, xl: 339 },
    move:    { s: 189, m: 249, l: 319, xl: 399 },
    office:  { s: 99,  m: 149, l: 199, xl: 259 }
  };
  var FREQ = [
    { id: 'once',     label: 'One-time',  off: 0 },
    { id: 'weekly',   label: 'Weekly',    off: 0.15 },
    { id: 'biweekly', label: 'Bi-weekly', off: 0.10 },
    { id: 'monthly',  label: 'Monthly',   off: 0.05 }
  ];
  var SLOTS = [
    { id: 'morning',   label: 'Morning',   sub: '8am – 12pm' },
    { id: 'afternoon', label: 'Afternoon', sub: '12pm – 4pm' },
    { id: 'evening',   label: 'Evening',   sub: '4pm – 7pm' }
  ];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function chips(name, items, checked, cls) {
    return items.map(function (it, i) {
      var id = 'bk-' + name + '-' + it.id;
      return '<div class="bk-chip ' + (cls || '') + '">' +
        '<input type="radio" name="' + name + '" id="' + id + '" value="' + it.id + '"' + (it.id === checked ? ' checked' : '') + '>' +
        '<label for="' + id + '"><span>' + esc(it.label) + '</span>' + (it.sub ? '<small>' + esc(it.sub) + '</small>' : '') + '</label></div>';
    }).join('');
  }

  var serviceItems = Object.keys(SERVICES).map(function (k) { return { id: k, label: SERVICES[k].name }; });

  var html =
    '<div class="book__aside">' +
      '<span class="logo"><img src="' + assetBase() + 'assets/icons/logo-mark.svg" alt=""><span>Clevaro.</span></span>' +
      '<div class="book__aside-copy">' +
        '<h2 class="book__title" id="book-title">Book your clean</h2>' +
        '<p>Tell us about your space and when suits you. We confirm every booking by email.</p>' +
      '</div>' +
      '<ul class="book__perks">' +
        '<li>Free, no-obligation quote</li><li>Vetted, insured cleaners</li>' +
        '<li>Reply within 2 hours</li><li>100% satisfaction guarantee</li>' +
      '</ul>' +
      '<p class="book__contact">Prefer to talk?<a href="tel:+16285550147">+1 (628) 555-0147</a></p>' +
    '</div>' +
    '<div class="book__main" data-lenis-prevent>' +
      '<button class="book__close" type="button" data-book-close aria-label="Close booking form">&times;</button>' +
      '<form class="book__form" novalidate>' +
        '<div class="book__progress"><span class="book__step-label" data-step-label aria-live="polite"></span><div class="book__bar"><i data-bar></i></div></div>' +

        '<div class="book__step" data-step="1">' +
          '<fieldset class="bk-group"><legend>What do you need?</legend><div class="bk-chips bk-chips--2">' + chips('service', serviceItems, 'regular') + '</div></fieldset>' +
          '<div class="bk-row">' +
            '<div class="bk-field"><label for="bk-size">Size of space</label>' +
              '<select id="bk-size" name="size" required><option value="">Select size</option>' + SIZES.map(function (s) { return '<option value="' + s.id + '">' + s.label + '</option>'; }).join('') + '</select>' +
              '<span class="bk-err" data-err="size"></span></div>' +
            '<div class="bk-field"><label for="bk-date">Preferred date</label>' +
              '<input id="bk-date" name="date" type="date" required><span class="bk-err" data-err="date"></span></div>' +
          '</div>' +
          '<fieldset class="bk-group"><legend>Preferred time</legend><div class="bk-chips bk-chips--3">' + chips('slot', SLOTS, 'morning') + '</div></fieldset>' +
          '<fieldset class="bk-group" data-freq><legend>How often?</legend><div class="bk-chips bk-chips--4">' + chips('freq', FREQ, 'once') + '</div>' +
            '<p class="bk-hint">Recurring plans save up to 15%.</p></fieldset>' +
        '</div>' +

        '<div class="book__step" data-step="2" hidden>' +
          '<div class="bk-row">' +
            '<div class="bk-field"><label for="bk-name">Full name</label><input id="bk-name" name="name" type="text" autocomplete="name" required><span class="bk-err" data-err="name"></span></div>' +
            '<div class="bk-field"><label for="bk-email">Email</label><input id="bk-email" name="email" type="email" autocomplete="email" required><span class="bk-err" data-err="email"></span></div>' +
          '</div>' +
          '<div class="bk-row">' +
            '<div class="bk-field"><label for="bk-phone">Phone</label><input id="bk-phone" name="phone" type="tel" autocomplete="tel" required><span class="bk-err" data-err="phone"></span></div>' +
            '<div class="bk-field"><label for="bk-address">Address &amp; ZIP</label><input id="bk-address" name="address" type="text" autocomplete="street-address" required><span class="bk-err" data-err="address"></span></div>' +
          '</div>' +
          '<div class="bk-field"><label for="bk-notes">Anything we should know? <em>(optional)</em></label><textarea id="bk-notes" name="notes" rows="2" placeholder="Pets, access instructions, areas that need extra care…"></textarea></div>' +
          '<div class="bk-summary" data-summary aria-live="polite"></div>' +
        '</div>' +

        '<p class="bk-fail" data-fail role="alert" hidden>Something went wrong sending your request. Please try again or call us.</p>' +
        '<div class="book__actions">' +
          '<button class="book__back" type="button" data-back hidden>Back</button>' +
          '<button class="btn btn--dark book__next" type="submit"><span data-next-label>Continue</span>' +
            '<span class="btn__icon"><img src="' + assetBase() + 'assets/icons/arrow-dark.svg" alt=""><img src="' + assetBase() + 'assets/icons/arrow-dark.svg" alt=""></span></button>' +
        '</div>' +
      '</form>' +

      '<div class="book__done" data-done hidden tabindex="-1">' +
        '<span class="book__tick" aria-hidden="true"><svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M6 14.5l5.5 5.5L22 9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>' +
        '<h3 class="book__done-title" data-done-title></h3>' +
        '<p class="book__done-copy" data-done-copy></p>' +
        '<dl class="bk-recap" data-recap></dl>' +
        '<button class="btn btn--lime" type="button" data-book-close>Done<span class="btn__icon"><img src="' + assetBase() + 'assets/icons/arrow-lime.svg" alt=""><img src="' + assetBase() + 'assets/icons/arrow-lime.svg" alt=""></span></button>' +
      '</div>' +
    '</div>';

  // pages live in the site root, so the icon path is the same everywhere
  function assetBase() { return ''; }

  var dialog = document.createElement('dialog');
  dialog.className = 'book';
  dialog.id = 'book-modal';
  dialog.setAttribute('aria-labelledby', 'book-title');
  dialog.innerHTML = html;
  document.body.appendChild(dialog);

  var form = dialog.querySelector('.book__form');
  var steps = dialog.querySelectorAll('.book__step');
  var done = dialog.querySelector('[data-done]');
  var bar = dialog.querySelector('[data-bar]');
  var stepLabel = dialog.querySelector('[data-step-label]');
  var backBtn = dialog.querySelector('[data-back]');
  var nextLabel = dialog.querySelector('[data-next-label]');
  var fail = dialog.querySelector('[data-fail]');
  var freqGroup = dialog.querySelector('[data-freq]');
  var step = 1;
  var sending = false;

  function lenis(fn) { var l = window.CLEVARO && CLEVARO.lenis; if (l) l[fn](); }
  function val(name) { var el = form.elements[name]; return el ? (el.value || '').trim() : ''; }
  function radio(name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : ''; }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function todayISO() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

  function setErr(name, msg) {
    var el = form.elements[name];
    var out = dialog.querySelector('[data-err="' + name + '"]');
    if (out) out.textContent = msg || '';
    if (el) { if (msg) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid'); }
  }
  function clearErrs() { ['size', 'date', 'name', 'phone', 'email', 'address'].forEach(function (n) { setErr(n, ''); }); fail.hidden = true; }

  function validate(n) {
    var ok = true, firstBad = null;
    function bad(name, msg) { setErr(name, msg); ok = false; if (!firstBad) firstBad = form.elements[name]; }
    if (n === 1) {
      if (!val('size')) bad('size', 'Please choose a size.'); else setErr('size', '');
      var d = val('date');
      if (!d) bad('date', 'Please pick a date.');
      else if (d < todayISO()) bad('date', 'Please choose today or a later date.');
      else setErr('date', '');
    } else {
      if (val('name').length < 2) bad('name', 'Please enter your name.'); else setErr('name', '');
      if (val('phone').replace(/\D/g, '').length < 7) bad('phone', 'Please enter a valid phone number.'); else setErr('phone', '');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val('email'))) bad('email', 'Please enter a valid email address.'); else setErr('email', '');
      if (val('address').length < 5) bad('address', 'Please add your street address and ZIP.'); else setErr('address', '');
    }
    if (firstBad) firstBad.focus();
    return ok;
  }

  function quote() {
    var svc = radio('service'), size = val('size');
    var base = size && PRICES[svc] ? PRICES[svc][size] : 0;
    if (!base) return null;
    var f = SERVICES[svc].recurring ? FREQ.filter(function (x) { return x.id === radio('freq'); })[0] : FREQ[0];
    return { base: base, price: Math.round(base * (1 - (f ? f.off : 0))), off: f ? f.off : 0 };
  }
  function label(list, id) { var m = list.filter(function (x) { return x.id === id; })[0]; return m ? m.label : ''; }
  function prettyDate(iso) {
    var p = iso.split('-'); var d = new Date(+p[0], +p[1] - 1, +p[2]);
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
  }

  function syncFreq() {
    var svc = radio('service');
    var rec = SERVICES[svc] && SERVICES[svc].recurring;
    freqGroup.hidden = !rec;
    if (!rec) form.querySelector('#bk-freq-once').checked = true;
  }

  function renderSummary() {
    var q = quote(), svc = radio('service');
    var rows = [
      ['Service', SERVICES[svc].name],
      ['Size', label(SIZES, val('size'))],
      ['When', prettyDate(val('date')) + ', ' + label(SLOTS, radio('slot')).toLowerCase()]
    ];
    if (SERVICES[svc].recurring) rows.push(['Frequency', label(FREQ, radio('freq'))]);
    var out = '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>';
    if (q) out += '<p class="bk-price"><span>Estimated from</span><strong>$' + q.price + '</strong>' + (q.off ? '<small>includes ' + Math.round(q.off * 100) + '% recurring saving</small>' : '') + '</p>' +
      '<p class="bk-hint">We confirm the final price after reviewing your home. No payment is taken now.</p>';
    dialog.querySelector('[data-summary]').innerHTML = out;
  }

  function goto(n) {
    step = n;
    steps.forEach(function (s) { s.hidden = +s.getAttribute('data-step') !== n; });
    bar.style.width = (n / 2 * 100) + '%';
    stepLabel.textContent = 'Step ' + n + ' of 2 — ' + (n === 1 ? 'Your clean' : 'Your details');
    backBtn.hidden = n === 1;
    nextLabel.textContent = n === 1 ? 'Continue' : 'Request booking';
    if (n === 2) renderSummary();
    var first = steps[n - 1].querySelector('input:not([type=radio]), select');
    if (first && dialog.open && n === 2) first.focus();
    dialog.querySelector('.book__main').scrollTop = 0;
  }

  function reset() {
    form.reset();
    clearErrs();
    form.hidden = false; done.hidden = true; sending = false;
    form.elements.date.min = todayISO();
    syncFreq();
    goto(1);
  }

  function open(opts) {
    opts = opts || {};
    if (dialog.open) return;
    reset();
    if (opts.service && SERVICES[opts.service]) {
      form.querySelector('#bk-service-' + opts.service).checked = true;
      syncFreq();
    }
    if (opts.freq) {
      var fr = form.querySelector('input[name="freq"][value="' + opts.freq + '"]');
      if (fr && !fr.disabled) { fr.checked = true; fr.dispatchEvent(new Event('change', { bubbles: true })); }
    }
    if (opts.size && form.elements.size) { form.elements.size.value = opts.size; form.elements.size.dispatchEvent(new Event('change', { bubbles: true })); }
    if (opts.focus) form.elements.notes.value = 'Focus area: ' + opts.focus + '.';
    dialog.showModal();
    lenis('stop');
    document.body.style.overflow = 'hidden';
  }
  function close() { if (dialog.open) dialog.close(); }

  dialog.addEventListener('close', function () {
    lenis('start');
    document.body.style.overflow = '';
    if (location.hash === '#book') history.replaceState(null, '', location.pathname + location.search);
  });
  dialog.addEventListener('click', function (e) {
    if (e.target === dialog) close();                       // backdrop
    if (e.target.closest('[data-book-close]')) close();
  });

  form.addEventListener('change', function (e) {
    if (e.target.name === 'service') syncFreq();
    if (e.target.name === 'size' || e.target.name === 'date') setErr(e.target.name, '');
  });
  form.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid')) setErr(e.target.name, ''); });
  backBtn.addEventListener('click', function () { goto(1); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (sending) return;
    if (step === 1) { if (validate(1)) goto(2); return; }
    if (!validate(2)) return;

    var svc = radio('service'), q = quote();
    var payload = {
      service: SERVICES[svc].name,
      size: label(SIZES, val('size')),
      date: val('date'),
      time: label(SLOTS, radio('slot')),
      frequency: SERVICES[svc].recurring ? label(FREQ, radio('freq')) : 'One-time',
      estimate: q ? '$' + q.price : '',
      name: val('name'), email: val('email'), phone: val('phone'),
      address: val('address'), notes: val('notes'),
      page: location.href
    };

    sending = true; fail.hidden = true;
    var submit = form.querySelector('.book__next');
    submit.disabled = true; nextLabel.textContent = 'Sending…';

    var send = BOOKING_ENDPOINT
      ? fetch(BOOKING_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
          .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); })
      : new Promise(function (res) { setTimeout(res, 700); });

    send.then(function () {
      document.dispatchEvent(new CustomEvent('clevaro:booking', { detail: payload }));
      showDone(payload);
    }).catch(function () {
      fail.hidden = false;
      nextLabel.textContent = 'Request booking';
    }).then(function () { sending = false; submit.disabled = false; });
  });

  function showDone(p) {
    form.hidden = true; done.hidden = false;
    dialog.querySelector('[data-done-title]').textContent = 'Thank you, ' + p.name.split(' ')[0] + '.';
    dialog.querySelector('[data-done-copy]').textContent = 'Your request is in. We will email ' + p.email + ' within 2 hours to confirm your visit.';
    var rows = [['Service', p.service], ['When', prettyDate(p.date) + ', ' + p.time.toLowerCase()], ['Where', p.address]];
    if (p.estimate) rows.push(['Estimate from', p.estimate]);
    dialog.querySelector('[data-recap]').innerHTML = rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('');
    dialog.querySelector('.book__main').scrollTop = 0;
    done.focus();
  }

  // open from any [data-book] trigger (capture so anchor-scroll handlers never see the click)
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-book]');
    if (!t) return;
    e.preventDefault(); e.stopPropagation();
    var menu = document.getElementById('menu');
    var go = function () { open({ service: t.getAttribute('data-book'), focus: t.getAttribute('data-focus'), freq: t.getAttribute('data-freq'), size: t.getAttribute('data-size') }); };
    if (menu && menu.classList.contains('is-open')) { var c = menu.querySelector('[data-menu-close]'); if (c) c.click(); setTimeout(go, 1300); } else go();
  }, true);

  window.CLEVARO = window.CLEVARO || {};
  CLEVARO.openBooking = open;
  if (location.hash === '#book') window.addEventListener('load', function () { open(); });
})();
