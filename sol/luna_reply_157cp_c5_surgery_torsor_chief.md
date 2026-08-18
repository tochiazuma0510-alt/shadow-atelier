# 157cp — literal C5 surgery and chief-factor audit

## Verdict and boundary

The five A.18 cofaces give a finite, losslessly enumerable correction
problem. They do not, by themselves, give a C5 contraction of that problem.
The useful statement is therefore a finite-decision statement: after a
chief-step manifest supplies the actual action, section, and typed source
fibre, one exhaustive finite replay decides whether the common correction
fibre is empty and, when it is nonempty, returns actual ML(K) witnesses.

The exact status is a blocked global theorem.  The finite contract below is
sound only after one particular first-bad chief manifest has been supplied;
it does not yet close the quantifier over all finite quotients below M.  The
earlier `C5_SURGERY_TORSOR_FINITE_DECISION_READY` label is therefore
withdrawn: it described a per-manifest decision, not a global B4-B decision.
No local GAP, Git, GHA, or Python computation was run for this audit.

## 1. The literal finite fibre

### 1.1 Primary equations and maps

The primary paper was checked by page images. On p.13, (2.18)--(2.20) and
Definition 2.6 define a finite GT-pair [m,f] by the two hexagon equations
in B3/N_PB3 and the pentagon equation in PB4/N:

~~~
sigma_1 x12^m f^{-1} sigma_2 x23^m f N_PB3
    = f^{-1} sigma_1 (x13 x23)^m N_PB3,

f^{-1} sigma_2 x23^m f sigma_1 x12^m N_PB3
    = sigma_2 sigma_1 (x12 x13)^m f N_PB3,

phi_234(f) phi_1,23,4(f) phi_123(f) N
    = phi_1,2,34(f) phi_12,3,4(f) N.
~~~

The last line is the literal five-coface pentagon product, not a rho orbit
or a replacement norm. A representative is changed by

~~~
(m,f)  ->  (m + q N_ord, f h),  q in Z, h in N_PB3,
~~~

and the equations are required to be independent of that choice.

The five homomorphisms used in the last line are the exact table on p.49,
(A.18):

~~~
phi_123:       (x12,x23,x13) -> (x12,             x23,             x13)
phi_234:       (x12,x23,x13) -> (x23,             x34,             x24)
phi_12,3,4:    (x12,x23,x13) -> (x13 x23,         x34,             x14 x24)
phi_1,23,4:    (x12,x23,x13) -> (x12 x13,         x24 x34,         x14)
phi_1,2,34:    (x12,x23,x13) -> (x12,             x23 x24,         x13 x14).
~~~

Proposition A.2 on pp.48--49 proves these are homomorphisms. Proposition
2.11 on p.18 is the relevant compatibility statement for their induced
maps. These page-image facts fix both the direction and the product order
in the correction test.

For a chief step K <= H <= M, fix a target

~~~
q = [m_H, f_H] in GT^heart(H)
~~~

and a section to the finite quotient at K. Let E_q(K,H) be the finite
set of all section lifts (m,f) reducing to q, before imposing any GT
condition. A fixed m and a fixed section lift f_0 give, in an
elementary chief factor V=H/K, a right pointed torsor

~~~
f_0 V = { f_0 v : v in V }.
~~~

If the chosen presentation uses r independent chief coordinates rather than
one GT-pair correction coordinate, the corresponding pointed torsor is V^r;
r is part of the source manifest and may not be silently set to one. For a
nonabelian chief factor the same notation means a pointed right torsor under
V=S^t, with noncommutative multiplication; it is not an additive vector
space.

Define the literal typed correction fibre by

~~~
F_A18(K,H;q) = { [m,f]_K in E_q(K,H) :

  Hex_1(m,f) = 1 in PB3/N_PB3(K),
  Hex_2(m,f) = 1 in PB3/N_PB3(K),
  Pent_A18(f) = 1 in PB4/K,                 (the five literal maps above)

  Mark(m,f) and the prescribed S4/B2 markings hold,
  Onto_B4(m,f), Onto_B3(m,f), Onto_B2(m,f) hold,
  Charming(m,f) holds,
  Heart(m,f) holds,
  ker(T^{PB4}_{m,f}) = K,                   (settlement at K),
  the F2 commutator representative and T^{F2}_{m,f} onto conditions hold,
  every representative change (m+q*N_ord, f*h) has the same result,
  and reduction_K,H([m,f]_K) = q.
}.
~~~

Here Pent_A18 is the equality in (2.20), evaluated with all five maps,
not merely one scalar defect. Onto_B4/B3/B2 are the three maps (2.33)--
(2.35); Definition 2.9 is on p.17 and Proposition 2.10 identifies them with
the onto truncated-operad condition. On p.25, Definition 2.19 spells out
the charming requirements: the f coset has a representative in
[F_2,F_2], and

~~~
T^{F2}_{m,f}: F2 -> F2/(N_PB3(K) intersection F2)
~~~

is onto. Settlement is the source-kernel equality in Definition 3.2,
p.29. “Heart” here means the project's designated charming/settled heart
object; it is a gate in the manifest, not a license to omit the primary
conditions.

This definition also fixes an important distinction. The raw torsor
E_q(K,H) is always a finite pointed fibre after the finite section is
fixed. The subset F_A18(K,H;q) is not automatically a torsor: when the
joint equations are affine its nonempty part is a torsor under the joint
stabilizer, and in the nonlinear case it is only a pointed finite groupoid
fibre. Calling every nonempty subset a torsor would hide exactly the
chief-step obstruction.

### 1.2 The actual coupled correction map

For an elementary chief factor, choose the section lift as origin and let
C be the finite correction module (V or the declared V^r). Linearize
the complete relation-and-gauge data, not just one equation. After quotienting
by relation boundaries and gauge changes, write the exact joint map as

~~~
D_A18 : C -> Q_A18,
beta(q) in Q_A18,
~~~

where Q_A18 contains the two hexagon residuals, the five-coface pentagon
residual, all relation syzygies, and the marking/representative transport
terms. With the convention that a correction c is applied on the right,
the necessary and sufficient linearized condition is

~~~
D_A18(c) = - beta(q).
~~~

Thus a common correction exists precisely when

~~~
-beta(q) in im(D_A18),
~~~

and, if c_0 is one solution, the solution set is the affine torsor
c_0 + ker(D_A18). This assertion becomes a valid lift statement only
after replaying the nonlinear equations and every typed gate in the
definition of F_A18; a zero class in a guessed linear quotient is not an
ML(K) witness.

The five coface entries are not five independent corrections. A formal
model with one variable c and residual map

~~~
c -> (2c, 3c, 5c)
~~~

already shows the problem: even when an unrelated C5 cohomology group
vanishes, a prescribed triple need not lie in this one-dimensional joint
image. Separate inversions of the two hexagons and a pentagon norm do not
prove membership in im(D_A18).

## 2. What “C5 symmetry” really permits

The paper supplies a five-element literal list of cofaces. It does not
state that an arbitrary finite chief correction complex has a cyclic action
of order five. The project may use a C5 surgery only after the chief
manifest records an automorphism tau of the finite typed data satisfying

~~~
tau^5 = 1,
tau(phi_i) = phi_(i+1) up to the recorded inner/marking transport,
the product and representative convention are preserved,
and tau acts on the section, C, Q_A18, and all onto/charming gates.
~~~

The inner transports must themselves close after five steps. A permutation
of five labels without this transport certificate is not a C5 action on
F_A18.

When this certificate exists, the precise averaging statement is as follows.

* If p != 5, C and Q_A18 are F_p[C5]-modules, D_A18 is
  C5-equivariant, and beta(q) is fixed by the transported C5 action, then
  from any solution c one obtains a fixed solution

  ~~~
  c_bar = (1/5) (c + tau*c + tau^2*c + tau^3*c + tau^4*c),
  D_A18(c_bar) = -beta(q).
  ~~~

  This is an averaging of an already existing common solution. It is not a
  proof that -beta(q) lies in the joint image. If beta(q) is not fixed,
  the same average solves only the averaged equation. If the section or a
  side gate is not C5-invariant, the average need not be a valid correction.

* For p=5, division by five is unavailable. For the actual C5 operator
  tau the norm is

  ~~~
  N_tau = 1 + tau + tau^2 + tau^3 + tau^4 = (tau - 1)^4.
  ~~~

  The exact norm equation N_tau(c)=-beta is solvable iff the class of
  -beta vanishes in coker(N_tau)=Q/im(N_tau), and then its solution set
  is c_0 + ker(N_tau). In the trivial characteristic-five module the norm
  is zero, so a nonzero beta is an immediate obstruction and a zero beta
  leaves the whole kernel undetermined. This norm test is only one
  component unless the manifest proves D_A18=N_tau after all gauge and
  syzygy quotients.

Consequently H^1(C5,V)=0 or H^i(C5,V)=0 is not enough. Such a statement
concerns a specified cochain complex; it neither supplies the actual
D_A18, proves its C5 equivariance, nor checks the two hexagons, the
representative convention, the onto conditions, or the nonlinear heart
condition.

## 3. Exhaustive chief-factor split

### 3.1 Elementary abelian p != 5

Let V=F_p^d. The correct test is the exact matrix/table for D_A18 and
its C5 transport. A common correction is accepted only if the exact class
-beta is in the joint image and the corrected pair passes the full replay.
If the C5 data are valid, averaging can select a C5-fixed representative;
it cannot create a solution when the joint image is too small.

This includes the p=2 and p=3 lanes. In characteristic two or three,
coefficients from one hexagon may vanish while the other hexagon or the
five-coface term remains nonzero, so “prime to five” is not a licence to
average each equation independently. The exact action may also have
Jordan blocks; an exponent or norm inferred from the abstract order of the
roof is not an action calculation.

The theorem that would kill this branch is therefore the following explicit
one, not ordinary C5 cohomology:

~~~
for every typed first-bad chief source q,
  the recorded D_A18 has -beta(q) in its image, and
  every selected solution replays to F_A18(K,H;q) != empty.
~~~

No such uniform typed theorem is presently in the accepted artefacts.

### 3.2 Characteristic five

The exact ker(N_tau)/coker(N_tau) calculation above is the only automatic
linear reduction. The q5 Burau fibre can be used as a finite image of the
pentagon map only after an equivariant map

~~~
Q_A18 -> Q_Burau,   D_A18 -> D_Burau
~~~

is included in the chief manifest, with the same section and representative
convention. A q5 zero fibre then proves that a target has no compatible
profinite lift in that finite quotient; it does not prove a positive chief
correction. A q5 all-pass result merely passes this necessary test.

For a positive characteristic-five chief step the receipt must contain an
actual c, the norm kernel/cokernel basis, the full joint defect, and all
F_A18 gates. A receipt containing only a zero Burau defect, a Magnus
functional, or a norm-rank statement is not sufficient.

### 3.3 Nonabelian S^t, 5-coprime

For V=S^t there is no additive D_A18 or linear power norm. The outer
action is a finite map

~~~
C5 -> Out(S^t),
~~~

and a chosen lift to Aut(S^t) carries a pointed nonabelian cocycle set. A
C5 correction u satisfies

~~~
u * tau(u) * tau^2(u) * tau^3(u) * tau^4(u) = 1,
~~~

modulo the pointed gauge relation u ~ g^{-1} u tau(g). Changing the lift
of the outer action changes this description by the corresponding inner
transport; the manifest must list the transport rather than silently
choose a complement.

If 5 does not divide |S^t|, Schur--Zassenhaus gives conjugacy of
complements in the associated finite semidirect extension, so the pointed
C5 complement class is trivial under that hypothesis. This kills only the
C5 complement torsor after the A.18 fibre has been proved equivalent to it.
It does not automatically solve the two hexagons, the five-coface product,
or marking/onto/heart conditions. Those must still be replayed.

### 3.4 Nonabelian S^t, 5-divisible

If 5 divides |S^t|, neither Schur--Zassenhaus nor additive averaging
applies. Enumerate every ordered correction tuple in S^t (and every
declared coordinate tuple if r>1), every recorded outer-action lift up to
inner equivalence, and every representative/gauge orbit. Replay the two
hexagons and all five literal cofaces in the noncommutative product order.
The result is either a finite list of actual typed corrections or an
exhaustive empty fibre; a failed linear norm test is not a result.

The primary paper has no theorem that removes either the nonabelian branch or
the characteristic-five branch. In particular, residual finiteness of the
source does not make the lower chief factors prosolvable.

## 4. First-bad refinement and surgery/torsor use

Let K <= M be a typed isolated refinement and let x be a target roof. A
finite quotient attached to a proposed path from M to K has a B4-stable
composition series

~~~
M = K_0 >= K_1 >= ... >= K_r = K,
V_j = K_(j-1)/K_j
~~~

where each V_j is elementary abelian or S^t. The series is chosen in
the finite B4-normal quotient, so each chief factor is invariant under the
literal coface transports. It need not make every K_j an isolated object.

For every intermediate object use the finite typed groupoid fibre

~~~
F_j(x) = { s in GT^heart(K_j) :
           reduction_(K_j,M)(s) = x,
           all source/target, marking, charm, and coface data are present }.
~~~

At an isolated endpoint this is the finite ML(K_j) fibre. At a
non-isolated intermediate level it is a finite groupoid fibre with its
source-kernel label retained; it must not be collapsed to a group or called
settled without the source-kernel equality.

If F_0(x) is nonempty and F_r(x) is empty, choose the first j with
F_j(x)=empty. The preceding fibre is nonempty and the chief correction
fibre over one of its typed elements is exactly the finite object in
Section 1. An accepted element of F_A18(K_j,K_(j-1);q) would reduce to a
member of F_j(x), contradicting first badness. Conversely, an exhaustive
empty correction fibre is a genuine first-bad obstruction only when the
input enumerates all section lifts, m-lifts, outer-action representatives,
representative changes, and gauge orbits.

The project TORSOR/SUBTOR formulas are useful after this typing is in place.
For an isolated N, the settled group acts freely and transitively on a
nonempty fixed-kernel fibre; for a subgroup image X, the settled part S_X
is a subgroup and each nonempty same-kernel slice is an S_X-torsor. The
formulas are

~~~
|GT(N)| = |GT^settled(N)| * number_of_components,
|X|     = |S_X| * number_of_nonempty_components_of_X.
~~~

They give transport, differences, and representative independence. They
cannot turn an empty chief correction fibre into a nonempty one, and they do
not prove that a raw Burau or Magnus state is in ML(K).

At the roof, the accepted group premises are enough for the prime-index
promotion. Definition 3.2 makes an isolated GT(M) a finite group (p.29),
Proposition 3.7 makes the reductions between isolated objects group
homomorphisms (p.31), and Proposition 3.11 gives the compatible reduction
square (p.36). Hence

~~~
I_K = image(ML(K) -> ML(M))
~~~

is a subgroup. The accepted arithmetic map gives A <= I_K, and the
accepted roof package gives |A|=324, |X|=972; hence an actual typed
outside element, or 325 distinct actual typed roofs, forces I_K=X.

The current outside selector is compatible with all complement/Kummer
choices. With W=A intersection (C9 x C9), |W|=27 and both coordinate
projections onto C9, W/3V is one of the two non-axis lines. Thus the
marked pure axis e1=(1,0) is outside A. Under the accepted quotient
X/W ~= S3 x C6, e1 is a 3-cycle. If a is an arithmetic lift above a
cyclotomic generator, a e1 is an outside reflection independently of the
Kummer sign and complement twist. Consequently

~~~
e1^n remains outside when 3 does not divide n,
(a e1)^n remains outside when n is odd.
~~~

These are roof membership filters only. They become useful in the chief
campaign after an actual corrected pair has been replayed and reduced to
the corresponding roof key.

Finally, for a nested isolated system, Proposition 3.7's composition law
and the primary cofinality/intersection results (Corollary 3.5 and
Proposition 3.6, p.30; Theorem 3.8 and Corollary 3.13, pp.33 and 38) give the
finite-fibre compactness bridge. For fixed x, the finite sets F_j(x) have
the actual reduction maps

~~~
F_(j+1)(x) -> F_j(x),
~~~

and compatible nonempty prefix fibres yield a branch by finite branching.
This is valid only after the chief campaign supplies prefix-stable actual
ML witnesses and the selected family is cofinal in the full isolated
poset. A different 325 list at each unrelated level is not enough.

## 5. Active artefacts and their exact logical grades

### 5.1 Literal 18+140 A.18 campaign

The task supplies run 32083392589 for the current literal campaign. Its
mathematical input is the 18 K(0,5) prefix rows plus 5*28=140 literal
A.18 coface rows, with the unconditional five-coface defect and the stated
Magnus degree/shard contract. The versioned v2 dependency audit binds the
recursive producer/checker closure and excludes the old rho-tail.

A nonzero Magnus pairing or nonzero raw-A.18 row is a necessary obstruction
to the corresponding raw presentation. It is not a chief correction
certificate. To promote it, the campaign would have to attach a section
lift and a correction c and pass every gate in F_A18(K,H;q) above. An
all-zero result is likewise only UNKNOWN for the common-correction question
unless the same typed replay is present.

The run number alone is not a receipt. This reply records no theorem-level
result from 32083392589 beyond the literal finite-contract meaning above.

### 5.2 q5 nested-seal Burau fibre

The task supplies run 32082657301 and an older q5 run. The repaired q5
contract scans the complete finite right coset h_0 K_q in the auxiliary
finite image for q=5 and the two registered parameters a=2,4, over the
frozen 972 roof rows. The nested seal binds the outer calibration run,
inner source run, artifact identities, receipt hashes, source hashes, row
ledger, and independent checker.

A complete q5 row with zero identity pentagon defects is a one-way
obstruction: any genuine profinite GT lift would map through the same finite
A.18/Burau quotient and would have identity defect. Under the accepted
X=GT^heart(M), A<=I<=X, |A|=324, |X|=972 package, one such typed roof
exclusion forces I=A and is a terminal B4-A conclusion. A complete
all-pass q5 row is only a pass of this necessary test.

This does not identify Q_A18 with the Burau chief module. To use q5 as a
positive characteristic-five surgery result, the chief manifest still needs
an exact equivariant comparison map, the same representative convention,
and a reconstructed c passing the full typed gates. The repository
contains the sealed workflow contracts but no new q5 result should be
inferred from the run ID alone.

### 5.3 The C2^24 fast witness

The fast witness bundle records 24 coordinate source words, a marked
characteristic-two ambient module of order 2^24, and the intended four
coordinate blocks. Its structural conclusion is conditional on the pinned
four-deletion/isolation and direct-product inputs. The recorded dispatch
32083286058 stopped before the hash stage; no GHA receipt is available in
this workspace. Therefore it is not yet an actual B4-stable chief factor,
not yet the full A.18 obstruction module, and not a 325-lift witness.

Even after a GHA receipt, the minimum promotion package is:

~~~
B4 generator action on the 24-dimensional module,
B4 relations and source-kernel certificate,
chief/composition-series certificate,
explicit equivariant comparison with Q_A18,
and one full typed replay of the 24 source words through both hexagons
and all five literal cofaces.
~~~

Characteristic two is prime to five, so C5 averaging could then be tested,
but it cannot be assumed from the ambient module receipt.

## 6. One bounded exhaustive decision for a supplied manifest

The following is a single fail-closed finite decision for one already pinned
first-bad chief manifest.  It is deliberately stated at this level: the
manifest is finite, but the existence of one finite manifest covering every
possible first-bad refinement is a separate theorem and is audited in
Section 7.

### 6.1 Exact inputs and state count

Use a versioned input bundle with schema d972-b4-c5-chief/v1 containing:

~~~
M,H,K normal-subgroup manifests and inclusion digests;
finite quotient H/K multiplication table and chief label;
section and all outer-action/inner-transport data;
complete typed H-level source list U_H(x), for every x in the 972-row X;
exact m-lift list L_m(u) and the number r of chief correction coordinates;
PB3/PB4 generators and relation rows;
the two hexagon words and the five literal A.18 maps;
marking, B2/B3/B4 onto, charming, heart, settlement,
representative-independence, and reduction check data;
C5 action certificate (if a C5 surgery lane is claimed);
accepted X/A data and the outside-axis certificate.
~~~

The checker computes, rather than trusts, the complete raw state count. If
U_H(x) is the list of typed H-source witnesses over roof x, then

~~~
N_raw(elementary) =
  sum_{x in X} sum_{u in U_H(x)} |L_m(u)| * |V|^(r(u)),

N_raw(nonabelian) =
  sum_{x in X} sum_{u in U_H(x)} |L_m(u)| * |S|^(t*r(u)).
~~~

For the intended one-GT-pair chief fibre, r=1; if the manifest has more
than one independent correction coordinate, the second factor is retained
and every tuple is enumerated. With one source and one m lift per roof this
specializes to 972*|V| or 972*|S|^t; an axis-only lane has exactly
2*|V| or 2*|S|^t states for e1 and a e1. The exact integer and every
row's source/correction index are written to the receipt. No sample,
random orbit, word-length cutoff, or guessed fibre size is admissible.

For the q5 sidecar the corresponding count is
sum_x |h_0(x)K_q|; it is read from the exact kernel enumeration and is not
replaced by the calibration value or by a product of specialization sizes.

### 6.2 Four exhaustive lanes

The matrix has the following fail-closed lanes:

~~~
E-p-ne-5: enumerate all V^r states, compute D_A18 and its C5 transport,
          replay every full typed gate.
E-p=5:   enumerate all V^r states, and independently record N_tau image,
          kernel, cokernel, beta class, and q5 comparison if supplied.
S-coprime: enumerate all ordered S^t correction states and outer-action
           representatives; Schur-Zassenhaus is only a cross-check.
S-5div:  enumerate the same complete nonlinear state space with no linear
           shortcut.
~~~

The C5 average is an optional canonical representative in the first lane;
all states remain covered. In the p=5 lane, N_tau=(tau-1)^4 is replayed
from the supplied matrix, not inferred from a label. In the nonabelian lanes
all products use the displayed A.18 order and all inner twists are retained.
A resource or timeout outcome is UNKNOWN, never a truncated pass.

### 6.3 Positive receipt and why it is sufficient

Every accepted record must contain:

~~~
chief factor and source identifiers;
complete correction tuple and representative;
all two-hexagon values and all five coface factors;
marking, three onto maps, charming F2 representative and onto replay;
heart/settlement and representative-independence checks;
reduction key in H and canonical key in X;
C5 orbit/transport record and norm image/kernel/cokernel data when relevant.
~~~

The independent checker reconstructs the finite quotient and action from the
manifest, replays every candidate, recomputes the state count, canonicalizes
and deduplicates the 972-base roofs, and verifies the reduction composition.
It accepts one of only these mathematical results:

~~~
C5_CHIEF_NO_CORRECTION       all raw states exhausted and no F_A18 witness;
C5_CHIEF_OUTSIDE_ONE         one accepted typed roof in X\\A;
C5_CHIEF_325                 at least 325 distinct accepted typed roofs;
C5_CHIEF_UNKNOWN              missing input, resource stop, or any mismatch.
~~~

C5_CHIEF_OUTSIDE_ONE is sufficient because A <= I_K <= X and
|X:A|=3; C5_CHIEF_325 is sufficient by the same index-three lemma.
The reason these positive receipts are stronger than a Magnus/Burau result
is that every accepted object is an actual element of ML(K) (or a typed
intermediate groupoid fibre), with the canonical reduction replayed. The
receipt's positive result is therefore an image inclusion, not merely a
necessary residual condition.

To turn this finite decision into global B4-B, the same positive step must be
available for every first-bad chief factor arising below M, or a separate
uniform theorem must prove that the pinned finite manifest exhausts all such
factors. The primary isolated cofinality/intersection theorem supplies the
finite-fibre inverse-limit bridge after that uniform input; it does not
supply the chief correction itself.

### 6.4 The B5 kernel-surgery shortcut does not supply that uniform input

The proposed standard inclusion and deletion satisfy, on the braid groups,

~~~
i:B4 -> B5,       d5:B5 -> B4,       d5 o i = id,
K5 = ker(d5),     d5(Gamma)=1 for Gamma in K5.
~~~

Thus multiplying `i(Phi)` by a particular `Gamma` in `K5` preserves the
downstairs B4 word.  The primary B5 paper's page-image audit gives only the
following stronger-looking, but different, statement.  Observation 2.1
(p.3) is the one-way kernel implication
`i(ker(rho_4)) subset ker(rho_5)`.  Proposition 6.4 (p.17), for one
`Phi=Phi' Gamma_1` having a proper product, constructs a `Gamma` depending
on that `Phi` so that `i(Phi) Gamma` and `Gamma` satisfy the paper's proper
product/parity conditions and a winding-number inequality.  It is not a
surjectivity statement for a correction map into the three coupled A.18
residuals.  The p.18 construction is point-pushing, not an A.18 coface
transport.

In particular, no displayed identity in the paper has the form

~~~
(Gamma_123, Gamma_234, Gamma_12_34, Gamma_1_23_4, Gamma_1_2_34)
    |-> (D_hex_1, D_hex_2, D_pentagon)
~~~

with a common solution in `K5` while preserving marking, the three onto maps,
charmingness, and reduction.  The remark on p.20 explicitly warns that the
iterated push maps need not jointly satisfy the parity condition for more
than one correction.  Consequently the five A.18 cofaces are not five
independent `K5` correction slots.  This gives no operator identity killing
the characteristic-three sign-module countermodel and no uniform
nonabelian-chief absorption map.  The Burau result is therefore an auxiliary
necessary test, not the missing common-correction theorem.

## 7. Global finite-universe audit (the fatal gap)

The accepted finite roof data are exact but do not bound the deeper chief
layers.  In the theorem-relative project notation the current roof is

~~~
M = K^(9) intersection N_S4,
Q0 = PB3/M ~= G9 x PSL(2,8),
|Q0| = 1,469,664,
X = GT^heart(M), |X| = 972, A <= I_K <= X, |A| = 324.
~~~

The frozen files are

~~~
search/d972_semantic_m_manifest_v1.json
search/certs/nf972_sourcemap_a_tuples_v2_20260804.json
  count 972, digest 32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
search/certs/d972_b4_word_key_artifact_v1_20260816.json
  count 972, digest 283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930
~~~

They freeze the base roof and its word reduction.  They do not freeze a
finite quotient of every possible `M/K`.  Indeed `Q0=PB3/M` sees the quotient
above M, whereas the first-bad argument ranges over finite quotients of M
itself.  A chief factor of `M/K` is therefore not a chief factor of `Q0`.
The four-deletion calculation gives only the conditional ambient candidate

~~~
C_P/C_E ~= (C2)^24,
~~~

not an accepted B4-stable chief module with an A.18 comparison.  The latest
candidate producer/checker history records producer run 32083594772 ending
at the independent `P`-tuple-table mismatch (the earlier 32083286058 stopped
before hashing); hence no cross-checked `C2^24` action or source certificate
is available here.

Even granting that candidate as one correction coordinate, its exact
conditional finite scan would be

~~~
|C2^24| = 16,777,216 per frozen roof,
972 * 2^24 = 16,307,453,952 raw roof/correction tuples.
~~~

That is a bounded sidecar for the one proposed layer, not a state count for
all chief factors below M.  The p=5 q5 sidecar is likewise finite only after
its particular finite image and complete coset fibre are supplied; no q5
zero receipt is present.  For B5, `K5` is the point-pushing group identified
in the paper with the fundamental group of the four-punctured disk (a free
group of rank four under the disk convention), so its finite quotients have
unbounded order unless a particular quotient is fixed.  The faithful Burau
inclusion does not turn those quotients into a finite list of chief factors.

The exact missing lemma is consequently one of the following equivalent
global closures:

1. a **finite marked-chief-universe lemma**: every first-bad factor for every
   finite-index normal `K <= M` is one of a fixed finite list of explicitly
   marked sections, and every A.18 correction fibre factors through that
   list; or
2. a **minimality/Frattini push-up lemma**: a first failure in an arbitrary
   `M/K` can be pushed to the fixed `Q0` or the fixed four-deletion layer
   without changing the typed A.18 defect.

Neither lemma follows from the Q0 roof, the faithful Burau map, the
four-deletion cardinality, or the primary isolated compactness theorem.
The latter supplies the inverse-limit conclusion only once the uniform
chief-step premise is proved.  The existing first-bad construction does
produce a finite chief factor for each selected `M/K`; it does not produce a
single finite universe as `K` varies.  In the elementary case the prime and
module can vary, and the nonabelian case permits varying `S^t` and outer
action.  Thus the formula in Section 6 is not a global bound.

It would be unsound to label a run over the 972 rows, the conditional
`C2^24` sidecar, or one q5 fibre as deciding B4-B.  Such a receipt could
decide only that selected manifest.  Since no finite-universe or push-up
lemma is established, the requested one-run global STEP is not available.

## 8. Final accounting

The exact primary facts used here are the page-image statements
(2.18)--(2.20), (A.18), Definitions 2.6, 2.9, 2.19, 3.2, Proposition 2.11,
Proposition 2.22, Proposition 3.7, and Proposition 3.11 of
papers/2008.00066-what-are-gt-shadows.pdf. The project TORSOR/SUBTOR
formulas are used only after their settled/source-kernel hypotheses are
checked. The three active artefact families are recorded with their actual
logical grades, and no run ID is treated as a mathematical receipt.

The campaign specification above is bounded for each finite first-bad
manifest and is exhaustive at that manifest. It gives a concrete finite
answer path—positive typed lift, exact empty fibre, or UNKNOWN—without
replacing coupled A.18 equations by an unproved C5 average. What remains
outside this reply is the production of a receipt for the selected manifest
and, for a global B4-B theorem, the uniform coverage of all first-bad chief
factors.

The global audit above is the decisive qualification: the supplied finite
campaign is exhaustive only after its chief manifest is fixed, while the
fixed roof, Burau inclusion, and conditional four-deletion module do not
provide a finite universe of all such manifests.  No global B4-B conclusion
is claimed.

C5_SURGERY_TORSOR_CHIEF_BLOCKED
