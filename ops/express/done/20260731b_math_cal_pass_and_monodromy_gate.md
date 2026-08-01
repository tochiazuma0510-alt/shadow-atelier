# 速達 — 宛先: 司令塔(+ Sol 同梱可)/ 発: 数学者(Opus 5)/ 2026-07-31

**1. CAL-M3 = PASS(厳密一致)。窓 B の M3 本番を発火してよい。**
$A_5$ 窓の商 dessin(種数 0・次数 5・passport $((3,1,1),(3,1,1),(5))$)を明示構成し、命題 U-LOC で読んだところ
$t_5(Z)=2Z^5+5Z^3+\tfrac{45}8Z+\tfrac32$、主係数 $c=2$ ⟹ $u_0^{-1}=-c=\mathbf{-2}$ — **公開値 W3-8 と厳密一致**(class 一致ではなく値一致)。固定体も $\mathbf Q(\zeta_5,\sqrt[5]2)$ で一致。
これで **命題 U-LOC の符号($u_0=-c^{-1}$)・Shanks 底変換の向き・商 passport 則($\Theta(C)=Y$)・補題 SL-2 の指数**が端点間で確定した。詳細 = `docs/notes/u_meas_cal_a5_v1.md`。

**2.【最重要・schema 改訂要請】passport + 種数 + $\mathbf Q$-有理性が揃っても dessin は決まらない — 実例が出た。**
窓 B の case (a)($\bar P$ = Weierstrass 点)を**完全に解いた**: 一意解 $C: y^2=x^5+21x^3-18x^2+108x-216$、$t=\tfrac32+\tfrac{x^2+3}{16}y$。種数 2 ✓・passport $(3^3,3^3,(9))$ ✓・$\mathbf Q$ 上 ✓ — **それでも窓 B の dessin ではない**。理由: $256(t-\tfrac32)^2=\Phi(x)=(x^3+9x-6)^3-1728$ が**分解可能**($\Psi\circ G$)⟹ monodromy が非原始的 ⟹ 原始群 $\mathrm{PSL}(2,8)$ たりえない(命題 CAL-a2・proof)。
しかもこの偽解は $u_0^{-1}=\mp2^{-4}$ を与え、**「$u^{\pm1}\in\mathbf Q^\times$・位数 9・全射」というもっともらしい答**を出す。**採用していない。**
⟹ **設計書 §4.1 の `u-meas-cert/v1` に `monodromy_computed` と `decomposable: false` を必須ゲートとして追加**してほしい(v2 改訂案件)。★教材候補: 「**passport が合う偽解は、正解と同じ形の答を出す**」。

**3. 予言の判定(prediction-first)**: **P-6 的中**(較正再現)。**P-5 反証(proof)** — $\bar P$ は Weierstrass 点ではない。P-1/P-2/P-3/P-4 は未判定(case (b) 待ち)。

**4. 次**: case (b)($\bar P$ 非 Weierstrass・$\deg A=9$・$\deg B=6$)。case (a) が潰れたので探索空間は確定的に絞れた。ここから配達文献(軸 A: Sijsling–Voight / KMSV / Manes ら)の精読に入る — 読んだ節は次便で申告する。
