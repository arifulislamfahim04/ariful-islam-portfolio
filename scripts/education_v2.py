"""CMS-driven education cards, layered after the existing content renderer."""
from lxml import html
import json, re
from datetime import datetime

def month(value):
 value=str(value or '').strip()
 if re.fullmatch(r'\d{4}',value):return value
 for fmt in ('%Y-%m-%d','%Y-%m','%b %Y','%B %Y','%Y'):
  try:return datetime.strptime(value,fmt).strftime('%b %Y')
  except ValueError:pass
 return value

def education_v2(page,*,root,esc,url,set_html,rich):
 records={p.stem:json.loads(p.read_text()) for p in (root/'editor/education').glob('*.json')}
 symbol=page.xpath('//symbol[@id="i-arrow"]')[0]
 arrow='<span class="edu-arrow" aria-hidden="true"><svg viewBox="0 0 256 256" fill="currentColor" style="transform:rotate(-45deg)">'+''.join(html.tostring(child,encoding='unicode') for child in symbol)+'</svg></span>'
 overrides=json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])
 for item in overrides:
  image=str(item.get('image') or '')
  if item.get('key')=='arrow' and re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',image) and '..' not in image:
   arrow='<span class="edu-arrow icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(image)+'\');transform:rotate(-45deg)"></span>'

 for card in page.xpath('//section[@id="education"]//article[@data-entry-id]'):
  v=records.get(card.get('data-entry-id').removeprefix('education-'),{})
  featured=v.get('featured',False)
  card.set('class',card.get('class','')+' education-v2'+(' education-featured' if featured else ' education-compact'))
  # Keep the existing rich optional-details renderer, including media and attachments.
  details=card.find('details')
  if details is not None:card.remove(details)
  for child in list(card):card.remove(child)
  card.text=None
  logo=url(v.get('institution_logo'));institution=v.get('institution') or ''
  logo_html=('<img class="institution-logo" src="'+esc(logo)+'" alt="'+esc(institution or v['title'])+' logo" width="64" height="64" loading="lazy">') if logo else '<span class="institution-initial" aria-hidden="true">'+esc(str(institution or v['title'])[0].upper())+'</span>'
  title='<h3>'+esc(v['title'])+'</h3>'
  subtitle=v.get('subtitle') or ''
  if subtitle:title+='<p class="edu-subtitle">'+esc(subtitle)+'</p>'
  dest=url(v.get('website'))
  if institution:title+='<p class="institution">'+('<a href="'+esc(dest)+'" target="_blank" rel="noopener noreferrer">'+esc(institution)+arrow+'</a>' if dest else esc(institution))+'</p>'
  start=str(v.get('start_date') or '');end=str(v.get('end_date') or '')
  date=' – '.join(filter(None,[month(start),'Present' if v.get('currently_studying') else month(end)])) or v.get('date') or ''
  if v.get('expected_completion') and not v.get('currently_studying'):date+=' · Expected'
  duration=str(v.get('programme_duration') or '').strip()
  if duration:title+='<p class="edu-duration">'+esc(duration)+'</p>'
  elif date and not (featured and v.get('show_progress',False) and start and end):title+='<p class="edu-date">'+esc(date)+'</p>'
  grade=str(v.get('grade') or '').strip();scale=str(v.get('grade_scale') or '').strip();label=v.get('grade_label') or 'GPA'
  result=''
  try:ratio=max(0,min(1,float(grade)/float(scale)))
  except (ValueError,ZeroDivisionError):ratio=None
  if grade:
   if featured and ratio is not None:
    result='<div class="edu-grade" aria-label="'+esc(label+' '+grade+' of '+scale)+'"><div class="edu-ring" data-ratio="'+str(ratio)+'"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="edu-ring-track" cx="50" cy="50" r="44"/><circle class="edu-ring-fill" cx="50" cy="50" r="44" pathLength="1" stroke-dasharray="'+str(ratio)+' 1"/></svg><div><span class="edu-grade-label">'+esc(label)+'</span><strong>'+esc(grade)+'</strong><small>of '+esc(scale)+'</small></div></div></div>'
   else:result='<span class="edu-grade-chip">'+esc(label+' '+grade+(' / '+scale if scale else ''))+'</span>'
  elif v.get('badge'):result='<span class="edu-grade-chip">'+esc(v['badge'])+'</span>'
  set_html(card,'<div class="edu-heading">'+logo_html+'<div class="edu-title">'+title+'</div>'+result+'</div>')
  if featured and v.get('show_progress',False) and start and end:
   progress=html.Element('div',{'class':'edu-progress','data-start':start,'data-end':end})
   status=v.get('status') or ('In progress' if v.get('currently_studying') else '')
   timeline_label=v.get('timeline_label','')
   set_html(progress,'<div class="edu-progress-top">'+('<span class="edu-status" data-pulse="'+str(bool(v.get('status_pulse',False))).lower()+'"><span aria-hidden="true"></span>'+esc(status)+'</span>' if status else '')+('<span class="edu-timeline-label">'+esc(timeline_label)+'</span>' if timeline_label else '')+'</div><div class="edu-progress-track" role="progressbar" aria-label="Elapsed programme period" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span></span></div><div class="edu-progress-dates"><span>'+esc(month(start))+'</span><span>'+esc(month(end)+(' · Expected' if v.get('expected_completion') else ''))+'</span></div>');card.append(progress)
  elif v.get('status'):
   status=html.fragment_fromstring('<div class="edu-completed-status"><span class="edu-status" data-pulse="'+str(bool(v.get('status_pulse',False))).lower()+'"><span aria-hidden="true"></span>'+esc(v['status'])+'</span></div>');card.append(status)
  # Descriptive text remains CMS-controlled. Existing grade-only prose migrated to subtitle.
  body=v.get('body') or ''
  if body and html.fragment_fromstring('<div>'+body+'</div>').text_content().strip():
   narrative=html.Element('div',{'class':'edu-description'});set_html(narrative,rich(body));card.append(narrative)
  facts=[]
  for key,label_text in [('specialization','Major'),('focus','Focus'),('location','Location'),('student_id','Student ID')]:
   if str(v.get(key) or '').strip():facts.append('<div><dt>'+label_text+'</dt><dd>'+esc(v[key])+'</dd></div>')
  courses=[str(x).strip() for x in v.get('coursework',[]) if str(x).strip()]
  if courses:facts.append('<div><dt>Key courses</dt><dd class="edu-course-chips">'+''.join('<span>'+esc(x)+'</span>' for x in courses)+'</dd></div>')
  if v.get('thesis_title'):facts.append('<div><dt>Thesis / project</dt><dd>'+esc(v['thesis_title'])+'</dd></div>')
  transcript=url(v.get('transcript_link'))
  if transcript:facts.append('<div><dt>Transcript</dt><dd><a href="'+esc(transcript)+'" target="_blank" rel="noopener noreferrer">View transcript '+arrow+'</a></dd></div>')
  if facts:
   if details is None:details=html.fragment_fromstring('<details class="entry-extra" data-animated-details=""><summary>View details<span class="detail-plus" aria-hidden="true">+</span></summary><div class="entry-extra-body"></div></details>')
   content=details.xpath('./div[@class="entry-extra-body"]')[0]
   # Remove only facts rendered in the new grid; preserve every other optional field.
   for fact in content.xpath('.//dl[@class="entry-facts"]/div'):
    if fact.xpath('string(dt)') in ('Specialization','Location','Thesis / dissertation'):fact.getparent().remove(fact)
   for node in content.xpath('.//section[@class="entry-detail-section"]'):
    if node.xpath('string(h3)')=='Relevant coursework':node.getparent().remove(node)
   for empty in content.xpath('.//dl[not(*)]'):empty.getparent().remove(empty)
   grid=html.fragment_fromstring('<dl class="edu-detail-grid">'+''.join(facts)+'</dl>');content.insert(0,grid)
  if details is not None:
   summary=details.find('summary');summary.text=v.get('details_label') or 'View details'
   details.set('data-education-details','');card.append(details)
