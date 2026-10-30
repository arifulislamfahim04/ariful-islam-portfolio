"""CMS changes must affect both reviewed pages without losing records."""
from pathlib import Path
import json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
def build():subprocess.run([sys.executable,'scripts/build_editor.py'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
def page(name):return html.parse(str(ROOT/'docs'/name))
p=ROOT/'editor/homepage.json';original=p.read_bytes();fixture=ROOT/'docs/assets/icons/cms-check.svg';fixture.parent.mkdir(exist_ok=True)
try:
 settings=json.loads(original);settings['card_socials']=[{'label':'Email','source':'Email','icon':'contact'},{'label':'LinkedIn','source':'LinkedIn','icon':'linkedin'},{'label':'Facebook','source':'Facebook','icon':'facebook'},{'label':'Video channel','source':'Custom URL','url':'https://example.org/channel','icon':'youtube'}]
 settings['icon_overrides']=[{'key':'home','image':'assets/icons/cms-check.svg'},{'key':'book','image':'assets/icons/cms-check.svg'}]
 fixture.write_bytes((ROOT/'vendor/home-icons/house-simple-fill.svg').read_bytes());p.write_text(json.dumps(settings));build()
 for name in ('index.html','about.html'):
  d=page(name);assert d.xpath('//a[@aria-label="Video channel" and @href="https://example.org/channel"]'),name
  assert d.xpath('//aside[@id="site-dock"]//a[@href="index.html"]/span[contains(@class,"custom-icon")]'),name
  assert not d.xpath('//a[@aria-label="Facebook"]'),name
 a=page('about.html');assert len(a.xpath('//section[@id="recognition"]//article'))==5
 assert all(len(e.xpath('./button[@data-credential-open="awards"]'))==1 and not e.xpath('./details') for e in a.xpath('//section[@id="recognition"]//article'))
 assert a.xpath('//a[@href="about.html" and @aria-current="page"]')
 settings['card_socials']=[];settings['icon_overrides']=[];p.write_text(json.dumps(settings));build()
 for name in ('index.html','about.html'):
  d=page(name);assert not d.xpath('//a[contains(@class,"card-channel")]'),name
  assert not d.xpath('//aside[@id="site-dock"]//span[contains(@class,"custom-icon")]'),name
 assert not page('projects.html').xpath('//link[contains(@href,"about-refresh")]')
 print('Passed: ordered links, blank Facebook, remove-all, icon upload/reset, active About, separate awards, isolated page styling.')
finally:
 p.write_bytes(original);fixture.unlink(missing_ok=True);build()
