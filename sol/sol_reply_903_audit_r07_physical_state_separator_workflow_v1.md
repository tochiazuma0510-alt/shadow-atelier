# Sol Task903 -- live physical-state / separator workflow v1 audit

## Verdict

**PASS.**  The repaired workflow is accepted for one audited marker/GHA run.
This authorizes only the fresh candidate workflow; it is not a Grade-2 result
and does not promote any state before the independent checker succeeds.

## Exact receipts

| file | bytes | LF | CR | BOM | ends LF | SHA-256 |
|---|---:|---:|---:|---|---|---|
| `.github/workflows/d972-r07-grade2-physical-state-separator-v1.yml` | 20,126 | 405 | 0 | no | yes | `e4ae6b1e7d17e1dc6df3cb7d1470810a535fce4fb8e208239d0614050ca02b78` |
| `sol/luna_reply_902_r07_physical_state_separator_workflow_v1.md` | 5,809 | 134 | 0 | no | yes | `8e71fa9d07deb73bf18b1e285fb3f77bc750508355d29d1d12e3b028679501dd` |
| `search/d972_r07_grade2_physical_state_separator_v1.py` | 75,934 | 1,407 | 0 | no | yes | `5f1267a7296a6f613f46a1d431c807da22239419362f32ea7c08b51fd7d6e13f` |
| `search/check_d972_r07_grade2_physical_state_separator_v1.py` | 57,325 | 734 | 0 | no | yes | `01df70e8c6be4bfdff4fbedc227488edce47b1e9c195466ea7658d36b63ee107` |
| `search/stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py` | 29,738 | 659 | 0 | no | yes | `ce84baea0bc18380af8a20e32eb8862f9adc20ad596c2012e127f8b7b8341a4b` |

The workflow authenticates the last three receipts before executing them.

## Gate table

| gate | result | finding |
|---|---|---|
| 1. two external authorities | PASS | Five exact API queries bind repository `tochiazuma0510-alt/shadow-atelier` / id `1312092366`, completed-success runs and attempts, heads, workflow paths/ids, connection job, artifact ids/names/bytes/digests/expiries, `expired=false`, and source/head repository ids. Downloads use the two fixed artifact names and fixed run ids. No caller input, wildcard, latest-run, `ANY`, fixture, expired, or self-sealed alternative reaches execution. |
| 2. sources, stager and launch | PASS | Producer/checker/stager bytes, LF and SHA-256 are checked exactly, including no CR/BOM and final LF. The workflow constructs canonical API-derived rho2 acquisition and invokes accepted v4 into absent `rho2-flat`; v4 checks and atomically publishes its exact ten-file roster in one bounded copy/hash pass per payload. The canonical ASCII launch has `fixture_only=false`, `resume=false`, fresh absolute roots, exact v11 live/final tuples, accepted v6/v7 identities and exact rho2-v4 identity. |
| 3. narrow computation | PASS | The only production calls are v4 staging, the accepted fresh producer, and the independent checker. The producer offers only the 1,354 authenticated connection rows to the file-backed state, with bound `1354*1353/2=915981`; the checker's separate replay is the commissioned independence pass. No PB3/PB4 rebuild, old A0 scan, SAT/nullspace solve, live resume, checkpoint reuse, or redundant workflow-level connection replay appears. The required 75,319,124-byte rho2 flat copy is streamed and is not duplicated by a hand-copy/select step. |
| 4. failure and publication | PASS | Producer and checker are distinct named steps with 30-minute caps inside a 75-minute job. Timeout/kill codes 124/137/143 write `UNKNOWN_RESOURCE` receipts and remain nonzero; every other error also fails closed. The unchecked artifact is labelled `candidate-unchecked` and is uploaded under `always()` with state/output, acquisition/launch, stager/producer/checker logs, both progress logs and resource receipts. Final `candidate` publication requires both named outcomes to be success and contains only completed state, terminal output and checker result. Both uploads use retention 90 and compression level 0; labels never say verified. |
| 5. static, trigger and efficiency | PASS | YAML parses as one job on `ubuntu-24.04`; Python 3.13 and `numpy==2.5.1` are fixed. There is one marker, `[task902-r07-physical-state-separator-v1]`. `workflow_dispatch` is explicit; an ordinary push starts no job because the sole job condition requires that marker. No literal secret or `secrets.*` reference exists; `github.token` is used only as an environment/action input and is not echoed. The repaired monitors poll completion every 1 second while emitting progress only about every 60 seconds, so each phase has at most about one second of avoidable tail rather than the rejected 60 seconds. File staging is streamed with a 1 MiB buffer, numerical state remains file-backed, and compression 0 avoids an unnecessary CPU-heavy archive pass. |

## Bounded checks

With bytecode output directed outside the repository, compilation of all
three frozen Python sources exited 0.  Stager selftest passed its ordinary
default promotion/return, exact roster, atomic promotion and mutation gates;
producer selftest passed member, separator, nonmonotone insertion and bounded
resume; the independent checker passed both outcomes and rejected all 19
mutations.  The bounded benchmark exited 0 with `status=BOUNDED_ONLY`, six
operations, physical rank 3 and the honest live upper bound 915,981.  No
production artifact was opened.

An independent static parser/census on the final YAML reported one job, one
marker, five API queries, two exact-name/run downloads, two 30-minute phase
caps, one 75-minute job cap, two `compression-level: 0` settings, zero
`sleep 60`, two `sleep 1`, two approximately-60-second progress clocks,
uploaded `checker-progress.log`, and zero `secrets.*` occurrences.  The
initial synchronous-monitor draft had up to 120 seconds of serial tail; the
only audited repair replaces that with at most approximately two seconds
total without changing authority or computation semantics.

```text
VERDICT=PASS
WORKFLOW_ACCEPTED=yes
SAFE_TO_PUSH_TRIGGER_GHA=yes
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
