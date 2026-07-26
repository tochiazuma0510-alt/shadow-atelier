# 掃引 ① r2 の spec 追補 3（§6 計算形と証明書 — 定義のみ）

本書は掃引 ① r2 の計算形実装に必要な §6 の定義と式。戦略・判定方針・可解性の結論は含めない。

---

## 1. 二次写像 F と極化 πB

**`docs/命題_E22三段判定_v1.md` 系 E22.4(§3.5, p142–148)**

$K$ の invariant factor 分解 $K=\bigoplus_{i=1}^r\langle e_i\rangle$、$\mathrm{ord}(e_i)=n_i$ を固定する。

**二次写像の定義**:
$$F:=\pi\ell+\pi\mathcal Q:K\to\mathrm{Ob},$$
$$F(\bar k):=\pi\ell(\bar k)+\pi\mathcal Q(\bar k),$$
ここで
$$\ell(\bar k):=\bigl(b_\theta(\bar f_0,\bar k),\ b_N(\bar f_0,\bar k)\bigr),$$
$$\mathcal Q(\bar k):=\bigl(\theta(s\bar k)s\bar k,\ \sigma^2(s\bar k)\sigma(s\bar k)s\bar k\bigr)\quad(\bar k\in K\text{ ゆえ }C\times C\text{ に値をとる}).$$

**極化(対称)**:
$$\pi B(\bar k,\bar l):=\bigl(b_\theta(\bar k,\bar l),\ b_N(\bar k,\bar l)\bigr),\quad b_\theta(\bar u,\bar v):=\beta(\bar\theta\bar v,\ \bar u),$$
$$b_N(\bar u,\bar v):=\beta(\bar\sigma^2\bar v,\ \bar\sigma\bar u+\bar u)+\beta(\bar\sigma\bar v,\ \bar u).$$

**障害定数**:
$$\omega_0:=\omega(\bar f_0),\quad \omega:=\pi\circ\Xi:\mathcal L\to\mathrm{Ob}.$$

---

## 2. 有限アーベル群上での展開式

**`docs/命題_E22三段判定_v1.md` §6.1(p250–261)**

$\bar k=\sum_ia_ie_i$($0\le a_i<n_i$)のとき:

$$\boxed{\ F(\bar k)\;=\;\sum_{i}\Bigl(a_i\,F(e_i)+\tbinom{a_i}2\,\pi B(e_i,e_i)\Bigr)\;+\;\sum_{i<j}a_ia_j\,\pi B(e_i,e_j)\ } \tag{6.1}$$

**必須の自己検査(postcondition)** — 表の内部整合性検査、実装のバグ露見:
$$\boxed{\ n_i\,F(e_i)+\tbinom{n_i}2\,\pi B(e_i,e_i)=0\quad\text{in }\mathrm{Ob}\qquad(\forall i)\ } \tag{6.2}$$

---

## 3. 普遍 class-5 における Ob の具体形

**`docs/命題_E22三段判定_v1.md` 系 E22.6(§5.3, p223–230)**

$P^{(5)}=F_2/\gamma_6$ の場合、$C$ 上で $\mathcal N_C=1+\sigma+\sigma^2=0$(恒等的に零写像)。したがって:
$$\Lambda(z)=\bigl((1+\theta)z,\ 0\bigr)\quad\text{for }z\in C,$$
$$\operatorname{im}\Lambda=\bigl\{\bigl((1+\theta)z,\ 0\bigr):z\in C\bigr\}=\langle\,(t_5+t_6,\,0)\,\rangle,$$
$$\mathrm{Ob}\cong\bigl(C/\langle t_5+t_6\rangle\bigr)\oplus C\quad(\text{階数 }3).$$

---

## 4. 判定手順(三段)

**`docs/命題_E22三段判定_v1.md` §6.2(p262–268)**

| 段 | 入力 | 出力 | 失敗時の証明書 |
|---|---|---|---|
| **① 線型段** | $\bar A$ 上の $2n\times n$ 整数系 $(1+\bar\theta)\bar f=0$、$\bar{\mathcal N}\bar f=-\bar E_m$ | $\mathcal L=\emptyset$ か、$\bar f_0$ と $K$ の invariant factor 分解 $(e_i,n_i)$ | `unsolvability_certificate`(dual witness $y$: $yM\equiv0$、$yb\not\equiv0$、行列 content hash・modulus・基底順序) |
| **② 線型障害段** | $\omega_0=\pi\Xi(\bar f_0)$、$\pi\ell(e_i)$ | $\mathrm{Ob}$ の中のアフィン部分 | — |
| **③ 二次段** | $\pi\mathcal Q(e_i)$、$\pi B(e_i,e_j)$($i\le j$) | (6.1) の全数評価、$-\omega_0\in F(K)$ か | `lift_obstruction_certificate/v2` |

---

## 5. `central_lift_obstruction/v2` の証明書内容

**`docs/命題_E22三段判定_v1.md` §6.3(p270–285)**

1. **対象**: $A_j$ の PC presentation または collection 多項式の content hash、$\bar A_j$ と $C_j$ の基底・invariant factors、**canonical section の定義**(Hall 正規形の規約)。

2. **線型段**: $M$、$b$ の content hash、$\bar f_0$、$K$ の生成元 $e_i$ と modulus $n_i$、**および $|K|=\prod n_i$ の根拠**(SNF の変換行列 $U,V$ と $\det U,\det V=\pm1$ の検査)。

3. **障害群**: $\Lambda$ の行列、$\operatorname{im}\Lambda$ の生成元、$\mathrm{Ob}$ の invariant factors、$\pi$ の明示行列。

4. **二次表**: $\omega_0$、$F(e_i)$($i=1..r$)、$\pi B(e_i,e_j)$($i\le j$)の**全値**($\mathrm{Ob}$ の座標で)。

5. **自己検査**: (6.2) の $r$ 本すべてが $0$ であること。

6. **全数性**: `parameter_domain_size` $=\prod n_i$、`scanned` $=$ 同数、`value_multiplicity_table`(値ごとの重複度)と `mass_check`($\sum$ 重複度 $=\prod n_i$)。

7. **target 非所属**: $-\omega_0\notin F(K)$ を、重複度表の $-\omega_0$ 欄が $0$ であることとして提示。

8. **独立再計算手順**: checker は保存された boolean や hash を信用せず、**群の積から**
 $$ \theta(f)f\quad\text{と}\quad E_m\sigma^2(f)\sigma(f)f $$
 を再計算する。肯定側は witness $f$ を Hall 座標で与え、**非可換群の積で**両式が $1$ になることを直接確認する(生成条件は別欄)。

**禁止項目**: `kernel_representatives_hash` と `form_values_hash` だけで「全 lift が失敗」を宣言すること。

---

## 6. 自己検査結果

禁止項目スキャン:
- ❌ 「可解」「solvable」「m-full」「解が存在する/存在しない」: 0 件
- ❌ 定理の結論文・判定の決定文・可解/不可解の主張: 0 件

**自己検査: PASS**(定義と式のみ・結論なし)
