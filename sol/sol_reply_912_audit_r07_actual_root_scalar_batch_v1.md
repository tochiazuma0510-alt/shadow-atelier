# Sol reply -- Task912 hostile audit of actual root-scalar batch v1

## Ruling

FAIL.  The actual arithmetic path is correctly pinned, its packed projection
kernel and blockwise scalar formulas pass, and the workflow itself has the
right parents and bounds.  Two commissioned acceptance gates nevertheless
fail: the independent checker does not check several launch/result and upper-
claim fields, and both advertised bounded selftests report several mutation
controls as `true` without executing them.  These are narrow checker/test
repairs; no mathematical or production-algorithm rewrite is required.

I did not run or download any actual large parent.

## Audited file receipts

| file | bytes | LF | CR | SHA-256 |
|---|---:|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v1.py` | 55,908 | 1,010 | 0 | `1be672444dc23f0912014f1a6aea858fd367c760c466506538471a331145ec96` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py` | 51,979 | 866 | 0 | `6317970ba964109199e70727b331974a41718762f1e06fabdb1bf958847123be` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml` | 23,735 | 433 | 0 | `cfa9814863e2c61db3158b5940854b72e9c0cd0bbd4b0ab53ea4a29fa7a238c3` |
| `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md` | 4,208 | 48 | 0 | `d43af0b0af9cc5a1c0617233447d7509ebc92137df9bd0117e2c7c39b003c329` |

All four have no BOM.  The reply's prose is visibly mojibake, but its numeric
receipts and conservative claim block are readable; that presentation defect
is not the reason for this verdict.

## Gate 2 -- PASS: exact parents and same objects

The source constants and workflow agree on every commissioned outer identity:

```text
P1       33851744070/1  6673eb2ea15ca6022acc2ddc5a8a204a0380172f
          artifact 9931437113, bytes 641518300
          sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c
Task554  33677346616/1  22c6dddb43d107c05e65f53ad898823ae8ebe276
          completed/failure; artifact ids
          9865061266,9865238399,9865242284,9865193269,9865239848
Task712  33814194630/1  5ff2c5a30b604536df12acba8801828a5a7e5fe0
          artifact 9915928157
          sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858
separator 33891714539/1  7b7b9de20faaa3b8f26e331bb738b374f6f5708c
          artifact 9944214057, bytes 107195261
          sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017
```

The five Task554 archive byte/digest pairs are exactly

```text
204360988  sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4
 81729645  sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838
 82259824  sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb
 82200189  sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d
 82266526  sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92
```

The API predicates bind repository, workflow path, run/attempt/head,
status/conclusion, artifact id/name/size/digest, expiry and repository linkage
before download.  P1, each Task554 state, Task712 and separator use distinct
download roots.  The launch has no semantic input selector and requires
`fixture_only=false`, `mode=actual`.

Before interpretation, the executables authenticate the fixed P1 manifest,
292,444,992-byte cache and 349,055,442-byte instruction stream; all five
Task554 body hashes and HEAD/prepare-parent joins; the complete Task712
envelope; and the fixed separator manifest, 16,377,984-byte physical store,
lambda, terminal, result and checker receipts.  Both sides stream all 1,354
physical rows and require zero lambda pairing.  No private 16-row or old A0
path is reachable.

## Gate 3 -- PASS: covectors and packed P1 kernel

Producer and checker separately use their pinned v15 arithmetic sides to form
`B_fwd^T lambda` and then the four `T_fwd^T` children in order
`[1,-1,2,-2]`.  All Task909 root/support/lead and child hashes are hard
requirements.  Each root `RawDual` has `actors=[]`,
`actor_table_identities_along_w=[]`, and no predecessor; child table identities
are not put into the root.

I independently compared both actual vectorized kernels with a scalar dense
decoder on 257 canonical packed rows, split as a full 256-row chunk plus the
one-row final chunk, at all four byte offsets and five slots.  Results were:

```text
producer independent_dense_4_offsets_256_plus_1=PASS
checker  independent_dense_4_offsets_256_plus_1=PASS
maximum possible uint32 row sum = 36288*2*2 = 145152 < 2^32
```

The offset is `character*9072`, and digit extraction is exactly
`(byte // 3**(index%4)) % 3`.  The final partial chunk is reshaped with its
actual row count.  All twenty result arrays are allocated with deterministic
zeros, and only the five authenticated nonzero character-0 covectors are
projected.  Each executable hashes the instruction stream once and streams
the cache once; there is no per-character or per-covector cache reread.

For reference, the independently reconstructed character-0 root has raw hash
`af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053`.
Its root RawDual seal is
`c19d8972ea9185628a3ae1f67d30da589cc7e47f5a707a0810e23c84ce244dd3`.

## Gate 4 -- PASS: blockwise scalars

The implementation matches v540/v15 entry by entry.  It uses old offsets
`[0,505,1008,1511]`, new offsets `[2014,3523,5035,6547]`, 44 seeds, 2,014
old rows, 6,045 new rows, 8,232 origins and 32,280 scalar slots.  Every term
is subtracted.  Each seed receives all `4*4=16` new-block expressions; each
old actor receives four new-block expressions; a new actor uses only its own
block.  `global_row` is computed from block offset plus pivot, so the unused
telemetry cursor cannot shift within the four slots.  The final scan is seeds
first, then rows and actors in the registered order.

Only prepare and the current parsed block are referenced.  No global nested
relation tree, simultaneous four-block parse, or dense defect matrix is
created.  Both independent source functions give the q-independent fixed
relation receipt
`47effc68794b6d5d9616d5378396a7f10a5d9e0412bfe2ccf95c7e67b1fcf8dc`,
which binds the five ordered exact body digests and all ranks, offsets,
orders and counts.

## Gate 5 -- FAIL: checker permits resealed false joins and claims

The producer's honest continuation arithmetic is correct.  For the actual
lead/value `3/2`, it records scale 2 and permits reconstruction of `2*q` from
the authenticated raw root file.  The normalized packed SHA-256 is
`e25314e3598b7105771aa55f51681c3d3adbb7a9d14ab2cb4d0e8a6051d86afe`,
distinct from the raw hash, and the rank-zero next rolling head is
`0b0c1f55717402da576f1def12bab089985b05c184338c0bbc1da910f1c9308d`.
The terminal also correctly says that a root EOF leaves 503 independent rows
and is not a complete orbit EOF.

The independent checker does not, however, require the result's
`launch_sha256`, `separator_manifest_sha256`, `p1_manifest_sha256`, or
`task712_manifest_sha256` values to equal the authenticated parents.  It also
checks only `verified=false` among the terminal's claim fields; it does not
require the terminal's Grade-2, A0, COMMON, cofinal-lift, fake, Ihara,
candidate or complete-orbit fields.  Nor does it require the manifest's
terminal field to equal the recomputed terminal.

This gives concrete same-roster resealing attacks.  Changing only
`result.launch_sha256`, then resealing result and its manifest receipts,
passes every displayed `check_output` predicate.  Likewise an attacker may
change `terminal.GRADE2_MEMBER` or `terminal.A0`, reseal terminal, update its
receipt and SHA in result, reseal result and manifest, and retain every field
the checker actually compares.  The checker would accept a published false
upper claim.  A self-consistent seal is not an independent parent/claim
check.

## Gate 6 -- FAIL: required selftests are telemetry, not tests

Bounded compilation and the two public selftests exit zero:

```powershell
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'shadow-atelier-task912-pycache'
python -B -m py_compile search/d972_r07_actual_grade2_root_scalar_batch_v1.py search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py
python -B -u search/d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
python -B -u search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
```

The compile and both processes passed in 4.9 seconds, but their reported
coverage is not real.  The producer constructs tiny `terms`, `values` and
`cache` objects and never calls the scalar scanner with them.  Both files
then return literal `true` for seed/actor violation, all-four EOF, zero root,
separator mutation, Task712 transpose mutation, P1 truncation/digest mutation
and Task554 order mutation.  Their “simultaneous versus separate” check runs
the same scalar expression twice.  The only actual reseal controls are generic
hash inequalities; they never pass a coherently resealed output through
`check_output`.  The two-offset/four-slot test calls only the leaf subtraction
helper, not the blockwise traversal it claims to protect.

The YAML parses successfully as one job with 18 steps.  Its sole push marker
occurs exactly once, Task554 `failure` is required, the job cap is 90 minutes,
producer/checker caps are 40 minutes each, progress polls each second and
reports at 60-second intervals, diagnostics are unconditional, and final
publication requires both named executions to succeed.  Static inspection
finds no instruction JSON parse, rebuild, physical closure/solve, 504-row
orbit scan, SAT/nullspace search, checkpoint/resume, dense `8059 x 145152`
matrix, or Python-level 110-million-element loop.

## Resource estimate and minimal repair

The eight fixed archive sizes sum to 1,303,935,694 bytes (1.214 GiB) of
downloads.  Per executable the substantive streams are 349,055,442 instruction
bytes, 292,444,992 cache bytes and 16,377,984 physical bytes.  The active
projection performs 110,488,890 multiply-add terms inside bounded NumPy
kernels, not a Python element loop.  Its row buffer is 9,289,728 bytes; value
arrays and the 32,280-trit scalar accumulator are small.  Task554 residency is
one parsed prepare plus at most one parsed block.  Producer and checker run
sequentially under their separate 40-minute caps.

The smallest repair is:

1. In checker `check_output`, reconstruct and compare the complete expected
   terminal, result and manifest bodies, including every upper claim and the
   exact launch/separator/P1/Task712 joins; do not accept arbitrary additional
   or unchecked fields.
2. Replace every literal selftest success flag with an executed bounded
   positive/negative case.  In particular run seed-violation, actor-violation
   and full 32,280 EOF scans; exercise a two-block/four-slot accumulator
   against a direct reference; and require the checker to reject coherently
   resealed parent, relation, child, prefix, terminal-claim and result-join
   mutations.  Report a flag only after that assertion ran.

No change is needed to the fixed mathematical formulas, vectorized real-data
kernel, one-pass structure, parent roster, workflow caps, or claim meanings.

```text
VERDICT=FAIL
SAFE_TO_PUSH_TRIGGER_GHA=no
```
