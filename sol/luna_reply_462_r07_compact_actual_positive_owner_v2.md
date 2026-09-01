# Luna reply 462 — compact actual positive owner v2

Status: IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN.

This is a guarded successor of the adopted Task458 v6 actual engine.  It
authenticates the full Task193/Task198 authority first, constructs Runtime and
BoundaryLedger from the original authority, then gives DirectEngine only a
read-only 44-row Task411 proxy.  The inherited actual `relator_seed`, marked
action, target oracle, translated PB boundary, proof DAG, `_member`, and
checker-side replay remain unchanged.  Misses are
`UNKNOWN_INCOMPLETE:compact_direct_span_exhausted`; NONMEMBER is not emitted or
accepted.  The owner is `resumable=false` and creates no checkpoint.

## Physical and generated pins

Inherited Task458 v6:

```text
producer 2342 32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c
checker  2334 a4db1b2b1ad5da1135c8ebcef1898c46fd07df7ebdbfa8778bd36a6098507bc3
driver   2106 212c76f2ca2e06df1aae2b2d783a15fcf1d4e5041d70cba26198d64d9bd4d4d6
generated producer 59382 83b31959a0c35bdeb1e2569e0ee384b116ed6ed0b7d57e9c363cecdc29fcfe87
generated checker  45888 cf44a9a8397eebf99271a4444bb41bd300fe5cfa60cc00696e9811a1469b52c7
```

Task411 roster owners:

```text
producer search/d972_r07_a0_compact_pc_invariant_owner_v1.py
        68222 be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9
checker  crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py
        44831 7c1aea086ce264ad6f51983554a3a371ac481d07a2ec5f5d9a96ee270af6dfcf
roster count 44
roster sha256 7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8
```

New outputs:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_compact_direct_relator_a5_a6_positive_v2.py` | 7707 | `47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3` |
| `crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v2.py` | 7720 | `535c7b8aa0983748204d0e381d367d3398380ea3097cd48ef374dfc3daf38c67` |
| `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v2.g` | 3763 | `1f6a5c51e382ffcb063bbb0b150073e6bc499662182a35f58b3b8f32f00e0d88` |
| `sol/luna_reply_462_r07_compact_actual_positive_owner_v2.md` | pending self-pin | pending self-pin |

Generated v2 bodies are guarded as:

```text
producer 61341 289dbff63af59daec0478bdc6eee376b711c4b944fee08d671b3e10a323b5539
checker  47815 ee826f1873e045574838e4fd478530edf2ef5986683c7f0ad72cf4958baac262
```

## Bounded commands

```text
$env:PYTHONPYCACHEPREFIX=(Join-Path $env:TEMP 'compact-v2-final-pyc17')
python -m py_compile search/d972_r07_compact_direct_relator_a5_a6_positive_v2.py crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v2.py
PASS

python -c "import runpy; ... run_name='not_main' ..."
producer_load 61341 61341
checker_load 47815 47815

python -c "... CompactAuthorityProxy ... rows==44; delegated receipt/identity/meter; row and attribute mutation reject ..."
PROXY_DELEGATION_IMMUTABILITY_PASS
```

Static scans passed: driver is ASCII-only, requires Task193 receipt/verdict
inputs, passes 14,400 seconds and 5,700,000,000 RSS bytes, has no resume or
checkpoint route, starts one producer process, invokes the checker only for
MEMBER, and accepts only the specified UNKNOWN_INCOMPLETE/UNKNOWN_RESOURCE/
UNKNOWN_INPUT nonpositive classes with NONE/false frontier claims.

No production runtime, Task193/A5 closure, GHA dispatch, workflow edit,
commit, or push was performed.  Production runtime and memory are unknown
until GHA execution.
