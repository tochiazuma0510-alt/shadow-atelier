# Task1006 — 同語 D v3 の path 結合と旧 target schema 点検

**F1 — 完了範囲。** Task1006 を全文読了し、指定の新 D v3 を作成した。旧 D v2 の producer / checker path をそれぞれ v3 にする二 literal だけを変更した。新 P v3 本文・Task1005 作者票・新 workflow の数学定数は読んでいない。P の全 bytes / SHA は root が実 pin を公開した後、既存 acceptance.consumer_sources の完全 descriptor 照合で受ける。未観測の P pin を作成していない。

着手前に Task1004 を Task995 へ保存した。995 の中断境界は search/check_d972_r07_fixed_lambda_cycle_batch_v1.py、169824 bytes / SHA256 65aad639896ad5f5366f8d2e41c453cb43e47e4c671b116af92148c4f2f90a42、LF2519。完成済 batch の旧 result / invocation / elapsed は旧受付に結び、今回の C 受付票と分離する。この短便の保存後、995 の残作業へ戻る。

**F2 — 新旧 source と全差分。**

| file | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_continuation_same_word_eleven_slots_v2.py（旧、不変） | 176579 | 865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v3.py（新） | 176579 | 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c |

両版は LF2636 / CR0 / BOMなし / final LF。変更は L1066 の search/d972_r07_continuation_positive_word_readout_v2.py → search/d972_r07_continuation_positive_word_readout_v3.py と、L1067 の自己 path v2 → v3 のみ。各旧 literal の出現が一回であることを確認し、新版をこの二箇所だけ逆置換した全 bytes の SHA が旧版 865ed6a5… に完全一致した。.NET の UTF-8 文字列・bytes 比較と SHA 計算で確認し、Python / import / AST は使用していない。新 source はこの pin で作者側の編集を終える。root / Task1007 の静的読了と release は別工程である。

wire は L56 の d972.r07.continuation-same-word-eleven-slots.v1、L57 の d972.r07.continuation-positive-word.v1 を保持する。新 P の修理を D 算術へ写した変更はない。

**F3 — 旧 refinement / seed30 / seed34 の実 schema。** D v2 の AcceptedInputs.read_selected（L1077–1139）、PhysicalRecipes の全旧行 intake（L1556–1667）、target_parent_history（L2304–2372）、compare_target_history（L2375–2433）、最終 manifest / result / main 接続を静的に読んだ。全 target_remainder_sha256 の参照も検索し、どの親の HEAD / snapshot / step を読むかを区別した。

refinement の保存 HEAD を %TEMP%/shadow-atelier-full-origin-completion-run33971897879-candidate-a1/output/HEAD から実読し、921 bytes / SHA256 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba、completed_steps=26、target_remainder_sha256 字段なしを確認した。D の当該 HEAD 読取は L1589–1590 の completed_steps=26 の確認であり、不存在の target 字段を読まない。

refinement の各行は保存 instruction.json / result.json / physical-normalized.bin から採り、L2315–2320 で result.target.parent_remainder_sha256 と直前 remainder、同 remainder_sha256 とその段の target-remainder.bin 全 file pin を結ぶ。最終第26段は instruction db5327c34a6447220a4309bd4f606a9372849977221bb1c290730c53df52ddc9、result 45588d8b319fe4c3497bb9ae6d7768119711aa2c8779779945bdf5fcbf78edd7、target packed 111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad を実ファイルの SHA と照合した。これは保存 metadata / hash の点検で、行の数値再生ではない。

後着の公開 Task1008 も全文読了した。root が独立取得した ZIP51943596 bytes / 0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8 の実 metadata と上記四 entry が整合する。最終 manifest 1932 bytes / 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c を指す HEAD の字段は step_manifest_sha256 であり、target を HEAD へ後付けする変更はしていない。

seed30 / seed34 の保存 result.target は旧入れ子 object で、どちらも old_remainder_sha256 / remainder_sha256 / scalar を持つ。D は L1580–1581 で両者を legacy-seed として読み、L2317 の親字段を old_remainder_sha256 に分岐する。実保存 target packed は seed30 f5040e3f29b42e71b86be047d40de5d538ddb7fc107cace219879bbc67238d3a、seed34 46a6b8281587a13236fd9af00eab9825a2d956dd878613af14182b5f9ae94c49 で、各 result.target.remainder_sha256 と一致した。新しい plain target 型へ置換せず、両世代を履歴から除外しない。

read_selected の HEAD target 参照は明示的に continuation 役の新 CEGAR HEAD へ限定される。そこでは最終 committed step / 実 packed target と結ぶ。全 named target history は base → 二 seed → packet3 → refinement26 → external E → 全 continuation 段の順で、最後にその selected HEAD へ閉じる。Separator の DERIVED object と Linear の null lambda_rho2 分岐も保持する。以上の読取に今回の不存在字段と同型の欠陥は認めず、追加 source 修理は不要だった。

**F4 — 数学・試験・未実行の境界。** 二 literal 以外の全 bytes が同一なので、同じ root の ordered word / 十三 file / 全 Ref 元 recipe / 十一 E3・E4 slot / full80644 / fresh rho2 実読 / 非単元 Act / 全 EOF / 全16親 / 資源上限 / 全 false 境界と、既存三群 selftest は不変である。一般 target 語へ source-lower96776 零を追加せず、現 PB4-dropped grade と full P / A0 の条件を混ぜない。grade2_member / grade2_nonmember は NOT_DECIDED、full_A0 / verified は false のままである。

run33999045563/1、head a324e4b44e3d24def59c901f2dbee758f04369fd の source / 全親 / 全64履歴 / metadata / P4 / D3 canary PASS後に本 P が停止し、D 本走は skipped という事実は root 配達の実観測として記録する。本 D v3 の selftest / AST / import / 数値本走 / GHA は未実施であり、旧 D3 成功を新版本走の成功へ読み替えない。ローカル network / Git / credentials / GAP / 新 agent も使用していない。commit / push / GHA と実 run の記帳は root が行う。

AUDIT_1006_VERDICT: SOURCE_PATH_ONLY_COMPLETE; OWN_OLD_TARGET_SCHEMAS_STATICALLY_CONSISTENT; ROOT_TASK1007_REVIEW_AND_GHA_PENDING.
