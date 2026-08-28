# Luna task 252 - task232 built-in H2(9) projection repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_232_r07_word_independent_successor_kernel_v1.md`.

Role: bounded implementation repair only.  Read tasks244/244b, proof v247,
and the current five task232 files in full.  Do not run Python, Node, GAP,
git, GHA, or network locally.  Edit only those same five task232 files.

## 1. Exact rejection

The returned production path requires a callable `q1_z0_evaluator` (the
checker first looks for `d1_z0_from_source_word`) in the pinned task179
runtime.  Neither API exists anywhere in the pinned dependency cone.  Hence
the current A4 producer is guaranteed to return
`UNKNOWN_INPUT: Q1_Z0_EVALUATOR_NOT_PROVIDED` before building the actual
kernel.  An honest guaranteed STOP is not an implementation of the v247
anchor.

## 2. Built-in producer projection

Implement the small quotient directly in task232; do not edit task179.  Use
the frozen normal form

```text
D1 = H2(9), element = (a,b,r) = x^a y^b [x,y]^r
(a,b,r)*(a',b',r') = (a+a', b+b', r+r' - b*a') mod 9
(a,b,r)^-1 = (-a,-b,-r-a*b) mod 9
x=(1,0,0), y=(0,1,0)
```

Evaluate each literal signed source word left-to-right.  For every accepted
K-basis word require a value `(0,0,r_i)` with `r_i` in `{0,3,6}`, and set
`a_i=r_i/3 mod 3`.  Require some nonzero `a_i`, choose the least such index,
let `e=a_i^-1` in F3, and freely reduce the selected word concatenated `e`
times.  Directly re-evaluate that word to `(0,0,3)`.

Do not serialize `delta0_identity`, `delta1_k_membership`, or `replay` as
bare asserted booleans.  Replay the selected word through the existing
complete ten-context roof evaluator and actual K/boundary membership oracle;
retain the returned ten roof values, membership coefficients, and the full
D1 values of every basis word.  Only then set the summary booleans.

## 3. Independent checker

The checker must implement its own H2(9) multiplication, inverse, free-word
evaluation, and least-index solve without importing producer code or calling
a producer-supplied evaluator.  It must independently replay the selected
word through its ten-context evaluator and complete boundary-plus-K oracle,
then compare all basis projections, selected index/scalar/source word,
Delta0 values, K coordinates, and D1 target with the producer receipt in both
directions.  Remove both missing-API fallbacks.

The seven anchor mutations must target these reconstructed objects, not only
summary booleans.  Keep the literal commutator cube forbidden.  Update the
SELFTEST to exercise a nonzero exponent-two basis projection as well as the
least-index rule.  Refresh fixture/driver pins and correct the Luna reply's
currently stale checker identity.  Re-read all five shared files and report
exact byte/SHA identities.  Remain `UNEXECUTED`.

