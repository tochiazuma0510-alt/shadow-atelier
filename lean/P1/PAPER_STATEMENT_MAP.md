# P1 paper-to-Lean statement map, implementation bundle 106

This is an implementation map, not a paper-fidelity ruling. “Closed” below means that the named
Lean declaration elaborates without a proof placeholder in the local targeted build. Sol retains
the source-fidelity and acceptance gate.

| Paper/workshop item | Lean declaration(s) | Typed scope | Local status |
|---|---|---|---|
| oddH Lemma A: `D_n^3` and even-parity `G_n` | `Dn`, `En`, `par`, `Gn`, `Gn_groupLaws` | `Gn n := {x : En n // par x = false}` with closed multiplication/inverse/group laws | Closed |
| Lemma A marking `X=a_1q_1`, `X in G_n` | `Xg`, `X_mem_Gn`, `Gn_X_eq_a1_q1` | Membership conclusion is on the real subtype, not merely ambient `En n` | Closed |
| Lemma A: `X^2=a_1^2`, `ord(X)=2n` | `Gn_X_sq`, `Gn_ord_X` | Order conclusion assumes `1<n` and `NatOdd n`; ambient power calculation is exposed | Closed |
| Lemma A: `|G_n|=4n^3` | `Gn_card_equiv`, `Gn_card_formula` | Explicit equivalence with three `Fin n` coordinates and two bits, plus exact arithmetic formula; no `Fintype.card` claim | Closed witness; cardinal API not imported |
| oddH window carrier `H_{j,α,β}` | `window.J`, `window.Code`, `window.H`, `window.encode` | `j` is an exact two-point type; `H` is a predicate on actual `Gn n`, not ambient `En n` | Foundation closed |
| oddH Lemma G, subgroup/cardinality core | `window.isSubgroup`, `window.carrierEquiv`, `window.carrier_card_formula` | Closure plus explicit `Code n ≃ H` witness for `2n²` elements | Partial: closed foundation only |
| oddH Lemma G, canonical factorization core | `window.split`, `window.join`, `window.decompositionEquiv` | Exact inverse coordinate maps `Gn n ≃ XCode n × Code n` | Partial: bridge `XCode=⟨X⟩` under oddness, marking-independent coset-index witness, P3 theorem, and parameter injectivity OPEN |
| oddH Lemma C(2), generic P1/P3 equivalence (LA-2) | `window.LeftCosets`, `window.Index2nWitness` (types only) | P1 witness contains `IsSubgrp H` and an exact `Fin (2*n) ≃ LeftCosets H`; it is marking-independent and contains no `X` action or transversal conclusion | OPEN: finite equal-cardinality orbit argument not yet implemented |
| oddH Lemma H(3) and Lemma I (LA-4/LA-5) | no theorem under planned names | Actual conjugation/normalizer and class-cardinality branches are required | OPEN |
| Lambda-REG conclusion | `Lambda`, `LambdaSimplyTransitive` | Real conjugacy-class subtype and exact existence/uniqueness proposition over `Fin (2*n)` | Statement closed; proof OPEN pending exact index/normalizer hypotheses |
| INN, generator calculation | `epow_X_even`, `INN_on_Y`, `inn_fixes_X` | Exact `En n` equalities; not presented as a completed automorphism-extension theorem | Closed calculation island |
| SURJ-Split (a), representative independence | `chiTilde_welldefined` | Natural-residue equality modulo `2*nu` | Closed |
| SURJ-Split (a), unit arithmetic | `chiTilde_isUnit` | `gcd(2m+1,nu)=1 -> gcd(2m+1,2nu)=1` | Closed |
| Integer identity (3.49) | `chiTilde_composition_identity` | Equality in `Int` | Closed |
| Residue consequence of (3.49) | `chiTilde_composition_mod` | Equality in `Nat` modulo `2*nu` | Closed |
| TORS-U abstract comparison | `torsor_compare_unit` | `m` faithful regular, `tau` faithful action, cyclic generators, conjugacy equality; returns unique conjugation-implementing bijective homomorphism | Closed abstract island |
| TORS-U explicit cyclic unit | `fin_cyclic_automorphism_unit` | Additive automorphism of `Fin M`, `1<M`; returns unique `b` with `gcd(b,M)=1` and `phi(k)=k*b` | Closed explicit island |
| TORS-U integration | `CyclicMul`, `torsor_compare_fin_unit` | Typed adapter applies the abstract comparison to additive `C_M` under multiplicative notation and attaches the unique residue-unit classification | Closed |
| Four proposed paper-specific T2 inputs | no declaration; `ShadowAxioms.lean` quarantine note only | Exact source statements are not yet approved | OPEN / quarantined |

The exact theorem-level type digests and sorted axiom sets—including generated theorem
declarations—are in `P1/AXIOMS.manifest.json`.
