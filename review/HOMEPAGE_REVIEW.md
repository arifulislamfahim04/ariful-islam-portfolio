# Homepage redesign — review branch

**Branch:** `homepage-polish-review` · **Scope:** homepage presentation, its CMS settings, and clearly marked gallery samples. Nothing has been merged or deployed to GitHub Pages.

[Desktop screenshot](screenshots/homepage-desktop-dark.jpg) · [Phone screenshot](screenshots/homepage-phone-light.jpg)

## What changed

1. One container grid aligns the header, hero, gallery, updates and footer. The ID-card name stays on one line. CV / About actions precede the availability line, and a separate labelled contact group contains LinkedIn, Mail and optional Facebook. The Connect label and main CTA use `contact.html`.
2. The smaller 4:5 photograph overlaps a printed card. Cursor-responsive foil, a clip, an elastic lanyard, and a fixed-substep damped spring replace the old 18px drag. Mouse dragging works across the card; touch and pen dragging start at the clip. Arrow keys move the card; Enter / Escape / leaving keyboard focus returns it. The card has a small idle sway and stops simulating off-screen or in a hidden tab. Travel is bounded by the viewport, so shorter screens permit less downward travel.
3. A responsive, locally stored Pixabay laptop photograph sits behind the full hero. Theme-specific overlays keep it quiet. Parallax uses transforms, and the decorative image has empty alt text and a low fetch priority.
4. `ARIFUL.` types first, then the descriptor, then the interests type / hold / delete in a loop. Full-text reserve layers prevent typing from changing the layout. Accessible heading text stays stable. Reduced motion shows the final text immediately.
5. The homepage rail is on the left: navigation, theme, then a separated back-to-top control with its existing progress ring. Tooltips support focus as well as hover. A sliding marker follows the homepage's hero, gallery preview and final CTA; page links retain their existing routes. Phones use a bottom bar; at very narrow widths theme / back-to-top stack above it. Other pages keep their current rail.
6. The gallery has two continuous, opposing rows with three visible columns on desktop, two on tablet, and larger partial cards on phones. Hover, focus, an explicit pause button, reduced motion, visibility and the photo dialog pause motion. Slideshow mode retains previous / next, position count, swipe / keyboard browsing, and optional autoplay. Mode is remembered in session storage for the visit. Placeholder badges depend on each image's CMS flag. One collection still feeds both the homepage and the existing Gallery page.
7. A dated updates timeline replaces the generic overview cards and interests strip. It shows the latest three matching entries, supports all four requested topic filters, and handles empty topics. Three entries are explicitly marked as examples; none claims an actual achievement.
8. The main CTA remains; the redundant footer CTA and ghost text are removed. The requested footer copy, editable search/sharing metadata, canonical URL and lettermark favicon are included. Bricolage Grotesque / Inter / JetBrains Mono are self-hosted. The homepage omits the old canvas and custom-cursor loop and uses only its scoped enhancement assets. Relative routes and the CMS résumé path remain intact; a local CV uses a real download attribute.

## What you can edit in Pages CMS

| CMS area | Editable content |
| --- | --- |
| Profile, résumé & homepage | Full name, photo and alt text, résumé PDF, availability, email, LinkedIn, optional Facebook; existing profile fields remain available |
| Homepage design & gallery settings | Logo / preferred name, headline, description, card label / tagline, rotating interests, optional background and smaller background variant, gallery headings / limit / autoplay / default mode, updates heading and introduction, optional search title / description / sharing image / canonical URL |
| Gallery | Image, alt text, title, caption, story, category, date / location, credit / source URL, order, featured, placeholder, published |
| Homepage news & updates | Title, date, one of four topics, short text, optional image / alt text / link, sample flag and published flag |

Upload media directly in Pages CMS. Its existing media configuration writes to `docs/assets` and stores an `assets/...` path. You do not need to edit HTML or upload through GitHub separately. Empty optional background, interests, news image/link, and Facebook values produce no corresponding content. Publish is off by default for new updates. Clear **Sample update** only for a real update; clear **Placeholder** only when a gallery photo is your own content.

These new forms belong to this review branch. The live site's CMS configuration will change only after the branch is reviewed, merged and built through the existing deployment workflow.

## Assets and licences

- All newly added stock photos are from Pixabay and live together under [`docs/assets/placeholders`](../docs/assets/placeholders/SOURCES.md). Six verified source pages and photographers are recorded there. WebP images are locally served, approximately 11–71KB each. The Pixabay Content License does not require attribution; credits and source links are retained. The photographs are illustrative samples, not personal documentation.
- All homepage icon vectors are from SVG Repo's Phosphor Filled collection. [`vendor/home-icons/sources.json`](../vendor/home-icons/sources.json) records every exact source and displayed CC0-1.0 licence. Vectors are embedded with `currentColor`; there are no icon-library requests.
- [`docs/assets/fonts/SOURCES.md`](../docs/assets/fonts/SOURCES.md) records the three font families. OFL notices are included. Latin WOFF subsets total approximately 100KB; display / text are preloaded and use `font-display: optional`. Other scripts have system-font fallbacks. WOFF avoids introducing a font-encoder dependency into deployment.
- The portrait remains the supplied photograph. The favicon is an original code-drawn lettermark. Existing photos/icons on unrelated pages are unchanged.

## Verification

The browser used an uncommitted iframe harness with the **actual CSS viewport dimensions** below, fitted inside its fixed desktop window. This tests responsive layout rather than physical-device input. Both themes were checked for horizontal overflow, loaded image failures, the card name's fit, and matching container edges.

| CSS viewport | Dark | Light |
| --- | --- | --- |
| 1920 × 1080 | Pass | Pass |
| 1440 × 900 | Pass | Pass |
| 1280 × 720 | Pass | Pass |
| 768 × 1024 | Pass | Pass |
| 390 × 844 | Pass | Pass |
| 320 × 700 | Pass | Pass |

The narrowest layout exposed an inherited automatic minimum grid width; the final build explicitly uses `minmax(0, 1fr)` and has no horizontal overflow. The card name fits on one line in all six layouts. Header / hero / gallery / footer content edges match at every tested width.

Browser checks covered a long mouse drag (520px horizontal pointer travel), elastic return, gallery mode switching, opposing animation directions, photo viewer, update filter empty state, and theme persistence. All five other top-level routes loaded with six navigation links and one theme control in both themes. No production-page console error was observed; browser-extension messages and a transient error in the local-only harness were excluded. The harness is not shipped.

Automated checks:

- `python scripts/build_editor.py`
- `python scripts/check_site.py`
- `python scripts/test_editor.py`
- `python scripts/test_optional_fields.py`
- `python scripts/test_home_design.py`
- `python scripts/test_home_polish.py`
- `node --check docs/home-core.js`
- `node --check scripts/home_polish.js`

The tests cover content add/edit/remove, drafts, safe HTML and URLs, optional-field clearing, résumé / photo replacement, gallery empty and single-photo cases, six-route navigation, ordered updates, optional update media, Facebook, and editable search metadata. The review workflow runs validation only; the Pages publishing workflow remains restricted to `main`.

Representative solid palette contrast ratios range from **4.90:1** (white on the dark-theme primary button) to **17.41:1** (main dark-theme text). Secondary and accent text pairs also exceed 4.5:1. This calculation is not a complete accessibility audit.

## Decisions and verification limits

- There is no updates archive page in the existing site, so no dead “See all updates” link was added. Each topic filter can show its latest three entries.
- Gallery images are intentionally marked as placeholders until replaced. The six sample source records replace only existing stock examples and add two samples; personal photos were not invented.
- The nav's page links continue opening real pages. Scroll-spy highlights the related homepage preview rather than changing those links into section-only routes.
- Reduced-motion branches are implemented and inspected, but the available browser cannot emulate the operating-system motion preference. Actual touch / pen hardware and multiple browser engines were not available.
- No Lighthouse run, numerical performance score, complete WCAG audit, or measured CLS score is claimed. Layout space is reserved for fonts, images and typed text, but Lighthouse 90+ and field performance still need measurement on the review build.
- The CV link retains the original CMS-selected PDF path, has a download attribute, and resolves to a valid 703,290-byte local PDF. The cloud browser’s end-to-end download capture timed out, so browser transfer completion is not claimed.
- The updated Pages CMS forms were checked against the repository's configuration and build tests, not exercised in the live CMS. Social-crawler rendering and the eventual GitHub Pages deployment are unverified because deployment is intentionally deferred.

## Review

Review the screenshots and this branch first. The implementation is split into eight numbered commits. Generated files under `docs/` are included for inspection, while `scripts/`, `editor/` and `.pages.yml` remain the source of truth. No new runtime dependency was added. Approval to merge/deploy remains a separate step.
