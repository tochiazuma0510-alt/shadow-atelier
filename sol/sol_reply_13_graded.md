# Sol 第 13 便 — E2 graded 再定式化と掃引 ① の発射監査

## 冒頭結論

| 対象 | 裁定 |
|---|---|
| Lemma A | **PASS（中間式一箇所の訂正つき）**。\(\mathcal N(p+q)=3\rho\) は正しい。ただし v2 §1.2 の \(\sigma^2(p+q)\) の表示は誤植で、正しくは \(-q+r_1+(m+2)r_2+2r_3\)。最終和はこの正しい係数を既に使っている。 |
| Lemma B と \((\dagger)\) | **paper mutual-audit PASS / candidate**。固定空間の二次元性、\(w\)-座標、Magnus の \(\xi^2\eta^2\)-係数を独立に追うと \(3E_m=-T_m\kappa_m+B_m\rho\) が出る。Lemma A と合わせて \((\dagger)\) は script に依存せず閉じる。Lean verified ではない。 |
| 命題 E16 | **現状の定理文は FAIL、class \(\le2\) の系は生存**。「\(\theta(A^\sigma)=A^\sigma\)」だけでは必要性を示せない。証明が実際に使うのは \(e\theta=\theta e\)、同値に \(A^\sigma\) と \(\ker\mathcal N\) の双方の \(\theta\)-安定性である。\(\iota_{X^u}=1\) ならこの強い仮定が成立するので E16-a は正しい。 |
| 補題 E18.1 / E18.2 | **E18.1 PASS。E18.2 は結論 PASS、証明語句を補修**。crossed product の行列環同型は使えるが、「単純加群は \(R\) のみ」「任意の加群が \(\mathbb Z_2[C_2]\)-自由」は誤り。Morita 同値と normal integral basis により「induced なので Tate cohomology が消える」と直せばよい。 |
| 定理 E18 と \(O_j\) | **中心主張は FAIL / 要再定式化**。真の局所 cokernel は \((M_j^{\bar\sigma})^{\bar\theta}\) であり、文書の \(O_j=(1+\bar\theta)M_j^{\bar\sigma}\) は「強制される欠損の像」であって障害群ではない。有限 2-primary 層では \(\bar\theta=-1\) でも位数 2 元が固定されるため、\(O_j=0\) から障害消滅は出ない。 |
| weight 5 初出 | **有理表現論として PASS**。自由 Lie 環および自由 metabelian graded の指標表は正しく、自明 \(\mathbb Q[S_3]\)-成分の初出は weight 5。ただし E18 の逆が未閉鎖なので、これだけを E9/E9′ の再証明とは呼べない。class 5 を最優先にする構造的根拠としては有効。 |
| 定理 E19 | **\(c=3,\ldots,7,\ m=0,\ldots,63\) の単系統 candidate のまま**。開示された `metab.mjs` のモデルと合同系の組み立ては概ね整合するが、数値出力を Sol は再実行していない。内蔵 `snf` は canonical Smith 形でなく整数対角化であり、第二系統が必須。 |
| 系 E19-b | **FAIL**。\(M(m)\bmod2\) の \(m\bmod8\) 周期性は正しいが、「Smith の全非零因子が奇数」は mod \(2\) 行列だけでは決まらない。有理 rank が同じ剰余類内で増える可能性を排除していないため、\(0..63\) から全 \(m\) への拡張は未成立。 |
| 便 12 ★ の逆修正 | **限定的に承服、一般形は反駁**。開示計算が正しければ、指定範囲の自由 metabelian 塔では 2-adic divisibility obstruction は実現していない。しかし「残余条件が \(C_2\)-側に載る」という便 12 の構造判断は反証されておらず、metabelian class \(\ge8\) と全 \(m\) も UNKNOWN。「生存層は class-5 非 metabelian だけ」は言えない。 |
| 定理 E21 | **PASS**。\(A/(\gamma_3[A,A]A^2)\cong C_2\) は常に非自明な同時 \(\sigma,\theta\)-不変一次元指標を与える。E12-a は本設定の非可換 \(P\) には適用不能。 |
| 補題 E22 | **積公式 PASS、持ち上げ枠組みは未完**。norm の双加法補正は正しい。しかし (H-a) にも \([\theta(g),f]\) という中心的二次補正があり、canonical section の cocycle も必要である。「線型判定 + E22 の一形式」だけでは十分性がまだない。 |
| 掃引 ① | **現仕様は NO-GO**。非可換 \(A\) に \(A\otimes\mathbb Z/2^j\) は定義できず、有限化・二つの中心欠損・全数性 certificate・cap の単位が未固定である。これらを versioned な修正版宇宙へ直せば、\(j\le6,m\le63\) の**有限 falsification battery**として GO。通過を class 6 への移動理由にはしない。 |

★ graded 解析の正しい成果は、「\(\sigma\)-非自明部は induced module なので局所 cokernel を持たず、問題は \(\sigma\)-固定部へ集約される」ことである。しかし、その局所 cokernel は

\[
\boxed{\quad
C_j=(M_j^{\bar\sigma})^{\bar\theta},
\quad}
\]

であって \((1+\bar\theta)M_j^{\bar\sigma}\) ではない。特に有限 2 群では「符号作用 \(-1\)」と「固定点なし」は同義でない。位数 2 元上では \(-1=+1\) だからである。この一点が、今回の graded 枠組みと発射仕様をそのまま採用できない理由である。

---

## 1. Lemma A/B と \((\dagger)\)

### F1. Lemma A は中間式を直せば閉じる

v2 の構造定数から

\[
\sigma(p+q)
=-p+2r_1+(1-m)r_2+r_3.
\]

さらに

\[
\begin{aligned}
\sigma^2(p+q)
&=-\sigma(p)+2\sigma(r_1)+(1-m)\sigma(r_2)+\sigma(r_3)\\
&=-q+r_2-mr_3
  +2r_3+(1-m)(-r_2-r_3)
  +(r_1+2r_2+r_3)\\
&=\boxed{-q+r_1+(m+2)r_2+2r_3}.
\end{aligned}
\]

v2 §1.2 の表示

\[
-q+r_1+(1+m)r_2+(2+m)r_3
\]

は、第一項 \(-\sigma(p)=-q+r_2-mr_3\) の中心座標を最後に足し忘れたものになっている。ただし直後の総和では

\[
(1-m)+(2+m)=3,\qquad 1+2=3
\]

と、正しい \((m+2,2)\) を使っている。従って結論

\[
\boxed{\mathcal N(p+q)=3(r_1+r_2+r_3)=3\rho}
\]

は正しい。この誤植は Lemma A を壊さないが、紙上証明の正本では直す必要がある。

構造定数自体も、v2 §3.3 の metabelian module 写像

\[
\tau(f)(s,t)=f\bigl(t,(st)^{-1}\bigr)s^{-1}
\]

を次数 2 まで展開すれば、

\[
\tau(1)=1-S+S^2,\quad
\tau(S)=T-ST,\quad
\tau(T)=-S-T+2S^2+2ST+T^2
\]

および

\[
\tau(S^2)=T^2,\quad
\tau(ST)=-ST-T^2,\quad
\tau(T^2)=S^2+2ST+T^2
\]

が紙上で再現できる。従って Lemma A は `class4.mjs` の実行結果を仮定しなくても閉じる。

### F2. Lemma B の二つの座標抽出は独立である

\(E_m,\kappa_m,\rho\) が \(\sigma\)-固定であり、

\[
\dim_{\mathbb Q}(A_{\rm free}^{\sigma})=2,\qquad
A_{\rm free}^{\sigma}\otimes\mathbb Q
=\mathbb Q\kappa_m\oplus\mathbb Q\rho
\]

となる議論は正しい。graded weight \(2,3,4\) の固定次元が \(1,0,1\) 以下で、\(w\)-係数を持つ \(\kappa_m\) と weight 4 の \(\rho\) が独立だからである。

従って

\[
E_m=a\kappa_m+b\rho.
\]

\(w\)-座標

\[
(E_m)_w=-T_m,\qquad(\kappa_m)_w=3
\]

から \(a=-T_m/3\) が出る。

残る \(b\) の抽出について、v2 §1.6 の Magnus 係数を追い直した。選択語 \(u_0=\xi^2\eta^2\) に対し、

\[
c_{u_0}(W_4)=
c_{u_0}(W_2^2)=
c_{u_0}(P_4)=0,\qquad
c_{u_0}(Q_4)=-1
\]

であり、

\[
c_{u_0}(\mu(E_m))=-\binom{m+1}{4}.
\]

一方、\(\rho\) の \(q\)-座標は 0 なので

\[
(E_m)_q=-\frac{T_m(m-1)}3=-\binom{m+1}{3}.
\]

従って

\[
(E_m)_{r_2}
=-\,(E_m)_q-c_{u_0}(\mu(E_m))
=\binom{m+2}{4}.
\]

ここには Lemma B の結論を先取りする循環はない。使っているのは、固定空間が \(\kappa_m,\rho\) で張られることと、\(\rho_q=0\) までである。よって

\[
3b
=3\binom{m+2}{4}+T_m
=\binom{T_m}{2}+T_m
=B_m
\]

となり、

\[
\boxed{3E_m=-T_m\kappa_m+B_m\rho}
\]

を得る。

### F3. \((\dagger)\) は paper mutual-audit PASS へ上げてよい

\[
f_0=3T_mw-B_m(p+q)
\]

に対し Lemma A/B から

\[
\begin{aligned}
\mathcal N(f_0)
&=3T_m\kappa_m-3B_m\rho\\
&=3T_m\kappa_m-3(3E_m+T_m\kappa_m)\\
&=-9E_m.
\end{aligned}
\]

これが加法表示の \((\dagger)\) である。さらに

\[
3\lambda^2\equiv\lambda,\qquad
9\lambda^2\equiv1\pmod{\exp A}
\]

なので、

\[
f=\lambda^2f_0
=\lambda T_mw-\lambda^2B_m(p+q)
\]

は \(\mathcal N(f)=-E_m\) を満たす。\(\theta(w)=-w\)、\(\theta(p+q)=-(p+q)\) から (H-a) も満たす。

従って E9′ の中心恒等式は、便 12 の「単系統」保留を解除し、

\[
\texttt{paper mutual-audit PASS / candidate}
\]

へ上げてよい。`docs/scout/class4.mjs` と `docs/scout/metab.mjs` の一致は補助的な照合であり、この昇格自体は script に依存しない。

---

## 2. graded 枠組みの監査

### F4. 命題 E16 は仮定が一つ足りない

E16 の十分方向は実は簡単である。\(\theta(E_m)=-E_m\) なら

\[
b=-\lambda E_m\in A^\sigma
\]

は \(\theta(b)=-b\) かつ

\[
\mathcal N(b)=3b=-E_m
\]

を満たす。

しかし必要方向で v2 が使う

\[
\theta\mathcal N\theta=\mathcal N
\]

は、定理文の仮定 \(\theta(A^\sigma)=A^\sigma\) からは出ない。この仮定は \(A_+\) を保つだけで、指定された補空間

\[
A_-=\ker\mathcal N
\]

まで保つとは限らない。

抽象反例を一つ与える。加法群

\[
A=C_4\oplus C_4^2
\]

で

\[
\sigma(a,x)=(a,Sx),\qquad
S=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},
\]

とする。\(S^3=1\)、\(1+S+S^2=0\) なので \(A^\sigma=C_4\oplus0\)。\(\varphi(x_1,x_2)=x_1\) と置き

\[
\theta(a,x)=(a+\varphi(x),-x)
\]

とすれば \(\theta^2=1\) かつ \(\theta(A^\sigma)=A^\sigma\) である。\(x=(2,0)\)、\(b=(1,x)\) とすると

\[
\theta(b)=-b,\qquad
\mathcal N(b)=(3,0).
\]

\(E=-\mathcal N(b)=(1,0)\) と置けば同時解はあるが

\[
\theta(E)=E\ne-E.
\]

これは braid 由来の追加関係を課した反例ではないが、**E16 の記載された抽象仮定と証明が不足している**ことを示す。

正しい修正版は、例えば

\[
\boxed{e\theta=\theta e}
\]

または同値な

\[
\theta(A_+)=A_+,\qquad\theta(A_-)=A_-
\]

を仮定することである。厳密な \(S_3\) 関係

\[
\theta\sigma\theta=\sigma^{-1}
\]

はこの条件を保証する。

従って v2 D3 の

\[
\theta(A^\sigma)\text{ を保つ}
\quad(=\ \iota_{X^u}|_A=\mathrm{id})
\]

という等号も誤りである。E16.1 が示すのは

\[
\theta(A^\sigma)\subseteq A^\sigma
\iff
\iota_{X^u}|_{A^\sigma}=\mathrm{id}
\]

までであり、\(\iota|_A=1\) は十分条件にすぎない。

ただし \(\iota|_A=1\) の場合は真の \(S_3\) 関係が回復する。charming 条件下でこれが class \(\le2\) と同値である E2′-a は前便までに閉じているので、E16-a の class \(\le2\) 結論は生存する。

### F5. E18.1 は PASS、E18.2 は Morita の言葉で直す

任意の \(g\in P\) について

\[
(\iota_g-1)\gamma_j\subseteq\gamma_{j+1}
\]

なので、inner twist と \(\operatorname{Ad}(Y^m)\) が \(M_j\) 上で消える E18.1 は正しい。従って associated graded 上では

\[
\bar\theta\bar\sigma\bar\theta=\bar\sigma^{-1}
\]

という \(S_3\) 関係が成立する。

\(M_j^-\) についても結論

\[
\widehat H^*(C_2,M_j^-)=0
\]

は正しい。指数 \(2^e\) の層なら

\[
R_e=(\mathbb Z/2^e)[\omega]
\]

とし、Frobenius を \(\bar\theta\) として

\[
R_e\#C_2
\cong
\operatorname{End}_{\mathbb Z/2^e}(R_e)
\cong
M_2(\mathbb Z/2^e)
\]

を使える。normal integral basis により、\(R_e\) は \(C_2\)-加群として \((\mathbb Z/2^e)[C_2]\) と同型である。Morita 同値で任意の crossed-product module は

\[
R_e\otimes_{\mathbb Z/2^e}N
\]

の形になり、\(C_2\) へ制限すると induced module になる。従って Tate cohomology が消える。

ただし v2 の

- 「行列環の単純加群は \(R\) 自身のみ」、
- 「任意の加群は \(\mathbb Z_2[C_2]\)-自由」、

という表現は正しくない。\(M_2(\mathbb Z_2)\) は semisimple 環ではなく、有限 torsion module は \(\mathbb Z_2[C_2]\)-自由でもない。必要なのは **free ではなく induced** である。この修文なら

\[
\ker(1-\bar\theta)=(1+\bar\theta)M_j^-,
\qquad
\ker(1+\bar\theta)=(1-\bar\theta)M_j^-
\]

は維持できる。

### F6. 真の graded cokernel

\[
M=M^+\oplus M^-,
\qquad
M^+=M^{\bar\sigma},
\qquad
M^-=\ker\bar{\mathcal N}
\]

とし、

\[
\Psi:M\longrightarrow M^{\bar\theta}\oplus M^+,\qquad
g\longmapsto((1+\bar\theta)g,\bar{\mathcal N}g)
\]

を考える。第二成分を \(\delta\)、第一成分を \(\varepsilon\) と書くと、

\[
g_+=\lambda\delta
\]

で強制される。従って

\[
\varepsilon_+
=\lambda(1+\bar\theta)\delta
\]

が必要であり、\(M^-\) 成分は E18.2 により常に埋められる。

ここから得られる正確な写像は

\[
\Phi:M^{\bar\theta}\oplus M^+
\longrightarrow (M^+)^{\bar\theta},
\qquad
\Phi(\varepsilon,\delta)
=\varepsilon_+-\lambda(1+\bar\theta)\delta.
\]

E18.2 を使えば

\[
\ker\Phi=\operatorname{im}\Psi
\]

であり、\(\Phi(h,0)=h\) なので全射でもある。従って

\[
\boxed{\quad
\operatorname{coker}\Psi
\cong
(M^+)^{\bar\theta}.
\quad}
\]

これが局所的な**潜在障害群**である。

一方、v2 の

\[
O_j=(1+\bar\theta)M_j^+
\]

は \(\delta\) が動いたときに右辺へ現れる**像**であり、cokernel ではない。最小反例は

\[
M=C_2,\qquad\bar\sigma=1,\qquad\bar\theta=1=-1.
\]

このとき文書の \(O=(1+\bar\theta)M=2M=0\) だが、

\[
(\varepsilon,\delta)=(1,0)
\]

は自然な target \(M^{\bar\theta}\oplus M^+\) に属しながら \(\Psi\) の像に入らない。真の cokernel は \(M\ne0\) である。

従って有限 2-primary 層で

\[
\bar\theta=-1\text{ on }M^+
\]

を「障害なし」の正本判定にしてはならない。\(-1\) 作用でも

\[
(M^+)^{\bar\theta}=M^+[2]
\]

が残る。

### F7. weight 5 の指標表は正しいが、意味を限定する

自由 Lie 環の Witt 指標

\[
\chi_{L_n}(g)
=\frac1n\sum_{d\mid n}\mu(d)\chi_V(g^d)^{n/d}
\]

から自明表現と符号表現の重複度を再計算した。v2 表 1(a) の \(j=2,\ldots,10\) は一致する。自由 metabelian 側

\[
M_j\otimes\mathbb Q
\cong
\operatorname{Sym}^{j-2}(V)\otimes\operatorname{sgn}
\]

についても、最初の自明成分は \(j=5\) である。

従って次は採用できる。

> torsion-free universal latticeを \(\mathbb Q\) 化したとき、\((M_j^+)^{\bar\theta}\otimes\mathbb Q\) の初出は weight 5 である。

これは class 5 を第一撃にする強い構造的理由である。

しかし次はまだ採用できない。

> \(j\le4\) で graded 自明表現がないことだけから、有限 2 群上の同時方程式が解ける。

理由は二つある。

1. 有限 2-torsion では符号成分にも固定点 \(M[2]\) がある。
2. v2 自身が E18 の逆、すなわち graded correction の厳密な持ち上げを【GAP-E18】として残している。

従って表 1 は E9/E9′ の**構造的説明**ではあるが、E9/E9′ の独立な再証明や contracting homotopy の完成ではない。

---

## 3. 定理 E19 と `metab.mjs`

### F8. 開示 script の静的監査

`docs/scout/metab.mjs` を全文読んだ。監査対象の SHA-256 は

```text
45CEA39CD2A3FD80C999DB21C5411B32202A50DFA744E48B0A86863F08FC09D9
```

である。静的に確認できた長所は次である。

- \(A_c=\mathbb Z[S,T]/(S,T)^{c-1}\) の monomial basis と \(\theta,\tau,\sigma_m,E_m\) が全て BigInt の切断多項式で組まれている。
- 行ベクトル規約の `matOf` に対し、合同系を作る箇所では行列を転置して通常の \(Mx=b\) 形に戻している。向きは整合する。
- \((1+\theta)f=0\) と \(\mathcal Nf=-E_m\) の二系を同じ未知ベクトルへ積み、行変換 \(U\) を右辺にも適用している。
- 13 個の fixture は、class-4 の構造定数、\(E_1,E_2,E_3\)、命題 E1、Lemma A/B を含む。

ただし状態札を上げられない理由も明瞭である。

1. `snf` は pivot を Euclid 操作で孤立させる**整数対角化**であり、対角成分の正値化・整除鎖 \(d_i\mid d_{i+1}\) を作らない。従って出力は canonical Smith 基本因子ではない。
2. 列変換 \(V\) を保存せず、\(UMV=D\)、\(D\) の対角性、\(U,V\) の unimodularity を postcondition として再検査していない。
3. main output は `max_v2` だけで、§4.2 が要求する `elementary_divisors` の全リストを出力しない。従って現状のまま GAP 出力との「バイト一致」は実行不能である。
4. self-test が FAIL しても結果部分へ進む。`fails>0` なら非零終了して main sweep を禁止すべきである。
5. default は `maxM=31` なので、文書の \(0..63\) を再現するには明示コマンド
   ```text
   node docs/scout/metab.mjs 7 63
   ```
   が必要である。exact command、stdout、exit code、script hash がまだ certificate として固定されていない。

対角化が本当に unimodular 同値を保っているなら、「全 pivot が奇数」という一点は canonical divisibility chain を要しない。mod \(2\) rank と有理 rank が一致するからである。しかし現状はその postcondition 自体が自己検査されていない。従って数値表は

\[
\texttt{Z2-solvable candidate (single system, statically audited)}
\]

のままとする。

### F9. E19 の第二系統は三段に分ける

第二系統は単に同じ \(M,b\) を別 SNF routine へ渡すだけでなく、次の三段を分離すべきである。

1. **model 照合**: GAP 側で monomial basis、\(\theta,\tau,\sigma_m,E_m\) を独立に構成し、各 \((c,m)\) の `M_content_hash` と `b_content_hash` を比較する。
2. **linear algebra 照合**: GAP の canonical Smith 形で、正の invariant factors、rank over \(\mathbb Q\)、rank over \(\mathbb F_2\)、\(Ub\) の零行条件を保存する。
3. **witness 照合**: 可解例では各 \(j=1,\ldots,6\) について少なくとも一つの \(f\) を復元し、二方程式の residual を元の \(M,b\) へ直接代入する。否定例なら便 12 の dual witness を出す。

node 側も canonical SNF list を比較したいなら、\(V\) と divisibility normalization を追加する必要がある。追加しない場合は、「byte equality」ではなく

\[
\operatorname{rank}_{\mathbb Q},\quad
\operatorname{rank}_{\mathbb F_2},\quad
\text{可解性},\quad
\text{直接 witness residual}
\]

を比較対象にする。

### F10. Lucas は mod 2 周期性までしか与えない

\[
(1+T)^8=1+T^8\equiv1\pmod{2,\ (S,T)^6}
\]

なので、\(c\le7\) では \(\sigma_m\) および \(M(m)\bmod2\) が \(m\bmod8\) のみに依存することは正しい。これは負の \(m\) も含め、Lucas より切断環の単元の位数で述べる方が明瞭である。

しかし

\[
M(m)\bmod2\text{ が同じ}
\]

から

\[
\text{全ての非零 Smith 因子が奇数}
\]

は従わない。後者は

\[
\operatorname{rank}_{\mathbb Q}M(m)
=
\operatorname{rank}_{\mathbb F_2}M(m)
\]

と同値であり、有理 rank は mod \(2\) 行列だけでは決まらない。

例えば

\[
D(t)=
\begin{pmatrix}
1&0\\
0&2t
\end{pmatrix}
\]

は全ての \(t\) で同じ mod \(2\) 行列を持つが、\(t=0\) では非零因子は \(1\) だけ、\(t=1\) では \(1,2\) となる。この例が示すように、同じ剰余類の未検査 \(m\) で有理 rank が増え、偶数因子が新しく現れる可能性を消す必要がある。

E19-b を閉じるには、各 \(m\bmod8\) について

\[
\operatorname{rank}_{\mathbb Q}M(m)
=r_{\bar m}
\]

が全整数 \(m\) で一定であり、その \(r_{\bar m}\) が mod \(2\) rank と等しいことを、記号的 row relation または minors で示せばよい。現在の \(0..63\) の有限表だけではその証明にならない。

従って採用可能な射程は

\[
c=3,\ldots,7,\quad m=0,\ldots,63
\]

の単系統 candidate までである。全 \(m\) への E19-b、そこから導く「素数 2 は完全に落ちた」は保留する。\(\mathbb Q\)-可解性の全 \(m\) も、文書自身が【GAP-E19】に残している。

### F11. 便 12 ★ への最終回答

便 12 の ★ は、

> \(C_3\)-norm は 3 可逆性で解け、残る同時条件は \(C_2\)-反不変性との交差にある

という**障害の所在**を述べたものであり、「必ず 2-adic divisibility obstruction が実現する」とは述べていない。今回の計算候補は、指定した自由 metabelian 塔でその潜在障害が実現しなかった、という強い負のデータである。

従って私は次の限定修正には承服する。

> `metab.mjs` の結果が第二系統と一致すれば、自由 metabelian \(c\le7,m\le63\) では高い \(2\)-冪で初出する divisibility obstruction はない。

しかし次の一般化には反駁する。

- 全 metabelian 塔に 2-primary obstruction は存在しない。
- class \(\le7\) の全 \(m\) で存在しない。
- 生存層は class-5 非 metabelian だけである。

少なくとも metabelian class \(\ge8\)、class \(\le7\) の未量化 \(m\)、および E19 の第二系統は残る。従って class-5 非 metabelian は**唯一の層**ではなく、現在もっとも情報価値の高い**第一優先層**と書くのが正しい。

---

## 4. E21 と E22

### F12. 定理 E21 は完全

\[
B=\gamma_3[A,A]A^2
\]

は \(\sigma,\theta\)-安定であり、

\[
A/B
\cong
(\gamma_2/\gamma_3)/(\gamma_2/\gamma_3)^2.
\]

2 生成非可換有限 2 群では \(\gamma_2/\gamma_3\) は \(w=[X,Y]\) で生成される非自明巡回 2 群なので、

\[
A/B\cong C_2.
\]

また

\[
\sigma(w)\equiv w\pmod{\gamma_3},\qquad
\theta(w)=w^{-1}\equiv w\pmod{A^2}.
\]

従って \(A/B\) は自明な \(\langle\sigma,\theta\rangle\)-加群であり、その非自明な双対指標は同時安定である。よって E12-a の「同時安定既約は自明だけ」という仮定は本設定の非可換 \(P\) では成立しない。

この結論は高次元既約表現を調べる必要すらなく、一次元指標だけで閉じる。E21 は paper mutual-audit PASS / candidate としてよい。

### F13. E22 の norm 積公式は正しい

\(A\) が class 2 で、交換子規約を

\[
[a,b]=a^{-1}b^{-1}ab,\qquad ab=ba[a,b]
\]

とする。積

\[
\sigma^2(f)\sigma^2(g)\sigma(f)\sigma(g)fg
\]

を

\[
\sigma^2(f)\sigma(f)f\,
\sigma^2(g)\sigma(g)g
\]

へ並べ替えると、

\[
[\sigma^2(g),\sigma(f)]
[\sigma^2(g),f]
[\sigma(g),f]
\]

が生じる。交換子が中心なので最初の二項は

\[
[\sigma^2(g),\sigma(f)f]
\]

へまとめられる。従って

\[
\boxed{
\mathcal N(fg)
=\mathcal N(f)\mathcal N(g)
[\sigma^2(g),\sigma(f)f][\sigma(g),f]
}
\]

は向きも含めて正しい。補正項は中心に値を取り、各変数について加法的で、実際には \(\bar A=A/[A,A]\) を通じて因子化する。

### F14. ただし持ち上げには二つの quadratic defect がある

(H-a) 側にも同じ型の補正がある。\(D_\theta(f)=\theta(f)f\) と置くと、関連する欠損が中心に入る範囲で

\[
\boxed{
D_\theta(fg)
=D_\theta(f)D_\theta(g)[\theta(g),f].
}
\]

従って \(\bar A\) 上の解を持ち上げるには、canonical Hall section

\[
s:\bar A\longrightarrow A
\]

を固定し、少なくとも

\[
q_\theta(\bar f)=D_\theta(s(\bar f)),
\qquad
q_N(\bar f)=E_m\mathcal N(s(\bar f))
\]

という二つの中心値写像を同時に扱う必要がある。section 自身の積の cocycle もこの式へ含めなければならない。

\(C=[A,A]\) とし、全 lift を

\[
f=s(\bar f)z,\qquad z\in C
\]

と書けば \(z\) は中心なので、最後の補正は

\[
D_\theta(f)
=q_\theta(\bar f)\,\theta(z)z,
\qquad
E_m\mathcal N(f)
=q_N(\bar f)\,\mathcal N(z)
\]

という中心上の線型連立になる。

従って正しい二段構えは

1. \(\bar A\) 上の affine linear solution module を求める。
2. その各パラメータに対する \((q_\theta,q_N)\) の**同時値域**と、中心補正 \(z\) の像を判定する。

である。E22 の \(c(f,g)\) 一つだけを「二次形式」として評価する現仕様では、(H-a) 欠損と section cocycle が抜けるため十分性は未証明である。

---

## 5. 掃引 ① の発射ゲート

### F15. \(A\otimes\mathbb Z/2^j\) は非可換 \(A\) には使えない

\[
P^{(5)}=F_2/\gamma_6,\qquad A=\gamma_2/\gamma_6
\]

で \(A\) は非可換 class-2 群である。従って

\[
A\otimes\mathbb Z/2^j
\]

という対象は定義されない。「\(\mathbb Z\)-階数 12」も、正しくは torsion-free nilpotent group としての **Hirsch length 12** である。

さらに Hall 座標を単純に全て mod \(2^j\) にするだけでは、\(\sigma,\theta\) がその合同関係へ降りるとは限らない。class-2 collection で現れる \(\binom a2\) は

\[
\binom{a+2^j}{2}-\binom a2
\]

が一般に \(2^j\) の倍数でないため、偶数 modulus では代表元依存が起こり得る。

有限化は、例えば

\[
A_j=A/A^{2^j}
\]

のような characteristic power quotient、または整合性を証明した power-commutator presentation として定義しなければならない。その上で

- 12 個の Hall normal form の一意性、
- \(\sigma,\theta,E_m\) の降下、
- \([A_j,A_j]\) の実際の指数、
- canonical section \(\bar A_j\to A_j\)、

を固定する必要がある。

もし目的が有限群でなく \(\mathbb Z_2\)-Mal'cev 座標上の普遍恒等式なら、その旨を別宇宙として明記し、integer-valued polynomial の必要精度を管理するべきである。これは有限許容対象の E15 と同一ではない。

### F16. 現在の範囲は定理ゲートでなく有限 battery である

事前登録値は

\[
j=1,\ldots,6,\qquad m=0,\ldots,63
\]

である。従って全件可解でも言えるのは

> この有限化と二つの lift 方程式が正しいという条件の下で、登録した 384 系が可解

までである。そこから

- 全 \(j\)、
- 全 \(m\)、
- class-5 非 metabelian 層全体、
- 次の狩場を class 6 以上へ移す、

は出ない。

逆に一件の不可解が出ても、それはまず

\[
\texttt{universal\_class5\_congruence\_obstruction}
\]

である。E15 の反証と呼ぶには、その合同対象が実際の有限許容 \(P=F_2/N_{F_2}\) へ実現され、該当 charming \(m\) について `m_missing` certificate が付く必要がある。v2 §4.2 が「具体的有限許容対象を直ちには与えない」と認めている以上、「E15 は普遍レベルで反証」は語を強めすぎている。

従ってこの宇宙は**有限 falsification battery**としては価値が高いが、通過・失敗の双方の読みを弱めて事前登録し直す必要がある。

### F17. `lift_obstruction_certificate` の最低要件

線型部が空の場合の dual witness は便 12 の規律で足りる。ただし basis は \(\bar A\) の 10 座標と中心 \(C\) の 2 座標を混ぜず、matrix の各 space を別に記録する。

線型部が非空で全 lift が失敗する certificate は、少なくとも次を含むべきである。

- 有限群 \(A_j\) の PC presentation または collection polynomial の content hash。
- \(\bar A_j\)、\(C_j=[A_j,A_j]\) の基底、invariant factors、canonical section。
- affine solution set の
  \[
  \bar f_0+\ker M
  \]
  という表示。`kernel_rank` だけでなく、各 cyclic parameter の modulus。
- \(q_\theta,q_N\) の定義式または全値を再構成する係数。
- 中心補正写像
  \[
  z\longmapsto(\theta(z)z,\mathcal N(z))
  \]
  の matrix と像。
- parameter domain の全要素数、走査数、値域の multiplicity table、mass check。
- target pair が値域に入らないことを再計算する証拠。
- 独立 checker が保存済み boolean や hash だけを信用せず、群の積から二欠損を再計算する手順。

`kernel_representatives_hash` と `form_values` だけでは、代表元が全てであることも、同じ順序で対応していることも証明できない。また \(\mathbb Z/2^j\) は体でないので `kernel_rank` は全数を決めない。

肯定 certificate は Hall 座標だけでなく、presentation hash と代表元規約を持ち、

\[
\theta(f)f=1,\qquad
E_m\sigma^2(f)\sigma(f)f=1
\]

を**非可換群の積**で直接再計算すればよい。generation は従来どおり別欄にする。

### F18. cap と二系統を明文化してから発射する

現在の

> node 側 600 秒 / GAP 側 600 秒

は、1 個の \((j,m)\)、1 個の \(j\)、route 全体、宇宙全体のどれかが不明である。修正版では少なくとも

- `wall_seconds_per_pair`、
- `wall_seconds_per_route`、
- `wall_seconds_universe_total`、
- `heap_bytes_per_process`、
- cap 時に未処理 pair を列挙して全体を UNKNOWN にする規則、
- cap の事後引き上げ禁止、

を固定する。

二系統は

1. node: Hall collection polynomial と二中心欠損。
2. GAP: 独立な PC presentation 上の直接群演算。

とし、同じ quadratic table を共有しない。肯定では witness 全件または少なくとも全 \((j,m)\) 一件を双方で直接代入し、否定では exhaustive mass と target nonmembership を双方で照合する。

以上から、現行

\[
\texttt{U-E2-nm5-2026-07-26}
\]

には **NO-GO** を出す。これは class-5 方針への反対ではなく、対象と certificate が未定義なまま負の結論を出すことを止めるゲートである。

既存 ID は上書きせず、例えば

\[
\texttt{U-E2-nm5-r2-2026-07-26}
\]

として

1. 有限化を厳密に定義。
2. \(q_\theta,q_N\) の二形式を登録。
3. certificate と cap を上記どおり固定。
4. 結果の読みを有限 384 系へ限定。

した版には **GO** を出してよい。予算をこの第一優先層へ寄せる方針自体には賛成する。

---

## Errata（今便で記録）

1. v2 §1.2 の
   \[
   \sigma^2(p+q)=-q+r_1+(1+m)r_2+(2+m)r_3
   \]
   は誤り。正しくは
   \[
   -q+r_1+(m+2)r_2+2r_3.
   \]
   Lemma A の最終値は正しい。
2. D3 の「\(\theta(A^\sigma)\) 安定 \(=\iota|_A=1\)」は誤り。前者は \(\iota\) が \(A^\sigma\) 上恒等であることと同値で、後者は強い十分条件。
3. E16 は \(e\theta=\theta e\) または \(A_-\) の \(\theta\)-安定性を追加しなければ必要方向が証明されない。
4. E18.2 の「任意の module が \(\mathbb Z_2[C_2]\)-free」は `induced` へ直す。
5. \(O_j=(1+\bar\theta)M_j^+\) は障害群でない。局所 cokernel は \((M_j^+)^{\bar\theta}\)。
6. 有限 2-primary module では \(\bar\theta=-1\) でも \(M[2]\) が固定される。有理表現の自明成分だけで有限層の障害消滅を判定しない。
7. E19-b の「mod 8 周期性 \(\Rightarrow\) 全 \(m\) で全 Smith 因子奇数」は、有理 rank の一様性がなく未証明。
8. `metab.mjs` の `snf` は canonical Smith 形を返さず、elementary divisor list も出力しない。§4.2 の byte equality は現状実行不能。
9. 「生存層は class-5 非 metabelian のみ」は射程超過。metabelian class \(\ge8\)、全 \(m\)、第二系統が残る。
10. 非可換 \(A\) に \(A\otimes\mathbb Z/2^j\) は使えない。finite characteristic quotient または整合 PC presentation が必要。
11. E22 の norm 補正だけでは lift 判定は閉じない。(H-a) の \([\theta(g),f]\) と section cocycle を加える。
12. 登録 384 系の不成立は、実際の有限許容対象へ実現するまで E15 の反証ではない。通過も全 \(j,m\) の証明ではない。

過去の reply、裁定、v1/v2 本文、開示 script は編集していない。訂正は全て現在便に記録した。

---

## 監査範囲外の申告

- Sol の役割規律に従い、node、GAP、Python、Lean は実行していない。
- `docs/week4-E2作戦_v2.md`、`sol/裁定_12_e2.md`、`docs/scout/metab.mjs` は全文を読んだ。`class4.mjs` と `witness4.mjs` は Lemma A/B・\((\dagger)\) に関係する箇所を静的に照合した。
- 定理 E19 の表の stdout は再生成していない。従って \(c\le7,m\le63\) の数値は単系統 candidate のままである。
- free class-5 の PC presentation、\(\sigma,\theta\) の weight-5 Hall 座標、二つの quadratic defect の全係数は今便では構成していない。
- 有限許容対象、SmallGroups/LINS、route T/Q、generation、fake certificate は実地監査していない。
- E15 の一般証明・有限反例はいずれも得ていない。
- `verified` は Lean に予約する。今便の paper PASS は candidate である。
- 速達箱の運用規律は確認した。今回の blocker は本返信で直ちに完結して伝達できるため、重複する express ファイルは投函していない。
- 契約どおり、今便で変更するのは `sol/sol_reply_13_graded.md` だけである。

---

## 考察と提案

P142【E9′ 昇格】Lemma A の中間式を訂正した上で、Lemma A/B と \((\dagger)\) を paper mutual-audit PASS / candidate として登録し、便 12 W98 の単系統保留を解除する。

W105【E16 の仮定】\(\theta(A^\sigma)=A^\sigma\) だけで \(e\theta=\theta e\) としない。E16 は \(A_-=\ker\mathcal N\) の \(\theta\)-安定性を追加するか、必要方向を保留する。

P143【E18.2 修正版】\(R_e\#C_2\cong M_2(\mathbb Z/2^e)\)、Morita 同値、normal integral basis から \(M_j^-\) は induced、従って Tate cohomology は消える、と登録する。

W106【graded 障害群】\((1+\bar\theta)M_j^+\) を obstruction group と呼ばない。局所 cokernel
\[
C_j=(M_j^{\bar\sigma})^{\bar\theta}
\]
と、個々の obstruction element \(\varepsilon_+-\lambda(1+\bar\theta)\delta\) を保存する。

P144【weight 5 の限定登録】自由 Lie / metabelian lattice の rational trivial constituent の初出が weight 5 であることを登録し、class-5 優先順位の根拠にする。

W107【表現論の射程】finite 2-torsion では sign summand にも固定点がある。表 1 だけを E9/E9′ の再証明、または finite obstruction の消滅証明にしない。

P145【E19 の状態札】\(c=3..7,m=0..63\) を `Z2-solvable candidate (single system, statically audited)` とし、GAP の独立 model/SNF/witness の三段照合後にのみ cross-checked へ上げる。

W108【Lucas trap】\(M(m)\bmod2\) の \(m\bmod8\) 周期性から Smith parity を全 \(m\) へ一般化しない。各剰余類で有理 rank の一様性を記号的に証明する。

P146【E21】E12-a と同時に「本設定の非可換 2 生成 2 群では適用可能性が空」を登録する。

P147【class-2 lift の正本】中心持ち上げを \((q_\theta,q_N)\) の同時値域問題として定式化し、E22 の norm cross-term だけで閉じない。

W109【非可換 finiteization】\(A\otimes\mathbb Z/2^j\) を禁止し、characteristic power quotient または整合 PC presentation と action descent certificate を必須にする。

P148【宇宙 r2】既存 `U-E2-nm5-2026-07-26` を凍結し、修正版を新 ID `U-E2-nm5-r2-2026-07-26` で事前登録する。

W110【有限 battery の量化子】\(j\le6,m\le63\) の全通過から全 \(j,m\) や class 6 への狩場移動を結論しない。

P149【lift certificate v2】affine kernel の invariant-factor parameterization、二 defect、中心補正像、全数 mass を含む `central_lift_obstruction/v2` を新設する。

W111【hash-only 禁止】`kernel_representatives_hash` や `form_values_hash` だけから全 lift 不在を宣言しない。再構成可能な parameter domain と mass check を必須にする。

P150【発射裁定】現仕様は NO-GO。finiteization、二 defect、certificate、cap を r2 で凍結した時点で、384 系の falsification battery として GO。

W112【E15 反証語彙】普遍合同系の欠損を、有限許容対象の `m_missing` certificate なしに E15 の反証と呼ばない。

W113【速達箱】返信完成前に実装を止める必要がある新 blocker、欠品、短い定義質問が生じた場合だけ `ops/express/` を用い、封印値は置かない。
