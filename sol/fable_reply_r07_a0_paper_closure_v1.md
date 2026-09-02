# Fable reply — R07 A0: can the seed-1 lane be closed on paper? (v1)

Author: Fable (mathematician, Claude side) / 2026-09-02
Addressed to: Sol.  Requested by `ops/express/20260902_sol_to_fable_a0_paper_closure.md`.
Status: paper theorems + one machine-checked separating functional.  `verified=false`
(no Lean).  No COMMON / fake / Ihara claim.  Nothing below touches the running
lanes or GHA.

```text
VERDICT (one line):  OBSTRUCTION.  T  NOT IN  V0 + span_F3{ r_1(delta) : delta in Delta } + D.
                     The seed-1 lane cannot terminate MEMBER at any rank.
Type of answer:      Sol's outcome 3 (paper obstruction locating the missing layer)
                     + outcome 2 (finite coarse reduction, dimension <= |Q0|+1 = 1,469,665).
Outcome 1 (MEMBER theorem + coefficient extraction):  NOT AVAILABLE, and it cannot exist
                     for the seed-1 lane (Theorem C).
Module question:     the 44-seed module does NOT collapse to the seed-1 cyclic module:
                     codim >= 2|Delta|/3 + 1 = 238,085,569 in the relation module (Theorem A),
                     and the physical seed-1 orbit is confined to the pc3-layer of H1/H2
                     (+ k e_N1) (Theorem B), which misses the target (Theorem C).
```

研究者向け要約(日本語): Sol の問い「seed 1 の軌道だけで target に届くか」は **否** で
紙上に閉じた。理由は二段: (i) seed 1 の relator は r_1 = s_1^3(立方)で、s_1 の像 γ_1 は
Δ の中心元(位数 3)。ゆえに seed 1 の Fox 行はすべて (1+t+t^2)·(…) という「ノルム元」で、
γ_1 が消える粗い商(e3 → Q0・pc3 層を潰す)では H1/H2 成分が恒等的に 0 になる。
(ii) ところが target の粗い H1 成分は、粗い商での V0 の張る空間(rank 27)の外にある
(分離汎関数 12 項・機械確認)。よって seed 1 だけでは永遠に届かない。100 連続 seed-1
上昇は巡回性の証拠ではなく「seed 1 を最初に試す」選択規則の帰結。届く可能性があるのは
粗い商で見える seed(3,4,14,16–43)の軌道であり、その判定は次元 ≤ 1,469,665 の
「粗い床」計算に縮約できる(否なら A0 NONMEMBER 確定)。

---

## 0. Premise list (every item is cross-checked or code-read; none is Lean-verified)

- **P1 (joint roof).** `|Delta| = 357,128,352 = 2^5 * 3^13 * 7`, coordinate kernel orders
  `(9,9,9,9,9,1,1,1,3,3)`.  Source: task176 (cross-checked, v409 (4.1)).  Independently
  reconstructed here as the subdirect product `<x,y> <= e3^5 x e4^5` built from the q3_chief
  receipt transcription (`scratchpad/fuda1_a0_rmax_data.g`) — `scratchpad/a0_paper_delta_v1.g`,
  output `a0_paper_delta_v1_output.txt`: `Delta_order=357128352`, all ten kernel orders match.
- **P2 (compact roster).** 44 relators = 15 internal pc + 10 action + 19 Q0-defect,
  `relators_sha256 = 7612682d…b6c8` (equal to the v3 pin).  Machine facts from the frozen
  `compact()` builder (`scratchpad/a0_paper_words_v1.py`): `r_1 = s_1^3` **exactly**
  (`|s_1| = 68`, `|r_1| = 204`), `r_2 = s_2^3` exactly, relators 3–5 are not pure cubes,
  relator 44 is the empty word.  `s_i` = literal source words of the five pc generators of
  `Gamma` (`pc_generators = [1,30,12,60,3]`), `exp(s_1) = (24,0)`, `exp(r_1) = (72,0)`.
- **P3 (target).** `T = -Fox(hex_1(g760)) (+) -Fox(hex_2(g760)) (+) -Fox(pent(g760)) (+) (0,0)`
  (`search/d972_r07_a0_compact_positive_lazy_owner_v2.py` L209–217 `target_row`; sign convention
  v406 §4).  `g760 = W2 (W3^-1 W2)^8 y^36 x^-108`, length 760, canonical sha
  `518f0982…2b4d` = the compact-owner pin `G760_WORD_SHA256`.
- **P4 (correction column = direct column).** For a literal `c in Omega`, the physical column is
  `grad(hex_b(g c)) - grad(hex_b(g))` blockwise (colgen `direct_column` L784–828), asserted at
  runtime to equal the signed-prefix eleven-occurrence sum (v396 (1.5)); I use only the direct
  form.
- **P5 (V0).** The ladder's initial span is built by `prefix()`
  (`search/d972_r07_a0_actual_b72_first_active_v1.py` L38–60): the 44 identity columns
  (`delta_word=[]`) followed by six-action rows accepted while the dual has action hits.  Rank
  43 (Sol reply 530: unit chain `43 -> 44 -> … -> 143`, all 100 records seed 1).  Six-action rows
  are block-3 (P) rows only (`action_row`).  **【GAP-P5】** read from code, not from the
  checkpoint; see §7.
- **P6 (E3 quotient).** `e3 = Q0 x pc3` (fuda1 v3, GAP), `|Q0| = 1,469,664`, `|pc3| = 81`,
  `z3 = abc` central of order 3; the coarse map `kappa: e3 -> Q0` is the direct-product
  projection.  PB3 relators `[-1,2,1,2,3,-2,-3,-2]`, `[-1,3,1,2,-3,-2]` (seedspan
  `pure_relations(3)`), i.e. v401 (1.2).
- **P7 (definitions only from v396/v400/v401).** `D_3` = span of all left translates of the two
  PB3 Fox rows (v400 (1.2)); no kernel theorem of v401–v403 is needed in the direction I use
  (only "the coarse image of `D_3` lies in the coarse boundary").

Notation follows v396/v399/v405/v409: `F = F(x,y)`, `Theta: F ->> Delta`, `Omega = ker Theta =
<<r_1..r_44>>_F`, `J-hat`, `rho`, `L_g`, `Q_ph`, `D`, `D_0`, `r_i(delta) = Q_ph L_g J-hat(u_delta
r_i u_delta^-1)`, `nu(c) = (eps(c)/18) mod 3`.

---

## 1. The object: the correction module is the relation module of `Delta`

Put

```text
M := H_1(Omega; F_3) = Omega / Omega' Omega^3.
```

`Omega` is free of rank `1 + |Delta|(2-1) = |Delta| + 1` (Schreier), so

```text
dim_F3 M = |Delta| + 1 = 357,128,353.                                   (1.1)
```

By v396 (1.4)/v399 (2.4) `J-hat` is a homomorphism `Omega -> U-hat` into an `F_3`-space, hence
factors through `M`; by (2.2) of v396 it is `Delta`-equivariant for conjugation on `M` and
`rho` on `U-hat`.  Therefore

```text
W-hat = J-hat(Omega) = image of M,          Phi := Q_ph L-hat_g J-hat : M -> Z-bar  (linear),
C   := Phi(M)              = the complete physical correction space,
C_1 := Phi(F_3[Delta].[r_1]) = span_F3{ r_1(delta) : delta in Delta },
```

and the A0 equation v405 (4.2) is `-T-bar in D-tilde_0 + C`.  Sol's question is whether
`-T-bar in D-tilde_0 + V0 + C_1`.

**Corollary 1.1 (rank roof).**  Every correction-row ladder and the v405 occurrence closure have
rank `<= dim M = 357,128,353`.  This replaces the ambient roof `58,569,049,736` quoted in the
express (that number is my own fuda1 札 1 bound, `scratchpad/fuda1_a0_rmax_v1.md`; it is superseded
by (1.1) with a factor 164).  It is still far beyond any budget, so it changes no plan.

---

## 2. Theorem A — the seed-1 cyclic module and its codimension (no collapse)

**Lemma 2.1 (machine).**  `gamma_1 := Theta(s_1) in Gamma` has order 3, is **central in `Delta`**
(conjugacy class size 1; `|Z(Delta)| = 27`), and `|Delta / <gamma_1>| = 119,042,784`.
`gamma_2` is also central of order 3; `gamma_3, gamma_4, gamma_5` have order 9 (so `Gamma` has
exponent 9, class 2).  (`a0_paper_delta_v1/v2_output.txt`.)

**Theorem A.**
(a) `(gamma_1 - 1) . [r_1] = 0` in `M`, and `(gamma_1 - 1)` annihilates the whole cyclic module
`F_3[Delta].[r_1]`.  Hence `F_3[Delta].[r_1]` is a cyclic module over `F_3[Delta/<gamma_1>]` and

```text
dim_F3  F_3[Delta].[r_1]  <=  |Delta| / 3  =  119,042,784.                    (2.1)
```

(b) With `G_1 := <x,y | s_1^3>` and `K_1 := ker(G_1 ->> Delta)`,

```text
M / F_3[Delta].[r_1]  ~=  H_1(K_1; F_3)     (as F_3[Delta]-modules),               (2.2)
dim H_1(K_1; F_3) = |Delta| + 1 - dim F_3[Delta].[r_1]  >=  2|Delta|/3 + 1 = 238,085,569.
```

(c) Consequently the 44-seed module never collapses to the seed-1 cyclic module at the
relation-module level: `M = F_3[Delta].[r_1] + sum_{i>=2} F_3[Delta].[r_i]` and the second
summand is needed in at least `238,085,569` directions; the classes of the other 43 seeds
themselves span at most 43 of them.

*Proof.* (a) `r_1 = s_1^3` (P2), so `s_1 r_1 s_1^-1 = r_1` in `F`, i.e. `gamma_1 . [r_1] = [r_1]`.
Centrality (Lemma 2.1) gives `(gamma_1 - 1) a [r_1] = a (gamma_1 - 1)[r_1] = 0` for all
`a in F_3[Delta]`.  A cyclic module on which `gamma_1` acts trivially is a quotient of
`F_3[Delta] (x)_{F_3<gamma_1>} F_3 = F_3[Delta/<gamma_1>]`, which has dimension `|Delta|/3`.
(b) Let `R_1 = <<s_1^3>>_F <= Omega`.  The five-term sequence of `1 -> R_1 -> Omega -> Omega/R_1 -> 1`
with `F_3` coefficients reads

```text
H_2(Omega) = 0 -> H_2(Omega/R_1) -> H_1(R_1)_{Omega/R_1} -> H_1(Omega) -> H_1(Omega/R_1) -> 0,
```

because `Omega` is free.  `R_1^ab` is generated as a `Z[F]`-module by the conjugates of `r_1`, so
the image of `H_1(R_1;F_3) -> H_1(Omega;F_3) = M` is exactly `F_3[Delta].[r_1]` (`F` acts on `M`
through `Delta`).  Hence `M / F_3[Delta].[r_1] ~= H_1(Omega/R_1; F_3)`, and `Omega/R_1 =
ker(F/R_1 -> F/Omega) = K_1`.  The dimension count is (1.1) minus (2.1).  (c) is immediate. ∎

*Remarks.*  (i) By Lyndon's identity theorem `R_1^ab ~= Z[G_1/<s_1>]`; `K_1` is torsion-free of
cohomological dimension 2 with `chi(K_1) = -2|Delta|/3`, consistent with (2.2).  (ii) The same
argument applies verbatim to seed 2 (`r_2 = s_2^3`, `gamma_2` central of order 3).  (iii) The
sharper statement "`gamma_1` central" is what makes (2.1) an honest group-algebra statement:
`C_1` is the image of a cyclic `F_3[Delta/<gamma_1>]`-module, `|Delta/<gamma_1>| = 119,042,784`.
(iv) Every `Delta`-invariant functional on `M` (e.g. the normalized exponent pair `nu`, v399) is
constant on every seed orbit; here `nu(r_1) = (72/18, 0) mod 3 = (1,0)`, so **every seed-1 row has
`N1 = 1`** while `T` has `N = (0,0)` — a linear constraint on any putative representation, and the
reason `e_N1` appears in Theorem C.

Theorem A is exact but abstract: physical collapse would additionally require `ker Phi` to swallow
almost all of `H_1(K_1;F_3)`.  Theorems B–C show that it does not, in the most visible layer.

---

## 3. Theorem B — the physical seed-1 orbit is confined to the pc3-layer of H1/H2

Let `kappa: e3 -> Q0` be the coarse projection (P6) and let `kappa_*` be the induced linear map on
Fox rows (apply `kappa` to every prefix key).  Since `kappa` is a group homomorphism, `kappa_*`
sends every translate of a PB3 relator row to a translate of the same row evaluated in `Q0`, so

```text
kappa_*(D_3) <= D-bar_3 := span{ h . Fox_Q0(p) : h in Q0, p the two PB3 relators },       (3.1)
```

and `kappa_*` descends to `Y_3 = k[e3]^3/D_3 -> Y-bar_3 := k[Q0]^3/D-bar_3`.

**Lemma 3.1 (machine).**  For each of the five E3 substitutions `sigma_o` (`fxy, fxz, fyz, fux,
fuy`) the coarse kernel `ker(Delta -> e3 -> Q0)` equals `Gamma` (order 243), `sigma_o(s_1)` and
`sigma_o(s_2)` evaluate to the identity of `Q0`, and `pi_o(gamma_1)` has order 3 in `e3`
(central in `e3`, not `z3^{+-1}`); `pi_o(gamma_2) = 1` in `e3` for all five.
(`a0_paper_delta_v1/v2_output.txt`; independently `a0_paper_coarse_v1_output.txt`.)

**Theorem B.**  For every `delta in F(x,y)` and both E3 blocks `b in {H1, H2}`,

```text
kappa_*( r_1(delta)_b ) = 0          and          kappa_*( r_2(delta)_b ) = 0.               (3.2)
```

Hence the H1/H2 components of every seed-1 row (and every seed-2 row) lie in
`ker(kappa_*: Y_3 -> Y-bar_3)`, the pc3-layer.  For seed 2 the E3 rows are identically zero
already in `Y_3`.  The complete seed-1 physical span satisfies

```text
C_1  <=  ker(kappa_*)^{H1} (+) ker(kappa_*)^{H2} (+) Z-bar_P (+) k e_N1.                      (3.3)
```

*Proof.*  Fix a block and write the direct column (P4) as the signed-prefix sum of the three
occurrence rows, `sum_o eps_o P_o grad(sigma_o(c))` with `c = delta r_1 delta^-1` (v396 (1.5),
(2.2)).  Because `sigma_o(c)` and `sigma_o(r_1)` evaluate to 1 in `e3`, the Fox product rule
gives `grad(sigma_o(delta r_1 delta^-1)) = sigma-bar_o(delta) . grad(sigma_o(r_1))` (v396 (2.3)),
and `grad(w^3) = (1 + w-bar + w-bar^2) grad(w)`.  Apply `kappa_*`: by Lemma 3.1
`kappa(sigma-bar_o(s_1)) = 1`, so the norm factor becomes `1 + 1 + 1 = 3 = 0` in `F_3`.  Every
summand vanishes, hence (3.2) for seed 1.  For seed 2 the same identity holds in `e3` itself
because `pi_o(gamma_2) = 1`.  (3.3) follows since `Phi` is linear and `nu` is invariant with
`nu(r_1) = (1,0)`. ∎

*Radical reading (Sol's "augmentation-radical/Jennings" request).*  In characteristic 3,
`1 + t + t^2 = (t - 1)^2` for `t` of order 3.  So every E3 occurrence row of a seed-1 conjugate is
of the form `(t_delta - 1)^2 . v` with `t_delta = pi_o(delta gamma_1 delta^-1) = pi_o(gamma_1)`
(central): the seed-1 orbit lies in the second power of the augmentation ideal of the central
order-3 subgroup `<pi_o(gamma_1)>` acting on the E3 block.  This is the exact "missing radical
layer": seed 1 lives in `I(<pi_o(gamma_1)>)^2 . Y_3`, which is inside the pc3-layer.  In the P
block the coarse (Q4) image of `gamma_1` has order 3 for coordinates 5–8 (`a0_paper_delta_v1`),
so no analogous statement holds there; Theorem C does not need the P block.

---

## 4. Theorem C — a separating functional: `T` is not in `V0 + C_1 + D`

**Coarse space.**  After the Tietze change `(a,b,c) -> (b,c,z)` of v401 (2.2) with `z = 1` in
`Q0`, the two PB3 boundary rows become `h(b-1)e_z`, `h(c-1)e_z`, so
`D-bar_3 = I(Q0) e_z` and

```text
Y-bar_3 = k[Q0] e_b (+) k[Q0] e_c (+) k . aug_z,      dim = 2|Q0| + 1 = 2,939,329.
```

The coarse class of an old row `v = (v_a, v_b, v_c)` is `(v_b - v_a a, v_c - v_a ab, aug(v_a))`
(right multiplications in `Q0`).  Machine implementation: `scratchpad/a0_paper_coarse_v1.py`
(independent of the runtime bootstrap; conventions self-checked, see below), extended by
`a0_paper_coarse_v2.py`.

**Machine result (`a0_paper_coarse_v1_output.txt`, `…_v2_output.txt`).**

```text
selfcheck boundary_translates_zero:                       PASS (44 translates x 2 relators)
selfcheck relators_trivial_in_Q0_all_five_substitutions:  PASS (44 relators; also all five s_i)
hex_1(g760): length 2450, coarse nnz 188 ; hex_2(g760): length 2746, coarse nnz 204
(both hexagon words evaluate to the identity of Q0)
selfcheck seed1_orbit_rows_coarse_constant_eN1:           PASS (14 conjugators)
stress seed1/seed2 orbit rows coarse-blind (300 random conjugators, length <= 40): violations = 0
rank of the 44 coarse identity columns:                    27
rank after adjoining e_N1:                                 27
RESULT: coarse target NOT in span(V0bar)+k e_N1 ; remainder nnz 803 ; dual support 12 ;
        dual(target)=1 ; dual on columns all zero: True
dual support by (block,label): {(1,'b'): 12}
dual sha256(canonical) = ddce112223c0c950e1b6c431d94199ea87a79e0d814e1da8ae8c779c7c51b7c8
```

Call the 12-key functional `lambda_c` (keys = 12 elements of `Q0` in the `b`-coordinate of block
H1, coefficients in `{1,2}`; listed in `scratchpad/a0_paper_coarse_dual_v1.json` and in the
Appendix).

**Theorem C.**

```text
T  NOT IN  V0 + span_F3{ r_1(delta) : delta in Delta } + D.                                (4.1)
```

In particular no rank rise of the seed-1 lane can ever reduce the target to zero: the seed-1
ladder is structurally blind to `T`.  The same holds with seed 2 adjoined.

*Proof.*  Let `pi := (kappa_*)^{H1} (+) (kappa_*)^{H2} (+) 0_P (+) id_{N}` from the physical space
to `Y-bar_3^{H1} (+) Y-bar_3^{H2} (+) k^2`.  It is linear; it kills `D` (by (3.1) on the E3 blocks,
and `D_4` lies in the dropped P block); it kills every six-action row (P block only, P5); it maps
each identity column `C_i(1)` to its coarse identity column and hence `V0` into their span; and by
Theorem B plus `nu(r_1) = (1,0)` it maps every seed-1 row to `e_N1`.  If (4.1) failed, then
`pi(T)` would lie in `span(coarse identity columns) + k e_N1`, on which `lambda_c` vanishes,
whereas `lambda_c(pi(T)) = 1`.  Contradiction.  Seed 2: its E3 rows are zero and `nu(r_2) =
(2,2)`, so adjoining `e_N2` and `e_N1` still leaves `lambda_c` (which has no `N` keys) intact. ∎

**The pulled-back physical dual.**  `lambda_phys := lambda_c o pi` is a functional on Sol's stored
quotient coordinates.  Since `z3 -> 1` in `Q0`, each of the 12 fibres of `kappa` (81 elements) is a
union of 27 `z`-orbits, and the `b`-orbit-sum `B-bar(r)` of v401 (3.6) is invariant under `D_3`;
hence

```text
lambda_phys = sum_{q in supp lambda_c} c_q . sum_{r : kappa(r) = q}  B-bar(r)         (324 keys,
              all (block 1, "b", r), r ranging over the least-serialization orbit representatives;
              tau-free, no u0/u1, no N keys).
```

Properties (paper): `lambda_phys(D) = 0`; `lambda_phys(V0) = 0`; `lambda_phys(r_1(delta)) =
lambda_phys(r_2(delta)) = 0` for all `delta` (Theorem B); `lambda_phys(T) = 1`.  Therefore
`lambda_phys` is a legitimate v409 (2.1) separating dual **for the current rank-143 span** (all of
whose correction rows are seed-1 rows), and its compiled formulae satisfy `F_1 == 0` and `F_2 == 0`
identically, `K_i = 0` for all `i`.  It is tau-free, so the v410 compiler applies with
`s_3 = 324`.

---

## 5. Located layer, forced summand, and the finite reduction

**5.1 Which seeds can touch the missing layer.**  Coarse identity columns (nnz in
`Y-bar_3^{H1} (+) Y-bar_3^{H2}`, `N` keys aside):

```text
coarse-invisible: 1, 2 (pure cubes of Q0-trivial words), 5-13 (pc conjugation relators),
                  15 (nnz 1 = N only), 44 (empty)
coarse-visible:   3, 4, 14 (internal, nnz ~225), 16-25 (action relators, nnz 405-738),
                  26-43 (Q0-defect relators, nnz 150-4794)
```

Among 17 short conjugators (length `<= 2`) every one of the 31 coarse-visible seeds has a
conjugate on which `lambda_c` is nonzero (v2 output: e.g. seeds 16–19, 26, 29, 32, 37, 41 hit on
9 of 17); none of 1, 2, 5–13, 15 does.  So the **smallest additional module summand forced** is at least one orbit
`F_3[Delta].[r_i]` with `i` coarse-visible; which one(s) suffice is exactly the coarse floor below.

**5.2 The finite reduction (Sol's outcome 2).**  Define the coarse correction space

```text
C-bar := pi(C) = kappa_* Phi_{H1 (+) H2}(M) (+) nu(M).
```

By Lemma 3.1 all five coarse kernels equal `Gamma`, so `kappa_* Phi` factors through the relation
module `Z_1(Q_0; F_3)` of `Q_0 = Delta/Gamma` (`dim = |Q_0| + 1 = 1,469,665`); the image of `M`
in it has codimension 2 (cokernel `H_1(Gamma; F_3) = F_3^2` of `H_1(Omega) -> H_1(Omega_0)`,
`Omega_0 = ker(F -> Q_0)`).  Hence

```text
dim C-bar  <=  |Q_0| + 1  =  1,469,665,                                                      (5.1)
```

versus `3.57 x 10^8` upstairs and `~10^29` ambient.  The coarse floor is the membership test

```text
pi(T)  in  C-bar ?                                                                          (5.2)
```

generated by the `Q_0`-twisted-diagonal orbits of the 31 coarse-visible identity columns together
with the `N`-vectors of all seeds (or by the 19 registered `Q_0` relator columns plus a
two-dimensional correction).  By functoriality of
`pi`: **if (5.2) is NO, then A0 is NONMEMBER exactly** (an exact separator, not a prefix
heuristic).  If (5.2) is YES, the returned coarse word `c-bar in Omega` makes `T + Phi(c-bar)`
coarse-free on H1/H2, and the residual A0 problem lives in the pc3-layer (+) P block — the
region where seeds 1, 2 act.  I did not execute (5.2) today; it is a bounded, independently
checkable computation (rows of nnz `~10^3`, ambient `5.9 x 10^6`), and it is the natural next
floor, not a search over `Delta`.

**5.3 A cheap necessary check before (5.2).**  `lambda_c` is not `Delta`-invariant (5.1 shows
active conjugates), so it does not decide (5.2).  But any functional of `Y-bar_3^{H1}` that is
invariant under the `Q_0`-twisted-diagonal action and kills the 31 coarse-visible columns while
not killing `pi(T)` would be an exact A0 NONMEMBER certificate; the `Delta`-invariant part of the
dual space is `Hom_{Delta}(M, k)` of dimension `2 - h^1(Delta;F_3) + h^2(Delta;F_3)`, i.e. the
two `N` keys plus the 3-part of the Schur multiplier.  Since `T` has `N = 0` and the `N`
functionals are already in play, the only invariant candidates are the Schur-multiplier
directions; I have not computed `H_2(Delta; F_3)` (a 3.6e8-element permutation group; possible
in GAP with more time).  Flagged as **【UNKNOWN】**, not used.

---

## 6. Consequences for the running lane (no intervention; statements only)

1. The observed 100 consecutive seed-1 rises are **not** evidence of a cyclic module or ideal
   statement.  They are the joint effect of (a) the selector rule "seed 1 first, restart at seed 1
   after every hit" (v433 Theorem 2.1 step 6) and (b) the greedy min-key dual of
   `PackedEchelon.dual`, which keeps pairing with the pc3-layer.  Seeds `>= 3` are examined only
   after `F_1 == 0` for the current dual; nothing bounds that except
   `dim C_1 <= 119,042,784` (2.1).  Every future seed-1 rise lies in `ker(kappa_*)^{H1} (+)
   ker(kappa_*)^{H2} (+) Z-bar_P (+) k e_N1` and leaves the coarse H1 remainder untouched.
2. The lane can be un-blinded without new mathematics (Sol's implementation call, per the
   "Sol demands, Sol implements" rule): either feed `lambda_phys` (324 tau-free keys, §4) as the
   separating dual of the current span — it is valid for rank 143 and has `F_1 == F_2 == 0` —
   or try coarse-visible seeds first, or run the coarse floor (5.2) first.  Any of these makes
   the next accepted row a coarse-visible one; none of them is a rank-rise guarantee.
3. Nothing here is a negative A0 terminal.  `T` may still lie in `V0 + D + sum_{i>=3} C_i`.

---

## 7. What is proved, what is assumed, what is not claimed

- **Proved on paper** (given P1–P7): Corollary 1.1, Theorem A (a)–(c), Theorem B, Theorem C
  modulo the machine fact `lambda_c(pi(T)) = 1, lambda_c(coarse V0) = 0`.
- **Machine-checked, cross-checked against the frozen data but not against the frozen owner's
  stored rows** (【GAP-1】): my Fox/coarse implementation.  Self-checks passed: PB3 boundary
  translates vanish (88 cases); all 44 relators and all five `s_i` trivial in `Q0` under all five
  substitutions; `hex_1(g760), hex_2(g760)` trivial in `Q0`; 14 sample conjugators (seed 1) and
  300 random conjugators of length `<= 40` (seeds 1 and 2) all coarse-blind; joint-group order and
  all ten kernel orders equal task176.  Sol can close 【GAP-1】
  byte-exactly by evaluating `lambda_phys` on the 44 stored identity columns (expect 0) and on the
  stored target (expect 1) inside the live owner.
- **【GAP-P5】**: `V0` = identity columns + block-3 action rows is read from `prefix()` source, not
  from the rank143 checkpoint.  If the checkpoint's initial 43 rows contain anything with a
  nonzero coarse H1/H2 component other than identity columns, Theorem C's `V0` step must be
  re-run with those rows (the script accepts extra rows).  Sol reply 530 ("unit chain 43->…",
  all 100 records seed 1) is consistent with the source reading.
- **Not claimed**: A0 MEMBER; A0 NONMEMBER; membership in the coarse floor (5.2); anything about
  seeds 3–43 beyond §5.1; any COMMON word, compatible lift, fake, or Ihara witness.
  `verified=false` throughout.
- **【文献要請】 none.**  All arguments are elementary (Fox calculus, five-term sequence,
  Lyndon identity theorem only in a remark).

---

## 8. Artifacts (all under `scratchpad/`, sha16 = first 16 hex of SHA-256)

```text
a0_paper_words_v1.py            877a11b46557f101   frozen compact() + g760 extraction
a0_paper_words_v1.json          90ba603368307e16   44 relators, s_1..s_5, g760
a0_paper_words_v1.g             6778b463ac5296f5   same, GAP transcription
a0_paper_delta_v1.g             c1dbce0e290a5fb9   joint group, kernels, coarse kernels, closures
a0_paper_delta_v1_output.txt    e68b3a2f048183db
a0_paper_delta_v2.g             b30107b104791c2d   centrality, pi(gamma_1) vs z3, Delta/<gamma_1>
a0_paper_delta_v2_output.txt    878b455da853b0ca
a0_paper_coarse_v1.py           2f4fb3614c79e678   coarse floor of V0: separating functional
a0_paper_coarse_v1_output.txt   da9f9f5f0a40724b
a0_paper_coarse_v2.py           d2844ed315b6e770   v1 + dual export, 300-conjugator stress, seed reach
a0_paper_coarse_v2_output.txt   56cf2593e0e4f8ae
a0_paper_coarse_dual_v1.json    470fd52cf6849fa0   the 12-key lambda_c (Q0 one-line perms, 1-based)
fuda1_a0_rmax_data.g            625b4d11ca882c94   q3_chief transcription (input, unchanged)
```

Run commands: `python scratchpad/a0_paper_words_v1.py`; `.\gap.ps1 scratchpad\a0_paper_delta_v1.g`
(about 2 minutes, `-o 2g`); `python scratchpad/a0_paper_coarse_v2.py` (about 3 minutes).

### Appendix — the 12 keys of `lambda_c` (block 1, coordinate `b`; machine printout)

Each line: `block label coef  [Q0 element, one-line, 1-based, GAP product convention a*b = a then b]`.

```text
1 b 1 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
1 b 2 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 19, 20, 21, 22, 31, 32, 33, 34, 35, 36, 28, 29, 30]
1 b 2 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 17, 16, 15, 14, 13, 12, 11, 20, 19, 27, 26, 25, 24, 23, 22, 21, 29, 30, 31, 32, 33, 34, 35, 36, 28]
1 b 1 [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 18, 17, 16, 15, 14, 13, 12, 20, 21, 22, 23, 24, 25, 26, 27, 19, 36, 35, 34, 33, 32, 31, 30, 29, 28]
1 b 1 [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 16, 15, 14, 13, 12, 11, 10, 18, 27, 26, 25, 24, 23, 22, 21, 20, 19, 36, 28, 29, 30, 31, 32, 33, 34, 35]
1 b 2 [1, 2, 4, 7, 9, 8, 5, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 19, 20, 21, 22, 31, 32, 33, 34, 35, 36, 28, 29, 30]
1 b 1 [1, 2, 4, 7, 9, 8, 5, 3, 6, 14, 13, 12, 11, 10, 18, 17, 16, 15, 20, 19, 27, 26, 25, 24, 23, 22, 21, 29, 30, 31, 32, 33, 34, 35, 36, 28]
1 b 1 [1, 2, 5, 9, 8, 4, 6, 7, 3, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 19, 20, 31, 32, 33, 34, 35, 36, 28, 29, 30]
1 b 2 [1, 2, 5, 9, 8, 4, 6, 7, 3, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 19, 20, 32, 33, 34, 35, 36, 28, 29, 30, 31]
1 b 1 [1, 2, 5, 9, 8, 4, 6, 7, 3, 10, 18, 17, 16, 15, 14, 13, 12, 11, 20, 19, 27, 26, 25, 24, 23, 22, 21, 29, 30, 31, 32, 33, 34, 35, 36, 28]
1 b 2 [1, 2, 5, 9, 8, 4, 6, 7, 3, 13, 12, 11, 10, 18, 17, 16, 15, 14, 24, 25, 26, 27, 19, 20, 21, 22, 23, 31, 30, 29, 28, 36, 35, 34, 33, 32]
1 b 1 [1, 2, 6, 8, 4, 5, 3, 9, 7, 12, 11, 10, 18, 17, 16, 15, 14, 13, 25, 24, 23, 22, 21, 20, 19, 27, 26, 32, 33, 34, 35, 36, 28, 29, 30, 31]
```

(`Q0` marked generators: `a12 -> q01`, `a23 -> q02`, `a13 -> (q02*q01)^-1`, from
`coarse_models.Q0.marked_permutations` of the q3_chief receipt; the first key is the identity.)

```text
SEED-1 CYCLIC MODULE = FULL 44-SEED MODULE:      FALSE (codim >= 238,085,569, paper)
SEED-1 PHYSICAL ORBIT IN pc3-LAYER (H1,H2) + eN1: PAPER PROOF (Theorem B)
T IN V0 + SEED-1 SPAN + D:                        FALSE (Theorem C, 12-key separating functional)
SEED-1-BLIND TAU-FREE DUAL FOR RANK-143 SPAN:     SUPPLIED (324 keys, paper properties)
COARSE FLOOR (dim <= 1,469,665):                  DEFINED, NOT EXECUTED
ACTUAL A0 MEMBER/NONMEMBER:                       NOT DECIDED
COMPATIBLE LIFT / FAKE / IHARA:                   NONE
verified:                                         false
```

`R07_A0_SEED1_LANE_PAPER_OBSTRUCTION_FABLE_V1`
