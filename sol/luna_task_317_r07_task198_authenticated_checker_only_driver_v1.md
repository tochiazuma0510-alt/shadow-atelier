# Luna task 317 — task198 authenticated checker-only GHA driver v1

From: Sol / 2026-08-28

Role: Luna bounded driver implementation.  Do not modify or rerun the
task198 producer.  The purpose is to avoid repeating the observed 10,564.41
second producer after the exact producer-capture object already exists.
Current direct run `33155710862` is not to be cancelled; this driver is the
failover and future nonduplicating path.

Read v258 and the current task198 producer/checker/driver in full.  Do not
run Python, GAP, GHA, network, or git.  Do not edit a workflow, v220, any
task198 v1 source, or any staged input.

## 1. Write exactly two new files

1. `search/d972_r07_seven_context_roof_presentation_checker_only_gha_driver_v1.g`
2. `sol/luna_reply_317_r07_task198_authenticated_checker_only_driver_v1.md`

The `.g` file is ASCII-only.  It must pin its complete dependency cone,
including the unchanged task198 independent checker and the existing
task176 production input/manifest.  It must never invoke the task198
producer or import producer helpers.

## 2. Exact captured input authority

The future parent staging paths are exactly:

```text
ci/in/d972_r07_seven_context_roof_presentation_v1.json
ci/in/d972_r07_seven_context_roof_presentation_v1.producer_capture.manifest.json
ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt
```

Reject missing paths, stale aliases, `..`, absolute paths, or any other
basename.  Pin the receipt directly to:

```text
bytes  = 31017244
sha256 = d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b
self_digest_sha256 = cdfd677f4d912232ad7d125bfec092905619e99f3d9ba9d6896614236443fec7
terminal = ROOF_BRIDGE_ISOMORPHISM
rows = 6441
rows_sha256 = e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950
```

Require the producer-capture manifest to be the exact canonical ASCII JSON
object with no extra keys and these exact string/number bindings:

```text
schema = d972-r07-seven-context-roof-presentation/v1/producer-capture-authority/v1
run = "33155653989"
head = bed1d5e6b41477b8799f2a33a24e46f7800f9510
artifact_id = "9684074697"
artifact_digest_sha256 = adbd58fb887bce0b3be86ce1302447f7a1fd875607384ef39c159ba855b36840
member = d972_r07_seven_context_roof_presentation_v1.json
member_bytes = 31017244
member_sha256 = d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b
member_self_digest_sha256 = cdfd677f4d912232ad7d125bfec092905619e99f3d9ba9d6896614236443fec7
rows_sha256 = e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950
producer_log_bytes = 399
producer_log_sha256 = d0d025088bae5f418a6e586d3c926d08740697c0872c0bc0ca3506f0af787bd1
producer_terminal_file_bytes = 24
producer_terminal_file_sha256 = 871dcf46449cf9e5313a6de0d5478d66813fa2879d185960b66f114cf91d5f3b
producer_ok_file_bytes = 55
producer_ok_file_sha256 = 21132c5d1dc58a8c56673089c8bf29b7a53f960d60fd4595cea0321e47ea89e7
```

These hashes were recomputed read-only from the downloaded run
`33155653989` artifact outside the repository.  The driver must require the
future canonical manifest byte-for-byte, not merely search it for a subset
of these values.  Execution remains forbidden until the three exact staged
inputs exist and a later independent audit accepts the driver; missing
staging must fail before the checker starts.

The producer attestation must bind the same run, head, receipt bytes/SHA,
self-digest, and exact producer terminal.  It is an input authentication
record only; it must explicitly state `independent_checker=absent`.

## 3. Checker-only execution

After the exact authority staging is present, the generated shell must:

1. reject stale verdict/log/attestation/terminal/sentinel outputs;
2. invoke only
   `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py`
   on the exact staged receipt and existing exact task176 receipt;
3. apply the same registered 14,400-second / 8 GB / Q0-state / edge / row /
   operation / DAG / serialized-byte / checkpoint-byte limits as the current
   task198 production checker;
4. require exactly one line
   `R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441`;
5. require a nonempty canonical verdict with `accepted=true`,
   `independent=true`, exact receipt bytes/SHA/terminal/rows, and its own
   self-digest;
6. write one checker attestation binding `${GITHUB_RUN_ID}`,
   `${GITHUB_SHA}`, exact checker source identity, verdict bytes/SHA, receipt
   bytes/SHA/self-digest, producer capture run/head/artifact, and terminal;
7. write exactly one final sentinel only after all gates.

The driver must require exactly-one checker terminal, attestation, terminal
file, and sentinel markers.  A checker `UNKNOWN_*`, timeout, missing output,
or untyped process loss is nonpositive.  Never combine a checker verdict
with a different receipt object merely because the terminal strings match.

## 4. Resource and performance accounting

Record that this path performs:

```text
task198 producer invocations = 0
receipt parses in checker process = 1
independent 6441-row checker replay = 1
```

The one checker replay is necessary work.  There may be no preliminary
producer reconstruction, second checker parse/process, sleep, polling loop,
lock, process pool, or unrelated computation.  The driver must publish its
static estimate and physical process count honestly.

## 5. Reply and boundary

List exact driver bytes/SHA and reply byte length.  State that execution is
forbidden until parent exact authority staging and an independent Sol(max)
audit.  End with:

```text
TASK317 CHECKER-ONLY DRIVER:             COMPLETE or BLOCKED
TASK198 PRODUCER RECOMPUTATION:          0
CAPTURE RECEIPT EXACT PIN:               PRESENT
CAPTURE MANIFEST/ATTESTATION:            EXPECTED / NOT YET STAGED
EXECUTION:                               UNEXECUTED
v220 A1:                                 3/4
A4 / LIFT / FAKE / IHARA:                NO PROGRESS
```

`TASK317_R07_TASK198_AUTHENTICATED_CHECKER_ONLY_DRIVER_V1_COMMISSION`
