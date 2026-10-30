# Edit your portfolio without code

Open **https://app.pagescms.org/** and sign in with your GitHub account.
Enable Pages CMS for **`ariful-islam-portfolio` (keep your older repository selected too if you still edit it)**, then select that repository and its `main` branch.
Your editor reads the `.pages.yml` configuration automatically.

## Daily editing

- **Profile, résumé & homepage**: choose your portrait, replace your résumé PDF, edit your introduction, contact details and statistics. A portrait replaces the decorative monogram. Leave it empty to retain the original textile design.
- **Biography, skills & references**: update your biography, repeating information fields, languages, skills and recommendations. Upload a transcript when available.
- **Blogs & articles / Projects**: click New, enter a title and summary, then write in the visual editor. Use headings, lists and image uploads between paragraphs. Add captions through Extra pictures. You can paste common formatting from Word; complex Word page layouts may need adjustment.
- **Education / Experience / Certificates / Achievements / Workshops**: click New for every new entry. There is no fixed number of entries. Upload a certificate PDF or picture to let visitors view it.
- **Show on website**: turn OFF to save an unpublished entry; ON to publish. Lower display-order numbers appear first.
- **Pictures, résumé & certificates**: organize media in folders if useful. Upload a file, then select it in the appropriate content field. You do not need fixed filenames. Uploading an image alone does not select it as your profile photo.

Save the entry. GitHub Actions builds and publishes the website automatically, usually within a few minutes. Check **Actions → Publish portfolio content** if an update has not appeared. A failed build keeps the last successful deployment live.

Each published blog/project has a shareable page URL as well as a reading dialog. Changing its filename changes its URL. Updating only its title does not require renaming it.

## Important practical details

The public site and repository are public. Unpublished entries are omitted from the website, but their text and uploaded files remain visible in the public GitHub repository. Do not use this as private storage for confidential drafts or documents. Keep certificate files suitable for public viewing.

Use YouTube links for large videos to keep repository storage manageable. Small MP4/WebM uploads also work. There is no paid domain, database, hosting subscription, or API key required by this setup.

GitHub history keeps previous versions of saved files. The content is stored in standard JSON and media files, so it can be moved if the editor changes in the future. A deletion remains in repository history; deleting a file does not erase all historical copies.

## For future maintainers

`editor/` is the content source. `templates/` retains the existing design. `docs/assets/` contains media. `.pages.yml` configures Pages CMS. `scripts/build_editor.py` builds the website and `.github/workflows/publish.yml` publishes it.

Run `python -m pip install -r requirements.txt`, `python scripts/build_editor.py`, then `python scripts/check_site.py`. The older `build_portfolio.py`, `content/` and `dist/` are retained for historical reference; do not use them for routine publication because they predate the editor.

GitHub Settings → Pages must use **GitHub Actions** as the source. Never put a GitHub token in frontend HTML or JavaScript. Pages CMS performs authenticated edits through its GitHub App.

## Optional information in every entry

The extra fields are optional. Leave them blank when they do not apply. Empty fields, untouched rich-text boxes, blank gallery items and empty document/link rows do not produce public labels, gaps or buttons. Only the entry title is required; Show on website controls publication.

- **Education:** qualification, department, specialization, location, separate start/end dates, currently studying, CGPA/GPA/classification and scale, thesis, supervisor and coursework.
- **Experience:** employment type, location, separate dates, currently working, organization website, responsibilities, achievements and skills.
- **Awards:** category, individual/team recognition, reason/criteria, related work and official verification link.
- **Certificates:** issue/expiry dates, Does not expire, credential ID, verification link and skills.
- **Projects:** status, dates, your role, collaborators, objectives, methods, results and report.
- **Blogs/articles:** author, tags, last updated date and sources/references.
- **Workshops:** duration, location/online, your role and learning outcomes.
- **All entries:** Additional details, Other facts (your own labels and values), Pictures & captions, video link, Supporting documents and Related links.
- **Profile:** additional social/professional links.

Cards stay concise. Education, experience and workshop extras open under **More details**. Award and certificate extras open in **View details / certificate**. Blog/project details appear in their reading view and full article page.

If you enter separate start/end dates, they replace the older Date / period display. Currently studying/working shows Present instead of an end date. A separate CGPA/result and scale replace the older Result / badge; that field remains available for existing entries. Does not expire takes precedence over an expiry date. The shorter card title remains independent from the optional qualification field.

For pictures and documents, upload/select the file inside its field in Pages CMS, then save the entry. Uploading to media storage alone does not place the file on a page. Remove a picture selection or clear an optional field and save to remove it from the public display. This does not erase its file or GitHub history.

There is no need to fill every form field. Add only the information you want visitors to see. Homepage statistics and the résumé PDF remain separately editable; adding education does not rewrite those automatically.

## New homepage and Moments gallery

**Homepage design & identity tag** controls the logo, preferred name, headline, introduction, tag label/tagline, gallery headings and slideshow settings. Your **full name and portrait** remain in Profile, résumé & homepage. Replace the portrait there at any time; the tag frame uses the new image automatically. The card responds to dragging (on phones, start at its grip) and returns gently to its resting position. Arrow keys move the focused grip; Escape resets it.

The clock uses Dhaka time in 12-hour AM/PM format. Location comes from your profile. The right rail contains navigation, theme and back-to-top. On phones, tap the grid button to expand navigation. Back-to-top appears after scrolling.

Use **Gallery · moments & photo stories → New** for each photo:

1. Enter a title and upload/select a picture. These are required.
2. Optionally add a caption, category, date, location, longer story, credit and source link. Blank details stay hidden.
3. Choose Landscape, Portrait or Square framing. The original uploaded file is retained.
4. Enable **Show in homepage preview** for featured photos. All published photos appear on the Gallery page, including unfeatured photos.
5. Save with **Show on website** enabled to publish. Turn it off to remove the entry from both views.

The four initial stock photographs are clearly marked **Sample image**. They demonstrate the layout and do not claim to depict your university, achievements or personal experiences. Replace them with your own photos, update the captions and credits, then turn off **This is a sample image**. You can also delete the sample entries.

The homepage preview swipes on phones and supports previous/next and play/pause buttons. It pauses during interaction and when offscreen. Reduced-motion preferences disable autoplay by default. Clicking a picture opens its story; **Explore the gallery** opens the complete gallery. Visitors can search and filter categories there. If there are no published featured photos, the homepage gallery preview disappears automatically.
