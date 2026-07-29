# 便 85 返信 — C-21/A7-fam・STR-1/H2′・ε・梯子・(n)/(o)・SAT

## 0. 総合判定

**総合判定: 分割採択。C-21 と A7-fam は PASS。STR-1 と H2′ は現行 statement package のままでは FAIL。(n) は PASS だが (o) に偽 PASS 経路が残るため、再発効と EP v7 発射は不許可。**

| 対象 | 独立判定 |
|---|---|
| **C-21** | **PASS** — paper-proof / framework-conditional |
| **A7-fam** | **PASS** — 全奇数 \(n\ge3\)、paper-proof / framework-conditional |
| 裁定 209 / A19-13t6 | **受領・PASS** — 奇パリティ枝で Ree 等号 |
| **STR-1** | **FAIL（現行 statement）** — 証明核は修理可能だが、(a) の型と便面の導来長系を直す必要がある |
| **H2′** | **FAIL（§3.0.1 全体）** — boxed core は PASS、しかし「\(Q\ne1\Rightarrow A^Q=0\)」が偽 |
| \(\varepsilon\) の \((P,c)\) 分解 | **PASS（紙上）** |
| M-1 / P-EPS-2 / P-EPS-5 package | **FAIL（現行形）** — norm の型落ち、交差ビット未測定、対抗予言の量化不備 |
| 梯子 prediction-first 17/17 | **PASS（的中の記録）** — 走査水準はなお GAP 単系統 |
| 追補 (n) v3 | **PASS** |
| 追補 (o) v4 / 再発効 | **FAIL** |
| **EP v7** | **発射不許可** |
| SAT \(n=21\) encoder completeness | **PASS（紙上補題）** |
| SAT/DRAT 実行結果 | **NOTE** — dispatch の `s VERIFIED` は受領。proof artifact 本体は作業ツリーになく、本返信では再読していない |
| 文献配達 | **受領** |

本便で Lean の意味の `verified` へ上げる主張はない。

指定された主要 digest はすべて一致した。

| artifact | SHA-256 |
|---|---|
| `c21_draft_v1.md` | `aabb7d96820e12e49da42f9ba1dd5ee9865d688f9fd50e47f86ee8636f9e5918` |
| `structthm_h2_v1.md` | `38d1fad0bb04382e8a590b7aad4b3feae0132b65f3aa82ec94a538679ed78953` |
| `epsilon_mechanism_v1.md` | `d44686a7a5dcd19d4240d302e61d1461f3549f7ece143250b5fbadcd166f028c` |
| 追補 (n) v3 | `46423604772da4809b3464a337f13f353c63e02808c2e8938fabe250f753bec6` |
| 追補 (o) v4 | `364c1b797b521f7dc04519d35edae02bf16fd5bf9c20d6a0241b00c19cd3f84a` |
| verifier A | `6e9237c2668f3cd7c47e8078a7b7482c30ff15efbc07dd850a4338ce7ba03226` |
| verifier B | `4a46d1d8552847e77a41e27d227af8afa0169c4e4395a648ca281a0960cf4f58` |
| evidence union | `4d7691ef91ed3f2e1db81cefa282eafd84d9bf1e9251ad0e9600541eca34c2fa` |
| 文献翻訳覚書 | `eadb58551d38adaa20c66ff51bd456efef8b0a3b1b14489c4cb49c21e62a27a9` |

---

## 1. C-21 と A7-fam

### F85-1.1 — C-21: PASS

#### C21-a / (S1): exact (TB4) は不要

依存鎖を BFC v2.15 の定理文だけでなく証明側まで追った。

1. 補題 B-5\(^{\rm u}\) は、(TB1)(TB2)(TB3)(TB4\(^{\rm u}\))+(W4) の下で
   B-5 の (i), (ii-loc), (iii), (7.1), (7.2) を与える。
2. 残る (ii-win) は定理 B-4(a) のモデル一意性から出る。
3. B-4(a) の前件は (TB1)–(TB3)+(W1)(W2)(W3)(W5)+(CAL) であり、
   exact (TB4) を含まない。
4. B-4(a) の証明で使うのも分裂、圏同値、B-4a/B-4b とコンパクト半群補題で、
   \(x,\sigma_\zeta\)、根生成元の exact identification は入らない。
5. exact (TB4) を使う B-4c は (ii-win) の証明経路ではない。

従って **A7 の全四成分は exact (TB4) でなく TB4\(^{\rm u}\) で閉じる**。反証点 1 は空振りである。

#### C21-a / (S2): per-window \((Z_{84}\text{-link})\) は不要

\((Z_{2M}\text{-link})\) が load-bearing なのは B-6 の torsor comparison、すなわち
\(b_{\rm op}=1\) を名指す段である。B-5 / B-5\(^{\rm u}\) の局所計算は
\(\tau\) と Rule-1/TB2 の二つの root object の同一視を使わない。

C-21 の結論は B-5 の

\[
(i),\quad(ii\text{-loc}),\quad(ii\text{-win}),\quad(iii)
\]

までであり、B-6、\(b_{\rm op}=1\)、(5′) を含まない。従って
**C-21 は \(Z_{84}\)-link の per-window migration を前件に持たない**。反証点 2 も空振りである。

#### C21-b / G3 の一般性

便 75 F3.2 は \(n=9,d=3\) に特殊化された証明ではない。記号を

\[
d\mid n,\qquad q_m:\widehat F_2\twoheadrightarrow P_m,\qquad
\widetilde H_m=q_m^{-1}(H_m^{\rm fun})
\]

として、

\[
\widetilde H_n\subseteq\widetilde H_d,\qquad
\widetilde H_d=\widetilde H_n\bar N_d
\]

から descent subgroup の包含を出す abstract lemma である。個別段に必要なのは
HF-2 と両段の (W1)。従って \((21,3)\) と \((21,7)\) の双方へそのまま適用できる。

#### 族入力

(W1)–(W5)+(CAL) の供給範囲も再点検した。

- (W1): 全 \(n\ge3\)。
- (W2) 群論側・算術側: 全奇数 \(n\ge3\)。
- (W3)(W4): ODD-H / HF-1、全奇数 \(n\ge3\)。
- (W5): \(\Phi(\mathfrak F_0)\) が内部自己同型として作用するため全奇数 \(n\)。
- (CAL): 窓非依存。
- 合成段で必要な HF-2/HF-3 は \(d\ge3\)、\(\alpha=1\) で満たされる。

\(n=21\) の素数性や素数冪性はどこにも使わない。よって

\[
\boxed{\text{C-21 = CLOSED (paper-proof / framework-conditional)}}
\]

を承認する。C-21 自体は \(u_{21}\) の数値、B-6、\(Z_{84}\)-link を主張しない。

`c21_cal_20260729.json` の SHA-256 は
`ba0e3dfb7e33cc7bd5a9667ec0aacfdafec5de18b58a514bcf0c107549ba3e33`。
q1–q8 の survey は記録値と整合し、8/8 の較正申告を受ける。ただしこれは
**GAP 単系統の較正**であり、C-21 の紙上証明を機械的に cross-check したという意味ではない。

### F85-1.2 — A7-fam: PASS

C-21 の合成で \(21\) 固有に使ったものは「奇数 \(n\ge3\)」だけである。
従って同じ証明を任意の奇数 \(n\ge3\) に読み替えれば、

\[
\boxed{
\text{(TB1)(TB2)(TB3)(TB4}^{\rm u}\text{)+(CAL) の下で、
A7 は全奇数 }n\ge3\text{ で成立}
}
\]

を得る。

これは C-21 とは別札で **PASS**。状態は
`paper-proof / framework-conditional / not Lean-verified` とする。
CASC【I23-a】はこの意味で解消してよく、\(q=7\) の帳簿は便面どおり
**C1′+C5** に縮む。C5 の survey は較正であって A7-fam の前件ではない。

### P85-1 — 台帳への推奨記法

C-21 と A7-fam を一つの claim に潰さず、次の二行に分けるのがよい。

```text
C-21    = A7@21; paper-proof/framework-conditional; CLOSED
A7-fam  = A7@odd n>=3; paper-proof/framework-conditional; CLOSED
```

これにより、将来 C-21 固有の C1′/C5 と、族命題の射程が混線しない。

---

## 2. 裁定 209 / A19-13t6

### F85-2.1 — 受領・PASS

便 84 F84-4.3 と同じ計算を維持する。

\[
\begin{array}{c|c}
\varepsilon=0\ (k\text{ 偶}) & 11+7+5=23>21\\
\varepsilon=1\ (k\text{ 奇}) & 10+7+4=21=19+2
\end{array}
\]

実現対は後者であり、\(k=9,j=6,m=3\)、\(u\) の型は
\((13,2,2,2)\)。従って A19-13t6 は Ree 違反ではなく等号生存。
撤回と現役復帰を受領する。

D4 チェックリストの「両パリティ枝を必ず評価する」は load-bearing な恒久修理である。

---

## 3. STR-1 と H2′

### F85-3.1 — STR-1 の証明核

次の部分は紙上で通る。

1. (H1)(H3) から \(A,S\trianglelefteq G\)、\(z\in Z(G)\)、
   \(G=S\circ_{\langle z\rangle}C_G(S)\)。
2. \(\bar C=C_G(S)/A\) は
   \(1\to\langle z\rangle\to\bar C\to Q\to1\) という中心拡大。
3. \((c)\Rightarrow(b)\): \(\bar C\) の分裂補群の逆像 \(Y\) に対し、
   (H2) と Schur–Zassenhaus を使って \(A\) の補群を \(Y\le C_G(S)\) 内に取る。
4. \((b)\Rightarrow\) 内部直積 \(G=S\times AH\)。
5. \((c)\Leftrightarrow(d)\): Sylow 2 部分への制限と Gaschütz/Frattini 判定。
6. (6): restriction-corestriction による
   \(H^2(Q;C_2)\to H^2(Q_2;C_2)\) の単射、および \(Q_2\) 巡回時の
   唯一の involution への再制限は正しい。

特に \(\operatorname{res}\) の単射性について、
\(\operatorname{cor}\operatorname{res}=[Q:Q_2]\) は 2-primary な
\(H^2(Q;C_2)\) 上の奇数倍なので可逆である。ここに穴はない。

### F85-3.2 — STR-1 の blocker 1: (a) の型

現行 (a)

\[
G\cong S\times(A\rtimes Q)
\]

は抽象群としての同型に読める。一方、証明の \((a)\Rightarrow(c)\) は

\[
G=S\times X,\qquad A\trianglelefteq X,\qquad X/A\cong Q
\]

という、**指定済みの内部部分群 \(S,A,K\) を尊重する分解**を使っている。
抽象同型だけでは、その同型が本 theorem data の \(S,A\) を各因子へ送ることは書かれていない。

従って (a) は例えば次へ retype すべきである。

> (a\(_{\rm int}\)) \(X\le C_G(S)\) が存在し、
> \(A\trianglelefteq X,\ X/A\cong Q,\ G=S\times X\)。
> さらに \(X\cong A\rtimes Q\)。

これなら \((b)\Rightarrow(a_{\rm int})\Rightarrow(c)\) と証明が逐語一致する。

### F85-3.3 — STR-1 の blocker 2: 便面の導来長系

STR-1(4) 本文の正しい一般式は

\[
\operatorname{dl}(G)=
\max\{\operatorname{dl}(S),\operatorname{dl}(A\rtimes Q)\}.
\]

便面の

\[
\operatorname{dl}(G)=\max\{\operatorname{dl}(S),2\}
\]

は一般の STR-1 の系ではない。明示反例は

\[
G=D_8\times S_4,\qquad K=D_8,\qquad A=1,\qquad Q=S_4.
\]

(H1)(H2)(H3) と \(\varepsilon=0\) は全て成立するが、

\[
\operatorname{dl}(G)=3,\qquad
\max\{\operatorname{dl}(D_8),2\}=2.
\]

「2」へ特殊化できるのは、別前件
\(A\rtimes Q\cong\operatorname{Hol}(C_N)\) などから
\(\operatorname{dl}(A\rtimes Q)=2\) を得た窓だけである。

### STR-1 判定

\[
\boxed{\text{STR-1 = FAIL as currently stated}}
\]

ただしこれは中心拡大の証明核の崩壊ではない。(a) を内部型へ直し、
導来長 \(=2\) を Hol 窓の系へ分離すれば、修正版 STR-1 は紙上 PASS にできる。

### F85-3.4 — H2′ (i): アーベル \(A\) での置換

\(A\) がアーベルなら、関連する拡大

\[
1\to A\to Y\to Q\to1
\]

の固定された \(Q\)-作用に対する拡大類は \(H^2(Q;A)\) に住む。
従って

\[
H^2(Q;A)=0
\]

だけで \((c)\Rightarrow(b)\) に必要な補群の**存在**は出る。
\(H^1(Q;A)=0\) は補群の \(A\)-共役一意性に必要であって、STR-1 の TFAE の存在部分には過剰である。

よって「(H2) を (H2′) \(H^1=H^2=0\) へ置換できる」は十分条件として正しい。
ただし最小前件は TFAE については \(H^2=0\) である。

### F85-3.5 — H2′ (ii): 巡回群と Tate 2 周期性

\(Q=\langle\sigma\rangle\) が巡回なら

\[
H^2(Q;A)=A^Q/N_QA,\qquad
H^1(Q;A)=\ker N_Q/(\sigma-1)A.
\]

\(A^Q=0\) なら \(\ker(\sigma-1)=0\)。有限 \(A\) 上で
\(\sigma-1\) は単射、従って全射であり
\((\sigma-1)A=A\)。さらに \(N_Q(\sigma-1)=0\) から \(N_Q=0\)。
従って

\[
H^1(Q;A)=H^2(Q;A)=0.
\]

この boxed implication は PASS。

### F85-3.6 — H2′ の blocker: \(Q\ne1\) は fixed-point-free を意味しない

§3.0.1 の

> \(Q\le(\mathbf Z/9)^\times\) が非自明なら \(A^Q=0\)

は偽である。反例を枝 B の中に取れる。

\[
Q=\langle4\rangle\cong C_3\le(\mathbf Z/9)^\times,\qquad A=C_3.
\]

\(4\equiv1\pmod3\) なので \(Q\) は \(A=C_3\) に自明に作用する。従って

\[
A^Q=A\ne0,\qquad
H^1(C_3;C_3)\cong C_3,\qquad
H^2(C_3;C_3)\cong C_3.
\]

よって

\[
Q\ne1\Longrightarrow(H2')
\]

は成り立たない。正しい下流条件は

\[
Q=C_6\quad\text{（現梯子の実測）}
\]

または直接 \(A^Q=0\) を仮定すること。現梯子では
\(Q=C_6=\langle2\rangle\) が実測されているので、この修理は
梯子の実際の STR-1 適用を反転させない。

### F85-3.7 — H2′ (iii): 非アーベル \(A\)

二つを分ける必要がある。

- 元の (H2) を維持するなら、Schur–Zassenhaus は \(A\) の可換性を要しない。
  \(A\) を奇位数群へ広げた STR-1 は、\(Z(K)=Z(A)\times Z(S)\) 等の文言を直せば
  同じ方法で進められる。
- (H2′) を ordinary \(H^2(Q;A)\) の消滅として非アーベル \(A\) に移すことはできない。
  非アーベル kernel の拡大分類は通常の群値 \(H^2(Q;A)\) ではない。
  「関連する全ての \(Y\) が分裂する」を直接前件にするか、
  outer action と非アーベル extension の pointed-set obstruction を明示する必要がある。

### H2′ 判定と修理案

\[
\boxed{\text{H2′ §3.0.1 package = FAIL}}
\]

boxed core は PASS だが、その \(N_{\rm ord}=9\) への「\(Q\ne1\)」特殊化が偽なので、
現行節全体を通すことはできない。

### P85-2 — 修正版 H2′

次の二段に分けることを推奨する。

> **H2′-exist.** \(A\) は有限アーベル \(Q\)-加群で
> \(H^2(Q;A)=0\)。すると STR-1 の \((c)\Rightarrow(b)\) が成立する。
>
> **H2′-uniq.** さらに \(H^1(Q;A)=0\) なら補群は \(A\)-共役を除いて一意。
>
> **Cyclic criterion.** \(Q\) が巡回かつ \(A^Q=0\) なら
> H2′-exist と H2′-uniq がともに成立。

適用欄は「全射、または少なくとも \(Q\ne1\)」でなく
「\(Q=C_6\)、または \(A^Q=0\) を別途確認」に直す。

---

## 4. \(\varepsilon\) 機構

### F85-4.1 — \((P,c)\) と次元公式: PASS

\[
Q_2\cong\prod_{i=1}^r C_{2^{a_i}}
\]

に対する中心拡大を、生成元 lift の冪ビット \(P(a_i)\) と
交換子ビット \(c(a_i,a_j)\) で記述する部分は正しい。UCT から

\[
0\to\operatorname{Ext}^1(Q_2,C_2)
\to H^2(Q_2;C_2)
\to\operatorname{Hom}(\Lambda^2Q_2,C_2)\to0
\]

を得て、

\[
\dim_{\mathbf F_2}H^2(Q_2;C_2)
=r+\binom r2.
\]

\(Q_2=C_4\times C_2\) で \(-1=a^2b\) と書いたとき

\[
P(-1)=P(a)+P(b)
\]

しか見えず、\(c(a,b)\) を見ないという警告も正しい。従って
\(-1\) 層だけで十分なのは \(Q_2\) が巡回、D4 系の奇数 \(N\) では
実質的に \(N\) が素数冪のとき、という運用警告を承認する。

### F85-4.2 — M-1 の blocker 1: norm の型落ち

§3.2 の正しい式は

\[
P(u)=\operatorname{pr}_{\langle z\rangle}
\bigl(\mathcal N_{T,n}(f)\bigr).
\]

従って \(P(u)=0\) が意味するのは

\[
\mathcal N_{T,n}(f)\in A,
\]

または同値に \(C_G(S)/A\) で lift が最小位数を持つことである。
一般には

\[
\mathcal N_{T,n}(f)=1
\]

までは出ない。

梯子証明書自身に反例がある。`W-E-A10-9t1` の \(u=7\) 層では

- \(\operatorname{ord}(u)=3\)、
- \(\widetilde G=C_G(S)/A\) の lift-order distribution は `[3:9]`、
- \(P\)-bit は false、
- しかし記録された実 lift は `ord_G=9`。

つまり quotient の中心ビットは消えているが、norm の \(A=C_9\) 成分は非自明になりうる。
従って M-1 の

\[
\text{centralizing}\Rightarrow\mathcal N_{T,n}(f)=1
\]

は現データによって既に反証されている。

### F85-4.3 — M-1 の blocker 2: 冪ビットから交差ビットは出ない

全生成元について「最小位数 lift がある」ことは \(P(a_i)=0\) を与えるだけで、

\[
c(a_i,a_j)=0
\]

を与えない。純粋な \(\Lambda^2\) 成分を持つ中心拡大では、全 generator lift が
同位数でも拡大は非可換・非分裂になりうる。

交差ビットの正しい検査は、選んだ lift \(g_i,g_j\) に対し

\[
[g_i,g_j]\in A
\]

を、すなわち \(\bar C=C_G(S)/A\) で commute することを直接調べること。
従って P-EPS-2 の層別最小位数検査を
「\(\varepsilon=0\) の検査」と呼んではならない。

### F85-4.4 — 164/164 と 24 点の会計

次の二種類を加算しない方がよい。

- 三 D4 窓: **164 個の centralizing shadow** の個体検査。
- 梯子四窓: \(4\times6=\)**24 個の \(u\)-layer predicate**。

後者の各 layer は内部に 9 個または 18 個の shadow を含む。
従って「188/188」は異なる単位を足した表示である。

```text
D4 windows: 164/164 shadow-level minimum-order observations
A13 ladder: 24/24 layer-level P-bit tests
```

と分けて記録する。さらにいずれも交差ビットの検査数ではない。

### F85-4.5 — M-1 と P-EPS-5 は現状では論理的な二者択一でない

P-EPS-5 の「\(S>D_8\) なら \(\varepsilon\ne0\) が起こりうる」は存在可能性の主張である。
一つの \(S>D_8\) 窓で \(\varepsilon=0\) が出ても、この存在主張は反証されない。
逆に一つでも \(\varepsilon\ne0\) が出れば universal M-1 は反証される。

また \(P=0\) かつ \(c\ne0\) なら、現行の最小位数検査は全 PASS しながら
\(\varepsilon\ne0\) であり、現行 P-EPS-2 と P-EPS-5 は同時に成立しうる。

従って「\(S\ne D_8\) の一窓で決着」は量化を直さない限り偽。
反証可能な札にするなら、例えば

> **P-EPS-5′.** 最初に実現する、(H1)(H3) と \(Z(S)=C_2\) を満たす
> tail-8 窓で \(\varepsilon\ne0\)。

のように「指名した第一窓」の値を凍結する必要がある。

### P85-3 — M-1 の修正版

M-1 は二つの独立候補へ分割すべきである。

> **M-1P.** centralizing shadow \(g=(m,f)\) について
> \(\operatorname{pr}_{Z(S)}\mathcal N_{T,n}(f)=1\)、
> すなわち \(\mathcal N_{T,n}(f)\in A\)。
>
> **M-1c.** \(Q_2\) の invariant-factor basis の lift を
> \(C_G(S)\) 内で選び、全対について \([g_i,g_j]\in A\)。

\(M\)-1P と M-1c の両方があって初めて \(\varepsilon=0\) になる。
§3.3 の raw cocycle 式は、shadow の積・逆元規約からの導出を一段付けるまで
group-level cocycle

\[
g_ug_vg_{uv}^{-1}\pmod A
\]

を正本にするのが安全である。

### P85-4 — 次の \(S\ne D_8\) 窓の設計

二段を推す。

1. **安価な vector-center pilot: `W-D-A19-13t6`。**
   既に実現対がある。ただし予想される
   \(S=\operatorname{Syl}_2(S_6)\cong D_8\times C_2\) は
   \(Z(S)\cong C_2^2\) で、現ノートの coefficient \(C_2\) を外れる。
   従ってこれは一般化コードの較正・M-1 の反例探索にはよいが、
   P-EPS-5′ の一ビット比較窓にはならない。
2. **clean tail-8 fork: \(\ell=17,n=25,t=8\)。**
   まず SAT で実現 existence を判定する。実現した場合に限り、
   \(S=\operatorname{Syl}_2(S_8)\)、\(Z(S)=C_2\)、(H3) を先に確認し、
   その後で \(\varepsilon\) を測る。

tail-8 では \(-1\) 層一個だけでなく、次を certificate に必須化する。

```text
Q_2 invariant-factor basis
P(a_i) for every basis generator
c(a_i,a_j) for every pair
H3 and Z(S)
the chosen lift identities and their quotient orders
```

これが M-1P/M-1c と P-EPS-5′を本当に分離する最小 signature である。

---

## 5. 梯子 17/17 と諮問 P85-a

### F85-5.1 — prediction-first の時系列と証憑

凍結 commit は
`41b8698b5bcc82de733e207e155ae00247abff2e`
（2026-07-29 22:01:20 +09:00）。現行予言文書の SHA-256 は
`1bdaf891af275ce27890df7d948d10da6445d953a21bdacb92c34b44aec7ff38`
で、対象ファイルに未記録差分はない。

manifest:

```text
search/certs/a13_ladder_manifest_20260730.json
sha256 = b9d2b02d021e53e6a63fc6d5d2ac47c4b7ad7aeed8731da54a63d89add03eb4a
```

について、

- `windows_processed=13`、
- 全 13 窓で stage-1/gate PASS、
- manifest に記録された全 cert digest と実ファイル digest が一致、
- canonical 4 窓と sibling 9 窓を全て収録

を確認した。

### F85-5.2 — 四 canonical 窓

| 窓 | \(|G|\) | \(K\) | odd / 2-part | \(Q\) | \(\varepsilon\) | IdGroup |
|---|---:|---|---:|---|---|---|
| A10-9t1 | 54 | \(C_9\) | \(9/1\) | \(C_6\) | 0（vacuum） | \([54,6]\) |
| A11-9t2 | 108 | \(C_{18}\) | \(9/2\) | \(C_6\) | 0 | \([108,26]\) |
| A12-9t3 | 108 | \(C_{18}\) | \(9/2\) | \(C_6\) | 0 | \([108,26]\) |
| A13-9t4 | 432 | \(C_9\times D_8\) | \(9/8\) | \(C_6\) | 0 | \([432,362]\) |

従って

- Cyc 律は \(C_{N_{\rm ord}}=C_9\)、
- Tail 律は \(\operatorname{Syl}_2(S_t)\)、
- \(t=4/t=1\) の 2-part 比は 8、
- 三つの非自明比較で
  \(\operatorname{GTSh}\cong\operatorname{Syl}_2(S_t)\times
  \operatorname{Hol}(\mathbf Z/9)\)、
- sibling 9 窓は対応する \((N_{\rm ord},t)\) の canonical 値と一致

という 17 欄の読みは正しい。NULL は発火していない。

H2′ の §3.0.1 に上で見つけた誤りは、実測 \(Q=C_6\) では
\(A^Q=0\) が成立するため、梯子の構造的中自体を反転させない。

### F85-5.3 — 三段語法

`a13_ladder_witness_recheck_20260730.json` の SHA-256 は
`7438b1d2fffa98638be743b845ce8de3f68070793e061a3c0d5b9198dcb6d0bb`。
Python/SymPy は全 13 窓で各 16 assertion を再計算し、全 PASS。
従って生成対、braid、\(c=1\)、\(N_{\rm ord}=9\)、\(\widetilde\theta\)、
\(\widetilde\tau\)、\(|B_q|=6|A_n|\)、\(|P|=|A_n|\) は独立系統で一致する。

一方、この certificate type は個別 \((m,f)\) witness を記録しない。
従って

- F2 三条件、
- \(P/B_q\) 水準の settled、
- (3.53) の二順比較、
- Ξ 制限された全 candidate set と `settled_fail_count=0`

は独立再列挙されていない。これは証明書自身の scope note と一致する。

従って梯子の正しい札は

```text
prediction-first 17/17 = PASS
generation-pair layer = cross-checked
CorrectedShadowsXi aggregate scan = GAP single-system
Lean verified = no
```

である。

### F85-5.4 — 【P85-a】回答

**回答: ladder law を cross-checked claim / theorem candidate へ上げる前に、
GAP 非共有の `CorrectedShadowsXi` を実装すべきである。現行 SAT 線は代替にならない。**

ただし目的を分ける。

- 「凍結 17 欄が GAP 測定に対して 17/17 的中した」と記帳するだけなら、今の証憑で足りる。
- 「全 Ξ candidate を走査し、全て settled、受理集合がこの集合である」を
  cross-checked と呼ぶなら、今実装する必要がある。

現行 SAT encoder は \(n=21\) の

\[
a:2^{10}1,\quad b=a u^{-1}:3^7,\quad \langle a,b\rangle\text{ transitive}
\]

という permutation-class 問題を符号化する。A13 ladder の F2、\(R_\tau\)、
settled、(3.53)、shadow composition は符号化していない。
従って方法が独立でも**別 predicate**であり、代替にはならない。

### P85-a 実装仕様

fresh Node/Python 実装は次を満たすべきである。

1. GAP の `kerchi-judge.g` や helper を import/翻訳しない。
2. \(P\), \(B_q\), \(\widetilde\theta,\widetilde\tau\)、action を
   generator image から独立に構成する。
3. \(m\) は \(\mathbf Z/N_{\rm ord}\) の class、
   \(u=2m+1\) は \((\mathbf Z/2N_{\rm ord})^\times\) の元として型を分ける。
   action で \(u\) を早まって mod \(N_{\rm ord}\) に落とさない。
4. subgroup は位数だけで同一視しない。生成部分群の相互包含または canonical element set で比較する。
5. F2 三条件、settled homomorphism の existence、(3.53) の両順を全 candidate ごとに再計算する。
6. 比較値は総数だけでなく、canonical UID を付けた accepted set と
   fail witness set の digest にする。

実行順は

```text
A10-9t1 canonical (486; naive-vs-Xi calibration)
  -> A13-9t4 canonical (139,968; priority stress)
  -> A11/A12 canonical
  -> sibling 9 windows
```

を推す。SAT が代替できるのは、将来 SAT 側がこの**同じ predicate**を再符号化し、
数学 candidate と CNF model の全単射/completeness を別証明した場合だけである。

---

## 6. (n)/(o) 再発効請求 v2

### F85-6.1 — 4 suite 再走

公称値をローカルで再現した。

```text
lane A           93/93
lane B          184/184
normalizer       51/51
evidence-union   94/94
合計            422/422
```

以下の FAIL はこの 422 件の外側に置いた敵対 probe による。

### F85-6.2 — 追補 (n) v3: PASS

次を確認した。

- 両 lane が ASCII `[0-9]` と全体一致を用いる。
- `-0`、末尾 newline、全角数字、Arabic-Indic digit を両 lane で拒否。
- `side_pair=["searcher","checker"]` が順序つきで、swap は MALFORMED。
- chart transport を UNKNOWN とする状態札は実装の能力と一致。
- canonical W-4 entry の七欄と native binding が文書・実装で同期。

従って (n) は単独で発効可能な内容になった。

### F85-6.3 — 追補 (o) v4: FAIL

schema nominal gate は強くなったが、**schema は provenance でも signature でもない**。
現実装は producer が正しい shape の偽 RouteResult を作る経路を閉じていない。

最小 probe は次の結果になった。

```text
h = "a"*64
r1 = route_result_pass("R1", h,h, 1,1, h,h)
r2 = route_result_pass("R2", h,h, 1,1, h,h)

r1.claim_source_ref = None
r1.evidence_refs    = None
coerce(r1, "R1")    = PASS
union(r1,r2)        = PASS

route_from_verifier_b_w6("BOGUS", forged_detail, "R2").route_status
                    = PASS
```

ここには四つの blocker がある。

#### B85-o1 — raw producer の self-asserted PASS が通る

`main()` は `{route1,route2}` という **already-built RouteResult dict** を JSON から読み、
そのまま `evidence_union_fail_closed_v2` へ渡す。
攻撃者は正しい `schema_id`、`R1/R2`、同じ偽 digest/count を書けばよい。
strict shape を満たすことは、その値が route-specific verifier から来た証明にならない。

文書 §「public combinator の義務」の
「raw producer JSON を RouteResult として直接受ける経路は存在しない」と
実装 `main()` は一致しない。

#### B85-o2 — provenance refs が必須でない

PASS/FAIL shape は `claim_source_ref` と `evidence_refs` を allowed field にするが、
`coerce_to_route_result` は non-None、shape、参照先 digest のいずれも検査しない。
constructor の default `None` のままで PASS する。

#### B85-o3 — status enum の fall-through

`route_from_verifier_b_w6` は ABSENT/MALFORMED/FAIL だけを分岐し、
それ以外を全て PASS branch へ落とす。従って `"BOGUS"` が PASS になる。

#### B85-o4 — connector 自身が armature/placeholder

source docstring は、この connector が

- `expected_domain_count=checked_domain_count=1` を hardcode、
- detail 自身の hash を claim/evidence/coverage 全てに再利用、
- full EP v7 wiring は deferred

であると明記する。この自己申告は正直だが、**armature を operative evidence route として
再発効することはできない**。

### P85-5 — (o) の必要修理

1. 公開 CLI は RouteResult を入力にしない。raw evidence artifact を入力にし、
   receiver 側の固定 dispatch が R1/R2 の route-specific verifier を呼ぶ。
2. `build_R1(raw)` と `build_R2(raw)` を別関数にし、caller が `route_id` を渡せない形にする。
3. route verifier の status は exhaustive enum match とし、未知値は必ず MALFORMED。
4. `claim_source_ref` / `evidence_refs` を non-null structured required field にし、
   受領側が参照先を解決して digest を再計算する。self-reported digest の比較だけにしない。
5. placeholder count/digest を廃止し、実 domain、native artifact、coverage set から算出する。
6. 少なくとも上の三 probe
   `valid-shape forged PASS`、`refs=None`、`unknown w6_status`
   を負例として追加する。
7. in-process API でも raw RouteResult dict を public trust boundary に置かない。

### §6 発効判定

\[
\boxed{\text{(n) PASS,\quad (o) FAIL,\quad EP v7 = NO-GO}}
\]

422/422 は既登録 schema mutation への回帰として有用だが、上の trust-boundary 反例を覆わない。

---

## 7. 文献配達

### F85-7.1 — 受領確認

`docs/notes/litgate_epsilon_translation_v1.md` と
`docs/scout/scout_report_structthm_20260730.md` を読み、配達 PDF 5 本の SHA-256 を
`provenance/LEDGER.md` 2026-07-30 欄と照合した。全て一致した。

- `arxiv_2603.24743.pdf`: `eadee8...63890`
- `arxiv_2305.13178.pdf`: `583504...893d`
- `arxiv_1604.04415.pdf`: `16a249...dea`
- `arxiv_1407.3112.pdf`: `416c0a...84b`
- `arxiv_math_0606374.pdf`: `940d9d...af2d`

覚書の訂正、すなわち Korbelář–Tolar/Galindo の
「4 で割れる」の主語は \(|Q|\) でなく Heisenberg kernel の dimension parameter \(N\)、
という読みを採用する。ただし GT-shadow の \(S\) への転用はなお類推であり、
P-EPS-5 の証明ではない。

本返信では原著 5 本を全ページ精読していない。覚書、scout report、配達 digest と、
ε ノートが申告した限定読解範囲を監査した。

---

## 8. SAT 線

### F85-8.1 — artifact と local check

現物 CNF は manifest と一致する。

| CNF | vars | clauses | SHA-256 |
|---|---:|---:|---|
| class | 672 | 14,806 | `6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33` |
| transitive | 9,723 | 50,128 | `02fcc56722880ccba8c6dcf83c80886b009d3b0f454d0d44a0c96874eba17113` |

`node search/sat/check_model_n21.mjs --self-test` も PASS。
fixture から再計算した \(a\) は \(2^{10}1\)、\(b\) は \(3^7\)、
product convention は \(b(i)=u^{-1}(a(i))\)、orbit partition は \([6,15]\)。

workflow の theorem run で hash 必須、tool/action SHA pin、input allowlist を置く修理も確認した。

### F85-8.2 — completeness 補題

> **補題 SAT-COMP-21.**
> 固定した
> \[
> u=(1\,2\,\dots\,13)(14\,15)(16\,17)(18\,19)(20\,21)
> \]
> に対し、\(a\) が型 \(2^{10}1\)、\(b=a u^{-1}\) が型 \(3^7\)、
> \(\langle a,b\rangle\) が推移的なら、
> `tail8_n21_transitive.cnf` は充足可能である。

**証明。**

1. \(X_{ij}=1\ (i<j)\) を \(a(i)=j\)（従って \(a(j)=i\)）のとき、
   \(D_i=1\) を \(a(i)=i\) のときと定める。
   \(a\) は involution なので各 row exactly-one を満たし、
   型 \(2^{10}1\) なので \(D_i\) は全体で exactly-one。
2. \(B_{ik}=1\iff b(i)=k\) と置く。
   規約 \(b(i)=u^{-1}(a(i))\) より
   \[
   B_{ik}=1\iff a(i)=u(k),
   \]
   したがって encoder の \(B\)-Tseitin biconditional を全て満たす。
3. \(b\) は型 \(3^7\) なので fixed-point-free かつ \(b^3=1\)。
   \(B\) は permutation matrix であるため、encoder の全
   \(b^3\)-implication と diagonal negative clause を満たす。
4. \(i<j\) に対し
   \[
   E_{ij}=1\iff
   j\in\{a(i),b(i),b^{-1}(i)\}
   \]
   と定める。これは \(\{a,b,b^{-1}\}\) による無向 Schreier graph の
   adjacency そのもので、\(E\) の biconditional を満たす。
5. \(R_{t,v}=1\) を「頂点 1 から \(v\) まで距離 \(\le t\)」と定め、
   \[
   \operatorname{STEP}_{t,w,v}
   =E_{wv}\wedge R_{t-1,w}
   \]
   と定める。すると base case、AND Tseitin、recurrence biconditional を全て満たす。
6. \(\langle a,b\rangle\) が推移的ならこの graph は連結。
   21 頂点の連結 graph では点 1 からの距離は高々 20 なので、
   全 \(v\) に対し \(R_{20,v}=1\)。最後の goal clauses も満たす。

以上で genuine witness から CNF assignment を構成できる。 \(\square\)

同じ構成の 1–3 だけで class CNF の completeness も従う。

### F85-8.3 — 固定 \(u\) で十分な理由

対象 cycle type の全 \(u'\) は \(S_{21}\) で共役である。
\(u'=huh^{-1}\) に対する witness \((a',b')\) を同時共役すれば、
固定 \(u\) に対する witness を得る。cycle type と推移性は同時共役で保存される。
従って固定 representative の transitive CNF が UNSAT なら、同 cycle class の
全 \(u\) に対して transitive witness は存在しない。

A21-generation は推移性を含意するので、

\[
\text{transitive UNSAT}\Longrightarrow
\text{\(A_{21}\)-generating pair なし}.
\]

これで encoding fidelity の数学 witness \(\Rightarrow\) assignment 方向は閉じた。

### F85-8.4 — DRAT 語法

dispatch が報告する `drat-trim: s VERIFIED` は、
上の exact hash の CNF が UNSAT であることの DRAT 照合である。
上の completeness 補題と合成すれば数学的非存在を読める。

ただし `proof.drat(.gz)`、`proof.lrat(.gz)`、`drat_verify.txt`、
`SHA256SUMS.txt` は現在の作業ツリーにない。本返信では CI artifact 本体を
再 hash・再実行していない。従って私の判定は

```text
encoding completeness = paper-proof PASS
CI DRAT verification   = dispatch receipt accepted / artifact not re-read here
independent LRAT check  = not done
Lean verified           = no
```

である。artifact を台帳へ束縛した時点で、GAP 悉皆と SAT/DRAT の
**独立方法による cross-check** と記録してよい。

### F85-8.5 — mutant matrix の監査

M1/M3/M4 の UNKNOWN は誤りでなく、現状を正直に表す。

- M1 class SAT の共役論法は正しいが、transitivity は保存されないので UNKNOWN。
- M3/M4 は class 側では単なる弱化なので SAT。transitive 側は新 cycle type を許すため UNKNOWN。
- M2 の UNSAT は diagonal exactly-one と fpf の直接矛盾で PROVEN。
- M5 の SAT は class instance への退化で PROVEN。
- M6 はこの instance がそもそも非連結なので、depth 19/20 の境界検査として弱い。

従って UNKNOWN 三行を solver の出力だけで「mutant closure」と数えてはならない。
ただしこれらは diagnostic matrix の残務であって、上の completeness lemma の前件ではない。

### P85-6 — 次の SAT hardening

優先順を次とする。

1. **reachability reverse-clause drop mutant**:
   \(R\Rightarrow(R_{\rm prev}\vee STEP)\) を落とす。
   class model に全 \(R_{t\ge1,v}=1\) を足せるので、transitive mutant は
   紙上 SAT。BFS の「自由に true」事故を鋭く検出する。
2. **edge reverse-clause drop mutant**:
   \(E\Rightarrow\) genuine adjacency を落とす。
   全 edge を true にできるため紙上 SAT。
3. **synthetic diameter boundary fixture**:
   真の直径がちょうど 20 の 21-頂点 path を固定して、
   depth 20 SAT / depth 19 UNSAT を照合する。
   現 M6 より境界検査として決定的。
4. **小次数 exhaustive calibration**:
   parameterized encoder を \(n=5,7\) 程度で全 permutation 列挙と突合する。
5. **独立 LRAT checker**:
   `drat-trim` が生成した LRAT を別実装で読む。theorem run の次段に必須化する。

標的順は前便どおり

\[
(c)\ n=21\text{ calibration}
\ \longrightarrow\
(b)\ \ell=17,n=25\text{ existence}
\ \longrightarrow\
(a)\ dl\ge3\text{ shadow}
\]

を維持する。特に \(\ell=17,n=25\) が SAT なら、§4 の full \((P,c)\) signature
を次の measurement contract にする。

---

## 9. 残務申告

便面 §9 の

- Ree capsule NOTE 3 点、
- ladder driver への個別 witness 欄追加、
- judge v1.4 の Ξ 会計 schema / 較正負例、
- `wac_tail8` stale 文の除去

は本便の請求外として受領した。本返信では判定も修正もしていない。

---

## ★ 教材

1. **schema は provenance ではない。**  
   正しい `schema_id` と field shape は誰でも書ける。origin を主張するなら、
   receiver-side dispatch と raw artifact の再 hash が要る。

2. **同じ位数で持ち上がることと拡大が分裂することは、rank \(>1\) では別。**  
   冪ビット \(P\) を全部消しても \(\Lambda^2\) 由来の交差ビット \(c\) が残る。

3. **抽象同型と指定部分群を尊重する内部同型を混ぜない。**  
   TFAE の証明が \(G=S\times X\) を使うなら、statement もその \(S,X\) を量化する。

4. **「作用が非自明」と「fixed-point-free」は別。**  
   \(4\in(\mathbf Z/9)^\times\) は \(C_9\) には非自明に作用するが、
   \(C_3\) には自明に作用する。

5. **DRAT は CNF を証明し、completeness が数学との橋を作る。**  
   `s VERIFIED` だけでは encoder の意味は証明されない。

6. **計数の単位を足さない。**  
   164 個の shadow と 24 個の layer predicate を「188 trial」と呼ぶと、
   統計的にも論理的にも何を数えたかが消える。

---

## 監査範囲

### 実施したこと

- 便 85 の全 numbered section 0 相当の導入から §9、返信様式まで全文読解。
- 対話帳の最新 T-17 まで確認。
- C-21、BFC v2.15 関連節、便 75 F3.2、STR-1、H2′、ε ノートを紙上監査。
- 指定 digest、C21 survey、ladder manifest/cert 13 本、witness recheck、
  epsilon ladder cert を読解・hash 照合。
- (n)/(o) の 4 suite 422/422 を再走。
- evidence-union に新しい敵対 probe を実行。
- SAT manifest、encoder、checker、mutant matrix、workflow、CNF header/hash を監査し、
  checker self-test を再走。
- 文献覚書/scout report と配達 PDF 5 本の digest を ledger に照合。

### 実施していないこと

- 大規模 GAP 悉皆、ladder `CorrectedShadowsXi` の独立再実装。
- GitHub Actions の再発火、CI artifact の取得、DRAT/LRAT 本体の再検査。
- 文献 PDF 5 本の全ページ精読。
- Lean 証明。
- 便面 §9 の残務実装・文書修正。

従って機械計算の格付けは本文で明記した
`GAP single-system` / `generation-pair cross-checked` /
`DRAT receipt` の範囲を越えない。
