# Luna reply 157bl — synchronized Burau/CRT obstruction

## Verdict

The bounded v1 bundle is ready for parent review and GHA.  No local GAP, Git,
push, or GHA execution was performed.  The producer emits only a finite
candidate or UNKNOWN result; it does not label A/B.

Authorized files written:

- `search/d972_b4_burau_joint_v1.py`
- `search/check_d972_b4_burau_joint_v1.py`
- `.github/workflows/d972-burau-joint-v1.yml`
- this reply

## Synchronized image and configurations

The image is built once from the same source pair `(x,y)` and the same signed
word in every row.  A tuple is

```text
(one roof permutation,
  q3a2:base/theta/tau/tau2 × five A.18 blocks,
  q4a2:base/theta/tau/tau2 × five A.18 blocks,
  ...)
```

The public `q3a2` lane is `(q=3,a=-1)`, matching v4; `q4a2` is `(4,2)`,
and the q5 lanes are `(5,2)` and `(5,4)`.  The registered matrix includes the
two single-specialization full-constraint lanes, followed by the three
required synchronized lanes:

```text
q3a2_full
q4a2_full
q3a2_q4a2
q3a2_q4a2_q5a2
q3a2_q4a2_q5a4
```

The fixed order is `x12,x13,x14,x23,x24,x34`, then the literal A.18 order
`123,234,12,3,4,1,23,4,1,2,34`.  The transform order is
`base,theta,tau,tau2`.  The receipt binds the field signatures, full block
order and its digest, configuration digest, source SHA, and all frozen 972
artifact hashes.

No Cartesian product of single-lane fibers is formed.  `H'_S` is obtained by
the exact normal closure of the joint commutator, its projection is required
to have order `367416`, and the complete kernel is enumerated from the joint
Schreier relators.  Every row uses the exact right fiber `h0*K_S`; lossless
kernel elements/generators, `h0`, fiber digest, and row-level witnesses are
serialized.

The roof gates retained from v4 are

```text
|P|  = 1469664
|P'| = 367416
single q3a2/q4a2 reference: |H|=105815808, |H'|=2939328, |K|=8
```

The last three values are recorded as learned single-lane reference gates,
not assumed to be the order of a synchronized image.  Joint order values are
computed exactly by the run and checked independently.

## Hexagon strengthening and CRT gate

For every specialization and every A.18 block, the tuple also carries the
images of the same source element under `theta`, `tau`, and `tau²`:

```text
theta(x)=y, theta(y)=x
tau(x)=y, tau(y)=inverse(PaperProd(x,y))
tau² = tau applied again to the preceding pair
```

`PaperProd` is the repository convention (displayed factors are reversed in
native multiplication).  The producer retains the pentagon-only count, and
also records `full_GT_identity_count`, which requires H10, H11, and the
five-block pentagon defect to be identity simultaneously in every
specialization.

The roof stores only `m mod 18`, so the producer never plugs the displayed
representative into H11 blindly.  For each row it computes the exact order of
the synchronized `y`, sets

```text
L = lcm(18, ord(y))
```

and records every residue `m~ in [0,L)` with `m~=m (mod 18)`, followed by the
necessary profinite-unit gate `gcd(2*m~+1,L)=1`.  For joint lanes the H11
witness residue set is intersected across all specializations, so one
profinite `m~` is used rather than independent residues.  The full CRT list,
unit list, modulus, congruence, and counts are stored per row.  A candidate is
reported only when a row has zero full-constraint elements; all-pass is
`UNKNOWN_BURAU_JOINT_ALLPASS`.

The producer and checker include negative fixtures for unsynchronized
Cartesian acceptance, kernel deletion, configuration/field swap, product
orientation, source word/key and `h0` mutation, A.18 defect mutation, and an
omitted-H10/hexagon mutation that leaves the pentagon blocks unchanged.

## Independent checker and workflow

The checker is standalone: it does not import the producer or v4 helpers.  It
rebuilds the roof, all fields, Burau/A.18 maps, theta/tau maps, joint closure,
Schreier kernel, CRT residues, right fibers, and all pentagon/hexagon counts.
It rejects `UNKNOWN_RESOURCE` receipts, truncated rows, aggregate-only
receipts, kernel/generator deletion, altered source/key/config/order, and
fiber/count/witness drift.

The workflow has five independent matrix jobs, read-only checkout credentials,
Python 3.13.5, hash-pinned SymPy 1.14.0/mpmath 1.3.0, a 12,000,000-KiB
virtual-memory limit, a 360-minute limit, exact one-line terminal-marker
cardinality, and `always()` evidence upload.  It checks the receipt with the
independent checker on every complete candidate/all-pass result and has no
`workflow_dispatch` entry.

## Static and lightweight evidence

Executed locally without GAP/Git/GHA:

```text
python -B -m py_compile search/d972_b4_burau_joint_v1.py search/check_d972_b4_burau_joint_v1.py
python -B search/d972_b4_burau_joint_v1.py --self-test
python -B search/check_d972_b4_burau_joint_v1.py --self-test
```

Observed:

```text
D972_B4_BURAU_JOINT_V1_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_JOINT_V1_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V1_SELFTEST_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_SELFTEST_PASS
D972_B4_BURAU_JOINT_V1_CHECKER_FINAL_MARKER status=PASS
YAML_PARSE_PASS ['joint'] ['q3a2_full', 'q4a2_full', 'q3a2_q4a2', 'q3a2_q4a2_q5a2', 'q3a2_q4a2_q5a4']
JOINT_WORKFLOW_STATIC_PASS
JOINT_CHECKER_STATIC_PASS
```

No full joint closure was run locally.  The exact joint order, kernel size,
row counts, and candidate/UNKNOWN outcome are therefore intentionally left to
GHA; memory/time exhaustion is fail-closed as `UNKNOWN_RESOURCE`.

The previously recovered q3/q4 v4 receipts were inspected only as reference.
They serialize matrix values but do not carry the common Schreier source-word
labels needed to prove an abstract cross-lane `C2^3` identification.  No raw
matrix-value identification was used in this bundle; the new joint closure
reconstructs the synchronized labels directly.

## SHA-256

```text
search/d972_b4_burau_joint_v1.py          6F8D66FB259FECD016CE6ECFAABA215BB14099DFA4C2710CAF6C8E7A94C8A4BA
search/check_d972_b4_burau_joint_v1.py    C0AF3054D16BCCD173D539B6D32E492C8CF1B00DCF1909BFD59778ECAC9D8C77
.github/workflows/d972-burau-joint-v1.yml 751DABDF330BF4E37B4DA2281E91E2991B10D8D9F74B60F79D5FACB72D1E7192
```

JOINT_BURAU_CRT_READY_FOR_GHA
