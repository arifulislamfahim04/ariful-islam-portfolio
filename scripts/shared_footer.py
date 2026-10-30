"""One footer generator for all static routes; no duplicated CMS contact values."""
import json,re
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit
from lxml import html
from navigation import read_navigation

def refine_footer(pages,*,root,esc,url,set_html):
 config=json.loads((root/'editor/footer.json').read_text());profile=json.loads((root/'editor/profile.json').read_text());home=json.loads((root/'editor/homepage.json').read_text());site=json.loads((root/'editor/site.json').read_text());about=json.loads((root/'editor/about-presentation.json').read_text());nav=read_navigation(root);overrides={x.get('key'):x.get('image') for x in home.get('icon_overrides',[])}
 def text(key,default):return str(config.get(key,default) or '')
 whatsapp=url(about.get('whatsapp_url'));parsed=urlsplit(whatsapp)
 if parsed.scheme!='https' or parsed.hostname not in ('wa.me','api.whatsapp.com','www.whatsapp.com','whatsapp.com'):whatsapp=''
 email=str(profile.get('email') or '').strip();phone=str(profile.get('phone') or '').strip();sources={'Email':('mailto:'+email if email else ''),'LinkedIn':url(profile.get('linkedin')),'Facebook':url(profile.get('facebook')),'WhatsApp':whatsapp}
 for name,page in pages.items():
  symbols={s.get('id'):s for s in page.xpath('//symbol')}
  def icon(key):
   custom=str(overrides.get(key) or '')
   if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
   symbol=symbols.get('i-'+key)
   if symbol is None:symbol=symbols.get('i-globe')
   return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
  def icon_link(label,dest,key):
   if not dest:return ''
   external=urlsplit(dest).scheme in ('https','http')
   return '<a class="footer-social" href="'+esc(dest)+'" aria-label="'+esc(label)+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+icon(key)+'<span class="footer-tooltip" role="tooltip">'+esc(label)+'</span></a>'
  def copy(value,label):return '<button type="button" class="footer-copy" data-footer-copy="'+esc(value)+'" aria-label="'+esc(text('copy_prefix','Copy')+' '+label)+'"><span data-copy-original>'+icon('copy')+'</span><span data-copy-done hidden>'+icon('check')+'</span></button>'
  socials=[]
  for row in config.get('socials',[]):
   if not row.get('published',True):continue
   source=row.get('source');dest=url(sources.get(source) if source in sources else row.get('url'));label=str(row.get('label') or source or 'Profile');key=str(row.get('icon') or 'globe')
   if not dest:continue
   if source not in ('Email','WhatsApp') and urlsplit(dest).scheme not in ('http','https'):continue
   socials.append((label,dest,key,source))
  external=[r for r in socials if r[3] not in ('Email','WhatsApp')];elsewhere=len(external)>1
  brand=str(home.get('logo_text') or 'ariful');brand=brand if brand.endswith('.') else brand+'.'
  headline=text('heading','Let’s build something');accent=text('heading_accent','together.');status=str(profile.get('availability') or '')
  top='<div class="footer-invitation" data-footer-reveal><div><h2>'+esc(headline)+(' <em>'+esc(accent)+'</em>' if accent else '')+'</h2>'+('<span class="footer-status"><i aria-hidden="true"></i>'+esc(status)+'</span>' if status else '')+'</div>'
  if email:top+='<div class="footer-invitation-actions"><a class="footer-email" href="mailto:'+esc(email)+'">'+icon('contact')+esc(text('email_button','Email me'))+'</a>'+copy(email,text('email_label','email'))+'</div>'
  top+='</div>'
  brand_column='<div class="footer-brand" data-footer-reveal><a class="footer-wordmark" href="index.html" aria-label="'+esc(profile.get('name') or brand)+'">'+esc(brand)+'</a>'+('<p>'+esc(text('tagline','Curiosity, woven into practice.'))+'</p>' if text('tagline','') else '')+('<p class="footer-location">'+icon('location')+esc(profile['location'])+'</p>' if profile.get('location') else '')+'</div>'
  navigation='<div class="footer-navigation" data-footer-reveal><h3>'+esc(text('navigate_label','Navigate'))+'</h3><nav aria-label="Footer navigation">'+''.join('<a href="'+p+'.html"'+(' aria-current="page"' if page.find('body').get('data-page')==p else '')+'>'+icon(key)+'<span>'+esc(label)+'</span>'+icon('arrow')+'</a>' for p,label,key in nav)+'</nav></div>' if nav else ''
  contacts=''
  if email:contacts+='<div class="footer-contact-row"><a href="mailto:'+esc(email)+'">'+icon('contact')+'<span>'+esc(email)+'</span></a>'+copy(email,text('email_label','email'))+'</div>'
  if phone:contacts+='<div class="footer-contact-row"><a href="tel:'+esc(re.sub(r'[^+0-9]','',phone))+'">'+icon('phone')+'<span>'+esc(phone)+'</span></a>'+copy(phone,text('phone_label','phone number'))+'</div>'
  if whatsapp:contacts+='<div class="footer-contact-row"><a href="'+esc(whatsapp)+'" target="_blank" rel="noopener noreferrer">'+icon('whatsapp')+'<span>'+esc(text('whatsapp_label','Message on WhatsApp'))+'</span></a>'+copy(whatsapp,text('whatsapp_copy_label','WhatsApp link'))+'</div>'
  contact_socials=[row for row in socials if not elsewhere or row[3] in ('Email','WhatsApp')]
  if contact_socials:contacts+='<div class="footer-socials" role="group" aria-label="'+esc(text('socials_label','Social profiles'))+'">'+''.join(icon_link(label,dest,key) for label,dest,key,source in contact_socials)+'</div>'
  contact_column='<div class="footer-contacts" data-footer-reveal><h3>'+esc(text('contact_label','Contact'))+'</h3>'+contacts+'</div>' if contacts else ''
  social_column='<div class="footer-elsewhere" data-footer-reveal><h3>'+esc(text('elsewhere_label','Elsewhere'))+'</h3><div class="footer-socials" role="group" aria-label="'+esc(text('socials_label','Social profiles'))+'">'+''.join(icon_link(label,dest,key) for label,dest,key,source in external)+'</div></div>' if elsewhere else ''
  columns='<div class="footer-columns'+(' has-elsewhere' if elsewhere else '')+'">'+brand_column+navigation+contact_column+social_column+'</div>'
  year=datetime.now(ZoneInfo('Asia/Dhaka')).year
  bottom='<div class="footer-end" data-footer-reveal><span>© <span data-footer-year>'+str(year)+'</span> '+esc(profile.get('name'))+'.</span>'+('<span>'+esc(site.get('footer_text'))+'</span>' if site.get('footer_text') else '')+'</div>'
  signature='<div class="footer-signature" aria-hidden="true"><span>'+esc(brand)+'</span><span>'+esc(brand)+'</span></div>' if config.get('show_wordmark',False) else ''
  footer=page.xpath('//footer')[0];footer.set('class','shared-footer shell');footer.set('id','site-footer');set_html(footer,'<div class="footer-panel">'+top+columns+bottom+signature+'</div><div class="footer-copy-status" id="footer-copy-status" role="status" aria-live="polite" data-copied-message="'+esc(text('copied','Copied'))+'" data-failed-message="'+esc(text('copy_failed','Could not copy. Please select and copy the contact text.'))+'"></div>')
  if name=='index':
   for old in page.xpath('//section[contains(concat(" ",@class," ")," closing-cta ")]'):old.getparent().remove(old)
  page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="shared-footer.css">'));page.find('body').append(html.fragment_fromstring('<script src="shared-footer.js" defer></script>'))
