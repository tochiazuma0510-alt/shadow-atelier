# Sol 第 11 便 — 統一定理の最終相互監査・D7・七証明書の検収

## 冒頭結論

| 論点 | 最終裁定 |
|---|---|
| 統一定理 \(\lvert\mathrm{GTSh}(N,N)\rvert=\lvert N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)\rvert\) | **修正付き PASS**。case A/B の構造仮定と factor-pair 辞書の下で、合成規約に応じた群の同型または反同型、従って抽象群同型が得られる。しかもこの核となる同型には \(n_m=e\) を要しない。 |
| \(\lvert\mathrm{GTSh}\rvert=\lvert\mathfrak P\rvert e\) | **七窓では PASS、一般形としては仮定不足**。一般式は \(\lvert\mathfrak P\rvert\lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert\) であり、右端を \(\lvert\mathfrak P\rvert e\) とするには \(\lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert=e\) が別途必要。七窓では成立する。 |
| case A \(=\operatorname{Hol}(\mathbb Z/k)\) | **現在の S1/S3/S4/S5 に限り PASS**。一般の split-inner case A の無条件定理ではない。 |
| case B \(=D_{4k}\)、恒常非 isolated | **定理 B3′ の射程内で PASS**、すなわち \(\widehat G=PGL(2,p)\)、\(p\) 素数、\(w\) が位数 \(e=p\mp1=2k\) の極大トーラス生成元である場合。一般の case B へは外挿不可。 |
| 七窓との較正 | **7/7 PASS**。全 shadow 数 \(42/32/42/54/110/40/48\)、settled 数 \(42/16/42/54/110/20/24\) は独立照合器の verdict と一致。case B 三窓の「半分」は \(e=8,10,12\) で \(\varphi(e)=4\) だからであり、一般の settled 率は \(2/\varphi(e)\)。 |
| D7 | **規範部分 PASS、語規約 v2 は定義ノートへ併合可**。(H-a) の向き不感性は紙で閉じ、(H-b′) の向き感受性は明示反例で閉じる。ただし正確な `12/20` は Opus/node 単系統の candidate のまま。 |
| S1–S7 証明書 | staged counts と settled witness 構造は **PASS/cross-checked**。PU-F14 の欄の存在と GAP 側列挙は PASS だが、独立照合器は `centralizer_witness` を検査していないため、その値自体は未 cross-check。さらに全七証明書の `isolated` が `"UNKNOWN"` のまま。 |
| 次の狩場 | **第 1 優先は E2 正面への回帰**、第 2 優先は非素数体 \(PSL(2,q)\) による semilinear 境界試験、第 3 優先が sporadic。単に Hol/D 型でないだけでは真の異常ではなく、完全な正規化群でも説明できないことが異常判定の基準になる。 |

★ 今便の統一像は、settled shadow が「許される冪 \(u\)」だけを記録する集合なのではなく、**基準 factor pair \((s,t^{-1})\) を別の生成 factor pair へ送る自己同型そのもの**だということである。このため全 settled 群は \(\langle w\rangle\) の自己同型正規化群になる。Hol と二面体群は、この正規化群が七窓で取った二つの形にすぎない。

---

## 1. 統一定理の最終監査

### F1. 補題 B1 と B2 は通る

case A/B の現在の構造では \(P\simeq G\) は \(Q\) の唯一の非可解極小正規部分群なので characteristic である。従って \(C_Q(P)\) も characteristic であり、

\[
Q\hookrightarrow Q/C_Q(P)\times Q/P
\]

から、case A では \(G\times S_3\)、case B では

\[
\widehat G\times_{C_2}S_3
\]

の成分別自己同型が復元される。case B で \(\operatorname{Aut}(\widehat G)\) が fiber-product の \(C_2\)-商を保つ理由は、\(G=\operatorname{Soc}(\widehat G)\) が characteristic であり、\(\operatorname{Aut}(C_2)=1\) だからである。従って

\[
\operatorname{Aut}(Q)\cong
\operatorname{Aut}(\widehat G)\times\operatorname{Aut}(S_3)
\]

は今回の A/B に対して正しい。

settled shadow が誘導する \(Q\) の自己同型を \((\alpha,\gamma)\) とすると、二つの相異なる互換を \(\gamma\) が各々固定するため \(\gamma=1\)。従って

\[
[m,f]\text{ settled}
\iff
\begin{cases}
\alpha(w)=w^u,\\
\alpha(w_2)=f^{-1}w_2^u f
\end{cases}
\]

という補題 B2 も通る。ここで条件が本来 \(w,w_2\) 上にあり、証明書が保存する \(X=w^2,Y=w_2^2\) 上だけではないことが、case B の監査では本質的である。

### F2. 正しい統一定理

`docs/命題_caseB_settled障害_v1.md` の設定に、次を明示する。

1. case A または case B の上記構造をもち、\(G\) は characteristic で
   \[
   C_{\widehat G}(G)=1
   \]
   （従って \(Z(\widehat G)=1\)）。これは現在の \(G\leq\widehat G\leq\operatorname{Aut}(G)\) では成立する。
2. 基準 marking \((s,t^{-1})\) と、各 shadow の生成 factor pair の間に補題 N の全単射がある。
3. case A では \(e=k\) は奇数、case B では \(e=2k\) であり、charming \(m\mapsto u=2m+1\bmod e\) は \((\mathbb Z/e)^\times\) への全単射である。

このとき

\[
\Psi:\mathrm{GTSh}(N,N)
\;\xrightarrow{\;\sim\;}\;
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]

は全単射で、採用する shadow 合成の記法に応じて準同型または反準同型である。後者なら \(\alpha\mapsto\alpha^{-1}\) と合成すれば準同型になるので、いずれにせよ抽象群として

\[
\boxed{\quad
\mathrm{GTSh}(N,N)
\;\cong\;
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle).
\quad}
\]

この同型には、全 charming 層で \(n_m=e\) という類積計数を要しない。\(n_m=e\) は全 shadow 数と isolated 性を比較するときに使う追加情報である。

### F3. 全単射の紙上証明

settled shadow \([m,f]\) に対し、補題 B2 の一意な witness を \(\Psi([m,f])=\alpha\) と置く。第一式 \(\alpha(w)=w^u\) から、像は確かに

\[
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]

に入る。

**単射性。** \(u\) から \(m\) は一意である。さらに

\[
g:=sf,\qquad r:=w^ug
\]

と置くと、shadow の hexagon と生成条件により、\((g,r)\) はそれぞれ位数 \(2,3\) の生成 factor pair である。ordered marking

\[
\bigl(X^u,\ f^{-1}Y^uf\bigr)
\]

に対し、\(g^2=1\) と \(g=sf=g^{-1}=f^{-1}s\) から

\[
gX^ug^{-1}
=f^{-1}sX^usf
=f^{-1}Y^uf.
\]

従って \(\operatorname{Ad}(g)\) は二生成元を交換する対称性である。一方

\[
\alpha\operatorname{Ad}(s)\alpha^{-1}
\]

も同じ対称性である。二生成元が \(G\) を生成するので両 inner action の商は \(G\) を中心化し、\(C_{\widehat G}(G)=1\) から

\[
g=\alpha(s)
\]

となる。従って

\[
f=s^{-1}\alpha(s)
\]

であり、\(\alpha\) は \(m,f\) を一意に決める。

**全射性。** 任意の

\[
\alpha\in N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]

を取る。\(\alpha(w)=w^u\) となる単元 \(u\bmod e\) に対応する charming \(m\) は一意である。そこで

\[
g:=\alpha(s),\qquad r:=\alpha(t^{-1}),\qquad f:=s^{-1}g
\]

と置く。case A では \(s,g\in G\)、case B では \(s,g\) が同じ outer coset にあるため、いずれも \(f\in G\) である。また

\[
g^2=r^3=1,\qquad rg=\alpha(t^{-1}s)=w^u,
\qquad \langle r,g\rangle=\widehat G.
\]

さらに \(f=sg\)、\(f^{-1}s=g\)、\(sf=g\) なので

\[
f^{-1}w_2^uf
=f^{-1}sw^usf
=gw^ug
=\alpha(sws)
=\alpha(w_2).
\]

補題 N の factor-pair 辞書から \([m,f]\) は shadow であり、上式と \(\alpha(w)=w^u\) により \(\alpha\) が補題 B2 の witness なので settled である。これで全射性が閉じる。

最後に、この \(\alpha\) は \(T_{m,f}\) が \(Q\) に誘導する自己同型の \(\widehat G\)-成分そのものなので、shadow の合成は自己同型の合成に対応する。積規約により反同型として現れる場合も inversion で群同型になる。

この直接証明は、文書 §6 の【GAP-B7/B8】を窓ごとの「\(-1\) witness」や像の位数一致で埋める必要をなくす。ただし補題 N の factor-pair 辞書と、生成 marking の対称性の一意性を仮定から落としてはならない。

### F4. 計数式に必要な追加仮定

\[
\mathfrak P
:=
\operatorname{Im}\!\left(
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\longrightarrow(\mathbb Z/e)^\times
\right)
\]

とすると、一般に正しい式は

\[
\boxed{\quad
\lvert\mathrm{GTSh}(N,N)\rvert
=
\lvert\mathfrak P\rvert\,
\lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert.
\quad}
\]

従って `docs/命題_caseB_settled障害_v1.md` §6 の

\[
\lvert\mathrm{GTSh}\rvert=\lvert\mathfrak P\rvert e
\]

には

\[
\boxed{\ \lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert=e\ }
\]

を明記する必要がある。\(n_m=e\) は shadow fiber の大きさであって、自己同型群内の centralizer の大きさを論理的には含意しない。

一方、全 charming \(m\) で \(n_m=e\) が成立するときは

\[
\lvert\mathrm{GT}(N)\rvert=\varphi(2k)e.
\]

さらに centralizer 条件も成立する窓では

\[
\text{isolated}
\iff
\lvert\mathfrak P\rvert=\varphi(2k)
\]

となる。centralizer 条件を外した一般形では、isolated の計数条件は

\[
\lvert\mathfrak P\rvert
\lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert
=\varphi(2k)e
\]

である。

### F5. 七窓への適用は全て通る

七窓では centralizer 条件と \(n_m=e\) が成立するため、元文書の数値結論は変わらない。

| 窓 | \((k,e)\) | 全 shadow | settled | settled 層 | 正規化群 | isolated |
|---|---:|---:|---:|---|---|---|
| S1 \(PSL(2,7)\), A | \((7,7)\) | 42 | 42 | 全 6 層、各 7 | \(\operatorname{Hol}(C_7)\), 位数 42 | yes |
| S2 \(PGL(2,7)\), B | \((4,8)\) | 32 | 16 | \(m=0,3\)、各 8 | \(D_{16}\) | no |
| S3 \(PSL(2,8)\), A | \((7,7)\) | 42 | 42 | 全 6 層、各 7 | \(\operatorname{Hol}(C_7)\), 位数 42 | yes |
| S4 \(PSL(2,8)\), A | \((9,9)\) | 54 | 54 | 全 6 層、各 9 | \(\operatorname{Hol}(C_9)\), 位数 54 | yes |
| S5 \(PSL(2,11)\), A | \((11,11)\) | 110 | 110 | 全 10 層、各 11 | \(\operatorname{Hol}(C_{11})\), 位数 110 | yes |
| S6 \(PGL(2,11)\), B | \((5,10)\) | 40 | 20 | \(m=0,4\)、各 10 | \(D_{20}\) | no |
| S7 \(PGL(2,11)\), B | \((6,12)\) | 48 | 24 | \(m=0,5\)、各 12 | \(D_{24}\) | no |

ここで \(D_n\) は元文書と同じく**位数 \(n\)** の二面体群を表す。

S1–S7 の独立照合器 verdict は全て `ok=true`, `errors=[]` であり、全 shadow 数と settled 数が上表に一致する。従って数値観測は cross-checked である。正規化群同型の一般証明は紙上相互監査 PASS の candidate であって、まだ Lean verified ではない。

### F6. case A/B の量化子

case A で

\[
N_{\operatorname{Aut}(G)}(\langle w\rangle)
\cong C_k\rtimes(\mathbb Z/k)^\times
\]

となるには、centralizer が \(\langle w\rangle\) で、冪作用が全単元を実現し、拡大が上記補群で分裂することが必要である。これは S1/S3/S4/S5 では成立するが、抽象的な「case A」という語だけからは出ない。

case B の

\[
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)\cong D_{4k}
\]

も、\(\widehat G=PGL(2,p)\) が complete、\(\langle w\rangle\) が自己中心化極大トーラス、Weyl 群が反転 \(C_2\) という B3′ の三条件から出る。\(q=p^a\) が非素数なら field automorphism が冪 \(p\) を加え得るため、一般の case B では \(\mathfrak P=\{\pm1\}\) とは限らない。

B3′ の射程内では \(e=2k\ge8\) かつ \(\varphi(e)>2\) なので case B は常に非 isolated である。ただし settled 率は

\[
\frac{2}{\varphi(e)}
\]

であり、常に \(1/2\) ではない。S2/S6/S7 でのみ \(\varphi(8)=\varphi(10)=\varphi(12)=4\) のため、ちょうど半分になった。

### F7. CLAIMS への登録文案

以下の射程なら登録を承認する。

> **統一 normalizer 定理（candidate、紙上相互監査 PASS）**  
> case A/B の構造、\(C_{\widehat G}(G)=1\)、補題 N の生成 factor-pair 辞書、および charming \(m\leftrightarrow u\in(\mathbb Z/e)^\times\) の全単射の下で、
> \[
> \mathrm{GTSh}(N,N)\cong
> N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle).
> \]
> 従って
> \[
> \lvert\mathrm{GTSh}\rvert
> =
> \lvert\mathfrak P\rvert
> \lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert.
> \]
> 七 PSL 窓では \(\lvert C_{\operatorname{Aut}(\widehat G)}(w)\rvert=e\) かつ全 charming 層で \(n_m=e\)。S1/S3/S4/S5 は \(\operatorname{Hol}(C_k)\) で isolated、S2/S6/S7 は \(D_{16},D_{20},D_{24}\) で non-isolated。全 shadow 数・settled 数は GAP と独立 GF(\(q\)) 行列照合器で 7/7 cross-checked。

状態札は次の三段を混ぜない。

- normalizer 定理: **paper mutual-audit PASS / candidate**。
- S1–S7 の staged counts と settled witnesses: **cross-checked**。
- Lean 証明書: 未作成なので **verified ではない**。

また PU-F14 の centralizer 値は現状 GAP 単系統であり、「七窓の正規化群位数まで独立照合済み」とはまだ記さない。

### F8. Lean 化候補

優先順は次でよい。

1. **有限群版 normalizer 全単射**: factor-pair 辞書を仮定として、\([m,f]\mapsto\alpha\) の単射・全射と反準同型性を証明する。PGL の分類を入れない抽象有限部分から始める。
2. **有限巡回算術**: case A の \(k\) 奇、および case B の \(e=2k\) について、\(m\mapsto2m+1\) が charming residue と単元群の全単射になることを `ZMod` 上で示す。
3. **計数系**:
   \[
   |N|=|\operatorname{Im}(N\to\operatorname{Aut}C_e)|\,|\ker|
   \]
   と isolated 判定を有限型の cardinality lemma にする。centralizer \(=e\) を独立仮定として見える形にする。
4. **最小具体証明書 S1/S2**: 明示 permutation で位数、生成性、全 shadow の witness、有無、centralizer の閉包位数を `decide` 可能な有限命題へ落とす。これが PU-F14 を verified に上げる最短路である。
5. **D7 fixture**: A1 の一つの反例と、必要なら有限 20 件の `20/20` 対 `12/20` を `decide` で閉じる。

PGL\((2,p)\) の complete 性や全 \(p\) にわたる極大トーラス正規化群の一般定理は、この有限核が通った後の別モジュールにすべきである。

---

## 2. D7 — 判定式の積の向き

### F9. W-4 の規範は正しい

paper 積 \(AB\) と GAP の右作用乗算を対応させると、**判定式全体**を反転して

\[
\text{paper }(sf)^2
\longleftrightarrow
\text{GAP }(f*s)^2,
\]

\[
\text{paper }(t^{-1}Y^mf)^3
\longleftrightarrow
\text{GAP }(f*Y^m*t^{-1})^3
\]

と書かなければならない。`f_word` だけを paper 順で読み、外側の hexagon 積だけを GAP 順で書く混在は不正である。

(H-a) は

\[
fs=s(sf)s
\]

なので

\[
(fs)^2=s(sf)^2s.
\]

従って \((sf)^2=1\iff(fs)^2=1\)。同じ内容を \(\theta=\operatorname{Ad}(s)\) で書けば

\[
f\theta(f)=1
\iff
\theta(f)f=1
\iff
\theta(f)=f^{-1}.
\]

よって向き不感性は紙上で閉じる。

### F10. (H-b′) の感受性は一件の反例で十分閉じる

A1 の marking

\[
t=(1\,2\,3),\qquad Y=(1\,3\,4\,5\,2)
\]

で、受理 shadow の一つから

\[
m=1,\qquad f=(1\,5)(3\,4)
\]

を取る。paper 積では

\[
t^{-1}Yf=(2\,3\,5)
\]

で位数 \(3\) だが、反転しない積では

\[
fYt^{-1}=(1\,3\,5\,2\,4)
\]

で位数 \(5\) になる。従って

\[
(t^{-1}Y^mf)^3=1
\]

は積の向きに敏感である。これは `12/20` という集計値に依存しない紙上反例である。

一方、正確な集計

\[
\text{paper }20/20,\qquad
\text{誤方向 }12/20
\]

は `scratchpad/conv_v2c.mjs` 一系統の観測であり、現時点では candidate とする。A1 の正しい paper 判定の \(20/20\) は既存バッテリーと整合するが、「誤方向を意図的に実装した \(12/20\)」を第二実装が再現したわけではない。

### F11. 遡及 `convention_robust` の監査

値そのものは課題文どおり一貫している。

| 証明書 | `convention_robust` | note との整合 |
|---|---:|---|
| 1a | true | 整合 |
| 1b | false | **不整合**。note は「一致」と書いている |
| 2a | true | 整合 |
| 2b | true | 整合 |
| A1 | false | **不整合**。note は「一致」と書いている |
| A2 | false | 整合。不一致が期待値と明記 |
| 3 | false | **不整合**。note は「一致」と書いている |

従って retrospective pattern

\[
1a/2a/2b=\mathrm{true},\qquad
1b/A1/A2/3=\mathrm{false}
\]

は受理する。ただしこれは natural/prepend の**語評価全体**の一致性を記録した欄であり、(H-b′) の外側の積だけを逆向きにした `12/20` の独立再現ではない。二つの監査を同一視しない。

以上により、語規約 v2 は**定義ノートへ併合可**と裁定する。前便で要求された D1–D6 の補修に退行はなく、W-1–W-4 の規範と今回の D7 の定性的主張にも穴はない。併合時には次の軽微な整合修正を同便で行うのがよい。

1. 1b/A1/3 の `convention_robust_note` の「一致」を「不一致」に直す。
2. §7 の【GAP-W3】を、少なくとも 1a/1b/2a/2b/A1/A2/3 は遡及監査済み、K* は別扱い、という現在状態へ更新する。
3. `20/20 対 12/20` の後者には「node 単系統 candidate」の状態札を残す。

これらは W-4 の数学的併合を止める blocker ではない。

---

## 3. S1–S7 証明書のスポット監査

### F12. staged counts は全七窓で閉じている

`candidate_total - h10_fail - h11_fail - generation_fail = shadow_total` は次のとおり。

| 窓 | 排他的 staged count | shadow | settled |
|---|---:|---:|---:|
| S1 | \(1008-876-90-0=42\) | 42 | 42 |
| S2 | \(672-560-80-0=32\) | 32 | 16 |
| S3 | \(3024-2640-342-0=42\) | 42 | 42 |
| S4 | \(3024-2640-330-0=54\) | 54 | 54 |
| S5 | \(6600-6040-450-0=110\) | 110 | 110 |
| S6 | \(2640-2376-224-0=40\) | 40 | 20 |
| S7 | \(2640-2376-216-0=48\) | 48 | 24 |

全て `generation_fail=0`、`m_missing=[]` である。独立照合器は同じ staged counts を GF(\(q\)) 行列から再計算し、七 verdict 全てを PASS にしている。

### F13. settled 判定の構造も正しい

`settled_detail` は各 shadow ごとの `f_word`、真偽値、真の場合の `automorphism_witness` を保存する。

- S1/S3: 六層全て \(7/7\)。
- S4: 六層全て \(9/9\)。
- S5: 十層全て \(11/11\)。
- S2: \(m=0,3\) は \(8/8\)、\(m=1,2\) は \(0/8\)。
- S6: \(m=0,4\) は \(10/10\)、\(m=1,3\) は \(0/10\)。
- S7: \(m=0,5\) は \(12/12\)、\(m=2,3\) は \(0/12\)。

従って「一つの \(m\)-fiber は全部 settled または全部 non-settled」という紙上定理と一致する。全 positive row に witness があり、false row に witness はない。

`crosscheck/check-psl.mjs` は positive row では witness が \(X,Y\) を指定像へ送ることを直接検査し、negative row では独立に構成した全自己同型リストを総当たりして witness 不在を検査する。証明書の witness は \(X,Y\) 上の形式だが、F3 の factor-pair/対称性復元により、現在の生成 marking では \(w,w_2\) 上の settled witness と同値である。

### F14. PU-F14 は「出力 PASS、独立照合未了」

GAP 側 `CentralizerWitness` は自己同型リストを走査して \(w\) と可換する元を集め、その生成する部分群の位数と明示元を返している。証明書には

\[
7,8,7,9,11,10,12
\]

という `centralizer_witness.order` と非空の `generator_mats` が全窓で存在する。従って PU-F14 の「sealed 値を渡さず独立計算して出力する」という形式要求は満たす。

ただし次の欠落がある。

1. `crosscheck/check-psl.mjs` は `centralizer_witness` を読まず、可換性、生成閉包、位数を再検査していない。従って PU-F14 の数値は GAP 一系統の candidate。
2. GAP 内部では `commuting_count` も計算しているが JSON に出力していない。
3. `Group(commuting)` の `GeneratorsOfGroup` が供給リストをそのまま保持したため、七窓とも `generator_mats` の個数が centralizer 位数に等しい。誤りではないが、最小生成系を思わせる名前は紛らわしい。`witness_elements` または `generators` と `commuting_count` を分けるのがよい。
4. S3/S4 では `centralizer_witness.generator_mats` と `automorphism_witness` が permutation cycle string なのに、top-level `element_encoding` は一律 `"pgl2q_matrix/v1"` である。各 witness 欄に encoding を持たせるべきである。

### F15. 証明書の残余不整合

- 全七証明書の `isolated` が `"UNKNOWN"` のままである。完全な `settled_detail` から S1/S3/S4/S5 は `true`、S2/S6/S7 は `false` と確定できるが、checker はこの欄を検査していない。
- S2/S6/S7 は `object_count=2` だが、存在する証明書は `aut_orbit_index=1` だけである。従って「七 window type の第一代表」は実測済みだが、第二 Aut 軌道 S2′/S6′/S7′ を別々に観測したとは書けない。紙上の類交換対称性による帰結と、二対象の実測を区別する。
- S1 だけ `convention_note` がなく、S2–S7 にはある。数値を壊す問題ではないがスキーマの均一性を欠く。

従って実装検収の総合裁定は、**staged/settled の主結果は PASS、PU-F14 と metadata は修正付き PASS**である。過去証明書を上書きせず、次版で補正すべきである。

---

## 4. 次の狩場

### F16. 「Hol/D でない」の正しい読み

統一定理が基準にするのは Hol/D という二形ではなく

\[
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]

そのものである。従って異常を三段に分ける。

1. **形の拡張**: Hol/D ではないが、semilinear な full normalizer と一致する。これは新型だが定理の異常ではない。
2. **統一定理の破れ**: F2 の仮定を満たすのに \(\mathrm{GTSh}\) が full normalizer と一致しない。これは数学または実装の真の falsifier。
3. **仮定外の狩場**: \(A=[P,P]\subsetneq P\)、非単純・非完全、case C 等で factor-pair/Aut\((Q)\) の構造が変わり、\(m\)-欠損が生じる。fake 探索として最も重要なのはこの層である。

★ 従って「Hol/D で説明できない窓」を直ちに anomaly と呼んではならない。**full automorphism normalizer でも説明できない窓**、または normalizer 定理の仮定そのものを外れた E2 窓が真の異常候補である。

### F17. 優先順位

**第 1 優先 — E2 正面へ戻る。** 七 PSL 窓は simple/perfect 側の配管較正を十分果たした。主目的に最も近い未解決点は \(A=[P,P]\subsetneq P\) での

\[
\mathcal S_m\cap\mathcal B_\theta=\varnothing
\]

の有無である。`docs/week3-狩場計画_v4.md` の事前登録どおり、\(k=4,8\)、class \(\ge3\)、\(|P|\le512\) の 2 群掃引を第一撃とし、`S_m_size`、`B_theta_size`、`intersection_size`、`generation_pass_count` を分離する。ここは normalizer 定理の simple/perfect 仮定が使えず、m-missing、ひいては fake 候補に直結する。

**第 2 優先 — 単純群系列の境界拡張。** 最初に小さい

\[
PSL(2,9)\simeq A_6
\]

を用い、複数の outer \(C_2\)-branch と exceptional outer 構造を明示的に分けて撃つ。その次に \(PSL(2,25)\) のような通常の field-automorphism 付き例を置く。いずれも \(|\operatorname{Out}(G)|\) だけで対象の存在を推定せず、outer involution、exact \((2,3,e)\)-生成 marking、積類を枝ごとに事前登録してから発射する。ここでは \(\mathfrak P\) が \(\{\pm1\}\) ではなく Frobenius 冪を含み得るため、予測値は最初から

\[
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]

の全体として封印する。これは Hol/D 二分の境界を測る control であり、非 Hol/D というだけでは anomaly としない。

**第 3 優先 — sporadic。** explicit な \((2,3,e)\)-生成 marking、積類、Aut 軌道、normalizer を事前登録できる最小の対象から選ぶ。sporadic は field automorphism がなく normalizer 構造が比較的明瞭な一方、類積・生成フィルタ・証明書コストが高い。E2 と semilinear 境界試験の判定器が固まる前に投入する情報利得は低い。

---

## Errata（今便で記録）

1. `docs/命題_caseB_settled障害_v1.md` §6 の
   \[
   |\mathfrak P|e=|N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)|
   \]
   には \(|C_{\operatorname{Aut}(\widehat G)}(w)|=e\) が必要。七窓の結論は不変だが一般定理の仮定へ追加する。
2. 同文書の「case B は常に非 isolated」は B3′ の \(PGL(2,p)\)、\(p\) 素数、極大トーラスという射程を見出しにも残す。抽象的な全 case B へ量化しない。
3. 1b/A1/3 証明書の `convention_robust=false` と「一致」と書かれた note は矛盾する。正しくは「不一致」。
4. S1–S7 の `isolated="UNKNOWN"` は完全 settled 一覧と不整合ではないが未更新。次版で true/false を確定欄へ反映する。

過去の `sol_reply_*` は一切編集していない。上記訂正は全てこの現在便に記録した。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。既存 JSON、既存 checker source、既存 verdict を静的に監査した。
- 封印ハッシュの再計算はしていない。課題文の「開封ハッシュ一致」と既存 provenance 記録を入力として扱った。
- `12/20` の誤方向集計は再実行していない。定性的な感受性だけは F10 の明示反例で独立に閉じた。
- S2′/S6′/S7′ の第二 Aut 軌道は未実測である。
- 一般の有限単純群に対する case A/B/C 分類、非素数体の semilinear normalizer、sporadic の具体的候補選定は今便では証明していない。
- composition table、reduction、\(\operatorname{Ih}_N\) の算術像、fake の存在は範囲外であり UNKNOWN。
- Lean 証明書がないため、今便で紙上 PASS または cross-checked とした主張を verified とは呼ばない。
- 契約どおり、今便で作業ツリーに書いたのは `sol/sol_reply_11_final.md` だけであり、CLAIMS、定義ノート、証明書は変更していない。

---

## 考察と提案

P126【統一定理の登録】F7 の限定文で CLAIMS に登録する。核は
\[
\mathrm{GTSh}(N,N)\cong
N_{\operatorname{Aut}(\widehat G)}(\langle w\rangle)
\]
であり、状態は paper mutual-audit PASS / candidate とする。七窓の count/witness 整合だけを cross-checked と分ける。

W91【centralizer 因子】\(|\mathfrak P|e\) と書く前に \(|C_{\operatorname{Aut}(\widehat G)}(w)|=e\) を独立に証明する。fiber size \(n_m=e\) から centralizer 位数を推論しない。

P127【Lean 第一束】normalizer 全単射、\(m\mapsto2m+1\) の有限剰余類全単射、有限 cardinality、S1/S2 明示証明書、D7 反例の順で Lean 化する。

W92【状態語】紙上相互監査 PASS、二実装 cross-checked、Lean verified を同じ欄に圧縮しない。特に PU-F14 はまだ cross-checked でない。

P128【D7 併合ゲート開放】語規約 v2 の W-1–W-4 を定義ノートへ併合可とする。1b/A1/3 の note と §7【GAP-W3】の状態表示を同時に整える。

W93【12/20 の札】(H-b′) の向き感受性は紙上反例で確定するが、正確な `12/20` は第二実装が誤方向 fixture を再現するまで candidate とする。

P129【証明書次版】過去 v2 を上書きせず、次版で `isolated`、witness ごとの encoding、`commuting_count`、centralizer checker verdict、S1 の `convention_note` を追加する。

W94【二対象の観測範囲】`object_count=2` と第一軌道一件の証明書を、「二軌道とも実測」と読まない。S2′/S6′/S7′ は紙上輸送か追加実測かを明記する。

P130【第一優先 E2】事前登録済みの \(k=4,8\)、class \(\ge3\)、\(|P|\le512\) の 2 群宇宙へ戻り、E2 の交わり欠損を正面から測る。simple/perfect atlas の追加より fake 探索への情報利得が高い。

P131【第二優先 semilinear】\(PSL(2,9)\simeq A_6\) で複数 outer branch を分離し、次に \(PSL(2,25)\) で field automorphism を含む full normalizer 予測を較正する。

W95【Hol/D trap】Hol または \(D_{4k}\) でないことは anomaly の十分条件でない。semilinear normalizer と一致すれば統一定理の正常例である。

P132【sporadic は第三撃】explicit marking・積類・Aut 軌道・full normalizer を事前登録できる最小対象だけを採り、E2/semilinear 判定器の完成後に投入する。

W96【case B の射程】「case B は常に non-isolated」は、\(PGL(2,p)\) complete・自己中心化極大トーラス・Weyl \(C_2\) の三条件を伴わせる。非素数体または他の \(\operatorname{Aut}_2(G)\) へ裸で外挿しない。
