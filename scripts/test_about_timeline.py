"""About timelines preserve content and expose only explicit CMS marker state."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 a=build();links=a.xpath('//nav[@class="section-index"]/a');assert [x.xpath('string(span)') for x in links]==[f'{i:02d}' for i in range(1,len(links)+1)]
 assert a.xpath('//article[@data-entry-id="education-01" and @data-timeline-state="results-pending"]')
 assert len(a.xpath('//div[contains(@class,"about-timeline")]'))==1
 assert not a.xpath('//*[@id="experience"]//*[contains(@class,"about-timeline")]')
 assert not a.xpath('//*[@id="certificates"]//*[contains(@class,"about-timeline")]')
 assert not a.xpath('//*[@id="recognition" or @id="skills"]//*[contains(@class,"about-timeline")]')
 assert not a.xpath('//*[@data-timeline-reveal and @data-reveal]')
 p=root/'editor/education/01.json';v=json.loads(p.read_text());v['timeline_state']='upcoming';p.write_text(json.dumps(v));a=build()
 assert a.xpath('//article[@data-entry-id="education-01"]//span[@class="about-timeline-dot" and @aria-label="Upcoming"]')
 assert a.xpath('//article[@data-entry-id="education-01"]//div[@aria-label="CGPA 3.90 of 4.00"]')
 assert a.xpath('//article[@data-entry-id="education-01"]//span[@class="edu-status" and contains(.,"Results pending")]')
 print('Passed: automatic section numbering, explicit timeline states, unchanged score/status, compact certificates/workshops, independent awards/skills and one card reveal.')
