"""Consistent numbered About headers and a CV panel derived from the CMS PDF."""
import hashlib,json,re,subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit,unquote
from lxml import html


def cv_metadata(root,source):
 """Inspect local files only. Never fetch arbitrary CMS URLs during a build."""
 result={};parsed=urlsplit(source or '')
 if parsed.scheme or parsed.netloc:return result
 base=(root/'docs').resolve();path=(base/unquote(parsed.path)).resolve()
 if not path.is_relative_to(base) or not path.is_file():return result
 result['size']=path.stat().st_size;result['format']=path.suffix.lstrip('.').upper()
 if path.suffix.lower()!='.pdf':return result
 digest=hashlib.sha256(path.read_bytes()).hexdigest()[:16];result['fingerprint']=digest
 try:
  info=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,timeout=15,check=True).stdout
  match=re.search(r'^Pages:\s*(\d+)',info,re.M)
  if match:result['pages']=int(match[1])
 except (OSError,subprocess.SubprocessError):pass
 try:
  relative=str(path.relative_to(root));changed=subprocess.run(['git','diff','HEAD','--quiet','--',relative],cwd=root,capture_output=True,timeout=5).returncode==1
  stamp=subprocess.run(['git','log','-1','--format=%cI','--',relative],cwd=root,capture_output=True,text=True,timeout=5,check=True).stdout.strip()
  if changed:stamp=datetime.fromtimestamp(path.stat().st_mtime).isoformat()
  if stamp:result['updated']=datetime.fromisoformat(stamp)
 except (OSError,ValueError,subprocess.SubprocessError):pass
 generated=base/'assets/generated';generated.mkdir(parents=True,exist_ok=True);preview=generated/('cv-preview-'+digest+'.jpg')
 if not preview.is_file():
  try:subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1000','-jpeg','-jpegopt','quality=80',str(path),str(preview.with_suffix(''))],capture_output=True,timeout=30,check=True)
  except (OSError,subprocess.SubprocessError):preview.unlink(missing_ok=True)
 if preview.is_file():result['preview']=str(preview.relative_to(base))
 # Only remove our obsolete generated CV previews; uploaded images are never touched.
 for old in generated.glob('cv-preview-*.jpg'):
  if old!=preview:old.unlink()
 return result


def refine_headers_cv(page,*,root,esc,url,set_html):
 config=json.loads((root/'editor/about-presentation.json').read_text());cv=config.get('cv_panel',{});units=config.get('header_units',{});subtitles=config.get('header_subtitles',{});profile=json.loads((root/'editor/profile.json').read_text())
 def word(key,default):return cv.get(key,default)
 def count(n,key,one,many):return str(n)+' '+str(units.get(key+('_one' if n==1 else '_many')) or (one if n==1 else many))
 def records(folder):return [json.loads(p.read_text()) for p in (root/'editor'/folder).glob('*.json') if json.loads(p.read_text()).get('published',True)]
 skills=json.loads((root/'editor/skills.json').read_text());tools=[v for v in skills.get('tools',[]) if v.get('published',True) and v.get('name')];languages=[v for v in skills.get('languages',[]) if v.get('published',True) and v.get('name')];skill_count=len(tools)+sum(len([s for s in g.get('items',[]) if str(s).strip()]) for g in skills.get('groups',[]) if g.get('published',True))
 roles=sum(v.get('record_type','role')!='event' for v in records('experience'));visits=sum(v.get('record_type')=='event' for v in records('experience'));recs=[v for v in config.get('recommendations',[]) if v.get('published',True) and v.get('quote')];real=sum(not v.get('sample') for v in recs);samples=len(recs)-real
 counts={'education':count(len(records('education')),'qualification','qualification','qualifications'),'experience':count(roles,'role','role','roles')+' · '+count(visits,'visit','visit','visits'),'skills':count(skill_count,'skill','skill','skills')+' · '+count(len(languages),'language','language','languages'),'recognition':count(len(records('achievements')),'award','award','awards'),'certificates':count(len(records('certificates')),'certificate','certificate','certificates')+' · '+count(len(records('workshops')),'event','event','events'),'recommendations':' · '.join(x for x in [count(real,'recommendation','recommendation','recommendations') if real else '',count(samples,'sample','sample','samples') if samples else ''] if x)}
 sections=page.xpath('//div[@class="about-body"]/section');nav=page.xpath('//nav[@class="section-index"]/a');numbers={a.get('href','').lstrip('#'):a.xpath('string(span[@class="section-number"])') for a in nav}
 for i,section in enumerate(sections,1):
  key=section.get('id');header=section.find('header')
  if header is None:continue
  header.attrib.pop('data-reveal',None);header.set('class','section-heading about-header-v2');header.set('data-header-motion','')
  label=header.xpath('./span[contains(@class,"section-label")]');badge=header.xpath('./*[contains(@class,"about-section-icon")]');heading=header.find('h2');controls=header.xpath('./div[@class="awards-controls"]');intro=header.xpath('./p')
  eyebrow=label[0] if label else html.Element('span',{'class':'section-label'})
  number=html.Element('span',{'class':'about-section-number','aria-hidden':'true'});number.text=numbers.get(key) or f'{i:02d}'
  row=html.Element('div',{'class':'about-header-row'});identity=html.Element('div',{'class':'about-header-identity'})
  if badge:
   tile=html.Element('span',{'class':'about-header-icon-tile','aria-hidden':'true'});tile.append(badge[0]);identity.append(tile)
  identity.append(number);identity.append(eyebrow);row.append(identity)
  right=html.Element('div',{'class':'about-header-right'})
  if counts.get(key):el=html.Element('span',{'class':'about-item-count'});el.text=counts[key];right.append(el)
  for c in controls:right.append(c)
  if len(right):row.append(right)
  for child in list(header):header.remove(child)
  header.append(row)
  if heading is not None:header.append(heading)
  subtitle=(skills.get('intro') or '') if key=='skills' else subtitles.get(key,'')
  if subtitle:
   el=html.Element('p',{'class':'about-header-subtitle'});el.text=str(subtitle);header.append(el)
 section=page.xpath('//*[@id="resume"]')[0];header=section.find('header')
 for child in list(section):
  if child is not header:section.remove(child)
 source=url(profile.get('resume'));meta=cv_metadata(root,source) if source else {};preview=url(cv.get('preview')) or meta.get('preview','');symbols={s.get('id'):s for s in page.xpath('//symbol')};overrides={x.get('key'):x.get('image') for x in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  custom=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
  symbol=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
 metadata=[]
 if source:metadata.append(meta.get('format') or ('PDF' if urlsplit(source).path.lower().endswith('.pdf') else word('document','Document')))
 if meta.get('pages'):metadata.append(count(meta['pages'],'page','page','pages'))
 if meta.get('size'):metadata.append(str(round(meta['size']/1024))+' KB' if meta['size']<1024*1024 else f"{meta['size']/1024/1024:.1f} MB")
 if meta.get('updated'):metadata.append(word('updated','Updated')+' '+meta['updated'].strftime('%b %Y'))
 pitch=str(cv.get('pitch') or '');content=('<p class="cv-pitch">'+esc(pitch)+'</p>') if pitch else ''
 if source:
  dest=source+('&' if '?' in source else '?')+'v='+meta['fingerprint'] if meta.get('fingerprint') else source
  content+='<div class="cv-actions"><a class="button primary" href="'+esc(dest)+'"'+(' download' if not urlsplit(source).scheme else '')+'>'+esc(word('download','Download CV'))+icon('download')+'</a><a class="cv-online" href="'+esc(dest)+'" target="_blank" rel="noopener noreferrer">'+esc(word('view_online','View online'))+icon('arrow')+'</a></div>'
  if metadata:content+='<p class="cv-metadata">'+esc(' · '.join(metadata))+'</p>'
 else:content+='<p class="cv-empty">'+esc(word('empty','Upload your CV through the CMS to show download and preview links.'))+'</p>'
 copy=html.fragment_fromstring('<div class="cv-panel-copy">'+content+'</div>');header.addnext(copy);copy.insert(0,header)
 if source and preview:
  image='<img src="'+esc(preview)+'" alt="'+esc(cv.get('preview_alt') or 'First-page preview of '+profile.get('name','')+'’s CV')+'" width="707" height="1000" loading="lazy" decoding="async">'
  section.append(html.fragment_fromstring('<a class="cv-preview" href="'+esc(dest)+'" target="_blank" rel="noopener noreferrer" aria-label="'+esc(word('open_preview','Open full CV'))+'">'+image+'<span class="cv-preview-hint">'+esc(word('preview_hint','Preview · open full CV'))+icon('arrow')+'</span></a>'))
 section.set('class',section.get('class','')+' cv-panel-v2'+(' has-preview' if source and preview else ''))
 page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="about-headers-cv.css">'));page.find('body').append(html.fragment_fromstring('<script src="about-headers-cv.js" defer></script>'))
