"""CMS coverage for independent roles, event grid and shared photo viewer."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def save(key,v):(root/'editor/experience'/(key+'.json')).write_text(json.dumps(v))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 a=build();assert len(a.xpath('//*[@id="experience"]//article[contains(@class,"exposure-role ")]'))==2
 assert len(a.xpath('//*[@id="experience"]//article[contains(@class,"exposure-event ")]'))==2
 assert not a.xpath('//*[@id="experience"]//*[contains(@class,"about-timeline") or contains(@class,"edu-ring")]')
 intern=a.xpath('//article[@data-entry-id="experience-04"]')[0];assert 'Completed' in intern.text_content() and 'Started Jul 2026' in intern.text_content() and 'Present' not in intern.text_content()
 rep=a.xpath('//article[@data-entry-id="experience-01"]')[0];assert '40+' in rep.text_content() and not rep.xpath('.//details//li[contains(.,"students")]')
 assert not a.xpath('//*[@id="experience"]//ul[@class="exposure-years"]')
 save('fixture',dict(title='Example role',record_type='role',start_date='2023-07',end_date='2024-09',currently_working=False,body='<p><em>Visible introduction</em></p>',responsibilities='<ul><li>Visible responsibility</li></ul>',impact=[dict(value='12',label='Projects'),dict(value='',label='Hidden metric')],image='assets/loom-spools.jpg',institution_logo='assets/loom-spools.jpg',extra_fields=[dict(label='Extra fact',value='Preserved fact')],published=True,order=-1))
 save('event',dict(title='Example visits',record_type='event',event_type='Exhibition',venue='Example venue',city='Dhaka',years=['2023','2025'],gallery=[dict(image='assets/loom-spools.jpg',caption='Example visit photo')],published=True))
 a=build();r=a.xpath('//article[@data-entry-id="experience-fixture"]')[0];assert '1 yr 2 mos' in r.text_content();assert 'Hidden metric' not in r.text_content();assert r.xpath('.//div[@class="exposure-proof"]//li[text()="Visible responsibility"]');assert r.xpath('.//em[text()="Visible introduction"]');assert 'Preserved fact' in r.text_content()
 years=a.xpath('//article[@data-entry-id="experience-event"]//ul[@class="exposure-years"]/li/text()');assert years==['2023','2025']
 data=json.loads(a.xpath('string(//script[@id="credential-data"])'))
 for b in a.xpath('//*[@id="experience"]//*[@data-credential-open]'):
  entry=data['leadership'][int(b.get('data-credential-index'))];assert entry['title']==b.xpath('ancestor::article')[0].xpath('string(.//h3)')
 assert len(a.xpath('//dialog[@id="credential-viewer"]'))==1
 save('fixture',dict(title='Example role',record_type='role',start_date='2023-07',currently_working=True,published=True));a=build();r=a.xpath('//article[@data-entry-id="experience-fixture"]')[0];assert r.xpath('.//span[contains(@class,"ongoing")]');assert 'Since Jul 2023' in r.text_content();assert not r.xpath('.//details|.//img|.//dl|.//button')
 save('fixture',dict(title='Example role',published=False));a=build();assert not a.xpath('//article[@data-entry-id="experience-fixture"]')
 if '--fixture-output' in sys.argv:Path(sys.argv[sys.argv.index('--fixture-output')+1]).write_bytes((root/'docs/about.html').read_bytes())
 print('Passed: role/event layouts, completed internship, visible proof, 40+ cohort, unknown dates, confirmed year pips, add/order/unpublish, optional impact/logo/media, shared viewer indices.')
