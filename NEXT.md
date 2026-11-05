# ArcRelay: where we are (end of Wednesday 4 November 2026)

Start a new conversation by reading this file. It replaces the long 4 Nov chat.

## The project in one paragraph
ArcRelay is Tony Goff-Yu's free, unofficial, voice-first Android companion for ARC Raiders (Pixel 9). Ask out loud ("Hey Relay" or tap), it answers out loud and shows a map: nearest exit, quest steps, items, "not that one" rerouting. Everything runs on the phone. Blue Gate only so far. Rules: £0 to run (no paid services or keys), UK English, no em dashes, no widows, palette charcoal #1C1E22 / panel #26282D / ink #15171C / cream #EEE8DC / amber #F2B33D, Barlow, Material Symbols Rounded only. Push to main when Tony says push or has approved the work. The style guide is the rulebook: `src/docs/style-guide.html`.

## Where things are
- Site copy (5 Nov): Google Doc "ArcRelay site copy" in Drive Claude/ArcRelay, every page of getarcrelay.app: https://docs.google.com/document/d/19BOlsHoYCjPqrISH58HC7CALxmGhzDompAL2HYUgYyw/edit . Tony edits there; copy changes go from the doc to the site, and any wording changed on the site goes back into the doc. Site only, not the app.
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
- Start animation: 1.0.65 launcher-icon match undone 4 Nov (logo shrank and jumped after Android's splash); back to the splash-matched 1.0.64 version. Check it on the Pixel.
- Test the pin flow in a raid (1.0.66).
- "Hey Relay" with game audio playing: false triggers or misses?
- Take a real screenshot with the map (for a third Play screenshot later; no Play changes until all maps are in).
- Reply from MetaForge on the marker data (below).

## Next: all the other maps (one map per day, fresh chat each)
Maps (7): Dam Battlegrounds, Buried City, Spaceport, Blue Gate (done), Stella Montis, Riven Tides (Apr 2026), Pendola Pass (8 Oct 2026, largest). MetaForge has all seven (metaforge.app/arc-raiders/map/<id>: dam, buried-city, spaceport, blue-gate, stella-montis, riven-tides, pendola-pass).
MetaForge OK'd using their data (Tony, 4 Nov evening), with credit. DONE 4 Nov: loot zone outlines and region / loot-zone / landmark names for all seven maps in `www/data-zones.js` (from their map config chunk, read through Chrome; the workspace can't reach metaforge.app, so files come via Tony's Downloads). Zones are drawn on the map. Still to pull: the markers (exits, hatches, quest spots, ARC) for the six new maps.
Step 1 (tiles and transform) is DONE for all six (4 Nov): `www/data-<map>.js`, read from MetaForge's live map config. Tile size, max zoom, tile bounds and pan limits are now per map (Dam and Stella Montis use 256 px tiles; Pendola Pass tops out at zoom 4; Stella Montis tiles are {z}/{x}_{y} and only its "default" floor layer is in). bounds/maxBounds are the whole image until markers arrive.
Per map (Blue Gate is the template; roughly a day each):
1. Tiles and coordinate transform (quick).
2. Markers: exits, hatches, quest spots, ARC.
3. Named places for "where are you?": MetaForge's labels are now in `www/data-zones.js` (regions, loot zones, landmarks), so this step is mostly data wiring, not fitting.
4. Quest steps and items for that map, checked against two guides.
5. Tests, like Blue Gate's.
Then: work out which map you're on from a spoken landmark (unique name: switch; ambiguous: "Which map?"; keep it for the raid). Order: the map Tony plays most after Blue Gate first, Pendola Pass last.

## Onboarding (agreed 4 Nov, not built yet)
Mockup: https://claude.ai/artifact/LaZfxhucnGwofdQdHAVK9d . Four screens, no Skip, each heading / body / visual, headlines two lines, dots centred with a full-width button under them:
1. "Say “Hey Relay”." Listening mic (static, with halo).
2. "Find what you need." Nearest Rocketeer map (items, enemies, spawns; not quests for now).
3. "Find the nearest exit." Evac on open ground, no zones, line in a different direction to screen 2.
4. "Pick Relay’s voice." Voice rows (name + Female/Male, no "Supertonic"), Skip (outline, 1/3) + Download (amber, 2/3) like Sniff's Back/Next.
Also: Settings voice row says "Offline. Tap to change." (drop "Supertonic"; credit stays in About).

## Other to-dos (smaller)
- Play packaging: a signed AAB with an upload key (like Sniff). App label on the phone is now "ArcRelay" (1.0.68), matching Play and the site. Wake phrase stays "Hey Relay".
- Site feedback form doesn't send (ImprovMX refuses Brevo mail). Parked by Tony (4 Nov): using the app first.
- Style guide Gaps: done 4 Nov (48 px map buttons, "Maps by MetaForge" everywhere, dead `.gkey input` styles gone, names under the map buttons hidden). 75% cream secondary text kept as the one exception.
- Block taps outside the playable area if MetaForge publishes a boundary.
- Estimates only: screen-off listening, live exit status. Loot tiers: parked (Tony, 4 Nov). MetaForge only has 8 loot zone points on Blue Gate anyway.
- Idea agreed in principle: keep the map tile on screen on standby once the map is known, with a map picker inside it before that (also answers "Which map?"). No new icon next to the mic.
