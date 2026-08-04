# IMAGE-MU 改版案 **v2** 草案(DRAFT・未採択・未着工)— 便 103 F103-6.3 裁定の反映

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED / 未着工**。**凍結 artifact は一切触っていない**(spec v20・contract v15・manifest v15・branch key v1・R1/R2・selfaudit v11/v12・freeze receipt・`ninfty-searcher-v2.mjs` すべて byte 不変)。
> - **前版 `docs/notes/ep_image_mu_revision_proposal_v1_draft.md`(v1)は byte 不変で保存**(versioned supersede)。本書は v1 の**差替**であって追記ではない。
> - 札は不動: **`W6_CLOSED=false` / `IMAGE-MU=UNKNOWN` / `W-6=OPEN` / `EP=uncalibrated・UNKNOWN`**。
> - 由来: **便 103 F103-6.3** — **EP-1 = spec 起草 + 実装 scope のみ条件付き認可** / **EP-2 = B または A′**(**A は不採択・C は明示却下**)/ **EP-3 = 裁定済み** / **未登録 live ID は今回インシデントとして記帳**(裁定 501 に採録済み)。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**着工は認可条件 4 点(§3)の spec 反映後**。

---

## 1. v1 → v2 の変更点(**すべて便 103 F103-6.3 由来**)

| # | v1 | v2 | 根拠 |
|---|---|---|---|
| **v2-1** | **三択 A を推奨**(D-2 certificate の `curve_model_digest` / `ambient_quotient_relations` へ pin) | ★ **A 不採択**。**採択 = B または A′**(versioned model registry) | §2 |
| **v2-2** | C は「明文で却下すべき」と上申 | ★ **C 明示却下(裁定済み)** | §2 |
| **v2-3** | W6-P14 が最小多項式を $(T-a_0)^2-p_0^2f_0$ と同定 | ★ **修理 1**: 常に最小多項式ではない。squarefree/因子分解 → 固定実埋込みで exact root rank に対応する**既約因子**を選択 → 原始・正 leading normalization 後に token bytes 比較 | §3.1 |
| **v2-4** | W6-P14 ① が「$x_0$ は $\gcd(a,a')$ の単根」 | ★ **修理 2**: これは **$e=2$ を固定**する。v1 宇宙を**重根ちょうど 2** に限定するか、**一般 $e$ を計算**して `gcd` 側の重複度 $e-1$ と照合 | §3.2 |
| **v2-5** | W6-P18 が support を「$\gcd(a,a')$ の根 × 2 rank + 無限遠 2 点」と断定 | ★ **修理 3**: これは Pell/genuine-v1 の**前件**と「**他に ramification が無い**」証明を要する。満たさなければ **UNKNOWN** | §3.3 |
| **v2-6** | W6-P16 が向きを「主係数関係から」とだけ | ★ **修理 4**: **固定埋込みで leading coefficient の平方根を exact に順位付け**し、**full local expansion から導出**。散文 orientation は証拠にしない | §3.4 |
| **v2-7** | W6-P19 の status algebra を上申 | ★ **EP-3 裁定を採録**: schema/pointer/digest 不正 → **MALFORMED/STOP** / model 欠品・事前登録宇宙外 → **UNKNOWN** / **well-formed な image・rank・multiplicity 不一致 → FAIL** | §4 |
| **v2-8** | GAP-6 を「改版を待たず記帳するのが安全」と上申 | ★ **インシデントとして記帳済み(裁定 501)**。**spec 側の対応条項 W6-P22 を新設** | §5 |

---

## 2. ★ curve model の供給経路 — **A 不採択の理由と A′/B**

### 2.1 なぜ A が採れないか(**Sol が特定した現物**)

`search/ninfty-searcher-v2.mjs` の当該行(**930 行目**)は次である。

```js
curve_model_digest: sha256Hex('y^2 = f6(x), mu = a(x)+p(x)y (lane A candidate-scoped model)'),
```

すなわち `curve_model_digest` は **候補モデルの artifact digest ではなく、固定散文文字列の SHA-256**(`25c6cadf…dc930`)である。**候補ごとの $a,p,f_6,C,\mu$ を一 byte も拘束しない。** `ambient_quotient_relations` も dereference 可能な model artifact ではない。

⟹ **A(既存 D-2 certificate の欄へ pin)は提案どおりには成立しない。** v1 の推奨は**現物の確認を欠いた設計**だった。**係の誤りとして記帳する。**

> ★ **教材点**: 「既存の欄があるから新しい信頼点を作らない」という設計判断は正しい方向だが、**その欄が実際に何を束縛しているかを code で確認する前に推奨してはならない**。欄名(`curve_model_digest`)が意味を保証しない — **[27] 事件と同じく「名前と実体の乖離」型**である。

### 2.2 採択案 — **A′ / B(versioned model registry)**

**受領側が保持する versioned model registry** に、候補ごとの model を **exact** に置く。

| registry entry が exact に保持するもの |
|---|
| **係数体**(base field) |
| **$a,\ p,\ f_6,\ C$**(exact 有理数係数・浮動小数点表現を持たない) |
| **map $\mu$** |
| **無限遠 chart / transition**(chart id と遷移写像) |
| **向き**(orientation・§3.4 の exact 順位付けと整合する形式) |
| **実埋込み / root order**(固定実埋込みの指定と根の順序) |

参照は:

```jsonc
"curve_model_ref": { "artifact_id": "…", "json_pointer": "/…", "whole_artifact_sha256": "<64hex>" }
```

- **D-2 cert はこの ref を転送してよい**が、**固定散文の digest で代用してはならない**(便 103 逐語)。
- **A′ と B の差**は registry の置き場所(既存 provisioning 系の中か、新規 registry artifact か)であり、**exact 保持と whole-artifact digest の要件は共通**。**どちらを採るかは実装段の選択**として spec v21 に両立可能な形で書く。
- **payload 埋込み(C)は明示却下**。ref 不在・inline-only は `LEGACY_UNVERIFIED_REF`(W6-C5)⟹ **IMAGE-MU = UNKNOWN**(PASS へ到達しない)。

---

## 3. ★ W6-P13〜P21 起草前の修理 4 点(**便 103 F103-6.3 の 1〜4**)

### 3.1 修理 1 — 最小多項式の同定(v1 の W6-P14 ④⑤ を置換)

$(T-a_0)^2 - p_0^2 f_0$ は **常に最小多項式ではない**($p_0^2f_0$ が有理平方なら可約、その他の退化もありうる)。**正しい手順**:

1. $g(T) = (T-a_0)^2 - p_0^2 f_0 \in \mathbf{Q}[T]$ を構成。
2. **squarefree 分解 → 既約因子分解**。
3. **固定実埋込み**で **exact root rank** に対応する**既約因子を選択**(§3.4 の順位付けと同じ埋込みを使う)。
4. **原始化 + 正 leading coefficient 正規化**。
5. **token bytes と比較**(バイト一致)。

⟹ v1 の「⑤ 原始整数化した最小多項式が token 係数列とバイト一致」は、**2〜4 を経ていないので不十分**だった。

### 3.2 修理 2 — $e=2$ の固定を解消(v1 の W6-P14 ① を置換)

「$x_0$ は $\gcd(a,a')$ の**単根**」は $e=2$ を暗黙に固定する。**二択を spec に明記**:

- **(2a) 宇宙の限定**: v1 宇宙を「$a$ の**重根がちょうど 2**」に**事前登録**して限定する。宇宙外は **UNKNOWN**(silent cap にせず**報告**)。
- **(2b) 一般 $e$**: 各分岐点で **$e$ を計算**し、`gcd` 側の**重複度 $e-1$ と照合**する。不一致は FAIL。

**係の見解**: (2a) を v1 とし、(2b) を v2 宇宙として**別途事前登録**する(宇宙を勝手に広げない)。**どちらを採るかは司令塔判断。**

### 3.3 修理 3 — support の悉皆性(v1 の W6-P18 を置換)

support $=\{\text{roots}(\gcd(a,a'))\}\times\{\text{2 つの } y\text{-rank}\}\ \cup\ \{\text{無限遠 2 点}\}$ は、**Pell/genuine-v1 の前件**と「**他に ramification が無い**」ことの**証明**を必要とする。

- **前件が確認できる**場合: 上式を support として使い、record 集合との**厳密一致**を要求。
- **確認できない場合**: ★ **UNKNOWN**(PASS へ到達しない)。**「他に無いはず」を仮定して PASS を出さない。**
- producer の `declared_support` は **cross-check へ降格**(参照系にしない)— v1 から不変。

### 3.4 修理 4 — inf$_\pm$ の exact 順位付け(v1 の W6-P16 を置換)

- **固定実埋込み**で **leading coefficient の平方根を exact に順位付け**する($\sqrt{\mathrm{lc}(f_6)}$ の符号選択を exact に固定)。
- 向き(どちらの無限遠点で 5 位の零か)は **full local expansion から導出**する。
- ★ **散文 `orientation` 文字列は証拠にしない**(現 producer の `orientation: '(Or) div(mu)=5P_0-5P_inf, …'` は witness として不可)。
- inf$_\pm$ の canonical ID は **K-1 の固定埋込みに対して**定義する。
- $e=5 \Rightarrow m_r=4$。**全 12 単位のうち 8 単位がここ**。

---

## 4. status algebra(**EP-3 裁定の採録**・W6-P19 を置換)

| 状況 | status |
|---|---|
| schema / json_pointer / digest 不正 | **MALFORMED / STOP** |
| **model 欠品**(`curve_model_ref` 不在・inline-only・dereference 不能) | **UNKNOWN** |
| **事前登録宇宙外**($e$ 条件外・係数体 $\ne\mathbf{Q}$・$d\ge3$・$p(x_0)=0$・§3.3 の前件未確認) | **UNKNOWN** |
| **well-formed な image / rank / multiplicity の不一致** | ★ **FAIL** |
| 全 record(有限点 + 無限遠点)が PASS | **IMAGE-MU = PASS** |

- **ABSENT は W6-P8 の予約語のまま使わない**(v1 から不変)。
- **部分被覆で PASS を出さない**(v1 から不変)。

---

## 5. ★ 未登録 live ID のインシデント記帳と spec 側対応条項(**W6-P22 新設**)

**事実**: `mb/ninfty-w6-image-witness/v1` は 4 本の live code(`ninfty-w6-key-gate-r1p.py` / `-r2p.py` / `-pointmap-lanea.mjs` / `-pointmap-laneb.py`)にのみ存在し、**spec v20・contract v15・manifest v15・branch key 文書 v1 のいずれにも文字列が無い**(branch key 文書 §4 は `"schema_id":"..."` の placeholder のまま)。**便 103 で今回インシデントとして記帳**(裁定 501 に採録済み)、**改版まで黙認しない**。

**spec 側の対応条項(案)**:

> **W6-P22(schema ID の登録義務・v21 新設)**
>
> 1. **live code が判定に用いる schema ID は、すべて凍結体系(spec / contract / manifest / branch key 文書)に versioned 登録されていなければならない。** 未登録 ID を判定 interface に用いた実装は **MALFORMED**。
> 2. `mb/ninfty-w6-image-witness/v1` を **W6-P1 と同格で plane に登録**する。**現行 live code の欄名がそのまま normative** になる(⟹ **code 側の改変は不要**)。branch key 文書 §4 の `"schema_id":"..."` placeholder を実 ID へ差し替える(**versioned 新版で**。v1 は byte 不変)。
> 3. **selfaudit v13 に「live code が参照する schema ID の集合 ⊆ 登録済み ID の集合」の検査を additive で追加**する。**既存 24 検査は逐語維持。** ⟹ **同型の再発を機械が止める**([27] 事件の型の恒久対策)。
> 4. **両縁 fixture**: ① 未登録 ID を持ち込んだ実装(**発火側**)② 登録済み ID のみの実装(**非発火側**)。

---

## 6. 改版の骨格(**additive only・凍結 byte 不変**)— v1 から不変

spec **v21**(§5.3.5.2 を additive 新設・**W6-P1〜P12 は逐語同一**)/ contract **v16** / manifest **v16**(`Y-3d`)/ point-map schema **v2**(`curve_model_ref` 追加を v1 の黙った拡張にしない)/ witness schema **v1 登録** / **`bundle-selfaudit-v13.py`**(**additive only**・既存 24 検査逐語維持)。hash 順序 **manifest → contract → spec → receipt** を維持。

**二 route は独立**(`R1'` = 終結式による $y$ 消去 / `R2'` = 二次拡大上のノルム構成 + 独立な原始化。**共通 module・相互 import 禁止**)。

### 6.1 負例 fixture(**両縁**・便 103 の条件)

① curve model と食い違う token(**発火**)/ ② model と一致する正規 token(**非発火**)/ ③ $p(x_0)<0$ 系で rank 反転(発火)+ $p(x_0)>0$ 系の正例(非発火)/ ④ 無限遠の向き入替(発火)+ 正しい向き(非発火)/ ⑤ $m_r$ を 4→3 に改竄し総和 12 を破る(発火)/ ⑥ `curve_model_ref` を inline-only に落として **UNKNOWN であって PASS でない**(縁の固定)/ ★ ⑦ **`curve_model_ref` を欄ごと削除**して **missing-both が素通りしない**(便 102 F102-4.1 と同型の穴の予防)/ ★ ⑧ **$g(T)$ が可約になる候補**で既約因子選択が効くこと(修理 1 の両縁)/ ★ ⑨ **$e\ne2$ の候補**が **UNKNOWN**(宇宙外)になること(修理 2 の縁)/ ★ ⑩ **§3.3 の前件未確認**で **UNKNOWN**(修理 3 の縁)。

---

## 7. 認可の範囲(**便 103 F103-6.3 逐語の再掲**)

> 以上を取り込むことを条件に、**EP-1 は spec 起草と実装 scope のみ条件付き認可**する。**凍結 bytes は不変、二 route は独立、両縁 fixture を置くこと。** これは **IMAGE-MU=PASS、W6_CLOSED、W-6 閉鎖、EP 較正を一切与えない。**

**係の実行順序(案)**: §3 の修理 4 点を spec v21 §5.3.5.2 の条文へ反映 → §5 の W6-P22 → §2 の A′/B 選択(司令塔判断)→ W6-P13〜P21 の逐語起草 → 司令塔検問 → 実装。**§3 が spec に入るまで W6-P13〜P21 を書かない。**

---

## 8. 発効しないもの(明示)

- **本書そのもの**(改版案 v2 草案)。spec の live 正本は **v20**。
- **W6-P13〜P22**(未起草・未採択)。
- **`IMAGE-MU=PASS` / `W6_CLOSED` / W-6 閉鎖 / EP 較正**(いずれも与えられない)。
- **§3.2 の (2a)/(2b) の選択**・**§2.2 の A′/B の選択**(司令塔判断待ち)。
