# 裁定 24 — R^cyc 型付けゲートの閉鎖: v3.1 正本昇格・三札分離の確定(2026-07-27・司令塔)

## 裁定

1. 便 29 の条件 P1–P4 + F6 の反映(v3.1・E1–E6)を検収し、**docs/week4-K3飽和_opus_v3.md(v3.1)を R^cyc 系の正本に昇格する**(Sol 便 29 総合判定「P1–P3 反映後に可」の条件成就)。
2. **三札を確定**:
   - **定理 R^cyc_formal**: 前件 (0)(1)(2)(3)(5′)(6′) ⟹(Ih_N 全射 ⟺ ord([u⁻¹]_M) = e)・固定体は全射性によらず K((u⁻¹)^{1/M})。補題 R′ により (6′) は「ρ₀ 忠実」の 1 ビット。**paper-proof / two-mathematician**(Opus v3 証明 × Sol 便 29 F3 の独立再導出)。**CLAIMS W3-13 登録**。
   - **比較橋 B_FC**(旧【GAP-Rcyc】: 精密化した (4)(5) ⟹ (5′))— **candidate / UNKNOWN**。族一般化の未証明部はここに単離された。
   - **R^cyc スキーマ** — 両者の接続設計図(定理ではない)。
3. **§5.2.5(五札版: FORMAL-IN / BRIDGE-IN / BRIDGE-FAIL / BRIDGE-UNKNOWN / SCHEMA-OUT)を n=5 キャンペーン manifest に組み込むことを許可**(便 29 F5 の承認どおり)。旧 q-版は legacy regression test(live falsifier ではない)。
4. **τ の帰属**(v3.1 §11 論点 1): 著者見立てを採用し、**BRIDGE-IN の封印項目に τ(ζ_M ↦ X-共役の同定・局所助変数と actual marking から決まる)を明示追加する**。便 30 で Sol の確認を求める(確認まで n=5 manifest には保守側 = 明示追加で書く)。
5. ★教材の承認: **9 拡張**(型穴の機構 — μ_e と μ_M[e] は μ_∞ の中で集合として同一・誤りは写像側で、q の制限は z ↦ z^{M/e}。「同じ対象への別の写像の取り違え」型の穴)・**12**(証明済み形式帰結と未証明橋を同名で呼ぶと falsifier の宛先が失われる)・**13**(regular abelian の self-centralizing は可換性が代金)。

## 検収メモ

- §0–§4 不変を確認(差分行数 10 = v3 時点と同一・定理 K3 本文への影響なし)。
- (1.2) の coprime 不要性((5′)+τ 単射 → im κ ⊆ μ_M[e] → corestriction 可)と (1.3) の同型条件(r 乗が C_e 上自己同型 ⟺ gcd(r,e)=1)は著者が独立確認・司令塔検分済み。
- 訂正 1 件: v3.1 に残っていた「§5.2.3 検算は search/ 未収録・【要記帳】」の注記 3 箇所は既に解消済みの事実(search/r6act-check.mjs・commit a0792b8・司令塔再走 10/10)に更新した(本裁定と同 commit)。

## 台帳

CLAIMS W3-13。次: K⁽⁵⁾ 橋 D1(走行中・便 29 F7 ガード反映指示済み)→ n=5 manifest 起草(§5.2.5 五札+BRIDGE-IN に τ 明示)→ falsifier 計画監査 → 発射錠。Lean Phase 1(plain 層)並行走行中。
