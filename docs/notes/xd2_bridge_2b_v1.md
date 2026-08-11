# 2-B の橋 — **通る**。RIBET-WINDOW 全域定理の復活(裁定 813)

**日付**: 2026-08-11 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・判定語の発効は司令塔専権)
**入力**: `docs/notes/cv9_chi_semantics_audit_v1.md`(falsifier・CV-9 判読)/ 裁定 813
**先行**: `xd2_twist6abs_adjudication_v1.md`(定理 TWIST-6-ABS)/ `card_pchi_m5_v1.md` / 規約 CHI-CARRY(813 暫定採択)

---

## §0 裁定(先出し)

| falsifier 指摘 | 私の答え |
|---|---|
| **2-A** 「§3(B) 撤回」はすり替え | ★ **全面的に受諾**。私の誤り(§1) |
| **2-B** 全域定理化に橋が未記載 | ★ **橋は通る**(§2 で証明)。ただし**主張の形が変わる** — 「$\rho$ の合成因子」ではなく「**非分裂性**」が消せない対象(§2.3) |
| **2-C/2-E** 条件束の分離 | ★ 受諾(§4) |
| **2-F** 切片定義は両端 $G$-正規 | ★ 受諾・§2 では最初から両端正規で書く |
| **1-A / 1-B / 2-H / ⑧ / ⑨** | 受諾(§5・編纂内の作業) |

---

## §1 2-A — 私の誤りの整理(すり替えの正体)

カード §3 の (B) は **抽象 $\mathbf F_p[G]$-加群**(切片でない)と書いてあった。xd2 §3 で私はそれを「外部標数の切片」と読み替えて撤回した。**この読み替えが無根拠だった。**

しかも**「外部標数の切片」は空概念**である: 切片 $A/B$($A,B\trianglelefteq G$)は $G$ の subquotient ゆえ $\lvert A/B\rvert\mid\lvert G\rvert$ ⟹ **必ず $p\mid\lvert G\rvert$**。⟹ 私が「閉じた」と言った対象は**最初から存在しなかった**。

> ### ★ 扉表の正しい形(カード §3 を差し替え・CHI-CARRY 準拠)
> | 読み | 対象 | $M_5$($e=10$)での状態 |
> |---|---|---|
> | **(A) 切片読み**(CHI-CARRY の述語) | $W=A/B$、$A,B\trianglelefteq G$ | ★ **閉**($\mathrm{ord}\mid\gcd(10,6,p-1)\mid2$・全 $p$。ただし $p\mid\lvert G\rvert$ は自動) |
> | **(B) 表現読み**(述語の外) | 抽象 $\mathbf F_p[G]$-加群 | ★ **開いたまま**。$G\twoheadrightarrow C_{10}\hookrightarrow\mathbf F_{11}^\times$ 等で**位数 10 が実在**($p=11,31,41,61,71$) |
> | **(C) $\dim\ge2$ 切片** | 非可換像・$\{\chi,\chi^{-1}\}$ | **開**(§3・§4) |
>
> **(A) と (B) は「同じ扉の二読み」ではなく別の扉。** xd2 §3 の表は本節で撤回・差し替え。

---

## §2 ★★★ 2-B の橋 — **通る**

## 2.1 橋(falsifier の候補を厳密化)

Ribet の $\rho:G_\mathbb Q\to GL_2(\mathbf F_p)$($p=691$, $k=12$)は**可約かつ非分裂**で、適当な基底で
$$\rho=\begin{pmatrix}1&*\\0&\omega^{k-1}\end{pmatrix},\qquad H:=\rho(G_\mathbb Q)\ \ \text{(像)}$$
$U:=H\cap\Bigl\{\begin{pmatrix}1&*\\0&1\end{pmatrix}\Bigr\}$ を単巾根基とおく。$\rho$ が**非分裂**であることは $U\ne1$ と同値で、このとき $U\cong\mathbf F_p$(位数 $p$)。

> ### 補題 **UNIP-CHAR**(candidate・本ノート)
> (i) $U\trianglelefteq H$ かつ **$U$ は $H$ の特性部分群**。
> (ii) $H$ の $U$ 上の共役作用は指標 $\omega^{1-k}$ による。$k=12$, $p=691$ で $\mathrm{ord}(\omega^{11})=690/\gcd(11,690)=\mathbf{690}$。
> **証明**: (i) $\lvert H/U\rvert$ は $\omega^{k-1}$ の像の位数 $=690$ を割り、$\gcd(691,690)=1$ ⟹ $U$ は $H$ の**唯一の** Sylow $691$-部分群 ⟹ 特性。
> (ii) $\begin{pmatrix}a&0\\0&d\end{pmatrix}\begin{pmatrix}1&u\\0&1\end{pmatrix}\begin{pmatrix}a&0\\0&d\end{pmatrix}^{-1}=\begin{pmatrix}1&ua/d\\0&1\end{pmatrix}$ ⟹ 作用は $\chi_1/\chi_2=1/\omega^{k-1}=\omega^{1-k}$。∎

## 2.2 定理

> ### 定理候補 **RW-ABS**(candidate・本ノート)
> $r>6$ とし、$H$ を「1 次元 $\mathbf F_p$ 単巾根基 $U$ をもち、$H/U$ が $U$ に位数 $r$ の指標で忠実に作用する($\gcd(p,r)=1$)」群とする。すると
> $$\boxed{\ H\ \textbf{は }B_3\ \textbf{の任意の商 }G\ \textbf{の切片として現れない(商としても現れない)}\ }$$
> **証明**: $H=A/B$($A,B\trianglelefteq G$)と仮定。$U$ は $H$ の特性部分群(補題 (i))ゆえ、$G$ の共役作用は $U$ を保つ。$\tilde U:=$($A$ 内の $U$ の原像)とおくと $\tilde U\trianglelefteq G$、$B\trianglelefteq G$、$\tilde U/B\cong U\cong\mathbf F_p$ は**両端 $G$-正規な 1 次元切片**。
> $G$ の $\tilde U/B$ 上の共役作用は $A$ 上で $H$ の作用に一致 ⟹ その像は位数 $r$ の部分群を含む ⟹ $\mathrm{ord}(\chi_{\tilde U/B})\ge r>6$。
> しかし **TWIST-6-ABS** より $\mathrm{ord}\mid\gcd(e,6,p-1)\mid6$。矛盾。∎
>
> **Ribet への適用**($r=690$): $\boxed{\ \textbf{Ribet の像 }H\ \textbf{は }B_3\ \textbf{のどの商の切片にもならない}\ }$

## 2.3 ★★★ 主張の形が変わる — **消せないのは「非分裂性」**

falsifier の指摘(「比が自明な可約表現に論法が通らない」)は正しく、**それがそのまま定理の内容になる**:

| $\rho$ の型 | 像 $H$ | $B_3$ 商に入るか |
|---|---|---|
| **分裂(半単純)** $1\oplus\omega^{k-1}$ | $U=1$、$H\cong C_{690}$ 可換 | ○ **入りうる**(表現読み・§1(B))。ただし**指標の直和にすぎず類群情報を運ばない** |
| ★ **非分裂**(= Ribet の定理の内容) | $U\cong\mathbf F_{691}$、$H$ 非可換 | ✘ **絶対に入らない**(RW-ABS) |

> $$\boxed{\ \textbf{Ribet の算術的内容は「拡大類が非自明であること」= 非分裂性そのもの。}\ \textbf{ゆえに }B_3\ \textbf{商が運べないのは}\textbf{まさにその内容}\textbf{である。}}$$

⟹ **全域定理は復活する**が、正しい文言は
> 「$\chi^{11}$ が窓に入らない」(← 型不整合)ではなく
> ★ **「Ribet の像($=$ 非分裂拡大)は $B_3$ のどの商の切片にもならない — 窓か否かも $c\in N$ も $e$ も不問」**

---

## §3 ★★ 概念的な心臓 — 命題 **SEC-MOD**(TWIST-6-ABS の真の理由)

> ### 命題候補 **SEC-MOD**(candidate・本ノート)
> $G=B_3/N$ 任意、$W=A/B$($A,B\trianglelefteq G$)任意の切片とすると
> $$\boxed{\ G/C_G(W)\ \textbf{は }PSL(2,\mathbf Z)=C_2*C_3\ \textbf{の商 — すなわち }(2,3)\textbf{-生成}\ }$$
> **証明**: $c$ の像 $z$ は $G$ の中心元 ⟹ 全切片に自明作用 ⟹ $z\in C_G(W)$ ⟹ $G/C_G(W)$ は $G/\langle z\rangle$ の商であり、$G/\langle z\rangle$ は $B_3/\langle c\rangle=PSL(2,\mathbf Z)$ の商。∎
>
> ★ **系 = TWIST-6-ABS**: $\dim W=1$ なら $G/C_G(W)$ は可換 ⟹ $(C_2*C_3)^{\rm ab}=C_2\times C_3=C_6$ の商 ⟹ **位数 $\mid6$**。
> $$\boxed{\ \textbf{「6」の正体は }\ PSL(2,\mathbf Z)^{\rm ab}=C_6\ \textbf{。}}$$

**これで TWIST-6 / TWIST-6-ABS / SG-EXACT の G2((2,3)-生成)が一本の事実に統合される。** $B_4$ 版は $B_4/\langle\Delta_4^2\rangle$ の ab が $C_{12}$ 型 ⟹ TWIST-12 の別証(【XD2-GAP-1】)。

---

## §4 2-C/2-E — 条件束の分離(死んだ道と生きている道)

| 道 | 条件 | 状態 |
|---|---|---|
| **切片・$\dim1$**(旧「唯一の残り番地 $W_{691}$」) | 旧記載「$345\mid j$ **かつ** $691\mid\lvert G\rvert$」 | ✘ **死道の条件**。RW-ABS で $\dim1$ 切片は位数 6 で絶対閉鎖 ⟹ **この 2 本の合同式は撤回** |
| ★ **切片・$\dim\ge2$ 非可換**(生存道) | ① $p\equiv\pm1\pmod r$($r=690$: $+1$ 側 $691,1381$ / $-1$ 側 $2069,3449$)**のみ** | ○ **生存**。$e$ への条件は**ない**($\det=\chi\chi^{-1}=1$ ゆえ TWIST-6-ABS の束縛を自動的に満たす) |
| | ★ ② **新規(SEC-MOD)**: 作用群 $G/C_G(W)\subseteq GL_2(\mathbf F_p)$ が **(2,3)-生成**、かつ $\mathrm{ord}(\det)\mid\gcd(e,6)$ | ★ **新しい絞り**(§4.1) |

### 4.1 ★ 新しい絞り込み(SEC-MOD の (C) 道への適用・要追検分)

位数 690 の元(固有値 $\{\chi,\chi^{-1}\}$・$\det=1$)を含む $GL_2(\mathbf F_{691})$ の部分群で **(2,3)-生成**なものは何か。
- **$SL(2,691)$ は不可**: 対合が中心の $-I$ 一つだけ ⟹ $\langle$対合, 位数 3$\rangle=\langle-I,b\rangle$ は可換 ⟹ 全体を生成しない。
- **分裂トーラスの正規化群 $D_{2\cdot690}$ も不可**: 二面体群は(位数 3 の回転を使う限り)位数 6 の部分群しか生成しない。
- **残る候補**: $\det=\pm1$ 群 $\langle SL(2,691),\ \mathrm{diag}(1,-1)\rangle$ 型(非中心対合をもち $\det$ の位数 $2\mid6$ ✔)。
> $$\boxed{\ \textbf{⟹ (C) 道の作用群は「}SL_2\ \textbf{を含み、かつ }\det\ \textbf{の位数が }6\ \textbf{を割る非中心対合をもつ」型に絞られる(candidate・要検分)}\ }$$
> **【BR-GAP-1】**: この型が実際に $B_3$ 商として実現するかは UNKNOWN。**XD 札の Burau 窓 $W_{691}$ 系が撃つべき正確な標的**はこれ。

---

## §5 受諾事項(編纂内の修正作業として実施)

- **1-A**: 「較正ゲート通過」表現は撤回 ⟹ **「TWIST-GCD と TWIST-6-ABS は全 40 点で無矛盾。識別力ある実例は 0 本」**と書く。識別点条件 $r\ge5\wedge r\mid e\wedge r\mid p-1$ は §1(B) の表現読みでのみ発生しうる ⟹ P-DISC-1 の結果を待つ。
- **1-B**: 追補 A §2.2 の「$Q_8$ 因子 $\mathrm{ord}\mid3$」は **cert 未裏取り**と明記。ただし §3(SEC-MOD)から $\gcd(3m,6)=3$ が**紙で従う**ので、主張自体は紙で独立に立つ(pchi1_v2 は確認)。
- **2-F**: 定理文の切片定義を **$A,B$ とも $G$-正規**に統一(本ノートは最初からこの形)。
- **2-H**: RW-CYC 簿記(「13/13」→窓層 15 行・$882/936/936$ の $\widehat G^{\rm ab}$ 未実測値混入)は**機械配管違反**として編纂で訂正・値は再生成を待つ。
- **⑧ CHI-CARRY**: 批准に賛成。**DOMAIN-PIN 第 4 点に `chi_semantics ∈ {切片読み, 表現読み}` を必記**とする形で統合。
- **⑨ ★ $[750,6]$ の $\dim2/\mathbf F_5$ 因子 $\{\zeta_6,\zeta_6^{-1}\}$・$\det=1$**: **CHI-DICHOTOMY の生存道の実物** ⟹ 編纂の扉節の実例に採用。$r=6$($\le6$)なので χ 扉そのものではないが、**「$\{\chi,\chi^{-1}\}$ 対という形が census 内に実在する」ことの証拠**。$p=5$ で $p\equiv\pm1\pmod 6$ ✔($5\equiv-1$)⟹ **§4 の必要条件 $p\equiv\pm1\pmod r$ の初の実例**でもある。

---

## §6 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| **【BR-GAP-1】** ★新 | §4.1 の作用群型が $B_3$ 商として実現するかは UNKNOWN | ★ 中 |
| **【BR-GAP-2】** ★新 | RW-ABS は $\gcd(p,r)=1$ を使う(単巾根基が特性であるため)。$p\mid r$ の場合は未検分 | 小 |
| **【XD2-GAP-2】** | ★ **閉**: CHI-CARRY 採択+§1 の扉表差し替えで「切片 vs 表現」の分離が明文化 | 閉 |

**帰属**: CV-9 判読・2-A〜2-H の摘発・橋の候補(単巾根基 $U$・両端 $G$-正規)= **falsifier**。委嘱 = 司令塔(裁定 813)。$[750,6]$ の $\dim2$ 因子の発見 = falsifier。
本ノートの新規部分 = **補題 UNIP-CHAR($U$ が特性・作用は $\omega^{1-k}$)** / **定理 RW-ABS(橋の厳密化と全域定理の復活)** / **§2.3 の主張の形の訂正(消せないのは非分裂性)** / **命題 SEC-MOD(「6」の正体 $=PSL(2,\mathbf Z)^{\rm ab}=C_6$・TWIST-6-ABS/SG-EXACT G2 の統合)** / **§4.1 の (C) 道の新しい絞り($SL_2$ は (2,3)-生成でない)** / **§1 の扉表の再構成**。

**novelty grep**(`docs/` `provenance/`): `RW-ABS` `UNIP-CHAR` `SEC-MOD` `PSL(2,Z)^ab` = **0 hit(本ノート初出)**。

**検算コマンド**(裁定 668 拡張):
```bash
python -c "
from math import gcd
from sympy import isprime
print('ord(omega^11) at p=691:', 690//gcd(11,690))          # 690
print('gcd(691,690) =', gcd(691,690))                        # 1 -> U は唯一 Sylow
print('TWIST-6-ABS bound gcd(e,6):', [(e,gcd(e,6)) for e in (2,6,10,15,45,690)])
print('p = +-1 mod 690:', [x for x in (690*k+1 for k in range(1,6)) if isprime(x)][:2],
                          [x for x in (690*k-1 for k in range(1,8)) if isprime(x)][:2])
print('[750,6] check: p=5, r=6, 5 mod 6 =', 5%6, '(= -1 -> 必要条件 OK)')
"
```
