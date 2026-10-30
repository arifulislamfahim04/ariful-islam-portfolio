# Pages CMS changes — redesign v2

Review branch: `portfolio-redesign-v2`. Main and its CMS configuration are unchanged. Select this review branch in Pages CMS to inspect the new forms.

The separate Sites review website is a generated snapshot. Pages CMS remains connected to the existing GitHub repository. After an approved merge, the existing main-only workflow builds GitHub Pages. CMS edits do not automatically regenerate this separate Sites preview.

## Where to edit

| Change | CMS section → field |
|---|---|
| Name, portrait, contacts, location, CV | Profile, résumé & homepage → corresponding field |
| Hero phrases, chips and home previews | Homepage · hero, previews & highlights |
| Photos, captions, stories, order, featured flag | Gallery · moments & photo stories |
| Highlights ticker and detail entries | Homepage news & updates |
| Biography, skills, recommendations, privacy toggles | Biography, skills & references |
| Page headings, introductions and SEO | Page headings & SEO → page |
| Footer, author bio, form delivery and category labels | Site settings · footer, forms & labels |
| Buttons, forms and static section wording | Interface wording · buttons, forms & section labels |

## Every configuration change

### Homepage · hero, previews & highlights

- `typewriter_phrases` — Hero typewriter phrases (string). Add, remove or reorder these phrases. Each types and deletes in turn.
- `status_chips` — Profile card status chips (string). Short labels below your name. Add or remove as needed.
- `ticker_label` — Highlights ticker label (string). Leave empty to omit optional text.
- `projects_heading` — Featured projects heading (string). Leave empty to omit optional text.
- `notes_heading` — Latest notes heading (string). Leave empty to omit optional text.
- `about_teaser_heading` — About teaser heading (string). Leave empty to omit optional text.
- `about_teaser` — Short about teaser (rich-text). Leave empty to omit optional text.
- `closing_heading` — Closing contact heading (string). Leave empty to omit optional text.
- Existing `headline`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `tagline`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `tag_label`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `background_image`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `background_image_small`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `roles`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.
- Existing `gallery_mode`: label/help updated. Previous design setting, retained for rollback. The new design uses Typewriter phrases, Status chips and the shared page settings.

### Biography, skills & references

- `transcript_public` — Show transcript publicly (boolean). Off by default. Enable only when you want your transcript visible.
- `references_notice` — Private references notice (string). Shown when no references are marked public.
- `image_alt` — About photo description (string). Describe the secondary photo for visitors who cannot see it.
- `image_caption` — About photo caption (string). The secondary photo is selected in Profile → Secondary image.
- Existing `references`: added per-reference `show_publicly` (default off).

### Blogs & articles

- `featured` — Feature on homepage (boolean). Enabled by default for existing entries; turn off to hide from the home preview.
- `seo_title` — Search / sharing title (string). Optional override. Your name is appended automatically.
- `seo_description` — Search / sharing description (text). Optional short description for search engines and social sharing.
- `social_image` — Sharing image (image). Optional social preview image.
- `share_enabled` — Show share button (boolean). Enabled by default; turn off to hide the share button.

### Projects

- `featured` — Feature on homepage (boolean). Enabled by default for existing entries; turn off to hide from the home preview.
- `seo_title` — Search / sharing title (string). Optional override. Your name is appended automatically.
- `seo_description` — Search / sharing description (text). Optional short description for search engines and social sharing.
- `social_image` — Sharing image (image). Optional social preview image.
- `share_enabled` — Show share button (boolean). Enabled by default; turn off to hide the share button.
- `tools` — Tools used (string). Optional tools or software used in this project.
- `duration` — Project duration (string). Optional readable duration, for example 6 weeks.

### Education

- `website` — Institution / organization website (string). Paste the official website URL. The institution name becomes a link in a new tab.

### Experience

- `website` — Institution / organization website (string). Paste the official website URL. The institution name becomes a link in a new tab.

### Certificates

- `website` — Institution / organization website (string). Paste the official website URL. The institution name becomes a link in a new tab.

### Achievements & awards

- `website` — Institution / organization website (string). Paste the official website URL. The institution name becomes a link in a new tab.

### Workshops & seminars

- `website` — Institution / organization website (string). Paste the official website URL. The institution name becomes a link in a new tab.

### Site settings · footer, forms & labels

New CMS file: `editor/site.json`.

- `site_name` — Site Name (string). Editable site-wide content.
- `description` — Description (string). Editable site-wide content.
- `site_url` — Site Url (string). Editable site-wide content.
- `social_image` — Social Image (image). Editable site-wide content.
- `footer_text` — Footer Text (string). Editable site-wide content.
- `footer_mark` — Footer Mark (string). Editable site-wide content.
- `author_bio` — Author Bio (string). Editable site-wide content.
- `form_provider` — Contact form delivery (select). Email app works immediately. Formspree/Web3Forms need your own form service details.
- `formspree_endpoint` — Formspree form endpoint (string). Public form identifiers only. Never enter a private API secret.
- `web3forms_access_key` — Web3Forms public access key (string). Public form identifiers only. Never enter a private API secret.
- `form_note` — Form Note (string). Editable site-wide content.
- `project_categories` — Project Categories (object). Edit the labels shown on the site.
- `project_categories.textile` — Textile (string). 
- `project_categories.research` — Research (string). 
- `project_categories.industry` — Industry (string). 
- `project_categories.creator` — Creator (string). 
- `about_index` — About Index (object). Edit the labels shown on the site.
- `about_index.education` — Education (string). 
- `about_index.experience` — Experience (string). 
- `about_index.skills` — Skills (string). 
- `about_index.recognition` — Recognition (string). 
- `about_index.certificates` — Certificates (string). 
- `about_index.recommendations` — Recommendations (string). 
- `about_index.resume` — Resume (string). 

### Page headings & SEO

New CMS file: `editor/pages.json`.

- `index` — Index (object). Heading and sharing settings for this page.
- `index.title` — Title (string). 
- `index.eyebrow` — Eyebrow (string). 
- `index.heading` — Heading (string). 
- `index.intro` — Intro (text). 
- `index.description` — Description (text). 
- `index.social_image` — Social Image (image). 
- `about` — About (object). Heading and sharing settings for this page.
- `about.title` — Title (string). 
- `about.eyebrow` — Eyebrow (string). 
- `about.heading` — Heading (string). 
- `about.intro` — Intro (text). 
- `about.description` — Description (text). 
- `about.social_image` — Social Image (image). 
- `projects` — Projects (object). Heading and sharing settings for this page.
- `projects.title` — Title (string). 
- `projects.eyebrow` — Eyebrow (string). 
- `projects.heading` — Heading (string). 
- `projects.intro` — Intro (text). 
- `projects.description` — Description (text). 
- `projects.social_image` — Social Image (image). 
- `gallery` — Gallery (object). Heading and sharing settings for this page.
- `gallery.title` — Title (string). 
- `gallery.eyebrow` — Eyebrow (string). 
- `gallery.heading` — Heading (string). 
- `gallery.intro` — Intro (text). 
- `gallery.description` — Description (text). 
- `gallery.social_image` — Social Image (image). 
- `blogs` — Blogs (object). Heading and sharing settings for this page.
- `blogs.title` — Title (string). 
- `blogs.eyebrow` — Eyebrow (string). 
- `blogs.heading` — Heading (string). 
- `blogs.intro` — Intro (text). 
- `blogs.description` — Description (text). 
- `blogs.social_image` — Social Image (image). 
- `contact` — Contact (object). Heading and sharing settings for this page.
- `contact.title` — Title (string). 
- `contact.eyebrow` — Eyebrow (string). 
- `contact.heading` — Heading (string). 
- `contact.intro` — Intro (text). 
- `contact.description` — Description (text). 
- `contact.social_image` — Social Image (image). 

### Interface wording · buttons, forms & section labels

New CMS file: `editor/interface.json`.

- `a97fb50947` — BLOGS (string). Change this interface label. Content entries are edited in their own sections.
- `f398f46c70` — SMALL IDEAS. USEFUL TAKEAWAYS. (string). Change this interface label. Content entries are edited in their own sections.
- `c326a4660b` — Field (string). Change this interface label. Content entries are edited in their own sections.
- `bcafdf9440` — notes. (string). Change this interface label. Content entries are edited in their own sections.
- `bb6113797d` — arif (string). Change this interface label. Content entries are edited in their own sections.
- `3a52ce7809` — . (string). Change this interface label. Content entries are edited in their own sections.
- `de2b346eee` — FOLLOW A THREAD (string). Change this interface label. Content entries are edited in their own sections.
- `6c9fc99089` — Close menu (string). Change this interface label. Content entries are edited in their own sections.
- `ddfe163345` — 01 (string). Change this interface label. Content entries are edited in their own sections.
- `70f8bb9a8a` — Home (string). Change this interface label. Content entries are edited in their own sections.
- `bcac9d1d8e` — 02 (string). Change this interface label. Content entries are edited in their own sections.
- `6b21fb791a` — About (string). Change this interface label. Content entries are edited in their own sections.
- `3ea6c91e24` — 03 (string). Change this interface label. Content entries are edited in their own sections.
- `5ef4439786` — Blogs (string). Change this interface label. Content entries are edited in their own sections.
- `798f861ee7` — 04 (string). Change this interface label. Content entries are edited in their own sections.
- `53e890d5f0` — Projects (string). Change this interface label. Content entries are edited in their own sections.
- `28a5c28185` — 05 (string). Change this interface label. Content entries are edited in their own sections.
- `b37456c453` — Contact (string). Change this interface label. Content entries are edited in their own sections.
- `7ac59684cc` — arifulislamfahim04@gmail.com (string). Change this interface label. Content entries are edited in their own sections.
- `6b6390a441` — LinkedIn (string). Change this interface label. Content entries are edited in their own sections.
- `b25a0477c3` — Dhaka, BD · (string). Change this interface label. Content entries are edited in their own sections.
- `ceeb27c057` — Close reading view (string). Change this interface label. Content entries are edited in their own sections.
- `be70b75841` — Previous document (string). Change this interface label. Content entries are edited in their own sections.
- `1fdb454043` — Next document (string). Change this interface label. Content entries are edited in their own sections.
- `a4ae4b24a1` — Zoom out (string). Change this interface label. Content entries are edited in their own sections.
- `4fc05f2763` — Zoom in (string). Change this interface label. Content entries are edited in their own sections.
- `7866c7c236` — Close document (string). Change this interface label. Content entries are edited in their own sections.
- `d36bcb4719` — Find your thread. (string). Change this interface label. Content entries are edited in their own sections.
- `1f7df2fe36` — Close command palette (string). Change this interface label. Content entries are edited in their own sections.
- `f27a7d8cb2` — Search pages and actions (string). Change this interface label. Content entries are edited in their own sections.
- `c92994da54` — Search pages and actions… (string). Change this interface label. Content entries are edited in their own sections.
- `c8eade842c` — Download CV (string). Change this interface label. Content entries are edited in their own sections.
- `9b0eaf14d3` — Toggle theme (string). Change this interface label. Content entries are edited in their own sections.
- `01345289e5` — Email me (string). Change this interface label. Content entries are edited in their own sections.
- `f8aae44c5e` — MY APPROACH (string). Change this interface label. Content entries are edited in their own sections.
- `f113803ac0` — THE COMMON THREAD (string). Change this interface label. Content entries are edited in their own sections.
- `698a041865` — Curiosity, made (string). Change this interface label. Content entries are edited in their own sections.
- `d585edbaa2` — practical. (string). Change this interface label. Content entries are edited in their own sections.
- `385cc51745` — NEXT CHAPTER (string). Change this interface label. Content entries are edited in their own sections.
- `a80804b43e` — A LITTLE SPACE FOR BIG IDEAS (string). Change this interface label. Content entries are edited in their own sections.
- `f6774fe69d` — Let’s make something (string). Change this interface label. Content entries are edited in their own sections.
- `a8eb6db6f0` — meaningful. (string). Change this interface label. Content entries are edited in their own sections.
- `a64b12d8ee` — WHO I AM (string). Change this interface label. Content entries are edited in their own sections.
- `1329fd0ad1` — THE PERSON BEHIND THE WORK (string). Change this interface label. Content entries are edited in their own sections.
- `26e5325f23` — me. (string). Change this interface label. Content entries are edited in their own sections.
- `4e6a22430e` — AT A GLANCE (string). Change this interface label. Content entries are edited in their own sections.
- `b9e4ab9527` — LEARNING (string). Change this interface label. Content entries are edited in their own sections.
- `593583b7da` — EDUCATION (string). Change this interface label. Content entries are edited in their own sections.
- `a99e56be67` — Where I’m (string). Change this interface label. Content entries are edited in their own sections.
- `9f9b15fe4d` — learning. (string). Change this interface label. Content entries are edited in their own sections.
- `21ab114259` — EXPERIENCE (string). Change this interface label. Content entries are edited in their own sections.
- `194b4835a0` — LEADERSHIP & INDUSTRY EXPOSURE (string). Change this interface label. Content entries are edited in their own sections.
- `3a628b12c1` — Putting learning in (string). Change this interface label. Content entries are edited in their own sections.
- `8af1917542` — context. (string). Change this interface label. Content entries are edited in their own sections.
- `2fbbf64505` — CAPABILITIES (string). Change this interface label. Content entries are edited in their own sections.
- `71b25448aa` — TECHNICAL SKILLS (string). Change this interface label. Content entries are edited in their own sections.
- `80cc55d5d7` — A practical (string). Change this interface label. Content entries are edited in their own sections.
- `bf2b84b1e8` — foundation. (string). Change this interface label. Content entries are edited in their own sections.
- `3ae9bc092d` — RECOGNITION (string). Change this interface label. Content entries are edited in their own sections.
- `200ad80484` — ACADEMIC HONOURS (string). Change this interface label. Content entries are edited in their own sections.
- `42e5140ff6` — Consistent effort, (string). Change this interface label. Content entries are edited in their own sections.
- `4ce4103ab6` — recognized. (string). Change this interface label. Content entries are edited in their own sections.
- `81a360f604` — CERTIFICATES (string). Change this interface label. Content entries are edited in their own sections.
- `661031bec1` — CONTINUING DEVELOPMENT (string). Change this interface label. Content entries are edited in their own sections.
- `972e77e4cc` — Learning beyond the (string). Change this interface label. Content entries are edited in their own sections.
- `a10864c1f0` — syllabus. (string). Change this interface label. Content entries are edited in their own sections.
- `14683d8111` — RECOMMENDATIONS (string). Change this interface label. Content entries are edited in their own sections.
- `478a2ad7d9` — REAL PERSPECTIVES (string). Change this interface label. Content entries are edited in their own sections.
- `3ea4ee781b` — Good work. Real (string). Change this interface label. Content entries are edited in their own sections.
- `f7ec18bbc3` — perspectives. (string). Change this interface label. Content entries are edited in their own sections.
- `a26a6ebdc9` — RESUME (string). Change this interface label. Content entries are edited in their own sections.
- `64677462f1` — THE FULL STORY (string). Change this interface label. Content entries are edited in their own sections.
- `058fe80b24` — Take the next (string). Change this interface label. Content entries are edited in their own sections.
- `9834541834` — thread. (string). Change this interface label. Content entries are edited in their own sections.
- `1742f5d553` — PROJECTS (string). Change this interface label. Content entries are edited in their own sections.
- `6aea88f48b` — IDEAS, EXPLORATIONS & THINGS IN PROGRESS (string). Change this interface label. Content entries are edited in their own sections.
- `9a976fc228` — Selected (string). Change this interface label. Content entries are edited in their own sections.
- `28f3a9b183` — work. (string). Change this interface label. Content entries are edited in their own sections.
- `a308935bf6` — SAY HELLO (string). Change this interface label. Content entries are edited in their own sections.
- `cf5b4626fa` — GOOD CONVERSATIONS START WITH AN IDEA (string). Change this interface label. Content entries are edited in their own sections.
- `0c50e3c4a6` — Let’s (string). Change this interface label. Content entries are edited in their own sections.
- `e1fb7c5376` — connect. (string). Change this interface label. Content entries are edited in their own sections.
- `d6fce70456` — LET’S TALK (string). Change this interface label. Content entries are edited in their own sections.
- `edee6ff660` — Good ideas start (string). Change this interface label. Content entries are edited in their own sections.
- `cfc31e1e8d` — For internships, trainee roles, academic collaboration, or a conversation about textiles and technology — get in touch. (string). Change this interface label. Content entries are edited in their own sections.
- `0cd50ae658` — SEND A MESSAGE (string). Change this interface label. Content entries are edited in their own sections.
- `3fd30dbd52` — What’s on your mind? (string). Change this interface label. Content entries are edited in their own sections.
- `ab42293e29` — Your name (string). Change this interface label. Content entries are edited in their own sections.
- `6db5ba5e66` — What should I call you? (string). Change this interface label. Content entries are edited in their own sections.
- `3fa6f5fb50` — Your email (string). Change this interface label. Content entries are edited in their own sections.
- `50e2b46ef8` — you@example.com (string). Change this interface label. Content entries are edited in their own sections.
- `8d183dbdce` — Subject (string). Change this interface label. Content entries are edited in their own sections.
- `e4a1c09b4d` — What’s your idea? (string). Change this interface label. Content entries are edited in their own sections.
- `f190c98ece` — Your message (string). Change this interface label. Content entries are edited in their own sections.
- `7c156fc177` — Tell me a little about it… (string). Change this interface label. Content entries are edited in their own sections.
- `c70a890d14` — Send message (string). Change this interface label. Content entries are edited in their own sections.
- `ad972af035` — Opens your email app with a draft addressed to me. Review it there, then send. (string). Change this interface label. Content entries are edited in their own sections.
- `38582b4b94` — Your email draft is ready. (string). Change this interface label. Content entries are edited in their own sections.
- `aab1a88bdc` — Finish sending it in your email app. (string). Change this interface label. Content entries are edited in their own sections.
- `781961bc81` — Pause (string). Change this interface label. Content entries are edited in their own sections.
- `5826b136ec` — Leave this field empty (string). Change this interface label. Content entries are edited in their own sections.
- `b583bb33fb` — No updates here yet. There will be more to share soon. (string). Change this interface label. Content entries are edited in their own sections.
- `30180a850b` — Pause gallery motion (string). Change this interface label. Content entries are edited in their own sections.
- `2a8a76d547` — More about me (string). Change this interface label. Content entries are edited in their own sections.
- `c5bfdb102c` — Contact me (string). Change this interface label. Content entries are edited in their own sections.
- `1371cbe4a7` — Open in Maps (string). Change this interface label. Content entries are edited in their own sections.
- `51e0b252cd` — Search site (Ctrl K) (string). Change this interface label. Content entries are edited in their own sections.
- `7587078164` — Theme: light. Switch to dark. (string). Change this interface label. Content entries are edited in their own sections.
- `197101e9db` — Open menu (string). Change this interface label. Content entries are edited in their own sections.
- `21deb29339` — Sample update (string). Change this interface label. Content entries are edited in their own sections.
- `ad086cf55b` — Read more (string). Change this interface label. Content entries are edited in their own sections.
- `e83249bd3b` — home (string). Change this interface label. Content entries are edited in their own sections.
- `efd197f3fc` — Main navigation (string). Change this interface label. Content entries are edited in their own sections.
- `b9bfabec0b` — Change theme (string). Change this interface label. Content entries are edited in their own sections.
- `378dc0b0bd` — Copy WhatsApp number (string). Change this interface label. Content entries are edited in their own sections.
- `16f8bb8836` — Search projects… (string). Change this interface label. Content entries are edited in their own sections.
- `1c0b1b030f` — THE LATEST THREADS (string). Change this interface label. Content entries are edited in their own sections.
- `058f36b25e` — Mobile navigation (string). Change this interface label. Content entries are edited in their own sections.
- `f2187c881c` — View projects (string). Change this interface label. Content entries are edited in their own sections.
- `9426c85d11` — A LITTLE ABOUT ME (string). Change this interface label. Content entries are edited in their own sections.
- `2bf93931c7` — min read (string). Change this interface label. Content entries are edited in their own sections.
- `508fadca1c` — Next project (string). Change this interface label. Content entries are edited in their own sections.
- `30c3c3680e` — Search projects (string). Change this interface label. Content entries are edited in their own sections.
- `7eb6c2e508` — MOMENTS, COLLECTED (string). Change this interface label. Content entries are edited in their own sections.
- `a8d4a06d59` — Explore the gallery (string). Change this interface label. Content entries are edited in their own sections.
- `c2cde8edc9` — THE NEXT THREAD (string). Change this interface label. Content entries are edited in their own sections.
- `3fab95cdf1` — View certificate (string). Change this interface label. Content entries are edited in their own sections.
- `28fe6e9638` — Map of (string). Change this interface label. Content entries are edited in their own sections.
- `00b7051632` — Share this page (string). Change this interface label. Content entries are edited in their own sections.
- `d287e34776` — More from the notebook (string). Change this interface label. Content entries are edited in their own sections.
- `badd385121` — View details (string). Change this interface label. Content entries are edited in their own sections.
- `35a6512bae` — Sample image (string). Change this interface label. Content entries are edited in their own sections.
- `419441605d` — Explore the map (string). Change this interface label. Content entries are edited in their own sections.
- `a32d98c0ef` — Footer navigation (string). Change this interface label. Content entries are edited in their own sections.
- `b3bd0b5a70` — Resume (string). Change this interface label. Content entries are edited in their own sections.
- `4ef6e9e867` — Resume gallery motion (string). Change this interface label. Content entries are edited in their own sections.
- `55fe1828e4` — Theme: dark. Switch to system. (string). Change this interface label. Content entries are edited in their own sections.
- `2b252b1e92` — Theme: system. Switch to light. (string). Change this interface label. Content entries are edited in their own sections.
- `b7c3ca0ee3` — Copied! (string). Change this interface label. Content entries are edited in their own sections.
- `ab40d89c86` — Select the text to copy it. (string). Change this interface label. Content entries are edited in their own sections.
- `e9cc6d0e9a` — No results found. (string). Change this interface label. Content entries are edited in their own sections.
- `9539a81a83` — Please complete this field. (string). Change this interface label. Content entries are edited in their own sections.
- `d2306dd897` — Please enter a valid email address. (string). Change this interface label. Content entries are edited in their own sections.
- `b785d343a2` — Your email draft is ready. Finish sending it in your email app. (string). Change this interface label. Content entries are edited in their own sections.
- `cf765512cc` — Sending… (string). Change this interface label. Content entries are edited in their own sections.
- `18d1dd0bc8` — Message sent. Thank you for getting in touch. (string). Change this interface label. Content entries are edited in their own sections.
- `693a733593` — The message could not be sent. Please try again or email me directly. (string). Change this interface label. Content entries are edited in their own sections.
- `86563d61b6` — Please add your form service details in Pages CMS first. (string). Change this interface label. Content entries are edited in their own sections.
- `9a9a20fae1` — Switch theme (string). Change this interface label. Content entries are edited in their own sections.
- `6a72085653` — All (string). Change this interface label. Content entries are edited in their own sections.
- `4e411c43d7` — Academic (string). Change this interface label. Content entries are edited in their own sections.
- `be601df25e` — Research (string). Change this interface label. Content entries are edited in their own sections.
- `973d438fe5` — Industry (string). Change this interface label. Content entries are edited in their own sections.
- `817b79b0af` — Creator (string). Change this interface label. Content entries are edited in their own sections.
- `be0068f918` — References available on request (string). Change this interface label. Content entries are edited in their own sections.
- `473710d327` — More details (string). Change this interface label. Content entries are edited in their own sections.
- `f2b789a1b8` — SELECTED THREADS (string). Change this interface label. Content entries are edited in their own sections.
- `c1055d0a89` — FROM THE NOTEBOOK (string). Change this interface label. Content entries are edited in their own sections.
- `c8a290f5ae` — Close photo (string). Change this interface label. Content entries are edited in their own sections.
- `09972524c1` — Previous photo (string). Change this interface label. Content entries are edited in their own sections.
- `fe66878201` — Next photo (string). Change this interface label. Content entries are edited in their own sections.
- `d9c883a905` — Back to top (string). Change this interface label. Content entries are edited in their own sections.
- `e1815787f2` — About sections (string). Change this interface label. Content entries are edited in their own sections.
- `6d1d62bc37` — No entries published yet. (string). Change this interface label. Content entries are edited in their own sections.
- `4fa8cc860c` — Tools (string). Edit this interface label.
- `1370004da7` — Duration (string). Edit this interface label.
- `01cedd0f0e` — No projects match your search. (string). Edit this interface label.

## Defaults and retained content

Existing entries, placeholder badges, repeated images/dates and recommendation placeholders remain. New featured/share flags are on for existing projects/posts. Location defaults to Narayanganj as requested; historical narrative copy is preserved. Official institution website fields are populated where verified; ICA Bangladesh remains blank rather than guessed. Previous card/hero fields remain in JSON for rollback, with help text identifying superseded controls. Uploads still use docs/assets and relative assets/ paths.

References and transcript opt-ins control website display. Values retained in a public GitHub repository are not secret.

## Form service setup

CMS → Site settings · footer, forms & labels → Contact form delivery. Email app works immediately. Formspree needs your own https://formspree.io/f/... endpoint. Web3Forms needs its public access key. Never enter a private API secret in a static site. Validation, honeypot, pending, success and failure states are implemented; actual delivery remains unverified until your service is configured.

The original editor/about.json is intentionally unchanged. New privacy flags default off when absent. New About-photo fields keep their original rendered values until filled. The website’s Based in fact follows Profile → Location. This avoids republishing the source file’s third-party contact details during this redesign.
