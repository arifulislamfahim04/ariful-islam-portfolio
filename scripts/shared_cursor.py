"""Apply the existing optional cursor setting to every page."""
import json
from lxml import html

def refine_cursor(pages,*,root):
 enabled=json.loads((root/'editor/about-presentation.json').read_text()).get('cursor_follower',True)
 for page in pages.values():
  page.getroot().set('data-custom-cursor','true' if enabled else 'false')
  for old in page.xpath('//*[contains(concat(" ",@class," ")," mint-cursor ") or @class="cursor-dot" or @class="cursor-ring" or @class="cursor-label"]'):
   old.getparent().remove(old)
  page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="shared-cursor.css">'))
  page.find('body').append(html.fragment_fromstring('<script src="shared-cursor.js" defer></script>'))
