# Luna reply 157f — matrix receipt contract

Modified exactly the authorized producer and reply files:

- `search/d972_b4_burau_matrix_v1.g`
- `sol/luna_reply_157f_matrix_receipt_contract.md`

The GAP producer now emits and runtime-gates an honest structured contract:

- hashes the exact producer source at runtime as `producer_source_sha256`;
- emits `source_target_key_digest`, exact generator order, exact A.18 pair
  order, and `kernel_generator_count`;
- emits `exact_kernel_canary` with complete order, distinctness, roof-block
  identity, and deletion-negative evidence;
- emits exactly the requested ten `algorithm_evidence` booleans;
- explicitly rejects any replayed common word not in the constructed `H'`.

The deletion canary uses the actual enumerated `K`: it removes one element,
requires the resulting set/order to be exactly one smaller, and errors if the
negative test is not detected. No `permutation_degree` or producer-side
independence claim was added. q5 order/counts remain unconstrained; q3/q4
constants remain calibration-only and candidate/all-pass semantics are
unchanged.

Static evidence:

- `PRODUCER_CONTRACT_STATIC_PASS`
- `YAML_PARSE_PASS`
- `git diff --check` was run; it reports only pre-existing trailing whitespace
  in unrelated `search/probe/wac_v1/scan_out.txt`.
- final producer SHA256:
  `50C30806C0A76FA4A4A9F33755D3E6C03B41A5C086CA9542F23214205383BB91`

No local GAP, checker, workflow, GHA, or git operation was run.
