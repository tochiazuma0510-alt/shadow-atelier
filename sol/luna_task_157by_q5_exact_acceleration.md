# Luna task 157by — exact q5 obstruction acceleration

## Role and objective

You are Luna.  The active q5 and synchronized Burau campaigns are already
running on GHA.  Design a materially faster **exact** route to the same
terminal question: whether one of the frozen 972 roof rows has an empty
complete pentagon fiber in the auxiliary finite Burau quotient.

The present producer enumerates the full image/derived image before a cheap
972-row scan.  Inspect the v4/v5 and joint-v1/v2 implementations and locate
the actual asymptotic bottleneck.  Seek a sound algebraic replacement, for
example a kernel/image computation from a finite presentation, quotient-first
Schreier calculation, or a generator-invariant orbit test.  Early discovery
of a zero is useful only if the emptiness proof is complete; sampling,
timeouts, Bloom filters, and incomplete BFS are forbidden.

## Deliverable

Write `sol/luna_reply_157by_q5_exact_acceleration.md` with:

1. an exact description of the current bottleneck;
2. the strongest sound acceleration you can actually justify;
3. a proof that its computed fiber is the complete fiber (or a fail-closed
   statement that no acceleration was established);
4. estimated state counts and which active specialization/joint lane benefits;
5. a terminal marker `Q5_EXACT_ACCELERATION_READY` or
   `Q5_EXACT_ACCELERATION_BLOCKED`.

If and only if the speedup is fully justified, you may also create these new,
versioned files:

- `search/d972_b4_burau_accel_v1.py`
- `search/check_d972_b4_burau_accel_v1.py`
- `.github/workflows/d972-burau-accel-v1.yml`

They must have independent producer/checker logic, negative selftests,
fail-closed hash gates, bounded memory, and evidence upload.  Do not alter any
existing producer/checker/workflow.  Do not dispatch GHA and do not run GAP or
any heavy local enumeration.  Lightweight static/selftests are allowed.

## File and git discipline

Only the reply and the three optional new files above may be changed.  Do not
run git operations.  The parent is the sole broker.
