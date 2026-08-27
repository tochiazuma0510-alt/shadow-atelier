# Luna reply 175 - R07 all-seven raw bridge preflight v1

Date: 2026-08-27
Role: bounded mechanical/static implementation repair (175b).

## Result

All five authorized task-175 files now contain the bounded production path and
the roster guard repair.  The latest parent production artifact (run
`33034678957`) completed the driver successfully but stopped at the typed
terminal `UNKNOWN_INPUT:RAW_FORMULA`; this is not mathematical evidence.
The producer has `--run-preflight --output`; the checker has
`--check --receipt --output` and a cheap fixture path.  No Python, GAP, Node,
Git, or GHA process was run in this turn.  The checked-in receipt therefore
remains the fail-closed fixture:

```text
UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD
```

No positive mathematical result is claimed.  Orbit images, membership,
column generation, affine solving, correction search, lifts, cofinal claims,
fake claims, and Ihara witnesses remain outside this preflight.

## Final artifact hashes

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_all_seven_raw_bridge_preflight_v1.py` | 55259 | `7fbc431217bf5992c90821930e927baa12f4a187f8f3c53c0859b5ed4843fee7` |
| `crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py` | 77970 | `4b52450c547834725fd61b874976ba1a60435bde60cc868a2ee7913a3c0ad9d8` |
| `search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g` | 14855 | `9ef865faaed354d4e41b95571a8272a57fa623eeb53fc6036de0e9506130f47d` |
| `search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json` | 6870 | `0d9a9588cd4f58531923dc208819f32d552006eea8e323a198382901d132c69f` |

The reply file is intentionally the last edited report; its byte count and
hash are to be taken from the parent static audit after this write.

## Independent checker audit

The checker contains local implementations of free reduction, inverse,
substitution, paper products, g760 reconstruction, permutation composition,
PC collection, E3/E4 quotients, cofaces, the v122 coarse/fine retraction,
the 31/46 context registry, literal hexagons and pentagon, left Fox,
translation, D1, D2, and serialization.  It reads pinned files as data only.

Static import scan: local standard-library imports only; zero `importlib`,
`exec_module`, `module_from_spec`, source-loader calls, or executable imports
of the producer, v172, g760, joint-kernel, PB4, or triple-cube modules in the
checker.  The predecessor paths occur only as authenticated data pins.

The checker reconstructs all 26 nonempty correction records and losslessly
retains all 6,441 signed rows (`6318 + 104 + 19`), including rows whose free
reduction is the empty word, and directly evaluates every retained joint word.
It selects the first deterministic nonempty row only for the typed correction
witness and Fox samples.  It retains five source pairs, five pentagon pairs, all 46 named
uses and 31 exact E4 rows, all retraction marks and PC preimages, two PB3 and
eleven PB4 raw columns, three raw base targets, three direct changes, three
prefix changes, the tagged stacked target, and the corrected word
`reduce(g760*c)`.

Both implementations build the direct pentagon words from the fresh literal
`paper_product(b1,b2,b3,inverse(b5),inverse(b4))` constructor; the natural
factor indices are `(1,3,0,2,4)` with signs `+++--`, and the ordered product
is checked against that exact signed word.  The correction-side mutation keeps
the registered `c` fixed and tests `reduce(c+g760)` against canonical
`reduce(g760+c)`.

The Fox transcript is fixed to the inventory printed order
`H1(3), H2(3), b1, b2, b3, b5^-1, b4^-1`: ten actual nonempty-conjugator
pairs per slot, 110 total, stratified over gamma-edge, xy-action, and
Q0-relator rows.  It includes two same-complete-context/different-conjugate
pairs and a separately labelled actual-product additivity check.

The semantic mutation suite contains 19 attempted/rejected cases:

```text
correction_left_right, corrected_base_sign, H2_u_z, inverse_fox_prefix,
negative_pentagon_factor_4, negative_pentagon_factor_5,
negative_pentagon_order, coface_slot_1_3_swap, E3_E4_rank_swap,
E3_E4_blob_swap, context_name_only_dedup, dropped_block_tag,
fourth_third_deletion_swap, fine_insertion_index_4_3_swap,
derived_u_order, derived_z_order, one_actual_roster_letter,
actual_product_additivity_term, terminal_marker
```

Each non-envelope mutation changes a load-bearing formula, map, word, rank,
blob, or execution branch and is sent through reconstruction and validation;
no receipt-field-only mutation is used for these controls.

## Production roster diagnosis and repair

Run `33034678957` wrote producer log `D175_PRODUCER_DONE` followed by
`UNKNOWN_INPUT:RAW_FORMULA`, and its minimal receipt reason was
`UNKNOWN_INPUT:RAW_FORMULA:roster`.  Static source comparison isolates the
guard: pinned v172 `build_roster` enforces the 6,441 count but does not require
each expanded row to be nonempty, whereas task175's wrapper added
`any(not r.get("word") for r in roster)` and stopped there.  The pinned q3
format also has a leading empty placeholder record, while the 26 word records
are deliberately selected by the existing nonempty-record manifest.  The
expanded roster must remain lossless, so an empty reduced row is retained.

The producer and independent checker now use count plus full joint evaluation
for all 6,441 rows, choose the first deterministic nonempty row for the
correction witness, choose nonempty rows for all 110 Fox samples, and target
that same witness in the actual-roster-letter mutation.  The receipt contract
records this explicitly as `nonempty_scope`; READY gates remain fail-closed.

## Pins and GHA contract

The task/ruling pins remain exact, including 175b
`a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836`, v173
`189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695`, PB3
v121 `efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5`,
bridge v122 `daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348`,
checkpoint v123 `272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac`,
PB4 v108 `4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f`,
q3 `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`,
and 157ee `1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`.

The authenticated implementation sources are g760 33,409 bytes /
`f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f`, joint
kernel 67,945 bytes /
`06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc`, PB4
444,497 bytes /
`b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7`, and
triple-cube 126,942 bytes /
`d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db`.

The ASCII GAP driver uses generic `.github/workflows/gap-run.yml`, rejects
pre-existing driver outputs, binds
`D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE` before `Read`, dispatches
exactly once, and runs one producer followed serially by one checker under:

```text
timeout 9000s bash -o pipefail -c 'set -euo pipefail; ...'
```

Production writes one receipt path and separate logs/verdict/sentinels.  It
requires exactly one `D175_PRODUCER_DONE`, one `D175_CHECK_PASS`, one allowed
terminal, and exact receipt/checker terminal agreement.  READY receives the
full lossless receipt JSON gate; each registered typed UNKNOWN receives the
static/minimal gate and is preserved as an honest fail-closed result.  Both
branches write the final `D175_DRIVER_PASS` sentinel at
`ci/out/d972_r07_all_seven_raw_bridge_preflight_driver_pass_v1.done` after
hash/verdict capture.  Selftest writes a separate selftest receipt and
requires `D175_PRODUCER_DONE` plus `D175_STATIC_CHECK_PASS`.  Estimated
external runtime is bounded by 9,000 seconds (2.5 hours), serial; this
heavy-lane allowance covers the canonical replay plus 19 semantic
reconstructions of the 6,441-row roster and Fox transcript.  RSS is UNKNOWN
until GHA records it.  `GHA dispatched=false`.

## Terminals and remaining UNKNOWNs

The only positive terminal is `R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY` and
is not present in the checked-in fixture.  The remaining runtime UNKNOWNs are
the E3 context/retraction replay, PB3/PB4 raw-column replay, complete roster
and direct formula replay, 110 Fox canaries, and all 19 mutation executions.
They are fail-closed typed inputs/resources, not nonexistence or mathematical
negative results.  All promotion boundaries remain false.

R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_STATIC_READY

## Parent GHA execution

The parent committed and pushed the pre-repair static bundle at
`dacb0f687aafb280b5cfc7540066a33ddb4fe157`.

The first SELFTEST dispatch, run `33034469339`, failed before reading the
task driver because the workflow input lost the quotes around the GAP string
`SELFTEST`; GAP therefore treated it as an unbound variable.  No producer,
checker, or mathematical replay ran in that attempt.  The code was unchanged.

The quote-free equivalent binding by `List([...],CharInt)` was then used.
SELFTEST run `33034589606`, at the same commit, completed successfully.  Its
uploaded artifact records:

```text
D175_DRIVER_PASS
mode=SELFTEST
terminal=FIXTURE_PASS

D175_PRODUCER_DONE
UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD

D175_STATIC_CHECK_PASS
terminal=FIXTURE_PASS
```

The bounded fixture result additionally records `pins_authenticated=16`,
`fox_d1=true`, `mutation_path=semantic_local_toy`, and
`serialized_components=3`.  This is a driver/checker selftest only.

After that success, the parent dispatched the serial production preflight:

```text
run id:       33034678957
commit SHA:   dacb0f687aafb280b5cfc7540066a33ddb4fe157
mode:         PRODUCTION
workflow:     gap-run.yml
out_dir:      ci/out
timeout_min:  180
packages:     false
status:       completed_success_with_typed_unknown
```

The artifact's driver pass was terminal-agreeing
`UNKNOWN_INPUT:RAW_FORMULA` and the producer/checker logs were preserved.  No
READY, correction, lift, fake, or Ihara claim is made; a post-repair GHA run is
required before any READY terminal can be considered.
