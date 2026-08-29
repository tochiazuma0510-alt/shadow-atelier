# R07 history-free A0 to task193 exact adapter

Date: 2026-08-29  
Status: paper theorem; implementation target for the production-only adapter.  
Scope: the actual `COMMON_WORD` branch of the history-free A0 solver.  This
note proves an input bridge only.  It claims neither A5 membership nor a
compatible lift, fake, or Ihara witness.

## 1. Accepted input

Let `R0` be a sealed receipt with

```text
schema   = d972-r07-history-free-positive-fast-resume/v10
status   = COMMON_WORD
terminal = R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD
```

and let `V0` be the independently sealed v13-checker verdict for the physical
bytes of `R0`.  The v18 producer changes only resource-stop bookkeeping; its
positive object is still this v10 schema and is checked by the frozen v13
arithmetic.

Write

```text
g = R0.g760,
c = R0.correction_word,
f = R0.corrected_word.
```

Acceptance of `V0` is stronger than merely trusting these three arrays.  The
checker reconstructs every selected old/new column, replays coefficient-two
inversion, multiplies the selected literal correction factors, checks their
joint-kernel values, and then independently evaluates

```text
D(c) = model.direct_column([], c).
```

In particular its positive route proves

```text
exp(c) = (0,0),
c is the reduced product of the selected kernel factors,
D(c) is the selected correction-row sum,
f = red(g c),
the eleven-occurrence and direct seven-window evaluations agree.
```

These are the checks in
`crosscheck/check_d972_r07_history_free_positive_fast_resume_v13.py`,
`validate_common`, especially the selected-support loop and the final
`direct_column([], correction_word)` replay.  No producer Boolean is used as
an equality oracle.

## 2. Canonical task193-compatible object

Rebuild the authenticated A0 runtime from the frozen source cone and compute
again, without reading a derived sparse row from `R0`,

```text
(r,replay) = model.direct_column([], c).
```

Let `pub(r)` be the canonical ordered sparse encoding and let `h(r)` be its
canonical SHA-256 digest.  Define the compatibility object `T(c)` in the
existing task186-v2 input schema by the following load-bearing fields:

```text
schema   = d972-r07-normalized-exact-common-word-colgen/v2
status   = COMMON_WORD
terminal = R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD

exactification.positive_receipt = true
exactification.literal.c_exact  = c

exact_direct_replay.row                       = pub(r)
exact_direct_replay.row_sha256                = h(r)
exact_direct_replay.replay.corrected_word     = f
exact_direct_replay.replay.direct_all_seven_replay = true
exact_direct_replay.right_g760_multiplication = true
exact_direct_replay.hexagons                  = true
exact_direct_replay.pentagon_printed_order    = true
```

The remaining provenance fields of the v2 envelope must name the physical
A0 receipt/verdict and the exact adapter producer/checker sources.  They are
not allowed to name a synthetic task186 search.  The whole object is sealed
in the usual canonical JSON form.

The independent compatibility checker reopens the physical `R0` and `V0`,
checks both seals and the verdict-to-receipt byte identity, authenticates the
A0 producer/checker pins, rebuilds the A0 runtime, and recomputes `c`, `f`,
`r`, and `replay`.  Only after equality with every load-bearing field of
`T(c)` may it issue the exact one-line compatibility attestation consumed by
task193.  The attestation artifact must also record the adapter source
identities, so the reused ABI line cannot be confused with an execution of
the old search route.

## 3. Exact-adapter theorem

**Theorem 3.1.**  For every accepted positive pair `(R0,V0)`, the object
`T(c)` above satisfies every mathematical premise read by
`search/d972_r07_second_frattini_affine_prefix_compiler_v1.py` before its
affine-prefix computation.  Running task193 on `T(c)` computes the same three
second-Frattini defects that direct execution on the literal word
`f=red(g760 c)` would compute.

**Proof.**  Task193 first reads

```text
corrected = exact_direct_replay.replay.corrected_word,
c_exact  = exactification.literal.c_exact.
```

It then rebuilds the authenticated task179 runtime and checks

```text
red(g760 c_exact) = corrected,
exp(c_exact) = (0,0).
```

For `T(c)` these are exactly the independently rechecked A0 identities.
Task193 also requires the four direct-replay flags and, before using the
affine rows, requires a literal sparse row and its digest.  The compatibility
checker derives all of them from a fresh call to the same authenticated
eleven-occurrence/direct-seven model; hence the row is `D(c)`, not a copied
claim.

After this gate, every task193 word is constructed only from `corrected`:
the two PB3 hexagon words and the printed-order PB4 pentagon word.  Its three
ordinary direct differences are recomputed from `g760` and `corrected` and
their stacked row is required to equal the supplied direct row.  Therefore a
wrong word, order, sign, occurrence, or direct row is rejected before the
affine-prefix output.  The subsequent prefix automaton and Fox arithmetic
are deterministic functions of that same literal word and the authenticated
task179 runtime.  Thus the emitted `beta1_H1`, `beta1_H2`, and `beta1_P` are
precisely the defects for `f=red(g760 c)`.  QED.

## 4. Zero-base consequence

By v344--v346, the actual A3 base is zero.  Therefore the task193 output of
Theorem 3.1 supplies the missing pointwise row

```text
e1(c) = -beta1(c)
```

for the exact A5 test

```text
e1(c) in (ker Phi)d1.
```

Consequently an accepted A0 word needs no second common-word search and no
task186 search.  It needs only this lossless adapter, one task193 execution,
and then the zero-base A5 membership computation.  If the first word fails,
v346's projected Schreier coset is the complete finite fallback; this theorem
does not linearize the nonlinear map `c -> beta1(c)`.

## 5. Failure boundary

An A0 `UNKNOWN_INPUT` or `UNKNOWN_RESOURCE` artifact cannot be adapted.
Likewise, a receipt without its agreeing independent verdict, a missing
physical source pin, a mismatch in `c`, `f`, `D(c)`, or the eleven/direct
replay, and any pre-existing output path must stop as typed `UNKNOWN_INPUT`.
No SELFTEST word or fixture is an admissible replacement.

Thus the remaining actual dependency is now exact and linear in workflow
order:

```text
A0 COMMON receipt+verdict
 -> lossless A0/task193 compatibility object+independent attestation
 -> task193 beta1(c)
 -> zero-base A5 membership.
```

