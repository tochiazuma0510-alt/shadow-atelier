# Luna task 379: R07 actual A0 class-two q2 compiler v1

Date: 2026-08-29

Role: mechanical implementation of v355.  Do not run production/GHA, edit a
frozen owner, add SELFTEST/mutation/retry lanes, or attempt cyclic-return/A9
completion.  Create only the three executables and reply listed below.

## Frozen contract

Read in full:

- `sol/proof_r07_actual_a0_to_class_two_q2_compiler_v355.md`;
- `sol/proof_r07_class_two_quadratic_remainder_compiler_v266.md`;
- task193-v3 producer/checker/driver;
- task292-v2 producer/checker, especially the PB3/PB4 presentations;
- task377-v5 only as an example of the current task198/task193 physical
  authentication paths.  Do not require an A5/A7 parent.

Exact frozen pins:

```text
search/d972_r07_second_frattini_affine_prefix_compiler_v3.py
  2826 bytes
  1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v3.py
  2792 bytes
  5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6
search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v3.g
  5798 bytes
  c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84
search/d972_r07_actual_three_exact_pb_endpoints_v2.py
  40044 bytes
  c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208
crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py
  46873 bytes
  8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8
search/d972_r07_word_independent_successor_kernel_v12.py
  7209 bytes
  816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5
crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py
  8074 bytes
  7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47
```

Reuse the deeper task198-v6 producer/checker pins already frozen in task377.
Accept only a physical task193 MEMBER receipt and matching accepted
independent verdict.  Reconstruct task198 producer contexts on the producer
side and task198-v14 checker arithmetic on the checker side.  A missing or
non-MEMBER parent is `UNKNOWN_INPUT`, not a q2 or witness obstruction.

## Producer algorithm

1. Authenticate `g760`, `correction_word`, `corrected_word` and all relation
   words from task193.  Require literal
   `corrected_word=reduce(g760*correction_word)`.  The applied word is exactly
   `correction_word`; never substitute A5 `mu1` coefficients for it.
2. Reconstruct the eleven task198 occurrence rows and the physical printed
   H1/H2/P factor order exactly as the v4 endpoint owner does.  For each row
   compute `g_o=rho_o(g760)`, `a_o=rho_o(correction_word)` and the v355 factor
   `d_o=P_hat_o*a_o^sigma_o*P_hat_o^-1`.
3. Independently construct the complete block relation words at `g760` and
   `corrected_word`.  Require literal free reduction of the ordered product
   of all `d_o` to equal `R_B(corrected)*R_B(g760)^-1`.  Store the exact order,
   not merely the eleven ordinals.
4. For PB3 and PB4 build the sparse class-two exponent-three coordinate owner
   from task292 `pure_relations`: degree one is the registered generator basis;
   degree two is the wedge basis modulo the echelon of every relator's
   degree-two initial form.  Directly require every full relator coordinate
   to vanish after quotienting.
5. Scan each literal `d_o` by the BCH law
   `(u,U)*(v,V)=(u+v,U+V+2*u wedge v)` over GF(3).  Retain raw and
   relation-reduced `(ell_o,tau_o)` coordinates.
6. In exact block factor order compute
   `q2_B=sum(tau_o)+2*sum_(o<o') ell_o wedge ell_o'`.  Also scan the complete
   ratio word once and require its class-two coordinate equals
   `(sum ell_o,q2_B)`.

The COMPLETE receipt contains the authenticated parent identities, full
occurrence/factor ledger, literal ratio replay, PB relator initial-form
matrices/echelons, every occurrence coordinate and the three tagged q2
vectors.  It may claim only `q2_computed=true` for the accepted A0 word.
`q2_return`, A9 completion, compatible lift, mixed-prime/perfect-core, fake
and Ihara remain NONE.

## Resource/checkpoint boundary

This is a finite sparse scan, not a search.  Expose seconds, RSS, operations
and checkpoint-byte caps.  Checkpoint after each PB roster and occurrence;
resume is all-or-none path/bytes/SHA and binds all sources plus task193 and
task198 physical owners.  A controlled cap is `UNKNOWN_RESOURCE`, never a
NONMEMBER result.  Persist literal words and sparse integer rows only.

## Independent checker and driver

The checker must not import the new producer.  Use task198-v14 and the
checker-side task292 `presentation_relators`, `pure_pairs` and free-word
implementation.  Reconstruct all eleven factors, the literal ratio, its own
wedge quotient bases, every occurrence coordinate and all three q2 vectors.
Compare mathematical sparse coordinates, not producer pivot numbering or a
hash.

The ASCII GAP driver runs one producer and, only on COMPLETE, one checker.
It exposes task193 receipt/verdict, the five task198 authority paths and the
resource/resume inputs.  Preserve receipt, verdict, checkpoint and two logs.
No GHA dispatch in this task.

## Deliverables

- `search/d972_r07_actual_a0_class_two_q2_v1.py`
- `crosscheck/check_d972_r07_actual_a0_class_two_q2_v1.py`
- `search/d972_r07_actual_a0_class_two_q2_gha_driver_v1.g`
- `sol/luna_reply_379_r07_actual_a0_class_two_q2_v1.md`

Run only bounded static checks: Python in-memory byte compilation, frozen
owner restoration, GAP `ReadAsFunction`, ASCII and exact driver pins.  If a
physical task193/task198 field cannot supply v355's literal factorization,
stop at that first ABI site and report it; do not guess or patch the parent.
