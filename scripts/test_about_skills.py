"""Skills CMS lifecycle and honest, unscored rendering."""
from pathlib import Path
import json,tempfile,shutil,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 p=root/'editor/skills.json';v=json.loads(p.read_text());a=build();s=a.xpath('//*[@id="skills"]')[0]
 assert len(s.xpath('.//li[@class="tool-row"]'))==9
 assert s.xpath('.//span[@class="tool-name" and text()="PowerPoint"]/following-sibling::span//span[text()="Advanced"]')
 assert s.xpath('.//span[@class="tool-name" and text()="Excel"]/following-sibling::span//span[text()="Basic"]')
 assert not s.xpath('.//*[@role="meter" or @role="progressbar" or @aria-valuenow]')
 assert 'GSM testing' not in s.text_content() and 'Tensile' not in s.text_content()
 assert s.xpath('.//span[@lang="bn" and text()="বাংলা"]')
 assert s.xpath('.//p[text()="Professional working"]')
 # Add/reorder and remove items, change labels, logo and usage; there is no score model.
 v['tools'].insert(0,dict(name='Example tool',level='Learning',logo='',monogram='ET',usage='Example context',published=True))
 v['languages'].append(dict(name='Example language',level='Learning',published=True))
 v['tools'][1]['published']=False;p.write_text(json.dumps(v));a=build();s=a.xpath('//*[@id="skills"]')[0]
 assert s.xpath('.//li[@class="tool-row"][1]//span[text()="Example tool"]')
 assert s.xpath('.//li[@class="tool-row"][1][@tabindex="0"]//span[@role="tooltip" and text()="Example context"]')
 assert not s.xpath('.//span[@class="tool-name" and text()="PowerPoint"]')
 assert a.xpath('//*[@id="about-facts"]//dd[@class="facts-languages"]/span[text()="Example language"]')
 v.update(tools=[],groups=[],languages=[]);p.write_text(json.dumps(v));a=build();s=a.xpath('//*[@id="skills"]')[0]
 assert not s.xpath('.//article|.//img|.//details')
 assert not a.xpath('//*[@id="about-facts"]//dd[@class="facts-languages"]')
 settings=root/'editor/about-presentation.json';d=json.loads(settings.read_text());d['recruiter_details']=[dict(label='Earliest start',value=''),dict(label='Example preference',value='Example value')];settings.write_text(json.dumps(d));a=build()
 assert a.xpath('//*[@id="about-facts"]//dt[text()="Example preference"]/following-sibling::dd[text()="Example value"]')
 assert not a.xpath('//*[@id="about-facts"]//dt[text()="Earliest start"]')
 print('Passed: separate tools, unscored rings/languages, user levels, add/reorder/remove/draft/usage fields, language chips from one source, optional recruiter facts.')
