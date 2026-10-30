# Homepage fonts

Self hosted Latin subsets (letters, punctuation, copyright and common typographic marks), encoded as WOFF to avoid a build-time font encoder dependency. No font transformation runs in deployment. Other scripts use browser fallback fonts.

- `display.woff`: Bricolage Grotesque, weight 700, from Google Fonts: https://fonts.google.com/specimen/Bricolage+Grotesque . SIL OFL 1.1, included alongside.
- `text.woff`, `text-semibold.woff`: Inter, weights 400 and 600, from Google Fonts: https://fonts.google.com/specimen/Inter . SIL OFL 1.1, included alongside.
- `mono.woff`: JetBrains Mono, weight 400, from Google Fonts: https://fonts.google.com/specimen/JetBrains+Mono . SIL OFL 1.1, included alongside.

The display and regular text faces are preloaded. `font-display: optional` prevents a late font swap. Total font payload is about 100KB. Keep the OFL notices when redistributing these files; no on-page attribution is required.
