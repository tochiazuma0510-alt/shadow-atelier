# CAL-M3 — $A_5$ 窓での商経路の端点間較正 **PASS**、および窓 B の case (a) 決着

**状態札: `calibration PASSED (exact) / 紙 + sympy 単系統・Sol 監査前`**
起草: 影工房 数学者(Claude・Opus 5)/ 2026-07-31
委嘱: 裁定 244 項 3(**M3 の入口条件 = $A_5$ 端点間較正**)
前提正本: `docs/notes/u_meas_m1_passport_v1.md`(M0–M2 凍結)/ `docs/notes/u_meas_m3_design_v1.md`(§1.2 命題 U-LOC・§1.5 CAL-M3・§6 予言)

> ## 汚染管理
> $A_5$ の $u^{-1}=-2$ は**公開値**(`surj_s4_v2` §4 先例欄・台帳 W3-8)であり封印外。較正の的として使うことは設計書 §1.5 で**測定前に**宣言済み。**窓 B の値を見た後に較正をやり直していない**(本書時点で窓 B の $u$ は未確定 — §2)。

---

## 0. 結論(4 行)

1. **CAL-M3 = PASS。しかも class 一致ではなく厳密一致**: 商経路 + 命題 U-LOC が $A_5$ 窓の公開値 **$u^{-1}=-2$ を厳密に再現**した(自然な有理正規化 $Z\mapsto Z/2$ のもとで)。
2. **⟹ 命題 U-LOC($u_0=-c^{-1}$)と Shanks 底変換の向き・符号がすべて正しいことが端点間で確認された。** 窓 B の本番を発火してよい(設計書 §1.5 の fail-closed ゲート通過)。
3. **窓 B の case (a)($\bar P$ が Weierstrass 点)は完全に解け、しかも「別の dessin」であることが証明された** — 解が $\Phi=G^3-1728$ という**分解可能**多項式を与え、monodromy が非原始的になるため。**⟹ 予言 P-5 は反証。$\bar P$ は Weierstrass 点ではない。**
4. **次の一手は case (b)**($\bar P$ 非 Weierstrass・$\deg A=9$・$\deg B=6$)。case (a) を潰したことで探索空間は確定的に絞られた。

---

## 1. CAL-M3($A_5$ 窓)— **PASS(厳密一致)**

### 1.1 底変換の検算(窓非依存)

sympy で厳密確認(`u_meas_cal_a5.py`):

| 検算 | 結果 |
|---|---|
| $t:=\lambda+\frac1{1-\lambda}+\frac{\lambda-1}{\lambda}$ が $\lambda^3-t\lambda^2+(t-3)\lambda+1=0$ を満たす | **True** |
| $t(1-\lambda)=3-t(\lambda)$($S_3$ の対合が $t\mapsto3-t$ を誘導) | **True** |
| $\mu$ の固定点 $\iff$ $t^2-3t+9=0$、$\tau_1+\tau_2=3$、$\tau_1\tau_2=9$ | **True**($\tau=\tfrac32\pm\tfrac{3\sqrt3}{2}i=3\zeta_6^{\pm1}$) |

### 1.2 $A_5$ 窓の商 dessin の明示構成

**passport**(M1 §3.5 の一般則を $M=5$ に適用): $\Theta(A),\Theta(B)$ は $A_5$ の位数 3 の元 ⟹ 5 点上の型 $(3,1,1)$、$\Theta(C)=Y$ は 5-巡回。RH: $2g_C-2=-10+2+2+4=-2$ ⟹ **$g_C=0$**。

$C\cong\mathbf P^1_Z$、$t$ は $\bar P=\infty$ に 5 位の極をもつ ⟹ **$t$ は $Z$ の 5 次多項式**。分岐は $\tau_1,\tau_2$ 上に 3 重点が 1 個ずつ ⟹ $t'=5c\,g(Z)^2$、$g$ = その 2 点を根にもつモニック 2 次式。2 点は $\mathbf Q(\sqrt{-3})$ 上共役ゆえ $Z\mapsto Z+\beta$ で根の和を 0 に、$Z\mapsto\gamma Z$ で $g=Z^2+3$ に正規化できる。積分して

$$\boxed{\ t_5(Z)=c\,(Z^5+10Z^3+45Z)+\tfrac32,\qquad c=\pm\tfrac1{16}\ }$$

($t_5(\pm\sqrt{-3})=\tfrac32\pm\tfrac{3\sqrt{-3}}2=\tau_{1,2}$ から定数項 $\tfrac32$ と $24c=\pm\tfrac32$ が出る。)

**機械確認**: $t_5'=5c(Z^2+3)^2$ ✓ / $t_5(\pm\sqrt{-3})$ が $t^2-3t+9=0$ の根 ✓ / $Z=\pm\sqrt{-3}$ の重複度が**ちょうど 3** ✓。
**monodromy**: 次数 5(素数)ゆえ**分解不可能**、$\infty$ 上単一点で推移的、生成元 2 個は 3-巡回型で偶 ⟹ $\langle\cdot\rangle=A_5$(5 点上推移で 3-巡回を含む群は $A_5$ か $S_5$、偶なので $A_5$)✓。**剛性**: 上の導出で解が一意(正規化を除く)⟹ passport 内で唯一 ✓(`week4-A5算術飽和_v4.md` 補題 FC-4(b) の「$S_5$-軌道は 1」と整合)。

### 1.3 命題 U-LOC の適用と厳密一致

$s=1/Z$($\mathbf Q$-有理助変数)で $t_5=c\,s^{-5}(1+O(s))$。命題 U-LOC($M=5$ 版):
$$u_0=-c^{-1}=\mp16,\qquad u_0^{-1}=\mp\tfrac1{16}=\mp2^{-4}.$$
$$\frac{u_0^{-1}}{-2}=\frac{-2^{-4}}{-2}=2^{-5}\in\mathbf Q^{\times5}\ \Longrightarrow\ \boxed{[u_0^{-1}]_5=[-2]_5\ \ \text{(class 一致)}}$$

**さらに厳密一致**: 助変数を $s\mapsto2s$(= 座標 $Z\mapsto Z/2$)に取り替えると $u_0^{-1}\mapsto u_0^{-1}\cdot2^5$(補題 SL-2)。実際
$$t_5(2Z_n)=2Z_n^5+5Z_n^3+\tfrac{45}8Z_n+\tfrac32\ \Longrightarrow\ c_{\rm new}=2\ \Longrightarrow\ u_0=-\tfrac12,\quad \boxed{u_0^{-1}=-2}$$
$$\boxed{\ \textbf{公開値 }u^{-1}=-2\ \textbf{と厳密に一致。CAL-M3 = PASS。}\ }$$
固定体も $L=K\bigl((u^{-1})^{1/5}\bigr)=\mathbf Q(\zeta_5,\sqrt[5]{-2})=\mathbf Q(\zeta_5,\sqrt[5]2)$ ✓(W3-8 と一致)。

> ### 較正で確認されたもの(名指し)
> | # | 項目 |
> |---|---|
> | C-1 | **命題 U-LOC の符号と指数**: $\lambda=-t^{-1}-2t^{-2}+\cdots$、$u_0=-c^{-1}$。逆($u_0=-c$)なら class は同じでも**厳密値が合わない**ので、この一致は向きまで確定させた |
> | C-2 | **Shanks 底変換の向き**($t=e_1(\lambda)$、$\lambda^3-t\lambda^2+(t-3)\lambda+1=0$) |
> | C-3 | **商 dessin の passport 則**(M1 §3.5・$\Theta(A)=\pi^{-1}$、$\Theta(B)=X^{-1}\pi$、$\Theta(C)=Y$)— これが誤っていれば $g_C$ が変わり $t$ の次数が変わって一致しない |
> | C-4 | **分岐点 $\tau^2-3\tau+9=0$ の同定**と $\mathbf Q$-正規化の手順 |
> | C-5 | **補題 SL-2 の助変数依存則** $u\mapsto ua^{-M}$ の符号 |

---

## 2. 窓 B — case (a) の完全決着(**P-5 = 反証**)

### 2.1 case (a) は一意に解ける

$C:y^2=f_5(x)$、$\bar P=\infty$(Weierstrass 点)、$t=A(x)+B(x)y$。$\mathrm{ord}_\infty(t)=-2\deg B-5=-9$ ⟹ $\deg B=2$。

> **補題 CAL-a1**(case (a) では $A\equiv\tfrac32$)【proof】
> $\mathcal N_{\tau_i}:=(A-\tau_i)^2-B^2f_5=\kappa_i g_i^3$($g_i$ モニック 3 次)。$\deg\mathcal N_{\tau_i}=9$ で最高次係数は $-\mathrm{lc}(B)^2\mathrm{lc}(f_5)$(**$\tau_i$ に依らない**)⟹ $\kappa_1=\kappa_2=:\kappa$。
> $\mathcal N_{\tau_1}-\mathcal N_{\tau_2}=(\tau_2-\tau_1)(2A-3)$ は次数 $\le4$。一方 $\kappa(g_1^3-g_2^3)=\kappa(g_1-g_2)(g_1^2+g_1g_2+g_2^2)$ で第 2 因子は次数ちょうど 6(最高次係数 3)。⟹ $g_1=g_2$ かつ $A=\tfrac32$。∎

⟹ $\mathcal N_\tau=-\tfrac{27}4-B^2f_5=\kappa g^3$。$P:=B^2f_5=\kappa'g^3-\tfrac{27}4$($\kappa'=-\kappa$)は**ちょうど 2 個の 2 重根**($B$ の根)をもつ必要がある。$P'=3\kappa'g^2g'$ で $g$ の根は $P=-\tfrac{27}4\ne0$ ゆえ不可 ⟹ **2 重根は $g'$ の根**。$g=x^3+px+q$(depressed)、$g'$ の根 $\pm\rho$($p=-3\rho^2$)、$m:=2\rho^3$ とすると条件 $g(\rho)^3=g(-\rho)^3$ は $m(3q^2+m^2)=0$。
$m=0$ は 3 重根を生んで型が合わない。$m^2=-3q^2$ から $4p^3=81q^2$、有理解は **$p=9z^2,\ q=\mp6z^3$ に限る**(機械確認)。$x\mapsto x/z$ で

$$\boxed{\ g(x)=x^3+9x-6,\qquad \kappa'=\tfrac1{256},\qquad \mathcal N_\tau=-\tfrac1{256}\,(x^3+9x-6)^3\ }$$

**機械確認(sympy・厳密)**:
$$\Phi(x):=(x^3+9x-6)^3-1728=(x^2+3)^2\,(x^3+9x-18)(x^2+12)\quad\textbf{True}$$
$$B=\tfrac{x^2+3}{16},\qquad f_5=(x^3+9x-18)(x^2+12)=x^5+21x^3-18x^2+108x-216,\qquad B^2f_5=\tfrac{\Phi}{256}\ \textbf{True}$$
$f_5$ は**平方因子なし・次数 5** ⟹ 種数 2 ✓。$t=\tfrac32+\tfrac{x^2+3}{16}y$、$\bar P$ での主係数 $c=\pm\tfrac1{16}$。

### 2.2 ★ しかしこれは窓 B の dessin ではない【proof】

> ### 命題 CAL-a2(case (a) の棄却)
> case (a) の解の monodromy は**非原始的**であり、$\mathrm{PSL}(2,8)$ ではありえない。したがって **$\bar P$ は Weierstrass 点ではない**。

**証明.** $t=\tfrac32+By$ と $y^2=f_5$ から $256\bigl(t-\tfrac32\bigr)^2=(x^2+3)^2f_5(x)=\Phi(x)$。すなわち $x$ は
$$\Phi(x)=256\bigl(t-\tfrac32\bigr)^2$$
の根で、$\mathbf Q(C)=\mathbf Q(x)\cdot\mathbf Q(t)$、$\mathbf Q(x)\cap\mathbf Q(t)=\mathbf Q(T)$($T:=256(t-\tfrac32)^2$)、$[\mathbf Q(t):\mathbf Q(T)]=2$、$[\mathbf Q(x):\mathbf Q(T)]=9$。ゆえに
$$\mathrm{Mon}\bigl(C/\mathbf P^1_t\bigr)\ \le\ \mathrm{Mon}\bigl(\Phi:\mathbf P^1_x\to\mathbf P^1_T\bigr)\quad(\text{指数}\le2\ \text{の部分群}).$$
ところが $\Phi=\Psi\circ G$、$\Psi(u)=u^3-1728$、$G(x)=x^3+9x-6$ — **$\Phi$ は分解可能**。したがって $\mathrm{Mon}(\Phi)$ は $G$ のファイバー(大きさ 3 のブロック 3 個)を保つ**非原始群**。$\mathrm{PSL}(2,8)$ は $\mathbf P^1(\mathbf F_8)$ 上**原始的**(点安定化群 Borel は極大)なので、非原始群の部分群にはなれない。$\blacksquare$

**整合の副検算**: $\Phi'=9(x^3+9x-6)^2(x^2+3)$ ⟹ $\Phi$ の分岐は $T=-1728$(型 $3^3$)・$T=0$(型 $2^21^5$)・$T=\infty$(型 $(9)$)。$\mathbf P^1_t\to\mathbf P^1_T$($T=256(t-\tfrac32)^2$)は $T=0,\infty$ で分岐し、$T=-1728$ の上は $t=\tfrac32\pm\tfrac{3\sqrt{-3}}2=\tau_{1,2}$ ✓。ファイバー積の分岐計算で $C\to\mathbf P^1_t$ は $\tau_1,\tau_2$ 上 $3^3$・$\infty$ 上 $(9)$・$t=\tfrac32$ 上不分岐 ⟹ $2g_C-2=-18+6+6+8=2$、$g_C=2$ ✓。**passport も種数もすべて合っているのに monodromy だけが違う** — M1【FINDING U-1】(passport は dessin を決めない)の実物である。
なお $\mathrm{PSL}(2,8)$ の対合は $\mathbf P^1(\mathbf F_8)$ 上で型 $2^41$ であり、$\Phi$ の $T=0$ 上の型 $2^21^5$ とは合わない — これも独立の不整合。

### 2.3 予言の判定(prediction-first の記録)

| 予言(設計書 §6 で測定前に凍結) | 判定 |
|---|---|
| **P-5**「$\bar P$ は Weierstrass 点」(弱い予想と自己申告) | **✗ 反証(proof)。命題 CAL-a2。** |
| **P-6**「CAL-M3 が $A_5$ の既知値 $-2$ を再現する」 | **✓ 的中(しかも厳密一致)** |
| P-1(窓 B の $u_0^{\pm1}\in\mathbf Q^\times$)・P-2(位数 9 ⟹ 全射)・P-3・P-4 | **未判定**(窓 B の case (b) 未解) |

> **⚠ 誘惑の記録(汚染防止のため明記)**: case (a) の解は $u_0^{-1}=\mp2^{-4}$、すなわち $[u_0^{-1}]_9=[2]_9^{-4}$ を与え、$2$ が $\mathbf Q$ の 3 乗でないことから「位数 9 = 全射」を導いてしまう。**これは P-1/P-2 の的中に見えるが、命題 CAL-a2 により当該 dessin は窓 B のものではない。したがってこの値は採用しない。** 記録に残すのは、**同じ passport の別成分から「もっともらしい値」が出うる**という危険の実例だからである(★教材候補)。

---

## 3. 次の一手 — case (b) の系

$\bar P=\infty_+$(非 Weierstrass)、$C:y^2=f_6(x)$($f_6$ モニック)。$\mathrm{ord}_{\infty_\pm}(x)=-1$、$y\sim\pm x^3$。$t=A(x)+B(x)y$ が $\infty_-$ で極をもたない条件から
$$\deg B=6,\qquad \deg A=9,\qquad A-Bx^3\bigl(1+O(x^{-1})\bigr)\ \text{が有界},$$
$\deg\mathcal N_\tau=9$(極因子 $9(\infty_++\infty_-)$)。**補題 CAL-a1 の論法は $\deg A=9$ ゆえ働かない**($\mathcal N_{\tau_1}-\mathcal N_{\tau_2}$ の次数が 9 になる)⟹ $A$ は定数でなく、$\kappa_1\ne\kappa_2$ もありうる。

**実装方針**(設計書 §1.4 の推奨 1 を継承):
1. $t$ の極が 1 点に集中する形を扱いやすくするため、$\bar P$ を有限点へ移す座標変換(または $\infty_\pm$ を $x=0,\infty$ に置く $f_6$ の正規化)を先に固定する。
2. **mod-$p$ 悉皆 → 有理再構成 → $p$ 進 Newton**。命題 U-Q($\mathbf Q$-有理性)が保証されているので再構成が効く。
3. **必須の篩**: 得た候補について **(i) $\Phi$-型の分解可能性が無いこと**(命題 CAL-a2 の再演を防ぐ)**(ii) monodromy が $\mathrm{PSL}(2,8)$ であること**を必ず確認する。**passport と種数の一致だけでは不十分**であることが §2 で実証された。
4. 安価な独立篩として M7-B4($\mathrm{Jac}(C)^\vee[3]$ に $\mathbf Q$-有理な位数 3 の元)を併用(文献配達の軸 B に接続。**ただし型 C 警戒: 我々は単一 $C_3$ であって $\mathbf Z_3\times\mathbf Z_3$ ではない**)。

> ### 【M3-f】新規の未閉鎖
> **「passport + 種数 + $\mathbf Q$-有理性」が揃っても dessin は決まらない。** 窓 B の M3 の受理条件に **monodromy 判定を必須ゲートとして入れる**(証明書 schema `dessin_binding.monodromy_T_label` を計算値で埋め、`decomposable: false` 欄を追加する)。設計書 §4.1 の schema を v2 で改訂すること。

---

## 4. 出所

| ファイル | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/u_meas_cal_a5.py` | `533bb6d2be0b9dfafc075fb5fcc16ef37f0158122f5210d54402118df3240545` | CAL-M3 の厳密検算 + 窓 B case (a) の恒等式(sympy 1.14.0・浮動小数点不使用) |

> **⚠ スクリプトの自認**: 出力行 `N_tau = -27/4 - B^2 f5 = -(1/256) Phi` は **False** と表示されるが、これは**検査式の書き間違い**である。正しい恒等式は $\mathcal N_\tau=-\tfrac{27}4-B^2f_5=-\tfrac1{256}(x^3+9x-6)^3$ で、別途 `sp.expand(-27/4 - B**2*f5 + G**3/256)==0` が **True** を返すことを確認した(本文 §2.1 の値はこちらが根拠)。同じ行の $\Phi$ の因数分解と $B^2f_5=\Phi/256$ はいずれも **True**。

**環境**: python + sympy 1.14.0。**単系統。cross-checked ではない。Lean verified ではない。**
**文献**: 配達分(`litgate_positive_genus_belyi_v1.md` および `papers/delivered/`)は**本書の時点で未読**(較正は自前の初等計算のみで閉じたため)。精読は case (b) 着手時に軸 A(Sijsling–Voight / KMSV / Manes ら)から始める予定 — **読んだ節・定理番号はそのとき申告する。**
