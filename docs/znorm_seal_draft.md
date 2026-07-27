# `Z-norm-seal/v1` 条文案(profinite root normalization)— **draft v1**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱。
**身分**: **候補条文であり、受理されるまで効力を持たない。** 起草者は正典(TB4 導出 v2.4・Rule 1 v1.4 §1.4.1・便 49 F6.5・便 55 F3・便 56 P56-1/P56-2)のみを用いた。外部文献は使っていない。

**認可の系譜(便 55 F3 の「別の明示的認可」要件)**: Rule 1 v1.4 §1.4.1 は full `(Z-norm)` の採用に **(a) 別の明示的認可**と **(b) status/CLAIMS 全域更新**を要求している。本案について **(a) の起点は研究者意向(2026-07-28)**、**Sol ゲートは便 59 予定**、**(b) は未実施**。したがって現状は `drafted / unapproved`。

---

## 1. 条文(scope = `profinite`)

```text
Z-norm-seal/v1 (scope = profinite):
  (1) bar_iota_id:        bar_iota は Rule 1 (1.6) の iota_infty の延長である(bar_iota|_K = iota_infty);
  (2) root_system_tb2_id: zeta_n^TB2 := bar_iota^{-1}(exp(2*pi*i/n))   for every n >= 1;
  (3) root_equality_edge (named edge, 便 56 P56-2):
        edge_id             = "rule1-tb2-root-equality/profinite-v1"
        lhs_object_id       = root_system_tb2_id
        rhs_object_id       = canonical_root_system_id     # (zeta_n^can)_n := (bar_iota^{-1}(exp(2*pi*i/n)))_n
        scope               = profinite
        certificate_digest  = (zeta_n^TB2)_n = (zeta_n^can)_n の equality_certificate_digest
  (4) すべての窓・すべての M における TB4 比較は、この同一の bar_iota_id・root_system_tb2_id・
      root_equality_edge を参照する(n の量化に制限を置かない)。
```

**atomic**: 4 条は**分割不能**。(1) だけ・(2) だけを採ると (4) の「同一の $\bar\iota$」が保証されず、窓ごとに別の比較データが混入しうる(TB4 導出 v2.4 §8.1 の理由づけを全 $n$ へ拡張して継承)。

**実現可能性(無償であること)**: $\bar\iota_0$ を $\iota_\infty$ の任意の延長とし $\zeta_n^{\rm TB2}:=\bar\iota_0^{-1}(e^{2\pi i/n})$ と**定める**。整合系である($\zeta_{mn}^m=\zeta_n$)。$n\mid20$ では Rule 1 (1.6)(1.7) と一致する。**新しい算術仮定ではなく、未指定だった比較データの選択である**(便 48 F8)。TB4 導出 v2.4 §4.3 の悉皆表により、$n\nmid20$ の $\zeta_n$ は現行正典のどこにも現れない**純粋な空白**である。

---

## 2. `Z20-link-seal/v1` との関係(別 ID・別 scope)

$$ \boxed{\ \texttt{Z-norm-seal/v1}\ \Longrightarrow\ \texttt{Z20-link-seal/v1},\qquad \textbf{逆は偽}\ } $$

- **順方向**: §1 (2) を $n=20$ で読むと $\zeta_{20}^{\rm TB2}=\bar\iota^{-1}(e^{2\pi i/20})$。§1 (1) と Rule 1 (1.6)(**一意**に $e^{2\pi i/20}$ を指す)より $\zeta_{20}^{\rm Rule1}=\bar\iota^{-1}(e^{2\pi i/20})$。ゆえに $\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}$、すなわち $t_{20}=1$。これは TB4 導出 v2.4 §3.5.1a **条件鎖 (3.6)** の第 1 段である。
- **逆が偽である witness**(TB4 導出 v2.4 §3.5.1a・便 50 F3.1 提供): $\hat{\mathbb Z}^\times$ の unit で **$2$-進・$5$-進成分 $=1$、$3$-進成分 $=-1$、他の素点 $=1$** なるものは、$\bmod\ 20$ では $1$(ゆえに `Z20-link` を満たす)だが **exact に $1$ ではない**(ゆえに `Z-norm` を満たさない)。**$L3\nRightarrow L4$。**

> **⇒ 両者を「一部凍結/全体凍結」の関係で呼んではならない**(便 49 F6.5)。**別 ID・別 scope として台帳化し、片方の版事故が他方を巻き込まない**ようにする。

---

## 3. 発効した場合の帰結(**列挙のみ・本案は他文書を変更しない**)

| # | 対象 | 発効後 |
|---|---|---|
| 1 | **定理 TB4-B** | **発動。$\varepsilon=1$**(= exact (TB4))が**定理**になる。状態札は `paper-proof / conditional on (Z-norm)` → **`root-normalization-relative theorem (relative to Z-norm-seal/v1)`**。**`verified`(Lean)ではなく、A3-framework-conditional のまま。** |
| 2 | **定理 TB4-A20** | **不変。** 有限札は `finite theorem (M\|20), conditional on Z20-link` のまま**据え置く**。`Z-norm` が `Z20-link` を含意しても、**有限定理の前件を profinite seal へ書き換えてはならない**(scope 逆行 = P55-2 lint 違反)。 |
| 3 | **`root_normalization_level`** | enum 値 `profinite` が使用可能になる(TB4 導出 v2.4 §8.6a の四段と 1:1)。`level_2M` を宣言した record が $\varepsilon=1$ を主張したら従来どおり fail-closed。 |
| 4 | **$B_{\rm FC}$ の「exact $\varepsilon=1$ の関所」表記** | **「`Z-norm-seal/v1` 下の定理」へ変わる候補箇所**(**列挙のみ・変更しない**): §0-6 の札本文/ §2 (2.2) 直後の「だから (TB4) は文献関所のままである」/ §4 依存表の注(S1 の射程限定)/ §8.1 末の状態札表/ §9 系 B-7′ の状態札 (ii)/ §10 の「exact $\varepsilon$ は load-bearing でない」注/ §12.1【GAP-TB】(TB4) 行と【文献要請 13】(ii)/ §13.3 の 6 層表 GLOBAL-FRAMEWORK 行。**実際の同期は司令塔の版イベントで行う。** |
| 5 | **$K^{(3)}$($M=6$)の $\zeta_6$ 射程** | **閉じる — ただし条件つき。** §1 (2) は $n=12$ を含むので (TB2) 側は確定する。**$b_{\rm op}=1$ には当該窓の Rule 側生成元が同じ $\bar\iota$ を通して定まっていることが要る**((4) の窓横断量化)。$K^{(3)}$ には**競合する $\iota_{12}$ の凍結文が存在しない**(TB4 導出 v2.4 §5.3)ので、$\zeta_{12}^{\rm Rule}:=\bar\iota^{-1}(e^{2\pi i/12})$ と定めれば $t_{12}=1$ が従い、$\varepsilon\equiv1\ (12)$・$b_{\rm cmp}=b_{\rm op}=1$。**⚠ 独立に凍結済みの埋め込みを持つ窓があれば、その窓では (1) と同型の互換性検査が別途要る**(本案は自動的には上書きしない)。 |
| 6 | **`NF-root-link` 系 fixture** | **不変**(negative regression として存続)。`Z-norm-seal` 発効は「$t_{20}=11$ が起こらない」ことを保証するのであって、**「起こっても検出できる」ことを保証しない** — 測定の盲点(TB4 導出 v2.4 §3.5.4)は seal では消えない。 |

---

## 4. 発効しても**不変**のもの(緩めてはならない)

1. **測定規律 Rule 1 (7.1)**: $b_i=1$ を仮定してはならない。必ず計算して記録する。**定理があることは、実装がその定理の規約を実現したことを保証しない。**
2. **観測後 fitting の禁止**・**$\exists b$ PASS の禁止**(TB4 導出 v2.4 §8.4・BFC §8.1 U5)。
3. **二段コミット**(Freeze 1 で rule 事前コミット / Freeze 2 で actual $b_i$ を $u$・$G_K$ 観測**前**に記録)と **integrity quarantine**(便 49 F11)。
4. **A3 gate — `Z-norm` は A3 を証明しない**(TB4 導出 v2.4 §8.2 の再掲):
```text
TB4-comparison / orientation seal (framework, NOT implied by TB2-norm):
  positive topological forward transport  <->  algebraic postcomposition-left action
```
 A3 は (TB1)(TB3) と同格の枠組み事実であり【GAP-TB】に残る。**本案が固定するのは root 選択の自由度であって、比較の向きではない。** 文献要請 13(ii) は A3 の comparison orientation として**縮小維持**。
5. **$K^{(5)}$ campaign の operative 述語 (5′$_b$)** および `b_semantics="op"` / `b_value_i = b_op_value`(便 49 F4.3 で確定)。

---

## 5. 出所対応表(便 56 P56-1 の 5 欄)

| transfer_mode | source_range | target_range | approval_id | change_summary |
|---|---|---|---|---|
| `normative-only` | TB4 導出 v2.4 §8.1 (i)(ii) | 本案 §1 (1)(2) | — | 版履歴注記・自己訂正説明を省略。規範内容は保存(∀n 量化を含む) |
| `adapted` | TB4 導出 v2.4 §8.1 (iii) | 本案 §1 (3) | 研究者意向 2026-07-28 | 単一 digest から **named edge**(便 56 P56-2)へ型替え。`scope = profinite` 欄を新設。**level 20 固有の対応(rhs = rule1_root_2M_id)を canonical 根系との等式へ一般化** |
| `adapted` | TB4 導出 v2.4 §8.1 (iv) | 本案 §1 (4) | 研究者意向 2026-07-28 | 「全 TB4 比較」を**窓横断(すべての窓・すべての $M$)**として明示量化 |
| `normative-only` | TB4 導出 v2.4 §3.5.1a (3.6) と witness 表 | 本案 §2 | — | 条件鎖の第 1 段と $L3\nRightarrow L4$ witness のみ抜粋 |
| `verbatim` | TB4 導出 v2.4 §8.2 | 本案 §4-4 の code block | — | A3 seal の逐語 |
| `adapted` | TB4 導出 v2.4 §5.3 | 本案 §3-5 | 研究者意向 2026-07-28 | 「(Z-norm) を採れば全 $M$ で一斉に解決」を、**窓ごとの Rule 側生成元の互換性を条件に付けた形**へ精密化(⚠ 行) |

---

## 6. 検証欄

| 項目 | 結果 |
|---|---|
| CR(復帰改行)・C0 制御文字・TAB | **0**(§7 の検査コマンドで実測) |
| **逆向き seal-scope lint**(便 55 P55-2) | **§1(profinite 節)に `level_20` の語なし**。実測: `level_20` は**本 §6 と §7(検証欄・検査コマンド)にしか現れない**。§2・§3 は別 seal を `Z20-link-seal/v1` という **ID 名**で参照しており、scope 語を profinite 本文へ持ち込んでいない |
| 順方向 seal-scope lint | §1 の `for every n` は scope = `profinite` の下でのみ現れる(`level_20` 節には無い) |
| 状態 | `drafted / unapproved` — **Sol ゲート(便 59 予定)前・status/CLAIMS 全域更新前・commit していない** |

## 7. 検査コマンド(再現用)

```sh
grep -c $'\r' docs/znorm_seal_draft.md          # CR = 0
grep -Pc '[\x00-\x08\x0B\x0C\x0E-\x1F]' docs/znorm_seal_draft.md   # C0 = 0
grep -Pc '\t' docs/znorm_seal_draft.md          # TAB = 0
awk '/^## 1\./,/^---/' docs/znorm_seal_draft.md | grep -c level_20  # profinite 節への混入 = 0
```
