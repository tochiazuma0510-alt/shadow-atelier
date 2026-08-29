# R07 A5/A6 v2 actual-owner static audit (368)

## F1. Verdict: STATIC REJECT at checkpoint (1)

The v2 pair is not an executable actual-owner compiler.  The first fatal
boundary is the task198 parser, before `E_pre` is constructed.  Therefore the
audit stops here, as commissioned; checkpoints (2)--(6) are not promoted by
this verdict.

The accepted physical task198 receipt
`ci/in/d972_r07_seven_context_roof_presentation_v1.json` has

```text
evaluator.context_maps = null
evaluator.joint_coordinate_image = null
```

and contains none of `action_edges`, `typed_action_edges`, `module_actions`,
`printed_block_map`, `block_map`.  This is not an accidental stale artifact:
the frozen producer initializes both serialized fields to `None` and populates
them only under `runtime.get("selftest_nonsplit") is True`
(`search/d972_r07_seven_context_roof_presentation_v1.py:842-846`).

By contrast, the A5 producer requires a nonempty serialized `context_maps` and
a non-null `joint_coordinate_image`
(`search/d972_r07_zero_base_a5_a6_compiler_v2.py:430-455`).  Its actual call
order is `pick_contexts` before `block_map` and `action_edges`
(`...compiler_v2.py:964-969`), so an otherwise correctly staged manifest using
the accepted task198 owner stops first as

```text
UNKNOWN_INPUT:task198:context_maps
```

The later requirements are absent too: `block_map` demands an externally
printed `printed_block_map|block_map|C` (`...compiler_v2.py:458-469`), and
`action_edges` demands `action_edges|typed_action_edges|module_actions`
(`...compiler_v2.py:647-668`).  The independent checker likewise demands the
same nonexistent action-edge roster
(`crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v2.py:447-467`).

These data can be injected only through uncommissioned manifest `spec`/
`runtime_overlay` fields.  Such an overlay is neither part of the accepted
task198 receipt/verdict pair nor present physically: the driver's default
`ci/in/d972_r07_zero_base_a5_a6_compiler_v2.actual-input-manifest.json` is
currently absent (`...gha_driver_v2.g:13-15`).  Calling those injected values
"actual task198 owner fields" would therefore be false.

Consequently `sol/luna_reply_360_r07_zero_base_actual_a5_a6_v2.md` is wrong in
claiming that the bound task198 receipt supplies typed context maps,
joint-coordinate image, and affine action edges.  This version must not be
committed/dispatched as an A5 candidate.  No MEMBER/NONMEMBER, A5, or A6 claim
is obtained.

Minimal repair boundary: either consume and independently replay task198's
real executable ABI (`module`, `runtime_constructor`, `registry_callable`,
entry points and frozen sources), or first produce a separately sealed and
cross-checked serialization owner for the required action/block maps.  Do not
silently manufacture them in the input manifest.

Audit mode: static source/physical-schema inspection only; no Python/GAP/GHA
execution and no SELFTEST/generalization.

`R07_A5_V2_ACTUAL_OWNER_STATIC_REJECT_TASK198_FIELDS`
