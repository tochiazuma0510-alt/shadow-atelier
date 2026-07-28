# `tb2-canonical-root-equality/profinite-v1` — $\forall n$ equality proof artifact **v1**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱・裁定 71。
**身分**: `Z-norm-seal/v1` §1 (3) の **certificate 本体**(component 1)。便 59 P59-A1 / 便 60 F3.1 の要求どおり、**「無限個の値を列挙した digest」ではなく一つの証明 artifact** である。
**状態**: `drafted / unapproved / non-operative`(発効 transaction 内で司令塔が hash・束縛する)。

---

## 1. 記号と与件

| 記号 | 内容 | 出所 |
|---|---|---|
| $\bar\iota$ | 体の埋め込み $\bar{\mathbb Q}\hookrightarrow\mathbf C$ で $\bar\iota|_K=\iota_\infty$ なるもの(`bar_iota_id` が指す artifact) | `Z-norm-seal/v1` (1) |
| $\zeta_n^{\rm TB2}$ | $:=\bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr)$($n\ge1$) | `Z-norm-seal/v1` (2)(`root_system_tb2_id`) |
| $\zeta_n^{\rm can}$ | $:=\bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr)$($n\ge1$) | `canonical_root_system_id` の定義 |
| $\mu_n,\ \mu_\infty$ | $\bar{\mathbb Q}$ 内の $n$ 乗根群・全冪根群 | — |

---

## 2. 主張

> ### 命題 ZP-1($\forall n$ equality)
> $$ \boxed{\ \forall n\ge1:\qquad \zeta_n^{\rm TB2}\ =\ \bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr)\ =\ \zeta_n^{\rm can}\ } $$
> さらに $(\zeta_n^{\rm TB2})_{n\ge1}$ は **(TB2) の要求する整合的原始冪根系**である。すなわち
> **(a) well-defined**、**(b) 原始的**($\mathrm{ord}=n$)、**(c) 整合的**($\zeta_{mn}^m=\zeta_n$)。

---

## 3. 証明

**(a) well-defined.** $\bar\iota$ は体の埋め込みだから単射であり、$X^n-1$ の根を根へ写す。$\bar{\mathbb Q}$ は代数閉体なので $\lvert\mu_n(\bar{\mathbb Q})\rvert=n=\lvert\mu_n(\mathbf C)\rvert$、したがって $\bar\iota$ は $\mu_n(\bar{\mathbb Q})\xrightarrow{\ \sim\ }\mu_n(\mathbf C)$ を与える(単射な $n$ 元集合間の写像)。$e^{2\pi i/n}\in\mu_n(\mathbf C)$ ゆえ $\bar\iota^{-1}(e^{2\pi i/n})$ は $\mu_n(\bar{\mathbb Q})$ の**一意な**元として定義される。∎

**(b) 原始的.** $\bar\iota|_{\mu_\infty}$ は群同型なので乗法的位数を保つ。$e^{2\pi i/n}$ の位数は $n$、ゆえに $\zeta_n^{\rm TB2}$ の位数も $n$。∎

**(c) 整合的.** $\bar\iota^{-1}|_{\mu_\infty}$ が群準同型であることから
$$ \bigl(\zeta_{mn}^{\rm TB2}\bigr)^{m} \;=\; \bar\iota^{-1}\bigl(e^{2\pi i/(mn)}\bigr)^{m} \;=\; \bar\iota^{-1}\Bigl(\bigl(e^{2\pi i/(mn)}\bigr)^{m}\Bigr) \;=\; \bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr) \;=\; \zeta_n^{\rm TB2}. \qquad\blacksquare $$

**(d) 等式そのもの.** $\zeta_n^{\rm TB2}$ と $\zeta_n^{\rm can}$ は、**同一の `bar_iota_id` から同一の式 $\bar\iota^{-1}(e^{2\pi i/n})$ で定義されている**。したがって等式は**定義的**であり、各 $n$ ごとの数値的一致の集積ではない。**これが「無限列の列挙 digest」ではなく単一の proof artifact で足りる理由である。** ∎

> **★ 何が証明の中身か(誤読防止)**: 実質は (a)(b)(c) — すなわち「**この定義が (TB2) の要求する整合的原始冪根系を実際に与える**」ことである。(d) 自体は同語反復に近い。**したがって本 artifact は「等式の証明」であると同時に「定義の適格性の証明」である。**

---

## 4. 派生(level 20 への restrict)

> ### 系 ZP-2(`rule1-tb2-root-equality/v1` の proof 欄)
> $\bar\iota|_K=\iota_\infty$ と Rule 1 (1.6)(「$\Phi_{20}$ の根のうち $\operatorname{Im}>0$ かつ $\operatorname{Re}$ 最大」は**一意**に $e^{2\pi i/20}$ を指す)より
> $$ \mathrm{restrict}\bigl(\zeta_\bullet^{\rm TB2},\,n=20\bigr)\;=\;\bar\iota^{-1}\bigl(e^{2\pi i/20}\bigr)\;=\;\iota_\infty^{-1}\bigl(e^{2\pi i/20}\bigr)\;=\;\zeta_{20}^{\rm Rule1}, $$
> すなわち $t_{20}=1$。∎
> **これは `Z-norm-seal/v1` §2 (2-a) の `proof = Z-norm(1)(2) + Rule 1 (1.6)` の内容である。**

---

## 5. 本 artifact が**証明しないもの**(射程の明示)

1. **A3(位相 forward transport $\leftrightarrow$ 代数 後合成左作用)を証明しない。** A3 は (TB1)(TB3) と同格の枠組み事実であり【GAP-TB】に残る(TB4 導出 v2.4 §8.2)。
2. **単独では $\varepsilon=1$ を与えない。** $\varepsilon=1$(定理 TB4-B)は本 artifact に**加えて** TB4-3 の比較式 ($*$) を要する。
3. **$K^{(5)}$ 以外の窓の Rule-side object identity を与えない。** 各窓の Rule 側生成元との typed comparison/equality record は**窓ごとの migration edge**が担う(`Z-norm-seal/v1` §1 (4)・§3 inventory)。
4. **$b_{\rm op}=1$ の最小前件を変更しない。** $b_{\rm op}=1$ は TB4-E package により **root-link-free** のままである(便 59 P59-A4)。

---

## 6. 依存(全列挙)

| # | 依存 | 型 |
|---|---|---|
| 1 | `bar_iota_id` が実在の埋め込み $\bar{\mathbb Q}\hookrightarrow\mathbf C$ を指し、$\bar\iota|_K=\iota_\infty$ | `Z-norm-seal/v1` (1) |
| 2 | Rule 1 (1.6) の一意性(系 ZP-2 のみ) | Rule 1 v1.4(operative) |
| 3 | 体の埋め込みが単射・乗法的位数を保つこと | 標準・初等 |
| 4 | $\bar{\mathbb Q}$ が代数閉 | 標準 |

**外部文献は使っていない。機械計算は行っていない**(本 artifact は紙上のみ)。

---

## 7. digest 欄(**司令塔記入枠**・便 60 F4.1 の順序)

```text
artifact_id        = "tb2-canonical-root-equality/profinite-v1#proof"
artifact_path      = docs/znorm_forall_proof_v1.md
artifact_sha256    = ____________________________________   # 司令塔が本ファイル確定後に記入
bound_edge_id      = "tb2-canonical-root-equality/profinite-v1"
bound_seal_id      = "Z-norm-seal/v1"
```

> **⚠ 自己参照禁止(便 60 F4.1)**: 本 artifact は**自らを含む receipt の digest を要求しない**。順序は
> `proof artifact / migration record → final seal に digest 記入 → final seal を hash → receipt が全 component を束縛`。
