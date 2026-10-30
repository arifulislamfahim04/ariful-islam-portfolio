"""Editorial redesign: CMS optional fields, privacy and metadata integration."""
import json,shutil,subprocess,sys,tempfile,hashlib
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','.openai','__pycache__'))
 def save(path,value):(base/path).write_text(json.dumps(value))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def doc(name='index'):return html.parse(str(base/'docs'/(name+'.html')))
 build();a=doc('about');raw=(base/'docs/content.js').read_text();assert not a.xpath('//a[starts-with(@href,"mailto:") and ancestor::*[contains(@class,"reference-grid")]]');assert '"id": "transcript"' not in raw;assert not a.xpath('//button[@data-document="transcript"]');assert len(a.xpath('//div[@class="awards-carousel"]/article'))==5
 assert not doc().xpath('//a[@aria-label="Facebook"]');p=json.loads((base/'editor/profile.json').read_text());p.update(facebook='https://www.facebook.com/example',location='A new location');save('editor/profile.json',p)
 about=json.loads((base/'editor/about.json').read_text());about['references']=[dict(title='Example referee',body='<p>Example referee <a href="mailto:referee@example.org">referee@example.org</a></p>',show_publicly=True),dict(title='Private example',body='<p>private-example@example.org</p>',show_publicly=False)];about['transcript_public']=True;save('editor/about.json',about)
 home=json.loads((base/'editor/homepage.json').read_text());home.update(gallery_heading='New gallery heading',typewriter_phrases=['Custom phrase'],secondary_button_text='Explore my work');save('editor/homepage.json',home)
 meta=json.loads((base/'editor/pages.json').read_text());meta['gallery'].update(heading='Editable gallery title',description='Unique editable description');save('editor/pages.json',meta)
 ui=json.loads((base/'editor/interface.json').read_text());ui[hashlib.sha1(b'View projects').hexdigest()[:10]]='Explore my work';save('editor/interface.json',ui)
 build();assert doc().xpath('//a[@aria-label="Facebook"]') and all(x=='_blank' for x in doc().xpath('//a[@aria-label="Facebook"]/@target'));assert 'Explore my work' in doc().xpath('string(//main)');assert doc('gallery').xpath('//h1/text()')==['Editable gallery title'];assert 'referee@example.org' in (base/'docs/about.html').read_text();assert 'private-example@example.org' not in (base/'docs/about.html').read_text();assert doc('about').xpath('//button[@data-document="transcript"]');assert 'A%20new%20location' in (base/'docs/contact.html').read_text();assert len(doc('contact').xpath('//iframe'))==1;assert not doc('contact').xpath('//details[contains(@class,"map-panel")]')
 # Website links, reports, tools and entry images remain native CMS content.
 e=json.loads((base/'editor/education/01.json').read_text());e.update(website='https://example.org',file='assets/ariful-islam-fahim-cv.pdf');save('editor/education/01.json',e)
 v=json.loads((base/'editor/projects/smart.json').read_text());v.update(tools=['Tool one','Tool two'],duration='Six weeks',seo_title='Custom study',seo_description='A unique project description');save('editor/projects/smart.json',v)
 site=json.loads((base/'editor/site.json').read_text());site.update(form_provider='Formspree',formspree_endpoint='https://formspree.io/f/example');save('editor/site.json',site)
 build();assert doc('about').xpath('//p[@class="institution"]/a[@href="https://example.org"]/@target')==['_blank'];assert doc('about').xpath('//article[@data-entry-id="education-01"]//a[@href="assets/ariful-islam-fahim-cv.pdf"]');assert 'Tool one, Tool two' in doc('projects-smart').xpath('string(//main)');assert doc('projects-smart').xpath('//title/text()')==['Custom study — '+p['name']];assert doc('contact').xpath('//form/@data-provider')==['Formspree']
 for name in ['index','about','gallery','projects','blogs','contact','projects-smart','posts-note1']:
  d=doc(name);assert len(d.xpath('//h1'))==1;assert len(d.xpath('//meta[@name="description"]'))==1;assert d.xpath('//meta[@property="og:image"]');assert d.xpath('//link[@rel="canonical"]');ids=d.xpath('//*[@id]/@id');assert len(ids)==len(set(ids)),name
 # All inherited data remains; only unpublished records are removed from generated output.
 for f in (base/'editor/updates').glob('*.json'):f.unlink()
 build();assert not doc().xpath('//div[@class="news-ticker"]');assert 'No updates here yet.' in doc().xpath('string(//main)')
 assert (base/'docs/sitemap.xml').exists();assert doc().xpath('//script[@type="application/ld+json"]')
print('Passed: privacy opt-ins, CMS links/headings/copy/SEO, website links, certificate controls, projects, form config and empty updates')
