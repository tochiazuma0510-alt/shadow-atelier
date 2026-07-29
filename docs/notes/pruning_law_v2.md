# 刈り込み処方 **v2** — SOL87-FIX 統合版(Sol 発・司令塔独立検証つき)

- 起草: 影工房 数学者(Claude)/ 2026-07-30
- 位置づけ: `pruning_law_v1.md`(初出・同定と PRUNE 主張)・`pruning_law_v1_1.md`(撤回・格付け・NORM 分離・補題 NORM-E)の**統合後継**。両者は不変。本稿が正本。
- 入力: `sol/sol_reply_87_math14.md` §9(定理 SOL87-FIX・系 SOL87-PRUNE・証明 2 本・torsor 分解)/ 裁定 232
- 状態: **SOL87-FIX = 定理(Sol 発・本稿で独立検証 PASS)/ PRUNE 飽和・$\Xi$ 単射 = 未証明(candidate)**。数値は GAP 4.16.0 単系統。

---

## 0. 結論(先出し)

| 委嘱項目 | 結果 |
|---|---|
| **① 証明 2 本の独立再導出** | **両方 PASS。穴なし。** 暗黙前提を 3 点名指し(いずれも真・§2.3) |
| **② 機械裏取り** | **$r=1..8$ で $\lvert C_{O_{2'}(H)}(T)\rvert=\ell^{s_2(r)}$ を全一致確認**。$r=4$ は既測 $C_{B_x}(D_8)=\langle\bar x\rangle$(=5)と一致・**$r=5$ は新データ点 = 25**($C_5\times C_5$)。tail $C_3$ 消滅も確認(§3) |
| **③ 統合** | SOL87-FIX を**定理として §4 に統合**。ただし**これは核側 $\lvert\ker\rvert_{\rm odd}=\ell^{s_2(r)}$ を証明しない** — 周辺群の右辺を閉じただけで、残る 2 点(飽和・単射)への還元を明示(§5・§6) |
| 飽和の第一歩 | torsor 分解 $\mathcal T_\alpha$ を LOC-1 と接続。**障害を「hexagon residual の平行移動下の変分」として定義**し、線型性補題 SAT-L1 を「証明すべき鍵」として名指し(§6) |

**格の要点(誤読防止)**: SOL87-FIX が閉じたのは $H=(C_\ell^r\rtimes S_r)\times S_t$ という**抽象群**の中の固定点計算である。核 $\ker\widetilde\chi$ の奇部がこの値になるには、なお **PRUNE 飽和**(像の逆包含)と **$\Xi$ 単射**が要る。$r=4$ 測定(裁定 231・凍結 fd5aab9)は不要にならない — むしろ $(5,8)$ が返れば「固定点計算が当たった」だけでなく**新しい $r$ で飽和方向を初めて支持する**。

---

## 1. 記号(v1 から継承)

命題 0.3 型窓($c\in N$、$P=A_n$、$\bar x=(\ell^r,1^t)$、$\ell$ 奇)。$\mathrm{Aut}(P)=S_n$、
$$H:=\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{S_n}(\bar x)=(C_\ell^{\,r}\rtimes S_r)\times S_t,\qquad B:=C_\ell^{\,r},\qquad T:=\mathrm{Syl}_2(H).$$
$T_r:=T$ の $S_r$ 成分(射影 $H\to S_r$ の像)。$\langle\bar x\rangle\cong C_\ell$ は $B$ の全対角。
$\Xi:\mathrm{GTSh}(N,N)\to N_{\mathrm{Aut}(P)}(\langle\bar x\rangle)$、$[m,f]\mapsto E_{m,f}$(`pruning_law_v1_1.md` 補題 NORM-E)。$m=0$ 層で $E_{0,f}(\bar x)=\bar x$・$E_{0,f}(\bar y)=\bar y^{\,f}$。

$s_2(r)$ := $r$ の 2 進桁和。

---

## 2. 任務 ① — 証明 2 本の独立検証

### 2.1 定理 SOL87-FIX(Sol 発)

> $\ell$ 奇、$r,t\ge0$、$H=(C_\ell^r\rtimes S_r)\times S_t$、$B=C_\ell^r$、$T\in\mathrm{Syl}_2(H)$ に対し
> $$C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{\,s_2(r)},\qquad \bigl\lvert C_{O_{2'}(H)}(T)\bigr\rvert=\ell^{s_2(r)}.$$

### 2.2 証明 1(Sylow 2 の軌道数 $=s_2(r)$)— **PASS**

Sol の骨子を追い、各段を独立に確認した。

1. $r=\sum_{i=1}^{s_2(r)}2^{a_i}$(相異なる 2 冪・2 進展開)。✓
2. 各 $2^{a_i}$-block 上の $\mathrm{Syl}_2(S_{2^{a_i}})$ は**推移的**(反復輪積 $C_2\wr\cdots\wr C_2$($a_i$ 回)= 深さ $a_i$ の 2 分木の葉 $2^{a_i}$ 個への推移作用)。✓
3. $v_2\bigl((2^{a})!\bigr)=2^a-1$(Legendre $v_2(m!)=m-s_2(m)$、$s_2(2^a)=1$)。✓
4. block 直積の 2-adic order $=\sum_i(2^{a_i}-1)=r-s_2(r)=v_2(r!)$。**独立検算**: `scratchpad` の Python で $r=1..16$ の $\sum(2^{a_i}-1)=r-s_2(r)=v_2(r!)$ を全一致確認。✓
5. ゆえに block 直積 $\prod_i\mathrm{Syl}_2(S_{2^{a_i}})$($\{1..2^{a_1}\},\{..\},\dots$ の Young 型 block 埋め込み)は位数 $2^{v_2(r!)}=\lvert\mathrm{Syl}_2(S_r)\rvert$ の 2-部分群、ゆえ **$S_r$ の Sylow 2-部分群**。✓
6. その block 軌道数 $=s_2(r)$(各 block 上推移的・block は互いに素)。Sylow は共役で軌道数は共役不変ゆえ**任意の $T_r$ で $s_2(r)$**。✓
7. $B=C_\ell^r$ 上 $S_r$ は座標置換ゆえ $B^{T_r}=\{$各 $T_r$-軌道上で座標一定$\}\cong C_\ell^{\,(\text{軌道数})}=C_\ell^{\,s_2(r)}$。✓

**判定: 証明 1 は正しい。**

### 2.3 証明 2(symmetric top の奇 core は固定点を増やさない)— **PASS**

1. $O_{2'}(S_n)=C_3\ (n=3),\ 1\ (n\ne3)$:
 - $n\le4$ 直接: $S_1=1$、$S_2=C_2\Rightarrow1$、$S_3$ の正規部分群 $\{1,C_3,S_3\}$ で奇は $C_3$、$S_4$ の正規 $\{1,V_4,A_4,S_4\}$ で奇は $1$。✓
 - $n\ge5$: $S_n$ の非自明正規部分群は $A_n$ を含み、$A_n$ は偶位数($n!/2$)ゆえ奇位数正規部分群は自明のみ。✓
2. 直積の 2' 根基 $O_{2'}(A\times B)=O_{2'}(A)\times O_{2'}(B)$(標準)、および $O_{2'}(C_\ell^r\rtimes S_r)=B\rtimes O_{2'}(S_r)$(射影 $H\to S_r$ の $O_{2'}(S_r)$ の逆像 — $B$ 奇正規で最大)。ゆえに $O_{2'}(H)=(B\rtimes O_{2'}(S_r))\times O_{2'}(S_t)$。✓
3. $n=3$: $S_3$ の対合(互換)は 3-巡回を逆元へ共役 ⟹ $C_{C_3}(C_2)=1$。✓
4. $r=3$ の半直積因子: $x=bc\in B\rtimes C_3$ が $T$ を中心化 ⟹ 射影 $H\to S_3$ で $\bar c\in C_{C_3}(\tau)=1$($\tau=T_r$ の対合)⟹ $c=1$($c\in C_3$、$c=c^{-1}\Rightarrow c^2=1\Rightarrow c=1$)。残るは $x=b\in B$ かつ $[b,T]=1$、すなわち $b\in B^{T_r}$。tail の $C_3$($t=3$ のとき)も同様に消える。∎

**判定: 証明 2 は正しい。**

### 2.4 暗黙前提の名指し(3 点・いずれも真)

証明の correctness は変わらないが、Sol の本文が飛ばしている段を記録する:

- **【暗黙 1】$T\cap B=1$ ゆえ $T\cong T_r$ かつ $T_r\in\mathrm{Syl}_2(S_r)$。** 証明 1 は「$T_r$ が Sylow」を使うが本文は $T$(=$\mathrm{Syl}_2(H)$)から始める。$B$ 奇ゆえ $T\cap B=1$、$\lvert T_r\rvert=\lvert T\rvert=2^{v_2(r!)}=\lvert\mathrm{Syl}_2(S_r)\rvert$。真。
- **【暗黙 2】$O_{2'}(A\times B)=O_{2'}(A)\times O_{2'}(B)$ と $O_{2'}(B\rtimes S_r)=B\rtimes O_{2'}(S_r)$。** 標準事実。後者は「奇正規部分群の射影は $S_r$ の奇正規部分群 $\subseteq O_{2'}(S_r)$」から従う。真。
- **【暗黙 3】block 直積の $S_r$ への埋め込みが Young 部分群経由で subgroup をなす。** block が互いに素ゆえ自明に成立。真。

**いずれも証明の load-bearing な穴ではない**(埋めても結論不変)。

---

## 3. 任務 ② — 機械裏取り(`sol87_fix.g`)

$\ell=5$、$t=0$。$H=C_5\wr S_r$ を置換群構成し、$O_{2'}(H)=$(base の射影 $H\to S_r$ による $O_{2'}(S_r)$ の逆像)、$T=\mathrm{Syl}_2(H)$、$C=C_{O_{2'}(H)}(T)$ を直接計算。

| $r$ | $\lvert H\rvert$ | $\lvert B\rvert$ | $O_{2'}(S_r)$ | $\lvert O_{2'}(H)\rvert$ | $\lvert T\rvert$ | $s_2(r)$ | 予測 $5^{s_2}$ | **実測 $\lvert C\rvert$** | 構造 | $C\le B$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 5 | 1 | 5 | 1 | 1 | 5 | **5** | $C_5$ | ✓ |
| 2 | 50 | 25 | 1 | 25 | 2 | 1 | 5 | **5** | $C_5$ | ✓ |
| 3 | 750 | 125 | $C_3$ | 375 | 2 | 2 | 25 | **25** | $C_5^2$ | ✓ |
| **4** | 15,000 | 625 | 1 | 625 | 8 | 1 | 5 | **5** | $C_5$ | ✓ |
| **5** | 375,000 | 3,125 | 1 | 3,125 | 8 | 2 | 25 | **25** | $C_5^2$ | ✓ |
| 6 | 11,250,000 | 15,625 | 1 | 15,625 | 16 | 2 | 25 | **25** | $C_5^2$ | ✓ |
| 7 | 393,750,000 | 78,125 | 1 | 78,125 | 16 | 3 | 125 | **125** | $C_5^3$ | ✓ |
| 8 | $1.575\times10^{10}$ | 390,625 | 1 | 390,625 | 128 | 1 | 5 | **5** | $C_5$ | ✓ |

**$r=1..8$ 全一致(MATCH? true)。**

- **$r=4$: $\lvert C\rvert=5$** — 既測 $C_{B_x}(D_8)=\langle\bar x\rangle$(`r4_window.g`)と**一致**。SOL87-FIX の一般式が $r=4$ の周辺群計算を包含することの確認。
- **$r=5$: $\lvert C\rvert=25=C_5\times C_5$**(新データ点・$s_2(5)=2$)。$r=4$ の 5 から**再び上昇** — $s_2$ の非単調性の第二例。
- **$r=8$: $\lvert C\rvert=5$**($s_2(8)=1$)— $r=7$ の 125 から**急落**。単調律が絶対に出せない署名。
- **tail $C_3$ 消滅**($r=2,t=3$): $\lvert O_{2'}(H)\rvert=75$($=25\times3$)だが $\lvert C\rvert=5=5^{s_2(2)}$。証明 2 の tail 部分の機械確認 ✓。

---

## 4. 任務 ③ — SOL87-FIX の統合

### 4.1 定理として採録

> ### 定理 PRUNE-FIX(= SOL87-FIX・**Sol 発・司令塔独立検証 PASS**)【定理】
> §1 の記号で
> $$C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{\,s_2(r)}.$$
> **格**: 紙上証明(§2・初等有限群論)。Sol が起草、本稿が証明 2 本を独立に再導出(穴なし・暗黙前提 3 点は真)+ $r=1..8$ を機械確認。**cross-checked**(紙 = Sol・機械 = 本稿、二系統)。**Lean verified ではない。**

これは v1 §3.5 の「系 PRUNE-1」(奇部 $=\ell^{s_2(r)}$)の**周辺群側を定理へ格上げ**する。v1.1 §2 で「candidate のまま」とした 2 つのうち、**$s_2(r)$ という指数の群論的根拠は確定した**。

### 4.2 撤回済 $\ell^{r-1}$ 律との最終対照

| $r$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $s_2(r)$(**定理**) | 1 | 1 | 2 | 1 | 2 | 2 | 3 | 1 |
| $\ell^{r-1}$(**撤回済**) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 一致 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

$\ell^{r-1}$ は $r=2,3$ でのみ $s_2$ と一致する偶然だった(`pruning_law_v1_1.md` R-PRUNE-1 の撤回を定理で裏づけ)。$r=4$ の測定(凍結 fd5aab9)が $(5,8)$ を返せば、$s_2$ と $\ell^{r-1}$ は**測定で決着**する。

---

## 5. 何が残っているか(系 SOL87-PRUNE の正確な読み)

> ### 系 PRUNE-FIX-C(= SOL87-PRUNE)
> **(a)** PRUNE 像飽和 $\Xi(\ker\widetilde\chi)=C_{O_{2'}(H)}(T)\times T$ が成立すれば
> $$\bigl\lvert\Xi(\ker\widetilde\chi)\bigr\rvert_{\rm odd}=\ell^{s_2(r)}\quad(\text{定理 PRUNE-FIX による}).$$
> **(b)** さらに $\Xi\vert_{\ker\widetilde\chi}$ が単射なら
> $$\bigl\lvert\ker\widetilde\chi\bigr\rvert_{\rm odd}=\ell^{s_2(r)}.$$

**未証明は正確に 2 点**(Sol の名指しと一致):

| # | 未証明命題 | 現状の材料 |
|---|---|---|
| **(S)** PRUNE 飽和 | $\Xi(\ker)\supseteq C_{O_{2'}(H)}(T)\times T$(逆包含) | 16 標本の一致(実測 12)。$\subseteq$ は v1 §4.2 で既測 2 事実から従う。$\supseteq$ = §6 |
| **(I)** $\Xi$ 単射 | $\ker\Xi\cap\ker\widetilde\chi=1$ | 補題 NORM-E(`v1_1` §3.2)で「核層だけの検査」に落ちた。9 窓で実測 $\ker\Xi=1$(`norm_embedding_20260731.json`)。一般窓は未証明 |

**定理 PRUNE-FIX は (S)(I) のどちらも与えない** — $H$ という抽象群の固定点を数えただけで、その固定点が shadow として実現するか($S$)・shadow が像で潰れないか($I$)は別問題。**この分離を混同しないこと**が本統合の主眼。

---

## 6. 飽和(S)の第一歩 — torsor 分解と LOC-1 の合流

### 6.1 torsor の定義(Sol §9)

$m=0$ 層で、$\alpha\in C_{O_{2'}(H)}(T)\times T=:\mathrm{Pr}(H)$ に対し
$$\mathcal T_\alpha:=\{f\in[P,P]=P:\ \bar y^{\,\alpha}=\bar y^{\,f}\}.$$
非空なら $\mathcal T_\alpha$ は $C_P(\bar y)$ の（右）torsor($f,f'\in\mathcal T_\alpha\Rightarrow f'f^{-1}\in C_P(\bar y)$)。

飽和 (S) は各 $\alpha\in\mathrm{Pr}(H)$ について:
1. **(T1) $\mathcal T_\alpha\ne\varnothing$**(transporter 障害・LOC-1 型)
2. **(T2)** その torsor 内に、hexagon (3.3)(3.4) の両残差を同時に 1 にする $f$ がある

を要する。**$\alpha\in C(T)$ からは (T1) は出ず、(T1) から (T2) は出ない**(Sol の正しい警告)。

### 6.2 (T1) の内実 — いつ自動か

> ### 補題 SAT-T1(transporter 非空の判定)
> $\mathcal T_\alpha\ne\varnothing\iff\bar y^{\,\alpha}\in\bar y^{\,P}$(すなわち $\bar y^\alpha$ が $\bar y$ と $P$-共役)。
> $P=A_n$、$\bar y=(\ell^r,1^t)$ 型で $\alpha\in\mathrm{Pr}(H)\subseteq H=C_{S_n}(\bar x)$。$\bar y^\alpha$ は $\bar y$ と**同じ巡回型**($\alpha$ は置換共役)。ゆえに $S_n$-共役は自動。
> **$A_n$-共役への落差**は $C_{S_n}(\bar y)\not\subseteq A_n$ のとき(型 $(\ell^r,1^t)$ の $A_n$-類が分裂しないとき)消える。$\ell$ 奇・$t$ の値により $C_{S_n}(\bar y)=C_\ell\wr S_r\times S_t$ は $S_n$ に奇置換をもつ($S_r$ の互換・$S_t$ の互換)ので**類は分裂せず (T1) は自動**。

**機械傍証**: 9 窓すべてで $\ker\Xi=1$ かつ $\lvert\Xi(\ker)\rvert=\lvert\ker\rvert$(§`norm_embedding`)。これは各 $\alpha\in\Xi(\ker)$ に $\mathcal T_\alpha\ne\varnothing$ かつ torsor 内にちょうど 1 個の valid $f$ があることと整合(単射 ⟹ torsor あたり高々 1、飽和観測 ⟹ ちょうど 1)。

> **したがって (T1) は本族で片づく見込み**(補題 SAT-T1・要 Sol 監査)。**残る本丸は (T2)。**

### 6.3 (T2) の障害を class として定義する(Sol の助言に沿う)

Sol の助言「$\alpha$ から直接 $f$ を書くより、hexagon residual が torsor の平行移動でどう変わるかを obstruction class として定義する方が安全」を実装する第一歩:

$f_0\in\mathcal T_\alpha$ を一つ固定。任意の $f=f_0c$($c\in C_P(\bar y)$)に対し hexagon 残差を
$$R_1(c):=\bigl(\sigma_1 f^{-1}\sigma_2 f\bigr)\bigl(f^{-1}\sigma_1\sigma_2\bar x^{0}\bigr)^{-1}\in P,\qquad
R_2(c):=\bigl(f^{-1}\sigma_2 f\sigma_1\bigr)\bigl(\sigma_2\sigma_1 f\bigr)^{-1}\in P$$
($m=0$・$c^{\pm}$ 項なし)と定める。(T2) $\iff\exists c:\ R_1(c)=R_2(c)=1$。

> ### 鍵補題 SAT-L1(**証明すべき命題・未証明**)
> 写像 $c\mapsto\bigl(R_1(c),R_2(c)\bigr)$ は $C_P(\bar y)$ から $P\times P$ への**アフィン写像**(ある準同型 $\rho:C_P(\bar y)\to P\times P$ と定数の合成)であり、その像が対角 $\{(1,1)\}$ を通る。
> **これが立てば** (T2) の解集合 $\{c:R=1\}$ は $\ker\rho$ の coset(または空)= **obstruction は $\mathrm{coker}\,\rho$ の 1 元**として定義でき、飽和は「その障害が消える」ことに帰着する。

### 6.4 LOC-1 との合流点

$\alpha\in C_{O_{2'}(H)}(T)\times T$ の $T$-成分が非自明なとき、$\alpha$ は $S=\mathrm{Syl}_2(K)$ を中心化する方向にある。LOC-1(`ideas_010` I10-3 / I11-A の補題候補)は「$S$-中心化 shadow の作用素 $T_{(m,f)}$ が $S$ 上恒等」を主張する。**SAT-L1 の $\rho$ が $S$-方向で退化する**(= $c$ の $S$-成分が $R$ に効かない)ことが LOC-1 の内実であり、両者は同じ線型構造を別の切り口で見ている。

> ### 統合の主張(§6 の到達点・candidate)
> 飽和 (S) は次の 2 補題に還元される:
> - **SAT-T1**(transporter 非空・§6.2・本族で片づく見込み)
> - **SAT-L1**(residual のアフィン性 + 対角到達・§6.3・**未証明の本丸**)
>
> SAT-L1 の $\rho$ の core が「$C_{O_{2'}(H)}(T)$ の像」とちょうど一致することが示せれば、飽和と定理 PRUNE-FIX が噛み合い、$\lvert\Xi(\ker)\rvert_{\rm odd}=\ell^{s_2(r)}$ が定理になる。**これが次の委嘱の型**(数学者 or Sol へ SAT-L1 単体で)。

### 6.5 詰まりの構造(v1 §4.4 の更新)

v1 §4.4 は「$\subseteq$ は群論・$\supseteq$ は算術で、『何が生き残るか』を出す定理が一本もない」とした。**SOL87-FIX でこの図式が半分動いた**:
- $C_{O_{2'}(H)}(T)$ の**大きさ**($\ell^{s_2(r)}$)は定理になった(群論側の勝ち)。
- しかし「その各元が shadow を**もつ**」(SAT-L1)は依然として算術側で、**GT 公理(hexagon residual)を使う初の『生き残り』定理**になるはず。$R_\tau$(死ぬ側)の双対を初めて書く場所。

---

## 7. 格付け表(本稿の全主張)

| 主張 | 格 |
|---|---|
| 定理 PRUNE-FIX(§4.1・= SOL87-FIX) | **定理**(紙 = Sol・機械 = 本稿 $r{=}1..8$ = **cross-checked**)|
| 証明 1・証明 2 の correctness(§2) | **検証 PASS**(穴なし・暗黙前提 3 点は真) |
| $r=1..8$ の $\lvert C\rvert=\ell^{s_2(r)}$(§3) | **GAP 単系統 measured**(定理 PRUNE-FIX の機械側) |
| $r=4$ が既測 $C_{B_x}(D_8)$ と一致(§3) | **calibrated** |
| PRUNE 飽和 (S)(§5・§6) | **未証明(candidate)** |
| $\Xi$ 単射 (I)(§5) | **未証明**(9 窓 measured・補題 NORM-E で核層へ還元) |
| 補題 SAT-T1(§6.2) | **candidate**(要 Sol 監査・本族で片づく見込み) |
| 鍵補題 SAT-L1(§6.3) | **未証明・次委嘱の本丸** |
| $\lvert\ker\widetilde\chi\rvert_{\rm odd}=\ell^{s_2(r)}(核側の律) | **(S)(I) 依存 = 未証明**。定理 PRUNE-FIX 単体では出ない |

## 8. 検算

| スクリプト | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/sol87_fix.g` | `70a103f3058cd43b2ee8930048bd8aeba11aa89a902cafe885720d2d9e52b992` | SOL87-FIX の $r=1..8$ 機械確認・tail $C_3$ 消滅($r{=}2,t{=}3$) |
| `search/probe/wac_v1/prune_ident2.g`(既出) | (v1) | $r=2,3$ の $\Xi$-像同定(飽和の実測側) |
| `search/probe/wac_v1/r4_window.g`(既出) | (r4 予言) | $r=4$ の $C_{B_x}(D_8)=\langle\bar x\rangle$(§3 の照合相手) |
| (Python) | — | 証明 1 の Legendre 恒等式 $\sum(2^{a_i}{-}1)=r{-}s_2(r)=v_2(r!)$ を $r=1..16$ で独立確認 |

**登録宇宙の掃引結果ではない。台帳請求権は発生していない。**
