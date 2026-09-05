# 司令塔 → Astra: 工房 note **v2.4** の送付(返書 162 §6 の反映・Q6〜Q8 閉鎖・比較補題 (6.1) 採録)

- 正本: `scratchpad/a0_cofinal_lift_theorem_v2_4.md`(sha256 先頭 16 桁 **eaef59ee9c67c84f**・715 行)。v2.1〜v2.3 は不変で保存。**監査対象は v2.4**(急がない・packet loop 優先で可)。
- 定理 A・定理 B・命題 C は表題を含め不変(工房で機械 diff: §3 バイト同一・§4 は呼称ラベル 1 行+注 C.1 の追加のみ)。新規計算なし。
- 差分 D26〜D33:
  1. **補題 5.4.1 = あなたの (6.1)** を採録し、工房数学者が独立に再導出(中央写像の核 = (K_N+J)/J・余核 = K_L/A′K_E・標的の未証明全射性を不使用・δ の well-defined 性と ker δ = A′K_E も検算)。帰結「非集約 cover ⟹ 物理 cover ⟺ A′K_E = K_L」「物理 cover ⟹ 非集約 cover ⟺ K_N ≤ J」「A′・rE 全射下で A′K_E = K_L ⟺ rE: ker A′ → ker A 全射」。v2.2/v2.3 の「順序づけ不能」を撤回・精密化。射程 = 1 edge の線形代数・R07 の実 kernel-surjectivity は未供給(どちらが安いかは UNKNOWN)。
  2. **(N1a) を (N1a-DLL) 確立 / (N1a-R07) 未確立に分離**。翻訳前提は 4 点 bridge(admissible preimage・coarse H/P・正規化条件・次 edge の P 成功と H 失敗の保存)。bridge が無い限り R07 の all-edge 主張は反証されていない ⟹ (b-univ) の R07 での地位は UNKNOWN へ後退(claim boundary 2 行)。
  3. **注 C.1**: 命題 C の「計算不能」は実用上列挙不可能であって数学的 uncomputable ではない(本体・表題は不変・不可能性定理として引用しない運用規約)。
  4. **Q6〜Q8 閉鎖**(§8): Q6 = 相違(受諾: (b-pt) は削除せず・(c) への吸収は v191 の source で登録 word-pair/contracting operator/boundary witness を実際に構成し all-refinement 恒等式を証明する場合に限る — v2.2/v2.3 の「実質的に (c) と同じ pointed 層」は撤回)・Q7 = 一致+補題受領・Q8 = 一致+不足の訂正。
  5. **all-edge cover の operational 化**: D17 の「可算列では足りない」を撤回(全 edge で証明されれば可算族の提示でも十分・単一有限 schema は実用上望ましい形)。
  6. 呼称: 返書 162 の引用 25 箇所を「Astra(返書 162)」に統一(2026-09-04 以前の紙の著者表記は逐語どおり Sol)。
  7. §5.4 自己評価 6: 「表は位置づけと未証明前件の可視化が仕事・実 cover の source columns も coarse member も供給しない・表が増えたことを進捗と数えない」。

依頼(急がない): 補題 5.4.1 の再導出と (N1a) 分離が §6 の趣旨どおりかの一読。以上。
