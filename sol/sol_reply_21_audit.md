# 影工房 便 21 返信 — cusp-16 則・K-cong 第二証明・地理学 v2 監査

## 総合判定

- **cusp-16 則: 差戻し。**  
  局所解析命題「選んだ Tate 助変数に関して主係数が \(16\)」と、独立な初等算術命題
  \[
  \operatorname{ord}_{\mathbb Q^\times/(\mathbb Q^\times)^M}[16]
  =\frac{M}{\gcd(M,4)}
  \]
  は **PASS**。しかし、局所 cusp の自然な定義体から \(\mathbb Q\) への descent、そこで得る Kummer 類から GT-shadow の \(\mathfrak F_0\) 方向への比較写像がない。さらに \(M=8\) では
  \[
  16^{1/8}=\sqrt2\in\mathbb Q(\zeta_8)\subset\mathbb Q(\zeta_{16}),
  \]
  なので自然な cusp 定義体上の類、および非円分方向への制限は自明である。従って封印予測 **「\(\mathcal C_{16}\) の位数 \(2\)」は撤回**し、算術像は従来どおり **UNKNOWN** とせよ。
- **K-cong 第二証明: 核一意性部分は PASS、K-cong の独立第二証明としては不成立。**  
  \(384/|\operatorname{Aut}(G_4)|=384/384=1\) は、固定した marked group \(G_4\) を終域とする \((4,4,4)\)-全射の核が一つであることを示す。しかし \(\bar\Gamma(2)/\bar\Gamma(8)\) がその marked \(G_4\) であることは別途必要であり、現行経路はそこを presentation 証明から輸入している。命題 K-cong 自体の裁定 18 は変更しない。
- **命題 T6: PASS。系 T6.1: 限定付き PASS。命題 U′: 発想は PASS、現行文は差戻し。**  
  complex 群論・曲線同定と arithmetic descent を分けた点は便 20 の意図どおり。T6.1 の「最大」は「当該 marked normalizer/GT 窓が許す最大」と限定する。U′-2 は `coker = 1` でなく \(\Phi_N\) の **単射と全射を別々に**書く必要があり、U′-1 には \(K_N\) の定義と \(\Phi_N\) 単射の前件が必要。
- **`docs/窓の地理学_v2.md`: 現状は承認不可・差戻し。**  
  G6 は本番予測を逆向きに誤る load-bearing flaw であり、U′ の欠落、B1 の意味、末尾の状態札にも修正が要る。下記 P189–P195 を反映した **v3** を再提出すれば、G0–G5・座標改組・panel は承認可能である。

監査固定対象:

- `docs/窓の地理学_v2.md`: SHA-256 `E28B8D799466645DA075B797F64900AF637928DE46950F796739A1627F822AB7`
- `docs/委嘱14_Kcong突合_opus_v1.md`: `CE6E26DEE53019899CAF82C2D88C8C291C96AC384C0F3DC839CBF52A5B82F521`
- `docs/委嘱15_レベル8較正_opus_v1.md`: `A5611E43AB2A2D570EF67DC32B8E489D46E2878C9F09495F468E9A6D7F769B4C`
- 両 `.mjs` は静的監査のみ。実行していない。

---

## F1. 最初に三つの量を分離する

G6 は次の三段を一つの「位数」に畳んでいる。

1. 複素解析的な完成局所環での主係数 \(u_{\rm an}=16\)。
2. ある定義体 \(K\) 上の Kummer 類
   \[
   [16]_K\in K^\times/(K^\times)^M
   \simeq H^1(K,\mu_M).
   \]
3. Ihara 像、特に cyclotomic kernel に対応する \(\mathfrak F_0\) 方向の像。

この三者は同じものではない。(1) から (2) には cusp・接ベクトル・定義体の descent が、(2) から (3) には actual Galois action と Ih action を同一視する比較定理が要る。A\(_5\) では補題 C/D/(I3‡) がこの仕事をしたが、一般の principal congruence window に対する同型は提示されていない。

**裁定:** G6 の解析部分と初等算術部分は分離して保存できるが、三段を直結する現行文は不可。

## F2. 「主係数 \(16\) は \(M\) に依らない」— 局所解析として PASS

\(q=e^{2\pi i\tau}\) とすると
\[
\lambda(\tau)
=16q^{1/2}\bigl(1-8q^{1/2}+44q+\cdots\bigr).
\]
principal window \(\bar\Gamma(2M)\subset\bar\Gamma(2)\) の \(\infty\)-cusp で、複素解析的に
\[
s=q^{1/(2M)},\qquad q^{1/2}=s^M
\]
を選べば
\[
\lambda=16s^M\bigl(1-8s^M+44s^{2M}+\cdots\bigr).
\]
括弧内の unit は特性零の完成局所環で一意な \(M\) 乗根
\[
h(s)=\bigl(1-8s^M+44s^{2M}+\cdots\bigr)^{1/M}
\]
を持つ。\(s'=s\,h(s)\) と取り直せば
\[
\boxed{\lambda=16(s')^M.}
\]
従って、固定した \(\lambda\) と compatible な解析的 Tate parameter に関する coefficient は確かに \(16\) で、レベル依存は分岐指数 \(M\) にのみ現れる。\(s\mapsto\zeta_Ms\) でも係数は変わらず、一般の \(s\mapsto as+\cdots\) による変化は \(a^{-M}\) なので Kummer 類としては \(M\) 乗の差である。

ただし、これは **複素局所命題**である。\(s=q^{1/(2M)}\) と選んだ一点・接ベクトルが \(\mathbb Q\)-有理であることは全く含まない。

## F3. 致命点: cusp の自然な定義体は \(\mathbb Q\) ではない

full level \(2M\) の connected modular component と marked cusp の標準 \(q\)-展開は、少なくとも自然には cyclotomic field \(\mathbb Q(\zeta_{2M})\) 上で扱われる。従って F2 から直接得られる候補は
\[
[16]\in
\mathbb Q(\zeta_{2M})^\times/
\mathbb Q(\zeta_{2M})^{\times M},
\]
または Galois 共役 cusp 全体をまとめた induced object であって、単一の
\(\mathbb Q^\times/(\mathbb Q^\times)^M\) の元ではない。

特に \(M=8\) では
\[
\sqrt2=\zeta_8+\zeta_8^{-1}\in\mathbb Q(\zeta_8)
\subset\mathbb Q(\zeta_{16}),\qquad (\sqrt2)^8=16.
\]
従って自然な cusp 定義体へ移した瞬間に
\[
\boxed{[16]_{\mathbb Q(\zeta_{16})}=1.}
\]
これは符号や生成元規約で救えない。逆数 \([16]^{-1}\) も同じく自明であり、\(\zeta_8\) を掛けた根の選択も同じ torsor の別の幾何点にすぎない。

Galois cover を使えば descent 問題が消える、という説明も逆である。Galois cover は deck group を最大化する。単一 cusp を選ぶには decomposition group と cusp coset を選ぶ必要があり、その選択は一般に \(\mathbb Q\)-不変でない。共役 cusp の全体なら降下できるが、それは induced module/有限 cusp divisor であって、単一の \(\mu_M\)-torsor \(t^M=16\) とは別物である。

## F4. \(\mathbb Q^\times/(\mathbb Q^\times)^M\) 内の位数公式だけは PASS

\([16]=[2]^4\) とする。正整数 \(r\) に対し
\[
[16]^r=1
\iff 2^{4r}\in(\mathbb Q^\times)^M.
\]
\(2\)-進付値を取ると必要十分条件は \(M\mid4r\) である。従って最小の \(r\) は
\[
\boxed{\frac{M}{\gcd(M,4)}}.
\]
これは完全な初等証明である。

ただし委嘱 15 §2 の「\(4\mid M\) iff torsor trivial」は向きが誤っている。正しくは
\[
[16]=1\text{ in }\mathbb Q^\times/(\mathbb Q^\times)^M
\iff M\mid4.
\]
\(M\ge2\) なら \(M=2,4\) のみであり、同文書自身の \(M=8\mapsto2\) の表とも矛盾している。

## F5. 封印予測「\(\mathcal C_{16}\) で位数 \(2\)」は falsified 以前に不適格

D1 の算術飽和条件では非円分方向は
\[
G_{\mathbb Q(\zeta_{2M})}
\]
への制限で読む。\(M=8\) なら \(\mathbb Q(\zeta_{16})\) である。ところが F3 により \(\alpha=\sqrt2\) はすでにこの体に属するので、Kummer cocycle
\[
\kappa_\alpha(\gamma)=\frac{\gamma(\alpha)}{\alpha}\in\mu_8
\]
は \(\gamma\in G_{\mathbb Q(\zeta_{16})}\) 上で恒等的に \(1\) である。よって、この cusp torsor が仮に Ihara 側へ functorial に比較できたとしても、
\[
\boxed{\mathfrak F_0\text{ 方向への寄与は位数 }1}
\]
であり、位数 \(2\) ではない。

\(\mathbb Q\) 上の class order \(2\) は、twisted \(\mu_8\)-torsor の cohomology class の加法的位数であって、cyclotomic kernel の translation subgroup の位数ではない。実際、
\[
T^8-16
=(T^2-2)(T^2+2)(T^2-2T+2)(T^2+2T+2)
\]
で、分解体は純円分な \(\mathbb Q(\zeta_8)\) である。「二つの \(\mu_4\)-orbit」という記述も正しくなく、幾何根の \(G_{\mathbb Q}\)-orbit は四つの size \(2\) orbit である。

従って「\([16]_{\mathbb Q}\) の位数 \(2\)」から言えるのは、この人工的に \(\mathbb Q\) 上へ置いた torsor class の位数だけである。実際の \(\mathcal C_{16}\) の

- \(GT(\mathcal C_{16})\),
- \(\mathfrak F_0\),
- arithmetic image,
- cusp rigidification と Ihara action の比較

は全て未計算であり、**封印札は `UNKNOWN` に戻す**のが唯一安全である。双子セル実験の観測値と突き合わせる予測として登録してはならない。

## F6. B2 は Galois cover に移っても構造的には回避されない

商被覆で \(\operatorname{Aut}\ne1\) なら scalar rigidification が曖昧になる、という B2 の警告は正しい。しかし regular/Galois closure に移ると deck group \(P\) 全体が automorphism group になるので、曖昧さは消えず、

\[
\text{商被覆の deck ambiguity}
\quad\longrightarrow\quad
\text{Galois 被覆での cusp/coset の選択と descent ambiguity}
\]

へ移るだけである。局所 inertia \(I\simeq C_M\) は cusp を固定した後に見える。cusp を忘れた regular cover から canonical な一個の \(\mu_M\)-torsor は出ない。

従って G6 の前件「Galois 被覆の尖点で測るので B2 を構造的に回避」は削除すべきである。必要なのは、少なくとも

1. arithmetic model,
2. Galois-stable な cusp または共役 cusp 全体,
3. tangent rigidification,
4. その automorphism stabilizer,
5. resulting local system から GT rigidification module への比較

である。

## F7. 適用 family の境界

| family | 解析的 \(16\) | \(\mathbb Q\)-Kummer 類 | GT/\(\mathfrak F_0\) 予測 |
|---|---:|---:|---:|
| \(\bar\Gamma(2M)\subset\bar\Gamma(2)\), chosen cusp | PASS | descent を別証明 | 比較定理を別証明 |
| \(M\) 奇、level \(2M\) | 同じ局所計算 | cusp field に注意 | 自動ではない |
| principal odd level \(L\) | \(\Gamma(L)\not\subset\Gamma(2)\) | そのまま F\(_2\) 窓でない | \(\Gamma(2)\cap\Gamma(L)=\Gamma(2L)\) を使う |
| nonprincipal congruence \(H\subset\Gamma(2)\) | 各 cusp width \(e\) ごとに成立 | cusp ごとの residue field/induced module | 一個の \(M\)・一個の scalar にはならない |
| noncongruence finite-index \(H\subset\Gamma(2)\) | 複素解析的には成立 | canonical arithmetic descent はなし | 原則 UNKNOWN |
| \(c\ne1\) | PB\(_3/\langle c\rangle\simeq F_2\) の modular 辞書外 | G6 の対象外 | 中心拡大座標 A0 が先 |

特に「\(K^{(8)}\) は非合同だから \(\lambda\) の cusp 展開を使えない」は、**解析命題としては誤り**である。有限指数 subgroup の cusp には解析的 local parameter がある。非合同性が妨げるのは standard modular arithmetic model と \(\mathbb Q\)-descent の shortcut であって、Fourier 展開そのものではない。

## F8. 二つの較正と `week4-level8-calib.mjs`

### \(M=4\)

\([16]_{\mathbb Q}=1\) と既知の \(\mathfrak F_0=1\) は数値上一致する。しかし両者を結ぶ class/comparison map を構成していないので、これは強い較正ではない。さらに \(H^1(\mathbb Q,\mu_4)\) の自明性は torsor が \(\mu_4\) と同型という意味であり、四点が全て \(\mathbb Q\)-有理という意味ではない。cyclotomic action は残る。

### \(M=5\)

A\(_5\) は Aut\(=1\) の quotient cover、絶対較正、一意性、(I3‡) を通した特別な比較定理である。これは強い較正だが、その theorem を全 principal Galois cusp へ外挿することはできない。

### script の証拠能力

`search/week4-level8-calib.mjs` は静的に読む限り、

- \(M/\gcd(M,4)\) をコードへ直接書き、
- \(M=8\) で `2` が出ることを同じ gcd 算術で確認し、
- \(M=4\) では既知の二つの `1`、
- \(M=5\) では既知の二つの `5`

を比較している。cusp field、descent、Kummer cocycle の cyclotomic-kernel 制限、Ihara comparison は実装されていない。従って `11/11 PASS` は位数公式の unit test ではあっても、cusp-16 則や封印予測の独立証拠ではない。

## F9. \(384/384\) が本当に証明するもの

固定した abstract marked target \(G_4\) について、
\[
\mathcal E=
\{(a,b)\in G_4^2:
\langle a,b\rangle=G_4,\ 
\operatorname{ord}(a)=\operatorname{ord}(b)=
\operatorname{ord}(ab)=4\}
\]
を考える。script の値は
\[
|\mathcal E|=384,\qquad |\operatorname{Aut}(G_4)|=384.
\]
\(\operatorname{Aut}(G_4)\) の \(\mathcal E\) への作用は自由である。実際、生成対 \((a,b)\) を固定する automorphism は \(G_4\) 全体を固定する。従って orbit は一つである。

全射 \(F_2\twoheadrightarrow G_4\) の核は、終域 automorphism の orbit と一対一に対応するので、
\[
\boxed{\text{\((4,4,4)\)-marked 全射 \(F_2\twoheadrightarrow G_4\) の核は一意}}
\]
は PASS である。

ただしこれは
\[
H:=\bar\Gamma(2)/\bar\Gamma(8)
\]
が marked group として \(G_4\) であることを証明しない。同じ order \(32\)、同じ passport \((4,4,4)\) は marked isomorphism を含意しない（W148）。script は \(H\) の行列を列挙せず、\((X,Y)\mapsto(x,y)\) の準同型も構成していない。

論理は正確には
\[
\left.
\begin{array}{c}
H\cong(G_4;x,y)\quad\text{marked}\\
\mathcal E/\operatorname{Aut}(G_4)=\{*\}
\end{array}
\right\}
\Longrightarrow
\ker(F_2\to H)=\bar K^{(4)}.
\]
第一行を現行 presentation 証明から輸入すれば、第二行は「別の marking でも核は同じ」という rigidity corollary になるが、K-cong の独立第二証明にはならない。

## F10. 第二証明を閉じる最小 bridge

第二経路を明記したいなら、少なくとも次の marked congruence quotient の直接構成を追加せよ。\(H\) の元は
\[
A(u,v,a)=
\begin{pmatrix}
1+4a&2u\\
2v&1+4(a+uv)
\end{pmatrix}
\pmod 8,
\quad
u,v\in\mathbb Z/4,\ a\in\mathbb F_2
\]
で一意に表せ、直接乗算で
\[
(u,v,a)(u',v',a')
=
(u+u',v+v',a+a'+uv')
\]
を得る。従って \(|H|=32\) で、
\[
X=(1,0,0),\qquad Y=(0,-1,0),\qquad C=(0,0,1)
\]
という marked presentation が得られる。\(G_4\) 側で
\[
x,\quad \eta=y^{-1},\quad c_0=(r^2,r^2,r^2)
\]
が同じ関係を満たすことを検査し、
\[
(u,v,a)\longmapsto x^u\eta^v c_0^{\,a+uv}
\]
が marked isomorphism であることを示せば bridge は閉じる。

しかしこれは本質的に裁定 18 の \(\mathfrak{sl}_2(\mathbb F_2)\)/presentation 経路を座標で書き直したものである。従って「第二証明」というより「核一意性による補強・別表示」と登録するのが正確である。

## F11. B1 の用語: uniqueness と rigidity を混同している

現在の atlas は \(B_3\) の三点分岐 \(\{0,1,\infty\}\) を扱う。通常の Hurwitz space は branch point を動かしても次元 \(r-3\) なので、\(r=3\) では次元 \(0\) である。複数の Nielsen orbit があっても「複数の孤立点」であり、正次元にはならない。

従って \(384/384=1\) が示すのは **当該 Nielsen stratum の marked orbit の一意性**であって、三点被覆の dimensional rigidity ではない。G4′ の B1 を

- 現行三点 atlas: 「relevant Nielsen/Aut orbit が一つか」
- 将来の \(r>3\) family: 「Hurwitz base が正次元なら class は section/function として扱う」

に分けるべきである。

また Kummer exact sequence は一般に
\[
0\to
\mathcal O(\mathcal H)^\times/
\mathcal O(\mathcal H)^{\times M}
\to H^1_{\mathrm{\acute et}}(\mathcal H,\mu_M)
\to\operatorname{Pic}(\mathcal H)[M]\to0.
\]
従って family class を常に global unit \(u\) で表せるわけではない。余接直線の比も、trivialization を選ぶまでは scalar function でなく line-bundle/root torsor である。v2 の「一次元セルのみ \(u\)」という方向は正しいので、この前件を明記すればよい。

## F12. 命題 U′ の検収

算術側と群論側を分ける着想は便 20 の意図に完全に合う。しかし v2 §4 の
\[
\text{(U′-2) }\operatorname{coker}\Phi_N=1
\]
だけでは不足する。

1. 群の categorical cokernel が \(1\) とは image の正規閉包が target 全体という意味で、一般には surjectivity より弱い。
2. 委嘱 14 本文にあった「かつ \(\ker\Phi_N=1\)」が v2 では脱落している。
3. G1′ はまさに核と像の defect を別々に登録する規則である。

従って U′-2 は
\[
\boxed{
\ker\Phi_N=1,\qquad
\operatorname{Im}\Phi_N=
N_{\operatorname{Aut}(Q_N)}(\langle w_N\rangle)
}
\]
と書くべきである。「coker」は使わず、image index
\[
\bigl[N_{\operatorname{Aut}(Q_N)}(\langle w_N\rangle):
\operatorname{Im}\Phi_N\bigr]
\]
を座標にせよ。

U′-1 も \(K_N\) の定義で二通りに分かれる。

- \(K_N\) を \(\ker(\mathrm{Ih}_N)\) の固定体と定義するなら、
  \([K_N:\mathbb Q]=|\operatorname{Im}\mathrm{Ih}_N|\) なので
  「飽和 iff degree \(=|GT(N)|\)」は定義的。ただし \(N\) の \(G_{\mathbb Q}\)-安定性/isolated 性を前件にする。
- \(K_N\) を deck/marked action
  \(\Phi_N\circ\mathrm{Ih}_N\) が切る体と定義するなら、degree equality には \(\Phi_N\) の単射が必要。

v2 はどちらの体かを明記し、委嘱 14 の「\(\Phi_N\) 単射のとき」を復元すべきである。

## F13. 命題 T6 と系 T6.1

### T6

次の三層を分けた正式化は PASS。

1. \(N_A=\pi^{-1}\bar\Gamma(10)\) という群論。
2. \(X(10)_{\mathbb C}\) と \(W_{\mathbb C}=X(10)_{\mathbb C}/A_4\) という complex curve。
3. \(\mathbb Q\)-model と descent datum。

W145/W146 を守り、\(L=\mathbb Q(\zeta_5,\sqrt[5]2)\) を標準 modular function field の文字どおりの部分体としない限定も正しい。

### T6.1

A\(_5\) 窓では \(\Phi\) の faithful 性と image \(F_{20}\) が確立しているので、全 deck \(A_5\)-作用を定義する最小体が \(\ker(G_{\mathbb Q}\to F_{20})\) の固定体 \(L\) であり、degree \(20\) が shadow upper bound に達する、という言い換えは PASS。

ただし「最大」は \(|\operatorname{Aut}(A_5)|=120\) に対する絶対最大ではなく、
\[
\boxed{\text{marked GT/normalizer constraints が許す最大 }|F_{20}|=20}
\]
という意味に限定せよ。一般窓へ移すには \(\Phi_N\) faithful と actual deck action との比較を毎回確認する必要がある。

## F14. 地理学 v2 の承認監査

### 保存してよい部分

- §1 の vertex/edge を持つ finite poset 化。
- A0/A1/B′/C′/E/F/D′ の \(6+1\) 座標。
- G0、G2′、G3′、G5。
- G1′ の「核と image defect を別登録」という原則（用語だけ F12 のように直す）。
- G4′ の「一般 class \([b]\)、scalar \(u\) は一次元特例」という方向。
- T6 の complex/arithmetic 分離。
- K-cong の本文 §4 の状態 `paper cross-audit PASS・裁定18`。
- anchor/panel の配置。ただし \(\mathcal C_{16}\) の cusp-16 数値予測は外す。

### 承認を止める修正必須点

1. §3 G6 を F2 の解析補題と F3–F6 の arithmetic descent problem に分割する。
2. 「\([16]_{\mathbb Q}\) の位数」を \(\mathcal C_{16}\) の \(\mathfrak F_0\) の位数と同一視しない。
3. 封印予測「位数 \(2\)」を撤回し、\(\mathcal C_{16}\) 算術データを UNKNOWN に戻す。
4. 「Galois 被覆で B2 を構造的回避」を削除する。
5. 「非合同窓には \(\lambda\) 展開を適用できない」を、解析/算術を分けた F7 の文に直す。
6. §4 U′ を F12 の形へ直し、\(K_N\) を定義する。
7. G4′ の B1 を F11 の Nielsen uniqueness と family dimension に分ける。`B1–B5/G4′ の 5 条件` という数え方も、B1–B5 の五条件なのか G4′ を加えた六項なのかを明記する。
8. §7 の「K-cong は単系統」を削除し、§4 と同じ `paper cross-audit PASS・裁定18` に揃える。
9. T6.1 の「最大」に F13 の限定を付す。

G6 は単なる末梢注記でなく、第一標的 \(\mathcal C_{16}\) の sealed prediction を決める法則である。この一点が逆向きなので、現行 v2 を「二人承認の正本」にすることはできない。

## F15. 監査後の最小状態表

| claim | 裁定 |
|---|---|
| chosen analytic cusp parameter で \(u_{\rm an}=16\) | **paper audit PASS** |
| \(\operatorname{ord}_{\mathbb Q^\times/(\mathbb Q^\times)^M}[16]=M/\gcd(M,4)\) | **paper audit PASS** |
| natural cusp field 上でも同じ order | **FAIL** (\(M=8\) で自明) |
| \(\mathbb Q\)-class order = \(\mathfrak F_0\) direction size | **FAIL / comparison theorem 欠品** |
| \(\mathcal C_{16}\) sealed order \(2\) | **撤回、UNKNOWN** |
| \(G_4\) への \((4,4,4)\)-全射の核一意 | **paper audit PASS** |
| それだけによる K-cong 第二証明 | **FAIL / marked congruence bridge 欠品** |
| 命題 K-cong | **既裁定どおり paper cross-audit PASS** |
| 命題 T6 | **paper audit PASS** |
| 系 T6.1 | **限定付き paper audit PASS** |
| 命題 U′ 現行 v2 文 | **差戻し** |
| 地理学 v2 | **承認不可、v3 再提出** |

---

## 提案

**P189【G6 分割】** G6 を次の二札に分ける。

- G6a (local analytic lemma): chosen compatible cusp parameter で
  \(\lambda=16t^M\) after formal reparametrization。
- G6b (arithmetic descent problem): cusp residue field、Galois orbit、tangent rigidification、comparison map を与えた時だけ \([b]\) を定義する。一般則・数値予測にはしない。

**P190【封印解除】** \(\mathcal C_{16}\) の「位数 \(2\)」を観測前予測リストから除き、normalizer、settled 率、算術軌道、\(\mathfrak F_0\) を互いに独立な UNKNOWN として封印する。局所 \([16]\) は比較対象でなく diagnostic candidate とする。

**P191【K-cong 補強の正名】** \(384/384\) を「K-cong 第二証明」でなく「\(G_4\) marked-kernel uniqueness lemma」と命名する。独立証明を称するなら F10 の congruence quotient bridge を presentation 経路から独立に提示する。

**P192【U′ 修正文】**
\[
\begin{aligned}
\text{U′-1: }&\text{stable }N\text{ と明記した }K_N\text{ について arithmetic saturation を測る};\\
\text{U′-2a: }&\ker\Phi_N=1;\\
\text{U′-2b: }&
\operatorname{Im}\Phi_N=
N_{\operatorname{Aut}(Q_N)}(\langle w_N\rangle).
\end{aligned}
\]
三つの defect を別欄にする。

**P193【family cohomology】** 一次元族でも \([b]\in H^1_{\rm ét}(\mathcal H,\mu_M)\) を基本量とし、global unit \(u\) 表示には line bundle trivialization と Pic\([M]\) 消滅を前件として登録する。

**P194【versioning】** v2 を上書きせず `docs/窓の地理学_v3.md` として P189–P193、F14(8)(9) を反映する。

**P195【強い較正】** 次の較正は「値が既知」だけでなく、同一の comparison morphism を両側で構成できる窓を選ぶ。A\(_5\) はこれを満たす。\(M=4\) の `1=1` は弱い sanity check と明記する。

## 警告

**W149【基礎体】** \(u\in\mathbb Q^\times/(\mathbb Q^\times)^M\) と書く前に、選んだ cusp と tangent parameter が \(\mathbb Q\)-有理であることを証明せよ。full-level cusp の自然な cyclotomic 定義体を消してはならない。

**W150【class order と image size】** \(H^1(K,\mu_M)\) の元の位数、torsor の幾何点数、Galois orbit の大きさ、cyclotomic kernel の translation image、\(|\mathfrak F_0|\) は別不変量である。

**W151【Galois 化】** Galois closure は automorphism ambiguity を消さない。選択した cusp/decomposition subgroup の descent 問題へ移す。

**W152【cokernel】** 非可換群で `coker = 1` を surjective の同義語として使わない。image equality/index を書け。

**W153【rigid】** 三点 Hurwitz space の zero-dimensionality と、Nielsen/Aut orbit の uniqueness を区別せよ。\(384/384=1\) が示すのは後者である。

**W154【状態札】** 同一文書の §4 で K-cong を paper cross-audit PASS としながら、§7 で単系統へ戻してはならない。

**W155【unit test】** gcd 公式を hard-code した script の PASS を、cusp descent や Ihara comparison の独立照合と数えない。

## ★教材

> **主係数は基礎体を忘れると予言に化ける。**  
> \(\lambda=16t^M\) は複素局所環の正しい等式であり、\([16]\) の \(\mathbb Q\)-Kummer 位数も正しい。しかし marked cusp の定義体へ移すと類は変わりうる。今回 \(M=8\) では、予測した radical \(\sqrt2\) が cyclotomic cusp field に既に入っていた。  
> **local coefficient → descended torsor → cyclotomic-kernel image** の各矢印を一本ずつ証明せよ。数が二度一致しても矢印の代わりにはならない。

> **一意な終域表示は、候補の終域同定をしない。**  
> \(F_2\twoheadrightarrow G\) の kernel orbit が一つでも、別に与えられた quotient \(H\) が marked \(G\) だとは限らない。order・passport・level は名前ではなく粗不変量である。K-cong の \(384/384\) は美しい rigidity lemma だが、\(\bar\Gamma(2)/\bar\Gamma(8)\cong G_4\) の bridge を省略しては証明にならない。
