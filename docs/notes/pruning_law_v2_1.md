# 刈り込み処方 **v2.1** — 修理記帳と現在地(刈り込み律の顛末)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 位置づけ: `pruning_law_v2.md` の**修理版・非上書き**(v1・v1.1・v2 はいずれも不変)。
- 入力: Sol 便 88 P88-1 の修理 4 点(**司令塔経由で伝達されたもの。私は便 88 本文を読んでいない** — ブラインド相互監査の規律による。文言の最終突合は司令塔が行うこと)/ `docs/notes/sat_l1_v1.md`(新定理群の正本)。
- **本稿の役割**: 刈り込み律(PRUNE 系)の**顛末を閉じる記録**。**生きた数学の正本は `sat_l1_v1.md` に移った**。本稿は「何が死に、何が無傷で、後継は何か」の索引である。

---

## 0. 格付け表(新世界との関係)

| 主張 | v2 での格 | **v2.1(現在)** |
|---|---|---|
| **定理 PRUNE-FIX**($C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{\,s_2(r)}$) | 定理(相互監査) | **無傷・定理のまま**。ただし**核とは無関係**であることが確定(§2) |
| 上包含 $\Xi(\ker\widetilde\chi)\subseteq\mathrm{Pr}(H)$(v2 §5) | 「既測 2 事実から従う」 | **撤回**。$r=4$ 両枝が反例(§3.1)。$n{=}18$ 窓では**証明つきの反例**(§3.2) |
| 飽和(S) $\Xi(\ker)\supseteq\mathrm{Pr}(H)$ | candidate | **問い自体が失効**(右辺が誤った標的)。後継は **CENT**(§4) |
| 系 PRUNE-1 核側 $\ell^{s_2(r)}$ | candidate | **反証**。正しい形は **$\ell^{\,r-p}$**(p 律・§4.2) |
| Stab 律(2-部 $=\mathrm{Syl}_2(H)$) | candidate | **反証**($r{=}4$ B 枝で $V_4\ne D_8$)。正しい形は $\mathrm{Syl}_2(C_{S_n}(w))$ |
| 補題 SAT-T1(transporter 非空) | candidate | **定理**(§5・sign 判定式+分裂例外) |
| 鍵補題 SAT-L1(アフィン性) | 「未証明の本丸」 | **偽・撤回**(§6)。後継は word map $\mathcal R_\alpha$ / 非可換 $Z^1$ |
| torsor $\mathcal T_\alpha=f_0C_P(\bar y)$(v2 §6.3 の右剰余類) | — | **訂正**: 左剰余類 $C_P(\bar y)f_0$(§6.1) |
| — | — | **新: 定理 SURV / SURV+**($C_{S_n}(w)\subseteq\Xi(\ker)\subseteq C_{S_n}(\bar x)$)(§4.1) |
| — | — | **新: 定理 CENT-0**($p{=}s{=}0$ で挟み撃ちが閉じ **CENT が定理**)(§4.3) |
| — | — | **新: 定理 TRI**(窓の存在ゲート $\mathrm{ord}(w)\ge7$)(§4.4) |
| — | — | **新: 壁 P4 到達**($n{=}24$ 窓で $\mathrm{GTSh}$ 非可解)(§4.5) |

> **一行**: 刈り込み(pruning)という描像そのものが誤りだった。**$\Xi(\ker\widetilde\chi)$ は $\mathrm{Stab}(\bar x)$ を刈り込んだものではなく、$\bar x$ の平方根 $w$ の中心化群**である。$p=s=0$ の窓では刈り込みは**ゼロ**($\Xi(\ker)=\mathrm{Stab}$ 丸ごと)。

---

## 1. 修理 4 点の記帳(便 88 P88-1)

| # | 修理項目 | 本稿での処置 |
|---|---|---|
| 1 | §5 の上包含を撤回・$r=4$ を反例として記録(F88-2.5) | **§3** |
| 2 | SAT-T1 を sign 判定式+分裂例外へ差し替え(F88-9.1) | **§5**(統合。両版は同内容と判断) |
| 3 | torsor を左剰余類へ訂正・SAT-L1 撤回・後継型へ参照(P88-SAT-1) | **§6**(`sat_l1_v1` §3 と相互参照) |
| 4 | 語法「検証 PASS」→「相互監査 PASS」等(F88-1.2 NOTE) | **§7** |
| 5 | 新定理群との整合(司令塔追加) | **§0・§4** |

---

## 2. 無傷なもの — 定理 PRUNE-FIX

> **定理 PRUNE-FIX**(= SOL87-FIX・Sol 発・Opus 独立再導出・$r=1..8$ 機械一致)は**そのまま定理である**:
> $$H=(C_\ell^{\,r}\rtimes S_r)\times S_t,\quad T\in\mathrm{Syl}_2(H)\ \Longrightarrow\ C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{\,s_2(r)} .$$

**ただしこれは核 $\ker\widetilde\chi$ について何も言わない。** v2 §0・§5 が既に「抽象群 $H$ の固定点計算まで」と正しく限定していた。v2.1 はその限定を**確定事実**に格上げする:$\Xi(\ker\widetilde\chi)$ は $C_{O_{2'}(H)}(T)\times T$ とは**別の部分群**である。

$s_2(r)$ という指数は、$H$ の内部構造としては正しく、**核の律としては誤り**だった。

---

## 3. 撤回 — 上包含 $\Xi(\ker)\subseteq\mathrm{Pr}(H)$

> ### 撤回記帳 R-PRUNE-2(上包含の撤回)
> v2 §5 表の「$\subseteq$ は v1 §4.2 で既測 2 事実から従う」を**撤回する**。補題 PR-1 は前提 **(D)** $\ker\widetilde\chi=A\times S'$(直積)と **(T)** Stab 律に依存しており、その両方が偽である。

### 3.1 反例 1 — $r=4$ 両枝(実測)

$\mathrm{Pr}(H)$ の奇部は定理 PRUNE-FIX により $\ell^{s_2(4)}=5$。実測は

| 枝 | $\varepsilon$ | $\lvert\ker\rvert$ | 奇部 | 2-部 | $\mathrm{Pr}(H)$ の奇部 | 判定 |
|---|---|---|---|---|---|---|
| C | 0 | 200 | **25** | $D_8$ | 5 | $\subseteq$ **不成立**(25 > 5) |
| B | 1 | 500 | **125** | $C_2\times C_2$ | 5 | $\subseteq$ **不成立**(125 > 5・2-部も $\mathrm{Syl}_2(H)=D_8$ でない) |

共役を取っても位数が足りないので、**どの Sylow の取り方でも包含は復活しない**。B 枝は Stab 律の反例でもある。

### 3.2 反例 2 — $n=18$ 窓(**証明つき**)

`sat_l1_v1` §10.6.4 の窓 `W-CENT-B`($\ell=9$、$(r,t)=(2,0)$、$w_0=(9,9)$、$p=s=0$)では、定理 CENT-0(§4.3)により
$$\Xi(\ker\widetilde\chi)=\mathrm{Stab}(\bar x)=C_9\times D_{18}\quad(\text{位数 }162)$$
が**定理として**成立する。一方 $\mathrm{Pr}(H)=C_{O_{2'}(H)}(S)\times S$ の位数は $9\cdot2=18$。**9 倍差で、測定ではなく証明による反証**である(162 個の $f_z$ の全数検算つき)。

> **⟹ 「刈り込み」は起きていない。$p=s=0$ の窓では $\Xi(\ker)$ は $\mathrm{Stab}$ 丸ごとである。**

---

## 4. 後継 — 現在の正本(`sat_l1_v1.md`)

### 4.1 定理 SURV / SURV+(下からの構成)

窓の marking を $a_1$($a_1^2=1$)・$b_1$($b_1^3=1$)、$w:=b_1^{-1}a_1$($\bar x=w^2$)、$v:=a_1b_1^{-1}$ とする。

> **定理 SURV**: $z\in C_{S_n}(v)$ ごとに $f_z:=(a_1^{\,z})a_1\in P$ は $m=0$ hexagon を満たし、$z\mapsto f_z$ は単射。
> **定理 SURV+**: $\Xi([0,f_z])=z^{a_1}$。ゆえに
> $$\boxed{\ C_{S_n}(w)\ \subseteq\ \Xi(\ker\widetilde\chi)\ \subseteq\ C_{S_n}(\bar x)=C_{S_n}(w^2).\ }$$

これが「何が生き残るか」を出す工房初の定理であり、v2 §6.5 が「一本もない」と書いた空白を埋める。

### 4.2 予想 CENT と p 律(位数の閉じた式)

> **予想 CENT**: $\ker\widetilde\chi\cong C_{S_n}(w)$。**11/11 窓で位数一致**・$r=4$ 両枝は構造文字列と `IdGroup` まで一致。
> **p 律(CENT-ORD)**: $w=(2\ell)^p(\ell)^{r-2p}(2)^s(1)^{t-2s}$ と書くと
> $$\lvert\ker\widetilde\chi\rvert=(2\ell)^pp!\cdot\ell^{\,r-2p}(r-2p)!\cdot2^ss!\cdot(t-2s)!,\qquad \lvert\ker\rvert_\ell=\ell^{\,r-p}\ (\text{標準域}).$$
> $\varepsilon$ は $\mathrm{sgn}(w)=\mathrm{sgn}(a_1)=(-1)^{p+s}$ でパリティを固定する。

**核側 $s_2$ 律の反証はここから**: $r\le3$ では TRI(§4.4)が $p$ を一意にして偶然 $r-p=s_2(r)$ になっていた。$r=4$ で $p$ に自由度が生じ、$p=2\Rightarrow\ell^2$、$p=1\Rightarrow\ell^3$ のどちらも $s_2(4)=1$ と外れる。

### 4.3 定理 CENT-0(挟み撃ちの閉包)

> **定理 CENT-0**: $p=s=0$(= $w$ が偶長巡回をもたない)なら $\ell$ 奇より $\langle w\rangle=\langle w^2\rangle$、ゆえに $C_{S_n}(w)=C_{S_n}(\bar x)$ となり §4.1 の挟み撃ちが閉じる:
> $$\Xi(\ker\widetilde\chi)=C_{S_n}(w)=\mathrm{Stab}(\bar x).$$
> **この族では CENT は定理であり、PRUNE は証明つきで反証される。**

### 4.4 定理 TRI(窓の存在ゲート)

> $a_1^2=b_1^3=1$ ゆえ $\langle a_1,b_1\rangle$ は von Dyck 群 $\Delta(2,3,\mathrm{ord}(w))$ の商。$\Delta(2,3,m)$ は $m\le5$ で有限($A_4,S_4,A_5$)。**$\mathrm{ord}(w)\le5$ の窓は存在しない。**

これが「$\ell=5$・$t=0$ で $p\ge1$ 強制」の出所であり、$r\le3$ での $s_2$ 律の見かけの成功の原因でもある。

### 4.5 壁 P4 到達

`sat_l1_v1` §10.6.5 の窓 **P-WALL-2**($n=24$、$\ell=19$、$(r,t)=(1,5)$、$w_0=(19,1^5)$)で
$$\Xi(\ker\widetilde\chi)=C_{S_{24}}(w_0)=C_{19}\times S_5\quad(\text{位数 }2280,\ \textbf{非可解})$$
が定理 CENT-0 により成立(2280 個の $f_z$ を構成し hexagon+全射を全数検算・落ち 0)。**$\mathrm{GTSh}(N,N)$ は非可解**。飽和・剛性・$\Xi$ 単射のいずれも使っていない(下限のみ)。

---

## 5. 補題 SAT-T1 の正本(修理 2)

v2 §6.2 の「$A_n$-類が分裂しない」という言い方を、**sign 判定式+分裂例外の場合分け**に差し替える。司令塔経由で伝えられた Sol 版(F88-9.1)と本稿版は**同内容と判断**する(私は便 88 本文未読 — 文言の最終突合は司令塔)。

> ### 補題 SAT-T1【定理・初等・完結】
> $\mathcal T_\alpha:=\{f\in P=A_n:\ \bar y^{\,f}=\bar y^{\,\alpha}\}$ とすると
> $$\mathcal T_\alpha\ne\varnothing\iff C_{S_n}(\bar y)\,\alpha\cap A_n\ne\varnothing\iff\bigl[\ \mathrm{sgn}(\alpha)=+1\ \ \text{または}\ \ C_{S_n}(\bar y)\not\le A_n\ \bigr].$$
> $\bar y$ が型 $(\ell^{\,r},1^{\,t})$($\ell$ 奇)なら $C_{S_n}(\bar y)=(C_\ell\wr S_r)\times S_t$ で
> $$C_{S_n}(\bar y)\not\le A_n\iff r\ge2\ \text{または}\ t\ge2$$
> ($\ell$ 奇ゆえ $\ell$-巡回は偶、2 つの $\ell$-ブロックの互換は $\ell$ 個の互換の積で**奇**、$S_t$ の互換も奇)。
> **分裂例外 $r=1,\ t\le1$**: このとき $C_{S_n}(\bar y)\le A_n$ なので判定は $\mathrm{sgn}(\alpha)=+1$ に落ちる。しかし同時に $H=C_{S_n}(\bar x)=C_\ell\le A_n$ なので**全ての $\alpha\in H$ は偶**。
> **⟹ 系: 本族の全窓・全 $\alpha\in H$ で $\mathcal T_\alpha\ne\varnothing$。**
> **証明.** $\bar y^{\,f}=\bar y^{\,\alpha}\iff f\alpha^{-1}\in C_{S_n}(\bar y)\iff f\in C_{S_n}(\bar y)\alpha$。剰余類が $A_n$ と交わるのは $\alpha$ が偶か、$C_{S_n}(\bar y)$ が奇置換を含むときに限る。∎

**格**: 定理(v2 の candidate から格上げ)。**「類の分裂」ではなく「剰余類が $A_n$ と交わるか」が正しい定式化**である(両者は同値だが後者は 1 行で閉じる)。

---

## 6. torsor の訂正と SAT-L1 の撤回(修理 3)

### 6.1 訂正: torsor は**左**剰余類

v2 §6.1 は $f'f^{-1}\in C_P(\bar y)$ と正しく書いたが、§6.3 で $f=f_0c$ と右から掛けていた。$\bar y^{\,f}=f^{-1}\bar yf$ の規約では
$$\bar y^{\,f}=\bar y^{\,f_0}\iff ff_0^{-1}\in C_P(\bar y)\iff \boxed{f=c\,f_0\ \ (c\in C_P(\bar y))}$$
で**左剰余類**。この訂正なしに §6.3 の平行移動公式は成立しない。

### 6.2 撤回: 鍵補題 SAT-L1

> ### 撤回記帳 R-PRUNE-3
> v2 §6.3 の**鍵補題 SAT-L1(アフィン性 + 対角到達)を撤回する。偽である。**
> $\mathcal A(f):=(fa)^2$ に対し平行移動公式は $\mathcal A(cf_0)=\rho_a(c)\mathcal A(f_0)$、$\rho_a(c)=c\cdot{}^{u}c$($u=f_0a$)で**正しく成立する**が、$\rho_a$ が準同型 $\iff[P,{}^uP]=1\iff P$ 可換。$P=A_n$ は完全群ゆえ**準同型でない**(反例: `W-E-A10-5x2t0`、$625$ 対中 $576$ 対で破れる)。
> したがって「解集合 $=\ker\rho$ の coset」「障害 $=\operatorname{coker}\rho$ の 1 元」は**いずれも成立しない**。

**後継**(`sat_l1_v1` §3.4・§2 が正本。司令塔経由で伝えられた Sol の P88-SAT-1 の word map $\mathcal R_\alpha$ と同型の診断と理解する):

- 正しい枠組みは**非可換 1-コサイクル**: $\{f:\mathcal A(f)=1\}=Z^1(\langle a\rangle,P)$、$\{f:\mathcal B(f)=1\}=Z^1(\langle b\rangle,P)$。障害は $\operatorname{coker}$ ではなく $H^1$ の類の**対角一致**条件。
- 同値な閉じた形(**定理 RED**): $m=0$ hexagon $\iff (fa_1)^2=1\wedge(fb_1^{-1})^3=1$ $\iff$ **$v=a_1b_1^{-1}$ の (2,3)-分解** $v=gh$($g^2=h^3=1$、$g=fa_1$)。
- 飽和は**剛性**へ還元(`sat_l1_v1` §6.2): $C_{S_n}(v)$ は生成分解の集合に**自由に**作用し、$\lvert\ker\rvert=\lvert C_{S_n}(v)\rvert\cdot N$。11 窓で $N=1$。

---

## 7. 語法の是正(修理 4)

| v2 の表現 | v2.1 で採る表現 |
|---|---|
| 「証明 2 本の**検証 PASS**」(§0・§2) | **相互監査 PASS**(Sol 起草 → Opus 独立再導出)。「検証(verified)」は **Lean 専用語**であり使わない |
| 「**紙 = Sol・機械 = 本稿**の二系統 = cross-checked」(§4.1) | 二系統の内訳は「**紙上証明の独立再導出**(Opus)+ **GAP 単系統の数値確認**(Opus)」。**紙と機械の担当者は同一人**であり、「紙×機械の二系統」という表現は**不正確**。正しくは「**Sol の紙上証明を Opus が独立再導出し、加えて機械確認を付した**」 |
| 「$r=1..8$ 全一致(MATCH? true)」 | 表現は不変(GAP 単系統 measured) |
| 「較正(calibrated)」 | 不変 |

**規律の再確認**: cross-checked(二系統一致)/ verified(Lean)/ measured(単系統)を混同しない。**本稿および `sat_l1_v1` の機械結果はすべて GAP 単系統 measured であり、cross-checked ではない。**

---

## 8. 現在地(関係図)

```
                     定理 PRUNE-FIX  (無傷・H の内部構造)
                              |  ※核とは無関係と確定
   ---------------------------+-------------------------------
   刈り込み描像(PRUNE 系)                    後継(sat_l1_v1)
   Xi(ker) = C_{O_2'(H)}(S) x S              定理 RED: hexagon = (2,3)-分解
      |- 上包含  ... 撤回(§3)                   |
      |- 飽和    ... 標的が誤り                  |- 定理 SURV/SURV+ : C(w) ⊆ Xi(ker) ⊆ C(x)
      |- s2 律   ... 反証 -> p 律 l^{r-p}        |- 定理 CENT-0 : p=s=0 で両端一致 => 定理
      |- Stab 律 ... 反証 -> Syl_2(C(w))         |- 予想 CENT   : 一般窓(11/11 measured)
      |- SAT-L1  ... 偽・撤回(§6)               |- 定理 TRI    : 窓の存在ゲート
      |- SAT-T1  ... 定理へ格上げ(§5)           |- 剛性 N=1    : 飽和の後継問題(未証明)
                                                 |- 壁 P4 到達  : n=24 で GTSh 非可解
```

**残る未証明**(`sat_l1_v1` §9.1 が正本): 剛性 $N=1$(一般窓での CENT の $\subseteq$)・【GAP-S1】生成条件の紙上証明・$m\ne0$ 層の一般公式・$\Xi$ 単射。

---

## 9. 検算

本稿は新しい計算を行わない。参照先はすべて `sat_l1_v1.md` §10(`search/probe/wac_v1/sat_l1_probe1..13.g`・SHA-256 併記)および v2 §8(`sol87_fix.g` ほか)。**すべて GAP 4.16.0 単系統。登録宇宙の掃引結果ではなく、台帳請求権は発生していない。**
