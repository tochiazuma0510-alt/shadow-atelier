# Sol reply -- Task905 / R07 physical-state manifest contract v2 audit

## Verdict

PASS.  The frozen v2 producer, independent checker, and workflow implement the
single commissioned rho2-v17 manifest-ABI repair.  I found no mathematical,
authority, claim-boundary, or public-resume broadening.  This accepts the v2
implementation/workflow for one root marker commit, push, and GHA rerun; it
does not decide Grade 2.

## Exact receipts

All four Task904 files are BOM-free, CR-free, and final-LF terminated.

| subject | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_grade2_physical_state_separator_v2.py` | 79,122 | 1,462 | `b068c9f3be153c5381f583b4a82448d5680777ce71ccb5250c2bbb972c8cff2e` |
| `search/check_d972_r07_grade2_physical_state_separator_v2.py` | 60,997 | 780 | `bb5d0c0a51408a65c3200b552e6a1eac2f832abeeca8e19fcce64d570f0967f6` |
| `.github/workflows/d972-r07-grade2-physical-state-separator-v2.yml` | 20,126 | 405 | `e7529e03f0125ae0d6b28f1fb817757d61d1f12dcb48ad929052fe7a1e81b6d7` |
| `sol/luna_reply_904_r07_physical_state_manifest_contract_v2.md` | 4,781 | 115 | `982087f359e4a894a3ccd38e34c1cf7ed7e32b8b5829684b23891ac7992510ab` |

The independently read live `manifest.json` is canonical ASCII JSON, exactly
26,047 bytes, SHA-256
`55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`.
It has 30 top-level keys.  The relevant exact nested contract is
`dimensions={lower:32260,packed_rho2:12096,top:48384}`,
`lower_all_zero=true`, a five-key `rho2` dictionary
(`dense_sha256`, `packed_sha256`, `packing_roundtrip`, `sparse_sha256`,
`support`), and a seven-entry `files` dictionary.  Its role receipts are:

| role | file | bytes | SHA-256 |
|---|---|---:|---|
| `lower_dense` | `lower-dense.bin` | 32,260 | `c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830` |
| `path_signatures` | `path-signatures.json` | 28,393,211 | `ef7fbd1d44647c058b33a1c18894ff5411dcd7870e7cf7e24b6763b68557ab25` |
| `rho2_dense` | `rho2-dense.bin` | 48,384 | `abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e` |
| `rho2_packed` | `rho2.bin` | 12,096 | `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e` |
| `roots` | `authenticated-roots.json` | 255,846 | `af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5` |
| `signature_buckets` | `signature-buckets.json` | 46,469,668 | `e67876dce3bb144ad6afa4895236c8fc37fbc0488c135f9903d8288039829c43` |
| `target_dense` | `target-dense.bin` | 80,644 | `122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2` |

All seven payload sizes and hashes recomputed exactly.  Independent base-3
unpack/repack matched the 48,384-byte dense rho2, and all 32,260 lower bytes
were zero.  The staged ten-file roster totaled 75,319,124 bytes.  Its verdict
was exactly 418 bytes / SHA-256
`cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848`;
the canonical 550-byte acquisition bound run `33839962829/1`, artifact
`9925190479`, and the frozen archive digest.

## Gate table

| gate | result | hostile audit |
|---|---|---|
| Whole manifest before interpretation | PASS | On both live paths, raw bytes are read and the exact size/SHA is required before ASCII decode, JSON parse, canonicality, or field access.  A same-length invalid-JSON mutation failed at `rho2_manifest_live_receipt` / `checker_rho2_manifest_live_receipt`, proving the ordering is executable. |
| Exact live contract | PASS | Both implementations independently require the dimensions, lower-zero flag, nested packed/dense hashes, packing-roundtrip flag, dictionary type, exact seven role set, exact three-key receipt shapes, unique filenames, normalized seven-file roster, and equality with every frozen receipt.  Exact acquisition, verdict receipt, ten-file roster, payload hashes, packed/dense equality, and zero lower payload remain enforced.  Both exact live readers returned 12,096-byte packed targets. |
| v1 regression | PASS | The real manifest fails the v1 producer at `rho2_manifest_shape` and v1 checker at `checker_rho2_shape`, matching run `33889253581/1` (job `101076608011`, exit 1 after the completed state build).  The named old list/top-level-hash mutation is rejected by both v2 selftests.  No MEMBER/NONMEMBER inference is drawn from that wiring failure. |
| Semantic confinement | PASS | AST comparison changes exactly `_read_target_parent`, `_fixture_target`, `selftest` in the producer and `_target`, `_make_target`, `selftest` in the checker; every other top-level node is identical to v1.  Thus physical elimination, insertion-order target reduction, reverse substitution, parent authority, state/output/launch schemas, claim boundary, and the already-disabled public live-resume path are unchanged. |
| Bounded executable controls | PASS | External `py_compile`, producer selftest, checker selftest, and producer benchmark all passed.  MEMBER, Separator, nonmonotone leads `[100,10,300]`, reverse leads `[300,10,100]`, stop/resume byte equality, all prior checker mutations, and the new old-shape rejection were exercised.  Benchmark remained `BOUNDED_ONLY`, with 6 offers, rank 3, two physical reductions, one target reduction, three reverse substitutions, and live bound 915,981. |
| Workflow v2 | PASS | The workflow authenticates and invokes only the exact v2 sources plus accepted stager v4; retains both exact external parent tuples, `resume=false`, fresh roots, 30/30-minute phase caps inside 75 minutes, one-second completion polling with approximately 60-second progress, and compression level 0.  It has five bounded authority API reads, no old-artifact scan, extra copy, SAT/nullspace work, or live-resume reuse.  Unchecked upload is diagnostic; final publication requires both named producer and checker steps to succeed.  The v2 marker occurs exactly once. |

The fresh approximately 82-second physical-state recomputation is therefore
intentional and remains the authenticated public path; the failed v1 state is
not resumed or trusted.

```text
VERDICT=PASS
IMPLEMENTATION_ACCEPTED=yes
WORKFLOW_ACCEPTED=yes
SAFE_TO_PUSH_TRIGGER_GHA=yes
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
