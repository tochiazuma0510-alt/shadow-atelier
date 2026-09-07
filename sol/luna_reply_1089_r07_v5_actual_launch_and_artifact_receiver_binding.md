# Task1089 — 実 launch と承認2215の受領器中間結合

F1. Task1089全文を読了し、実launch/具体承認だけを結ぶguardclosed中間版を凍結した。新sourceは `%TEMP%/shadow-atelier-audit163/task1089/root-review-receiver-v5-run34148667863-launch-bound-guardclosed-v1.ps1` = **516900 B / 49601381a834c583071251288e7f9b94e9b1036b6f88e32262d1051a8dbee0e4**、LF4626 / CR0 / ASCII only / BOMなし / final LFあり。基点1088の516693 B / 5e51d5ab28459ae565a8ee61dd0ea1f6f7d0e1c579c8786f4c8277edf46a39b7を新task directoryへ全raw同一で保存した。既存1080/1083/1088/実親/source/WFは変更していない。以下のpinは全て本便の新metadata材料であり、受領器の実行結果ではない。

F2. L30に次のexact五字段を一行の `[pscustomobject]` として登録した。runは明示 `[long]`、attempt/workflow_idは普通Int32、head/workflowはstringで、実JSON読取型と既存消費側L4074–4081の型・字段へ対応する。bool/float/arrayを普通整数・文字列へ通す変更はない。

| 字段 | 実値 | 型 |
|---|---|---|
| run | 34148667863 | System.Int64 |
| attempt | 1 | System.Int32 |
| head | 3e7e1ccf1996dad15b9019de849cf61548c654d1 | System.String |
| workflow | .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml | System.String |
| workflow_id | 352449001 | System.Int32 |

根拠はroot保存live票 `v5-run34148667863-root-live-progress-v1.json` =2306 B / 3e820ac1a90aa40c4ab73a6296d1e7b938a4df6439c7ba76a3600f2050409d5d、およびhead API票 `v5-envelope-v2-head-runs-first-v1.json` =13879 B / bb41553c52080534a5c8c8748f234dddbe11670a0010d48ed1ff0c5f509d0df9。両票を全文読了・全SHA照合し、APIの唯一のrunに対して五字段をtyped比較した。保存liveの観測時刻2026-09-07T17:48:23.7515235Zでは本Pがin_progress、P/C exit・新selection・新rankはnullである。現時点の最新APIを当方で取得したという意味ではない。

F3. L31の `$taskExpectedApproval` は普通整数 **2215** とした。具体envelope承認 `provenance/rulings_2215_snapshot_20260908.md` =2393 B / e089796b0374d96b968ab7ae7748564439dc13cececaa231103c58b7625089caを全文読了した。配置後7path・同run確認の2216 =940 B / a326a438cb9ab3d646c564ae01fdd9085991b80606cf7ece5177a29b9f65851cも全文読了したが、2216を事前承認値へ代入していない。発射通知受領のexpress738 B / 0462bf81436c5c02ae35c83264e1c64c15b1d01dc66d6dfc171e2cab4243ff67も保存した。これらはrun完了や候補の格付けを示す値ではない。九つの公開根拠copyとtyped五字段の対応は `observed-launch-and-approval-reception-v1.json` =6328 B / ce9fa8be89c802229fa94659e746e1e667b3e65c1fddb8eea50c9d44034cf06aにまとめた。

F4. 全変更はL30/L31の二宣言と、L14/L28の未観測表示を正すheader comment二行、計四行だけである。+207 B、LF差0。L29 artifact=nullとL34 guard=falseは全raw不変。歴史v4の局所launch/承認/guardは変更せず、current用と混ぜない。全四行のbefore/afterを `launch-binding-full-four-line-diff-v1.txt` =1001 B / 63d8e6b3d44f1bd4474afd675bbae1c97ed381056c58e63f8de3e291b74cc688で全文読了した。変更登録票 `launch-binding-four-edits-v1.json` =1266 B / f910566da2887f305fdd08f928ad832d1c260b3e9edf3b8d4752cd7c4b172798にも同四行を保存した。

全EOF/逆復元票 `launch-binding-full-EOF-reverse-and-siblings-v1.json` =**215985 B / 1e536e69568ded52d430e03048d658364e5c22fe094086e412658329814f1f80**は、旧96→新96区間、変更PREAMBLE一つ、残る95区間の全raw同一を閉じている。追加/削除区間0、全EOF欠落/重複0、後続offsetは一律+207。四変更と五不変spanからのforward全bytes、および新rawから旧rawへのreverse全bytesが一致した。旧60関数、全一般helper、old main、二型修理、cost、全scope/serializerも全raw不変である。rootからも四行全文・全行forward/reverse・五sibling全bytesの独自照合完了を受領した（root票3577 B / 84ff1ced36f6436f1adc606ed30f28f5a945b0472ae350cf7e9329ae0e8a757d）。このroot票は当方の実行票へ読み替えない。

F5. 同じdirectoryに必要な五siblingを1088から全bytes同一でcopyし、新旧全file pinと全bytesを照合した。以下のfileは実行時siblingであり、公開根拠copy九件や全静的材料21件とは別のrosterである。

| sibling filename | bytes | SHA256 |
|---|---:|---|
| registered-producer-current-regions-v2.json | 267079 | b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9 |
| registered-producer-body-inheritance-v2.json | 17587 | 768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed |
| v4-run34120585268-registered-canonical-files-v1.json | 1931889 | ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5 |
| v4-run34120585268-registered-canonical-directories-v1.json | 200290 | f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64 |
| v4-run34120585268-final-parent-inventory-registration-v1.json | 7022 | 64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753 |

F6. 入口の九つの必須string引数を保持した。次表の既知pathは `%TEMP%/` 基準で、旧実acquisitionと保存契約へ結んだ。六つの既知入力の存在・leaf非reparse、旧ZIPの実sizeをmetadataで確認した。本便では旧ZIP全bodyの再hashを行っていない（rootは別に全実SHAの再一致を通知済み）。新REPORT/acquisition/receipt pathは未登録である。

| 引数 | 現登録pathまたは境界 |
|---|---|
| ArtifactRoot | 未登録。新candidateの正式全展開rootを後着handbackで指定 |
| AcquisitionReceipt | 未登録。新candidateのroot全取得票を後着で指定 |
| Old64Root | shadow-atelier-cegar-resume64-run33990567016-candidate-a1 |
| BatchParentRoot | shadow-atelier-fixed-lambda-batch-v3-run34023589045-candidate-a1 |
| BatchParentArchive | shadow-atelier-audit163/fixed-lambda-batch-v3-run34023589045-candidate-a1.zip |
| BatchParentV4Root | shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1 |
| BatchParentV4Archive | shadow-atelier-audit163/fixed-lambda-batch-v4-run34120585268-candidate-a1.zip |
| BatchParentV4AcquisitionReceipt | shadow-atelier-audit163/v4-run34120585268-root-acquisition-v1.json |
| ReceiptPath | 未登録。TEMP内の新規fileで、受領REPORT・旧三親・PSScriptRootの外側 |

旧v3取得票719 B / 18aeadb7b5388c21eff5a143645f600ef1ccd676ca829809ca38efefbe325337と、旧v4取得票720 B / c377a2ed0d38d45d53236a8d1952f95d5a20433863fc3d764efda04b4b0caf7cを公開入力として保存した。現在source/driver/WF/registryの公開pinは1088の最終値から不変で、旧archiveや新cacheを受理条件へ足していない。

F7. 旧v3の認証済み空directory復元票4595 B / 86b588eb3feaee2034235f8958e074d006f6926b4666cc119866cea4b242aaf6は、11437 fileを保持し3439→3475 directory、復元36件を記録している。旧v4正式inventory票は11648 file/3525 directoryで、implicit3487に対する認証済み38件を列挙している。当方は両票の各宣言path合計74件について、実directoryの存在・非reparseだけを再確認した。親全file内容の再hash、親全directoryの再集計、親directoryの作成は本便では行っていない。

両親はread-onlyで、旧宣言directoryが欠ける場合は既存preflightが全payload/body読取・新REPORT mkdirより前に拒否してrootへ返す。前件票の original_v4_full_typed_status=NOT_COMPLETE_REEXECUTION_REQUIRED は保存された旧状態名であり、既に継続中のroot v4 attempt2（session82390 / PID13988）を新規に再起動する要求ではない。既存A2を継続したまま、2210どおり新GHAと分離する。将来このv5受領器自身を実行する時にも歴史v4のtyped受領を省略せず、既成功とみなすcache/skipを足さない、という限定である。これらの九引数・実path・全74件・前件の票は `invocation-and-readonly-parent-preconditions-v1.json` =47095 B / 38dffea1ed72bcf4d07679369530599fd17e8283729ee5f87063bc8cd393ea32。新artifactの空directory数や新rankはnullで、予測していない。

F8. **artifact handbackはUNKNOWN・未受領**であり、`$taskExpectedArtifact=$null` / `$taskImplementationComplete=$false` を維持した。rootの正式success API、candidate全ZIP/全展開取得/全entry pin/実rootのhandbackと再指示を受けた場合だけ、別の新snapshotでartifact exact四字段とguardを結ぶ。現中間sourceはそのために上書きしない。diagnostics-only/失敗/partialを完成candidate入口へ適用しない。新parent inventoryへの昇格は行わない。受領器/dot-source/fixture/cost/数学/source実行0、AST/import/compile/Git/GHA/network/credential操作0、新P/C私的body読取0、新agent0を維持した。

F9. 全21材料の目録 `launch-bound-final-material-manifest-v1.json` =**6584 B / 35a6e4836836e9c535eca241425af1b58f356ad1d7c906127d54eaba72aa8bf4**を保存し、全fileの実bytes/SHAを再照合した。目録自身と本返信だけが目録外で、directoryはpublic-inputs一つ。この中間納品の許可済みlaunch/承認結合の未接続箇所0、追加required finding0。一般本文・実行前件は保持し、rootのGHAへ新しい待ち条件を足さない。現source・全比較資料をこのpinで凍結し、実artifactの後着指示を待つ。

AUDIT_1089_VERDICT: OBSERVED_LAUNCH_AND_APPROVAL_STATIC_BINDING_PASS; INTERMEDIATE_FROZEN; ARTIFACT_UNKNOWN_NULL; GUARD_CLOSED; FULL_FORWARD_REVERSE_EOF_EQUAL; ALL_FIVE_SIBLINGS_RETAINED; NO_RECEIVER_SOURCE_FIXTURE_COST_EXECUTION; CANDIDATE_FALSE; CROSS_CHECKED_FALSE; VERIFIED_FALSE.
