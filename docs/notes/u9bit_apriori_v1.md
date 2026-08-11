
# U9-BIT の a priori 代替(裁定 860)— 半分は値なしで決まる・半分は決まらない

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査)
**問い**: 段 A(分岐素点スクリーン)を $u$ の値なしで代替できるか。**前件不成立**(U9-BIT-EXTRACT: $u_9/u_{S4}$ は工房内に無い)を受けての a priori 検討。

---

## §0 答え(4 行)

| 問 | 答 |
|---|---|
| ① $L_9$ 側 | ★★ **決まる。$u_9$ の値は抽出不要** — 9 層は $\mathbf Q(\zeta_9,\sqrt[9]{3})$ に**一意確定**(§1) |
| ② $L_{S4}$ 側 | ✘ **決まらない**。$PB_3/N_{S4}\cong PSL(2,8)$、$\lvert PSL(2,8)\rvert=504=2^3\cdot3^2\cdot7$ ⟹ $S_{S4}\subseteq\{2,3,7\}$ **まで**(§2) |
| ③ 段 A で null 確定? | ✘ **しない**。$S_9\cap S_{S4}\subseteq\{2,3\}\not\subseteq\{3\}$、かつ $L_9\cap L_{S4}$ は非可換でありうるので Kronecker–Weber が効かない(§3) |
| ④ 律速 | ★ **$u_{S4}$ ただ一つ**。しかも「値」ではなく**分岐 1 ビット**に落ちる(§4)。⚠ **そして私の凍結予言の理由づけは逆向きだった**(§5) |

---

## §1 ★★ $L_9$ の 9 層は **$\mathbf Q(\zeta_9,\sqrt[9]{3})$ に一意確定**(抽出不要)

> ### 命題候補 **U9-RIGID**(candidate・本ノート・repo 初出)
> $L$ を $\mathbf Q$ のガロア拡大で $\mathrm{Gal}(L/\mathbf Q)\cong\mathrm{Aff}(\mathbb Z/9)=\mathbb Z/9\rtimes(\mathbb Z/9)^\times$、かつ **$3$ の外で不分岐**とする。すると
> $$\boxed{\ L=\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr)\ \textbf{(一意)}\ }$$
> **証明**(4 段):
> 1. $\mathrm{Aff}(\mathbb Z/9)$ の $(\mathbb Z/9)^\times$ 部が $\mathbb Z/9$ に乗法で作用する ⟹ 円分作用 ⟹ $L\supseteq\mathbf Q(\zeta_9)$ で $\mathbb Z/9$ 層は Kummer、しかも $u\in\mathbf Q^\times$(**$\mathrm{Aff}$ 型 $\iff$ 有理数の冪根拡大**: $\sigma\tau\sigma^{-1}=\tau^a$ の計算)。
> 2. $\ell\ne3$ で不分岐 ⟹ $v_\ell(u)\equiv0\ (\mathrm{mod}\ 9)$ ⟹ $u\equiv\pm3^b$ mod $(\mathbf Q^\times)^9$。
> 3. $-1=(-1)^9$ は **9 乗**ゆえ符号は消える ⟹ $u\equiv3^b$。
> 4. $3\mid b$ なら $\sqrt[9]{3^b}$ は 3 乗根に退化し層が $\mathbb Z/9$ にならない ⟹ $\gcd(b,3)=1$ ⟹ $b$ は $9$ を法として可逆 ⟹ $\mathbf Q(\zeta_9,\sqrt[9]{3^b})=\mathbf Q(\zeta_9,\sqrt[9]{3})$。∎
> **次数照合**: $[\mathbf Q(\zeta_9,\sqrt[9]{3}):\mathbf Q]=6\cdot9=54=\lvert\mathrm{Aff}(\mathbb Z/9)\rvert$ ✔

**$L_9$ への適用**: $\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$(ihnec U-11)の $\mathrm{Aff}$ 因子は**幾何 $\pi_1$ の 3-群商**に対応。$\mathbb P^1_{\mathbb Z}-\{0,1,\infty\}$ は $\mathrm{Spec}\,\mathbb Z$ 上滑らか(3 点は全標数で相異なる)ゆえ、**pro-3 商への Galois 作用は 3 の外で不分岐**(Ihara 型・古典)【要 pin: IHARA-LIT-1】。
$$\boxed{\ \Longrightarrow\ u_9=3\ \textbf{(9 乗類として)。抽出戦役は }L_9\ \textbf{側については}\textbf{不要}\ }$$
⚠ **条件**: 「$\mathrm{Aff}$ 因子が 3 の外で不分岐」は、$\Theta_9$ の $C_2$ 因子(2 での分岐源)が **$\mathrm{Aff}$ 層と分離している**ことを要する。$\Theta_9\cong\mathrm{Aff}\times C_2$ が**直積**である(U-11 の主張形)ならこれは従う ⟹ **U-11 の直積性が本命題の前件**【U9A-GAP-1】。

---

## §2 ✘ $L_{S4}$ 側は縛れない

**命題 ROOF**: $PB_3/M\cong G_9\times PSL(2,8)$ ⟹ $PB_3/N_{S4}\cong PSL(2,8)$。
$$\lvert PSL(2,8)\rvert=504=2^3\cdot3^2\cdot7$$
被覆の位数を割る素数は $\{2,3,7\}$ ⟹ **moduli 体の分岐は $\{2,3,7\}$ の外でない**(位数 $m$ の Belyi 被覆は $m$ の素因子の外で良還元)。
- $PSL(2,8)$ は**単純**ゆえ $C_9$ 商をもたない ⟹ $\mathfrak F_0\cong C_9$ は**窓商の商ではなく** $GT(N_{S4})$ 側の対象(なお $PSL(2,8)$ の Sylow-3 は $C_9$ — $q\pm1=7,9$ より元の位数は $\{1,2,3,7,9\}$)。
- ⟹ $L_{S4}$ の 9 層は $2$ でも $7$ でも分岐しうる ⟹ $u_{S4}\equiv2^a3^b7^c$($(a,b,c)\in(\mathbb Z/9)^3$)。
$$\boxed{\ \Longrightarrow\ \textbf{a priori では }u_{S4}\ \textbf{は }\le9^3\ \textbf{類までしか縛れない。決まらない。}}$$

---

## §3 ✘ 段 A は a priori では閉じない

$S_9\subseteq\{2,3\}$($\Theta_9$ の位数 $108=2^2\cdot3^3$)・$S_{S4}\subseteq\{2,3,7\}$ ⟹
$$S_9\cap S_{S4}\subseteq\{2,3\}\ \not\subseteq\ \{3\}$$
さらに **$L_9\cap L_{S4}$ は非可換でありうる**(共通商が $\mathrm{Aff}$ 型なら非可換)⟹ **Kronecker–Weber は適用できない**($u9bit\_spec\_v1$ 段 A の論法は「abel なら」の暗黙前提を含んでいた ⟹ **仕様の訂正**)。
$$\boxed{\ \Longrightarrow\ \textbf{段 A の a priori 代替は}\textbf{不成立}\textbf{。null は確定しない。}}$$

---

## §4 ★ 律速は $u_{S4}$ ただ一つ — しかも「値」ではなく**分岐 1 ビット**

§1 で $u_9=3$ が確定するので、U9-BIT の述語は**片側だけの問い**になる:
$$\textbf{U9-BIT}\iff \exists a:\ u_{S4}\equiv3^a\ \iff\ \boxed{\ u_{S4}\ \textbf{の台が }\{3\}\ \textbf{に限られる}\ \iff\ L_{S4}\ \textbf{の 9 層が }3\ \textbf{の外で不分岐}\ }$$
⟹ **必要なのは $u_{S4}$ の値ではなく、$L_{S4}$ の 9 層における 2 と 7 の分岐/不分岐の 1 ビット。**

> ### ★ 代替発注案 **U9-RAMIF**(値抽出より軽い)
> $N_{S4}$ 窓の被覆データ(既収)から、**$\mathfrak F_0\cong C_9$ に対応する部分拡大の 2 および 7 での分岐**を判定する。
> - **陰性(2 でも 7 でも不分岐)** ⟹ §1 の一意性で $L_{S4}$ の 9 層も $\mathbf Q(\zeta_9,\sqrt[9]{3})$ ⟹ ★ **U9-BIT は自動的に真** ⟹ $\lvert Q_A\rvert\ge54$ ⟹ $\lvert X\setminus A\rvert\ge864$(**発火**)。
> - **陽性(どちらかで分岐)** ⟹ 9 層は別体 ⟹ U9-BIT 偽 ⟹ $\lvert Q_A\rvert\le18$。
> **律速の所在**: 「$\mathfrak F_0$ の $C_9$ がどの体を切るか」の**同定**は依然必要。これは $u$ の**値**より弱いが**ゼロではない** ⟹ 抽出戦役の 7 前件のうち**経路 B(9 層の同定)だけが残る**。
> ★ **代替不能性の 1 行**(便 116 用): $$\boxed{\ \textbf{$u_9$ は理論で消えたが、$u_{S4}$ は消えない — $N_{S4}$ が dihedral 塔外で }PSL(2,8)\ \textbf{が }7\ \textbf{を含むため、分岐の自由度が残る。}}$$

---

## §5 ⚠ **私の凍結予言の理由づけは逆向きだった**(測定前の自己訂正)

`u9bit_spec_v1.md` §3 で私は予言を **null 側**に置き、理由を「二窓は独立な戦役で選ばれ、共通の非円分分岐を持つ設計上の理由がない」とした。**この理由づけは誤りである。**

> $$\boxed{\ \textbf{正しい構図}: \textbf{問いは「たまたま一致するか」ではなく「}\textbf{食い違う余地があるか}\textbf{」である。}}$$
> §1 の一意性により、**3 のみに台をもつ 9 層は $\mathbf Q(\zeta_9,\sqrt[9]{3})$ しかない** ⟹ 両者がともに 3-のみなら**一致は強制**される。独立性は一致を妨げない。
> ⟹ **予言の向きは、$u_{S4}$ が 2 または 7 で分岐するか否かに完全に依存する**(§4)。「独立だから null」は**根拠にならない**。

> ### 予言の扱い(**IF-FIRST の遵守**)
> **測定は一切行っていない**(前件不成立で段 A/B/C は未走)。本ノートは**紙の議論のみ**による予言の理由づけの訂正である。
> - **P-U9BIT(旧・null 予言)**: ★ **理由づけを撤回**。予言そのものは司令塔裁定に委ねる — **(i) 中立へ戻す**(理由が消えたので予言も外す)か **(ii) §4 の分岐ビットに賭け直す**か。**起草者の推奨は (i) 中立**(a priori の材料が両側にある以上、根拠のない方向づけはしない)。
> - **新設 P-U9RAM(§4)**: 述語 = 「$L_{S4}$ の 9 層は 2 でも 7 でも不分岐」/ 定義域 = $N_{S4}$ 単窓 / 陽含意 = **U9-BIT 真・発火 $\ge864$** / 陰含意 = U9-BIT 偽・$\lvert Q_A\rvert\le18$。**予言は置かない(真の UNKNOWN)** — 今度は**根拠がないことが根拠**(a priori に $2,7$ の分岐を決める材料が積荷にない)。

---

## §6 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| ★ **【U9A-GAP-1】** | U9-RIGID の $L_9$ への適用は **$\Theta_9\cong\mathrm{Aff}\times C_2$ の直積性**(U-11)と、$\mathrm{Aff}$ 因子が幾何 $\pi_1$ の 3-群商に対応することを要する | ★ 中 |
| ★ **【IHARA-LIT-1】**(文献要請) | 「$\mathbb P^1-\{0,1,\infty\}$ の pro-$\ell$ 商への $G_\mathbf Q$ 作用は $\ell$ の外で不分岐」の**正確な形と条件**(Ihara/Deligne 系)【要 pin】 | ★ 中 |
| ★ **【U9A-GAP-2】** | $\mathfrak F_0\cong C_9$ が**どの体を切るか**の同定は未了 — §4 の分岐ビットもこれに依存 | ★ 中 |
| **【U9A-GAP-3】** | 仕様 `u9bit_spec_v1` 段 A の Kronecker–Weber 論法は**abel 前提**を暗黙に含んでいた ⟹ 訂正済(§3) | 小(訂正済) |

**帰属**: 問い(a priori 代替の可否・pro-3 分岐制約の示唆)= 司令塔(裁定 860)。$\Theta_9$・命題 ROOF・$\mathfrak F_0$ = ihnec 戦役。抽出計画の前件 7 項 = `u9_extraction_plan_v1.md`。
**本ノートの新規部分** = ★ **命題候補 U9-RIGID($\mathrm{Aff}(\mathbb Z/9)$ ∧ 3-外不分岐 ⟹ $\mathbf Q(\zeta_9,\sqrt[9]{3})$ 一意)** / **$u_9$ が抽出不要になること** / **$L_{S4}$ 側が $PSL(2,8)$ の 7 のために縛れないことの同定** / **段 A の abel 前提の摘発と訂正** / **律速を「値」から「分岐 1 ビット」へ落とす U9-RAMIF** / ★ **凍結予言の理由づけの自己訂正(「たまたま一致」ではなく「食い違う余地」が問い)**。

**novelty grep**: `U9-RIGID` `U9-RAMIF` `P-U9RAM` `IHARA-LIT-1` = **0 hit(本ノート初出)**。

**検算**:
```bash
python -c "
from sympy import factorint, totient
print('|PSL(2,8)| =',factorint(504),' -> S_S4 subset {2,3,7}')
print('|Aff(Z/9)| = 9*phi(9) =',9*totient(9),' = [Q(z9,3^(1/9)):Q] = 6*9 =',54)
print('b with gcd(b,3)=1:',[b for b in range(1,9) if b%3],'-> 全て 9 を法として可逆 -> 体は一意')
print('3|b:',[b for b in range(1,9) if b%3==0],'-> 3乗根へ退化 -> C_9 が立たない')
"
```
