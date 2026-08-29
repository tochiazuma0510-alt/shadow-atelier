# R07 canonical residual generators, run 33263377923 (v363)

Author: Sol / 2026-08-30

Status: physical producer plus independent-checker audit of the bounded v360
construction.  The two canonical values generating
`R_S(Delta0)=tilde-S` are cross-checked and have lossless literal-word
representatives.  The enclosing task382 terminal is intentionally
`UNKNOWN_INPUT` because no positive A4 `K`/action owner was supplied; hence
`C_rel`, a compatible lift, a fake and an Ihara witness are not claimed.
This is not Lean verification.  `verified=false`.

## 1. Immutable run and artifacts

Task382 ran through `gap-run.yml` as:

```text
run id:       33263377923
head:         527dcab5c371316fccb17046e33d9136bfce35bd
artifact id:  9717909682
artifact:     gap-run-out
zip bytes:    8838
zip digest:   sha256:ce57749e7e00d067ea874bf10ae7f7316bfaf0e8385cb8cf285a627faf19ae69
```

The mathematical payloads are:

```text
producer receipt:
  bytes  17923
  SHA256 3b83126efe64e83bb149a82d58094e2784ada0684bbf733e25ca60a65a245cda

independent verdict:
  bytes  5496
  SHA256 4038626a4e8b98460f2d392f845ca85df94ad6dfc036416e611907cfc4e13fe9
```

Both JSON objects are canonical and their internal self-digests replay.
The producer and checker terminal files are identical 14-byte
`UNKNOWN_INPUT` tokens.  The producer reason and independently accepted
checker reason are both exactly

```text
UNKNOWN_INPUT:A4_POSITIVE_AMBIENT_K_NOT_AVAILABLE
```

Thus workflow success is not being read as a positive A4 terminal.  The
cross-checked subclaim below is explicitly retained inside that typed
missing-A4 result.

## 2. Lossless compact words

Let `w_i` denote the freely reduced source word for one-based task176
`Gamma` state `i`, reconstructed from the pinned parent-state/parent-record
recurrence and its 26 literal record words.  Let `p_1,p_2` be the first two
pinned task157ee split words, i.e. the two pure-`PSL(2,8)` quotient words.

The producer's preliminary inner representative for each split generator is
state 4.  The unique passing central corrections are states 114 and 172.
Consequently its explicit representatives are

\[
 \boxed{
 s_1=\operatorname{red}(w_{114}w_4^{-1}p_1),
 \qquad
 s_2=\operatorname{red}(w_{172}w_4^{-1}p_2).}
\tag{2.1}
\]

The frozen recurrence gives:

| word | reduced length | canonical-list SHA-256 |
|---|---:|---|
| `w_4` | 146 | `92a51dce182e430f67e26eeef26e34577664c5a8aba6b2ae1f0e193a6a339043` |
| `w_114` | 372 | `6d9504cff2850084146639b1058635d84bb33c5f9b05d6a641c813dba4a70755` |
| `w_172` | 204 | `551882f7d02a1a01012da54274bd56b42c94c264e4c972fa389a0f1b40ed6a4b` |
| `s_1` | 538 | `ac1c47a75b8327c89aca45e4ebd1782b89cedd4cafec2b60bba6ecd647e920d4` |
| `s_2` | 328 | `eb49b2897dec1ad014789da1f232ae9f0bce3ff05d867339ff3b0aba2e3e7ea4` |

Here the digest is SHA-256 of the canonical JSON integer list.  Directly
reconstructing (2.1) from the pinned parent recurrence reproduces both full
word arrays in the producer receipt byte for byte.

The elements represented by (2.1) are canonical values in the actual roof
group.  Their free-word spellings are explicit but not asserted unique: the
independent checker deliberately starts from a different preliminary inner
representative and compares the final ten-coordinate values rather than
requiring the same spelling.

## 3. Cross-checked group gates

Producer and checker independently establish all of the following:

1. the task176 `Gamma` owner contains exactly 243 distinct states and its
   lossless word recurrence replays;
2. each pure-`S` split word has exactly 27 inner-action corrections after a
   complete 243-state scan;
3. `Z(Gamma)` consists of exactly 27 states, with full-state centrality
   replay;
4. all `27^2=729` central pairs are tested against the five pinned complete
   `PSL(2,8)` relators, and exactly one pair passes;
5. the selected values centralize `Gamma`, generate a subgroup of order 504,
   and meet `Gamma` in the identity only; and
6. their `Q0` projections are the two fixed pure-`PSL(2,8)` generators.

The relevant physical pins are:

```text
Gamma table raw SHA256:
  c890e99f66e2987c3ff658dc00ba4ddab24a1d83556767b9cd4bfcd6b60d191d
Gamma parent recurrence SHA256:
  b57f3bf3bd362beb3e3e959bbe0a23efea36afc6ce52c33ccc13e5922f6fff37
five PSL relators SHA256:
  85329c1f9d34eb2e0e8ed00944f023ba1eb67cb6e7775e29d20e8a9bfa7bd3ba
final Q0 projection SHA256:
  c9bfa685583c725c3d8e14e7706a7c7a50e8604baf77edcf6efe1a72110e5d48
```

The checker uses reverse state/central-pair order, a different preliminary
inner representative, a separate word evaluator and its own subgroup
closure.  It reports `accepted=true`, `independent=true`, and
`word_values_independently_replayed=true` for this subclaim.

It follows that the values of (2.1) generate the unique complement

\[
 \boxed{\langle s_1,s_2\rangle=\widetilde S=R_S(\Delta_0)
        \cong PSL(2,8).}
\tag{3.1}
\]

This is the physical conclusion of v360, now cross-checked rather than only
a paper algorithm.

## 4. Exact effect on the lift route

For a future positive A4 owner with kernel basis `K` and marked action, the
two explicit words (2.1) can be composed immediately to give `S_1,S_2` and

\[
 \boxed{C_{\rm rel}=[\widetilde S,K]
  =\operatorname{im}(S_1-I)+\operatorname{im}(S_2-I).}
\tag{4.1}
\]

Task382 already implements and independently checks this block echelon.  It
was not executed in run 33263377923 because the positive A4 basis/action is
the deliberately missing input.  Therefore the exact frontier is:

```text
WORD-BEARING CANONICAL RESIDUAL GENERATORS: CROSS-CHECKED
ACTUAL TWO SOURCE WORDS:                    LENGTHS 538, 328 / LOSSLESS OWNER
POSITIVE A4 K/ACTION:                       NOT YET AVAILABLE
ACTUAL C_rel RANK/BASIS:                    NOT COMPUTED
OCCURRENCE IMAGE / A/JA / L/JL:             NOT CLAIMED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:     NOT CONSTRUCTED
```

`R07_CANONICAL_RESIDUAL_GENERATORS_RUN33263377923_V363_CROSS_CHECKED`
