# 影工房 便 27 返信 — 定理 \(K3\) 総合監査

## 総合判定

\[
\boxed{\textbf{条件付き PASS}}
\]

定理 \(K3\) の結論
\[
\operatorname{Ih}_{K^{(3)}}\twoheadrightarrow
\operatorname{GT}(K^{(3)})\cong S_3\times C_2,
\qquad
L_3=\mathbf Q(\zeta_{12},\sqrt[3]{2})
\]
は正しい。以下で与える修正を本文へ組み込めば、
**paper-proof / two-mathematician audit PASS** に上げてよい。
新しい計算仮定や外部文献待ちは生じない。

ただし `docs/week4-K3飽和_opus_v1.md` **現文のまま**は PASS ではない。
load-bearing な修正は二つある。

1. 補題 P(a) の stabilizer が誤っている。
   \(H\cap\langle\bar x\rangle=1\) だけでは
   \(\langle\bar x\rangle\) の \(\Lambda\) 上の自由性は出ない。
   ここでは B2 の \(N_{G_3}(H)=H\) が必要である。
2. 補題 P(d) の
   「\(S_6\) 内でともに不動点なしの \(C_3\) だから同一」
   は偽である。また (K4) の
   「Thm 4.3 のパラメータ表示が一意だから \(\Phi\) は単射」
   も論証になっていない。
   前者は包含と位数、後者は生成元像の直接計算で修理できる。

一方、§5 の \(R^{\mathrm{gen}}\) は現状では**定理として差戻し**である。
二事例を包む設計図としてはよいが、「\(\mathfrak F_0\)-成分」が未定義で、
比較射・円分商・translation 同定の仮定が不足している。

---

## F1. 補題 P(a) — 現証明は FAIL、B2 を入れれば PASS

有限商を \(G=G_3\) とし、選んだ指数 \(6\) 部分群を \(H\) とする。
点集合 \(G/H\) と共役部分群集合
\[
\Lambda=\{gHg^{-1}:g\in G\}
\]
の間の自然写像は
\[
G/H\longrightarrow\Lambda,\qquad
gH\longmapsto gHg^{-1}
\tag{1.1}
\]
であり、その非単射性を測るのは
\[
N_G(H)/H=\operatorname{Aut}_G(G/H)
\tag{1.2}
\]
である。

特に、\(\langle\bar x\rangle\) が \(H\in\Lambda\) を共役作用で固定する
stabilizer は
\[
\operatorname{Stab}_{\langle\bar x\rangle}(H)
=N_G(H)\cap\langle\bar x\rangle,
\tag{1.3}
\]
であって、一般には \(H\cap\langle\bar x\rangle\) ではない。
したがって v1 の
\[
H\cap\langle\bar x\rangle=1
\Longrightarrow
\langle\bar x\rangle\text{ が }\Lambda\text{ に自由に作用}
\]
は飛躍である。

しかし選択した class #2/#4 では
\[
\operatorname{Aut}(\text{dessin})
\cong N_G(H)/H=1
\]
が P2/B2 および `gap18a.json` により与えられている。従って
\[
N_G(H)=H,
\]
これを (1.3) に代入すれば stabilizer は自明である。
さらに
\[
|\langle\bar x\rangle|=|\Lambda|=6
\]
だから軌道は \(\Lambda\) 全体であり、
\[
\boxed{\langle\bar x\rangle\cong C_6
\text{ は }\Lambda\text{ に単純推移的に作用する。}}
\tag{1.4}
\]

従って補題 P(a) は、前件を
\[
N_G(H)=H,\qquad
H\cap\langle\bar x\rangle=1,\qquad
|\Lambda|=\operatorname{ord}(\bar x)=6
\]
と書き直せば PASS である。これは新仮定ではなく、既存の B2+B3 である。

---

## F2. 補題 P(b)(c) — Kummer 計算は PASS

\[
K=\mathbf Q(\zeta_{12}),\qquad u=-4.
\]
補題 C/D0/D/E/I3\(^{\ddagger}\) と FC-3 により、
接繊維と \(\Lambda\) の actual \(G_{\mathbf Q}\)-作用は一致する。
さらに \(G_K\) では
\[
\chi\equiv1\pmod {12},
\]
従って特に \(\chi\equiv1\pmod6\) であり、
\(C_6\)-torsor \(\Lambda\) 上の線形部は消える。
作用は Kummer character
\[
\kappa_{u^{-1}}:G_K\longrightarrow\mu _6
\tag{2.1}
\]
による translation になる。

ここで「像が Kummer 類で生成される」という文言は、
厳密には「(2.1) が表す cohomology class が
\([u^{-1}]_6\in K^\times/K^{\times6}\) である」と書くべきである。
\(\mu _6\subset K\) なので
\[
\operatorname{ord}([u^{-1}]_6)=|\operatorname{im}\kappa_{u^{-1}}|.
\tag{2.2}
\]

位数計算は v1 の結論どおりである。より短く直接には
\[
-1=\zeta_{12}^{\,6},\qquad
[-4]_6=[4]_6,
\]
かつ
\[
[4]_6^3=[64]_6=[2^6]_6=1.
\]
もし \([4]_6=1\) なら、ある \(a\in K\) が \(a^6=4\) を満たし、
\[
a^3=\pm2
\]
だから \(\sqrt[3]{2}\in K\) となる。しかし
\[
[\mathbf Q(\sqrt[3]{2}):\mathbf Q]=3\nmid
[K:\mathbf Q]=4
\]
で矛盾する。従って
\[
\boxed{\operatorname{ord}([-4]_6)
=\operatorname{ord}([u^{-1}]_6)=3.}
\tag{2.3}
\]

2-primary 成分を明示的に見るなら
\[
-4=(2i)^2\in K^{\times2}
\tag{2.4}
\]
なので自明であり、3-primary pushout は
\[
[u^{-1}]_3=[-4]^{-1}_3=[2^2]^{-1}_3\ne1.
\tag{2.5}
\]
従って local image は余分な \(C_2\) を含まず、ちょうど \(C_3\) である。
合成数 \(M=6\) に対する必要な監査はここで支払われている。

v1 の「\([2]\) の位数は \(6\)」も正しいが、定理には不要である。
必要なのは直接 (2.3) だけであり、こちらの方が失敗様式が少ない。

---

## F3. 補題 P(d)(e) — (d) の理由は FAIL、(e) で完全修理

### F3.1 捨てるべき論証

\(S_6\) には cycle type \(3^2\) の \(C_3\) が多数ある。
例えば
\[
\langle(1\,2\,3)(4\,5\,6)\rangle,\qquad
\langle(1\,2\,4)(3\,5\,6)\rangle
\]
はともに不動点なしだが、同じ部分群ではない。

従って

> Kummer 像と \(\mathfrak F_0\) 像がともに不動点なしの \(C_3\)  
> \(\Longrightarrow\) 同一

は成立しない。「\(C_6\) の位数 \(3\) 部分群は一意」という事実を使うには、
\(\mathfrak F_0\) の像も**同じ regular \(C_6\)** の中に入ることを
先に示す必要がある。v1 はそれを示していない。

### F3.2 正しい一行修理

\[
T:=\operatorname{GT}(K^{(3)}),\qquad
\mathfrak F_0:=\ker\widetilde\chi\cong C_3,
\]
また \(\rho_\Lambda:T\to\operatorname{Sym}(\Lambda)\) を
\(\Lambda\) 上の作用とする。

\(G_K=\ker(\chi\bmod12)\) だから
\[
\operatorname{Ih}(G_K)\le\mathfrak F_0.
\tag{3.1}
\]
一方 F2 により
\[
|\rho_\Lambda(\operatorname{Ih}(G_K))|=3.
\tag{3.2}
\]
【GAP-18a】は
\[
\rho_\Lambda|_{\mathfrak F_0}
\text{ が忠実}
\tag{3.3}
\]
と与えるので
\[
|\rho_\Lambda(\mathfrak F_0)|=3.
\]
(3.1)–(3.3) から直ちに
\[
\boxed{
\rho_\Lambda(\operatorname{Ih}(G_K))
=\rho_\Lambda(\mathfrak F_0),
\qquad
\operatorname{Ih}(G_K)=\mathfrak F_0.
}
\tag{3.4}
\]

これは v1 (e) の包含を先に使った証明であり、
\(S_6\) 内の共役型や「同じ \(C_6\)」の同定を一切要しない。
従って補題 P の正しい論理順は
\[
\boxed{(a')\to(b)\to(c)\to(e\text{ の包含})\to(d'\text{ の位数比較})}
\]
である。

### F3.3 2-成分は本当に円分側で埋まる

次の完全列を使う。
\[
1\longrightarrow\mathfrak F_0\cong C_3
\longrightarrow T
\xrightarrow{\widetilde\chi}
(\mathbf Z/12)^\times\cong C_2^2
\longrightarrow1.
\tag{3.5}
\]
\(A:=\operatorname{Ih}(G_{\mathbf Q})\) と置くと、円分指標の全射性より
\[
\widetilde\chi(A)=(\mathbf Z/12)^\times.
\tag{3.6}
\]
また (3.4) より
\[
A\cap\mathfrak F_0=\operatorname{Ih}(G_K)=\mathfrak F_0.
\tag{3.7}
\]
従って
\[
|A|=|A\cap\mathfrak F_0|\,
|\widetilde\chi(A)|
=3\cdot4=12=|T|,
\]
すなわち
\[
\boxed{A=T.}
\tag{3.8}
\]

これが「2-primary は円分側で吸収される」の厳密な意味である。
degree \(6\) の local torsor に位数 \(6\) を要求する必要はない。
要求されるのは kernel \(C_3\) を埋めることだけであり、
商 \(C_2^2\) は独立に円分指標が埋める。

なお (3.8) は \(\Phi\) の単射性を使わない。
従って全射性の証明から (K4) を外すと、依存関係はさらに強くなる。

---

## F4. (K4) \(\Phi\) の単射性 — 現理由は FAIL、主張自体は紙上 PASS

「GT-shadow のパラメータ表示が一意」と
「それが \(G_3\) に誘導する自己同型が一意」は別問題である。
異なる shadow が同じ有限群自己同型を与える可能性を排除しなければならない。
これは \(A_5\) 戦で警戒した罠そのものである。

本件は生成元像を直接計算すれば閉じる。\(D_3\) で
\[
r^3=s^2=1,\qquad srs=r^{-1},
\]
\[
\bar x=(r,s,s),\qquad
\bar y=(rs,r,rs),
\]
\[
f_{m,k}=(r^{2k},r^{-2k},r^{\kappa(m)}),\qquad
u_m=2m+1
\]
とする。定義式
\[
\Phi_{m,k}(\bar x)=\bar x^{u_m},\qquad
\Phi_{m,k}(\bar y)=f_{m,k}^{-1}\bar y^{u_m}f_{m,k}
\]
から、\(u_m\) は奇数なので
\[
\Phi_{m,k}(\bar x)=(r^{u_m},s,s),
\tag{4.1}
\]
\[
\Phi_{m,k}(\bar y)
=
\left(
r^{1-4k}s,\ r^{u_m},\ r^{1-2\kappa(m)}s
\right)
=
\left(
r^{1-k}s,\ r^{u_m},\ r^{1-2\kappa(m)}s
\right)
\tag{4.2}
\]
（指数は mod \(3\)）。

charming な \(m\) について
\[
\begin{array}{c|c|c|c}
m&u_m\bmod3&\kappa(m)\bmod3&
r^{1-2\kappa(m)}s\\ \hline
0&1&0&rs\\
2&2&1&r^2s\\
3&1&1&r^2s\\
5&2&0&rs
\end{array}
\tag{4.3}
\]
である。
従って (4.1) と (4.2) の第三成分の組が \(m\) を一意に決める。
さらに (4.2) の第一成分
\[
r^{1-k}s\qquad(k=0,1,2)
\]
は \(rs,s,r^2s\) と相異なるので \(k\bmod3\) も一意に決まる。

よって 12 個の \((m,k)\) は 12 個の相異なる自己同型を与え、
\[
\boxed{\Phi:T\hookrightarrow\operatorname{Aut}(G_3)
\text{ は単射。}}
\tag{4.4}
\]

【GAP-K3a】はこの紙上計算で閉じてよい。
機械検算を足すなら補助証拠であり、数学的残件ではない。

---

## F5. 窓非依存 import の監査

| 部品 | 判定 | \(K^{(3)}\) で追加確認する点 |
|---|---|---|
| 補題 C | **PASS** | \(\mathbf P^1-\{0,1,\infty\}\)、二つの接基点、標準実経路だけの命題。\(M\)、\(H\)、有限商を使わない |
| 補題 D0 | **PASS** | 自由副有限群 \(\widehat F_2\) の中心化群命題だけ。窓非依存 |
| 補題 D・系 E | **PASS** | 正準 outer action の \(\widehat F_2'\)-正規化持ち上げの一意性。有限商を使わない |
| I3\(^{\ddagger}\) | **PASS** | paper Ihara action 自体についての source-closed statement。\(N_A\) 固有ではなく、任意の有限 quotient へ落とせる |
| FC-3 | **条件を明記して PASS** | 「次数に依らない」は正しい。ただし \(W_0/\mathbf Q\) の存在、幾何連結性、stabilizer map の全単射性が要る。K3 では P4/P7 と \(N_G(H)=H\) がこれを供給 |
| 局所 Kummer | **PASS** | \(\lambda=us^6\)、\(\mu_6\subset K\)、全分岐一点という前件が K3 で成立 |

非忠実な 6 点表現は import を壊さない。
FC-3 が使うのは \(\widehat F_2\) の有限推移集合と点 stabilizer であり、
その作用核が非自明でもよい。

ここで区別すべき二つの \(C_3\) がある。

- 6 点表現 \(G_3\to S_6\) の**幾何 monodromy kernel**（位数 \(3\)）。
- \(\mathfrak F_0\le\operatorname{GT}(K^{(3)})\le\operatorname{Aut}(G_3)\) という
  **shadow automorphism group**。

前者が非自明でも後者が \(\Lambda\) 上で忠実なら検出器は生きている。
【GAP-18a】はまさに後者の忠実性を測っている。

---

## F6. P1–P7 の監査

### P1 — 次数 6・非忠実表現

**PASS。**
便 24 の B2/B5 FAIL は「最小忠実次数 12」の作用についての判定であり、
本稿は明示的に別の指数 \(6\) 部分群を選んでいる。
次数 6 側では
\[
N_G(H)=H,\quad |\Lambda|=6,\quad
\rho_\Lambda|_{\mathfrak F_0}\text{ faithful}
\]
が成立するので、次数 12 側の residual \(C_3\)-descent は生じない。

### P2 — B1–B5

**修文後 PASS。**

- B1 は ordered generating pair の stabilizer が自明なので、
  \(1296/|\operatorname{Aut}(G_3)|=1\) の軌道計算は正しい。
- B2/B3 は選択した degree-6 representation について PASS。
- B4 は \(\mathfrak F_0\cong C_3\) として PASS。
- B5 は「不要」ではなく、
  **3-primary kernel と 2-primary cyclotomic quotient を分離した**
  と書くべきである。F3.3 がその厳密な代替証明である。

### P3 — 一意性

**定理には不要。記録の修正が必要。**

`gap18a.json` は良い側を二つの \(G_3\)-共役類 #2/#4
（各 6 個、計 12 個）、悪い側を #1/#3
（各 3 個、計 6 個）として分けている。
良い 12 個が一つの \(\operatorname{Aut}(G_3)\)-軌道という限定主張は
委嘱 20 の意図と整合する。

しかし委嘱 20 §2 の

> orbit size 18、うち cent \(=1\) が 12

という文はそのままでは不可能である。任意の
\(\varphi\in\operatorname{Aut}(G)\) について
\[
N_G(\varphi(H))/\varphi(H)
\cong N_G(H)/H
\tag{6.1}
\]
だから、dessin automorphism の位数 \(1\) と \(2\) は
同じ Aut-orbit 内で混ざらない。

従って本文では「良い #2/#4 の 12 個が一軌道」とだけ書き、
「18 個全体が一軌道」は削除すべきである。
いずれにせよ P4 の exact conjugator が選んだ \(H\) を直接同定するため、
全体軌道の一意性は主証明の前件ではない。

### P4 — exact conjugator

**PASS。**
\[
h=[6,1,5,4,2,3]
\]
による
\[
h\bar xh^{-1}=\sigma_1,\quad
h\bar yh^{-1}=\sigma_\infty,\quad
h\bar zh^{-1}=\sigma_0
\]
は ordered passport を揃えた actual marking の証明書であり、
passport・群位数だけの同定より強い。三本目が独立検査である点もよい。

### P5 — 平面モデルと分岐

**PASS。**
\[
F=t^2+(x-1)^2(4x-1)t+4x^6
\]
について
\[
t=0:(6),\qquad t=-1:(2^21^2),\qquad t=\infty:(6)
\]
および \(x=1/3,t=-2/27\) が正規化上の分岐点でなく
平面モデルの node であるという分離は正しい。
\(P_0=(0,0)\) では \(F_t=-1\ne0\) なので \(x\) は uniformizer である。

### P6 — 接方向 rigidification

**本件では不要。一般補題の文言だけ修正。**
委嘱 18 の

> \(p\) を固定する deck 変換は接直線に原始 \(M\) 乗根で作用する

は強すぎる。合成数 \(M\) では非生成元は非原始根で作用する。
正しい主張は

> characteristic \(0\) の有限 automorphism group では、
> 点 stabilizer の接直線への作用は faithful。
> 従って非零接ベクトルまで固定する元は恒等元。

である。結論は保たれるが、degree \(6\) 標的はそもそも
\(\operatorname{Aut}=1\) なので P6 を主証明から外してよい。

### P7 — 残留 descent

**PASS。**

- 曲線と写像が \(\mathbf Q\) 上。
- \(\lambda=0\) 上は唯一の滑らかな点 \(P_0=(0,0)\)。
- \(x\) は \(\mathbf Q\)-有理 uniformizer。
- \(N_G(H)/H=1\)。
- P4 が actual marking を固定。

従って degree-12 側の「二つの cusp を Galois が交換する」問題も、
deck twist も残らない。ここでは induced module は不要である。

---

## F7. \(u\) 両翼の記載

数値と数学内容は一致している。
\[
\boxed{u=-4,\qquad [u]_3=[2^2]\ne1.}
\]

- Opus 経路は分岐値・node の除外・exact conjugator・もう一つの
  全分岐 cusp での正規化比較まで行う。
- Sol 便 25 は \(P_0\) での局所 implicit expansion と
  \([u^{-1}]_3\) の向きを中心に行う。

従って「役割が相補的」という記述は正しい。
ただし便 25 自身が、計算後とはいえ Opus checker を開き、
そのヘッダ内の \(u\) と mod \(3\) 判定を見たと申告している。
ゆえに

\[
\boxed{\text{「両翼一致」は可、厳密な「blind 独立二系統」は不可。}}
\tag{7.1}
\]

v1 冒頭・§3・状態札の「両翼独立一致」は
「二者の紙上経路が一致（ただし便 25 は途中で独立性汚染を自己申告）」
へ修正すべきである。これは状態札の問題で、数値結論には影響しない。

また §3 の

> 意味のある Möbius 正規化は 2 通りで尽き、残り 4 通りは
> 非全分岐点を \(0\) に置く

は字義どおりには誤りである。6 通り中、全分岐点を \(0\) に置くものは
4 通りある。そのうち **ordered passport
\((6,2^21^2,6)\) を保つものが 2 通り**であり、
残る全分岐 2 通りは passport order を
\((6,6,2^21^2)\) に変える。
本定理が固定した marking に必要なのは前者 2 通りなので、
結論は変わらないが、説明はこのように限定すべきである。

---

## F8. 主定理と固定体

### F8.1 全射性

全射性は F3.3 の核・商の議論だけで従う。
\[
\operatorname{Ih}(G_K)=\mathfrak F_0,\qquad
\widetilde\chi(\operatorname{Ih}(G_{\mathbf Q}))
=(\mathbf Z/12)^\times
\]
だから
\[
\operatorname{Ih}_{K^{(3)}}(G_{\mathbf Q})
=\operatorname{GT}(K^{(3)}).
\]
(K4) はこの段には不要である。

### F8.2 固定体

F4 により \(\Phi\) は単射であり、【GAP-18a】により
\(\mathfrak F_0\) は \(\Lambda\) 上忠実である。従って
\[
\Phi(\operatorname{Ih}(\gamma))=1
\]
であることは、次の二条件と同値である。

1. \(\chi(\gamma)\equiv1\pmod {12}\)、すなわち
   \(\gamma\) が \(K=\mathbf Q(\zeta_{12})\) を固定する。
2. \(G_K\) 上の Kummer character \(\kappa_{u^{-1}}\) が零、
   すなわち \(\gamma\) が
   \[
   K\bigl((u^{-1})^{1/6}\bigr)
   \]
   を固定する。

\(-1\in K^{\times6}\) かつ \(u=-4\) なので
\[
K\bigl((u^{-1})^{1/6}\bigr)
=K(2^{-1/3})=K(\sqrt[3]{2}).
\tag{8.1}
\]
従って
\[
\boxed{
\operatorname{Fix}\ker(\Phi\circ\operatorname{Ih})
=L_3=\mathbf Q(\zeta_{12},\sqrt[3]{2}).
}
\tag{8.2}
\]

\(\sqrt[3]{2}\notin K\) より
\[
[L_3:\mathbf Q]=4\cdot3=12.
\]
\(K\) は \(\mu _3\) を含むので \(L_3/K\) は cyclic cubic で、
\((\mathbf Z/12)^\times\) の mod \(3\) 作用は
\[
\{1,7\}:\text{自明},\qquad
\{5,11\}:\text{反転}.
\]
従って
\[
\operatorname{Gal}(L_3/\mathbf Q)
\cong C_3\rtimes(C_2\times C_2)
\cong S_3\times C_2,
\tag{8.3}
\]
であり、D1 Thm 4.6 の
\(\operatorname{GT}(K^{(3)})\cong
\operatorname{Aff}(\mathbf Z/3)\times\mathcal Z_2\)
と一致する。

---

## F9. \(R^{\mathrm{gen}}\) — 定理としては差戻し

現言明の最大の問題は

> \([u]\) の \(\mathfrak F_0\)-成分

が一般には定義されていないことである。
\(\mathfrak F_0\) が \(\Lambda\) 上忠実というだけでは、
その像が regular \(C_M\) の translation subgroup に入るとも、
\(\mathfrak F_0\) が巡回とも限らない。
補題 P(d) が踏んだ穴を一般定理へ持ち込んでいる。

少なくとも次を前件に加える必要がある。

1. \[
   1\to\mathfrak F_0\to\operatorname{GT}(N)
   \xrightarrow{\widetilde\chi}(\mathbf Z/2M)^\times\to1
   \]
   と
   \(\widetilde\chi\circ\operatorname{Ih}=\chi_{2M}\)。
2. \(\mathfrak F_0\cong C_e\)、\(e\mid M\)。
3. \(\operatorname{ord}(X)=|\Lambda|=M\)。
4. explicit \(\mathbf Q\)-model、\(\mathbf Q\)-有理な全分岐 cusp、
   actual marked identification。
   \(\operatorname{Aut}=1\) だけでは field of moduli が
   \(\mathbf Q\) であることは出ない。
5. FC-2b/FC-3 による actual Galois action と tangential fiber の比較。
6. 指定した pushout
   \[
   q:\mu_M\twoheadrightarrow\mu_e
   \xrightarrow{\sim}\mathfrak F_0
   \tag{9.1}
   \]
   が、\(\mathfrak F_0\) の \(\Lambda\) 上の作用と一致すること。

この形なら正しい族命題は
\[
\operatorname{Ih}_N\text{ 全射}
\iff
q_*[u^{-1}]_M=[u^{-1}]_e
\text{ が }H^1(G_K,\mu_e)\text{ で位数 }e
\tag{9.2}
\]
となり、全射時の固定体は
\[
K(u^{1/e})
\]
（逆元・\((\mathbf Z/e)^\times\) 乗は同じ体）である。

\(A_5\) では \(M=e=5\)、\(K^{(3)}\) では \(M=6,e=3\) として
(9.1) が実際に構成される。従って二事例を包む骨格は正しいが、
現 v1 の T1–T3 だけからは (9.2) は出ない。

提案する状態札は

\[
\boxed{
R^{\mathrm{gen}}=\text{「定理」ではなく比較スキーマ};
\quad
R^{\mathrm{cyc}}=\text{上記 1--6 を前件にした定理候補}.
}
\]

---

## F10. 根基 \(2\) の観察

現時点で
\[
A_5:\ q_*[u]=[2]^4,\qquad
K^{(3)}:\ q_*[u]=[2]^2
\]
という二点があることは記録価値がある。しかし二点は

- 素数/合成数、
- 合同/非合同、
- 非可解/可解

の全てで対極にあり、ここから族則を予測する機構はまだない。
従って §6 の「予測として登録しない」という判断に同意する。

安価に事前登録するなら、法則ではなく次の**観測列**に留めるべきである。

> 各新規 \(R^{\mathrm{cyc}}\) 窓について、
> \(q_*[u]\in K^\times/K^{\times e}\) が
> \(\langle[2]\rangle\) に入るかを盲検で記録する。
> \(2\) 以外の素点で valuation が \(e\) の倍数でない一例が出れば
> 「根基 2」候補は即棄却する。

三つ以上の独立な新規窓で残ってから初めて
\[
\mathrm{(G7_{rad2})}\qquad q_*[u]\in\langle[2]\rangle
\]
を予測候補へ上げるのが安全である。

---

## 修正必須・推奨

### 必須

- **P1**: 補題 P(a) に \(N_G(H)=H\) を明示投入し、F1 の証明へ交換。
- **P2**: 補題 P(d) の「\(S_6\) 内の同じ \(C_3\)」を削除し、
  F3.2 の包含+位数比較へ交換。
- **P3**: (K4) を F4 の生成元像計算へ交換。
- **P4**: 主定理の全射証明を F3.3 の kernel/quotient proof に交換。

### 推奨

- **P5**: P3 の orbit 記録を「良い 12 個」に限定し、
  不可能な「18 個の同一 orbit 内で Aut 位数が 1/2」を削除。
- **P6**: P6/B2\(^{\prime}\) の「原始根」を「faithful tangent action」へ修正。
- **P7**: 「両翼独立一致」を、便 25 の自己申告に沿って
  「二者一致・厳密な blind independence なし」へ修正。
- **P8**: Möbius 2 通りを
  「ordered passport \((6,2^21^2,6)\) を保つ 2 通り」
  と限定。
- **P9**: \(R^{\mathrm{gen}}\) を比較スキーマへ降格し、
  F9 の前件を備えた \(R^{\mathrm{cyc}}\) を別途起案。

---

## Warnings

- **W1**: coset stabilizer \(H\) と、共役部分群 stabilizer \(N_G(H)\) を
  取り違えない。stabilizer map が全単射なのは self-normalizing のときだけ。
- **W2**: permutation cycle type は部分群を同定しない。
  \(S_6\) の fixed-point-free \(C_3\) は一意でない。
- **W3**: 「shadow parameter の一意性」と
  「有限商への automorphism の単射性」を分ける。
- **W4**: B2/B3/B5 は窓だけでなく permutation representation ごとの判定。
- **W5**: \(\operatorname{Aut}=1\) は descent obstruction を消すが、
  field of moduli \(=\mathbf Q\) を単独では与えない。
  本件では explicit \(\mathbf Q\)-model と exact marking が別途ある。
- **W6**: 合成数 \(M\) では「local torsor 全体を推移的にすること」と
  「GT kernel の必要な primary 成分を埋めること」を区別する。
- **W7**: 経路が異なることと blind independence は同義でない。

---

## ★ 教材

1. **包含があるなら、共役型で同定せず位数を数える。**
   補題 P は
   \(\operatorname{Ih}(G_K)\le\mathfrak F_0\) と両者の位数 \(3\)
   だけで閉じる。
2. **合成数 torsor は primary に分け、群拡大の核と商へ対応させる。**
   今回は \(C_3\) を Kummer、\(C_2^2\) を cyclotomic が埋める。
3. **非忠実な幾何表現でも検出器になり得る。**
   必要なのは元の有限群の忠実作用でなく、
   求める shadow kernel の \(\Lambda\) 上の忠実性である。
4. **一般定理では「成分」という語を写像にする。**
   \(\mathfrak F_0\)-成分と書く代わりに
   \(q:\mu_M\twoheadrightarrow\mathfrak F_0\) をデータとして置く。

---

## 最終状態札

| 項目 | 裁定 |
|---|---|
| 補題 P v1 | **現文 FAIL、F1–F3 で無条件修理可能** |
| (K4) \(\Phi\) 単射 | **主張 PASS、現理由 FAIL、F4 で紙上閉鎖** |
| C/D0/D/E/I3\(^{\ddagger}\) import | **PASS** |
| FC-3 の次数非依存 | **PASS（self-normalizing・\(\mathbf Q\)-model 前件を明記）** |
| degree-6 選択 | **PASS** |
| P7 descent | **PASS** |
| \(u=-4\)、3-primary 位数 3 | **PASS** |
| 固定体 \(L_3\) と Galois 群 | **PASS** |
| 定理 \(K3\) | **修文後 paper-proof / mutual-audit PASS** |
| 現 v1 | **条件付き PASS** |
| \(R^{\mathrm{gen}}\) | **定理として差戻し・比較スキーマとして保持** |
| Lean verified | **なし** |

