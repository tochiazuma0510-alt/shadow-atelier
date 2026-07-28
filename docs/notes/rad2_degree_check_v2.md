# 命題 RAD-deg — 予想 RAD-2 の次数恒等式の検証(v2)

**版歴**
| 版 | 日付 | 変更 |
|---|---|---|
| v1 | 2026-07-28 | 初版(`rad2_degree_check_v1.md`・sha256 `98d26e38…8b9ce3`)。**上書きせず保存** |
| **v2** | 2026-07-28 | **Sol 便 76 F1.2 の指摘 1 件のみを修理**: §2.1 補題 1 の証明で、因子 $g$ の**定数項** $c$ を「根の積」と同一視して $c^p=a^k$ と書いていた箇所の**符号 $(-1)^k$ の落ち**($p$ 奇では $c^p=(-1)^{kp}a^k$ で符号が残る)。根の積 $b:=(-1)^kc\in F$ を取る形に修正($g,h$ のモニック性も明示)。**Bézout 以降の議論・補題 1 の主張・補題 2/3・定理 RAD-deg・命題 RAD-grp・FINDING は一切不変。** 差分は当該箇所と本版歴のみ |

**状態札: candidate(裁定前・未 commit)**
起草: Claude 第二インスタンス(数学者・独立監査役)/ 2026-07-28
設問: 裁定 112 / 発案 **I-11「予想 RAD-2」**(`ideas/ideas_003_scalefree.md`)の**数学核のみ**
正典: `docs/week1-定義ノート.md` §3(Thm 4.6 の位数式)・台帳 `provenance/CLAIMS.md` W3-8 / W3-11
外部文献: **不使用**(全て学部代数の範囲で自己完結。【文献要請】なし)

**検証したもの / していないもの**

| 対象 | 判定 |
|---|---|
| **次数恒等式** $[\mathbf Q(\zeta_{4n},2^{1/n}):\mathbf Q]=2n\varphi(n)$(全奇数 $n\ge3$) | **成立(完全証明・§3)** |
| その核 = $x^n-2$ の $\mathbf Q(\zeta_{4n})$ 上の既約性 | **成立(補題 1–3・独立 2 経路)** |
| 「abelian-Capelli 基盤補題」の一般化可否 | **可(補題 2)。ただし $p=2$ で偽 — 反例つき(§2.2)** |
| Capelli の例外枝 $-4F^4$ | **二重に空虚(§4)** |
| **強化: $\operatorname{Gal}(L_n/\mathbf Q)\cong\operatorname{GT}(K^{(n)})$**(位数一致より強い) | **成立(命題 RAD-grp・§3.3)** |
| 既知 2 点との照合 | **$L_3$ は完全一致。$L_{A_5}$ は RAD-2 の式の instance では *ない*(F2)** |
| **予想 RAD-2 本体**($L_n$ が飽和の固定体か) | **検証対象外**(§5 に論理関係のみ記載) |

---

## 1. 結論

> **定理 RAD-deg.** $n\ge3$ を奇数とする。$\zeta_{4n}$ を原始 $4n$ 乗根、$2^{1/n}$ を実正 $n$ 乗根とすると
> $$\boxed{\;[\mathbf Q(\zeta_{4n},\,2^{1/n}):\mathbf Q]\;=\;2n\varphi(n)\;}$$
> であり、これは正典 Thm 4.6 の奇数側位数 $|\operatorname{GT}(K^{(n)})|=2n_0\varphi(n_0)\big|_{n_0=n}$ と一致する。**反例は存在しない。**

さらに(発案が主張していない強化):

> **命題 RAD-grp.** 同じ仮定の下で $L_n:=\mathbf Q(\zeta_{4n},2^{1/n})$ は $\mathbf Q$ 上 Galois で
> $$\operatorname{Gal}(L_n/\mathbf Q)\;\cong\;\operatorname{Aff}(\mathbf Z/n)\times C_2\;\cong\;\operatorname{GT}(K^{(n)})\qquad(\text{正典 Thm 4.6},\ \alpha=0).$$
> すなわち一致は**位数だけでなく群としての同型**である。

---

## 2. 補題

### 2.1 補題 1(素数指数の既約性)— 自己完結

> **補題 1.** $F$ を体、$p$ を素数、$a\in F^\times$、$\operatorname{char}F\ne p$ とする。
> $$x^p-a\ \text{が}\ F\ \text{上既約}\iff a\notin F^p .$$

**証明.** ($\Rightarrow$)対偶: $a=b^p$ なら $x-b$ が因子。
($\Leftarrow$)対偶: $x^p-a=g\cdot h$、$g,h$ はモニック、$1\le k:=\deg g<p$ とする。分解体で $x^p-a=\prod_{j}(x-\zeta^j\alpha)$($\alpha^p=a$、$\zeta$ は原始 $p$ 乗根)。$g$ の定数項を $c\in F$ とすると、**$g$ の根($=$ 選んだ $k$ 個の根)の積**は
$$b:=(-1)^{k}c\;=\;\zeta^{s}\alpha^{k}\in F\qquad(\text{ある }s)$$
である($c=(-1)^k\prod(\text{根})$ ゆえ。**定数項そのものを取ると符号 $(-1)^{k}$ を落とす** — 定数項 $c$ では $c^p=(-1)^{kp}a^k$ となり、$p$ 奇では符号が残る)。すると $\zeta^p=1$ より
$$b^p=\zeta^{sp}\alpha^{kp}=a^{k}.$$
$\gcd(k,p)=1$ ゆえ $uk+vp=1$ なる $u,v\in\mathbf Z$ を取れば
$$a=a^{uk+vp}=(a^{k})^{u}(a^{v})^{p}=(b^{p})^{u}(a^v)^p=\bigl(b^{u}a^{v}\bigr)^{p}\in F^p. \qquad\blacksquare$$

> **註**: 素数指数では Capelli の $-4$ 例外枝は現れない。例外枝は $4\mid n$ のときだけの現象である(§4)。

### 2.2 補題 2(abelian-Capelli 基盤補題)— 発案が命名を求めた補題

> **補題 2.** $F/\mathbf Q$ を**アーベル拡大**(より弱く「$F$ の全ての部分体が $\mathbf Q$ 上正規」でよい)、$p$ を**奇**素数、$a\in\mathbf Q^\times$ で $a\notin\mathbf Q^p$ とする。このとき
> $$a\notin F^p .$$

**証明.** $a=\beta^p$、$\beta\in F$ と仮定する。補題 1 より $x^p-a$ は $\mathbf Q$ 上既約、$\beta$ はその根だから $[\mathbf Q(\beta):\mathbf Q]=p$。$F/\mathbf Q$ はアーベルゆえ $\operatorname{Gal}(F/\mathbf Q)$ の全ての部分群は正規、したがって**中間体 $\mathbf Q(\beta)$ は $\mathbf Q$ 上正規**。正規性より $\mathbf Q(\beta)$ は $x^p-a$ の全ての根 $\zeta_p^{j}\beta$ を含む($p\ge3$ ゆえ根は 2 個以上)。二根の比から $\zeta_p\in\mathbf Q(\beta)$、すなわち $\mathbf Q(\zeta_p)\subseteq\mathbf Q(\beta)$、よって
$$(p-1)\mid p .$$
$p\ge3$ で $p-1\ge2$、$\gcd(p-1,p)=1$ だから矛盾。$\blacksquare$

> **⚠ 射程(重要)**
> * **$p=2$ で偽**。反例: $F=\mathbf Q(\sqrt2)$(アーベル)、$a=2\notin\mathbf Q^2$ だが $2=(\sqrt2)^2\in F^2$。**「全奇素数」という限定は装飾ではなく必須**である。
> * $a\in\mathbf Q$ の仮定も必須(一般の $a\in F$ には言えない)。
> * したがって発案の「全奇数 $p$・全 abelian 体・radical 冪一般」への昇格は**可能**だが、**$p=2$ を含めた形に一般化してはならない**。$L_4=\mathbf Q(\zeta_8)$ が $\sqrt2$ を含む(§6.3)のはまさにこの反例の実現である。

### 2.3 補題 2′(分岐による独立経路)— 第二系統

同じ結論を、アーベル性を使わない valuation 論法でも得る。工房の規律に照らして**独立 2 経路**を持たせる価値があるので併記する。

> **補題 2′.** $K/\mathbf Q$ を有限次拡大、$q$ を有理素数、$e_q$ を $K$ における $q$ 上の(いずれかの素点の)分岐指数とする。$a\in\mathbf Q^\times$、$p$ を素数とし、$p\nmid e_q\cdot v_q(a)$ とする。このとき $a\notin K^p$。

**証明.** $\mathfrak q$ を $q$ 上の素点、$w$ をその正規化付値($w(\pi)=1$)とすると $w(a)=e_q\,v_q(a)$。$a=\beta^p$ なら $w(a)=p\,w(\beta)$ ゆえ $p\mid e_qv_q(a)$、矛盾。$\blacksquare$

**本件への適用**: $K=\mathbf Q(\zeta_{4n})$、$n$ 奇。$4n$ の $2$-部分はちょうど $4$ だから $2$ の分岐指数は $e_2=\varphi(4)=2$。$a=2$、$v_2(2)=1$ ゆえ $e_2v_2(a)=2$。$p$ が奇素数なら $p\nmid2$、よって **$2\notin K^p$** $\blacksquare$

> **補題 2 と 2′ の比較**: 補題 2 はアーベル性(=非正規性の矛盾)を使い、補題 2′ は分岐指数だけを使う。**2′ は非アーベル基礎体でも効く**ので、将来 $L_n$ の外側(非アーベル塔)へ出るときはこちらが生き残る。$p=2$ での破れも 2′ なら見える($e_2=2$ が $p=2$ で割れる = まさに $\sqrt2\in\mathbf Q(\zeta_8)$)。

### 2.4 補題 3(Kummer 判定・$\mu_n\subseteq K$ の場合)— 自己完結

> **補題 3.** $K$ を体、$n\ge1$、$\operatorname{char}K\nmid n$、$\mu_n\subseteq K$、$a\in K^\times$、$\alpha$ を $x^n-a$ の一根とする。このとき
> $$[K(\alpha):K]=n\iff a\notin K^{p}\ \text{for every prime}\ p\mid n .$$

**証明.** $\mu_n\subseteq K$ ゆえ $x^n-a$ の全根 $\zeta\alpha$($\zeta\in\mu_n$)は $K(\alpha)$ に属し、$K(\alpha)/K$ は Galois。$\sigma\mapsto\sigma(\alpha)/\alpha$ は $\operatorname{Gal}(K(\alpha)/K)\hookrightarrow\mu_n$ の単射準同型で、像を $\mu_d$($d\mid n$)とすると $[K(\alpha):K]=d$。
$\sigma$ を生成元、$\sigma(\alpha)=\zeta_d\alpha$ とすると $\sigma(\alpha^{d})=\zeta_d^{d}\alpha^d=\alpha^d$ ゆえ $\alpha^{d}\in K$。$m:=n/d$ と置けば
$$a=\alpha^{n}=(\alpha^{d})^{m}\in K^{m}.$$
$d<n$ すなわち $m>1$ なら素数 $p\mid m$($p\mid n$)が存在し $a\in K^m\subseteq K^p$。
逆に $a=b^{p}$($p\mid n$)なら $(\alpha^{n/p})^{p}=b^{p}$ より $\alpha^{n/p}=\zeta b$($\zeta\in\mu_p\subseteq K$)、よって $\alpha^{n/p}\in K$ で $d\mid n/p<n$。$\blacksquare$

> **註**: $\mu_n\subseteq K$ を仮定したので Vahlen–Capelli の一般形は不要。本件は $K=\mathbf Q(\zeta_{4n})\supseteq\mu_{4n}\supseteq\mu_n$ なので条件を満たす。

---

## 3. 定理 RAD-deg とその強化

### 3.1 円分部

$n$ が奇数なら $\gcd(4,n)=1$ ゆえ
$$[\mathbf Q(\zeta_{4n}):\mathbf Q]=\varphi(4n)=\varphi(4)\varphi(n)=2\varphi(n). \tag{3.1}$$

### 3.2 radical 部

$K:=\mathbf Q(\zeta_{4n})$ と置く。$\mu_n\subseteq K$。$n$ の任意の素因子 $p$ は**奇素数**であり、$2\notin\mathbf Q^p$(有理数の一意分解)だから補題 2(または補題 2′)より $2\notin K^{p}$。補題 3 より
$$[K(2^{1/n}):K]=n. \tag{3.2}$$
(同値に: **$x^n-2$ は $\mathbf Q(\zeta_{4n})$ 上既約**。合成数 $n$ でも $p\mid n$ を走らせるだけで一様に従う — 合成数の特別扱いは不要。)

(3.1)(3.2) の乗法性より $[L_n:\mathbf Q]=n\cdot2\varphi(n)=2n\varphi(n)$。$\blacksquare$

**正典との照合**: Thm 4.6($n=2^\alpha n_0$、$\alpha\le1$)は $|\operatorname{GT}(K^{(n)})|=2n_0\varphi(n_0)$。奇数 $n$ は $\alpha=0,n_0=n$ ゆえ $2n\varphi(n)$。**一致** $\blacksquare$

### 3.3 命題 RAD-grp(位数一致より強い整合)

$L_n$ は $x^n-2$ の分解体と $\mathbf Q(\zeta_{4n})$ の合成なので $\mathbf Q$ 上 Galois。$\sigma\in\operatorname{Gal}(L_n/\mathbf Q)$ は
$$\sigma(\zeta_{4n})=\zeta_{4n}^{t}\ (t\in(\mathbf Z/4n)^\times),\qquad \sigma(2^{1/n})=\zeta_n^{s}\,2^{1/n}\ (s\in\mathbf Z/n)$$
で定まり、§3.1–3.2 の次数計算より $(s,t)$ の**全**組が実現する($n\cdot\varphi(4n)=2n\varphi(n)$ 個)。合成則は $\zeta_n=\zeta_{4n}^4$ に注意して
$$(s,t)\cdot(s',t')=(s+t\,s'\bmod n,\ tt'\bmod 4n),$$
すなわち $\operatorname{Gal}(L_n/\mathbf Q)\cong(\mathbf Z/n)\rtimes(\mathbf Z/4n)^\times$($(\mathbf Z/4n)^\times$ は mod $n$ 還元を通して作用)。$n$ 奇ゆえ CRT で
$$(\mathbf Z/4n)^\times\cong(\mathbf Z/4)^\times\times(\mathbf Z/n)^\times\cong C_2\times(\mathbf Z/n)^\times,$$
第一因子 $C_2=\ker\bigl((\mathbf Z/4n)^\times\to(\mathbf Z/n)^\times\bigr)$ は $\mathbf Z/n$ に**自明に作用**する。明示的には
$$(s,t)\ \longmapsto\ \bigl(\,(s,\;t\bmod n),\ t\bmod4\,\bigr)\ \in\ \operatorname{Aff}(\mathbf Z/n)\times(\mathbf Z/4)^\times$$
が準同型($(s+ts',tt')\mapsto((s+(t\bmod n)s',\,tt'\bmod n),\,tt'\bmod4)$ が像の積と一致)かつ CRT より全単射。よって
$$\boxed{\ \operatorname{Gal}(L_n/\mathbf Q)\cong\bigl((\mathbf Z/n)\rtimes(\mathbf Z/n)^\times\bigr)\times C_2=\operatorname{Aff}(\mathbf Z/n)\times C_2\ }$$
(この明示写像の準同型性・全単射性・$|\ker|=2$ は $n=3,5,7,9,11,13,15,21,25,27,33,45$ で機械検算済み — 単系統・紙上証明の確認)
これは正典 Thm 4.6($\alpha=0$)の $\operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$、$|\mathcal Z_2|=2$ と**群として同型**。$\blacksquare$

$n=3$: $\operatorname{Aff}(\mathbf Z/3)\times C_2=S_3\times C_2$ — 台帳 W3-11 の $\operatorname{GT}(K^{(3)})\cong S_3\times C_2$ と**逐語一致**。

---

## 4. Capelli の例外枝について(設問で名指しされた注意点)

一般の Vahlen–Capelli は「$x^n-a$ が $F$ 上既約 $\iff$ ($\forall p\mid n$)$a\notin F^p$ **かつ**($4\mid n$ なら $a\notin-4F^4$)」である。本件で例外枝は**二重に空虚**:

1. **$n$ が奇数だから $4\nmid n$** — 枝の前件が成立しない。
2. 仮に $4\mid n$ の状況を考えても、$\zeta_4=i\in K=\mathbf Q(\zeta_{4n})$ であり
   $$-4=\bigl((1+i)\bigr)^{4}\qquad\bigl((1+i)^2=2i,\ (2i)^2=-4\bigr)$$
   ゆえ $-4\in K^4$、したがって $-4K^4=K^4$ となり例外枝は主条件 $a\notin K^{2}$ に吸収される。

> 発案本文の「$2\in4\cdot\mathbf Q(\zeta_{4n})^4$ の例外枝」は符号が落ちている(正しくは $-4F^4$)。いずれにせよ本件では発火しない。**$\mu_4\subseteq K$ が枝を潰す**というのが最も筋の良い理由づけで、これは $\zeta_{4n}$ の $4$ をわざわざ付けている RAD-2 の形と整合する。

---

## 5. 予想本体との論理関係(設問 3)

台帳の飽和判定式(命題 U′-1、対話帳 T-8)は「飽和 $\iff[K_N:\mathbf Q]=|\operatorname{GT}(N)|$」である。したがって:

$$\text{RAD-2}\ (\,L_n\ \text{が}\ K^{(n)}\ \text{飽和の固定体}\,)\ \wedge\ \text{飽和}\quad\Longrightarrow\quad[L_n:\mathbf Q]=|\operatorname{GT}(K^{(n)})| .$$

* 本稿が示したのは**この必要条件が全奇数 $n$ で成立する**ことである。**予想の証拠ではなく、予想が矛盾で即死しないことの確認**にすぎない。次数恒等式は「$L_n$ が候補たりうる」以上を何も言わない(同じ位数・同じ群型の体は他にもいくらでもある)。
* 逆向きは強い: **次数恒等式が落ちれば RAD-2 は予言ごと死ぬ**(帰結 1・2・3 のいずれも $L_n$ が固定体であることに乗っている)。**その死に方は起こらない**ことが確定した。
* 命題 RAD-grp(群同型)は必要条件を一段強めたもので、これも通過した。ただし**「群として同型」と「$\operatorname{Ih}$ が誘導する同型である」は別物**であり、後者こそが飽和の内容である。抽象同型は $\operatorname{Ih}$ の像について何も言わない。
* $u_n$・封印量には本稿は一切触れていない。**次数恒等式は $u_n$ の値と独立**(radical が $2$ であるという仮定を置いたときの体論だけ)であり、発案が「破綻しそうな点」に挙げた「$u_n$ の素因子支持が太る」筋は本稿の射程外で**依然生きている**。

---

## 6. 既知 2 点との照合(設問 2)

### 6.1 $L_3$(W3-11)— **完全一致**

$$L_3=\mathbf Q(\zeta_{12},\sqrt[3]2)=\mathbf Q(\zeta_{4\cdot3},2^{1/3}),\qquad [L_3:\mathbf Q]=\varphi(12)\cdot3=4\cdot3=12=2\cdot3\cdot\varphi(3).$$
$\operatorname{Gal}\cong S_3\times C_2\cong\operatorname{GT}(K^{(3)})$(§3.3)。**RAD-2 の式の instance であり、群レベルまで一致する。**

### 6.2 $L_{A_5}$(W3-8)— **RAD-2 の式の instance ではない(F2)**

台帳 W3-8: $L=\mathbf Q(\zeta_5,\sqrt[5]2)$、$\operatorname{GT}(N_A)\cong F_{20}$。
$$[\mathbf Q(\zeta_5,2^{1/5}):\mathbf Q]=\varphi(5)\cdot5=4\cdot5=\boxed{20}=n\varphi(n)\big|_{n=5},$$
($x^5-2$ の $\mathbf Q(\zeta_5)$ 上の既約性は補題 2+補題 3 で同様に従う。$\operatorname{Gal}\cong\operatorname{Aff}(\mathbf Z/5)=F_{20}$ ✓)
一方 **RAD-2 の式の $n=5$ 値**は
$$L_5^{\rm RAD}=\mathbf Q(\zeta_{20},2^{1/5}),\qquad[L_5^{\rm RAD}:\mathbf Q]=2\cdot5\cdot\varphi(5)=\boxed{40}\ (=|\operatorname{GT}(K^{(5)})|).$$

> **FINDING F2**: 発案 I-11 帰結 1 は「$[\mathbf Q(\zeta_{4n},2^{1/n}):\mathbf Q]=2\varphi(n)n=|\operatorname{GT}(K^{(n)})|$。**K³: 12=12 ✓・A₅: 20=20 ✓**」と書き、二例で確認したと述べる。しかし **$A_5$ 側の体には $\zeta_4$ 因子がなく、$20=n\varphi(n)$ であって $2n\varphi(n)=40$ ではない**。$A_5$ が確認しているのは
> $$[\mathbf Q(\zeta_n,2^{1/n}):\mathbf Q]=n\varphi(n)=|\operatorname{GT}(N_A)|$$
> という**別の(相似形の)恒等式**である。両者はどちらも真だが**同じ式ではない**。
> **帰結**: RAD-2 の式そのものを確認する既知データ点は **$n=3$ の一点のみ**。「二例+2 冪一例」という帰納の基盤は、正確には「**一例 + 相似形の一例 + 2 冪の一例**」であり、発案が自認する「帰納の根拠として薄い」はさらに一段薄い。**この差は $C_2$ 因子 = $\zeta_4$ の有無**という構造的なもので(§3.3 の $C_2$ は $(\mathbf Z/4)^\times$ そのもの)、$A_5$ 窓に $\mathcal Z_2$ が無いこととちょうど対応している — 「同形の観察」として記録するのが正しい位置づけで、**instance と数えてはならない**。

### 6.3 $L_4=\mathbf Q(\zeta_8)$(便 75)— 「radical 自明」は正しくない

発案は「$L_4=\mathbf Q(\zeta_8)=\mathbf Q(\zeta_8,2^{1/1})$(radical 自明)」と書くが、**$\sqrt2=\zeta_8+\zeta_8^{-1}\in\mathbf Q(\zeta_8)$** である。したがって同じ体は
$$L_4=\mathbf Q(\zeta_8,2^{1/2})=\mathbf Q(\zeta_{4\cdot2},2^{1/2})$$
とも書け、$2n\varphi(n)\big|_{n=2}=4=[\mathbf Q(\zeta_8):\mathbf Q]$ で**数値も合ってしまう**。

> **FINDING F3(偶然の一致・警告)**: $n=2$ での数値一致は**二つの誤差の相殺**である。
> * $[\mathbf Q(\zeta_{4n}):\mathbf Q]=\varphi(8)=4$ だが $2\varphi(n)=2\varphi(2)=2$ — (3.1) は $\gcd(4,n)=1$ を要するので**破れている**(2 倍過小)。
> * $[K(2^{1/n}):K]=[\mathbf Q(\zeta_8)(\sqrt2):\mathbf Q(\zeta_8)]=1$ だが (3.2) の主張は $n=2$ — **破れている**(2 倍過大)。
>
> 積では相殺して $4=4$。**「$n=2$ でも成り立つように見えるから族は自然だ」という読みは誤り**で、$n$ 奇の仮定は §3 の両ステップに本質的である($p=2$ での補題 2 の反例 §2.2 がその根)。$2$ 冪側は RAD-2 の族に**属さない**ものとして扱うべきである。

---

## 7. FINDING 一覧

| # | 種別 | 内容 |
|---|---|---|
| **F1** | **成立(主結果)** | 次数恒等式は**全奇数 $n\ge3$ で成立**。反例なし。核である $x^n-2$ の $\mathbf Q(\zeta_{4n})$ 上の既約性は補題 1–3 で完全証明(独立 2 経路)。合成数 $n$ の特別扱いは不要($p\mid n$ を走らせるだけ)。Capelli 例外枝は二重に空虚(§4)。**外部文献不要**という発案の見立ては正しい |
| **F2** | **誤り(発案本文)** | 帰結 1 の「A₅: 20=20 ✓」は **RAD-2 の式の確認ではない**。$L_{A_5}=\mathbf Q(\zeta_5,\sqrt[5]2)$ には $\zeta_4$ がなく $20=n\varphi(n)$、RAD-2 の $n=5$ 値は $\mathbf Q(\zeta_{20},\sqrt[5]2)$ の $40$。**RAD-2 の式そのものの既知確認点は $n=3$ の一点のみ**。差は $C_2=(\mathbf Z/4)^\times$ 因子で、$A_5$ 窓に $\mathcal Z_2$ が無いことと対応 — 「同形の観察」に格下げすべき |
| **F3** | 注意(偶然) | $L_4=\mathbf Q(\zeta_8)\ni\sqrt2$ なので「radical 自明」は不正確。$n=2$ で数値が合うのは (3.1)(3.2) が**両方破れて相殺**するため。$n$ 奇の仮定は装飾でなく本質 |
| **F4** | **強化(新規)** | 位数一致は**群同型**に強化できる: $\operatorname{Gal}(L_n/\mathbf Q)\cong\operatorname{Aff}(\mathbf Z/n)\times C_2\cong\operatorname{GT}(K^{(n)})$(§3.3)。$n=3$ では台帳の $S_3\times C_2$ と逐語一致。**必要条件が一段強い形で通った**(ただし抽象同型 ≠ $\operatorname{Ih}$ による同型) |
| **F5** | 射程の限定 | 補題 2 は **$p=2$ で偽**(反例 $F=\mathbf Q(\sqrt2)$, $a=2$)。発案の「全奇数 $p$」の限定は必須。$a\in\mathbf Q$ の仮定も必須。**「radical 冪一般」への昇格時にこの 2 条件を落とさないこと** |
| **F6** | 経路の提供 | 補題 2′(分岐版)はアーベル性を使わず $e_2(\mathbf Q(\zeta_{4n})/\mathbf Q)=2$ と $p$ 奇だけで同じ結論を出す。**非アーベル基礎体へ出たときはこちらが生き残る**(発案 帰結 2 が「abelian 体」に限定していた部分の緩和材料) |
| **F7** | 論理関係の明示 | 次数恒等式は**必要条件の確認**にすぎず、RAD-2 の証拠ではない。逆に落ちれば予言ごと死ぬ関係(§5)。**「$u_n$ の素因子支持が太る」という発案自認の破綻筋は本稿では一切潰れていない**(本稿は radical $=2$ を仮定した体論のみ) |

---

## 8. 未閉鎖項・付記

* 【RAD-1】本稿は**紙上証明**(paper-proof candidate)。Lean 検証はしていない。ただし内容は学部代数(Kummer 理論+分岐)なので、Mathlib の円分体・Kummer 拡大の既存整備次第では形式化コストは低い見込み(所感・未調査)。
* 【RAD-2】発案 帰結 2(「$\operatorname{ord}(a_n)=n$ が類群と無関係に従う」)・帰結 3($\mathcal E_n$ 一斉消滅)は**本稿の検証対象外**。ただし帰結 3 の群論部だけは §3.3 から 3 行で出る:$\operatorname{Gal}(L_n/\mathbf Q)^{\rm ab}\cong(\mathbf Z/n)^\times\times C_2$ ゆえ **$L_n$ の最大アーベル部分拡大は $\mathbf Q(\zeta_{4n})$** — ここで交換子群 $=\mathbf Z/n$(平行移動部)は $\{u-1:u\in(\mathbf Z/n)^\times\}$ が $\mathbf Z/n$ を生成すること($u=-1$ で $-2$、$n$ 奇ゆえ単元)による。さらに $\sqrt2\notin\mathbf Q(\zeta_{4n})$: もし含めば $i\in\mathbf Q(\zeta_{4n})$ と併せて $\mathbf Q(\zeta_8)=\mathbf Q(i,\sqrt2)\subseteq\mathbf Q(\zeta_{4n})$、円分体の包含判定($a\not\equiv2\bmod4$ で $\mathbf Q(\zeta_a)\subseteq\mathbf Q(\zeta_b)\iff a\mid b$)より $8\mid4n$、すなわち $2\mid n$ で矛盾。同様に $\sqrt{-2}\notin\mathbf Q(\zeta_{4n})$。したがって **RAD-2 と「$L_{2^\alpha}=\mathbf Q(\zeta_{2^{\alpha+1}})$」の下では $L_{2^\alpha}\cap L_{n_0}=\mathbf Q(\zeta_4)$、すなわち $\mathcal E_n=1$** が従う。**ただし前件のうち $L_{2^\alpha}=\mathbf Q(\zeta_{2^{\alpha+1}})$ は $\alpha=2$ でしか確認されていない**ので、帰結 3 全体は依然 conditional(この一行は範囲外の副産物として記録するのみ)。
* 【RAD-3】設問どおり予想 RAD-2 本体($L_n$ が飽和の固定体か)は**未検証・凍結予言のまま**。本稿は凍結の中身に触れていない($u$・封印量に一切言及なし)。
