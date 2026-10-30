"""One navigation dock and accessible full menu across every route."""
from lxml import html
import json,re
from navigation import read_navigation

def refine_dock(pages,*,root,esc,url,set_html):
 nav=read_navigation(root);profile=json.loads((root/'editor/profile.json').read_text());settings=json.loads((root/'editor/homepage.json').read_text())
 overrides={row.get('key'):row.get('image') for row in settings.get('icon_overrides',[])}
 for name,page in pages.items():
  body=page.find('body');body.set('class',(body.get('class','')+' shared-dock-site').strip())
  current='projects' if name.startswith('projects-') else 'blogs' if name.startswith('posts-') else name
  symbols={s.get('id'):s for s in page.xpath('//symbol')}
  def icon(key):
   custom=str(overrides.get(key) or '')
   if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
   symbol=symbols.get('i-'+key)
   return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
  top=page.xpath('//*[@id="back-top"]')[0];top.getparent().remove(top)
  for old in page.xpath('//aside[contains(@class,"hero-rail") or contains(@class,"dock-rail")]|//nav[@class="header-nav"]|//header[contains(@class,"site-header")]//*[contains(concat(" ",@class," ")," menu-trigger ")]'):
   if old.getparent() is not None:old.getparent().remove(old)
  rail=html.Element('aside',{'id':'site-dock','class':'shared-dock','aria-label':'Site controls'})
  links=''.join('<a href="'+p+'.html" data-dock-page="'+p+'"'+(' data-dock-extra=""' if p not in ('index','about','projects','contact') else '')+' aria-label="'+esc(label)+'"'+(' aria-current="page"' if p==current else '')+'>'+icon(key)+'<span class="dock-tooltip" aria-hidden="true">'+esc(label)+'</span><span class="dock-label" aria-hidden="true">'+esc(label)+'</span></a>' for p,label,key in nav)
  set_html(rail,'<button type="button" class="dock-menu-button" data-dock-menu aria-label="Open menu" aria-haspopup="dialog" aria-controls="site-menu" aria-expanded="false">'+icon('menu')+'<span class="dock-tooltip" aria-hidden="true">Menu</span></button><nav class="dock-nav" aria-label="Main navigation"><span class="dock-indicator" aria-hidden="true"></span>'+links+'</nav>')
  rail.append(top);body.append(rail)
  # Keep the existing single back-to-top control, adding its visible progress track.
  for child in list(top):top.remove(child)
  top.set('class','dock-back-top');set_html(top,'<svg class="dock-progress" viewBox="0 0 48 48" aria-hidden="true"><circle class="dock-progress-track" cx="24" cy="24" r="21"></circle><circle class="dock-progress-value" cx="24" cy="24" r="21" pathLength="100"></circle></svg>'+icon('up'))
  menu=page.xpath('//*[@id="site-menu"]')[0];menu.set('class','shared-menu');menu.set('aria-labelledby','site-menu-title');menu.set('data-shared-menu','')
  brand=str(settings.get('logo_text') or 'ariful').rstrip('.')+'.'
  menu_links=''.join('<a href="'+p+'.html"'+(' aria-current="page"' if p==current else '')+' style="--menu-order:'+str(i)+'"><span>'+esc(label)+'</span>'+icon('arrow')+'</a>' for i,(p,label,key) in enumerate(nav))
  # Reuse the footer's published icon destinations and labels, with no duplicate CMS values.
  footer=page.xpath('//footer')[0];socials=footer.xpath('.//a[contains(concat(" ",@class," ")," footer-social ")]')
  social_markup=''.join('<a class="menu-social" href="'+esc(a.get('href'))+'" aria-label="'+esc(a.get('aria-label'))+'"'+(' target="_blank" rel="noopener noreferrer"' if a.get('target') else '')+'>'+''.join(html.tostring(c,encoding='unicode') for c in a if c.tag in ('svg','span') and 'footer-tooltip' not in c.get('class',''))+'</a>' for a in socials)
  used={a.get('href') for a in socials}
  for row in settings.get('card_socials',[]):
   if not row.get('published',True):continue
   source=row.get('source');dest=url({'Email':('mailto:'+profile['email']) if profile.get('email') else '', 'LinkedIn':profile.get('linkedin'), 'Facebook':profile.get('facebook')}.get(source,row.get('url')))
   if not dest or dest in used or not dest.startswith(('https://','http://','mailto:')):continue
   used.add(dest);social_markup+='<a class="menu-social" href="'+esc(dest)+'" aria-label="'+esc(row.get('label') or source or 'Profile')+'"'+(' target="_blank" rel="noopener noreferrer"' if dest.startswith(('https://','http://')) else '')+'>'+icon(row.get('icon') or 'globe')+'</a>'
  status='<span class="menu-status"><i aria-hidden="true"></i>'+esc(profile['availability'])+'</span>' if profile.get('availability') else ''
  contact='<a class="menu-email" href="mailto:'+esc(profile['email'])+'">'+icon('contact')+esc(profile['email'])+'</a>' if profile.get('email') else ''
  set_html(menu,'<div class="shared-menu-top"><a class="menu-wordmark" href="index.html">'+esc(brand)+'</a><button type="button" class="dock-menu-close" data-dock-close aria-label="Close menu">'+icon('close')+'</button></div><h2 id="site-menu-title">Find your next thread.</h2><nav class="menu-links" aria-label="Full site navigation">'+menu_links+'</nav><div class="shared-menu-end">'+status+contact+'<div class="menu-utilities"><div class="menu-socials" aria-label="Social profiles">'+social_markup+'</div><div class="menu-theme"><span>Appearance</span><button type="button" class="theme-toggle" aria-label="Switch theme"></button></div></div></div>')
  page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="shared-dock.css">'));body.append(html.fragment_fromstring('<script src="shared-dock.js" defer></script>'))
