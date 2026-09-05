# Task923 -- corrected filtered root-scalar workflow v2

## Disposition

The v2 workflow is implemented in
`.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v2.yml`.
Task922 producer/checker source pins and the final source/schema join are
frozen. The workflow is ready for root's narrow source audit and GHA launch;
local execution was intentionally not performed. No workflow run or commit
was made by this agent. Root remains the sole commit/push/dispatch broker.

During this task root explicitly expanded the assignment to finish
`search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py`. Task922 handed
over that saved checker exclusively; this agent completed its state-fold,
output reconstruction and focused-test glue. The producer was not edited.

The change implements the staging required by v541, not a new arithmetic
result. `verified=false`; Grade2 MEMBER/NONMEMBER remain `NOT_DECIDED`, and
A0/COMMON/COFINAL_LIFT/FAKE/IHARA remain `NOT_DECLARED`.

## F923-1: exact retained production and parent boundary

The workflow starts from the mechanically completed v1 workflow. All 51
existing environment fields, the live metadata/authentication step, and the
eight artifact downloads are unchanged. In particular, Task554's actual
parent run has conclusion `failure`; its five accepted artifacts and fixed
bodies remain the intended inputs. That conclusion gate was not relabeled.

| Parent | Run/attempt | Artifact IDs |
|---|---|---|
| P1 | `33851744070/1` | `9931437113` |
| Task554 | `33677346616/1` | `9865061266`, `9865238399`, `9865242284`, `9865193269`, `9865239848` |
| Task712 | `33814194630/1` | `9915928157` |
| Separator | `33891714539/1` | `9944214057` |

The fixed head, artifact name, archive byte count/digest, repository identity,
run attempt, workflow path and expiration gates are retained exactly. No
parent rebuild, provider hierarchy, full instruction-DAG expansion or extra
audit job was added.

The one `ubuntu-24.04` job keeps its 90-minute limit, Python 3.13, pinned
`numpy==2.5.1`, 40-minute producer and 40-minute checker caps, serial bounded
selftests then the actual producer then the independent checker. Per the
Task922 handoff, each serial selftest receives
`--actual-canary-launch "$RUNNER_TEMP/launch.json"`: the bounded actual-q
seed-2 comparison and Task712 homogeneous-adjoint check use the fixed parents,
not another 8,059-row/32,280-origin production pass. The v2
executables retain the complete 32,280-origin root family; readiness does
not imply that a nonzero root scalar is a physical pivot or that a zero
root scan completes the later dual orbit.

Minute-scale progress, producer/checker logs and diagnostic output upload
with `always()` are preserved. Final candidate upload requires both real
executions to succeed. There is no synthetic-only success route.

## F923-2: body-authenticated lower roster

The stager checks the actual body SHA against the fixed digest before
parsing any blob descriptor. It then checks the HEAD/body/parent join and
selects only the prescribed existing lower payloads:

- prepare: `old_blocks[c].lower_basis_blob`, then
  `old_blocks[c].lifted_grade_blob`, for `c=0,1,2,3`;
- block `b`: `basis_blob`, for `b=0,1,2,3`.

Each Task554 state remains exactly `{root,head,body,files}`. Each `files`
roster starts with its HEAD/body pair, followed by the selected blobs in the
order above. A roster receipt remains `{file,bytes,sha256}`; the authenticated
body descriptor additionally carries `{rows,width,encoding}`. Exact shape,
row counts, width, `base3-four-trits-per-byte`, content-addressed basename,
byte size and recomputed SHA are checked before staging. Paths reject
absolute paths, traversal, Windows separators/drive prefixes, symlinks and
resolved escapes. Producer and checker separately authenticate/decode the
same body-bound payloads and enforce their packed-row constraints.

The five frozen body digests, in prepare then block order, are:

```text
1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865
9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74
d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6
a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac
642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01
```

The expected blob receipts below come from Task920's actual intake and
Task922's descriptor handoff. They are not claims of a local replay by this
workflow agent. The exact filename is `<stem>.<SHA-256>.bin`.

| Stem | Rows | Width | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| `old-0-lower-basis` | 505 | 6056 | 764570 | `46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837` |
| `old-0-lifted-grade` | 505 | 72576 | 9162720 | `08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b` |
| `old-1-lower-basis` | 503 | 6056 | 761542 | `8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333` |
| `old-1-lifted-grade` | 503 | 72576 | 9126432 | `14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364` |
| `old-2-lower-basis` | 503 | 6056 | 761542 | `ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4` |
| `old-2-lifted-grade` | 503 | 72576 | 9126432 | `0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4` |
| `old-3-lower-basis` | 503 | 6056 | 761542 | `3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48` |
| `old-3-lifted-grade` | 503 | 72576 | 9126432 | `7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5` |
| `block-0-basis` | 1509 | 18144 | 6844824 | `cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39` |
| `block-1-basis` | 1512 | 18144 | 6858432 | `0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461` |
| `block-2-basis` | 1512 | 18144 | 6858432 | `602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6` |
| `block-3-basis` | 1512 | 18144 | 6858432 | `4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9` |

The roster gate requires twelve blobs totaling exactly `67011332` bytes:
`39591212` prepare bytes plus `27420120` new-basis bytes. Independent static
arithmetic gives `2014` old rows plus `6045` new rows, hence `8059` total.
Every artifact already contains its required blobs; all existing downloads
are retained intact. The stager opens one JSON body at a time and does not
retain the full five-body DAG.

## F923-3: versioned source/schema join and checks

The workflow name is `d972-r07-actual-root-scalar-batch-v2`. The launch,
Task554-parent and separator-parent schema prefix is
`d972.r07.actual-grade2.root-scalar-batch.v2`, with the existing
`.launch.v1`, `.task554-parent.v1` and `.separator-parent.v1` suffixes.
The source receipt uses
`d972.r07.actual-root-scalar-batch.source-receipt.v2`.

The workflow uses only the new actual-batch v2 producer/checker paths while
retaining each side's independent v15 arithmetic context. Both new source
SHA/byte pins are frozen below and enforced before the v2 executables run.
The existing v15 pins are unchanged and were reproduced with local
`Get-FileHash -Algorithm SHA256` (no Python):

```text
producer-v15 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632
checker-v15  8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662
```

Static checks performed without local Python: all 51 old environment fields
match v1; live parent gates/download steps are byte-identical; from bounded
selftests through candidate upload the only differences are v2 executable
paths, artifact labels and the bounded actual-canary selftest argument;
both Python heredoc delimiters and YAML block
indentation were inspected. No local YAML parser was available; no package
was installed. Task922 confirmed the exact schema and ordered roster above
in its implementation handoff. Final producer/checker CLI paths, ordered
roster, source pins and nested output contracts were statically joined.
The checker source passed a read-only lexical string/bracket-delimiter
check; this is not Python compilation or an executed selftest.

```text
WORKFLOW_BYTES=29421
WORKFLOW_LINES=519
WORKFLOW_SHA256=326bc19f837a1c03a2613713747e0eed80d94ad466608a948209e52827abbe63
PRODUCER_BYTES=118315
PRODUCER_LINES=2106
PRODUCER_SHA256=3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856
CHECKER_BYTES=119619
CHECKER_LINES=1968
CHECKER_SHA256=e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6
ALL_THREE_FILES=LF_ONLY_NO_BOM_FINAL_LF
```

Receipts were reproduced by `Get-FileHash -Algorithm SHA256` and .NET byte
reads; no local Python was used.

## F923-4: checker handoff completion

The already completed checker-owned raw-seed evaluator, lower adjoints,
packed-dot implementation and slice readers were preserved. No producer
kernel is imported. Completion was limited to the following v541 work:

- Restore the accidentally truncated Task554 validator/state function from
  checker v1, then extend it to authenticate the exact ordered lower roster.
- Fold all twelve lower blobs while prepare and one block are resident;
  add the four lower-value arrays to actor direct values before the unchanged
  relation subtractions. No full P1 matrix or parent/DAG reconstruction.
- Independently reconstruct raw-seed receipts, lower-covector/blob receipts,
  separate homogeneous/lower/complete-direct value hashes, corrected seed
  scalars and the sealed `filtered_direct` receipt. Compare every saved
  small array byte-for-byte and include it in exact result/manifest rosters.
- Preserve RootViolationBatch/AllFourRootEOF/RootZero boundaries. All records
  carry the formula identifier, but zero roots have no repaired small arrays
  or `filtered_direct`. Active scalar Violation/EOF records bind the new
  receipt and the five original P1 value-vector hashes.
- Keep `32280` as `global_relation_declared_count` at terminal scope (and
  `relation_origin_declared_count` in the run receipt). Violation's actual
  checked prefix is `origin_id+1`; ScalarEOF's `origins/next_origin` is the
  completed scan count. `504` is explicitly a future orbit declared bound,
  with `future_orbit_rows_executed=0`.

Focused tests now include sixteen mixed full-actor/adjoint comparisons;
a constructed nonzero lower-only contribution; pure-top/full-defect
comparisons; negative controls for omitted lower terms and one-sided seed
projection; a tiny authenticated packed old/new fold with a guaranteed
nonzero cross-character grade companion; and coherent resealing rejection
for the repaired output receipt. The actual-parent canary checks seed2
raw/projected/difference pairings `0/1/2`, four independently pinned P1
character-0 slices and corrected scalar `0`, plus the four Task712 pure-top
adjoints. These tests are implemented, **not locally executed**.

Task926's narrow audit identified one stale relation-receipt recipe during
the handoff. It was corrected before freeze: checker and producer now both
bind `filtered-direct-blockwise-scalar-v2`, `V541_FORMULA_ID`,
`LOWER_BLOB_PIN_SHA256` and `task554-v3-body-and-lower-blob-pins` in the same
canonical relation receipt. The actual-canary CLI mismatch noted during
in-progress audit was also closed before freeze.

## F923-5: root-only launch handoff

Fixed push branch: `sol/r07-explicit-lift-20260825`.

Exact distinct push marker:

```text
[r07-actual-root-scalar-batch-v2-run]
```

After the authorized root broker has committed/pushed the frozen intended
sources, the explicit dispatch command is:

```powershell
gh workflow run d972-r07-actual-grade2-root-scalar-batch-v2.yml --ref sol/r07-explicit-lift-20260825
```

Use either the marker-triggered push or explicit dispatch for one production
launch; this agent performed neither.

```text
COMMIT_SHA=NOT_CREATED_BY_TASK923
RUN_ID=NOT_DISPATCHED_BY_TASK923
WORKFLOW_READY=STATIC_SOURCE_AND_ROSTER_JOIN_COMPLETE
LOCAL_PYTHON_COMPILE_SELFTEST=NOT_RUN
GHA_COMPILE_SELFTEST_ACTUAL_CANARY=REQUIRED_BEFORE_PRODUCTION
ACTUAL_CORRECTED_ROOT_SCAN=PENDING
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
