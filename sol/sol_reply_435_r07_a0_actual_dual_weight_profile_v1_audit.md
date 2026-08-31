# Task435 actual-dual profile: mathematical and implementation audit

Date: 2026-08-31
Scope: v409, v410, task435, and the pinned v12 code paths needed to check the
stated ABI.  No production or heavy computation was run.

## Verdict

**GO.**  The mathematical selector, tau-free adjoint bound, prefix orientation,
and proposed actual-runtime profile are sound.  The implementation must retain
the four small gates below; none requires a broader algorithm or enumeration.

## Findings

1. **Adjoint and primal section are correctly separated.**  With
   `Q_ph = N o J_T`, the dual pullback is
   `Q_ph^* lambda = J_T^* N^* lambda`.  V410 constructs `N^* lambda` by
   evaluating the direct `contract` map on candidate new-coordinate
   singletons, then applies `J_T` to each finite seed gradient before pairing.
   This is exactly equivalent to applying `J_T^*`; it never identifies
   v12 `normal_section` with an adjoint.  Task435 only measures the quotient
   dual and its tau coefficients, so it does not need either adjoint yet.

2. **The 15/33 reverse neighbourhood is complete.**  V12 `contract`
   (lines 149--174) sends a central singleton only to the same orbit
   representative (and possibly global tau).  A noncentral singleton in
   component `c` has localized output only at `r(h)` and `r(h s_c)` (plus
   tau); newly introduced representatives have zero noncentral input and do
   not create a second edge.  For an output representative `r`, the complete
   predecessors are therefore
   `e_n(r z^j)`, `e_c(r z^j)`, and
   `e_c(r z^j s_c^-1)`.  This is `3 + 6n`, hence 15 for PB3 and 33 for PB4.
   Computing the last family in the actual group before applying the actual
   transversal includes the nonsplit PB3 cocycle.  The proof correctly
   excludes nonzero global tau from this localization theorem.

3. **Both occurrence-prefix formulae have the correct orientation.**  For an
   unprefixed Tietze key `h`, the translated key is `P h`, and conjugator
   action gives `P pi(delta) h`; pairing with `g` yields
   `pi(delta)=P^-1 g h^-1`, as in v410 (5.1) and task179.  If `H=P h` is the
   already-prefix-translated key, solving
   `P pi(delta) P^-1 H=g` instead gives
   `pi(delta)=P^-1 g H^-1 P`, exactly v409 (3.5).  The apparent extra right
   `P` is therefore required, not an ambiguity.

4. **The v12 bootstrap is the actual runtime adapter.**  V12 lines 432--433
   load the byte-pinned task413/base chain, accepted compact roster, task198
   core and roof, validate the task379 layout, construct `core.Runtime`, bind
   task179's `AllSevenModel` through `direct_physical_owner`, load task176, and
   instantiate the actual v12 `Quotient` and target.  This is not task434's
   fake-key fixture and does expose the real E3/E4 arithmetic and eleven
   occurrence specifications.  It performs finite actor/canary/bootstrap work,
   but no Delta, Q0, E3, E4, PB3, or PB4 roster enumeration.

5. **The requested prefix is proportionate.**  Forty-four calls to
   `seed_v12` followed by `aggregate`, plus the support-times-support v404
   action oracle, are the necessary actual work.  The six fixed action Fox
   rows may be cached, but recomputing those six small rows is not a dispatch
   blocker.  The producer should serialize only target/remainder/dual and
   compact retained source recipes/digests; serializing decoded runtime objects
   or full duplicate rows in progress/checkpoints would be unnecessary.

## Minimal implementation gates

- V12 `PackedEchelon.dual` guarantees a nonzero remainder pairing, not
  necessarily the normalized value one used in v409 (2.1).  Scale the whole
  dual by the inverse of that F3 scalar before reporting exact coefficients or
  compiling weights, and have the checker require the normalized pairing.
  Tau zero/nonzero is scale invariant, but its reported coefficient and direct
  scalar comparisons are not.
- `q.parse` accepts only framed `Q` keys.  Parse `Q` keys with `q.parse`, handle
  exactly `b"N\x01"` and `b"N\x02"` as the two exponent keys, and reject every
  other key.  Calling `q.parse` indiscriminately on exponent support would be a
  runtime failure.
- Because task435 intentionally creates no occurrence echelon, it cannot call
  v12 `positive` unchanged: that function expects occurrence pivot ancestry.
  On target zero, replay the retained identity-seed coefficients and action
  sources directly through the same literal/exactification/all-seven gates, or
  fail closed.  Do not manufacture PHYSICAL occurrence-pivot metadata.
- A resource checkpoint should contain only phase/cursor, normalized retained
  seed/action source recipes, counters, and seals.  Rebuild the small physical
  echelon after the pinned bootstrap on resume; do not marshal runtime groups,
  decoded rows, or a second full echelon.  The target digest has no numeric
  value frozen in task435, so it must either be preregistered explicitly or be
  computed independently by producer and checker and compared, not
  self-attested by one process.

Subject to these local gates, the profile terminal remains informational:
`PROFILE_READY` and `UNKNOWN_RESOURCE` prove neither A0 membership nor
nonmembership, and nonzero tau remains the explicit global-adjoint gate.

GO
