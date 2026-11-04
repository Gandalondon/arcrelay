/* Dam Battlegrounds map from MetaForge (metaforge.app/arc-raiders/map/dam), read 4 Nov 2026.
   Tiles and transform only. Markers wait for MetaForge's go-ahead on their marker data.
   Note: Dam's tiles are 256 px (Blue Gate's are 512). bounds and maxBounds are the whole image
   for now; tighten them to the playable area once the markers are in. */
window.DAM = {
  id: "dam",
  name: "Dam Battlegrounds",
  tiles: "https://static.metaforge.app/arc-raiders/maps/dam/20260112-q85/{z}/{x}/{y}.webp",
  transform: [0.02899823907870071, -0.5500098883744897, 0.029003656496347927, -0.2453962393344682],
  tileSize: 256,
  maxNativeZoom: 5,
  tileBounds: [[8.46, 18.97], [8800.46, 8812.6]],
  bounds: [[8.46, 18.97], [8800.46, 8812.6]],
  maxBounds: [[8.46, 18.97], [8800.46, 8812.6]],
  rows: []
};
