# Task978 — 継続checker snapshot alias故障の独立delta監査

役: read-only数学/source監査。変更可は
`sol/luna_reply_978_r07_cegar_checker_snapshot_isolation_audit.md` 一ファイルのみ。
公刊973/976/source/workflow不変。ローカルPython/import/AST/数値/GAP、
network/git/credential、追加agentは禁止。source/metadata/bytes/hash読取だけ可。

Task977全文を読み、同じ実diagとfail-result/producer-result/HEAD/32段manifest/ログを読む。
実run33984832010/1、diag9975236748、root展開先
`%TEMP%/shadow-atelier-cegar-run33984832010-diagnostics-a1`。
P32行/rank1418/gen8123/UNKNOWN_CAP/Separator、Ccursor32後HEAD完全比較FAIL。
数値一致の正式格は未受理、既往rank1386/gen8091を保持。

rootはv1 summary/derived→root_start_owner/current snapshotのmutable parent参照を原因として
静的に特定した。startの親33件がstate32段で65件へappendされ、末尾HEADで再hashされる経路を
独立に検査する。producer immutable bytesを修正せずC側metadata所有を隔離するのが妥当か裁定。
特にstartだけではなく過去snapshot/DERIVED/diagnostic receiptへ出るaliasを全て点検する。

977が作る新v2とC-only completion workflowをdelta監査する。
- 算術とscope/pins/九phase/完全HEAD/terminal/invocation比較のgateを弱めていないこと。
- 新regressionが実serializer/state境界を通り、元のaliasなら失敗し、start/過去snapshotは
  不変でcurrent stateは正しく更新されることを要求する。実試験はGHAまで未観測。
- 元14親＋失敗diagのlive役割付き認証、20source/3raw、全output保存、元19source由来join。
- 成功済み旧suite/P再生成0、新Cのみ全32段/現在HEADの完全再照合。両run/runtime/commit/試験/失敗
  由来を区別し、元Ccursor32を完成PASSへ格上げしない。全候補/always診断保存を確認。

各sourceの最終hashとdiff範囲、workflow全文を読み、必須修正を早期にroot/977へ伝える。
runtimeとCV9、旧TCB/独立性限定、grade2/A0の境界は保持。
最終行 `AUDIT_978_VERDICT:`。
