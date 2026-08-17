# Luna reply 157cf: literal-A.18 obstruction audit

## Verdict

`LITERAL_A18_OBSTRUCTION_AUDIT_FAIL`

The literal presentation and unconditional defect reconstruction are correct,
and the bounded d2 replay is clean, but the checker/workflow do not fail closed
on several required receipt metadata mutations even when the defect list is
empty.  These are release-blocking under task 157cf item 4.

## Mathematical and source audit

The producer takes the first 18 source rows as the K(0,5) prefix and applies all
five signed maps to all 28 seeds (`search/d972_b4_next_obstruction_v1.py:198-215`).
The maps are the literal A.18 maps, not a rho tail (`:62-68`, `:208-212`).
The temporary rho field is passed only for the legacy core parser and is marked
excluded from ideal/defect (`:218-235`); the actual core input has
`all_relators = prefix + a18` (`:221-230`).  The checker independently repeats
source, map, row, and presentation reconstruction (`search/check_d972_b4_next_obstruction_v1.py:179-218`).
The pinned semantic hashes agree:

```text
source       c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9
prefix       62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6
seeds        366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822
raw A18      1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722
presentation 783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305
Dtilde       32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef
word artifact 564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
```

`exact_dtilde` implements the required five-coface product, with the paper
order and inverses (`search/d972_b4_next_obstruction_v1.py:115-130`; checker
`:107-121`):

```text
f(x45,x34)^-1 f(x12,x15)^-1 f(x23,x34) f(x45,x51) f(x12,x23),
x51=x15, x15=(-3,-2,-1), x45=(-6,-5,-3).
```

For a genuine lift, equation (2.20) makes this five-factor product the identity
in the target quotient.  Replacing a frozen F2 representative by another one
changes it by an element of the marked kernel; every coface image of that
kernel is among the literal ideal generators, and normality absorbs the five
factor changes.  Thus the evaluated word is zero modulo the literal ideal.  No
condition that the chosen F2 word itself lie in `F2'` is needed for this
representative-independence implication.  This is only the conditional
semantic implication; the finite Magnus receipt does not itself prove that the
quotient is the semantic B4 quotient or that a row is genuine.

The checker independently builds the complete two-sided ideal with tuple
monomials and lowest pivots (`check_d972_b4_next_obstruction_v1.py:221-313`),
rechecks the ideal equivalence and all 158 relators (`:377-418`), and replays
all 972 Dtilde rows (`:420-452`).  There is no producer import or shared helper.

## Bounded checks

Passed:

```text
producer self-test: D972_B4_NEXT_OBSTRUCTION_V2_SELFTEST_PASS
checker self-test:  D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_SELFTEST_PASS
Python AST:         both source files PASS
workflow YAML:      PASS
embedded Python:    5/5 AST PASS
d2 shard/merge:     D2_ALLPASS_UNKNOWN
d2 dtilde rows:     972; nonzero defects: 0
independent d2 receipt replay: D972_B4_NEXT_OBSTRUCTION_D2_RECEIPT_CHECK_PASS
```

The d2 receipt had ideal rank 27, monomial count 43, quotient dimension 16,
and `D2_ALLPASS_UNKNOWN`; this is nonterminal, not an A/B conclusion.

Current source/core/workflow hashes agree with the pinned values:

```text
producer  a312bac0ed794d5a470db4c5a5ae82f4abed63c487b41aec33fef1f044e920cd
checker   4ff8b96178dfe04ad6c8509a27a3ee047aed1f777cdc9ff0104900d4b8f87443
workflow  76caa0e3395df7d12ef15849743cff53f42160285ae8566798be8ff9e7754a32
shard     1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63
merge-v3  6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5
merge-v2  c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c
```

The workflow has the intended 4 single-shard lanes plus 16 d6 shards
(`.github/workflows/d972-b4-next-obstruction-v1.yml:37-65`), exact source/selftest
gates (`:82-104`), shard evidence uploads (`:106-152`), complete shard-set
normalization (`:178-212`), merge receipts (`:214-264`), independent checker
(`:266-344`), and always-running fail-closed aggregate/evidence upload
(`:346-497`).

## Fail-open mutations (release blockers)

All mutations below were made only to temporary d2 receipt copies.  The base
receipt had zero defects, so acceptance as `D2_ALLPASS_UNKNOWN` is directly a
fail-open result.

| Mutation | Result | Relevant code |
|---|---|---|
| `degrees["2"]["shards"] = []` | **ACCEPT** | checker `:368-375`, `:420-452`; no shard-record validation |
| `literal_input_sha256 = "f" * 64` | **ACCEPT** | checker `:362-364` checks only string length |
| replace 27 `ideal_basis_pivots` by `[999]*27` | **ACCEPT** | checker `:399-403` checks shape/type only |
| degree shard `shard_index = 99` | **ACCEPT** | checker ignores shard records; workflow aggregate `:429-449` checks merge row but not its `shards` list |
| degree `rho_used = true` (and likewise `rho_tail_used = true`) | **ACCEPT** | checker only bans old rho field names at `:373-375`, not these degree flags |

Controls that did reject their bounded mutations: top-level `relator_sha256`,
top-level source binding, top-level stale `rho_words`, and a truncated Dtilde
ledger.  The existing fail-closed status fixtures are present at checker
`:471-479`, but they do not cover the receipt-level acceptance failures above.

Therefore the literal mathematics, maps, convention, independent ideal, all
972 coverage, and d2 result are sound as far as these light checks establish,
but the required adversarial receipt/workflow gate is not satisfied.
