# Luna reply 187 — R07 `u0/v0` boundary-preimage shortcut v1

Date: 2026-08-27
Role: bounded mechanical implementation. No Python, GAP, Node, git, GHA, or network execution was performed.

## 1. Mathematical objective

Implemented a fresh boundary-only F3 echelon over the fixed task179
all-seven runtime. The producer selects the unique q0-relator ordinals
`r3,r9,r12` and constructs literally

```text
v0 = r9 r12 r3^-2,  exp(v0)=(0,18)
u0 = r9 v0^-8,       exp(u0)=(18,0).
```

Integer exponents are computed by the new signed-letter counter. The task179
`exponent_pair` is never used as an integer-exponent source; its mod-3 result
remains confined to the authenticated task179 arithmetic path. `A(u0)` and
`A(v0)` are replayed by the literal direct all-seven route, and only the two
explicit exponent keys are removed before the decisions.

## 2. Authenticated sources

The task179 producer, independent checker, task179 driver, fixture, v156, and
v157 are pinned by exact bytes and SHA-256 in both new Python files. The
current bundle driver separately pins all four new machine artifacts. The producer
also calls task179's complete arithmetic-input authentication gate before
runtime reconstruction; its returned arithmetic pin manifest is carried in
the receipt and checked independently.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_u0v0_boundary_preimage_v1.py` | 35173 | `18040f4f73fe963632bbd2200e730818a7354c5963143a5871e73b2d1284dbfe` |
| `crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py` | 32825 | `e94d19311d0afe23fde869045f959490528d18e0f3537209e57b7cbefb452b18` |
| `search/d972_r07_u0v0_boundary_preimage_gha_driver_v1.g` | 7721 | `16d354d387db53cfadd22a7442f9a7aa77580c8410664f9dd5b1a618fef026b8` |
| `search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json` | 699 | `230de05643a94f775120ef7e62b2f2023b13fd12228f18ca860ef81b134babff` |
| `sol/luna_reply_187_r07_u0v0_boundary_preimage_v1.md` | final reply file | self-identity intentionally not embedded |

The four predecessor identities used by the bundle are task179 producer
`123870 / 47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7`,
checker `73780 / de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d`,
driver `12872 / 48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b`,
fixture `407 / 46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78`;
v156 is `10409 / 2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d`,
and v157 is `8367 / 08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8`.

## 3. Producer

`full_boundary_correlation` scans every support-times-occurrence pair in all
two PB3 and eleven PB4 rows. It reconstructs `t=g*h^-1`, checks `t*h=g`,
accumulates modulo 3 only after the literal translation check, and marks the
scan `complete=true, sampled=false`. Active rows are selected by the frozen
lexicographic `(block,translation_blob,relator_index)` order. Every retained row must raise
rank, and each column stores its sparse row, active dual, pairing, pivot,
ordered ancestry, block/translation/relator-index provenance, and complete contributors. Boundary
occurrence inverses and dual-support group values are precomputed once per
correlation call, preserving the exact pair count while avoiding repeated
finite-group work.

The two target remainders are reconsidered after every rank increase. A
positive terminal stores `MEMBER_D`, the ordered boundary chain, literal sum,
and exact zero residual. A negative terminal stores `NONMEMBER_D` only with a
dual annihilating the retained and complete translated boundary family. Any
resource stop is typed `UNKNOWN_RESOURCE` and never converted to nonmembership.

If both targets are members, the receipt records
`nu(ker(A on correction plus boundary coefficients)) = F3^2` and the exact
v161 rule `c1=c q(u0,a) q(v0,b)`, `d1=d-a*d_u-b*d_v`, with
`q(w,0)=1`, `q(w,1)=w^-1`, `q(w,2)=w`; registered cubes exactify the integer
exponent. No raw task179 word is claimed.

## 4. Independent checker

The checker does not import the new producer. It loads the authenticated
task179 independent checker, reconstructs its finite arithmetic and roster,
recomputes all five integer exponents and normalized residues, checks all five
joint-kernel evaluations, and independently recomputes `A(u0),A(v0)`.

It replays each translated boundary row, complete contributor list, frozen
least-active selection, active dual, rank transition, pivot ancestry, and
chain coefficients. For `NONMEMBER_D` it independently reconstructs the
terminal dual and requires exact equality with a complete empty correlation.
Both-positive consequence and the corrected negative-power normalization
rule are checked as conditional receipt fields.

## 5. SELFTEST and controls

The bounded noncommutative toy has one target in the boundary span and one
outside. Two base rows are enumerated over all six S3 left translations (the
component-2 identity is explicitly checked in-orbit), while the outside
target is a typed component-3 basis vector absent from that complete family.
Its second retained row overlaps the first, forcing coefficient-2 elimination
and nontrivial ancestry. The fixture records the positive chain, negative
dual, complete-correlation flag, and rank transitions.

The toy uses explicit noncommuting S3 permutations, computes a literal left
translation `t*h`, and materializes typed block keys before echelon replay.
Fifteen mutation controls are routed through the actual toy echelon and dual
replay: roster ordinal, exponent sign, both word formulas, target sign, block
tag, boundary coefficient, left translation, coefficient-two inverse, pivot
ancestry, positive residual, terminal dual coefficient, sampled-as-complete,
resource-stop-as-nonmember, and boundary provenance. All fifteen are expected
to reject.

## 6. Driver and controls

The GAP driver is ASCII-only and serial. It authenticates the four new
machine artifacts and all six registered predecessor/proof sources, rejects
stale outputs, writes one shell, enforces exact producer/checker markers, and
touches the completion sentinel only after matching terminals. Production
allows only the boundary-preimage terminal or typed `UNKNOWN_RESOURCE` /
`UNKNOWN_INPUT`. Suggested conservative GHA limits are 19,800 seconds,
8,000,000 boundary pairs, 250,000 retained columns, and 5.7 GB RSS; the
producer also checks wall/RSS limits internally. The fail-closed resource
phase table admits only the authenticated task175/task176 reconstruction
phases (`task175_reconstruction`, `fine_deletion`, `Q0_positive_shortlex_section`,
`Q0_discovery`, `A_L_membership_scan`, `L_subgroup_closure`,
`typed_singleton_equality`), plus `runtime_reconstruction`,
`complete_boundary_correlation`, and `boundary_echelon`, with only their
registered wall/RSS or boundary-pair/retained-column caps.
The production shell now extracts exactly one terminal from each anchored
producer/checker marker and compares the two terminal strings byte-for-byte
before touching the completion sentinel.

## 7. Execution boundary

No local execution was performed. The parent Sol controls audit and any GHA
SELFTEST/PRODUCTION run. The implementation is bounded to the first-rung
boundary-preimage selector and makes no cofinal, fake, or Ihara claim.

Dispatch record: GHA run `33071521623` encountered a producer SELFTEST
`SyntaxError` caused by a missing outer return-dictionary brace. This is a
syntax-only candidate failure; it produced no mathematical result and is not
evidence for either boundary-preimage decision. The missing brace is repaired
in the producer.

Dispatch record: GHA run `33071845558` reached the producer but encountered a
runtime-contract failure because the bounded SELFTEST `Budget` namespace did
not provide all registered resource attributes. This is likewise a
syntax/runtime-only candidate failure with no mathematical result; the
SELFTEST namespace now supplies every `Budget` constructor field.

Dispatch record: GHA run `33072235499` produced a PASS receipt, but the
checker rejected the independent toy certificate. This is a checker-certificate
contract failure only, with no mathematical result; the checker now reports
the exact mismatching toy receipt or fixture field while retaining strict
independent equality.

Dispatch record: GHA run `33072786153` passed the producer and independent
checker SELFTESTs, but the wrapper reported a missing completion sentinel.
This is a wrapper-sentinel failure only (no production mathematical result);
the driver now writes a fixed nonempty ASCII sentinel and verifies its exact
contents before reporting completion.

Dispatch record: GHA run `33073247508` again passed producer/checker SELFTESTs,
but failed the wrapper postcheck on the sentinel. The duplicated post-run
existence probe is removed; the postcheck now performs a direct `StringFile`
read and rejects fail, empty, or mismatched sentinel content. This run has no
production mathematical result.

Dispatch record: GHA run `33073632603` emitted producer/checker PASS markers,
but the wrapper failed before sentinel completion. The driver is simplified to
direct `python > logfile 2>&1; cat logfile` execution with `set -e`, explicit
producer/checker/process/marker stage markers, exact marker gates, and a
nonempty sentinel write after all gates. This run is a wrapper failure only
and has no mathematical result.

Dispatch record: GHA run `33074324149` showed the checker PASS line and
checker-process stage, but the fragile SELFTEST `grep -Fxc` marker gate failed.
This is a wrapper-only failure with no mathematical result; the SELFTEST gate
now prints matching marker lines diagnostically, extracts exactly one anchored
terminal, and compares it to the authenticated SELFTEST terminal string.

Dispatch record: GHA run `33074806399` isolated that wrapper failure to GNU
`grep: Trailing backslash` after the checker-process stage. The checker itself
returned zero and printed the expected PASS line. The SELFTEST postcheck now
uses shell `read -r`, exact full-line equality, and an exact one-line count,
with no regular-expression parser. This run used commit
`5dd8c668ea4d11d5f4e0fb67a6bf5559e0d705a7` and has no mathematical result.

Dispatch record: GHA run `33075126873` showed that even the shell-builtin
postcheck was split before completion. The common cause is now identified:
the GAP output stream retained print formatting, so long generated shell
lines were folded with continuation backslashes. The driver now calls
`SetPrintFormattingStatus(D187Stream,false)` before writing any shell text.
This was a wrapper-only failure and produced no mathematical result.

GHA SELFTEST run `33075481646`, commit
`257d01e154f020901d24b96599da5a9602e58913`, completed successfully: producer,
independent checker, all driver gates, final sentinel, and artifact upload
passed. This authenticates the bounded SELFTEST only. Production run
`33075593185` was then dispatched from the same commit with the registered
19,800-second and resource caps; it is in progress and has no result yet.

U0 BOUNDARY PREIMAGE:                       NOT EXECUTED BY LUNA
V0 BOUNDARY PREIMAGE:                       NOT EXECUTED BY LUNA
RAW-TO-NORMALIZED SHORTCUT:                 NOT DECLARED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:     NOT DECLARED

## 8. Parent GHA dispatch record

The parent Sol committed the initial bundle as
`288076fd7cc1d1246a721c3ecb30ac90bb499ed3` and dispatched GHA run
`33071521623`; that run exposed only the brace defect recorded above.  The
brace repair was committed as `91aa747becfb599c682a84040adb30d70c0777a0`
and dispatched as run `33071845558`; that run exposed only the bounded
`Budget`-namespace defect recorded above.  That repair was committed as
`bb5094070327bcbc38ffbea79b69f469a536d0ae` and dispatched as run
`33072235499`; the producer passed and the checker exposed the stale fixture
row recorded above.  None of these runs produced a boundary-preimage
decision.
