# Luna task 157ca — strongest next exact finite obstruction

## Objective

Prepare the strongest **nonredundant and computationally feasible** next
finite necessary-condition test for a frozen B4 roof row, in case the active
q5/q7 and synchronized Burau campaigns all pass.

Audit the existing SAT, Magnus, Burau, permutation, and third-party packageGT
finite-quotient machinery.  A proposed quotient must be a genuine continuous
finite quotient of the relevant profinite free/pure braid data, and its tested
identity must be a necessary condition for a \hat{GT} lift.  It must add
information not already implied by the active q3/q4/q5/q7 Burau lanes.

Rank candidates by exact or rigorously bounded image/fiber size, memory, and
chance of separating a row.  Prefer a quotient whose complete fiber can be
certified without enumerating an infeasible full matrix group.  Sampling or
bounded word search cannot certify a zero.

## Deliverable

Write `sol/luna_reply_157ca_next_finite_obstruction.md` containing:

1. the audited candidate list and redundancy eliminations;
2. the selected quotient/identity and the proof of finite-fiber completeness;
3. an exact GHA computation/certificate specification and resource estimate;
4. either a ready implementation or a precise blocker.

If and only if a sound feasible candidate is found, you may create:

- `search/d972_b4_next_obstruction_v1.py`
- `search/check_d972_b4_next_obstruction_v1.py`
- `.github/workflows/d972-b4-next-obstruction-v1.yml`

Use independent producer/checker logic, negative selftests, fail-closed source
hashes, bounded memory, and always-uploaded evidence.  Do not modify existing
files, dispatch GHA, run GAP, run a heavy local enumeration, or use git.

End the reply with `NEXT_FINITE_OBSTRUCTION_READY` or
`NEXT_FINITE_OBSTRUCTION_BLOCKED`.
