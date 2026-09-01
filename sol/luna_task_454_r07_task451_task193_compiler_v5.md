# Luna task 454: Task451-carrier-fed task193 compiler v5

Role: Luna implementation owner.  Implement the tagged task193 successor
whose mathematical justification is v417 and whose accepted input is the
independently audited Task452 carrier.  This is an input-firewall and pin
migration, not a new affine-prefix algorithm.

## Frozen owners

Exact-pin all six files below.

```text
search/d972_r07_task451_task193_carrier_v1.py
  8553 / 18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644
crosscheck/check_d972_r07_task451_task193_carrier_v1.py
  8516 / 82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73
search/d972_r07_task451_task193_carrier_gha_driver_v1.g
  2499 / cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a

search/d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2851 / a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py
  2986 / 04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g
  5798 / 7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4
```

## Exact accepted firewall

Consume two physical inputs: a Task452 carrier receipt and its Task452 checker
verdict.  Bind canonical bytes/path/SHA and both self-digests.  Accept only:

```text
carrier.schema   = d972-r07-task451-task193-carrier/v1
carrier.status   = ACCEPTED
carrier.terminal = R07_TASK451_TASK193_CARRIER_V1_ACCEPTED
carrier.claims   = {carrier:true,A2:false,lift:false,fake:false,Ihara:false}

verdict.schema   = d972-r07-task451-task193-carrier/v1/checker
verdict.status   = PASS
verdict.terminal = R07_TASK451_TASK193_CARRIER_V1_CHECKER_PASS
verdict.carrier  = exact physical carrier identity
verdict.claims   = {literal_carrier_replayed:true,A2:false,lift:false,
                    fake:false,Ihara:false}
```

Also require the carrier's exact Task451 pins/input identities and parse its
literal payload.  Independently enforce valid 760-letter `g760`, valid freely
reduced `correction_word` and `corrected_word=red(g760+correction_word)`, and
the complete `direct_replay` gates.  Recompute the historical sparse digest
with `u32be(len(key)) || key || coefficient`; never substitute v12's
little-endian digest.  Require the embedded full replay, all-seven and
eleven-occurrence flags, right multiplication, exponent `[0,0]`, joint
kernel, hexagons, and printed-order pentagon.  Task452's checker verdict is
the independent authentication receipt; do not forge or call the old
history-free adapter-v5 envelope.

Normalize exactly to the dialect-free object

```text
boundary = {
  c_exact: carrier.correction_word,
  corrected_word: carrier.corrected_word,
  g760: carrier.g760,
  direct_replay: {
    row: carrier.direct_replay.physical_row,
    row_sha256: carrier.direct_replay.physical_row_sha256,
    replay: carrier.direct_replay.replay,
    direct_all_seven_replay: true,
    right_g760_multiplication: true,
    hexagons: true,
    pentagon_printed_order: true
  }
}
```

and then to the exact `minimal_input` of v417.  The accepted mathematical run
must call the frozen task193-v4 affine/Fox owner from rank zero.  Retain its
ordinary rows, pointed rows, equality oracle, and presentation-boundary
mathematics byte-for-byte.  Only the accepted input firewall, schema,
terminal, source provenance, checkpoint schema/path, and exact pins advance
to v5.

## Producer/checker independence

- The producer may load the exact v4 producer as the mathematical owner, but
  must not call its old adapter `main` or synthesize a history-free-v5
  receipt.  Give the mathematical core only the normalized in-memory minimal
  input and the new physical carrier/verdict identity.
- The checker implements its own Task452 firewall and normalization.  It may
  load the exact v4 checker for the accepted affine/Fox replay, but must not
  import the new v5 producer or trust its normalized payload/claims.
- A PASS must bind the physical v5 receipt and reproduce all v4 mathematical
  output checks.  UNKNOWN_INPUT and UNKNOWN_RESOURCE remain typed and have
  all task193/A2/lift/fake/Ihara claims false.
- Any resumable checkpoint has a fresh v5 schema and exact carrier/verdict
  input identity.  Never accept or relabel a v4 checkpoint.  Starting the new
  dialect from rank zero is the accepted baseline.

## Bounded tests and performance

Provide a small firewall/minimal-input fixture marked
`actual_task451_positive=false` and mutations for at least: carrier seal,
verdict-to-carrier identity, both schemas/terminals, claims, correction word,
g760/right product, sparse digest, full replay, exponent, joint kernel,
hexagon, pentagon, and exact source pins.  This fixture must not assert
task193 values.  Compile/static/fixture tests only; do not run A0, Task452
production, or task193 production locally.

Do not copy Task451 batches, duals, echelons, Q0 stores, or selector fibres.
Do not add a production SELFTEST, worker pool, retry loop, or new equality
oracle.  The firewall should be seconds-scale before the pre-existing
task193 computation.

## Allowed files

Create only versioned files with these roles:

```text
search/d972_r07_second_frattini_affine_prefix_compiler_v5.py
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v5.g
search/certs/d972_r07_second_frattini_affine_prefix_compiler_v5_selftest.json
  (optional)
sol/luna_reply_454_r07_task451_task193_compiler_v5.md
```

Do not edit v4, Task452, workflows, v220, claims, or provenance.  Do not
commit, push, dispatch GHA, use credentials, or run production.  Report exact
bytes/SHA, reuse boundary, fixture terminals/mutations, and any blocker.  If
the v4 mathematical core cannot be called without its old physical adapter,
STOP with the exact missing ABI instead of weakening the firewall.
