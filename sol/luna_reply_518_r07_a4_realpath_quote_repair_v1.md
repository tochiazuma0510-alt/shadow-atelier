# Luna reply 518 -- A4 realpath generated-shell quote repair

Implemented the requested versioned one-line repair.

- Created `search/d972_r07_word_independent_successor_kernel_gha_driver_v47.g` from v46.
- Changed only the generated-shell `realpath --` fragment, removing emitted quote bytes around `D514Input`.
- Exact generated command:
  `test "$(realpath -- ci/in/d972_r07_seven_context_roof_presentation_v1.json)" = "$root/ci/in/d972_r07_seven_context_roof_presentation_v1.json"`

Bounded checks:

1. GAP `ReadAsFunction` parse: exit 0.
2. Independent shell reconstruction: exact command shown above; no shell execution.
3. `bash -n` on repository-external `%TEMP%\luna518\task514_v47.sh`: passed.
4. v46-to-v47 diff: exactly one replaced source line; no other files changed by this task.

Bytes/SHA-256:

- v46: 12544 bytes; `d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7`
- v47: 12536 bytes; `ba74cd1bb09bb87b50c582330bf54f943a5c4c1c77522a518460acf76a5748aa`
