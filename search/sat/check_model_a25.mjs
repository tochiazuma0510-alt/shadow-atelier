#!/usr/bin/env node
// search/sat/check_model_a25.mjs
//
// Independent SAT model checker for the n=25, ell=17 2-transitivity
// existence target (search/sat/encode_a25.py, sol/sol_reply_84_math11.md
// sec 6.3). DELIBERATELY DOES NOT import encode_a25.py, shares no helper
// module with it, different language (node vs python) -- searcher/checker
// separation (CLAUDE.md, search/sat/README.md), same discipline as
// check_model_n21.mjs.
//
// Re-derives the X/D/B variable numbering independently (same *design*,
// independently re-typed) purely to be able to READ a kissat
// model_vlines.txt file. Every mathematical property reported
// (involution/cycle type, b=a*u^-1, b^3=1, exactly-one-fixed-point,
// 2-transitivity) is recomputed from the DECODED PERMUTATIONS, never
// trusted from the model's B/TEMP/RNEW/R pair-BFS variables directly.
//
// IMPORTANT: the "2-transitive" check in this checker does its OWN
// UNBOUNDED (iterate-to-fixpoint, no depth cap) BFS over the diagonal
// action of {a,b,b^-1} on ordered pairs, starting from (1,2) -- it does
// NOT read the CNF's depth-bounded R/TEMP/RNEW variables at all. This is
// deliberate: the CNF's depth bound (see encode_a25.py's
// DEFAULT_2TRANS_DEPTH docstring) is REASONED, not PROVEN sufficient, so
// this checker's own from-scratch BFS is the only fully trustworthy
// arbiter of "is the decoded (a,b) actually 2-transitive" for a given
// model -- independent of whatever depth the CNF used.
//
// Usage:
//   node check_model_a25.mjs --mode class --model out/model_vlines.txt
//   node check_model_a25.mjs --mode 2transitive --model out/model_vlines.txt
//   node check_model_a25.mjs --self-test

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const N = 25;

function buildU() {
  const u = new Map();
  for (let i = 1; i <= 16; i++) u.set(i, i + 1);
  u.set(17, 1);
  for (const [a, b] of [[18, 19], [20, 21], [22, 23], [24, 25]]) {
    u.set(a, b);
    u.set(b, a);
  }
  return u;
}
const U = buildU();
const UINV = new Map();
for (const [k, v] of U) UINV.set(v, k);

const PAIRS = [];
for (let i = 1; i <= N; i++) {
  for (let j = i + 1; j <= N; j++) PAIRS.push([i, j]);
}
const PAIR_IDX = new Map();
PAIRS.forEach(([i, j], k) => PAIR_IDX.set(`${i},${j}`, k + 1));
const NUM_PAIRS = PAIRS.length; // 300

const X_BASE = 0;
const X_COUNT = NUM_PAIRS;
function Xvar(i, j) {
  if (i === j) throw new Error("X(i,i) undefined");
  if (i > j) [i, j] = [j, i];
  return X_BASE + PAIR_IDX.get(`${i},${j}`);
}

const D_BASE = X_BASE + X_COUNT;
const D_COUNT = N;
function Dvar(i) {
  return D_BASE + i;
}

const B_BASE = D_BASE + D_COUNT;
const B_COUNT = N * N;
function Bvar(i, k) {
  return B_BASE + (i - 1) * N + k;
}

const CLASS_VAR_COUNT = B_BASE + B_COUNT; // 950
if (CLASS_VAR_COUNT !== 950) throw new Error("internal: CLASS_VAR_COUNT mismatch");

// ---------------------------------------------------------------------
// Model parsing (identical shape to check_model_n21.mjs).
// ---------------------------------------------------------------------

export function parseModelVLines(text) {
  const trueVars = new Set();
  const tokens = [];
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (line.length === 0) continue;
    if (line.startsWith("c")) continue;
    let body = line;
    if (body.startsWith("v")) body = body.slice(1);
    for (const tok of body.trim().split(/\s+/)) {
      if (tok.length === 0) continue;
      const n = Number(tok);
      if (Number.isNaN(n)) continue;
      tokens.push(n);
    }
  }
  for (const lit of tokens) {
    if (lit === 0) continue;
    if (lit > 0) trueVars.add(lit);
  }
  return trueVars;
}

// ---------------------------------------------------------------------
// Decoding.
// ---------------------------------------------------------------------

export function decodeA(trueVars) {
  const a = new Array(N + 1).fill(null);
  const issues = [];
  for (let i = 1; i <= N; i++) {
    const candidates = [];
    for (let j = 1; j <= N; j++) {
      if (j === i) {
        if (trueVars.has(Dvar(i))) candidates.push(i);
        continue;
      }
      if (trueVars.has(Xvar(i, j))) candidates.push(j);
    }
    if (candidates.length !== 1) {
      issues.push(`row ${i}: expected exactly one of X/D true, found ${candidates.length} (${candidates.join(",")})`);
      continue;
    }
    a[i] = candidates[0];
  }
  return { a, issues };
}

export function decodeBFromModel(trueVars) {
  const b = new Array(N + 1).fill(null);
  const issues = [];
  for (let i = 1; i <= N; i++) {
    const candidates = [];
    for (let k = 1; k <= N; k++) {
      if (trueVars.has(Bvar(i, k))) candidates.push(k);
    }
    if (candidates.length !== 1) {
      issues.push(`B row ${i}: expected exactly one B[i][k] true, found ${candidates.length}`);
      continue;
    }
    b[i] = candidates[0];
  }
  return { b, issues };
}

export function recomputeBFromA(a) {
  const b = new Array(N + 1).fill(null);
  for (let i = 1; i <= N; i++) {
    if (a[i] == null) continue;
    b[i] = UINV.get(a[i]);
  }
  return b;
}

// ---------------------------------------------------------------------
// Mathematical property checks, from decoded permutations only.
// ---------------------------------------------------------------------

export function cycleType(perm) {
  const seen = new Array(N + 1).fill(false);
  const lengths = [];
  for (let i = 1; i <= N; i++) {
    if (seen[i]) continue;
    let len = 0;
    let j = i;
    while (!seen[j]) {
      seen[j] = true;
      j = perm[j];
      len++;
      if (j == null) return { ok: false, lengths: null, reason: `perm undefined at ${j}` };
    }
    lengths.push(len);
  }
  lengths.sort((x, y) => x - y);
  return { ok: true, lengths };
}

export function isType2_12_1(perm) {
  const ct = cycleType(perm);
  if (!ct.ok) return { ok: false, reason: ct.reason };
  const want = [1, ...Array(12).fill(2)];
  const got = ct.lengths;
  const match = got.length === want.length && got.every((v, idx) => v === want[idx]);
  return { ok: match, lengths: got, expected: want };
}

export function isType3_8_1(perm) {
  const ct = cycleType(perm);
  if (!ct.ok) return { ok: false, reason: ct.reason };
  const want = [1, ...Array(8).fill(3)];
  const got = ct.lengths;
  const match = got.length === want.length && got.every((v, idx) => v === want[idx]);
  return { ok: match, lengths: got, expected: want };
}

export function permCubeIsIdentity(perm) {
  for (let i = 1; i <= N; i++) {
    let x = i;
    for (let s = 0; s < 3; s++) x = perm[x];
    if (x !== i) return false;
  }
  return true;
}

export function fixedPointCount(perm) {
  let c = 0;
  for (let i = 1; i <= N; i++) if (perm[i] === i) c++;
  return c;
}

export function invertPerm(perm) {
  const inv = new Array(N + 1).fill(null);
  for (let i = 1; i <= N; i++) inv[perm[i]] = i;
  return inv;
}

// UNBOUNDED (iterate-to-fixpoint) BFS on ordered pairs -- does NOT read
// any model TEMP/RNEW/R variable, does NOT use the CNF's depth bound.
// Guaranteed to terminate (state space is finite, 600 pair-vertices) --
// this is a plain orbit-closure computation, not a depth-capped search.
export function twoTransitiveCheck(a, b) {
  const bInv = invertPerm(b);
  const gens = [a, b, bInv];
  const start = "1,2";
  const visited = new Set([start]);
  let frontier = [[1, 2]];
  let rounds = 0;
  const depthOf = new Map([[start, 0]]);
  while (frontier.length > 0) {
    rounds++;
    const next = [];
    for (const [i, j] of frontier) {
      for (const g of gens) {
        const gi = g[i];
        const gj = g[j];
        if (gi === gj) continue; // defensive; should not happen for a genuine permutation
        const key = `${gi},${gj}`;
        if (!visited.has(key)) {
          visited.add(key);
          depthOf.set(key, rounds);
          next.push([gi, gj]);
        }
      }
    }
    frontier = next;
  }
  const trueDiameter = Math.max(...depthOf.values());
  return {
    orbitSize: visited.size,
    twoTransitive: visited.size === N * (N - 1),
    trueBfsDiameterFrom_1_2: trueDiameter,
  };
}

// ---------------------------------------------------------------------
// Top-level check routines.
// ---------------------------------------------------------------------

export function checkClassModel(trueVars) {
  const report = { checks: [], ok: true };
  const record = (name, ok, detail) => {
    report.checks.push({ name, ok, detail });
    if (!ok) report.ok = false;
  };

  const { a, issues: aIssues } = decodeA(trueVars);
  record("a_decodes_to_total_function", aIssues.length === 0, aIssues);
  if (aIssues.length > 0) return report;

  const invCheck = isType2_12_1(a);
  record("a_is_type_2^12_1", invCheck.ok, invCheck);

  const bModel = decodeBFromModel(trueVars).b;
  const bRecomputed = recomputeBFromA(a);
  const bAgrees = bModel.every((v, i) => i === 0 || v === bRecomputed[i]);
  record("model_B_agrees_with_independently_recomputed_b=u^-1(a(.))", bAgrees, {
    model_B: bModel.slice(1),
    recomputed_b: bRecomputed.slice(1),
  });

  const b = bRecomputed; // ground truth for all downstream checks

  const cubeOk = permCubeIsIdentity(b);
  record("b_cubed_equals_identity", cubeOk, {});

  const fpCount = fixedPointCount(b);
  record("b_has_exactly_one_fixed_point", fpCount === 1, { fixed_point_count: fpCount });

  const type381 = isType3_8_1(b);
  record("b_is_type_3^8_1", type381.ok, type381);

  report.decoded = { a: a.slice(1), b: b.slice(1) };
  return report;
}

export function check2TransitiveModel(trueVars) {
  const report = checkClassModel(trueVars);
  if (!report.decoded) return report;
  const a = [null, ...report.decoded.a];
  const b = [null, ...report.decoded.b];
  const trans = twoTransitiveCheck(a, b);
  report.checks.push({
    name: "diagonal_action_on_ordered_pairs_is_2transitive (unbounded BFS, no depth cap)",
    ok: trans.twoTransitive,
    detail: trans,
  });
  if (!trans.twoTransitive) report.ok = false;
  return report;
}

// ---------------------------------------------------------------------
// Self-test using the machine-found witness fixture.
// ---------------------------------------------------------------------

function selfTest() {
  const here = fileURLToPath(new URL(".", import.meta.url));
  const fixturePath = here + "fixtures/witness_a25_2transitive.json";
  const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));

  const aImg = fixture.a_images_1indexed;
  const trueVars = new Set();
  for (let i = 1; i <= N; i++) {
    const ai = aImg[i - 1];
    if (ai === i) trueVars.add(Dvar(i));
    else trueVars.add(Xvar(i, ai));
  }
  const bImg = fixture.b_images_1indexed;
  for (let i = 1; i <= N; i++) {
    trueVars.add(Bvar(i, bImg[i - 1]));
  }

  const uOk = fixture.u_images_1indexed.every((v, idx) => U.get(idx + 1) === v);
  const uInvOk = fixture.uinv_images_1indexed.every((v, idx) => UINV.get(idx + 1) === v);

  const classReport = checkClassModel(trueVars);
  const transReport = check2TransitiveModel(trueVars);

  const twoTransCheck = transReport.checks.find((c) => c.name.startsWith("diagonal_action"));

  const results = {
    fixture_u_matches_checker_u: uOk,
    fixture_uinv_matches_checker_uinv: uInvOk,
    class_report_ok: classReport.ok,
    class_checks: classReport.checks,
    two_transitive_report_ok_expected_true: transReport.ok,
    two_transitive_detail: twoTransCheck?.detail,
    fixture_python_independent_diameter: fixture["python_independent_true_bfs_diameter_from_(1,2)"],
  };

  const pass =
    uOk &&
    uInvOk &&
    classReport.ok === true &&
    transReport.ok === true && // fixture IS 2-transitive
    twoTransCheck.detail.trueBfsDiameterFrom_1_2 === fixture["python_independent_true_bfs_diameter_from_(1,2)"];

  console.log(JSON.stringify({ pass, results }, null, 2));
  process.exit(pass ? 0 : 1);
}

// ---------------------------------------------------------------------
// CLI.
// ---------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  if (args.includes("--self-test")) {
    selfTest();
    return;
  }
  const modeIdx = args.indexOf("--mode");
  const modelIdx = args.indexOf("--model");
  if (modeIdx === -1 || modelIdx === -1) {
    console.error(
      "usage: node check_model_a25.mjs --mode class|2transitive --model <path-to-vlines-file>\n" +
        "   or: node check_model_a25.mjs --self-test"
    );
    process.exit(2);
  }
  const mode = args[modeIdx + 1];
  const modelPath = args[modelIdx + 1];
  const text = readFileSync(modelPath, "utf8");
  const trueVars = parseModelVLines(text);

  let report;
  if (mode === "class") report = checkClassModel(trueVars);
  else if (mode === "2transitive") report = check2TransitiveModel(trueVars);
  else {
    console.error(`unknown mode: ${mode}`);
    process.exit(2);
  }
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.ok ? 0 : 1);
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) main();
