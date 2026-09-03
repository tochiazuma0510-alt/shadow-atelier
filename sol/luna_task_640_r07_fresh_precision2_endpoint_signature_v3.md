# Luna Task640: accepted-SLP fresh precision-two consumer v3

Role: Luna implementation.  Read this mail and every mandatory parent below
completely, first section to last.  Build the real v478/Task630 consumer that
turns the now accepted Task625 canonical selected SLP into a fresh degree-two
residual.  This stops before the v474 grade-two MEMBER/NONMEMBER decision.

Create only these four versioned outputs:

1. `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
2. `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
3. `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml`;
4. `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md`.

Do not edit the rejected v2 quartet, proofs, v220, parents, or any other
file.  Do not run production, GHA, or git.  Small serial selftests are
allowed; use repository-external temporary storage.  This is a fresh live
implementation, not removal of v2's terminal `NOT_READY` placeholder.

## 1. Mandatory contracts and accepted parent

Authenticate and implement the full contracts in:

- Task627 FAIL and its complete repair list: 18,171 bytes, SHA-256
  `5ce7efabb36c454c688248249acd47ee9c6e4594039cb872674101e34239538c`;
- Task630 semantic-contract PASS: 32,029 bytes, SHA-256
  `d64122daa3b6396e494d8309eb98ecadebad2062a173a80fca2ab88baacd7dd1`;
- v478: 5,131 bytes, SHA-256
  `a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b`;
- Task636 PASS: 7,089 bytes, SHA-256
  `2cdecfcb47cf6727d45cbc7cf494c84230a5be5af489d6bca306a4df04552c79`;
- Task639 `PASS_SELECTED_SLP_PARENT`: 10,104 bytes, SHA-256
  `b48fe4bfb43aedb76c9109e2ca73e7a9de323687c69c64807e74f3ad62db0a1b`.

Also authenticate every frozen paper/arithmetic/source pin listed in Task630
Sections 1 and 7.  The permitted producer arithmetic owner remains
`search/d972_r07_a0_first_rung_grade2_prebuild_v1.py`, 145,917 bytes,
SHA-256
`acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8`.
The checker may not import it.

The immutable selected-SLP parent is:

```text
workflow d972-r07-a0-grade1-selected-slp-staged-v3
run/attempt/job 33734643746/1/100582244001
head b401d724bbdbef8cf67e96def22fc51c014ab546
conclusion success
payload artifact 9885925239
name task625-grade1-selected-slp-staged-v3-33734643746-1
archive digest sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75
manifest 9034 bytes / 381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22
uploaded verdict 1120 bytes / a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740
producer ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a
checker 8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9
workflow 736f5f86dde47ebe46fcfdbf8a8d20d4e8f052461c4ae1f137433f6618dd0f9f
Task632 reply 6ef38b64baee05ed26a57b8cfbf7e2c80baaa11079ea0775ad9aed5b392d8ab8
```

Require the exact fifteen-file roster and recompute each byte count/hash:

```text
grade-edges.bin       12372120 aa3a506fd2f1358e6edce102d5fb6f129a4b75bd2675e03bb401f01904e47557
grade-nodes.bin         146276 6b79485d9c69a05cf0d6c64788bc4f341792c8cedbb4f00cd1fdc887d42ca82b
grade-origins.bin     30506112 fcc5e5e43a9923b549e0b894c8ab995e545f78563134f37dae99917026283e68
literal-leaves.bin      565981 4a0b631004c9fbbf0b3cc965ff606711e04081c7d79beecb2db6b7be264fc851
lower-companions.bin  10045728 299ff5f214d32a85bea401705bffe01b2cf4f4f327c50a34f26fed1ba433dcaa
lower-edges.bin        1911741 b83e05df054d43952640b4442f08fb54aadf3303675dedc5443268aa3c3e9809
lower-nodes.bin          48169 4e9b5a98f9b434649d3eeac664fdcdc029d81a1247b193cb3260dabe2c22ee3c
lower-origins.bin      3350237 1cbbb4444858828d9b3ddb78c799a087c6ada69b058155f02d11e5f63316135c
lower-stored.bin       3350237 50361df9c85a525e0c3f73a2ef82a337a870b3cb4eb30caad5816df49c98a683
old-lower-zero.bin      712001 f2793fac59ae4cb798f479f764eb494b5db51256fb7d01dfc523000a7b217a33
roots.json              255846 af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5
selected-grade.bits        631 e2fd7f3147f4880e42d6da6f211f2ed7991af9d9d1925416ec30120c46ac832a
selected-lower.bits        208 771af58b72061d7c94ec28c9086c375bf4e1c5b55254cbb11a541fea4093d48e
source-ancestry.json  149359882 315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908
source-refs.json       19876945 18767d10ab9e697c5f9cb54fbdcabfbc1824c0f4e0afde15e0e550e4a3b781ea
```

Their sum is 232,502,114 bytes; with the manifest the inclusive payload is
232,511,148 bytes.  Require the Task625 marker, exact Task554/Task595 pins,
cursor/offers/ranks `8059`, `2014/6398`, `1661/5044`, 3,317 coefficients,
zero remainder, staged/root/leaf bindings, and every false/null claim guard.
The workflow must authenticate the run identity, attempt, head and successful
conclusion, hash the exact parent checker before execution, rerun it against
the exact Task554/Task595 parents, and byte-compare its verdict with the
uploaded verdict before invoking this consumer.

## 2. Exact source and compact-leaf reconstruction

Implement Task630 Sections 3--4 literally.  Stream-parse `R07LEAF1` including
its header, ancestry binding, strict `(seed,path)` order, coefficients 1/2,
signed letters, free reduction, record lengths and exact EOF.  Independently
traverse every reachable constructor edge from all 3,317 ordered roots using
right-appended freely reduced actor paths; do not prune graph reachability by
coefficient cancellation.  Re-encode and byte-compare the resulting exact
`C_T` leaf stream.

Separately reconstruct the 2,622-term registered `C_<1` source in its stored
order, then preserve the source syntax
`C_1=Compose(C_<1,C_T)`.  Only after authenticating all three roots may exact
equal `(seed,path)` keys be added for evaluation.  Never identify source
words by endpoint, signature, hash or seed.

## 3. Eleven typed endpoints, trie and all-seven canary

Recompute the actual Task630 eleven-context ledger from words, not opaque
endpoint constants: six E3 H slots then five E4 P slots, signs
`(+,-,+,-,-,+,+,+,+,-,-)` and coordinates
`(0,1,2,3,0,4,5,6,7,8,9)`.  Preserve PP reversal, PB3 lift exactly on slots
1--6, quotient types, signed block products and every fixed prefix `U_j`.
There is no `% 6`, E4-to-E3 adapter, P/H alias, or P-zero theorem.

Before grouping, check endpoint one for every reached seed in all eleven
contexts.  Build the exact prefix trie with right multiplication in source
order, retain the complete typed `Sigma_11` for every path, and seal the
path/signature table plus all nonzero `(seed,Sigma_11)` buckets.  Emit exact
`L/U/G` and require `G <= L`.  Run Task630's direct-versus-occurrence H1,
H2, pentagon all-seven canary on every nonzero exact complete-root key.

Only after all eleven receipts pass, take the typed first-six H restriction.
Compare Task565's substitutions, signs and prefixes entrywise with ordinals
1--6 and independently bind the accepted PB4-drop/filtration-commutation
map.  Keep P slots in source/all-seven receipts, but do not feed them into
the present two-hexagon physical row.

## 4. Fresh precision-two residual

Use occurrence-first action: seed tuple, each of the first six actor
endpoints, registered substitution/crossed cochain, fixed prefix, one sign,
PB3 normal/boundary maps, then physical aggregation.  Do not act commonly on
an already aggregated row.  Cache at most the 44 compact seed tuples and
charge dense action only to nonzero signature buckets.

Independently construct the exact `g760` target.  Separately prove in bytes:

1. the selected `C_T` degree-one physical row equals the accepted Task625
   physical replay; and
2. the exact Task595 ordered MEMBER coefficient equation has zero remainder.

Then compare every one of the 32,260 lower/auxiliary coordinates to zero.
Only after that gate may the producer emit `rho2` as all 48,384 trits and the
registered exactly 12,096-byte packing.  Decode the packing back to the dense
row.  Seal canonical target, lower, dense/sparse top, support, packing,
endpoint, trie, bucket, root, parent and claim receipts.  This payload is an
input to v474; it is not a grade-two decision.

## 5. Truly independent checker and real-path fixtures

The checker must not import the producer, Task565, the old floor helper, or
their semantic helpers.  Independently implement graph/leaf traversal,
E3/E4 endpoints and substitutions, truncated-polynomial arithmetic,
negative/inverse action, target, PB3/boundary maps, occurrence-first
aggregation, trie/signatures and packing.  Recompute and byte-compare all
32,260 lower and all 48,384 top coordinates plus every manifest receipt.
Its success path must be reachable and end in a unique versioned PASS marker;
no unconditional `NOT_READY` remains.

Route bounded mutations through live validators, covering at least every
case in Task630 item 12: occurrence omission/permutation and slot-1/5
deduplication, E3/E4 confusion, sign/inverse/PP/block/prefix/multiplication
order, nonidentity block product, premature endpoint merging, failed seed
gate, missing/swapped roots, malformed leaf header/record/EOF, altered
ancestry/parent/target, nonzero lower trit, altered top/packed byte, and each
forbidden claim flag.  Avoid synthetic dictionary-only tests and avoid
quadratic or production-sized selftests.

## 6. Resource and workflow contract

Keep only the selected graph, compact path/trie/signature structures, 44 seed
tuples, one acted tuple and the physical accumulators.  Do not allocate a
dense row per graph node/path, rebuild the 1.853-GiB joint grade-two input,
or invoke old closure/projector/member routines.  Stream-hash the 149-MB and
other parent receipts instead of duplicating them in memory.  Avoid hidden
list/array copies and accidental densification.

Give producer and checker explicit wall, RSS, durable-output, path/trie/state
and record-count caps.  A cap or partial comparison is
`UNKNOWN_RESOURCE`/`NOT_READY`, never mathematical NONMEMBER.  Use a workflow
job allowance large enough for the known approximately 12-minute parent
checker plus both consumer phases (120 minutes is acceptable), while keeping
per-process 7-GiB-style memory guards.  Install an exact pinned NumPy version
if used.  Upload logs always and the residual only after the independent
checker PASS marker.  All actions remain immutable-SHA pinned.

Leave one inert versioned fire marker for root to arm after static audit; do
not dispatch it.  Run only serial `py_compile`, bounded selftests, YAML parse,
hash and whitespace checks.  Report exact commands/results, file bytes and
SHA-256, resource design and all remaining claim boundaries.

## 7. Claim boundary

The manifest and checker must keep all of the following false:

```text
grade2 MEMBER, grade2 NONMEMBER, A0, ORDER-54432, full-Q0,
COMMON, cofinal lift, FAKE, IHARA, cross_checked, verified.
```

Do not increase any v220 numerator.  The only intended new mathematical
object is an independently reproduced fresh `rho2` payload for v474.

