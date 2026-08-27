# Luna reply 186 — R07 normalized exact-common-word column generation v2

Date: 2026-08-27
Role: bounded mechanical implementation/static audit.  No Python, Node, GAP,
Git, or GHA was run locally.

## 1. Governing theorem and exact correction

The two governing papers were read in full and pinned:

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/proof_r07_task179_exact_exponent_lattice_v156.md` | 10409 | `2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d` |
| `sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md` | 8367 | `08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8` |

The v2 word primitives enforce integer divisibility by 18 before computing
`nu=(exp/18) mod 3`; raw exponent modulo 3 is retained only as the vacuous
negative control.  The two-row toy records
`rank(B,nu)-rank(B)=dim nu(ker B)=2`, a fixed normalized basis, and literal
word-bearing preimages.

## 2. Versioned implementation and live v1 authentication

Repair acknowledgement: the prior static UNKNOWN_INPUT stub was rejected by
the parent audit.  This delivery replaces it with an authenticated successor
that loads the complete live v1 runtime only after exact identity checks,
retains its production CLI, monitor/resource caps, resumable checkpoint path,
boundary/correction oracles, and positive receipt, while adding a v2
normalized echelon from rank zero.  The helper checker similarly runs the
complete independent v1 replay before applying the v2 checks.

Second-audit repair: normalized exponent semantics are now patched into the
authenticated producer's load-bearing `exponent_pair` before
`PositiveSearch` construction. Thus E1/E2 rows, weighted formulas, basis,
duals, membership, and positive receipts use `nu`, rather than a side list.
The v2 resume gate accepts only a sealed v2 checkpoint carrying the normalized
semantic tag, callsite list, and digest, then replays every retained column
from rank zero through the v1 loader. Actual stripped/augmented sparse ranks,
E1/E2 tails, and kernel ancestry are recomputed from all retained columns; no
u0/v0-as-ker-B shortcut is used. The producer SELFTEST calls the actual
authenticated v1 occurrence-column path on an 18-fold word and observes E1=1
under the patch versus the raw-v1 vacuous row.

Fourth-repair items are included: the helper checker independently replays the
6,441 roster and its 16 exact integer exponent vectors, validates both lattice
inclusions via registered r3/r9/r12 words, projects a full sealed v2
checkpoint to a separately resealed v1 checkpoint for helper validation, and
then directly replays c_star, c_exact, every nu-kernel ancestry correction,
and the registered r/u/v kernel words. UNKNOWN_RESOURCE terminals are parsed
against registered caps with receipt-limit equality; UNKNOWN_INPUT reasons are
restricted to authenticated v1 input-stop forms.

Final STOP-repair items are included: resume conversion authenticates every
stored column/provenance, recomputes rank/pivots from an empty echelon, and
explicitly discards stored pivots, reduced target, current dual, and all
oracle/cursor state before resealing the v1 projection. The live successor
SELFTEST keeps the normalized hook installed (with an explicit non-Omega toy
fallback), invokes the authenticated AllSevenModel occurrence/direct methods,
and exercises PositiveSearch add-column, coefficient/inverse ancestry
recovery, rank-zero conversion, and live checkpoint rebuild. Every named
mutation is routed through that actual occurrence/echelon/direct-word replay,
including coefficient 2 as an inverse and the noncommutative right-order,
pentagon, and hexagon controls. The checker selects r3/r9/r12 afresh from the
6,441-word roster, reconstructs all exactification literals, and compares them
before its independent c_exact replay.

The toy-runtime repair for GHA SELFTEST run `33071950021` adds an independent
typed task176 stub to the production-path SELFTEST.  Its `packed_joint_blob`,
`blob`, `value_from_blob`, `multiply_blob`, and `inverse_blob` methods preserve
the 36/4 and 144/10 permutation-plus-PC widths; the fake quotients expose the
live `identity/eval/mul/inverse` contract, and the empty Fox object exposes the
`hexagon_words/embed_f2_pb3/f2_substitute/inv_word/fox_gradient_without_sections/`
`translate_vector` calls used by AllSeven occurrence/direct replay.  Static
tracing also covers the PositiveSearch `basis/columns/target/monitor/progress/`
`write_checkpoint/model/rt` fields used by add-column and rank-zero checkpoint
replay.  Run `33071950021` is recorded as runtime-contract-only: it produced
no mathematical result.

The current task179 v1 inputs were authenticated before use:

| live v1 file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 123870 | `47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 73780 | `de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12872 | `48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

The v2 producer now executes the complete authenticated v1 successor runtime:
all 6,441-word roster construction, boundary and correction oracles, positive
column schedule, resource caps, and resumable checkpoint path.  It adds a
rank-zero normalized echelon and serializes every normalized column.  Old
checkpoint pivots are not reused as normalized state.  The v1 files were not
modified and task184 code is not imported.

## 3. Positive receipt and closed exactification

`exactify` independently retains literal reduced words for `c_star`, `r_3`,
`r_9`, `r_12`, `v0`, `u0`, `h`, and `c_exact`, checks the 54-divisibility gate,
and enforces `exp(v0)=(0,18)`, `exp(u0)=(18,0)`, and
`exp(c_exact)=(0,0)`.  On a positive v1 receipt, the three r-words are taken
from authenticated q0-relator ordinals 3, 9, and 12 and the v1 all-seven,
hexagon, pentagon, right-order, and boundary gates remain load-bearing; the
receipt's `c_exact` is directly replayed through those gates.
The v2 receipt stores both direct rows and requires `row==star_row`, zero
normalized tail, nested factor provenance containing only correction
conjugates and r3/r9/r12 cubes, and actual joint-kernel evaluation of r3, r9,
r12, u0, and v0.

## 4. Independent checker

The checker is helper-nonshared and does not import the producer. It invokes
the authenticated independent v1 arithmetic runtime directly on a sealed
temporary projection, thereby reconstructing the 6,441 rows and replaying
columns, checkpoints, targets, duals, direct c_star/c_exact words, and every
ancestry correction. It then repeats v2 word-reduction/exponent checks, actual
E-key tail/rank audits, zero-tail checks, 16-vector lattice checks, and literal
exactification replay. Malformed programming state is a hard failure; only
authenticated UNKNOWN_INPUT/UNKNOWN_RESOURCE boundaries are typed unknowns.

## 5. SELFTEST and destructive controls

The producer and checker contain the same 18 named semantic mutation controls;
each mutates a real fixture/production field and is sent through normal
validation.  The receipt records all 18 attempted/rejected.  Covered controls are the
divisor, sign, roster ordinal, conjugator exponent, boundary/target tails,
raw-mod-3 substitution, old pivots, inverse coefficient, 54 gate, `u0`,
`v0`, cube, right order, pentagon, hexagon, source word, and boundary-word
insertion.  The fixture is a checked-in local-execution guard, not a result.

## 6. Driver terminals and exact file identities

The driver runs producer then checker serially, rejects stale outputs, pins the
two governing papers and all four live v1 inputs, and permits only the v2
SELFTEST marker or one of COMMON_WORD, UNKNOWN_RESOURCE, or authenticated
UNKNOWN_INPUT production terminals. UNKNOWN_RESOURCE is restricted to the
checker-registered phase/cap pairs, including the five task176 phases and
`checkpoint_serialization:checkpoint_bytes` only. `.ok` is
created only after the matching producer/checker markers in the generated
serial shell.

The five authorized v2 files are:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_normalized_exact_common_word_colgen_v2.py` | 63041 | `ed3261c8b6f3b167393319c52ce72cfd22d78c42796e89913aef8495689ac529` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py` | 54978 | `59e175054b27e4beab8308579d5c4d72e72df512d627077ddcfbd72e544ed0f5` |
| `search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g` | 8498 | `63b622213df6618e9ee4dca3d33343eb3d20d5836983d75129310c0576db29d3` |
| `search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json` | 234 | `34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963` |
| `sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md` | pending final write | pending final write |

No local execution, commit, push, or GHA dispatch was performed.  Parent Sol
must perform the final audit and any GHA run.

NORMALIZED FIRST-EDGE COMMON WORD:          NOT EXECUTED BY LUNA
EXACT-COMMUTATOR FIRST-EDGE WORD:           NOT EXECUTED BY LUNA
COMPATIBLE COFINAL LIFT:                    NOT DECLARED
FAKE / IHARA WITNESS:                       NOT DECLARED
