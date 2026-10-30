# Incomplete comments draft — not deployed

Preserved on 30 October 2026 when Arif requested a handoff to a new chat.

These files are untested scaffolding, not a working feature. They are deliberately outside the active build. There is no comments.js runtime, no configured Firebase project, no active Google authentication, no deployed rules, no moderation dashboard and no verified permission tests. Do not move these files into the active build and claim completion.

Intended features: anyone reads; Google sign-in to post/reply/vote; owner approval/deletion; one like/dislike vote per account; no public email addresses; free plan only with billing disabled. Arif reports the Firebase integration does not work in ChatGPT and asks for an alternative. Reassess the provider/setup route before continuing. Giscus does not satisfy the Google-sign-in requirement.

The attempted local rules-test dependency installation failed with registry 403 errors. No emulator security test passed. Review all rules and test authorization before deploying any backend. The hardcoded draft moderator email must be deliberately verified with the owner; do not infer authority from a frontend setting.
