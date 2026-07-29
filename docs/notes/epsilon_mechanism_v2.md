# ε 機構ノート v2 — 持ち上げ位数の定式化・M-1P/M-1c 分割・測定契約

作成: 数学者(Opus 5)・2026-07-30(裁定 214 工程 1)
**本ノートが正本**。`docs/notes/epsilon_mechanism_v1.md` は**凍結**(erratum 方式・上書きしない)。
入力: Sol 便 85(`sol/sol_reply_85_math12.md` §4)の F85-4.1〜4.5・P85-3・P85-4 / v1 / 梯子証明書 `search/certs/epsbits_a13_ladder_20260730.json`
関係: 構造定理の正本は `docs/notes/structthm_h2_v2.md`(STR-1 v2)。凍結済み予言(41b8698)非接触。

---

## 0. v1 からの差分(erratum 一覧)

| # | v1 の記述 | 判定 | v2 での処置 |
|---|---|---|---|
| E-1 | M-1「centralizing $\Rightarrow\mathcal N_{T,n}(f)=1$」 | **FAIL**(F85-4.2:型落ち) | **$\mathcal N\in A$ へ型訂正**。さらに **M-1P / M-1c へ分割**(P85-3)。「$\mathcal N=1$」は梯子 `W-E-A10-9t1` で**反証済** |
| E-2 | M-1 が単独で $\varepsilon=0$ を含意 | **FAIL**(F85-4.3:冪ビットから交差ビットは出ない) | **M-1P と M-1c の両方**で初めて $\varepsilon=0$。P-EPS-2 を「$\varepsilon=0$ の検査」と呼ぶのを**禁止** |
| E-3 | 「188/188」(便面の会計) | **FAIL**(F85-4.4:単位混合) | **分計**: D4 三窓 164/164 shadow-level / 梯子 24/24 layer-level。**いずれも交差ビット検査数ではない**と明記 |
| E-4 | P-EPS-5(存在主張) | **FAIL**(F85-4.5:反証不能) | **P-EPS-5′** へ指名凍結の量化 |
| E-5 | §3.1 の raw cocycle 式(shadow 積で書いた形) | 導出未添付 | **group-level cocycle $g_ug_vg_{uv}^{-1}\bmod A$ を正本**に。shadow 積規約からの導出は付録扱い(未完) |
| — | $(P,c)$ と次元公式・$u=-1$ ビット同定・素点分解・§4 型 I | **PASS**(F85-4.1) | 維持 |

> **E-1〜E-5 はいずれも私(起草者)の責**。ただし証明済部分(§1・§2・§3.2 の位数=ノルム公式)は健在で、修理は主張の**型と量化**に限られる。

---

## 1. 【LG-1】持ち上げ位数による正式化(v1 §1 から変更なし・F85-4.1 で PASS)

$\tilde G:=C_G(S)/A$、$1\to\langle z\rangle\to\tilde G\to Q\to1$(中心拡大)、$\varepsilon=[\tilde G]\in H^2(Q;C_2)$。

> **補題 A**. $x\in Q$ 偶位数 $n$ に対し $P(x):=[\tilde x^{\,n}=z]\in\mathbb F_2$ は持ち上げによらない($(\tilde xz)^n=\tilde x^n$)。$c(x,y):=[[\tilde x,\tilde y]=z]$ も同様、双線型交代。
> **補題 B**. $Q$ 有限アーベル、$Q_2=\langle a_1\rangle\times\cdots\times\langle a_r\rangle$(各位数偶)のとき
> $$\varepsilon\longmapsto\bigl((P(a_i))_i,(c(a_i,a_j))_{i<j}\bigr):H^2(Q;C_2)\xrightarrow{\ \sim\ }\mathbb F_2^{\,r+\binom r2}.$$
> **定理 LG-1**. $\varepsilon=0$ $\iff$ **$Q_2$ の(不変因子)基底が全て同位数で持ち上がり、かつ持ち上げが互いに可換に取れる**。

**補助関係式**: $\mathrm{ord}(x)=4$ なら $P(x^2)=P(x)$;$x,y$ 位数 2 なら $P(xy)=P(x)+P(y)+c(x,y)$;$c(x^2,y)=0$。

### 1.3 三窓の実測(維持)

| 窓 | $Q_2$ の基底 | 層サイズ | $S$ 中心化 | $\tilde G$ 持ち上げ位数分布 | $P$ |
|---|---|---|---|---|---|
| A16 | $u=-1$(位数 2) | 88 | 22 | $[2\!:\!22]$ | **0** |
| A18 | $u=5$(位数 4) | 104 | 26 | $[4\!:\!26]$ | **0** |
| ″ | ($u=-1$) | 104 | 26 | $[2\!:\!26]$ | **0** |
| A20 | $u=7$(位数 4) | 120 | 30 | $[4\!:\!30]$ | **0** |
| ″ | $u=11$(位数 2) | 120 | 30 | $[2\!:\!30]$ | **0** |
| ″ | ($u=-1$) | 120 | 30 | $[2\!:\!30]$ | **0** |

$\tilde G$ は三窓ともアーベル($C_{10}\times C_2$/$C_{12}\times C_2$/$C_4\times C_2\times C_2$)ゆえ $c\equiv0$。A18・A20 は witness 対の交換子も直接 0 を確認。

### 1.4 A20 は直因子ごとの条件に分解しない(維持)

$\dim H^2=2+1$。交差項は $\Lambda^2(C_4\times C_2)=C_2$ 由来で**巡回部分群への制限では原理的に検出不能**。

### 1.5 $u=-1$ 層が拾うビットの正確な同定(維持)

A20 で $-1=29=a^2b$($a=7,b=11$)ゆえ $P(-1)=P(a)+P(b)$。**$u=-1$ 判定は和のビット 1 個しか見ない**。$Q_2$ 巡回($N$ が素数冪)のときだけ 1 ビットで尽きる。

### 1.6 層内一様性(維持・**ただし §4 の会計に注意**)

全測定層で分布は単一値。これは補題 A の実測的確認。

---

## 2. 素点分解(v1 §2 から変更なし)

$Q\cong(\mathbb Z/N)^\times$、$N$ 奇平方因子なしなら
$$\dim_{\mathbb F_2}H^2(Q;C_2)=\pi(N)+\binom{\pi(N)}2,\qquad
\varepsilon(W)=\bigl((\varepsilon_p)_{p\mid N},(c_{pq})_{p<q}\bigr).$$
実測 $N=11,13,15$ に対し $1,1,3$ ✔。三窓とも全成分 0。

---

## 3. 【LG-2】閉形式候補(型を訂正)

### 3.1 コサイクル式 — **group-level を正本に**(E-5)

各 $u\in Q$ に対し $S$ を中心化する元 $g_u\in C_G(S)$($\tilde\chi(g_u)=u$)を選ぶ。(H3) よりこれは可能。
$$\boxed{\ \varepsilon=\Bigl[(u,v)\longmapsto \mathrm{pr}_{\langle z\rangle}\bigl(g_ug_vg_{uv}^{-1}\bigr)\Bigr]\in H^2(Q;C_2),\qquad g_ug_vg_{uv}^{-1}\in C_G(S)\cap K=A\times\langle z\rangle .\ }$$
$\varepsilon=0$ $\iff$ **$\{g_u\}$ を mod $A$ で honest な準同型切断に取り直せる**。

> **v1 §3.1 の shadow 座標版**($f_uT_{(m_u,f_u)}(f_v)f_{uv}^{-1}$ の $Z(S)$ 成分)は、shadow の積・逆元規約からの導出を一段付けるまで**参考扱い**とする(F85-4.2/P85-3 の指示)。上の group-level 式が正本。

### 3.2 位数条件 = 捻れノルム(**型訂正**)

$T$ は乗法的($T_{gh}=T_gT_h$;合成則から証明済)。よって $(m,f)^j=\bigl(u^j,\ \prod_{i=0}^{j-1}T^i(f)\bigr)$、$T=T_{(m,f)}$。$n=\mathrm{ord}(u)$ とすると $g^n=(1,\mathcal N_{T,n}(f))\in K$。$g$ が $S$ を中心化するなら $g^n\in C_K(S)=A\times\langle z\rangle$ ゆえ

$$\boxed{\ P(u)=\mathrm{pr}_{\langle z\rangle}\bigl(\mathcal N_{T,n}(f)\bigr),\qquad
P(u)=0\iff \mathcal N_{T,n}(f)\in A\ \ (\textbf{not } =1).\ }$$

> **v1 の「$\mathcal N_{T,n}(f)=1$」は型落ちの誤り**(F85-4.2)。$A$-成分は非自明でありうる。

**反証データ(梯子・`epsbits_a13_ladder_20260730.json`)**: `W-E-A10-9t1`、$u=7$ 層、$\mathrm{ord}(u)=3$、$\tilde G$ 持ち上げ位数分布 `[3:9]`、$P$-bit false、**しかし記録された実 lift は $\mathrm{ord}_G=9$**($A=C_9$)。つまり $\mathcal N_{T,3}(f)\in A\setminus\{1\}$。**「$\mathcal N=1$」はこれで反証済**。

> **誠実な補足(反証の射程)**: この窓は $S_{\rm order}=1$(証明書 `S_trivial_vacuous: true`)で「$S$ を中心化」が**空虚に真**、かつ $\mathrm{ord}(u)=3$ は奇で補題 A の $P$ は定義域外(奇位数は Schur–Zassenhaus で常に分裂ゆえ自明に 0)。したがって「$S=D_8$ の三窓に後退させれば未反証」という Sol の但し書きも同時に正しい。**しかし $P=0\Rightarrow\mathcal N=1$ という導出自体が成立しない**という指摘は射程に依らず有効であり、私はこれを全面的に受け入れる。

### 3.3 GT-shadow の公理も 2 本のノルム方程式(維持)

θ-公理 $f\tilde\theta(f)=1$ = 位数 2 作用素の 2 重ノルム。τ-公理 $R_\tau(m,f)=c^m$ = 位数 3 作用素の 3 重ノルム。$B_3/Z\cong PSL_2(\mathbb Z)\cong C_2*C_3$ の二つの捻れ生成元に対応。**【GAP-1′】= 「$B_3$ 方向の 2 本のノルム条件が、なぜ $\tilde\chi$ 方向のノルム条件を導くのか」**。
外部確認(Guillot digest §0–1.2): $GT(G)$ の定義も「$\theta$(位数 2)と $\delta$(位数 3)と $\mathrm{Out}$ で可換」の 2 条件のみ — 骨格一致。ただし Guillot 系は $\lambda$ 座標を持たないので $\varepsilon$ に対応する量が無く、型 III からの機構輸入は不可。

### 3.4 candidate 札(**P85-3 の分割を採用**)

> **【M-1P】(冪ビット)** $S$ を中心化する shadow $g=(m,f)$ について
> $$\mathrm{pr}_{Z(S)}\mathcal N_{T,n}(f)=1\quad\text{すなわち}\quad \mathcal N_{T,n}(f)\in A\qquad(n=\mathrm{ord}(u)).$$
> 同値: $\tilde G$ における lift が最小位数。**これが D4 三窓 164/164 が支持している主張**。
>
> **【M-1c】(交差ビット)** $Q_2$ の**不変因子基底**の lift を $C_G(S)$ 内に選び、**全対**について $[g_i,g_j]\in A$(= $\bar C$ で可換)。
>
> $$\boxed{\ \varepsilon=0\iff \text{M-1P(全基底)}\ \wedge\ \text{M-1c(全対)}\ }$$
> **M-1P だけでは $\varepsilon=0$ は出ない**(F85-4.3: 純 $\Lambda^2$ 成分を持つ中心拡大では全生成元 lift が同位数でも非可換・非分裂)。

> **【M-2】素点局所性** $\varepsilon_p$ は $p$ と $S$ のみに依存。最小実験: 素因数を共有する二窓の比較。
> **【M-3】θ-公理が源** 対照実験(設計は司令塔判断待ち・v1 §3.4 のまま)。

### 3.5 閉形式の現状(維持・型訂正済)

$\varepsilon(W)=((\varepsilon_p),(c_{pq}))$、$\varepsilon_p=\mathrm{pr}_{\langle z\rangle}\mathcal N_{T,2^{a_p}}(f_{a_p})$、$c_{pq}=\mathrm{pr}_{\langle z\rangle}[g_{a_p},g_{a_q}]$。
**候補 = 恒等的に 0(M-1P ∧ M-1c)。証明はない。** 右辺は依然として窓の内部量を参照しており「閉じた式」ではない。

---

## 4. 会計の分計(F85-4.4・E-3)

**「188/188」という表示は廃止する**。異なる単位を足していた。

```text
D4 windows (A16/A18/A20): 164/164  shadow-level minimum-order observations
A13 ladder (4 windows):    24/24   layer-level P-bit tests   (= 4 x 6 layers)
```
- 前者は **164 個の centralizing shadow の個体検査**(22+26+26+30+30+30)。
- 後者は **24 個の $u$-layer predicate**。各 layer は内部に 9 個または 18 個の shadow を含む。
- **いずれも交差ビット $c(a_i,a_j)$ の検査数ではない。** 交差ビットは D4 三窓で $\tilde G$ のアーベル性(+ A18/A20 の witness 対)として別途確認されているのみで、層別最小位数検査からは一切出ない。

---

## 5. 型 I(4-可除性)の読み(v1 §4・§4.1 から変更なし)

- 我々の $Q$ は $\mathrm{Out}(S)$ に**自明**に作用(KE-o)。忠実 symplectic 前提の定理は適用外 — 輸入すべきは局所化の方法のみ。
- **主語の訂正**(Korbelář–Tolar 原文 pp.1–2): 「$4\mid N$ で非半直積」の $N$ は**核(Heisenberg)側のパラメータ**であって $\lvert Q\rvert$ ではない。$D_8$ は $\mathbb Z/2$ 上の Heisenberg 群で $4\nmid2$ ゆえ**分裂側の端**。三窓の $\varepsilon=0$ はこの読みと整合するが、**類推であって証明ではない**。

---

## 6. 予言(**量化を訂正**)

- **P-EPS-1**: 新 D4 型窓で $\dim H^2(Q;C_2)=\pi(N)+\binom{\pi(N)}2$($\tilde\chi$ 全射のとき)。
- **P-EPS-2(改称・M-1P 専用)**: 全 $u$-層で「$S$ を中心化する shadow $\Rightarrow$ $\tilde G$ で位数 $\mathrm{ord}(u)$」。
 **⚠ これは $\varepsilon=0$ の検査ではない**(F85-4.3)。冪ビットのみ。
- **P-EPS-2c(新設・M-1c 専用)**: $Q_2$ 不変因子基底の $C_G(S)$ 内 lift 全対について $[g_i,g_j]\in A$。
 **P-EPS-2 と P-EPS-2c の両方が PASS して初めて $\varepsilon=0$。**
- **P-EPS-3**: 素因数を共有する二窓で $\varepsilon_p$ が一致(M-2)。
- **P-EPS-4**: $\pi(N)\ge2$ の窓では $u=-1$ 層の判定だけでは $\varepsilon$ は決まらない(§1.5)。
- **P-EPS-5′(v1 の P-EPS-5 を差し替え・指名凍結)**:
 > **最初に実現する、(H1)(H3) と $Z(S)\cong C_2$ を満たす tail-8 窓において $\varepsilon\ne0$。**
 v1 の「$S>D_8$ なら $\varepsilon\ne0$ が起こりうる」は**存在主張で反証不能**だった(F85-4.5)。また $P=0$ かつ $c\ne0$ なら P-EPS-2 全 PASS でも $\varepsilon\ne0$ なので、旧 P-EPS-2 と旧 P-EPS-5 は**同時に成立しうる**(二者択一ではなかった)。指名凍結でこれを解消する。
 **私の立場**: M-1P∧M-1c(普遍)と P-EPS-5′ は真の二者択一。**現時点でどちらにも賭けない**(観測は $S=D_8$ の 1 点のみ)。

---

## 7. 測定契約 — $S\ne D_8$ 窓の certificate 必須 signature(P85-4)

次の 5 項を**証明書の必須欄**とする。これが M-1P / M-1c / P-EPS-5′ を分離する最小 signature である。

```text
1. Q_2 invariant-factor basis            (基底の取り方を明示・不変因子で)
2. P(a_i) for every basis generator      (冪ビット・全基底)
3. c(a_i,a_j) for every pair             (交差ビット・全対)  <- 従来欠けていた欄
4. H3 and Z(S)                           (G = S.C_G(S) の成否 と Z(S) の同型型)
5. the chosen lift identities and their quotient orders
                                          (選んだ g_i の shadow 座標 と tilde G での位数)
```

**窓設計(P85-4 の二段を採用)**:
1. **安価な pilot: `W-D-A19-13t6`** — 実現対あり。ただし $S=\mathrm{Syl}_2(S_6)\cong D_8\times C_2$ で $Z(S)\cong C_2^2$ となり、**本ノートの係数 $C_2$ を外れる**(STR-1 の (H1) の $Z(S)\cong C_2$ も外れる)。**一般化コードの較正と M-1P の反例探索には有用だが、P-EPS-5′ の比較窓にはならない**。
 → $Z(S)=C_2^2$ 版の一般化(係数 $Z(S)$ の $Q$-加群構造・$H^2(Q;Z(S))$)は**未着手**。【GAP-5(新)】
2. **clean tail-8 fork: $\ell=17,\ n=25,\ t=8$** — まず SAT で実現 existence を判定。実現した場合に限り $S=\mathrm{Syl}_2(S_8)$、$Z(S)=C_2$、(H3) を先に確認してから $\varepsilon$ を測る。

---

## 8. 【GAP】と次の一手

- **【GAP-1′】** なぜ「$S$ を中心化する」ことが $\mathcal N_{T,n}(f)$ の $Z(S)$-成分を消すのか($B_3$ 方向 → $\tilde\chi$ 方向のノルム転送)。
- **【GAP-2′】** $\pi(N)\ge3$ の窓が未観測(交差項が複数になる挙動が完全に未知)。
- **【GAP-5(新)】** $Z(S)\not\cong C_2$($\mathrm{Syl}_2(S_6)$ 等)への一般化が未着手。$\varepsilon$ は $H^2(Q;Z(S))$ に住み、$Z(S)$ の $Q$-加群構造が新たな変数になる。
- **次の一手**: 既存 `search/_probe_epsilon_bits.g` に **交差ビット欄(§7 の 3)** を追加すること。現状のコードは冪ビットしか出しておらず、**そのままでは $\varepsilon=0$ を主張できない**(これが F85-4.3 の実務的帰結)。費用は小(既に $C_G(S)$ と $\bar C$ を構成済み)。

---

## 9. 出所・格付け

- v1(凍結): `docs/notes/epsilon_mechanism_v1.md`
- スクリプト: `search/_probe_epsilon_bits.g` + driver `_a{16,18,20}.g`
- 証明書: `search/certs/.epsbits_W-D-A{16,18,20}-*.json`(D4 三窓)・`search/certs/epsbits_a13_ladder_20260730.json`(梯子・§3.2 の反証データ)
- 監査: `sol/sol_reply_85_math12.md` §4(F85-4.1〜4.5・P85-3・P85-4)
- 格付け: §1・§2・§3.1・§3.2 の公式は**証明済**。§1.3 の表と §4 の会計は **GAP 単系統の実測**。§3.4 の M-1P/M-1c/M-2/M-3、§5 の類推、P-EPS-5′ は **candidate(未証明)**。
- 文献の読んだ範囲は v1 §8 のまま(追加の精読はしていない)。
