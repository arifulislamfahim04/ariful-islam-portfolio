"""CMS-editable skills and unscored language/tool rings, isolated to About."""
import json,re
from lxml import html

def refine_skills(page,*,root,esc,url,set_html):
 v=json.loads((root/'editor/skills.json').read_text());section=page.xpath('//*[@id="skills"]')[0];header=section.find('header')
 h=header.find('h2');set_html(h,esc(v.get('heading') or 'Skills'))
 if v.get('intro'):
  p=html.Element('p');p.text=v['intro'];header.append(p)
 for child in list(section):
  if child is not header:section.remove(child)
 symbols={s.get('id'):s for s in page.xpath('//symbol')};overrides={x.get('key'):x.get('image') for x in json.loads((root/'editor/homepage.json').read_text()).get('icon_overrides',[])}
 def icon(key):
  custom=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:return '<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'
  symbol=symbols.get('i-'+key)
  return '<svg class="icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">'+(''.join(html.tostring(s,encoding='unicode') for s in symbol) if symbol is not None else '')+'</svg>'
 cards=''
 tools=[x for x in v.get('tools',[]) if x.get('published',True) and str(x.get('name') or '').strip()]
 if tools:
  rows=''
  for i,tool in enumerate(tools):
   name=tool['name'];logo=url(tool.get('logo'));level=str(tool.get('level') or '').strip();usage=str(tool.get('usage') or '').strip()
   visual='<img src="'+esc(logo)+'" alt="" width="24" height="24" loading="lazy">' if logo else '<span>'+esc(tool.get('monogram') or name[:2].upper())+'</span>'
   rows+='<li class="tool-row"'+(' tabindex="0" aria-describedby="tool-use-'+str(i)+'"' if usage else '')+'><span class="tool-logo">'+visual+'</span><span class="tool-name">'+esc(name)+'</span>'+('<span class="skill-level-orbit" aria-label="'+esc('Self-described level: '+level)+'"><span>'+esc(level)+'</span></span>' if level else '')+('<span class="tool-usage" role="tooltip" id="tool-use-'+str(i)+'">'+esc(usage)+'</span>' if usage else '')+'</li>'
  cards+='<article class="skill-group toolkit-group"><div class="skill-group-heading"><span class="skill-group-icon">'+icon('focus')+'</span><div><h3>'+esc(v.get('tools_heading') or 'Software & tools')+'</h3>'+('<p>'+esc(v['tools_description'])+'</p>' if v.get('tools_description') else '')+'</div></div><ul class="tool-stack">'+rows+'</ul>'+('<p class="skill-level-note">'+esc(v['level_note'])+'</p>' if v.get('level_note') else '')+'</article>'
 for group in v.get('groups',[]):
  items=[str(x).strip() for x in group.get('items',[]) if str(x).strip()]
  if not group.get('published',True) or not items:continue
  cards+='<article class="skill-group"><div class="skill-group-heading"><span class="skill-group-icon">'+icon(group.get('icon') or 'research')+'</span><div><h3>'+esc(group.get('title'))+'</h3>'+('<p>'+esc(group['description'])+'</p>' if group.get('description') else '')+'</div></div>'+('<span class="skill-draft">'+esc(group.get('draft_label') or 'Suggested skills · review')+'</span>' if group.get('draft') else '')+'<ul class="textile-skill-chips">'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul></article>'
 if cards:section.append(html.fragment_fromstring('<div class="skills-v4-grid">'+cards+'</div>'))
 languages=[x for x in v.get('languages',[]) if x.get('published',True) and x.get('name')]
 if languages:
  content='<h3 class="skills-languages-heading"><span class="section-label">'+icon('language')+esc(v.get('languages_heading') or 'Languages')+'</span></h3><div class="skills-language-grid">'
  for lang in languages:
   name=lang['name'];level=lang.get('level') or ''
   native='<span lang="'+esc(lang.get('native_tag') or '')+'" class="bengali-script">'+esc(lang['native_script'])+'</span>' if lang.get('native_script') else ''
   content+='<article class="skills-language-card"><span class="language-orbit" aria-hidden="true">'+icon('language')+'</span><div><h4>'+esc(name)+native+'</h4>'+('<p>'+esc(level)+'</p>' if level else '')+'</div></article>'
  content+='</div>';section.append(html.fragment_fromstring('<div class="skills-languages">'+content+'</div>'))
 if tools:
  section.append(html.fragment_fromstring('<details class="skill-icon-credits"><summary>'+esc(v.get('icon_credits_label') or 'Icon credits')+'</summary><p>Logos from SVG Repo: Office icons by vscode-icons (MIT); AutoCAD by Pictonic (CC Attribution); GitHub by jimlamb (public domain); Canva under its logo licence. Brand marks identify tools used and do not imply endorsement. <a href="assets/skill-logos/SOURCES.md">Sources and licence notices</a>.</p></details>'))
