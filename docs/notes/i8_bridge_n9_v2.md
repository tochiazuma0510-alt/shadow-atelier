# I8 — 比較橋 (5′) の $n=9$ instance(+ I10・I9 の記載差分)v2

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 117)・**v2 = 裁定 119(算術ゲートの (D) 解消)**。状態 = candidate。commit していない。**

> **【v1 ⇒ v2 の変更は §3.4 と、その live 参照 6 箇所のみ】** — v1 §3.4 が立てた算術ゲート(9×6≠108)は **裁定 119 の (D) = 水準の取り違え**で解消した。**他節(§1 の表の一行を除く)・§2 の (5′_b)@9・§4 の残件区分・§5 の I10・§6 の I9 は不変。**
> **本メモが立てた三択 (A)(B)(C) はいずれも当たらなかった** — 正解は選択肢の外(**(D)**)であった。**自認。**
**正本**: `docs/notes/c2c4_closure_v1.md` §3(C3 inventory)/ `docs/week4-BFC攻略_opus_v2.md` v2.15(定理 B-7・系 B-7′・三層供給・補題 B-9′)/ `docs/amendment_5prime_draft.md` v8 §2(条文案 A = (5′_b))/ `docs/notes/i2_family_rule1_memo_v2.md` §2.4((E-iv) 裁定)/ `docs/notes/hfun_functoriality_v1.md` 命題 HF-1 / `docs/notes/抽出_Kn定義_D1.md` §3–§4。
**規律**: $u$ の値・平方類・封印量に**一切触れていない**。外部文献なし(正典 + repo のみ)。lane 実装の中身には触れていない。

---

## 0. 判定(先に 6 行)

1. **(5′_b) の $n=9$ instance は形式的には 1 行で書ける**(§2)。GLOBAL 層はそのまま降り、**PER-WINDOW は 8 項**残る(§4)。
2. **そのうち 3 項は族 Rule 1 条項で賄える**(便 76 ゲート待ち)、**5 項は $n=9$ 固有の凍結が要る**(§4 の区分)。
3. **I10((E-iv) の $n=9$ instance)は $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$** で、I-2 memo v2 §2.4 の裁定どおり **family Rule 1 側に残る**(§5)。
4. **I9 は両案の記載差分が 4 欄に閉じる**(§6)。数学は変わらず、`root_twist_36_value` の**供給元**だけが変わる。
5. **v1 が立てた算術ゲート(9×6≠108)は解消した**(§3.4・裁定 119 の **(D) = 水準の取り違え**)。**完全列の水準は $2M=4n=36$** であって $M=18$ ではない: $\varphi(36)=12$、$108/12=9$ ⟹ **$\mathfrak F_0\cong C_9$・$e=n=9$ は不変**。**v1 の $\ker\chi_{18}\cong C_{18}$ も正しい** — それは $M$ 水準の核であり、$\mathfrak F_0$($2M$ 水準の核)ではない(§3.4 に和解の完全列)。
6. ゆえに **系 B-7′ の判定「$\mathrm{Ih}_N$ 全射 $\iff\mathrm{ord}([u^{-1}]_M)=e=n$」は不変**であり、**$K^{(5)}$ への遡及懸念も消滅**した。残るのは **(W2)-fam の形式証明**(第二数学者・走行中)と**便 29 (6.1) 原文照合**の二本で、これは **P2 の残件**として §3.2・§4.2 に残す。

---

## 1. $n=9$ 窓の助変数(正典からの転記)

| 記号 | $K^{(5)}$(既済) | $K^{(9)}$(本メモ) | 出所 |
|---|---|---|---|
| $n$(奇) | 5 | **9** | 委嘱 |
| $M=2n$ | 10 | **18** | HF-1 の $M:=2n$ |
| $2M=4n$ | 20 | **36** | Rule 1 の root object 準位 |
| $e$($\mathfrak F_0\cong C_e$) | 5 | **9**($=n$・§3.4 で確定) | I7 / §3.4(裁定 119) |
| 基礎体 $F_n$ | $\mathbb Q(\zeta_{20})$ | **$\mathbb Q(\zeta_{36})$** | 委嘱・Rule 1 |
| 検出器 $H$ | $H_5^{\rm fun}$ | **$H_9^{\rm fun}$** | HF-1 |
| $[P_n:H_n^{\rm fun}]$ | 10 | **18** | HF-1(a) |
| $\mathrm{ord}(X)$ | 10 | **18** | HF-1(b) |
| $\lvert\mathrm{GT}(K^{(n)})\rvert$ | 40 | **108** | I3′(便 75 F2)・D1 §4 導出値 $2n_0\varphi(n_0)$ |
| $\lvert(\mathbb Z/M)^\times\rvert$ | 4 | **6** | $\varphi(18)=6$($M$ 水準・**(W2) の商ではない**) |
| $\lvert(\mathbb Z/2M)^\times\rvert$ | 8 | **12** | $\varphi(36)=12$($2M$ 水準・**(W2) の商はこちら**) |
| link 名 | $(Z_{20}$-link$)$ | **$(Z_{36}$-link$)$** | I9 |

---

## 2. (5′_b) の $n=9$ instance

条文案 A(Rule 1 v1.4 §8.4.1)の判定式を $M=18$ へ instance 化する。**式の形は 1 文字も変えない**:

$$ \boxed{\ \rho_9\bigl(\operatorname{Ih}_N(\gamma)\bigr)\;=\;\tau_9\bigl(\kappa_9(\gamma)^{\,b_9}\bigr)\qquad(\forall\gamma\in G_{F_9}),\qquad b_9\in(\mathbb Z/18)^\times.\ } \tag{5$'_b$@9} $$

補題 B-9′(a)(BFC v2.15 §10.1・two-mathematician PASS)より、**捻れ指数は二因子に分解する**:
$$ b_9\;=\;b_{\rm op}\;=\;\bigl(\bar t_{18}\,\varepsilon\bigr)^{-1}\bmod 18,\qquad \bar t_{18}:=t_{36}\bmod 18 . $$

- **$\varepsilon$ 側**(framework-global)は **GLOBAL 層**が供給(§3.1)。
- **$\bar t_{18}$ 側**(root object shift)は **PER-WINDOW 層**が供給 = **I9**(§6)。
- 両方が $1$ になったとき、**exact (5′) が route **(R-a)** で回収**される:
$$ \varepsilon=1\ \wedge\ t_{36}=1\ \Longrightarrow\ \bar t_{18}=1\ \Longrightarrow\ b_9=1\ \Longrightarrow\ (5') \text{@}9:\ \rho_9(\operatorname{Ih}_N(\gamma))=\tau_9(\kappa_9(\gamma)). $$
**結果 record の `exact_recovery_path` には (R-a) と書く**(条文案 A の 8.4.1 の 2 route のうち、現行 BFC proof を採るため)。**(R-b)(TB4-E alternate)と前件を混ぜない。**

> **⚠ 型の注意(K⁵ の轍)**: $\bar t_{18}=1$ は $(Z_{36}$-link$)$ と**同値ではない**。link は $t_{36}=1$($\bmod\,36$)であり、$\bar t_{18}=1$ はその $\bmod\,18$ 帰結にすぎない。条文案 A (F4) の `root_twist_36_value` と `root_twist_mod_18_value` を**別欄で**記録する(K⁵ で $2M$ と $M$ を混ぜた誤りの再発防止)。

---

## 3. 三層供給 — 何が降りて何が要るか

BFC v2.15 の 4 分類(`[global seal-relative]` / `[per-window inventory]` / `[pre-event candidate ⟷ post-receipt operative]` / `[historical]`)をそのまま使う。

### 3.1 GLOBAL 層(そのまま降りる — $n=9$ で新たに何もしない)

| 項目 | 供給元 | 型 | $K^{(5)}$ での典拠 |
|---|---|---|---|
| **(TB1)(TB3)** | retained framework | `[global]` | BFC §13.1 |
| **(TB4)**(exact $\varepsilon=1$ の向き) | `Z-norm-seal/v1` + retained TB4-3/A3 | `[global seal-relative]` | BFC v2.15 §0 第 6 項 |
| **(TB4$^{\rm u}$)**(向き不問の inertia 比較) | 独立枠組み仮定 | `[global]` | BFC §8.1 |
| **(CAL)** $\alpha^{\rm Ih}=\alpha^{\rm std}$ | $A_5$ v4 §1.4 | `[global]`(**窓非依存**) | I5(閉) |
| **B-7 / B-7′ / B-9′ の証明そのもの** | BFC v2.15 | `[global]` | 数学は窓に依存しない |
| **(6′-ii) の $\rho_0$ 忠実**+像の記述 | 命題 K5-1(**全奇 $n$**) | `[global]`(族定理) | I4(閉) |
| **(W3)(W4)** | 命題 HF-1(**全奇 $n\ge3$**) | `[global]`(族定理) | I2(閉) |
| **(W1)** | c2c4 §1(Thm 4.3 + (CAL)) | `[global]`(族供給 W1-fam) | I1(閉) |

> **★ $K^{(5)}$ の轍からの教訓**: 上の 8 行は **$n=9$ で再証明しない**。ここを窓ごとに焼き直すと、K⁵ で起きた「同じ定理を窓ごとに別 ID で持つ」型の二重正本を招く。**降りてくるものは降ろす。**

### 3.2 PER-WINDOW 層(窓ごとに供給が要る)

| # | 項目 | 何が窓固有か | 現状 |
|---|---|---|---|
| **P1** | **(W2)** の $n=9$ instance | 完全列と $\tilde\chi\circ\mathrm{Ih}=\chi_{18}$ | **OPEN**(I6・族閉鎖の見込みあり) |
| **P2** | **(W2)-fam** の形式証明($2M$ 水準の完全性)+ 便 29 (6.1) 原文照合 | $\mathfrak F_0\cong C_9$・$e=n=9$ は**確定**(§3.4)。残るのは**形式閉鎖** | **OPEN(形式証明)** — 第二数学者が走行中 |
| **P3** | **(W5)** $\Lambda_9$ の $\Phi(\mathfrak F_0)$-安定 | 窓の有限計算 | **閉**(便 75 F2・cross-checked) |
| **P4** | $(Z_{36}$-link$)$ / inventory の `K9` 行 | $t_{36}$ の凍結 | **OPEN**(I9・現状 `not_assessed`) |
| **P5** | **(E-iv)** $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$ | 命名規約 | **OPEN**(I10・§5) |
| **P6** | `root_system_tb2_id`($M=18$ の (TB2) 根系) | artifact の凍結 | **未着手** |
| **P7** | `rule1_root_2M_id`($2M=36$ の field-generator object) | artifact の凍結 | **未着手** |
| **P8** | `b_value_9` の **value commitment**(凍結 2 / BRIDGE-IN) | Model-Builder が $c_9,\ell_9$ から (7.1) で計算 | **未着手**(窓 campaign 待ち) |

### 3.3 CURRENT 層(receipt が発効させるもの)

`[pre-event candidate ⟷ post-receipt operative]` の型はそのまま。**$n=9$ 窓は現在 `inventory(window)=not_assessed`** であり、**`migrated` になるまで B-7 は「(TB4)・$(Z_{36}$-link$)$ を明示前件に持つ conditional theorem」として読む**(BFC v2.15 §9 の二段落規約を逐語適用)。

### 3.4 算術ゲートの解消 — **(D) 水準の取り違え**【v2・裁定 119】

> **v1 の指摘(記録)**: C3 inventory の 3 行 — I3′($\lvert\mathrm{GT}(K^{(9)})\rvert=108$)・I6((W2) の商が $(\mathbb Z/18)^\times$)・I7($\mathfrak F_0\cong C_9$) — が $9\times6=54\neq108$ で合成しない、と本メモ v1 が立てた。**本日別線で二度観測された同一現象の第三観測**であった。
> **v1 が挙げた三択 (A)(B)(C) はいずれも当たらない。正解は選択肢の外にあった。自認。**

#### (D) 解消 — 完全列の水準は $2M=4n$ である

$$ 1\;\longrightarrow\;\mathfrak F_0\;\longrightarrow\;\mathrm{GT}(K^{(9)})\;\xrightarrow{\ \tilde\chi_{36}\ }\;(\mathbb Z/36)^\times\;\longrightarrow\;1 $$

| 量 | 値 | 検算 |
|---|---|---|
| $\lvert\mathrm{GT}(K^{(9)})\rvert$ | $108$ | $2n\varphi(n)=2\cdot9\cdot6$ |
| $\lvert(\mathbb Z/36)^\times\rvert$ | $12$ | $\varphi(36)=\varphi(4)\varphi(9)=2\cdot6$ |
| $\lvert\mathfrak F_0\rvert$ | $\mathbf 9$ | $108/12=9$ |
| **合成** | $9\times12=108$ | **✓ 成立** |

**族恒等式として書くと(全奇 $n$・機械確認済)**:
$$ \boxed{\ \frac{\lvert\mathrm{GT}(K^{(n)})\rvert}{\varphi(2M)}=\frac{2n\varphi(n)}{\varphi(4n)}=\frac{2n\varphi(n)}{2\varphi(n)}=n\ }\qquad(n\ \text{奇}) $$
($n$ 奇より $\varphi(4n)=\varphi(4)\varphi(n)=2\varphi(n)$。$n=3,5,7,9,11,15$ で実測一致。)
**ゆえに $\mathfrak F_0\cong C_n$・$e=n$ は全奇 $n$ で数の上でも整合する。**

#### 二つの計算の和解 — **v1 の $C_{18}$ も正しい**

v1 が計算した $\ker\chi_{18}\cong C_{18}$ は **$M$ 水準の核**であって $\mathfrak F_0$ ではない。両者は次の完全列で結ばれる:

$$ 1\;\longrightarrow\;\underbrace{\ker\tilde\chi_{36}}_{=\ \mathfrak F_0\ \cong\ C_9}\;\longrightarrow\;\underbrace{\ker\chi_{18}}_{\cong\ C_{18}}\;\longrightarrow\;\ker\bigl((\mathbb Z/36)^\times\twoheadrightarrow(\mathbb Z/18)^\times\bigr)\;\longrightarrow\;1 $$

右端の核は **位数 2**($\varphi(36)/\varphi(18)=12/6=2$)で、具体的に $\{1,\,19\}\bmod 36$ である($19=18+1$ は $\gcd(19,36)=1$ かつ $19\equiv1\bmod18$)。**したがって $18=9\times2$** であり、**v1 の factor 2 のずれは「$M$ 水準へ落ちる際に増える 2」そのもの**だった。**二つの計算は矛盾しない — 水準が違っただけである。**

#### 独立較正(裁定 119 の 2 点 + 本メモの確認)

| # | 較正点 | $e=n$ 側の予測 | $e=M$ 側の予測 | 実測 |
|---|---|---|---|---|
| C1 | $K^{(3)}$ の $\mathrm{ord}([u_3^{-1}]_6)$ | $3\ (=n)$ | $6\ (=M)$ | **$3$** ⟹ $e=M$ は**反証** |
| C2 | link の水準($K^{(3)}$: $Z_{12}=4\cdot3$ / $K^{(5)}$: $Z_{20}=4\cdot5$) | $2M=4n$ 水準 | — | **$2M$ 水準**の実績 ⟹ (D) と整合 |
| C3 | `search/certs/k9_package_20260728_r2.json`(各 charming $m$ の繊維) | $9$ | $18$ | **$9$** |

#### 帰結(I8 にとって何が変わったか)

1. **系 B-7′ の判定は不変**: $$ \mathrm{Ih}_N\ \text{全射}\iff\mathrm{ord}\bigl([u^{-1}]_M\bigr)=e=n=9 . $$ **右辺は $9$ である**($18$ ではない)。**判定の形も $M=18$ 準位での位数を見る点も v1 から変わらない。**
2. **$K^{(5)}$ への遡及懸念は消滅**: $n=5$ で $\varphi(20)=8$・$40/8=5=n$。**K⁵ campaign の $e=5$ は正しかった。** v1 が「族の問題であり $K^{(5)}$ にも遡及する」と書いたのは**誤りで、遡及すべき瑕疵は存在しない。自認。**
3. **(6′-ii) の像**は $\tau(\mu_{18}[9])$(位数 9 の部分群)であり、v1 が (A) 案で述べた「$\mu_{18}$ 全体」**ではない**。
4. **残るのは形式閉鎖の二本**(下記)。**数値の整合はもう問題ではない。**

> **⇒ P2 の残件(改訂後)**: **(a) (W2)-fam の証明** — 「$2M$ 水準で $1\to\mathfrak F_0\to\mathrm{GT}(K^{(n)})\xrightarrow{\tilde\chi_{2M}}(\mathbb Z/2M)^\times\to1$ が全奇 $n$ で完全」の形式証明(**第二数学者が走行中**)。**(b) 便 29 (6.1) の原文照合**($\mathfrak F_0\cong C_n$・$e=n$ の転記確認 — I7 が「転記確認のみ」と札を付けた当の作業)。
> **⇒ 位数勘定は (a) の代用にならない。** 上の $108=9\times12$ は**必要条件の一致**であって、完全列そのもの(単射性・全射性・$\tilde\chi$ と $\mathrm{Ih}$ の両立)を与えない。**I8 は (a)(b) に依存する。**

## 4. PER-WINDOW 残件と供給文書案

### 4.1 族 Rule 1 条項で賄える(便 76 の族条項ゲート待ち)— **3 項**

| # | 項目 | 供給文書案 | 根拠 |
|---|---|---|---|
| **P1** | (W2) の $n=9$ instance | **族条項**「Thm 4.3 (4.12) + $K_{\rm ord}^{(n)}=2n$ から全奇 $n$ で (W2) を読み取る」1 条 | c2c4 §3 の I6 所見(族閉鎖の見込み)。**§3.4 の算術ゲートと同時に決着する** |
| **P5** | (E-iv) 命名規約 | **family Rule 1 §1.3 の (1.8) 族版**(§5 に条文案) | I-2 memo v2 §2.4「(E-iv) は I-2 残留」 |
| **P8-rule** | `b_rule_commitment`((7.1) の**規則**) | **family Rule 1 §7.1**(規則は窓非依存・digest 1 個) | 条文案 A (F1)「凍結 1 で固定するのは規則」 |

### 4.2 $n=9$ 固有の凍結が要る — **5 項**

| # | 項目 | 供給文書案 | なぜ族で賄えないか |
|---|---|---|---|
| **P2** | **(W2)-fam の形式証明** + 便 29 (6.1) 原文照合 | **(a) 第二数学者の (W2)-fam 証明**(走行中)・**(b) 便 29 (6.1) 照合メモ** | $e=n=9$ は§3.4 で**確定済**。残るのは**形式閉鎖**であり、閉じれば §4.1 の P1 と同時に族条項化できる |
| **P4** | $(Z_{36}$-link$)$ / `K9` 行 | **`Z-norm-seal/v1` §1(4) の migration certificate($n=9$ 版)** または族条項(§6 の両案) | root object の**個別**同一視。§6 で案が二つ |
| **P6** | `root_system_tb2_id` | **$M=18$ の (TB2) 根系 artifact**(ID + digest) | 根系は $M$ ごとの具体物 |
| **P7** | `rule1_root_2M_id` | **$2M=36$ の field-generator object**(ID + digest) | 同上($\zeta_{36}$ の選択) |
| **P8-value** | `b_value_9` / `b_value_source` | **$n=9$ 窓の凍結 2 / BRIDGE-IN bundle**(Model-Builder が $c_9,\ell_9$ から算出) | 条文案 A (F2)「actual 値は個別モデル依存」。**(F3) の順序要件**($u$ 開示・$G_K$ 観測より前)も窓ごと |

> **⇒ PER-WINDOW 残件は 8 項**(P1–P8。うち P3 = (W5) は既に閉)。**族で賄える 3・$n=9$ 固有 5。**
> **⇒ 最短経路**: **(W2)-fam の証明(P2-a)→ P1 が族条項で同時に閉じる** → 残るは P4・P6・P7・P8-value の**手続き 4 項**。**数学の未決は実質 P2-a の一点**(数値の整合ではなく**完全列の証明**)。

---

## 5. I10 —(E-iv)の $n=9$ instance

I-2 memo v2 §2.4 の裁定(**(E-iv) は I-1 へ渡らず family Rule 1 = I-2 側に残る**)に従い、$n=9$ では次の 1 条を要する。

> **(E-iv)@9(命名規約)**
> $$ \boxed{\ \tau\bigl(\zeta_{18}^{\rm Rule}\bigr)\;=\;\tau\bigl(X_9\bigr)\ } $$
> ここで $\zeta_{18}^{\rm Rule}$ は **family Rule 1 の較正指定**(補題 U: $\Phi_{36}$ の根のうち $\operatorname{Im}>0$ かつ $\operatorname{Re}$ 最大 $=e^{2\pi i/36}$ から誘導される $M=18$ 準位の根)、$X_9$ は $H_9^{\rm fun}$ に対する marking 元。

**供給できるもの / できないもの(型の分離 — ★教材 T5)**:
- **HF-1(b) が与えるのは $\mathrm{ord}(X_9)=18=M$ という「量」**。これは全奇 $n$ で証明済み(GLOBAL)。
- **(E-iv) が要求するのは「どの根を $X_9$ と呼ぶか」という「名前」**。量から名前は出ない。**ここが I-2 残留の実質。**
- ゆえに **条文は family Rule 1 §1.3 に置く**(窓ごとに書き下ろさない)。**$n=9$ 側で要るのは「族条項を $M=18$ に適用した」という 1 行の宣言と、`rule1_root_2M_id`(P7)との突合**である。

**記録欄(条文案 A (F4) の schema へ追加する 2 欄)**:
```text
naming_convention_id   = family-Rule1 §1.3 (1.8) の族版 clause ID + digest
naming_instance_M      = 18                      # 適用先の準位
```

---

## 6. I9 — 両案の**記載差分だけ**(採否は便 76 の族条項ゲート)

数学は両案で同一である。**変わるのは `root_twist_36_value` の供給元と、その根拠 ID の欄だけ**。

| 欄 | **案 α: 個別 link 凍結** | **案 β: 族条項適用** |
|---|---|---|
| `root_twist_36_value` | `Z-norm-seal/v1` の **$n=9$ migration certificate** が $t_{36}=1$ を供給 | **族条項**(全奇 $n$ で $t_{2n\cdot2}=1$)から降ろす |
| `link_supply_source` | `seal:migration_record@K9` + digest | `family-clause:root-normalization` + digest |
| window inventory の `K9` 行 | `migrated`(certificate 受領後) | `migrated_by_family_clause` |
| `exact_recovery_path` | **(R-a)**(変わらず) | **(R-a)**(変わらず) |

**共通(どちらでも変わらない)**:
- $b_9=(\bar t_{18}\varepsilon)^{-1}$ の**式**(補題 B-9′(a))
- `root_twist_36_value` と `root_twist_mod_18_value` を**別欄**に置く規律(§2 の型注意)
- **供給前は `[pre-event candidate]`**、receipt 発効後に `[post-receipt operative]`(BFC v2.15 §9 の二段落)

> **⇒ 記載差分は 3 欄**(`root_twist_36_value` の供給元・`link_supply_source`・inventory 行の語)。**採否がどちらでも I8 本体の数学は 1 行も変わらない。**

---

## 7. まとめ

1. **(5′_b)@9**: $\rho_9(\mathrm{Ih}_N(\gamma))=\tau_9(\kappa_9(\gamma)^{b_9})$、$b_9=(\bar t_{18}\varepsilon)^{-1}\bmod18$、exact 回収は route (R-a)。
2. **GLOBAL 8 行はそのまま降りる**(再証明しない)。
3. **PER-WINDOW 残件 8 項** — 族で賄える 3 / $n=9$ 固有 5。
4. **I10 は family Rule 1 §1.3 の族条項 + 適用宣言 1 行**(量と名前の型分離)。
5. **I9 は記載差分 3 欄のみ**(数学は不変)。
6. **算術ゲートは (D) で解消**($2M$ 水準・$e=n=9$・$K^{(5)}$ 遡及懸念も消滅)。**未決の本体は (W2)-fam の形式証明(P2-a)1 点**であり、**位数勘定はその代用にならない**。**閉じるまで I8 を閉じたと呼ばない。**

---

## 8. 規律の自己申告

- **v1 の誤り(自認)**: §3.4 で立てた三択 (A)(B)(C) は**いずれも当たらなかった**(正解は水準の取り違え = (D))。また v1 は「$K^{(5)}$ にも遡及する」と書いたが、**遡及すべき瑕疵は存在しなかった**。
- **UNKNOWN として残るもの**: **(W2)-fam の形式証明**(P2-a・第二数学者走行中)と**便 29 (6.1) の原文照合**(P2-b)。**位数の一致は必要条件であって完全列の証明ではない。**
- **本メモが証明していないもの**: (W2) の族閉鎖(I6・P2-a)・$\mathfrak F_0$ の同型型の原文照合(I7・P2-b)・$t_{36}$ の値。**いずれも「誰が供給するか」を書いただけである。**
- **触れていないもの**: $u$ の値・平方類・封印量・lane 実装・freeze 線の文書(N∞ spec / contract / manifest)。
- **機械計算**: §3.4 の表($\varphi$ と位数の算術・族恒等式 $\lvert\mathrm{GT}\rvert/\varphi(4n)=n$ の $n=3..15$ 実測・$(\mathbb Z/36)^\times\to(\mathbb Z/18)^\times$ の核 $\{1,19\}$ の明示)のみ。入力は $n$ と正典の個数式だけで、**窓のデータには接していない**。
