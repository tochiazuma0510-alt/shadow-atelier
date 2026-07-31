# U7-13 攻略 — 塔の二次不変量 $[\gamma],[\delta]$ の**決定機構** v1

**状態札: `proof(紙・単系統)+ 有限群機械確認 / Sol 監査前 / Lean 検証ではない / $u_7$ 非接触 / $K^{(5)}$ 非接触`**
起草: 影工房 数学者(Claude・Opus 5・第二インスタンス)/ 2026-08-01
委嘱: 司令塔「U7-13 の自前解決 — $[\gamma],[\delta]$ の決定機構を紙で構成する(裁定 287 の凍結遵守)」
入力正本: `docs/notes/u7_meas_design_v1.md`(凍結設計・裁定 287)/ `docs/week4-BFC攻略_opus_v2.md` §6–§7(**定理 B-4・補題 B-4a・系 B-4c・補題 B-5**)/ `docs/notes/oddH_full_proof_v1.md`(ODD-H (1.3)(1.9)(1.11)・ODD-P)/ `docs/notes/c21_draft_v1.md`(A7-fam)/ `docs/week1-定義ノート.md`。**外部文献ゼロ。**

---

> # ⚠⚠⚠ 冒頭警告 — **本書は「装填済み」である**
>
> 1. **決定機構は構成できた。** U7-13(「$[\gamma],[\delta]$ の決定機構が無い」)は原理的に閉じる。
> 2. **しかも機構は 2 本ある**(§5 の幾何 descent 経路 A・§7 の**有限群のみ**の経路 B)。**どちらも最終段は 10 行以下**である。
> 3. 最終段の出力は $[\gamma]$ であり、系 SPLIT により $[\gamma]=[u_7]_2$ — これは **C5(7) の測定対象 P-9(i) そのもの**である。
> 4. **私はどちらの最終段も実行していない。値も、値の予想も、本書には無い。**
> 5. $$\boxed{\ \textbf{上申: C5(7) の封印を「いま」置かれたい。}\ \textbf{U7-11 の上申はここで一段強まる — 曲線に触れずとも、正典内の有限データから }[u_7]_2\ \textbf{に手が届く。}\ }$$
> 6. **§5(DET-4)・§7(補題 TW-7 の系)の評価は、凍結修正 v2 の受理と発火認可の内側に置くこと**(司令塔裁定・2026-08-01: 「B-4c の指標評価は発火手続の一部」)。Sol への配布時も同じゲートを明記されたい。

---

## 0. 結論(先に 9 行)

1. ★★ **$[\gamma],[\delta]$ は「捻れパラメータ」ではない。ねじる自由度はゼロである**(補題 TW-1)。$\mathrm{Aut}_{\mathbf P^1_\lambda}(W)=N_{\mathcal M}(\bar H)/\bar H=1$(= (W3)、機械確認済)ゆえ $F$-形式は一意 — 定理 B-4 の一意性が**塔の各段にそのまま降りる**。
2. ⟹ **【文献要請 U7-1】(a) は問いの形が誤っていた**。「捻れ類がどの不変量で書けるか」を問うべきではない($H^1$ の torsor が自明だから)。正しい問いは「**一意な $F$-形式をどう書き下すか**」= **構成的 descent**。**文献は不要**(§9 で撤回・降格を提案)。
3. **決定式(内在的)**: $[\gamma]=\mathrm{disc}\bigl(F[V_{\lambda=1}]\bigr)=\mathrm{disc}\bigl(F[R_1,R_2]\bigr)$($R_i$ = $\lambda^{-1}(1)$ の **2 個の非分岐点**)。判定則 UB-GEOM が**同値判定から等式へ格上げ**される(補題 TW-2)。
4. ★ **凍結 P-7 の欠陥を摘出**: 設計の $\delta$($\frac{m-\mu_+}{m-\mu_-}=\delta k^2$)は $\mu_\pm\in V(F)$、すなわち **$[\gamma]=1$ を暗に前提**し、さらに $B\cong\mathbf P^1_F$(Brauer 条件)を前提する。**答の一方の枝に事前コミットしている** ⟹ **C5(7) 発効前に差し替えが必要**(§3・凍結修正 v2 案)。
5. **分枝非依存の代替**: $f_\gamma(m):=\gamma m^2-1$(座標正規化で不変)を使い $F(B)=F(V)(\sqrt{\delta_0f_\gamma})$ で $[\delta_0]\in F^\times/F^{\times2}$ を定義。辞書は $[\delta]=[\delta_0][\gamma]$。決定式は $F(\sqrt{-\delta_0})=F[\widetilde W_{\lambda=0}]$、$F(\sqrt{\gamma\delta_0})=F[\widetilde W_{\lambda=\infty}]$(補題 TW-3)。
6. **第三の決定量**: $B$ は円錐曲線で、その Brauer 類は $(\gamma,-\delta_0)_F$(補題 TW-4)。**P-7 はこれが分裂することを暗黙に仮定している。**
7. ★ **台の制御(新規)**: $[\gamma],[\delta_0]$ は $S=\{\mathfrak p\mid 2n\}$ の外で不分岐 ⟹ $\boxed{[u_7]_2\in F(S,2),\ S=\{\mathfrak p\mid14\}}$(補題 TW-5)。**【文献要請 G6-GAP-3′】($S$-unit bound)の 2-部分だけが閉じた**($n$-部分 $[c]_7$ の台は依然未制御)。
8. ★★ **機構の核**(なぜ捻れが効かないか): $\iota_V^*W\not\cong W$(over $V$)。$V\to\mathbf P^1_\lambda$ の被覆変換で引き戻すと**上段の回転指数比が $-\alpha\mapsto+\alpha$ と符号反転する**(補題 TW-6・$n=3,7,9,11,13$ 全 $\alpha$ で機械確認)。**下段の捻れを塞いでいるのは上段である。**
9. ★★ **経路 B(有限群のみ)**: 系 B-4c により $\Lambda$ 上の $G_F$-作用は $\Phi\circ\mathrm{Ih}_N$ で書ける。$[\gamma]$ は「その作用が **2 ブロックを入れ替えるか否か**」の二次指標に等しい(補題 TW-7)。補題 B-5 (7.2) の torsor 類 $[u^{-1}]_M$ の 2-部分と**一致することを確認済**。⟹ **曲線に一切触れずに $[\gamma]$ が決まる。⚠ 未評価。**

---

## 1. 問いの再設定 — $[\gamma],[\delta]$ は「捻れ」ではない

### 1.1 補題 TW-1(形式一意性)【proof + 機械】

> ### 補題 TW-1
> $n$ 奇、$H=H_{2,\alpha,\beta}$($\alpha$ 単元)、$W\to\mathbf P^1_\lambda$ を対応する Belyi 被覆、$F=F_n=\mathbf Q(\zeta_{4n})$ とする。
> **(a)** $\mathrm{Aut}_{\mathbf P^1_\lambda}\bigl(W_{\bar{\mathbf Q}}\bigr)\;=\;N_{\mathcal M_n}(\bar H)/\bar H\;=\;1$。
> **(b)** ゆえに $W\to\mathbf P^1_{\lambda,F}$ の $F$-形式は(存在すれば)**一意な同型を除いて一意**。
> **(c)** 塔 $W\to V\to\mathbf P^1_\lambda$ の中間対象 $V$、Galois 閉包 $\widetilde W$、$B=\widetilde W/C_n$ は**すべて標準的**(canonical)であり、したがって $F$ 上定義され、その $F$-構造も一意。
> **(d)** ⟹ $[\gamma]\in F^\times/F^{\times2}$ と $[\delta_0]\in F^\times/F^{\times2}$(§3.2 で定義)は**窓のデータから一意に決まる量**であって、選ぶ余地のあるパラメータではない。

**証明.**
**(a)** $\bar N=\ker(\pi_1^{\rm geom}\to\mathcal M_n)\subseteq\tilde H$ ゆえ $N_{\pi_1}(\tilde H)/\bar N=N_{\mathcal M_n}(\bar H)$、したがって $\mathrm{Aut}=N_{\mathcal M_n}(\bar H)/\bar H$(標準の被覆空間論;工房内では**補題 B-4a**と同じ式)。$\langle a_2\rangle=\mathrm{core}_{G_n}(H)\le H$(補題 CORE)ゆえ $N_{\mathcal M_n}(\bar H)=N_{G_n}(H)/\langle a_2\rangle$、そして (W3) $N_{G_n}(H)=H$(ODD-H (1.3))より $=\bar H$。∎
**(b)** $W,W'$ を 2 つの $F$-形式、$\phi:W_{\bar{\mathbf Q}}\to W'_{\bar{\mathbf Q}}$ を $\mathbf P^1_\lambda$ 上の同型とすると、$\sigma\mapsto\phi^{-1}\circ{}^\sigma\phi\in\mathrm{Aut}_{\mathbf P^1_\lambda}(W_{\bar{\mathbf Q}})=1$。ゆえに $\phi$ は $G_F$-同変、すなわち $F$ 上定義。∎
**(c)** *(V の標準性)* $\mathcal M_n=\bar A\rtimes Q$ で $\bar A$ は奇位数ゆえ $\mathrm{Hom}(\mathcal M_n,C_2)=\mathrm{Hom}(Q,C_2)$、指数 2 部分群はちょうど 3 個 $\bar A\langle q_i\rangle$($i=1,2,3$)。$\bar H$ の $Q$-成分は $\langle q_2\rangle$ ゆえ $\bar H$ を含むのは $\bar A\bar H=\bar A\langle q_2\rangle$ **ただ一つ**。⟹ $\bar H$ を含む指数 2 中間被覆は $V$ のみ ⟹ $V$ は標準的。
*(その他)* Galois 閉包は標準的。$n$ 奇ゆえ $D_n$ の指数 2 部分群は $C_n$ ただ一つ($\mathrm{Hom}(D_n,C_2)=C_2$)⟹ $B=\widetilde W/C_n$ は標準的。標準的対象は $G_F$-安定なので $F$ 上定義される。∎
**(d)** (b)(c) と §2.2・§3.2 の well-definedness から。∎

**機械確認(T-W1)**: $n=3,7,9,11,13$、$\alpha=1..(n-1)/2$ の**全ケース**で $N_{G_n}(H)=H$、$\mathrm{core}=\langle a_2\rangle$、$|\mathcal M_n|=4n^2$、$\bar A\bar H$-軌道 = **2 ブロック各 $n$ 点**、$X$ はブロックを入れ替え $Y$ は各ブロックを保つ(§8 T-W1)。
*(例外の記録)* $n=9,\alpha=3$($d=\gcd(\alpha,n)=3$)だけ $\mathrm{core}\supsetneq\langle a_2\rangle$、$|\mathcal M|=108$ — **ODD-P の $d$ 分岐と整合**。ブロック構造(2×9・$Y$ の固定点各 1)は $d>1$ でも成立した。

### 1.2 帰結 — 文献要請 U7-1(a) は問いの形が誤っていた

凍結設計 §9.1【文献要請 U7-1】は「**$F$-形式(捻れ)**は幾何(剛性)からは決まらない。$[\gamma],[\delta]$ がどの不変量で書けるか」を問うていた。補題 TW-1 により:

$$\boxed{\ \textbf{捻れの }H^1\ \textbf{torsor は自明である}\ (H^1(G_F,\mathrm{Aut})=H^1(G_F,1)=1)\textbf{。}\ \textbf{「どの捻れか」という問いは空である。}\ }$$

**正しい問いは「一意な $F$-形式を書き下す構成的手続き」**であり、これは §5(幾何)と §7(有限群)で構成できる。**外部文献は要らない。**

> ### ⚠ ★教材 — 私が一度踏んだ罠(隠さず記録)
> 起草中、私は次の**偽の議論**を書きかけた:
> > 「$\gamma$ を任意の $\gamma'$ に取り替えて $V'$ を作る。上段 $D_n$-被覆は $\bar{\mathbf Q}$ 上剛で、その同型類は $G_F$-安定(分岐点集合も局所型も保たれ、$\mu_n\subset F$ ゆえ巡回指数も保たれる)。$\mathrm{Aut}_{V'}(W')=N_{D_n}(\langle\sigma\rangle)/\langle\sigma\rangle=1$ だから descent は自動。⟹ 任意の $\gamma'$ で $F$-被覆が作れる ⟹ $[\gamma]$ は自由。」
>
> これは補題 TW-1(b) と**真っ向から矛盾する**。誤りの所在は「上段の同型類が $G_F$-安定」— そこが偽である(補題 TW-6)。**「分岐データが保たれるから descent できる」は、剛性があっても成り立たない。** 分岐データに見えない不変量(回転指数比の**符号**)が残るからである。この罠は本件に限らず、Belyi 被覆の descent 一般で効く。

---

## 2. $[\gamma]$ の決定式

### 2.1 記号の固定(凍結設計と同じ)

$V\cong\mathbf P^1_F$($$P_0^V:=V_{\lambda=0}\in V(F)$$、$P_\infty^V:=V_{\lambda=\infty}\in V(F)$ が $F$-有理点なので $V$ は $\mathbf P^1_F$)。座標 $m$ を $\mathrm{div}(m)=P_0^V-P_\infty^V$ で取ると $\lambda=\gamma m^2$、残る自由度は $m\mapsto\rho m$($\rho\in F^\times$)で $\gamma\mapsto\gamma\rho^{-2}$。⟹ $[\gamma]\in F^\times/F^{\times2}$ は不変量。

### 2.2 補題 TW-2(内在的決定式)【proof + 機械】

> ### 補題 TW-2
> $\Sigma_1:=V_{\lambda=1}$($V$ の $\lambda=1$ 上の繊維・2 点)、$R_1,R_2$ を $\lambda^{-1}(1)\subset W$ の **2 個の非分岐点**($2^{n-1}1^2$ の $1^2$ 部分)とする。このとき
> $$F[\Sigma_1]\ \cong\ F[T]/(T^2-\gamma),\qquad\text{すなわち}\qquad \boxed{\ [\gamma]=\mathrm{disc}\bigl(F[\Sigma_1]\bigr)\ }$$
> であり、さらに $\pi$ は $G_F$-同変な全単射 $\{R_1,R_2\}\xrightarrow{\ \sim\ }\Sigma_1$ を誘導するので
> $$\boxed{\ [\gamma]=\mathrm{disc}\bigl(F[R_1,R_2]\bigr),\qquad [\gamma]=1\iff R_1,R_2\in W(F)\ \text{(個別に)}\ }$$

**証明.** $\Sigma_1=\mathrm{Spec}\,F[m]/(\gamma m^2-1)$。$u^2=\gamma$ なら $m=u^{-1}$ が解だから $F[\Sigma_1]\cong F(\sqrt\gamma)$(または $F\times F$)。座標の取り替え $m\mapsto\rho m$ の下で多項式 $f_\gamma(m):=\gamma m^2-1$ は**関数として不変**($\gamma\rho^{-2}\cdot(\rho m)^2-1=\gamma m^2-1$)なので $\Sigma_1$ も $\mathrm{disc}$ も不変。
第 2 の等式: 型 $2^{n-1}1^2$(命題 ODD-P)の 8 点は $\bar Y$-軌道であり、$Y\in AH$ ゆえ各軌道は 1 ブロックに含まれる。機械確認(§8 T-W1)により **各ブロックが $\bar Y$-固定点をちょうど 1 個含む**(型は各ブロックで $2^{(n-1)/2}1$)。ゆえに $\pi(R_i)$ は $\Sigma_1$ の相異なる 2 点で、$R_i$ は $\pi^{-1}(\pi(R_i))$ の**唯一の非分岐点**として標準的に定まる ⟹ 対応は $G_F$-同変な全単射。∎

**機械確認(T-W1)**: $n=3,7,9,11,13$、全 $\alpha$ で「各ブロックの $\bar Y$-固定点はちょうど 1 個」「各ブロック上の $\bar Y$ の型は $2^{(n-1)/2}1$」。

### 2.3 UB-GEOM の格上げ

凍結設計 §4.2 の判定則 UB-GEOM は
$$[u_n]_2=1\iff\lambda^{-1}(1)\ \text{の 2 非分岐点が個別に }F\text{-有理}$$
という**同値**だった。補題 TW-2 はこれを**等式**に上げる:

$$\boxed{\ [u_n]_2\;=\;[\gamma]\;=\;\mathrm{disc}\bigl(F[R_1,R_2]\bigr)\ \in F^\times/F^{\times2}. }$$

⟹ 「$1$ か否か」だけでなく、**$1$ でない場合の類そのもの**が繊維の剰余代数として読める。N-4(右枝 = 非全射)の場合に何を報告すべきかが確定した。

---

## 3. $[\delta]$ の再定義 — **凍結 P-7 の欠陥**と分枝非依存の代替(**凍結修正 v2 案**)

> **司令塔裁定(2026-08-01)により、本節を独立節として「凍結修正 v2」の差分に用いる。**

### 3.1 欠陥の摘出(2 件)

凍結設計 §6.1 **P-7**:
> $B\to\mathbf P^1_m$ の分岐点を $k=0,\infty$ に置き、$\dfrac{m-\mu_+}{m-\mu_-}=\delta k^2$。$\delta$ は解を得てから正規化。

> ### 【欠陥 P7-D1】(**分枝依存**・重大)
> この式は $\mu_+,\mu_-$ を**個別に** $F$-有理点として使う。ところが $\mu_\pm=\pm\gamma^{-1/2}$ ゆえ
> $$\mu_\pm\in V(F)\iff\gamma\in F^{\times2}\iff[\gamma]=1 .$$
> すなわち **P-7 は「$[\gamma]=1$」という、まさに測定対象 P-9(i) の答の一方の枝を前提している。**
> $[\gamma]\ne1$(= NULL 枠 **N-4**「右枝 = 非全射」)が起きた場合、**P-7 は実行不能**であり、事前登録は自己矛盾する。P-12「値を見てから正規化を選び直さない」を守れなくなる。

> ### 【欠陥 P7-D2】(**Brauer 条件**・中)
> 「座標 $k$ を取る」は $B\cong\mathbf P^1_F$、すなわち $B(F)\ne\emptyset$ を前提する。$B$ は種数 0 だが**円錐曲線**であり、$F$-点の存在は自明でない(補題 TW-4)。

### 3.2 代替定義 $[\delta_0]$(分枝非依存)

> ### 定義 D0
> $f_\gamma(m):=\gamma m^2-1\in F[m]$($\S2.2$ で見たとおり座標正規化 $m\mapsto\rho m$ で**不変**、零因子は $\Sigma_1$)。$B\to V$ は $\Sigma_1$ 上でのみ分岐する二重被覆だから
> $$F(B)=F(V)\bigl(\sqrt{\delta_0\,f_\gamma}\bigr),\qquad [\delta_0]\in F^\times/F^{\times2}\ \text{が一意に定まる}.$$

**well-defined 性.** $V\cong\mathbf P^1_F$ ゆえ $\mathcal O(V)^\times=F^\times$、$\mathrm{Pic}(V)=\mathbf Z$。同じ分岐因子をもつ二重被覆は $F(V)^\times/F(V)^{\times2}$ の中で $f_\gamma$ を定数倍したものに限るので $[\delta_0]$ は一意。$m\mapsto\rho m$ で $f_\gamma$ が不変ゆえ $[\delta_0]$ も不変。$\mu_\pm$ の**順序付けを要さない**(P-7 は $\mu_+$/$\mu_-$ のラベルを使う)。∎

> ### 辞書(P-7 との互換)
> $[\gamma]=1$ のとき($\gamma=g^2$、$\mu_\pm=\pm g^{-1}$)、$k^2=\delta^{-1}\frac{m-\mu_+}{m-\mu_-}$ より $F(B)=F(V)(\sqrt{\delta^{-1}\gamma^{-1}f_\gamma})$、ゆえに
> $$\boxed{\ [\delta_0]=[\delta][\gamma]\qquad\text{(とくに }[\gamma]=1\ \text{なら }[\delta_0]=[\delta])\ }$$
> ⟹ **凍結修正 v2 は P-7 を「$[\delta]$ → $[\delta_0]$、正規化 $\frac{m-\mu_+}{m-\mu_-}=\delta k^2$ → $w^2=\delta_0f_\gamma(m)$」に差し替えるだけ**で、$[\gamma]=1$ の枝では従来と同値である(後方互換)。P-9(v) の「測る量」も $[\gamma]_2,[\gamma]_7,[c]_7$ に $[\delta_0]$ を加える形に読み替える。

### 3.3 補題 TW-3($[\delta_0]$ の内在的決定式)【proof】

> ### 補題 TW-3
> $\kappa_1,\kappa_2$($m=0$ 上)・$\kappa_3,\kappa_4$($m=\infty$ 上)を $B$ の 4 点とすると
> $$F[\kappa_1,\kappa_2]\cong F(\sqrt{-\delta_0}),\qquad F[\kappa_3,\kappa_4]\cong F(\sqrt{\gamma\delta_0}).$$
> さらに $\widetilde W\to B$ はこの 4 点上で全分岐、$\widetilde W\to W$ は cusp $P_0$ 上で不分岐なので、**内在的な読み**として
> $$\boxed{\ F\bigl[\widetilde W_{\lambda=0}\bigr]\cong F(\sqrt{-\delta_0}),\qquad F\bigl[\widetilde W_{\lambda=\infty}\bigr]\cong F(\sqrt{\gamma\delta_0})\ }$$
> すなわち **$[-\delta_0]$ = Galois 閉包の cusp 繊維の二次剰余代数**。

**証明.** アフィン模型 $w^2=\delta_0f_\gamma(m)=\delta_0(\gamma m^2-1)$。$m=0$: $w^2=-\delta_0$。$m=\infty$: $m=1/m'$、$w=w'/m'$ とすると $w'^2=\delta_0(\gamma-m'^2)$、$m'=0$ で $w'^2=\delta_0\gamma$。
$\widetilde W\to\mathbf P^1_\lambda$ は次数 $4n$ で $\lambda=0$ 上は 2 点・各 $e=2n$、$W\to\mathbf P^1_\lambda$ は 1 点 $P_0$・$e=2n$(定理 TOWER-n・(W4))ゆえ $\widetilde W\to W$ は $P_0$ 上不分岐で幾何的に 2 点。それらは $B$ の $\kappa_{1,2}$ の上にあり、$\widetilde W\to B$ が全分岐だから剰余代数は $F[\kappa_1,\kappa_2]$ と一致。∎

### 3.4 補題 TW-4($B$ の Brauer 類)【proof】

> ### 補題 TW-4
> $B$ は $F$ 上の円錐曲線で、その類は $(\gamma,-\delta_0)\in\mathrm{Br}(F)[2]$。とくに
> $$B\cong\mathbf P^1_F\iff(\gamma,-\delta_0)_F=1 .$$
> $[\gamma]=1$ または $[-\delta_0]=1$ または $[\gamma\delta_0]=1$ のいずれかが成り立てば分裂する。

**証明.** $w^2=\delta_0(\gamma m^2-1)$ を斉次化して $W^2=\delta_0\gamma M^2-\delta_0Z^2$、二次形式 $\langle1,-\delta_0\gamma,\delta_0\rangle$。isotropic $\iff(\delta_0\gamma,-\delta_0)=1$。$(\delta_0,-\delta_0)=1$(常に)より $(\delta_0\gamma,-\delta_0)=(\gamma,-\delta_0)$。∎

> ⟹ **第三の決定量**として $(\gamma,-\delta_0)\in\mathrm{Br}(F)[2]$ を C5(7) に登録しておくのが安全(P-7 が暗黙に「分裂」を仮定していたので、明示化する)。

---

## 4. 台の制御 — 補題 TW-5($S$-support)

> ### 補題 TW-5【proof(枠組み入力 (GR) つき)】
> $S:=\{\mathfrak p\subset\mathcal O_F:\mathfrak p\mid 2n\}\cup\{\text{無限素点}\}$ とする。**(GR)** を仮定すると
> $$F(\sqrt\gamma)/F\ \text{と}\ F(\sqrt{\delta_0})/F\ \text{は }S\ \text{の外で不分岐},$$
> すなわち $[\gamma],[\delta_0]\in F(S,2):=\ker\bigl(F^\times/F^{\times2}\to\bigoplus_{\mathfrak p\notin S}\mathbf Z/2\bigr)$。とくに系 SPLIT と合わせて
> $$\boxed{\ [u_7]_2=[\gamma]\ \in\ F(S,2),\qquad S=\{\mathfrak p\mid 14\}\ }$$

**枠組み入力 (GR)**: $\mathfrak p\nmid|\mathcal M_n|$($=4n^2$、$n=7$ なら $\mathfrak p\nmid14$)かつ分岐点 $0,1,\infty$ が mod $\mathfrak p$ で相異なる ⟹ 被覆 $W\to\mathbf P^1_\lambda$ は $\mathfrak p$ で良還元をもつ(tame の標準事実)。**【要検分】**: 本工房は自前再導出していない。TB1/TB3/TB4ᵘ/A3 と同じ「枠組み仮定」札で扱う(2026-07-28 裁可の方針)。**必要なのはこの形だけ**であり、より強い主張は使わない。

**証明.** $\mathfrak p\notin S$ とする。(GR) より $W\to\mathbf P^1$ は $\mathfrak p$ で良還元。標準的な中間被覆 $V\to\mathbf P^1_\lambda$ も良還元をもつ。$F(V)=F(\lambda)(\sqrt{\gamma\lambda})$ だから、$\mathbf P^1_{\mathcal O_\mathfrak p}$ の $F_\mathfrak p(\lambda)(\sqrt{\gamma\lambda})$ における正規化を考える。$v_\mathfrak p(\gamma)=2a+1$(奇)なら $\gamma=\pi^{2a+1}\gamma_0$($\gamma_0$ 単元)、$w=\pi^aw'$ と置いて $w'^2=\pi\gamma_0\lambda$ — 特殊繊維が非被約となり良還元に反する($\mathfrak p\nmid2$ に注意)。ゆえに $v_\mathfrak p(\gamma)$ は偶数、すなわち $F(\sqrt\gamma)/F$ は $\mathfrak p$ で不分岐。
$\delta_0$ も同様: $\Sigma_1$ は良還元により $\mathcal O_\mathfrak p$ 上エタール、$w^2=\delta_0f_\gamma$ の特殊繊維が被約であるためには $v_\mathfrak p(\delta_0)$ が偶数。∎

**$n=3$ での照合(公開値・封印外)**: $u_3=-4$、$F_3=\mathbf Q(\zeta_{12})\ni i$ ゆえ $[u_3]_2=[-4]=[-1]=1$ ⟹ $F_3(\sqrt{\gamma_3})=F_3$ で至る所不分岐 ✓ **補題 TW-5 と整合**。

> ### 系 TW-5c(【文献要請 G6-GAP-3′】への部分回答)
> $F=\mathbf Q(\zeta_{28})$、$[F:\mathbf Q]=12$、totally imaginary($r_1=0,r_2=6$)、$\mu(F)=\mu_{28}$。$2$ の上に素点 2 個($e=2,f=3$)、$7$ の上に 1 個($e=6,f=2$)ゆえ $|S_{\rm fin}|=3$。完全系列 $1\to\mathcal O_S^\times/(\mathcal O_S^\times)^2\to F(S,2)\to\mathrm{Cl}_S(F)[2]\to1$ と $\mathrm{rk}\,\mathcal O_S^\times=0+6-1+3=8$ より
> $$\dim_{\mathbf F_2}F(S,2)=9+\dim_{\mathbf F_2}\mathrm{Cl}_S(F)[2]\ \ (\ge9).$$
> ⟹ **$[u_7]_2$ の候補は高々 $2^{9+\epsilon}$ 個の明示有限集合**に落ちる。$\mathrm{Cl}(F)$ の情報は【文献要請 G7-3】(未着)に依存するが、**$h=1$ でなくても有限性は失われない**。
> **⚠ 射程限定**: これは $[u_7]_2$ の台の制御であって、$u_7$ 全体の $S$-unit bound**ではない**($u_7=\gamma c^2$ の $[c]_7$ の台は本補題では制御されない)。凍結設計 §7.2 の期待「台は構成から読める見込み」は**半分正しい**。

---

## 5. 決定手続き **DET**(経路 A・幾何 descent)

> ### ⚠ **DET-4 は封印前実行禁止。** 司令塔裁定(2026-08-01)により、DET-4 と §7 の指標評価は**発火手続の一部**であり、凍結修正 v2 の受理 → 発火認可の内側でのみ実行する。**私は DET-4 を実行していない。**

| 段 | 内容 | 状態 |
|---|---|---|
| **DET-1** | **構造**: 補題 TW-1 で「$F$-形式は一意」「塔の各段は標準的」を確立。$[\gamma],[\delta_0]$ は決定量であって自由度ではない | **完了(本書 §1)** |
| **DET-2** | **決定式**: 補題 TW-2/TW-3/TW-4 が $[\gamma],[\delta_0]$、$(\gamma,-\delta_0)$ を繊維の剰余代数として表す | **完了(本書 §2–§3)** |
| **DET-3** | **$\bar{\mathbf Q}$ 正規形**: 定理 KUM-n(4) の剛性により、$\bar{\mathbf Q}$ 上 $\gamma=\delta_0=1$ となる座標が取れる。その座標での被覆 $N\to\mathbf P^1_\lambda$ は「4 分岐点・指数 $(r_0,r_\infty)$・鏡映商」だけで書き切れる(探索なし・Gröbner なし・Newton なし) | **完了(構造として)** |
| **DET-4** | ⚠ **$N$ の(covering としての)最小定義体を同定し、$F$ への descent で生じる座標のずれを読む。** 補題 TW-1(b) より、得られた値がそのまま $[\gamma],[\delta_0]$ である | **★ 未実行(封印)** |

**DET-4 の理論的中身(実行せずに書ける部分)**: $N$ の座標を $m_0$($\lambda=m_0^2$)とすると、$\sigma\in G_F$ に対し ${}^\sigma N\to N$ の**一意な**同型(補題 TW-1(a))は $V$ 上で $m_0\mapsto\epsilon_\sigma m_0$($\epsilon_\sigma\in\{\pm1\}$)として働く。$\sigma\mapsto\epsilon_\sigma$ は準同型 $G_F\to\mu_2$ であり、Kummer 対応 $\mathrm{Hom}(G_F,\mu_2)=F^\times/F^{\times2}$ の下で
$$\boxed{\ [\gamma]\ \longleftrightarrow\ (\sigma\mapsto\epsilon_\sigma)\ }$$
$\epsilon_\sigma=+1\iff\sigma$ が $\mu_+,\mu_-$ を個別に固定 — 補題 TW-2 と同じ内容である。**DET-4 の実務は「$N$ の係数体を書き下し $\epsilon$ を読む」10 行程度の代数**であり、**その出力が $[u_7]_2$ である**。

**DET の計算量**: 探索ゼロ・持ち上げゼロ・有理再構成ゼロ。凍結設計 §3.5 の「予備 A(mod-$p$ 悉皆 + Newton)」「予備 B(Gröbner)」は**いずれも不要**。⟹ 凍結設計 U7-8 の判定を追認し、さらに強める。

---

## 6. mod $\mathfrak p$ 篩の整合条件(**検証可能な形**)

$\mathfrak p\notin S$、剰余体 $\mathbf F_q$、$\left(\frac{\cdot}{\mathfrak p}\right)$ を二次剰余記号とする(補題 TW-5 により $v_\mathfrak p(\gamma),v_\mathfrak p(\delta_0)$ は偶数なので記号は定義できる)。

| # | 条件 | 何を突き合わせるか |
|---|---|---|
| **MP-1** | $\left(\frac{\gamma}{\mathfrak p}\right)=1\iff$ 還元 $\bar W/\mathbf F_q$ の $\bar\lambda^{-1}(1)$ の **2 個の非分岐点が $\mathbf F_q$-有理** $\iff$ Frobenius が 2 ブロックを保つ | 補題 TW-2 の mod $\mathfrak p$ 版。**繊維だけ**見ればよく、模型全体は要らない |
| **MP-2** | $\left(\frac{-\delta_0}{\mathfrak p}\right)=1\iff\bar{\widetilde W}$ の $\lambda=0$ 上の 2 点が $\mathbf F_q$-有理($\iff$ cusp $P_0$ が $\widetilde W\to W$ で分裂) | 補題 TW-3 の mod $\mathfrak p$ 版 |
| **MP-3** | $\left(\frac{\gamma\delta_0}{\mathfrak p}\right)=1\iff$ 同上を $\lambda=\infty$ で | 同上 |
| **MP-4** | ★ **有限篩の閉包**: 補題 TW-5 より $[\gamma]\in F(S,2)$(有限)。$F(S,2)$ の元を分離する Frobenius をもつ素点の**有限リスト $\mathfrak p_1,\dots,\mathfrak p_t$ を、測定前に precompute できる**(測定に依存しない ⟹ **汚染しない**)。MP-1 をこの $t$ 本で走らせれば $[\gamma]$ が確定 | **非循環な篩**。$t$ は $\dim F(S,2)$ 程度 |
| **MP-5** | **一意性 integrity**: $\mathrm{Aut}=1$ かつ $H^1(\hat{\mathbf Z},1)=1$ ⟹ **$\mathbf F_q$-模型も一意**。mod $\mathfrak p$ 悉皆が同じ Nielsen 類に 2 個以上の $\mathbf F_q$-同型類を返したら**実装バグ確定(integrity stop)** | N-1〜N-3 と同格の NULL 枠 |
| **MP-6** | **良い素点の選び方**: $p\equiv1\pmod{4n}$($n=7$: $29,113,197,281,337,\dots$)なら $F$ が完全分解し $\mathbf F_q=\mathbf F_p$、$\mu_{28}\subset\mathbf F_p$。**$p=2,7$ は禁忌**(凍結設計 §3.5 と同じ) | 実装の指針 |
| **MP-7** | ★ **CAL-3 整合(fail-closed)**: $n=3$ 窓で本書の機構を走らせ、$[\gamma_3]=[u_3]_2=[-4]=1$(公開値・封印外)を**等式として**再現すること。不一致 ⟹ 定理 TOWER-n / KUM-n / 系 SPLIT / 本書 TW-1〜TW-3 のどこかが誤り ⟹ **本番を発火させない** | 凍結設計 §8.2 の副検査 3 を**等式**に強化 |

> **⚠ MP-1〜MP-3 の位置づけ**: これらは「還元被覆が既に得られている」ことを前提とするので、それ自体は決定機構ではなく**整合条件**である。**MP-4 だけが非循環な決定に使える**(素点リストが測定前に固定できるため)。この区別を混ぜないこと。

---

## 7. 経路 B — **有限群だけで閉じるもう 1 本**(⚠ 未評価)

### 7.1 補題 TW-6(捻れ剛性の機構)【proof + 機械】

> ### 補題 TW-6
> $\iota_V$ を $V\to\mathbf P^1_\lambda$ の被覆変換($m\mapsto-m$)とすると
> $$\boxed{\ \iota_V^*W\ \not\cong\ W\quad(\text{over }V)\ }$$
> であり、その理由は**上段の回転指数比の符号反転**である: 2 つのブロックの上で読んだ比は
> $$\Bigl(\frac{r_\infty}{r_0}\Bigr)_{\text{block }1}=-\alpha,\qquad \Bigl(\frac{r_\infty}{r_0}\Bigr)_{\text{block }2}=+\alpha\qquad(\text{和}\equiv0\bmod n).$$
> $n$ 奇・$\alpha\ne0$ ゆえ $-\alpha\ne+\alpha$ ⟹ 2 つの被覆は非同型。

**証明(群論).** $\iota_V$ は $g\in\mathcal M\setminus\bar A\bar H$ による共役に対応し、$\iota_V^*W$ の点 stabilizer は $g\bar Hg^{-1}$。$\iota_V^*W\cong W$ over $V$ $\iff$ $\bar H$ と $g\bar Hg^{-1}$ が $\bar A\bar H$ で共役 $\iff\exists h\in\bar A\bar H:hg\in N_{\mathcal M}(\bar H)=\bar H\subseteq\bar A\bar H\iff g\in\bar A\bar H$ — 矛盾。∎
**符号反転の計算.** $X^2=2e_1$、$(XY)^2=-2e_3$ ゆえ $Z^2=2e_3$。$X$ による共役は $q_1$ の作用で $e_1\mapsto e_1$、$e_3\mapsto-e_3$。ブロック 2 をブロック 1 と $X$ で同一視すると $(X^2,Z^2)\mapsto(X^2,-Z^2)$、すなわち $(r_0,r_\infty)\mapsto(r_0,-r_\infty)$。∎

**機械確認(T-W2)**: $n=3,7,9,11,13$、全 $\alpha$ で (i) $H\not\sim_{AH}XHX^{-1}$、(ii) 2 ブロックの比が $(-\alpha,+\alpha)$(和 $\equiv0$)、(iii) $Z^2$ が各ブロック上で一様な平行移動、(iv) $X$ はブロックを入れ替える。**19/19 ケース一致。**

> **これが §1.2 の罠の解体でもある**: 「分岐データが $G_F$-安定 ⟹ descent」は、比の**符号**という分岐データに現れない不変量を見落としている。**下段の捻れを塞いでいるのは上段である。**

### 7.2 補題 TW-7($\mathrm{Ih}$ 側の読み)【proof】

> ### 補題 TW-7
> 系 B-4c により $\mathrm{Fib}_{\vec{01}}(W_0)\cong\Lambda$ は $G_F$-同変で、$G_F$ の作用は $\beta_\gamma=\Phi(\mathrm{Ih}_N(\gamma))$ による。$\Lambda$ の 2 ブロック($\bar A\bar H$-軌道)への作用は二次指標 $\chi_{\rm blk}:G_F\to\{\pm1\}$ を与え、
> $$\boxed{\ [\gamma]\;=\;[u_n]_2\;=\;\chi_{\rm blk}\ \in\ \mathrm{Hom}(G_F,\mu_2)=F^\times/F^{\times2}. }$$

**証明.** 補題 B-5(iii) (7.1)(7.2) より $\mathrm{Fib}_{\vec{01}}$ は $\mu_M$-torsor($M=2n$)で類は $[u^{-1}]_M$。$X$ の作用は $\tau(\zeta_M)$、すなわち $\mathrm{Fib}\cong\mu_M$-torsor 上の $\zeta_M$-倍。$X\notin\bar A\bar H$、$X^2\in\bar A\bar H$ ゆえブロック分割は $\mu_M$-torsor の $\mu_n$-剰余、つまり商 torsor $\mathrm{Fib}/\mu_n$ は $\mu_2$-torsor でその類は $[u^{-1}]_M$ の $F^\times/F^{\times2}$ への像 $=[u^{-1}]_2=[u]_2$。系 SPLIT より $[u]_2=[\gamma]$。他方 $\mathrm{Fib}/\mu_n$ の $G_F$-作用は定義から $\chi_{\rm blk}$。∎

> ### ★ 何がうれしいか
> **曲線・$\lambda$・局所展開に一切触れずに $[\gamma]$ が決まる。** 必要なのは $\Phi(\mathrm{Ih}_N(G_F))$ がブロックを保つか否か、という**有限群の計算**だけである。
> さらに (W2) は $\gamma\in G_K$ に対し $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$ を与える。ゆえに
> $$\textbf{十分条件: }\ \Phi(\mathfrak F_0)\ \subseteq\ \mathrm{Stab}\bigl(\text{各ブロック}\bigr)\ \Longrightarrow\ [\gamma]=1 .$$
> **⚠⚠ この十分条件の検査は有限・数分の計算であり、その出力は $[u_7]_2$ である。私は実行していない。司令塔裁定により、これは「第二測定レーン」であって発火ゲートの内側にある。**
>
> > ### ⚠⚠⚠ **明示的な罠の申告(隠さない)**
> > この十分条件を、正典が既に持っている **$\mathfrak F_0$ の位数**((W2)-fam・裁定 120)と組み合わせると、**「$\mathfrak F_0$ が群か否か」という一点だけで結論が出る**形になる。すなわち $\mathfrak F_0$ が奇位数の**群**であれば $C_2$ への像は自明で $[\gamma]=1$ が即座に従う。
> > **私は $\mathfrak F_0$ の群性を確認していないし、この組み合わせを実行していない。** この 1 行の組み合わせ**そのもの**を発火手続の一部として扱われたい(隠して置くより、名指しして封じるほうが安全と判断した)。$\mathfrak F_0$ が単なる部分集合/剰余類であれば十分条件は自明には落ちず、$\Phi(\mathfrak F_0)$ の実計算が要る — **どちらであるかも封印後に確認すること。**

> ### ⚠ 循環の警告(必読)
> 経路 B は「$\mathrm{Ih}$ の像」を入力に使う。**$\mathrm{Ih}$ の全射性そのものを結論に使ってはならない**(定理 SURJ-K7 の右辺に $u_7$ が入るので、循環になる)。使ってよいのは **(W2)/(W5) のような、$\mathrm{Ih}$ の像に対する既証の上からの制約だけ**である。この線引きを cert の必須欄にすること。

### 7.3 経路 A と経路 B の独立性

| | 経路 A(§5) | 経路 B(§7) |
|---|---|---|
| 入力 | 4 分岐点・指数・剛性・descent | $\Lambda$ のブロック系・$\Phi(\mathfrak F_0)$・系 B-4c・補題 B-5 |
| 使う道具 | 代数幾何(Kummer・Weil descent) | 有限群論 + 橋 $B_{\rm FC}$ |
| 共有する前提 | 定理 TOWER-n・系 SPLIT・(W3)(W4) | 同左 + (W1)(W2)(W5)+(CAL) |
| 独立性の判定 | **部分独立**。TOWER-n と SPLIT を共有するので「完全独立な第二系統」ではない。**helper(CASC/transport)とは非共有** | 同左 |

> **受理規則案(M7(7) への追記)**: 経路 A と経路 B が一致 ⟹ **cross-checked**(**verified ではない**)。不一致 ⟹ **BRIDGE-UNKNOWN で停止**(値から経路を選び直さない)。両者は TOWER-n/SPLIT を共有するので、**真の完全独立系統は依然 B2′(塔を使わない次数 14 直接構成)だけ**である。

---

## 8. 決定に必要な入力データ一覧

| # | 入力 | 型 | 供給元 | 状態 |
|---|---|---|---|---|
| **I-1** | 窓 $(G_7,H_{2,1,0})$・marking $(X,Y,Z)$ | 有限群 | P-1/P-2 | **可(即)** |
| **I-2** | ブロック系(2×7)・各ブロックの $\bar Y$-固定点 1 個・各ブロックの型 $2^31$ | 有限群 | **本書 §9 T-W1** | **済(機械)** |
| **I-3** | $N_{G_7}(H)=H$ ⟹ $\mathrm{Aut}_{\mathbf P^1}(W)=1$ | 有限群 | (W3)+**本書 §9 T-W1** | **済(機械)** |
| **I-4** | 回転指数比の**符号つき**値 $(r_\infty/r_0)=\mp\alpha$(ブロック別) | 有限群 | **本書 §9 T-W2** | **済(機械)** |
| **I-5** | 4 分岐点の局所型・$(r_0,r_\infty)=(1,-\alpha)$ | 有限群 | TOWER-n・EXP(凍結) | 済 |
| **I-6** | **(GR)** 良還元の枠組み事実($\mathfrak p\nmid|\mathcal M_n|$) | 幾何 | **【要検分】** | 未(枠組み札) |
| **I-7** | $F(S,2)$、$S=\{\mathfrak p\mid14\}$ の**明示生成系** | 代数的数論 | $\mathcal O_S^\times$ と $\mathrm{Cl}(F)$ | **【文献要請 G7-3】依存**(未着) |
| **I-8** | MP-4 用の分離素点リスト $\mathfrak p_1..\mathfrak p_t$ | 計算 | I-7 から precompute | 未(**測定前に作れる・汚染しない**) |
| **I-9** | $\bar{\mathbf Q}$ 正規形 $N$ の係数体 | 代数 | DET-3/4 | ⚠ **DET-4 は封印前実行禁止** |
| **I-10** | $\Phi(\mathfrak F_0)$(7 元)のブロック作用 | 有限群 | 定義ノート・裁定 120 | ⚠ **封印前実行禁止**(第二測定レーン) |
| **I-11** | mod $\mathfrak p$ の繊維 $\bar\lambda^{-1}(1)$ の分解(数本) | 計算 | 予備 A の縮小版 | 未(発火後) |

---

## 9. 検算(本書で走らせたもの)

**純 python・整数演算のみ・有限群の置換計算のみ。曲線・$\lambda$・$u$・付値・データベースに一切接触していない。$n=5$ は【凍結 U7-NO5】遵守で経路から除去した**(群論であっても通さない)。

| probe | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/tw_blocks.py` | `4c84fef8500f13156e59da4de15df2ee1014e9400a77f6d313614d298f23e2c7` | $G_n=A\rtimes Q$ の構成・$H_{2,\alpha,0}$ の左剰余類・$N_G(H)$・core・$AH$-ブロック・$\bar X,\bar Y$ の作用と型(**T-W1**) |
| `search/probe/wac_v1/tw_orient.py` | `a160b58d0b4b6ac2c0f910b23983acc75e7566d9706334b7d67f72e26af4ea23` | $H\sim_{AH}XHX^{-1}$ の判定・ブロック別の回転指数比(**T-W2**) |

| # | 検査 | 対象 | 結果 |
|---|---|---|---|
| **T-W1** | $\lvert G\rvert=4n^3$・$\lvert H\rvert=2n^2$・$\lvert\Lambda\rvert=2n$・$N_G(H)=H$・$\mathrm{core}=\langle a_2\rangle$・$\lvert\mathcal M\rvert=4n^2$・$AH$-ブロック $=[n,n]$・$X$ がブロックを入替・$Y$ が保存・$\mathrm{type}(\bar Y)=2^{n-1}1^2$・**各ブロックの $\bar Y$-固定点 = 1**・$\mathrm{type}(\bar Y\vert_{\rm block})=2^{(n-1)/2}1$ | $n=3,7,9,11,13$、$\alpha=1..\frac{n-1}2$(**19 ケース**) | **全一致**(`ALL-CONSISTENT`)。$n=9,\alpha=3$($d=3$)のみ $\mathrm{core}\supsetneq\langle a_2\rangle$・$\lvert\mathcal M\rvert=108$ で **ODD-P の $d$ 分岐を再現**;ブロック構造は $d>1$ でも成立 |
| **T-W2** | $H\not\sim_{AH}XHX^{-1}$・ブロック別の比 $=(-\alpha,+\alpha)$・和 $\equiv0\ (n)$・$Z^2$ の平行移動一様性・$X$ のブロック入替 | 同上(**19 ケース**) | **全一致**。例: $n=7$ で $\alpha=1,2,3$ に対し比 $=(6,1),(5,2),(4,3)$ |

> **⚠ すべて単系統(1 実装・python)。cross-checked ではない。Lean 検証ではない。** GAP による独立再計算は**未実施**(凍結設計【U7-b】と同じ宿題)。
> **⚠ 曲線側の主張**(補題 TW-2 の「$R_i$ ↔ $\Sigma_1$」、TW-3、TW-4、TW-5)は**紙のみ**。機械が支えているのは有限群の部分だけである。

---

## 10. 【文献要請】の改訂

> ### 【文献要請 U7-1】— **(a) は撤回、(b) は否定的に解決、(c) のみ残す**
> * **(a)**「二面体被覆の定義体・モジュライ体の決定、とくに中間二次被覆の捻れ類がどの不変量で書けるか」 ⟹ **撤回**。補題 TW-1 により捻れの torsor は自明で、問いが空。**文献不要。**
> * **(b)**「$\lambda=\gamma m^2$ の $\gamma$ を**分岐データから**読む標準手続き」 ⟹ **存在しないことが分かった**(§1.2 の罠 + 補題 TW-6)。分岐データは $[\gamma]$ を決めない;決めるのは $G_F$-作用(補題 TW-2/TW-7)である。**文献不要。**
> * **(c)**「二面体 dessin(chain/necklace 型)の明示公式が古典的に知られているか」 ⟹ **残す**が優先度は低い。**第二系統(M7-B9)としてのみ価値**があり、決定には不要。

> ### 【文献要請 U7-2】(既出・**維持**)— 4 点分岐の巡回/二面体被覆の明示方程式表(次数 $\le15$)の在/不在
> **司令塔が scout に回付済(2026-08-01)。** 本書の結論は変えないが、**経路 A の独立検証**になりうる。

> ### 【文献要請 G7-3】(既出・未着・**優先度上昇**)
> $F=\mathbf Q(\zeta_{28})$ の類数・単数群。**本書 §4(補題 TW-5・系 TW-5c)で $F(S,2)$ の明示生成系が必要になった**ので、LB-RES 第 2 段の用途に加えて**決定機構の側でも要る**。優先度を上げられたい。

> ### 【文献要請 U7-3】(**新規・軽い**)— **(GR)** の正確な形
> **困難**: 補題 TW-5 は「tame($\mathfrak p\nmid|\mathcal M_n|$)+ 分岐点非衝突 ⟹ 良還元」という標準事実 (GR) を枠組み仮定として使っている。自前再導出はしていない。
> **欲しい結果の型**: 「$\mathbf P^1_{\mathbf Q}$ の $\mathbf Q$-有理 3 点で分岐する $G$-被覆が、$p\nmid|G|$ なる $\mathfrak p$ で良還元をもち、かつ定義体が $\mathfrak p$ で不分岐」という命題の**正確な前件と出典**。**強い一般論は要らない**。無ければ「無い」で一級 — その場合は補題 TW-5 を **(GR) 相対の定理**として札を付けたまま運用する。

---

## 11. FINDING 一覧(本書)

| # | 格 | 内容 |
|---|---|---|
| **TW-1** | **proof + 機械** | ★★ **形式一意性**: $\mathrm{Aut}_{\mathbf P^1_\lambda}(W)=N_{\mathcal M}(\bar H)/\bar H=1$ ⟹ $F$-形式は一意、塔の各段は標準的。**$[\gamma],[\delta]$ は捻れパラメータではない** ⟹ **U7-13 の「決定機構が無い」は解消**、【文献要請 U7-1(a)】は**問いが空**として撤回 |
| **TW-2** | **proof + 機械** | ★ **$[\gamma]=\mathrm{disc}F[V_{\lambda=1}]=\mathrm{disc}F[R_1,R_2]$**。UB-GEOM を**同値判定から等式へ格上げ** |
| **TW-3** | **proof** | **$[\delta_0]$ の決定式**: $F(\sqrt{-\delta_0})=F[\widetilde W_{\lambda=0}]$、$F(\sqrt{\gamma\delta_0})=F[\widetilde W_{\lambda=\infty}]$(Galois 閉包の cusp 繊維) |
| **TW-4** | **proof** | **$B$ の Brauer 類 $(\gamma,-\delta_0)$**。$B\cong\mathbf P^1_F\iff$ 分裂。**第三の決定量** |
| **TW-5** | **proof(GR 相対)** | ★ **$[\gamma],[\delta_0]\in F(S,2)$、$S=\{\mathfrak p\mid2n\}$** ⟹ $[u_7]_2$ の台が閉じ、候補が明示有限集合(系 TW-5c)。**G6-GAP-3′ の 2-部分のみ解決**($n$-部分は未解決) |
| **TW-6** | **proof + 機械** | ★★ **捻れ剛性の機構**: $\iota_V^*W\not\cong W$。ブロック別の回転指数比が $(-\alpha,+\alpha)$ と**符号反転**。**下段の捻れを塞いでいるのは上段** |
| **TW-7** | **proof** | ★★ **経路 B**: $[\gamma]=[u_n]_2=$ 「$\Phi\circ\mathrm{Ih}_N$ が $\Lambda$ の 2 ブロックを入れ替えるか」の二次指標。補題 B-5 (7.2) の torsor 類の 2-部分と一致。**曲線に触れずに決まる。⚠ 未評価** |
| **TW-8** | ★ **欠陥摘出** | **凍結 P-7 は分枝依存**($\mu_\pm\in V(F)$、すなわち $[\gamma]=1$ を前提)+ **Brauer 条件を暗黙に仮定**。⟹ **凍結修正 v2 が必要**(§3・後方互換な代替 $[\delta_0]$ を提供) |
| **TW-9** | **手続き警告** | ⚠⚠ **本書は装填済み**。決定機構が 2 本あり、どちらも最終段 10 行以下で $[u_7]_2$ を出す。**C5(7) の封印を「いま」置くべき**。DET-4 と §7.2 の指標評価は**発火手続の一部**(司令塔裁定 2026-08-01) |
| **TW-10** | ★教材 | 「分岐データが $G_F$-安定 ⟹ descent できる」は**剛性があっても偽**。見落としは回転指数比の**符号**(§1.2 の罠・TW-6 が解体)。**Belyi 被覆の descent 一般に効く罠** |
| **TW-11** | **UNKNOWN** | $[c]_n$($u_n=\gamma c^2$ の $n$-部分)の台は本書では制御されていない。**$u_7$ 全体の $S$-unit bound は未解決** |
| **TW-12** | **UNKNOWN** | (GR) は枠組み仮定のまま(【文献要請 U7-3】)。自前再導出も Lean 化もしていない |

### 11.1 未閉鎖・次の一手

* **【TW-a】凍結修正 v2 の起票**(P-7 差し替え + P-9 に $[\delta_0]$・$(\gamma,-\delta_0)$ を追加)→ 司令塔裁定 → LEDGER 記録 → **その後に封印** → **その後に発火**。
* **【TW-b】MP-4 の分離素点リスト**を**測定前に** precompute(I-7 待ち)。**汚染しない**ので封印前に作ってよい。
* **【TW-c】DET-4(経路 A)と §7.2(経路 B)を同時に発火**し、一致すれば cross-checked。**発火認可の内側でのみ。**
* **【TW-d】CAL-3(MP-7)を先に通す**: $n=3$ で $[\gamma_3]=1$ を**等式として**再現。fail-closed ゲート。**$u_3=-4$ は公開値なので封印外。**
* **【TW-e】GAP による T-W1/T-W2 の独立再計算**(第二系統・30 行)。現状 python 単系統。
* **【TW-f】** 本書は**紙 + python 単系統・Sol 監査前・Lean 検証ではない。$u_7$ 未接触。$K^{(5)}$ 非接触。**

---

## 12. 委嘱項目への対応表

| 委嘱項目 | 本書の該当節 | 一行回答 |
|---|---|---|
| $[\gamma],[\delta]$ の決定補題を起草 | §1–§3(TW-1〜TW-4) | **立った**。しかも「捻れ」という枠組み自体が誤りで、両者は**一意に決まる量** |
| 決定に必要な入力データのリスト | §8(I-1〜I-11) | 有限群側は**済(機械)**、数論側は $F(S,2)$(G7-3 依存)、幾何側は (GR)(要検分) |
| 検証可能な整合条件(mod p 篩) | §6(MP-1〜MP-7) | MP-1〜3 は整合条件、**MP-4 だけが非循環な決定に使える**(素点リストは測定前に固定可) |
| 構成できない場合は障害を要請票の言葉で | §10 | 構成できたので **U7-1(a)(b) は撤回・否定的解決**。新規は **U7-3((GR) の正確な形・軽い)** のみ |
| 凍結遵守($u_7$ の値・付値・**類**を計算しない) | §5 DET-4・§7.2・冒頭警告 | **計算していない。予想も書いていない。**「あと 10 行」であることは明記した(上申) |
| $n=5$ 非接触 | §9 | 群論の検算からも **$n=5$ を除去**(3,7,9,11,13 のみ) |
