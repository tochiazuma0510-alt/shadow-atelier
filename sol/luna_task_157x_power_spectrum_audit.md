# Luna task 157x - independent audit of D972 power spectrum v1

Role: independent implementation and mathematical auditor. Do not run local
GAP, do not edit the producer/checker/workflow, and do not use git/GHA.

Allowed write only:

- `sol/luna_reply_157x_power_spectrum_audit.md`

Audit the four artifacts produced under task 157r:

- `search/d972_power_spectrum_v1.g`
- `search/check_d972_power_spectrum_v1.py`
- `.github/workflows/d972-power-spectrum-v1.yml`
- `sol/luna_reply_157r_d972_power_spectrum.md`

Required checks:

1. Establish exactly which frozen D972 model is loaded, whether all 972
   canonical rows are reconstructed without guessed multiplication, and
   whether the operation/order/power-table orientation agrees with the
   repository's GT-shadow composition convention.
2. Check that the Python checker is genuinely independent: it must not import
   the producer or share multiplication/order helpers, and it must replay a
   lossless serialized receipt rather than trust summaries/digests.
3. Adversarially inspect identity, closure, inverses, associativity coverage,
   exact element orders, exponent, order histogram, square/cube maps, and the
   proposed finite-state data needed for the 2/3 power game. Identify any
   unchecked inference.
4. Confirm that arithmetic membership is fail-closed. Cardinality 324 or a
   row ordering must never be used to invent the arithmetic subgroup; outside
   spectra must remain UNKNOWN unless authenticated generators/list are
   actually supplied.
5. Check workflow pins, source hashes, artifact upload, time/memory limits,
   and that the workflow really executes both producer and checker on Linux.
6. Run only light static/Python self-tests. No local GAP. Report exact hashes,
   commands, and PASS/FAIL findings. Any semantic error is a blocker.

This audit may approve a GHA candidate measurement only. It cannot promote an
A/B conclusion or authenticate the missing arithmetic image.
