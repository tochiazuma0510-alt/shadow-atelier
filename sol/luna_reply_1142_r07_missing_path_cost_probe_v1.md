# Task1142 返信 — missing-path context の限定実測

F1. **この固定16値では退行なし（NO）。** A=原provider版、B=現attributes版、C=原Test-Pathを保ちpresent-node属性取得だけをfresh GetAttributesへ替えた一箇所候補。2pass・96callを一度で完了し、全96件SUCCESS、例外0、出力0。missing-contextのBは両passともAよりwallが短かったため、Cを修理案として提案しない。現在receiver、PID13240/watcher10572、P1138、親の内容・directoryは変更していない。

F2. 登録と実値

元sourceは `root-task1136-full-activation-v1.json`（10626 B / `663755f7470b186b006e7de004a61da6013b204e1b4d7a1f3ac392ce8cf1d925`）のruntime_filesから特定し、basenameから内容を推測していない。登録sourceはtask1136の `root-review-receiver-v5-directory-stability-cost-v5.ps1`、527244 B / `d4ca12668c334c4668f02f4aae795ab85fbd4c5d0ced9cee39d29d809a28199d`。現sourceはTask1142指定527401 B / `6a8e1a516365e2d32a0da232452ba0bbad8b15d05ad306087aefd25a61aaf7ec`と一致。

実fixture inventoryは916522 B / `ea3fd38116229ce7b8845e6876fd28f6effd8bae119715da37e4d16b399a6cfd`。files4790件からindex **0,1596,3192,4789**、directories2351件から **0,783,1566,2350** を保存順で選択した。全8名についてtaskRoot/nameとtaskRoot/selftest-fixtures/nameを登録。前者のleafは**0/8存在**、後者は**8/8存在**。各絶対綴り・全親鎖綴り・存在/不在節点数は名簿に保存し、再帰走査やfixture内容読取はしていない。

関連callは現LocalPath R138–146 → NoReparse、InventoryShape R234/R240のglobal taskRoot、RestoreFixtures R1898–1902のfixture-relative inventoryである。これらmetadata行のみを抽出した。全InventoryShapeは実行していない。

F3. 実測（秒、各セル8callのhelper内合計）

| helper / context | pass1 wall | pass1 CPU | pass2 wall | pass2 CPU |
| --- | ---: | ---: | ---: | ---: |
| A / taskRoot（leaf不在） | 0.1005182 | 0.093750 | 0.0497280 | 0.062500 |
| A / fixtureRoot（leaf存在） | 0.0822396 | 0.125000 | 0.0802423 | 0.093750 |
| B / taskRoot（leaf不在） | 0.0383351 | 0.078125 | 0.0197995 | 0.000000 |
| B / fixtureRoot（leaf存在） | 0.0208790 | 0.031250 | 0.0197057 | 0.015625 |
| C / taskRoot（leaf不在） | 0.0388867 | 0.015625 | 0.0348714 | 0.031250 |
| C / fixtureRoot（leaf存在） | 0.0458952 | 0.062500 | 0.0448219 | 0.062500 |

実行順はpass1 **A→B→C**、pass2 **C→B→A**。各helperはtaskRoot8名→fixtureRoot8名、各8名はfiles4点→directories4点の登録順。全96個別receiptと12個context receiptを即時CreateNew保存し、登録順・実path・全pinを保存bytesと照合した。表のみ表示桁を整理し、原値・native CPU tick・Stopwatch tick・receipt書込を含む外側context wall/CPUは原票に保持する。CPUはprocess全体の粗いnative計器であり、0差分を作業0とは解釈しない。事前の存在確認によるmetadata cache warmingと2pass限定も残る。

F4. 起動・終了の欠測

専用probe PID2340のnative startは **2026-09-09T15:45:44.1340240Z**。最初のA/taskRoot完了票は **15:45:44.8073899Z** に保存、全96callの完了票も保存された。子stderrは空。

ただし監督scriptはWaitForExit/Refresh後の終了票作成時、`ExitTime.ToUniversalTime()`でnull例外になりtool exit1。**子native exit時刻・exit code・全process CPUは未収録**で、完了票やscript末尾の予定exit0で代用していない。96call上限に達したため再実行0。欠測票を別保存した。この制約のある測定を、native終了票まで完備した成功runとは称しない。

F5. 原票pin（すべて `%TEMP%/shadow-atelier-audit163/task1142/`）

| ファイル | bytes / SHA256 |
| --- | --- |
| helper-A-NoReparse-v1.ps1 | 402 / `b88ee2e0da47263bbc4b7da9c490ca3acfe109ba85bf7509e2a975532d3f3ff8` |
| helper-B-NoReparse-v1.ps1 | 559 / `ab22c9de5a39d42b8d35940ea1a2a86aba4bc042e910b92f9911e5da2f314fcc` |
| helper-C-NoReparse-v1.ps1 | 386 / `02189b03ee2080b3f4791ee7d523d7a74f766a95141d5e49726c11e5aaebf9e3` |
| metadata-helper-source-registration-v1.json | 4481 / `85093dddd164a7683845446b90a141ea7373358fce6af367d79218f1ce9128e6` |
| fixed-eight-names-sixteen-context-paths-v1.json | 85591 / `bb0c8095f8142b803bf62180caa5ecb2e9b4095236b57508d864a965c0c1a55b` |
| missing-path-context-harness-v1.ps1 | 8672 / `78900b193f636d760c5ce35f0ebe97ad86bc5ac725e243aed3e843e0a06b3301` |
| bounded-probe-registration-v1.json | 13024 / `c81fd8dd14043d8255139ca3e77ecf3d60abcef0362fa9a78eb7a77698fe072a` |
| runtime-v1/completed-v1.json | 192705 / `a7a8cee19ed82ddda133847d1bca908a9ad5dcbf3c42c34a07a7f112e72f7c3a` |
| supervisor-native-exit-missing-observation-v1.json | 2066 / `876a0bb658219f9daf1ce9513012a57f56539626eda1b69539c7bcfc64fb05cc` |
| bounded-probe-result-and-material-audit-v1.json | 11686 / `56d8cc80de14e9b108c52a10701ae9cc51afc6193ac1d139a7cb2445f0db8c17` |

source/helper/名簿/harness/順序を全helper呼出前にpin登録した。Cの変更はA内の`(Get-Item -LiteralPath $probe -Force).Attributes`→`[IO.File]::GetAttributes($probe)`だけで、Test-Path・Need・reparse拒否・親遡行の残余bytesは保持。動作同値の全条件監査は本便の範囲外である。数学source実行/import/AST、C private本文読取、Git/GHA/network/credential、全親profile、追加controlは0。現在stackの場所・因果・全receipt ETAは主張しない。

TASK1142_VERDICT: NO_MISSING_PATH_REGRESSION_IN_REGISTERED_96_CALLS_NATIVE_EXIT_METADATA_MISSING
