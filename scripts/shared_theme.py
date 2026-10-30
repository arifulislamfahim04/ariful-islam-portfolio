"""One accessible control and runtime, shared by every generated page."""
from lxml import html

def refine_theme(pages, *, root):
 icon='<svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle class="theme-sun" cx="12" cy="12" r="4"/><g class="theme-rays"><path d="M12 1v2m0 18v2M1 12h2m18 0h2M4.2 4.2l1.4 1.4m12.8 12.8 1.4 1.4M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></g><path class="theme-moon" d="M20.5 13.4A8.5 8.5 0 0 1 10.6 3.5a8.5 8.5 0 1 0 9.9 9.9Z"/></svg>'
 for page in pages.values():
  for old in page.xpath('//label[contains(@class,"hero-theme-switch")]|//button[contains(@class,"theme-toggle")]'):
   button=html.fragment_fromstring('<button type="button" class="hero-theme-switch" data-theme-toggle="" aria-label="Switch to dark mode" aria-pressed="false">'+icon+'<span data-theme-label="" aria-hidden="true">Switch to dark mode</span></button>')
   old.getparent().replace(old,button)
  head=page.find('head')
  head.append(html.fragment_fromstring('<link rel="stylesheet" href="theme.css">'))
  page.find('body').append(html.fragment_fromstring('<script src="theme.js" defer></script>'))
