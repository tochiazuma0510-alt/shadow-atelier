#!/usr/bin/env node
// search/sat/check_model_n21.mjs
//
// Independent SAT model checker for the n=21 tail-8 target
// (search/sat/encode_tail8_n21.py, sol/sol_reply_84_math11.md sec 6.2).
//
// DELIBERATELY DOES NOT import encode_tail8_n21.py, does not share any
// helper module with it, and is written in a different language (node vs
// python) -- this is the searcher/checker separation mandated by CLAUDE.md
// and search/sat/README.md. It re-derives the variable numbering scheme
// from scratch (same *design*, independently re-typed, so a bug in one
// side's arithmetic is unlikely to reproduce in the other) purely to be
// able to READ a kissat model_vlines.txt file; every mathematical property
// it reports (involution/cycle types, b=a*u^-1, b^3=1, fixed-point-free,
// transitivity) is recomputed from the DECODED PERMUTATIONS, never trusted
// from the SAT model's B/E/STEP/R variables directly except to decode them
// into a permutation in the first place.
//
// Usage:
//   node check_model_n21.mjs --mode class      --model out/model_vlines.txt
//   node check_model_n21.mjs --mode transitive --model out/model_vlines.txt
//   node check_model_n21.mjs --self-test
//
// "class" mode checks only: a is an involution of type 2^10 1, b=a*u^-1,
// b^3=1, b fixed-point-free (=> type 3^7). It explicitly does NOT require
// transitivity (that would be checking a stronger property than CNF#1
// encodes, which would be a checker bug in the other direction).
//
// "transitive" mode checks the same class properties PLUS full
// transitivity of <a,b> on {1..21}, via a check-side BFS/orbit
// computation over generators {a, b, b^-1} that does not read the model's
// R/STEP/E variables at all (only a,b are decoded from X/D/B variables;
// reachability is recomputed by this checker's own graph traversal).

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const N = 21;

// ---------------------------------------------------------------------
// Fixed u (re-typed independently from the design in Sol 6.2 / the
// encoder's docstring -- NOT copy-pasted from the .py source).
// ---------------------------------------------------------------------
function buildU() {
  const u = new Map();
  for (let i = 1; i <= 12; i++) u.set(i, i + 1);
  u.set(13, 1);
  for (const [a, b] of [[14, 15], [16, 17], [18, 19], [20, 21]]) {
    u.set(a, b);
    u.set(b, a);
  }
  return u;
}
const U = buildU();
const UINV = new Map();
for (const [k, v] of U) UINV.set(v, k);

// ---------------------------------------------------------------------
// Variable numbering (must match encode_tail8_n21.py's scheme so a model
// can be decoded -- but re-derived independently here, not imported).
// ---------------------------------------------------------------------
const PAIRS = [];
for (let i = 1; i <= N; i++) {
  for (let j = i + 1; j <= N; j++) PAIRS.push([i, j]);
}
const PAIR_IDX = new Map();
PAIRS.forEach(([i, j], k) => PAIR_IDX.set(`${i},${j}`, k + 1));
const NUM_PAIRS = PAIRS.length; // 210

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

const CLASS_VAR_COUNT = B_BASE + B_COUNT; // 672
if (CLASS_VAR_COUNT !== 672) throw new Error("internal: CLASS_VAR_COUNT mismatch");

// ---------------------------------------------------------------------
// Model parsing.
// ---------------------------------------------------------------------

// Parse a kissat "v ..." model listing (possibly spread over several
// lines, each starting with 'v', terminated by a 0) OR a bare list of
// signed integers. Returns a Set of TRUE variable ids (1-indexed).
export function parseModelVLines(text) {
  const trueVars = new Set();
  const tokens = [];
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (line.length === 0) continue;
    if (line.startsWith("c")) continue; // comment
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
// Decoding: SAT model (set of true var ids) -> permutations a, b as
// plain arrays a[1..21], b[1..21] (1-indexed, a[0]/b[0] unused).
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
      issues.push(
        `row ${i}: expected exactly one of X/D true, found ${candidates.length} (${candidates.join(",")})`
      );
      continue;
    }
    a[i] = candidates[0];
  }
  return { a, issues };
}

export function decodeBFromModel(trueVars) {
  // Decode B[i][k] directly from the model's own B variables (used only
  // to cross-check against the independently recomputed b = u^-1 o a,
  // see recomputeBFromA below -- NOT trusted on its own).
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

// Independent recomputation of b from a and the fixed u, NOT reading any
// B/E/STEP/R model variable. This is the checker's actual authority for
// "is b=a*u^-1 satisfied" -- the decodeBFromModel() value above is only
// used to flag encoder/solver disagreement, never as ground truth.
export function recomputeBFromA(a) {
  const b = new Array(N + 1).fill(null);
  for (let i = 1; i <= N; i++) {
    if (a[i] == null) continue;
    b[i] = UINV.get(a[i]);
  }
  return b;
}

// ---------------------------------------------------------------------
// Mathematical property checks (all computed from decoded permutations,
// independent of which model variables "said so").
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

export function isInvolutionType2_10_1(perm) {
  const ct = cycleType(perm);
  if (!ct.ok) return { ok: false, reason: ct.reason };
  const want = [1, ...Array(10).fill(2)];
  const got = ct.lengths;
  const match = got.length === want.length && got.every((v, idx) => v === want[idx]);
  return { ok: match, lengths: got, expected: want };
}

export function isType3_7(perm) {
  const ct = cycleType(perm);
  if (!ct.ok) return { ok: false, reason: ct.reason };
  const want = Array(7).fill(3);
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

export function isFixedPointFree(perm) {
  for (let i = 1; i <= N; i++) {
    if (perm[i] === i) return false;
  }
  return true;
}

export function invertPerm(perm) {
  const inv = new Array(N + 1).fill(null);
  for (let i = 1; i <= N; i++) inv[perm[i]] = i;
  return inv;
}

// Orbit / transitivity check via check-side BFS over generators
// {a, b, b^-1} starting at point 1 -- does not read any R/STEP/E model
// variable.
export function orbitsUnderGenerators(a, b) {
  const bInv = invertPerm(b);
  const gens = [a, b, bInv];
  const seen = new Array(N + 1).fill(false);
  const orbits = [];
  for (let start = 1; start <= N; start++) {
    if (seen[start]) continue;
    const orbit = [];
    const queue = [start];
    seen[start] = true;
    while (queue.length > 0) {
      const v = queue.shift();
      orbit.push(v);
      for (const g of gens) {
        const w = g[v];
        if (!seen[w]) {
          seen[w] = true;
          queue.push(w);
        }
      }
    }
    orbits.push(orbit.sort((x, y) => x - y));
  }
  orbits.sort((o1, o2) => o1.length - o2.length);
  return orbits;
}

export function isTransitiveFrom1(a, b) {
  const orbits = orbitsUnderGenerators(a, b);
  return { transitive: orbits.length === 1 && orbits[0].length === N, orbits: orbits.map((o) => o.length) };
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

  const invCheck = isInvolutionType2_10_1(a);
  record("a_is_involution_type_2^10_1", invCheck.ok, invCheck);

  const bModel = decodeBFromModel(trueVars).b;
  const bRecomputed = recomputeBFromA(a);
  const bAgrees = bModel.every((v, i) => i === 0 || v === bRecomputed[i]);
  record("model_B_agrees_with_independently_recomputed_b=u^-1(a(.))", bAgrees, {
    model_B: bModel.slice(1),
    recomputed_b: bRecomputed.slice(1),
  });

  // Ground truth for all downstream checks is the RECOMPUTED b, never
  // the model's B variables, per the file header note.
  const b = bRecomputed;

  const cubeOk = permCubeIsIdentity(b);
  record("b_cubed_equals_identity", cubeOk, {});

  const fpfOk = isFixedPointFree(b);
  record("b_is_fixed_point_free", fpfOk, {});

  const type37 = isType3_7(b);
  record("b_is_type_3^7", type37.ok, type37);

  report.decoded = { a: a.slice(1), b: b.slice(1) };
  return report;
}

export function checkTransitiveModel(trueVars) {
  const report = checkClassModel(trueVars);
  if (!report.decoded) return report;
  const { a, b } = { a: [null, ...report.decoded.a], b: [null, ...report.decoded.b] };
  const trans = isTransitiveFrom1(a, b);
  report.checks.push({
    name: "generated_group_is_transitive_on_1..21",
    ok: trans.transitive,
    detail: trans,
  });
  if (!trans.transitive) report.ok = false;
  return report;
}

// ---------------------------------------------------------------------
// Self-test using the machine-extracted GAP witness fixture. This is the
// checker's OWN calibration: it must accept the fixture as a valid CNF#1
// (class-only) witness, and must correctly report it as NON-transitive
// (matching GAP's independently reported orbits=[6,15]).
// ---------------------------------------------------------------------

function selfTest() {
  const here = fileURLToPath(new URL(".", import.meta.url));
  const fixturePath = here + "fixtures/witness_n21_nontransitive.json";
  const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));

  // Build a synthetic "model" (set of true X/D/B vars) directly from the
  // fixture's a_images, WITHOUT touching encode_tail8_n21.py.
  const aImg = fixture.a_images_1indexed; // 0-indexed array, aImg[k-1] = a(k)
  const trueVars = new Set();
  for (let i = 1; i <= N; i++) {
    const ai = aImg[i - 1];
    if (ai === i) trueVars.add(Dvar(i));
    else trueVars.add(Xvar(i, ai));
  }
  // Populate B vars too (from fixture's b_images, so the cross-check
  // against recomputeBFromA is exercised, not skipped).
  const bImg = fixture.b_images_1indexed;
  for (let i = 1; i <= N; i++) {
    trueVars.add(Bvar(i, bImg[i - 1]));
  }

  const uOk = fixture.u_images_1indexed.every((v, idx) => U.get(idx + 1) === v);
  const uInvOk = fixture.uinv_images_1indexed.every((v, idx) => UINV.get(idx + 1) === v);

  const classReport = checkClassModel(trueVars);
  const transReport = checkTransitiveModel(trueVars);

  const results = {
    fixture_u_matches_checker_u: uOk,
    fixture_uinv_matches_checker_uinv: uInvOk,
    class_report_ok: classReport.ok,
    class_checks: classReport.checks,
    transitive_report_ok_expected_false: transReport.ok,
    transitive_orbits_reported: transReport.checks.find(
      (c) => c.name === "generated_group_is_transitive_on_1..21"
    )?.detail,
    gap_reported_orbits: fixture.gap_reported_orbits,
    gap_reported_transitive: fixture.gap_reported_transitive,
  };

  const pass =
    uOk &&
    uInvOk &&
    classReport.ok === true &&
    transReport.ok === false && // fixture is known non-transitive
    JSON.stringify(results.transitive_orbits_reported.orbits.slice().sort((x, y) => x - y)) ===
      JSON.stringify(fixture.gap_reported_orbits.slice().sort((x, y) => x - y));

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
      "usage: node check_model_n21.mjs --mode class|transitive --model <path-to-vlines-file>\n" +
        "   or: node check_model_n21.mjs --self-test"
    );
    process.exit(2);
  }
  const mode = args[modeIdx + 1];
  const modelPath = args[modelIdx + 1];
  const text = readFileSync(modelPath, "utf8");
  const trueVars = parseModelVLines(text);

  let report;
  if (mode === "class") report = checkClassModel(trueVars);
  else if (mode === "transitive") report = checkTransitiveModel(trueVars);
  else {
    console.error(`unknown mode: ${mode}`);
    process.exit(2);
  }
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.ok ? 0 : 1);
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) main();
