# Luna reply 385 - A4 canonical batch examined-cap repair v1

## Outcome

PASS.  The v14/v16 mathematical order, full correlation, and canonical
private roster are retained, while the producer and independent checker now
decode, translate, and current-basis-reduce exactly the canonical prefix

```text
examined = min(64, len(private_candidates)).
```

No candidate at index 64 or later (the 65th or later candidate) is accessed
by the batch loop.  A dependent current-basis reduction consumes one
`examined` position but does not increment `accepted`.  An independent one is
inserted chronologically with the unchanged ordinary
`BOUNDARY_RANK_RISE` record.  After the prefix, control returns to the
inherited outer query loop.

The first canonical candidate is required to have nonzero current remainder
and to be accepted.  The completed prefix is gated by

```text
0 < examined <= 64
0 < accepted <= examined
examined == min(64, len(private_candidates))
```

There is no implementation blocker.

## Physical artifacts

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v15.py` | 7417 | `964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v17.py` | 7574 | `0b0281af7d38f4c255f7cd3346dc816987da863a29275a2c6c1851366171cef0` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v24.g` | 5591 | `06dc70b8b4a4c2b97ed58d7c132c9346a4c01d123d68d41df5858c9d6479517e` |

The reply file is intentionally excluded from its own non-self-referential
identity table; its final identity is reported to the commissioner after the
file is closed.

## Frozen and generated-source pins

| owner/source | bytes | SHA256 |
|---|---:|---|
| frozen producer v14 wrapper | 11918 | `0c7595d50765062a6d2270d5b40c44b753f0ea4a96311795994a3c2502fe0c2c` |
| restored producer v14 generated source | 225853 | `952e559d363ae6c5261a057438ad3bfdfb1d85cc9f4417d714b85ed66fa9239c` |
| resulting producer v15 generated source | 226857 | `fe3c23ffb4c5c952f99eceba73cb8594885dbadd9d2c4bd50d8b28c173e46940` |
| frozen checker v16 wrapper | 12407 | `1470f12585d8ed16bb1dea0480787ba99d80592d3a034215cbbde20748f6090e` |
| restored checker v16 generated source | 265792 | `60973559b2f139dad471059b99746902a17b5ad5e52fba81288564303b8b05ec` |
| resulting checker v17 generated source | 266860 | `78409970ed60b7e5d97335592275716adb298ed85e65b49829c66bacc98f1d92` |
| frozen v6 driver | 13775 | `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0` |
| resulting v24 inner driver source | 14191 | `f18b0ac95380cc2d1a0bccf95375eb9b22ea92cd1bdba6772d89b21313258af4` |

All wrapper restoration gates require exact byte length and SHA256 before a
patch is applied and again after the generated source is produced.

## Patch cardinality

- Producer v15 has one direct replacement site in the restored v14 generated
  source.  Its old accepted-count loop occurs exactly once and the examined
  prefix replacement is applied exactly once.

- Checker v17 has two direct replacement sites in the restored v16 generated
  source: one exact producer-code path pin and one exact accepted-count loop.
  Each old site occurs exactly once.

- Driver v24 restores the exact frozen v6 driver, applies 13 exact
  path/output/physical-pin replacement pairs, and applies one exact
  diagnostic-tail replacement.  Every old site has cardinality one before
  replacement and zero afterward; every new site has cardinality one
  afterward.

The inherited v14/v16 transitive patches are not duplicated or rewritten.

## Direct examined-cap proof

Static AST inspection of each resulting generated Python source established:

```text
producer: one candidate_index loop, iterator = range(examined_limit)
checker:  one candidate_index loop, iterator = range(examined_limit)

examined_limit = min(CANONICAL_BATCH_CAP, len(private_candidates))
examined_limit == min(64, len(private_candidates))
```

In each source there is exactly one indexed access
`private_candidates[candidate_index]`.  It is inside that bounded loop.  The
loop contains the only candidate-specific `decode_token`, `translate`,
current combined-basis `reduce`, and `add_boundary` chain.  There is no direct
`for` loop or comprehension over `private_candidates`.  Thus a complete
correlation can perform those candidate operations at most 64 times.

The two implementations retain separate arithmetic owners: the producer uses
its ledger seed and basis implementation, while the checker independently
uses `boundary.by_key` and its checker basis.  Both use the inherited identical
canonical roster order and the same prefix index order.

## ABI, checkpoint, and terminal preservation

The patch does not add `examined` or the private roster to a receipt,
checkpoint, correlation object, or progress object.  The public correlation
fields and event record are inherited unchanged.  The existing
`accepted_batch_size` remains the number of actual rank rises, not the number
examined.

Because the producer changes only its unique batch-loop block, and the
checker changes only that block plus its producer path pin, v13 early
completed-row checkpoint behavior, v14/v16 current-combined semantics,
resource meters and caps, resume rules, and terminal contracts are retained.
The changed physical code pins prevent an old v13/v14 checkpoint from being
silently accepted as a fresh v24 checkpoint.

Driver v24 pins the physical v15/v17 wrappers and uses fresh v24 receipt,
verdict, producer/checker checkpoint, log, shell, and sentinel paths.  Its
reconstructed inner source retains the frozen limits:

```text
internal time limit: 14400 seconds
external timeout:    14520 seconds
RSS cap:             8000000000 bytes
modes:               PRODUCTION / RESUME
```

## Static checks

The following bounded checks passed:

```text
producer/checker wrapper ASCII decode
producer/checker physical AST parse and in-memory compile
exact frozen-owner restoration and generated-source SHA gates
resulting generated-source AST parse and non-main load
direct AST loop/index/call bound proof
patch-site cardinality and post-replacement gates
frozen v6 driver reconstruction, pin closure, and cap retention
v24 fresh-path and stale-checkpoint-path absence gates
GAP ReadAsFunction parse: TASK385_GAP_READ_AS_FUNCTION_PASS
```

No production, GHA, network, SELFTEST, mutation campaign, or result search was
run.  Therefore no runtime speedup, resource outcome, or accepted A4
word-bearing K is claimed.

```text
EARLY COMPLETED-ROW CHECKPOINT:                   RETAINED
CANONICAL CURRENT-BASIS EXAMINED CAP:            64
PUBLIC RECEIPT/CHECKPOINT SCHEMA MIGRATION:       NONE
INDEPENDENT CHECKER RECOMPUTATION:                RETAINED
PRODUCTION / A4 ACCEPTED WORD-BEARING K:          NOT RUN / NOT DECLARED
```

`TASK385_A4_CANONICAL_BATCH_EXAMINED_CAP_COMMISSIONED`
