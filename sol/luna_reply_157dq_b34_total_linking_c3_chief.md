# Luna reply 157dq - total-linking C3 chief descent

## Verdict

`B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED`.

The false-negative predicate exposed by run `32195410958` is repaired and the
same candidate-124 lane passed its same-job producer/checker replay in run
`32197397734`.  The repair changes only the PB3 joint-quotient onto test:

- the 30 strict coface intertwining equalities remain lossless diagnostics;
- they are no longer acceptance conditions;
- Definition 2.9 onto is certified by PB3 relation descent and joint-tuple
  generator recovery;
- the reverse relation/recovery direction remains an independently recorded
  diagnostic canary and is excluded from acceptance.

No candidate, 27-element fibre, literal hexagon/pentagon,
chief-factor, A5, order, outside-class, terminal-boundary, or resource gate was
changed.  No local production GAP, Git, or GHA command was run.

## Frozen files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b34_total_linking_c3_chief_v1.g` | 41483 | `d3096078bf1b7ff99dbf72ae6a1142c701e1db4d6cba31ca07bfabcaba0d64e8` |
| `search/check_d972_b34_total_linking_c3_chief_v1.py` | 57969 | `33aecc2fb86957addc9fc0cbc4c9bc0b30040dfe93a99b08391a317153617107` |
| `search/d972_b34_total_linking_c3_chief_gha_driver_v1.g` | 11632 | `1a6ae128c67d67fc7358365933c80000de737c6a982ff31dc74c3f21e205526c` |

The driver pins the exact producer and checker hashes above.  Existing q3,
FC8, 157dp, source, and theorem pins are unchanged.

## Mathematical correction

The primary 2008 GT-shadow definitions distinguish two statements:

1. Definition 2.9 and Proposition 2.10, p.17, require the induced PB3 map to
   be onto.
2. Proposition 2.11, equation (2.38), p.19, gives coface compatibility with a
   parenthesization conjugator `g`.

The superseded implementation tested, for each of five cofaces and three PB3
generators, the literal equality

```text
d_i(S_3(x_j)) = S_4(d_i(x_j))
```

and its inverse analogue.  This sets the conjugator in (2.38) to the identity.
That is stronger than Definition 2.9 and is not a valid rejection gate.

For each of the five actual `(Q4, Pi4[3], C18)` components, the repaired
producer and independent checker instead replay:

```text
S sends every PB3 defining relation to 1;
S(T_i) = x_i for i=1,2,3.
```

The first line makes `S` a homomorphism on the actual joint quotient; the
second recovers every marked generator, hence proves surjectivity.  The
following are retained losslessly as diagnostics, but are not acceptance
conditions:

```text
T sends every PB3 defining relation to 1;
T(S_i) = x_i for i=1,2,3.
```

The receipt separates these facts explicitly:

```text
definition_2_9_S_relation_descent
definition_2_9_S_of_T_generator_recovery
T_relation_and_T_of_S_canaries
T_canaries_required_for_acceptance = false
strict_global_intertwining_required_for_acceptance = false
strict_intertwining_not_Def2_9_gate = true
strict_intertwining_parenthesization_conjugator_not_forced_identity = true
strict_intertwining_diagnostic_pass
```

Each component carries the corresponding four per-component booleans and all
underlying residual words/values.  Its `pass` is exactly `S` relation descent
plus `S(T_i)=x_i`; neither T canary contributes.  At the outer source level,
T relations, `T(S_i)`, five-character rows, and the T exponent matrix remain
in the receipt and residual digest but do not feed `all_pass`.  The misleading old field
`global_E4_C18_automorphism_restricted_by_intertwining` is removed.  The
`inverse.found=false` branch emits the same exact top-level schema with false
acceptance fields.  Because the inverse word is certificate supply rather
than a literal negative predicate, its absence yields
`B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT`, never candidate REJECT.
The 27-fibre selector itself now chooses the first word satisfying only the
load-bearing `S(T_i)=x_i` equations; T relations and `T(S_i)=x_i` are computed
after selection as diagnostics and cannot indirectly suppress availability.

## Reclassification of run 32195410958

Run `32195410958`, commit `53f525f9`, produced and independently replayed the
following receipt under the superseded predicate:

```text
old terminal             B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED
receipt SHA-256          06dcf42a038ed16150814b9b2b38300d970acf4a7d7550ad63fd84e49fe30559
producer log runtime     5999 ms
receipt runtime_ms       5790 ms
literal residuals        131
inverse attempts         1
old checker              PASS
```

That token is now retracted as a mathematical rejection.  It established only
that producer and checker agreed on an overstrong implementation predicate.
It did not establish that candidate 124 fails Definition 2.9.

The old receipt localizes all twelve failures to strict Q4 intertwining:

- component 1: S/T, generators 1,2,3 (six records);
- component 3: S/T, generator 1 (two records);
- component 4: S/T, generators 2,3 (four records).

Components 2 and 5 pass those diagnostics.  Every failed diagnostic has
identity `Pi4[3]` value and zero `C18` residue.  More importantly, all five
components pass the PB3 relations and both three-generator recovery
directions.  Thus the old receipt supports the repaired onto gate but cannot
itself be promoted because its schema and checker pins predate this repair.

## Cross-checked repaired run 32197397734

Commit `80a20cdf5fd9022f7951834c7e450625e787876e` completed the repaired
producer and independent checker in the same job:

```text
GHA run                 32197397734
URL                     https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32197397734
terminal/status         B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED
artifact id             9346352687
artifact name           gap-run-out
artifact archive size   102420 bytes
receipt SHA-256         86dfc0cb513eacbc1d4df26a7ce6ae64d3f96b727351b413905eb5572376e326
receipt size            966678 bytes
receipt runtime_ms      5385
producer final runtime  5590 ms
literal residuals       131
inverse attempts        1
checker log SHA-256     b48198fe91d01a694a8e67397466c8b7921434e9f9c9b9d106f0f4a2fb8091d6
independent checker     PASS
```

The receipt independently replays the exact Definition 2.9 acceptance data:

- S relation descent is true;
- `S(T_i)=x_i` generator recovery is true;
- all five component `pass` values are true;
- source `all_pass`, the outside classifier, and FC-29 are true;
- twelve of the 30 strict intertwining records are false, but are explicitly
  diagnostic-only;
- all T canaries happen to be true and are explicitly not required.

The exact licensed conclusion is:

> One outside `GT^heart(L')` pair exists, and accepted T48-1 moves the known
> window from `L` to the strict index-three subgroup `L'`.

This is one chief descent.  It is not global B4-B and does not establish a
uniform/cofinal iteration, isolation of `L` or `L'`, or compactness.
A fresh same-job replay is required.

## Unchanged certified construction

The lane still reconstructs the actual total-linking chief rather than an
abstract C3:

- the marked H9 binary matrix has rank 5 and kernel generated by `111111`;
- `|H9|=32*3^24` and `|H9'|=3^24` are producer gates independently checked by
  the G9 commutator/conjugation module and rank-12 Nakayama certificate;
- the marked `Pi4[3]` abelian action is `I6 mod 3`;
- the integral lattice is
  `{3w : w mod 2 is 000000 or 111111}`;
- its canonical basis has determinant/index 23328 and linking gcd 6;
- `ell(H)=6Z`, `beta=ell/6 mod 3` is onto, and
  `Kbeta=H cap ker(ell mod 18)` is B4-normal;
- the natural adjacent transpositions and inverse maps are replayed on all
  relations and marked generators.

Candidate 124 remains the exact 92-letter registered word with

```text
outer=1, shift=0, correction=124
free exponent sums=(0,0)
SHA-256=c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b
```

Its inverse still comes from the complete registered 27-element q3 fibre.
The literal residual records still cover both hexagons through all five
cofaces, the ordered A.18 pentagon, candidate/base and A5 correction bindings,
all FC-30 differences, PB4 relations, and two-sided generator compositions.

The FC8 intersection, FC-29 orders, and outside classifier are unchanged:

```text
H_ord=18, Kbeta_ord=18, L_ord=90, Lprime_ord=90
gcd(L_ord,Kbeta_ord)=18
row37 = exponent 2 of the row19 pure axis; 3 does not divide 2
```

## Terminal scope

The repaired replay returned the positive token.  The lane's exact outcomes
remain:

- `B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED` when every literal and
  chief gate passes;
- `B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED` when a genuine
  remaining literal gate fails.
- `B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT` when the registered 27-fibre
  does not supply the inverse/preimage certificate needed to evaluate onto.

A positive result proves one strict C3-chief descent for this outside pair.
A negative result rejects only this fixed candidate.  Neither token alone is
B4-A or B4-B, and neither proves isolation, cofinal iteration, or compactness.
Settlement remains diagnostic-only.

## Run history

- `32194128426` / `a5769bab`: driver quoting transport failure; no producer.
- `32194643806`: missing untracked T48 input; no mathematical replay.
- `32194873275`: producer ran, checker crashed on the wrong collector API;
  producer-only result was not cross-checked.
- `32195410958` / `53f525f9`: producer/checker agreed under the now-superseded
  strict-intertwining predicate; its rejection token is reclassified above.
- `32197159346` / `80a20cdf`: transport failed before mathematics because the
  preamble quotes were lost and GAP read `ci` as a variable; no artifact.
- `32197284524` / `80a20cdf`: quoting was corrected, but the optional JSON
  package was absent; no mathematical producer result or artifact.
- `32197397734` / `80a20cdf`: repaired producer and independent checker PASS;
  the cross-checked positive record is fixed above.

## Static audit

- producer function/end balance: `27/27`;
- producer if/fi balance: `43/43`;
- the obsolete intertwining acceptance field/string is absent;
- strict diagnostics remain present in all 30 records and in the digest;
- all T relation/reverse/character/exponent canaries remain in the receipt and
  digest but are absent from both component and outer acceptance predicates;
- producer/checker receipt schemas, including the inverse-not-found branch,
  match exactly;
- driver producer/checker pins match the frozen hashes;
- no PB5, ANUPQ, full-universe, or new heavy operation was added.

The one authorized lightweight checker self-test after the predicate split
passed:

```text
D972_B34_TOTAL_LINKING_C3_CHECKER_SELFTEST_PASS mutations=22
```

It sets both T canaries false and flips the strict-intertwining diagnostic
while still accepting the fixture; mutations of S-relation descent or
`S(T_i)=x_i` recovery are rejected.  The final pin/reply updates were then
audited statically; no further execution was performed.
