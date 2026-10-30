"""Scoped homepage presentation layer; original templates and other routes stay intact."""
from lxml import html, etree
import json
from datetime import date
from urllib.parse import urljoin
from copy import deepcopy

def polish(pages, profile, settings, updates, *, root, esc, url, rich, one, select, set_html):
 h=pages['index'];body=one(h,'//body');body.set('data-home-polish','true')
 def add(parent,s):
  for child in html.fragments_fromstring(s):
   if not isinstance(child,str):parent.append(child)
 def icon(name):return f'<svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><use href="#i-{name}"></use></svg>'
 def erase(e):e.getparent().remove(e)
 # Keep layout and content decisions in the build, rather than brittle runtime replacements.
 socials=one(h,'//div[@class="home-socials"]');erase(socials)
 for a in select(h,'//div[@class="hero-actions"]/a'):a.attrib.pop('data-magnetic',None)
 for a in select(h,'//a[contains(@class,"cta-link")]'):a.set('href','contact.html')
 one(h,'//div[contains(@class,"identity-caption")]/h2').set('title',profile['name'])
 # A separate stage opts out of the old, tightly clamped physics implementation.
 stage=one(h,'//div[@class="tag-stage"]');stage.set('class','physical-stage')
 one(stage,'.//span[@class="tag-hint"]').text='GRAB THE CLIP · PULL A LITTLE FURTHER'
 grip=one(stage,'.//button[@class="tag-grip"]');grip.set('aria-label','Move portrait card. Drag the clip, or use arrow keys. Escape returns it.')
 photo=one(stage,'.//div[@class="identity-photo"]');add(photo,'<span class="photo-foil" aria-hidden="true"></span>')
 caption=one(stage,'.//div[@class="identity-caption"]');name=one(caption,'.//h2');label=one(caption,'.//span[@class="tag-label"]');caption.remove(name);caption.insert(0,name)
 contacts=etree.SubElement(caption,'div',{'class':'card-contact','aria-label':'Contact Ariful'})
 icons=etree.SubElement(contacts,'div',{'class':'card-socials'})
 links=[('contact','mailto:'+profile.get('email',''),'Email '+profile['name']),('linkedin',profile.get('linkedin'),'LinkedIn'),('facebook',profile.get('facebook'),'Facebook')]
 for glyph,href,label in links:
  if url(href) and href!='mailto:':
   external=' target="_blank" rel="noopener noreferrer"' if glyph!='contact' else ''
   add(icons,f'<a class="round-control" href="{esc(url(href))}" aria-label="{esc(label)}"{external}>{icon(glyph)}</a>')
 button_link=url(settings.get('card_button_link','contact.html'))
 if button_link:add(contacts,f'<a class="card-connect" href="{esc(button_link)}">{esc(settings.get("card_button_text","Connect with me"))}</a>')
 bottom=one(caption,'.//div[@class="tag-bottom"]');caption.remove(bottom);caption.append(bottom)
 for img in select(photo,'.//img'):
  img.set('width','600');img.set('height','750');img.set('loading','eager');img.set('decoding','async');img.set('fetchpriority','high');img.set('draggable','false')
 # Full text is server rendered; reserve layers give typing the final layout from frame one.
 title=one(h,'//*[@id="home-title"]');name=(settings.get('preferred_name') or 'Ariful').upper()+'.';headline=settings.get('headline') or 'Textile engineering, with a practical mind.'
 def typed(key,text):return f'<span class="typed-line"><span class="typed-reserve" aria-hidden="true">{esc(text)}</span><span class="typed-live" data-type="{key}">{esc(text)}</span></span>'
 set_html(title,typed('name',name)+typed('headline',headline));title.set('aria-label',name+' '+headline)
 roles=[str(v).strip() for v in settings.get('roles',[]) if str(v).strip()][:12]
 if roles:
  reserve=''.join('<span class="role-reserve" aria-hidden="true">'+esc(v)+'</span>' for v in roles)
  title.addnext(html.fragment_fromstring('<div class="role-line" data-roles="'+esc(json.dumps(roles))+'"><span class="sr-only">Exploring '+esc(', '.join(roles))+'</span>'+reserve+'<span class="typed-live" data-type="roles" aria-hidden="true">'+esc(roles[0])+'</span></div>'))
 background=url(settings.get('background_image'))
 if background:
  small=url(settings.get('background_image_small'));sources=f' srcset="{esc(small)} 640w, {esc(background)} 1280w" sizes="100vw"' if small else ''
  stage=one(h,'//div[@class="home-stage"]');stage.insert(0,html.fragment_fromstring(f'<div class="hero-backdrop" aria-hidden="true"><img src="{esc(background)}"{sources} alt="" width="1280" height="853" decoding="async" fetchpriority="low"></div>'))
 # Two independently looping rows; the original single track remains the accessible slideshow.
 for showcase in select(h,'//div[@class="moments-carousel"]'):
  showcase.set('class','moments-showcase is-slideshow');showcase.set('data-default-mode',settings.get('gallery_mode') or 'Marquee')
  track=one(showcase,'.//div[@class="moments-track"]');track.set('class','slideshow-track');track.set('aria-label','Photo slideshow. Use left and right arrow keys or the previous and next buttons.')
  slides=list(track);wall=html.Element('div',{'class':'marquee-wall','aria-hidden':'true','hidden':''})
  for row in range(2):
   viewport=etree.SubElement(wall,'div',{'class':'marquee-row'});belt=etree.SubElement(viewport,'div',{'class':'marquee-belt'})
   selected=slides[row::2] or slides
   # At least three cells per group, even with a small personal collection.
   while len(selected)<3:selected=selected+selected
   for repeat in range(2):
    group=etree.SubElement(belt,'div',{'class':'marquee-group'})
    for original in selected:
     clone=deepcopy(original)
     for button in clone.xpath('.//button'):button.set('tabindex','-1')
     group.append(clone)
  showcase.insert(0,wall)
  controls=one(showcase,'.//div[@class="moments-controls"]');set_html(controls,f'<button class="gallery-mode" data-gallery-mode aria-pressed="true">Slideshow</button><button class="gallery-pause" data-gallery-pause aria-pressed="false">Pause motion</button><div class="slideshow-controls"><button class="round-control" data-slide-prev aria-label="Previous moments">{icon("left")}</button><span class="slide-position" role="status"></span><button class="round-control" data-slide-next aria-label="Next moments">{icon("right")}</button></div>')
  add(controls,'<span class="gallery-mode-help">Switch to Slideshow to browse with a keyboard or swipe.</span>')
 # A dated feed replaces the old generic overview cards on the homepage only.
 topics=['Content creation','Research','Fabric testing','Apparel manufacturing'];items=sorted(updates,key=lambda u:str(u.get('date') or ''),reverse=True)
 chips=''.join(f'<button class="update-filter" data-update-filter="{esc(t)}" aria-pressed="{str(i==0).lower()}">{esc(t)}</button>' for i,t in enumerate(['All']+topics))
 cards=[]
 for i,u in enumerate(items):
  raw=str(u.get('date') or '')[:10];valid_date=False
  try:label=date.fromisoformat(raw).strftime('%d %b %Y').lstrip('0');valid_date=True
  except ValueError:label=raw
  sample='<span class="update-sample">Sample update</span>' if u.get('sample') else ''
  stamp=f'<time datetime="{esc(raw)}">{esc(label)}</time>' if valid_date else (f'<span>{esc(label)}</span>' if label else '')
  date_block=f'<div class="update-date">{stamp}{sample}</div>' if stamp or sample else ''
  picture=f'<img class="update-photo" src="{esc(url(u["image"]))}" alt="{esc(u.get("image_alt") or u["title"])}" loading="lazy" width="320" height="200">' if url(u.get('image')) else ''
  link=f'<a class="text-link" href="{esc(url(u["link"]))}">Read more<span class="sr-only">: {esc(u["title"])}</span> {icon("arrow")}</a>' if url(u.get('link')) else ''
  prefix=('On '+esc(label)+', ') if label else ''
  text=str(u.get('text') or '').strip()
  narrative=('<p>'+prefix+'this example illustrates how a new update will appear.</p>' if u.get('sample') else '')
  if text:narrative+='<p>'+('' if u.get('sample') else prefix)+esc(text)+'</p>'
  hidden=' hidden' if i>=3 else ''
  topic=esc(u.get('topic') or topics[0])
  cards.append(f'<article class="update-entry" data-reveal data-update-topic="{topic}"{hidden}>{date_block}<div class="update-copy"><span class="update-topic">{topic}</span><h3>{esc(u["title"])}</h3>{narrative}{link}</div>{picture}</article>')
 markup='<section class="section updates-section" id="updates" aria-labelledby="updates-title"><header class="section-heading"><span class="section-label">THE LATEST THREADS</span><h2 id="updates-title">'+esc(settings.get('updates_heading') or 'A few threads in progress.')+'</h2><p>'+esc(settings.get('updates_intro'))+'</p></header><div class="update-filters" role="group" aria-label="Filter updates by topic">'+chips+'</div><div class="updates-feed">'+''.join(cards)+'</div><p class="updates-empty"'+(' hidden' if cards else '')+'>No updates here yet. There will be more to share soon.</p><p class="updates-count" role="status">'+str(min(3,len(cards)))+' latest updates</p></section>'
 old=one(h,'//main//section[contains(@class,"section") and not(contains(@class,"cta-section")) and not(contains(@class,"moments"))]');old.getparent().replace(old,html.fragment_fromstring(markup))
 for e in select(h,'//div[@class="skills-marquee"]'):erase(e)
 # Only the homepage symbol library is replaced; original vectors remain on other routes.
 library=one(h,'//svg[@class="icon-library"]')
 for child in list(library):library.remove(child)
 manifest=json.loads((root/'vendor/home-icons/sources.json').read_text())
 for key,asset in manifest.items():
  svg=etree.parse(str(root/'vendor/home-icons'/asset['file'])).getroot()
  symbol=etree.SubElement(library,'symbol',id='i-'+key,viewBox=svg.get('viewBox'),fill='currentColor')
  for path in svg.iter():
   if isinstance(path.tag,str) and etree.QName(path).localname in ('path','polygon','circle','rect','ellipse','polyline','line'):
    item=deepcopy(path);item.tag=etree.QName(item).localname
    for key in ('id','style','fill','stroke'):item.attrib.pop(key,None)
    if path.get('fill')=='none':continue
    symbol.append(item)
 rail=one(h,'//aside[@class="site-rail"]');nav=one(rail,'.//nav');rail.insert(0,nav)
 menu=one(rail,'.//button[contains(@class,"menu-trigger")]');one(h,'//header[contains(@class,"site-header")]').append(menu)
 for u in select(h,'//*[@id="back-top"]//use'):u.set('href','#i-up')
 add(nav,'<span class="rail-marker" aria-hidden="true"></span>')
 one(h,'//div[@class="home-stage"]').set('id','home-top')
 # Finishing copy and social metadata all come from editable profile/homepage values.
 footer=one(h,'//footer');set_html(footer,'<span>© <span data-year>2026</span> '+esc(profile['name'])+'. · Made with curiosity. Woven with care.</span>')
 for e in select(h,'//*[@class="ghost-word"]'):erase(e)
 for e in select(h,'//canvas[@id="woven-canvas"]|//*[contains(@class,"cursor-dot") or contains(@class,"cursor-ring") or contains(@class,"cursor-label")]'):e.set('hidden','')
 for e in select(h,'//section[@class="section cta-section"]'):e.set('id','connect')
 head=one(h,'//head');title=settings.get('seo_title') or profile['name']+' — Textile Engineering & Curious Making';one(h,'//title').text=title
 description=settings.get('seo_description') or html.fragment_fromstring('<div>'+rich(settings.get('description'))+'</div>').text_content().strip()
 one(h,'//meta[@name="description"]').set('content',description)
 site=url(settings.get('site_url')) or 'https://arifulislamfahim04.github.io/arif-portfolio-studio/'
 for prop,value in [('og:type','website'),('og:title',title),('og:description',description),('og:url',site),('twitter:card','summary_large_image')]:
  add(head,'<meta '+('name' if prop.startswith('twitter:') else 'property')+'="'+prop+'" content="'+esc(value)+'">')
 social_image=url(settings.get('social_image') or profile.get('photo'))
 if social_image:add(head,'<meta property="og:image" content="'+esc(urljoin(site,social_image))+'"><meta property="og:image:alt" content="'+esc(profile.get('photo_alt') or profile['name'])+'">')
 add(head,'<link rel="canonical" href="'+esc(site)+'"><link rel="icon" type="image/svg+xml" href="assets/home-favicon.svg">')
 for e in select(h,'//link[@href="site.css"]'):e.set('href','home-base.css')
 for e in select(h,'//script[@src="site.js"]'):e.set('src','home-core.js')
 for family in ('display','text'):add(head,f'<link rel="preload" as="font" type="font/woff" href="assets/fonts/{family}.woff" crossorigin="anonymous">')
 # These assets are only loaded on index: other pages retain their existing design.
 add(one(h,'//head'),'<link rel="stylesheet" href="home-polish.css">')
 add(body,'<script src="home-polish.js" defer></script>')
