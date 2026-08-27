# Luna task 186 — R07 normalized exact-common-word column generation v2

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP, git,
or GHA locally.  Preserve the currently running task179 v1 files byte for
byte.  Create a versioned v2 successor; parent Sol alone will audit, commit,
push, and launch GHA.

## 1. Governing theorem and exact correction

Read these two papers in full and pin their exact bytes/SHA-256:

```text
sol/proof_r07_task179_exact_exponent_lattice_v156.md
sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md
```

The authenticated 6,441-word task179 roster normally generates
`Omega=ker(F(x,y)->G_joint)`, and v156 proves

```text
exp(Omega) = 18 Z^2.
```

Therefore task179 v1's rows `exp(word) mod 3` are identically zero and must
not be copied.  The exact first-edge charming quotient is

```text
nu(word) = (exp_x(word)/18, exp_y(word)/18) mod 3.
```

Integer divisibility by 18 is an integrity condition checked before every
division.  Conjugation does not change the exponent.  Boundary columns and
the target have zero `nu` tail.

## 2. Versioned implementation

Create only:

```text
search/d972_r07_normalized_exact_common_word_colgen_v2.py
crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py
search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g
search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json
sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md
```

Start from the current live task179 producer/checker/driver only after
authenticating their exact bytes and SHA-256.  Discover and record the live
identities rather than trusting an old mail pin.  Copy the full positive-only
resumable schedule, word provenance, direct replays, resource honesty, and
fail-closed terminals.  Do not import the withdrawn task184 implementation.

Rebuild the retained echelon from rank zero with the two normalized rows.
An old task179 checkpoint may be used only after authenticating its complete
column provenance and reconstructing every column in the enlarged space;
discard its pivots, reduced target, dual, and oracle cursor state.  A fresh
production run is the default.

## 3. Positive receipt and closed exactification

On augmented membership, independently materialize the ordinary correction
word `c_star` and compute its exact integer exponent.  The normalized zero
tail must imply

```text
exp(c_star) = (54 A, 54 B)
```

for integers `A,B`.  Use the fixed registered Q0-defect words `r_3,r_9,r_12`
of v156 and form, with literal word multiplication and free reduction,

```text
v0 = r_9 r_12 r_3^-2       exp(v0)=(0,18)
u0 = r_9 v0^-8             exp(u0)=(18,0)
h  = u0^(-3A) v0^(-3B)
c_exact = c_star h.
```

Retain the exact roster ordinals, source-word definitions, unreduced and
reduced signed words, integer exponents, and digests.  Recompute rather than
assert:

1. every `r_i`, `u0`, and `v0` lies in the registered joint kernel;
2. the normalized augmented sparse target equality;
3. the tail has zero first-Frattini/all-seven change;
4. `exp(c_exact)=(0,0)` over the integers;
5. the corrected word uses right multiplication from the frozen g760 base;
6. both hexagons and the five-factor printed-order pentagon;
7. every marked/reduction/side gate already required by task179; and
8. no PB3/PB4 boundary chain entered the source correction word.

If a coefficient solution somehow fails the 54-divisibility implication,
hard-stop as an integrity failure.  Never weaken the target to raw exponent
modulo three.

## 4. Independent checker

The checker must not import either producer.  It may use pinned arithmetic
sources only behind the existing helper firewall.  It must independently:

1. reconstruct all 6,441 literal roster words and exact exponent pairs;
2. reproduce the complete 16-vector set and prove the two inclusions giving
   `exp(Omega)=18 Z^2` from the registered rows;
3. rebuild every normalized correction column and every boundary zero tail;
4. replay every retained rank transition, target reduction, dual pairing,
   coefficient recovery, and source-word materialization;
5. reconstruct `r_3,r_9,r_12,u0,v0,h,c_exact` independently; and
6. recompute every positive replay listed in Section 3.

For `UNKNOWN_RESOURCE`, authenticate a complete resumable v2 checkpoint and
absence of any negative, fake, cofinal, or Ihara claim.  Programming errors
are hard nonzero failures, not typed UNKNOWN.

## 5. SELFTEST and destructive controls

Use a noncommutative toy whose kernel exponent lattice is exactly a proper
rank-two sublattice, so raw exponent mod 3 is vacuous while normalized rows
are nonzero.  Exercise the real production column, checkpoint-rebuild,
coefficient, basis-word, cube-tail, and direct-replay paths.

At minimum reject mutations of: divisor 18; one exponent sign; one roster
ordinal; conjugator exponent incorrectly added; a boundary nonzero tail;
raw-mod-3 substitution; target tail; old-pivot reuse; coefficient 2 treated
as repetition rather than inverse; 54-divisibility; `u0` formula; `v0`
formula; cube exponent; right-correction order; pentagon order; one hexagon;
one source word; and a boundary word inserted into the correction.

## 6. Driver terminals and reply

Allowed PRODUCTION terminals are exactly:

```text
R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD
UNKNOWN_RESOURCE:<registered phase and cap>
UNKNOWN_INPUT:<authenticated missing or malformed input>
```

Require exactly one producer terminal and its matching independent-checker
terminal before writing `.ok`.  Always upload the latest checkpoint on a
resource stop.  The reply must process Sections 1--6 in order, list exact
file identities, and end with:

```text
NORMALIZED FIRST-EDGE COMMON WORD:          NOT EXECUTED BY LUNA
EXACT-COMMUTATOR FIRST-EDGE WORD:           NOT EXECUTED BY LUNA
COMPATIBLE COFINAL LIFT:                    NOT DECLARED
FAKE / IHARA WITNESS:                       NOT DECLARED
```
