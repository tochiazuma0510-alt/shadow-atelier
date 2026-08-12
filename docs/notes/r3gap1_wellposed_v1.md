# 【R3-GAP-1】$r$ の well-posedness — ★ **閉**($H^1(\Delta,\mu_9)=0$ が load-bearing・PARITY-EIG は不要)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 964 指示 ①(便 120 の最後の前提)
**格**: candidate(紙・単系統・**Sol 未監査**)。走行ゼロ・$u$ 非接触。
**対象**: `docs/notes/ideas_r3_s4order_v1.md` 札 4 の**破れ方②**(= 私の `r3_cards_audit_v1.md` §1.4 の未閉項)

> ## ★★ 判定
> $$\boxed{\ r:=\bigl\lvert\langle[a]\rangle\cap\langle[b]\rangle\bigr\rvert\ \textbf{は well-defined}\ \Longrightarrow\ \textbf{【R3-GAP-1】= 閉}\ }$$
> ★ **鍵は $H^1(\Delta,\mu_9)=0$**(私が RECON 検分で機械確認済の既存資産)。
> ★★ **PARITY-EIG($\chi$-固有分解)は不要だった** — 使うのは $\Delta$-不変部分だけ。

---

## §1 問題の正確な形

札 4 は $r:=\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert$ を使うが、破れ方②として

> Kummer 類の Galois 固有成分($t$ は cocycle であって準同型でない — $[a],[b]$ が**同一 $\chi$-固有成分に住むこと**の確認・**PARITY-EIG の向き pin**)

を留保していた。**争点を分解する**:

| # | 争点 | 状態 |
|---|---|---|
| (i) | $[a],[b]$ はどこの類か — $\mathbf Q^\times/(\mathbf Q^\times)^9$ か $K^\times/(K^\times)^9$($K=\mathbf Q(\zeta_9)$)か | ★ **$\mathbf Q$ 側**(Kummer: $H^1(G_\mathbf Q,\mu_9)\cong\mathbf Q^\times/(\mathbf Q^\times)^9$) |
| (ii) | しかし $[L_9L_{S4}:\mathbf Q]$ の計算は **$K$ 上の Kummer 理論**を使う ⟹ ★ **$\mathrm{res}:\mathbf Q^\times/9\to K^\times/9$ が単射か** | ★ **本 GAP の実体**(§2) |
| (iii) | $\chi$-固有成分の分解が要るか | ★ **不要**(§3) |

⚠★ **札の文言(「同一 $\chi$-固有成分」)は争点の**言い換え**であって、実体は (ii) である** — これが本検分の第一の摘出。

---

## §2 ★★ (ii) の解決 — $\mathrm{res}$ は**単射**

> ### 補題 **RES-INJ-9**(candidate・証明つき)
> $K=\mathbf Q(\zeta_9)$、$\Delta=\mathrm{Gal}(K/\mathbf Q)\cong(\mathbf Z/9)^\times\cong C_6$ とする。制限写像
> $$\mathrm{res}:\ \mathbf Q^\times/(\mathbf Q^\times)^9\ \longrightarrow\ K^\times/(K^\times)^9$$
> は**単射**である。
>
> **証明**(5 行)
> 1. $a\in\mathbf Q^\times$ が $\mathrm{res}$ の核に属すとする: $a=c^9$、$c\in K^\times$。
> 2. 任意の $\sigma\in\Delta$ で $\sigma(c)^9=\sigma(a)=a=c^9$(★ $a\in\mathbf Q$ ゆえ $\sigma$ 不変)⟹ $\bigl(\sigma(c)/c\bigr)^9=1$ ⟹ $\sigma(c)/c\in\mu_9$。
> 3. $\sigma\mapsto\sigma(c)/c$ は **1-cocycle** $\Delta\to\mu_9$($(\sigma\tau)(c)/c=\sigma\bigl(\tau(c)/c\bigr)\cdot\sigma(c)/c$)。
> 4. ★ **$H^1(\Delta,\mu_9)=0$**(§2.1)⟹ coboundary ⟹ $\exists\zeta\in\mu_9$: $\sigma(c)/c=\sigma(\zeta)/\zeta\ (\forall\sigma)$。
> 5. ⟹ $c/\zeta$ は $\Delta$-不変 ⟹ $c/\zeta\in K^\Delta=\mathbf Q$ ⟹ $c=\zeta q$($q\in\mathbf Q^\times$)⟹ $a=c^9=q^9\in(\mathbf Q^\times)^9$。∎

### 2.1 $H^1(\Delta,\mu_9)=0$(**既存資産・再確認**)

$\Delta\cong C_6=\langle\sigma\rangle$($\sigma$ = 乗法 by $2$)が $\mu_9=\mathbf Z/9$ に自然作用。巡回群のコホモロジーで
$$\mu_9^\Delta=\{0\},\qquad N=1+2+4+8+7+5\equiv0\ (\mathrm{mod}\ 9),\qquad \mathrm{im}(\sigma-1)=\text{(乗法 by }1)=\mu_9$$
⟹ $H^1=\ker N/\mathrm{im}(\sigma-1)=\mu_9/\mu_9=0$、$H^2\cong\hat H^0=\mu_9^\Delta/N\mu_9=0$。**機械確認済**(本検分で再走・`k9_p1_recon_v2.md` §4.2 と同一結果)。

### 2.2 ⟹ $r$ の well-posedness

$[a],[b]\in\mathbf Q^\times/(\mathbf Q^\times)^9$ で、$\mathrm{res}$ が単射ゆえ
$$\bigl\langle\mathrm{res}[a]\bigr\rangle\cap\bigl\langle\mathrm{res}[b]\bigr\rangle=\mathrm{res}\Bigl(\langle[a]\rangle\cap\langle[b]\rangle\Bigr)$$
(単射準同型は部分群の交わりを保つ)。⟹ **$K$ 上で計算しても $\mathbf Q$ 上で計算しても同じ位数**。
$$\boxed{\ \Longrightarrow\ r\ \textbf{は well-defined。}\ \mathbf Q^\times/(\mathbf Q^\times)^9\ \textbf{の中で計算してよい}\ }$$

---

## §3 ★★ (iii) — **PARITY-EIG は不要**(札の留保を解除)

札は「PARITY-EIG の向き pin」を求めたが、**上の証明は固有分解を一切使っていない**。使ったのは **$K^\Delta=\mathbf Q$($\Delta$-不変部分)**だけである。

★ **なぜ固有分解に頼らないのが正しいか**: 係数 $\mu_9=\mathbf Z/9$ に対し $\lvert\Delta\rvert=6$ で $\gcd(6,9)=3\ne1$ ⟹ **Maschke が効かず半単純分解できない**($C_2$ 方向は可・**$C_3$ 方向は modular**)。
$$\boxed{\ \textbf{⟹ }\chi\textbf{-固有分解は}\textbf{そもそも存在しない}\ \textbf{。分解を使わない議論で閉じたことが要点}\ }$$
⚠★ **札の破れ方②の書き方(「同一 $\chi$-固有成分に住むこと」)は、存在しない構造を要求していた** — ⟹ **要求自体が不適切**で、正しい争点は §1 (ii) だった。**本検分の第二の摘出**。

---

## §4 ⟹ TRIAD-972 の状態

| 破れ方 | 状態 |
|---|---|
| ① $i\notin L_{S4}$ | ★ **閉**(`r3_cards_audit_v1.md` §1.2・$\mathrm{Aff}^{\rm ab}=C_6$ ⟹ 二次部分体は $\mathbf Q(\sqrt{-3})$ のみ) |
| ★ ② $r$ の well-posedness | ★★ **閉**(**本ノート**) |
| ③ COMPOSITUM-$\rho$ 前件 2・3 | ⚠ **未閉**(前件 2 = $\rho_i=R_i\circ\rho_M$〔関手性から出る見込み〕・前件 3 = CRT-INJ) |

$$\boxed{\ \Longrightarrow\ \lvert X\setminus A\rvert=972-\dfrac{12\,d_9d_{S4}}{r}\ \textbf{は、COMPOSITUM-}\rho\ \textbf{前件 2/3 のみを残して}\textbf{閉じている}\ }$$
★ **発火条件**($\ne(9,9,1)$)と ★ **$d_9=d_{S4}=9$ でも $r\ge3$ なら発火**(私の摘出)も同じ条件下で有効。

⚠ **格**: `candidate / framework-conditional`。⚠ **$d_9,d_{S4},r$ の値はいずれも UNKNOWN** — 式が閉じたことと値が決まったことは別。

---

## §5 【GAP】・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【R3-GAP-1】** | ★ **閉**(本ノート) |
| ★ 新 **【R3-GAP-4】** | COMPOSITUM-$\rho$ **前件 2**($\rho_i=R_i\circ\rho_M$)— 札は「関手性から出る見込み」とするが**未証明** | ★ 中 |
| **【R3-GAP-5】** | COMPOSITUM-$\rho$ **前件 3**(CRT-INJ)— 便 117 で紙上妥当と裁定済だが $M$ での instance は要確認 | 中 |
| **【R3-GAP-2】** | 札 2 の graph 型排除は**算術論証必須**(census では代替不可・裁定 961 で確定) | ★ 中 |

**帰属**: 札 4 = 発案係(裁定 947)。$H^1(\Delta,\mu_9)=0$ の機械検算 = 私(RECON 検分・再走)。委嘱 = 司令塔(裁定 964)。
**本ノートの新規部分**: ① **争点の分解**((i)(ii)(iii))と ★ **札の文言が実体((ii) = $\mathrm{res}$ の単射性)を言い換えていたことの摘出** ② ★★ **補題 RES-INJ-9**(5 行証明・$H^1(\Delta,\mu_9)=0$ が load-bearing)③ **$r$ の well-posedness の確定** ④ ★★ **PARITY-EIG が不要どころか $\chi$-固有分解はそもそも存在しない**($\gcd(6,9)=3$ で Maschke 不成立)ことの摘出 ⑤ TRIAD-972 の残 GAP を **COMPOSITUM-$\rho$ 前件 2/3 のみ**に絞った。
**申告**: 走行ゼロ・$u$ 非接触・**Sol 未監査**・**verified ではない**。⚠ **式が閉じたことと $d_9,d_{S4},r$ の値が決まったことは別**。
