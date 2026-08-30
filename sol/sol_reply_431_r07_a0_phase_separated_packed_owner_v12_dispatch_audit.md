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
