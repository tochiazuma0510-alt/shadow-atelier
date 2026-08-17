# Luna reply 157cg: adversarial audit of synchronized Burau accelerator

## Verdict

JOINT_ACCEL_AUDIT_PASS

I read the complete 157cg instruction and both 157cd files.  I audited only

    search/d972_b4_burau_joint_accel_v1.py
    search/check_d972_b4_burau_joint_accel_v1.py
    .github/workflows/d972-burau-joint-accel-v1.yml

No GAP, heavy local enumeration, Git, or GHA was run.  No bundle file was
modified.  This is an authorization for the parent to commit/dispatch only;
it is not an A/B result.

## Exact file and artifact bindings

The current SHA-256 values, recomputed from the working tree, are:

    producer  e3e77de7c328df792a3a77c1de3b6badbe479dc364c120faa28fef8d2d8a7404
    checker   60599a0092bff16bf324775ad3a08d647cfa95f6b38516ab02165bb2c566e670
    workflow  91c605b7fe893b1ebeadd70988d8d28a59977815ee26f35656c3a555b1f20dc9
    words     564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9

The workflow pins the producer, checker, and word-artifact hashes at lines
18--20 and independently checks those three paths at lines 61--70.  The
producer and checker also enforce the word file schema/count 972 and its
canonical, target, and tuple digests (producer lines 281--306; checker lines
272--290).  The embedded artifact constants are:

    artifact rows  283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930
    target         9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
    frozen tuple   32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
    semantic       3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729

All referenced source/certificate paths exist.  The checker is standalone:
it imports no producer or helper module (checker lines 1--5 and 13--20) and
rebuilds the synchronized image itself.

## Exact joint kernel and witnesses

The producer's section and normal-closure route is exact.  The signed
Schreier section and relator construction are at lines 560--587; the kernel
BFS at lines 590--608 runs until its queue is empty, with no sampling, word
bound, timeout, or Bloom filter.  `complete_hprime` (lines 629--660) rejects
projection overflow, requires the full P' order 367416, and iterates the
normal closure before returning.

Each discovery edge label is retained as a witness (lines 590--608).  The
discovery induction gives every visited kernel element as a product of prior
witnesses, while each witness is an exact kernel relator.  The receipt keeps
both the complete `kernel_elements` and the witness list (lines 970--979),
and explicitly records one synchronized image, no Cartesian product, and no
word bound (lines 946--965).

The checker independently repeats section/relator construction and BFS at
lines 490--555 and 557--579.  It checks the serialized kernel length and
ordered contents (lines 797--800), verifies witness membership and
`closure(witnesses)==K` (lines 801--812), and checks the exact-kernel canary
(lines 813--820).  Thus an incomplete K, incomplete witness set, or
unsynchronized Cartesian replacement cannot pass.

## Pentagon, H10/H11, and common m semantics

The producer computes the A.18 defect per synchronized specialization and
uses the full conjunction in the fiber loop (lines 809--829 and 870--917):

    pentagon AND H10 AND H11 AND a common CRT/unit-m witness.

`m_compatibility` enumerates every residue congruent to the source m modulo
18 in the lcm with `ord(y)`, then applies the stated gcd/unit gate (lines
764--786).  `hexagon_status` intersects the valid residue sets across all
registered specializations (lines 809--829), so a pentagon-only zero is not
treated as a full-GT zero.  `full_GT_identity_count` is incremented only when
all three matrix predicates and a nonempty common residue set hold (lines
881--906).  The independent checker repeats this logic at lines 645--701
and 868--895, including the serialized m-witness prefix.

The candidate stop occurs only after the whole `h0*K` fiber has been checked:
the producer stops on `full_count == 0` at lines 918--929.  A pentagon-only
zero with positive full count therefore cannot trigger the stop.  The
checker requires the only full zero to be the final row of the prefix at
lines 847--907; missing, duplicated, or earlier terminal-zero rows fail.
The full-GT witness-prefix helper and negative cases are at producer lines
699--710 and 1058--1073, with the independent copy at checker lines 716--721.

## Receipt and scan gates

`row_scan_contract` requires either a complete 972-row all-pass receipt with
no terminal row, or a contiguous candidate prefix whose last row is the
terminal zero (producer lines 712--727; checker lines 731--741).  The
checker replays every cited source word, roof key, representative, complete
right fiber, digest, defect, H10/H11 count, full count, and witness prefix
(checker lines 843--895).  It then rejects duplicate/incomplete prefixes and
enforces the candidate/all-pass dichotomy (lines 897--907).  All-pass is
therefore never accepted from a partial scan.

## Bounded hostile mutations

The producer and independent checker self-tests both passed.  Their explicit
fixtures cover incomplete witness/K closure, partial all-pass, missing
candidate terminal zero, short all-pass, source-word/roof-key mutation,
product/A.18 mutation, omitted-H10 mutation, unsynchronized Cartesian fibers,
config substitution, and corrupt/status-disagreement receipts (producer
lines 1039--1121; checker lines 946--1010).  I additionally replayed bounded
mutations without creating repository files:

    JOINT_ACCEL_BOUNDED_MUTATION_PASS
    PRODUCER_CHECKER_CONFIG_BINDING_PASS 14

The direct checks included: pentagon-only witness omission, positive full-GT
prefix serialization, candidate/all-pass scan mutations, q3/q4 config swap,
and a one-byte source-hash drift.  The checker source-hash gate is at lines
750--751, and the workflow scalar/status gates are at lines 91--127.

## Workflow and resource audit

YAML parsing passed; both Python files passed AST parsing.  The two embedded
Python here-documents compiled successfully.  The Windows audit environment
has no `bash` executable, so `bash -n` could not be run; shell quoting,
`set -euo pipefail`, `PIPESTATUS`, and marker/error control flow were checked
manually.

The workflow has the requested five registered matrix entries at lines
29--35, `fail-fast: false` and a 360-minute cap at lines 25--27.  It installs
hash-pinned SymPy/mpmath, checks Python/SymPy and the 12,000,000-KiB virtual
memory guard (lines 48--57), runs both self-tests, requires exactly the
producer/checker markers, rejects `UNKNOWN_RESOURCE` and partial all-pass,
and independently checks every receipt (lines 73--127).  The checker marker
is required at line 127.  Evidence uploads use `if: always()` at lines
130--135, so failure diagnostics are retained.

The matrix is only the pre-registered q3/q4/q5 set from 157cd:

    q3a2_full
    q4a2_full
    q3a2_q4a2
    q3a2_q4a2_q5a2
    q3a2_q4a2_q5a4

No unregistered production field or parameter was added.  The producer's
additional q2/q7 configurations are audited and self-tested but are not
silently inserted into the workflow matrix.

JOINT_ACCEL_AUDIT_PASS
