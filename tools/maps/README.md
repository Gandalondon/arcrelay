# Map data tools (5 Nov 2026)

How the seven maps' markers, places and quests were built. Run from this folder with `node`.

- `source/raw-<map>.txt`: MetaForge markers as read through Chrome (packed: ARC rows grouped by type). `node unpack.js <map>` rebuilds `source/rows-<map>.json` and prints the checksum to compare with the page.
- Markers into `www/data-<map>.js`: rows from `source/rows-<map>.json` (done by hand per map, see NEXT.md step 2 for the filter and bounds rule).
- `node genplaces.js`: `www/data-<map>-places.js` for the five newer maps (MetaForge labels in `www/data-zones.js` plus the spoken short forms in the script). `node damplaces.js` does Dam's.
- `node genq.js <map> <research files>`: `www/data-<map>-quests.js` from the quest research in `source/` (Dam: no arguments, uses q1 to q3). It checks every pin against the map's markers and drops risky spoken names.
- Then `node ../../tests/maps.js` and `node ../../tests/run.js`.
- `node genloot.js`: `www/data-loot.js` (loot spots, 6 Nov) from `source/loot.json`, MetaForge's nature and container markers for all seven maps, read from each map page in Chrome (the page keeps them in its WebGL layer as `markerData`). Same coordinates as the other markers.
