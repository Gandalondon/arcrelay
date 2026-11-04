/* Spaceport map from MetaForge (metaforge.app/arc-raiders/map/spaceport), read 4 Nov 2026.
   Tiles and transform only. Markers wait for MetaForge's go-ahead on their marker data.
   bounds and maxBounds are the whole image for now; tighten to the playable area once markers are in. */
window.SPACEPORT = {
  id: "spaceport",
  name: "Spaceport",
  tiles: "https://static.metaforge.app/arc-raiders/maps/spaceport/20260114-q85/{z}/{x}/{y}.webp",
  transform: [0.05754430970149254,  0.41474755130596463,  0.057570375981248076,  4.204424533065776],
  tileSize: 512,
  maxNativeZoom: 5,
  tileBounds: [[-73.03,  -7.21],  [8803.06,  8872.91]],
  bounds: [[-73.03,  -7.21],  [8803.06,  8872.91]],
  maxBounds: [[-961,  -895],  [9691,  9761]],
  rows: []
};
