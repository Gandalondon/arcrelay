// The scenes, shared by every output. Edit the words here, then re-run capture.js.
module.exports = [
  { id: 'home' },
  { id: 'listening', listen: true },
  { id: 'find', map: 'blue-gate', place: 'Village', ask: 'nearest Bastion' },
  { id: 'exit', map: 'blue-gate', place: 'Village', ask: "I'm under fire, where's the nearest exit" },
  { id: 'loot', map: 'blue-gate', place: 'Village', ask: 'any apricots near me' },
  { id: 'whole', map: 'blue-gate', place: 'Village', ask: 'any apricots near me', click: '#full' },  // portfolio: the whole map
];
module.exports.push({ id: 'quest', map: 'blue-gate', place: 'Village', ask: "I'm on A First Foothold, step 2" });  // homepage: Get help on quests
