# [P1-D2] R-1 正準化 v2 — falsifier 監査反映 + 【D2-GAP-4 改】ゲート prereg

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔【CP】(裁定 1083 + 裁定 1086 の一本化)
**v1 を全面置換**(`p1d2_r1_canonicalization_v1.md`・commit `b036267d`・上書きせず版で残す)
入力 = falsifier 前哨監査 `fals_p1d2_r1_audit_v1.md`(commit `16dd7ca8`)・実装係速達 `ops/express/20260813_implementer_D2GAP4_構成の二義性.md`・
　　　`w9_E_model_v1.md`・`t3_spec_and_C2_calib_v1.md` §1・cert `w9_k3_p1_0d_check_v1_20260812` / `r13_p1_0_blocks_v1_20260812` / `p1_d2_scan_v2_20260813`
本ターンの新規計算の詳細記録 = `d2gap4_gate_adjudication_v1.md`(census の生データ・本書はその上に立つ)
⚠ $u$/$c$ 非接触・prereg 非抵触・封印非接触。**格: candidate**(Sol 未監査・verified ではない)。

---

## §0 ★★★ 結論(v2)

1. ⚠ **【命題 CAN-1】(v1 §1.5)は撤回します**。前提「$\lambda_9$ が類で一意」は**偽**(falsifier B-1・機械反証)、正しく述べ直すと**恒真**(B-2)。**overclaim を認めます**。
2. ⚠ さらに **falsifier が指摘した以上に深い穴**を私自身の census で見つけました:代数走査が拾った **4 点は候補の全体ではなく 72 本中 4 本**【D2-GAP-6】。
3. ★★★ **その代わりに、前提なしの結果が 1 本立ちました**(本書 §4):

$$\boxed{\ \lambda_9\ \text{の二次分解体は }P_1=(0,-2)=\ominus Q_0\ \text{に対応する }E\ \text{の 2 重被覆である}\quad\textbf{【CAN-1}'\textbf{】}\ }$$
$$\text{(一意性仮定なし・moduli 体仮定なし・算術入力ゼロ・機械 census + Galois 同変性のみ)}$$

4. ★ **モデルは $W_9$ ではなく $W(P_1)$ と名乗ります**(監査 M-4):
$$\boxed{\ W(P_1):\ x^2w^3-27\zeta_3\,y\,(w+1)=0\quad\text{over}\quad E:\ y^2+3\zeta_3xy+2y=x^3\ }$$
$$\boxed{\ W(P_1)=W_9\ \Longleftrightarrow\ \textbf{【CAN-2】}(=\lambda_9\ \text{の Tschirnhaus 束が split)}\quad\textbf{— 未決・§8 の 1 走行で決まる}\ }$$

5. ★ **監査 M-5 への回答は肯定**: $E\to\mathbf P^1_t$ の明示式は既存資産から復元でき、**$\mathbf Q(\zeta_3)$-有理**です:
$$\boxed{\ t=-\frac{y^2}{4}\ }\qquad(\text{独立検算 2 本・§7.2})$$
⟹ **合成 $\lambda:W(P_1)\to\mathbf P^1_t$ 全体が $\mathbf Q(\zeta_3)$ 上に定義される** ⟹ 【D2-GAP-4 改】は**実装可能**(実装係の (B) 読みが正しく、その障害は存在しませんでした)。

---

## §1 v1 からの改訂一覧(監査項目 → 反映先)

| 監査 | 内容 | 本書での処理 |
|---|---|---|
| **B-1** | CAN-1 の前提は偽(passport を実現する推移群 13 本) | ★ **受諾・撤回**(§5)。**さらに強く**: 幾何的に関連する母集団は **72 本**(§4.2) |
| **B-2** | 直すと前提⟺結論の恒真 | ★ **受諾**(§5.1)。恒真でない置換を §4.4 に用意 |
| **M-1** | 324 は既に cert 済・[P1-0d] 参照は $E$ 側(36)の誤り | ★ **受諾**(§8.1 で cert 2 本を明示引用)。⚠ **ただし逆向きの修正 1 件**: 位数 324 は**被覆を一意にしない**(§4.3・324 の被覆は 3 本) |
| **M-2** | D2-GAP-5 は既閉 | ★ **受諾 + 強化**: $\sigma_0$ が 18-cycle ゆえ**任意の**被覆で一意(§2.3)⟹ 監査の留保($\mathrm{Mon}=$T18n140 限定)も外れる |
| **M-3** | 4 分岐の行き先を事前記載 | ★ **受諾**(§8.3)。⚠ **census により 2 分岐は事前に排除**され、予言つき prereg になる |
| **M-4** | $W_9$ 名乗りは過剰 | ★ **受諾**(§0・§7 の全箱を $W(P_1)$ へ) |
| **M-5** | 定義体は $W\to E$ 層まで | ★ **受諾のうえ拡張**: $E\to\mathbf P^1_t$ も $\mathbf Q(\zeta_3)$-有理(§7.2)⟹ 合成まで言える(CAN-2 条件つき) |
| **m-1** | $A_0(R)=A_0(R')$ の箱は $R=R'$ で偽 | ★ 受諾(§2.1 で $R\ne R'$ を明記) |
| **m-2** | ORD9 の仮定と証明が非整合 | ★ 受諾(§6.2 で $\deg R\ge4\Rightarrow g\ge3>0$ に差し替え) |
| **m-3** | $S_3$ 判定に既約性が抜けている | ★ 受諾(§6.3 に Newton 多角形 1 行) |
| **m-4** | 自己同型 $\psi(R)=Q_0\ominus R$ の見落とし | ★ 受諾(§2.2)。$\psi$ の**固定点集合 = 4 点そのもの**という形で補完 |
| **m-5** | cert の規約自己矛盾(CV-9 型) | ★ 受諾(§7.1 に規約宣言) |
| **m-6** | V1 の述語名が実体と不一致 | ★ 受諾(§2.4 に記帳・実装係へ差し戻し) |
| **m-7** | 「0 ビット」は判別力の話 | ★ 受諾(§2.4 で語を限定) |
| **m-8** | 「独立の傍証」に力はない | ★ **受諾**。⟹ ★ §4 が**その欠けていた力を供給**します(傍証 → 定理) |
| **m-9** | norm が平方になる理由 | ★ 受諾(§3.1 に 1 行) |

---

## §2 【問 1】4/4 PASS の解釈(v1 §1 の継承 + 修理)

### 2.1 (V4) は [D2-1] の恒等的帰結 — 判別力 0 ビット

$A_0^{(P)}(R):=X(R\ominus P)-X_P$ は $\lvert2P\rvert$ の定める**次数 2 写像**で、その対合は $\iota_P(R)=[2]P\ominus R$。よって

$$\boxed{\ R\ne R'\ \text{のとき}\quad A_0(R)=A_0(R')\iff R\oplus R'=[2]P\ }\qquad(\text{m-1 修理: }R=R'\ \text{は除く})$$

走査は $[2]P=Q_0$ の 4 点上で行われ、[D2-1] は $B_1\oplus B_2=Q_0$ を確定済み ⟹ **(V4) は 4 点すべてで論理的必然として PASS**。
V1・V3・V5 も構成上の恒等式、V7 は空虚、V6 は紙で閉じ(§6)4 点すべてで自動 ⟹

$$\boxed{\ \textbf{見張り体系 V1–V7 の}\textbf{判別力}\textbf{は合計 0 ビット}\ }\qquad(\text{m-7 修理: 「無価値」ではない — §2.4})$$

### 2.2 4 点は $E$ 上の被覆として互いに非同型(m-4 の補完込み)

$\pi_*\mathcal O_W$ の Tschirnhaus 束 $\mathcal E$ は $\deg\mathcal E=3$。split 枝 $\mathcal E\cong\mathcal O(P)\oplus\mathcal O(2P)$ では $M=\mathcal O(P)$ が被覆の不変量 ⟹ $P$ が復元できる。
標識を動かす自己同型がないことの**完全版**(m-4):

- $j(E)=9261/8\notin\{0,1728\}$ ⟹ $\mathrm{Aut}(E)=\{\pm1\}$;$[-1]$ は 3-等分点 $Q_0$ を動かす ⟹ $\mathrm{Aut}(E,Q_0,Q_\infty)=1$
- ⚠ **しかし被覆の同型は $Q_0\leftrightarrow Q_\infty$ の交換も許す**。それを実現するのは $\psi(R):=Q_0\ominus R$ のみ($\psi(Q_0)=Q_\infty$, $\psi(Q_\infty)=Q_0$)。$B_1\oplus B_2=Q_0$ ⟹ $\psi(B_1)=B_2$ ⟹ ★ **$\psi$ は分岐データを完全に保つ**。
- ★ **結論は救われる**: $[2]P=Q_0$ ゆえ $\psi(P)=Q_0\ominus P=[2]P\ominus P=P$。
$$\boxed{\ \textbf{4 点は}\ \psi\ \textbf{の固定点集合そのもの}\ (\{R:[2]R=Q_0\}=\mathrm{Fix}(\psi))\ \Longrightarrow\ M=\mathcal O(P)\ \textbf{の不変性は無傷}\ }$$
⟹ $\{Q_0,Q_\infty\}$ を setwise に保つ自己同型は $\{\mathrm{id},\psi\}$ の 2 個、どちらも 4 点を各々固定 ✔
- ⚠ **語の修正**(m-4): 「4 本の別の**曲線**」は言い過ぎ。正しくは「**$E$ 上の被覆として非同型な 4 本**」。

### 2.3 ★【D2-GAP-5】閉鎖 — 紙 1 行(監査 M-2 の強化)

$\lambda_9$ の $\sigma_0$ は **18-cycle**(cert / 本ターン測定 §4.1)。任意のブロック系は $\langle\sigma_0\rangle$ のブロック系でもあり、巡回群のブロック系は**位数の約数と 1 対 1** ⟹ 各サイズにつき**一意**。
★ この論証は「$\mathrm{Mon}=$T18n140」を使いません ⟹ **passport を満たす任意の被覆で (3,6) ブロック系は一意** ⟹ 監査 M-2 の留保も外れます。
機械確認: `AllBlocks` はサイズ 3・9 の代表を各 1 個(本ターン + falsifier `fals_lam9_structure.g` + cert `r13_p1_0_blocks_v1` の `nontrivial_block_systems_count: 2`)⟹ **三重一致**。

### 2.4 記帳(m-6, m-7, m-5)

- **m-7**: 「0 ビット」= **4 候補を判別する情報が 0 ビット**の意。走査自体は各 $P$ の $c,\rho$(モデルの実パラメータ)を産出しており無価値ではない。
- **m-6**: cert の `V1_pole_order2_probe_...` は述語 `|A0_near| > 1e10` で**極の位数 2 を判定していない**(単純極でも通る)⟹ **実装係へ名称是正の差し戻し**。★ ただし記録値 $4.0$ は厳密値と一致($A_0=-2y/x^2$、$P_1$ で $y\to-2$、$x$ が局所母数 ⟹ $A_0\sim4/x^2$)⟹ 独立突合 1 本増 ✔
- **m-5(CV-9)**: 本書の**規約を宣言**します — **$z^3+Az+B$**、$\mathcal D=-4A^3-27B^2$、$\rho:=\alpha^3/\beta^2=-27/(4c)$。cert `p1_d2_scan_v2` の `watches_V1_V7.V6` の $z^3=Az+B$ 表記は**誤記**であり、script 実装は $z^3+Az+B$ 側 ⟹ **cert 側を次版で訂正**(上書きせず)。

---

## §3 4 点の Galois 構造(v1 §1.5 の継承・m-8/m-9 修理)

### 3.1 既約性(m-9 の 1 行補完)

4 点 = $\{P_1=(0,-2)\}\cup\{x^3-2a_1x-8=x^3+(3-3\sqrt3i)x-8\ \text{の 3 根},\ y=2\}$。
$f\in\mathbf Q(\zeta_3)[x]$ かつ $[F:\mathbf Q(\zeta_3)]=2$($F=\mathbf Q(\zeta_{12})$)⟹ **$N_{F/\mathbf Q}(f)=(f\bar f)^2$ は自動的に平方**(m-9: 平方性は証拠ではない)。$f\bar f=x^6+6x^4-16x^3+36x^2-48x+64$ は $\mathbf Q$ 上既約 ⟹ 根の $\mathbf Q$ 上次数 6、$6\nmid[F:\mathbf Q]=4$ ⟹ **$f$ は $F$ 上既約**。

$$\boxed{\ \{P_1\}\ \sqcup\ \{P_2,P_3,P_4\}\qquad(\text{後者は }\mathrm{Gal}(\bar{\mathbf Q}/F)\ \text{の 1 軌道})\ }$$

配置 $(E,Q_0,Q_\infty,B_1,B_2)$ はすべて $F$-有理(★ $B_i$ の三角モデル $y$ 座標は $-2(1+i)/\zeta_{12}\in F$)⟹ Galois は 4 点集合に作用し、$P\mapsto W(P)$ は Galois 同変 ✔

### 3.2 ⚠ m-8 の受諾

v1 の「★ 独立の傍証: $P_1=\ominus Q_0$ は標識データだけで書ける唯一の点」は、**「$P_1$ が唯一の $F$-有理点」の言い換えに過ぎず、$\lambda_9$ がどれかについての証拠ではありません**(監査 m-8 のとおり)。★ 印を外し、**傍証としても使いません**。
⟹ 欠けていたのは「$\lambda_9$ 側にも $F$-有理性の理由がある」こと。**それを §4 が供給します。**

---

## §4 ★★★ 新規 — 母集団の全量(72 本)と resolvent 不変量 ⟹ $P=P_1$ を**前提なしに**確定

(生データ・script は `d2gap4_gate_adjudication_v1.md` §3。以下は要点と論理。)

### 4.1 $\lambda_9$ の全量(標的・$P$ 非依存)

`BuildPnFull(9)`+`H9fun` 構成(= cert `w9_k3_p1_0d_check_v1_20260812` と同一)から本ターンで抽出:

$$\boxed{\ \text{passport}=\bigl((18),\ (2^81^2),\ (18)\bigr),\quad g=4,\quad \lvert\mathrm{Mon}\rvert=324\ (\cong D_{18}\!\times\!D_{18}=\text{T18n140}),\quad\text{deck}=1\ }$$
次数 6 商: $qX=(1,2,3,4,5,6)$, $qY=(2,4)(3,5)$, $\lvert\mathrm{quot}\rvert=36$・ブロック $(3,2)$・deck 自明 = **Nielsen 類 #1**(`t3_spec` §1)✔

★ **塔の幾何がこの passport を予言し、測定が一致**($W\to E$ は $Q_0,Q_\infty$ で全分岐・$B_1,B_2$ で単純 ⟹ $t=0,\infty$ で 18-cycle、$t=1$ で $(2,2,2)(2,2,2)(2,1)(2,1)=2^81^2$、$\sum(e-1)=42$ ⟹ $g=4$)。
★★ **しかも配置は測定で強制されます**: $B_1,B_2$ が $t=1$ 上の $e_E=2$ 点だとすると $\sigma_1$ に 4-cycle が出て対合でなくなる ⟹ 矛盾 ⟹ **$B_1,B_2=e_E=1$ 点**(`w9_E_model_v1` §4 表と一致・以後推測なし)。

### 4.2 母集団 = **72 本**(2 系統独立に一致)

$\lambda_9$ はサイズ 3 ブロック系(§2.3 で一意)により $E$ を経由する ⟹ 母集団は「$E$ 上・分岐 $\{Q_0,Q_\infty,B_1,B_2\}$・局所類 $(3),(3),(2\,1),(2\,1)$ の次数 3 被覆」全体:

| 系統 | 方法 | 結果 |
|---|---|---|
| ① python | $\pi_1(E\setminus4)=\langle a,b,c_1..c_4\mid[a,b]c_1c_2c_3c_4\rangle\to S_3$ 全数 / 共役 | 432 組 ⟹ ★ **72 本** |
| ② GAP | 次数 6 データ上の誘導表現(gauge 固定 7 自由度)+ full passport filter | 432 割当 ⟹ ★ **72 本** |

$$\boxed{\ \textbf{【D2-GAP-6】(★大・新)}\ \text{代数走査(split Tschirnhaus 枝)が拾ったのは }\textbf{72 本中 4 本}\ \Longrightarrow\ \text{「}\lambda_9\in\{W(P_i)\}\text{」は未証明}\ }$$

⚠ これは falsifier B-1 の**幾何版**であり、より深刻です:B-1 は「passport 内に 13 本以上」(抽象群レベル)、本項は「**$E$ を経由する幾何的母集団の中で 4/72**」。v1 §1.4 は 4 本の非同型性を示しただけで、**4 本が候補の全部だとは示していませんでした**。

### 4.3 ⚠ 監査 M-1 への逆向きの修正 — 位数 324 は被覆を一意にしない

72 本の $\lvert\mathrm{Mon}\rvert$ 分布(GAP・本ターン):

$$324\times3,\qquad 972\times9,\qquad 2916\times6,\qquad 419904\times54$$

(★ 324/972/2916 は falsifier の悉皆掃引 `[140,324],[233,972],[245,972],[417,2916]` と整合。419904 は $>60000$ で監査の「未検査 247」側。)

$$\boxed{\ \lvert\mathrm{Mon}\rvert=324\ \textbf{をもつ被覆は 3 本ある}\ \Longrightarrow\ \text{「位数 324 と突合」だけでは }\lambda_9\ \textbf{を同定できない}\ }$$

3 本は $\mathrm{StructureDescription}=D_{18}\times D_{18}$・deck 1・中心 1・導来列 $[324,81,1]$・共役類数 36 が**すべて一致**し、**$S_{18}$ の部分群としても互いに共役**(= 同じ T18n140)。⟹ 監査 M-1 の「位数 324 + passport ⟹ T18n140 一意」は**群としては正しいが、被覆の一意性ではありません**。
⟹ ★ **ゲートの判定量は $\lvert\mathrm{Mon}\rvert$ ではなく三つ組の $S_{18}$-共役類**(§8)。

### 4.4 ★★★ resolvent 不変量 ⟹ $P=P_1$(恒真でない置換)

**構成**: 次数 3 被覆 $W\to E$ の二次分解体は $\varepsilon={\rm sgn}\circ\rho$。$Q_0,Q_\infty$ で $+1$(3-cycle)・$B_1,B_2$ で $-1$(transposition)⟹ $\varepsilon$ は $\pi_1(E\setminus\{B_1,B_2\})$ の指標に落ち、**$\{B_1,B_2\}$ で分岐する $E$ の 2 重被覆 4 本**を分類。

**代数側との対応(紙)**: split model で $\mathcal D=A_0^2\,(-4\alpha^3A_0-27\beta^2)$ ⟹ 平方類 $=[A_0-c]$、$\mathrm{div}(A_0-c)=B_1+B_2-2P$。$P\ne P'$ なら比の因子 $2P'-2P$ の半分 $P'-P$ は非主因子 ⟹ **4 点は 4 つの相異なる 2 重被覆を与える**。逆に 2 重被覆は $L^{\otimes2}=\mathcal O(B_1+B_2)$ の解 4 個 ⟹

$$\boxed{\ \{\text{4 resolvent 類}\}\ \longleftrightarrow\ \{P:[2]P=B_1\oplus B_2=Q_0\}=\{P_1,P_2,P_3,P_4\}\qquad(\textbf{Galois 同変})\ }$$

**測定**(GAP・`d2gap4_census2.g`・不変量 $=({\rm sgn}\,\beta_2,{\rm sgn}\,\beta_3)$):

| resolvent 類 | 本数 | $\lvert\mathrm{Mon}\rvert$ の分布 |
|---|---|---|
| a | 18 | $419904^{18}$ |
| b | 18 | $419904^{18}$ |
| c | 18 | $419904^{18}$ |
| ★ **d**($\lambda_9$ が属する) | 18 | ★ **$324^{3},\ 972^{9},\ 2916^{6}$** |

**論証**:
1. $\mathrm{Gal}(\bar{\mathbf Q}/F)$ は 72 本に作用(配置は $F$-有理・§3.1)。
2. Galois は **monodromy 群を保ち**(dessin の標準事実;関数体の Galois 閉包の群が共役で保たれることによる)、**resolvent を取る操作と可換** ⟹ 4 類の集合に作用し各類の $\lvert\mathrm{Mon}\rvert$ 多重集合を保つ。
3. 類 d は多重集合が他 3 類と異なる**唯一の類** ⟹ ★ **類 d は Galois 安定**。
4. ⟹ 対応する $P$ は Galois 固定 ⟹ §3.1 の軌道構造 $\{P_1\}\sqcup\{P_2,P_3,P_4\}$ より

$$\boxed{\ \textbf{【CAN-1}'\textbf{】}\quad \lambda_9\ \text{の二次分解体は }P_1=(0,-2)=\ominus Q_0\ \text{の類}\ }$$
$$\text{⟹ }\lambda_9\ \text{の任意の Tschirnhaus モデルの判別式は }A_0^{(P_1)}-c\ \text{の平方類に属する}$$

★ **これは恒真ではありません**(B-2 への回答): 前提は「Galois が monodromy 群と resolvent を保つ」という一般論だけで、結論は $P$ の名指し。$\lambda_9$ の moduli 体も 4 点族への所属も仮定していません。
★ **m-8 で欠けていた「$\lambda_9$ 側の $F$-有理性の理由」= 類 d の組合せ的一意性**が、これです。

### 4.5 ⚠ 組合せだけでは閉じない残り(正直な申告)

$\lvert\mathrm{Mon}\rvert=324$ の 3 本は上記の標準不変量すべてで**区別できません** ⟹ 3 本の Galois 軌道構造(1+1+1 か 3 か)は**未決**【D2-GAP-7】⟹ **$\lambda_9$ の moduli 体の次数は $\le3$ とまでしか言えません**。UNKNOWN は UNKNOWN と書きます。

---

## §5 CAN-1 の撤回と後継

### 5.1 撤回(B-1・B-2 の受諾)

v1【CAN-1】の前提「類の中で一意」は**偽**、括弧書き「(同値: 定義体の moduli 体 $\subseteq F$)」は**二重に誤り**(語が壊れている + 同値でない)。正しく述べ直した版
$$\lambda_9\ \text{の moduli 体}\subseteq F\iff\lambda_9=W(P_1)$$
は「$\lambda_9\in\{W(P_i)\}$」を前提としたうえでの**恒真**⟹ 還元になっていません。
$$\boxed{\ \textbf{v1 §0-3 の「正準化は「規約」ではなく「強制」です」は }\textbf{overclaim — 撤回}\ }$$
⚠ ただし CAN-1 の**証明の中身**($\sigma(W(P))=W(\sigma P)$ の同変性・deck 自明性による降下・$\sigma P=P$)は監査でも壊れず、§4.4 でも同じ同変性を使っています。**壊れていたのは前提の立て方だけ**です。

### 5.2 後継 2 本

| 札 | 内容 | 状態 |
|---|---|---|
| **【CAN-1′】** | $\lambda_9$ の二次分解体 $=P_1$ の類 | ★ **成立**(§4.4・前提なし・機械 + 紙) |
| **【CAN-2】** | $\lambda_9$ の Tschirnhaus 束は split($\cong\mathcal O(P_1)\oplus\mathcal O(2P_1)$)か | ⚠ **未決**(= $\lambda_9=W(P_1)$)⟹ §8 の 1 走行 |

---

## §6 【問 2】V6 の紙路(m-2・m-3 修理版)

### 6.1 上界(モデル非依存)

$\mathrm{div}_E(y)=3Q_0-3Q_\infty$、$\pi$ は $Q_0,Q_\infty$ で全分岐 ⟹ $\mathrm{div}_W(\pi^*y)=9P_0-9P_\infty$ ⟹ $\mathrm{ord}(P_0-P_\infty)\mid9$。★ 全分岐だけを使う ⟹ 72 本すべてが自動継承。

### 6.2 ★【補題 ORD9】(m-2 修理版 — 仮定を証明に合わせた)

> $\pi:W\to E$ を標数 0・代数閉体上の次数 3 被覆、$Q_0,Q_\infty$ で**全分岐**、$\mathrm{ord}(Q_0-Q_\infty)=3$、$K(W)/K(E)$ が**非 Galois**とする。このとき $\mathrm{ord}(P_0-P_\infty)=9$。

*証明*: §6.1 より位数は $1,3,9$。
- ★ **$=1$ の排除(修理)**: 全分岐 2 箇所だけで $\deg R\ge2+2=4$ ⟹ $2g(W)-2=3(2\cdot1-2)+\deg R\ge4$ ⟹ **$g(W)\ge3>0$**(genus を仮定に入れずに出る)。$\mathrm{ord}=1$ なら $P_0\sim P_\infty$ ⟹ $g(W)=0$ ⟹ 矛盾。
- $=3$: $\mathrm{div}(h)=3P_0-3P_\infty$ なる $h$ ⟹ $h^3$ と $\pi^*y$ が同因子 ⟹ $h^3=\pi^*y$(定数吸収)。$[K(E)(h):K(E)]\mid3$。$=1$ なら $y$ が $K(E)$ の立方 ⟹ $\mathrm{ord}(Q_0-Q_\infty)=1$ で仮定に矛盾。$=3$ なら $K(W)=K(E)(y^{1/3})$ で $\zeta_3$ が定数体にある ⟹ 巡回 Kummer ⟹ Galois、矛盾。∎

### 6.3 非 Galois 性(m-3 修理 — 既約性を明示)

$\mathcal D=\rho^2A_0^2(-4\rho A_0-27)$、第 2 因子の因子は $B_1+B_2-2P$。$B_1\ne B_2$ ⟹ $B_1$ での重複度 1(奇)⟹ **判別式は平方でない**。
★ **既約性**(m-3): $Q_0$ での Newton 多角形は $(0,1)\to(3,0)$ の 1 辺 ⟹ $e=3$ ⟹ 局所 monodromy が 3-巡回 ⟹ 推移的 ⟹ **3 次式は既約**。⟹ 既約 + 判別式非平方 ⟹ $S_3$ ✔
★ **群論側の独立確認**(falsifier §5.2): T18n140 のサイズ 3 ブロックの stabilizer $M$(位数 54)のブロック上の像 $=S_3$・deck $=1$ ✔
★ **census 側の独立確認**(本ターン): 72 本すべてが $\langle\cdot\rangle=S_3$ で可移 ✔

$$\boxed{\ \textbf{(V6) は紙で閉じ、72 本すべてで自動成立 — 判別力 0 ビット}\ }$$

---

## §7 【問 3】厳密モデル($W(P_1)$ 名乗り)と定義体

### 7.1 規約と厳密量(m-5 準拠: $z^3+Az+B$、$\mathcal D=-4A^3-27B^2$)

| 量 | 厳密値 | 検算 |
|---|---|---|
| $P_1$ | $(0,-2)=\ominus Q_0$ | 曲線上 ✔ |
| $A_0=X(R\ominus P_1)-X_{P_1}$ | $-\dfrac{2y}{x^2}$ | 曲線関係で余り 0 ✔(falsifier 独立再現 ✔) |
| $c=A_0(B_1)=A_0(B_2)$ | $\dfrac{\zeta_6}{2}=\dfrac14+\dfrac{\sqrt3}{4}i$ | 厳密差 0 ✔ / cert 30 桁一致 ✔ |
| $\rho=\alpha^3/\beta^2=-27/(4c)$ | $-\dfrac{27}{2\zeta_6}=-\dfrac{27}4+\dfrac{27\sqrt3}4i$ | cert `alpha3_over_beta2_ratio`(P1)一致 ✔ |
| $\rho A_0$ | $-27\zeta_3\,\dfrac{y}{x^2}$ | ✔ |

$$\boxed{\ W(P_1):\quad x^2w^3-27\zeta_3\,y\,(w+1)=0\quad\text{over}\quad E:\ y^2+3\zeta_3xy+2y=x^3\ }$$
$$\boxed{\ W(P_1)=W_9\iff \textbf{【CAN-2】}\ (\text{未決 — §8})\ }\qquad(\text{M-4 準拠: 無条件では名乗らない})$$

### 7.2 ★★ $E\to\mathbf P^1_t$ の明示式(監査 M-5 への回答・実装係の問 3 への回答)

**所在**: `t3_spec_and_C2_calib_v1.md` §8 は**別車線**($\mathbf P^1_t$ 上の直接 ansatz)の未完部分で、本ゲートの臨界路ではありません。必要な式は `w9_E_model_v1.md` §1 にあります: $\mathrm{div}(s)=3Q_0-3Q_\infty$ なる次数 3 の $s$ と **$t=c\,s^2$**。

**Weierstrass 座標への翻訳**(私・本ターン・独立検算 2 本):
$E:y^2+3\zeta_3xy+2y=x^3$ を $x$ の 3 次式と読むと $x^3-3\zeta_3y\,x-(y^2+2y)=0$ ⟹ $E\to\mathbf P^1_y$ が次数 3 で、$\mathrm{div}(y)=3Q_0-3Q_\infty$ ⟹ **$y$ が $s$ の役**。

- **検算 1(判別式)**: $\Delta_x=-4(-3\zeta_3y)^3-27(y^2+2y)^2=-27y^2(y^2+4)$ ⟹ 分岐は $y=0,\infty,\pm2i$ ⟹ $s=\pm1$ に合わせて $s=y/(2i)$。
- **検算 2(ゲージ不変量・独立)**: `w9_E_model_v1` §3 の不変量は $\beta/\gamma=i$ と $\alpha^3/\beta^2=27i/2$。$s=\lambda y$ とすると $\beta'/\gamma'=1/(2\lambda)=i\Rightarrow\lambda=1/(2i)$、このとき $\alpha'^3/\beta'^2=-27\lambda=27i/2$ ✔ ⟹ ★ **未知数 1 に対し独立な等式 2 本が同じ $\lambda$ で一致**(2 文書の $E$ が同一の三角化つき曲線であることの初の突合)。

$$\boxed{\ s=\frac{y}{2i},\qquad \boxed{\,t=s^2=-\frac{y^2}{4}\,}\qquad \mathrm{div}(t)=6Q_0-6Q_\infty\ }$$

★ **$i$ は 2 乗で消えます** ⟹ **$t$ は $\mathbf Q$-有理な関数**、$E$ と $W(P_1)$ の係数は $\mathbf Q(\zeta_3)$ ⟹

$$\boxed{\ \textbf{合成 }\lambda:W(P_1)\to\mathbf P^1_t\ \textbf{全体が }\mathbf Q(\zeta_3)\ \textbf{上に定義される}\ }\qquad(\text{★ M-5 は肯定的に解決})$$

⚠ **ただし $\lambda_9$ の定義体への外挿は【CAN-2】条件つき**。中間座標 $s$ 単独は $i$ を要する(が $\lambda$ には現れない)。$F_9=\mathbf Q(\zeta_{36})$ は corpus 側の作業体であって $\lambda$ の定義体の上界ではありません。

### 7.3 18 枚の葉の明示(実装直結)

$$t\ \xrightarrow{\ y^2=-4t\ (2\ \text{枚})\ }\ y\ \xrightarrow{\ x^3-3\zeta_3yx-(y^2+2y)=0\ (3\ \text{枚})\ }\ (x,y)\ \xrightarrow{\ x^2w^3-27\zeta_3y(w+1)=0\ (3\ \text{枚})\ }\ (x,y,w)$$
$2\cdot3\cdot3=18$ ✔ 分岐は $t=0$($y=0$)・$t=1$($y=\pm2i$)・$t=\infty$ のみ ✔(各層の判別式が他で消えないことは上表で確認)
⟹ **層ごとの path-tracking で合成 monodromy が組める**(新規の数学設計は不要)。

---

## §8 ★【D2-GAP-4 改】ゲート — 事前登録(prereg)

### 8.1 標的(既に認証済み・再測定しない)

| cert | 引用値 |
|---|---|
| `search/certs/w9_k3_p1_0d_check_v1_20260812.json` | `monG_size: 324`, `D: 18`, `quotG_order: 36`, `centralizer_order: 1` |
| `search/certs/r13_p1_0_blocks_v1_20260812.json` | `D: 18`, `mon_group_size: 324`, `block_sizes: [9,3]`, `is_primitive: false` |
| 本ターン(`scratchpad/lambda9_passport.g`) | 三つ組の**明示**: $\sigma_0=(1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18)$, $\sigma_1=(2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14)$ |

⚠ **判定量は $\lvert\mathrm{Mon}\rvert$ ではなく三つ組の $S_{18}$-共役類**(§4.3: 324 の被覆は 3 本ある)。
★ **共役判定の実装**: $\sigma_0$ は 18-cycle ⟹ $\sigma_0$ を $(1,2,\dots,18)$ に正規化して $\sigma_1$ を比較し、$\langle\sigma_0\rangle$(18 個)の共役を尽くせばよい。

### 8.2 測定(実装係 A へ・**これが実装係の (B) 読み**)

```
=== [D2-GATE] W(P_1) が lambda_9 か(prereg・裁定1086 M-3 準拠)===
根拠: docs/notes/p1d2_r1_canonicalization_v2.md §7・§8
⚠ 算術入力ゼロ(純幾何)・u/c 非接触・封印非接触・規約 = z^3+Az+B

[G-0] 起動時テスト(fail-closed・★ 答えは走らせる前に確定している)
   (a) 次数 6 層 E->P^1_t 単独の monodromy が (qX,qY)=((1,2,3,4,5,6),(2,4)(3,5))・|quot|=36・
       ブロック(3,2)・deck 1 に S_6-共役  ⟹ 外れたら t の正規化が誤り ⟹ 即停止
   (b) 得た次数18三つ組の passport が ((18),(2^8 1^2),(18))・g=4  ⟹ 外れたら式が誤り ⟹ 即停止
   (c) 判別式の平方類が A_0^{(P_1)}-c と一致(CAN-1' の回帰)

[G-1] 明示データ(厳密・Q(ζ_3) 係数・本書 §7)
   E : y^2 + 3ζ_3 x y + 2y = x^3     Q_0=(0,0), Q_∞=O, P_1=(0,-2)
   W : x^2 w^3 - 27 ζ_3 y (w+1) = 0
   t = -y^2/4                        (層: t -> y (2枚) -> x (3枚) -> w (3枚) = 18)
[G-2] 本測定: 合成 W(P_1)->P^1_t の monodromy 三つ組(数値 path-tracking・mpmath 50桁)
      ★ 対照 1 本: 同じコードで W(P_2)(cert p1_d2_scan_v2 の P_2 座標・c, ρ を使用)
[G-3] 出力 = (|Mon(W(P_1))|, S18-共役か) と (|Mon(W(P_2))|)
出力: cert (schema d2_gate/v1)。u_touched=false ; c_touched=false ; 生値のみ(判定は司令塔)
★ 規模: 18 根 × 3 loop の追跡 = 分級。
```

### 8.3 ★ 事前登録した予言と 5 分岐の行き先(発火前に固定)

**予言(§4.4 の帰結・外れたら私の resolvent 同定が誤り)**:
- **PRED-1**: $\lvert\mathrm{Mon}(W(P_1))\rvert\in\{324,\ 972,\ 2916\}$ — 特に $\ne419904$。
- **PRED-2**: $\lvert\mathrm{Mon}(W(P_2))\rvert=419904$(類 a/b/c は 18 本すべて 419904)。

| # | 出力 | 意味 | ★ 行き先(事前記載) |
|---|---|---|---|
| **(a)** | $W(P_1)$ の三つ組が $\lambda_9$ と $S_{18}$-共役 | ★★ **$W_9=W(P_1)$ 確定** | **CAN-1/CAN-2 とも不要**・§7.1 のモデルを無条件で宣言・定義体 $\subseteq\mathbf Q(\zeta_3)$ も無条件 |
| **(b)** | $\lvert\mathrm{Mon}\rvert=324$ だが非共役 | $\lambda_9$ は類 d の別の 324 本 | ★ **§7.1 のモデルを棄却**・`t3_spec` §4 の $m$ 走査($\mathcal E$ 一般形)へ差し戻し・【CAN-1′】は生存 |
| **(c)** | $\lvert\mathrm{Mon}\rvert\in\{972,2916\}$ | $\lambda_9$ は split でない | ★ 同上(棄却 + $m$ 走査)。【D2-GAP-6】が本命であったと確定 |
| **(d)** | $\lvert\mathrm{Mon}(W(P_1))\rvert=419904$ | ★ **PRED-1 違反** | ⚠ **即停止** — §4.4 の resolvent 同定または $t$ 正規化が誤り。census を再現検査 |
| **(e)** | $\lvert\mathrm{Mon}(W(P_2))\rvert\ne419904$ | ★ **PRED-2 違反** | ⚠ **即停止**(同上) |

★ falsifier M-3 の 4 分岐との対応: 監査の (c)「両方 324」・(b)「$P_1\ne324,P_2=324$」は **§4.4 により事前に排除**され、出れば停止分岐 (d)/(e) になります。⟹ **確認枠(confirmation framing)ではなく、両側かつ予言つきの検定**になりました。

### 8.4 ⚠ 便 122 への載せ方

- **無条件で書けるもの**: passport・$\lvert\mathrm{Mon}(\lambda_9)\rvert=324$・ブロック系一意(D2-GAP-5 閉)・母集団 72 本・**【CAN-1′】($\lambda_9$ の resolvent $=P_1$)**・$t=-y^2/4$・2 つの $E$ モデルの一致。
- **書いてはいけないもの**: 「$W_9$ の正準モデル」「定義体 $\subseteq\mathbf Q(\zeta_3)$」を**無条件で**。「4/4 PASS ゆえ確定」「一意性ゆえ強制」も禁止。
- ★ **推奨**: [D2-GATE] は**分級**なので**先に走らせる**。1 走行で (a) なら無条件宣言、(b)(c) なら棄却 — どちらでも便 122 の内容が確定します。

---

## §9 GAP・記帳

- **【D2-GAP-4】★ 改称・実質前進**: 「どの $P$ か」は §4.4 で**測定により確定**($P=P_1$・前提なし)。残余は【CAN-2】=【D2-GAP-6】へ。
- **【D2-GAP-5】★ 閉鎖**(§2.3・紙 1 行 + 機械三重一致)。監査 M-2 の留保も解消。
- **【D2-GAP-6】(★大・新)=【CAN-2】**: $\lambda_9$ の Tschirnhaus 束は split か(= 4 点族に属するか)。§8 の 1 走行。
- **【D2-GAP-7】(中・新)**: $\lvert\mathrm{Mon}\rvert=324$ の 3 本の Galois 軌道構造 ⟹ $\lambda_9$ の moduli 体の次数は $\le3$ までしか言えない(§4.5)。
- **【D2-GAP-1/2/3】** 既設(GAP-2 は閉鎖)。
- ★ **本書の新規部分**(v1 からの増分): ① $\lambda_9$ の完全 passport 抽出と塔幾何による遡及検証・**配置の強制**(§4.1)② D2-GAP-5 の紙 1 行閉鎖(18-cycle 論法・任意の被覆で成立)③ **母集団 72 本**(2 系統)④ **【D2-GAP-6】の摘出**(4/72)⑤ **$\lvert\mathrm{Mon}\rvert=324$ の被覆は 3 本**(監査 M-1 への逆向き修正)⑥ **resolvent 類 $\leftrightarrow$ 4 点 $P$** の Galois 同変対応 ⑦ ★★ **【CAN-1′】: $P=P_1$ の無条件確定** ⑧ 2 つの $E$ モデルの同定・**$t=-y^2/4$**・合成の $\mathbf Q(\zeta_3)$-有理性(M-5 の肯定的解決)⑨ 18 葉の層分解(実装直結)⑩ 予言つき 5 分岐 prereg。
- ⚠ **自己捕獲(暫定札・案 B により自番号は立てず Sol 採番待ち)**:
  - **m1083-1**: v1 §4.1 の指示文「[P1-0d] の次数 18 版を $P_1$/$P_2$ で」は**標的と測定を取り違えた型エラー**。`BuildPnFull` が作るのは測定器ではなく**標的**($P$ 非依存)。実装係が着手前に停止したのは正しく、**停止がなければ 0 ビット cert を作っていました**。⟹ 教訓: **「既存 script の $n$ を差し替える」型の指示は、その script が測定器か標的かを明記する**。
  - **m1083-2**: v1 §1.5 の「(同値: 定義体の moduli 体 $\subseteq F$)」は語も論理も誤り。CAN-1 の前提は偽で、直すと恒真(監査 B-1/B-2)。
  - **m1083-3**: v1 は**母集団の大きさを検めずに**「4 点が候補」と扱っていた(4/72)。⟹ 教訓: **候補を数え上げる前に、母集団の位数を独立に測る**(Hurwitz/Nielsen 数は安い)。
- **申告**: GAP 4.16.0(`scratchpad/lambda9_passport.g`, `d2gap4_census.g`, `d2gap4_census2.g`, `d2gap4_census3.g`)+ python(`scratchpad/deg3_census_over_E.py`)。$u$/$c$ 非接触・prereg 非抵触・**Sol 未監査**・**verified ではない**(candidate 格)。
