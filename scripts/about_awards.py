"""Individual award cards and one reusable credential/photo viewer."""
import json,re
from lxml import html
from urllib.parse import urlsplit

def refine_awards(page,*,root,esc,url,rich,set_html,story_body):
 settings=json.loads((root/'editor/about-presentation.json').read_text());labels=settings.get('award_labels',{})
 def text(key,default):return labels.get(key,default)
 symbols={s.get('id'):s for s in page.xpath('//symbol')};overrides={x.get('key'):x.get('image') for x in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  source=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',source) and '..' not in source:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(source)+'\')"></span>'
  symbol=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
 def records(folder):return sorted([(p.stem,json.loads(p.read_text())) for p in (root/'editor'/folder).glob('*.json') if json.loads(p.read_text()).get('published',True)],key=lambda x:(x[1].get('order',10),x[0]))
 def item(key,v,picture='',caption=''):
  file=url(v.get('file'));image=url(picture or v.get('image'))
  if not image and file and urlsplit(file).path.lower().endswith(('.png','.jpg','.jpeg','.webp','.gif')):image=file
  return dict(id=key,title=v.get('title') or '',issuer=v.get('institution') or '',year=v.get('year') or v.get('date') or '',semester=v.get('semester') or '',received_date=v.get('received_date') or '',image=image,image_alt=v.get('image_alt') or v.get('title') or '',caption=caption,file=file,description=story_body(dict(v,file='',gallery=[],institution='',date='',start_date='',end_date='',issue_date=''),key.partition('-')[0]))
 collections={'awards':[],'certificates':[],'leadership':[]};award_cards=''
 for key,v in records('achievements'):
  record=item('achievements-'+key,v);index=len(collections['awards']);collections['awards'].append(record)
  for photo in v.get('gallery',[]):
   if url(photo.get('image')) and url(photo['image'])!=record['image']:collections['awards'].append(item('achievements-'+key,v,photo['image'],photo.get('caption') or ''))
  thumbnail=('<img src="'+esc(record['image'])+'" alt="'+esc(record['image_alt'])+'" width="560" height="320" loading="lazy">') if record['image'] else '<span class="award-placeholder" aria-hidden="true">'+icon('award')+'</span>'
  content='<span class="award-thumbnail">'+thumbnail+'<span class="award-view-hint">'+icon('zoom')+esc(text('view','View'))+'</span></span><span class="award-card-content">'
  if record['year']:content+='<span class="award-year">'+esc(record['year'])+'</span>'
  if record['semester']:content+='<span class="award-semester">'+esc(record['semester'])+'</span>'
  content+='<h3>'+esc(record['title'])+'</h3>'+('<span class="award-issuer">'+esc(record['issuer'])+'</span>' if record['issuer'] else '')+'</span>'
  award_cards+='<article class="award-card'+(' featured' if v.get('featured') else '')+'" data-entry-id="achievements-'+esc(key)+'"><button type="button" class="award-open" data-credential-open="awards" data-credential-index="'+str(index)+'" aria-label="'+esc(text('open','Open')+' '+record['title']+(' · '+record['semester'] if record['semester'] else '')+' · '+record['year'])+'">'+content+'</button></article>'
 section=page.xpath('//*[@id="recognition"]')[0];section.attrib.pop('data-reveal',None);header=section.find('header')
 for old in list(section):
  if old is not header:section.remove(old)
 if award_cards:
  controls=html.fragment_fromstring('<div class="awards-controls"><button type="button" class="round-control" data-awards-prev aria-label="'+esc(text('previous_awards','Previous awards'))+'">'+icon('left')+'</button><button type="button" class="round-control" data-awards-next aria-label="'+esc(text('next_awards','Next awards'))+'">'+icon('right')+'</button></div>');header.append(controls)
  section.append(html.fragment_fromstring('<div class="awards-block"><p class="awards-instruction" id="awards-instruction">'+esc(text('instruction','Each card is a separate award. Swipe, drag or use the arrow buttons to explore.'))+'</p><div class="awards-window"><div class="awards-carousel" tabindex="0" role="region" aria-label="'+esc(text('carousel_label','Individual academic awards'))+'" aria-describedby="awards-instruction">'+award_cards+'</div></div><div class="awards-progress" aria-hidden="true"><span></span></div></div>'))
 else:section.append(html.fragment_fromstring('<p>'+esc(text('empty','Awards will appear here when published.'))+'</p>'))
 for folder,collection in [('certificates','certificates'),('experience','leadership')]:
  for key,v in records(folder):
   photos=[p for p in v.get('gallery',[]) if url(p.get('image'))]
   record=item(folder+'-'+key,v)
   if record['image']:photos.insert(0,dict(image=record['image'],caption=''))
   elif collection=='certificates' and record['file']:photos.insert(0,dict(image='',caption=''))
   if not photos:continue
   first=len(collections[collection])
   for photo in photos:collections[collection].append(item(folder+'-'+key,v,photo.get('image') or '',photo.get('caption') or ''))
   cards=page.xpath('//article[@data-entry-id="'+folder+'-'+key+'"]')
   if cards:
    button=html.fragment_fromstring('<button type="button" class="credential-photo-trigger" data-credential-open="'+collection+'" data-credential-index="'+str(first)+'">'+icon('gallery')+esc(text('view_certificate','View certificate') if collection=='certificates' else text('view_photos','View photos'))+'</button>');cards[0].append(button)
 dialog=html.fragment_fromstring('<dialog id="credential-viewer" class="credential-dialog" aria-labelledby="credential-title"><div class="credential-toolbar"><span id="credential-counter" aria-live="polite"></span><div class="credential-zoom-controls"><button type="button" data-credential-zoom="out" aria-label="'+esc(text('zoom_out','Zoom out'))+'">−</button><button type="button" data-credential-zoom="reset">'+esc(text('reset','Reset'))+'</button><button type="button" data-credential-zoom="in" aria-label="'+esc(text('zoom_in','Zoom in'))+'">+</button></div><button type="button" class="round-control" data-credential-close aria-label="'+esc(text('close','Close viewer'))+'">'+icon('close')+'</button></div><div class="credential-stage" tabindex="0" aria-label="'+esc(text('image_controls','Certificate image. Use the zoom buttons, pinch to zoom or drag to pan.'))+'"><div class="credential-image-canvas"><img alt="" draggable="false"></div><div class="credential-missing">'+icon('award')+'<p>'+esc(text('missing','Certificate image not uploaded yet.'))+'</p></div><iframe class="credential-pdf" title="'+esc(text('pdf_title','Certificate PDF'))+'" hidden></iframe></div><div class="credential-caption"><h2 id="credential-title"></h2><p class="credential-meta"></p><p class="credential-photo-caption"></p><div class="credential-description"></div><a class="credential-file-link" target="_blank" rel="noopener noreferrer">'+esc(text('open_file','Open or download certificate'))+'</a></div><div class="credential-navigation"><button type="button" class="round-control" data-credential-prev aria-label="'+esc(text('previous_item','Previous item'))+'">'+icon('left')+'</button><span>'+esc(text('swipe_hint','Swipe or use the arrow keys'))+'</span><button type="button" class="round-control" data-credential-next aria-label="'+esc(text('next_item','Next item'))+'">'+icon('right')+'</button></div></dialog>')
 page.find('body').append(dialog)
 payload=html.Element('script',{'id':'credential-data','type':'application/json'});payload.text=json.dumps(collections,ensure_ascii=False).replace('<','\\u003c');page.find('body').append(payload)
 page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="about-awards.css">'));page.find('body').append(html.fragment_fromstring('<script src="about-awards.js" defer></script>'))
