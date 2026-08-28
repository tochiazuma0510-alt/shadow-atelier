# R07 Neumann endpoint-only group-like gate v250

Author: Sol / 2026-08-28

Status: paper corollary of v249.  It removes finite-level Fox inversion from
the actual word-integrability computation.  The decisive object is one sparse
group-algebra endpoint, obtained by a finite conjugation recursion in each
finite 3-group quotient.  The actual task192 word and A6 multiplier have not
yet been accepted or tested.  No compatible lift, fake certificate, or Ihara
witness is declared.  verified=false.

## 1. The endpoint operator

Retain v249's free pro-3 roof kernel \(\mathcal P\), completed group algebra

\[
 \mathcal R=\mathbf F_3[[\mathcal P]],
 \qquad I=\ker\varepsilon,
\tag{1.1}
\]

completed Fox chain module \(\mathcal C_1\), and isomorphism

\[
 \partial:\mathcal C_1\xrightarrow{\sim}I.
\tag{1.2}
\]

For a source conjugator \(W\), write \(\sigma_W=\operatorname{Ad}_W\) on
\(\mathcal R\) and

\[
 T_W=\partial^{-1}\sigma_W\partial
\tag{1.3}
\]

on \(\mathcal C_1\).  Let the accepted A6 polynomial be

\[
 M=\sum_i b_i(U_i-V_i),
 \qquad \pi(U_i)=\pi(V_i),
\tag{1.4}
\]

and define the two matching operators

\[
 \mathcal M=\sum_i b_i(T_{U_i}-T_{V_i})
 \quad\hbox{on }\mathcal C_1,
\tag{1.5}
\]

\[
 \overline{\mathcal M}
   =\sum_i b_i(\sigma_{U_i}-\sigma_{V_i})
 \quad\hbox{on }\mathcal R.
\tag{1.6}
\]

### Lemma 1.1 (FOX ENDPOINT INTERTWINING)

\[
 \boxed{\partial\mathcal M
       =\overline{\mathcal M}\partial.}
\tag{1.7}
\]

#### Proof

Equation (1.3) gives
\(\partial T_W=\sigma_W\partial\) for every retained source word.  Multiply
by \(b_i\), take each difference, and sum. \(\square\)

This identity is basis-independent.  A finite implementation may replay one
Fox-chain naturality canary, but it need not invert a finite quotient endpoint.

## 2. Closed endpoint recursion

Let \(a_{\rm w}\in\mathcal P\) be the task192 word and
\(\alpha=\delta(a_{\rm w})\).  Put

\[
 z_0=a_{\rm w}-1,\qquad
 z_{r+1}=\overline{\mathcal M}z_r.
\tag{2.1}
\]

V249's Neumann Fox chain is

\[
 Q_\infty=-\sum_{r\ge0}\mathcal M^r\alpha.
\tag{2.2}
\]

### Theorem 2.1 (ENDPOINT-ONLY NEUMANN FORMULA)

The endpoint and word candidate are

\[
 \boxed{\partial Q_\infty=-\sum_{r\ge0}z_r,}
\tag{2.3}
\]

\[
 \boxed{u_\infty
       =1+\partial Q_\infty
       =1-\sum_{r\ge0}z_r.}
\tag{2.4}
\]

Moreover \(Q_\infty\) is the Fox chain of one pro-3 word if and only if
\(u_\infty\) is group-like.  On a pass the word is \(c_\infty=u_\infty\).

#### Proof

The Fox fundamental formula gives
\(\partial\alpha=a_{\rm w}-1=z_0\).  Lemma 1.1 gives inductively

\[
 \partial\mathcal M^r\alpha
 =\overline{\mathcal M}^{\,r}z_0=z_r.
\tag{2.5}
\]

Continuity permits termwise passage to the convergent series, proving
(2.3)--(2.4).  V249 Theorem 3.1 gives the final equivalence and the displayed
word. \(\square\)

Thus production does not need a finite Schreier basis, a finite inverse of
\(\partial\), or a chosen finite Fox section.  Those objects are useful
ancestry checks but are not part of the decisive support calculation.

## 3. Exact finite-rung algorithm

Let \(Q\) be a finite 3-group quotient of \(\mathcal P\), stable under all
retained conjugation actions.  Write
\(\bar\sigma_W\in\operatorname{Aut}(Q)\) for the induced action.  It may be
encoded either as a complete permutation of \(Q\) or by a finite ambient
context group \(E\) in which \(Q\triangleleft E\) and the retained \(W\)'s
have values.  Compute in \(\mathbf F_3[Q]\):

\[
 z_{0,Q}=\bar a_{\rm w}-1,
\tag{3.1}
\]

\[
 z_{r+1,Q}
 =\sum_i b_i
   \bigl(\bar\sigma_{U_i}(z_{r,Q})
        -\bar\sigma_{V_i}(z_{r,Q})\bigr).
\tag{3.2}
\]

In an ambient realization, (3.2) is ordinary conjugation by the values of
\(U_i,V_i\).  Because \(U_iV_i^{-1}\in\mathcal P\), the two automorphisms
differ by the inner action of an element of \(Q\).  Therefore
the proof of v249 Lemma 4.1 gives

\[
 z_{r,Q}\in J_Q^{r+1},
\tag{3.3}
\]

where \(J_Q\) is its augmentation ideal.  Since \(J_Q\) is nilpotent, there
is an exact first \(N_Q\) with \(z_{N_Q,Q}=0\).  Hence

\[
 \boxed{u_Q=1-\sum_{r=0}^{N_Q-1}z_{r,Q}}
\tag{3.4}
\]

is a finite sparse calculation.

### Corollary 3.1 (FINITE SUPPORT CERTIFICATE)

1. If the collected support of \(u_Q\) is not one quotient element with
   coefficient one, then the named pair \((a_{\rm w},M)\) is not integrable
   to one completed pro-3 word.
2. If its support is one coefficient-one element, the named candidate passes
   this quotient only.
3. If a cofinal system of stable quotients passes and the singleton elements
   commute with all reduction maps, then \(u_\infty\) is group-like and
   gives the unique word \(c_\infty\).

#### Proof

Equation (3.4) is the reduction of (2.4).  A group-like element of a finite
group algebra is exactly one coefficient-one group basis element by v249
Lemma 2.1, proving items 1 and 2.  In item 3 the compatible singleton
elements define an element of \(\mathcal P\); equality with every reduction
of \(u_\infty\) and separatedness prove that \(u_\infty\) is that group
element. \(\square\)

A finite list, however long, is not cofinal unless its constructor and
reduction maps are authenticated.  Such a list may report only registered-
family success, never all-rung success.

## 4. Certificate contract

At every registered rung retain:

1. the full finite group roster, multiplication, inverse, and identity,
   together with every retained action automorphism (or the ambient context
   group which induces it);
2. task192 and every A6 source word with its quotient, action, and roof
   evaluations;
3. every full sparse \(z_{r,Q}\), including the first exact zero;
4. the collected support and counit of \(u_Q\);
5. on failure, the first preregistered rung and complete nonsingleton support;
6. on pass, the singleton basis element; and
7. for adjacent rungs, the literal reduction of the finer singleton and all
   input words to the coarser data.

The independent checker reconstructs (3.1)--(3.4) from the finite group
table.  A receipt Boolean, a support hash, or a manifest-supplied name for
the reduced element is not a replay.

## 5. Fixed frontier

    FOX CHAIN NEUMANN ENDPOINT = FINITE CONJUGATION RECURSION: PAPER PROOF
    FINITE FOX ENDPOINT INVERSION IN PRODUCTION:                REMOVED
    NONSINGLETON FINITE SUPPORT REJECTS NAMED CANDIDATE:        PAPER PROOF
    COFINAL COMPATIBLE SINGLETONS CONSTRUCT THE WORD:           PAPER PROOF
    ACTUAL TASK192/A6 ENDPOINT RECURSION:                       NOT COMPUTED
    EXACT H1/H2/P FOR THE RESULTING WORD:                       OPEN
    MIXED-PRIME / PERFECT-CORE / FAKE / IHARA:                  OPEN

R07_NEUMANN_ENDPOINT_ONLY_GROUP_LIKE_GATE_V250_PAPER_GRADE
