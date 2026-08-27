# Luna reply 177 - R07 weighted-cell column generation v1

Date: 2026-08-27

## Scope and terminal

The five task177 files were created in the authorized scope.  No local
Python, Node, GAP, git, or GHA execution was performed.  No production PASS
is claimed.  Production is deliberately sealed at
`UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED` because the positive task175 and
task176 run ids, head SHAs, receipt digests, and checker verdict digests are
not registered.

## Implemented

- The producer contains a local D6 = C3 semidirect C2 word/group model and
  a real noncommutative SELFTEST validator.
- The checker independently uses permutations, with no producer or
  predecessor import and no shared weighted/projection/cell/word helper.
- The SELFTEST path reconstructs the linked extension, weighted same-target
  merge, exact Boolean cells including the all-star complement, lazy
  one-, two-coordinate subset queries and kernel counts, section/Gamma
  provenance, source conjugation, typed PB3/PB4 block rows, negated target,
  exponent rows, common correction replay, and ordered pentagon replay.
- Twelve semantic mutations are passed through the validator path:
  merge cancellation, multi-coordinate target, inclusion-exclusion sign,
  kernel order, complement, section/Gamma adjustment, transversal word,
  block tag, target coordinate, exponent coordinate, final coefficient, and
  pentagon order/sign.
- The production skeleton has an outside-repository fixed-width streaming
  primitive and schema-only task175/task176 receipt ingestion, but the
  promotion switch remains unset.
- The GAP driver is ASCII-only, binds/checks the mode before dispatch,
  executes producer then checker serially, requires exact stage/terminal
  agreement, and writes the final driver-pass artifact for both SELFTEST and
  the honest typed UNKNOWN production terminal.  The stdout sentinel is
  emitted by a generated fail-closed bash printf helper, so GAP line wrapping
  cannot alter it.
- The driver-pass checks now pass an explicit label to both `T177Read` and
  `T177AssertOne` in SELFTEST and PRODUCTION.  A static inventory found every
  `T177Read` call has two arguments and every `T177AssertOne` call has three.

## Not implemented and intentionally not claimed

The production branch has not run the 6,441-row weighted occurrence table,
arbitrary-subset v132 query cache, full PB3/PB4 translated boundary
families, sparse column-generation loop, or a positive common correction.
The code therefore emits no separator, common-word, cofinal, fake, or Ihara
conclusion.

## Static file hashes

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_weighted_cell_colgen_v1.py` | 29523 | `d955d7717f55ffca3abb92229b96ce2b8ee092ddae3d5e6c7379df92f3892d2e` |
| `crosscheck/check_d972_r07_weighted_cell_colgen_v1.py` | 20157 | `b4d8d046c6850042e0c74778ff8410d9725ef8d0d9387ddb2f75325a6f72d50e` |
| `search/d972_r07_weighted_cell_colgen_gha_driver_v1.g` | 13670 | `cb32e46412622e55b53859d0e2f2684932204dfdff85477244d1619f9df71304` |
| `search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json` | 4932 | `d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b` |

The driver pins v110, v118, v125, v132, PB3 v121, PB4 v108, and v122 by
their checked-in byte counts and SHA-256 values.  The v132 pin is the current
13,394-byte file.

## GHA SELFTEST preamble

The driver dispatches the following serial shape after the host binds
`D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE` to `SELFTEST` before `Read`:

```text
timeout 1800s bash -o pipefail -c 'set -euo pipefail; mkdir -p ci/out; python3 -B search/d972_r07_weighted_cell_colgen_v1.py --selftest --fixture search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json >ci/out/d972_r07_weighted_cell_colgen_producer_v1.log 2>&1; echo T177_SELFTEST_PRODUCER_STAGE_DONE >ci/out/d972_r07_weighted_cell_colgen_selftest_producer_v1.done; python3 -B crosscheck/check_d972_r07_weighted_cell_colgen_v1.py --selftest --fixture search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json >ci/out/d972_r07_weighted_cell_colgen_checker_v1.log 2>&1; echo T177_SELFTEST_CHECKER_STAGE_DONE >ci/out/d972_r07_weighted_cell_colgen_selftest_checker_v1.done'
```

Expected producer/checker markers are each exactly one line with
`mutations=12 rejected=12 linked_nonabelian_order=6`.  The driver then emits
`R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS`.
The final line is emitted through `ci/out/d972_r07_weighted_cell_colgen_command_v1.sh`
using `printf '%s\n'`, with newline/CR rejection and an exact mode/terminal
case gate.  Production uses the same emitter with terminal
`UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED`.

The driver-pass file itself is written through an
`OutputTextFile(...); SetPrintFormattingStatus(false)` helper in both modes,
and is then read back with an explicit label.  The generated emitter shell is
also read back and rejected if it contains a literal backslash followed by a
newline, matching the task176 fail-closed gate.
