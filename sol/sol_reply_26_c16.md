# 8 の説明 — 総合判定: **PASS**（ただし U′-2 の「normalizer 上限一致」説は **差戻し**）

\[
\boxed{
Q_{16}:=\bar\Gamma(2)/\bar\Gamma(16)
\cong
\langle x,y,z\mid x^8=y^8=z^4=1,\ z=xyx^{-1}y^{-1},\
[z,x]=[z,y]=1\rangle .
}
\]

この class-2 表示では \([Q_{16},Q_{16}]=\langle z\rangle\cong C_4\) である。各
\(m=0,\ldots ,7\) と \(f=z^r\) に対し、第一 hexagon は自動で、第二
hexagon は
\[
3r-\binom{m+1}{2}\equiv0\pmod4
\]
に等しい。従って各 \(m\) に
\[
\boxed{r\equiv-\binom{m+1}{2}\pmod4}
\]
という唯一の解があり、生成条件も自動である。ゆえに
\[
\boxed{|GT(\mathcal C_{16})|=8.}
\]
これは証明書の
\[
32\longrightarrow32\longrightarrow8\longrightarrow8
\]
を紙上で完全に説明する。

一方、任務に書かれた
\[
N_{\operatorname{Aut}(Q_{16})}(\langle w_{16}\rangle)
\]
は、`week3` 補題 2 の規約を文字どおり使うと **型が合わない**。
\(w_{16}=\bar\sigma _1\) は
\[
\widehat Q_{16}:=B_3/N
\]
の元であり、\(Q_{16}=PB_3/N\) には入らず、\(w_{16}^2=x\) だけが
\(Q_{16}\) に入る。\(Q_{16}\) 内で意味のある
\(\langle x\rangle=\langle w_{16}^2\rangle\) に修正すると、
\[
\boxed{
\left|N_{\operatorname{Aut}(Q_{16})}(\langle x\rangle)\right|=512,
\quad |\ker\Phi_x|=2,\quad |\operatorname{Im}\Phi_x|=4,
\quad [N_{\operatorname{Aut}(Q_{16})}(\langle x\rangle):\operatorname{Im}\Phi_x]=128.
}
\]
従って **8 は normalizer 上限との一致ではない**。むしろ本セルは
G1′ が要求した「核 defect と像 defect の別登録」が実際に必要となる
最初の反例である。

また、full cyclotomic lift
\[
\widetilde\chi([m,f])=2m+1\pmod {16}
\]
は \(GT(\mathcal C_{16})\) から \((\mathbb Z/16)^\times\) への全単射である。
従って
\[
\boxed{
GT(\mathcal C_{16})\cong(\mathbb Z/16)^\times\cong C_4\times C_2,
\qquad |\mathfrak F_0(\mathcal C_{16})|=1.
}
\]
この 8 は **純円分**であり、非円分方向の余剰はない。

---

## 監査固定対象

- `sol/sol_task_26_c16.txt`: SHA-256
  `DA0465BEFA6F028831F3F1FD9BE7EA85575AD27A41F1F7DDDA9A80AAD6F3FE5B`
- `certificates/twincell/C16.matrix.v1.json`:
  `F1C2C3F044FF4C4933E433572150FB346343A664AB374049860C0E018BF8B91B`
- `certificates/twincell/K8.dncubed.v1.json`:
  `532EC2B17FB517179CCBB45E789CEA9B24E3116E4EED58DDE5DD107B7E791A5F`
- `docs/窓の地理学_v3.md`:
  `EB829676F04918F0A60E0B5A6FF6385BDA996006BA3CAA0BD2228821173D2389`
- `sol/sol_reply_21_audit.md`:
  `12C453897839223F9C042F941D61561C39BD0E6FFB2294C0D066A5D520A58CCD`
- `sol/裁定_18_kcong.md`:
  `1E5FB5F56753FF77574C4220F155B02149A21BF69A64EFD657F6C8297635C047`

以下で「証明書と一致」は、課題文が開示した GAP・独立照合器・falsifier の
三系統状態を入力にした比較を意味する。紙上導出には Lean 証明書を付けていない。

---

## F1. \(Q_{16}\) の class-2 表示

行列を
\[
x=\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad
y=\begin{pmatrix}1&0\\-2&1\end{pmatrix}
\quad\pmod {16,\ \{\pm I\}}
\]
とし、
\[
z:=xyx^{-1}y^{-1}
=
\begin{pmatrix}13&8\\8&5\end{pmatrix}
\]
と置く。直接乗算から
\[
x^8=y^8=1,\qquad z^2=9I\ne1,\qquad z^4=1,\qquad
[z,x]=[z,y]=1
\]
を得る。従って全ての元は
\[
x^a y^b z^r
\qquad
(a,b\in\mathbb Z/8,\ r\in\mathbb Z/4)
\tag{1.1}
\]
の形に収集できる。

右辺の抽象表示の位数は高々
\[
8\cdot8\cdot4=256.
\]
一方、
\[
[\bar\Gamma(2):\bar\Gamma(16)]=256
\]
であり、\(x,y\) はこの合同商を生成する。よって (1.1) は一意な正規形で、
\[
[Q_{16},Q_{16}]=\langle z\rangle\cong C_4,\qquad |Q_{16}|=256.
\tag{1.2}
\]
証明書の `derived_order: 4` は (1.2) と一致する。

この群の積規則は
\[
(x^a y^b z^r)(x^{a'}y^{b'}z^{r'})
=x^{a+a'}y^{b+b'}z^{r+r'-a'b}.
\tag{1.3}
\]
以下の全計算は (1.3) だけで行える。

---

## F2. 第二 hexagon が各 \(m\) の \(f\) を一意に較正する

\(\theta,\tau\) は定義ノートの規約
\[
\theta(x)=y,\quad\theta(y)=x,\qquad
\tau(x)=y,\quad\tau(y)=(xy)^{-1}
\]
とする。交換子への作用は
\[
\theta(z)=z^{-1},\qquad \tau(z)=z.
\tag{2.1}
\]

全ての charming class は \(m=0,\ldots ,7\) であり、候補は
\[
f=z^r\quad(r\in\mathbb Z/4).
\]
第一 hexagon は (2.1) により
\[
f\theta(f)=z^rz^{-r}=1
\]
なので、32 候補が全て通る。これは `h10_fail = 0` を説明する。

第二 hexagon に \(a_m:=y^m z^r\) と置く。まず
\[
\tau^2(y)=x,\qquad
(xy)^{-m}=z^{-\binom{m+1}{2}}x^{-m}y^{-m}.
\tag{2.2}
\]
従って
\[
\begin{aligned}
\tau^2(a_m)\tau(a_m)a_m
&=(x^mz^r)\bigl((xy)^{-m}z^r\bigr)(y^mz^r)\\
&=z^{\,3r-\binom{m+1}{2}}.
\end{aligned}
\tag{2.3}
\]
ゆえに第二 hexagon は
\[
3r\equiv\binom{m+1}{2}\pmod4.
\]
\(3^{-1}\equiv3\equiv-1\pmod4\) なので解は一意である。

具体的には
\[
\begin{array}{c|cccccccc}
m&0&1&2&3&4&5&6&7\\ \hline
r&0&3&1&2&2&1&3&0
\end{array}
\tag{2.4}
\]
である。これは証明書の四種の語
\[
1,\quad z,\quad z^{-1},\quad z^2
\]
の配置と逐語的に一致する。従って per-\(m\) で
\[
4\longrightarrow4\longrightarrow1.
\]
全体では \(24\) 個だけが第二 hexagon で落ちる。

最後に \(u:=2m+1\) は奇数で、\(f=z^r\) は中心的だから、生成対は
\[
x^u,\qquad f^{-1}y^uf=y^u.
\]
\(uv\equiv1\pmod8\) なる \(v\) を取れば
\((x^u)^v=x,\ (y^u)^v=y\) なので、この二元は \(Q_{16}\) を生成する。
よって `generation_fail = 0` も紙上で従い、
\[
|GT(\mathcal C_{16})|=8
\]
が閉じる。

---

## F3. 「8」の群構造と \(\mathfrak F_0\)

isolated が確定したので \(GT(\mathcal C_{16})=GTSh(N,N)\) は有限群である。
合成則では \(2m+1\) が乗法的であり、
\[
\widetilde\chi:
GT(\mathcal C_{16})\longrightarrow(\mathbb Z/16)^\times,\qquad
[m,f]\longmapsto2m+1
\tag{3.1}
\]
は群準同型である。
\(m\) を \(m+8\) に替えると \(2m+1\) は \(16\) だけ変わるので、
この mod \(16\) lift は \(m\in\mathbb Z/8\) 上で well-defined である。

\(m=0,\ldots ,7\) に対する像は
\[
1,3,5,7,9,11,13,15
\]
であり、F2 により各 \(m\) に shadow は一つだけである。従って (3.1) は
全単射で、
\[
GT(\mathcal C_{16})
\cong(\mathbb Z/16)^\times
\cong C_4\times C_2.
\tag{3.2}
\]

\(\mathfrak F_0\) は \(m=0\) の fibre であり、(2.4) から
\[
\mathfrak F_0(\mathcal C_{16})=\{[0,1]\}.
\tag{3.3}
\]
またこの場合は (3.1) の核とも一致する。従って
\[
\boxed{|\mathfrak F_0|=1}
\]
で、8 個は全て円分方向で区別される。\(m\ne0\) で現れる非自明な
\(z^r\) は、独立な非円分 fibre ではなく、各円分指数に第二 hexagon が
強制する **一意な較正項**である。

なお、定義ノートの
\[
\chi_{\rm vir}=2m+1\pmod {N_{\rm ord}}=2m+1\pmod8
\]
へ落とすと核は位数 2 になる。これは full lift (3.1) から
\((\mathbb Z/8)^\times\) への reduction の核 \(\{1,9\}\) であり、
\(\mathfrak F_0\) ではない。この二つを区別しなければならない。

---

## F4. \(w_{16}\) の型監査

week3 補題 2 の正本は
\[
v_m=\bar\sigma _1^{\,2m+1}
\quad\text{in}\quad
\widehat Q_{16}:=B_3/N.
\]
従って
\[
w_{16}:=\bar\sigma _1\in\widehat Q_{16},\qquad
\operatorname{ord}(w_{16})=16,\qquad w_{16}^2=x.
\tag{4.1}
\]
\(PB_3/N\) は \(\widehat Q_{16}\twoheadrightarrow S_3\) の核である一方、
\(\bar\sigma _1\) の像は transposition なので
\[
w_{16}\notin Q_{16}=PB_3/N.
\tag{4.2}
\]

従って v3 の
\[
Q_N=PB_3/N
\quad\text{かつ}\quad
w_N=\bar\sigma _1
\]
という二つの規約を同時に採る
\[
N_{\operatorname{Aut}(Q_N)}(\langle w_N\rangle)
\]
は一般には未定義である。A\(_5\) の odd-\(k\) split-inner 例では
\(w=X^a\in P\) となって偶然この型問題が隠れていた。今回の even-\(k\)
セルで初めて露出した。

修正候補は二つである。

1. \(Q_N=PB_3/N\) を維持し、\(\langle w_N^2\rangle=\langle x\rangle\) と、
   \(w_N\) の square-root coset / \(S_3\)-輸送作用を別の marking として持つ。
2. target を \(\widehat Q_N=B_3/N\) に替え、
   \(N_{\operatorname{Aut}(\widehat Q_N)}(\langle\bar\sigma _1\rangle)\) を測る。

後者の full normalizer は今回の証明書に含まれていないので **UNKNOWN** として
新たに事前登録すべきであり、8 を答えとして逆算してはならない。

---

## F5. \(Q_{16}\) 内での修正版 normalizer は 512

F1 の正規形を用いる。任意の自己準同型は
\[
\begin{aligned}
\alpha(x)&=x^a y^b z^r,\\
\alpha(y)&=x^s y^t z^q
\end{aligned}
\qquad
\left(
\begin{array}{c}
a,b,s,t\in\mathbb Z/8,\\
r,q\in\mathbb Z/4
\end{array}
\right)
\tag{5.1}
\]
で指定できる。実際、\(Q_{16}\) の全元の位数は 8 を割り、交換子は中心で
位数 4 を割るため、表示の関係は保たれる。

交換子への作用は
\[
\alpha(z)=z^{at-bs}.
\tag{5.2}
\]
従って \(\alpha\) が自己同型であるための必要十分条件は
\[
at-bs\quad\text{が奇数}
\tag{5.3}
\]
である。これは \(Q_{16}^{\rm ab}\cong(\mathbb Z/8)^2\) 上の行列が可逆で
あることに等しく、(5.2) により導来群にも全射となる。

\(\alpha\) が \(\langle x\rangle\) を正規化するには
\(\alpha(x)\) が \(\langle x\rangle\) の生成元でなければならない。正規形の
一意性から
\[
b=0,\qquad r=0,\qquad a\in(\mathbb Z/8)^\times.
\]
さらに (5.3) は \(t\) が奇数であることに等しい。従って自由な選択は
\[
a:\ 4,\qquad s:\ 8,\qquad t:\ 4,\qquad q:\ 4
\]
であり、
\[
\boxed{
\left|N_{\operatorname{Aut}(Q_{16})}(\langle x\rangle)\right|
=4\cdot8\cdot4\cdot4=512.
}
\tag{5.4}
\]

これは探索器の shadow 数からの逆算ではなく、群表示からの紙上計算である。

---

## F6. \(\Phi_x\) の核 defect と像 defect

shadow \([m,z^r]\) が \(Q_{16}\) に誘導する自己同型は
\[
\Phi_x([m,z^r]):
\quad x\longmapsto x^u,\qquad
y\longmapsto z^{-r}y^uz^r=y^u,
\qquad u=2m+1.
\tag{6.1}
\]
従って \(\Phi_x\) は \(u\bmod8\) しか見ず、
\[
\operatorname{Im}\Phi_x
=
\{\alpha_u:x\mapsto x^u,\ y\mapsto y^u
\mid u\in(\mathbb Z/8)^\times\}
\cong(\mathbb Z/8)^\times
\tag{6.2}
\]
である。ゆえに
\[
|\operatorname{Im}\Phi_x|=4.
\]

恒等自己同型を与える shadow は
\[
[0,1]\quad(u=1),\qquad [4,z^2]\quad(u=9)
\]
の二つである。従って
\[
\boxed{\ker\Phi_x\cong C_2.}
\tag{6.3}
\]
最後に (5.4) と (6.2) から
\[
\boxed{
\left[
N_{\operatorname{Aut}(Q_{16})}(\langle x\rangle):
\operatorname{Im}\Phi_x
\right]=\frac{512}{4}=128.
}
\tag{6.4}
\]

従って G1′ の欄は
\[
\begin{array}{c|c}
\text{量}&\mathcal C_{16}\\ \hline
|\ker\Phi_x|&2\\
|\operatorname{Im}\Phi_x|&4\\
|N_{\operatorname{Aut}(Q_{16})}(\langle x\rangle)|&512\\
\text{image index}&128
\end{array}
\]
と別々に登録せよ。U′-2a と U′-2b は、この修正 target に対して
**両方とも偽**である。

特に \(\ker\Phi_x\cong C_2\) を cusp-16 の撤回済み「非円分位数 2」の
救済に使ってはならない。その非自明元の full cyclotomic character は
\(9\bmod16\) であり、これは **円分方向だが \(Q_{16}\) の exponent 8 の
作用から見えなくなった元**である。

---

## F7. 双子セルを分ける機構

証明書を per-\(m\) に割ると、
\[
\begin{array}{c|c|c|c|c}
&|[P,P]|&\text{候補}&\text{第一 hexagon 後}
&\text{第二 hexagon 後}\\ \hline
\mathcal C_{16}&4&4&4&1\\
K^{(8)}&16&16&8&2
\end{array}
\tag{7.1}
\]
であり、この分布は八つの \(m\) 全てで一様である。

従って 8 対 16 の shadow-theoretic な直接原因は
\[
\boxed{
\text{各円分指数の \(f\)-fibre が }\mathcal C_{16}\text{ では 1、}
K^{(8)}\text{ では 2}
}
\tag{7.2}
\]
である。言い換えると
\[
|\mathfrak F_0(\mathcal C_{16})|=1,\qquad
|\mathfrak F_0(K^{(8)})|=2.
\tag{7.3}
\]

その群論的な置き場はまず **(A1) 完全 marked quotient**、より圧縮して
言えば **(C′) 導来層と \(\theta,\tau\) の作用**である。

- \(\mathcal C_{16}\) では \([P,P]=C_4\) かつ
  \(\theta(z)=z^{-1}\) なので第一 hexagon は全 \(4\) 元を通し、第二
  hexagon が一意解へ切る。
- \(K^{(8)}\) では \(|[P,P]|=16\) で、marked \(\theta\)-条件がまず
  \(16\) 元を \(8\) 元へ切り、第二条件が \(2\) 元を残す。

従って両者は完全 marked 構造以前に、抽象群の
\[
|[P,P]|=4\quad\text{対}\quad16
\]
ですでに分かれる。marking はさらに「どの半分・どの二元が残るか」を決める。

### \(d_{\rm cong}\) の裁定

\[
d_{\rm cong}(\mathcal C_{16})=1,\qquad
d_{\rm cong}(K^{(8)})\ne1
\]
なので、**B′ 座標が二点を区別する**という弱い命題は正しい。従って
「order・level・passport の粗表より B′ が強い」という教材としては採用してよい。

しかし
\[
\boxed{\text{「\(d_{\rm cong}\) が 8 対 16 を生んだ」とはまだ言えない。}}
\]
同じ一対で A1/C′ も同時に変化しており、(7.1) は実際にそちらの
hexagon 機構だけで数を説明する。従って今回実証されたのは

- B′ の **記述的な分離力**: Yes。
- \(d_{\rm cong}\) の **shadow 数に対する独立な因果力**: 未証明。

である。

(A0) の braid 中心については両窓とも \(c\in N\)、すなわち
\(e_c=1\) である。この A0 座標は今回の分離因子ではない。内部中心・交換子
pairing は A1/C′ に置くべきで、braid 中心の拡大類と混同しない。

---

## F8. cusp-16 撤回予測の事後検分

実測・紙上導出は
\[
|\mathfrak F_0(\mathcal C_{16})|=1
\]
であり、撤回前の「位数 2」とは一致しない。便 21 で撤回した判断は正しかった。

便 21 の自然な cusp 定義体
\[
K=\mathbb Q(\zeta_{16})
\]
では
\[
16^{1/8}=\sqrt2\in K,
\]
従って \([16]\in K^\times/K^{\times8}\) は自明であった。今回の
\(\mathfrak F_0=1\) はこの診断と **整合**する。

ただし、これは局所 Kummer 類から GT rigidification への比較射を新たに
構成したわけではない。ゆえに正しい結論は

\[
\boxed{
\text{自然な体上の局所類自明と \(\mathfrak F_0=1\) は整合するが、}
\text{cusp-16 一般則が証明されたわけではない。}
}
\]

である。G6a はそのまま、G6b の「比較射を全て与えるまで数値予測しない」という
封印もそのまま維持する。

---

## F9. settled・isolated と算術像

`settled 8/8` は、F2 の八つの shadow が全て同じ marked kernel に戻り、
(6.1) の自己同型を与えることを意味する。`isolated = true` は connected
component がこの一対象だけで、これらが有限群として閉じることを意味する。

ここからは次が従う。

1. **G2′ の settled 率は 1。**  
   \(e=16\)、\(U_e=(\mathbb Z/16)^\times\) の全八指数が stabilizer に入り、
   各指数 fibre は一様に一元だから
   \[
   \frac{\#\mathrm{settled}}{\#GTSh(N,N)}
   =1
   =\frac{|\operatorname{Stab}_{U_{16}}(\nu_N)|}{|U_{16}|}.
   \]
   従って G2′ はこのセルを通る。なお \(K^{(8)}\) も settled 率 1 なので、
   G2′ は双子を分離しない。
2. **isolated は \(\Phi_x\) の faithful 性を含まない。**  
   (6.3) が明示反例である。
3. 標準互換性
   \[
   \widetilde\chi\circ\operatorname{Ih}_N
   =\chi_{\rm cyc}\pmod {16}
   \tag{9.1}
   \]
   を用いると、\(\chi_{\rm cyc}:G_{\mathbb Q}\twoheadrightarrow
   (\mathbb Z/16)^\times\) は全射で、\(\widetilde\chi\) は F3 の全単射である。
   従って
   \[
   \boxed{\operatorname{Ih}_N:G_{\mathbb Q}\twoheadrightarrow
   GT(\mathcal C_{16})}
   \tag{9.2}
   \]
であり、\(\mathcal C_{16}\) は **算術飽和**する。
すなわち八つの shadow は全て arithmetical である。

(9.2) は cusp torsor からの推論ではなく、isolated 性・純円分性・通常の
cyclotomic character の全射性だけから従う。

U′-1 の二つの体の区別もここで実物になる。

- \(\ker(\operatorname{Ih}_N)\) の固定体は full character を切る
  \(\mathbb Q(\zeta_{16})\) で、次数 \(8=|GT|\)。
- \(\Phi_x\circ\operatorname{Ih}_N\) が切る deck-\(Q_{16}\) 作用は
  \(u\bmod8\) しか見ず、固定体は \(\mathbb Q(\zeta_8)\)、次数 \(4\)。

従って v3 が後者に \(\Phi_N\) 単射を前件としたのは正しい。今回その前件が
実際に破れ、二つの「定義体」が分離した。

---

## F10. 地理学 v3 の法則札

\[
\begin{array}{c|c|l}
\text{札}&\text{判定}&\text{理由}\\ \hline
G0&\text{未検査}&
一つの既知 kernel の shadow 全列挙は、全 admissible triple/Aut の窓数計算ではない\\
G1'&\text{帳簿原則 PASS、普遍等式 FAIL}&
\ker\Phi_x=2、image\ index=128。さらに \(w\) の型修正が必要\\
G2'&\text{PASS}&
全 \(U_{16}\) が stabilizer、settled 率 1\\
G3'&\text{未検査}&
中央塔の各層の obstruction map は今回の証明書にない\\
G4'/G6b&\text{整合のみ}&
\mathfrak F_0=1 は自然体上の局所類自明と整合するが比較射は未構成\\
G5&\text{未検査}&
CRT intersection / gluing edge を計算していない\\
U'-1&\text{二定義の分離を実証}&
\operatorname{Ih}\text{ の体は次数 8、deck-\(\Phi\) の体は次数 4}\\
U'-2a&\text{反証}&|\ker\Phi_x|=2\\
U'-2b&\text{反証}&|\operatorname{Im}\Phi_x|=4<512
\end{array}
\]

G1′ は「法則として失敗した」のではなく、**欠損を二欄に分ける監査規則として
初めて本領を発揮した**。一方、v3 §4 が U′-2a/b を無条件の「確定命題」として
掲げている文面は、このセルにより反証されたので改訂が必要である。

---

## F11. panel 更新

科学的な次の本命は
\[
\boxed{\mathcal C_{12}\ \text{対}\ K^{(3)}}
\]
とする。

理由は次の三つである。

1. level/passport を合わせた第二の congruence/noncongruence 対で、
   「B′ は区別するが A1/C′ が shadow 数を直接支配する」という今回の読みが
   再現するかを試せる。
2. \(12=4\cdot3\) は最初の mixed CRT であり、未検査の G5/gluing を同時に撃てる。
3. \(K^{(3)}\) は算術予想の最小 open target なので、単なる atlas 埋めより
   主線への情報利得が大きい。

\(\mathcal C_{14}\) は別種の高優先 control である。商は
\(PSL_2(7)\)、odd \(k=7\) なので、今回露出した
\[
w\notin P,\qquad \langle w^2\rangle\text{ では full cyclotomic 情報を失う}
\]
という even-\(k\) 問題との対照になる。また既存 S1 データがあるため、新規全走査の
前に
\[
\mathcal C_{14}\longrightarrow S1
\]
の **明示 marked factor map** を一本出せば、安価な panel bridge になる。
名前・位数一致だけで S1 を流用してはならない。

従って実務順と科学順を分ける。

1. **実務上の先手**: \(\mathcal C_{14}\leftrightarrow S1\) の marked factor
   map を短い較正ゲートとして閉じる。
2. **次の新規 blind pair**: \(\mathcal C_{12}/K^{(3)}\) を同一 manifest で走らせる。
3. その後に \(\mathcal C_{18}\)、次いで
   \(\mathcal C_{20}/K^{(5)}\) の mixed pair。

各次窓には従来の count/settled/isolated に加え、必ず

\[
\begin{gathered}
|[P,P]|,\quad
\#\ker(1+\theta|_{[P,P]}),\quad
\text{per-\(u\) hexagon fibre},\\
|\ker\Phi|,\quad|\operatorname{Im}\Phi|,\quad
\text{plain normalizer order},\quad
\text{full-\(B_3/N\) marked normalizer order}
\end{gathered}
\]

を別欄で出すべきである。

---

## 提案

**P196【定理 C16-8】**  
F1–F3 を `C16 class-2 lemma` として採録する。核心式は
\[
3r=\binom{m+1}{2}\pmod4
\]
で、各円分指数に唯一の中央較正項がある、という形にする。

**P197【G1′ の型修正】**  
\(P_N=PB_3/N\) と \(\widehat Q_N=B_3/N\) を別記号に固定する。
\(w_N=\bar\sigma _1\) を使う normalizer は \(\widehat Q_N\) 側で定義する。
\(P_N\) 側では \(\langle X\rangle=\langle w^2\rangle\) に加えて square-root
coset と \(S_3\)-輸送作用を marking に含める。

**P198【C16 の G1′ 台帳】**  
\[
|\ker\Phi_x|=2,\quad|\operatorname{Im}\Phi_x|=4,\quad
|N_{\operatorname{Aut}(P)}(\langle X\rangle)|=512,\quad
\text{image index}=128
\]
を別欄で登録する。

**P199【算術像更新】**  
F9 の cyclotomic 全射論により、v3 の
「\(\mathcal C_{16}\) の算術像 UNKNOWN」を
\[
\operatorname{Im}\operatorname{Ih}_N=GT(\mathcal C_{16})
\cong(\mathbb Z/16)^\times
\]
へ更新する。状態は紙上証明、Lean 未接続とする。

**P200【双子セルの標準表示】**  
双子比較は総数だけでなく
\[
\mathcal C_{16}:4\to4\to1,\qquad
K^{(8)}:16\to8\to2
\]
を per-\(m\) 標準行として panel に保存する。

**P201【次便順】**  
\(\mathcal C_{14}\leftrightarrow S1\) の marked bridge を安価に先に閉じ、
新規計算の第一順位を \(\mathcal C_{12}/K^{(3)}\) とする。

---

## 警告

**W156【\(w\) の所在】**  
\(w=\bar\sigma _1\in B_3/N\) と
\(X=w^2\in PB_3/N\) を同じ群の元として書かない。odd-\(k\) の
split-inner 例で偶然 \(\langle w\rangle=\langle X\rangle\) となった記法を
2-primary 窓へ移植しない。

**W157【三つの核】**  
\[
\mathfrak F_0=\ker\widetilde\chi_{16}=1,\qquad
\ker(\chi_{\rm vir}\bmod8)\cong C_2,\qquad
\ker\Phi_x\cong C_2
\]
は別の量である。後二者の位数 2 を cusp の非円分 torsor と呼ばない。

**W158【相関を機構にしない】**  
\(d_{\rm cong}\) は双子を区別するが、同時に
\(|[P,P]|\) と marked \(\theta,\tau\) 作用も変わる。一対の観測だけから
「非合同だから fibre が 2」と一般化しない。

**W159【isolated \(\not\Rightarrow\) faithful】**  
isolated は groupoid component と kernel stability を与えるが、
\(\Phi\) の単射性を与えない。\([4,z^2]\ne[0,1]\) が同じ deck 自己同型を
与える本セルを恒久反例にする。

**W160【局所類の事後救済禁止】**  
撤回予測「位数 2」と \(|\ker\Phi_x|=2\) の数値一致は別物である。
自然な cusp 体上の \([16]\) は自明、実測 \(\mathfrak F_0\) も自明であり、
旧予測を別の核へ付け替えて救済してはならない。

**W161【状態語】**  
双子セルの count/settled/isolated は開示された二系統+falsifier の
照合済み入力、F1–F9 の構造説明は本便の紙上証明である。Lean 証明書がないため
`verified` とは呼ばない。
