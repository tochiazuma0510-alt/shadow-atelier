#!/usr/bin/env node
/*
 * Independent replay of the sealed grade-one MEMBER result.  This file is
 * intentionally self-contained: it does not import a producer or any of its
 * packing/reduction helpers.
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const MARKER = "R07_GRADE1_MEMBER_RESULT_REPLAY_V1_PASS";
const SCHEMA = "d972.r07.a0.first-rung-grade1.decision.v2";
const V2_SHA256 = "5a445cf9a263c1968c004f04227d9f5bd5349e433f4dfd8776af80b1d53d9748";
const V3_SHA256 = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff";
const WIDTH = 24192;
const PACKED = 6048;
const BASIS_ROWS = 5044;
const OLD_RANKS = [505, 503, 503, 503];
const BLOCK_RANKS = [1509, 1512, 1512, 1512];
const OLD_COUNT = 2014;
const BLOCK_COUNT = 6045;
const HEX64 = /^[0-9a-f]{64}$/i;

function fail(message) { throw new Error(message); }
function sha256(data) { return crypto.createHash("sha256").update(data).digest("hex"); }
function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, "utf8")); }
  catch (e) { fail(`json:${path.basename(file)}:${e.message}`); }
}
function integer(value, name) {
  if (!Number.isInteger(value)) fail(`integer:${name}`);
  return value;
}
function digest(value, name) {
  if (typeof value !== "string" || !HEX64.test(value)) fail(`digest:${name}`);
  return value.toLowerCase();
}
function same(actual, expected, name) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) fail(`mismatch:${name}`);
}
function receipt(body, key, expectedRows, expectedWidth) {
  const r = body[key];
  if (!r || typeof r !== "object") fail(`receipt:${key}`);
  if (typeof r.file !== "string" || !r.file || path.basename(r.file) !== r.file) fail(`receipt_file:${key}`);
  integer(r.bytes, `${key}.bytes`);
  if (r.bytes !== expectedRows * expectedWidth / 4) fail(`receipt_size:${key}`);
  digest(r.sha256, `${key}.sha256`);
  if (r.rows !== expectedRows || r.width !== expectedWidth) fail(`receipt_shape:${key}`);
  if (r.encoding !== "base3-four-trits-per-byte") fail(`receipt_encoding:${key}`);
  return r;
}
function fileFor(dir, name, r) {
  if (r.file !== name) fail(`receipt_name:${name}`);
  const file = path.join(dir, name);
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) fail(`missing:${name}`);
  return file;
}

// Four low-order base-3 digits are stored in each byte.
const POW = [1, 3, 9, 27];
function trit(byte, digit) { return Math.floor(byte / POW[digit]) % 3; }
function pack4(a, b, c, d) { return a + 3 * b + 9 * c + 27 * d; }
const FIRST = new Int8Array(81);
FIRST.fill(-1);
for (let b = 1; b <= 80; b++) {
  for (let d = 0; d < 4; d++) if (trit(b, d) !== 0) { FIRST[b] = d; break; }
}
const SUB = [null, Array.from({ length: 81 }, () => new Uint8Array(81)), Array.from({ length: 81 }, () => new Uint8Array(81))];
const ADD = [null, Array.from({ length: 81 }, () => new Uint8Array(81)), Array.from({ length: 81 }, () => new Uint8Array(81))];
for (let c = 1; c <= 2; c++) for (let a = 0; a <= 80; a++) for (let b = 0; b <= 80; b++) {
  SUB[c][a][b] = pack4(...POW.map((_, d) => (trit(a, d) - c * trit(b, d) + 30) % 3));
  ADD[c][a][b] = pack4(...POW.map((_, d) => (trit(a, d) + c * trit(b, d)) % 3));
}

function decodePacked(bytes, width, name) {
  if (bytes.length !== width / 4) fail(`packed_size:${name}`);
  const out = Buffer.alloc(width);
  for (let i = 0; i < bytes.length; i++) {
    const b = bytes[i];
    if (b > 80) fail(`noncanonical_byte:${name}:${i}`);
    for (let d = 0; d < 4; d++) out[4 * i + d] = trit(b, d);
  }
  return out;
}
function packedSupports(bytes) {
  const out = [];
  for (let i = 0; i < bytes.length; i++) if (bytes[i] !== 0) out.push(i);
  return out;
}
function tritSupport(decoded) {
  let n = 0;
  for (const x of decoded) if (x !== 0) n++;
  return n;
}
function checkPacked(bytes, name) {
  for (let i = 0; i < bytes.length; i++) if (bytes[i] > 80) fail(`noncanonical_byte:${name}:${i}`);
}
function parseArgs(argv) {
  if (argv.length === 1 && argv[0] === "--selftest") return { selftest: true };
  if (argv.length !== 2 && argv.length !== 4) fail("usage: --candidate DIR [--residual FILE]");
  if (argv[0] !== "--candidate" || (argv.length === 4 && argv[2] !== "--residual")) fail("usage: --candidate DIR [--residual FILE]");
  return { candidate: path.resolve(argv[1]), residual: argv.length === 4 ? path.resolve(argv[3]) : undefined };
}

function selftest() {
  const basis = Buffer.from([1, 0]); // e0 in width eight
  const twoE0 = Buffer.from([2, 0]);
  const zero = Buffer.from([0, 0]);
  const scaled = Buffer.from([SUB[2][twoE0[0]][basis[0]], SUB[2][twoE0[1]][basis[1]]]);
  if (!scaled.equals(zero)) fail("selftest:coefficient_two");
  const nonzero = Buffer.from([0, 1]);
  if (nonzero.equals(zero)) fail("selftest:nonzero_remainder");
  const before = sha256(zero);
  const mutated = Buffer.from(zero); mutated[0] = 1;
  if (sha256(mutated) === before) fail("selftest:mutated_hash");
  // Also exercise canonical-byte rejection without allocating a production row.
  try { checkPacked(Buffer.from([81]), "selftest"); fail("selftest:byte_rejection"); }
  catch (e) { if (!String(e.message).startsWith("noncanonical_byte")) throw e; }
  return { marker: MARKER, selftest: "PASS", coefficient_two: "PASS", zero_remainder: "PASS", nonzero_remainder: "PASS", mutated_hash_rejection: "PASS" };
}

function replay(candidate, residualPath) {
  if (!fs.existsSync(candidate) || !fs.statSync(candidate).isDirectory()) fail("candidate_dir");
  const entries = fs.readdirSync(candidate);
  if (entries.length !== 4 || entries.some((n) => !fs.statSync(path.join(candidate, n)).isFile()) || !entries.includes("decision-v2.HEAD")) fail("candidate_must_have_exactly_four_files");
  const headPath = path.join(candidate, "decision-v2.HEAD");
  const head = readJson(headPath);
  if (head.schema !== `${SCHEMA}.head` || head.stem !== "decision-v2") fail("head_schema");
  const bodySha = digest(head.body_sha256, "head.body_sha256");
  const bodyName = `decision-v2.${bodySha}.json`;
  if (!entries.includes(bodyName)) fail("head_body_missing");
  const bodyPath = path.join(candidate, bodyName);
  const bodyRaw = fs.readFileSync(bodyPath);
  if (sha256(bodyRaw) !== bodySha) fail("head_body_hash");
  const body = readJson(bodyPath);

  if (body.schema !== SCHEMA || body.phase !== "decision" || body.terminal !== "GRADE1_DECISION_MEMBER") fail("schema_or_terminal");
  if (body.producer_sha256 !== V2_SHA256 || body.v3_producer_sha256 !== V3_SHA256) fail("producer_hash");
  digest(body.prepare_sha256, "prepare_sha256");
  if (!Array.isArray(body.block_sha256) || body.block_sha256.length !== 4) fail("block_sha256");
  for (let i = 0; i < 4; i++) digest(body.block_sha256[i], `block_sha256[${i}]`);
  integer(body.logical_cursor, "logical_cursor");
  if (body.logical_cursor !== 8059) fail("logical_cursor");
  same(body.old_ranks, OLD_RANKS, "old_ranks");
  same(body.block_ranks, BLOCK_RANKS, "block_ranks");
  if (body.old_logical_count !== OLD_COUNT || body.block_logical_count !== BLOCK_COUNT) fail("logical_counts");
  if (body.lower_offer_count !== OLD_COUNT || body.lower_rank !== 1661) fail("lower_counts");
  if (body.grade_offer_count !== 6398 || body.grade_rank !== BASIS_ROWS) fail("grade_counts");

  const basisReceipt = receipt(body, "basis_receipt", BASIS_ROWS, WIDTH);
  const remainderReceipt = receipt(body, "remainder_receipt", 1, WIDTH);
  const residualReceipt = receipt(body, "residual_receipt", 1, WIDTH);
  if (residualReceipt.bytes !== PACKED) fail("residual_size");
  const basisName = basisReceipt.file;
  const remainderName = remainderReceipt.file;
  const basisPath = fileFor(candidate, basisName, basisReceipt);
  const remainderPath = fileFor(candidate, remainderName, remainderReceipt);
  if (basisName === remainderName || basisName === "decision-v2.HEAD" || remainderName === "decision-v2.HEAD" || basisName === bodyName || remainderName === bodyName) fail("receipt_file_collision");
  const basis = fs.readFileSync(basisPath);
  const remainder = fs.readFileSync(remainderPath);
  if (basis.length !== basisReceipt.bytes || sha256(basis) !== basisReceipt.sha256.toLowerCase()) fail("basis_receipt_auth");
  if (remainder.length !== remainderReceipt.bytes || sha256(remainder) !== remainderReceipt.sha256.toLowerCase()) fail("remainder_receipt_auth");
  checkPacked(basis, "basis"); checkPacked(remainder, "remainder");

  if (!Array.isArray(body.grade_pivot_leads) || body.grade_pivot_leads.length !== BASIS_ROWS) fail("basis_leads_shape");
  const seenLeads = new Set();
  for (let row = 0; row < BASIS_ROWS; row++) {
    const declared = integer(body.grade_pivot_leads[row], `grade_pivot_leads[${row}]`);
    if (declared < 0 || declared >= WIDTH || seenLeads.has(declared)) fail(`basis_lead:${row}`);
    seenLeads.add(declared);
    const offset = row * PACKED;
    let actual = -1;
    for (let j = 0; j < PACKED; j++) {
      const b = basis[offset + j];
      if (b !== 0) { actual = 4 * j + FIRST[b]; break; }
    }
    if (actual !== declared || trit(basis[offset + Math.floor(declared / 4)], declared % 4) !== 1) fail(`basis_normalization:${row}`);
  }

  if (!Array.isArray(body.member_coefficients) || body.member_coefficients.length === 0) fail("member_coefficients_empty");
  const seenPivots = new Set();
  // Sum the selected basis rows independently to reconstruct the target.
  const reconstructed = Buffer.alloc(PACKED);
  for (let k = 0; k < body.member_coefficients.length; k++) {
    const pair = body.member_coefficients[k];
    if (!Array.isArray(pair) || pair.length !== 2) fail(`coefficient_shape:${k}`);
    const pivot = integer(pair[0], `coefficient[${k}].pivot`);
    const coefficient = integer(pair[1], `coefficient[${k}].value`);
    if (pivot < 0 || pivot >= BASIS_ROWS || seenPivots.has(pivot) || (coefficient !== 1 && coefficient !== 2)) fail(`coefficient_range:${k}`);
    seenPivots.add(pivot);
    const offset = pivot * PACKED;
    for (let j = 0; j < PACKED; j++) reconstructed[j] = ADD[coefficient][reconstructed[j]][basis[offset + j]];
  }
  const reconstructedDense = decodePacked(reconstructed, WIDTH, "reconstructed");
  if (sha256(reconstructed) !== residualReceipt.sha256.toLowerCase()) fail("reconstructed_residual_packed_hash");
  if (sha256(reconstructedDense) !== digest(body.residual_sha256, "residual_sha256")) fail("reconstructed_residual_dense_hash");
  let replayMode = "DIGEST_BOUND_PASS";
  if (residualPath !== undefined) {
    if (!fs.existsSync(residualPath) || !fs.statSync(residualPath).isFile()) fail("residual_missing");
    if (path.basename(residualPath) !== residualReceipt.file) fail("residual_name");
    const residual = fs.readFileSync(residualPath);
    if (residual.length !== residualReceipt.bytes || sha256(residual) !== residualReceipt.sha256.toLowerCase()) fail("residual_receipt_auth");
    checkPacked(residual, "residual");
    if (!residual.equals(reconstructed)) fail("residual_reconstruction_bytes");
    const residualDense = decodePacked(residual, WIDTH, "residual");
    if (sha256(residualDense) !== digest(body.residual_sha256, "residual_sha256")) fail("residual_dense_hash");
    const work = Buffer.from(residual);
    for (let k = 0; k < body.member_coefficients.length; k++) {
      const pivot = body.member_coefficients[k][0];
      const coefficient = body.member_coefficients[k][1];
      const offset = pivot * PACKED;
      for (let j = 0; j < PACKED; j++) work[j] = SUB[coefficient][work[j]][basis[offset + j]];
    }
    if (!work.equals(remainder)) fail("replay_remainder_bytes");
    replayMode = "EXACT_FILE_PASS";
  }
  const remainderDense = decodePacked(remainder, WIDTH, "remainder");
  const remainderSha = sha256(remainder);
  if (remainderSha !== digest(body.remainder_sha256, "remainder_sha256")) fail("remainder_hash");
  const support = tritSupport(remainderDense);
  const packedSupport = packedSupports(remainder);
  if (body.remainder_support !== support) fail("remainder_support");
  same(body.remainder_packed_support, packedSupport, "remainder_packed_support");
  if (support !== 0 || packedSupport.length !== 0) fail("member_not_zero");

  return {
    basis_rows: BASIS_ROWS,
    basis_bytes: basis.length,
    basis_sha256: basisReceipt.sha256.toLowerCase(),
    block_sha256: body.block_sha256.map((x) => x.toLowerCase()),
    block_ranks: BLOCK_RANKS,
    block_logical_count: BLOCK_COUNT,
    cursor: body.logical_cursor,
    grade_offers: body.grade_offer_count,
    grade_rank: body.grade_rank,
    lower_offers: body.lower_offer_count,
    lower_rank: body.lower_rank,
    marker: MARKER,
    old_ranks: OLD_RANKS,
    old_logical_count: OLD_COUNT,
    prepare_sha256: body.prepare_sha256.toLowerCase(),
    producer_sha256: body.producer_sha256.toLowerCase(),
    replay: replayMode,
    remainder_bytes: remainder.length,
    residual_packed_sha256: residualReceipt.sha256.toLowerCase(),
    residual_sha256: body.residual_sha256.toLowerCase(),
    residual_bytes: residualReceipt.bytes,
    remainder_sha256: remainderSha,
    remainder_support: support,
    selected_coefficients: body.member_coefficients.length,
    status: "PASS",
    terminal: body.terminal,
    v3_producer_sha256: body.v3_producer_sha256.toLowerCase(),
    width: WIDTH,
    packed_row_length: PACKED
  };
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const verdict = args.selftest ? selftest() : replay(args.candidate, args.residual);
    process.stdout.write(`${JSON.stringify(verdict)}\n`);
    return 0;
  } catch (e) {
    process.stderr.write(`${JSON.stringify({ marker: MARKER, status: "REJECTED", error: String(e.message || e) })}\n`);
    return 1;
  }
}
process.exitCode = main();
