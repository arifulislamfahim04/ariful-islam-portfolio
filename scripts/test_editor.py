"""Exercise content lifecycle, asset replacement and safe rich-text rendering."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def dump(p,v):p.write_text(json.dumps(v))
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','__pycache__'))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 story=base/'editor/posts/lifecycle.json';draft=base/'editor/posts/draft.json'
 dump(story,dict(title='Lifecycle article',category='New category',published=True,order=0,body='<h2>A heading</h2><p>Text <strong>bold</strong></p><img src="assets/wool-weave.jpg" onerror="alert(1)"><script>alert(2)</script>',gallery=[dict(image='assets/loom-spools.jpg',caption='A caption')],video_url='https://youtu.be/dQw4w9WgXcQ'))
 dump(draft,dict(title='Unpublished private-ish draft',published=False,body='Not for website'))
 p=base/'editor/profile.json';profile=json.loads(p.read_text());profile.update(photo='assets/loom-spools.jpg',resume='assets/ariful-islam-fahim-cv.pdf',email='example@example.com',name='Updated name');dump(p,profile)
 cert=base/'editor/certificates/new.json';dump(cert,dict(title='New certificate',published=True,file='assets/ariful-islam-fahim-cv.pdf'))
 build();published=(base/'docs/posts-lifecycle.html').read_text();data=(base/'docs/content.js').read_text();home=(base/'docs/index.html').read_text()
 assert '<strong>bold</strong>' in published and 'A caption' in published and 'youtube-nocookie.com/embed/dQw4w9WgXcQ' in published
 assert 'onerror=' not in data and 'alert(2)' not in data and 'Unpublished private-ish draft' not in data
 assert 'hero-card-photo' in home and 'assets/loom-spools.jpg' in home and 'Updated name' in home and 'example@example.com' in home
 assert not (base/'docs/posts-draft.html').exists()
 assert 'certificate-pdf' in data and 'New certificate' in data
 story.unlink();build();assert not (base/'docs/posts-lifecycle.html').exists()
 # Empty repeatable collections must not break the page or its JavaScript.
 for folder in ('posts','projects','certificates','achievements','education','experience','workshops'):
  for f in (base/'editor'/folder).glob('*.json'):f.unlink()
 build();assert 'No entries published yet.' in (base/'docs/about.html').read_text()
 assert 'award-track' not in (base/'docs/about.html').read_text()
print('Passed: add/edit/remove, drafts, gallery, video, certificate PDF, portrait replacement, contact updates, empty sections and unsafe HTML')
