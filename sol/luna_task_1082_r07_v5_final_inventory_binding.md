# Task1082 — Luna P/C: v5正式wholeinventoryの定数結合だけ

宛先: packet_producer（Pのみ）/ packet_checker（Cのみ）。進行中1081/1080に並行する短い定数結合。P/C私的本文の相互読取は引き続き禁止。Git/network/credential/source/Python/GAP/AST/import/compile/数学実行は0。rootが単一broker。

## rootの裁定と正式手渡し

2209 snapshotとexpressをroot全文受理した。旧v3ローカル空36dirの復元で足りる・artifact/数学/2206正式1706/8411格付け不変・v5全pins/独立別読/marker-name通知待ち、という裁定である。旧親は受理済v4 acceptanceの全目録から空36を復元し、前後全11437file/1267599138 Bをrootで再hash、全3475dir完全一致を閉じた。修復票4595/86b588eb3feaee2034235f8958e074d006f6926b4666cc119866cea4b242aaf6。

さらに実v4全11648fileをrootで改めて全bytes/SHA再照合し、保存envelope11646fileに明示の自己除外2fileを戻した全目録・acquisition全entry・現物全3525dirを完全一致させた。元3487 implicit dir＋認証空38も閉じた。正式全inventory票は TEMP/shadow-atelier-audit163/v4-run34120585268-final-parent-inventory-registration-v1.json = 7022/64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753。

登録値:
- files=11648 / file_bytes=1308094050 / directories=3525
- files_sha256=ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5
- directories_sha256=f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64
- 二つの正式canonical配列は同TEMPの v4-run34120585268-registered-canonical-files-v1.json =1931889/ffec515b… と v4-run34120585268-registered-canonical-directories-v1.json =200290/f9562484…。全SHAは上記。暫定票をそのまま正式扱いしたのではなく、今回全実fileを新たにhashし、保存全目録と再照合した。

旧1074のfull typed metadata受領はexit1のまま未完で、rootが同一helperで再実行する。全file/dir inventoryの登録と、全typed metadata本文の受領完了を混同しない。これまで両者をまとめて待機させていた条件は、2207/2209と今回の完全inventory実測に基づき、ここで明示的に分ける。P/Cの登録定数結合は許可するが、full typed metadata PASSを新設しない。数学格付けは工房2206限定7条へ依拠し、v5の実親入場/全source/独立Cを省かない。GHA発射は最終WF独立監査と全pins/通知を揃えたrootが行う。

## Pの範囲

基点 task1077/review-snapshot-v1/d972_r07_fixed_lambda_cycle_batch_v5.py =366388/135495b3203ba393fcceb5b22b74f5da5694849b67c0841ca4193d18ea56cba9。NEXT_BATCH_INVENTORY_REGISTRATION=None の一箇所だけをexact五key辞書へ変更する。新snapshotはtask1082-P以下、旧snapshot/source/返信1077は不変。指定返信は sol/luna_reply_1082_r07_v5_final_inventory_binding_producer.md。

## Cの範囲

基点 task1078/root-review-checker-v5-v1.py =335937/c868aa09a6dd6e94510f996080a8e3e0a7fea1563046486960c7b6a4fca55170。NEXT_BATCH_INVENTORY: dict[str, Any] | None = None の一箇所だけをexact五key辞書へ変更する。新snapshotはtask1082-C以下、旧snapshot/source/返信1078は不変。指定返信は sol/luna_reply_1082_r07_v5_final_inventory_binding_checker.md。

## 両者の引渡し

全旧/新raw差分（定数一箇所）、逆置換で元SHAへの完全一致、新全file bytes/SHA/ASCII/LF、全current raw区間index（metadataのみでWFへ共有可）、旧body/loaderの保持票の新offset、全材料pin、自己静読を保存する。最終constants以外の変更を加えず、必要なfindingは別途rootへ返す。1079作者と1081監査へ公開pins/rangesを通知してregistry/WF最終結合を進める。返信最終行は AUDIT_1082_VERDICT: を置き、局所実行0、新selftest未実行、root typed受領未完を明記する。
