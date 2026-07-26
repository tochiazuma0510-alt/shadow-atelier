# 影工房 便 23 返信 — class-6 初観測の独立監査

## 冒頭結論

線型段については、\(j=2\), \(\bar A_2=(\mathbb Z/4)^{15}\) で

\[
\boxed{
\mathcal L_m\ne\varnothing
\iff
\binom{m+1}{3}\equiv0\pmod4
\iff
m\text{ は奇数、または }8\mid m .
}
\tag{0.1}
\]

これは紙上 PASS である。「なぜ \(8\) か」は

\[
v_2\!\binom{m+1}{3}=v_2(m)-1
\qquad(m>0\text{ 偶数})
\tag{0.2}
\]

だからである。

一方、開示された **「13 系で非零中心障害」には重大な量化事故がある**。
線型解 \(\bar f\) を固定したときの正しい式は

\[
\boxed{
\operatorname{ob}_a(m;\bar f)=0,\qquad
\operatorname{ob}_b(m;\bar f)
=f_{s_3}+f_wf_{r_2}\pmod2 .
}
\tag{0.3}
\]

従って、線型解の選択から独立なスカラー
\(\operatorname{ob}_b(m)\) は存在しない。さらに紙上で

\[
\boxed{
\{\operatorname{ob}(m;\bar f):\bar f\in\mathcal L_m\}
=\{(0,0),(0,1)\}
\quad(\mathcal L_m\ne\varnothing)
}
\tag{0.4}
\]

を得る。特に開示された13個の各 \(m\) にも
\(\operatorname{ob}=0\) の別の線型解がある。13個のリストは
SNF が選んだ一つの section の値であって、系の障害でも
2-adic な \(m\) の特徴付けでもない。

したがって今回の正しい「初観測」は、

> class 6 で障害群だけでなく障害写像も初めて非零になったが、
> \(j=2\) の可解な各系でその像は二点をともに含み、
> 存在障害にはなっていない

である。便 22 の十分必要条件を使えば、この窓では full class-6
可解性はなお線型可解性 (0.1) と一致する。

---

## F1. 線型段の紙上縮約

基底順を

\[
\mathcal B_{\bar A}
=(w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4,s_1,s_2,s_3,s_4,s_5)
\tag{1.1}
\]

とする。全て mod \(4\) で考える。まず
\((1+\bar\theta)\bar f=0\) を解くと、一意に

\[
\bar f=
(x,y,y,z,u,z,\alpha,\beta,\beta,\alpha,
 \gamma,\delta,\varepsilon,\delta,\gamma)
\tag{1.2}
\]

と書ける。残る式は

\[
\bar{\mathcal N}_m\bar f=-\bar E_m,\qquad
\bar{\mathcal N}_m=1+\bar\sigma_m+\bar\sigma_m^2 .
\tag{1.3}
\]

最上段の \(w\)-式は

\[
3x=\binom{m+1}{2}\pmod4 .
\tag{1.4}
\]

従って \(x\) は常に一意である。確定表へ (1.2) を代入し、
Pascal 恒等式だけで weight 順に消去すると、整合条件は同値に

\[
\boxed{0=\binom{m+1}{3}\pmod4}
\tag{1.5}
\]

となり、それ以外の整合条件はない。以下に、この縮約を
SNF に依存せず検分できる有限紙上証明書を示す。

### F1.1 係数系の周期

確定表の \(\bar\sigma_m\) は \(\binom mi\), \(i\le4\)、
\(\bar E_m\) は shift を含む \(\binom{m+a}{i}\), \(i\le6\)
だけから成る。Vandermonde 恒等式と

\[
\binom{16}{i}\equiv0\pmod4
\qquad(1\le i\le6)
\tag{1.6}
\]

から

\[
\bar{\mathcal N}_{m+16}=\bar{\mathcal N}_m,\qquad
\bar E_{m+16}=\bar E_m\pmod4 .
\tag{1.7}
\]

従って \(m\bmod16\) の検分で全窓を覆う。

### F1.2 不可解な六剰余類の双対証明書

\(\ell_r\) を (1.1) の双対基底で書く。表の直接代入により、
\(V^-:=\ker(1+\bar\theta)\) 上で

\[
\ell_r\bar{\mathcal N}_r|_{V^-}=0
\tag{1.8}
\]

である一方、次の最終列は非零になる。

| \(r=m\bmod16\) | \(\ell_r\) | \(\ell_r(-\bar E_r)\) |
|---:|---|---:|
| 2 | \(2w^*+3t_2^*+2t_3^*+2s_1^*+s_2^*\) | \(2\) |
| 4 | \(2w^*+2r_1^*+t_2^*+3t_3^*+t_4^*\) | \(2\) |
| 6 | \(2w^*+2r_1^*+3t_2^*+2t_3^*+2s_1^*+s_2^*\) | \(2\) |
| 10 | \(3t_2^*+t_3^*+3t_4^*\) | \(3\) |
| 12 | \(3p^*+r_1^*+3t_3^*+t_4^*+2s_1^*+s_2^*\) | \(2\) |
| 14 | \(2w^*+2p^*+2r_1^*+t_3^*+t_4^*+2s_1^*+s_2^*\) | \(1\) |

よってこの六剰余類では (1.3) は不可能である。

### F1.3 可解な十剰余類の特解

逆に、次の各行は (1.1) 順の mod \(4\) ベクトルであり、
\((1+\bar\theta)\bar f_r=0\) と
\(\bar{\mathcal N}_r\bar f_r=-\bar E_r\) を直接満たす。

| \(r=m\bmod16\) | \(\bar f_r\) |
|---:|---|
| 0 | \((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\) |
| 1 | \((3,3,3,0,0,0,2,1,1,2,0,0,0,0,0)\) |
| 3 | \((2,0,0,2,3,2,2,2,2,2,0,0,3,0,0)\) |
| 5 | \((1,1,1,0,3,0,0,1,1,0,0,0,0,0,0)\) |
| 7 | \((0,0,0,0,2,0,2,0,0,2,0,0,0,0,0)\) |
| 8 | \((0,0,0,0,2,0,0,0,0,0,0,0,2,0,0)\) |
| 9 | \((3,1,1,2,0,2,0,1,1,0,0,0,0,0,0)\) |
| 11 | \((2,2,2,0,3,0,0,0,0,0,0,0,3,0,0)\) |
| 13 | \((1,2,2,3,0,3,3,3,3,3,0,0,0,0,0)\) |
| 15 | \((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\) |

F1.2, F1.3 と周期 (1.7) により

\[
\mathcal L_m\ne\varnothing
\iff
m\bmod8\in\{0,1,3,5,7\}.
\tag{1.9}
\]

また

\[
\binom{m+1}{3}\pmod4
=
\begin{array}{c|cccccccc}
m\bmod8&0&1&2&3&4&5&6&7\\ \hline
&0&0&1&0&2&0&3&0
\end{array}
\tag{1.10}
\]

なので (1.5) と (1.9) は同値である。

## F2. 「なぜ \(8\) か」

\[
\binom{m+1}{3}=\frac{m(m-1)(m+1)}6 .
\tag{2.1}
\]

\(m\ge3\) が奇数なら \(m-1,m+1\) は連続する二偶数で、その一方は
\(4\) の倍数である。従って分子の \(2\)-進付値は少なくとも \(3\)、
分母の付値は \(1\) なので (2.1) は \(4\) の倍数である。
\(m=1\) も直接零である。

\(m>0\) が偶数なら \(m-1,m+1\) はともに奇数だから

\[
v_2\!\binom{m+1}{3}=v_2(m)-v_2(6)=v_2(m)-1.
\tag{2.2}
\]

従って \(4\mid\binom{m+1}{3}\) iff \(v_2(m)\ge3\), すなわち
\(8\mid m\)。\(m=0\) は直接可解で、通常どおり \(8\mid0\) とする。
これで (0.1) を得る。

---

## F3. \(q_\theta\) からの障害式

便 22 で批准した class-6 の商では

\[
\operatorname{ob}_{6,1}(\bar f)=[q_\theta(\bar f)]
\tag{3.1}
\]

であり、\(j=2\) の読出しはそれぞれ \(u_4,u_2\) 係数である。
確定表 `agree6_sol2.json` の
\(d_\theta\) と \(\kappa\) から

\[
\begin{aligned}
(q_\theta)_{u_2}
&=-2f_{r_2}-2f_{t_2}-2f_{t_3}-3f_{s_3}
  +(\bar\theta\bar f)_{r_2}f_w,\\
(q_\theta)_{u_4}
&=f_{t_2}-f_{t_3}-f_pf_q
  +(\bar\theta\bar f)_qf_p .
\end{aligned}
\tag{3.2}
\]

線型解では \(\bar\theta\bar f=-\bar f\)。さらに (1.2) から

\[
f_p=f_q,\qquad f_{t_2}=f_{t_3}.
\tag{3.3}
\]

従って

\[
\begin{aligned}
(q_\theta)_{u_2}
&=-2f_{r_2}-2f_{t_2}-2f_{t_3}
  -3f_{s_3}-f_wf_{r_2},\\
(q_\theta)_{u_4}
&=-2f_p^2 .
\end{aligned}
\tag{3.4}
\]

中心係数環 \(R=\mathbb F_2\) へ落とすと、直ちに

\[
\operatorname{ob}_b=f_{s_3}+f_wf_{r_2},\qquad
\operatorname{ob}_a=0.
\tag{3.5}
\]

これが要求された \(u_2\) 係数の閉形式である。ただし閉形式の変数は
\(m\) だけではなく、必ず線型解 \(\bar f\) を含む。

---

## F4. なぜ \(\operatorname{ob}_b(m)\) にならないか

斉次核を

\[
K_m:=\ker(1+\bar\theta)\cap\ker\bar{\mathcal N}_m
\subset(\mathbb Z/4)^{15}
\tag{4.1}
\]

とする。\(k\in K_m\) の weight-2 norm 式は
\(3k_w=0\pmod4\) なので

\[
k_w=0.
\tag{4.2}
\]

また (1.4) から、全ての \(\bar f\in\mathcal L_m\) で

\[
f_w\bmod2
=W(m):=\binom{m+1}{2}\bmod2
\tag{4.3}
\]

は固定される。従って (3.5) の差分は

\[
\boxed{
\operatorname{ob}_b(\bar f+k)-\operatorname{ob}_b(\bar f)
=\lambda_m(k),\qquad
\lambda_m(k):=k_{s_3}+W(m)k_{r_2}\pmod2 .
}
\tag{4.4}
\]

正しい構造式は、任意の基点 \(\bar f_0\in\mathcal L_m\) に対し

\[
\boxed{
\Omega_b(m):=
\{\operatorname{ob}_b(\bar f):\bar f\in\mathcal L_m\}
=\operatorname{ob}_b(\bar f_0)+\lambda_m(K_m).
}
\tag{4.5}
\]

である。section を一つ選んだ値ではなく、この affine image が
系に固有の対象である。

### F4.1 一発の反例

\(m=3\) の開示 witness を mod \(4\) で書くと

\[
\bar f_3=(2,0,0,2,3,2,2,2,2,2,0,0,3,0,0)
\tag{4.6}
\]

で、(3.5) は \(\operatorname{ob}_b(\bar f_3)=1\) を返す。一方

\[
k_3=(0,0,0,0,0,0,3,2,2,3,0,0,1,0,0)\in K_3
\tag{4.7}
\]

であり、

\[
\operatorname{ob}_b(\bar f_3+k_3)=0.
\tag{4.8}
\]

従って \(m=3\) は「全線型解が障害非零」の系ではない。

逆方向も起こる。\(m=1\) の開示 witness

\[
\bar f_1=(3,3,3,0,0,0,2,1,1,2,0,0,0,0,0)
\tag{4.9}
\]

は ob \(=0\) だが、

\[
k_1=(0,1,1,3,3,3,1,0,0,1,0,0,0,0,0)\in K_1
\tag{4.10}
\]

を足すと ob \(=1\) になる。従って「13個以外では障害写像が零」
という読みも誤りである。

### F4.2 全可解剰余類での反転元

次の三ベクトルを (1.1) 順に置く。

\[
\begin{aligned}
k_+&=(0,0,0,0,0,0,1,2,2,1,0,0,3,0,0),\\
k_-&=(0,0,0,0,0,0,3,2,2,3,0,0,1,0,0),\\
k_1&=(0,1,1,3,3,3,1,0,0,1,0,0,0,0,0).
\end{aligned}
\tag{4.11}
\]

確定表への直接代入で次を得る。

| \(m\bmod16\) | \(K_m\) に入る元 | \(\lambda_m\) |
|---|---|---:|
| \(0,5,7,9,13\) | \(k_+\) | \(1\) |
| \(3,8,11,15\) | \(k_-\) | \(1\) |
| \(1\) | \(k_1\) | \(1\) |

これは (0.1) の可解な十剰余類を尽くす。従って
\(\lambda_m(K_m)=\mathbb F_2\) であり、(0.4) が従う。
各 fiber は同じ大きさなので、線型 mass は ob \(=0\) と ob \(=1\)
へ正確に半分ずつ分かれる。

現在見えている `certificates/e2c6/m6_j2_m*.json` の multiplicity
table も、可解40系全てについて

\[
\texttt{ob\_table}=\{\texttt{"0,0"}:|\mathcal L_m|/2,\
\texttt{"0,1"}:|\mathcal L_m|/2\},
\qquad
\texttt{all\_nonzero=false}
\tag{4.12}
\]

を記録しており、この紙上結論と一致する。

### F4.3 13個のリストの正体

初期 `sweep_j2_m*.json` が選んだ section
\(m\mapsto\bar f_m^{\rm cert}\) に対してだけ

\[
\operatorname{ob}_b(\bar f_m^{\rm cert})=1
\]

となる集合が、開示された

\[
\{3,5,11,21,27,35,37,45,51,53,57,59,61\}
\tag{4.13}
\]

である。系自体は mod \(16\) で同一なのに、例えば

\[
\begin{array}{c|cc}
&m&m+16\text{ または同剰余}\\ \hline
\operatorname{ob}_b(\bar f_m^{\rm cert})
&3:1&19:0\\
&11:1&43:0\\
&13:0&45:1\\
&9:0&57:1
\end{array}
\tag{4.14}
\]

となる。これは solver section が周期的に選ばれていないだけである。
したがって (4.13) に intrinsic な 2-adic 特徴付けを与えることは
できない。

便 22 の

\[
\bar f\text{ が full lift を持つ}
\iff\operatorname{ob}(\bar f)=0
\tag{4.15}
\]

を使うと、結論は次のとおりである。

\[
\boxed{
j=2,\ 0\le m<64:\quad
\text{full class-6 解あり}
\iff m\text{ 奇または }8\mid m .
}
\tag{4.16}
\]

「13個の fake 候補」はこの段階では一つも生じていない。

---

## F5. \(u_4\) 全零の理由と \(j=3\) の予言

(3.4) の

\[
(q_\theta)_{u_4}=-2f_p^2
\tag{5.1}
\]

が全てである。\(j=2\) の中心係数環は \(\mathbb F_2\) なので、
この成分は構造的に必ず零になる。13 witness の偶然ではない。

ただしこれは \(j=2\) 特有である。\(j=3\) では中心係数環は
\(R=\mathbb Z/4\) となり、

\[
\boxed{
\operatorname{ob}_a(\bar f)=2(f_p\bmod2)\,a,
\qquad
\text{\(a\)-bit}=f_p\bmod2 .
}
\tag{5.2}
\]

従って次の gate では \(u_4\) 成分が初めて見え得る。
ただし \(f_p\) が affine 線型解空間上で一定とはまだ示していないので、
(5.2) から \(m\) の封印リストを予言してはならない。\(j=3\) でも
一 witness ではなく、全線型 mass 上の像を調べる必要がある。

---

## F6. 実現ギャップを越える最小手順

今回のデータは最初の gate で止まる。有限許容対象へ進む前に必要な
system-level 条件は

\[
\mathcal L_m\ne\varnothing,\qquad
0\notin\operatorname{ob}(\mathcal L_m)
\tag{6.1}
\]

である。一個の非零 witness では (6.1) を証明しない。
本便では逆に \(0\in\operatorname{ob}(\mathcal L_m)\) を全40系で
証明した。

将来 (6.1) を満たす普遍 congruence 商が見つかった場合の最小昇格手順は
次である。

1. **affine-image gate**
   全線型解空間の obstruction image を決定し、零点不存在を
   kernel/mass 証明書で確定する。
2. **有限 equivariant realization**
   \(\theta,\tau,\sigma_m,E_m\) が降下する有限指数の
   \(B_3\)-安定な \(N\) を構成し、普遍 class-6 商との比較写像を作る。
3. **obstruction survival**
   中心核と障害群の比較図式を作り、非零 class が有限商で殺されないこと、
   また有限対象の解が普遍側の零点を強制することを示す。
4. **許容性 gate**
   \(N\) の normality、有限指数、admissibility、charming 性、
   marking と必要な GT-shadow 条件を検査する。
5. **群積と独立照合**
   presentation 上の直接群積で二方程式を再評価し、helper 非共有の
   第二照合器と一致させる。

この五段を通って初めて fake 候補、さらに E15 反例候補と呼べる。
並行中と開示された M8 直接再計算は本便では監査していないが、
仮に選択 witness の非零を再現しても F6.1 の欠落は埋まらない。

---

## F7. E15 の改訂案

「障害素数は \(3\)」「2群では E2 障害なし」という形は撤回すべきである。
代わりに、次の central-layer criterion を正本候補とする。

> **E15\(^\mathrm{layer}\) 候補。**
> \(\sigma,\theta\)-安定な中心列の各 kernel \(M_r\) について
> \[
> \tag{G2\(_r\)}M_r^\sigma=0,
> \qquad
> \tag{G3\(_r\)}
> \widehat H^0(\langle\theta\rangle,M_r)
> =M_r^\theta/(1+\theta)M_r=0
> \]
> が成立すれば、下位商の解は全中心列を通して持ち上がる。

便 19 の中央欠損補題を各層へ適用すれば、この条件付き言明は証明できる。
重要なのは二条件の由来を分けることである。

- class 5 の非自明 \(C_3\)-lattice では
  \(\det(1-\sigma)=3\) なので、\(p\ne3\) が (G2) を与えた。
- (G3) は素数 \(3\) の話ではなく、
  \(\langle\theta\rangle\)-lattice が induced かどうかの話である。
  同じ 2-primary でも class 6 で破れる。
- 一般には \(\sigma\)-自明成分があれば \(p\ne3\) でも (G2) は破れる。
  従って W139 は「該当する標準 lattice 上での \(p\ne3\)」と限定して
  読む必要がある。

class 6, \(p=2\) では障害群が非零で、障害写像も非零値を取る。
しかし像に零も含むため、これは E15 の反例ではない。
改訂後は「障害群の非消滅」「障害写像の非零」「零点不存在」を
三段階に分けて台帳化すべきである。

---

## F8. 状態札

| 主張 | 裁定 |
|---|---|
| 線型可解律 \(m\) 奇または \(8\mid m\) | **紙上 PASS** |
| 閉形式 \(\binom{m+1}{3}\equiv0\pmod4\) | **紙上 PASS** |
| \(m\) だけの \(\operatorname{ob}_b(m)\) | **不適切／存在しない** |
| 正式 \(\operatorname{ob}_b(m;\bar f)=f_{s_3}+f_wf_{r_2}\) | **紙上導出** |
| \(u_4\) bit 全零 at \(j=2\) | **紙上 PASS** |
| 開示13系が system-level obstruction | **棄却** |
| 可解40系の obstruction image | **全て \(\{(0,0),(0,1)\}\)** |
| \(j=2\) full 可解律 | **線型可解律と同じ** |
| \(j=3\) \(a\)-bit | **branch-wise に \(f_p\bmod2\)** |
| 有限許容 fake 候補 | **なし。実現 gate 以前に零点あり** |
| E15 反例 | **成立せず** |
| Lean verified | なし |

## ★ 教材

> **障害値が一つ非零であることと、障害方程式に零点がないことは別である。**
>
> 線型解空間が affine torsor のとき、正しい対象は選ばれた一点の値でなく
> \[
> \operatorname{ob}(\mathcal L_m)
> \]
> である。今回の写像は全可解系で二値へ全射だった。ゆえに
> 「初の非零値」は本物だが、「初の非可解障害」はまだ観測されていない。

---

## 監査範囲外申告

- ブラインド指定された `docs/委嘱17*` は読んでいない。
  `docs/対話帳.md` は T-8 までしか読まず、T-9 以降は不可視のままである。
- GAP、node、Python、Lean、および sweep script は実行していない。
  UTF-8 ファイルと JSON の読取り・表示には PowerShell を用いたが、
  掃引や証明書生成はしていない。
- 配達開示の 89/89 PASS と、現在の multiplicity certificate の内容は
  比較資料として採用した。独立 checker の再実行、証明書生成経路、
  M8 群積の監査はしていない。
- 有限許容 \(PB_3/N\) の構成、admissibility/charming 性、
  GT-shadow 条件、E15 の実対象への適用は本便の範囲外である。
- 本便で変更したのは `sol/sol_reply_23_first_light.md` のみである。
