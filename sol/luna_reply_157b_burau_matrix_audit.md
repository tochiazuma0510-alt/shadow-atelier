# Luna reply 157b — independent matrix-56 audit

## Verdict: PASS

Task 157e closes the sole 157b blocker.  The workflow now lists the producer,
word artifact, worker, and every helper directly read by the worker prefix in
`on.push.paths` (`.github/workflows/d972-burau-matrix-v1.yml:3-15`), while
retaining the exact branch and the original three trigger paths.  The producer
still loads exactly that worker prefix (`search/d972_b4_burau_matrix_v1.g:35-40`);
the four transitive reads are `search/d972_dovetail_worker_v1.g:18-21`.

The prime-field receipt encoder is now explicitly `IntFFE(x)`
(`search/d972_b4_burau_matrix_v1.g:81-84`); the GF(4) `0,1,Z(4),Z(4)^2`
branch is unchanged.  The environment parser's `Int(x)` at `:12-14` is
unrelated and correctly remains a string-to-integer conversion.

No unrelated semantic or workflow change is visible: the producer remains 165
lines with the single encoder-token repair, and the workflow retains its prior
body with only the five trigger paths inserted (now 199 lines).

## Positive static findings

- The producer constructs a 36-point permutation-matrix block plus five 4x4
  blocks, dimension 56 (`search/d972_b4_burau_matrix_v1.g:56-73,
  122-124`); the row-action canary checks
  `R(p*q)=R(p)*R(q)` (`:89-98`).  No vector-point action or projectivization
  is present.
- The Burau field helper agrees with the audited v2 encoding
  (`:53-60`, compared with `search/d972_b4_burau_fiber_v2.g:77-93`); the
  explicit GF(4) branch handles `0,1,Z(4),Z(4)^2`, while the prime-field
  branch uses documented `IntFFE(x)` for q=3 or q=5 (`:81-84`).
- The five pair blocks and reversed `PaperProd` defect agree with v2
  (`:115-121, :85`; v2 `:190-200, :130-133`).  The selftest includes Artin,
  determinant, orientation, block-extraction, reversed-conjugate, reversed
  product, and swapped-defect controls (`:89-100`).
- `H`, `H'`, the restricted roof homomorphism, image-surjectivity, exact
  `Kernel`, complete `Elements(K)` enumeration, distinctness, and first-block
  identity are explicit (`:125-134`).  No q5 H/H'/K/fiber constants are used;
  the only hard-coded orders are the frozen roof orders (`:127-131`), while
  q3/q4 calibration constants are scoped under `D972MMode="calibration"`
  (`:157-162`).
- All 972 words are replayed, target keys are checked and unique, each row
  gets an exact `H'` preimage and full right coset by the enumerated kernel,
  and all five blocks are defect-scanned (`:136-155`).  The status logic is
  candidate-only for a zero identity fiber and UNKNOWN for all-pass or an
  incomplete/resource outcome (`:156-164`).
- The workflow gates q3/q4 calibration before q5 (`:108-116`), runs q5 a=2
  and a=4 as independent `fail-fast:false` matrix cells (`:113-117`), runs
  selftest before full execution in every cell (`:66-99, :155-187`), captures
  `PIPESTATUS`, rejects GAP diagnostics, checks exact markers, uses
  `persist-credentials: false`, six-hour timeouts, and a 12GB virtual-memory
  ceiling (`:17-30, :36-54, :74-99, :111-121, :127-187`).  Artifact names are
  attempt-unique (`:100-106, :188-194`).

## Static evidence and remaining runtime uncertainty

- YAML parse: PASS (`name=d972-burau-matrix-v1`, jobs `calibrate,matrix56`).
  The parser's YAML 1.1 representation of `on` as a boolean was inspected and
  contains the expected push branch/path map; this is normal PyYAML behavior,
  not a workflow defect.
- `PATH_CLOSURE_AND_INTFFE_PASS`: all eight retained/required trigger paths
  are present, all four worker-prefix `Read(...)` paths exist on disk, and the
  receipt encoder contains `IntFFE(x)` with the GF(4) branch intact.
- Frozen word artifact: SHA-256
  `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`;
  JSON schema/count/972 rows and 972 unique keys agree with producer constants
  (`:26-33, :106-107, :136-141`).
- Matrix producer SHA-256:
  `3eb4975ed2b5721634868004cf3b1b7db25b3d709da5679e891054765f0bd728`.
  Workflow SHA-256:
  `e4dba1a160852b22392f8ebc96e9df9a76e8d45730db9030d564bd37b7d7ce4b`.
  Replacing only `IntFFE(x)` by the former `Int(x)` reconstructs the prior
  producer SHA `92ece7f5531438c69aa6d0cd2933b6f2fa2013804ec435ce53ff4344fafbf41e`;
  removing exactly the five new trigger lines reconstructs the prior workflow
  SHA `cc28b6373066a76ec5d536e7e76c57d5c94205e397bc6e1983f7bbcac9f2dfab`.
  This is an exact static confirmation that no unrelated semantic/workflow
  diff was introduced.
  Both files have no trailing whitespace.  A static authorized-file diff
  check found only the five workflow paths and the `IntFFE` token change;
  `git diff --check` was not rerun in this re-audit per task instructions.
- No local GAP, git, or full computation was run.  GAP 4.16 behavior/resource use
  for matrix-group construction, `GroupHomomorphismByImages`,
  `DerivedSubgroup`, exact `Kernel`/`Elements`, and all 972 coset scans remains
  runtime uncertainty.  The workflow's exit/diagnostic/marker gates make such
  failures nonterminal.  The workflow checks only receipt nonemptiness
  (`:99`, `:187`); schema validity is statically supplied by the producer's
  deterministic serializer/receipt fields (`:42-51, :150-163`) rather than an
  independent runtime JSON checker.

With the 157e repair applied, the files are suitable for the parent's exact
campaign launch; this audit makes no A/B claim and treats a q5 all-pass as
UNKNOWN.
