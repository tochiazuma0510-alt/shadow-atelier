# Task968 — u32 root sentinel 修理と保存 oracle の checker completion

F0. **v2 checker と13親の checker-only workflow を作成した。新照合はGHA未実行。** Task968全文を読み、Task966を途中保存して中断した。変更は本便の指定3ファイルだけ。公開済み959/960/961のsource/workflow/replyは変更していない。ローカルPython/import/AST/数値/GAP、network/git/credential/dispatch、追加agentは実行していない。以下の実観測は保存JSON・file bytes・hash・source本文の読取である。

| 作成物 | bytes | SHA256 | LF |
|---|---:|---|---:|
| `search/check_d972_r07_section_cochain_oracle_v2.py` | 84402 | `a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d` | 1272 |
| `.github/workflows/d972-r07-section-cochain-checker-completion-v1.yml` | 44679 | `b439c24229523daec90570f527a72a5bdc5c32f475fd3a1ad0361922a0cb60e8` | 704 |

両ファイルはCRなし・末尾LF。sourceはroot/Task969が差分を全文読みblockerなし。workflowもTask969が最後の不変gate/receipt/uploadまで全文読み、追加修正なしと連絡した。この表を最終freeze値として通知する。新GHA/CV9完了を意味しない。

F1. **失敗の所在と最小修理。** 元run33975617653/1、head `c57a722224320f9a573cfe84dea6979df5cb5320`、job101331666867は2026-09-05T15:45:37Z failure。rootによる実行時間の観測はproducer約69秒、checker約65秒。保存されたchecker-resultは `status:FAIL,phase:complete_tree_eof,reason:OverflowError:Python integer 4294967295 out of bounds for int32` である。v1 `geometry_payloads` の二つの `np.where(int32-array,4294967295,...)` がNumPy2.5.1でcoercion例外となり、`check_actual` のstage比較loopへまだ入っていなかった。Task960の静的source読取ではこのruntime型境界を見落とした。全配列一致やchecker PASSは成立していない。

v1 80740 bytes / `2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967` を新v2へ複製し、production `geometry_payloads` のparentとparent-edgeを `rooted_indices_u32` に渡した。helperは1次元のsigned int32/int64配列、位置0だけのroot=-1、非rootの非負性と上限未満を確認する。parent上限は54432、parent-edge上限は108864。別のint64配列へcopyし位置0へ4294967295を代入した後、明示little-endian u32へ変換する。元配列を変更せず、他の負値や上限外値をwrapしない。

変更はこのserializer helper、専用canary/CLI、冒頭説明、productionの二呼出しだけ。A–Dの数学/source/solver、owner/start/result、選択規則、公開 `d972.r07.section-cochain-oracle.v1` schemaはそのまま。Task969は宣言した差分を文字列として逆適用すると旧v1全文と一致することも確認した。旧producer 73290 bytes / `4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb` は再走しない。

F2. **専用serialization gate。** `--serialization-selftest` は実production helperと `typed_array` を呼ぶ。int32のroot/0/末端parent・parent-edgeに対して `ff ff ff ff` と正indexのlittle-endian全bytes、元配列の不変を要求する。非root -1/-2、root不正、parent/edge上限、oversized int64、float/unsigned/bool/list/2次元/空配列、非整数boundを拒否する15件の限定receiptを出す。旧full selftest、実parent両経路canary、producerは呼ばない。新helperが実serialization経路に接続していることをGHAで試す専用CLIであり、ローカル実行結果はない。

F3. **実diagnosticのmetadataを独立に確認した。** root回収rootは `%TEMP%/shadow-atelier-section-oracle-run33975617653-diagnostics-a1`。元artifactはid9972256636、name `d972-r07-section-cochain-oracle-v1-diagnostics-33975617653-1`、ZIP2271586 bytes / `c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a`、元workflow `.github/workflows/d972-r07-section-cochain-oracle-v1.yml`。ZIP/live tuple自体はrootの回収証拠で、新workflowでもexact live APIと実download ZIP bytes/SHAを要求する。

次の8 entryを独立にbyte/SHAで照合した。

| entry | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 315 | `e500b7fa0a5f4387c36d787999f438cea91189b9ea3fd8ec80e0830cb29173e0` |
| source-receipt.json | 2673 | `cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934` |
| output/manifest.json | 1430 | `7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639` |
| output/owner.json | 8419 | `6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322` |
| output/start.json | 48377 | `7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a` |
| output/source.json | 1246 | `af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac` |
| output/result.json | 13727 | `c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312` |
| output/tree/witness.json | 486 | `1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd` |

さらにtop/stage manifestの全file receiptを読み、output全44ファイル・4ディレクトリ・5361492 bytesの全長/hash/rosterに一致、reparseなしを確認した。これは保存物の認証であり全arrayの数学再計算ではない。実sourceのruntimeはPython `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`、NumPy2.5.1。workflowは元の `sys.version` 文字列ともexact equalityを要求する。

保存producer treeはaux `[0,0]`、selected chords `[2,3,4,6,11]`、first failed chord12、residual nonzero36343、witness scalar1を記録している。これは未照合の候補の観測値である。v2の期待算術へこの数列をliteralで埋め込まず、全A–Dを自分で再計算して全bytesを比較する。修理前のFAILをPASSや受理oracle親に読み替えない。

F4. **13親・runtime/sourceのclosure。** 元workflowの12親exact tupleとsource/data pinsを保持し、13番目に今回のdiagnosticを追加した。run/attempt/head/workflow/status/conclusion、artifact id/name/bytes/digest/expiry/repositoryを全件確認し、13番目はconclusion failureを要求する。新ZIPは実bytes/hashを確認してから相対path・symlink等を検査して展開する。branchは `sol/r07-explicit-lift-20260825`、markerは `[r07-section-cochain-checker-completion-v1-run]`。

原14 Python実行体と二raw dataを認証し、原source-receiptと同じcanonical bytesを再構成して一致させる。新v2を加えた15本と新workflow hash、launch/run/runtimeは `repair-source-receipt.json` へ別記録する。Python ASTはGHAだけ。raw g/word JSONはbytes/SHAのみでCRLFや終端を正規化しない。Python3.13.15・NumPy2.5.1・元sourceのfull runtime文字列を保持する。

F5. **保存不変と新旧receiptの分離。** 元output全体とsource-receiptをcompletion配下へcopyし、全ファイルのorigin path/bytes/SHA、全output directoryを `preserved-input.json` に保存する。旧FAILとlogは `previous-checker-result.json/previous-checker.log` へ移し、旧canary/parent-layoutの保存receiptは再走せずcopyする。v2 source/new workflowそのものも `repair-source/` に別保存する。元source-receiptと `output/source.json` を修理側のsource receiptで置き換えない。

新serialization gate→新v2 checker一回（内部1800秒/外40分/job60分）→全8059式/54433chord/2aux/全stage・top比較PASSの順とした。checkerはcheckpointを持たないため必要なA–D全再計算を行う。旧26scan/insertやproducer・旧成功suite・旧parent canaryは0回である。実checker invocationの開始markerとexit codeを保存する。

finalizeはchecker成否にかかわらず、元とcopy双方の全saved file bytes/hash、output全roster・directory、原source receiptの不変を照合する。PASS時は新checker SHA/runtime、全array gate、元manifest/start/owner/result/stage refs、rank/generation/state head/target derivation/direct pairingを結ぶ。元producerの出力と新completionの由来を分けた `completion-run-receipt.json` を出す。candidate uploadは新checker PASSと不変gateの両方の後だけ。diagnosticsはalways。UNKNOWN_RESOURCEや比較未完はcandidateにしない。

F6. **TCBと残るgate。** SOURCE_MAP、accepted P1/Conn、普通の群係数source錨、current dense対packed P1というTask961の境界、裁定2131の七限定は不変。旧full-originの走査算術F-fo-1の独立性不足も残る。原rho2は明示DERIVEDであり、新直接読込値ではない。新scalar oracleの受理・CV9、Eによる実体化、grade2 MEMBER/NONMEMBER、全11slot/全A0はこのsource修理だけでは成立しない。verified=false。

残るのはTask969の正式返信とroot release、その後GHAのAST/専用serialization/new checker全array比較/保存不変gate、および実completion artifactのpin・CV9である。本便はdispatchしていない。rootが受理した成功completionのexact pinを受領してから、Task966の薄いloaderにv1 producer/sourceとv2 checker completionの二つの由来を接続する。

AUDIT_968_VERDICT: SOURCE_AND_CHECKER_COMPLETION_WORKFLOW_FROZEN — Task969 static source/workflow review found no required change; all new GHA/CV9 gates pending; verified=false.
