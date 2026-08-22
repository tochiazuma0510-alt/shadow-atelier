# Luna reply 157a — WO-157-1 D972 dovetail GHA repair audit

## 結論

推奨する clean branch の基点は **`bce25e75c60b752337208d7e9fda42dfe5127d78`** である。この固定点では `.github/workflows/d972-dovetail-v2.yml` が既に、SHA-256 固定 tarball から DMTCP 4.2.0 を build し、version/help/checkpoint exit semantics と stateful checkpoint/restart smoke を検査する形になっている。したがって、この基点からの WO-157-1 の最小差分は次の 1 件だけでよい。

- **削除**: `.github/workflows/d972-dovetail.yml`

この削除は共有 worktree に実施済みである。`d972-dovetail-v2.yml` 自体は変更していない。commit / push / dispatch は指示どおり行っていない。

`origin/master=59aa890e79ba1eb4ff111d7d750f89d9faeccb44` に source-build 部分だけを摘んで移す案は推奨しない。現 fixed point の manifest/producer/worker/checker は v1 library・state schema・semantic-M assets を digest で束縛しており、workflow と manifest だけの移植では閉包しない。`origin/master` を直接基点にするなら、テキスト上の最小差分は `runs-on: ubuntu-22.04` の 1 行 pin と旧 workflow 削除だが、この組合せについて今回の run-backed smoke 証拠はなく、DMTCP/GAP ABI も source-build 契約より弱い。従って「最小」より「既監査固定点」を採る。

## 実行証拠

### 壊れている master cron

- run **32575013338**
- event `schedule`, branch `master`, head `59aa890e79ba1eb4ff111d7d750f89d9faeccb44`
- job `resume-or-run` の `Install and inventory GAP plus DMTCP` が failure
- Noble (`ubuntu-24.04`) で `apt-get install ... gap dmtcp` が `Package 'dmtcp' has no installation candidate`、exit **100**
- 後続の static test / DMTCP smoke / campaign はすべて skipped

### 固定 source-build の Linux 実績

- run **32055311874**
- event `workflow_dispatch`, branch `sol/d972-dmtcp-provision-v420`, head **`983bd8b960c5d71ef686ee0d8a590728913f61d7`**
- `Bash syntax gate for exact DMTCP inventory step`: success
- `Install and inventory GAP plus DMTCP`: success
- `Static wrapper and independent-checker tests`: success
- `DMTCP stateful checkpoint-restart smoke test`: success
- 実測 DMTCP は `4.2.0`; release commit `f8009ce7b4ad211311ca2f72a929b975e4aa1155`; archive SHA-256 `0288457860517cf3b221da794bbf0bea8804d846fcb629a50181a7225b93a392`
- failure はその後の `Run or resume one whole-process slice`（約 2 時間 26 分後、`STATE_STOP incomplete independent calibration output`, exit 3）。これは DMTCP provisioning/smoke failure ではない。

workflow blob は `acdefa54`, run 32055311874 の head `983bd8b9`, fixed point `bce25e75` で同一である。

```text
.github/workflows/d972-dovetail-v2.yml
git blob = 03541f9d0808ad89a415a6c6694549a9cf3d836b
```

また、run head `983bd8b9` と `bce25e75` では次の core blob も一致する。

```text
search/d972_dovetail_manifest_v2.json  a01ccd2ca4c7e89e8a10ea24ecf7b08253fb4bbf
search/d972_dovetail_producer_v2.py    b9dd384201c15249532c5a94d2795db50c951ea7
search/d972_dovetail_worker_v2.g       b7054517db8da970f1caccf3dae661cacbe96ae0
```

従って `bce25e75` 上の provisioning/smoke 契約には run 32055311874 の直接証拠がある。ただし campaign の数学的成功を意味しない。

### 死んだ旧 workflow

- run **32580269313**, head `bce25e75`, event `push`
- run name/path が `.github/workflows/d972-dovetail.yml`
- created と updated が同時刻、jobs は空配列、即時 failure
- 同型の 0 秒 failure が複数 branch push で反復している。

従って旧ファイルの削除は residue cleanup として妥当である。

## predecessor と checkpoint compatibility

2026-08-23 の read-only GitHub 照合では、v2 workflow の successful run は **0 件**、live artifact `d972-dovetail-v2-state` も **0 件**だった。従って最初の修理 run は predecessor なしの genesis seed になり、旧 DMTCP image を誤って resume する危険は現時点ではない。

ただし最初の successful artifact が出来た後は、selector は全 branch の successful v2 run から最新の live artifact を自動選択する。明示 `resume_run_id` も「最新と一致」しか許さず、blank は fresh seed 指定ではない。さらに workflow は artifact 内 `source_commit` に detach し、trigger 側と source 側の supervisor **content SHA** 一致を要求する。従って 5 分 test 後は次を守る必要がある。

1. test に使った commit を fast-forward/merge で到達可能に保つ（branch を先に消さない）。
2. master 配備時に `d972-dovetail-v2.yml` の byte content を変えない。
3. DMTCP/runtime compatibility drift が起きた場合、現在の selector には fresh-seed escape hatch がないため、UNKNOWN/STATE_STOP として別修理が必要。

## 5 分 manual dispatch の判定力

`slice_minutes=5`, `resume_run_id=""` の manual dispatch は、現在 artifact がないため次を一度に検査できる。

- pinned source download/build/inventory
- producer/checker static self-tests
- Python process と GAP worker の DMTCP checkpoint/restart smoke
- campaign process tree の `--kcheckpoint`、envelope seal、artifact upload

既往 run では campaign failure は 5 分より十分後だったため、5 分 deadline で suspended generation を作る設計は妥当である。ただし実 run 未実施なので成功とは記帳しない。成功しても確立するのは **provisioning/checkpoint plumbing と UNKNOWN/RESUME artifact** のみで、A/B は引き続き UNKNOWN である。

## ローカル静的監査

- PyYAML parse: `YAML_OK steps=14`
- `python -m py_compile search/d972_dovetail_producer_v2.py search/check_d972_dovetail_v2.py`: pass
- `python search/d972_dovetail_producer_v2.py --self-test`: PASS
  - `binding_set_sha256=34132db41c7fb1b3083a8cefc5e68c61d4b69887e2dee68bd5ab443e433ed1e1`
  - `contract_sha256=f4eb427c13561354992ff5dbed2b98d53e6dce318fa586f1afe12b616fe4b741`
- ローカル Git Bash の `bash -n` は sandbox の `CreateFileMapping ... Win32 error 5` で起動不能。代わりに、同一 workflow blob に対する GHA run 32055311874 の workflow 内 bash syntax gate success を証拠とする。
- checker `--self-test` は Windows sandbox が `TemporaryDirectory` への access を拒否して未完。数学的 failure ではない。

注意: checker self-test の試行が空ディレクトリ `scratchpad/d972-v2-receipt-selftest-krla27pj` を作ったが、sandbox の deny ACL により exact-path の `Remove-Item` と `icacls` の双方が拒否された。stage 対象に含めないこと。この副作用は親へ即時通知済みである。

## 親セッションへの handoff

1. clean branch を `bce25e75` から作る。
2. この worktree の `.github/workflows/d972-dovetail.yml` 削除だけを exact-path stage する（他の大量の dirty/untracked file を絶対に含めない）。
3. commit/push 後、`slice_minutes=5`, blank predecessor で v2 を manual dispatch。
4. run ID と commit SHA、各 plumbing step、artifact upload の有無を親の最終返書に記録。
5. master cron への統合は、test commit の到達可能性と supervisor bytes を保った経路で行う。

残る blocker は親 broker による commit/push/dispatch と master 統合だけである。

## Addendum 157a-1 — 旧 workflow 削除後の genesis binding 修理

### 再 dispatch の観測

親 broker による 5 分 run **32581574880**（head `2617bfd701009582e7075dd971a3e1980274f6e1`）では次が success になった。

- DMTCP source-build / inventory
- producer/checker static self-tests
- stateful DMTCP checkpoint/restart smoke

campaign は開始直後に

```text
STATE_STOP required code absent: .github/workflows/d972-dovetail.yml
```

で停止し、artifact upload は skipped だった。従って provisioning 修理は実 run で成立した一方、genesis seed の legacy code binding が旧 workflow をなお必須としていた。

### 原因

v2 producer は fresh launch で `legacy.initial_state()` を呼ぶ。その内部の v1 `_bind_seed_integrity()` は `search/d972_dovetail_manifest_v1.json` の

```json
{"path":".github/workflows/d972-dovetail.yml","required":true,"sha256":null}
```

を bind しようとするため、v2 wrapper が state receipt を付与するより前に fail-closed していた。successful v2 artifact は引き続き 0 件なので、既存 checkpoint の migration は不要であり、行ってはならない。

### 実装した最小 versioned repair

`.github/workflows/d972-dovetail-v2.yml` の bytes は変えず、次の 2 ファイルだけを修正した。

1. `search/d972_dovetail_manifest_v2.json`
   - contract version を `d972-dmtcp-whole-process/v2.1` に更新。
   - `d972-legacy-seed-workflow-rebind/v1` を追加。
   - scope を `fresh-genesis-seed-only` に固定。
   - 旧行の exact precondition、v2 workflow への replacement、`existing_checkpoint_migration=false`、precondition drift の fail-closed を pin。
   - 新 contract SHA-256 は `343ffe0b5c14d186b6e423c449048084c2b6a03e0e651c160a61810887f0c750`。
2. `search/d972_dovetail_producer_v2.py`
   - `install_v2_adapter()` が legacy `_bind_seed_integrity` を fresh-seed 限定 wrapper で包む。
   - state schema、`integrity.ready=false`、旧 workflow 行全体が contract precondition と完全一致する場合に限り path を v2 workflow へ変更し、元の binder を呼ぶ。
   - bind 後の path / required / SHA-256 も完全一致で再検査する。
   - bound state や異なる seed row は migration せず `STATE_STOP legacy seed workflow rebind precondition drift`。
   - versioned rebind spec を v2 runtime-integrity receipt に含める。
   - producer self-test に正例と `required=false` 陰性 canary を追加。

### ローカル test

```text
python -m json.tool search/d972_dovetail_manifest_v2.json          PASS
python -m py_compile producer_v2.py checker_v2.py                  PASS
python search/d972_dovetail_producer_v2.py --self-test             PASS
legacy_seed_workflow_rebind                                        PASS
campaign_loop_fixture                                              PASS
checker expected_runtime_receipt direct reconstruction             PASS
```

新しい runtime `binding_set_sha256` は

```text
fa72f255a33a5837421489d01498e84604b21c4ed63ee0bcb8c1617c058c528f
```

である。checker の full `--self-test` は既知の Windows deny-ACL tempfile 副作用を避けて実行していない。独立 checker module の `load_manifest()` と `expected_runtime_receipt()` による direct reconstruction で、version、`existing_checkpoint_migration=false`、同じ binding-set digest を照合した。campaign の最終判定は次の Linux GHA run に委ねる。

### exact file digests（再 dispatch 用）

| path | bytes | SHA-256 |
|---|---:|---|
| `.github/workflows/d972-dovetail-v2.yml` | 32056 | `86806791346ed4cf9063a7c4fefaaa2c3aa414decc32973a3b4efa5633a41d7f` |
| `search/d972_dovetail_manifest_v2.json` | 15051 | `0abe98057b81bca1c626d0e2b6708bd82430e361b219c9c7e401f1d206e6fcf8` |
| `search/d972_dovetail_producer_v2.py` | 40727 | `0c59ff1aa54aa15e88a19302140eae9413413f03c8b7fd62f1f7685f875a08be` |
| `search/check_d972_dovetail_v2.py`（未変更） | 89493 | `ddfe0a0725f4281df3ce488e8c541dce5d890dda6a7634ce438c31db88dcd7c4` |

v2 workflow digest は修理前と同一である。次の commit では旧 workflow の削除、上記 manifest、上記 producer、および報告ファイルだけを exact-path stage すればよい。passing run が作る suspended image は引き続き UNKNOWN/RESUME であり、A/B authority はない。
