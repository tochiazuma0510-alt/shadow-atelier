# Sol(max) Task639 reply: successful Task625 selected-SLP artifact audit

## Verdict

`PASS_SELECTED_SLP_PARENT`.

The immutable producer payload, independently completed checker, and this
external artifact audit accept run `33734643746/1` as the selected-SLP parent
for a new versioned Task630/v478 precision-two consumer.  All fifteen payload
receipts match the downloaded bytes, their size equation closes, the staged
statistics agree, the three roots have the required order and arities, the
standalone checker exhausts the complete 8,059-object physical route, and all
forbidden claim flags remain false/null.

The stored `cross_checked=false` is correctly retained as a self-promotion
guard inside both producer objects.  Acceptance here comes from the immutable
producer plus independent checker plus this external audit; it does not
rewrite that stored field and does not promote any later grade.

No implementation or theorem was re-audited, no full computation was rerun,
and no production, GHA dispatch, or git operation was performed.
`verified=false`.

## Exact audit input and run binding

The Task639 instruction is 4,003 bytes with 103 LF and SHA-256
`aea71220c6d894ce71d78009471e4f13c5ce7cf490ddb7613b79c5413d784065`.

```text
workflow  d972-r07-a0-grade1-selected-slp-staged-v3
run       33734643746
attempt   1
job       100582244001
head      b401d724bbdbef8cf67e96def22fc51c014ab546
conclusion / main step / payload upload / log upload
          success / success / success / success
```

The immutable artifact envelope is:

```text
payload id/name   9885925239
                  task625-grade1-selected-slp-staged-v3-33734643746-1
archive bytes     50,793,121
archive digest    sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75

logs id/name      9885925893
                  task625-grade1-selected-slp-staged-v3-logs-33734643746-1
archive bytes     3,770
archive digest    sha256:7cd8678a48dc0036beb0d1f887e1680145be8d1987272f35c9cce57982f0b86e
```

The four required downloaded files match exactly:

| file | bytes | SHA-256 |
|---|---:|---|
| `manifest.json` | 9,034 | `381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22` |
| `task625-verdict.json` | 1,120 | `a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740` |
| `producer.log` | 6,921 | `bfb54eb7decf3cd712f8dc225d33b7e12c5dc13cbd9a186fbba5b9553b7d8bdf` |
| `checker.log` | 8,982 | `5ee903d35000a38e654973acb853fed41a78e698a9736847dad3d4d16db922e3` |

## Fifteen payload receipts

Every listed file was hashed from the downloaded artifact rather than copied
from the instruction or manifest.

| manifest key | file | bytes | recomputed SHA-256 |
|---|---|---:|---|
| `grade_edges` | `grade-edges.bin` | 12,372,120 | `aa3a506fd2f1358e6edce102d5fb6f129a4b75bd2675e03bb401f01904e47557` |
| `grade_nodes` | `grade-nodes.bin` | 146,276 | `6b79485d9c69a05cf0d6c64788bc4f341792c8cedbb4f00cd1fdc887d42ca82b` |
| `grade_origins` | `grade-origins.bin` | 30,506,112 | `fcc5e5e43a9923b549e0b894c8ab995e545f78563134f37dae99917026283e68` |
| `literal_leaves` | `literal-leaves.bin` | 565,981 | `4a0b631004c9fbbf0b3cc965ff606711e04081c7d79beecb2db6b7be264fc851` |
| `lower_companions` | `lower-companions.bin` | 10,045,728 | `299ff5f214d32a85bea401705bffe01b2cf4f4f327c50a34f26fed1ba433dcaa` |
| `lower_edges` | `lower-edges.bin` | 1,911,741 | `b83e05df054d43952640b4442f08fb54aadf3303675dedc5443268aa3c3e9809` |
| `lower_nodes` | `lower-nodes.bin` | 48,169 | `4e9b5a98f9b434649d3eeac664fdcdc029d81a1247b193cb3260dabe2c22ee3c` |
| `lower_origins` | `lower-origins.bin` | 3,350,237 | `1cbbb4444858828d9b3ddb78c799a087c6ada69b058155f02d11e5f63316135c` |
| `lower_stored` | `lower-stored.bin` | 3,350,237 | `50361df9c85a525e0c3f73a2ef82a337a870b3cb4eb30caad5816df49c98a683` |
| `old_lower_zero` | `old-lower-zero.bin` | 712,001 | `f2793fac59ae4cb798f479f764eb494b5db51256fb7d01dfc523000a7b217a33` |
| `roots` | `roots.json` | 255,846 | `af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5` |
| `selected_grade` | `selected-grade.bits` | 631 | `e2fd7f3147f4880e42d6da6f211f2ed7991af9d9d1925416ec30120c46ac832a` |
| `selected_lower` | `selected-lower.bits` | 208 | `771af58b72061d7c94ec28c9086c375bf4e1c5b55254cbb11a541fea4093d48e` |
| `source_ancestry` | `source-ancestry.json` | 149,359,882 | `315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908` |
| `source_refs` | `source-refs.json` | 19,876,945 | `18767d10ab9e697c5f9cb54fbdcabfbc1824c0f4e0afde15e0e550e4a3b781ea` |

All fifteen size and hash comparisons pass.  Their exact size equation is

```text
receipt count                         15
sum of fifteen receipt bytes          232,502,114
manifest bytes                              9,034
inclusive payload bytes               232,511,148
producer/checker declared payload     232,511,148
```

The manifest root pointer is exactly `roots.json`, equal to the filename in
the authenticated `files.roots` receipt.

## Parent and route equations

The manifest/checker bind the registered Task554/Task595 parents:

```text
prepare SHA      1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865
decision SHA     62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d
block SHAs       9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74
                 d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6
                 a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac
                 642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01
basis SHA        b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d
zero remainder  564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0
```

Both the manifest and final checker equation give:

```text
cursor                         8,059
lower / grade offers           2,014 / 6,398
lower / grade ranks            1,661 / 5,044
ordered nonzero coefficients   3,317
```

The producer reaches `route-member-physical-closure-complete`, seals the
canonical graph/leaf payload, and ends with the same cursor, ranks,
coefficient count, and inclusive payload bytes.  The checker then completes
all four independent old boundaries, all four independent block boundaries,
and `basis-member-complete`; its standalone route ends at logical cursor
8,059 with ranks 1,661/5,044 and 3,317 coefficients.  Thus neither the basis
nor the zero-remainder MEMBER equation is inferred from the staged leaf
receipt.

## Staged graph, leaves, and roots

The producer and checker each complete the twelve ordered stages

```text
physical-grade, physical-lower, block-0, block-1, block-2, block-3,
defect, old-0, old-1, old-2, old-3, leaves.
```

This is exactly the required `G,L,B0..B3,D,O0..O3,leaves` schedule.  All
twelve observable deterministic stage records agree between the producer,
checker, and manifest.  The independently summed totals are:

```text
processed nodes             14,920
expanded states             46,629
state-edge traversals     7,682,296
accumulated states        2,605,954
interned exact paths          2,565
maximum path length               24
maximum live entries          25,267
terminal leaves               19,393
```

The checker final receipt binds the exact leaf-stream SHA
`4a0b631004c9fbbf0b3cc965ff606711e04081c7d79beecb2db6b7be264fc851`,
the ancestry SHA
`315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908`,
and the roots SHA
`af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5`.
Its final marker is exactly
`R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS`, and it additionally binds:

```text
payload manifest SHA       381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22
staged manifest SHA        7b41dee023880fd43e2a5303d8c68968bac731cb6c8e966782e404e318953703
staged projection SHA      acc7ac15e36e15c825e84950b64a8330dacc033dc7f705802928e0a0a7a3fa13
staged theorem SHA         757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e
```

The authenticated root object has exactly:

```text
C_T   type OrderedProduct;          3,317 ordered GradeNodeRef children
C_<1  type RegisteredPriorProduct;  2,622 stored terms
C_1   type Compose;                 left C_<1, right C_T
```

This preserves “prior followed by update”; it is not an additive or
commutative source-word replacement.

## Claim flags and resources

Both `manifest.json` and `roots.json` independently retain:

```text
direct_occurrence_replay = false
next_degree2_residual    = null
A0                       = false
COMMON                   = false
FAKE                     = false
IHARA                    = false
cross_checked            = false
verified                 = false
```

The checker verdict also has `cross_checked=false` and `verified=false`.
There is no embedded precision-two residual or self-declared mathematical
promotion.

All reported resources are within the declared caps.  In particular, the
checker peak is exactly `5,505,130,496` bytes: about 5.505 decimal GB
(5.127 GiB), below the 7-GiB RSS cap `7,516,192,768`.  Its terminal elapsed
time is about 711.175 seconds, below the 2,400-second wall cap.  The producer
peak is 2,698,469,376 bytes and its elapsed time is about 464.288 seconds;
the 232,511,148-byte durable payload is also below its 7-GiB cap.

## v220 mapping and handoff boundary

This artifact materializes the already decided and cross-checked grade-one
update as an exact canonical selected SLP.  It is now an accepted parent for
constructing and independently checking the fresh precision-two residual.
It does not itself contain or decide that residual.

```text
v220 A0 actual:                         0 / 1
v220 first-rung grades cross-checked:   1 / 6
selected grade-one SLP parent:          ACCEPTED
fresh rho2 consumer:                    UNLOCKED, NOT YET RUN
grade two / complete first rung:        NOT DECIDED
full A0 / cofinal lift:                 NOT DECIDED
COMMON / FAKE / IHARA:                  NOT DECLARED
verified:                                false
```

`R07_TASK625_SELECTED_SLP_PARENT_ACCEPTED_RUN_33734643746`
