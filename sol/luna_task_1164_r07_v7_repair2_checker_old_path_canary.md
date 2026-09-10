# Task1164 — C旧path負例の実変異を復旧しrepair-v2へ

宛先: Helmholtz / c6_final_binding、Luna。1163のpublic exportを保存し、この実失敗修理を優先。指定返信 `sol/luna_reply_1164_r07_v7_repair2_checker_old_path_canary.md`、最終行 `AUDIT_1164_VERDICT:`。新材料 `%TEMP%/shadow-atelier-audit163/task1164/`。既存source・1149/1159/1160/1163・旧artifactは上書き禁止。新agent/Git/GHA/network/credential、数学source実行/import/AST/compile/selftestは禁止。自身のCだけraw/textで読み、P source/privateは読まない。

実run34518126217/1/head2f8ad063da52da90ed74fd230fb122f96ad79ec7は19:11:56Z failure。metadata11/P-selftest12 success、C-selftest13 failure、本P14/C16 skipped。artifact10168815742、25041369 B/baf33f0ee8033902bbef976262c43385a88a651c02974361e0004df2feb2e3dfをrootがAPI digest一致で取得した。`run34518126217-reception-v1/checker-selftest-stderr.log`287 B/2d437aa4a935ffc21501e00546fda2a02c5c611466fa3fc3feebdb6fc86da524は `ValueError:cycle_batch:missing_required_rejection:old-producer-path`。exit-code.txt2 B/4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 = 1。あなたの独立静的初見とroot L6016–6023/rejected全文読みに一致。

基準は実repair-v1 C525657 B/ccd572ee1f0cd2504521526fbfbf830a95197d99044870cf19c7a6cc0ffb67a7。k128_registration_canary L6021の `.replace("_v7.py", "_v6.py")` はrepair_v1名でno-opとなる。この**一assignmentのみ**を、sideから固定の旧v6 P/C basenameを構成する式へ修理する。例: `"search/" + ("check_" if side == "checker" else "") + "d972_r07_fixed_lambda_cycle_batch_v6.py"`。current名のsuffix置換に依存させない。正対照→異なる旧v6 path→既存check_executable_pathsで拒否、両sideそれぞれの実文字列と型・入出力位置をraw/JSONで示す。negative数・case名・元6群の範囲を変えない。新テスト追加やchecker predicate変更は不要。

新配置identity:

- P `search/d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py`
- C `search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py`
- WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v7-repair-v2.yml`
- name `d972-r07-fixed-lambda-cycle-batch-v7-repair-v2-envelope-v1`
- marker `[r07-fixed-lambda-cycle-batch-v7-repair-v2-envelope-v1-run]`

PRODUCER_FILE/CHECKER_FILE/CHECKER_WORKFLOWを上記へ、CURRENT_PRODUCER_REGISTRATIONをNoneにしてroot actual P D3だけを待つ有限binderを新規版で用意する。1159 binderの全source・入力契約・CreateNew/正逆原理を再利用し、変更は新unbound source/pin/identityの具体束縛だけ。Pは1165でC_FILE/WF identityのみ変えるため、既存P機械結果は新実行の結果に読み替えない。

納品: 全194連続領域の全EOF正逆、prefixとk128_registration_canary以外のraw保持、C4登録24/一意21の元raw/境界保持、public source/retention/identity overlay、全selftest consumerのidentity依存箇所(特にv7/v6 suffix・old-producer/checker-path)を有限に全列挙、有限opaque binderと契約。6群のcase意味を新identityの実negativeへ再束縛する。以前の「全selftest raw同一だから新identityでも同義」はこの負例の前提を落としていたと訂正する。実binder/receiver実行はroot別読後、C数学実行はGHAのみ。論理v7・19親・1962/8667・k128/no-refill/caps/C4 raw/著者分離/数学宇宙は保持。
