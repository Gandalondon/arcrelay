# ArcRelay for Android: Play Store release

Everything for the Google Play listing lives here. Off the site (the site is `site/`), and changes here don't build the APK.

## Done (4 Nov 2026)

- **Icon**, `icon/arcrelay-play-icon.png`: 512 x 512 PNG, sRGB, no alpha, full square (Play adds the rounded corners and shadow). The same three signal lines as the launcher icon, made by `tools/make-icon.py`.
- **Play listing art**, in `play-listing/`:
  - `arcrelay-play-screenshot-1-ask.png`, `arcrelay-play-screenshot-2-hey-relay.png`: 1080 x 1920, 24-bit PNG with no alpha. Real app screens (captured at 9:30pm so the greeting says Evening) in a phone outline, one headline each.
  - `arcrelay-play-feature-graphic.png`: 1024 x 500, the logo and "Ask. Find. Get out." beside the site's desk photo. Content kept clear of the edges, which Play can crop.
  - `arcrelay-play-listing-text.txt`: short description (79/80) and full description, above and below the `---`.
  - `arcrelay-play-alt-text.txt`: alt text for each image.
  - `source/`: `capture.js` captures the app screens, `shot.html` + `render.js` lay them out. Re-run both after UI changes.

## Listing details

- App name: ArcRelay: Voice Companion. Category: Tools. Privacy policy: https://getarcrelay.app/beta/privacy
- Data safety: collects nothing, shares nothing, no account.

## To do

- A screenshot with the map (exits marked, you-dot and route). Best taken on the Pixel, then framed with `shot.html`. The build sandbox can't reach MetaForge's map tiles.
- More screenshots as features land (Play promotes listings with 4 or more).
