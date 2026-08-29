# Task 404 — GAP-safe checkpoint decoder v30

Status: versioned driver repair complete; no GHA dispatch, production
calculation, or git operation was performed.

## Diagnosis

The enormous checkpoint assignments at v29 lines 85 and 88 are valid: a tiny
GAP extraction of both `Concatenation("hex-chunk",...)` assignments evaluated
successfully.  The immediate failure was instead line 97 in `D386HexDecode`:

```gap
out:=Concatenation(out,CharInt(16*hi+lo));;
```

`CharInt(...)` returns a character, while `Concatenation` requires list
arguments.  The minimal GAP-safe repair is exactly:

```diff
- out:=Concatenation(out,CharInt(16*hi+lo));;
+ Add(out,CharInt(16*hi+lo));;
```

A tiny GAP probe reproduced the old error (`Error, Concatenation: arguments
must be lists`) and confirmed `Add` produces `AB` from two characters.  A
second probe extracted the unchanged v30 checkpoint assignments and decoder;
it returned `decoded producer=25581 checker=8991`.

## v30 pin

- `search/d972_r07_word_independent_successor_kernel_gha_driver_v30.g`
  - 76229 bytes
  - SHA-256: `bacea39ac0615e0051d5cb59356f45f7fd8b8cd6867bad7b2bc2ec286949575c`

The v30 driver retains the v16 producer, v22 checker, all mathematical/order
logic, and both embedded checkpoint payloads exactly.  Independent byte
decoding confirms the unchanged payload pins:

- producer: 25581 bytes,
  `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`
- checker: 8991 bytes,
  `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`

The driver remains ASCII-only; no other file was modified.
