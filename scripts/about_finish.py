from lxml import html,etree
from copy import deepcopy
import json

def finish_about(pages,*,root,esc,url,set_html):
 settings=json.loads((root/'editor/about-presentation.json').read_text())
 a=pages['about']
 # Consolidate the personal facts; repeated glance values need no second panel.
 grid=a.xpath('//dl[@class="info-grid"]')[0]
 panel=html.Element('section',{'class':'profile-facts-panel','aria-label':settings.get('facts_heading') or 'Personal facts'})
 set_html(panel,'<span class="section-label">'+esc(settings.get('facts_heading'))+'</span>')
 old=grid.getparent();grid.getparent().remove(grid);panel.append(grid);old.addprevious(panel)
 if not len(old):old.getparent().remove(old)
 aliases={'focus area':'specialization','availability':'current focus'}
 present={aliases.get(e.text_content().strip().lower(),e.text_content().strip().lower()) for e in grid.xpath('.//dt')}
 for glance in a.xpath('//aside[contains(@class,"at-glance")]'):
  for fact in glance.xpath('.//dl/div'):
   label=fact.xpath('string(.//dt)').strip().lower();key=aliases.get(label,label)
   if key and key not in present:
    item=deepcopy(fact);item.set('class','info-card glass');grid.append(item);present.add(key)
  glance.getparent().remove(glance)

 for empty in a.xpath('//div[@class="info-layout" and not(*)]'):empty.getparent().remove(empty)
 for section,folder in [('education','education'),('experience','experience')]:
  records={p.stem:json.loads(p.read_text()) for p in (root/'editor'/folder).glob('*.json')}
  for card in a.xpath('//section[@id="'+section+'"]//article[@data-entry-id]'):
   key=card.get('data-entry-id').removeprefix(folder+'-');v=records.get(key,{})
   title=card.find('h3')
   if title is None:continue
   head=html.Element('div',{'class':'institution-head'});logo=url(v.get('institution_logo'))
   if logo:set_html(head,'<img class="institution-logo" src="'+esc(logo)+'" alt="'+esc(v.get('institution') or v.get('title'))+' logo" width="54" height="54" loading="lazy">')
   else:set_html(head,'<span class="institution-initial" aria-hidden="true">'+esc(str(v.get('institution') or v.get('title') or 'A')[0].upper())+'</span>')
   words=html.Element('div');head.append(words);title.addprevious(head);words.append(title)
   for org in card.xpath('./p[@class="institution"]'):words.append(org)
 for detail in a.xpath('//details[contains(@class,"entry-extra")]'):
  detail.set('data-animated-details','');summary=detail.find('summary')
  if summary is not None:
   plus=html.Element('span',{'class':'detail-plus','aria-hidden':'true'});plus.text='+';summary.append(plus)
 recommendations=[v for v in settings.get('recommendations',[]) if v.get('published',True) and v.get('quote')]
 if recommendations:
  section=a.xpath('//*[@id="recommendations"]')[0]
  for old in section.xpath('./div[contains(@class,"recommendation-empty")]'):old.getparent().remove(old)
  grid=html.Element('div',{'class':'recommendation-grid'})
  for v in recommendations:
   card=html.Element('article',{'class':'recommendation-card'})
   set_html(card,('<span class="sample-label">Sample · not a real endorsement</span>' if v.get('sample') else '')+'<blockquote>'+esc(v['quote'])+'</blockquote><div class="recommendation-person">'+esc(v.get('name'))+'</div><p class="recommendation-role">'+esc(v.get('role'))+'</p>');grid.append(card)
  section.append(grid)
 for name in ('index','about'):
  d=pages[name];body=d.find('body');head=d.find('head')
  if settings.get('intro_animation',True):
   mark=html.Element('div',{'class':'wordmark-intro','hidden':'','aria-hidden':'true'});set_html(mark,'<span>'+esc(settings.get('intro_wordmark') or 'ARIFUL')+'</span>');body.append(mark)
  head.append(html.fragment_fromstring('<link rel="stylesheet" href="shared-motion.css">'))
  body.append(html.fragment_fromstring('<script src="shared-motion.js" defer></script>'))
