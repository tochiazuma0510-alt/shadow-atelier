# Luna 162 — R07 p=2/p=3 joint literal independent checker v1

Author: Luna independent checker / 2026-08-25

Status: **GHA-ready; full PB4 replay not locally executed; finite verdict
pending**.  This preparation does not claim `cross_checked`, `verified`, a
fake certificate, an Ihara witness, a named rung, or a cofinal/all-prime lift.

## 1. Versioned checker

```text
crosscheck/check_d972_r07_p23_joint_literal_v1.py
bytes  = 32201
lines  = 726
SHA256 = 56f479bbb17b0a7aa756ce79ce02dcccab5236b67ea85f90a90830f97e389bc2
```

The checker is one self-contained Python-standard-library implementation.  It
does not open or import the joint producer, its receipt, any producer helper,
any prior checker, or any repository module.  The two authoritative words and
their provenance pins are embedded, so a clean GHA checkout has no dependency
on the large untracked row artifacts.

## 2. Frozen input provenance and word construction

The embedded words were transcribed from exactly these authoritative row
artifacts:

| row | artifact | bytes | artifact SHA256 | word length | signed-list SHA256 |
|---|---|---:|---|---:|---|
| `P2R00004` / `W00004` | `search/certs/d972_row36_pent_bridge_p2_prereg_v5_20260824.json` | 114911 | `bf58d269fa587c693dd3ab9872129fdc695fe141e37d5c2582b858227bf056d9` | 40 | `eec36b318e094eedadd575e231246043de8542657b80e6ec24f9e8eb8717f91a` |
| `P3R00023` / `W00023` | `ci/row36_p3_outcome_artifacts_32675485659/d972_row36_pent_bridge_p3_prereg_v8_20260824.json` | 66337660 | `2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4` | 58 | `1af161dbc0bd96156d858867e959f305677a6ba145f7d4eb235a40fa9f12b3e4` |

Here every signed-list digest is canonical compact sorted-key JSON.  The
checker reconstructs, rather than merely accepts,

```text
d = free_reduce(w2^-1 * w3)
length(d) = 72
SHA256(d) = 2e1d84946e458a7f73ef7e18838127e5cf0d9fbb3b18138a12d28bc3ccbe172a

a = -8
a mod 2 = 0
a mod 9 = 1

w23 = free_reduce(w2 * d^-8)
length(w23) = 616
SHA256(w23) = 3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90
exponent sums (x,y) = (108,-36)
```

The exact relation-complete tuple orders `o2=2`, `o3=9` are load-bearing full
run assertions, not local results claimed by this report.

## 3. Independent finite reconstruction

The checker independently builds the following and fails on the first
disagreement.

1. For each `p=2,3`, the source quotient `F2/D4_p(F2)` and PB4 quotient
   `PB4/D4_p(PB4)` are represented inside the units of the truncated group
   algebra `F_p[G]/I^4`.  The two-sided Artin-relator ideal is row-reduced from
   scratch.  Expected filtration dimensions are `(1,2,4,8)` and
   `(1,6,25,90)`.
2. The relation-complete key is the source value followed by the five primitive
   coface values.  The six component orders of `d` are computed separately,
   their lcm must be exactly `2` and `9`, and `a=-8` is checked against these
   measured orders.
3. Both input premises are replayed: `Phi_2(w2)=1` and `Phi_3(w3)=1`.  Then
   `Phi_2(w23)=Phi_3(w23)=1` is checked directly.  This includes all ten
   individual coface identities, not only their product.
4. The printed noncommutative A.18 product is evaluated in the literal order

   ```text
   phi12_3_4^-1 * phi1_2_34^-1 * phi234 * phi1_23_4 * phi123.
   ```

5. `G36` is rebuilt as the displayed triple-dihedral marked group, and
   `PSL(2,8)` as 2-by-2 matrices over the independently implemented
   `GF(8)=F2[t]/(t^3+t+1)`.  Both `w2` and `w3`, and then `w23`, must have the
   exact common mark `([[4,0],[32,0],[0,0]],1)`; `w23` must be the identity in
   both source groups `Q2,Q3`.
6. The checker directly evaluates the typed words

   ```text
   theta(w23) * w23,
   w23 * tau(w23) * tau^2(w23),
   theta: x->y, y->x,
   tau:   x->y, y->x^-1*y^-1,
   ```

   in `G36`, `PSL(2,8)`, `Q2`, and `Q3`.
7. Charming is checked both by the authoritative mod-36 exponent criterion and
   by direct membership in the rebuilt component derived subgroups.  Their
   required orders are `1458,504,8,27`.
8. At `m=0`, the marked endomorphism images are `x` and
   `w23*y*w23^-1`.  Direct generated factor orders must be
   `G36=23328`, `PSL(2,8)=504`, `Q2=128`, `Q3=2187`.

The JSON result records the full signed `d` and `w23`, all six component-order
lists for both primes, every gate, relation-word digests, factor orders,
independence scope, and a canonical self-digest.

## 4. GHA invocation and markers

No workflow file or queue plan was changed in this lane.  A broker-supplied
GHA Python job can run:

```text
python -B crosscheck/check_d972_r07_p23_joint_literal_v1.py --out-dir ci/out
```

It writes:

```text
ci/out/d972_r07_p23_joint_literal_checker_v1.json
```

A 90-minute timeout is conservative; no third-party package is required.
Expected success markers, in order, are:

```text
R07_P23_WORD_PASS
R07_P23_FIREWALL_PASS
R07_P23_JENNINGS_PASS
R07_P23_INPUT_KEYS_PASS
R07_P23_CRT_PASS order2=2 order3=9 a=-8
R07_P23_COFACES_A18_PASS cofaces=10
R07_P23_MARK_PASS
R07_P23_HEXAGONS_PASS
R07_P23_CHARMING_PASS
R07_P23_ONTO_PASS G36=23328 PSL2_8=504 Q2=128 Q3=2187
R07_P23_RESULT
R07_P23_JOINT_CHECKER_FINAL status=PASS
```

Any exception emits the same terminal prefix with `status=FAIL` and exits
nonzero.  GHA acceptance must require exit code zero, exactly one PASS final
marker, no FAIL final marker, and the uploaded JSON artifact.

## 5. Local quick preflight only

The permitted lightweight checks completed with exit code zero:

```text
python -B crosscheck/check_d972_r07_p23_joint_literal_v1.py --selftest
R07_P23_JOINT_CHECKER_SELFTEST status=PASS d_length=72 a=-8 w23_length=616

AST_PARSE_PASS
QUICK_COARSE_PASS True True 23328 504
QUICK_SOURCE_PASS [(2, True, 2), (3, True, 9)]
```

`QUICK_SOURCE_PASS` covers only the source components of the relation key; it
must not be confused with the full six-component orders.  The six-generator
PB4 algebras, all ten cofaces, literal A.18, full hexagons, charming, and onto
replay were intentionally left to GHA.  The finite verdict therefore remains
pending.
