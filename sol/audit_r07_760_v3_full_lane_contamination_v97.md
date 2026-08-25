# R07 g760 fresh-RHS v3 full-lane contamination audit v97

Author: Sol / 2026-08-26

Status: source-level hostile audit plus GHA failure adjudication.  The v3
preflight/settled certificate remains valid at its stated scope.  The v3
full B0/B1/109-RHS lane is not accepted as fresh and produced no receipt.
No mathematical nonmembership, lift or Ihara witness is claimed.

## 1. Evidence

The source bundle was fixed at commit

```text
f3698fffd3b73370f753c4b0d9eb1e86751b1159
```

Its GHA selftest run `32875252515` succeeded.  Full run `32875451735`
used the same head and stopped after about three minutes with

```text
_d972_157ed_old_producer.Reject: unexpected geometric blocker pivot
```

at

```text
search/d972_b345_strong_wform_inertness_v1.py:370
```

No producer terminal, canonical receipt, checker run or mathematical
sentinel was emitted.

## 2. Exact contaminated call chain

The v3 source temporarily sets `old.FIXED_WORD = g760` and calls

```text
em.build_prefix_with_recovery
  -> ed.build_instrumented_prefix
  -> strong.build_fresh_prefix
```

The final function is historical old20 code.  Although its target word `r0`
is supplied by the caller and therefore uses g760, line 265 constructs the
six persistent source anchors from the module constant

```python
raw_source_tuple = tuple(
    e4.eval(word) for word in base.source_words_m0(F0))
```

where `F0` is the hard-coded 20-letter word with SHA-256

```text
b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d
```

and not `old.FIXED_WORD`.  The supposedly fresh B0 state is therefore
mixed-base before the BFS begins: g760 supplies the target, while old20
supplies persistent source anchors.

The same function contains a second old-base theorem as an assertion.  It
probes the first g760 target blocker only at checkpoint one, then at every
later geometric checkpoint merely requires that the old blocker key has
not become a basis pivot.  In run `32875451735` that key did become a pivot,
so the assertion stopped.  This proves only that the first checkpoint-one
blocker was absorbed; it does not prove that the complete target reduced to
zero, because the target was not reprobed for a possible next blocker.

Had this assertion not stopped, two further old-base gates would still have
prevented a fresh certificate:

1. `ed.build_instrumented_prefix` requires the historical exact prefix
   counts and digest schedule, rather than accepting fresh g760 ranks and
   dependencies;
2. `em.construct_fixed_B1` constructs the historical old-qstar first ACTIVE
   block and requires the frozen old20 B1 hashes, ranks, column count and
   translation.  It is not a base-independent B1 constructor.

Thus these booleans in a hypothetical v3 full receipt would not by
themselves establish their names:

```text
B0_fresh
B1_fresh
all_109_rows_fresh
```

The fail-closed stop occurred before they were serialized, so no false
positive certificate escaped.

## 3. Valid and invalid portions

The bounded preflight does not enter the contaminated call chain.  Its
producer/checker agreement still supports:

- exact reconstruction and hash of g760;
- exponent sums $(0,0)$;
- identity of $x^{108}y^{-36}$ in every settled constituent;
- equality of the 616 and 760 settled joint values;
- current E4 relations and onto certificate;
- the same-base left/right canary.

It does not support a fresh B0, B1, target6 solve, 109-row RHS, actual A.18
matrix or normalized Brunnian class.

## 4. Mandatory v4 repair

A successor must not wrap the old `strong.build_fresh_prefix` or
`construct_fixed_B1`.  It must implement these base-parametric operations.

1. Accept the exact base word and exact source tuple as explicit arguments;
   reject any access to the historical module constant `F0`.
2. At every preregistered checkpoint, freshly reduce all ordered targets.
   If the first missing pivot was absorbed, either record a complete
   coefficient ledger or replace it with the newly reduced blocker.
3. Permit fresh ranks, dependency counts and semantic digests.  Structural
   invariants are the eleven-relator complete-block rule, exact recovery,
   $D_1D_2=0$, target quotient identity and lossless coefficient replay, not
   equality with old20 counts.
4. If the base target is already in B0, emit a typed positive target6
   membership ledger and do not manufacture an old-qstar B1.
5. If it remains inconsistent, derive the current normalized dual from the
   fresh g760 affine system, correlate that dual with full $D_2$, and choose
   the canonical current ACTIVE block.  No old-qstar support or B1 digest may
   enter.
6. Rebuild all 109 word/gradient/remainder rows only after the final fresh
   basis is frozen.
7. The independent checker must reconstruct the dynamic blocker sequence,
   coefficients and terminal through a separate implementation and reject a
   forged `fresh=true` field.

The faster L3 task

```text
sol/luna_task_163_r07_760_l3_target6_v1.md
```

is independent of this repair.  It tests the g760 target against the complete
C-13 legal-correction overapproximation plus full $D_2$.  A cross-checked L3
NONMEMBER would kill this base and make the expensive dynamic v4 unnecessary;
a MEMBER result would justify implementing v4 and then the literal A.18
double build of v96.

## 5. Fixed ledger

```text
V3 PREFLIGHT/SETTLED SCOPE:        CROSS_CHECKED
V3 FULL B0/B1/109-RHS SCOPE:       REJECTED AS MIXED-BASE IMPLEMENTATION
RUN 32875451735:                   IMPLEMENTATION FAIL, NO MATH TERMINAL
OLD FIRST BLOCKER ABSORPTION:       OBSERVED
COMPLETE g760 TARGET6 MEMBERSHIP:   UNKNOWN
MANDATORY SUCCESSOR:               BASE-PARAMETRIC DYNAMIC B0/B1
```

Nothing here is Lean-verified.
