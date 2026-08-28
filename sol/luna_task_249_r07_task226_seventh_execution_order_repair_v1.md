# Luna task 249 - task226 seventh execution-order repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

Role: bounded surgical implementation repair only.  Do not run Python, Node,
GAP, git, GHA, or network locally.  Edit only the same five task226 files.
Keep all mathematical formulas and the task246 26-name roster unchanged.

## 1. Rejection boundary

The task246 return is rejected before execution for three concrete defects.

1. Producer SELFTEST calls `validate_package(pkg)` and
   `mutation_execution(pkg)` immediately after `specialize`.  Only afterward
   does it attach `terminal_probes`, `output_guard`, and the two binding
   canaries.  Since validation already requires `output_guard`, SELFTEST must
   stop before any semantic test; binding/terminal mutation accessors would
   also be missing.
2. The `word_g0` mutation reverses `[1,2,1]`, and the `word_a` mutation
   reverses `[2,2]`.  Both are palindromes, so these two registered mutations
   do not alter their owner and cannot be honest controls.
3. Producer and checker publish `input_bytes=8_000_000`, while the upstream
   task198 production contract permits a receipt up to 2,000,000,000
   serialized bytes.  Production can therefore hit a preregistered cap before
   reading a legitimate authenticated predecessor.  The cap must cover the
   sum of the registered task192/task198 receipts and sidecars, with an
   explicit finite margin.

## 2. Correct SELFTEST order

The SELFTEST order is exactly:

```text
pkg = specialize(...)
execute zero-safe, arithmetic, malformed-input, and resource probes
attach pkg.terminal_probes
attach pkg.output_guard = fresh-output-only
attach both production-shaped binding canaries
validate_package(pkg)
run mutation_execution(pkg)
attach mutation transcript
validate_package(pkg) again
serialize
```

The checker reconstructs the same order semantically: it validates the final
package, reruns the independent oracles/probes, compares the probes, and runs
its own mutation suite.  Do not weaken an existing gate to make this pass.

## 3. Make the two word mutations nontrivial

For `word_g0` and `word_a`, alter one literal letter to another valid nonzero
signed generator so that:

```text
before_sha256 != after_sha256
```

and the owning `mutation word` gate is reached.  Do not change `word_f` or
reseal/rebuild the dependent package; the purpose is to test the carried-word
relation.  Keep the separate `word_f` mutation distinct and nontrivial.

Producer and checker use independent mutation code but the same registered
owner/reason contract.

## 4. Production-cap alignment

Set `input_bytes` in producer and checker to a finite value at least
2,100,000,000 bytes, or derive an equally explicit finite sum from the pinned
upstream serialized limits plus sidecar margin.  Keep the 6 GiB RSS cap and
live RSS measurement.  The driver estimate/contract must state the same
input bound.  This raises only the admissible authenticated input size; it
does not permit unpinned paths or extra processes.

## 5. Delivery

Re-read the five shared files, refresh driver pins, and report exact
byte/SHA identities.  No execution.  End with:

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
