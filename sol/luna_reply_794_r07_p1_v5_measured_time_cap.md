# Luna Task794: canonical P1 v5 measured time-cap receipt

## Verdict

`READY_FOR_ROOT_RELEASE_REVIEW=yes`

The v5 workflow is a mechanical v4 successor with only the commissioned
measured resource/name changes.  It is a release candidate for root review;
it was not dispatched.  No production run, GHA operation, network access, or
git mutation was performed.  Root remains the sole git/GHA broker.

## Authority identities

The exact resource result and v4 workflow were read in full:

| file | bytes | LF | CR | SHA-256 |
|---|---:|---:|---:|---|
| `sol/sol_reply_792_root_r07_p1_v4_resource_result.md` | 3507 | 84 | 0 | `38baef05570a0dfa8f4abbaa665eb45b4a19d39d1a96f09b9452cc0f4faa41b7` |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v4.yml` | 27574 | 497 | 0 | `5405fd5a83844ff95e3b79239e1f158ab653b237d2f8bfb6fd20eba73497f1cb` |

The task names `sol/sol_reply_784_audit_r07_canonical_p1_v7_v4.md`, but that
path is absent.  The repository's matching Task784 audit is
`sol/sol_reply_784_audit_r07_canonical_p1_lift_v7_input_size_repair.md`; it
was read in full as the available authority (12115 bytes, 243 LF, CR=0,
SHA-256 `1d6d7b875fd1ca8d4ea40be9750ee8ccf93bda506516324025254bef5569cee5`).
No file was created or edited to repair this input-path discrepancy.

## v5 YAML receipt

| file | bytes | LF | CR | NUL | final byte | SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v5.yml` | 27574 | 497 | 0 | 0 | `10` (LF) | `5ef35e08febb9cbf29c6611c1570fefec8c6181c32c6d67b4bffb4b23e017aff` |

The v4 and v5 byte counts and LF counts are identical; only the eight
listed semantic/name lines below differ.  The reply is the receipt itself,
so its own self-referential SHA is intentionally not included.

## Exact normalized diff

The bounded comparison normalized exactly these v4/v5 pairs and no others:

| line | v4 | v5 |
|---:|---|---|
| 1 | `name: d972-r07-canonical-p1-dag-degree2-lift-v4` | `name: d972-r07-canonical-p1-dag-degree2-lift-v5` |
| 98 | `D972_LIFT_SECONDS: "2220"` | `D972_LIFT_SECONDS: "3540"` |
| 103 | fire tag `[fire-r07-canonical-p1-degree2-lift-v4]` | fire tag `[fire-r07-canonical-p1-degree2-lift-v5]` |
| 105 | `timeout-minutes: 45` | `timeout-minutes: 75` |
| 318 | `Construct canonical v4 launch manifest` | `Construct canonical v5 launch manifest` |
| 406 | GNU `timeout ... 38m` | GNU `timeout ... 60m` |
| 483 | `task781-canonical-p1-degree2-lift-v4-${{ github.run_id }}-${{ github.run_attempt }}` | `task794-canonical-p1-degree2-lift-v5-${{ github.run_id }}-${{ github.run_attempt }}` |
| 493 | `task781-canonical-p1-degree2-lift-v4-logs-${{ github.run_id }}-${{ github.run_attempt }}` | `task794-canonical-p1-degree2-lift-v5-logs-${{ github.run_id }}-${{ github.run_attempt }}` |

After normalizing those exact fields, the v4 and v5 texts compare equal:

```text
normalized_equal=true
raw_changed_lines=8
unexpected_normalized_diff=none
```

The v5 retains launch schema
`d972.r07.canonical-p1-dag-degree2-lift.launch.v6` and candidate schema
`d972.r07.canonical-p1-dag-degree2-lift.v6`.  Producer, checker, source,
commands, selftest, validation, artifact content, arithmetic, inputs and all
accepted hash/byte/LF/action/parent pins are unchanged.  The exact event-SHA
checkout, read-only permissions, Python/NumPy versions, serial BLAS
variables, RSS/virtual-memory limits, success-only candidate upload and
always-run log upload are likewise unchanged.

The push guard remains manual dispatch or the v5 fire tag; a push without
`[fire-r07-canonical-p1-degree2-lift-v5]` cannot enter production.  The
external recurrence cap is now 60 minutes, the workflow job cap is 75
minutes, and the measured environment value is 3540 seconds.  No checkpoint,
resume, parallelism, profiling, extra replay, SELFTEST, or other repair was
added.

## Bounded check boundary

The only local check was an in-memory v4/v5 exact-text comparison after the
eight substitutions above, plus byte/LF/CR/NUL/final-LF and SHA-256 receipt
checks.  No YAML package was installed and the workflow was not executed.

This release candidate makes no claim of a canonical P1 lift, A0, COMMON,
cofinality, compatible lift, fake, Ihara result, or Lean verification.

`verified=false`

READY_FOR_ROOT_RELEASE_REVIEW=yes
