# Task388 independent static code/performance reaudit -- pre-A0 A3/v5

## 0. Decisive result

**STATIC REJECT.**  The frozen identities, bounded v5-to-v4 delta, P0 and
authority graph, live evaluator route, v303 projection, one closure/one
independent verifier, baseline plus twelve mutations, duplicate-pass removal,
receipt-digest transport, GAP `Process` status gate, and the numerical
performance caps all pass static inspection.

The remaining defect is in the final sentinel admission.  The shell helper can
successfully create, fsync and close the sentinel and return zero; after GAP has
accepted that zero status, driver lines 242--244 perform a new fallible
`StringFile`/identity gate.  Failure of that gate calls neither dirfd-relative
unlink nor output-directory fsync.  Thus an exact, already durable sentinel can
survive a post-create failure.  This violates task388 Section 5's requirements
that every post-create failure roll back and that no fallible admission gate
remain after the publication terminal.  This trace is nonaccepting for the
current invocation, but it is not a durable rollback and therefore forbids the
candidate run.

I read task363, task369/reply369, task370/reply370, task374/reply374,
task377/reply377, task381/reply381, task384/reply384, v302, v303, the P0, all
23 recursively named authorities, all four frozen task388 subjects, and the
installed GAP 4.16 `process.gd`/`process.gi` definitions.  No candidate or
executable program was run.

## 1. Frozen physical owners, P0, and reverse delta

The four subjects match the task envelope exactly:

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_pre_a0_single_target_a3_v5.py` | 104,446 | `4fbbd5792a1d1cc7bb1c3d534bdc0966291751cc9d3cea99d1ed20ca7d70fecb` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v5.py` | 116,872 | `90838f12061783c77651c656f7bd1a572ca4a687339b5b70747342d18d32028a` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v5.g` | 18,597 | `0465b46a734048b4ef6c16ed079e7daf825f71407f8cfe1b969a648ffb936d27` |
| `sol/sol_reply_384_r07_pre_a0_a3_v5_driver_performance_repair.md` | 16,209 | `1dd63647ad95a54e1ee09e62550386e795f5b5e5f9d510966dee68c4b17a6a6c` |

The three machine owners are ASCII, LF-only, final-LF files.  The compact P0
is exactly 16,417 ASCII bytes, has neither BOM nor CR/LF, begins with `{`, ends
with `}`, and has SHA-256
`14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae`.
Removing its single top-level 88-byte self-seal pair leaves 16,329 bytes whose
SHA-256 is
`f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7`.

Recursive collection under `authority` gives exactly 23 occurrences, 23
unique normalized paths, and 33,121,619 bytes.  The sorted paths equal the
declared inventory, its count and byte sum agree, and every present physical
owner matches its declared size and SHA-256.  No candidate producer/checker,
driver, or P0 path occurs below the authority root, so the graph remains

`immutable authorities -> P0 -> producer/checker -> driver`.

I reversed the complete line hunks in memory and compared the reconstructed
bytes, not merely labels or hashes:

| reverse target | lines v4 -> v5 | minimal line edit | reconstructed v4 bytes | reconstructed v4 SHA-256 | exact |
|---|---:|---:|---:|---|---|
| producer | 2,322 -> 2,323 | -12 / +13 | 104,369 | `171e73dab2bd27f638021ceea43d8fb96ec4623a13d45873f364114e4290badd` | yes |
| checker | 2,469 -> 2,492 | -22 / +45 | 115,675 | `eb07e34164f27b6676b97c722fb0fb2ef87b1e971baaab3d18c26770f17b7804` | yes |
| driver | 240 -> 245 | -81 / +86 | 20,111 | `78ee39b6f8926c267cb24d6b15bdc3a961906cdb8ddf9de8f7668222a5113f91` | yes |

The producer delta is confined to truthful v5 labels/schema/path/module
names, three RLIMIT readback lines, and removal of the two immediate source
rehashes.  The checker adds only the corresponding labels/readback/removals
and typed authenticated-receipt-SHA transport through normal and UNKNOWN
construction.  The driver delta consists of v5 paths/pins/schema labels,
deletion of the old full pre-checker helper and `rsha2`, consolidation of the
final helper, the exact-bash `Process` gate, and the new sentinel error
retention.  Reversing those regions alone recovers the frozen v4 bytes.

## 2. Retained mathematical and authority route

The 31,017,244-byte accepted task198 receipt is physically read and hashed in
the 23-owner sweep, then has exactly one large DOM parse, one streaming
canonical comparison, and one body-seal traversal in each process.  The later
ordinary raw-owner mutation re-enters the same validator using the real
2,722-byte manifest and does not parse, hash, canonicalize, or seal the large
receipt again.

Producer lines 1249--1318 and checker lines 1450--1509 each build one live
task198 evaluator from the pinned task176/task198 support.  Both directly call
`eval` three times, `inverse` twice, and `multiply`, `source_section`, `action`,
and `section_cocycle` once.  Producer transitive counts are
`eval=6,inverse=3,multiply=4` plus the three single calls; the independent
checker route has `eval=8,inverse=3,multiply=4` plus those same single calls.
Both bind all eleven signs, orientations, ten-indices and 40/154-byte typed
coordinates.  Checker `EvaluatorBudget.check` calls the existing
`Meter.check` directly at lines 1440--1442, with no broad UNKNOWN conversion.

The task226 producer `specialize(g760, [], rows)` and independent checker
`reconstruct(g760, [], rows)` build the computational base once.  Projection
construction retains only the explicit v303 interface: ledger, quotient
arithmetic, occurrence `p_o/xi_o/w_o/u0`, combined `w/u0`, and the three
base targets.  Full-package fields such as corrected `f`, `rword_f`, `B_a`,
and exact PB chains are not asserted equal to an unknown A0 package.  All
eight conclusion flags, including `actual_a3_numerator`, remain false.

Producer lines 2204--2217 contain the sole task227 closure call and require
the exact 486/729 post-call rosters.  Checker lines 2302--2313 contain the sole
independent `verify_gate` call; frozen task227 then performs its twelve directed
span comparisons and validates rank/echelon/ancestry/replay-or-dual evidence.
There is no wrapper reverse comparison or second closure/verifier.

Producer lines 1773--1938 and checker lines 1714--1877 preserve an untouched
ordinary baseline and exactly the P0 roster of twelve owner-local mutations:
raw task198 manifest binding, ledger sign, prefix, g760 digest,
computational-base mode, forbidden task192 binding, H1/H2/P central row,
projected target, ABI seal/target, and forbidden conclusion flag.  Each changes
the smallest selected list/dict owner, proves before/after digest inequality,
uses its ordinary validator, narrowly maps the expected first reason, and
hard-fails acceptance or a wrong reason.  No receipt/P0/full ABI/interface
deep clone or per-mutation closure is present.

## 3. Pass consolidation and static performance

For each dynamically imported source, `read_bytes` performs the physical
regular/non-symlink size and SHA check.  `load_engine` then has an authenticated
pre-read, one `compile`/`exec` into one fresh module, and an authenticated
physical post-read.  The initial authority sweep is separate and retained;
the two import-boundary reads remain the required TOCTOU pair.  The removed
immediate hashes do not remove either read, source pin, deadline, import
counter, or module build.

The producer's six source pins sum to 894,133 bytes, so its two removed
in-memory passes save exactly 1,788,266 hashed bytes.  The checker's seven pins
sum to 1,450,252 bytes, saving exactly 2,900,504 hashed bytes.  Checker
`read_receipt` lines 1909--1940 performs one physical receipt SHA at line 1929,
then canonical/body-seal/schema authentication and returns that typed digest.
`verdict_document` lines 2095--2114 requires lowercase 64-hex typing and exact
equality with the driver pin whenever receipt bytes are present; normal and
post-read UNKNOWN paths carry the same value, while an unavailable/unreturned
receipt is forced to bytes-empty/digest-`None`.  No verdict-population receipt
rehash or producer digest summary is used.

Let `R` be the future canonical receipt length, `0 < R <= 19,000,000`.  Driver
lines 96--102 retain only owner/type/size and one injected streaming SHA before
the checker.  The final helper retains the sole driver receipt parse,
canonical/body-seal pass, complete P0/23-owner/projection/evaluator/mutation/
rank/resource gates, and its in-memory receipt/verdict hashes; lines 166--169
retain the required post-validation physical rehashes.  The deleted work is

`1,788,266 + 2,900,504 + R + (2R-88) + R = 4,688,682 + 4R`,

at most 80,688,682 enumerated hashed/serialized bytes, plus the separately
removed pre-helper `R`-byte read and DOM parse.

Remaining component formulas independently recompute as follows:

| component | exact formula / bound |
|---|---:|
| P0 plus 23 authorities | `16,417+33,121,619 = 33,138,036 < 40,000,000` |
| producer input | `16,417+33,121,619+2*894,133 = 34,926,302 < 60,000,000` |
| checker before receipt | `16,417+33,121,619+2*1,450,252 = 36,038,540` |
| checker with maximum receipt | `36,038,540+19,000,000 = 55,038,540 < 60,000,000` |
| producer normal serializer component | `3*19,000,000+65,536 = 57,065,536` |
| producer failed-normal plus emergency charge | `57,065,536+4*65,536 = 57,327,680` |
| checker verdict serializer component | `3*1,000,000+65,536 = 3,065,536` |
| evaluator build operations | `26+243*26+59,049*6+243*10 = 363,068 < 1,000,000` |
| checker private Q0 retained bytes | `5*1,469,664 = 7,348,320` |
| checker Q0 construction component peak | `2*7,348,320 = 14,696,640` |
| required address-space ceiling | 4,294,967,296 requested bytes, exact installed target read back |
| walls | `1,800 < 2,100`; `2*2,100 = 4,200 < 21,600` seconds |

The large raw map and one task198 DOM coexist only through snapshot creation
and are released before task226/closure or verifier work.  At an import post
boundary only the current pre/post source byte objects and its single compiled
module coexist.  The checker deliberately constructs and releases the private
Q0 transient before reading the produced receipt; this ordering avoids
overlapping the 14,696,640-byte construction component with an up-to-19-MB
receipt DOM and is not a duplicate receipt pass.  Receipt-side live objects are
one `R`-byte raw, one DOM, one shallow seal dictionary, and one at-most-65,536-
byte canonical chunk.  The driver final helper holds at most the receipt,
1,000,000-byte verdict and 16,417-byte P0 raws/DOMs and reads one authority at
a time.

All data-dependent Python work is under the elapsed-adjusted 1,800-second outer
deadline and nested timers.  Closure/rank/roster/mutation/module counts have
explicit caps.  The driver helpers have fixed bounded inputs (one bounded
receipt/verdict, P0 and exactly 23 owners; the sentinel loop has 15 bytes) and
the workflow envelope retains 17,400 seconds beyond the two serial external
candidate bounds.  No second large task198 route, hidden ABI build, closure,
verifier, receipt parse, unbounded collection, quadratic wrapper scan, or
additional avoidable whole-owner pass was found.  These are payload/component
bounds, not observed RSS; Python object and allocator overhead are covered only
by the required Linux RLIMIT_AS ceiling.

## 4. Status-bearing gate and durable-sentinel defect

Installed GAP 4.16 `lib/process.gd` documents the exact signature
`Process(dir, prg, stream-in, stream-out, options)`, states that it waits for
termination and returns the process return value, and declares filters
`[IsDirectory, IsString, IsInputStream, IsOutputStream, IsList]`.
`lib/process.gi`'s input-none/output-text method returns `ExecuteProcess(...)`.

Driver line 2 binds exact `/usr/bin/bash`; lines 37--38 require that exact path
to be executable; lines 236--237 invoke
`Process(DirectoryCurrent(), D363Bash, InputTextNone(), OutputTextUser(),
["--", D363Shell])`.  Lines 238--241 reject a noninteger or every nonzero
(including signalled) status before inspecting the sentinel.  There is no
status-discarding `Exec`, and a sentinel surviving any nonzero helper/bash
status cannot accept.  This status gate itself passes.

Within the helper, lines 170--191 bind root/`ci`/`out` by no-follow directory
fds, exclusively create the fixed basename, loop to all exact bytes, fsync the
file, require file close, and fsync `out`.  Lines 192--232 retain original and
file/root/ci/out close failures; every recorded post-create helper failure
attempts dirfd-relative unlink and directory fsync, retains rollback errors,
prints both classes, and exits 70.  Those in-helper paths are fail-closed.

The complete remaining counterexample is outside that helper:

```text
sentinel helper writes D363_V5_ACCEPTED, fsyncs, closes and exits 0
  -> bash exits 0
  -> GAP Process returns integer 0 and lines 238--241 pass
  -> line 242 StringFile fails, or line 243 sees a nonexact read
  -> GAP Error is raised without sentinel unlink or out-directory fsync
  -> the already created sentinel survives the post-create failure
```

Thus lines 242--244 are a fallible post-terminal admission gate with no durable
cleanup edge.  A bounded repair must either perform exact readback/identity
inside the status-bearing helper before its success return, routing every
failure through the existing unlink+fsync rollback, or add an equally durable
status-bearing cleanup edge for GAP-side admission failure.  Merely relying on
the next invocation's stale-name rejection is not rollback.

## 5. Static-only boundary

This audit used only read-only PowerShell/.NET inspection and hashing and the
single permitted patch that creates this reply.  I did not run Python, Node,
GAP, GHA/workflows, git, network, imports, syntax compilation, candidate code,
mutations, subprocess tests, or RSS measurement.  No frozen owner was edited.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
V5 TO V4 BOUNDED REVERSE DELTA:        PASS
P0 / AUTHORITY / LIVE EVALUATOR:       PASS
V303 / ONE CLOSURE / CHECKER:          PASS
BASELINE + TWELVE MUTATIONS:           PASS
SOURCE / RECEIPT PASS CONSOLIDATION:   PASS
STATUS-BEARING PROCESS GATE:           PASS
DURABLE SENTINEL ROLLBACK:             REJECT
STATIC CAPS / PERFORMANCE:             PASS
AVOIDABLE DUPLICATED PROCESSING:       PASS
PRE-A0 A3/V5 GHA:                      FORBIDDEN
ACTUAL A3 NUMERATOR:                   remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:      NONE

TASK388_R07_PRE_A0_A3_V5_CODE_PERFORMANCE_REAUDIT_V1
