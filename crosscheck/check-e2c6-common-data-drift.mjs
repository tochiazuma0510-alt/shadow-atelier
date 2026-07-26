// crosscheck/check-e2c6-common-data-drift.mjs
// Automated drift check between search/e2c6-common-data.g (j=3 gate's shared data module,
// new) and search/e2c6-sweep.g (frozen, hash-ledgered j=2 gate) -- both files carry a VERBATIM
// copy of the same 7 transcribed class-6 table-data blocks (BASIS21, ThetaTable21,
// SigmaTablePoly21, EmComponents21, KappaTerms, DThetaFormula, DSigmaFormula). This was
// previously confirmed ONLY by a falsifier's one-off manual Python string comparison
// (docs/notes/反証前哨_j3.md 問4) -- this script makes that check permanent/automated/rerunnable
// as part of the ordinary fixture pass, per commander instruction (item 4).
//
// METHOD: for each of the 7 block names, extract the GAP source text starting at
// "NAME := " and scanning forward tracking bracket depth (both "[...]" and "(...)", combined,
// since KappaTerms/DThetaFormula/DSigmaFormula are `rec(...)`-shaped while the others are
// `[...]`-shaped) until depth returns to 0 -- this is a generic, block-name-agnostic
// extractor, not hand-tuned per block. The extracted text (including the trailing ";;") must
// be BYTE-IDENTICAL between the two files for the check to PASS.
//
// This script does NOT read search/e2c6j3-sweep.g or crosscheck/check-e2c6j3.mjs -- it only
// compares the two GAP source files directly (this is a source-level provenance check, not a
// certificate crosscheck, so it does not follow the certificates/ input convention of the
// other crosscheck/*.mjs scripts).

'use strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const __dirname_ = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname_, '..');

const PATH_A = join(ROOT, 'search', 'e2c6-sweep.g');       // frozen j=2 gate (source of truth)
const PATH_B = join(ROOT, 'search', 'e2c6-common-data.g'); // new j=3 shared module (the copy)

const BLOCK_NAMES = [
  'BASIS21', 'ThetaTable21', 'SigmaTablePoly21', 'EmComponents21',
  'KappaTerms', 'DThetaFormula', 'DSigmaFormula',
];

function extractBlock(source, name, fileLabel) {
  const marker = `${name} := `;
  const start = source.indexOf(marker);
  if (start === -1) throw new Error(`block "${name}" not found in ${fileLabel}`);
  const bodyStart = start + marker.length;
  let depth = 0;
  let i = bodyStart;
  let started = false;
  for (; i < source.length; i++) {
    const c = source[i];
    if (c === '[' || c === '(') { depth++; started = true; }
    else if (c === ']' || c === ')') { depth--; }
    if (started && depth === 0) { i++; break; }
  }
  // expect ";;" immediately following (skip nothing -- must be adjacent, matching GAP style
  // used throughout these files)
  if (source.slice(i, i + 2) !== ';;') {
    throw new Error(`block "${name}" in ${fileLabel}: expected ";;" immediately after closing bracket, got "${source.slice(i, i + 10)}"`);
  }
  return source.slice(start, i + 2);
}

let fails = 0;
console.log('=== crosscheck/check-e2c6-common-data-drift.mjs (source-level byte-identity check) ===');
console.log(`  A (source of truth, frozen): ${PATH_A}`);
console.log(`  B (copy, j=3 shared module):  ${PATH_B}`);

const srcA = readFileSync(PATH_A, 'utf8');
const srcB = readFileSync(PATH_B, 'utf8');

for (const name of BLOCK_NAMES) {
  let blockA, blockB;
  try {
    blockA = extractBlock(srcA, name, 'e2c6-sweep.g');
    blockB = extractBlock(srcB, name, 'e2c6-common-data.g');
  } catch (e) {
    console.log(`FAIL  ${name}: extraction error -- ${e.message}`);
    fails++;
    continue;
  }
  const identical = blockA === blockB;
  console.log(`${identical ? 'PASS ' : 'FAIL '} ${name}: ${blockA.length} chars (A) vs ${blockB.length} chars (B) -- byte-identical=${identical}`);
  if (!identical) {
    fails++;
    // report first differing offset for diagnosis
    const n = Math.min(blockA.length, blockB.length);
    let diffAt = -1;
    for (let k = 0; k < n; k++) { if (blockA[k] !== blockB[k]) { diffAt = k; break; } }
    if (diffAt === -1) diffAt = n;
    console.log(`  first difference at offset ${diffAt}: A="${blockA.slice(Math.max(0, diffAt - 20), diffAt + 20)}" B="${blockB.slice(Math.max(0, diffAt - 20), diffAt + 20)}"`);
  }
}

console.log(`\n${fails === 0 ? 'ALL PASS' : fails + ' FAILURES'} (7 blocks checked: ${BLOCK_NAMES.join(', ')})`);
if (fails > 0) process.exit(1);
