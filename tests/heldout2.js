/* Second held-out set, written 6 Nov BEFORE the fixes for the first set's misses, and never tuned against.
   Run: SET=heldout2 node tests/run.js. Scores how well the fixes generalise, not whether they fixed known sentences. */
const HTR = { quest: "Home to Roost", step: 3 }, HTR5 = { quest: "Home to Roost", step: 5 }, NONE = {}, AT = { place: "Village" };
module.exports = [
  /* moving on */
  { set: HTR, say: "right, that's done", want: { advance: true } },
  { set: HTR, say: "okay got it, what next", want: { advance: true } },
  { set: HTR, say: "sweet, next", want: { advance: true } },
  { set: HTR, say: "I'm in, now what", want: { advance: true } },
  { set: HTR5, say: "read them", want: { advance: true } },
  /* repeat */
  { set: HTR, say: "sorry what was that", want: { same: true } },
  { set: HTR, say: "say it one more time", want: { same: true } },
  { set: HTR, say: "where am I going again", want: { same: true } },
  /* way out */
  { set: HTR, say: "I need to leave now", want: { exit: true } },
  { set: HTR, say: "how do I get out of here", want: { exit: true } },
  { set: AT, say: "time to go home", want: { exit: true } },
  { set: HTR, say: "I'm dying, nearest extract", want: { exit: true } },
  { set: AT, say: "get me out", want: { exit: true } },
  /* raid events */
  { set: HTR, say: "they got me", want: { died: true } },
  { set: HTR, say: "I'm dead", want: { died: true } },
  { set: HTR, say: "just loaded into a new match", want: { newraid: true } },
  { set: HTR, say: "made it out alive", want: { extracted: true } },
  { set: HTR, say: "extracted safely", want: { extracted: true } },
  /* quests and steps */
  { set: NONE, say: "home to roost, the locker room bit", want: { quest: "Home to Roost", step: 3 } },
  { set: NONE, say: "doing roost, I need the hidden key", want: { quest: "Home to Roost", step: 6 } },
  { set: HTR, say: "I'm at step four", want: { quest: "Home to Roost", step: 4 } },
  { set: NONE, say: "I'm doing the frigate", want: { quest: "Boarding the Frigate" } },
  /* where I am */
  { set: NONE, say: "I'm by the village", want: { place: "Village" } },
  /* signing off */
  { set: HTR, say: "cheers mate", want: { stop: true } },
  { set: HTR, say: "that's me, thanks", want: { stop: true } }
];
