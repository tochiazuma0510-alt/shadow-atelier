# 【ISO-S4】紙側 3 点の検分 — settled ⟹ isolated / $S_3$ 拡大水準 / $c\in N_{S4}$

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 894 第二仕事(裁定 889/891/892 の紙側残件)
**格**: **すべて candidate**(紙・単系統・**Sol 未監査**)。機械側の値は **cross-checked** どまり — **verified は Lean に予約**。
**対象 cert**: `search/certs/s4_settled54_v2_20260812.json`(commit `43542bb`・生成器 `search/s4_settled54_v1.g`)
**正典**: 2401.06870(**Def 3.13** = 印刷 p.20)/ 2405.11725 / `docs/week1-定義ノート.md`(Def 3.1・Def 3.7・Prop 3.2・Prop 3.4・Prop 3.6)

> ### ★ 結論の一行
> $$\boxed{\ \textbf{(i) 成立(ただし「1 行」の中身は}\textbf{全称量化子の解消}\textbf{) / (ii) }\textbf{理由づけが不足}\textbf{— 1 行で修理可 / (iii) 正しく完結}\ }$$

---

## §0 三点の位置関係(**先に依存関係を書く** — 独立 3 件ではない)

$$\boxed{\ \textbf{(iii) }c\in N_{S4}\ \Longrightarrow\ \textbf{列挙器の }W1\ \textbf{近道が合法}\ \Longrightarrow\ \textbf{(i) の完全性 (A)}\ }$$
$$\boxed{\ \textbf{(ii) }S_3\ \textbf{水準が恒等}\ \Longrightarrow\ \ker T_{m,f}\subseteq PB_3\ \textbf{かつ}\ T_{m,f}(PB_3)\subseteq PB_3/N\ \Longrightarrow\ \textbf{機械の }\ker\psi=1\ \textbf{が (i) の (B) になる}\ }$$

⟹ **(ii)(iii) は (i) の前件**。cert が三つを並列に置いているのは記帳上の便宜であって、論理は上の 2 本の矢印で結ばれている。

---

## §1 (i) settled ⟹ isolated — **Def 3.13 の最終 1 行**

### 1.1 正典の逐語(2401.06870 印刷 p.20・Def 3.13)

> Let $N\in\mathrm{NFI}_{PB_3}(B_3)$. A GT-shadow $[m,f]\in GT(N)$ is called **settled** if $\ker(T_{m,f})=N$, i.e. $[m,f]\in GTSh(N,N)$. An object $N$ of the groupoid $GTSh$ is called **isolated** if **every** GT-shadow in $GT(N)$ is settled.
> It is clear that $N$ is isolated if and only if the connected component of $N$ in $GTSh$ has exactly one object. Of course, in this case, $GT(N)=GTSh(N,N)$. In particular, **$GT(N)$ is a group**.

### 1.2 ★ 判定: **isolated は定理ではなく定義**である

「settled ⟹ isolated」は**含意ではない**。isolated は $\forall[m,f]\in GT(N):$ settled と**定義されている**。
$$\boxed{\ \textbf{従って「最終 1 行」の数学的内容は}\ \textbf{全称量化子 }\forall[m,f]\in GT(N)\ \textbf{をどう解消したか}\ \textbf{に尽きる}\ }$$
⟹ **証明の重心は (b) kernel equality ではなく (a) 完全性にある**。cert が (a) を先に置いているのは正しい。

### 1.3 補題 **ISO-S4-FINAL**(candidate)

**前件**
- **(A)〔完全性〕** 列挙された 54 個の集合 $\mathcal S$ が $\mathcal S\supseteq GT(N_{S4})$ を満たす。
- **(B)〔kernel equality〕** 各 $[m,f]\in\mathcal S$ で $\ker(T_{m,f})=N_{S4}$。

**結論** $N_{S4}$ は **isolated**。さらに $GT(N_{S4})=GTSh(N_{S4},N_{S4})$ は**群**であり、$GTSh$ における $N_{S4}$ の連結成分は**一点**。

**証明** (A)(B) より $\forall[m,f]\in GT(N_{S4}):\ker(T_{m,f})=N_{S4}$、すなわち全 shadow が settled。Def 3.13 を適用。∎

> ### ★★ 検分で得た非自明な観察 — **必要なのは $\supseteq$ であって $=$ ではない**
> (A) を「$\mathcal S=GT(N_{S4})$」ではなく「$\mathcal S\supseteq GT(N_{S4})$」で書いた。理由: $\mathcal S$ が**真の超集合**でも (B) は $GT(N_{S4})$ の全元を覆うので isolated は従う。
> $$\boxed{\ \textbf{列挙器が}\textbf{余分な候補を混ぜる}\textbf{のは isolated の証明にとって}\textbf{無害}\textbf{。}\textbf{取りこぼす}\textbf{のだけが致命的}\ }$$
> ⟹ ★ **cert の (c) staleness check(「降下フィルタが列挙に混入していないか」)は、まさに致命的な方向だけを検査している** — 設計として正しい。
> ⚠ **ただし超集合の場合 $\lvert GT(N_{S4})\rvert<54$ となり、$54$ を位数として使う下流の主張(§10 の圧縮率 $C=6=108\cdot54/972$ 等)は別途 $\mathcal S=GT(N_{S4})$ を要する。** isolated だけが超集合で足りる。

### 1.4 (A) の分解と、cert がどこまで供給したか

正典の定義(定義ノート Def 3.1 / Def 3.7)より
$$GT(N)\ \subseteq\ \mathcal X_N\times[G,G],\qquad G:=F_2/N_{F_2}\cong PB_3/N,$$
$$\mathcal X_N=\{m\in\{0,\dots,N_{\rm ord}-1\}\ :\ \gcd(2m+1,N_{\rm ord})=1\}$$
(**charming** の定義そのもの: $2m+1\in(\mathbf Z/N_{\rm ord})^\times$ かつ $fN_{F_2}\in[F_2/N_{F_2},F_2/N_{F_2}]$)。

| 分解 | 内容 | 供給元 | 私の検算 |
|---|---|---|---|
| **(A1)** | $GT(N)\subseteq\mathcal X_N\times[G,G]$ | ★ **定義から自動**(charming)— 仮定ではない | ✔ |
| **(A2)** | 候補全体 $=\lvert\mathcal X_N\rvert\cdot\lvert[G,G]\rvert$ を**全走査** | cert `candidate_total=3024`・`candidate_total_eq_dwords_times_charming=true`・`bfs_covers_full_g=true` | ✔ **手検算一致**(下記) |
| **(A3)** | 除外フィルタが**必要条件のみ**($W1$ = 簡約 hexagon (3.10)(3.11)、SURJ = 全射性) | cert `no_descent_filter_in_enumeration`(生成器 lines 315–372 + 裁定 529) | ✔ 両者とも Def 3.7 の**定義の一部** ⟹ 除外は無損失 |

**(A2) の手検算**(私の独立計算):
$N_{\rm ord}=9$ に対し $2m+1\bmod9$ は $m=0,\dots,8$ で $1,3,5,7,0,2,4,6,8$。$\gcd(\cdot,9)=1$ となるのは $m\in\{0,2,3,5,6,8\}$ ⟹ $\lvert\mathcal X_9\rvert=\mathbf 6$(cert `charming_set_size=6` と一致)。
$G\cong PSL(2,8)$ は**単純ゆえ perfect** ⟹ $[G,G]=G$、$\lvert[G,G]\rvert=504$(cert は独立 2 経路 `dwords_count` と `independent_gap_call` で 504 を一致確認)。
$$6\times504=3024\quad\checkmark$$

> ### ⚠★ **(A3) の隠れた前件 — ここが (iii) と結ばれる**
> 定義ノートの実装注記(2026-07-25・$M_5$ で判明)は明記する:
> > $\theta/\tau$ を商 $F_2/N_{F_2}$ 上の準同型として評価する近道は $N_{F_2}$ の $\theta,\tau$-不変性を要し、これは **$c\in N$** に依存する。$c\notin N$ の対象では近道が壊れる(定理は無傷)。
> cert の $W1$ は**まさにこの近道**(`GroupHomomorphismByImages` による $\theta/\tau$ 評価)である。
> $$\boxed{\ \Longrightarrow\ \textbf{(iii) }c\in N_{S4}\ \textbf{は (A3) の前件であり、独立な傍証ではない}\ }$$
> ★ cert の `point2_c_in_N.paper_cross_reference.load_bearing=false` は「**紙の論証**が load-bearing でない(機械値が直接あるから)」の意味であり、その読みなら正しい。⚠ **ただし「$c\in N_{S4}$ という事実」自体は (a) にとって load-bearing** — この区別を cert の語で読み違えないこと。

### 1.5 ⟹ (i) の判定

$$\boxed{\ \textbf{(i) は}\textbf{成立}\textbf{。ただし「Def 3.13 の 1 行」は}\textbf{定義の適用}\textbf{であり、実質は (A1)(A2)(A3) の三点}\ }$$
**残 GAP**: なし(紙側)。⚠ **格は candidate** — (A2)(A3) は cert の申告に依存し、私は生成器を独立実行していない。**格は cross-checked どまり**。

---

## §2 (ii) $S_3$ 拡大水準の初等論証 — ★ **理由づけが不足**(結論は正しい)

### 2.1 cert / 生成器の原文(`search/s4_settled54_v1.g` lines 127–131)

> This directly computes $\ker(T_{m,f})\cap PB_3=N_{S4}\cap PB_3$ at the $PB_3/N$ level (elementary argument …: $N_{S4}\le PB_3$ for this window per PU-F7, and **the $B_3/PB_3=S_3$ quotient component of $T_{m,f}$ is untouched by $m,f$** — $\bar\Delta,\bar\delta_B$ are FIXED markings independent of the shadow per PU-F8 — so kernel equality at the full $B_3$ level reduces to triviality of $\mathrm{Kernel}(\psi)$ here, GIVEN `c_in_N` holds).

### 2.2 ★★ 検分 — **「$m,f$ に無依存」では足りない**

機械が計算するのは $\psi:PB_3/N\to PB_3/N$ の核の自明性、すなわち
$$\ker(T_{m,f})\cap PB_3=N_{S4}.$$
Def 3.13 が要求するのは $B_3$ の部分群としての $\ker(T_{m,f})=N_{S4}$。両者の差は
$$\ker(T_{m,f})\subseteq PB_3\quad(\ast)$$
の 1 点である。$(\ast)$ を出すには、$T_{m,f}$ が誘導する $S_3=B_3/PB_3$ 上の自己写像が **単射**でなければならない。

> $$\boxed{\ \textbf{「}m,f\ \textbf{に無依存(independent)」}\ \ne\ \textbf{「恒等(identity)」}\ \ne\ \textbf{「単射」}\ }$$
> ⚠ 仮に固定された $S_3$ 成分が**自明写像**や**核 $A_3$ をもつ写像**であっても「$m,f$ に無依存」は真である。**無依存性からは $(\ast)$ は出ない。**
> ⟹ cert の理由づけは**必要な強さに達していない**。★ ただし**結論は正しい** — 下記 1 行で埋まる。

### 2.3 ★ 修理(命題 **S3-ID**・candidate・証明つき)

**命題 S3-ID.** 任意の GT-shadow $[m,f]\in GT(N)$($N\in\mathrm{NFI}_{PB_3}(B_3)$)に対し、$T_{m,f}$ が $B_3/PB_3\cong S_3$ 上に誘導する自己写像は**恒等写像**である。

**証明**(4 行)
1. $u:=2m+1$ は**定義から奇数**(Prop 3.2: $T_{m,f}(\sigma_1)=\sigma_1^{u}N$, $T_{m,f}(\sigma_2)=f^{-1}\sigma_2^{u}fN$)。
2. $f\in[F_2,F_2]\subseteq F_2\subseteq PB_3$ ゆえ、$B_3\to S_3$ の下で $f\mapsto1$ ⟹ 誘導写像は $s_i\mapsto s_i^{u}$($s_i$ = $\sigma_i$ の像)。
3. $s_1,s_2$ は $S_3$ の**互換**で位数 2、$u$ は奇数 ⟹ $s_i^{u}=s_i$。
4. $S_3=\langle s_1,s_2\rangle$ ⟹ 誘導写像は恒等。∎

**系 S3-ID(a)**: 誘導写像が恒等 ⟹ 単射 ⟹ $\ker(T_{m,f})\subseteq PB_3$、すなわち $(\ast)$。
**系 S3-ID(b)**: 同じ理由で $T_{m,f}(PB_3)\subseteq PB_3/N$ ⟹ **$\psi$ の定義そのものが正当化される**。
**系 S3-ID(c)**: $(\ast)$ と機械値 $\ker\psi=1$ と $N_{S4}\subseteq PB_3$ を合わせて
$$\ker(T_{m,f})=\ker(T_{m,f})\cap PB_3=N_{S4}.$$

> ### ★ 判定
> $$\boxed{\ \textbf{結論は正しいが、cert の理由(「}m,f\ \textbf{に無依存」)は}\textbf{十分でない}\ \Longrightarrow\ \textbf{命題 S3-ID に差し替える}\ }$$
> ★ **load-bearing なのは「$u$ が奇数」**であって「無依存」ではない。実装係の申告(「数学者検分対象に含めるのが安全」)は**正しい判断**だった。
> ⚠★ **S3-ID は二重に load-bearing**: 系 (a) が $(\ast)$ を、系 (b) が $\psi$ の存在自体を支える。cert の (b) 項全体がこの命題の上に乗っている。

---

## §3 (iii) $c\in N_{S4}$ の 2 行中心性論法 — ★ **正しく完結**

### 3.1 cert の原文(`point2_c_in_N.paper_cross_reference.argument`)

> $c$ is central in $B_3$, hence central in $PB_3$; its image lies in $Z(PSL(2,8))$; $Z(PSL(2,8))=1$ (PSL simple, trivial center) $\Rightarrow$ image $=1$ $\Rightarrow$ $c\in N_{S4}$.

### 3.2 ★ 検分 — 各段の裏取り

| 段 | 主張 | 裏取り |
|---|---|---|
| 1 | $c=\Delta^2$ は $B_3$ の中心元($\Delta=\sigma_1\sigma_2\sigma_1$) | ✔ 古典的($Z(B_3)=\langle\Delta^2\rangle$)。**$c\in PB_3$** も要る: $\Delta\mapsto$ 互換だが $\Delta^2\mapsto1$ ⟹ $c\in PB_3$ ✔ |
| 2 | $c\in Z(PB_3)$ | ✔ $c$ は $B_3$ の全元と可換、特に $PB_3$ の全元と。かつ $c\in PB_3$ ⟹ $c\in Z(PB_3)$ |
| 3 | 像が $Z(PB_3/N_{S4})$ に入る | ✔ **全射準同型は中心を中心へ写す**。$PB_3\twoheadrightarrow PB_3/N_{S4}$ は全射 |
| 4 | $Z(PSL(2,8))=1$ | ✔ $PSL(2,q)$ は $q\ge4$ で単純、非可換単純群の中心は自明。$\lvert PSL(2,8)\rvert=504$ |
| 5 | ⟹ 像 $=1$ ⟹ $c\in N_{S4}$ | ✔ |

$$\boxed{\ \textbf{(iii) は}\textbf{正しく、隙間なし}\textbf{。機械値 }S^2=()\ \textbf{の}\textbf{独立な紙側裏取り}\textbf{として成立}\ }$$

### 3.3 ★ 一般化(本検分の副産物・candidate)

**命題 CENT-IN-N.** $N\in\mathrm{NFI}_{PB_3}(B_3)$ が $PB_3/N$ **中心無し**(例: 非可換単純)ならば $Z(PB_3)\subseteq N$、特に $c\in N$。

**証明** $z\in Z(PB_3)$ の像は全射準同型で $Z(PB_3/N)=1$ に入る ⟹ 像 $=1$ ⟹ $z\in N$。∎

> ★ ⟹ **$c\in N$ は $S4$ 窓に固有の事実ではなく、$PB_3/N$ が非可換単純な窓族すべてで自動**(PSL 族全体)。
> ⚠ 逆に **$PB_3/N$ が中心をもつ窓では $c\in N$ は保証されない** — 定義ノートが $M_5$ を「近道が壊れる例」として挙げているのと整合する。⟹ ★ **$W1$ 近道の可否は窓ごとに $Z(PB_3/N)$ を見れば判る**(実務上有用な判定法)。

---

## §4 総合判定と残件

| # | 点 | 判定 | 残件 |
|---|---|---|---|
| **(i)** | settled ⟹ isolated(Def 3.13 最終 1 行) | ★ **成立**(定義の適用)。実質は (A1) 定義から自動 + (A2) 手検算一致 + (A3) 必要条件のみ | **紙側なし**。格 = **cross-checked**(生成器を独立実行していない) |
| **(ii)** | $S_3$ 拡大水準の初等論証 | ⚠ ★ **理由づけ不足**(無依存 ≠ 恒等 ≠ 単射)⟹ **命題 S3-ID に差し替え**。結論は正しい | cert の当該コメントを S3-ID の文言へ改める(**実装係へ差し戻すほどではない — 本ノートが正本**) |
| **(iii)** | $c\in N_{S4}$ の中心性論法 | ★ **正しく完結**。副産物 **CENT-IN-N** で窓族一般へ | なし |

> ### ★★ ⟹ 【ISO-S4】の状態
> $$\boxed{\ \textbf{紙側 3 点はすべて閉じた}\ \Longrightarrow\ N_{S4}\ \textbf{は isolated}\ \textbf{(格 = candidate / cross-checked・Sol 未監査)}\ }$$
> ⟹ **2401 Prop 3.15** により $M=K^{(9)}\cap N_{S4}$ も isolated ⟹ $\rho_{S4},\rho_M$ が**群準同型として定義され**、$A_{S4},L_{S4},S_{S4},A_M,L_M,S_M$ が意味をもつ。
> ⟹ **COMPOSITUM-$\rho$**(見立て v1.4.7 §2.2)の前件 1 が満たされ、$L_M=L_9L_{S4}$ が使える(前件 2・3 は別途)。
> ⟹ **G6** の条件付き形($d=9$・$\mathbf Q(\zeta_9)\subseteq L_9\cap L_{S4}$・$\lvert Q_A\rvert\ge6$)も前件が揃う。
>
> ⚠★ **ただし発火は依然しない**: 972 屋根の窓側圧縮率は $C=6$ で、円分下界も $\varphi(9)=6$ ⟹ $6>6$ は**偽**。
> $$\boxed{\ \textbf{ISO-S4 が閉じても 972 は発火しない — 必要なのは}\ \lvert Q_A\rvert>6\ \textbf{を与える}\textbf{非円分の共通部分体}\ }$$
> ★ **過大評価しないこと。** 閉じたのは**型の門(G0)**であって、発火条件ではない。

**⚠ 本ノートは Sol 未監査**。見立て v1.4.7 §10 の「本版時点で $N_{S4}$ の isolated は依然 UNKNOWN」は**本ノートより前の時点の記述**であり、**Sol 検収後に v1.4.8 で更新する**(先走って書き換えない)。

---

## §5 帰属・依存申告

- **Def 3.13 の逐語**・型境界(isolated = 対象の述語 / settled = shadow の述語)= 正典 2401.06870 + **Sol 便 118 F2**。
- **I2 再監査路への一本化**($S\times S$ 反模型で I1 を落とす)= **Sol 便 118 P3.3**。
- **機械側 (a)(b)(c)(d)** = 実装係 cert `s4_settled54_v2_20260812`(裁定 891/892 仕様)。
- **本ノートの新規部分** = ① **(A) を $\supseteq$ で書けば足りるという観察**(超集合は無害・取りこぼしのみ致命的)② **(iii) ⟹ (A3) の依存関係の摘出**($W1$ 近道は $c\in N$ に依存)③ **命題 S3-ID**(「無依存」では不足・$u$ 奇数から恒等を出す 4 行)④ **命題 CENT-IN-N**(窓族一般への一般化と $W1$ 近道の判定法)。
- **未実施**: 生成器 `search/s4_settled54_v1.g` の独立再実行、独立照合器の再実装、Lean 化。⟹ **verified ではない**。
