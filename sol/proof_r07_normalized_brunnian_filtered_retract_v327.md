# R07 normalized-Brunnian filtered retract (v327)

Author: Sol / 2026-08-29

Status: paper synthesis of v72 and v326.  Simplicial normalization already
projects onto all but one deletion kernel.  The full linear Brunnian target
is a filtered retract exactly after the remaining normalized differential
is split as a module map.  A prime-to-three symmetry quotient supplies such
a split by averaging.  The actual R07 formation intersection and
three-primary action are not identified with this semisimple case.  No
compatible lift, fake certificate or Ihara witness is declared.

## 1. Normalization leaves one differential

Let \(A_\bullet\) be a simplicial left \(\Lambda\)-module.  All face and
degeneracy maps are assumed \(\Lambda\)-linear and filtration-preserving.
At degree \(n\), retain v72's normalized module

\[
 N_n=\bigcap_{i=1}^n\ker d_i
\tag{1.1}
\]

and normalization idempotent

\[
 P_n=(1-s_0d_1)(1-s_1d_2)\cdots(1-s_{n-1}d_n),
\qquad
 P_n^2=P_n,\quad\operatorname{im}P_n=N_n,
\tag{1.2}
\]

with the composition order fixed as in v72.  The full linear Brunnian
submodule is

\[
 B_n=N_n\cap\ker d_0.
\tag{1.3}
\]

Put

\[
 \partial_n=d_0|_{N_n}:N_n\longrightarrow A_{n-1},
\qquad
 I_{n-1}=\operatorname{im}\partial_n.
\tag{1.4}
\]

Then there is an exact sequence

\[
 0\longrightarrow B_n\longrightarrow N_n
 \xrightarrow{\partial_n}I_{n-1}\longrightarrow0.
\tag{1.5}
\]

Thus normalization has already made \(N_n\) a \(\Lambda\)-linear retract
of \(A_n\).  The only remaining split question for full Brunnian support is
the exact sequence (1.5).

## 2. A split normalized differential gives the Brunnian projector

Assume there is a \(\Lambda\)-linear section

\[
 s:I_{n-1}\longrightarrow N_n,
\qquad
 \partial_ns=1_{I_{n-1}}.
\tag{2.1}
\]

Define on \(N_n\)

\[
 q_n=1-s\partial_n
\tag{2.2}
\]

and on \(A_n\)

\[
 \boxed{e_{\rm Br}=q_nP_n.}
\tag{2.3}
\]

### Theorem 2.1 (NORMALIZED BRUNNIAN RETRACT)

\[
 \boxed{
 e_{\rm Br}^2=e_{\rm Br},
 \qquad
 \operatorname{im}e_{\rm Br}=B_n.}
\tag{2.4}
\]

Consequently, for every two-sided ideal \(J\triangleleft\Lambda\),

\[
 \boxed{
 B_n\cap J^rA_n=J^rB_n
 \quad(r\geq0).}
\tag{2.5}
\]

#### Proof

On \(N_n\),

\[
 q_n^2
 =1-2s\partial_n+s\partial_ns\partial_n
 =1-s\partial_n=q_n,
\tag{2.6}
\]

and \(\partial_nq_n=0\), so
\(\operatorname{im}q_n\subseteq B_n\).  Conversely \(q_nz=z\) for
\(z\in B_n\), proving \(\operatorname{im}q_n=B_n\).

The map \(P_n\) lands in \(N_n\) and is the identity there.  Therefore
\(e_{\rm Br}\) lands in \(B_n\), is the identity on \(B_n\), and is an
idempotent.  This proves (2.4).  Equation (2.5) is v326 Theorem 1.1 applied
to the \(\Lambda\)-linear idempotent (2.3). \(\square\)

The section (2.1), not merely a vector-space section, is load-bearing for
the same-depth equality.

## 3. Prime-to-three averaging constructs the split

Let \(k=\mathbf F_3\) and suppose the relevant module action factors through
a finite group \(Q\) with \(3\nmid|Q|\), so

\[
 \Lambda=k[Q].
\tag{3.1}
\]

Choose any \(k\)-linear section

\[
 s_0:I_{n-1}\longrightarrow N_n
\tag{3.2}
\]

of \(\partial_n\), and define

\[
 \boxed{
 s_Q(y)=|Q|^{-1}\sum_{g\in Q}g^{-1}s_0(gy).}
\tag{3.3}
\]

### Theorem 3.1 (SEMISIMPLE BRUNNIAN SPLITTER)

The map \(s_Q\) is \(k[Q]\)-linear and

\[
 \partial_ns_Q=1_{I_{n-1}}.
\tag{3.4}
\]

Hence (2.3) with \(s=s_Q\) is an explicit \(k[Q]\)-linear Brunnian
idempotent.

#### Proof

The calculation is the Reynolds splitter of v112:

\[
 \partial_ns_Q(y)
 =|Q|^{-1}\sum_{g\in Q}g^{-1}\partial_ns_0(gy)
 =y.
\tag{3.5}
\]

Changing variables in the sum proves \(Q\)-equivariance. \(\square\)

This is a concrete all-target formula.  It does not apply when the actual
action ring contains a nonsemisimple three-primary radical and the desired
section must be linear over that larger ring.

## 4. The exact three-primary obstruction

For a general \(\Lambda\), the obstruction to (2.1) is precisely the
extension class of (1.5):

\[
 [N_n]\in
 \operatorname{Ext}^1_\Lambda(I_{n-1},B_n).
\tag{4.1}
\]

### Proposition 4.1 (BRUNNIAN SPLIT DICHOTOMY)

The following are equivalent:

1. the extension class (4.1) is zero;
2. \(\partial_n:N_n\to I_{n-1}\) has a \(\Lambda\)-linear section;
3. \(B_n\) is the image of the explicit-form idempotent
   \((1-s\partial_n)P_n\) for some \(\Lambda\)-linear \(s\).

#### Proof

The equivalence of 1 and 2 is the definition of splitting of (1.5).
Theorem 2.1 proves 2 implies 3.  If 3 holds with the displayed form, its
\(s\) is a section in (2.1), giving 2. \(\square\)

At a finite R07 layer this is decidable by module linear algebra or a
complete cocycle/extension certificate.  A failure to find a section in a
bounded roster is UNKNOWN; a nonzero Ext class with complete ancestry is a
genuine obstruction to this retract route, not to existence of a witness by
another nonlinear correction scheme.

## 5. Intersecting formation support

Let \(R_n\leq A_n\) be the exact formation-supported residual submodule.
Suppose it is itself the image of a \(\Lambda\)-linear idempotent

\[
 e_R:A_n\longrightarrow A_n,
\qquad \operatorname{im}e_R=R_n.
\tag{5.1}
\]

### Corollary 5.1 (BRUNNIAN--FORMATION RETRACT)

If

\[
 e_Re_{\rm Br}=e_{\rm Br}e_R,
\tag{5.2}
\]

then

\[
 e_{\rm loc}=e_Re_{\rm Br}
\tag{5.3}
\]

is an idempotent with

\[
 \boxed{
 \operatorname{im}e_{\rm loc}=R_n\cap B_n.}
\tag{5.4}
\]

Thus the doubly localized submodule is filtration-strict.

#### Proof

Apply v326 Theorem 4.1 to the two commuting idempotents. \(\square\)

If (5.2) is unavailable, it suffices instead to retract \(A_n\) onto one
factor and then retract its image onto the intersection, as in v326
Corollary 5.1.  Two unrelated projections do not prove (5.4).

## 6. Word-bearing and cofinal requirements

For use in v319--v321, a finite certificate must retain:

1. the exact occurrence-tagged face and degeneracy maps;
2. direct replay of the simplicial identities used by \(P_n\);
3. the normalized image \(N_n\), the map \(\partial_n\), and its exact image;
4. a module-linear section \(s\) with direct replay of (2.1), or a complete
   non-split certificate;
5. the formation idempotent/retraction and the commutation or nested
   preservation required in Section 5; and
6. application of the resulting projector to an ambient-depth ancestry as
   in v326 Proposition 2.1.

Across a cofinal tower, all maps and projectors must commute with reduction
for a closed explicit selector.  If only finite-level solution sets are
known nonempty, compatibility must instead be supplied by a complete
finite-fibre compactness argument containing all nonlinear side gates.

## 7. R07 boundary

V72 identifies the Brunnian part \(Z_3(A)\) on an actual abelian
diagram-chief factor.  Theorem 2.1 shows that its saturation is automatic
once the remaining normalized \(d_0\) sequence splits over the actual action
ring.  Theorem 3.1 discharges that split for a genuinely prime-to-three
action quotient.

This does not yet identify the completed group-level target \(B_P\) of v252
with a compatible inverse system of the linear \(B_3\) projectors.  Nor does
it construct the formation projector \(e_R\) or prove (5.2).  The remaining
structural gates are therefore:

1. authenticate the action ring and decide the normalized extension (1.5);
2. lift the degreewise Brunnian projectors through the chosen filtration;
3. construct the exact formation retraction or use pointed saturation; and
4. replay their interaction on the actual class-two remainder.

Normalized-Brunnian projection under a split \(d_0\), the prime-to-three
averaged section, the Ext split criterion and the commuting formation
intersection are paper proofs.  Their actual R07 hypotheses are not yet
authenticated.  A compatible cofinal lift, fake certificate and Ihara
witness remain absent.

R07_NORMALIZED_BRUNNIAN_FILTERED_RETRACT_V327_PAPER_GRADE
