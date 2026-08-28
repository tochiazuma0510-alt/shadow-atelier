# R07 actual-owner first-rejection trace theorem (v297)

## 0. Scope

This note fixes the mutation-evidence semantics shared by the active A0 and
A4 SELFTEST implementations.  It is a finite software-proof contract, not an
execution result.  It neither accepts either implementation nor changes an
A0/A4 numerator, and it proves no lift, fake, or Ihara statement.

The contract excludes four recurring false certificates:

- copying `reached_validator` from a fixture;
- recording the SHA-256 of empty bytes when a path mutation was attempted;
- throwing an artificial "accepted" exception and catching it as though an
  ordinary validator rejected; and
- rerunning an unchanged expensive baseline for every envelope mutation.

## 1. Ordinary pipeline and events

Fix one side, producer or checker.  Its ordinary pipeline is a composition

```text
Open -> Decode -> Seal -> Type -> Authority -> Algebra -> Terminal.
```

Not every case reaches every stage.  Each ordinary validator has a stable
versioned identifier and emits an internal entry event

```text
(ordinal, validator, stage, owner_identity)
```

before reading the load-bearing owner for that stage.  This event mechanism
is part of the ordinary pipeline and contains no mutation name, expected
reason, or SELFTEST acceptance flag.

An ordinary rejection has the typed value

```text
(validator, stage, narrow_reason).
```

The first rejection is the first such value in the actual event order.  A
`KeyError`, assertion accident, missing field access, process crash, timeout
outside the typed resource owner, or arbitrary exception is not a narrow
rejection.

## 2. Physical owner identity

For regular-file bytes use

```text
I_file = (resolved registered path, byte length, SHA-256,
          opened-handle device/file-id, link count, type).
```

For a path object which is intentionally nonregular or rejected before its
contents can be read, use

```text
I_path = (lexical path, lstat/reparse type, link/reparse target if readable,
          device/file-id and link count where available).
```

Thus a symlink, hardlink, missing path, traversal path, or replaced pathname
has a real before/after *path identity*.  `SHA256(b"")` is not a substitute.
TOCTOU evidence additionally records the opened-handle identity before and
after the hook and the pathname identity after the hook.

For a genuinely ephemeral algebraic owner, use its canonical typed encoding
and digest.  This case is legal only when the ordinary validator consumes
that same live owner.  Serializing a detached dictionary and validating some
other live object does not establish a mutation.

## 3. One mutation experiment

For a registered case `m`, perform the following construction.

1. Open or construct the unmutated ordinary owner and run the ordinary
   pipeline to its registered successful baseline terminal.
2. Record the actual identity `I_before` of the narrow owner.
3. In a fresh bounded owned temporary location, copy the authenticated bytes
   or canonical ordinary envelope and change exactly the registered owner.
   Reseal only derived envelopes which are downstream of that owner and are
   needed to reach the intended validator.
4. Record the resulting actual identity `I_after` and require
   `I_after != I_before` under the registered identity type.
5. Clear the event trace and invoke the same ordinary entry point.  Catch
   only its narrow registered rejection type.
6. Take `(validator,stage,reason)` from that caught value and the emitted
   events.  Require it to equal the fixture row exactly.
7. If the ordinary call returns, throw `MUTATION_ACCEPTED` *outside* the
   narrow-rejection catch.  This hard SELFTEST failure can never satisfy the
   expected row.
8. Dispose of the fresh physical owner.  For an in-place ephemeral owner,
   restore `I_before` in `finally` and rerun its baseline validator.

The resulting evidence row is

```text
{
  id, owner, identity_kind,
  before_identity, after_identity,
  event_trace_digest,
  entered_validators,
  first_rejection: {validator, stage, narrow_reason},
  baseline_revalidated,
  terminal_count
}.
```

Every field except the expected comparison row is measured or derived from
the actual experiment.  In particular `entered_validators` and
`first_rejection` are never copied from the fixture.

## 4. Resealing rule

Let the canonical envelope dependencies form a directed acyclic graph.  If
the mutated owner is `x`, a reseal may change only seal nodes reachable from
`x`.  It may not rewrite an independent authority identity, the expected
reason registry, or the field which the intended validator is meant to
recompute.  The evidence records the set of resealed nodes.

This distinguishes two legitimate tests:

- an unresealed byte change whose first ordinary rejection is a physical
  digest or self-seal failure; and
- a locally resealed semantic change which passes transport and reaches a
  later algebraic validator.

If resealing causes a different earlier field to become inconsistent, that
earlier rejection is the truthful result; the test is not relabelled as the
desired later reason.

## 5. Independence

Producer and checker have separate fixture maps, constructors, event traces,
ordinary validators and evidence ledgers.  They may share the immutable list
of mutation names and frozen primitive group meanings.  The checker does not
accept producer values for `I_before`, `I_after`, entered validators, first
reason, or terminal count.

The final checker may compare the two ledgers for coverage, but equality is
not required: independently written pipelines may reject the same owner at
different narrow validators, and those different expected rows must be
preregistered explicitly.

## 6. Expensive immutable context

Suppose an ordinary stage computes an immutable expected value `E` from
authenticated inputs, and the registered mutations alter only later
candidate envelopes.  Compute `E` once per side, bind its complete canonical
identity, and let the ordinary envelope validator compare every candidate to
that immutable `E`.

### Lemma 6.1 (baseline factoring)

This factoring preserves the accepted/rejected set and first rejection if:

1. the computation of `E` is deterministic and passes once before any
   mutation;
2. no registered mutation changes an input on which `E` depends;
3. the ordinary candidate validator consumes the same bound `E`; and
4. every producer/checker side derives its own `E`.

**Proof.**  Under (1)--(2), recomputing `E` for each candidate yields the same
canonical value.  Replacing those identical computations by the bound value
therefore leaves every comparison and its order unchanged.  Conditions
(3)--(4) preserve the ordinary route and independence.  QED.

Consequently an A0 boundary baseline may run the required W2/W4 and fault
matrix once per side, then use its independently bound result in the 13
ordinary envelope mutations.  Spawning a fresh worker pool and repeating the
same full epoch thirteen times is unnecessary work, not stronger evidence.
The same rule applies to immutable K0 table digests after v296's one-pass
construction.

## 7. The first-rejection theorem

### Theorem 7.1

Assume Sections 1--6 and a complete finite fixture registry.  If all mutation
experiments succeed, then for every registered row:

1. a real load-bearing owner changed;
2. the ordinary pipeline reached exactly the recorded prefix;
3. its first typed rejection is the preregistered narrow result; and
4. neither mutation-name control flow nor an artificial exception can supply
   that result.

**Proof.**  Physical or canonical identity inequality proves (1).  The
ordinary entry events prove (2).  The narrow catch and event order give (3).
The expected registry is read only after the ordinary call chooses its
result, while `MUTATION_ACCEPTED` is outside the catch, proving (4).  QED.

This is a trace theorem, not proof that the underlying ordinary mathematics
is sound.  That remains a separate Sol(max) code audit and GHA comparison.

## 8. Mandatory audit checks

Reject a candidate if any row has an empty/dummy after identity, a fixture-
copied `reached_validator`, an expected-reason branch, a broad exception
catch, an artificial accepted exception caught as ordinary rejection, an
unrestored live owner, a detached transcript, a mutation-only validator, or
an avoidable repeat of immutable heavy work.  Also reject if the exact key
set of producer or checker rows differs from its preregistered roster.

```text
ACTUAL-OWNER TRACE SEMANTICS:       PAPER PROOF
FIRST-REJECTION EXTRACTION:         PAPER PROOF
IMMUTABLE BASELINE FACTORING:       PAPER PROOF
A0/A4 IMPLEMENTATION:               PENDING
SELFTEST / PRODUCTION:              UNEXECUTED
LIFT / FAKE / IHARA:                NONE
```

`R07_ACTUAL_OWNER_FIRST_REJECTION_TRACE_V297_PAPER_GRADE`
