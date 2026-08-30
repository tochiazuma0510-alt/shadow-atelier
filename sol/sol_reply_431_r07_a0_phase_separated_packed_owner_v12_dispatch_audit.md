# Sol reply 431 — v12 dispatch audit

## 判定

**NO-GO**。数学・migration pin・driver は概ね task431/v407 に一致するが、checker の phase 証明と checkpoint I/O に dispatch 前修正が必要である。

## 確認できた点

- Producer lines 26–29 の URL/zip/entry/whole checkpoint pins は task431 と一致する。lines 355–379 は zip と checkpoint whole/payload を同じ extraction stream で照合し、v11 schema/binding と `44/86/344`, rank 344, frontier 258 を固定する。
- Lines 383–398 は partial physical 四 field を先に破棄し、occurrence row を一行ずつ pop/pack し、GC/`malloc_trim`/4.8 GB gate を通す。line 406 は v12 checkpoint を line 407 の `core.Runtime` より前に書く。
- `PackedEchelon` lines 53–103 は shared registry と packed-row axpy を使い、actor hot path は lines 448–456 で packed parent を直接 iterate する。progress/state は incremental `payload_nnz` を使う。physical insertion は queue exhaustion 後の lines 457–461 のみで、row ごとに digest、insert、occurrence payload drop の順である。
- Positive path lines 270–315 は retained expression/source DAG から occurrence row を再構築し、stored `source_digest` と fresh digest を照合後、v11 の exactification/joint/direct/correction/target-zero gatesを保持する。
- Driver lines 5–22 の producer/checker pins、exact release URL、fresh v12 paths、external `D972_R07_A0_PB34_V12_RUN`, 9000 s, 4,800,000,000 bytes、one producer/one checker/live logs は一致する。workflow edit や production self-test 呼出しはない。
- 実測 pins は reply/driver と一致した: producer 43652 bytes / `531e44c56fa5860bedd5d1418edf9dd4c0de610a64bbd87c80791d3751aef001`; checker 10115 bytes / `517b56192b39b72af2e10f44292018a0692c79b7eb68c14e78e5728976e5dcca`; driver 3140 bytes / `b3ef32d7137c8647342514146175928fcfed1be86b9facb99217dc11feb04da6`。

## Dispatch blockers と最小修正

1. **Checker は physical prefix/suffix mismatch を拒否できない。** Checker line 75 は `pc + len(occ_rows) == len(occ_order)` しか見ないため、例えば `pc=1`, order `[a,b,c]`, rows `{a,c}` を正しい suffix `{b,c}` と区別しない。さらに lines 68–72 は `physical_build` 中にも `action` source を許し、PHYSICAL source の `occurrence_pivot` が processed prefix に属することも検査しない。Producer cp reader lines 345–353 も phase ごとの physical source family/prefix 対応を検査しない。両方で、order uniqueness、`set(occ_rows)==set(occ_order[pc:])`、`physical_build` では action 禁止、各 PHYSICAL source pivot が processed prefix に一意かつ順序整合することを要求する。Checker line 112 の result/checkpoint agreement も、現在の seq/rank/nnz だけでなく phase、physical cursor、seed/parent/action cursors、frontier と packed payload counters まで一致させる。
2. **明示された no-duplicate-full-scan gate に反する。** Checker `seal` lines 47–53 は `whole(p)` の後に同じ checkpoint payload を再度全走査する。Producer は resume の seal/decode 後に line 431 と main line 556 で whole checkpoint を重ねて走査し、output も save line 419 の後に main line 557 で再走査する。加えて shared `coordinate_keys` の `len(set(keys))` を producer line 341 と checker line 64 で occurrence/physical の二回ずつ実行し、producer line 103 でも再度巨大 temporary set を作る。outer/payload hashes を一回の streaming pass で同時計算して seal を返し、artifact へその値を引き回すこと。shared registry は一回だけ、または構築する `ids` 自体で uniqueness を検査し、phase loop 内で set copy を作らないこと。
3. **Migration の atomic-seal と必須 fixture が未実装。** Producer lines 356–362 は固定 `.tmp` を直接書いて hash 後そのまま開き、flush/fsync と authenticated path への `os.replace` がないため、task431 §3 の「atomically seal it」を満たさない。random temp を close/fsync/hash 後に atomic rename してから zip を開く。併せて現 fixture lines 487–493 は一文字 atom tuple のみで reverse multi-prefix actor replay/digest equality を実行せず、line 513 は physical dict の破棄だけで queue/sources/expressions/cursors を保持する migration fixture になっていない。brief が列挙した二つの bounded gate を実際の helper に接続する。

## 実行した bounded commands

- Repo 外 `%TEMP%` cfile を指定した producer/checker `py_compile`: exit 0
- `python -B search/d972_r07_a0_pb34_direct_quotient_owner_v12.py --mode FIXTURE`: `R07_A0_PHASE_SEPARATED_PACKED_OWNER_V12 FIXTURE_PASS`
- `python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py --self-test`: `R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS {"fresh_object_mutation_gates":3,"packed_corruption_gates":4,"status":"FIXTURE_PASS"}`

実 migration/download/full production、workflow edit、commit、push、dispatch は行っていない。

NO-GO

## Re-audit after repair

### 判定

**NO-GO**。前回 blocker 2 は閉じ、blocker 3 の atomic migration/migration-state 部分も閉じたが、blocker 1 の durable agreement に実行時即死があり、blocker 3 の positive fixture も一部未完である。

1. **Blocker 1: 未完。** Producer/checker `phase_gate`（producer lines 333–344、checker lines 49–60）は、`physical_build` の PHYSICAL sources を processed prefix の **strict subsequence** として正しく許す。依存 aggregate が source を作らないため全 prefix との一対一を要求しておらず、この条件は正しい。wrong suffix と premature action も拒否する。しかし checker line 129 は `frontier_length` を checkpoint state の同名 field と直接比較する一方、producer state line 430 は frontier を `queue` としてだけ保存する。したがって有効 checkpoint でも `ds.frontier_length` は整数、`s.get("frontier_length")` は `None` となり、output checkpoint が存在する全 run で `durable_state_agreement` が必ず失敗する。`frontier_length` を direct-key tuple から外し、`ds["frontier_length"] == len(s["queue"])` と比較すること。また occurrence phase gate は現在 `physical_rows` だけを空とし、空でない `physical_order/expr/sources`（特に action-only metadata）を許すため、producer/checker とも physical 四 field 全てを空と要求する。
2. **Blocker 2: CLOSED。** Checker `seal` lines 42–48 と producer `cp_read` lines 345–353 は outer/payload hashes を単一 streaming pass で計算する。`cp_write` lines 320–332 は copy と同時に outer seal を返し、save/main は cached seal を使う。shared registry uniqueness は phase loop 外で一回だけ検査され、runtime `ids` は別の巨大 `set` を作らず構築される。packed hot path も `memoryview(...).cast("I")` へ変更された。
3. **Blocker 3: 一部未完。** Migration lines 374–404 は random temp、flush/fsync、pin 検査、`os.replace` 後の sealed zip 使用へ修正され、toy migration lines 529–532 は physical discard と queue/order/expr/sources/cursors の保持を実際に確認する。ここは CLOSED。一方、positive fixture lines 509–515 は二文字 atom tuple を作るだけで `actor_v12`/toy actor を reverse iteration して rebuilt row を作らず、stored digest との equality/mutation rejection も実行しない。line 552 は digest の辞書順不変性だけで、前回指摘した reverse-prefix actor replay + digest equality gate にはならない。bounded fixture を実際の二段 actor applicationと rebuilt aggregate digest comparison に接続すること。

### Final pins

- producer: 48902 bytes, SHA-256 `ede5a447ed2e250e8548d9e165ca0e60b5a5f12e58cfc521bb9c8ecb22e7bd1e`
- checker: 12079 bytes, SHA-256 `073b909d8803b124a9a0285e752ebe240af58dad24e024b1262d6f43866e452f`
- driver: 3140 bytes, SHA-256 `3cb727579b03db5d94724599cab898422c4140d544fef35d71afc1e086d815ea`

Driver lines 5–6 と Luna reply の pins は実測値に一致する。

### Bounded commands

- Repo 外 `%TEMP%` cfile の producer/checker `py_compile`: exit 0
- producer `--mode FIXTURE`: `R07_A0_PHASE_SEPARATED_PACKED_OWNER_V12 FIXTURE_PASS`
- checker `--self-test`: `R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS {"fresh_object_mutation_gates":3,"packed_corruption_gates":4,"phase_mutation_gates":2,"status":"FIXTURE_PASS"}`

実 migration/download/full production は未実行。コード、driver、workflow は変更していない。

NO-GO

## Final re-audit

**GO**。直前 re-audit の残り3点は全て閉じた。

1. `frontier_length` は producer migration state line 415 と通常 state line 422 に `len(queue)` として保存され、producer/checker phase gate（producer line 325、checker line 51）が保存値と queue 長の一致を要求する。durable state も producer lines 420/433/447 で同じ値を持ち、checker line 135 の agreement tuple と一致する。以前の必敗 `integer != None` は解消した。
2. Producer lines 325–329 と checker lines 51–55 は physical row keys と unique physical order を exact に一致させ、rows/order/expr/sources の長さ、packed nnz counters も一致させる。`occurrence_queue` では physical rows/order/expr/sources と両 nnz counter を全て空/zero に要求する。PHYSICAL sources は引き続き processed occurrence prefix の strict subsequence であり、依存 row を一対一対応させる誤条件は導入されていない。
3. Production の top-level `replay_atom` lines 273–277 は authenticated seed から `for letter in reversed(tuple(prefix))` で actor を適用し、positive line 298 が全 selected PHYSICAL atom replay にこの helper を共有する。line 299 は freshly aggregated row と stored digest を照合する。Bounded fixture lines 501–511 は非可換 toy actor で reverse と forward を区別し、prefix-order mutation が framed row digest を変えることを要求するため、直前の fixture 欠落も閉じた。

Final identities は driver と Luna reply に一致する。

- producer: 50017 bytes, SHA-256 `ff856827e462c9cd09fe6068fed7930b06bbf9de0d04b78e1f20bbf3965063a8`
- checker: 13334 bytes, SHA-256 `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`
- driver: 3140 bytes, SHA-256 `4e1550da1b28bf42b2871838b5213e6296b5a3e046607a526daa256c5bf03340`

この最終便では上記3点の bounded static inspection と byte/SHA 照合のみ実施し、download/migration/production は実行していない。コード、driver、workflow は変更していない。

GO

## Immediate driver-only repair audit after run 33328233304

Run `33328233304`, job `99302076654`, stopped before Python/migration with
GAP `Concatenation: arguments must be lists`.  The exact cause is the
one-argument expression `Concatenation(" --resume-v11-url ...")`: with one
argument GAP treats the string as the outer collection to concatenate, so its
character entries fail the list requirement.

The repair replaces only that expression by the same literal GAP string.
Every multi-argument `Concatenation`, the URL, producer/checker pins, resource
limits, paths, workflow, and all Python code are byte-for-byte unchanged.
The repaired driver is 3125 bytes with SHA-256
`b3921e7c975b5bd4dfd2a581829d6c6497230105218dea1af88f0676f7bb1dc8`.
Static inspection finds no remaining one-argument `Concatenation` in the
driver.  Local Windows GAP remains unavailable because of the previously
recorded signal-pipe error; the Linux GHA parse is therefore the next bounded
gate.

**GO for immediate redispatch.**  This repair has no mathematical claim
effect; A0 remains 0/1 actual until a production artifact says otherwise.

## Seq40 recovery re-audit

**NO-GO.**  The producer-side recovery repair itself is closed:

- `normalize_parent_checkpoint` (producer lines 338--345) accepts only the
  exact 326449173-byte / `0b3169fe...` whole-checkpoint seal and additionally
  binds sequence 40, all cursors, occurrence rank/shape, frontier, both
  occurrence nnz counters, and empty/zero physical state.  It changes only
  `parent` to `occurrence_queue`.
- `cp_read` invokes that normalization before its ordinary phase gate
  (lines 357--359), so the one pinned legacy checkpoint is admitted while no
  other `parent` checkpoint passes.  `guard(event)` writes `save(phase, ...)`
  after checking the enclosing canonical phase (lines 446--450), so event
  labels can no longer become checkpoint phases.
- Driver lines 8 and 18 keep input/output paths distinct and select the exact
  v12 input with `--resume`, clearing the v11 migration argument.  The scoped
  changes contain no checker, workflow, search-math, or hot-path change.

There is one dispatch blocker in driver line 17.  The recovery command writes
both the download and extracted checkpoint directly to their final paths
(`curl --output D431RecoveryZip` and `unzip -p ... > D431Input`) and never
enumerates or compares the archive members with the preregistered exact
six-name roster.  Thus an interrupted command can leave a partial final input,
and an authenticated zip with extra/duplicate/path-confusing entries is not
rejected; merely extracting the named member and touching an unbound seal does
not satisfy the frozen atomic/exact-roster gate.  The smallest repair is to
download and extract to fresh relative temporary files, validate zip
bytes/SHA and the exact six-entry roster (including duplicate, absolute, and
traversal rejection), validate checkpoint bytes/SHA, atomically rename both
validated files to their final paths, and create the seal only afterward.
Pre-existing final input/seal must be revalidated or rejected rather than
trusted by existence alone.

Actual final identities match the driver and Luna reply: producer 51884 bytes,
SHA-256 `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`;
checker 13334 bytes, SHA-256
`e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`;
driver 4418 bytes, SHA-256
`b1135b53baf80cea54f9164bc8b23e6b0c12da54c172e8c36e5e33ef52e4d345`.
Bounded `py_compile` and producer `--mode FIXTURE` passed; no download,
migration, or production run was performed.

NO-GO

## Recovery-driver repair re-audit

**NO-GO.**  The prior direct-write/roster defect is repaired, but strict
pre-existing-state authentication still has one dispatch blocker.

Driver line 17 now names the exact v12 six-file roster (the four v12
artifact/checkpoint/log names plus `driver.g` and `run.log`).  Six total lines,
six unique lines, and one exact match for every registered name reject
duplicates, extras, directory names, absolute names, and traversal names.
The exact release URL is `artifact_9738910465_gap-run-out.valid.zip`; its
132415389-byte / `75223cf...` pin and the extracted checkpoint's 326449173-byte
/ `0b3169fe...` pin are checked.  Zip and checkpoint temporaries are created
respectively under `ci/in` and `ci/out`, the same directories as their final
paths, and are moved into place only after validation.  Input and output
checkpoint paths remain distinct.  The seal binds both full hashes, and the
pre-existing branch attempts regular-file, non-symlink, roster, size, hash,
and exact-seal revalidation.

However, `Exec(D431RecoveryCommand)` does not propagate the shell's failure
status, and the only GAP-side postcondition is
`IsExistingFile(D431RecoverySeal)`.  On the pre-existing branch that file
already exists.  For example, take an exact valid input checkpoint, an invalid
zip (or invalid seal contents), and an existing seal pathname: Bash exits
nonzero at the failed roster/hash/seal test, GAP `Exec` discards that status,
the existence test still passes, and line 18 selects `--resume` from the valid
input.  Thus the claimed strict revalidation is not an enforced gate.  GAP
4.16's `Exec` status-discarding behavior is already recorded from installed
`lib/process.gi` in the repository audit record; `set -e` alone cannot carry
success back to GAP.

The smallest repair is a distinct, initially absent completion receipt.  The
shell must create it (preferably temp plus atomic rename) only after either the
pre-existing triple has fully revalidated or the fresh triple has been fully
installed, and GAP must require its exact hash-bound contents.  A stale receipt
must be rejected before `Exec`.  Also use `-e OR -L` both when detecting any
pre-existing final path and immediately before installation: the current
`-e` tests miss dangling symlinks, most importantly a dangling seal symlink
which the final redirection can follow.

Producer and checker remain at their previously audited identities
(`3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`
and `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`);
the scoped repair changes only driver/reply and no task431 workflow or math/hot
path.  The actual driver is 7073 bytes, SHA-256
`8a87290e4cdadb967947471b103f9d2154ed5c9daeffd64ba93f45bead7e67eb`,
matching its reply pin.  In bounded static inspection the 71-part GAP
`Concatenation` reconstructed to exactly `bash -lc <one payload>` with balanced
quoting.  Local `bash -n` could not start because of the already-recorded
Windows signal-pipe error; no download or production run was attempted.

NO-GO

## Final receipt delta re-audit

**GO.**  The prior stale-seal/status blocker is closed.  Driver line 17 rejects
an existing regular receipt before invoking the shell; line 18 additionally
requires both `! -e` and `! -L`, so a dangling receipt symlink also fails
closed.  The shell creates a same-directory receipt temporary only after the
pre-existing-validation or fresh-install branch has completed, writes one
hash-bound line, and atomically moves it to the final receipt path.  GAP then
requires the receipt to exist and exact-matches its complete one-line contents,
so discarded `Exec` status can no longer masquerade as success.

The fresh branch rechecks both `! -e` and `! -L` for zip, input checkpoint, and
seal before installing them.  The exact v12 six-name roster, duplicate/extra
and path rejection, release URL, zip/checkpoint bytes and SHA, distinct
input/output paths, and v12 `--resume` selection are unchanged.  Producer and
checker are unchanged at 51884 / 13334 bytes and SHA-256
`3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3` /
`e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`.
The actual driver and Luna pin agree: 7996 bytes, SHA-256
`924b629340bd3d319b75db1edaa6e7d19a99b9fa5de40dd35719a4cb00eb55cd`.

Bounded reconstruction of the 91-part GAP `Concatenation` produced exactly
three outer arguments, `bash -lc <payload>`, with a one-line payload and one
double-quoted occurrence of
`D972-A0V12-RECOVERY-RECEIPT1 <zip-sha> <checkpoint-sha>` after the branch
`fi`.  No download, production, or dispatch was run.

GO
