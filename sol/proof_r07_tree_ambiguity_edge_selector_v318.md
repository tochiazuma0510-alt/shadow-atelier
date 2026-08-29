# R07 rooted-tree ambiguity edge selector (v318)

Author: Sol / 2026-08-29

Status: paper theorem refining v317.  Once the actual common-source image is
an authenticated tree fibre product, it reduces the remaining quotient-valued
marginal problem to one local ambiguity map at each non-root vertex.  Local
right inverses give an explicit top-down selector, and natural right inverses
give the same selector simultaneously on a cofinal tower.  The actual
seven-context tree presentation and its local edge maps have not been
authenticated or computed.  No lift, fake certificate, or Ihara witness is
declared.

## 1. Rooted edge equations

Retain the tree data of v317.  Choose a root \(r\).  For every non-root
vertex \(v\), write \(p(v)\) for its parent and \(e_v=\{p(v),v\}\) for its
parent edge.  Put

\[
 E_v=k[D_{e_v}],
\qquad
 q_v=(\pi_{v,e_v})_*:k[G_v]\longrightarrow E_v,
\tag{1.1}
\]

and write

\[
 \bar q_v=q_v|_{U_v}:U_v\longrightarrow E_v
\tag{1.2}
\]

for the pushforward of the local ambiguity space.  The parent occurrence on
the same edge is denoted

\[
 q_{p(v),v}
   =(\pi_{p(v),e_v})_*:k[G_{p(v)}]\longrightarrow E_v.
\tag{1.3}
\]

Choose one representative \(a_v\in k[G_v]\) of every prescribed local class
\(\alpha_v\in Q_v=k[G_v]/U_v\).  We seek \(u_v\in U_v\) such that the adjusted
representatives \(a_v+u_v\) agree on every edge.  If the parent correction
has already been chosen, the required parent-edge target at \(v\) is

\[
 \boxed{
 d_v(u_{p(v)})=
 q_{p(v),v}(a_{p(v)}+u_{p(v)})-q_v(a_v)\in E_v.}
\tag{1.4}
\]

The edge equation is exactly

\[
 \boxed{\bar q_v(u_v)=d_v(u_{p(v)}).}
\tag{1.5}
\]

There is no equation involving a descendant correction in (1.5).  This
triangularity is the gain supplied by rooting a tree.

## 2. The top-down selector

For each non-root vertex let \(D_v\leq E_v\) be a registered subspace and
suppose a linear word-bearing right inverse is given:

\[
 h_v:D_v\longrightarrow U_v,
\qquad
 \bar q_vh_v=1_{D_v}.
\tag{2.1}
\]

### Theorem 2.1 (ROOTED AMBIGUITY SELECTOR)

Choose \(u_r\in U_r\).  Process vertices in any order in which every parent
precedes its children.  Whenever the value (1.4) lies in \(D_v\), define

\[
 \boxed{u_v=h_v(d_v(u_{p(v)})).}
\tag{2.2}
\]

If every step is defined, then

\[
 \mu_v=a_v+u_v
\tag{2.3}
\]

belongs to v317's edge-compatible space \(C_T\), represents every prescribed
class \(\alpha_v\), and therefore gives the explicit common-source
coefficient

\[
 \boxed{\ell=G_T((\mu_v)_v).}
\tag{2.4}
\]

#### Proof

Equation (2.2) and (2.1) give

\[
 q_v(a_v+u_v)
 =q_v(a_v)+d_v(u_{p(v)})
 =q_{p(v),v}(a_{p(v)}+u_{p(v)}).
\tag{2.5}
\]

Thus the parent edge of \(v\) is compatible.  It is never changed later:
all later choices occur at descendants, and an edge has exactly one child
endpoint.  Induction over the rooted order proves compatibility on every
edge.  Since \(u_v\in U_v\), equation (2.3) retains the class \(\alpha_v\).
V317 Corollary 3.1 then gives (2.4). \(\square\)

### Corollary 2.2 (FULL LOCAL-EDGE SURJECTIVITY)

If

\[
 \boxed{\bar q_v(U_v)=E_v
 \quad\text{for every }v\ne r,}
\tag{2.6}
\]

choose any linear right inverses \(h_v:E_v\to U_v\) and put \(u_r=0\).
Then (2.2) is a linear selector for every tuple of quotient classes
\((\alpha_v)_v\).  In particular,

\[
 \mathcal R(\alpha)\cap C_T\ne\varnothing
\tag{2.7}
\]

for every \(\alpha\), and v317's global marginal membership is automatic.

#### Proof

Finite-dimensional surjectivity supplies the right inverses.  Condition
(2.6) makes every target (1.4) admissible, so Theorem 2.1 applies.  Every
operation is linear in the chosen representatives. \(\square\)

Condition (2.6) is sufficient and deliberately stronger than necessary.
Changing the root may replace a difficult map by the ambiguity map at the
other endpoint.  Even when no root makes every map onto, the actual-class
recursion can succeed because it only asks membership of the encountered
values (1.4).

### Proposition 2.3 (EXACT ACTUAL-CLASS FORM)

A representative tuple for \(\alpha\) exists if and only if there are a
root value \(u_r\in U_r\) and choices \(u_v\in U_v\), made top-down, which
satisfy (1.5) at every vertex.

#### Proof

Any such choices give a compatible tuple by the proof of Theorem 2.1.
Conversely, the ambiguity coordinates of any tuple in
\(\mathcal R(\alpha)\cap C_T\) satisfy (1.5) when read in rooted order.
\(\square\)

The proposition is not a claim that one fixed greedy choice is complete.
If a local map has a kernel, different preimages can change later targets.
A positive explicit branch retains its selected preimage ancestry; a
complete negative must eliminate all such choices, for example by one
global finite elimination or dynamic programming on the tree.

## 3. Exact local dual obstruction

At one non-root vertex, finite-dimensional duality gives

\[
 d_v\in\bar q_v(U_v)
 \quad\Longleftrightarrow\quad
 \lambda(d_v)=0
 \text{ for every }
 \lambda\in E_v^*
 \text{ with }\bar q_v^*\lambda=0.
\tag{3.1}
\]

For the prefix-corrected v313 ambiguity

\[
 U_v=\epsilon_vK_{r_v}p_v^{-1},
\qquad
 K_{r_v}=\ker(a\mapsto a(1-r_v)),
\tag{3.2}
\]

the annihilator in (3.1) has a literal orbit description.

### Lemma 3.1 (LOCAL OVERLAP DUAL)

Let \(\pi:G_v\twoheadrightarrow D\) be the parent-edge map.  A functional
\(\lambda\in k[D]^*\) annihilates
\(\pi_*(\epsilon_vK_{r_v}p_v^{-1})\) if and only if

\[
 \boxed{
 \sum_{g\in C}
 \lambda\!\left(\pi(gp_v^{-1})\right)=0}
\tag{3.3}
\]

for every right \(\langle r_v\rangle\)-orbit \(C\subseteq G_v\).

#### Proof

The scalar \(\epsilon_v\ne0\) does not change an annihilator.  As in v315,
\(K_{r_v}\) has one basis vector \(\sum_{g\in C}[g]\) for each right
\(\langle r_v\rangle\)-orbit.  Its translated image is
\(\sum_{g\in C}[gp_v^{-1}]\).  Pushforward by \(\pi\) and pairing with
\(\lambda\) gives exactly (3.3). \(\square\)

Consequently a local MEMBER receipt consists of one \(u_v\) with direct
replay of (1.5).  A local NONMEMBER receipt consists of a \(\lambda\)
satisfying every orbit equation (3.3) and

\[
 \lambda(d_v)\ne0.
\tag{3.4}
\]

Unlike a bounded failure of common-source column generation, (3.4) is a
complete obstruction for that fixed parent choice.  A global negative still
has to account for earlier kernel choices as stated after Proposition 2.3.

## 4. Return split

Assume a return involution \(\theta\) commutes with all edge maps and
preserves every \(U_v\).  Over \(k=\mathbf F_3\), put

\[
 e_-=(1-\theta)/2,\qquad e_+=(1+\theta)/2.
\tag{4.1}
\]

Then every equation (1.5) splits.  If the relative-dihedral theorem gives a
right inverse

\[
 h_{v,-}:D_{v,-}\longrightarrow e_-U_v
\tag{4.2}
\]

on the required odd targets, the only remaining condition at \(v\) is

\[
 \boxed{
 e_+d_v(u_{p(v)})\in
 \bar q_v(e_+U_v).}
\tag{4.3}
\]

One retained preimage \(h_{v,+}(e_+d_v)\) is enough for the actual branch,
and the correction is

\[
 u_v=h_{v,-}(e_-d_v)+h_{v,+}(e_+d_v).
\tag{4.4}
\]

Thus, conditional on the tree presentation, the class-specific second
homotopy is not one ambient map on the entire seven-context target.  It is a
top-down list of at most \(|V|-1\) return-even overlap preimages.  Each has
the explicit dual test of Lemma 3.1.

## 5. Natural cofinal tower

Let all data carry a level \(n\), with the cartesian tree system and natural
gluing maps of v317 Section 4.  Assume:

1. the representatives \(a_{v,n}\) reduce compatibly;
2. root corrections \(u_{r,n}\) reduce compatibly;
3. every ambiguity and edge map commutes with reduction; and
4. the local right inverses are natural on the registered targets:

   \[
   U_{v,n+1}\longrightarrow U_{v,n},
   \qquad
   h_{v,n+1}\longmapsto h_{v,n}.
   \tag{5.1}
   \]

### Theorem 5.1 (COFINAL ROOTED-EDGE SELECTOR)

The recursion (2.2) produces compatible adjusted representatives at every
vertex and level.  Composing it with the natural v317 gluing map gives one
compatible family

\[
 \boxed{
 \ell_n=
 G_{T,n}\bigl((a_{v,n}+u_{v,n})_v\bigr),}
\tag{5.2}
\]

and hence one completed common-source coefficient.

#### Proof

Induct first over levels at the root and then down the fixed rooted tree.
If the parent corrections reduce compatibly, naturality of the representatives
and edge maps makes the upper target (1.4) reduce to the lower target.
Naturality of \(h_v\) then makes the child corrections compatible.  This
proves compatibility of every adjusted representative.  V317 Theorem 4.1
proves compatibility of (5.2). \(\square\)

Full natural right inverses on every \(E_v\) are sufficient but not required.
For one R07 branch it is enough to register the recursively encountered
odd/even target subspaces and prove naturality there.

## 6. R07 application boundary

The executable order after A0/A3/A4 is now sharply separated:

1. authenticate whether the actual joint seven-context image has a tree
   fibre-product presentation, including all higher Goursat constraints;
2. choose a root and construct each exact map
   \(\bar q_v:U_v\to k[D_{e_v}]\);
3. on the odd part, bind the existing relative-dihedral section;
4. on the actual even part, run (3.1)--(3.4), retaining a preimage or a
   complete local dual;
5. materialize the glued coefficient through one common source section; and
6. replay the literal H1/H2/ordered pentagon and every side gate.

If the actual image is not a tree fibre product, none of Theorems 2.1 or 5.1
may be applied; v314--v316 remain the general fallback.  If it is a tree but
some full local map is not onto, that is not yet a branch obstruction: use
the pointed recursion and its actual pairings.

    ROOTED TREE MAKES EDGE ADJUSTMENTS TRIANGULAR:     PAPER PROOF
    LOCAL EDGE ONTO GIVES CLOSED GLOBAL SELECTOR:      PAPER PROOF
    PREFIX-TWISTED LOCAL DUAL ORBIT TEST:              PAPER PROOF
    NATURAL LOCAL SECTIONS GIVE COFINAL SELECTOR:      PAPER PROOF
    ACTUAL SEVEN-CONTEXT TREE PRESENTATION:            NOT ESTABLISHED
    ACTUAL LOCAL EDGE MAPS / RETURN-EVEN PAIRINGS:     NOT COMPUTED
    NONLINEAR / FORMATION / PERFECT-CORE GATES:        OPEN
    COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:    NONE

R07_TREE_AMBIGUITY_EDGE_SELECTOR_V318_PAPER_GRADE
