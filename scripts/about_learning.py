"""Compact, year-grouped learning records; retain CMS detail and shared media viewer."""
import json,re
from lxml import html
from urllib.parse import urlsplit

def refine_learning(page,*,root,esc,url,rich,set_html,story_body):
 settings=json.loads((root/'editor/about-presentation.json').read_text());labels=settings.get('learning_labels',{})
 def label(key,default):return labels.get(key) or default
 symbols={s.get('id'):s for s in page.xpath('//symbol')}
 overrides={x.get('key'):x.get('image') for x in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  source=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',source) and '..' not in source:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(source)+'\')"></span>'
  symbol=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
 payload=page.xpath('//script[@id="credential-data"]')[0];collections=json.loads(payload.text);collections['workshops']=[]
 def year(v):
  match=re.search(r'\b(?:19|20)\d{2}\b',str(v.get('year') or v.get('issue_date') or v.get('date') or ''))
  return match[0] if match else ''
 def records(folder):
  rows=[(p.stem,json.loads(p.read_text())) for p in (root/'editor'/folder).glob('*.json')]
  return sorted([(k,v) for k,v in rows if v.get('published',True)],key=lambda kv:(-int(year(kv[1]) or 0),kv[1].get('order',10),kv[0]))
 def media(folder,key,v):
  collection=collections[folder];first=len(collection);picture=url(v.get('image'));file=url(v.get('file'))
  if not picture and urlsplit(file).path.lower().endswith(('.png','.jpg','.jpeg','.webp','.gif')):picture=file
  photos=[dict(image=picture,caption='')] if picture or file else []
  photos += [p for p in v.get('gallery',[]) if url(p.get('image')) and url(p['image'])!=picture]
  for p in photos:collection.append(dict(id=folder+'-'+key,title=v.get('title') or '',issuer=v.get('institution') or '',year=year(v),semester='',received_date='',image=url(p.get('image')),image_alt=v.get('image_alt') or v.get('title') or '',caption=p.get('caption') or '',file=file,description=rich(v.get('body'))))
  return first if photos else None,picture
 # Rebuild certificate viewer indices in the same order as the compact list.
 collections['certificates']=[]
 def group_markup(folder):
  rows=records(folder);groups={}
  for index,(key,v) in enumerate(rows):
   yr=year(v);groups.setdefault(yr,[]);viewer,picture=media(folder,key,v);title=v.get('title') or '';issuer=v.get('institution') or '';logo=url(v.get('institution_logo'));credential=url(v.get('verification_url') or v.get('credential_url'));website=url(v.get('website'))
   logo_html='<img class="learning-logo" src="'+esc(logo)+'" alt="'+esc(issuer or title)+' logo" width="32" height="32" loading="lazy">' if logo else '<span class="learning-logo learning-monogram" aria-hidden="true">'+esc((issuer or title or 'L')[0])+'</span>'
   summary='<span class="learning-row-year">'+esc(yr or label('undated','Undated'))+'</span><span class="learning-title-block"><h3 class="learning-title">'+esc(title)+'</h3>'+('<span class="learning-issuer">'+esc(issuer)+'</span>' if issuer else '')+'</span>'+logo_html+'<span class="learning-row-end">'+(icon('certificate') if viewer is not None else '')+'<span class="learning-chevron" aria-hidden="true">'+icon('down')+'</span></span>'
   clean=dict(v,file='',gallery=[],skills=[],institution='',date='',duration='',verification_url='');content=story_body(clean,folder)
   if picture and viewer is not None:content='<button type="button" class="learning-thumbnail" data-credential-open="'+folder+'" data-credential-index="'+str(viewer)+'" aria-label="'+esc(label('open_certificate','Open certificate')+' · '+title)+'"><img src="'+esc(picture)+'" alt="'+esc(v.get('image_alt') or title)+'" width="240" height="160" loading="lazy">'+icon('zoom')+'</button>'+content
   elif viewer is not None:content='<button type="button" class="learning-view" data-credential-open="'+folder+'" data-credential-index="'+str(viewer)+'">'+icon('certificate')+esc(label('view_file','View certificate'))+'</button>'+content
   extra_photos=[p for p in v.get('gallery',[]) if url(p.get('image')) and url(p['image'])!=picture]
   for offset,photo in enumerate(extra_photos):
    photo_index=(viewer or 0)+(1 if picture or url(v.get('file')) else 0)+offset
    content+='<figure class="learning-extra-photo"><button type="button" class="learning-thumbnail" data-credential-open="'+folder+'" data-credential-index="'+str(photo_index)+'" aria-label="'+esc(label('open_certificate','Open certificate')+' · '+title)+'"><img src="'+esc(url(photo['image']))+'" alt="'+esc(photo.get('caption') or title)+'" width="240" height="160" loading="lazy"></button>'+('<figcaption>'+esc(photo['caption'])+'</figcaption>' if photo.get('caption') else '')+'</figure>'
   if v.get('badge'):content+='<p>'+esc(v['badge'])+'</p>'
   if v.get('skills'):content+='<ul class="learning-skills">'+''.join('<li>'+esc(s)+'</li>' for s in v['skills'] if str(s).strip())+'</ul>'
   if v.get('duration'):content+='<p class="learning-duration">'+esc(label('duration','Duration'))+': '+esc(v['duration'])+'</p>'
   if credential:content+='<a class="learning-link" href="'+esc(credential)+'" target="_blank" rel="noopener noreferrer">'+esc(label('view_credential','View credential'))+icon('arrow')+'</a>'
   if website:content+='<a class="learning-link" href="'+esc(website)+'" target="_blank" rel="noopener noreferrer">'+esc(issuer or label('issuer_website','Issuer website'))+icon('arrow')+'</a>'
   # No expansion affordance for genuinely empty records.
   inner='<details class="learning-details"><summary>'+summary+'</summary><div class="learning-detail-body">'+content+'</div></details>' if content.strip() else '<div class="learning-static">'+summary+'</div>'
   groups[yr].append('<article class="learning-row" data-entry-id="'+folder+'-'+esc(key)+'"'+(' data-learning-overflow hidden' if index>=5 else '')+'>'+inner+'</article>')
  result=''
  for yr,items in groups.items():result+='<div class="learning-year-group"><h4 class="learning-year-label">'+esc(yr or label('undated','Undated'))+'</h4><div class="learning-year-items">'+''.join(items)+'</div></div>'
  if not rows:result='<p class="learning-empty">'+esc(label('empty','Published learning records will appear here.'))+'</p>'
  result='<div class="learning-list" id="learning-'+folder+'">'+result+'</div>'
  if len(rows)>5:result+='<button type="button" class="learning-show-all" aria-controls="learning-'+folder+'" aria-expanded="false" data-learning-show="'+folder+'" data-show-label="'+esc(label('show_all','Show all'))+' ('+str(len(rows))+')" data-less-label="'+esc(label('show_less','Show fewer'))+'">'+esc(label('show_all','Show all'))+' ('+str(len(rows))+')</button>'
  return result
 section=page.xpath('//*[@id="certificates"]')[0];header=section.find('header');transcript=section.xpath('.//div[contains(@class,"transcript-action")]')
 for old in list(section):
  if old is not header:section.remove(old)
 set_html_container=html.fragment_fromstring('<div class="learning-collections"><h3 class="learning-subheading">'+esc(label('certificates_heading','Certificates & short courses'))+'</h3>'+group_markup('certificates')+'<h3 class="learning-subheading learning-workshops-heading">'+esc(label('workshops_heading','Workshops & seminars'))+'</h3>'+group_markup('workshops')+'</div>');section.append(set_html_container)
 for node in transcript:section.append(node)
 payload.text=json.dumps(collections,ensure_ascii=False).replace('<','\\u003c')
 # Experience keeps its full existing content, with its own quieter editorial shell.
 for card in page.xpath('//*[@id="experience"]//article[@data-entry-id]'):
  card.set('class',card.get('class','')+' exposure-card')
  for node in card.xpath('./span[contains(@class,"care-chip")]'):node.set('class',node.get('class')+' exposure-date')
 page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="about-learning.css">'));page.find('body').append(html.fragment_fromstring('<script src="about-learning.js" defer></script>'))
