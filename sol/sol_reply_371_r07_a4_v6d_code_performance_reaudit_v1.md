# Sol(max) reply 371 — independent A4/v6d code/performance reaudit v1

## 0. Boundary and decision

This was a source-static, read-only audit.  I used PowerShell inspection and
SHA-256 hashing only.  I did not run either candidate, Python, Node, GAP, GHA,
a workflow, git, the network, or a syntax compiler.  Thus none of the findings
below is a syntax, runtime, mutation, RSS, or workflow result.

The frozen v4 pair is **STATIC REJECT**.  Its authority graph and seven intended
mutation routes are source-statically coherent, but the advertised live-memory
account is not an allocation account, material duplicate canonical/hash work
remains, and the optional publisher does not cover every exceptional rollback
edge.  The rejection is confined to this rows-1--7 candidate; A4 remains 1/3.

## 1. Exact physical identities

All four task371 subjects matched physically:

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v4.py` | 102,525 | `4c32f9f9d80664c8f5ce962152f0f4f697d272f8ee77c102dda29b2b6578bde0` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v4.py` | 99,978 | `e0f27444aefffeb55f2d06637d0e1feb0f366239600262aeca9ce4e5c24c25c7` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v4_20260829.json` | 8,457 | `9bf92d19c8ebcabb8cb6a342508af60689e3c689979b065a7733052b499172b3` |
| `sol/sol_reply_367_r07_a4_v6d_complete_finite_repair.md` | 13,295 | `bcc85c3612c4ddc60d943b33ddd2eedb98e0d17987d757696755ae414ee49f66` |

The v3 lineage also matched: producer 94,299 bytes,
`22edde4e3c2fa00ad858f7aa8175774037c0f02ebd28eec27d83ffd184bb534c`;
checker 91,766 bytes,
`f9b1305d975a53309fff527aa9061aa3182fb3409a7e4003d35044cb98e64c25c7`;
fixture 8,457 bytes,
`0d58bace814a7b838f7bf08a91ca7e1eea79e7d4d5099b52281ea7cce61ed225`.

The immutable task198 graph matched as well:

| owner | bytes | SHA-256 |
|---|---:|---|
| receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| acceptance manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| task198 GHA driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

## 2. Fixture, authority, seal DAG, and baseline

1. Independent canonical reconstruction gives an 8,252-byte fixture body and
   self seal
   `f7d929846f069139bcfe148d07b072849b1f92d2dd9c782aa4a387b4d3467663`.
   The exact 8,457 physical bytes are pinned in both programs (producer
   24--28; checker 22--26), and the parsed body is checked at producer 563--570
   and checker 394--400.  The fixture contains no v4 program or task367-reply
   identity, so the dependency DAG is acyclic.
2. Removing the sole seal field from the canonical task198 owners gives receipt
   body 31,017,156 bytes with
   `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`,
   and manifest body 2,625 bytes with
   `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`.
   Each seal field occurs once.  The manifest's nested receipt binding and its
   six task198 source identities equal the physical owners above.  Producer
   423--445 and checker 285--307 traverse the complete receipt-to-manifest
   seal/binding graph.
3. Both stores open through a component-wise no-follow parent walk, `fstat` the
   one opened file before reading, compare the same fd after reading and against
   a fresh no-follow pathname identity, then retain all nine authority fds
   (producer 271--293, 318--346; checker 157--174, 190--216).  Fourteen full
   before/after scans recheck exact length, SHA-256, and identity (producer
   355--377; checker 224--243); final cleanup closes retained fds and evicts
   caches (producer 383--388, 922--926; checker 249--254, 713--717).
4. The checker literal independently reconstructs to exactly eleven rows, each
   with exactly twelve keys; row 11 has literal `context_id=28`.  Its canonical
   size is 2,385 bytes and digest is
   `040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`.
   The producer literal, checker literal, and task198 receipt agree.  The
   complete canary value is 16,464 canonical bytes with SHA-256
   `6fb8df36710628faded5438e993a21416809e05688fb66d0`, and the type/width/module/
   row-digest/coordinate-digest ABI checks are complete (producer 499--534;
   checker 346--377).  The checker untouched ordinary call at line 574 precedes
   its mutation loop at 579--589, so the corrected literal is not transformed
   away before use.

## 3. Rows 1--7 and case owners

Static control-flow tracing agrees independently on both sides (producer
636--771; checker 448--571):

| row | physical mutation | first ordinary rejection |
|---:|---|---|
| 1 | first presentation ordinal `1 -> 2`, receipt and manifest resealed | row order / `layer_ordinal` |
| 2 | manifest `accepted: true -> false`, manifest resealed | manifest acceptance |
| 3 | last receipt byte changed, no reseal | manifest receipt SHA identity |
| 4 | invocation-unique absent receipt path outside repository/workspace | path containment |
| 5 | normal-generation proof count changed, full downstream reseal | normal generation proof |
| 6 | occurrence block `H1 -> H1_mutated` (+8 bytes), full downstream reseal | bridge occurrence ledger |
| 7 | coordinate width `40 -> 41`, full downstream reseal | evaluator ABI canary |

The checker imports no producer helper.  `MutationAccepted` is outside the
narrow rejection catch, the narrow exception traceback is cleared before case
tokens are released (producer 750--769; checker 553--569), and per-case caches
are evicted in the outer `finally` (producer 777--794; checker 573--589).

Each ordinary case writer passes the concrete file, hence retains the actual
workspace parent fd and uses its leaf; all create/link/stat/unlink operations
are fd-relative (producer 661--734; checker 472--544).  Row 4 alone uses
`identity_kind=path` before and after, creates an invocation-unique external
parent, proves the leaf initially absent, and disposes it in both the narrow
route and outer `finally` (producer 644--648, 747--771; checker 456--460,
550--571).  These rows and case-owner properties therefore pass source-static
inspection; they remain unexecuted.

## 4. Independent resource arithmetic and load-bearing rejection

Let `S=315,289` (six source pins), `F=8,457`, `R=31,017,244`, and `M=2,722`.
The source formulas recompute exactly as follows:

```text
opened       = S+F+R+M + 3(R+M) + (R+8+M) + (M+1) + R
             = 186,443,551
temporary    = 3(R+M) + (R+8+M) + (M+1) + R
             = 155,099,839
parsed       = F + 5R + 8M + 9 = 155,116,462
DOM          = opened + parsed + 4(200,000,000) + 4(10,000)
               + 10,000 + R
             = 1,172,627,257
revalidated  = 14(S+F+R+M) = 438,811,968
logical opens = 19 owner opens + 20 case-writer opens
                + 14 retained-fd passes = 53
writes/events/mutations = 10 / 66 / 7
```

The `opens=53` label at producer 210--213/checker 122--123 is truthful only as
the stated logical account; it deliberately excludes component-directory OS
opens.  The exact *meter-token* peak arithmetic is also correct:

```text
B0 = 2S+8F+8M+8R                         = 248,857,962
row-6 case physical = 2(R+8+M)           =  62,039,948
row-6 parsed owner  = 6(R+8+M)           = 186,119,844
one canonical bound                            35,000,000
                                             -----------
modeled token peak                           532,017,754
```

That confirms 532,017,754 only as the code's intended token ledger, not as an
allocation peak and not as observed RSS.  The static cap nevertheless fails:

1. `canonical` first allocates a complete `str` with `json.dumps` and then a
   complete `bytes` with `.encode`, so both coexist (producer 216--228; checker
   125--134).  `canon_meter` reserves only one `bound`.  It therefore does not
   reserve every simultaneous canonical allocation before allocation, exactly
   where a receipt is about 31 MB.  Shallow `dict` copies, journal/record/result
   containers, and serializer/object overhead are likewise outside
   `live_peak_bytes`.
2. `json.loads` and `copy.deepcopy` are charged by fixed surrogates `6*raw` and
   200,000,000 rather than by a statically established object bound (producer
   403--420, 599--616; checker 266--283, 419--434).  Python container, integer,
   string, decoder, allocator, and traceback overhead is unmeasured.  The
   public field is nevertheless named `peak_live_bytes`, not
   `modeled_payload_tokens`.  Consequently the 750,000,000 cap does not
   constrain actual allocation or RSS.
3. The final exact-account assertion is made before the optional result is
   sealed/written (producer 795--797 versus 800--914; checker 590--592 versus
   594--706).  The same meter enforces remaining cumulative caps, but the
   already-created public resource snapshot does not report the optional two
   serializations, three logical opens, one write, or temporary bytes.

Cache lifetimes, retained fds, row-6 case eviction, and explicit traceback
clearing are otherwise coherent.  No runtime/RSS observation exists.

## 5. Avoidable material work

The task367 claim that remaining full scans are all required is false.
Immediately after `seal_receipt` has computed and stored `raw_sha256`,
`copy_manifest` hashes the same full receipt again (producer 574--587; checker
402--411).  Rows 1, 5, 6, and 7 therefore rehash
`4R+8 = 124,068,984` receipt bytes per program solely to compare a locally
created tuple with itself.

Moreover, exact receipt parsing serializes the complete DOM once and seal
validation immediately serializes the receipt-minus-seal body again (producer
403--431; checker 266--293), followed by a separate 6,441-row canonical/type
walk (producer 459--490; checker 318--345).  Baseline and rows 5--7 take the
full row walk four times, whose row-object canonical payload alone is
`4 * 30,533,732 = 122,134,928` bytes per program, in addition to the whole-DOM
serializations.  A streaming/fused canonical-and-seal pass can preserve the
same independent checks without these repeated full materializations.  These
are material GHA costs, not the contract-required fourteen fd revalidations.

## 6. Optional publication

The target-parent binding itself is correct: passing `ci/out/result.json` to
the helper retains `ci/out`, and normal success uses exclusive stage creation,
no-follow fd-relative file operations, fsync, exclusive hard link, exact final
fd/path identity, stage removal, parent fsync, and a final parent rewalk
(producer 804--864; checker 596--656).  A stale final is not removed.

The advertised all-exception transaction is nevertheless not established.
The transaction handlers catch `Exception`, not `BaseException` (producer 865;
checker 657), so an interrupt after publication bypasses rollback while the
`finally` only closes fds/releases tokens.  More directly, if rollback's final
unlink fails, `published` stays true, but the code raises the typed
`output:rollback_failed` at producer 867--903/checker 659--695.  That is a typed
non-PASS with a possibly published output, contrary to the required invariant.
Thus ordinary parent substitution is detected, but not every exceptional edge
ends in proved absence.

## 7. One bounded versioned repair

A single v5 producer/checker/fixture tranche is sufficient: (i) either use a
streaming byte serializer or account both simultaneous canonical outputs and
rename the ledger explicitly as modeled payload tokens while bounding all
claimed allocations; (ii) eliminate the local receipt rehash and fuse the
whole-object/seal/row canonical traversals without weakening the independent
digests; and (iii) make publication rollback cover `BaseException` and never
emit a typed no-output result when rollback absence was not proved.  Preserve
the seven mutations, their first reasons, immutable task198 pins, and exact
scope.  Until that new version is independently audited, execution is
forbidden.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
FIXTURE / AUTHORITY / SEAL DAG:        PASS
CHECKER BASELINE / ROW 11:             PASS
ROWS 1--7 ORDINARY MUTATION ROUTES:    PASS
CASE WRITER / ROW-4 IDENTITY:          PASS
STATIC CAPS / PERFORMANCE:             REJECT
AVOIDABLE DUPLICATED PROCESSING:       REJECT
OPTIONAL ATOMIC PUBLICATION:           REJECT
A4/V6D EXECUTION:                      FORBIDDEN
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE

TASK371_R07_A4_V6D_CODE_PERFORMANCE_REAUDIT_V1
