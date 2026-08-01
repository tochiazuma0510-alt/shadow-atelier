# 追補(erratum)— **§6 の「1 行 assert」は偽だった**。正しい対象は**反準同型ラベル $\ell$**(または opposite 群 $P^{\rm op}$)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 位置づけ: `docs/notes/pent_settled_cent_v1.md`(本体)への **第 1 追補**。**erratum 方式 — 本体は 1 バイトも書き換えない。**
- 委嘱: 司令塔(便 93 修理波・裁定 303)「settled の『1 行 assert』を正対象(反準同型ラベル/opposite group)で書き直し — **実装係の捕獲が正しかった件**」
- 入力正本: `sol/sol_reply_93_math20.md` **F93-4.1 / W93-4.1 / P93-4**
- 検算: `search/probe/wac_v1/repair93_check.py` §F(`d35e7949…0faaf4e2`)/ `search/probe/wac_v1/repair93_opp_check.py`(`54ddb7e8 71d1b2a0 21d0e8a8 03a36f78 8b081b66 f8d98cd9 ecab2b35 69e2904d`)。**いずれも純整数(置換)演算・本体 probe を import しない独立実装。**

---

## 0. 結論(先に 5 行)

| # | 内容 | 格 |
|---|---|---|
| **①** | **本体 §6 末尾の「修理の指定(実装係へ・1 行の assert で十分)」は偽である。** $\rho(T'(\Psi(y)))\overset{!}{=}(\bar y^u)^f$ は**非自己逆元 $f$ で一般に成立しない**。**実装係の cert 失敗行は実装事故ではなく、型の不一致を正しく捕獲していた** | **erratum(私の誤指定)** |
| **②** | 正しい可換図は**粗ラベル $\ell:=\tau\circ\rho$ を通した**もの: $\boxed{\ \ell\bigl(T'(\Psi(y))\bigr)=(\bar y^u)^f\ }$。$\rho$ 側で書くなら $\rho(T'(\Psi(y)))=(\bar y^u)^{\hat c(f)}$ | **定理**(§2)+ **240/240 機械** |
| **③** | $\ell$ は**準同型ではなく反準同型**($\ell(q_1q_2)=\ell(q_2)\ell(q_1)$)。型としては $\ell:Q_P\to P^{\rm op}$ が**群準同型** | **定理**(1 行) |
| **④** | ★ **Sol 要求 2(「$T'$ の合成と opposite 側の積が一致する」)を証明した**(補題 OPP)。正典の合成則 (3.53) は $\tau$-座標で $g_{12}=\Phi'_{m_1,g_1}(g_2)\cdot g_1$ という**逆順の積**になる。**9600 対で機械一致** | **定理 + 機械(新規)** |
| **⑤** | 残る gate は Sol 要求 3(PB₃ 層 20/20 と PB₄ source kernel の分離)と要求 4(`red` の積保存)。**$\mathrm{GT}(K_\pi)$ の群化・`red` の準同型化は candidate のまま**、$K_\pi$ の `isolated (candidate)` 復活は承認済 | **未閉鎖の名指し** |

> **一行で**: 私は「向きの混線」を正しく診断しておきながら、**その修理指定を混線したままの座標で書いた**。$\Psi$ が反準同型である以上、ラベル $f$ と作用の比較は $\rho$ ではなく $\ell=\tau\circ\rho$ の側で書かねばならない。

---

## 1. 誤りの正確な所在

### 1.1 本体の該当箇所(逐語)

> 本体 §6 末尾:
> > ### 修理の指定(実装係へ・1 行の assert で十分)
> > 非自己逆元 $f$(例 $(2,3,4)$)について、**$T$ の $y$-像の粗成分が $\Phi_{m,f}(\bar y)$ に等しいこと**を hard assert せよ:
> > $$\rho\bigl(T(\Psi(y))\bigr)\ \overset{!}{=}\ \Phi_{m,f}(\bar y)=(\bar y^u)^f .$$

### 1.2 なぜ偽か(Sol W93-4.1 の再構成)

指数を $a^g=g^{-1}ag$ とする。整合規約 $T'$($\Psi(y)\mapsto q\,\Psi(y)^uq^{-1}$)について、$\rho$ を直接取ると **定理 ORI**($\rho(q)=\hat c(f)^{-1}$)より

$$\rho\bigl(T'(\Psi(y))\bigr)=\rho(q)\,\bar y^u\,\rho(q)^{-1}=\hat c(f)^{-1}\bar y^u\hat c(f)=(\bar y^u)^{\hat c(f)} .$$

$\hat c(f)=f$ は「$f$ が $\hat c$-不変」の条件であり、settled 4 行($f\in\{1,\kappa\}$)では自明に成り立つが**一般には成り立たない**。ゆえに指定した assert は非自己逆元で落ちる。

**機械確認(§F・$P=A_5$、$u\in\{1,3,7,9\}$、$f$ は $A_5$ 全 60 元 = 240 対)**:

| 主張 | 結果 |
|---|---|
| $\rho(T'(\Psi(y)))\overset{!}{=}(\bar y^u)^f$(**本体の指定**) | **160/240 で不成立** ⟹ **偽** |
| $\rho(T'(\Psi(y)))=(\bar y^u)^{\hat c(f)}$(Sol) | **240/240 一致** |
| $\ell(T'(\Psi(y)))=(\bar y^u)^f$(**正しい指定**) | **240/240 一致** |

(一致する 80 対は $\hat c(f)f^{-1}\in C_P(\bar y)=\langle\bar y\rangle$ の 20 個の $f$ × 4 個の $u$。**settled 4 行はこの中に含まれる** — だから本体 §6 の診断そのものは無傷で、誤りは修理指定の書き方だけだった。)

### 1.3 実装係の捕獲は正しかった(明示の訂正)

cert の当該失敗行は**実装事故ではない**。私が渡した assert が**型として誤っていた**ため、正しい実装がそれを拒否した。**捕獲は正しく、指定側が誤っていた。** この訂正を記録に残す。

> **★教材**: 診断で「$\Psi$ は反準同型だから共役の向きが裏返る」と正しく書いた直後に、**修理の assert を $\rho$(準同型)側の等式として書いた**。反準同型を診断に使ったなら、修理も反準同型の座標で書かなければならない。**診断と処方で座標を変えない** — 本件の一行教訓。

---

## 2. 正しい可換図(P93-4 の採択・証明つき)

### 2.1 記号

$\tau(g):=\hat c(g)^{-1}$($P$ の位数 2 の**反自己同型**;本体 §2)、$\ell:=\tau\circ\rho:Q_P\to P$。定理 ORI より $\rho(q)=\tau(f)$、$\tau^2=\mathrm{id}$ ゆえ

$$\boxed{\ \ell(q)=\tau(\rho(q))=\tau(\tau(f))=f\ }$$

すなわち **$\ell$ は probe の粗ラベルそのもの**である。

### 2.2 定理 LBL(正しい 1 行 assert)

> ### 定理 LBL【定理・3 行】
> $$\boxed{\ \ell\bigl(T'(\Psi(y))\bigr)\ =\ (\bar y^u)^f\ =\ \Phi_{m,f}(\bar y)\ }$$
> **証明.** $\tau$ は反自己同型ゆえ $\tau(abc)=\tau(c)\tau(b)\tau(a)$、$\tau(g^{-1})=\tau(g)^{-1}$。また $\tau(\bar y^u)=\bigl(\hat c(\bar y)^u\bigr)^{-1}=\bigl(\bar y^{-u}\bigr)^{-1}=\bar y^u$($\hat c$ は $\bar y$ を反転する)。よって
> $$\ell(T'(\Psi(y)))=\tau\bigl(\rho(q)\bar y^u\rho(q)^{-1}\bigr)=\tau(\rho(q))^{-1}\,\tau(\bar y^u)\,\tau(\rho(q))=f^{-1}\bar y^uf=(\bar y^u)^f .\ \blacksquare$$
> **機械**: §F で 240/240 一致(不一致 0)。

### 2.3 実装係への**新しい**指定(本追補が本体 §6 の指定を置換する)

> ### 修理の指定 v2(実装係へ)
> 非自己逆元 $f$(例 $(2,3,4)$)を含む**全行**について、次を hard assert せよ:
> $$\underbrace{\mathrm{coarse\_of}\bigl(\mathrm{WordOf}\bigl(T'(\Psi(y))\bigr)\bigr)}_{=\ \ell(T'(\Psi(y)))}\ \overset{!}{=}\ (\bar y^u)^f .$$
> **同値な、$\rho$ しか使わない形**(実装が $\ell$ を持たない場合):
> $$\rho\bigl(T'(\Psi(y))\bigr)\ \overset{!}{=}\ (\bar y^u)^{\hat c(f)},\qquad \hat c=\mathrm{conj}_\kappa,\ \kappa=(1,4)(2,5).$$
> **禁止**: $\rho(T'(\Psi(y)))\overset{!}{=}(\bar y^u)^f$(= 本体の旧指定・**偽**)。
> **回帰 fixture**: 旧指定が落ちること(160/240)を**負例として保存**する。

---

## 3. 型の固定 — Sol 要求 1〜4 への逐条対応

### 3.1 要求 1: $\ell(q_1q_2)=\ell(q_2)\ell(q_1)$ を型として固定【**閉じた**】

> ### 補題 ANTI【定理・1 行】
> $\rho$ は準同型、$\tau$ は反自己同型ゆえ
> $$\ell(q_1q_2)=\tau\bigl(\rho(q_1)\rho(q_2)\bigr)=\tau(\rho(q_2))\,\tau(\rho(q_1))=\ell(q_2)\ell(q_1).$$
> すなわち **$\ell:Q_P\to P^{\rm op}$ は群準同型**である。∎
> **型宣言(以後の正本)**: 粗ラベル写像の余域は $P$ ではなく **$P^{\rm op}$** とする。本体 系 ORI′ の「well-defined な反準同型」はこの型宣言と同じ内容である。

### 3.2 要求 2: $T'$ の合成と opposite 側の積が一致【**閉じた(本追補の新規結果)**】

> ### 補題 OPP【定理 + 機械 9600 対】
> $g_i:=\tau(f_i)$、$u_i:=2m_i+1$、$E_{m,f}\in\mathrm{End}(P)$ を正典の $\bar x\mapsto\bar x^{u},\ \bar y\mapsto f^{-1}\bar y^{u}f$、$\Phi'_{m,g}$ を $\bar x\mapsto\bar x^{u},\ \bar y\mapsto g\bar y^{u}g^{-1}$ とする。このとき
> $$\boxed{\ \tau\circ E_{m,f}\circ\tau\;=\;\Phi'_{m,\tau(f)}\ }$$
> であり、正典の合成則 (3.53) $f_{12}=f_1\cdot E_{m_1,f_1}(f_2)$ は $\tau$-座標で
> $$\boxed{\ g_{12}\;=\;\Phi'_{m_1,g_1}(g_2)\cdot g_1\ }$$
> となる。**すなわち $\tau$ は「正典の積」を「$\Phi'$ で捻れた opposite の積」へ写す。**
>
> **証明.** $\hat c(\bar x)=\bar x^{-1},\hat c(\bar y)=\bar y^{-1}$ ゆえ $\tau(\bar x)=\bar x,\ \tau(\bar y)=\bar y$ — **$\tau$ は生成元を固定する**(が、恒等写像ではない:反準同型である)。$\tau\circ E\circ\tau$ は(反 ∘ 準同型 ∘ 反)= 準同型で、生成元では
> $$\bar x\mapsto\tau(E(\bar x))=\tau(\bar x^{u})=\bar x^{u},\qquad
> \bar y\mapsto\tau(E(\bar y))=\tau(f^{-1}\bar y^{u}f)=\tau(f)\,\bar y^{u}\,\tau(f)^{-1}$$
> ゆえ $\Phi'_{m,\tau(f)}$ に一致。よって
> $$\tau\bigl(f_1E_{m_1,f_1}(f_2)\bigr)=\tau\bigl(E_{m_1,f_1}(\tau(g_2))\bigr)\,\tau(f_1)=(\tau E_{m_1,f_1}\tau)(g_2)\cdot g_1=\Phi'_{m_1,g_1}(g_2)\cdot g_1 .\ \blacksquare$$
>
> **機械**(`repair93_opp_check.py`): $m\in\{0,1,2,3,4\}$、$\Phi_{m,f_1}$ が存在する $f_1$ 全て($25+25+60+25+25=160$ 対)× $f_2\in P$ 全 60 元 = **9600 対で全一致**。

> ### ⟹ 何が言えたか
> 「$\mathrm{GT}(K_\pi)$ を群と呼んでよいか」という問いのうち、**合成則の側は $P^{\rm op}$ 座標で整合する**ことが確定した。$T'$ が実現する写像の合成が (3.53) と一致するのは、上の $\tau$-辞書を通してである。**残るのは $Q_P$ 水準($\ker\rho=V$ を含む層)での主張**(§3.4)。

### 3.3 要求 3: PB₃ 層の 20/20 と PB₄ の source kernel / Prop. 2.11 の分離【**明示**】

| 層 | 主張 | 格 |
|---|---|---|
| **PB₃ 層** | 整合規約 $T'$ で `well_defined = 20/20`、`settled = 20/20` | **採択済**(Sol F93-4.1)。本体 §6 の (U-rev)/(U-fwd) 二経路 + 機械 |
| **PB₄ 層** | source kernel の isolated 性・Prop. 2.11 相当 | ★ **未着手**。**PB₃ の 20/20 からは一切従わない**(本体 LEVEL CAVEAT) |
| 混同の禁止 | 「20/20 settled」を PB₄ の主張として引用しない。cert の必須欄に `level = PB3` を持つ | **手続き** |

### 3.4 要求 4: `red` が積を保つ【**未閉鎖・名指し**】

> ### 【GAP-PSC-2】(新規・名指し)
> `red`(= 粗化 $\mathrm{GT}(K_\pi)\to\mathrm{GT}(N_A)$ に相当する写像)が**積を保つ**ことは、上の $P^{\rm op}$ 型のもとで**まだ証明されていない**。必要な段は 2 つ:
> 1. **$Q_P$ 水準への持ち上げ**: 補題 OPP は $P=Q_P/V$ 上の等式である。$V=Z(Q_P)\cong C_5^3$ 上でも合成が整合すること(本体 定理 STR/TRI の $T=\Phi\times(u\cdot\mathrm{id}_V)$ 分解を合成に対して回す)。
> 2. **$\ell$ の $\mathrm{GT}$ 水準への降下**: $\ell$ は $Q_P\to P^{\rm op}$ だが、必要なのは shadow の対 $(m,q)\mapsto(m,\ell(q))$ が合成と可換であること。$m$ 成分は $(m_1,m_2)\mapsto2m_1m_2+m_1+m_2$ で**可換**(順序に依らない)ので、**非可換性は $f$ 成分にのみ現れる** — この非対称が opposite 型の必然性である。
>
> **⟹ この 2 段が済むまで、$\mathrm{GT}(K_\pi)$ の群化と `red` の準同型化は candidate。**(Sol P93-4 の判定と一致。)

---

## 4. 状態札の更新(裁定 293 まわり)

| 項目 | 便 93 前 | **本追補後** |
|---|---|---|
| 整合規約 $T'$ での `well_defined=20/20`, `settled=20/20` | candidate | **採択**(Sol F93-4.1) |
| 旧 `4/8/8`(混成規約) | 反例か artifact か係争 | **反例ではない**。廃止した混成規約の**回帰 fixture** として保存 |
| $K_\pi$ の isolated | 降格中 | **`isolated (candidate)` に復活してよい**(Sol 承認) |
| $\mathrm{GT}(K_\pi)$ の群化 | 既成 | **candidate**(要求 3・4 未了) |
| `red` の準同型性 | 既成 | **candidate**(【GAP-PSC-2】) |
| 本体 §6 の「1 行 assert」 | 指定済 | **撤回**。§2.3 の**修理の指定 v2** が正本 |
| 定理 STR / ORI / TRI / KQ / SC | 定理 | **無傷**(規約に依存しない構造定理) |
| Lean | — | **verified ではない**(本追補も紙 + 機械のみ) |

---

## 5. 予言の更新

本体 §8 の **P-SC-0**(修理後は 20/20 settled)は **実現した**(整合規約 $T'$ で 20/20)。**P-SC-1**(現行実装を他窓へ回した場合の settled 行 $=\{(m,f):\tau_N(f)\in\Sigma_m\}$)は**混成規約の予言**として保存し、**修理後の実装には適用しない**。**P-SC-2**(核の二値性)・**P-SC-3**($\hat c$ の存在条件)は規約非依存ゆえ**そのまま生存**。

> ### 予言 P-SC-4(**新規・本追補**)
> 補題 OPP は $P$ の**具体形に依らない**($\hat c$ が両生成元を同時反転する $\mathrm{Aut}(P)$ の元として存在すれば成り立つ)。ゆえに **$\hat c_N$ が存在する任意の窓で、正典の合成則は $\tau_N$-座標で opposite 積になる**。
> **追試**: 壁族の既存 cert で $\hat c_N$ の存在を調べ、存在する窓では $\ell$ が反準同型であることを 1 行 assert で確認する。**新測定ゼロ**(既存 cert の粗ラベル列を読むだけ)。
> **破綻条件**: $\hat c_N$ が存在するのに $\ell$ が準同型に見える窓があれば、その窓の実装は**まだ混線している**。

---

## 6. Sol への申し送り(第 2 巡)

- **監査点 A**: **補題 OPP**($\tau\circ E_{m,f}\circ\tau=\Phi'_{m,\tau(f)}$)。骨は「$\tau$ が**生成元を固定する反準同型**である」という 1 点。$\hat c$ が両生成元を反転することの帰結だが、**この一致が偶然かどうか**を見てほしい($\hat c$ = 複素共役 shadow の像であることと関係があるなら、opposite 型は「複素共役が向きを反転する」ことの群論的影である)。
- **監査点 B**: §3.4 の分解 —「$m$ 成分の合成 $2m_1m_2+m_1+m_2$ は可換ゆえ、非可換性は $f$ 成分にのみ現れる」。これが opposite 型の**必然性**の説明として十分か。
- **監査点 C**: §2.3 の実装指定 v2 のうち $\rho$ だけを使う形 $\rho(T'(\Psi(y)))=(\bar y^u)^{\hat c(f)}$ — 実装が $\hat c$ を持たない場合の代替形として妥当か。
