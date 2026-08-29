# R07 C_rel eleven-occurrence chain closure v370

Author: Sol / 2026-08-30

Status: paper identification of the physical task395 map after v357, v367,
v368 and v369.  It fixes the eleven base prefixes, signs, simultaneous left
action, and exact finite closure theorem.  It neither supplies the future
positive task382 basis nor computes its closure.  The strict localized
target, leading surjectivity, nonlinear recursion and every non-pro-3 gate
remain open.  No compatible lift, fake certificate or Ihara witness is
declared.  `verified=false`.

## 1. The chain map, not the endpoint map

Let \(F_0=g_{760}\).  For the eleven frozen task198 occurrences write

\[
 (B(o),\rho_o,t(o),\sigma_o),\qquad 1\leq o\leq11,
\tag{1.1}
\]

for the block, substitution, ten-context index and factor sign.  Put

\[
 r_o=\rho_o(F_0),\qquad
 Q_o=\prod_{j\in\operatorname{pref}(o)}r_j^{\sigma_j},
\tag{1.2}
\]

where the product uses the literal `fox_prefix_occurrences` order, and put

\[
 P_o=\begin{cases}
 Q_or_o,&\sigma_o=1,\\
 Q_o,&\sigma_o=-1.
 \end{cases}
\tag{1.3}
\]

The frozen roster is

| \(o\) | occurrence / type | \(t(o)\) | \(\sigma_o\) | prefix ordinals |
|---:|---|---:|---:|---|
| 1 | H1_fxy / PB3 | 0 | +1 | 3, 2 |
| 2 | H1_fxz / PB3 | 1 | -1 | 3 |
| 3 | H1_fyz / PB3 | 2 | +1 | empty |
| 4 | H2_fux / PB3 | 3 | -1 | 6, 5 |
| 5 | H2_fxy / PB3 | 0 | -1 | 6 |
| 6 | H2_fuy / PB3 | 4 | +1 | empty |
| 7 | P_b1 / PB4 | 5 | +1 | 11, 10, 9, 8 |
| 8 | P_b2 / PB4 | 6 | +1 | 11, 10, 9 |
| 9 | P_b3 / PB4 | 7 | +1 | 11, 10 |
| 10 | P_b5_inverse / PB4 | 8 | -1 | 11 |
| 11 | P_b4_inverse / PB4 | 9 | -1 | empty |

Thus an empty prefix list does not make \(P_3\) or \(P_6\) the identity:
\(P_3=r_3\) and \(P_6=r_6\).  Conversely \(P_{11}=1\).

Let \(\delta\) be the retained left-Fox one-chain.  If \(c\) is a relative
seed whose every \(\rho_o(c)\) has value one in the retained coefficient
quotient, define the separately tagged column

\[
 \boxed{
  \widehat B(c-1)_o
   =\sigma_oP_o\,\delta(\rho_o(c)).}
\tag{1.4}
\]

The coordinate key is the full tuple

\[
 (B(o),o,\operatorname{type}(o),a,z),
\tag{1.5}
\]

where \(a\) is the Fox component and \(z\) the marked PB3 or PB4 group
element.  In particular, (1.4) is the component-bearing chain map of v357;
it is not v214's endpoint-only action on a fixed vector.

### Lemma 1.1 (SIGNED PREFIX FORMULA)

Formula (1.4) is the literal first difference of the H1, H2 and printed
pentagon products at the base \(F_0\).

#### Proof

In a positive slot the perturbed factor is
\(\rho_o(F_0)\rho_o(c)\).  The Fox product rule places the new chain after
the preceding factor product, giving
\(Q_or_o\delta(\rho_o(c))=P_o\delta(\rho_o(c))\).

In a negative slot the perturbed factor is
\((\rho_o(F_0)\rho_o(c))^{-1}\).  Since \(\rho_o(c)=1\) in the retained
coefficient quotient,
\(\delta(\rho_o(c)^{-1})=-\delta(\rho_o(c))\).  Its contribution is
therefore
\(-Q_o\delta(\rho_o(c))=\sigma_oP_o\delta(\rho_o(c))\).  Thus one must not
both invert the correction chain and multiply by the stored negative sign.
Summing the literal slots proves the assertion. \(\square\)

The literal \(g_{760}\) word, or its evaluated values \(r_o\), is
load-bearing input.  Prefix ordinals alone do not determine
(1.2)--(1.3).  The current frozen source is
`search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py`, 33,409
bytes, SHA-256
`f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f`;
its `construct_base()[2]` must have length 760 and canonical word digest
`518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`.
Failure of this authentication is `UNKNOWN_INPUT`, not a zero column.

## 2. The simultaneous left action

For a source word \(g\), define the occurrence actor

\[
 A_o(g)=P_o\rho_o(g)P_o^{-1}.
\tag{2.1}
\]

It acts on a tagged Fox coordinate by left multiplication of its group
element:

\[
 (o,a,z)\longmapsto(o,a,A_o(g)z).
\tag{2.2}
\]

### Lemma 2.1 (ACTION--ANCESTRY COMPATIBILITY)

For every relative seed \(c\),

\[
 g\cdot\widehat B(c-1)
 =\widehat B\bigl(g(c-1)\bigr),
\tag{2.3}
\]

and its \(o\)-th component is

\[
 \sigma_oP_o\rho_o(g)\delta(\rho_o(c)).
\tag{2.4}
\]

Consequently applying a generator \(h\) to ancestry \(g(c-1)\) replaces
its action word by \(hg\), not by \(hgh^{-1}\).

#### Proof

By (2.1), the left side of (2.3) at occurrence \(o\) is

\[
 P_o\rho_o(g)P_o^{-1}
 \bigl(\sigma_oP_o\delta(\rho_o(c))\bigr),
\]

which is (2.4).  The group-algebra identity
\(h\,g(c-1)=(hg)(c-1)\) gives the last assertion. \(\square\)

There is also a word-pair replay which does not trust the sparse action:

\[
 \widehat B\bigl(g(c-1)\bigr)_o
 =\sigma_oP_o\left(
   \delta(\rho_o(gc))-\delta(\rho_o(g))\right).
\tag{2.5}
\]

Since \(\rho_o(c)=1\), the Fox rule reduces (2.5) to (2.4).
Equivalently, the literal conjugate \(gcg^{-1}\) has retained derivative
\(\rho_o(g)\delta(\rho_o(c))\).  Aggregating the eleven tagged rows by the
H1/H2/P block therefore equals the direct base-versus-corrected replay for
\(F_0(gcg^{-1})\).  These are two replay routes for the same column, not
two definitions which may be mixed slot by slot.

## 3. Why exhausted generator closure is exactly \(W_C\)

Let \(c_1,\ldots,c_r\) be the future authenticated task382 basis of
\(C_{\rm rel}\), and let \(V_{\rm raw}\) be the finite separately tagged
Fox chain space (1.5) at the registered first edge.  Put

\[
 I_{\rm rel}=\sum_{i=1}^r\mathbf F_3[\Delta_1](c_i-1),
 \qquad
 W_C=\operatorname{im}
 \left(\widehat B\vert_{I_{\rm rel}}\right).
\tag{3.1}
\]

### Theorem 3.1 (FINITE GENERATOR CLOSURE)

Start with all columns (1.4), insert nonzero rank rises into a sparse
\(\mathbf F_3\)-echelon, and repeatedly apply the simultaneous actions of
\(x,x^{-1},y,y^{-1}\) to every retained rank-raising row.  If the queue is
exhausted without a resource stop, the resulting span is exactly \(W_C\).
This includes the case \(r=0\), when both spans are zero.

#### Proof

The output span contains every seed column.  Queue exhaustion makes it
stable under the four marked generators, hence under the group they generate
and therefore under \(\mathbf F_3[\Delta_1]\).  It consequently contains
the right side of (3.1).  Conversely, every row ever inserted is obtained
from seed columns by the actions (2.1)--(2.2) and
\(\mathbf F_3\)-linear echelon operations, so it belongs to \(W_C\).
Both inclusions give equality. \(\square\)

The theorem requires no enumeration of all \(\Delta_1\) states.  A complete
certificate consists of the eleven structural coordinate descriptors, the
ordered active coordinate roster actually reached, all seed columns, and
the full rank/queue/action/ancestry/reduction transcript.  A cap reached
before queue exhaustion is `UNKNOWN_RESOURCE`; it is not a smaller invariant
closure and not negative evidence.

## 4. Exact claim boundary

Task395 may use Theorem 3.1 only after authenticating the positive task382
producer and independent verdict, including their physical A4/task198
owners, queue exhaustion, complete \(C_{\rm rel}\) basis, literal
commutator/value replay, echelon rank and two-way span certificate.  Its
independent checker must reconstruct (1.2)--(2.5) through independent Fox
arithmetic, rather than copy a producer row or repeat the same parser.

Even a positive task395 receipt computes only the raw first-edge image
\(W_C\).  It does not identify the strict localized quotient \(L/JL\),
prove that \(W_C\to L/JL\) is onto, establish the affine/nonlinear depth
laws, or solve settlement, mixed-prime or perfect-core gates.

```text
ELEVEN CHAIN PREFIX/SIGN FORMULA:                  PAPER PROOF
SIMULTANEOUS LEFT ACTION / hg ANCESTRY:            PAPER PROOF
EXHAUSTED FOUR-GENERATOR CLOSURE = W_C:            PAPER PROOF
POSITIVE TASK382 C_rel BASIS:                      FUTURE INPUT
ACTUAL W_C RANK / BASIS:                           NOT COMPUTED
STRICT L/JL / LEADING ONTO:                        OPEN
DEPTHWISE NONLINEAR REPLAY:                        OPEN / CONDITIONAL
COMPATIBLE LIFT / FAKE / IHARA WITNESS:            NOT CONSTRUCTED
```

`R07_CREL_ELEVEN_OCCURRENCE_CHAIN_CLOSURE_V370_PAPER_GRADE`
