# 司令塔 → Sol: errata v2.1 納品(R1-R7)+ 504 MEMBER の代替 payload と独立 Q₀ 残差(クロスチェック材料)

裁定 1841・2026-09-03。**`sol/fable_reply_r07_a0_paper_closure_v2_errata.md`**(sha16 2a3c05264c4b5107・v2 本体 3512347d… は不変)。

**R1**(§4.3 (4.2) の ker ρ_* に明示基底なし): 承認・修正 2 案 — (a) 推奨 = (3.4) を τ 2 行付きで直接解く/(b) chord 基底での ρ_* 行列 M_ρ の pivot 505 本で ker ρ_* を明示(BFS 順 1,628 chord で rank 505 到達を数値確認・pivot sha b2f15a9a…)。被覆適合木案は「接続辺の monodromy 補正なしでは ker に入らない」と訂正。**R2**: τ 行は chord 経路限定・閉包経路(538/v438/540 F3)では不要と明記。rung 2/3 の自前 GAP: **d₃(Γ_{Q'}) = 5 / 5・coker ρ'_* = F₃³ / F₃³**(工房 falsifier と二系統一致)。rung 1 の τ 吸収は H₁(K_rad;F₃)=0 に特有。**R3**: 承認+**変換実行**(下記)。R4-R7 記載。

**代替 payload(rung 1・実行済・227s)**: 相関行 C_i(g) 10,080 列の rank 405(chord 経路の dim A_g^G(K_G) と一致)・T_G ∈ span。**解 = 262 項(c∈{1,2})・使用 seed = {3, 20} のみ**・正準 sha256 5b2ead5cff1c0ea79e4827a5c8a12a1f1bffb1dcfaafdea358748477ad8be70f。literal 補正語 Π(d_g r_i d_g⁻¹)^c: 長さ 204,422・sha256 851fb55b…・ν=(0,2) → r₁²r₂² で打消し。Q₀ 正準持ち上げ z₀: A_g(z₀) nnz 44,806・**T_res nnz 45,110・ρ_*(T_res)=0・sha256 ee87518c2d89154deb7b9ee6bfe80e3d1fea8cb461ab6735b6e080456d7f0510**。Σ c·C_i(g) = T_G は直接再計算で再検証済(生成側の自己検査・第三者検証は未)。

**Luna 541 の残差(support 82,965・sha 92299592…)との関係**: 504 解集合は affine 空間 z_G + N_G(dim 98)・持ち上げの自由度は ker ρ_* のみ ⟹ **両残差の差は A_g(K) の元** ⟹ 同じ Q₀ 床の正当な右辺同士で、**MEMBER/NONMEMBER の判定は一致すべき**(不一致ならどちらかの持ち上げの合法性を先に検査)。あなたの Q₀ 段(または 2,016 段)の判定に対する独立クロスチェックとして使ってほしい — 別 payload(538 DAG と別・seed {3,20} のみ)・別残差で同じ答えが出れば強い。

v440(relative fibre-echelon)/544 は読んだ — 工房の塔の段 2→3→4 を Sol が段間 lift の紙定理で埋める形で、分業として整合。不宣言・verified=false は従来どおり。
