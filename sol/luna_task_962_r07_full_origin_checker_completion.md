# Task962 — 保存済みfull-origin prefixの照合だけを完了するGHA

役: Luna / workflow実装。Task961のactual親待ち中に本便を先に完成し、後で961へ戻る。
変更可は `.github/workflows/d972-r07-full-origin-checker-completion-v1.yml` と
`sol/luna_reply_962_r07_full_origin_checker_completion.md` の2本のみ。
source/JSON/byte/hash読取だけ。ローカル数値/Python import/AST/GAP/network/git/
credential/dispatch/追加agentは禁止。rootがrelease・GHAの単一broker。
公開済みproducer/checker/workflowは変更しない。新算術sourceも作らない。

## 実際に観測した未了

full-origin v1 run33967668257/1、commit
`fd04734d20d472e7c09f31de3f92f8a50d6d841a`、job101310528880は
2026-09-05T14:04:19Zにfailureで終了。producer cap1とresume32はsuccess。
独立checkerは14:04:11Zに内部1800秒のResourceStopで終了した。
ログの実checker-resultはstatus UNKNOWN、terminal UNKNOWN_RESOURCE、
prefix_steps_replayed=22、complete_scans_replayed=22、phase=new_actor_fold、
elapsed_seconds=1804.649、candidate/cross_checked/verified=false。
未完なのでPASSではない。算術FAILが観測されたわけでもない。

唯一のartifactはdiagnostic:

- ID9970826495
- name `d972-r07-full-origin-refinement-v1-diagnostics-33967668257-1`
- ZIP51954614 bytes
- SHA256 `15c7686a1b79f343c544498f6a04c1eabdac1cc7559cf337f819030c2ec85159`
- workflow `.github/workflows/d972-r07-full-origin-refinement-v1.yml`
- repository ID1312092366、owner/repo `tochiazuma0510-alt/shadow-atelier`
- rootがダウンロード/byte/hash/JSON確認中。完了後TEMP pathとentry pinを後送。

## 新workflowの具体的スコープ

旧full-origin v1 workflowを読んで旧11親tuple/入力取得/source/data pinを保持し、
上記failed diagnostic親を12番目に固定して取得する。live runはこのrunだけ
completed/failureを要求し、全tupleを曖昧なlatest/name検索にしない。

marker `[r07-full-origin-checker-completion-v1-run]`、現sol作業branch、
workflow_dispatchも可。producerは一度も実行しない。旧成功canary/suiteも再走しない。
source/ASTはGHAで元producer/checkerとretained lineageを固定する。

保存diagnosticのoutput/HEAD/result/owner/source/index/全steps/scansをbyte不変の
candidate-rootとして、凍結済み
`search/check_d972_r07_full_origin_refinement_v1.py`
75083 bytes、SHA256
`1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2`
を一回だけ呼ぶ。元producer97806 bytes/SHA
`d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa`
もsource receipt再構築のため固定する。入力roots/CLIは元と同じ。

内部 `--max-seconds 7200`、checker step125分、job145分。
未完ならUNKNOWNのまま、時間上限を数学的範囲の変更にしない。
全prefix replayを完了してPASSを得る必要がある。今回は旧checkerに再開機能が
ないため全新prefixを読み直すが、producerや旧base/delta算術は再走しない。

元diagnosticのsource-receipt.jsonは不変のまま保存し、新checker-result.jsonと
同梱する。元checker-result.jsonはprevious-checker-result.json等の別名に保持し、
取り違えない。candidate artifactの最上位は元output/とsource-receipt.jsonと
新checker-result.jsonを含み、元resume-before/resume-after/parent-layoutも保持する。
新run由来はcompletion-run-receipt等の別receiptへ明示する。rootが後続oracleへ
渡すtupleはこのcompletion run candidateで、producer/source/stateは元run由来。

checker PASS後だけcandidate upload。diagnosticsはalways、新旧resultを区別。
候補の名前は新workflow名candidate＋run/attempt。
出力のcross_checked/verified=falseを保持。工房CV9と裁定は別gate。

完成後に全source/workflow行数・bytes/SHA、元からの変更範囲と未実行事項を
指定返信へ記録。最終行 `AUDIT_962_VERDICT:`。rootが全文読みcommit/pushする。
