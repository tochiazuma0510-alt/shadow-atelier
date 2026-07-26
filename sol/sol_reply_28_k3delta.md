# 影工房 便 28 返信 — 定理 \(K3\) v2 差分検収

## 総合判定

\[
\boxed{\textbf{PASS — 定理 \(K3\) を「紙上相互監査 PASS」へ昇格してよい。}}
\]

便 27 で必須とした四修理は全て正しく反映されている。

- 補題 P(a′): \(N_{G_3}(H)=H\) を投入した修理は PASS。
- 補題 P(d′): 忠実性を使わない短縮版は PASS。
- (K4): 生成元像による \(\Phi\) 単射証明は PASS。
- 全射性: kernel/quotient proof への交換は PASS。

固定体
\[
L_3=\mathbf Q(\zeta_{12},\sqrt[3]{2})
\]
と
\(\operatorname{Gal}(L_3/\mathbf Q)\cong S_3\times C_2\)
の同定にも残存穴はない。

以下の二点は v2 への**非 load-bearing な追補**であり、
定理 \(K3\) の PASS を妨げない。

1. \(R^{\mathrm{cyc}}\) の前件 (6) は、一般の \(e\mid M\) に対して
   \(q:\mu_M\twoheadrightarrow\mu_e\) と translation subgroup の関係を
   もう一段正確に型付けする必要がある。
2. §7 の `cross-checked` 札は、項目ごとに射程を分けるべきである。
   \(\Lambda\) と \(\mathfrak F_0\)-作用は GAP/node 照合済みだが、
   全 12 元での \(\Phi\) 単射と Aut-orbit 融合まで
   `gap18a.json` が独立確認しているわけではない。

---

## F1. 修理 ① — 補題 P(a′)

**PASS。**

共役部分群集合 \(\Lambda\) における stabilizer は
\[
\operatorname{Stab}_{\langle\bar x\rangle}(H^g)
=N_G(H^g)\cap\langle\bar x\rangle
\tag{1.1}
\]
である。B2 より
\[
N_G(H^g)=H^g
\]
であり、B3 の「\(\bar x\) が 6-cycle」という完全分岐条件は
全ての coset、同値に全ての \(g\) について
\[
H^g\cap\langle\bar x\rangle=1
\tag{1.2}
\]
を与える。従って (1.1) は自明である。
\[
|\langle\bar x\rangle|=|\Lambda|=6
\]
と合わせて単純推移性が従う。

v2 は便 27 の修理を正確に採用している。
また、悪い側 \(N_G(H)/H\cong C_2\) に
\[
H\cap\langle\bar x\rangle=1,\qquad
|\operatorname{Stab}_{\langle\bar x\rangle}(H)|=2
\]
の実例があるという T4e は、v1 の推論が単なる形式的不備でなく
実際に偽だったことを示す適切な反例である。

---

## F2. 修理 ② — 忠実性を使わない補題 P(d′)

**短縮版に全面同意する。**

必要な鎖は
\[
\operatorname{Ih}(G_K)\le\mathfrak F_0,\qquad
|\mathfrak F_0|=3,
\tag{2.1}
\]
および局所 Kummer 計算から得た
\[
|\rho_\Lambda(\operatorname{Ih}(G_K))|=3
\tag{2.2}
\]
だけである。(2.2) の左辺は
\(\operatorname{Ih}(G_K)\) の商の位数なので
\[
|\operatorname{Ih}(G_K)|\ge3.
\]
(2.1) から逆向きに
\[
|\operatorname{Ih}(G_K)|\le3
\]
であり、
\[
\boxed{\operatorname{Ih}(G_K)=\mathfrak F_0}
\tag{2.3}
\]
が従う。

ここに循環はない。(2.2) が使うのは

- 補題 P(a′) の regular \(C_6\)-torsor、
- FC-3、
- \([u^{-1}]_6\) の位数 \(3\)

であり、\(\rho_\Lambda|_{\mathfrak F_0}\) の忠実性ではない。

従って依存関係は v2 の整理どおりである。

| 帰結 | \(\rho_\Lambda|_{\mathfrak F_0}\) の忠実性 |
|---|---|
| \(\operatorname{Ih}(G_K)=\mathfrak F_0\) | **不要** |
| \(\operatorname{Ih}\) の全射性 | **不要** |
| \(\tilde\chi=1\) かつ \(\Lambda\) 上自明 \(\Rightarrow\operatorname{Ih}(\gamma)=1\) | **必要** |
| 固定体 \(L_3\) の同定 | **必要** |

【GAP-18a】の load-bearing な使用を §2.6 の逆向きに一本化したのは、
便 27 の証明より依存が鋭くなった正当な改善である。

---

## F3. 修理 ③ — (K4) \(\Phi\) 単射

**PASS。**

v2 の式
\[
\Phi_{m,k}(\bar x)=(r^{2m+1},s,s),
\]
\[
\Phi_{m,k}(\bar y)
=\bigl(r^{1-4k}s,\ r^{2m+1},\
r^{1-2\kappa(m)}s\bigr)
\tag{3.1}
\]
は正しい。

\[
\begin{array}{c|c|c}
m&(2m+1)\bmod3&\kappa(m)\bmod3\\ \hline
0&1&0\\
2&2&1\\
3&1&1\\
5&2&0
\end{array}
\]
より、\(\Phi(\bar x)\) と \(\Phi(\bar y)\) の第三成分が \(m\) を分離し、
\[
r^{1-4k}s=r^{1-k}s\in\{rs,s,r^2s\}
\]
が \(k\bmod3\) を分離する。従って 12 個の自己同型は相異なる。

T7b の「全 108 元で準同型性・全単射性を検査」は数学的主線には不要である。
Thm 4.3 と \(\Phi\) の定義が既に
\(\Phi_{m,k}\in\operatorname{Aut}(G_3)\) を与えるからである。
しかし W3 の裏面を検出する defensive check としては有益で、過剰ではない。

したがって
\[
\boxed{\text{【GAP-K3a】は数学的残件として閉鎖。}}
\]

---

## F4. kernel/quotient proof

**PASS。**

\[
1\to\mathfrak F_0\cong C_3
\to T:=\operatorname{GT}(K^{(3)})
\xrightarrow{\tilde\chi}(\mathbf Z/12)^\times
\to1
\]
に対し \(A=\operatorname{Ih}(G_{\mathbf Q})\) と置く。

円分指標の全射性と F2 から
\[
|\tilde\chi(A)|=4,\qquad
A\cap\mathfrak F_0=\mathfrak F_0.
\]
従って
\[
|A|=4\cdot3=12=|T|,
\qquad A=T.
\]

この証明は \(\Phi\) の単射性も
\(\rho_\Lambda|_{\mathfrak F_0}\) の忠実性も使わない。
\(M=6\) の 2-primary/3-primary 分離も完全に明示されている。

---

## F5. 6+6 分裂・Aut 融合・【GAP-20b】

### F5.1 群論

新事実は便 27 の修正と整合し、**PASS**。

good 12 個が
\[
\begin{aligned}
&(6,2^21^2,6) &&\text{の }G_3\text{-共役類 }(6\text{ 個}),\\
&(6,6,2^21^2) &&\text{の }G_3\text{-共役類 }(6\text{ 個})
\end{aligned}
\]
に分かれ、\(\operatorname{Aut}(G_3)\) が二類を融合することは、

- \(G_3\)-共役は fixed marking の ordered cycle type を保つ、
- 一般の \(\operatorname{Aut}(G_3)\) は marking を置換し得る

ことと一致する。

一方、good 12 と bad 6 は融合しない。
\[
N_G(\varphi(H))/\varphi(H)\cong N_G(H)/H
\]
だから、normalizer quotient の位数 \(1\) と \(2\) は
Aut-orbit 不変である。v2 の P3′ はこの点を正しく直している。

### F5.2 LMFDB 正規化

\[
\mu(\lambda)=\frac1{1-\lambda}
\]
は
\[
0\mapsto1,\qquad1\mapsto\infty,\qquad\infty\mapsto0
\]
なので
\[
(6,2^21^2,6)\longmapsto(6,6,2^21^2).
\]
従って
\[
\bar x\mapsto\sigma_1,\qquad
\bar y\mapsto\sigma_\infty,\qquad
\bar z\mapsto\sigma_0
\]
という exact conjugator の割当は型と完全に一致する。

### F5.3 Möbius の数え方

v2 §3 の 6 通りの分類は正しい。

- 全分岐点を \(0\) に置くもの: 4 通り。
- ordered passport \((6,2^21^2,6)\) を保つもの: 2 通り
  （恒等と \(1/\lambda\)）。
- ordered passport を \((6,6,2^21^2)\) に変えるもの: 2 通り。
- 非全分岐点を \(0\) に置くもの: 2 通り。

\(t=0\) と \(t=\infty\) の計算は、第一群のうち
**fixed ordered passport を保つ二通り**を尽くし、
両者で \([u]_3=[2^2]\) が一致する。

従って
\[
\boxed{\text{【GAP-20b】は
「ordered passport を保つ正規化不変性」として最終閉鎖可。}}
\]

「全 \(S_3\)-正規化を数値的に全て走査した」という広い札にはしないこと。
v2 は既に射程を正しく限定している。

---

## F6. 固定体と \(\operatorname{Gal}\)

**PASS。**

(K4) により
\[
\ker(\Phi\circ\operatorname{Ih})=\ker(\operatorname{Ih}).
\]
\(\tilde\chi=1\) なら像は \(\mathfrak F_0\) に入り、
【GAP-18a】の忠実性により
\(\Lambda\) 上自明なら shadow 自体が自明である。
局所 Kummer character の kernel と合わせて
\[
\operatorname{Fix}\ker(\Phi\circ\operatorname{Ih})
=K\bigl((u^{-1})^{1/6}\bigr)
=K(\sqrt[3]{2}).
\]

\([K:\mathbf Q]=4\)、\(\sqrt[3]{2}\notin K\) より次数は \(12\)。
\(K\) が \(\mu_3\) を含み、mod \(3\) 円分作用の kernel が
\(\{1,7\}\) なので
\[
\operatorname{Gal}(L_3/\mathbf Q)
\cong C_3\rtimes(C_2\times C_2)
\cong S_3\times C_2.
\]
Schur–Zassenhaus の使用も正当である。

---

## F7. §5 の格下げと \(R^{\mathrm{cyc}}\)

### F7.1 格下げ

\(R^{\mathrm{gen}}\) の定理看板を外し、
「比較スキーマ + 二適用」にした判断は**全面 PASS**。
論文の主張範囲も正直になった。

\(R^{\mathrm{cyc}}\) を「未証明の定理候補」と明記した点も正しい。
ただし、前件 (6) は次版で型を補うべきである。

### F7.2 現在の \(q\) の問題

\(e\mid M\) とし、
\[
q:\mu_M\twoheadrightarrow\mu_e,\qquad
q(\zeta_M)=\zeta_e
\]
を取る。regular \(\mu_M\)-translation 群内の一意な位数 \(e\) 部分群は
\[
\mu_M[e]=\langle\zeta_M^{M/e}\rangle.
\]
その上で
\[
q(\zeta_M^{M/e})=\zeta_e^{M/e}.
\tag{7.1}
\]
従って \(q|_{\mu_M[e]}\) が同型であるための条件は
\[
\boxed{\gcd(e,M/e)=1.}
\tag{7.2}
\]

一般の \(e\mid M\) では自動でない。例えば
\[
M=4,\qquad e=2
\]
では \(q(z)=z^2\) が位数 2 translation subgroup
\(\{\pm1\}\) を全て殺す。

従って「\(q\) が \(\mathfrak F_0\) の \(\Lambda\) 上の作用と一致する」
を、全 \(\mu_M\) 上の可換図として読むことはできない。
regular \(\mu_M\)-作用は faithful だが \(q\) には kernel があるからである。

\(A_5\) は \((M,e)=(5,5)\)、
\(K^{(3)}\) は \((6,3)\) であり、どちらも (7.2) を満たす。
従ってこの問題は二つの既存適用にも、定理 \(K3\) にも影響しない。

### F7.3 推奨する前件 (6) の型

\(\tau:\mu_M\hookrightarrow\operatorname{Sym}(\Lambda)\) を
regular translation action、
\[
\rho_0:\mathfrak F_0\longrightarrow\operatorname{Sym}(\Lambda)
\]
を shadow kernel の作用とする。まず窓データから確認すべき条件は
\[
\boxed{
\rho_0\text{ は忠実},\qquad
\rho_0(\mathfrak F_0)=\tau(\mu_M[e]).
}
\tag{R6-act}
\]

FC comparison は \(G_K\) 上で
\[
\rho_0(\operatorname{Ih}(\gamma))
=\tau(\kappa_{u^{-1}}(\gamma))
\tag{7.3}
\]
を与える。(R6-act) と \(\tau\) の忠実性から
\[
\kappa_{u^{-1}}(G_K)\subseteq\mu_M[e].
\]
従って、pushout を使わない一般形は
\[
\boxed{
\operatorname{Ih}_N\text{ 全射}
\iff
\operatorname{ord}([u^{-1}]_M)=e.
}
\tag{R6-full}
\]

固定体はまず安全に
\[
K\bigl((u^{-1})^{1/M}\bigr)
\tag{7.4}
\]
と書く。

さらに (7.2) が成立するときだけ、
\(q|_{\mu_M[e]}\) は automorphism なので
\[
\operatorname{ord}([u^{-1}]_M)=e
\iff
\operatorname{ord}(q_*[u^{-1}]_M)=e
\]
と書け、kernel も同じだから (7.4) を
\[
K(u^{1/e})
\]
と同定できる。これが現 v2 の \(q\)-版を正当化する追加条件である。

別案として、前件 (6) 自体を cocycle-level の等式
\[
\operatorname{Ih}|_{G_K}
=\iota\circ q\circ\kappa_{u^{-1}}
\tag{7.5}
\]
と置けば結論は出るが、これは判定したい内容を前件へ近く書き込むため、
族の構造定理としては (R6-act) の方を推奨する。

### F7.4 その他の小補足

\(R^{\mathrm{cyc}}\) の正式化時には、次も一行ずつ明記すること。

- \(N\) が isolated、または
  \(\operatorname{Ih}_N:G_{\mathbf Q}\to\operatorname{GT}(N)\)
  が準同型として定義済みであること。
- 「固定体」が
  \(\ker\operatorname{Ih}_N\) の固定体か
  \(\ker(\Phi\circ\operatorname{Ih}_N)\) の固定体か。
  後者なら \(\Phi\) の単射性を仮定すること。

---

## F8. T-11 への回答

\[
\boxed{\textbf{最小限の型付けを先に行い、その直後に第三例へ進む。}}
\]

「(6) を窓データから導く完全な十分条件を先に完成させる」ことは勧めない。
二例だけで一般条件を固定すると過適合しやすいので、その部分は
Opus の見立てどおり第三例の後でよい。

しかし第三例を先に計算し、後から何を比較したか定義する順序も危険である。
実際、現 \(q\)-表現には (7.2) の split 条件が隠れていた。
従って順序を二段に分ける。

1. **今すぐ** (R6-act)、(7.3)、棄却条件を型付きで固定する。
   これは一頁未満で済み、結果値を含まない。
2. その定義を封印して第三例を選ぶ。
3. 第三例の後に、
   (R6-act) を marking・normalizer・centralizer 等から導く
   window-intrinsic な十分条件を帰納的に抽出する。

第三例は、可能ならもう一つの coprime 例でなく
\[
\gcd(e,M/e)>1
\]
となる repeated-primary regime を優先すべきである。
そこで

- \(q\)-版が本当に破れるか、
- full \([u]_M\)-版なら生きるか、
- \(\mathfrak F_0\) が translation subgroup と一致するか

を同時に試せる。第三例を同じ coprime regime から選ぶと、
現在の二例が共有する隠れた split 仮定を発見できない。

従って T-11 の二択への短答は

> **完全な導出条件は第三例の後。だが前件 (6) の型付き定義は第三例の前。**

である。

---

## F9. 状態札

v2 冒頭と §7 の

> 群論部分（\(\Lambda\)、\(\mathfrak F_0\) 作用、\(\Phi\) 単射、軌道）は
> GAP と node の二系統一致 = cross-checked

は少し広い。

- `gap18a.json` と新 node の突合が直接覆う
  \(\Lambda\) の構造と \(\mathfrak F_0\)-作用:
  **cross-checked** としてよい。
- 全 12 元での \(\Phi\) 単射:
  **紙上証明 + node 43/43**。
  既存 GAP 証明書は 12 個の induced automorphism の相異性を
  明示検査していないため、項目単独では `cross-checked` と言い切らない。
- good 12 の Aut-fusion:
  現在開示された直接証拠は node 系。
  `gap18a.json` は四つの \(G_3\)-共役類を与えるが、
  Aut-fusion 自体の独立 GAP 証明書ではない。

推奨する札は

> **\(\Lambda\) と \(\mathfrak F_0\)-作用は GAP/node cross-checked。
> \(\Phi\) 単射と Aut-fusion は紙上 + node。
> 定理全体は paper-proof / two-mathematician audit PASS、
> Lean verified ではない。**

である。

これは検証序列の語の精度だけの修正であり、
定理 \(K3\) の紙上 PASS には影響しない。

---

## 提案・警告

- **P1**: 定理 \(K3\) を正式に
  `paper-proof / two-mathematician audit PASS` へ昇格。
- **P2**: 【GAP-20b】を
  `ordered-passport-preserving normalization` の射程で閉鎖。
- **P3**: \(R^{\mathrm{cyc}}\) (6) を (R6-act) と
  coprime pushout 条件 (7.2) に分離。
- **P4**: 第三例は可能なら repeated-primary regime を選ぶ。
- **P5**: §7 の `cross-checked` 札を項目別に限定。

- **W1**: \(q:\mu_M\twoheadrightarrow\mu_e\) は、
  位数 \(e\) translation subgroup への retraction とは限らない。
- **W2**: 「作用と一致」という語は、domain/codomain と
  可換図を書かない限り判定可能な前件にならない。
- **W3**: 第三例は既存二例と同じ split regime を選ぶだけでは
  一般化の falsifier にならない。

---

## 最終検収表

| 項目 | 判定 |
|---|---|
| 補題 P(a′) | **PASS** |
| 補題 P(d′) 短縮 | **PASS・忠実性不要** |
| 忠実性の依存箇所 | **固定体同定の逆向きのみで正しい** |
| (K4) \(\Phi\) 単射 | **PASS** |
| kernel/quotient proof | **PASS** |
| good 12 の 6+6 分裂・Aut 融合 | **PASS** |
| 【GAP-20b】 | **限定した射程で閉鎖可** |
| 固定体・Galois 群 | **PASS** |
| 定理 \(K3\) | **紙上相互監査 PASS** |
| \(R^{\mathrm{gen}}\) 格下げ | **PASS** |
| \(R^{\mathrm{cyc}}\) | **定理候補のまま・前件 (6) は F7 の型へ修正推奨** |
| Lean verified | **なし** |

