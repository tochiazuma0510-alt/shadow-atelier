# Task998 — 同語readoutのWF-only v3・全相対path順の修理

宛先: 既存packet_producer。Task994/997の保存境界を報告してから本便を先に完成し、その後994へ戻る。
変更可は新 .github/workflows/d972-r07-continuation-positive-word-readout-v3.yml と
sol/luna_reply_998_r07_positive_readout_inventory_order_v3.md のみ。P/C source、全v1/v2、凍結991–993を変えない。
sourceの実装変更は本便に含めない。ローカルPython/import/AST/数値/GAP/network/git/credential/新agent禁止。
rootだけがgit/GHA broker。999が独立差分監査する。

## 1. 観測した失敗と境界

実v2 run33997745566/1、head c6278fe1365f447b6183600e446f36defef80e76、job101391117505。
source/runtime/16live全ZIP/64全履歴入場は成功。P4/D3の新interface canary全七群は実PASS。
P本走23:07:42Z–23:07:43Zでexit1、保存P-stdoutはreason=ValueError:unique_sorted_files、elapsed_seconds=0.265004。
P.logでstate/delta/seed34/packet/refinement入場済み、oracleのfiles順で最初に拒否。word/Dは未形成、D本走skipped。
これは元startや数値親の変更ではない。WF v2 scan(root) 567–579が sorted(Path) のcomponent順でfilesを返し、
P v2の637–639は完全な相対POSIX文字列順を正として比較する。両者の不一致が実受付に存在する。

rootが診断をwhole ZIP照合・安全展開済み:
- artifact9978580135、name d972-r07-continuation-positive-word-readout-v2-diagnostics-33997745566-1、
  3919059 B / 14951bde6ccf8a0bbf05587be8f0929ea146266b9d74661e60b9e14247a73f4f。
- TEMP root shadow-atelier-positive-readout-run33997745566-diagnostics-a1、162file/18503891 B。
- P-stdout.json 501 B/a5c248537a4e4f80a9fe503fea57418534dc94a63cbf97f696a52be710ecfb2d。
- P_SELFTEST-stdout.json 2256 B/34735ea19a3bbe8214eedf4f5e99b86245c08ef40d43991c73737f4155f91eb7。
- D_SELFTEST-stdout.json 678 B/7ca09522e6f3955fdde2281a7acb0fbb08d3e198f76f30702ad213587decc3be。
- new-canary-result.json 1508 B/615beda80c792a0e1dab1267c40e072072e96c4ea9c1ee4c597a8e2abf761ca0。
- preservation-result.json 893 B/5268e4bf4ce62eb87e13089de5a2c1542c27b4554d97d554212f533f4426d620。
  全16親/取得済みsource/raw/acceptance/driverは不変true、word/D不足だけINCOMPLETE。前回の早期保存修理は働いた。

実acceptance.filesの初不一致（0始まり）:
- oracle 64fileのindex58: 観測repair-source/check_...、文字列順はrepair-source-receipt.jsonを先にする。
- task712 50fileのindex0: 観測r07-grade2-maps-v4/B_adj_a0.jsonl、文字列順はr07-grade2-maps-v4-checker.jsonを先にする。
- continuation 7916fileのindex41: 観測accepted-completion/original/artifact-...、文字列順はaccepted-completion/original-cegar-run.jsonが先。
親filesを削る、P/Cのsorted/unique条件を緩める、旧artifactを書き直す修理は禁止。

## 2. 最小修理・静的契約

v2 WF全体を新v3へ引き継ぐ。source P/Cはv2のまま、全同16数学親/各全pins/全64履歴/原start/同語13file/11slot/80644/全budgetsは不変。
scanの返値だけ、filesをentry.file完全文字列で、directoriesも完全文字列で整列する。symlink/safe-name/regular/全EOF/全hashは維持。
new admission/before/afterを同一のcorrect scanで作り、古い保存inventoryを修理済みとして書き換えない。
source自体の数学/reader/header/CLIを変更しない。WF名/path/schema suffix/marker/uploadはv3にし、
markerは [r07-continuation-positive-word-readout-v3-run]。既存 branch/checkout exact head/read-only credential/alwaysを維持。

今回見逃したworkflow→P/Cの境界にproduction直結のmetadata canaryを追加する。
新scanと同じ整列/重複/整形検査helperを本番にも使い、小さな一時filesystem fixtureをGHA上で作る。
通常fileと同prefix directory、'-'と'/'の逆転、複数階層、uppercaseを含む例を全file/dir/bytesで照合する。
component順のlist、directory順の乱れ、duplicate file/dir、別size/hash等の拒否をactual helperにつなぐ。
全実16roleでも、scan完了後に同じ文字列順/unique/descriptor型検査を通してから受付へ載せる。
fixtureはREPORTの専用診断領域へ置き、数学親やword成功rosterへ混ぜない。新metadata群は300秒以内。

同七interface canary stepはWF本走との結合を今回再確認するため保持してよい。v2七群は既に実PASSとして区別し、
v3を初回成功や旧数値suiteの再走とは記さない。新旧どちらのcanaryもGHAのみ。
旧数値sourceの全success suiteを追加しない。新metadata結果をfinal receiptへjoin、失敗ならcandidateを出さない。

## 3. 来歴・診断・完成票

v1 int/bool失敗の来歴を保持し、v2実失敗run/head/ZIP/源/WF pinsと七群実PASS/未実行Dを新repair metadataへ追加する。
これは診断来歴であり第17数学親ではない。診断ZIPを新mathematical acceptanceへ差し込まない。
alwaysは取得直後/入場前baselineと全afterの個別保存、partial不足INCOMPLETEを維持。
全source/runtime/実start/全親/完全before-after/word-D比較の成功条件を緩めない。
WF全差分を静的に読み、変更区分、source/全親pins不変、新metadata群のproduction接続と射程、未実行を返信へ書く。
WF bytes/SHA/LF、既存P175318/cf6ac987...、C176579/865ed6a5...の不変を報告。最終行 AUDIT_998_VERDICT:。
完成し999/rootが読了後だけrootが公開・新runを起動する。以後WF/返信は凍結し994へ戻る。
