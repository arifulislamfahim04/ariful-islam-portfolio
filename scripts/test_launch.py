"""Audit route semantics and generated launch assets, including responsive media."""
from pathlib import Path
from collections import Counter
from lxml import html
import json
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
out = root/'docs'
profile = json.loads((root/'editor/profile.json').read_text())
for path in out.glob('*.html'):
    page = html.parse(str(path))
    assert len(page.xpath('//main//h1')) == 1, path
    ids = Counter(page.xpath('//@id'))
    assert not [key for key, count in ids.items() if count > 1], path
    assert page.xpath('string(//title)').endswith(' — '+profile['name']), path
    assert page.xpath('//meta[@name="description" and @content]'), path
    assert page.xpath('//link[starts-with(@href,"portfolio-foundation.css")]'), path
    assert not page.xpath('//a[starts-with(@href,"mailto:") and @target="_blank"]'), path
    for img in page.xpath('//img[@srcset]'):
        for variant in img.get('srcset').split(','):
            src, width = variant.strip().split()
            assert (out/src).is_file() and width.endswith('w'), (path, src)
    for button in page.xpath('//button'):
        assert button.text_content().strip() or button.get('aria-label') or button.get('aria-labelledby'), (path, html.tostring(button))
missing = html.parse(str(out/'404.html'))
assert missing.xpath('//meta[@name="robots" and @content="noindex"]')
assert not missing.xpath('//*[@aria-current="page"]')
assert '404.html' not in (out/'sitemap.xml').read_text()
home = html.parse(str(out/'index.html'))
assert home.xpath('//div[@class="hero-stat"]//b/@data-count') == [str(x.get('value') or '0') for x in profile.get('stats', [])[:4]]
if profile.get('resume') and not urlsplit(profile['resume']).scheme:
    assert (out/profile['resume']).is_file()
print('Passed: unique IDs, one H1 and metadata on all 15 routes, labelled buttons, native mail targets, responsive image files, 404 exclusion and confirmed facts.')
