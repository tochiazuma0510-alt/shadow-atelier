# R07 task198 direct production acceptance v264

Author: Sol / 2026-08-28

Status: artifact and provenance audit of the completed producer-plus-
independent-checker GHA run.  This closes v220 A1 only.  It does not execute
A4, construct an actual first correction, or declare a lift, fake, or Ihara
witness.  The evidence class is `cross-checked`, not Lean `verified`.

## 1. Immutable run and artifact

GitHub Actions run `33155710862` completed successfully at immutable head

```text
bed1d5e6b41477b8799f2a33a24e46f7800f9510
```

The GAP-script step ran from `2026-08-28T08:32:40Z` through
`2026-08-28T12:57:18Z`.  Artifact `9686477718`, named `gap-run-out`, has the
GitHub archive digest

```text
sha256:8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854
```

An independent download to a directory outside the repository gave these
load-bearing members:

| member | bytes | SHA-256 |
|---|---:|---|
| production receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| producer log | 399 | `d0d025088bae5f418a6e586d3c926d08740697c0872c0bc0ca3506f0af787bd1` |
| checker log | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| terminal | 24 | `871dcf46449cf9e5313a6de0d5478d66813fa2879d185960b66f114cf91d5f3b` |
| final sentinel | 55 | `21132c5d1dc58a8c56673089c8bf29b7a53f960d60fd4595cea0321e47ea89e7` |

The exact terminal evidence is

```text
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441
```

and the verdict is canonical JSON with `accepted=true`,
`independent=true`, and the same receipt terminal.

## 2. Receipt contents and independent replay

The accepted receipt has status `COMPLETE`, terminal
`ROOF_BRIDGE_ISOMORPHISM`, self-digest

```text
c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f
```

and the following independently replayed structural payload:

- 6,441 presentation rows in the exact layer-local split
  `6318 + 104 + 19` and seven sealed chunks;
- row digest
  `e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950`;
- exact normal generation and normal closure;
- bridge image order `357128352` and bridge kernel order `1`;
- seven block maps, eleven typed occurrences, eleven ten-to-eleven maps,
  and four marked inverse replays; and
- the v188 evaluator ABI with the ten distinct E3/E4 typed coordinates.

The independent checker reconstructed the task176 input, the complete
presentation, the quotient bridge, all 6,441 relator bridge traces, the
occurrence ledger, and the evaluator contract before emitting its PASS.

## 3. Comparison with the producer-capture run

The earlier producer-only capture `33155653989` had receipt SHA-256
`d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b`.
Top-level canonical-object comparison of that receipt with the direct-run
receipt shows exact equality for every mathematical and structural field:

```text
D_all, Delta0, Gamma, Q0, bridge, evaluator, input, resume,
direct_Delta_states_enumerated, million_row_Q0_Schreier_stream,
cofinal_lift, fake, Ihara_witness, schema, status, terminal.
```

The only unequal payload is `resource`: elapsed seconds are
`10564.409710082` versus `10845.990959367`, and peak RSS is `2195398656`
versus `2204901376`.  All integer work counters and limits agree.  The
receipt self-digest consequently changes as designed.  Thus the byte-level
difference is runtime telemetry, not a different presentation, bridge,
row roster, or evaluator.

## 4. Acceptance and frontier

Run `33155710862` supplies the previously missing combined actual producer
and independent-checker production acceptance.  Therefore v220 A1 advances
from **3/4 RUNNING** to **4/4 CROSS-CHECKED**.

This does not by itself increment A4.  A4 still requires a separately
audited lightweight consumer, a frozen exact authority manifest and
attestations, actual invariant closure, and an accepted word-bearing
successor kernel/anchor.  Task198 also declares neither a cofinal lift nor a
fake/Ihara result.

```text
TASK198 DIRECT PRODUCER:                 ROOF_BRIDGE_ISOMORPHISM
TASK198 INDEPENDENT CHECKER:             PASS / rows=6441
TASK198 EVIDENCE:                        CROSS-CHECKED
V220 A1:                                 4/4
V220 A4:                                 0/3
COMPATIBLE LIFT / FAKE / IHARA:          NONE
```

`R07_TASK198_DIRECT_CROSSCHECKED_ACCEPTANCE_V264`

Authority-bundle staging commit:
`fbd71e522368f77a43041195af54c798df5bd0bd`.
