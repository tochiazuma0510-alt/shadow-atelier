// search/certs/gen_full_cert_base.mjs
//
// Standalone export helper (NOT a lane implementation file -- same pattern
// as the existing search/certs/ep-lanea-export.mjs / fixtures-lanea.mjs).
// Calls lane A's OWN real D-2 generator (search/ninfty-searcher-v2.mjs
// generateCertificate/buildSearcherNative) on the genuine curve fixture
// search/fixtures/ninfty/checker_pos_01.json, and prints the resulting
// certificate + native artifact as JSON to stdout.
//
// This produces the base certificate whose component_bijection /
// exact_point_equality_witnesses / distinctness_witnesses /
// multiplicity_equalities / total_coverage_and_no_extra_component_witness
// fields are ALREADY in the flat + divisor_object-tag shape (裁定127/128).
// Its chart_overlap_witnesses / pushforward_compatibility_witness fields
// are still lane A's OLD single-structured-object shape (未移行, tracked
// by search/ninfty-cert-validator.py as the two open interp-4 violations)
// -- those two fields are REPLACED downstream by
// search/certs/assemble_full_witness_cert.py using the independently
// generated content from search/ninfty-witness-gen.py.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { buildSearcherNative, generateCertificate } from '../ninfty-searcher-v2.mjs';

const THIS_DIR = dirname(fileURLToPath(import.meta.url));
const FIXTURE_PATH = join(THIS_DIR, '..', 'fixtures', 'ninfty', 'checker_pos_01.json');

const candidate = JSON.parse(readFileSync(FIXTURE_PATH, 'utf8'));
const native = buildSearcherNative(candidate);
const cert = generateCertificate({
  candidateRef: 'full-witness-fixture-01',
  searcherNative: native,
  checkerNative: native, // same lane's native used for both slots -- see report for the honest caveat this implies
});

console.log(JSON.stringify({ certificate: cert, native }, null, 2));
