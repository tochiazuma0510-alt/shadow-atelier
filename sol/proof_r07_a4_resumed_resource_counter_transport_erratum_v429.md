# R07 A4 resumed-resource counter transport erratum (v429)

Author: Sol / 2026-09-02

Status: paper correction to v428 equation (2.2), derived from the immutable
row-26 artifact and the pinned producer accounting.  This note supersedes
only v428 (2.2); its closed-delta replay and v423's unique resource witness
remain unchanged.  It does not promote row 26.  `verified=false`.

## 1. Exact immutable relation

Let `B` be the authenticated row-24 resume checkpoint, `T` the terminal
resource object, and `S` the registered semantic-counter domain.  Put

```text
D = {terminal_canonicalization,
     terminal_serialized_bytes,
     terminal_final_write}.
```

The exact asset satisfies

\[
 B_{\rm sem}=B_{\rm completed},                                      \tag{1.1}
\]

\[
 T_{\rm completed}(k)=B_{\rm sem}(k) \quad(k\in S\setminus D),       \tag{1.2}
\]

\[
 T_{\rm completed}(k)=T_{\rm sem}(k) \quad(k\in D),                 \tag{1.3}
\]

and componentwise

\[
 T_{\rm completed}\leq T_{\rm sem}.                                \tag{1.4}
\]

Moreover the difference domain is exact:

\[
 \{k\in S:T_{\rm completed}(k)\ne B_{\rm sem}(k)\}=D.              \tag{1.5}
\]

On `D`, the base values are `(0,0,0)` and the terminal completed/semantic
values are `(7,9300,1)` in the displayed order.  These three increments are
terminal transport bookkeeping produced by the pinned `Meter.terminal_bump`;
they are not row work and do not move the durable cursor.

Thus v428's whole-domain equality
`T.completed = B.semantic = B.completed` is false and is withdrawn.

## 2. Positive-safe checker predicate

The checker must authenticate the exact domains, numeric types, nonnegative
bounds and (1.1)--(1.5).  For `k in D`, it must additionally bind the three
values to the terminal canonical/semantic map and to the corresponding
transport fields for canonicalization count, serialized-work bytes and final
write.  For `k not in D`, it must bind to both base maps.  No terminal-minus-
base difference is used to infer a row, delta, or closed cursor.

Together with independent base/delta/HEAD replay, this accepts only the
sealed row-26 cursor.  V423 still applies to the terminal canonical map and
its genuine typed views; `wall_seconds` remains the unique allowed over-cap
coordinate.

## 3. Regression obligations

The positive fixture must be constructed from all exact maps in the pinned
asset, including base `(0,0,0)` on `D`.  It must reject:

- a missing or extra member of the exact difference domain;
- drift in either base map, any non-`D` completed value, or any `D` transport
  equality;
- `completed > terminal semantic` in any coordinate;
- a simultaneous canonical+typed-view second over-cap mutation; and
- any attempt to use the three transport increments as durable row progress.

`R07_A4_COUNTER_TRANSPORT_ERRATUM_V429_PAPER_GRADE`
