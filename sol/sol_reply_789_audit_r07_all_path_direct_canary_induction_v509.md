# Sol(max) Task789 — hostile audit of all-path direct-canary induction v509

## Verdict

`PASS_WITH_EXPLICIT_FINITE_REPAIR`

The mathematical reduction is sound: after the reached-seed endpoint gates,
the direct H1/H2/five-factor-pentagon Fox difference for
`P r_s P^-1` depends on `P` only through its complete typed eleven-slot
endpoint signature.  The four signed actor atoms and right-extension trie
therefore prove the identity for every reached path.  On the actual v14
input, the generic all-seven calls may be reduced from `G=21,287` to the
`S=23` reached-seed calls at the empty path, on each of producer and checker.

Two finite clarifications are mandatory before dispatching a successor.

1. v509 (2.1) must define `L_o` as the **actual g-dependent occurrence
   prefix** below.  The prose that unchanged copies of `g` “cancel” is too
   loose: derivatives of unchanged `g` cancel, but evaluated `g` factors
   remain as left multipliers.  If `L_o` meant only the prefix before the
   base factor, the first wrong term would already be `H1_fyz`: the actual
   term is `G_yz D(K_yz)`, not `D(K_yz)`.
2. The successor must make the reduced canary observable and independently
   replayable: record the sorted 23 base-row digests/counts and the four
   typed atom signatures (including inverse/order gates), and have the
   nonimporting checker recompute them.  Merely changing the loop bound while
   emitting no receipt would not certify that the producer executed the new
   canary.  The complete `G`-bucket precision-two loop is unchanged.

These are finite text/schema/loop repairs.  They require neither another
all-path direct loop nor new mathematics.

## Audited inputs

The following are the exact bytes inspected.  The workflow is the actual v14
driver.

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/proof_r07_all_path_direct_canary_induction_v509.md` | 6,220 | `bee19b30ad8e3ced8905795566540626141d6623c1e8bcaf05e5389c0d0aff95` |
| `sol/proof_r07_direct_all_seven_signature_bucket_replay_v500.md` | 4,777 | `f0efc3d4292e512bfc8ff920c1c54ce31257310566c5e89b2981d287372a3318` |
| `sol/proof_r07_signature_bucket_source_ancestry_split_v507.md` | 5,496 | `760cd6dc51173e2327dd3a66a7a5db4112480ff4f5bfd3913a0d44dc9ee9e416` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` | 59,749 | `9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v6.py` | 98,228 | `8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v14.yml` | 12,320 | `6ce08d351d8db84448bcb4657ecbc13ba39dea7c0ddd7882b1a35265b486ada2` |
| `search/d972_r07_history_free_positive_fast_resume_v12f.py` | 343,155 | `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb` |
| `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 145,917 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| `scratchpad/a0_paper_words_v1.json` | 115,928 | `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893` |
| `search/d972_b345_seedspan_triple4_v1.py` | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| `sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md` | 8,731 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| `sol/proof_r07_endpoint_signature_precision2_consumer_v471.md` | 8,819 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| `sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v477.md` | 8,668 | `11aa7c86ddf2da6e936621534efa56d118d8546ece299b8952013835656b33e9` |
| `sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v478.md` | 5,131 | `a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b` |
| `sol/proof_r07_task640_endpoint_minimal_runtime_v484.md` | 6,571 | `25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492` |
| `sol/sol_reply_788_root_r07_a0_v14_resource_result.md` | 2,461 | `70d4f593f90c9531f42693cab0e0ef2a37418b699c6eecbbf9e3a23c026ab4d9` |

The producer definitions audited are `ProducerAllSeven` and its
`coordinates`, `occurrence_column`, `_pentagon_word`, and `direct_column` in
the pinned v12f owner; v8 supplies reached seeds, exact-key collection, atom
cache, trie, nonzero signature buckets and precision-two aggregation.  The
checker uses its separately written `IndependentAllSeven`, local Fox/group
arithmetic, independent leaf replay, trie, buckets and precision-two replay.

## 1. Independent crossed-Fox derivation

Fix one unsigned occurrence map and its pulled-back Fox derivative

\[
 \bar q_o=\eta_o\circ\theta_o:F(x,y)\longrightarrow Q_o,
 \qquad \bar D_o(w)=D_{\eta_o}(\theta_o(w)).
\]

The code uses the left convention

\[
 \bar D_o(ab)=\bar D_o(a)+\bar q_o(a)\bar D_o(b),\qquad
 \bar D_o(a^{-1})=-\bar q_o(a)^{-1}\bar D_o(a).
\]

For `C=P r_s P^-1`, direct expansion gives

\[
\begin{aligned}
\bar D_o(C)
 &=\bar D_o(P)+\bar q_o(P)\bar D_o(r_s)
   +\bar q_o(Pr_s)\bar D_o(P^{-1})\\
 &=\bar D_o(P)+\bar q_o(P)\bar D_o(r_s)
   -\bar q_o(Pr_sP^{-1})\bar D_o(P).
\end{aligned}
\]

The reached-seed gate is `bar q_o(r_s)=1`, separately in all six E3 and
five E4 typed slots.  Hence `bar q_o(C)=1` and

\[
 \boxed{\bar D_o(C)=\bar q_o(P)\bar D_o(r_s)},\qquad
 \boxed{\bar D_o(C^{-1})=-\bar q_o(P)\bar D_o(r_s)}. \tag{1}
\]

This uses no commutativity and no derivative of `P` survives.  It also shows
why the inverse sign occurs exactly once.  Coordinate zero is repeated as
the distinct slots `H1_fxy` and `H2_fxy`; both have the same endpoint bytes
but different block prefixes/signs.

The producer's `direct_column` has one stronger, implementation-only guard:
its lightweight joint evaluator checks E3 plus all 31 registered E4
contexts.  A successful empty-path call for each reached seed establishes

\[
 J_a(r_s)=1\quad\text{for every joint component }a,
\]

and therefore `J_a(P r_s P^-1)=1` for every path.  Thus the 23 base calls
also propagate this stronger guard; the eleven mathematical endpoint gates
alone should not be described as the source of that 31-context fact.

## 2. Literal expansion of the two hexagons

Write `G_ab=eta_ab(theta_ab(g))` and
`K_ab=theta_ab(P r_s P^-1)`; in expressions such as `D(K_ab)`, `D` is the
Fox derivative followed by the corresponding `eta_ab`.  The pinned
`pp_words` reverses displayed factors.  Therefore the actual words used by
`direct_column` are

\[
 H_1(f)=f_{yz}f_{xz}^{-1}f_{xy},\qquad
 H_2(f)=f_{uy}f_{xy}^{-1}f_{ux}^{-1}.                \tag{2}
\]

For `f=g(P r_s P^-1)` this is

\[
 H_1(f)=G_{yz}K_{yz}K_{xz}^{-1}G_{xz}^{-1}G_{xy}K_{xy},
\]

\[
 H_2(f)=G_{uy}K_{uy}K_{xy}^{-1}G_{xy}^{-1}K_{ux}^{-1}G_{ux}^{-1}.
\]

Using endpoint one for every `K`, and subtracting the corresponding base
rows, gives exactly

\[
\begin{aligned}
\Delta H_1={}&
 G_{yz}D(K_{yz})-G_{yz}D(K_{xz})
 +(G_{yz}G_{xz}^{-1}G_{xy})D(K_{xy}),\\
\Delta H_2={}&
 G_{uy}D(K_{uy})-G_{uy}D(K_{xy})
 -(G_{uy}G_{xy}^{-1})D(K_{ux}).                     \tag{3}
\end{aligned}
\]

The parenthesized full base products are required to be identity, but they
are the prefixes actually constructed before that simplification.  In the
registered slot order, (3) is precisely

| slot | label/sign | actual occurrence prefix `U_o` |
|---:|---|---|
| 1 | `H1_fxy +` | `G_yz G_xz^-1 G_xy = 1` |
| 2 | `H1_fxz -` | `G_yz` |
| 3 | `H1_fyz +` | `G_yz` |
| 4 | `H2_fux -` | `G_uy G_xy^-1` |
| 5 | `H2_fxy -` | `G_uy` |
| 6 | `H2_fuy +` | `G_uy` |

This agrees with the reverse-index prefix loop and with the rule that a
positive factor includes its base factor in `occurrence_prefix`, whereas an
inverse factor does not.

## 3. Literal expansion of the five-factor pentagon

Let `G_i,K_i` denote the five substitutions in natural context order
`i=0,...,4`.  The displayed helper input is `1,3,0,-2,-4`, and the paper
product reversal makes the actual word

\[
 P(f)=f_4^{-1}f_2^{-1}f_0f_3f_1.                    \tag{4}
\]

Thus

\[
 P(gK)=K_4^{-1}G_4^{-1}K_2^{-1}G_2^{-1}
        G_0K_0G_3K_3G_1K_1.
\]

After subtraction of `P(g)=G_4^-1 G_2^-1 G_0 G_3 G_1`,

\[
\begin{aligned}
\Delta P={}&-D(K_4)-G_4^{-1}D(K_2)
 +(G_4^{-1}G_2^{-1}G_0)D(K_0)\\
 &+(G_4^{-1}G_2^{-1}G_0G_3)D(K_3)
 +(G_4^{-1}G_2^{-1}G_0G_3G_1)D(K_1).                \tag{5}
\end{aligned}
\]

The last multiplier is the checked base pentagon endpoint and equals one.
In registered order this gives

| slot | label/sign | actual occurrence prefix `U_o` |
|---:|---|---|
| 7 | `P_b1 +` (natural 1) | `G_4^-1 G_2^-1 G_0 G_3 G_1 = 1` |
| 8 | `P_b2 +` (natural 3) | `G_4^-1 G_2^-1 G_0 G_3` |
| 9 | `P_b3 +` (natural 0) | `G_4^-1 G_2^-1 G_0` |
| 10 | `P_b5_inverse -` (natural 2) | `G_4^-1` |
| 11 | `P_b4_inverse -` (natural 4) | `1` |

Substituting (1) into (3) and (5) proves the repaired meaning of v509
(2.1):

\[
 \boxed{
 \mathscr D(s,P)=
 \sum_{o=1}^{11}\epsilon_o
     L_{U_o}L_{\bar q_o(P)}\bar D_o(r_s)+e(r_s).}    \tag{6}
\]

Here `bar D_o(r_s)` is the **unsigned substituted** seed derivative and
`epsilon_o=(+,-,+,-,-,+,+,+,+,-,-)`.  Equivalently, one may absorb
`epsilon_o` into the derivative of the signed relation, as the code does,
but not do both.  There is no mismatched direct term once `U_o` has the table
above.

## 4. Exponent coordinates

The two `E` keys are auxiliary coordinates, not eleven separately signed
occurrence rows.  Both implementations use

\[
 e(w)=(\operatorname{exp}_x(w),\operatorname{exp}_y(w))\bmod3.
\]

The direct side evaluates `e(P r_s P^-1)` and the occurrence side evaluates
`e(r_s)`.  Free reduction and conjugation preserve integral abelianization,
so these agree exactly before reduction modulo three.  They are independent
of `P`; no assumption that the pair is zero is needed.

## 5. Four-actor/right-trie induction

The actual source paths are freely reduced signed-letter lists with letters
`(-2,-1,1,2)`.  For every typed slot set

\[
 S_o(())=1,\qquad A_o(t)=\bar q_o(t),\qquad
 S_o(Pt)=S_o(P)A_o(t).                               \tag{7}
\]

The frozen group evaluators scan a word left-to-right with
`out=mul(out,image)`, and both production recurrence helpers use
`mul(parent,atom)`.  Thus (7), not `A_o(t)S_o(P)`, is the exact convention.
The signed atoms must additionally satisfy

\[
 A_o(-1)=A_o(1)^{-1},\qquad A_o(-2)=A_o(2)^{-1}
\]

on both sides.  Starting from the typed identity, induction over the full
exact prefix trie proves `S_o(P)=bar q_o(P)` for every reached prefix.  No further
mathematical anchor is needed; one independently evaluated noncommuting
two-letter fixture/anchor is nevertheless required to make reversal of (7)
hostile-test visible.

V509 (3.4) should not be implemented as right multiplication of the already
formed row `V(P)=S_o(P) bar D_o(r_s)`: in a noncommutative group algebra,
`S_o(P)A_o(t) bar D_o(r_s)` is obtained by first extending the endpoint and then
left-translating the fixed seed row.  The current trie follows this correct
order.

Signatures are formed only after canonical exact-key collection: v8 first
forms `complete=terms(raw_terms)`, then the trie, then keys
`(seed, full eleven-slot signature)`, and only then deletes coefficient-zero
buckets.  Equality of signatures is never used as equality of source words;
v507's exact source/ancestry track remains mandatory.

## 6. Exact executable repair and retained loops

For each side, replace only its `replay_bucket_direct(...)` production call
by the following bounded canary:

1. iterate the sorted raw reached-seed set;
2. call that side's unchanged `direct_column((), relators[s-1])` exactly once;
3. retain the complete returned sparse row, canonicalize it independently,
   and record `{seed, nnz, row_sha256}`;
4. require the completion count to equal `S`; and
5. record all four typed atom signatures in fixed order
   `(-2,-1,1,2)`, the two inverse equalities, and a noncommuting-order anchor.

The checker must recompute this table with `IndependentAllSeven` and its local
Fox/group code and compare the exact table/digest; it must not import the
producer.  A successful producer base call also establishes its stronger
31-context joint guard for that seed, which propagates by conjugacy.

The following complete work must remain:

- Task601/source/candidate authentication and exact ancestry/leaf replay;
- raw reached-seed extraction before cancellation;
- canonical exact `(seed,path)` collection and mod-three cancellation;
- all exact prefixes, four signed atoms, typed 11-slot trie, serialized path
  receipt and exact producer/checker comparison;
- canonical nonzero `(seed,signature)` table, coefficient/representative/zero
  gates and serialized receipt comparison;
- all 11 reached-seed endpoint checks;
- the producer precision-two loop over **all `G=21,287` buckets** (v8
  `evaluate`, current lines 581--592), including coefficients in `{1,2}`;
- the checker's independent precision-two replay over the same full bucket
  table (v6 current lines 616--623); and
- target construction, all 32,260 lower/auxiliary zero gates, all 48,384 top
  coordinates, packing roundtrip, receipts and false claim flags.

Only the nonempty bucket-representative generic H1/H2/P direct calls are
removed.  `direct_column` itself, its three printed-equation construction,
its base/occurrence comparison, and the 23 empty-path calls remain.

Required hostile mutations include at least:

- actor order: mutate `mul(parent,atom)` to `mul(atom,parent)`; the independent
  noncommuting two-letter anchor must reject it; and
- typed occurrence/sign/prefix: change slot 10 `P_b5_inverse` from sign `-`
  to `+`, or replace its prefix `G_4^-1` by identity; the contract/base-row
  canary must reject it.  The existing literal pentagon order anchor and an
  E4-to-E3 slot mutation must also remain live.

## 7. Actual count and scope

The terminal v14 log/result fixed

```text
L = 21,608 exact nonzero keys
U = 13,043 trie prefixes
G = 21,287 nonzero full-signature buckets
S = 23 reached seeds
```

Thus the generic `direct_column` schedule changes, per side, by

\[
 21,287\longrightarrow23,
 \quad 21,264\text{ calls removed},
 \quad \frac{21,287}{23}=925.5217\ldots .
\]

This is a 99.89195% reduction.  Across producer and checker the schedule is
`42,574 -> 46`.  At the observed late v14 rate of about four calls per 61
seconds, 23 calls correspond to about 351 seconds per side; this is only a
measured-rate estimate, not a runtime theorem.  The full precision-two
aggregation may become the next bottleneck.

| requested item | ruling |
|---|---|
| `FOX_CONJUGATE_IDENTITY` | PASS; exact left-Fox identity (1), all 11 endpoint hypotheses explicit |
| `PRINTED_ALL_SEVEN_TO_ELEVEN_SUM` | PASS after pinning the g-dependent `U_o` table and unsigned/sign convention |
| `EXPONENT_COORDINATES` | PASS; conjugation preserves both integral exponent sums |
| `FOUR_ACTOR_TRIE_INDUCTION` | PASS; identity + four signed atoms + `parent*atom` right extension suffice |
| `23_BASE_ANCHORS_SUFFICIENT` | PASS, with observable base-row receipt and producer joint-guard note |
| `FULL_PRECISION2_AGGREGATE_RETAINED` | REQUIRED YES; all 21,287 bucket actions remain on both sides |
| `SAFE_GENERIC_CALL_REDUCTION` | YES after the finite schema/loop/mutation repair above |
| `EXPECTED_CALL_REDUCTION` | `21,287 -> 23` per side; factor `925.52`; combined `42,574 -> 46` |
| `A0_IMPACT` | removes the measured generic-direct resource blocker only; fresh rho2/A0 remain unproduced |
| `verified` | `false` |

```text
VERDICT=PASS_WITH_EXPLICIT_FINITE_REPAIR
SAFE_TO_IMPLEMENT_SUCCESSOR=yes
SAFE_TO_DISPATCH_CURRENT_V509_TEXT_AS_IS=no
GENERIC_DIRECT_CALLS_PER_SIDE=23
FULL_PRECISION2_BUCKETS_PER_SIDE=21287
FRESH_RHO2=NOT_PRODUCED
A0=NOT_CLAIMED
COMMON=NOT_CLAIMED
COMPATIBLE_LIFT=NOT_CLAIMED
FAKE=NOT_CLAIMED
IHARA=NOT_CLAIMED
verified=false
```
