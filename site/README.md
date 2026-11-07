# Relay site (getarcrelay.app)

- `index.html`: the holding page ("coming soon").
- `beta/`: the full site, unlisted (noindex) at getarcrelay.app/beta.
- `fonts/`: Inter Tight (SIL Open Font Licence), served from here, not Google Fonts.
- Vercel: project root directory is `site/`, no build step. Pushes that only touch `site/` don't build the APK.
- Every page with a map credits MetaForge at the bottom (their condition, 1 Nov 2026).
- Domain getarcrelay.app is on the existing Vercel project "arcrelay" (Ganda team, Hobby), root directory site/.
- Go-live is prepared (7 Nov): the /beta pages already have final canonical and share tags, and feedback is an email link. To go live, redo commit c399dd5 (move beta/ to the root, holding page to tools/hero/, drop noindex and base, /beta redirects, robots allow, sitemap), e.g. git revert of the commit that undid it.
