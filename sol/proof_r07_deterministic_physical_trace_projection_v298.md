# R07 deterministic projection of physical mutation traces (v298)

## 0. Scope

V297 requires real opened-handle/path identities.  A0-v12a additionally
requires deterministic candidate R/V bytes so a later v12b can pin them.
Raw device numbers, inode/file ids, mtimes, PIDs and random temporary paths
are necessary runtime observations on some platforms but make R/V bytes vary
between runs.  This note separates the runtime witness from its deterministic
load-bearing projection.

It is a paper transport theorem only.  It does not accept a mutation suite,
authorize execution, or change an A0/A4 numerator.

## 1. Raw witness and stable projection

Let `W` be the process-local physical trace used by the ordinary validator:

```text
W = (actual temporary path, lstat/reparse record,
     opened-handle device/file id, size, link count, mtime,
     bytes/SHA, before/after handle records, pathname-after record,
     ordinary validator events).
```

The validator uses all of `W` to decide regularity, one-handle stability,
unique-link ownership and pathname substitution.  Define a deterministic
projection `pi(W)` by retaining only:

```text
logical_case_path, owner_kind,
byte_length, content_sha256,
link_count_before, link_count_after,
symlink_or_reparse, logical_link_target,
single_open_handle, opened_handle_stable,
pathname_matches_opened_handle,
substitution_detected,
canonical_before_sha256, canonical_after_sha256,
resealed_logical_nodes,
entered_validators, event_trace_digest,
first_typed_rejection.
```

`logical_case_path` is a preregistered label such as
`physical/03/toctou_candidate`, not the randomly allocated host directory.
`logical_link_target` is likewise a case label.  The projection omits host
time, PID, absolute temporary path, device number, inode/file id, mtime and
RSS.  Those raw observations may appear only in non-load-bearing diagnostic
logs.

For a file rejected before readable contents exist, `byte_length` and
`content_sha256` are typed `UNREADABLE_AT_REGISTERED_STAGE`, not the digest of
empty bytes.  The path type/link/reparse predicates still come from `W`.

## 2. Projection constructor discipline

The same ordinary physical validator which consumes `W` constructs `pi(W)`
after its handle/path comparisons.  A mutation harness may not manufacture
the booleans.  In particular:

- `opened_handle_stable=true` follows from equality of the raw before/after
  opened-handle records;
- `pathname_matches_opened_handle=false` follows from the raw post-hook
  pathname/handle inequality;
- unique-link rejection records the observed link counts but omits the inode;
  and
- an unsupported Windows one-handle API gives the deterministic typed input
  result registered for that platform contract; it is not projected as a
  successful physical test.

Producer and checker have separately written projection constructors.  They
may share the field schema and logical labels, not raw witnesses or projected
values.

## 3. Receipt/verdict placement

The deterministic candidate receipt R contains only producer `pi(W)` rows.
The candidate verdict V contains only checker `pi(W_check)` rows plus the
stable receipt identity `(logical path, bytes, SHA-256, canonical self seal)`.
It must not serialize the full identity object returned by a low-level open
routine if that object contains device, inode/file id or mtime.

Similarly, a process cleanup receipt contains deterministic counts and
boolean completeness, not PIDs or host exit timestamps.  Telemetry is written
only to ordinary logs which P0/R/V do not hash and which v12b does not pin as
semantic artifacts.

## 4. Determinism theorem

### Theorem 4.1

Assume:

1. the authenticated input bytes, mutation roster, logical case labels,
   canonical encoding and ordinary algorithms are fixed;
2. each raw V297 experiment reaches the same typed outcome;
3. `pi` retains every content/type/link/stability/substitution predicate used
   by acceptance but omits only host-instance identifiers and telemetry; and
4. all iteration orders are explicit.

Then the canonical producer and checker projected ledgers are deterministic,
even when the raw temporary directory, inode/file id, mtime and PID differ.
Moreover, replacing a raw identity comparison by a fabricated projected
boolean is still rejected by the ordinary experiment and independent checker.

**Proof.**  Under (1)--(2), every retained semantic value and predicate has a
fixed result.  The omitted coordinates identify only the host instance, not
the registered semantic outcome, so varying them cannot change `pi(W)`.
Explicit ordering fixes the canonical byte sequence.  The projection is
constructed only after the raw comparisons and is independently reconstructed
by the checker, so a harness-supplied Boolean is not an input to acceptance.
QED.

## 5. Mandatory A0-v12a consequences

1. R/V must not contain the current `open_physical` dictionary verbatim if it
   contains `device`, `inode`, `mtime_ns`, PID or a random temporary path.
2. Top-level `receipt_physical` in V is exactly the stable path/bytes/SHA/self
   tuple, while raw handle data remains local.
3. Every mutation `before_identity`/`after_identity` field is replaced by its
   deterministic projection; content-unreadable cases use a typed marker,
   never `SHA256(empty)`.
4. Producer/checker mutation ledgers and process cleanup fields are scanned
   recursively for nondeterministic host data before sealing.
5. P0 preregisters this projection schema.  V12b may pin exact R/V bytes only
   after a fresh audit confirms the deterministic constructors.

The A4 mutation layer need not preregister future R/V hashes at its current
stage, but using the same projection keeps its later receipt reproducible and
prevents raw telemetry from becoming mathematical authority.

```text
RAW PHYSICAL WITNESS USED INTERNALLY:       REQUIRED
DETERMINISTIC LOAD-BEARING PROJECTION:      PAPER PROOF
INODE/MTIME/PID/TEMP PATH IN R/V:           FORBIDDEN
A0/A4 IMPLEMENTATION:                       PENDING
SELFTEST / PRODUCTION:                      UNEXECUTED
LIFT / FAKE / IHARA:                        NONE
```

`R07_DETERMINISTIC_PHYSICAL_TRACE_PROJECTION_V298_PAPER_GRADE`
