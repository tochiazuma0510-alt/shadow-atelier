# Task 613 - audit of endpoint-signature precision-two consumer v471

## Verdict

`PASS`

V471 is a sound conditional sharpening of v470.  Equality of the complete
eleven-occurrence endpoint tuple fixes every left multiplier which survives
the conjugate Fox formula, so exact actor paths may be coalesced by signature
for the current precision-two evaluation.  The base-relator endpoint gate is
an explicit prerequisite; the canonical source graph is authenticated and
retained; and the prior root, update, prefixes, signs and physical aggregation
remain occurrencewise.

The prefix trie evaluates an appended letter by right multiplication in word
order and preserves a terminal pointer for every exact path.  All requested
dimensions and the dense seed-cache arithmetic are correct.  V471 also carries
forward, rather than silently discharging, Task568's independent-helper
obligation and does not rely on its inactive resumable join.  There is no
load-bearing repair.

This is a paper verdict.  The Task601 payload and the proposed consumer/checker
have not been accepted or run, and no residual or later mathematical decision
is produced.  `verified=false`.

## 1. Inputs read in full

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_613_audit_r07_endpoint_signature_precision2_consumer_v1.md` | 2,058 | 38 | `50b050ec11f631703a3e65325ec3aa21b8fbce2505ee509caddd26c26bf590a0` |
| `sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md` | 8,731 | 225 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| `sol/sol_reply_611_audit_r07_selected_slp_leaf_gated_precision2_join_v1.md` | 9,580 | 202 | `4212afae131eda13c8d1199bd2a41ad2b232957fd8de2d565fbfe24e34fccd92` |
| `sol/proof_r07_endpoint_signature_precision2_consumer_v471.md` | 8,819 | 220 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md` | 8,050 | 229 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| `sol/sol_reply_568_audit_r07_a0_grade2_prebuild_v1.md` | 22,018 | 385 | `7f2deaf56067f18131a62388b4b82fcd4c7c8fb180d2e750d630c1ac3e771680` |

The audited v471 is bound to 8,819 bytes and SHA-256
`38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f`.

## 2. Complete signatures license exactly the claimed coalescence

After the v470 base gate, every terminal leaf is
\(L_{s,P}=Pr_sP^{-1}\) with
\(\eta\theta_j(r_s)=1\).  The left Fox rule gives

\[
 D_{\eta\theta_j}(L_{s,P})
   =\eta\theta_j(P)\,D_{\eta\theta_j}(r_s).
\]

There is no \(D(P)\) term left: its two occurrences cancel because the
middle relator endpoint is one.  Consequently, for a fixed seed \(s\), two
paths with

\[
 \Sigma(P)=\Sigma(P')
   =\bigl(\eta\theta_j(P)\bigr)_{j\in J}
\]

give identical leaf rows in every registered occurrence.  Regrouping the
finite characteristic-three module sum therefore proves v471 (2.3).

The qualifications in that statement are all necessary and present.

- The signature contains the full marked \(Q_2\) endpoint, not merely its PSL,
  character, coarse or physically aggregated image.
- All eleven registered slots occur in the ordered tuple.  Repeated slots are
  not identified, so their later prefixes and signs remain separately bound.
- Coalescence is only between pairs with the same seed \(s\); different base
  derivatives are not equated from actor endpoints alone.
- The action is left multiplication by \(\tau_j\), agreeing with v443 and the
  left Fox convention.  No right-action substitution is introduced.
- A coefficient two is \(-1\) in \(\mathbf F_3\), hence represents the inverse
  leaf and supplies exactly the minus sign in
  \(D(Pr_s^{-1}P^{-1})=-\eta(P)D(r_s)\).

Thus full signature equality is sufficient.  Equality of an aggregated row
or of any proper component would not be sufficient, and v471 explicitly
forbids those weaker keys.

## 3. Endpoint gates precede every semantic use of a coalesced map

The exact-path table \(\mu_{s,P}\) can be derived from the authenticated graph
before endpoint evaluation as a finite formal coefficient table.  At that
stage it is not yet licensed as a Fox evaluation and cannot be sealed as the
result.  V471 Section 2 assumes the complete base gate before proving either
the leaf formula or signature regrouping, and Section 4 checks that gate
before steps (1.3)--(2.2), dense action, physical comparison or residual
extraction.

This distinction makes the operational order fail-closed.  Computing and
comparing a candidate exact-path table in Section 4 step 2 uses only the
canonical graph; semantic exact-path coalescence and the disappearance of
\(D(P)\) are accepted only after step 3 has checked every reached
seed/occurrence pair.  A failed endpoint check terminates the consumer and
cannot yield a Fox row, signature receipt or residual.

The reached seed set includes the separately authenticated literal terms of
\(C_{<1}\) as well as the descendants of \(C_T\), exactly as v471 (2.3) and
Theorem 2.1 state.  Hence the prior root has no unchecked seed premise.

## 4. Prefix-trie order and exact-path identity

For a trie vertex labelled by a freely reduced prefix \(P\) and an outgoing
letter \(a\), the homomorphism recursion is

\[
 g_j(1)=1,\qquad
 g_j(Pa)=g_j(P)\,\eta\theta_j(a).
\]

This is the right multiplication meant by v471's prefix extension: letters
are consumed in their stored left-to-right word order.  Left multiplication
would reverse the word and is not licensed.  Negative edges use the exact
marked inverse images fixed by v443.

Prefix sharing changes only the evaluation schedule.  Every terminal retains
a pointer to its original freely reduced exact key, and the receipt binds
every path-to-signature assignment to the independently recomputed exact-path
map and ordered occurrence contexts.  The checker may instead evaluate each
path directly.  Either route detects a side/order mutation.  The trie is
therefore not source syntax, does not identify unequal free words, and cannot
delete an edge of the canonical graph.

## 5. Complete root and physical join

V471's \(\mu\) includes both components of

\[
 C_1=\operatorname{Compose}(C_{<1},C_T)
\]

in their registered complete-root order.  Under the current meaning audited
in Task611, `Compose` is the ordered source-group product of the sealed prior
terms followed by the update.  Both parts are endpoint one after the base
gate, so Fox additivity applies to the complete root.

The evaluation remains occurrence-first:

1. apply each occurrence substitution and its signature component;
2. apply the occurrence's inverse sign, fixed prefix and pinned PB3 map;
3. retain repeated slots separately; and
4. only then perform signed physical aggregation.

No action on an already aggregated row is postulated.  The consumer evaluates
the authenticated target independently and requires the entire lower,
grade-one and auxiliary difference to vanish.  It also separately compares
the selected update with the Task601 physical replay and Task595 MEMBER
equation.  Only after those gates may it define the grade-two block of the
complete difference.

## 6. Dimensions and resource arithmetic

The five numerical claims are exact.

\[
\begin{aligned}
44\cdot11 &=484,\\
8{,}064+24{,}192+4 &=32{,}260,\\
\dim\operatorname{gr}_2 &=48{,}384,\\
48{,}384/4 &=12{,}096.
\end{aligned}
\]

The last division is valid because the registered base-three packing stores
four trits per byte.  One dense compact-seed tuple consists of the
occurrence degree-zero, degree-one and degree-two rows plus eight auxiliary
entries:

\[
24{,}192+72{,}576+145{,}152+8=241{,}928
\]

`uint8` bytes.  Therefore

\[
44\cdot241{,}928=10{,}644{,}832
\]

row bytes, before array metadata.  The 484 figure counts endpoint equality
assertions, not actor-path multiplications or trie work; v471 charges those
separately by \(11U\).  Likewise \(G\le L\) because every nonzero signature
bucket contains at least one exact key.

## 7. Task568 independence boundary and claim boundary

Task568 found that its checker shared the floor helper and had no active,
independently authenticated result-dependent join; resume could also accept
an insufficiently rebound residual.  V471 does not cite that old path as a
receipt.  It specifies a new narrow consumer whose checker must independently
implement endpoint, truncated-polynomial, action, target and aggregation
arithmetic, must derive the exact-path/signature tables rather than trust
exports, and must bind an accepted Task601 independent-check receipt.
It expressly carries forward the shared-floor-helper repair and excludes the
unaccepted closure/resumable-join code from the construction.

Accordingly an eventual implementation is not accepted merely by reusing the
Task568 helper or its inactive join.  It must provide the independent active
consumer just specified, recompute all lower and top coordinates and digests,
and stop after sealing the fresh residual.  V471 does not claim that this has
already happened.

```text
TASK613_V471_AUDIT:                         PASS
FULL ENDPOINT SIGNATURE COALESCENCE:        SOUND AT CURRENT QUOTIENT
BASE ENDPOINT GATE BEFORE FOX USE:          REQUIRED AND PRESENT
PREFIX-TRIE WORD ORDER:                     PREFIX ENDPOINT TIMES NEXT LETTER
EXACT PATH / CANONICAL GRAPH PRESERVED:     YES
PRIOR ROOT + SELECTED UPDATE:               BOTH INCLUDED
COMMON ACTION AFTER PHYSICAL AGGREGATION:   NOT USED
ENDPOINT / LOWER / TOP / PACKED WIDTHS:     CORRECT
DENSE 44-SEED CACHE BYTES:                  10,644,832
TASK568 SHARED-HELPER DEFECT:               STILL A REQUIRED REPAIR
TASK568 INACTIVE JOIN USED AS RECEIPT:       NO
ACTUAL TASK601 PAYLOAD / FRESH RHO2:        NOT PRODUCED
GRADE TWO / A0 / COMMON / COFINALITY:       NOT DECIDED
FAKE / IHARA:                               NOT DECLARED
verified:                                    false
```
