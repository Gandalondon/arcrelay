# Relay for Android: Play Store release

Everything for the Google Play listing lives here. Off the site (the site is `site/`), and changes here don't build the APK.

## Done (4 Nov 2026)

- **Icon**, `icon/arcrelay-play-icon.png`: 512 x 512 PNG, sRGB, no alpha, full square (Play adds the rounded corners and shadow). The same three signal lines as the launcher icon, made by `tools/make-icon.py`.
- **Play listing art**, in `play-listing/` (redone 5 Nov 2026 to match the new site):
  - `arcrelay-play-screenshot-1-evac.png`, `-2-ask.png`, `-3-find.png`, `-4-where.png`: 1080 x 1920, 24-bit PNG with no alpha. The homepage's four headlines in cream Inter Tight on charcoal, each above the matching real app screen in a phone frame (frame and corners in proportion, as on the site). No gradients or glows.
  - `arcrelay-play-feature-graphic.png`: 1024 x 500, the site's closing lockup: "Ask. Find. / Get out." in 700 cream on the left, the 3D phone turned the finale's way on the right showing the evac answer. Content kept clear of the edges, which Play can crop.
  - `arcrelay-play-listing-text.txt`: short description (79/80) and full description, above and below the `---`.
  - `arcrelay-play-alt-text.txt`: alt text for each image.
  - `source/`: `shot.html` lays the art out, `render.js` renders it, `finish.py` flattens it to the final names. The screens are copies of the site's captures (`site/beta/screens/`).
  - **Before upload:** the screens were captured on 4 Nov, before the app moved to Inter Tight, so the app text in them is still Barlow. Re-capture on the Pixel (`capture.js`), copy them over the four `screen-*.webp` in `source/`, then `node render.js && python3 finish.py`.

## Listing details

- App name: Relay: Raid Voice Guide. Category: Tools. Privacy policy: https://getarcrelay.app/beta/privacy
- Data safety: collects nothing, shares nothing, no account.

## To do

- A screenshot with the map (exits marked, you-dot and route). Best taken on the Pixel, then framed with `shot.html`. The build sandbox can't reach MetaForge's map tiles.
- Re-capture the four screens in Inter Tight (above). More screenshots as maps and features land.
