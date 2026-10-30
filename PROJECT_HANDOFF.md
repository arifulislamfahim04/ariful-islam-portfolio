# Portfolio review handoff

Updated 30 October 2026. This file records the current implementation so work can continue in another chat or after launch.

## Source and publication

- GitHub repository: `arifulislamfahim04/ariful-islam-portfolio`.
- Authoring branch: `main` in the new independent repository. The original repository is unchanged.
- Review site: https://ariful-homepage-review.misc-obsurfer.chatgpt.site
- The review site is public. Preserve its current audience.
- The Sites deployment checkout contains generated output only. Continue code changes in the authoring repository.
- The owner requested a new independent GitHub repository and public GitHub Pages launch, preserving the original repository and site.

## Design and content decisions

- Use the approved mint `#78cc6d`, Poppins, rounded cards and neutral light/dark surfaces across all pages.
- Current CGPA: **3.90 / 4.00**. Previous 3.91 is outdated.
- Class representative: 41 students in the cohort; display **40+ students** consistently.
- Existing content is mostly real but may be outdated. Preserve it until the owner supplies revisions; do not describe all older content as fictitious.
- Classes are complete; final defense/project remain. Do not invent dates or grades.
- Analytics has not been added.

## Editing and building

- `editor/` contains CMS JSON; `.pages.yml` defines the Pages CMS interface.
- `scripts/build_editor.py` builds `docs/`. Edit builders and source CSS/JS, then rebuild; editing generated HTML alone will be overwritten.
- `dist/` is an immutable legacy build input. Do not replace it with the generated site.
- `scripts/launch_polish.py` and `portfolio-foundation.css` apply the shared design, email clarity, responsive image variants, 404 and print rules.
- Pillow is now a declared build dependency for WebP generation.
- All six main routes and eight detail pages retain their existing URLs. `404.html` is additional and excluded from the sitemap.

## Existing interactions

- Shared footer, dock/menu, theme control, page transitions and optional custom cursor work across routes.
- CMS can disable motion/cursor. Reduced motion and native fallbacks are implemented.
- Contact is in **Email app** mode: it prepares a draft and does not send from the website. Gmail is an explicit alternative compose action. Copy-email controls remain available.
- Email links do not force new tabs. A laptop still needs a configured email handler for `mailto:`; the site cannot configure that for the visitor.
- A future direct-send form would require an intentionally configured form service. Do not claim delivery without a successful service response.

## Verification and next review

- Build and local-reference checks cover 15 pages. Regression checks cover CMS optional content, shared navigation, theme, page transitions and cursor behavior.
- Browser checks covered six main pages at 360, 390, 768, 1024, 1280 and 1440 CSS-pixel iframe widths, without page overflow. These are browser layout checks, not physical-device testing.
- Contact validation, dark colors, Gallery viewer Escape/focus return, and print-style rendering were checked in the browser.
- Physical phones, real screen readers, actual printer pagination and throttled-phone performance still need separate validation.
- No external email was sent during testing. Do not trigger actual contact messages for QA.
- Before replacing GitHub main, review the current output, resolve any requested detail changes, and explicitly handle the pending GitHub synchronization authorization.
- Keep temporary `qa-*` fixtures out of deployments.
