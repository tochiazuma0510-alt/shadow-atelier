# `Z-norm-seal/v1` 条文案(profinite root normalization)— **draft v2(便 59 Part A の P59-A1〜A4 修理版)**

2026-07-28 起草(draft v1)・**同日 draft v2**: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱・裁定 70。
**身分**: **候補条文であり、受理されるまで効力を持たない。** 正典(TB4 導出 v2.4・Rule 1 v1.4 §1.4.1・便 49 F6.5・便 55 F3・便 56 P56-1/P56-2・**便 59 Part A F2/F3/F4**)のみを用いた。外部文献は使っていない。

**認可の系譜(便 55 F3 の「別の明示的認可」要件)**: **(a) 認可の起点 = 研究者意向(2026-07-28)**。**便 59 F2 が数学的採用原理を PASS**、**F4.1 が「P59-A1〜A4 を逐語的に満たす差分なら新たな定理候補ゲートは不要」と条件付き認可**。**(b) status/CLAIMS 全域更新は未実施**。状態は `drafted / unapproved`。
**⚠ digest の扱い(便 59 F4.1)**: **draft の digest を発効 seal の digest として使ってはならない。** 本 v2 の digest も draft のものであり、発効時には司令塔が改めて hash して差分検収を通すこと。

---

## 1. 条文(scope = `profinite`)

```text
Z-norm-seal/v1 (scope = profinite):
  (1) bar_iota_id:        bar_iota は Rule 1 (1.6) の iota_infty の延長である(bar_iota|_K = iota_infty);
  (2) root_system_tb2_id: zeta_n^TB2 := bar_iota^{-1}(exp(2*pi*i/n))   for every n >= 1;
  (3) profinite canonical edge (named edge, 便 56 P56-2 / 便 59 P59-A1):
        edge_id  = "tb2-canonical-root-equality/profinite-v1"
        lhs      = root_system_tb2_id
        rhs      = canonical_root_system_id      # (zeta_n^can)_n := (bar_iota^{-1}(exp(2*pi*i/n)))_n
        scope    = profinite
        proof    = forall n, both sides are bar_iota^{-1}(exp(2*pi*i/n))
        certificate = 上の forall n の証明 artifact とその digest
  (4) root_normalization_level = profinite を主張する全 TB4 comparison は、この bar_iota_id、
      profinite root-system ID、profinite canonical edge を参照しなければならない。
      既存窓は migration/compatibility certificate が出るまで従来の normalization level に留まり、
      seal 採用だけで profinite に昇格しない(窓の一覧は §3)。
```

**atomic**: 4 条は**分割不能**。(1) だけ・(2) だけを採ると (4) の「同一の $\bar\iota$」が保証されず、窓ごとに別の比較データが混入しうる(TB4 導出 v2.4 §8.1 の理由づけを全 $n$ へ拡張して継承)。

**【P59-A1】certificate の型**: (3) の equality certificate は **「無限列を列挙した digest」であってはならない**。**$\forall n$ の証明 artifact とその digest** である($\zeta_n^{\rm TB2}$ と $\zeta_n^{\rm can}$ が**同じ $\bar\iota$ の同じ式で同時に定義される**という定義的等式の証明)。

**実現可能性(無償であること)**: $\bar\iota_0$ を $\iota_\infty$ の任意の延長とし $\zeta_n^{\rm TB2}:=\bar\iota_0^{-1}(e^{2\pi i/n})$ と**定める**。整合系である($\zeta_{mn}^m=\zeta_n$)。TB4 導出 v2.4 §4.3 の悉皆表により、$n\nmid20$ の $\zeta_n$ は現行正典のどこにも現れない**純粋な空白**である(**新しい算術仮定ではなく、未指定だった比較データの選択** — 便 48 F8・便 59 F2.1)。

---

## 2. 既存 finite seal との interface(**identity binding**・P59-A1 後段 / P59-A2)

> **本節も seal の規範内容の一部**である。ただし scope 語を含むため、**P55-2 の逆向き lint を守って §1(profinite 条文)とは節を分ける**。

**(2-a) 派生する finite edge — 既存 ID を維持し、lhs を restrict で型付けする(P59-A1)**

```text
edge_id  = "rule1-tb2-root-equality/v1"          # 既存 ID をそのまま維持(新設・改名しない)
lhs      = restrict(root_system_tb2_id, n=20)
rhs      = rule1_root_2M_id
scope    = level_20
proof    = Z-norm(1)(2) + Rule 1 (1.6)
```

**(2-b) object identity の固定(P59-A2)**

```text
Z-norm.bar_iota_id                        = Z20-link.bar_iota_id
restrict(Z-norm.root_system_tb2_id, n=20) = Z20-link.root_system_tb2_id
derived_level20_edge_id                   = "rule1-tb2-root-equality/v1"
```

> **なぜ値の等式では足りないか(便 59 F3.2)**: §4 の含意証明は**値**の等式を与えるが、版イベントに必要なのは **artifact の identity まで含む typed extension** である。「どちらも $\iota_\infty$ を延長する」だけでは**別の extension ID が二本並び**、finite result record と profinite result record が**別 object を参照できてしまう**。

---

## 3. window inventory(P59-A3・**総覧**)

**規約**: `compatibility_status` は $\{$`migrated`, `pending`, `not_assessed`$\}$ の三値 enumeration。**既定値への fallback を禁止**する(未知値・欠落は fail-closed)。`migrated_record_digest` は `migrated` のとき REQUIRED。

| window_id | previous_level | rule_root_id | compatibility_status | migrated_record_digest |
|---|---|---|---|---|
| `K5`($M=10$, $2M=20$) | `level_20` | `rule1_root_2M_id`($\zeta_{20}^{\rm Rule1}$・Rule 1 (1.5)(1.6) で凍結済) | **`migrated`**(§2 の (2-a)(2-b) がそのまま migration edge) | **発効時に司令塔が記入**(draft では発行できない) |
| `K3`($M=6$, $2M=12$) | `level_none`(埋め込み未凍結) | **未凍結**($\iota_{12}$ の凍結文が存在しない — TB4 導出 v2.4 §5.3) | **`pending`** | — |
| `A5`($M=5$, $2M=10$) | `level_none` | **未凍結**(司令塔実測 2026-07-28: A₅ v4 全文 grep で (1.6) 型の埋め込み凍結文なし — 競合 object 不在の**観測**であり非存在の証明ではない) | **`pending`**(裁定 70 追補・司令塔記入) | — |
| **上記以外のすべての窓** | 各窓の従来値 | 各窓の値 | **`not_assessed`**(既定) | — |

> **total 性(P59-A3)**: 最終行により inventory は**全窓を被覆**する。**`not_assessed` の窓は seal 採用によって昇格しない** — §1 (4) 後段がそれを規範として与える。**「競合 object が無いこと」と「同一 object が記録されたこと」は別の主張である**(便 59 F3.3)。
> **⚠ 起草者の申告**: `A5` 行および最終行の `not_assessed` は、**私が凍結文を確認できなかった**という意味であり、**存在しないことの証明ではない**(負の探索結果は非存在の証明ではない)。発効前に司令塔が inventory を実測で埋めること。

---

## 4. `Z20-link-seal/v1` との関係(別 ID・別 scope)

$$ \boxed{\ \texttt{Z-norm-seal/v1}\ \Longrightarrow\ \texttt{Z20-link-seal/v1},\qquad \textbf{逆は偽}\ } $$

- **順方向**: §1 (2) を $n=20$ で読むと $\zeta_{20}^{\rm TB2}=\bar\iota^{-1}(e^{2\pi i/20})$。§1 (1) と Rule 1 (1.6)(**一意**に $e^{2\pi i/20}$ を指す)より $\zeta_{20}^{\rm Rule1}=\bar\iota^{-1}(e^{2\pi i/20})$。ゆえに $\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}$、すなわち $t_{20}=1$。これは TB4 導出 v2.4 §3.5.1a **条件鎖 (3.6)** の第 1 段であり、§2 (2-a) の `proof` 欄の中身でもある。
- **逆が偽である witness**(TB4 導出 v2.4 §3.5.1a・便 50 F3.1 提供): $\hat{\mathbb Z}^\times$ の unit で **$2$-進・$5$-進成分 $=1$、$3$-進成分 $=-1$、他の素点 $=1$** なるものは、$\bmod\ 20$ では $1$ だが **exact に $1$ ではない**。**$L3\nRightarrow L4$。**

> **⇒ 両者を「一部凍結/全体凍結」の関係で呼んではならない**(便 49 F6.5)。**別 ID・別 scope として台帳化**し、片方の版事故が他方を巻き込まないようにする。

---

## 5. 発効した場合の帰結(**列挙のみ・本案は他文書を変更しない**)

| # | 対象 | 発効後 |
|---|---|---|
| 1 | **定理 TB4-B** | **発動。$\varepsilon=1$**(= exact (TB4))が**定理**になる。札は `paper-proof / conditional on (Z-norm)` → **`root-normalization-relative theorem (relative to Z-norm-seal/v1)`**。**`verified`(Lean)ではなく、A3-framework-conditional のまま。** |
| 2 | **定理 TB4-A20** | **不変。** 有限札は `finite theorem (M\|20), conditional on Z20-link` のまま**据え置く**。含意されても**有限定理の前件を profinite seal へ書き換えてはならない**(scope 逆行 = P55-2 lint 違反)。 |
| 3 | **`root_normalization_level`** | enum 値 `profinite` が使用可能になる(TB4 導出 v2.4 §8.6a の四段と 1:1)。**ただし §1 (4) により、その値を主張できるのは §3 で `migrated` の窓だけ。** |
| 4 | **$B_{\rm FC}$ の「exact $\varepsilon=1$ の関所」表記** | **「`Z-norm-seal/v1` 下の定理」へ変わる候補箇所**(**列挙のみ・変更しない**): §0-6 の札本文/ §2 (2.2) 直後の「だから (TB4) は文献関所のままである」/ §4 依存表の注(S1 の射程限定)/ §8.1 末の状態札表/ §9 系 B-7′ の状態札 (ii)/ §10 の「exact $\varepsilon$ は load-bearing でない」注/ §12.1【GAP-TB】(TB4) 行と【文献要請 13】(ii)/ §13.3 の 6 層表 GLOBAL-FRAMEWORK 行。**実際の同期は司令塔の版イベントで行う。** |
| 5 | **$K^{(3)}$($M=6$)の $\zeta_6$ 射程**【**P59-A4 で型修正**】 | **TB2 側の profinite root は本 seal で確定する。** $K^{(3)}$ の Rule 側 $\zeta_{12}$ に**同じ object を採用する explicit migration edge** が出れば、$t_{12}=1$、$\varepsilon\equiv1\ (\mathrm{mod}\ 12)$、$b_{\rm cmp}=b_{\rm op}=1$ が従う。**$b_{\rm op}=1$ 自体の最小前件は従来どおり TB4-E package(root-link-free)であり、root compatibility を最小前件へ追加しない。** |
| 6 | **`NF-root-link` 系 fixture** | **不変**(negative regression として存続)。seal 発効は「$t_{20}=11$ が起こらない」ことを保証するのであって、**「起こっても検出できる」ことを保証しない** — 測定の盲点(TB4 導出 v2.4 §3.5.4)は seal では消えない。 |

> **⚠【P59-A4・自認】draft v1 の誤り**: v1 の $K^{(3)}$ 行は「**$b_{\rm op}=1$ には当該窓の Rule 側生成元が同じ $\bar\iota$ を通して定まっていることが要る**」と書いた。**TB4 導出 v2.4 §3.5.1a/§3.5.2 の辞書と衝突する。** 共通 package の下では **$b_{\rm op}=1$ は TB4-E により root-link-free** であり、root compatibility が要るのは **$t_{12}=1$・$\varepsilon\equiv1\,(12)$・$b_{\rm cmp}=1$・$b_{\rm cmp}=b_{\rm op}$ の側**である。私は「**窓固有の Rule 側規約(TB4-E の (E-ii)(E-iv) の一部)**」と「**TB2↔Rule の root compatibility(link)**」を同じものとして書いていた。**自認。**
> **⇒ 併せて禁止**: **「現行 $B_{\rm FC}$ proof artifact が link 前件を保持すること」と「定理の最小前件が root-link-free であること」を混同しない**(便 59 F3.4)。

---

## 6. 発効しても**不変**のもの(緩めてはならない)

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

## 7. 出所対応表(便 56 P56-1 の 5 欄)

| transfer_mode | source_range | target_range | approval_id | change_summary |
|---|---|---|---|---|
| `normative-only` | TB4 導出 v2.4 §8.1 (i)(ii) | §1 (1)(2) | — | 版履歴注記・自己訂正説明を省略。規範内容($\forall n$ 量化を含む)は保存 |
| `adapted` | TB4 導出 v2.4 §8.1 (iii) | §1 (3) | 研究者意向 2026-07-28 + 便 59 P59-A1 | 単一 digest から **named edge** へ型替え。**edge_id を `tb2-canonical-root-equality/profinite-v1` に分離**(既存 Rule edge との型衝突を回避)。certificate を **$\forall n$ 証明 artifact** と規定 |
| `adapted` | TB4 導出 v2.4 §8.1 (iv) | §1 (4) | 研究者意向 2026-07-28 + 便 59 P59-A3 | 全称を **「`profinite` を主張する comparison が参照すべき ID 群」+「既存窓は certificate まで昇格しない」**の二文へ total 化 |
| `adapted` | Rule 1 v1.4 §1.4.1 の named edge | §2 (2-a)(2-b) | 便 59 P59-A1/A2 | 既存 edge ID を**維持**し lhs を `restrict(..., n=20)` へ型付け。**object identity 三式**を新設 |
| `adapted` | (新設) | §3 window inventory | 便 59 P59-A3 | 五欄 inventory を新設。**最終行の既定 `not_assessed` で total 化** |
| `normative-only` | TB4 導出 v2.4 §3.5.1a (3.6) と witness 表 | §4 | — | 条件鎖の第 1 段と $L3\nRightarrow L4$ witness のみ抜粋 |
| `verbatim` | TB4 導出 v2.4 §8.2 | §6-4 の code block | — | A3 seal の逐語 |
| `adapted` | draft v1 §3-5 | §5-5 | 便 59 P59-A4 | **$b$ の型を修正**(中身は §5 の ⚠ 参照)。最小前件へ root compatibility を追加しない形へ |

---

## 8. 検証欄(**実測値**)

| 項目 | 結果 |
|---|---|
| CR(0x0D)・C0 制御文字・TAB | **0**(§9 のコマンドで実測) |
| **逆向き seal-scope lint**(便 55 P55-2) | **§1(profinite 条文)に `level_20` の語なし**(実測 0)。scope 語 `level_20` を含む規範内容は **§2 に分離**した |
| 順方向 seal-scope lint | `for every n` は §1(scope = `profinite`)にのみ現れ、§2(scope = `level_20`)には無い(実測 0) |
| edge ID の分離(P59-A1) | `tb2-canonical-root-equality/profinite-v1`(§1)と `rule1-tb2-root-equality/v1`(§2)が**別 ID**で共存 |
| window inventory の total 性(P59-A3) | 最終行 `上記以外のすべての窓 → not_assessed` により全被覆 |
| 状態 | `drafted / unapproved` — **P59-A1〜A4 の逐語充足が発効条件・status/CLAIMS 全域更新前・commit していない** |

## 9. 検査コマンド(再現用)

```sh
grep -Pc '\r' docs/znorm_seal_draft.md                              # CR = 0
grep -Pc '[\x00-\x08\x0B\x0C\x0E-\x1F]' docs/znorm_seal_draft.md    # C0 = 0
grep -Pc '\t' docs/znorm_seal_draft.md                              # TAB = 0
awk '/^## 1\./,/^## 2\./' docs/znorm_seal_draft.md | grep -c level_20        # profinite 条文への混入 = 0
awk '/^## 2\./,/^## 3\./' docs/znorm_seal_draft.md | grep -c 'for every n'   # level_20 節への混入 = 0
```
