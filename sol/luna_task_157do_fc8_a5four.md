# Luna task 157do — FC-8* concrete `A5^4` chief factor immediately below the frozen B4 roof

## 0. Role and scope

You are Luna. Implement one bounded, exact, cross-checked finite certificate. Do not claim B4-B and do not call this the canonical/unique "first" nonabelian chief factor.

Authorized new files only:

1. `search/d972_b4_fc8_a5four_v1.g`
2. `search/check_d972_b4_fc8_a5four_v1.py`
3. `search/d972_b4_fc8_a5four_gha_driver_v1.g`
4. `sol/luna_reply_157do_fc8_a5four.md`

No workflow edit, no git/GHA action, no local GAP, and no heavy local Python. One lightweight checker selftest is allowed. Reuse frozen sources by SHA pin; do not copy an unauthenticated receipt value.

## 1. Mathematical target

Let `rho0: PB4 -> Q0=P^4 x H9` be the frozen actual coarse B4 roof map and `M=ker(rho0)`. Let `a:F2 -> A5` use the canonical A5 marking from `certificates/A1.v2.2.json` / A5-CONV:

```text
X=(1,3,2,4,5), Y=(1,3,4,5,2).
```

For the four strand deletions `d_i:PB4->PB3`, compose the free quotient `PB3 -> F2 -> A5` and form

```text
rhoA=(a d_1,...,a d_4): PB4 -> A5^4.
```

The positive target is to prove, with literal marked words:

1. `im(rhoA)=A5^4`;
2. `ker(rhoA)` is B4-normal and the B4 action permutes the four simple direct factors transitively through the standard S4 strand action;
3. `Q0` has no nontrivial A5 quotient (use the frozen `Q0=P^4 x H9`, `P=PSL(2,8)` of order 504 and solvable H9/order data; in particular `5` does not divide `|Q0|`), hence the joint PB4 image in `Q0 x A5^4` is the full direct product by Goursat;
4. for `K=M intersection ker(rhoA)`, restriction gives `M/K ~= A5^4`;
5. every B4-normal subgroup of `A5^4` is a product of a B4-stable subset of the four simple factors; coordinate transitivity leaves only `1,A5^4`. Hence `M/K` is a B4-chief factor with `S=A5,t=4`.

This closes the **registered concrete FC-8*** question. It does not prove that every possible first nonabelian factor has `t=4`, and it deliberately shows that T-39 CB-2's `t=1` branch does not apply to this natural factor.

## 2. Producer requirements

- Pin and load the smallest frozen source that gives the exact four deletion PB3 words/rows and the actual `Q0=P^4 x H9` order/type contract. Pin the canonical A5 marking source/certificate.
- Reconstruct A5 as a concrete permutation group; assert order 60, simplicity/perfectness using exact GAP predicates or an explicit normal-closure certificate.
- Evaluate all six canonical PB4 pure generators in all four A5 coordinates from the deletion words. Replay the PB4 presentation relations.
- Prove `A5^4` without enumerating its 12,960,000 elements. Preferred certificate: four literal single-support words/elements, each nontrivial in exactly one coordinate, whose normal closure in that A5 coordinate has order 60, plus full coordinate projections. Record signed source words and all four coordinate images losslessly.
- Reconstruct the three Artin/B4 generator actions on the six PB4 rows. Verify braid/commutation relations, exact transport of all six rows, and induced factor permutation equal to a transitive S4 action. No inference from labels alone.
- Bind `rho0` and `rhoA` as maps from the same six marked PB4 generators. Record the direct-product/Goursat proof premises, not only orders.
- Emit exact source hashes, marking, deletion table, support words/images, B4 action table, factor orders, prime-support/no-common-quotient receipt, and the definition of `K`.
- Terminal token only after every gate:

```text
FC8_A5_FOUR_CHIEF_CROSSCHECKED
```

On an unmet premise emit a precise `FC8_UNKNOWN_*`; never relabel a partial result.

## 3. Independent checker

Do not import producer helpers.

- Independently build A5 from the two permutations and independently evaluate signed PB4 words/deletion rows.
- Recheck PB4 relations, four coordinate projections, every single-support image, and normal-closure order 60.
- Independently replay the B4/Artin action and transitivity.
- Independently validate the frozen Q0 factor data and the no-common-nontrivial-quotient argument. Do not accept `direct_product=true` from JSON.
- Reconstruct the chief conclusion from `normal subgroups of S^4 are products of factors` plus transitivity; record this lemma's finite premises explicitly.
- Mutation tests must reject: one deletion letter, swapped coordinate, one support image, one Artin transport, P order/type, H9 solvability/order/prime support, `t`, and terminal relabel.

## 4. Performance

- No `Elements(A5^4)`, Cayley table of `A5^4`, or generic `Size(Group(tuple_generators))` if the structural certificate already proves equality.
- Cache fixed word evaluations. All closures occur only inside one A5 factor (order 60) or the already-frozen small action groups.
- The intended GHA runtime is minutes, not hours. Include source-only runtime estimate and heavy-operation count in the reply.

## 5. Reply

Report exact SHA256/bytes for all three code files, static/selftest results, the exact mathematical implication, and remaining boundary: isolation of `K` and OBS-NA/D1/NA-5 are not supplied by this FC-8 certificate.
