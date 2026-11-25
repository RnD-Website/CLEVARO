#!/usr/bin/env python3
"""Generate blog.html, blog-single.html, faq.html, pricing.html, contact.html.
Shares the header / menu / footer / hero partials with build.py (everything above `def about()`)."""
import pathlib

_src = pathlib.Path(__file__).resolve().with_name('build.py').read_text()
exec(_src[:_src.index('def about():')])   # head, menu, header, footer, phero, band, BOOKBTN, ARROW, LINES, SCRIPTS, ROOT

EXTRA = '''  <script src="js/extra.js"></script>
</body>
</html>
'''
SCRIPTS2 = SCRIPTS.replace('</body>\n</html>\n', '') + EXTRA

def page(title, desc, cur, hero, body):
    s = head(title, desc)
    s += menu(False)
    s += '\n  <div class="page-wrapper" id="top">\n' + header(cur)
    s += '\n    <main id="main">\n' + hero + body + '\n    </main>\n' + footer(False) + '  </div>\n' + SCRIPTS2
    return s

def pg_head(eyebrow, title, tid, text='', center=False):
    c = ' pg-head--center' if center else ''
    p = f'\n            <p data-r>{text}</p>' if text else ''
    return f'''<div class="pg-head{c}">
            <span class="eyebrow">{eyebrow}</span>
            <h2 class="h2" id="{tid}" data-split="words">{title}</h2>{p}
          </div>'''

# ============================== BLOG DATA ==============================
AUTHORS = {
    'hannah': ('Hannah Reyes', 'Founder & Lead Cleaner', 'team-1'),
    'daniel': ('Daniel Okafor', 'Operations Manager', 'team-2'),
    'sofia':  ('Sofia Marin', 'Senior Cleaner', 'team-3'),
    'marcus': ('Marcus Lee', 'Quality Inspector', 'team-4'),
}
# (img, w, h, alt, category, key, read, date, title, excerpt, author)
POSTS = [
    ('blog/blog-1', 646, 646, 'Cleaner preparing eco-safe products', 'Guides', 'guides', '5 min read', 'Nov 12, 2026',
     'How often should you deep clean your home?',
     'A deep clean is a reset, not a bigger weekly tidy. Here is how to decide how often your home needs one and what to include.', 'hannah'),
    ('blog/blog-2', 848, 668, 'Person organising a tidy shelf', 'Routines', 'routines', '4 min read', 'Nov 5, 2026',
     'How to build a cleaning routine that actually works',
     'Start small, anchor tasks to things you already do and let a simple weekly rhythm do the heavy lifting.', 'sofia'),
    ('blog/blog-3', 646, 756, 'Cleaning supplies on a bright counter', 'Routines', 'routines', '3 min read', 'Oct 28, 2026',
     '7 easy habits for a cleaner home',
     'Seven two-minute habits that stop mess building up, from the evening reset to the one-in, one-out rule.', 'daniel'),
    ('categories/kitchen', 939, 1049, 'Spotless modern kitchen', 'Guides', 'guides', '6 min read', 'Oct 21, 2026',
     'The 20-minute weekly kitchen reset',
     'Counters, sink, hob and fridge shelf: a quick order of work that keeps the busiest room fresh.', 'hannah'),
    ('categories/bathroom', 939, 1261, 'Bright, freshly cleaned bathroom', 'Guides', 'guides', '5 min read', 'Oct 14, 2026',
     'Bathroom grime: what actually works',
     'Soap scum, limescale and grout each need a different approach. Match the product to the problem.', 'sofia'),
    ('services/move-in-out', 2480, 1100, 'Empty room ready for move-in', 'Moving', 'moving', '7 min read', 'Oct 7, 2026',
     'Moving out? Your deposit-ready cleaning checklist',
     'What landlords and buyers look at first, and the room-by-room order that gets you the full deposit back.', 'marcus'),
    ('categories/apartment', 939, 1066, 'Tidy, light-filled apartment', 'Routines', 'routines', '4 min read', 'Sep 30, 2026',
     'Small-space cleaning: make your apartment feel bigger',
     'Clear surfaces, closed storage and a smart weekly loop make compact homes feel calm and open.', 'daniel'),
    ('services/deep-cleaning', 2480, 1100, 'Cleaner wiping a window sill', 'Eco-safe', 'eco', '5 min read', 'Sep 23, 2026',
     'Eco-safe cleaning: what to look for on the label',
     'Plain-language tips for choosing products that clean well and keep the air in your home fresh.', 'marcus'),
    ('categories/office', 939, 866, 'Clean, organised office workspace', 'Guides', 'guides', '4 min read', 'Sep 16, 2026',
     'A home-office clean that keeps you focused',
     'Desk, screen and cables: a short weekly routine that keeps your workspace tidy and your head clear.', 'sofia'),
]

def card(p, cls='bcard'):
    img, w, h, alt, cat, key, read, date, title, ex, au = p
    return f'''
            <article class="{cls}" data-cat="{key}">
              <a class="bcard__img" href="blog-single.html" tabindex="-1" aria-hidden="true"><img src="assets/images/{img}.jpg" width="{w}" height="{h}" alt="" loading="lazy"></a>
              <div class="bcard__body">
                <span class="post__meta">{cat} · {read}</span>
                <h3 class="bcard__title"><a href="blog-single.html">{title}</a></h3>
                <p class="bcard__ex">{ex}</p>
                <span class="post__meta">{date}</span>
              </div>
            </article>'''

# ============================== BLOG ==============================
def blog():
    f = POSTS[0]
    fa = AUTHORS[f[10]]
    feat = f'''
      <!-- ===== FEATURED ===== -->
      <section class="section bfeat" aria-labelledby="feat-title">
        {LINES.format(c='')}
        <div class="container">
          <article class="bfeat__row" data-r>
            <a class="bfeat__img" href="blog-single.html" tabindex="-1" aria-hidden="true"><img src="assets/images/blog/blog-1.jpg" width="646" height="646" alt="" ></a>
            <div class="bfeat__body">
              <span class="eyebrow">Featured · {f[4]}</span>
              <h2 class="bfeat__title" id="feat-title"><a href="blog-single.html">{f[8]}</a></h2>
              <p class="bfeat__ex">{f[9]}</p>
              <div class="byline"><img src="assets/images/team/{fa[2]}.jpg" width="48" height="48" alt=""><div><b>{fa[0]}</b><span>{f[7]} · {f[6]}</span></div></div>
              <a class="btn btn--dark" href="blog-single.html">Read the article{ARROW('dark')}</a>
            </div>
          </article>
        </div>
      </section>
'''
    chips = [('all', 'All articles'), ('guides', 'Guides'), ('routines', 'Routines'), ('eco', 'Eco-safe'), ('moving', 'Moving')]
    chip_html = ''.join(f'<button class="chip{" is-active" if k == "all" else ""}" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in chips)
    cards = ''.join(card(p) for p in POSTS[1:])
    grid = f'''
      <!-- ===== LATEST ===== -->
      <section class="section blist" aria-labelledby="latest-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="blist__top">
            {pg_head('Latest', 'Fresh reading for a fresher home', 'latest-title')}
            <div class="chips" role="group" aria-label="Filter articles">{chip_html}</div>
          </div>
          <div class="bgrid" data-blog-grid>{cards}
          </div>
          <p class="bempty" data-blog-empty hidden>No articles in this topic yet. Check back soon.</p>
        </div>
      </section>

      <!-- ===== NEWSLETTER ===== -->
      <section class="section bnews" aria-labelledby="news-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="bnews__row">
            <div class="bnews__copy">
              <span class="eyebrow">Newsletter</span>
              <h2 class="h2" id="news-title" data-split="words">One useful cleaning tip, every month.</h2>
            </div>
            <div class="bnews__form" data-r>
              <p>Short, practical and free of spam. Unsubscribe whenever you like.</p>
              <form class="nl2" data-newsletter novalidate>
                <label class="sr-only" for="nl-email-2">Email address</label>
                <input id="nl-email-2" type="email" name="email" placeholder="Email Address" autocomplete="email" required>
                <button type="submit">Subscribe</button>
              </form>
              <p class="newsletter__msg nl2__msg" role="status" aria-live="polite"></p>
            </div>
          </div>
        </div>
      </section>
'''
    hero = phero('assets/images/cta/cta-bg.jpg', 'Blog', 'Ideas for <em>a fresher home.</em>',
                 'Practical cleaning guides, routines and eco-safe tips from the team that cleans homes every day.')
    return page('Blog — Cleaning Guides & Tips | Clevaro', 'Practical cleaning guides, routines and eco-safe tips from the Clevaro team.', 'blog',
                hero, feat + grid + band('A cleaner home is <em>one booking away.</em>', 'Skip the to-do list. Choose your service, pick a time and we will confirm by email within two hours.'))

# ============================== SINGLE ==============================
def blog_single():
    f = POSTS[0]; au = AUTHORS['hannah']
    meta = f'<div class="byline byline--light"><img src="assets/images/team/{au[2]}.jpg" width="48" height="48" alt=""><div><b>{au[0]}</b><span>{f[7]} · {f[6]}</span></div></div>'
    hero = phero('assets/images/services/deep-cleaning.jpg', '<a href="blog.html">Blog</a> <span aria-hidden="true">/</span> Guides',
                 f[8].replace('deep clean', '<em>deep clean</em>'),
                 f[9], meta)
    hero = hero.replace('section-lines on-dark', 'section-lines on-dark no-mid')
    toc = [('what', 'What a deep clean covers'), ('often', 'A simple rule of thumb'), ('rooms', 'Room by room'), ('between', 'Between deep cleans')]
    toc_html = ''.join(f'<a href="#{i}">{t}</a>' for i, t in toc)
    related = ''.join(card(p) for p in POSTS[1:5])
    body = f'''
      <!-- ===== ARTICLE ===== -->
      <section class="art" aria-label="Article">
        {LINES.format(c=' no-mid')}
        <div class="container">
          <div class="art__row">
            <aside class="art__aside" aria-label="About this article">
              <div class="art__card">
                <span class="art__label">Written by</span>
                <div class="byline"><img src="assets/images/team/{au[2]}.jpg" width="48" height="48" alt=""><div><b>{au[0]}</b><span>{au[1]}</span></div></div>
              </div>
              <nav class="art__toc" aria-label="In this article"><span class="art__label">In this article</span>{toc_html}</nav>
              <div class="art__share"><span class="art__label">Share</span>
                <div>
                  <a href="#" data-share="facebook" aria-label="Share on Facebook"><img src="assets/icons/facebook.svg" alt=""></a>
                  <a href="#" data-share="x" aria-label="Share on X"><img src="assets/icons/x.svg" alt=""></a>
                  <a href="#" data-share="pinterest" aria-label="Share on Pinterest"><img src="assets/icons/pinterest.svg" alt=""></a>
                  <button type="button" data-copy-link aria-label="Copy link">Copy link</button>
                </div>
              </div>
            </aside>

            <article class="art__body prose">
              <p class="prose__lead">Most homes get a weekly tidy. Fewer get a proper reset. A deep clean reaches everything the weekly routine skips, and a simple schedule means you never have to dread it.</p>

              <h2 id="what">What a deep clean actually covers</h2>
              <p>Regular cleaning keeps surfaces tidy: floors vacuumed, counters wiped, bathrooms refreshed. A deep clean goes further. It reaches behind and under furniture, inside appliances, along skirting boards and window tracks, and into the grout lines and vents that quietly collect dust and grease.</p>
              <figure class="prose__fig"><img src="assets/images/blog/blog-2.jpg" width="848" height="668" alt="A tidy shelf after a clean" loading="lazy"><figcaption>Deep cleaning is about the places a weekly tidy never reaches.</figcaption></figure>

              <h2 id="often">A simple rule of thumb</h2>
              <p>For most households, two to four deep cleans a year is the sweet spot. Where you land depends on how your home is used:</p>
              <ul>
                <li><b>Quiet home, regular weekly cleaning:</b> twice a year, ideally in spring and autumn.</li>
                <li><b>Children or pets:</b> every three months, as floors, soft furnishings and entrance areas work harder.</li>
                <li><b>Allergies in the household:</b> bedrooms and soft furnishings more often, as dust and pollen build up.</li>
                <li><b>Life events:</b> before or after moving, renovations, a new baby or hosting guests.</li>
              </ul>
              <aside class="prose__note"><b>Tip.</b> Tie deep cleans to the calendar. The first weekend of each season is easy to remember and spreads the work evenly across the year.</aside>

              <h2 id="rooms">Room by room: what to prioritise</h2>
              <p>You do not need to do everything at once. If time is tight, start with the rooms that work hardest.</p>
              <ul>
                <li><b>Kitchen:</b> oven interior, fridge shelves, extractor filter and cabinet fronts.</li>
                <li><b>Bathrooms:</b> grout, shower head, extractor fan and the base of taps and fixtures.</li>
                <li><b>Bedrooms:</b> mattress and under the bed, curtains and the tops of wardrobes.</li>
                <li><b>Living areas:</b> sofa cushions, skirting boards and the space behind the TV unit.</li>
              </ul>
              <blockquote class="prose__quote"><p>A deep clean makes your weekly clean faster, because the hard work is already done.</p><cite>{au[0]}, {au[1]}</cite></blockquote>

              <h2 id="between">Make the time between cleans easier</h2>
              <p>The best deep clean is the one you do not dread. Between visits, keep it light: wipe as you go, take ten minutes for an evening reset, and give one zone of the home a little extra attention each week. Small habits compound, and a deep clean then becomes a refresh rather than a rescue.</p>
              <p>If you would rather hand it over, our team follows a written room-by-room checklist, brings eco-safe products and equipment, and re-cleans for free if anything is missed.</p>
              <div class="prose__cta">{BOOKBTN('Book a deep clean', 'btn--dark', ' data-book="deep"')}<a class="link-u" href="services.html#deep">See what is included</a></div>
            </article>

            <aside class="art__side" aria-label="Book a cleaning">
              <div class="side-card">
                <span class="art__label">Ready for a reset?</span>
                <h3>Deep cleans from <b>$159</b></h3>
                <p>Fixed price, eco-safe products and a 100% satisfaction guarantee.</p>
                {BOOKBTN('Get a quote', 'btn--lime', ' data-book="deep"')}
              </div>
            </aside>
          </div>
        </div>
      </section>

      <!-- ===== RELATED ===== -->
      <section class="section blist blist--rel" aria-labelledby="rel-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="blist__top">
            {pg_head('Keep reading', 'More from the blog', 'rel-title')}
            <a class="link-u" href="blog.html">View all articles</a>
          </div>
          <div class="bgrid">{related}
          </div>
        </div>
      </section>
'''
    return page('How often should you deep clean your home? | Clevaro Blog', 'A deep clean is a reset, not a bigger weekly tidy. Here is how often your home needs one and what to include.', 'blog',
                hero, body + band('A cleaner home is <em>one booking away.</em>', 'Choose your service, pick a time and we will confirm by email within two hours.'))

# ============================== FAQ ==============================
FAQ_GROUPS = [
    ('general', 'General', 'The basics', 'How Clevaro works and what to expect on the day.', [
        ('How long does a visit take?', 'A regular clean of a two-bedroom home usually takes two to three hours. Deep cleans and move-out cleans take four to seven hours depending on size and condition. We give you a time window when we confirm.'),
        ('Do I need to be home?', 'No. Many clients give us a key, a door code or a lockbox. If you prefer to be there, that is fine too. Either way you will get a message when we arrive and when we finish.'),
        ('Do you bring your own supplies and equipment?', 'Yes. We bring everything, including eco-safe, allergen-aware products and professional equipment. If you would like us to use something specific, add it to your booking notes.'),
        ('Which areas do you cover?', 'We cover Portland and the surrounding suburbs. Enter your address in the booking form and we will confirm coverage straight away.'),
        ('Are your cleaners vetted and insured?', 'Every cleaner is background-checked, trained in our room-by-room method and covered by our liability insurance before their first visit.'),
    ]),
    ('booking', 'Booking', 'Booking & scheduling', 'Choosing a time, changing plans and recurring visits.', [
        ('How do I book a cleaning?', 'Use the Book a Cleaning button on any page. Choose your service and home size, pick a date and time, and add your details. We confirm by email within two hours.'),
        ('Can I change or cancel a booking?', 'Yes. You can reschedule or cancel free of charge up to 24 hours before your visit. Recurring plans can be paused or changed at any time.'),
        ('Can I get the same cleaner each time?', 'We aim to send the same small team to every recurring visit so they get to know your home. If you have a favourite, tell us and we will request them.'),
        ('How far ahead should I book?', 'Most slots are available within a few days. Weekends and the end of the month fill up quickly, so book a week ahead if you need a specific day.'),
        ('Do you offer same-day cleaning?', 'Sometimes. Call us on +1 (628) 555-0147 and we will check what is available that day.'),
    ]),
    ('pricing', 'Pricing', 'Pricing & payment', 'How prices are set and when you pay.', [
        ('How is the price worked out?', 'Prices start from the size of your home and the service you choose. We confirm a fixed price after a quick review of your space, so there are no surprises on the day.'),
        ('When do I pay?', 'No payment is taken when you book. You pay after the clean, once you have seen the result.'),
        ('Do recurring plans cost less?', 'Yes. Weekly visits save 15%, bi-weekly 10% and monthly 5% on every visit, and you can pause or cancel at any time.'),
        ('Are there any extra or hidden fees?', 'No. The price we confirm is the price you pay. Add-ons such as inside the oven are listed on the pricing page and only added when you ask.'),
        ('Which payment methods do you accept?', 'We accept all major cards and bank transfer. You will receive a receipt by email after every visit.'),
    ]),
    ('safety', 'Products & safety', 'Products & safety', 'What we use in your home and how we look after it.', [
        ('Are your products safe for kids and pets?', 'We use eco-safe, allergen-aware products and follow label guidance on every surface. If anyone in your home has a sensitivity, tell us and we will adjust.'),
        ('Can you use my own products?', 'Of course. Add a note to your booking and leave the products where we can find them.'),
        ('What if something gets damaged?', 'It is rare, but if it happens tell us straight away. Our liability insurance covers accidental damage caused during a visit.'),
        ('What if I am not happy with the result?', 'Tell us within 24 hours and we will come back and re-clean the areas you are not happy with at no charge. That is our 100% satisfaction guarantee.'),
    ]),
]

def qa_list(items, first_open=False):
    return ''.join(f'<details class="qa"{" open" if (i == 0 and first_open) else ""}><summary>{q}</summary><p class="qa__a">{a}</p></details>' for i, (q, a) in enumerate(items))

def faq():
    nav = ''.join(f'<a href="#{k}">{lab}</a>' for k, lab, *_ in FAQ_GROUPS)
    groups = ''
    for i, (k, lab, title, desc, items) in enumerate(FAQ_GROUPS):
        groups += f'''
      <section class="section faq faq--g" id="{k}" aria-labelledby="{k}-title" data-faq-group>
        {LINES.format(c='')}
        <div class="container">
          <div class="faq__row">
            <div class="faq__aside">
              <div class="pg-head">
                <span class="eyebrow">0{i + 1} — {lab}</span>
                <h2 class="h2" id="{k}-title" data-split="words">{title}</h2>
              </div>
              <p data-r>{desc}</p>
            </div>
            <div class="faq__list" data-r>{qa_list(items, i == 0)}</div>
          </div>
        </div>
      </section>
'''
    search = f'''
      <section class="faq-search" aria-label="Search the FAQ">
        {LINES.format(c='')}
        <div class="container">
          <div class="faq-search__row">
            <div class="faq-search__box" data-r>
              <label class="sr-only" for="faq-q">Search questions</label>
              <input id="faq-q" type="search" placeholder="Search questions, e.g. “cancel”, “pets”, “price”" autocomplete="off" data-faq-search>
              <span class="faq-search__count" data-faq-count aria-live="polite"></span>
            </div>
          </div>
          <p class="bempty" data-faq-empty hidden>No questions match your search. Try another word, or <a class="link-u" href="contact.html">ask us directly</a>.</p>
        </div>
      </section>
'''
    hero = phero('assets/images/services/move-in-out.jpg', 'FAQ', 'Questions, <em>answered.</em>',
                 'Everything you need to know about booking, pricing and what happens on the day.', BOOKBTN())
    sub = f'''
      <div class="subnav-wrap"><nav class="subnav" aria-label="On this page">{nav}</nav></div>
'''
    end = f'''
      <section class="section help" aria-labelledby="help-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="help__row">
            <div class="help__copy">
              <span class="eyebrow">Still need a hand?</span>
              <h2 class="h2" id="help-title" data-split="words">Talk to a real person.</h2>
            </div>
            <div class="help__cards" data-r-group>
              <a class="help__card" href="tel:+16285550147"><span>Call us</span><b>+1 (628) 555-0147</b><small>Mon–Sat, 8am–6pm</small></a>
              <a class="help__card" href="mailto:hello@clevaro.com"><span>Email us</span><b>hello@clevaro.com</b><small>Reply within two hours</small></a>
            </div>
          </div>
        </div>
      </section>
'''
    return page('FAQ — Booking, Pricing & Safety | Clevaro', 'Answers to common questions about booking a cleaning, pricing, products, safety and our satisfaction guarantee.', 'faq',
                hero, sub + search + groups + end + band('A cleaner home is <em>one booking away.</em>', 'Choose your service, pick a time and we will confirm by email within two hours. Free, no-obligation quote.'))

# ============================== PRICING ==============================
P = {'regular': (89, 119, 149, 189), 'deep': (159, 209, 269, 339), 'move': (189, 249, 319, 399), 'office': (99, 149, 199, 259)}
SIZES = [('s', 'Studio / 1 bed', 'Studio / 1 bedroom', 'up to 750 sq ft'), ('m', '2 beds', '2 bedrooms', 'up to 1,100 sq ft'),
         ('l', '3 beds', '3 bedrooms', 'up to 1,600 sq ft'), ('xl', '4+ beds', '4+ bedrooms', 'up to 2,400 sq ft')]

def pricing():
    size_btns = ''.join(f'<label class="chip chip--radio"><input type="radio" name="psize" value="{k}"{" checked" if k == "m" else ""}><span>{short}</span></label>' for k, short, *_ in SIZES)
    plans = [
        ('One-time', 'once', 0, 'A single visit when you need it.', ['Full regular clean', 'Eco-safe products and equipment', 'Satisfaction guarantee', 'No commitment'], False),
        ('Monthly', 'monthly', 5, 'A fresh start every month.', ['Everything in One-time', 'Same trusted team', 'Priority scheduling', 'Pause or cancel anytime'], False),
        ('Bi-weekly', 'biweekly', 10, 'The sweet spot for most homes.', ['Everything in Monthly', 'Save 10% on every visit', 'Free reschedule up to 24h', 'Add-ons at member rates'], True),
        ('Weekly', 'weekly', 15, 'Always-ready, effortlessly clean.', ['Everything in Bi-weekly', 'Save 15% on every visit', 'Dedicated cleaner', 'Free add-on each quarter'], False),
    ]
    pc = ''
    for name, fid, off, desc, feats, pop in plans:
        base = P['regular'][1]
        price = round(base * (1 - off / 100))
        ck = ''.join(f'<li>{f}</li>' for f in feats)
        badge = '<span class="plan__badge">Most popular</span>' if pop else ''
        save = f'<span class="plan__save">Save {off}%</span>' if off else '<span class="plan__save plan__save--none">Standard rate</span>'
        btn = BOOKBTN('Choose ' + name.lower(), 'btn--lime' if pop else 'btn--dark', f' data-book="regular" data-freq="{fid}"')
        pc += f'''
            <article class="plan{' plan--pop' if pop else ''}" data-off="{off}">
              <div class="plan__top"><h3 class="plan__name">{name}</h3>{badge}</div>
              <p class="plan__desc">{desc}</p>
              <div class="plan__price"><small>from</small><b data-plan-price>${price}</b><small>/ visit</small></div>
              {save}
              <ul class="checks checks--one">{ck}</ul>
              {btn}
            </article>'''
    rows = ''.join(f'<tr><th scope="row">{n}<small>{sub}</small></th>' + ''.join(f'<td><small>from </small>${P[k][i]}</td>' for k in ('regular', 'deep', 'move', 'office')) + '</tr>' for i, (_, _s, n, sub) in enumerate(SIZES))
    addons = [('Inside the oven', '$35', 'Degreased racks, door glass and cavity.'), ('Inside the fridge', '$30', 'Shelves, drawers and seals wiped clean.'),
              ('Interior windows', 'from $39', 'Glass, frames and tracks, priced by window count.'), ('Wash & fold laundry', '$25', 'One load washed, dried and folded.'),
              ('Cabinet interiors', '$40', 'Kitchen cabinets emptied, wiped and reset.'), ('Pet-hair treatment', '$30', 'Extra attention on sofas, beds and floors.'),
              ('Balcony or patio', '$35', 'Swept, wiped and furniture refreshed.'), ('Wall spot-cleaning', '$25', 'Marks and scuffs removed from painted walls.')]
    ad = ''.join(f'''
            <article class="addon"><div class="addon__top"><h3>{n}</h3><b>{p}</b></div><p>{c}</p><button class="link-u" type="button" data-book="regular" data-focus="{n}">Add to a booking</button></article>''' for n, p, c in addons)
    pfaq = [('Is there a contract?', 'No. Recurring plans can be paused, changed or cancelled at any time. We only ask for 24 hours’ notice before a visit.'),
            ('How do the prices work for bigger homes?', 'Choose your size above to see the starting price. For very large or heavily lived-in homes we confirm a fixed price after a quick review.'),
            ('When do I pay?', 'No payment is taken when you book. You pay after the clean, once you have seen the result.'),
            ('What is included in a regular clean?', 'Dusting, vacuuming and mopping, kitchen and bathroom clean, bed making and a tidy of every room. See the full checklist on the services page.')]
    hero = phero('assets/images/hero/hero-bg.jpg', 'Pricing', 'Simple pricing, <em>spotless results.</em>',
                 'Clear starting prices, no hidden fees and no payment until the job is done. Recurring plans save up to 15% on every visit.', BOOKBTN())
    body = f'''
      <!-- ===== PLANS ===== -->
      <section class="section plans-sec" id="plans" aria-labelledby="plans-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="plans__top">
            {pg_head('Plans', 'Pick the rhythm that suits your home', 'plans-title', 'Prices below are for a regular clean. Choose your home size to update them.')}
            <fieldset class="plans__size"><legend class="sr-only">Home size</legend><div class="chips" data-size-chips>{size_btns}</div></fieldset>
          </div>
          <div class="plans__grid" data-r-group data-plans>{pc}
          </div>
          <p class="plans__note" data-r>Prices are starting estimates for homes in standard condition. We confirm a fixed price after a quick review of your space.</p>
        </div>
      </section>

      <!-- ===== SERVICE TABLE ===== -->
      <section class="section price" id="rates" aria-labelledby="price-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          {pg_head('Every service', 'Starting prices by service and size', 'price-title', 'Deep cleans, move-in / move-out and office cleaning, side by side.')}
          <div class="price__wrap" data-r>
            <table class="ptable">
              <thead><tr><th scope="col">Size of space</th><th scope="col">Regular</th><th scope="col">Deep</th><th scope="col">Move-In / Out</th><th scope="col">Office</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
          <div class="price__note" data-r>
            <p>Recurring plans apply to regular and office cleaning. Deep and move-in / move-out cleans are one-time services.</p>
            <div class="save"><span>Weekly <b>−15%</b></span><span>Bi-weekly <b>−10%</b></span><span>Monthly <b>−5%</b></span></div>
          </div>
        </div>
      </section>

      <!-- ===== ADD-ONS ===== -->
      <section class="section addons" id="addons" aria-labelledby="addons-title">
        {LINES.format(c='')}
        <div class="container">
          {pg_head('Add-ons', 'Extras for the details that matter', 'addons-title', 'Add any of these to a booking. Prices are per visit.')}
          <div class="addons__grid" data-r-group>{ad}
          </div>
        </div>
      </section>

      <!-- ===== PRICING FAQ ===== -->
      <section class="section faq" id="faq" aria-labelledby="faq-title">
        {LINES.format(c='')}
        <div class="container">
          <div class="faq__row">
            <div class="faq__aside">
              <div class="pg-head">
                <span class="eyebrow">Pricing FAQ</span>
                <h2 class="h2" id="faq-title" data-split="words">Good to know.</h2>
              </div>
              <p data-r>More questions? Browse the <a class="link-u" href="faq.html">full FAQ</a> or call us on <a class="link-u" href="tel:+16285550147">+1 (628) 555-0147</a>.</p>
              {BOOKBTN('Book a Cleaning', 'btn--dark')}
            </div>
            <div class="faq__list" data-r>{qa_list(pfaq, True)}</div>
          </div>
        </div>
      </section>
'''
    return page('Pricing & Plans — Clevaro Home Cleaning', 'Transparent starting prices for regular, deep and move-in cleaning. Recurring plans save up to 15%. No payment until the job is done.', 'pricing',
                hero, body + band('Get your fixed price <em>in two minutes.</em>', 'Choose your service, pick a time and we will confirm a fixed price by email within two hours.'))

# ============================== CONTACT ==============================
def contact():
    info = [('Call us', '+1 (628) 555-0147', 'tel:+16285550147', 'Mon–Sat, 8am–6pm'),
            ('Email us', 'hello@clevaro.com', 'mailto:hello@clevaro.com', 'We reply within two hours'),
            ('Visit us', '24 Maple Avenue, Portland, OR 97205', '', 'By appointment only'),
            ('Opening hours', 'Mon–Sat, 8am–6pm', '', 'Closed on Sundays')]
    ic = ''.join(f'''
            <article class="cinfo"><span class="cinfo__label">{l}</span>{f'<a class="cinfo__val" href="{h}">{v}</a>' if h else f'<span class="cinfo__val">{v}</span>'}<span class="cinfo__sub">{s}</span></article>''' for l, v, h, s in info)
    areas = ['Pearl District', 'Alberta Arts', 'Hawthorne', 'Sellwood', 'Nob Hill', 'Lake Oswego', 'Beaverton', 'Tigard', 'Gresham']
    ar = ''.join(f'<li>{a}</li>' for a in areas)
    hero = phero('assets/images/footer/footer-bg.jpg', 'Contact', 'Let’s talk about <em>your home.</em>',
                 'Questions, quotes or a special request? Send us a message and a real person will get back to you within two hours.', BOOKBTN())
    body = f'''
      <!-- ===== INFO ===== -->
      <section class="section cinfo-sec" aria-label="Contact details">
        {LINES.format(c='')}
        <div class="container">
          <div class="cinfo__grid" data-r-group="fade">{ic}
          </div>
        </div>
      </section>

      <!-- ===== FORM ===== -->
      <section class="section cform-sec" id="message" aria-labelledby="cform-title">
        {LINES.format(c=' on-white')}
        <div class="container">
          <div class="cform__row">
            <div class="cform__aside">
              <div class="pg-head">
                <span class="eyebrow">Send a message</span>
                <h2 class="h2" id="cform-title" data-split="words">How can we help?</h2>
                <p data-r>Tell us a little about your home and what you need. For a faster quote, use the booking form and we will confirm a fixed price by email.</p>
              </div>
              {BOOKBTN('Book a Cleaning', 'btn--dark')}
              <div class="area" data-r>
                <span class="art__label">Areas we cover</span>
                <ul>{ar}</ul>
              </div>
            </div>
            <div class="cform" data-r>
              <form class="cf" data-contact-form novalidate>
                <div class="cf__row">
                  <div class="cf__field"><label for="cf-name">Full name</label><input id="cf-name" name="name" type="text" autocomplete="name" required><span class="cf__err" data-err="name"></span></div>
                  <div class="cf__field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required><span class="cf__err" data-err="email"></span></div>
                </div>
                <div class="cf__row">
                  <div class="cf__field"><label for="cf-phone">Phone <em>(optional)</em></label><input id="cf-phone" name="phone" type="tel" autocomplete="tel"></div>
                  <div class="cf__field"><label for="cf-topic">What is this about?</label>
                    <select id="cf-topic" name="topic" required><option value="">Select a topic</option><option>New booking or quote</option><option>Existing booking</option><option>Office or commercial cleaning</option><option>Feedback</option><option>Something else</option></select>
                    <span class="cf__err" data-err="topic"></span></div>
                </div>
                <div class="cf__field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" rows="5" required placeholder="Tell us about your home, the service you need and any dates in mind."></textarea><span class="cf__err" data-err="message"></span></div>
                <button class="btn btn--dark" type="submit">Send message{ARROW('dark')}</button>
                <p class="cf__fine">We only use your details to reply to your message.</p>
              </form>
              <div class="cf__ok" data-contact-ok hidden tabindex="-1">
                <span class="cf__tick" aria-hidden="true"></span>
                <h3>Message sent</h3>
                <p>Thank you, <b data-ok-name></b>. We will reply to <b data-ok-email></b> within two hours during opening hours.</p>
                <button class="link-u" type="button" data-contact-again>Send another message</button>
              </div>
            </div>
          </div>
        </div>
      </section>
'''
    return page('Contact Clevaro — Home Cleaning in Portland', 'Get in touch with Clevaro for quotes, bookings and questions. Call, email or send a message and we will reply within two hours.', 'contact',
                hero, body + band('Prefer to book <em>straight away?</em>', 'Choose your service, pick a time and we will confirm by email within two hours. Free, no-obligation quote.'))

for name, fn in (('blog', blog), ('blog-single', blog_single), ('faq', faq), ('pricing', pricing), ('contact', contact)):
    (ROOT / f'{name}.html').write_text(fn())
print('ok')
