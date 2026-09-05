# Task998 — 同語 readout WF v3 の全相対 POSIX path 順修理

## F1. 完了範囲と実失敗

Task998 を全文読み、新 `.github/workflows/d972-r07-continuation-positive-word-readout-v3.yml` と本返信だけを作成した。Task994 は 563 行の保存境界で保留し、キャンセルしていない。P/D の source、旧 WF v1/v2、公刊済み返信991–993は変更しない。

実 readout v2 は run **33997745566/1**、head **c6278fe1365f447b6183600e446f36defef80e76**、job **101391117505**。source/runtime、16 live artifact の全 ZIP、実64段の親履歴入場は成功し、P4/D3 の interface canary 全七群が実 PASS。その後 P 本走は 23:07:42Z–23:07:43Z、exit 1、保存 elapsed_seconds **0.265004**、reason **ValueError:unique_sorted_files** で終了した。state/delta/seed34/packet/refinement の入場まで log にあり、oracle の一覧で拒否。word は形成されず、D 本走は未実行である。

実診断の root 回収先は `%TEMP%/shadow-atelier-positive-readout-run33997745566-diagnostics-a1`。artifact **9978580135**、ZIP **3919059 B / 14951bde6ccf8a0bbf05587be8f0929ea146266b9d74661e60b9e14247a73f4f**。展開162 files / 18503891 B は root の whole ZIP 認証・安全展開記録であり、本担当はその保存 JSON と source 差分を読む範囲に限定した。

原因は WF v2 の `sorted(Path)` による component 順と、P v2 が要求する完全な相対 POSIX 文字列順の不一致。原 start の取り違えや数値親の変更ではない。前便の strict integer header 修理は実入場を通過した。

## F2. 実一覧と保存診断の照合

保存 `acceptance.json` は **1493571 B / 2c619f2fc4cc37e36d60175a7c68947da35d57023cf6159a89d6aca42ce10b8f**。PowerShell の JSON 読取と ordinal 文字列整列で16 role の実一覧を調べた。新しい Python/helper/AST をローカル実行したのではない。

| role | files | directories | 文字列順と異なる file entry 数 | 初不一致 index |
|---|---:|---:|---:|---:|
| oracle | 64 | 6 | 3 | 58 |
| task712 | 50 | 2 | 50 | 0 |
| continuation | 7916 | 1265 | 53 | 41 |
| 残る13 role | 各実一覧全件 | 各実一覧全件 | 0 | なし |

全16 role の directories は、今回の実一覧ではすでに文字列順だった。修理は files と directories の両方を完全な相対文字列順へ固定する。oracle では `repair-source-receipt.json` と `repair-source/...`、task712 では `r07-grade2-maps-v4-checker.json` と `r07-grade2-maps-v4/...`、continuation では `accepted-completion/original-cegar-run.json` と `accepted-completion/original/...` が境界になる。

保存 `preservation-result.json` は **893 B / 5268e4bf4ce62eb87e13089de5a2c1542c27b4554d97d554212f533f4426d620**。全16親、取得済み source/raw、acceptance、driver の不変は true、未形成 word/D だけが INCOMPLETE。Task991 の早期保存修理は働いており、v3 でも維持した。

## F3. 新一覧の production 契約

新 `inventory_fields` は exact `{files,directories}`、list 型、各 file の exact `{file,bytes,sha256}`、非負の厳密 int byte 数（bool 不可）、小文字64桁 SHA、safe relative POSIX name、file/dir の重複排除と disjoint を確認する。

`validate_inventory` はこの共通型検査の後、files の `entry["file"]` と directories がそれぞれ完全な相対文字列順であることを要求し、全 file descriptor の map と全 directory 集合を actual observation へ一致させる。型や EOF を整列だけで代用しない。

`scan(root)` の regular root、symlink 拒否、regular file、安全名、全 file の実 bytes/SHA、全 directory EOF は元通り。走査で取得した各実 descriptor の map を残し、返値だけを `sorted(files,key=lambda entry:entry["file"])` / `sorted(directories)` にして同 validator を通す。これにより admission、取得直後 baseline、新 before/after、word/D roster は同じ正規順になる。16 role 全部の scan がこの本番 helper を通ってから acceptance に入る。

actual map は scan が一度取得した file hash の全集合であり、新順のために同じ payload を二度 hash する必要はない。P/D 側の sorted/unique 条件を緩めていない。

## F4. 旧保存 roster の比較 adapter

Task999 は修理後の一覧を旧保存一覧と list のまま比較すると再度失敗すると指摘した。実 `retained-parent-receipts/resume64/all-parent-files-before.json` と after は、ともに **593399 B / e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c**。旧 JSON は exact hash の認証と before == after をそのまま維持する。

新 `retained_inventory(value,role,observed)` は exact `{role,files,directories}` と指定 role を確認し、共通 `inventory_fields` で全型・全名・重複・file/dir 型を先に認証する。次に file descriptor を一件ずつ copy した比較用 object だけを全文字列順へ整列し、新 scan の actual descriptor map / directory EOF と `validate_inventory` で一致させる。元 object や旧 JSON bytes は書き換えない。旧順の許容はこの保存済み比較 adapter に限定し、新 acceptance の順序要件は厳密なままである。

旧15 role は exact unique role 集合（元14親と COMPLETION_ROOT）を確認する。14親は新 admission の実 scan と、COMPLETION_ROOT は現 continuation 内の `accepted-completion/` の全 scan と結ぶ。本担当は実保存 JSON 同士でも、14親全 descriptor と全 directories、および COMPLETION_ROOT の **2699 files / 424 directories** を照合した。全件一致し、旧順の不一致は ORACLE_ROOT 3件、TASK712_ROOT 50件、COMPLETION_ROOT 53件だけだった。この確認は metadata の比較であり、旧算術を再走していない。

## F5. production 直結 metadata canary

新 GHA mode は `python -B "$report/driver.py" inventory-canary`。source receipt PASS の後、16 live artifact 入場の前に、REPORT 専用 `inventory-order-fixture/` へ7つの小 file と5つの directories を作る。通常 file と同 prefix directory、`-` / `/`、複数階層、uppercase、空 directory を含む。fixture は数学親にも13 word files にも入らない。

同じ `scan` / `validate_inventory` / `retained_inventory` を呼び、fixture の全名前・bytes・SHA・directory EOF を照合する。旧 component 順の歴史 copy は adapter で受理し、元 canonical bytes が変更されないことも確認する。拒否20件の exact 順序は次の通り。

1. component-order-files
2. component-order-directories
3. reversed-directory-order
4. duplicate-file
5. duplicate-directory
6. wrong-file-size
7. wrong-file-hash
8. bool-file-size
9. extra-file-descriptor-key
10. non-POSIX-file-name
11. missing-observed-file
12. missing-observed-empty-directory
13. retained-duplicate-file
14. retained-duplicate-directory
15. retained-wrong-size
16. retained-wrong-hash
17. retained-missing-file
18. retained-missing-directory
19. retained-extra-field
20. retained-wrong-role

同群の結果 schema は `d972.r07.continuation-positive-word-workflow.v3.inventory-canary`、group は `full-relative-POSIX-inventory-order`。source/driver hash、production_interfaces 三名、全 fixture descriptor、上記 rejected_cases、旧順受理/元bytes不変、elapsed/max_seconds、数学親再走 false、旧 success suites 0、candidate/cross_checked/verified false を保存する。結果と stdout は同一 canonical bytes、exit code は通常の改行付き `0\n` である。

内側は300秒未満を各境界で確認し、shell は290秒 TERM + 最大10秒 kill、step は5分。これは上限であり速度予測ではない。新 metadata canary はまだ未実行。既存 P4/D3 の七群は v2 ですでに実 PASS、v3 では WF と本走の結合確認として同じ七群を維持する。旧数値 success suite を追加していない。

## F6. 来歴、wire、成功 gate

新 WF の name/path/marker/upload は v3。marker は `[r07-continuation-positive-word-readout-v3-run]`。wrapper schema だけを `d972.r07.continuation-positive-word-workflow.v3` とし、P/D wire はそれぞれ既存 `d972.r07.continuation-positive-word.v1` / `d972.r07.continuation-same-word-eleven-slots.v1` のまま。P/D source の呼出し先は v2 である。

v1 の int/bool 失敗来歴に、v2 の実 run/head/WF/source/診断 ZIP/P stdout pins、七群実 PASS、D 本走未実行を `REPAIR_PROVENANCE.previous_readout_v2` へ追加した。二つの診断は来歴であり、第17数学親として入場させない。

`finish()` は新 metadata result の seal/schema、group、三 production helper、20拒否名、旧順copy受理/元bytes不変、driver hash、資源宣言、false assurance、stdout全bytes、exit0を認証する。最終 run receipt はその結果 file の bytes/SHA を `inventory_canary` として結ぶ。新群が欠落/FAILなら candidate を出さない。

元の全16数学親、30個の実 continuation entry pins、旧 completion、原 start、P/D source/raw closure、全文 runtime、同 root、13 file、11 slot、全80644座標、fresh rho2 全body、P一回/D一回、全保存 gate を保持した。P5400秒/D10800秒・各外側上限、7168 MiB、job330分は変えない。非零残差なら positive_readout は NOT_APPLICABLE。新数学結果、rank 増加、grade2 membership、full A0 をこの修理から主張しない。

always の取得直後 baseline、before 不足に依存しない取得済み after の保存、全16親/source/raw/acceptance/driver 不変、不足時 INCOMPLETE は前版と同一である。新 fixture と失敗診断も always artifact に残る。

## F7. 静的差分と修正過程

v2→最終v3の関数単位テキスト比較では、既存関数の削除は0、追加は `inventory_fields` / `validate_inventory` / `retained_inventory` / `inventory_canary`、本文変更は `scan` / `authenticate_continuation` / `finish` / `main` の4本だけ。定数の差分は wrapper v3 identity と実v2診断来歴に限る。ARTIFACTS、COMPLETION_ENTRIES、ACCEPTED_COMPLETION_ARTIFACT、CONTINUATION_ENTRIES、全 source/raw/鮮度親 pins、runtime、limits の各定数本文が v2 と同一であることをテキスト比較した。

未凍結の先行版には、canary 挿入時に `exact_pin` が欠落したことと、shell printf に backslash が二個入ったことを root が指摘した。前者は v2 の4行をそのまま復元して同一本文を確認し、後者は既存 step と同じ実 backslash 一個へ直した。Task999 の旧 roster 順指摘は F4 の限定 adapter で修理した。いずれも最終凍結前の差分で、旧版の source や artifact は修理していない。

ローカル作業は source/JSON 読取、テキスト差分、metadata の型/名前集合/bytes/SHA 照合だけ。Python/import/AST/GAP/数値、network/git/credentials/GHA、新agentは実行していない。D v2 の新算術本文は読んでいない。

## F8. 凍結値と未実行境界

| file | bytes | SHA-256 |
|---|---:|---|
| 新 WF v3 | 108358 | 04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604 |
| P v2（不変） | 175318 | cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c |
| D v2（不変） | 176579 | 865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1 |
| 旧 WF v2（不変） | 92986 | 47043063db8e330210a29594cb8b91900a40c0750f651b2647c2101047bc8477 |
| 旧 WF v1（不変） | 84418 | 9e90bfeca6907fd71a4158308737a5a23677e3f2972b6e31391b5736b14bf36a |

新 WF は **LF1674 / CR0 / BOMなし / 最終LFあり / 行末空白0**。公刊済み reply991 も **15212 B / 896b29a97912ed3ca31ea910319adf900de2ca14e1f8038d8658d390ab426930** のまま。

本票は WF-only 修理の静的完成票である。v3 の新 metadata 群、七 interface 群、本 P/D、candidate、CV9 は未観測。Task999 と root の最終差分読了後、公開と GHA は root が行う。新しい必須修正がなければ本 WF と返信を凍結し、Task1000/1001 の共通追補を読んで保留中 Task994 へ戻る。

AUDIT_998_VERDICT: WF_V3_STATIC_COMPLETE_RUNTIME_PENDING
