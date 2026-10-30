"""The global footer and navigation remain one CMS-driven component on every route."""
from pathlib import Path
import json,tempfile,shutil,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def save(path,value):(root/path).write_text(json.dumps(value))
 def load(path):return json.loads((root/path).read_text())
 def build():subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
 def page(name='index'):return html.parse(str(root/'docs'/(name+'.html')))
 build()
 for path in (root/'docs').glob('*.html'):
  d=html.parse(str(path));f=d.xpath('//footer');assert len(f)==1 and f[0].get('id')=='site-footer'
  assert len(d.xpath('//*[@id="back-top"]'))==1
  assert d.xpath('//link[contains(@href,"shared-footer.css")]') and d.xpath('//script[contains(@src,"shared-footer.js")]')
  assert f[0].xpath('.//a[@aria-label="LinkedIn"]') and f[0].xpath('.//a[@aria-label="Email"]')
  assert not f[0].xpath('.//a[contains(@aria-label,"YouTube") or contains(@aria-label,"Twitter")]')
  assert f[0].xpath('.//button[@data-footer-copy]') and f[0].xpath('.//span[@data-footer-year]')
  assert len(f[0].xpath('.//nav[@aria-label="Footer navigation"]/a'))==6
 assert not page().xpath('//section[contains(@class,"closing-cta")]')
 assert not page().xpath('//div[@class="footer-signature"]')
 profile=load('editor/profile.json');profile.update(email='new@example.org',phone='+8801234567890',availability='Available for a new role',location='Updated location',linkedin='https://example.org/linkedin');save('editor/profile.json',profile)
 footer=load('editor/footer.json');footer.update(show_wordmark=True,tagline='Editable footer tagline');footer['socials'] += [dict(label='Video channel',source='Custom URL',url='https://example.org/channel',icon='youtube',published=True)];save('editor/footer.json',footer)
 site=load('editor/site.json');site['navigation']=[dict(page='contact',label='Let’s talk',icon='contact',published=True),dict(page='index',label='Start',icon='home',published=True)];save('editor/site.json',site);build()
 for name in ['index','about','projects','gallery','blogs','contact','posts-note1','projects-smart']:
  d=page(name);f=d.xpath('//footer')[0];assert 'Editable footer tagline' in f.text_content() and 'Updated location' in f.text_content()
  assert f.xpath('.//a[@href="mailto:new@example.org"]') and f.xpath('.//a[@href="tel:+8801234567890"]')
  assert f.xpath('.//a[@aria-label="Video channel" and @target="_blank"]') and f.xpath('.//div[@class="footer-elsewhere"]')
  assert f.xpath('.//div[@class="footer-signature"]')
  assert f.xpath('.//nav/a/@href')==['contact.html','index.html']
  nav=d.xpath('//nav[@class="dock-nav"]')[0];assert nav.xpath('./a/@href')==['contact.html','index.html']
  assert d.xpath('//nav[@class="menu-links"]/a/@href')==['contact.html','index.html']
  assert 'Available for a new role' in f.text_content()
 footer.update(socials=[],show_wordmark=False);save('editor/footer.json',footer);profile.update(email='',phone='',availability='',location='',linkedin='');save('editor/profile.json',profile);site['navigation']=[];save('editor/site.json',site);build();d=page();f=d.xpath('//footer')[0]
 assert not f.xpath('.//a[starts-with(@href,"mailto:") or starts-with(@href,"tel:")]|.//button|.//nav|.//div[@class="footer-elsewhere"]|.//div[@class="footer-socials"]|.//span[@class="footer-status"]')
 assert d.xpath('string(//body/@data-page)')=='index'
 print('Passed: one footer/back-to-top on 14 routes, real/blank social links, shared Profile contacts/status, reorder/hide shared navigation, wordmark/labels, empty fields and no duplicate Home CTA.')
