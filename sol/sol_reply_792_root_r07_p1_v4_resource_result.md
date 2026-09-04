# Root result 792 — canonical P1 v4 resource terminal

Date: 2026-09-04

Status: actual GHA resource result. This note records the terminal and the
smallest next action; it does not promote a canonical P1 lift, A0, COMMON,
compatible lift, fake, Ihara, or `verified`.

## 1. Exact run identity

- workflow: `d972-r07-canonical-p1-dag-degree2-lift-v4`
- run/attempt: `33829243641/1`
- job: `100888477356`
- head: `af6df45eba857234d5b6576e4bd0d0b86eac2181`
- terminal producer exit: `124`
- typed status: `UNKNOWN_RESOURCE`, phase `degree2-lift`

All checkout, immutable-source authentication, bounded selftest, accepted
checker staging, five parent downloads and launch construction passed. The
independent candidate checker did not run because the producer did not reach
EOF.

## 2. Exact reached prefix

The last durable progress receipt in `build.log` is

```json
{"cursor":6400,"durable_bytes":487139163,"elapsed_seconds":2183.8690695719997,"phase":"new","rss_bytes":5206851584}
```

Thus the actual recurrence reached `6400/8059 = 79.4143%` in 36.40 minutes.
RSS was 5,206,851,584 bytes (4.849 GiB), below the 8-GiB virtual-memory and
producer RSS gates. This is a wall-clock cap, not OOM and not a mathematical
negative.

Using only the actual late interval `5120 -> 6400`, the measured rate is
0.4405 seconds/row. At that rate the remaining 1,659 rows take 12.18 minutes
and the recurrence reaches EOF at about 48.58 minutes total. A 60-minute
producer cap therefore has about 11.4 minutes of measured margin. This is an
engineering projection, not a terminal claim.

## 3. Artifact and restart truth

The always-uploaded log artifact is:

- artifact id: `9921870995`
- name: `task781-canonical-p1-degree2-lift-v4-logs-33829243641-1`
- API archive size: 86,585 bytes
- API digest:
  `sha256:25ee5758030b507c2b1fc83debd3314a6e42c215b3b4c16036e7f6a80149f176`
- expiry: `2026-12-03T02:21:57Z`

Its 18 extracted files are logs and provenance receipts only. The partial
`degree2.cache.bin` and `instructions.jsonl` were not uploaded. Producer v7
deletes its temporary output on an exceptional exit, so this particular
prefix is **not resumable**. The `durable_bytes` field means fsynced on the
ephemeral runner, not preserved in the uploaded artifact.

Downloaded `build.log` is 5,621 bytes with SHA-256
`67252e0c105b6244408507c58707ef73428055809353949650a1461d9588106a`.
`build-status.txt` has SHA-256
`9928ea3971cd4135914ba71a26461fe3ea9ff7b1f421136761ef2d7903411836`.
`unknown-resource.json` has SHA-256
`f126fa9a198201168e1e49bf4237b038423207152dd86e6ade4dc64976a2f070`.

## 4. Smallest next action

Do not alter the accepted arithmetic or add a new SELFTEST. The measured
finite repair is a versioned workflow with the same producer/checker and a
60-minute producer cap, followed by one actual GHA run. Raising the cap does
not make a successful run consume the cap; it merely permits the measured
approximately 49-minute recurrence to finish. A more invasive parallel or
resume rewrite is not on the critical path unless this measured-margin run
also returns `UNKNOWN_RESOURCE`.

## 5. v220 mapping

Canonical P1 remains an open diagnostic finite gate. It has advanced from
pre-loop interface failure to an actual 79.4143% arithmetic recurrence with
stable memory and a measured terminal-time remedy. Numerators remain A0
`0/1 actual`, first-rung grades `1/6 cross-checked`, A1 `4/4`, A2 `2/3`, A3
`3/3`, and A4 `1/3`. `verified=false`.

`R07_CANONICAL_P1_V4_UNKNOWN_RESOURCE_TIME_AT_6400_OF_8059`
