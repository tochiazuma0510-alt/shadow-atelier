# Luna reply 432 — A0 prefix-positive probe v1

Implemented the bounded positive-only fork from task432. The probe byte-pins
the task431/v12 producer, independently seals the exact sequence-40 input,
temporarily replaces only the imported producer's `deque` with a false-truth
content-preserving subclass, and restores the binding in `finally`. The probe
never writes a checkpoint and emits top-level `COMMON_CANDIDATE` or `UNKNOWN`.
A resource stop is retained as `a0.probe_terminal=UNKNOWN_RESOURCE`, because
the unchanged checker requires an output checkpoint for a top-level resource
terminal; all claim-boundary flags remain false.

Allowed output pins:

- `search/d972_r07_a0_prefix_positive_probe_v1.py`: 6270 bytes, SHA-256 `b48d84850a6c0033e62f3e2ebe41bdf14b73f68dcb0670ba06dcf9e825a38bbd`
- `search/d972_r07_a0_prefix_positive_probe_gha_driver_v1.g`: 7620 bytes, SHA-256 `1ebe5d486882dad8674359cbdd5e6afb59945e67cc27d47aeef4cebd1b6c05ba`
- `sol/luna_reply_432_r07_a0_prefix_positive_probe_v1.md`: this designated report (not self-pinned)

The unchanged checker remains task431/v12:

- `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py`: 13334 bytes, SHA-256 `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`

Recovery pins are unchanged and preserved in the distinct task432 driver
paths: zip 132415389 bytes, SHA-256
`75223cf534c5864ec32ad895887c16e0ff097ba8871d72162156dc9fdafc863a`; input
326449173 bytes, SHA-256
`0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1`.
The exact six-entry v12 roster, temporary extraction, regular/non-symlink
gates, release seal, one-shot receipt, external preamble, and exact checker
input binding are retained. No output checkpoint is passed to the checker.

Bounded gates passed:

- probe compile with `python -B` and no repository bytecode;
- false-truth deque fixture preserving length, iteration, and content;
- imported v12 fixture;
- source-level no-checkpoint-write guard;
- unchanged checker self-test;
- driver static/reconstructed receipt checks and `git diff --check`.

This fork is positive-discovery only. A nonpositive result is top-level
`UNKNOWN` (including resource stops), never `NONMEMBER`; it does not promote COMMON_WORD, fake,
Ihara, or compatible-lift claims. No checkpoint was loaded locally, and no
production run, download, workflow edit, commit, push, or dispatch was done.

## Parent dispatch record

After the independent Sol dispatch audit returned `GO`, the parent broker
committed and pushed the exact audited files at immutable head
`eba7ebec4ee7a12d0d199d522f225ce42ba25366`.  Without changing a workflow,
the parent dispatched generic `gap-run.yml` run `33339152288`, job
`99331474026`, with:

```text
script               search/d972_r07_a0_prefix_positive_probe_gha_driver_v1.g
preamble             D972_R07_A0_PREFIX_POSITIVE_PROBE_V1_RUN:=true;;
out_dir              ci/out
timeout_min          180
with_pquot_packages  false
```

The exact continuation run `33337628476`, job `99327291932`, remains a
separate active process.  The probe does not replace or mutate it.

## Parent result record

Run `33339152288`, job `99331474026`, completed successfully.  The probe
authenticated and restored the exact sequence-40 state at rank 1316 and
frontier 906, then completed physical aggregation and the six-action oracle.
Its mathematical terminal is

```text
status  UNKNOWN
reason  positive_only_six_action_exhausted
```

The unchanged checker returned `PASS {"fail_closed":true,"terminal":"UNKNOWN"}`.
Artifact `9740537102` has size 133083510 bytes.  The extracted JSON is 1876
bytes with SHA-256
`3e13a1f2f0bdf78168489349a79d5b2ff63c648a2c2ab6d8b1c813380e6216f2`.
The input checkpoint was independently rehashed to its pinned 326449173 bytes
and SHA-256
`0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1`.

This excludes a positive solution only inside the rank-1316 prefix plus the
complete six-action space.  It is not a full A0 negative.  The current v12
UNKNOWN envelope does not retain the completed physical rank/payload, so no
numerical physical-size claim is extracted from this run.
