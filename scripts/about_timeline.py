"""About-only navigation and explicit CMS timeline states."""
import json
from lxml import html

def refine_timeline(page,*,root,esc):
 nav=page.xpath('//nav[@class="section-index"]')[0]
 for index,link in enumerate(nav.xpath('./a'),1):
  label=link.text or '';link.text=None
  number=html.Element('span',{'class':'section-number','aria-hidden':'true'});number.text=f'{index:02d}';number.tail=label;link.insert(0,number)
 track=html.fragment_fromstring('<span class="section-scroll-track" aria-hidden="true"><span></span></span>');nav.insert(0,track)
 states={'completed':'Completed','in-progress':'In progress','results-pending':'Results pending','upcoming':'Upcoming'}
 for section_id in ('education','experience','certificates'):
  section=page.xpath('//*[@id="'+section_id+'"]')[0];section.attrib.pop('data-reveal',None);section.set('tabindex','-1')
  groups=section.xpath('./div[contains(@class,"stitched-timeline") or contains(@class,"certificate-grid")]')
  for group in groups:
   cards=group.xpath('./article[@data-entry-id]')
   if not cards:continue
   group.set('class',group.get('class','')+' about-timeline')
   group.insert(0,html.fragment_fromstring('<span class="about-timeline-track" aria-hidden="true"><span></span></span>'))
   for index,card in enumerate(cards):
    key=card.get('data-entry-id');folder,_,record=key.partition('-');path=root/'editor'/folder/(record+'.json')
    value=json.loads(path.read_text()) if path.exists() else {};state=value.get('timeline_state','completed')
    if state not in states:state='completed'
    card.set('data-timeline-state',state);card.set('data-timeline-reveal',str(index));card.set('class',card.get('class','')+' timeline-entry');card.attrib.pop('data-reveal',None)
    for old in card.xpath('./span[@class="timeline-node"]'):card.remove(old)
    node=html.Element('span',{'class':'about-timeline-dot','role':'img','aria-label':states[state]});card.insert(0,node)
