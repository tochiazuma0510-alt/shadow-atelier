# Luna reply 172 — full-E4 orbit preflight repair v7

Terminal: `R07_FULL_E4_ORBIT_PREFLIGHT_READY`.

This is only a bounded successor-preflight receipt. No full correction orbit,
full D2 prefix, GHA, git, literal A18, cofinal lift, fake, or Ihara witness
was run or claimed.

## Authenticated bridge

The producer consumed the full q3 artifact (26 nonempty signed words,
word-roster digest `08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f`, artifact SHA
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`) through
the authenticated predecessor API. It reconstructed typed E4, 31 contexts,
46 aliases, all 6,318 gamma + 104 action + 19 q0 signed-word rows, and 11
raw PB4 Fox rows with value identity and `D1=0`.

The g760 word has length 760, zero exponent sums, and SHA
`518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`.
Action rows use the frozen token order with the trailing inverse letter and
layer-local ordinal `ri*4+li*2+(1 for orient +1, 2 for orient -1)`.

## Fox and same-context canaries

The target6 formula uses the exact substitutions `(X0,Y0)`, `(X0,Z0)`, and
`(Y0,Z0)`, convention `corrected_minus_base`, and transport
`constant*psi(u)` under the left-action convention. The actual deterministic
sample passed 101/101 rows:

```text
gamma_edge 35
xy_action  33
q0_relator 33 (19 eligible rows expanded by distinct conjugators)
same-context pairs 5
```

Each pair has full direct/predicted sparse transcript in the certificate. The
five same-context checks use a separate eligible joint-kernel `k`, with
`v=u*k`; the two freely reduced conjugates differ, have identical three
context states, and have identical Sigma rows. Empty-u and noncommuting-u
canaries pass.

## Independent checker and toy

The checker does not import the producer. It loads authenticated predecessor
modules under fresh names and independently reconstructs E4, context
registry, the 6,441-word roster, all 11 PB4 rows, g760, and every one of the
101 Fox direct/predicted transcript rows. Producer and checker were run
serially twice. Both checker runs emitted:

```text
D172_V7_CHECK_PASS
terminal=R07_FULL_E4_ORBIT_PREFLIGHT_READY
toy=image=486 fibre=81 orbit=81 raw=27 exact=True load_bearing=True
fox_pairs=101/101 mutations=18
```

The genuine toy is marked nonabelian `S3`, with coordinate-permutation action
on `F3^3` and `F3^2` cocycle coordinates. Its exact identity-G fibre equals
the independently enumerated normal-orbit span (81), while the unconjugated
span is 27, so conjugation is load-bearing.

The executed mutation harness caught 18 semantic mutations, including source
pin, signed letter, layer/ordinal, E4 inverse, PB4 raw digest, seven Fox
fields, Fox transcript digest, four toy fields, and forbidden global terminal.

## v111 context-action boundary

The v111 source is pinned in the certificate (SHA
`08dd631a074329257507bafa50c813100341bfff70127655064bee940af83014`). The
receipt preserves the three literal target context bindings and:

```text
Delta = registered simultaneous context-conjugation operators on seven blocks
Lambda = F3[Delta]
A_delta((i,e)) = (i, delta_i*e)
K_z = Ann_{F3[Delta]}(z)
```

The actual diagonal image order, O3/normal-Sylow data, and return involution
action remain explicitly unknown/not reconstructed. No K_z solver or bare
`B a=z` promotion was added.

## Authorized outputs and commands

```text
search/d972_r07_full_e4_joint_orbit_preflight_v7.py
crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py
search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json
sol/luna_reply_172_r07_full_e4_orbit_preflight_repair_v7.md
```

Commands, all serial:

```text
python -B search/d972_r07_full_e4_joint_orbit_preflight_v7.py
python -B search/d972_r07_full_e4_joint_orbit_preflight_v7.py
python -B crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py
python -B crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py
```

Required claim boundaries:

v1 toy/checker promotion rejected by Sol audit

full-E4 raw bridge and canaries are bounded preflight, not a correction

positive target6 at one universal relation-module layer is not literal A18

no cofinal lift / fake / Ihara witness declared
