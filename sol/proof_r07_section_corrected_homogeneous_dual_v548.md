# R07: section-corrected homogeneous dual, without a physical lower multiplier (v548)

Author: root / 2026-09-05

Status: paper strengthening of v543 on its same registered finite source.
It removes that oracle's separate Conn lower-multiplier adapter, not the
retained Conn premise or the actual source-coordinate adapter. It does not
decide the physical target. The next seed34 materialization proceeds without
waiting for this paper. `verified=false`.

## 1. The precise lower and top types

Work over k=F3 and keep v543's complete legal occurrence images

```text
pi: W2 -> W1,                 onto, dim W1=8059,
ell=ell1 pi: W2 -> Lphys,     Lphys=k^32260,
G: W2 -> P,                  P=k^48384.
```

The coordinate truncation pi is SOURCE truncation. In the fixed ambient
coordinates from v541, an element of W2 is u=(b,z), where

```text
b in Lsrc=k^96776 = d0 + d1 + aux,
z in V=(k^36288)^4.
```

Thus W1 is a subspace of Lsrc, pi(b,z)=b, and W2 is a subspace of
Lsrc direct-sum V. Neither decomposition is asserted equivariant.

Let b_i (i=0,...,8058) be the complete accepted P1 source basis, and let
tilde_b_i=(b_i,z_i) be its accepted canonical lifts. V483 with its v486
repair gives pi(tilde_b_i)=b_i. Consequently there is a linear section

```text
s: W1 -> W2,             s(b_i)=tilde_b_i,
R=id_W2-s pi,            R(W2)=ker pi.                  (1.1)
```

This is a section of vector spaces, not a homomorphism on literal words.
Its values carry the existing finite P1 DAGs.

Use Task712 only for its correct pure homogeneous physical map:

```text
H(b,z) = sum_(a=0)^3 B_a(z[a]).                         (1.2)
```

By v530(2.1), H and G agree on ker pi. More explicitly, v530's full
filtered aggregation has a lower-to-top contribution C, so

```text
G(b,z)=C(b)+H(b,z),       G-H=C pi on W2.               (1.3)
```

Here C is only needed on W1. No numerical C table is needed below. The
factorization also follows abstractly: a linear map vanishing on ker pi
factors uniquely through the surjection pi.

The complete physical lower-zero image is still the v543/v535 object

```text
M2=G(ker ell)=span(Conn)+G(ker pi).                     (1.4)
```

The retained Conn is the FULL image of all lower-physical relations among
the canonical P1 lifts. Its accepted derivation is not removed or replaced
by a source-rank count in this note.

## 2. Subtract the section on BOTH sides of the filtered comparison

Let lambda in P* be the current separator, with

```text
lambda(Conn)=0,       lambda(S_current)=0,
Conn <= S_current <= M2,      lambda(rho2)=1.            (2.1)
```

Define a functional chi on W1 by its basis values

```text
chi(b_i)=lambda H(tilde_b_i)
        =sum_a <B_a^*lambda,z_i[a]>.                    (2.2)
```

Because the b_i are an actual independent basis, this prescription is
well-defined WITHOUT solving any physical lower-row relation. Equivalently
chi=lambda H s. Put

```text
F_lambda = lambda H - chi pi
         = lambda H R
         = lambda G R.                                 (2.3)
```

The last equality is the key cancellation: (G-H)R=C pi R=0.

### Proposition2.1 (section-corrected invariance)

For any linear C':W1->P, replacing a map H by H+C' pi does not change
its section-corrected functional

```text
lambda H - (lambda H s) pi.                            (2.4)
```

Proof: the change is lambda C' pi - lambda C' pi s pi=0, since pi s=id.
This proves (2.3) for the ACTUAL C in (1.3) without constructing C. QED.

This does NOT assert H(tilde_b_i)=G(tilde_b_i). That equality is generally
false and was precisely the filtered-type problem in v530/v541. In (2.3)
the omitted lower-to-top contribution is subtracted from BOTH the input and
its complete canonical section. Projecting or changing only the direct side
of a mixed seed/actor relation remains invalid.

In particular, the values (2.2) are NOT the values lambda G(tilde_b_i) used
in v543 to define its physical multiplier mu. No such identification is
needed. If mu is chosen as in v543, then

```text
lambda G s = mu ell1,
lambda G - mu ell = lambda G R = F_lambda.              (2.5)
```

Thus the new construction gives exactly the old oracle functional, rather
than a stronger test on the wrong lower fibre.

## 3. Complete separator equivalence, now using only P1 interpolation

### Theorem3.1

Under the stated complete-source and Conn premises,

```text
lambda(M2)=0  iff  F_lambda(W2)=0.                      (3.1)
```

Proof: (1.1) and (2.3) give
F_lambda(W2)=lambda G(ker pi). The other summand of M2 in (1.4) is
annihilated by (2.1). Hence (3.1). QED.

If F_lambda(u) is nonzero for a legal u, the explicit corrected source

```text
v=R(u)=u-s pi(u) in ker pi
```

satisfies lambda G(v)=F_lambda(u) !=0. As lambda kills S_current, G(v)
is a new physical direction. The P1 subtraction remains necessary for
actual source/literal materialization; its scalar can be known first.

Changing the section changes the nonzero search functional in general.
Nevertheless the ZERO criterion (3.1) is invariant, since every section's
R maps onto the same ker pi. The actual implementation must use the same
accepted canonical section on both sides. No switch of P1 lifts is hidden
in (2.3).

## 4. Existing fresh contraction bytes supply all interpolation values

For the current actual rank1355 separator, run33954712636/1 has computed

```text
q_a=B_a^*lambda,                  four roots,
v_a[i]=<q_a,z_i[a]>,             four8059-entry vectors. (4.1)
```

The run's authenticated output contains q-aA-root.bin and
p1-values-aA.bin for a=0,1,2,3. Its source/launch commit is
92c98486ab659f7e3358fc3c4afb53ab6b78293d; candidate artifact9966008518.
The exact actual receipts are recorded in reply162 section14 and v220
Delta532. Therefore

```text
chi(b_i)=sum_a v_a[i] mod3                              (4.2)
```

uses already computed finite data. Summing ALL four characters is the
general formula; in this particular run q1=q2=q3=0, so the sum happens
to reduce to v0. That sparsity is an observed current value, not a premise
for later separators. After any next pivot these root values are stale.

To apply chi without reducing each raw chain separately, choose any
extension kappa in Lsrc* with

```text
<kappa,b_i>=chi(b_i),       i=0,...,8058.                (4.3)
```

Such an extension exists by independence of the b_i. It can be obtained by
dual interpolation on the EXISTING joint P1 source echelon, with zero
choices for ambient free coordinates, and then checked by all8059 dots.
This is source-basis back substitution, not the physical lower-pivot solve
of v543. If stored block leads differ from the joint coordinate order, that
embedding must be used correctly; insertion order must not be mistaken for
increasing lead order. No unproved triangular ABI is imposed here.

The immutable Task554 lower-row payloads total67011332 bytes by v541
section5. Old rows contain an owner d0 block, all four d1 blocks, and the
shared eight auxiliary slots; new rows contain one d1 block. Those shared
auxiliary slots must NOT be split into fictitiously independent per-character
coordinates. Equation (4.3) is on the full96776-coordinate source row.

This eliminates the need to export the6705 physical lower-pivot pairs and
to compute mu(ell_i)=lambda G(tilde_b_i) for this oracle. It does not assert
that kappa has already been implemented/exported, that its practical solve
is free, or that any measured runtime reduction has occurred. Nor does it
remove Conn from the correctness premises of (3.1).

## 5. The tree/five-carry test with the cheaper adjoint input

Use the same complete actual source of v543:

```text
Z=ker(partial:k[Q2]^2 -> k[Q2]),    |Q2|=54432,
tau:Z -> k^5 onto,                 K=ker tau,
D=K x k^2,
Psi:D -> W2 onto.                                      (5.1)
```

V546 gives the five legality functionals as three rotation carries and
two ordinary exponent rows; it does not by itself export their marked
Cayley-tree array. Keep the actual same-owner Fox/occurrence/truncation
map Psi, not six independently chosen occurrence rows.

Write the lower/top coordinate components of Psi as Psi1,Psi2. Then

```text
F_lambda Psi
  = sum_a q_a Psi2[a] - kappa Psi1.                    (5.2)
```

Use an authenticated linear raw-chain extension of these SAME source maps
to obtain an edge cochain f and a two-coordinate auxiliary row b_aux:

```text
F_lambda Psi(z,eta)=f(z)+b_aux(eta),   (z,eta) in D.     (5.3)
```

Only the value on D matters. Abstract extensions always exist, but an
efficient actual adapter must implement the source Fox maps, marked
substitutions, Fourier/monomial coordinates and handedness correctly.
This note does not replace that adapter by a claim of automatic availability.
The full PHYSICAL lower-to-top aggregation and the Conn multiplier are
absent from (5.2); the SOURCE maps can still contain their own mixed terms.

For the fixed tree, let z_e be each fundamental cycle, choose five with
independent tau(z_e), and fit a in (k^5)* on those five. Theorem3.1 and
v543 Theorem3.1 now give exactly

```text
lambda(M2)=0
 iff b_aux=0 and f(z_e)=a tau(z_e) on ALL54433 chords.   (5.4)
```

Tree integration computes f(z_e) from the108864 edge entries; no full
legal-source-by-physical-target matrix is required by this test. The counts
are finite array/comparison sizes, not an end-to-end time estimate.

If a chord fails, v543 constructs a legal combination z of at most six
fundamental cycles with F_lambda Psi(z,0)!=0. V547's literal formula
R_word(w)=w (r_x^3)^(-eps_x(w)/6) (r_y^3)^(-eps_y(w)/6)
[r_x,r_y]^omega(w) supplies its exact-normalized Omega word without an
endpoint table. This R_word is DISTINCT from the linear section subtraction
R in (1.1). Subtract the selected P1 lifts as in Section3 to obtain the
actual lower-zero rank-raising word ancestry. If an auxiliary test fails,
use its literal c_x or c_y source first. An actual materializer still checks
the complete lower-zero row and the physical value.

## 6. New work removed, remaining gates, and completion boundary

Relative to v543, the separate mu/Conn-lower-pair export and the physical
mixed-term adjoint are removed from this prospective oracle. The replacement
is (4.3), using the fresh8059 basis values that the production root scan
already computes. V546 supplies the legality formulas; v547 removes the
endpoint-table step. All three improvements preserve the same complete
registered source and the same target.

Still needed for an actual complete oracle result are:

1. an actual P1-source kappa interpolation and its8059 equalities;
2. the actual same-owner SOURCE adjoint in (5.2), including its mixed terms;
3. the marked tree/carry roster and the full finite identity test (5.4);
4. for a violation, the selected word/P1 subtraction and physical replay.

These are prospective alternative-oracle tasks, not new release gates for
the current seed34 materializer. No such adapter has been run in this note.
The current176-root-seed result is a concrete violation already, so it needs
no complete tree test before materialization.

Independent Task942 audit is PASS with no necessary mathematical repair;
see `sol/sol_reply_942_audit_r07_section_corrected_dual.md`. Its complete
P1/Conn/source-map premises are retained, not numerically re-audited here.

```text
SECTION-CORRECTED H/G INVARIANCE:      PAPER PROOF
CONN PHYSICAL LOWER MULTIPLIER:       NOT NEEDED FOR THIS ORACLE
FRESH8059 SOURCE BASIS VALUES:        ALREADY COMPUTED FOR RANK1355
ACTUAL kappa / SOURCE ADJOINT / TREE: NOT YET EXPORTED
ACTUAL rho2 MEMBERSHIP / GRADE2:      NOT DECIDED
FULL A0 / COFINAL / FAKE / IHARA:      NOT DECLARED
verified=false
```
