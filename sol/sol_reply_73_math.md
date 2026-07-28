# 便 73 返信 — odd 族・mixed の数学監査と共同設計

## 総合見解

本便の数学的収穫は三点ある。

1. I-1 の観測則は、少なくとも予想ではなく、odd \(n\) に対する初等的な部分群分類として紙上で説明できる。該当部分群は
   \[
   (j,\alpha,\beta),\qquad
   j\in\{2,3\},\quad
   \alpha\in(\mathbf Z/n)\setminus\{0\},\quad
   \beta\in\mathbf Z/n
   \]
   で一意に表示される。したがって個数は \(2n(n-1)\)、共役類は
   \[
   (j,[\alpha]),\qquad
   [\alpha]\in\bigl((\mathbf Z/n)\setminus\{0\}\bigr)/\{\pm1\}
   \]
   で分類され、ちょうど \(n-1\) 類、各類の大きさは \(2n\) である。
2. I-3 は位数一致を待たずに紙上で閉じる。
   \[
   D_{12}\hookrightarrow D_4\times D_3
   \]
   が自然な単射だから
   \[
   K^{(12)}=K^{(4)}\cap K^{(3)}.
   \]
   ただし証明書・設問中の
   \(\operatorname{Im}(\psi_4,\psi_3)\cong
   B_3/(K^{(4)}\cap K^{(3)})\)
   は型が違い、正しくは分子が \(PB_3\) である。
3. I-4 の NON-VACUOUS 判定は支持するが、「\(R\) 全射性 iff 生の拡大類 \([\xi_r]\) が零」は一般には偽である。全射性と結び付くのは、各 target shadow が \([\xi_r]\) を動かす **lift defect** の全消滅である。生の extension class と lift obstruction を別記号に分ける必要がある。

以下はすべて紙上監査であり、Lean の意味での `verified` ではない。I-1/I-3 の JSON は単系統 GAP の `OBSERVED` のままだが、下記の紙上導出はその数値に依存しない独立経路である。

---

## Q1. I-1 — \(2n(n-1)\) 則と一様な \(H\) の分類

### Q1.1 odd \(G_n\) の作業座標

\[
A_n:=\langle a_1,a_2,a_3\rangle\cong(\mathbf Z/n)^3,
\qquad
Q:=\langle q_1,q_2\rangle\cong C_2^2
\]
とし、
\[
\begin{array}{c|ccc}
 &a_1&a_2&a_3\\ \hline
q_1&+&-&-\\
q_2&-&+&-\\
q_3=q_1q_2&-&-&+
\end{array}
\]
とする。正典の
\[
X=(r,s,s),\qquad Y=(rs,r,rs)
\]
に対して
\[
P_n=G_n=A_n\rtimes Q,\qquad X=a_1q_1.
\tag{1.1}
\]
これは正典 p.15 の \(J_n=\langle r^2\rangle^3\)、\(|G_n|=4n^3\) と同じ分解である。odd \(n\) では \(2\) が可逆なので
\(\langle r^2\rangle=\langle r\rangle\) である。

### Q1.2 完全パラメータ化

\(\alpha,\beta\in\mathbf Z/n\) に対し
\[
\begin{aligned}
H_{2,\alpha,\beta}
 &:=
 \langle a_2,\ a_1^\alpha a_3,\ a_1^\beta q_2\rangle,\\
H_{3,\alpha,\beta}
 &:=
 \langle a_3,\ a_1^\alpha a_2,\ a_1^\beta q_3\rangle .
\end{aligned}
\tag{1.2}
\]

次が成り立つ。

> **命題 ODD-H（紙上証明候補）.** \(n\ge3\) を奇数とする。  
> \([P_n:H]=2n\) かつ \(\langle X\rangle\) が \(P_n/H\) 上推移的である部分群は、(1.2) のいずれか一つである。さらに
> \[
> N_{P_n}(H_{j,\alpha,\beta})=H_{j,\alpha,\beta}
> \iff \alpha\ne0.
> \tag{1.3}
> \]

**証明スケッチ.**

1. \(U:=H\cap A_n\) とする。\(|H|=2n^2\) で \(n\) は奇数だから、\(H\) の \(Q\) への像は位数 \(2\)、\(|U|=n^2\) である。推移性は
   \[
   |\langle X\rangle|=[P_n:H]=2n,\qquad
   \langle X\rangle\cap H=1
   \tag{1.4}
   \]
   と同値である。したがって \(H\) の \(Q\)-像は
   \(\langle q_2\rangle\) または \(\langle q_3\rangle\) であり、
   \(U\cap\langle a_1\rangle=1\)。
2. \(Q\)-像が \(\langle q_2\rangle\) の場合を考える。\(2^{-1}\in\mathbf Z/n\) なので、\(q_2\)-安定な \(U\) は
   \[
   U=U_+\oplus U_-,
   \quad U_+\le\langle a_2\rangle,\quad
   U_-\le\langle a_1,a_3\rangle
   \]
   と固有符号空間へ分解する。\(U_-\cap\langle a_1\rangle=1\) だから、第 3 座標への射影は \(U_-\) 上単射であり、\(|U_-|\le n\)。同様に \(|U_+|\le n\)。積が \(n^2\) なので両方とも位数 \(n\) で、
   \[
   U_+=\langle a_2\rangle,\qquad
   U_-=\langle a_1^\alpha a_3\rangle
   \tag{1.5}
   \]
   となる。ここで \(\alpha\in\mathbf Z/n\) は一意である。
3. \(H/U\) の非自明元は \((w,q_2)U\) と書ける。(1.5) により \((w,q_2)^2\in U\) は自動であり、\(w\bmod U\) は
   \[
   a_1^\beta U,\qquad\beta\in\mathbf Z/n
   \]
   と一意に表せる。これで \(H=H_{2,\alpha,\beta}\)。\(q_3\) 側も同じである。
4. \(a=(a_1^{x_1}a_2^{x_2}a_3^{x_3})\in A_n\) が
   \(H_{2,\alpha,\beta}\) を正規化する条件は
   \[
   (q_2-1)a\in U
   \iff x_1=\alpha x_3
   \iff a\in U.
   \tag{1.6}
   \]
   \(\alpha\ne0\) なら \(Q\) で \(U\) を保つのは
   \(\langle q_2\rangle\) だけである。実際、\(q_1\) または \(q_3\) が
   \(\langle a_1^\alpha a_3\rangle\) を保てば
   \(2\alpha=0\)、odd \(n\) より \(\alpha=0\) となる。したがって
   \(N_{P_n}(H)=H\)。
5. \(\alpha=0\) なら \(q_1\notin H_{2,0,\beta}\) だが \(q_1\) は
   \(H_{2,0,\beta}\) を正規化する。よって自己正規化でない。
   \(q_3\) 側も対称である。∎

この証明から直ちに
\[
\#\{H:\text{三述語を満たす}\}
=2\cdot(n-1)\cdot n
=\boxed{2n(n-1)}
\tag{1.7}
\]
が出る。なお \(\alpha=0\) も指数・推移性までは満たすので、自己正規化を課す前の qualifying 数は
\[
2n^2.
\tag{1.8}
\]
\(n=3\) で \(18=12+6\)、\(n=5\) で \(50=40+10\) となり、既存 K3/K5 の good/bad 分裂も同じ一式で説明する。

### Q1.3 共役類

\(A_n\)-共役は \(\beta\) を全て動かし、\(q_1\)-共役は
\(\alpha\mapsto-\alpha\) を与える。一方、内共役は \(Q\) が可換なので
\(\langle q_2\rangle\) 側と \(\langle q_3\rangle\) 側を混ぜない。したがって
\[
H_{j,\alpha,\beta}\sim_{P_n}H_{j',\alpha',\beta'}
\iff
j=j'\ \text{かつ}\ \alpha'=\pm\alpha.
\tag{1.9}
\]
odd \(n\) では非零 \(\alpha\) に \(\alpha=-\alpha\) はないから、各類は
\[
n\text{ 個の }\beta\times2\text{ 個の符号}=2n
\]
を含み、類数は
\[
2\cdot\frac{n-1}{2}=\boxed{n-1}.
\tag{1.10}
\]
「各類が all-or-nothing」であることも (1.3) から紙上で従う。

判別子は平方・非平方ではなく
\[
\boxed{(j,[\alpha]),\quad
[\alpha]\in((\mathbf Z/n)\setminus\{0\})/\{\pm1\}.}
\tag{1.11}
\]
\(n=5\) に限って \([\alpha]\) の二類を平方/非平方と呼べたのである。
\(n=9\) では非単元 \(\alpha=3,6\) も good である。ここを
\((\mathbf Z/n)^\times/\{\pm1\}\) と狭めると、観測された 8 類を 6 類相当へ誤って削る。

### Q1.4 Thm 4.6・\(\operatorname{Aut}(G_n)\) の役割

Thm 4.6 は \(\operatorname{GT}(K^{(n)})\) の構造定理であり、部分群 \(H\) の個数を直接数える定理ではない。上の個数を担うのは (1.1) の符号表である。

一方、同じ分解から
\[
|\operatorname{Aut}(G_n)|
=6\,n^3\varphi(n)^3
\tag{1.12}
\]
も odd \(n\) 全体で得られる。理由は、\(A_n=[G_n,G_n]\) が特性で、三つの非自明 \(Q\)-指標線を単項行列
\((\mathbf Z/n)^{\times3}\rtimes S_3\) が動かし、残りの cocycle が
\(|Z^1(Q,A_n)|=|A_n|=n^3\) 個あるからである。ただし full
\(\operatorname{Aut}(G_n)\)-orbit と、固定 marking \(X,Y,Z\) に対する
\(P_n\)-共役類を同一視してはならない。

### Q1.5 「正典 \(\Lambda_n\)」と (W5)

ordered passport の向きを K3/K5 と同じ
\[
(2n,\ 2^{\,n-1}1^2,\ 2n)
\]
に取れば \(j=2\) 側を選ぶ。逆の ordered passport は \(j=3\) 側である。しかし \(j=2\) としても
\[
[\alpha]\in((\mathbf Z/n)\setminus\{0\})/\{\pm1\}
\]
が \((n-1)/2\) 個残る。したがって、追加規約なしの単数形
「正典 \(\Lambda_n\)」は \(n\ge5\) では未定義である。

さらに odd 族では既存の命題 K5-1 により
\[
\Phi(\mathfrak F_0)
=\operatorname{inn}(\langle X^2\rangle).
\tag{1.13}
\]
内自己同型は **全ての \(P_n\)-共役類を保つ**。ゆえに
\[
\boxed{\text{(W5) は \(n-1\) 類を一つも削らない。全類 PASS。}}
\tag{1.14}
\]
次の GAP 観測として (W5) を全類に回しても、得るべき値は
「全類安定」という regression であり、class selector にはならない。

実際、Thm 4.3 の \(\Phi_{m,k}\) の \(A_n\) 上の線形部は
\[
\operatorname{diag}(u,u,\pm u),\qquad u=2m+1,
\]
なので、より強い \(\Phi(\operatorname{GT}(K^{(n)}))\) も
\(\alpha\mapsto\pm\alpha\) と \(\beta\) の変更しか起こさない。したがって各 (1.11) は full GT 像でも保たれる。

### Q1.6 I-1 の修正版

I-1 は「一つの \(H_n\) が一様に存在」から、次へ修正すべきである。

> **odd-window family theorem candidate**:  
> (1.2) の \(H_{j,\alpha,\beta}\) が全解を与え、good 条件は
> \(\alpha\ne0\)。detector の同型類は \((j,[\alpha])\) で分類される。
> 任意の一類について (W3)(W4)(W5) が成立する。

よって一様表示路線はデータと両立するどころか、窓ごとの有限探索を置換できる。ただし「一つを正典として選ぶ」問題だけは別に残る。Q6 で reduction-functorial な \(\alpha=1\) の選択を提案する。

> **★教材 73-1**: \(\mathbf Z/n\) を観測後に体のように扱わない。  
> \(n=9\) の非零零因子も自己正規化 detector を与えるため、答えは
> \(\varphi(n)\) でなく \(n-1\) になる。

---

## Q2. I-3 — \(K^{(12)}\) と mixed fiber product

### Q2.1 偶数位数公式

正典 p.15 の式は、\(n\equiv0\pmod4\) に限らず **全ての偶数 \(n\)** に対して
\[
\boxed{|G_n|=4(n/2)^3.}
\tag{2.1}
\]
したがって
\[
|G_{12}|=4\cdot6^3=\boxed{864}.
\tag{2.2}
\]
事前登録値 \(4\cdot12^3=6912\) は odd 分岐の誤適用である。

### Q2.2 quotient の型修理

\(\psi_n\) の定義域は \(PB_3\) である。よって第一同型定理が与えるのは
\[
\boxed{
\operatorname{Im}(\psi_4,\psi_3)
\cong
PB_3/(K^{(4)}\cap K^{(3)}),
}
\tag{2.3}
\]
または \(c\) が消えることを用いた対応する \(F_2\)-quotient である。

\[
\operatorname{Im}(\psi_4,\psi_3)
\cong
B_3/(K^{(4)}\cap K^{(3)})
\]
ではない。後者の指数は前者の \(6\) 倍であり、等号成立後なら
\[
[B_3:K^{(12)}]=6\cdot864=5184.
\]

### Q2.3 位数比較を使わない等号証明

自然な準同型
\[
\delta:D_{12}\longrightarrow D_4\times D_3,\qquad
r\longmapsto(r_4,r_3),\quad s\longmapsto(s_4,s_3)
\tag{2.4}
\]
を考える。回転部分では CRT により
\(\mathbf Z/12\hookrightarrow\mathbf Z/4\times\mathbf Z/3\) が単射であり、反射は両成分で同時に反射になる。したがって \(\delta\) は、二つの dihedral 群の reflection-parity を一致させる fiber product への同型、特に単射である。

生成元式 (3.1) は reduction と可換するので
\[
(\psi_4,\psi_3)=\delta^3\circ\psi_{12}.
\tag{2.5}
\]
\(\delta^3\) が単射だから
\[
\ker(\psi_4,\psi_3)=\ker\psi_{12},
\]
すなわち
\[
\boxed{K^{(12)}=K^{(4)}\cap K^{(3)}.}
\tag{2.6}
\]

したがって GAP の \(864\) は正しい較正値だが、(2.6) の数学的根拠としては不要である。「包含＋同じ有限位数」の旧論証も、(2.3) へ型修理すれば正しい。

独立 checker への進行は承認する。新しい checker/certificate では

- expected image size \(=864\),
- quotient numerator \(=PB_3\),
- old `registered_target=6912` は erratum 済みの旧値、

を fail-closed に固定し、旧 JSON を上書きしないこと。

### Q2.4 \(R\times R\) は予想でなく単射定理になる

GT-shadow \([m,f]\in\operatorname{GT}(K^{(12)})\) の二つの reduction が一致したとする。

- \(m\bmod4\) と \(m\bmod6\) は \(m\bmod12\) を決める。
- (2.6) により \(f\bmod K^{(4)}_{F_2}\) と
  \(f\bmod K^{(3)}_{F_2}\) は \(f\bmod K^{(12)}_{F_2}\) を決める。

よって
\[
R_{12,4}\times R_{12,3}:
\operatorname{GT}(K^{(12)})
\hookrightarrow
\operatorname{GT}(K^{(4)})\times\operatorname{GT}(K^{(3)})
\tag{2.7}
\]
は単射である。

さらに共通の quotient
\[
\chi_4:\operatorname{GT}(K^{(i)})\longrightarrow
(\mathbf Z/4)^\times\cong C_2
\]
を \(2m+1\bmod4\) で定めると、
\[
\boxed{
\operatorname{GT}(K^{(12)})
\cong
\operatorname{GT}(K^{(4)})
\times_{(\mathbf Z/4)^\times}
\operatorname{GT}(K^{(3)}).
}
\tag{2.8}
\]
実際、像は共通 \(\chi_4\) が一致する fiber product に含まれ、その位数は
\[
\frac{4\cdot12}{2}=24
=|\operatorname{GT}(K^{(12)})|
\]
だから等しい。

Thm 4.6 の記法では
\[
\operatorname{GT}(K^{(12)})
\cong\operatorname{Aff}(\mathbf Z/3)\times\widetilde H_2
\]
であり、(2.8) は
\[
(a,h)\longmapsto
\bigl(h,\,(a,\epsilon(h))\bigr),
\tag{2.9}
\]
すなわち odd 側の余分な \(C_2\) が \(h\) の mod-\(4\) sign で決まる graph と読める。これが「\(24\to4\times12\) は指数 \(2\)」の正体で、Thm 4.6 と完全に両立する。

同じ証明は
\[
n=2^\alpha n_0,\qquad \alpha\ge2,\quad n_0>1\text{ odd}
\]
に対し
\[
\boxed{
\operatorname{GT}(K^{(n)})
\cong
\operatorname{GT}(K^{(2^\alpha)})
\times_{(\mathbf Z/4)^\times}
\operatorname{GT}(K^{(n_0)})
}
\tag{2.10}
\]
を与える。群論側の「単射予想」はこれで閉じる。

### Q2.5 算術的同時実現は依然 UNKNOWN

両射影が算術的に全射でも、Galois 像が (2.8) の fiber product 全体とは限らない。二成分が定める固定体を \(L_2,L_{\mathrm{odd}}\) とすれば、必要な次の一点は
\[
\boxed{L_2\cap L_{\mathrm{odd}}=\mathbf Q(\zeta_4)}
\tag{2.11}
\]
（共通 \(\chi_4\)-quotient が定める体）である。交差がこれより大きければ、その余分な交差が Goursat 型 entanglement である。

したがって I-3 は

- 群論: (2.10) まで紙上 PASS、
- 算術: 固定体交差 (2.11) が UNKNOWN、

と分離するのが正しい。

> **★教材 73-2**: \(PB_3\)-像を \(B_3\)-quotient と書くと指数 \(6\) を失う。  
> **★教材 73-3**: 二つの算術射影の全射性は、同時像の fiber-product 全射性を意味しない。共通商を越える固定体交差を別に払う。

---

## Q3. I-2 memo の監査

### Q3.1 補題 U

補題 U は PASS である。上半平面の原始 \(N\) 乗根は
\[
e^{2\pi ik/N},\qquad 0<k<N/2,\quad(k,N)=1
\]
であり、\(\cos\) は \((0,\pi)\) 上 **狭義** 単調減少だから、実部最大は一意に \(k=1\) である。\(N\ge3\) も必要で、\(N=1,2\) では上半平面の根がない。

また、根の一意性から埋め込みの一意性へ進む際に
\[
K_q=\mathbf Q[T]/(\Phi_{4q}),\qquad \bar T\mapsto e^{2\pi i/(4q)}
\]
を明記するという memo の型注意も正しい。

### Q3.2 \(M\mid20\) の意味

TB4-E の証明が本当に使うのは

> Rule 側で凍結した primitive root の level が \(M\) の倍数である

という事実である。K5 では ambient level が
\[
20=2M
\]
だったため \(M\mid20\) と見えていた。族版では ambient level を毎回
\[
2M=4q
\]
に取るので \(M\mid2M\) は自明である。したがって memo の主結論は PASS。

ただし「元の固定体 \(\mathbf Q(\zeta_{20})\) のまま \(M\mid20\) を消した」のではない。固定体を \(\mathbf Q(\zeta_{2M})\) へ動かす **family schema に置換した後**の証明依存である、と限定して書くべきである。

### Q3.3 (E-iii)(E-iv) は同じ意味では I-1 に合流しない

- **(E-iii)** の \(c_\Lambda\) の \(x\)-同変性は、I-1 が供給する (W3)(W4)(W5) と既存の (W1)(W2)(CAL)(TB1)–(TB3) を B-4c に入れて初めて得る。したがって「I-1 が主要な窓固有入力を供給する」は正しいが、(E-iii) 自体を I-1 の一行へ吸収してはいけない。
- **(E-iv)** の
  \[
  \tau(\zeta_M^{\rm Rule})=\tau(X)
  \]
  は root object と marking \(X\) の **命名規約**である。I-1 は \(X\) の位数と torsor 性を与えるが、\(\zeta_M^{\rm Rule}\) を \(X\) に結ぶことはできない。これは family Rule 1 側に残すべきである。

したがって「(E-iii)(E-iv) が共に I-1 へ合流」は差し戻し。(E-iii) の有限群側だけが I-1 から供給され、(E-iv) は I-2 に残る。

### Q3.4 差し戻された二条

1. **\(\bar\iota|_{K_q}=\iota_\infty^{(q)}\)** は必要である。これなしには
   \[
   \bar\iota(\zeta_M^{\rm Rule})=e^{2\pi i/M}
   \]
   を結論できない。完全な制限等式を、生成元一個上の等式へ弱めることは可能だが、何らかの typed compatibility は必須。
2. **(1.7) 族版**は精密化が要る。TB4-E が必要とするのは
   \[
   \zeta_M^{\rm Rule}
   :=(\zeta_{2M}^{\rm Rule})^2
   \tag{3.1}
   \]
   と、その位数が \(M\) であることだけである。memo が併記した
   \[
   \zeta_q^{\rm Rule}:=(\zeta_{4q}^{\rm Rule})^4
   \]
   は TB4-E の証明では使わない。後続 Rule 1 が必要なら残してよいが、TB4-E の load-bearing clause としては過剰である。

結論は、
\[
\boxed{\text{\((1.7)\) の \(\zeta_M\) 部分は必要（または式へ inline 可）、
\(\zeta_q\) 部分は TB4-E には不要。}}
\]

memo の「TB4-E の含意は族で逐語に通るが、各窓が前件を満たすことは別問題」という札も正しい。現段階で family TB4-E を無条件定理とは呼ばない。

---

## Q4. I-4 — \(H^2\) の型修理と fake 探索

### Q4.1 NON-VACUOUS 判定

掃引が空虚でないという falsifier の総論は支持する。中央層で lift defect を実際に計算する必要があり、新しい細分が NFI/isolated のどちらであるかも自動ではない。

ただし次の二つを区別する必要がある。

- 生の中央拡大
  \[
  1\to M\to\widetilde Q\to Q\to1
  \]
  の class
  \[
  [\xi]\in H^2(Q,M);
  \]
- target shadow \(g\) が \(Q,M\) に誘導する作用
  \((a_g,b_g)\) に対する lift defect
  \[
  \operatorname{ob}_\xi(g)
  :=b_{g*}[\xi]-a_g^*[\xi]\in H^2(Q,M).
  \tag{4.1}
  \]

中央拡大の通常の lifting criterion は
\[
g\text{ がこの層へ lift}
\iff \operatorname{ob}_\xi(g)=0
\tag{4.2}
\]
である。したがって、他の marking/charming 条件も満たす固定 tower では
\[
R\text{ 全射}
\iff
\operatorname{ob}_\xi(g)=0
\quad(\forall g\text{ in target}).
\tag{4.3}
\]

一方、
\[
R\text{ 全射}\iff[\xi]=0
\tag{4.4}
\]
は一般には偽である。反例は非分裂中央拡大
\[
1\to C_2\to C_4\to C_2\to1.
\]
その class は \(H^2(C_2,C_2)\) で非零だが、商 \(C_2\) の自己同型は恒等しかなく、それは \(C_4\) へ lift する。よって reduction は全射である。

従って falsifier の \([\xi_r]\) が便 20 G3′ の **raw extension class** を指すなら括弧書きの iff は差し戻す。もし「全 target shadow に付く obstruction の束」を指していたなら内容は正しいが、記号を
\(\operatorname{ob}_r\) に改めるべきである。

### Q4.2 G3′ の族的見通し

便 20 G3′ の
\[
M^\sigma=0,\qquad
M^\theta=(1+\theta)M
\tag{4.5}
\]
は raw \([\xi]\) を零にする条件ではなく、E23 型 defect の **着地点を零にする十分条件**である。この読みなら現在も有効である。

特に \(M\) が odd order で \(\theta^2=1\) なら、\(2^{-1}\) が存在するため
\[
M^\theta=(1+\theta)M
\tag{4.6}
\]
は自動である。実際 \(m\in M^\theta\) に対し
\(m=(1+\theta)(m/2)\)。したがって odd 中央層では非自明な判定は主に
\[
M^\sigma=0
\tag{4.7}
\]
へ縮む。

odd \(G_n\) の三つの sign-character 分解は、この検査に適している。対象中央層が \(\sigma\) の \((-1)\)-固有成分だけから成れば、\(2\) が可逆なので (4.7) が成立する。一方、\(+1\)-成分を一つでも含めば obstruction の **居場所**が残る。ただし居場所が非零でも実際の \(\operatorname{ob}_r\) が非零とは限らない。

族定理として狙うべき安全な形は次である。

> 各中央層で (4.5) が成立し、各段の quotient/marking が正しく lift されるなら、全 target shadow は中央列に沿って帰納的に lift する。

raw extension class の split 性は前件にしない。

### Q4.3 探索順序の反転

「非全射 edge を先に探す」は妥当である。ただし結論は element-level に書く。

1. \(L\le N\) を事前登録し、\(R_{L,N}\) の **完全な像**を得る。
2. \(a\in\operatorname{GT}(N)\setminus\operatorname{Im}R_{L,N}\) を一つ明示する。
3. 2401 Cor. 5.4 により、その \(a\) は fake。

したがって
\[
R_{L,N}\text{ 非全射}
\Longrightarrow
\text{少なくとも一つの finite fake certificate}
\tag{4.8}
\]
である。全射だった場合は一つの必要条件を通っただけで、genuine/arithmetical は従わない。

なお fake witness のために **source \(L\) の isolated 性は不要**である。isolated 性が必要なのは \(L\) を Main Line の群対象として扱う場合であり、Cor. 5.4 の一細分反証を得るために先払いしてはいけない。ただし非 isolated source で実装するなら、reduction の定義域を勝手に \(\operatorname{GT}(L)\) の一部分へ狭めず、Cor. 5.4 が要求する lift 全体を完全列挙すること。

探索優先度は

- (4.5) により自動全射が予測される層を後回し、
- \(M^\sigma\ne0\) または Tate defect space が非零の層を先行、
- その後に実際の \(\operatorname{ob}_r\) を計算、

とするのがよい。「obstruction space 非零」を「obstruction 非零」と読まないこと。

> **★教材 73-4**: extension class と automorphism-lift defect は同じ \(H^2\) に住んでも別 object である。生の拡大が非分裂でも全自己同型が lift することはある。

---

## Q5. I-5 — odd 算術心臓と最初の述語試験

### Q5.1 単離の射程

odd \(n\) で
\[
M=2n,\qquad e=n,\qquad
F_n:=\mathbf Q(\zeta_{4n})
\]
とする。I-1 の窓条件、I-2 の root/marking 条件、BFC の比較前件、定理
\(R^{\rm cyc}_{\rm formal}\) の全前件が揃った **各窓ごと**には
\[
\operatorname{Ih}_{K^{(n)}}\text{ 全射}
\iff
\operatorname{ord}(a_n)=n,
\qquad
a_n:=[u_n^{-1}]_{2n}
\in F_n^\times/F_n^{\times 2n}.
\tag{5.1}
\]
この conditional isolation は正しい。

ただし I-1 と I-2 だけで (5.1) が出るわけではなく、(5′) を供給する比較橋などを省略しないこと。また formal theorem が与える
\[
\operatorname{ord}(a_n)\mid n
\tag{5.2}
\]
も前件成立後の帰結である。

### Q5.2 型だけの挟み撃ちは有望でない

私は反例枝、より正確には **\(n\)-依存の Kummer/Selmer 枝**を優先する。

全分岐指数 \(M\)、\(|\mathfrak F_0|=n\)、regular detector という型は (5.2) の上界を説明するが、下界を与えない。同じ \(M,e\) の Kummer torsor 型に、位数 \(1\) の class と真の約数位数の class と位数 \(n\) の class が共存し得る。幾何 cusp の全分岐性と、係数が定める Galois Kummer class の full order は別命題である。

したがって「\(u_n\) の値を一切使わない型論」だけから
\(\operatorname{ord}(a_n)=n\) を出すには、現在の前件にはない新しい幾何定理、例えば divisor/valuation の primitive 性が必要である。現状の型から無償には出ない。

また「類群が大きい \(n\)」だけを危険地帯とするのも粗い。まず divisor の \(2n\)-可除性を分離し、その後に \(S\)-unit と class-group obstruction が現れる。類数表だけで \(a_n\) の order は決まらない。

### Q5.3 exact な predicate vector

(5.2) の下では
\[
\boxed{
\operatorname{ord}(a_n)=n
\iff
a_n^{\,n/p}\ne1
\quad\text{for every prime }p\mid n.
}
\tag{5.3}
\]
これは必要十分である。proper divisor \(d<n\) なら、ある \(p\mid n\) について \(d\mid n/p\) となるからである。

従って first test は、class representative を表示せず
\[
\mathcal P_{n,p}:=
\bigl[a_n^{\,n/p}\ne1\bigr]
\tag{5.4}
\]
という boolean 群だけを返せばよい。結果型は

```text
FULL_p_DEPTH / DEPTH_DROP / UNKNOWN
```

とし、代表元・平方類・係数値は出力しない。

### Q5.4 最鋭の最初の窓

運用上の次窓 \(n=5\) では (5.3) は単なる \(a_5\ne1\) である。素数窓なので「非自明か」しか測れず、型挟み撃ちと \(p\)-進深さを区別しにくい。

科学的に最も識別力のある最初の窓は
\[
\boxed{n=9.}
\]
formal upper bound \(\operatorname{ord}(a_9)\mid9\) の下で
\[
\boxed{\operatorname{ord}(a_9)=9\iff a_9^3\ne1.}
\tag{5.5}
\]

- \(a_9^3\ne1\): full \(3^2\)-depth。
- \(a_9^3=1\): order は \(1\) または \(3\) へ落ち、型だけの楽観枝を反証。

という一ビットで明確に分かれる。実行順序は I-1/I-2/BFC 前件を先に閉じ、その後に (5.5) を封印述語として測る。現時点の値は UNKNOWN であり、本返信では計算していない。

> **★教材 73-5**: \(n=5,7\) の prime test が続いても prime-power depth の証拠にはならない。最初の識別点は \(n=9\) の「order \(3\) で止まるか、\(9\) まで上がるか」である。

---

## Q6. 共同設計者としての代案

### Q6.1 reduction-functorial detector tower

Q1 の多数の class から値を見て一つを選ぶ代わりに、値を見る前に
\[
\boxed{
H_n^{\mathrm{fun}}:=H_{2,1,0}
=\langle a_2,\ a_1a_3,\ q_2\rangle
}
\tag{6.1}
\]
を全 odd \(n\) で事前固定することを提案する。

\(d\mid n\) に対する自然な marked quotient
\[
P_n\twoheadrightarrow P_d
\]
は
\[
H_n^{\mathrm{fun}}\twoheadrightarrow H_d^{\mathrm{fun}}
\tag{6.2}
\]
を誘導し、coset cover に
\[
P_n/H_n^{\mathrm{fun}}\longrightarrow
P_d/H_d^{\mathrm{fun}}
\]
という次数 \(n/d\) の写像を与える。\(\alpha=1\) はどの divisor でも \(0\) に退化しないため、全段で good のままである。

これは (W5) が与えられなかった class selector を **poset functoriality** から与える。K5 の `all_two_classes` blind 規律を過去に遡って変更するものではない。次の族定理で用いる detector を、将来値と独立に事前登録する提案である。

### Q6.2 算術を窓ごとの孤立計算から tower compatibility へ移す

(6.2) を pointed cover と局所座標まで持ち上げられれば、各段の Kummer class の間に typed な関係が生じるはずである。狙うべき候補式は、\(d\mid n\) に対して
\[
\operatorname{res}_{F_n/F_d}(a_d)
=a_n^{\,n/d}
\quad\text{in}\quad
F_n^\times/F_n^{\times 2d}.
\tag{6.3}
\]
現時点で (6.3) は **UNKNOWN** であり、主係数の値から推測して採用してはならない。cover composition と局所 parameter の functorialityから先に証明すべき式である。

もし \(n=p^k,d=p^{k-1}\) で (6.3) が成立し、下段 class が full order \(p^{k-1}\) なら、上段の \(p\)-depth を強制できる。これが成立すれば、I-5 は「各 \(n\) の class を独立に計算」から「prime-power tower の一段 compatibility を証明」へ変わる。

### Q6.3 mixed 側の新しい基本量

Q2 の群論的 fiber product を受けて、mixed 窓には
\[
\mathcal E_n:=
\operatorname{Gal}\!\left(
(L_{2^\alpha}\cap L_{n_0})/\mathbf Q(\zeta_4)
\right)
\tag{6.4}
\]
を entanglement invariant として置くことを提案する。

- \(\mathcal E_n=1\): componentwise saturation から mixed saturation へ進める。
- \(\mathcal E_n\ne1\): 同時実現の正確な余分障害。

これなら「Kummer 部が絡むかもしれない」を、計算・証明可能な一つの有限 Galois 群へ落とせる。最初の対象は \(n=12\) でよい。

### Q6.4 推奨順序

1. 命題 ODD-H を第二数学者が独立監査し、I-1 の観測則を paper-proof candidate へ上げる。
2. 次の GAP 便の (W5) は selector 探索でなく、全 \(n-1\) 類 PASS を期待する regression として実行する。
3. \(H_n^{\mathrm{fun}}\) の quotient compatibility (6.2) を紙上定理化する。
4. mixed は (2.10) を群論正本にし、\(n=12\) の \(\mathcal E_{12}\) を調べる。
5. odd 算術は prime 窓の後、最初の深さ試験を \(n=9\) の述語 (5.5) に置く。

---

## 監査範囲・状態

全文を読んだ対象と SHA-256:

```text
3e0d7233323b571479ba8281914572414816255e3b706666141d1ebac1a2c0ea  ideas/ideas_001_odd_family.md
89f45085cd89604c021177b7c0cd2aef96d31e6555b59f49e585ab1484276772  docs/notes/i2_family_rule1_memo_v1.md
2272695979c8d5664d00f4bb4876990d3826bbc9644b46f8e742a58c9cc50a74  search/certs/i1_survey_20260728.json
55235296ab6ab82f8a4c54e4c04b4e63855b81b8a2b1a76fbdbbc61c9858b6cd  search/certs/i3_equality_20260728.json
1d07056f6ab04da4c5f5567c01bbaaf0290f116808462b6bf5cb624a2cde9309  provenance/registered/universe_I1_I3.md
```

memo digest は便記載値と一致した。両 JSON の script digest と現物
`search/family-window-survey.g` /
`search/mixed-equality-check.g` も一致した。正典 PDF は p.15 の
\(|G_n|\) 分岐、p.20 の Prop. 4.5、p.22 の Thm 4.6 を頁画像で再照合した。

監査範囲外:

- I-1/I-3 の独立 checker の実装・実行。
- (6.3)、(6.4) の算術計算。
- 各窓の (E-iii)(E-iv) 実供給。
- \(a_n\) の predicate の実測。
- freeze/契約層 B72-1〜4。

\(u\) の値、\(u/c\) の平方類、\(\widehat c_\mu\) は計算も表示もしていない。
