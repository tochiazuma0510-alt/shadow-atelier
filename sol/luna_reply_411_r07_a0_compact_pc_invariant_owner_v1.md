# Luna reply 411 — R07 A0 compact PC/invariant owner

## F1 Scope and authenticated inputs

Processed sections 1–6 in order. Only the four task-411 outputs were
changed. No legacy 1.66 GB checkpoint, adaptive search, SAT, mutation
campaign, local heavy production run, commit, or GHA dispatch was used.

The producer pins the joint receipt (2,166,036 bytes,
`1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`), q3
receipt (231,570 bytes,
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`), roof
input (31,017,244 bytes,
`82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5`), and
`acceptance_v2` (2,722 bytes,
`cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4`).
The bootstrap loader is task379 (`50355` bytes,
`125eb99d54764c546511741ac8eaefaa07c1fdaf2026117ee99fbfa4e6010627`),
which authenticates task198 v12/v6 (`7209`/`219187` bytes); task179,
task176, and g760 physical owners are independently byte-pinned in the
producer.

## F2 Compact presentation

The deterministic PC chain is `[1, 30, 12, 60, 3]`, with five relative
orders 3 and 243 normal forms. The authenticated action and Q0 endpoints
produce 15 internal, 10 marked-action, and 19 adjusted-Q0 relators: 44
literal relators in total, digest
`7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.

The registered, unadjusted Q0 defects needed by v399 are reconstructed from
the original Gamma source representatives, not the compact relators. Their
digest is
`bf24506f259414c3d375d5291c3014f1478b9b4ea73d389c07b7d10b07c82dc5`; entries
3, 9, and 12 have lengths 190, 344, and 902.

## F3 Closure implementation and honesty gates

The producer now uses the direct authenticated task198 v12/v6 bootstrap
(`load_task198`, `Meter`, `Runtime`) and `validate_layout`; it does not call
the v3 `restore_runtime`. Task179's physical `AllSevenModel` and g760 are
separately byte-pinned and bound to that runtime. It constructs the 2+2+11 typed
boundary seeds and 44 tagged correction seeds, closes signed actors,
aggregates only after retaining occurrence tags, and reduces the target
constructed as the negative of the three base Fox gradients.

Exponent rows use normalized `epsilon/18 mod 3`, with exact divisibility by
18; raw exponent mod 3 is not used. Seed/direct Fox replay is checked. The
sparse reducer copies each incoming row once, deletes zero coefficients
immediately, and uses a maintained pivot order. Dependent candidates are
not retained in the ancestry store. Phase metrics expose row nnz/max nnz,
total pivot nnz, frontier nnz, worker-batch bytes, and owner/worker RSS
slots. This first implementation is explicitly sequential: no worker RSS
or parallel speedup is claimed. Canonical v2 checkpoints now serialize full
sparse pivots, orders, live DAG/frontier, correction image, input digest, and
result with an atomic self-hash. After closure, the checkpoint also stores
the occurrence interner, compact pivots/order, physical pivots, remainder,
and an authenticated closure-state digest. During the 6,441-row oracle it is
atomically refreshed every 128 rows; `--resume` rebuilds the pinned runtime,
revalidates that digest, and continues at the saved cursor. The driver allows
at most two same-job continuation slices, only for `UNKNOWN_RESOURCE` with a
checkpoint. The advertised resume scope is therefore the oracle cursor with
revalidated compact closure (not arbitrary mid-closure process recovery).
Correction closure checkpoints at cursor zero and then on a bounded adaptive
cadence (512 pivots or five minutes), while progress remains visible every 32
pivots. The checkpoint stores the occurrence interner reverse table,
pivot/order/expression state, live frontier references, reachable nodes, and
binding digests; frontier entries store pivot references rather than duplicate
row copies. Oracle checkpoints include the occurrence expression map and an
explicit exhausted frontier.
Boundary and occurrence sparse rows now use one canonical integer interner;
serialization retains the tagged coordinate table for replay.

Rank-raising correction rows now receive hash-consed SCALE/ADD/CONJUGATE
expressions; dependent rows leave no retained DAG node. A zero remainder is
expanded once, exactified using the registered v399 words, replayed in the
joint runtime with exponent `(0,0)`, and reduced against the boundary image
to emit a typed preimage. The preimage is now a deterministic list of
`(block, base_relator_index, translation_word, coefficient)` records, not only
opaque physical pivot labels. A nonzero remainder is
held until the streamed 6,441-row oracle is exhausted. After exhaustion, the
producer emits a genuine triangular dual functional (support, hash, and
nonzero target pairing), rather than a pivot label. An old row outside the
compact span is typed `UNKNOWN_INPUT` because that is an equivalence mismatch;
only deadline/RSS interruption is `UNKNOWN_RESOURCE`.

## F4 Bounded gates and platform result

Passed:

```text
python -m py_compile search/d972_r07_a0_compact_pc_invariant_owner_v1.py crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py
R07_A0_COMPACT_PC_OWNER FIXTURE_PASS
R07_A0_COMPACT_PC_CHECKER_FIXTURE_PASS
task198 direct bootstrap symbol gate: PASS (`Runtime`, `Meter`, 11-row layout)
bounded cap probe: `R07_A0_COMPACT_PC_OWNER UNKNOWN_RESOURCE`
```

The bounded production invocation is intentionally not run locally after the
direct-bootstrap change: the frozen v6 owner gate is Windows-incompatible
(`authority.manifest:windows_same_handle_identity_unavailable`), and Linux GHA
is the permitted environment for the closure. No A0 membership, common word,
lift, fake, or Ihara witness is claimed locally.

## F5 Exact versioned hashes

```text
search/d972_r07_a0_compact_pc_invariant_owner_v1.py
  bytes=59733
  sha256=0c5e364a3ba3946081ea2551f2cc75331f29d4d570ed8b0613ffeccd1928c55f
crosscheck/check_d972_r07_a0_compact_pc_invariant_owner_v1.py
  bytes=44831
  sha256=7c1aea086ce264ad6f51983554a3a371ac481d07a2ec5f5d9a96ee270af6dfcf
search/d972_r07_a0_compact_pc_invariant_owner_gha_driver_v1.g
  bytes=3168
  sha256=075c3eec66029f2ffd4ea3a24ffdd3d6635ad2cbe6e9c33a54d076beff418f05
```

The driver pins the current producer/checker hashes and guards stale output.
No run ID or commit is claimed because dispatch remains parent-controlled.

**Terminal:** compact presentation cross-checked; direct-runtime A0 closure is
not locally certified because of the Windows owner gate. The GHA path contains
the compact closure, positive exactification, streamed oracle, and dual output;
the independent checker is being finalized by Sol(max). No witness is
certified.
