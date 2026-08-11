# P4-0 DEF/LATTICE-COMPARE — 骨子(裁定 834②)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(**設計と方針**・結論を出す文書ではない)
**入力**: Sol 便 114 返書 P1/P4-0(`sol/sol_reply_114_phase2_hunt_audit.md`)/ 裁定 830・834
**位置**: 実験列**優先度 0**。これを通るまで ④/e sweep は**診断器**であって反例検出器ではない。

---

## §0 三つの下位課題と、本骨子の結論の型

| # | Sol の要求 | 本骨子の見立て |
|---|---|---|
| **1** | $L_{\rm gen}/L_{\rm sat}$ を分離し**どの SNF がどの商を測るか** exact sequence を書く | ★ **書ける**(§1)。しかも**測定値は救われる見込み**(§1.4)— ただし CV-9 判読が前件 |
| **2** | Brown の non-trivial isomorphism が **unimodular か**を証明するか「選択格子依存」と凍結 | ★ **凍結を推奨**(§2)。加えて**依存の正体の同定候補**を出す(検定可能) |
| **3** | $E(k,p)\Rightarrow$ 反例 の**比較射を定理として提示**。無ければ proxy と明記 | ★ **建設不可能寄り**(§3)。しかも**旧「箱入り同値」は循環していた**ことが分かる |

---

## §1 課題 1 — 三格子と exact sequence

### 1.1 対象の固定

$$A:=L_{\rm gen}^{\mathbf Z}=\mathbf Z\langle\text{Ihara 括弧語}\rangle\ \subseteq\ B:=L_{\rm sat}^{\mathbf Z}=(\mathbf Q A)\cap C\ \subseteq\ C:=\mathrm{ls}_k^{\mathbf Z}$$
いずれも有限生成自由 $\mathbf Z$-加群、$A\otimes\mathbf Q=B\otimes\mathbf Q$。

### 1.2 ★ 命題候補 **LAT-TOR**(candidate・本骨子)

> $$0\to B/A\to C/A\to C/B\to0,\qquad B/A\ \textbf{有限}\ ,\quad C/B\ \textbf{torsion-free}$$
> $$\boxed{\ \mathrm{Tor}\bigl(\mathrm{coker}(A\hookrightarrow C)\bigr)\ =\ B/A\ =\ L_{\rm sat}^{\mathbf Z}/L_{\rm gen}^{\mathbf Z}\quad(\textbf{標準同型})\ }$$
> **証明**: $x\in C$ が $C/A$ で捩れ ⟺ $\exists n\ge1: nx\in A$ ⟹ $x\in\mathbf QA=\mathbf QB$ かつ $x\in C$ ⟹ $x\in B$。逆も明らか。∎

⟹ **「捩れを測る」という言い方は、$A=L_{\rm gen}$ を左項に置く限り正しい。** 私の誤りは、**飽和である $B$ の記号に $L$ を使いながら $A$ の捩れを測っていた**こと(記号の取り違え)。

### 1.3 ★ どの SNF が何を測るか(**課題 1 の中心成果物**)

$M$ を「$C$ の基底で書いた $A$ の生成元行列」とし、SNF の単因子を $s_1\mid\cdots\mid s_r$($r=\mathrm{rank}\,A$)とする。

| 計算 | 測るもの | 値 |
|---|---|---|
| $\mathrm{SNF}(M)$ の単因子 | ★ $B/A=\bigoplus\mathbf Z/s_i$ | **非自明になりうる**(5, 691 等) |
| $\mathrm{coker}(A\hookrightarrow C)$ | $\bigoplus\mathbf Z/s_i\ \oplus\ \mathbf Z^{\dim C-r}$ | 捩れ部が $B/A$ |
| $\mathrm{SNF}$ of $B\hookrightarrow C$ | 全単因子 $=1$ | ★ **常にゼロ情報**(飽和ゆえ) |
| $\ker(\beta_k^{\mathbf Z})=\mathsf P_k^{\mathbf Z}$ | **核は自動的に飽和** ⟹ 自身の捩れは 0 | 𝖯 側の情報は「**別の自然格子との指数**」としてのみ現れる(§2) |

### 1.4 ★★ 深さ 2 での CONE-B の**条件つき復活**

$$L_{\rm gen,2}^{\mathbf Z}=\beta_k\bigl(\Lambda^2D_1^{\mathbf Z}\bigr)\quad(\text{括弧語の }\mathbf Z\text{-張り} = \beta\ \text{の像})$$
$$\boxed{\ \mathrm{Tor}\,\mathrm{coker}(\beta_k^{\mathbf Z})\ =\ L_{\rm sat,2}^{\mathbf Z}/L_{\rm gen,2}^{\mathbf Z}\quad\textbf{(前件: 始域}=\Lambda^2D_1^{\mathbf Z},\ \textbf{終域}=\mathrm{ls}_2^{\mathbf Z}\textbf{)}\ }$$
⟹ **CONE-B(「$\mathrm{coker}(L\hookrightarrow\mathrm{ls})$ と $\mathrm{coker}\beta_k$ が同じ捩れ」)は誤りではなく、格子の前件を書き落としていた。**

> ### ★★★ 測定値は救われる見込み(**論理からの示唆・CV-9 判読が前件**)
> 飽和格子の包含は**必ず** torsion-free な余核を与える。cert は**非自明な捩れ(5・691)を出力した**。
> $$\boxed{\ \Longrightarrow\ \textbf{機械が消費した行列は }L_{\rm sat}\ \textbf{ではありえず、}L_{\rm gen}\ \textbf{(生成元行列)である}\ }$$
> ⟹ **B114-1 は「文章の誤り」であって「測定の誤り」ではない可能性が高い。**
> ⚠ **ただしこれは出力からの逆推論**であり、**実装が実際に何を消費したかの判読(CV-9 型)が必須**。⟹ **発注 LAT-CV9**(§4)。

---

## §2 課題 2 — unimodularity:**凍結を推奨し、依存の正体を同定候補として出す**

### 2.1 なぜ証明できないか

Sol の頁照合どおり、Brown p.25 は $e$ を "defined over $\mathbf Z$" とし、周期多項式空間との "non-trivial isomorphism" を経由して differential と比較するが、**その同型が選択格子上 unimodular とは書いていない**。両側の整構造は**別の出自**をもつ:

| 側 | 整構造の出自 |
|---|---|
| $\mathsf P_k^{\mathbf Z}$(周期多項式側) | modular symbols / $H^1$ の $\mathbf Z$-係数(Eichler–Shimura) |
| $\ker\beta_k^{\mathbf Z}$(Lie 側) | $\mathrm{ls}^{\mathbf Z}$ の選択 + $\sigma_{2i+1}$ の正規化 |

**同じ $\mathbf Q$-空間の中の二格子**であり、その比較は**指数**である。⟹ unimodularity は「証明する」よりも「**指数を同定する**」問題。

### 2.2 ★ 同定候補(candidate・検定可能)

> ### 予想候補 **EIS-INDEX**(candidate・本骨子・repo 初出)
> $$\boxed{\ [\mathsf P_k^{\rm arith}:\ \ker\beta_k^{\mathbf Z}]\ \ \textbf{(または逆向き)は、重み }k\ \textbf{の}\textbf{Eisenstein 合同数}\textbf{と一致する}\ }$$
> **動機**: 古典的に、尖点部分格子と全格子の指数は $\mathrm{num}(B_k/2k)$ 型の量で測られ、$k=12$ ではそれが **691** である。工房が測った $\mathbf Z/691$ は**この既知量の再現**である可能性が高い。
> **★ 効用 2 つ**:
> 1. **retrodiction 検定になる**: 既収の「こだま retrodiction 合格」と整合するか、重み $k=16,18,20,\dots$ で $\mathrm{num}$ と突合せよ(**紙+既存表で可能・安い**)。
> 2. ★ **新規性の防波堤**: もし一致するなら、測定値は**既知の合同数の再現**であって新発見ではない ⟹ 「捩れを発見」型の主張を**事前に封じる**(規約: novelty grep の数論版)。
> **外れたら**: 指数が既知量と一致しない ⟹ **格子選択のアーティファクト**である可能性が上がる(LAT チャート)。どちらでも情報。

### 2.3 凍結文案

> **凍結(推奨)**: 「$\mathsf P^{\mathbf Z}$・$\mathrm{ls}^{\mathbf Z}$・商格子は**選択**であり、Brown は正準格子を供給しない。ゆえに ④ の整数不変量はすべて **選択格子依存**と明記する。依存の正体の同定候補は EIS-INDEX(§2.2)であり、検定は重みごとの $\mathrm{num}$ 突合。」
> 【文献要請 **BROWN-LIT-1**】: Brown p.25 の non-trivial isomorphism の**明示形と、両側の整構造の比較**を述べた箇所(原論文または後続)。無ければ「供給されていない」ことの確認で足りる。

---

## §3 課題 3 — 比較射 $E\Rightarrow CE$:**建設不可能寄り。しかも旧「箱入り同値」は循環していた**

### 3.1 必要な鎖と、切れている環

$$E(k,p)\ne0\ \xrightarrow{\ (a)\ }\ \text{motivic/pro-unipotent の格子欠損}\ \xrightarrow{\ (b)\ }\ \text{profinite }\widehat{GT}\ \text{の言明}\ \xrightarrow{\ (c)\ }\ GT(N)\ne\mathrm{im}(\mathrm{Ih}_N)$$

- **(b) が最大の断絶**: Brown の $\mathrm{ls}$ は**深さ次数付き motivic(pro-unipotent)**側の対象で、$GT(N)$ は**profinite**側の有限商。両者は**別の completion** に住む。橋は「motivic ⟹ ℓ 進実現 ⟹ pro-ℓ GT ⟹ 有限窓」で、**各段で整構造(格子)の選択が新たに入る**。
- **(c)**: 有限窓での非全射が深さ 4 に必ず現れる理由はない(逆向きも同様)。

### 3.2 ★★★ 構造的障害(本骨子の主要成果)

$E(k,p)\ne0$ の意味を mod $p$ で読むと:
$$L_{\rm gen}\otimes\mathbf F_p\ \subsetneq\ \mathrm{ls}_k^{\mathbf Z}\otimes\mathbf F_p$$
「$\sigma$ たちの括弧の $\mathbf Z$-張り」が全体を張らない、という言明である。これを反例に変換するには
$$\textbf{(必要)}\qquad(\text{算術像})_{\rm graded}\ \subseteq\ L_{\rm gen}\otimes\mathbf F_p$$
が要る。しかし**成り立つのは逆向きだけ**である:
$$\boxed{\ L_{\rm gen}\otimes\mathbf F_p\ \subseteq\ (\text{算術像})_{\rm graded}\quad(\sigma\ \textbf{の括弧は確かに算術的})\ }$$
$$\boxed{\ \textbf{逆向き}\ (\text{算術像})\subseteq L_{\rm gen}\ \textbf{は「算術像が }\sigma\ \textbf{たちで生成される」= 井原予想の一形}\ }$$

> ### ★★★ 帰結 — **旧「箱入り同値」は循環していた**
> 「井原予想の $p$ 進の運命 $\iff$ $e$ の $\mathbf Z$ 上飽和」の**順方向は、まさに「算術像 $=\langle\sigma\rangle$」を仮定して初めて出る**。それは結論の一形である。
> $$\boxed{\ \Longrightarrow\ \textbf{同値に見えたのは、結論を前提に置いていたからである。}}$$
> ⟹ **撤回(v1.2 §1.1)は正しく、かつ理由は「比較定理が無い」より強い —「順方向は循環」である。**

### 3.3 ★ ゆえに $E$ は何か

$$\boxed{\ E(k,p)\ne0\ \textbf{は、算術像の複体の}\textbf{下界}\textbf{が全体に届かないことを示す — 上界の言明ではない ⟹ }\mathbf{alarm}\ \textbf{であって witness ではない}}$$
「$E$ を proxy と明記せよ」という Sol 裁定に**機構つきで**同意する。

### 3.4 建設可能性の見積り(結論不要とのことだが、方針として)

| 部品 | 状態 | 見積り |
|---|---|---|
| (a) $E$ ⟹ motivic 側格子欠損 | ほぼ定義 | 容易 |
| (b) motivic ⟹ pro-ℓ GT の Lie 環(ℤ_ℓ 構造つき) | **文献に部分的にありうる**(Ihara の ℓ 進 Galois 表現 / Deligne–Goncharov)⟹ 【文献要請 **CMP-LIT-1**】 | 中(他人の道具に乗れる可能性) |
| (c) pro-ℓ ⟹ 有限窓での非全射 | **深さの局所性がない** | ★ **困難** |
| ★ 順方向に必要な「算術像 $=\langle\sigma\rangle$」 | ★ **予想そのもの** | ★ **循環 — 建設不可** |
> $$\boxed{\ \textbf{方針}: (a)(b)(c)\ \textbf{を積んでも順方向は §3.2 の循環で止まる。ゆえに }E\Rightarrow CE\ \textbf{の建設は}\textbf{推奨しない}\textbf{。}}$$
> $$\boxed{\ \textbf{代わりに逆向き }CE\Rightarrow E\ \textbf{(反例が見つかったとき }E\ \textbf{に痕跡が出るか)を「事後検証器」として設計するのが健全。}}$$
> ⟹ ★ **④ の正しい役回りは「反例検出器」ではなく「反例が出たときに深さ側で確認する検証器」**。これは実験列順位 1(CRT-ENTANGLE)と**補完的**で競合しない。

---

## §4 発注案(便 115 で監査を請う 2 件)

> ### **LAT-CV9**(判読・falsifier へ)
> ④ 系の cert(`torsweep_*`・`cbrecon_*`)が SNF に**実際に消費した行列**が、$L_{\rm gen}$(生成元行列)か $L_{\rm sat}$(飽和後)かを**非当事者として判読**せよ。§1.4 の逆推論(非自明な捩れが出た以上 $L_{\rm gen}$ のはず)が**実装と一致するか**。
> **判定**: 一致 ⟹ **B114-1 は文章の誤りに限局**(測定値は scope つきで救われる)。不一致 ⟹ **測定のやり直し**。

> ### **EIS-CHK**(紙+既存表・安い)
> §2.2 の EIS-INDEX を重み $k=12,16,18,20,22,26$ で検定: 測定された指数(単因子の積)と、当該重みの **Eisenstein 合同数**($\mathrm{num}(B_k/2k)$ 型)を突合。
> **IF-FIRST 凍結**: $k=12$ で **691** が再現する(既知の一致)。$k=16,18,20$ では対応する分子(3617, 43867, 283·617)が現れるか — **現れれば選択格子は「自然」であり、現れなければ格子アーティファクト**。
> **DOMAIN-PIN**: 述語 = 単因子の積 vs 数論的分子の一致 / 定義域 = 既測の $k$ / 帰属根拠 = ④ の cert / chi_semantics = 該当なし / factor_filter = 深さ 2 のみ / 落とした因子 = 深さ $\ge3$ / 比較射 = **EIS-INDEX(未証明・本検定の対象)** / 陽性 = 格子の自然性の証拠+**新規性の否定**(既知量の再現)/ 陰性 = LAT チャートの実在。

---

## §5 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| **【P40-GAP-1】** | §1.4 の「測定値は救われる」は**出力からの逆推論** ⟹ LAT-CV9 が前件 | ★ 中 |
| **【P40-GAP-2】** | EIS-INDEX は**同定候補**であって証明されていない | ★ 中 |
| **【P40-GAP-3】** | §3.2 の「算術像 $\subseteq L_{\rm gen}$ は予想の一形」は**私の読み** — Sol/falsifier の反論を請う | ★ 中 |
| **【BROWN-LIT-1 / CMP-LIT-1】** | 文献要請 2 件(§2.3・§3.4) | 中 |

**帰属**: P1 の摘発・$L_{\rm gen}/L_{\rm sat}$ の分離・P4-0 の三課題 = **Sol**(便 114 返書)。委嘱 = 司令塔(裁定 834②)。
本骨子の新規部分 = **命題候補 LAT-TOR(標準同型 $\mathrm{Tor}\,\mathrm{coker}(A\hookrightarrow C)=B/A$)** / **§1.3 の「どの SNF が何を測るか」表** / **§1.4 の CONE-B 条件つき復活と「測定値は救われる」逆推論** / **予想候補 EIS-INDEX(依存の正体の同定候補+新規性の防波堤)** / ★ **§3.2 の循環の指摘(旧箱入り同値の順方向は「算術像 $=\langle\sigma\rangle$」= 予想の一形を仮定していた)** / **④ の役回りの転換(検出器 → 事後検証器)** / **発注 LAT-CV9・EIS-CHK**。

**novelty grep**(`docs/` `provenance/`): `LAT-TOR` `EIS-INDEX` `EIS-CHK` `LAT-CV9` `Eisenstein congruence` `アイゼンシュタイン合同` = **0 hit(本骨子初出)**。`L_gen` / `L_sat` は `docs/状態.md`(司令塔の記録)のみ既在。

**検算**(EIS-CHK の突合対象・**予言値であって実測ではない**):
```bash
python -c "
from sympy import bernoulli, Rational, factorint
for k in [12,16,18,20,22,26]:
    B=bernoulli(k); num=Rational(B,2*k).p
    print('k=%2d  num(B_k/2k) = %s  = %s'%(k,num,factorint(abs(num))))
"
# k=12 -> 691 が出れば §2.2 の動機どおり
```
