# Luna Task645: Task640 v3 finite release repair after Task644

Role: Luna implementation. Read this mail and the complete Task644 reply,
then repair the still-unaccepted Task640 v3 quartet in place. This is one
finite release repair, not a redesign. Modify only:

1. `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
2. `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
3. `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml`;
4. `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md`.

Do not create another implementation version, edit proofs/v220/Task644, run
production/GHA, or use git. Keep all already-correct Task640/643 semantics,
dimensions, exact per-key direct canaries, serial resource model and false
claim boundary. Run only bounded serial fixtures/static checks.

## 1. Exact eight repairs

Implement F644-1 through F644-8 completely and minimally.

### R1. Task595 artifact name

Download the actual exact artifact
`task595-grade1-decision-v2-candidate-33707397894-1`; do not use the
nonexistent `decision-v3` name.

### R2. Task625 live envelope

Before download, query and require the exact Task625 job and payload artifact
metadata:

```text
run/attempt/job 33734643746/1/100582244001
head b401d724bbdbef8cf67e96def22fc51c014ab546
job name selected-slp; conclusion success
artifact id 9885925239
name task625-grade1-selected-slp-staged-v3-33734643746-1
archive bytes 50793121
digest sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75
expired false; workflow_run id/head equal the above run/head
```

Retain the existing run/name/content gates. Put the exact artifact
id/size/digest and job identity in the producer parent receipt and require the
same complete parent object in the checker.

### R3. Source-before-group ordering

Let `raw_terms` be the separately authenticated ordered prior terms followed
by the raw `R07LEAF1` terms. Derive the endpoint-gate seed set from
`raw_terms` before any exact-key cancellation. Then form the canonical
nonzero exact-key evaluation map. Run the direct all-seven canary for every
nonzero exact evaluation key before constructing signature buckets. Only
after those gates may `(seed,Sigma_11)` buckets be formed. Apply this exact
order independently in producer and checker.

### R4. Checker dense replay by its own buckets

The checker must pass its own independently recomputed nonzero signature
buckets, with their coefficients and retained representative paths, to the
dense replay. It must not dense-act all roughly twenty thousand exact keys
and must not treat the producer bucket file as arithmetic authority. Keep the
separate required sparse direct canary on every nonzero exact key.

### R5. Genuinely independent endpoint checker

Remove `SevenSources.load`/dynamic `exec` and every live execution/import of
the producer-shared semantic modules (`old`, `joint`, `v172`, `g760`, `pb4`).
Implement locally in the checker only the operations actually needed for the
eleven endpoint/direct-versus-occurrence path: finite marked quotient/group
operations, word reduction/inversion/product, F2 substitution, PP/PB3 lift,
Fox gradient/translation, E3/E4 reconstruction, joint endpoint, hexagon and
pentagon words, prefixes/signs and the direct/occurrence comparison. Parse
exact pinned JSON/tables as immutable data when useful; the already pinned
`scratchpad/a0_paper_words_v1.json` supplies exact `g760` and relators.

Do not copy in a generic unused package or rebuild the old full v13 checker.
Delete shared-source execution and unused target/boundary/roster work from
this endpoint-only path. The existing checker-local truncated-ring, dense
target/action, aggregation and packing implementation remains. A source file
may be hash-pinned as provenance, but none of its Python functions/classes
may execute as the endpoint authority.

### R6. Complete manifest equality

Give the payload manifest an exact allowed-key/schema contract. Independently
recompute and equality-check:

- the full parent run/attempt/head/job/artifact/source/candidate and decision,
  basis/remainder/verdict bindings;
- root label and source/roots digests;
- the eleven types, coordinates, signs, raw-source base-check count,
  all-seven and first-six flags;
- exact `L/U/G`, `G<=L`, and seed cache count;
- dimensions, both positive degree-one gates, coefficient count and
  lower-zero gate;
- every target/lower/top/sparse/packing receipt and rho2 field; and
- every required false/null claim.

The exact rerun-and-byte-equal Task625 verdict is the compositional witness
for the two degree-one gates; seal its digest. Do not restore graph traversal.

### R7. Remove ancestry DOM and make caps live

Stream-hash `source-ancestry.json` once as part of the exact receipt roster;
do not `read_bytes`, `json.loads`, canonicalize or retain it. Bind its frozen
SHA in the `R07LEAF1` header and child manifest. Remove the now-unused live
ancestry argument and dead graph-replay functions if simplest.

In both executables wire bounded, adjustable caps into actual counters:
record count during `R07LEAF1` parsing, unique complete paths, trie prefixes,
and live evaluation/signature state. Use the existing environment names and
return `UNKNOWN_RESOURCE:*` on exhaustion. Do not parse the parent graph just
to manufacture a state count. Add a small path-length cap only if required
by the live parser. Keep caps above the accepted parent values.

### R8. Bounded live-predicate fixtures

Factor only small validators already needed by production and drive the
Task640 Section 5 mutation roster through those same predicates. Cover
occurrence omission/permutation, slot-1/5 distinction, E3/E4, sign,
inverse/PP/block/prefix/right-multiplication order, nonidentity block product,
premature signature merge, failed raw seed gate, missing/swapped roots,
malformed leaf/header/record/EOF and ancestry binding, parent/envelope and
manifest mutations, target/lower/top/packed receipt mutations, and every
false/null claim. These fixtures must stay tiny and serial; do not build the
real groups, graph, ancestry or dense production row in selftest.

## 2. No new scope

Do not add a grade-two membership calculation, full module/closure, graph
traversal, production checkpoint system, SAT layer, generic framework or
large selftest. Producer-side exact-pinned v12f use remains permitted. The
result remains only a fresh-rho2 candidate input to v474.

## 3. Handoff

Run and report serial `py_compile`, both bounded selftests, YAML safe parse,
immutable-action and workflow-hash checks, forbidden-import/exec scans,
whitespace, exact bytes/lines/SHA-256, and a static memory explanation. The
reply must explicitly map all `R1..R8` to code locations and end
`READY_FOR_TASK646_REAUDIT`. No production result is claimed.
