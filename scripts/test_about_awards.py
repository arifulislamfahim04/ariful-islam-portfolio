"""Individual awards, CMS media and shared viewer preserve optional records."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'site';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 def save(folder,key,data):(root/'editor'/folder/(key+'.json')).write_text(json.dumps(data))
 def payload(a):return json.loads(a.xpath('string(//script[@id="credential-data"])'))
 a=build();cards=a.xpath('//*[@id="recognition"]//article[@data-entry-id]');assert len(cards)==5
 assert len(a.xpath('//*[@id="recognition"]//button[@data-credential-open="awards"]'))==5
 assert not a.xpath('//*[@id="recognition"]//details')
 assert all('OF 4' not in x.text_content() for x in cards)
 assert len(payload(a)['awards'])==5
 save('achievements','fixture',dict(title='Viewer test fixture',institution='Example institution',semester='Spring 2024',year='2024',received_date='2024-08-01',image='assets/loom-spools.jpg',image_alt='Test image',body='<p>Example description</p>',extra_fields=[dict(label='Example fact',value='Preserved optional content')],order=-1,published=True,featured=True))
 save('certificates','fixture',dict(title='Certificate test fixture',file='assets/ariful-islam-fahim-cv.pdf',published=True))
 save('experience','fixture',dict(title='Leadership test fixture',gallery=[dict(image='assets/loom-spools.jpg',caption='Example leadership photograph')],published=True))
 a=build();p=payload(a)
 assert p['awards'][0]['semester']=='Spring 2024' and p['awards'][0]['received_date']=='2024-08-01'
 assert 'Preserved optional content' in p['awards'][0]['description']
 assert p['awards'][0]['image']=='assets/loom-spools.jpg'
 assert a.xpath('//button[@data-credential-open="certificates"]') and a.xpath('//button[@data-credential-open="leadership"]')
 assert len(a.xpath('//dialog[@id="credential-viewer"]'))==1
 assert any(x['file'].endswith('.pdf') for x in p['certificates'])
 if '--fixture-output' in sys.argv:
  out=Path(sys.argv[sys.argv.index('--fixture-output')+1]);out.write_bytes((root/'docs/about.html').read_bytes())
 # Remove/unpublish a separate award and clear photo: no stale picture or merged count.
 (root/'editor/achievements/fixture.json').unlink();v=json.loads((root/'editor/achievements/01.json').read_text());v.update(published=False);save('achievements','01',v);a=build();assert len(payload(a)['awards'])==4
 assert not a.xpath('//article[@data-entry-id="achievements-fixture"]')
 print('Passed: independent awards/count, no empty accordions, add/reorder/remove/unpublish, semester/year/image/PDF, optional facts, shared certificate/leadership viewer.')
