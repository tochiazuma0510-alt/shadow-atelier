# Task1041 — 同旧64からのfresh k128 WF v3（実装完成・未実行）

最終 WF は 283,886 B / `6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f`。公開 registry の生成・全 raw range 照合・二票・非実行 history 全保全まで完成した。F2–F5 は先行作成時の記録であり、そこでの registry 未受領・生成未接続は F6–F10 で閉じている。新 GHA と数学実測は未実行、root の最終公開判断を残す。

## F1. 読了契約と固定範囲

Task1041、公開1040/1035/1029/1030を全文読了した。新 `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml` と本返信だけを作成する。旧WF v2は166471 B / `887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5`、実hash一致を確認した。旧版・P3/C3・1039 helper/返信は変更しない。

初期状態は同run33990567016/1、旧64/rank1450/gen8155、同15親である。新batchはv3 / batch_size128 / max_batches1 / no-refill / fresh P一回・C全新payload一回。P5400秒・C10800秒・各7168 MiB・outer6000/11400秒・job330分を保持する。新rankやa(128)、速度は未観測である。現在までのa(32)=32 / a(64)=64は、同固定lambda・候補順の前置長の観測として扱う。

新Pの公開pinは209926 B / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8`、Cは178914 B / `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7`。新二群は `k128-version-registration-and-types` / `k128-full-roster-cutoff-and-restoration`、拒否件数P30/9・C28/8。Cにbatch-size CLIを増やさない。保持19＋新2のPython21とraw3の全24を維持する。

## F2. 作成中の追加受領証

REPORTへ `arithmetic-selftest-inheritance.json` / `shared-tcb.json` を加える。歴史自己試験は実v1/run34004423047の保存pinへの参照で、再実行0・本runで歴史payload再取得falseとする。共有二kernelは独立実装の除外として明示し、現在runのcall coverageはNOT_MEASUREDのままにする。

継承source/regionの実registryはTask1042の独立静的票をrootが読んで配達するのを待つ。未受領pinを推定せず、未登録のままでは入場を拒否する形で他のWF処理を作る。歴史sourceを照合する場合も非実行のaudit-history-sourcesとして全fileを保存し、21実行Python/3rawや15数学親には加えない。

全fixture raw/empty dirs、三比較、inner ZIP全entry再読、always全保全、全REPORTの明示二除外、二upload・30日を保持する。新二票を既存inventory/source保全/run全file pinへ結ぶ。継承regionの実登録・全新WF静読・別WF監査・root公開は未閉であり、本返信とWFは未freezeである。

## F3. 先行保存したWF差分と保持確認

旧WF v2全2314行を全文読了した。外側workflow名/path/marker/REPORT/SCHEMA/WF_SCHEMA、新P/Cの二pin、128の登録/CLI、二群名と件数、selected count上限128、local ordinal/row上限127、private sequence上限771を新WFへ移した。元親64・履歴32・SHA64桁・64 GiB展開上限・旧schema/旧source/旧artifact名は変更していない。

旧WFの実upload保持値は二箇所とも14日だった。Task1041の明示指定に従い、新WFの二uploadだけを30日へ変更した。旧版を30日だったとは記録しない。source入場の先頭には未登録registryを拒否する暫定gateがあり、二新票の発行と全pin結合は未完成である。

現在の保持19＋新2＋raw3の全24source/dataについて、公開WF pin表を抽出して実fileの全bytes/hashを局所metadata操作で照合し、全24が一致した。C本文は表示・読解せずhashだけを使った。旧WFと新WFの全親env表、およびP_DEPS/C_DEPS/DATAから全completion/continuation entry表とretained定数末尾までの文字列も完全一致した。親API/ZIPの新取得や数学は実行していない。

二新票はsource-receipt後・live親入場前に発行し、実行receipt・既存control baseline・sourceのbefore/middle/after保全・最終run receiptへ結ぶ予定である。歴史source非実行の全copy、registry原文pin、各rangeのraw LF bytes/hashと必要な明示除外を認証する具体的registry字段は、Task1042からのroot手渡しを待って確定する。全REPORTへの二新票等の追加は明示二除外の外側として収録し、新たな省略名を設けない。

## F4. registry 受領前に保存した二票の配線

WF の現在保存値は 180,446 B / SHA256 `90577199c6a4d9ebd28b32e00edbb295a8691a3eaccc2723d8e47698dd294427`、2,504 LF、CR/BOM/non-ASCII なし、末尾 LF。これは完成 freeze ではない。root 既読の 171,811 B / `fb3bc4224a6d2955491bf81049449702bca5d740b388a638a1295535fe9c5667` から、以下の metadata 配線を加えた。

- `arithmetic-selftest-inheritance.json` / `shared-tcb.json` の固有 status と false assurance、source-receipt / launch / registry / 非実行 history roster を結ぶ `audit_material_bindings` を保存した。履歴 source は全 file hash と保存 copy 全 inventory を照合し、実行対象 21 Python / raw 3 へ追加しない。
- 二票と registry、history copy 全体の基準を `audit-materials-before.json` に置き、live 入場・五実行の start/result・P 後から C 前・C 後・最終 gate に同じ full pin を結ぶ。run-receipt に二票それぞれと registry / before / after の full pin を載せる。
- `always` は完成した基準があれば source / copy / registry / 二票を再照合し、途中であれば `acquired-audit-history` の取得済み各 source/copy と部分 inventory を保全する。全 REPORT inventory の除外二件は増やさない。
- 新 `audit` 工程を source 入場後・15 親 live 入場前に置いた。`INHERITANCE_REGISTRY = None` と生成処理の明示拒否を維持し、未受領の Task1042 region / raw hash を仮作成していない。実 registry の全量取り込み・生成・範囲比較を残件として保持する。

この差分は保存後に全追加 helper と全接続点を静読した。ローカルで driver / AST / selftest / 数値処理を実行していない。root から公開 registry が渡った後にこの未完箇所を閉じ、全最終差分・別 WF 監査を受けて最終票にする。

## F5. 登録 marker と監査票の型比較の自己点検

F4 保存後の全文検索で、job の push marker に旧 `v2-run` が一箇所残っていたことを作者が発見し、新 `v3-run` に修理した。現在の workflow/source path と 128/127/771 の各登録は新値、旧64親・64 GiB・SHA幅64・nonce32等は従来の意味のままと確認した。監査票の registry / history / 歴史自己試験表 / 共有kernel表は canonical JSON bytes 比較へ揃え、bool と普通整数が Python の値比較だけで一致する境界を避けた。

現在 WF は 180,534 B / SHA256 `b725a5204c75af7bd8caa20c2576e40e494dc7989b3faae28c5b767d850c48b4`。F4 からの変更はこの marker 一箇所と四つの canonical 比較だけ。実 Task1042 registry の受領・生成箇所は依然未完成、未 freeze / 未実行である。

## F6. root 手渡し registry の全文読了と原文固定

root が独立 Task1042 の限定静的 PASS を受理した後、公開された `%TEMP%/shadow-atelier-audit163/k128-sources-and-inheritance-registry-v1.json` を全文読了した。正本は 76,867 B / `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38`、878 LF、CRなし、末尾LF。最初の分割表示の合成出力が切り詰められたため、その後に全 JSON を省略なしで表示し直して全字段を補完した。C 私的 source 本文・C 作者票・1042 私的監査本文は読んでいない。

WF は原文を `INHERITANCE_REGISTRY_RAW` として完全固定し、全 bytes/SHA を `INHERITANCE_REGISTRY_PIN` へ固定する。YAML の共通10空白を除くメタデータ抽出で、埋込原文が同76,867 B・878 LF・全SHA一致することを確認した。GHA の `public_audit_registry` も同原文全pinを必須とし、REPORT の `audit-region-registry.json` へ pretty JSON の元bytesをそのまま保存する。canonical 再整形で元pinを変えていない。

全6 source は P1/P2/P3/C1/C2/C3。P3/C3 は既登録の現 code 二本へ、歴史 P1/P2/C1/C2 は独立した非実行証拠へ結ぶ。全11字段を持つ各 source descriptor の version/side/role/LF型と現sourceの全pinを接続する。歴史 suite の run/head/artifact/ZIP、二 selftest 全pin、三群名・P7/6/26・C2/3/14、現k128の初期64/1450/8155・15親・21Python/3raw・新二群P30/9/C28/8も公開表へ一致させる。

## F7. GHA で実行する range 照合と二票の exact 範囲

`capture_audit_source_versions` は全6 sourceの実全bytes/hashとLF/UTF-8/EOFを読み、歴史4本だけを `audit-history-sources/search/<元basename>` に全保存する。各完成copyは `acquired-audit-history/P1.json` 等の取得ledgerに元全pin・copy実path・非実行を記録する。ファイルを import/AST/算術実行せず、既存21実行Python・3raw・15数学親を増やさない。

`compare_audit_regions` は公開20 regionに属する60 descriptorを全量処理する。1始まり・両端包含・各行LFを含む元UTF-8 bytesの範囲を取り、その全bytes/SHAを照合する。

- 9不変 region は PまたはCの三版を同じ順で取り、hashだけでなく三つのraw bytesを直接比較する。正規化は行わない。
- 2 literal 除外は各三版の実一行と公開 `raw_utf8` を完全比較する。WORKFLOW literal と selector docstringを削除した同一本文とは呼ばず、別登録行として保持する。
- 9変更 region は三版それぞれの範囲・全pinを照合し、`STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY` として不変claimの外に置く。Cの切出し・追加gateを無条件に継承したとは書かない。
- 全sourceごとに全登録範囲を行順に並べ、1行目から最終LFまで欠落・重複がないことを必須とする。結果に6件の全source partition、60 descriptor、9/2/9件と正規化falseを保存する。

`compare_audit_shared_kernels` は公開四kernelの実全file pinを現在の24件code/raw closureへ結び、四つのraw range全pinを照合する。登録どおり `sparse_adjoint` のP/C範囲は直接byte一致も要求する。projectionの異なるdocstring/error-labelを同一byteと偽らず、個々の登録pinを比較する。call coverageは `NOT_MEASURED`、`kernel_third_independence_claimed=false` を維持する。

REPORT の二票はそれぞれ schema suffix `.arithmetic-selftest-inheritance` / `.shared-tcb`、status `STATIC_INHERITANCE_REFERENCE` / `DECLARED_SHARED_TCB`、candidate/cross_checked/verifiedすべてfalse。共通字段は registry全file pin、source-receipt全SHA、非実行4source roster、launch、現code、全6source登録表、line_contract。前者は公開inheritance全表・静的source監査・実60range照合結果・歴史自己試験表を、後者は共有TCB全表・実四range照合結果を保存する。歴史数学suiteは参照であり、`old_mathematical_suites_rerun=0` / `historical_payload_reacquired_in_this_run=false`。両票から新実行の旧数学PASSや完全独立性を導かない。

## F8. 二票と実行・全保全・最終 run の結合

source admissionの次、live親入場の前に一回の `audit` 工程を置く。原文registry・4歴史source全copy・二票が揃ってから `audit-materials-before.json` をsealed保存する。そこにはregistry全pin、二票各全pin、非実行4source全pin、copyの全file/dir inventory、source-receipt全SHA、launch、非実行/非数学親false型を固定する。

live入場と全五実行（metadata/P新自己試験/C新自己試験/本P/本C）は `audit_material_bindings` を通る。基準・registry原文全bytes・二票全file pin・source/歴史/共有表・false assuranceを再照合し、execution-start/resultに同じ基準pinと二票pinを載せる。P直前の全REPORT基準にもこれらを含む。P後からC前の入力票と、C後の `audit-materials-after.json` / preservation-resultへ同じ全量を結ぶ。

`always` の完成経路では全歴史source実bytes・全copy・registry・二票の同一性を要求する。生成途中なら不足をINCOMPLETEに残したまま、取得済みledgerの各全copyと部分inventoryを採る。source/raw/親/acceptance/fixture/通常P出力の既存比較を取り除かない。最終gateは新audit保全flagとP/C別の入力保全flagを明示必須とする。

`run-receipt.json` に二票それぞれの full file pin と registry/before/afterの全pinを載せる。全REPORTの除外は従来の `envelope-inventory-before-run.json` / `run-receipt.json` の二件だけで、二票・全history copy・全取得ledgerは除外しない。全fixture raw/hidden/空dir、三比較、inner ZIPの明示dir/全entry再読/hash/CRC/EOF、両uploadが同じREPORTを指す条件を維持する。新WFの保持は両方30日。

## F9. 最終 CLI・自己点検・旧版との差分

本Pは同15 root＋acceptance、`--output REPORT/output --batch-size 128 --max-seconds 5400 --max-memory-mib 7168` でfresh一回。Cは同15 root＋acceptance、`--candidate-root REPORT/output --output REPORT/checker-result.json --max-seconds 10800 --max-memory-mib 7168 --producer-max-seconds 5400 --producer-max-memory-mib 7168`、batch-size引数なしで全新payload一回。外側6000/11400秒・job330分は上限であり、時間予測ではない。新自己試験は各 `--selftest --selftest-root REPORT/selftest-fixtures/P` または `/C`、内300秒/7168MiB・外360秒、Pだけbatch-size128。新二群の全fixtureを保存し、歴史三群を追加再実行しない。

全文静読済み旧WF v2を基点に、新登録部分・新registry全字段・追加10関数・変更12関数・YAML tailを自己静読した。ASTではなくテキスト上のtop-level `def` 境界で旧67関数/新77関数を照合し、55本文が完全不変、削除0と確認した。変更12は source_mode/live_mode/command/execute/checked_execution/test_gate/post_producer/preservation_mode/coverage_receipt/final_gate/final_mode/main。追加10は公開registryとraw範囲・history保存・二票結合のmetadata helperである。

旧WFと新WFの全親env表、P_DEPS/C_DEPS/DATAと全completion/continuation/retained entry表の全文字列は完全一致した。新helper作成中に共有kernel射影の字段名を既存nested `source` / `first_line` / `last_line` へ揃えた。最終版で未受領None/未接続仮拒否/旧v2-run markerは残っていない。登録値128/127/771と履歴64/nonce32/SHA64幅を区別して全文検索した。

ローカル作業はsource/公開metadataの読取・整形・全bytes/hash照合のみ。WF driver、Python、AST、自己試験、数学、GAP、GHA、network、git、credential操作は実行していない。C本文を読まず、根拠はroot公開registryとpublic WFに限った。新run id/新成果/新rank/a(128)/速度は未観測である。

## F10. freeze と残る実行境界

作者最終WFを **283,886 B / SHA256 `6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f` / LF3601 / CR0 / BOMなし / 全ASCII / 末尾LF / 行末空白0** としてfreezeする。元WF v2は166471 B / `887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5`のまま、P3/C3もF1の全pinから不変を再確認した。

rootから受領したregistryを含む実装上の残件はない。新GHAのsource/runtime/AST・metadata16・P/C新二群・新P/C全比較・全保全は未実行で、rootの全静読と別WF監査の正式最終票を経た公開/GHAが残る。既存k64の受領/CV9と、新k128結果を混ぜない。UNKNOWNは保持し、同固定lambdaの前置長a(n)だけを扱う。新lambda oracle未計算、positive adapter未実装、grade2 NOT_DECIDED・full_A0=false・verified=falseの限定は変えない。

AUDIT_1041_VERDICT: WORKFLOW_COMPLETE_STATIC_ONLY_RUNTIME_AND_ROOT_RELEASE_PENDING
