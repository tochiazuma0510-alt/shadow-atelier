# Luna 152 — B4-B global audit (2026-08-16)

## Verdict

`B4_STATUS=UNKNOWN_NO_TERMINAL_GLOBAL_CERTIFICATE`.

I found no completed global proof that the 972 norm words are identities in
`U_M`, and no nonidentity norm in a sound finite quotient (therefore no A
candidate).  The finite-image, low-index, and bounded p-quotient all-pass
lanes remain necessary tests only.  I did not promote any of them to B.

## Exact global route and gates

The intended presentation is

```text
U_M = K(0,5) / << rho^i(j(r)) : r in R_Q0, i=0,...,4 >>,
j(x)=X12, j(y)=X23.
```

The audited universal source `search/d972_b4_universal_v2.g` constructs this
presentation from the marked pure `Q0` presentation, not from an unmarked
surrogate:

- `|Q0|=1,469,664`, two marked generators, and 28 Q0 relators (lines 92–100);
- K05 relators are loaded and rho is checked on them, including rho^5 (lines
  102–129);
- the five coface pairs are the rho orbit
  `[(X12,X23),(X45,X51),(X23,X34),(X51,X12),(X34,X45)]` (lines 131–158);
- the quotient has 18 K05 relators plus `5*28=140` rho-closed coface images,
  hence 158 total (lines 153–164), with coface containment and rho descent
  checked (lines 166–184);
- the complete roof count is guarded at 972 (line 189).

The exact word/relator artifacts from GHA run `31917195213` independently
bind the same input:

```text
d972_b4_word_key_artifact_v1.json
  schema d972-b4-word-key-artifact/v1, count 972
  source target-key digest 9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
  frozen tuple digest       32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
  raw rows digest           12675f6f5223806cab1af4b7e08386122b5013bdbda0b7490359992082b85929

d972_b4_u_relators_v1.json
  schema d972-b4-u-relators/v1, count 158
  relator digest            12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e
```

The word artifact has exactly the two known GAP empty-list serialization
rows, 0-based indices `0` (`m=0`) and `891` (`m=17`), encoded as `""`.  An
in-memory normalization of only those two rows gives normalized-row digest
`283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`; the
independent checker `search/check_d972_b4_word_key_artifact_v1.py` then
recomputed all 972 marked keys and returned:

```text
PASS_UNPINNED, count=972,
frozen_tuple_sha256=32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
```

The corrected artifact still needs to be regenerated for a final proof; the
legacy artifact is suitable only for this exploratory audit.

Crucially, the roof rows are not automatically relators of `U_M`.  The worker
enumerates `f` in `DerivedSubgroup(Q0)` (`search/d972_dovetail_worker_v1.g`
lines 451–473), then obtains one F2 preimage (`search/d972_b4_universal_v2.g`
lines 187–217).  A Q0 element in `[Q0,Q0]` is generally not in
`M_F=ker(F2 -> Q0)`.  Thus the coface relators kill the Q0 presentation
kernel, not each of the 972 shadow representatives; no tautological B
argument is available.

## Why the current proof channels do not close B

1. **KBMAG.** The source calls `KnuthBendix` and tests `IsConfluent`, but it
   hard-caps equations, states, word differences, stored lengths, and roof
   reduction time (`search/d972_b4_kbmag_v1.g` lines 41–46, 119–126, 144–167).
   Its terminal labels are explicitly candidate-only and require an
   independent replay (lines 167–186).  More seriously, v1 is not even the
   right word problem: `D972KBToUWord` maps the second F2 letter to U2 and
   reduces the representative directly; it never forms the rho norm.  Thus
   any v1 all-pass is mathematically invalid for B4-B.

   I added the repaired versioned lane
   `search/d972_b4_kbmag_v2.g`, plus the non-sharing constructor/checker
   `search/d972_b4_kbmag_v2.py` and
   `search/check_d972_b4_kbmag_v2.py`.  v2 maps F2 letters as
   `1 -> U1`, `2 -> U4`, constructs the exact six-generator word
   `rho^4(j(f))*...*rho(j(f))*j(f)`, and binds the independently reproduced
   972-word digest
   `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`.
   The Python constructor and independent checker both pass on the normalized
   artifact, with normalized-row digest
   `283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`.
   v2 remains bounded/candidate-only; no completed confluent system or
   972-word reduction receipt exists, and no local GAP run was launched.
   The no-GAP cross-check command returned `RC=0` with
   `status=ROOF_NORM_CROSSCHECKED_RECEIPT_BOUND`,
   `roof_norm_words_sha256=ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`,
   and `old_direct_f2_mapper_absent=true` for v2.
   The v2 source SHA at this audit is
   `7e8af274ebf1fd1ba91bb05273b2118b1d77db020fdcac1317dfffe35230626`.

2. **Universal presentation.** The source deliberately sets
   `B4Finite := false`, computes only `AbelianInvariants(B4UMfp)`, and emits
   `UNKNOWN_U_FINITE_UNCHECKED` (lines 196–210).  The finite abelian image is
   only `U_M^ab ~= (C2)^5`; it cannot imply that `U_M` itself is finite or
   that commutator norm words vanish.

3. **P-quotient / finite-image lanes.** `search/d972_b4_pquotient_v1.g`
   scans finite groups and p-central classes 1–5 (lines 125, 270–309), with
   collector failures explicitly labelled `UNKNOWN_RESOURCE`.  These are
   quotients of `U_M`, so all-pass images cannot prove an equality in `U_M`.
   The existing low-index and S3/D18/S4 receipts have the same one-way
   limitation.

4. **Structural finite reduction.** A reduction to a finite product such as
   `Q0^5` would require an exact kernel statement (or an exact finite
   permutation/pc presentation) for the diagonal map from K05.  The audited
   sources provide only the five coface relator inclusions and rho closure;
   they do not prove equality of the resulting normal closure with a finite
   kernel, nor give a finite order/isomorphism certificate for `U_M`.
   K05 has abelianization `Z^5`, so the finite `(C2)^5` abelian image is not
   such a reduction.  The paper's nonabelian setting is also not covered by
   the Abelian theorem: the source text explicitly leaves identification of
   all genuine charming shadows for nonabelian `F2/N_F2` as Question 4.7
   (`papers/txt/2008.00066-what-are-gt-shadows.txt` lines 3514–3580).

I added the GAP-free, fail-closed structural/artifact audit
`search/d972_b4_global_b_audit_v1.py`.  It emits schema
`d972-b4-global-b-audit/v1`, status
`UNKNOWN_NO_TERMINAL_GLOBAL_CERTIFICATE`, and records:

```text
exact_972_input                 CROSSCHECKED_INPUT_ARTIFACTS
completed_confluent_rewriting   NOT_TERMINAL_BOUNDED_CANDIDATE
structural_presentation         NOT_FOUND_IN_AUDITED_SOURCES
finite_exact_U_M                 NOT_PRESENT_U_FINITE_GATE_DISABLED
bounded_p_quotient               NOT_GLOBAL_B
proof-producing_rewrite          CHECKER_AVAILABLE_CERTIFICATE_NOT_SUPPLIED
```

The receipt was generated outside the repository in `%TEMP%` after
`python -B -m py_compile search/d972_b4_global_b_audit_v1.py` and
`python -B -m py_compile search/check_d972_b4_rewrite_cert_v1.py` passed.  No
local GAP process was launched by this audit.  The serializer/preflight slot
is now free; a parent-authorized heavy run may start after coordination with
the universal agent, but only a genuinely terminal finite model or completed
confluent system would change the status above.

## Proof-producing lane (confluence not required)

The parent’s replay criterion is sound: a concrete chain of free cancellations
and insertions/deletions of conjugates of the 158 original relators proves an
individual norm identity even if the rewrite system is nonconfluent.  I checked
the installed KBMAG implementation statically before any GAP run.  Its
rewriting-system representation contains `equations`, `originalEquations`,
`isConfluent`, and reduction automata, but no derivation/provenance field
(`pkg/kbmag/gap/kbsmg.gi`, representation declaration).  The documented
`Rules(rws)` operation returns only two-element left/right word pairs, while
`UpdateRWS` reads `.kbprog` equations and `.reduce` reduction automata; neither
retains a replay chain.  Therefore a v2 `ReducedForm`/`IsConfluent` result by
itself cannot be promoted to B without separately replayable derivations.

To make the terminal lane explicit, I added
`search/check_d972_b4_rewrite_cert_v1.py`.  It independently reconstructs the
exact six-generator norms and validates the 158-relator digest, then accepts
only a certificate with all 972 rows and step-by-step `after` words.  Each step
is checked as one of:

- free cancellation of an adjacent inverse pair;
- deletion of a contiguous cyclic conjugate of one of the 158 relators (or its
  inverse); or
- insertion of such a relator conjugate.

Every resulting word is free-reduced and compared with the supplied `after`
field, and every row must end at `[]`.  Thus a future receipt with status
`B4_B_SIDE_CROSSCHECKED_CERTIFICATE` and no legacy artifact rows would be a
direct B4-B proof, independent of confluence.  Running the checker now against
the GHA artifact returns `RC=0`,
`status=UNKNOWN_NO_REWRITE_CERTIFICATE`; no 972-row certificate exists yet.
The two exploratory `""` rows are accepted only after exact in-memory
normalization and force `UNKNOWN_FINAL_ARTIFACT_LEGACY_EMPTY_ROWS` even if a
certificate is supplied.

## Non-applicable B4-VAC note

I also audited `docs/notes/b4_theorem_check_v1.md`, which at first appears to
offer a structural B route.  It is a different verbal (7)-group window:

- its (Q) has order (7^{40}) and its parameter is (m\bmod 7);
- the present exact `Q0` has order
  (1{,}469{,}664=2^5\cdot3^8\cdot7) and the artifact has (m=0,\ldots,17);
- the note itself leaves the Drinfeld/\(\rho\)-norm term correspondence as
  UNKNOWN and proposes a separate (117{,}649)-row test.

Consequently that note cannot identify the current 158-relator `U_M` with a
finite (7)-group or prove these 972 norms; it remains a non-applicable
structural candidate.

```text
B4_A_SIDE_CANDIDATE = NONE
B4_B_GLOBAL_PROOF   = NOT_ESTABLISHED
B4_STATUS           = UNKNOWN

## Exact 6-to-5 simplifier transport lane (new)

Added the versioned pair
`search/d972_b4_u_simplified_transport_v1.g` /
`search/check_d972_b4_u_simplified_transport_v1.py`.  The GAP producer pins
the corrected source/word artifacts, reconstructs all 158 U relators and all
972 exact F6 rho norms, runs `IsomorphismSimplifiedFpGroup`, and requires the
known 5-generator/141-relator shape.  It serializes both generator maps
(`U -> S` and `S -> U`), the complete simplified relator list, and all 972
norm words in the simplified alphabet.  Optional KBMAG is explicitly
candidate-only; the independent checker returns UNKNOWN even for KBMAG
all-pass because it does not replay GAP's rewriting rules.

The source currently compiles statically; after the signed-word helper
shadowing fix its SHA is
`e173c23e62d8eb9bcbf66d05d5ac02e10072a90dfaf0bdede2b0d7c602b041b5`, and the
checker SHA is
`cbfd3b5c844467464fe02182347feba1b272d45df1d9484127ceae48104b490e`.
The producer also has no terminal `QUIT` (the wrapper's `Read(...)` context
rejects it).  Execution is pending the parent-owned GAP/GHA boundary; local
startup currently fails with the known signal-pipe Win32 error, so no
transported presentation result or finite defect is claimed yet.

## Alexander/F19 twisted-metabelian screen (2026-08-16)

The versioned producer `search/d972_b4_u_alexander_v1.py` was rerun with an
explicit output path after the first process failed to leave an artifact.  The
complete receipt is `%TEMP%/d972_b4_u_alexander_all220_v1.json`; its captured
stdout has no stderr and records all 220 de-duplicated candidates (10 lifted
mod-9 basis characters, 90 signed pair combinations, and 120 deterministic
random combinations).  Every candidate has Fox-relator rank 160 and
translation nullity 1 over F19.  Since this is only the universal affine
coboundary direction, no norm translation pairing is available.  Canonical
pins in the receipt are source `c61b2b...`, rho `23db...`, relator `12fc...`,
roof `ecf0...`, and raw word artifact
`564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`.
This is a clean finite-character screen, not a nonexistence theorem and not
a B proof.

The next finite-K route is `search/d972_b4_u_anupq_kernel_v1.g`.  Its exact
transport is: construct U from the pinned 158 relators, form the index-32
kernel K, build the ordinary K RRS presentation (expected 132 generators and
4695 relators), then rewrite each of the exact 972 six-generator roofs into
that presentation before ANUPQ p=3 class scans.  A K quotient defect would
promote through `core_U` and can be checked independently; all-pass remains
UNKNOWN.  Static audit fixed a genuine GAP syntax issue (`If(...)` expression)
by replacing it with an explicit conditional status assignment.  Local GAP
execution was attempted at a safe no-GAP boundary but stopped before script
input due the known Windows signal-pipe failure:

```text
gap.exe: fatal error - couldn't create signal pipe, Win32 error 5
```

Therefore no ANUPQ class result or transport certificate is claimed locally;
the corrected script needs a GHA GAP-4.16 run.

## Degree-four Magnus continuation (2026-08-16)

The new versioned pair
`search/d972_b4_u_magnus4_functional_v1.py` /
`search/check_d972_b4_u_magnus4_functional_v1.py` was executed on the pinned
canonical inputs.  The producer receipt is
`%TEMP%/d972_b4_u_magnus4_functional_v1.json` (producer SHA, as replayed,
`6302305ae4f2138346f5b29b19e469efa95c6dbbf67d83d68918b715a0824565`).  It
parameterizes degree four by the degree-two annihilator (900 variables),
includes both-sided D2 constraints and both D3 placements, and finds:

```text
linear rank/nullity       151 / 10
D2 relator rank           91  (perp dimension 9)
D3 relator basis rank     725
D4 constraint rank        900 / 900
D4 functional nullity     0
all 972 norm pairings      0
status                    UNKNOWN_ALLPASS_MAGNUS4_LANE
```

The non-importing checker independently replayed the same computation and
returned `UNKNOWN_ALLPASS_MAGNUS4_CROSSCHECKED` (exit 2) in
`%TEMP%/d972_b4_u_magnus4_functional_v1.check.json`.  Source hashes are
`2ab685c5ab7300ce4f26227ec7a18328b0f0b79d27ef57954871391cda479139` for the
producer and `d5ba9ce46a4441112fbb1e9c0ac7c761cc0a1c209c88dfc42fab94522a5326f9`
for the checker.  This closes the degree-four truncated lane as a checked
all-pass/UNKNOWN result; it is not a global B proof.

## Canonical raw-RS ANUPQ v2 handoff

The parent lane's newer `search/d972_b4_u_anupq_kernel_v2.g` now constructs
the exact raw 161-generator/5056-relator Schreier presentation directly,
without opaque Tietze transport, and rewrites the 972 canonical norms by the
same mask-major regular C2^5 transversal.  Its independent Python checker
replayed a synthetic all-pass receipt over all raw relators and norms:
`UNKNOWN_P3_ALLPASS_OR_RESOURCE`, with 161/5056/972 replay gates true.  This
is only a checker selftest; no GAP p-quotient result has been obtained.

During static audit I repaired the remaining non-GAP `If(...)` expression in
the class receipt construction and added a final selftest marker.  The
corrected v2 must be rehashed before dispatch.  Local GAP remains blocked
before script input by the signal-pipe Win32 error above, so the shortest
remaining terminal-capable experiment is a GHA run of v2 with classes 2 and 3.

After the syntax/marker repair, the v2 source SHA is
`ae605e53f0a6823b6362ffe9e063cb9b4ea824ff1a28992c17da8706feb62576`, and the
checker SHA is `ef9bb2c12610468f2df31548bc9bef7e025ad58ec502b8cf0b0a24381d1f04bd`.
```

## Exact finite-K functional lanes (2026-08-16)

The pure-Python ordinary Reidemeister--Schreier construction has 161
generators and 5056 relators, with the deterministic transversal
`t_m=prod(g_i : bit i of m)`.  All computations below use the canonical
source SHA `c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`,
relator digest `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`,
rho digest `23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed`,
and exact norm digest `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`.

`search/d972_b4_u_mod3_functional_v1.py` and its standalone checker
`search/check_d972_b4_u_mod3_functional_v1.py` independently give rank 151,
nullity 10 over F3; every one of the 972 norm rewrites pairs to zero with
every null functional.  This is `UNKNOWN_ALLPASS_MOD3_FUNCTIONAL_LANE`.

The Hensel mod-9 lane (the versioned `d972_b4_u_mod9_functional_v1.py`
pair, with its separate checker) likewise has rank 151/nullity 10 and all
972 pairings zero.  It gives no A witness and is not promoted.

The degree-two Magnus pair
`search/d972_b4_u_magnus2_functional_v1.py` /
`search/check_d972_b4_u_magnus2_functional_v1.py` is independently replayed:
`D2` relator rank 91, dual nullity 9, and all 972 quadratic pairings zero.
Its receipt explicitly records `kernel_characteristic=false` and
`finite_U_quotient_via_core=true`; the finite-U step is by core, not a false
characteristic-kernel assertion.

The degree-three pair
`search/d972_b4_u_magnus3_functional_v1.py` /
`search/check_d972_b4_u_magnus3_functional_v1.py` gives the two-sided ideal
rank 89 in the 90-variable dual parameterization (nullity 1), with all 972
cubic pairings zero.  An exact structural follow-up reconstructing its one
nonzero cubic dual class and solving
`h3 tensor W` intersect `W tensor h3` over F3 gives dimension 0 (rank 20 in
the 20 unknown `(u,v)` variables).  Thus this particular degree-four
truncated-algebra continuation has no degree-four dual functional at all;
it is an obstruction to that route, not a B proof.

The next versioned exploratory fallback is
`search/d972_b4_u_anupq_kernel_v1.g`, which builds the exact index-32 K RRS
presentation and attempts ANUPQ `PQuotient(K,3,class=2,3)` while evaluating
the exact 972 norm rewrites.  It is intentionally K-level: any defect is
mathematically promoted only through `core_U(kernel)`, and the script does
not claim a six-generator U receipt.  It has not been run while the current
Python replay process is active.

## Canonical-v2 low-index max-7 scanner

Added [d972_b4_lowindex_v2.g](C:/Users/81905/Desktop/shadow-atelier/search/d972_b4_lowindex_v2.g)
without modifying v1.  It consumes only
`search/certs/d972_b4_p2_magnus_input_v2_20260816.json`, fail-closing on the
c61b2b source SHA, canonical rho SHA 23db316e, relator 12fc1146, roof 3015b4,
norm ecf0cc, target 9c77e6, and word-key 283bf9 digests.  It constructs
`F6/<158 exact relators>` directly, maps F2 `1 -> U1` and `2 -> U4`, checks
rho⁵ and all relators at every rho power, then runs
`LowIndexSubgroupsFpGroup(Ufp,7)` over every returned subgroup.  All-pass is
explicitly UNKNOWN.

The defect path emits `d972-b4-finite-image/v2` with the current checker’s
required `rho_words_source`, canonical rho SHA, `source_sha256`,
`rho_words_legacy_json_mismatch=false`, `p2_input_schema`,
`p2_input_file_sha256`, all 158 relators/booleans, rho5, all 972 roof/key
rows, `expected_defect`, and the independent word-key digest.  The all-pass
artifact is `ci/out/d972_b4_lowindex_v2.json`; the defect receipt is
`ci/out/d972_b4_lowindex_v2.defect.json`.  Markers are
`B4_LI_V2_INPUT_AUDIT_PASS`, `B4_LI_V2_LOW_INDEX_BEGIN`, and
`B4_LI_V2_FINAL_MARKER`.

Numeric-only GHA preambles:

```text
script: search/d972_b4_lowindex_v2.g
preamble: D972_B4_LI_V2_MAX_INDEX:=7;; D972_B4_LI_V2_SELFTEST:=0;;
out_dir: ci/out
with_pquot_packages: false
timeout_min: 120
```

The cheap selftest driver
`search/d972_b4_lowindex_selftest_v2.g` passed locally:

```text
B4_LI_V2_SELFTEST_PASS max_index=7 numeric_controls=true y_to_U4=true
B4_LI_V2_SELFTEST_FINAL_MARKER max_index=7
```

Scanner SHA256 is
`321352e56882194bd5d2d901f9c79de9552baead6bfe5c3b4b45ee5b585da83f` and the
selftest driver SHA256 is
`d29c988831e025fab22687484a37728c5317698dca80734418121d852170ba16`.
No low-index enumeration was run locally; the GHA dispatch is the execution
boundary.  Therefore no max-7 mathematical verdict is claimed here.

## P2 SG16_14 MappedWord repair and bounded rerun

The SG16_14 abort in run `31921231869` was a type-family bug, not a
mathematical defect: `P2Roof` created a fresh `FreeGroup(6)` for `rw`, while
`rf` and `relsU` belonged to the presentation's other free group.  The call
`MappedWord(w,f6g,rf)` therefore had no GAP method on that path.  The shared
v1 worktree now type-hardens all four free-word substitutions with an
`ExtRepOfObj` evaluator and evaluates F2 roof rows with an explicit signed
evaluator; its identity-image selftest is included.  The versioned wrapper
`search/d972_b4_pquotient_v2.g` independently tests the ExtRep evaluator on a
permutation target with identity generator images and on a second free-group
family, then pins and executes the repaired source.  Wrapper SHA256 is
`3709731f45e5c585c20657ede1d1fd8adef7b183ae12170c7887ae7311255a89`.

The bounded local command

```text
& .\gap.ps1 search\d972_b4_pquotient_v2.g
```

selects only `SG16_14` (`D972_P2_TARGET`, `exhaustive=false`) and completed
with `P2_V2_REPAIR_FINAL_MARKER`.  The pinned repaired-v1 source SHA was
`16ad5f1f3223d10c3d45c0cc422d2d63e351f09c1c2bbd88d46e3ad46a046571` and the
worker SHA was `f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8`.
The wrapper rewrites v1's old expected-worker literal to that f9 pin only in
its temporary execution copy; a direct v1 run must update its source pin (and
then refresh the v1 source SHA) before it can be used as a terminal rerun.
The result was:

```text
SG16_14 order=16 epi_count=31
all 31/31: relator_bad=0, rho5=true, roof_fail_count=0
defect_receipt=null, status=UNKNOWN, exhaustive=false
```

The receipt also recomputed and bound the immutable c61b2b input, relator
12fc1146, roof 3015b4, target 9c77e6, and word-key 283bf9 digests.  Thus the
repaired target has no A witness; it is only a bounded finite-image
all-pass/UNKNOWN observation and does not advance the B4-B global proof.  A
separate Python receipt check replayed all 31 rows and the same c61b2b input
pin (`P2_SG16_14_INDEPENDENT_RECEIPT_PASS rows=31 allpass=true defect=null`).

## Auxiliary B3 GAP 4.12 compatibility handoff

Run `31920068697` reached
`D972V2_MAPPING_STAGE subgroup_done order=17496` and then failed at the next
frozen-v1 call `Size(Group(qt9.s1,qt9.s2))`.  The current frozen-v1 source in
this worktree is SHA
`f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8`; v1 was
not edited.  I added a v2-only, exact one-occurrence bridge in
`search/d972_dovetail_worker_v2.g` (SHA
`c7fab7e525368ea7ad21e29b343449f9058ef0c7e0fa619bcbc04a1b756b6485`):

```text
Size(Group(qt9.s1,qt9.s2))
  -> D972V2PointActionGroupOrder([qt9.s1,qt9.s2],6*Size(G9))
count = 1
```

The helper enumerates the unchanged finite action images, converts them to
`PermList` generators, and computes the same generated subgroup using the
explicit `Subgroup(SymmetricGroup(degree),perms)` parent form.  It handles
both permutation mappings (`point^map`) and general mappings (`Image`).  The
v2 selftest returned
`D972V2_COMPAT_SELFTEST_PASS point_action_order=4 qt9_rewrite_count=1`, with
the rewrite recorded in the v2 receipt envelope.  This is a representation
compatibility repair only; the full base audit was not rerun, so no B3
completeness or terminal claim follows.  The next qt4/base calls remain an
explicit future compatibility boundary rather than being silently rewritten.

## Corrected immutable-input handoff

To honor versioning without overwriting the legacy input, I added
`search/d972_b4_correct_p2_rho_v1.py`. It validates the old source SHA and all
three public row digests, then writes schema `d972-b4-p2-magnus-input/v2` with
the canonical rho and these pins:

```text
legacy v1 source SHA        caef3c6735678e1b87bc427791d4c96474d6a4c566d4078a8fafd89742c7d2c8
corrected v2 source SHA     c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9
canonical rho digest        23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed
relator digest (unchanged)  12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e
roof digest (unchanged)     3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8
target digest (unchanged)   9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
```

The generated corrected file passed `B4_GQ2_INPUT_AUDIT_PASS` with
`legacy_json_rho_mismatch=false`. The terminal GQ2/checker lanes now accept
only this corrected v2 source SHA; the legacy v1 JSON and temporary GAP bridge
are fail-closed historical inputs. P2/Magnus/SAT consumers that read the old
field must be rerun or switched to corrected v2 before their norm outputs can
be considered semantically sound. The independent checker now pins the
canonical rho digest, corrected source SHA, and `mismatch=false` (checker SHA
`6f924a40610988f523859ea4e996e230952a744edd02e3d7b5694a9cb127e7c5`).

## B4-A central-cover GQuotients lane (exact v2)

I added the exact-artifact driver
`search/d972_b4_gquotient_covers_v2.g`.  It consumes the immutable pinned JSON
input directly through GAP's `json` package (the generated GAP bridge from
`search/d972_b4_exact_input_export_v1.py` is retained only as a historical
exploratory artifact and is rejected by the terminal lane),
constructs `F_6/<158 signed relators>`, and independently rebuilds every roof
norm with `1 -> U1`, `2 -> U4` and rho order `rho^4 ... rho^0`.  The source
JSON SHA and recomputed digests are bound before any target enumeration:

```text
source JSON SHA256       c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9
relator digest           12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e
roof-word digest         3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8
target-key digest        9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
normalized key digest    283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930
exact F6 norm digest     ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e
```

The short GAP gates passed:

```text
B4_GQ2_INPUT_AUDIT_PASS source_sha256=c61b2b77... relator_digest=12fc... roof_digest=3015... target_digest=9c77...
B4_GQ2_SELFTEST_PASS asymmetric_y_U4=true
```

The scanner now emits a defect receipt only when all 158 relators and the
complete rho cycle pass; an invalid target hom cannot be mistaken for an A
candidate.  No defect receipt was produced.

One input-field audit found a legacy convention mismatch that is now fail
closed.  The legacy v1 JSON `rho_words` field spells `(g3*g5*g6)^-1` as
`[-3,-5,-6]`; the authoritative universal map is the actual inverse word
`[-6,-5,-3]`, with the complete canonical list
`[[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]]`.  This is exactly the map
in `search/d972_b4_universal_v2.g` and `search/probe/hsp7_gap_v1/stage2_k05.g`,
and is independently mirrored by `search/d972_b4_kbmag_v2.py`.  v2 now binds
this canonical map, records `rho_words_source=universal_v2_canonical`, and
marks `legacy_json_rho_mismatch=false`; the independent checker
`search/check_d972_b4_finite_image_v2.py` rejects any receipt-controlled rho
map that is not this frozen list and rejects any source other than the
corrected v2 SHA above.  The exact relator/roof/target digests are unchanged
because this metadata correction does not alter the 158 relators or 972 F2
rows.

The earlier legacy-source target scans were exploratory only:

```text
SL2_3  order=24 degree=9   epi_count=0  defects=0  (legacy source; not terminal)
SL2_4  order=60 degree=16  epi_count=0  defects=0  (legacy source; not terminal)
```

Their summaries are in `%TEMP%/d972_b4_gq_v2_sl2_3.json` and
`%TEMP%/d972_b4_gq_v2_sl2_4.json`, both with status
`UNKNOWN_ALLPASS_CONTINUE` and the six exact digests above.  GL2_3 reached a
summary with `epi_count=0` but the five-minute wrapper stop lost its final
marker, so I conservatively record it as `ENUMERATION_BLOCKED`, not as a
completed no-hom gate.  SL2_5 remained responsive/CPU-bound for five minutes
without a summary and was stopped as `ENUMERATION_BLOCKED`.  GL2_4, GL2_5,
and q=7,8 targets were not started after these GQuotients cost signals; no
nonexistence statement follows from those blockers.  No finite-image A
candidate was found.

Corrected-source reruns of both small targets are complete:

```text
SL2_3  %TEMP%/d972_b4_gq_v2_sl2_3_corrected.json  epi_count=0 defects=0
SL2_4  %TEMP%/d972_b4_gq_v2_sl2_4_corrected.json  epi_count=0 defects=0
```

Both carry source SHA
`c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`, rho
digest `23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed`,
and `rho_words_legacy_json_mismatch=false`.  These remain finite-image
nonexistence observations, not a proof about `U_M`.

As a bounded structural complement, `search/d972_b4_gquotient_simplify_v1.g`
ran `IsomorphismSimplifiedFpGroup` on the same exact 158-relator input and
returned `generators=5, relators=141`; its bounded GL2_3 `findall=false` probe
observed zero epimorphisms.  It exposed no finite-order or isomorphism
certificate and is therefore only a probe.  The operative v2 source SHA after
the canonical-rho and source-pin edits was
`dbeba06debdb1a242f9cd23e6d9e864aa1cbb74964ef64c622ddbfa67dbbc6c3` before
the numeric-dispatch edits below.

## GQ2 numeric dispatch handoff

The GQ2 driver is now dispatch-safe with a numeric, quote-free selector:
`D972_B4_GQ_TARGET_INDEX` is fail-closed to this exact 1-based table:

```text
1 SL2_3   2 GL2_3   3 SL2_4   4 GL2_4   5 SL2_5   6 GL2_5
7 SL2_7   8 GL2_7   9 PSL2_7  10 PGL2_7  11 PSL2_8  12 PGL2_8
```

Numeric `SL2_8` is intentionally omitted because `SL(2,8)=PSL(2,8)`;
the pre-existing quoted `D972_B4_GQ_TARGET:="SL2_8"` control remains
accepted unchanged.  An explicitly conflicting numeric/string target fails
closed.  The new `search/d972_b4_gquotient_covers_selftest_v2.g` sets only
numeric globals (`D972_B4_GQ_TARGET_INDEX:=1;;` and
`D972_B4_GQ_SELFTEST:=1;;`) and exercises the asymmetric `U4` canary plus
the final marker.  The v2 source also emits final markers for selftest,
input-audit, and target modes.  The current source hashes are:

```text
search/d972_b4_gquotient_covers_v2.g
  3790ec55cf0c3b59a5b21b2e208152382f84897c6976c858213faa37fec4a272
search/d972_b4_gquotient_covers_selftest_v2.g
  361c99cd0f22de971eeebf5bc53e1656a0baf64b3ac5e2fb5b8ad821a70d2745
```

The four recommended first GHA shards are indices 7, 8, 10, and 11
(`SL2_7`, `GL2_7`, `PGL2_7`, `PSL2_8`): these are central/projective targets
whose natural permutation degree is beyond the low-index-7 lane.  An
all-pass result remains `UNKNOWN`; only a checker-replayed canonical defect
receipt can be an A candidate.  The shared finite-image checker was not
edited by this handoff (its existing dirty diff belongs to the parent lane).

Dispatch preambles (with the canonical corrected JSON supplied through the
existing `D972_B4_GQ_INPUT` workflow setting) are:

```text
D972_B4_GQ_TARGET_INDEX:=7;;
D972_B4_GQ_TARGET_INDEX:=8;;
D972_B4_GQ_TARGET_INDEX:=10;;
D972_B4_GQ_TARGET_INDEX:=11;;
```

Each line is used alone before `Read("search/d972_b4_gquotient_covers_v2.g");`.
The quote-free selftest command is
`& .\gap.ps1 search\d972_b4_gquotient_covers_selftest_v2.g`.

The local GAP invocation was not retried after the known Windows signal-pipe
failure (`Win32 error 5`); parent can run the new driver on GHA 4.16.

Thus the B4-A lane remains exploratory and does not alter the global verdict:

```text
B4_A_SIDE_CANDIDATE = NONE
B4_B_GLOBAL_PROOF   = NOT_ESTABLISHED
B4_STATUS           = UNKNOWN
```

## Final direct Read-context fix audit (2026-08-16)

`search/d972_b4_original_automatic_v1.g` now has SHA256
`fcb32175837412bbce9bf117fbe0eb8c4f8cc1b11f9fa921b46acf133ecc6874`.
The only code change is the Read-illegal `QUIT;` and its immediate closing
`fi;` replaced by `else`, with one matching `fi;` appended after the automatic
receipt/final marker.  PRECHECK=1 therefore writes only the precheck receipt
and skips the body; PRECHECK=0 enters only the automatic body.  `rg 'QUIT'`
is empty, Python checker `py_compile`, ASCII, and `git diff --check` pass.
Local GAP Read-smoke was not started because PIDs 33332, 33744, and 39624
were active; parent should run the short GHA PRECHECK=1 smoke before direct
heavy execution.  The global result remains UNKNOWN pending that run and the
subsequent independent receipt/replay checks.

## Versioned KBMAG bootstrap for generic `gap-run` (2026-08-16)

The generic workflow does not install `kbmag` binaries, although the
sha256-verified setup-gap GAP image contains its source tree.  I added the
ASCII-only bootstrap
`search/d972_b4_kbmag_bootstrap_v1.g`.  In mode `1` it runs
`./configure <GAPROOT> && make -j2` in the supplied `pkg/kbmag` directory,
reads an out-of-tree `PASS` status file, then requires
`LoadPackage("kbmag")=true` and a one-generator `C2` Knuth--Bendix plus
`ReducedForm(a^2)=1` probe before reading a target.  It emits
`B4_KBMAG_BOOTSTRAP_BUILD_PASS`,
`B4_KBMAG_BOOTSTRAP_PREFLIGHT_PASS`, and a final marker, and writes
`ci/out/d972_b4_kbmag_bootstrap_v1.json`.  Unsafe shell path characters and
noncanonical targets are rejected; mode `1` requires explicit GAPROOT and
package-directory bindings.  No workflow file or network download is used.

The exact generic-workflow dispatch for direct 6/158 AutomaticStructure is:

```text
script=search/d972_b4_kbmag_bootstrap_v1.g
out_dir=ci/out
timeout_min=350
with_pquot_packages=true
preamble=D972_B4_KBMAG_BOOTSTRAP_MODE:=1;; D972_B4_KBMAG_BOOTSTRAP_GAPROOT:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112],CharInt);; D972_B4_KBMAG_BOOTSTRAP_PACKAGE_DIR:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112,47,112,107,103,47,107,98,109,97,103],CharInt);; D972_B4_KBMAG_BOOTSTRAP_TARGET:=List([115,101,97,114,99,104,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,46,103],CharInt);; D972_B4_KBMAG_BOOTSTRAP_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,107,98,109,97,103,95,98,111,111,116,115,116,114,97,112,95,118,49,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_INPUT:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,117,116,112,117,116,95,118,49,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_AUTOMATA_PREFIX:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,95,97,117,116,111,109,97,116,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=0;; D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=0;;
```

The bootstrap preflight already passed in run `31933132160` (parent's
equivalent compile preamble).  Parent subsequently dispatched direct
`31933338663` and simplified `31933338572`; their receipts remain the
authoritative result.  The bootstrap file is the reproducible replacement
for that ad-hoc preamble and has not been run locally while GAP slots were
occupied.

### Direct v2 correction after run 31933338663

Run `31933338663` exposed a real GAP issue: the v1 precheck branch contains
`QUIT`, which is illegal while the generic runner evaluates a file via
`Read()`.  I left v1 immutable and added
`search/d972_b4_original_automatic_v2.g`.  It checks the exact v1 splice,
rewrites that branch to a true `if/else`, rejects any remaining `QUIT`, and
executes the transformed source from `%TEMP%`; a completion sentinel and
receipt-presence gate are checked before its own
`B4_ORIGINAL_AUTOMATIC_V2_FINAL_MARKER`.  The v2 source is ASCII-only.  The
new `search/check_d972_b4_original_automatic_v2.py` adds a static QUIT-free,
sentinel/final-marker/source-SHA gate and then invokes the existing
independent canonical v1 receipt checker.  The existing replay checker is
compatible because the v2 producer retains the pinned receipt schema.

For the corrected direct redispatch, use the bootstrap command above with
the target character list changed to the v2 path:

```text
D972_B4_KBMAG_BOOTSTRAP_TARGET:=List([115,101,97,114,99,104,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,50,46,103],CharInt);;
```

The producer bindings and `D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=0;;`
`D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=0;;` remain unchanged.  Parent should
dispatch the bootstrap with this v2 target, then run
`search/check_d972_b4_original_automatic_v2.py` on the resulting receipt,
and only then run the existing GAP replay checker.  A missing receipt,
missing v2 completion marker, syntax diagnostic, or any checker exception is
failure, not a generic-runner success.

Correction: the parent then requested the strict minimal fix in the existing
v1 file.  The temporary v2 wrapper/checker described above were removed;
`search/d972_b4_original_automatic_v1.g` now directly has the safe
`if D972OAPrecheck=1 then ... else ... fi` branch and no `QUIT` token.  Use
the v1 target character list from the dispatch immediately above.  The
bootstrap allow-list is correspondingly back on v1.  The required receipt and
final-marker gates remain the existing v1 producer/checker contract.

## Direct 6-generator AutomaticStructure lane and size gate (2026-08-16)

The transport lane had `transport_relator_checks=NOT_RUN`, so I added a
separate direct lane that never calls `IsomorphismSimplifiedFpGroup`:

```text
search/d972_b4_original_automatic_v1.g
search/check_d972_b4_original_automatic_v1.py
search/check_d972_b4_original_automatic_replay_v1.g
```

The producer reads the corrected source and word artifact, independently
reconstructs the canonical rho orbit and all 972 exact F6 norms in the
six-generator presentation, checks all 158 relators, runs
`AutomaticStructure` on the direct 6/158 presentation, exports wa/diff1/diff2
(and reduction when present), and records the complete reduced ledger.  The
Python checker replays the source/artifact/norm digests without importing the
producer; the GAP replay rebuilds 6/158 and all 972 norms from those inputs,
attaches only the exported FSA files, and replays every `ReducedForm` call.
Neither checker turns a finite all-empty result into a theorem
(`terminal_claim=false`).

The direct lane's immutable pins were recomputed independently:

```text
source SHA       c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9
word SHA         564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
relator SHA      12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e
rho SHA          23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed
roof SHA         3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8
norm SHA         ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e
```

The producer now has numeric `D972_B4_ORIGINAL_AUTOMATIC_PRECHECK` and
`D972_B4_ORIGINAL_AUTOMATIC_SELFTEST` flags.  Either value `1` performs the
source/word/158-relator/972-roof/norm digest gate, emits
`B4_ORIGINAL_AUTOMATIC_PRECHECK_FINAL_MARKER`, and never calls
`AutomaticStructure`; `0` is required for the heavy run.  The direct source
hash is verified before any group construction.

The simplified 5/141 automatic producer now records
`rws_size_status`, `rws_size` (integer or `"infinity"`),
`expected_sq_order=111577100832`, and
`rws_size_matches_expected`.  A candidate status requires a computed size;
the independent Python checker and GAP FSA replay verify the size metadata.
Equality with `111577100832` is only an equal-order candidate pending the
independent SQ-surjection receipt; it is not itself a terminal claim.

Current source hashes after these changes:

```text
f60241ef6a9b6e3ccb5eb2a08b9bf12a51c95147945903a3d6658ea8b515c5de  search/d972_b4_simplified_automatic_v1.g
f1ef6358ae7cf6fa33d563a92e9969bdf96cc499f81a3ce3b582fabf67bb2ea1  search/check_d972_b4_simplified_automatic_v1.py
3910ccffc34201957a2f16faceb9093081439dc77ab3bb5ded6baf10009be649  search/check_d972_b4_simplified_automatic_replay_v1.g
a843fcb1573f19779606df6d72bf36f10842f5894a72bdc03ab82943f631324f  search/d972_b4_original_automatic_v1.g
7462e2c02be098156acbb9b5816c62d8ad5b703204c0ded5f6533c07e8d92dd9  search/check_d972_b4_original_automatic_v1.py
002b114a2d367c1b7891dbb373d9dd214cb82cb916e65e5da1b9a561626d3a5a  search/check_d972_b4_original_automatic_replay_v1.g
```

The ordering lane remains unchanged and self-audited: eight numeric KBMAG
orderings times ten numeric signed-generator permutations, with independent
canonical transport replay; all-pass remains UNKNOWN.  Its hashes remain the
ones recorded above (`8e633c...` producer, `c781dc...` Python checker,
`17541c...` selftest).

Exact quote-free GHA precheck preamble (the numeric character lists avoid
workflow quote stripping) is:

```text
& .\gap.ps1 search\d972_b4_original_automatic_v1.g -ExtraArgs @('-c','D972_B4_ORIGINAL_AUTOMATIC_INPUT:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=1;; D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=1;;')
```

For the heavy direct run, use the same preamble with both flags set to `0`
and additionally set
`D972_B4_ORIGINAL_AUTOMATIC_AUTOMATA_PREFIX` to the numeric path
`ci/out/d972_b4_original_automatic_v1_automaton` (character list
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,95,97,117,116,111,109,97,116,111,110`).
Run the producer before either replay checker; GHA workers do not share `%TEMP%`.

The direct GAP replay preamble binds
`D972_B4_ORIGINAL_REPLAY_RECEIPT`, `D972_B4_ORIGINAL_REPLAY_SOURCE`,
`D972_B4_ORIGINAL_REPLAY_WORDS`, and `D972_B4_ORIGINAL_REPLAY_OUTPUT` to
numeric `List([...],CharInt)` paths (receipt chars
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,46,106,115,111,110`; output chars
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,114,101,112,108,97,121,95,118,49,46,106,115,111,110`).
The source and word arrays are exactly those in the producer precheck above.
This is the command shape:

```text
& .\gap.ps1 search\check_d972_b4_original_automatic_replay_v1.g -ExtraArgs @('-c','D972_B4_ORIGINAL_REPLAY_RECEIPT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,49,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_REPLAY_SOURCE:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_REPLAY_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_REPLAY_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,114,101,112,108,97,121,95,118,49,46,106,115,111,110],CharInt);;')
```

The simplified 5/141 GHA chain is the following exact numeric sequence.  The
transport producer must run first because workers have isolated `%TEMP%`:

```text
& .\gap.ps1 search\d972_b4_u_simplified_transport_v1.g -ExtraArgs @('-c','D972_B4_SIMPLE_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,115,105,109,112,108,105,102,105,101,100,95,116,114,97,110,115,112,111,114,116,95,118,49,46,106,115,111,110],CharInt);;')
```

Then run the automatic producer with input/output/prefix lists
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,115,105,109,112,108,105,102,105,101,100,95,116,114,97,110,115,112,111,114,116,95,118,49,46,106,115,111,110`,
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,115,105,109,112,108,105,102,105,101,100,95,97,117,116,111,109,97,116,105,99,95,118,49,46,106,115,111,110`, and
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,115,105,109,112,108,105,102,105,101,100,95,97,117,116,111,109,97,116,105,99,95,118,49,95,97,117,116,111,109,97,116,111,110`, respectively:

```text
D972_B4_SIMPLE_AUTOMATIC_INPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,115,105,109,112,108,105,102,105,101,100,95,116,114,97,110,115,112,111,114,116,95,118,49,46,106,115,111,110],CharInt);; D972_B4_SIMPLE_AUTOMATIC_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,115,105,109,112,108,105,102,105,101,100,95,97,117,116,111,109,97,116,105,99,95,118,49,46,106,115,111,110],CharInt);; D972_B4_SIMPLE_AUTOMATIC_AUTOMATA_PREFIX:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,115,105,109,112,108,105,102,105,101,100,95,97,117,116,111,109,97,116,105,99,95,118,49,95,97,117,116,111,109,97,116,111,110],CharInt);; D972_B4_SIMPLE_AUTOMATIC_COMPUTE_SIZE:=1;;
```

Each ordering shard reuses the same transport input/output lists above and
adds the numeric selector pair
`D972_B4_SIMPLE_ORDERING_INDEX:=i;;` for one `i` in `1..8` and
`D972_B4_SIMPLE_PERM_INDEX:=j;;` for one `j` in `1..10`, with output list
`99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,115,105,109,112,108,105,102,105,101,100,95,111,114,100,101,114,105,110,103,115,95,118,49,46,106,115,111,110`.
The independent Python checker accepts only the corresponding digest and
selector ledger; all-pass ordering results remain UNKNOWN.

No local GAP run was started: parent GAP processes 39624, 33744, and 42424
were still active during this handoff.  Python canonical replay and py_compile
passed; GAP precheck/full/replay results remain pending GHA execution.  The
latest transport GHA run `31932781091` succeeded.  The attempted simplified
AutomaticStructure run `31932804116` failed closed before computation because
the runner reported `kbmag`: `kbprog` is not compiled and `LoadPackage("kbmag")`
returned false.  This is an environment/package blocker, not a canonical
input or norm-digest failure; a KBMAG-capable runner is required for either
automatic lane.

AutomaticStructure metadata upgrade: successful runs now export `wa`,
`diff1`, and `diff2` FSA files, record their state counts and SHA-256
digests, bind the KBMAG package version, and require
`automatic_axiom_checked=true` before emitting
`B4_B_CANDIDATE_PENDING_REPLAY` for an all-empty 972 ledger.  Its independent
checker accepts only this metadata-complete pending status and never silently
turns it into a theorem.  Local execution was deferred while parent GAP
processes held the slot.

## Nonconfluent KBMAG reduced-form audit and ordering lanes (2026-08-16)

The new `search/d972_b4_simplified_reduced_v1.g` consumes the pinned
transport receipt and follows the KBMAG contract: `KnuthBendix` returning
`false` is still a normal halt when the reduction automaton is installed.
It therefore applies `ReducedForm` unconditionally after
`ReductionAutomaton`, rather than testing the private `.reduced` flag or
confluence.  On the exact 5-generator/141-relator presentation, with
`maxeqns=maxstates=maxwdiffs=250000` and `maxstoredlen=[4000,4000]`, the run
took 222.1 seconds and reported:

```text
normal_stop=true  confluent=false  rule_count=14413
unique_norms=486  reduced_norms=972  empty=2/972  shortest_nonempty=36
status=NONZERO_REDUCED_WORDS
```

Receipt: `%TEMP%/d972_b4_simplified_reduced_v1_receipt.json`, 4,014,055
bytes, SHA `7b5e6417bb286fcdc81901e40ef53037509f19eabbb08a3b021cde8a4d6472a6`.
The independent checker
`search/check_d972_b4_simplified_reduced_v1.py` replayed the canonical
transport and all 972 reduced-word ledgers, returning exit 2 with
`UNKNOWN_NONZERO_REDUCED_WORDS`; `kbmag_rule_ancestry_replayed=false` is
explicit.  The nonempty shortest word is not an A witness because the
nonconfluent system does not certify nonidentity.

I also added the independent shortlex AutomaticStructure lane
`search/d972_b4_simplified_automatic_v1.g` plus
`search/check_d972_b4_simplified_automatic_v1.py`.  It invokes
`AutomaticStructure(rws,true,true,false)` on a fresh pinned presentation and
only uses `ReducedForm` after a successful automatic-structure/axiom check.
No local result is recorded yet because the parent GAP process occupied the
local slot during handoff.

For the requested recursive/`rt_recursive`/wreath-product search, the new
numeric scanner is `search/d972_b4_simplified_orderings_v1.g`, with checker
`search/check_d972_b4_simplified_orderings_v1.py` and numeric selftest
`search/d972_b4_simplified_orderings_selftest_v1.g`.  It has eight ordering
indices (`shortlex`, `recursive`, `rt_recursive`, two `wreathprod`, two
`wtlex`, and reversed recursive) and ten signed-generator permutations,
giving 80 quote-free GHA shards.  Each receipt contains the exact selector,
normal-stop/confluence/empty ledger, and 972 reduced words; finite all-pass
remains UNKNOWN.  Current source SHA pins are:

```text
904176edf101d2b63ba4843f8b4045ad15dd111fcbfef2ff6336d841bff66f18  search/d972_b4_simplified_reduced_v1.g
a612145690f5c1e83b0fff8c76d5bf3f56aa6d7ba80c9ff049cdcc1429dc692f  search/check_d972_b4_simplified_reduced_v1.py
a53f641efee6f0135a389441b43762dda5f1dca9e99038f9b153a7c7cea1a4af  search/d972_b4_simplified_automatic_v1.g
3694bb632ee428d3cedadf02200a5c7fbf8d8f3a53865ef7f84176fb31fa217e  search/check_d972_b4_simplified_automatic_v1.py
8e633cc03aa6937da4756dbb804d1f6ecd88e06d0f645923ef27e574987422b8  search/d972_b4_simplified_orderings_v1.g
c781dc9dc0d53a0e600ee530236b182b1557b5934f8a42d6c33596911c65441f  search/check_d972_b4_simplified_orderings_v1.py
17541cf7f745af28a24b18bf7eefc94b7ccd30c2176589097ba1036d71b7ddd1  search/d972_b4_simplified_orderings_selftest_v1.g
```

For GHA, first run the transport producer into `ci/out` and pass that exact
receipt path numerically/immutably as `D972_B4_SIMPLE_*_INPUT` to each lane;
GHA workers do not share local `%TEMP%`.  No B4-A candidate or terminal B4-B
certificate has resulted from the reduced audit.

## Simplified 6-to-5 transport and KBMAG attempt (2026-08-16)

I added the versioned producer
`search/d972_b4_u_simplified_transport_v1.g` and independent checker
`search/check_d972_b4_u_simplified_transport_v1.py`.  Both pin source SHA
`c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`, relator
digest `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`,
rho digest `23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed`,
and exact norm digest
`ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`.
The producer constructs the exact F6 rho norms with `j(1)=U1` and
`j(2)=U4`, obtains the 5-generator/141-relator range of
`IsomorphismSimplifiedFpGroup`, and maps every norm by exact free-reduced
substitution through the six generator images.  The producer/checker hashes
are respectively:

```text
3bf11e915a63f4bd2b5a4e8351f9975c909aa1685324a9e22f2aec056ecfe1eb  search/d972_b4_u_simplified_transport_v1.g
c0b6bd027d9ae5a46f4a984b58c9a9b2f264e7935b9cd1fb7e64d9fbb0da3262  search/check_d972_b4_u_simplified_transport_v1.py
```

The transport-only receipt is
`%TEMP%/d972_b4_u_simplified_transport_v1_receipt.json`, with simple-relator
SHA `6d614c32365753d62477cad8803420ffa58bcca0b5d18b0e5eadaaf6bf81b35a`
and simple-norm SHA
`127f029a2bafc7f8adf249b8c5f37cda594b105d3e1b567ba00400771cdca63e`.
The independent checker replayed all 972 norm substitutions and returned
exit 2, status `TRANSPORT_CROSSCHECKED_UNKNOWN` (receipt SHA
`535d033019140e76cb9d3d7452b3e551c156f50ce74728b76bf6238d81806323`).
The GAP quotient relation `IsOne` replay was made opt-in because it did not
finish in the local bounded wrapper; this is recorded in the receipt as
`transport_relator_checks=NOT_RUN`, not silently promoted to a proof.

The optional simplified KBMAG run used
`maxeqns=maxstates=maxwdiffs=250000` and `maxstoredlen=[4000,4000]`.  It
completed its own final marker in 23.1 seconds with
`status=NO_TERMINAL_KBMAG_RESULT`, receipt
`%TEMP%/d972_b4_u_simplified_transport_v1_kbmag_receipt.json` (SHA
`4682ea05f77a995eca73c980bbe90263a8df96bbfbedf84afe6245fa5d2054b0`).  Its
independent checker again returned exit 2,
`TRANSPORT_CROSSCHECKED_UNKNOWN`; no finite defect and no all-972 proof
receipt resulted.  Therefore this lane changes neither global verdict:

```text
B4_A_SIDE_CANDIDATE = NONE
B4_B_GLOBAL_PROOF   = NOT_ESTABLISHED
B4_STATUS           = UNKNOWN
```

## Configurable direct v2 lane (2026-08-16)

Without modifying the running v1 producer, I added
`search/d972_b4_original_automatic_v2.g`.  It pins the committed v1 source
SHA `fcb32175837412bbce9bf117fbe0eb8c4f8cc1b11f9fa921b46acf133ecc6874`,
rejects any Read-context `QUIT`, preserves the v1 canonical source/word/norm
and 6/158/972/FSA logic, and textually binds only the KBMAG call/options to
typed controls: `large`, `filestore`, `diff1`, `compute_size`,
`maxeqns`, `maxstates`, `maxwdiffs`, and `maxstoredlen`.  It appends the exact
configuration and v1-source pin as `v2_settings` in the receipt and emits
`B4_ORIGINAL_AUTOMATIC_V2_FINAL_MARKER`.

The independent setting-aware checker is
`search/check_d972_b4_original_automatic_v2.py`; the GAP replay wrapper is
`search/check_d972_b4_original_automatic_replay_v2.g`; the quote-free
canonical precheck/selftest is
`search/d972_b4_original_automatic_v2_selftest.g` (uses `diff1=true`, caps
`123/234/345/[456,567]`, and `compute_size=false`, without invoking
AutomaticStructure).  All four files are ASCII; Python `py_compile`, bare
`QUIT` scan, and `git diff --check` pass.  Parent may run the selftest first,
then a heavy v2 `diff1=true` shard with the same canonical path bindings.

Post-hardening file hashes (recompute if any parent-side path binding is
changed) are:

```text
49ed4279e0d947c1b5b9349255279b2c0c7b355418085273fb9a61e239b57a39  search/d972_b4_original_automatic_v2.g
d0d70a17e401d8a36478fc823eccb2d65d860e201522788c72272bf709a02596  search/d972_b4_original_automatic_v2_selftest.g
a572244d855dadccb5b69fac3559fe7c539b9936103ff68c00bbdef8acf3658e  search/check_d972_b4_original_automatic_replay_v2.g
f631062e90c2b2b90903b0d7ea42f59c6d5927b1356eee4e5be18598cfdc9c37  search/check_d972_b4_original_automatic_v1_terminal_v1.g
d2b0e2156247f675a9db89aea3d676b0ec51e18b2fe018f0df9f6a0b8fadc662  search/check_d972_b4_original_automatic_v2.py
```

## Independent GpAxioms replay and same-job binding (2026-08-16)

The v2 lane is now fail-closed on the actual KBMAG axiom checker.  The replay
does not trust the producer's `automatic_axiom_checked` bit: after rebuilding
the 6-generator/158-relator RWS and reattaching every exported FSA, it runs
`GpGenMult`, `GpCheckMult`, and explicitly
`GpAxioms(D972OA2RRws,large,filestore)`, then independently applies
`ReducedForm` to all 972 exact norms.  Its v2 JSON records
`gpgenmult_rechecked`, `gpcheckmult_rechecked`, `gpaxioms_rechecked`,
`gpaxioms_result`, and the empty/nonempty ledger.  All 972 empty gives
`B4_B_TERMINAL_CANDIDATE_REPLAYED`; any nonempty normal form gives
`B4_A_CANDIDATE_REPLAYED`; no size computation is needed.

`D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY` is a typed bool defaulting to
`false`; the selftest binds it explicitly to `false`.  A heavy Linux preamble
sets it to `true`, and the producer then binds its receipt, canonical source,
word artifact, settings, and `ci/out/d972_b4_original_automatic_replay_v2.json`
and reads the replay in the same job.  The producer receipt records
`post_replay=true` in `v2_settings` and emits
`B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY_PASS` only when that output exists.
This avoids relying on a second worker's isolated temporary directory.

The frozen v1 run has a separate wrapper,
`search/check_d972_b4_original_automatic_v1_terminal_v1.g`, which accepts only
the exact v1 defaults and routes the v1 receipt through the same independent
replay.  `search/check_d972_b4_original_automatic_v2.py` supports
`--legacy-v1`, validates canonical reconstruction, FSA hashes/state counts,
the replay's GpAxioms flags and receipt binding, and requires `--replay` for
`terminal_claim=true`; heavy receipts without replay remain
`UNKNOWN_V2_REPLAY_REQUIRED`.  The v2 Python checker also requires matching
`--post-replay 1` when the producer settings bind post-replay.
In legacy mode it hard-rejects any settings other than
`large=1,filestore=1,diff1=0,compute_size=1,maxeqns=maxstates=maxwdiffs=250000,`
`maxstoredlen=[4000,4000],post_replay=1`; the GAP replay output carries
`legacy_v1=true,post_replay=true` for that binding.

Static/selftest status after this hardening:

```text
python -B -m py_compile search/check_d972_b4_original_automatic_v2.py : PASS
v2 synthetic precheck (diff1=1, caps=123/234/345/[456,567], compute_size=0,
                       post_replay=false)                         : PASS
v2 replay/legacy Python contract (GpAxioms flags + A/B binding)  : PASS
ReadAsFunction syntax gate for replay_v2 + legacy wrapper       : ADDED (GHA selftest)
bare QUIT scan in v2 producer/replay/wrapper                     : PASS
local GAP heavy/replay                                             : NOT STARTED (parent GAP PIDs active)
```

Current GHA authoritative direct v1 run `31934354049` remains in progress;
its producer result/artifacts are not yet available for the new wrapper.
Parent owns commit/dispatch.  No A/B terminal result is claimed by this
update.

## GHA v2 precheck audit (run 31936795822)

Run `31936795822` checked out head `e9da5205cec4f72f734d7a6ba83a2cd5b20064a2`
and passed GAP setup, optional package installation, and the KBMAG bootstrap
(`KBMAG_BOOTSTRAP_PASS`).  It failed before mathematical execution during
the v2 selftest: GAP reported `Syntax error: String must not include
<newline>` on the `v2_settings` concatenation lines 66--74 of
`d972_b4_original_automatic_v2.g`.  Artifact upload was skipped, so there is
no receipt/run artifact to download or audit; this is fail-closed UNKNOWN, not
a mathematical result.

I corrected all nine malformed comma fragments from `),",` to `),",",`.
Static post-fix checks pass: all target GAP files have balanced per-line
quotes, ASCII/no bare `QUIT`, Python `py_compile` passes, and the synthetic
v2 precheck checker returns `PRECHECK_CROSSCHECKED`.  Corrected producer SHA:

```text
49ed4279e0d947c1b5b9349255279b2c0c7b355418085273fb9a61e239b57a39  search/d972_b4_original_automatic_v2.g
```

Exact heavy v2 `diff1=true,post_replay=true` preamble shape for the parent to
dispatch (with the immutable canonical source/word paths and explicit `ci/out`
receipt/FSA prefix) is:

```text
D972_B4_ORIGINAL_AUTOMATIC_INPUT:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,50,46,106,115,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_AUTOMATA_PREFIX:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,111,114,105,103,105,110,97,108,95,97,117,116,111,109,97,116,105,99,95,118,50,95,97,117,116,111,109,97,116,111,110],CharInt);; D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=0;; D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=0;; D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1:=true;; D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY:=true;;
```

The word-artifact list above is the canonical `search/certs` path; parent
should verify the `search/certs/d972_b4_word...` character list before
dispatch (the source list is unchanged).  After a corrected GHA selftest,
the heavy run must emit producer and post-replay final markers plus a
`ci/out/d972_b4_original_automatic_replay_v2.json` receipt before any Python
terminal checker is run.

## Follow-up audit: precheck 31937139097 and B3 31929665342 (2026-08-16)

Precheck `31937139097` reached all immutable source/relator/word/norm gates,
KBMAG bootstrap, and the v2 input/final precheck marker, then failed before
the automatic calculation with `Error, ORIGINAL automatic v2: malformed
receipt`.  The cause was GAP's `Position` being used for a string search on
the reversed JSON receipt.  The producer now uses
`PositionSublist(D972OA2Rev,"}")`; no receipt or mathematical result existed
to download from that failed run.  Current producer SHA after this fix is
`49ed4279e0d947c1b5b9349255279b2c0c7b355418085273fb9a61e239b57a39`.

For B3 run `31929665342`, the only job `95122480774` failed in its long
calibration process at `STATE_STOP ... GAP failed with exit 1`, emitted
`CALIBRATION_PENDING 42d223ed4c6742ebd667b33833fa45c01dd9b2698d65329189dae86f739d4afd`,
and had no checkpoint artifact (step 12 failure, upload skipped).  This is a
B3 calibration UNKNOWN and is unrelated to the v2 automatic lane; no A/B
claim is made from it.

## B3 calibration exception isolation and K_ab replay (2026-08-16)

The B3 log only records the fail-closed wrapper message because
`run_isolated_gap` captures GAP stderr and raises only the return code:
`STATE_STOP independent k=1,2 lossless calibration reconstruction UNKNOWN:
GAP failed with exit 1`.  Static expansion of the generated GAP source shows
the first concrete candidate failure is the pre-scan presentation gate at
`check_d972_dovetail_v2.py:440` (`calibration presentation/base mismatch`),
after the fixed base-order gates.  The workflow currently loses the actual
GAP diagnostic; the shortest repair proposal is to include a bounded stderr
tail (and the generated script SHA) in the fail-closed state/log before
raising, without weakening the UNKNOWN gate.  No workflow file was changed.

The archived K_ab receipt
`%TEMP%/gaptempdirKmIgul/d972_b4_u_kernel32_ab_v1.json` was independently
replayed.  The frozen v1 checker has a concrete indexing bug: it initializes
the replay cursor as `start` although GAP CosetTable entries are 1-based;
relator 0 therefore falsely fails at coset 1.  I added the fresh, non-importing
versioned checker `search/check_d972_b4_u_kernel32_ab_v2.py`, whose replay
uses `cursor=start+1`, validates all 158 relators and the regular C2^5 action,
and recomputes the exact 4695-by-132 integer Smith data.

```text
checker SHA256 = 48fa71312717700de1458ca76c6f89acee9409827837cbc7ef4be825bb819d87
receipt SHA256 = 7cb4bd4e080838c3bc5555c0a94371d135a282006317c73a4056d5d02ca0f106
status = K_AB_NONTRIVIAL
abelian_invariants = [9,9,9,9,9,9,9,9,9,9]
exponent_sum_matrix_sha256 = 2d9055559900f9423096e491d47dc1b5a3b70e88f438ac792c37ff43122cbefe
independent_snf_match = true
```

This is a cross-check of the archived GAP K_ab candidate, not a terminal B
claim: it proves only the receipt's finite-index kernel abelianization once
the GAP-generated RRS words are accepted.  It rules out the hoped-for
trivial-kernel/C2^5 simplification and makes the C9^10 metabelian lane the
relevant next proof target.

For the requested additional v2 KBMAG shards, retain the four immutable
numeric path bindings in the earlier preamble and use these typed controls
(the producer's explicit caps remain in force):

```text
D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=0;; D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=0;; D972_B4_ORIGINAL_AUTOMATIC_V2_LARGE:=false;; D972_B4_ORIGINAL_AUTOMATIC_V2_FILESTORE:=false;; D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1:=false;; D972_B4_ORIGINAL_AUTOMATIC_V2_COMPUTE_SIZE:=false;; D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY:=true;;
```

The companion shard is identical except for
`D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1:=true;;`.  Both retain same-job
post-replay and final-marker gates; a producer-only all-empty ledger is not
terminal.

## K to metabelian KBMAG lane (2026-08-16)

The archived independent K_ab result remains only `K_AB_NONTRIVIAL`, with
exact invariants `[9,9,9,9,9,9,9,9,9,9]`; it does not prove that K is
abelian.  I added a raw ordinary-RS lane that keeps the canonical
161-generator/5056-relator presentation and tests all 12880 pairwise
generator commutators before interpreting any of the 972 norms.  A norm
defect is an A candidate only when the commutator ledger is empty and the
independent exact SNF is C9^10; then K is C9^10 and the finite-index extension
can be replayed on every exact norm.

New versioned files:

```text
search/d972_b4_u_metabelian_kbmag_v1.g
search/check_d972_b4_u_metabelian_kbmag_replay_v1.g
search/check_d972_b4_u_metabelian_kbmag_v1.py
search/d972_b4_kbmag_bootstrap_metabelian_v1.g
```

The producer pins constructor SHA `ae605e53...`, input SHA `c61b2b77...`,
rho SHA `23db316e...`, relator SHA `12fc1146...`, original norm SHA
`ecf0cc84...`, raw-RS SHA `29c65a6c...`, and RS-norm SHA `f7134e15...`.
It disables only the frozen source's optional p-quotient block by a unique
occurrence check, runs AutomaticStructure followed by GpGenMult,
GpCheckMult, and GpAxioms, exports the wa/diff FSAs, and records complete
commutator/norm boolean ledgers.  The replay independently reconstructs the
transversal, all RS relators and exact norms from the JSON artifacts, reloads
only the exported FSAs, reruns the three Gp* gates, and compares both ledgers.
The Python checker independently rebuilds the same rows and exact integer
SNF; it never imports the producer or replay.  No local GAP/Python heavy run
was started, so these remain dispatch-ready candidates, not A/B results.

Current file hashes:

```text
a3972236122dac32e74c6c8527d8dec8c8adc61e7f4dabb107af7660bc039dac  search/d972_b4_u_metabelian_kbmag_v1.g
c397141107994a914c31892b775065b64f8c13c0425c6a2fafb86e494eae5963  search/check_d972_b4_u_metabelian_kbmag_replay_v1.g
b7b5c604b480565050ef619c13ce35915a6425bed8353706d40db0f5651e0a0b  search/check_d972_b4_u_metabelian_kbmag_v1.py
ed843a323962431f20f66a0967ab6514b778b5c4d2be23c6bbecc4611d52deea  search/d972_b4_kbmag_bootstrap_metabelian_v1.g
```

The shim pins bootstrap base SHA `bc9fdfd7...`, adds only the metabelian
target to its temporary allow-list, and leaves the workflow unchanged.

Dispatch preamble (numeric/quote-free; parent should preserve these paths):

```text
D972_B4_KBMAG_BOOTSTRAP_MODE:=1;;
D972_B4_KBMAG_BOOTSTRAP_GAPROOT:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_PACKAGE_DIR:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112,47,112,107,103,47,107,98,109,97,103],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_TARGET:=List([115,101,97,114,99,104,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,118,49,46,103],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,107,98,109,97,103,95,98,111,111,116,115,116,114,97,112,95,109,101,116,97,98,101,108,105,97,110,95,118,49,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_INPUT:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,118,49,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_AUTOMATA_PREFIX:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,97,117,116,111,109,97,116,111,110],CharInt);;
D972_B4_METABELIAN_LARGE:=false;; D972_B4_METABELIAN_FILESTORE:=false;; D972_B4_METABELIAN_DIFF1:=false;; D972_B4_METABELIAN_MAXEQNS:=250000;; D972_B4_METABELIAN_MAXSTATES:=250000;; D972_B4_METABELIAN_MAXWDIFFS:=250000;; D972_B4_METABELIAN_MAXSTOREDLEN:=[4000,4000];; D972_B4_METABELIAN_POST_REPLAY:=true;;
```

For the existing direct/transport comparison: direct 6/158 has the lowest
setup cost and should remain the first shard.  The 5/141 transport is cheaper
per KBMAG run but needs its map and relator replay, and its prior 1.1MB
receipt must not be assumed present.  The raw K lane is larger but removes
that isomorphism trust gap and directly proves the needed K commutativity;
it is the stronger terminal route if a long GHA slot is available.

Runs `31939302578` and `31939304180` both failed before GAP script output,
immediately after `P2_PACKAGE_BUILD_PASS`; no artifact, receipt, or
mathematical result exists.  This is fail-closed UNKNOWN, not A/B.

## Final metabelian bundle audit (2026-08-16)

The producer/replay/checker status precedence is now fail-closed: a norm
defect is labelled B4-A only after all 12880 K commutators reduce to one and
the independently recomputed K_ab is C9^10.  A nonabelian commutator ledger is
`UNKNOWN_K_NONABELIAN`, even if a raw automatic reduction has a norm defect.
The four files are ASCII, have no trailing whitespace or GAP `QUIT;`, and the
constructor/input/word pins recompute as `ae605e53...`, `c61b2b77...`, and
`564a921b...`; no local GAP or Python heavy run was started.  GAP Read/syntax,
KBMAG execution, FSA replay, and the Python receipt command remain GHA gates,
not local claims.  Parent may stage exactly the four new `search/` files plus
this reply; no workflow or v1 file was edited.

## v2 terminal-receipt wrapper and bootstrap (2026-08-16)

The v2 wrapper now pins the v1 producer, forces
`D972_B4_METABELIAN_POST_REPLAY:=true`, checks the v1 producer receipt and the
same-job `d972_b4_u_metabelian_kbmag_replay_v1.json` receipt, and only then
writes the v2 terminal receipt.  The v1 FSA exports, `GpGenMult`,
`GpCheckMult`, `GpAxioms`, and both complete ledgers remain the source of the
v2 result.  The v2 bootstrap shim pins the corrected generic bootstrap SHA
`bc9fdfd7a8314436b81ed75d908542727f03515c83dbcb851ebe5a5d6d083c0b` and
allow-lists exactly the v2 wrapper.  The earlier v1 shim was also corrected to
that exact 64-character base SHA.

New/updated versioned files and current hashes:

```text
search/d972_b4_u_metabelian_kbmag_v2.g
search/d972_b4_kbmag_bootstrap_metabelian_v2.g
```

The final hashes are reported below after the static audit.  The existing
independent `crosscheck/check_d972_b4_u_metabelian_kbmag_v2.py` is unchanged;
it consumes the v2 receipt schema and independently rebuilds raw RS/SNF data.

Exact quote-free/numeric preamble for the v2 shim and wrapper:

```text
D972_B4_KBMAG_BOOTSTRAP_MODE:=1;;
D972_B4_KBMAG_BOOTSTRAP_GAPROOT:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_PACKAGE_DIR:=List([47,104,111,109,101,47,114,117,110,110,101,114,47,103,97,112,47,112,107,103,47,107,98,109,97,103],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_TARGET:=List([115,101,97,114,99,104,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,118,50,46,103],CharInt);;
D972_B4_KBMAG_BOOTSTRAP_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,107,98,109,97,103,95,98,111,111,116,115,116,114,97,112,95,109,101,116,97,98,101,108,105,97,110,95,118,50,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_INPUT:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,112,50,95,109,97,103,110,117,115,95,105,110,112,117,116,95,118,50,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_WORDS:=List([115,101,97,114,99,104,47,99,101,114,116,115,47,100,57,55,50,95,98,52,95,119,111,114,100,95,107,101,121,95,97,114,116,105,102,97,99,116,95,118,49,95,50,48,50,54,48,56,49,54,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_V2_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,118,50,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_V2_V1_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,118,49,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_V2_REPLAY_OUTPUT:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,114,101,112,108,97,121,95,118,49,46,106,115,111,110],CharInt);;
D972_B4_METABELIAN_AUTOMATA_PREFIX:=List([99,105,47,111,117,116,47,100,57,55,50,95,98,52,95,117,95,109,101,116,97,98,101,108,105,97,110,95,107,98,109,97,103,95,97,117,116,111,109,97,116,111,110],CharInt);;
D972_B4_METABELIAN_LARGE:=false;; D972_B4_METABELIAN_FILESTORE:=false;; D972_B4_METABELIAN_DIFF1:=false;; D972_B4_METABELIAN_MAXEQNS:=250000;; D972_B4_METABELIAN_MAXSTATES:=250000;; D972_B4_METABELIAN_MAXWDIFFS:=250000;; D972_B4_METABELIAN_MAXSTOREDLEN:=[4000,4000];;
D972_B4_METABELIAN_V2_POST_REPLAY:=true;;
```

This is dispatch-ready only; no A/B result is claimed before GHA Read,
KBMAG, v1 replay, and the independent v2 checker all pass.

## Raw-RS to dense-127 trace handoff (2026-08-16)

The proof-oriented transport lane is now the pure-Python fixed-basis producer
`search/d972_b4_norm_tietze_trace_v2.py`; the earlier GAP
`PresentationAugmentedCosetTable` draft is intentionally not part of this
handoff because its raw Schreier tree/conversion-map assumptions were not
replayed.  The producer pins source `c61b2b...`, relator `12fc...`, corrected
word artifact `564a921b...`, exact 972 norm `ecf0cc...`, raw RS
`29c65a...`, and RS-norm `f7134e...`.  It records all 34 elementary
one-occurrence substitutions, defining row/pivot/sign, before/after
presentation and norm digests, stable 161-generator maps, and the final
dense maps/relators/norm ledger.

Parent's independent full run after the map-snapshot repair replayed all
34 steps and all 972 norms: final generator count `127`, empty norms `2/972`,
final relator digest
`1b4e1e86405dd348d633e706f0a66210df243dc2cbb4a04ed176bb452e2b2439`, final
norm digest
`49b90fb6215f425703cd59dc405048edd2db6e7ca24d062e8833473ccaf6042e`, and
the independent checker returned PASS (receipt SHA prefix `87a7e766`).
The two empty rows are therefore not a B result: the remaining 970 words
must pass a sound replay or KBMAG/automatic certificate route.

The producer's regression selftest now uses two successive eliminations to
ensure earlier `new_to_old` snapshots are value-copied rather than aliased.
The current light checks are:

```text
producer --selftest                 PASS
independent dense checker --selftest PASS
Python py_compile                    PASS
KBMAG consumer bare QUIT scan        PASS (none)
KBMAG consumer undefined-call scan   PASS (none)
```

Current source hashes after these fixes:

```text
5ec4602524ff470e4b62b7625177481c22f087ab058c85a5bd53276967fad67f  search/d972_b4_norm_tietze_trace_v2.py
462ee5bc43432e4f97428304b601b16bfb0aeabf2ce6f4ffdaed67939d438cbd  search/d972_b4_norm_tietze_kbmag_consumer_v2.g
10da50ccdc4291aaa81ed44a33c24d28926fba8ba45e9b2eb2d6d2cb7cf14388  crosscheck/check_d972_b4_norm_tietze_dense_v1.py
```

The GHA same-job order is: (1) run the producer with the pinned canonical
input and word-artifact paths, writing
`ci/out/d972_b4_norm_tietze_trace_v2.json`; (2) run
`crosscheck/check_d972_b4_norm_tietze_dense_v1.py` against that receipt and
write its checker receipt; (3) only if the checker accepts the dense artifact,
`Read("search/d972_b4_norm_tietze_kbmag_consumer_v2.g")` with
`D972_B4_NORM_TZ_ARTIFACT:="ci/out/d972_b4_norm_tietze_trace_v2.json";;`.
The GAP consumer remains candidate-only: an all-empty 972 ledger needs a
separate sound replay/axiom receipt; a nonempty normal form is an A candidate
only after independent replay and finite-image validation.

## Single-job Python/checker/KBMAG driver (2026-08-16)

Added the versioned generic-run target
`search/d972_b4_norm_tietze_gap_driver_v1.g`.  It is safe in the workflow's
`Read(...)` wrapper and contains no `QUIT`.  In heavy mode it performs, in one
GAP job:

1. fixed `python3 -B` producer command with `--max-steps 34`,
2. fixed independent checker command, requiring exit status zero and exact
   checker schema/status (`UNKNOWN_STAGE_LIMIT`), 34 steps, 127 generators,
   `2/972` empty norms, and the pinned final relator/norm digests, then
3. `Read` of the dense KBMAG consumer with the checked trace path.

The driver also builds the setup-gap KBMAG source with the fixed
`/home/runner/gap/pkg/kbmag` and `/home/runner/gap` paths when bootstrap mode
is enabled.  Every Exec command writes an explicit status file; all command
paths are source constants and shell-quoted/rejected if unsafe.  The driver
writes `ci/out/d972_b4_norm_tietze_gap_driver_v1.json` and emits a final
marker only after the consumer receipt passes its candidate schema gate.  It
never promotes all-empty KBMAG output to B: the driver receipt is explicitly
`KBMAG_CANDIDATE_PENDING_REPLAY`.

Exact generic `gap-run` dispatch:

```text
script: search/d972_b4_norm_tietze_gap_driver_v1.g
out_dir: ci/out
with_pquot_packages: true
timeout_min: 350
precheck preamble: D972_B4_NORM_TZ_SELFTEST:=1;; D972_B4_NORM_TZ_BOOTSTRAP:=0;;
heavy preamble:   D972_B4_NORM_TZ_SELFTEST:=0;; D972_B4_NORM_TZ_BOOTSTRAP:=1;;
```

Equivalent parent-owned dispatch command:

```text
gh workflow run gap-run.yml -f script=search/d972_b4_norm_tietze_gap_driver_v1.g -f out_dir=ci/out -f timeout_min=350 -f with_pquot_packages=true -f 'preamble=D972_B4_NORM_TZ_SELFTEST:=0;; D972_B4_NORM_TZ_BOOTSTRAP:=1;;'
```

Light checks pass: producer/checker selftests, Python compilation, ASCII
source check, lexical GAP delimiter check, and no-bare-`QUIT` scan.  Current
driver SHA:

The consumer and driver JSON serializers test empty lists before `IsString`,
because GAP 4.16's empty-list object also satisfies the string filter.  This
keeps the two empty norm rows as JSON `[]` rather than `""`; the driver also
allows only the three explicit candidate statuses from the consumer.

```text
28ae660955b48487a39ba59105bd5a7294cf5c73df9e340dc42a913b7779cd8a  search/d972_b4_norm_tietze_gap_driver_v1.g
5ec4602524ff470e4b62b7625177481c22f087ab058c85a5bd53276967fad67f  search/d972_b4_norm_tietze_trace_v2.py
46bbe8e55c0c785c6826ba8edde7e7c4a73a51cf284112274a264f638fd3fd9b  search/d972_b4_norm_tietze_kbmag_consumer_v2.g
10da50ccdc4291aaa81ed44a33c24d28926fba8ba45e9b2eb2d6d2cb7cf14388  crosscheck/check_d972_b4_norm_tietze_dense_v1.py
```
