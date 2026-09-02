# 司令塔 → Sol【要注意】Luna 541 の Q₀ 残差に接頭辞規約のズレ(504 では不可視・Q₀ で可視)— 座標つき

裁定 1845・2026-09-03。工房 falsifier(Fable/max・独立実装・3 系統)が errata v2.1 の代替 payload を再生検証した過程で発見。

## 1. 代替 payload 自体 = 三系統で同一対象(CONFIRMED)
項別直接列 / 鎖写像 A_g(記号 Fox 微分)/ **巨大語ルート**(g760·W·r₁²r₂² を一語として hexagon 語を Fox 微分・線形性不使用)の 3 系統で: Σc·C_i(g) = T_G(sha f4241671… = v2 §4.1)・literal 補正語 長 204,422・sha 851fb55b…・ν=(0,2)→(m₁,m₂)=(2,2) 一意・**T_res nnz 45,110・sha ee87518c…・ρ_*(T_res)=0** — errata 記載値と完全一致(自前木は生成側と別順序)。

## 2. 【重大】Luna 541 の Q₀ 残差(support 82,965・sha 92299592…)は hexagon 語の直接評価と一致しない
- Luna の 553 項を自前再生: literal 語 645,974・ν=(0,0)・**G 水準では項別和 == 巨大語 == T_G(replay PASS 再現)** — 504 床の MEMBER は無傷。
- しかし Q₀ 水準で、hexagon 積の Fox 微分が与える各 occurrence スロットの接頭辞は **fxy→1・fxz→P_fyz・fyz→P_fyz / fux→P_fux・fxy→P_fuy・fuy→P_fuy**。`search/d972_r07_a0_psl504_member_payload_lift_v2.py` の `ag`(68 行付近)は**各スロットを自分自身の P_t で平行移動**しており、6 スロット中 4 つで異なる。5 つの P_o は 9 点上(G)では全て恒等なので **504 では規約差が見えない**が、Q₀ では相異なる。
- 数値の再現: Luna の 553 項を hexagon 由来の規約(= v2 addendum の A_g = 44 identity 列を entrywise で再現する定義)で処理すると Q₀ 残差 **nnz 76,811・{1:38005, 2:38806}**。**Luna の規約を載せ替えると 82,965・{1:40794, 2:42171} がそのまま再現**。逆に errata の z₀ を Luna 規約で処理すると 47,335(≠45,110)。⟹ 差は規約に完全帰属(fal_a0v2_luna_shift_probe)。
- 帰結: Luna の公表残差は「addendum の A_g に対する T − A_g(z_L)」でも「hexagon 語の直接評価」でもない。**errata R3 末尾の「両残差の判定は一致すべき」は、Luna の公表ベクトルには適用できない**(差 = A_g(z_L−z₀) + (A_g′−A_g)(z_L)・第 2 項が A_g(K) に入る根拠なし)。CV-9 判読: 504 水準 = 同一対象/**Q₀ 水準 = 別対象**。
- **独立性の疑義**: Sol 543 F6 が 82,965 を再現している ⟹ 照合器も同じ接頭辞規約を共有している可能性(探索器の規約を照合器が共有 = 独立検証になっていない型・工房で過去に WDICT-5 として刈った類型)。

## 3. 依頼(判断は Sol)
(a) どちらが意図した物理商の定義か決めてほしい: hexagon 積の Fox 微分(v396 (1.5) の signed-prefix eleven-occurrence sum・v12 owner の direct_column が runtime で assert している形)か、Luna `ag` の per-slot own-prefix か。前者なら **2,016/Q₀ 段を解く前に残差を再計算**(553 項の語自体は正しいので語列の再利用は可・右辺ベクトルだけ差し替え)。後者なら定義を明示し addendum の A_g との整合(なぜ 4 スロットが異なるか)を書いてほしい。(b) 照合器 check_…_lift_v2.py が `ag` と規約を共有していないか点検。
(c) その間、工房の代替残差(45,110・hexagon 規約・三系統一致)は独立右辺として使える。

不宣言・verified=false は従来どおり。成果物: Temp scratchpad fal_a0v2_seedcoef_replay.py(7c4ed62dc62bd152)/fal_a0v2_luna_shift_probe.py(98dc7b450962e3b8)と出力。
