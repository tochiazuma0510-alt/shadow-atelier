# Task1029 — 固定lambda k64 batch v2 初回 GHA

宛先: 既存 packet_checker。1027 の新 C v2 と作者票を凍結したまま、新 WF の受付・実行・全保存を用意する。P 私的1023/1026票・新 P 本文/helperを読まない。
変更可は新 .github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml と新 sol/luna_reply_1029_r07_fixed_lambda_k64_workflow_v2.md だけ。旧全 WF/source/票は不変。ローカル Python/import/AST/数値/GAP/network/git/credential/追加 agent は禁止。root だけが git/GHA broker。未確定 P pin を推定せず、確定前の WF は非凍結とする。

## 固定契約と旧基点

公開1025全文を最優先とし、旧1009と共通994/997（R1優先）/1000/1001/1002/1003/1004/1011の保持部分を継承する。旧 WF v1 全文（142206 B / SHA256 8596ab900175c69cc38085c0caa0455a75dd74eb251e7eb2870a05e030490c73 / LF1993）を基点に新 v2 の限定差分を作る。旧 run34004423047/1 の算術結果や自己試験を再走して埋めない。
新 source は search/d972_r07_fixed_lambda_cycle_batch_v2.py と search/check_d972_r07_fixed_lambda_cycle_batch_v2.py。外側 prefix は d972.r07.fixed-lambda-cycle-batch.v2。C 最終 pin は 177544 B / 4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90 / LF2675。P 最終 pin は root が別途公開する。
batch_size=64、max_batches=1、refill=false、selection_policy=CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX、partial_policy=PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY。整数型は bool/float/string を拒否する。初回 fresh 一回・自動 resume/再試行なし、dispatch で k/cap/親/制限を変更できる入口を増やさない。
親は run33990567016/1、旧64/rank1450/gen8155、head c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、ZIP304642285 B / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792。元14＋continuationの15親全tuple/ZIP/全file/dir/history/実旧C64を保持する。別 k32/control96 の rank1482 や positive 第16親を混ぜない。rho2 は DERIVED のまま。
保持 Python19＋新 P/C2＝Python21、raw3 を足す全24file を公開1002と実新pinへ結ぶ。旧batch v1を新source closureへ追加しない。Python3.13.15/NumPy2.5.1の実完全文字列・ソース/raw/driver/WF・exact firing HEAD を旧どおり認証する。

## shell・受付・新二群

push marker [r07-fixed-lambda-cycle-batch-v2-run]、workflow_dispatch、既定作業branch限定、read-only permissions、checkout credentials非永続を継承する。REPORT は RUNNER_TEMP/fixed-lambda-batch-v2 とし、作成前に不存在/非symlinkを確認して fresh root にする。旧 artifact 名・旧親schema・旧inner phase schema・nonce32hex/int32/歴史before32等は改名しない。
元 WF の全 live API tuple、全 ZIP bytes/SHA、safe extraction の全entry/EOF/path/duplicate/casefold/type、全源と全親の before/middle/after、実旧64 acceptance、portable hash と host込み hash の区別を保持する。未知の live pin や runtime の変更を自動承認しない。source/intake中断でも取得済み全診断を always に残す。
旧 metadata 16 cases は新 REPORT/新登録/新source の受付結合を確かめるため今回も実行する。新しい数学16試験とは呼ばず、変更された実 metadata helper に接続した回帰受付として、件数と旧数学成功suite再走0を receipt に明記する。新数学試験は1025の P/C 各二群だけ。
P/C 新 --selftest は --selftest-root を必須にする。外側 command は REPORT/selftest-fixtures/P と /C の絶対 path を各一回だけ渡す。既存 regular parent を外側で作るが P/C root 自体は CLI が fresh に作る。自系 source と root 引数以外の数学親/acceptance/actual output を渡さない。P の既存 batch-size 指定は64、Cへ不要な --batch-size を増やさない。
各 selftest 内側300秒/7168 MiB、外側360秒。名前と順は k64-version-registration-and-types、k64-full-roster-cutoff-and-restoration。sealed top は body exact status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verified、tests は exact二要素で各 {name,status,rejected_cases}。status PASS、非空str/list、普通整数 old_success_suites=0、actual_anchor_arithmetic_replayed=false、三 assurance false を実全 stdout/receiptへ結ぶ。架空の P 別名/source/root 字段を追加しない。旧三群を新dispatcherから呼ばない。
実 root は command/start/result と REPORT の全 inventory に結び、作成された全正負fixture・失敗ledger・stderr・hidden file・empty dirを終了後も保持する。pre-P の全 control inventory に両 fixture tree を含め、P/C 後も全既存 fixture bytes/dirs 不変を要求する。新fixtureを cleanup や whitelist で削らない。未知の private layout を推定しない。

## 本 P/C と完成境界

本 P は5400秒/7168 MiB、外側6000秒。本 C は10800秒/7168 MiB、外側11400秒、job330分を保持する。TERM/killと全 stdout/stderr/exit/start/finish/runtime/source/実 command を保存する。C の producer-max-seconds=5400/producer-max-memory-mib=7168 を受付へ結ぶ。
全54433弦＋2aux/full failed/full residual、全候補六相、全保存 ancestry/Ref/零係数/挿入順、full B/dotを再読する通常 source の仕事を WF が省略・代用しない。候補 ordinal/local row 0..63、private sequence 上限387を新sourceと整合させる。P結果 selected/processed/dependent/accepted/skipped の整合を実全 C と結び、rank=1450+accepted、generation=8155+accepted。accepted64/rank1514を期待値にしない。
P全outputをC前に完全保存し、C後の全bytes/dirs不変、全親/source/raw/受付/driverの全不変を要求する。partial/UNKNOWN/FAILをcandidateにせず、全試験・本P完成・本C全比較/partial=false・全HEAD/result/manifest/selection/coverageとbefore-afterの実結合だけでcandidateをuploadする。candidateとalways diagnosticsが同じREPORTならそのまま記帳し、ZIP digest差を内容差としない。
新lambda oracle=null、grade2二字段NOT_DECIDED、full_A0=false、verified=false。Linearだけ NEW_BATCH_SAME_WORD_ADAPTER_PENDING、その他 NOT_APPLICABLE。P/C既存 candidate/cross_checked の限定型を保持し、工房CV-9正式受理や full A0 と混同しない。二保持kernelの共有TCB/F-fo-1/F-flb-1の限定は163 F8.89/2173を継承する。
実 P/C 秒・候補六相の秒・累積 RSS/I/O・全保存量は実 receipt から記帳し、旧94%をP全の割合にしない。全phase・full failed/selected roster・各candidateのscalar/omega/全修理項・全rusageを保存する。

## 静的閉包と返信

新全WF/旧差分・通常gate・失敗保存・新二群型・実CLI・全親/全24source pins・新fixture全inventoryを全文静的に読む。作者票へ F#、全bytes/SHA/LF/CR/BOM/末尾空白と未実行を残し、最終行 AUDIT_1029_VERDICT: とする。rootと独立監査が新差分を全読了するまでは公開・GHAなし。P pinの通知を待つ間も独立に準備を進めてよい。
