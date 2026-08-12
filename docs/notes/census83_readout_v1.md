# 83 窓 census 読解(裁定 999)— 半率の正体は settled 性・15 窓中 13 窓が非 isolated

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 999
入力 = cert `search/certs/iso_census83_deep15_v1_20260812.json`(生値)+ 述語定義(`iso_census83_deep15_v1.g` :86-92 逐語・裁定 999 で配達)
⚠ 型境界: 83 窓($c\notin N$)限定。$K^{(9)}$ 窓への外挿は §5 の警告を読むこと(W-48)。
⚠ 数値出力なし($u$-touched = false)。**格付け: candidate**(§4 の機構は未証明・Sol 未監査)。

---

## §0 結論(3 行)

1. ★★★ **半率は「核が非自明」ではない** — 半分は `well_defined=False`(`kernel_size=fail` のまま `kernel_trivial=False` に計上)。全 15 窓+witness+control で**例外 0 件**(機械確認)。
2. ★★★ **述語の正体は settled 性**。正典 L173 逐語「**settled**: $\ker(T_{m,f})=N$」に照らすと `well_defined ∧ kernel_trivial` ⟺ **settled($PB_3$ 版)**。⟹ **`all_kernel_trivial` は isolated 判定**。
3. ★★★ ⟹ **15 窓中 13 窓が非 isolated** ⟹ **$GT(N)$ が群にならない** ⟹ **$\rho_N$(群準同型)が存在しない**(2405 Remark 1.4 の型境界)⟹ **χ 扉の算術比較の土俵に乗るのは 1152 系の 2 窓だけ**。

---

## §1 述語の意味論(定義から)

```gap
psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u, f^-1 * W.y^u * f]);
```
- 始域も終域も `W.PN` $=PB_3/N$ ⟹ ★ **これは「$T_{m,f}$ が $PB_3/N$ の自己準同型に**降りる**か」の検査**。
- $T(x)=T(\sigma_1^2)=\sigma_1^{2u}=x^u$ ✔、$T(y)=T(\sigma_2^2)=(f^{-1}\sigma_2^uf)^2=f^{-1}y^uf$ ✔ ⟹ 確かに $T_{m,f}|_{PB_3}$。

$$\boxed{\ \texttt{well\_defined}\iff N\cap PB_3\subseteq\ker T_{m,f}\quad(\textbf{降下}) }$$
$$\boxed{\ \texttt{kernel\_trivial}\iff \ker T_{m,f}\cap PB_3=N\cap PB_3\quad(\textbf{核が}\ N\ \textbf{ちょうど}) }$$

⚠ **重要**: 降下は hexagon (3.3)(3.4) の帰結では**ありません**。Prop 3.2 が言うのは「$T_{m,f}:B_3\to B_3/N$ が well-defined」であって、**$B_3/N\to B_3/N$ に降りる**($T(N)\subseteq N$)ことは別条件です。⟹ **`well_defined=False` は「hexagon を満たさない」を意味しない** — 列挙器のバグではありません。

## §2 ★★★ 正典との接続 — これは settled 判定

定義ノート L173 **逐語**:
> **settled**: $\ker(T_{m,f})=N$。**isolated**: 全 shadow が settled ⇒ $GT(N)=GTSh(N,N)$ は**有限群**。

$$\boxed{\ \texttt{well\_defined}\wedge\texttt{kernel\_trivial}\iff \ker T_{m,f}\cap PB_3=N\cap PB_3\iff \textbf{settled}\ (PB_3\ \textbf{版})\ }$$

⟹ ★ `all_kernel_trivial = True` ⟺ **列挙された全 shadow が settled** ⟺ **isolated**($PB_3$ 版・列挙が完全なら)。

| 窓 | shadow | settled | 率 | `all_kernel_trivial` | ⟹ isolated? |
|---|---|---|---|---|---|
| control $K^{(3)}$($c\in N$) | 12 | 12 | 1 | True | ★ isolated ✔(既知) |
| control S4($c\in N$) | 54 | 54 | 1 | True | ★ isolated ✔(既知) |
| **[1152,154161] / [154163]** | 48 | 48 | **1** | **True** | ★★ **isolated 候補** |
| [1008,521] / [683] | 48 / 72 | 24 / 36 | 1/2 | False | ✘ **非 isolated** |
| [1134,55] / [53] | 12 / 36 | 6 / 18 | 1/2 | False | ✘ **非 isolated** |
| [1872,568] / [780] | 96 / 144 | 48 / 72 | 1/2 | False | ✘ **非 isolated** |
| witness 1728/31095 | 8 | 4 | 1/2 | False | ✘ **非 isolated** |

★ **positive control 2 本が 100% でこれを裏付け**(どちらも $c\in N$・既知の isolated 窓)⟹ 述語の意味論の較正が取れています。

---

## §3 ★ 法則 — settled ⟺ $u\equiv1\ (\mathrm{mod}\ 3)$

7 系統すべてで**完全一致・例外 0**(機械確認):

| 窓 | $z$ | der | der の奇部分 | settled な $u$ | 非 settled な $u$ |
|---|---|---|---|---|---|
| [1008,521] | 2 | 14 | **7** | 1, 7, 13, 19 | 5, 11, 17, 23 |
| [1008,683] | 2 | 56 | **7** | 1, 7 | 5, 11 |
| [1134,55] | 3 | 7 | **7** | 1 | 5 |
| [1134,53] | 3 | 7 | **7** | 1, 7, 13 | 5, 11, 17 |
| [1872,568] | 2 | 26 | **13** | 1, 7, 13, 19 | 5, 11, 17, 23 |
| [1872,780] | 2 | 104 | **13** | 1, 7 | 5, 11 |
| **[1152,·]** | 2, 4 | **64** | **1** | **全部** | (なし) |

$$\boxed{\ \textbf{settled}\iff u\equiv1\ (\mathrm{mod}\ 3)\qquad\text{ただし der が 2 群の 1152 系では}\textbf{恒真}\ }$$

⚠ $z$($=\mathrm{ord}(cN)$)では**説明できません**($z=2$ の窓と $z=3$ の窓が同じ法則に従う)。$u$ の奇偶でも $u\bmod7$ でもありません(1008 では $u=5$ が両側に現れる)。⟹ **法則は $u\bmod3$ で確定**。

---

## §4 機構の候補(★ candidate 格・未証明)

**(a) なぜ 3 か**: $c=\delta^3$($\delta=\sigma_1\sigma_2$)、$\tilde\tau=\mathrm{Ad}(\delta)$ は $A=PB_3/N$ 上で**位数 3**。降下の破れは $c$ 絡みの関係式で起きるはず。

**(b) アーベル層には障害がない**(証明済): $T$ は $(PB_3/N)^{ab}$ 上で $u$ 倍。$c\equiv W_c(x,y)\ (\mathrm{mod}\ N)$ と書くと $\mathrm{ab}(T(W_c))=u\,\mathrm{ab}(W_c)=\mathrm{ab}(c^u)$ ⟹ **一致** ⟹ 障害は**導来部分群に住む** ✔ 1152 系の例外性と整合。

**(c) $\omega$ 退化の候補**: $7\equiv13\equiv1\ (\mathrm{mod}\ 3)$ ⟹ $\mathbf F_7^\times,\mathbf F_{13}^\times$ は原始 3 乗根 $\omega$ を含む ⟹ $C_7,C_{13}$ は位数 3 の自己同型($\omega$ 倍)を許す。その成分で $\tilde\tau$ のノルム $1+\omega+\omega^2=0$ が退化し、$T$ が $\omega$-固有成分と可換になる条件が $u\equiv1\ (\mathrm{mod}\ 3)$ になる、という筋。
⟹ **1152 系は der が 2 群 ⟹ 3 が可逆 ⟹ $\omega$-成分がない ⟹ 恒真** ✔ 整合。

⚠⚠ **(c) は証明していません。** W-50(census 後付けの罰)の再発を避けるため、**格付けは candidate に留めます**。以下の測定で決着します。

### ★ 決定的な測定 3 本(いずれも秒級)
```
[C1] well_defined=False の 1 例で、PB_3/N の *どの関係式* が壊れるかを 1 本特定せよ。
     (GroupHomomorphismByImages の代わりに presentation の各関係語へ代入し、
      像が単位元にならないものを出す)。出力: 関係語と、その像の位数。
[C2] その像が (PB_3/N)' のどこに落ちるか(位数・Sylow 成分)。
     ★ 予言: 奇部分(7 or 13)の成分に落ちる。落ちなければ (c) は棄却。
[C3] ★ x, y が PB_3/N を生成するか(|<x,y>| = pn_order か)を全窓で確認。
     ⚠ 生成しなければ GroupHomomorphismByImages の fail は *生成不足由来* になり
        全 u で fail するはずだが、実測は u で割れている ⟹ 生成しているはず。
        この 1 行で「fail が数学的障害である」ことが確定する(fail-closed)。
```

---

## §5 ⚠⚠ χ 扉への直結(司令塔の指摘への回答)

$$\boxed{\ \textbf{非 isolated }\Longrightarrow\ GT(N)\ \textbf{は群でない}\ \Longrightarrow\ \rho_N\ \textbf{(群準同型)は存在せず、集合写像 }a_N\ \textbf{のみ}\ }$$
(= **2405 Remark 1.4 の型境界** = TYPE-IMAGE$^\rho$ の 5 対象が定義できる条件)

⟹ ★★ **算術比較(marked target / $\rho_N$ / 像 $A_N$ / 核体 $L_N$ / 局所分岐)の土俵に乗るのは、この 15 窓では 1152 系の 2 窓だけ**です。他の 13 窓で $\rho_N$ を書いたら**型境界エラー**になります。

⚠ **$K^{(9)}$ への外挿は禁止**(W-48)。$K^{(n)}$ は **Thm 4.3 で isolated と確定済**(定義ノート L189)なので $K^{(9)}$ 側は安全ですが、**それは 83 窓の性質とは無関係**です。83 窓の非 isolated 性から $K^{(9)}$ について何かを言うことはできません。

★ **設計への提案**: 83 窓で $\rho$ 層の実験をするなら **1152 系 2 窓を primary に**。他の 13 窓は「$a_N$(集合写像)までしか作れない窓」として別枠に記帳すべきです。

---

## §6 GAP / 記帳

- **【C83-GAP-1】(中)** settled の正典定義は $\ker(T_{m,f})=N$ で、$T_{m,f}$ は $B_3\to B_3/N$。census が測っているのは **$PB_3$ 版**。★ 全射性については Prop 3.6 が「$T_{m,f},T^{PB_3},T^{F_2}$ で同値」と言うが、**核についての同種の主張が正典にあるかを私は未確認** ⟹ **$PB_3$ 版 = $B_3$ 版**が要証明。⟹ §2 の同値と §5 の帰結は**この GAP に条件つき**。
- **【C83-GAP-2】(小)** 「列挙が完全」が isolated 判定の前提。(F2) 商規律の列挙の完全性は別途の保証が要る。
- **記帳(自己)**: 前回の中間報告で私は半率を「核の非自明性」の枠で読み始めた。実際は `well_defined` 層だった。★ **述語の運用定義を読む前に機構を語らない**という規律(W-50)が今回は正しく効き、格付けを保留したまま定義を要求できた ⟹ **手戻りゼロ**。
- **申告**: GAP 走行ゼロ(cert の生値のみ使用)・$u$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
