# XD-2 検分 — 定理候補 **TWIST-6-ABS** の裁定(裁定 811)

**日付**: 2026-08-11 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・判定語の発効は司令塔専権)
**入力**: `docs/notes/ideas_chi_door_assault_v1.md`(c5a02ae・札 XD-2)/ 裁定 811
**先行**: 定理 TWIST-6(`ribet_dig_campaign_v1.md` §2.1)・補題 TWIST-GCD / 命題 AB-CYC / 命題 AB-2J

---

## §0 裁定(1 行)

> $$\boxed{\ \textbf{XD-2 は}\textbf{成立する}\textbf{。しかも発案係の前提 2 点(}B_3'\cong F_2\ \textbf{・}x^2-x+1\textbf{)はどちらも}\textbf{不要}\textbf{で、証明は 4 行。穴(Schur 乗数)は}\textbf{発生しない}\textbf{。}}$$

さらに**強い形**が出る:
$$\boxed{\ \mathrm{ord}(\chi_W)\ \bigm|\ \gcd\bigl(e,\ 6,\ p-1\bigr)\qquad(e=\lvert G^{\rm ab}\rvert)\ }$$

---

## §1 ★★★ 定理候補 **TWIST-6-ABS**(証明)

> ### 定理候補 TWIST-6-ABS(candidate・本検分)
> $N\trianglelefteq B_3$ 任意($c\in N$ を仮定しない・有限性も不要)、$G=B_3/N$。$W$ を $G$ の**切片**($W=A/B$、$B\trianglelefteq A\trianglelefteq G$)で 1 次元 $\mathbf F_p$-加群とし、$\chi_W:G\to\mathrm{Aut}(W)=\mathbf F_p^\times$ を共役による捻れ指標とする。すると
> $$\mathrm{ord}(\chi_W)\ \bigm|\ \gcd(e,6,p-1),\qquad\textbf{とくに}\quad \mathrm{ord}(\chi_W)\mid6.$$

**証明**(4 行)
1. $\chi_W$ の標的 $\mathbf F_p^\times$ は可換 ⟹ $\ker\chi_W\supseteq[G,G]$ ⟹ $\chi_W$ は $G^{\rm ab}$ を経由。**AB-CYC** より $G^{\rm ab}=\mathbf Z/e$ で、生成元は $\bar\sigma_1$。
2. $c=(\sigma_1\sigma_2)^3=\Delta^2$ は $B_3$ の**中心**を生成する。その像 $z\in G$ は $G$ の中心元 ⟹ $z$ は $G$ の**あらゆる切片に共役で自明に作用**する ⟹ $\chi_W(z)=1$。
3. $B_3^{\rm ab}=\mathbf Z$ で $c\mapsto6$、$\sigma_1\mapsto1$ ⟹ $G^{\rm ab}$ において $\bar z=6\bar\sigma_1$。よって $\chi_W$ は $G^{\rm ab}/\langle\bar z\rangle=(\mathbf Z/e)/\langle6\rangle=\mathbf Z/\gcd(e,6)$ を経由。
4. ゆえに $\mathrm{ord}(\chi_W)\mid\gcd(e,6)$。さらに像は $\mathbf F_p^\times\cong C_{p-1}$ の中 ⟹ $\mathrm{ord}(\chi_W)\mid\gcd(e,6,p-1)$。∎

**使った事実は 3 つだけ**: ① $Z(B_3)=\langle c\rangle$ ② $c\mapsto6\in B_3^{\rm ab}=\mathbf Z$ ③ $\chi_W$ の標的が可換。

## §2 発案係の骨子との対照 — **前提 2 点は不要・穴は消滅**

| 発案係の骨子 | 本検分 |
|---|---|
| $\chi_W\ne1\Rightarrow W\subseteq B_3'$-像 | ★ **正しいが不要**。§1 は $W$ の位置を一切使わない |
| $B_3'\cong F_2$(Gorin–Lin) | ★ **不要**。自由性は使わない |
| $\det(M-1)=p_M(1)=1$・六角 $x^2-x+1$・$\bar\sigma$ 固有値は $\zeta_6$ 冪 | ★ **不要**(Alexander 加群経由の別証にはなる — §2.1)。中心元 1 個で足りる |
| ★ **穴**: 完全根基の Schur 乗数経由($691\mid$ 乗数は $n\ge691$ の PSL 型) | ★ **発生しない**。§1 は乗数・完全根基・合成列の位置を通らない。$G$ が完全なら $e=1$ ⟹ $\chi_W=1$ で即座に閉じる |

### 2.1 骨子の路線も**正しい**(独立な第二証明・整合確認)

$B_3\cong F_2\rtimes_\varphi\mathbf Z$($F_2=B_3'$)。$\varphi$ の $F_2^{\rm ab}=\mathbf Z^2$ 上の行列は特性多項式 $\Phi_6(x)=x^2-x+1$(三葉結び目の Alexander 多項式)⟹ 固有値は原始 6 乗根 $\zeta,\zeta^{-1}$。$\mathrm{gr}_n(F_2)=\mathrm{Lie}_n(V)$ 上の固有値は $\zeta^{a-b}\ (a+b=n)$ ⟹ **全て 6 乗根**。
⟹ 下中心列に沿う因子では位数 $\mid6$。**ただしこの路線は「chief factor が LCS の因子とは限らない」ギャップを残す** — §1 はそれを迂回する。
★ **等価な言い換え**: $B_3\supseteq B_3'\times Z(B_3)\cong F_2\times\mathbf Z$ が**指数 6** ⟹ $\varphi^6$ は $F_2$ の内部自己同型 ⟹ $\mathrm{Out}$ での位数 6。§1 の中心元論法はこの事実の最短形。

---

## §3 ★★★ 帰結 1 — **扉 (B) も閉じる。私の P-CHI-M5 §3(B) は保守的すぎた(自己訂正)**

`card_pchi_m5_v1.md` §3 で私は三読みを分け、**(B) 外部標数 $p\equiv1\bmod5$ では位数 5 の指標が実在するので扉は開いたまま**と書いた。**これは撤回する。**

$M_5$: $e=10$ ⟹ $\gcd(10,6)=2$ ⟹
$$\boxed{\ \mathrm{ord}(\chi_W)\mid2\quad\textbf{が}\textbf{全ての標数 }p\ \textbf{で成立}\ (p\mid\lvert G\rvert\ \textbf{を仮定しない})}$$
⟹ **(A) だけでなく (B) も閉鎖**。$p=11,31,41,\dots$ の抜け道は $z$ の中心性で塞がれる(私は $\chi_W$ が**切片**の共役作用であることを使い切っていなかった)。

| 読み | 旧(カード §3) | ★ 新(本検分) |
|---|---|---|
| (A) $G$ の chief factor($p\mid\lvert G\rvert$) | 閉(定理・$p\in\{2,3,5\}$ 経由) | 閉(**より強い定理**・$p$ 不問) |
| (B) 外部標数の切片 | **開** | ★ **閉** |
| (C) $\dim\ge2$ 因子 | 開 | **開**(§4) |
| (D) 切片でない抽象 $\mathbf F_p[G]$-加群 | — | ★ **射程外**(§5 の限定) |

**P-CHI-M5 の凍結値は変えない**($\mathrm{ord}\mid2$)。**射程だけが広がる**(全標数)。カード §3 の表は本検分で差し替え。

### 3.1 ★ 独立裏取り — Q₈⋊C₃ₘ 族で二つの論法が一致

追補 A §2.2 では**構造的論法**(「$C_m$ は直積因子ゆえどの合成因子にも作用しない ⟹ $\mathrm{ord}\mid3$」)で族の捻れを押さえた。§1 の**中心元論法**は $e=3m$ から
$$\gcd(15,6)=3,\quad\gcd(21,6)=3,\quad\gcd(27,6)=3,\quad\gcd(45,6)=3$$
⟹ **$\mathrm{ord}\mid3$**。**まったく別経路で同一の値** ⟹ 追補 A §2.2 の結論は二重に立つ(cross-check ではなく二系統の紙証明の一致)。同様に $e=10$ ⟹ $\gcd=2$、完全群 $e=1$ ⟹ $\gcd=1$(自明)で全て整合。

---

## §4 ★★★ 帰結 2 — 司令塔の二択が**定理になる**

$W$ が $\dim d\ge2$ の chief factor のとき、$\det\circ\rho_W:G\to\mathbf F_p^\times$ は可換標的 ⟹ §1 がそのまま適用:
$$\boxed{\ \mathrm{ord}(\det\rho_W)\ \bigm|\ \gcd(e,6,p-1)\ }$$

> ### ★ 系 **CHI-DICHOTOMY**(candidate・本検分)
> $B_3$ 商の切片に位数 $r>6$ の捻れ情報が入る道は**次の 1 つだけ**:
> $$\boxed{\ \textbf{非可換な }\dim\ge2\ \textbf{因子の中の固有指標対 }\{\chi,\chi^{-1}\}\ (\det=\chi\cdot\chi^{-1}=1\ \textbf{ゆえ }\S1\ \textbf{の束縛を回避})\ }$$
> **det 経由(1 次元核・可換像)の道は位数 6 で絶対閉鎖。**

**Ribet 型への適用**: Ribet の $\rho$ は**可約**(合成因子が 1 次元・指標 $\{1,\omega^{k-1}\}$)⟹ §1 より両捻れの位数 $\mid6$ ⟹ $\chi^{11}$(位数 690)は **どんな $B_3$ 商の切片にも 1 次元因子として現れない**($c\in N$ 不要・$e$ 不問・窓か否かも不問)。
⟹ ★ **TWIST-6 の「窓限定」という限定が外れ、RIBET-WINDOW の不成立が $B_3$ 商**全体**の定理になる。**

**残る唯一の道の必要条件**: $\{\chi,\chi^{-1}\}$ が位数 690 ⟹ $\chi\in\mathbf F_{p^2}^\times$ で $\chi^p=\chi^{-1}$ も許される ⟹
$$\boxed{\ p\equiv\pm1\ \ (\mathrm{mod}\ 690)\ }$$
($+1$ 側の最小素数 $=691$・追補済/$-1$ 側は $689=13\cdot53$、$1379=7\cdot197$、$2069$ を順に検定 — §6 の検算コマンド)。**梯子 $G_p$ はまさにこの「非可換 2 次元」型**であり、$B_3$ 商での χ の唯一の生息可能地が定理で 1 本に絞られた。

---

## §5 ⚠ 射程の限定(過大禁止・3 点)

1. **$W$ は $G$ の切片であること**が本質(中心元 $z$ が自明に作用するのは共役作用だから)。$G$ の**抽象表現**の合成因子には適用**されない** — 例: $G\twoheadrightarrow C_e\hookrightarrow\mathbf F_p^\times$ という抽象指標は位数 $e$ を持てる。**「窓が χ を運ぶ」の意味を切片に固定する**必要がある(この限定を編纂に明記)。
2. **$\dim\ge2$ は閉じていない**(§4)。閉じたのは **1 次元因子と det 成分**。
3. **$\mathrm{Out}$ 位数 6 の事実**(§2.1)は $B_3$ 固有。$B_4$ への移送は別途($Z(B_4)=\langle\Delta_4^2\rangle$・$\Delta_4^2\mapsto12$ in $B_4^{\rm ab}=\mathbf Z$ ⟹ 同じ論法で **$\mathrm{ord}\mid\gcd(e,12,p-1)$** が出るはず — **TWIST-12 の別証**・要検分)。

---

## §6 発効文案・【GAP】・帰属

> ### 正札案(発効は司令塔専権)
> **TWIST-6-ABS**: 「$B_3$ の任意の商の任意の切片について、1 次元捻れ指標の位数は $\gcd(e,6,p-1)$ を割る。ゆえに **6 を超える捻れは 1 次元では原理的に入らない**。」
> **CHI-DICHOTOMY**: 「$B_3$ 商における位数 $>6$ の捻れの唯一の入口は、非可換 $\dim\ge2$ 因子内の $\{\chi,\chi^{-1}\}$ 対($\det=1$)であり、その必要条件は $p\equiv\pm1\pmod r$。」

| # | 内容 | 重さ |
|---|---|---|
| **【XD2-GAP-1】** | $B_4$ 版($\gcd(e,12,p-1)$)は未検分 — TWIST-12 との突合が要る | 小 |
| **【XD2-GAP-2】** | §5(1) の「切片 vs 抽象表現」の分離が、既存の TWIST-6 系全ての主張で一貫しているかの棚卸し未了(**CV-9 型の仕様同一性** ⟹ falsifier 判読推奨) | ★ 中 |
| **【XD2-GAP-3】** | §4 の $p\equiv\pm1\ (690)$ は必要条件。十分性(実際に窓が作れるか)は未検分 — XD 札の Burau 窓 $W_{691}$ 系が扱う領域 | 中 |

**帰属**: 札 XD-2 の発案・骨子・穴の正直な併記 = **発案係**(c5a02ae)。検分委嘱 = 司令塔(裁定 811)。
本検分の新規部分 = **中心元による 4 行証明(前提 2 点の不要性)** / **強形 $\gcd(e,6,p-1)$** / **扉 (B) の閉鎖と自己訂正(カード §3)** / **系 CHI-DICHOTOMY(司令塔の二択の定理化)** / **RIBET-WINDOW 不成立の $B_3$ 商全体への拡張** / **$p\equiv\pm1\ (690)$ の必要条件** / **$B_4$ 版の予想 $\gcd(e,12,p-1)$** / **§5 の射程限定 3 点**。

**novelty grep**(`docs/` `provenance/`): `TWIST-6-ABS` は発案札 c5a02ae 既在(**本検分は証明**)。`CHI-DICHOTOMY` `gcd(e,6,p-1)` `p ≡ ±1 (mod 690)` = **0 hit(本検分初出)**。

**検算コマンド**(裁定 668 拡張):
```bash
python -c "
from sympy import isprime
from math import gcd
# TWIST-6-ABS の数値形: ord | gcd(e,6,p-1)
for e,name in [(10,'M5'),(6,'window c in N'),(2,'window'),(15,'Q8:C15'),(45,'Q8:C45'),(690,'dream')]:
    print('%-16s e=%-4d gcd(e,6)=%d'%(name,e,gcd(e,6)))
print()
print('p = +-1 mod 690 の最小素数:')
print(' +1:',[x for x in (690*k+1 for k in range(1,6)) if isprime(x)][:2])
print(' -1:',[x for x in (690*k-1 for k in range(1,8)) if isprime(x)][:2])
"
# 期待: M5 -> gcd=2 / window -> 2 or 6 / Q8:C15 -> 3 / Q8:C45 -> 3 / dream(690) -> 6
```
