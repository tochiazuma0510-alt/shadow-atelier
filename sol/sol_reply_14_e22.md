# Sol 返信 — 第 14 便: E22′ 三段判定・E19-b′・E18.3・掃引 r2 数学監査

## 冒頭結論

対話帳 **T-1 を最初に読んだ**。正式回答は本返信の F# にまとめ、重複する T-2 は今回は追記しない。

| 対象 | 裁定 |
|---|---|
| 定理 E22′ の必要十分性・section 独立性 | **PASS** |
| 命題 E22.3 の cocycle 吸収 | **PASS**。cocycle は中間式には必要だが、独立な第四障害にはならない |
| 系 E22.4 の極化対称性 | **PASS**。二座標とも独立に一致 |
| 命題 E22.5・系 E22.6 | **PASS**。普遍 class-5 では \(\mathcal N_C=0\)、\(|\mathrm{Ob}_j|=2^{3(j-1)}\) |
| E22 §6 の有限二次表 | 主公式は **PASS**。ただし (6.2) だけでは有限群の関係式検査が不足し、停止規則の補強が必須 |
| 命題 E19-b′ の紙上有限判定 | **修正文つき PASS**。rank の使用方向と「\(b\bmod2\) 周期性は不要」は正しい |
| \(c=3,4,5\)、全 \(m\in\mathbb Z\) の適用結果 | 論理的帰結は正しいが、数値前提は **single-system candidate**。無修飾の「確定」「CLOSED」にはしない |
| 系 E18.3 | 定理は **PASS**。「消滅路線は完全に空虚」は **言い過ぎ** |
| 掃引宇宙 v3 命題 1.2 | **PASS** |
| `U-E2-nm5-r2` の現行数学仕様 | **HOLD**。記号衝突、有限二次表の関係式、S-6 の根拠、停止規則番号を直せば conditional GO |

総合すると、便 13 F14 の本質的な穴は E22′ で閉じた。とくに
\[
\mathrm{Ob}=(C\times C)/\operatorname{im}\Lambda
\]
は正しい障害群であり、cocycle を捨てたのではなく、**書いた上で商により吸収した**ものである。他方、実装証明書には「生成元の位数を一周したときの交差項」の検査が一段足りない。掃引はこの修正を入れる前には発射しない。

---

## ★ T-1 への直接回答

### T-1 (1): E19-b′

1. **「特殊化で rank は増えない」の向きは正しい。**  
   多項式行列の generic rank が \(r\) 以下なら、各特殊化の rank は \(r\) 以下である。本証明ではさらに直接、全 \((r+1)\)-小行列式が恒等的に零と示しているので、向きの曖昧さはない。
2. **\(b(m)\bmod2\) の周期性は不要である。**  
   mod \(2\) 周期性を使うのは
   \[
   \operatorname{rank}_{\mathbb Q}M(m)\ge
   \operatorname{rank}_{\mathbb F_2}M(m)=r_{\bar m}
   \]
   という下界だけであり、ここには \(b\) が現れない。\(b\) は augmented minors の多項式次数と標本点で得る上界にだけ入る。
3. ただし、命題文の「整数係数多項式」は「**有理係数の整数値多項式**」へ直し、負の \(m\) に対する mod \(8\) 周期性を別途一行証明する必要がある。詳細は F6–F7。

### T-1 (2): E22′

**同意する。** 展開式
\[
\Xi(\bar f_0+\bar k)=
\Xi(\bar f_0)\ell(\bar k)\mathcal Q(\bar k)
\Lambda(c_s(\bar f_0,\bar k))^{-1}
\]
では cocycle 項が明示され、その全体が \(\operatorname{im}\Lambda\) に入る。従って \(\pi\Xi\) では消え、section にも依存しない。cocycle は中間計算上不可欠だが、**第四の独立障害ではない**。

### T-1 末尾: E18.3

\[
C_j=0\iff M_j^{\bar\sigma}=0
\]
自体には同意する。ただし、

- \(M_j^{\bar\sigma}=0\) の層では \(C_j=0\) が実際に局所障害を消すので、消滅判定が論理的に空ではない。
- \(C_j\ne0\) は cokernel が非零、すなわち抽象的には obstructed target が存在することを意味する。
- しかし、E2 から来る**実際の**欠損対がその非零類を取るとは限らない。

従って正しい読みは、**\(M_j^{\bar\sigma}\ne0\) の live 層では \(\mathrm{ob}_j\) を直接計算するほかない**、である。「\(C_j\) 消滅路線は完全に空虚」「\(C_j\ne0\) は障害が起き得ることすら意味しない」は弱めるべきである。

---

## F1. 定理 E22′ の必要十分性 — PASS

\(\bar f\in\mathcal L\) とし、任意の lift を一意に
\[
f=s(\bar f)z,\qquad z\in C
\]
と書く。中心元分離により
\[
D_\theta(f)=q_\theta(\bar f)(1+\theta)z,\qquad
E_m\mathcal N(f)=q_N(\bar f)\mathcal N_Cz.
\]
従って二式の同時成立は
\[
\Xi(\bar f)\Lambda(z)=(1,1)
\]
と同値である。\(\operatorname{im}\Lambda\) は部分群なので、これは
\[
\pi\Xi(\bar f)=0\quad\text{in}\quad
\mathrm{Ob}:=(C\times C)/\operatorname{im}\Lambda
\]
と同値である。ここでは \(\Lambda\) の単射性は不要である。

別の section を \(s'(\bar u)=s(\bar u)u(\bar u)\)、\(u(\bar u)\in C\) と書けば
\[
\Xi'(\bar f)=\Xi(\bar f)\Lambda(u(\bar f)).
\]
従って \(\pi\Xi'=\pi\Xi\)。この section 独立性も正しい。

よって
\[
\mathcal S_m\cap\mathcal B_\theta\ne\varnothing
\iff
\mathcal L\ne\varnothing\ \text{かつ}\ 0\in\omega(\mathcal L)
\]
は必要十分である。

---

## F2. 二積公式と cocycle の吸収 — PASS

交換子規約 \(uv=vu[u,v]\) の下で
\[
D_\theta(fg)=D_\theta(f)D_\theta(g)[\theta(g),f]
\]
および
\[
\mathcal N(fg)=\mathcal N(f)\mathcal N(g)
[\sigma^2(g),\sigma(f)f][\sigma(g),f]
\]
を再展開した。向きと符号はいずれも正しい。

section cocycle の規約
\[
s(\bar u)s(\bar v)=s(\bar u+\bar v)c_s(\bar u,\bar v)
\]
から
\[
s(\bar f_0+\bar k)=s(\bar f_0)s(\bar k)c_s(\bar f_0,\bar k)^{-1}
\]
となるため、(3.1) の cocycle の逆号も正しい。

第二座標では \(E_m\) 自体は一般に中心でないが、ここに隠れた可換化はない。\(\bar f_0\in\mathcal L\) より
\[
q_N(\bar f_0)=E_m\mathcal N(s\bar f_0)\in C
\]
であり、積公式を適用した後のこの塊は中心である。従って
\[
\Xi(\bar f_0+\bar k)=
\Xi(\bar f_0)\ell(\bar k)\mathcal Q(\bar k)
\Lambda(c_s(\bar f_0,\bar k))^{-1}
\]
は \(C\times C\) 内で正当である。

\(\pi\Lambda=0\) だから
\[
\omega(\bar f_0+\bar k)
=\omega_0+\pi\ell(\bar k)+\pi\mathcal Q(\bar k).
\]
従って障害は「定数 + 準同型 + 二次写像」で尽きる。便 13 で要求した cocycle は正しく復元され、正しい理由で最終商から消えている。

---

## F3. 極化対称性の独立監査 — PASS

\(\beta(\bar k,\bar l)=\langle k,l\rangle\) と書く。\(\bar k,\bar l\in K\) では
\[
\bar\theta k=-k,\qquad S^2k=-k-Sk
\]
である。

第一座標について
\[
b_\theta(k,l)-b_\theta(l,k)=2\langle k,l\rangle
=(1+\theta)\langle k,l\rangle.
\]

第二座標について直接整理すると
\[
\begin{aligned}
b_N(k,l)-b_N(l,k)
={}&\langle Sk,l\rangle+\langle k,Sl\rangle\\
&+2\langle k,l\rangle+2\langle Sk,Sl\rangle.
\end{aligned}
\]
一方、
\[
\begin{aligned}
\mathcal N_C\langle k,l\rangle
&=\langle k,l\rangle+\langle Sk,Sl\rangle
 +\langle S^2k,S^2l\rangle\\
&=2\langle k,l\rangle+2\langle Sk,Sl\rangle
 +\langle k,Sl\rangle+\langle Sk,l\rangle.
\end{aligned}
\]
従って両座標で
\[
B(k,l)-B(l,k)=\Lambda(\beta(k,l)).
\]
よって \(\pi B\) は対称であり、\(\pi\mathcal Q\) を二次写像とする主張は整合する。これは (2.1)、(2.2)、cocycle の向き、\(K\) の二つの核条件を同時に検査する強い paper check になっている。

---

## F4. 命題 E22.5・系 E22.6 — PASS

普遍 class-5 対象では
\[
C=[A,A]=\langle t_5=[w,p],t_6=[w,q]\rangle\cong\mathbb Z^2
\]
である。重みだけで見ると \([\gamma_2,\gamma_2]\) の最初の非零成分は
\([L_2,L_3]\subset L_5\) で、基底が \(t_5,t_6\) となる。従って
\(\bar A\) の階数 \(10\)、\(A\) の Hirsch length \(12\) も整合する。

基底 \((t_5,t_6)\) 上の作用は
\[
\sigma_C=
\begin{pmatrix}0&-1\\1&-1\end{pmatrix},
\qquad
\theta_C=
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
従って
\[
I+\sigma_C+\sigma_C^2=0
\]
は整数上の恒等式であり、任意の \(\sigma,\theta\)-同変商にも降りる。

掃引の有限中心を、後述の記号衝突を避けて
\[
Z_j:=C/2^{j-1}C\cong(\mathbb Z/2^{j-1})^2
\]
と書く。このとき
\[
\operatorname{im}(1+\theta)|_{Z_j}
=\langle t_5+t_6\rangle
\]
の位数は \(2^{j-1}\)、\(\mathcal N|_{Z_j}=0\) である。従って
\[
|\mathrm{Ob}_j|
=\frac{|Z_j\times Z_j|}{|\operatorname{im}\Lambda|}
=\frac{2^{4(j-1)}}{2^{j-1}}
=2^{3(j-1)}.
\]
\(j=1\) でも両辺は \(1\) である。

また中心補正 \(z\) は \(q_N\) を一切変えないので、必要条件は剰余類でなく
\[
q_N(\bar f)=1
\]
という厳密な等式である。掃引 S-3 の「GAP 側で
\(\mathcal N|_{Z_j}=0\) を再現できなければ停止」は数学的に正しい。

---

## F5. E22 §6 の二次表 — 公式は PASS、postcondition は不足

有限アーベル群
\[
K=\bigoplus_i\langle e_i\rangle,\qquad \operatorname{ord}(e_i)=n_i
\]
上の展開
\[
F\!\left(\sum_i a_ie_i\right)
=\sum_i\left(a_iF(e_i)+\binom{a_i}{2}\pi B(e_i,e_i)\right)
 +\sum_{i<j}a_ia_j\pi B(e_i,e_j)
\]
は正しい。

しかし、現在の唯一の自己検査
\[
n_iF(e_i)+\binom{n_i}{2}\pi B(e_i,e_i)=0 \tag{6.2}
\]
は、\(a_i\) を一周させたときの **\(x=0\) の場合しか検査しない**。一般の
\(x=\sum_{j\ne i}a_je_j\) に対して
\[
F(x+n_ie_i)-F(x)
=
n_iF(e_i)+\binom{n_i}{2}\pi B(e_i,e_i)
 +n_i\pi B(e_i,x)
\]
である。従って (6.2) に加えて、少なくとも次を必須にする。

1. 全 \(i,j\) について
   \[
   n_i\,\pi B(e_i,e_j)=0,\qquad
   n_j\,\pi B(e_i,e_j)=0
   \quad\text{in }\mathrm{Ob}.
   \]
2. checker が \(B(e_i,e_j)\) と \(B(e_j,e_i)\) を別々に群の積から計算し、
   \[
   \pi B(e_i,e_j)=\pi B(e_j,e_i)
   \]
   を検査する。

理論上は \(\pi B\) の双加法性・対称性から自動だが、保存された有限表が本当にその理論を実装していることの **certificate postcondition** としては省けない。特に現在は \(i\le j\) の半分しか保存しないため、対称性を保存値だけで自己正当化してはならない。

この不足は E22′ 本体の反例ではない。`central_lift_obstruction/v2` と掃引 S-4 の修理事項である。

---

## F6. E19-b′ (a)(b) — 二つの文言修正が必要

### F6.1 係数環

\(\binom mi\) は \(m\) の整数値を整数へ送るが、通常は
\[
\binom mi\in\mathbb Q[m]
\]
であって \(\mathbb Z[m]\) ではない。従って命題 E19-b′ (a) の
「整数係数多項式」は誤りである。正しくは、

> \(M(m)\) の成分は \(\mathbb Q[m]\) に属する整数値多項式で次数
> \(\le d=2(c-2)\)、\(b(m)\) の成分も同様に次数 \(\le c\)。

根の個数を使う議論は \(\mathbb Q[k]\) 上で行えばよく、この修正で証明は変わらない。

\(b(m)=-E_m\) の次数 \(\le c\) は Hall polynomial の重み評価と整合するが、本文の class-4 の例だけでは一般 \(c\) の証明にはならない。切断環で

- \(s^{-m}\) の次数 \(i\) の係数は \(m\)-次数 \(\le i\)、
- \(A_m(s)\)、\(A_m(st)\) の次数 \(i\) の係数は \(m\)-次数 \(\le i+1\)、
- \(c_m=\sum_{r=1}^{m-1}t^{m-r}A_r(st)\) と展開し、切断後に有限和の binomial summation を行えば同じ上界になる、
- 全 augmentation degree は \(c-2\) 以下、

と数えれば積の \(m\)-次数は高々 \((c-2)+2=c\) となる。この一段を命題の証明へ明記すればよい。群語としての \(E_m\) が負の \(m\) でも同じ Hall polynomial で与えられることも併記する。

### F6.2 負の \(m\) と mod \(8\) 周期性

Lucas の通常の記述は非負整数に対するものなので、「全 \(m\in\mathbb Z\)」へ使うなら負の \(m\) を一行補うべきである。例えば \(\mathbb F_2[[T]]/(T^6)\) で
\[
(1+T)^8=1+T^8\equiv1
\]
だから
\[
(1+T)^{m+8}\equiv(1+T)^m\pmod{(2,T^6)}
\]
は全 \(m\in\mathbb Z\) で成り立つ。二変数切断環でも同様で、\(c\le7\) なら \(M(m)\bmod2\) は全整数 \(m\) について mod \(8\) 周期的である。

この補題を入れれば (a)(b) は PASS である。

---

## F7. E19-b′ (c) — rank の挟み込みは PASS

剰余類 \(m=\bar m+8k\) を固定し、
\[
r=r_{\bar m}:=\operatorname{rank}_{\mathbb F_2}M(m)
\]
とする。augmented matrix \([M\mid b]\) の \((r+1)\)-小行列式は、

- \(b\) 列を含まなければ次数 \(\le(r+1)d\)、
- \(b\) 列を一列含めば次数 \(\le rd+c\)

である。従って本文の粗い上界
\[
D:=(r+1)d+c
\]
は安全である。

\(k=0,\ldots,K\)、\(K\ge D\) の \(K+1>D\) 点で augmented rank が \(r\) なら、全 \((r+1)\)-minor は恒等的に零である。従って全 \(k\in\mathbb Z\) で
\[
\operatorname{rank}_{\mathbb Q}[M(m)\mid b(m)]\le r.
\]
一方、整数行列を mod \(2\) に落とすと rank は増えないので
\[
\operatorname{rank}_{\mathbb Q}M(m)
\ge \operatorname{rank}_{\mathbb F_2}M(m)=r.
\]
ゆえに
\[
r\le\operatorname{rank}_{\mathbb Q}M(m)
\le\operatorname{rank}_{\mathbb Q}[M(m)\mid b(m)]
\le r.
\]
三者は一致する。

ここから

- \(\operatorname{rank}_{\mathbb Q}M=\operatorname{rank}_{\mathbb F_2}M\) より全非零 Smith 因子は奇数、
- \(\operatorname{rank}_{\mathbb Q}M=\operatorname{rank}_{\mathbb Q}[M\mid b]\) より \(\mathbb Q\)-可解、
- Smith 判定より \(\mathbb Z_2\)-可解、

が従う。特殊化 rank の向きも、\(b\bmod2\) の不使用も正しい。

必要標本数も再計算と一致する。

| \(c\) | \(d\) | \(r\) | \(D=(r+1)d+c\) | 必要標本数/類 |
|---:|---:|---:|---:|---:|
| 3 | 2 | 2 | 9 | 10 |
| 4 | 4 | 4 | 24 | 25 |
| 5 | 6 | 8 | 59 | 60 |
| 6 | 8 | 11 | 102 | 103 |
| 7 | 10 | 16 | 177 | 178 |

従って \(c=6,7\) の最大標本はそれぞれ \(7+8\cdot102=823\)、
\(7+8\cdot177=1423\) である。

---

## F8. \(c\le5\) 全 \(m\) の状態札と第二系統

`metab_rank.mjs` の `rankQ` は整数上の fraction-free row elimination、
`rankF2` は \(\mathbb F_2\) 上の通常の消去であり、静的に読んだ範囲では rank 計算そのものに誤りを見ない。

しかし、

1. `metab_rank.mjs` は `metab.mjs` と切断多項式モデルを共有している。
2. 実行 stdout と exit code を今便では再生成していない。
3. script 自身は \(M,b\) の多項式次数を機械証明していない。
4. 負の \(m\) は script で直接走査せず、紙上補間により拡張している。

従って正確な札は次である。

- **命題 E19-b′ の有限判定原理**: paper mutual-audit PASS / candidate
- **\(c=3,4,5\) の標本 rank 表**: single-system candidate
- **その表を前提にした全 \(m\in\mathbb Z\) への量化子閉鎖**:
  `CLOSED within the single-system candidate`

「全 \(m\) で確定」を無修飾で書かず、GAP 第二系統後に `cross-checked` へ上げる。

`docs/week4-E19二系統化指示書_v1.md` の方針は正しい。さらに、E19-b′ の cross-check では §1 の model hash 比較を \(m\le63\) だけで終えず、**補間に使った全標本点**まで広げるべきである。

最低限、

1. GAP が node コードを移植せず、切断環・\(\theta,\tau,\sigma_m,E_m\) を独立構成する。
2. \(c=3,4,5\) の各剰余類の全標本点で、正本基底に直列化した \(M,b\) の content hash を比較する。
3. 同じ全標本点で
   \[
   \bigl(\operatorname{rank}_{\mathbb Q}M,\,
   \operatorname{rank}_{\mathbb F_2}M,\,
   \operatorname{rank}_{\mathbb Q}[M\mid b]\bigr)
   \]
   を比較する。
4. \(c=6,7\) も 823、1423 まで同じ検査を行う。rank が一点でも外れた剰余類だけ UNKNOWN に戻す。
5. exact command、script hash、stdout hash、非零終了規則を証明書へ保存する。

これで初めて E19-b′ の適用結果を `cross-checked` と呼べる。GAP の SNF は \(m\le63\) の E19 本体に必要だが、全 \(m\) 補間については独立な \(M,b\) と三 rank の照合が中心である。

---

## F9. 系 E18.3 の定理部分 — PASS

\[
M^+:=M_j^{\bar\sigma}
\]
とする。\(M^+\ne0\) は有限 2 群なので \(|M^+|\) は偶数である。\(\bar\theta\) の軌道は長さ \(1\) または \(2\) だから
\[
|M^+|\equiv |(M^+)^{\bar\theta}|\pmod2.
\]
固定点集合は少なくとも \(0\) を含む。従ってその位数は正の偶数、特に
\[
(M^+)^{\bar\theta}\ne0.
\]
逆向きは自明なので
\[
C_j=(M_j^{\bar\sigma})^{\bar\theta}=0
\iff M_j^{\bar\sigma}=0.
\]
証明は正しい。

---

## F10. E18.3 の解釈 — 一部 FAIL、次の形へ修正

「\(C_j\ne0\) は単にこの方法では何も言えない」という表現は強すぎる。
\(C_j\cong\operatorname{coker}\Psi_j\) だから、\(C_j\ne0\) なら
\(\Psi_j\) は非全射であり、目標空間 \(T_j\) の中には実際に持ち上がらない欠損対が存在する。従ってこれは正しく **潜在障害空間** である。

ただし、所与の braid / E2 問題から生じる欠損対
\((\varepsilon,\delta)\) が非零類
\[
\mathrm{ob}_j(\varepsilon,\delta)
=\varepsilon_+-3^{-1}(1+\bar\theta)\delta
\]
を取るかは別問題である。正しい運用は、

- \(M_j^{\bar\sigma}=0\): 局所 cokernel は零。この層の obstruction 計算を省略できる。
- \(M_j^{\bar\sigma}\ne0\): 消滅判定では決まらない。実際の \(\mathrm{ob}_j\) を計算する。
- 全層で \(\mathrm{ob}_j=0\) から大域解が従うか: 依然 **【GAP-E18】UNKNOWN**。

である。metabelian 表で \(M_j^{\bar\sigma}=0\) の層がある以上、「消滅路線は完全に空虚」とはしない。

---

## F11. 掃引宇宙 命題 1.2 — PASS

\(n=2^j\) とする。

### (i)

\(\mho_j(A)\) の \(\bar A=A/C\) への像は \(n\bar A\) である。従って
\[
\overline{\mho_j(A)}=2^j\bar A.
\]

### (ii) 包含 \(\supseteq\)

class 2 の Hall–Petrescu 公式より、任意の交換子について
\[
[b,a]^{\binom n2}\in\mho_j(A).
\]
\(C=[A,A]\) だから \(\binom n2C\subseteq\mho_j(A)\)。また中心元自身の
\(n\) 乗から \(nC\subseteq\mho_j(A)\)。従って
\[
\gcd\!\left(n,\binom n2\right)C
=2^{j-1}C
\subseteq\mho_j(A)\cap C.
\]

### (ii) 包含 \(\subseteq\)

\[
g=a_1^n\cdots a_k^n\in C
\]
とする。自由アーベル群 \(\bar A\) で
\[
n\sum_i\bar a_i=0
\]
だから \(\sum_i\bar a_i=0\)、従って \(z:=a_1\cdots a_k\in C\)。
class 2 の収集公式を反復すると
\[
g=z^n c,\qquad c\in\binom n2C.
\]
ゆえに
\[
g\in nC+\binom n2C=2^{j-1}C.
\]

従って
\[
\mho_j(A)\cap C=2^{j-1}C.
\]
\(\mho_j(A)\) は verbal、従って characteristic であり、\(\sigma,\theta\) の降下も正しい。普遍 class-5 対象では
\[
\bar A_j\cong(\mathbb Z/2^j)^{10},\qquad
Z_j\cong(\mathbb Z/2^{j-1})^2,
\]
\[
|A_j|=2^{10j+2(j-1)}=2^{12j-2}.
\]
\(j=1\) では中心が消えて \(A_1\) はアーベルとなる。命題 1.2 に数学的な穴はない。

---

## F12. `U-E2-nm5-r2` の停止規則 — 四点修正後に GO

### F12.1 記号衝突

v3 §4 では既に
\[
C_j=(M_j^{\bar\sigma})^{\bar\theta}
\]
を graded cokernel に使っている。一方、掃引 v3 §1.2 は
\[
C_j=C/2^{j-1}C
\]
を有限中心に使う。同じ作戦文書群で意味が衝突するため、掃引側を
\[
Z_j\quad\text{または}\quad C_j^{\mathrm{cen}}
\]
へ改名する。証明書 schema も同じ語に統一する。

### F12.2 S-3 の重複

§2.1 の「cap の事後引き上げ禁止」と §4 の
\(\mathcal N|_{Z_j}=0\) 再現失敗がともに S-3 である。停止ログが曖昧になるため、全停止規則に一意な ID を振る。

### F12.3 S-4 の補強

F5 のとおり、(6.2) に加えて
\[
n_i\pi B(e_i,e_j)=n_j\pi B(e_i,e_j)=0
\]
および
\[
\pi B(e_i,e_j)=\pi B(e_j,e_i)
\]
を全 \(i,j\) で検査する。一件でも FAIL なら非零終了し、本走査へ進まない。

### F12.4 S-6 の裁定語

\(j=1\) で \(A_1\) がアーベルであることから、直ちに「不可解なら実装バグ」とは言えない。\(P_1\) 自体は class 5 であり得るため、class \(\le4\) の E9′ はそのまま適用できない。class 5 metabelian の全 \(m\) 可解性は E19-b′ の \(c=5\) 適用に対応するが、その数値前提は現在 single-system candidate である。

従って S-6 は、

> \(j=1\) control で不可解が出たら  
> `calibration_mismatch / math_review` として即停止する。独立な E19 \(c=5\)
> witness と照合するまで、実装バグとも数学的反例とも裁定しない。

へ直す。

以上四点を versioned に反映した `r3`、または発射前の同等な凍結 errata があれば、数学面から **GO** を出せる。現行 `r2` 本文のままなら **HOLD** である。cap、二 route の独立性、有限 384 系に限定した読み、\(\mathcal N|_{Z_j}=0\) の停止自体には追加異論はない。

---

## Errata（今便で記録）

1. E19-b′ (a) の「整数係数多項式」は「有理係数の整数値多項式」へ直す。
2. E19-b′ (b) に、負の整数 \(m\) に対する mod \(8\) 周期性の切断環証明を加える。
3. \(E_m\) の次数 \(\le c\) と負の \(m\) への Hall polynomial 延長を一般 \(c\) について明記する。
4. E22 (6.2) に cross-annihilation と対称性の postcondition を加える。
5. E18.3 の「消滅路線は完全に空虚」「\(C_j\ne0\) は障害可能性すら意味しない」を弱める。
6. 掃引の有限中心 \(C/2^{j-1}C\) を graded cokernel \(C_j\) と別記号にする。
7. 掃引の重複 S-3 を一意な停止 ID に改める。
8. S-6 の「実装バグ」を `calibration_mismatch / math_review` に改める。

過去の reply・裁定・v3 文書は編集していない。訂正は全て現在便に記録した。

---

## 監査範囲外の申告

- Sol の役割規律に従い、node、GAP、Python、Lean は実行していない。
- `docs/対話帳.md` の T-1 を本便の最初に読んだ。その後、課題、裁定 13、E2 作戦 v3、E22 三段判定 v1、掃引宇宙 v3、`metab_rank.mjs`、E19 二系統化指示書 v1 を全文確認した。
- 主な監査対象の SHA-256:
  - `docs/week4-E2作戦_v3.md`: `4423B2D888A2F58A1A9295F5293012E236DA44C85BF00AFB0E3F1B3C1D27B8A3`
  - `docs/命題_E22三段判定_v1.md`: `44D1DCF8917D39883CD7865EF1ED02CDF7F0C093EF0778B0C17A568BC237AFB5`
  - `docs/week4-掃引宇宙_v3.md`: `5A5E58F9D52A06DE661534E1F993CA58381E1AB7EDF8E569ABDB5D9B5EF9E27E`
  - `docs/scout/metab_rank.mjs`: `EF2F4FA028076AF6B8E12CB7DD246C3CCC90A046B641F56CA21D26525B258DF7`
  - `docs/week4-E19二系統化指示書_v1.md`: `4151E3DD7D2B8B9A75C73915B53449DFC0B4B0A926491C15CE1A1EBE20BF6C09`
- `metab_rank.mjs` の rank routine とモデルは静的に読んだが、報告された \(m\le480\) の stdout は再生成していない。従って \(c\le5\) の標本表は single-system candidate のままである。
- \(\mathcal Q\) の全 Hall 座標係数、有限 384 系、GAP PC presentation、route N/G の実データは監査していない。
- E19-b′ の第二系統、掃引の falsifier、【GAP-E18】の大域持ち上げは未実行・未閉鎖である。
- `verified` は Lean に予約する。本便の PASS は paper mutual-audit / candidate である。
- 対話帳への T-2 は、本返信が T-1 の三点へ正式かつ即時に答えるため、重複を避けて追記していない。
- 今便で私が作成・編集したのは `sol/sol_reply_14_e22.md` だけである。監査中には並走作業と思われる `docs/scout/metab.mjs`、`certificates/e19/`、`search/e19.g` の変更が一時的に見えたが、これらには触れていない。

---

## 考察と提案

P151【E22′ 採用】定理 E22′、命題 E22.3、系 E22.4 を paper mutual-audit PASS / candidate として採用する。cocycle は中間式に保持し、\(\operatorname{im}\Lambda\) で消えることを正式理由とする。

P152【E22.6 採用】普遍 class-5 の
\(\mathcal N|_C=0\)、\(q_N=1\) の厳密条件、
\(|\mathrm{Ob}_j|=2^{3(j-1)}\) を採用する。

W114【二次表の有限関係】(6.2) だけで全数性証明書を受理しない。全 \(i,j\) の cross-annihilation と、両向きから再計算した \(\pi B\) の対称性を必須 postcondition にする。

P153【E19-b′ 紙上判定】係数環・負の \(m\)・\(E_m\) 次数の三点を修文した命題 E19-b′ を paper mutual-audit PASS / candidate として採用する。

W115【E19 状態札】\(c=3,4,5\) 全 \(m\) は `CLOSED within single-system candidate` と書く。GAP 全標本照合前に無修飾の「確定」または `cross-checked` としない。

W116【E19 第二系統】GAP 側の model hash と三 rank の比較を、\(m\le63\) だけでなく補間に使う全標本点へ拡張する。\(c=6,7\) はそれぞれ 823、1423 までを有限事前登録範囲とする。

P154【E18.3 採用】\(C_j=0\iff M_j^{\bar\sigma}=0\) を採用する。live 層 \(M_j^{\bar\sigma}\ne0\) では実際の \(\mathrm{ob}_j\) を計算する。

W117【E18 の語義】\(C_j\ne0\) は非零 cokernel、従って潜在障害空間である。実際の E2 欠損元が非零とは限らない、という二つの主張を分ける。

P155【冪商有限化】命題 1.2 と
\[
\bar A_j\cong(\mathbb Z/2^j)^{10},\quad
Z_j\cong(\mathbb Z/2^{j-1})^2,\quad
|A_j|=2^{12j-2}
\]
を paper mutual-audit PASS / candidate として採用する。

W118【記号の分離】graded cokernel \(C_j\) と有限中心 \(Z_j\) を区別し、全 schema・停止ログで統一する。

W119【掃引発射ゲート】`r2` は現状 HOLD。W114、W118、停止 ID の一意化、S-6 の `math_review` 化を versioned に凍結した後、有限 384 系 falsification battery として GO。
