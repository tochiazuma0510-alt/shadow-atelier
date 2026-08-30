# R07 compact-extension presentation and A0 seed reduction v397

Author: Sol / 2026-08-30

Status: paper theorem.  This note replaces the 6,441 Cayley-edge presentation
as an A0 input *in principle* by a Tietze-equivalent presentation with at most
44 literal relators.  The compact literal roster and its independent replay
are not yet materialized, so A0 remains `0/1 UNKNOWN_RESOURCE`; no COMMON,
lift, fake, or Ihara witness is declared.

The frozen finite data used below are the task157ee joint-extension receipt

```text
ci/b345_157ee_artifacts_32359956713/
  d972_b345_joint_kernel_qstar_closure_v1.json
sha256 = 1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df
```

and the accepted task198 roof bridge recorded in v258.  Direct receipt
readback gives

\[
 |\Gamma|=243=3^5,\qquad |Q_0|=1{,}469{,}664,
 \qquad m_{Q_0}=19.                                      \tag{0.1}
\]

The receipt also gives

\[
 |\Phi(\Gamma)|=27,\qquad
 \dim_{\mathbf F_3}\Gamma/\Phi(\Gamma)=2,               \tag{0.2}
\]

and authenticates 26 source correction records whose images generate
\(\Gamma\), together with the complete \(x,y\)-action and the 19 lifted
\(Q_0\) defects.  Equation (0.2) is useful redundancy information, but the
proof below uses only the safer order bound \(|\Gamma|=3^5\).

## 1. Compact finite-extension presentation

Let

\[
 1\longrightarrow \Gamma\longrightarrow G
 \xrightarrow{\pi}Q\longrightarrow1                 \tag{1.1}
\]

be an exact finite extension, and let

\[
 \rho:F(X)\twoheadrightarrow G,
 \qquad \bar\rho=\pi\rho:F(X)\twoheadrightarrow Q.  \tag{1.2}
\]

Choose a polycyclic generating sequence

\[
 \boldsymbol\gamma=(\gamma_1,\ldots,\gamma_d)          \tag{1.3}
\]

for \(\Gamma\), a consistent power--conjugate presentation

\[
 \Gamma\cong\langle k_1,\ldots,k_d\mid S\rangle,       \tag{1.4}
\]

and source words \(s_i\in\ker\bar\rho\) with
\(\rho(s_i)=\gamma_i\).  For a word \(v(\boldsymbol\gamma)\) in
\(\Gamma\), write \(\widehat v(\boldsymbol k)\) for its collected word in
the abstract generators \(k_i\).

Let

\[
 Q\cong\langle X\mid q_1,\ldots,q_m\rangle             \tag{1.5}
\]

be a complete marked presentation.  Record, in collected \(k\)-words,

\[
 \begin{aligned}
  \rho(u)^{-1}\gamma_i\rho(u)&=\alpha_{u,i}(\boldsymbol\gamma),
       &&u\in X,\ 1\le i\le d,\\
  \rho(q_j)&=\delta_j(\boldsymbol\gamma),
       &&1\le j\le m.
 \end{aligned}                                           \tag{1.6}
\]

Define the auxiliary presentation

\[
 \begin{split}
 P=\langle X,k_1,\ldots,k_d\mid {}&S(\boldsymbol k),\\
 &u^{-1}k_i u=\widehat\alpha_{u,i}(\boldsymbol k),\\
 &q_j=\widehat\delta_j(\boldsymbol k),\\
 &k_i=s_i(X)\rangle .
 \end{split}                                               \tag{1.7}
\]

### Theorem 1.1 (COMPACT EXTENSION PRESENTATION)

The natural marked map \(P\to G\) is an isomorphism.  After eliminating all
\(k_i\) by the defining equations \(k_i=s_i(X)\), the following literal
words normally generate \(\ker\rho\) in \(F(X)\):

1. every internal pc relation \(S(\boldsymbol s)\);
2. for each \(u\in X\) and \(i\),
   \(u^{-1}s_i u\,\widehat\alpha_{u,i}(\boldsymbol s)^{-1}\);
3. for each \(j\),
   \(q_j\widehat\delta_j(\boldsymbol s)^{-1}\).

#### Proof

All relations (1.7) hold after sending \(X\) to its marked images in \(G\)
and \(k_i\) to \(\gamma_i\).  Hence there is a marked surjection

\[
 P\twoheadrightarrow G.                                  \tag{1.8}
\]

Let \(C=\langle k_1,\ldots,k_d\rangle\le P\).  The relations
\(S(\boldsymbol k)\) give a surjection \(\Gamma\twoheadrightarrow C\), so

\[
 |C|\le |\Gamma|.                                         \tag{1.9}
\]

The action relations send \(C\) into itself under conjugation by each
\(u\in X\).  Since \(C\) is finite, each such injective conjugation is a
bijection on \(C\); its inverse therefore also preserves \(C\).  Thus
\(C\triangleleft P\).  Modulo \(C\), the adjusted relations in the third
line of (1.7) become \(q_j=1\), whence completeness of (1.5) gives

\[
 |P/C|\le |Q|.                                             \tag{1.10}
\]

Consequently

\[
 |P|\le |\Gamma||Q|=|G|.                                  \tag{1.11}
\]

The surjection (1.8) gives the reverse inequality, so (1.8) is an
isomorphism.  The last line of (1.7) consists of Tietze definitions; eliminate
the \(k_i\) to obtain precisely the three source-word families stated above.
Their normal closure is therefore \(\ker\rho\). \(\square\)

This is the same order argument as v190, but replaces the complete Cayley
table on every \(\Gamma\)-state by one exact pc presentation of \(\Gamma\).
No splitting of (1.1) is assumed: the words \(\delta_j\) retain the extension
cocycle.

## 2. Uniform relator-count bound for the frozen roof

A finite group of order \(3^5\) admits a composition-refining polycyclic
sequence of length

\[
 d=5                                                       \tag{2.1}
\]

with every relative order equal to three.  A consistent power--conjugate
presentation on that sequence needs at most one power relation for each
generator and one conjugation relation for each ordered pc pair.  Thus

\[
 |S|\le d+\binom d2=5+10=15.                              \tag{2.2}
\]

For the marked set \(X=\{x,y\}\), Theorem 1.1 requires only one conjugation
orientation per marked generator; finiteness of \(C\) supplies the inverse
orientation.  Therefore the pure \(F(x,y)\) roster has size at most

\[
 \boxed{|S|+2d+19\le 15+10+19=44.}                       \tag{2.3}
\]

Every pc generator has a literal source representative: the 26 authenticated
task157ee correction records generate all of \(\Gamma\), so each chosen
\(\gamma_i\) is a product of their images and the same product of the source
records is an \(s_i\in\ker\bar\rho\).  The multiplication table collects all
internal, action, and \(Q_0\)-defect right sides in (1.6).  Hence (2.3) is an
effective reduction, not merely an abstract existence statement.

The receipt's Frattini dimension two says that a smaller two-generator
\(\Gamma\) presentation may exist, but no relation-count advantage from it is
used here.  The five-step pc route is chosen because its order proof and
collection certificate are canonical and bounded.

### Corollary 2.1 (SAME ROOF KERNEL, AT MOST 44 SEEDS)

Let \(\Theta:F(x,y)\twoheadrightarrow\Delta_7\) be the accepted task198/v189
marked roof map, and let \(\mathcal R_{\rm pc}\) be the source roster obtained
from (2.3).  Then

\[
 \boxed{
  \langle\!\langle\mathcal R_{\rm pc}\rangle\!\rangle_F
  =\ker\Theta
  =\langle\!\langle\mathcal R_{6441}\rangle\!\rangle_F,
  \qquad |\mathcal R_{\rm pc}|\le44.}                    \tag{2.4}
\]

#### Proof

Apply Theorem 1.1 to the exact task157ee extension, then transport across the
task176 equal-order bridge and the v189 marked isomorphism exactly as in v190
Sections 2--3.  Both rosters present the same marked group \(\Delta_7\), so
both normal closures equal \(\ker\Theta\). \(\square\)

## 3. Consequence for A0

Let \(J\), \(\rho\), \(W\), and the physical aggregation \(L_g\) be the
occurrence-level objects of v396.  Corollary 2.1 permits the definition

\[
 W=\operatorname{span}_{\mathbf F_3}
 \{\rho(a)J(r):r\in\mathcal R_{\rm pc},\ a\in F(x,y)\}.  \tag{3.1}
\]

The proof of v396 Theorem 2.1 is unchanged, because it depends only on the
normal closure of the seed roster.  If \(r=\dim W\), exact invariant closure
therefore needs at most

\[
 \boxed{44+4r}                                             \tag{3.2}
\]

row-insertion attempts, rather than \(6{,}441+4r\), and still returns a
word-bearing ancestry DAG.  The complete typed boundary remains the separate
15-seed invariant closure of v396.

Thus the A0 decision remains the finite exact membership test

\[
 -T\in D+L_g(W),                                           \tag{3.3}
\]

but its registered input is now:

```text
roof correction seeds:  <= 44 literal pc/Tietze relators
roof actions:            x, x^-1, y, y^-1 on retained rows only
typed boundary seeds:    15
global conjugator list:  none
Q0 section enumeration:  none
6441 Cayley edges:        independent equivalence oracle only
```

## 4. Speed and memory contract

The mathematics now supports speed and memory control simultaneously.

1. A single owner stores only sparse echelon pivots and compact ancestry/action
   DAG nodes.
2. Workers receive immutable batches of newly retained sparse rows and apply
   the four occurrence-dependent actions.  They never inherit the owner's
   reducer, the 1.66 GB adaptive checkpoint, or historical dual columns.
3. Returned rows are reduced once by the owner.  Only rank-raising rows enter
   the next frontier, so parallel work is bounded by the true correction rank,
   not by a conjugator-radius universe.
4. The 6,441-roster remains a streaming equality oracle: replaying every old
   seed into the final compact invariant span checks
   \(J(\mathcal R_{6441})\subseteq W\), while replaying the at-most-44 compact
   relators in the accepted roof checks the easy reverse soundness.  Neither
   replay needs to retain all rows in memory.

The old run 33285081587 checkpoint is therefore only a durable fallback.  Its
8,727 retained columns and 22,912,880 boundary pairs are not loaded by the
compact owner, avoiding the measured 14,534,844,416-byte parent-plus-children
RSS terminal which killed the two-worker batch path.

## 5. Exact remaining mechanical gate

The paper reduction is complete; the following finite materialization is
still required before production:

1. extract a five-step pc sequence from the authenticated 243-state table;
2. emit its at-most-15 consistent power/conjugation relations;
3. express the two marked actions and 19 \(Q_0\) defects in pc normal form;
4. replace each pc generator by its literal task157ee source word;
5. independently replay (2.4), then run the v396 sparse invariant owner.

No search over pc presentations is needed: a deterministic composition series
and first admissible source representatives suffice.

```text
6441 -> <=44 NORMAL-CLOSURE REDUCTION: PAPER PROOF
OCCURRENCE-LEVEL A0 INSERTION BOUND:    <=44 + 4r
BOUNDARY INSERTION BOUND:               15 + 6(b1+b2) + 12b3 (v396)
COMPACT LITERAL ROSTER:                 NOT YET MATERIALIZED
MEMORY-SAFE PARALLEL OWNER:             SPECIFIED, NOT IMPLEMENTED
A0 COMMON + INDEPENDENT ACCEPTANCE:     0/1 UNKNOWN_RESOURCE
```

`R07_COMPACT_EXTENSION_A0_SEED_REDUCTION_V397_PAPER_GRADE`
