# Luna task 254 — task226 mod-9 bracket normalization repair

Role: bounded implementation repair only.  Do not run Python, GAP, git, GHA,
or network commands.  Modify only the five task226 files already owned by this
line:

- `search/d972_r07_actual_two_word_endpoint_specializer_v2.py`
- `crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py`
- `search/d972_r07_actual_two_word_endpoint_specializer_gha_driver_v2.g`
- `search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json`
- `sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`

## Exact observed failure

GHA diagnostic run `33144163231` at head
`21019483b66efee8547c35f398e9dd3c82048db4` produced

```text
D226_PRODUCER_TERMINAL UNKNOWN_INPUT
{"result":{"reason":"Q commutator"}, ...}
```

The class-2 coordinate arithmetic is in `Z/9`.  `cmul`/`mul` returns the
central coordinate canonically in `0..8`, but the base PB3/PB4 bracket tables
contain literal `-1`.  Thus the first negative bracket is compared as `8`
against `-1`.  The same latent mismatch occurs in direct bracket-roster checks.

## Required repair

1. In both producer and independent checker, make the public bracket lookup
   return canonical residues in `0..8` for *both* table orientations.  Do not
   change the multiplication convention, commutator word convention, bracket
   roster, or actual mathematical signs.
2. Preserve producer/checker independence: implement the normalization
   separately in both files; import no producer helper in the checker.
3. Inspect every bracket equality in both files and ensure that all compared
   coordinate tuples use the same canonical `Z/9` representation.  Do not
   weaken or delete the commutator and direct-roster assertions.
4. Add a non-vacuous SELFTEST assertion or mutation control that exercises at
   least one *negative* PB3 bracket and one *negative* PB4 bracket, so reverting
   canonicalization is rejected.  If this requires extending the fixture
   mutation roster, update producer, checker, fixture, and reply consistently.
5. Refresh exact byte counts/SHA-256 pins in the GAP driver and reply.  Recheck
   that shell `sha256sum` output is compared to lowercase pins.
6. Keep all conclusion flags false and report `UNEXECUTED`; no claim that the
   repair passed until parent GHA execution.

Report the exact five final byte counts and SHA-256 identities in the reply.
