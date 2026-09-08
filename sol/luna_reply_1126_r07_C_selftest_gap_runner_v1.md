# Task1126 — C6 artifact identity selftest の GHA 外側器案

F0. Luna/外側作者として指定 TEMP/task1126 だけへ新4資料を作り、既 gap-run.yml 全文と既 GAP Process の選択境界を静読した。C6/依存は公開登録とopaque bytes/SHAだけで結合し、相手private本文・fixtureは読んでいない。Python/GAP/import/AST/compile/selftest/数学・Git/GHA/network/credential・既process操作は0。PowerShell/.NETによるraw/JSON/EOF台帳生成だけを行った。自身の作者点検を別人の独立監査とは呼ばない。

F1. 最終新4資料は `%TEMP%/shadow-atelier-audit163/task1126/search/` と、同rawの `review-snapshot-v2/` に固定。repo配置はroot担当、現repoのsource/WFは未変更。共通stemは `d972_r07_C6_artifact_identity_selftest_gha_v1`。

| 提案repo path | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_C6_artifact_identity_selftest_gha_v1.g | 924 | e469718090908245d31a2e9e686664e1764d43e299e20a3240d4b390c7848a76 |
| search/d972_r07_C6_artifact_identity_selftest_gha_v1.sh | 2064 | 766ef48e25298154ea7691c1e3714ef5415242adf1fd0bc277bdabfe32a4e77d |
| search/d972_r07_C6_artifact_identity_selftest_gha_v1.py | 25914 | 1d5d45debb1708f79af5c6ad3cb72a16a2282e641fbcd7735b1dee9b517e12e7 |
| search/d972_r07_C6_artifact_identity_selftest_gha_v1.json | 37389 | 5b3163083d8e2e684a3bc7f82900c1179827f343202d75296360949e864deead |

F2. 既 `.github/workflows/gap-run.yml` は 13309 B / 0c2ba9089d7e43d9d34d43afa039618a354307037ddf9ea332535e43a70cecae と不変。root報告のworkflow idは322329646。script/out_dir入力、Ubuntu/GAP4.16.0、空preamble、with_pquot_packages=false、常時 `gap-run-out` uploadを使う。このstemは旧fast-resumeの親取得条件に該当しない。GAPは固定shell bytes/SHAを照合してProcess、shellは固定py/JSONの全pinを照合してpython3を呼ぶ。GAP Read失敗でOS exit0になり得るため、GAP job successだけは成功根拠にしない。

F3. Cの唯一登録sourceは `search/check_d972_r07_fixed_lambda_cycle_batch_v6.py` =427740 B / a5c449721663940ed2155f90980eb7422999cbaa6af466512e95a0819cd02f58。公開依存10本は既1108 driver L974のC_DEPSから原型で登録し、C計11本の実raw pinをここでも照合した。実GHAではC11＋旧WFの12本を起動前・環境構築後C直前・終了後に全EOF照合し、外側4本も前後同一を要求。起動時の全16資料はopaque copyとしてartifactへ保存する。採択wire25393 B / e59e87cb9b5fbe9e399d46619bd9f37206d6afad6cd9a1018060c1002a89d071は登録JSON内へ全typed同値で収録。新Cの2 Noneおよび通常親入場のguardは変更しない。

F4. 公開S03とroot明確化に従い、実fixture/専用venvはfreshな `RUNNER_TEMP/task1126-<UUID>/` に置きrepoとdisjointにする。taskの「artifact下」は保存先の意図であり、`ci/out/task1126`をCのselftest-rootには渡さない。Cには未作成のfixture pathを渡す。旧親root/受領中processへアクセスしない。child環境は必要なPATH/locale/専用HOME/TEMP/RUNNER_TEMP/Python flagsのみ、秘密環境やGitHub APIは渡さない。

F5. runner既存python3の実版を保存し、新venvへNumPy==2.5.1を導入、venv実版/NumPyも別probeで照合する。Python3.13.15との差は実値で記帳し、同環境本走を称さない。venv60秒/pip180秒/probe30秒、Cには公開 `--selftest --selftest-root <fresh absolute root> --max-seconds 300 --max-memory-mib 7168` のみ。実C外側timeout360秒、超過時はこの新子groupのみkillし実returncodeを待つ。各start/resultにargv/cwd/UTC/elapsed/実exit/error/stdout/stderr全pinを保存。GAP setup時間はC時間・外側Python時間へ混入しない。tool/pip/版不一致・非零・timeout・不正JSON・UNKNOWN_RESOURCEはFAIL。

F6. C stdoutの .v6.selftest exact11/seal、exact3の5群順・拒否数[28,9,6,7,8]、topの全43 production_interfaces_usedを完全一致で照合。artifact_identityはtopの追加名。第五群は全28file/全implicit dir/empty1、8件のexact4 rejectionと実 `cycle_batch:` prefix＋裸labelを照合する。既四群の個別拒否文字列は公開count/非空文字列/重複なしを受け、第五だけ公開8実名の順序まで固定する。18役×10字段の正対照は、root採択のC通常loop＋pinned source＋実sealed PASSへの依存である。stdoutに独立の実測18行/countが新設されたとはしない。positive.jsonと実全fixtureを保存し、架空の測定字段・全1834親入場・全481算術再生を作らない。

F7. C失敗時にも、実在するpartial fixtureの全entryを列挙して全file EOF/SHA、全dir/emptydirを保存。全raw copy後に元/copy同値、全dir entryを含むZIP生成後に全entry EOF/SHA/通常種別を読み戻し、元/copyを再読する。hiddenを除外せず、symlink/nonregularを黙って飛ばさない。uploadがloose hidden/emptyを省く場合もinner ZIPに全収録する。ZIP CRCは標準zipfileの読戻し、独立CRC実装の主張はfalse。partial archiveのPASSはselftest成功に昇格しない。未形成はNOT_CREATED、保存不成立はFAIL。自分の作ったfixtureを消すcleanupは加えていない。

F8. 成功候補でも `selftest-end.json` の PASS_SELFTEST_ONLY/全errors0、実C exit0/no-timeout、全source前後一致、public gate、全fixture保存、shell-endの実returncode、OUTER/SHELL/GAP各terminal markerをrootが全実受領で結ぶ。終了JSON未形成・GAP marker欠品を未来のPASSにしない。fullA0/candidate/cross_checked/verifiedは全false。通常P/Cのgate、正式typed受領、inventory5、1108最終bindingの代用ではない。現在GHA run/head/artifact tupleは未形成で、runtime結果は未観測。

F9. Python全482行/18関数・preamble/最終guardを含む20 EOF区間と全4資料の再連結を `.NET` で閉鎖。全関数consumer10組と134行の角括弧字句母集団（construct/slice/output/dynamic読みを含み、134独立readerとはしない）を static-consumer-and-EOF-audit-v1.json =116297 B / 617ac515fea5cbe0636bfee539c109cb61ef1928933770de7e79d5497e03d470 に保存した。選択した旧Process境界は同票へraw/全file pin付きで引用、長い旧GAP実装全体の読了は主張しない。初稿4rawはreview-snapshot-v1へ保持し、shellの書込/列挙失敗停止の修理とGAP2pin追随はbootstrap-refinement-full-delta-v1.jsonへ全before/afterで保存。Python/公開型の本文差は0。

F10. root-dispatch-and-final-snapshot-v1.json =6584 B / aa66b4c7a3ca568258f0c3b6e1936c0e7caecca56ead4cad7f293feb37a4c51b に配置4pin・既WF・C pin・回収順を固定。発射例（rootだけが採択branchを代入）: `gh workflow run 322329646 --ref <ROOT_ADOPTED_BRANCH> -f script=search/d972_r07_C6_artifact_identity_selftest_gha_v1.g -f preamble= -f out_dir=ci/out/task1126 -f timeout_min=20 -f with_pquot_packages=false`。全納品目録はtask1126/final-material-manifest-v1.json。正式1112 handbackが届けば1108限定bindingを優先する。

TASK1126_VERDICT: AUTHOR_STATIC_PUBLIC_SELFTEST_RUNNER_PROPOSAL_PASS_RUNTIME_PENDING
