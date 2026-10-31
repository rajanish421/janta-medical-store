/* Shared helpers: CSV parser, Google Sheet link fixer, price formatter, blog posts loader */
function parseCSV(t){const r=[];let row=[],c="",q=false;for(let i=0;i<t.length;i++){const ch=t[i];
 if(q){if(ch=='"'){if(t[i+1]=='"'){c+='"';i++}else q=false}else c+=ch}
 else if(ch=='"')q=true;else if(ch==','){row.push(c);c=""}
 else if(ch=='\n'||ch=='\r'){if(ch=='\r'&&t[i+1]=='\n')i++;row.push(c);r.push(row);row=[];c=""}else c+=ch}
 if(c||row.length){row.push(c);r.push(row)}return r}
/* Link kaisa bhi ho (publish CSV / pubhtml / normal edit link / extra space) usse kaam karne wale CSV links ki list banata hai */
function csvCandidates(u){u=(u||'').replace(/[\s"'<>]+/g,'');if(!u)return[];
 if(u.includes('/pubhtml'))u=u.replace('/pubhtml','/pub');
 if(/\/spreadsheets\/d\/e\//.test(u)||!/docs\.google\.com\/spreadsheets\/d\//.test(u)){if(!/output=csv/.test(u))u+=(u.includes('?')?'&':'?')+'output=csv';return[u]}
 const id=u.match(/\/spreadsheets\/d\/([^\/?#]+)/)[1],g=(u.match(/[#?&]gid=(\d+)/)||[])[1]||'0';
 return['https://docs.google.com/spreadsheets/d/'+id+'/gviz/tq?tqx=out:csv&gid='+g,'https://docs.google.com/spreadsheets/d/'+id+'/export?format=csv&gid='+g]}
function csvUrl(u){return csvCandidates(u)[0]||''}
window.CSV_DIAG={};
/* Normal Sheet link (address bar wala) se Sheet ID + tab (gid) nikalta hai */
function sheetRef(u){const m=(u||'').match(/docs\.google\.com\/spreadsheets\/d\/(?!e\/)([^\/?#\s"']+)/);return m?{id:m[1],gid:((u.match(/[#?&]gid=(\d+)/)||[])[1])||'0'}:null}
/* JSONP: script tag se data aata hai, isliye CORS / file:// ki dikkat nahi hoti. Sheet "Anyone with the link: Viewer" honi chahiye */
function sheetJsonp(ref){return new Promise((res,rej)=>{const cb='__gv'+Math.random().toString(36).slice(2),s=document.createElement('script');
 const done=()=>{clearTimeout(to);delete window[cb];s.remove()},to=setTimeout(()=>{done();rej(new Error('jawab nahi aaya (Sheet private ho sakti hai: Share -> Anyone with the link -> Viewer)'))},10000);
 window[cb]=r=>{done();if(!r||r.status!=='ok'){rej(new Error('Google ne data nahi diya (Share -> Anyone with the link -> Viewer karein)'));return}
  const cols=r.table.cols,rows=[cols.map(c=>c.label||'')];r.table.rows.forEach(x=>rows.push(cols.map((_,i)=>{const c=x.c&&x.c[i];return c?(c.f!=null?c.f:(c.v==null?'':String(c.v))):''})));res(rows)};
 s.onerror=()=>{done();rej(new Error('script load nahi hui (Sheet private hai ya internet band)'))};
 s.src='https://docs.google.com/spreadsheets/d/'+ref.id+'/gviz/tq?headers=1&gid='+ref.gid+'&tqx=out:json;responseHandler:'+cb+'&_='+Date.now();document.head.appendChild(s)})}
/* Sheet fetch + last good copy browser mein save (internet/Sheet down ho to purani list chalti rahe) */
async function fetchCsv(u,key,nocache){const c=csvCandidates(u);if(!c.length)return null;let rows=null;const d={tried:[]};const ref=sheetRef(u);
 if(ref){try{rows=await sheetJsonp(ref);d.tried.push('JSONP (CORS ke bina) -> OK')}catch(e){d.tried.push('JSONP -> '+e.message)}}
 if(!rows)for(const x of c){try{const r=await fetch(x,{cache:'no-store'});d.tried.push('CSV '+x.slice(0,70)+'… -> HTTP '+r.status);if(!r.ok)continue;const t=await r.text();
  if(/^\s*<(!doctype|html)/i.test(t)){d.tried[d.tried.length-1]+=' (CSV nahi, web page mila)';continue}rows=parseCSV(t);break}catch(e){d.tried.push('CSV '+x.slice(0,70)+'… -> '+e.message)}}
 if(rows){try{localStorage.setItem(key,JSON.stringify(rows))}catch(e){}}else if(!nocache){try{rows=JSON.parse(localStorage.getItem(key)||'null')}catch(_){}d.cached=!!rows}
 window.CSV_DIAG[key]=d;return rows}
/* Price: sheet mein sirf number likhein (15). Website par "₹ 15" dikhega. "₹15", "15.50", "1250" sab chalega */
function fmtPrice(v){v=(v||'').trim();if(!v)return'';const m=v.match(/^(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)\s*(.*)$/i);if(!m)return v;
 const n=parseFloat(m[1].replace(/,/g,''));return'₹ '+n.toLocaleString('en-IN',{maximumFractionDigits:2})+(m[2]?' '+m[2]:'')}
const TYPE_LABEL={tip:'सेहत टिप',pehchan:'बीमारी की पहचान',quote:'डॉक्टर के विचार',lekh:'लेख'};
function typeKey(s){s=(s||'').toLowerCase().trim();if(/pehchan|पहचान|symptom|लक्षण/.test(s))return'pehchan';if(/quote|विचार|vichar|सुविचार/.test(s))return'quote';if(/lekh|लेख|article|blog/.test(s))return'lekh';return'tip'}
function parseDate(s){s=(s||'').trim();let m=s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);if(m)return new Date(+m[1],m[2]-1,+m[3]);m=s.match(/^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{4})/);if(m)return new Date(+m[3],m[2]-1,+m[1]);return null}
/* Posts: Sheet ki date aaj ya pehle ki ho tabhi dikhti hai (aage ki date = schedule). Naya upar. */
async function loadPosts(){let list;
 if(CONFIG.blogCsv){const rows=await fetchCsv(CONFIG.blogCsv,'jms_blog');list=rows?rows.slice(1).filter(r=>r[2]&&r[2].trim()).map((r,i)=>({id:i+1,date:parseDate(r[0]),type:typeKey(r[1]),title:r[2].trim(),body:(r[3]||'').trim(),by:(r[4]||'').trim()})):[]}
 else list=CONFIG.posts.map((r,i)=>({id:i+1,date:parseDate(r[0]),type:typeKey(r[1]),title:r[2],body:r[3]||'',by:r[4]||''}));
 const now=new Date();return list.filter(p=>!p.date||p.date<=now).sort((a,b)=>(b.date||0)-(a.date||0)||b.id-a.id)}
function esc2(t){return String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function bodyHtml(b){const o=[];let ul=false;(b||'').split(/\r?\n/).forEach(l=>{l=l.trim();if(!l){if(ul){o.push('</ul>');ul=false}return}const m=l.match(/^[-•*]\s*(.+)/);
 if(m){if(!ul){o.push('<ul>');ul=true}o.push('<li>'+esc2(m[1])+'</li>')}else{if(ul){o.push('</ul>');ul=false}o.push('<p>'+esc2(l)+'</p>')}});if(ul)o.push('</ul>');return o.join('')}
function fmtDate(d){return d?d.toLocaleDateString('hi-IN',{day:'numeric',month:'long',year:'numeric'}):''}
function excerpt(b,n){const t=(b||'').split(/\r?\n/).map(l=>l.trim().replace(/^[-•*]\s*/,'')).filter(Boolean).join(' · ');return t.length>n?t.slice(0,n).replace(/\s+\S*$/,'')+'…':t}
