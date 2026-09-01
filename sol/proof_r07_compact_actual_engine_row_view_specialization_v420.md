# R07 compact actual-engine row-view specialization (v420)

Author: Sol / 2026-09-02

Status: paper/ABI theorem supporting the Task462 compact positive owner.  It
proves that the adopted Task458 occurrence-separated engine can be
specialized from its authenticated 6,441-word presentation view to the 44
Task411 literal relators without changing its target, action, or PB-boundary
arithmetic.  It proves soundness of every finite MEMBER, not completeness of
the compact span.  No actual MEMBER, lift, fake, or Ihara witness is asserted.
`verified=false`.

## 1. Frozen objects and two distinct roles of the authority

Let \(\mathcal A\) be the authenticated Task198 authority and let

\[
 \mathcal R_{\rm old}=(r_1,\ldots,r_{6441}),\qquad
 \mathcal R_{\rm pc}=(s_1,\ldots,s_{44})                 \tag{1.1}
\]

be respectively its historical presentation roster and the independently
reconstructed Task411 compact roster.  Task411 fixes

```text
count  = 44
digest = 7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8
```

and v397/v418 give

\[
 \langle\!\langle\mathcal R_{\rm pc}\rangle\!\rangle
 =\langle\!\langle\mathcal R_{\rm old}\rangle\!\rangle
 =\ker(F(x,y)\twoheadrightarrow\Delta _0).              \tag{1.2}
\]

The actual Task456 engine uses \(\mathcal A\) in two logically different
ways.

1. Its Task193/Task198 owner data construct the pointed target, the eleven
   occurrence actors, the three outer universes, the marked action, and the
   typed PB-boundary oracle.
2. Its `rows` view supplies the literal word \(u_i\) when a relator column is
   evaluated and again when a successful proof node is expanded into
   \(((w u_i)-w)\).

The first role must never be replaced by Task411 data.  Only the second role
is specialized below.

## 2. Extensionality of the actual direct engine

Fix the authenticated Task193 target package and all Task198 runtime data.
For a finite indexed roster
\(\mathcal U=(u_1,\ldots,u_m)\subset\ker\rho _0\), define

\[
 q_i=\operatorname{relator\_seed}(u_i),\qquad
 \bar q_i=\operatorname{project}(q_i).                  \tag{2.1}
\]

Here `relator_seed`, `project`, the marked action, and the target oracle mean
the inherited Task458 operations, not newly encoded coordinates.

### Lemma 2.1 (ROSTER EXTENSIONALITY)

After the actual authority, runtime, boundary ledger, and Task193 package
have been constructed, the Task458 `DirectEngine` depends on the relator
roster only through:

```text
relator_seed(i):       authority.rows[i-1]["word"]
run seed traversal:   i = 1,...,m
member expansion:     authority.rows[i-1]["word"]
replay_terms:         relator_seed(i)
```

All occurrence actors, `fixed_pre`, pointed target, marked-action operators,
outer PB seeds, translated-boundary correlation, and target reductions are
independent of the choice of \(\mathcal U\).

#### Proof

This is a direct decomposition of the accepted Task458 generated body.
`DirectEngine.__init__` constructs its universes, generator states,
Task193 transitions, pointed rows, occurrence package, fixed pre-column,
target, outer-boundary seeds, and the four source actions from the delegated
authority receipt, runtime, boundary ledger, and Task193 package.  It does
not traverse `authority.rows`.  The four sites displayed above are the only
semantic roster reads.  `action_pair`, `action_source_word`, `project`,
`correlate_outer`, and `translated_outer_boundary` operate on the already
constructed actual states and sparse coordinates.  Hence two read-only
authorities with the same delegated owner objects and the same indexed word
view give identical actual arithmetic for every selected word. \(\square\)

### Corollary 2.2 (READ-ONLY COMPACT PROXY)

Authenticate \(\mathcal A\) completely first.  Let \(\mathcal A_{\rm pc}\)
delegate every attribute to \(\mathcal A\), except that its read-only `rows`
property is the 44-word view \(\mathcal R_{\rm pc}\).  Construct the runtime
and boundary ledger from \(\mathcal A\), and give only the DirectEngine and
its proof expansion \(\mathcal A_{\rm pc}\).  Then a module-local loop bound
of 44 evaluates exactly

\[
 q(s_1),\ldots,q(s_{44})                                \tag{2.2}
\]

inside the original Task193/Task198 target module.  It neither bypasses the
6,441-row authority authentication nor evaluates those 6,441 words as A5
seeds.

The order is load-bearing: mutating the physical receipt before its authority
validation would be unsound, while replacing only the post-validation
read-only word view is the extensional specialization of Lemma 2.1.

## 3. Positive soundness

Close the actual rows (2.2) under the inherited four marked left actions and
allow the inherited typed PB-boundary oracle to insert equality slack.  If
the actual target reduces to zero at a finite time, the Task458 proof DAG
expands the solution as

\[
 \theta=\sum_{g,i}a_{g,i}g(b_i-1),\qquad
 M=\sum_{g,i}a_{g,i}\bigl((w s_i)-w\bigr),               \tag{3.1}
\]

where \(b_i=\rho _1(s_i)\), with all selected PB translations kept in the
separate boundary ledger.

### Theorem 3.1 (ACTUAL COMPACT MEMBER)

Every checker-replayed finite MEMBER returned by this specialization is a
sound actual A5 MEMBER with literal A6 ancestry \(M\).

#### Proof

Each \(s_i\) lies in \(\ker\rho _0\) by (1.2), so v419 Lemma 1.1 makes each
actual column and every marked translate legal.  Lemma 2.1 says the machine
column, action, target, and PB reduction are exactly the inherited Task458
operations.  The inherited `_member`/`replay_terms` equality proves the raw
target equation, and its proof expansion reads the same compact word view to
produce (3.1).  The independent checker repeats these operations using the
Task411 checker reconstruction of the 44 words. \(\square\)

## 4. Negative and resume boundaries

The compact action span need not be the full relative ideal before the v418
K closure.  Therefore an exhausted actual run has only the terminal

```text
UNKNOWN_INCOMPLETE:compact_direct_span_exhausted
```

and no A5/A6/A7/fake/Ihara claim.  An inherited `NONMEMBER` object may be
used internally to detect exhaustion but must not cross the producer or
checker boundary.

This short specialization has no automatic honest serialization of the
Task456 universes, proof DAG, two echelons, action queue, and PB cursor.
Until such a state is physically implemented, it must declare
`resumable=false`; a cursor-only or rank-only checkpoint would be false.
Task459/459a remains the resumable complete two-level owner.

## 5. Machine acceptance gate

A compact positive implementation is admissible only if all of the following
hold.

```text
full Task193/Task198 authority authentication precedes the row proxy
runtime and BoundaryLedger are built from the original authority
DirectEngine receives the read-only 44-word proxy
Task411 producer count/digest are pinned
checker reconstructs the roster through the Task411 checker path
actual relator_seed / action_pair / project / target oracle / PB oracle remain
actual _member and checker-side check_member remain
miss -> UNKNOWN_INCOMPLETE
resumable=false unless complete actual state is serialized
synthetic sparse_column / external JSON target / empty assumed PB ledger: absent
```

`R07_COMPACT_ACTUAL_ENGINE_ROW_VIEW_SPECIALIZATION_V420_PAPER_GRADE`
