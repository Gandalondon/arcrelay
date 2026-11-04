/* Pendola Pass map from MetaForge (metaforge.app/arc-raiders/map/pendola-pass), read 4 Nov 2026.
   Tiles and transform only. Markers wait for MetaForge's go-ahead on their marker data.
   bounds and maxBounds are the whole image for now; tighten to the playable area once markers are in.
   Note: tiles only go to zoom 4 here (5 on the other maps). */
window.PENDOLA_PASS = {
  id: "pendola-pass",
  name: "Pendola Pass",
  tiles: "https://static.metaforge.app/arc-raiders/maps/pendola-pass/20261005b-satellite/{z}/{x}/{y}.webp",
  transform: [0.03125,  0,  0.03125,  0],
  tileSize: 512,
  maxNativeZoom: 4,
  tileBounds: [[3162,  626],  [13220,  15758]],
  bounds: [[3162,  626],  [13220,  15758]],
  maxBounds: [[2156,  -887],  [14226,  17271]],
  rows: []
};
