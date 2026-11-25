# CLEVARO — Home Cleaning Website

A premium home-cleaning company site, rebuilt from the layout, spacing, typography and motion of the Miyerd Webflow template, with CLEVARO content.

Plain HTML, CSS and JavaScript. There is no build step. Open `index.html` through any static server (for example `python -m http.server` in this folder, then visit `http://localhost:8000`). Opening the file directly also works, but a server is recommended for fonts.

## Folder structure

```
CLEVARO/
├─ index.html              Homepage (9 sections, in the reference's order)
├─ about.html              About us: story, stats, values, team
├─ services.html           Service details, room specialities, pricing, FAQ
├─ css/
│  ├─ base.css             Design tokens, fonts, reset, layout primitives
│  ├─ components.css       Header, menu overlay, buttons, split-text helpers
│  ├─ sections.css         One block per section (hero → footer)
│  ├─ responsive.css       Breakpoints: 1280 · 991 · 767 · 479
│  ├─ pages.css            About + Services page styles
│  └─ booking.css          Booking popup styles
├─ js/
│  ├─ smooth-scroll.js     Lenis smooth scroll wired into GSAP ScrollTrigger
│  ├─ menu.js              Full-screen menu overlay
│  ├─ slider.js            Testimonial slider (autoplay + avatar buttons)
│  ├─ animations.js        Homepage entrance and scroll animations
│  ├─ inner.js             Motion for about.html / services.html
│  ├─ booking.js           Booking popup (opens from any [data-book] button)
│  └─ vendor/              GSAP, ScrollTrigger, SplitText, Lenis (local copies)
└─ assets/
   ├─ fonts/               Manrope (variable, latin + latin-ext)
   ├─ icons/               SVG icons, logo mark, decorative sparkles
   └─ images/              hero · about · services · categories · testimonials
                           · blog · cta · footer
```

## Replacing the image placeholders

Every file in `assets/images/` is a correctly sized placeholder showing its size and role (for example `HERO BACKGROUND 2400x1500`). To use real photography, save your photo over the file with the **same name and size ratio**. No code changes are needed.

| File | Size | What to show |
| --- | --- | --- |
| `hero/hero-bg.jpg` | 2400×1500 | Professional cleaner working in a bright, modern home |
| `about/about-1.jpg` | 648×816 | Cleaner at work (portrait) |
| `about/about-2.jpg` | 646×560 | Mopping, or a spotless floor |
| `services/*.jpg` | 2480×1100 | Regular, deep and move-in/move-out cleaning |
| `categories/*.jpg` | 939 wide | Kitchen, bathroom, apartment, office |
| `testimonials/avatar-1…6.jpg` | 436×438 | Client portraits |
| `blog/*.jpg` | 646–848 wide | Cleaning guides |
| `cta/cta-bg.jpg` | 2400×1000 | Bright, spotless living room |
| `footer/footer-bg.jpg` | 2400×1600 | Cleaner portrait |

## Animation notes

- **Smooth scroll:** Lenis (1.5s duration, cubic ease-out), driven by the GSAP ticker.
- **Text:** SplitText masked reveals on the hero, section headings and footer.
- **Hero:** background zoom-out, parallax, floating glass circle, staggered card entrance.
- **Services:** sticky stacked cards that scale and dim as the next card arrives.
- **How it works:** a sticky row where the three staircase cards rise in as you scroll.
- **Other sections:** clip-path image reveals, staggered category and blog cards, parallax backgrounds, a looping testimonial slider.
- `prefers-reduced-motion` turns the animations and smooth scroll off.

## Placeholder content to replace

- Phone `+1 (628) 555-0147`, email `hello@clevaro.com` and the Portland address in the footer are sample values.
- Social links, "Read More" links and the legal links point to `#`.
- The newsletter form validates and confirms on the page only. It is not connected to a mailing service.

## Booking popup

`js/booking.js` builds the popup and opens it from any element with `data-book`:

- `<button data-book>` opens it on step 1.
- `data-book="deep"` pre-selects a service (`regular`, `deep`, `move`, `office`).
- `data-focus="Kitchen"` pre-fills the notes with "Focus area: Kitchen."
- Adding `#book` to any page URL opens it on load.

The form validates and shows a confirmation on the page. To actually receive bookings, set `BOOKING_ENDPOINT` at the top of `booking.js` to a form service URL (Formspree, Basin, your own API). The booking is then POSTed there as JSON. The starting prices live in `PRICES` in the same file and must match the table in `services.html`.

## Sample content to replace on the new pages

Team names and photos, the founder quote, the stats (1k+ homes, 35+ cleaners), service durations, starting prices and FAQ answers are all sample values.

## More pages
`blog.html` (topic filter), `blog-single.html` (article template), `faq.html` (live search), `pricing.html` (prices follow the chosen home size) and `contact.html` (validated form). The contact form only confirms on the page until you set `CONTACT_ENDPOINT` in `js/extra.js`. Blog posts, prices, hours and the address are sample content to replace. Shared markup (header, menu, footer) is generated from `build.py` / `build2.py` if you keep the generator, otherwise edit each page.

## Page generators
`tools/build.py` (About, Services) and `tools/build2.py` (Blog, Single post, FAQ, Pricing, Contact) regenerate those HTML pages from shared header/footer partials. Run `python3 tools/build.py && python3 tools/build2.py` from the repo root. `index.html` is edited by hand.
