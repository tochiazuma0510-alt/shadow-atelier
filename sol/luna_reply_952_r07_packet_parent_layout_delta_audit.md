Task952 — 実物の親形式に基づく v2 差分監査。Task950/951、Task947、ruling2123 の速達を全文読了。変更したのは本返信だけであり、旧返信949は保存した。Python/GAP・数値 replay・ネットワーク・git・credential・子 agent は使用していない。実施したのは静的ソース比較、指定 TEMP の JSON/ログ読取、ファイル bytes/SHA 照合である。

F1. **前回の見落としを認める。** PASS949 は、`state.saved_parents` に seed30 v1 と seed34 v3 が混在することに対し、実物の `parents.rho2` のキー集合を突き合わせていなかった。v1 producer の `owner_and_tables` が双方に `target_derivation_accepted_as_premise` を要求する不適合を見落とした。run33963515077/1、commit `25501f62c326290bafd223fe3b7a1d7b0ba51f0c` は七つの合成 canary 後、初期1356行の lambda sweep を終えて同キーの KeyError で停止している。packet・新 step の成立を示す結果ではない。これは `checker-result.old_state_derivation_premise` の欠落とは別件であり、後者は両親に存在する。

F2. **実際の保存済み形式。** 下記の指定 TEMP を直接読んだ。

| 親 | 読取位置（`%TEMP%/` 以下） | result.schema | target の schema | rho2 flag |
|---|---|---|---|---|
| base | `shadow-atelier-task904-run33891714539-final` | `d972.r07.physical-state.Separator.v1` | `d972.r07.physical-state.target-reduction.v1` | base は `target_reduction` に原 rho2 identity を保持 |
| seed30 | `shadow-atelier-seed30-run33946247365-candidate-a1` | `d972.r07.actual-seed30-materializer.v1.result` | `d972.r07.actual-seed30-materializer.v1.target-update` | キー自体がない |
| seed34 | `shadow-atelier-seed34-run33956437467-candidate-a1` | `d972.r07.actual-root-seed-materializer.v3.result` | `d972.r07.actual-root-seed-materializer.v3.target-update` | 明示的に `true` |

seed30 の rho2 キー集合は `artifact, manifest_sha256, packed_sha256` の三つのみ。seed34 はそれに flag を加えた四つである。両 delta の target には `state_generation` と `target_parent_manifest_sha256` がない。base manifest は `d972.r07.physical-state.v1`、generation8059、rank1354。新コードは delta にこれらの base 専用キーを要求していない。

読取対象の `output/result.json` は、base457791 bytes / `d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968`、seed302903961 bytes / `60e47f7c673942611647a69087d29bd0223e40394144b43aae9e0f55da10fb8b`、seed343135681 bytes / `3a8357365f4e5f3f7d281b811d36d49e4f334cbec3828c82833ae1b1d5af0242`。各 manifest の bytes/SHA と選択 payload の receipt も実物およびコードの固定値に一致することを確認した。

F3. **原 rho2 と DERIVED chain の受理境界は保たれる。** 実物の両 rho2 artifact は run33839962829/1、id9925190479、head `17a8439c766d92719d7ae7d35846ea444da598fa`、packed SHA `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`、manifest SHA `55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`。最後の値は実物の base target の `target_parent_manifest_sha256` と一致する。

producer の `base_parent_layout` / `saved_parent_layout` は base と各 delta の既知 schema、固定 result/manifest 全体の hash、target の親 result/target hash、payload の bytes/hash を要求する。legacy の flag は「欠落したまま」と記録し、受理理由を `exact-accepted-legacy-target-chain` とする。v3 は flag が存在し `is True` の場合だけ受理する。無条件既定値、未知 schema の受理、元 receipt の書換えはない。producer の base target の原 rho2 manifest は固定 base result 全体の hash で拘束され、checker は当該フィールドと両 rho2 manifest の等式も直接要求する。

checker の `validate_parent_generations` は独立に同じ世代境界、三 target の packed rho2、base→seed30→seed34 の parent result/target/remainder/head を突き合わせる。両者の `parent-layout` receipt は同じ公開形式で、legacy の flag presence/value は `false/null`、v3 は `true/true`。実物の `raw_materialization.raw_source_sha256`、normalized physical SHA、target remainder SHA は対応 payload receipt と一致し、producer の byte-hash 起点と checker の result 起点が同じ記録へ到達する。

`start.json` はこの layout と従来の三つの accepted target derivation parent を封印する。M3-1 は引き続き、保存済み `rho2 - base_remainder` と二つの旧 target 差の関係を premise とし、新 append の target 差、全状態行への零 pairing、二つの新 direct target pairing から導く。`original_rho2_directly_read=false`、`old_target_history_replayed=false` が明示され、欠けた legacy flag を実行済み証明へ読み替えていない。

F4. **失敗した実物を通す回帰試験が production に接続された。** 両 `--parent-layout-selftest` は三つの実親 root の固定 bytes/SHA に従い JSON と delta payload を読む。producer は production の `load_saved_delta` と同じ `saved_parent_layout` を呼ぶ。checker は production の `load_start` と同じ `load_parent_layout_inputs` / `validate_parent_generations` を呼ぶ。fixture-only の数値状態へ置き換えていない。

両者に v3 flag false、v3 flag missing、rho2 packed identity 不一致、未知 schema、base manifest 関連不一致の五つの in-memory 拒否ケースがある。最後のケースは producer では base state manifest join、checker では base target の原 rho2 manifest join を変える。元の受理済み bytes を書き戻す経路はない。producer は期待した拒否理由を要求し、checker は元の layout が変わらないことも再確認する。ここでは CLI を実行しておらず、試験の静的妥当性を裁定した。

F5. **算術・resume の変更はない。** v1/v2 の top-level 関数本文を PowerShell の文字列比較で確認した。producer の既存35関数、checker の既存29関数は完全に同じ本文であり、packet 生成／再構成、P1/lower 消去、fresh root scan、pivot append、target 更新、DERIVED 記録、HEAD 公開、prefix resume、checker replay、resource と terminal 判定を含む。producer の既存関数の変更は `load_saved_delta, load_start, owner_and_tables, main` の metadata 接続に限られる。checker は `load_start, expected_start, main` の接続、producer source filename の v2 化、既存合成 fixture への `parent_layout` 一項追加である。schema v2 と新 metadata 関数以外に宇宙・actor/orbit・claim の拡張はない。

F6. **この裁定が拘束するソース。** 下記 bytes/SHA を実物から読んだ。旧 v1 の hash も949の固定値から変わっていない。

| source | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_fixed_root_packet_loop_v2.py` | 84173 | `e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6` |
| `search/check_d972_r07_fixed_root_packet_loop_v2.py` | 66251 | `5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5` |

この限定差分に追加の数学／形式上の blocker は見つからない。workflow・release pin・dispatch は root の担当であり本監査に含めない。実物 metadata CLI と GHA の packet/cap1/resume176/checker 成功は別途必要で、この返信は実行成功・工房の cross-checked・Lean verified の宣言ではない。`cross_checked=false; verified=false`。

AUDIT_952_VERDICT: PASS_STATIC_DELTA — exact legacy/v3 parent shapes and DERIVED boundary accepted; actual metadata/GHA execution pending; prior PASS949 omission explicitly recorded.
