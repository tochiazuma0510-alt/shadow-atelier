# Luna Reply 842 — P1 reached nonpromotion repair v9

## Result

Implemented only the sole Task838 blocker in the three authorized new files.
No mathematical row loop, row order, schema, immutable input, cross-runner
pin, prior fixture, resource cadence, or time/memory envelope was changed.
No GHA, git, or production run was used.

## Exact repair

Producer-v10 adds `_promotion_boundary`, and the production build calls this
same helper from both relevant terminals:

- `except (ResourceStop, KeyboardInterrupt)` supplies the actual terminal,
  cache/instruction streams, and last checkpoint.  The helper rolls back the
  two streams and immediately re-raises that same terminal.  This branch
  reaches no checkpoint unlink, manifest write, or output replacement.
- the successful production tail supplies the completed manifest.  The
  helper performs exactly the former checkpoint unlink, canonical manifest
  write, and atomic `os.replace(staging, out)` promotion.

The added bounded fixture uses an actual fresh requested output path.  It
publishes a cursor-4 checkpoint, writes two orphan rows, enters the same
helper with an actual `ResourceStop`, and proves all four commissioned facts:
the helper was reached, the identical terminal object propagated, the prefix
re-authenticates at cursor 4 after rollback, and the requested output was not
created.  Its second branch calls the same helper on a tiny success staging
tree and checks checkpoint removal, canonical manifest writing, payload
retention, staging removal, and creation of the actual promoted output.

## Identities and diff

| file | SHA-256 | bytes | LF |
|---|---|---:|---:|
| producer-v9 baseline | `c05149e41e62b4aa78b483c61fb03570228ba7697d95d3cd10848758b8735ed9` | 149350 | 3164 |
| `search/d972_r07_canonical_p1_dag_degree2_lift_v10.py` | `af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f` | 154825 | 3273 |
| workflow-v8 baseline | `fff09e419fbc625a6faf9510a98b0e0be0e4a5bb5b9b8ff29a0817f1a5b0df46` | 34261 | 629 |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v9.yml` | `a1465601d3843e199741d0130c99003d7c90c74fc0ca60fe39e1dca2417a888d` | 34262 | 629 |

The producer no-index diff is 125 insertions / 16 deletions.  Every source
change is the factored boundary, its two call sites, the reached fixture, and
selftest reporting.  The workflow diff is 9 insertions / 9 deletions: fixed
producer path/SHA/bytes/LF, workflow/artifact labels, and fire token
`[fire-r07-canonical-p1-degree2-lift-v9]`.  Candidate/checkpoint schemas stay
v8 as commissioned.

## Bounded checks

| check | result |
|---|---|
| external-pycache `py_compile` producer-v10 | PASS, 0.316 s |
| serial producer-v10 `--selftest` | PASS, 1.809 s, exit 0 |
| reached resource/nonpromotion fixture | PASS, accepts 1 |
| reached success-promotion fixture | PASS, accepts 1 |
| prior resume fixture | PASS, accepts 12 / rejects 12 |
| prior cross-runner fixture | PASS, accepts 3 / rejects 1 |
| YAML BaseLoader | PASS, one job / 22 steps |
| all extracted `run:` scalars under Git Bash `bash -n` | PASS, 10/10 |
| `git diff --check` on the two implementation files | PASS |

Selftest terminal fields include
`promotion_fixture_accept=2`, `promotion_fixture_rejections=0`,
`selftest=PASS`, `actual_replay=DEFERRED_TO_GHA`, and `verified=false`.
All A0, COMMON, cofinal, fake and Ihara claims remain false.

IMPLEMENTED_AUDIT_REQUIRED
