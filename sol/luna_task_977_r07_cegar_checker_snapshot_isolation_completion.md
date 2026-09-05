# Task977 — 継続checkerのsnapshot隔離修理と保存済み32段completion

役: Luna独立checker実装。変更可は次の三つだけ。

- `search/check_d972_r07_complete_oracle_cegar_continuation_v2.py`
- `.github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml`
- `sol/luna_reply_977_r07_cegar_checker_snapshot_isolation_completion.md`

公刊v1 source/workflow/reply972/975は不変。rootがgit/GHAの唯一のbroker。
ローカルPython/import/AST/数値/GAP、network/git/credential、追加agentは禁止。
source編集/静的読取、JSON metadata/bytes/hashのみ可。producer新算術を読取/import/コピーしない。
新workflowの事前source監査と実pin固定後にrootが実GHAを発火する。

## 観測済み故障と保存親

run33984832010/1、head b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e、
job101356330429、workflow d972-r07-complete-oracle-cegar-continuation-v1.yml。
P cap1/resume32 success、C stepは18:56:51–19:09:25Z failure、全保存不変チェックsuccess。
root回収ZIPはartifact9975236748、name
`d972-r07-complete-oracle-cegar-continuation-v1-diagnostics-33984832010-1`、
101830254 bytes / SHA256 `09ffef9d13e21e27fe9733bf997ec875a5795b5af56c7f4875e36725924d7a35`、
expiry2026-10-05T19:09:26Z、repository/head_repository 1312092366。
rootの全ZIP hash一致、安全pathの全2636 entry展開済み。
実読取先 `%TEMP%/shadow-atelier-cegar-run33984832010-diagnostics-a1`。
outputはpreservation receipt上2584 files/420 dirs/346710509 bytes、全不変PASS。

`checker-exit-code.txt` は1。checker-resultはFAIL/candidate=false、reason
`ValueError:cegar_checker:HEAD_entire_replayed_prefix_and_cursor`。
checked_cursorはcompleted_steps32/last_complete_phase physical。ログはstep32独立再生と
最後のcurrent all-row測定の末尾まで到達。正式PASSやrank受理ではない。
producer resultはUNKNOWN_CAP/Separator、completed32/rank1418/gen8123。
state_head `0c2451e45fb1859f1ebe9f3fcbada1caefffb9f9c9adb222521cd556c3cdc2dd`、
target `cbe44dbec2f40a06f90636f6ae66d3d24c4002f44b4358b642376da3c9eee139`、
lambda `ecac50df38ce180d220b64e24ce5f53b163d65c3c54c7372c4b36e6ddc82e04b`、
current snapshot/checkpoint null。受理済み起点はrank1386/gen8091のまま。

## 修理する不具合

rootの静的追跡ではv1 `PhysicalState.summary/derived` が `self.parents` のmutable参照を返し、
`root_start_owner` がそれを浅くsealする。各attachのappendで、開始時に作ったstartの二つの
parent-listも伸びる。replay_head_prefix冒頭のstart_shaは固定される一方、末尾head_recordは
変化後のstartを再hashするため最終HEADだけが不一致になる。実startは親33件、finalは65件。
snapshot_recordも同じsummaryを使い、attach後のreceipt hash等に同種aliasが残り得る。
この因果を実codeから独立確認し、**immutable metadataの境界をdeep-copyで隔離**する。
head equality gateを弱める、実producer HEADをexpectedへコピーする、hashを無視する修理は禁止。

- v1を新v2へ複製し、root start/current snapshot/derived parentsの所有境界を必要十分に修理する。
  全算術・scope・accepted pins・serial形式・source adapter・九phase比較は原則不変。
  一箇所のrootだけを隠すのでなく、summary/derivedが外へ出る全箇所を点検する。
- 不正なmutable参照を残したcontrolではseal/hashが変わり、修正版では開始時と過去snapshotが
  state append/深いparent字段更新を受けても不変、という新専用regressionを追加する。
  実PhysicalState/実serializerの入口を通す。正しい更新後current stateは進むことも確認。
  ローカル実行は禁止。専用CLI/selftestはGHAだけで実行する。
- actual HEAD/terminal/invocationの完全比較を保つ。新sourceで初めて全gate PASSを確認する。
  戻りreceiptに過去snapshotの間違ったhashを残さない。修理範囲と保持TCBを明記。

## 保存済み出力だけを使うcompletion workflow

marker `[r07-complete-oracle-cegar-checker-completion-v1-run]`、workflow_dispatchも用意。
元942行workflow/旧oracle checker-completionの実親取得を参考に、元の14親＋上の失敗diagを
live exact run/attempt/head/repository/workflow/artifact id/name/size/digestで認証する。
Task554と今回diagのfailureは役割つきで許容し、成功親へ一律successを適用しない。
元P/C19 source＋新v2の20 source/raw3をGHA AST/bytes/SHAで固定し、旧source-receiptとjoin。
元producer/runtime/source/run、新v2 checker/runtime/runの由来を分ける。

1. diag ZIPを完全認証・安全展開。全output files/dirsと各小receiptのbytes/hashを固定。
   rootが次に渡す実entry hash表を受領後固定。未観測pinを作らない。
2. 新snapshot isolation regressionだけを内部240秒/外5分で実行。
   既にPASSしたoracle v2 full四件、新P/C三群/五metadata拒否は再走せず、diag保存receiptを認証する。
   producerの全計算・旧26scan・外部E・新32Eの再生成は**0回**。
3. 保存outputをcandidate-rootに、修理C v2だけで**全32 committed prefix/current HEADを再照合**。
   内10800秒/外190分、job230分/7GiB。全算術を再生して最終HEAD/terminal/invocationまでPASSが必要。
   checker資源停止/失敗をPASSへ転換しない。CLI schemaは既存payload v1を保持してよい。
4. source/raw/全親/outputの前後bytes不変と、旧C failure、新C PASS、元P32/新P0、
   original source/current checker/source/runtime/launch/runを結ぶcompletion receiptを残す。
5. candidateは完全PASS後だけ。always diagnosticsは保存済み全producer output、
   旧/new checker receipts/log/code、source/intake/preservation、新試験結果を含む。retention30日。
   hidden pendingを落とさず、不変保存。GH_TOKENはprocess環境のみ。

成立しないgateや別故障を発見したら、具体値と差分を直ちにrootへ伝える。
source/wfを段階保存し、最終freezeのbytes/SHA/LFをroot/978へ連絡する。
受理/cross-checked/grade2/A0は先取りせず、最終行 `AUDIT_977_VERDICT:`。
