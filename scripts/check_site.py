"""Check generated pages, local media, story targets and document references."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from lxml import html
import json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs'
raw=(OUT/'content.js').read_text();details=json.loads(raw.split('window.PORTFOLIO_DETAILS=')[1].split(';\nwindow.PORTFOLIO_DOCUMENTS=')[0]);documents=json.loads(raw.split('window.PORTFOLIO_DOCUMENTS=')[1].split(';\nwindow.PORTFOLIO_PROFILE=')[0]);ids={d['id'] for d in documents};errors=[];count=0
for p in OUT.glob('*.html'):
 d=html.parse(str(p))
 for e in d.xpath('//*[@href or @src or @data-project or @data-document]'):
  if e.tag=='base':continue
  if e.get('data-project') and e.get('data-project') not in details:errors.append(f'{p.name}: missing story {e.get("data-project")}')
  if e.get('data-document') and e.get('data-document') not in ids:errors.append(f'{p.name}: missing document {e.get("data-document")}')
  for attr in ('href','src'):
   value=e.get(attr,'');u=urlsplit(value)
   if not value or value.startswith('#') or u.scheme or u.netloc:continue
   dest=(p.parent/unquote(u.path)).resolve()
   if not dest.is_relative_to(OUT.resolve()) or not dest.exists():errors.append(f'{p.name}: missing {value}')
   count+=1
for item in [*details.values(),*documents]:
 d=html.fragment_fromstring('<div>'+item.get('body','')+'</div>')
 for e in d.xpath('.//*[@src or @href]'):
  for attr in ('href','src'):
   value=e.get(attr,'');u=urlsplit(value)
   if value and not u.scheme and not u.netloc and not value.startswith('#') and not (OUT/unquote(u.path)).exists():errors.append(f'Reader media missing: {value}')
assert not errors,'\n'.join(errors)
print(f'Checked {len(list(OUT.glob("*.html")))} pages, {count} local references, {len(details)} stories and {len(ids)} documents')
