# task381 fresh independent static code/performance reaudit — pre-A0 A3/v4

## 0. Decisive result and boundary

**STATIC REJECT.**  The five task374 repair families are present in the two
Python owners: the evaluator adapters call real meter methods, the accepted
31,017,244-byte task198 receipt is authenticated once per process, mutations
are owner-local, the elapsed-adjusted outer deadline covers the whole normal
route, and both receipt/verdict writers fsync the bound directory after
pre-/post-rename rollback.  The mathematical route, including the v303-only
projection, one producer closure, one independent checker verifier, and the
twelve ordinary mutations, is statically coherent.

Authorization nevertheless fails at the accepting sentinel.  Driver
223--228 swallows an unlink or rollback-directory-fsync error.  If the exact
sentinel bytes have already been written and a file/directory fsync (or close)
then fails, a failed unlink can leave those exact bytes in place.  The helper
and bash then exit nonzero, but driver 236 uses GAP `Exec` without observing
the exit status, and 237--240 accepts solely from the surviving sentinel.
This is a concrete fsync/rollback-failure accepting path forbidden by task381
Sections 7--8.  GAP 4.16's installed `lib/process.gi` 261--263 confirms that
`Exec` calls `Process(...)` and discards its returned process status.

There is also avoidable whole-owner processing: the driver fully parses,
canonicalizes, and body-seal-traverses the same at-most-19,000,000-byte receipt
before the checker (98--133) and again in its final binding validator
(154--200), with the pinned checker independently doing the same work.  The
intermediate receipt hash at 147--148 is redundant with the immediately
following final validator's in-memory hash at 176 and required post-validator
rehash at 203--204.  Further exact duplicate hashes are inventoried in Section
7 below.  Therefore no A3/v4 candidate is authorized.

I did not run the producer, checker, driver, Python, Node, GAP, GHA, workflow,
git, network, syntax/import compilation, mutations, RSS sampling, or any
candidate.  Inspection and hashes were read-only PowerShell operations.  The
only written owner is this designated reply.

## 1. Frozen physical owners

All five task381 subjects are ordinary, non-reparse physical files and match
the frozen bytes/SHA-256 exactly.

| owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v4.prereg.v1.json` | 16,417 | `14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae` |
| `search/d972_r07_pre_a0_single_target_a3_v4.py` | 104,369 | `171e73dab2bd27f638021ceea43d8fb96ec4623a13d45873f364114e4290badd` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v4.py` | 115,675 | `eb07e34164f27b6676b97c722fb0fb2ef87b1e971baaab3d18c26770f17b7804` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v4.g` | 20,111 | `78ee39b6f8926c267cb24d6b15bdc3a961906cdb8ddf9de8f7668222a5113f91` |
| `sol/sol_reply_377_r07_pre_a0_a3_v4_bounded_repair.md` | 15,911 | `7c8c3692ea9e8dc508f59c72014479ac897a3247aa3cdf91d48d748d8e19fde4` |

The driver is 240 LF-terminated ASCII lines, with no BOM, CR, or non-ASCII
byte.  Its P0/producer/checker pins at 15--22 are exactly the first three rows
above; there is no retained v3 final-owner hash or path.

## 2. Canonical P0 and one-way authority graph

Independent PowerShell reconstruction gives compact canonical ASCII identical
to the 16,417 physical bytes.  There is no BOM, CR, or LF; the first/last bytes
are `{`/`}`, so the exact terminator is `0x7d`.  Removing the top-level
`self_digest_sha256` field and canonically reconstructing the root body gives
16,329 bytes and
`f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7`,
equal to both the declared body seal and both machine pins.

The recursive walk stops at every keyed ordinary `{path,bytes,sha256}` owner,
including owners nested in lists.  It yields exactly 23 unique normalized
paths and exactly 33,121,619 bytes.  Every row matches its current ordinary,
non-reparse physical file:

| path | bytes | SHA-256 |
|---|---:|---|
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt` | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json` | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt` | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| `crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py` | 35,463 | `e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 34,200 | `028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95` |
| `search/check_d972_b345_joint_kernel_qstar_closure_v1.py` | 47,661 | `9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f` |
| `search/check_d972_b345_seedspan_triple4_v1.py` | 574,347 | `ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981` |
| `search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 33,409 | `f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f` |
| `search/d972_b345_joint_kernel_qstar_closure_v1.py` | 67,945 | `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc` |
| `search/d972_b345_seedspan_triple4_v1.py` | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `search/d972_r07_760_l3_target6_v1.py` | 53,284 | `7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde` |
| `search/d972_r07_actual_two_word_endpoint_specializer_v2.py` | 40,556 | `a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g` | 5,387 | `38352fd53e2aa2534e6b4d61c5a613c38fd65c4a6843fa5cb6dd2a04918cfe7d` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 47,135 | `755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e` |
| `sol/proof_r07_a18_area_invisibility_single_a3_target_v302.md` | 7,340 | `ba508bbe96f34967ebe456c51285ecbe774861a864c369699bbf1dce2b9fc6c3` |
| `sol/proof_r07_pre_a0_computational_base_equivalence_v303.md` | 6,739 | `9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2` |

There is no duplicate, extra, missing, aliased, partially pinned, or skipped
owner.  P0 excludes itself and the v4 machine/driver owners; the machines pin
P0, and the driver pins the machines.  The graph is therefore exactly
`23 immutable authorities -> P0 -> producer/checker -> driver`, with no back
edge or cycle.

## 3. F1 — accepted authority and live evaluator

The accepted task198 receipt has body seal
`c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`;
the 2,722-byte manifest has body seal
`0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`.
The evaluator contract digest is
`4fc38881ffee293f0820d3639230dd44a2af9b9ed126dfb21dc5831290ff08b8`,
and the literal 11-row ledger digest is
`040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`.

Producer `EvaluatorBudget.check` 1236--1238 calls the existing
`Meter.check_wall` at 233--238.  Checker `EvaluatorBudget.check` 1437--1439
calls its existing `Meter.check` at 215--220.  Frozen task176
`build_fine_deletion` 428--447 calls `budget.check` already at `sid=0`
because `(sid & 1023)==0`; the later Q0/membership/closure scans likewise
check at their zero index.  The build functions' `except BaseException`
clauses only release reservations and immediately re-raise.  No broad catch
turns a missing method into UNKNOWN, and `AttributeError` is absent from both
main UNKNOWN catch rosters.

The producer obtains all six live callables from the accepted task198
registry (producer 1340--1356); the checker calls its six checker-local
functions directly (checker 1533--1552), not a producer receipt summary.
Source expansion gives:

| side | direct `eval/multiply/inverse/source/action/cocycle` | actual transitive `eval/multiply/inverse/source/action/cocycle` |
|---|---|---|
| producer | `3/1/2/1/1/1` | `6/4/3/1/1/1` |
| checker | `3/1/2/1/1/1` | `8/4/3/1/1/1` |

The producer source-section contains one multiply and one replay eval;
action contributes one eval, two multiplies and one inverse; cocycle
contributes one eval.  The checker source-section independently contributes
three evals and one multiply, which accounts for its transitive `eval=8`.

All live values are exact ten-coordinate lowercase-hex values with byte widths
`[40,40,40,40,40,154,154,154,154,154]`.  Static extraction of the accepted
canaries gives canonical value-array fingerprints:

| value | coordinate count | canonical SHA-256 |
|---|---:|---|
| `x` | 10 | `217d7fe2704a8ee64ec504a6d7d685d25e0513165ad1fba96cf5fc76dd9dd57f` |
| `y` | 10 | `c1bffa7c46ef9e46ce82bfbbd8be7baf11595380300ec1427da0f091069f319f` |
| `xy` | 10 | `16c1b7c1799b2f201e737c4ceb44520c9ed852a9829005687029f9a8fcf371e1` |
| `x_inverse` | 10 | `a0f8cad48600aca8ea6a22445632c15d45bbe34973529add26086ce3246ff45c` |
| `source_2_2.value` | 10 | `6a4e10ec6064421bd63815a2beb1a906304b0eab6256287b2e0ad8732b3ac131` |
| `x_action_y` | 10 | `0b0d62051c5054b19830826fc6f211191d5dc4c644440a5ead79bcd0b2b763f8` |
| `xy_section_cocycle` | 10 | `c2d1919f6482674962871bcf3226bfa71cd1e0409542cc9be624ea15d02d3728` |

The whole accepted canary object is 16,464 canonical bytes with SHA-256
`6fb8df36710628faded5438e993a21416809e056b214c5a732aac05688fb66d0`.
Both sides compare every listed live result to those accepted values and
derive `g760`/`g760_inverse` live rather than accepting serialized summaries.

The occurrence binding is exact:

| ordinal/name | ten index | width | sign | orientation |
|---|---:|---:|---:|---|
| 1 `H1_fxy` | 0 | 40 | +1 | direct |
| 2 `H1_fxz` | 1 | 40 | -1 | inverse |
| 3 `H1_fyz` | 2 | 40 | +1 | direct |
| 4 `H2_fux` | 3 | 40 | -1 | inverse |
| 5 `H2_fxy` | 0 | 40 | -1 | inverse |
| 6 `H2_fuy` | 4 | 40 | +1 | direct |
| 7 `P_b1` | 5 | 154 | +1 | direct |
| 8 `P_b2` | 6 | 154 | +1 | direct |
| 9 `P_b3` | 7 | 154 | +1 | direct |
| 10 `P_b5_inverse` | 8 | 154 | -1 | inverse |
| 11 `P_b4_inverse` | 9 | 154 | -1 | inverse |

Thus the ten-to-eleven insertion is `[0,1,2,3,0,4,5,6,7,8,9]`, signs are
`[+,-,+,-,-,+,+,+,+,-,-]`, and every sign/orientation/value selection is
checked at producer 1381--1398 and checker 1576--1594.

## 4. F2/F3 — authenticate once and owner-local mutations

`read_bytes` performs the sole physical raw SHA for each 31,017,244-byte
task198 receipt (producer 400--430; checker 354--384).  Producer 760--967 and
checker 737--932 then perform exactly one `json.loads`, one full raw/canonical
comparison, and one body-seal traversal.  Neither route subsequently hashes,
parses, canonical-compares, seals, nor rereads that large owner.

The recursively immutable snapshot is `MappingProxyType` for every mapping and
tuple for every list (producer 657--672; checker 635--650).  It carries the
receipt path/basename/bytes/raw SHA/body seal; manifest owner path/bytes/raw
SHA/body seal; complete manifest contract; accepted member tuple; exact
producer/checker attestation owners and texts; checker-verdict owner and
content; task198 source identities; run/head/artifact/zip acceptance binding;
and decoded ledger/evaluator contract/canaries.  It carries no receipt DOM or
31-MB canonical clone.

The real raw mutation changes only the extant 2,722-byte manifest receipt SHA,
reseals that manifest, and shallow-copies only the raw-owner dictionary
(producer 970--1003; checker 935--969).  Before/after physical SHA inequality
is proved before the validator call.  Baseline and mutant both enter the same
`validate_task198_binding_snapshot`; the mutant reaches exact first reason
`task198 raw/manifest binding` at producer 696--697 / checker 673--674 before
manifest seal/raw checks and without touching the large receipt.  The snapshot
is then deleted and retained raw owners are cleared at producer 2148--2156 /
checker 2395--2406.

Both sides pass the untouched ordinary baseline and the same exact twelve-row
roster:

| mutation | ordinary validator | exact first reason |
|---|---|---|
| `task198_raw_manifest_binding` | `validate_task198_binding_snapshot` | `task198 raw/manifest binding` |
| `task198_ledger_sign` | `validate_ledger_owner` | `task198 ledger sign` |
| `task198_prefix` | `validate_ledger_owner` | `task198 ledger prefix` |
| `g760_letter_digest` | `validate_g760_owner` | `g760 digest` |
| `computational_base_mode` | `validate_base_owner` | `computational-base mode` |
| `forbidden_task192_binding` | `validate_base_owner` | `task192 binding` |
| `H1_central_row` | `central_replay` | `H1_central_row` |
| `H2_central_row` | `central_replay` | `H2_central_row` |
| `P_central_row` | `central_replay` | `P_central_row` |
| `projected_area_target` | `target_from_fox` | `projected area target` |
| `ABI_seal_target` | `validate_projection` | `ABI seal/target` |
| `forbidden_conclusion_flag` | `validate_false_flags` | `forbidden conclusion flag` |

The allocation inventory is owner-local: the two ledger cases allocate one
11-slot list and one row dictionary; `g760` allocates one 760-entry list; the
two base cases allocate one shallow top dictionary; each central case allocates
the central/block/row path only; projected target allocates its two small
constructor branches; ABI target allocates a shallow consumer plus its target
block; the flag case allocates one eight-key dictionary.  The fixture itself
only groups references.  There is no per-case full fixture/reference,
task226 ABI, interface, consumer, P0, receipt, or canonical-roundtrip clone.
Every case proves owner digest inequality, catches only its mapped narrow
reason, and hard-fails `MutationAccepted` or a wrong reason (producer
1770--1936; checker 1711--1875).

All eight flags — `actual_a3_numerator`, `boundary_membership`, `cofinal_lift`,
`exact_pb_endpoint_zero`, `fake`, `Ihara_witness`, `pointed_mu1`, and
`task192_consumed` — are required false at P0, receipt, result, gate, verdict,
and driver acceptance layers.

## 5. V303 projection and the one closure/one verifier routes

V303 (1.6), Theorem 3.1, and (4.1) establish equality only for the projection
consumed by the pre-A0 A3 gate, not equality of full task226 packages.  The
machine projection at producer 1599--1653 / checker 1342--1392 contains the
ledger/quotient codecs, eleven occurrence fields, `w`, `u0`, and the three
target blocks.  Full literals, `B_a`, exact PB chains, task192 ancestry, and an
actual corrected word are excluded.  Consumer fields are exactly
`schema/modulus/ten_to_eleven/occurrences/bar_epsilon_1/u0`; the presence-only
`rword_f` and `rword_g` values are both exact
`V303_OMITTED_NOT_CONSUMED`.

Producer 2203--2216 calls frozen task227 `closure` exactly once and checks the
post-call 486/729 rosters.  No checker verifier or reverse closure occurs on
that side.  Checker 2282--2309 calls frozen checker `verify_gate` exactly once;
no producer closure is called there.  Frozen `verify_gate` reconstructs the
ABI, occurrence ancestry, rank/echelon and block map; checks exact 486 ideal
rows and 729 translates; makes 12 internal directed span comparisons; and
checks MEMBER replay or NONMEMBER dual annihilation/target pairing.  The v4
wrapper makes zero reverse/second-closure calls.  These clauses PASS.

## 6. F4 and source-derived resource arithmetic

Producer outer deadline 2277--2283 covers output preflight, P0/authority,
snapshot/raw mutation, imports, evaluator, base plus three area builds,
projection/seals, all mutation copies/validators, the sole closure, receipt
serialization, and publication.  Checker outer deadline 2384--2429 covers the
corresponding independent route, production receipt parsing, sole verifier,
verdict serialization, and publication.  Emergency publication uses the same
meter's remaining elapsed time (producer 2305--2312; checker 2451--2459).
Nested timer restoration subtracts actual elapsed time from the prior timer
(producer 353--363; checker 308--318) and fails if it expired.

Both processes require Linux `RLIMIT_AS`, `SIGALRM`/`ITIMER_REAL`, and
`renameat2`; absence/failure cannot enter an accepting route.  The strict wall
ordering is `1800 < 2100` and `2*2100 = 4200 < 21600`, and the driver starts the
two candidate processes serially.

| bounded quantity | independent source formula | bound/cap |
|---|---|---:|
| authority inventory | recursive 23-owner sum | 33,121,619 bytes |
| P0 + authority | `16,417 + 33,121,619` | 33,138,036 `< 40,000,000` |
| producer six source imports | exact size sum | 894,133 bytes |
| producer input | `16,417+33,121,619+2*894,133` | 34,926,302 `< 60,000,000` |
| checker seven source imports | exact size sum | 1,450,252 bytes |
| checker before produced receipt | `16,417+33,121,619+2*1,450,252` | 36,038,540 bytes |
| checker with maximum receipt | `36,038,540+19,000,000` | 55,038,540 `< 60,000,000` |
| producer normal fixed-point component | `3*19,000,000+65,536` | 57,065,536 bytes |
| failed normal + emergency charge | `57,065,536+4*65,536` | 57,327,680, cap exact |
| checker verdict fixed-point component | `3*1,000,000+65,536` | 3,065,536 bytes |
| checker private Q0 | `5*1,469,664`; construction `2*` | 7,348,320; 14,696,640-byte component peak |
| hard total address-space ceiling | Linux `RLIMIT_AS` | 4,294,967,296 bytes |
| walls | internal / each external / serial / workflow | 1,800 / 2,100 / 4,200 / 21,600 s |

The evaluator build formula is
`26+243*26+59,049*6+243*10 = 363,068 < 1,000,000` operations.  Task226 is
base build 1 plus area builds 3 per side; producer closure is 1; checker
verifier is 1.  Mutation work is 12 per side.

Simultaneous-object reasoning is also bounded.  During task198 authentication,
the retained raw map and the one large DOM coexist; the DOM is dropped after
the compact frozen snapshot is made, and all large authority raws are released
before task226/closure work.  In the checker, the 7,348,320-byte private Q0
copy is local to evaluator reconstruction and is no longer returned when the
at-most-19-MB production receipt DOM is constructed.  Loaded modules,
task226/closure structures, receipt/verdict objects, and serializer objects
are Python objects rather than payload-byte-equal quantities; the formulas are
component bounds, while the 4-GiB `RLIMIT_AS` is the hard simultaneous total
ceiling.  RSS samples are boundary telemetry, not in-call interrupts, and no
observed RSS/time is claimed because this audit did not execute a candidate.

## 7. Avoidable duplicated processing — REJECT

The caps and deadline envelopes above are arithmetically sound, but task381's
zero-avoidable-full-owner performance condition does not pass:

1. Driver 98--133 fully parses the produced receipt and performs a complete
   canonical reconstruction plus body-seal reconstruction before invoking the
   pinned checker.  The checker itself performs those validations at
   1908--1938 and fully reconstructs the result at 2219--2367.  Driver
   154--200 then again reads/parses/canonically reconstructs/body-seal-checks
   the same receipt to bind the accepted verdict.  The first helper's full
   receipt work is redundant with the pinned checker plus the final binding
   helper and adds two avoidable full receipt serializations.
2. Driver 147--148 hashes the full receipt after the checker, immediately
   before the final helper opens it and proves `sha(rraw)==rsha` at 176.  The
   required post-validation physical rehash remains at 203--204.  The
   intermediate `rsha2` full pass can be removed without weakening injection,
   in-helper binding, or post-validation stability.
3. Checker `read_receipt` hashes the full produced receipt at 1928--1929, but
   `verdict_document` hashes the same retained immutable bytes again at
   2103--2105 merely to print the already-known digest.  Passing the authenticated
   digest forward avoids one more at-most-19,000,000-byte full hash.
4. Each producer source `read_bytes` already hashes its immutable bytes at
   430, yet `load_engine` hashes the same pre-read bytes again at 1961; its
   post-read is already hashed by `read_bytes`, then immediately hashed again
   at 1964.  That is `2*894,133 = 1,788,266` avoidable hashed bytes.  The
   checker repeats the same pattern at 384 versus 1899/1902, adding
   `2*1,450,252 = 2,900,504` avoidable hashed bytes.  The physical post-import
   reread itself is a legitimate drift boundary; only the duplicate hashes of
   the same immutable returned byte objects are defective.

There is no hidden second task226 build, closure, verifier, 31-MB task198 DOM,
or per-mutation full clone.  The rejection is limited to the concrete repeated
passes above, but those are precisely whole-owner work requested by the
performance audit.  Consequently both `AVOIDABLE DUPLICATED PROCESSING` and
the composite `STATIC CAPS / PERFORMANCE` line are REJECT, even though the
numeric caps and deadlines themselves pass.

## 8. F5 bound publication and serial-driver defect

The producer writer at 2044--2115 and checker writer at 2010--2082 PASS
line-by-line.  Each binds repo root -> `ci` -> `out` with
`O_DIRECTORY|O_NOFOLLOW`, creates the temp on that same directory fd using
`O_CREAT|O_EXCL|O_NOFOLLOW`, loops to a complete write, fsyncs and closes the
file, uses same-dirfd `renameat2(..., RENAME_NOREPLACE)`, then fsyncs the
directory.  On any pre-rename failure it unlinks the temp and fsyncs that bound
directory; on any post-rename directory-fsync failure it unlinks the final and
fsyncs the same directory.  `FileNotFoundError` still reaches directory fsync,
and any unlink/fsync/close rollback error is re-raised as a nonaccepting
`ResourceStop`.

The driver otherwise pins all final owners, rejects stale outputs/temps and
UNKNOWN, requires exact-one producer/checker terminals and zero accepting
process status, injects the receipt SHA into the checker, requires terminal
equality, validates verdict/P0/23-owner/projection/evaluator/mutation/rank and
resource cross-bindings, and performs final receipt/verdict rehashes.  Its
sentinel uses a no-follow bound directory chain, exclusive creation, exact
complete bytes, file fsync, and directory fsync (207--222).

The following failure trace is nevertheless accepting:

```text
sentinel exact bytes written
  -> file fsync or directory fsync raises
  -> rollback os.unlink raises, so sentinel survives
  -> driver 227 swallows rollback OSError
  -> helper exits nonzero; bash fail exits 40
  -> GAP Exec discards status
  -> StringFile sees exact surviving sentinel
  -> D363_DRIVER_ACCEPTED
```

A close failure raised from the `finally` block after a fully durable sentinel
can likewise make the helper nonzero while leaving the exact sentinel; GAP
still does not consult the status.  Thus `fsync failure must not accept` and
`rollback failure remains nonaccepting` are both violated.  Publication/driver
is REJECT.

A bounded repair must do all of the following together: (i) retain and expose
the sentinel rollback exception instead of `except OSError: pass`; (ii) invoke
bash through GAP `Process` (or another status-bearing primitive) and require
exact status 0 before reading the sentinel, so even a surviving rollback
failure cannot accept; (iii) preserve the exact exclusive/no-follow/file-fsync/
directory-fsync sentinel success route; and (iv) remove or consolidate the
avoidable full passes in Section 7, updating resource disclosure and frozen
hashes in a new version.  A fresh independent static audit is required before
one bounded serial GHA candidate can be authorized.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
P0 / ACYCLIC AUTHORITY GRAPH:          PASS
TASK198 AUTHORITY / LIVE EVALUATOR:    PASS
V303-ONLY PROJECTION SUFFICIENCY:      PASS
ONE PRODUCER CLOSURE ROUTE:            PASS
INDEPENDENT CHECKER ROUTE:             PASS
BASELINE + TWELVE MUTATIONS:           PASS
STATIC CAPS / PERFORMANCE:             REJECT
AVOIDABLE DUPLICATED PROCESSING:       REJECT
BOUND PUBLICATION / SERIAL DRIVER:     REJECT
PRE-A0 A3/V4 GHA:                      FORBIDDEN
ACTUAL A3 NUMERATOR:                   remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:      NONE

TASK381_R07_PRE_A0_A3_V4_CODE_PERFORMANCE_REAUDIT_V1
