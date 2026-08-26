# Luna task 170: PB4 presentation equality Artin audit v1

Date: 2026-08-27  
Role: Luna / bounded mechanical producer + independent checker  
Evidence grade: `CROSSCHECKED` (not Lean-verified)

## Result

```text
PB4_ARTIN_IDENTITY_CROSSCHECKED
11 frozen PB4 relators, 44 Artin images: all literal identities
```

For every frozen pure relation, the standard PB4 marking was expanded through
the six `A_ij` braid words and evaluated on all four free generators.  Every
image was exactly `[1]`, `[2]`, `[3]`, `[4]`.  The independent checker repeated
the relation reconstruction and all 44 image checks without importing the
producer or its helper functions.

## Inputs and implementation pins

| input | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_q3_chief_v1.g` | 76867 | `b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755` |
| `search/certs/koubou158_completeness_v3.3_20260822.json` | 46439 | `98cf541edf17e6950ea53b9d44bd57536b43b89101dc7d89b70b197a04e4c80b` |
| `search/d972_pb4_artin_presentation_equality_v1.py` | 5408 | `9db37e225deb4ff6c1864969b5bdaf7632ecbe39d729e1cafac11ac8fba86716` |
| `crosscheck/check_d972_pb4_artin_presentation_equality_v1.py` | 2870 | `a850ad08a5f3dc5081abf754b765982eec1f2ac6c12f36f7d1e7735e94b189a3` |
| `search/certs/d972_pb4_artin_presentation_equality_v1_20260827.json` | 4909 | `40494583a32894a6028bb5b421b5f228d4dc110050d8096032af8bcdbed727a0` |

The C-12 completeness input is pinned as a historical input only; its former
D2 statement remains unclaimed.

## Conventions and checks

The ordered pure generators are

```text
(a12,a13,a14,a23,a24,a34)
```

with lexicographic `(i,j)` order.  The standard words are

```text
A_ij = sigma_(j-1) ... sigma_(i+1) sigma_i^2
       sigma_(i+1)^-1 ... sigma_(j-1)^-1.
```

Artin uses

```text
sigma_i: t_i -> t_i*t_(i+1)*t_i^-1,
         t_(i+1) -> t_i,
```

with other free generators fixed.  Signed braid words are composed
left-to-right by substitution; free-word inverses reverse order and negate.
The six `A_ij` induced strand permutations are all identity.  Both adjacent
braid relations and the distant commutation relation were checked before the
PB4 relators.

The producer serialized each of the 11 pure relations, its expanded braid-word
length and SHA, and its complete 4-image row.  The checker independently
reconstructed the same 11 relations and compared only these public values and
direct identity facts.

## Mutation coverage

The producer registered and exercised all required categories:

```text
relator row mutations (11/11 destructive direct nonidentity)
A_ij conjugating-tail sign                REJECT
braid multiplication/order mutation       REJECT
forward/inverse Artin mutation             REJECT
free-word inverse-order mutation           REJECT
q3 source pin drift                         REJECT
q3 relator-order mutation                   REJECT
one of 44 output images                     REJECT
false VERIFIED terminal token               REJECT
```

The checker independently exercised the 11 row mutations and an alternative
order convention canary; its terminal output was:

```text
PB4_ARTIN_CHECKER_PASS
relators=11 images=44 all_identity=true
alternative_order_canary_reject=true mutation_rows=11/11
q3_pin=true c12_pin=true
```

## Commands and scope

Executed serially from the repository root:

```powershell
python -u search/d972_pb4_artin_presentation_equality_v1.py
python -u crosscheck/check_d972_pb4_artin_presentation_equality_v1.py
```

No full g760/Jennings run, ANUPQ construction, GAP, GHA, workflow change,
git operation, or credential access was used.  Scratch was confined to TEMP.

machine result: 11 frozen relators are identity under the Artin action
faithfulness is a literature theorem, not established by this checker
combined D1+D2 presentation equality requires Sol's paper inference
no literal A18 / cofinal lift / fake / Ihara witness declared
