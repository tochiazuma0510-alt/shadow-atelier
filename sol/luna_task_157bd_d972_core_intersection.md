# Luna task 157bd — D972 roof core intersection with the C2^24 B4 cell

Role: Luna implementation/mathematics reinforcement.  This is the next
highest-priority B4-B gate after 157ax.  Do not run local GAP, git, push, or
GHA.  The parent is the only broker.  Small Python-only checks are allowed.

## Fixed objects

Use the exact marked PB3 quotients already frozen in the repository:

- `N_E = ker(PB3 -> E)` for the nonsplit `2^6.PSL(2,8)` receipt;
- `N_P = N_S4 = ker(PB3 -> P)` with `P=PSL(2,8)`;
- `N_M = K^(9) intersect N_P`, the fixed D972 PB3 roof;
- the four canonical strand-deletion maps `d_i:PB4 -> PB3` from
  `search/certs/d972_b4_marity_reduction_maps_v1.json`.

Put

```text
C_E = intersection_i d_i^-1(N_E),
C_P = intersection_i d_i^-1(N_P),
C_M = intersection_i d_i^-1(N_M),
K_0 = C_E intersection C_M.
```

157ax/157ba establish the finite structural target
`C_P/C_E ~= V^4 ~= C2^24`.  Since `N_M <= N_P`, `C_M <= C_P`, and therefore
there is a canonical injection

```text
W := C_M/K_0  -->  C_P/C_E ~= V^4.
```

## Required decision

Determine the exact image `W` for these pinned maps.  In particular decide,
with a replayable certificate, whether

```text
W = V^4  (rank 24),
0 < W < V^4, or
W = 0.
```

This is a finite joint-image problem.  A valid equivalent formulation is to
construct the image of PB4 under the four E coordinates together with the
four `G9=PB3/K^(9)` coordinates, and compute the kernel of the G9^4
projection inside the E^4 image, then intersect the E^4 image with V^4.
Do not assume the four-delete map to `G9^4` is onto: PB4 abelianization can
create compatibility constraints.  Do not infer survival from order labels.

Bind the exact marked generators and conventions.  Replay all six PB4 pure
generator rows.  If the computation can be reduced to a structural proof or
linear algebra, spell it out and independently check the ranks/witnesses.
If a GAP producer is needed, create versioned assets only:

```text
search/d972_d972core_c2six_intersection_v1.g
search/check_d972_d972core_c2six_intersection_v1.py
.github/workflows/d972-d972core-c2six-intersection-v1.yml
```

The full receipt must contain lossless generators for `W`, its F2 rank,
their words in the six PB4 generators, replay in E^4, vanishing in P^4 and
G9^4, and the induced B4 action/composition-factor data.  The independent
checker must rebuild the maps without importing producer helpers.  A timeout
is UNKNOWN.

## Mathematical boundary

- You may use 157ax's exact `C_P/C_E ~= C2^24`, but bind its inputs rather
  than trusting a prose label.
- Isolation of `C_E,C_P,C_M` is being audited separately in 157bb.  Record it
  as conditional until that theorem/certificate passes.
- Do not claim `ML`, 325, cofinality, B4-B, or an Ihara counterexample from a
  nonzero `W`.  State exactly how a nonzero/24-dimensional result feeds the
  first-chief correction lane.
- Do not use the old raw-158 presentation.

## Reply

Write the full report to
`sol/luna_reply_157bd_d972_core_intersection.md`, ending with one exact
verdict token such as `D972_CORE_INTERSECTION_RANK_24_READY_FOR_GHA`,
`D972_CORE_INTERSECTION_NONZERO_RANK_R`, or
`D972_CORE_INTERSECTION_ZERO`/`BLOCKED_<reason>`.
