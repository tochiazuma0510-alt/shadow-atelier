# Sol(max) Task760: A0 endpoint-hotspot v7 finite release audit

## Decision

The four finite blockers from Task756 are repaired.  Producer v7 preserves the
checker-v4 wire contract, enforces both parent and atom slot tags, implements
the proved right recurrence, and contains a genuinely noncommutative signed
order fixture which rejects the reversed-product mutant.  Workflow v12 pins,
tests, and invokes the audited v7 producer and the unchanged checker v4 while
preserving the immutable-parent gates.  I found no load-bearing finite blocker
to one authorized GHA dispatch.

This is a static/bounded release ruling.  It is not a prediction that the
remaining required direct-row arithmetic will finish within the outer timeout.
No real parent, prior artifact, endpoint payload, or GHA job was used.

## Audited bytes

All listed files are LF-only, contain zero CR bytes, and end in LF.

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_760_audit_r07_a0_endpoint_hotspot_v7.txt` | 3,395 | 72 | `9b2d167ed80f490c2b0694d38c954576cecf5bd3d8336815be362e43f02dc199` |
| `sol/proof_r07_endpoint_signature_monoid_cache_v495.md` | 3,937 | 112 | `fd3f5cf0195fe0e018aea37dc9db0c240cce6a051ba770af865627a70b5c88a2` |
| `sol/proof_r07_endpoint_timeout_localization_repair_v499.md` | 2,190 | 58 | `b866f5df65e016accb68968b8231f295eb1aeae943039da07e803d44ade6fbfe` |
| `sol/sol_reply_756_audit_r07_a0_endpoint_hotspot_v6.md` | 14,453 | 289 | `51ecd5688ce84e479934bf0935762b4f02be7054749b42330bbf12c8c2f39a96` |
| `sol/luna_task_759_r07_a0_endpoint_hotspot_v7_and_workflow_v12.md` | 3,797 | 86 | `c9a888a0c0a4b1ecb2435ac97a6dd0c34e567377680e29d03c0128ab6543cb4d` |
| `sol/luna_reply_759_r07_a0_endpoint_hotspot_v7_and_workflow_v12.md` | 5,482 | 123 | `d4ce3fafcae54a0865f23baaab91a753d5921dfba2f29d3c9613aaa1a0af5a51` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | 43,838 | 671 | `2f8cb910c79cb6046c8cd7a83f77e9e883187fe81b43209e3a8d09679a12ad6b` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v6.py` | 52,114 | 859 | `81265a0e198d0228bd10871c92e7f6944b8c4c48f0909d0002df49911e47e734` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py` | 54,803 | 925 | `6e26e6b96eb610e29dfd191040cea604e7768a643ed2ef916033c8449373e465` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v11.yml` | 11,866 | 182 | `b1b5dce5dbd97364d019420d47e6325073b48c33822360671bfe2f5e174d88e9` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml` | 11,976 | 183 | `1ac07ad79e218f7926e1db95bf19fcfa94042dc80c4f80fadcb32815015f2d3d` |

## 1. Task756 blockers

### Wire contract

V7 deliberately emits

```text
schema = d972.r07.a0.fresh-precision2-endpoint-signature.v4
marker = R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE
```

and its `occurrence` object has exactly the checker-v4 eight keys:

```text
count, types, coordinates, signs, base_checks, max_base_checks,
all_seven_canary, first_six_typed_restriction
```

There are no profiling-only keys.  The complete manifest AST, including all
claim flags, is identical to accepted producer v5's manifest AST.  Checker v4
requires the same schema, marker, key set, and exact occurrence value.

### Typed right recurrence

`extend_signature` first requires the cache binding and an existing/non-`None`
atom, then requires both signatures to have eleven slots.  In each slot it
requires the parent and atom tags to be `E3` for slots 0--5 and `E4` for slots
6--10.  It emits that expected tag, unpacks with the matching quotient block,
and computes

```text
quotient.mul(parent_value, atom_value)
```

so the implementation is exactly (S(pa)=S(p)S(a)).  A missing cache key is
rejected by the exact cache binding, an explicit `None` atom is rejected as
`endpoint_atom_missing`, a missing slot is rejected by the width gate, and the
bounded fixtures reject mislabeled parent and atom slots separately.

The fixture uses a 3-cycle and a transposition in both degrees.  In E3,
`(1,2,0)` and `(1,0,2)` have products `(0,2,1)` and `(2,1,0)` in the two
orders.  In E4, `(1,2,3,0)` and `(1,0,2,3)` have products `(0,2,3,1)` and
`(2,1,3,0)`.  Thus neither block is accidentally commutative.  All four
two-letter order cases agree with direct evaluation and reject the explicit
reversed order in both E3 and E4; two cases end in a negative atom, and the
other signed cases also exercise a negative parent atom.  Independently
replacing the sole production expression `mul(left,right)` by
`mul(right,left)` made the bundled selftest fail with
`fixture_recurrence_direct_equality`.

### Logging

The two large phases have exactly these four unconditional boundary calls:

```text
endpoint_direct_column_start
endpoint_direct_column_complete
endpoint_precision2_aggregation_start
endpoint_precision2_aggregation_complete
```

Inside each item loop there is one retained resource `guard` and one direct
`Meter.check(done/total)`, with no `endpoint_checkpoint` and no unconditional
print.  The pinned `Meter.check` emits only when at least 60 seconds have
elapsed since its previous meter emission.  Atom and reached-seed boundary
logging remains bounded by 8 and 88 lines respectively.

### Workflow v12

The workflow authenticates the actual v7 bytes and digest above, as well as
the unchanged checker-v4 bytes and digest.  Its compile/selftest step names v7
and checker v4, and the production step invokes those same two files.  The
fire token is exactly `[fire-fresh-precision2-endpoint-v12]`.

After normalizing only the v12 names/token/artifact labels, the v7 producer
path/size/digest, and the added checker-size assertion, workflow v12 is byte
for byte equal to v11.  Consequently the exact Task625 run, attempt, job,
head, workflow, artifact identity/digest/size, verdict staging, Task554 and
Task595 downloads, paper/source pins, authentication gates, pipe-fail logs,
success-only result upload, and always-run log upload are unchanged.

## 2. Production call graph and v5 noninterference

This was checked on the call graph, not by literal counts alone.

1. `build_endpoint_minimal` constructs the producer, authenticates deletion of
   the E4 identity to the E3 identity, and calls `identity_signature`; none of
   those paths calls `ProducerAllSeven.coordinates`.  The pinned
   `ProducerAllSeven.__init__` likewise does not call `coordinates`.
2. The only production caller of `signature` is `build_atom_cache`.  Its one
   fixed loop visits `ATOM_LETTERS=(-2,-1,1,2)` exactly once, contributing four
   generic coordinate evaluations, including both signed inverse atoms.
3. Trie construction starts from the explicit eleven-slot identity and calls
   only `extend_signature` for a new edge.  It performs no direct empty-word
   evaluation and no full-prefix `signature` comparison.
4. The only remaining production `coordinates` call is inside the loop over
   `reached_seeds`.  `raw_seed_gate` produces a set of seed integers in
   `1..44`, and the loop calls it once per seed.  Hence its contribution is
   exactly (R), with (0\leq R\leq44).

Therefore the generic endpoint-signature count is exactly

```text
empty word                   0
actor atoms                  4
full-prefix direct replay    0
reached seeds                R, 0 <= R <= 44
total                        4 + R
```

The separately required `direct_column` call remains once per canonical
complete term; its internal joint-kernel check is not a generic signature
replay and was not removed or counted as one.

AST comparison against v5 found the exact authentication and universe helpers
unchanged: paper pins, context/Q0 gates, parent receipts, literal-leaf replay,
candidate binding, state binding, free reduction, mod-3 canonical terms, and
raw reached-seed selection.  Within `evaluate`, the following production
expressions are AST-identical to v5:

- `prior + replaced`, canonical `complete`, path universe, and base-check
  ceiling;
- every `direct_column(path, relator[seed-1])` call;
- `(seed, full_signature)` bucket keys, mod-3 coefficient accumulation,
  zero-sum deletion, and `G <= L`/state-cap gates;
- all 44 precision-two seed rows, `act_precision2`,
  `aggregate_precision2`, and replay accumulation;
- direct target, difference, 32,260-coordinate lower-zero gate, 48,384 top
  row, 12,096-byte rho2 packing, and pack/unpack roundtrip;
- path/bucket serialization, receipts, sparse digest, parent object, and the
  complete v4 manifest.

The v495 monoid-cache replacement therefore changes only redundant generic
endpoint evaluation and the commissioned progress plumbing.  It does not
alter the candidate universe, direct columns, bucket relation, precision-two
arithmetic, lower-zero requirement, or rho2 bytes.

## 3. Narrow performance audit

No accidental dense materialization, whole-family copy, repeated prefix
evaluation, or per-item forced logging was introduced by v7.  The new
production state is only one eleven-slot identity and four eleven-slot atom
signatures; each trie node already required its stored signature.  The
existing `complete`, trie, buckets, 44-row precision-two cache, replay arrays,
and final `path_rows`/`bucket_rows` output serialization are inherited from v5
and remain contract-bearing.

The still-required direct-column family and precision-two aggregation can
remain expensive.  Whether they finish in the GHA time envelope is unknown;
a mathematical acceleration of those rows is outside this finite release
audit and is not a v7 blocker.

## 4. Bounded probes

Only source reads, in-memory AST/source mutations, selftests, hashes, and YAML
parsing were used.

```text
producer-v7 compile:                         PASS
checker-v4 compile:                          PASS
producer-v7 --selftest:                      PASS
  actor_atom_generic_evaluations             4
  empty_endpoint_generic_evaluations         0
  full_prefix_generic_comparisons            0
  typed_signature_mutation_rejections        3
  noncommuting_recurrence_cases              4
  signed_noncommuting_recurrence_cases       2
checker-v4 --selftest:                       PASS (mutation_count=44)
reversed-production-multiplication mutant:   REJECTED
workflow-v12 YAML parse:                     PASS (12 steps)
workflow-v12 normalized exact-v11 comparison PASS
AST production call graph/noninterference:   PASS
```

## 5. Classified findings

### Load-bearing finite blockers to the one GHA release

None.

### Nonblocking observations

1. V499 correctly supersedes v495's historical localization sentence: the
   old empty-word canary had completed by 17 seconds; the exact later timeout
   subregion is `UNKNOWN`.  This does not affect the monoid lemma or v7.
2. The actual runtime of the unchanged direct-row and aggregation phases is
   unknown until an authorized run.  The four phase boundaries and throttled
   meters now make a future stop localizable without flooding the log.

### Out of scope

Real-parent replay, artifact production, stronger nonexistence conclusions,
and a new direct-row algorithm are outside this finite audit.

No fresh rho2, A0, COMMON, cofinal, fake, or Ihara claim follows from this
static audit.  In particular:

```text
REAL_PARENT_REPLAY=NOT_RUN
GHA_DISPATCH=NOT_RUN
FRESH_RHO2=NOT_PRODUCED
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

VERDICT=PASS_A0_ENDPOINT_V7_SAFE_FOR_GHA
SAFE_TO_DISPATCH_GHA=yes
