# Luna task 430 — v11 finite central-power API fix

## Exact GHA finding

The full v10 GHA run `33319489870` / job `99278843069`, commit
`a6c32f379fcaafc32d030eeb4da7c325bb9695c3`, completed its transport and
uploaded artifact `9734471174`, but the producer failed closed before a seed
checkpoint or search progress.  The bounded traceback is:

```text
AttributeError: 'MatchedQuotient' object has no attribute 'power'
owner_v10.py line 230: target=q.transform(...)
owner_v10.py line 108: self.contract(block,es)
owner_v10.py line 65: h,j=self.h0(g,z,v)
owner_v10.py line 58:
  need(g.mul(r,g.power(z,j))==v,"pb3_transversal")
```

Inspection of the pinned `MatchedQuotient` implementation establishes that its
public element operations are exactly `identity`, `mul`, `inverse`, and `eval`;
there is no `power` or `pow` method.  Both PB3 and PB4 `h0` use only exponents
`0,1,2`.  Make one versioned v11 patch which expresses those powers through
the real API.  Preserve every v10 component-origin, namespace, memory,
checkpoint, resource, bounded-telemetry, search, and claim-boundary invariant.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v11.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v11.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v11.g`;
4. `sol/luna_reply_430_r07_a0_pb34_direct_quotient_owner_v11_power_api_fix.md`.

Do not edit v10 or earlier files, workflows, proofs, v220, checkpoints, or
artifacts.  Do not commit, push, dispatch, or run the production search locally.

## 1. Exact local helper

Add a small helper near `need`:

```python
def central_power3(group, value, exponent):
    j = int(exponent)
    need(0 <= j < 3, "central_power3_exponent")
    if j == 0:
        return group.identity
    if j == 1:
        return value
    return group.mul(value, value)
```

Replace all three nonexistent API calls in `Quotient.h0`, and only those
calls:

```python
g.power(z, j)             -> central_power3(g, z, j)
g.power(g.inverse(z), j)  -> central_power3(g, g.inverse(z), j)
g.power(z, j)             -> central_power3(g, z, j)
```

Do not change the PB3 `j=(-shift)%3` convention, the PB4 kappa coordinate,
the reconstruction equalities, or any surrounding formula.  Do not introduce
a generic exponentiation loop or cache: the exponent universe is frozen to
three values and this helper allocates no closure.

Extend the bounded producer fixture with a toy group using only `identity` and
`mul`; assert outputs for exponents `0,1,2`, and rejection for `-1,3`.  Assert
the producer source contains no `.power(` or `.pow(` token after the patch.

## 2. Version and driver discipline

Clone v10 to v11 and update every executable version/schema/header/marker,
checkpoint header, module name, owner/seed/actor name, driver symbol, fresh
input/output/artifact/log path, and task number from v10/task429 to v11/task430.
No stale executable `V10`, `v10`, or `task429` identifier may remain.  Prose in
the module docstring may identify v10 as the base if necessary, but prefer a
clean v11 header.

The driver must pin exact v11 producer/checker bytes and SHA-256, require the
external preamble `D972_R07_A0_PB34_V11_RUN:=true`, use fresh distinct v11
input/output paths, 9000 seconds, 4.8 GB, one Python owner and one checker,
live logs, and generic `gap-run.yml` compatibility.  Do not add self-test work
to the production path.

## Gates

Run only:

1. Python syntax compilation of producer/checker;
2. v11 producer `--mode FIXTURE`;
3. v11 checker `--self-test`;
4. bounded static search confirming no `.power(` / `.pow(` and no stale
   executable v10/task429 identifiers;
5. independent diff v10→v11 showing only versioned identity plus the helper,
   its three uses, and its fixture.

The Windows real bootstrap remains inapplicable because of the frozen
same-handle gate.  End the reply with
`V11_LOCAL_GO_FOR_PARENT_AUDIT_AND_DISPATCH` or a precise `NO-GO`.
