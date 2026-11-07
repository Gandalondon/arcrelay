# Relay site (getarcrelay.app)

- The full site lives at the root (7 Nov 2026): `index.html` (homepage), `how-it-works`, `privacy`, `legal`, `feedback`. It replaced the holding page, which is kept in `tools/hero/holding-page-7nov.html`.
- Old /beta addresses redirect to the same page at the root (`vercel.json`), so the links in the app and the Play listing keep working.
- `fonts/`: Inter Tight (SIL Open Font Licence), served from here, not Google Fonts.
- Feedback is an email link to feedback@getarcrelay.app (ImprovMX forwards it), not a form.
- Vercel: project root directory is `site/`, no build step. Pushes that only touch `site/` don't build the APK.
- Every page with a map credits MetaForge at the bottom (their condition, 1 Nov 2026).
- Domain getarcrelay.app is on the existing Vercel project "arcrelay" (Ganda team, Hobby), root directory site/.
