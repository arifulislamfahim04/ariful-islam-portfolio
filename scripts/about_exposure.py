"""CMS-backed professional/leadership roles and industry exposure, without timelines."""
import json,re
from datetime import date
from calendar import month_abbr
from urllib.parse import urlsplit
from lxml import html

def refine_exposure(page,*,root,esc,url,rich,set_html,story_body):
 settings=json.loads((root/'editor/about-presentation.json').read_text());labels=settings.get('exposure_labels',{})
 def label(k,d):return labels.get(k) or d
 symbols={s.get('id'):s for s in page.xpath('//symbol')};overrides={x.get('key'):x.get('image') for x in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  custom=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
  s=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(x,encoding='unicode') for x in s) if s is not None else '')+'</svg>'
 def format_date(raw):
  raw=str(raw or '')
  if re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',raw):
   y,m=map(int,raw.split('-')[:2])
   if 1<=m<=12:return month_abbr[m]+' '+str(y)
  return raw
 def period(v):
  start,end=v.get('start_date') or '',v.get('end_date') or '';ongoing=v.get('currently_working',False)
  if ongoing and start:return label('since','Since')+' '+format_date(start)
  if start and end:return format_date(start)+' – '+format_date(end)
  if start:return label('since','Since')+' '+format_date(start) if ongoing else label('started','Started')+' '+format_date(start)
  return str(v.get('date') or '')
 def duration(v):
  if v.get('duration_label'):return v['duration_label']
  a,b=str(v.get('start_date') or ''),str(v.get('end_date') or '')
  if not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',a):return ''
  if v.get('currently_working'):b=date.today().strftime('%Y-%m')
  if not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',b):return ''
  sy,sm=map(int,a.split('-')[:2]);ey,em=map(int,b.split('-')[:2])
  if not (1<=sm<=12 and 1<=em<=12):return ''
  months=(ey-sy)*12+em-sm
  if months<=0:return ''
  years,months=divmod(months,12)
  return ' '.join(x for x in [str(years)+' '+label('year','yr') if years==1 else str(years)+' '+label('years','yrs') if years else '',str(months)+' '+label('month','mo') if months==1 else str(months)+' '+label('months','mos') if months else ''] if x)
 payload=page.xpath('//script[@id="credential-data"]')[0];collections=json.loads(payload.text);collections['leadership']=[]
 def media(key,v):
  picture=url(v.get('image'));file=url(v.get('file'))
  if not picture and urlsplit(file).path.lower().endswith(('.jpg','.jpeg','.png','.webp','.gif')):picture=file
  photos=[dict(image=picture,caption='')] if picture or file else []
  photos += [p for p in v.get('gallery',[]) if url(p.get('image')) and url(p['image'])!=picture]
  markup=''
  for i,p in enumerate(photos):
   index=len(collections['leadership']);image=url(p.get('image'));caption=p.get('caption') or '';title=v.get('title') or ''
   collections['leadership'].append(dict(id='experience-'+key,title=title,issuer=v.get('institution') or '',year=period(v),semester='',received_date='',image=image,image_alt=v.get('image_alt') or caption or title,caption=caption,file=file,description=rich(v.get('body'))+rich(v.get('responsibilities'))))
   if image:markup+='<figure class="exposure-photo"><button type="button" data-credential-open="leadership" data-credential-index="'+str(index)+'" aria-label="'+esc(label('view_photos','View photos')+' · '+title)+'"><img src="'+esc(image)+'" alt="'+esc(v.get('image_alt') or caption or title)+'" width="640" height="360" loading="lazy">'+icon('zoom')+'</button>'+('<figcaption>'+esc(caption)+'</figcaption>' if caption else '')+'</figure>'
   elif i==0:markup+='<button type="button" class="exposure-file" data-credential-open="leadership" data-credential-index="'+str(index)+'">'+icon('certificate')+esc(label('view_document','View supporting document'))+'</button>'
  return '<div class="exposure-photos">'+markup+'</div>' if markup else ''
 def logo(v):
  source=url(v.get('institution_logo'));org=v.get('institution') or v.get('title') or 'A'
  if source:return '<img class="exposure-logo" src="'+esc(source)+'" alt="'+esc(org)+' logo" width="48" height="48" loading="lazy">'
  return '<span class="exposure-logo exposure-initial" aria-hidden="true">'+esc(str(org)[0].upper())+'</span>'
 def organization(v):
  name=v.get('institution') or '';dest=url(v.get('website') or v.get('organization_url'))
  if not name:return ''
  return '<p class="exposure-organization">'+('<a href="'+esc(dest)+'" target="_blank" rel="noopener noreferrer">'+esc(name)+icon('arrow')+'</a>' if dest else esc(name))+'</p>'
 roles=[];events=[]
 records=sorted([(p.stem,json.loads(p.read_text())) for p in (root/'editor/experience').glob('*.json')],key=lambda kv:(kv[1].get('order',10),kv[0]))
 for key,v in records:
  if not v.get('published',True):continue
  kind=v.get('record_type') or 'role';ongoing=bool(v.get('currently_working'));title=v.get('title') or '';dates=period(v);length=duration(v)
  clean=dict(v,body='',responsibilities='',institution='',date='',start_date='',end_date='',employment_type='',location='',gallery=[],file='',skills=[])
  extra=story_body(clean,'experience')
  if v.get('skills'):extra+='<ul class="exposure-skill-chips">'+''.join('<li>'+esc(x)+'</li>' for x in v['skills'] if str(x).strip())+'</ul>'
  detail='<details class="entry-extra exposure-extra" data-animated-details><summary>'+esc(label('more_details','More details'))+'<span class="detail-plus" aria-hidden="true">+</span></summary><div class="entry-extra-body">'+extra+'</div></details>' if extra.strip() else ''
  body=rich(v.get('body'));responsibilities=rich(v.get('responsibilities'));photos=media(key,v)
  if kind=='event':
   event_type=v.get('event_type') or '';years=[str(x).strip() for x in v.get('years',[]) if str(x).strip()];venue=v.get('venue') or '';city=v.get('city') or v.get('location') or ''
   markup='<div class="exposure-event-head">'+logo(v)+('<span class="exposure-type">'+esc(event_type)+'</span>' if event_type else '')+'</div><h3>'+('<a class="exposure-event-title-link" href="'+esc(url(v.get('website') or v.get('organization_url')))+'" target="_blank" rel="noopener noreferrer">'+esc(title)+icon('arrow')+'</a>' if (v.get('institution') or '')==title and url(v.get('website') or v.get('organization_url')) else esc(title))+'</h3>'+('' if (v.get('institution') or '')==title else organization(v))
   place=' · '.join(x for x in [venue,city] if x)
   if place:markup+='<p class="exposure-place">'+icon('location')+esc(place)+'</p>'
   if years:markup+='<ul class="exposure-years" aria-label="'+esc(label('visit_years','Attendance years'))+'">'+''.join('<li tabindex="0">'+esc(y)+'</li>' for y in years)+'</ul>'
   elif dates:markup+='<p class="exposure-period event-period">'+esc(dates)+'</p>'
   markup+=body+responsibilities+detail+photos
   events.append('<article class="exposure-event exposure-v2" data-entry-id="experience-'+esc(key)+'">'+markup+'</article>')
  else:
   status=label('ongoing','Ongoing') if ongoing else label('completed','Completed')
   markup='<div class="exposure-role-top"><div class="exposure-role-brand">'+logo(v)+('<span class="exposure-role-kind">'+esc(v['employment_type'])+'</span>' if v.get('employment_type') else '')+'</div><span class="exposure-status'+(' ongoing' if ongoing else '')+'"><i aria-hidden="true"></i>'+esc(status)+'</span></div><h3>'+esc(title)+'</h3>'+organization(v)
   if dates:markup+='<p class="exposure-period">'+esc(dates)+('<span> · '+esc(length)+'</span>' if length else '')+'</p>'
   if v.get('location'):markup+='<p class="exposure-place">'+icon('location')+esc(v['location'])+'</p>'
   markup+='<div class="exposure-proof">'+body+responsibilities+'</div>' if body or responsibilities else ''
   impacts=[x for x in v.get('impact',[]) if str(x.get('value') or '').strip()]
   if impacts:markup+='<dl class="exposure-impact">'+''.join('<div><dt>'+esc(x.get('label') or '')+'</dt><dd>'+esc(x['value'])+'</dd></div>' for x in impacts)+'</dl>'
   markup+=detail+photos;roles.append('<article class="exposure-role exposure-v2" data-entry-id="experience-'+esc(key)+'">'+markup+'</article>')
 section=page.xpath('//*[@id="experience"]')[0];header=section.find('header')
 for old in list(section):
  if old is not header:section.remove(old)
 markup=''
 if roles:markup+='<div class="exposure-role-list">'+''.join(roles)+'</div>'
 if events:markup+='<h3 class="exposure-events-heading">'+esc(label('events_heading','Industry visits & exhibitions'))+'</h3><div class="exposure-event-grid">'+''.join(events)+'</div>'
 if not markup:markup='<p>'+esc(label('empty','Published roles and visits will appear here.'))+'</p>'
 section.append(html.fragment_fromstring('<div class="exposure-layout">'+markup+'</div>'))
 payload.text=json.dumps(collections,ensure_ascii=False).replace('<','\\u003c')
 page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="about-exposure.css">'));page.find('body').append(html.fragment_fromstring('<script src="about-exposure.js" defer></script>'))
