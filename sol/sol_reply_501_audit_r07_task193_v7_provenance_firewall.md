# Task501 independent audit — Task193-v7 provenance firewall

## Verdict

`GO_FOR_ADOPTION_PENDING_ACTUAL_COMMON`.

All Task501 load-bearing gates pass.  The Task498 provenance blocker is repaired on both real non-fixture paths.  Mathematics changes: **none**.  The affine-prefix construction, replay, resource/checkpoint behavior, compatibility views, search order, and claim meanings remain those of the frozen Task193-v5/v6 owners.

## Frozen pins and generated-source confinement

All frozen files matched before testing:

| subject | bytes | SHA-256 |
|---|---:|---|
| v7 producer wrapper | 9574 | `05cd9bd5c965941d89d09a7ea2a1438e99d7f9fed8effdb0241f1bc2a1a99bc2` |
| generated v7 producer | 18194 | `b5461b39c842bf9d310a4b70fd4be82a43d5249f2380beca27b6fe21459dce87` |
| v7 checker wrapper | 9539 | `4660de49dab3fbb4c749b7c0b841d812b22b77fc1d7ca625ca55755adff1ee48` |
| generated v7 checker | 13831 | `4469ea689ca6dec1864fa842525cb680fa49463789a4dd6357406ff706776cb5` |
| v7 driver | 2887 | `1fba473e278ec98bd33f1daaf5d515b1b92a6c5ec2e27e853ceac47f5bac6041` |
| Task500 reply | 4174 | `abb4625aa04d9ebd2ddf26f5f8fe2643796b86c958afcaa244d5434d224e210f` |

The inherited pins also matched exactly:

| inherited subject | bytes | SHA-256 |
|---|---:|---|
| carrier producer | 17290 | `34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd` |
| carrier checker | 17400 | `fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b` |
| carrier driver | 3019 | `9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99` |
| v6 producer wrapper | 5512 | `0f1bf66f53d8cd4decdcd28b1ef6c1b185329f1b8b00f9e681bff112d8534fc1` |
| generated v6 producer | 12282 | `2d26dd83c930165f740ec53b621b03d1b57b1232a7b2cd1905730033f4e20341` |
| v6 checker wrapper | 5428 | `ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb` |
| generated v6 checker | 7831 | `b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3` |

I regenerated both v7 bodies from those exact v6 owners and obtained the frozen v7 byte counts and hashes above.  Reversing every declared cardinality-checked v7 patch reproduced both v6 bodies byte-for-byte.  AST/source comparison confined the change to v7 schema/markers, the separately inserted provenance gates, final output provenance, and bounded fixtures.  No mathematical or owner-computation path changed.

## Real-path reachability and independence

The actual generated producer `main` calls, in source order, `firewall` at `(76,144)`, owner `load` at `(76,245)`, and `actual_compile` at `(76,300)`.  The actual generated checker calls `boundary` at `(71,64)`, then owner `load`, `check_result`, and `independent_production` at `(72,5)`, `(72,70)`, and `(72,124)`.

A bounded runtime probe fed independently constructed, independently sealed carrier documents to those real `main` functions and stopped at the first frozen-owner `load`:

- an honest producer input reached owner `load`; a re-sealed input missing upstream `binding` did not;
- an honest checker input reached owner `load`; independently re-sealed final-output artifact/head/run drift did not.

Thus neither gate is helper-only or fixture-only.  The producer and checker define and invoke their own predicates in separate generated modules; neither imports nor calls the other's predicate or fixture.  The audit fixture used an audit-local canonical-JSON/SHA-256 seal implementation, not either subject's fixture or seal helper.

## Provenance predicates and adversarial battery

Both predicates require exact head `dd6d90b64e2bfba73d7f131f4da876235746f314`, exact run `33553895281`, and a dynamically supplied artifact which is a string-typed canonical ASCII positive decimal.  They require:

- exactly the five `upstream` keys and exact v5 schema, binding, head, run, and dynamic artifact;
- exactly `v5_result`, `v5_checkpoint`, `v5_checker_log`, `source_head`, `run_id`, and `artifact_id` in carrier `inputs`;
- the retained path/string, positive integer byte-count, and 64-character digest-text identity shapes;
- checker-verdict `inputs` exactly equal to the complete carrier dictionary;
- receipt, upstream, verdict, and final Task193 `source_provenance.carrier_provenance` to bind the same head/run/artifact text.

Two unrelated honest artifact strings, `7` and `987654321012345678901234567890`, passed both actual predicates with `actual_common=false`.

Thirty independently mutated carrier/verdict pairs were re-sealed with the audit-local seal implementation.  Both predicates rejected every pair: missing/extra upstream; wrong upstream schema/binding/head/run; receipt head/run; coordinated artifact `0`, `00`, `01`, `+1`, leading/trailing whitespace, full-width digit, and integer; isolated upstream/verdict artifact drift; verdict head/run drift; missing/extra input; each result/checkpoint/checker-log identity drift on both receipt and verdict sides; and stale v4/v6 dialect.  Separately, final Task193 output artifact, head, and run were each mutated and re-sealed; the real checker rejected all three before owner replay.

Trust-boundary note: there is no hard-coded/default artifact ID, no `100009888831` implementation/driver fixture, and the driver retains the externally supplied carrier files.  A caller that coordinately substitutes and re-seals every artifact field with another canonical decimal, including decimal text numerically equal to the known job number, is structurally indistinguishable to this local firewall and is accepted as a canonical caller-supplied artifact.  Per the clarified Task501 boundary, GitHub supplies the actual API artifact ID after upload; this external dynamic binding is an explicit adoption assumption, not a local defect.  The driver neither loses that binding nor defaults it to the job ID.

## Driver and bounded checks

Static inspection found exact pins for both wrappers, mandatory `D500Carrier` and `D500CarrierVerdict`, one producer invocation, and one checker invocation only after producer acceptance.  Each log must contain its exact owned success line exactly once.  The driver rejects `UNKNOWN`, `RESOURCE`, `ERROR`, and `Traceback`, rejects empty or stale outputs, and contains neither a fixture path nor a v6 marker.  Bounded GAP `ReadAsFunction` passed; only expected unbound-global warnings were emitted.

The supplied producer fixture and checker self-test also passed, but the verdict above rests on the independent real-path probes and mutation battery.  No A0/Task193 heavy owner, production, GHA, or git operation was run.

## Claim state

- A0 remains `0/1 actual`.
- A2 remains `2/3`.
- Compact A5 remains blocked on an actual checker-approved COMMON pair.

TASK501_R07_TASK193_V7_PROVENANCE_FIREWALL_AUDIT_GO
