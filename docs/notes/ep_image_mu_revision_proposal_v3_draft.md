# IMAGE-MU 改版案 **v3** 草案(DRAFT・未採択・未着工)— 便 104 F104-5.2 差戻しの修理

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED / 未着工**。**凍結 artifact は一切触っていない**(spec v20・contract v15・manifest v15・branch key v1・R1/R2・selfaudit v11/v12・freeze receipt・`ninfty-searcher-v2.mjs` すべて byte 不変)。
> - **前版は byte 不変で保存**(versioned supersede): v1 = `docs/notes/ep_image_mu_revision_proposal_v1_draft.md` / v2 = `docs/notes/ep_image_mu_revision_proposal_v2_draft.md`。本書は **v2 の差替**。
> - 札は不動: **`IMAGE-MU=UNKNOWN` / `W6_CLOSED=false` / `W-6=OPEN`**(便 104 F104-5.2 逐語)。**`EP=uncalibrated・UNKNOWN`** も不動。
> - ★ **認可の現況**(便 104 F104-5.2 逐語): 「**これを v3 に直すまで implementation scope の継続認可も発火認可も出さない。**」⟹ 便 103 で出た **EP-1 条件付き認可は保留状態**である。本書はその解除を請うための修理稿であって、**着工の根拠ではない**。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。

---

## 1. v2 → v3 の変更点(**すべて便 104 F104-5.2 由来**)

| # | v2 の誤り | v3 での修理 | 節 |
|---|---|---|---|
| **v3-1** ★ | §3.1 が $g(T)=(T-a_0)^2-p_0^2f_0 \in \mathbf{Q}[T]$ と書いていた — **一般には偽**。$x_0$ が代数的なら $a_0,p_0,f_0 \in \mathbf{Q}(x_0)$ であり、左辺はまず $\mathbf{Q}(x_0)[T]$ にしかない | **resultant 構成へ差替**: $q_x(X)$(= $x_0$ の既約多項式)と $H(X,T)=(T-a(X))^2-p(X)^2f_6(X)$ から $R(T)=\operatorname{Res}_X(q_x, H)$ | §3 |
| **v3-2** ★ | resultant/候補多項式を**最小多項式と呼んでいた** | **呼ばない**。resultant は**共役全体や重複を含み得る**。因子選択後の既約因子だけが $\mu$ の最小多項式である | §3.2 |
| **v3-3** ★ | 因子選択が「固定実埋込みで **exact root rank** に対応する既約因子」だけ | **不足**。**$x_0$ と $\mu$ を結ぶ isolating data(isolating interval / Thom encoding 等)**が要る。$x$ 側と $y$ 側の双方 | §3.3 |
| **v3-4** ★ | 無限遠の順位付けを無条件に「$\mathrm{lc}(f_6)$ の平方根を exact に順位付け」 | **$\mathrm{lc}(f_6)>0$ が固定実埋込みで確認できる枝に限る**。**二実枝が無い場合は UNKNOWN** | §4 |

**v2 から引き継ぎ、内容を変更しない部分**: §2(A 不採択の理由と A′/B)・修理 2(e=2 の解消)・修理 3(support の悉皆性)・status algebra・W6-P22(未登録 live ID)・改版の骨格。以下では §3/§4 を差し替え、他は要旨のみ再掲する。

> ★ **便 104 F104-5.2 が明示的に「よい」と認めた点は v3 でも不変**: **A 撤回・versioned model registry・三値/STOP の分離・multiplicity/support/orientation の修理方針**。

---

## 2. curve model の供給経路 — **v2 から不変**(要旨)

`search/ninfty-searcher-v2.mjs`(**930 行目**)の `curve_model_digest` は**固定散文文字列**

```js
sha256Hex('y^2 = f6(x), mu = a(x)+p(x)y (lane A candidate-scoped model)')
```

の SHA-256(`25c6cadf…dc930`)に過ぎず、**候補ごとの $a,p,f_6,C,\mu$ を一 byte も拘束しない**。`ambient_quotient_relations` も dereference 可能な model artifact ではない。⟹ **A は不採択・C は明示却下**(便 103 F103-6.3 裁定)。

**採択 = B または A′**: 受領側が保持する **versioned model registry** に、**係数体・$a,p,f_6,C$・map $\mu$・無限遠 chart/transition・向き・実埋込み/root order** を **exact** に置き、

```jsonc
"curve_model_ref": { "artifact_id": "…", "json_pointer": "/…", "whole_artifact_sha256": "<64hex>" }
```

で参照する。**D-2 cert はこの ref を転送してよいが、固定散文の digest で代用してはならない。** ref 不在・inline-only は `LEGACY_UNVERIFIED_REF`(W6-C5)⟹ **IMAGE-MU = UNKNOWN**。

---

## 3. ★ 修理 1(全面差替)— 有限点の像多項式の **resultant 構成**

### 3.1 なぜ v2 が偽だったか

v2 は $a_0 = a(x_0)$, $p_0 = p(x_0)$, $f_0 = f_6(x_0)$ と置き、$g(T)=(T-a_0)^2-p_0^2f_0$ を **$\mathbf{Q}[T]$ の元**として扱った。しかし **$x_0$ は一般に代数的数**であり($\gcd(a,a')$ の根であって有理数とは限らない)、$a_0,p_0,f_0 \in \mathbf{Q}(x_0)$ である。⟹ $g(T) \in \mathbf{Q}(x_0)[T]$ にしかなく、**$\mathbf{Q}[T]$ 上の因数分解にも token bytes 比較にもそのままでは載らない**。

> ★ **教材点**: 「係数が有理数のように見える式」を **$\mathbf{Q}[T]$ と書いてしまう**型の誤り。**$x_0$ の代数性を明示的に持ち回る**設計にしないと、実装段で暗黙の有理数化(= 浮動小数点近似)へ落ちる。

### 3.2 正しい構成(**便 104 F104-5.2 指定**)

1. **$q_x(X)$ = $x_0$ を選ぶ既約多項式**($\mathbf{Q}[X]$・原始・正 leading)。$x_0$ は **$q_x$ + isolating data** の対で**一意に指定**する(§3.3)。
2. **$H(X,T) = (T - a(X))^2 - p(X)^2 f_6(X)\ \in \mathbf{Q}[X,T]$**。
3. ★ **$R(T) = \operatorname{Res}_X\!\big(q_x(X),\, H(X,T)\big)\ \in \mathbf{Q}[T]$** — **これが $\mathbf{Q}$ 上の候補多項式**である。
4. **squarefree 分解**。
5. **$\mathbf{Q}[T]$ 上で因数分解**。
6. **固定実埋込み + isolating data で $\mu$ を含む既約因子を一意選択**(§3.3)。
7. **primitive / positive-leading 正規化**。
8. **token bytes と比較**(バイト一致)。

### 3.3 ★ 呼称と選択の規律

- ★ **$R(T)$ を最小多項式と呼ばない。** resultant は **$x_0$ の共役全体**にわたる像($y$ の両 branch を含む)と**重複**を含み得る。**最小多項式は「選択された既約因子」だけ**である。条文・cert・報告のいずれでもこの区別を守る。
- ★ **選択には exact root rank だけでは足りない。** **$x_0$ と $\mu$ を結ぶ isolating data** が要る:
  - **$x$ 側**: $q_x$ に対する $x_0$ の **isolating interval**(有理端点)または **Thom encoding**(導多項式の符号列)。
  - **$y$ 側**: $y^2 = f_6(x_0)$ の二根のどちらか(= exact root rank $\rho$)を、**同じ固定実埋込み**の下で isolating data として持つ。
  - **$\mu$ 側**: 上記から $\mu = a(x_0)+p(x_0)y$ の **isolating data を伝播**させ、$R(T)$ の既約因子のうち**その data と両立するものがちょうど 1 つ**であることを確認する。
- ★ **一意選択に失敗したら(候補が 0 個または 2 個以上)UNKNOWN**。**「たぶんこれ」で選ばない。** 分離精度が足りない場合は **精度を上げて再試行**し、**上限に達したら UNKNOWN**(無限ループにしない)。
- **申告値は入力でなく照合対象**: producer の `exact_reduction` は**照合対象**であり、選択の入力に使わない(v1 から不変)。
- **全計算は exact**(有理数/代数的数の exact 演算)。**浮動小数点を判定に使わない**(isolating interval の端点も有理数)。

### 3.4 縮退の扱い

| 縮退 | 扱い |
|---|---|
| $p(x_0)^2 f_6(x_0)$ が $\mathbf{Q}(x_0)$ の平方 | 像が $\mathbf{Q}(x_0)$ へ退化。**因数分解 + 選択が自動的に処理する**(二点は**次数の下がった別 token** を持ちうる)。特別扱いの分岐を書かない |
| $p(x_0)=0$ | 二点が像を共有する縮退 ⟹ **v1 宇宙外 → UNKNOWN** |
| $f_6(x_0)=0$ | 前件違反 ⟹ **UNKNOWN**(有限点の枝が成立しない) |
| $R(T)$ が定数/零 | **MALFORMED / STOP**(構成の前提が壊れている) |

---

## 4. ★ 修理 4(差替)— 無限遠 2 点の順位付け

- **固定実埋込み**で **$\mathrm{lc}(f_6)$ の平方根を exact に順位付け**し、inf$_\pm$ の canonical ID を **K-1 の固定埋込みに対して**定義する。
- ★ **この順位付けは $\mathrm{lc}(f_6)>0$ が固定実埋込みで確認できる枝に限る。**
- ★ **二実枝が無い場合(= $\mathrm{lc}(f_6)$ が当該埋込みで正でない・実の二枝が立たない)は UNKNOWN。** **順位を仮定して PASS を出さない。**
- 向き(どちらの無限遠点で 5 位の零か)は **full local expansion から導出**する。★ **散文 `orientation` 文字列は証拠にしない**(現 producer の `orientation: '(Or) div(mu)=…'` は witness として不可)。
- $e=5 \Rightarrow m_r=4$。**全 12 単位のうち 8 単位がここ**。

---

## 5. 修理 2 / 修理 3 — **v2 から不変**(要旨)

- **修理 2($e=2$ の固定解消)**: 「$x_0$ は $\gcd(a,a')$ の**単根**」は $e=2$ を暗黙に固定する。**(2a)** v1 宇宙を「$a$ の重根がちょうど 2」に**事前登録**して限定(宇宙外は **UNKNOWN**・silent cap にせず報告)、または **(2b)** 一般 $e$ を計算し `gcd` 側の**重複度 $e-1$ と照合**(不一致は FAIL)。**係の見解は (2a) を v1 宇宙・(2b) を別途事前登録の v2 宇宙**。**選択は司令塔判断。**
- **修理 3(support の悉皆性)**: support $=\{\text{roots}(\gcd(a,a'))\}\times\{2\ y\text{-rank}\}\cup\{\text{無限遠 2 点}\}$ は **Pell/genuine-v1 の前件**と「**他に ramification が無い**」証明を要する。**満たさなければ UNKNOWN。** producer の `declared_support` は **cross-check へ降格**。

---

## 6. status algebra(**EP-3 裁定・v2 から不変**)

| 状況 | status |
|---|---|
| schema / json_pointer / digest 不正 | **MALFORMED / STOP** |
| **model 欠品**(`curve_model_ref` 不在・inline-only・dereference 不能) | **UNKNOWN** |
| **事前登録宇宙外**($e$ 条件外・係数体 $\ne\mathbf{Q}$・$d\ge3$・$p(x_0)=0$・$f_6(x_0)=0$・§3.3 の一意選択失敗・§3 の前件未確認・§4 の二実枝なし) | **UNKNOWN** |
| **well-formed な image / rank / multiplicity の不一致** | **FAIL** |
| 全 record(有限点 + 無限遠点)が PASS | **IMAGE-MU = PASS** |

**ABSENT は W6-P8 の予約語のまま使わない。部分被覆で PASS を出さない。**

---

## 7. 未登録 live ID のインシデント(**W6-P22・v2 から不変**)

`mb/ninfty-w6-image-witness/v1` は 4 本の live code にのみ存在し、凍結体系(spec v20 / contract v15 / manifest v15 / branch key v1)に**文字列が無い**。**便 103 で今回インシデントとして記帳**(裁定 501 採録)。spec 側対応条項 **W6-P22**: ① 未登録 schema ID を判定 interface に用いた実装は **MALFORMED** ② 当該 ID を **W6-P1 と同格で plane 登録**(現行 code の欄名がそのまま normative ⟹ **code 改変不要**)③ **selfaudit v13 に「live code が参照する schema ID の集合 ⊆ 登録済み ID の集合」検査を additive 追加**(**既存 24 検査は逐語維持**)④ **両縁 fixture**。

---

## 8. 改版の骨格(**additive only・凍結 byte 不変**・v2 から不変)

spec **v21**(§5.3.5.2 additive 新設・**W6-P1〜P12 は逐語同一**)/ contract **v16** / manifest **v16**(`Y-3d`)/ point-map schema **v2** / witness schema **v1 登録** / **`bundle-selfaudit-v13.py`**(**additive only**)。hash 順序 **manifest → contract → spec → receipt** 維持。**二 route は独立**(`R1'` = resultant 経路 / `R2'` = 二次拡大上のノルム構成 + 独立な原始化。**共通 module・相互 import 禁止**)。

### 8.1 負例 fixture(**両縁**)

**発火側**: ① curve model と食い違う token / ③ $p(x_0)<0$ 系の rank 反転 / ④ 無限遠の向き入替 / ⑤ $m_r$ を 4→3 に改竄し総和 12 を破る / ⑦ `curve_model_ref` を欄ごと削除(**missing-both が素通りしない**)/ ★ ⑧ **$R(T)$ が可約**な候補で**誤った既約因子**を選ばせる試み / ★ ⑫ **共役 $x_0'$ の像の因子**を token として提出(resultant が共役を含むことを突く変異)。
**非発火側**: ② model と一致する正規 token / ③′ $p(x_0)>0$ 系の正例 / ④′ 正しい向き。
**UNKNOWN の縁**: ⑥ `curve_model_ref` を inline-only(**UNKNOWN であって PASS でない**)/ ⑨ $e\ne2$ の候補 / ⑩ §5 修理 3 の前件未確認 / ★ ⑪ **isolating data の一意選択が失敗**する候補 / ★ ⑬ **$\mathrm{lc}(f_6)$ の二実枝が無い**候補。

---

## 9. 発効しないもの(明示)

- **本書そのもの**(改版案 v3 草案)。spec の live 正本は **v20**。
- **W6-P13〜P22**(未起草・未採択)。★ **§3〜§5 が spec v21 の条文へ反映されるまで W6-P13〜P21 を書かない。**
- ★ **implementation scope の継続認可・発火認可**(便 104 F104-5.2 により**保留中**)。
- **`IMAGE-MU=PASS` / `W6_CLOSED` / W-6 閉鎖 / EP 較正**(いずれも与えられない)。
- **§5 の (2a)/(2b) の選択**・**§2 の A′/B の選択**(司令塔判断待ち)。
