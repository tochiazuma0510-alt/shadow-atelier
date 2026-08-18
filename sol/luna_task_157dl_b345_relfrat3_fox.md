# Luna task 157dl — B345 relative Frattini-3 sparse Fox positive lane

Date: 2026-08-18

## 0. Role, target, and non-regression

Implement the first exact positive-semidecision at the relative mod-3
Frattini stage below the successful authenticated q=3 stage. This is not a
rerun of the ambient exponent-3 scan and not a claim of final B4-B.

Read completely before editing:

- `sol/luna_reply_157dk_b345_q3_positive_run_record.md`
- `docs/対話帳.md`, T-29 through T-34
- `sol/luna_reply_157da_b345_q3_chief.md`
- `sol/luna_reply_157cq_b4_cofinal_compactness.md`
- `search/d972_b345_q3_chief_v1.g`
- `search/check_d972_b345_q3_chief_v1.py`
- `search/d972_b345_q3_gha_driver_v1.g`
- the PB3/PB4/PB5 presentations and coface/deletion code used by 157da

All earlier closed claims remain fixed. In particular, do not re-audit the
successful ambient q=3 witness, one-outside, or compactness.

## 1. Authorized files only

Create/edit only:

```text
search/d972_b345_relfrat3_v1.py
search/check_d972_b345_relfrat3_v1.py
search/d972_b345_relfrat3_gha_driver_v1.g
sol/luna_reply_157dl_b345_relfrat3_fox.md
```

Do not edit workflows, frozen q3 files, prior replies, CLAIMS, or any other
file. No Git, push, or GHA. Do not run local GAP or heavy/parallel Python.
One lightweight producer/checker self-test is allowed if it does not build
the production quotient.

## 2. Frozen base and mathematical target

Pin exactly:

```text
q3 producer b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
q3 checker  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
q3 driver   c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
formula     b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
successful artifact SHA
            3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

Let `q_r: PB_r -> E_r` be the matched quotient reconstructed from the frozen
q3 receipt and let `H_r=ker(q_r)`. The target is

```text
Phi_r = closure(H_r^3 [H_r,H_r]),
V_r   = H_r/Phi_r = H_1(H_r,F3).
```

One fully literal charming/onto outside pair at target `Phi_4` proves the
same outside roof survives into every isolated elementary-F3 chief
refinement `L` with `Phi_4 <= L <= H_4`; `Phi_4` itself need not be isolated
or settled.

## 3. Same-job bootstrap

The new GAP driver must pin and invoke the frozen q3 driver in full mode to
regenerate and independently check
`ci/out/d972_b345_q3_chief_v1.json` in the same job. Only after the existing
q3 checker PASS/sentinel may it run the new Python producer and independent
checker. Do not trust an unbound or stale JSON.

The new Python producer consumes the exact q3 JSON and writes a new canonical
receipt. The new checker must not import producer helpers. The driver must
use exact fixed paths, delete stale logs/sentinels before each invocation,
require exit-zero sentinels and exactly one terminal/checker marker, and bind
all source SHA values.

## 4. Exact sparse Fox model

For each required arity use the independently generated finite presentation

```text
PB3: d=3,  m=2
PB4: d=6,  m=11
PB5: d=10, m=35
```

over `k=F3`. With right/left conventions explicitly frozen, construct sparse
group-ring maps

```text
k[E]^m --D2--> k[E]^d --D1--> k[E]
```

from evaluated Fox derivatives. Gate `D1*D2=0` literally. For every
`w in H`, compute its finite-support gradient and use only the equivalence

```text
w in Phi_3(H)  iff  gradient_q(w) is in image(D2).
```

A positive membership claim must include a lossless finite ledger of
translated relator columns and coefficients in F3 whose exact sparse sum is
the gradient. The checker reconstructs presentations, Fox derivatives,
quotient multiplication/keys, every translation, and the equality without
sharing helpers.

Never construct a full regular-module matrix, full H1 basis/rank, full
isotypic decomposition, coset table, Reidemeister-Schreier presentation, or
relative ANUPQ quotient.

## 5. Candidate order and first positive lane

Fix the exact outside word from the successful receipt first:

```text
[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
```

Try the empty correction first. Its current roof, marking, and all base q3
gates must be replayed, not merely copied. Then seek sparse boundary
certificates for:

- both literal hexagon residuals;
- the literal ordered five-coface A.18 pentagon residual;
- all representative/marking residuals which are actual group equalities;
- forward and inverse generator-composition residuals sufficient to prove
  onto at the finer target.

Onto may be certified by a two-sided inverse on the marked PB generators:
the base E maps are the frozen settled automorphisms, and every `ST(x_i)x_i^-1`
and `TS(x_i)x_i^-1` must have an exact sparse Phi membership certificate.
Do not require Phi isolation or parameterize all Phi shadows.

If the empty correction fails to obtain certificates within the registered
search cap, proceed to a bounded correction dictionary of explicit words in
the **coarse source kernel** `J_H=ker(PB3 -> E3)`.  Their classes modulo the
finer source kernel

```text
J_Phi = intersection over the five A.18 cofaces of preimage(Phi_4)
```

are precisely the lift freedom.  Do **not** require a correction itself to lie
in `J_Phi`: that would make it trivial in the finer source quotient and reduce
every candidate to the empty-correction class.  Authenticate `c in J_H` by
checking that all five PB3-to-PB4 coface images are identity in the frozen
coarse `E4=PB4/H4` (an E3 identity test alone is sufficient only if the
receipt separately proves that E3 is exactly this five-preimage quotient);
the full corrected word must then pass all ten
five-coface hexagon certificates, the direct pentagon, charming, and onto
certificates at `Phi_4`.  Do not identify `J_Phi` with `Phi_3(H3)` without
proof. Construct dictionary words from authenticated kernel/relator/preimage
words in the q3 receipt and record the complete preregistered order. Small
representation projections may prioritize or reject a candidate, but a
positive must end in full sparse group-ring certificates.

Run direct B3/B4 positive-first. Construct PB5/six pentagon/three square
objects only if the direct lane yields no certified pair. A bounded search
failure is UNKNOWN, never an exact obstruction.

## 6. Performance caps and prohibited work

Use at most:

```text
small representation dimension             64
candidate correction dictionary           4096 words
coefficient translates per relator        32768
total sparse group-ring keys             1000000
single word/section length                 100000
affine residual dimension                     12
explicit affine candidates                531441
ambient PB5 ANUPQ                               1 (only if B5 branch is needed)
relative ANUPQ / RS / full Elements             0
```

Log phase runtimes and live support/basis sizes. Cache quotient word values,
Fox gradients, translated columns, and row pivots. Never recompute the same
long word for each candidate. Cap/resource exhaustion must serialize a
precise UNKNOWN reason and still reach the independent checker.

## 7. Receipt and independent checker

Schema: `d972-b345-relative-frattini3/v1`.

Bind at least:

- all frozen input hashes and q3 artifact hash;
- selected word/correction and roof identity;
- presentation/formula digest and Fox convention canaries;
- sparse D1/D2 supports and `D1D2=0` receipts;
- exact q3 quotient element keys used by every support term;
- J3 five-coface source certificates;
- every residual gradient and translated-relator boundary ledger;
- literal hexagon/pentagon/charming/marking replay;
- two-sided inverse/onto certificates;
- search universe/order/caps, visited supports, cache counts, and timings;
- theorem boundary: all isolated elementary-F3 chief refinements immediately
  below current H are covered; nonabelian, other primes, deeper iteration,
  and global B4-B are not claimed.

The checker independently rebuilds every accepted equality and rejects
mutations of orientation, support key, coefficient, relator index,
translation, coface, selected word, inverse word, roof, terminal, or source
hash. Do not accept producer booleans in place of reconstructed facts.

## 8. Terminals

Use exactly one:

```text
B345_RELFRAT3_LITERAL_PAIR_PASS
B345_RELFRAT3_PROJECTED_OBSTRUCTION
B345_RELFRAT3_SEARCH_INCOMPLETE
B345_RELFRAT3_MISSING_MATCHED_CHAIN
B345_RELFRAT3_UNKNOWN_RESOURCE
```

Only `...LITERAL_PAIR_PASS`, followed by independent checker PASS, proves
the Relative-Frattini-3 jump for all isolated elementary-F3 next-chief
refinements. None of these terminals alone is final B4-B.

End the reply with one implementation readiness token and exact hashes.
