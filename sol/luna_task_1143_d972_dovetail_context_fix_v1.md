# Luna 1143 — dovetail RUN_ROOT context 修理（2237）

宛先: receiver_cost_repair / Noether。公開 workflow の限定実装修理。Sol/root が git/GHA の単一 broker。

裁定2237と `ops/express/20260910_fable_astra_2237_ack.md` により、job-level runner context 違反の修理は配置前 pin の express 通知後 notify-and-go 承認済み。研究 run34416548935 は別のR07 v6本走で実行中。

入力を全文rawとして読む: `.github/workflows/d972-dovetail.yml` **60829 B / 21127ce22024310b6272bfd581c7362d959d3303eccab86bdb88168c9cc5c9c2**。診断 `ops/express/20260910_astra_d972_dovetail_context_diagnostic.md`、公式仕様 https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability を前提とする。

実装は TEMP/shadow-atelier-audit163/task1143/ の新規版のみ。作業ツリーで変更してよいのは `sol/luna_reply_1143_d972_dovetail_context_fix_v1.md` のみ。git/gh/credential/dispatch/source数学本文の実行・import・compileは禁止。P/C private sourceと他taskのprivate sourceは開かない。

厳密に2箇所のみ:

1. L43の `      RUN_ROOT: ${{ runner.temp }}/d972-dovetail` 行（LF込み）を削除。
2. `    steps:` 直後、checkoutより前に最初のbash stepを追加し、`printf 'RUN_ROOT=%s/d972-dovetail\n' "$RUNNER_TEMP" >> "$GITHUB_ENV"` で同じ実パスを後続全stepへ供給する。明示 `shell: bash`、名前は簡潔に。

全未変更bytesを保持。on/schedule/dispatch/input defaults、timeout330/300分・slice上限、親/manifest/schema/producer/checker/GAP worker、runtime、resume選択、保存/採択/緊急STATE_STOP経路、その他envと全数学bodyを変更しない。source内埋込みPythonを実行しない。現在の用途に必要な変更以外を足さない。

出力: 新規 workflow raw、2 editsのold/new base64+bytes/SHA/offsetと正逆EOF復元・未変更区間表、source/after format pin（LF/CR/BOM/EOF）、機械作成の小さなreceipt。本文には変更前後の行位置とcontext制約の理由、テストは原文の正逆raw一致で足りる旨、GHA実挙動はroot担当と明記。可能なら GITHUB_ENV 設定stepより前のRUN_ROOT使用がないことをmetadata検索で確認する。

返信最後: `LUNA_1143_VERDICT:`。rootは実別読後にpin通知・作業branch配置/pushを行う。本文・caps変更は依頼していない。
