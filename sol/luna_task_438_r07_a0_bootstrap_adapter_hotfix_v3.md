# Luna task 438 - Task436 selective bootstrap-adapter hotfix v3

Task437 v2 run `33405554013`, job `99532138064`, passed the p176 adapter,
compiled all 44 formulae, and then stopped before Q0 with exact producer
reason `KeyError('load_json')`.  The 44 records have 1,060,263 merged targets
in total (maximum 95,736; 42 nonempty seeds).  The failing v1
`selective_runtime` asks `base["load_json"]`; the authenticated loader is
actually `t413["load_json"]`, as shown by task435 `bootstrap` lines 43--49.

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_actual_b72_first_active_v3.py`
2. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v3.py`
3. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v3.g`
4. `sol/luna_reply_438_r07_a0_bootstrap_adapter_hotfix_v3.md`

Do not overwrite v1/v2 or modify any other file.  No local production,
commit, push, dispatch, download, workflow edit, or heavy bootstrap.

## 2. Producer wrapper

Byte-pin the exact v1 producer (24,643 bytes,
`5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc`).
Use the v2 thin-wrapper design, but make one explicit `adapt(P)` gate that:

1. wraps `P["p176"]` in v1 `_P176Adapter`; and
2. shallow-copies `P["base"]` and inserts
   `P["base"]["load_json"] = P["t413"]["load_json"]`.

Patch the v1 prefix with this adapter before `m.run`.  Preserve the quotient
and every v1 mathematical/selector/checkpoint/status gate.  Use v3 schema,
marker, artifact, and checkpoint paths.

The bootstrap-free fixture must call `adapt` on a toy dictionary and require
both attribute access `p176.value_from_blob` and the injected `base.load_json`
identity before delegating to the v1 72-point fixture.  Thus this exact pair
of GHA failures is now exercised locally.

## 3. Independent checker wrapper

Byte-pin the exact v1 checker (13,834 bytes,
`3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916`).
Define an independent dict-plus-attribute class and independent `adapt(P)`
with the same two ABI results.  Wrap only checker `bootstrap`, preserve all
v1 checker gates, and use v3 schema/marker.  Its `--self-test` must first run
the toy two-key adapter test and then the unchanged ten mutation rejections.
Do not import the producer wrapper.

The checker needs the `base.load_json` insertion because its direct ACTIVE
ten-coordinate replay also reads Q3 through that bound base.

## 4. Driver and bounded gates

Create a v3 driver with exact wrapper pins, external v3 preamble, fresh v3
JSON/checkpoint/log paths, 2,400-second/4.8-GB producer caps, checker PASS
marker, and unique driver PASS marker.  Run only syntax compile, the enhanced
producer fixture outside the repository, enhanced checker self-test, static
pin/command reconstruction, and `git diff --check`.  No Q0, formula rebuild,
prefix, production, or new framework.  Report exact bytes/SHA-256.
