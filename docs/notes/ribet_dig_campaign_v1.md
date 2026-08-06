# RIBET-DIG 採掘戦役 v1 — 証明済み結果の納品(裁定 707 / **713 により範囲限定**)

**状態札: `paper proof / all candidate / Sol 未監査 / GAP 実走ゼロ・窓生成ゼロ・cert 発行ゼロ / 封印非接触・S₁₂@691 blind 遵守(実測値への言及も推測もなし)/ Ĝ₂ 機械走行の結果を仮定しない`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: **裁定 707**(研究者直接指示)。**裁定 713 により範囲を限定** — 発案札(RDG-1..10)の検証・採否作業は中止し、**本ノートは既に証明の済んだ結果のみを証明つきで納める**。新規探索・新規軸作業は加えない。未着手/未完の部分は §7 に**明示的に「未納品」**として列挙する。
- 入力正本: `ribet_window_feasibility_v1.md` + `_addendum_thick.md` / `theorem_check_mirrorall_l3vacuous_v1.md` §A・§G / `sg_band_sweep_prereg_iffirst_v1.md` §2 / `b4_mirror_transfer_design_v1.md`(**v1.3**)/ `docs/scout/brown_eq14_verbatim_v1.md` / `search/certs/lins_twin_census_v1_20260806.json`(**読み出しのみ**)
- **自前検算の申告**: §1 の紙の定理を、**python の小スクリプト(整数演算・GAP 不使用・cert ではない)**で $p=5,7,11,13$ について再現した。**格は一切上げない**(単系統・実装係の測定と別物)。★ **初版のスクリプトには規約バグ(§1.1 の注)があり、修正版で再走した**。修正前後の差は §1.6 に正直に記録する。
- **分界**: `aside_measurement_*` 系ファイルには触れていない(期待表の数値予言は別係管轄)。

---

## 0. 納品一覧(9 件・すべて証明つき)

| # | 結果 | 場所 | 格 |
|---|---|---|---|
| **T1** | **定理 LADDER-WIN**: $G_p=H_{p^3}\rtimes S_3$ は **$p\ge5$ 一様に $B_3$ 窓商**。$G_p^{\rm ab}=C_2$・$(2,3)$-生成・$\twoheadrightarrow S_3$・$Z(G_p)=1$・$\Phi(G_p)=Z(H)$・$\mathrm{Syl}_p$ 非巡回(MIRROR-ODD 射程外)。⟹ **【RW-GAP-6】/ P-RW-4 を紙で閉じた(691 込み)** | §1.3 | 紙(candidate)+ 検算 4/4 |
| **T2** | **定理 LADDER-UNIQ**: $H_{p^3}\rtimes S_3$ が $(2,3)$-生成するのは **$S_3$-作用が忠実なときに限る**。⟹ **【RW-GAP-5】は構造的に閉じる**(det$=-1$ は選択でなく強制) | §1.2, §1.4 | 紙(candidate) |
| **T3** | **定理 LADDER-REFL**: $G_p$ は **全 $p\ge5$ で reflexible**。$\dim H^1(R,\mathbf F_p(\chi))=0$、$\dim H^2=1$。反射 $\beta$ を明示構成 | §1.5 | 紙(candidate)+ 検算 4/4 |
| **T4** | **定理 TWIST-6** と **系 RW-NOEIG**: 窓の 1 次元 $\mathbf F_p$-合成因子のねじれ指標は位数 $\mid\gcd(6,p-1)$。⟹ **$\chi^{11}$(位数 690)はどんな $B_3$ 窓にも入らない** | §2.1 | 紙(candidate) |
| **T5** | **補題 CYC-CHAR** と **定理 RW-CYC**: $q\ge5$ の巡回正規 Sylow をもつ $B_3$ 窓は $\widehat G^{\rm ab}=C_6$・$\mathrm{ord}(\chi)=6$・**$6\mid q-1$**。**既存 census の窓 13 行で例外ゼロ** | §2.2 | 紙 + cert 照合 13/13 |
| **T6** | **erratum E-1 / E-2**: $\widehat G_1=C_{691^2}\rtimes S_3$ は**そもそも窓でない**($(2,3)$-生成しない)。本体 §4 の R1 行「③窓 ✔」は誤り(RW-NOS3 で ✗)⟹ **P-RW-1..3 は取り下げ** | §2.3 | 紙 |
| **T7** | **補題 SG-AB-B4** と **定理 TWIST-12**: $B_4$ 窓($\Delta_4^2\in\widetilde N$)の $\widehat Q^{\rm ab}$ は位数 $\in\{2,4,6,12\}$ の巡回群 ⟹ ねじれ位数 $\mid\gcd(12,p-1)$。**$p=691$ では $=6$ = $B_3$ と同じ** | §3.2 | 紙(candidate) |
| **T8** | **【PIN-B4-2】閉**($\gamma^3=\delta^4=\Delta_4^2$)+ **【GAP-B4-5】閉**(補題 IOTA-NORM-B4: $\iota$ の正規化は**両生成元反転**)⟹ **定理 MIRROR-ODD-B4 が成立** | §3.3–§3.5 | 紙(candidate) |
| **T9** | **命題 RW-NOS4**($P\rtimes$ 巡回 に $S_n$ 商なし・$n\le4$、$p\ge5$)+ **軸③の答え = $n=4$ で消える RW 系 no-go はゼロ** | §3.6 | 紙(candidate) |

> ### ★ 一行の総括
> $$\boxed{\ \textbf{重なりは「Ribet が窓に入る場所」ではなく「窓が Ribet を排除する仕組み」にあった。}\ }$$
> その仕組み = **TWIST-6**: 窓の生得的制約 $\widehat G^{\rm ab}\in\{C_2,C_6\}$ が円分指標の通過帯域を位数 6 に絞る。これは否定 3 定理(RW-FRAT / RW-NOWIN / RW-NOS3)を 1 本にまとめ、$B_4$ へも延び(TWIST-12・$p=691$ では同じ 6)、**族一様**である。ゆえに RIBET-WINDOW の不成立は事故ではなく**定理**であり、その定理が掘るべき場所を一意に指す: **1 次元でない(既約 $\dim\ge2$ の)合成因子と、その間の拡大類**。$G_p$ はその条件を満たす**最小の族**であり、T1–T3 がそれを $p\ge5$ 一様に確立した。

---

# 1. 梯子 $G_p$(T1・T2・T3)

## 1.1 定義(作用まで完全に固定する)

> ### 定義 LADDER($G_p$ の正本定義)
> $p\ge5$ を素数とする。
> - $H=H_{p^3}$ := 位数 $p^3$・**指数 $p$** の extraspecial 群(Heisenberg)。$Z:=Z(H)=[H,H]=\Phi(H)\cong C_p$、$V:=H/Z\cong\mathbf F_p^2$。交換子は同型 $c:\Lambda^2V\xrightarrow{\sim}Z$ を与える。
> - $\rho:S_3\hookrightarrow GL_2(\mathbf F_p)$ := **忠実** 2 次元表現(標準表現 $\{(x_1,x_2,x_3):\sum x_i=0\}$ の $\bmod p$ 還元。$p\ge5$ ゆえ既約かつ忠実)。
> - $\mathrm{Aut}(H)\to GL_2(\mathbf F_p)$ は**全射で分裂**($p$ 奇)。$M$ の持ち上げは $Z=\Lambda^2V$ に $\det M$ で作用。$p\nmid6$ ゆえ $H^1(S_3,\mathrm{Inn}(H))=0$ で、$S_3\to\mathrm{Aut}(H)$ は $GL_2$ での像で共役を除き決まる。
> $$\boxed{\ G_p\ :=\ H\rtimes_\rho S_3,\qquad \lvert G_p\rvert=6p^3\ }$$
> - 標識対: $W:=\tilde u$($S_3$ 補群の 3-巡回)、$U:=$ $\tilde t$($t$ = 互換)の適当な $H$-共役(§1.3 (b) で条件を与える)。

**分裂の明示式(手で追える形・検算に使った規約)**: $H=\{(a,b,c)\}$、$(a,b,c)(a',b',c')=(a+a',b+b',c+c'+ab')$。$M=\begin{pmatrix}\alpha&\beta\\\gamma&\delta\end{pmatrix}$ に対し
$$\varphi_M(a,b,c)=\Bigl(a\alpha+b\gamma,\ a\beta+b\delta,\ (\det M)c+\tfrac{\alpha\beta}2a^2+\beta\gamma\,ab+\tfrac{\gamma\delta}2b^2\Bigr)$$
($2$ の可逆性を使う ⟹ $p$ 奇でのみ)。
> ⚠ **規約の注(検算バグの記録)**: この $\varphi$ は行ベクトルへの**右**作用に整合するので **$M\mapsto\varphi_M$ は反準同型**($\varphi_{MN}=\varphi_N\circ\varphi_M$)である。左作用として使うときは $\psi_M:=\varphi_{M^{-1}}$ を取ること($\psi_{MN}=\psi_M\circ\psi_N$)。**初版の検算スクリプトはここを取り違えて非結合的な積を作っていた**(§1.6)。紙の証明は $\varphi$ の明示式に依存しない(使うのは「$\mathrm{Aut}(H)\to GL_2$ が分裂し $Z$ に $\det$ で作用する」という抽象事実だけ)ので、**定理は無傷**。
$\rho(u)=\begin{pmatrix}0&-1\\1&-1\end{pmatrix}$、$\rho(t)=\begin{pmatrix}0&1\\1&0\end{pmatrix}$(手で確認: $\rho(u)^3=I$、$\rho(t)^2=I$、$\det\rho(t)=-1$、$\rho(t)\rho(u)\rho(t)=\rho(u)^{-1}$)。

## 1.2 補題 DET-FORCED(【RW-GAP-5】の構造的閉鎖・1 行)

> ### 補題 DET-FORCED(candidate・本ノート)
> $q$ 奇のとき $SL_2(\mathbf F_q)$ の位数 2 の元は $-I$(中心)のみ。ゆえに **$S_3$ の任意の忠実 2 次元表現は互換上で $\det=-1$**。
> $$\Longrightarrow\ \boxed{\ Z(H)=\Lambda^2V\ \text{は }S_3\text{-加群として必ず符号加群 }\mathbf F_p(\mathrm{sgn}).\ }$$

**証明.** $A\in SL_2(\mathbf F_q)$、$A^2=I$、$A\ne\pm I$ とすると $A$ の最小多項式は $X^2-1=(X-1)(X+1)$ で相異なる根をもつ ⟹ 対角化可能 ⟹ $A\sim\mathrm{diag}(1,-1)$、$\det A=-1\ne1$、矛盾。ゆえに $A=\pm I$。$S_3$ の忠実表現では互換の像は非中心(中心 $\{\pm I\}$ は位数 $\le2$ で $S_3/\ker$ が非可換になれない)ゆえ $\det=-1$。∎

⟹ 追補 `_addendum_thick.md` §4 の【RW-GAP-5】(「$-1$ 作用だと $Z$ が中心に落ちて $c\notin N$ が開く / det$=-1$ に取れるか要検算」)は**検算不要で閉じる**: 窓資格に必要な忠実性が det$=-1$ を**強制**し、したがって $Z(G_p)=1$(§1.3 (d))も自動である。

## 1.3 ★★ 定理 LADDER-WIN(T1)

> ### 定理 LADDER-WIN(candidate・本ノート)
> 全ての素数 $p\ge5$ に対し
> $$\boxed{\textbf{(a) } G_p^{\rm ab}=C_2\quad \textbf{(b) } G_p=\langle U,W\rangle,\ U^2=W^3=1\quad \textbf{(c) } G_p\twoheadrightarrow S_3\quad \textbf{(d) } Z(G_p)=1\quad \textbf{(e) } \Phi(G_p)=Z}$$
> ゆえに**定理 SG-EXACT**(`sg_band_sweep_prereg_iffirst_v1.md` §2.4)により
> $$\exists\,N_p\trianglelefteq B_3:\quad N_p\le PB_3,\quad c\in N_p,\quad B_3/N_p\cong G_p .$$
> さらに $\mathrm{Syl}_p(G_p)=H$ は**非巡回** ⟹ **定理 MIRROR-ODD の前件 (H) を満たさない**(紙で即死しない)。

**証明.**

**(c)** $G_p/H\cong S_3$。∎

**(a)** $[G_p,G_p]$ の $V=H/Z$ での像は $\sum_{\sigma}(1-\rho(\sigma))V$ を含む。$V$ は既約かつ非自明($p\nmid6$)ゆえ余不変式 $V_{S_3}=0$、すなわちこの像は $V$ 全体。また $Z=[H,H]\subseteq[G_p,G_p]$。ゆえに $[G_p,G_p]\supseteq H$、さらに $[G_p,G_p]/H=[S_3,S_3]=A_3$ ⟹ $[G_p,G_p]=H\rtimes A_3$、$G_p^{\rm ab}=C_2$。∎

**(d)** $z=hs$($h\in H$、$s\in S_3$)が中心なら $H$ への共役作用 $\mathrm{Inn}(h)\circ\rho(s)$ が恒等。$V$ 上 $\mathrm{Inn}(h)$ は自明($[H,H]=Z$)ゆえ $\rho(s)|_V=1$ ⟹ $s=1$($\rho$ 忠実)。すると $h\in Z(H)$ かつ $S_3$ で固定 ⟹ $h\in\mathbf F_p(\mathrm{sgn})^{S_3}=0$($p\ne2$、補題 DET-FORCED)。∎

**(e)** *($\supseteq$)* 拡大 $1\to Z\to G_p\xrightarrow{\pi} R\to1$($R:=G_p/Z\cong V\rtimes S_3$)は**非分裂**である。実際、補群 $C$ があれば $C\cap H$ は $Z$ の $H$ における補群になる($\pi(C)=R\supseteq V$ ゆえ $C\cap H$ は $V$ に全射、$(C\cap H)\cap Z\subseteq C\cap Z=1$)。しかし $H$ は extraspecial で、指数 $p$ の部分群はすべて $[H,H]=Z$ を含む ⟹ 補群なし。矛盾。$\lvert Z\rvert$ が素数ゆえ**補題 FRAT-SPLIT**(§G.12.4)より $Z\le\Phi(G_p)$。
*($\subseteq$)* $\Phi(R)=1$ を示す。$R$ の極大部分群は (i) $V\rtimes C_3$(指数 2)、(ii) $V\rtimes C_2$(指数 3)、(iii) $S_3$ の $V$-共役。(iii) が極大なのは、$S_3<K<R$ なら $K\cap V$ が $S_3$-部分加群($K\twoheadrightarrow S_3$ かつ $V$ 可換)で $V$ 既約ゆえ $K=S_3$ か $R$、による。$\Phi(R)\subseteq(V\rtimes C_3)\cap(V\rtimes C_2)=V$、かつ $\Phi(R)\subseteq\mathrm{core}_R(S_3)$。$\mathrm{core}_R(S_3)$ は $V$ と自明に交わり $R$ に正規ゆえ $[V,\mathrm{core}]\subseteq V\cap\mathrm{core}=1$、すなわち $V$ を中心化 ⟹ $\ker\rho=1$ より $\mathrm{core}=1$。よって $\Phi(R)=1$。したがって $\pi(\Phi(G_p))\subseteq\Phi(R)=1$ ⟹ $\Phi(G_p)\subseteq Z$。∎

**(b)** 2 段。
*(b-1) $R=V\rtimes S_3$ の生成。* $U_R:=(v,t)$ で $v\ne0$ を $\rho(t)$ の $(-1)$-固有直線に取る($U_R^2=(v+\rho(t)v,1)=1$ ✓)、$W_R:=(0,u)$。$K:=\langle U_R,W_R\rangle$ は $S_3$ に全射ゆえ $K\cap V$ は $S_3$-部分加群 ⟹ $V$ 既約より $0$ か $V$。$K\cap V=0$ なら $K$ は補群で、$H^1(S_3,V)=0$($p\nmid6$)ゆえ $K={}^wS_3$($w\in V$)。$(0,u)={}^w(0,u)=((1-\rho(u))w,u)$ ⟹ $(1-\rho(u))w=0$;$\rho(u)$ は固有値 1 をもたない($X^2+X+1$)ので $w=0$ ⟹ $K=S_3$ ⟹ $v=0$、矛盾。ゆえに $K=R$。
*(b-2) $G_p$ への持ち上げ。* まず $U,W\in G_p$ で $\pi(U)=U_R$、$\pi(W)=W_R$、$U^2=W^3=1$ なるものが存在する: $W=\tilde u$ ✓;$U$ は $\tilde t$ の $H$-共役 $h\tilde th^{-1}$ を取ればよく、その像は $(\delta_t(\bar h),t)$、$\delta_t(\bar h)=\bar h-\rho(t)\bar h$、$\mathrm{Im}\,\delta_t=(1-\rho(t))V=(-1)$-固有直線 ⟹ $v\ne0$ を実現できる ✓。
$\widetilde K:=\langle U,W\rangle$ は $\pi(\widetilde K)=R$ ゆえ $\widetilde KZ=G_p$。$Z\not\subseteq\widetilde K$ なら $\lvert Z\rvert$ 素数より $\widetilde K\cap Z=1$ ⟹ $\widetilde K$ は $Z$ の補群 ⟹ (e) の非分裂性に矛盾。ゆえに $Z\subseteq\widetilde K$ ⟹ $\widetilde K=\widetilde KZ=G_p$。∎
$\blacksquare$

> ### ★ 系(Frattini 収縮)
> (e) と Burnside の基底定理より
> $$\boxed{\ \langle U,W\rangle=G_p\iff\langle U_R,W_R\rangle=R=\mathbf F_p^2\rtimes S_3\quad(\lvert R\rvert=6p^2)\ }$$
> ⟹ **$(2,3)$-生成の判定は位数 $6p^2$ で決まる**。$p=691$ では $6\cdot691^2=\mathbf{2{,}864{,}886}$。
> ⚠ **同位数の別群と混同しない**: 追補の $\widehat G_1=C_{691^2}\rtimes S_3$ も位数 2,864,886 だが**別群**であり、しかも §2.3 で窓でないと判明する。

> ### ★ 【RW-GAP-6】/ P-RW-4 の決着
> 追補 §6 は「$\widehat G_2=H\rtimes S_3$ の $(2,3)$-生成の存否」を**本当の関門**とし、否なら Ribet 線完全閉鎖としていた。定理 LADDER-WIN (b) は **$p\ge5$ 一様に「存在する」**を与える(691 を含む)。⟹ **P-RW-4 は的中**、**【RW-GAP-6】は閉**。走行中の機械判定は**確認**の位置づけになる。
> ⚠ **必ず作用を突合すること**: 定理 LADDER-UNIQ(§1.4)により、**忠実標準表現以外の $S_3$-作用では $(2,3)$-生成は偽**である。機械側が別の作用で構成していれば「否」が出るが、それは Ribet 線閉鎖を意味しない。

## 1.4 ★★ 定理 LADDER-UNIQ(T2)

> ### 定理 LADDER-UNIQ(candidate・本ノート)
> $\psi:S_3\to\mathrm{Aut}(H_{p^3})$($p\ge5$)に対し
> $$\boxed{\ H_{p^3}\rtimes_\psi S_3\ \text{が }(2,3)\text{-生成}\iff \psi\ \text{が忠実}.\ }$$
> ⟹ $H_{p^3}\rtimes S_3$ 型の窓商は同型を除き**ちょうど 1 個 = $G_p$**。

**証明.** ($\Leftarrow$)$\psi$ 忠実なら $GL_2$ での像は $S_3$ の忠実 2 次元表現 ⟹ 標準表現(唯一。$\mathrm{std}\otimes\mathrm{sgn}\cong\mathrm{std}$ ゆえ同伴も同じ)⟹ 定理 LADDER-WIN (b)。
($\Rightarrow$)$\bar\psi:S_3\to GL_2(\mathbf F_p)$ が非忠実とする。$\ker\bar\psi\ne1$ かつ $S_3$ の正規部分群は $1,A_3,S_3$ ゆえ $\ker\bar\psi\supseteq A_3$。$p\nmid6$ より $\ker\psi=\ker\bar\psi\supseteq A_3$、すなわち **$A_3$ は $H$ に自明に作用**。
- 位数 3 の元 $s=h\tilde u$ は $s^3=h\cdot(\tilde uh\tilde u^{-1})\cdot(\tilde u^2h\tilde u^{-2})=h^3$($\tilde u$ の作用が自明)⟹ $h^3=1$ ⟹ $h=1$($\exp H=p\ge5$)⟹ **$s=\tilde u$ または $\tilde u^2$**。
- すべての互換は**同じ** $\theta:=\bar\psi(t)$ に写る。位数 2 の元 $r=a\tilde t$ の $V$-成分 $v$ は $r^2=1$ から $v+\theta v=0$。
$R=V\rtimes S_3$ の中で $\Sigma:=\{(0,\sigma):\sigma\in A_3\}\cup\{(v,\tau):\tau\ \text{互換}\}$ は積で閉じる:
$$(v,\tau)(v,\tau')=(v+\theta v,\tau\tau')=(0,\tau\tau'),\qquad (0,\sigma)(v,\tau)=(\sigma v,\sigma\tau)=(v,\sigma\tau)\ (\sigma\in A_3\ \text{自明作用}),$$
$$(v,\tau)(0,\sigma)=(v,\tau\sigma).$$
ゆえに $\langle\bar r,\bar s\rangle\subseteq\Sigma$ は位数 $\le6$ で $R$($=6p^2$)を生成しない。$\Phi$ 収縮(§1.3 の系。(e) の証明は $\rho$ の忠実性を使うので、非忠実な場合は $\Phi(G)\subseteq Z$ が言えない — しかし**生成しないことの証明には $\Phi$ は不要**: $\langle r,s\rangle$ の $R$ での像が真部分群なら $\langle r,s\rangle$ 自身も真部分群)⟹ $\langle r,s\rangle\ne G$。∎

> ### ★ 機構の一行
> $$\boxed{\ \textbf{生成を可能にしているのは「3 つの互換が 3 つの相異なる鏡映に写る」ことである。}\ }$$
> 非忠実だと 3 つの互換が同一の鏡映に潰れ、アフィン部分がねじれを失う。これは §2.2 の **CYC-CHAR** と同じ機構の 2 次元版であり、§2.3 の erratum の原因でもある。

## 1.5 ★★ 定理 LADDER-REFL(T3)

> ### 定理 LADDER-REFL(candidate・本ノート)
> 全ての $p\ge5$ で $G_p$ は **reflexible**、すなわち $\iota(N_p)=N_p$。ゆえに $[-1,1]$ は $N_p$ で **settled** であり、鏡映経路は $G_p$ に witness を供給しない。

**証明(明示構成).** $-I\in GL_2(\mathbf F_p)$ はスカラーゆえ $\rho(S_3)$ と可換で、その $\mathrm{Aut}(H)$ への持ち上げ $\varphi_{-I}$ は $S_3$-作用と可換(共役で移り合う作用が一致する)。ゆえに
$$\phi(h,\sigma):=(\varphi_{-I}(h),\sigma)$$
は $\mathrm{Aut}(G_p)$ の元。$\tilde t=(1,t)$ による内部自己同型と合成し $\beta_0:=\phi\circ\mathrm{Ad}(\tilde t)$ と置く。
- $\beta_0(W)=\phi(\tilde t\,\tilde u\,\tilde t^{-1})=\phi(1,tut^{-1})=(1,u^{-1})=W^{-1}$(**厳密**)。
- $U=(a,t)$ に対し $\mathrm{Ad}(\tilde t)(U)$ の $V$-成分は $\rho(t)v=-v$、$\varphi_{-I}$ で $+v$ に戻る ⟹ $\beta_0(U)\in UZ$。
次に $z\in Z$ による内部自己同型は、$\chi:=$($Z$ へのねじれ)$=\mathrm{sgn}$ ゆえ
$$\mathrm{Ad}(z)(U)=U\,z^{\chi(U)^{-1}-1}=Uz^{-2},\qquad \mathrm{Ad}(z)(W)=W\,z^{\chi(W)^{-1}-1}=W .$$
$2$ は $\bmod p$ 可逆ゆえ、$\beta_0(U)=Uz_0$ に対し $z^{-2}=z_0^{-1}$ なる $z$ を選べば
$$\beta:=\mathrm{Ad}(z)\circ\beta_0\ \in\ \mathrm{Aut}(G_p):\qquad \beta(U)=U,\quad \beta(W)=W^{-1}.$$
補題 **MIRROR-PSL**(§A.2)より $\iota(N_p)=N_p$。∎

> ### ★ コホモロジー側の理由(FRAT-CHIR の $\mathbf F_p$ 一般化の最初の実例)
> $\lvert S_3\rvert=6$ は $\bmod p$ 可逆 ⟹ LHS スペクトル系列が退化し $H^n(R,M)=H^n(V,M)^{S_3}$。$p$ 奇で $H^*(V,\mathbf F_p)=\Lambda(x_1,x_2)\otimes\mathbf F_p[y_1,y_2]$($y_i=\beta x_i$、Bockstein)ゆえ $S_3$-加群として
> $$H^1(V,\mathbf F_p)\cong V^*\cong\mathrm{std},\qquad H^2(V,\mathbf F_p)\cong\Lambda^2V^*\oplus V^*\cong\mathrm{sgn}\oplus\mathrm{std}.$$
> $\mathrm{std}\otimes\mathrm{sgn}\cong\mathrm{std}$、$\mathrm{sgn}^{\otimes2}\cong\mathbf 1$、$\mathrm{std}^{S_3}=0$ より
> $$\boxed{\ \dim H^1\bigl(R,\mathbf F_p(\mathrm{sgn})\bigr)=0,\qquad \dim H^2\bigl(R,\mathbf F_p(\mathrm{sgn})\bigr)=\mathbf 1\ }$$
> **FRAT-CHIR の強制予言は「掌性 ⟹ $\dim H^2\ge2$」**(§G.11.3: $\beta_R^*$ は $\mathrm{char}\ne2$ で対角化可能な対合ゆえ、$\dim=1$ なら任意の非零類が固有ベクトル ⟹ Wells 障害が消える)。ここは $\dim=1$ ⟹ **層 3 掌性は原理的に発火できない**。上の明示構成と整合する。
> ★ さらに $\dim H^1=0$ ゆえ $\dim Z^1=\dim B^1+\dim H^1=1$ で標識補正の自由度は 1 次元しかないが、**$W$ 成分の補正は不要**である: 弱持ち上げ $\beta(W)=W^{-1}y$($y\in Z$)は $\beta(W)^3=1$ から $y^{\chi(W)^2+\chi(W)+1}=y^3=1$ ⟹ $y=1$ が自動($p\nmid3$)。補正すべきは $U$ 成分のみで、$B^1$ の像 $\{z^{-2}\}=Z$ がそれを覆う。⟹ **【GAP-G11-1】型の穴は梯子上では閉じる。**

> ### 補題 CHIR-DIM(candidate・本ノート・副産物)
> $X\trianglelefteq\widehat P$、$X\cong C_p$($p$ 奇)、$R=\widehat P/X$ が reflexible とする。
> $$\dim_{\mathbf F_p}H^2(R,X)=1\ \Longrightarrow\ \text{Wells 障害は消える}\ \Longrightarrow\ (\text{標識補正が可能なら})\ \widehat P\ \text{は reflexible}.$$
> **証明.** $\beta_R^*$ は $H^2$ 上の対合、$\mathrm{char}\ne2$ ⟹ 対角化可能、$\dim=1$ ⟹ 任意の非零ベクトルが固有ベクトル ⟹ $\omega(\beta_R,\pm1)=0$。∎

## 1.6 自前検算(cert ではない・格を上げない)

**スクリプト**: python・整数演算のみ・GAP 不使用。$G_p$ を三つ組 $\times$ $2\times2$ 行列で明示構成し、群演算の**結合律を乱択 2000 組で検査**した上で測る。

| $p$ | $\lvert G_p\rvert$ | assoc 違反 | #involution | #(位数 3) | #生成 $(2,3)$-対 | $\lvert Z(G_p)\rvert$ | $\lvert G_p^{\rm ab}\rvert$ | reflexible |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 5 | 750 | **0** | 75 $(=3p^2)$ | 50 $(=2p^2)$ | **3000** $(=6p^3(p-1))$ | **1** | **2** | **True** |
| 7 | 2058 | **0** | 147 | 98 | **12348** $(=6p^3(p-1))$ | **1** | **2** | **True** |
| 11 | 7986 | **0** | 363 | 242 | (悉皆せず) | **1** | **2** | **True** |
| 13 | 13182 | **0** | 507 | 338 | (悉皆せず) | **1** | **2** | **True** |

- reflexible の判定は、標識対 $(U,W)$ と $(U,W^{-1})$ の **BFS 正準番号づけによる右乗置換 2 本**(標識対の完全不変量)の一致で行った。
- ★ **初版スクリプトの誤りの記録**: §1.1 の注のとおり $\varphi$ を左作用として使ったため積が非結合的になり、生成対の個数が $2880$ / $12096$(真値 $3000$ / $12348$)と出ていた。**修正版では結合律違反 0・紙の予測値と完全一致**。$\lvert Z\rvert=1$・$\lvert G^{\rm ab}\rvert=2$・reflexible は修正前後で同じ値だった。**誤った中間値を報告に使っていない**ことを申告する。

> ### ★ 副産物: 定理 LADDER-UNIQ-N(candidate・本ノート)
> 生成 $(2,3)$-標識対の個数は $6p^3(p-1)$(紙 + 検算 2/2)。$\mathrm{Aut}(G_p)$ は生成対に**自由**に作用し($\alpha$ が両生成元を固定 ⟹ $\alpha=\mathrm{id}$)、$\lvert\mathrm{Inn}(G_p)\rvert=\lvert G_p\rvert=6p^3$($Z(G_p)=1$)。スカラー $\lambda\in\mathbf F_p^\times$ の誘導する $\varphi_\lambda$ は $\rho(S_3)$ と可換で $\mathrm{Aut}(G_p)$ を与え、$V$ 上の作用が $\lambda\cdot\mathrm{id}$;内部自己同型の $V$ への作用は $\rho(S_3)$ に限られ $-I\notin\rho(S_3)$(位数 2 の元は $\det=-1$)ゆえ $\varphi_\lambda$ が内部 $\iff\lambda=1$。ゆえに $\lvert\mathrm{Aut}(G_p)\rvert\ge6p^3(p-1)=\#\{\text{生成対}\}$、軌道数 $\le1$、生成対は存在するので
> $$\boxed{\ \lvert\mathrm{Aut}(G_p)\rvert=6p^3(p-1),\quad \lvert\mathrm{Out}(G_p)\rvert=p-1,\quad B_3/N\cong G_p\ \text{なる窓 }N\ \text{はちょうど 1 個}.\ }$$
> **⟹ $G_p$ は双子(twin)にならない。** ゆえに既存 twin census に $G_5$(位数 750)が載っていないことは**矛盾ではなく予言の的中**である。
> (実際 cert の指数 750 行は `((C5xC5):C5):C6` のみで、しかも `in_PB3 = False` = 窓外 — これは $P\rtimes$ 巡回 に $S_3$ 商が無いという **RW-NOS3 の実測確認**でもある。)
> *生成対の個数の紙の計算*: 位数 3 の元は $u,u^2$ の上に各 $\lvert H\rvert/\lvert C_H(\tilde u)\rvert=p^3/p=p^2$ 個(計 $2p^2$、$V$ の値と全単射);位数 2 の元は 3 つの互換の上に各 $p^2$ 個(計 $3p^2$、$V$ での像 $v$ は $(-1)$-固有直線の $p$ 値、繊維 $p$)。生成条件は正規化後の $v\ne0$ で、$(v,w)$ を $V$-共役で $w=0$ に正規化すると $v\mapsto v-(1-\rho(t))(1-\rho(u))^{-1}w$;各 $w$ に対し消える $v$ はちょうど 1 つ ⟹ 各 shape で生成する $R$-対は $p^3-p^2=p^2(p-1)$、$G$-対はその $p$ 倍 ⟹ 総計 $6\cdot p\cdot p^2(p-1)=6p^3(p-1)$ ✓(検算 2/2 一致)。

---

# 2. 辞書 — TWIST-6・RW-CYC・erratum(T4・T5・T6)

## 2.1 ★★★ 定理 TWIST-6 と系 RW-NOEIG(T4)

> ### 定理 TWIST-6(candidate・本ノート)
> $N$ を $B_3$ 窓($N\le PB_3$、$c\in N$)、$\widehat G=B_3/N$ とする。$\widehat G$ の任意の正規 $p$-部分群の任意の切片に現れる **1 次元 $\mathbf F_p[\widehat G]$-合成因子**の指標 $\psi:\widehat G\to\mathbf F_p^\times$ について
> $$\boxed{\ \psi\ \text{は }\widehat G^{\rm ab}\in\{C_2,C_6\}\ \text{を経由する}\ \Longrightarrow\ \mathrm{ord}(\psi)\ \bigm|\ \gcd(6,\,p-1).\ }$$
> **証明.** $\mathbf F_p^\times$ は可換ゆえ $\psi$ は $\widehat G^{\rm ab}$ を経由。補題 SG-AB($c\in N$、$N\le PB_3$)より $\widehat G^{\rm ab}\in\{C_2,C_6\}$ ⟹ $\mathrm{ord}(\psi)\mid6$。また $\psi$ の像は $\mathbf F_p^\times$(位数 $p-1$)の部分群。∎(3 行)

> ### 系 RW-NOEIG(candidate・本ノート。**Ribet 線が閉じている理由の最短形**)
> Ribet 型の可約 2 次元表現(合成因子の指標が $\{1,\omega^{k-1}\}$)の像が窓商の切片として現れるなら、両合成因子が 1 次元ゆえ TWIST-6 が適用され
> $$\mathrm{ord}(\omega^{k-1})=\frac{p-1}{\gcd(k-1,\,p-1)}\ \bigm|\ 6\qquad\Longleftrightarrow\qquad (p-1)\bigm|6(k-1).$$
> $(p,k)=(691,12)$: $\gcd(11,690)=1$ ⟹ 位数 $690\nmid6$。
> $$\boxed{\ \textbf{Ribet の }(691,12)\ \textbf{固有空間は、どんな }B_3\ \textbf{窓にも入らない。}\ }$$

> ### ★ 既在 3 定理との関係(**これが「辞書」の本体**)
> | 既在 | TWIST-6 から見た位置 |
> |---|---|
> | **RW-NOWIN**($Z=1\Rightarrow c\in N\Rightarrow\widehat G^{\rm ab}=C_{690}$ で矛盾) | **特別な場合**。TWIST-6 は $Z(\widehat G)$ にも $c$ にも触れずに同じ結論を出し、しかも**任意の合成因子**に効く |
> | **RW-FRAT**(第 1 層は Schur–Zassenhaus で常に分裂) | **直交する情報**。TWIST-6 は「ねじれの帯域」、RW-FRAT は「隠れる深さ」 |
> | **RW-NOS3**($P\rtimes$ 巡回 に $S_3$ 商なし) | **トーラスの非可換性要求**。TWIST-6 と合わせて「トーラスは非可換だが $\widehat G^{\rm ab}$ は $C_2$ か $C_6$」 |
> | **RW-CYC**(§2.2・新) | 巡回 Sylow の場合に TWIST-6 を**飽和**させた形($\mathrm{ord}\chi=6$ ちょうど) |
>
> $$\boxed{\ \textbf{辞書の一行目: }\widehat G^{\rm ab}\in\{C_2,C_6\}\ \textbf{という窓の生得的制約が、円分指標の通過帯域を位数 6 に絞る。}\ }$$
> ⟹ **算術情報が窓に入る道は 2 つしかない**: (i) 位数 $\le6$ のねじれ、(ii) **既約 $\dim\ge2$ の合成因子とその間の拡大類**。$G_p$ は (ii) の最小実現($V=\mathrm{std}$ は 2 次元既約、$Z=\mathrm{sgn}$ は位数 2 ✓ TWIST-6 と整合)。

## 2.2 ★★★ 補題 CYC-CHAR と定理 RW-CYC(T5)

> ### 補題 CYC-CHAR(candidate・本ノート)
> $A\cong C_{q^n}$($q$ 素数)、$Q$ を $q'$-群、$\widehat G=A\rtimes Q$、$\chi:\widehat G\to\mathrm{Aut}(A)$ をねじれ指標とする。$\widehat G=\langle U,W\rangle$ で $\mathrm{ord}(U)\mid a$、$\mathrm{ord}(W)\mid b$、$q\nmid ab$ ならば
> $$\boxed{\ \chi(U)\ne1\quad\textbf{かつ}\quad\chi(W)\ne1.\ }$$

**証明.** $A\trianglelefteq\widehat G$ ゆえ $\Phi(A)=A^q\le\Phi(\widehat G)$(標準事実)。Burnside の基底定理により生成判定は $\widehat G/A^q$ で決まるので $A\cong C_q$ としてよい。
$U=(x,u)$、$U^a=(N_u(x),u^a)$、$N_u=1+\chi(u)+\dots+\chi(u)^{a-1}$。$\chi(u)=1$ なら $N_u=a\ne0$ in $\mathbf F_q$ ⟹ $x=0$;$\chi(u)\ne1$ なら $\chi(u)^a=1$ より $N_u=\frac{\chi(u)^a-1}{\chi(u)-1}=0$ ⟹ $x$ 自由。$W=(y,w)$ も同様。
$K:=\langle U,W\rangle$ に対し $K\cap A$ は $K\twoheadrightarrow Q$ の作用で $Q$-部分加群 ⟹ $0$ か $A$。$K\cap A=0$ ⟺ $K$ は補群 ⟺($H^1(Q,A)=0$ ゆえ補群は全て $A$-共役)$\exists f\in A$:
$$x=(1-\chi(u))f\quad\text{かつ}\quad y=(1-\chi(w))f .$$
$\chi(u)=1$ の場合: $x=0$ で第 1 式は任意の $f$ で成立。第 2 式は $\chi(w)\ne1$ なら $f=y/(1-\chi(w))$ で解け、$\chi(w)=1$ なら $y=0$ で任意の $f$ で成立。いずれも解があるので $K$ は補群 ⟹ $K\ne\widehat G$。$\chi(w)=1$ の場合も対称。∎

> ### ★★ 定理 RW-CYC(candidate・本ノート。**第 4 の no-go**)
> $N$ を $B_3$ 窓($N\le PB_3$、$c\in N$)、$\widehat G=B_3/N$ が **$q\ge5$ の非自明巡回正規 Sylow $A$** をもつとする。このとき
> $$\boxed{\ \widehat G^{\rm ab}=C_6,\qquad \mathrm{ord}(\chi)=6,\qquad \mathbf{6\mid q-1}.\ }$$
> **証明.** $A$ は正規 Hall 部分群 ⟹ Schur–Zassenhaus で $\widehat G=A\rtimes Q$。$A$ 巡回 ⟹ $\mathrm{Aut}(A)$ 可換 ⟹ $\chi$ は $\widehat G^{\rm ab}$ を経由し、補題 SG-AB より $\mathrm{ord}(\chi)\mid6$。標識対は $\mathrm{ord}(U)=2$、$\mathrm{ord}(W)=3$、$q\nmid6$ ゆえ補題 CYC-CHAR が適用でき $\chi(U)\ne1$、$\chi(W)\ne1$ ⟹ $2\mid\mathrm{ord}\chi$ かつ $3\mid\mathrm{ord}\chi$ ⟹ $\mathrm{ord}(\chi)=6$、$\widehat G^{\rm ab}=C_6$。$\mathrm{Im}\,\chi\le\mathrm{Aut}(C_{q^n})$(位数 $q^{n-1}(q-1)$)が位数 6 で $\gcd(6,q)=1$ ⟹ $6\mid q-1$。∎

> ### ★★ 独立照合(既存 cert の読み出し・**13 行で例外ゼロ**)
> `search/certs/lins_twin_census_v1_20260806.json` の窓層(両 member が `c_in_N ∧ in_PB3`)13 行:
>
> | 指数 | 構造 | $q\ge5$ | $q\bmod6$ | $\widehat G^{\rm ab}$ | RW-CYC |
> |---:|---|---:|---:|---|---|
> | 126 | `C7:(C3xS3)` | 7 | **1** | $C_6$ | ✔ |
> | 234 | `C13:(C3xS3)` | 13 | **1** | $C_6$ | ✔ |
> | 342 | `C19:(C3xS3)` | 19 | **1** | $C_6$ | ✔ |
> | 378 | `C7:((C3xC3):C6)` | 7 | **1** | $C_6$ | ✔ |
> | ★ **432** | `(((C3xC3):Q8):C3):C2` | **なし** | — | ★ **$C_2$** | ✔(前件が空) |
> | 486 | `((C9:C9):C3):C2` | **なし** | — | $C_6$ | ✔(前件が空) |
> | 504 | `C7:(C3xS4)` | 7 | **1** | $C_6$ | ✔ |
> | 504 | `C7:(A4xS3)` | 7 | **1** | $C_6$ | ✔ |
> | 558 | `C31:(C3xS3)` | 31 | **1** | $C_6$ | ✔ |
> | 666 | `C37:(C3xS3)` | 37 | **1** | $C_6$ | ✔ |
> | 702 | `C13:((C3xC3):C6)` | 13 | **1** | $C_6$ | ✔ |
> | 774 | `C43:(C3xS3)` | 43 | **1** | $C_6$ | ✔ |
> | 882 | `C49:(C3xS3)` | 7 | **1** | $C_6$ | ✔ |
> | 936 | `C13:(C3xS4)` | 13 | **1** | $C_6$ | ✔ |
> | 936 | `C13:(A4xS3)` | 13 | **1** | $C_6$ | ✔ |
>
> ($\widehat G^{\rm ab}$ の値は `sg_band_sweep_prereg_iffirst_v1.md` §2.1.1 の `AbelianInvariants` 実測 12/12 から。指数 882 の Syl$_7=C_{49}$ は $\mathrm{Aut}=C_{42}$ で $6\mid42$ ✓。)
> ★ **唯一 $\widehat G^{\rm ab}=C_2$ の窓(指数 432)が、ちょうど $q\ge5$ をもたない窓である** — 定理が要求する完全な相関が実データで成立している。出現した $q\in\{7,13,19,31,37,43\}$ はすべて $\equiv1\ (6)$ で、$q\equiv5\ (6)$($5,11,17,23,29,41,\dots$)は**一つも現れない**。
> ⚠ **格の限定**: 上表は twin cert の読み出しであり非 twin の窓は載っていない ⟹ 「$q\equiv5\ (6)$ の窓が存在しない」は**まだ悉皆主張ではない**。現時点の格は「**陽性 13 行で一致・反例ゼロ**」。

> ### ★ 副産物: MIRROR-ODD の別証明
> CYC-CHAR で $\chi(W)\ne1$ を出し、**Tool R2′**($\mathrm{Aut}(A)$ 可換 ⟹ SECT は $\mu(W)=1$ に退化)を当てるだけで MIRROR-ODD が出る。旧証明($\widehat P_0^{\rm ab}$ の指数 3 を経由)より短く、しかも **$6\mid q-1$ という追加情報**が付く。
> ### ★ 統合(狩場判定の最終形)
> $q\ge5$ 巡回正規 Sylow の窓は **(i) 存在するには $6\mid q-1$ かつ $\widehat G^{\rm ab}=C_6$**(RW-CYC)、**(ii) 存在しても MIRROR-ODD で chiral・witness $[-1,1]$ は算術元** ⟹ B 型は棲めない。
> $$\boxed{\ \textbf{「}q\ge5\ \textbf{巡回正規 Sylow の窓は B 型の狩場でない」は、存在側の条件まで込みで閉じた。}\ }$$

## 2.3 ★★ erratum(T6)

> ### erratum E-1(`ribet_window_feasibility_v1_addendum_thick.md` §3 への訂正)
> $\widehat G_1=C_{691^2}\rtimes S_3$。$\mathrm{Aut}(C_{691^2})$ は可換ゆえ $S_3$ の作用は $S_3^{\rm ab}=C_2$ を経由 = 反転。よって $\chi(W)=\mathrm{sgn}(u)=1$($u$ は 3-巡回)。補題 CYC-CHAR より
> $$\boxed{\ \widehat G_1\ \textbf{は }(2,3)\textbf{-生成でない ⟹ そもそも }B_3\ \textbf{窓商ではない。}\ }$$
> 明示: 位数 3 の元は $s=\tilde u$ に限られ($A_3$ が自明に作用ゆえ $s^3=h^3=1\Rightarrow h=1$)、位数 2 の元 $(b,\tau)$ と合わせて $\langle(b,t),(0,u)\rangle=\{(0,\text{偶})\}\cup\{(b,\text{奇})\}\cong S_3$(位数 6)。
> 追補 §3 の表は ②($\Phi$)③-a($S_3$ 商)③-b(ab)③-c($Z$)を検査したが **G2($(2,3)$-生成)を検査していなかった**。$\widehat G_1$ の死因は追補 §3.1 の MIRROR-ODD **ではなく、その手前の非生成**である(結論「$\widehat G_1$ は使えない」は不変、**理由と死ぬ深さが違う**)。
> ★ これは定理 RW-CYC の帰結でもある: $\widehat G_1^{\rm ab}=C_2\ne C_6$ ⟹ 窓になれない。

> ### erratum E-2(`ribet_window_feasibility_v1.md` §4 表 R1 行・§7 予言表への訂正)
> R1 $=C_{691}\rtimes C_m$($m\in\{2,6\}$)の「③窓 ✔」は**誤り**。追補で導入された **RW-NOS3**($P\rtimes$ 巡回 に $S_3$ 商なし)がそのまま適用され、R1 は **G3(**$\twoheadrightarrow S_3$**)で落ちる**。
> $$\Longrightarrow\ \textbf{P-RW-1}(\text{「}C_{691}\rtimes C_6\ \text{は窓として実在」})\ \textbf{は紙で偽}.$$
> **P-RW-2 / P-RW-3 は前件が空**になる。⟹ **この 3 本は測定せずに取り下げ、墓標として記録する**(費用 GAP 数秒の較正実験も不要)。

---

# 3. $B_4$ 側(T7・T8・T9)

## 3.1 前提の訂正(先に)

委嘱文「**NO-PSL-B4 により MIRROR-ODD は $n=3$ 限定**」は、**2026-08-06 の v1.3(裁定 637・Sol 便 112 指摘)で既に撤回済み**である(`b4_mirror_transfer_design_v1.md` §4.2 の警告枠)。現行の正しい状態:
- 旧補題は **NO-PSL-GEN-B4** に改名・狭形化(言えるのは「$(\Delta_4,\delta_4)$ 対の逐語移植が不能」まで)。
- 正しい対 $(\gamma,\delta)$($\gamma=\sigma_1\delta$)で **補題 PSL-GEN-B4**($V^3=W^4=1$)が成立し、**エンジンの段 (1)(2)(3) は移る**。
- 残っていたのは **段 (4) = $\iota$ の正規化【GAP-B4-5】ただ 1 つ**、および **【PIN-B4-2】**($\gamma^3=\Delta_4^2$)。
⟹ 以下でその 2 つを閉じる。

## 3.2 補題 SG-AB-B4 と定理 TWIST-12(T7)

> ### 補題 SG-AB-B4(candidate・本ノート)
> $\widetilde N\trianglelefteq B_4$、$\widetilde N\le PB_4$、$\Delta_4^2\in\widetilde N$ ⟹ $\widehat Q:=B_4/\widetilde N$ の $\widehat Q^{\rm ab}$ は**位数 $\in\{2,4,6,12\}$ の巡回群**。
> **証明.** $B_4^{\rm ab}\cong\mathbf Z$($\sigma_i\mapsto1$)で $\Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4\mapsto12$。$\Delta_4^2\in\widetilde N$ ⟹ $\widehat Q^{\rm ab}$ は $\mathbf Z/12$ の商 = 位数が 12 を割る巡回群。$\widetilde N\le PB_4$ ⟹ $\widehat Q\twoheadrightarrow B_4/PB_4=S_4$ ⟹ $\widehat Q^{\rm ab}\twoheadrightarrow S_4^{\rm ab}=C_2$ ⟹ 偶数。∎

> ### 定理 TWIST-12(candidate・本ノート)
> 上の設定で、正規 $p$-部分群の切片の 1 次元 $\mathbf F_p[\widehat Q]$-合成因子の指標 $\psi$ は $\mathrm{ord}(\psi)\mid\gcd(12,p-1)$。
> $$p=691:\quad 690=2\cdot3\cdot5\cdot23,\quad \gcd(12,690)=\mathbf 6 .$$
> $$\boxed{\ \textbf{$p=691$ では }B_4\ \textbf{の帯域上限は }B_3\ \textbf{と同じ 6。}\ \chi^{11}\ \textbf{(位数 690)は }B_4\ \textbf{でも死ぬ。}\ }$$

> ### 補題 WIN-B4-NEC(窓資格の**必要条件**の一覧)
> $\widetilde N$ が $B_4$ 窓($\widetilde N\le PB_4$)で $\Delta_4^2\in\widetilde N$ なら $\widehat Q$ は:
> **(H1)** $\widehat Q^{\rm ab}$ が位数 $\in\{2,4,6,12\}$ の巡回群(SG-AB-B4)/ **(H2)** $\widehat Q=\langle V,W\rangle$、$V^3=W^4=1$(PSL-GEN-B4 + §3.3)/ **(H3)** $\widehat Q\twoheadrightarrow S_4$ / **(H4)** 非可換窓なら $[B_4:\widetilde N]\ge192$(既在 INDEX-LB)。
> ⚠ **十分性は未証明**(§7【DIG-GAP-3】): $B_3$ の補題 SG-S3 に対応する「$\psi:B_4\to S_4$ の核がちょうど $PB_4$」の議論が要る($B_4^{\rm ab}=\mathbf Z\to C_2$ からは $\psi(\sigma_i)$ が奇置換までしか出ず、**4-巡回の可能性を排除していない**)。⟹ **SG-EXACT-B4 は未完**。

## 3.3 ★★ 【PIN-B4-2】を閉じる($\gamma^3=\delta^4=\Delta_4^2$・1 行)

$\delta:=\sigma_1\sigma_2\sigma_3$、$\gamma:=\sigma_1\delta$。既在の **(D2)**(`b4_mirror_transfer_design_v1.md` §11 で braid 関係から検算済): $\delta\sigma_1\delta^{-1}=\sigma_2$、$\delta\sigma_2\delta^{-1}=\sigma_3$。ゆえに
$$\gamma^3=(\sigma_1\delta)^3=\sigma_1(\delta\sigma_1)(\delta\sigma_1)\delta=\sigma_1(\sigma_2\delta)(\sigma_2\delta)\delta=\sigma_1\sigma_2(\delta\sigma_2)\delta^2=\sigma_1\sigma_2(\sigma_3\delta)\delta^2=\underbrace{\sigma_1\sigma_2\sigma_3}_{\delta}\cdot\delta^3=\boxed{\delta^4}$$
$\delta^4=(\sigma_1\sigma_2\sigma_3)^4=\Delta_4^2$ は既在(同 §1.3)。$\blacksquare$
($n=3$ 版の整合: $\gamma=\sigma_1\cdot\sigma_1\sigma_2=\sigma_1^2\sigma_2$、$\gamma^2=\delta^3=c$ — 工房既在の検算 $(\sigma_1^2\sigma_2)^2=c$ と一致 ✓。)

## 3.4 ★★★ 【GAP-B4-5】を閉じる(補題 IOTA-NORM-B4 = **両生成元反転**)

$\iota:\sigma_i\mapsto\sigma_i^{-1}$。**FLIP-INNER**(同 §11)より $\mathrm{Ad}(\Delta_4)$ は $\sigma_1\leftrightarrow\sigma_3$・$\sigma_2$ 固定;$\Delta_4^2$ が中心ゆえ $\mathrm{Ad}(\Delta_4^{-1})=\mathrm{Ad}(\Delta_4)$。

1. $\iota(\delta)=\sigma_1^{-1}\sigma_2^{-1}\sigma_3^{-1}=(\sigma_3\sigma_2\sigma_1)^{-1}=\bigl(\mathrm{Ad}(\Delta_4)\delta\bigr)^{-1}=\Delta_4\delta^{-1}\Delta_4^{-1}$。
2. $\iota':=\mathrm{Ad}(\Delta_4^{-1})\circ\iota$ とおくと $\iota'(\delta)=\delta^{-1}$、$\iota'(\sigma_1)=\mathrm{Ad}(\Delta_4^{-1})(\sigma_1^{-1})=\sigma_3^{-1}$。
3. (D2) を 2 回使って $\sigma_3=\delta^2\sigma_1\delta^{-2}$;$\sigma_1=\gamma\delta^{-1}$ ゆえ $\sigma_1^{-1}=\delta\gamma^{-1}$、したがって $\sigma_3^{-1}=\delta^2(\delta\gamma^{-1})\delta^{-2}=\delta^3\gamma^{-1}\delta^{-2}$。
4. $\iota'(\gamma)=\iota'(\sigma_1)\,\iota'(\delta)=\sigma_3^{-1}\delta^{-1}=\delta^3\gamma^{-1}\delta^{-3}$。$\delta^4=\Delta_4^2$ は中心ゆえ $\mathrm{Ad}(\delta^3)=\mathrm{Ad}(\delta^{3}\delta^{-4})=\mathrm{Ad}(\delta^{-1})$ ⟹ $\iota'(\gamma)=\delta^{-1}\gamma^{-1}\delta$。
5. $\iota'':=\mathrm{Ad}(\delta)\circ\iota'$ とおくと $\iota''(\delta)=\delta\cdot\delta^{-1}\cdot\delta^{-1}=\delta^{-1}$、$\iota''(\gamma)=\delta(\delta^{-1}\gamma^{-1}\delta)\delta^{-1}=\gamma^{-1}$。

> ### 補題 IOTA-NORM-B4(candidate・本ノート。**【GAP-B4-5】閉**)
> $$\boxed{\ \iota''=\mathrm{Ad}(\delta\Delta_4^{-1})\circ\iota\in\mathrm{Aut}(B_4):\qquad \gamma\mapsto\gamma^{-1},\qquad \delta\mapsto\delta^{-1}\ }$$
> (整合検査: $\iota''(\gamma^3)=\gamma^{-3}$、$\iota''(\delta^4)=\delta^{-4}$、$\gamma^3=\delta^4$ ⟹ 両辺整合 ✓。$B_4=\langle\gamma,\delta\rangle$ ゆえこれで $\iota''$ は決まる。)

> ### ★ 統一($B_3$ の「僥倖」の正体)
> $B_3$ でも $\iota'=\mathrm{Ad}(\Delta^{-1})\circ\iota$ は $\Delta\mapsto\Delta^{-1}$、$\delta\mapsto\delta^{-1}$ — **こちらも両生成元反転**である。$c\in N$ のとき $U=\bar\Delta$ は $U^2=1$ ゆえ $U^{-1}=U$ に**見える**だけだった。
> $$\boxed{\ \textbf{普遍形は「}(\gamma,\delta)\ \textbf{表示の両生成元を反転する」。}B_3\ \textbf{の }\iota(U)=U\ \textbf{は僥倖ではなく退化である。}\ }$$

> ### 補題 MIRROR-PSL-B4(candidate・本ノート)
> $\Delta_4^2\in\widetilde N$、$V=\bar\gamma$、$W=\bar\delta$、$\widehat Q=B_4/\widetilde N$ とすると
> $$\iota(\widetilde N)=\widetilde N\iff\exists\beta\in\mathrm{Aut}(\widehat Q):\ \beta(V)=V^{-1},\ \beta(W)=W^{-1}.$$
> **証明.** $\iota''$ は $\iota$ に内部自己同型を合成したもので、内部自己同型は正規部分群を動かさない ⟹ $\iota(\widetilde N)=\widetilde N\iff\iota''(\widetilde N)=\widetilde N$。$\iota''$ が $\widehat Q$ に降りることが右辺。∎

## 3.5 ★★★ 定理 MIRROR-ODD-B4(T8)

> ### 定理 MIRROR-ODD-B4(candidate・本ノート。名は `b4_mirror_transfer_design_v1.md` §4.2.1 で予約済・**証明は本ノート**)
> $\widetilde N\trianglelefteq B_4$、$\Delta_4^2\in\widetilde N$、$\widehat Q=B_4/\widetilde N$ とする。ある素数 $q\ge5$ について
> $$\textbf{(H4)}\qquad \mathrm{Syl}_q(\widehat Q)\ \text{が非自明・巡回・正規}$$
> が成り立てば $\boxed{\ \iota(\widetilde N)\ne\widetilde N\ }$。($\widetilde N\le PB_4$ は**不要**。)

**証明.** PSL-GEN-B4(§3.3 で PIN 完了)より $\widehat Q=\langle V,W\rangle$、$V^3=W^4=1$。

**(1) 正規閉包.** $\widehat Q_0:=\langle V^{\widehat Q}\rangle=\langle V,\,WVW^{-1},\,W^2VW^{-2},\,W^3VW^{-3}\rangle$。$\widehat Q/\widehat Q_0$ は $\bar W$ で生成 ⟹ $[\widehat Q:\widehat Q_0]\mid4$。$\widehat Q_0$ は位数が 3 を割る 4 元で生成 ⟹ $\widehat Q_0^{\rm ab}$ は指数 3 の初等可換 3-群。

**(2) $\mu(V)\ne1$($\iota$ を使わない).** $A:=\mathrm{Syl}_q(\widehat Q)=O_q(\widehat Q)$ は唯一ゆえ**特性**、巡回ゆえ $\mathrm{Aut}(A)$ 可換。$\mu:\widehat Q\to\mathrm{Aut}(A)$ を共役表現とする。$\gcd(q^k,4)=1$ ⟹ $A$ の $\widehat Q/\widehat Q_0$($\lvert\cdot\rvert\mid4$)での像は自明 ⟹ $A\subseteq\widehat Q_0$、したがって $A=\mathrm{Syl}_q(\widehat Q_0)\trianglelefteq\widehat Q_0$。
$\mu(V)=1$ と仮定すると、$\mathrm{Aut}(A)$ 可換ゆえ $\mu(W^iVW^{-i})=\mu(W)^i\mu(V)\mu(W)^{-i}=\mu(V)=1$ ⟹ $\mu(\widehat Q_0)=1$ ⟹ $A\le Z(\widehat Q_0)$。$A$ は正規 Hall ⟹ Schur–Zassenhaus で $\widehat Q_0=A\rtimes B$、中心的ゆえ $\widehat Q_0=A\times B$ ⟹ $\widehat Q_0^{\rm ab}$ が位数 $q\ge5$ の元をもつ — (1) の指数 3 に矛盾。ゆえに **$\mu(V)\ne1$**。

**(3) $\iota$ の排除.** $\iota(\widetilde N)=\widetilde N$ とすると補題 MIRROR-PSL-B4 の $\beta$ が存在。$A$ 特性ゆえ $h:=\beta|_A\in\mathrm{Aut}(A)$ で、任意の $g$ に対し $\mu(\beta(g))=h\mu(g)h^{-1}=\mu(g)$($\mathrm{Aut}(A)$ 可換)。$g=V$ に適用して
$$\mu(V)^{-1}=\mu(V^{-1})=\mu(\beta(V))=\mu(V)\ \Longrightarrow\ \mu(V)^2=1,$$
一方 $V^3=1$ ⟹ $\mu(V)^3=1$ ⟹ $\mu(V)=1$ — (2) に矛盾。∎

> ★ 既存予言 **P-B4-2**(「$B_4$ 版 MIRROR-ODD が紙で閉じる対の数 $=0$」)は **棄却**。墓標として記録。
> ★ **$W$ ではなく $V$(位数 3 側)を使う**のが要点。$B_3$ 版が $W$(位数 3)を使ったのと同じで、**位数 3 の生成元が反転で殺される**という構造が両方の心臓である。

## 3.6 命題 RW-NOS4 と軸③の答え(T9)

> ### 命題 RW-NOS4(candidate・本ノート・2 行)
> $P\trianglelefteq\widehat G$ が $p$-群($p\ge5$)で $\widehat G/P$ が巡回なら、$\widehat G$ は $S_3$ も $S_4$ も商にもたない。
> **証明.** $\varphi:\widehat G\twoheadrightarrow S_n$($n\le4$)なら $\varphi(P)$ は $S_n$ の正規 $p$-部分群 = $1$($\lvert S_n\rvert=n!$ は $p\ge5$ で割れない)⟹ $\varphi$ は巡回群 $\widehat G/P$ を経由 ⟹ 像可換、$S_n$($n\ge3$)非可換で矛盾。∎

> ### ★★ RW 系 no-go の $n=4$ 残存表(**委嘱「$n=4$ で消えるものはどれか」への答え**)
> | no-go | $B_3$ | $B_4$($\Delta_4^2\in\widetilde N$ 層) | 判定 |
> |---|---|---|---|
> | **RW-FRAT**(第 1 層は分裂 ⟹ $C_p\not\le\Phi$) | ✔ | ✔ **不変**(Schur–Zassenhaus は基底群に無関係) | **残存** |
> | **RW-NOWIN / TWIST-6**(ねじれ位数の上限) | ✔ 6 | ✔ **TWIST-12**、ただし $p=691$ で $\gcd(12,690)=6$ | **残存**(改善ゼロ) |
> | **RW-NOS3**(巡回トーラスに $S_3$ 商なし) | ✔ | ✔ **RW-NOS4**(同証明) | **残存** |
> | **RW-CYC**(巡回 Sylow ⟹ $6\mid q-1$) | ✔ | ✔ CYC-CHAR は $(\mathrm{ord}\,V,\mathrm{ord}\,W)=(3,4)$ でも同型 ⟹ $3\mid\mathrm{ord}\chi$、$2\mid\mathrm{ord}\chi$ ⟹ $\mathrm{ord}\chi\in\{6,12\}$、$6\mid q-1$ | **残存** |
> | **MIRROR-ODD**(巡回正規 Sylow ⟹ chiral・witness 算術) | ✔ | ★ **MIRROR-ODD-B4**(§3.5 で新規に成立) | **残存**(★ 委嘱の前提と逆) |
> | **ABEL-FIXED**(可換商 ⟹ $\iota$ 固定) | ✔ | ✔ ABEL-FIXED-B4(既在) | 残存 |
>
> $$\boxed{\ \textbf{軸③の答え: }n=4\ \textbf{で消える RW 系 no-go は「ひとつも無い」。}\ }$$

> ### ★ とくに $\widehat G_1$ 型巡回肥厚 $C_{691^2}\rtimes(-)$ について
> - **$B_3$**: §2.3 erratum E-1 により **「窓ですらない」**($(2,3)$-生成しない)。
> - **$B_4$**: $C_{691^2}\rtimes S_4$($\mathrm{Aut}(C_{691^2})$ 可換ゆえ作用は $S_4^{\rm ab}=C_2$ 経由 = 反転)では $\chi(V)=\mathrm{sgn}(3\text{-巡回})=1$ ⟹ **補題 CYC-CHAR で $(3,4)$-生成しない** ⟹ **窓でない**。仮に別構成で窓になったとしても MIRROR-ODD-B4 が発火する。
> $$\boxed{\ \textbf{巡回肥厚は }B_4\ \textbf{でも生き返らない(二重死: 非生成 + MIRROR-ODD-B4)。}\ }$$

---

# 4. 罠 DEPTH-WEIGHT(規約台帳へ上申)

**本節は新規探索ではなく、既在資料の突合で判明した用語の混同の指摘である。**

> ### 罠 DEPTH-WEIGHT
> - **窓側の目盛り**: $p$-群 $P$ の**下中心列の段**。工房既在の対応(定理 TRI-LCS・Lazard、`b_type_synthesis_design_v1.md` §1.1–§1.3)は
> $$\boxed{\ \textbf{窓の class}\ =\ \textbf{Lie 側の weight}\ }$$
> で、$\lvert P\rvert=p^{W(c)}$、$W(c)=\sum_{k\le c}\mathrm{Witt}(2,k)$、$W(12)=747$。
> - **Brown / Ihara の目盛り**: **depth** = $e_1$($=Y$)次数。**別のフィルトレーション**である。
> - 工房既在の申告(2 か所): 「**depth-graded を窓の言葉に翻訳する装置が無い**」(`aside_measurement_design_v1.md`、`counterexample_hotspots_ideation_v1.md` (J-iii))。さらに「(ℓ,w) 対応の工房版(class = weight)は **depth 1 でしか較正されていない**」。
>
> $$\Longrightarrow\ \boxed{\ \textbf{「Heisenberg は depth 2」は誤り。正しくは「weight(class)2」。}\ }$$
> **訂正申告(影響箇所)**: `_addendum_thick.md` §4 の「**depth 感受**: $H/Z$(深さ 1)・$Z(H)$(深さ 2)」の**深さの札は誤り**。ただし同じ枠の後半「$\Lambda^2(H/Z)\to Z$ = cup 積の群論版 ⟹ Sharifi の $\kappa\cup\kappa$ 住所」は**独立の主張であり、そちらは正しい**(交換子形式は実際に cup 積の双対であり、Heisenberg 埋め込み問題の障害は $\chi_1\cup\chi_2$ である — 詳細な定式化は本納品の範囲外・§7)。
>
> ### ★ 逐語事実との突合(`docs/scout/brown_eq14_verbatim_v1.md`)
> | 場所 | 式 | 691 |
> |---|---|---|
> | (1.7) dg$^{\mathfrak m}$、**weight 12・depth 2** | $\{\bar\sigma_3,\bar\sigma_9\}-3\{\bar\sigma_5,\bar\sigma_7\}=0$ | **現れない**(有理的に厳密成立) |
> | (8.8) $\mathfrak g^{\mathfrak m}$、**weight 12・depth 4** | $\{\tilde\sigma_3,\tilde\sigma_9\}-3\{\tilde\sigma_5,\tilde\sigma_7\}=\frac{691}{144}e_{12}$ | **分子**(depth 4) |
>
> ⟹ **691 の住所は (weight 12, depth 4)**。窓側が持つ目盛りは weight のみであり、weight 12 に届くには class 12 = $\lvert P\rvert=p^{747}$ が要る。
> $$\boxed{\ \textbf{窓の class 梯子から 691 に触れる経路は、目盛りの点でも規模の点でも開いていない。}\ }$$
> ⚠ この判定は **weight 側の規模**についてのものであり、「B 型が窓側に無い」という主張ではない(それは別の論点・§7)。

---

# 5. 検算指示(**紙の定理の確認のみ**・新規測定の設計ではない)

本納品の定理を機械で**確認**したい場合の最小手順。すべて既存装置で数秒〜分。**新しい宇宙の登録も帯の拡大も要求しない。**

| # | 対象 | 確認内容 | 予測(紙の値) |
|---|---|---|---|
| **V-1** | $G_p$、$p\in\{5,7,11,13\}$ | $\lvert G\rvert$、$G^{\rm ab}$、$\lvert Z(G)\rvert$、$\Phi(G)$、$\mathrm{Syl}_p$ の構造、$(2,3)$-生成 | $6p^3$、$C_2$、$1$、$C_p$、非巡回(extraspecial)、生成する |
| **V-2** | 同上 | $G_p$ と $R_0(p)=G_p/Z$(位数 $6p^2$)の $(2,3)$-生成の一致 | 一致(§1.3 の系) |
| **V-3** | 同上 | **Test ORB**(§F.8 の既存指示書)で標識対が $\iota$-固定か | **reflexible**(定理 LADDER-REFL) |
| **V-4** | $R_0(p)$、$M=\mathbf F_p(\mathrm{sgn})$ | `OneCohomology` / `TwoCohomology` の次元 | $(\dim H^1,\dim H^2)=(0,1)$ |
| **V-5** | $G_p$、$p\in\{5,7\}$ | 生成 $(2,3)$-標識対の個数、$\lvert\mathrm{Aut}(G_p)\rvert$、$\mathrm{Aut}$-軌道数 | $6p^3(p-1)$、$6p^3(p-1)$、**1**(定理 LADDER-UNIQ-N) |
| **V-6** | $C_{p^2}\rtimes S_3$(反転作用)、$p\in\{5,7\}$ | $(2,3)$-生成の**不成立** | 生成しない(erratum E-1 / CYC-CHAR)— **fail-closed 較正**(誤って窓と判定したら実装バグ) |
| **V-7** | ★ 既存 LINS 走行 | 指数 750 の**全 node**(twin に限らない)の `in_PB3 / c_in_N / id_group` | $G_5$ が `in_PB3=True, c_in_N=True` で**ちょうど 1 node**・twin に属さない;`[750,6]` は `in_PB3=False` |
> ⚠ **V-7 は現行 cert では実行できない**: `search/certs/lins_twin_census_v1_20260806.json` は `twin_pairs` しか持たず(キー: `generated_by, ruling, note, census_index_hi, pb3_index_in_b3, lins_nodes_total_this_call, lins_elapsed_ms, idx1_count, rows_processed, pair_checks, twin_pairs_found, total_elapsed_ms, twin_pairs`)、単独 node の一覧が無い。実行するには既存スクリプトの**出力を全 node ダンプに広げた派生**が要る(LID-1 規律継承・`census_index_hi=1000` は変えない)。**発注の可否は司令塔裁定**。

---

# 6. novelty grep(実施済・`docs/` `provenance/` `sol/` 全域)

| 語 | hit |
|---|---|
| `LADDER-WIN` / `LADDER-UNIQ` / `LADDER-REFL` / `LADDER-UNIQ-N` / `DET-FORCED` | **0**(本ノート初出) |
| `TWIST-6` / `TWIST-12` / `RW-NOEIG` / `RW-CYC` / `CYC-CHAR` / `CHIR-DIM` | **0**(本ノート初出) |
| `MIRROR-PSL-B4` / `SG-AB-B4` / `RW-NOS4` / `WIN-B4-NEC` / `IOTA-NORM-B4` | **0**(本ノート初出) |
| `MIRROR-ODD-B4` | **2**(`b4_mirror_transfer_design_v1.md` §4.2.1・§9.4 で**名前だけ予約**され「【GAP-B4-5】が閉じれば成立」と記載)⟹ **名の帰属は同 v1.3(数学者)と共有・証明は本ノート** |
| `Heisenberg` | 33 ファイル(既在語)⟹ **$H_{p^3}\rtimes S_3$ の族としての定式化と窓資格の $p$ 一様定理**が初出部分 |

---

# 7. 【GAP】と**未納品**の明示(裁定 713 に従う)

## 7.1 未閉の穴(納品分に付随するもの)

| # | 内容 | 重さ |
|---|---|---|
| **【DIG-GAP-1】** | 本ノートの全命題は **candidate(単系統・Sol 未監査)**。**TWIST-6 / RW-CYC / MIRROR-ODD-B4 / LADDER-\* を確定として引用しない。** | — |
| **【DIG-GAP-2】** | $\lvert\mathrm{Out}(G_p)\rvert=p-1$ の**上界**は「軌道数 $\ge1$」から逆算した。$\mathrm{Aut}(G_p)$ の直接決定はしていない(結論は同値だが独立確認ではない)。$p=5,7$ の生成対数一致が間接的支持 | 小 |
| **【DIG-GAP-3】** | **定理 SG-EXACT-B4 は未完**(十分性)。$\psi:B_4\to S_4$ で $\psi(\sigma_i)$ が互換であること(4-巡回の排除)が未証明 ⟹ WIN-B4-NEC は**必要条件のみ** | 中 |
| **【DIG-GAP-4】** | RW-CYC の陰性側(「$q\equiv5\ (6)$ の窓は存在しない」)は twin cert の 13 行での**陽性一致**にとどまり、悉皆主張ではない(V-7 が必要) | 中 |
| **【DIG-GAP-5】** | LADDER-REFL の $H^1/H^2$ 会計は $R=V\rtimes S_3$($V$ 初等可換)の場合の計算。**梯子を class 3 以上に上げると $R$ が初等可換でなくなり、そのままでは使えない** | 中 |

## 7.2 ★ 未納品(裁定 713 により中止・次版送り)

以下は委嘱 707 の項目のうち、**本納品に含めなかったもの**である。中途半端な形で混ぜないため、明示的に「無い」と書く。

| 委嘱項目 | 状態 |
|---|---|
| **軸①(b) 中心予想 HR-WIN**(「$G_p$ の算術飽和は $p$ の正則性で二分される」の IF-FIRST 起票) | ★ **未納品**。起票の作業は行ったが、**証明も反証もできていない**ため裁定 713 の範囲外とした。★ ただし本納品の **定理 TWIST-6 は予想に不利な構造的証拠**である(Herbrand–Ribet 固有空間 $\omega^{1-k}$ の位数が $6$ を超えると窓に映らない;$(691,12)$ では $690$)。この 1 行だけ記録に残す |
| **軸②(a)** FRAT-CHIR の $\mathbf F_p$ 一般化の**完全な変更点表** | 部分納品。$G_p$ に必要な範囲(§1.5・補題 CHIR-DIM)のみ |
| **軸②(b)** Eisenstein ideal の窓側 avatar | ★ **未納品**(構造的類比のみで定理が無い) |
| **軸②(c)** $\Lambda^2(H/Z)\to Z$ と $\kappa\cup\kappa$ の精密対応 | ★ **未納品**(§4 で「後半は正しい」とだけ記録。Koch 公式経由の定式化は符号規約が未 pin) |
| **軸④** E-DIM 橋の対応表 | ★ **未納品**。§4 の罠 DEPTH-WEIGHT(用語の混同の指摘と Brown 逐語との突合)のみ納める |
| **軸⑤** 小 $p$ 較正計画・測定梯子・宇宙事前登録 | ★ **未納品**。§5 の「紙の定理の確認手順」に縮小した(新規宇宙の登録・帯の拡大は要求しない) |
| 発案札 RDG-1..10 の検証・採否 | ★ **中止**(裁定 713) |

## 7.3 帰属

- **委嘱・戦役設計**: 研究者(逐語指示)+ 司令塔(裁定 707 / 713)。
- **$G_p=H_{p^3}\rtimes S_3$ の同定・RW-GAP-5/6 の起票**: 数学者(`_addendum_thick.md` §4)。
- **本ノートの新規部分**: DET-FORCED / LADDER-WIN / LADDER-UNIQ / LADDER-REFL / LADDER-UNIQ-N / CHIR-DIM / CYC-CHAR / **RW-CYC** / **TWIST-6** / RW-NOEIG / **TWIST-12** / SG-AB-B4 / WIN-B4-NEC / RW-NOS4 / **IOTA-NORM-B4(【GAP-B4-5】閉)** / **【PIN-B4-2】閉** / **MIRROR-ODD-B4 の証明** / 罠 DEPTH-WEIGHT / erratum E-1・E-2。
- 既在道具(すべて工房既在): FRAT-SPLIT / MIRROR-ODD / Tool R2′ / MIRROR-PSL / SG-AB / SG-S3 / SG-EXACT / FRAT-CHIR / PSL-GEN-B4 / FLIP-INNER / (D2) / ABEL-FIXED-B4 / INDEX-LB / TRI-LCS。
- 逐語文献: Brown 1301.3053(`docs/scout/brown_eq14_verbatim_v1.md` 経由)。Ribet / Mazur / Sharifi / WWE は**本納品では使っていない**(§7.2 の未納品項目でのみ必要だった)。

## 7.4 次の一手(司令塔裁定用・優先順)

1. **Sol 便への積荷**: **TWIST-6 / RW-CYC / LADDER-WIN / MIRROR-ODD-B4** の 4 本。いずれも証明が短く、監査費用に対して効用が大きい(no-go の族一様化 + $B_4$ 側の open GAP 2 本の閉鎖)。
2. **erratum E-1 / E-2 の台帳反映**(**P-RW-1..3 の取り下げ**)。
3. **V-1 〜 V-3(秒〜分)**: 梯子カナリアと Test ORB。★ 走行中の Ĝ₂ 関門は §1.3 により**確認**に降格 — 位数 $2\times10^9$ の走行は不要で $R_0(691)$(位数 2,864,886)で足りる。**必ず $S_3$-作用が忠実標準表現であることを突合すること**(定理 LADDER-UNIQ)。
4. **【PIN-B4-2】【GAP-B4-5】の閉鎖を `b4_mirror_transfer_design_v1.md` の穴一覧へ反映**(v1.4 として)。
5. V-7(LINS 全 node ダンプ)の発注可否。実行すれば RW-CYC の陰性側が指数 $\le1000$ で悉皆主張になる。
