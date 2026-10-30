"""Build the portfolio from Pages CMS content; never import the legacy generator."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json, shutil, re, hashlib
from home_design import enhance
from home_polish import polish
from editorial import redesign
from hero_refresh import refresh_hero
from about_refresh import refresh_about
from about_finish import finish_about
from education_v2 import education_v2
from about_timeline import refine_timeline
from about_facts import refine_facts
from about_skills import refine_skills
from about_awards import refine_awards
from about_learning import refine_learning
from about_exposure import refine_exposure
from about_headers_cv import refine_headers_cv
from shared_footer import refine_footer
from shared_theme import refine_theme
from page_navigation import refine_navigation
from shared_dock import refine_dock
from shared_cursor import refine_cursor
from launch_polish import refine_launch
from navigation import read_navigation
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
TAGS=['p','br','strong','b','em','i','u','s','h2','h3','h4','h5','h6','ul','ol','li','blockquote','a','img','figure','figcaption','pre','code','hr','table','thead','tbody','tr','th','td','mark','span','div']
def esc(v):return escape(str(v or ''),quote=True)
def url(v):
 v=str(v or '').strip()
 if not v:return ''
 if v.startswith('//') or '\\' in v or any(ord(c)<32 for c in v):return ''
 if urlsplit(v).scheme.lower() not in ('','http','https','mailto','tel'):return ''
 return v

def rich(v):
 root=html.fragment_fromstring('<div>'+str(v or '')+'</div>')
 for e in list(root.iterdescendants()):
  if e.getparent() is None:continue
  if not isinstance(e.tag,str):
   e.getparent().remove(e);continue
  if e.tag in ('script','style','iframe','object','embed','svg','math','form','input','button'):
   e.drop_tree();continue
  if e.tag not in TAGS:
   e.drop_tag();continue
  allowed={'class'}|{'a':{'href','title'},'img':{'src','alt','title','width','height'},'th':{'colspan'},'td':{'colspan'}}.get(e.tag,set())
  for key in list(e.attrib):
   if key not in allowed:del e.attrib[key]
   elif key in ('href','src'):
    safe=url(e.get(key))
    if safe:e.set(key,safe)
    else:del e.attrib[key]
 return inner(root)
def read(path):return json.loads((ROOT/'editor'/path).read_text())
def entries(folder):
 result=[]
 for p in (ROOT/'editor'/folder).glob('*.json'):
  d=json.loads(p.read_text())
  if d.get('published',False):result.append(dict(d,_id=folder+'-'+p.stem))
 return sorted(result,key=lambda x:(float(x.get('order') or 0),str(x.get('date') or ''),x['_id']))
def set_html(e,markup):
 for c in list(e):e.remove(c)
 e.text=None
 wrapper=html.fragment_fromstring('<div>'+markup+'</div>');e.text=wrapper.text
 for c in wrapper:e.append(c)
def select(d,x):return d.xpath(x)
def one(d,x):return select(d,x)[0]
def inner(e):return (e.text or '')+''.join(html.tostring(c,encoding='unicode') for c in e)
def section(d,id,markup):
 e=one(d,f'//*[@id="{id}"]'); header=e[0]
 for c in list(e)[1:]:e.remove(c)
 for c in html.fragments_fromstring(markup):
  if isinstance(c,str):continue
  e.append(c)
def image(path,alt='',cls=''):
 return f'<img class="{esc(cls)}" src="{esc(url(path))}" alt="{esc(alt)}" loading="lazy">' if url(path) else ''
def attachment(path,title):
 path=url(path)
 if not path:return ''
 link=f'<p><a class="button secondary" href="{esc(path)}" target="_blank" rel="noopener">Open / download {esc(title)}</a></p>'
 if urlsplit(path).path.lower().endswith(('.jpg','.jpeg','.png','.webp','.gif')):return image(path,title)+link
 if urlsplit(path).path.lower().endswith('.pdf'):return f'<iframe class="certificate-pdf" src="{esc(path)}" title="{esc(title)}" loading="lazy"></iframe>'+link
 return link

def visible_rich(value):
 """Treat an untouched visual editor (<p><br></p>) as empty."""
 cleaned=rich(value)
 fragment=html.fragment_fromstring('<div>'+cleaned+'</div>')
 return cleaned if fragment.text_content().strip() or fragment.xpath('.//img[@src]') else ''

def filled(value):
 return value is not None and str(value).strip()!=''

def date_text(v,kind):
 start=str(v.get('start_date') or '').strip();end=str(v.get('end_date') or '').strip()
 current=v.get('currently_studying') if kind=='education' else v.get('currently_working') if kind=='experience' else False
 if current:end='Present'
 if start or end:return ' – '.join(x for x in (start,end) if x)
 if kind=='certificates' and filled(v.get('issue_date')):return str(v['issue_date'])
 return str(v.get('date') or '').strip()

def grade_text(v):
 grade=str(v.get('grade') or '').strip();scale=str(v.get('grade_scale') or '').strip()
 if grade:return grade+(' / '+scale if scale else '')
 return str(v.get('badge') or '').strip()

def optional_facts(v,kind):
 fields={
 'education':[('degree','Qualification'),('department','Department'),('specialization','Specialization'),('location','Location'),('thesis_title','Thesis / dissertation'),('supervisor','Supervisor')],
 'experience':[('employment_type','Employment type'),('location','Location')],
 'achievements':[('award_category','Category'),('recognition_type','Recognition'),('related_work','Related work')],
 'certificates':[('credential_id','Credential ID')],
 'projects':[('status','Status'),('role','My role')],
 'posts':[('author','Author'),('last_updated','Last updated')],
 'workshops':[('duration','Duration'),('location','Location / format'),('participation_role','Participation role')]
 }.get(kind,[])
 facts=[(label,v.get(key)) for key,label in fields if filled(v.get(key))]
 if kind=='education' and filled(v.get('grade_scale')) and not filled(v.get('grade')):facts.append(('Grade scale',v['grade_scale']))
 if kind in ('projects',):
  dates=date_text(v,kind)
  if dates:facts.append(('Period',dates))
 if kind in ('certificates','achievements'):
  if filled(v.get('institution')):facts.append(('Issuer',v['institution']))
  if date_text(v,kind):facts.append(('Issued' if kind=='certificates' else 'Date',date_text(v,kind)))
 if kind=='certificates':
  if v.get('does_not_expire'):facts.append(('Validity','Does not expire'))
  elif filled(v.get('expiry_date')):facts.append(('Expires',v['expiry_date']))
 for item in v.get('extra_fields') or []:
  if filled(item.get('value')):facts.append((item.get('label') or '',item['value']))
 return '<dl class="entry-facts">'+''.join('<div>'+(f'<dt>{esc(label)}</dt>' if label else '')+f'<dd>{esc(value)}</dd></div>' for label,value in facts)+'</dl>' if facts else ''

def optional_sections(v,kind):
 markup=''
 for key,label in [('responsibilities','Responsibilities'),('achievements','Achievements / impact'),('reason','Reason / selection criteria'),('objectives','Objectives'),('methods','Methods / tools'),('results','Results / outcomes'),('learning_outcomes','Learning outcomes'),('references','Sources / references'),('additional_details','Additional details')]:
  content=visible_rich(v.get(key))
  if content:markup+=f'<section class="entry-detail-section"><h3>{label}</h3>{content}</section>'
 for key,label in [('coursework','Relevant coursework'),('skills','Skills'),('collaborators','Collaborators'),('tags','Tags')]:
  values=[str(x).strip() for x in (v.get(key) or []) if filled(x)]
  if values:markup+=f'<section class="entry-detail-section"><h3>{label}</h3><ul>'+''.join(f'<li>{esc(x)}</li>' for x in values)+'</ul></section>'
 return markup

def optional_resources(v):
 markup=''
 for key,label in [('file','Supporting document'),('report','Project report')]:
  markup+=attachment(v.get(key),label)
 documents=''
 for item in v.get('attachments') or []:
  if url(item.get('file')):documents+=attachment(item['file'],item.get('label') or 'Document')
 if documents:markup+='<section class="entry-detail-section"><h3>Supporting documents</h3>'+documents+'</section>'
 links=[]
 for key,label in [('organization_url','Organization website'),('verification_url','Verification / official record')]:
  if url(v.get(key)):links.append((label,url(v[key])))
 for item in v.get('related_links') or []:
  dest=url(item.get('url'))
  if dest:links.append((item.get('label') or 'Open link',dest))
 if links:markup+='<section class="entry-detail-section"><h3>Related links</h3><ul>'+''.join(f'<li><a href="{esc(dest)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a></li>' for label,dest in links)+'</ul></section>'
 return markup

def optional_tag(tag,cls,value):
 return f'<{tag} class="{cls}">{esc(value)}</{tag}>' if filled(value) else ''

def story_body(d,kind=None):
 body=visible_rich(d.get('body',''))+optional_facts(d,kind)+optional_sections(d,kind)
 for pic in d.get('gallery') or []:
  if not url(pic.get('image')):continue
  body+='<figure>'+image(pic.get('image'),pic.get('caption',''))+(('<figcaption>'+esc(pic['caption'])+'</figcaption>') if filled(pic.get('caption')) else '')+'</figure>'
 video=url(d.get('video_url',''))
 if video:
  u=urlsplit(video); host=u.netloc.lower(); vid=''
  if host in ('youtube.com','www.youtube.com'):
   from urllib.parse import parse_qs
   vid=parse_qs(u.query).get('v',[''])[0] if u.path=='/watch' else u.path.split('/')[-1]
  elif host=='youtu.be':vid=u.path.strip('/')
  if re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):body+=f'<iframe class="story-video" src="https://www.youtube-nocookie.com/embed/{vid}" title="Video" allowfullscreen loading="lazy"></iframe>'
  elif u.path.lower().endswith(('.mp4','.webm')):body+=f'<video controls preload="metadata" src="{esc(video)}"></video>'
  else:body+=f'<p><a href="{esc(video)}" target="_blank" rel="noopener">Watch video</a></p>'
 return body+optional_resources(d)

def build():
 OUT.mkdir(exist_ok=True)
 # Immutable original design lives in templates; uploaded media lives in docs/assets.
 pages={p.stem:html.parse(str(p)) for p in (ROOT/'templates').glob('*.html')}
 profile=read('profile.json'); about=read('about.json'); details={};documents=[]
 version=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'scripts').glob('*')) if p.is_file())+b''.join(p.read_bytes() for p in sorted((ROOT/'editor').rglob('*.json')))).hexdigest()[:16]
 for d in pages.values():
  for a in select(d,'//a[@href]'):
   href=a.get('href')
   if href=='assets/ariful-islam-fahim-cv.pdf':
    a.set('href',url(profile['resume']));a.attrib.pop('download',None)
   elif href.startswith('mailto:arifulislamfahim04@gmail.com'):a.set('href','mailto:'+profile['email']+href.partition('?')[1]+href.partition('?')[2])
   elif href=='tel:+8801968718018':a.set('href','tel:'+profile['phone'])
   elif 'linkedin.com/in/ariful-islam-fahim' in href:a.set('href',url(profile['linkedin']))
  for e in select(d,'//*[@data-copy]'):
   value=e.get('data-copy')
   if '@' in value:e.set('data-copy',profile['email'])
   elif value.startswith('+880'):e.set('data-copy',profile['phone'])
  for e in select(d,'//footer//span[1]'):
   # Only replace the name text, preserving the live year.
   for child in e:
    if child.get('data-year') is not None:child.tail=' '+profile['name']+'.'
 h=pages['index']
 for selector,key in [('//div[@class="profile-content"]/h2','name'),('//p[@class="profile-role"]','role'),('//span[@class="availability"]','availability'),('//div[@class="profile-location"]/span','location')]:set_html(one(h,selector),esc(profile[key]))
 for key,x in [('cover','//div[@class="profile-photo"]/img'),('secondary_image','//div[@class="floating-swatch"]/img')]:
  for e in select(h,x):e.set('src',url(profile[key]))
 if profile.get('photo'):
  e=one(h,'//div[@class="profile-photo"]/img');e.set('src',url(profile['photo']));e.set('alt',profile.get('photo_alt',''));e.set('class','textile-photo portrait-upload')
  for e in select(h,'//span[@class="portrait-monogram"]|//div[@class="floating-swatch"]|//div[@class="yarn-spool"]|//svg[contains(@class,"needle-thread")]|//span[@class="photo-credit"]'):e.getparent().remove(e)
 for item in profile.get('social_links') or []:
  dest=url(item.get('url'))
  if dest:
   link=html.Element('a',href=dest,target='_blank',rel='noopener noreferrer',**{'class':'text-link'})
   link.text=item.get('label') or 'Profile';one(h,'//div[@class="profile-socials"]').append(link)
 title=one(h,'//*[@id="home-title"]');typebox=one(title,'.//span[@class="type-box"]');typebox.getparent().remove(typebox);set_html(title,esc(profile['hero_title']));title.append(typebox)
 title.set('aria-label',profile['hero_title']+' '+(profile.get('rotating_words') or [''])[0])
 for key,x in [('hero_description','//p[@class="hero-description"]'),('introduction','//section[.//span[text()="MY APPROACH"]]/p'),('call_to_action','//section[contains(@class,"cta-section")]/p')]:set_html(one(h,x),rich(profile[key]))
 stats=''
 for s in profile.get('stats',[]):
  value=float(s.get('value') or 0); decimals=max(0,min(3,int(s.get('decimals') or 0)))
  stats+=f'<article class="stat"><div><strong><span data-count="{value}" data-decimals="{decimals}">{value:.{decimals}f}</span><small>{esc(s.get("suffix"))}</small></strong><h3>{esc(s.get("label"))}</h3><span class="stat-detail">{esc(s.get("detail"))}</span></div></article>'
 set_html(one(h,'//div[@class="stats-glass glass"]'),stats)
 a=pages['about'];set_html(one(a,'//div[@class="bio"]'),rich(about['biography']))
 for key,x in [('information','//dl[@class="info-grid"]'),('glance','//aside[contains(@class,"at-glance")]/dl')]:
  markup=''.join(f'<div class="info-card glass"><div><dt>{esc(v.get("label"))}</dt><dd>{esc(v["value"])}</dd></div></div>' for v in about.get(key,[]) if filled(v.get("value")));set_html(one(a,x),markup)
 def timeline(folder):
  cards=''
  for v in entries(folder):
   extra=story_body(dict(v,body=''),folder)
   expanded='<details class="entry-extra"><summary>More details</summary><div class="entry-extra-body">'+extra+'</div></details>' if extra else ''
   cards+=f'<article class="timeline-card glass" data-entry-id="{esc(v["_id"])}" data-reveal><span class="timeline-node"></span>{optional_tag("span","care-chip",date_text(v,folder))}<h3>{esc(v["title"])}</h3>{optional_tag("p","institution",v.get("institution"))}{visible_rich(v.get("body"))}{optional_tag("span","fact-chip",grade_text(v))}{expanded}</article>'
  return '<div class="stitched-timeline">'+cards+'</div>' if cards else '<p>No entries published yet.</p>'
 for folder in ('education','experience'):section(a,folder,timeline(folder))
 skills='<div class="skill-grid">'
 for s in about.get('skills',[]):skills+=f'<article class="skill-card glass"><h3>{esc(s["title"])}</h3>{visible_rich(s.get("body"))}<ul class="skill-list">'+''.join('<li>'+esc(v)+'</li>' for v in s.get('items',[]) if filled(v))+'</ul></article>'
 skills+='</div><div class="language-grid">'+''.join(f'<article class="language-card glass"><div><h3>{esc(v["title"])}</h3><p>{esc(v.get("description"))}</p></div></article>' for v in about.get('languages',[]))+'</div>'
 section(a,'skills',skills)
 def certificates(folder):
  cards=''
  for v in entries(folder):
   content=story_body(v,folder)
   button=''
   if content:
    documents.append(dict(id=v['_id'],kind='Academic recognition' if folder=='achievements' else 'Certificate record',title=v['title'],body=content))
    button=f'<button class="text-link" data-document="{esc(v["_id"])}">View details / certificate →</button>'
   cards+=f'<article class="certificate-card glass" data-entry-id="{esc(v["_id"])}" data-reveal>{optional_tag("span","care-chip",date_text(v,folder))}<h3>{esc(v["title"])}</h3>{optional_tag("p","institution",v.get("institution"))}{visible_rich(v.get("body"))}{button}</article>'
  return '<div class="certificate-grid">'+cards+'</div>' if cards else '<p>No entries published yet.</p>'
 section(a,'recognition',certificates('achievements'))
 transcript_button='<div class="transcript-action"><button class="button secondary" data-document="transcript">View Transcript</button></div>' if visible_rich(about.get('transcript_body')) or url(about.get('transcript')) else ''
 section(a,'certificates',certificates('certificates')+transcript_button+'<h3 class="subsection-title">Workshops &amp; seminars</h3>'+timeline('workshops'))
 documents.append(dict(id='transcript',kind='Academic transcript',title='Academic transcript',body=rich(about.get('transcript_body'))+attachment(about.get('transcript'),'transcript')))
 recommendations=''.join(f'<article class="glass certificate-card"><h3>{esc(v["title"])}</h3>{visible_rich(v.get("body"))}</article>' for v in about.get('recommendations',[])) or '<div class="recommendation-empty glass"><h3>Recommendations coming soon</h3><p>Real recommendations will appear here as they become available.</p></div>'
 references=''.join('<article class="reference-card glass">'+visible_rich(v.get('body'))+'</article>' for v in about.get('references',[]))
 section(a,'recommendations',recommendations+'<details class="academic-references glass"><summary>Academic references</summary><div class="reference-grid">'+references+'</div></details>')
 # Generate both listing cards and shareable full pages from every published entry.
 for folder,page,cls,attr in [('posts','blogs','blog','data-blog-category'),('projects','projects','project','data-category')]:
  cards='';items=entries(folder);cats=[]
  for v in items:
   key=v['_id'];category=v.get('category') or 'General';cats.append(category)
   filename=key+'.html';body=story_body(v,folder);details[key]=dict(title=v['title'],tag=v.get('label') or category,body=body)
   picture=image(v.get('cover'),v.get('cover_alt') or v['title'],'textile-photo')
   if picture:picture=f'<a class="{cls}-cover" href="{filename}" data-project="{key}">{picture}</a>'
   cards+=f'<article class="{cls}-card glass" {attr}="{esc(category)}" data-reveal>{picture}<div class="{cls}-content"><span class="section-label">{esc(v.get("label") or category)}</span>{optional_tag("div","blog-meta",v.get("date"))}<h2><a href="{filename}" data-project="{key}">{esc(v["title"])}</a></h2>{optional_tag("p","entry-summary",v.get("summary"))}<a class="text-link" href="{filename}" data-project="{key}">Read more →</a></div></article>'
   single=html.parse(str(ROOT/'templates'/f'{page}.html'));main=one(single,'//main');set_html(main,f'<article class="page-content shell story-page"><a class="button secondary" href="{page}.html">← Back to {page}</a><p class="section-label">{esc(" · ".join(str(x) for x in (category,v.get("date")) if filled(x)))}</p><h1>{esc(v["title"])}</h1>{image(v.get("cover"),v.get("cover_alt") or v["title"],"story-cover")}<div class="story-body">{body}</div></article>');one(single,'//title').text=v['title']+' — '+profile['name'];pages[key]=single
  set_html(one(pages[page],f'//div[@class="{cls}-grid"]'),cards or '<p>No entries published yet.</p>')
  filterattr='data-blog-filter' if folder=='posts' else 'data-project-filter'
  markup=''.join(f'<button class="filter {"active" if i==0 else ""}" {filterattr}="{esc(c)}" aria-pressed="{str(i==0).lower()}">{esc("All" if i==0 else c)}</button>' for i,c in enumerate(['all']+sorted(set(cats))))
  set_html(one(pages[page],'//div[contains(@class,"filter-bar")]'),markup)
 moments=enhance(pages,profile,entries('gallery'),read('homepage.json'),esc=esc,url=url,rich=rich,image=image,set_html=set_html,one=one,select=select,story_body=story_body,root=ROOT)
 polish(pages,profile,read('homepage.json'),entries('updates'),root=ROOT,esc=esc,url=url,rich=rich,one=one,select=select,set_html=set_html)
 editorial_site,editorial_ui=redesign(pages,profile,about,read('homepage.json'),root=ROOT,esc=esc,url=url,rich=visible_rich,one=one,select=select,set_html=set_html,entries=entries,story_body=story_body,date_text=date_text)
 refresh_hero(pages['index'],profile,read('homepage.json'),esc=esc,url=url,rich=visible_rich,set_html=set_html,navigation=read_navigation(ROOT))
 refresh_about(pages['about'],pages['index'],read('homepage.json'),root=ROOT,esc=esc,url=url,set_html=set_html)
 finish_about(pages,root=ROOT,esc=esc,url=url,set_html=set_html)
 education_v2(pages['about'],root=ROOT,esc=esc,url=url,set_html=set_html,rich=rich)
 refine_timeline(pages['about'],root=ROOT,esc=esc)
 refine_facts(pages['about'],root=ROOT,esc=esc,url=url,set_html=set_html)
 refine_skills(pages['about'],root=ROOT,esc=esc,url=url,set_html=set_html)
 refine_awards(pages['about'],root=ROOT,esc=esc,url=url,rich=visible_rich,set_html=set_html,story_body=story_body)
 refine_learning(pages['about'],root=ROOT,esc=esc,url=url,rich=visible_rich,set_html=set_html,story_body=story_body)
 refine_exposure(pages['about'],root=ROOT,esc=esc,url=url,rich=visible_rich,set_html=set_html,story_body=story_body)
 refine_headers_cv(pages['about'],root=ROOT,esc=esc,url=url,set_html=set_html)
 refine_footer(pages,root=ROOT,esc=esc,url=url,set_html=set_html)
 refine_dock(pages,root=ROOT,esc=esc,url=url,set_html=set_html)
 refine_theme(pages,root=ROOT)
 navigation_css=refine_navigation(pages,root=ROOT)
 refine_cursor(pages,root=ROOT)
 refine_launch(pages,profile=profile,root=ROOT,esc=esc,set_html=set_html)
 # Remove previously generated post pages, so deleted/unpublished entries disappear.
 for pattern in ('posts-*.html','projects-*.html'):
  for p in OUT.glob(pattern):p.unlink()
 for name,d in pages.items():
  # All pages use the same editable contact and resume values.
  for e in select(d,'//script[@src="content.js" or @src="site.js" or @src="home-core.js" or @src="home-polish.js"]'):e.set('src',e.get('src')+'?v='+version)
  for e in select(d,'//link[@href="home-base.css" or @href="home-polish.css"]'):e.set('href',e.get('href')+'?v='+version)
  for e in select(d,'//a[@href]'):
   old=e.get('href')
   if old=='assets/ariful-islam-fahim-cv.pdf':e.set('href',url(profile['resume']));e.attrib.pop('download',None)
   elif old.startswith('mailto:arifulislamfahim04@gmail.com'):e.set('href',old.replace('arifulislamfahim04@gmail.com',profile['email']))
   elif old=='tel:+8801968718018':e.set('href','tel:'+profile['phone'])
   elif 'linkedin.com/in/ariful-islam-fahim' in old:e.set('href',url(profile['linkedin']))
  if name=='index' and not urlsplit(url(profile.get('resume'))).scheme:
   for e in select(d,'//div[@class="hero-actions"]/a[1]'):e.set('download','')
  for e in select(d,'//body//*'):
   for key in ('text','tail'):
    value=getattr(e,key)
    if value:
     value=value.replace('Ariful Islam Fahim',profile['name']).replace('arifulislamfahim04@gmail.com',profile['email']).replace('+880 1968-718018',profile['phone'])
     setattr(e,key,value)
  # The editorial runtime retains gallery behavior without the legacy rail and card effects.
  for e in select(d,'//head'):

   pass
  for script in select(d,'//script[@src]'):script.set('defer','')
  (OUT/(name+'.html')).write_text(html.tostring(d,encoding='unicode',doctype='<!doctype html>'))
 if not about.get('transcript_public',False):documents=[v for v in documents if v['id']!='transcript']
 for folder in ('education','experience','workshops'):
  for v in entries(folder):
   if story_body(v,folder):documents.append(dict(id=v['_id'],kind='Supporting document',title=v['title'],body=story_body(v,folder)))
 payload='window.PORTFOLIO_DETAILS='+json.dumps(details,ensure_ascii=False)+';\nwindow.PORTFOLIO_DOCUMENTS='+json.dumps(documents,ensure_ascii=False)+';\nwindow.PORTFOLIO_PROFILE='+json.dumps(profile,ensure_ascii=False)+';'
 (OUT/'content.js').write_text(payload+'\nwindow.PORTFOLIO_MOMENTS='+json.dumps([dict(m,body=visible_rich(m.get('body')),source_url=url(m.get('source_url'))) for m in moments],ensure_ascii=False)+';')
 for extension in ('css','js'):
  shutil.copyfile(ROOT/('scripts/home_polish.'+extension),OUT/('home-polish.'+extension))
 shutil.copyfile(ROOT/'scripts/portfolio-foundation.css',OUT/'portfolio-foundation.css')
 shutil.copyfile(ROOT/'scripts/home.css',OUT/'home.css')
 shutil.copyfile(ROOT/'scripts/home.js',OUT/'home.js')
 js=(ROOT/'dist/site.js').read_text().replace("const words=['CREATOR’S CURIOSITY','ENGINEER’S MIND','STORYTELLER’S EYE','LOVE FOR AI'];","const words=window.PORTFOLIO_PROFILE.rotating_words?.length ? window.PORTFOLIO_PROFILE.rotating_words : ['CURIOUS MIND'];")
 js=js.replace('mailto:arifulislamfahim04@gmail.com?subject=',"mailto:${window.PORTFOLIO_PROFILE.email}?subject=")
 js=js.replace("h.setAttribute('aria-label','I’m Arif, a textile engineering student with a creator’s curiosity.');","h.setAttribute('aria-label',window.PORTFOLIO_PROFILE.hero_title+' '+words[0]);")
 js=js.replace("if(e.button!==0||","if(a.hasAttribute('data-project')||e.button!==0||")
 js=js.replace("hour:'2-digit',minute:'2-digit'","hour:'numeric',minute:'2-digit',hour12:true").replace("el.textContent=time+' BD'","el.textContent=time.toUpperCase()+' BD'")
 (OUT/'site.js').write_text(js)
 # Homepage reuses the core behavior with its old canvas/cursor loop removed.
 home_js=re.sub(r'// Only thin, transparent cursor layers.*?(?=let scrollQueued=false;)', 'function drawWeave(){}\n',js,flags=re.S)
 home_js=home_js.replace('if(reduced.matches||!document.startViewTransition)', 'if(body.hasAttribute("data-home-polish")||reduced.matches||!document.startViewTransition)')
 (OUT/'home-core.js').write_text(home_js)
 base_css=(ROOT/'dist/site.css').read_text()
 base_css=re.sub(r"@import url\([^;]+;",'',base_css,count=1)
 (OUT/'home-base.css').write_text(base_css)

 (OUT/'editor.css').write_text('''.portrait-upload{object-fit:cover!important;filter:none!important}.story-page{max-width:900px}.story-page h1{font-size:clamp(2rem,5vw,4rem);line-height:1.15;margin:2rem 0}.story-body{font-size:1.1rem;line-height:1.85}.story-cover{width:100%;max-height:500px;object-fit:cover;border-radius:16px}.story-body img,#reader-body img,#document-body img{max-width:100%;height:auto;border-radius:12px}.story-body figure,#reader-body figure{margin:1.5rem 0}.story-body figcaption,#reader-body figcaption{font-size:.9rem;opacity:.75}.story-video,video{width:100%;aspect-ratio:16/9;border:0}.certificate-pdf{width:100%;height:65vh;border:0}.story-body table,#reader-body table{width:100%;border-collapse:collapse}.story-body td,.story-body th,#reader-body td,#reader-body th{padding:.5rem;border:1px solid #8886}.info-card dd{overflow-wrap:anywhere}.certificate-card .text-link{margin-top:1rem}.certificate-card img{max-width:100%}.entry-facts{margin:1rem 0}.entry-facts>div{display:grid;grid-template-columns:minmax(7rem,1fr) minmax(0,2fr);gap:.6rem;padding:.55rem 0;border-bottom:1px solid #8883}.entry-facts dt{font-size:.85rem;opacity:.75}.entry-facts dd{margin:0;overflow-wrap:anywhere}.entry-extra{margin-top:1.25rem;border-top:1px solid #8883;padding-top:1rem}.entry-extra summary{cursor:pointer;font-weight:600}.entry-extra-body{padding-top:1rem}.entry-extra img{max-width:100%;height:auto}.entry-detail-section{margin:1.4rem 0}.entry-detail-section h3{font-size:1.05rem!important;margin-bottom:.6rem}.entry-extra-body p,.entry-facts dd{overflow-wrap:anywhere}.entry-extra .button{white-space:normal}.profile-socials{flex-wrap:wrap}@media(max-width:540px){.entry-facts>div{grid-template-columns:1fr;gap:.2rem}.entry-extra .certificate-pdf{height:50vh}}''')
 for extension in ('css','js'):
  shutil.copyfile(ROOT/('scripts/editorial.'+extension),OUT/('editorial.'+extension))
  shutil.copyfile(ROOT/('scripts/hero-refresh.'+extension),OUT/('hero-refresh.'+extension))
  shutil.copyfile(ROOT/('scripts/about-refresh.'+extension),OUT/('about-refresh.'+extension))
  shutil.copyfile(ROOT/('scripts/shared-motion.'+extension),OUT/('shared-motion.'+extension))
  shutil.copyfile(ROOT/('scripts/about-awards.'+extension),OUT/('about-awards.'+extension))
  shutil.copyfile(ROOT/('scripts/about-learning.'+extension),OUT/('about-learning.'+extension))
  shutil.copyfile(ROOT/('scripts/about-exposure.'+extension),OUT/('about-exposure.'+extension))
  shutil.copyfile(ROOT/('scripts/about-headers-cv.'+extension),OUT/('about-headers-cv.'+extension))
  shutil.copyfile(ROOT/('scripts/shared-footer.'+extension),OUT/('shared-footer.'+extension))
  shutil.copyfile(ROOT/('scripts/theme.'+extension),OUT/('theme.'+extension))
  shutil.copyfile(ROOT/('scripts/shared-dock.'+extension),OUT/('shared-dock.'+extension))
  shutil.copyfile(ROOT/('scripts/shared-cursor.'+extension),OUT/('shared-cursor.'+extension))
  if extension=='css':(OUT/'page-navigation.css').write_text(navigation_css)
 gallery_source=(ROOT/'scripts/home.js').read_text().split('// Gallery filter and photo-story lightbox work independently of the carousel.')[1]
 (OUT/'gallery-runtime.js').write_text("(()=>{'use strict';const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];\n"+gallery_source)
 (OUT/'content.js').write_text((OUT/'content.js').read_text()+'\nwindow.PORTFOLIO_SITE='+json.dumps(editorial_site,ensure_ascii=False)+';\nwindow.PORTFOLIO_UI='+json.dumps(editorial_ui,ensure_ascii=False)+';\nwindow.PORTFOLIO_LABELS='+json.dumps({v:editorial_ui.get(k,v) for k,v in json.loads((ROOT/'scripts/interface-defaults.json').read_text()).items()},ensure_ascii=False)+';')
 for p in OUT.glob('*.html'):
  d=html.parse(str(p))
  for e in d.xpath('//link[@href="portfolio-foundation.css" or @href="editorial.css" or @href="hero-refresh.css" or @href="about-refresh.css" or @href="shared-motion.css" or @href="about-awards.css" or @href="about-learning.css" or @href="about-exposure.css" or @href="about-headers-cv.css" or @href="shared-footer.css" or @href="shared-cursor.css" or @href="shared-dock.css" or @href="theme.css" or @href="page-navigation.css"]|//script[@src="editorial.js" or @src="gallery-runtime.js" or @src="hero-refresh.js" or @src="about-refresh.js" or @src="shared-motion.js" or @src="about-awards.js" or @src="about-learning.js" or @src="about-exposure.js" or @src="about-headers-cv.js" or @src="shared-footer.js" or @src="shared-cursor.js" or @src="shared-dock.js" or @src="theme.js"]'):e.set('href' if e.tag=='link' else 'src',e.get('href' if e.tag=='link' else 'src')+'?v='+version)
  p.write_text(html.tostring(d,encoding='unicode',doctype='<!doctype html>'))
 from xml.sax.saxutils import escape as xml_escape
 base=editorial_site['site_url'].rstrip('/')+'/'
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml_escape(base+p.name)+'</loc></url>' for p in sorted(OUT.glob('*.html')) if not p.name.startswith('qa-') and p.stem!='404')+'</urlset>')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n')
 (OUT/'.nojekyll').touch()
 print(f'Built {len(pages)} pages, {len(details)} stories, {len(documents)} documents')
if __name__=='__main__':build()
