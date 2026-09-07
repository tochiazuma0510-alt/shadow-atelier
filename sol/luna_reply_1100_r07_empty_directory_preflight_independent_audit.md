# Task1100 — 認証済み空 directory 前処理の独立静的別読

F1. Task1100 全文2304 / `43448a8dbd6e0e9b08b32eadad317a2a64ef6da5af834c4202a8c4d6d0cbadc5`、Task1099、裁定2219 snapshotと応答を読み、作者の全材料凍結通知後に最終 helper 全509行と返信1099 全文を別読した。判定は `LIMITED_INDEPENDENT_STATIC_PREFLIGHT_PASS_GUARD_CLOSED_RUNTIME_PENDING`。最終 source の未読0、必須修正0。対象は `%TEMP%/shadow-atelier-audit163/task1099/root-review-authenticated-empty-directory-preflight-v1.ps1`、48090 B / `38a756f12174738e5433750e403d3ee0b66b22e8f95d3c80ad1917532890fa8d`、LF509 / CR0 / ASCII / BOMなし / 最終LF / 行末空白0。既定guard=false、root承認入力は未形成である。

作者返信1099は10167 B / `0543d273027f9742882dcc6f71d4dad4c5b04c99b41d946882c347b74d320588`、作者目録は7879 B / `463882b25ea5cf89360f76d92785210bfb7a988e21a568b39a10338a6418afd1`。目録の全20材料 / 2624309 B / subdir0を独自に全hash照合し、目録・返信を含む22本を `task1100/independent-final-snapshot-v1/` へ全raw同一コピーした。歴史draftとsource断片は保存材料として認証したもので、最終実装の代用にはしていない。作者の静的PASSや未実行票を独立根拠として転記せず、以下を自系rawと実保存metadataから確認した。

F2. 全32関数＋prefix/main＝34区間を、ASCII rawの関数開始位置とMAIN境界から独自に再分割した。全48090 bytesに隙間・重複なし、全区間のoffset/bytes/SHA/先頭行/LF数が作者台帳と一致し、順方向連結と逆順offset配置の双方で全byte一致した。全EOFは次のとおり。各区間の完全SHAは `independent-entire-raw-EOF-and-retention-v1.json` に収録した。

| 区間 | offset | bytes | 行 |
|---|---:|---:|---:|
| MODULE_PREFIX | 0 | 1557 | 1–23 |
| Need | 1557 | 84 | 24 |
| Same | 1641 | 3019 | 25–75 |
| PlainInt | 4660 | 78 | 76 |
| Fields | 4738 | 381 | 77–84 |
| Flag | 5119 | 111 | 85 |
| NoReparse | 5230 | 402 | 86–93 |
| StreamPin | 5632 | 760 | 94–107 |
| RawSHA | 6392 | 231 | 108–112 |
| AbsolutePath | 6623 | 430 | 113–120 |
| Within | 7053 | 197 | 121–123 |
| SafeRelative | 7250 | 617 | 124–131 |
| RelativePath | 7867 | 257 | 132–137 |
| JSONInteger | 8124 | 104 | 138 |
| Descriptor | 8228 | 289 | 139–143 |
| FullPin | 8517 | 474 | 144–151 |
| CheckPin | 8991 | 363 | 152–157 |
| PinnedJSON | 9354 | 1072 | 158–173 |
| InventoryModel | 10426 | 2051 | 174–194 |
| ObserveTree | 12477 | 2124 | 195–219 |
| WholeZIP | 14601 | 3027 | 220–251 |
| ParentSpec | 17628 | 3386 | 252–276 |
| ReadRegistrations | 21014 | 3529 | 277–306 |
| ExpectedInventory | 24543 | 3867 | 307–337 |
| AuthenticateDirectoryEvidence | 28410 | 4267 | 338–364 |
| AuthenticateParent | 32677 | 888 | 365–375 |
| ValidateOutputPaths | 33565 | 851 | 376–387 |
| ReadRootApproval | 34416 | 2497 | 388–405 |
| JSONBytes | 36913 | 156 | 406 |
| SaveNewEvidence | 37069 | 395 | 407–413 |
| Journal | 37464 | 128 | 414–417 |
| RestoreRegisteredEmptyDirectories | 37592 | 2596 | 418–446 |
| ParentBeforeRecord | 40188 | 423 | 447–449 |
| MAIN | 40611 | 7479 | 450–509 |

保持8関数は Need / Same / PlainInt / Fields / Flag / NoReparse / StreamPin / RawSHA。旧1096 helper全516701 B / `fd26b0e1f571350d23732d2966d10ae3c3a64b07dc87298bfd2b5cc3ea3ba632`をraw pinで認証し、旧側の開始位置も独自に求め、各旧本文と最終本文の全byte一致を確認した。Sameのnull・配列順・ordinary scalarの厳密型/値・object key照合は不変。旧1096受領器や保持関数を実行したという意味ではない。

F3. scopeは旧v3空36と旧v4空38の74名だけである。source中の固定literal20本（sibling4と各親metadata/inner ZIP8本）を抽出し、各実保存fileの全bytes/SHAへ独自に結んだ。実root全payloadを再hashする代わりにはしていない。

| 親 | run / attempt | 全file / bytes | 全dir / file由来祖先 / 登録empty |
|---|---|---|---|
| v3 | 34023589045 / 1 | 11437 / 1267599138 | 3475 / 3439 / 36 |
| v4 | 34120585268 / 1 | 11648 / 1308094050 | 3525 / 3487 / 38 |

各native run/envelopeの二self-exclusionを含めた全file宣言を再構成し、全directory宣言・全file祖先を比較した。v4は正式canonical files1931889 B / `ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5`とdirectories200290 B / `f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64`の全配列へ一致した。旧v3 fixture全4600 file / 2281 dir、旧v4全4747 file / 2330 dirを各全root目録からの投影と比較し、controlsの全file descriptorと全directoryも全root目録へ結んだ。archive receiptのnative schemaと4descriptorはsource literal/実file pinに一致する。

74名すべての全目録membership・重複なし・宣言regular-file子孫0と、全非implicit directoryがこの74名だけであることを独自に照合した。fixture分はP registrationのhost0/1のparentsと各子で、旧v3は32名、旧v4はbatch-parent子を含め34名。残り各4名は `ZIP-casefold-extracted` / `ZIP-duplicate-extracted` / `ZIP-traversal-extracted` / `metadata-fixture/empty` で、保存controlsと全envelopeに束縛される。前者の根拠をinner ZIPの明示directory、後者を保存controls/envelopeとする区別は通常本文L338–363にも接続している。Task1100自身はZIP entryを開かず、実rootの現在directory censusや全payload照合も行っていない。inner explicit entryの型・全EOF/SHA照合は、次項の未実行通常経路を静読した判定である。

F4. 最初のmkdirより前の認証順を全callerから追った。AuthenticateParent L365–374は、元outer container全pin、登録siblingの同じ認証済みbytesのJSON読取り、完全目録、hidden込みの実全regular file読取り、登録以外の欠directory拒否、outer全entryのtype/名/size/全stream SHA/EOF、inner全entryとdirectory根拠をすべて完了してから返る。outerは元files-only形を要求し、明示dirを捏造しない。innerは全P/C namespace・Unix regular/directory型・zero-byte directory EOF・全登録entry集合を要求する。独立CRC計算を実施済みとは記録しない。

MAIN L470で両親を完全認証し、L471で2件完了を要求し、L473で両親の実全before目録・欠名・根拠を親外へCreateNew保存した後だけ、L475の復元へ進む。いずれかの認証/全before保存失敗でmkdirに到達する枝はない。唯一のdirectory APIはL438、唯一のmain callerはL475。depth順・同depthでordinal順に登録全名を見直し、既存ordinary directoryはALREADY_PRESENTでAPI0、欠品時は登録名/子孫なし/既存file衝突なし/全path非reparse/直上親実在・非reparseを直前に要求する。requestをflushした後にAPIを呼び、返った後もdirectory型と非reparseを確認する。削除・rename・regular file補充・ACL・入力内marker・cache・source/process実行経路はない。

F5. 現L14のfalse guardとL451は入力認証や出力I/Oより前にある。将来rootが別途全pin付きで受理するguard有効版でも、RootApproved switchと実承認JSONのwhole pinが必要。承認はexact9字段、sourceはexact3、v3→v4のordered parentsは各exact5で、ordinary整数・Boolean・stringを区別する。現在helperの絶対path/full pin、両親の元root、両archive全pin、新receipt pathとscopeに束縛する。2219だけで実行が自動解禁される条件ではなく、本監査は承認JSONや実行可能snapshotを作成していない。

receipt / `.preflight.json` / `.creation-journal.jsonl`は別々の新pathで、両root/両archive/承認/helper所在directoryの外、既存の親directory配下だけを許す。SafeRelativeのPOSIX要件・traversal/予約名/末尾dotやspace拒否、Ordinal集合とcasefold重複排除、file/dir相互衝突、実全treeのreparse拒否まで確認した。すべてCreateNewとFlush(true)を使い、既存証拠を書き換える枝はない。

F6. 途中失敗と最終成功を区別する。L476–501は早いerrorを保持し、認証済み各親について独立に全after読取りを試みる。各regular fileの全EOF/SHAとbefore同一、完全directory集合、outer container全再hashを要求する。異常親はFAILとnull inventory、未認証親は完成推定しない。一方の失敗で他方の観測を省いて自動PASSにせず、両after PASSかつ以前のerrorなしとcompletion eventのflush成功後だけcomplete=trueになる。

journalは到達したrequest / returned-present / already-present-no-callを別々に記録する。API要求数を排他的な実作成数へ読み替えず、exclusive_creation_ownership_proved=falseを維持する。全dir既存の場合も同じ両親全認証とafter再読を通り、mkdir0になる。journal/最終receiptの記帳失敗・最終receipt未形成・FAILは前処理成功ではない。外部processの競合を排除するlockはなく、直上親確認とAPIの間の外部変更、最終観測後の削除を防ぐ保証もない。以前の36名再欠品の主体・原因はUNKNOWNのまま保持する。

F7. 自系証拠はすべて `%TEMP%/shadow-atelier-audit163/task1100/` の新規fileに保存した。最終目録は自己と本返信を除く全28 file / 2835642 Bを固定し、作成時に作者の全20材料pinも再照合した。scope先行票2本は当時のhelper未読境界を残した履歴で、現在の最終判定は全本文別読を保存した後続票にある。

| 独自証拠 | bytes | SHA256 |
|---|---:|---|
| independent-final-material-intake-v1.json | 8809 | d71f01edb1915a107913efd42ac3954b630c92ee582624589b6359ea23b4753f |
| independent-entire-raw-EOF-and-retention-v1.json | 25901 | 21bb8d327a3625a0ec8eca2864cd5192496ca1287c886dd852c9c9b067ce996f |
| independent-source-literals-and-empty-authorities-v1.json | 128264 | a4f9b42bacc107e1b87641744ec33dc99c17cf15647cb4bd46a08a0e6f0b22d3 |
| independent-final-source-control-review-v1.json | 9417 | f0e46a683e7e36e6795deac741147630413af3d6a298f6ec5aae44438aba11e4 |
| final-independent-static-proof-index-v1.json | 10749 | 3d637cac0c2badc471b228e6ab80529bf596c644200d650aab15931e041f4649 |

F8. helper/dot-source/AST/import/compile/Python/GAP/source/数学/自己試験の実行0、実親/archive/dir/file変更0、Git/GHA/network/credential/process操作0、receiver再開0。実行したのは本便で許可されたraw/全pin/宣言metadataの静的比較だけである。P/C数学本文を独立監査したとは主張しない。旧typed受領の未完、正式v4 inventory採択1706/8411、新v5研究GHAを区別し、本便を新v5発射の追加gateにしない。本判定は静的採否のみで、実復元や旧typed再起動の実施・許可を含まない。数学上のcandidate/cross_checked/verifiedの昇格は0。

AUDIT_1100_VERDICT: LIMITED_INDEPENDENT_STATIC_PREFLIGHT_PASS_GUARD_CLOSED_RUNTIME_PENDING
