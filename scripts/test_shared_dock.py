"""Navigation consistency, parent-page state and CMS edits across real routes."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
 root=Path(folder)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
 def read(name):return html.parse(str(root/'docs'/(name+'.html')))
 build()
 for p in (root/'docs').glob('*.html'):
  d=html.parse(str(p));dock=d.xpath('//*[@id="site-dock"]');assert len(dock)==1,p
  assert len(d.xpath('//*[@id="back-top"]'))==1,p
  assert len(dock[0].xpath('.//nav[@aria-label="Main navigation"]/a'))==6,p
  active=dock[0].xpath('.//a[@aria-current="page"]');assert len(active)==(0 if p.stem=='404' else 1),p
  expected='projects' if p.stem.startswith('projects-') else 'blogs' if p.stem.startswith('posts-') else p.stem
  assert not active if p.stem=='404' else active[0].get('href')==expected+'.html',p
  assert len(d.xpath('//button[@data-theme-toggle]'))==2,p
  assert d.xpath('//dialog[@id="site-menu" and @aria-labelledby="site-menu-title"]//a[@aria-current="page"]/@href')==([] if p.stem=='404' else [expected+'.html']),p
  assert d.xpath('//*[@id="site-dock"]//button[@data-dock-menu and @aria-controls="site-menu"]'),p
  assert not d.xpath('//aside[@class="hero-rail" or @class="dock-rail"]|//nav[@class="header-nav"]'),p
  assert d.xpath('//*[@id="back-top"]//circle[@pathlength="100"]'),p
 site_path=root/'editor/site.json';site=json.loads(site_path.read_text());site['navigation']=[dict(page='contact',label='Say hello',icon='contact',published=True),dict(page='about',label='My background',icon='about',published=True),dict(page='gallery',published=False)]
 site_path.write_text(json.dumps(site));build()
 for name in ['index','about','projects-smart','posts-note1']:
  d=read(name);assert d.xpath('//*[@id="site-dock"]//nav/a/@href')==['contact.html','about.html']
  assert d.xpath('//*[@id="site-menu"]//nav/a/@href')==['contact.html','about.html']
  assert d.xpath('//footer//nav/a/@href')==['contact.html','about.html']
  assert 'Say hello' in d.xpath('string(//*[@id="site-menu"])')
 print('Passed: one shared dock/menu on all routes including 404, parent-page state, one progress control, linked theme controls and CMS reorder/hide/rename consistency.')
