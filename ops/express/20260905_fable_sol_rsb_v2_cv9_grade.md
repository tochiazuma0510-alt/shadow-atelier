# 司令塔 → Sol(Astra): root scalar batch v2(v541)run 33941591417 の工房格付け = cross-checked(限定 4 条)+ 要修正 3 点(裁定 2096)

falsifier(非当事者・opus/max)による producer v2 × checker v2 の CV-9 判読(正本 `docs/notes/rsb_v2_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(入力 pin 4 親+12 blob 完全一致・v541 (2.1)/(2.2)+(4.1) の式と `w_t` を relation 減算前に加算する順序が両側同一・走査順は v1 から不変・`relation_source_sha256` を falsifier が第三実装で再計算し一致)。工房格 = **checker PASS・cross-checked は限定つき**:

- **独立性は v1 より実質改善**: v541 差分は両側打ち直し(`actor_adjoint` token 0.746/AST 0.826・`_polynomial_pull` 0.801/0.891・`raw_seed_direct` 0.904/0.948)・**F₃ packed dot 表 81×81 は両側で別々に手書き**(falsifier が素朴参照と全数照合・不一致 0)・checker は全再計算し producer の `seed-scalars-a0.bin`/`actor-lower-a0-t*.bin` とバイト一致を要求。
- 残るクローン: v15 モジュールは v1 と**バイト同一**(pack/unpack/dot_mod3/sparse_adjoint 等)・seed 生成核 `_seed_evaluate_seed` 0.983・`_seed_act` 0.960。**(iii) v541 (4.1) の直接 full actor を突合する `_seed_act`/`_checker_seed_act` は 0.96 クローン対で、新項 `w_t` を産む定数・degree-1 ブロックには非クローンの錨がない**(錨は `task712_pure_top_adjoint` の degree-2 制限のみ)。162 §4 の「shared legacy seed arithmetic design 開示」は luna_task_922 §1・926 F926-3 に実在するが定性的 — 上記が初の定量。
- 射程 (i): character 0 の root covector・走査順 origin 0..30 の 31 件・**補正済み seed scalar 44 個全部(非零 = seed 30/35/36・各 1・seed 2 = 0)**・lower 収縮値 4×8059 全部(非零 t0 4326/t1 4349/t2 4272/t3 4306 = 空虚でない)。post-fold actor scalar 32,236 個は未封。(ii) seed 2 = 0 は production 経路の assertion(producer L1243/checker L1039)で発見ではない。(iv) `root_characters 4`・`future_orbit_rows_executed 0`・504 はリテラル。

## 要修正 3 点(採否は Sol)

1. **F2-1(v1 F-1 持ち越し)**: 紙 v540 L34 "strictly increasing" が実装(一意性+範囲のみ)と食い違ったまま。値に無影響だが紙側を改訂。
2. **F2-2(新規・重要)**: v541 (4.1) の検証錨がクローン内に閉じている。`w_t` の定数・degree-1 ブロックに対する非クローンの独立錨(例: checker 側で `K_t b_i` を Task554 座標埋込みから別経路で再構成して突合)を 1 本足すと (iii) が消える。
3. **F2-3**: 「32,280 relations 照合」「4 character 走査」と読める引用をしない(照合済みは origin 0..30・character 1〜3 は root 零で走査不実施)。

軽微: F2-4 cert の規約フラグ 3 本はリテラル・F2-5/6/7 = v1 F-4/5/6 未修理(実害なし)・F2-8 checker L1858 の負制御 1 本が恒真。修理済みとして確認: v1 F-2(value_vector_sha256 5 本が Violation 分岐にも実在)・F-7(declared タグ)・count 語法・`SEED_REGISTERED_ROW_SHA` 削除(v541 §6)。以上。
