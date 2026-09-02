# Sol reply 522 -- independent A0 rank111 continuation-driver audit

## Verdict

**GO_FOR_GHA_DISPATCH_RANK111_CONTINUATION.**

The exact subject is commit
`dcd1b29e4e450c5eaf22c8c1901e455229895d1c` (`sol: prepare A0 rank111
continuation driver`).  I found no dispatch-blocking identity, archive,
resume-member, shell, resource, path, quoting, stale-output, or upload defect.
This is transport/implementation authorization only.

## Clean subject and executable pins

I resolved the abbreviated object, exported that exact object with
`git archive --format=tar`, and extracted it under the repository-external
directory
`%TEMP%/shadow-atelier-task522-9b2c76cda5bc4d24a47d69ce0c7e86c8/tree`.
All subsequent subject/dependency reads and fixtures used that tree.  No
untracked working-tree file supplied a dependency.

| clean-archive object | bytes | SHA-256 |
|---|---:|---|
| rank111 resume driver v11 | 8,683 | `84db6c150d8ce764c411afa91a9cc9c31ad193ecaf719900faa9ebdbc32b5b7d` |
| sole owner, rank98 driver v10 | 8,662 | `8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e` |
| producer v3 | 12,215 | `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37` |
| checker v7 | 3,653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |

The clean subject also contains the frozen Task521 task/reply and the generic
`gap-run.yml`; their read-only pins are respectively
`3935/db22932e...cf125a`, `1319/dfcfab9a...ac8c5d`, and
`13309/0c2ba908...cecae`.

## Parse, generated shell, and owner diff

Through the required GAP wrapper, `ReadAsFunction` parsed the exact clean v11
file and printed one `TASK522_V11_PARSE_PASS`; production was not entered.
The usual unbound-global parse warnings are expected for a top-level driver
parsed as a function and were not syntax errors.

An audit copy changed only the top-level `Exec` line, after the GAP manifest
loop had closed, to serialize `D521Cmd` and quit.  The resulting full shell
passed Git-for-Windows `bash -n`.  GAP's serializer inserted only shell
line-continuation pairs (`backslash + LF`); after removing those continuations,
the command is 9,220 bytes and mechanical inspection found:

- exactly one pinned producer command and one later pinned checker command;
- resume copy before producer, producer before checker;
- `set -euo pipefail`, `umask 077`, and eight v11 stale-path checks;
- exactly one `ulimit -v 5200000`;
- exactly one outer producer timeout of 7,500 seconds, containing the unchanged
  `--mode PRODUCTION --seconds 7200 --rss-bytes 4800000000 --max-rises 64`;
- exactly one 3,600-second checker timeout and its one-line v7 PASS gate.

The v10 and v11 sources both have 122 lines.  `SequenceMatcher` found ten
replacement hunks and no insertion or deletion.  After mechanically
normalizing only `D504`/`D521` and `task504`/`task521`, 85 lines are identical;
the remaining 37 lines are exactly:

- line 2: version/rank header;
- lines 5--6: required rank111/v11 preamble name;
- lines 10--24: source run/job/head/artifact, release ZIP pin, and versioned
  archive/output paths;
- lines 29--30: promoted checkpoint bytes/SHA;
- lines 32--39: the eight replacement manifest rows;
- lines 47--52: repeated immutable source/archive assertions;
- lines 65--66 and 122: versioned preflight/final markers.

In particular, producer/checker path pins are unchanged, and v10/v11 lines
100--110 (memory cap, producer invocation, result/checkpoint nonempty gates,
producer terminal cardinality, checker invocation, and checker cardinality)
are byte-identical after namespace substitution.  Therefore positive and
RESOURCE handling, the 7,200-second/4.8-GB/64-rise computation, and the
3,600-second checker boundary have not changed.  No new computation or branch
was introduced.

## Permanent release and frozen provenance

Fresh read-only API queries reproduced the frozen source:

- run `33564845217`, attempt 1, `workflow_dispatch`, head
  `c582f8d786012a668783790007b72c5c422c3db8`, `completed/success`;
- its sole job `100045550767`, name `gap`, same run/head,
  `completed/success`;
- its sole Actions artifact `9826862037`, `gap-run-out`, API size 96,198,
  `expired=false`, owned by that run/head, service digest
  `sha256:22aa0d836298e01fa27b2d893427839b18fe51a83781a840d357a1243e6d412c`.

Release tag `archive-gha-checkpoints` is neither draft nor prerelease.  It has
exactly one asset with the commissioned name
`artifact_9826862037_gap-run-out.a0-rank111.zip`: asset `540421734`, state
`uploaded`, content type `application/zip`, size 37,586, browser URL equal to
the driver's literal URL, and release-asset digest
`sha256:8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de`.

The independently downloaded bytes are exactly 37,586 bytes with that same
SHA-256.  Direct ZIP inspection found exactly eight unique, flat, non-directory
members, no path separators, no extras, and no Unix symlink/special-file mode:

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint` | 69,947 | `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f` |
| `d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log` | 38 | `52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10.json` | 86,354 | `39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log` | 51 | `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint` | 85,934 | `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log` | 4,905 | `271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c` |
| `driver.g` | 128 | `393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978` |
| `run.log` | 5,004 | `ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15` |

## Reached pre-producer transport fixture

From the exact generated shell I replaced the producer launch, at its unique
top-level timeout token and with no conditional open, by one
`TASK522_PREPRODUCER_TRANSPORT_PASS` print and immediate exit.  Executing this
copy in the clean export actually performed every preceding command:
source pin checks, permanent release download, archive size/SHA check, unzip,
eight entry counts and member byte/SHA checks, resume copy, copied-file pin,
and the virtual-memory limit.  It printed the marker exactly once and exited
zero.  No producer result or checker log was created.

The copied input is 85,934 bytes with SHA-256 `69a7ec3d...dfd93` and is
byte-for-byte equal to manifest member 5,
`d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint`.  It is not
member 1: member 1 is 69,947 bytes with SHA-256 `c0fcb581...0d37f`.  Thus the
rank111 continuation cannot silently resume the stale rank98 input through
this fixed transport.

## Real `gap-run` reachability

The clean workflow reaches the audited commands with this bounded invocation:

```text
script=search/d972_r07_a0_actual_tau_free_rank111_resume_gha_driver_v11.g
preamble=D972_R07_A0_RANK111_CHECKPOINT_RESUME_V11_RUN:=true;;
out_dir=ci/out
timeout_min=240
with_pquot_packages=false
```

The script path passes the workflow's path grammar and exists in the exact
tree.  The workflow creates `ci/out`, writes the preamble before its exact
`Read(...)`, skips the opt-in p-quotient build/load step, uses `set -euo
pipefail`, and pipes GAP through `tee` under pipefail.  A 240-minute job limit
leaves 55 minutes beyond the two inner hard windows (7,500 + 3,600 seconds),
in addition to their own kill-after controls.  The observed predecessor job
also completed the same 7,200-second producer plus v7 checker well inside this
bound.

All download, extracted-member, input, result, checkpoint, producer/checker
log, diagnostic, `driver.g`, and `run.log` paths are under `ci/out`; the
workflow uploads `ci/out/` under `always()`.  A fresh checkout has no v11
stale path, while the pre-created `driver.g`/`run.log` names do not collide
with any v11 stale gate.  Literal paths contain no rejected quote/newline/CR,
the driver single-quotes its flat shell after checking those characters, and
both pipeline exit codes remain fail-closed.  The 5,200,000-KiB virtual-memory
cap leaves margin over the producer's 4.8-GB RSS gate.  I found no upload-file
or runtime reachability incompatibility.

## Claim boundary

The mathematics does not change.  Dispatch may only continue the archived
`68 literal rungs / rank 111 / round 73` RESOURCE prefix.  It promotes no new
A0 row, COMMON result, compatible lift, fake, or Ihara claim.  Any future
positive still requires the exact independent v7 checker and a separate
artifact audit; `verified=false` remains unchanged.

The final physical bytes/SHA-256 of this reply are supplied after freeze in
the parent delivery envelope because embedding its own digest would be
self-referential.

GO_FOR_GHA_DISPATCH_RANK111_CONTINUATION
