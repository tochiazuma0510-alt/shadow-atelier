# Luna reply 157cd — exact synchronized Burau early acceleration

## Verdict

The versioned synchronized accelerator is ready.  I read all sections of the
157cd instruction and changed only the four authorized files.  No GAP, heavy
local enumeration, Git operation, or GHA dispatch was performed; no run result
is claimed.

Authorized assets:

```text
search/d972_b4_burau_joint_accel_v1.py
search/check_d972_b4_burau_joint_accel_v1.py
.github/workflows/d972-burau-joint-accel-v1.yml
sol/luna_reply_157cd_joint_early_acceleration.md
```

## Exact acceleration and soundness

The producer still constructs one synchronized image of the source pair for
all registered specializations, the exact projected section, the exact joint
kernel, and every cited right fiber `h0*K`.  It retains the complete sorted
`kernel_elements`; no single-lane Cartesian product is used.

The kernel generator list is now extracted during the already exhaustive
single BFS.  Whenever an edge `z -> z*g` discovers a new kernel element, `g`
is recorded in the witness set `W`.  The BFS proves by induction that every
visited vertex is in `<W>`, while every witness is an exact Schreier kernel
relator, so `<W> <= K`.  Therefore `<W>=K`.  The checker independently
rebuilds the joint kernel, reconstructs the same deterministic discovery set,
checks each witness lies in `K`, and recomputes `closure(W)==K`.

The row accelerator stops only after the entire finite fiber for a row has
been evaluated against the complete conjunction

```text
pentagon + H10 + H11 + common CRT-compatible m residue with lambda unit
```

If `full_GT_identity_count == 0`, it writes a contiguous candidate prefix and
the terminal row index.  The checker requires that the terminal row is the
first and last zero row in the prefix and independently replays every cited
fiber.  A partial all-pass receipt is rejected; `UNKNOWN_BURAU_JOINT_ALLPASS`
requires all 972 rows and `row_scan_complete=true`.  Thus the early stop is a
finite obstruction candidate only, not a nonexistence or final B proof.

## Workflow matrix and gates

`.github/workflows/d972-burau-joint-accel-v1.yml` runs the registered compact
matrix in parallel with `fail-fast: false` and a 360-minute job cap:

```text
q3a2_full
q4a2_full
q3a2_q4a2
q3a2_q4a2_q5a2
q3a2_q4a2_q5a4
```

Each job uses Python 3.13.5, hash-pinned SymPy/mpmath, the corrected
`RLIMIT_AS` byte guard (`ulimit -v 12000000` and expected
`12000000*1024`), source/artifact SHA gates, producer and checker self-tests,
the exact receipt scalar/prefix gate, and the independent checker.  Evidence
is uploaded with `always()`.  The workflow never treats `UNKNOWN_RESOURCE` or
an incomplete all-pass receipt as admissible.

## Final SHA-256 bindings

```text
producer  E3E77DE7C328DF792A3A77C1DE3B6BADBE479DC364C120FAA28FEF8D2D8A7404
checker   60599A0092BFF16BF324775AD3A08D647CFA95F6B38516AB02165BB2C566E670
workflow  91C605B7FE893B1EBEADD70988D8D28A59977815EE26F35656C3A555B1F20DC9
words     564A921BE8114BDEB963F679C121E8D9AA90E148C65E95E393874FCBA843E9F9
```

## Lightweight checks

All passed without GAP or heavy enumeration:

```text
AST_PASS
YAML_PARSE_PASS
WORKFLOW_SOURCE_HASH_BINDING_PASS
D972_B4_BURAU_JOINT_ACCEL_SELFTEST_PASS
D972_B4_BURAU_JOINT_ACCEL_CHECKER_FINAL_MARKER status=PASS
D972_B4_BURAU_JOINT_ACCEL_DISCOVERY_WITNESS_PASS
D972_B4_BURAU_JOINT_ACCEL_PARTIAL_ALLPASS_NEGATIVE_PASS
```

The candidate status remains subject to parent audit; all-pass remains
nonterminal.

JOINT_EARLY_ACCELERATION_READY
