# task336 / task333 A4 v4 lazy affine oracle — Luna implementation report

Scope was restricted to the five task336 outputs.  `AGENTS.md`, task336, the
task328/task331 contracts, task333 audit, v268/v271/v272, v273/task339 and
v274/task340 were read in full.  No Python, Node, GAP, GHA/workflow, git or
network execution was performed; the following is a static implementation
trace only.

## Four sealed machine files

The current byte identities (the reply file is not a machine-file input) are:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v4.py` | 98454 | `d895996da8c6014327028d5bd5c7076f27aa481f2d68511ac2cdbd55b1adaa6c` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v4.py` | 49223 | `e006cfef8f6c650298f8ceaab0522c9459d5868d6d25939d575177eee60fc3eb` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v4.g` | 7087 | `6cf2553045090a9dca8003fa8d5a6d6378811f666809aff61b851d4309ecb53a` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v4_20260829.json` | 593 | `2cbf25f57c9b28c9b8b212b5ac6b56c10fc570ea33a75f1e3eb5adaa50c38c16` |

The GAP driver pins the first, second and fourth rows above before dispatch.
The five permitted edits are exactly the two consumers, one ASCII GAP driver,
one v4 selftest fixture and this reply.

## Import and authority graph

The producer imports only Python standard-library modules and dynamically loads
the pinned arithmetic module
`search/d972_b345_seedspan_triple4_v1.py` plus the pinned q3 JSON
`ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json`.  It authenticates
the task176 source bytes at
`search/d972_r07_all_seven_extension_section_census_v1.py` but does not import
task176 or call task179.  The checker has a separate adapter, separate EKey
registry, separate arithmetic load and separate reverse trie; it never imports
the producer and never treats producer Booleans/digests as mathematical
evidence.  The driver performs one producer process followed by one checker
process.

Both adapters read and parse the five task198 members once, under their exact
paths:

* `ci/in/d972_r07_seven_context_roof_presentation_v1.json` — 31017244 bytes,
  `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5`;
* `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` —
  2722 bytes, `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4`;
* producer attestation — 81 bytes,
  `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090`;
* checker attestation — 95 bytes,
  `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e`;
* checker verdict — 150 bytes,
  `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de`.

Manifest schema, accepted/independent/nonsynthetic flags, self-seal, run
`33155710862`, head
`bed1d5e6b41477b8799f2a33a24e46f7800f9510`, artifact `9686477718`, ZIP seal,
receipt member identity, both attestation identities and the three source
identities are checked.  Receipt rows, counts, proof, chunks and seals are
read only from `receipt["Delta0"]["presentation"]`; the bridge is read only
from `receipt["bridge"]["occurrence_ledger"]`.  The adapters check all 6441
ordinals, all seven chunks, normal-generation arithmetic, both bridge maps,
both bridge digests, ABI entry points/widths/canaries, and the literal false
flags (`Ihara_witness`, `cofinal_lift`, `fake`, `D_all.materialized`, and
`direct_Delta_states_enumerated == 0`).

## Static positive route

1. `AuthorityAdapter` authenticates the receipt and retains one authority
   object.  The producer constructs actual `e3,e4` using
   `old.reconstruct_quotients(q3)`, not a state/edge enumeration.
2. The ten exact task232 contexts are five E3 and five E4 substitutions with
   IDs `(21,22,23,24,25,1,27,21,26,28)`.  Each of the 40 signed actor states
   is obtained once from the actual Fox evaluator.  Direct signed inverse
   products are checked against affine identity and the authenticated x/y,
   inverse, xy, x-action-y and source-2-2 canaries, including coordinate
   widths.
3. For every row, `replay_ancestry` checks the literal row word before use:
   Gamma is `red(section_source + record + inv(section_target))`; action uses
   its raw `tokens` and the orientation-specific outer conjugator; Q0 lift is
   `red(q0_relator + inv(section_target))`.  All three grammars and all
   stored row words are checked by both sides.
4. The producer builds one forward prefix trie over the 288 primitive words.
   Nodes contain roof metadata and immutable parent/edge affine deltas; only
   terminal affine values are materialized.  Row assembly consumes primitive
   terminals (or their exact inverse terminal), then is compared with a direct
   flat affine replay.  The fixed flat sample indices are
   `(0,6317,6318,6421,6422,6440)`.
5. `BoundaryLedger` constructs exactly `5*2 + 5*11 = 65` separately tagged
   seeds.  Every base relator is evaluated by
   `old.fox_gradient_without_sections`, requires identity roof, stores typed
   `(coordinate, component, support)` occurrences and caches support inverses.
6. `LazyBoundaryOracle` keeps one chronological coefficient-bearing B+K
   echelon.  A zero reduction is MEMBER with exact external B/K coefficients
   and raw replay.  A nonzero reduction constructs a finite active registry
   from current B/K support plus target, back-substitutes a dual through the
   actual projection, zero-extends it, and checks all-row and target pairings.
   Full-D correlation visits all matching occurrences from all 65 seeds,
   computes `t=g*h^-1`, checks `t*h=g`, accumulates
   `a*lambda(i,c,g)` under `(i,j,t)`, and selects the lexicographically first
   nonzero accumulator.  The translated column is actual, rank-raising and
   registered before the next query.  An all-zero accumulator is exported as
   a complete zero certificate; no artificial target coordinate is inserted.
7. Each accepted K item stores representative, literal word, raw E ledger,
   parent/action provenance and coefficients.  With internal
   `remainder=input+correction`, the exported convention is
   `r=v-Psi(Q)-sum(c_l*k_l)`.  For
   `W_new=(W_v*product_l W_l^(-c_l))^s`, the code computes and directly replays
   `E_new=s*(E_v+Q-sum(c_l E_l))`.  Source action translates every raw ledger
   key by the actual context actor.  The integer word DAG materializes source,
   outer-first conjugate, inverse, product and power nodes and directly
   replays every new K word and the anchor word.
8. The queue applies exactly x, x-inverse, y, y-inverse to each K item until
   exhaustion.  Complete member receipts build the four action matrices;
   inverse products, order-three and pairwise affine commutation are checked.
9. The anchor projects every retained K word to H2(9), chooses the least
   nonzero projected coordinate, computes its F3 inverse scalar, constructs
   the literal power, and repeats direct ten-context roof/discrepancy/K
   replay.  The required endpoint is `(0,0,3)`; an all-zero projection is
   `UNKNOWN_INPUT`, never a theorem.

The checker independently replays all ancestry rows, builds the opposite
association reverse suffix trie, reconstructs all 65 seeds and their actual
support inverses, uses a max-pivot finite dual convention, sorts its flat
occurrence/support stream, recomputes translations/correlations and directly
replays every producer K discrepancy.  It checks the chronological dual meter
and sealed producer certificate before emitting its own sealed verdict.

## Inventories and resource accounting

The static gates preserve the authenticated inventory:

* Gamma sections 243; record words 26; Q0 relators 19;
* combined primitive words 288 and 114458 literal primitive letters;
* producer prefix edges 15970; checker suffix edges 26136;
* stored row letters 5475488, split as Gamma 5433366, action 33206 and Q0
  lift 8916;
* exactly 10 contexts, 40 actor applications and 65 boundary seeds.

For `n=6441`, terminal K rank `t`, discovered boundary rank `p`, and one
anchor query, the declared query count is `Q=n+4t+q_anchor=6441+4t+1`.
There are exactly `p` active-boundary rank-rise rounds and at most one complete
zero-correlation terminal per quotient query.  The output reports the actual
correlation-pair sum, not the invalid `65+12b` shortcut.  Metered fields cover
input bytes, trie nodes/edges, terminal materializations, affine sparse
operations, row assemblies, quotient reductions, dual support, correlation
pairs, discovered columns, K queries/actions, word-DAG nodes/expanded letters,
direct replays, RSS, canonicalization, serialization and final write.  The
checkpoint field is explicitly `null` because no checkpoint was implemented.

## Mutation routes (static, unexecuted)

Producer and checker register the same 48 names and distinct owner stages.
The 34 inherited owners cover authority layer/member/bytes/path/proof/bridge/
ABI, echelon/raw coefficients/scale, basis change, conjugator/section/action/
target orientations, trie terminals, row mismatch, all eight task333 boundary
owners, queue and complete-zero correlation.  The task339 additions are
`omitted_candidate_discrepancy`, `omitted_prior_k_discrepancy`, `flipped_q_sign`,
`missing_discrepancy_scale`, `reversed_source_action_discrepancy`,
`changed_raw_tag_translation`, and `modulo_discovered_b_only_replay`.  The
task340 additions are `deleted_active_key`, `unregistered_dual_key`,
`raw_pivot_functional`, `omitted_matching_occurrence`,
`incomplete_translation_key`, `premature_zero_correlation`, and
`omitted_new_key_registration`.

The selftest fixture drives typed live-state mutations, reseals the resulting
object where applicable, and routes each one to its named owner.  The checker
repeats the owner dispatch independently.  The static result for every one of
the 48 routes is `rejected=true` with a narrow owner reason; no result is based
on a hash-only change, arbitrary exception, forced transcript, or producer
mutation flag.  Resource cap exhaustion routes only to `UNKNOWN_RESOURCE`;
malformed authority/runtime routes only to `UNKNOWN_INPUT`; unexpected
implementation errors are explicit `*_STOP` markers.

## Driver flow and execution status

The ASCII GAP driver rejects unresolved pins and stale v1/v2/v3/v4 output,
log, shell and sentinel paths.  It pins all five authority members plus E4,
q3, task176, the current producer, current checker and fixture.  GAP emits a
strict `set -eu; set -o pipefail` shell, executes exactly one bounded producer
and then exactly one bounded independent checker, requires one full-line
terminal per side, compares the terminal payloads, requires a nonempty sealed
checker verdict, and writes the sole sentinel last.  There is no sleep, retry,
poll, lock, pool, local parallelism or hidden mathematical subprocess.

No selftest or production command was authorized or run in this turn.  The
actual 1/3 A4 claim therefore remains unchanged; this report records only the
static positive/negative routes and implementation wiring.

IMPLEMENTATION:                  IMPLEMENTED
SELFTEST / PRODUCTION:           UNEXECUTED
AUTHORITY-V2 INPUT:              PASS / A4 1/3 only
ACTUAL POSITIVE BRANCH:          STATICALLY REACHABLE
ACTUAL A4:                       remains 1/3 at most before execution
LIFT / FAKE / IHARA:             NONE
