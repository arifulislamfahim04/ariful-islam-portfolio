"""Optional free-plan comments; no credentials or moderation authority in the CMS."""
from copy import deepcopy
from lxml import html
import json


def refine_comments(pages, *, root, esc, set_html):
    settings = json.loads((root/'editor/comments.json').read_text())
    articles = {}
    for path in (root/'editor/posts').glob('*.json'):
        value = json.loads(path.read_text())
        if value.get('published'):
            articles['posts-'+path.stem] = value.get('title') or 'Article'
    public = dict(enabled=bool(settings.get('enabled')), firebase=settings.get('firebase') or {}, articles=articles,
                  ownerEmail='arifulislamfahim04@gmail.com')
    # Keep comments separate from page content so an unpublished comment is never in Git.
    admin = deepcopy(pages['contact'])
    admin.find('body').set('data-page', 'comment-admin')
    for e in admin.xpath('//*[@aria-current="page"]'):
        e.attrib.pop('aria-current', None)
    admin.xpath('//title')[0].text = 'Comment moderation — Ariful Islam Fahim'
    for e in admin.xpath('//meta[@property="og:title" or @name="twitter:title"]'):
        e.set('content', 'Comment moderation — Ariful Islam Fahim')
    for e in admin.xpath('//link[@rel="canonical"]|//meta[@property="og:url"]'):
        e.getparent().remove(e)
    admin.find('head').append(html.fragment_fromstring('<meta name="robots" content="noindex">'))
    set_html(admin.xpath('//main')[0], '<section class="page-content shell comment-admin"><span class="section-label">OWNER TOOLS</span><h1>Comment moderation.</h1><p>Approve comments, remove conversations and manage article discussions.</p><div data-comments-admin></div></section>')
    pages['comment-admin'] = admin
    for name, page in pages.items():
        if name not in articles and name != 'comment-admin':
            continue
        article_settings = json.loads((root/'editor/posts'/(name.removeprefix('posts-')+'.json')).read_text()) if name in articles else {}
        if name in articles and article_settings.get('comments_enabled', True) is False:
            continue
        if name in articles and not settings.get('enabled'):
            continue
        if name in articles:
            panel = html.fragment_fromstring('<section class="article-comments" aria-labelledby="comments-title" data-comments-article="'+esc(name)+'"><h2 id="comments-title">Comments</h2><p>Read without an account. Sign in with Google to join the conversation. New comments and replies appear after approval.</p><div data-comments-public></div><noscript><p>JavaScript is needed to read and post comments.</p></noscript></section>')
            story = page.xpath('//main/article')[0]
            related = story.xpath('./section[contains(@class,"section")]')
            if related:related[0].addprevious(panel)
            else:story.append(panel)
        config = html.Element('script', type='application/json', id='comments-config')
        config.text = json.dumps(public, ensure_ascii=False).replace('<', '\\u003c')
        page.find('body').append(config)
        page.find('head').append(html.fragment_fromstring('<link rel="stylesheet" href="comments.css">'))
        page.find('body').append(html.fragment_fromstring('<script type="module" src="comments.js"></script>'))
