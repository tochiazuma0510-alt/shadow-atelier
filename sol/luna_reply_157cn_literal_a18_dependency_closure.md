# 157cn — literal A.18 dependency-closure v2

## Verdict

The versioned v2 lane is ready.  It delegates the already-audited literal
18+140 A.18 producer and the independent tuple-based checker without changing
their mathematics.  The new wrapper authenticates the recursive local file
closure before either dynamic import, and carries that authentication into
the shard receipts, the complete merge shard ledger, the merge receipts, the
checker aggregate, and the final workflow aggregate.

## Recursive closure

The closure bound in each v2 receipt is

| role | repository path | SHA-256 | provenance |
|---|---|---|---|
| parent producer | `search/d972_b4_next_obstruction_v1.py` | `bbf91f461e0c0d9d67ea49186450e709fcb97025ac4ebc3462b3dc6c278eb886` | tracked at supplied parent commit `0e0b0b0855f3c42c00c614b863ff0e14368734da` |
| parent checker | `search/check_d972_b4_next_obstruction_v1.py` | `2cd42ed369d9bb946f474cc6c10d90aaa4a32ab53e299c190763749a07660994` | tracked at supplied parent commit |
| Magnus shard core | `search/d972_b4_magnus_ideal_shard_v2.py` | `1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63` | tracked at supplied parent commit |
| streaming merge core | `search/d972_b4_magnus_ideal_merge_v3.py` | `6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5` | tracked at supplied parent commit |
| base merge core | `search/d972_b4_magnus_ideal_merge_v2.py` | `c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c` | tracked at supplied parent commit |
| transitive base producer | `search/d972_b4_magnus_ideal_v1.py` | `b2e5184e31e177dcf5bfdc9fcd715e2146db877e0eccda2056cc5d7f999ae6bc` | the one explicitly authorized unchanged dependency |
| frozen Magnus input | `search/certs/d972_b4_p2_magnus_input_v2_20260816.json` | `c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9` | tracked at supplied parent commit |
| frozen word artifact | `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` | tracked at supplied parent commit |

The recursive import audit found no other repository executable import:

`v2 producer → v1 producer → {shard core, streaming merge core} → {base merge core, base producer}`.

The shard core and base producer have only standard-library imports.  The v1
checker has no repository import.  The v2 checker authenticates the same
closure before importing the v1 checker.  The receipt field
`unbound_executable_imports` is therefore the empty list; an absent, changed,
or unlisted executable dependency fails before execution.

## Receipt and fail-closed repairs

`search/d972_b4_next_obstruction_v2.py` preserves the v1 campaign contract:

- literal A.18 is still 18 prefix rows plus 140 raw coface rows;
- the unconditional five-coface D-tilde has 972 rows;
- degrees are exactly 2, 3, 4, 5, and 6, with the exact 16-way d6 partition;
- rho is still excluded (`rho_used=false`, `rho_tail_used=false` and the
  original omission role);
- all existing v1 relator, ideal, partition, and status gates remain active.

The new closure and its digest are attached at the top level, each degree row,
and each shard ledger record.  Merge refuses a shard lacking the same closure
before it invokes the v1 merge.  The checker first validates those annotations
and then checks annotation-stripped temporary copies with the independent v1
ideal reconstruction; this preserves the v1 exact shard-record schema while
making the new provenance mandatory.

Both v2 selftests mutate/remove the base-producer entry at top, degree, and
shard-record levels.  Every mutation is rejected on a synthetic
`D2_ALLPASS_UNKNOWN` (zero-defect) receipt, so an all-pass mathematical status
cannot bypass the dependency gate.

## Workflow and bounded checks

`.github/workflows/d972-b4-next-obstruction-v2.yml` keeps the 20-shard matrix,
the exact d2–d5 singleton and d6 16-way partition, merge, independent checker,
and final aggregate.  Every action is pinned by immutable SHA.  The first
shard step hashes both v2 wrappers, all v1/core files, the authorized base
producer, and both frozen data files before running either selftest.  The
merge/check/campaign jobs repeat the relevant closure checks and validate the
base entry in the aggregate.

Performed locally within scope (no Git, GHA, GAP, or d3–d6 computation):

- producer dependency selftest: pass;
- independent-checker dependency selftest: pass;
- YAML parse: pass;
- all five embedded Python heredocs: AST parse pass;
- temporary d2 shard replay: pass (`ideal_rank=27`);
- temporary d2 merge replay: pass (`D2_ALLPASS_UNKNOWN`);
- replayed d2 merge receipt: closure tree and authorized base SHA pass.

Created versioned files only:

- `search/d972_b4_next_obstruction_v2.py` — `85e2c3e954a2778579fcc3fa6d375a44effb49d34bf87b7e9c391970d2639f98`
- `search/check_d972_b4_next_obstruction_v2.py` — `5c746220d3ef4e0bfb458b9736e03fd3e8553421603c3d8b87a12e4a7e893181`
- `.github/workflows/d972-b4-next-obstruction-v2.yml` — `6b2124311565c9c64a44efbfd0967b75e87d0e2e33d15a5eeb54fb7a475291da`
- this reply

The parent may stage those four files plus the unchanged authorized base
producer; no existing v1 file was edited.

LITERAL_A18_DEPENDENCY_CLOSURE_READY
