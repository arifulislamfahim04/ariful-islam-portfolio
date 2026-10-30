"""A shared editorial presentation of the existing Pages CMS portfolio.
The original templates, collections, URLs and rich-content sanitizer remain the source.
"""
from copy import deepcopy
from lxml import html,etree
from pathlib import Path
from urllib.parse import quote,urljoin,urlsplit
from datetime import date
import json,re,hashlib
from navigation import read_navigation, DEFAULT_NAV

NAV=[('index','Home','home'),('about','About','about'),('projects','Projects','projects'),('gallery','Gallery','gallery'),('blogs','Blogs','blogs'),('contact','Contact','contact')]

def redesign(pages,profile,about,settings,*,root,esc,url,rich,one,select,set_html,entries,story_body,date_text):
 NAV=read_navigation(root)
 site=json.loads((root/'editor/site.json').read_text()); ui=json.loads((root/'editor/interface.json').read_text()); meta=json.loads((root/'editor/pages.json').read_text())
 def t(text):return esc(ui.get(hashlib.sha1(text.encode()).hexdigest()[:10],text))
 def icon(key):return f'<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><use href="#i-{key}"></use></svg>'
 def erase(e):
  if e.getparent() is not None:e.getparent().remove(e)
 def add(e,s):
  for n in html.fragments_fromstring(s):
   if not isinstance(n,str):e.append(n)
 def image(src,alt,cls='',eager=False):
  return f'<img class="{cls}" src="{esc(url(src))}" alt="{esc(alt)}" width="960" height="720" loading="{"eager" if eager else "lazy"}" decoding="async">' if url(src) else ''
 def link(dest,text,cls='text-link',glyph='arrow',external=False):
  return f'<a class="{cls}" href="{esc(url(dest))}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'>{text} {icon(glyph)}</a>' if url(dest) else ''
 def social_links():
  return ''.join(f'<a class="round-control" href="{esc(url(dest))}" aria-label="{label}"'+(' target="_blank" rel="noopener noreferrer"' if key!='contact' else '')+f'>{icon(key)}</a>' for key,dest,label in [('linkedin',profile.get('linkedin'),'LinkedIn'),('contact','mailto:'+profile.get('email',''),'Email '+profile['name']),('facebook',profile.get('facebook'),'Facebook')] if url(dest) and dest!='mailto:')
 def heading(kicker,title,intro=''):
  return '<header class="section-heading" data-reveal><span class="section-label">'+esc(kicker)+'</span><h2>'+esc(title)+'</h2>'+('<p>'+esc(intro)+'</p>' if intro else '')+'</header>'
 def section_top(kicker,title,dest='',label='',intro=''):
  return '<div class="section-top" data-reveal><div><span class="section-label">'+esc(kicker)+'</span><h2>'+esc(title)+'</h2>'+('<p>'+esc(intro)+'</p>' if intro else '')+'</div>'+link(dest,esc(label))+'</div>'
 def nav_markup(current):
  return ''.join(f'<a href="{page}.html"'+(' aria-current="page"' if current==page else '')+f'>{icon(glyph) if page=="index" else ""}{t(label)}</a>' for page,label,glyph in NAV)
 # Use the chosen Phosphor filled pack, with a single 256-square viewBox everywhere.
 manifest=json.loads((root/'vendor/home-icons/sources.json').read_text())
 aliases={'message':'contact','mail':'contact','play':'right','pause':'menu','spark':'focus','sparkles':'focus','briefcase':'projects','external':'arrow','quality':'research','ai':'focus','chart':'research','thread':'fabric','heart':'award','code':'projects','plus':'zoom','sun-moon':'sun','resume':'download'}
 symbol_keys=set(manifest)
 for d in pages.values():symbol_keys.update(d.xpath('//svg[@class="icon-library"]/symbol/@id'))
 for key in list(symbol_keys):
  if key.startswith('i-'):symbol_keys.remove(key);symbol_keys.add(key[2:])
 sprite=etree.Element('svg',{'class':'icon-library','aria-hidden':'true','xmlns':'http://www.w3.org/2000/svg'})
 for key in sorted(symbol_keys):
  asset=manifest.get(key) or manifest[aliases.get(key,'focus')]
  svg=etree.parse(str(root/'vendor/home-icons'/asset['file'])).getroot();sym=etree.SubElement(sprite,'symbol',id='i-'+key,viewBox='0 0 256 256',fill='currentColor')
  for node in svg.iter():
   if isinstance(node.tag,str) and etree.QName(node).localname in ('path','polygon','circle','rect','ellipse','polyline','line'):
    n=deepcopy(node);n.tag=etree.QName(n).localname
    for a in ('id','style','fill','stroke'):n.attrib.pop(a,None)
    if node.get('fill')!='none':sym.append(n)
 for name,d in pages.items():
  body=one(d,'//body');body.attrib.pop('data-home-polish',None);body.attrib.pop('data-home-redesign',None);body.set('data-editorial','true')
  current=name if name in dict((p,l) for p,l,g in DEFAULT_NAV) else 'blogs' if name.startswith('posts-') else 'projects';body.set('data-page',current)
  # Retain data/content and gallery business logic, replace legacy chrome/motion only.
  for e in select(d,'//head/link[@rel="stylesheet"]|//script[@src and not(starts-with(@src,"content.js"))]|//head/script|//canvas|//div[contains(@class,"cursor-")]|//span[contains(@class,"cursor-")]|//div[@class="page-wipe"]|//aside[@class="site-rail"]|//*[contains(@class,"ghost-word")]'):erase(e)
  lib=one(d,'//svg[@class="icon-library"]');lib.getparent().replace(lib,deepcopy(sprite))
  for svg in select(d,'//svg[contains(concat(" ",@class," ")," icon ")]'):
   for attr in ('viewbox','stroke','stroke-width','stroke-linecap','stroke-linejoin'):svg.attrib.pop(attr,None)
   svg.set('viewBox','0 0 256 256');svg.set('fill','currentColor')
  header=one(d,'//header[contains(@class,"site-header")]');header.set('class','site-header')
  set_html(header,f'<a class="logo" href="index.html" aria-label="{esc(profile["name"])} {t("home")}">{esc(settings.get("logo_text") or "ariful")}<span>.</span></a><nav class="header-nav" aria-label="{t("Main navigation")}">'+nav_markup(current)+f'</nav><div class="header-actions"><button class="round-control command-trigger" aria-label="{t("Search site (Ctrl K)")}">{icon("search")}<kbd>Ctrl K</kbd></button><button class="round-control theme-toggle" aria-label="{t("Theme: light. Switch to dark.")}">{icon("sun")}</button><button class="round-control menu-trigger" aria-label="{t("Open menu")}" aria-haspopup="dialog" aria-controls="site-menu">{icon("menu")}</button></div>')
  menu=one(d,'//*[@id="site-menu"]');set_html(menu,f'<div class="menu-top"><a class="logo" href="index.html">{esc(profile["name"])}</a><button class="round-control" data-close aria-label="{t("Close menu")}">{icon("close")}</button></div><nav class="menu-links" aria-label="{t("Mobile navigation")}">'+nav_markup(current)+f'</nav><div class="menu-bottom">'+link('mailto:'+profile['email'],esc(profile['email']),glyph='contact')+f'<p>{esc(profile["location"])}</p></div>')
  for i,a in enumerate(select(menu,'.//nav/a')):a.set('style',f'--i:{i}')
  footer=one(d,'//footer');footer.set('class','site-footer shell');set_html(footer,'<div class="footer-top"><a class="logo" href="index.html">'+esc(profile['name'])+'</a><nav aria-label="'+t('Footer navigation')+'">'+nav_markup(current)+'</nav></div><div class="footer-bottom"><span>© <span data-year>2026</span> '+esc(profile['name'])+'. · '+esc(site['footer_text'])+'</span><span class="footer-mark">'+esc(site['footer_mark'])+'</span></div>')
  # Commands retain page navigation, CV, theme and email; add real post/project results.
  commands=one(d,'//div[@class="command-results"]');set_html(commands,''.join(f'<a href="{p}.html" data-command>{icon(g)}{t(l)}</a>' for p,l,g in NAV)+link(profile['resume'],t('Download CV'),glyph='download')+f'<button data-theme-command data-command>{icon("sun")}{t("Change theme")}</button>'+link('mailto:'+profile['email'],t('Email me'),glyph='contact'))
  for a in commands:a.set('data-command','')
  for folder in ('projects','posts'):
   for item in entries(folder):add(commands,link(item['_id']+'.html',esc(item['title']),glyph='projects' if folder=='projects' else 'blogs'))
  for a in commands:a.set('data-command','')
  back=etree.SubElement(body,'button',{'id':'back-top','class':'back-top','aria-label':'Back to top'});set_html(back,'<svg class="progress-ring" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="21" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"></circle></svg>'+icon('up'))
  etree.SubElement(body,'div',{'class':'thread-field','aria-hidden':'true'})
  # Restore consistent titles / metadata. Individual story overrides stay with their entry.
  pm=meta.get(current,{}) if name==current else {}; entry=next((v for v in entries('posts' if current=='blogs' else 'projects') if v['_id']==name),{}) if name!=current else {}
  page_title=entry.get('seo_title') or entry.get('title') or pm.get('title') or current.title()
  description=entry.get('seo_description') or entry.get('summary') or pm.get('description') or site['description']
  one(d,'//title').text=page_title+' — '+profile['name']
  for e in select(d,'//meta[@name="description" or @name="theme-color" or starts-with(@property,"og:") or starts-with(@name,"twitter:")]|//link[@rel="canonical" or @rel="icon"]'):erase(e)
  head=one(d,'//head');base=site['site_url'].rstrip('/')+'/';canonical=urljoin(base,name+'.html');social=url(entry.get('social_image') or pm.get('social_image') or site.get('social_image') or profile.get('photo'))
  add(head,f'<meta name="description" content="{esc(description)}"><meta name="theme-color" content="#f5efe6"><meta property="og:type" content="{"article" if entry else "website"}"><meta property="og:title" content="{esc(page_title)} — {esc(profile["name"])}"><meta property="og:site_name" content="{esc(site["site_name"])}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(page_title)} — {esc(profile["name"])}"><meta name="twitter:description" content="{esc(description)}"><link rel="canonical" href="{esc(canonical)}"><link rel="icon" href="assets/home-favicon.svg" type="image/svg+xml">')
  if social:add(head,f'<meta property="og:image" content="{esc(urljoin(base,social))}"><meta property="og:image:alt" content="{esc(profile.get("photo_alt") or profile["name"])}"><meta name="twitter:image" content="{esc(urljoin(base,social))}">')
  # Resolve the saved/system preference before styles can paint.
  early=html.Element('script',{'data-theme-init':''});early.text=(root/'scripts/theme-init.js').read_text();head.insert(1,early)
  add(head,'<link rel="preload" href="assets/editorial-fonts/fraunces.woff" as="font" type="font/woff" crossorigin="anonymous"><link rel="preload" href="assets/editorial-fonts/dmsans.woff" as="font" type="font/woff" crossorigin="anonymous"><link rel="stylesheet" href="editorial.css">')
  if name==current and current!='index':
   headers=select(d,'//main//header[.//h1]')
   if headers:
    sh=headers[0];set_html(sh,'<span class="section-label">'+esc(pm.get('eyebrow'))+'</span><h1>'+esc(pm.get('heading') or page_title)+'</h1>'+('<p>'+esc(pm['intro'])+'</p>' if pm.get('intro') else ''))
  for img in select(d,'//img'):
   if not img.get('width'):img.set('width','960')
   if not img.get('height'):img.set('height','720')
   img.set('decoding','async')
  for e in select(d,'//meta[@name="viewport"]'):e.set('content','width=device-width, initial-scale=1, viewport-fit=cover')
  add(body,'<script src="editorial.js" defer></script><script src="gallery-runtime.js" defer></script>')
  # Fixed layout copy inherited from templates can also be edited without code.
  for e in select(d,'//main//*[not(self::script or self::style)]|//dialog//*'):
   for attr in ('placeholder','aria-label'):
    if e.get(attr):e.set(attr,ui.get(hashlib.sha1(e.get(attr).encode()).hexdigest()[:10],e.get(attr)))
   for attr in ('text','tail'):
    old=getattr(e,attr)
    if old and old.strip():
     stripped=old.strip();key=hashlib.sha1(stripped.encode()).hexdigest()[:10]
     if key in ui:setattr(e,attr,old.replace(stripped,ui[key]))
 # Home reuses existing CMS material and routes, in the requested short landing sequence.
 h=pages['index'];main=one(h,'//main');set_html(main,'');main.set('class','page-content-home')
 phrases=[v.strip() for v in settings.get('typewriter_phrases',[]) if v.strip()] or ["I'm Ariful."]
 portrait=image(profile.get('photo'),profile.get('photo_alt') or profile['name'],'identity-portrait',True) or '<div class="identity-monogram">'+esc(''.join(v[0] for v in profile['name'].split()[:2]))+'</div>'
 chips=''.join('<span class="status-chip">'+esc(v)+'</span>' for v in settings.get('status_chips',[]) if v)
 reserve=''.join('<span class="phrase-reserve" aria-hidden="true">'+esc(v)+'</span>' for v in phrases)
 add(main,'<section class="home-hero shell"><div class="profile-column" data-reveal><article class="compact-profile" data-tilt><div class="compact-photo">'+portrait+'<span class="portrait-corner" aria-hidden="true">a.</span></div><h2>'+esc(profile['name'])+'</h2><div class="profile-chips">'+chips+'</div></article><div class="profile-contact">'+social_links()+'</div>'+link('contact.html',esc(settings.get('card_button_text') or 'Contact me'),'button secondary','contact')+'</div><div class="hero-copy" data-reveal><p class="eyebrow">'+esc(settings.get('eyebrow'))+'</p><h1 class="loop-headline" id="home-title" aria-label="'+esc(' '.join(phrases))+'" data-phrases="'+esc(json.dumps(phrases))+'">'+reserve+'<span class="phrase-live" aria-hidden="true">'+esc(phrases[0])+'</span></h1><div class="hero-intro">'+rich(settings.get('description'))+'</div><div class="hero-actions">'+link(profile['resume'],t('Download CV'),'button primary','download')+link('projects.html',t('View projects'),'button secondary','projects')+'</div><div class="location-clock">'+icon('location')+'<span>'+esc(profile['location'])+'</span><time data-dhaka-time></time></div></div></section>')
 stats=''
 for s in profile.get('stats',[])[:4]:
  value=str(s.get('value') or '0');dec=max(0,min(3,int(s.get('decimals') or 0)))
  stats+='<div class="slim-stat"><strong><b data-count="'+esc(value)+'" data-decimals="'+str(dec)+'">'+esc(value)+'</b><small>'+esc(s.get('suffix'))+'</small></strong><span>'+esc(s.get('label'))+'</span></div>'
 if stats:add(main,'<div class="slim-stats shell" data-reveal>'+stats+'</div>')
 updates=sorted(entries('updates'),key=lambda u:str(u.get('date') or ''),reverse=True)
 if updates:
  items=''.join('<a href="#update-'+esc(u['_id'])+'">'+esc(u.get('ticker_text') or u['title'])+'</a>' for u in updates)
  ticker='<div class="news-ticker"><span class="ticker-label">'+esc(settings.get('ticker_label') or 'Highlights')+'</span><div class="ticker-viewport"><div class="ticker-belt"><div class="ticker-group">'+items+'</div><div class="ticker-group" aria-hidden="true">'+items.replace('<a ','<a tabindex="-1" ')+'</div></div></div><button class="ticker-toggle" aria-pressed="false">'+t('Pause')+'</button></div>'
  news=''
  # Every ticker destination exists, even beyond the three initially expanded cards.
  for i,u in enumerate(updates):
   raw=str(u.get('date') or '');formatted=readable_date(raw);sample='<span class="sample-label">'+t('Sample update')+'</span>' if u.get('sample') else ''
   news+='<details class="news-card" id="update-'+esc(u['_id'])+'"'+(' hidden data-extra-update' if i>=3 else '')+'><summary><time datetime="'+esc(raw)+'">'+esc(formatted)+'</time>'+sample+'<h3>'+esc(u['title'])+'</h3><p>'+esc(u.get('text'))+'</p><span class="text-link">'+t('View details')+' '+icon('down')+'</span></summary><div class="news-detail"><span class="section-label">'+esc(u.get('topic'))+'</span>'+image(u.get('image'),u.get('image_alt') or u['title'])+link(u.get('link'),t('Read more'))+'</div></details>'
  add(main,'<section class="home-section shell" id="highlights">'+ticker+section_top(t('THE LATEST THREADS'),settings.get('updates_heading'),intro=settings.get('updates_intro'))+'<div class="latest-updates">'+news+'</div></section>')
 else:add(main,'<section class="home-section shell">'+section_top(settings.get('ticker_label'),settings.get('updates_heading'))+'<p>'+t('No updates here yet. There will be more to share soon.')+'</p></section>')
 def features(folder,page,title):
  originals=select(pages[page],'//article[contains(@class,"project-card") or contains(@class,"blog-card")]');items=entries(folder);chosen=[v for v in items if v.get('featured',True)][:3];nodes=[]
  for v in chosen:
   match=next((n for n in originals if n.xpath('.//a[@href="'+v['_id']+'.html"]')),None)
   if match is not None:nodes.append(deepcopy(match))
  if nodes:
   sec=html.fragment_fromstring('<section class="home-section shell">'+section_top(t('SELECTED THREADS' if folder=='projects' else 'FROM THE NOTEBOOK'),title,page+'.html',t('All projects' if folder=='projects' else 'All notes'))+'<div class="feature-grid"></div></section>')
   sec[-1].extend(nodes);main.append(sec)
 features('projects','projects',settings['projects_heading'])
 moments=[m for m in entries('gallery') if url(m.get('image')) and m.get('featured',True)][:max(1,int(settings.get('gallery_limit') or 6))]
 if moments:
  wall=''
  for row in range(2):
   chosen=moments[row::2] or moments
   while len(chosen)<3:chosen=chosen+chosen
   group=''.join('<a href="gallery.html#'+esc(m['_id'])+'">'+image(m['image'],m.get('alt') or m['title'])+('<span class="sample-label">'+t('Sample image')+'</span>' if m.get('placeholder') else '')+'<span class="preview-caption">'+esc(m['title'])+'</span></a>' for m in chosen)
   wall+='<div class="preview-row"><div class="preview-belt"><div class="preview-group">'+group+'</div><div class="preview-group" aria-hidden="true">'+group.replace('<a ','<a tabindex="-1" ')+'</div></div></div>'
  add(main,'<section class="home-section shell moments-section">'+section_top(t('MOMENTS, COLLECTED'),settings['gallery_heading'],'gallery.html',t('Explore the gallery'))+'<div class="preview-wall">'+wall+'</div><div class="preview-controls"><button data-preview-pause aria-pressed="false">'+t('Pause gallery motion')+'</button></div></section>')
 add(main,'<section class="home-section shell home-about" data-reveal><div><span class="section-label">'+t('A LITTLE ABOUT ME')+'</span><h2>'+esc(settings['about_teaser_heading'])+'</h2></div><div class="teaser-body">'+rich(settings['about_teaser'])+link('about.html',t('More about me'))+'</div></section>')
 features('posts','blogs',settings['notes_heading'])
 add(main,'<section class="closing-cta shell" data-reveal><div><span class="section-label">'+t('THE NEXT THREAD')+'</span><h2>'+esc(settings['closing_heading'])+'</h2>'+rich(profile['call_to_action'])+'</div>'+link('contact.html',t('Contact me'),'button primary','contact')+'</section>')
 for a in select(h,'//div[@class="hero-actions"]/a[1]'):
  if not urlsplit(url(profile.get('resume'))).scheme:a.set('download','')
 # About: keep all original entries, add structure and opt-in public reference/transcript controls.
 a=pages['about'];container=one(a,'//main/div');container.set('class','page-content shell')
 sections=select(container,'./section');intro=[e for e in list(container) if e not in sections]
 content=html.Element('div',{'class':'about-body'});sidebar=html.Element('nav',{'class':'section-index','aria-label':'About sections'})
 for e in sections:
  label=e.xpath('string(.//h2)') or e.get('id');add(sidebar,'<a href="#'+esc(e.get('id'))+'">'+esc(site.get('about_index',{}).get(e.get('id')) or label)+'</a>');content.append(e)
 for e in list(container):
  if e in intro:continue
  container.remove(e)
 layout=html.Element('div',{'class':'about-layout'});layout.append(sidebar);layout.append(content);container.append(layout)
 # Keep the secondary photo, caption and alt text under CMS control.
 for box in select(a,'//div[contains(@class,"bio-fabric")]'):
  src=url(profile.get('secondary_image'))
  if src:
   one(box,'.//img').set('src',src)
   if 'image_alt' in about:one(box,'.//img').set('alt',about['image_alt'])
   if 'image_caption' in about:one(box,'.//span').text=about['image_caption']
  else:erase(box)
 for folder,section_id in [('education','education'),('experience','experience'),('workshops','certificates')]:
  for v in entries(folder):
   targets=select(a,'//section[@id="'+section_id+'"]//article[@data-entry-id="'+esc(v['_id'])+'"]')
   for card in targets:
    institution=select(card,'./p[@class="institution"]');website=url(v.get('website') or v.get('organization_url'))
    if institution and website:set_html(institution[0],link(website,esc(v.get('institution')),'institution-link','arrow',True))
    for summary in select(card,'.//summary'):summary.text=ui.get(hashlib.sha1(b'View details').hexdigest()[:10],'View details')
    if not select(card,'.//details') and rich(v.get('body')):
     detail=html.Element('details',{'class':'entry-extra'});set_html(detail,'<summary>'+t('View details')+'</summary><div class="entry-extra-body">'+rich(v.get('body'))+'</div>');card.append(detail)
     for old in select(card,'./p[not(@class="institution")]'):erase(old)
    if v.get('file'):add(card,'<button class="text-link" data-document="'+esc(v['_id'])+'">'+t('View certificate')+' '+icon('certificate')+'</button>')
 for folder,section_id in [('achievements','recognition'),('certificates','certificates')]:
  for v in entries(folder):
   for card in select(a,'//section[@id="'+section_id+'"]//article[@data-entry-id="'+esc(v['_id'])+'"]'):
    for button in select(card,'.//button[@data-document]'):erase(button)
    details_html=story_body(v,folder)
    if details_html:
     detail=html.Element('details',{'class':'entry-extra'});set_html(detail,'<summary>'+t('View details')+'</summary><div class="entry-extra-body">'+details_html+'</div>');card.append(detail)
     for old in select(card,'./p[not(@class="institution")]'):erase(old)
    if v.get('file'):add(card,'<button class="text-link" data-document="'+esc(v['_id'])+'">'+t('View certificate')+' '+icon('certificate')+'</button>')
    institution=select(card,'./p[@class="institution"]')
    if institution and url(v.get('website')):set_html(institution[0],link(v['website'],esc(v.get('institution')),'institution-link','arrow',True))
 for grid in select(a,'//section[@id="recognition"]/div[@class="certificate-grid"]'):grid.set('class','recognition-shelf');grid.set('tabindex','0');grid.set('aria-label','Awards. Swipe horizontally to explore each separate award.')
 for i,skill in enumerate(select(a,'//article[contains(@class,"skill-card")]')):skill.insert(0,html.fragment_fromstring(icon(['research','fabric','projects'][i%3])))
 for el in select(a,'//details[contains(@class,"academic-references")]'):erase(el)
 refs=[r for r in about.get('references',[]) if r.get('show_publicly',False)]
 refsection=one(a,'//*[@id="recommendations"]')
 if refs:add(refsection,'<div class="reference-grid">'+''.join('<article class="reference-card glass">'+rich(r.get('body'))+'</article>' for r in refs)+'</div>')
 else:add(refsection,'<p class="privacy-note">'+esc(about.get('references_notice') or 'References available on request')+'</p>')
 if not about.get('transcript_public',False):
  for e in select(a,'//div[@class="transcript-action"]'):erase(e)
 # Contact: update every location occurrence and map query from the profile.
 c=pages['contact'];phone=re.sub(r'\D','',profile.get('phone',''));formatted=('+880 '+phone[3:7]+' '+phone[7:]) if phone.startswith('880') and len(phone)==13 else profile.get('phone','')
 direct=one(c,'//div[@class="direct-contacts"]')
 for item in select(direct,'./article'):
  heading=one(item,'.//h3').text_content().lower();target=one(item,'.//a')
  if heading=='phone':target.text=formatted
  if heading=='location':target.text=profile['location'];target.set('href','https://www.google.com/maps/search/?api=1&query='+quote(profile['location']));one(item,'.//button[@data-copy]').set('data-copy',profile['location'])
 if phone:add(direct,f'<article class="direct-contact glass"><span class="icon-badge">{icon("whatsapp")}</span><div><h3>WhatsApp</h3>'+link('https://wa.me/'+phone,formatted,'whatsapp-link','arrow',True)+'</div><button class="copy-control" data-copy="'+esc('+'+phone)+'" aria-label="'+t('Copy WhatsApp number')+'">'+icon('copy')+'</button></article>')
 for old in select(c,'//details[contains(@class,"map-module") or contains(@class,"map-panel")]'):erase(old)
 contact_layout=one(c,'//div[@class="contact-layout"]');add(contact_layout.getparent(),'<details class="map-module"><summary>'+icon('location')+' '+esc(profile['location'])+' · '+t('Explore the map')+'</summary><div class="map-canvas"><iframe title="'+t('Map of')+' '+esc(profile['location'])+'" src="https://maps.google.com/maps?q='+quote(profile['location'])+'&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'+link('https://www.google.com/maps/search/?api=1&query='+quote(profile['location']),t('Open in Maps'),'map-open','arrow',True)+'</details>')
 form=one(c,'//form');form.set('data-provider',site['form_provider']);form.set('data-endpoint',site.get('formspree_endpoint',''));form.set('data-access-key',site.get('web3forms_access_key',''));add(form,'<label class="honeypot" aria-hidden="true">'+t('Leave this field empty')+'<input name="_gotcha" tabindex="-1" autocomplete="off"></label><p class="form-status" role="status" aria-live="polite"></p>')
 for success in select(form,'.//div[@class="form-success"]'):erase(success)
 if site['form_provider']!='Email app':
  for note in select(form,'.//p[@class="form-note"]'):note.text=site['form_note']
 # Story enhancements preserve full body, own images, reports and optional metadata.
 for folder,page in [('posts','blogs'),('projects','projects')]:
  items=entries(folder)
  for i,v in enumerate(items):
   single=pages[v['_id']];article=one(single,'//main/article');body=one(article,'.//div[@class="story-body"]')
   raw=str(v.get('date') or '');plain=html.fragment_fromstring('<div>'+rich(v.get('body'))+'</div>').text_content();minutes=max(1,len(plain.split())//200)
   actions='<div class="story-actions"><span>'+esc(readable_date(raw))+((' · '+str(minutes)+' '+t('min read')) if folder=='posts' else '')+'</span>'+(('<button class="round-control" data-share aria-label="'+t('Share this page')+'">'+icon('arrow')+'</button>') if v.get('share_enabled',True) else '')+'</div>'
   body.addprevious(html.fragment_fromstring(actions))
   if folder=='projects':
    facts=[(t('Tools'),', '.join(v.get('tools') or [])),(t('Duration'),v.get('duration') or '')]
    if any(value for label,value in facts):body.addprevious(html.fragment_fromstring('<dl class="story-facts">'+''.join('<div><dt>'+label+'</dt><dd>'+esc(value)+'</dd></div>' for label,value in facts if value)+'</dl>'))
   if v.get('summary'):body.addprevious(html.fragment_fromstring('<p class="entry-summary">'+esc(v['summary'])+'</p>'))
   if folder=='posts':
    add(article,'<aside class="author-bio"><strong>'+esc(v.get('author') or profile['name'])+'</strong><p>'+esc(site['author_bio'])+'</p></aside>')
    related=[p for p in items if p['_id']!=v['_id']][:2]
    if related:add(article,'<section class="section"><h2>'+t('More from the notebook')+'</h2><div class="related-grid">'+''.join(link(p['_id']+'.html',esc(p['title'])) for p in related)+'</div></section>')
   elif len(items)>1:add(article,link(items[(i+1)%len(items)]['_id']+'.html',t('Next project')+' · '+esc(items[(i+1)%len(items)]['title']),'story-next'))
  # Category slugs remain stored unchanged; human labels are explicit, editable aliases.
  if folder=='projects':
   labels=site['project_categories'];d=pages[page];filters=one(d,'//div[contains(@class,"filter-bar")]');keys=['all']+list(labels)
   for item in items:
    if item.get('category') and item['category'] not in keys:keys.append(item['category'])
   set_html(filters,''.join('<button class="filter'+(' active' if k=='all' else '')+'" data-project-filter="'+esc(k)+'" aria-pressed="'+str(k=='all').lower()+'">'+(t('All') if k=='all' else esc(labels.get(k,k)))+'</button>' for k in keys))
   grid=one(d,'//div[@class="project-grid"]');grid.addnext(html.fragment_fromstring('<p class="search-empty" id="project-empty" hidden>'+t('No projects match your search.')+'</p>'))
   # Search is additive, alongside the existing project filters.
   filters.addprevious(html.fragment_fromstring('<label class="search-box"><span class="sr-only">'+t('Search projects')+'</span><input type="search" id="project-search" placeholder="'+t('Search projects…')+'"></label>'))
  else:
   for doc in pages.values():
    for item in select(doc,'//div[@class="blog-meta"]'):item.text=readable_date(item.text_content())
 # Remove redundant destination CTAs only on their target page.
 for e in select(pages['gallery'],'//dialog[@id="moment-viewer"]//a[@href="gallery.html"]'):erase(e)
 for page in pages.values():
  for el in select(page,'//a[starts-with(@href,"tel:")]'):el.text=formatted
  for label in select(page,'//dl//dt'):
   if label.text_content().strip().lower()=='based in':
    siblings=label.xpath('following-sibling::dd')
    if siblings:siblings[0].text=profile['location']
  for el in select(page,'//dl//dd'):
   if re.sub(r'\D','',el.text_content())==phone:el.text=formatted
 # Structured data is built safely and never interpolated into executable JS.
 schema={'@context':'https://schema.org','@type':'Person','name':profile['name'],'url':site['site_url'],'jobTitle':profile.get('role'),'image':urljoin(site['site_url'],profile.get('photo','')),'sameAs':[url(profile[k]) for k in ('linkedin','facebook') if url(profile.get(k))],'address':{'@type':'PostalAddress','addressLocality':profile['location'],'addressCountry':'BD'}}
 add(one(h,'//head'),'<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>')
 for page in pages.values():
  for el in select(page,'//section|//article[contains(@class,"gallery-item")]|//div[@class="bio-fabric glass"]'):el.set('data-reveal','')
 return site,ui

def readable_date(raw):
 try:return date.fromisoformat(str(raw)[:10]).strftime('%d %b %Y').lstrip('0')
 except ValueError:return raw
