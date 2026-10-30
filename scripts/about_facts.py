"""Two-zone About facts panel; source data stays in Pages CMS."""
from lxml import html
from datetime import datetime
import json,re
from urllib.parse import urlsplit

def refine_facts(page,*,root,esc,url,set_html):
 panel=page.xpath('//section[@class="profile-facts-panel"]')[0];panel.set('id','about-facts')
 settings=json.loads((root/'editor/about-presentation.json').read_text());profile=json.loads((root/'editor/profile.json').read_text());about=json.loads((root/'editor/about.json').read_text())
 existing=[]
 for item in panel.xpath('.//dl/div'):
  label=item.xpath('string(.//dt)').strip();value=item.xpath('string(.//dd)').strip()
  if label and value:existing.append((label,value))
 values={k.lower():v for k,v in existing}
 records=[json.loads(p.read_text()) for p in (root/'editor/education').glob('*.json')]
 records=sorted([v for v in records if v.get('published',True) and v.get('use_for_now_panel')],key=lambda v:v.get('order',10))
 degree=records[0] if records else {}
 def label(key,default):return esc(settings.get(key,default))
 symbols={e.get('id'):e for e in page.xpath('//symbol')};overrides={v.get('key'):v.get('image') for v in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  source=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',source) and '..' not in source:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(source)+'\')"></span>'
  symbol=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(v,encoding='unicode') for v in symbol) if symbol is not None else '')+'</svg>'
 def fact(title,value,glyph=''):
  return '<div class="facts-pair"><dt>'+ (icon(glyph) if glyph else '')+esc(title)+'</dt><dd>'+esc(value)+'</dd></div>' if str(value or '').strip() else ''
 availability=profile.get('availability') or '';specialization=degree.get('specialization',values.get('specialization',''))
 now='<span class="section-label">'+label('now_label','Now')+'</span>'
 if availability:now+='<div class="facts-availability"><span aria-hidden="true"></span>'+esc(availability)+'</div>'
 if specialization:now+='<dl class="facts-specialization">'+fact(settings.get('specialization_label','Specialization'),specialization)+'</dl>'
 stage=degree.get('status') or ''
 try:years=max(0,min(12,int(degree.get('programme_years') or 0)));year=max(0,min(years,int(degree.get('programme_year') or 0)))
 except (TypeError,ValueError):years=year=0
 if stage or years:
  now+='<dl class="facts-study"><div><dt>'+label('study_label','Study stage')+'</dt><dd>'
  if years:
   now+='<div class="study-segments" aria-label="'+esc(str(year)+' of '+str(years)+' programme years reached; qualification status: '+stage)+'">'+''.join('<span'+(' class="reached"' if i<=year else '')+'><i aria-hidden="true"></i><small>'+label('year_label','Year')+' '+str(i)+'</small></span>' for i in range(1,years+1))+'</div>'
  if stage:now+='<p class="facts-stage-status">'+esc(stage)+(' · '+label('study_level','undergraduate') if settings.get('study_level','undergraduate') else '')+'</p>'
  now+='</dd></div></dl>'
 identity='<dl class="facts-identity">'+fact('Full name',profile.get('name'))+fact('Nationality',values.get('nationality'))+fact('Based in',profile.get('location'),'location')
 language_source=json.loads((root/'editor/skills.json').read_text()).get('languages',[])
 languages=[str(v.get('name') or '').strip() for v in language_source if v.get('published',True) and str(v.get('name') or '').strip()]
 if languages:identity+='<div class="facts-pair"><dt>Languages</dt><dd class="facts-languages">'+''.join('<span>'+esc(v)+'</span>' for v in languages)+'</dd></div>'
 handled={'full name','nationality','based in','languages','email','phone','study stage','specialization','focus area','current focus','availability'}
 for title,value in existing:
  if title.lower() not in handled:identity+=fact(title,value)
 for item in settings.get('recruiter_details',[]):
  identity+=fact(item.get('label') or '',item.get('value'))
 identity+='</dl>'
 contacts=''
 for key,title,glyph,scheme in [('email','Email','contact','mailto:'),('phone','Phone','phone','tel:')]:
  value=str(profile.get(key) or '').strip()
  if not value:continue
  dest=scheme+(re.sub(r'[^+0-9]','',value) if key=='phone' else value)
  copy_label=settings.get('copy_'+key+'_label','Copy '+title.lower())
  success=settings.get(key+'_copied_text',title+' copied')
  display=esc(value).replace('@','@<wbr>',1) if key=='email' else esc(value)
  contacts+='<div class="facts-contact-row">'+icon(glyph)+'<div><span class="facts-contact-label">'+esc(title)+'</span><a href="'+esc(url(dest))+'">'+display+'</a></div><button type="button" class="facts-copy" data-facts-copy="'+esc(value)+'" data-copy-success="'+esc(success)+'" aria-label="'+esc(copy_label)+'"><span class="copy-glyph">'+icon('copy')+'</span><span class="copied-glyph">'+icon('check')+'</span></button></div>'
 whatsapp=url(settings.get('whatsapp_url'));parsed=urlsplit(whatsapp)
 if whatsapp and parsed.scheme=='https' and parsed.hostname in ('wa.me','api.whatsapp.com','www.whatsapp.com','whatsapp.com'):
  contacts+='<a class="facts-whatsapp" href="'+esc(whatsapp)+'" target="_blank" rel="noopener noreferrer">'+icon('whatsapp')+label('whatsapp_text','Message on WhatsApp')+'</a>'
 right=identity+('<div class="facts-contacts" aria-label="'+label('contact_heading','Contact')+'">'+contacts+'</div>' if contacts else '')
 reviewed=''
 if settings.get('reviewed_on'):
  try:
   date=datetime.strptime(settings['reviewed_on'],'%Y-%m-%d');reviewed='<time datetime="'+date.strftime('%Y-%m-%d')+'">'+label('updated_label','Updated')+' '+date.strftime('%b %Y')+'</time>'
  except ValueError:pass
 if not (availability or specialization or stage or years):now=''
 now_zone='<div class="facts-now" data-facts-reveal="0">'+now+'</div>' if now else ''
 set_html(panel,'<div class="facts-panel-heading"><span class="section-label">'+esc(settings.get('facts_heading') or 'A little more about me')+'</span>'+reviewed+'</div><div class="facts-zones">'+now_zone+'<div class="facts-right" data-facts-reveal="1">'+right+'</div></div><span class="facts-copy-status" role="status" aria-live="polite" data-copy-failure="'+label('copy_failed_text','Copy failed. Please select and copy the text.')+'"></span>')
