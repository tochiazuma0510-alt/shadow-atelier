# Task968 — oracle checker の u32 root sentinel を修理し保存出力を照合

役: Luna checker/workflow。Task966を一時中断し本便を優先、完了後966へ戻る。
変更可は新 `search/check_d972_r07_section_cochain_oracle_v2.py`、
新 `.github/workflows/d972-r07-section-cochain-checker-completion-v1.yml`、
`sol/luna_reply_968_r07_section_oracle_checker_completion.md` の三本だけ。
公開済み959/960/961 source/workflow/replyは凍結。ローカル数値/Python import/AST/GAP、
network/git/credential/dispatch/追加agent禁止。source/JSON/byte/hashと指定実装のみ。

実失敗: run33975617653/1、headc57a722224320f9a573cfe84dea6979df5cb5320、
job101331666867、2026-09-05T15:45:37Z failure。producerは69秒で全A–D完成、
checkerは65秒後 complete_tree_eof で
`OverflowError:Python integer 4294967295 out of bounds for int32`。
v1 geometry_payloads L573/574 の np.where(int32-array, Python4294967295,...) が原因。
比較loopの前なので全array一致/PASSはまだ無い。candidate artifact無し。

root回収済み diagnostics: id9972256636、name
`d972-r07-section-cochain-oracle-v1-diagnostics-33975617653-1`、
ZIP2271586 bytes/SHA256 c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a。
実展開 `%TEMP%/shadow-atelier-section-oracle-run33975617653-diagnostics-a1`。
元workflow `.github/workflows/d972-r07-section-cochain-oracle-v1.yml`。

1. v1 checker80740 bytes/2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967
   を新v2ファイルへversion化し、root -1→公開u32 4294967295の型変換だけ修理する。
   例えばsigned int64へ広げて代入してからu32へ出す。元int32配列は変更しない。
   root以外の不正な負値、上限外indexを黙ってwrapしない。parentはN、parent-edgeは2N。
   新helperなら実geometry_payloadsから使う。ABI/schemaはv1の保存producer出力と一致を
   維持し、source arithmetic/solver/owner/start/result/selectionは変更しない。
2. GHAだけで走る少数のserialization canaryを追加。実production変換へint32 root -1と
   正indexを入れ、little-endian root bytes ff ff ff ff、非root保持、末端index、誤った
   負値/範囲/型の拒否を確認する。旧full selftestやproducerを再走しない専用CLIを付ける。
3. checker-only新workflowを作る。markerは `[r07-section-cochain-checker-completion-v1-run]`、
   同じsol branch。Task962の保存出力不変方式を必要な範囲で使う。
   旧12親と13番目の今回diagnosticをlive exact run/attempt/head/workflow/artifact/name/
   ZIP bytes/digestへ固定。元run conclusionはfailureを要求。全source/data pinsを認証し、
   producer73290/4e7546eb…は一回も呼ばない。Python3.13.15/NumPy2.5.1を要求する。
4. 元outputの全roster/file/directory/bytes/hashを保存し、source-receiptと原source.jsonを
   維持する。旧FAIL checker-resultはprevious-checker-resultへ分離。新checker-v2と
   新workflowのsource/実行receiptを別に追加する。元producer artifactと修理checker
   completion artifactのprovenanceを区別する。全output前後不変を機械で確認する。
5. 元metadata両経路canaryと旧成功canaryはこのrunで再走しない。新serialization canary
   →新checker一回（内部1800秒/外40分/job60分）→全stage/全top配列・JSON比較PASSと
   不変gate後だけcandidate upload。diagnostics always。旧算術loop/producer再走は0。
   新checkerはcheckpointを持たないためA–D全再計算を行うが、未完の必要checkである。
6. 実producer tree.jsonはaux=[0,0]、first_failed_chord12、selected[2,3,4,6,11]、
   residual_nonzero36343、witness scalar1。これは未照合の観測値であり、修理checker's
   期待値を数字のliteralで固定しない。rootから全entry pinを受け、実bytesで確認する。

主要実entry pins（全file hash）:
- checker-result.json315/e500b7fa0a5f4387c36d787999f438cea91189b9ea3fd8ec80e0830cb29173e0
- source-receipt.json2673/cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934
- output/manifest.json1430/7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639
- output/owner.json8419/6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322
- output/start.json48377/7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a
- output/source.json1246/af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac
- output/result.json13727/c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312
- output/tree/witness.json486/1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd

replyに最小source diff、実metadata gate、最終bytes/SHA/LF、残るGHA/CV9を記載。
SOURCE_MAP/P1/Connと工房2131七限定は不変。verified=false。
最終行 `AUDIT_968_VERDICT:`。最終source/workflow pinsをroot/969へ通知する。
