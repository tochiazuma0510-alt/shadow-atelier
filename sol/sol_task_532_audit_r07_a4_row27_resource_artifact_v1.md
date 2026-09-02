# Sol task 532 -- bounded audit of A4 row27 RESOURCE artifact

Role: Sol(max), independent artifact/provenance auditor.  This artifact is
841 MB compressed and contains transient physical shards.  **Do not download
or expand it in full.**  Use read-only API metadata and HTTP byte ranges to
read only the ZIP central directory and the small terminal/result/HEAD/log
members needed below.  Do not run production/checker, edit implementation,
dispatch GHA, or mutate git/releases.  Reply only to
`sol/sol_reply_532_audit_r07_a4_row27_resource_artifact_v1.md`.

## Frozen external identity

- run `33579631937`, job `100090966487`;
- expected head `efaa6234d5ea12c9f81dcb1f33f0609387964475`;
- completed conclusion `success`;
- artifact `9831693721`, name `gap-run-out`, API size `841367330`, service
  digest
  `sha256:2f77b0d3e24009a669761f1066e9e61dd79c88c14a85fd092e85cc11b70dd0b7`;
- ZIP central directory reports 1907 entries, size 164671, offset 841202637.

## Parent range-read observations to reproduce

- marker `task514_v45.success`: 60 uncompressed bytes, exact content
  `TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0\n`;
- producer result `task514_v25_producer.json`: 928325 /
  `dab9b493f935f5a15283820bb98b782ce0621d880176992cec7dc51beaa791b3`,
  status/terminal `UNKNOWN_RESOURCE`, reason
  `dual_pullback:rss_bytes:8001912832>8000000000:state=dual_pullback`;
- producer log `task514_v25.producer.log`: 42809 /
  `fdd79b4bc9af65a334671c0c5cf76f812c0f7019690b84821699e04b3416c9f8`;
- returned producer HEAD: 700 /
  `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`,
  `last_row=26,next_row=27,segment_count=2,last_sequence=2`, chain
  `240714843f67b24fdee9593601130c5d36ef9996909a08af9ec909888cb8cfdb`;
- returned checker checkpoint: 8991 /
  `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`;
- no top-level checker result/log is present and marker says checker=0.

The returned HEAD and checker checkpoint hashes are byte-identical to the
already cross-checked row26 release recorded by Tasks 511/516/520.  The log
entered row27 correlation, reached transient combined/boundary rank 112099,
33,535,212 correlation pairs and RSS near 8 GB, but every progress line kept
`completed_row=26,durable_checkpoint_row=26,K_rank=0` before the typed RESOURCE
terminal.  Transient ranks/pairs are not durable A4 progress.

## Required audit and verdict

1. Authenticate API run/job/head/artifact and the exact small-member identities
   above by range reads.  Confirm unique RESOURCE terminal and absence of any
   checker PASS, positive/NONMEMBER/A4/fake/Ihara claim.
2. Compare the returned HEAD and checker checkpoint exactly with the archived
   row26 identities.  Confirm no row27 delta/HEAD advancement is committed;
   do not count transient physical rank or correlation pairs as a numerator.
3. Classify the outcome.  Return exactly
   `AUDITED_ZERO_DURABLE_PROGRESS_RESOURCE` or `STOP_INCONSISTENT_ARTIFACT`,
   with evidence, limitations and final reply bytes/SHA.  The first verdict
   leaves A4 at `1/3 UNKNOWN_RESOURCE / cross-checked through row 26` and may
   record only a diagnosed 8-GB resource boundary.
