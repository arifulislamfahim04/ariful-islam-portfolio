"""Isolated homepage hero; content continues to come from Pages CMS."""
from lxml import html, etree
import json, re

NAV=[('index','Home','home'),('about','About','about'),('projects','Projects','projects'),('gallery','Gallery','gallery'),('blogs','Blogs','blogs'),('contact','Contact','contact')]
def refresh_hero(d, profile, settings, *, esc, url, rich, set_html, navigation=None):
 NAV=globals()['NAV'] if navigation is None else navigation
 body=d.find('body');body.set('data-hero-refresh','true')
 overrides={v.get('key'):v.get('image') for v in settings.get('icon_overrides',[]) if isinstance(v,dict)}
 def icon(key):
  custom=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:
   return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><use href="#i-'+esc(key)+'"></use></svg>'
 def link(dest,text,cls='',glyph='',external=False):
  dest=url(dest)
  if not dest:return ''
  return '<a class="'+cls+'" href="'+esc(dest)+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+text+(icon(glyph) if glyph else '')+'</a>'
 def nav():
  return ''.join('<a href="'+p+'.html" aria-label="'+label+'"'+(' aria-current="page"' if p=='index' else '')+'>'+icon(key)+'<span>'+label+'</span></a>' for p,label,key in NAV)
 # Header utilities share the same container edges as the hero and footer.
 header=d.xpath('//header[contains(@class,"site-header")]')[0]
 set_html(header,'<div class="hero-header-inner shell">'+link('index.html',esc(settings.get('logo_text') or 'ariful')+'<span>.</span>','logo')+'<div class="hero-utilities"><span class="hero-location">'+icon('location')+esc(profile.get('location'))+'</span><time data-dhaka-time aria-label="Current time in Dhaka"></time></div></div>')
 # The original native menu dialog and command palette remain functional.
 rail=html.Element('aside',{'class':'hero-rail','aria-label':'Site controls'})
 set_html(rail,'<button class="hero-menu-button round-control menu-trigger" aria-label="Open menu" aria-haspopup="dialog" aria-controls="site-menu" aria-expanded="false">'+icon('menu')+'</button><nav class="hero-page-nav" aria-label="Main navigation">'+nav()+'</nav><label class="hero-theme-switch"><input type="checkbox" role="switch" data-hero-theme aria-label="Dark mode"><span class="theme-track" aria-hidden="true">'+icon('sun')+icon('moon')+'<span class="theme-thumb"></span></span><span class="rail-tooltip">Dark mode</span></label>')
 body.append(rail)
 rail.append(d.xpath('//*[@id="back-top"]')[0])
 switch=rail.xpath('.//label')[0];rail.remove(switch);header.xpath('.//div[@class="hero-utilities"]')[0].append(switch)
 menu=d.xpath('//*[@id="site-menu"]//nav')[0];set_html(menu,nav())
 hero=d.xpath('//section[contains(@class,"home-hero")]')[0]
 phrases=[str(v).strip() for v in settings.get('typewriter_phrases',[]) if str(v).strip()] or [str(settings.get('headline') or 'Textile engineering, with a practical mind.')]
 reserves=''.join('<span class="hero-role-reserve" aria-hidden="true">'+esc(v)+'</span>' for v in phrases)
 portrait=url(profile.get('photo'));photo='<img src="'+esc(portrait)+'" alt="'+esc(profile.get('photo_alt') or profile.get('name'))+'" width="600" height="600" decoding="async" fetchpriority="high" draggable="false">' if portrait else '<span class="hero-monogram">'+esc(settings.get('preferred_name'))+'</span>'
 socials=[]
 # Optional ordered slots refer to existing profile fields without duplicating their values.
 rows=settings.get('card_socials')
 if rows is None:rows=[{'label':'Email','source':'Email','icon':'contact'},{'label':'LinkedIn','source':'LinkedIn','icon':'linkedin'},{'label':'Facebook','source':'Facebook','icon':'facebook'}]
 for row in rows[:4]:
  source=row.get('source');dest={'Email':('mailto:'+profile.get('email','')) if profile.get('email') else '', 'LinkedIn':profile.get('linkedin'),'Facebook':profile.get('facebook')}.get(source,row.get('url',''))
  dest=url(dest)
  if not dest:continue
  glyph=row.get('icon') or 'globe';label=row.get('label') or source or 'Social profile'
  socials.append('<a class="card-channel" href="'+esc(dest)+'" aria-label="'+esc(label)+'"'+(' target="_blank" rel="noopener noreferrer"' if not dest.startswith('mailto:') else '')+'>'+icon(glyph)+'<span>'+esc(label)+'</span></a>')
 availability=profile.get('availability');status='<div class="hero-availability"><span class="availability-dot" aria-hidden="true"></span><span>'+esc(availability)+'</span></div>' if availability else ''
 card='<div class="hero-card-stage"><svg class="hero-lanyard" aria-hidden="true"><path data-lanyard-shadow></path><path data-lanyard></path></svg><article class="hero-id-card" aria-label="Profile card"><div class="hero-card-grip" role="button" tabindex="0" aria-label="Move profile card. Drag or use arrow keys. Escape resets."><span></span></div><div class="hero-card-content"><div class="hero-card-photo">'+photo+'<span class="photo-sheen" aria-hidden="true"></span></div><p class="hero-card-title">'+esc(settings.get('card_title') or profile.get('role'))+'</p><h2 class="hero-card-name">'+esc(profile.get('name'))+'</h2>'+('<p class="hero-card-tagline">'+esc(settings.get('tagline'))+'</p>' if settings.get('tagline') else '')+status+'<div class="card-channels">'+''.join(socials)+'</div>'+link(settings.get('card_button_link'),esc(settings.get('card_button_text')),'hero-card-connect','arrow')+'<div class="hero-card-foot"><span>'+esc(settings.get('card_serial') or 'ARIFUL / 01')+'</span><span class="hero-barcode" aria-hidden="true"></span></div></div></article></div>'
 stat_icons=['book','award','users','research'];stats=''
 for i,s in enumerate(profile.get('stats',[])[:4]):
  val=str(s.get('value') or '0');dec=max(0,min(3,int(s.get('decimals') or 0)))
  stats+='<div class="hero-stat">'+icon(s.get('icon') or stat_icons[i])+'<div><strong><b data-count="'+esc(val)+'" data-decimals="'+str(dec)+'">'+esc(val)+'</b><small>'+esc(s.get('suffix'))+'</small></strong><span>'+esc(s.get('label'))+'</span></div></div>'
 headline=esc(settings.get('preferred_name') or 'Ariful').upper()
 copy='<div class="hero-copy"><p class="eyebrow">'+esc(settings.get('eyebrow'))+'</p><h1 id="home-title"><span class="hero-greeting">'+esc(settings.get('greeting') or 'I’m')+' </span><span class="hero-name">'+headline+'<span class="name-highlight" aria-hidden="true"><i></i><i></i><i></i></span></span></h1><div class="hero-role" data-hero-phrases="'+esc(json.dumps(phrases))+'" aria-label="'+esc('; '.join(phrases))+'">'+reserves+'<span class="hero-role-live" aria-hidden="true">'+esc(phrases[0])+'</span></div><div class="hero-intro">'+rich(settings.get('description'))+'</div><div class="hero-actions">'+link(profile.get('resume'),esc(settings.get('cv_button_text') or 'Download CV'),'button primary','download')+link(settings.get('secondary_button_link'),esc(settings.get('secondary_button_text')),'hero-about-link','arrow')+'</div><div class="hero-stats" aria-label="Profile statistics">'+stats+'</div></div>'
 set_html(hero,'<div class="hero-pointer-light" aria-hidden="true"></div>'+card+copy)
 hero.set('class','home-hero shell hero-refreshed')
 old=d.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," slim-stats ")]')
 for e in old:e.getparent().remove(e)
 # Override any existing homepage icon from CMS, not just new hero icons.
 for use in d.xpath('//svg[contains(concat(" ",@class," ")," icon ")]/use'):
  key=(use.get('href') or '').removeprefix('#i-')
  if key in overrides:
   replacement=html.fragment_fromstring(icon(key));svg=use.getparent();svg.getparent().replace(svg,replacement)
 # Equal-height summaries keep their action aligned across a grid row.
 for summary in d.xpath('//details[contains(@class,"news-card")]/summary'):
  meta=html.Element('div',{'class':'update-meta'})
  for e in list(summary):
   if e.tag=='time' or e.get('class')=='sample-label':meta.append(e)
  summary.insert(0,meta)
 controls=d.xpath('//div[@class="preview-controls"]')
 if controls:
  set_html(controls[0],'<button type="button" class="gallery-motion-switch" role="switch" aria-checked="true" data-gallery-switch><span>'+esc(settings.get('gallery_motion_label') or 'Gallery motion')+'</span><span class="gallery-switch-track" aria-hidden="true"><span></span></span></button>')
 # Keep the ticker switch outside its hover/focus pause region.
 tickers=d.xpath('//div[@class="news-ticker"]')
 if tickers:
  ticker=tickers[0]
  for b in ticker.xpath('.//button[contains(@class,"ticker-toggle")]'):b.getparent().remove(b)
  control=html.Element('div',{'class':'preview-controls ticker-controls'})
  set_html(control,'<button type="button" class="gallery-motion-switch" role="switch" aria-checked="true" data-ticker-switch><span>'+esc(settings.get('ticker_motion_label') or 'Highlights motion')+'</span><span class="gallery-switch-track" aria-hidden="true"><span></span></span></button>')
  ticker.addnext(control)
 # Consistent up-right arrows, including legacy plain-text links.
 for a in d.xpath('//main//a[contains(@class,"text-link") or contains(@class,"cta-link")]|//span[@class="text-link"]'):
  text=''.join(a.itertext()).replace('→','').strip()
  set_html(a,esc(text)+icon('arrow'))
 for a in d.xpath('//section[contains(@class,"closing-cta")]//a[contains(@class,"button")]'):
  text=''.join(a.itertext()).strip();set_html(a,esc(text)+icon('arrow'));a.set('class',a.get('class')+' upward-action')
 utility=header.xpath('.//div[@class="hero-utilities"]')[0]
 place=html.Element('div',{'class':'hero-place-time'})
 for e in list(utility):
  if e.tag in ('span','time'):place.append(e)
 utility.insert(0,place)
 # Reuse the card's CMS social destinations; empty links remain hidden.
 footer_top=d.xpath('//footer/div[@class="footer-top"]')[0]
 if socials:
  channels=html.Element('div',{'class':'footer-channels','role':'group','aria-label':'Social and contact links'})
  set_html(channels,''.join(socials));footer_top.append(channels)
 # Inline the existing SVG Repo shapes so every icon is self-contained.
 symbols={e.get('id'):e for e in d.xpath('//symbol')}
 for svg in d.xpath('//svg[contains(concat(" ",@class," ")," icon ")]'):
  for use in list(svg):
   if etree.QName(use).localname!='use':continue
   symbol=symbols.get((use.get('href') or '').lstrip('#'))
   if symbol is not None:
    svg.remove(use)
    for shape in symbol:svg.append(etree.fromstring(etree.tostring(shape)))
 # The right-hand rail already provides page navigation.
 for e in d.xpath('//footer//nav|//footer//span[@class="footer-mark"]'):
  e.getparent().remove(e)
 head=d.find('head')
 for e in head.xpath('./link[@rel="preload" and contains(@href,"editorial-fonts")]'):head.remove(e)
 for weight in (400,500,600):head.append(html.fragment_fromstring(f'<link rel="preload" href="assets/hero-fonts/poppins-{weight}.woff" as="font" type="font/woff" crossorigin="anonymous">'))
 head.append(html.fragment_fromstring('<link rel="stylesheet" href="hero-refresh.css">'))
 body.append(html.fragment_fromstring('<script src="hero-refresh.js" defer></script>'))
