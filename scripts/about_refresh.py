"""About adopts the approved homepage chrome without changing other routes."""
from copy import deepcopy
from lxml import html, etree
from pathlib import Path
import re,json

def refresh_about(d,home,settings,*,root,esc,url,set_html):
 body=d.find('body');body.set('data-hero-refresh','true');body.set('data-about-refresh','true')
 for query in ['//header[contains(@class,"site-header")]','//footer']:
  old=d.xpath(query)[0];old.getparent().replace(old,deepcopy(home.xpath(query)[0]))
 for old in d.xpath('//*[@id="back-top"]|//aside[contains(@class,"hero-rail")]'):old.getparent().remove(old)
 rail=deepcopy(home.xpath('//aside[@class="hero-rail"]')[0]);body.append(rail)
 for nav in [rail.xpath('.//nav')[0],d.xpath('//*[@id="site-menu"]//nav')[0]]:
  if nav is not rail.xpath('.//nav')[0]:set_html(nav,html.tostring(rail.xpath('.//nav')[0],encoding='unicode').split('>',1)[1].rsplit('</nav>',1)[0])
  for a in nav.xpath('.//a'):
   a.attrib.pop('aria-current',None)
   if a.get('href')=='about.html':a.set('aria-current','page')
 for logo in d.xpath('//header//a[@class="logo"]'):logo.set('aria-label','Home')
 overrides={v.get('key'):v.get('image') for v in settings.get('icon_overrides',[]) if isinstance(v,dict)}
 symbols={e.get('id'):e for e in d.xpath('//symbol')}
 for svg in d.xpath('//svg[contains(concat(" ",@class," ")," icon ")]'):
  uses=svg.xpath('./use')
  if not uses:continue
  key=(uses[0].get('href') or '').removeprefix('#i-');custom=str(overrides.get(key) or '')
  if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:
   replacement=html.fragment_fromstring('<span class="icon custom-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>');svg.getparent().replace(svg,replacement);continue
  for use in uses:
   symbol=symbols.get((use.get('href') or '').lstrip('#'))
   if symbol is not None:
    svg.remove(use)
    for shape in symbol:svg.append(deepcopy(shape))
 # Keep every collection and all optional fields; improve section orientation.
 icons={'education':'book','experience':'projects','skills':'research','recognition':'award','certificates':'certificate','recommendations':'quote','resume':'download'}
 for section in d.xpath('//main//section[@id]'):
  header=section.xpath('./header')
  if header:
   key=icons.get(section.get('id'),'about');symbol=symbols.get('i-'+key)
   custom=str(overrides.get(key) or '')
   if re.fullmatch(r'assets/[A-Za-z0-9 _./-]+\.svg',custom) and '..' not in custom:
    header[0].insert(0,html.fragment_fromstring('<span class="icon custom-icon about-section-icon" aria-hidden="true" style="--icon-source:url(\''+esc(custom)+'\')"></span>'));continue
   if symbol is not None:
    badge=etree.Element('svg',{'class':'icon about-section-icon','viewBox':'0 0 256 256','fill':'currentColor','aria-hidden':'true'})
    for shape in symbol:badge.append(deepcopy(shape))
    header[0].insert(0,badge)
 # Body formatting from Pages CMS must render as formatting, including emphasis.
 for a in d.xpath('//main//a[contains(@class,"text-link")]'):
  a.set('class',a.get('class')+' about-action')
 head=d.find('head')
 for e in head.xpath('./link[@rel="preload" and contains(@href,"editorial-fonts")]'):head.remove(e)
 for e in home.xpath('//head/link[contains(@href,"hero-fonts") or @href="hero-refresh.css"]'):head.append(deepcopy(e))
 head.append(html.fragment_fromstring('<link rel="stylesheet" href="about-refresh.css">'))
 body.append(html.fragment_fromstring('<script src="about-refresh.js" defer></script>'))
