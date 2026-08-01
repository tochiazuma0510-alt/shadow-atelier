// search/certs/ep_first_run/extract_beta.mjs
//
// EP first unit-run - candidate beta extractor
// (design: docs/notes/ep_first_candidate_design_v1.md sec.2 案β / sec.3).
//
// Machine-extracts, from certificates/mb/ninfty-branch-search-bound3.json's
// stage1_pass_details (288 entries, stage1-only passes over the bound=3
// integer lattice), the dictionary-order-minimal tuple by
// (a5,a4,a3,a2,a1,a0,p2,p1,p0) -- a purely mechanical rule, no manual
// choice -- then re-derives f6 by re-running the search script's own
// exported `testCandidateNinfty` (imported, not reimplemented) on that one
// tuple. This is a re-derivation of f6 from (a,p), not a new search.
//
// This script does NOT search. It reads one already-produced, already
// hash-bound certificate and extracts one entry by a fixed, disclosed rule.
//
// Usage: node search/certs/ep_first_run/extract_beta.mjs
// Output: prints JSON to stdout (candidate + source digest + extraction rule).

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { testCandidateNinfty, factorCheckNinfty } from '../../mb-ninfty-branch-search.mjs';
import { Frac } from '../../mb-frac.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..', '..');
const CERT_PATH = join(ROOT, 'certificates', 'mb', 'ninfty-branch-search-bound3.json');

function main() {
  const raw = readFileSync(CERT_PATH);
  const sourceDigest = createHash('sha256').update(raw).digest('hex');
  const cert = JSON.parse(raw.toString('utf-8'));
  const details = cert.stage1_pass_details;
  if (!Array.isArray(details) || details.length !== cert.stage1_passes) {
    throw new Error(`stage1_pass_details length ${details && details.length} != stage1_passes ${cert.stage1_passes}`);
  }

  const sortKey = (d) => [d.a5, d.a4, d.a3, d.a2, d.a1, d.a0, d.p2, d.p1, d.p0];
  const cmp = (x, y) => {
    const kx = sortKey(x), ky = sortKey(y);
    for (let i = 0; i < kx.length; i++) {
      if (kx[i] !== ky[i]) return kx[i] - ky[i];
    }
    return 0;
  };
  const sorted = [...details].sort(cmp);
  const min = sorted[0];

  // full-pipeline re-run (stage1 + stage2), exactly the search script's own
  // exported entry point -- this is what tells us the predicted verdict
  // (design doc P-EP-1: stage1 PASS, stage2 REJECT).
  const rederived = testCandidateNinfty(min.a0, min.a1, min.a2, min.a3, min.a4, min.a5, min.p0, min.p1, min.p2);
  if (!rederived.ok && rederived.stage === 1) {
    throw new Error(`stage-1 re-derivation FAILED for the extracted dict-min tuple, contradicting stage1_pass_details: ${JSON.stringify(rederived)}`);
  }

  // f6 itself (needed regardless of the stage2 outcome, since the unit run
  // needs a fully-formed (a,p,f6) candidate to hand to lane A/B): re-derive
  // it directly via the same exported factorCheckNinfty, using the same
  // Frac class the search script itself imports from ./mb-frac.mjs (no
  // reimplementation of the arithmetic).
  const aFrac = [min.a0, min.a1, min.a2, min.a3, min.a4, min.a5].map((x) => Frac.from(x));
  const pFrac = [min.p0, min.p1, min.p2].map((x) => Frac.from(x));
  const stage1 = factorCheckNinfty(aFrac, pFrac);
  if (!stage1.ok) {
    throw new Error(`factorCheckNinfty stage-1 re-derivation FAILED, contradicting stage1_pass_details: ${JSON.stringify(stage1)}`);
  }

  const out = {
    role: 'EP first unit-run candidate beta extraction (single point, not a search)',
    design_ref: 'docs/notes/ep_first_candidate_design_v1.md sec.2 案β / sec.3',
    source_cert_path: 'certificates/mb/ninfty-branch-search-bound3.json',
    source_cert_sha256: sourceDigest,
    extractor_path: 'search/certs/ep_first_run/extract_beta.mjs',
    extraction_rule: 'lexicographic-minimal over (a5,a4,a3,a2,a1,a0,p2,p1,p0) across all 288 stage1_pass_details entries, machine-sorted, no manual choice',
    dict_min_raw_from_cert: min,
    full_pipeline_rederivation: rederived,
    candidate: {
      a: aFrac.map((x) => x.toString()),
      p: pFrac.map((x) => x.toString()),
      f6: stage1.f6.map((x) => x.toString()),
      cHatMu: stage1.cHatMu.toString(),
    },
  };
  process.stdout.write(JSON.stringify(out, null, 2) + '\n');
}

main();
