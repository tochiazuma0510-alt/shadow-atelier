# The 616-letter R07 relation/onto block at E4 v89

Author: Sol / 2026-08-26

Status: the registered v1 scope is `cross_checked`.  The finite type/inverse
subclaim was rebuilt by the fibre-only checker, and GHA run `32870813120`
independently replayed the complete registered 4096 dictionary with seven
mutations.  `verified=false`.  Charmingness at this E4 target, the next chief
correction, cofinality and an Ihara witness remain open.

## 1. Frozen word and target

The literal word is

\[
w_{23}=w_2(w_3^{-1}w_2)^8,
\qquad |w_{23}|=616,
\tag{1.1}
\]

with signed-list SHA-256

```text
3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90.
```

The target is the authenticated matched q3 object

\[
E_4=Q_4\times\Pi_4[3],
\tag{1.2}
\]

not merely its G9 roof coordinate.

## 2. Relation block

Using the frozen coface order \([C,A,E,B,F]\) and native A.18 product

\[
FEC B^{-1}A^{-1},
\tag{2.1}
\]

direct evaluation gives

\[
\boxed{
H_1(w_{23})=H_2(w_{23})=1,
\qquad
A.18(w_{23})=1
\quad\text{in }E_4.}
\tag{2.2}
\]

The five individual coface values are not the old 20-letter tuple.  All five
fine coordinates differ even though the total product (2.1) is identity for
both words.  Thus (2.2) is a direct 616-word fact, not an inherited verdict.

## 3. Explicit two-sided inverse

Let \(S_i=S_i(w_{23})\), \(1\leq i\leq6\), be the six marked source words.
The complete authenticated exponent-seven diagnostic family has 27 entries.
All 27 were evaluated.  Exactly index 1 passes, so its correction word is
empty and its base word is the canonical exponent-seven row

\[
v=[-1,-1,-1,-1,2,2,1,-2,-2,-2,1,1,2,-1,-2,-2,1,1,2,2].
\tag{3.1}
\]

Writing \(T_i=S_i(v)\), direct evaluation gives

\[
\boxed{
T_i(S_1,\ldots,S_6)=x_i,
\qquad
S_i(T_1,\ldots,T_6)=x_i
\quad(1\leq i\leq6)
}
\tag{3.2}
\]

in \(E_4\).  The six inverse-word lengths are

\[
(1,41,101,41,161,61),
\tag{3.3}
\]

their ordered-list SHA-256 is

```text
7d49ed8811f661031077b45d7fd6fab2eb21fdef308486367dc8981d0918879e,
```

and the exact ordered six-image cache-key SHA-256 is

```text
59ae54aedb638b5cf69d76ba4d838c94a1c6412af89689f6709af4350e5ef0a2.
```

Equation (3.2) proves that the six-source substitution is an automorphism on
the marked E4 object.  Hence the E4 onto gate is closed without relying on the
alternative v88 Goursat--Nakayama test.

## 4. Evidence grade

The producer certificate is

```text
search/certs/d972_r07_relfrat3_actual_class_preflight_v1_20260826.json
bytes   473404
SHA256  2d23aababa215955699f3774205bbe8356b52a3067f4f8d052f84048a5bc7f3d
```

The bounded fibre-only checker rebuilt the E3/E4 evaluations, both hexagons,
ordered A.18, both-side 27-source audit and all 27 inverse candidates, and
ended

```text
R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_PASS
terminal=R07_RELFRAT3_TYPE_MISMATCH_STOP
mutations=7 dictionary_replayed=false
```

The separate single-process full replay on commit
`a4cd978c9af15783d858e145047901027a8ad3be` completed successfully as GHA
run `32870813120` and ended

```text
R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_PASS
terminal=R07_RELFRAT3_TYPE_MISMATCH_STOP
mutations=7 dictionary_replayed=true
receipt_sha256=2d23aababa215955699f3774205bbe8356b52a3067f4f8d052f84048a5bc7f3d
R07_RELFRAT3_ACTUAL_CLASS_V1_GHA_DRIVER_PASS mode=full checker_marker_count=1
```

Thus the complete registered dictionary and the type separation are now
independently replayed.  The terminal stops only transport of the old
base-specific Fox data.  It does not negate (2.2)--(3.2), and it is not an
obstruction to the fresh 760-letter base.

## 5. Exact remaining boundary

The current finite branch ledger is

```text
616 E4 TWO HEXAGONS:                         CROSS_CHECKED
616 E4 ORDERED A18:                          CROSS_CHECKED
616 E4 SOURCE ONTO / TWO-SIDED INVERSE:      CROSS_CHECKED
616 E4 EXPLICIT CHARMING COMMUTATOR WITNESS: OPEN
616 NEXT-CHIEF ACTUAL BETA AND A18 MAP:       OPEN
616 REGISTERED TARGET-6 CORRECTION:           NOT YET COMPUTED
FULL J_H/J_PHI CORRECTION TOTALITY:           OPEN
COFINAL COMPATIBLE LIFT:                      NOT YET CONSTRUCTED
IHARA WITNESS:                                NOT DECLARED
```

Thus the current E4 relation/onto block is no longer a blocker.  The next
load-bearing computation is the base-specific affine right-hand side and the
finite-derived/charming witness, followed by the actual normalized Brunnian
class.
