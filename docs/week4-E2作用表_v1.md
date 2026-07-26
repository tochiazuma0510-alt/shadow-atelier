# Week 4 — 掃引 ① r2 用 **$A=\gamma_2/\gamma_6$ 上の作用表** v1(定義と導出のみ)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 導出委嘱**(並列インスタンス・狭スコープ)。

**本稿の射程**: $P^{(5)}=F_2/\gamma_6$、$A=\gamma_2/\gamma_6$ 上の **Hall 積表・$\theta$/$\sigma_m$ の全基底作用・$E_m$ の明示式・section の欠損項 $d_\theta,d_\sigma,\varepsilon_m$** を書き下すこと。**可解性の議論は一切しない**(可解/不可解・$\mathcal L$ の空非空・$-\omega_0\in F(K)$ の判定は本稿の対象外)。

依存(正本): `docs/week4-掃引宇宙_v3.md` §1.3(基底と section の正本)・`docs/命題_E22三段判定_v1.md`(記号と定義)・`search/manifest_spec_e2_actions.md` / `..._actions2.md`(既存記載との整合先)・`sol/sol2_reply_01_q.md`(cocycle 式 (1)–(4))・`docs/notes/検証_q式導出.md`(修理の型)。

**検算スクリプト**(共有ツリー・監査対象): **`docs/scout/hall5.mjs`**(node・BigInt 整数演算のみ・外部依存なし)。本稿の全表を独立に再計算し、**46 項目の自己検査を全通過(FAILS = 0)**。

> **本稿が閉じるもの**: 【GAP-E22a】(「$\mathcal Q(\bar k)$ の閉形 = Hall collection 係数の明示式」)。§6.2 の補題 6.3 がその閉形である。
> **本稿が閉じないもの**: $C$ 層のデータ($d_\theta,d_\sigma,\varepsilon_m$ と重み 5 の交換子補正)には**第二系統がない**。route G(GAP・PC presentation)がこれを独立に再現するまで札は `candidate`(単系統)。

---

## 0. 要旨(実装者が最初に読む 8 行)

| # | 内容 | 場所 |
|---|---|---|
| **A1** | $A$ は class 2、$C=[A,A]=\langle t_5,t_6\rangle$。**非自明な交換子は $[w,p]=t_5$、$[w,q]=t_6$ の 2 本だけ**。積は $H(a)H(b)=H\bigl(a+b-(a_pb_w)t_5-(a_qb_w)t_6\bigr)$ | §2 |
| **A2** | **$P$ の中では $[q,x]=r_2t_5t_6$**($\ne r_2$)。既存正本 v2 §1.0 の「Jacobi: $[q,x]=r_2$」は **class 4 での話**であり、class 5 では重み 5 の補正が付く。同様に $[r_2,x]=t_2t_5$、$[r_3,x]=t_3t_6$ | §2.1 |
| **A3** | $\theta(p)=q^{-1}t_6^{-1}$、$\theta(q)=p^{-1}t_5^{-1}$、$\theta(r_2)=r_2^{-1}t_5^{-1}t_6^{-1}$、$\theta(t_2)=t_3^{-1}t_6^{-1}$、$\theta(t_3)=t_2^{-1}t_5^{-1}$。他は符号反転のみ | §3 |
| **A4** | $\sigma_m$ の全 12 基底像。$m$ 依存は $\binom m1,\binom m2,\binom m3$ のみ。**$\sigma$ の $C$ 成分($d_\sigma$)は $m$ に依らない** | §4 |
| **A5** | $\bar E_m$ の $S^aT^b$ 係数 $=(-1)^{a+1}\binom{m+1+a}{a+b+2}$。$\varepsilon_m$ は $m$ の 5 次(二項基底で整係数) | §5 |
| **A6** | **$d_\theta$ は線型**(二次項なし)。**$d_\sigma$ は線型 $+\binom{a_w}2(t_5-mt_6)$ の一項だけ**。これが【GAP-E22a】の閉形 | §6 |
| **A7** | 上の全閉形は $A_j$($\bar A$ を $\bmod\,2^j$、$C$ を $\bmod\,2^{j-1}$)で**代表元非依存**。鍵は $\binom{a+2^j}2-\binom a2\equiv0\ (\mathrm{mod}\ 2^{j-1})$ | §7 |
| **A8** | 自己検査: $\mathcal N_C=0$・$\operatorname{im}\Lambda=\langle(t_5+t_6,0)\rangle$・$c_s(w,p)=0$・$c_s(p,w)=-t_5$ を再現、**E19 c=5 ダンプ 10 件と $20\times10$ 行列 $M$ の全成分・$b$ の全成分が一致** | §8 |

---

## 1. 対象・記号・モデル

### 1.1 規約

$F_2=\langle x,y\rangle$ 自由群、$z:=(xy)^{-1}$、$P:=P^{(5)}=F_2/\gamma_6$、$A:=\gamma_2/\gamma_6=\gamma_2(P)$。

$$ [u,v]:=u^{-1}v^{-1}uv,\qquad u^v:=v^{-1}uv,\qquad uv=vu[u,v],\qquad u^v=u[u,v]. $$

使う恒等式:
$$ [uv,z]=[u,z]^v\,[v,z],\qquad [u,vz]=[u,z]\,[u,v]^z,\qquad [u^{-1},v]=\bigl([u,v]^{-1}\bigr)^{u^{-1}},\qquad [u^{-1},v^{-1}]=[u,v]^{(uv)^{-1}} . \tag{1.1}$$

**Hall–Witt**(本稿で使う形。$P^{(5)}$ 内で機械検査済 — §8 検査 (16)):
$$ \bigl[[a,b],c^a\bigr]\cdot\bigl[[c,a],b^c\bigr]\cdot\bigl[[b,c],a^b\bigr]=1 . \tag{1.2}$$

### 1.2 Hall 基底(正本 — `週4-掃引宇宙_v3.md` §1.3 と同一・以後変更しない)

$$ w:=[x,y];\quad p:=[w,x],\ q:=[w,y];\quad r_1:=[p,x],\ r_2:=[p,y],\ r_3:=[q,y]; $$
$$ t_1:=[r_1,x],\ t_2:=[r_1,y],\ t_3:=[r_2,y],\ t_4:=[r_3,y];\quad t_5:=[w,p],\ t_6:=[w,q]. $$

重み $2;3,3;4,4,4;5,5,5,5;5,5$、Hirsch length $1+2+3+6=12$。

> **基底であることの確認.** 自由 Lie 環 $L_5$ の階数は $\frac15\sum_{d\mid5}\mu(d)2^{5/d}=6$。標準 Hall 基底($x<y<w<p<q<r_1<r_2<r_3$)の重み 5 の元は $[r_1,x],[r_1,y],[r_2,y],[r_3,y],[p,w],[q,w]$ の 6 個。$t_5=[p,w]^{-1}$、$t_6=[q,w]^{-1}$ ゆえ、登録基底は Hall 基底の符号違いであり基底である。∎

**座標**: $a=(a_w,a_p,a_q,a_{r_1},a_{r_2},a_{r_3},a_{t_1},a_{t_2},a_{t_3},a_{t_4}\mid a_{t_5},a_{t_6})\in\mathbb Z^{12}$ に対し
$$ H(a):=w^{a_w}p^{a_p}q^{a_q}r_1^{a_{r_1}}r_2^{a_{r_2}}r_3^{a_{r_3}}t_1^{a_{t_1}}t_2^{a_{t_2}}t_3^{a_{t_3}}t_4^{a_{t_4}}t_5^{a_{t_5}}t_6^{a_{t_6}} . $$
$\bar a\in\mathbb Z^{10}$ は最初の 10 座標。**canonical section** は $s(\bar a):=H(\bar a\mid 0,0)$(= 昇順 Hall 正規形・v3 §1.3 の正本)。

### 1.3 検算モデル(Magnus 埋め込み)

自由結合環 $R:=\mathbb Z\langle\xi,\eta\rangle/(\deg\ge6)$、$x\mapsto1+\xi$、$y\mapsto1+\eta$。自由群では次元部分群が下中心列に一致する(Magnus)ので、この写像は $F_2/\gamma_6$ 上**単射**であり、$P^{(5)}$ の厳密モデルを与える。`docs/scout/hall5.mjs` はこの $R$(次元 $1+2+4+8+16+32=63$)の上で全計算を BigInt 整数演算で行い、Hall 正規形は「重み昇順に主要項を剥がす」アルゴリズム(有理 Gauss 消去で係数を決定、非整数解・残余 $\ne1$ で例外)で決めている。

---

## 2. Hall 積表(委嘱項目 1)

### 2.1 $P$ 内の交換子表(基底元 × 生成元)

| | $[\,\cdot\,,x]$ | $[\,\cdot\,,y]$ |
|---|---|---|
| $w$ | $p$ | $q$ |
| $p$ | $r_1$ | $r_2$ |
| $q$ | $\boxed{r_2\,t_5\,t_6}$ | $r_3$ |
| $r_1$ | $t_1$ | $t_2$ |
| $r_2$ | $\boxed{t_2\,t_5}$ | $t_3$ |
| $r_3$ | $\boxed{t_3\,t_6}$ | $t_4$ |
| $t_1,\dots,t_6$ | $1$ | $1$ |

**導出**(枠の 3 本。他は定義)。(1.2) に $(a,b,c)=(w,y,x)$ を代入する。

- $\bigl[[w,y],x^w\bigr]=[q,\,x[x,w]]=[q,xp^{-1}]=[q,p^{-1}]\,[q,x]^{p^{-1}}=[q,x]$($[q,p]$ は重み 6、$[q,x]\in\gamma_4$ は $\gamma_3$ と可換)。
- $\bigl[[x,w],y^x\bigr]=[p^{-1},\,yw^{-1}]=[p^{-1},w^{-1}]\,[p^{-1},y]^{w^{-1}}$。(1.1) より $[p^{-1},w^{-1}]=[p,w]^{(pw)^{-1}}=[p,w]=t_5^{-1}$(中心)、$[p^{-1},y]=(r_2^{-1})^{p^{-1}}=r_2^{-1}$、$(r_2^{-1})^{w^{-1}}=r_2^{-1}$($[\gamma_4,\gamma_2]\subseteq\gamma_6=1$)。ゆえに $=t_5^{-1}r_2^{-1}$。
- $\bigl[[y,x],w^y\bigr]=[w^{-1},wq]=[w^{-1},q]\,[w^{-1},w]^q=[w^{-1},q]=(t_6^{-1})^{w^{-1}}=t_6^{-1}$。

(1.2) より $[q,x]\cdot t_5^{-1}r_2^{-1}\cdot t_6^{-1}=1$、すなわち $\boxed{[q,x]=r_2t_5t_6}$。∎

同様に $(a,b,c)=(p,y,x)$:
$\bigl[[p,y],x^p\bigr]=[r_2,xr_1^{-1}]=[r_2,x]$、$\bigl[[x,p],y^x\bigr]=[r_1^{-1},yw^{-1}]=[r_1^{-1},w^{-1}][r_1^{-1},y]^{w^{-1}}=1\cdot t_2^{-1}$、$\bigl[[y,x],p^y\bigr]=[w^{-1},pr_2]=[w^{-1},r_2][w^{-1},p]^{r_2}=t_5^{-1}$。
ゆえに $\boxed{[r_2,x]=t_2t_5}$。

$(a,b,c)=(q,y,x)$:
$\bigl[[q,y],x^q\bigr]=[r_3,x]$、$\bigl[[x,q],y^x\bigr]=[(r_2t_5t_6)^{-1},yw^{-1}]=[r_2^{-1},y]^{w^{-1}}=t_3^{-1}$、$\bigl[[y,x],q^y\bigr]=[w^{-1},qr_3]=[w^{-1},q]=t_6^{-1}$。
ゆえに $\boxed{[r_3,x]=t_3t_6}$。∎

> **★ 既存正本への注意(実装者へ).** `docs/week4-E2作戦_v2.md` §1.0 は「**Jacobi**: $[q,x]=r_2$」と書いている。これは **class 4($F_2/\gamma_5$)での話**であり正しい。**class 5 では $[q,x]=r_2t_5t_6$** であって、$t_5,t_6$ の補正が付く。同じ理由で $\bar A$(= $C$ で割った層)の上では $[q,x]=r_2$ が成り立つ。**$C$ 座標を落とすかどうかで答えが変わる箇所**なので、実装は必ず本表を使うこと。

### 2.2 $A$ 内の交換子表(全 $12\times12$ 対)

$$ \boxed{\ [w,p]=t_5,\qquad [w,q]=t_6,\qquad \text{他の全ての基底元の対は可換}\ } $$
($[p,w]=t_5^{-1}$、$[q,w]=t_6^{-1}$ は上の逆。)

**理由**: $[\gamma_2,\gamma_4]\subseteq\gamma_6=1$、$[\gamma_3,\gamma_3]\subseteq\gamma_6=1$。ゆえに残るのは $[\gamma_2/\gamma_3,\gamma_3/\gamma_4]$ 由来の $[w,p],[w,q]$ のみ。したがって
$$ A\ \text{は class }2,\qquad C:=[A,A]=\langle t_5,t_6\rangle\cong\mathbb Z^2\subseteq\gamma_5=Z(P),\qquad \bar A:=A/C\cong\mathbb Z^{10}. $$

交換子対($\bar u,\bar v\in\bar A$):
$$ \beta(\bar u,\bar v)=[\,H(\bar u),H(\bar v)\,]=(u_wv_p-u_pv_w)\,t_5+(u_wv_q-u_qv_w)\,t_6 . \tag{2.1}$$
(= `manifest_spec_e2_actions2.md` §2 の明示形。再現。)

### 2.3 collection 公式(**積表の本体**)

> **命題 2.1(積・冪・逆元).** 任意の $a,b\in\mathbb Z^{12}$、$n\in\mathbb Z$ に対し
> $$ \boxed{\ H(a)\,H(b)=H\bigl(a+b-(a_pb_w)\,e_{t_5}-(a_qb_w)\,e_{t_6}\bigr)\ } \tag{2.2}$$
> $$ \boxed{\ H(a)^n=H\Bigl(na-\tbinom n2\bigl[(a_pa_w)e_{t_5}+(a_qa_w)e_{t_6}\bigr]\Bigr)\ } \tag{2.3}$$
> $$ H(a)^{-1}=H\bigl(-a-(a_pa_w)e_{t_5}-(a_qa_w)e_{t_6}\bigr). \tag{2.4}$$

**証明.** (2.2): $R_a:=r_1^{a_{r_1}}\cdots t_6^{a_{t_6}}$ は $A$ の中心に入る(重み $\ge4$ の元は $\gamma_2$ と可換)。ゆえに
$$ H(a)H(b)=w^{a_w}p^{a_p}q^{a_q}\cdot w^{b_w}p^{b_p}q^{b_q}\cdot R_aR_b . $$
$w^{b_w}$ を左へ送る: $q^{a_q}w^{b_w}=w^{b_w}q^{a_q}[q,w]^{a_qb_w}=w^{b_w}q^{a_q}t_6^{-a_qb_w}$、$p^{a_p}w^{b_w}=w^{b_w}p^{a_p}t_5^{-a_pb_w}$($t_5,t_6$ は中心)。$[p,q]=1$ ゆえ $p^{a_p}q^{a_q}p^{b_p}q^{b_q}=p^{a_p+b_p}q^{a_q+b_q}$。以上を束ねて (2.2)。
(2.3): $\delta_a:=(a_pa_w)e_{t_5}+(a_qa_w)e_{t_6}$ と置き $G(n):=H\bigl(na-\binom n2\delta_a\bigr)$ とする。(2.2) より、任意の $n\in\mathbb Z$ で
$$ G(n)H(a)=H\Bigl(na-\tbinom n2\delta_a+a-\bigl((na)_pa_w\bigr)e_{t_5}-\bigl((na)_qa_w\bigr)e_{t_6}\Bigr)=H\Bigl((n+1)a-\bigl[\tbinom n2+n\bigr]\delta_a\Bigr)=G(n+1). $$
$G(0)=1$ ゆえ、$n$ の増加方向・減少方向の両方の帰納法で $G(n)=H(a)^n$($\forall n\in\mathbb Z$)。(2.4) は $n=-1$($\binom{-1}2=1$)。∎

**検算**: `hall5.mjs` §2 — 座標をランダムに振った 200 対で (2.2)、60 例で (2.3) を Magnus モデル上の実際の積と照合、全一致。

### 2.4 section cocycle

$c_s(\bar u,\bar v):=s(\bar u)s(\bar v)s(\bar u+\bar v)^{-1}$。(2.2) から直ちに
$$ \boxed{\ c_s(\bar u,\bar v)=-(u_pv_w)\,t_5-(u_qv_w)\,t_6\ } \tag{2.5}$$

- $c_s(w,p)=0$、$c_s(p,w)=-t_5$ (**委嘱の自己検査項目**・§8 で再掲)。
- $c_s(\bar u,\bar v)-c_s(\bar v,\bar u)=(u_wv_p-u_pv_w)t_5+(u_wv_q-u_qv_w)t_6=\beta(\bar u,\bar v)$ — (2.1) と整合(`命題_E22三段判定_v1.md` (1.1))。
- **$\beta$ だけでは $c_s$ は決まらない**(反対称部しか決めない)。(2.5) は昇順 Hall section という**登録された規約**から出る。`sol2_reply_01_q.md` §1 の (1) と一致。

> **★ 記法の橋渡し.** 以後 $\kappa(\bar u,\bar v):=(u_pv_w)t_5+(u_qv_w)t_6=-c_s(\bar u,\bar v)$ と書く(符号を追いやすくするため)。$\delta(\bar u):=\kappa(\bar u,\bar u)=(u_pu_w)t_5+(u_qu_w)t_6$。

---

## 3. $\theta$ の full-$A$ 作用表(委嘱項目 2a)

$\theta\in\operatorname{Aut}(F_2)$、$x\leftrightarrow y$。$\gamma_i$ を保つので $A$ に降りる。

### 3.1 導出(全 12 元・手計算)

$\theta(w)=[y,x]=w^{-1}$(自由群で厳密)。

$\theta(p)=[\theta w,\theta x]=[w^{-1},y]\overset{(1.1)}{=}\bigl([w,y]^{-1}\bigr)^{w^{-1}}=(q^{-1})^{w^{-1}}=q^{-1}[q^{-1},w^{-1}]=q^{-1}\,[q,w]=q^{-1}t_6^{-1}$
(中心値なので $[q^{-1},w^{-1}]=[q,w]$)。同様に
$\theta(q)=[w^{-1},x]=(p^{-1})^{w^{-1}}=p^{-1}[p,w]=p^{-1}t_5^{-1}$。

$\gamma_5$ は中心なので $\theta(p)=q^{-1}t_6^{-1}$ の $t_6$ は以下の交換子計算に効かない:
- $\theta(r_1)=[\theta p,\theta x]=[q^{-1},y]=(r_3^{-1})^{q^{-1}}=r_3^{-1}$($[\gamma_4,\gamma_3]\subseteq\gamma_7=1$)。
- $\theta(r_2)=[\theta p,\theta y]=[q^{-1},x]=\bigl([q,x]^{-1}\bigr)^{q^{-1}}=(r_2t_5t_6)^{-1}=r_2^{-1}t_5^{-1}t_6^{-1}$ ← **§2.1 の $[q,x]=r_2t_5t_6$ がここで効く**。
- $\theta(r_3)=[\theta q,\theta y]=[p^{-1},x]=(r_1^{-1})^{p^{-1}}=r_1^{-1}$。
- $\theta(t_1)=[\theta r_1,\theta x]=[r_3^{-1},y]=(t_4^{-1})^{r_3^{-1}}=t_4^{-1}$。
- $\theta(t_2)=[\theta r_1,\theta y]=[r_3^{-1},x]=\bigl([r_3,x]^{-1}\bigr)^{r_3^{-1}}=(t_3t_6)^{-1}=t_3^{-1}t_6^{-1}$。
- $\theta(t_3)=[\theta r_2,\theta y]=[r_2^{-1},x]=(t_2t_5)^{-1}=t_2^{-1}t_5^{-1}$。
- $\theta(t_4)=[\theta r_3,\theta y]=[r_1^{-1},x]=t_1^{-1}$。
- $\theta(t_5)=[\theta w,\theta p]=[w^{-1},q^{-1}]=[w,q]=t_6$、$\theta(t_6)=[w^{-1},p^{-1}]=[w,p]=t_5$。

### 3.2 表(Hall 座標・順序 $w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4\mid t_5,t_6$)

| $g$ | $\theta(g)$(乗法形) | Hall 座標 |
|---|---|---|
| $w$ | $w^{-1}$ | $[-1,0,0,0,0,0,0,0,0,0\mid0,0]$ |
| $p$ | $q^{-1}t_6^{-1}$ | $[0,0,-1,0,0,0,0,0,0,0\mid0,-1]$ |
| $q$ | $p^{-1}t_5^{-1}$ | $[0,-1,0,0,0,0,0,0,0,0\mid-1,0]$ |
| $r_1$ | $r_3^{-1}$ | $[0,0,0,0,0,-1,0,0,0,0\mid0,0]$ |
| $r_2$ | $r_2^{-1}t_5^{-1}t_6^{-1}$ | $[0,0,0,0,-1,0,0,0,0,0\mid-1,-1]$ |
| $r_3$ | $r_1^{-1}$ | $[0,0,0,-1,0,0,0,0,0,0\mid0,0]$ |
| $t_1$ | $t_4^{-1}$ | $[0,\dots,0,-1\mid0,0]$ |
| $t_2$ | $t_3^{-1}t_6^{-1}$ | $[0,\dots,-1,0\mid0,-1]$ |
| $t_3$ | $t_2^{-1}t_5^{-1}$ | $[0,\dots,-1,0,0\mid-1,0]$ |
| $t_4$ | $t_1^{-1}$ | $[0,\dots,-1,0,0,0\mid0,0]$ |
| $t_5$ | $t_6$ | $[0,\dots,0\mid0,1]$ |
| $t_6$ | $t_5$ | $[0,\dots,0\mid1,0]$ |

**$\bar A$ 上の $\bar\theta$**: $\bar\theta=-\varsigma$、$\varsigma$ は基底の対合
$$ \varsigma:(w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4)\mapsto(w,q,p,r_3,r_2,r_1,t_4,t_3,t_2,t_1). $$
成分で書くと $(\bar\theta \bar f)_w=-f_w$、$(\bar\theta\bar f)_p=-f_q$、$(\bar\theta\bar f)_q=-f_p$、$(\bar\theta\bar f)_{r_1}=-f_{r_3}$、$\dots$ 。
$\theta\vert_C=\begin{pmatrix}0&1\\1&0\end{pmatrix}$(基底 $(t_5,t_6)$)— `manifest_spec_e2_actions.md` と一致。

**検算**: `hall5.mjs` §3(表そのもの)・§12($\theta^2=\mathrm{id}$ を Hall 座標上の合成で確認)。$\bar\theta$ の $10\times10$ 行列は E19 c=5 ダンプの $(1+\bar\theta)$ ブロック(行 1–10)と**全成分一致**(10 個の $m$ で・§8)。

---

## 4. $\sigma_m$ の full-$A$ 作用表(委嘱項目 2b)

$\tau\in\operatorname{Aut}(F_2)$: $x\mapsto y\mapsto z\mapsto x$($z=(xy)^{-1}$)。$\iota_g(h):=h^g=g^{-1}hg$。
$$ \sigma_m:=\iota_{Y^m}\circ\tau,\qquad \sigma_m(g)=y^{-m}\,\tau(g)\,y^{m}. $$

### 4.1 collection 公式($\mathrm{Ad}(y^m)$ の展開)

> **補題 4.1.** $h\in A=\gamma_2$ に対し(左から順に)
> $$ \boxed{\ h^{y^m}=h\cdot[h,y]^{\binom m1}\cdot\bigl[[h,y],y\bigr]^{\binom m2}\cdot\bigl[[[h,y],y],y\bigr]^{\binom m3}\ }\qquad(m\in\mathbb Z). \tag{4.1}$$
> 同形が $x$ でも成立する。

**証明.** $c_0:=h$、$c_{k+1}:=[c_k,y]$ と置く。$h\in\gamma_2$ より $c_k\in\gamma_{2+k}$、特に $c_4\in\gamma_6=1$。**鍵となる可換性**: $[c_1,c_2]\in[\gamma_3,\gamma_4]\subseteq\gamma_7=1$、$[c_2,c_3]\in[\gamma_4,\gamma_5]=1$、$[c_1,c_3]=1$。すなわち $c_1,c_2,c_3$ は**互いに可換**($c_0$ とは可換でなくてよい)。

$m$ についての帰納法。$h^{y^m}=c_0c_1^{a}c_2^{b}c_3^{c}$($a=\binom m1,b=\binom m2,c=\binom m3$)を仮定し、両辺を $y$ で共役する。$c_k^y=c_k[c_k,y]=c_kc_{k+1}$ なので
$$ (c_0c_1^ac_2^bc_3^c)^y=(c_0c_1)(c_1c_2)^a(c_2c_3)^bc_3^c = c_0\,c_1^{a+1}c_2^{a+b}c_3^{b+c} $$
($(c_1c_2)^a=c_1^ac_2^a$、$(c_2c_3)^b=c_2^bc_3^b$ は上の可換性から。並べ替えは一切生じない)。Pascal $\binom{m+1}k=\binom mk+\binom m{k-1}$ より右辺は $m+1$ の場合の主張。$m=0$ は自明。負の $m$ については、両辺とも $f(m+1)=f(m)^y$ という同じ漸化式を満たし $f(0)=h$ で一致し、Pascal は全ての $m\in\mathbb Z$ で成立するので、$\mathbb Z$ 全体で一致する。∎

**検算**: `hall5.mjs` §19($m\in\{0,1,2,3,5,8,13,-4\}$ × ランダム $h$ 20 例、および $x$ 版)。

### 4.2 導出例(2 本を手計算・残りは同一手順)

**$\tau(w)$**: $\tau(w)=[y,z]=[y,y^{-1}x^{-1}]\overset{(1.1)}{=}[y,x^{-1}]\cdot[y,y^{-1}]^{x^{-1}}=[y,x^{-1}]$。
$[y,x^{-1}]=([y,x]^{-1})^{x^{-1}}=w^{x^{-1}}=w[w,x^{-1}]$、$[w,x^{-1}]=(p^{-1})^{x^{-1}}=p^{-1}[p^{-1},x^{-1}]=p^{-1}\cdot r_1t_1^{-1}$
(∵ $[p^{-1},x^{-1}]=[p,x]^{(px)^{-1}}=r_1[r_1,x^{-1}p^{-1}]=r_1t_1^{-1}$)。ゆえに
$$ \boxed{\ \tau(w)=w\,p^{-1}r_1t_1^{-1}\ }\quad\text{(Hall 座標 }[1,-1,0,1,0,0,-1,0,0,0\mid0,0]\text{)}. $$

$h:=\tau(w)$ に (4.1) を適用する:
$[h,y]=[w,y][p^{-1},y][r_1,y]=q\,r_2^{-1}t_2$、$\ [h,y,y]=[q,y][r_2^{-1},y]=r_3t_3^{-1}$、$\ [h,y,y,y]=t_4$。
これらの積を Hall 順に並べ替えるときの $c_s$ 補正は $\kappa$ の第一引数の $p,q$ 座標 × 第二引数の $w$ 座標だが、第 2 因子以降の $w$ 座標は $0$ なのですべて消える。よって

$$ \boxed{\ \sigma_m(w)=w-p+m\,q+r_1-m\,r_2+\tbinom m2 r_3-t_1+m\,t_2-\tbinom m2 t_3+\tbinom m3 t_4\ } $$

(以後、$C$ 成分が $0$ の像は加法的に書く。class-4 部分 $w-p+mq+r_1-mr_2+\binom m2r_3$ は既存正本 `E2作戦_v2` §1.0 と一致 ✓。)

**$\tau(p)$**: $\tau(p)=[\tau w,\tau x]=[\tau(w),y]=q\,r_2^{-1}t_2$。(4.1) より
$$ \sigma_m(p)=q-r_2+t_2+m(r_3-t_3)+\tbinom m2t_4=q-r_2+m\,r_3+t_2-m\,t_3+\tbinom m2 t_4 . $$
class-4 部分 $q-r_2+mr_3$ は既存正本と一致 ✓。

残る $\tau(q),\tau(r_i),\tau(t_j)$ も同じ手順($\tau(q)=[\tau(w),z]$ など)で得られる。**全表は Magnus モデルで計算し、$m=0..12$ の値から $m$ の多項式に補間、$m\in\{13,20,33,-1,-5,-12\}$ で外挿検査に通した**(`hall5.mjs` §4)。

### 4.3 表($\sigma_m$ の全 12 基底像)

$$
\begin{aligned}
\sigma(w)&=w-p+m\,q+r_1-m\,r_2+\tbinom m2 r_3\;-\;t_1+m\,t_2-\tbinom m2 t_3+\tbinom m3 t_4\\[2pt]
\sigma(p)&=q-r_2+m\,r_3\;+\;t_2-m\,t_3+\tbinom m2 t_4\\[2pt]
\sigma(q)&=-p-q+2r_1+(2-m)r_2+(1-m)r_3\;-\;3t_1+(2m-3)t_2+\bigl(2m-2-\tbinom m2\bigr)t_3+\bigl(m-1-\tbinom m2\bigr)t_4\;\boxed{-\,t_5}\\[2pt]
\sigma(r_1)&=r_3\;-\;t_3+m\,t_4\\[2pt]
\sigma(r_2)&=-r_2-r_3\;+\;2t_2+(2-m)t_3+(1-m)t_4\;\boxed{+\,t_5}\\[2pt]
\sigma(r_3)&=r_1+2r_2+r_3\;-\;3t_1+(m-6)t_2+(2m-5)t_3+(m-2)t_4\;\boxed{-\,3t_5-t_6}\\[2pt]
\sigma(t_1)&=t_4\\
\sigma(t_2)&=-t_3-t_4\;\boxed{-\,t_6}\\
\sigma(t_3)&=t_2+2t_3+t_4\;\boxed{+\,t_5+t_6}\\
\sigma(t_4)&=-t_1-3t_2-3t_3-t_4\;\boxed{-\,2t_5-t_6}\\[2pt]
\sigma(t_5)&=t_6,\qquad \sigma(t_6)=-t_5-t_6 .
\end{aligned}
$$

> **★ 観測 4.2($m$ 依存の局在).** 枠で囲った $C$ 成分($=d_\sigma(e_k)$)は **$m$ に依らない**。$m$ が現れるのは $\bar A$ 成分だけであり、しかも $\binom m1,\binom m2,\binom m3$ の整係数結合に限る($\sigma$ は $\gamma_5$ を 3 段しか上げられないため — (4.1))。この事実は §6 の $d_\sigma$ 閉形を著しく単純にする。

**構造の確認**:
- $\sigma\vert_{\gamma_4}$ の class-4 部分($r_1\mapsto r_3$、$r_2\mapsto-r_2-r_3$、$r_3\mapsto r_1+2r_2+r_3$)は既存正本と一致 ✓。**ただし class 5 では重み 5 の補正が付き、$m$ に依存する**($\sigma\vert_{\gamma_4}=\tau\vert_{\gamma_4}$ は class 4 限定の主張)。
- $\sigma\vert_C=\begin{pmatrix}0&-1\\1&-1\end{pmatrix}$、$\theta\vert_C=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ — `manifest_spec_e2_actions.md` と一致 ✓。
- **$\sigma^3=\mathrm{Inn}_A(E_m)$**($f\mapsto E_m^{-1}fE_m$)を全 12 基底・$m\in\{0,1,2,3,5,7\}$ で確認 ✓(`hall5.mjs` §12)。
- **命題 E1**: $\theta\sigma\theta=\iota_{X^u}\sigma^{-1}$、$u=2m+1$ を全 12 基底・同じ $m$ で確認 ✓。

---

## 5. $E_m$ の明示式(委嘱項目 3)

$$ E_m:=\tau^2(y^m)\,\tau(y^m)\,y^m=x^m z^m y^m\in A\qquad(z=(xy)^{-1}). $$

$\sigma(E_m)=y^{-m}(y^mx^mz^m)y^m=x^mz^my^m=E_m$ を $P^{(5)}$ の中で厳密に確認済($m=0..10$)。

### 5.1 $\bar A$ 成分(**閉形**)

`metab.mjs` の $c=5$ 辞書 $w=1,\ p=S,\ q=T,\ r_1=S^2,\ r_2=ST,\ r_3=T^2,\ t_1=S^3,\ t_2=S^2T,\ t_3=ST^2,\ t_4=T^3$ の下で

$$ \boxed{\ \bar E_m=\sum_{a+b\le3}(-1)^{a+1}\binom{m+1+a}{a+b+2}\,S^aT^b\ } \tag{5.1}$$

成分に開くと(Hall 順):

| 座標 | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $\bar E_m$ | $-\binom{m+1}2$ | $\binom{m+2}3$ | $-\binom{m+1}3$ | $-\binom{m+3}4$ | $\binom{m+2}4$ | $-\binom{m+1}4$ | $\binom{m+4}5$ | $-\binom{m+3}5$ | $\binom{m+2}5$ | $-\binom{m+1}5$ |

> **整合**: 最初の 6 成分は `E2作戦_v3` §6.2(a) が class-4 の閉形として登録している
> $\bigl(-\binom{m+1}2,\binom{m+2}3,-\binom{m+1}3,-\binom{m+3}4,\binom{m+2}4,-\binom{m+1}4\bigr)$ と**完全一致**。(5.1) はその weight-5 への自然な延長である。
> **$w$ 成分**: $-\binom{m+1}2=-T_m$ — class $\le2$ の $E_m=w^{-T_m}$(系 E16-a)と整合 ✓。

### 5.2 $C$ 成分 $\varepsilon_m$(**閉形**)

$$ \boxed{\ \varepsilon_m:=E_m\,s(\bar E_m)^{-1}=\Bigl[\tbinom m1+7\tbinom m2+17\tbinom m3+17\tbinom m4+6\tbinom m5\Bigr]t_5-\Bigl[\tbinom m2+4\tbinom m3+6\tbinom m4+3\tbinom m5\Bigr]t_6\ } \tag{5.2}$$

因数分解形(整合確認用):
$$ (\varepsilon_m)_{t_5}=\frac{m(m+1)(m+2)(6m^2+7m+7)}{120},\qquad (\varepsilon_m)_{t_6}=-\frac{(m-1)m(m+1)(3m^2+8)}{120}. $$

### 5.3 数値表($E_m$ の 12 座標)

| $m$ | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ | $t_5$ | $t_6$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | $-1$ | 1 | 0 | $-1$ | 0 | 0 | 1 | 0 | 0 | 0 | **1** | **0** |
| 2 | $-3$ | 4 | $-1$ | $-5$ | 1 | 0 | 6 | $-1$ | 0 | 0 | **9** | **$-1$** |
| 3 | $-6$ | 10 | $-4$ | $-15$ | 5 | $-1$ | 21 | $-6$ | 1 | 0 | **41** | **$-7$** |
| 4 | $-10$ | 20 | $-10$ | $-35$ | 15 | $-5$ | 56 | $-21$ | 6 | $-1$ | **131** | **$-28$** |
| 5 | $-15$ | 35 | $-20$ | $-70$ | 35 | $-15$ | 126 | $-56$ | 21 | $-6$ | **336** | **$-83$** |
| 6 | $-21$ | 56 | $-35$ | $-126$ | 70 | $-35$ | 252 | $-126$ | 56 | $-21$ | **742** | **$-203$** |

### 5.4 E19 ダンプとの整合(**委嘱の指定**)

`certificates/e19/gap_system_c5_m{m}.txt` の `b=` 行の後半 10 成分は $-\bar E_m$ である。$m\in\{0,1,2,3,5,7,11,17,23,63\}$ の **10 件すべてで全成分一致**。例:

| $m$ | dump の $b$ 後半 = $-\bar E_m$ |
|---|---|
| 1 | $[1,-1,0,1,0,0,-1,0,0,0]$ |
| 3 | $[6,-10,4,15,-5,1,-21,6,-1,0]$ |
| 63 | $[2016,-43680,41664,720720,-677040,635376,-9657648,8936928,-8259888,7624512]$ |

さらに、同ダンプの $20\times10$ 行列 $M$(上 10 行 $=1+\bar\theta$、下 10 行 $=\bar{\mathcal N}=1+\bar\sigma+\bar\sigma^2$)の**全 200 成分**を、本稿の $\bar\theta,\bar\sigma$ から独立に再計算して照合 — **10 個の $m$ すべてで全成分一致**(`hall5.mjs` §13)。$\kappa_m=\bar{\mathcal N}(w)$ は `E2作戦_v2` §1.3 の閉形とも一致($m=1$: $[3,-3,0,4,1,1\mid-5,-2,-2,-1]$、前半 6 成分が閉形 $3w-(m+2)p+(m-1)q+\frac{m^2+3m+4}2r_1+r_2+\frac{m^2-m+2}2r_3$)。

---

## 6. Section と欠損項(委嘱項目 4)

### 6.1 定義

$$ s(\bar a)=w^{a_w}p^{a_p}q^{a_q}r_1^{a_{r_1}}r_2^{a_{r_2}}r_3^{a_{r_3}}t_1^{a_{t_1}}t_2^{a_{t_2}}t_3^{a_{t_3}}t_4^{a_{t_4}}\qquad(\text{昇順・v3 §1.3 の正本}) $$
($A_j$ では $0\le a_i<2^j$。$A$ では $a_i\in\mathbb Z$。)

$\varphi\in\{\theta,\sigma_m\}$ に対し
$$ d_\varphi(\bar a):=\varphi\bigl(s(\bar a)\bigr)\,s\bigl(\bar\varphi\bar a\bigr)^{-1}\in C,\qquad \varepsilon_m:=E_m\,s(\bar E_m)^{-1}\in C $$
($C$ が中心なので $s(\bar\varphi\bar a)^{-1}\varphi(s\bar a)$ と書いても同じ — 委嘱の表記と一致)。

### 6.2 **閉形**(【GAP-E22a】の中身)

> **補題 6.3(collection 閉形).** $\varphi\in\operatorname{Aut}(A)$ が下中心フィルトレーション $\gamma_2\supseteq\gamma_3\supseteq\gamma_4\supseteq\gamma_5$ を保つとする($\theta,\sigma_m$ はどちらも保つ)。$u_k:=\bar\varphi(e_k)\in\bar A$ と置く。このとき $\bar a=\sum_{k}a_ke_k$ に対し
> $$ d_\varphi(\bar a)=\sum_{k=1}^{10}a_k\,d_\varphi(e_k)\;-\;\sum_{k=1}^{10}\tbinom{a_k}2\,\delta(u_k)\;-\;\sum_{1\le j<k\le10}a_ja_k\,\kappa(u_j,u_k) \tag{6.1}$$
> さらに **$k\ge2$ では $(u_k)_w=0$**($\varphi(\gamma_3)\subseteq\gamma_3$)なので $\delta(u_k)=\kappa(u_j,u_k)=0$($k\ge2$)。$j<k$ は $k\ge2$ を強制するので二重和は**丸ごと消え**、
> $$ \boxed{\ d_\varphi(\bar a)=\sum_{k=1}^{10}a_k\,d_\varphi(e_k)\;-\;\tbinom{a_w}2\,\delta\bigl(\bar\varphi w\bigr)\ },\qquad \delta(\bar u)=(u_pu_w)t_5+(u_qu_w)t_6 . \tag{6.2}$$

**証明.** $\varphi(s\bar a)=\prod_{k=1}^{10}\varphi(g_k)^{a_k}$($g_k$ は基底元、積は Hall 順)。$\varphi(g_k)=H(u_k\mid z_k)$、$z_k:=d_\varphi(e_k)$ と書くと、(2.3) より
$$ \varphi(g_k)^{a_k}=H\Bigl(a_ku_k\ \Big|\ a_kz_k-\tbinom{a_k}2\delta(u_k)\Bigr). $$
(2.2) を反復すると、積の $\bar A$ 成分は $\sum_ka_ku_k=\bar\varphi(\bar a)$、$C$ 成分は各因子の $C$ 成分の和から $\sum_{j<k}\kappa(a_ju_j,a_ku_k)$ を引いたもの($\kappa$ は双線型)。$s(\bar\varphi\bar a)$ の $C$ 成分は $0$ なので、これが $d_\varphi(\bar a)$ そのもの。(6.1) を得る。後半は $\varphi$ がフィルトレーションを保つことから $u_k\in\gamma_3/\!\sim$($k\ge2$)ゆえ $(u_k)_w=0$。∎

**検算**: (6.1) を $\theta$(ランダム 120 例)と $\sigma_m$($m\in\{0,1,2,3,5,7,11,17\}$ × 25 例)で Magnus モデル上の実測と照合、全一致(`hall5.mjs` §7)。

### 6.3 $\theta$ の欠損 — **線型**

$d_\theta(e_k)$ の表(§3.2 の $C$ 成分):

| $e_k$ | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $d_\theta$ | $0$ | $-t_6$ | $-t_5$ | $0$ | $-t_5-t_6$ | $0$ | $0$ | $-t_6$ | $-t_5$ | $0$ |

$\bar\theta w=-w$ ゆえ $\delta(\bar\theta w)=((-w)_p(-w)_w,\ (-w)_q(-w)_w)=(0,0)$。したがって (6.2) の二次項は消え、

$$ \boxed{\ d_\theta(\bar a)=-\bigl(a_q+a_{r_2}+a_{t_3}\bigr)\,t_5\;-\;\bigl(a_p+a_{r_2}+a_{t_2}\bigr)\,t_6\ }\qquad(\textbf{線型・}m\textbf{ 非依存}) \tag{6.3}$$

**検算**: ランダム 300 例で実測と一致(`hall5.mjs` §11)。

### 6.4 $\sigma_m$ の欠損 — **線型 + 一つの $\binom{a_w}2$ 項**

$d_\sigma(e_k)$ の表(§4.3 の枠内・**$m$ 非依存**):

| $e_k$ | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $d_\sigma$ | $0$ | $0$ | $-t_5$ | $0$ | $+t_5$ | $-3t_5-t_6$ | $0$ | $-t_6$ | $t_5+t_6$ | $-2t_5-t_6$ |

$\bar\sigma w=w-p+mq+\cdots$ ゆえ $(\bar\sigma w)_w=1,\ (\bar\sigma w)_p=-1,\ (\bar\sigma w)_q=m$、したがって $\delta(\bar\sigma w)=-t_5+m\,t_6$。(6.2) より

$$ \boxed{\ d_\sigma(\bar a)=\Bigl[-a_q+a_{r_2}-3a_{r_3}+a_{t_3}-2a_{t_4}+\tbinom{a_w}2\Bigr]t_5\;+\;\Bigl[-a_{r_3}-a_{t_2}+a_{t_3}-a_{t_4}-m\tbinom{a_w}2\Bigr]t_6\ } \tag{6.4}$$

**検算**: $m\in\{0,1,2,3,5,7,11,17,63\}$ × ランダム 40 例で実測と一致(`hall5.mjs` §11)。

$\sigma^2$ の欠損は(`sol2_reply_01_q.md` (4) と同形)
$$ d_{\sigma^2}(\bar a)=d_\sigma(\bar\sigma\bar a)+\sigma\vert_C\bigl(d_\sigma(\bar a)\bigr),\qquad \sigma\vert_C(z_5,z_6)=(-z_6,\ z_5-z_6). \tag{6.5}$$

### 6.5 $q_\theta$ と $q_N$ の明示式

`sol2_reply_01_q.md` (2)(3) の形に (2.5)(6.3)(6.4)(6.5)(5.2) を代入する。**$\bar f\in\mathcal L$ を仮定する**($\mathcal L$ の中身は本稿の対象外 — 判定はしない)。

**第一座標.** $c_s(\bar\theta\bar f,\bar f)=-\bigl((\bar\theta\bar f)_pf_w\bigr)t_5-\bigl((\bar\theta\bar f)_qf_w\bigr)t_6=(f_qf_w)t_5+(f_pf_w)t_6$($(\bar\theta\bar f)_p=-f_q$、$(\bar\theta\bar f)_q=-f_p$)。よって

$$ \boxed{\ q_\theta(\bar f)=\bigl(f_wf_q-f_q-f_{r_2}-f_{t_3}\bigr)\,t_5\;+\;\bigl(f_wf_p-f_p-f_{r_2}-f_{t_2}\bigr)\,t_6\ } \tag{6.6}$$

**検算**: ランダム 200 例で、$\theta(s\bar f)\,s\bar f$ の Hall 正規形の $C$ 座標が (6.6) と一致(`hall5.mjs` §17)。

> **★ 現行実装(`search/e2-sweep-r2.g` 188–215)との差.** 誤った $c_s^{\rm code}(a,b)=(a_wb_p,a_wb_q)$ を使うと $q_\theta=-f_wf_p\,t_5-f_wf_q\,t_6$ となる。真の値 (6.6) との差は
> $$ \bigl(f_wf_q+f_wf_p-f_q-f_{r_2}-f_{t_3}\bigr)t_5+\bigl(f_wf_p+f_wf_q-f_p-f_{r_2}-f_{t_2}\bigr)t_6\ \ne\ 0 $$
> であり、$t_5$/$t_6$ の**両成分とも**ずれる。`docs/notes/検証_q式導出.md` §1・§3 P-1 の指摘と整合する。

**第二座標.** $S:=\bar\sigma$、$\bar e:=\bar E_m$ と書く。一般の $\bar f$ に対し
$$ q_N(\bar f)=\varepsilon_m+d_{\sigma^2}(\bar f)+d_\sigma(\bar f)+c_s\bigl(\bar e,S^2\bar f\bigr)+c_s\bigl(\bar e+S^2\bar f,\ S\bar f\bigr)+c_s\bigl(\bar e+S^2\bar f+S\bar f,\ \bar f\bigr). \tag{6.7}$$
**検算**: $E_m\sigma^2(s\bar f)\sigma(s\bar f)s\bar f$ を Magnus モデルで直接計算し、(6.7) と $m\in\{0,1,2,3,5,7\}$ × ランダム 25 例で一致($\bar A$ 成分・$C$ 成分とも)(`hall5.mjs` §8)。

$\bar f\in\mathcal L$(すなわち $\bar e+S^2\bar f+S\bar f+\bar f=0$)のときは代入により
$$ q_N(\bar f)=\varepsilon_m+d_{\sigma^2}(\bar f)+d_\sigma(\bar f)-\kappa\bigl(\bar e,S^2\bar f\bigr)+\kappa\bigl(\bar f+S\bar f,\ S\bar f\bigr)+\kappa\bigl(\bar f,\bar f\bigr) \tag{6.8}$$
と簡約できる($\kappa(\bar u,\bar v)=(u_pv_w)t_5+(u_qv_w)t_6$、$\kappa(\bar f,\bar f)=\delta(\bar f)=(f_pf_w)t_5+(f_qf_w)t_6$)。

> **注意(実装)**: (6.8) は $\mathcal L$ 上でのみ有効な簡約である。$\mathcal L$ の元かどうかを実装側が保証できないなら **(6.7) を使うこと**。(6.7) は任意の $\bar f$ で正しい(その場合 $\bar A$ 成分は $\bar e+\bar{\mathcal N}\bar f$ で、$C$ 座標は正規形の座標としての意味しかもたない)。

---

## 7. 有限商 $A_j=A/\mho_j(A)$ での読み方

> **補題 7.1(代表元非依存).** §2–§6 の全ての閉形((2.2)–(2.5)・(5.1)(5.2)・(6.1)–(6.8))は、
> **$\bar A$ 座標を $\bmod\,2^j$、$C$ 座標を $\bmod\,2^{j-1}$** で読むと、$\bar A$ 座標の代表元の取り方に依らない。

**証明.** 閉形に現れる非線型項は二種類しかない。
(i) **双線型項** $a_pb_w$ 型($c_s,\kappa,\beta$、および (6.1) の二重和): $a_p\mapsto a_p+2^j$ で値は $2^jb_w$ だけ変わり、$2^{j-1}$ を法として $0$。
(ii) **$\binom{a}2$ 型**((2.3) の冪補正、(6.2)(6.4) の $\binom{a_w}2$): 
$$ \binom{a+2^j}2-\binom a2=2^ja+\binom{2^j}2=2^ja+2^{j-1}(2^j-1)\equiv0\pmod{2^{j-1}} . $$
線型項は明らか。∎

> **★ これは `週4-掃引宇宙_v3.md` §1.1 の裏返しである.** v3 §1.1 は同じ計算を使って「$C$ を $\bmod\,2^j$ で読むと代表元依存になる」($2^{j-1}(2^j-1)\not\equiv0\bmod2^j$)ことを示し、素朴な有限化を否定した。**補題 7.1 は同じ計算の肯定側**であり、$\mho_j$ 有限化($\bar A_j=(\mathbb Z/2^j)^{10}$、$C_j=(\mathbb Z/2^{j-1})^2$)の下で本稿の表がそのまま使えることを保証する。
> **検算**: $j=1..6$ × $m\in\{0,1,5,13,63\}$ × ランダム 30 例で (2.5)(6.3)(6.4) の代表元非依存性を確認、また対照として「$C$ を $\bmod\,2^j$ で読むと $\binom a2$ 項が代表元依存になる」ことも確認(`hall5.mjs` §15)。

**実装への注意 3 点**
1. $m$ は $0..63$ の**リテラル整数**として扱う(表の $\binom m2,\binom m3$ や (5.1)(5.2) の $\binom mk$ を先に整数で評価してから還元する)。$m$ を先に $\bmod\,2^j$ に落としてはならない。
2. $d_\sigma$ の $\binom{a_w}2$ 項では、$a_w$ は section の代表元 $0\le a_w<2^j$ を使う。補題 7.1 によりどの代表元でも $C_j$ 値は同じだが、**$\binom{a_w}2$ を整数で計算してから $\bmod\,2^{j-1}$** に落とすこと($\binom{\cdot}2$ を $\mathbb Z/2^{j-1}$ の中で「$a(a-1)/2$」として計算すると 2 で割れない)。
3. $j=1$ では $C_1=0$ なので $d_\theta,d_\sigma,\varepsilon_m,c_s$ は全て $0$ に潰れる(v3 の可換 control と整合)。

---

## 8. 自己検査節(委嘱項目 5)

`docs/scout/hall5.mjs` を `node docs/scout/hall5.mjs` で実行。**46 項目・FAILS = 0**。指定された項目は以下。

| # | 検査 | 結果 |
|---|---|---|
| **S1** | $\mathcal N_C=1+\sigma+\sigma^2=0$ on $C$($m\in\{0,1,2,3,7,13\}$ で $\sigma\vert_C$ を実測して確認) | **PASS** |
| **S2** | $\operatorname{im}\Lambda=\langle(t_5+t_6,\,0)\rangle$($\Lambda(t_5)=\Lambda(t_6)=(t_5+t_6,0)$) | **PASS** |
| **S3** | $c_s(w,p)=0$ | **PASS** |
| **S4** | $c_s(p,w)=-t_5$ | **PASS** |
| **S5** | E19 c=5 ダンプ **10 件**($m=0,1,2,3,5,7,11,17,23,63$)の `b` 後半 $=-\bar E_m$ 全成分一致 | **PASS** |
| **S6** | 同ダンプの $20\times10$ 行列 $M$($(1+\bar\theta)$ ブロックと $\bar{\mathcal N}$ ブロック)**全 200 成分**を 10 個の $m$ で照合 | **PASS** |
| **S7** | $\kappa_m=\bar{\mathcal N}(w)$ が `E2作戦_v2` §1.3 の閉形と一致($m=0,1,3,7$) | **PASS** |

**その他の主要検査**(全て PASS)

| 検査 | 内容 |
|---|---|
| モデル健全性 | 12 基底元の Hall 座標が単位ベクトルになる |
| 積・冪公式 (2.2)(2.3) | ランダム 200 対 / 60 例 |
| Hall–Witt (1.2) | $P^{(5)}$ 内でランダム 40 組 |
| $[q,x]=r_2t_5t_6$、$[r_2,x]=t_2t_5$、$[r_3,x]=t_3t_6$ | 手計算(§2.1)と実測が一致 |
| $\theta^2=\mathrm{id}$ on $A$ | Hall 座標上の合成 |
| $\sigma$ 表の $m$ 多項式 | $m=0..12$ で補間 → $m\in\{13,20,33,-1,-5,-12\}$ で外挿一致 |
| $\sigma(E_m)=E_m$ | $P^{(5)}$ 内で厳密($m=0..10$) |
| $\sigma^3=\mathrm{Inn}_A(E_m)$ | 全 12 基底・$m\in\{0,1,2,3,5,7\}$ |
| 命題 E1 $\theta\sigma\theta=\iota_{X^u}\sigma^{-1}$($u=2m+1$) | 全 12 基底・同上 |
| (5.1)(5.2) の閉形 | $m\in\{0,\dots,5,9,17,31,63,-3,-8\}$ |
| (6.1)(6.2)(6.3)(6.4) | ランダム 120/300/40×9 例 |
| (2)(3)(4)(= (6.6)(6.7)(6.5)) | 群積からの直接計算と一致 |
| (4.1) の collection 公式 | $m\in\{0,1,2,3,5,8,13,-4\}$、$x$ 版も |
| 補題 7.1 の代表元非依存 | $j=1..6$ × $m$ 5 種 × 30 例 |

> **★ 発射条件について(`検証_q式導出.md` §4 の門).** 同ノートは「checker が**群の積から** $\theta(f)f$ と $E_m\sigma^2(f)\sigma(f)f$ を再計算する」ことを発射条件とした。本稿の検査 §8(2)(3)(4) 行は**まさにそれ**を Magnus モデルの群積で行ったものである。ただし**これは単系統**(node・一つのモデル)であり、v3 §4 が要求する route G(GAP の PC presentation 上の群演算)はまだ存在しない。**二系統一致(cross-checked)には至っていない。**

---

## 9. 状態札・【GAP】・引き継ぎ

### 9.1 状態札

| 対象 | 札 |
|---|---|
| §2 の積表・交換子表・(2.2)–(2.5) | **紙上証明**(手計算)+ Magnus モデル検算。**単系統** |
| §2.1 の $[q,x]=r_2t_5t_6$ 等 | **紙上証明**(Hall–Witt)+ 機械検算一致。**単系統** |
| §3 の $\theta$ 表 | **紙上証明**(全 12 元を手計算)+ 機械検算一致。$\bar\theta$ 部分は **E19/GAP と cross-checked** |
| §4 の $\sigma_m$ 表 | **導出ルート紙上**(4.1)+2 元を手計算、**全表は Magnus モデル計算(単系統)**。$\bar{\mathcal N}=1+\bar\sigma+\bar\sigma^2$ は **E19/GAP と cross-checked**(全 200 成分 × 10 個の $m$)。$\bar\sigma$ 自身の第二系統は**ない** |
| §5.1 $\bar E_m$ の閉形 (5.1) | **単系統の計算 + E19/GAP と cross-checked**(10 件・全成分)。閉形そのもの(全 $m$)は **candidate** |
| §5.2 $\varepsilon_m$ の閉形 (5.2) | **単系統**(第二系統なし)。$m\in\{0..5,9,17,31,63,-3,-8\}$ で検証 |
| §6 補題 6.3・(6.3)(6.4)(6.6)(6.7) | **紙上証明**(補題 6.3)+ Magnus モデル検算。**単系統** |
| §7 補題 7.1 | **紙上証明**(2 行)+ 機械検算 |
| verified(Lean) | **一つもない** |

**「cross-checked」と言えるもの**: $\bar\theta$、$\bar{\mathcal N}$、$\bar E_m$(いずれも $\bar A$ 層のみ・E19 の GAP 系統と本稿の Magnus 系統の二系統一致)。
**「candidate(単系統)」に留まるもの**: $C$ 層の一切($d_\theta,d_\sigma,\varepsilon_m$、$\sigma$ の $t_5,t_6$ 成分、§2.1 の重み 5 補正、$c_s$)。**これは本稿の最大の未閉鎖点である。**

### 9.2 【GAP】

| # | 内容 | 状態 |
|---|---|---|
| **【GAP-E22a】** | $\mathcal Q(\bar k)$ の閉形(Hall collection 係数の明示式) | **本稿で閉鎖**(補題 6.3・式 (6.2)(6.3)(6.4))。ただし札は単系統 |
| **【GAP-E22a′】(新設)** | $C$ 層のデータ($d_\theta,d_\sigma,\varepsilon_m$、$[q,x]$ 等の重み 5 補正)の**第二系統**。route G(GAP の $A_j$ PC presentation 上の群演算)が本稿の表を独立に再現するか | **UNKNOWN**。掃引 ① r2 の発射前に必須 |
| **【GAP-E22e】(新設)** | (5.1) の二項閉形と (5.2) の $\varepsilon_m$ 閉形の**証明**(現状は多点検証)。Fox 微分 $\partial E_m/\partial x=\sum_{k<m}s^k-\sum_{k=1}^{m}s^{m-k}t^{-k}$($s=1+S,\ t=1+T$)からの導出が有望 | **UNKNOWN**(有限・実行可能) |

### 9.3 実装への引き継ぎ(route N / route G 共通の最小仕様)

1. **$\bar A_j$ 側**: $\bar\theta$($\S3.2$ の $10\times10$)、$\bar\sigma_m$($\S4.3$ の $\bar A$ 部・$10\times10$・$m$ 多項式)、$\bar E_m$((5.1))。**これは E19 ダンプで二系統照合できる** — 実装は最初にこの照合を通すこと。
2. **$C_j$ 側**: $\theta\vert_C,\sigma\vert_C$(§4.3 末)、$c_s$((2.5))、$d_\theta$((6.3))、$d_\sigma$((6.4))、$d_{\sigma^2}$((6.5))、$\varepsilon_m$((5.2))。**照合先がないので route G が独立に構成すること**(二次表・$\mathrm{Ob}_j$ の座標系・section の実装コードを共有しない — v3 §4)。
3. **$q_\theta,q_N$**: (6.6)(6.7)。**(6.8) は $\mathcal L$ 上限定の簡約なので、$\mathcal L$ 所属を保証できないときは使わない。**
4. **還元規約**: $\bar A$ を $\bmod\,2^j$、$C$ を $\bmod\,2^{j-1}$(補題 7.1)。$\binom{a_w}2$ と $\binom mk$ は**整数で評価してから**還元する。
5. **禁止**: 「$\bar A$ 上で成り立つ式を $A$ でも使う」($[q,x]=r_2$ 型の誤り・§2.1 の ★)。「$c_s$ を $\beta$ から一意に決める」(§2.4)。

---

## 付録 A. 検算スクリプトの構成

`docs/scout/hall5.mjs`(node・BigInt・外部依存なし・約 330 行)

| 節 | 内容 |
|---|---|
| 0 | モデル健全性(12 基底の Hall 座標) |
| 1 | $P$ 内交換子表 / $A$ 内交換子表(全 $12\times12$) |
| 2 | 積・冪公式、$c_s(w,p)$、$c_s(p,w)$ |
| 3 | $\theta$ の全 12 像・$\theta^2=\mathrm{id}$ |
| 4 | $\sigma_m$ の全 12 像($m$ 補間 + 外挿検査) |
| 5 | $E_m$ の 12 座標・$\sigma(E_m)=E_m$・二項閉形 |
| 6 | $d_\theta,d_\sigma,\varepsilon_m$ の基底値 |
| 7 | 補題 6.3 の (6.1) 検査 |
| 8 | cocycle 式 (6.5)(6.6)(6.7) を群積から検査 |
| 9 | $\mathcal N_C=0$、$\operatorname{im}\Lambda$ |
| 10, 13 | E19 c=5 ダンプ照合($b$ / 行列 $M$ 全成分) |
| 11 | (6.3)(6.4) の明示閉形 |
| 12 | $\sigma^3=\mathrm{Inn}(E_m)$、命題 E1 |
| 14 | $\bar\theta,\bar\sigma$ の行列ダンプ(文書掲載用) |
| 15 | 補題 7.1(代表元非依存)+ 対照 |
| 16 | Hall–Witt (1.2) と §2.1 の 3 本 |
| 17 | (6.6) の明示形 |
| 18 | (5.1)(5.2) の二項閉形 |
| 19 | (4.1) の collection 公式 |

実行結果: `pass` 46 件、`FAIL` 0 件、終了コード 0。
