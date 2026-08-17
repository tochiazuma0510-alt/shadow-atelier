# Luna reply 157bc: exact generic Burau decision

## Verdict

```text
SOME_NORMS_NONCENTRAL_IN_K05_U_M_UNDECIDED
```

The generic unreduced Burau calculation does not give an all-972 identity.
It gives an exact K(0,5) nonidentity for 970 of the 972 canonical norm
words.  This is not, by itself, an A witness in `U_M`, because the 140
additional presentation relators can still kill a word which is nonidentity
in K(0,5).

## Frozen input and independent norm reconstruction

The producer and checker both bind
`search/certs/d972_b4_p2_magnus_input_v2_20260816.json` directly, with:

```text
schema                 d972-b4-p2-magnus-input/v2
relators               158
relator sha256         12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e
rho sha256             23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed
roof words             972
roof sha256            3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8
target key digest      9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
norm digest            ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e
unique norm count      486
```

The roof rows are the frozen marked `F2` words.  The exact inclusion used in
both independent paths is `j(x)=X12` and `j(y)=X23`, i.e. signed `1` maps to
signed six-generator `1` and signed `2` maps to signed six-generator `4`.
For each row the code constructs

```text
rho^4(j(f)) rho^3(j(f)) rho^2(j(f)) rho(j(f)) j(f)
```

by free reduction, rather than importing an earlier norm constructor.  The
frozen norm digest above is required before any matrix decision is accepted.

## Exact Burau representation

The unreduced generator block is

```text
              [ 1-t   t ]
rho(s_i) =    [  1    0 ]
```

and the exact inverse block is

```text
              [  0       1       ]
rho(s_i)^-1 = [ t^-1  1-t^-1     ].
```

Entries are sparse Laurent polynomials represented by complete sorted
`(exponent, integer coefficient)` pairs.  No finite evaluation is used.
The convention is column vectors with
`M(a1...an)=M(a1)...M(an)`; the running matrix is right-multiplied by each
literal letter.  Centrality/equality is unchanged if the opposite transpose
convention is used consistently.

The six pure generators were lifted in exactly this order:

```text
X12 = s1^2
X13 = s2*s1^2*s2^-1
X14 = s3*s2*s1^2*s2^-1*s3^-1
X23 = s2^2
X24 = s3*s2^2*s3^-1
X34 = s3^2
```

Both implementations passed all exact representation gates:

```text
braid relations                 [true, true]
far commutativity               true
exact generator inverses        [true, true, true]
six pure-generator formulas     [true, true, true, true, true, true]
Delta4^2 centrality             true
generic/full-multiply agreement true
```

Here `Delta4^2` is the literal `(s1*s2*s3)^4`; its full exact Laurent matrix
was used as the center reference.  The K(0,5) test for a norm with exponent
vector `e` is:

```text
e not constant       -> NONIDENTITY_BY_PB4_ABELIANIZATION
e=(k,k,k,k,k,k)      -> compare M(norm) exactly with M(Delta4^2)^k
```

This uses generic Burau faithfulness only for equality of individual `B4`
words.  No specialization-cofinality assertion is invoked.

## Primary-source provenance and the reduced/unreduced point

The primary source used for the generic-faithfulness premise is the local PDF
`C:\Users\81905\Desktop\文献リスト\2607.05283v1.pdf`, SHA-256
`ECAF125B6075BCBCCA9D7B9A55274CB1C8E16BB1BF22BBE0737BF25DED381C7C`.
Page-image checks (not text extraction alone) confirm the following locations:

```text
PDF p.1   Main Theorem: the unreduced Burau representation rho_4 of B_4 is faithful;
          the paragraph above it distinguishes the reduced (rank n-1) and
          unreduced (rank n) conventions.
PDF p.2   Proposition 1.2: faithfulness on Brun_4 implies faithfulness on B_4.
PDF p.3   Section 2 definition: rho_n is the unreduced relative-homology action.
PDF p.17  Proposition 6.4 (the B_4 -> B_5 push construction).
PDF p.21  Corollary 6.5 and Theorem 6.6 (faithfulness on Brun_4).
```

The calculation above uses the paper's unreduced 4-by-4 generator blocks
directly.  No ``unreduced = reduced'' kernel equality is being assumed: the
reduced representation is the quotient by the standard invariant rank-one
line, so reduced faithfulness would imply unreduced faithfulness, whereas the
converse requires an additional integral splitting/kernel argument.  The
paper explicitly works mainly with the unreduced representation and proves
the stated Main Theorem for that representation; it does not supply (and this
reply does not use) a blanket equality of the two kernels.  Thus the
generic-faithfulness input to this computation is sourced by Main Theorem
p.1 (with its reduction to Proposition 1.2 p.2), not by an unproved
reduced/unreduced equivalence.

## Full result

```text
rows checked                         972
unique norms                         486
unique exact matrices                486
identity in K(0,5)                    2
nonidentity by PB4 abelianization   854
noncentral in K(0,5)                116
nonidentity total                   970
```

The producer evidence was written outside the repository at
`%TEMP%\d972_b4_generic_burau_v1.json` and has SHA-256
`e3a9df2b38638dd04021e6d2cc70c4004d310757ff8770c65cf068f36c886768`.
It contains lossless coefficient dictionaries for every one of the 972 rows;
the checker independently rebuilt all rows and all 486 distinct matrices and
matched every coefficient.

The two central rows are genuine identities in K(0,5), hence remain
identities in the further quotient `U_M`.  The 970 nonidentity results are
only K(0,5) results: they must not be relabelled as A defects without proving
that the relevant additional relators do not kill them.

## Independent checker hardening

The checker has a separate tuple-of-pairs Laurent implementation and does not
import the producer or an old norm helper.  Its mutation-rich selftest and
the completed run reject:

```text
omitted or duplicated/reordered roof rows
evaluation-only matrices with no coefficient lists
reversed rho orbit
wrong Delta4^2 center power
duplicate/unsorted/zero Laurent coefficients
forged aggregate counts or status
```

Selftests passed before the full run:

```text
PRODUCER_SELFTEST_PASS
CHECKER_SELFTEST_PASS
```

Commands actually run were Python-only:

```text
python search/d972_b4_generic_burau_v1.py --output "%TEMP%\d972_b4_generic_burau_v1.json" --skip-selftest
python search/check_d972_b4_generic_burau_v1.py --evidence "%TEMP%\d972_b4_generic_burau_v1.json"
```

No GAP, Git, GHA, finite-field evaluation, or workflow change was used.

## What this does and does not settle

This is a decisive exact answer for the 972 frozen words in the generic
faithful `B4` representation and the K(0,5) center quotient.  It does not
promote the universal pentagon identity: 970 rows already fail in K(0,5),
and a K(0,5) failure can still disappear in `U_M`.

It also does not settle B4-B or the 325 actual ML lifts.  Those require, in
addition, the audited identification of the six-generator presentation with
the intended typed quotient, the five coface maps and their fibers,
isolatedness/finite-index typing of `M`, and the universal lift/cofinality
argument.  The generic theorem supplies exact word separation, not those
typed GT-shadow or compactness bridges.

SOME_NORMS_NONCENTRAL_IN_K05_U_M_UNDECIDED
