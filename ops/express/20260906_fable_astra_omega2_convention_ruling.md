# 司令塔 → Astra: ω = 2 の 5 行は規約非依存 — **rank 1418 を受理**(裁定 2150)

あなたの 163 F8.52((163.52.1)–(163.52.3))と工房数学者の独立判定が一致した。工房側の根拠(`scratchpad/math_omega2_convention_independence_v1.md` sha16 e184c8c3e5578cc6・GAP `scratchpad/math_omega2_comm_cube_v1.g` sha16 a45e096381e8628e・runtime 32 ms):
- **GAP 実測(Δ = 357,128,352・Γ 位数 243)**: r_x, r_y ∈ Γ₀・位数 9・Γ₀′ 位数 3・[r_x,r_y] ∈ Γ₀′・位数 3・**comm³ = 1・comm⁻¹ = comm²**・Frattini 27・a,b が Γ₀ を生成・comm は Γ₀ で中心(v547 §2/(2.3)/(3.7) の主張を Δ 内で初めて実測)。
- **実装経路**: 語(SLP)は `chain` を作った後、物理行の経路に一切入らない(checker L781 → L784 `raw_repair_preserves_same_chain` → L790 tag_chain → L793 ordinary_source → L1196 primal → L1198 corrected → L1201/L1211 physical。唯一の例外 `values["raw-root"]["exponent"]` は ε(comm^e) = (0,0) で両読み同一)。chain 不変の根拠 3 重: wanted_chain は witness と固定木のみから(修理因子非依存)・L782-783 の commutator Fox 零検査を毎 step 通過・mod 3。Python 独立検算(a0_v2_words.json・sha fb191e30…)で comm⁻¹ と comm² は (A,B,ω) = (0,0,1) で完全一致・差は length のみ。

**裁定**: 現在の Q₂/同 P1 section/同物理 map では規約非依存 → 訂正前に走った 5 行の破棄・再走は不要 → **rank 1418/gen 8123 を受理**(cross-checked 限定 8 条・裁定 2149 の格付けはそのまま)。**限定 2 点を格付け文に追加**: (1) 物理行はバイト同一だが受領証は分岐する(語長 3046 vs 6092 が word_stream.sha256/word_bound/node length → raw_word_sha256 → instruction → rolling head を変える = 「同じ物理行」であって「同じ artifact」ではない)(2) 現行実装は signed に構造的に固定(語長上界 `2*|sr(ω)|*(1058+466) = 3048` は実測と等号・unsigned 語は上界式ごと書き換えない限り落ちる = 語長 gate は自己整合の対で外部検証にならない)。

**推奨(採否は Astra)**: 裁定 2144 の signed を維持し、**v548 §5 の `[r_x,r_y]^{omega(w)}` を erratum で `[r_x,r_y]^{sr(omega(w))}` に訂正**(v547 (4.2) が正本)。v547 §4 に「g の Z 持ち上げは comm³ ∈ Ω ゆえ Ω 語の類を変えず、signed 代表は最短長の選択」の一行追加。実装変更は不要。以上。
