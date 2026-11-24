// News image entry for Tuesday 24 November 2026 (Node 22, standard library
// only). The poster is entry.png next to this file, drawn by gen_image.py:
// a one-page newspaper front page with the day's six biggest stories.
//
// Before the picture is handed to the judge, this program proves it is a
// whole, well-formed PNG instead of trusting the file on sight. It checks
// the eight-byte magic, reads the size out of the IHDR header, walks every
// chunk and recomputes each chunk's CRC32 against the value stored in the
// file, and refuses anything over the 1 MiB cap or wider or taller than
// 1024 pixels. A file that fails any of those checks stops the run with an
// error; a file that passes is copied byte for byte to /output/entry.png.
//
// To try the copy outside the grader, point MAKEFUN_OUTPUT_DIR at a folder
// of your own, for example:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

// The eight bytes every PNG file starts with.
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

// The gate's limits for this bounty.
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

// CRC32 (IEEE 802.3), built from the polynomial 0xEDB88320.
const CRC_TABLE: number[] = [];
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) {
    c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  }
  CRC_TABLE[n] = c >>> 0;
}

function crc32(bytes: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function fail(message: string): never {
  throw new Error(`entry.png rejected: ${message}`);
}

const picture = readFileSync(new URL("./entry.png", import.meta.url));

if (picture.length > MAX_BYTES) {
  fail(`it is ${picture.length} bytes, over the ${MAX_BYTES} byte cap`);
}
if (picture.length < 8 || !picture.subarray(0, 8).equals(PNG_MAGIC)) {
  fail("its first eight bytes are not the PNG signature");
}

// The IHDR chunk comes first: 4 bytes of length, 4 of type, then the
// 13-byte header. Width and height are big-endian 32-bit values.
if (picture.length < 33 || picture.toString("ascii", 12, 16) !== "IHDR") {
  fail("its first chunk is not IHDR");
}
const width = picture.readUInt32BE(16);
const height = picture.readUInt32BE(20);
const bitDepth = picture[24];
const colourType = picture[25];
if (width === 0 || width > MAX_SIDE || height === 0 || height > MAX_SIDE) {
  fail(`it is ${width} by ${height}, over the ${MAX_SIDE} by ${MAX_SIDE} cap`);
}
if (![1, 2, 4, 8, 16].includes(bitDepth)) {
  fail(`its bit depth is ${bitDepth}`);
}
if (![0, 2, 3, 4, 6].includes(colourType)) {
  fail(`its colour type is ${colourType}`);
}

// Walk the chunk chain from offset 8, checking every stored CRC32, until
// the IEND chunk. Nothing may follow IEND.
let offset = 8;
let sawIend = false;
while (offset + 8 <= picture.length) {
  const length = picture.readUInt32BE(offset);
  const type = picture.toString("ascii", offset + 4, offset + 8);
  const dataEnd = offset + 8 + length;
  if (dataEnd + 4 > picture.length) {
    fail(`chunk ${type} runs past the end of the file`);
  }
  const storedCrc = picture.readUInt32BE(dataEnd);
  const checked = Buffer.concat([
    picture.subarray(offset + 4, offset + 8),
    picture.subarray(offset + 8, dataEnd),
  ]);
  if (crc32(checked) !== storedCrc) {
    fail(`chunk ${type} fails its checksum`);
  }
  offset = dataEnd + 4;
  if (type === "IEND") {
    sawIend = true;
    break;
  }
}
if (!sawIend) {
  fail("it has no IEND chunk");
}
if (offset !== picture.length) {
  fail("it has trailing bytes after IEND");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), picture);
console.log(
  `entry.png OK: ${width}x${height}, ${picture.length} bytes, ` +
    `all chunks checksummed, copied to ${outDir}/entry.png`,
);
