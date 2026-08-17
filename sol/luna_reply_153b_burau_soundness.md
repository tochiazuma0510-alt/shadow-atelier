# Luna reply 153b — independent audit of the finite Burau fiber route

## Scope and verdict

I read `sol/luna_task_153_b5_burau_fiber.md` from start to finish, the requested §§12.2–12.8 of `sol/sol_reply_152_pushback.md`, `sol/luna_reply_152_b4_158_pentagon_semantics.md`, and the local paper `2607.05283v1.pdf`.  I rendered the paper pages containing Observation 2.1 (p.3), Theorem 2.3 (p.5), Proposition 6.4 (p.17), and Corollary 6.5/Theorem 6.6 (p.21).  No GAP run or A/B computation was performed.

The mathematical one-way implication in Question 1 is sound.  The end-to-end task contract is **SOUND_WITH_REPAIRS**, because the finite-image meaning of “identity”, the commutator-image lemma, the semantic roof/index-3 prerequisites, and the limits of the 2026 faithfulness theorem must be written as explicit gates.  These are repairs to the proof/ledger contract, not a refutation of the obstruction.

## 1. Finite-fiber implication

Put (G=F_2), and write

\[
 \psi_0:G\longrightarrow P,
 \qquad \psi_i=\beta_{q,a}\circ\varphi_i:G\longrightarrow L:=GL_4(\mathbf F_q)
 \quad(1\leq i\leq5).
\]

Then (E=(\psi_0,\psi_1,\ldots,\psi_5):G\twoheadrightarrow H) is surjective by the definition (H=\operatorname{im}E).  For every surjection of groups,

\[
 E(G')=[H,H]=H'.
\]

Indeed, inclusion in (H') is immediate, while each commutator
\([h_1,h_2]) has the form (E([g_1,g_2])) after choosing preimages (g_i), and products give all of (H').  Thus using ([H,H]), rather than an unproved equality with a profinite derived subgroup, is correct.

Every map to the finite group (H) extends continuously to \(\widehat G\).  The image of the closure of (G') (equivalently, the natural image of the profinite completion of (G')) is still (H').  No assertion that the abstract subgroup \(\widehat G'\) equals the closure of (G') is needed; the finite-image equality above is the only required fact.

Suppose an arithmetic row (r=(m,\bar f)) had a \(\widehat{GT}\) lift \((m,\widehat f)).  The GT commutator condition puts \(\widehat f\) in the closure of (G'), so

\[
 h=\widehat E(\widehat f)\in H',
 \qquad \pi(h)=\bar f.
\]

The five component maps also extend continuously.  With the task's ordering

\[
 (1,2,3,4,5)=(123,234,12{,}3{,}4,1{,}23{,}4,1{,}2{,}34),
\]

the finite raw defect is the well-defined function of the tuple (h)

\[
 D_{q,a}(h)=(h_5h_3)^{-1}h_2h_4h_1.
\]

For a common word (w) producing (h), this equals
\(\beta_{q,a}(D_{\mathrm{A.18}}(w))\), where

\[
 D_{\mathrm{A.18}}(w)=
 (\varphi_{1,2,34}(w)\varphi_{12,3,4}(w))^{-1}
 \varphi_{234}(w)\varphi_{1,23,4}(w)\varphi_{123}(w).
\]

The profinite pentagon identity (D_{\mathrm{A.18}}(\widehat f)=1) therefore forces (D_{q,a}(h)=I_4).  Consequently, if the *complete, nonempty* fiber

\[
 F_r=\{h\in H':\pi(h)=\bar f\}
\]

has no (h) with (D_{q,a}(h)=I_4), the row has no \(\widehat{GT}\) lift.  This proves the requested implication.

Important wording repair: a finite matrix identity is only a necessary image of the literal raw defect identity.  The producer must say “finite raw-A.18 image defect is (I_4)”; it must not claim that a finite specialization proves a nonidentity or identity in profinite (PB_4).  The direction used here is exactly the safe one:

\[
 D_{\mathrm{A.18}}=1\text{ in the profinite group}
 \Longrightarrow D_{q,a}=I_4.
\]

The five components do determine this finite defect: no sixth value occurs in the displayed product.  They must, however, be the five components of one common word.  Enumerating arbitrary independently chosen matrix tuples would lose provenance and is not a complete (E(G')) fiber.

The paper/GAP convention is a real implementation gate, not a change to the theorem.  Every paper product must be replayed through the explicit reverse-list `PaperProd` convention, including
`PaperProd([s2,s1^2,s2^-1])` for the Artin canary (x_{13}).  Reversing that conjugate or swapping the leading (\varphi_{1,2,34}) and (\varphi_{12,3,4}) factors changes the tested defect.  The required negative tests (reverse product, reverse (x_{13}), swap leading factors, delete a kernel element, corrupt a roof word/key) are therefore acceptance gates for the implementation and independent checker.

An empty projection fiber is not a terminal A witness in the ledger: it can indicate a broken roof/key binding.  The terminal record must require `fiber_size > 0` and `identity_defect_count = 0`.  Mathematically, an actually correct empty fiber would also contradict an arithmetic lift, but the task's fail-closed data contract is right to classify an empty/broken binding as UNKNOWN rather than A.

## 2. No extra B4-normal NFI window is needed for this A obstruction

Let

\[
 K_E=\ker E=\ker\psi_0\cap\bigcap_{i=1}^5\ker\psi_i.
\]

Each factor has finite image, so (K_E\triangleleft F_2) has finite index and (F_2/K_E\cong H).  The finite quotient of these defining equations is already sufficient for the contradiction in §1: every profinite solution maps to a solution in every finite quotient, while the complete finite fiber has no solution to the finite pentagon equation.

There is no logical requirement here that (K_E) be a B4-normal subgroup, belong to an NFI family, be isolated, or be cofinal among B4-normal refinements.  Taking a B4 normal core of the five F2 kernels would introduce an additional construction and a coface/B4-stability proof, but cannot strengthen this one-way finite obstruction.  The B4-normal/NFI/isolated and compatible-lift requirements belong to a global B (genuine-survival) argument.

This does not waive the existing semantic roof gates.  To call the resulting row a D972 row, one must still bind the first component to the actual fixed (P=PB_3/M), with (M=K^{(9)}\cap N_{S4}), and verify the 972-row roof dataset and its arithmetic/index-3 facts.  Those are properties of the fixed roof, not an NFI requirement on (K_E).

## 3. What the 2026 Burau theorem does and does not add

The paper's Observation 2.1 (p.3) gives kernel propagation under the standard inclusion (B_n\hookrightarrow B_{n+1}).  Moody's Theorem 2.3 (p.5) says that a change in the Moody polynomial under conjugation detects that a braid is not in the kernel.  Proposition 6.4 (p.17) supplies a push-map in (K_5) for a proper product, Corollary 6.5 (p.21) gives a Moody-polynomial inequality, and Theorem 6.6 (p.21) proves that the Burau representation is faithful on (Brun_4); together with the paper's reduction (Proposition 1.2), this yields faithfulness of the symbolic unreduced (\rho_4) on (B_4).

The separation of consequences is:

* **Finite-specialization A semidecision:** A single finite (eta_{q,a}) is merely a finite quotient.  The zero-fiber argument above needs only that it is a homomorphism.  A zero finite defect fiber is sound A evidence; an all-pass specialization is UNKNOWN.  Faithfulness of symbolic (\rho_4) is not needed for this direction.
* **Discrete Brunnian/discrete detection:** Symbolic faithfulness implies that a nontrivial discrete braid (in particular a nontrivial Brunnian braid, by Theorem 6.6) has a nonidentity Laurent-polynomial Burau matrix.  This is useful for discrete canaries and, after an additional elementary specialization argument, can support detection of a given discrete word somewhere in a family of finite fields.
* **Profinite detection:** Discrete faithfulness does **not** imply faithfulness of an induced map on \(\widehat{B_4}\), nor injectivity of the map to an inverse limit of the selected finite specializations.  A profinite element can lie in the intersection of the finite-specialization kernels unless a separate residual/cofinal theorem is proved.
* **B/cofinality:** To promote finite all-pass data to B, one would need a cofinal compatible family of relevant B4-normal finite quotients (or an equivalent profinite construction), with compatible nonempty solution fibers and all required hexagon, unit, onto, and charming conditions.  The Burau theorem supplies none of that.  In particular, no finite list of ((q,a)) values, and no all-pass result at one ((q,a)), is B evidence.

## 4. Index-3 terminal conclusion

The conclusion “one fake row makes all 648 outside rows fake” uses all of the following premises:

1. The fixed semantic roof is correct: (M=K^{(9)}\cap N_{S4}), the roof target (X) has 972 rows, and the row/reduction map used by (E) is the actual one.
2. The arithmetic image (A\subseteq X) has size 324, so there are (972-324=648) outside rows.
3. Every arithmetic row has a Galois/\(\widehat{GT}\) lift satisfying the literal A.18 pentagon, and the finite fiber scan is complete and nonempty when evaluated on such a lift.
4. The fixed D972 index-3 dichotomy is available: the \(\widehat{GT}\)-image is the arithmetic branch (A), or one genuine outside element forces the full outside branch (equivalently all 648 outside rows are genuine).  This is a stated structural dichotomy, not a conclusion from the number 3 alone; subgroup/normality and the arithmetic-image inclusion are part of the premise.
5. The zero-fiber row is a valid roof row (correct word/key binding, correct multiplication convention, and independent producer/checker agreement).

Under (1), (3), and (5), a nonempty zero finite-defect fiber contradicts arithmeticity, so the row is outside.  Under (2) and (4), the “all outside genuine” branch is impossible, leaving the arithmetic branch and hence all 648 outside rows fake.  Without the fixed dichotomy, the finite-fiber argument proves only the one row fake; it does not propagate to 648 rows.

## 5. Exact repairs and final status

The route should be accepted with these explicit repairs:

1. State and independently check the lemma (E(F_2')=[H,H]), and state that the profinite map is used only through its finite continuous extension.
2. Name the tested quantity (D_{q,a}(h)) and reserve “literal raw defect identity” for the group-level equation; finite identity is (D_{q,a}(h)=I_4).
3. Before scanning, independently verify the six unreduced Burau generator matrices are invertible and satisfy the braid relations; then require exact common-word provenance, complete (H')-fiber enumeration, nonempty fibers, and the frozen P/roof binding before any terminal label.
4. Replay all products with the paper convention and require the five listed negative tests, including the (x_{13}) canary and swapped leading factors.
5. Keep the semantic (M), 972/324/648, and fixed index-3 dichotomy as explicit terminal premises.  Do not infer them from Burau faithfulness or from the finite quotient.
6. Label all-pass, timeout, cap, or a finite-specialization family without a cofinal/compatible theorem as `UNKNOWN`; do not call it profinite faithfulness or B.

With these repairs, the finite Burau route is a sound A-semidecision and a cross-checkable one-way obstruction.  No partial computation in this audit is an A/B result.

**FINAL VERDICT: SOUND_WITH_REPAIRS**
