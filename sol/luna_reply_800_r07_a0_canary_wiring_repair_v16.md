# Task800 — A0 reached-seed canary wiring repair v16

Status: `READY_FOR_HOSTILE_REAUDIT`

## Scope

Processed all numbered sections of `sol/luna_task_800_r07_a0_canary_wiring_repair_v16.md` and the four named inputs. Only the two requested versioned successors and this reply were created. Producer v9 was not edited.

## Checker v8

Created `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` as the v7 successor.

- The reached production call now passes the reconstructed five-key `base_receipt` as the final argument to `validate_direct_canary`; it no longer passes the twelve-key `direct_canary` object.
- Added exactly one bounded positive wiring regression. It constructs a distinct five-key `positive_base` and twelve-key `positive_full`, invokes the complete `validate_direct_canary` path, and requires acceptance.
- Existing v7 mutation and completion-rejection coverage was retained; no arithmetic, owner/source universe, schedule, target, cap, generic-call count, aggregation, or claim flag was changed.
- Checker marker/schema are v8; verdict remains `verified=false` and `cross_checked=false`.

The source diff is limited to the v8 marker, the one production call argument, the positive fixture and its selftest receipt field, and the versioned verdict schema. AST comparison found no added or removed top-level definitions/classes. Changed function bodies are exactly `fixture_rejects`, `validate_payload`, `selftest`, and `main`. The `validate_direct_canary` call graph changes from one v7 production call with final argument `direct_canary` to two v8 calls: the bounded fixture with `positive_base`, and production with `base_receipt`.

## Workflow v16

Created `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml` by copying v15. The exact changed surface is: workflow name/path, checker marker, v16 fire token, checker v8 path/byte count/SHA, the authentication step's versioned label, and the two v16 artifact/log names. Producer v9 pins/SHA, all parent/source pins, limits, and the single serial job are unchanged. No GHA or production run was started.

## Bounded checks

Ran only:

```text
python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py
python -B search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py --selftest
python -B search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py --selftest
```

All three checks passed. The producer selftest reports `fixture=PASS`; the checker selftest reports `fixture=PASS`, `positive_direct_canary=1`, `base_canary_direct_calls=2`, `base_canary_completion=2`, and `mutation_count=55`.

## Byte receipts

All files are LF-only, CR count zero, and have no UTF-8 BOM.

| file | bytes | LF | CR | BOM | SHA-256 |
|---|---:|---:|---:|---|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` (unchanged producer) | 70,945 | 1,272 | 0 | false | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` | 111,387 | 1,925 | 0 | false | `1e8e82191bb8d82189a194010228ed180ebc0607732a6bb338ab13abf16d86fc` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml` | 13,249 | 198 | 0 | false | `996854c74cefbfc873bfa09ed74881c4163bebf32bc5880310f069748831e2f5` |

This reply is 3,732 bytes, 50 LF, 0 CR, and has no BOM. Its detached self-receipt is the SHA-256 of all reply bytes with the final receipt line removed.

No fresh rho2, A0, COMMON, compatible-lift, fake, or Ihara claim is made. `verified=false`.

reply_sha256_excluding_this_receipt_line: fca7c81fcb392ddba6d985a99e2939599cf1f78216f5ac997a46a971d71d1cf4
