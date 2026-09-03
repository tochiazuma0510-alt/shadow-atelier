# Luna Task699 — all-four Task554 block ingest and P1 structural completion

## Mathematical shortening

Read `sol/proof_r07_grade2_lazy_presentation_interface_v480.md` and
`sol/proof_r07_grade2_p1_disjoint_lead_completion_v481.md`.  Task693's
independent actual census establishes that all 2,014 old leads lie in degree
zero or the final auxiliary interval.  Hence a new row's global lead is simply
`24192 + 18144*a + local_lead`; the four degree-one intervals are disjoint
from one another and from every old lead.  Do not assemble or reduce an
8059-by-96776 matrix.

## Exact input

Extend the current
`search/d972_r07_grade2_specific_owner_prejoin_v1.py` after Task696.  The four
already extracted read-only roots are
`%TEMP%/r07_grade1_blocks_33677346616/b0` through `b3`.  Exact body pins,
service artifact receipts and ranks are already frozen in `PARENTS`/`SERVICE`:

```text
body ranks: 1509,1512,1512,1512
attempts:   14268,14280,14280,14280
body SHA:   9ebcc7ad..., d783bbe6..., a6dcc904..., 642a4ec0...
basis SHA:  cc7e3811..., 0223f72b..., 602f2308..., 4ed4de15...
width:      18144 trits; row bytes: 4536
```

Use the complete literal values from the receipts, never the ellipses above.

## Required implementation

1. Refactor the already accepted prepare ingest only enough that the combined
   path authenticates/scans prepare once and retains its parsed body/digest
   while validating the four blocks.  Preserve the existing prepare-only CLI.
2. Add a combined CLI taking exactly one prepare root and exactly four ordered
   block roots.  Keep default/Task640 join fail-closed.
3. For each block serially, apply the same non-following root/member gates and
   require its exact three-file roster: canonical HEAD, its pinned canonical
   body, and its one content-addressed basis blob.  Validate HEAD/body schema,
   stem, parent prepare digest, exact pinned body digest, phase/fixture,
   character/index/order, dimensions, packet binding, origin count, exact
   rank/attempts/FIFO/actor order, false downstream claims and the typed basis
   receipt.
4. Completely traverse and type-check all `origin_reductions`, all four actor
   transition expressions per row, every DAG node/reduction, pivot leads,
   scales and the canonical DAG digest.  DAG reductions must be strictly
   prior.  Validate each DAG `origin`: defect origins are in `[0,8232)`;
   actor origins have a prior parent and a letter in `[1,-1,2,-2]`.  Report
   exact expression-list and coefficient-pair totals per block.
5. During one sequential pass over each basis blob, bind exact count/SHA/range
   to its receipt and retain only one 4,536-byte row at a time.  Recompute each
   actual local first nonzero coordinate, require equality with its declared
   pivot lead and coefficient one, and compute canonical per-block lead
   digests.
6. Apply v481 without zero fill: combine the accepted old summary with mapped
   new leads, require 8,059 distinct normalized global leads, and emit their
   canonical digest, ranks/offsets and `global_echelonicity=true`.  If any
   actual condition fails, fail closed rather than trusting v481.
7. Parse one large block body at a time and release its raw/body object after
   extracting canonical small diagnostics; do not retain four JSON bodies,
   any dense family, or duplicate basis blobs.  Report real serial elapsed
   time and measured peak RSS.
8. Fixtures must exercise the live block-envelope/semantic/local-lead/global-
   summary helpers, including wrong parent, wrong block order, bad expression,
   forward DAG edge, wrong origin type, late byte 81, wrong declared lead,
   coefficient two and cross-family collision.  Do not add generic security
   hardening or precision-two code.

Run serial `py_compile`, bounded selftest, and one actual all-five-root replay.
Report in `sol/luna_reply_699_r07_p1_four_block_structural_ingest.md` with exact
file bytes/LF/SHA and all real counters/digests.  Candidate only;
`verified=false`; no workflow, GHA, git, independent checker, semantic
44+4*8059 equality claim, Task640 join or grade-two decision.

## Mutation boundary

- `search/d972_r07_grade2_specific_owner_prejoin_v1.py`
- `sol/luna_reply_699_r07_p1_four_block_structural_ingest.md`
