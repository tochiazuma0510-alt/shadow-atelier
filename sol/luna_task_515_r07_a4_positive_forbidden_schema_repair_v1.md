# Luna task 515 -- A4 positive forbidden-schema repair

Role: Luna implementation only.  Do not run production traversal, GHA, git, or
edit any file other than the two versioned outputs and the named reply.

## Frozen inputs

- `search/d972_r07_word_independent_successor_kernel_gha_driver_v45.g`
  - 12430 bytes
  - SHA-256 `d59bee6ea9a5366643d5409505ce25e91baa7c18031911eea36565e2f221782f`
- generated producer v25 positive output uses exactly
  `{"lift": false, "fake": false, "Ihara": false, "base_pairs": false,
  "ambient_E3_E4_enumeration": false}`;
  its RESOURCE output uses exactly the first three keys.
- generated checker v35 has the same distinction: positive uses five keys,
  RESOURCE uses three keys.

## Required minimal repair

Create the versioned successor
`search/d972_r07_word_independent_successor_kernel_gha_driver_v46.g`.

Preserve v45 byte-for-byte except for its positive-terminal JSON predicates:

1. Producer PASS must require the exact five-key false dictionary above.
2. Checker PASS must require the exact five-key false dictionary above.
3. Producer RESOURCE and checker RESOURCE must continue to require the exact
   three-key false dictionary `{"lift": false, "fake": false, "Ihara": false}`.
4. Preserve every v45 authority, digest, member, regular-file/non-symlink,
   elapsed, timeout, resource, terminal-cardinality, forbidden-token, and
   execution gate.  Do not refactor or broaden the change.

Run only bounded static checks: GAP parse (`ReadAsFunction`) and generated-shell
`bash -n` if already exercised by the driver without production traversal.  Do
not execute the production shell.

Reply to
`sol/luna_reply_515_r07_a4_positive_forbidden_schema_repair_v1.md` with exact
bytes/SHA-256, a concise diff-accounting statement, and test results.
