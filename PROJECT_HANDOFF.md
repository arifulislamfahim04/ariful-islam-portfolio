# Website project — start here
Updated 30 October 2026 (Asia/Dhaka).

## Read this before doing work
Arif wants to continue in a NEW CHAT inside his Website project. Do not start over, rebuild the website from scratch, or make him repeat decisions. Read this file, inspect current GitHub main and any new CMS commits, then act on his requested edits. This file describes the handoff snapshot; live repository/CMS content takes precedence if it changes.

## Exact destinations
- Live website: https://arifulislamfahim04.github.io/ariful-islam-portfolio/
- ACTIVE repository: https://github.com/arifulislamfahim04/ariful-islam-portfolio
- Active branch: main
- CMS editor: https://app.pagescms.org/arifulislamfahim04/ariful-islam-portfolio/main
- CMS sign-in/root: https://app.pagescms.org/
- Latest verified website source commit before this documentation handoff: 9052a47fb6d9ad5dcdb47a8e2911510197805ba3
- Successful build/deploy: https://github.com/arifulislamfahim04/ariful-islam-portfolio/actions/runs/41009767788
- Older original repository, KEEP INTACT: https://github.com/arifulislamfahim04/arif-portfolio-studio
- Earlier review copy: https://ariful-homepage-review.misc-obsurfer.chatgpt.site
The GitHub website is now the active editing target. Do not deploy routine edits only to the review copy.

## Owner and working preferences
- Name: Ariful Islam Fahim; preferred name Arif. Bangladeshi textile engineering student, Green University of Bangladesh, Apparel Manufacturing.
- Current CGPA is **3.90 / 4.00**, explicitly confirmed. Older memory saying 3.91 is outdated.
- Class representative for 41 students; display **40+ students**.
- Classes complete; final defense/project remain. Do not invent dates.
- Existing content is mostly genuine but some is outdated. Keep it pending the owner's revisions. Explicitly labelled sample content still exists.
- Arif is not a coder, uses voice typing and wants plain, concise explanations.
- **Zero ongoing budget. No paid services, billing upgrades, credit cards, paid trials or chargeable backend features.** His ChatGPT Plus trial is nearly over; minimize unnecessary tool calls and preserve progress.
- He wants to make small, specific website changes and expand CMS control.
- Keep the original repository/website and current CMS access to it intact.
- Continue authorized reversible work without repeatedly asking for permission. Authentication, terms acceptance and sensitive access still need the appropriate user involvement.

## What is LIVE and verified
- Complete static multi-page portfolio with Home, About, Projects, Gallery, Blogs and Contact; eight project/article detail pages and a custom 404 (15 generated pages total).
- Approved mint #78cc6d, Poppins, neutral light/dark surfaces and rounded cards on all pages.
- Responsive dock: right vertical navigation on desktop, bottom navigation on phones; active indicator, tooltips, progress back-to-top and accessible menu dialog.
- Shared footer: contacts, copy controls, status, social links and CMS-driven navigation.
- Theme: early head script, saved/system preference, circular reveal from initiating toggle, fallback and reduced-motion behavior.
- Native page navigation with brief ariful. signature transitions; no hash-link interference; keyboard focus/scroll handling.
- Optional two-element custom desktop cursor; native fallback on touch, reduced motion, text inputs, dialogs and transitions.
- About sections: education/timeline, facts/Now panel, skills/languages, awards carousel/viewer, compact certificates/workshops, experience/leadership/visits, recommendations and real CV preview/download.
- Mint favicon; route titles/descriptions/sharing metadata; print styling for About; responsive WebP variants of heavy rendered images.
- Contact form prepares an email draft, with an explicit Gmail compose alternative. **It does not send messages through a server.** mailto links no longer force a new tab. Native mailto requires a configured email handler. Copy-email controls remain.
- Google Analytics and other analytics have NOT been added.

## CMS: confirmed connected, with limitations
Arif signed in and authorized the new repository. After a refresh, BOTH old and new repositories appeared in Pages CMS. The new main branch opened successfully with fields, portrait, CV and current facts.
- Collections/fields include Profile; Homepage; Biography; Blogs; Projects; Education; Experience; Certificates; Awards; Workshops; Gallery; Updates; Site settings; Page headings/SEO; Interface wording; About design/motion; Skills; Shared footer.
- Entries can be added/edited/hidden/reordered/deleted; blog/project detail pages are generated automatically.
- Article bodies are rich-text HTML with uploaded media. Ordinary titles are plain strings.
- Bold, italic, lists, links, inserted images and basic code/table markup are supported by the content pipeline. Free text colors/styles and executable scripts are not.
- Blog publication save -> GitHub commit -> Actions build -> GitHub Pages deployment. Initial build/deploy passed. **A new save made THROUGH CMS has not yet been tested end to end.**
- Some CMS fields are obsolete leftovers and no longer control the final visible design. Do not claim every field works.
- A dedicated favicon picker, truly page-by-section organization, controls for EVERY icon/heading/button, arbitrary section addition/reordering, presets for typography/color and advanced article blocks remain future work.

## Most recent requested future features
Arif accepted the direction of improving CMS organization and adding article blocks:
- Text, images/captions, quotes, tables, properly displayed mathematics, displayed code snippets and selectable interactive tools (e.g. unit converters).
- No need to write a sample converter just to explain it.
- Proper equation rendering is NOT installed. No interactive-tool registry is installed.
- Code can be displayed; pasted executable code is removed by the sanitizer. New runnable tools need an integration before the CMS can select them.
- Prefer visual inputs/presets; do not make Arif edit source code for routine updates.
These broader CMS upgrades have NOT been implemented.

## Comments: NOT LIVE; reassess the provider first
Requirements agreed:
1. Anyone can READ comments without an account.
2. Google sign-in to post/reply/like/dislike; do not require GitHub accounts.
3. Owner can approve/delete/moderate comments and close discussions.
4. New comments/replies should wait for approval.
5. No public email addresses; one vote per signed-in account.
6. Zero ongoing cost. A separate free moderation page/tab is acceptable.

Firebase Spark was proposed, with billing disabled. An official Firebase integration was suggested but **not confirmed connected**. Arif reports Firebase does not open/work properly in this ChatGPT environment and asks for an alternative. Do not keep repeating the failed integration setup as if it worked.
- Giscus was researched: free, but requires GitHub accounts; it DOES NOT meet Arif's Google sign-in requirement.
- Do not claim an alternative supports Google sign-in/free hosting without checking its current official documentation.
- Provider/account setup and data permissions may require Arif's involvement.
- No Firebase project, Firestore database, active Google sign-in, moderation dashboard, comments UI runtime or deployed security rules was completed.
- Untested partial scaffolding is archived in **drafts/comments/**, OUTSIDE the active build. Read its README before reusing anything.
- Draft files include a build helper, public configuration placeholder, CSS, pure JS helpers and Firestore rules/indexes.
- **No comments.js runtime exists.** Draft helper would reference it if mistakenly activated.
- Local emulator test dependency installation failed with npm registry 403 errors. NO backend authorization tests passed. Do not deploy draft rules without review/testing.
- Draft moderator email is hardcoded; verify authority before any real setup.
- The last user message prioritizes this HANDOFF and explanation of ChatGPT usage before further comments implementation.

## Repository/build map
- editor/: JSON content edited by Pages CMS.
- .pages.yml: Pages CMS schema (JSON syntax in a YAML-named file).
- templates/: retained structural inputs.
- scripts/build_editor.py: active build pipeline.
- scripts/*.py: source component builders.
- scripts/*.css and *.js: maintained presentation/runtime sources.
- docs/: generated static output PLUS uploaded assets in docs/assets/.
- dist/: **immutable legacy build input**. Never overwrite it with docs/.
- .github/workflows/publish.yml: main push/workflow_dispatch builds, tests and deploys docs via GitHub Actions.
- .github/workflows/homepage-review.yml: review validation.
- README.md, EDITING.md, CMS_QUICK_START.md: user/maintainer guidance.
- drafts/comments/: inactive unfinished work; no build hook.
- requirements.txt includes lxml and Pillow.
- No frontend passwords, service-account keys or GitHub tokens.

Build:
    python -m pip install -r requirements.txt
    python scripts/build_editor.py
    python scripts/check_site.py

Relevant checks (run those appropriate to actual changes):
    python scripts/test_launch.py
    python scripts/test_editor.py
    python scripts/test_optional_fields.py
    python scripts/test_home_design.py
    python scripts/test_home_polish.py
    python scripts/test_shared_footer.py
    python scripts/test_shared_dock.py
    python scripts/test_about_headers_cv.py
    node scripts/test_theme.cjs
    node scripts/test_page_navigation.cjs
    node scripts/test_cursor.cjs
    node --check docs/editorial.js
Do not run snapshot-mutating tests concurrently with edits/build copies. Some tests use temporary copies; test_about_refresh.py temporarily changes live local settings with finally restoration.

## Verified checks and their limits
- First GitHub build and deployment succeeded, including all workflow tests.
- Browser verified all six live main pages: correct design, no horizontal desktop overflow, no broken loaded images.
- Earlier review layout checks used iframe widths 360, 390, 768, 1024, 1280, 1440 with no page overflow.
- Contact validation, Gallery Esc/focus return, menu behavior, theme handoff, copy feedback and print-style rendering were checked.
- Physical phones, actual screen readers, actual printer pagination and throttled-phone performance are NOT verified.
- No external emails were sent and no real visitor comments were posted.
- All reviews should distinguish existing real content from explicitly marked samples.

## Access in a new chat
Project membership does not itself guarantee access to prior browser tabs, credentials or scratch files. Check tool connections and current repository access. Use the connected GitHub tools where sufficient. For repository creation/Pages controls, the connector lacked those actions and GitHub web UI was used.
- Prefer fetching current main, preserving any CMS commits.
- Do not ask Arif to paste secrets into chat.
- Existing CMS browser session may be reusable, but do not promise it exists in a new chat.
- The repository and this handoff are the durable source of truth; local scratch paths below are conveniences only.

## Prior local workspace (may not exist in a new chat)
- Active checkout: /workspace/scratch/405adc299f16/ariful-islam-portfolio (main tracks origin/main).
- Previous authoring checkout: /workspace/scratch/405adc299f16/portfolio-polish (hero-soft-geometric).
- Old Sites output checkout: /workspace/sites/ariful-homepage-review (generated dist only).
- Uploaded CV sources: /workspace/scratch/405adc299f16/project_sources/ .
- Current live CV PDF contains 3.90 / 4.00.
- A prior copied-history backup branch is prepared-copy-history.
Do not rely on these paths instead of retrieving the repository if absent.

## Recommended next actions
1. Ask for/accept Arif's specific next website edit, without repeating the full project interview.
2. Inspect current main/CMS content before changing it.
3. If resuming comments, first select a genuinely free Google-sign-in-compatible setup that works in his environment; retain his moderation/voting requirements.
4. If resuming CMS improvements, reorganize page/section controls and remove legacy fields carefully while preserving existing data.
5. Test, publish to the NEW GitHub repository only, and report what is actually live versus pending.
