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
