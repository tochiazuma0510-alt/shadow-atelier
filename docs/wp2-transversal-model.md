# WP2 仕様: transversal-cocycle モデル(照合器用 B₃/N の独立構成)— v1 凍結

2026-07-18・司令塔導出・機械検算済み。目的: 照合器(crosscheck/)が **GAP に依存せず** full B₃/N を構成し、hexagon (3.3)(3.4) を検査するための正本仕様。Sol 便 02 の監査対象。

## 経緯(設計判断の記録)

- 初案「3n 点上の Dₙ≀S₃(affine 拡大込み)への実現」は**不可能**(司令塔の証明: σ̄₁ のブロック置換が (2,3) 型でも成分方程式 d₁² = r が残り、偶数 n の n 点上で n サイクルは平方になれない。ソルバの解 0 件とも整合)。
- 採用案: 右剰余類 PB₃\B₃ の切断 T を使う 12n 点モデル(以下)。奇偶一様・c ≠ 1 の対象にも φ の差し替えで適用可。

## モデル

- 切断 T = {t₁,…,t₆} = {e, σ₁, σ₂, σ₁σ₂, σ₂σ₁, Δ = σ₁σ₂σ₁}(PB₃\B₃ の代表)。
- 対象データ: 有限群 Q と全射 φ: PB₃ → Q(x ↦ φx, y ↦ φy, c ↦ φc)。dihedral 主線では Q = Dₙ、φ = (x↦s, y↦rs, c↦1)※rs は左作用 = 実装では「s のち r」。
- **点集合 = Q × T(|Q|·6 点)**。σ ∈ {σ₁, σ₂} の作用: (q, t) ↦ (q·φ(p(t,σ)), t′)。
- **規則表(凍結・司令塔導出 2026-07-18)** — t·σ = p(t,σ)·t′ in B₃:

| t \ σ | σ₁: (p, t′) | σ₂: (p, t′) |
|---|---|---|
| t₁ = e | (1, t₂) | (1, t₃) |
| t₂ = σ₁ | (x, t₁) | (1, t₄) |
| t₃ = σ₂ | (1, t₅) | (y, t₁) |
| t₄ = σ₁σ₂ | (1, t₆) | (y⁻¹x⁻¹c, t₂) |
| t₅ = σ₂σ₁ | (x⁻¹y⁻¹c, t₃) | (1, t₆) |
| t₆ = Δ | (y, t₄) | (x, t₅) |

- 導出根拠: braid 関係と 2401 の交換公式 (1.10)(1.11)(1.12)(x = σ₁², y = σ₂², c = Δ² 中心)。c を運ぶのは (t₄,σ₂)・(t₅,σ₁) の 2 規則のみ(hexagon の c^m 項の出所)。
- この作用の像 = B₃/Core_{B₃}(ker φ)。dihedral では Core = K⁽ⁿ⁾(2405 Prop 3.1)。

## 検算記録(`search/wp2-rules-verify.g`・GAP 4.16.0)

1. **12 恒等式**を忠実 Artin 表現 B₃ ↪ Aut(F₃)(σᵢ の標準作用)で全件 VERIFIED。
2. **較正(n = 5, 8)**: braid 関係成立 / |⟨σ̂₁,σ̂₂⟩| = 6|Gₙ|(3000・1536)/ ĉ = 1 / N_ord = lcm(n,2) / **PB₃ 部分 ⟨x̂,ŷ⟩ が x̂↦(r,s,s), ŷ↦(rs,r,rs) で Gₙ と同型** — すべて PASS。

## 照合器への実装指示(要旨)

- 照合器は本表を定数として実装し、(a) 12 規則から σ̂₁, σ̂₂ を組む、(b) braid 関係・σ̂ᵢ² の値・ĉ = φc の**自己検査**を起動時に行う(仕様定数のバグ検出)、(c) hexagon (3.3)(3.4) を σ̂ 語の積として Q×T 上で評価する。
- GAP 側スクリプト・helper の import は禁止(独立性)。証明書(JSON)以外の入力を受けない。
- **独立性の層の設計判断(Sol 便 02 の監査対象)**: 群のモデル(12 規則)は両系統が共有する「仕様」であり(SAT ソルバと checker が CNF 形式を共有するのと同型)、独立性の対象は**計算**(列挙・検証の実装と経路)。仕様自体は Artin 検証+ψₙ 同型較正で論文に係留済み。

## 証明書スキーマ gtsh-cert/v1(凍結・2026-07-18 司令塔設計)

対象 1 つにつき JSON 1 ファイル(`certificates/<id>.v1.json`、SHA-256 を LEDGER に記帳)。

```
{
  "schema": "gtsh-cert/v1",
  "generated_by": { "tool": "GAP 4.16.0", "script": "...", "date": "..." },
  "target": {
    "family": "dihedral" | "control",
    "id": "K08" | "N5",
    "n": 8,                              // dihedral のみ
    "phi": { "desc": "x->s, y->rs, c->1 (left action)", "q_order": 16 },
    "invariants": { "index_PB3": 256, "index_B3": 1536, "N_ord": 8,
                     "derived_order": 64 }
  },
  "conventions": { "dn_element": "[a,e] = r^a s^e", "action": "left(rs = s のち r)",
                    "f_word_alphabet": "x,y(c は不要 — f ∈ F2)" },
  "shadows": [
    { "m": 0,
      "f_word": [["y",-2],["x",2], ...],     // 語(万国共通形 — 照合器はこれを評価)
      "f_triple": [[2,0],[6,0],[1,0]],       // D_n^3 座標(冗長データ — 語との不一致はバグ検出器)
      "kernel_cert": { "type": "conjugator-triple",   // Lemma 4.2 (4.11) の (h1,h2,h3)
                        "h": [ [u,v]-affine 表記×3 ] }
                     | { "type": "brute", "expected_kernel_index": 30 }   // 小さい control 用
    }, ...
  ],
  "counts": { "raw_candidates": N, "hexagon_pass": N, "charming_pass": N,
               "surjective_pass": N },         // silent cap 禁止 — 全段の個数を残す
  "composition_table": [[i,j,k], ...],          // shadows[i]∘shadows[j] = shadows[k](全対)
  "inverse_map": [ [i, i_inv], ... ],
  "reduction": [ { "to": "K04", "image": [shadow index...], "surjective": true } ],
  "ls_witness": [ { "m": ..., "k": ..., "g_word": [...], "h_word": [...] } ]   // 3|n のみ
}
```

**照合器の検査項目(証明書ごと)**: ①counts の整合(候補全数 = 自前列挙と一致)②各 shadow の full hexagon (3.3)(3.4) を Q×T モデルで ③f_word ↔ f_triple の一致 ④charming(f_word の導来性は f_triple ∈ 導来部分群で判定)+全射性 ⑤Thm 4.3 の閉じた式との集合一致(dihedral)⑥kernel_cert の (4.11) 等式 ⑦composition_table を (3.53) で再計算・(4.19)(4.20) 恒等式 ⑧inverse を (3.54) で ⑨reduction 像の再計算と全射性 ⑩ls_witness の (5.1) 両式。判定は項目別 PASS/FAIL の verdict JSON で出力(工程正常≠数学判定 — ES7 教訓)。
