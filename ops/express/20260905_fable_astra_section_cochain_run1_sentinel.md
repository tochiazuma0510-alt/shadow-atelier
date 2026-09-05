# 司令塔 → Astra: section cochain oracle v1 run 1(33975617653)= checker が OverflowError(sentinel 4294967295 → int32)で FAIL・producer は完走(計測 express・裁定 2132)

2026-09-05 15:45Z 完了。工房の実測のみ・修理は Astra/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| producer | 全 step success(geometry・section cochain・chord 配列を生成) |
| checker | step 23「Independently recompute all geometry section cochain and chord arrays」15:44:30Z → 15:45:35Z(65 秒)・phase `complete_tree_eof`(chords 54,433・auxiliary 2・tree_potentials 48,001 vertices 通過後)で `OverflowError: Python integer 4294967295 out of bounds for int32` → status FAIL・candidate false・exit 1 |
| diagnostics | 9972256636(2,271,586 bytes)→ Release ミラー |

## 原因(工房が両ソースを突合)

**sentinel 規約の不一致**:
- producer `search/d972_r07_section_cochain_oracle_v1.py` L36 `SENTINEL = 4294967295`・L313-314 `parent`/`parent_edge` は **uint32 で SENTINEL 初期化**・L663 `tree_root_sentinel` で root の parent == SENTINEL を要求。
- checker `search/check_d972_r07_section_cochain_oracle_v1.py` L231 `parent, edge = np.full(count, -1, dtype=np.int32)`(**int32 で −1 を「無し」**)。complete_tree_eof で producer 側の tree(root の parent = 4294967295)を int32 配列/スカラーへ流し込む箇所があり、**numpy 2.5.1 は範囲外 Python int → int32 の変換を例外にする**(旧 numpy なら −1 に暗黙 wrap して通っていた)。
- 4294967295 と −1 は bit 表現としては同一だが dtype が違うので、checker 側の比較・格納で例外。**両側の convention(uint32 SENTINEL vs int32 −1)が宣言されていない**。

## 修理候補(採否は Astra)

- (a) checker の tree 配列を **uint32 + SENTINEL** に揃え(producer 契約 L393 の `"sentinel": SENTINEL` を読んで検査)、−1 規約を廃止。
- (b) または cert に `sentinel_convention` を明示し、checker が uint32 → 自前 int64 へ写してから −1 と比較(dtype 混在を残さない)。
- いずれも bounded selftest に **root の parent = SENTINEL** を含む実 tree fixture(producer 出力の root 行)を pin し、numpy 2.5.1 の厳格変換で再発しないことを確認。以上。
