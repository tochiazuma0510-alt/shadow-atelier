# Luna reply 157by - exact q5 obstruction acceleration

## Result and scope

I read the complete 157by instruction.  I inspected the v4 and v5 single-
specialization producers and the synchronized joint-v1/v2 producers, together
with their independent checkers.  I did not run GAP, a heavy enumeration, Git,
or a GHA dispatch, and I did not modify any existing producer, checker, or
workflow.

The strongest sound acceleration is an exact single-BFS Schreier-witness
extraction.  It removes the repeated exact kernel closures used only to
reduce the kernel-generator list without changing the kernel, the 972 fibers,
or the terminal predicate.  I implemented it as a new versioned bundle; no
existing producer, checker, or workflow was changed, and no receipt is being
represented as run or checked.

## 1. Current bottleneck

The v4/v5 code has two different exact costs.

1. `complete_hprime` first performs `exact_section` over the projected
   derived roof.  The frozen constants are

   ```text
   |P|  = 1,469,664
   |P'| =   367,416
   ```

   For every normal-closure round it constructs the full
   Reidemeister-Schreier edge-relator set and runs `enumerate_kernel` to
   closure.  The edge count in a round is
   `367,416 * 2 * hprime_generator_count`; the synchronized producers do the
   same traversal with five blocks per registered specialization.  This is
   the principal image/derived-image cost and cannot be replaced by a sample.

2. Once the exact kernel `K` is available, `run_full` reconstructs each of all
   972 right fibers as `h0*K` and evaluates `matrix_defect` on every element.
   Thus this part costs exactly `972 * |K|` defect evaluations.  The q3/q4
   calibration has `|K|=8`, i.e. 7,776 evaluations.  The historical q5/a4
   matrix receipt records `|K|=15,000`, which would be 14,580,000 exact
   evaluations.  A synchronized lane has the same formula with its actual
   joint-kernel order; no Cartesian product assumption is involved.

There is also an avoidable secondary cost after the row scan.  The producers
call `reduce_kernel_generators(schreier_relators, ...)`.  For each selected
relator this calls `enumerate_kernel` again, even though the preceding exact
enumeration has already computed all of `K`.  `quotient_cosets` is not the
dominant cost in the calibrated lane: its quotient order is 36.

## 2. Sound acceleration: witnesses from the existing exact BFS

The Reidemeister-Schreier relators `R` already generate the complete matrix
kernel.  The new producer changes only the exact enumeration routine in its
versioned copy so that it records a witness label whenever a BFS edge
discovers a new element:

```text
V := {1}; queue := [1]; W := empty set
while queue is nonempty:
    g := pop(queue)
    for r in R union R^{-1}:
        z := g*r
        if z not in V:
            add z to V and queue
            add r to W
return (V, W)
```

Use `W` as `kernel_generators` and do not call
`reduce_kernel_generators`.  The `V` returned by this same BFS remains the
serialized complete `kernel_elements` list.  Deduplicating `W` is optional;
it is useful for keeping the receipt compact.

This is not a heuristic generating-set guess.  Every discovered vertex has a
BFS path whose edge labels are in `W`, by induction on its discovery time;
hence `V` is contained in `<W>`.  Conversely `W` consists of relators, so
`<W>` is contained in `<R>`.  The exhaustive signed-generator BFS has
`V=<R>=K`, therefore `<W>=K`.  The extra work is only recording labels on the
already-required exact BFS.  It removes the repeated closure BFSes from the
current reduction stage while retaining bounded state of the same order as
the existing relator set and kernel enumeration.

The current independent checkers already have the required fail-closed gate:
they check every supplied kernel generator is in the independently rebuilt
`K`, then recompute its exact closure and require that closure to equal `K`.
This is present in the v4/v5 checkers and in both joint checkers.  Thus the
new witness list cannot make an incomplete fiber pass.

The speedup is especially relevant to q5 (and q7) single-specialization
lanes and to joint-v1/v2 lanes whose kernels are larger than the q3/q4
calibration kernel.  It does not remove the exact `|P'|` section traversal or
the `972*|K|` nonlinear defect scan.  I found no justified homomorphism or
quotient identity for `matrix_defect` that would permit replacing that scan
by a histogram or an early zero test: the defect is a five-block word with
inverses, and its value on `h0*k` is not a homomorphic image of `k`.

For the q5/q7 candidate path, the producer additionally stops immediately
after a fully scanned fiber with zero identity defects.  The receipt marks
`row_scan_complete=false`, records the contiguous prefix and the terminal
zero-row index, and never presents that prefix as an all-pass result.  The
independent checker reconstructs `K` and recomputes every cited prefix fiber;
it accepts a partial ledger only for a candidate whose final cited row is the
unique zero row.  An all-pass receipt still requires all 972 rows.  This is a
complete witness of existence, not an incomplete nonexistence claim.

## 3. Complete-fiber proof and fail-closed boundary

Let `pi:H' -> P'` be the roof projection, let `sec` be the exact section
constructed by `exact_section`, and let `K=ker(pi)`.  For a replayed row with
roof `r`, the producer takes `h0=sec[r]`.  Every element `h` above `r` has

```text
k = h0^{-1} h in K,       h = h0 k,
```

and this `k` is unique.  The exhaustive `V` BFS enumerates every element of
`K`, so `sorted(h0*k for k in V)` is exactly the full finite fiber.  The
witness-list change affects only generator metadata and never weakens `V`.
The candidate-only row stop is allowed only after that complete cited fiber
has been scanned; it is not an early acceptance of an untested fiber.  A
versioned checker must retain the existing equality test `closure(W)==K`, and
must reject missing kernel elements, roof drift, source/hash drift, invalid
row prefixes, or an incomplete section.  No sampling, timeout acceptance,
word bound, or Bloom filter is used.

## 4. Versioned implementation

The authorized new files are:

```text
search/d972_b4_burau_accel_v1.py
search/check_d972_b4_burau_accel_v1.py
.github/workflows/d972-burau-accel-v1.yml
```

The workflow runs q5/a2 and q5/a4 as a `fail-fast: false` matrix.  Each job
pins the existing q3/q4 artifact IDs, names, sizes, run ID, JSON SHA-256,
legacy v4 producer/checker hashes, and calibration metadata before invoking
the new producer.  Both calibrations are rechecked with the legacy
independent checker, then the new checker independently reconstructs the q5
roof, exact kernel, every cited fiber, and the witness-generator closure.
The workflow uploads `ci/in` and `ci/out` even on failure.  Source hashes in
the workflow are fail-closed and were refreshed after the final edits:

```text
producer  fe9ee097c50a54ffc69ce9bcb820e7ac09847581eb82a3dd2d83962aab69e2dc
checker   e36405fafb75ea3eaf096e507920b9d2ebe683e867a49a35c8f1bdcb708a0c7a
workflow aad5feadd26687be0d84ac85ab9cacfc6ae211b5bec74f83f2029888a1bab1e9
```

The checker also has a negative contract test proving that a partial
all-pass ledger is rejected while a terminal candidate prefix is admissible.

## 5. Static checks and state accounting

The following lightweight checks passed without invoking GAP or a heavy
producer enumeration:

```text
AST_PARSE_AND_EXACT_PIPELINE_PASS
  d972_b4_burau_fiber_v4.py
  d972_b4_burau_fiber_v5.py
  d972_b4_burau_joint_v1.py
  d972_b4_burau_joint_v2.py

ACCEL_PRODUCER_AND_CHECKER_AST_PARSE_PASS
  d972_b4_burau_accel_v1.py
  check_d972_b4_burau_accel_v1.py

ACCEL_WORKFLOW_YAML_PARSE_PASS
ACCEL_WORKFLOW_EMBEDDED_PYTHON_COMPILE_PASS (3 blocks)

D972_B4_BURAU_ACCEL_V1_SELFTEST_PASS
D972_B4_BURAU_ACCEL_CHECKER_SELFTEST_PASS

GENERATOR_CLOSURE_GATE_PASS
  check_d972_b4_burau_fiber_v5.py

SINGLE_BFS_WITNESS_GENERATOR_PASS
  producer bounded C2xC2 tuple replay: |V|=4, <W>=V

D972_B4_BURAU_ACCEL_PARTIAL_ALLPASS_NEGATIVE_PASS
  checker rejects partial all-pass and accepts only candidate partial scans
```

The exact current state counts used above are `367,416` projected section
states, 972 frozen rows, calibration `|K|=8`, quotient order 36, and the
historical q5/a4 `|K|=15,000` record.  For any new joint specialization the
kernel count must be read from that run; it must not be estimated by
multiplying independent specialization kernels.

No GHA result is claimed.  The new workflow is ready for the parent to
commit/push and dispatch; existing lanes remain untouched.

Q5_EXACT_ACCELERATION_READY
