"""Facts panel CMS wiring: no private references, no duplicate study status."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 def read(path):return json.loads((root/path).read_text())
 def write(path,v):(root/path).write_text(json.dumps(v))
 a=build();panel=a.xpath('//*[@id="about-facts"]')[0]
 assert panel.xpath('.//p[text()="Results pending · undergraduate"]')
 assert len(panel.xpath('.//div[@class="study-segments"]/span[@class="reached"]'))==4
 assert panel.xpath('.//a[starts-with(@href,"mailto:")]') and panel.xpath('.//a[starts-with(@href,"tel:")]')
 assert not panel.xpath('.//time|.//a[@class="facts-whatsapp"]')
 assert panel.xpath('.//dd[@class="facts-languages"]/span[text()="Bengali"]')
 assert 'Professional working' not in panel.text_content()
 edu=read('editor/education/01.json');edu.update(status='Completed',specialization='Textile research',programme_year=3);write('editor/education/01.json',edu)
 settings=read('editor/about-presentation.json');settings.update(whatsapp_url='https://wa.me/0000000000',reviewed_on='2026-10-29');write('editor/about-presentation.json',settings);a=build();panel=a.xpath('//*[@id="about-facts"]')[0]
 assert panel.xpath('.//p[text()="Completed · undergraduate"]') and panel.xpath('.//dd[text()="Textile research"]')
 assert len(panel.xpath('.//div[@class="study-segments"]/span[@class="reached"]'))==3
 assert panel.xpath('.//a[@class="facts-whatsapp" and @href="https://wa.me/0000000000"]')
 assert panel.xpath('.//time[text()="Updated Oct 2026"]')
 # Clearing optional data removes controls/labels; no stale glance status reappears.
 profile=read('editor/profile.json');profile.update(email='',phone='',availability='');write('editor/profile.json',profile)
 edu.update(status='',specialization='',programme_years=0);write('editor/education/01.json',edu)
 settings.update(whatsapp_url='',reviewed_on='');write('editor/about-presentation.json',settings);a=build();panel=a.xpath('//*[@id="about-facts"]')[0]
 assert not panel.xpath('.//div[@class="facts-now"]|.//div[@class="facts-contacts"]|.//button|.//time')
 assert 'Final year' not in panel.text_content()
 print('Passed: Profile contact wiring, single-source degree status/specialization/year, language chips, optional WhatsApp/review date, empty sections hidden.')
