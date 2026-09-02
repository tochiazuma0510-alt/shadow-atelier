# Task 550 audit — affine engine, transition defects, and graded Fourier blocks

`verified=false`.  This is a mathematical/static audit.  The strongest new
machine status is **UNKNOWN**, for the coordination reason recorded below.

## 1. Preconditions, pins, and audit record

I read all eight commissioned inputs in full and also the final Task 548
reply.  Task 548 ends in
`EXPLICIT_G9_TWO_RUNG_TWISTING_PASS` and `verified=false`; it is not a STOP.
The byte pins are:

| input | bytes | SHA-256 |
|---|---:|---|
| v443 | 10,291 | `80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c` |
| v444 | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v445 | 9,670 | `98d073c896cae8304252327ea285b876f8868b6c2d00e8ba3c00465ea86612e7` |
| v442 | 8,710 | `afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4` |
| v441 | 11,696 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| Task 544 reply | 14,931 | `7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3` |
| v439 | 9,111 | `b18e27ac79f870a6bb5c104a12e85a95daf8644e080153305ce8447e3736f122` |
| Task 540 reply | 21,385 | `3114977ca62727296bf4c3980e405e920169a9c10b4bfdfa80f15990aac3a31d` |
| Task 548 reply | 14,448 | `bd1b0239e0410f2ab63abd30e7ff9a422528d141138cfeafc8ca3960da1cd834` |

The source-reading commands were PowerShell `Get-Content -Raw
-LiteralPath <path>` (and the same command with a line-numbering pipeline for
v443 and v444).  The finite-check command, from the repository root, was

```powershell
python "$env:TEMP\task550_affine_transition_fourier_audit_v1.py"
```

The first invocation exited 1 after 0.45 seconds at its first marked-inverse
pin: the temporary harness had named the two (A)-coordinates of (X) and
(Y) in the opposite order.  No theorem comparison had failed.  After the
parent authorized the narrow replacement
(X_A=(1,0),Y_A=(0,1)), the identical command completed with exit 0.  Its
temporary source had 15,949 bytes and SHA-256
`82752741e511122b5af41669824c48cad3037340ff69b40230672263dc531089`;
the canonical result payload SHA-256 was
`4b63f42d60867f93b7264fe908ff7dce2d92fc0de6e9042174274de8230fa031`.

That corrected run overlapped an unrelated local Python process which began
after the initial process-table clearance.  The stop instruction arrived
after this checker had naturally exited.  I did not touch the unrelated
process and made no further run.  Under the commissioned single-Python-slot
rule I record the corrected run as **coordination-interrupted / independence
UNKNOWN**.  Its output is preserved below as candidate telemetry only and is
not a premise for the verdict:

```text
split products                         11,664
split inverse sides                       216
carry products                         11,664
carry cocycle triples                1,259,712
occurrence carries                     17,496
action/intertwining identities          17,496
crossed-cochain identities                  96
exact signed substitutions                 162
Fox words of length <= 4                   341
```

The ruling below instead follows from the explicit derivations and tiny
counterexamples in Sections 2--6.

## 2. v443 split arithmetic — PASS

Write an element as (sigma(q)n(v)), with (q=(p,a)).  In the frozen
right-action convention,

[
 (v,a)star(w,b)=(S(b)v+w,a+b).
]

Consequently the parity of the **right** factor, not the left factor, acts
on the left kernel coordinate, and direct expansion gives

[
 (sigma(q)n(v))(sigma(q')n(w))
 =sigma(qq')n(S(b)v+w).
]

Linearity in (E(v)) gives exactly v443 (2.4),

[
 ([p,a]f)([p',b]g)
 =[pp',a+b],\rho_b(f)g,qquad
 \rho_b(E(v))=E(S(b)v).
]

Solving both (gg^{-1}=1) and (g^{-1}g=1) gives
((q,v)^{-1}=(q^{-1},-S(a)v)).  With
(S(s_X)=\operatorname{diag}(1,-1,-1)) and
(S(s_Y)=\operatorname{diag}(-1,1,-1)), this yields

[
v_X=(1,0,0),quad v_Y=(1,1,1),quad
v_{X^{-1}}=(-1,0,0),quad v_{Y^{-1}}=(1,-1,1),
]

so (2.5)--(2.7) are correct.

For a left actor (ell=sigma(q_ell)n(v_ell)), the row quotient parity
(a) is the right parity in the product.  Hence

[
L_ell([q]f)=[q_ell q]E(S(a)v_ell)f,
]

which is (3.1).  Likewise
(alpha_j(sigma(p,a)n(v))) has quotient
((alpha_j^P(p),A_ja)) and kernel
(M_jv+c_j(a)).  This is precisely (3.2); its validity uses

[
c_j(a+b)=S(A_jb)c_j(a)+c_j(b),qquad
M_jS(a)=S(A_ja)M_j.
]

No left/right reversal or missing crossed term occurs.

The polynomial substitution is also exact through degree six.  If
(M_je_i=epsilon_i e_{pi(i)}), then

[
u_i\longmapsto
\begin{cases}
u_{pi(i)},&epsilon_i=1,\\
2u_{pi(i)}+u_{pi(i)}^2,&epsilon_i=-1.
\end{cases}
]

This is the exact image of (t_i-1) in
(mathbf F_3[C_3^3]), not a linear approximation, and preserves the
truncation ideal.  Thus (1.1)--(1.4), (2.2)--(2.7), and (3.1)--(3.2) pass.

## 3. v443 carry arithmetic, Fox convention, and dimensions — PASS

Represent an upstairs rotation by
(d(\bar r)+3k), with section-left/kernel-right coordinates
((q,k)), (q=(p,\bar r,a)).  Multiplying two such representatives gives

[
q q'=(pp',S(b)\bar r+\bar s,a+b),qquad
k_new=S(b)k+l+\omega(q,q'),
]

where the integer digit discrepancy divided by three is exactly (4.4).
This proves (4.3)--(4.5) and again shows that the right parity (b) acts.
Putting the actor on the left makes the row parity (a) the right parity,
so its kernel contribution is
(S(a)k_ell+\omega(q_ell,q)), exactly (4.6).

The actual inverse rotations are (8) in (X)'s first coordinate and
((1,8,1)) for (Y^{-1}).  Relative to digit representatives (2) and
((1,2,1)), their kernel carries are therefore

[
k_{X^{-1}}=(2,0,0),qquad k_{Y^{-1}}=(0,2,0),
]

as in (4.7).

For occurrences, direct decomposition of

[
M_j(d(\bar r)+3k)+c_j(a)
]

into its new digit section and a multiple of three gives (4.8), (4.9), and

[
\alpha_j([q]f)=[\bar\alpha_j(q)]
 E(\kappa_j(\bar r,a))\phi_{M_j}(f),
]

so (4.10) has neither a missing carry nor a wrong sign.  The corresponding
right-action cocycle identity is

[
S(c)\omega(q,q')+\omega(qq',q'')
=\omega(q,q'q'')+\omega(q',q''),
]

and the occurrence compatibility follows by applying the same unique digit
decomposition to a product.

The Fox rule in Section 5 is consistent with this product convention:
(partial(uv)=partial u+upartial v), while a negative letter contributes
(-wx^{-1}) after updating the prefix.  Hence “positive: add then multiply”
and “negative: multiply then subtract” are correct.  All six tags remain
separate until fixed prefixes and aggregation, and normalized exponent and
PB3 auxiliary coordinates remain present.

The coefficients of ((1+t+t^2)^3) are
((1,3,6,7,6,3,1)), with cumulative dimensions

[
H_d=(1,4,10,17,23,26,27).
]

Multiplication by (12|Q_1|=24,192) and (4|Q_1|=8,064) gives exactly

```text
d                    0       1        2        3        4        5        6
occurrence        24192   96768   241920   411264   556416   628992   653184
physical           8064   32256    80640   137088   185472   209664   217728
```

For (|Q_2|=54,432), (H_1=4) gives
2,612,736/870,912, and (H_6=27) gives
17,635,968/5,878,656.  These are ambient dimensions only.

There are two harmless source-control-character typos: the prose after v443
(4.1) should read `\bar r`, and the prose after v445 (3.2) should read
`\varepsilon_j(\alpha)`.  The displayed defining formulas are unambiguous.

## 4. v444 transition-defect theorem — PASS

Let (L=\operatorname{span}\{\widetilde b_i\}) and let (H_d) be (3.3).
This proof does not use the proof printed in v444.

First, literal ancestry gives (widetilde b_i\in U_{d+1}).  Each seed or
transition defect is a linear combination of legal upstairs orbit vectors,
and equivariance of reduction puts it in (ker r_d).  Since (U_{d+1}) is
(Gamma)-stable, (L+H_d\subseteq U_{d+1}).

Conversely, (3.1) puts every upstairs seed in (L+H_d).  Formula (3.2)
puts every registered generator image of every (widetilde b_i) there, and
the definition of (H_d) makes (H_d) generator-stable.  Thus (L+H_d)
is a stable subspace containing all seeds, so it contains the complete legal
orbit (U_{d+1}).  Finally, if
(sum c_i\widetilde b_i\in H_d\subseteq\ker r_d), reduction gives
(sum c_i b_i=0).  Since (B_d) is a basis, every (c_i=0).  The sum is
direct and

[
U_{d+1}=L\oplus H_d,qquad
\dim U_{d+1}-\dim U_d=\dim H_d.
]

Two tiny filtered examples show why both kinds of defect are substantive.

* **Dependent seed.**  Let
  (r:\mathbf F_3^2\to\mathbf F_3), (r(x,z)=x), with trivial actor.
  Downstairs take (s_1=s_2=1) and basis (b=s_1); upstairs take
  (widetilde s_1=(1,0)), (widetilde s_2=(1,1)).  Then
  (epsilon_2=(0,1)), and
  (operatorname{span}\{(1,0),\epsilon_2\}=\mathbf F_3^2=U_1).
  Omitting seed defects leaves rank one.
* **Dependent actor edge.**  On the same reduction let the downstairs actor
  be the identity and let the upstairs actor be
  (A(x,z)=(x,z+x)), of order three.  With seed and lift (b=(1,0)), the
  old transition is (Ab=b), but
  (delta_A=A\widetilde b-\widetilde b=(0,1)).  The upstairs orbit has rank
  two and is exactly the old lift plus the closure of this defect.

Thus a producer must account for every registered actor transition.  Since
the actors occur with their inverses, some inverse-transition defects can be
algebraically derived from a complete positive transition matrix; v444's
safer certificate requirement to store and replay all four tables is correct
and makes no minimality claim.

Closing only in (ker r_d) is sufficient because this kernel is
(Gamma)-stable and the transition defects supply precisely the missing
stability of (L).  It is essential that the hatted reduced module include
normalized exponent, PB3 central augmentation, and every occurrence tag;
otherwise “in the kernel” would not imply pure new grade and the
associated-grade closure would be unjustified.  Inverse actors are ordinary
members of the four-generator source action.  Semilinear occurrences are
already encoded in the six-tag occurrence module.  No action on the
aggregated physical module is used or needed.

## 5. v444 physical-fibre interface — PASS

Let (F_{d+1}) denote the full occurrence-to-physical map, including
occurrence transport, prefixes, PB3 normalization, and aggregation.  Since

[
U_{d+1}=\operatorname{span}\{\widetilde b_i\}\oplus H_d,
]

the images of the lifted old basis together with an exhausted basis of
(H_d) span the entire physical image.  Lower-first echelonization of this
spanning roster computes exactly
(F_{d+1}(U_{d+1})\cap\ker(\text{physical reduction})), which is v441's
complete fibre.

Physical dependencies among old lifts can expose grade directions absent
from (F(H_d)).  A minimal model has physical coordinates
((\ell\mid g_1,g_2)) and two lifted old rows

[
r_1=(1\mid1,0),qquad r_2=(1\mid0,1).
]

Their lower parts agree, but
(r_1-r_2=(0\mid1,2)) is a nonzero grade connection supported in two grade
blocks, even if (H_d=0).  This proves both that v444 correctly retains the
lifted old basis and that a pure-defect-only physical solve can be false.
Closing aggregated rows under guessed actors is still prohibited: the legal
action is the correlated pre-aggregation source action, while occurrence
semilinearity and fixed prefixes prevent a single inherited physical action.

## 6. v445 Fourier arithmetic and the load-bearing source-splitting defect

### 6.1 Correct formulas and exact degree-one transport

For (A=C_2^2), the primitive idempotent is normally
(|A|^{-1}\sum_a\lambda(a)^{-1}[a]).  In (mathbf F_3), (4=1), every
element and every character value is self-inverse, and therefore

[
e_\lambda=\sum_{a\in A}\lambda(a)[a].
]

The four (e_\lambda) are normalized, mutually orthogonal, sum to one, and
give (1.5).

On associated grade (d), every positive term of
(E(S(a)v_\ell)) raises degree, so the actor reduces to quotient left
translation and preserves each character and monomial coordinate.  Under an
occurrence,

[
e_\lambda\mapsto e_{\lambda\circ A_j^{-1}},qquad
u^\alpha\mapsto
\left(\prod_i\epsilon_{j,i}^{\alpha_i}\right)u^{\pi_j\alpha}.
]

The inverse on the character is essential.  The crossed factor and an
actor/prefix kernel factor have constant term one on a pure associated grade;
their positive and quadratic terms are nevertheless retained when a lower
row is reevaluated one precision higher.

Put
(eta_1=(0,1)), (eta_2=(1,0)), (eta_3=(1,1)), where (eta_i) is
the sign character of kernel coordinate (i).  Intertwining implies that
both labels in ((\eta_a,i)) are moved by the same permutation.  In tag
order (j=0,\ldots,5), the six permutations are

[
1,quad(23),quad(123),quad(132),quad1,quad(13).
]

For an explicit twelve-pair enumeration, write (0i=(\mathbf1,i)) and
(ai=(\eta_a,i)).  Each row lists its six tag images:

| source | (j0) | (j1) | (j2) | (j3) | (j4) | (j5) |
|---|---|---|---|---|---|---|
| 01 | 01 | 01 | 02 | 03 | 01 | 03 |
| 02 | 02 | 03 | 03 | 01 | 02 | 02 |
| 03 | 03 | 02 | 01 | 02 | 03 | 01 |
| 11 | 11 | 11 | 22 | 33 | 11 | 33 |
| 12 | 12 | 13 | 23 | 31 | 12 | 32 |
| 13 | 13 | 12 | 21 | 32 | 13 | 31 |
| 21 | 21 | 31 | 32 | 13 | 21 | 23 |
| 22 | 22 | 33 | 33 | 11 | 22 | 22 |
| 23 | 23 | 32 | 31 | 12 | 23 | 21 |
| 31 | 31 | 21 | 12 | 23 | 31 | 13 |
| 32 | 32 | 23 | 13 | 21 | 32 | 12 |
| 33 | 33 | 22 | 11 | 22 | 33 | 11 |

The pure coordinate-transport orbits are exactly

[
\{01,02,03\},qquad
\{11,22,33\},qquad
\{12,13,21,23,31,32\}.
]

Thus the structural (3+3+6) partition and candidate physical widths
(6,048+6,048+12,096=24,192) are correct.  They do not by themselves give
three independent complete-fibre solves.  The lower-row example in Section 5
also directly validates the need to union two pure components when a
connection row meets both.

### 6.2 Defect: invariant monomial summands need not split the legal module

The inference in v445 Section 2 from ambient block invariance to an
independent closure in all (4h_d) character--monomial blocks is false in
general.  An invariant direct-sum decomposition of the ambient module does
not imply that a generated submodule contains the coordinate projections of
its generators.

A two-coordinate counterexample already occurs with a trivial
(Gamma)-action.  Let the two invariant summands be
(W u_1\oplus W u_2), take (0\ne w\in W), and let the sole defect be

[
d=w u_1+w u_2.
]

Then the legal closure is (H=\mathbf F_3d), of rank one.  Routing the two
homogeneous components independently inserts (w u_1) and (w u_2), whose
span has rank two.  This is exactly the situation not excluded by v444:
seed and transition defects can have several degree-(d) monomials, while
the associated-grade kernel subgroup acts trivially on the monomial
multiplicity space.  The bad split can therefore enlarge the legal source
space and produce a false MEMBER.  Physical connection hyperedges added
only for lifted old rows do not repair a source-space enlargement that has
already occurred in (H_d).

Accordingly, these statements of v445 are load-bearing and cannot be adopted
as written:

* “close independently in the (4h_d) source blocks” in Section 2;
* routing every homogeneous defect component as an independent legal row in
  implementation step 3;
* the assertion that every pure defect row is automatically confined to one
  pure transport component; and
* the resulting claim that old-row connection hyperedges alone make the
  complete graph sufficient.

### 6.3 Exact local repair

The character splitting *is* legal, not merely ambient invariance.  The
marked source actors generate (Q_1=P\times A), hence actor words include
every pure element ((1,a)).  Since (H_d) is stable under those
translations,

[
e_\lambda h=\sum_{a\in A}\lambda(a)L_{(1,a)}h\in H_d.
]

Orthogonality of the (e_\lambda) therefore proves the genuine decomposition

[
H_d=\bigoplus_{\lambda\in\widehat A}e_\lambda H_d.
]

There is no analogous actor-algebra projector onto an individual monomial.
The strongest paper-justified source decomposition is consequently four
character blocks with all (h_d) monomials coupled.  At degree one each has

[
3\cdot6\cdot2\cdot504=18,144
]

occurrence coordinates, and the four blocks total (72,576).  At degree
(d), replace (3) by (h_d).  A finer monomial split is permitted only
after an actual certificate proves that the computed defect module is closed
under those coordinate projections.

For a graph implementation, retain each exact character-projected defect as
one coupled row, close it without separating monomials, and add a support
hyperedge for every actual retained pure-defect physical row that meets more
than one pure transport component.  Then also add the actual zero-lower
connection-row hyperedges from the lifted old basis.  Equivalently, use the
safe joint 24,192-coordinate physical grade solve.  After both classes of
actual-row hyperedges are included, every generating row is supported inside
one resulting component, which proves sufficiency; omitting either class is
unsound.

The Fourier/monomial transport formulas, the (3+3+6) coordinate orbit
calculation, and the retention of lower-to-grade terms all survive this
repair.  The construction does not extend unchanged to the second rung:
its quotient contains the characteristic-three subgroup (C_3^3), and
(A) is in the noncentral semidirect factor (C_3^3\rtimes A).  The four
(A)-idempotents are therefore not central projectors for the full source
actor action, while the (C_3^3) group algebra is nonsemisimple.

## 7. Efficiency and claim boundaries

V444 saves rediscovery of historical actor words only after a complete
transition presentation is retained.  The persistent data must include:

1. the filtered module and reduction, all auxiliary coordinates, literal
   evaluator, seed roster, and four actor maps;
2. the complete old basis with literal instruction-tree ancestry;
3. every seed reduction (q_{ai}) and every actor transition (q_{Aij}),
   together with their sparse reduction DAGs;
4. the exhausted defect basis and updated transition presentation at every
   grade; and
5. occurrence-side ancestry plus the lower-first physical dependency/fibre
   DAG needed for literal replay or a full dual.

Task 542 retained a particular positive correction, not the complete
degree-zero seed/transition presentation.  Therefore the transition-reuse
route still needs one complete order-2016 pass that records that presentation.
The alternative is one full degree-one construction from the 44 seeds and
to begin reuse only afterwards; there is no free lift from the existing
target preimage alone.

The stated reduction of the 3,936-term candidate correction to 2,622
surviving terms is only a candidate preprocessing count here.  It is not an
orbit rank, attempt bound, runtime measurement, surjectivity statement, or
membership result.  Neither v443 nor v444 nor the repaired v445 block scheme
runs an actual residual test.  In particular none implies MEMBER,
NONMEMBER, full (Q_0), A0, COMMON, fake, or Ihara.

Finally, reusing transition records through the six grades of either fixed
(C_3^3) extension is a finite filtered computation.  It does not construct
the strict compatible selector through every cofinal depth required by
v397/v400 and must not be promoted to such a claim.

## 8. Separate findings and verdict

```text
v443 split arithmetic:                    PASS
v443 carry arithmetic:                    PASS
v443 Fox/action conventions + dimensions: PASS
v444 transition theorem:                  PASS
v444 physical interface:                  PASS
v445 Fourier formulas and 3+3+6 orbits:   PASS
v445 4h_d independent source blocks:      FAIL AS WRITTEN
safe repair:                              4 CHARACTER BLOCKS,
                                          MONOMIALS COUPLED;
                                          ADD ALL ACTUAL-ROW HYPEREDGES
claim boundaries:                         PASS AFTER THAT REPAIR
new finite replay status:                 UNKNOWN (PYTHON-SLOT OVERLAP)
strongest status:                         PAPER-AUDITED, NOT VERIFIED
```

The defect is local and has the exact fail-closed replacement in Section
6.3; it does not invalidate v443, v444, or the degree-one transport table.

AFFINE_ENGINE_TRANSITION_DEFECTS_PASS_AFTER_REPAIR

verified=false
