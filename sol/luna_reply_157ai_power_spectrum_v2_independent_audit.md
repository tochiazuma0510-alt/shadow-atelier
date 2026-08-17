# Luna independent audit: power-spectrum v2 (157ai)

## Verdict

**BLOCKER.** The producer/checker mathematics and the zero-based power-map
repair are statically coherent, but the advertised workflow cannot reach the
power-spectrum producer, and the independent associativity argument has an
unverified homomorphism-descent premise. No local GAP, git, push, or GHA was
run.

## F1: workflow execution is preempted by the worker's top-level `QUIT`

`search/d972_power_spectrum_v2.g:8` first executes
`Read("search/d972_dovetail_worker_v1.g");;`.  The worker dispatches its
selftest at `search/d972_dovetail_worker_v1.g:1502-1503` when the workflow sets
`D972_WORKER_MODE=selftest`, then unconditionally executes `QUIT;` at line
1522.  Consequently GAP exits during the `Read` before the producer assigns
`DPS2Mode` or reaches `DPS2SelfTest`/`DPS2Run` (`search/d972_power_spectrum_v2.g:10-12,64-77,79-205`).

The workflow nevertheless requires the producer selftest marker at
`.github/workflows/d972-power-spectrum-v2.yml:66-73` and the producer final
marker at lines 77-84.  The worker emits a different selftest marker before
exiting.  Thus both the selftest gate and full receipt path fail on the
audited bundle; F1/F4 are not operationally closed.

The declared five-file manifest does bind the four fixed helper reads
(`search/d972_power_spectrum_v2.g:17-18`, checker `:17-30`, workflow `:7-16,37-48`),
but the worker also has environment-controlled `Read(taskPath)` calls at
`search/d972_dovetail_worker_v1.g:965,1144,1408`.  Those task files are not
manifested.  They are not reached by the current selftest setting, but the
claim of complete transitive binding is broader than what is actually bound.

## F2: runtime is version-pinned, not immutable

The source and action SHA checks are good, but
`.github/workflows/d972-power-spectrum-v2.yml:29,50-54` uses the mutable
`ubuntu-24.04` runner label and performs `apt-get update` against the live
archive before installing `gap="4.12.1-2build2"`.  The GAP version check is
useful, but no package SHA, repository snapshot, executable digest, or runner
image digest is recorded/enforced.  A future image/archive change can therefore
run different code while all repository SHA gates pass.  This does not meet the
immutable-runtime requirement from 157x; action commits at `:34,92` are
properly immutable.

If “dispatch-ready” means manual `gh workflow run`, there is an additional
operational blocker: `.github/workflows/d972-power-spectrum-v2.yml:3-16` has
only a `push` trigger and no `workflow_dispatch`.  A push on the named branch
is the only available trigger unless that is explicitly the intended launch
mechanism.

## F3: zero/one-based maps and exponent

This portion is closed statically.  The producer initializes the power walk at
the serialized zero-based identity and converts back to GAP indexing only for
the table lookup (`search/d972_power_spectrum_v2.g:131-145`); square/cube maps
and the folded LCM exponent are serialized at `:149-155,195-199`.  The checker
recomputes the same values from its independently rebuilt table at
`search/check_d972_power_spectrum_v2.py:379-388`, and its C2 zero-based
identity/order selftest is at `:399-418`.

## F4: associativity check is conditional on an unchecked descent premise

The checker does exhaust all 972^2 pairs and compares the proposed composite
map on the two roof generators (`search/check_d972_power_spectrum_v2.py:243-271,388-391`).
That comparison proves associativity only when each assignment

`x -> x^u`, `y -> f^-1 y^u f`

is already known to descend to a homomorphism of the compact roof group.  The
GAP producer checks that premise with
`GroupHomomorphismByImages` at `search/d972_power_spectrum_v2.g:115-118`, but
the independent Python checker does not replay any relation/descent test.  It
only requires the receipt's self-asserted `settled=true` at
`search/check_d972_power_spectrum_v2.py:313-324`, then checks generator images.
The frozen artifact contains words/keys, not an independently checked descent
certificate.  Therefore the claimed “structure-derived associativity proof” is
conditional on producer behavior rather than a complete independent proof;
malformed settlement metadata can pass the row and table gates unless descent
is independently checked or an authenticated certificate is consumed.

## Static evidence

Read-only checks (no GAP) produced:

```text
D972_POWER_SPECTRUM_V2_CHECKER_SELFTEST_PASS
PY_AST_PASS
YAML_PARSE_PASS
```

SHA-256 recomputation matched the current workflow constants for the producer
(`98fe4a05db5d307603d0f33a58f89c00179d18fbc268618629fbd431aead631d`), checker
(`3e17089bdd83596d913c7b88ddf510e446935fb9b3e0abe6ef757a6f8aea23d1`), worker,
four fixed helper files, and frozen artifact.  This confirms source binding,
not successful GAP execution.

BLOCKER
