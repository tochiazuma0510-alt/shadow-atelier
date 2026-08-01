# 追補 E-F(**裁定 394 採択札 F** = GEN-DESC / FIVE-BYPASS / 量化緩和)

**位置づけ**: `docs/notes/ihnec_v1.md` への**追補 E の第 1 部**(erratum 方式)。**v1 本文・追補 A/B/C/D は 1 バイトも改変していない** — 置換関係は §E-F.6 の対応表に明記する。
**起草**: 数学者(Opus 5)/ 2026-08-01。**委嘱** = 発案係第 18 便・裁定 394 採択札 F。**Sol 未監査。**
**封印遵守**: $K^{(5)}$ の**値・座標・位数・測定・窓内計算に一切触れない**。§E-F.4.3 の系のみが $K^{(5)}$ を**名指し**するが、それは純粋に形式的な含意であり、**正式登録は §E-F.4.1 の量化緩和形のみ**(裁定 394 の規律ガード)。

> ### 【追記 F ポインタ(2026-08-01・裁定 396 / 399 / 398)】
> ★ **上の「正式登録は量化緩和形のみ」という規律ガードは解除された。** **裁定 396**($K^{(5)}$ 開封の研究者認可)により、**系 FIVE-BYPASS は $K^{(5)}$ を名指しした完全形で正式登録される**(裁定 399 が次波での登録を指示)。⟹ **§E-F.4.3 の「研究者確認待ち・正式登録しない」札と ⚠ 規律枠、§E-F.7.1 の同札、§E-F.7.5 の項 3 は、末尾の【追記 F】が置換**する(**本文は 1 バイトも改変していない** — CV-10 additive erratum 方式)。
> ★ さらに **裁定 398**(n=5 開封対決)により **$K^{(5)}$ の封印そのものが解除**されたため、**FIVE-BYPASS の位置づけが「$n=5$ の肩代わり」から「独立の整合性検査 + GEN-COFINAL の系」へ変わる**(【追記 F】§F.3)。**§E-F.4.4 の「買うもの」欄はこの変化を受ける。**

---

## E-F.0 先に一枚 — **何を検査し、何が出たか**

発案係が「破綻しそうな点」として名指ししたのは **(THM44) の射程**であった。検査の結果:

| 検査項目 | 結果 |
|---|---|
| **(THM44) の向き**($K^{(q)}\le K^{(n)}$ で $R$ がどちら向きか) | ★ **合っている**。逐語 pin 取得済(§E-F.2.1)。$q=15,n=5$ は $5\mid15$ で適用可 ⟹ **停止報告は不要** |
| **(THM44) の証明** | ★★ **問題あり**。**奇 $q$ の分岐は、正典の証明が「読者演習」と明記された分岐を経由している**(§E-F.2.2)。**工房が実際に使っているのはこの分岐だけである** |
| 格の訂正 | v1 §5.2 前件表の「**(THM44) 格 $=$ 正典の定理**」は**誤り** ⟹ 「**正典の言明・奇分岐の証明は原論文に無い**」へ差替(§E-F.6) |
| 自前補完 | **補題 THM44-odd**(§E-F.3.2)で奇分岐を閉じた。その依存先 Thm 4.3 も偶 $m$ 分岐が読者演習だったので**補題 PROP41-EVEN-odd**(§E-F.3.1)で先に閉じた ⟹ **読者演習 2 段を降りきった** |
| 札 F 本体 | **補題 GEN-DESC**(§E-F.1・定義から 1 行)+ **定理 GEN-COFINAL**(§E-F.4.1)は成立。系 FIVE-BYPASS は §E-F.4.3(**研究者確認待ちの札**) |

> ★ **本追補の核心を一行で**: 札 F の論理($n=5$ を $n=15$ が肩代わりする)は正しいが、**それを支える (THM44) は工房が思っていたほど正典に載っていなかった**。値打ちは迂回の系そのものより、**依存の根を 2 段掘って閉じたこと**にある。
>
> ⚠ **同時に、迂回の実効性を過大評価してはならない**: $\lvert\mathrm{GT}(K^{(15)})\rvert=240$、$\lvert\mathrm{GT}(K^{(5)})\rvert=40$ — **迂回先は 6 倍大きい窓**であり、しかも「全 shadow が genuine」は有限深度で決定できない(【IHNEC-GAP-1】)。**負担は軽くならず、置き場所が変わるだけ**である(§E-F.4.4)。

---

## E-F.1 補題 GEN-DESC — **genuine は reduction で押し出される**

### E-F.1.1 逐語 pin(2401.06870)

| 札 | 正典逐語 | 頁 |
|---|---|---|
| **(GEN-DEF)** | **Definition 4.2**: "*Let $N\in\mathrm{NFI}_{PB_3}(B_3)$ and $[m,f]\in\mathrm{GT}(N)$. We say that the GT-shadow $[m,f]$ is **genuine** if there exists $(\hat m,\hat f)\in\widehat{GT}_{gen}$ such that $[m,f]$ comes from $(\hat m,\hat f)$, i.e. $m+N_{ord}\mathbb Z=\widehat P_{N_{ord}}(\hat m)$, $fN_{F_2}=\widehat P_{N_{F_2}}(\hat f)$. Otherwise, the GT-shadow is called **fake**.*" | §4 |
| **(P312a/b)** | **Prop 3.12**(追補 D.3.1 で pin 済): "*Let $N,H\in\mathrm{NFI}_{PB_3}(B_3)$, $N\le H$ and $(m,f)$ represent a GT-pair with the target $N$. Then $H_{ord}\mid N_{ord}$, $N_{F_2}\le H_{F_2}$ …*" | p.19 |
| **(P312c)** | **Prop 3.12 c)**: "*if the pair $(m,f)$ represents a GT-shadow with the target $N$, then $(m,f)$ also represents a GT-shadow with the target $H$.*" | p.19 |
| **(3.60)** | $R_{N,H}([m,f]):=(m+H_{\rm ord}\mathbb Z,\ fH_{F_2})$ | p.19 |

### E-F.1.2 補題

> ### 補題 GEN-DESC
> $N,H\in\mathrm{NFI}_{PB_3}(B_3)$、$N\le H$(すなわち $N\subseteq H$)とする。
> $$[m,f]\in\mathrm{GT}(N)\ \text{が genuine}\quad\Longrightarrow\quad R_{N,H}([m,f])\in\mathrm{GT}(H)\ \text{も genuine}.$$
> すなわち $\ R_{N,H}\bigl(\mathrm{GT}_{\rm gen}(N)\bigr)\subseteq\mathrm{GT}_{\rm gen}(H)$。

**証明.** (P312c) より $R_{N,H}([m,f])\in\mathrm{GT}(H)$ は定義される。$[m,f]$ が genuine なので (GEN-DEF) の証人 $(\hat m,\hat f)\in\widehat{GT}_{\rm gen}$ があり
$$m+N_{\rm ord}\mathbb Z=\widehat P_{N_{\rm ord}}(\hat m),\qquad fN_{F_2}=\widehat P_{N_{F_2}}(\hat f).$$
(P312a) より $H_{\rm ord}\mid N_{\rm ord}$ だから、射影 $\widehat{\mathbb Z}\to\mathbb Z/H_{\rm ord}$ は $\widehat{\mathbb Z}\to\mathbb Z/N_{\rm ord}\to\mathbb Z/H_{\rm ord}$ と分解する。ゆえに
$$\widehat P_{H_{\rm ord}}(\hat m)=\bigl(m+N_{\rm ord}\mathbb Z\bigr)\bmod H_{\rm ord}=m+H_{\rm ord}\mathbb Z.$$
同様に (P312a) の $N_{F_2}\le H_{F_2}$ より $\widehat F_2\to F_2/H_{F_2}$ は $F_2/N_{F_2}$ を経由し
$$\widehat P_{H_{F_2}}(\hat f)=(fN_{F_2})H_{F_2}=fH_{F_2}.$$
(3.60) より右辺の対は $R_{N,H}([m,f])$ そのもの。したがって**同一の証人 $(\hat m,\hat f)$** が $R_{N,H}([m,f])$ の genuine 性を与える。$\blacksquare$

> ### ★ この補題の性格(**「定義から 1 行」の意味**)
> 使ったのは **Def 4.2・Prop 3.12・(3.60)・射影の分解**だけである。とくに
> - **$N$ も $H$ も isolated である必要がない**(群構造を一切使わない)。
> - **$\mathcal{PR}_N$ が関手であること(2401 Thm 4.4)を使わない**。genuine の定義が**成分ごとの射影の像**として与えられているため、二段の射影 $=$ 一段の射影という**集合水準の事実**だけで閉じる。
> - **$\widehat{GT}_{\rm gen}$ の位相・群構造を使わない**。

> ### 系 GEN-DESC-arith(**算術層でも同じ** — 無料)
> $R_{N,H}\bigl(\mathrm{GT}_{\rm arith}(N)\bigr)\subseteq\mathrm{GT}_{\rm arith}(H)$。
> **証明.** 上と同じ計算を $\hat\sigma=\mathrm{Ih}(\gamma)$ に適用すれば $R_{N,H}\circ\mathcal{PR}_N=\mathcal{PR}_H$(v1 補題 IH-0 の一般形)、ゆえに $R_{N,H}\circ\mathrm{Ih}_N=\mathrm{Ih}_H$。∎

> ### 系 GEN-DESC-fake(**対偶 — fake は reduction で引き戻る**)
> $N\le H$、$y\in\mathrm{GT}(H)$ が fake ならば、$R_{N,H}(x)=y$ なる**任意の** $x\in\mathrm{GT}(N)$ は fake。

---

## E-F.2 (THM44) の逐語 pin と **射程の訂正**

### E-F.2.1 逐語 pin(2405.11725)— **向きの確認 = 札 F の唯一の依存**

> **Theorem 4.4**(p.18): "*Let $n,q\in\mathbb Z_{\ge3}$ and $K^{(q)}\le K^{(n)}$. Then the reduction homomorphism*
> $$R_{K^{(q)},K^{(n)}}:\mathrm{GT}(K^{(q)})\to\mathrm{GT}(K^{(n)})$$
> *is surjective.*"

> **Proposition 3.5**(p.15): "*Let $n,q\ge3$. Then $K^{(q)}\subset K^{(n)}\iff n\mid\mathrm{lcm}(q,2)$.*"
> **Remark 3.3**(p.14): "*If $q,n\in\mathbb Z_{\ge3}$, $n\mid q$, … the formulas $\eta_{q,n}(a):=r,\ \eta_{q,n}(b):=s$ define a natural homomorphism $\eta_{q,n}:D_q\to D_n$. Since $\eta_{q,n}\circ\psi_q=\psi_n$, we have $K^{(q)}\le K^{(n)}$.*"

**向きの判定**: **源 $=K^{(q)}$(細かい窓)・標的 $=K^{(n)}$(粗い窓)**。v1 §1 表の (THM44) 行の記述と**一致**。
**$q=15,n=5$ への適用可能性**: $5\mid15$ ゆえ Remark 3.3 で直ちに $K^{(15)}\le K^{(5)}$(Prop 3.5 でも $\mathrm{lcm}(15,2)=30$、$5\mid30$ で一致)。両者 $\ge3$。
⟹ ★ **向きは合っている。裁定 394 が指示した「向きが合わなければ停止報告」の条件は発動しない。**

> ### ⚠ **名前衝突の警告(grep 事故の元)**
> **2401 にも「Theorem 4.4」がある**が、それは **$\mathcal{PR}:\widehat{GT}^{\rm NFI}_{\rm gen}\to\mathrm{GTSh}$ が関手であること**(approximation)であり、**本札 (THM44) $=$ 2405 Thm 4.4(reduction 全射性)とは別物**である。
> 工房内で **2401 Thm 4.4** を指しているのは `docs/notes/2401.06870-抽出ノート_v1.md` L117 と `docs/notes/wexist_check_v1.md` L207(**本追補の訂正は及ばない**)。**`Thm 4.4` の grep 結果を無条件に本追補の対象と読まないこと。**

### E-F.2.2 ★★ **しかし証明の場合分けに穴がある**(本追補の第 1 の発見)

Thm 4.4 の証明(2405 pp.18–19)は 3 分岐からなる。**逐語**:

1. "*Proof. Let us assume that $4\mid q$. …*"(以下、CRT による完全な証明)…"*We proved that the reduction homomorphism $R_{K^{(q)},K^{(n)}}$ is surjective in the case when $4\mid q$.*"
2. "*If $4\nmid q$ but $q$ is even, then Proposition 3.5 still implies that $n\mid q$. **In this case the proof of surjectivity of $R_{K^{(q)},K^{(n)}}$ is easier and we leave it to the reader.**"*
3. "*If $q$ is odd, then Proposition 3.5 implies that $n\mid2q$. Due to Proposition 3.4, we have $\mathrm{GT}(K^{(q)})=\mathrm{GT}(K^{(2q)})$ and the desired statement follows from the surjectivity of the reduction homomorphism $R_{K^{(2q)},K^{(n)}}:\mathrm{GT}(K^{(2q)})\to\mathrm{GT}(K^{(n)})$ **established above**.*"

> ### ★ 指摘
> $q$ が**奇**ならば $2q\equiv2\pmod4$、すなわち **$4\nmid2q$**。したがって分岐 3 が参照する $R_{K^{(2q)},K^{(n)}}$ は**分岐 1(4 で割れる場合)ではなく分岐 2(読者演習)に属する**。
> $$\boxed{\ \textbf{分岐 3 の「established above」が指す先は、証明が掲載されていない分岐である。}\ }$$
> ⟹ **(THM44) の奇 $q$ 分岐は、正典に証明が掲載されていない。**

**格の訂正**:

| | v1 §5.2 前件表 | ★ 訂正後 |
|---|---|---|
| **(THM44)** | 格 $=$ **正典の定理** | **正典の言明**(p.18・逐語照合済)。**$4\mid q$ 分岐のみ証明掲載**。$4\nmid q$ 偶分岐 $=$ 読者演習。**奇 $q$ 分岐 $=$ 読者演習分岐を経由**(上記) |

### E-F.2.3 **射程の実害**(どこに効くか)

v1 が (THM44) を使う箇所は 3 つで、**すべて $\mathrm{Dih}^{\rm odd}$ 内部**($q,n$ ともに奇):

| 使用箇所 | 内容 |
|---|---|
| 補題 E1-3d($\mathrm{pr}_n$ 全射) | E1 ノート §3.1。定理 E1-3 の (ii)$\Rightarrow$(i) が乗る |
| **ML-ODD (i)$\Rightarrow$(iii)**(v1 §4.3) | 補題 E1-3d 経由 |
| 系 ML-C(v1 §4.4) | $\mathrm{Dih}^{\rm odd}$ 内部の共通部分が恒真 |

$$\Longrightarrow\ \textbf{工房が実際に使っているのは、正典に証明が掲載されていない分岐だけである。}$$

**軽減材料(先行資産・grep 済)**: E1 ノート §2.1 の **系 E1-S2′**(「$d\mid n$ 奇に対し $\mathbb Z/n\twoheadrightarrow\mathbb Z/d$ と $(\mathbb Z/n)^\times\twoheadrightarrow(\mathbb Z/d)^\times$ はともに全射だから $R_{K^{(n)},K^{(d)}}$ は全射」)は、**この奇分岐の独立再導出として既に工房にあった**。⟹ **本追補は「新しい穴を開けた」のではなく「既にあった補修の必要性を確定させた」**。
ただし系 E1-S2′ は 命題 E1-S1(座標 $\Theta_n$)経由で **正典 Thm 4.3 (4.12)** に依拠し、**Thm 4.3 の証明も Prop 4.1 の偶 $m$ 分岐が読者演習**である(§E-F.3.1)。⟹ **読者演習が 2 段重なっていた。** §E-F.3 で両方を閉じる。

---

## E-F.3 自前補完 — 読者演習 2 段を降りる

記法は 2405 §3–§4 に従う。$n$ 奇 $\ge3$ とし
$$F_2/K^{(n)}_{F_2}\ \cong\ G_n=\langle x,y\rangle\le D_n^3,\qquad x=(r,s,s),\ y=(rs,r,rs),\ z=(r^2s,r^{-1}s,r)\tag{3.6}$$
$xyz=1$(ゆえに $z=(xy)^{-1}$)。$\theta(x)=y,\ \theta(y)=x$;$\tau(x)=y,\ \tau(y)=z,\ \tau(z)=x$。
$n$ 奇より $\mathrm{ord}(r^2)=n$ かつ **Remark 3.7 (3.8)**: $[G_n,G_n]=\langle r^2\rangle^3=\langle r\rangle^3$。
$K^{(n)}_{\rm ord}=\mathrm{lcm}(n,2)=2n$(Remark 3.2 (3.4))。charming GT-pair $(m,g)$ の条件は
$$m\in\{0,\dots,K^{(n)}_{\rm ord}-1\},\quad\gcd(2m+1,K^{(n)}_{\rm ord})=1,\quad g\in[G_n,G_n],$$
$$g\,\theta(g)=1,\tag{4.4}\qquad \tau^2(y^mg)\,\tau(y^mg)\,y^mg=1.\tag{4.5}$$
(4.7) より (4.4) $\iff$ $g=(r^{2k},r^{-2k},r^{2t})$(正典が全 $m$ で解いている段)。

### E-F.3.1 補題 PROP41-EVEN-odd(**Prop 4.1 の偶 $m$ 分岐・$n$ 奇**)

> **正典の逐語**(Prop 4.1 の証明、p.16): "*For odd $m$, the desired statement is proved right above the proposition. **The case when $m$ is even is easier and we leave it to the reader.***"

> ### 補題 PROP41-EVEN-odd
> $n$ 奇 $\ge3$、$m$ **偶**、$g=(r^{2k},r^{-2k},r^{2t})\in[G_n,G_n]$ が (4.4) を満たすとする。このとき
> $$(4.5)\iff 2t\equiv-m\equiv\varkappa(m)\pmod n .$$
> ($\varkappa$ は (4.9);$m$ 偶で $\varkappa(m)=-m$。)

**証明.** $m=2\mu$ と置く。$D_n$ で $(rs)^2=r(srs)=r\cdot r^{-1}=1$、すなわち $\mathrm{ord}(rs)=2$。ゆえに $m$ 偶のとき
$$y^m=\bigl((rs)^m,\ r^m,\ (rs)^m\bigr)=(1,\ r^{2\mu},\ 1),$$
$$w:=y^mg=\bigl(r^{2k},\ r^{2(\mu-k)},\ r^{2t}\bigr).$$
$n$ 奇より各成分は $\langle r^2\rangle$ に属するので **$w\in[G_n,G_n]$**、したがって (4.8) $\tau(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_3},r^{2n_1},r^{2n_2})$ が適用できて
$$\tau(w)=\bigl(r^{2t},\ r^{2k},\ r^{2(\mu-k)}\bigr),\qquad \tau^2(w)=\bigl(r^{2(\mu-k)},\ r^{2t},\ r^{2k}\bigr).$$
積 $\tau^2(w)\tau(w)w$ を成分ごとに計算すると(全て $\langle r\rangle$ 内なので可換)
$$\text{第 1}:\ r^{2(\mu-k)+2t+2k}=r^{2(\mu+t)},\quad\text{第 2}:\ r^{2t+2k+2(\mu-k)}=r^{2(\mu+t)},\quad\text{第 3}:\ r^{2k+2(\mu-k)+2t}=r^{2(\mu+t)} .$$
ゆえに $(4.5)\iff 2(\mu+t)\equiv0\pmod n$。$n$ 奇で $2$ は可逆だから $\iff\mu+t\equiv0\pmod n\iff 2t\equiv-2\mu=-m\pmod n$。$\blacksquare$

> ### ★ なぜ偶の方が「easier」なのか(正典の言い回しの裏取り)
> **$m$ 偶のときだけ $y^m\in[G_n,G_n]$ になる**ため、(4.8) がそのまま適用できて 3 行で終わる。$m$ 奇では $y^m=(rs,r^m,rs)\notin\langle r\rangle^3$ なので (4.5) を手で展開する必要があり、正典の長い display はそのためである。**正典の "easier" の内実はこれ**であり、上の証明はその内実を書き下したものである。

> ### 系 THM43-odd(**Thm 4.3 (4.12) の $n$ 奇分岐が完全に証明された**)
> $n$ 奇 $\ge3$ に対し
> $$\mathrm{GT}(K^{(n)})=\bigl\{\,(m,\ (r^{2k},r^{-2k},r^{\varkappa(m)}))\ \big|\ m\in\mathcal X_n,\ k\in\mathbb Z/n\,\bigr\},\qquad\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n).$$
> **証明.** (4.4) の解は正典が全 $m$ で与えている。(4.5) の解は $m$ 奇が正典(p.16 の display)、$m$ 偶が補題 PROP41-EVEN-odd。両分岐とも「第 3 成分 $r^{2t}=r^{\varkappa(m)}$」に帰着する($n$ 奇で $2$ 可逆ゆえ $t$ は $\varkappa(m)$ から一意)。$4\nmid n$ なので $k$ と $m$ を結ぶ追加条件は発動せず、$k$ は $\mathbb Z/n$ を自由に走る($\mathrm{ord}(r^2)=n$)。charming GT-pair が GT-shadow であることは Lemma 4.2(正典・完全な証明あり)。個数は $\lvert\mathcal X_n\rvert\cdot n=2\varphi(n)\cdot n$(命題 E1-S1 (c))。∎

### E-F.3.2 補題 THM44-odd(**(THM44) の奇分岐**)

> ### 補題 THM44-odd
> $n,q$ 奇 $\ge3$、$n\mid q$($\iff K^{(q)}\subseteq K^{(n)}$;Remark 3.3 / E1-D2(3))。このとき
> $$R_{K^{(q)},K^{(n)}}:\mathrm{GT}(K^{(q)})\longrightarrow\mathrm{GT}(K^{(n)})\quad\textbf{は全射}.$$

**証明.** 系 THM43-odd により両辺は (4.12) の座標で書ける。

**(a) $R$ の座標表示.** (3.60) より $R([m,f])=(m\bmod 2n,\ fK^{(n)}_{F_2})$。第 2 成分は、Remark 3.3 の $\eta_{q,n}:D_q\to D_n$($r\mapsto r,\ s\mapsto s$)から誘導される $G_q\twoheadrightarrow G_n$ による像である(両者は生成元 $x,y$ の上で一致する準同型であり、$G_q=\langle x,y\rangle$ ゆえ一致する — 命題 E1-S2 と同じ観察)。ゆえに $r^{2\tilde k}\mapsto r^{2\tilde k\bmod n}$。
第 3 成分の整合: $\tilde m\equiv m\pmod{2n}$ ならば $\tilde m\equiv m\pmod2$ なので $\varkappa$ は同じ分岐を使い、$\varkappa(\tilde m)\equiv\varkappa(m)\pmod{2n}$、とくに $\pmod n$。ゆえに $r^{\varkappa(\tilde m)}\mapsto r^{\varkappa(m)}$。
$$\Longrightarrow\quad R:\ (\tilde m,\tilde k)\ \longmapsto\ (\tilde m\bmod2n,\ \tilde k\bmod n).$$

**(b) 目標.** 与えられた $(m,k)\in\mathcal X_n\times\mathbb Z/n$ に対し $(\tilde m,\tilde k)\in\mathcal X_q\times\mathbb Z/q$ を作る。$\tilde k$ は $k$ の代表を取ればよい($n\mid q$ より $\tilde k\equiv k\bmod n$)。$4\nmid q$ ゆえ $\tilde k$ と $\tilde m$ を結ぶ条件は無い。残るのは
$$\exists\,\tilde m\in\mathcal X_q\ \text{with}\ \tilde m\equiv m\pmod{2n}.$$

**(c) 存在.** $\tilde m=m+2nz$($z\in\mathbb Z$)と置くと $2\tilde m+1=(2m+1)+4nz$。$q$ 奇より $\mathcal X_q$ の条件 $\gcd(2\tilde m+1,2q)=1$ は $\gcd(2\tilde m+1,q)=1$ と同値($2\tilde m+1$ は奇)。素数 $p\mid q$ ごとに:
- **$p\mid n$ のとき**: $4nz\equiv0\pmod p$ ゆえ $2\tilde m+1\equiv2m+1\pmod p$。仮定 $\gcd(2m+1,2n)=1$ より $p\nmid2m+1$。⟹ **$z$ に依らず成立**。
- **$p\nmid n$ のとき**: $q$ 奇より $p$ 奇、ゆえ $\gcd(4n,p)=1$。したがって $z\mapsto(2m+1)+4nz \bmod p$ は $\mathbb Z/p$ 上の全単射であり、$p\nmid(2\tilde m+1)$ となる $z\bmod p$ が $p-1\ge2$ 個ある。

$p\nmid n$ なる $p\mid q$ は有限個で互いに素だから、**CRT** により全条件を同時に満たす $z$ が取れる。その $\tilde m$ を $\bmod\ 2q$ で代表すれば $\tilde m\in\mathcal X_q$。$\blacksquare$

> ### ★ 依存の向きの確認(**非循環** — この確認が無いと補完に意味がない)
> 補題 THM44-odd の証明が使ったのは
> **Remark 3.2 (3.4)・Remark 3.3・(3.60)・Lemma 4.2・Prop 4.1 の (4.4) 段と奇 $m$ 段(正典)・補題 PROP41-EVEN-odd(本追補)・CRT** のみ。
> - **Theorem 4.4 本体を使っていない**(当然)。
> - ★ **Proposition 3.4($K^{(q)}=K^{(2q)}$)を使っていない** ⟹ **正典の奇分岐が経由する $K^{(2q)}$ への迂回そのものを回避している**。したがって「読者演習分岐に載る」問題は再発しない。
> - **Prop 3.5 も不要**($n\mid q$ から Remark 3.3 で直接に $K^{(q)}\le K^{(n)}$)。
> - **Cor 5.4・Thm 5.2・Prop 3.14/3.15 を使っていない** ⟹ v1 の他の前件と循環しない。
> また補題 PROP41-EVEN-odd は **(4.8)・$D_n$ の初等計算**のみを使い、Prop 4.1 以降の一切を使わない。

> ### 射程の申告(**閉じていない分岐**)
> 本追補が閉じたのは **$n,q$ ともに奇**の場合のみである。**$4\nmid q$ かつ $q$ 偶**の分岐(正典の読者演習)は**依然として未証明**であり、**Prop 4.1 の偶 $m$ 分岐も $4\mid n$ の場合は未閉鎖**($[G_n,G_n]$ の同偶奇条件が効くため上の 3 行証明はそのままでは通らない)。⟹ 【IHNEC-GAP-5】(§E-F.7)。

---

## E-F.4 一般形と系

### E-F.4.1 ★ 定理 GEN-COFINAL(**正式登録するのはこれ**)

> ### 定理 GEN-COFINAL(ML-ODD (iii) の量化緩和)
> $S\subseteq\{n\ \text{奇}\ \ge3\}$ が **整除共終**(divisibility-cofinal)であるとする。すなわち
> $$\forall\,n\ \text{奇}\ \ge3\ \ \exists\,s\in S:\ n\mid s. \tag{DC}$$
> このとき
> $$\boxed{\ \bigl[\forall s\in S:\ \mathrm{GT}_{\rm gen}(K^{(s)})=\mathrm{GT}(K^{(s)})\bigr]\ \iff\ \bigl[\forall n\ \text{奇}\ \ge3:\ \mathrm{GT}_{\rm gen}(K^{(n)})=\mathrm{GT}(K^{(n)})\bigr]\ =\ \textbf{ML-ODD (iii)}\ }$$

**証明.** ($\Leftarrow$)$S$ は奇数の部分集合だから自明。
($\Rightarrow$)奇 $n\ge3$ を取り、(DC) により $s\in S$ を $n\mid s$ に取る。Remark 3.3 より $K^{(s)}\subseteq K^{(n)}$。**補題 THM44-odd** より $R_{K^{(s)},K^{(n)}}$ は全射。仮定より $\mathrm{GT}(K^{(s)})=\mathrm{GT}_{\rm gen}(K^{(s)})$。**補題 GEN-DESC** より
$$\mathrm{GT}(K^{(n)})=R_{K^{(s)},K^{(n)}}\bigl(\mathrm{GT}(K^{(s)})\bigr)=R_{K^{(s)},K^{(n)}}\bigl(\mathrm{GT}_{\rm gen}(K^{(s)})\bigr)\subseteq\mathrm{GT}_{\rm gen}(K^{(n)})\subseteq\mathrm{GT}(K^{(n)}).$$
ゆえに等号。$\blacksquare$

> ### 系 CHAIN(**1 本の塔で足りる**)
> $N_1\mid N_2\mid N_3\mid\cdots$ を奇数の増大列で、任意の奇 $n\ge3$ がある $N_j$ を割るものとする(例: $N_j:=\mathrm{lcm}(3,5,7,\dots,2j+1)$、あるいは $N_j:=3\cdot5\cdots(2j+1)$)。このとき
> $$\textbf{ML-ODD (iii)}\iff\forall j\ge1:\ \mathrm{GT}_{\rm gen}(K^{(N_j)})=\mathrm{GT}(K^{(N_j)}).$$
> ⟹ **(iii) は「奇数全体にわたる族の条件」ではなく「1 本の塔に沿った条件」として書ける。**($\{K^{(N_j)}\}$ は $\mathrm{Dih}^{\rm odd}$ の中で共終な**鎖**である。)

> ### 系 FAKE-LIFT(**対偶 — fake は整除で上へ伝播する**)
> 奇 $n\mid s$($n,s\ \text{奇}\ \ge3$)ならば
> $$\mathrm{GT}(K^{(n)})\ \text{が fake を含む}\ \Longrightarrow\ \mathrm{GT}(K^{(s)})\ \text{も fake を含む}.$$
> **証明.** $y\in\mathrm{GT}(K^{(n)})$ を fake とする。補題 THM44-odd より $R_{K^{(s)},K^{(n)}}(x)=y$ なる $x$ が存在し、系 GEN-DESC-fake より $x$ は fake。∎
>
> ⟹ $\mathcal F:=\{n\ \text{奇}\ \ge3\mid\mathrm{GT}(K^{(n)})\ \text{が fake を含む}\}$ は**整除順序で上に閉じ**、補集合 $\mathcal G$ は**下に閉じる**。とくに
> $$\bigl[\mathrm{GT}(K^{(n)})\ \text{全 genuine}\bigr]\Longrightarrow\bigl[\text{全ての奇約数}\ d\mid n\ \text{で}\ \mathrm{GT}(K^{(d)})\ \text{全 genuine}\bigr].$$
> **ML-ODD (iii)** $\iff\mathcal F=\emptyset$。

> ### ★ 哨戒設計への含意(追補 D.1.5 の 4 点への追加)
> 5. **fake 探索は極小元探索である**。$\mathcal F$ が上に閉じるので、「最初に fake が出る奇数」を探す問題は $\mathcal F$ の**整除順序での極小元**を探す問題に等しい。⟹ **小さい奇数から順に潰す**戦略が(全数走査ではなく)構造的に正当化される。逆に **大きい $n$ で fake が出ても、その約数について何も言わない**(伝播は上向きの一方通行)。

### E-F.4.2 ML-ODD (ii) 側の対応物

> ### 系 GEN-COFINAL-(ii)
> $S$ を (DC) を満たす奇数集合とすると、v1 定理 ML-ODD の (ii) についても
> $$\bigl[\forall s\in S,\ \forall N\in I,\ N\subseteq K^{(s)}:\ R_{N,K^{(s)}}\ \text{全射}\bigr]\iff\textbf{(ii)}.$$
> **証明.** ML-ODD の (ii)$\iff$(iii)(v1 §4.3・(COR54))を各 $n$ で使い、定理 GEN-COFINAL を挟む。∎

### E-F.4.3 系 FIVE-BYPASS(★ **研究者確認待ちの札 — 正式登録しない**)

> ### 系 FIVE-BYPASS
> $$\mathrm{GT}_{\rm gen}(K^{(15)})=\mathrm{GT}(K^{(15)})\quad\Longrightarrow\quad\mathrm{GT}_{\rm gen}(K^{(5)})=\mathrm{GT}(K^{(5)}).$$
> **証明.** 定理 GEN-COFINAL の証明の $n=5,\ s=15$ の場合($5\mid15$)。∎
>
> ### ⚠ 規律(裁定 394 の規律ガード)
> - 本系は $\mathrm{GT}(K^{(5)})$ の**値・元・座標・位数・測定値に一切触れない形式的含意**であり、$K^{(5)}$ の窓内計算を**一切要求しない**。
> - **台帳・地図・便・他文書への登録は §E-F.4.1 の定理 GEN-COFINAL(量化緩和形)のみ**とする。本系は**研究者確認まで本追補の内部にとどめ、引用しない**。
> - 同じことは「$S=\{n\ \text{奇}\ \ge3\}\setminus\{5\}$ は (DC) を満たす($5\mid15$)」と述べれば **$K^{(5)}$ を名指さずに**言える。⟹ **公開面ではこの形を使うこと。**

### E-F.4.4 ★ 正直な評価(**迂回が何を買い、何を買わないか**)

| | 内容 |
|---|---|
| **買うもの** | ML-ODD (iii) の証明は、**任意の有限個の奇数の窓に一度も入らずに**閉じられる(除外した奇数の倍数が $S$ に残っていればよい)。⟹ **「封印($n=5$ 非接触)と ML-ODD (iii) の証明可能性は両立する」** — これが札 F の実質的な内容である |
| ★ **買わないもの(1)** | **計算量は下がらない、むしろ上がる**。$\lvert\mathrm{GT}(K^{(15)})\rvert=2\cdot15\cdot\varphi(15)=240$ に対し $\lvert\mathrm{GT}(K^{(5)})\rvert=2\cdot5\cdot\varphi(5)=40$ — **迂回先は 6 倍大きい窓**。$\mathrm{Dih}^{\rm odd}$ の外の細分 $N\subseteq K^{(15)}$ の量化も $K^{(5)}$ の場合より真に広い |
| ★ **買わないもの(2)** | 「全 shadow が genuine」は **有限深度では決定できない**(【IHNEC-GAP-1】・(COR54))。⟹ **負担が軽くなるのではなく、負担の置き場所が変わるだけ** |
| **買わないもの(3)** | 系 FAKE-LIFT により、**$K^{(15)}$ の方が fake を含みやすい**($\mathcal F$ は上に閉じる)。すなわち迂回先は**前件が偽になりやすい側**である |

> ⟹ **札 F の値打ちは「近道」ではなく「封印が数学的障害でないことの証明」**である。これは規律の設計上は重要だが、**中間峰の登頂距離を 1 ミリも縮めない**。

---

## E-F.5 検算(**証明とは独立・単系統 python・整数演算のみ**)

**script**: `search/probe/wac_v1/thm44_odd_check.py`
**SHA-256**: `d1d5bc34f624901ff12386480050330a303b66c0f9383676044c1e3aa91a7a33`

| 部 | 内容 | 結果 |
|---|---|---|
| **(A)** | $n=3,5,7,9$ で $G_n\le D_n^3$ を BFS 構成($\lvert G_n\rvert=4n^3$ を確認)、$\theta,\tau$ を生成元語から構成して**準同型性を機械検査**($\tau(z)=x$ も)、$[G_n,G_n]=\langle r\rangle^3$($n^3$ 個)を確認。**(4.4)(4.5) を定義どおり悉皆判定**して得た集合を Thm 4.3 (4.12) の予測と比較 | $\lvert\mathrm{GT}(K^{(n)})\rvert=12,40,84,108$($=2n\varphi(n)$)。**all-m / odd-m / EVEN-m すべて一致**。⟹ **補題 PROP41-EVEN-odd の機械照合 PASS** |
| **(B)** | $(q,n)=(9,3),(15,5),(15,3),(21,7),(25,5),(27,9),(45,15),(45,5),(45,9),(33,11),(35,7),(105,15)$ で (4.12) 座標の $R$ の像を悉皆計算 | **全 12 対で像 $=$ 全体(全射)**。⟹ **補題 THM44-odd の機械照合 PASS** |

**failures 0 / ALL PASS**。
⚠ **格の申告**: **単系統(python 1 実装)**。**cross-checked ではない。verified(Lean)でもない。** $n=9$ の $\lvert\mathrm{GT}(K^{(9)})\rvert=108$ は追補 C の GAP 証明書と一致するが、これは**独立系統での再現**であって CV-9 判読を経ていない。$n=5$ については **$\lvert\mathrm{GT}(K^{(5)})\rvert=40=2\cdot5\cdot\varphi(5)$ という正典 (4.23) から直ちに従う個数**のみが現れ、**封印対象(shadow の値・座標・算術性)には触れていない**。

---

## E-F.6 v1 本文・追補 B への訂正(**erratum 置換表**)

**v1 本文・追補 A/B/C/D は不改変。** 以下の読み替えを行う。

| 対象 | 差替前 | ★ 差替後 |
|---|---|---|
| **v1 §1 表 (THM44) 行** | 「$K^{(q)}\le K^{(n)}$ のとき $R$ は全射 / 出所 2405 Thm 4.4」 | 同左 + **格の注記**: 「正典の**言明**。$4\mid q$ 分岐のみ証明掲載。**奇 $q$ 分岐は読者演習分岐を経由**(§E-F.2.2)。**工房の証明 $=$ 補題 THM44-odd(§E-F.3.2)**」 |
| **v1 §5.2 前件表 (THM44) 行の「格」欄** | **正典の定理** | ★ **正典の言明 / 奇分岐は工房の証明(補題 THM44-odd)に相対的**。独立に系 E1-S2′(E1 ノート §2.1)も同じ分岐を再導出している(ただし同じく Thm 4.3 経由) |
| **v1 §5.2 前件表 (THM44) 行の「言明」欄** | 「**$\mathrm{Dih}$ 内** reduction 全射」 | ★ 「**$\mathrm{Dih}^{\rm odd}$ 内** reduction 全射」へ**狭める**。v1 の使用は全て奇であり(§E-F.2.3)、$\mathrm{Dih}$ 全体の形は偶 $q$ の未証明分岐(【IHNEC-GAP-5】)を含んでしまう |
| **v1 §7 格付け表** | — | **追加**: GEN-DESC・GEN-DESC-arith/fake・PROP41-EVEN-odd・THM43-odd・THM44-odd・GEN-COFINAL・CHAIN・FAKE-LIFT(§E-F.7 の表) |
| **v1 §8 GAP 表** | — | **追加**: 【IHNEC-GAP-5】(§E-F.7) |
| **追補 D.1.5 の哨戒 4 点** | — | **追加 5 点目**(§E-F.4.1 末尾・fake 探索は極小元探索) |
| **E1 ノート §2.1 系 E1-S2′ の位置づけ** | 「正典 Thm 4.4 の odd 部分の**独立再導出**であり新結果ではない」 | ★ **「独立再導出」ではなく「正典に証明が無い分岐の唯一の証明」だった**(本追補以前は)。ただし E1-S2′ 自身は Thm 4.3 経由 ⟹ **§E-F.3.1 が無いと根が閉じない**。**格は据え置き**(paper-proof candidate)だが**役割の記述を訂正** |

> **凍結物は不変**: 事前登録予言 **P-IHN-1〜7** および検算 digest(`edf6181376…d49309`、`f8be65ae…c88820b`)は**改訂なし**。本追補は $n=9$ の実測に一切波及しない($n=9$ で使った (THM44) の実例は無く、追補 C は証明書からの再導出のみ)。

---

## E-F.7 格付け・GAP・新規性申告・申し送り

### E-F.7.1 格付け

| # | statement | 状態 | 出所 |
|---|---|---|---|
| **GEN-DESC** | genuine は reduction で押し出される | **paper-proof candidate**(定義の展開のみ・Sol 未監査) | §E-F.1 |
| **GEN-DESC-arith / -fake** | 算術層でも同じ / 対偶 | **paper-proof candidate** | §E-F.1 |
| **PROP41-EVEN-odd** | $n$ 奇での Prop 4.1 偶 $m$ 分岐 | ★ **paper-proof candidate**(**正典に証明が無い分岐の補完**・検算 PASS・Sol 未監査) | §E-F.3.1 |
| **THM43-odd** | Thm 4.3 (4.12) の $n$ 奇分岐が完全 | **paper-proof candidate**(正典 $+$ 上の補完) | §E-F.3.1 |
| **THM44-odd** | $n,q$ 奇・$n\mid q$ で $R$ 全射 | ★ **paper-proof candidate**(**正典に証明が無い分岐の補完**・非循環確認済・検算 PASS・Sol 未監査) | §E-F.3.2 |
| **GEN-COFINAL** | (iii) の量化は整除共終集合へ緩められる | ★ **paper-proof candidate**(**本追補の主定理**) | §E-F.4.1 |
| **CHAIN** | (iii) $\iff$ 1 本の塔での条件 | **paper-proof candidate** | §E-F.4.1 |
| **FAKE-LIFT** | fake は整除で上へ伝播・$\mathcal F$ は上に閉じる | **paper-proof candidate** | §E-F.4.1 |
| **FIVE-BYPASS** | $K^{(15)}$ 全 genuine $\Rightarrow K^{(5)}$ 全 genuine | ★ **研究者確認待ち・正式登録せず** | §E-F.4.3 |
| **(THM44) 一般形($q$ 偶)** | — | ★ **UNKNOWN**(正典の読者演習・本追補でも未閉鎖) | 【IHNEC-GAP-5】 |

### E-F.7.2 GAP

> ### 【IHNEC-GAP-5】(**新規**)— (THM44) の偶 $q$ 分岐
> $4\nmid q$ かつ $q$ 偶の場合の $R_{K^{(q)},K^{(n)}}$ の全射性は、**正典で読者演習・本追補でも未閉鎖**。同様に **Prop 4.1 の偶 $m$ 分岐は $4\mid n$ の場合が未閉鎖**($[G_n,G_n]$ の同偶奇条件(Remark 3.7)が効くため §E-F.3.1 の 3 行証明が通らない)。
> **射程**: $\mathrm{Dih}^{\rm odd}$ 主線では**不要**。2 冪 dihedral(Thm 5.3 の線)・混合位数窓・$\mathrm{Dih}$ 全体での議論を使う文書があれば**そこは (THM44) の未証明分岐に乗っている**。
> **状態: UNKNOWN(未着手)。起票は司令塔判断。**

### E-F.7.3 新規性の申告(**grep 済**)

**grep 語**: `THM44`・`Thm 4.4`・`Theorem 4.4`・`GEN-DESC`・`FIVE-BYPASS`・`GEN-COFINAL`・`FAKE-LIFT`・`共終`・`読者演習`・`leave it to the reader`・`E1-S2`・`Prop 4.1`・`整除`。

- **既出**: 系 **E1-S2′**(E1 ノート §2.1・L165)が「(THM44) の odd 部分の座標的再導出」を既に持っていた ⟹ **補題 THM44-odd は結論としては新結果ではない**。定義ノート §6 の較正 branch suite が「(q,n) = (8,4),(36,12),(12,4),(18,3),(9,3)(Thm 4.4 の証明分岐を被覆)」として分岐の存在を意識していた。「読者演習」の型の指摘は **追補 B(2401 Prop 3.15)が 1 例目**。
- **本追補で新しいもの**: ① **(THM44) の奇 $q$ 分岐が正典で未証明であることの発見**(「established above」が読者演習分岐を指すという読み)② **補題 PROP41-EVEN-odd**(正典の "easier" の内実を書き下し、根まで閉じた)③ **定理 GEN-COFINAL / 系 CHAIN / 系 FAKE-LIFT**(ML-ODD (iii) の量化構造 — grep ヒット 0)④ 系 FAKE-LIFT による**哨戒の極小元構造**。
- **補題 GEN-DESC は自明**(定義の展開)。**定理としての新規性は主張しない** — 値打ちは「(iii) の量化緩和を成立させる唯一の道具がこれである」という位置づけにある。
- **「初」という語は使わない**。GEN-COFINAL の型(共終部分族での判定)は逆極限論の標準であり、一般論としては既知である可能性が高い。**本設定への翻訳と、依存の根の補完が本追補の寄与**である。

### E-F.7.4 Sol 監査の依頼(**優先順位つき**)

1. ★★ **§E-F.2.2 の読みの独立確認**(最優先)— 「$q$ 奇 $\Rightarrow$ $4\nmid2q$ $\Rightarrow$ 分岐 3 の "established above" は分岐 2(読者演習)を指す」という私の読解が**誤読でないか**。ここが誤読なら本追補の第 1 の発見は消える(が、§E-F.3 の補完は無害に残る)。
2. **補題 THM44-odd の (c) 段**(CRT の 2 場合分け。とくに $p\mid n$ の場合に $\gcd(2m+1,2n)=1$ から $p\nmid2m+1$ を出す段)。
3. **補題 PROP41-EVEN-odd の (4.8) 適用条件** — $m$ 偶で $w=y^mg\in[G_n,G_n]$ となること($n$ 奇に依存)。$4\mid n$ で破れることの確認も。
4. **定理 GEN-COFINAL** の (DC) の必要性 — (DC) を落とすと何が壊れるか(私の理解: $S$ が整除共終でなければ、$S$ の外の $n$ について $K^{(s)}\subseteq K^{(n)}$ なる $s\in S$ が無く、補題 THM44-odd を適用する相手が消える)。
5. **系 FIVE-BYPASS の封印適合性** — 「$K^{(5)}$ の値に触れない形式的含意」という私の判断が規律上正しいか(**Sol へは量化緩和形のみ提示し、$K^{(5)}$ 名指し形は司令塔判断で伏せてよい**)。

### E-F.7.5 申し送り(司令塔へ)

1. ★ **正典 2405 Thm 4.4 の証明の穴は、著者へのエラッタ候補**である(結論は正しいと考えられるが、奇 $q$ 分岐の論証が循環的に読者演習を指している)。**外部連絡は司令塔の専権** — 本追補は事実の記録のみ。
2. **E1 ノート §2.1 の系 E1-S2′ の位置づけの訂正**(§E-F.6 の最終行)を E1 ノートにも反映するか。**E1 ノートは別文書なので erratum が要る** — 起票は司令塔判断。
3. ★ **系 FIVE-BYPASS の研究者確認**を求める。確認事項は 1 点のみ: 「**$\mathrm{GT}(K^{(5)})$ の genuine 性についての形式的含意を紙に書くことは封印に抵触しないか**」。抵触するとの判断なら §E-F.4.3 を削除し、**§E-F.4.1 のみで本追補は完結する**(数学的損失ゼロ)。
4. **【IHNEC-GAP-5】の射程点検**(起草者が grep 済・結果を先に報告する)—
   - **v1 §5.2 前件表の (THM44) 行の言明欄は「$\mathrm{Dih}$ **内** reduction 全射」と書かれており、$\mathrm{Dih}$ 全体(偶を含む)を主張している**。実際の**使用**は $\mathrm{Dih}^{\rm odd}$ 内部のみ(§E-F.2.3)。⟹ **言明欄を「$\mathrm{Dih}^{\rm odd}$ 内 reduction 全射」へ狭めるのが安全**(§E-F.6 の差替に含めた)。
   - **`docs/week1-定義ノート.md` L202 の較正 branch suite** は $(q,n)=(8,4),(36,12),(12,4),(18,3),(9,3)$ で「Thm 4.4 の証明分岐を被覆」と設計している。**$(18,3)$ は $q$ 偶・$4\nmid18$ = 読者演習分岐、$(9,3)$ は奇分岐**。⟹ **この較正スイートを回せば、未証明 2 分岐の実測的支持が得られる**(証明にはならないが、較正としては正しく設計されていた)。**起票は司令塔判断。**
   - 他の該当文書(`n12_goursat_v1.md` L260 等)は**参照リストへの掲載のみ**で前件として使っていない。
5. **名前衝突の記録**(§E-F.2.1 の ⚠ 枠)— **2401 Thm 4.4 と 2405 Thm 4.4 は別物**。規約台帳に「Thm 番号は論文 ID とセットで書く」を足すことを提案する。
5. **検算スクリプトの所在**: 追補 D.1.3 の規約に従い `search/probe/wac_v1/` に置いた。digest は §E-F.5。

---
---

# 【追記 F】(2026-08-01)— **系 FIVE-BYPASS の完全形登録**と位置づけの更新

> **位置づけ**: 本追補(E-F)への **erratum**(CV-10 additive 方式)。**§E-F.0〜§E-F.7 の本文は 1 バイトも改変していない**。抵触箇所は**本追記 F が優先**する。
> **認可**: **裁定 396**(2026-08-01 研究者一括認可)①「**札 F の $K^{(5)}$ 名指し: 認可 — 系 FIVE-BYPASS を $K^{(5)}$ 名指しの完全形で正式登録可(blind 規律判定 = 形式的含意・値非接触につき適合)**」。**裁定 399**(札 F 検収)が「委嘱が 396 より先行していたため確認待ち札のまま — **次波で登録指示**」と記録。**本追記がその履行**である。
> **さらに**: **裁定 398**(n=5 開封対決)で $K^{(5)}$ の封印は解除され、**裁定 398 → domain 復帰追補**(`docs/notes/fam_u_v1_addendum_domain_restore.md`)で FAM-U の定理領域も全奇数へ戻った。⟹ 本追記は**位置づけの更新**も併せて行う(§F.3)。
> **本追記は新しい数学を主張しない** — 系そのものは §E-F.4.3 で既に証明済(GEN-COFINAL の $n=5,\ s=15$ の場合)。変えるのは**札と位置づけ**である。**Sol 未監査**。

---

## F.1 ★ 正式登録(**§E-F.4.3 を置換**)

> ### 系 FIVE-BYPASS【**正式登録**・paper-proof candidate】
> $$\boxed{\ \mathrm{GT}_{\rm gen}(K^{(15)})=\mathrm{GT}(K^{(15)})\quad\Longrightarrow\quad\mathrm{GT}_{\rm gen}(K^{(5)})=\mathrm{GT}(K^{(5)})\ }$$
> **証明.** 定理 GEN-COFINAL(§E-F.4.1)の $n=5,\ s=15$ の場合($5\mid15$)。使う道具は **補題 THM44-odd**($R_{K^{(15)},K^{(5)}}$ の全射性・§E-F.3.2)と **補題 GEN-DESC**(genuine は reduction で押し出される・§E-F.1)の 2 本のみ。$\blacksquare$
>
> **格**: **paper-proof candidate**(**Sol 未監査**)。依存は §E-F.7.1 の GEN-COFINAL 行と同一 — すなわち **THM44-odd**(正典に証明が無い奇分岐の工房補完)と **PROP41-EVEN-odd**(その根)に相対的。
> **登録の認可**: **裁定 396 ①**(逐語は本追記冒頭)。

### F.1.1 置換される札(**逐条**)

| 箇所 | 旧 | ★ 新 |
|---|---|---|
| **§E-F.4.3 見出し** | 「(★ **研究者確認待ちの札 — 正式登録しない**)」 | ★ **正式登録済**(裁定 396) |
| **§E-F.4.3 の ⚠ 規律枠** 第 2 項「台帳・地図・便・他文書への登録は §E-F.4.1 の量化緩和形のみ / 本系は研究者確認まで本追補の内部にとどめ、引用しない」 | — | ★ **撤回**。**FIVE-BYPASS は台帳・地図・便・他文書から引用してよい** |
| **§E-F.4.3 の ⚠ 規律枠** 第 3 項「公開面では $K^{(5)}$ を名指さない形($S=\{$奇 $n\ge3\}\setminus\{5\}$)を使うこと」 | — | ★ **撤回**($K^{(5)}$ の封印は裁定 398 で解除)。**名指し形を使ってよい**。ただし**同値な言い換えとして依然有効**なので、量化緩和形で書きたい場面ではそちらを使ってよい |
| **§E-F.4.3 の ⚠ 規律枠** 第 1 項「$\mathrm{GT}(K^{(5)})$ の値・元・座標・位数・測定値に一切触れない形式的含意」 | — | ★ **事実として維持**(本系は実際に値に触れていない)。**ただし義務ではなくなった** |
| **§E-F.7.1 格付け表 FIVE-BYPASS 行** | 「★ **研究者確認待ち・正式登録せず**」 | ★ **paper-proof candidate(正式登録済・裁定 396)・Sol 未監査** |
| **§E-F.7.5 申し送り 項 3**(「系 FIVE-BYPASS の研究者確認を求める。抵触するとの判断なら §E-F.4.3 を削除」) | — | ★ **回答済 = 抵触しない**(裁定 396 の blind 規律判定)。**§E-F.4.3 は削除せず、完全形で登録** |
| **本追補冒頭「封印遵守」ブロック**の「正式登録は §E-F.4.1 の量化緩和形のみ」 | — | ★ **撤回**(冒頭ポインタで既に告知) |

---

## F.2 定理 GEN-COFINAL 側への影響(**ゼロ**)

- **§E-F.4.1 の定理 GEN-COFINAL は無変更**。FIVE-BYPASS はその**系**であり、**主定理の格・射程・証明のいずれにも触れない**。
- **系 CHAIN・系 FAKE-LIFT・系 GEN-COFINAL-(ii) も無変更**。
- ⟹ **本追記で新しく登録されるのは「系 1 本の札」だけ**である。

---

## F.3 ★ 位置づけの更新(**§E-F.4.4 の「買うもの」欄を置換**)

### F.3.1 旧位置づけ(**失効**)

> **§E-F.4.4「買うもの」(旧)**: 「ML-ODD (iii) の証明は、**任意の有限個の奇数の窓に一度も入らずに**閉じられる ⟹ **『封印($n=5$ 非接触)と ML-ODD (iii) の証明可能性は両立する』** — これが札 F の実質的な内容である」
> ★ **この値打ちは消えた。** **$K^{(5)}$ の封印が裁定 398 で解除された**以上、「封印を迂回する」ことに実用価値はない。

### F.3.2 ★ 新しい位置づけ(**3 点**)

| # | 位置づけ | 内容 |
|---|---|---|
| **(a)** | **GEN-COFINAL の系**(構造的位置) | FIVE-BYPASS は **(DC) を満たす $S$ が $5$ を含まなくてよい**ことの最小の具体例である。**主定理の射程を示す例示**として残る(封印とは無関係に、$S$ から任意の有限集合を落としてよいことの見本) |
| **(b)** | ★ **独立の整合性検査**(**二窓にまたがる fail-closed**) | 「$K^{(15)}$ 全 genuine」と「$K^{(5)}$ に fake」が**同時に出たら矛盾**である。⟹ 将来 $K^{(5)}$ と $K^{(15)}$ の双方に計算が及んだとき、**実装バグ・窓の取り違え・reduction の向き違いを捕まえる検査**になる。系 FAKE-LIFT の $n=5,s=15$ 版(fake は $5\to15$ へ**上向きに**伝播)が同じ検査の対偶 |
| **(c)** | ★★ **戦略の反転**(封印解除の最大の帰結) | **系 FAKE-LIFT により $\mathcal F$ は整除順序で上に閉じる ⟹ 探索すべきは極小元**(§E-F.4.1 末の哨戒 5 点目)。$\{n$ 奇 $\ge3\}$ の整除順序の**極小元は奇素数** $3,5,7,11,\dots$。$K^{(3)}$ は既決(定理 K3・framework-conditional)ゆえ、**次の極小元は $n=5$** であり $\lvert\mathrm{GT}(K^{(5)})\rvert=2\cdot5\cdot\varphi(5)=40$ — **極小元の中で最小**。⟹ **封印が解けた今、正しい向きは迂回ではなく直撃**である |

> ### ★ 一行で
> **迂回は不要になり、迂回の根拠だった定理(FAKE-LIFT の極小元原理)が、逆に「$K^{(5)}$ を最優先で撃て」と言っている。** $\lvert\mathrm{GT}(K^{(15)})\rvert=240$ に対し $\lvert\mathrm{GT}(K^{(5)})\rvert=40$ — **6 倍の差は、いま順方向に効く**。

### F.3.3 ⚠ 過大評価の禁止(**§E-F.4.4 の「買わないもの」は全て維持**)

1. **「全 shadow が genuine」は有限深度で決定できない**(【IHNEC-GAP-1】・(COR54))。⟹ **$K^{(5)}$ が小さいことは「$K^{(5)}$ を有限計算で落とせる」を意味しない**。小ささが効くのは**有限に決まる部分**(shadow の列挙・合成表・reduction・$\mathfrak F_0$ 等)だけである。
2. **FAM-U の domain が $n=5$ へ復帰したこと**(`fam_u_v1_addendum_domain_restore.md`)は、$\mathrm{ord}([u_5]_{10})=5$ を**主張してよくした**が、そこから $\mathrm{Ih}_{K^{(5)}}$ の全射性へは **ASM 追記 A / v2 §V.5 の矢印 (b)(c-2)(c-n)(d)** を跨ぐ必要がある。**(c-n) は FAITH 条件付きで循環**(F96-1.6)。⟹ **二つの線が $n=5$ で交わったことは、どちらの線の障壁も下げない**。
3. **本系は FAM-U を入力に使っていない**(純粋に有限群論・§E-F.1 と §E-F.3 のみ)。⟹ 逆向きの依存も無い。

---

## F.4 FINDING(追記 F の分)

| # | 格 | 内容 |
|---|---|---|
| **FB-1** | ★ **札の確定** | **系 FIVE-BYPASS を $K^{(5)}$ 名指しの完全形で正式登録**(裁定 396 ①)。格は **paper-proof candidate・Sol 未監査**(GEN-COFINAL と同じ依存 = THM44-odd / PROP41-EVEN-odd 相対)。§E-F.4.3 の規律枠 3 項のうち**引用禁止と名指し禁止を撤回**、値非接触は**事実として維持・義務としては解除** |
| **FB-2** | ★ **位置づけの転換** | 「$n=5$ の肩代わり」→「**(a) GEN-COFINAL の系(射程の見本)/ (b) 二窓にまたがる整合性検査 / (c) 戦略の反転**」。**封印解除により迂回の実用価値は消滅**した |
| **FB-3** | ★★ **戦略の帰結(実務的に最重要)** | FAKE-LIFT の極小元原理 + 封印解除 ⟹ **$K^{(5)}$ は整除順序の極小元(奇素数)であり、既決の $K^{(3)}$ を除けば $\lvert\mathrm{GT}\rvert=40$ で最小** ⟹ **哨戒の最優先標的**。「$K^{(15)}$ 経由の迂回」は**推奨しない**(6 倍大・前件が偽になりやすい側) |
| **FB-4** | ⚠ **過大評価の予防** | 【IHNEC-GAP-1】は不変(有限深度で全 genuine は決まらない)。FAM-U の $n=5$ 復帰と本線の交差は**どちらの障壁も下げない**(矢印 (b)(c-n)(d) は不変) |

---

## F.5 申し送り

1. **司令塔へ**: **`docs/地図.md` の P1 行**が「genuine 層は**系 FIVE-BYPASS = $K^{(15)}$ 経由の封印非接触迂回が候補**(裁定 394・**研究者確認まで量化緩和形のみ登録**)」と書いている(L32)。⟹ **登録札の更新**(確認済・完全形登録)と、**§F.3.2 (c) の戦略反転**(迂回候補 → $K^{(5)}$ 直撃)の反映が要る。**地図は司令塔の文書なので本追記は触っていない**。
2. **司令塔へ**: 同じく **L52 の ML-ODD 行**「量化は札 F で $S=\{$奇 $n\ne5\}$ へ緩和可 = FIVE-BYPASS・$K^{(15)}$ が $n=5$ を肩代わり」も、**肩代わりの必要は消えた**旨の更新対象。
3. **Sol へ(便 99)**: **監査点 F-1** — §F.3.2 (c) の「極小元 = 奇素数、$K^{(3)}$ 既決ゆえ次は $K^{(5)}$、$\lvert\mathrm{GT}(K^{(5)})\rvert=40$ が最小」という戦略推論。$\mathcal F$ の上向き閉性(FAKE-LIFT)から**探索は極小元に限ってよい**という段が、**$\mathcal F$ が空である可能性**(= ML-ODD (iii) が真)と両立して意味を持つか — 私の読みは「**極小元を潰しても (iii) は出ない**(無限個ある)が、**反例を探すなら極小元だけ見ればよい**」という非対称であり、**探索の向きにのみ効く**。この非対称の記述で正しいか。
4. **Sol へ(便 99)**: **監査点 F-2** — 本追記が変えたのは**札と位置づけのみ**で、**§E-F.4.1 の定理 GEN-COFINAL・その証明・§E-F.3 の 2 補題には一切触れていない**(§F.2)。この分離でよいか。

**【文献要請】**: **本追記からの新規はゼロ。**
