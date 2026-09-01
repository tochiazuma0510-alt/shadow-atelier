# Task 511 independent audit — A4 actual-production shard wiring

## Verdict

`STOP_DO_NOT_ADOPT`.

The helper-only/assignment-only defect of Task502 is repaired: the v24 generated production body has live `build_kernel -> consume_row -> Oracle.query` call sites, and v43 executes its generated shell.  However, the actual v24 resume order corrupts the physical semantic continuation.  This is a reached production-path defect, not a helper-only objection.

## Exact pins

| object | bytes | SHA-256 |
|---|---:|---|
| v430 proof | 7137 | `acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904` |
| Task502 audit reply | 5061 | `c747e61c83579b4f886f77d42d9989fcf48aabde4e9d4442b55e2a7c8b55db79` |
| Luna Task503 task | 6913 | `8de80a222b68c051f360e46cfdcb2f2d3d95e9c233abeda6562e4bf5c2359e2a` |
| Luna Task503 reply | 3579 | `fc5b35b026c56016e6ba1a537501caf3d66948296da416784b60e1c743489d38` |
| producer v24 | 34535 | `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe` |
| generated producer | 285814 | `9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a` |
| checker v33 | 24033 | `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf` |
| generated checker | 312046 | `cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57` |
| driver v43 | 15449 | `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb` |
| frozen v22 / v31 / v41 | 4055 / 19483 / 2674 | `0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2` / `7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e` / `002dcea0d78bb14252e975ff69311f596aac742392658a9b7fb7022cf5c17bbd` |
| rejected v23 / v32 / v42 | 14472 / 10036 / 4362 | `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a` / `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0` / `650b1d052dbae8df65b2b8a4e8b7a33ab6f9c66d7b74117600e361b1dfa74629` |
| Task483 checker-only driver v3 | 13710 | `7fa72fb5a56dbbb2d6b50253883d5d5992c0f8ebedaae59c9cba71e81645add2` |
| v423 / v425 / v429 | 3899 / 6538 / 2845 | `4557b1f4789490b5797c04775a9173510314ae2abd20eb545d9951716407ee1d` / `96ebedf23592249a994631fd58c4b62979cfb51e1d1e204a743c43dbb44496ec` / `25ee7f1023db3de17933c24a3214049619e70767c87bf998bb01ca4e685d1fbb` |

V43's release pin is 56410 / `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a336e3`.  Its six member pins are: result 9300 / `7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5`; producer base 25581 / `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`; producer HEAD 700 / `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`; delta1 3551 / `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19`; delta2 3625 / `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523`; checker checkpoint 8991 / `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`.

## Bounded audit and findings

I hash-checked the wrappers, generated bodies, references and all release members; compiled/AST-inspected both generated Python bodies; inspected the reached v43 shell; and used a bounded generated-body harness with three real closed `_A4PhysicalShardStore` shards followed by the actual `build_kernel` resume block and a fourth close.  No production, GHA, git, or unbounded traversal ran.

- **F1 — PASS.** V24 has 35 exact positive patch cardinalities and nonzero active generated-result pins.  The generated non-SELFTEST path constructs one store and contains live `prepare`, `close_batch`, `direct_restore`, and `commit` calls.  Removing the helpers leaves unresolved live calls; it cannot restore the old owner silently.
- **F2 — PASS.** The live loop records exactly `m=min(64,len(private_candidates))`, one ordered candidate and mask bit per examined candidate, and one full entry per real accepted `LiveBasis.add_boundary`.  `expected_mask[0] == 1` in v33 is not an overrestriction: `dual_from_projection` annihilates the current combined span, while `correlate_private` retains `private[0]` only with nonzero dual pairing, hence its current remainder cannot be zero.  An honest mask beginning in zero is unreachable.
- **F3 — STOP.** The shard-before-HEAD close order and delayed completed-prefix appends are present, but completion durability is reversed.  The generated `consume_row` calls `physical_store.commit(query)` first; that immediately writes `obsolete=true` to the physical HEAD.  Only afterward does it append bridge/row/chunk/sample state and call the ordinary `write_checkpoint`.  A crash in that interval loses the only live physical continuation before the ordinary row delta exists, contrary to v425/v430's commit boundary.
- **F4 — STOP (executable counterexample).** The generated source executes `physical_store.direct_restore(...)` before the inherited `meter.install_completed(...)`.  Three closed shards ended with `semantic_after.active_keys=3`; direct restore installed 3, `install_completed` overwrote it with the ordinary row-26 value 0, and the reached fourth close sealed `semantic_before.active_keys=0`, not 3.  The bounded output was:

  ```text
  TASK511_BUILD_KERNEL_RESTORE_ORDER_STOP {'prior_after_active': 3, 'post_install_active': 0, 'fourth_before_active': 0, 'live_duals_expected_1_got': 4}
  ```

  Direct restore also appends one `live_duals` item per shard.  The uninterrupted implementation retains only the first live dual, so a historical length of 1 becomes 4 after three-shard restore.  In contrast, accepted-entry event accounting is correct: each stored accepted entry captures `self.event_chain[-1]`, and restore appends that query event exactly once; zero decisions have no entry.
- **F5 — PASS on the inspected terminal gates.** A closed chain selects the typed physical reference; the pre-first-close route remains the ordinary reference, and the claim flags remain false.  This does not cure F3/F4.
- **F6 — checker route PASS in isolation, end-to-end gate FAIL.** V33 neither imports nor calls v24.  Its actual acceptance route independently rebuilds the dual, prefix, mask, entries and transitions and retains v423/v429.  It will correctly reject the discontinuous fourth shard produced by the current resumed v24; therefore interrupted/resumed equality is not established.
- **F7 — PASS for the bounded dispatch envelope.** V43 actively authenticates both wrapper/generated pins, the release and six members; executes one producer with the stated 14400 s / 8 GB limits and margins; routes RESOURCE without checker; and permits at most one checker after a positive terminal.  Its script is executed, not merely parsed or assigned.
- **F8 — PASS.** No full physical-matrix snapshot, cumulative shard-prefix rewrite, dense conversion, worker pool, retry search, production SELFTEST, or extra closure was found.  The blockers above are state/durability defects, not cosmetic allocation concerns.

## Smallest repair boundary

1. In the resume block, run `meter.install_completed(...)` first, then invoke physical `direct_restore` exactly once, before deriving `_a4_correlation_rounds` or continuing the open query.  Keep direct restoration of physical maps/formals/records/accepted-entry events/dual-event chain once, but remove the per-shard `oracle.live_duals.append(...)`; the ordinary first-live-dual list is already restored.
2. On MEMBER/ZERO, durably install the completed prefixes and ordinary row delta exactly once before atomically marking the physical HEAD obsolete.  No path may expose `obsolete=true` while the ordinary delta is absent.
3. Add the real bounded regression: three closed shards -> CLI/build-kernel resume -> fourth close, asserting `shard4.semantic_before == shard3.semantic_after`, exact uninterrupted `live_duals`, maps/events/epoch/counters, and safe ordinary-delta/obsolete-HEAD order.

The mathematics does **not** change.  A4 remains `1/3 UNKNOWN_RESOURCE`, cross-checked only through row 26; there is no MEMBER/NONMEMBER/A4/fake/Ihara promotion and `verified=false`.

TASK511_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_AUDIT_STOP
