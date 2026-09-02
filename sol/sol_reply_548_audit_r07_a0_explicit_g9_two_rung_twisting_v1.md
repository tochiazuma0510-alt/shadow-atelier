# Task 548 independent audit -- explicit G9 two-rung twisting

`verified=false` (no Lean certificate is supplied).  The frozen affine data,
all six occurrence tables, both extension formulae, and the truncated grade
sizes are correct.  The formulae use section-left, kernel-right normal form;
with that convention there is no missing sign, transpose, or reversal.  The
strongest status below is cross-checked, not verified.

## 1. Frozen inputs and audit scope

The dispatch hash of v442 matched before the audit and again inside the final
independent checker.  I read every prescribed input in full.  The final bytes
used were:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `sol/sol_task_548_audit_r07_a0_explicit_g9_two_rung_twisting_v1.md` | 4,492 | `504d61e1d808df204a2d5bf9e748b6aa1cdcf453c81147c77fcbd0254eda7cbf` |
| `sol/proof_r07_a0_explicit_g9_two_rung_twisting_v442.md` | 8,710 | `afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4` |
| `sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md` | 11,696 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| `sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md` | 14,931 | `7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3` |
| `sol/proof_r07_a0_c2fourier_joint_lift_v439.md` | 9,111 | `b18e27ac79f870a6bb5c104a12e85a95daf8644e080153305ce8447e3736f122` |
| `sol/sol_reply_540_audit_r07_a0_c2fourier_next_rung_v1.md` | 21,385 | `3114977ca62727296bf4c3980e405e920169a9c10b4bfdfa80f15990aac3a31d` |
| `scratchpad/fuda1_a0_rmax_data.g` | 4,709 | `625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba` |
| `scratchpad/a0_paper_words_v1.json` | 115,928 | `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893` |

For the requested convention comparison I also pinned these current
occurrence/Fox artifacts:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `scratchpad/a0_paper_coarse_v2.py` | 12,267 | `d2844ed315b6e7702a841ccd06a210d6f2e90b956161a2c132bf4d9a66daacd8` |
| `search/d972_r07_a0_c2fourier_joint_floor_v1.py` | 26,235 | `6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba` |
| `search/check_d972_r07_a0_c2fourier_joint_floor_v1.py` | 8,539 | `abd8279e14b673ad1e1b197a9a29bb1ecefe5546762a81d314d50ccf89d90dd0` |

The JSON was parsed completely: its top-level keys are `g760`,
`pc_generators`, `pc_source_words`, `registered_q0_relators`, `relators`, and
`relators_sha256`; `g760` has length 760 and the 44 relators contain 35,384
letters in total.  Nothing in this audit runs either later six-grade search.

## 2. Affine group and complement -- PASS

Number the points in each G9 block by $t=0,\ldots,8$.  Direct restriction of
the two frozen degree-36 permutations gives

\[
 X=((1,0),(0,1),(0,1)),\qquad
 Y=((1,1),(1,0),(1,1)).
\]

The independently used permutation composer was
`compose(p,q)[i]=q[p[i]]`.  Hence applying (p) and then (q) gives exactly

\[
 (r,e)\star(s,f)=(S(f)r+s,e+f),
 \qquad S(f)=(-1)^f,
\]

which is v442 (1.1), not its opposite.  Direct word evaluation then gives

\[
 X^{10}=t_1=(1,0,0),\quad
 Y^{10}=t_2=(0,1,0),\quad
 (XY)^{10}=t_3=(0,0,1).
\]

Thus these words generate all (9^3=729) rotations.  A BFS in the independently
recovered affine coordinates gave `|<X,Y>|=2916`, with exactly 729 pure
rotations.  The complement words gave

```text
sX = X^9                  rotation (0,0,0), parity (0,1,1)
sY = t1*t2^-1*t3*Y        rotation (0,0,0), parity (1,0,1)
```

Both square to one and commute.  Conversely
(X=s_Xt_1) and (Y=s_Yt_1t_2t_3), so they give the whole group, not merely
an abstract complement.  In the order

```text
[sX,t1], [sX,t2], [sX,t3], [sY,t1], [sY,t2], [sY,t3]
```

the recovered commutator rotation vectors were

```text
(0,0,0), (0,2,0), (0,0,2), (2,0,0), (0,0,0), (0,0,2).
```

Since 2 is a unit modulo 9, these span all (C_9^3).  The quotient by the
rotations is abelian, so this proves independently that

\[
 G9'=N=C_9^3,qquad G9=N\rtimes\langle s_X,s_Y\rangle.
\]

Conjugating the three rotations gives, respectively,

\[
 S(s_X)=\operatorname{diag}(1,-1,-1),\qquad
 S(s_Y)=\operatorname{diag}(-1,1,-1),
\]

so v442 (1.2)--(1.8) all pass.

## 3. Six occurrence matrices and crossed terms -- PASS

The two nontrivial auxiliary words were recovered as

\[
 Z=X^{-1}Y^{-1}=((2,1),(-1,1),(1,0)),\qquad
 U=Y^{-1}X^{-1}=((0,1),(1,1),(-1,0)).
\]

Here each displayed component is `(rotation, parity)`.  The following table
is independently derived.  `M columns` lists the images of
((t_1,t_2,t_3)); `A columns` lists the images of the ordered quotient basis
((s_X,s_Y)).  Thus it fixes both possible transpose ambiguities.

| (j) | pair | (M_j) columns / images of (t_i) | (A_j) columns | (c_j(s_X)) | (c_j(s_Y)) | (c_j(s_Xs_Y)) |
|---:|---|---|---|---|---|---|
| 0 | `(X,Y)` | ((e_1,e_2,e_3)) | (((1,0),(0,1))) | ((0,0,0)) | ((0,0,0)) | ((0,0,0)) |
| 1 | `(X,Z)` | ((e_1,e_3,-e_2)) | (((1,0),(1,1))) | ((0,0,0)) | ((1,0,0)) | ((1,0,0)) |
| 2 | `(Y,Z)` | ((e_2,e_3,e_1)) | (((0,1),(1,1))) | ((1,0,1)) | ((1,-2,0)) | ((0,-2,1)) |
| 3 | `(U,X)` | ((-e_3,e_1,-e_2)) | (((1,1),(1,0))) | ((0,1,0)) | ((0,1,1)) | ((0,0,1)) |
| 4 | `(X,Y)` | ((e_1,e_2,e_3)) | (((1,0),(0,1))) | ((0,0,0)) | ((0,0,0)) | ((0,0,0)) |
| 5 | `(U,Y)` | ((-e_3,e_2,e_1)) | (((1,1),(0,1))) | ((0,1,0)) | ((0,0,2)) | ((0,1,2)) |

The column lists are exactly the six matrices printed in v442 (2.2).  For an
additional derivation check, if their columns are (m_1,m_2,m_3) and the
second image has affine data ((r_b,e_b)), the defining source word for
(s_Y) gives

\[
 c_j(s_Y)=S(e_b)(m_1-m_2+m_3)+r_b.
\]

This reproduces every entry, including the `-2` and both occurrences of
`2`; they are not copied linear data.

With section-left, kernel-right coordinates an affine element is
(s(e)n(r)).  Therefore

\[
 c_j(e+f)=S(A_jf)c_j(e)+c_j(f),
 \qquad
 \alpha_j(r,e)=(M_jr+c_j(e),A_je).
\]

All 96 crossed-law cases passed.  The intertwining identity

\[
 M_jS(e)=S(A_je)M_j
\]

and the full formula were checked for all
(6\cdot4\cdot9^3=17{,}496) affine inputs.  Thus v442 (3.2)--(3.4) use the
correct right crossed law; ordinary addition of the two displayed generator
values would be wrong.

The current artifacts use the same convention.  Their occurrence registry is
literally

```text
(x,y), (x,x^-1 y^-1), (y,x^-1 y^-1),
(y^-1 x^-1,x), (x,y), (y^-1 x^-1,y),
```

their permutation multiplication is `q after p`, word evaluation folds from
left to right, and their negative Fox rule multiplies the inverse before
recording the negative prefix.  An independent integral group-ring replay
checked the Fox fundamental identity 270 times: the 44 relators in all six
occurrences (264 identities), plus all six `g760` occurrences.  All 264
relator endpoints were the degree-36 identity.  Finally, the above (A_j)
matrices give the character transports

```text
(u,v), (u,u+v), (u+v,u), (v,u+v), (u,v), (u+v,v),
```

exactly as in the current Fourier artifacts.  This rules out a hidden
transpose or occurrence-order reversal.

## 4. The two extension formulae -- PASS

For the first extension, reduction modulo (N^3) gives

\[
 Q_2=P\times(C_3^3\rtimes A)\longrightarrow Q_1=P\times A.
\]

The section ((p,e)\mapsto(p,0,e)) is multiplicative.  All 16 pairs in
(A^2) replayed with zero multiplication cocycle.  The kernel action is
the displayed sign action, and direct reduction of all six affine maps gives
exactly (M_j\bmod3) and (c_j(e)\bmod3).  This was also checked on all
(6\cdot108=648) affine quotient coordinates.

For the second extension, the convention pin is important.  Write every
element uniquely as

\[
 \sigma(q)n(v),\qquad q=(\bar r,e),\quad v\in C_3^3,
\]

with the section on the left and the kernel on the right.  Then

\[
 (q,v)(q',w)=
 (qq',S(f)v+\omega(q,q')+w),\qquad q'=(\bar s,f).
\]

If

\[
 \Omega(q,q')=S(f)d(\bar r)+d(\bar s)
 -d(S(f)\bar r+\bar s\bmod3),
\]

then $\Omega\in3(\mathbf Z/9)^3$, and the actual $C_3^3$ coordinate is
$\omega=\Omega/3\bmod3$.  Equivalently,

\[
 \sigma(q)\sigma(q')=\sigma(qq')n(\Omega).
\]

This is precisely the sign and order in v442 (5.2).  Its right-cocycle
identity is

\[
 S(g)\omega(q,q')+\omega(qq',q'')
 =\omega(q,q'q'')+\omega(q',q''),
\]

where (g) is the parity of (q'').  The numerator divisibility and product
reconstruction passed on all (108^2=11{,}664) pairs, and this identity
passed on all (108^3=1{,}259{,}712) triples.

For an occurrence put

\[
 \beta_j(\bar r,e)=(M_j\bar r+c_j(e),A_je)\pmod3.
\]

The numerator in v442 (5.3) is exactly the right-kernel difference in

\[
 \alpha_j(\sigma(q))=\sigma(\beta_jq)n(3\kappa_j(q)).
\]

It was divisible by three and reconstructed the direct affine occurrence in
all 648 cases.  For every one of the (6\cdot108^2=69{,}984) ordered
occurrence/pair cases, both $\beta_j(qq')=\beta_j(q)\beta_j(q')$ and

\[
 \boxed{
 \kappa_j(qq')+M_j\omega(q,q')
 =S(A_jf)\kappa_j(q)
  +\omega(\beta_jq,\beta_jq')+\kappa_j(q') }
\]

held in (C_3^3).  This is the required compatibility with multiplication.

If one instead placed the kernel on the left, the stored cocycle would be
conjugated by the total quotient parity.  That is a different convention,
not a missing factor in v442.  The right-normal convention above is the one
compatible with its affine law and the current word/Fox evaluator.

## 5. Truncation and dimensions -- PASS

The six exact generator substitutions recovered from the signed columns are

```text
j=0: (u1,                 u2,                 u3)
j=1: (u1,                 u3,                 2u2+u2^2)
j=2: (u2,                 u3,                 u1)
j=3: (2u3+u3^2,           u1,                 2u2+u2^2)
j=4: (u1,                 u2,                 u3)
j=5: (2u3+u3^2,           u2,                 u1).
```

Indeed, in characteristic three with (u^3=0),

\[
 (1+u)^{-1}-1=2u+u^2,\qquad (2u+u^2)^2=u^2.
\]

More generally, each negative column occurring on a source exponent-one
factor replaces (u) by (2u+u^2); multiplying these factors produces all
terms through total degree six.  The independent polynomial-ring replay
checked

\[
 \phi_{M_j}(E(v))=E(M_jv)
\]

for all (6\cdot27=162) pairs ((j,v)), in the full 27-monomial ring.  The
crossed factors (E(c_j(e))) or (E(\kappa_j(q))) likewise must be retained
as full products; their linear parts alone do not determine grades two
through six.  Thus v442 (6.1) and its warning are correct.

Counting the 27 monomials by total degree gives

\[
 [t^d](1+t+t^2)^3=(1,3,6,7,6,3,1),
\]

so the positive multiplicities are ((3,6,7,6,3,1)).  Multiplication by
(6\cdot2\cdot2016=24{,}192) for occurrence coordinates and by
(2\cdot2\cdot2016=8{,}064) for physical coordinates gives exactly

```text
grade d          1       2        3        4       5       6
occurrence    72576  145152   169344   145152   72576   24192
physical      24192   48384    56448    48384   24192    8064
```

These are new-grade coordinate widths only.  They are neither ranks nor time
or memory estimates.

## 6. Mathematical verdict and claim boundary

| component | verdict |
|---|---|
| affine group, (G9'=C_9^3), and explicit complement | cross-checked PASS |
| six (M_j,A_j,c_j) tables and right crossed law | cross-checked PASS |
| first split extension and zero multiplication cocycle | cross-checked PASS |
| second digit/carry extension and occurrence compatibility | cross-checked PASS |
| exact truncated substitutions and all displayed widths | cross-checked PASS |
| algorithmic consequence | sound conditionally, within v441's occurrence-first/fibre contract |

No displayed item requires repair.  The affine formulae remove the need for a
generic G9 transversal or a materialized 54,432-/1,469,664-entry multiplication
table, but they do not supply the 44-seed closure, PB3/PB4 gates, fibre ranks,
or residual membership outcomes required by v441.  V442 expressly leaves all
twelve positive-grade tests unrun and makes no positive-grade MEMBER claim.
It therefore does not decide the full-Q0 coarse floor, A0, COMMON, a cofinal
compatible lift, fake, or Ihara.

## 7. Commands and independent output receipt

The static reads and pins used PowerShell `Get-Content -Raw -Encoding UTF8`,
`Get-FileHash -Algorithm SHA256`, and `Get-Item` on each path in section 1.
The convention inspection used:

```powershell
rg -n "def (perm_|eval|word|fox|sub|occ)|OCC|occ|SUBS|substitution|compose|mul|inverse|inv|Z|U|tags|TAGS" search/d972_r07_a0_c2fourier_joint_floor_v1.py search/check_d972_r07_a0_c2fourier_joint_floor_v1.py search/d972_r07_a0_psl504_occurrence_floor_v1.py search/check_d972_r07_a0_psl504_occurrence_floor_v1.py
```

After explicit parent coordination and release of the sole Python slot, the
independent checker was run with exactly:

```powershell
python -B -u "$env:TEMP\task548_explicit_g9_audit_v1.py" "C:\Users\81905\Desktop\shadow-atelier"
```

The first invocation stopped after 3.807 seconds at a harness-only assertion
which incorrectly required the JSON to have exactly two top-level keys.  It
reached no finite mathematical test.  With parent authorization, the single
assertion was weakened only to require the two consumed keys, and the same
command was rerun.  The final run exited 0 in 14.301 seconds with
`TASK548_INDEPENDENT_FINITE_REPLAY_PASS`.  No repository helper was imported
and no Python process overlapped it.

Final independent checker source:

```text
path    %TEMP%/task548_explicit_g9_audit_v1.py
bytes   22635
sha256  730e6daabc8ca11e1d40787fd1f1302f2a434ff2360fea299886e0882d5c8bcc
```

The checker emitted one canonical JSON record.  The SHA-256 of its canonical
`{"audit":payload}` object was

```text
854c43dcfd5e226bb30e5c1b8ea134ab71ef27c874775362421eca8e26b1aab1
```

Its load-bearing counts were:

```text
crossed-law cases                              96
full affine occurrence cases              17,496
sign-intertwining cases                    17,496
relator occurrence identities                264
Fox fundamental identities                    270
first split section pairs                       16
first occurrence reductions                   648
second carry products                       11,664
second cocycle triples                   1,259,712
second occurrence carries                     648
second occurrence compatibility pairs      69,984
full signed polynomial substitutions           162
```

No GAP, GHA, git, es7ops, later-grade search, or Lean invocation was used.

EXPLICIT_G9_TWO_RUNG_TWISTING_PASS

verified=false
