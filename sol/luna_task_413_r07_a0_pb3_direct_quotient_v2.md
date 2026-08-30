# Luna task 413 — R07 A0 compact positive-first lazy owner v2

Role: Luna implementation and bounded fixtures only. This supersedes the
unlaunched PB3-direct-quotient draft that previously occupied this filename.
Do not prove a new PB3/PB4 quotient theorem, construct either full boundary
closure, run heavy production locally, commit, push, edit a workflow, or touch
pre-existing files.

The objective is one useful A0 production run as soon as possible. Combine:

1. task411's authenticated compact presentation (44 literal correction
   relators), direct task198 runtime, normalized exponent coordinates, compact
   integer interner/reducer, and literal exactification support;
2. task179/v140/v163's positive-first column generation and exact lazy
   PB3/PB4 boundary oracle.

The full PB3 and PB4 closures are forbidden. The lazy oracle is already exact
for all translates of the 2+2+11 typed boundary seeds.

## 1. Required versioned outputs

Create only:

1. `search/d972_r07_a0_compact_positive_lazy_owner_v2.py`;
2. `crosscheck/check_d972_r07_a0_compact_positive_lazy_owner_v2.py`;
3. `search/d972_r07_a0_compact_positive_lazy_owner_gha_driver_v2.g`;
4. `sol/luna_reply_413_r07_a0_compact_positive_lazy_owner_v2.md`.

Do not modify task411 or task179. Copy narrowly from them and pin the exact
source bytes used. Do not read or resume the obsolete 1.66 GB checkpoint or
the failed task411 full-closure checkpoint.

## 2. Frozen mathematical contract

Use:

- `sol/proof_r07_positive_only_common_word_colgen_v140.md`;
- `sol/proof_r07_full_boundary_dual_decision_v163.md`;
- `sol/proof_r07_a0_occurrence_quotient_invariant_span_v396.md`, Theorem 2.1
  only for the 44-relator normal-image source;
- `sol/proof_r07_a0_normalized_exponent_lattice_repair_v399.md`.

Solve only the positive finite equation

```text
-T in D_full + V(normal_closure(compact_44)).
```

Because the compact 44 relators have the same registered normal closure as
the old 6,441 roster, task179's exact occurrence formula and support-hitting
conjugator oracle apply with the compact roster substituted literally. Do not
stream the 6,441 equality oracle before useful production. A no-hit or resource
stop is `UNKNOWN_RESOURCE`/`UNKNOWN`, never NONMEMBER.

## 3. Runtime and compact roster

Reuse task411's direct authenticated bootstrap, roof/acceptance/joint/q3
pins, deterministic compact presentation, registered unadjusted Q0 defects,
and roster gates. Require:

```text
compact_relator_count == 44
compact_roster_sha256 ==
7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8
```

Every relator must evaluate to the identity in the joint accepted runtime.
For every relator require exact exponent divisibility by 18 and attach
`(epsilon_x/18, epsilon_y/18) mod 3`; source conjugation copies these two
coordinates unchanged.

Use task179's frozen eleven-occurrence `AllSevenModel` semantics. Keep all
occurrences separate until its signed-prefix physical aggregation. A
correction factor is the literal `delta * r * delta^-1`, with ancestry
sufficient to reconstruct it; coefficient two means the inverse factor.

## 4. Positive-first loop — no boundary closure

Start a fresh compact central sparse echelon. It may insert the 15 identity
boundary seeds and the 44 identity correction columns if rank-raising. Then
repeat:

1. reduce the target;
2. if zero, reconstruct and directly replay the positive certificate;
3. otherwise construct task179's exact triangular dual;
4. call the exact lazy boundary oracle first;
5. if it returns an ACTIVE translated boundary, insert that one full sparse
   physical column and restart;
6. otherwise call the correction oracle over the 44 compact relators;
7. if it returns an ACTIVE literal conjugate, insert that one physical column
   and restart;
8. if the finite/bounded correction schedule has no hit, return UNKNOWN.

Port task179's `boundary_oracle` exactly: for each dual support occurrence and
each of the 2+2+11 base boundary rows, form the left translation
`t = g*h^-1`, accumulate all contributions by `(block,relator,t)`, and only
then declare ACTIVE. It covers the complete PB3 and PB4 boundary images
without enumerating them. No B3/B4 pivot table, frontier, closure DAG, or
closure checkpoint is permitted.

Port task179's `occurrence_data`, `formula_scalar`, fibre/global section
machinery, and correction support-hitting schedule, but replace its old roster
with the compact 44 words. Retain its direct formula/full-column scalar
equality gate. Do not pre-enumerate or cache a global conjugator roster.

## 5. Memory, checkpoint, and progress contract

Use task411's canonical integer interner and sparse reducer or an equally
compact port. Keep only rank-raising central columns, minimal word/boundary
ancestry, current correction cursor state, and immutable runtime tables.
Do not retain contributor lists for inactive boundary candidates, failed-row
reduction traces, old duals, full section rosters, or verbose direct-replay
objects per column.

Checkpoint is for this positive-first state only. It must be gzip+marshal,
hash-before-decode, atomic, and contain the compact echelon/interner, retained
minimal ancestry, current dual-bound correction cursor, counters, and binding
hashes. Write after a rank increase and at most once per wall-clock slice;
never write a duplicate phase-zero checkpoint. Resume must continue the
current correction cursor exactly. A resource stop with a valid checkpoint is
resumable.

Print a progress line immediately after runtime/roster construction and at
least every rank increase or 60 seconds:

```text
phase=positive_lazy rank=... round=... boundary_pairs=...
compact_relator_cursor=... correction_candidate_cursor=...
row_nnz=... total_pivot_nnz=... owner_rss_bytes=... elapsed=...
```

Run sequentially first. Do not add multiprocessing, profiling infrastructure,
SAT, SELFTEST-before-production, mutation campaigns, or speculative PB4
mathematics. The 44-roster reduction and absence of both full boundary
closures are the speed and memory repair.

## 6. Positive terminal

On zero remainder, reconstruct only selected ancestors and require:

- exact sparse identity `T + correction + boundary = 0`;
- correction literal lies in the joint kernel;
- normalized exponent coordinates are zero;
- v399 reconstruction of `r3,r9,r12,u0,v0`, followed by exactification;
- exact integer exponent pair `(0,0)`;
- direct full all-seven Fox replay of the exactified word;
- typed boundary records `(block, base_relator_index, translation_hex,
  coefficient)` replay to the emitted residual. A literal section word may be
  included when already available, but must not trigger a new section search;
  the exact typed quotient element is a sufficient boundary coefficient.

Only this terminal may be `COMMON_WORD`. It is finite A0 only; do not claim a
cofinal lift, fake, or Ihara witness.

The independent checker should be a narrow positive-receipt checker. It may
skip expensive work on UNKNOWN. It must rebuild the selected literal
correction, exactification, target, and selected typed boundaries without
importing the producer, then check the final identity. Do not build full
closures in the checker either.

## 7. Bounded acceptance and handoff

Run only `py_compile`, `--help`, hash pins, and fixtures lasting a few seconds:

1. tiny sparse positive column-generation fixture;
2. exact lazy-boundary cancellation/ACTIVE fixture, including wrong
   translation orientation rejection;
3. compact-roster substitution gate (44, exact digest);
4. checkpoint roundtrip and one-byte corruption rejection.

Do not run actual A0 locally. Production must be the first parent action after
the files are handed back. Report exact bytes/SHA-256, the precise GHA command,
done/progress markers, and a conservative per-slice RSS/time bound.

`TASK413_COMPACT_POSITIVE_LAZY_OWNER_V2`
