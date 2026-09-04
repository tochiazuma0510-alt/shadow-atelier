# Luna reply — Task871 / Task899

Implemented the bounded R07 physical-state / canonical-separator core in the
two authorized executables. The implementation is complete at this scope,
but remains audit-required and does not declare an actual Grade-2 result.

## Implemented boundary

- The producer authenticates the v6 connection parent in one chronological
  pass: all 8,059 offers/instruction rows, source ancestry, P1 identity,
  `ell_sha256`/`g_sha256`, lower/top/coefficient offsets and digests, rolling
  head, EOF, and exact source counts.
- Only the 1,354 `kind=connection` offers enter physical `S_0`; the 6,705
  lower pivots remain authenticated but skipped. The live pins are
  `offers=8059`, `rank=6705`, `dependent=1354`,
  `reduction_count=7665974`, and final rolling head
  `3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd`.
- Physical rows are packed 48,384-trit rows (12,096 bytes), with synchronized
  packed P1 companions (2,015 bytes), stored file-backed. Reduction scans
  every prior pivot's own lead in insertion order; a free coordinate is never
  used as an early stopping condition. Accumulators use `uint32` for the
  48,384-coordinate dot products.
- Target reduction records exact pivot scalars and P1 expression. A nonzero
  remainder produces the v536 separator by reverse *insertion* order, with
  all pivot equations and target pairing checked over all 48,384 coordinates.
  No generic nullspace solver or dense square matrix is used.
- Checkpoints use `d972.r07.physical-state.checkpoint.v1`, are written after
  whole offers at interval 128 (plus requested-stop/final boundaries), carry
  actual previous-checkpoint SHA, path-free connection/source identity pins,
  nonzero RSS and wall-time receipts, and are removed before final `HEAD`
  publication. The completed state roster is exactly `physical.bin`,
  `physical-p1-coeff.bin`, `instructions.jsonl`, `manifest.json`, and `HEAD`.
  Public live resume is intentionally disabled in v1 because no authenticated
  resume-artifact authority and semantic prefix replay are available; bounded
  stop/resume remains covered internally.
- Public producer/checker CLIs reject `fixture_only=true`; fixtures are
  reachable only by their internal selftest paths. The live path is fresh
  only and requires the exact final artifact tuple below.
- The independent checker has no producer import edge. It independently
  replays source/state/target rows, file rosters, hashes, rolling chains,
  reductions, scales, leads, `MEMBER` back-substitution, and separator reverse
  substitution.

## Immutable parent pins

The ordinary path binds repository
`tochiazuma0510-alt/shadow-atelier`, workflow
`.github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml`,
run/attempt `33876776771/1`, head
`b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2`, job `101035535909`, accepted
producer-v6 SHA-256
`6c450c2d82f7ad5795d9188e2912a4587882ae3fb9351217f33393c96f75526a`,
independent-checker-v7 SHA-256
`b5b210f6063a8fed6172417d350510eeccbafa0f60e5e676aa2732fee5e8757e`, and
workflow SHA-256
`c7f3c9a8b728fa5ab0bd6be0b550b381e5b33d8ce1f59523dc04fb82b306fb74`.

The final v11 artifact receipt is bound exactly as:

```text
repository=tochiazuma0510-alt/shadow-atelier
run=33876776771
attempt=1
head=b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2
job=101035535909
status=completed
conclusion=success
artifact_id=9939860701
artifact_name=d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1
archive_bytes=245546516
digest=sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a
expires_at=2026-12-03T13:12:28Z
```

The rho2 acquisition is pinned to accepted flat-stager v4 run `33839962829`,
attempt 1, workflow
`.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml`, workflow
id `349904905`, head
`17a8439c766d92719d7ae7d35846ea444da598fa`, artifact `9925190479`, and
artifact digest
`sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4`.
The exact endpoint receipts include `rho2.bin` (12,096 bytes,
`b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`),
`rho2-dense.bin` (48,384 bytes,
`abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e`), and
`lower-dense.bin` (32,260 bytes,
`c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830`).

## Bounded tests and receipts

Commands (PowerShell, repository root):

```text
python -m py_compile search/d972_r07_grade2_physical_state_separator_v1.py search/check_d972_r07_grade2_physical_state_separator_v1.py
python search/d972_r07_grade2_physical_state_separator_v1.py --selftest
python search/check_d972_r07_grade2_physical_state_separator_v1.py --selftest
python search/d972_r07_grade2_physical_state_separator_v1.py --benchmark
```

Observed final run: compile PASS in 0.135 s; producer selftest PASS in
0.725 s; independent checker selftest PASS in 3.416 s; benchmark PASS in
0.556 s. The checker rejected all 19 commissioned mutation/control cases,
including top/coefficient/source ancestry, physical reduction/scale/lead,
state HEAD, rho2, target remainder/free coordinate, lambda, terminal kind,
wrong parent/claim flags, missing/extra file, truncation, false EOF, and wrong
schema. The fixtures contain both a genuine `ConnectionMember` and a genuine
`Separator`; non-monotone leads are `[100,10,300]` and the reverse transcript
is `[300,10,100]`. The free-before-existing-pivot control uses free coordinate
5 and passes.

The final benchmark JSON was:

```text
offers=6, physical_rank=3, physical_reductions=2,
target_reductions=1, reverse_substitution=3, operations=6,
seconds=0.12887369998497888, operations_per_second=46.55721066982124,
packed_physical_p1_axpy_pairs_per_second=8509.280441000037,
reverse_row_dot_checks_per_second=16823.95319663971,
live_source_offers=8059, live_source_connections=1354,
live_physical_reduction_upper_bound=915981,
status=BOUNDED_ONLY, verified=false
```

The honest live physical envelope is `c(c-1)/2 + target + reverse` with
`c=1354`, hence at most `915981` physical reductions, plus the target and
reverse passes. The bounded benchmark is not a production runtime claim.
Maximum physical store size at the live physical rank is
`1354*12096=16,377,984` bytes and companion-store size is
`1354*2015=2,728,310` bytes; processing
uses positioned reads, reusable row buffers, metadata, and streaming
whole-file hashes rather than a dense rank-by-48,384 resident matrix.

Authorized file receipts after the final edit:

```text
search/d972_r07_grade2_physical_state_separator_v1.py
  bytes=75934 LF=1407 sha256=5f1267a7296a6f613f46a1d431c807da22239419362f32ea7c08b51fd7d6e13f
search/check_d972_r07_grade2_physical_state_separator_v1.py
  bytes=57325 LF=734 sha256=01df70e8c6be4bfdff4fbedc227488edce47b1e9c195466ea7658d36b63ee107
```

The claim boundary is preserved exactly:

```text
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
cross_checked=false
verified=false
```

R07_PHYSICAL_STATE_SEPARATOR_V1_IMPLEMENTED_AUDIT_REQUIRED
