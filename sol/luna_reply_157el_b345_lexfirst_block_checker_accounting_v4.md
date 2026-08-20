# Luna reply 157el — completed-anchor accounting repair v4

## Status

The three authorized v4 outputs are frozen.  After Sol's static GO, the one
authorized combined lightweight self-test ran exactly once.  Producer and
checker both exited zero, every registered inherited/v4 marker occurred
exactly once, traceback count was zero, and all P/C/D hashes were unchanged.

Only checker wiring changed.  The v2 producer, receipt schema, output path,
receipt task hash, mathematical predicate, prefix replay, ordered block,
target-6 system, and terminal meanings remain byte-for-byte frozen.

## Frozen contract and active chain

The task was read in full and authenticated:

```text
sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md
755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a / 16945
```

Active chain at this static freeze:

```text
P(v2) search/d972_b345_lexfirst_block_target6_v2.py
  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
    -> C(v4) search/check_d972_b345_lexfirst_block_target6_v4.py
       f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533 / 21594
         -> D(v4) search/d972_b345_lexfirst_block_target6_gha_driver_v4.g
            fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836 / 14899
```

The reply SHA-256 and byte count are reported out of band because embedding a
file's final digest in that same file is self-referential.

Unchanged public contract:

```text
schema:       d972-b345-lexfirst-block-target6/v2
output:       ci/out/d972_b345_lexfirst_block_target6_v2.json
receipt task: sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md
task SHA:     1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290
producer:     ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a
```

## Exact repair

The v4 checker is a thin authenticated wrapper over the frozen v3 and v2
checkers.  It preserves the v3 exact three-key projection and the entire v2
independent replay.  At the sole completed-normal callback it separates two
types that the frozen v2 callback had conflated:

- checker-native replay accounting has exactly six keys: `columns`, `pivots`,
  `dependent`, `live_sparse_entries`, `pool_size`, and
  `pool_order_sha256`;
- producer public accounting has exactly those six plus `DAG_nodes`,
  `DAG_edges`, `section_bindings`, `section_expression_nodes`, and
  `section_expression_edges`.

The source-shape gate authenticates that the old bad callback, its independent
`basis.live_entries` argument, and `_validate_completed_core` each occur once
and in the frozen order.  The installed production wrapper executes that
callback once under a narrow argument capture, then:

1. exact-types the six-key independently replayed ledger;
2. preserves frozen `_replay_block` semantic equality and binds replayed
   `post_accounting.live_sparse_entries` to the independently replayed basis;
3. passes the authenticated `data["translation_block"]` and
   `data["post_block_anchor"]` to the unchanged eleven-key
   `_validate_anchor_public`, with that independent live-entry count.

It does not catch the old failure, synthesize public DAG/section fields,
compare private pool IDs/order, weaken an exact key set, or bypass the frozen
public validator.  The original `_validate_completed_block_anchor`,
`_validate_anchor_public`, `_replay_block`, and completed terminal branch core
remain load-bearing.

## Frozen pin ledger

The driver binds SHA-256 and byte count for every active and inherited input:

```text
157el task                    755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a / 16945
157ej P(v2)                   ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
157el C(v4)                   f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533 / 21594
157ek C(v3)                   bc0c1c4dfe2e4bc6ea8fd6c18e3af245d20e0959408649dd61d23f969cba9845 / 14032
157ek D(v3)                   2637e08c67e48bd0fca41e3b79a68be68344488734123d4043725d5c82971908 / 13805
157ek task                    af5bfe5182e66010fb8893a68ad9f02dda87389171ea425c4122c3fad8addb7c / 13686
157ek reply                   accf8cf58f511ebca7b30a1409be02a742a454762220df6c1ea9d9c69eb327b0 / 8603
157ej C(v2)                   fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba / 130007
157ej D(v2)                   48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394 / 13597
157ej task                    1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290 / 14667
157ej reply                   f00a3f56e140663002e85a488f78b37ade796126928d475f30bb57e951020428 / 8676
157ei P(v1)                   f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb / 143075
157ei C(v1)                   d0601533131008002d09a6320ab643df865a2a86245ed23f399e4c469bd93c57 / 128399
157ei D(v1)                   e0cb01bf119ae7834fa85da7910c6dd82048c8ae756e48f834fad055a7bc4c0a / 10516
157ei reply                   de6c22867a7a66cb28fdbbffae2f92632e8dfc382a5f7088a097d7518cef2ad2 / 13277
157ei task                    cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4 / 24179
157eh P(v2)                   6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f / 42449
157eh C(v2)                   881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060 / 21933
157eh D(v2)                   5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde / 13253
157eh task                    5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e / 15015
157ec P(v1)                   fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 / 535219
157ec C(v1)                   ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981 / 574347
157ec D(v1)                   a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4 / 9041
157ec task                    1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2 / 14751
q3 producer                  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755 / 76867
q3 checker                   ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73 / 89082
q3 driver                    c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831 / 5488
```

The checker authenticates v3/v2 and thereby retains their closed q3,
157ec/157ed/157eh/v1 pin gates.  The v4 driver additionally carries the full
explicit inherited list above.

## Regression contract and one combined self-test

The v4 checker first invokes the complete frozen v3 self-test, which invokes
the v2 fixtures.  The v4 additions use the same installed completed-core
wrapper as production and cover:

```text
semantic_public_accounting_split=1
semantic_ledger_as_public_rejected=1
public_ledger_as_semantic_rejected=1
public_only_omissions_rejected=5
public_relation_mutations_rejected=6
semantic_shape_mutations_rejected=2
replayed_live_entries_bound=1
completed_anchor_production_wrapper=1
eleven_key_validator_retained=1
completed_anchor_source_recurrence=1
inherited_v3_projection=1
```

The five omissions are the five producer-only DAG/section fields.  The six
public mutations are section increment, column increment, rank gain,
dependent increment, anchor binding, and anchor semantic digest.  Separate
mutations reject a replay-live mismatch, a missing/extra semantic key, and a
deleted/no-op eleven-key validator.

After Sol audit and explicit permission, the combined boundary ran exactly
once, producer first and checker only after producer exit zero:

```text
python3 -u -B search/d972_b345_lexfirst_block_target6_v2.py --self-test
python3 -u -B search/check_d972_b345_lexfirst_block_target6_v4.py --self-test
```

Result:

```text
producer exit: 0
checker exit:  0
traceback count: 0
log: C:\Users\81905\AppData\Local\Temp\d972_157el_combined_selftest_1787249438384.log
log SHA-256: 97686822a7bfd022804626bc4b4a696a9c1c1a7f022a0ae921de99139f5c59f5
log bytes: 2434
```

Exact-once marker counts:

```text
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_SELFTEST_PASS: 1
D972_B345_LEXBLOCK_TARGET6_V2_CHECKER_SELFTEST_PASS: 1
D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS: 1
D972_B345_LEXBLOCK_TARGET6_V4_CHECKER_SELFTEST_PASS: 1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_PRODUCER_SELFTEST_PASS: 1
D972_B345_FULL_D2_DUAL_CORRELATION_V2_CHECKER_SELFTEST_PASS: 1
prefix_projection_three_keys=1: 1
directed_base_support_consumed=1: 1
semantic_public_accounting_split=1: 1
semantic_ledger_as_public_rejected=1: 1
public_ledger_as_semantic_rejected=1: 1
public_only_omissions_rejected=5: 1
public_relation_mutations_rejected=6: 1
semantic_shape_mutations_rejected=2: 1
replayed_live_entries_bound=1: 1
completed_anchor_production_wrapper=1: 1
eleven_key_validator_retained=1: 1
completed_anchor_source_recurrence=1: 1
inherited_v3_projection=1: 1
```

Pre/post hashes were identical:

```text
P(v2) ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
C(v4) f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533 / 21594
D(v4) fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836 / 14899
```

No additional self-test or computation followed this run.

## Run 32397796696 boundary

Run `32397796696`, exact head
`f7dc097f2b9f317898f3e5035329235156561008`, failed after 19m49s.  q3 and the
unchanged P(v2) completed; P(v2) emitted exactly one candidate marker with
terminal `B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT`.  The v3 checker then
failed at frozen v2 line 453 with
`RuntimeError: checker complete block accounting relation`, after independent
32768-translation prefix and block replay.  Checker PASS and driver PASS were
absent, upload was skipped, and artifact count was zero.

Repository-external provenance-only log:

```text
C:\Users\81905\AppData\Local\Temp\gha_run_32397796696_1787248129247.log
3e2da0f3b54cab45d70102818592bb0de77dee3abc582ce36d9927ceb688bc15 / 196222
```

Stable logged producer phase timings were authenticated input 169.117504s,
source preflight 86.342308s, fresh prefix 104.089495s, raw-lambda 14.257491s,
correlation 1.104663s, section witness 0.008473s, block insertion 1.748643s,
and target reduction 333.197588s.  They are volatile provenance only.

There is no cross-checked terminal or artifact receipt.  The producer value is
a candidate only: it proves neither B1/full-D2 inconsistency, nonexistence,
failed lift, B4-A, nor B4-B.  The failed runner-local receipt is not an input;
the v4 contract requires a fresh same-job P(v2)+C(v4) run.

## Fresh cross-checked run 32401947156

The required fresh same-job rerun completed successfully:

```text
run:       32401947156
head:      2808c3fb61962d7180a192947fed375c754a25ce
URL:       https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32401947156
workflow:  success
job:       success
```

Step ledger (UTC): GAP setup `18:13:06--18:13:46`, bundled package
build/load `18:13:46--18:13:57`, math `18:13:57--18:37:54`, and artifact
upload `18:37:54--18:37:55`; all four completed successfully.  q3 producer,
q3 checker, unchanged P(v2), C(v4), and v4 driver PASS markers each occur
exactly once in their bounded logs.  Traceback and `RuntimeError` counts are
zero.  Common-deadline accounting is producer 708s, checker initial remaining
17292s, final elapsed 1420s, and final margin 16580s.

Artifact and receipt evidence:

```text
artifact id:      9419642796
artifact name:    gap-run-out
archive SHA-256:  1d764a5f1c5c6581229b636ad2a8d0d69ae3673412348e1a16e86eccd5c7f73d
archive bytes:    160648
receipt SHA-256:  746ca938a962f4d918c07ee270d4e03c3e4f75e40689f3a0507c8daff9d57053
receipt bytes:    1314365
canonical JSON:   true
producer log:     73470b1f7b7ebfe187d0e4b703a49f85c2b6fcbccbcf218cc85cb60cce80aee4 / 56786
checker log:      5540a67099c9f080e4e31854892bdf414bda995f9372460016e6c02fa05a0c97 / 753
artifact run.log: cf8c77a22a2289da47e2e8dbf6aebcbbf4befa8fd90e8979b575874df172a535 / 65974
job log:          e4a673e15162cd0aa1953294a029c936490531988150f2fe083d8fb39090d95e / 196924
```

The archive was downloaded again as raw ZIP and independently hashed to the
same GitHub digest.  Repository-external extracted evidence is at:

```text
C:\Users\81905\AppData\Local\Temp\shadow157el-run32401947156-94904c5163be43b7917a8e22cff2ece5
```

The terminal is cross-checked
`B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT`.  The complete correlation has 886
pair attempts, 724 nonzero-before-cancellation candidates, 156 cancellations,
568 active rows, and scalar distribution 284/284.  Its lexicographically first
active row is relator 9 with scalar 1 at translation ordinal 32976; the exact
154-byte translation has SHA-256
`b4e86ceeaee5ad995a64442abd9ba397322951feb80a6aad59215c0584ee2e7e`.

The one complete block contains all 11 relator columns, all independent:
rank gain and shadow rank are 11, relator 9 is independently pivoting, and its
actual pivot count changes `362717 -> 362718`.  The block changes public basis
accounting from columns/pivots/dependent/live
`362725/362709/16/3090367` to
`362736/362720/16/3090463`; the public post-block anchor matches exactly.

Target 6 was recomputed with 109 fresh remainders on that B1 basis.  The full
33687-coordinate, 108-variable system has rank 54, nullity 54, and is
inconsistent after complete absorption (not first-contradiction stopping).
The normalized dual has support 1, normalized RHS 1, `yTz=2`, and annihilates
all 108 registered directions.  Its sole coordinate is target 6,
`hexagon_1_coface_0`, component 4, with exact element-byte SHA-256
`0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903`.

Producer receipt runtime is 707.496644s with peak RSS 787005440 bytes.  The
cross-process state-no-mutation gate is exact, no old B0 remainder/dual was
imported, no full E4 enumeration occurred, and the independent checker replay
passed.

The result is limited to the exact 108-variable target-6 affine system after
the single fixed lex-first 11-relator block over the frozen prefix.  It is not
a full-D2 obstruction, global nonexistence theorem, failed lift, B4-A, B4-B,
or a result for targets 7--33.  It is cross-checked, not Lean-verified.

## Recurrence-prevention table

| Boundary | Required type/gate | Forbidden recurrence | Static result |
|---|---|---|---|
| replay block | exact six-key checker-native ledger | use as public provenance | PASS |
| semantic equality | ordered replay plus four basis counts | compare private pool/DAG/section IDs | PASS |
| public validator | authenticated eleven-key receipt block | synthesize five missing fields | PASS |
| anchor | producer anchor plus independent replay live count | trust producer live count alone | PASS |
| prefix input | inherited v3 exact three-key projection | regress to old two-key projection | PASS |
| fixture | installed production completed-core wrapper | toy-only validator/early return | PASS (static) |
| terminal | fresh same-job producer and v4 checker PASS | promote failed candidate | PASS |

## Static audit and scope

```text
checker AST parse: PASS
driver ASCII-only: PASS
driver lexical quote/bracket audit: PASS
checker source-shape recurrence: PASS
six-key semantic shape closed: PASS
eleven-key public shape and original validator retained: PASS
v3 three-key projection retained: PASS
driver P(v2) -> C(v4) active paths: PASS
driver v2 schema/output preserved: PASS
unfinished-token scan: 0
combined self-test: PASS, exactly once
local GAP/full/Git by Luna: NOT RUN
authorized GHA full run: PASS, recorded above
```

Scoped status at freeze contains only the pre-existing task and the three
authorized new outputs:

```text
?? search/check_d972_b345_lexfirst_block_target6_v4.py
?? search/d972_b345_lexfirst_block_target6_gha_driver_v4.g
?? sol/luna_reply_157el_b345_lexfirst_block_checker_accounting_v4.md
?? sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md
```

The wider shared worktree was already dirty; no unrelated file was modified.

READY_FOR_GHA
