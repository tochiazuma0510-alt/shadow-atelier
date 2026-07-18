# 監査結論: 条件付き PASS

定義ノートの中核、すなわち hexagon (3.3), (3.4)、charming 条件、合成 (3.53)、逆射 (3.54)、(N_{\mathrm{ord}}), (N_{F_2})、Prop. 3.6 による全射性判定は、2401.06870v2 の原文と一致する。dihedral 側の (K^{(n)})、Thm. 4.3、Thm. 4.6、およびそこから導いた位数公式も正しい。GAP における `rs = s*r` という実装規約も論文の左作用規約に合っている。

ただし、次の条件を満たすまでは sprint の「定義系 + 既知例の再現」を達成したとは宣言しない。

1. 「混合位数の最小 open は (n=12)」を、後述の正規化条件つきの表現に修正する。文字どおりの意味では (n=6) が先であり、(K^{(6)}=K^{(3)}) である。
2. 較正項目 1 の `n=3..16` を実際に完走し、Prop. 3.5 の marked factor map による検算を加える。現状のスクリプトは \(n=3,\dots,12\) と奇数 \(n=3,\dots,11\) までなので、「済」ではない。
3. Thm. 4.3 の列挙と同時に、全 shadow の source kernel が (K^{(n)}) であること、したがって isolated であることを独立に証明書化する。
4. (K^{(n)}) では常に (c=1) なので、(c\ne1) の既知・可解な有限商を較正対象に一つ加え、完全な (B_3/N) 上で (3.3), (3.4) と (T(c)=c^{2m+1}) を検証する。
5. 逆射 (3.54)、代表元不変性、reduction の関手性を明示的なゲートにする。現行 6 項目はこれらを直接試していない。

条件 1–5 を満たせば、定義ノートを v1 正本として固定し、Week 1–2 の「定義 + 既知例の再現」を達成と宣言してよい。以下、根拠と修正文案を示す。

## 1. 参照範囲

- 定義の正本: 2401.06870v2, 2024-01-29、特に §3, §3.1, §3.2, §5。
- dihedral 正本: 2405.11725v2, 2026-01-13、特に §2–§5。
- 原文照合は、リポジトリ内の UTF-8 抽出テキストと PDF 由来の式番号を基準にした。
- この実行環境には GAP executable が無かったため、`week1-kn-spotcheck.g` は source audit のみ行い、再実行はできなかった。数値公式は Thm. 4.6 から独立に再導出した。ゲート通過時には司令塔側の GAP 実行ログを証明書に含めること。
- 2405.11725v2 が「fake の例を一つも知らない」と述べるのは §1.1, p.3 の執筆時点の主張である。2026-07-18 に arXiv を完全一致語で限定検索した範囲でも後発の一次報告は見つからなかったが、これは網羅的な文献調査ではない。候補の新規性は着手直前に再確認すべきである。[2401.06870](https://arxiv.org/abs/2401.06870), [2405.11725v2](https://arxiv.org/abs/2405.11725v2)

## 2. 定義の敵対的照合

### 2.1 hexagon、charming、(N_{\mathrm{ord}})、(N_{F_2})

【提案】この部分は内容上 PASS。正本 2401 の (3.1)–(3.5) と逐語的に一致している。

正本の二式は

\[
\sigma_1^{2m+1}f^{-1}\sigma_2^{2m+1}fN
=f^{-1}\sigma_1\sigma_2x^{-m}c^mN, \tag{3.3}
\]

\[
f^{-1}\sigma_2^{2m+1}f\sigma_1^{2m+1}N
=\sigma_2\sigma_1y^{-m}c^mfN. \tag{3.4}
\]

定義ノートは、左右、σ の順序、(x^{-m},y^{-m})、(c^m)、末尾の (f) をすべて正しく写している。特に (3.4) の (f) は右辺末尾であり、(3.3) の右辺先頭の (f^{-1}) と対称な位置ではない。

また、

\[
N_{\mathrm{ord}}=\operatorname{lcm}
(\operatorname{ord}(xN),\operatorname{ord}(yN),\operatorname{ord}(cN)),
\qquad N_{F_2}=N\cap F_2
\]

も (3.1), (3.2) と一致する。charming は Def. 3.1 のとおり、

- (2m+1\in(\mathbb Z/N_{\mathrm{ord}}\mathbb Z)^\times),
- (fN_{F_2}\in[F_2/N_{F_2},F_2/N_{F_2}]),

の二条件である。後者は「その剰余類が ([F_2,F_2]) の元で代表できる」と同値である。

【軽微】定義ノートの「(T^{F_2}) の全射性で十分」は正しいが、Prop. 3.6 の強さを弱く書いている。hexagon と (2m+1) の単元条件の下では

\[
T_{m,f}\text{ 全射}
\Longleftrightarrow T^{PB_3}_{m,f}\text{ 全射}
\Longleftrightarrow T^{F_2}_{m,f}\text{ 全射}. \tag{Prop. 3.6}
\]

修正文案:

> charming GT-pair に対して、全射性は Prop. 3.6 により (T_{m,f}), (T^{PB_3}_{m,f}), (T^{F_2}_{m,f}) のいずれで判定しても同値である。有限商では
> \(\langle \bar x^{2m+1},\bar f^{-1}\bar y^{2m+1}\bar f\rangle=F_2/N_{F_2}\)
> を用いる。

【提案】簡約 hexagon に付した「(f\in[F_2,F_2]) 前提」は重要であり、現状の注記を残すべきである。根拠は 2401 Prop. 3.4, (3.10), (3.11)。有限商の derived subgroup の元を扱うときは、そこに ([F_2,F_2]) からの lift が存在すること、かつ θ,τ が商へ降りることを別途保証する必要がある。

### 2.2 合成と逆射

【提案】合成 (3.53) は PASS。

\[
[m_1,f_1]\circ[m_2,f_2]
= [2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2)], \tag{3.53}
\]

\[
E_{m,f}(x)=x^{2m+1},\qquad
E_{m,f}(y)=f^{-1}y^{2m+1}f. \tag{3.41}
\]

順序も正しい。これは先に ([m_2,f_2])、次に ([m_1,f_1]) を適用する categorical composition である。(2m+1) は (3.49) のとおり乗法的になる。

【提案】逆射 (3.54) も PASS。ただし、実装仕様には型をさらに露出させるべきである。

\[
\widetilde m=-\,(2m+1)^{-1}m\pmod {N_{\mathrm{ord}}},
\]

\[
\widetilde fK_{F_2}
=\left(T_{m,f}^{F_2,\mathrm{isom}}\right)^{-1}
(f^{-1}N_{F_2}). \tag{3.54}
\]

ここで

\[
T_{m,f}^{F_2,\mathrm{isom}}:
F_2/K_{F_2}\xrightarrow{\sim}F_2/N_{F_2}
\]

なので、\(\widetilde f\) は source \(K\) 側の剰余類である。単なる全射 \(F_2\to F_2/N_{F_2}\) の「逆」を取るのでも、target 側で \(f^{-1}\) を代入するだけでもない。正本の証明ではさらに

\[
(2m+1)(2\widetilde m+1)\equiv1\pmod{2N_{\mathrm{ord}}} \tag{3.56}
\]

を使う。偶数法で ((u^{-1}-1)/2) を機械的に計算せず、(3.54) の (-u^{-1}m) を使う方が安全である。

### 2.3 settled、isolated、reduction、genuine

【提案】この部分も定義上 PASS。

- Def. 3.13: settled は \(\ker T_{m,f}=N\)、isolated は target \(N\) の全 shadow が settled。
- Prop. 3.14: connected component の全対象の交わり (N^\diamond) は isolated。
- (3.60): (N\le H) のとき
  \(R_{N,H}([m,f])=(m+H_{\mathrm{ord}}\mathbb Z,fH_{F_2})\)。
- Cor. 5.4: ([m,f]\in GT(N)) が genuine であることと、全 (K\in\mathrm{NFI}_N(B_3)) について (R_{K,N}) の像に入ることは同値。

したがって、ある一つの有限細分 (K\le N) と一つの shadow (a\in GT(N)) について (a\notin\operatorname{Im}R_{K,N}) を完全列挙で証明すれば、fake の有限証明書になる。この向きは Cor. 5.4 の「genuine ⇒ every refinement へ survive」の対偶である。ただし「探索で lift が見つからなかった」だけでは証明書ではなく、(GT(K)) の完全列挙または像を拘束する数学的不変量が必要である。

【軽微】Conj. 5.1 を (Ih_K:G_{\mathbb Q}\to GTSh(K,K)) の全射と書けるのは、2405 Thm. 4.3 が (K\in\mathrm{Dih}) を isolated と証明し (GT(K)=GTSh(K,K)) となるためである。この依存を一言残すと、一般の target (N) への誤った一般化を防げる。

## 3. (rs) の作用慣習

### 裁定

【提案】司令塔の読みは論文の意図と一致する。論文は Lemma 4.2 で

\[
r(j)=j+1,\qquad s(j)=-j
\]

という左作用を使うため、抽象群の積 (rs) は点に (s) を先に、(r) を後に作用させる。GAP の右作用記法では (j^{pq}=(j^p)^q) なので、論文の (rs) は GAP では `s*r` である。`week1-kn-spotcheck.g` の実装は正しい。

原文内の自己検査値は 2405 (3.6):

\[
\bar z=(\bar x\bar y)^{-1}
=(r^2s,r^{-1}s,r).
\]


実際、

\[
(rs)^{-1}r^{-1}=sr^{-2}=r^2s,
\quad r^{-1}s,
\quad (rs)^{-1}s=s r^{-1}s=r.
\]

この値を fixture にすれば、作用規約の混在を即座に検出できる。Thm. 5.2 の証明中の

\[
\psi_n(xy)=(r^2s,r^{-1}s,r^{-1})
\]

も第二の fixture になる。

### 逆読みの影響

【提案】両方の `rs` を一貫して `sr` と読んでも、marked kernel 自体は変わらない。ただし座標表示は変換しなければならない。

次の (D_n^3) の自己同型を考える。

\[
\Phi=(\phi_1,\mathrm{id},\phi_3),
\]

\[
\phi_1(r)=r,\quad \phi_1(s)=r^{-2}s,
\qquad
\phi_3(r)=r^{-1},\quad \phi_3(s)=s.
\]

すると

\[
\Phi(r,s,s)=(r,s,s),
\qquad
\Phi(rs,r,rs)=(sr,r,sr).
\]

よって逆読みの写像は Φ を論文の ψₙ に後合成したものになり、kernel は等しい。したがって \(K^{(n)}\)、\(|G_n|\)、\(K^{(n)}=K^{(2n)}\)、poset 構造は不変である。ただし Thm. 4.3 の生の三座標、\(z\)、θ,τ の式を論文と比較するときは Φ で移送する必要がある。一部だけ逆に読むことは許されない。

## 4. 導出値の独立再導出

(n=2^\alpha n_0)、(n_0) は奇数とする。2405 Thm. 4.6, (4.23), (4.24) より、

\[
GT(K^{(n)})\cong
\begin{cases}
\operatorname{Aff}(\mathbb Z/n_0\mathbb Z)\times C_2,&\alpha<2,\\
\operatorname{Aff}(\mathbb Z/n_0\mathbb Z)\times\widetilde H_\alpha,&\alpha\ge2.
\end{cases}
\]

ここで

\[
|\operatorname{Aff}(\mathbb Z/n_0\mathbb Z)|=n_0\varphi(n_0).
\]

\(\alpha\ge2\) では \(\widetilde H_\alpha\) は

\[
\mathbb Z/2^{\alpha-1}\mathbb Z
\rtimes(\mathbb Z/2^{\alpha+1}\mathbb Z)^\times
\]

の指数 2 の部分群である。従って

\[
|\widetilde H_\alpha|
=\frac{2^{\alpha-1}\varphi(2^{\alpha+1})}{2}
=\frac{2^{\alpha-1}2^\alpha}{2}
=2^{2\alpha-2}.
\]

よって抽出ノートの式

\[
|GT(K^{(n)})|=
\begin{cases}
2n_0\varphi(n_0),&\alpha\in\{0,1\},\\
n_0\varphi(n_0)2^{2\alpha-2},&\alpha\ge2
\end{cases}
\]

は正しい。

2405 Thm. 5.3, (5.4) の算術的 shadow の下限は

\[
|GT_{\mathrm{arith}}(K^{(n)})|\ge
\begin{cases}
2\varphi(n_0),&\alpha\in\{0,1\},\\
2^{2\alpha-2}\varphi(n_0),&\alpha\ge2.
\end{cases}
\]

従って、どちらの範囲でも「全体の位数 / 証明された下限」は (n_0) である。(n_0=1) のとき、すなわち (n=2^\alpha,α≥2) のときだけ、この比較だけで全射が従う。

### 最小 open

【提案】「この二論文で未証明な最小の dihedral target は (K^{(3)})」は正しい。

\[
K^{(3)}=K^{(6)},\qquad
|GT(K^{(3)})|=2\cdot3\varphi(3)=12,
\]

に対し、Thm. 5.3 の保証は (2\varphi(3)=4) である。(n\ge3) の最初の target であり、2 冪の証明範囲にも入らない。

【要修正】「混合位数の最小 open は (n=12)」は、無条件には誤りまたは少なくとも曖昧である。

- 「\(n=2^\alpha n_0\) で \(\alpha\ge1\) かつ \(n_0>1\)」を mixed と呼ぶなら、最小は \(n=6\) であり \(K^{(6)}=K^{(3)}\)。
- 「dihedral 群の位数 \(2n\) が複数の素因数をもつ」を mixed と呼ぶなら、すでに \(n=3\) で位数 6 である。
- Dih の重複 \(K^{(n_0)}=K^{(2n_0)}\) を除き、代表を「\(\alpha=0\) または \(\alpha\ge2\)」に正規化し、さらに「高次 2-primary 因子と奇数 affine 因子がともに非自明」すなわち \(\alpha\ge2, n_0>1\) と定義するなら、最小代表は \(n=12\)。

修正文案:

> 最小 open target は (K^{(3)}=K^{(6)})。重複 (K^{(n_0)}=K^{(2n_0)}) を除いた正規化代表のうち、α≥2 と (n_0>1) が同時に現れる最小 open 代表は (n=12)。

## 5. 較正ゲートの裁定

### 現行 6 項目

| 項目 | 裁定 | 通過条件 |
|---|---|---|
| 1. \(K^{(n)}\) と数値 | 【要修正】未完了 | \(n=3,\dots,16\) の全範囲、奇数 \(n=13,15\) の \(K^{(n)}=K^{(2n)}\)、および Prop. 3.5 の marked factor map を検査する。現行スクリプトは \(n\le12\)。 |
| 2. GT の完全列挙 | 【重大】必要だが現文だけでは不足 | simplified hexagon からの探索と、完全な有限群 (B_3/K^{(n)}) 上の (3.3), (3.4) による検証を分離する。全候補を数え、各 source kernel も検査する。 |
| 3. 乗積表と Thm. 4.6 | 【提案】妥当 | (4.18)–(4.20)、単位、結合、さらに (3.54) で得る逆元との一致まで含める。(m) と (u=2m+1) の法を混同しない。 |
| 4. \(n=4,8,16\) | 【提案】妥当 | 位数だけでなく \(\widetilde H_\alpha\) への明示同型、\(n=8,16\) の非可換 witness の非可換積を保存する。 |
| 5. reduction | 【要修正】「具体対」だけでは弱い | Thm. 4.4 の証明分岐を覆い、lift と全射像を保存する。下記の 5 対が小さい branch suite になる。 |
| 6. LS witness | 【提案】妥当 | (n=3) と (n=12) で全許容 (m,k) を回し、特に (m\equiv2,3\pmod6) を (5.1) の両式で確認する。 |

reduction の branch suite として、

\[
(q,n)=(8,4),(36,12),(12,4),(18,3),(9,3)
\]

を勧める。順に、(p=2)、奇素数 (p\mid n)、奇素数 (p\nmid n)、(4\nmid q) の偶数、奇数 (q) の分岐を覆う。向きは常に (R_{K^{(q)},K^{(n)}}) である。

### 現行ゲートに不足する三つの検査

【重大】全 dihedral target で (c\in K^{(n)}) であるため、現在の 6 項目を全部通しても、(3.3), (3.4) の (c^m)、(N_{\mathrm{ord}}) の (cN) 成分、Prop. 3.5 の (T(c)=c^{2m+1}) は実質的に一度も試されない。これは Dih 外へ出た直後に顕在化する定義盲点である。

小さな control として、(C_5=\langle t\rangle) とし、

\[
\beta_5:B_3\longrightarrow S_3\times C_5,
\quad
\sigma_1\mapsto((12),t),\quad
\sigma_2\mapsto((23),t),
\]

\[
N_5:=\ker\beta_5
\]

を勧める。(S_3) 射影が ρ なので (N_5\le PB_3)。また

\[
PB_3/N_5\cong C_5,quad x,y\mapsto t^2,quad c\mapsto t^6=t,quad (N_5)_{\mathrm{ord}}=5.
\]

2405 Remark 5.5 により

\[
GT(N_5)=\{(m,1):0\le m<5,\ \gcd(2m+1,5)=1\}
\]

で、期待個数は 4。対応する (T_{m,1}) は (S_3\times C_5) 上の「(S_3) は恒等、(C_5) は (t\mapsto t^{2m+1})」という自己同型になるので source も (N_5) である。これは位数 30 の完全商だけで中心項を較正できる。

【要修正】代表元と型のゲートを加える。

- ((m,f)\sim(m+N_{\mathrm{ord}},fh)), (h\in N_{F_2}) で、hexagon、(T)、合成、reduction が同じ剰余類を与える。
- (3.54) の \(\widetilde f\) が source quotient に属し、左右の合成が単位になる。
- (L\le N\le H) で (R_{N,H}\circ R_{L,N}=R_{L,H}), すなわち (5.3) を実データで検査する。

【要修正】isolated の較正を明文化する。Thm. 4.3 の閉式との個数一致だけでは Lemma 4.2 の kernel 主張を再現していない。各 shadow について (4.11) の共役 triple、または同等の marked-quotient 証明書により \(\ker T=K^{(n)}\) を示すこと。

以上を加えれば較正ゲートは十分である。逆に、現行 6 項目を文字どおり通しただけでは、一般 GTSh エンジンへの定義ゲートとしては不足する。

## 6. 実装で踏みやすい数学的な罠

1. 【重大】(G_n=PB_3/K^{(n)}) だけでは full hexagon (3.3), (3.4) は評価できない。式には σ₁,σ₂ が出るため、ground truth verifier は (B_3/K^{(n)}) とその marked generators を持つ必要がある。(G_n) 内の (3.10), (3.11) と同じ helper を共有すると独立検証にならない。

2. 【重大】surjective \(T:B_3\to B_3/N\) なら \(|B_3:\ker T|=|B_3:N|\) は自動的に成り立つ。従って「kernel と target の指数が同じ」は settled の証明にならない。\(N\le\ker T\) を示して初めて等指数から equality が従う。dihedral では Lemma 4.2, (4.11) の \(T^{PB_3}=\delta\circ\psi_n\) が理想的な証明書である。

3. 【要修正】fp 群 (B_3) の subgroup object を直接比較しない。有限 permutation representation の marked factor map を使い、kernel inclusion は「target map が source mapを経由して factor する」ことで証明する。GAP の subgroup equality や同じ `Size` への依存は避ける。

4. 【要修正】Prop. 5.1 の `Core_B3` は無限 fp 群の一般 core 計算に投げない。(PB_3\triangleleft B_3) の指数が 6 なので、6 個の共役写像の直積像として有限 marked quotient を作る。dihedral Prop. 3.1 では対称性により 3 個へ減るが、一般の seed でこの簡約を仮定してはいけない。

5. 【重大】(PB_3\cong F_2\times\langle c\rangle) でも、一般の (N\le PB_3) は (N_{F_2}\times(N\cap\langle c\rangle)) に分裂するとは限らない。従って (PB_3/N) を常に ((F_2/N_{F_2})\times\langle cN\rangle) と実装してはいけない。(N_{F_2})、(cN)、その交わりは完全商内で別々に計算する。

6. 【要修正】charming で列挙すべきは ([F_2/N_{F_2},F_2/N_{F_2}]) であり、([B_3/N,B_3/N]) や full quotient の derived subgroupではない。dihedral の Prop. 3.6 の「三指数の parity が揃う」という表現は、Remark 3.7 により (4\mid n) のときだけ意味のある追加制約である。奇数 (n) や (n\equiv2\pmod4) に機械的に課すと真の候補を落とす。

7. 【要修正】(m) は法 (N_{\mathrm{ord}}) だが、2405 Prop. 4.5 の affine 表現では (u=2m+1) を法 (2n) で保持する。例えば (n=4) で (u) を法 4 に潰すと別の (m) を同一視し、群を半分にし得る。virtual character の法 (N_{\mathrm{ord}}) と、Thm. 4.6 の faithful parameter の法を混同しない。

8. 【要修正】Thm. 4.3 の \(k\) は法 \(|r^2|\)、すなわち奇数 \(n\) なら \(n\)、偶数 \(n\) なら \(n/2\)。\(4\mid n\) の parity 条件を課した後で canonicalize しないと重複または欠落が生じる。\(\varkappa(m)/2\) は整数代表で計算してから法 2 に落とす。

9. 【重大】逆射で使う (T^{F_2,\mathrm{isom}}) の domain は source quotient、codomain は target quotient である。非 settled shadow では両者は別 object なので、target 側の endomorphism として逆を取る実装は型違反である。合成も同様に、(f_2) を (E_{m_1,f_1}) で正しい quotient へ移す必要がある。

10. 【要修正】reduction の向きは細かい方から粗い方、(N\le H) に対し (R_{N,H})。Dih では包含条件は単なる (n\mid q) ではなく Prop. 3.5 の
    \(K^{(q)}\le K^{(n)}\iff n\mid\operatorname{lcm}(q,2)\)。奇数 (q) の raw (D_q\to D_n) 座標剰余に頼らず、marked factor map または (K^{(q)}=K^{(2q)}) を使う。

11. 【要修正】(N^\diamond) を作るには (GT(N)) の完全列挙と全 source kernel が必要である。一つの target (N) に入る全 morphism を列挙すれば、その connected component の全 object は source として現れるが、列挙が不完全なら isolated 化も偽になる。

12. 【提案】計算量の予測値は \(|PB_3:N|\) だけでは不足する。少なくとも
    \(|X_N|\cdot|[F_2/N_{F_2},F_2/N_{F_2}]|\)、full quotient \(|B_3:N|\)、kernel/factor-map の時間とメモリを記録する。fake 証明書には target shadow、source 全候補数、reduction image、欠落判定を含める。

## 7. 「Dih 外への最初の狩場」の裁定

### 結論: 目的は採用、第一撃は修正採用

【提案】価値は非常に高い。(L\le K^{(3)}) で (R_{L,K^{(3)}}) が非全射なら、欠落した shadow は 2401 Cor. 5.4 により fake である。同時に arithmetical ⇒ genuine なので Conj. 5.1 の (K^{(3)}) ケースを反証する。完全な有限証明書を伴うなら atlas の主結果になり得る。

【軽微】一方、全射が一つ続いただけで得られるのは「その有限細分に対する genuine の必要条件を通った」という弱い証拠であり、arithmetical であることの直接証拠ではない。「Conj. 5.1 の supporting evidence」と書く場合は、この限定を付すべきである。

### 現候補の危険

【重大】Prop. 5.1 は arbitrary seed を即座に小さな isolated object にする安価なアルゴリズムではない。core \(\widetilde N\) を作った後、\(\widetilde N^\diamond\) を得るために connected component、すなわち \(GT(\widetilde N)\) と source kernel の完全把握が必要で、指数が大きく跳ね得る。

【要修正】「位数最小の非-dihedral isolated (N)」の global minimality は、有限群の位数だけでなく全 generating pair、core、kernel の重複、isolated closure を尽くさないと証明できない。Week 3 の一撃としては探索目標が過大である。

【要修正】seed の有限群 \(G\) が抽象的に非 dihedral でも、得られた kernel が Dih 外とは限らない。Dih は有限群の族ではなく marked kernel の poset である。外部性は kernel の marked factor data、または \(|PB_3:N|\) のような排他的不変量で証明する。

【要修正】fake witness には source (L) の isolated 性は不要である。Cor. 5.4 は任意の (L\in\mathrm{NFI}_{K^{(3)}}(B_3)) に適用できる。最初から (N^\diamond) を作るのは、証明に不要な指数膨張を先払いしている。

### より安い第一撃

【提案】free class-2 exponent-3 quotient を先に撃つ。

(V:=F_2^3\gamma_3(F_2)) を verbal subgroup とし、(F_2/V) を 2 生成自由 class-2 exponent-3 群 (H_3) とする。これは位数 (3^3=27) の Heisenberg 群で、(V) は characteristic である。自然な射影

\[
PB_3\longrightarrow PB_3/\langle c\rangle\cong F_2
\]

における (V) の逆像を (N_0) と置く。(B_3) の共役作用は (PB_3/\langle c\rangle) に降り、(V) は characteristic なので

\[
N_0\triangleleft B_3,\qquad N_0\le PB_3,\qquad PB_3/N_0\cong H_3.
\]

\(|PB_3:N_0|=27\) はすべての \(|G_n|\) が 4 の倍数であることと両立しないため、\(N_0\notin\mathrm{Dih}\) も即座に証明できる。

次に

\[
L:=K^{(3)}\cap N_0
\]

を取り、(PB_3/L) を (G_3\times H_3) の marked subdirect product として作る。すると

\[
|PB_3:L|\le108\cdot27=2916,
\qquad |B_3:L|\le17496.
\]

さらに

\[
[G_3,G_3]\text{ の位数}=27,\qquad [H_3,H_3]\text{ の位数}=3
\]

なので

\[
|[F_2/L_{F_2},F_2/L_{F_2}]|\le81.
\]

\(L_{\mathrm{ord}}=6\) かつ \(|X_L|=4\) だから、simplified-hexagon の生の \((m,f)\) 候補は高々 \(4\cdot81=324\)。これは現提案の \(10^6\) 撤退線より二桁以上安全であり、core や isolated closure を先に計算する必要もない。

推奨手順は次のとおり。

1. (N_0) と (L=K^{(3)}\cap N_0) を marked finite quotient で構成する。
2. (GT(L)) を完全列挙し、full hexagon verifier と source kernel 証明書を通す。
3. (R_{L,K^{(3)}}) の像を求める。非全射なら fake 証明書を固定する。
4. 全射なら「一つの Dih 外 refinement を通過」と記録する。atlas 用の群構造が必要になった時点でのみ (N_0^\diamond) または (L^\diamond) を検討する。

【提案】撤退条件 \(|PB_3:L|>10^6\) は外枠として残してよいが、候補数 \(|X_L|\cdot|\text{derived subgroup}|\)、full quotient の位数、factor-map の実測時間も同時に cap とするべきである。指数だけでは derived 列挙の難しさを予測できない。

## 8. 修正文案の要約

1. Prop. 3.6:

   > charming GT-pair では (T), (T^{PB_3}), (T^{F_2}) の全射性は同値である。

2. 最小 open:

   > 最小 open target は (K^{(3)}=K^{(6)})。α≥2, (n_0>1) をともに要求する正規化代表の最小は (n=12)。

3. 較正項目 1:

   > 現在は \(n=3,\dots,12\) の spotcheck 済み。\(n=13,\dots,16\)、奇数 13,15 の doubled check、Prop. 3.5 は未完了。

4. 較正項目 2:

   > 列挙一致に加え、全 shadow の source kernel (=K^{(n)}) と full (B_3/K^{(n)}) 上の hexagon を独立検証する。

## 9. 考察と提案

戦況の読み: 定義ノートの数学的な骨格は健全である。

最も危険な転記箇所だった (3.3), (3.4), (3.53), (3.54) は原文と一致した。

位数公式も Thm. 4.6 から一行ずつ再導出でき、数値表と矛盾しない。

従って、現時点で撤退条件に触れるような定義崩壊はない。

ただし「Dih の再現」と「一般 GTSh 定義の再現」は同じではない。

Dih では (c=1) なので、中心拡大に関するバグが完全に隠れる。

この盲点を残したまま非 Dih 探索へ進むのは危険である。

また、settled は指数比較では判定できない。

全 shadow の kernel は最初から target と同指数だからである。

必要なのは kernel inclusion または marked factorization の証明書である。

次の一手 P1: 位数 30 の (N_5) control を較正ゲートへ追加する。

これにより (c^m)、(T(c))、full (B_3/N) を最小コストで検査できる。

次の一手 P2: 現行 6 項目を、source kernel・逆射・reduction triangle を含む形へ改訂する。

特に item 1 の「済」を「部分済」に戻し、\(n=13,\dots,16\) と Prop. 3.5 を埋める。

次の一手 P3: Dih 外の第一撃を (H_3) seed と (L=K^{(3)}\cap N_0) に変更する。

isolated closure は fake 判定に不要なので後回しにする。

この対象は \(|PB_3:L|\le2916\)、raw candidate \(\le324\) と事前評価できる。

非全射なら fake の有限証明書と Conj. 5.1 の反例が同時に得られる。

全射でも、Dih 外 refinement 一件の atlas データとして価値がある。

ただし、その全射を arithmetical の証拠と過大評価してはいけない。

司令塔への警告 1: GAP の `s*r` を論文の `rs` として固定し、(z) を fixture にせよ。

司令塔への警告 2: (PB_3/N) を常に (F_2/N_{F_2}\times\langle cN\rangle) と分解するな。

司令塔への警告 3: (u=2m+1) の法 (N_{\mathrm{ord}}) と法 (2n) を混同するな。

司令塔への警告 4: `Size(kernel)=Size(target-kernel)` を settled 証明に使うな。

司令塔への警告 5: non-dihedral な seed 群だけで Dih 外の kernel と判定するな。

司令塔への警告 6: fake の負判定には完全列挙の個数証明を必ず添付せよ。

P1–P3 は、次便冒頭でそれぞれ採用 / 却下 / 保留と理由を裁定してほしい。
