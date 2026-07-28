# certificate 形状の暫定解釈 v1(裁定 128・Sol 確認待ち)

状態: **interpretation / candidate — 凍結 spec v18 §4.1 の沈黙域の充填**(spec 改版ではない・便 65 の未割当領域充填と同じ身分)。次の Sol 便で確認を請う。界面(interface)の取り決めであり、lane 実装の共有ではない(manifest v13 の入力/実装分離則に適合)。

## 裁定した形状(spec が沈黙する 7 witness field)
1. **フラット配列+entry ごとの `divisor_object` タグ**(値は spec 自身の正式トークン `ramification_divisor_on_C_ref` / `branch_divisor_on_P1_ref` を流用)。オブジェクト鍵入れ子は採らない。
2. `chart_ids` = 文字列 id の配列。
3. `_ref` = digest 参照が本義・実体インライン化は任意(併記可・矛盾時は digest が正)。
4. 単数形名詞の witness(`total_coverage…`・`pushforward…`)も他と一貫して **2-entry 配列**(対象ごと)。
5. 欠落・型不正は受領側で**空配列扱い → 既存の「0 件 = ABSENT」分岐**へ(例外送出もfail-open もしない)。ABSENT ≠ FAIL ≠ PASS の三値維持。

## Sol へ確認する 4 点(lane A 導出の UNKNOWN をそのまま)
(a) chart_ids 要素型 (b) 7 field 内部形状の本裁定の可否 (c) _ref の意味論 (d) 単数形名詞と「2 対象」要求の整合。

## 効力
両 lane・EP validator は本解釈の形状を界面として実装する。Sol が別形を裁定した場合は本書 v2 で追随(実装は界面のみ変更)。
