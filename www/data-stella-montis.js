/* Stella Montis map from MetaForge (metaforge.app/arc-raiders/map/stella-montis), read 4 Nov 2026.
   Tiles and transform only. Markers wait for MetaForge's go-ahead on their marker data.
   bounds and maxBounds are the whole image (maxBounds exactly, so zooming out never shows past its edge); tighten to the playable area once markers are in.
   Note: tile paths are {z}/{x}_{y} (not {z}/{x}/{y}), and this is the "default" floor layer.
   Stella Montis is multi-level; other floors may need their own layer later. */
window.STELLA_MONTIS = {
  id: "stella-montis",
  name: "Stella Montis",
  tiles: "https://static.metaforge.app/arc-raiders/maps/stella-montis/v3/default/{z}/{x}_{y}.webp",
  transform: [0.0352558095952024,  -13.055565967016491,  0.03522865853658536,  -7.731432926829257],
  tileSize: 256,
  maxNativeZoom: 5,
  tileBounds: [[219.46,  370.31],  [7457.89,  7603.16]],
  bounds: [[219.46,  370.31],  [7457.89,  7603.16]],
  maxBounds: [[219.46,  370.31],  [7457.89,  7603.16]],
  rows: []
};
