# Luna task 159o — corrected-canary gate and first cumulative K2 rung

## 0. Authority, order, and role separation

Read `AGENTS.md`, the full mail
`ops/inbox_codex/sol_task_159o_ladder_launch.txt`, the execution authorization
`ops/express/20260823_fable_sol159n_canary_exec_auth.md`, Sol reply sections 21–23,
and the complete `sol/luna_task_159n_pent_canaries.md` before acting.

The mandatory order is:

```text
corrected Zassenhaus canary producer + independent checker
  -> all four freeze gates in Sol section 22.5
  -> explicit ORDINARY versus SPECIAL-PENT mode freeze
  -> selected K1 joint / diamond / row-36 universe
  -> one-seed K2 execution and independent replay
```

Do not name, freeze, or execute K2 while a predecessor is open.  Use separate
producer and checker authors.  A checker may receive only immutable receipt and
manifest paths, byte counts, and SHA-256 values; it must not open/import the new
producer source, helper, or report.  `verified` remains false without Lean.

Only the parent Sol session is the git/GHA broker.  A child must not commit, push,
dispatch, edit a workflow, or use es7ops.  If GHA is needed, return an exact
selective-publish list and existing-workflow argv to the parent.

## 1. Frozen ledger facts that are inputs, not jobs to rerun

1. The five accepted named windows each cover all 972 M-targets, but they are not
   a nested tower.  Individual M-relative lift choices do not imply a lift in an
   intersection with K1.
2. The bootstrap is

   ```text
   K1 = K^(36) cap N_S4.
   ```

   Its cross-checked roster has 1,944 GT rows and fibres `{2:972}` over M.
3. The sniper-chain result for `K^(27) cap N_S4` is a separate non-cofinal
   calibration only.  Its receipt/checker found three `m1=0` lifts with
   `nu=50,32,14`.  It is not rung 2 and does not advance the fair-shell cursor.
4. Dovetail v7 is healthy but has a different predicate.  Never rename or resume
   its checkpoint as RUNG cargo.  Any future live rung uses a fresh lineage.
5. LOCAL-3 continues independently; `M^[4]` remains shelved.

## 2. Fixed target and bootstrap pins

The target remains the zero-based canonical row 36; no result may substitute a
different row or either 432-set:

```text
key = [0,[[4,0],[5,0],[0,0]],[1,2,3,4,5,6,7,8,9]]
full-row compact SHA256 = 31d19295b8b5c2f5e36387f6bb63cec508a7b8770e30bfa6d02909b1f16f4cd8
target-key compact SHA256 = 3940557ee6c0118f2563ff7d19a41059d0fcdd5c7c876bc56c84b4fa9ae242ac
word compact SHA256 = b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d
```

`seed_pool_432 = X \ (NN-09 union NN-12)` is the rung pool.  It is not the
`NN-09 triangle NN-12` LOCAL-3 canary, despite both having cardinality 432.

Bind the K1 producer receipt/checker verdict and reconstruct the exact marked
quotient rather than importing a search helper.  The pre-diamond K1 raw reduction
fibre over one M target has 16 elements; this is not a post-charming candidate
count and may not be used as one.

## 3. Predecessor gate: corrected canaries

Require a versioned producer receipt and helper-disjoint checker verdict for the
entire applicable contract in `sol/luna_task_159n_pent_canaries.md`:

- literal `Dpap = RHS^-1 * LHS` in the five-factor 2008 order;
- the five printed A.18 coface tables stored verbatim, one declared paper-to-native
  conversion applied exactly once, and both frozen PB3 relators mapped to identity
  by every coface before any quotient or census is accepted;
- original exponent-two W2 explicitly rejected, never executed as class 3;
- raw Lie ranks labelled calibration only;
- exact `D4_p` pc quotients and a concrete four-deletion Brunnian witness;
- complete commutator over-universe and separately gated actual-charming subset;
- p-specific `M_F2 <= D4_p(F2)` adjudication;
- isolated/diamond refinement and complete row-36 fibre;
- `CLAIM-COVER-PENT-CANARY-2` and all mandatory mutants.

Blindness is prime-local.  A p=2 blind result does not imply that every class-3
prime is blind.  If p=3 is supplied, replay and report it separately.  A preflight
or environment-blocked receipt does not close this gate.

Bind the current mathematical addendum before interpreting either result:

```text
scratchpad/d972_idx3_arith_datum_independent_v1.md
bytes 96640
sha256 a2fae0a0365a8f1587781c797120a25532b6d274dedc609bad11c0c22082e31a
```

Keep its three ledgers separate: `W_l` collapse is proved only for `l=2,3`;
`M_F2` non-containment in `D4_p(F2)` is a distinct all-prime structural theorem;
and commutator-over-universe sensitivity is not actual-target evidence.

Also freeze `P-PENT-4` before any higher-class measurement: class 3 blindness and
first pentagon sensitivity in weight/class 4 are a preregistered prediction, not
an input fact.  A class-3 producer/checker agreement adjudicates only the first
part.  Do not scan the full `PB4/D5_2` universe of size `2^57`.  Any class-4
follow-up requires a new versioned target-fibre design, preregistration, separate
producer/checker, and explicit coverage of the selected row-36 fibre; retain
`PB3/D5_2 = 2^16` and `F2/D5_2 = 2^13` as size canaries only.

## 4. Freeze exactly one launch mode

After the corrected canary is cross-checked, issue one immutable mode token.

### 4.1 SPECIAL_PENT_FINITE_PREFIX_THEN_FAIR_SHELLS

This mode is available only when a selected prime `p` has an exact sensitive
window and the producer/checker close

```text
Jpent = (K1 cap D4_p(PB3))^diamond,
Jpent <= K1,
Jpent isolated,
```

including the actual index, marked quotient, and complete row-36 fibre.  Then the
same complete canary fibre is the proposed special K2 execution; do not run it a
second time under a renamed predicate.  Name it K2 only after the checker closes
the receipt and the parent adjudicates the token.

The Sol-side paper/marked preflight has now closed the abstract isolation step:
`D4_p(PB3)` is fully invariant and isolated; K1 is isolated; hence Prop. 3.15
makes `H_p=K1 cap D4_p(PB3)` isolated and Prop. 3.14 gives
`H_p^diamond=H_p`.  It also predicts the exact maximal common marked quotient
and row-36 raw-fibre count:

| prime | common quotient with K1 | post-diamond raw row-36 fibre |
|---:|---:|---:|
| 2 | 32 (`G36/C9^3`) | 64 |
| 3 | 1 | 34,992 |

These values are frozen expectations, not a substitute for the required
producer/checker materialization.  The next exact implementation datum is
`MARKED-QP-COLLECTOR-AND-JOINT-KERNEL-MATERIALIZATION-RECEIPT`; reject a receipt
that merely asserts the table without reconstructing the marked maps, joint
kernel, all rows, and coverage digest.

This is a finite extra prefix, not the ordinary fair-shell winner.  The manifest
must freeze `fair_resume_shell=2`.  After this rung, process index shells 2,3,...
without permanently skipping any shell; the finite extra intersection then does
not damage cofinality.

### 4.2 ORDINARY_FAIR_SHELL_FIRST

Use this mode if no special pent prefix is selected.  The current LINS artifact is
candidate-grade inventory, not a K1 joint receipt.  Its index-2 C2 row is a no-op.
The first potentially strict ordinary source is the unique cyclic index-3 row:

```text
node_id = 16437e56512d99ab2c7ca8328293863fe6b7792504ebd592fa21da9d7952bc37
b3_index = 3
quotient = C3
source_digest = c6f20bd5c6edc071c48a6ecd10f09e0dcfd0ef232bfa0ee7d3bf4aba45a60158
```

Close every index-2 and index-3 subgroup/core class, including the S3 no-op, before
declaring the shell complete.  For the C3 row, independently reconstruct the
pre-diamond marked joint `G36 x C3 x PSL(2,8)` and its predicted raw fibre 48, but
do not promote either expected value until producer and checker agree.

The existing Q8/L48B/Heisenberg/PGL receipts are over M, not K1, and cannot replace
this work.  Q8/L48A is a prospective duplicate of K1; L48B is a prospective central
refinement.  Both statements remain preflight until a dedicated joint/diamond
receipt is independently checked.

The prepare-only ordinary word section is now frozen:

```text
producer  search/d972_rung_ordinary_idx3_producer_v1.py
          54140 bytes / 6fc7035cbeff7e77cdb3c89ef10fa577c44c9f3ecfae86e38932206f264bba63
prereg    search/certs/d972_rung_ordinary_idx3_prereg_v1_20260824.json
          46431 bytes / 17c1046765eaaec51022f541055d602431baa9f7aa6fb44964f33036c0c23f11
manifest  search/certs/d972_rung_ordinary_idx3_launch_manifest_v1_20260824.json
          5678 bytes / 4463f5c81c945b18be723167ececb95670b22de07654392ac146800e9f4408fd
```

It deterministically materializes all 48 predicted coordinates as signed x/y
words and replays their marked images.  This is `PREREGISTERED_NOT_RUN`, not an
outcome receipt.  Its execute path must continue to stop on `MODE_TOKEN_REQUIRED`
unless the parent supplies an immutable `ORDINARY` token bound to this exact
preregistration after both corrected-canary checker gates close.

## 5. Selected-source producer contract

Freeze a preregistration before the outcome run.  It must bind:

1. parent K1 and selected source/core/diamond definitions and byte/SHA pins;
2. exact maps on marked `sigma1,sigma2,x,y,c`, relation replay, kernel equality,
   and `Kcandidate <= K1 <= M`;
3. the complete finite component set used to define `H^diamond`, equality proof,
   isolation, index, `N_ord`, quotient order, and nontriviality/duplicate decision;
4. row 36, both 432 rosters, word/action/multiplication conventions;
5. exact raw fibre cardinality and deterministic enumeration order;
6. each candidate's two hexagons, charming, onto, exact reduction, and—only in
   special pent mode—the same-representative `Dpap` result;
7. candidate/evaluated/rejected counts, reason histogram, aggregate digests, and
   omission/duplicate guards.

A positive run may stop at the lex-first valid lift, but it must retain enough data
for exact word-level checker replay.  A negative run may not stop early and must
close `CLAIM-COVER-RUNG-1` over the entire registered raw fibre.

## 6. Independent checker and destructive suite

The checker must reconstruct the selected quotient/maps/predicate without new
producer code or helpers.  At minimum reject:

- source omission/duplication and an unclosed index shell;
- wrong parent inclusion, duplicate/non-strict source relabelled as K2;
- missing or forged diamond/isolation equality;
- row 35/37 or one-based row shift;
- the wrong 432 roster;
- reversed word or permutation multiplication;
- one hexagon/coface omitted, charming without onto, target-key mutation;
- single representative reported as a fibre;
- early-stop negative, count/digest mutation, and receipt/hash mutation;
- old W2 or a prime-local blind result relabelled as a universal pentagon result.
- a count-fitting A.18 product reversal that fails even one source relator, and a
  mixed paper/native serialization that happens to preserve the final histogram.

## 7. Venue and GHA contract

Measure exact raw count and a fixed-prefix benchmark before choosing a venue.
Finite-group exact enumeration on GHA is the default.  SAT is forbidden unless a
new same-predicate encoder, producer-independent semantic checker, positive and
negative controls, and independent LRAT replay all exist and benchmark cheaper.

For GHA, return to the parent before dispatch with: exact selective file list,
bytes/SHA, remote parent/ref, existing workflow name, all inputs, timeout/memory,
artifact paths, ordered success markers, and forbidden diagnostics.  Do not edit a
workflow.  The final report must record every run ID and commit SHA, including
superseded/failing preflights.

## 8. Scoped outcomes

Allowed terminal routing is:

```text
K2_CROSS_CHECKED_SURVIVES_FIXED_ROW36
K2_CROSS_CHECKED_FULL_FIBRE_NO_LIFT__RUNG_FALL_CANDIDATE
K2_STATE_STOP_PREDECESSOR_CANARY_OPEN
K2_STATE_STOP_DIAMOND_OR_JOINT_CONTRACT_OPEN
K2_UNKNOWN_ENVIRONMENT_OR_RESOURCE_BLOCKED
```

`RUNG_FALL_CANDIDATE` still requires commander adjudication before any 648/fake
ledger promotion.  A positive K2 is one named-rung survival, not genuine and not
cofinal survival.  Never emit a B4, arithmetic, fake/genuine, or 648-wide token from
this task alone.

Write the implementation report to a new versioned `sol/luna_reply_159o_*.md` path.
End it with exact bytes/SHA values, commands/runtimes, firewall statement, all
git/GHA run metadata, selected mode, first missing datum, and one scoped token above.
