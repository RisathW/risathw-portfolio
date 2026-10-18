const $ = s => document.querySelector(s);

// theme: dark by default, light on request; remembered (and shared with the story page)
(function () {
  const root = document.documentElement, btn = $('#theme');
  const apply = t => {
    root.dataset.theme = t;
    if (btn) btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    // logos that are white on dark get a dark version on the light theme
    document.querySelectorAll('img[data-light]').forEach(img => {
      if (!img.dataset.dark) img.dataset.dark = img.getAttribute('src');
      img.src = t === 'light' ? img.dataset.light : img.dataset.dark;
    });
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = t === 'dark' ? '#000000' : '#ececec';
  };
  let saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  apply(saved === 'light' ? 'light' : 'dark');
  if (btn) btn.addEventListener('click', () => {
    const next = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.classList.add('theme-switching');   // the photo's shading changes instantly instead of easing
    apply(next);
    setTimeout(() => root.classList.remove('theme-switching'), 80);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
})();

// loading screen: counts up while the page loads, then slides away
(function () {
  const loader = $('#loader'), bar = $('#ld-bar'), num = $('#ld-num');
  if (!loader) return;
  document.documentElement.classList.add('is-loading', 'hero-wait');
  const MIN = 1400, MAX = 8000, t0 = performance.now();
  let shown = 0, loaded = document.readyState === 'complete', done = false;
  window.addEventListener('load', () => { loaded = true; });
  const finish = () => {
    if (done) return; done = true;
    loader.classList.add('out');
    document.documentElement.classList.remove('is-loading');
    setTimeout(() => document.documentElement.classList.remove('hero-wait'), 350); // hero entrance starts as the loader lifts
    setTimeout(() => loader.remove(), 1100);
  };
  const tick = now => {
    const t = now - t0;
    // eases towards 90% while loading, jumps to 100% once the page has loaded
    const target = loaded && t > MIN ? 100 : Math.min(90, (t / MIN) * 90);
    shown += (target - shown) * 0.12;
    if (target === 100 && shown > 99.2) shown = 100;
    bar.style.transform = `scaleX(${shown / 100})`;
    num.textContent = Math.round(shown);
    if (shown >= 100 || t > MAX) { num.textContent = 100; bar.style.transform = 'scaleX(1)'; setTimeout(finish, 250); return; }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  setTimeout(finish, MAX + 600); // safety net, e.g. when the tab is in the background
})();

// full-screen menu behind the four dots
const btn = $('#menu-btn'), overlay = $('#overlay');
const setMenu = open => {
  overlay.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', open);
  overlay.setAttribute('aria-hidden', !open);
};
btn.addEventListener('click', () => setMenu(!overlay.classList.contains('open')));
overlay.addEventListener('click', e => { if (e.target.tagName === 'A') setMenu(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

// showcase tabs
const items = [
  { tag: 'Digital infrastructure', text: 'Fortechz: architecting elite digital infrastructure, from software development to IT infrastructure management.', link: 'https://fortechz.com/', label: 'Visit Fortechz', img: 'assets/screenshots/fortechz.jpg' },
  { tag: 'Web design & development', text: 'A warm, play-based preschool in Matara, open since 2000, now with a site for programs, teachers, gallery and visit booking. Designed and built at Fortechz.', link: 'https://sakura-pre-school.vercel.app/', label: 'View live', img: 'assets/screenshots/sakura.jpg' },
  { tag: 'Brand & graphic design', text: 'ArtifeX Designs: brand identities, banners and social graphics that turn ideas into powerful visual stories.', link: 'https://risathw.github.io/artifex.github.io/#home', label: 'View portfolio', img: 'assets/screenshots/artifex.jpg' },
  { tag: 'Photography', text: 'City nights, street life and festival lights, shot around Colombo and shared as @risathxclicks.', link: 'https://www.instagram.com/risathxclicks/', label: 'Open Instagram', img: 'assets/photography/dsc03472.jpg' }
];
const FZ_URL = 'https://fortechz.com/', AX_URL = 'https://risathw.github.io/artifex.github.io/#home';
const brandLinks = t => t
  .replace(/\b(Fortechz|ForTechZ)\b/g, `<a class="bl" href="${FZ_URL}" target="_blank" rel="noopener">$1</a>`)
  .replace(/\bArtifeX(?: Visual Studio| Designs)?/g, m => `<a class="bl" href="${AX_URL}" target="_blank" rel="noopener">${m}</a>`);
const sImg = $('#s-img'), sLink = $('#s-link');
$('#thumbs').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  const it = items[b.dataset.i];
  document.querySelectorAll('#thumbs button').forEach(x => x.classList.toggle('on', x === b));
  $('#s-tag').textContent = it.tag;
  $('#s-text').innerHTML = brandLinks(it.text);
  sLink.innerHTML = it.label + ' <b>↗</b>';
  sLink.href = it.link;
  if (it.link.startsWith('#')) sLink.removeAttribute('target'); else sLink.target = '_blank';
  sImg.style.opacity = 0;
  setTimeout(() => { sImg.src = it.img; sImg.style.opacity = 1; }, 200);
});

// certificates carousel
const rec = $('#rec');
const step = () => rec.firstElementChild.getBoundingClientRect().width + 40;
$('#next').addEventListener('click', () => rec.scrollBy({ left: step(), behavior: 'smooth' }));
$('#prev').addEventListener('click', () => rec.scrollBy({ left: -step(), behavior: 'smooth' }));

// loop the two marquees seamlessly
['#m-track'].forEach(s => { const t = $(s); if (t) t.innerHTML += t.innerHTML; });

// reveal on scroll
const els = document.querySelectorAll('.sec > *, .steps article, .gal > *, .photo-grid > *, .feat article, .repos a, .foot > *');
els.forEach(e => e.classList.add('reveal'));
const io = new IntersectionObserver(es => es.forEach(x => {
  if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); }
}), { threshold: 0.06 });
els.forEach(e => io.observe(e));

// lightbox for the visual portfolio
const lb = $('#lightbox'), lbImg = lb.querySelector('img');
document.querySelectorAll('.gal, .photo-grid').forEach(g => g.addEventListener('click', e => {
  const f = e.target.closest('.g-img'); if (!f) return;
  lbImg.src = f.dataset.full; lbImg.alt = f.querySelector('img').alt;
  lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
}));
const closeLb = () => { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); };
lb.addEventListener('click', closeLb);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLb(); });

