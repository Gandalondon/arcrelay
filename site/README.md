# ArcRelay site (getarcrelay.app)

- `index.html`: the holding page ("coming soon").
- `beta/`: the full site, unlisted (noindex) at getarcrelay.app/beta.
- `fonts/`: Barlow (SIL Open Font Licence), served from here, not Google Fonts.
- Vercel: project root directory is `site/`, no build step. Pushes that only touch `site/` don't build the APK.
- Every page with a map credits MetaForge at the bottom (their condition, 1 Nov 2026).
- Domain getarcrelay.app is on the existing Vercel project "arcrelay" (Ganda team, Hobby), root directory site/.
