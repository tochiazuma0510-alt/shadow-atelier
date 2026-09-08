# Task1126 — 既存 gap-run による C6 修理の先行 selftest 実行器

宛先: packet_bounds_audit。Luna/外側実装担当。1124は完了、1108正式handback待機と並行できる独立な小作業。新agent禁止。返信 sol/luna_reply_1126_r07_C_selftest_gap_runner_v1.md、最終行 TASK1126_VERDICT:。全新実装/票を %TEMP%/shadow-atelier-audit163/task1126/ に作る。現repo/source/WF/1124/1108/親/processへ変更しない。

目的は、正式親inventoryが未着でも、guardclosedのC6を --selftest で先行確認する実GHA経路を具体化すること。userはGHAの反復実行を包括認可済み、rootが単一Git/GHA broker。既存 .github/workflows/gap-run.yml を全文読み、その workflow_dispatch script/out_dir/timeout_min/with_pquot_packages=false を使う。workflow変更0。追加の人の承認待ちを勝手に作らない。最終全pin/静的別読/通知が揃えばrootが配置・発射する。

公開固定入力:
- Task1125 の新未実行C6 source: task1125/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py = 427740 B / a5c449721663940ed2155f90980eb7422999cbaa6af466512e95a0819cd02f58。相手private本文/差分を読まない。pinだけは全文hash可。root採択後に search/check_d972_r07_fixed_lambda_cycle_batch_v6.py へ配置予定。公開C依存pinは以前の1107/1110公開dependency票/元registryのうち公開metadataだけを使う。
- 公開CLI: python -B search/check_d972_r07_fixed_lambda_cycle_batch_v6.py --selftest --selftest-root <new isolated dir> --max-seconds 300 --max-memory-mib 7168。parent root/acceptance/candidate/output引数を渡さない。C selftest stdoutだけが正式結果、stderrには進捗/異常。mainはselftest枝でAcceptedInputsを呼ばず、formal inventory/P pinのNoneを必要としない。fullRunのNoneは保持。
- selftestは既四群後に第五群を呼ぶ。第五の拒否数8/実保持28file＋empty1と全群拒否[28,9,6,7,8]は元通り、第五production_interfaces_usedに artifact_identity が追加された公開変更がある。実helper全18role×artifact10字段の正対照が含まれる。出力exact schema/key/groupの最終公開票はC担当からroot経由で渡す。捏造せず、この公開後着だけを末尾gateの未着箇所として明示。

実装の限定範囲:
1. 新GAP入口 search/d972_r07_C6_artifact_identity_selftest_gha_v1.g と小さい独立外側実行器（必要な .py / .sh、名前を同stem v1で明示）をTEMPに提案する。既GAP driverのProcess/exit伝達の実例を静読し、GAPがRead失敗でもexit0になり得ることを踏まえ、実子exit/保存した終了JSON/最終markerを別々に残す。成功判定はrootの実receipt全読が必須。preambleは空、任意code注入を使わない。
2. scriptはchecked-out head/refを記録、C6全source427740/SHAを起動前後照合。公開依存も登録された全source pinへ接続し、現在repoで既存の親数学sourceや旧成果は上書きしない。Cをroot未採択の別sourceへ切替えない。
3. 既gap-runはGAPをsetupするがPython setup stepはない。この先行診断はrunner既存 python3 の実versionを記録し、新しい専用venvに元本走と同じ NumPy==2.5.1 をinstallする。実Pythonが本走の3.13.15と異なる場合は明示し、同環境の本走試験を済ませたと称さない。必要tool/version/pip失敗はFAILとして保存、実本走設定を変更しない。大きい親artifact/GitHub API/secretは読み込まない。
4. C実subprocessにtimeout360秒、selftest内300秒/RSS7168。artifact下の新isolatedrootだけを書込み、stdout/stderr raw、exitcode、実argv、UTC・elapsed、実Python/NumPy、元/後C/依存pins、run id/attempt/head、実最終resultを保存。UNKNOWN_RESOURCE/nonzero/未形成/不正JSONをPASSにしない。wholefixture files/dirs/emptydirを全EOF hashしてmetadata一覧と圧縮容器へ保存し、rootが後で照合できるようにする。fullA0/candidate/cross_checked/verifiedはfalse。
5. artifact out_dir は ci/out/task1126、workflow timeout_min は20以内、optional pquot package buildはfalse。GAP自体のsetup時間とC selftest時間を混ぜない。本走P/C/driver/WFのgate、fullreception、既registryへ追加の完了を代用しない。
6. 全proposal source/差分無しの既workflowpin/公開入力pin/全script consumerとresult格納/失敗保存/timeout/end markerの静読票、全材料manifestを納品。repo配置前の想定再現CLIと外側source全pinを具体化する。GHA発射はrootが行うまで未実施と記す。

ローカルsource/Python/GAP/AST/import/compile/selftest実行禁止。PowerShell/.NET raw/JSON/bytes/SHA編集のみ。.ps1を作る場合ASCII。Git/GHA/network/credential/secret環境、既process操作は禁止。相手C/P数学private不読。正式1112終了が届けば1108 bindingを優先してrootへ知らせる。
