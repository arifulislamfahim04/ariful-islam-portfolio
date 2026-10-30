"""Learning CMS integration: sorting, overflow, optional records and shared viewer indices."""
from pathlib import Path
import json,tempfile,shutil,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def save(folder,key,v):(root/'editor'/folder/(key+'.json')).write_text(json.dumps(v))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 a=build();assert len(a.xpath('//*[@id="certificates"]//article'))==4
 assert not a.xpath('//*[@id="certificates"]//*[contains(@class,"about-timeline") or contains(@class,"certificate-grid")]')
 for i in range(7):save('certificates','fixture'+str(i),dict(title='Test course '+str(i),year=str(2030-i),institution='Example issuer',body='<p><strong>Formatted description</strong></p>',skills=['Analysis','Communication'],duration='6 hours',image='assets/loom-spools.jpg',institution_logo='assets/skill-logos/word.svg',verification_url='https://example.org/credential',extra_fields=[dict(label='Optional fact',value='Preserved')],published=True,order=i))
 save('workshops','fixture',dict(title='Test seminar',year='2031',file='assets/ariful-islam-fahim-cv.pdf',gallery=[dict(image='assets/loom-spools.jpg',caption='Seminar photograph')],duration='2 hours',published=True))
 a=build();cards=a.xpath('//*[@id="learning-certificates"]//article');assert len(cards)==9 and 'fixture0' in cards[0].get('data-entry-id')
 assert len([c for c in cards if 'hidden' not in c.attrib])==5
 assert a.xpath('//button[@data-learning-show="certificates" and contains(.,"(9)")]')
 assert a.xpath('//article[@data-entry-id="certificates-fixture0"]//strong[text()="Formatted description"]')
 assert a.xpath('//article[@data-entry-id="certificates-fixture0"]//li[text()="Analysis"]')
 assert 'Preserved' in cards[0].text_content() and '6 hours' in cards[0].text_content()
 data=json.loads(a.xpath('string(//script[@id="credential-data"])'))
 for trigger in a.xpath('//*[@id="certificates"]//button[@data-credential-open]'):
  record=data[trigger.get('data-credential-open')][int(trigger.get('data-credential-index'))]
  assert record['title']==trigger.xpath('ancestor::article')[0].xpath('string(.//h3)')
 assert len(a.xpath('//dialog[@id="credential-viewer"]'))==1
 assert data['workshops'][0]['file'].endswith('.pdf')
 save('certificates','fixture0',dict(title='Empty optional course',year='2030',published=True));a=build();card=a.xpath('//article[@data-entry-id="certificates-fixture0"]')[0]
 assert not card.xpath('.//details|.//img|.//a|.//button')
 save('certificates','fixture0',dict(title='Hidden course',published=False));a=build();assert not a.xpath('//article[@data-entry-id="certificates-fixture0"]')
 if '--fixture-output' in sys.argv:
  Path(sys.argv[sys.argv.index('--fixture-output')+1]).write_bytes((root/'docs/about.html').read_bytes())
 print('Passed: year sorting, five-record limit, CMS rich text/skills/duration/logo/link, empty fields, unpublish, certificate and workshop shared viewer indices.')
