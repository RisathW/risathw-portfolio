"""Regenerates every SEO file that needs the site's public address.

Usage:  python build-seo.py
Edit the address in seo.config.json first (siteUrl), then run this again.

It rewrites:
  - the block between <!-- seo:start --> and <!-- seo:end --> in index.html
    (canonical link, og:url, absolute og/twitter image links, JSON-LD for Google)
  - sitemap.xml (page + image sitemap with titles)
  - robots.txt (points crawlers at the sitemap)
"""
import json, os, re, html
from datetime import date
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(ROOT, "seo.config.json"), encoding="utf-8"))
BASE = cfg["siteUrl"].rstrip("/") + "/"
TODAY = date.today().isoformat()


def url(path):
    return BASE + path.lstrip("/")


page = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# ---- collect images + alt text straight from the page -------------------------------------
images = []
seen = set()
for m in re.finditer(r"<img\b[^>]*>", page):
    tag = m.group(0)
    src = re.search(r'src="(assets/(?:work|photography|screenshots|images|brand)/[^"]+)"', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    if not src or src.group(1) in seen:
        continue
    seen.add(src.group(1))
    images.append((src.group(1), html.unescape(alt.group(1)) if alt and alt.group(1) else ""))
# the OG card and portrait first
images = [i for i in images if "og-image" not in i[0]]
images.insert(0, ("assets/brand/og-image.png", "Risath Athsara Wijethunga, co-founder of Fortechz"))
gallery = [i for i in images if i[0].startswith("assets/work/")]
photos = [i for i in images if i[0].startswith("assets/photography/")]

# ---- JSON-LD ------------------------------------------------------------------------------
PERSON = url("#risath")
ORG = url("#fortechz")
desc = re.search(r'<meta name="description" content="([^"]*)"', page).group(1)
same_as = [
    "https://www.linkedin.com/in/risath-athsara-wijethunga-007844340/",
    "https://github.com/RisathW",
    "https://www.instagram.com/risathxclicks/",
    "https://www.instagram.com/itz.r1sath",
    "https://www.facebook.com/profile.php?id=100069518536727",
]


def image_objects(items, creator_id):
    return [{"@type": "ImageObject", "contentUrl": url(p), "name": a or os.path.basename(p),
             "caption": a or os.path.basename(p), "creator": {"@id": creator_id}} for p, a in items]


graph = [
    {"@type": "WebSite", "@id": url("#website"), "url": BASE, "name": "Risath Athsara Wijethunga",
     "description": desc, "inLanguage": "en", "publisher": {"@id": PERSON}},
    {"@type": "ProfilePage", "@id": url("#profile"), "url": BASE, "name": "Risath Athsara Wijethunga | Co-Founder of Fortechz",
     "isPartOf": {"@id": url("#website")}, "mainEntity": {"@id": PERSON}, "dateModified": TODAY,
     "primaryImageOfPage": {"@type": "ImageObject", "url": url("assets/brand/og-image.png"), "width": 1200, "height": 630}},
    {"@type": "Person", "@id": PERSON, "name": "Risath Athsara Wijethunga",
     "alternateName": ["Risath Wijethunga", "R.W", "risathxclicks"],
     "jobTitle": "Co-Founder of Fortechz", "description": desc,
     "url": BASE, "image": url("assets/brand/og-image.png"),
     "email": "mailto:risathwijethunga@gmail.com",
     "telephone": "+94704604737",
     "address": {"@type": "PostalAddress", "addressLocality": "Matara", "addressRegion": "Southern Province", "addressCountry": "LK"},
     "worksFor": {"@id": ORG},
     "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Curtin University"},
                  {"@type": "CollegeOrUniversity", "name": "SLIIT City Uni"},
                  {"@type": "School", "name": "Rahula College Matara"}],
     "hasCredential": [
         {"@type": "EducationalOccupationalCredential", "name": "President's Scout Award", "recognizedBy": {"@type": "Organization", "name": "Sri Lanka Scout Association"}},
         {"@type": "EducationalOccupationalCredential", "name": "AI/ML Engineer - Stage 1", "recognizedBy": {"@type": "Organization", "name": "SLIIT"}},
         {"@type": "EducationalOccupationalCredential", "name": "Red Hat System Administration I (RH124)", "recognizedBy": {"@type": "Organization", "name": "Red Hat"}}],
     "knowsAbout": ["Software development", "Digital infrastructure", "IT infrastructure management", "Cyber security", "Linux",
                    "Java", "JavaScript", "React", "Node.js", "PostgreSQL", "Graphic design", "Brand identity", "Photography"],
     "sameAs": same_as + ["https://fortechz.com/", "https://risathw.github.io/artifex.github.io/"]},
    {"@type": "Organization", "@id": ORG, "name": "Fortechz", "url": "https://fortechz.com/",
     "description": "Architecting elite digital infrastructure: software, websites and POS systems.",
     "founder": {"@id": PERSON}, "logo": url("assets/logos/ondark/fortechz.png")},
    {"@type": "ItemList", "name": "Projects built at Fortechz", "itemListElement": [
        {"@type": "ListItem", "position": 1, "item": {"@type": "SoftwareApplication", "name": "POS System",
            "description": "Point of sale system with checkout, stock control, staff and shift management and reports, as a Windows desktop app that also works on phones and tablets.",
            "applicationCategory": "BusinessApplication", "operatingSystem": "Windows", "creator": {"@id": ORG}}},
        {"@type": "ListItem", "position": 2, "item": {"@type": "WebSite", "name": "Sakura Pre-School", "url": "https://sakura-pre-school.vercel.app/",
            "description": "Website for a play-based preschool in Matara, Sri Lanka.", "creator": {"@id": ORG}}},
        {"@type": "ListItem", "position": 3, "item": {"@type": "WebSite", "name": "ArtifeX Designs", "url": "https://risathw.github.io/artifex.github.io/",
            "description": "Graphic design studio portfolio website.", "creator": {"@id": ORG}}},
        {"@type": "ListItem", "position": 4, "item": {"@type": "WebSite", "name": "DeTuch Fragrance", "url": "https://risathw.github.io/DeTuch_Fragrance/",
            "description": "Online fragrance storefront with WhatsApp ordering.", "creator": {"@id": ORG}}}]},
    {"@type": "ImageGallery", "name": "Visual portfolio: graphic design by Risath Athsara Wijethunga", "creator": {"@id": PERSON},
     "image": image_objects(gallery, PERSON)},
    {"@type": "ImageGallery", "name": "Photography by @risathxclicks", "creator": {"@id": PERSON},
     "image": image_objects(photos, PERSON)},
]
ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False).replace("</", "<\\/")

block = f"""<!-- seo:start (generated by build-seo.py, do not edit by hand) -->
<link rel="canonical" href="{BASE}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{url('assets/brand/og-image.png')}">
<meta property="og:image:secure_url" content="{url('assets/brand/og-image.png')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Risath Athsara Wijethunga, co-founder of Fortechz">
<meta name="twitter:image" content="{url('assets/brand/og-image.png')}">
<script type="application/ld+json">{ld}</script>
<!-- seo:end -->"""

if "<!-- seo:start" in page:
    page = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda _: block, page, flags=re.S)
else:  # first run: replace the older static tags
    page = re.sub(r'<meta property="og:image" content="[^"]*">\n', "", page)
    page = re.sub(r'<meta name="twitter:image" content="[^"]*">\n', "", page)
    page = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", page, flags=re.S)
    page = page.replace("</head>", block + "\n</head>", 1)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)

# ---- blog.html: canonical, Open Graph and BlogPosting JSON-LD ---------------------------------
blog_path = os.path.join(ROOT, "blog.html")
BLOG_URL = url("blog.html")
if os.path.exists(blog_path):
    b = open(blog_path, encoding="utf-8").read()
    b_title = re.search(r"<h1>(.*?)</h1>", b, re.S).group(1).strip()
    b_desc = re.search(r'<meta name="description" content="([^"]*)"', b).group(1)
    b_img = re.search(r'<figure class="feature">\s*<img src="([^"]+)"', b).group(1)
    b_date = re.search(r'<time datetime="([^"]+)"', b).group(1)
    posting = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": html.unescape(b_title),
               "description": html.unescape(b_desc), "datePublished": b_date, "dateModified": TODAY,
               "image": url(b_img), "mainEntityOfPage": BLOG_URL, "inLanguage": "en",
               "author": {"@type": "Person", "name": "Risath Athsara Wijethunga", "url": BASE},
               "publisher": {"@type": "Person", "name": "Risath Athsara Wijethunga", "url": BASE}}
    b_ld = json.dumps(posting, indent=1, ensure_ascii=False).replace("</", "<\\/")
    b_block = f"""<!-- seo:start (generated by build-seo.py, do not edit by hand) -->
<link rel="canonical" href="{BLOG_URL}">
<meta property="og:url" content="{BLOG_URL}">
<meta property="og:image" content="{url(b_img)}">
<meta name="twitter:image" content="{url(b_img)}">
<script type="application/ld+json">{b_ld}</script>
<!-- seo:end -->"""
    b = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda _: b_block, b, flags=re.S)
    open(blog_path, "w", encoding="utf-8").write(b)

# ---- social.html: canonical, Open Graph and WebPage JSON-LD ----------------------------------
social_path = os.path.join(ROOT, "social.html")
SOCIAL_URL = url("social.html")
social_images = []
if os.path.exists(social_path):
    sp = open(social_path, encoding="utf-8").read()
    s_desc = re.search(r'<meta name="description" content="([^"]*)"', sp).group(1)
    social_images = [(m.group(1), html.unescape(m.group(2))) for m in re.finditer(r'<img src="(assets/social/[^"]+)" alt="([^"]*)"', sp)]
    page_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Social projects | Risath Athsara Wijethunga",
               "description": html.unescape(s_desc), "url": SOCIAL_URL, "inLanguage": "en",
               "isPartOf": {"@type": "WebSite", "name": "Risath Athsara Wijethunga", "url": BASE},
               "author": {"@type": "Person", "name": "Risath Athsara Wijethunga", "url": BASE},
               "image": [url(p) for p, _ in social_images],
               "about": ["Community service", "Scouting", "President's Scout Award", "Blood donation", "Health camp", "Concert", "National Jamboree"]}
    s_ld = json.dumps(page_ld, indent=1, ensure_ascii=False).replace("</", "<\\/")
    s_block = f"""<!-- seo:start (generated by build-seo.py, do not edit by hand) -->
<link rel="canonical" href="{SOCIAL_URL}">
<meta property="og:url" content="{SOCIAL_URL}">
<meta property="og:image" content="{url(social_images[0][0]) if social_images else url('assets/brand/og-image.png')}">
<meta name="twitter:image" content="{url(social_images[0][0]) if social_images else url('assets/brand/og-image.png')}">
<script type="application/ld+json">{s_ld}</script>
<!-- seo:end -->"""
    sp = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda _: s_block, sp, flags=re.S)
    open(social_path, "w", encoding="utf-8").write(sp)

# ---- photography.html: canonical, Open Graph and ImageGallery JSON-LD ------------------------
photo_path = os.path.join(ROOT, "photography.html")
PHOTO_URL = url("photography.html")
photo_images = []
if os.path.exists(photo_path):
    pp = open(photo_path, encoding="utf-8").read()
    p_desc = re.search(r'<meta name="description" content="([^"]*)"', pp).group(1)
    seen_p = set()
    for m in re.finditer(r"<img\b[^>]*>", pp):
        t = m.group(0)
        src = re.search(r'src="(assets/photography/[^"]+)"', t)
        alt = re.search(r'alt="([^"]*)"', t)
        if src and src.group(1) not in seen_p:
            seen_p.add(src.group(1))
            photo_images.append((src.group(1), html.unescape(alt.group(1)) if alt else ""))
    p_ld = json.dumps({"@context": "https://schema.org", "@type": "ImageGallery", "name": "Photography | Risath Athsara Wijethunga",
                       "description": html.unescape(p_desc), "url": PHOTO_URL, "inLanguage": "en",
                       "isPartOf": {"@type": "WebSite", "name": "Risath Athsara Wijethunga", "url": BASE},
                       "creator": {"@type": "Person", "name": "Risath Athsara Wijethunga", "url": BASE},
                       "image": image_objects(photo_images, PERSON)}, indent=1, ensure_ascii=False).replace("</", "<\\/")
    p_img = url(photo_images[0][0]) if photo_images else url("assets/brand/og-image.png")
    p_block = f"""<!-- seo:start (generated by build-seo.py, do not edit by hand) -->
<link rel="canonical" href="{PHOTO_URL}">
<meta property="og:url" content="{PHOTO_URL}">
<meta property="og:image" content="{p_img}">
<meta name="twitter:image" content="{p_img}">
<script type="application/ld+json">{p_ld}</script>
<!-- seo:end -->"""
    if "<!-- seo:start" in pp:
        pp = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda _: p_block, pp, flags=re.S)
    else:
        pp = re.sub(r'<meta property="og:image" content="[^"]*">\n', "", pp)
        pp = pp.replace("</head>", p_block + "\n</head>", 1)
    open(photo_path, "w", encoding="utf-8").write(pp)

# ---- sitemap.xml (page + images) -----------------------------------------------------------
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
         "  <url>", f"    <loc>{escape(BASE)}</loc>", f"    <lastmod>{TODAY}</lastmod>",
         "    <changefreq>monthly</changefreq>", "    <priority>1.0</priority>"]
for p, a in images:
    if p.startswith("assets/brand/") and "og-image" not in p:
        continue
    lines += ["    <image:image>", f"      <image:loc>{escape(url(p))}</image:loc>"]
    if a:
        lines += [f"      <image:title>{escape(a)}</image:title>", f"      <image:caption>{escape(a)}</image:caption>"]
    lines += ["    </image:image>"]
lines += ["  </url>"]
if os.path.exists(blog_path):
    lines += ["  <url>", f"    <loc>{escape(BLOG_URL)}</loc>", f"    <lastmod>{TODAY}</lastmod>",
              "    <changefreq>yearly</changefreq>", "    <priority>0.7</priority>", "  </url>"]
if social_images:
    lines += ["  <url>", f"    <loc>{escape(SOCIAL_URL)}</loc>", f"    <lastmod>{TODAY}</lastmod>",
              "    <changefreq>yearly</changefreq>", "    <priority>0.6</priority>"]
    for p_, a_ in social_images:
        lines += ["    <image:image>", f"      <image:loc>{escape(url(p_))}</image:loc>", f"      <image:title>{escape(a_)}</image:title>", "    </image:image>"]
    lines += ["  </url>"]
if photo_images:
    lines += ["  <url>", f"    <loc>{escape(PHOTO_URL)}</loc>", f"    <lastmod>{TODAY}</lastmod>",
              "    <changefreq>monthly</changefreq>", "    <priority>0.8</priority>"]
    for p_, a_ in photo_images:
        lines += ["    <image:image>", f"      <image:loc>{escape(url(p_))}</image:loc>", f"      <image:title>{escape(a_)}</image:title>", "    </image:image>"]
    lines += ["  </url>"]
lines += ["</urlset>", ""]
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines))

# ---- robots.txt ----------------------------------------------------------------------------
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nAllow: /\nDisallow: /assets/original/\n\n" + f"Sitemap: {url('sitemap.xml')}\n")

print("Site address:", BASE)
print("Images in sitemap:", sum(1 for p, _ in images if not (p.startswith('assets/brand/') and 'og-image' not in p)))
print("Updated: index.html, blog.html, social.html, photography.html (seo blocks), sitemap.xml, robots.txt")
