# Task979 — 保存済み32段から別GHAで同owner継続するための限定intake

役: producer側read-only設計。変更可は
`sol/luna_reply_979_r07_saved_continuation_cross_run_resume_intake.md` 一ファイルのみ。
公刊source/workflow/974不変。ローカルPython/import/AST/数値/GAP、
network/git/credential、追加agentは禁止。source/JSON metadata/bytes/hashのみ可。

実run33984832010/1のproducerは32追加/rank1418/gen8123/UNKNOWN_CAP/Separatorで完了。
Cは32段再生後HEAD比較FAIL。Task977/978でC metadata隔離と保存済みoutputのみのcompletionを行う。
現時点のrank1418は候補で、completion成功/CV9はまだない。
root認証済みdiag9975236748は `%TEMP%/shadow-atelier-cegar-run33984832010-diagnostics-a1`。
全ZIP101830254 bytes/SHA09ffef9d13e21e27fe9733bf997ec875a5795b5af56c7f4875e36725924d7a35。

本便は、後でこのprefixが受理された場合の次の継続を具体化する。
新数値を作らず、元producer971を改変しない。

1. 同じ19source/runtime/14親と保存outputを別runnerへ完全移送して `--resume --max-appends 64`
   を呼ぶ場合、source/owner/start/fixed/HEAD/invocationのどの値が同一でなければならないかを列挙。
   sys.version/NumPy strings、C修理の新sourceとPのsource hashは別扱い。
   GITHUB_RUN_IDやlaunch commitがP ownerへ入るか、実sourceの経路で確認する。
2. load_prefixが旧32段の何を読み、何を算術再走せずattachするかを型と関数で示す。
   raw/P1/E再生成0と、保存row/全rowの現在測定等が走ることを分ける。
   current snapshot nullの実HEADから始まるが、将来durable phaseがある一般再開規則も保持。
3. 次のworkflowに要る元14親＋新completion artifactのexact pin、保存全file/dir/隠しfile、
   readonly parentとmutable outputの分離、元32prefix不変、before HEAD/max64/after countのgateを示す。
   新completion run/artifact/source pinは未観測として、偽の値を埋めない。
4. C v2が保存全prefixを再照合する方式で実行可能か、追加adapterが本当に必要かを判定する。
   次回登録枠案はP内5400秒/外100分、C内10800秒/外190分、job330分/7GiB。
   累積64は停止枠で、64到達や将来速度を予測しない。現在の固定source宇宙を変えない。

次のversioned workflowにそのまま使える最小変更一覧と、誤ったrestart/reset/owner混入を
拒否する観測可能な条件を簡潔に出す。本便でworkflow実装・GHAはしない。
最終行 `AUDIT_979_VERDICT:`。
