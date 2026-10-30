"""Shared portfolio foundation, contact clarity and launch essentials."""
from copy import deepcopy
import json
from urllib.parse import urlsplit
import hashlib
from PIL import Image, ImageOps
from lxml import html


def refine_launch(pages, *, profile, root, esc, set_html):
    for name, page in pages.items():
        head = page.find('head')
        head.append(html.fragment_fromstring('<link rel="stylesheet" href="portfolio-foundation.css">'))
        for old in page.xpath('//link[@rel="preload" and contains(@href,"editorial-fonts")]'):
            old.getparent().remove(old)
        head.append(html.fragment_fromstring('<link rel="preload" href="assets/hero-fonts/poppins-400.woff" as="font" type="font/woff" crossorigin="anonymous">'))
        for meta in page.xpath('//meta[@name="theme-color"]'):
            meta.set('content', '#f6f7f2')
        for a in page.xpath('//a[starts-with(@href,"mailto:")]'):
            a.attrib.pop('target', None)
        for img in page.xpath('//img[@src]'):
            source = img.get('src', '')
            if urlsplit(source).scheme or not source.startswith('assets/'):
                continue
            path = (root/'docs'/source).resolve()
            if not path.is_relative_to((root/'docs').resolve()) or not path.is_file() or path.suffix.lower() not in ('.jpg', '.jpeg', '.png') or path.stat().st_size < 150000:
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
            variants = []
            with Image.open(path) as original:
                original = ImageOps.exif_transpose(original).convert('RGB')
                for width in sorted({min(w, original.width) for w in (480, 960, 1440)}):
                    target = root/'docs/assets/generated'/f'{digest}-{width}.webp'
                    target.parent.mkdir(exist_ok=True)
                    if not target.exists():
                        resized = original.resize((width, round(original.height*width/original.width)), Image.Resampling.LANCZOS)
                        resized.save(target, 'WEBP', quality=82, method=6)
                    variants.append(f'assets/generated/{target.name} {width}w')
            img.set('srcset', ', '.join(variants))
            img.set('sizes', '(max-width:960px) 100vw, 900px' if img.xpath('ancestor::*[contains(@class,"story-page")]') else '(max-width:600px) 100vw, (max-width:900px) 50vw, 33vw')
        for a in page.xpath('//a[@href]'):
            if a.get('href') == profile.get('resume') and not a.get('href', '').startswith(('http:', 'https:')):
                if 'download' in a.text_content().lower():
                    a.set('download', '')
    contact = pages['contact']
    form = contact.xpath('//form[@id="contact-form"]')[0]
    if form.get('data-provider') == 'Email app':
        button = form.xpath('.//button[@type="submit"]')[0]
        set_html(button, 'Prepare email draft <svg class="icon" viewBox="0 0 256 256" aria-hidden="true"><use href="#i-arrow"></use></svg>')
        button.addnext(html.fragment_fromstring('<button type="submit" class="button secondary" data-compose="gmail">Prepare in Gmail</button>'))
        for note in form.xpath('.//p[@class="form-note"]'):
            note.text = 'Prepares a draft; nothing is sent here. Use your configured email app or Gmail, review the draft, then send. No email app? Copy my address from the contact card.'
    # Reuse the finished shared chrome and scripts, keeping 404 out of the menu.
    missing = deepcopy(contact)
    missing.find('body').set('data-page', '404')
    site_url = json.loads((root/'editor/site.json').read_text()).get('site_url', '')
    prefix = urlsplit(site_url).path.rstrip('/')+'/'
    base = html.Element('base', href='/')
    missing.find('head').insert(0, base)
    init = html.Element('script')
    init.text = 'if(location.hostname.endsWith("github.io"))document.querySelector("base").href='+json.dumps(prefix)+';'
    missing.find('head').insert(1, init)
    for node in missing.xpath('//*[@aria-current="page"]'):
        node.attrib.pop('aria-current', None)
    for node in missing.xpath('//*[@data-dock-page]'):
        node.set('class', node.get('class', '').replace(' active', ''))
    missing.xpath('//title')[0].text = 'Page not found — ' + profile['name']
    for node in missing.xpath('//meta[@property="og:title" or @name="twitter:title"]'):
        node.set('content', 'Page not found — ' + profile['name'])
    for node in missing.xpath('//meta[@name="description" or @property="og:description" or @name="twitter:description"]'):
        node.set('content', 'This page could not be found. Return to Ariful’s portfolio.')
    for node in missing.xpath('//link[@rel="canonical"]|//meta[@property="og:url"]'):
        node.getparent().remove(node)
    missing.find('head').append(html.fragment_fromstring('<meta name="robots" content="noindex">'))
    set_html(missing.xpath('//main')[0], '<section class="page-content shell not-found"><span class="section-label">404 · A MISSING THREAD</span><h1>Let’s find your way.</h1><p>This page may have moved, or the address may be incomplete.</p><div class="not-found-actions"><a class="button primary" href="index.html">Back to Home</a><a class="button secondary" href="projects.html">Explore projects</a></div></section>')
    pages['404'] = missing
    (root/'docs/assets/home-favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#78cc6d"/><path d="M38 22v22h-6v-3c-2 3-5 4-8 3-5-1-8-5-8-11s4-12 10-12c3 0 5 1 6 3v-2zm-11 5c-4 0-5 3-5 6s1 6 5 6 5-3 5-6-1-6-5-6Z" fill="#18251e"/><circle cx="47" cy="41" r="4" fill="#18251e"/></svg>')
