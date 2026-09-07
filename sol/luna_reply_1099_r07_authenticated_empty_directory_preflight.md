# Task1099 — 認証済み空74 directory の起動時前処理案

F1. 作者静読を完了した ASCII metadata helper を凍結した。最終 source は `%TEMP%/shadow-atelier-audit163/task1099/root-review-authenticated-empty-directory-preflight-v1.ps1`、48,090 B / `38a756f12174738e5433750e403d3ee0b66b22e8f95d3c80ad1917532890fa8d`、509 LF / CR 0 / BOM なし / 最終 LF / 行末空白 0。実装 guard は false、root 承認入力は未形成、helper/fixture/AST/import/compile/dot-source/数学実行は 0、実親の mkdir/delete/regular-file 書換えは 0。これは自作案の静的完成であり、独立監査や実前処理成功を主張しない。

F2. 根拠は Task1099 全文3327/02572d713fa0c82acc5b6e8ddd1fc42f41b4a8c1873a7a32fb6ebec421406cff、裁定2219 snapshot 全文2278/80fffd6a0dde27644c80a54f8b8c5d66fb4e257f48b94c4029be4ac2a5a07da4、応答全文1250/db4c7a550a478999581498d38013fb84afdd8e4aaba7879be0bfcf305f241e00。旧 A2 終了票2544/5ec16f9edf3cf5c131f0d5d1f7615c3f80599ee303414512e1387c86d5ed1043 は2026-09-07T18:44:49.9690861Z、exit 1、receipt null、Inventory L148 → ReceiveBatchParentFixtureHistory L705 の missing directory を保存している。旧v3復元票4595/86b588eb3feaee2034235f8958e074d006f6926b4666cc119866cea4b242aaf6 の15:40:06Z全集合一致後、診断票24781/00866355d8d821e8b22ca56d98d0fbe721992d13a33267781db8443b2d04d199 は19:04Zに同じ空36名の再欠品、全11437 file SHA一致、extra dir 0 を記録する。主体・原因は UNKNOWN。mtime や工房の無操作回答から原因を補わない。

F3. 両親を別々の native schema/root/run/全pinで扱う。旧v3の歴史復元票と旧v4の正式7022/64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753、canonical files1931889/ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5、canonical directories200290/f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64 を、helper sibling 4本として全raw同一コピーした。各使用時に全SHAを確かめ、その同じbytesだけをJSONとして読む。同名別rootへの取り違えは、保存票の絶対root、明示root承認、native launch、全container/file pinの結合で拒否する。

| 親 | run / artifact | 全file / bytes | 全dir / implicit / 登録empty |
|---|---|---|---|
| v3 | 34023589045 / 9987222571 | 11437 / 1267599138 | 3475 / 3439 / 36 |
| v4 | 34120585268 / 10020349387 | 11648 / 1308094050 | 3525 / 3487 / 38 |

旧v3 outer ZIP は369233546/781c9f467bd38305c524a0a2bf5b361f45e75bc4234d9cf6e891e01175db9e2e、旧v4は377383320/84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5。旧v3 head794c5e9f883cb5ff21b2ee087c1d4baa84ac6760、旧v4 head92720e5371164545259c3007cb11e951fa5e1686、各attempt 1を保持。外側ZIPに明示directory entryを捏造しない。旧v3空36＝P registration host0/1のparents＋各15子の32と外側4、旧v4空38＝同各16子の34と外側4。外側4名は ZIP-casefold-extracted / ZIP-duplicate-extracted / ZIP-traversal-extracted / metadata-fixture/empty。

F4. 通常経路の全接続を静読した。ReadRegistrations L277→ExpectedInventory L307 は native run/envelope の正確な二self-exclusionを含む全fileと全directoryを構成し、旧v4ではcanonical全配列へ結ぶ。InventoryModel L174 は型・全名の相対POSIX規則・casefold重複・file/dir衝突・祖先宣言・全順序を確認する。ObserveTree L195 はhidden込みで実全file集合/各全bytes/SHAを読み、不足file・余剰file/dir・reparseを拒否する。欠directoryは登録74名の部分集合だけを許し、それぞれに登録regular-file子孫がないことを確認する。

WholeZIP L220 は全outer container SHAの後に全entryの型/全名/size/全stream SHA/EOFを読み、inner selftest-fixtures.zip は全明示directoryの型/0-byte EOFと全regular entryまで読む。独立CRC再計算は主張しない。AuthenticateDirectoryEvidence L338 は全fixture三目録、全archive receipt、実root内全fixture投影を結び、fixture空名をinner ZIPの登録明示directoryへ、外側4名を全controls/envelopeへ接続する。登録empty以外を例外扱いする枝はない。

MAIN L470–471で両親のAuthenticateParent完了を要求し、L473で両方の実全before目録と欠名/根拠を親外へ保存してから、L475で唯一の復元関数へ進む。RestoreRegisteredEmptyDirectories L418はdepth順・同depth内ordinal順、既存ならALREADY_PRESENTでAPIなし、欠品なら既存file衝突/非reparse/直上親の実在を再確認する。L438のDirectory.CreateDirectoryが唯一のmkdir callsite。失敗時のcleanup/delete/rename/regular-file補充/ACL変更はない。既に全dirが揃っている場合も両親の同じ全認証を行い、mkdirは0回になる。

F5. 明示8引数は OldV3Root / OldV3Archive / OldV4Root / OldV4Archive / RootApprovalReceipt / RootApprovalBytes / RootApprovalSHA256 / ReceiptPath、別にRootApproved switchを持つ。現false guardはL451で停止する。将来rootが別版の実行可能snapshotを全pin付きで読了し、approved=true・正確なhelper全pin・両root/両archive全pin・新receipt pathを持つ実承認JSONを固定するまで、mkdirへ到達しない。承認JSONはexact9字段、各parentはexact5、sourceはexact3で普通整数・Boolean・ordinary stringを区別する。2219だけで実行を自動解禁せず、追加のユーザー承認質問を本便で発行しない。

ReceiptPathおよびその`.preflight.json`/`.creation-journal.jsonl`は別々の新pathで、両root/両archive/承認/handler所在directoryの外、既存の親directory配下に限る。全CreateNew＋Flush(true)を使う。journalのSTART/認証完了/CREATE_REQUEST/CREATE_RETURNED_PRESENT/既存no-call/失敗/最終読了を実到達時だけ保存する。要求数・APIが戻って存在を再観測した数・既存でAPIを呼ばなかった数を分け、排他的な作成主体を証明したとは記録しない。未実行の現在、成功receiptや実作成数は作っていない。

L482–501は復元に失敗しても各認証済み親の終了観測を別々に試みる。全file再hash・before fileとの同一性・完全directory集合・outer container全再hashを両親に要求する。一方の異常で他方を自動PASSにせず、異常親のinventoryはnullと実error、未認証親は完成扱いしない。途中のerrorは保持する。全before保存前の停止はbefore nullのまま。最終journalのflush後だけcomplete=trueとなり、最終receipt未形成/FAIL/記帳例外は前処理成功へ読み替えない。

F6. 静的実測材料と限界を分けた。選択20入力（登録sibling4、各親metadata/inner ZIP8）を実full SHAで照合し、最後にも同20本の不変を再hashした。全saved目録から74空名のmembership/regular-file子孫なし/controlsまたはfixture接続を独自に照合し、現在この74名が全不在・同名regular-file衝突0をread-onlyで再観測した。全実parent file census/全payload hash/全ZIP entry再読は本便で実行していない。それらを将来のhelper通常経路から省くこともしていない。実親全raw不変をこの選択観測だけで主張しない。

全32関数＋prefix/mainを全48090 bytes/34 EOF領域へ分割し、全区間のoffset/bytes/SHA/LFと全rawの順・逆組立一致を記帳した。1096のNeed/Same/PlainInt/Fields/Flag/NoReparse/StreamPin/RawSHAの8本文は、各旧rawと最終rawが完全一致する。Sameの配列順・null・普通scalar型/値・object key比較を変更していない。新一般parserや算術readerは追加しない。将来のWholeZIPにあるAdd-Type -AssemblyNameは既存.NET ZIP assemblyの読込のみで、受領sourceのimport/compileではなく、本便ではこれも未実行。rootから全509行先行読了/追加required 0の通知を受けたが、1100独立票は本票凍結時点で未受領。

| 最終材料（task1099相対） | bytes | SHA256 |
|---|---:|---|
| complete-source-EOF-and-retained-helpers-v1.json | 26666 | 648945bd08b51839ae6ebf8db05d1efdc54471f351c34d7a9d5c03eb2537211a |
| registered-parent-metadata-and-empty-scope-static-v1.json | 91337 | 348703bca7c39256dda02cc9a0f762d730f5704a82e7f2d9165b9ae968483b6b |
| static-control-paths-and-public-approval-contract-v1.md | 11751 | 3d7f355c6175fccd1892ff182d981fc2579ca722a7f7c93808e98b9f82093aaf |
| final-static-closure-and-input-retention-v1.json | 16058 | 2902d14bc32830035328511d5cbfdc7807b35e8b2ce34e754f6bc5fec788939b |
| final-material-manifest-v1.json | 7879 | 463882b25ea5cf89360f76d92785210bfb7a988e21a568b39a10338a6418afd1 |

目録は自己と本返信を除く全20 file / 2624309 B、subdir 0を固定する。現物の旧draft/素材は履歴役として含め、最終sourceへ取り違えない。未完成draft01の括弧、draft04のtext組立改行不備は保存直後の静読で発見し、旧draftを保持したまま別版へ修理した。いずれも実行せずPASSにしていない。最終rawはdraft05と完全一致。旧1096 helper516701/fd26b0e1f571350d23732d2966d10ae3c3a64b07dc87298bfd2b5cc3ea3ba632と旧返信9548/b632da110edbc721ff5cd03a0a686cf509d4fb5d5bfb45e88cddc319b92eda1fも不変。

F7. これは起動時の認証と限定復元であり、filesystem全体をlockせず、外部操作の後日/同時削除を防ぐ保証はない。直上親確認からAPIまでの外部変更も排除できないため、API呼出しと実後観測を分け、最終全再読を必須にする。最後に成功を観測しても、その後のdirectory存続を主張しない。旧36再欠品の除去原因はUNKNOWNのまま。正式v4 inventory採択1706/8411、追加typed未完、新v5研究GHAを別に保ち、本前処理を新v5発射の追加gateとしない。既走receiver/process再開0、Git/network/credential/GHA0、P/C数学本文不読、数学格付け変更0。

AUDIT_1099_VERDICT: AUTHOR_STATIC_PREFLIGHT_COMPLETE_GUARD_CLOSED_RUNTIME_PENDING
