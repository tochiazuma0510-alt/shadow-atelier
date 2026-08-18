# Luna reply 157dq — total-linking C3 chief descent

## Verdict

The three versioned executable files are implemented and statically frozen.
They give a fail-closed, same-job producer/checker lane for one strict
index-three descent

```text
L = H ∩ ker(rho_A5)  >  L' = L ∩ ker(total-linking mod 18).
```

No production GAP, Git, or GHA command was run.  The final corrective
lightweight checker self-test passed:

```text
D972_B34_TOTAL_LINKING_C3_CHECKER_SELFTEST_PASS mutations=21
```

The bundle is ready for its first GHA production replay:

```text
B34_TOTAL_LINKING_C3_CHIEF_V1_GO
```

This is deliberately one chief descent only.  Even a production PASS will not
assert isolation of `L` or `L'`, uniform/cofinal iteration, compactness, or
global B4-B.

## Frozen files and SHA-256

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b34_total_linking_c3_chief_v1.g` | 38547 | `dba9adc5a8d06665c89e97697bc737a28ec68096ccd02a58db03ccfe63d1d837` |
| `search/check_d972_b34_total_linking_c3_chief_v1.py` | 53000 | `917b3fef37129850887b3b498d4c7c9ee573cdb7944139652deb2acaf5f2064a` |
| `search/d972_b34_total_linking_c3_chief_gha_driver_v1.g` | 11632 | `46dd32aacb9cc23aad52bfa4944786a45ca060441a73a5e5393419fc2f76e766` |

The driver hard-pins the producer and checker hashes above.  It also pins the
q3, FC8, and 157dp receipts and all registered source/theorem inputs required
by the task.

## FC-beta-1: actual marked lattice and chief factor

Producer and checker independently reconstruct the four deletion images in
the actual `G9` marking.  In tuple order
`[12,13,14,23,24,34]`, the emitted `8 x 6` matrix is

```text
000110
000011
011000
001001
101000
001010
110000
010100
```

Both sides obtain rank `5`, kernel
`{000000,111111}`, and image order `32`.  The producer computes the actual
marked `H9` group once and gates

```text
|H9|  = 32 * 3^24,
|H9'| = 3^24.
```

The checker does not trust those two GAP booleans: it reconstructs `G9'`, the
commutator/conjugation module, and the rank-12 Nakayama certificate proving
`H9'=(G9')^4`.  It also reconstructs the exponent-three collector and proves
that the marked `Pi4[3]` abelian matrix is exactly `I6 mod 3` and that its
derived subgroup has order `3^4`.

The integral lattice is then rebuilt by enumerating the complete `6^6`
residue box:

```text
ker(q_ab) = {3w : w mod 2 is 000000 or 111111}.
```

Its canonical row basis is `6e1,...,6e5,3(1,1,1,1,1,1)`, determinant/index
`23328`, with basis linking sums `[6,6,6,6,6,18]` and gcd `6`.  The receipt
binds the exact-sequence reason
`im(H -> PB4_ab)=ker(PB4_ab -> E4_ab)` and explicitly makes no claim that
`A12^6` itself lies in `H`.

Consequently the certified conclusions are

```text
ell(H)=6Z,
beta(h)=ell(h)/6 mod 3 is onto,
Kbeta=H ∩ ker(ell mod 18),
Phi3(H) <= Kbeta.
```

The natural three adjacent transpositions are replayed on all six edge
classes.  Their Artin word maps and explicit inverse word maps preserve every
PB4 relation and compose to the identity in both `Q4` and `Pi4[3]`.  Their
abelian matrices preserve total linking, hence beta.  Thus `Kbeta` is
`B4`-normal, and the prime-order quotient `H/Kbeta=C3` is an actual chief
factor.

## FC-beta-2: the actual candidate 124

The producer and checker independently expand the registered section DAG

```text
124 -> 45 -> 16 -> 5 -> 1
```

and reconstruct the exact 92-letter candidate (base length 20 plus the
registered correction).  They require

```text
outer=1, shift=0, correction=124,
free exponent sums=(0,0),
word SHA-256=c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b.
```

Every acceptance equation is stored losslessly with its reduced word, word
digest, `Q4` row, `Pi4[3]` coordinates, integer total linking, and `C18`
residue.  Direct gates cover:

- both hexagons through all five cofaces;
- the ordered A.18 pentagon;
- the candidate/base correction and the registered A5 correction in `E3`
  and through all five finer cofaces;
- all six FC-30 source differences;
- all S and T PB4 relations;
- every ST and TS generator composition.

The T word is not an abstract existence witness: it is selected from the
pinned normalized exponent-seven row times the complete registered 27-element
q3 fibre.  Every attempted word is evaluated directly, and the selected
word, attempt count, relations, and two-sided residuals are recorded.

### Five-coface coupling correction

The five formal total-linking rows are exactly

```text
111, 221, 212, 122, 111  (mod 3 when reduced),
```

with formal rank `3` and F2-column rank `2`.  These ranks are explicitly
diagnostic only; the implementation does not infer the joint pullback image
from component abelianizations.

Instead it restricts S and T to canonical PB3 order `[x12,x13,x23]` and, for
each of all five cofaces, directly replays:

- S and T PB3 relation residuals;
- ST and TS on all three generators;
- the intertwining of each source image with the authenticated global
  `E4 x C18` automorphism.

This common-global-automorphism/intertwining diagram handles possible
cross-component coupling without constructing or enumerating the joint
group.  The same actual fifteen-component tuple is also used to compute
`N_ord` from `x`, `y`, and `c=x12*x13*x23`.

## FC-beta-3: A5 intersection, orders, and outside class

The FC8 input is not consumed as a `surjective=true` assertion.  Both sides
reconstruct the compact `D_F` image and its derived subgroup, the four
single-support words, each order-60 normal closure, the transitive `S4`
factor action, and the perfect/simple `A5` factor.  Perfectness supplies the
no-`C3`-quotient gate, so Goursat gives `L Kbeta=H` and `[L:L']=3`.

Definition 3.1 orders are evaluated in the actual quotient components using
all three words `x`, `y`, and `c`, never only `A12`:

```text
H_ord=18, Kbeta_ord=18, L_ord=90, L'_ord=90,
gcd(L_ord,Kbeta_ord)=18.                 (FC-29)
```

The selected roof is rebound independently to the frozen 972-key normalized
orbit: row 37 is exponent `2`, the square of the row-19 pure axis, and
`3` does not divide `2`.  The accepted `X/W ~= S3 x C6` complement classifier
then proves it is outside `A`; no q3 arithmetic-outside boolean is used.

## Terminal and claim boundary

The checker reconstructs the terminal bidirectionally:

- all gates pass: `B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED`;
- a fully evaluated literal gate fails:
  `B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED`.

The latter is only a rejection of candidate 124 and is never B4-A.  Missing
or capped typed input is reserved for the two explicit UNKNOWN tokens.  On a
PASS the exact permitted implication is only:

> one outside `GT^heart(L')` pair exists, and accepted T48-1 moves the known
> window from `L` to the strict index-three subgroup `L'`.

Settlement is recorded as diagnostic-only.

## Driver and resource contract

The thin driver removes all fixed artifacts/logs/sentinels, regenerates q3,
FC8, and 157dp through the pinned 157dp driver exactly once, and requires each
independent checker PASS before running the new producer/checker in the same
job.  The registered two nonsemantic 157dp runtime observations are normalized
only after proving every other parsed field unchanged; the frozen raw SHA is
then required and the upstream checker is rerun.

New-core operation bounds are:

```text
candidate scans                  0
registered candidates replayed  1
inverse fibre cap                27
H / E4 / A5^4 element listings   0
PB5 / ANUPQ calls                0
translation BFS                 0
sparse Gaussian searches        0
five-component intertwining     30 residuals
```

No full PB3 pullback group is enumerated.  The largest explicit checker
enumerations remain the already established small `G9`/A5/D_F groups; the new
five-component check is word evaluation only.

### Transport-only failure in run 32194128426

The first registration run, commit `a5769bab`, was reported green by the
outer job but did not start an upstream producer.  GAP stopped while parsing
driver line 162: the two double-quoted strings inside the shell `-c` payload
were not escaped inside the enclosing GAP string.  The uploaded artifact
contained only the driver source and run log; it contained no q3/FC8/157dp
receipt, no 157dq receipt, and no mathematical checker result.  Run
`32194128426` is therefore a transport failure and supplies no mathematical
evidence.

The repair changes only those two delimiters, exactly following the frozen
157dp driver's quoting convention:

```text
D972_B34_A5_SELECTED_LIFT_OUTPUT:=\"ci/out/...json\"
Read(\"search/...driver_v1.g\")
```

Producer, checker, candidate, predicates, terminal meanings, and all frozen
input pins are unchanged.  The permitted local driver SELFTEST subsequently
parsed the repaired driver and returned exactly:

```text
D972_B34_A5_SELECTED_LIFT_CHECKED_IO_SELFTEST_PASS
D972_B34_TOTAL_LINKING_C3_CHECKED_IO_SELFTEST_PASS
D972_B34_TOTAL_LINKING_C3_CHECKER_SELFTEST_PASS mutations=21
B34_TOTAL_LINKING_C3_GHA_DRIVER_PASS mode=selftest
```

Source-only estimate, pending first GHA calibration:

- new producer: approximately 2--10 seconds;
- new independent checker: approximately 3--12 seconds;
- same-job regeneration plus new lane: approximately 25--60 seconds;
- expected peak memory: below 1 GB.

## Static audit

- producer function/end balance: `27/27`;
- producer conditional balance: `43/43`;
- producer and driver are ASCII-only;
- driver producer/checker pin chain: exact;
- forbidden new PB5/ANUPQ/full-universe operations: absent;
- only the four authorized files were created or changed.

The first development Python self-test invocation exposed only aliasing in the
synthetic mutation fixture (list multiplication had shared rows).  The fixture
was corrected without changing production logic.  After explicit permission,
the single corrective invocation produced the 21-mutation PASS quoted above;
no further Python run was made.  After the transport repair, one separately
authorized GAP driver SELFTEST produced the four PASS markers above.  No local
production GAP, Git, or GHA run was made.
