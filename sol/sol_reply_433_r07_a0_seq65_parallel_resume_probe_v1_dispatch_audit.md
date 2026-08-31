# Task433 sequence-65 parallel resume/probe dispatch audit

Date: 2026-08-31
Scope: task433 and its four final outputs, with the pinned v12 producer/checker
and previously audited driver structures used only for comparison.

## Verdict

**GO for immediate GHA dispatch of either task433 path.**

- Both drivers pin the exact one-entry release URL, 178918944-byte zip and
  SHA-256
  `b27a70ffe4095f9c9760c51694e7b56d68efb3e22d7df4ecaab4513f7328dbcc`,
  and the 461087575-byte checkpoint with SHA-256
  `8918df4407e91a7b4ab1a29246a23ba5b0ed1a7b6011f4abf74775cc33d82705`.
  Each branch requires exactly the sole registered v12 output-checkpoint name;
  absent, extra, duplicate, directory, absolute, and traversal names fail.
- Reconstructed recovery commands for the final continuation and probe drivers
  each have 93 GAP `Concatenation` parts and exactly one one-line
  `bash -lc` payload.  In both, the pre-existing `unzip` path is the configured
  concrete recovery zip, not a stale GAP identifier.  Fresh zip/checkpoint
  temporaries are in the final directories, bytes/SHA are checked before
  atomic moves, and `-e` plus `-L` gates cover zip, input, seal, and the fresh
  receipt.  The exact hash-bound receipt is created once, after either branch
  fully validates, then exact-compared by GAP; a failed shell cannot reuse a
  stale seal as success.
- The continuation driver invokes unchanged v12 directly with `--resume` on
  the authenticated canonical `occurrence_queue` input.  It supplies no v11
  migration and cannot enter the seq40-only `parent` normalization.  The whole
  checkpoint pin binds the recorded sequence 65 state; ordinary v12 `cp_read`
  performs the canonical phase, shape, cursor, frontier, nnz, packed-row, and
  source gates.  Its input, output checkpoint, artifact, and logs are distinct.
  The checker is bound to both exact input and output paths.
- The probe v1-to-v2 source diff is exactly the allowed set: task/module/marker
  names, input bytes/SHA, and informational rank/frontier `1655/1132`.
  The pinned v12 import, false-truth deque, mutable-global reset/final restore,
  positive replay, no-checkpoint call, and claim boundary are unchanged.
  Resource and six-action failure normalize to top-level UNKNOWN; any forbidden
  terminal fails closed to UNKNOWN.  A probe UNKNOWN is not a negative result,
  and neither NONMEMBER nor promotion to COMMON_WORD, compatible lift, fake, or
  Ihara is possible.  The unchanged checker receives input only and no output
  checkpoint.
- The required preambles are exact:
  `D972_R07_A0_PB34_V13_RUN:=true;;` and
  `D972_R07_A0_PREFIX_POSITIVE_PROBE_V2_RUN:=true;;`.  Each driver requires one
  and only one producer marker and checker PASS marker.  No fixture,
  diagnostic scan, duplicate decode, or other avoidable production work was
  added.

## Exact final identities

- continuation driver v13: 6988 bytes, SHA-256
  `4238b358553cb1ee14d0861416184746e003f094a55bb638a62a85a910846896`
- prefix probe wrapper v2: 6271 bytes, SHA-256
  `e04121d1f451031fb18b519a74330d357d9b9f79027ce2614c2ecf3e72e86fed`
- prefix probe driver v2: 6856 bytes, SHA-256
  `06c9f5f00a22c53f9f947eee2ce6b0a99089a4262bb9aef3e0675886b5edeee6`
- Luna reply: 2282 bytes, SHA-256
  `0911b4791421e823d335a9310681d6b5e87fc75bad8efa15f0803b94a1197d33`
- unchanged v12 producer: 51884 bytes, SHA-256
  `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`
- unchanged v12 checker: 13334 bytes, SHA-256
  `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`

Bounded work performed: full static inspection, exact v1-to-v2 diff,
in-memory v2 compilation, unchanged checker self-test, recovery-command
reconstruction, byte/SHA checks, and `git diff --check`.  No checkpoint was
loaded, and no download, production, commit, push, or dispatch was performed.

GO
