# Task504 — A0 rank-98 checkpoint resume driver v10

Implemented only the two requested outputs.  The producer, checker, search
order, mathematics, resource bounds, workflows, A4, Task193, and v9 source
files were not edited.

## Independent permanent-release check

Downloaded from the specified permanent release URL:

```text
artifact_9821857621_gap-run-out.a0-rank98.zip
bytes=30758
sha256=d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4
members=8
```

All eight flat members independently matched the supplied byte counts and
SHA-256 values:

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

The copied resume checkpoint independently contains binding
`6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`, state
SHA `7fd45ecad90fda912df5dfdb15f2f422aa63dc8a3abfc992150079b44405685a`,
rank/count/round `98/55/59`, and 55 accepted sources.  Its first 41 accepted
sources equal the 41-source v9 input prefix exactly.  No supplied release
value was mistyped.

## Final driver pin

`search/d972_r07_a0_actual_tau_free_rank98_resume_gha_driver_v10.g`

```text
bytes=8662
sha256=8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e
```

The v10 driver is a surgical v9 successor.  It preserves producer v3
`12215/0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`,
checker v7 `3653/e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`,
producer limits `--seconds 7200 --rss-bytes 4800000000 --max-rises 64`,
7500-second producer timeout, 3600-second checker timeout, and
`ulimit -v 5200000`.  It has one producer and one independent checker,
fresh v10-owned paths/symlink gates, exact eight-member authentication,
single resume copy, fail-closed diagnostic, and the v10 external preamble and
terminal marker.

## Bounded gates

```text
exact release ZIP/member manifest and resume-state check: PASS
v9-to-v10 source diff/confinement and static pins: PASS
GAP ReadAsFunction(v10): PASS (unbound-global warnings only)
generated shell capture + bash -n: PASS (9153 bytes)
fail-closed preflight fixture: PASS
  TASK504_R07_A0_RANK98_PREFLIGHT_BEGIN
  TASK504_R07_A0_RANK98_PREFLIGHT_FAIL rc=1 cmd=false
one-producer/one-checker/resource-margin static check: PASS
```

The real producer/checker, production, GHA, workflow, search, and git were
not run.  Fixture success is not A0 progress.

TASK504_R07_A0_RANK98_RESUME_DRIVER_V10_PASS
