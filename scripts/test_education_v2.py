"""Education CMS lifecycle: no hardcoded degree, grade scale, optional facts or logo."""
from pathlib import Path
import json,tempfile,shutil,subprocess,sys
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 root=Path(t)/'repo';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():
  subprocess.run([sys.executable,str(root/'scripts/build_editor.py')],check=True,capture_output=True)
  return html.parse(str(root/'docs/about.html'))
 def save(path,data):path.write_text(json.dumps(data))
 a=build();b=a.xpath('//article[@data-entry-id="education-01"]')[0]
 assert b.xpath('.//p[@class="edu-duration" and text()="4-year programme"]')
 assert not b.xpath('.//p[@class="edu-date"]|.//span[@class="edu-timeline-label"]')
 assert b.xpath('.//div[@class="edu-progress-dates"]/span[text()="Dec 2026 · Expected"]')
 assert b.xpath('.//div[@class="edu-ring"]//span[@class="edu-grade-label" and text()="CGPA"]')
 assert b.xpath('.//span[@data-pulse="true"]')
 assert b.xpath('.//div[@aria-label="CGPA 3.90 of 4.00"]')
 assert b.xpath('.//span[@class="edu-status" and contains(.,"Results pending")]')
 assert len(a.xpath('//article[contains(@class,"education-featured")]'))==3
 for entry,value in [('02','4.92'),('03','4.67')]:
  school=a.xpath('//article[@data-entry-id="education-'+entry+'"]')[0]
  assert school.xpath('.//div[@aria-label="GPA '+value+' of 5.00"]')
  assert school.xpath('.//p[text()="Science group"]')
  assert school.xpath('.//span[@class="edu-status" and contains(.,"Completed")]')
  assert school.xpath('.//details//dt[text()="Group"]/following-sibling::dd[text()="Science"]')
  assert school.xpath('.//div[@class="edu-progress"]')
  assert school.xpath('.//p[@class="edu-duration" and text()="2-year programme"]')
  assert not school.xpath('.//p[@class="edu-date"]|.//span[@class="edu-timeline-label"]')
  assert school.xpath('.//span[@data-pulse="false"]')
 p=root/'editor/education/01.json';d=json.loads(p.read_text());d.update(title='A future degree',grade='4.20',grade_label='GPA',grade_scale='5.00',institution_logo='assets/loom-spools.jpg',focus='Quality science',location='Example location',coursework=['Materials','Testing'],thesis_title='A sample thesis',transcript_link='https://example.org/public-transcript',student_id='DEMO-ONLY',body='<p><strong>Formatted</strong> description</p><script>alert(1)</script>');save(p,d);a=build();b=a.xpath('//article[@data-entry-id="education-01"]')[0]
 assert b.xpath('.//h3[text()="A future degree"]')
 assert b.xpath('.//div[@aria-label="GPA 4.20 of 5.00"]')
 assert b.xpath('.//div[@class="edu-ring" and @data-ratio="0.8400000000000001"]') or abs(float(b.xpath('.//div[@class="edu-ring"]/@data-ratio')[0])-.84)<.0001
 assert b.xpath('.//img[@class="institution-logo"]')
 assert len(b.xpath('.//dl[@class="edu-detail-grid"]/div'))==7
 assert b.xpath('.//a[@href="https://example.org/public-transcript"]')
 assert b.xpath('.//strong[text()="Formatted"]') and not b.xpath('.//script')
 # Clearing optional values must remove details, ring, links and narrative, not empty labels.
 save(p,dict(title='Minimal qualification',published=True,order=1));a=build();b=a.xpath('//article[@data-entry-id="education-01"]')[0]
 assert not b.xpath('.//details|.//img|.//a|.//p|.//div[@class="edu-ring"]|.//div[@class="edu-progress"]')
 # Entry lifecycle remains a collection: add, reorder, remove and unpublish.
 q=root/'editor/education/new.json';save(q,dict(title='New education',published=True,order=-1,grade='4.00',grade_scale='5.00',grade_label='GPA'));a=build()
 assert a.xpath('//section[@id="education"]//article')[0].get('data-entry-id')=='education-new'
 q.unlink();a=build();assert not a.xpath('//article[@data-entry-id="education-new"]')
 print('Passed: real grade labels/scales, December/results pending, featured/compact, full optional grid, safe rich text, logo/transcript, clear/add/reorder/remove education.')
