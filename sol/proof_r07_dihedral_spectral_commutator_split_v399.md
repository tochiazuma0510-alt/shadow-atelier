# R07 dihedral spectral split of an actual commutator v399

Author: Sol / 2026-08-30

Status: paper theorem strengthening v398.  If the typed dihedral involution
commutes with the same actual eleven-occurrence operator and the literal Fox
split has odd value part and even connection part, the two parts have
closed-form legal preimages: the antisymmetric and symmetric projections of
the actual commutator instruction.  Thus no independent value solve or
field-outer connection homotopy is needed for that paired instruction.  The
actual R07 equivariance, parity, legality, A0 seed, and all-depth occurrence
typing are not asserted here.  No compatible R07 lift, fake certificate, or
Ihara witness is declared.  `verified=false`.

## 1. The typed involution

Let \(k=\mathbf F_3\).  At one adjacent registered layer, let

\[
 D^{\rm rel}=\ker(r_D:D_1\to D_0)                         \tag{1.1}
\]

be the physical legal relative correction space.  As in v395, all marking,
boundary, exponent-zero, formation, and already-imposed relation side gates
are included in this source.  Let

\[
 B:D^{\rm rel}\longrightarrow L^{\rm rel}                \tag{1.2}
\]

be the actual leading residual operator obtained by evaluating the eleven
literal occurrences with their individual prefixes and then aggregating in
the printed order.

Assume there are \(k\)-linear involutions

\[
 \theta_D:D^{\rm rel}\longrightarrow D^{\rm rel},
 \qquad
 \theta_L:L^{\rm rel}\longrightarrow L^{\rm rel}         \tag{1.3}
\]

which satisfy the physical intertwining identity

\[
 \boxed{B\theta_D=\theta_LB.}                             \tag{1.4}
\]

Equation (1.4) is the literal `DIH-A18-COMP` requirement.  It is not
inferred from an abstract isomorphism of endpoint modules.  In particular,
\(\theta_D\) must preserve the complete legal source and \(\theta_L\) must
act after the same occurrence owner and aggregation as \(B\).

Because \(2\) is invertible in \(k\), put

\[
 P_-={1\over2}(1-\theta_D),
 \qquad P_+={1\over2}(1+\theta_D).                         \tag{1.5}
\]

These are complementary idempotents on \(D^{\rm rel}\).  Over
\(\mathbf F_3\), their literal formulas are

\[
 \boxed{P_-=2(1-\theta_D),
 \qquad P_+=2(1+\theta_D).}                               \tag{1.6}
\]

Thus applying either projector needs only the original instruction and its
dihedral partner; no averaging denominator is hidden.

## 2. Splitting the commutator into its two actual preimages

Let \(x\) be one literal, occurrence-tagged commutator instruction whose
evaluated class

\[
 c=c(x)\in D^{\rm rel}                                    \tag{2.1}
\]

is legal.  The exact crossed-Fox expansion, transported separately through
all occurrences, gives the v398 identity

\[
 \boxed{Bc=V+K,}                                          \tag{2.2}
\]

where \(V\) is the value term and \(K\) is the complete same-depth
connection term.  For a nested commutator, \(K\) denotes the full iterated
connection sum, not only its last summand.

Assume the actual parity equalities

\[
 \boxed{\theta_LV=-V,
 \qquad \theta_LK=K.}                                     \tag{2.3}
\]

### Theorem 2.1 (DIHEDRAL SPECTRAL COMMUTATOR SPLIT)

Under (1.4) and (2.3), define

\[
 \boxed{
 d_V=P_-c={1\over2}(c-\theta_Dc),
 \qquad
 d_K=P_+c={1\over2}(c+\theta_Dc).}                        \tag{2.4}
\]

Then both corrections are legal and relative, and

\[
 \boxed{Bd_V=V,
 \qquad Bd_K=K,
 \qquad c=d_V+d_K.}                                       \tag{2.5}
\]

In characteristic three this is the completely explicit formula

\[
 \boxed{
 d_V=2(c-\theta_Dc),
 \qquad d_K=2(c+\theta_Dc).}                              \tag{2.6}
\]

#### Proof

The involution preserves \(D^{\rm rel}\), so both expressions in (2.4)
belong to the legal relative source.  Equations (1.4), (2.2), and (2.3)
give

\[
 \begin{aligned}
 Bd_V
 &=\frac12\bigl(Bc-B\theta_Dc\bigr)\\
 &=\frac12\bigl((V+K)-\theta_L(V+K)\bigr)\\
 &=\frac12\bigl((V+K)-(-V+K)\bigr)=V,                   \tag{2.7}
 \end{aligned}
\]

and similarly

\[
 Bd_K
 =\frac12\bigl((V+K)+(-V+K)\bigr)=K.                   \tag{2.8}
\]

Finally \(P_-+P_+=1\), proving the last identity in (2.5).  Formula (2.6)
uses \(2^{-1}=2\) in \(\mathbf F_3\). \(\square\)

This theorem supplies the value lift assumed in v398 Theorem 2.1 and, at
the same time, supplies the resulting connection lift.  Indeed v398's
subtraction is

\[
 c-d_V=d_K.                                                \tag{2.9}
\]

The return-even nature of \(K\) is therefore not a reason for failure of
the dihedral route.  The antisymmetrizer extracts \(V\), while the
complementary symmetrizer extracts \(K\).  What would fail is discarding
\(K\) and applying only \(1-\theta\) to the total residual.

## 3. A finite roster and the class-specific selector

Let \(X^{\rm rel}\) be the free space on a finite registered roster of
legal literal commutator instructions, and suppose (2.2)--(2.3) hold
linearly for every vector in that roster.  Define

\[
 s_V=P_-c:X^{\rm rel}\to D^{\rm rel},
 \qquad
 s_K=P_+c:X^{\rm rel}\to D^{\rm rel}.                    \tag{3.1}
\]

Then

\[
 Bs_V=V,
 \qquad Bs_K=K.                                            \tag{3.2}
\]

For one named \(\chi_{07}\) instruction history, (3.1) is already the
closed-form selector: its literal ancestry is the pair
\((c(x),\theta_Dc(x))\).  No target-basis choice is needed.

If a right inverse is required on every vector in \(V(X^{\rm rel})\) or
\(K(X^{\rm rel})\), (3.1) need not descend through relations among target
vectors.  Choose a target basis and one preimage instruction for each basis
vector, exactly as in v397.  Equations (3.1)--(3.2) then give a
word-bearing pivot section without demanding equality of source and target
relation modules.

The actual parity test can be made without separately constructing \(V\)
and \(K\) as abstract modules.  Replay \(Bc\), replay
\(B\theta_Dc\), and require the literal Fox decomposition to satisfy

\[
 \boxed{Bc=V+K,
 \qquad B\theta_Dc=-V+K.}                                 \tag{3.3}
\]

Adding and subtracting (3.3) then emits the two columns (2.6).  An abstract
candidate saying that one field-outer line is return-even is not a
substitute for this actual replay.

## 4. Compatibility through every refinement

Suppose now that the registered cofinal tower carries compatible
involutions

\[
 r_D\theta_{D,n+1}=\theta_{D,n}r_D,
 \qquad
 r_L\theta_{L,n+1}=\theta_{L,n}r_L                       \tag{4.1}
\]

and that the literal instruction history
\(c=(c_n)\), its Fox split \((V_n,K_n)\), and (1.4), (2.3) all reduce
compatibly.  Define

\[
 d_{V,n}=2(c_n-\theta_{D,n}c_n),
 \qquad
 d_{K,n}=2(c_n+\theta_{D,n}c_n).                          \tag{4.2}
\]

### Theorem 4.1 (ONE ALL-REFINEMENT SPECTRAL SELECTOR)

The families \(d_V=(d_{V,n})\) and \(d_K=(d_{K,n})\) are compatible legal
relative corrections and satisfy

\[
 \boxed{Bd_V=V,
 \qquad Bd_K=K}                                            \tag{4.3}
\]

in the inverse limit.  Thus the paired odd/even Fox history is corrected at
all refinements by one formula, not by independently selected finite-stage
solutions.

#### Proof

Theorem 2.1 applies at each coordinate.  Equation (4.1) makes both formulas
in (4.2) commute with reduction, so their coordinatewise solutions define
the two inverse-limit corrections. \(\square\)

This theorem does not assert that every future residual is of the paired
form (2.2), or that (2.3) holds automatically at a new chief factor.  Its
uniform input is the literal commutator materialization and the same typed
dihedral parity identity at every active layer.

## 5. Consequence for the current R07 proof plan

V398 reduced the connection problem to an actual value lift.  Theorem 2.1
reduces that value lift further:

\[
 \boxed{
 \begin{matrix}
 \text{legal literal commutator }c,\\
 B\theta_D=\theta_LB,\\
 \theta_LV=-V,\ \theta_LK=K
 \end{matrix}
 \Longrightarrow
 \begin{matrix}
 d_V=2(c-\theta_Dc),\\
 d_K=2(c+\theta_Dc).
 \end{matrix}}                                            \tag{5.1}
\]

Accordingly, the next actual finite certificate is smaller than a full
connection-homotopy solve.  It needs:

1. an A4-owned legal word-bearing commutator instruction and its dihedral
   partner;
2. direct legality and relative-kernel replay for both instructions;
3. direct actual-operator equivariance replay (1.4);
4. the two literal residual equalities (3.3); and
5. reduction compatibility of these data.

If those clauses hold for the recursively generated \(\chi_{07}\) history,
the odd value and even field-outer connection corrections are both explicit
at every depth.  The initial base defect still has to enter this instruction
history; that is the separate A0 actual membership gate.

```text
ODD/EVEN PROJECTORS IN CHARACTERISTIC THREE:       PAPER PROOF
ACTUAL COMMUTATOR -> VALUE AND CONNECTION LIFTS:   PAPER PROOF / TYPED PARITY CONDITIONAL
INDEPENDENT VALUE MATRIX SOLVE FOR PAIRED HISTORY: NOT NEEDED IF ACTUAL PARITY PASSES
INDEPENDENT CONNECTION HOMOTOPY:                   NOT NEEDED IF ACTUAL PARITY PASSES
ACTUAL DIH-A18 EQUIVARIANCE:                       OPEN
ACTUAL VALUE-ODD / CONNECTION-EVEN REPLAY:         OPEN
LEGAL A4 COMMUTATOR/PARTNER WORDS:                 OPEN
ALL-DEPTH REDUCTION COMPATIBILITY:                 OPEN
INITIAL A0 ACTUAL CLASS:                           RUNNING
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:        NOT CONSTRUCTED
```

`R07_DIHEDRAL_SPECTRAL_COMMUTATOR_SPLIT_V399_PAPER_GRADE`
