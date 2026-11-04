# ArcRelay: where we are (end of Wednesday 4 November 2026)

Start a new conversation by reading this file. It replaces the long 4 Nov chat.

## The project in one paragraph
ArcRelay is Tony Goff-Yu's free, unofficial, voice-first Android companion for ARC Raiders (Pixel 9). Ask out loud ("Hey Relay" or tap), it answers out loud and shows a map: nearest exit, quest steps, items, "not that one" rerouting. Everything runs on the phone. Blue Gate only so far. Rules: £0 to run (no paid services or keys), UK English, no em dashes, no widows, palette charcoal #1C1E22 / panel #26282D / ink #15171C / cream #EEE8DC / amber #F2B33D, Barlow, Material Symbols Rounded only. Push to main when Tony says push or has approved the work. The style guide is the rulebook: `src/docs/style-guide.html`.

## Where things are
- Repo: github.com/Gandalondon/arcrelay (renamed from spottr), branch main. Mac copy: `~/ArcRelay` (git clone; pull after each push).
- App: `www/index.html` (whole app), native plugins in `android/app/src/main/java/app/spottr/companion/`. Tests: `node tests/run.js`.
- Builds: GitHub Actions makes APK releases `v1.0.N` on each push that touches the app; Tony installs via Obtainium. Pushes touching only `site/`, `android-release/`, `marketing/`, `src/docs/`, `tools/style-guide/` or `*.md` skip the build.
- Site: `site/` on Vercel project "arcrelay" (Ganda team, Hobby), root directory `site`. getarcrelay.app = holding page; getarcrelay.app/beta = full site (noindex).
- Play listing: `android-release/` (icon, 2 screenshots, feature graphic, listing text, alt text, README). App name on Play: "ArcRelay: Voice Companion".
- Email: *@getarcrelay.app forwards to tony@gandalondon.com via ImprovMX (second account, Tony's personal Gmail login). DNS records in Vercel.
- Map data: MetaForge (metaforge.app). Map images allowed with credit "at the bottom of every page" (Discord ticket #2061, 1 Nov 2026). `www/data-bluegate.js` (markers), `www/data-bluegate-places.js` (28 named areas, fitted with `tools/places/`).

## Latest app state (1.0.66)
Voice: Supertonic offline voices (F Sophie, Amy, Ava, Maya, Ivy; M Adam, Ben, Owen, Leo, Mark), on-device speech recognition with a one-tap offline pack download, "Hey Relay" wake phrase (sherpa-onnx keyword spotter), one 8-second follow-up listen then standby. Map: inset tile, amber buttons top right (Full map, Set location, Show route when there's a route), two-step pin (Set location, tap, "I'm here"; hollow ring until confirmed; a confirmed pin replaces a spoken location). Start animation: Android reports where it drew the icon, the lines drop out of the circle, then the screen appears.

Since 1.0.66 (4 Nov, 1.0.67): answer headline with a map is fixed 48 px, three lines max, in a fixed box, and the context line always holds its line, so the map never moves. Place names no longer vanish after a small pinch.

## Needs Tony (on the Pixel)
- Cold-launch the app and check the start animation lines up and drops cleanly (1.0.65+).
- Test the pin flow in a raid (1.0.66).
- "Hey Relay" with game audio playing: false triggers or misses?
- Take a real screenshot with the map (for a third Play screenshot later; no Play changes until all maps are in).
- Reply from MetaForge on the marker data (below).

## Next: all the other maps (one map per day, fresh chat each)
Maps (7): Dam Battlegrounds, Buried City, Spaceport, Blue Gate (done), Stella Montis, Riven Tides (Apr 2026), Pendola Pass (8 Oct 2026, largest). MetaForge has all seven (metaforge.app/arc-raiders/map/<id>: dam, buried-city, spaceport, blue-gate, stella-montis, riven-tides, pendola-pass).
Blocked on: MetaForge permission for their MARKER data (exits, hatches, quests, named areas), not just the map images. Tony is asking on the Discord ticket whether there's an export or API to use. Do not bulk-pull their data before they say yes.
Step 1 (tiles and transform) is DONE for all six (4 Nov): `www/data-<map>.js`, read from MetaForge's live map config. Tile size, max zoom, tile bounds and pan limits are now per map (Dam and Stella Montis use 256 px tiles; Pendola Pass tops out at zoom 4; Stella Montis tiles are {z}/{x}_{y} and only its "default" floor layer is in). bounds/maxBounds are the whole image until markers arrive.
Per map (Blue Gate is the template; roughly a day each):
1. Tiles and coordinate transform (quick).
2. Markers: exits, hatches, quest spots, ARC.
3. Named places for "where are you?" (slowest; check if MetaForge has area labels first).
4. Quest steps and items for that map, checked against two guides.
5. Tests, like Blue Gate's.
Then: work out which map you're on from a spoken landmark (unique name: switch; ambiguous: "Which map?"; keep it for the raid). Order: the map Tony plays most after Blue Gate first, Pendola Pass last.

## Other to-dos (smaller)
- Play packaging: a signed AAB with an upload key (like Sniff). App label on the phone is now "ArcRelay" (1.0.68), matching Play and the site. Wake phrase stays "Hey Relay".
- Site feedback form doesn't send (only worked in the Claude preview). ImprovMX refuses Brevo mail; find another free route.
- Style guide Gaps section: 75% cream secondary text, 44 px map buttons, "Maps by MetaForge" vs "Map: MetaForge" wording, leftover `.gkey input` styles.
- Block taps outside the playable area if MetaForge publishes a boundary.
- Estimates only: screen-off listening, live exit status. Loot tiers: parked (Tony, 4 Nov). MetaForge only has 8 loot zone points on Blue Gate anyway.
- Idea agreed in principle: keep the map tile on screen on standby once the map is known, with a map picker inside it before that (also answers "Which map?"). No new icon next to the mic.
