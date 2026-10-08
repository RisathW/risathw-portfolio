const root = document.documentElement;
const themeBtn = document.getElementById('theme');

// theme: dark by default, remembered when storage is available
const apply = t => {
  root.dataset.theme = t;
  themeBtn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = t === 'dark' ? '#0f0f0f' : '#ececec';
};
try { const saved = localStorage.getItem('theme'); if (saved === 'light' || saved === 'dark') apply(saved); } catch (e) {}
themeBtn.addEventListener('click', () => {
  const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
  apply(next);
  try { localStorage.setItem('theme', next); } catch (e) {}
});

// share links use the page's own address
const url = encodeURIComponent(location.href.split('#')[0]);
const text = encodeURIComponent(document.title);
const shareX = document.getElementById('share-x'), shareIn = document.getElementById('share-in');
if (shareX) shareX.href = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
if (shareIn) shareIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;

// gentle reveal on scroll
const els = document.querySelectorAll('.back, .tags, h1, .date, .feature, .prose p, .prose h2, .prose .timeline, .prose blockquote, .share, .proj');
els.forEach(e => e.classList.add('reveal'));
const io = new IntersectionObserver(es => es.forEach(x => {
  if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); }
}), { threshold: 0.08 });
els.forEach(e => io.observe(e));

// full-screen menu behind the four dots (same as the main page)
const btn = document.getElementById('menu-btn'), overlay = document.getElementById('overlay');
const setMenu = open => {
  overlay.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', open);
  overlay.setAttribute('aria-hidden', !open);
};
btn.addEventListener('click', () => setMenu(!overlay.classList.contains('open')));
overlay.addEventListener('click', e => { if (e.target.tagName === 'A') setMenu(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
