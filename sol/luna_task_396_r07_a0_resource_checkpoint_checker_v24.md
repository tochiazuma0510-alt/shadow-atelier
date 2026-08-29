# Luna task 396: A0 resource-checkpoint checker v24

Role: **Luna implementation reinforcement**.  Repair one observed transport
bug from GHA run `33259268996`.  Do not alter the A0 search, producer,
candidate order, budgets, checkpoint body, resume semantics, or terminal
meaning.

## 1. Observed failure and frozen inputs

Run `33259268996` reached the producer terminal

```text
UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:...
```

but the checker stopped at `resource Q0-LATE phase boundary`.  In the
generated checker the false branch is literally

```python
not heavy_complete and checkpoint.get("heavy_reconstructible") is bool
```

which compares a value with the `bool` class object.  The intended physical
type check is `type(checkpoint.get("heavy_reconstructible")) is bool`.

Freeze exactly:

```text
search/d972_r07_history_free_positive_fast_resume_v23.py
  3729 bytes
  0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3
crosscheck/check_d972_r07_history_free_positive_fast_resume_v23.py
  2066 bytes
  b0e6f447c92cf76f7735c56ce7dc71b2fa7c3a2247abab3962d50ba9e9bb926c
search/d972_r07_history_free_positive_fast_resume_gha_driver_v23.g
  8275 bytes
  3c469e03244bd4d286c8e0fb2d12544f21ef1a7c2cb1c0cf2c97574a55670313
```

Fail closed on any pin drift.

## 2. Only authorized semantic change

Generate a v24 checker from the frozen v23 checker and replace exactly the
single bad predicate above by

```python
not heavy_complete and type(checkpoint.get("heavy_reconstructible")) is bool
```

No other generated checker statement may change except the necessary
version/pin identity text.  Keep the producer physically at v23; there is no
v24 producer because the production search is unchanged.

Generate a v24 driver from the frozen v23 driver which:

1. pins and invokes the unchanged v23 producer and the new v24 checker;
2. advances only driver/checker owner labels and fresh output paths to v24;
3. retains the optional exact resume triple, 10,800-second internal cap,
   11,100-second external producer timeout, 7,500-second checker timeout,
   typed terminal grammar, terminal equality and checkpoint requirement;
4. exits successfully after the independently checked `UNKNOWN_RESOURCE`
   terminal so the existing workflow artifact-upload step runs; and
5. changes no workflow file and adds no extra preflight, SELFTEST, mutation
   campaign, search, or heavy processing.

## 3. Exact outputs

Create only:

```text
crosscheck/check_d972_r07_history_free_positive_fast_resume_v24.py
search/d972_r07_history_free_positive_fast_resume_gha_driver_v24.g
sol/luna_reply_396_r07_a0_resource_checkpoint_checker_v24.md
```

Perform bounded definition-load/generated-source compilation, an AST/text
comparison proving the one predicate repair, GAP `ReadAsFunction` parse-only,
ASCII and physical bytes/SHA checks, and `git diff --check`.  Do not run A0,
GHA, SELFTEST, git, network, or any large fixture.

`TASK396_R07_A0_RESOURCE_CHECKPOINT_CHECKER_V24_COMMISSIONED`
