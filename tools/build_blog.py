# -*- coding: utf-8 -*-
"""Health Tips pages (Hindi + English) banane ki script.
Chalane ka tareeka:  python tools/build_blog.py
Naya article: tools/articles.json mein ek entry jodein (hi aur en dono), phir script chalayein.
Domain badalna ho to: python tools/set_domain.py https://aapka-domain.in"""
import os, json, html, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); OUT = os.path.join(ROOT, "health-tips")
BASE = "https://www.example.com"; NAME = "Janta Medical Store"; PHONE = "9721889885"; WA = "919721889885"
ART = json.load(open(os.path.join(HERE, "articles.json"), encoding="utf-8"))
today = datetime.date.today().isoformat()
L = {
 "hi": dict(p="../", other="English", homeN="होम", tips="स्वास्थ्य टिप्स", all="सभी स्वास्थ्य टिप्स", back="← सभी स्वास्थ्य टिप्स", backh="🏠 होम पेज",
   what="क्या करें", red="⚠ डॉक्टर को कब दिखाएं:", rev="समीक्षा: %s की फार्मेसी टीम · अपडेट: %s", rel="और पढ़ें", ctah="दवा या सलाह चाहिए?",
   ctat="पर्ची की फोटो WhatsApp करें। 5 किमी में फ्री होम डिलीवरी।", wa="💬 WhatsApp करें",
   foot="%s, प्रेमनगर चौराहा, सपहा रोड, कसया, कुशीनगर। यह लेख सिर्फ सामान्य जानकारी है, डॉक्टर की सलाह का विकल्प नहीं।",
   it="स्वास्थ्य टिप्स और सलाह", id="बुखार, शुगर, BP, बच्चों की देखभाल और दवा से जुड़ी आसान हिंदी जानकारी।", ih="आसान हिंदी में ज़रूरी जानकारी, ताकि आपको बेकार दौड़ना न पड़े।"),
 "en": dict(p="../../", other="हिंदी", homeN="Home", tips="Health tips", all="All health tips", back="← All health tips", backh="🏠 Home page",
   what="What to do", red="⚠ When to see a doctor:", rev="Reviewed by the %s pharmacy team · Updated: %s", rel="Read more", ctah="Need medicine or advice?",
   ctat="Send a photo of your prescription on WhatsApp. Free home delivery within 5 km.", wa="💬 WhatsApp us",
   foot="%s, Premnagar Chauraha, Sapaha Road, Kasia, Kushinagar. This article is general information and not a substitute for a doctor's advice.",
   it="Health Tips and Advice", id="Simple information on fever, sugar, BP, child care and medicines.", ih="Useful information in simple language, so you avoid unnecessary trips."),
}
CSS = """*{box-sizing:border-box;margin:0}html{scroll-behavior:smooth}
body{font:18px/1.75 Hind,system-ui,sans-serif;color:#12332c;background:#fbfaf6;animation:fade .5s}
h1,h2{font-family:'Baloo 2',Hind,sans-serif;line-height:1.25;color:#0f5c4d}a{color:#0f5c4d}
.w{max-width:760px;margin:auto;padding:0 18px}
header{background:rgba(255,255,255,.95);border-bottom:1px solid #d7e3da;position:sticky;top:0;z-index:5;backdrop-filter:blur(6px)}
header .w{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;min-height:60px}
header b{font:800 20px 'Baloo 2'}header a{display:inline-block;padding:10px 6px}
h1{font-size:clamp(28px,5vw,40px);margin:14px 0 10px}h2{font-size:24px;margin:26px 0 8px}li{margin:8px 0 8px 22px}
.bc{font-size:15px;color:#5b6f68;padding-top:14px}.bc a{display:inline-block;padding:6px 0}
.red{background:#fdecea;border-left:4px solid #c0392b;padding:12px 16px;border-radius:8px;margin:20px 0}
.cta{background:#e6f4ec;border-radius:16px;padding:20px;margin:28px 0;text-align:center}
.btn{display:inline-flex;align-items:center;min-height:44px;background:#1fa855;color:#fff;padding:10px 22px;border-radius:10px;font-weight:600;text-decoration:none;margin:6px;transition:transform .2s,filter .2s}
.btn:hover{filter:brightness(1.08);transform:translateY(-2px)}.btn.c{background:#0f5c4d}.btn.alt{background:#fff;color:#0f5c4d;border:2px solid #0f5c4d}
.card{display:block;background:#fff;border:1px solid #d7e3da;border-radius:14px;padding:16px 18px;margin:12px 0;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 22px #0f5c4d1f}.card b{font-size:19px;display:block}.card span{color:#5b6f68;font-size:16px}
.n{font-size:14px;color:#5b6f68}.back{margin:24px 0 4px}footer{padding:24px 0 40px;color:#5b6f68;font-size:15px}
@keyframes up{from{opacity:0;transform:translateY(20px)}}@keyframes fade{from{opacity:0}}
main>*{animation:up .6s backwards}main>:nth-child(2){animation-delay:.07s}main>:nth-child(3){animation-delay:.14s}main>:nth-child(4){animation-delay:.21s}main>:nth-child(5){animation-delay:.28s}main>:nth-child(n+6){animation-delay:.35s}
.pl{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.pl button{min-height:44px;padding:4px 16px;border-radius:99px;border:1px solid #1f8a5b;background:#fff;color:#0f5c4d;font:600 16px Hind;cursor:pointer}.pl button[aria-pressed=true]{background:#0f5c4d;color:#fff}
.tg{display:inline-block;background:#e6f4ec;color:#0f5c4d;font-weight:600;font-size:13px;padding:2px 10px;border-radius:99px;margin-bottom:6px}.card small{display:block;color:#5b6f68;margin-top:6px;font-size:14px}.post p{margin:10px 0}.post ul{margin:8px 0}
@media(min-width:1100px){.w{max-width:820px}}
@media(min-width:1500px){html{zoom:1.3}}@media(min-width:1900px){html{zoom:1.6}}@media(min-width:2300px){html{zoom:2.1}}
@media(max-width:480px){li{margin-left:18px}.cta .btn,.back .btn{display:flex;margin:8px 0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto}}"""

def page(lang, slug, title, desc, body, extra_ld=None, solo=False):
    t = L[lang]; fn = slug + ".html" if slug else "index.html"
    folder = "health-tips/en/" if lang == "en" else "health-tips/"
    canon = f"{BASE}/{folder}{slug + '.html' if slug else ''}"
    hi_u = f"{BASE}/health-tips/{slug + '.html' if slug else ''}"; en_u = f"{BASE}/health-tips/en/{slug + '.html' if slug else ''}"
    alt = ("en/" if lang == "hi" else "../") + fn
    home = t["p"] + "index.html?lang=" + lang
    sw = f'<a href="{alt}" hreflang="{"en" if lang == "hi" else "hi"}">{t["other"]}</a>' + (f' · <a href="index.html">{t["all"]}</a>' if slug else "")
    crumbs = f'<nav class="bc" aria-label="Breadcrumb"><a href="{home}">{t["homeN"]}</a> › ' + (f'<a href="index.html">{t["tips"]}</a> › <span>{html.escape(title)}</span>' if slug else f'<span>{t["tips"]}</span>') + "</nav>"
    e = html.escape
    ttl = title
    for suf in (" | Janta Medical Store, Kasia", " | Janta Medical Store", " | Janta Medical"):
        if len(title + suf) <= 68: ttl = title + suf; break
    ld = ""
    if extra_ld: ld = '<script type="application/ld+json">' + json.dumps(extra_ld, ensure_ascii=False) + "</script>"
    og_loc = "hi_IN" if lang == "hi" else "en_IN"
    if solo: sw = f'<a href="index.html">{t["all"]}</a>'
    hl = "" if solo else f'<link rel="alternate" hreflang="hi" href="{hi_u}"><link rel="alternate" hreflang="en" href="{en_u}"><link rel="alternate" hreflang="x-default" href="{hi_u}">'
    return f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(ttl)}</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0f5c4d">
<link rel="canonical" href="{canon}">{hl}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{'article' if slug else 'website'}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/images/og-cover.png"><meta property="og:locale" content="{og_loc}"><meta property="og:site_name" content="{NAME}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💊</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Hind:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style>{ld}</head><body>
<header><div class="w"><b>✚ <a href="{home}" style="text-decoration:none;padding:0">{NAME}</a></b><span>{sw}</span></div></header>
<main class="w">{crumbs}{body}</main>
<footer><div class="w">{e(t["foot"] % NAME)}</div></footer></body></html>"""

def cta(t):
    return f'<div class="cta"><b>{t["ctah"]}</b><br>{t["ctat"]}<br><a class="btn" href="https://wa.me/{WA}">{t["wa"]}</a><a class="btn c" href="tel:+91{PHONE}">📞 {PHONE}</a></div>'

def daily_card(lang):
    if lang == "en":
        return '<a class="card" href="../daily.html"><b>📅 Daily health advice</b><span>Spot the illness, learn from doctors and get a new tip every day (this page is in Hindi).</span></a>'
    return '<a class="card" href="daily.html"><b>📅 रोज़ की सेहत सलाह</b><span>बीमारी की पहचान, डॉक्टरों की सीख और रोज़ एक नई टिप।</span></a>'
urls = []
for lang in ("hi", "en"):
    t = L[lang]; d = os.path.join(OUT, "en") if lang == "en" else OUT; os.makedirs(d, exist_ok=True)
    pre = "en/" if lang == "en" else ""
    for i, a in enumerate(ART):
        c = a[lang]; e = html.escape
        li = "".join(f"<li>{e(x)}</li>" for x in c["tips"])
        others = [ART[(i + k) % len(ART)] for k in (1, 2)]
        related = f'<h2>{t["rel"]}</h2>' + "".join(f'<a class="card" href="{o["slug"]}.html"><b>{o[lang]["icon"]} {e(o[lang]["title"])}</b><span>{e(o[lang]["desc"])}</span></a>' for o in others)
        body = (f'<p class="n" style="margin-top:12px">{c["icon"]} {t["tips"]} · {NAME}</p><h1>{e(c["title"])}</h1><p>{e(c["intro"])}</p>'
                f'<h2>{t["what"]}</h2><ul>{li}</ul><div class="red"><b>{t["red"]}</b> {e(c["red"])}</div>'
                f'<p class="n">{t["rev"] % (NAME, today)}</p>{cta(t)}'
                f'<div class="back"><a class="btn c" href="index.html">{t["back"]}</a><a class="btn alt" href="{t["p"]}index.html?lang={lang}">{t["backh"]}</a></div>{related}')
        u = f"{BASE}/health-tips/{pre}{a['slug']}.html"
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": c["title"], "description": c["desc"], "inLanguage": lang, "datePublished": today, "dateModified": today, "mainEntityOfPage": u,
             "image": f"{BASE}/images/og-cover.png", "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["homeN"], "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": t["tips"], "item": f"{BASE}/health-tips/{pre}"},
                {"@type": "ListItem", "position": 3, "name": c["title"], "item": u}]}]}
        open(os.path.join(d, a["slug"] + ".html"), "w", encoding="utf-8").write(page(lang, a["slug"], c["title"], c["desc"], body, ld))
        urls.append((a["slug"] + ".html", True))
    cards = "".join(f'<a class="card" href="{a["slug"]}.html"><b>{a[lang]["icon"]} {html.escape(a[lang]["title"])}</b><span>{html.escape(a[lang]["desc"])}</span></a>' for a in ART)
    body = (f'<h1>{t["it"]}</h1><p>{t["ih"]}</p>{daily_card(lang)}{cards}'
            f'<div class="back"><a class="btn alt" href="{t["p"]}index.html?lang={lang}">{t["backh"]}</a></div>{cta(t)}')
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": t["it"], "inLanguage": lang, "url": f"{BASE}/health-tips/{pre}"}
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(lang, "", t["it"], t["id"], body, ld))

# daily.html: Google Sheet (Blog tab) se chalne wala page
DAILY_JS = r"""(async()=>{
const $=i=>document.getElementById(i),P=await loadPosts(),id=+new URLSearchParams(location.search).get('id'),p=id&&P.find(x=>x.id===id),V=$('view'),C=CONFIG.store;
const card=x=>`<a class="card" href="daily.html?id=${x.id}"><span class="tg">${TYPE_LABEL[x.type]}</span><b>${esc2(x.title)}</b><span>${esc2(excerpt(x.body,110))}</span><small>${fmtDate(x.date)}${x.by?' · '+esc2(x.by):''}</small></a>`;
if(p){
 const cn=document.querySelector('link[rel=canonical]'),d=excerpt(p.body||p.title,150);
 document.title=p.title+' | '+C.name;cn.href=cn.href.split('?')[0]+'?id='+p.id;
 document.querySelector('meta[name=description]').content=d;document.querySelector('meta[property="og:title"]').content=p.title;document.querySelector('meta[property="og:description"]').content=d;
 $('h1').textContent=p.type=='quote'?'“'+p.title+'”':p.title;
 $('lead').innerHTML='<span class="tg">'+TYPE_LABEL[p.type]+'</span> · '+fmtDate(p.date)+(p.by?' · '+esc2(p.by):'');
 document.querySelector('.bc span').outerHTML='<a href="daily.html">रोज़ की सेहत सलाह</a> › <span>'+esc2(p.title)+'</span>';
 $('bk').href='daily.html';$('bk').textContent='← सभी सेहत सलाह';
 const rel=P.filter(x=>x.id!==p.id).slice(0,3);
 V.innerHTML='<div class="post">'+bodyHtml(p.body)+'</div><div class="red"><b>ध्यान दें:</b> यह सामान्य जानकारी है, डॉक्टर की सलाह का विकल्प नहीं। तकलीफ बढ़े तो डॉक्टर को दिखाएं।</div>'+(rel.length?'<h2>और पढ़ें</h2>'+rel.map(card).join(''):'');
 const ld=document.createElement('script');ld.type='application/ld+json';
 ld.textContent=JSON.stringify({"@context":"https://schema.org","@type":"Article","headline":p.title,"inLanguage":"hi","datePublished":p.date?p.date.toISOString().slice(0,10):undefined,"author":{"@type":"Organization","name":C.name},"publisher":{"@type":"Organization","name":C.name}});document.head.appendChild(ld);
}else{
 let cur='all';const K=[['all','सब कुछ'],['tip',TYPE_LABEL.tip],['pehchan',TYPE_LABEL.pehchan],['quote',TYPE_LABEL.quote],['lekh',TYPE_LABEL.lekh]];
 const draw=()=>{const f=P.filter(x=>cur=='all'||x.type==cur);$('lst').innerHTML=f.length?f.map(card).join(''):'<p>जल्द ही नई जानकारी आएगी।</p>'};
 V.innerHTML='<div class="pl" id="pl">'+K.map(k=>'<button data-k="'+k[0]+'" aria-pressed="'+(k[0]=='all')+'">'+k[1]+'</button>').join('')+'</div><div id="lst"></div>';
 $('pl').onclick=e=>{const k=e.target.dataset.k;if(!k)return;cur=k;[...$('pl').children].forEach(b=>b.setAttribute('aria-pressed',b.dataset.k==k));draw()};draw();
}})();"""
t = L["hi"]
dbody = ('<h1 id="h1">रोज़ की सेहत सलाह</h1><p id="lead">बीमारी की पहचान, घरेलू देखभाल और डॉक्टरों की सीख, रोज़ एक नई जानकारी।</p><div id="view"></div>'
         '<noscript><p>कृपया JavaScript चालू करें।</p></noscript>' + cta(t) +
         f'<div class="back"><a class="btn c" id="bk" href="index.html">{t["back"]}</a><a class="btn alt" href="../index.html?lang=hi">{t["backh"]}</a></div>'
         '<script src="../config.js"></script><script src="../site.js"></script><script>' + DAILY_JS + '</script>')
open(os.path.join(OUT, "daily.html"), "w", encoding="utf-8").write(page("hi", "daily", "रोज़ की सेहत सलाह", "बीमारी की पहचान, घरेलू देखभाल और डॉक्टरों की सीख, रोज़ एक नई जानकारी। जनता मेडिकल स्टोर, कसया।", dbody, solo=True))
rows_extra = [f"<url><loc>{BASE}/health-tips/daily.html</loc><lastmod>{today}</lastmod></url>"]

# sitemap (hreflang ke saath) + robots
X = lambda s: f"{BASE}/health-tips/{s}"; XE = lambda s: f"{BASE}/health-tips/en/{s}"
rows = [f"<url><loc>{BASE}/</loc><lastmod>{today}</lastmod></url>"]
for s in [""] + [a["slug"] + ".html" for a in ART]:
    for loc in (X(s), XE(s)):
        rows.append(f'<url><loc>{loc}</loc><lastmod>{today}</lastmod><xhtml:link rel="alternate" hreflang="hi" href="{X(s)}"/><xhtml:link rel="alternate" hreflang="en" href="{XE(s)}"/></url>')
rows += rows_extra
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /check.html\nSitemap: {BASE}/sitemap.xml\n")
print("Pages:", len(ART) * 2 + 2, "| sitemap URLs:", len(rows))
