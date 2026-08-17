# Luna task 157ac — power-spectrum v1 audit repair

Role: Luna implementation repair. Do not run local GAP, git, push, or GHA.

Read `sol/luna_reply_157x_power_spectrum_audit.md` in full and repair every
F1--F4 finding in a new versioned v2 bundle. Do not overwrite v1. The v2
workflow must trigger on, and the receipt/checker must hash-bind, every direct
runtime source including `search/probe/wac_v1/gap_output_prelude.g` and
`search/gaplib_common.g`. Pin GitHub actions by immutable commit SHA and pin
and enforce one GAP runtime/version as far as the Ubuntu workflow contract
allows. Serialize and independently replay the square map, cube map, and group
exponent. Independently check associativity (a mathematically equivalent
exhaustive or structure-derived check is allowed, but the receipt field may
not be trusted).

Preserve the fail-closed `UNKNOWN_MISSING_AUTHENTICATED_LABEL` outside lane.
Run lightweight Python compile/self-tests and YAML parse only. Write the full
report to `sol/luna_reply_157ac_power_spectrum_repair.md`, listing changed
files, exact checks, hashes, and whether the bundle is dispatch-ready.
