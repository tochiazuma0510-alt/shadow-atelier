# ENT-ARITH-TYPE gate v1(裁定 872)— TYPE-IMAGE 規約の実践第一号

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・**走行ゼロ・紙のみ**)
**位置**: Sol P4 の段構成の**①**(最前線)。②以降(mark+K9 橋 / S4-RAM+ORDER / U9-RAMIF / 本走)は本 gate を通ってから。
**規約**: **TYPE-IMAGE**(型・実算術像・核体・分岐は 4 つの別対象。**①→② と ③→④ に橋が要る・②→③ は標準構成**)。

> ### ★ 本 gate の一行
> $$\boxed{\ \textbf{ENT-PREFLIGHT で使う量を、}\textbf{4 対象のどれか}\ \textbf{に一つずつ帰属させ、橋の有無を明示する。値は出さない。}}$$

---

## §0 4 対象の固定(記号)

| # | 対象 | $K^{(9)}$ 側 | $N_{S4}$ 側 | 現状 |
|---|---|---|---|---|
| ① | **型**(GT 群の構造) | $GT(K^{(9)})\cong\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$(位数 108・U-11) | $GT(N_{S4})$(位数 54・$\mathfrak F_0\cong C_9$・$m$ 像 6 元) | ★ **既知**(cert/定理) |
| ② | **実算術像** | $A_9:=\mathrm{im}(\mathrm{Ih}_{K^{(9)}})\subseteq GT(K^{(9)})$ | $A_{S4}:=\mathrm{im}(\mathrm{Ih}_{N_{S4}})\subseteq GT(N_{S4})$ | ✘ **位数すら UNKNOWN** |
| ③ | **実核体** | $L_9:=\bar{\mathbf Q}^{\ker(\mathrm{Ih}_{K^{(9)}})}$ | $L_{S4}:=\bar{\mathbf Q}^{\ker(\mathrm{Ih}_{N_{S4}})}$ | 定義は一意(§4)・**実体は UNKNOWN** |
| ④ | **分岐 support** | $S_9:=\{\ell:\ell\ \text{ramifies in}\ L_9\}$ | $S_{S4}$ | ✘ **UNKNOWN**(型から推論**不可**・B116-3) |

$$\boxed{\ \textbf{①→② の橋}=\textbf{算術全射性(井原予想の局所形)}\ \textbf{— これが無い限り①の値を②に代入してはならない}\ }$$

---

## §1 marked 算術射影 $\rho_9$ / $\rho_{S4}$ の定義

$\Delta:=\mathrm{Gal}(\mathbf Q(\zeta_9)/\mathbf Q)\cong(\mathbb Z/9)^\times$、$\chi_9:\Delta\xrightarrow{\sim}(\mathbb Z/9)^\times$ を mod 9 円分指標とする。

> ### 定義 **marked 射影**(型付き)
> $$\rho_N:\ A_N\ \longrightarrow\ C_9\qquad\textbf{(群の全射)}$$
> で、次の **marking** を満たすもの: $A_N$ の $\Delta$-共役作用($\Delta$ は $A_N$ の $\mathbf Q(\zeta_9)$ 上の商として作用)に対し
> $$\rho_N(\sigma x\sigma^{-1})=\chi_9(\sigma)\cdot\rho_N(x)\qquad(\textbf{すなわち }\theta=\chi_9\textbf{ 型})$$
> **型**: $\rho_N$ は「$\Delta$-加群への全射」であって、単なる群の全射ではない。**marking を落とすと U9-RIGID$^{\rm mark}$ の前提 (4) が消える。**

| 既存の資源が与えるもの | 与えないもの |
|---|---|
| **U-11**: $\Theta_9$ の**型**に $\mathrm{Aff}(\mathbb Z/9)$ 因子があること ⟹ **$GT(K^{(9)})$ には marked 射影が存在する**(①の言明) | ★ **$A_9$ に制限しても全射のままか**(②の言明)= **①→② の橋・OPEN** |
| **cert**: $\mathfrak F_0(N_{S4})\cong C_9$・$m$ 像 6 元 ⟹ $GT(N_{S4})$ 側の①も既知 | ★ 同上(**$A_{S4}\to C_9$ が全射か**)・**$\mathfrak F_0$ 上の $\Delta$-作用が $\chi_9$ か**(marking 自体が UNKNOWN) |

> ### ⚠ **UNKNOWN(明記)**
> 1. $\rho_9\vert_{A_9}$ の像の位数(§3)。
> 2. $N_{S4}$ 側で **marking $\theta=\chi_9$ が成り立つか**(型の上でも未検証 — $\mathfrak F_0$ が $\Delta$-加群としてどの指標をもつかは cert に無い)。
> 3. $\rho_N$ の**一意性**($C_9$ 商が複数あれば射影は複数)。

---

## §2 $N_{S4}$ の isolated / genuine の現状

| 条件 | $K^{(9)}$ | $N_{S4}$ |
|---|---|---|
| **isolated** | ✔ $K^{(9)}\in I$(ihnec 戦役) | ✘ **UNKNOWN** |
| **genuine / settled** | 正典の dihedral 族として扱われている | ✘ **UNKNOWN** |
| **GTSh 非空性** | — | ✘ **UNKNOWN** |

**根拠**: `hcen_ab` / `lins_census` は自ら明記するとおり **GTSh の非空性・settled/isolated・算術像を判定していない**(v1.4.5 §1.6)。⟹ $N_{S4}$ の三条件は**cert では出ない**。
> $$\boxed{\ \textbf{判定は}\textbf{紙}\textbf{(定義ノートの述語を }N_{S4}\ \textbf{に直接適用)か、}\textbf{新規 cert}\ \textbf{(述語評価器を }N_{S4}\ \textbf{に走らせる)}\ }$$
> ⚠ **ENT-EQUIV の Sol 注記**(F2): 「真正の dihedral 反例と呼ぶには $N=N_1\cap N_2$ の isolated 性、または元が $GTSh(N,N)$ に属することも必要」⟹ **$M$ 側の isolated/genuine も別途 UNKNOWN**。

---

## §3 実像位数の三枝表と ORDER gate

$q:=\lvert Q_A\rvert$ の 9-部分は、**両側の marked 像の共通部分**で決まる。

| $\lvert\rho_9(A_9)\rvert$ | $\lvert\rho_{S4}(A_{S4})\rvert$ | 9 層の共有 | $q$(円分 6 と合わせて) | $\lvert X\setminus A\rvert=972-a_1a_2/q$ |
|---|---|---|---|---|
| 9 | 9 かつ**同一体** | $C_9$ | **54** | $a_1a_2$ 依存(飽和なら 864) |
| 9 | 9 だが**別体** | $1$ | **6** | 同(飽和なら 0) |
| 9 | 3 | $C_3$ まで | **18** | 同(飽和なら 648) |
| $\le3$ | 任意 | $\le C_3$ | $\le18$ | — |

> ### ★ ORDER gate の観測量候補(**いずれも未実装・優劣は未評価**)
> | 候補 | 測るもの | 前件 |
> |---|---|---|
> | **(O1) 次数** | $[L_N:\mathbf Q]=\lvert A_N\rvert$ | ③の実体が要る(循環気味) |
> | **(O2) Frobenius 標本** | 補助素点 $\ell$ での $\mathrm{Ih}_N(\mathrm{Frob}_\ell)$ の位数 ⟹ $\lvert A_N\rvert$ の**下界**を積み上げる | $\mathrm{Ih}_N(\mathrm{Frob}_\ell)$ の計算手段(dessins/Belyi 側)— **未整備** |
> | **(O3) 部分族の既知全射性** | 2 冪族 $n=2^\alpha$ は Cor 5.4 で全射(正典)⟹ **$n=9$ には及ばない** | ✘ 使えない(M-1 の緊張) |
> | **(O4) 型からの上界のみ** | $\lvert A_N\rvert\le\lvert GT(N)\rvert$ | ✔ **無条件**(ただし上界だけ) |
> $$\boxed{\ \textbf{現時点で無条件に使えるのは (O4) の}\textbf{上界}\textbf{のみ ⟹ ENT-MECH の}\textbf{陽性側}\textbf{しか撃てない(v1.4.5 §3.1 と整合)}}$$

---

## §4 実核体 $L_N$ の定義(**一意性だけ固定・実現手段は未定**)

> ### 定義 $L_N$
> $$L_N:=\bar{\mathbf Q}^{\,\ker(\mathrm{Ih}_N)},\qquad \mathrm{Gal}(L_N/\mathbf Q)\ \cong\ A_N$$
> **一意性**: $\ker(\mathrm{Ih}_N)\trianglelefteq G_\mathbf Q$ は $\mathrm{Ih}_N$ から一意に定まり、Galois 対応で $L_N$ も一意 ✔ **有限次ガロア**($A_N$ 有限)✔
> **重要**: この定義は **$A_N=GT(N)$ を仮定しない**(②→③ は標準構成 = 橋不要)。
> ⚠ **実現手段は未定**: $L_N$ の定義多項式・判別式・分岐を得る道は**本 gate の射程外**(それが③→④ の橋 =【ENT-GAP-4】)。

---

## §5 共通円分商の下界の「構成」要件(Sol P2.1 の履行様式)

> ### 要件(**同名では不足**)
> $Q_A^{\rm lb}$ を使うには、**具体的な有限群 $Q$ と二つの全射**
> $$A_1\ \xrightarrow{\ \pi_1\ }\ Q\ \xleftarrow{\ \pi_2\ }\ A_2$$
> を与え、**$\pi_1\circ\mathrm{Ih}_{N_1}=\pi_2\circ\mathrm{Ih}_{N_2}$ が $G_\mathbf Q$ 上の写像として一致する**ことを示す。これで初めて $L_1\cap L_2\supseteq\bar{\mathbf Q}^{\ker(\pi_i\circ\mathrm{Ih}_{N_i})}$ が従い $\lvert Q_A\rvert\ge\lvert Q\rvert$。

> ### ★ 円分部分は**構成可能**(5 項のうち唯一の見込みあり)
> $Q:=\mathrm{Gal}(\mathbf Q(\zeta_d)/\mathbf Q)$、$d:=\gcd(N_{{\rm ord},1},N_{{\rm ord},2})$。$\pi_i$ = GT-shadow の $\lambda=2m+1$ 成分の mod $d$ 還元。
> **一致の根拠**: $\mathrm{Ih}$ の定義により $\lambda$ 成分は**円分指標 $\chi_{\rm cyc}$ そのもの** ⟹ 両側の合成はともに $\chi_{\rm cyc}\bmod d$ ⟹ **一致 ✔**
> ⟹ $$\boxed{\ \lvert Q_A\rvert\ \ge\ \varphi(d)\quad\textbf{が「構成済み」下界として使える(この 1 本だけ)}\ }$$
> ⚠ **ただし**: $A_i$ の $\lambda$ 像が全体かは②の問題 ⟹ **厳密には $\lvert Q_A\rvert\ge\lvert\chi_{\rm cyc}(G_\mathbf Q)\bmod d\rvert=\varphi(d)$**($\chi_{\rm cyc}$ は全射ゆえ ✔)⟹ **この下界は②に依存しない** ✔✔
> **数値**($K^{(9)}$: $N_{\rm ord}=18$ / $K^{(12)}$: $12$)⟹ $d=6$、$\varphi(6)=2$。**$N_{S4}$ の $N_{\rm ord}$ は cert から要取得**。

---

## §6 gate の通過条件(まとめ)

| # | 項目 | 状態 | 通過に要るもの |
|---|---|---|---|
| G1 | isolated / genuine($N_{S4}$・$M$) | ✘ UNKNOWN | 紙判定 or 新規 cert(§2) |
| G2 | marked 射影の存在と marking($\rho_{S4}$ の $\theta=\chi_9$) | ✘ UNKNOWN | 型の水準でも未検証(§1) |
| G3 | 実像位数($\lvert A_9\rvert,\lvert A_{S4}\rvert$) | ✘ UNKNOWN(上界のみ) | ORDER gate の観測量(§3)— **(O2) の整備が律速** |
| G4 | 実核体 $L_N$ | ✔ **定義は固定**(§4) | 実現手段は③→④ の橋 |
| G5 | 共通円分商の構成 | ★ **可**($\varphi(d)$) | $N_{S4}$ の $N_{\rm ord}$ 取得のみ |

> $$\boxed{\ \textbf{5 項中}\ \textbf{通過は G4(定義)と G5(構成)の 2 つ}\ \textbf{。G1–G3 は UNKNOWN で、}\textbf{G3 が律速}\textbf{。}}$$
> ⟹ **ENT-PREFLIGHT の 972 行は「候補格」のまま動かない。** 本 gate は**値を出す工程ではなく、出せない理由を型付きで確定する工程**である。

---

## §7 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| ★ **【GATE-GAP-1】** | **①→② の橋**(算術全射性)が両窓で無い — 本 gate の根本 | ★★ 最大 |
| ★ **【GATE-GAP-2】** | $N_{S4}$ 側の **marking $\theta=\chi_9$ が型の水準でも未検証** | ★ 中 |
| ★ **【GATE-GAP-3】** | ORDER gate の観測量 **(O2) Frobenius 標本の計算手段が未整備**(律速) | ★★ 大 |
| **【ENT-GAP-4/5/6】** | S4-RAM-SUPPORT / K9-BRIDGE / ORDER(v1.4.5 §8 で採番済) | ★ 中 |
| **【GATE-GAP-4】** | $M=K^{(9)}\cap N_{S4}$ 自身の isolated/genuine も UNKNOWN(Sol F2) | ★ 中 |

**帰属**: 段構成と「実質の最前線」の指定 = **Sol**(P4)。TYPE-IMAGE 規約の起点 = Sol R0 + 数学者(v1.4.4 §6.1)。委嘱 = 司令塔(裁定 872)。$\Theta_9$・$\mathfrak F_0$・972 = ihnec 戦役。
**本 gate の新規部分** = **4 対象への帰属表(§0)** / **marked 射影の型付き定義($\Delta$-加群への全射)** / **§2 の「cert では出ない」の確定** / **§3 の三枝表と観測量候補 4 種((O3) が使えない理由込み)** / **§4 の $L_N$ 一意性(②→③ は橋不要)** / ★ **§5 の円分下界が「②に依存せず構成できる」ことの証明**($\chi_{\rm cyc}$ の全射性を使う)/ **§6 の通過条件表(2/5 通過・G3 が律速)**。

**novelty grep**: `ENT-ARITH-TYPE` `GATE-GAP-*` `marked 射影` = **0 hit(本ノート初出)**。
