# R07 full translated-boundary dual decision v163

Author: Sol / 2026-08-27

Status: paper theorem and task187 algorithm certificate.  No task187
production result has yet been computed.  No common word, compatible cofinal
lift, fake, or Ihara witness is declared.

## 1. Typed translated boundary family

For each typed block (b\in\{H1,H2,P\}), let (Q_b) be the fixed finite
quotient used by the first-rung Fox module.  A base PB3/PB4 boundary row has
the form

\[
 d_{b,j}=\sum_{k=1}^{m_{b,j}}
             \alpha_k[c_k,h_k],
 \qquad
 \alpha_k\in{\bf F}_3, h_k\in Q_b,
 \tag{1.1}
\]

where the component tag (c_k), block tag (b), and group value (h_k)
are all retained.  Its left translate by (t\in Q_b) is

\[
 t d_{b,j}=\sum_k\alpha_k[c_k,t h_k].
 \tag{1.2}
\]

Let

\[
 D=\operatorname{span}_{\bf F_3}
       \{t d_{b,j}:b,j,t\}
 \tag{1.3}
\]

be the complete translated-boundary space.  Equal underlying group bytes in
different blocks or components remain different coordinates.

## 2. Support-inversion formula

Let (lambda) be a finitely supported dual row.  Write

\[
 \lambda_{b,c}(g)=
 \lambda([b,c,g]).
\]

Directly from (1.2),

\[
 \langle\lambda,t d_{b,j}\rangle
 =\sum_k\alpha_k\lambda_{b,c_k}(t h_k).
 \tag{2.1}
\]

For fixed (h_k), every nonzero summand in (2.1) has

\[
 g=t h_k\in\operatorname{supp}\lambda_{b,c_k},
 \qquad
 \boxed{t=g h_k^{-1}}.
 \tag{2.2}
\]

Thus all pairings with all translations can be computed without iterating
over (Q_b): for every base occurrence ((c_k,h_k,\alpha_k)) and every
dual-support value ((g,\lambda_{b,c_k}(g))), compute the single translation
(t=g h_k^{-1}) and add

\[
 \alpha_k\lambda_{b,c_k}(g)
 \tag{2.3}
\]

to the accumulator keyed by ((b,j,t)).

### Proposition 2.1 (complete correlation identity)

Let (S_{b,j,t}) be the accumulator produced by (2.2)--(2.3), after all
base occurrences and all matching dual-support entries have been processed.
Then

\[
 \boxed{
 S_{b,j,t}=\langle\lambda,t d_{b,j}\rangle}
 \tag{2.4}
\]

for every block, base boundary, and translation.

#### Proof

Fix ((b,j,t)).  Each summand on the right of (2.1) is nonzero only if
(g=t h_k) occurs in the matching support list.  The support-inversion loop
then processes that exact pair ((h_k,g)), reconstructs
(g h_k^{-1}=t), and contributes precisely (2.3) to (S_{b,j,t}).
Conversely every contribution accumulated at key ((b,j,t)) came from a
matching support value (g) and a base occurrence (h_k) satisfying
(g h_k^{-1}=t), hence (g=t h_k); it is exactly a summand of (2.1).
Multiplicity is preserved because the loop retains every base occurrence
before summing modulo three.  Therefore the two sums agree.  \(\square\)

The equality (t h_k=g) must be replayed directly in the finite quotient.
Changing left translation to right translation, or using (h_k^{-1}g),
invalidates (2.4).

## 3. Exact membership decision

Let (W\subseteq D) be the span of the boundary columns retained so far and
let (z\in V) be one target.  If (z\notin W), exact elimination constructs
a dual row (lambda) with

\[
 \lambda(W)=0,
 \qquad
 \lambda(z)\ne0.
 \tag{3.1}
\]

### Theorem 3.1 (FULL-BOUNDARY DUAL DICHOTOMY)

With the complete accumulator of Proposition 2.1, exactly one of the
following occurs.

1. Some (S_{b,j,t}\ne0).  Then (t d_{b,j}\notin W), so retaining this
   literal column strictly raises rank.
2. Every (S_{b,j,t}=0).  Then (lambda(D)=0), while
   (lambda(z)\ne0); hence
   \[
   \boxed{z\notin D}.
   \tag{3.2}
   \]

#### Proof

In the first case (2.4) gives a nonzero pairing with (lambda).  Since
(lambda) annihilates (W), the active column cannot lie in (W).

In the second case (2.4) says (lambda) annihilates every generator in
(1.3), hence all of (D).  Equation (3.1) separates (z) from (D), proving
(3.2).  \(\square\)

### Corollary 3.2 (finite termination)

Repeatedly adding an active translated boundary decides membership of (z)
in (D) after finitely many rank increases.

#### Proof

Each active column strictly increases (dim W), while the ambient typed Fox
space is finite-dimensional.  If (z) enters (W), coefficient ancestry
gives a positive boundary chain.  Otherwise a later dual has no active
translated boundary, and Theorem 3.1 gives the negative certificate.  \(\square\)

Two or more targets may share the same retained space.  After every rank
increase, all target remainders are recomputed; each eventual positive chain
is recovered in the common original-column order.

## 4. Why this negative result is allowed

The task179 correction oracle visits a much larger word-bearing family by a
bounded fair schedule.  A miss before that schedule is exhausted is UNKNOWN,
not nonmembership.

The boundary oracle here is different.  Proposition 2.1 evaluates the dual
pairing with **every** translated PB3/PB4 boundary column through the exact
support-inversion identity.  Therefore an empty complete accumulator is a
genuine dual separator for the full family, provided:

1. all dual support entries were processed;
2. all two PB3 and eleven PB4 base rows were processed in their typed blocks;
3. equal-key contributions were summed modulo three before deciding ACTIVE;
4. every quotient multiplication/inverse and (t h=g) equality was replayed;
5. no resource cap interrupted the correlation; and
6. the independent checker reconstructs the same complete accumulator.

A resource interruption before these gates is `UNKNOWN_RESOURCE`, never
`NONMEMBER_D`.

## 5. Complexity consequence

The correlation work is proportional to

\[
 \sum_{b,j}\sum_{(c,h)\in\operatorname{supp}d_{b,j}}
       |\operatorname{supp}\lambda_{b,c}|,
 \tag{5.1}
\]

not to the number of all triples ((b,j,t)).  This is the mathematical
reason task187 can test the two `u0/v0` boundary preimages much more cheaply
than a new all-correction column-generation run, while retaining an exact
negative certificate.

```text
SUPPORT-INVERSION CORRELATION:               PAPER_PROOF
EMPTY COMPLETE CORRELATION => NONMEMBER_D:   PAPER_PROOF
ACTIVE CORRELATION => STRICT RANK RISE:      PAPER_PROOF
FINITE BOUNDARY MEMBERSHIP DECISION:         PAPER_PROOF
TASK187 U0/V0 OUTCOME:                       NOT YET COMPUTED
RAW COMMON WORD / COFINAL / FAKE / IHARA:    NOT DECLARED
```

`R07_FULL_TRANSLATED_BOUNDARY_DUAL_DECISION_V163`
