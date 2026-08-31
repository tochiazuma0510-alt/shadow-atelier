# Luna task 437 - Task436 p176 attribute-adapter hotfix v2

Task436 v1 was independently audited and dispatched at source commit
`695310b7a7c28462145fe3827eb5181869020701`.  GHA run `33403284390`, job
`99524587327`, stopped after the authenticated prefix with producer reason

```text
'dict' object has no attribute 'value_from_blob'
```

The failure is at the task179 `AllSevenModel` ABI: its `unpack_element` and
`element_blob` use attribute access on `runtime["p176"]`, while Task436 v1
passes the bound-module dictionary.  The v1 `_P176Adapter` already supplies
the required dict-plus-attribute interface.  Mathematics, selector, and
resource design are unchanged.

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_actual_b72_first_active_v2.py`
2. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v2.py`
3. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v2.g`
4. `sol/luna_reply_437_r07_a0_p176_adapter_hotfix_v2.md`

Do not overwrite v1 or modify any other file.  No local production, commit,
push, dispatch, download, workflow edit, or heavy bootstrap.

## 2. Producer wrapper

Byte-pin and load the exact v1 producer:

```text
bytes  24643
sha256 5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc
```

Use a small versioned wrapper, not a copied 24-KB implementation.  Wrap the
v1 `prefix` result so `P["p176"]` is v1 `_P176Adapter(P["p176"])` before
`model179` is called.  Preserve the already constructed quotient object and
all v1 algorithms.  Change the public schema/marker to v2.  The driver passes
explicit v2 artifact/checkpoint paths, so no v1 path may be reused.

## 3. Independent checker wrapper

Byte-pin and load the exact v1 checker:

```text
bytes  13834
sha256 3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916
```

Define an independent local dict subclass with `__getattr__`, wrap only the
`p176` entry returned by the v1 checker `bootstrap`, and preserve every v1
prefix/adjoint/formula/ACTIVE/EMPTY gate.  Change schema/marker to v2.  Do
not import or share the producer wrapper.

## 4. Driver and bounded gates

The v2 driver must pin the two wrappers, require an external v2 preamble,
use fresh v2 JSON/checkpoint/log paths, invoke producer with 2,400 seconds
and 4.8 GB, invoke checker, and require unique v2 PASS markers.  It must not
invoke v1 paths directly except through the wrappers' byte-pinned imports.

Run only syntax compile without repository bytecode, producer fixture to a
temporary output outside the repository, checker self-test, reconstructed
driver command/static pin check, and `git diff --check`.  Report exact bytes
and SHA-256.  This task repairs one ABI mismatch only; no resume framework,
selector rewrite, new audit infrastructure, or unrelated optimization.
