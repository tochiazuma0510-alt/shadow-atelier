# Sol(max) Task743: P1 literal-LF v5 hostile audit

## Verdict

```text
VERDICT=PASS_P1_EQUALITY_LF_V5_SAFE_FOR_GHA
SAFE_TO_DISPATCH_GHA=yes
ACTUAL_FIVE_PARENT_REPLAY=DEFERRED_TO_GHA
P1_SEMANTIC_REPLAY=NOT_YET_ACCEPTED
verified=false
```

All six requested finite checks pass.  The v5 producer changes exactly the
four record-digest literals and their equality-list digest, plus one bounded
live rejection fixture.  The v3 checker is the v2 checker with only the
producer provenance binding moved from v4 to v5 (including the corresponding
identifier/diagnostic/fixture references).  No actual parent replay, GHA,
workflow, git operation, or Lean check was performed.

The kickoff names
`sol/sol_reply_726_audit_r07_p1_semantic_checker_v2.md`, which is absent from
the tree.  The unique matching Task726 reply is
`sol/sol_reply_726_audit_r07_task724_p1_checker_v2.md`; its title, contents,
and paired Task726 kickoff identify it unambiguously, so that existing file was
audited.  This handoff filename discrepancy is non-executable and does not
affect the release verdict.

## Exact audited bytes

Every listed repository file is LF-only (`CR bytes = 0`) and ends in one LF.

| input | bytes | LF bytes | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/sol_task_743_audit_r07_p1_equality_lf_v5.txt` | 2,298 | 45 | yes | `0aae139d23d1740709c0f4ab86613e01086a3d18ffe02ea1feb7eb8c672d5ffe` |
| `sol/proof_r07_p1_equality_literal_lf_repair_v489.md` | 2,771 | 69 | yes | `14e4d33967cea1a26d1cb41c11ab125abad2cc9d5455e3c85e0377987832c789` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py` | 41,259 | 381 | yes | `ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | 41,619 | 382 | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py` | 130,683 | 2,689 | yes | `8636440c5e51d71a1f06d20d89a3d60c588453e741b17fbbd61735c76a9d3e88` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py` | 130,683 | 2,689 | yes | `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e` |
| `sol/luna_reply_740_r07_p1_equality_literal_lf_v5.md` | 3,340 | 75 | yes | `512d480ce007a2573eaf6ec8fa9fbbb3623a741d08000e33edef16f23c0dfe1a` |
| `sol/sol_reply_726_audit_r07_task724_p1_checker_v2.md` | 12,288 | 268 | yes | `c7a917e6dd93e34d2ba9ecf9a2cb6bb22b0e30d7f7533566554471cb5d3690eb` |

The external prepare body is exactly 15,398,340 bytes, contains one LF byte,
has no CR byte, ends in `0a`, and has SHA-256
`1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865`.
That is exactly the digest embedded in both its filename and the pinned
`PREPARE_DIGEST`.  Independently decoding and re-encoding the whole body as
sorted compact ASCII JSON plus one LF reproduced the raw 15,398,340 bytes
exactly.

## F743-1: body-derived literal-LF pins — PASS

I parsed the authenticated external body directly and used the independent
serialization

```text
C(x) = json.dumps(x, sort_keys=True, separators=(",", ":"),
                  ensure_ascii=True).encode("ascii")
```

without importing either producer.  For each `old_blocks[i].record`, the v5
input is exactly `C(record) || 0a`; it has one appended byte and final LF.
The old v4 input is exactly `C(record) || 5c 6e`; it has two appended ASCII
bytes (backslash, `n`) and does not have final LF.

| i | bytes in `C(record)` | bytes with v5 `0a` | v5 SHA-256 | bytes with old `5c 6e` | old v4 SHA-256 |
|---:|---:|---:|---|---:|---|
| 0 | 3,602,655 | 3,602,656 | `5b3f5dfd965861f33ec9cb2c2ac2e7401629b73b3571491110d063f47398cb4f` | 3,602,657 | `2a1f0b96effc5bb808d70303f63f78cbc4ef069d80290e5d2f24b072948fcee2` |
| 1 | 3,743,493 | 3,743,494 | `75aa31bfcd4ec622ff985afb6e92bfa16707206508683b012eeb9be1ab2544a6` | 3,743,495 | `2eb0b06da23e6bb45066cb9db0d0bf8c1d6676e6f85067c0eb9da48afa1149fa` |
| 2 | 3,599,100 | 3,599,101 | `d732aa55163be06b50199d864761ec0f1eeb5f29fcea171d4e674616c40d7e75` | 3,599,102 | `10725c2587ce2c9f8b19df2d62be48dd01a16349f60ad9c604b9fb278052a7df` |
| 3 | 3,747,340 | 3,747,341 | `ad89a5738a65e6b1340816534b4dca8b82d3127ae82765a718eec6f6a1025022` | 3,747,342 | `547720cf7162f84957a3f2c5bb7af42fe618641f3a89796814a577bb9ae57b7e` |

All four complete body-derived equality entries, not only their record field,
equal the v5 literals.  In particular the unchanged blob pins are:

| i | `lower_sha256` | `lifted_sha256` |
|---:|---|---|
| 0 | `46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837` | `08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b` |
| 1 | `8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333` | `14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364` |
| 2 | `ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4` | `0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4` |
| 3 | `3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48` | `7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5` |

The ordered equality list has 1,081 compact JSON bytes before its suffix and
1,082 bytes after appending exactly one `0a`; it has one LF and final LF.  Its
SHA-256 is exactly
`e04c0d8de2cfbd264d3c93d915dc19e613a001c5278c8efdb704f06d1abb3565`,
matching v5 `EQUALITY_SHA`.  Replacing its four record fields with the four
old backslash-`n` digests and still appending the aggregate's real `0a`
reproduces old v4 `EQUALITY_SHA` exactly:
`99da0c4a42a0c747cde28cd91797d7c655d797c27f8f78a7423142bf56bc5dbf`.

## F743-2: producer v4 to v5 scope — PASS

The direct unified byte-source diff has exactly two hunks:

1. four `record_sha256` string replacements and the one `EQUALITY_SHA`
   replacement at the equality constants;
2. one physical line in `selftest`, the bounded coordinated-old-pin rejection
   fixture.

An independent AST comparison found identical assignment and function-name
rosters.  The only changed top-level assignments are `EQUALITY_RECORDS` and
`EQUALITY_SHA`; within the four records, the changed-field set is exactly
`{record_sha256}` for every entry.  Every `character_index`, `lower_sha256`,
and `lifted_sha256` is identical.  The only changed function AST is
`selftest`.  Its new physical line 354 comprises five simple AST statements;
removing precisely those statements makes the complete v5 selftest body
identical to v4.  Every other function AST is identical.

Consequently the source/lower/lifted pins, `canonical`, prepare and block
replay, DAG/FIFO logic, packet authentication and traversal, projector,
resource caps, schemas, receipt validators, CLI, and all claim flags are
unchanged.  There is no hidden executable change outside the five literals
and the charged fixture.

## F743-3: checker v3 independence and release scope — PASS

The complete checker v2/v3 unified diff is restricted to:

- `PRODUCER_V4_SOURCE/SHA` becoming `PRODUCER_V5_SOURCE/SHA`, with the exact
  v5 path and `dc5931...dcbdcf` digest;
- the associated v4-to-v5 diagnostic strings and references in
  `validate_producer_source`, `producer_source_digest`, and its bounded source
  mutation fixture;
- the explanatory provenance comment.

After mechanically normalizing only those v5 provenance identifiers, path,
digest, and diagnostic strings back to v2 spelling, the complete executable
module AST is identical to v2.  The only functions whose raw AST differs are
exactly `validate_producer_source`, `producer_source_digest`, and `selftest`.

The import roster is standard-library modules, NumPy, and the optional
standard-library `resource` module.  There is no `importlib`, producer import,
module loader, `__import__`, `exec`, `eval`, or `runpy` call.  The producer is
only read as bytes for its provenance digest.  Each of the four corrected
record digests and the corrected aggregate digest occurs zero times in checker
v3.

The independent equality route is unchanged from v2:

- `replay_prepare` independently reconstructs each old closure record,
  compares it to the authenticated body record, reconstructs lower/lifted
  bytes, and hashes `canonical(record)`, `owner.matrix_bytes()`, and the packed
  lifts;
- it independently hashes the ordered equality list with its own
  canonical-LF function;
- `validate_peer_prepare` checks the producer list's exact shape and
  self-consistent aggregate without importing a producer pin;
- `compare_semantic_receipts` then requires the independently reconstructed
  list and aggregate to equal the producer receipt before success can be
  emitted.

The ASTs of `canonical`, `replay_prepare`, `validate_equality_receipts`,
`validate_peer_prepare`, `compare_semantic_receipts`, and `run_actual_check`
are byte-for-byte unchanged at AST-dump level from checker v2.

## F743-4: bounded execution and live mutation — PASS

The exact external bytecode directory was
`C:\Users\81905\AppData\Local\Temp\task743-pycache-f0c2bee3a5664390b8e47b6b8e7d43ca`.
The following bounded commands were run:

```powershell
$env:PYTHONPYCACHEPREFIX = 'C:\Users\81905\AppData\Local\Temp\task743-pycache-f0c2bee3a5664390b8e47b6b8e7d43ca'
python -m py_compile search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py
python -B search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py --selftest
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py --selftest
```

Results:

```text
py_compile: exit 0
producer v5 selftest: exit 0; status=PASS; fixture_accept=2; rejections=35
checker v3 selftest:  exit 0; status=PASS; fixture_accept=6; rejections=41
```

The producer output includes `literal_lf_equality_gate` in
`live_entry_points`, reports `coordinated_equality_mutation=REJECT`, and keeps
`actual_replay=DEFERRED_TO_GHA`.  I also made a bounded direct call to the same
production route: copied `_fixture_receipts()`, changed character 0 to the old
`2a1f...fcee2` record digest, recomputed the aggregate so the mutation was
coordinated, and called `validate_join_receipts`.  It rejected with the exact
reason `equality_record_pin`.  Thus rejection is not supplied by a toy
assertion or a stale aggregate; the mutation reaches
`validate_join_receipts -> validate_prepare_receipt ->
validate_equality_receipts` and fails the live per-record pin.

For the body/digest audit I used `Get-FileHash -Algorithm SHA256` and a separate
stdin Python program using `json.loads`, the displayed independent `C(x)`,
`hashlib.sha256(C(x) + b"\n")`, and
`hashlib.sha256(C(x) + b"\\n")`.  Static release scope was checked with a
direct `difflib.unified_diff` and independent `ast` comparisons; neither
release module was imported for the pin extraction.

## F743-5: resource-path inspection — PASS

The producer's added source lines contain no NumPy allocation and no thread,
process, executor, concurrency, retry, wait, or sleep construct.  The only new
executable work is a bounded selftest JSON copy, aggregate hash, and call to an
existing validator.  It is unreachable from the actual replay modes.  The
checker has no arithmetic/replay change after provenance normalization; its
only extra practical effect is reading the 41,619-byte v5 source instead of
the 41,259-byte v4 source through the pre-existing provenance gate.

No new resident global matrix, dense artifact-scale allocation, concurrency,
retry policy, or avoidable slow path is introduced.  Existing per-owner dense
lift work and all time/RSS caps are unchanged.  No unrelated refactor is
requested.

## Claim boundary

This verdict authorizes dispatch of the already designed bounded GHA replay;
it does not accept the five-parent semantic result in advance.  The external
prepare body was opened only for the expressly requested digest and literal
audit.  None of the five real parent replay routes was run locally.

```text
REAL_FIVE_ARTIFACT_REPLAY=DEFERRED_TO_GHA
P1_SEMANTIC_REPLAY=NOT_YET_ACCEPTED
precision2=false
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```
