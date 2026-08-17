# Luna reply 157bo - joint Burau hexagon soundness audit

## Verdict and scope

The direct finite-obstruction implication is sound for the synchronized
finite image constructed by the frozen bundle.  A row with
`full_GT_identity_count = 0` excludes every genuine profinite lift whose
roof image is that row, provided the separate semantic identification of the
roof with the intended D972 quotient is accepted.  This audit does not turn
that conditional statement into B4-A/B: the 972/324/index-3 and named-roof
premises remain the separate task 157bn gate.

No local GAP, Git, push, GHA, or heavy producer run was used.  Only the two
lightweight Python selftests, compilation, and static workflow checks were
run.

## 1. Page-image audit and conventions

The PDF
`papers/2401.06870-gt-shadows-gentle-version.pdf` (SHA-256
`4e0a29e19825810eb9db24ebda120a6805c42fee4eb51679d409c5437e0943ab`)
was rendered and checked as page images:

- PDF page 5, printed page 5, displays (1.14) and (1.15) exactly as
  `theta(x)=y`, `theta(y)=x`, and
  `tau(x)=y`, `tau(y)=y^(-1) x^(-1)`.
- PDF page 12, printed page 12, Proposition 3.4 displays
  `f theta(f) in N_F2` and
  `tau^2(y^m f) tau(y^m f) y^m f in N_F2` as (3.10) and (3.11),
  and states the equivalence with the two hexagons for
  `f in [F2,F2]`.

The A.18 image was also checked in the cited original
`papers/2008.00066-what-are-gt-shadows.pdf`, PDF/printed page 49 (SHA-256
`c44eba890f83c1ac84a44a5b52fd5c6849250b242331d7eaaff9dd983167fb33`).
It gives, in order,

```text
123       (x12,              x23)
234       (x23,              x34)
12,3,4    (x13*x23,          x34)
1,23,4    (x12*x13,          x24*x34)
1,2,34   (x12,              x23*x24).
```

The repository `PaperProd` convention is displayed-factor order: native
matrix/permutation multiplication reverses the displayed list.  The
producer's `paper_prod` and `matrix_paper_prod` implement that convention
(producer lines 142-148 and 371-375), and the checker has independent copies
(checker lines 133-139 and 354-358).  Thus the image-level formula for the
pentagon defect is

```text
(b5*b3)^(-1) * b2 * b4 * b1,
```

where the `b_i` are the five A.18 blocks above.  This is the identity form
of the paper's pentagon, not a reverse-rho or raw-158 norm.

## 2. One synchronized source and the complete F2' fiber

For a registered list of specializations S, let `Psi_S` be the map from the
same free group `F2=<x,y>` to the tuple group whose two generators are
constructed by `make_joint_gens` (producer lines 491-500).  Each component is
obtained from the same x/y pair by the same A.18 assignment and one of the
four transformations.  `eval_joint_word` (lines 503-511) applies one signed
source word to the two joint generators, not one word per lane.  Therefore

```text
Psi_S(w) = (roof(w), all A.18/Burau/theta/tau/tau2 images of w)
```

for one common source word w.  The direct product in the codomain is only an
ambient representation; the image is the synchronized diagonal image, not a
Cartesian product of single-lane images.

Write `H=im(Psi_S)`.  Since Psi_S is onto H,

```text
Psi_S(F2') = [H,H] = H'.
```

The producer starts with the joint commutator and closes its conjugates by
both joint generators and their inverses (lines 596-625).  At each round it
computes the complete projected section (lines 520-533), all Schreier kernel
relators (536-547), and an uncapped finite closure of those relators
(553-567).  It refuses to continue unless the projection has the exact
advertised order `367416` (616-625).  This is a finite normal-closure and
Schreier computation, not a bounded word sample.

For a row roof element p in the projected derived image, the stored section
element `h0` is the exact section representative over p (producer lines
820-827).  With `K_S=ker(H' -> P')`, the enumerated set

```text
h0 * K_S
```

is exactly the right fiber over p: every element has roof p, and if h has
roof p then `h0^(-1)h` is in K_S.  The receipt stores every kernel element,
the section representative, the sorted fiber, and its digest.  The checker
rebuilds this argument independently at lines 692-756 and rejects a missing
kernel element, altered h0, or altered fiber digest.

The frozen word is used to replay and bind the roof key, not to restrict the
matrix fiber to that word.  This is correct: the finite image of the closed
commutator subgroup is H', so a genuine profinite f in the commutator closure
must lie somewhere in the complete `h0*K_S` fiber.  The nonzero free
abelianizations of many parent-chain representatives are therefore not a
counterexample; they are representatives of finite derived-image elements,
and the row scan uses the full H' fiber rather than trusting those words.

This establishes completeness inside the constructed synchronized finite
image.  It does not by itself prove that the hard-coded semantic label
`M=K^(9) intersect N_S4` is the abstract PB3/M quotient; that is the
separate semantic premise explicitly excluded from this audit.

## 3. The m/CRT gate

For a genuine lift, the profinite m has the roof congruence
`m~=m (mod 18)`.  In a finite tuple image, every occurrence of m in H11 is
periodic modulo the order of the joint y element.  The producer computes that
order exactly by taking the lcm of the roof and every matrix block
(lines 671-704), then sets

```text
L = lcm(18, ord(Psi_S(y))).
```

`m_compatibility` enumerates every residue in `[0,L)` congruent to the row
residue modulo 18 and retains only
`gcd(2*m+1,L)=1` (lines 723-744).  This is a necessary condition for a
profinite unit `lambda=2*m+1`: a profinite unit is a unit modulo every finite
quotient, hence modulo L.  It is intentionally only a necessary finite gate;
it never creates a false exclusion by claiming sufficiency.

The interval representative handles negative source representatives because
the congruence is reduced modulo 18 and then enumerated modulo L.  Since L
contains the full finite orders, including all prime-power factors, no
prime-power or sign case is omitted.  `hexagon_status` intersects the valid
residue sets across all specializations (lines 770-789), so one common m is
used for the synchronized tuple; it does not silently choose independent
m's for separate lanes.

## 4. Pentagon, transforms, independence, and fail-closed behavior

The producer's `a18_pairs` (403-409) matches the page-49 A.18 table.  The six
pure Burau generators are formed from the three braid generators in the
standard order

```text
x12=s1^2, x13=s2*x12*s2^-1, x14=s3*s2*x12*s2^-1*s3^-1,
x23=s2^2, x24=s3*x23*s3^-1, x34=s3^2.
```

The code's PaperProd reversal makes these displayed products the intended
native matrix products.  The selftest checks invertibility, both braid
relations, and the distant commutation relation for every registered field
lane.  `transformed_pair` applies theta, tau, and tau again recursively
(producer lines 412-431), so tau2 is not an unproved shortcut.  Block order is
specialization, then `base/theta/tau/tau2`, then the five A.18 blocks; both
`_transform_slice` and `tslice` use exactly that order.

For every fiber element, H10, H11 with the common m residue, and all five
pentagon blocks are required simultaneously (producer lines 820-874).  A
zero `full_GT_identity_count` therefore means that every element fails at
least one necessary genuine-GT condition.  In particular, requiring the
hexagons in addition to the pentagon cannot turn a genuine lift into a false
negative: every genuine lift satisfies all of them.

The checker does not import the producer or any v4 helper.  It independently
rebuilds the fields, Burau matrices, A.18 maps, transformations, joint
closure, Schreier kernel, CRT list, fibers, and row counts (checker lines
1-6, 386-434, 497-648, and 665-815).  It binds the producer source hash but
does not execute producer code.

The workflow is fail-closed: it uses a read-only checkout, pinned Python
dependencies, a 12,000,000-KiB virtual-memory limit, and a 360-minute limit
(workflow lines 30-51).  Producer resource/error status is rejected
(52-76); the receipt must have exactly 972 ordered unique rows and a positive
fiber size (77-95); exactly one candidate/all-pass final marker is required
(97-101); and the independent checker must exit successfully and print its
PASS marker (102-108).  Evidence upload is under `always()` (109-115).
Thus timeout/resource/partial output cannot be promoted to either a zero
fiber or all-pass result.

## Lightweight evidence and hashes

Observed locally:

```text
python -B -m py_compile search/d972_b4_burau_joint_v1.py search/check_d972_b4_burau_joint_v1.py
  PASS
python -B search/d972_b4_burau_joint_v1.py --self-test
  D972_B4_BURAU_JOINT_V1_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
  D972_B4_BURAU_JOINT_V1_NEGATIVE_FIXTURES_PASS
  D972_B4_BURAU_JOINT_V1_SELFTEST_PASS
python -B search/check_d972_b4_burau_joint_v1.py --self-test
  D972_B4_BURAU_JOINT_V1_CHECKER_NEGATIVE_FIXTURES_PASS
  D972_B4_BURAU_JOINT_V1_CHECKER_SELFTEST_PASS
  D972_B4_BURAU_JOINT_V1_CHECKER_FINAL_MARKER status=PASS
workflow YAML/static contract
  JOINT_WORKFLOW_YAML_STATIC_PASS ['joint']
```

Frozen input and implementation hashes:

```text
search/d972_b4_burau_joint_v1.py
ae87ea25c6cea8da7f0145f433e94b4fcb1e17709c3a5c1f7f2b449358faee15

search/check_d972_b4_burau_joint_v1.py
ad31d32af1b67298b4ad1a3dcedf8770568ec2c5b48a3df73b454c2b93989cf7

.github/workflows/d972-burau-joint-v1.yml
751dabdf330bf4e37b4da2281e91e2991b10d8d9f74b60f79d5facb72d1e7192

search/certs/d972_b4_word_key_artifact_v1_20260816.json
564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
```

The direct implication is therefore valid at the finite-image level: a
complete zero row contradicts the finite image of any genuine profinite
lift.  No B4-A/B terminal claim is made here.

JOINT_HEXAGON_SOUNDNESS_PASS
