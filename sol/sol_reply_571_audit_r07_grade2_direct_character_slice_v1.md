# Sol(max) Reply 571: audit of the grade-two direct character slice

Author: Sol / 2026-09-03

## 1. Scope and decision

V453's paper theorem is correct.  Task565's first array axis is already the
common **source Fourier-character** axis, not the raw `A=C2^2` group-basis
axis.  Consequently, on a lower-zero pure degree-two defect, each legal
v447 projector is exactly the coordinate selector for that axis.  The four
word actions and the subsequent Walsh transform may be removed from each
defect without changing any packet row.

This conclusion does not accept an implementation of that optimization.
The current Task565 producer still calls its word projector for every defect
(`build_grade2_defect_packets`, lines 1866--1884), and the current checker
still reconstructs those word projectors for every defect (lines 907--928).
Task568's streaming, structural-DAG, independent-helper and MEMBER-join
repairs also remain open.  No production phase, membership reduction, or
certificate was run in this audit.

The audited inputs were:

| input | bytes | SHA-256 |
|---|---:|---|
| v447 | 4,415 | `3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2` |
| v451 | 8,050 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| v452 | 12,975 | `754c5ae214ee48ad530948feb734a50395386e5bb1d8fe25daf0cedc6c3313c1` |
| Task568 full reply | 22,018 | `7f2deaf56067f18131a62388b4b82fcd4c7c8fb180d2e750d630c1ac3e771680` |
| v453 | 3,780 | `41390912a33b94d3c185acf022edcd62d1a1dcd077049cb9f172eed89cf37a2e` |

For the factual storage claim I also inspected the unchanged Task565
producer and checker, respectively SHA-256
`acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8`
and
`fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf`.

## 2. The stored index is the Fourier-character index

Write `A_j` for the parity map at occurrence tag `j`.  If `lambda` is the
common source label, the tag-local character used by the engines is

\[
 \tau_j(\lambda)=\lambda\circ A_j^{-1}.             \tag{2.1}
\]

This is not inferred from a field named `character`.  It is how the arrays
are constructed:

- the inherited label order is literally
  `(00,01,10,11)` (grade-one v4 line 35 and Task565 producer line 42);
- `cv((r,s),a,b)=(-1)^(ra+sb)` in `F3` (v4 lines 157--158);
- the six `transport` tables are computed from the inverses of the actual
  occurrence parity matrices (v4 lines 259--285);
- literal seed evaluation writes source index `lambda` with coefficient
  `cv(transport[j][lambda],b)` (v4 lines 379--410 and the degree-two
  extension at Task565 lines 776--815); and
- flattening and unflattening preserve the character as the outer axis
  (Task565 lines 818--852).  Within one degree-two character row the exact
  order is `tag, Fox component, monomial, PSL index`, of size
  `6*2*6*504=36,288`.

Thus a degree-two coordinate has the semantic form

\[
 \widehat\beta_{\lambda,j,c,\alpha,p}
 =\sum_{b\in A}\tau_j(\lambda)(b)
                 \beta_{j,c,\alpha,p,b}.           \tag{2.2}
\]

The independent checker spells out the same label order, character pairing,
transport construction and source evaluation at lines 30--49, 279--307 and
490--514.  Task568 correctly identified a shared lower-level `floor` helper,
so that checker is not thereby promoted to fully independent production
evidence; the displayed definitions are nevertheless enough to settle what
the stored index means.

## 3. Diagonal action, including all occurrence coordinates

For the v447 word `w_a`, its source endpoint is `(1_P,a)`.  In tag `j`, the
same correlated word has quotient endpoint `(1_P,A_j a)`, possibly followed
upstairs by a kernel value `v_[j,a]`.  On a homogeneous degree-two term,
v447's associated-grade calculation gives

\[
 [p,A_j a+b]E(S(b)v_{j,a})u^\alpha
 \equiv [p,A_j a+b]u^\alpha\pmod {I^3}.             \tag{3.1}
\]

Every nonconstant term of `E(S(b)v_[j,a])-1` raises degree, so no assertion
that the upstairs kernel coordinate vanishes is needed.  The PSL endpoint is
the identity, and neither the Fox component nor the degree-two monomial is
changed.  Fourier transformation of the translated `A` coordinate supplies

\[
 \tau_j(\lambda)(A_j a)=\lambda(a).                 \tag{3.2}
\]

The scalar is therefore independent of `j`.  It applies simultaneously to
all six tags, both Fox components, all six degree-two monomials and all 504
PSL positions.  This proves the precise Task565 statement

\[
       (T_a\beta)_\mu=\mu(a)\beta_\mu,              \tag{3.3}
\]

not merely a statement about a conveniently labelled test vector.  Direct
slicing does not authorize a tag, component, monomial or PSL-coordinate
projection.  Each emitted packet remains the complete coupled width-36,288
row, and physical occurrence transport plus old-lift connection rows remain
unchanged.

The pure hypothesis is load-bearing.  If a lower degree-one term `u_1` is
present and a word has kernel factor `E(u_1)`, then
`E(u_1)u_1=u_1+u_1^2` through degree two; selecting only the pre-existing
degree-two character slice would miss the induced `u_1^2` term.  V453
excludes this counterexample, v451 keeps the full filtered `P_chi` separate,
and Task565 asserts zero degree zero, degree one and auxiliary parts before
projecting every grade-two defect.

## 4. Normalization and registered order

With rows and columns both ordered `(00,01,10,11)`, the pinned character
table over `F3` is

\[
 H=
 \begin{pmatrix}
 1&1&1&1\\
 1&2&1&2\\
 1&1&2&2\\
 1&2&2&1
 \end{pmatrix}.                                    \tag{4.1}
\]

This is the repaired v452 order: its second row is `chi01` and its third is
`chi10`.  Since every character and every element of `A` is self-inverse,
no inverse-character convention changes a label.  Character orthogonality
gives

\[
 \sum_{a\in A}\lambda(a)\mu(a)
 =\begin{cases}4,&\lambda=\mu,\\0,&\lambda\ne\mu.
 \end{cases}                                       \tag{4.2}
\]

In `F3`, `4=1` and hence also `1/4=1`; there is no omitted scalar.  Combining
(3.3) and (4.2) yields

\[
 (e_\lambda\beta)_\mu=\delta_{\lambda\mu}\beta_\mu.
                                                               \tag{4.3}
\]

Accordingly the packet operation is literally

```text
packet[lambda] = beta.reshape(4,36288)[lambda]
```

with reconstruction understood as embedding each local packet back into its
own disjoint character slot before summing.  It is not the sum of four local
36,288-coordinate arrays as though they shared a character label.

For comparison, if the first axis were the raw `A` basis, direct slicing
would be false.  A single raw basis vector `delta_00` would be sent by
`e_lambda` to `sum_a lambda(a) delta_a`, whereas selecting raw slot `lambda`
would retain at most one coordinate.  This is the minimal counterexample to
the premise that v453 independently checks above; it does not apply to the
actual Task565 storage.

## 5. Exact fail-closed integration gates

V453 section 4 is sufficient when “establish from pinned data” is read as an
exact semantic replay, not as trusting labels or passing one sampled vector.
The following is the precise once-per-run realization of its four bullets.

1. Producer and checker independently pin the field, character function,
   label order `(00,01,10,11)`, degree-two monomial order
   `(200,110,101,020,011,002)`, dimensions and the complete flattening order
   `character,tag,component,monomial,PSL`.
2. From the four literal words and the registered quotient marking, each side
   derives all four source endpoints `(1_P,a)` and, for every one of the six
   occurrence substitutions, all 24 tag endpoints `(1_P,A_j a)`.  It derives
   each invertible `A_j` and checks that the stored transport is exactly
   `lambda -> lambda o A_j^-1`.  Checking only the source endpoint or a
   declared character label is insufficient.
3. Each side binds the affine lift of every word.  Arbitrary upstairs kernel
   values are accepted, but the checker explicitly applies the associated-
   grade truncation and derives scalar `lambda(a)` with identity action on
   every tag/component/monomial/PSL stratum.  A word with a nonidentity tag
   PSL endpoint, a wrong transport, or a coordinate permutation must fail.
4. Each side constructs (4.1) from `cv`, checks the four orthogonality/selector
   identities over `F3`, and compares one bounded legal-word/Walsh canary per
   character with the corresponding direct embedded slice.  Each canary must
   meet every tag, both components and all six monomials.  These canaries are
   regression checks; the exact endpoint, transport and layout derivation in
   steps 1--3 is the load-bearing proof.
5. The sealed prepare/block receipts bind the direct-slice mode and theorem
   inputs, character index and label, width 36,288, full origin roster and
   order, parent digest, row count and packet bytes/hash.  Resume must replay
   these run-global gates or authenticate a receipt which binds their complete
   results and the exact executable identities.

There are also unavoidable per-defect gates; moving them into a once-per-run
canary would be unsound.  For every one of the exact
`44+4*rank(B1)` origins, both paths must reconstruct the complete defect,
assert all lower and auxiliary coordinates are zero, compare every one of
the 36,288 entries of each direct slice, and check the four disjoint
embeddings reconstruct the full 145,152-coordinate degree-two row.  Sampling
actual packets is not allowed.

If step 2 were omitted, one tag could accidentally use an untransported
character.  For any nontrivial `A_j` choose `lambda,a` with
`lambda(A_j a) != lambda(a)`; source endpoints and labels would still look
right while that tag has the wrong eigenvalue.  If steps 1 and 3 were reduced
to one canary, a coordinate permutation fixing that canary would also pass.
These are implementation counterexamples, not defects in v453, whose phrase
“from pinned data” and full-action requirement exclude them.

## 6. Claim boundary

The result is a paper-level equality of two ways to form the same legal pure-
grade projectors.  It authorizes replacing only Task565's per-defect
`project_pure_degree2_by_words` split by direct character-row copies after
the gates above.  It does not replace the full filtered seed operators of
v451, alter the defect roster or closure universe, split the six monomials,
accept Task565/Task567 production, close any Task568 release repair, or decide
grade-two membership.

No v220 numerator was changed.  No grade is decided, and no A0, COMMON,
cofinal-lift, fake or Ihara conclusion follows.  `verified=false`.

GRADE2_DIRECT_CHARACTER_SLICE_V453_AUDIT_PASS
