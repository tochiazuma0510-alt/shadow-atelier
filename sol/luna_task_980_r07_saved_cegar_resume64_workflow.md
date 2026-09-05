# Task980 — 保存32段の受理後に同ownerで累積cap64へ進むGHA

役: Luna実装（workflowだけ）。変更可は次の二ファイルのみ。

- `.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml`
- `sol/luna_reply_980_r07_saved_cegar_resume64_workflow.md`

公刊producer/source/返信979/旧workflowは不変。rootがgit/GHAの唯一のbroker。
ローカルPython/import/AST/数値/GAP、network/git/credential、追加agentは禁止。
workflow source編集/読取、公開ABI・metadata/bytes/hashだけ可。checkerの算術を読取/コピーしない。

reply979全文を実装する。同じ凍結producer971と新C v2の通常CLIを使い、数値adapterを新設しない。
現在rank1418/gen8123/32段は候補、Task977 completion成功と工房CV9は未観測である。
**新completion run/artifact/receipt pinsはrootの実観測待ち**。前処理でmissingを必ず拒否し、
未来の値や失敗diagを成功親として埋めない。未観測pin以外の構造とgateを先に完成・保存する。

## 登録入力と実行

新marker `[r07-complete-oracle-cegar-resume64-v1-run]`、workflow_dispatchも用意する。
元14親は凍結continuation-v1の実tupleを保持し、15番目に今後のTask977成功completion候補を置く。
同14親のrun/attempt/head/repository/workflow/expiry/artifact-name/id/size/digestと、
新completion候補の全来歴・旧output不変・新C全32 PASSをlive metadataと保存receiptで認証する。
Task554だけのaccepted failureを誤ってsuccess必須へ変えない。

Python3.13.15/NumPy2.5.1をpinし、Pの実source.jsonと
`3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`/`2.5.1`の全文一致を起動前に確認する。
元source19本＋C v2の計20本/raw3を新source receiptで認証し、ASTはGHA上だけ。
C v2は現時点129557 bytes/SHAe985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3だが、
公刊前なので977最終freezeをrootから受けた値を採用する。
元source/run、修理source/run、今回source/runを別の字段で保持する。

completionをreadonly親rootへ安全展開し、そのoutput全file/dir/hiddenを別mutable outputへ複製。
親とoutputは互いに包含しない。複製前後の全size/SHA/dir rosterと以下のbefore状態を認証する。

- HEAD全file hash d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b、
  completed32/rank1418/gen8123/Separator、current snapshot/checkpoint null。
- owner/source/start/fixed hashはreply979 F1の実pin、startはrank1386/gen8091/completed0のまま。
- 元output2584 files/420 dirs/346710509 bytes、固定32prefixの全旧bytesを保持する。
  root HEAD/resultだけをmutableとして旧bytesをroot外へ退避。既存invocations二件もimmutable。

Pは一回だけ `--resume --max-appends 64 --max-seconds 5400`、外100分。
初回cap1や同job内cap32を繰り返さない。旧32段のbuilder再生成0と、型/bytes/保存row測定を分ける。
Pのstdout/result全bytesとexit0を要求、新invocation一件の明示hashでbefore32/HEAD/cap64/resumeを結ぶ。
after countは32以上64以下、rank=1386+count、generation=8091+count。未来の新rankを推定しない。
UNKNOWN_CAP/UNKNOWN_RESOURCE/二candidateの型を保持。入場前exit3を旧resultのsuccessへ読み替えない。

C v2は同14親＋candidate-rootで全保存32段と新追加分/current checkpointを通常CLIから再生する。
内10800秒/外190分、job330分/7GiB。status PASS/exit0/stdout=report、全new arrays/JSON/HEAD/
terminal/invocation、四scope/8059/54433/二aux/96776/mod54/fourBを要求する。
旧32段を新追加数へ重複計上せず、Cの全prefix件数は累積countに一致させる。

旧oracle v2 full4/P・C三群/五metadata拒否/修理snapshot3件は、成功親の実receiptを認証して再走0。
今回新たに必要なのはcross-run複製・runtime一致・同owner resume・旧prefix不変・全after比較である。
新regressionを足す必要を認めた場合は、その新境界だけを明示してrootへ提案する。

P後の全outputを保存し、C前後で不変を比較。元14親とcompletion親、全20source/raw3も不変照合。
run receiptに実launch/run/attempt/workflow、accepted completion tuple、元P/newC source/runtime、
before/after HEAD/count、今回追加数after-32、停止枠、実resume、各保存receipt hashを記録する。
成功candidateは全C PASS後だけ。always diagnosticsは全producer output/hidden、途中code/log/receipt、
旧成功parentの由来・今回failure/UNKNOWNを完全保存。両artifact retention30日、GH_TOKENは環境のみ。

保存blockの区切りでrootへ進捗を伝える。必要な新completion pinsが未観測ならその箇所だけpendingとし、
それ以外の全文をレビュー可能にする。公開/実走/CV9待ちを成功と報告しない。
最終行 `AUDIT_980_VERDICT:`。
