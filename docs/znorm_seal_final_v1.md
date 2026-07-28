# `Z-norm-seal/v1`(profinite root normalization)— **final v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱・裁定 71。**component 3(final seal 本文)**。
**系譜**: draft v1(裁定 70)→ draft v2(便 59 P59-A1〜A4 修理・`docs/znorm_seal_draft.md`)→ **本 final v1**(便 60 F4.2/F4.3/F4.4 の修文 3 点を反映)。
**依拠正典**: TB4 導出 v2.4・Rule 1 v1.4 §1.4.1・manifest v1.6・便 49 F6.5・便 55 F3・便 56 P56-1/P56-2・便 58 F5・便 59 Part A・**便 60 Part A F3〜F5**。外部文献は使っていない。

**認可の系譜**: **(a) 認可の起点 = 研究者意向(2026-07-28)**。**便 59 F2 = 数学的採用原理 PASS**。**便 60 F3 = P59-A1〜A4 全 PASS**、**便 60 F5 = 小版イベント payload の発効許可**(便 60 F4 の apply 条件を同一 transaction で満たすことが条件)。

### 状態欄(便 60 F4.2)

```text
# 現況(本ファイル確定時点・起草者が記入)
status_now        = committed as draft / unapproved / non-operative
draft_provenance  = docs/znorm_seal_draft.md (draft v2)

# 発効時(司令塔が event receipt と同時に記入)
status_on_apply   = ____________________   # "approved / operative"
applied_at        = ____________________   # 発効時刻
event_receipt_id  = ____________________
```

> **⚠ 状態文の分離(便 60 F4.2)**: 「commit していない」という**起草時の作業状態**を final へ持ち越さない。**履歴 draft の起草時状態と現時点の repository 状態は別**である。
> **⚠ digest(便 60 F4.5)**: draft の hash(`5b071429df5c72db95ee60ab2a88ba4efb05ff1b7ee32de349959bdeb39360eb`)を**発効 seal の digest として使うことは明示的に禁止**されている。本 final を F4.1 の順序で新たに hash すること。

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

**実現可能性(無償であること)**【**便 60 F4.3 で射程を縮小**】: $\bar\iota_0$ を $\iota_\infty$ の任意の延長とし $\zeta_n^{\rm TB2}:=\bar\iota_0^{-1}(e^{2\pi i/n})$ と**定める**。整合系である($\zeta_{mn}^m=\zeta_n$;証明は component 1 命題 ZP-1)。**空白であるのは root の存在や記号ではなく**、
$$ \boxed{\ n\nmid20\ \text{における}\ \zeta_n^{\rm TB2}\ \textbf{の具体値}、\text{および各 window の Rule-side object との}\ \textbf{typed comparison / equality record}\ } $$
である。**したがって本 seal は新しい算術仮定ではなく、未指定だった比較データの選択にとどまる**(便 48 F8・便 59 F2.1)。

> **⚠ draft v2 の誤り(自認・便 60 F4.3)**: draft は「$n\nmid20$ の $\zeta_n$ は現行正典の**どこにも現れない純粋な空白**」と書いた。**そのままでは偽である** — (TB2)/(TB4) は**抽象的な全 root system をすでに使って**おり、$K^{(3)}$ 正典にも $\zeta_{12}$ という **field object** は現れる。空白の所在を上の 2 点へ狭める。**結論(規約選択にすぎない)は不変。**

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

**規約**: `compatibility_status` は $\{$`migrated`, `pending`, `not_assessed`$\}$ の**閉じた三値 enumeration**。**既定値への fallback を禁止**する(**未知値・行欠落は fail-closed** — 下の catch-all で救済してはならない)。`migrated_record_digest` は `migrated` のとき **REQUIRED**。

| window_id | previous_level | rule_root_id | compatibility_status | migrated_record_digest |
|---|---|---|---|---|
| `K5`($M=10$, $2M=20$) | `level_20` | `rule1_root_2M_id`($\zeta_{20}^{\rm Rule1}$・Rule 1 (1.5)(1.6) で凍結済) | **`migrated`**(record 本体 = `docs/k5_migration_record_v1.md`) | `sha256:ae1e9ef051c04d02c78f23bfb16b358da2077bfe65b684b9da6c998adb291120`(component 2) |
| `K3`($M=6$, $2M=12$) | `level_none`(埋め込み未凍結) | **未凍結**($\iota_{12}$ の凍結文が存在しない — TB4 導出 v2.4 §5.3) | **`pending`** | — |
| `A5`($M=5$, $2M=10$) | `level_none` | **未凍結**(司令塔実測 2026-07-28: A₅ v4 全文 grep で (1.6) 型の埋め込み凍結文なし — 競合 object 不在の**観測**であり非存在の証明ではない) | **`pending`**(裁定 70 追補・司令塔記入) | — |
| **上記以外のすべての window**(**明示 catch-all rule**) | 各窓の従来値 | 各窓の値 | **`not_assessed`** | — |

> **total 性(P59-A3)**: 最終行は **`上記以外のすべての window を明示的に捕捉する catch-all rule`** であり、inventory を**全窓被覆**にする。**`not_assessed` の窓は seal 採用によって昇格しない** — §1 (4) 後段がそれを規範として与える。**「競合 object が無いこと」と「同一 object が記録されたこと」は別の主張である**(便 59 F3.3)。
> **⚠【便 60 F4.4】catch-all は既定値ではない**: draft は最終行を「`not_assessed`(**既定**)」と書いたが、**default fallback を禁止しながら「既定」と呼ぶのは自己矛盾**である。**未知の enum 値・行の欠落をこの catch-all で救済してはならない**(それらは fail-closed)。catch-all が捕捉するのは「**列挙されていない window**」だけである。**自認。**
> **⚠ 観測の身分**: `A5` 行の rule_root_id は**司令塔実測(2026-07-28)による競合 object 不在の観測**であって**非存在の証明ではない**。`K3`・`A5` はいずれも `pending` であり、**seal 採用だけによる自動昇格は禁じられている**。

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
| `adapted` | (新設) | §3 window inventory | 便 59 P59-A3 | 五欄 inventory を新設。**最終行の明示 catch-all rule で total 化** |
| `adapted` | draft v2 §1 の「純粋な空白」文 | §1 の実現可能性 | 便 60 F4.3 | 空白の所在を **$n\nmid20$ の具体値 + typed comparison/equality record** へ縮小 |
| `adapted` | draft v2 §3 最終行・§8 | §3 最終行・§8 | 便 60 F4.4 | **「既定」→「明示 catch-all rule」**へ統一。未知値・行欠落の救済禁止を明記 |
| `adapted` | draft v2 §8 状態行 | 冒頭状態欄・§8 | 便 60 F4.2 | 起草時状態文を除去し、**現況 `committed as draft / unapproved / non-operative`** と**発効欄(司令塔記入枠)**に分離 |
| `adapted` | draft v2 §3 `K5` 行・§9 | §3 `K5` 行・§9 | 便 60 F4.1 | **component 1/2 の digest 枠**と **F4.1 の hash 順序**を新設。自己参照禁止を明記 |
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
| window inventory の total 性(P59-A3) | **明示 catch-all rule** 行により全被覆(F4.4 の語で統一済) |
| 状態(F4.2) | `committed as draft / unapproved / non-operative` — 発効欄は冒頭の状態欄(司令塔記入枠) |
| $n\nmid20$ の空白の記述(F4.3) | **具体値 + typed comparison/equality record** へ縮小済(§1) |

## 9. component 束(**司令塔記入枠**・便 60 F4.1 の順序厳守)

```text
# 1) 先に hash する component
component_1_path    = docs/znorm_forall_proof_v1.md          # forall n equality proof artifact
component_1_sha256  = a8eee73829a8f66c925f1eee18a8cd92fd505a8709d526d20ed594ce7c0d9c55
component_2_path    = docs/k5_migration_record_v1.md         # K5 typed migration record
component_2_sha256  = ae1e9ef051c04d02c78f23bfb16b358da2077bfe65b684b9da6c998adb291120

# 2) 上の digest を本 final に埋めてから本 final を hash
final_seal_path     = docs/znorm_seal_final_v1.md
final_seal_sha256   = (event receipt に記録 — 自己参照禁止につき本 artifact には記入しない)

# 3) receipt が final seal hash と全 component を束縛(final は receipt digest を要求しない)
event_receipt_id    = (event receipt 側で発行 — 同上)

# 実在を要する ID 群(F4.1-3)
bar_iota_id                 = "bar-iota/ext-of-iota-infty/v1"
root_system_tb2_id          = "root-system/tb2/v1"
canonical_root_system_id    = "root-system/canonical-exp2pi/v1"
rule1_root_2M_id            = "root/rule1-zeta20/v1"
edge_profinite              = "tb2-canonical-root-equality/profinite-v1"
edge_level20                = "rule1-tb2-root-equality/v1"
```

> **⚠ 自己参照禁止**: **final seal 自身に、それを含む receipt の digest を要求して循環させてはならない**(便 60 F4.1)。
> **⚠ `migrated` と空 digest の組合せを final artifact に残してはならない** — §3 の `K5` 行と上の `component_2_sha256` は**同じ値**で埋めること。

## 10. 検査コマンド(再現用)

```sh
grep -Pc '\r' docs/znorm_seal_final_v1.md                              # CR = 0
grep -Pc '[\x00-\x08\x0B\x0C\x0E-\x1F]' docs/znorm_seal_final_v1.md    # C0 = 0
grep -Pc '\t' docs/znorm_seal_final_v1.md                              # TAB = 0
awk '/^## 1\./,/^## 2\./' docs/znorm_seal_final_v1.md | grep -c level_20        # profinite 条文への混入 = 0
awk '/^## 2\./,/^## 3\./' docs/znorm_seal_final_v1.md | grep -c 'for every n'   # level_20 節への混入 = 0
grep -c '既定' docs/znorm_seal_final_v1.md                             # F4.4: catch-all を「既定」と呼ばない
```
