# Luna 162: K2 total-fibre roster GHA repair v3

## 1. Verdict and scope

GHA run `32812618841` reached the Python full-run terminal and produced the
complete v2 JSON, but the GAP wrapper rejected that result in its final
diagnostic-contamination gate.  The rejection was a wrapper false positive,
not a roster-computation failure: v2 intentionally recorded the historical
run-`32810928194` exception as the literal metadata value

```text
repair_v2.v1_failure = STATE_STOP TARGET_WORD_REPLAY: 81
```

while the wrapper globally rejected every occurrence of the live diagnostic
prefix.  The v3 repair removes that self-contamination and keeps genuine
diagnostics fail-closed.

The v3 adapter changes no K2 source enumeration, raw-fibre cardinality,
predicate, reduction, fixed-row36 lineage, or v2 modulus-9 roof word-replay
law.  It is producer-side plumbing, not an independent checker and not a
mathematical claim promotion.

## 2. Repair design

`search/d972_k2_total_fibre_roster_producer_v3.py` byte/SHA pins and imports
v2.  V2 continues to pin/import v1 and to install the already-audited
roof-word convention dispatch.  After the complete v2-plus-v1 validation
chain returns, v3 replaces only the historical free-text value by

```json
{
  "historical": true,
  "code": "TARGET_WORD_REPLAY",
  "detail_zero_based": 81,
  "live_diagnostic_prefix_elided": true
}
```

It then records the v2 parent pin, v3 lineage, and the following explicit
scope assertions:

```text
historical_failure_text_sanitized=true
global_result_diagnostic_scan_preserved=true
enumeration_or_predicate_law_changed=false
roof_word_replay_law_changed_from_v2=false
```

The sanitation assertion serializes only the two small repair metadata
objects, so v3 does not add a second in-memory serialization of the large
roster.  The GAP wrapper remains responsible for a global scan of the final
serialized JSON.

## 3. Fail-closed controls

`search/d972_k2_total_fibre_roster_gha_v3.g` preserves the v2 controls:

- byte/SHA pins for v3, v2, v1, all authenticated inputs, and the workflow;
- pre-existing-output rejection;
- subprocess exit sentinels and full failure-log emission;
- exact-one selftest/Python/result terminal markers;
- schema, status, coverage, completeness, convention-repair, and
  non-preregistered-acceptance semantic gates;
- global forbidden-diagnostic scans for both subprocess logs and result JSON.

V3 does not allow-list a location containing the forbidden prefix.  It removes
the prefix from historical data, leaving the global detector simple.  Both the
Python adapter and GAP wrapper contain destructive controls which establish:

```text
injected live diagnostic -> rejected
structured historical record -> accepted
sanitizer output -> contains no forbidden diagnostic token
```

Thus a genuine traceback, memory/syntax error, producer stop, kill, or GAP
error remains fatal.

## 4. Versioned assets and pins

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_k2_total_fibre_roster_producer_v3.py` | 9531 | `80fd30217b9a682c5b7ebcb970e0ca6b383b7f84951abb9b7aec3fe8f489f267` |
| `search/d972_k2_total_fibre_roster_gha_v3.g` | 11475 | `2c46f68a1707a64c3cd8e30742704cd0d62b5ad0236eb0d53f0a2565bb67ed45` |
| `sol/luna_reply_162_k2_total_fibre_roster_gha_repair_v3.md` | self | not self-pinned |

Pinned parent adapter:

```text
path=search/d972_k2_total_fibre_roster_producer_v2.py
bytes=9776
sha256=a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411
```

Pinned roster core remains:

```text
path=search/d972_k2_total_fibre_roster_producer_v1.py
bytes=44829
sha256=cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499
```

## 5. Lightweight local audit

No full roster computation was run locally.  No Git or GHA operation was
performed.  The requested lightweight checks passed:

```text
Python AST parse:
D972_K2_V3_AST_PASS

python -B search/d972_k2_total_fibre_roster_producer_v3.py --preflight
D972_K2_TOTAL_FIBRE_ROSTER_V3_PREFLIGHT_PASS targets=972 v1_g9_mismatches=810 first_v1_mismatch=81 v3_roof_g9_mismatches=0 psl_mismatches=0 parent_sha256=a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411

python -B search/d972_k2_total_fibre_roster_producer_v3.py --selftest
D972_K2_TOTAL_FIBRE_ROSTER_CORE_V1_SELFTEST_PASS mutations=8 small_component_cases=6 inputs=13
D972_K2_TOTAL_FIBRE_ROSTER_V3_SELFTEST_PASS targets=972 v1_g9_mismatches=810 first_v1_mismatch=81 v3_roof_g9_mismatches=0 psl_mismatches=0 diagnostic_mutant_rejected=true structured_history_accepted=true sanitizer_rewrite_pass=true parent_sha256=a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411

GAP 4.16.0 ReadAsFunction parse-only:
D972_K2_V3_PARSE_PASS
```

The GAP parse emitted only the usual top-level unbound-global syntax warnings;
there was no syntax error.  The wrapper has zero non-ASCII bytes.  The
temporary parse driver and generated v3 bytecode were removed; no persistent
test output was left in the repository.

## 6. Dispatch contract

Dispatch the existing `.github/workflows/gap-run.yml` with exactly:

```text
script: search/d972_k2_total_fibre_roster_gha_v3.g
preamble: <empty>
out_dir: ci/out
timeout_min: 120
with_pquot_packages: false
```

Expected result/log paths:

```text
ci/out/d972_k2_total_fibre_roster_v3_20260825.json
ci/out/d972_k2_total_fibre_roster_v3_selftest.log
ci/out/d972_k2_total_fibre_roster_v3_full.log
```

Expected terminals:

```text
D972_K2_TOTAL_FIBRE_ROSTER_V3_SELFTEST_PASS
D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V3_FINAL
D972_K2_TOTAL_FIBRE_ROSTER_GHA_V3_FINAL result=ci/out/d972_k2_total_fibre_roster_v3_20260825.json python_terminal_count=1 result_terminal_count=1
```

Only a successful full GHA terminal upgrades this repair from locally
preflighted code to a producer candidate artifact.  The valid total and
histogram must be read from that artifact and must not be inferred from the
earlier preregistration.

`K2_TOTAL_FIBRE_ROSTER_GHA_REPAIR_V3_READY`
