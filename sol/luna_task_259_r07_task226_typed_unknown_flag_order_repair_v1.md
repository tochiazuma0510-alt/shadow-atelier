# Luna task 259 — task226 typed-UNKNOWN flag-order repair v1

Role: bounded implementation repair only. Read task226, task258, and the
current task226 producer/checker/driver in full. Do not run Python, Node, GAP,
git, GHA, or network. Edit only the same five task226 files plus the existing
task226 Luna reply.

## Exact parent rejection

The producer's exception envelopes for `UNKNOWN_INPUT` and
`UNKNOWN_RESOURCE` intentionally contain only the typed reason (and, for one
resource path, the meter). They do not assert downstream mathematical
conclusion flags. The checker currently requires all six top-level false
flags before it reads the terminal. Therefore an authentic
`UNKNOWN_RESOURCE` receipt is converted by the checker to `UNKNOWN_INPUT`,
and the serial driver's exact producer/checker terminal-equality gate fails.
This breaks the advertised typed-UNKNOWN contract.

## Required repair

1. Authenticate schema, self-digest, and terminal before any conclusion-flag
   gate. For `UNKNOWN_INPUT` and `UNKNOWN_RESOURCE`, preserve that exact typed
   terminal, do not run accepted-package reconstruction, do not write an
   accepted verdict, and do not require mathematical conclusion flags.
2. Require all six top-level flags to be exactly false for SELFTEST and
   COMPLETE receipts. Retain the package-level false-flag validation and the
   non-vacuous `forbidden_conclusion` mutation.
3. Retain exact producer/checker terminal equality in the driver. Add or
   retain executable terminal probes sufficient to show both typed terminals
   survive independent checker classification; do not weaken an exception to
   a positive result.
4. Do not change PB3/PB4, word, Fox, ABI, ledger, mutation-owner, arithmetic,
   or conclusion semantics. Refresh exact driver pins and reply identities.
   Report UNEXECUTED; parent Sol will run GHA.

A2 remains 1/3 until both producer and independent checker SELFTEST pass.
