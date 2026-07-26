# Week 4 — **$A^{(6)}=\gamma_2/\gamma_7$ 上の作用表** v1(定義と導出のみ)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 E2 転進委嘱**(class-6 作用表の独立導出・ブラインド並列)。

**本稿の射程**: $P^{(6)}=F_2/\gamma_7$、$A:=A^{(6)}=\gamma_2/\gamma_7$(class 2・rank 21)上の
**collection 表・$\theta/\sigma_m$ の全基底作用・$E_m$ の明示式・section 欠損 $d_\theta,d_\sigma,\varepsilon_m$** を書き下すこと。
**可解性の議論は一切しない**(可解/不可解・$\mathcal L$ の空非空・$\mathrm{Ob}$ の中の位置の判定は本稿の対象外)。

**検算スクリプト**(共有ツリー・監査対象): **`docs/scout/hall6.mjs`**
(node・BigInt 整数演算のみ・外部依存なし・約 500 行)。**67 項目の自己検査を全通過(FAILS = 0)**。
モデルは class-5 稿とは独立に一から実装した(次数 7 打ち切り Magnus 埋め込み・`hall5.mjs` は参照していない)。

> **本稿が閉じるもの**
> - class-6 の collection 表・$\theta$/$\sigma_m$ 全 21 基底作用・$E_m$・$d_\theta,d_\sigma,\varepsilon_m$ の明示式。
> - **【GAP-E22e】の $\bar E_m$ 側**: (5.1') の二項閉形に **紙上証明**が付いた(§5.4 — Fox 微分 → $\bar E_m=-\sum_{1\le i\le j\le m}s^{-i}t^{m-j}$ → Vandermonde)。class-5 稿で UNKNOWN だった項目。
> - $\bar A$ 層(rank 15)には **第二系統がある**: `certificates/e19/gap_system_c6_m*.txt`(GAP)の $30\times15$ 行列 **4500 成分**と $b$ の **300 成分**が全一致(§8)。
>
> **本稿が閉じないもの**
> - $C$ 層(rank 6)のデータ($d_\theta,d_\sigma,\varepsilon_m$、$\sigma$/$\theta$ の $u$ 成分、重み 6 の交換子補正)には**第二系統がない**。札は `candidate`(単系統)。
> - $\varepsilon_m$ の閉形 (5.2') は多点検証のみ(証明なし)。

---

## 0. 要旨(実装者が最初に読む 10 行)

| # | 内容 | 場所 |
|---|---|---|
| **A1** | $A$ は class 2。$C=[A,A]=\langle t_5,t_6,u_1,u_2,u_3,u_4\rangle\cong\mathbb Z^6$、$\bar A=A/C\cong\mathbb Z^{15}$。**非自明な交換子は 6 本**: $[w,p]=t_5,[w,q]=t_6,[w,r_i]=u_i,[p,q]=u_4$ | §2.2 |
| **A2** | **★ 罠 1**: $[q,x]=r_2t_5t_6\,\boxed{u_2u_4^{-1}}$、$[r_2,x]=t_2t_5\,\boxed{u_1u_2}$、$[r_3,x]=t_3t_6\,\boxed{u_2^2u_3^2u_4^{-1}}$。class-5 の値にさらに重み 6 の補正が乗る | §2.1 |
| **A3** | **★ 罠 2**: class 5 で「$[t_j,\cdot]=1$」だった**行が全部生きる**。$[t_5,x]=u_1$、$[t_5,y]=u_2u_4^{-1}$、$[t_6,x]=u_2u_4$、$[t_6,y]=u_3$、$[t_2,x]=s_2u_1$、$[t_3,x]=s_3u_2^2u_4^{-1}$、$[t_4,x]=s_4u_3^2$ | §2.1 |
| **A4** | **★ 罠 3**: collection 補正 $\kappa$ に **$a_qb_p\to u_4$ の項が増える**。これは「第 2 引数の $w$ 座標」型ではないので、class-5 で「二重和が丸ごと消える」と言えた論法が**壊れる**(3 対だけ生き残る) | §2.3, §6.2 |
| **A5** | **★ 罠 4**: その結果 **$d_\theta$ は線型でなくなる** — $-a_pa_q\,u_4$ という二次項が付く(class 5 では線型だった) | §6.3 |
| **A6** | $\bar A$ 層は**完全な閉形**をもつ: $\bar A$ は $\mathbb Z[s^{\pm1},t^{\pm1}]$ 上 $w$ で自由(自由メタベリアン)。$\bar\theta(\lambda w)=-\lambda(t,s)w$、$\bar\sigma_m(\lambda w)=\lambda(t,s^{-1}t^{-1})\,s^{-1}t^m\,w$、$\bar E_m=-\sum_{1\le i\le j\le m}s^{-i}t^{m-j}\cdot w$。**いずれも紙上証明つき** | §3.3, §4.4, §5.4 |
| **A7** | $\bar E_m$ の成分は $(-1)^{a+1}\binom{m+1+a}{a+b+2}$($a+b\le4$)。class-5 の閉形の自然な延長で、**今回は証明された** | §5.1 |
| **A8** | $\sigma_m$ の $m$ 依存: $\bar A$ 成分は $m$ の 4 次まで、**$C$ 成分は高々 1 次**。**$t_5,t_6$ 成分は $m$ 非依存**(class-5 の観測が生き残る)が、**$u_1,u_2,u_3,u_4$ 成分は $m$ 依存**になる | §4.3 |
| **A9** | $\varepsilon_m$ は $m$ の 6 次(二項基底で整係数)。$t_5,t_6$ 成分は class-5 の (5.2) と完全一致 | §5.2 |
| **A10** | 自己検査: (i) $\theta^2=\mathrm{id}$、(ii) $\sigma_m(E_m)=E_m$・$\sigma_m^3=\mathrm{Inn}(E_m)$、(iii) **weight $\le5$ 制限が class-5 正本と全 2564 セル一致**。さらに E19 の GAP c6 ダンプと $\bar A$ 層で 4800 成分一致 | §8 |

---

## 1. 対象・記号・モデル

### 1.1 規約(class-5 稿 `docs/week4-E2作用表_v1.md` と同一)

$F_2=\langle x,y\rangle$、$z:=(xy)^{-1}$、$P:=P^{(6)}=F_2/\gamma_7$、$A:=\gamma_2/\gamma_7=\gamma_2(P)$。

$$ [u,v]:=u^{-1}v^{-1}uv,\qquad u^v:=v^{-1}uv,\qquad uv=vu[u,v],\qquad u^v=u[u,v]. \tag{1.0}$$

使う恒等式:
$$ [uv,z]=[u,z]^v\,[v,z],\qquad [u,vz]=[u,z]\,[u,v]^z,\qquad [u^{-1},v]=\bigl([u,v]^{-1}\bigr)^{u^{-1}},\qquad [u,v^{-1}]=\bigl([u,v]^{-1}\bigr)^{v^{-1}} . \tag{1.1}$$

**Hall 恒等式**(class-5 稿 (1.2) と同形。$P^{(6)}$ 内で機械検査済 — §8 検査 9):
$$ \bigl[[a,b],c^a\bigr]\cdot\bigl[[c,a],b^c\bigr]\cdot\bigl[[b,c],a^b\bigr]=1 . \tag{1.2}$$

**Jacobi**(Lie 環 $L=\bigoplus_{k\le6}\gamma_k/\gamma_{k+1}$ 内。以下 $[[a,b],c]=[[a,c],b]+[a,[b,c]]$ の形で使う):
$$ [[a,b],c]+[[b,c],a]+[[c,a],b]=0 . \tag{1.3}$$

### 1.2 Hall 基底(委嘱で事前登録・以後変更しない)

$$ w:=[x,y];\quad p:=[w,x],\ q:=[w,y];\quad r_1:=[p,x],\ r_2:=[p,y],\ r_3:=[q,y]; $$
$$ t_1:=[r_1,x],\ t_2:=[r_1,y],\ t_3:=[r_2,y],\ t_4:=[r_3,y];\quad t_5:=[w,p],\ t_6:=[w,q]; $$
$$ s_1:=[t_1,x],\ s_2:=[t_1,y],\ s_3:=[t_2,y],\ s_4:=[t_3,y],\ s_5:=[t_4,y];\quad u_1:=[w,r_1],\ u_2:=[w,r_2],\ u_3:=[w,r_3],\ u_4:=[p,q]. $$

重み $2;3,3;4,4,4;5,5,5,5,5,5;6\times9$。$\mathbb Z$-階数 $1+2+3+6+9=21$、Hirsch length $21$。

> **基底であることの確認.** 自由 Lie 環の階数は $\dim L_6=\frac16\sum_{d\mid6}\mu(d)2^{6/d}=\frac16(64-8-4+2)=9$。
> 順序 $x<y<w<p<q<r_1<r_2<r_3<t_1<\dots<t_4<[p,w]<[q,w]$ に対する標準 Hall 基底の重み 6 の元は、
> Hall の条件「$[c_i,c_j]$、$c_i=[c_s,c_t]\Rightarrow t\le j$」により
> $[t_1,x],[t_1,y],[t_2,y],[t_3,y],[t_4,y]$(重み $5\times1$)、$[r_1,w],[r_2,w],[r_3,w]$(重み $4\times2$)、$[q,p]$(重み $3\times3$)の 9 個。
> $[t_2,x],[t_3,x],[t_4,x]$ と $[[p,w],x]$ 等は $t\le j$ を破るので基本でない。
> 登録基底 $u_1,u_2,u_3,u_4$ はそれぞれ $[r_1,w],[r_2,w],[r_3,w],[q,p]$ の**符号違い**、$t_5,t_6$ は $[p,w],[q,w]$ の符号違い。ゆえに基底である。∎
> **機械確認**: §8 検査 2–4(21 基底の Hall 座標が単位ベクトル・往復一意性)。

**座標**: $a\in\mathbb Z^{21}$ に対し、**昇順**の積
$$ H(a):=w^{a_w}p^{a_p}q^{a_q}r_1^{a_{r_1}}r_2^{a_{r_2}}r_3^{a_{r_3}}t_1^{a_{t_1}}t_2^{a_{t_2}}t_3^{a_{t_3}}t_4^{a_{t_4}}t_5^{a_{t_5}}t_6^{a_{t_6}}s_1^{a_{s_1}}\cdots s_5^{a_{s_5}}u_1^{a_{u_1}}\cdots u_4^{a_{u_4}}. $$
$C$ の 6 元は $A$ の中心にあるので、$C$ 生成元をどこに置いても $H(a)$ は同じ(順序の曖昧さはない)。

**canonical section**(v3 §1.3 の規約の class-6 版):
$$ s(\bar a):=w^{a_w}p^{a_p}q^{a_q}r_1^{a_{r_1}}r_2^{a_{r_2}}r_3^{a_{r_3}}t_1^{a_{t_1}}t_2^{a_{t_2}}t_3^{a_{t_3}}t_4^{a_{t_4}}s_1^{a_{s_1}}s_2^{a_{s_2}}s_3^{a_{s_3}}s_4^{a_{s_4}}s_5^{a_{s_5}} = H(\bar a\mid 0). $$
$\bar A$ の 15 座標の並びは $(w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4,s_1,s_2,s_3,s_4,s_5)$、$C$ の 6 座標は $(t_5,t_6,u_1,u_2,u_3,u_4)$。

> **class-5 への射影**: $P^{(6)}\twoheadrightarrow P^{(5)}$ は $g_i\mapsto g_i$($i\le t_6$)、$s_k,u_i\mapsto1$。座標では **先頭 12 成分を取るだけ**で、class-5 稿の並び $(w,p,q,r_1,r_2,r_3,t_1,\dots,t_4,t_5,t_6)$ と一致する。§8 の全セル照合はこの射影で行う。

### 1.3 検算モデル(Magnus 埋め込み)

$R:=\mathbb Z\langle\xi,\eta\rangle/(\deg\ge7)$、$x\mapsto1+\xi$、$y\mapsto1+\eta$。自由群では次元部分群が下中心列に一致する(Magnus/Witt)ので、この写像は $F_2/\gamma_7$ 上**単射**であり $P^{(6)}$ の厳密モデルを与える。`hall6.mjs` はこの $R$(次元 $\sum_{k=0}^{6}2^k=127$)の上で全計算を BigInt で行う。

Hall 正規形は**重み昇順に剥がす**アルゴリズム: 重み $d=2,\dots,6$ について、残差の次数 $<d$ 部分が消えていること(= 残差が $\gamma_d$ にあること、Magnus)を確認 → 次数 $d$ 部分は $L_d$ の元 → 重み $d$ の基底の主要項で張られる行列に対し BigInt 有理 Gauss 消去で解き、**整数解であること**を要求 → その分を剥がして次へ。単項冪は $(1+N)^n=\sum_{k\le6}\binom nkN^k$($N^7=0$)で $n$ の大きさに依らず 6 回の積で計算する。

---

## 2. Hall 積表(委嘱項目 1)

### 2.1 $P^{(6)}$ 内の交換子表(基底元 × 生成元)— **委嘱の主要因**

| | $[\,\cdot\,,x]$ | $[\,\cdot\,,y]$ |
|---|---|---|
| $w$ | $p$ | $q$ |
| $p$ | $r_1$ | $r_2$ |
| $q$ | $\boxed{r_2\,t_5\,t_6\,u_2\,u_4^{-1}}$ | $r_3$ |
| $r_1$ | $t_1$ | $t_2$ |
| $r_2$ | $\boxed{t_2\,t_5\,u_1\,u_2}$ | $t_3$ |
| $r_3$ | $\boxed{t_3\,t_6\,u_2^{2}\,u_3^{2}\,u_4^{-1}}$ | $t_4$ |
| $t_1$ | $s_1$ | $s_2$ |
| $t_2$ | $\boxed{s_2\,u_1}$ | $s_3$ |
| $t_3$ | $\boxed{s_3\,u_2^{2}\,u_4^{-1}}$ | $s_4$ |
| $t_4$ | $\boxed{s_4\,u_3^{2}}$ | $s_5$ |
| $t_5$ | $\boxed{u_1}$ | $\boxed{u_2\,u_4^{-1}}$ |
| $t_6$ | $\boxed{u_2\,u_4}$ | $\boxed{u_3}$ |
| $s_1..s_5,\ u_1..u_4$ | $1$ | $1$ |

**機械確認**: `hall6.mjs` §1(全 24 エントリ × 21 座標 = **504 セル**が下記の手計算と一致 — 検査 10)。

#### (a) 重み 5 の行($t_1,\dots,t_6$)— **Lie 環内で厳密**

$[\gamma_5,\gamma_1]\subseteq\gamma_6$ かつ $\gamma_7=1$ なので $\gamma_6$ は中心で $\gamma_6\cong L_6$、したがって重み 5 の元と生成元の交換子は $L_6$ の Lie 括弧そのものである。(1.3) を使って:

- $[t_5,x]=[[w,p],x]=[[w,x],p]+[w,[p,x]]=[p,p]+[w,r_1]=u_1$
- $[t_5,y]=[[w,p],y]=[[w,y],p]+[w,[p,y]]=[q,p]+[w,r_2]=-u_4+u_2$
- $[t_6,x]=[[w,q],x]=[[w,x],q]+[w,[q,x]]=[p,q]+[w,r_2]=u_4+u_2$  ($L_4$ では $[q,x]=r_2$)
- $[t_6,y]=[[w,q],y]=[[w,y],q]+[w,[q,y]]=[q,q]+[w,r_3]=u_3$
- $[t_2,x]=[[r_1,y],x]=[[r_1,x],y]+[r_1,[y,x]]=[t_1,y]-[r_1,w]=s_2+u_1$
- $[t_3,x]=[[r_2,y],x]=[[r_2,x],y]+[r_2,[y,x]]=[t_2+t_5,\,y]+u_2=s_3+(u_2-u_4)+u_2=s_3+2u_2-u_4$
- $[t_4,x]=[[r_3,y],x]=[[r_3,x],y]+[r_3,[y,x]]=[t_3+t_6,\,y]+u_3=s_4+u_3+u_3=s_4+2u_3$

(ここで $L_5$ 内の $[r_2,x]=t_2+t_5$、$[r_3,x]=t_3+t_6$ は再び (1.3) から:
$[[p,y],x]=[[p,x],y]+[p,[y,x]]=t_2-[p,w]=t_2+t_5$、$[[q,y],x]=[[q,x],y]+[q,[y,x]]=[r_2,y]-[q,w]=t_3+t_6$。)

#### (b) 重み 3–4 の行 — **群の中で Hall 恒等式 (1.2)**

**$[q,x]$**: (1.2) に $(a,b,c)=(w,y,x)$。

- $\bigl[[w,y],x^w\bigr]=[q,\,x[x,w]]=[q,xp^{-1}]\overset{(1.1)}{=}[q,p^{-1}]\cdot[q,x]^{p^{-1}}$。
 $[q,p]\in\gamma_6$ は中心ゆえ $[q,p^{-1}]=[q,p]^{-1}=[p,q]=u_4$。$[[q,x],p^{-1}]\in[\gamma_4,\gamma_3]\subseteq\gamma_7=1$ ゆえ第 2 因子は $[q,x]$。$\Rightarrow u_4\,[q,x]$。
- $\bigl[[x,w],y^x\bigr]=[p^{-1},\,yw^{-1}]=[p^{-1},w^{-1}]\cdot[p^{-1},y]^{w^{-1}}$。
 $[p,w^{-1}]=([p,w]^{-1})^{w^{-1}}=t_5^{\,w^{-1}}=t_5$($[\gamma_5,\gamma_2]\subseteq\gamma_7=1$)、よって $[p^{-1},w^{-1}]=(t_5^{-1})^{p^{-1}}=t_5^{-1}$。
 $[p^{-1},y]=(r_2^{-1})^{p^{-1}}=r_2^{-1}$、$(r_2^{-1})^{w^{-1}}=r_2^{-1}[r_2^{-1},w^{-1}]=r_2^{-1}[r_2,w]=r_2^{-1}u_2^{-1}$
 (中心交換子では $[g^{-1},h^{-1}]=[g,h]$)。$\Rightarrow t_5^{-1}r_2^{-1}u_2^{-1}$。
- $\bigl[[y,x],w^y\bigr]=[w^{-1},wq]=[w^{-1},q]=(t_6^{-1})^{w^{-1}}=t_6^{-1}$。

(1.2) より $u_4[q,x]\cdot t_5^{-1}r_2^{-1}u_2^{-1}\cdot t_6^{-1}=1$。$[q,x]\in\gamma_4$ は $t_5,t_6,r_2$ と可換($[\gamma_4,\gamma_5]=[\gamma_4,\gamma_4]=1$)なので
$$ \boxed{\ [q,x]=r_2\,t_5\,t_6\,u_2\,u_4^{-1}\ }. $$

**$[r_2,x]$**: $(a,b,c)=(p,y,x)$。

- $\bigl[[p,y],x^p\bigr]=[r_2,\,xr_1^{-1}]=[r_2,r_1^{-1}]\cdot[r_2,x]^{r_1^{-1}}=[r_2,x]$($[\gamma_4,\gamma_4]=1$、$[\gamma_5,\gamma_4]=1$)。
- $\bigl[[x,p],y^x\bigr]=[r_1^{-1},yw^{-1}]=[r_1^{-1},w^{-1}]\cdot[r_1^{-1},y]^{w^{-1}}=[r_1,w]\cdot t_2^{-1}=u_1^{-1}t_2^{-1}$。
- $\bigl[[y,x],p^y\bigr]=[w^{-1},pr_2]=[w^{-1},r_2]\cdot[w^{-1},p]^{r_2}=u_2^{-1}\,t_5^{-1}$。

$\Rightarrow\ \boxed{[r_2,x]=t_2\,t_5\,u_1\,u_2}$。

**$[r_3,x]$**: $(a,b,c)=(q,y,x)$。$g:=[x,q]=[q,x]^{-1}=r_2^{-1}t_5^{-1}t_6^{-1}u_2^{-1}u_4$ と置く。

- $\bigl[[q,y],x^q\bigr]=[r_3,\,xg]=[r_3,g]\cdot[r_3,x]^{g}=[r_3,x]$。
- $\bigl[[x,q],y^x\bigr]=[g,\,yw^{-1}]=[g,w^{-1}]\cdot[g,y]^{w^{-1}}$。
 $[g,w^{-1}]=[r_2^{-1},w^{-1}]=[r_2,w]=u_2^{-1}$($\gamma_5$ 部分は $[\gamma_5,\gamma_2]\subseteq\gamma_7=1$ で効かない)。
 $[g,y]=[r_2^{-1},y]\cdot[t_5^{-1}t_6^{-1}u_2^{-1}u_4,\,y]=t_3^{-1}\cdot[t_5,y]^{-1}[t_6,y]^{-1}=t_3^{-1}\,(u_2u_4^{-1})^{-1}u_3^{-1}=t_3^{-1}u_2^{-1}u_3^{-1}u_4$。
 ($[ab,y]=[a,y]^b[b,y]$ で $a=r_2^{-1}$、$b=t_5^{-1}t_6^{-1}u_2^{-1}u_4\in\gamma_5$。共役 $[a,y]^b$ は $[\gamma_5,\gamma_5]=1$ ゆえ効かない。
 また $v\mapsto[v,y]$ は $\gamma_5\to\gamma_6$ 上の準同型 — $[v_1v_2,y]=[v_1,y]^{v_2}[v_2,y]$ かつ $[\gamma_6,\gamma_5]=1$。)
 $w^{-1}$ 共役は $[\gamma_5,\gamma_2]\subseteq\gamma_7=1$ ゆえ効かない。$\Rightarrow t_3^{-1}u_2^{-2}u_3^{-1}u_4$。
- $\bigl[[y,x],q^y\bigr]=[w^{-1},qr_3]=[w^{-1},r_3]\cdot[w^{-1},q]^{r_3}=u_3^{-1}\,t_6^{-1}$。

$\Rightarrow\ \boxed{[r_3,x]=t_3\,t_6\,u_2^{2}\,u_3^{2}\,u_4^{-1}}$。

> **★ 実装者への注意(罠の総まとめ).**
> 1. class-5 稿 §2.1 は「$[q,x]=r_2t_5t_6$」を正としたが、それは **class 5 での話**。class 6 ではさらに $u_2u_4^{-1}$ が付く。$[r_2,x],[r_3,x]$ も同様。
> 2. class-5 稿では $t_1,\dots,t_6$ の行が**全部 $1$** だった。class 6 では**全部生きる**。特に $[t_5,\cdot],[t_6,\cdot]$($C$ の元と生成元の交換子)が非自明になる — $C$ は $A$ の中心だが **$P$ の中心ではない**。
> 3. $\bar A$ 上で成り立つ式($[q,x]=r_2$、$[r_2,x]=t_2$、…)を $A$ で使ってはならない。

### 2.2 $A$ 内の交換子表(全 $21\times21$ 対)

$$ \boxed{\ [w,p]=t_5,\quad [w,q]=t_6,\quad [w,r_1]=u_1,\quad [w,r_2]=u_2,\quad [w,r_3]=u_3,\quad [p,q]=u_4,\quad\text{他の基底対はすべて可換}\ } $$
(逆向きは $[p,w]=t_5^{-1}$ 等。)

**理由**: 基底対 $(g_i,g_j)$ の重みの和が $\ge7$ なら $\gamma_7=1$。和が $\le6$ の対は
$(2,3)\to t_5,t_6$;$(2,4)\to u_1,u_2,u_3$;$(3,3)\to[p,q]=u_4$($[p,p]=[q,q]=1$)のみ。$(2,2)$ は $[w,w]=1$。ゆえに
$$ A\ \text{は class }2,\qquad C:=[A,A]=\langle t_5,t_6,u_1,u_2,u_3,u_4\rangle\cong\mathbb Z^6\subseteq Z(A),\qquad \bar A:=A/C\cong\mathbb Z^{15}. $$
($t_5,t_6\in\gamma_5$ は $A$ の中心だが $P$ の中心ではない。$u_1,\dots,u_4\in\gamma_6=Z(P^{(6)})$。)

**交換子対**($\bar u,\bar v\in\bar A$):
$$ \beta(\bar u,\bar v)=[H(\bar u),H(\bar v)]
=(u_wv_p-u_pv_w)t_5+(u_wv_q-u_qv_w)t_6+\sum_{i=1}^{3}(u_wv_{r_i}-u_{r_i}v_w)\,u_i+(u_pv_q-u_qv_p)\,u_4 . \tag{2.1'}$$
(class-5 の (2.1) に $u_1,u_2,u_3$ の 3 項と、**$w$ を含まない新項** $u_4$ が加わる。)

### 2.3 collection 公式(**積表の本体**)

$$ \kappa(a,b):=(a_pb_w)e_{t_5}+(a_qb_w)e_{t_6}+(a_{r_1}b_w)e_{u_1}+(a_{r_2}b_w)e_{u_2}+(a_{r_3}b_w)e_{u_3}+\boxed{(a_qb_p)e_{u_4}},\qquad \delta(a):=\kappa(a,a). $$

> **命題 2.1'(積・冪・逆元).** 任意の $a,b\in\mathbb Z^{21}$、$n\in\mathbb Z$ に対し
> $$ \boxed{\ H(a)H(b)=H\bigl(a+b-\kappa(a,b)\bigr)\ } \tag{2.2'}$$
> $$ \boxed{\ H(a)^n=H\Bigl(na-\tbinom n2\delta(a)\Bigr)\ },\qquad H(a)^{-1}=H\bigl(-a-\delta(a)\bigr). \tag{2.3'/2.4'}$$

**証明.** (2.2'): $A$ は class 2 で $[A,A]=C$ は中心。昇順の積 $\prod_ig_i^{a_i}\cdot\prod_jg_j^{b_j}$ をひとつの昇順積に直すには、$j<i$ の各対について $g_i^{a_i}g_j^{b_j}=g_j^{b_j}g_i^{a_i}[g_i,g_j]^{a_ib_j}$ を使う。非自明な $[g_i,g_j]$($i>j$)は §2.2 の 6 本の逆、すなわち
$[p,w]=t_5^{-1},[q,w]=t_6^{-1},[r_i,w]=u_i^{-1},[q,p]=u_4^{-1}$。よって補正は $\prod$ で $-\kappa(a,b)$ ちょうど。
(2.3'): $G(n):=H(na-\binom n2\delta(a))$ とおくと (2.2') より $G(n)H(a)=G(n+1)$($\kappa(na,a)=n\delta(a)$ と $\binom n2+n=\binom{n+1}2$)。$G(0)=1$ から $n$ の両方向の帰納法。(2.4') は $n=-1$($\binom{-1}2=1$)。∎

**機械確認**: 検査 16–18(ランダム 200 対 / 60 例 / 40 例、負の指数を含む)。

### 2.4 section cocycle

$$ \boxed{\ c_s(\bar u,\bar v):=s(\bar u)s(\bar v)s(\bar u+\bar v)^{-1}=-\kappa(\bar u,\bar v)\ } \tag{2.5'}$$

- $c_s(w,p)=0$、$c_s(p,w)=-t_5$(class-5 と同じ)。**新規**: $c_s(q,p)=-u_4$、$c_s(r_2,w)=-u_2$。
- $c_s(\bar u,\bar v)-c_s(\bar v,\bar u)=\beta(\bar u,\bar v)$ — (2.1') と整合(検査 24)。
- **$\beta$ だけでは $c_s$ は決まらない**(反対称部しか決めない)。(2.5') は昇順 Hall section という**登録された規約**から出る。

> **★ 罠 3 の核心.** class 5 では $\kappa(a,b)$ の全項が $b_w$ を含んでいた。class 6 の $u_4$ 項 $a_qb_p$ は **$b_p$ 型**である。$\varphi$ がフィルトレーションを保つとき「$k\ge2$ なら $(\bar\varphi e_k)_w=0$」は使えるが、$(\bar\varphi e_k)_p=0$ は $e_k$ の重みが $\ge4$ のときしか言えない。これが §6.2 で二重和が完全には消えない理由である。

---

## 3. $\theta$ の full 作用表(委嘱項目 2a)

$\theta\in\operatorname{Aut}(F_2)$、$x\leftrightarrow y$。$\gamma_i$ を保つので $A$ に降りる。

### 3.1 導出(全 21 元・手計算)

$\theta(w)=[y,x]=w^{-1}$(自由群で厳密)。$u,v\in A$ に対し $C$ が中心なので $[u^{-1},v^{-1}]=[u,v]$ が使える。

**記法**: 以下 $\theta(g)=[\theta g',\theta g'']$($g=[g',g'']$)の第 2 引数は**代入後**の元を書く($\theta x=y$、$\theta y=x$)。

- $\theta(p)=[w^{-1},y]=(q^{-1})^{w^{-1}}=q^{-1}[q^{-1},w^{-1}]=q^{-1}[q,w]=q^{-1}t_6^{-1}$。同様に $\theta(q)=[w^{-1},x]=p^{-1}t_5^{-1}$。
- $\theta(r_1)=[\theta p,y]=[q^{-1}t_6^{-1},y]=[q^{-1},y]^{t_6^{-1}}[t_6^{-1},y]=r_3^{-1}\cdot u_3^{-1}$。**← $[t_6,y]=u_3$ がここで効く**(class 5 では $0$ だった)。
- $\theta(r_2)=[\theta p,x]=[q^{-1}t_6^{-1},x]=[q,x]^{-1}\cdot[t_6,x]^{-1}=(r_2t_5t_6u_2u_4^{-1})^{-1}(u_2u_4)^{-1}=r_2^{-1}t_5^{-1}t_6^{-1}u_2^{-2}$。
- $\theta(r_3)=[\theta q,x]=[p^{-1}t_5^{-1},x]=[p,x]^{-1}[t_5,x]^{-1}=r_1^{-1}u_1^{-1}$。
- $\theta(t_1)=[\theta r_1,y]=[r_3^{-1}u_3^{-1},y]=[r_3,y]^{-1}=t_4^{-1}$。
- $\theta(t_2)=[\theta r_1,x]=[r_3^{-1}u_3^{-1},x]=[r_3,x]^{-1}=t_3^{-1}t_6^{-1}u_2^{-2}u_3^{-2}u_4$。
- $\theta(t_3)=[\theta r_2,x]=[r_2^{-1}t_5^{-1}t_6^{-1}u_2^{-2},x]=[r_2,x]^{-1}[t_5,x]^{-1}[t_6,x]^{-1}=(t_2t_5u_1u_2)^{-1}u_1^{-1}(u_2u_4)^{-1}=t_2^{-1}t_5^{-1}u_1^{-2}u_2^{-2}u_4^{-1}$。
- $\theta(t_4)=[\theta r_3,x]=[r_1^{-1}u_1^{-1},x]=t_1^{-1}$。
- $\theta(t_5)=[\theta w,\theta p]=[w^{-1},q^{-1}t_6^{-1}]=[w^{-1},q^{-1}]=[w,q]=t_6$。同様に $\theta(t_6)=t_5$。
- $\theta(s_1)=[\theta t_1,y]=[t_4^{-1},y]=[t_4,y]^{-1}=s_5^{-1}$、$\theta(s_5)=[\theta t_4,x]=[t_1^{-1},x]=s_1^{-1}$。
- $\theta(s_2)=[\theta t_1,x]=[t_4,x]^{-1}=(s_4u_3^2)^{-1}=s_4^{-1}u_3^{-2}$。
- $\theta(s_3)=[\theta t_2,x]=[t_3,x]^{-1}[t_6,x]^{-1}=(s_3u_2^2u_4^{-1})^{-1}(u_2u_4)^{-1}=s_3^{-1}u_2^{-3}$。
- $\theta(s_4)=[\theta t_3,x]=[t_2,x]^{-1}[t_5,x]^{-1}=(s_2u_1)^{-1}u_1^{-1}=s_2^{-1}u_1^{-2}$。
- $\theta(u_1)=[\theta w,\theta r_1]=[w^{-1},r_3^{-1}u_3^{-1}]=[w^{-1},r_3^{-1}]=[w,r_3]=u_3$。同様に $\theta(u_2)=[w^{-1},\theta r_2]=[w,r_2]=u_2$、$\theta(u_3)=[w^{-1},\theta r_3]=[w,r_1]=u_1$。
- $\theta(u_4)=[\theta p,\theta q]=[q^{-1}t_6^{-1},p^{-1}t_5^{-1}]=[q^{-1},p^{-1}]=[q,p]=u_4^{-1}$。

### 3.2 表(加法記法・座標順 $w,p,q,r_1,r_2,r_3,t_1..t_4,s_1..s_5\mid t_5,t_6,u_1..u_4$)

$$
\begin{aligned}
\theta(w)&=-w & \theta(t_5)&=t_6 & \theta(s_1)&=-s_5\\
\theta(p)&=-q-t_6 & \theta(t_6)&=t_5 & \theta(s_2)&=-s_4-2u_3\\
\theta(q)&=-p-t_5 & \theta(t_1)&=-t_4 & \theta(s_3)&=-s_3-3u_2\\
\theta(r_1)&=-r_3-u_3 & \theta(t_2)&=-t_3-t_6-2u_2-2u_3+u_4 & \theta(s_4)&=-s_2-2u_1\\
\theta(r_2)&=-r_2-t_5-t_6-2u_2 & \theta(t_3)&=-t_2-t_5-2u_1-2u_2-u_4 & \theta(s_5)&=-s_1\\
\theta(r_3)&=-r_1-u_1 & \theta(t_4)&=-t_1 & &\\
\theta(u_1)&=u_3 & \theta(u_2)&=u_2 & \theta(u_3)&=u_1,\quad\theta(u_4)=-u_4
\end{aligned}
$$

**$C$ 上**(基底 $(t_5,t_6,u_1,u_2,u_3,u_4)$):$\theta\vert_C$ は対合 $t_5\leftrightarrow t_6$、$u_1\leftrightarrow u_3$、$u_2\mapsto u_2$、$u_4\mapsto-u_4$。
$t_5,t_6$ ブロックは class-5 稿 §4.3 末の $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ と一致 ✓。

### 3.3 $\bar A$ 上の $\bar\theta$ — **加群記述(閉形・紙上証明)**

> **命題 3.2'.** $\bar A=\gamma_2/([\gamma_2,\gamma_2]\gamma_7)$ は自由メタベリアン群 $F_2/[\gamma_2,\gamma_2]$ の交換子群の切り詰めであり、
> $\mathbb Z[s^{\pm1},t^{\pm1}]$-加群として $w$ が**自由生成**(階数 1)。ここで $s,t$ は $x,y$ による共役作用($h^x\mapsto s\cdot h$、$h^y\mapsto t\cdot h$)、$S:=s-1$、$T:=t-1$($=[\,\cdot\,,x],[\,\cdot\,,y]$ の作用)。基底の辞書は
> $$ w\leftrightarrow1,\ p\leftrightarrow S,\ q\leftrightarrow T,\ r_1\leftrightarrow S^2,\ r_2\leftrightarrow ST,\ r_3\leftrightarrow T^2,\ t_1\leftrightarrow S^3,\dots,t_4\leftrightarrow T^3,\ s_1\leftrightarrow S^4,\dots,s_5\leftrightarrow T^4, $$
> すなわち $\bar A\cong\mathbb Z[S,T]/(\deg\ge5)$(全次数 $\le4$ の 15 単項式)。このとき
> $$ \boxed{\ \bar\theta(\lambda(s,t)\cdot w)=-\lambda(t,s)\cdot w\ } \tag{3.3'}$$

**証明.** $\theta$ は $F_2/\gamma_2$ 上 $s\leftrightarrow t$ を誘導するので $\bar\theta$ は $s\leftrightarrow t$ 半線型。$\theta(w)=w^{-1}\leftrightarrow-1$。∎

**機械確認**: 検査 64(15 基底で (3.3') と表が一致)。
成分で書けば $\bar\theta=-\varsigma$、$\varsigma$ は $S\leftrightarrow T$ 対称による対合
$$ \varsigma:\ w\mapsto w,\ p\leftrightarrow q,\ r_1\leftrightarrow r_3,\ r_2\mapsto r_2,\ t_1\leftrightarrow t_4,\ t_2\leftrightarrow t_3,\ s_1\leftrightarrow s_5,\ s_2\leftrightarrow s_4,\ s_3\mapsto s_3 . $$
この $15\times15$ 行列は E19 c6 ダンプの $(1+\bar\theta)$ ブロックと **10 個の $m$ で全成分一致**(§8)。

---

## 4. $\sigma_m$ の full 作用表(委嘱項目 2b)

$\tau\in\operatorname{Aut}(F_2)$: $x\mapsto y\mapsto z\mapsto x$($z=(xy)^{-1}$)。$\sigma_m:=\iota_{y^m}\circ\tau$、$\sigma_m(g)=y^{-m}\tau(g)y^m$。

### 4.1 collection 公式

> **補題 4.1'.** $h\in A=\gamma_2$、$g\in\{x,y\}$ に対し(左から順に)
> $$ \boxed{\ h^{g^m}=h\cdot[h,g]^{\binom m1}\cdot[h,g,g]^{\binom m2}\cdot[h,g,g,g]^{\binom m3}\cdot[h,g,g,g,g]^{\binom m4}\ }\qquad(m\in\mathbb Z). \tag{4.1'}$$

**証明.** $c_0:=h$、$c_{k+1}:=[c_k,g]$。$c_k\in\gamma_{2+k}$、$c_5\in\gamma_7=1$。**鍵**: $[c_i,c_j]\in[\gamma_{2+i},\gamma_{2+j}]\subseteq\gamma_{4+i+j}$ で $i,j\ge1$、$i\ne j$ なら $4+i+j\ge7$、$i=j$ なら $0$。したがって $c_1,c_2,c_3,c_4$ は**互いに可換**($c_0$ とは可換でなくてよい)。
帰納法: $(c_0c_1^ac_2^bc_3^cc_4^e)^g=(c_0c_1)(c_1c_2)^a(c_2c_3)^b(c_3c_4)^cc_4^e=c_0c_1^{a+1}c_2^{a+b}c_3^{b+c}c_4^{c+e}$(可換性から並べ替えは生じない)。Pascal より主張。$m=0$ は自明、負の $m$ は $f(m+1)=f(m)^g$、$f(0)=h$ の一意性と Pascal の全 $\mathbb Z$ 成立から。∎

**機械確認**: 検査 28($g=x,y$ × $m\in\{0,1,2,3,5,8,13,-4,-7\}$ × ランダム 8 例)。

**帰結**: $\sigma_m$ の各座標は $\binom m0,\dots,\binom m4$ の整係数結合($m$ の 4 次以下)。実測でも 5 階以上の差分は $0$(検査 29)、外挿検査に通る(検査 30)。

### 4.2 導出の型

$\tau(g_i)=$ `buildBasis`$(\tau x,\tau y)_i=$ 同じ交換子式を $(y,z)$ に適用したもの。例えば
$$ \tau(w)=[y,z]=[y,\,y^{-1}x^{-1}]=[y,x^{-1}]=w^{x^{-1}}=w\,p^{-1}r_1t_1^{-1}s_1\qquad(\text{Hall 正規形}) $$
($[y,x^{-1}]=([y,x]^{-1})^{x^{-1}}=w^{x^{-1}}$、そして $w^{x^{-1}}$ は §4.4 の加群記述で $s^{-1}\cdot w=(1-S+S^2-S^3+S^4)w$)。
これに (4.1') を適用し、(2.2')(2.3') で Hall 正規形に直す。$\bar A$ 成分は §4.4 の閉形で決まり、$C$ 成分は各 $c_k$ の $C$ 座標と $\kappa$ 補正から出る。全表は Magnus モデルで計算し、$m=0..10$ から二項基底に補間、$m\in\{11,13,20,33,64,-1,-5,-12,-30\}$ で外挿検査に通した。

### 4.3 表($\sigma_m$ の全 21 基底像)

$$
\begin{aligned}
\sigma(w)&=w-p+mq+r_1-mr_2+\tbinom m2r_3\;-t_1+mt_2-\tbinom m2t_3+\tbinom m3t_4\;+s_1-ms_2+\tbinom m2s_3-\tbinom m3s_4+\tbinom m4s_5\;\boxed{+\,m\,u_4}\\
\sigma(p)&=q-r_2+mr_3\;+t_2-mt_3+\tbinom m2t_4\;-s_2+ms_3-\tbinom m2s_4+\tbinom m3s_5\;\boxed{+\,u_4}\\
\sigma(q)&=-p-q+2r_1+(2-m)r_2+(1-m)r_3\;-3t_1+(2m-3)t_2+\bigl(2m-2-\tbinom m2\bigr)t_3+\bigl(m-1-\tbinom m2\bigr)t_4\\
&\quad +4s_1+(4-3m)s_2+\bigl(3-3m+2\tbinom m2\bigr)s_3+\bigl(2-2m+2\tbinom m2-\tbinom m3\bigr)s_4+\bigl(1-m+\tbinom m2-\tbinom m3\bigr)s_5\\
&\quad \boxed{-\,t_5+2u_1+(1-m)u_2+(m-3)u_4}\\
\sigma(r_1)&=r_3-t_3+mt_4\;+s_3-ms_4+\tbinom m2s_5\\
\sigma(r_2)&=-r_2-r_3+2t_2+(2-m)t_3+(1-m)t_4\;-3s_2+(2m-3)s_3+\bigl(2m-2-\tbinom m2\bigr)s_4+\bigl(m-1-\tbinom m2\bigr)s_5\\
&\quad \boxed{+\,t_5-2u_1+(m-1)u_2+(2-m)u_4}\\
\sigma(r_3)&=r_1+2r_2+r_3-3t_1+(m-6)t_2+(2m-5)t_3+(m-2)t_4\\
&\quad +6s_1+(12-3m)s_2+\bigl(12-6m+\tbinom m2\bigr)s_3+\bigl(8-5m+2\tbinom m2\bigr)s_4+\bigl(3-2m+\tbinom m2\bigr)s_5\\
&\quad \boxed{-\,3t_5-t_6+9u_1+(9-3m)u_2+(2-m)u_3+(3m-6)u_4}\\
\sigma(t_1)&=t_4-s_4+ms_5\\
\sigma(t_2)&=-t_3-t_4+2s_3+(2-m)s_4+(1-m)s_5\;\boxed{-\,t_6+3u_2-m\,u_3}\\
\sigma(t_3)&=t_2+2t_3+t_4-3s_2+(m-6)s_3+(2m-5)s_4+(m-2)s_5\;\boxed{+\,t_5+t_6-4u_1+(m-7)u_2+(m-2)u_3+(3-m)u_4}\\
\sigma(t_4)&=-t_1-3t_2-3t_3-t_4+4s_1+(12-m)s_2+(15-3m)s_3+(10-3m)s_4+(3-m)s_5\\
&\quad \boxed{-\,2t_5-t_6+12u_1+(17-2m)u_2+(5-m)u_3+(2m-8)u_4}\\
\sigma(t_5)&=t_6-u_2+m\,u_3-u_4,\qquad \sigma(t_6)=-t_5-t_6+2u_1+(2-m)u_2+(1-m)u_3+(1+m)u_4\\
\sigma(s_1)&=s_5,\qquad \sigma(s_2)=-s_4-s_5-2u_3,\qquad \sigma(s_3)=s_3+2s_4+s_5+3u_2+3u_3\\
\sigma(s_4)&=-s_2-3s_3-3s_4-s_5-2u_1-6u_2-3u_3+2u_4,\qquad \sigma(s_5)=s_1+4s_2+6s_3+4s_4+s_5+5u_1+9u_2+3u_3-4u_4\\
\sigma(u_1)&=u_3,\qquad \sigma(u_2)=-u_2-u_3,\qquad \sigma(u_3)=u_1+2u_2+u_3,\qquad \sigma(u_4)=u_4 .
\end{aligned}
$$

> **観測 4.2'($m$ 依存の局在).** 枠の $C$ 成分のうち **$t_5,t_6$ 成分は $m$ に依らない**(class-5 稿の観測 4.2 がそのまま生き残る)。
> 一方 **$u_1,u_2,u_3,u_4$ 成分は $m$ に依存しうる**(class-5 にはなかった現象)。$m$ 依存をもつのは
> $\sigma(w)_{u_4},\sigma(q)_{u_2},\sigma(q)_{u_4},\sigma(r_2)_{u_2},\sigma(r_2)_{u_4},\sigma(r_3)_{u_2},\sigma(r_3)_{u_3},\sigma(r_3)_{u_4},\sigma(t_2)_{u_3},\sigma(t_3)_{u_2},\sigma(t_3)_{u_3},\sigma(t_3)_{u_4},\sigma(t_4)_{u_2},\sigma(t_4)_{u_3},\sigma(t_4)_{u_4},\sigma(t_5)_{u_3},\sigma(t_6)_{u_2},\sigma(t_6)_{u_3},\sigma(t_6)_{u_4}$ の 19 成分。
>
> **観測 4.3'.** $C$ 成分の $m$ 次数は**高々 1**(実測最高次 = 1)。$\bar A$ 成分は 4 次。$C$ は $\theta,\sigma_m$ 不変(検査 32–34)。

### 4.4 $\bar A$ 上の $\bar\sigma_m$ — **加群記述(閉形・紙上証明)**

> **命題 4.4'.** 命題 3.2' の記法で
> $$ \boxed{\ \bar\sigma_m\bigl(\lambda(s,t)\cdot w\bigr)=\lambda\bigl(t,\ s^{-1}t^{-1}\bigr)\cdot s^{-1}t^{m}\cdot w\ } \tag{4.4'}$$
> (全次数 $\le4$ で打ち切る。)

**証明.** (i) 半線型性: $\sigma_m(x)=y^{-m}\tau(x)y^m=y$、$\sigma_m(y)=y^{-m}zy^m$ で $F_2/\gamma_2$ 上の像は $z$ の像 $=s^{-1}t^{-1}$。共役は $F_2/\gamma_2$ 上自明なので、$\sigma_m$ が誘導する $\mathbb Z^2=\langle s,t\rangle$ 上の写像は $s\mapsto t$、$t\mapsto s^{-1}t^{-1}$。$\sigma_m(\lambda\cdot h)=\lambda^{\sigma}\cdot\sigma_m(h)$。
(ii) 生成元の像: $\tau(w)=[y,z]=[y,y^{-1}x^{-1}]\overset{(1.1)}{=}[y,x^{-1}]\cdot[y,y^{-1}]^{x^{-1}}=[y,x^{-1}]=([y,x]^{-1})^{x^{-1}}=w^{x^{-1}}\leftrightarrow s^{-1}\cdot w$。
$\sigma_m(w)=\tau(w)^{y^m}\leftrightarrow t^m s^{-1}w$。∎

**機械確認**: 検査 65(15 基底 × $m\in\{0,1,2,3,5,7,11,-3,-7\}$)。

**構造の確認**
- class-5 制限(先頭 12 成分)は class-5 稿 §4.3 と**全セル一致**(§8・$m$ 10 種 × 12 元 × 12 座標 = 1440 セル)。
- $\sigma\vert_C$ の $t_5,t_6$ ブロックは $\begin{pmatrix}0&-1\\1&-1\end{pmatrix}$ で class-5 稿・`manifest_spec_e2_actions.md` と一致 ✓。ただし **class 6 では $C$ は $t_5,t_6$ ブロックだけで閉じない**($\sigma(t_5)$ が $u$ 成分をもつ)。
- $\bar{\mathcal N}=1+\bar\sigma+\bar\sigma^2$ は E19 c6 ダンプと全成分一致(§8)。
- $\sigma_m^3=\mathrm{Inn}_A(E_m)$、命題 E1 $\theta\sigma_m\theta=\iota_{x^{2m+1}}\sigma_m^{-1}$ を全 21 基底で確認(§6・検査 44–46)。

---

## 5. $E_m$ の明示式(委嘱項目 3)

$$ E_m:=\tau^2(y^m)\,\tau(y^m)\,y^m=x^mz^my^m\in A\qquad(z=(xy)^{-1}). $$
$\sigma_m(E_m)=y^{-m}(y^mx^mz^m)y^m=x^mz^my^m=E_m$ を $P^{(6)}$ の群積で厳密確認($m=-6..12$・検査 41)。

### 5.1 $\bar A$ 成分(**閉形**)

命題 3.2' の辞書($w=1,\ p=S,\ q=T,\ \dots,\ s_1=S^4,\ s_2=S^3T,\ s_3=S^2T^2,\ s_4=ST^3,\ s_5=T^4$)の下で

$$ \boxed{\ \bar E_m=\sum_{a+b\le4}(-1)^{a+1}\binom{m+1+a}{a+b+2}\,S^aT^b\ } \tag{5.1'}$$

成分表(Hall 順):

| 座標 | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $\bar E_m$ | $-\binom{m+1}2$ | $\binom{m+2}3$ | $-\binom{m+1}3$ | $-\binom{m+3}4$ | $\binom{m+2}4$ | $-\binom{m+1}4$ | $\binom{m+4}5$ | $-\binom{m+3}5$ | $\binom{m+2}5$ | $-\binom{m+1}5$ |

| 座標 | $s_1$ | $s_2$ | $s_3$ | $s_4$ | $s_5$ |
|---|---|---|---|---|---|
| $\bar E_m$ | $-\binom{m+5}6$ | $\binom{m+4}6$ | $-\binom{m+3}6$ | $\binom{m+2}6$ | $-\binom{m+1}6$ |

> **整合**: 先頭 10 成分は class-5 稿 (5.1) と**完全一致**。(5.1') はその weight-6 への自然な延長で、**§5.4 で証明される**。

### 5.2 $C$ 成分 $\varepsilon_m:=E_m\,s(\bar E_m)^{-1}$(**閉形**・二項基底・整係数)

$$
\boxed{
\begin{aligned}
(\varepsilon_m)_{t_5}&=\tbinom m1+7\tbinom m2+17\tbinom m3+17\tbinom m4+6\tbinom m5\\
(\varepsilon_m)_{t_6}&=-\Bigl[\tbinom m2+4\tbinom m3+6\tbinom m4+3\tbinom m5\Bigr]\\
(\varepsilon_m)_{u_1}&=-\Bigl[\tbinom m1+10\tbinom m2+34\tbinom m3+52\tbinom m4+37\tbinom m5+10\tbinom m6\Bigr]\\
(\varepsilon_m)_{u_2}&=\tbinom m2+7\tbinom m3+17\tbinom m4+17\tbinom m5+6\tbinom m6\\
(\varepsilon_m)_{u_3}&=-\Bigl[\tbinom m3+4\tbinom m4+6\tbinom m5+3\tbinom m6\Bigr]\\
(\varepsilon_m)_{u_4}&=3\tbinom m3+10\tbinom m4+11\tbinom m5+4\tbinom m6
\end{aligned}} \tag{5.2'}
$$

$t_5,t_6$ 成分は class-5 稿 (5.2) と**完全一致** ✓。

> **観測 5.3'(二項基底の一段シフト).** $(\varepsilon_m)_{u_2}$ の二項係数列 $[0,0,1,7,17,17,6]$ は $(\varepsilon_m)_{t_5}$ の列 $[0,1,7,17,17,6]$ の一段シフトであり、同様に $u_3$ は $t_6$ のシフト。すなわち
> $$ (\varepsilon_m)_{u_2}=\sum_{j=0}^{m-1}(\varepsilon_j)_{t_5},\qquad (\varepsilon_m)_{u_3}=\sum_{j=0}^{m-1}(\varepsilon_j)_{t_6} . $$
> $u_1,u_4$ 成分にはこの型の関係が見当たらない。**説明は与えていない**(検査 40 で数値確認のみ)。

### 5.3 数値表($E_m$ の 21 座標)

順序 $(w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4\mid t_5,t_6\mid s_1..s_5\mid u_1..u_4)$ ではなく、本稿の**索引順**
$(w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4,t_5,t_6,s_1,s_2,s_3,s_4,s_5,u_1,u_2,u_3,u_4)$ で:

| $m$ | $E_m$ |
|---|---|
| 0 | $[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]$ |
| 1 | $[-1,1,0,-1,0,0,1,0,0,0,\mathbf1,\mathbf0,-1,0,0,0,0,\mathbf{-1},\mathbf0,\mathbf0,\mathbf0]$ |
| 2 | $[-3,4,-1,-5,1,0,6,-1,0,0,\mathbf9,\mathbf{-1},-7,1,0,0,0,\mathbf{-12},\mathbf1,\mathbf0,\mathbf0]$ |
| 3 | $[-6,10,-4,-15,5,-1,21,-6,1,0,\mathbf{41},\mathbf{-7},-28,7,-1,0,0,\mathbf{-67},\mathbf{10},\mathbf{-1},\mathbf3]$ |
| 4 | $[-10,20,-10,-35,15,-5,56,-21,6,-1,\mathbf{131},\mathbf{-28},-84,28,-7,1,0,\mathbf{-252},\mathbf{51},\mathbf{-8},\mathbf{22}]$ |
| 5 | $[-15,35,-20,-70,35,-15,126,-56,21,-6,\mathbf{336},\mathbf{-83},-210,84,-28,7,-1,\mathbf{-742},\mathbf{182},\mathbf{-36},\mathbf{91}]$ |
| 6 | $[-21,56,-35,-126,70,-35,252,-126,56,-21,\mathbf{742},\mathbf{-203},-462,210,-84,28,-7,\mathbf{-1848},\mathbf{518},\mathbf{-119},\mathbf{280}]$ |

($t_5,t_6,u_1,\dots,u_4$ = 太字 = $\varepsilon_m$。$t_5,t_6$ 列は class-5 稿 §5.3 と一致 ✓。)

### 5.4 $\bar E_m$ の加群閉形と **(5.1') の証明**

> **命題 5.4'.** $[n]_u:=1+u+\dots+u^{n-1}=\dfrac{1-u^n}{1-u}$($n<0$ では $[n]_u=-u^n[-n]_u$)と置く。命題 3.2' の記法で
> $$ \boxed{\ \bar E_m=\frac{1}{1-s}\Bigl([m]_t-s^{-m}[m]_{st}\Bigr)\cdot w\ =\ -\sum_{1\le i\le j\le m}s^{-i}t^{\,m-j}\cdot w\ } \tag{5.4'}$$
> であり、$(S,T)$ 展開が (5.1') に一致する。

**証明.** *(a) Fox 微分による第 1 式.* 自由メタベリアン群の Magnus 埋め込みにより、$g\in\gamma_2$ の $\gamma_2/[\gamma_2,\gamma_2]$ 内のクラスは左 Fox 微分 $d(g)=(\partial g/\partial x,\partial g/\partial y)\in\mathbb Z[\mathbb Z^2]^2$ から一意に定まる:$\{(A,B):(s-1)A+(t-1)B=0\}$ は $d(w)$ で生成される自由階数 1 加群で、$d(g)=\lambda_F(g)\,d(w)$。
$d(x^{-1}hx)=s^{-1}d(h)$($h\in\gamma_2$)ゆえ $\lambda_F$ は **$h^x\mapsto s^{-1}h$** の規約に対応する。本稿の規約は $h^x\mapsto s\,h$ なので
$$ \lambda_{\text{本稿}}(g)(s,t)=\lambda_F(g)(s^{-1},t^{-1}). $$
$w=x^{-1}y^{-1}xy$ から $\partial w/\partial y=s^{-1}t^{-1}(s-1)$。$E_m=x^m\cdot z^m\cdot y^m$、$z=y^{-1}x^{-1}$、$\partial z/\partial y=-t^{-1}$、$\bar z=s^{-1}t^{-1}$、$\overline{x^mz^m}=t^{-m}$ より
$$ \frac{\partial E_m}{\partial y}=0+s^m\bigl(-t^{-1}\bigr)[m]_{s^{-1}t^{-1}}+t^{-m}[m]_t . $$
よって $\lambda_F(E_m)=\dfrac{st}{s-1}\Bigl(-s^mt^{-1}[m]_{s^{-1}t^{-1}}+t^{-m}[m]_t\Bigr)=\dfrac{1}{s-1}\Bigl(-s^{m+1}[m]_{s^{-1}t^{-1}}+st^{1-m}[m]_t\Bigr)$。
$s\to s^{-1},t\to t^{-1}$ を代入し、$[m]_{t^{-1}}=t^{1-m}[m]_t$、$\frac{s^{-1}}{s^{-1}-1}=\frac1{1-s}$ を使うと第 1 式を得る。

*(b) 第 2 式.* $s^{-m}[m]_{st}=\sum_{k=0}^{m-1}s^{k-m}t^{k}=\sum_{j=1}^{m}s^{-j}t^{\,m-j}$、$[m]_t=\sum_{j=1}^{m}t^{\,m-j}$ ゆえ
$$ [m]_t-s^{-m}[m]_{st}=\sum_{j=1}^{m}t^{\,m-j}\bigl(1-s^{-j}\bigr),\qquad \frac{1-s^{-j}}{1-s}=-s^{-j}[j]_s=-\sum_{i=1}^{j}s^{-i}. $$
よって $\bar E_m=-\sum_{j=1}^m\sum_{i=1}^{j}s^{-i}t^{\,m-j}$。

*(c) (5.1') への展開.* $s^{-i}=\sum_a(-1)^a\binom{i+a-1}{a}S^a$、$t^{m-j}=\sum_b\binom{m-j}{b}T^b$。$S^aT^b$ の係数は
$$ (-1)^{a+1}\sum_{i=1}^{m}\binom{i+a-1}{a}\sum_{j'=0}^{m-i}\binom{j'}{b} =(-1)^{a+1}\sum_{i=1}^{m}\binom{i-1+a}{a}\binom{m-i+1}{b+1} =(-1)^{a+1}\binom{m+1+a}{a+b+2} $$
最後の等号は、$\sum_{k\ge0}\binom{k+a}{a}x^k=(1-x)^{-(a+1)}$、$\sum_{k\ge0}\binom{k}{b+1}x^k=x^{b+1}(1-x)^{-(b+2)}$ の積 $x^{b+1}(1-x)^{-(a+b+3)}$ の $x^m$ 係数を読むことによる:
$$ \sum_{k\ge0}\binom{k+a}{a}\binom{m-k}{b+1}=\binom{(m-b-1)+(a+b+2)}{a+b+2}=\binom{m+1+a}{a+b+2}. $$
($k=i-1$ と置いた。$k\ge m$ では $\binom{m-k}{b+1}=0$ なので和は $i=1..m$ と同じ。)∎

**機械確認**: 検査 38(225 セル)・66・67($m$ 15 種)。

> **これは class-5 稿の【GAP-E22e】の前半を閉じる。** 同稿は「(5.1) の二項閉形の**証明**」を UNKNOWN として登録し、Fox 微分からの導出を「有望」と書いていた。上の (a)(b)(c) がそれである(しかも class 6 版で)。$\varepsilon_m$ の閉形 (5.2') の証明は**依然 UNKNOWN**(§9 の【GAP-E22e6】)。

---

## 6. Section と欠損項(委嘱項目 4)

### 6.1 定義

$\varphi\in\{\theta,\sigma_m\}$ に対し
$$ d_\varphi(\bar a):=\varphi\bigl(s(\bar a)\bigr)\,s\bigl(\bar\varphi\bar a\bigr)^{-1}\in C,\qquad \varepsilon_m:=E_m\,s(\bar E_m)^{-1}\in C . $$
$C$ が $A$ の中心なので、$d_\varphi(\bar a)$ は「$\varphi(H(\bar a\mid0))$ の Hall 座標の $C$ 部分」に等しい。

### 6.2 一般 collection 閉形

> **補題 6.3'.** $\varphi\in\operatorname{Aut}(A)$ が下中心フィルトレーションを保つとする。$u_k:=\bar\varphi(e_k)\in\bar A$($k$ は $\bar A$ の 15 基底を走る)と置くと、$\bar a=\sum_ka_ke_k$ に対し
> $$ d_\varphi(\bar a)=\sum_{k}a_k\,d_\varphi(e_k)\;-\;\sum_{k}\tbinom{a_k}2\,\delta(u_k)\;-\;\sum_{j<k}a_ja_k\,\kappa(u_j,u_k). \tag{6.1'}$$
> さらに、$\varphi$ がフィルトレーションを保つので
> - $(u_k)_w=0$($k\ne w$)、$(u_k)_p=(u_k)_q=0$($\mathrm{wt}(e_k)\ge4$);
>
> したがって $\kappa$ の $t_5,t_6,u_1,u_2,u_3$ 成分は二重和で完全に消え、**$u_4$ 成分だけが 3 対 $(w,p),(w,q),(p,q)$ で生き残り**
> $$ \boxed{\ d_\varphi(\bar a)=\sum_{k}a_k\,d_\varphi(e_k)-\tbinom{a_w}2\delta(W)-\Bigl[\tbinom{a_p}2P_qP_p+\tbinom{a_q}2Q_qQ_p+a_wa_pW_qP_p+a_wa_qW_qQ_p+a_pa_qP_qQ_p\Bigr]e_{u_4}\ } \tag{6.2'}$$
> ここで $W:=\bar\varphi(w)$、$P:=\bar\varphi(p)$、$Q:=\bar\varphi(q)$。

**証明.** $\varphi(s\bar a)=\prod_k\varphi(g_k)^{a_k}$(昇順)。$\varphi(g_k)=H(u_k\mid z_k)$、$z_k=d_\varphi(e_k)$ とすると (2.3') より $\varphi(g_k)^{a_k}=H(a_ku_k\mid a_kz_k-\binom{a_k}2\delta(u_k))$。(2.2') を反復すると積の $C$ 成分は各因子の $C$ 成分の和 $-\sum_{j<k}\kappa(a_ju_j,a_ku_k)$。$s(\bar\varphi\bar a)$ の $C$ 成分は $0$。以上で (6.1')。
後半: $\kappa$ の $t_5,t_6,u_1,u_2,u_3$ 成分は第 2 引数の $w$ 座標を含むが $j<k\Rightarrow k\ne w$ ゆえ $0$。$\kappa$ の $u_4$ 成分 $(u_j)_q(u_k)_p$ は $(u_k)_p\ne0$ を要求するので $\mathrm{wt}(e_k)\le3$、すなわち $k\in\{w,p,q\}$。$j<k$ と合わせて 3 対。$\delta(u_k)=\kappa(u_k,u_k)$ も同じ理由で $k=w$ の全成分と $k\in\{p,q\}$ の $u_4$ 成分だけが残る。∎

**機械確認**: 検査 47–50($\theta$ 120/200 例、$\sigma_m$ 9 個 × 25 例 / 10 個 × 40 例)。

> **★ class-5 との差.** class-5 稿 (6.2) では二重和が**丸ごと**消え、$d_\varphi$ は「線型 $+\binom{a_w}2$ の一項」だった。class 6 では $\kappa$ の $u_4$ 項が $b_p$ 型なので、上の 5 つの二次項が残る。

### 6.3 $\theta$ の欠損 — **線型 + 一つの $a_pa_q$ 項**

$d_\theta(e_k)$ の表($\S3.2$ の $C$ 成分):

| $e_k$ | $w$ | $p$ | $q$ | $r_1$ | $r_2$ | $r_3$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ | $s_1$ | $s_2$ | $s_3$ | $s_4$ | $s_5$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d_\theta$ | $0$ | $-t_6$ | $-t_5$ | $-u_3$ | $-t_5-t_6-2u_2$ | $-u_1$ | $0$ | $-t_6-2u_2-2u_3+u_4$ | $-t_5-2u_1-2u_2-u_4$ | $0$ | $0$ | $-2u_3$ | $-3u_2$ | $-2u_1$ | $0$ |

$\bar\theta w=-w$ ゆえ $\delta(\bar\theta w)=0$、$P=\bar\theta p=-q$($P_p=0$)、$Q=\bar\theta q=-p$($Q_q=0$)。したがって (6.2') の二次項は
$\binom{a_p}2P_qP_p=0$、$\binom{a_q}2Q_qQ_p=0$、$W_qP_p=W_qQ_p=0$、$P_qQ_p=(-1)(-1)=1$ の**一つだけ**残り

$$
\boxed{
\begin{aligned}
(d_\theta)_{t_5}&=-\bigl(a_q+a_{r_2}+a_{t_3}\bigr)\\
(d_\theta)_{t_6}&=-\bigl(a_p+a_{r_2}+a_{t_2}\bigr)\\
(d_\theta)_{u_1}&=-\bigl(a_{r_3}+2a_{t_3}+2a_{s_4}\bigr)\\
(d_\theta)_{u_2}&=-\bigl(2a_{r_2}+2a_{t_2}+2a_{t_3}+3a_{s_3}\bigr)\\
(d_\theta)_{u_3}&=-\bigl(a_{r_1}+2a_{t_2}+2a_{s_2}\bigr)\\
(d_\theta)_{u_4}&=a_{t_2}-a_{t_3}\;\boxed{-\,a_p\,a_q}
\end{aligned}}\qquad(\textbf{$m$ 非依存}) \tag{6.3'}
$$

$t_5,t_6$ 行は class-5 稿 (6.3) と**完全一致** ✓。**$u_4$ 行の $-a_pa_q$ が class-6 で新規**(class 5 では $d_\theta$ は線型だった)。
**機械確認**: 検査 51・53(この逐語式を 300 例で実測と照合)。

### 6.4 $\sigma_m$ の欠損

$d_\sigma(e_k)$ の表(§4.3 の枠内・$m$ 多項式):

| $e_k$ | $d_\sigma(e_k)$ |
|---|---|
| $w$ | $m\,u_4$ |
| $p$ | $u_4$ |
| $q$ | $-t_5+2u_1+(1-m)u_2+(m-3)u_4$ |
| $r_1$ | $0$ |
| $r_2$ | $t_5-2u_1+(m-1)u_2+(2-m)u_4$ |
| $r_3$ | $-3t_5-t_6+9u_1+(9-3m)u_2+(2-m)u_3+(3m-6)u_4$ |
| $t_1$ | $0$ |
| $t_2$ | $-t_6+3u_2-m\,u_3$ |
| $t_3$ | $t_5+t_6-4u_1+(m-7)u_2+(m-2)u_3+(3-m)u_4$ |
| $t_4$ | $-2t_5-t_6+12u_1+(17-2m)u_2+(5-m)u_3+(2m-8)u_4$ |
| $s_1$ | $0$ |
| $s_2$ | $-2u_3$ |
| $s_3$ | $3u_2+3u_3$ |
| $s_4$ | $-2u_1-6u_2-3u_3+2u_4$ |
| $s_5$ | $5u_1+9u_2+3u_3-4u_4$ |

$W=\bar\sigma w$ は $W_w=1,W_p=-1,W_q=m,W_{r_1}=1,W_{r_2}=-m,W_{r_3}=\binom m2$、$P=\bar\sigma p$ は $P_p=0,P_q=1$、$Q=\bar\sigma q$ は $Q_p=-1,Q_q=-1$。よって
$\delta(W)=-e_{t_5}+m\,e_{t_6}+e_{u_1}-m\,e_{u_2}+\binom m2e_{u_3}-m\,e_{u_4}$、$P_qP_p=0$、$Q_qQ_p=1$、$W_qP_p=0$、$W_qQ_p=-m$、$P_qQ_p=-1$。(6.2') に代入して

$$
\boxed{
\begin{aligned}
(d_\sigma)_{t_5}&=-a_q+a_{r_2}-3a_{r_3}+a_{t_3}-2a_{t_4}+\tbinom{a_w}2\\
(d_\sigma)_{t_6}&=-a_{r_3}-a_{t_2}+a_{t_3}-a_{t_4}-m\tbinom{a_w}2\\
(d_\sigma)_{u_1}&=2a_q-2a_{r_2}+9a_{r_3}-4a_{t_3}+12a_{t_4}-2a_{s_4}+5a_{s_5}-\tbinom{a_w}2\\
(d_\sigma)_{u_2}&=(1-m)a_q+(m-1)a_{r_2}+(9-3m)a_{r_3}+3a_{t_2}+(m-7)a_{t_3}+(17-2m)a_{t_4}+3a_{s_3}-6a_{s_4}+9a_{s_5}+m\tbinom{a_w}2\\
(d_\sigma)_{u_3}&=(2-m)a_{r_3}-m\,a_{t_2}+(m-2)a_{t_3}+(5-m)a_{t_4}-2a_{s_2}+3a_{s_3}-3a_{s_4}+3a_{s_5}-\tbinom m2\tbinom{a_w}2\\
(d_\sigma)_{u_4}&=m\,a_w+a_p+(m-3)a_q+(2-m)a_{r_2}+(3m-6)a_{r_3}+(3-m)a_{t_3}+(2m-8)a_{t_4}+2a_{s_4}-4a_{s_5}\\
&\qquad +m\tbinom{a_w}2-\tbinom{a_q}2+m\,a_wa_q+a_pa_q
\end{aligned}} \tag{6.4'}
$$

$t_5,t_6$ 行は class-5 稿 (6.4) と**完全一致** ✓。
**機械確認**: 検査 52・54(この逐語式を $m\in\{0,1,2,3,5,7,11,17,63,-4,-11\}$ × 40 例で実測と照合)。

### 6.5 $\sigma^2$ の欠損

$$ d_{\sigma^2}(\bar a)=d_\sigma(\bar\sigma\bar a)+\sigma\vert_C\bigl(d_\sigma(\bar a)\bigr) \tag{6.5'}$$
($\sigma\vert_C$ は §4.3 の $\sigma(t_5),\sigma(t_6),\sigma(u_i)$ の 6 行 — **class 6 では $t_5,t_6$ の像が $u$ 成分をもつので $2\times2$ では足りない**)。
**機械確認**: 検査 55($m$ 7 種 × 25 例)。

---

## 7. 有限商 $A_j$ での読み方(補足)

> **補題 7.1'(代表元非依存).** §2–§6 の全ての閉形は、**$\bar A$ 座標を $\bmod\,2^j$、$C$ 座標を $\bmod\,2^{j-1}$** で読むと $\bar A$ 座標の代表元の取り方に依らない。

**証明.** 非線型項は (i) 双線型項($a_pb_w$, $a_qb_p$ 型)と (ii) $\binom a2$ 型のみ。(i): $a_p\mapsto a_p+2^j$ で値は $2^j\cdot(\text{整数})$ しか変わらず $2^{j-1}$ を法として $0$。(ii): $\binom{a+2^j}2-\binom a2=2^ja+2^{j-1}(2^j-1)\equiv0\pmod{2^{j-1}}$。∎

**機械確認**: 検査 61($j=2..6$ × $m$ 5 種 × 20 例)、および対照として「$C$ を $\bmod\,2^j$ で読むと代表元依存」(検査 62)。

**実装への注意 3 点**(class-5 稿と同じ)
1. $m$ はリテラル整数として扱う($\binom mk$ を先に整数で評価してから還元)。$m$ を先に $\bmod\,2^j$ に落としてはならない。
2. $\binom{a_w}2,\binom{a_q}2,\binom{a_p}2$ は**整数で評価してから** $\bmod\,2^{j-1}$ に落とす。
3. $j=1$ では $C_1=0$ で $d_\theta,d_\sigma,\varepsilon_m,c_s$ が全て潰れる。

---

## 8. 自己検査(委嘱項目 5)

`node docs/scout/hall6.mjs`。**67 項目・FAILS = 0・終了コード 0**。委嘱指定の 3 項目:

| # | 検査 | 内容 | 結果 |
|---|---|---|---|
| **(i)** | $\theta^2=\mathrm{id}$ on $A$ | 表の座標合成 $\theta_{\rm coord}\circ\theta_{\rm coord}$ をランダム 60 例、および全 21 基底で | **PASS**(検査 26, 27) |
| **(ii-a)** | $\sigma_m(E_m)=E_m$ | $P^{(6)}$ の群積で厳密($m=-6..12$)+ 作用表の座標計算($m$ 10 種) | **PASS**(検査 41, 42) |
| **(ii-b)** | $\sigma_m^3=\mathrm{Inn}(E_m)$ | 座標で $a\mapsto a+\beta(a,\bar E_m)$ と一致($m$ 8 種 × 8 例)、表の 3 重合成で全 21 基底($m$ 8 種)、群積で直接($m$ 6 種 × 21 基底) | **PASS**(検査 43, 44, 45) |
| **(iii)** | **weight $\le5$ 制限 = class-5 正本** | 下表 | **PASS**(検査 56) |

**(iii) の内訳**(class-5 稿 `docs/week4-E2作用表_v1.md` の表を逐語ハードコードし、本稿の class-6 座標の**先頭 12 成分**と全セル比較):

| 区分 | 出典 | セル数 |
|---|---|---|
| 交換子表 $[g,x],[g,y]$ | §2.1(12 元 × 2 × 12 座標) | 288 |
| $\theta$ 表 | §3.2(12 元 × 12 座標) | 144 |
| $\sigma_m$ 表 | §4.3($m\in\{0,1,2,3,4,5,7,11,17,63\}$ × 12 元 × 12 座標) | 1440 |
| $E_m$($\bar E_m$ (5.1) + $\varepsilon_m$ (5.2)) | §5.1/5.2($m\in\{0,\dots,6,9,17,31,63\}$ × 12 座標) | 132 |
| $d_\theta$ (6.3) / $d_\sigma$ (6.4) の $t_5,t_6$ | §6.3/6.4(ランダム 100 例 + $m$ 9 種 × 20 例、各 2 成分) | 560 |
| | **合計** | **2564** |

**不一致 0 件。**

### 8.1 第二系統(GAP)との照合 — **$\bar A$ 層のみ**

`certificates/e19/gap_system_c6_m{m}.txt`($m\in\{0,1,2,3,5,7,11,17,23,63\}$、10 件)は $30\times15$ 行列 $M$ と長さ 30 の $b$ を含む。
上 15 行 $=1+\bar\theta$、下 15 行 $=\bar{\mathcal N}=1+\bar\sigma+\bar\sigma^2$、$b$ の後半 15 成分 $=-\bar E_m$(前半 15 は $0$)。

| 対象 | セル数 | 結果 |
|---|---|---|
| c6 の $M$ 全成分($15\times15\times2$ ブロック × 10 個の $m$) | **4500** | **全一致**(検査 58) |
| c6 の $b$ 全成分($30\times10$) | **300** | **全一致**(検査 59) |
| c5 の $M,b$(class-5 射影・$10\times10\times2+10$ × 10 個の $m$) | **2100** | **全一致**(検査 60) |

> これにより **$\bar\theta$、$\bar{\mathcal N}$、$\bar E_m$(いずれも $\bar A$ 層)は cross-checked**(GAP 系統 × 本稿の Magnus 系統)。
> **$C$ 層(rank 6)には第二系統がない** — 本稿最大の未閉鎖点(§9)。

### 8.2 その他の主要検査(全て PASS)

| 検査 | 内容 |
|---|---|
| モデル健全性 | $\dim R=127$・21 基底の Hall 座標が単位ベクトル・重み別階数 $(1,2,3,6,9)$・往復一意性 |
| Hall 恒等式 (1.2) | $P^{(6)}$ 内で 1000 組 |
| §2.1 の手計算 vs 機械 | **504 セル**(24 エントリ × 21 座標)一致 |
| $A$ の交換子構造 | 非自明対が 12 個・class 2・$C\subseteq Z(A)$・$\beta$ の明示形 (2.1') |
| 積 (2.2') / 冪 (2.3') / 逆 (2.4') / $c_s$ (2.5') | 200 対 / 60 例 / 40 例 / 120 対 |
| collection 公式 (4.1') | $g=x,y$ × $m$ 9 種 × 8 例 |
| $\sigma_m$ の $m$ 多項式 | $m=0..10$ で補間 → $m\in\{11,13,20,33,64,-1,-5,-12,-30\}$ で外挿一致 |
| 命題 E1 $\theta\sigma\theta=\iota_{x^{2m+1}}\sigma^{-1}$ | 全 21 基底 × $m$ 8 種(群レベル) |
| (5.1')(5.2')(5.4') | $m$ 14–18 種 |
| (6.1')(6.2')(6.3')(6.4')(6.5') | $\theta$ 側 120/200/300 例、$\sigma_m$ 側 225/400/440/175 例(**本文の逐語式そのものの検査**を含む) |
| §9.4 の $\mathcal N_C\vert_C$ 一般 $m$ 式 | 36 成分 × $m$ 12 種 |
| (3.3')(4.4') 加群閉形 | 15 基底 / 15 基底 × $m$ 9 種 |
| 補題 7.1' 代表元非依存 + 対照 | $j=2..6$ × $m$ 5 種 × 20 例 |

---

## 9. 状態札・【GAP】・引き継ぎ

### 9.1 状態札

| 対象 | 札 |
|---|---|
| §2.1 の交換子表(weight-6 補正込み) | **紙上証明**(Hall 恒等式 + Jacobi)+ Magnus 検算一致。**単系統** |
| §2.2–2.4 の積表・(2.2')–(2.5') | **紙上証明** + Magnus 検算。**単系統** |
| §3 の $\theta$ 表(全 21 元) | **紙上証明**(手計算)+ Magnus 検算。$\bar A$ 部分は **E19/GAP と cross-checked** |
| §3.3 命題 3.2'/(3.3')(加群記述) | **紙上証明** + 機械検算 |
| §4.1 補題 4.1' | **紙上証明**(帰納法・全 $m\in\mathbb Z$)+ 機械検算 |
| §4.3 の $\sigma_m$ 表 | $\bar A$ 部は **紙上証明**(命題 4.4')+ **E19/GAP と cross-checked**。**$C$ 部は Magnus 単系統** |
| §5.1 (5.1') $\bar E_m$ の閉形 | **紙上証明**(命題 5.4')+ **E19/GAP と cross-checked**(10 件・全成分) |
| §5.2 (5.2') $\varepsilon_m$ の閉形 | **単系統・証明なし**($m\in\{0..7,9,13,17,31,63,100,-1,-3,-8,-20\}$ で検証) |
| §5.4 命題 5.4' | **紙上証明** + 機械検算 |
| §6 補題 6.3'・(6.2')(6.3')(6.4')(6.5') | **紙上証明**(補題 6.3')+ Magnus 検算。**$C$ 層なので単系統** |
| §7 補題 7.1' | **紙上証明**(2 行)+ 機械検算 |
| verified(Lean) | **一つもない** |

**「cross-checked」と言えるもの**: $\bar\theta$、$\bar\sigma_m$($\bar{\mathcal N}$ 経由)、$\bar E_m$ — いずれも $\bar A$ 層(rank 15)。
**「candidate(単系統)」に留まるもの**: $C$ 層(rank 6)の一切 — $d_\theta,d_\sigma,\varepsilon_m$、$\sigma/\theta$ の $t_5,t_6,u_i$ 成分、§2.1 の重み 5・6 補正、$c_s$。

### 9.2 【GAP】

| # | 内容 | 状態 |
|---|---|---|
| **【GAP-E22e】** | (5.1) の二項閉形の**証明**(class-5 稿で新設・UNKNOWN) | **本稿で閉鎖**(命題 5.4'・class 6 版で証明、class 5 は $a+b\le3$ への制限) |
| **【GAP-E22a′6】** | $C$ 層(rank 6)のデータの**第二系統**。route G(GAP の $A_j$ PC presentation 上の群演算)が本稿の $C$ 成分を独立に再現するか | **UNKNOWN**。class-5 の【GAP-E22a′】の class-6 版で、規模が 2 → 6 座標に増えている |
| **【GAP-E22e6】(新設)** | $\varepsilon_m$ の閉形 (5.2') の**証明**。$\bar E_m$ は Fox 微分で落ちたが、$C$ 成分は自由メタベリアン加群の外に出るので同じ手が効かない。$\gamma_2/\gamma_7$ の「二段目の Magnus 座標」(Fox 二階微分 / Chen の反復積分)が要るか | **UNKNOWN**(有限・実行可能) |
| **【GAP-E22f6】(新設)** | 観測 5.3'($(\varepsilon_m)_{u_2}=\sum_{j<m}(\varepsilon_j)_{t_5}$、$u_3$ と $t_6$ も同様)の**説明**。$u_1,u_4$ には対応物がないので、$u_2,u_3$ だけが $t_5,t_6$ の「$y$ 方向の積分」になる理由 | **UNKNOWN** |

> **【文献要請】**(司令塔宛・優先度中)
> **困難**: 自由群 $F_2$ の $\gamma_2/\gamma_7$ における、非メタベリアン成分($[\gamma_2,\gamma_2]$ 部分)の**閉形式座標**。$\bar A=\gamma_2/[\gamma_2,\gamma_2]$ は Magnus 埋め込み(Fox 微分)で完全に制御でき、本稿の (3.3')(4.4')(5.4') はすべてそこから落ちた。しかし $C=[\gamma_2,\gamma_2]\gamma_7/\gamma_7$ の側には対応する「一階の」道具がなく、$\varepsilon_m$ や $d_\sigma$ の $u$ 成分は数値補間でしか得られていない。
> **欲しい結果の型**: 自由群の**二段可解商 $F/[\gamma_2,\gamma_2]$ の一段上**(例: $F/[[\gamma_2,\gamma_2],\gamma_2]$、あるいは $\gamma_2$ の下中心層)に対する、Fox 微分の類似物 —「$g\in\gamma_2$ の $[\gamma_2,\gamma_2]$ 成分を、$g$ の語から明示式で読み出す関数」。候補となる語彙: Magnus 展開の高次項、Fox 二階微分と Blanchfield/Alexander 加群の二次版、Chen の反復積分・Chen 群 $F/\gamma_k(\gamma_2)$、Milnor 不変量 $\bar\mu$、free differential calculus の「second-order Jacobian」。$E_m=x^mz^my^m$ のような**具体語**に対して評価できる形であることが必須(存在定理だけでは足りない)。
> **これが効けば**: (5.2') と §6.4 の $u$ 成分に紙上証明が付き、$C$ 層が「単系統の数値」から「証明された閉形」に上がる。第二系統(route G)の必要性も下がる。

### 9.3 実装への引き継ぎ(最小仕様)

1. **$\bar A_j$ 側**(rank 15): $\bar\theta$(§3.3 の $-\varsigma$)、$\bar\sigma_m$(§4.3 の $\bar A$ 部・$m$ 4 次多項式)、$\bar E_m$((5.1'))。**E19 c6 ダンプで二系統照合できる** — 実装は最初にこの照合を通すこと。
2. **$C_j$ 側**(rank 6): $\theta\vert_C,\sigma_m\vert_C$(§3.2/§4.3 の最後 6 行)、$c_s$((2.5'))、$d_\theta$((6.3'))、$d_\sigma$((6.4'))、$d_{\sigma^2}$((6.5'))、$\varepsilon_m$((5.2'))。**照合先がないので route G が独立に構成すること**(座標系・section の実装コードを共有しない)。
3. **還元規約**: $\bar A$ を $\bmod\,2^j$、$C$ を $\bmod\,2^{j-1}$(補題 7.1')。$\binom{a}2$ と $\binom mk$ は**整数で評価してから**還元。
4. **禁止**: 「$\bar A$ 上で成り立つ式を $A$ でも使う」(§2.1 の罠 1・2)。「$c_s$ を $\beta$ から一意に決める」(§2.4)。「class-5 の $C$ 用公式をそのまま持ち込む」(罠 3・4 で形が変わる)。
5. **$\sigma\vert_C$ は $2\times2$ ではない**: class 5 では $C=\langle t_5,t_6\rangle$ が $\sigma$ 安定な $2\times2$ ブロックだったが、class 6 では $\sigma(t_5)=t_6-u_2+mu_3-u_4$ のように $u$ 成分が出る。$C$ 上の作用は $6\times6$(かつ $m$ 依存)。

### 9.4 作用表からの一行帰結(**解釈は本稿の射程外**)

実装が必要とするので数値だけ置く。$\mathcal N_C:=1+\sigma+\sigma^2$ を $C$ に制限すると(基底 $t_5,t_6,u_1,u_2,u_3,u_4$)、

| | $t_5\mapsto$ | $t_6\mapsto$ | $u_1\mapsto$ | $u_2\mapsto$ | $u_3\mapsto$ | $u_4\mapsto$ |
|---|---|---|---|---|---|---|
| 任意の $m$ | $(m+2)(u_1{+}u_2{+}u_3)+(m-1)u_4$ | $(1-m)(u_1{+}u_2{+}u_3)+(m+2)u_4$ | $2(u_1{+}u_2{+}u_3)$ | $-(u_1{+}u_2{+}u_3)$ | $2(u_1{+}u_2{+}u_3)$ | $3u_4$ |

(像の $t_5,t_6$ 成分はすべて $0$、すなわち $\mathcal N_C(C)\subseteq\langle u_1,u_2,u_3,u_4\rangle$。
$m\in\{0,1,2,3,4,5,7,11,17,63,-2,-9\}$ の 12 種 × 36 成分で機械確認 — 検査 63。
**class 5 では $\mathcal N_C=0$ だったが class 6 では $0$ でない。** 本稿はこの事実を解釈しない — $\Lambda$・$\mathrm{Ob}$・可解性の議論は委嘱の範囲外。)

---

## 付録 A. 検算スクリプトの構成

`docs/scout/hall6.mjs`(node・BigInt・外部依存なし)

| 節 | 内容 |
|---|---|
| 0 | モデル健全性(127 次元・21 基底・重み別階数・往復一意性・$\tau^3=\mathrm{id}$) |
| 1 | Hall 恒等式 (1.2)・$P^{(6)}$ 内交換子表(手計算 504 セルとの照合) |
| 2 | $A$ 内交換子表(全 $21\times21$)・(2.1')–(2.5') |
| 3 | $\theta$ の全 21 像・$\theta^2=\mathrm{id}$ |
| 4 | (4.1') collection 公式・$\sigma_m$ の全 21 像($m$ 補間 + 外挿)・$m$ 依存の局在・$\theta\vert_C,\sigma\vert_C$ |
| 5 | $E_m$ の 21 座標・(5.1')(5.2')・観測 5.3' |
| 6 | $\sigma_m(E_m)=E_m$・$\sigma^3=\mathrm{Inn}(E_m)$(3 通り)・命題 E1 |
| 7 | $d_\theta,d_\sigma$ の基底値・(6.1')(6.2')(6.3')(6.4')(6.5')・**本文の逐語式の検査** |
| 8 | class-5 正本との全 2564 セル照合 |
| 9 | E19 の GAP c6 / c5 ダンプ照合(4500 + 300 + 2100 成分) |
| 10 | 補題 7.1' 代表元非依存 + 対照 |
| 11 | 実装引き継ぎダンプ($\bar\theta,\bar\sigma$ の $15\times15$・$\mathcal N_C\vert_C$) |
| 12 | 加群記述 (3.3')(4.4')(5.4') |

実行結果: `pass` 67 件、`FAIL` 0 件、終了コード 0。
