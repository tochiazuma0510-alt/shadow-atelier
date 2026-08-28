# Luna task 264 — task226 rg/rf variable-collision repair v1

Role: bounded implementation repair only. Read task226, task259, GHA runs
33145825325 / 33146069436 / 33146219086, and all current five task226 files.
Do not run Python, Node, GAP, git, GHA, or network. Edit only those five files
plus the existing task226 Luna reply.

## Exact executed rejection and static owner

- Full driver run `33145825325` failed its sentinel.
- Direct producer diagnostic `33146069436` emitted the exact positive
  SELFTEST terminal.
- Producer+checker diagnostic `33146219086` emitted producer SELFTEST PASS but
  checker `UNKNOWN_INPUT reason=fresh complete ABI rebuild`.

Parent's producer/checker source comparison found the first exact mismatch.
Producer correctly computes the eleven per-occurrence quotient values as
`rkeys_g` and `rkeys_f`, but later reuses the names `rg` and `rf` for flattened
three-block free words. It then serializes those flattened words as
`literals.rg/rf`. The independent checker reconstructs `literals.rg/rf` as
the eleven quotient values, consistent with each occurrence's `r_g/r_f`.
The free block words already have distinct fields `relation_words_g/f` and
`R_B_g0/f`.

## Required repair

1. Remove the producer variable collision. Serialize `literals.rg` and
   `literals.rf` as the exact eleven per-occurrence quotient values, each
   matching the owning occurrence `r_g/r_f`. Keep flattened/block free words
   only in their already named word fields.
2. Producer and checker must explicitly require the eleven `rg/rf` entries to
   equal the independently evaluated `rword_g/rword_f` values and the
   occurrence entries. This is a semantic field gate, not only whole-object
   equality.
3. Inspect the remainder of the reconstructed ABI key-by-key for another
   producer/checker shape mismatch. Do not change class-2 arithmetic, Fox
   identities, ledger, typed UNKNOWN, mutation semantics, or conclusions.
4. Refresh exact driver pins and reply identities. Report UNEXECUTED; parent
   Sol reruns the full producer+checker GHA driver.

A2 remains 1/3 until the full serial SELFTEST passes.
