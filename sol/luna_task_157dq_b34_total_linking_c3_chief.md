# Luna 157dq — total-linking C3 chief descent below the cross-checked A5^4 layer

Role: Luna implementation.  This is the fast T-50 fallback while frozen 157dn
continues on GHA.  Do not edit, stop, or repin the running 157dn v2 lane.

Create only these four versioned files:

1. `search/d972_b34_total_linking_c3_chief_v1.g`
2. `search/check_d972_b34_total_linking_c3_chief_v1.py`
3. `search/d972_b34_total_linking_c3_chief_gha_driver_v1.g`
4. `sol/luna_reply_157dq_b34_total_linking_c3_chief.md`

No workflow edit, Git, GHA dispatch, local production GAP, or other heavy local
run.  One lightweight checker selftest is authorized.  Use the existing GAP
wrapper only if a truly lightweight syntax/selftest needs GAP; otherwise leave
the first GAP production replay to GHA.  Preserve unrelated worktree changes.

## Frozen inputs

Bind exact source SHAs from the corresponding receipts and at least these
artifact identities:

- q3 receipt `ci/out/d972_b345_q3_chief_v1.json`, frozen SHA-256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`;
- FC8 receipt `ci/out/d972_b4_fc8_a5four_v1.json`, frozen SHA-256
  `558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584`;
- 157dp receipt `ci/out/d972_b34_a5_selected_lift_v1.json`, cross-checked run
  32171982444, frozen SHA-256
  `d3cb729d972a1b460cd8f0a76b49cd6abf4eafd7fe0c112ad0ad742de5200157`;
- current 157dp sources: producer
  `9fb5fa16cd913ba559e96a0431cf6be4b902f1dedff289ab7e5e3d6c9adb6500`,
  checker
  `2d30b1458725cb70d94cb4ab35256988bf23cc2d796a422d3f0b14d1c2f6805e`,
  driver
  `cce2dff8e4a96046d97f70f64a31f279ced5feeeb08dca55de82b59f7154171e`.

The thin full driver must regenerate q3, FC8, and 157dp in child processes,
require every upstream independent checker PASS, and then run the new producer
and checker in the same job.  If fresh FC8/157dp receipts differ from the frozen
ones only in their registered nonsemantic runtime field, normalize only that
field to the historical value, prove all other parsed fields equal, require the
exact frozen SHA, and rerun the upstream checker.  Reject every other drift.
Delete all fixed output/log/sentinel paths before use; zero-exit sentinels and
exactly-one terminal/checker markers are mandatory.

## Mathematical target

Let

```text
H     = ker(PB4 -> E4),       E4 = Q4 x Pi4[3] from the q3 receipt,
L     = H intersect ker(rho_A5) from the cross-checked 157dp/FC8 layer,
ell   : PB4^ab = Z^6 -> Z,    ell(A_ij)=1,
beta(h) = ell(h)/6 mod 3,
Kbeta = ker(beta) = H intersect ker(ell mod 18),
L'    = L intersect Kbeta.
```

Prove by receipt, not by an asserted boolean, that `H/Kbeta = C3` is an actual
`B4`-chief factor and that the *same actual 157dp candidate 124* defines one
outside literal charming/onto pair at `L'`.  This is one strict chief descent
`L -> L'`; it is not global B4-B and is not a uniform iteration theorem.

## FC-beta-1: exact marked abelian lattice (load-bearing)

Use tuple order `[12,13,14,23,24,34]` throughout.

1. Reconstruct from the four deletion maps and actual G9 marks the marked map
   `H9 -> (G9/G9')^4`.  Emit the complete `8 x 6` binary matrix (or an exactly
   equivalent canonical row representation), prove rank 5, kernel exactly
   `<(1,1,1,1,1,1)>`, and image order `32 = |H9^ab|`.  Do not infer this from
   the abstract isomorphism type alone.
2. Independently replay that the marked matrix of `Pi4[3]^ab` is `I6 mod 3`.
3. Construct the integral congruence lattice

   ```text
   ker(q_ab) = { v=3w in Z^6 : w mod 2 lies in <(1,1,1,1,1,1)> }.
   ```

   Producer and checker must independently obtain a canonical HNF/SNF-style
   basis (enumerating the 6^6 residue box is permitted), its determinant/index,
   and `gcd{sum(v): v in a lattice basis}=6`.  Bind the exact-sequence reason
   `im(H -> PB4^ab)=ker(PB4^ab -> E4^ab)`; do not claim that `A12^6` itself is
   automatically in H.
4. Hence certify `ell(H)=6Z`, beta onto, `Phi3(H)<=Kbeta`, and
   `Kbeta=H intersect ker(ell mod18)`.
5. Replay the frozen `H normal B4` typing.  Reconstruct the natural B4 action
   on the six edge classes and prove it preserves total linking and beta.
   Therefore `Kbeta normal B4`; prime order `|H/Kbeta|=3` makes it chief.

The Python checker must reconstruct the matrices, modular ranks/kernels, and
integer lattice independently; it must not import or translate producer helper
code.

## FC-beta-2: direct replay of the real candidate 124

Do not use only the 20-letter q3 base pair and do not invoke an abstract glue
existence theorem as the certificate.  Reconstruct the actual selected 157dp
candidate (outer 1, shift 0, correction 124) from the registered universe and
require its exact word, word SHA, 92-letter reduced representative, and free
exponent sums `(0,0)` to agree with the cross-checked receipt.

Rebuild every acceptance residual independently from the literal formulas:

- two hexagons, with every required PB3->PB4 coface typing;
- the ordered A.18 pentagon;
- charming/derived representative and friendly/marking data (`m=0`,
  `lambda=1`);
- source/representative-independence residuals;
- the S and T relation residuals used by onto;
- both `ST` and `TS` generator residuals for the two-sided inverse.

For every residual require, by direct evaluation,

```text
E4 value = identity,
integer total-linking value = 0              (stronger than only mod 18).
```

PB3/F2 typing for `Kbeta` is the five-coface pullback
`intersection_j (d^j)^-1 Kbeta`; never identify it with `Phi3(H3)`.  Also replay
the difference between the 92-letter candidate and the q3 20-letter base as an
actual H_F2 correction, all five cofaces, `m=0`, and all six marked maps
(FC-30).  A single aggregate digest is not enough: preserve per-residual words,
values, and bounded digests so the checker can locate a failure.

## FC-beta-3: onto, intersection, orders, and outside roof

1. For `PB4/Kbeta = im(PB4 -> E4 x C18)`, prove the candidate map descends and
   is onto using exact relation replay, the authenticated E4 automorphism, and
   the induced identity on beta.  Replay the corresponding PB3/F2 five-character
   maps.  Do not replace onto by a raw generator-count heuristic.
2. Pin and independently replay the FC8 single-support/full-product proof of
   `H/L = A5^4`, including perfectness/no-C3-quotient; do not trust only the
   inherited `surjective=true` field.  Then prove by Goursat
   `L Kbeta=H` and `[L:L']=3`.  Componentwise literal validity of the same word
   gives the pair at the intersection; settlement remains diagnostic-only.
3. Compute every `N_ord` with Definition 3.1's PB3 formula
   `lcm(ord(x),ord(y),ord(c))`, where `c=x12*x13*x23`, in each actual finite
   quotient.  Require exact values

   ```text
   H_ord=18, Kbeta_ord=18, L_ord=90, L'_ord=90,
   gcd(L_ord,Kbeta_ord)=H_ord=18.             (FC-29)
   ```

   An `A12`-only order gate is insufficient.
4. Replay the frozen row-37/exponent-2 outside classifier and the exact
   reduction of the selected pair.  No new arithmetic membership classifier
   may be inferred.

## Terminals and claim boundary

Use a strict schema and exactly one of these outcomes (names may be tightened
before freeze but their meanings may not be widened):

- `B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED`: all gates above pass;
- `B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED`: the fully evaluated
  registered candidate fails a literal mathematical gate; this is only a
  candidate-specific negative, not B4-A and not an obstruction theorem;
- `B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT` or
  `B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_RESOURCE`: missing/drifting typed input
  or a declared cap prevents evaluation.

On PASS, state exactly: one outside `GT^heart(L')` pair exists and accepted
T48-1 moves the known window from `L` to the strict index-three subgroup `L'`.
Do not write `I_L=X`, isolation of L/L', cofinal iteration, compactness, or
global B4-B.  A non-PASS result must not be promoted to B4-A.

## Performance and independent checking

This lane must not construct/enumerate H, E4, A5^4, or a full Fox/group-ring
basis.  No PB5, ANUPQ call, translation BFS, sparse Gaussian search, or
candidate universe scan is allowed in the new core.  Only the existing small
P/G9/PC collectors, 6-dimensional integer/modular linear algebra, and the
finite list of literal residuals may be used.  Record exact operation counts,
caps, and runtime.  Target standalone runtime is 2--10 seconds and same-job
upstream runtime 20--60 seconds; if the source contradicts that estimate,
report it rather than hiding work.

The independent checker must reconstruct all load-bearing data from frozen
receipts/formulas without importing producer code, require exact schema/key
sets, replay the selected word and every residual, and include mutations for:

- binary marked matrix/rank/kernel;
- Pi4 `I6` marking;
- lattice gcd/index and beta invariance;
- candidate word/index/hash;
- one hexagon, pentagon, S/T relation, and ST/TS residual;
- FC-29 order tuple;
- FC8 perfect/no-C3 gate;
- outside row;
- terminal/claim-boundary widening.

Report exact final SHAs, the one authorized selftest result, source-only runtime
estimate, and an honest GO/STOP in the reply.
