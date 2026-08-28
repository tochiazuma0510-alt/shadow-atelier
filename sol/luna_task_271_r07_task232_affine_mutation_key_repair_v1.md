# Luna task 271 - task232 affine mutation key repair v1

Role: bounded two-owner implementation repair only. Read task267 and GHA
diagnostic run 33147829352. Do not run Python, Node, GAP, git, GHA, or network.
Edit only the same five task232 files plus its existing Luna reply.

The one-mutation-at-a-time diagnostic proved that 55/57 producer mutations
are rejected. The only unrejected names are `affine_multiplication` and
`affine_inverse`. Their construction uses `name.replace("_order", "")`, which
creates new keys `affine_multiplication` / `affine_inverse`; the extant checked
owners are `affine_checks.multiplication` / `.inverse`. Map these two names to
those exact extant keys. Preserve `crossed_derivation_order` mapping, the
57-name roster, all mathematics, terminals, caps, and conclusions. Refresh
driver/reply identities and report UNEXECUTED. Parent Sol will rerun the full
serial GHA SELFTEST.

A4 remains 0/3 because actual task198 K has not been run.
