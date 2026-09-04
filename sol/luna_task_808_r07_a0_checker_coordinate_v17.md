# Luna Task808 — A0 v17: actual occurrence-coordinate checker repair

Role: minimal implementation/wrapper repair only.  Process all numbered
sections first to last.  Do not run GHA, commit, push, or change producer
arithmetic.  Modify only the new versioned checker/workflow and designated
reply named below.

## 1. Frozen evidence and parents

Read in full:

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py`
- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml`
- `sol/sol_reply_802_reaudit_r07_a0_canary_wiring_v16.md`
- `sol/sol_reply_804_root_r07_a0_v16_launch.md`
- `C:/Users/81905/Desktop/shadow-atelier-artifacts/gha/run33836732706-attempt1-task640-logs/producer.log`
- `C:/Users/81905/Desktop/shadow-atelier-artifacts/gha/run33836732706-attempt1-task640-logs/checker.log`

Run/attempt `33836732706/1`, job `100910685815`, exact head
`f72d9173ce2b90b6ce8ad137d4d82ff7b059fe53`, completed all 21,287 producer
aggregations in 889 seconds.  The independent checker then stopped with
`{"error":"'coordinate'","status":"NOT_READY"}`.  This is the only
commissioned checker defect.  Do not redesign the 23-call producer or its
21,287-bucket aggregation.

## 2. Create only these files

- `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml`
- `sol/luna_reply_808_r07_a0_checker_coordinate_v17.md`

Producer v9 must remain byte-identical and be reused by path/SHA.

## 3. Exact checker repair

Trace the actual `IndependentAllSeven.specs` constructor and confirm the first
exception.  The actual eleven records currently omit `coordinate`, although
`occurrence_prefix_contract` correctly requires it and the synthetic
`PrefixModel` fixture includes it.  Bind the frozen coordinate order

```text
(0,1,2,3,0,4,5,6,7,8,9)
```

to the actual spec construction, and require its complete tuple to equal
`TEN`.  Do not weaken/remove `occurrence_prefix_contract`, infer a coordinate
from a label after construction, or accept a missing field.

Add one bounded regression which traverses the same actual spec-construction
helper and then `occurrence_prefix_contract`; mutate one coordinate and require
rejection at the layout gate.  It must not run producer arithmetic or a
production-size checker replay.  Preserve all 55 prior mutations and the
five-field `base_receipt` repair.

Bump checker schema/marker/version pins honestly to v9.  Make no arithmetic,
source, bucket, parent, dimension, or terminal-claim change.

## 4. Resilient v17 wrapper without recomputation ambiguity

Clone v16 to v17 and update only honest version/path/SHA/bytes/LF/marker/fire
and artifact labels plus this bounded staging improvement:

1. run the unchanged producer v9 in its own step;
2. immediately authenticate its marker and upload the complete payload as an
   explicitly **unchecked candidate** artifact;
3. run checker v9 in a separate step against exactly that payload;
4. only after the checker marker, upload the accepted payload plus verdict;
5. upload producer/checker logs always.

The unchecked artifact must never carry an accepted/cross-checked label or
be consumed as a result.  Its purpose is only to avoid losing another
completed 889-second producer if a later checker wrapper fails.  Keep one
serial job, the 8-GiB virtual-memory cap, exact parent pins, bounded fixtures,
90-day retention, and all claim flags false.

## 5. Bounded checks

Run only checker py_compile/selftest and static workflow checks.  Also invoke
the new actual-spec regression directly enough to show the honest tuple
accepts and a coordinate mutation rejects.  Do not run the full producer or
checker locally.

In the reply give the exact first old failure and new accepting gate, mutation
count, producer unchanged SHA, checker/workflow bytes/LF/CR/BOM/SHA-256, and
terminal `READY_FOR_HOSTILE_REAUDIT` or `NOT_READY:<reason>`.  State that
fresh rho2, A0, COMMON, compatible lift, fake and Ihara are not claimed;
`verified=false`.
