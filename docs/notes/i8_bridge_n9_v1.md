# I8 — 比較橋 (5′) の $n=9$ instance(+ I10・I9 の記載差分)v1

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 117)。状態 = candidate。commit していない。**
**正本**: `docs/notes/c2c4_closure_v1.md` §3(C3 inventory)/ `docs/week4-BFC攻略_opus_v2.md` v2.15(定理 B-7・系 B-7′・三層供給・補題 B-9′)/ `docs/amendment_5prime_draft.md` v8 §2(条文案 A = (5′_b))/ `docs/notes/i2_family_rule1_memo_v2.md` §2.4((E-iv) 裁定)/ `docs/notes/hfun_functoriality_v1.md` 命題 HF-1 / `docs/notes/抽出_Kn定義_D1.md` §3–§4。
**規律**: $u$ の値・平方類・封印量に**一切触れていない**。外部文献なし(正典 + repo のみ)。lane 実装の中身には触れていない。

---

## 0. 判定(先に 6 行)

1. **(5′_b) の $n=9$ instance は形式的には 1 行で書ける**(§2)。GLOBAL 層はそのまま降り、**PER-WINDOW は 8 項**残る(§4)。
2. **そのうち 3 項は族 Rule 1 条項で賄える**(便 76 ゲート待ち)、**5 項は $n=9$ 固有の凍結が要る**(§4 の区分)。
3. **I10((E-iv) の $n=9$ instance)は $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$** で、I-2 memo v2 §2.4 の裁定どおり **family Rule 1 側に残る**(§5)。
4. **I9 は両案の記載差分が 4 欄に閉じる**(§6)。数学は変わらず、`root_twist_36_value` の**供給元**だけが変わる。
5. **★ ただし I8 の合成には算術ゲートが 1 本立ちはだかる**(§3.4)。**I3′(|GT(K⁽⁹⁾)|=108)・I6((W2) の商 $(\mathbb Z/18)^\times$)・I7($\mathfrak F_0\cong C_9$, $e=9$)は同時に成立しない** — $9\times6=54\neq108$。**この 3 行のどれが動くかで系 B-7′ の結論($\mathrm{ord}([u^{-1}]_{18})=e$)の $e$ が 9 か 18 かに分かれる。** 本メモはこれを **I8 の最初の必須検分**として立てる。
6. ゆえに **I8 は「材料は揃っているが未合成」ではなく「材料の一つが未確定」**である。UNKNOWN を UNKNOWN と書く。

---

## 1. $n=9$ 窓の助変数(正典からの転記)

| 記号 | $K^{(5)}$(既済) | $K^{(9)}$(本メモ) | 出所 |
|---|---|---|---|
| $n$(奇) | 5 | **9** | 委嘱 |
| $M=2n$ | 10 | **18** | HF-1 の $M:=2n$ |
| $2M=4n$ | 20 | **36** | Rule 1 の root object 準位 |
| $e$($\mathfrak F_0\cong C_e$) | 5 | **9 か 18(未確定 — §3.4)** | I7 / §3.4 |
| 基礎体 $F_n$ | $\mathbb Q(\zeta_{20})$ | **$\mathbb Q(\zeta_{36})$** | 委嘱・Rule 1 |
| 検出器 $H$ | $H_5^{\rm fun}$ | **$H_9^{\rm fun}$** | HF-1 |
| $[P_n:H_n^{\rm fun}]$ | 10 | **18** | HF-1(a) |
| $\mathrm{ord}(X)$ | 10 | **18** | HF-1(b) |
| $\lvert\mathrm{GT}(K^{(n)})\rvert$ | 40 | **108** | I3′(便 75 F2)・D1 §4 導出値 $2n_0\varphi(n_0)$ |
| $\lvert(\mathbb Z/M)^\times\rvert$ | 4 | **6** | $\varphi(18)=6$ |
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
| **P2** | $\mathfrak F_0\cong C_e$・$e$ の値 | $e=9$ か $e=18$ か | **OPEN(§3.4 の算術ゲート)** |
| **P3** | **(W5)** $\Lambda_9$ の $\Phi(\mathfrak F_0)$-安定 | 窓の有限計算 | **閉**(便 75 F2・cross-checked) |
| **P4** | $(Z_{36}$-link$)$ / inventory の `K9` 行 | $t_{36}$ の凍結 | **OPEN**(I9・現状 `not_assessed`) |
| **P5** | **(E-iv)** $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$ | 命名規約 | **OPEN**(I10・§5) |
| **P6** | `root_system_tb2_id`($M=18$ の (TB2) 根系) | artifact の凍結 | **未着手** |
| **P7** | `rule1_root_2M_id`($2M=36$ の field-generator object) | artifact の凍結 | **未着手** |
| **P8** | `b_value_9` の **value commitment**(凍結 2 / BRIDGE-IN) | Model-Builder が $c_9,\ell_9$ から (7.1) で計算 | **未着手**(窓 campaign 待ち) |

### 3.3 CURRENT 層(receipt が発効させるもの)

`[pre-event candidate ⟷ post-receipt operative]` の型はそのまま。**$n=9$ 窓は現在 `inventory(window)=not_assessed`** であり、**`migrated` になるまで B-7 は「(TB4)・$(Z_{36}$-link$)$ を明示前件に持つ conditional theorem」として読む**(BFC v2.15 §9 の二段落規約を逐語適用)。

### 3.4 ★ I8 の最初の必須検分 — **算術ゲート**(本メモの新結果)

C3 inventory の 3 行を並べると **数が合わない**:

```text
I3′ : |GT(K^(9))| = 108                      (便 75 F2・D1 §4 導出値 2n₀φ(n₀) = 2·9·6)
I6  : 1 → 𝔉₀ → GT(K^(9)) → (Z/18)^× → 1 完全   (φ(18) = 6)
I7  : 𝔉₀ ≅ C_9 ・ e = 9                      (便 29 (6.1) の転記・「転記確認のみ」)
      ⇒ |𝔉₀|·|(Z/18)^×| = 9 · 6 = 54  ≠  108 = |GT(K^(9))|
```

機械で全奇 $n$ を表にすると、**ずれは常に factor 2** である:

| $n$ | $M=2n$ | $\lvert\mathrm{GT}\rvert=2n\varphi(n)$ | $\varphi(M)$ | $\lvert\mathrm{GT}\rvert/\varphi(M)$ | $=n$? | $=M$? |
|---|---|---|---|---|---|---|
| 3 | 6 | 12 | 2 | 6 | ✗ | **✓** |
| 5 | 10 | 40 | 4 | 10 | ✗ | **✓** |
| 7 | 14 | 84 | 6 | 14 | ✗ | **✓** |
| **9** | **18** | **108** | **6** | **18** | ✗ | **✓** |
| 11 | 22 | 220 | 10 | 22 | ✗ | **✓** |

さらに正典の群構造(D1 §4・Thm 4.6 (4.23))は $\alpha<2$ で
$$ \mathrm{GT}(K^{(n)})\;\cong\;\mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\mathcal Z_2 $$
であり、$n=9$ では $\lvert\mathrm{Aff}(\mathbb Z/9)\rvert\cdot2=54\cdot2=108$。**$\chi_{18}$ の核**は $\mathrm{Aff}$ の並進部分 $\mathbb Z/9$ と $\mathcal Z_2$ の合成で、$\gcd(9,2)=1$ より
$$ \ker\chi_{18}\;\cong\;\mathbb Z/9\times\mathbb Z/2\;\cong\;C_{18}=C_M . $$

> **⇒ 三択(どれか一つが動く)**
> **(A)** $e=M=2n$(I7 の転記が factor 2 ずれ)— 数の上では最も素直。すると **(6′-ii) の像は $\tau(\mu_{18}[18])=\tau(\mu_{18})$ 全体**になり、系 B-7′ の判定は $\mathrm{ord}([u^{-1}]_{18})=18$。
> **(B)** $\mathfrak F_0\subsetneq\ker\chi_{18}$(I6 の「完全」が実は完全でない/$\mathfrak F_0$ が $\ker$ の指数 2 部分群)— この場合 **(W2) の言明を弱める**必要がある。
> **(C)** I3′ の 108 が別対象($\mathrm{GT}_{\rm arith}$ 等)の位数 — 便 75 F2 の現物確認と D1 §4 の導出値が一致しているので**可能性は低い**。
>
> **本メモは (A)(B)(C) のどれかを決めない。** 決めるには **便 29 (6.1) の原文と (W2) の出所**を照合する必要があり、それは I7 が「**転記確認のみ**」と札を付けた当の作業である。
> **⚠ この検分を通す前に I8 を「閉じた」と言ってはならない** — 系 B-7′ の結論(全射性判定 $\mathrm{ord}([u^{-1}]_M)=e$)の右辺が $9$ か $18$ かは、**判定そのものを変える**。
> **同じ検分は $K^{(5)}$ にも遡及する**($e=5$ と $\ker\chi_{10}\cong C_{10}$ の同型ずれ)。**$n=9$ 固有の問題ではなく族の問題である。**

---

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
| **P2** | $e$ の確定($9$ / $18$) | **§3.4 の検分メモ**(便 29 (6.1) 照合) | 族の問題だが**値の確定**が要る。族条項化は検分後 |
| **P4** | $(Z_{36}$-link$)$ / `K9` 行 | **`Z-norm-seal/v1` §1(4) の migration certificate($n=9$ 版)** または族条項(§6 の両案) | root object の**個別**同一視。§6 で案が二つ |
| **P6** | `root_system_tb2_id` | **$M=18$ の (TB2) 根系 artifact**(ID + digest) | 根系は $M$ ごとの具体物 |
| **P7** | `rule1_root_2M_id` | **$2M=36$ の field-generator object**(ID + digest) | 同上($\zeta_{36}$ の選択) |
| **P8-value** | `b_value_9` / `b_value_source` | **$n=9$ 窓の凍結 2 / BRIDGE-IN bundle**(Model-Builder が $c_9,\ell_9$ から算出) | 条文案 A (F2)「actual 値は個別モデル依存」。**(F3) の順序要件**($u$ 開示・$G_K$ 観測より前)も窓ごと |

> **⇒ PER-WINDOW 残件は 8 項**(P1–P8。うち P3 = (W5) は既に閉)。**族で賄える 3・$n=9$ 固有 5。**
> **⇒ 最短経路**: §3.4 の算術ゲート(P2)→ P1 が族条項で同時に閉じる → 残るは P4・P6・P7・P8-value の**手続き 4 項**。**数学の未決は実質 P2 の一点。**

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
6. **★ 未決の本体は §3.4 の算術ゲート 1 点**($e=9$ か $18$ か)。**これは $n=9$ 固有ではなく族の問題**であり、$K^{(5)}$ にも遡及する。**閉じるまで I8 を閉じたと呼ばない。**

---

## 8. 規律の自己申告

- **UNKNOWN として明示したもの**: §3.4 の三択(A)(B)(C)。本メモは**どれかを決めていない**。決めるには便 29 (6.1) の原文照合が要る。
- **本メモが証明していないもの**: (W2) の族閉鎖(I6)・$\mathfrak F_0$ の同型型(I7)・$t_{36}$ の値。**いずれも「誰が供給するか」を書いただけである。**
- **触れていないもの**: $u$ の値・平方類・封印量・lane 実装・freeze 線の文書(N∞ spec / contract / manifest)。
- **機械計算**: §3.4 の表($\varphi$ と位数の算術)のみ。入力は $n$ と正典の個数式だけで、窓のデータには接していない。
