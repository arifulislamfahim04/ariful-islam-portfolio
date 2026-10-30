"""Integration coverage for optional form data and the HTML visitors actually see."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
def dump(p,v):p.write_text(json.dumps(v))
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def document():return html.parse(str(base/'docs/about.html'))
 def card(title):return document().xpath('//article[.//h3[text()="'+title+'"]]')[0]
 def data():
  raw=(base/'docs/content.js').read_text()
  return json.loads(raw.split('window.PORTFOLIO_DETAILS=')[1].split(';\nwindow.PORTFOLIO_DOCUMENTS=')[0]),json.loads(raw.split('window.PORTFOLIO_DOCUMENTS=')[1].split(';\nwindow.PORTFOLIO_PROFILE=')[0])
 config=json.loads((base/'.pages.yml').read_text())
 collections=[e for e in config['content'] if e['type']=='collection' and e['name'] not in ('gallery','updates')]
 # A title is the only required content field; optional fields must be genuine.
 for e in collections:
  names=[f['name'] for f in e['fields']];assert len(names)==len(set(names))
  assert all(not f.get('required') for f in e['fields'] if f['name']!='title')
  assert {'additional_details','extra_fields','gallery','attachments','related_links','video_url'}<=set(names)
 # Missing keys, cleared fields, empty editor markup and blank list items render no gaps.
 empty=dict(body='<p><br></p>',additional_details='<p> </p>',extra_fields=[{'label':'Never show this empty label','value':''}],gallery=[{'image':'','caption':'Orphan caption'}],attachments=[{'file':'','label':'Orphan document'}],related_links=[{'label':'Orphan link','url':''}])
 for e in collections:dump(base/'editor'/e['name']/'optional-empty.json',dict(title='Empty '+e['name'],published=True,**empty))
 build();stories,docs=data()
 initial_asset=html.parse(str(base/'docs/index.html')).xpath('//script[contains(@src,"content.js?v=")]/@src')[0]
 for kind in ('education','experience','workshops','certificates','achievements'):
  c=card('Empty '+kind)
  assert not c.xpath('.//details|.//p|.//img|.//button[not(@data-credential-open)]|.//span[contains(@class,"care-chip") or contains(@class,"fact-chip")]'),html.tostring(c)
 for kind in ('posts','projects'):
  d=html.parse(str(base/'docs'/f'{kind}-optional-empty.html'))
  assert not d.xpath('//div[@class="story-body"]/*'),html.tostring(d)
 assert all('Orphan' not in d.get('body','') for d in docs)
 common=dict(published=True,additional_details='<p>Extra narrative</p>',extra_fields=[{'label':'Custom fact','value':'Custom value'}],gallery=[{'image':'assets/wool-weave.jpg','caption':'Gallery caption'}],attachments=[{'file':'assets/ariful-islam-fahim-cv.pdf','label':'Supporting report'}],related_links=[{'url':'https://example.org','label':'Official link'}],video_url='https://youtu.be/dQw4w9WgXcQ')
 fixtures={
 'education':dict(degree='Master of Science',department='Textiles',specialization='Smart materials',location='Dhaka',start_date='2028',end_date='2030',currently_studying=True,grade='3.95',grade_scale='4.00',thesis_title='Responsive fibres',supervisor='Example supervisor',coursework=['Materials science']),
 'experience':dict(employment_type='Internship',location='Remote',start_date='2027',end_date='2028',currently_working=True,organization_url='https://example.org/company',responsibilities='<p>Inspect fabrics</p>',achievements='<p>Improved quality</p>',skills=['Testing']),
 'achievements':dict(award_category='Research',recognition_type='Team',reason='<p>Original research</p>',related_work='Textile study',verification_url='https://example.org/award'),
 'certificates':dict(issue_date='2027-01-01',expiry_date='2029-01-01',credential_id='ABC-123',verification_url='https://example.org/verify',skills=['Analysis']),
 'projects':dict(status='Completed',start_date='2027',end_date='2028',role='Researcher',collaborators=['Example team'],objectives='<p>Measure performance</p>',methods='<p>Laboratory testing</p>',results='<p>Useful results</p>',report='assets/ariful-islam-fahim-cv.pdf'),
 'posts':dict(author='Example author',tags=['Textiles'],last_updated='2027-02-01',references='<p>Reference source</p>'),
 'workshops':dict(duration='12 hours',location='Online',participation_role='Participant',learning_outcomes='<p>New learning</p>')}
 for kind,values in fixtures.items():dump(base/'editor'/kind/'optional-full.json',dict(title='Full '+kind,**common,**values))
 build();stories,docs=data()
 next_asset=html.parse(str(base/'docs/index.html')).xpath('//script[contains(@src,"content.js?v=")]/@src')[0]
 assert initial_asset!=next_asset,'Content changes must invalidate cached assets'
 document_bodies={d['id']:d['body'] for d in docs}
 for kind in fixtures:
  if kind in ('posts','projects'):body=stories[kind+'-optional-full']['body']
  elif kind in ('certificates','achievements'):body=document_bodies[kind+'-optional-full']
  elif kind=='achievements':body=document_bodies[kind+'-optional-full']
  else:body=html.tostring(card('Full '+kind),encoding='unicode')
  assert all(x in body for x in ('Extra narrative','Custom value','Gallery caption','Supporting report','Official link','youtube-nocookie.com')),(kind,body)
  for key,value in fixtures[kind].items():
   if key in ('end_date','currently_studying','currently_working'):continue
   expected=' '.join(html.fromstring(value).itertext()) if isinstance(value,str) and value.startswith('<') else value
   if isinstance(expected,list):assert all(x in body for x in expected),(kind,key)
   else:assert str(expected) in body,(kind,key,expected)
 edu=html.tostring(card('Full education'),encoding='unicode');exp=html.tostring(card('Full experience'),encoding='unicode')
 assert '2028 – Present' in edu and '2030' not in edu and '3.95 / 4.00' in edu
 assert 'Since 2027' in exp and '2028' not in exp
 assert '2027-01-01' in html.tostring(card('Full certificates'),encoding='unicode')
 certpath=base/'editor/certificates/optional-full.json';cert=json.loads(certpath.read_text());cert['does_not_expire']=True;dump(certpath,cert);build();_,docs=data();body=next(x['body'] for x in docs if x['id']=='certificates-optional-full')
 assert 'Does not expire' in body and '2029-01-01' not in body
 # Clearing every optional value removes all generated details, media and captions.
 for kind in fixtures:dump(base/'editor'/kind/'optional-full.json',dict(title='Full '+kind,published=True))
 build();stories,docs=data()
 assert not card('Full education').xpath('.//details|.//p|.//button')
 assert 'certificates-optional-full' not in {x['id'] for x in docs}
 assert stories['projects-optional-full']['body']==''
print('Passed: all optional sections populated/cleared, blank rich text and lists hidden, current study/work dates, CGPA scale, certificate validity, galleries, files, links and video')
