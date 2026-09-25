/**
 * Worker engine: list, host, join, and the private passphrase gate.
 * Author: Aziel Eliab only.
 */
import {
  handleNew,
  importExport,
  resetAzchatStore,
  roomHost,
  roomJoin,
  roomList,
  roomOpen,
  roomPost,
  roomPull,
} from "../workers/download-tracker/src/engine.js";

const SECRET = "correct-horse-battery-staple";

function assert(cond, message) {
  if (!cond) throw new Error(message);
}

function blob(value) {
  return JSON.stringify(value);
}

resetAzchatStore();
const host = await handleNew({ label: "host" });
const guest = await handleNew({ label: "guest" });

const missing = await roomHost({ token: host.token, title: "quiet", private: true });
assert(missing.ok === false && missing.error === "passphrase-required", "private host without passphrase");
assert(roomList().count === 0, "failed host must not list");

const dropped = await roomHost({ token: host.token, title: "quiet", passphrase: SECRET });
assert(dropped.ok === false && dropped.error === "private-flag-required", "passphrase without private flag");

const hosted = await roomHost({ token: host.token, title: "quiet", private: true, passphrase: SECRET });
assert(hosted.ok === true && hosted.listed === true && hosted.e2e === false, "private host");
assert(!blob(hosted).includes(SECRET), "host response leaked passphrase");
assert(!blob(hosted).includes("passphrase_hash"), "host response leaked verifier");

const listed = roomList();
const card = listed.rooms.find((room) => room.room_id === hosted.room_id);
assert(card && card.private === true && card.passphrase_required === true && card.entry === "passphrase", "private card");
assert(!blob(listed).includes(SECRET), "list leaked passphrase");
assert(!blob(listed).includes("passphrase_hash") && !blob(listed).includes("passphrase_salt"), "list leaked verifier");

const noPass = await roomJoin({ token: guest.token, room_id: hosted.room_id });
assert(noPass.ok === false && noPass.status === 403 && noPass.error === "passphrase-required", "missing passphrase");
const wrong = await roomJoin({ token: guest.token, room_id: hosted.room_id, passphrase: "not-the-passphrase" });
assert(wrong.ok === false && wrong.status === 403 && wrong.error === "passphrase-rejected", "wrong passphrase");
assert(!blob(wrong).includes("not-the-passphrase"), "wrong passphrase echoed");
const stranger = await roomPull({ token: guest.token, room_id: hosted.room_id });
assert(stranger.ok === false && stranger.status === 404, "stranger pull after failed join");
assert((await roomPost({ token: guest.token, room_id: hosted.room_id, text: "no" })).status === 404, "stranger post");

const joined = await roomJoin({ token: guest.token, room_id: hosted.room_id, passphrase: SECRET });
assert(joined.ok === true && joined.joined === true, "join with passphrase");
assert(!blob(joined).includes(SECRET), "join response leaked passphrase");
assert((await roomPost({ token: guest.token, room_id: hosted.room_id, text: "inside" })).ok === true, "member post");

const pub = await roomHost({ token: host.token, title: "hall", private: false });
assert(pub.ok === true, "public host");
const guest2 = await handleNew({ label: "guest-2" });
assert((await roomJoin({ token: guest2.token, room_id: pub.room_id })).ok === true, "public join");
const again = roomList();
assert(again.rooms.some((room) => room.room_id === pub.room_id && room.private === false), "public room listed");

const pairA = await handleNew({ label: "a" });
const pairB = await handleNew({ label: "b" });
const pair = await roomOpen({ token_a: pairA.token, token_b: pairB.token });
assert(!roomList().rooms.some((room) => room.room_id === pair.room_id), "pairwise room listed");
const sneak = await roomJoin({ token: guest.token, room_id: pair.room_id });
assert(sneak.ok === false && sneak.status === 404, "unlisted join");

const dumped = importExport({ mode: "export" });
const dump = blob(dumped);
assert(!dump.includes(SECRET) && !dump.includes("passphrase_hash") && !dump.includes("passphrase_salt"), "export leaked");

console.log("worker room gate ok");
