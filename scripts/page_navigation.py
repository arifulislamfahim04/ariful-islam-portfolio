"""Shared signature for genuine document navigations, independent of the CMS."""
from lxml import html
from html import escape
import json

def refine_navigation(pages, *, root):
 settings=json.loads((root/'editor/about-presentation.json').read_text())
 mark=str(settings.get('intro_wordmark') or 'ariful.').strip()[:24]
 enabled=settings.get('intro_animation',True)
 for page in pages.values():
  page.getroot().set('data-page-signature','true' if enabled else 'false')
  # Replace the former first-load intro; this signature is navigation-only.
  for old in page.xpath('//*[contains(concat(" ",@class," ")," wordmark-intro ")]'):
   old.getparent().remove(old)
  head=page.find('head')
  startup=html.Element('script',{'data-page-navigation':''})
  startup.text=(root/'scripts/page-navigation.js').read_text()
  head.append(startup)
  head.append(html.fragment_fromstring('<link rel="stylesheet" href="page-navigation.css">'))
  letters=''.join('<span class="signature-letter signature-letter-'+str(i)+'">'+escape(char)+'</span>' for i,char in enumerate(mark))
  page.find('body').append(html.fragment_fromstring('<div id="page-signature" aria-hidden="true" inert=""><div class="signature-panel"></div><div class="signature-wordmark" style="--signature-length:'+str(len(mark))+'">'+letters+'</div></div>'))

 css=(root/'scripts/page-navigation.css').read_text()
 for i,char in enumerate(mark):
  start=26+24*i/max(1,len(mark)-1);end=start+10
  bounce='-3px' if char=='.' else '0'
  css+=f"""
html.nav-signature .signature-letter-{i}{{view-transition-name:signature-letter-{i}}}
html.nav-signature::view-transition-group(signature-letter-{i}){{z-index:3}}
html.nav-signature::view-transition-old(signature-letter-{i}){{opacity:0}}
html.nav-signature::view-transition-new(signature-letter-{i}){{animation:signature-letter-{i} 600ms cubic-bezier(.22,1,.36,1) both}}
html.nav-signature-repeat::view-transition-new(signature-letter-{i}){{animation:signature-repeat-letter 360ms ease-out both}}
@keyframes signature-letter-{i}{{0%,{start:.2f}%{{opacity:0;transform:translateY(14px)}}{end:.2f}%{{opacity:1;transform:translateY({bounce})}}66%{{opacity:1;transform:translateY(0)}}88%,100%{{opacity:0;transform:translateY(-8px)}}}}
"""
 return css
