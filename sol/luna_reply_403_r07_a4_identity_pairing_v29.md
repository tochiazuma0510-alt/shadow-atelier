# Task 403 — exact legacy authority pairing v22/v29

Status: versioned correction complete; no production calculation, GHA
dispatch, or git operation was performed.

## Versioned outputs

- `crosscheck/check_d972_r07_word_independent_successor_kernel_v22.py`
  - 6579 bytes
  - SHA-256: `91ae327d9a983136cc5a1ac9188dc1ea11f9e553aef606e8bc4bf45cb9bd819a`
  - generated checker source: 268101 bytes
  - generated source SHA-256: `28cba6455e249edac835babb63b099940d91965d4e7c0f1d6a5310c57d569d18`
- `search/d972_r07_word_independent_successor_kernel_gha_driver_v29.g`
  - 76245 bytes
  - SHA-256: `5227f5e916790ad004db237c7cd3df400c3629251b79ae4bccfcb39371a5473e`

## Surgical identity repair

The v22 legacy branch now constructs a fresh copy of `authority.identity`,
removes `receipt_bytes`, and restores the exact `ci/in/` prefix on all five
`task198` paths (`checker`, `manifest`, `producer`, `receipt`, `verdict`).  A
key-set gate requires exactly those five fields.  The checkpoint identity
condition remains paired exclusively:

- current authority + runtime v22 checker SHA; or
- legacy authority with the five `ci/in/` paths + frozen v17 checker SHA.

Schema, owner, and self-seal gates are unchanged.  The v29 driver pins the
exact v22 file and updates only its checker/driver/output names and markers.
The embedded checkpoint bytes remain unchanged:

- producer checkpoint: 25581 bytes,
  `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`
- checker checkpoint: 8991 bytes,
  `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`

Static `restore_frozen()` execution reproduces the generated-source hash and
the single `receipt_bytes` field.  The GAP driver is ASCII-only.  Earlier
versions were not overwritten.
