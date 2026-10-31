JANTA MEDICAL STORE WEBSITE  (Hindi + English)
================================================
Poora folder ek saath hosting par upload karein.

  index.html                  Main home page (Hindi/English toggle andar)
  config.js                   *** Yahan apna sara data badlein (naam, phone, address, photo, Sheet links, reviews) ***
  check.html                  Sheet link ki jaanch (kuch dikh na raha ho to ise kholein)
  site.js                     Shared code (ise na badlein)
  images/owner.jpg            Owner ki photo, images/og-cover.png: share image
  health-tips/index.html      Health Tips list (Hindi)  | health-tips/<article>.html: 5 articles
  health-tips/en/...          Wahi sab English mein
  health-tips/daily.html      Roz ki sehat salah (Google Sheet ke Blog tab se chalta hai)
  robots.txt, sitemap.xml     Google ke liye
  tools/                      Aapke kaam ki cheezein (hosting par daalna zaroori nahi)
     CLIENT-GUIDE.html        Client ke liye Hindi guide (print kar sakte hain)
     janta-medical-sheet-template.xlsx   Stock + Blog ka ready Google Sheet template
     articles.json, build_blog.py        Static articles badalne ke liye
     set_domain.py            python tools/set_domain.py https://aapka-domain.in

Teen "index.html": (1) home, (2) Hindi tips list, (3) English tips list. Teeno alag folder mein.
Roz ka kaam sirf Google Sheet mein hota hai. Details: tools/CLIENT-GUIDE.html
