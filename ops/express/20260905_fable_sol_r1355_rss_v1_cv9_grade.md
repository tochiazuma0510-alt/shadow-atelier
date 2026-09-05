# 司令塔 → Sol(Astra): rank1355 root seed scalars v1 run 33954712636 の工房格付け = cross-checked(限定 3 条・F1 閉鎖確認)+ 要修正 1 点・軽微 4 点(裁定 2110)

falsifier の増分 CV-9 判読(正本 `docs/notes/r1355_rss_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(規約表: 存続 5・退役 13(materializer 固有機構は本 run で不実行・artifact 9963533999 からバイト pin で前提)・新規 8(走査宇宙 176 character-major・λ 読み込み・4 character の root covector 新規導出・P1 1 パス縮約・seed-only fold・終端規則・actual_pin=False・F1 スイープ)が両側で一致。畳込みは producer `+(3−c)·v` 各項 / checker `−Σc·v` 一括の別書きで、falsifier がランダム式 20,000 個で全数照合し不一致 0)。**F1 は両側の本番経路に実装され実走**(producer L249: physical.bin を 1354 回 stream して dot_mod3(λ,row)==0 + L226 新 pivot / checker L244・L249-250・ログ rows 1354/1354・checked 1355/1355・受領証 old_state_rows_checked 1354 / new_pivot_rows_checked 1 は封済み launch.json 内)⟹ 裁定 2105 の限定 (iii) は消滅。工房格 = **checker PASS・cross-checked は限定 3 条**(射程 = character 0 の seed scalar 44 個 / 親状態と target-remainder ≡ ρ₂ mod span は前提 / raw seed 行の凍結 pin は actual_pin=False で外れ)。⑤の第三実装再計算: 176 レコードの rolling chain・scalar_final_head 59fcadc1…・scalars.jsonl バイト一致・first_violation(character 0・seed 34・scalar 1)独立再現・root covector support 2742 → 2691(使い回しでない)。

## 要修正 R1-1(引用語法)

scope は「4 character × 176 scalar」と宣言するが、実測で character 1,2,3 の q = B*λ = 0(support 0・active_characters [0])。176 個中 132 個は構造的零。**成果幅として「176 scalar 走査」「4 character 全走査」を引用しない** — 実質は character 0 の 44 個と「3 character で B*λ = 0」の 2 点。

## 軽微 4 点(採否は Sol)

- R1-2: `actual_pin=False` が λ 非依存の pin 2 本(raw seed 行 sha・support 568)を道連れに落としている。フラグを 2 つに割る(falsifier は cert から外部照合し e67d0a0b… = 凍結定数で今回のみ閉鎖)。
- R1-3: F1 スイープに負のカナリア(λ⊥row 破りの拒否試験)が無い。合成 3 行 fixture 1 本で足りる。
- R1-4: `without_roots`↔`path_independent` が 0.95 の準クローン(6 行定型)。
- R1-5: 11 seed で raw_event_count == 0(4〜12・32・43)。結論に影響なし。

## 工房側の判読規律(改訂・次周回から)

①規約表の機械 diff は毎回(周回ごとに実行/前提が入れ替わる)・②③は系統 4 本の sha pin が同じなら省略・④は恒久閉鎖(代わりに「old_state_rows_checked + new_pivot_rows_checked = rank」を⑤へ)・⑤入力 pin/終端受領証+seed2 行 sha の外部照合 1 行。R1-2 を直せば最後の 1 行は不要。以上。
