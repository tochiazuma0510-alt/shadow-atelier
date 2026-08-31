# Task436 actual-b72 first-ACTIVE final dispatch audit v2

Author: Sol / 2026-08-31

## Verdict

**GO for the first positive-first GHA dispatch.**  On the final pinned
snapshot, I found no path which can promote an incomplete selector, a raw
exponent row, or an unchecked literal to `ACTIVE_COLUMN_READY` or
`CURRENT_DUAL_CORRECTION_EMPTY`.  The acknowledged terminal-only checkpoint
means a capped run must restart; that is an operational limitation, not a
false mathematical promotion path.

No production, download, GAP run, git operation, GHA dispatch, or checkpoint
load was performed.

## Frozen files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_first_active_v1.py` | 24,643 | `5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc` |
| `crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py` | 13,834 | `3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916` |
| `search/d972_r07_a0_actual_b72_first_active_gha_driver_v1.g` | 2,349 | `0be621eb16a11a0d17c02a18be4a428010ccaa7d86b365c1b0eb1c678f8759ce` |
| `sol/luna_reply_436_r07_a0_actual_b72_first_active_v1.md` | 4,354 | `b9d21d0fc29f487d1f00ee82e154c7d18cb3e8ff751c9973ccad468a36e4ae9e` |

The driver's producer/checker pins at line 11 equal the first two rows, and
the Luna reply agrees with all three executable pins.

## Dispatch gates

### 1. Selective S0--S2 construction and resource boundary

The former packed-value type error is closed: membership now compares
`family_key(section_row(...),(i,))`, rather than passing an already packed
40-byte value back through `tuple_key` (producer lines 128--138).  The local
Q0 construction retains exactly three 40-byte stores, checks the exact
1,469,664-state shape, and enforces the 176,359,680-byte store total
(lines 99--119 and 167).  S0, S1, and S2 independently rebuild their A, L,
and order-9 kernel data.  Budget checks cover Q0, membership, coarse-index,
formula, target, and fibre loops; progress logging is sparse.

There is no call to task179 `build_runtime`, task175 `run_preflight`, a
6,441-row roster, occurrence/boundary closure, or a global Delta scan.  No
physical row is copied into source metadata (producer line 49; checker line
46), no deep copy of the prefix is made, and the final rank gate uses
`phys.reduce`.

### 2. Quotient adjoint, Tietze adjoint, and 44 formulae

Every one of the 72 raw new-`b` points is checked directly through
`q.contract` (producer line 176; checker line 30).  The complete localized
PB3 reverse neighbourhood is formed in new coordinates: components 0, 1,
and 2 at `r*z^j`, plus the two noncentral predecessors.  Its merged pairing
is checked against the component-0 adjoint and zero on the other components
(producer lines 181--190; checker lines 33--41).  No invalid PB3 old
component 4--6 reaches `q.transform`.

The old adjoint uses `b@h += mu` and `a@(h*x^-1) -= mu`; every retained old
key is checked by a direct singleton transform.  All 44 formulae require
`K=0`, coordinates in `{0,1,2}`, and equality of formula, raw-direct, and
physical-dual scalars (producer lines 203--216; checker lines 65--71).

### 3. ACTIVE literal and normalized-v12 replay

The producer's selected fibre candidate is replayed by the inherited literal
kernel-candidate gate in all ten coordinates.  It then requires:

- v12 `replay_atom(seed, delta_word)` equals fresh
  `seed_v12(delta * relator * delta^-1)`;
- integer `v12.v3.exp_pair`, divisibility by 18, exact `N1/N2`, and no raw
  `E` key;
- equality with the fresh eleven-occurrence quotient row;
- nonzero formula/physical-dual scalar; and
- a nonzero physical remainder with the emitted pivot/rank transition.

These are the producer gates at lines 219--241.  The checker independently
binds the claimed formula and target, evaluates the **delta prefix** (not the
conjugate) in all ten coordinates, recomputes its scalar, replays the full
v12 normalized-`N` conjugate and eleven occurrences, and checks the row
digest, exact new pivot, and `[43,44]` transition (checker lines 74--85).

### 4. UNKNOWN/EMPTY and checker independence

The producer downgrades complete-but-unchecked exhaustion to
`UNKNOWN_RESOURCE:empty_requires_independent_exhaustion` (producer lines
243 and 257--258).  The checker accepts only top-level
`ACTIVE_COLUMN_READY` or `UNKNOWN_RESOURCE`; it rejects EMPTY outright,
requires a nonempty UNKNOWN phase, and performs the full prefix, adjoint, and
44-formula replay before either accepted terminal (checker lines 86--94).
Thus neither a cap nor an unowned empty scan can become a separator claim.
All A0/COMMON/NONMEMBER/fake/Ihara claim flags must remain false.

### 5. Driver

The driver requires the external preamble, pins the exact producer/checker
bytes, refuses pre-existing artifact/checkpoint paths, passes 2,400 seconds
and 4.8 GB, requires both artifact and producer marker, then requires the
checker PASS marker before its unique driver PASS marker (driver lines
11--22).  A producer exception or forged ACTIVE/EMPTY artifact therefore
cannot reach driver PASS without checker acceptance.

## Nonblocking checkpoint limitation

There is no mid-run checkpoint reader or resume cursor: the checkpoint is a
terminal compact summary written after the selector returns.  If Q0/fibre
construction reaches a cap, the artifact is `UNKNOWN_RESOURCE` and the next
run rebuilds from the authenticated prefix.  This loses work but cannot
create ACTIVE, EMPTY, MEMBER, or NONMEMBER.  It is not a blocker for this
first positive-first dispatch; any continuation intended to accumulate work
across the 2,400-second cap needs a separate resume repair.

## Bounded commands run

- external-`PYTHONPYCACHEPREFIX` `python -B -m py_compile` on producer and
  checker: PASS;
- producer `--mode FIXTURE` with output under `%TEMP%`: PASS;
- checker `--self-test`: PASS, ten declared mutation rejections.

GO
