# Luna reply 460 — compact direct-relator positive owner v1

Status: IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN.

The owner reconstructs the compact roster through the authenticated Task411
producer; the checker reconstructs it independently through the pinned
Task411 checker path.  The producer has no NONMEMBER terminal.  An exhausted
44-seed/action span is `UNKNOWN_INCOMPLETE:compact_direct_span_exhausted`,
with A5/A6/A7/fake/Ihara claims NONE or false.  No K quotient completeness or
full-relative-ideal claim is made.

## Authorized output pins

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_compact_direct_relator_a5_a6_positive_v1.py` | 17452 | `0a3c2473448ecade6cd4a313c21b09359756214dd36933725fbb11700e1c121c` |
| `crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v1.py` | 12062 | `3c455dbfbb914fb89498be7249c1230042d432145e3680b391c09ada7a658ab7` |
| `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v1.g` | 2454 | `ce8d6800c733d0064b89397f8d445de831b4f293f1bb444668938d70e1106363` |
| `sol/luna_reply_460_r07_compact_direct_relator_positive_owner_v1.md` | pending self-pin | pending self-pin |

Authenticated inherited Task456 pins are embedded in both Python owners:

```text
producer 2810 df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2
checker  2698 4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019
driver   1812 3ea33ee4ed8fdcf6a6f004ced6431d6c622e6d76cf8334cd8f57e72af4076ec1
```

The Task411 helper pins are:

```text
producer search/d972_r07_a0_compact_pc_invariant_owner_v1.py
        68222 be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9
checker  crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py
        44831 7c1aea086ce264ad6f51983554a3a371ac481d07a2ec5f5d9a96ee270af6dfcf
```

The reconstructed roster is required to have exactly 44 literal words and
SHA-256 `7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.

## Bounded commands and results

```text
$env:PYTHONPYCACHEPREFIX=(Join-Path $env:TEMP 'compact-positive-pyc2')
python -m py_compile search/d972_r07_compact_direct_relator_a5_a6_positive_v1.py crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v1.py
PASS

python search/d972_r07_compact_direct_relator_a5_a6_positive_v1.py --help
PASS
python crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v1.py --help
PASS

python search/d972_r07_compact_direct_relator_a5_a6_positive_v1.py --fixture
R07_COMPACT_DIRECT_RELATOR_POSITIVE_PRODUCER_FIXTURE_PASS
python crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v1.py --fixture
R07_COMPACT_DIRECT_RELATOR_POSITIVE_CHECKER_FIXTURE_PASS
```

The fixtures cover exact roster reconstruction/count/digest, one positive
ancestry and literal `M` replay, exhausted-miss mapping, old NONMEMBER
rejection, checkpoint resume/seal preservation, and rejection of relator,
marked-action, PB-ledger, literal-M, and checkpoint mutations.  The driver is
ASCII-only and pins the two new Python byte counts/hashes; its route invokes
the checker only for MEMBER and treats UNKNOWN_INCOMPLETE as nonpositive.

No Task193/A5 production closure, GHA dispatch, workflow edit, commit, push,
or production input was run.  Expected GHA envelope from the bounded owner is
one Python roster reconstruction plus the positive lane, with a 5.7 GB RSS
cap; measured Windows fixture wall times were 0.262 s (producer) and 0.283 s
(checker).  A conservative GHA estimate is under 60 s for the bounded owner
and under 5.7 GB RSS; actual production runtime/memory remains unknown because
production was explicitly out of scope.
