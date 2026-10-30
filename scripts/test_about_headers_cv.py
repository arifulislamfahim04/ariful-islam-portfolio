"""Seven numbered headers, published counts and CV file/preview/metadata integration."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
from about_headers_cv import cv_metadata
metadata=cv_metadata(ROOT,'assets/ariful-islam-fahim-cv.pdf')
stamp=subprocess.run(['git','log','-1','--format=%cI','--','docs/assets/ariful-islam-fahim-cv.pdf'],cwd=ROOT,capture_output=True,text=True).stdout.strip()
if stamp:
 from datetime import datetime
 assert metadata.get('updated').strftime('%Y-%m')==datetime.fromisoformat(stamp).strftime('%Y-%m')
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(base/'docs/about.html'))
 def save(p,v):(base/p).write_text(json.dumps(v))
 a=build();headers=a.xpath('//header[contains(@class,"about-header-v2")]');assert len(headers)==7
 assert [h.xpath('string(.//span[@class="about-section-number"])') for h in headers]==[f'{n:02d}' for n in range(1,8)]
 assert all(h.xpath('.//span[@class="about-header-icon-tile"]') for h in headers)
 assert '5 awards' in a.xpath('string(//*[@id="recognition"]//span[@class="about-item-count"])')
 assert '1 sample' in a.xpath('string(//*[@id="recommendations"]//span[@class="about-item-count"])')
 assert not a.xpath('//*[@id="resume"]//span[@class="about-item-count"]')
 panel=a.xpath('//*[@id="resume"]')[0];links=panel.xpath('.//div[@class="cv-actions"]/a');assert len(links)==2 and links[0].get('href')==links[1].get('href');assert 'download' in links[0].attrib and links[1].get('target')=='_blank'
 assert panel.xpath('.//img[contains(@src,"assets/generated/cv-preview-")]')
 assert '2 pages' in panel.text_content() and '687 KB' in panel.text_content()
 # Change counts, optional subtitle and preview through their real CMS sources.
 save('editor/achievements/fixture.json',dict(title='Extra award',published=True))
 cfg=json.loads((base/'editor/about-presentation.json').read_text());cfg['header_subtitles']['education']='Optional education subtitle';cfg['cv_panel'].update(preview='assets/loom-spools.jpg',pitch='A changed CV pitch',view_online='Read online');save('editor/about-presentation.json',cfg)
 a=build();assert '6 awards' in a.xpath('string(//*[@id="recognition"]//span[@class="about-item-count"])');assert a.xpath('//p[@class="about-header-subtitle" and text()="Optional education subtitle"]');assert a.xpath('//*[@id="resume"]//img[@src="assets/loom-spools.jpg"]');assert a.xpath('//*[@id="resume"]//a[contains(.,"Read online")]')
 # Same bytes uploaded with a new filename change every CV action and still render metadata.
 shutil.copyfile(base/'docs/assets/ariful-islam-fahim-cv.pdf',base/'docs/assets/updated-cv.pdf');profile=json.loads((base/'editor/profile.json').read_text());profile['resume']='assets/updated-cv.pdf';save('editor/profile.json',profile);a=build();assert all('assets/updated-cv.pdf' in href for href in a.xpath('//*[@id="resume"]//a/@href'))
 # Remote files retain working links without invented page count/size/update date.
 profile['resume']='https://example.org/cv.pdf';save('editor/profile.json',profile);cfg['cv_panel']['preview']='';save('editor/about-presentation.json',cfg);a=build();assert a.xpath('string(//*[@class="cv-metadata"])')=='PDF';assert not a.xpath('//*[@id="resume"]//img');assert not a.xpath('//*[@id="resume"]//a[@download]')
 profile['resume']='';save('editor/profile.json',profile);a=build();assert not a.xpath('//*[@id="resume"]//a|//*[@id="resume"]//img|//*[@id="resume"]//p[@class="cv-metadata"]')
 print('Passed: 7 matching section numbers, published counts/sample honesty, optional subtitles, CV preview override, shared download/view source, real PDF count/size, file replacement, remote/empty fallbacks.')
