# R07: Task640 v10 missing owner binding classification (v488)

Author: Sol / 2026-09-04

Run `33811630349/1`, job `100834536849`, head
`2468d38778a411544a366bb85593296263facd97`, authenticated all frozen inputs,
passed both bounded fixtures, downloaded all three parents, and staged the
fixed Task625 verdict.  The fresh producer then stopped at endpoint-minimal
step 1 with

```text
NameError: name 'validate_q3_literal_owner' is not defined.
```

This note classifies that stop and gives the unique minimal repair.  It does
not produce a residual or change any mathematical claim.  `verified=false`.

## 1. Exact cause

The endpoint-minimal builder is called as

```text
build_endpoint_minimal(module, registry, meter, words),
```

where `module` is the already hash-pinned v12f runtime module.  That module
defines and uses

```text
module.validate_q3_literal_owner(q3).
```

The v4 extraction copied the call body as the unqualified name
`validate_q3_literal_owner(q3)` but did not copy or bind that definition.
Repository-wide definition census confirms the function remains present in
the pinned v12f source and absent locally in v4.  Hence this is Python name
resolution before quotient construction, not a failed Q3 row, endpoint,
deletion, precision-two, or rho2 assertion.

## 2. Minimal repair

In a versioned producer successor replace exactly

```text
q3_owner = validate_q3_literal_owner(q3)
```

by

```text
q3_owner = module.validate_q3_literal_owner(q3).
```

The same `module` already supplies `SourceRegistry`, quotient constructors,
the resource meter and all other endpoint-minimal primitives.  Calling its
public validator preserves byte-for-byte the v12f Q3 literal-owner gate while
avoiding any second implementation.  The v4 payload protocol and independent
v4 checker need no semantic change.

```text
V10 TERMINAL:                    INPUT/BINDING FAILURE
MATHEMATICAL NEGATIVE:           NO
REPAIR SURFACE:                  ONE QUALIFIED CALL IN VERSIONED PRODUCER
FRESH RHO2:                      NOT PRODUCED
A0 / COMMON / COFINAL / FAKE:    NOT DECLARED
IHARA:                           NOT DECLARED
verified:                        false
```

`R07_TASK640_V10_MISSING_OWNER_BINDING_CLASSIFIED_V488`
