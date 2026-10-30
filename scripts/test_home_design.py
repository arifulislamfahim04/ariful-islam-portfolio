"""Regression coverage for the redesigned homepage/gallery content lifecycle."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','.openai','__pycache__'))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def doc(name):return html.parse(str(base/'docs'/name))
 def save(path,value):(base/path).write_text(json.dumps(value))
 build();h=doc('index.html');assert h.xpath('//div[@class="hero-card-photo"]/img/@src')==['assets/ariful-portrait.jpg'];assert h.xpath('//div[@class="hero-role"]/@data-hero-phrases');assert not h.xpath('//*[contains(@class,"physical-stage")]');assert len(h.xpath('//div[@class="hero-stat"]'))==4
 for p in (base/'docs').glob('*.html'):
  d=doc(p.name);expected=['index.html','about.html','projects.html','gallery.html','blogs.html','contact.html']
  if p.name in ('index.html','about.html'):
   assert d.xpath('//nav[@class="dock-nav"]/a/@href')==expected
   assert len(d.xpath('//nav[@class="dock-nav"]/a[@aria-current="page"]'))==1
  else:
   assert d.xpath('//nav[@class="dock-nav"]/a/@href')==expected
   assert d.xpath('//nav[@aria-label="Footer navigation"]/a/@href')==expected
  assert d.xpath('//nav[@class="menu-links"]/a/@href')==expected
  if p.name not in ('index.html','about.html','404.html'):assert len(d.xpath('//nav[@class="dock-nav"]/a[@aria-current="page"]'))==1
  assert len(d.xpath('//*[@id="moment-viewer"]'))==1
  assert len(d.xpath('//*[@id="back-top"]'))==1
  assert d.xpath('//link[starts-with(@href,"editorial.css")]')
  assert not d.xpath('//script[starts-with(@src,"site.js") or starts-with(@src,"home-polish.js")]')
 assert len(doc('gallery.html').xpath('//article[contains(@class,"gallery-item")]'))==6
 assert len(h.xpath('//div[@class="preview-row"]'))==2
 item=dict(title='A real moment',image='assets/loom-spools.jpg',published=True,featured=True,order=0,body='<p>My story</p>',caption='A real caption',date='2026',location='Dhaka',category='Personal')
 save('editor/gallery/personal.json',item);build();assert doc('gallery.html').xpath('//*[@id="gallery-personal"]');assert doc('index.html').xpath('//a[@href="gallery.html#gallery-personal"]');assert not doc('gallery.html').xpath('//*[@id="gallery-personal"]//span[@class="sample-label"]')
 item['featured']=False;save('editor/gallery/personal.json',item);build();assert not doc('index.html').xpath('//a[@href="gallery.html#gallery-personal"]');assert doc('gallery.html').xpath('//*[@id="gallery-personal"]')
 item['published']=False;save('editor/gallery/personal.json',item);build();assert not doc('gallery.html').xpath('//*[@id="gallery-personal"]');assert 'A real moment' not in (base/'docs/content.js').read_text()
 for p in (base/'editor/gallery').glob('*.json'):p.unlink()
 build();assert not doc('index.html').xpath('//div[@class="preview-wall"]');assert doc('gallery.html').xpath('//*[contains(@class,"gallery-empty-state")]')
 p=json.loads((base/'editor/profile.json').read_text());p.update(photo='',name='New Full Name',availability='New availability');save('editor/profile.json',p);s=json.loads((base/'editor/homepage.json').read_text());s.update(typewriter_phrases=['A new phrase.'],status_chips=['New chip'],logo_text='newname');save('editor/homepage.json',s);build();h=doc('index.html');assert h.xpath('//span[@class="hero-monogram"]');assert 'A new phrase.' in h.xpath('string(//div[@class="hero-role"])');assert h.xpath('//h2[@class="hero-card-name"]/text()')==['New Full Name'];assert 'New availability' in h.xpath('string(//div[@class="hero-availability"])')
print('Passed: six-page shared nav, portrait/CMS replacement, typewriter/availability, gallery lifecycle and empty states')
