# Task505 independent audit — A0 rank-98 resume driver v10

## Verdict

`GO_FOR_GHA_DISPATCH`.

The frozen v10 driver is a bounded, surgical continuation of the independently checked v9 output checkpoint at rank/count/round `98/55/59`.  No production, producer, checker, GHA, or git operation was run.  This dispatch verdict is not A0 progress; A0 remains `0/1 actual`.

## Frozen pins and permanent release

All three preflight pins matched:

| subject | bytes | SHA-256 |
|---|---:|---|
| v10 driver | 8662 | `8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e` |
| Task504 reply | 3410 | `89271e329e104a3a5269103674e8f2b25e9870c3ad180bc3f7b9ff59a3787640` |
| freshly downloaded permanent ZIP | 30758 | `d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4` |

I read the ZIP directly and independently recomputed its manifest.  It contains exactly eight unique, flat names, with no omitted or extra entry:

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank84_resume_v9_input.checkpoint` | 52707 | `eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f` |
| `d972_r07_a0_actual_tau_free_rank84_resume_v9_preflight.log` | 35 | `4d3dd0892debc756d57c12ab585ff63d473aad334bf25339c3fe3af6cef79139` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v9.json` | 70365 | `2bbe05d8c5c2b97177854e7cd77944e9b89af70cea7f50e7565a6faec3a70b1d` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v9_checker.log` | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v9_output.checkpoint` | 69947 | `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v9_producer.log` | 4989 | `d585eec9c9b2f81a5689749ddc9fbe9d9e5e658651907ae95baf41d8827082fa` |
| `driver.g` | 126 | `ee8f36e711d719244b40b283f8d9debcdfd553b4ca0bee8dedcade6cd6ac8081` |
| `run.log` | 5087 | `d2c1cc146af7b1af3eddfbd213b29ee2b75e8b8030a77dcff2747dbb9ff2dc7c` |

The driver selects and copies the 69,947-byte v9 **output** checkpoint, not the 52,707-byte v9 input.  Independent JSON parsing and canonical SHA-256 recomputation gave:

- binding `6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`;
- state SHA `7fd45ecad90fda912df5dfdb15f2f422aa63dc8a3abfc992150079b44405685a`;
- rank/count/round `98/55/59` and exactly 55 accepted sources;
- exact equality between the first 41 sources and all 41 sources of the archived old input checkpoint.

## Driver envelope

Before computation, the driver guards the immutable run/job/head/API metadata, permanent URL, ZIP bytes/hash, exact eight-entry manifest, every extracted member, and the copied resume bytes/hash.  The actual producer and checker matched their retained pins:

| executable | bytes | SHA-256 |
|---|---:|---|
| producer v3 | 12215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| checker v7 | 3653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |

The generated shell has ten owned/source `test ! -L` gates in addition to fresh `! -e` checks, a fresh extraction directory, and exactly one resume `cp`.  A tiny audit-local run with the producer deliberately absent exited `1` before download or computation and left the owned diagnostic:

```text
TASK504_R07_A0_RANK98_PREFLIGHT_BEGIN
TASK504_R07_A0_RANK98_PREFLIGHT_FAIL rc=1 cmd=test -f "search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py"
```

Static counts over the exact generated shell found exactly two Python calls: one producer followed by one checker.  The producer has exactly one each of `timeout ... 7500s`, `--seconds 7200`, `--rss-bytes 4800000000`, and `--max-rises 64`; the checker has exactly one `3600s` timeout; and `ulimit -v 5200000` occurs exactly once.  Thus the wall margin is 300 seconds and the VM ceiling is `5,324,800,000 > 4,800,000,000` bytes.  There is no retry, worker pool, SELFTEST/fixture path, old-prefix search, or second large-state copy.

## Terminal and transport typing

The shell uses `set -euo pipefail`, requires nonempty result and checkpoint, exactly one typed producer terminal, and exactly the one-line v7 checker PASS.  A nonzero producer, timeout, `tee`, or checker exit therefore stops the shell; stale owned paths stop before it.  Checker output containing ERROR or Traceback cannot equal the required one-line PASS.  An uncaught producer ERROR/Traceback is a nonzero pipeline failure, while the frozen producer converts an ordinary caught exception to plain `UNKNOWN`; plain `UNKNOWN` is outside the checker's exact `{UNKNOWN_RESOURCE, COMMON_CANDIDATE}` status set and cannot reach driver PASS.

The corrected Task505 distinction is satisfied: checker-approved `UNKNOWN_RESOURCE` is an intentional transport success, not an A0 promotion.  The permanent v9 witness has status/terminal `UNKNOWN_RESOURCE`, and its exact claims are

```json
{"A0":false,"COMMON":false,"Ihara":false,"NONMEMBER":false,"fake":false}
```

The pinned checker requires precisely those false claims for `UNKNOWN_RESOURCE`, verifies the allowed typed reason, closed durable checkpoint, replayed state, and current profile, and only then emits its one-line PASS.  Hence such a terminal may reach `upload-artifact` while making no mathematical claim.  A `COMMON_CANDIDATE` follows the separate positive replay boundary.

## Diff and syntax confinement

After normalizing the v10/v9 variable and task labels, the entire generated command-builder block matched v9 byte-for-byte except the authenticated archive-member count changing from seven to eight.  The remaining bounded source differences are the new permanent source binding/manifest, v10-owned paths, preamble, comments, and markers.  Producer/checker pins, call order, search mathematics, checkpoint replay, resource limits, and claim meanings are unchanged.  Mathematics changes: none.

GAP `ReadAsFunction` passed with only unbound-global warnings.  Independently captured generated shell was `9153` bytes with SHA-256 `633896e05c53c6ce0407c1d8db4968656292e12539486b773f7449cc305ce7a0`; `bash -n` passed.

TASK505_R07_A0_RANK98_RESUME_DRIVER_V10_AUDIT_GO
