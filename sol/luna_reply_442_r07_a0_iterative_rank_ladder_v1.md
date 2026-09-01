# Luna reply — Task442 iterative quotient-weighted rank ladder v1

Implemented only the four authorized outputs. The producer exact-pins v4,
rebuilds the authenticated rank-43 prefix, builds the selective Q0/Gamma
runtime once, and repeats six-action-first then weighted-fibre selection.
Every accepted source is direct-replayed, required to pair nontrivially with
the current normalized dual, and required to raise rank exactly once.

Exact mathematical source pins are v4 producer: 3,619 bytes,
`6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f`;
its transitively authenticated v1 source: 24,643 bytes,
`5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc`.

Checkpoint schema is `d972-r07-a0-actual-b72-rank-ladder/v1/checkpoint`.
It stores only the binding, accepted compact sources, round/rank/count,
reason, and canonical state digest. It never stores physical rows, Q0 stores,
formulae, or fibre caches. Restart rebuilds rank 43 and replays every compact
source with pre/post remainder and dual digests, row digest, scalar, pivot,
exponents, and rank transition.

On target zero, producer and checker independently reconstruct the selected
literal product from all direct correction sources, keep action ancestry
separate, apply the v12 u0/v0 exactification lattice, and require exact
exponents, joint identity, fresh all-seven correction replay, and target zero.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_rank_ladder_v1.py` | 16068 | `880c4fe79b28391e3fa2d439566298cf3d9d2dfdbd9759615cd3c3300049fa7a` |
| `crosscheck/check_d972_r07_a0_actual_b72_rank_ladder_v1.py` | 7746 | `d95d52f806aa29b497d014ee0c6efe37436b38fb6c82a745677e0c852c6730b1` |
| `search/d972_r07_a0_actual_b72_rank_ladder_gha_driver_v1.g` | 2299 | `a075c0f403fee6b354677c41a4094b6ae4a71b8e00d2c67120a9272a5ca2709b` |

Memory audit: the live packed physical echelon grows by one reduced pivot row
per rise. Fixed three-coordinate selective stores remain 176,359,680 bytes
and are built once. Formula/adjoint objects are released after each weighted
rise and the per-target singleton cache is cleared; checkpoint serialization
is compact and cannot duplicate the physical basis or Q0 stores.

The weighted adjoint compiler remains the exact byte-pinned Task436
implementation. If a later normalized dual leaves that authenticated ABI,
the ladder stops fail-closed as `UNKNOWN_RESOURCE:current_dual_adjoint` with
the last compact rank checkpoint; it never converts an unsupported adjoint
shape into EMPTY or NONMEMBER.

Bounded gates only: external-cache compilation, producer fixture, independent
checker self-test with compact-field mutations, static driver reconstruction,
and `git diff --check`. No production, Q0, GHA, workflow edit, commit, push,
download, old occurrence closure, or broad SELFTEST was run.
