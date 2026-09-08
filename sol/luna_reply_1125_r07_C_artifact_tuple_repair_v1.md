# Task1125 — C6 artifact tuple の限定修理

**F1. 結論と固定境界。** 第三親 `batch-parent-v5` の内部登録を、既17親と同じ7要素 `(run, head, id, name, bytes, bare_digest, workflow_basename)` へ修理した新 C6 草案を凍結した。通常 `artifact_identity` 本体を変更せず、第五群にその実 helper の全18親・各10字段の公開値正対照を接続した。これは静的な source 修理の完了であり、局所実行・自己試験通過・GHA 結果は未観測。正式 inventory と最終 P6 の二つの `None` は閉鎖を保持する。旧1110/1123資料・親は変更しておらず、他系 private 本文は読んでいない。

根拠指示は `sol/luna_task_1125_r07_C_artifact_tuple_repair_v1.md`（SHA256 `6ebe7b2a5a3b44a2427683b4cb2ead7fcef261dad278d0cd16d9a7748af987bf`）。先行する別所見 `task1123/static-artifact-identity-arity-finding-v1.json` は 19,814 B / `3a2b8f2b3103c57048de8524cbee461377c648ebc7d7fbe9a8f69d63fa44d829`。原 C259–262 の8要素、C637 の7変数 unpack、通常 C702 と native C1366/2019/2855 の全 caller を固定した。root が裁定した欠陥は「正式 binding 後、その helper に達した時の arity 不一致」であり、現在runの実失敗や実親不一致へ読み替えない。

**F2. 新旧 source と全差分。** 以下の `task*` 相対材料の基準は `%TEMP%/shadow-atelier-audit163/`。

| 対象 | bytes | SHA256 |
|---|---:|---|
| 旧 `task1110/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py` | 419541 | `3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff` |
| 新 `task1125/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py` | 427740 | `a5c449721663940ed2155f90980eb7422999cbaa6af466512e95a0819cd02f58` |
| `task1125/whole-registered-raw-diff-v1.txt` | 9311 | `0b39817bf2297391e52766c22d8f72625743d11178695ae8cdd45df173137b7d` |
| `task1125/full-raw-and-EOF-delta-v1.json` | 246300 | `800518112a08a4aee3790980d276bbfb10c409eb9aff911b76b62aa0506fb0e6` |

新 source は LF5721、CR0、ASCII、UTF-8 BOMなし、最終LFあり、末尾空白行0。連続置換は三つだけ。D01 は旧 offset21309/327 B → 新21309/302 B の第三tuple。D02 は旧406352/0 B → 新406327/8203 B の正対照挿入。D03 は旧412722/107 B → 新420900/128 B の `production_interfaces_used` 一文字列追加。全165区間の両側 EOF、間隙、末尾、全raw forward/reverse を比較し、162区間不変、変更は PREAMBLE / third_batch_parent_admission_canary / selftest の3区間のみとした。全旧 production helper、数値核、旧17親定義、旧4 loader＋保持20登録（重複を除く21 body）の raw は不変。区間数の変更はない。

**F3. 全18親の独立公開値結合。** 事前登録後に root の `root-v6-all18-parent-GHA-api-preflight-2230-v1.json` 全文を読了した（61,944 B / `2d8ff89346629d937f9a2b042dab10895a5f51898ba67113f7e255dc92ee9e38`）。これはAPI時点の登録照合であり、payload全読や正式 inventory の代わりではない。

`task1125/all18-static-literal-to-public-artifact-join-v1.json`（196,485 B / `a39df775f5b06330465f1e5aaa1963243585762a288f260dc612dd9ea79bbc58`）に、全18の元/新定義raw範囲、5件の固定loop外式、展開7tuple、helperの紙上投影、独立API期待10字段、埋込期待辞書、全180型付き比較を保存した。静的字句抽出の範囲は登録した文字列/整数literalと当該固定loopのみ。Pythonの評価・AST・一般source parserを使っていない。旧17は元から7、新第三も7になり、公開10字段はすべて一致する。整数は ordinary integer、残りは文字列として結んだ。

第三親の公開10字段は run34161493396 / attempt1 / head `a5b456a973f8a917f3af386d327061a02a0cf900` / workflow `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml` / id10034053256 / name `d972-r07-fixed-lambda-cycle-batch-v5-candidate-34161493396-1` / bytes384961441 / sha256 `sha256:72e19a87e3a4ca06daa3b1b9dc8a16e76778e6ce1d6bd3a57b25acea363602db` / repository_id1312092366 / conclusion `success`。既 `prepare` と4 `block-*` の conclusion=`failure` もそのまま維持する。

**F4. 新正対照の到達と停止。** 公開 `task1125/public-selftest-artifact-identity-contract-v1.json`（25,393 B / `e59e87cb9b5fbe9e399d46619bd9f37206d6afad6cd9a1018060c1002a89d071`）が exact 出力型と全call-flowの正本。標準CLIは `--selftest --selftest-root <fresh-absolute-TEMP-or-RUNNER_TEMP-root> --max-seconds 300 --max-memory-mib 7168`。個別第五群だけを選択する新flagは設けない。

新 C5685–5690 は parent/acceptance/candidate/output 引数なしを要求し、fresh root の通常guard（C4780–4796）を通って `selftest` へ進む。最初の既四群が正常完了した後、C5608 が第五群を呼ぶ。C5495–5497 の最初の既存pairは正例受理→元の単独変異→元の exact rejection をそのまま実施する。その保存 `parent1834/omit-v4-from-native17-projection/positive.json` を C5522–5524 の CandidateFiles.json と通常 projection helper で再読し、C5525–5527 の全18 role loopで **production artifact_identity の返値全体**を独立公開期待辞書へ same_json で比較する。role順も C5521 で一致を要求し、C5528 は全当該fixture file/hash保全を要求する。期待値は FIXED_ARTIFACTS から作らず、公開API登録をliteralで埋め込む。

新比較labelは `c6_parent1834_public_artifact_role_order` と `c6_parent1834_registered_artifact_identity:<role>`。失敗時は既requireの `cycle_batch:` prefix を伴う。これらは追加した拒否ケース名ではない。既8負対照を経て第五群が返り、最後の全5群/count guardと document封印に達した場合のみ、成功selftest stdoutが形成される。途中の例外/資源停止は既 main の FAIL/UNKNOWN_RESOURCE checker-result と exit1/3であり、成功selftestと区別する。

標準経路は AcceptedInputs を呼ばず、二つの正式 `None` を要求しない。一方、登録された repository の checker path への配置、保持source pin/依存runtime、fresh root、既四群の完了は前件である。孤立TEMP sourceだけで実行可能という主張や、資源上限内の完了保証ではない。C264/265 の `None` と通常C686–687の入場guardは不変。

**F5. 公開 stdout の exact 型。** 以下は未実行の**成功時契約**であり、実PASS票ではない。schema は `d972.r07.fixed-lambda-cycle-batch.v6.selftest`。top keys は次の11個だけ。

```text
schema, sha256, status, tests, fixture_scope, production_interfaces_used,
old_success_suites, actual_anchor_arithmetic_replayed,
candidate, cross_checked, verified
```

`sha256` は unsigned document のcanonical bytesに対する bare hex64 の inner seal。stdout全file SHAとは別。`status` は文字列PASS、`fixture_scope` は非空文字列、`old_success_suites` は普通整数0、`actual_anchor_arithmetic_replayed/candidate/cross_checked/verified` は厳密Boolean false。tests は次の順の5 dictで、各exact keysは `name/status/rejected_cases`、statusはPASS、rejected_casesは既ケース名の順序付き文字列配列。

| name | rejected_cases の件数 |
|---|---:|
| k128-version-registration-and-types | 28 |
| k128-full-roster-cutoff-and-restoration | 9 |
| batch-parent1578-admission-and-projection | 6 |
| batch-parent1706-two-layer-admission | 7 |
| batch-parent1834-three-layer-admission | 8 |

`production_interfaces_used` は第五groupの内部字段ではなくtop字段。以下が全43件のexact順序であり、先頭の artifact_identity だけを追加した。

```json
[
    "artifact_identity",
    "check_third_native_parent_projection",
    "check_third_row_namespace",
    "check_third_ancestry_records",
    "check_third_previous_target",
    "check_third_selection_lambda_contract",
    "check_third_inventory_arrays",
    "check_third_unobserved_oracle",
    "check_registration",
    "check_acceptance_header",
    "check_executable_paths",
    "compare_root_records",
    "phase_at_sequence",
    "row_source",
    "compare_phase",
    "ProgressAudit",
    "invocation_records",
    "registered_basenames",
    "select_all_residuals",
    "witness_records",
    "batch_tree_payloads",
    "selection_record",
    "compare_selection_publication",
    "compare_candidate_roster",
    "CandidateFiles",
    "prepare_selftest_root",
    "BatchReductionState.reduce",
    "BatchReductionState.advance",
    "reduction_payloads",
    "accepted_row_record",
    "candidate_decision_record",
    "compare_candidate_publication",
    "check_parent_roles",
    "check_v4_acceptance_header",
    "check_batch_parent_header",
    "check_batch_current_projection",
    "check_saved_batch_target",
    "check_next_parent_roles",
    "check_next_row_namespace",
    "check_next_ancestry_shape",
    "check_next_ancestry_records",
    "check_next_previous_target",
    "check_next_fixed_local_names"
]
```

既第一群28、全五群の拒否名/件数、第五8目的label、正負payload生成body、rejection exact4字段、zero rosterは不変。第五の28 file＋明示empty directory1と全暗黙親directoryは継承し、追加file/dir/group/rejection/ledger字段は0。正対照は既存fixtureだけを読む。旧dependent陰性が expected-file size/hash gate で止まる射程も変えず、semantic outcome比較へ到達したとはしない。自己source pinを含む他の既fixtureは新sourceの実pinへ当然結び直されるので、過去runとの全fixture byte同一を主張しない。

**F6. 公開consumerへの引渡し。** `task1125/public-opaque-current-ranges-v1.json` は 146,590 B / `bd744394ef0f17d90b3ba3ad57525cceb2406b132916548d6a3c9a3afc957396`、`retained24-current-range-binding-v1.json` は 46,579 B / `adb5610a661c941331177650610c4e5a50329fd8d139337c5b4d268af3e22ca9`。全165新offset/bytes/hash、保持24のoffset移動と同一raw hashを公開metadataで渡す。必要な外側差分は新C全pin/registry範囲とtop interface配列43件への結合。公刊wire keyや既fixture rosterを変更しない。WF/driverは本便では編集していない。後の正式bindingの基点を新task1125 sourceへ切り替える案はroot採択に委ねる。Task1123の62-reader調査と元419541 pinはそのまま保護する。

**F7. 最終保存と限界。** `task1125/final-author-static-completion-v1.json`（28,801 B / `4c54ffc4ff150cf587ab59d302a5724928b626e71ce96360aee4407bf53ab3cf`）に全原入力の再pin、通常/helper/既群の不変raw、第五から挿入だけを除いた完全一致、2 None、EOLを記帳した。`task1125/final-material-manifest-v1.json` は 3,780 B / `8663a97d8e0721248c4806d4bb4a8215618e3e1f9f41a659dcd67b079ec5b75f`。自己目録とこの返信を除く全12材料/1,141,143 B、directoryはsearchのみ。全原票と新source/材料をこのpinで凍結する。

PowerShell/.NETによる静的bytes/型付きJSON比較だけを行った。途中の metadata側探索範囲とculture依存BOM判定の不適切な試行は、最終票へ対象範囲限定と実3byte判定の訂正を記録した。いずれもC sourceを実行/変更する診断ではない。Python/AST/import/compile/自己試験/数学/親変更/Git/GHA/network/credential/private P読取は0。rootの先行GHA実通過はPENDINGで、正式1834/8539の格付けや元の費用見通しを昇格させない。本修理をcold-storage/1123設計全体の新たなv6待ち条件へ拡大しない。

TASK1125_VERDICT: LIMITED_ARTIFACT_TUPLE_REPAIR_STATIC_COMPLETE_GUARD_CLOSED_RUNTIME_PENDING
