# Task1029 — 固定lambda k64 batch v2 初回workflow

## F1. 変更範囲と静的基点

公開1025・1029・1030を全文読み、新 `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml` と本票だけを作成した。旧WF v1全1993行（142206 B / SHA256 `8596ab900175c69cc38085c0caa0455a75dd74eb251e7eb2870a05e030490c73`）を基点とし、k64登録・新source識別・新二群・全fixture保全を移行した。旧source/旧WF/既刊票は不変。新Pの数学本文・私的1023/1026票は読まず、root公開CLI/型/最終pinだけを使用した。

最終WFは **166471 B / SHA256 `887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5` / LF2314 / CR0 / BOMなし / 最終LFあり / 末尾空白0**。全差分の静的読了と実bytes/hash照合を終えた。基点の旧57関数のうち47関数は全文同一、10関数を限定変更、10関数をfixture関連のmetadata処理として追加した。親env全体、および保持code/data/親entry/旧実receipt定数ブロックも全文同一。旧WF全hashも上記のまま一致した。Python/ASTでこの比較を実行したという意味ではなく、PowerShell/.NETの文字列比較である。

## F2. 登録、実親、source閉包

外側prefixは `d972.r07.fixed-lambda-cycle-batch.v2`、本WF自身のreceiptはその `.workflow-v2.*`。登録は普通整数 `batch_size=64,max_batches=1`、`refill=false`、`CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX`、`PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY`。canonical受付比較でbool/float/stringの等値を許さない。旧inner phase/親schema、nonce32hex、int32、歴史のbefore32等は変更しない。新ordinal/local rowは0..63、private sequence上限387であり、採用64を期待値にはしない。

唯一のcontinuation親は実 run33990567016/1、head `c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70`、candidate9977040548、ZIP304642285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`。旧64段/rank1450/gen8155と、元14＋continuationの全15親を保持する。旧64成功C全receipt、元32の全prefix比較、全invocation、全source/runtime、Task554型、全file/dir、live tuple/ZIPの全bytes/SHA/EOFへの入場をそのまま残した。別k32、control96/rank1482、positiveの第16親を採用しない。rho2は既存97親のDERIVEDを保持する。

| 新実行source | bytes | SHA256 | LF |
|---|---:|---|---:|
| `search/d972_r07_fixed_lambda_cycle_batch_v2.py` | 208805 | `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e` | 3420 |
| `search/check_d972_r07_fixed_lambda_cycle_batch_v2.py` | 177544 | `4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90` | 2675 |

保持P9/C10 Python＋上の新2本＝21 Python、raw3を足した全24fileについてローカル実bytes/SHAをmetadataとして照合し全一致した。保持配列は公開1002および旧WF全文と一致、旧batch v1は新closureに追加しない。GHAでは全24をcheckout-sourcesへ保存し、実runtime/driver/WF/source-before/middle/afterへ結ぶ。Python実完全文字列は `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`、NumPyは `2.5.1`。今回のローカル照合にP本文読解・importは含まない。

## F3. 入口と試験登録

作業branch `sol/r07-explicit-lift-20260825`、push marker `[r07-fixed-lambda-cycle-batch-v2-run]` と入力なしworkflow_dispatchを登録。checkoutは実 `github.sha`、credentials非永続、権限はcontents/actions read。`RUNNER_TEMP/fixed-lambda-batch-v2` と同 `fixed-lambda-batch-v2-inputs` は作成前に不存在/非symlinkを確認する。fresh本P一回・本C一回、自動resume/retryなし。

旧metadata16件は新REPORT/登録/sourceの実受付を通す**回帰16件**として再実行する。旧数学成功suite再走は0。metadata receipt/gate/run receiptにこの区別を記載した。新数学自己試験は以下のP/C各二群だけで、すべて未実行である。

| 群名（両者同順） | Pの拒否登録数 | Cの拒否登録数 |
|---|---:|---:|
| `k64-version-registration-and-types` | 30 | 28 |
| `k64-full-roster-cutoff-and-restoration` | 8 | 7 |

各selftestは内300秒/7168 MiB、外360秒。sealed topのexact字段と二要素tests、各 `{name,status,rejected_cases}`、PASS、非空str/list、ordinary `old_success_suites=0`、`actual_anchor_arithmetic_replayed=false`、candidate/cross_checked/verified全falseを実stdoutへ結ぶ。新Pだけに `--batch-size 64` を渡し、新Cへ不要な同flagを追加しない。旧三群は呼ばない。

GHAでの実コマンドは `python -B <P-v2> --selftest --selftest-root "$REPORT/selftest-fixtures/P" --batch-size 64 --max-seconds 300 --max-memory-mib 7168` と、`python -B <C-v2> --selftest --selftest-root "$REPORT/selftest-fixtures/C" --max-seconds 300 --max-memory-mib 7168`。外側で既存regular parent `selftest-fixtures` だけを用意し、P/C rootは各CLIがfreshに作る。数学親/acceptance/本outputをselftestへ渡さない。絶対rootはargvとstart/resultおよびfixture baselineへ結び、架空のsource自己試験字段は要求しない。

## F4. 全fixture、空directory、部分停止の保全

各自己試験の成功gateでP/C root全scanを `fixture-baselines/P.json,C.json` へ固定する。正常/拒否fixture、失敗ledger、hidden tail、意図的に空のsynthetic host directoryを全て含め、private layoutの一覧を推定しない。`before-producer`、`before-checker`、`after-checker` の各stageでP/C subtreeの全files/dirs/descriptorsを完全比較し、各inventoryと比較票を保存する。P前の旧全control baselineにも両treeが入り、全既存control file/dir不変を保持する。REPORT自体への後続の正当なoutput/receipt追加は許し、fixture内への追加は完全比較で拒否する。

alwaysの `fixtures` modeは、実在する `selftest-fixtures` 全体を独立scanし、subtree外の `selftest-fixtures.zip` に全directory entryを明示収録する。regular fileはstream読取りで全bytes/SHA/EOFを確認し、ZIPを再openして全entry集合、directory type/空EOF、展開fileの全bytes/SHA/EOF/CRCを元scanへ照合する。safe POSIX名、duplicate/casefold/type/no-linkを保持し、再読後の元tree全scanも一致させる。raw fixtureは削除しない。metadata処理の登録枠は内300/外360秒・7168 MiBで、新数学再演は0。

独立scanは `selftest-fixtures-inventory.json`、ZIP全entry再読は `selftest-fixtures-archive-readback.json`、作成後全scanは `selftest-fixtures-after-archive.json`、結果は `selftest-fixtures-archive-receipt.json`。全pinはrun receiptとalways artifactへ結ぶ。可変mtime/ZIP digestだけから元treeの不変を主張しない。

**archiveのPASSと両試験の完成は別条件である。** comparisonがINCOMPLETEでも、実在する部分fixtureを全収録・全再読できた場合はarchive処理自体のstatusがPASSになり得る。この場合 `both_completed_roots_unchanged=false` で、未形成rootを完成した空rootへ補完せず、最終candidate gateは拒否する。未形成/部分停止は実presence・PARTIAL/UNFORMED・missingとして記録する。許されないlink/typeでscanが失敗すれば理由とFAILを残し、問題entryを黙って除外したarchiveを全保全PASSにしない。REPORT scanも失敗した時はrun receiptへ実errorを残してcandidate=falseとする。

## F5. 本P/Cと完成candidateの境界

本Pは15登録root（block4回）＋`--acceptance "$REPORT/acceptance.json" --output "$REPORT/output" --batch-size 64 --max-seconds 5400 --max-memory-mib 7168`。本Cは同root/acceptance＋`--candidate-root "$REPORT/output" --output "$REPORT/checker-result.json" --max-seconds 10800 --max-memory-mib 7168 --producer-max-seconds 5400 --producer-max-memory-mib 7168`。外側P6000秒/C11400秒、job330分。TERM/kill、全stdout/stderr/exit/start/finish、実command/source/runtime、累積RSS/I/O/秒を保存し、予測を実測へ置換しない。

全54433弦＋2aux/full failed/full residual、全選択candidateの六相、全保存ancestry/Ref/零係数/挿入順、全B/dotは通常P/C自身が処理する。WFは保存receiptを認証して完成gateへ結び、その数値経路を省略しない。P後の全outputをC前に固定し、C後の全files/dirs/hidden診断不変と、全15親/source/raw/acceptance/driver/WFのbefore/middle/after不変を要求する。fixtureの全三比較、全ZIP再読、raw treeの最終完全一致も独立flagで必須にした。

candidateは本Pの完成PASS、本Cの全比較PASS/partial=false/durable_tail=null、全HEAD/result/final/selection/coverageの実結合、全試験と全保全の成功に限る。selected/processed/dependent/accepted/skippedを全Cへ結び、rank=1450+accepted、generation=8155+acceptedとする。partial/UNKNOWN/FAILを完成candidateにしない。全候補scalar/omega/修理項と全phase測定をcoverageへ保存する。candidate/diagnosticsは同REPORTをuploadし、ZIP digest差を内容差と呼ばない。全REPORT実inventoryは新inventory自身/run receiptを除いて保存し、そのpinもrun receiptへ記載する。

1031指摘のrun receiptを一字段修理した。`same_word_adapter_for_batch_rows` は正常final gateからresultを受け取れない場合None、受け取れた場合 `result['positive_readout']`。Linearのみ `NEW_BATCH_SAME_WORD_ADAPTER_PENDING`、他の完成terminalは `NOT_APPLICABLE` という既存final gate/currentの型に一致し、無条件pendingを出さない。旧WF v1は修理しない。

## F6. 保持TCBと未実行

二保持kernelの共有TCBとF-fo-1/F-flb-1の限定（root返信163 F8.89・裁定2173）を継承する。本WFはその独立性の遡及閉鎖を主張しない。rho2はDERIVED、新lambda oracle=null、grade2の二字段NOT_DECIDED、full_A0=false、verified=falseを保持する。Linearになっても正語の新batch adapterは別の未完条件である。

本票はsource/workflowの静的完成票であり、新GHAのruntime/AST、metadata16回帰、新P/C各二群、本k64 P/C、全before-after/ZIP、実rank/terminal/測定値および工房CV9は未観測。ローカルPython/import/AST/数値/GAP/network/git/credential/追加agentを実行していない。新run id/commit shaはまだ存在するものとして記帳しない。公開・GHAはroot唯一brokerが独立監査票と全差分読了を合流させて行う。

AUDIT_1029_VERDICT: STATIC_WORKFLOW_COMPLETE_READY_FOR_ROOT_REVIEW; FROZEN_WF_166471_887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5; NEW_RUNTIME_METADATA16_P2_C2_AND_K64_PC_PRESERVATION_CV9_PENDING; VERIFIED_FALSE.
