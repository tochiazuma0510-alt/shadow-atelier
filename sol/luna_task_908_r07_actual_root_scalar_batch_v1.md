# Luna Task908 -- actual four-character root scalar batch v1

## Role and purpose

You are Luna.  Implement the narrow executable bridge from the now
cross-checked actual initial physical separator to the first four J3 scalar
tests.  This is implementation and bounded testing only; do not change the
mathematics, run GHA, use Git, or claim Grade-2 MEMBER/NONMEMBER.

The mathematical operation is fixed.  For the exact separator functional
`lambda` and each character `a=0,1,2,3`, form

```text
q_a = B_adj,a(lambda),
T_adj,a,t(q_a),  t in [1,-1,2,-2].
```

Pair those five covectors against the character-`a` slice of every one of
the 8,059 canonical P1 degree-two rows, reconstruct the already fixed 44 seed
and `4*8059=32236` actor scalar relations, and emit the first nonzero scalar
or an exact root-EOF for that character.  Do all four characters in one
sequential P1 cache pass.  This is only the four orbit roots, not yet complete
dual-orbit closure.

## Authorized files

Create exactly:

1. `search/d972_r07_actual_grade2_root_scalar_batch_v1.py`;
2. `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py`;
3. `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml`;
4. `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md`.

Do not modify any other file.  Temporary fixtures belong outside the
repository.

## Frozen mathematical parents

Reuse, with exact source-hash pins, the producer-side arithmetic in
`search/d972_r07_targeted_grade2_owner_generated_join_v15.py` and the
independent arithmetic in its checker counterpart.  The producer must not
import the checker and the checker must not import the producer.  Preserve:

- Task712 table authentication and transpose checks;
- `direct_seed_evaluations`;
- `_global_relations` on the actual Task554 prepare/four block bodies;
- scalar sign convention `_pair(direct, terms, values)`;
- `Violation`/`ScalarEOF` record meanings and canonical seals.

Production must use the actual parents below, never the private 16-row v15
fixture.

### Actual canonical P1

```text
run/attempt=33851744070/1
head=6673eb2ea15ca6022acc2ddc5a8a204a0380172f
artifact_id=9931437113
name=task809-canonical-p1-degree2-lift-v9-33851744070-1
archive_bytes=641518300
archive_digest=sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c
manifest.json=17472 bytes, sha256:86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb
degree2.cache.bin=292444992 bytes, sha256:b88edb9b12753cdb7a3629403f8ac14206595e03525fa2a201b6b00b985c1abf
instructions.jsonl=349055442 bytes, sha256:8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae
rows=8059; row_trits=145152; row_bytes=36288
```

Authenticate the exact manifest and all three file receipts.  The prior
cross-checked physical connection already replayed every instruction and
row, so this bridge must not spend another large JSON parse rebuilding the
same P1 DAG.  Hash `instructions.jsonl` as a byte stream; stream/hash the
cache while computing the scalar values.  Do not load either large file into
RAM.

### Actual Task554 relation parents

All five come from run/attempt `33677346616/1`, head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`, whose conclusion is the
accepted typed value `failure`:

```text
prepare: id 9865061266; task554-grade1-v3-prepare-33677346616-1;
         204360988 bytes; sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4
block-0: id 9865238399; task554-grade1-v3-state-block-0-33677346616-1;
         81729645 bytes; sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838
block-1: id 9865242284; task554-grade1-v3-state-block-1-33677346616-1;
         82259824 bytes; sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb
block-2: id 9865193269; task554-grade1-v3-state-block-2-33677346616-1;
         82200189 bytes; sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d
block-3: id 9865239848; task554-grade1-v3-state-block-3-33677346616-1;
         82266526 bytes; sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92
```

Read the exact canonical state HEAD/body objects and authenticate their fixed
body hashes/parent joins using the already accepted grade1/semantic formats.
Only the bodies needed by `_global_relations` are retained; do not mmap or
replay the large basis/packet blobs, and do not rebuild PB3/PB4 closure.
Require actual ranks `(505,503,503,503)` and `(1509,1512,1512,1512)`, exact
origin count 8,100, global row count 8,059, and relation count 32,280.

### Actual Task712

Use the exact accepted artifact already pinned by v15:

```text
run/attempt=33814194630/1
head=5ff2c5a30b604536df12acba8801828a5a7e5fe0
artifact_id=9915928157
name=d972-r07-grade2-maps-v4-33814194630-1
archive_bytes=22404961
digest=sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858
```

Load every character's one `B` and four `T` forward/adjoint pairs exactly
once.  Recompute each raw root from `B_fwd^T lambda` and each child from
`T_fwd^T q`; never trust caller-supplied q bytes.

### Actual cross-checked separator

```text
run/attempt=33891714539/1
head=7b7b9de20faaa3b8f26e331bb738b374f6f5708c
artifact_id=9944214057
name=d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1
archive_bytes=107195261
digest=sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017
```

Require the exact internal receipts fixed by Task907, in particular:

```text
state/manifest.json sha256 d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b
state/physical.bin 16377984 bytes sha256 1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e
output/lambda.bin 12096 bytes sha256 7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed
output/terminal.json sha256 098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf
output/result.json sha256 d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968
checker-result.json sha256 2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433
state_generation=8059; state_rank=1354
state_head=69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88
lambda_rho2=1
```

Stream all 1,354 physical rows once and independently confirm their dot
product with lambda is zero.  This is cheap and prevents a wrong-state join.
Do not rerun physical closure or target reverse substitution.

## One-pass scalar kernel

The P1 row contains four consecutive 36,288-trit character slices.  Compute
all 20 pairings (root plus four actor children for each of four characters)
in the same sequential cache pass.  Use exact sparse packed-trit projection:
for nonzero covector coordinate `i`, extract trit
`(packed[i//4] // 3**(i%4)) % 3`; sum coefficient times trit modulo 3.
Cross-check this kernel against dense unpacking in bounded selftests.  No
`8059 x 145152` dense matrix, no per-character cache reread, and no large
temporary copies are allowed.

After the one pass, run the fixed scalar relation order for every character:
44 seeds first, then `(basis_i, actor)` in row-major order.  Emit for each
character exactly one of:

- `RootZero` if `B_adj,a(lambda)=0`;
- the first canonical v15-compatible `Violation`;
- a canonical `RootScalarEOF` binding the underlying v15-compatible
  `ScalarEOF` and all 32,280 origins.

Also publish the exact packed root/four children and their Task712 table
identities so a later materializer or orbit continuation can consume them.
For every nonzero root EOF, publish its normalized one-pivot dual state
(lead, scale, packed row and rolling receipt); a violation is not silently
inserted.  Output character order is `[0,1,2,3]` and actor order is
`[1,-1,2,-2]`.

The terminal is `RootViolationBatch` if at least one character violates and
`AllFourRootEOF` only if all four roots are zero/EOF.  Neither spelling is a
complete-orbit EOF or Grade-2 decision.

## Independent checker and negative controls

The checker must authenticate the same exact launch/artifacts independently,
reconstruct all roots/children, make its own single cache pass, recompute all
scalar relations, and compare the complete terminal and file roster.  It may
use its own sparse kernel but must not import producer helpers.

Bounded public selftests must cover at least:

1. sparse packed projection equals dense unpack for all four offsets;
2. simultaneous 20-value pass equals four separate five-value passes;
3. seed and actor first-violation positions;
4. all-four root EOF;
5. zero root;
6. separator lambda/state-row mutation;
7. Task712 transpose/table mutation;
8. P1 cache truncation and digest mutation;
9. Task554 relation/order mutation;
10. result, q-child and scalar-prefix resealing attacks.

Keep selftests bounded.  Do not parse or generate the real 641 MB P1 object
locally.

## Workflow

Create one fresh workflow with sole marker
`[task908-r07-actual-root-scalar-v1]`.  It must:

- query and pin repository/run/attempt/head/status/conclusion plus every
  artifact identity above before download;
- accept Task554's exact `failure` conclusion and require `success` for P1,
  Task712 and separator;
- download each artifact directly into a fixed separate root;
- build a canonical launch with no caller-selected semantic path;
- run bounded producer/checker selftests;
- run the actual producer and independent checker with unbuffered minute-scale
  progress;
- upload diagnostic logs on failure and publish the final result only after
  both named executions succeed.

Use a 90-minute job cap and conservative per-process caps, but do not add
checkpoint/resume or unrelated hardening for this small one-pass calculation.
No old A0 exhaustive scan, SAT search, PB3/PB4 closure, physical-state rebuild,
or 349 MB instruction JSON parsing belongs here.

## Claim boundary and reply

Every embedded claim remains false/not-decided:

```text
ROOT_SCALAR_BATCH_CANDIDATE=true
COMPLETE_DUAL_ORBITS=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```

Report exact file bytes/LF/SHA-256, compile/selftest results, the workflow
marker and caps, and an honest expected resource envelope.  End with
`READY_FOR_SOL_AUDIT=yes`; do not say safe to dispatch before Sol(max) audit.
