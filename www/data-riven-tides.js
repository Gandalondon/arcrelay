/* Riven Tides map from MetaForge (metaforge.app/arc-raiders/map/riven-tides), read 4 Nov 2026.
   Tiles and transform only. Markers wait for MetaForge's go-ahead on their marker data.
   bounds and maxBounds are the whole image for now; tighten to the playable area once markers are in. */
window.RIVEN_TIDES = {
  id: "riven-tides",
  name: "Riven Tides",
  tiles: "https://static.metaforge.app/arc-raiders/maps/riven-tides/20260428-q85/{z}/{x}/{y}.webp",
  transform: [0.03125,  0,  0.03125,  0],
  tileSize: 512,
  maxNativeZoom: 5,
  tileBounds: [[0,  0],  [16352,  16352]],
  bounds: [[0,  0],  [16352,  16352]],
  maxBounds: [[-1635,  -1635],  [17987,  17987]],
  rows: []
};
