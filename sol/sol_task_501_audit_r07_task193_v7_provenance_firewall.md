# Sol(max) task 501 - audit Task193-v7 rank99 provenance firewall

Role: independent Sol(max) mathematical/implementation auditor.  Audit only
the Task500 repair of Task498's exact provenance defect.  Do not edit the
implementation, run A0/Task193 production, GHA or git, and do not broaden the
Task193 search.  Write only
`sol/sol_reply_501_audit_r07_task193_v7_provenance_firewall.md`.

Read Task496, Task498, Task500 and their replies in full.  Do not trust
Task500's fixture or prose.  Use bounded read-only checks and independently
constructed temporary fixtures.

## 1. Frozen subject

- v7 producer wrapper, 9574 /
  `05cd9bd5c965941d89d09a7ea2a1438e99d7f9fed8effdb0241f1bc2a1a99bc2`;
- generated v7 producer, 18194 /
  `b5461b39c842bf9d310a4b70fd4be82a43d5249f2380beca27b6fe21459dce87`;
- v7 checker wrapper, 9539 /
  `4660de49dab3fbb4c749b7c0b841d812b22b77fc1d7ca625ca55755adff1ee48`;
- generated v7 checker, 13831 /
  `4469ea689ca6dec1864fa842525cb680fa49463789a4dd6357406ff706776cb5`;
- v7 driver, 2887 /
  `1fba473e278ec98bd33f1daaf5d515b1b92a6c5ec2e27e853ceac47f5bac6041`;
- Task500 reply, 4174 /
  `abb4625aa04d9ebd2ddf26f5f8fe2643796b86c958afcaa244d5434d224e210f`.

The frozen carrier trio and rejected v6 transformation owners are exactly the
pins in Task500.  Reproduce both generated v7 bodies independently.  A pin
mismatch is a preflight STOP.

## 2. Audit question

Decide whether v7 repairs the only Task498 blocker while preserving the
Task193-v5 mathematics and positive-only handoff.

Independently establish:

1. The real non-fixture producer calls its patched `firewall` before any
   Task193 owner call; the real checker calls its separately implemented
   `boundary` before compatibility/owner replay.  This must not be another
   helper-only/self-test-only wiring error.
2. Both paths require exact head
   `dd6d90b64e2bfba73d7f131f4da876235746f314`, exact run
   `33553895281`, and a string-typed canonical ASCII positive-decimal artifact
   id.  No artifact id is hard-coded; job `100009888831` is not accepted as a
   substitute.
3. `upstream` has exactly the five Task500 keys and exact v5
   schema/binding/head/run, with `production_artifact_id` equal to the dynamic
   receipt artifact.  Missing or extra fields fail after outer resealing.
4. Carrier `inputs` has exactly the three physical identities plus
   source-head/run/artifact, with the old identity-shape gates retained; the
   carrier-checker verdict inputs equal that complete dictionary exactly.
5. Receipt, upstream, carrier-verdict and final Task193 output provenance bind
   the same dynamic artifact/head/run text.  A change to any one of the three
   physical identities or provenance coordinates fails even after every
   affected outer seal is recomputed.
6. Producer and checker predicates are genuinely independent: neither imports
   nor calls the other's helper, and a correlated implementation mistake is
   not hidden by shared fixture construction.
7. Generated v6-to-v7 diffs are confined to version/schema/markers, the two
   provenance gates, output provenance and bounded fixtures.  Affine-prefix
   linear algebra, actual compilation, search order, replay, resource bounds,
   checkpoints, compatibility views and claim meanings are unchanged.
8. The v7 driver exact-pins both wrappers, requires explicit carrier receipt
   and verdict, runs one producer and one post-acceptance checker, accepts one
   exact owned success line each, and cannot accept UNKNOWN/RESOURCE/ERROR/
   Traceback, empty/stale output, v6 markers, or a fixture path.

## 3. Bounded adversarial checks

Call the actual generated `firewall` and `boundary` through independent
fixtures.  Re-seal all relevant envelopes and test at least: missing/extra
upstream, wrong head/run/binding/schema, artifact `0`, `00`, `01`, signed,
whitespace, non-ASCII digit and integer, upstream/receipt/verdict/output drift,
each of the three physical-identity drifts, missing/extra input key, and stale
v4/v6 dialect.  Include two different honest canonical artifact strings to
show the value is dynamic.  Keep `actual_common=false`.

Also reproduce AST/diff confinement, driver pins/call counts/markers, bounded
GAP `ReadAsFunction`, and generated-source hashes.  Do not run the heavy
Task193 owner.

Return `GO_FOR_ADOPTION_PENDING_ACTUAL_COMMON` only if every gate passes.
Otherwise return `STOP_DO_NOT_ADOPT` with the smallest exact reproducer and
minimal repair.  In either case A0 remains `0/1 actual`, A2 remains `2/3`, and
compact A5 remains blocked on an actual checker-approved COMMON pair.

End with exactly one of:

`TASK501_R07_TASK193_V7_PROVENANCE_FIREWALL_AUDIT_GO`

or

`TASK501_R07_TASK193_V7_PROVENANCE_FIREWALL_AUDIT_STOP`
