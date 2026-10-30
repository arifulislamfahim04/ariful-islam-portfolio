"""One CMS navigation source for header, menu, dock and footer."""
import json
DEFAULT_NAV=[('index','Home','home'),('about','About','about'),('projects','Projects','projects'),('gallery','Gallery','gallery'),('blogs','Blogs','blogs'),('contact','Contact','contact')]
def read_navigation(root):
 config=json.loads((root/'editor/site.json').read_text())
 if 'navigation' not in config:return list(DEFAULT_NAV)
 icons=set(json.loads((root/'vendor/home-icons/sources.json').read_text()))
 allowed={p:(label,icon) for p,label,icon in DEFAULT_NAV};result=[];seen=set()
 for row in config.get('navigation') or []:
  page=row.get('page')
  if not row.get('published',True) or page not in allowed or page in seen:continue
  seen.add(page);default_label,default_icon=allowed[page];result.append((page,str(row.get('label') or default_label),str(row.get('icon')) if row.get('icon') in icons else default_icon))
 return result
