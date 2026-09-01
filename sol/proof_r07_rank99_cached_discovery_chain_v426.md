# R07 rank-99 cached discovery chain (v426)

Author: Sol / 2026-09-02

Status: paper theorem and execution contract.  It separates an optional
selector cache and candidate checkpoint chain from the final independent
semantic certificate.  The completed Task453 timing audit below shows that
the cache is not the present bottleneck and must not be implemented ahead of
the candidate-chain/partial-batch repairs.  This note does not promote the
current rank-99 state, assert a COMMON word, or make a negative exhaustion
claim.  `verified=false`.

## 1. The expensive object is an oracle index, not a proof premise

In the Task451 lineage the selective construction visits exactly

```text
Q0 states                    1,469,664
three coordinate stores     176,359,680 bytes total
```

and then performs the three `S0,S1,S2` membership passes.  These data are
independent of the current dual and of the physical rank.  They depend only
on the byte-pinned Q3/joint input, the fixed marked actions, and the frozen
coordinate conventions.  Rebuilding them at every 16-rise continuation is
therefore not a mathematical requirement.

Let `Omega` be a versioned cache containing at least the three packed
coordinate stores, the Q0 parent/letter tree, and the emitted word-bearing
kernel generators.  Its manifest binds all frozen source hashes, dimensions,
component offsets, byte lengths, and component SHA-256 values.  Ephemeral
process-dependent hash tables are not part of `Omega`; a consumer rebuilds
them from the packed stores.

The cache is a **discovery index**.  It may propose a singleton fibre and a
kernel-prefix word, but it is not allowed to certify a row, a miss, or a
prefix.

### 1.1 Measured priority correction

Task453 run `33516227668` gives the required wall-clock decomposition on the
same GHA hardware.  The GAP script started at `13:55:18Z`; the first Q0
progress line appeared at `14:08:24Z`.  Q0 plus all three membership passes
then finished at `14:08:45Z`, only about 21 seconds later.  The producer did
not reach a closed row and stopped at `15:57:27Z`.  Its independent checker
then rebuilt/replayed and passed at `16:50:32Z`.

Thus the 176-MB cache would remove roughly tens of seconds in this run, while
base reconstruction cost about 13 minutes, the open candidate scan about one
hour 49 minutes, and the resource checker about 44 minutes.  Cache reuse is
mathematically safe by Theorem 2.1, but it is **deferred** unless later
profiling shows a materially larger share.  The immediate speed work is
delayed literal certification, durable partial batches, and terminal-only
full replay.

## 2. Literal replay makes cache use positive-safe

For a proposed correction `(i,delta)`, retain the v424 order and gates:

1. evaluate `delta` in all registered coordinates and require the selected
   coordinate to equal the requested target;
2. replay the kernel word and require its selected coordinate to be the
   identity;
3. compute the actual row
   `aggregate(replay_atom(i,delta))`;
4. reduce it nonmutatingly in the current physical echelon and discard it if
   dependent;
5. only for an independent row, construct the literal conjugate, require
   equality with the fresh `seed_v12` row, exact exponent divisibility,
   forbidden-coordinate absence, formula/direct/dual scalar equality, row
   digest equality, and predicted-pivot equality; and
6. mutate once with the actual `add` and require the returned pivot to be the
   predicted pivot.

### Theorem 2.1 (CACHE-INDEPENDENT POSITIVE SOUNDNESS)

Any row which passes clauses 1--6 is the same legal literal correction
column that would be obtained by evaluating its recorded source word without
`Omega`.  This remains true if `Omega` is incomplete, reordered, or otherwise
wrong.  Such a cache may cause a hard rejection, a different search order, or
a missed candidate, but cannot make an invalid row pass the retained gates.

#### Proof

The cache contributes only the proposed word `delta`.  Clauses 1--2 replay
its fibre assertions from the word.  Clauses 3 and 5 independently identify
the physical occurrence column with the literal conjugate column and impose
all legal side conditions.  Clauses 4 and 6 prove the exact rank rise in the
current physical span.  None of these equalities reads a claimed row or
scalar from the cache.  Hence acceptance depends only on literal evaluation
and the current authenticated echelon.  Cache corruption can remove or alter
proposals, so it cannot support a nonexistence conclusion.  It cannot forge
an accepted proposal because every load-bearing value is recomputed. \(\square\)

Thus a producer may load `Omega` after checking its structural manifest.  A
final independent checker need not trust or even read `Omega`; it replays the
recorded literal rows.

## 3. Candidate segments need not each pay for a full checker

Let `C99` be the exact Task451 closed state of v424.  Let

\[
 C_{99}=S_0\prec S_1\prec\cdots\prec S_m
\tag{3.1}
\]

be an append-only chain of own-schema closed states.  Every segment retains
the v424 equations:

- the first 56 records and first three batches are literally equal to
  `C99`;
- appended batches flatten exactly to appended records;
- segment starts equal the complete preceding end tuple and seal;
- each batch has at most 16 rises and each invocation has at most 64 new
  rises; and
- every resumed producer reconstructs the physical prefix by actual row
  replay before adding a new row.

Call an intermediate `S_j` a **producer-authenticated candidate** until an
independent checker replays it.

### Theorem 3.1 (FINAL-REPLAY SUFFICES FOR A CANDIDATE CHAIN)

Suppose the independent checker starts from the canonical `C99` owner,
replays every row of `S_m` in chronological order, checks every literal,
scalar, pivot, batch, dual/remainder, segment, and prefix equation, and
accepts the final COMMON reconstruction.  Then the mathematical certificate
does not depend on independent acceptance of `S_1,...,S_{m-1}` at the times
they were produced.

#### Proof

The terminal state `S_m` contains the complete append-only ancestry, not
references to unexpanded semantic claims made by intermediate checkers.  The
final replay reconstructs the unique physical sequence from canonical
`C99` and checks every transition which occurred in every segment.  Hence an
incorrect intermediate state either cannot be replayed into `S_m` or is
rejected at its first false transition.  Intermediate checker verdicts add
redundant evidence but no missing premise to the accepted final replay.
\(\square\)

The same argument permits an occasional audit checkpoint without requiring
one after every short batch.  It does **not** permit an intermediate miss or
cache exhaustion to be called NONMEMBER.

## 4. Exact fast execution contract

The positive discovery lane may therefore run as follows.

1. Cross-check `C99` once.  This remains the gate currently assigned to the
   recovered checker-only run.
2. Build `Omega` normally in memory.  A persistent version is optional and
   is not an immediate implementation target under the Task453 timings.  If
   one is later used, its interruption retains the preceding closed A0
   checkpoint and contributes no progress numerator.
3. Run repeated 16-rise/at-most-64-rise producer segments.  Each invocation
   authenticates the entire literal prefix and writes BOOTSTRAP before heavy
   reconstruction, as in v424.  Resource terminals publish a candidate
   checkpoint and optional cache, without running a full independent checker
   merely to start the next candidate segment.
4. On COMMON, run the independent checker from canonical `C99` across the
   complete appended chain.  Only its accepted literal replay promotes A0.
5. Any structural/cache/path failure is UNKNOWN.  Any fully searched finite
   cache miss is still UNKNOWN_INCOMPLETE because `Omega` is not an exhaustive
   instruction-universe certificate.

This contract preserves the load-bearing prefix comparison while allowing
semantic replay of the whole growing chain to be paid at the terminal (or at
deliberately chosen audit intervals), not after every short segment.  Under
the present timing evidence, this replay deferral is material; persistent
selector caching is not.

## 5. v220 consequence

This theorem changes runtime architecture, not a milestone numerator.

```text
A0 actual COMMON:                         still 0/1
rank-99 prefix equality:                  remains load-bearing
selector table rebuilt every segment:     cheap in current profile; cache optional
independent replay after every segment:   not required for discovery
independent final full-prefix replay:      required for promotion
negative claim from cache miss:           forbidden
```

The immediate implementation successor should be a narrow transform of the
audited actual rank-99 owner which adds a `DISCOVERY_RESOURCE` chain mode and
preserves already certified rows at a resource boundary, while leaving the
COMMON checker and all v424 literal gates unchanged.  Do not add persistent
`Omega` export/import until profiling justifies its 176-MB payload.

`R07_RANK99_CACHED_DISCOVERY_CHAIN_V426_PAPER_GRADE`
