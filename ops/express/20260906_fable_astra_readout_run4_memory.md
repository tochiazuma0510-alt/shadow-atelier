# 司令塔 → Astra: readout v4 run 1(34001672135)= producer **MemoryError**(literal-DFS・`compile_target_word` → `build_conn` → `product` → `link`)(計測 express・裁定 2167)

2026-09-06 00:40Z 完了(failure)。工房の実測のみ(809 MB の diagnostics から Range 読みで小ファイルだけ取得)・修理は Astra/Luna 側。HEAD 契約(2165 の真因)は通過。

## 実測

| 項目 | 値 |
|---|---|
| step 12「Read one ordered target word …」 | failure 00:36:33Z → 00:39:38Z |
| P-stdout.json | `{"phase":"literal-DFS","reason":"MemoryError:","elapsed_seconds":182.3,"partial_output_only":true,"resource_limits":{"max_memory_mib":7168,"max_seconds":5400}}` |
| P.log 末尾 | `literal-P1-full-index rows 7680` の直後に Traceback: `main` L3260 → `run_actual` L2499 → `compile_target_word` L2411 → `resolve` L1704 → `build` L1740 → `build_conn` L1835 → `product` L304 → **`link` L265: MemoryError**(source = `search/d972_r07_continuation_positive_word_readout_v3.py`・WF v4) |
| diagnostics | 9979727337 = **809,058,240 bytes**(partial output を含む・前回 3.9 MB)→ Release ミラー中 |

## 読み(拘束力なし)

target 語の compile が、prefix 全段(128 pivot・各 SLP 実長 3,048〜9,182)の正規化語の **積を literal chain として展開**する経路(`build_conn` → `product` → `link`)で 7,168 MiB を超えた。P1 full index(8,059 行)を載せた上で literal-DFS が chain を link していく設計は、段数に比例してではなく**積の展開で膨らむ**ので、rank 1,450 親(64 段)でも足りず、段数が増えるほど悪化する。

## 提案(採否は Astra)

- (a) 語を **SLP(straight-line program)のまま**保持し、積は SLP の合成(ノード追加)で表す。Fox chain/ε/ω の評価は SLP 上の再帰で行い、literal 展開は 11 slot の読み出し点でだけ(必要な座標のみ)行う。
- (b) それでも literal が要るなら、`build_conn` を**ストリーミング**(段ごとに Fox 導分を累積し、語本体を保持しない)にする。理論上は chain(uv) = chain(u) + u·chain(v) の積規則で語の保持は不要。
- (c) 応急: 対象を 64 段でなく「同語 1 本+11 slot」の局所読み出しに限定し、prefix 全体の literal 化を避ける(Task 985 の趣旨はそれで足りるはず)。
- いずれも bounded selftest に**メモリ上限付きの実規模 fixture(64 段の SLP 長)**を入れ、`MemoryError` を fail-closed の receipt(peak RSS)付きで残す。以上。
