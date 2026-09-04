# Luna reply 773 — canonical P1 lift actual-runtime type repair v1

## Outcome

Implemented the bounded v6 runtime-type repair and workflow v3.  No real
parent artifact, production build, GHA, git, network, or delegated agent was
used.

## Diagnosis and repair

The opaque terminal is the CPython `hashlib` rejection reached by the packet
row receipt expression in the production stream.  The value entering the
conversion was a `numpy.memmap` row view (`packet[origin["origin"]]`), not an
owned bytes object.  V5 used the runtime-dependent implicit
`bytes(memmap_view)` conversion before `sha`; v6 uses the explicit, typed
`packet[...].tobytes(order="C")` materialisation.

This is semantics-neutral: the packet has frozen `uint8` dtype and shape
`(8232, SOURCE_BLOCK // 4)`, and a selected row is C-contiguous in its stored
order.  Both expressions intend the same `SOURCE_BLOCK // 4` packed bytes;
v6 merely makes the buffer boundary explicit.  No row arithmetic, DAG,
ordering, reduction, projector, or claim flag changed.

V6 additionally maintains a bounded phase label over authentication, word
load, context construction, lazy-P1 opening, each old/new row, terminal, and
final receipts.  Every ordinary rejected exception now carries both the
phase and an 8192-character traceback tail.  Fail-closed exit code 1 is
unchanged, so a future failure cannot collapse to the former one-line opaque
terminal.

## Receipts

- `search/d972_r07_canonical_p1_dag_degree2_lift_v6.py`
  - bytes: 105983
  - sha256: `e83f6fca9643905b935b73b8dcaea51effbe08f6a9549523478227d3ec85bc62`
  - LF/CR/NUL: 2257/0/0
  - final byte: 10 (LF)
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v3.yml`
  - bytes: 27574
  - sha256: `ac5d47c2e8b709af96b2ebc3e9fef60d4844f3014efef26806b69c06b14c40c1`
  - LF/CR/NUL: 497/0/0
  - final byte: 10 (LF)

The workflow invokes only v6, authenticates its exact path/bytes/LF/SHA,
uses launch schema v5 and executable key `producer_v6`, and expects candidate
manifest schema v5.  Success/log artifact names are versioned task773/v3.
The inherited exact five-parent authentication, serial producer, 7-GiB RSS
gate, 38-minute gate, progress/checkpoint logging, and always-uploaded logs
remain unchanged.

## Bounded checks

1. `python -B -m py_compile ...v6.py` — PASS (external temporary pycache on
   the final run).
2. `python -B ...v6.py --selftest` — PASS; `fixture_accept=6`,
   `rejections=50`, `actual_replay=DEFERRED_TO_GHA`.
3. Deliberately incomplete `--build` invocation — expected exit 1 and a
   bounded JSON terminal containing `phase=startup`, `traceback_tail`, and
   `verified=false`.
4. Python AST parse — PASS.  Static gates locate the explicit C-order
   `.tobytes`, phase field, and traceback tail.
5. PyYAML parse — PASS; one job and 17 steps.
6. Static search finds no `PRODUCER_V5`, `producer_v5`, v5 producer path,
   launch-v4, or candidate-v4 reference in v6/workflow v3.

The only newly materialised data on the production path is the same single
packed packet-row byte string that v5 already attempted to materialise with
`bytes(...)`; there is no additional full-file pass, matrix copy, dense owner,
duplicate parse, or heavy SELFTEST.

All mathematical and downstream claim flags remain false; this is an
implementation candidate, not a mathematical or Lean verification claim.

READY_FOR_SOL_AUDIT=yes
