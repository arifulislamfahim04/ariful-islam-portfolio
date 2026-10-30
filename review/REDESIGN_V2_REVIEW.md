# Ariful Islam Fahim — Portfolio · redesign v2

Review branch: portfolio-redesign-v2. Do not merge until Ariful writes “approved”. Main and the original GitHub Pages deployment remain unchanged. The existing separate Sites review URL is reused and its current public audience preserved.

## Phases

A: warm paper/ink/madder tokens, dark theme, Fraunces display and DM Sans UI, shared spacing/type/form controls, self-hosted fonts and locked SVG Repo filled icon inventory.

B: identical header/footer/mobile nav order (Home, About, Projects, Gallery, Blogs, Contact), home icon retained, search/Ctrl K, persisted light/dark/system applied before paint, right-side mobile dialog and back-to-top ring. Cross-document View Transitions with a nonblank fallback replace the delayed page wipe.

C: compact CMS profile, status chips/social links, reserved typewriter layout, CV/projects buttons, CMS location and Dhaka clock, four slim stats. Highlights ticker/latest details, projects, opposing gallery rows, About teaser, latest notes and contact CTA.

D: retained gallery filters, search, placeholder flags, captions/stories/credits. Native photo dialog with keyboard/focus behavior and added swipe handling. Lazy local images and fixed ratios.

E: About section index, timelines, skill chips, five separate awards in a horizontal shelf, expandable details, optional certificate actions and institution website fields. Reference/transcript website display is opt-in.

F: project rich content/reports preserved, optional tools/duration/SEO, project search/filter chips, readable blog dates, reading time, author/related posts/sharing. Contact retains email/phone/LinkedIn/copy buttons and adds WhatsApp and optional Formspree/Web3Forms delivery. Map and location derive from CMS; one map sits in normal document flow, collapsed by default.

G: scroll reveals, subtle desktop tilt/magnetic interaction, small portrait parallax, stats counting, cursor-responsive thread texture, pause/focus/touch controls. Reduced-motion CSS/script guards and a static gallery grid.

H: content/code tests, local-reference validation, responsive browser inspection and 20 requested screenshots.

## Preserved

Original templates, Python/lxml generator, Pages CMS media/collections, all 14 routes, full story content, CV PDF and relative paths remain. No new runtime dependency. Sample badges, historical expected dates, repeated photos/post dates and recommendation placeholders were not corrected or removed. Old presentation files remain for rollback; only the editorial stylesheet/runtime is loaded in review pages.

## Verification

Passed: build; 14 pages/741 local references; CMS add/edit/remove/drafts; optional fields populated/cleared; shared nav/gallery lifecycle; profile/phrase/chip changes; safe rich text/URLs; privacy opt-ins; website/file controls; page/entry SEO; form-provider configuration; JS syntax; git diff whitespace. Inline SVG references resolve.

Browser: Chromium desktop and 390px phone widths in both themes; additional 768px and 320px inspection. Final inspected states had no horizontal overflow or loaded-image failures. Menu/Escape, Ctrl K and gallery search/viewer were exercised. Some early narrow-width samples were captured before navigation completed and were not accepted as final evidence; the harness was changed to wait for iframe load. A long QA batch later timed out. This is not a claim of an exhaustive automated device matrix.

QA fixes: intrinsic About image overflow; an overbroad cleanup removing Gallery from the mobile menu; a second legacy Contact map; empty rich-text fields generating empty details controls.

## Limits and decisions

- Actual iPhone Safari, touch/pen hardware, safe areas on hardware, OS-level reduced motion, measured frame rate and full accessibility audit remain unverified.
- Lighthouse/mobile performance 90+ and numeric CLS were not measured; no score is claimed.
- Actual form delivery needs the owner’s service configuration. Email app remains the default. No test messages were sent.
- Actual uploaded certificate files, live CMS UI clicks and the eventual GitHub Pages deployment were not tested. Optional document fixtures pass generation tests.
- The ICA Bangladesh official URL remains blank/editable because it could not be confidently established.
- A custom replacement cursor and excessive heading motion were intentionally omitted. The system cursor/native dialogs and subdued thread pattern favor keyboard/touch usability. No results, charts or certificates were fabricated.
- Privacy toggles hide website content; they do not make values retained in a public source repository confidential.

## Review material

CMS_CHANGES_V2.md contains every configuration addition and editing instructions. FILES_CHANGED_V2.md lists every changed file. SCREENSHOTS_V2.md links all 20 desktop/phone light/dark screenshots. ICONS.md and asset source/licence files document the icon/font choices.

The separate Sites preview is a snapshot of generated docs, not a replacement CMS. After approval, the existing main-only GitHub Pages workflow remains the publishing path. The original repository was not renamed because doing so could affect its live Pages URL.

## About source preservation

Automatic approval review rejected rewriting editor/about.json because it includes third-party contact details, even though those records were already present and unchanged. That source file is left byte-for-byte unchanged from the previous public branch. New privacy controls default off in the renderer when absent; the original photo caption/alt are retained until edited, and the rendered location follows Profile. No rejected data update was published.
