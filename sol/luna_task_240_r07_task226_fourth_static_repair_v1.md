# Luna task 240 - task226 fourth static repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

Role: bounded mechanical repair only.  Do not run Python, Node, GAP, git,
GHA, or network locally.  Edit only the same five task226 files authorized by
task236.  Parent Sol owns mathematical adjudication and every execution.

## 1. Rejection boundary

The task236 return is rejected before execution.  Preserve no result merely
because producer and checker currently agree: they duplicate a wrong Fox sign
and a non-zero-safe sparse construction.  Read in full task236, v225, and
`proof_r07_actual_pointed_row_sign_cokernel_bridge_v239.md`, then repair every
section below.  Status remains `UNEXECUTED`.

## 2. Fix the literal Fox algebra

For each independently tagged block put

```text
G = fox(R_B(g0))
F = fox(R_B(f))
d_raw = d_occ = -G
B_a = F - G = F + d_raw
e = d_raw - B_a = -F.
```

The returned producer currently forms `B_a = F - d_raw = F + G`; this is
wrong.  Fix producer and checker separately.  Serialize and independently
replay all of:

```text
d_occ = d_raw
B_a = F - G
e = d_raw - B_a
e = -F
D1(d) = 1 - R_B(g0)
D1(e) = 1 - R_B(f).
```

Do not require `D1(d)=0`; v239 proves that the original target is a full-Fox-
cokernel row and generally is not a cycle at the upper shadow.

## 3. Make every sparse difference zero-safe

Never construct a difference with a Python dictionary literal containing two
possibly equal keys.  In particular,

```text
xi_o = r_o^-1 - 1
one_minus_R_g = 1 - R_B(g0)
one_minus_R_f = 1 - R_B(f)
```

must be formed by an accumulating sparse-add routine modulo three.  If the
two keys coincide, the result is the empty list.  Apply the same rule to
translated-minus-original `u0`.  Add explicit SELFTEST cases in which
`r_o=1`, `R_B(g)=1`, and translated `w_o=w_o`; producer and independent
checker must both return literal empty sparse rows rather than one overwritten
coefficient.

## 4. Authenticate the two predecessor seal dialects exactly

The actual task192 v3 receipt inherits task179's seal field `self_digest`.
Task198 uses `self_digest_sha256`.  One generic verifier which requires the
latter makes every actual task192 input fail.  Implement separately named,
independently replayed adapters:

```text
task192: remove/recompute self_digest
task198: remove/recompute self_digest_sha256.
```

Reject an object carrying only the other dialect.  Authenticate the complete
sidecars and all immutable run/head/artifact/member/checker fields without
renaming their actual schemas.

## 5. Fix the independent checker syntax and actual-input binding

The returned checker has an indentation error in `check_attestation`; it is
not parsable.  Repair it, but do not stop at syntax.

On a COMPLETE production receipt the checker must obtain

```text
actual_g0   = task192["g760"]
actual_a    = task192["exactification"]["literal"]["c_exact"]
actual_f    = task192["exact_direct_replay"]["replay"]["corrected_word"]
actual_rows = task198["bridge"]["occurrence_ledger"]
```

and require `actual_f == reduce(actual_g0 + actual_a)`.  Reconstruct the full
ABI from those four actual predecessor values and compare it literally with
the producer ABI.  Reconstructing from `receipt.result.words` alone is not an
independent predecessor binding: a malicious receipt may bind the correct
sidecar hashes while carrying self-consistent synthetic words.  Explicitly
compare the result words and ledger to the predecessor values before any ABI
comparison.  The verdict's `checker_reconstruction_sha256` must hash the
fresh independently reconstructed object, not simply hash the producer ABI a
second time.

## 6. Use genuine field-specific mutations

The current mutation harness routes most names to the same
`rword_g[0]=[]` edit and leaves the ABI seal stale.  Rejection then occurs at
the seal rather than at the claimed semantic gate.  This does not satisfy the
contract.

For every retained mutation name:

1. alter the field named by that mutation;
2. recompute all enclosing canonical seals except for the dedicated seal
   mutation;
3. preserve unrelated fields;
4. run the producer validator or independent reconstruction;
5. require the observed reason to identify the intended semantic gate; and
6. serialize the literal before/after target or a compact digest pair proving
   that the named datum actually changed.

It is acceptable to reduce the roster to a smaller one-to-one set if two old
names are exact aliases, but it is not acceptable to claim 96 distinct
controls while executing one generic edit.  At minimum retain distinct live
mutations for the two words, each block/sign/orientation/prefix family, each
Fox equality, every Q3/Q4 bracket table, actor product/inverse/conjugation,
zero-safe xi/endpoint/u0, predecessor bindings, terminal/resource handling,
and forbidden conclusions.

## 7. Strengthen the arithmetic SELFTEST

The current group check tests one associativity triple and generator inverses.
Add a bounded exhaustive oracle which is genuinely independent of the closed
coordinate routine.  At minimum exhaust all elements of the modulo-three PB3
class-two fixture for multiplication, inverse, associativity, and the three
brackets, and compare PB4 bracket/product/inverse values against direct
collection on a preregistered finite word roster covering every nonzero
bracket and both orders.  The checker builds its own oracle.  Do not label one
sample `exhaustive`.

## 8. Pin the executable cone in the driver

The returned driver checks only file existence.  Pin exact byte counts and
SHA-256 for producer, checker, and fixture and fail before startup on any
mismatch.  Input receipts and sidecars remain bound by their internal exact
attestations, and the immutable GHA head is recorded by Parent Sol.  Do not
self-pin the driver.  Keep exact-one terminal markers, strict terminal
equality, fresh outputs, and a sentinel only after checker completion.

## 9. Resource and terminal integrity

Use live counters for every registered cap or remove a cap that is not
actually measured.  In particular, do not publish an RSS cap with
`peak_rss_bytes=None` as if it had been enforced.  A real malformed-input
probe must traverse the same input authenticator used in production, and a
real resource probe must traverse the same live budget path; merely raising a
synthetic exception is insufficient.  UNKNOWN remains fail-closed and never
sets independent acceptance true.

## 10. Delivery

Process Sections 1--9 in order.  State that no execution was performed and
that A2 remains paper-only pending Parent Sol's static acceptance and GHA
SELFTEST.  End with:

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

