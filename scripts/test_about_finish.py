"""Optional presentation fields retain content and can be cleared without code."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def page(name):return html.parse(str(base/'docs'/name))
 p=base/'editor/about-presentation.json';d=json.loads(p.read_text());d.update(recommendations=[],intro_animation=False,cursor_follower=False);p.write_text(json.dumps(d))
 edu=next((base/'editor/education').glob('*.json'));v=json.loads(edu.read_text());v['institution_logo']='assets/loom-spools.jpg';edu.write_text(json.dumps(v));build();a=page('about.html')
 assert not a.xpath('//article[@class="recommendation-card"]')
 assert not a.xpath('//div[@class="mint-cursor" or @class="wordmark-intro"]')
 assert a.xpath('/html[@data-page-signature="false" and @data-custom-cursor="false"]')
 assert a.xpath('//img[@class="institution-logo"]')
 assert a.xpath('//section[@class="profile-facts-panel"]//dt[contains(text(),"Study stage")]')
 assert not a.xpath('//aside[contains(@class,"at-glance")]')
 d.update(recommendations=[{'quote':'A clearly marked test quotation.','name':'Example','sample':True,'published':True}],intro_animation=True,cursor_follower=True,intro_wordmark='TEST NAME');p.write_text(json.dumps(d));build();a=page('about.html')
 assert a.xpath('//article[@class="recommendation-card"]//span[contains(text(),"not a real endorsement")]')
 assert ''.join(a.xpath('//*[@class="signature-wordmark"]//text()'))=='TEST NAME'
 assert a.xpath('/html[@data-page-signature="true" and @data-custom-cursor="true"]')
 assert not a.xpath('//div[@class="wordmark-intro"]')
 assert len(a.xpath('//details[@data-animated-details]'))>0
 print('Passed: recommendations add/remove, sample label, logo upload, unique profile facts, motion controls and shared navigation wordmark.')
