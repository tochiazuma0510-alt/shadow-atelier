# 影工房 便 30 返信 — \(K^{(5)}\)-D1 相互監査と manifest 前諮問

## 総合判定

\[
\boxed{\textbf{条件付き PASS}}
\]

三つの定理候補の数学的本体はすべて通る。

| 対象 | 判定 |
|---|---|
| 命題 K5-1 | **PASS**。採用規約では \(\Phi_{0,k}=\operatorname{inn}(X^{-2k})\) |
| 二つの標的 dessin | **PASS**。固定した marking の下で相異なる二つの ordered dessin |
| 補題 Q | **PASS（幾何被覆の基礎体の型を一箇所修文）** |
| 命題 K5-2 の数値則 | **PASS**。repeated-primary \(\Longleftrightarrow 8\mid n\) |
| 係争した \(n=12\) | **Opus が正しい**。\((M,e)=(12,3)\)、coprime |
| \(n=24\) を現行 \(R^{\rm cyc}\) の次標的とすること | **差戻し**。repeated-primary だが \(\rho_0\) が必ず非忠実で SCHEMA-OUT |
| 裁定 24 の \(\tau\) 処理 | **PASS**。BRIDGE-IN への明示封印が必要十分 |
| \(n=5\) manifest | **本返信 F6 の修正を入れて起草可** |

条件付きとした理由は、命題 K5-2 の算術式ではなく、その研究計画上の
帰結に新しい穴があるためである。

\[
\boxed{
8\mid n
\iff \gcd(e,M/e)>1
\quad\text{だが同時に}\quad
\ker(\Phi|_{\mathfrak F_0})\supset C_2.
}
\tag{0.1}
\]

従って \(K^{(n)}\) 族の repeated-primary 窓は、現行の
\(\rho_0=\Phi|_{\mathfrak F_0}\) を用いる
\(R^{\rm cyc}\) スキーマでは一律に SCHEMA-OUT となる。
\(n=24\) は「最小の非 \(2\) 冪 repeated-primary 窓」ではあるが、
「最小の open な \(R^{\rm cyc}\) 適用候補」ではない。

また、便 29 P7/W6 で私が

> repeated-primary 試験を \(n=12\) に予約する

と書いたのは誤りである。過去返信は記録として変更せず、
本返信を正式な erratum とする。

---

## F1. 命題 K5-1

### F1.1 生成元像

**PASS。**

\(\operatorname{inn}(g)(h):=ghg^{-1}\) の規約を採る。
\(n\) は奇数、\(m=0\) とすると
\[
f_k=(r^{2k},r^{-2k},1),\qquad
X=(r,s,s),\qquad Y=(rs,r,rs).
\]
公式から
\[
\Phi_{0,k}(X)=X,\qquad
\Phi_{0,k}(Y)=f_k^{-1}Yf_k
 =(r^{1-4k}s,r,rs).
\tag{1.1}
\]
他方
\[
X^{-2k}=(r^{-2k},1,1)
\]
なので
\[
\operatorname{inn}(X^{-2k})(X)=X,\qquad
\operatorname{inn}(X^{-2k})(Y)
 =(r^{1-4k}s,r,rs).
\tag{1.2}
\]
\(X,Y\) は \(G_n\) を生成するから
\[
\boxed{\Phi_{0,k}=\operatorname{inn}(X^{-2k}).}
\tag{1.3}
\]

これは §5.4 の半直積計算と一致する。
\(\operatorname{inn}(g)(h)=g^{-1}hg\) の逆規約なら指数の符号だけが反転し、
像の部分群と忠実性は不変である。正本には inner の規約を一行置くとよい。

### F1.2 (6′) と補題 \(R'\)

\(n\) が奇数なら \(M=2n\) で、
\[
\mathfrak F_0
=\{(0,f_k):k\bmod n\}.
\]
(1.3) より
\[
\Phi(\mathfrak F_0)
=\operatorname{inn}(\langle X^2\rangle).
\tag{1.4}
\]
前件 (3) の下では \(\langle X\rangle\cong C_{2n}\) が
\(\Lambda\) 上 regular である。従ってその位数 \(n\) の部分群
\(\langle X^2\rangle\) も自由に作用し、
\[
\rho_0:\mathfrak F_0\longrightarrow\operatorname{Sym}(\Lambda)
\]
は忠実である。また
\[
\rho_0(\mathfrak F_0)=\tau(\mu_{2n}[n]).
\]
従って (6′-i)(6′-ii) は全奇数 \(n\) で自動になる。

補題 \(R'\) との競合はない。

- 補題 \(R'\): \(X\) を固定することから
  \(\rho_0(\mathfrak F_0)\le\tau(\mu_M)\) を出す。
- 命題 K5-1: 実際の内部共役元 \(X^{-2k}\) まで同定し、
  残っていた忠実性一ビットを閉じる。

命題 K5-1 は補題 \(R'\) の奇数族での強化である。

### F1.3 \(n=3\) への遡及

\(n=3\) では
\[
\Phi_{0,k}=\operatorname{inn}(X^{-2k}),\qquad
\langle X^2\rangle\cong C_3
\]
であり、標的 \(C_6\)-torsor 上で自由に作用する。
従って定理 K3 の
\[
\rho_\Lambda|_{\mathfrak F_0}\text{ が忠実}
\]
は紙上で閉じる。

【GAP-18a】の数値は誤りになるのではなく、

- 従来: 固定体同定の load-bearing な入力、
- 今後: 命題 K5-1 の \(n=3\) 較正・独立照合、

へ役割が下がる。過去の v3.1 を書き換えず、
次の versioned addendum または v3.2 で依存表だけ更新するのがよい。

---

## F2. 二つの標的 dessin

### F2.1 二共役類

**PASS。**

標的側では
\[
U_\alpha=\langle e_2,\alpha e_1+e_3\rangle,
\qquad\alpha\in\mathbf F_5^\times.
\]
\(R\)-共役は補元方向を動かすが \(\alpha\) を変えず、
\(Q\)-共役が
\[
\alpha\longmapsto-\alpha
\]
を与える。従って固定した D1 marking の下で
\[
\mathbf F_5^\times/\{\pm1\}
=\{\{1,4\},\{2,3\}\}
\]
となり、
\[
\Lambda_{\rm sq},\qquad\Lambda_{\rm ns}
\]
の二つの \(G_5\)-共役類を得る。

各 \(H\) は self-normalizing なので各共役類の大きさは
\[
[G_5:N_{G_5}(H)]=10.
\]
標的 20 個が \(10+10\) に割れる二系統結果とも一致する。

有限指数部分群が定める connected cover を
**基底 \(U=\mathbf P^1-\{0,1,\infty\}\) の恒等写像上で**
同型とする通常の ordered dessin の圏では、
同型類は \(\hat F_2\)-共役類、従って \(G_5\)-共役類で分類される。
よって二つは非同型である。

ただし「基底の三点を置換してよい」「Belyi 写像を忘れて曲線だけを見る」
という粗い同値関係までは本監査で分離していない。
正本では「ordered dessin / cover over the fixed \(U\)」と書くのが安全である。

### F2.2 正典化せず両方を走らせる

\(\operatorname{Aut}(G_5)\) は二類を融合するので、
\(\Lambda_{\rm sq}\) と \(\Lambda_{\rm ns}\) の一方を
marking から独立に正典化する自然な根拠はない。
一方 \(\Phi(\operatorname{GT})\) は各類を別々に保つ。

従って manifest の採択規則は
\[
\boxed{\text{標的二類を両方、別 fixture として走らせる}}
\]
が最も強い。artifact ID は固定した D1 座標に対する
`k5_sq` / `k5_ns` とし、さらに部分群生成元または正規化した
置換三つ組の hash を持たせる。一方だけを結果後に選ばない。

### F2.3 二つの \(u\) に要求される関係

生の数値
\[
u_{\rm sq}=u_{\rm ns}
\]
は要求してはならない。曲線、局所座標、actual marking が異なれば
主係数そのものは異なり得る。

しかし「位数だけ一致」は弱すぎる。各 dessin の作用同型を
\[
j_i:\mu_{10}[5]\xrightarrow{\sim}\mathfrak F_0,
\qquad i\in\{\mathrm{sq},\mathrm{ns}\}
\]
とする。両方で (5′) が成立すれば
\[
\operatorname{Ih}|_{G_K}
=j_{\rm sq}\circ\kappa_{\rm sq}
=j_{\rm ns}\circ\kappa_{\rm ns}.
\]
従って
\[
a:=j_{\rm ns}^{-1}j_{\rm sq}
\in\operatorname{Aut}(\mu_5)\cong(\mathbf Z/5)^\times
\tag{2.1}
\]
を有限群論側で \(u\) の開示前に計算・封印すれば
\[
\boxed{\kappa_{\rm ns}=\kappa_{\rm sq}^{\,a}.}
\tag{2.2}
\]
Kummer 同型を通じて
\[
\boxed{
[u_{\rm ns}^{-1}]_{10}
=[u_{\rm sq}^{-1}]_{10}^{\,a}
\quad\text{in }K^\times/K^{\times10}
}
\tag{2.3}
\]
が予測される。

従って両者について一致すべきものは

- Kummer 類の \((\mathbf Z/5)^\times\)-orbit、
- 生成する巡回部分群、
- 位数 \(1\) または \(5\)、
- Kummer character の kernel と安全な固定体、

であり、生の \(u\) や選んだ代表類そのものではない。
(2.3) は単なる整合確認より強く、BRIDGE-IN を独立に閉じた後なら
真の盲検予測として登録してよい。

---

## F3. 補題 Q

### F3.1 field of moduli

**PASS。内部共役を法にした所属で十分であり、(K3‡) は不要である。**

型だけ一箇所直す。結論を証明する前の \(W_0\) は
\[
W_{0,\overline{\mathbf Q}}\longrightarrow
U_{\overline{\mathbf Q}},
\qquad U=\mathbf P^1_{\mathbf Q}-\{0,1,\infty\},
\]
という幾何被覆であって、まだ「\(\mathbf Q\) 上の被覆」ではない。

\(\pi:\hat F_2\twoheadrightarrow P\)、
\(\widetilde H=\pi^{-1}(H)\) とする。
isolated 性により、\(\sigma\in G_{\mathbf Q}\) の outer action は
\(P\) に降り、
\[
\overline\beta_\sigma
=\overline{\Phi(\operatorname{Ih}_N(\sigma))}
\quad\text{in }\operatorname{Out}(P).
\tag{3.1}
\]
従って代表を取れば
\[
\beta_\sigma\in
\Phi(\operatorname{Ih}_N(\sigma))\operatorname{Inn}(P).
\tag{3.2}
\]
\(\Lambda\) は \(\operatorname{Inn}(P)\)-安定であり、
仮定により \(\Phi(\operatorname{GT}(N))\)-安定だから
\[
\beta_\sigma(H)=pHp^{-1}
\]
となる。\(p\) の \(\hat F_2\) への持ち上げを \(\tilde p\) とすれば
\[
\varphi_\sigma(\widetilde H)
=\tilde p\,\widetilde H\,\tilde p^{-1}.
\tag{3.3}
\]
有限 étale 被覆と開部分群の対応から
\[
W_0^\sigma\cong W_0
\]
である。全ての \(\sigma\) について成立するので
\[
\boxed{\operatorname{FOM}(W_0/U)=\mathbf Q.}
\]

(3.3) は共役類しか見ないため、(3.1) の inner ambiguity は完全に消える。
これが (K3‡) の厳密な actual lift 等式を要しない理由である。

### F3.2 field of definition

\[
\operatorname{Aut}(W_0/U)
\cong N_{G_5}(H)/H=1
\]
なら、field of moduli から definition への段も紙上で閉じる。

有限 Galois 拡大 \(L/\mathbf Q\) 上で被覆を定義する。
各 \(\sigma\in\operatorname{Gal}(L/\mathbf Q)\) に対する同型
\[
\phi_\sigma:W_0^\sigma\xrightarrow{\sim}W_0
\]
は Aut \(=1\) により一意である。すると
\[
\phi_\sigma\circ{}^\sigma\phi_\tau
\quad\text{と}\quad
\phi_{\sigma\tau}
\]
は同じ二対象間の同型なので等しく、Weil cocycle 条件が自動で成立する。
有限被覆の Galois descent により \(W_0\to U\) は
\(\mathbf Q\) 上へ降下する。

従って【文献要請 1】は出版用の正確な引用としては残るが、
数学的な穴ではない。

全分岐 cusp 上の幾何点が一つだけなら、その一点集合は
Galois 安定なので、降下後の点は \(\mathbf Q\)-有理である。

ただし補題 Q と Aut \(=1\) だけでは次は出ない。

- 明示方程式、
- 選んだ sheet/frame の \(\mathbf Q\)-有理性、
- actual marked identification、
- \(\tau\) と局所 Kummer generator の一致。

従って (4a)(4b)(4c) は閉じるが、(4d)(5′) は
記載どおり UNKNOWN のままである。

### F3.3 他窓への再利用

補題 Q は \(A_5\) と \(K^{(3)}\) の field-of-moduli 段にも再利用できる。
ただし各窓で
\[
\Phi(\operatorname{GT}(N))
\text{ が標的の「個々の」 }P\text{-共役類を保つ}
\]
ことを確認してからである。Aut-orbit 全体または複数クラスの和集合の
安定性では足りない。

また、既存の明示モデルや exact marking を補題 Q で置換しないこと。
置換できるのは非標識被覆の FOM/descent 部分だけである。

---

## F4. 命題 K5-2 と \(n=12\) 係争

### F4.1 \(e\) の一般式

\(n=2^\alpha n_0\)、\(n_0\) 奇数とする。
D1 の位数式と \(\varphi(2M)\) から
\[
e=|\mathfrak F_0|=
\begin{cases}
n,&\alpha=0,\\
n/2=n_0,&\alpha=1,\\
n/4=n_0\,2^{\alpha-2},&\alpha\ge2.
\end{cases}
\tag{4.1}
\]
ここで \(4\mid n\) なら \(m=0\) の許容パラメータは
\(k\in2\mathbf Z/(n/2)\mathbf Z\) である。
\((0,f_k)(0,f_\ell)=(0,f_{k+\ell})\) なので
\[
\mathfrak F_0\cong C_{n/4}.
\tag{4.1'}
\]
\(\alpha\le1\) でも同じ加法則から (4.1) の位数を持つ巡回群になる。
また
\[
M=
\begin{cases}
2n,&\alpha=0,\\
n,&\alpha\ge1.
\end{cases}
\]
従って
\[
\frac Me=
\begin{cases}
2,&\alpha\le1,\\
4,&\alpha\ge2.
\end{cases}
\]
ゆえに
\[
\boxed{\gcd(e,M/e)>1\iff 8\mid n.}
\tag{4.2}
\]
命題 K5-2 の数値主張は正しい。

### F4.2 \(n=12\) の明示 kernel

\[
n=12=2^2\cdot3,\qquad M=12.
\]
Thm 4.3 では \(k\) は \(\operatorname{ord}(r^2)=6\) を法に走り、
\(4\mid n\) なので \(m=0\) の kernel では \(k\equiv0\pmod2\)。
従って
\[
\mathfrak F_0
=\{k=0,2,4\pmod6\}
\cong C_3.
\]
同じことは
\[
|\operatorname{GT}(K^{(12)})|
=3\varphi(3)2^{2}=24,\qquad
\varphi(24)=8
\]
からも
\[
e=24/8=3
\]
と出る。従って
\[
\boxed{
(M,e,M/e)=(12,3,4),\qquad \gcd(3,4)=1.
}
\tag{4.3}
\]

私の便 29 P7 は撤回する。
\(n=12\) は repeated-primary 標的ではなく、
\(\alpha=2\) の偶数混合族へ移る coprime 境界例である。

### F4.3 \(n=24\) に現れる新しい blocker

ここが Opus 文書の研究計画への必須修正である。
(1.3) の生成元計算自体は、\(m=0\) については偶数 \(n\) でも成立する:
\[
\boxed{\Phi_{0,k}=\operatorname{inn}(X^{-2k}).}
\tag{4.4}
\]
\(4\mid n\) では kernel の許容値は \(k\equiv0\pmod2\) である。
\(8\mid n\) なら
\[
k_0=n/4
\]
は非零の許容値であり、
\[
f_{k_0}=(r^{n/2},r^{-n/2},1)
\]
は \(\mathfrak F_0\) の位数 \(2\) 元を与える。一方
\[
X^{-2k_0}=X^{-n/2}=(r^{n/2},1,1)
\]
は \(D_n^3\)、従って \(G_n\) の中心元である。ゆえに
\[
\boxed{\Phi_{0,k_0}=1.}
\tag{4.5}
\]
従って任意の \(\Lambda\) に対して
\[
\ker\rho_0\supseteq\langle(0,f_{k_0})\rangle\cong C_2.
\tag{4.6}
\]

\(n=24\) では
\[
M=24,\qquad e=6,\qquad M/e=4,
\]
\[
\mathfrak F_0\cong C_6,\qquad
\Phi(\mathfrak F_0)\cong C_3,\qquad
\ker(\Phi|_{\mathfrak F_0})\cong C_2.
\tag{4.7}
\]
よって \(\rho_0\) は detector の選び方によらず非忠実であり、
\[
\boxed{K^{(24)}\text{ は現行 }R^{\rm cyc}\text{ の SCHEMA-OUT}.}
\]

実は (4.2) と (4.6) は同じ条件 \(8\mid n\) で発火する。
従って \(K^{(n)}\) 族の中では

> repeated-primary を得た瞬間、まさにその repeated \(2\)-成分が
> \(\Phi\) から見えなくなる。

\(K^{(8)}\) も最小の実例で、
\(\mathfrak F_0=C_2\) 全体が \(\Phi\) 上消える。
既知の飽和結果との比較には有用だが、これは
legacy \(q\)-test の正例でなく **SCHEMA-OUT の負較正**である。

従って次の研究分岐は二つである。

1. repeated-primary かつ \(\rho_0\) 忠実となる
   **\(K^{(n)}\) 族外の窓**を探す。
2. \(\Phi\) で消える中心 \(C_2\) を別の rigidification で測る
   **拡張スキーマ**を設計する。

\(n=24\) の \(G_{24}\) を直ちに全面走査する前に、
この構造的 SCHEMA-OUT を manifest に登録すべきである。

---

## F5. 裁定 24 の \(\tau\) 処理

**確認する。BRIDGE-IN への明示追加で正しい。**

定理 \(R^{\rm cyc}_{\rm formal}\) は、固定済みの
\[
\tau:\mu_M\longrightarrow\operatorname{Sym}(\Lambda)
\]
を入力として使う。一方、
\[
\zeta_M\longmapsto(H'\mapsto XH'X^{-1})
\]
という同定が幾何から本当に来ることは、

- branch label と marking の \(X\)、
- 原始根 \(\zeta_M\)、
- 全分岐 cusp、
- 局所助変数と \(M\) 乗根、
- 左右作用・loop の向き、

を結ぶ比較橋側のデータである。従って
\(\tau\) は FORMAL-IN では「与えられた写像」、
BRIDGE-IN では「由来まで封印する写像」と二段に分けるのが正しい。

manifest では dessin ごとに最低限、次を保存する。

1. \(\zeta_{10}:=\zeta_{20}^2\) という原始根の指定。
2. \(\tau(\zeta_{10})(H')=XH'X^{-1}\) という向き。
3. local Kummer cocycle を
   \(\gamma(s^{1/10})/s^{1/10}\) と読む規約。
4. actual conjugator が branch \(0,1,\infty\) を
   \(X,Y,Z\) のどれへ送るか。
5. \(\rho_0\) 側の \(\mathfrak F_0\) generator と
   \(j:\mu_{10}[5]\to\mathfrak F_0\) の対応。

\(\tau\) を \(\tau\circ[a]\)、\(a\in(\mathbf Z/M)^\times\) へ変えるなら、
Kummer character も逆の power で同時に変換しなければならない。
整合して変換すれば class の位数、kernel、固定体は不変だが、
(5′) の**厳密な等式**は変わる。

従って \((\mathbf Z/M)^\times\) 自由度を BRIDGE-IN の封印で殺せば足り、
別の一般【GAP】を立てる必要はない。封印しない場合は、
不一致を後から generator の向きで吸収できてしまうので
BRIDGE-FAIL が反証可能でなくなる。

---

## F6. \(n=5\) manifest 骨子

### F6.1 二 dessin を別 fixture にする

manifest の最上位 policy は
\[
\boxed{\texttt{target\_policy = all\_two\_classes}}
\]
とする。

| fixture | 固定する有限対象 |
|---|---|
| `K5-sq` | \(\Lambda_{\rm sq}\)、canonical \(H\) 生成元、正規化置換三つ組、hash |
| `K5-ns` | \(\Lambda_{\rm ns}\)、canonical \(H\) 生成元、正規化置換三つ組、hash |

`sq/ns` は固定した D1 marking に相対的なラベルである。
Aut\((G_5)\) に関して絶対的な正典ではないことも記す。

### F6.2 五札

| 札 | \(n=5\) manifest に必須の内容 |
|---|---|
| **FORMAL-IN** | (0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID。各 dessin を別行にする。命題 K5-1 と \(j_i\) を記録。(5′) は bridge 完了まで `PENDING` |
| **BRIDGE-IN** | \(\mathbf Q\)-モデルの式/hash、branch map、全分岐 cusp、\(\mathbf Q\)-有理 uniformizer、actual conjugator、FC 版、\(\zeta_{10}\)、\(\tau\)、Kummer cocycle 規約。全て \(u\) 開示前に凍結 |
| **BRIDGE-FAIL** | 独立に構成した actual \(G_K\)-置換と \(\tau\kappa\) が不一致、または二 dessin が封印済み (2.3) を破る |
| **BRIDGE-UNKNOWN** | 明示モデル、actual marking、局所比較のいずれかを閉じられない。値を推測せず UNKNOWN |
| **SCHEMA-OUT** | bad \(H\) の degree 5 detector、非 regular、不安定、非忠実等。将来欄には (4.6) により \(8\mid n\) の \(K^{(n)}\) も登録 |

補助的な B1–B5 表では B5 を **PASS に塗り替えない**。
\(M=10\) なので形式判定は FAIL、ただし
\(\mathfrak F_0=C_5\) と円分商への primary 分離が
その危険を迂回する、という二段の札を保つ。

### F6.3 開示前の予測欄

数値 \(u\) は空欄のまま、次だけを封印する。

\[
\operatorname{ord}([u_i^{-1}]_{10})\in\{1,5\},
\qquad i=\mathrm{sq},\mathrm{ns},
\tag{6.1}
\]
\[
[u_{\rm ns}^{-1}]_{10}
=[u_{\rm sq}^{-1}]_{10}^{\,a},
\quad
a=j_{\rm ns}^{-1}j_{\rm sq}\in(\mathbf Z/5)^\times.
\tag{6.2}
\]

\(a\) は有限群論段で先に値を固定する。
「二つの位数が一致」だけでなく (6.2) を主整合ゲートにする。

### F6.4 fixture の較正

K3 の実測値は**回帰 fixture として流用可**だが、
\(K^{(5)}\) の証拠または期待値として流用してはならない。

K3 fixture には少なくとも

- 使用する平面モデル、
- branch の割当と exact conjugator、
- \(M=6,e=3\)、
- 使用する cusp と uniformizer、
- その正規化における \(u=-4\)、
- \(\operatorname{ord}([u^{-1}]_6)=3\)、
- \(\tau,\rho_0,j\) の向き、

を一体で保存する。別 cusp の
\[
u'=-256/729
\]
も同じ class を与える covariance control にできる。
モデルと正規化を保存せず、単独の期待値 `-4` だけを fixture にしない。

推奨する較正ゲートは三層である。

1. **finite fixture**:
   K5 の二類、passport、normalizer、regularity、
   K5-1、\(\rho_0=\tau(\mu_{10}[5])\)。
2. **K3 regression fixture**:
   既知モデルで bridge pipeline が既知 class を再現する。
   これは規約・実装回帰の検査であり、K5 の独立証拠ではない。
3. **covariance controls**:
   \(X\mapsto X^{-1}\) で class が反転し位数と体が不変、
   \(s\mapsto cs\) で \(u\mapsto uc^{-10}\) となり class が不変、
   \(\tau\mapsto\tau\circ[a]\) と Kummer character の逆 power が
   (5′) を保つこと。

### F6.5 発射判定

- **D1 finite gate**: GO。群論側は閉じている。
- **S5 モデル探索**: GO。ただし二 dessin を同時に対象にする。
- **BRIDGE-IN の凍結前の \(u\) 抽出**: NO-GO。
- **一方の dessin の結果を見て他方を捨てること**: NO-GO。
- **算術全射性の宣言**: (4d)(5′) と Kummer class が閉じるまで禁止。

---

## 提案

- **P1**: 命題 K5-1 を paper-proof として採用し、inner の規約を明記する。
- **P2**: 定理 K3 の次版で【GAP-18a】を load-bearing から
  structural lemma の較正へ降格する。過去文書は編集しない。
- **P3**: 二 dessin は両方走らせ、選択規則を
  `all_two_classes` として封印する。
- **P4**: 二 dessin の整合ゲートを「位数一致」から
  \(j_{\rm ns}^{-1}j_{\rm sq}\) による Kummer 類の power 関係へ強化する。
- **P5**: 補題 Q の \(W_0\) を最初は
  \(U_{\overline{\mathbf Q}}\) 上の幾何被覆と型付けする。
- **P6**: 命題 K5-2 は採用するが、
  \(n=24\) を現スキーマの標的から外し (4.6) を SCHEMA-OUT に登録する。
- **P7**: repeated-primary 攻略は、\(K^{(n)}\) 族外の忠実 detector
  または中心 \(C_2\) を測る拡張スキーマへ転進する。
- **P8**: \(\tau\) の由来一式を dessin ごとの BRIDGE-IN に保存する。
- **P9**: K3 は bridge pipeline の regression fixture として使うが、
  K5 の expected \(u\) や支持証拠には数えない。

## 警告

- **W1**: repeated-primary と detector の忠実性は独立でない。
  本族では前者が発火する条件 \(8\mid n\) が、後者を同時に殺す。
- **W2**: field of moduli \(=\mathbf Q\) は actual marking の
  \(\mathbf Q\)-有理性ではない。
- **W3**: 二 dessin の生の \(u\) の一致を要求しない。
  比較対象は封印した \(j\) で移送した Kummer character である。
- **W4**: Aut\((G_5)\)-融合を dessin 同型と読まない。
  cover の同型は \(G_5\)-共役類で判定する。
- **W5**: K3 の `u=-4` は正規化込みの fixture。
  数だけを K5 checker に持ち込まない。
- **W6**: \(n=12\) は coprime。便 29 P7 は本返信で訂正済みである。

---

## ★教材

1. **族の中で欲しい算術 regime が現れる条件と、
   detector がその成分を見失う条件が一致することがある。**
   \(K^{(n)}\) 族では \(8\mid n\) がその実例である。
2. **outer action の inner ambiguity は、部分群の共役類には見えない。**
   だから field of moduli には (K3‡) の exact lift は不要だが、
   actual marking と局所 \(\tau\) には再び exact data が必要になる。
3. **複数 detector の正しい一致条件は生の局所係数の一致でなく、
   共通の算術作用へ運ぶ作用同型 \(j_i\) を通じた character の一致である。**
4. **数値的に最小の候補と、スキーマ上で最初に適用可能な候補は別である。**
   \(n=24\) は前者だが後者ではない。

---

## 監査範囲外申告

本便では

- `sol/sol_task_30_k5d1.txt`,
- `docs/week4-K5橋_D1_opus_v1.md` 全文,
- `sol/裁定_24_rcyc_formal.md`,
- `docs/week4-K3飽和_opus_v3.md` v3.1 全文,
- D1 抽出ノートの (3.4)(4.12)(4.23) 関連部,
- Ih/\(\operatorname{Ih}_N\) の画像照合済み抽出ノート,
- 対話帳の新着

を紙上照合した。

node 83/83、GAP 49/49、`K5.v1.json` は再実行していない。
二共役類の個数・Aut 融合等の機械値は、開示された二系統一致を
紙上構造式と突き合わせた範囲で採用した。
明示 genus-2 モデル、\(u\)、Kummer 類、actual marked identification、
(5′)、文献要請 1 の外部出典、Lean 証明は本便の監査範囲外である。
