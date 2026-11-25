#!/usr/bin/env python3
"""Generate about.html / services.html and patch index.html (shared header, menu, footer)."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

ARROW = lambda c: f'<span class="btn__icon"><img src="assets/icons/arrow-{c}.svg" alt=""><img src="assets/icons/arrow-{c}.svg" alt=""></span>'

def head(title, desc, extra_css=True):
    css = '''  <link rel="stylesheet" href="js/vendor/lenis.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/sections.css">
  <link rel="stylesheet" href="css/responsive.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/booking.css">'''
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#10291d">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">

  <link rel="preload" href="assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{css}
  <script>document.documentElement.classList.replace('no-js', 'js');</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
'''

def menu(home):
    p = '' if home else 'index.html'
    return f'''
  <!-- ===== MENU OVERLAY ===== -->
  <div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Site menu" aria-hidden="true">
    <div class="menu__top">
      <a class="logo" href="index.html" data-menu-link aria-label="Clevaro home"><img src="assets/icons/logo-mark.svg" alt=""><span>Clevaro.</span></a>
      <button class="menu__close" type="button" data-menu-close>Close</button>
    </div>
    <ul class="menu__list">
      <li class="menu__item"><a class="menu__link" href="index.html" data-menu-link><small>01</small>Home</a></li>
      <li class="menu__item"><a class="menu__link" href="about.html" data-menu-link><small>02</small>About</a></li>
      <li class="menu__item"><a class="menu__link" href="services.html" data-menu-link><small>03</small>Services</a></li>
      <li class="menu__item"><a class="menu__link" href="pricing.html" data-menu-link><small>04</small>Pricing</a></li>
      <li class="menu__item"><a class="menu__link" href="blog.html" data-menu-link><small>05</small>Blog</a></li>
      <li class="menu__item"><a class="menu__link" href="faq.html" data-menu-link><small>06</small>FAQ</a></li>
      <li class="menu__item"><a class="menu__link" href="contact.html" data-menu-link><small>07</small>Contact</a></li>
    </ul>
    <div class="menu__foot">
      <span>A Cleaner Home. A Better Everyday.</span>
      <a href="mailto:hello@clevaro.com">hello@clevaro.com</a>
    </div>
  </div>
'''

def header(cur, home=False):
    p = '' if home else 'index.html'
    def a(key, href, label):
        c = ' is-current' if cur == key else ''
        return f'<a class="nav__link{c}" href="{href}">{label}</a>'
    return f'''
    <!-- ===== HEADER ===== -->
    <header class="header" data-anim="header">
      <div class="header__row">
        <div class="header__left">
          <a class="logo" href="index.html" aria-label="Clevaro home"><img src="assets/icons/logo-mark.svg" alt=""><span>Clevaro.</span></a>
        </div>
        <nav class="nav" aria-label="Primary">
          {a('home', 'index.html', 'Home')}
          {a('about', 'about.html', 'About')}
          {a('services', 'services.html', 'Services')}
          {a('pricing', 'pricing.html', 'Pricing')}
        </nav>
        <div class="header__right">
          <a class="header__cta" href="tel:+16285550147" aria-label="Book a consultation: call +1 (628) 555-0147"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.6 3.5l2.2-.5c.5-.1 1 .2 1.200.7l1 2.600c.2.500 0 1-.4 1.300L9.300 8.800c1.100 2.300 2.900 4.100 5.200 5.200l1.200-1.300c.3-.4.8-.5 1.300-.4l2.600 1c.5.2.8.700.7 1.200l-.5 2.200c-.1.600-.6 1-1.200 1C10.600 17.600 5.300 12.300 5.600 4.700c0-.6.400-1.100 1-1.200z" stroke="currentColor" stroke-width="1.600" stroke-linejoin="round"/><path d="M14.500 3.500a6 6 0 016 6M14.500 6.500a3 3 0 013 3" stroke="currentColor" stroke-width="1.600" stroke-linecap="round"/></svg><span>Book A Consultation</span></a>
          <button class="header__book" type="button" data-book aria-label="Book a cleaning"><img src="assets/icons/calendar.svg" alt=""></button>
          <button class="menu-btn" type="button" data-menu-open aria-label="Open menu" aria-controls="menu"><img src="assets/icons/menu.svg" alt=""></button>
        </div>
      </div>
    </header>
'''

def footer(home=False):
    p = '' if home else 'index.html'
    return f'''
    <!-- ===== FOOTER ===== -->
    <footer class="footer" id="contact">
      <div class="footer__bg" data-parallax="footer" role="img" aria-label="A cleaner smiling in a bright home"></div>
      <div class="container">
        <div class="footer__row">
          <div class="footer__cta">
            <h2 class="footer__title" data-split="words">Let’s create a home that <span class="accent">Shines beautifully</span></h2>
            <div class="btn-wrap">
              <button class="btn btn--lime" type="button" data-book>Book a Cleaning
                {ARROW('lime')}
              </button>
            </div>
          </div>
          <div class="footer__card" data-footer-card>
            <div class="footer__top">
              <div class="footer__col">
                <a class="logo logo--footer" href="index.html" aria-label="Clevaro home"><img src="assets/icons/logo-mark.svg" alt=""><span>Clevaro.</span></a>
                <p class="footer__about">Premium home cleaning, designed around your lifestyle. A cleaner home, a better everyday.</p>
              </div>
              <div class="footer__col">
                <span class="footer__label">Newsletter</span>
                <form class="newsletter" data-newsletter novalidate>
                  <label class="sr-only" for="nl-email">Email address</label>
                  <input id="nl-email" type="email" name="email" placeholder="Email Address" autocomplete="email" required>
                  <button type="submit">Sign up</button>
                </form>
                <p class="newsletter__msg" role="status" aria-live="polite"></p>
              </div>
              <div class="footer__col footer__col--wide">
                <span class="footer__label">Quick links</span>
                <div class="footer__links">
                  <a href="about.html">About</a><a href="blog.html">Blog</a>
                  <a href="services.html">Services</a><a href="pricing.html">Pricing</a>
                  <a href="faq.html">FAQ</a><a href="contact.html">Contact</a>
                </div>
              </div>
              <div class="footer__col footer__col--wide">
                <span class="footer__label">Get in touch</span>
                <a class="footer__phone" href="tel:+16285550147">+1 (628) 555-0147</a>
                <a class="footer__mail" href="mailto:hello@clevaro.com">hello@clevaro.com</a>
                <span class="footer__label gap-top">Office</span>
                <address class="footer__address" style="font-style:normal">24 Maple Avenue,<br>Portland, OR 97205</address>
              </div>
            </div>
            <div class="footer__bottom">
              <span>© 2026 Clevaro. All rights reserved.</span>
              <div class="footer__social">
                <a href="#" aria-label="Facebook"><img src="assets/icons/facebook.svg" alt=""></a>
                <a href="#" aria-label="Instagram"><img src="assets/icons/instagram.svg" alt=""></a>
                <a href="#" aria-label="Pinterest"><img src="assets/icons/pinterest.svg" alt=""></a>
                <a href="#" aria-label="X"><img src="assets/icons/x.svg" alt=""></a>
              </div>
              <div class="footer__bottom-links"><a href="#">Privacy policy</a><a href="#">Terms</a></div>
            </div>
          </div>
        </div>
      </div>
    </footer>
'''

SCRIPTS = '''
  <script src="js/vendor/gsap.min.js"></script>
  <script src="js/vendor/ScrollTrigger.min.js"></script>
  <script src="js/vendor/SplitText.min.js"></script>
  <script src="js/vendor/lenis.min.js"></script>
  <script src="js/smooth-scroll.js"></script>
  <script src="js/menu.js"></script>
  <script src="js/booking.js"></script>
  <script src="js/inner.js"></script>
</body>
</html>
'''

LINES = '<div class="section-lines{c}" aria-hidden="true"><span></span><span></span><span></span><span></span></div>'

def phero(img, crumb, title, lead, extra=''):
    return f'''
      <section class="phero" aria-labelledby="page-title">
        <div class="phero__bg" style="background-image:url('{img}')" role="img" aria-label=""></div>
        <div class="section-lines on-dark" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <div class="container">
          <div class="phero__row">
            <div class="phero__main">
              <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
              <h1 class="phero__title" id="page-title">{title}</h1>
            </div>
            <div class="phero__side">
              <p class="phero__lead">{lead}</p>
              {extra}
            </div>
          </div>
        </div>
      </section>
'''

BOOKBTN = lambda label='Book a Cleaning', cls='btn--lime', attr='': f'<button class="btn {cls}" type="button" data-book{attr}>{label}{ARROW("lime" if cls=="btn--lime" else "dark")}</button>'

def band(title, text):
    return f'''
      <section class="band" aria-label="Book a cleaning">
        <div class="container">
          <div class="band__wrap">
            <h2 class="band__title">{title}</h2>
            <div class="band__side">
              <p>{text}</p>
              {BOOKBTN()}
            </div>
          </div>
        </div>
      </section>
'''

# ============================== ABOUT ==============================
def about():
    members = [
        ('team-1', 'Hannah Reyes', 'Founder &amp; Lead Cleaner'),
        ('team-2', 'Daniel Okafor', 'Operations Manager'),
        ('team-3', 'Sofia Marin', 'Senior Cleaner'),
        ('team-4', 'Marcus Lee', 'Quality Inspector'),
    ]
    team = ''.join(f'''
            <article class="member">
              <div class="member__img"><img src="assets/images/team/{i}.jpg" width="600" height="600" alt="{n}, {r.replace('&amp;','and')}" loading="lazy"></div>
              <div><h3 class="member__name">{n}</h3><p class="member__role">{r}</p></div>
            </article>''' for i, n, r in members)
    values = [
        ('01', 'about-detail', 'Detail first', 'We work to a written checklist for every room, so nothing gets missed, from skirting boards to switch plates.'),
        ('02', 'about-fresh', 'Fresh air inside', 'Eco-safe, allergen-aware products only. Your home should smell clean, not chemical.'),
        ('03', 'about-season', 'Reliable, every time', 'The same trusted team, on time, with the same standard on the first visit and the fiftieth.'),
        ('04', 'work-walkthrough', 'Respect for your home', 'Vetted, insured cleaners who treat your space and belongings exactly as they would their own.'),
    ]
    vals = ''.join(f'''
            <article class="value">
              <span class="value__no">{n}</span>
              <div class="value__body"><img src="assets/icons/{ic}.svg" alt=""><h3 class="value__title">{t}</h3><p class="value__copy">{c}</p></div>
            </article>''' for n, ic, t, c in values)
    s = head('About Clevaro — Premium Home Cleaning in Portland', 'Meet the trained, insured team behind Clevaro and the values that shape every visit: detail first, fresh air inside, reliable every time.')
    s += menu(False)
    s += '\n  <div class="page-wrapper" id="top">\n' + header('about')
    s += '\n    <main id="main">\n'
    s += phero('assets/images/footer/footer-bg.jpg', 'About us',
               'Cleaning with care, <em>for homes that matter.</em>',
               'Clevaro started with a simple belief: coming home should feel good. We are a team of trained, insured cleaners who treat every space like our own.',
               BOOKBTN())
    s += f'''
      <!-- ===== STORY ===== -->
      <section class="section story" aria-labelledby="story-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="story__row">
            <h2 class="story__lead" id="story-title" data-split="lines">We believe a clean home shouldn’t be complicated. So we built a service that is <em>careful, calm</em> and completely reliable.</h2>
            <div class="story__body" data-r-group>
              <p>Clevaro began in Portland with one cleaner, one van and a very long checklist. Friends told friends, and the checklist stuck: every room, every surface, every visit.</p>
              <p>Today we are a team of trained professionals who bring the same careful routine to apartments, family homes and small offices. We use safe products, show up on time and finish with an inspection, so you never have to wonder whether it was done properly.</p>
              <div class="story__img" data-r-img><img src="assets/images/about/about-2.jpg" width="646" height="560" alt="Two Clevaro cleaners making a bed with fresh white linen" loading="lazy"></div>
            </div>
          </div>
          <div class="stats" data-r-group>
            <div class="stats__item"><span class="stats__num" data-count="1" data-suffix="k+">1k+</span><span class="stats__label">Homes cleaned</span></div>
            <div class="stats__item"><span class="stats__num" data-count="4.9">4.9</span><span class="stats__label">Average client rating</span></div>
            <div class="stats__item"><span class="stats__num" data-count="100" data-suffix="%">100%</span><span class="stats__label">Satisfaction guarantee</span></div>
            <div class="stats__item"><span class="stats__num" data-count="35" data-suffix="+">35+</span><span class="stats__label">Trained, insured cleaners</span></div>
          </div>
        </div>
      </section>

      <!-- ===== VALUES ===== -->
      <section class="section values" aria-labelledby="values-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="pg-head">
            <span class="eyebrow">What we stand for</span>
            <h2 class="h2" id="values-title" data-split="words">Four promises behind every visit</h2>
          </div>
          <div class="values__grid" data-r-group>{vals}
          </div>
        </div>
      </section>

      <!-- ===== QUOTE ===== -->
      <section class="section quote" aria-label="Founder’s note">
        <div class="container">
          <figure class="quote__wrap">
            <blockquote class="quote__text" style="margin:0">“We don’t measure a visit by how long we stayed. We measure it by how the home feels when you walk back in.”</blockquote>
            <figcaption class="quote__by">Hannah Reyes, Founder</figcaption>
          </figure>
        </div>
      </section>

      <!-- ===== TEAM ===== -->
      <section class="section team" aria-labelledby="team-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="team__top">
            <div class="pg-head">
              <span class="eyebrow">Our team</span>
              <h2 class="h2" id="team-title" data-split="words">The people behind the shine</h2>
            </div>
            <p class="pg-head" style="max-width:380px;font-size:16px;line-height:155%" data-r>Every cleaner is background-checked, trained in our room-by-room method and fully insured before their first visit.</p>
          </div>
          <div class="team__grid" data-r-group>{team}
          </div>
        </div>
      </section>
'''
    s += band('Ready for a home that <em>feels fresh</em> every day?', 'Tell us about your space and pick a time. We confirm every booking by email within two hours.')
    s += '\n    </main>\n' + footer(False) + '  </div>\n' + SCRIPTS
    return s

# ============================== SERVICES ==============================
def services():
    def checks(items):
        return '<ul class="checks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
    def sd(id_, flip, img, alt, tag, n, title, copy, dur, frm, best, inc, key):
        return f'''
        <article class="sd{' sd--flip' if flip else ''}" id="{id_}">
          <div class="sd__media" data-r-img><img src="{img}" width="2480" height="1100" alt="{alt}" loading="lazy"><span class="sd__tag">{tag}</span></div>
          <div class="sd__body" data-r-group>
            <span class="eyebrow">{n}</span>
            <h2 class="sd__title">{title}</h2>
            <p class="sd__copy">{copy}</p>
            <dl class="sd__meta"><div><dt>Duration</dt><dd>{dur}</dd></div><div><dt>From</dt><dd>{frm}</dd></div><div><dt>Best for</dt><dd>{best}</dd></div></dl>
            <div><h3 class="sd__inc-title">What’s included</h3></div>
            {checks(inc)}
            <div class="sd__actions">{BOOKBTN('Book Move-In / Out' if key=='move' else 'Book ' + title, 'btn--dark', f'="{key}"')}<a class="link-u" href="#pricing">See pricing</a></div>
          </div>
        </article>'''
    blocks = sd('regular', False, 'assets/images/services/regular-cleaning.jpg', 'Cleaner vacuuming a bright living room', 'Most popular', '01 — Regular',
                'Regular Cleaning', 'A thoughtful routine designed around your space and lifestyle. Weekly, bi-weekly or monthly, the same trusted team keeps your home fresh so you can enjoy it.',
                '2–3 hrs', '$89', 'Busy households',
                ['Dusting of all reachable surfaces', 'Vacuuming and mopping all floors', 'Kitchen counters, sink and hob wiped', 'Bathrooms scrubbed and sanitised', 'Mirrors and glass polished', 'Beds made on request', 'Bins emptied and re-lined', 'Eco-safe products only'], 'regular')
    blocks += sd('deep', True, 'assets/images/services/deep-cleaning.jpg', 'Cleaner steam-cleaning tiles during a deep clean', 'Top to bottom', '02 — Deep',
                'Deep Cleaning', 'Turn your busiest rooms into a fresh, spotless, healthy living space. A slow, detailed reset that reaches everything a regular visit does not.',
                '4–6 hrs', '$159', 'Seasonal resets',
                ['Steam-cleaned tile and grout', 'Inside oven and microwave', 'Fridge and cabinet fronts', 'Baseboards and door frames', 'Window sills and tracks', 'Descaled taps and fixtures', 'Light fittings and vents', 'Behind and under furniture'], 'deep')
    blocks += sd('move', False, 'assets/images/services/move-in-out.jpg', 'Empty apartment being cleaned before move-in', 'Deposit-ready', '03 — Move-In / Move-Out',
                'Move-In / Move-Out', 'Hand over or settle into a home that is spotless and stress-free. We work from a landlord-style checklist so you get your deposit back or start fresh.',
                '4–7 hrs', '$189', 'Moving day',
                ['Full clean of the empty home', 'Inside all cupboards and drawers', 'Appliances cleaned inside and out', 'Wall marks and scuffs spot-cleaned', 'Interior windows and sills', 'Floors steamed or mopped', 'Bathrooms descaled and polished', 'Move-out checklist for your deposit'], 'move')

    rooms = [
        ('kitchen', 'Kitchen Cleaning', 'Degreased, sanitised and gleaming from counters to appliances.', 'deep', 'Kitchen', 'Spotless modern kitchen'),
        ('bathroom', 'Bathroom Cleaning', 'Every tile and fixture cared for, so your bathroom feels brand new.', 'deep', 'Bathroom', 'Bright, freshly cleaned bathroom'),
        ('apartment', 'Apartment Cleaning', 'Start fresh with a tidy, comfortable space. Built your way.', 'regular', 'Apartment', 'Tidy, light-filled apartment'),
        ('office', 'Office Cleaning', 'Simple, reliable cleaning for everyday workspaces.', 'office', '', 'Clean, organised office workspace'),
    ]
    rm = ''.join(f'''
            <article class="room">
              <div class="room__img"><img src="assets/images/categories/{k}.jpg" width="939" height="1049" alt="{alt}" loading="lazy"></div>
              <div class="room__body"><h3 class="room__name">{n}</h3><p class="room__copy">{c}</p>
                <button class="link-u" type="button" data-book="{b}"{f' data-focus="{fo}"' if fo else ''}>Book this clean</button></div>
            </article>''' for k, n, c, b, fo, alt in rooms)

    steps = [('01 — Read the home', 'work-walkthrough', 'Home walkthrough', 'Tell us about your rooms, pets and priorities. We confirm the plan and a fixed estimate before we arrive.'),
             ('02 — Layer the clean', 'work-layers', 'Plan in layers', 'Your cleaners follow a room-by-room checklist, working top to bottom so every surface is done once, properly.'),
             ('03 — Clean and hand off', 'work-sparkle', 'Clean and inspect', 'We finish with a quality inspection and a quick walk-through. Not happy? We come back and re-clean, free.')]
    st = ''.join(f'''
            <article class="step"><div class="step__top"><span class="step__no">{n}</span><img src="assets/icons/{ic}.svg" alt=""></div><div><h3 class="step__title">{t}</h3><p class="step__copy">{c}</p></div></article>''' for n, ic, t, c in steps)

    P = {'regular': (89, 119, 149, 189), 'deep': (159, 209, 269, 339), 'move': (189, 249, 319, 399), 'office': (99, 149, 199, 259)}
    sizes = [('Studio / 1 bedroom', 'up to 750 sq ft'), ('2 bedrooms', 'up to 1,100 sq ft'), ('3 bedrooms', 'up to 1,600 sq ft'), ('4+ bedrooms', 'up to 2,400 sq ft')]
    rows = ''.join(f'<tr><th scope="row">{n}<small>{sub}</small></th>' + ''.join(f'<td><small>from </small>${P[k][i]}</td>' for k in ('regular', 'deep', 'move', 'office')) + '</tr>' for i, (n, sub) in enumerate(sizes))

    faqs = [('How long does a visit take?', 'A regular clean of a two-bedroom home usually takes two to three hours. Deep cleans and move-out cleans take four to seven hours depending on size and condition. We give you a time window when we confirm.'),
            ('Do I need to be home?', 'No. Many clients give us a key, a door code or a lockbox. If you prefer to be there, that is fine too. Either way you will get a message when we arrive and when we finish.'),
            ('Do you bring your own supplies and equipment?', 'Yes. We bring everything, including eco-safe, allergen-aware products and professional equipment. If you would like us to use something specific, just add it to your booking notes.'),
            ('Are your cleaners vetted and insured?', 'Every cleaner is background-checked, trained in our room-by-room method and covered by our liability insurance before their first visit.'),
            ('What if I am not happy with the result?', 'Tell us within 24 hours and we will come back and re-clean the areas you are not happy with at no charge. That is our 100% satisfaction guarantee.'),
            ('Can I change or cancel a booking?', 'Yes. You can reschedule or cancel free of charge up to 24 hours before your visit. Recurring plans can be paused or changed at any time.')]
    fq = ''.join(f'<details class="qa"{" open" if i == 0 else ""}><summary>{q}</summary><p class="qa__a">{a}</p></details>' for i, (q, a) in enumerate(faqs))

    s = head('Cleaning Services & Pricing — Clevaro', 'Regular, deep and move-in / move-out cleaning with clear inclusions and transparent starting prices. Book online in under two minutes.')
    s += menu(False)
    s += '\n  <div class="page-wrapper" id="top">\n' + header('services')
    s += '\n    <main id="main">\n'
    s += phero('assets/images/services/regular-cleaning.jpg', 'Services',
               'Cleaning that fits <em>your home,</em> not the other way round.',
               'Three core services, four room specialities and plans that flex around your week. Pick what you need and we will handle the rest.',
               BOOKBTN())
    s += '''
      <div class="subnav-wrap"><nav class="subnav" aria-label="On this page">
        <a href="#regular">Regular</a><a href="#deep">Deep</a><a href="#move">Move-In / Out</a><a href="#rooms">Rooms</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a>
      </nav></div>

      <!-- ===== SERVICE DETAILS ===== -->
      <section class="sd-wrap" aria-label="Cleaning services">
        <div class="section-lines" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <div class="container">''' + blocks + '''
        </div>
      </section>
'''
    s += f'''
      <!-- ===== ROOMS ===== -->
      <section class="section rooms" id="rooms" aria-labelledby="rooms-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="pg-head">
            <span class="eyebrow">Room specialities</span>
            <h2 class="h2" id="rooms-title" data-split="words">Need one room done right?</h2>
            <p data-r>Book a focused clean for the spaces that matter most. Every speciality starts from our core services and adds extra time where you need it.</p>
          </div>
          <div class="rooms__grid" data-r-group>{rm}
          </div>
        </div>
      </section>

      <!-- ===== HOW IT WORKS ===== -->
      <section class="section steps" aria-labelledby="steps-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="pg-head">
            <span class="eyebrow">How it works</span>
            <h2 class="h2" id="steps-title" data-split="words">Three steps. One spotless home.</h2>
          </div>
          <div class="steps__grid" data-r-group>{st}
          </div>
        </div>
      </section>

      <!-- ===== PRICING ===== -->
      <section class="section price" id="pricing" aria-labelledby="price-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="pg-head">
            <span class="eyebrow">Transparent pricing</span>
            <h2 class="h2" id="price-title" data-split="words">Clear starting prices, no surprises</h2>
            <p data-r>Pick the size of your space to see what each service costs. Recurring plans save up to 15% on every visit.</p>
          </div>
          <div class="price__wrap" data-r>
            <table class="ptable">
              <thead><tr><th scope="col">Size of space</th><th scope="col">Regular</th><th scope="col">Deep</th><th scope="col">Move-In / Out</th><th scope="col">Office</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
          <div class="price__note" data-r>
            <p>Prices are starting estimates for homes in standard condition. We confirm a fixed price after a quick review of your space, and no payment is taken when you book.</p>
            <div class="save"><span>Weekly <b>−15%</b></span><span>Bi-weekly <b>−10%</b></span><span>Monthly <b>−5%</b></span></div>
          </div>
        </div>
      </section>

      <!-- ===== FAQ ===== -->
      <section class="section faq" id="faq" aria-labelledby="faq-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="faq__row">
            <div class="faq__aside">
              <div class="pg-head">
                <span class="eyebrow">FAQ</span>
                <h2 class="h2" id="faq-title" data-split="words">Questions, answered.</h2>
              </div>
              <p data-r>Can’t find what you are looking for? Call us on <a class="link-u" href="tel:+16285550147">+1 (628) 555-0147</a> or send your question with a booking request.</p>
              {BOOKBTN('Book a Cleaning', 'btn--dark')}
            </div>
            <div class="faq__list" data-r>{fq}</div>
          </div>
        </div>
      </section>
'''
    s += band('A cleaner home is <em>one booking away.</em>', 'Choose your service, pick a time and we will confirm by email within two hours. Free, no-obligation quote.')
    s += '\n    </main>\n' + footer(False) + '  </div>\n' + SCRIPTS
    return s

# ============================== INDEX PATCH ==============================
def patch_index():
    p = ROOT / 'index.html'
    s = p.read_text()
    if 'booking.css' in s:
        print('index already patched'); return
    s = s.replace('  <link rel="stylesheet" href="css/responsive.css">\n', '  <link rel="stylesheet" href="css/responsive.css">\n  <link rel="stylesheet" href="css/booking.css">\n')
    # menu
    s = re.sub(r'\n  <!-- ===== MENU OVERLAY ===== -->.*?\n  </div>\n\n  <div class="page-wrapper"', menu(True) + '\n  <div class="page-wrapper"', s, flags=re.S)
    s = s.replace('<a class="logo" href="index.html" data-menu-link', '<a class="logo" href="#top" data-menu-link')
    s = s.replace('<li class="menu__item"><a class="menu__link" href="index.html" data-menu-link>', '<li class="menu__item"><a class="menu__link" href="#top" data-menu-link>')
    s = s.replace('href="#categories" data-menu-link', 'href="#categories" data-menu-link')
    # header
    s = re.sub(r'\n    <!-- ===== HEADER ===== -->.*?</header>\n', header('home', True).replace('href="index.html" aria-label="Clevaro home"', 'href="#top" aria-label="Clevaro home"'), s, flags=re.S)
    # hero links
    s = s.replace('<a class="btn btn--lime" href="#services">Explore Services', '<a class="btn btn--lime" href="services.html">Explore Services')
    s = s.replace('<a class="round-arrow" href="#about" aria-label="Learn more about Clevaro">', '<a class="round-arrow" href="about.html" aria-label="Learn more about Clevaro">')
    # service arrows
    for name, anchor in (('Regular Cleaning', 'regular'), ('Deep Cleaning', 'deep'), ('Move-In / Move-Out Cleaning', 'move')):
        s = s.replace(f'<a class="service__arrow" href="#contact" aria-label="Book {name}">', f'<a class="service__arrow" href="services.html#{anchor}" aria-label="Learn more about {name}">')
    # CTA
    s = s.replace('<a class="btn btn--dark" href="#contact">Explore Plans', '<a class="btn btn--dark" href="services.html#pricing">Explore Plans')
    # footer
    s = re.sub(r'\n    <!-- ===== 9\. FOOTER ===== -->.*?</footer>\n', footer(True).replace('<!-- ===== FOOTER ===== -->', '<!-- ===== 9. FOOTER ===== -->').replace('href="index.html" aria-label="Clevaro home"', 'href="#top" aria-label="Clevaro home"'), s, flags=re.S) if False else s
    s = s.replace('<a class="btn btn--lime" href="mailto:hello@clevaro.com">Explore Our Services\n                <span class="btn__icon"><img src="assets/icons/arrow-lime.svg" alt=""><img src="assets/icons/arrow-lime.svg" alt=""></span>\n              </a>',
                  '<button class="btn btn--lime" type="button" data-book>Book a Cleaning\n                <span class="btn__icon"><img src="assets/icons/arrow-lime.svg" alt=""><img src="assets/icons/arrow-lime.svg" alt=""></span>\n              </button>')
    s = s.replace('<a href="#about">About</a><a href="#blog">Blog</a>\n                  <a href="#services">Services</a><a href="#plans">Plans</a>\n                  <a href="#process">FAQ</a><a href="#contact">Contact</a>',
                  '<a href="about.html">About</a><a href="#blog">Blog</a>\n                  <a href="services.html">Services</a><a href="#plans">Plans</a>\n                  <a href="services.html#faq">FAQ</a><a href="#contact">Contact</a>')
    s = s.replace('  <script src="js/video.js"></script>\n', '  <script src="js/video.js"></script>\n  <script src="js/booking.js"></script>\n')
    p.write_text(s)
    print('index patched')

(ROOT / 'about.html').write_text(about())
(ROOT / 'services.html').write_text(services())
patch_index()
print('ok')
