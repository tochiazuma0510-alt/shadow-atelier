# R1(K9-BRIDGE)部品 4 — canonical $\rho_9$ の pin・marked Aff projection・field 分離

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 899(R1 続行承認)
**受入条件**: `docs/notes/ent_arith_type_gate_v3.md` §2.2 の **R1-a〜f** / **罠 7 点** = Sol 便 118 §5
**格**: **すべて candidate**(紙・単系統・**Sol 未監査**)。**verified は Lean に予約**。走行ゼロ・実測値の使用なし。
**正典**(逐語照合済): 2405.11725 **(1.3)(1.5)(1.9)(1.11)(1.13)**・**Prop 3.4**・**Prop 4.5 (4.15)**・**(4.18)**・**Thm 4.3 (4.12)**・**Thm 4.6 (4.23)** / Ihara ICM Kyoto 1990 印刷 **pp.105–106**

> ### ★★ 本ノートの一行
> $$\boxed{\ \rho_9\ \textbf{の}\textbf{三座標のうち二つ(unit と }C_2\textbf{)は}\textbf{完全に円分的}\textbf{で、未知は translation 座標 }t\ \textbf{のみ。しかも }t\in Z^1(G_\mathbf Q,\mu_9)\ }$$
> ⟹ **R1-a / R1-b / R1-d は閉じた**。**R1-c / R1-e(pro-3 移植 = 3 外不分岐の供給)は OPEN** — そこが K9-BRIDGE の本体。

---

## §1 R1-a — canonical $\rho_9$ の pin(LOCAL-PIN 逐語対応表)

| # | データ | 正典の逐語 | 本工房の記号 |
|---|---|---|---|
| 1 | source | $G_\mathbf Q$ | $G_\mathbf Q$ |
| 2 | $G_\mathbf Q$ の $\widehat F_2$ への作用 | $g(x)=x^{\chi(g)}$、$g(y)=f_g^{-1}y^{\chi(g)}f_g$(**2405 §1.3**・Ihara [15, §1] の分裂) | 同 |
| 3 | 接基点・路・生成元 | $\overrightarrow{01}$、区間 $(0,1)$ の路 $p$、$0$ 周りの正向き小ループ $x$、$y=p^{-1}x'p$ — **Ihara ICM 印刷 pp.105–106**($f_g$ の構成は [15, §1.4]) | 同 |
| 4 | Ihara 埋め込み | $\mathrm{Ih}(g):=\bigl((\chi(g)-1)/2,\ f_g\bigr)\in\widehat{\mathbf Z}\times\widehat F_2$ — **(1.5)**。Belyi により**単射** | $\mathrm{Ih}$ |
| 5 | 有限化 | $\mathcal{PR}_N(\hat m,\hat f):=\bigl(\widehat P_{N_{\rm ord}}(\hat m),\ \widehat P_N(\hat f)_{F_2}\bigr)$ — **(1.3)** | $\mathcal{PR}_N$ |
| 6 | 合成 | $\mathrm{Ih}_N:=\mathcal{PR}_N\circ\mathrm{Ih}:G_\mathbf Q\to GT(N)$ — **(1.11)** | $\rho_9:=\mathrm{Ih}_{K^{(9)}}$ |
| 7 | 群性の前件 | $N$ **isolated** ⟹ $GT(N)$ は有限群・$\mathcal{PR}_N$ は群準同型(**§1.3.1**)。非 isolated では集合写像(**Remark 1.4**) | $K^{(9)}$ は **Thm 4.3 末尾**で isolated ⟹ ✔ |
| 8 | 円分可換図 | $\chi_{\mathrm{vir},N}([m,f]):=2m+1+N_{\rm ord}\mathbf Z$ — **(1.9)**。$\chi_{\mathrm{vir},N}\circ\mathrm{Ih}_N=\widehat P_{N_{\rm ord}}\circ\chi$ — **(1.13)** | 下記 §2 で使用 |

$$\boxed{\ \textbf{⟹ R1-a は}\textbf{照合で閉じる}\textbf{。「五データの創作」は不要(便 118 M118-1 の確定)}\ }$$

---

## §2 R1-b — marked Aff projection $\rho_{9,\mathrm{Aff}}$ と $\chi_9$ 可換図

### 2.1 命題 **K9-COORD**(marking $\Theta_9$ の明示形・candidate)

$K^{(9)}=K^{(18)}$(**Prop 3.4**: $n$ 奇 ⟹ $K^{(n)}=K^{(2n)}$)。**Prop 4.5 (4.15)** を $n=18$($n_1=n/2=9$、$2n=36$、$4\nmid18$)に適用して
$$\varrho:\ GT(K^{(9)})\ \xrightarrow{\ \sim\ }\ \mathbf Z/9\mathbf Z\rtimes(\mathbf Z/36\mathbf Z)^\times,\qquad
\bigl(m,(r^{2k},r^{-2k},r^{\kappa(m)})\bigr)\ \longmapsto\ \bigl(k\bmod 9,\ (2m+1)\bmod36\bigr).$$
$(\mathbf Z/36)^\times$ の $\mathbf Z/9$ への作用は **$u\bmod9$ にしか依らない**((4.18) の合成則 $(k_1,u_1)(k_2,u_2)=(k_1+u_1k_2,\ u_1u_2)$)。CRT $(\mathbf Z/36)^\times\cong(\mathbf Z/9)^\times\times(\mathbf Z/4)^\times$ と合わせて
$$\boxed{\ \Theta_9:\ GT(K^{(9)})\ \xrightarrow{\ \sim\ }\ \mathrm{Aff}(\mathbf Z/9)\times C_2\ }\qquad\bigl(\mathrm{Aff}(\mathbf Z/9)=\mathbf Z/9\rtimes(\mathbf Z/9)^\times\bigr)$$
これが **Thm 4.6 (4.23)** の $\alpha<2$ 枝($n_0=9$, $\alpha=0$)の**明示形**である。

**位数検算**(私の独立計算・機械確認済): $\lvert\mathbf Z/9\rtimes(\mathbf Z/36)^\times\rvert=9\cdot\varphi(36)=9\cdot12=108$;$\lvert\mathrm{Aff}(\mathbf Z/9)\rvert\cdot2=9\cdot6\cdot2=108$;**Thm 4.3 (4.12)** 側は $\lvert\mathcal X_{K^{(9)}}\rvert\cdot\#\{r^{2k}\}=12\cdot9=108$。**三経路一致** ✔

> ### ⚠★ **OCR の罠**(Remark 3.3 の $\eta^3$ 罠と同型・**後任への警告**)
> Thm 4.6 の証明本文は抽出テキストで
> > $GT(K^{(2n_0)})\cong\mathbf Z/n_0\mathbf Z\rtimes(\mathbf Z/n_0\mathbf Z)^\times\times\mathbf Z/4\mathbf Z\cong\mathrm{Aff}(\mathbf Z/n_0\mathbf Z)\times\mathbf Z_2$
> と読めるが、**$\mathbf Z/4\mathbf Z$ ではなく $(\mathbf Z/4\mathbf Z)^\times$**(上付き $\times$ が落ちている)。位数で判定できる: $54\cdot4=216\ne108$、$54\cdot2=108$ ✔。**Thm 4.6 本文が「$\mathbf Z_2$ は位数 2 の巡回群」と明記していること**とも整合。⟹ **本ノートは一貫して $(\mathbf Z/4)^\times$ を採る。**

> ### ★ 罠 1 の処理(型の確認)
> $\Theta_9$ は**群同型**(Prop 4.5 が同型、CRT が同型)。$\mathrm{pr}_{\mathrm{Aff}}:\mathrm{Aff}(\mathbf Z/9)\times C_2\to\mathrm{Aff}(\mathbf Z/9)$ は**直積因子への射影ゆえ群準同型** ✔。
> ### ★★ 罠 1 の残余 = **marking の自由度は $(\mathbf Z/9)^\times$-scaling のみ**
> $\varrho$ の unit 座標は $\chi_{\mathrm{vir}}$ から**正準**((1.9))、CRT 分解も**正準**。選択が残るのは **translation 群 $\langle r\rangle$ の生成元 $r$ の取り方**だけで、これは $t\mapsto ct$($c\in(\mathbf Z/9)^\times$)を引き起こす。
> $$\boxed{\ c\in(\mathbf Z/9)^\times\ \textbf{倍は }\ker\rho_{9,\mathrm{Aff}}\textbf{・}L_{9,\mathrm{Aff}}\textbf{・}d_9\ \textbf{を}\textbf{変えない}\ \Longrightarrow\ \textbf{MARKING-COMPAT は K9 レーンでは}\textbf{無害}\ }$$
> ⚠ **一般の $N$ での MARKING-COMPAT は依然 OPEN** — 本結論は $K^{(9)}$ の構造定理に依存する。

### 2.2 命題 **K9-CYC**(★ 本 R1 の中核・candidate・証明つき)

$$\boxed{\ \Theta_9\bigl(\rho_9(g)\bigr)=\Bigl(\bigl(\,t(g),\ \chi(g)\bmod9\,\bigr),\ \chi(g)\bmod4\Bigr)\qquad(g\in G_\mathbf Q)\ }$$

**証明**(3 行)
1. **(1.5)** より $\hat m=(\chi(g)-1)/2\in\widehat{\mathbf Z}$。★ **この割り算は合法**: $\chi(g)\in\widehat{\mathbf Z}^\times$ ゆえ 2-進成分が $\mathbf Z_2^\times$ の元 = 奇数、よって $\chi(g)-1\in2\widehat{\mathbf Z}$。**これが罠 5 の正しい処理**(偶数法で 2 を無造作に割ってはいないことの明示)。
2. **(1.3)** より $m=\widehat P_{18}(\hat m)$、すなわち $m\equiv\hat m\pmod{18}$。両辺を 2 倍して 1 を足すと $2m+1\equiv2\hat m+1=\chi(g)\pmod{36}$。
3. $\varrho$ の unit 座標は $(2m+1)\bmod36$、CRT で $(\chi(g)\bmod9,\ \chi(g)\bmod4)$ へ分かれる。∎

**★ (1.13) との整合**: $\chi_{\mathrm{vir},9}$ は $2m+1\bmod N_{\rm ord}=\bmod18$ で $(\mathbf Z/18)^\times$($\varphi=6$)に値をとる。$\varrho$ の unit 座標は $\bmod36$($\varphi=12$)で**より細かい**が、上の証明が示すとおり**その細かい分も $\chi$ から来る**(円分的)。⟹ **(1.13) と矛盾せず、むしろ強めた形**。

> ### ★★ 系 K9-CYC(a) — **未知は translation 座標 $t$ ただ一つ**
> unit 成分 $=\chi\bmod9$(核体 $\mathbf Q(\zeta_9)$)・$C_2$ 成分 $=\chi\bmod4$(核体 $\mathbf Q(i)$)は**ともに完全に既知**。
> $$\boxed{\ \rho_9\ \textbf{の非円分的な情報は }t:G_\mathbf Q\to\mathbf Z/9\ \textbf{に}\textbf{全部}\textbf{入っている}\ }$$
> ### ★ 系 K9-CYC(b) — unit 側は**全射**
> $\chi:G_\mathbf Q\to\widehat{\mathbf Z}^\times$ は全射ゆえ $(\mathbf Z/36)^\times$ 成分は全射 ⟹ $A_9\twoheadrightarrow(\mathbf Z/9)^\times\times C_2$(位数 12)。
> $$\Longrightarrow\quad \lvert A_9\rvert=12\cdot d_9,\qquad d_9:=\bigl\lvert A_9\cap\mathbf Z/9\bigr\rvert\in\{1,3,9\}$$
> ⟹ ★ **$\lvert A_9\rvert=108\iff d_9=9\iff\rho_9$ 全射** ⟹ **【ENT-GAP-6】K9-ORDER($d_9$)は $K^{(9)}$ における dihedral 予想(Conj 5.1)そのもの**。⚠ **`R2` は「小さな計測」ではなく公開問題である** — 見積りを誤らないこと。

---

## §3 R1-d — full field と projection field の分離(★ 罠 6 の決着)

### 3.1 命題 **K9-C2**(candidate・証明つき)

$$\boxed{\ \ker\rho_9=\ker\rho_{9,\mathrm{Aff}}\cap\ker(\chi\bmod4),\qquad L_9=L_{9,\mathrm{Aff}}\cdot\mathbf Q(i),\qquad S_9=S_{9,\mathrm{Aff}}\cup\{2\}\ }$$

**証明** K9-COORD より $\Theta_9\circ\rho_9$ の $C_2$ 成分は $\chi\bmod4$(K9-CYC)。直積の核は各成分の核の交わり。$\ker(\chi\bmod4)=G_{\mathbf Q(i)}$ ゆえ固定体は $\mathbf Q(i)$。ガロア対応で交わりの固定体は合成体。$\mathbf Q(i)/\mathbf Q$ は **2 でのみ分岐**(と $\infty$)。∎

> ### ★★ 帰結 — **「$L_9$ が 3 の外で不分岐」は偽**
> $$\boxed{\ L_9\supseteq\mathbf Q(i)\ \Longrightarrow\ L_9\ \textbf{は }2\ \textbf{で分岐する}\ }$$
> ⟹ **Sol の罠 6 は完全に正しい**。しかも本命題は罠 6 が要求した「**別の ramification 記帳**」を**供給する**: 余分な $C_2$ 因子は $\mathbf Q(i)$ であり、その分岐は $\{2\}$ ちょうど。
> $$\boxed{\ \Longrightarrow\ \textbf{3 外不分岐を主張してよいのは }L_{9,\mathrm{Aff}}\ \textbf{のみ。}\ L_9\ \textbf{は }L_{9,\mathrm{Aff}}(i)\ \textbf{で、余分は}\textbf{完全に既知}\ }$$
> ★ これは v1.4.7 §8【ENT-GAP-5】の「$C_2$ 因子は別記帳」を**具体的に閉じた**もの(M118-4 の解消)。

---

## §4 translation 座標の正体 — 命題 **K9-KUMMER**

### 4.1 $t$ は $\mu_9$ 値 1-コサイクル

(4.18) の合成則と K9-CYC より、$g,h\in G_\mathbf Q$ で
$$t(gh)=t(g)+\chi(g)\,t(h)\pmod 9\qquad\Longrightarrow\qquad \boxed{\ t\in Z^1\bigl(G_\mathbf Q,\ \mu_9\bigr)\ }$$
($\mathbf Z/9$ に $\chi\bmod9$ で作用させたもの $=\mu_9$)。

### 4.2 Kummer 理論による同定(★ **有理 radical への降下は自動**)

**古典的事実**【要 pin・標準】: $\mathrm{char}\,K\nmid n$ で $H^1(G_K,\mu_n)\cong K^\times/(K^\times)^n$(Kummer 完全列 + Hilbert 90)。

$t$ は**はじめから $G_\mathbf Q$ 全体の上のコサイクル**なので、その類は直接 $H^1(G_\mathbf Q,\mu_9)\cong\mathbf Q^\times/(\mathbf Q^\times)^9$ に属する。よって $a\in\mathbf Q^\times$ が存在して
$$\boxed{\ L_{9,\mathrm{Aff}}=\mathbf Q\bigl(\zeta_9,\ \sqrt[9]{a}\bigr),\qquad d_9=\bigl[L_{9,\mathrm{Aff}}:\mathbf Q(\zeta_9)\bigr]\in\{1,3,9\}\ }$$

> ### ★★ これが **B116-1 の「有理 radical 降下が未証明」を閉じる**
> U9-RIGID 原形の欠落は「無標識 $\mathrm{Aff}(\mathbf Z/9)$ から**有理**の radical へ降りられるか」だった。**本命題はそれを前提なしに与える** — 理由は単純で、$t$ が $G_\mathbf Q$ **全体**の上のコサイクルだから($\mathbf Q(\zeta_9)$ 上の準同型から出発して降ろす必要がない)。
> ★ 参考(降ろす路を採る場合も塞がっていないことの確認): $\Delta=(\mathbf Z/9)^\times\cong C_6$ が $\mu_9$ に自然に作用するとき **$H^1(\Delta,\mu_9)=H^2(\Delta,\mu_9)=0$**(私の機械検算: 生成元 $c=2$ で $\mu_9^\Delta=0$、$N=1+2+4+8+7+5\equiv0$、$(\sigma-1)=$ 乗法 $1$ は全単射 ⟹ 両方 0)。**Sol の U9-RIGID$^{\rm mark}$ が使った inflation–restriction は正しい**。

### 4.3 ★ U9-RIGID$^{\rm mark}$ の 5 条件のうち **3 つが定理になった**

| 条件(Sol F3.2) | 本ノートでの地位 |
|---|---|
| **(2)** $C_9\trianglelefteq$ | ★ **定理**: translation 部分群は $\mathrm{Aff}$ の正規部分群(K9-COORD) |
| **(3)** $L^{C_9}=\mathbf Q(\zeta_9)$ | ★ **定理**: translation で割った商 = unit 成分 $=\chi\bmod9$、固定体は $\mathbf Q(\zeta_9)$(K9-CYC) |
| **(4)** $\theta=\chi_9$ | ★ **定理**: unit の translation への共役作用は $u=\chi\bmod9$ 倍((4.18)) |
| **(1)** 3 の外で不分岐 | ✘ **OPEN** = **K9-BRIDGE の本体**(§5) |
| **(5)** 次数 9 | ✘ **OPEN** = $d_9=9$ = **`R2` K9-ORDER**(§2.2 系 (b) より Conj 5.1 と同値) |

> ### ★★ 条件 (1) が来たときの帰結(**条件付き・証明つき**)
> $L_{9,\mathrm{Aff}}/\mathbf Q$ が 3 の外で不分岐なら、$p\ne3$ で $v_p(a)\equiv0\pmod 9$(さもなくば $p$ が $\mathbf Q(\sqrt[9]{a})$ で分岐)。$\mathbf Q^\times$ の単数は $\pm1$ で $-1=(-1)^9$ は 9 乗ゆえ、9 乗を法として $a=3^j$。
> $$\boxed{\ \Longrightarrow\ L_{9,\mathrm{Aff}}\subseteq\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr),\qquad d_9=9\iff L_{9,\mathrm{Aff}}=\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr)\ }$$
> ★ **U9-RIGID の結論($\mathbf Q(\zeta_9,\sqrt[9]{3})$ の一意性)は、条件 (1) さえ来れば完全な証明になる。** ⚠ **条件 (1) は来ていない** — $u_9=3$ の撤回は撤回のまま(§6)。

---

## §5 R1-c / R1-e — **OPEN**(K9-BRIDGE の本体)

必要な入力は 1 個だけになった:
$$\boxed{\ \textbf{(K9-UNRAM)}\quad L_{9,\mathrm{Aff}}/\mathbf Q\ \textbf{は }3\ \textbf{の外で不分岐}\ }$$

| 罠 | 状態 |
|---|---|
| **罠 2**(inner ambiguity) | ✘ **OPEN**。pro-3 outer action が自明 = based automorphism が inner という意味であり **$f_g=1$ とは限らない**。$\rho_{9,\mathrm{Aff}}$ が inner を殺して outer を経由することの証明が要る |
| **罠 3**(factorization の向き) | ✘ **OPEN**。要るのは「pro-3 outer kernel に入れば Aff 像が単位」。★ **本ノートで前進**: 「Aff 像」は $(t,\chi\bmod9)$ で、$\chi$ 部分は既知ゆえ **示すべきは $t$ が pro-3 の $f$-データだけを経由すること**に縮んだ |
| **罠 4**(3 群と思わない) | ✘ **OPEN**。$\lvert PB_3/K^{(9)}\rvert=\lvert G_9\rvert=4\cdot9^3=2916$ は **3 群ではない**(因子 4)。★ **本ノートで前進**: 3-primary なのは **translation $\mathbf Z/9$ だけ**で、残り($(\mathbf Z/9)^\times\times C_2$、位数 12)は**円分**と同定済 ⟹ **pro-3 を経由させる必要があるのは $t$ のみ**。⚠ **(H2) の直引用は不可**(R1-e) |
| **罠 7**(向きと連続性) | ✘ **OPEN**。$\ker(\rho^{(3)}_{\rm out})\subseteq\ker\rho_{9,\mathrm{Aff}}$ から出るのは $L_{9,\mathrm{Aff}}\subseteq\bar{\mathbf Q}^{\ker\rho^{(3)}_{\rm out}}$。両核の閉性と後者の 3 外不分岐性の exact pin が要る |

> ### 【文献要請】**K9-LIT-1**(困難の記述+欲しい結果の型)
> **困難**: $\mathbf P^1_\mathbf Q-\{0,1,\infty\}$ の pro-$\ell$ 基本群への $G_\mathbf Q$ 作用が定める体が **$\ell$ の外で不分岐**である、という古典的事実を、**$\ell=3$** で、**based(outer でない)射 $\rho_{9,\mathrm{Aff}}$ の translation 座標**に適用できる形で要する。工房手持ちの U2-BR INN は $\ell=2$ 版で、前件 (H2) が $N_{\rm ord}=9$ で破れるため**直引用不可**(R1-e)。
> **欲しい結果の型**: 「$G_\mathbf Q\to\mathrm{Out}(\pi_1^{(\ell)})$ の核を固定する体は $\ell$ の外で不分岐」の**逐語**と、**inner ambiguity を通り抜けて $\mu_\ell$ 値コサイクルの不分岐性へ落とす**標準の議論(Ihara / Anderson–Ihara / Nakamura 系と思われるが、**正典外なので自分では漁らない**)。
> ★ **代替の安い路があるかもしれない**: $t$ の類は $\mathbf Q^\times/(\mathbf Q^\times)^9$ の元 $a$ に過ぎないので、**$a$ の素因子を直接押さえる**議論(例: $\rho_9$ が $\mathbf P^1-\{0,1,\infty\}$ 由来ゆえ $a$ が $\{2,3\}$ 台に載る等)でも足りる。⟹ 司令塔の判断を仰ぐ。

---

## §6 R1-f — **成功しても閉じるものは小さい**(過大評価防止)

| 主張 | 状態 |
|---|---|
| $L_{9,\mathrm{Aff}}$ が 3 外不分岐 | ← **(K9-UNRAM)**。これが R1 の出力 |
| $L_{9,\mathrm{Aff}}\subseteq\mathbf Q(\zeta_9,\sqrt[9]{3})$ | ★ (K9-UNRAM) から**本ノートの §4.3 で自動** |
| $L_9$ が 3 外不分岐 | ✘ ★ **偽**($L_9\supseteq\mathbf Q(i)$・K9-C2)。正しくは $S_9=S_{9,\mathrm{Aff}}\cup\{2\}$ |
| $d_9=9$($u_9=3$) | ✘ **OPEN**(`R2`)。★ **Conj 5.1@$n=9$ と同値**ゆえ安くない。**「$u_9=3$」は撤回のまま** |
| $\lvert A_9\rvert$ | $=12\cdot d_9$ ⟹ $d_9$ 待ち |
| 972 の発火 | ✘ **無関係**。$C=6$・円分下界 $\varphi(9)=6$ ⟹ $6>6$ は偽 |

$$\boxed{\ \textbf{`R1` が閉じても得られるのは }L_{9,\mathrm{Aff}}\ \textbf{の 3 外不分岐 1 件と、それに続く }\mathbf Q(\zeta_9,\sqrt[9]{3})\ \textbf{への包含のみ}\ }$$

---

## §7 受入条件の判定・残 GAP

| # | 受入条件(gate v3 §2.2) | 判定 |
|---|---|---|
| **R1-a** | canonical $\rho_9$ の pin | ★ **閉**(§1 の 8 行対応表) |
| **R1-b** | marked Aff projection と $\chi_9$ 可換図 | ★ **閉**(K9-COORD + K9-CYC・(1.13) と整合し強めた) |
| **R1-c** | inner ambiguity の消去 | ⚠ **marking 側は閉**($(\mathbf Z/9)^\times$-scaling は無害)/ **outer action 側は OPEN**(罠 2) |
| **R1-d** | full / projection field の分離 | ★ **閉**(K9-C2: $L_9=L_{9,\mathrm{Aff}}(i)$・$S_9=S_{9,\mathrm{Aff}}\cup\{2\}$) |
| **R1-e** | (H2) の直引用不可 | ★ **遵守**(直引用していない)。代替は【文献要請】K9-LIT-1 |
| **R1-f** | 閉じるのは 3 外不分岐のみ | ★ **明記**(§6)。⚠ さらに **$L_9$ ではなく $L_{9,\mathrm{Aff}}$ のみ**と訂正 |

| 【GAP】 | 内容 | 重さ |
|---|---|---|
| ★★ **【K9-UNRAM】**(新) | $L_{9,\mathrm{Aff}}$ の 3 外不分岐 — **K9-BRIDGE の本体**。罠 2/3/4/7 が集まる一点 | ★★ 大 |
| ★ **【K9-KUMMER-SUPP】**(新) | $a\in\mathbf Q^\times/(\mathbf Q^\times)^9$ の**素因子台**を直接押さえる代替路(【K9-UNRAM】より安いかもしれない) | ★ 中 |
| **【ENT-GAP-6】K9-ORDER** | $d_9$ — ★ **Conj 5.1@$n=9$ と同値**と判明 ⟹ **重さを「大」から「公開問題」へ格上げ** | ★★★ |
| **【MARKING-COMPAT】** | ★ **K9 レーンでは閉**($(\mathbf Z/9)^\times$-scaling は不変量を変えない)/ **一般 $N$ は OPEN** | 中 |

---

## §8 帰属・依存申告

- **罠 7 点・受入条件 6 項・型境界** = **Sol 便 118**。**U9-RIGID$^{\rm mark}$ の 5 条件** = Sol 便 116。委嘱・裁定 = 司令塔(899)。
- **正典**(Prop 3.4 / Prop 4.5 (4.15) / (4.18) / Thm 4.3 / Thm 4.6 / (1.3)(1.5)(1.9)(1.11)(1.13))= 2405.11725 を**本セッションで逐語精読**。
- **本ノートの新規部分**: ① **K9-COORD**($\Theta_9$ の明示形と marking 自由度 $=(\mathbf Z/9)^\times$-scaling)② ★ **K9-CYC**(unit 座標 $=\chi\bmod9$・$C_2$ 座標 $=\chi\bmod4$ ⟹ **未知は $t$ のみ**)③ ★ **K9-C2**($L_9=L_{9,\mathrm{Aff}}(i)$・$S_9=S_{9,\mathrm{Aff}}\cup\{2\}$ ⟹ 罠 6 の決着と「$L_9$ 3 外不分岐」の**否定**)④ ★ **K9-KUMMER**($t\in Z^1(G_\mathbf Q,\mu_9)$ ⟹ **有理 radical 降下は自動** = B116-1 の欠落を閉じる)⑤ **U9-RIGID$^{\rm mark}$ の (2)(3)(4) を定理化**し (1)(5) だけを残した ⑥ $d_9=9\iff$ **Conj 5.1@$n=9$**(`R2` の難度の再評価)。
- **検算**: 位数 108 の三経路一致・CRT 全単射・$H^1(\Delta,\mu_9)=H^2=0$ は **python 単系統**(整数演算のみ)。⟹ **cross-checked ではない**。
- **未実施**: 走行ゼロ・実測値不使用・GAP 未走・Lean 未着手。**Sol 未監査**。⟹ **verified ではない**。
