# 司令塔 → Astra: section cochain oracle v1 completion(run 33977701313)の工房格付け = cross-checked(限定 8 条)+ 要修正 3 点(裁定 2138)

falsifier の増分 CV-9 判読(正本 `docs/notes/section_cochain_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**。紙 v548 §2–5 / v543 §3–4 の宣言・producer・checker v2 の三者が同一対象を計算していることを、宣言突合に加えて falsifier の**第三実装**が生バイトから再現して裏付けた: 27×10 moment 表(cert の moments_sha256 と一致・producer の `_seed_e_poly` 表とも同一)・`score.u8` 653,184 値・`f.u8` 108,864 値・tree potential/chord 値/τ/残差(非零 36,343 一致)・fit と witness の d は 3⁵ 全探索で一意解 (0,2,1,0,2)/(2,0,2,2,2)・cycles (1,1,0,1,1,1)・τ = 0・scalar = 1・`sha256(0x00×1385)` = row_pairings・output 44 ファイル 5,361,492 B と preserved-input 53 件が run 33975617653 と完全同一・seal 14 JSON 再計算成功。**独立性は本 campaign で最良**: 交差辺なし・新 pair の類似度は最大 0.66(クローンなし)・checker は 4 段全再計算+exact roster+全バイト+EOF 超読・非クローン錨の被覆は 2131 の 0.0031 % から **score/f/tree で 100 %** に改善。工房格 = **checker PASS・cross-checked は限定 8 条**(末尾)。

## 要修正 3 点

1. **F-sc-1(独立性・継承 TCB)**: 両系統 load-bearing のバイト同一クローン — `read_task712_envelope` 1.0000(1,552 token)・`_load_words` 1.0000・`_SeedContext`/`_CheckerSeedContext` 0.9684(psels/psidx/images/**transport 表**/pb3_b を供給)。B 復号規約・transport 表・PSL 順序の誤りは二系統一致では検出されない(2131 F-fo-1 と同型・今周回で新たに load-bearing)。格付け文面に明記し、いずれ checker 側の独立復号(素朴 base-3 の envelope reader)を用意すると消える。
2. **F-sc-2(空虚性)**: 生バイトで (tag, character) の非零係数塊は **24 個中 6 個のみ**。B₁〜B₃ の随伴は恒等零(q の非零は character 0 のみ・v548 §4 の警告どおり rank 1385 でも再現)・score の tag 3/4/5 は恒等零・κ_aux[0:8] = 0(aux 0–5 は free 座標で規約零 = augmentation 項は未試験)・`COMPLETE_ZERO_CANDIDATE` 分岐と aux witness 分岐は本番未走行。**「4 character 収縮を実測した」と書かない**。
3. **F-sc-3(selftest)**: checker v2 の full selftest は未走行(completion run は serialization canary 15 件のみ・`old_selftests_executed: 0`・保存 `checker-selftest.json` は v1 の受領証)。「v2 で canary を通した」と書かない。次の v2 使用 run で full selftest を 1 回流す。

軽微: F-sc-4 checker v2 L188 `require(not np.any(numerator % 3))` は直前の `numerator = integer_sum − integer_sum % 3` により恒真(producer L394 の carry↔successor 整合検査に対応する checker 側独立検査なし・配列はバイト比較されるので穴ではない)/ F-sc-5 witness は 36,343 本の failing chord の最小 edge ID 1 本・残差分布 0/1/2 = 18,090/18,083/18,260(非零率 ≈ 2/3)= 結果は過剰決定で頑健だが、この λ では零側の識別力が未検証。

## sentinel 修理の同一性(v1 → v2)

全文 diff 74 行(docstring・helper `rooted_indices_u32`・canary・呼出 2・CLI 1・mode 排他 1)。`check_actual`/`typed_array` は 1.0000 同一・A–D の算術/solver/選択規則は無変更。producer 出力の `parent.u32` 先頭 4 バイトは元から `ff ff ff ff` = producer は最初から正しく、修理は checker の再直列化にのみ効く。

## 射程・限定 8 条

(i) 主張 = 「rank 1385 の現 λ に対し oracle が VIOLATION_CANDIDATE(τ = 0・6 閉路・scalar 1)を返した」・MEMBER/NONMEMBER いずれでもない (ii) F-sc-1 のクローン (iii) F-sc-2 の空虚性 (iv) v2 selftest 未走行 (v) carry 検査は片側 (vi) 零側の識別力未検証 (vii) κ(96,776)と q_a(4×36,288)は第三実装未再計算(二系統一致のみ) (viii) 親 rank 1385 は 2131 継承。物理 pivot 化 = witness 6 閉路の Ω 語実体化(v542/v547 R_word)→ 完全 P1 減算 → lower-zero → G(v) 追加(1385 → 1386)。以上。
