# 【BSY-GAP-1】決定実験 — **辞書は無罪。かつ「正解基準」自体が偽だった**(裁定 645 ①)

**状態札: `measured / candidate / 原因②は棄却・新原因④を発見 / 窓ゼロ・GAP ゼロ・封印非接触 / 機械 = 分数演算 2 本(scratchpad/decisive2.py, tau_inhom.py)`**

- 実行: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 裁定 645 ①「pr 不使用・$\theta_{\exp F}$ を群交換子から直接計算する第二実装で $h(v_1),h(v_2),h(v_3)$ を独立導出。②辞書誤りなら値が変わる / ③層対応なら不変」

---

## 0. 結論(4 行)

> 1. ★ **辞書は無罪** — 完全独立ルート(Fox 微分)で $h(u)=1,\ h(u_1)=-\xi,\ h(u_2)=-\eta,\ h(v_1)=\xi^2,\ h(v_2)=\xi\eta,\ h(v_3)=\eta^2$ を **6/6 再現**。線型性も別サンプルで確認。⟹ **原因②(辞書誤り)は棄却。**
> 2. 委嘱の判別基準に従えば「値が変わらない ⟹ ③」だが、**実験は同時に第 3 の事実を出した**。
> 3. ★★ **本ノートの「正解基準 $F_4=0$」が偽だった** — 深さ 4 の hexagon (3.11) は $F_3\ne0$ のとき**真に非斉次**である($\tau$ が非斉次写像であるため)。機械確認: $F_3=a\mathfrak h_3$($a\ne0$)に対し $F_4=0$ でも $F_4=a(1,4,1)$ でも次数 4 の残差が**非零で、しかも同一**(= $\mathrm{span}(1,4,1)$ が斉次核であることの確認)。
> 4. ★ **残った不整合は $\tau$ の非斉次版の実装/規約に局在**した(§3)— **E-DIM の結果には一切波及しない**(あちらは純粋に斉次・較正 4/4)。
>
> $$\boxed{\ \textbf{原因②棄却・原因④(斉次性の誤仮定)発見・GAP は }\tau\ \textbf{の非斉次版へ縮小。}\ }$$

---

## 1. 実験 1 — 独立ルートによる辞書の再導出(**pr 側の Lie 論を一切使わない**)

**方法**(`scratchpad/decisive2.py`):
- Magnus 埋め込み $F_2\hookrightarrow\hat{\mathbb Z}\langle\langle X,Y\rangle\rangle$、$x\mapsto1+X$。
- 古典恒等式 $\mathrm{Magnus}(w)-1=\mu(\partial w/\partial x)\!\cdot\!X+\mu(\partial w/\partial y)\!\cdot\!Y$(**最後の文字による右分解**・一意)。これで**級数**に対しても Fox 微分が取れる — $\exp(F)$ を扱える唯一の形。
- 変数を可換化($X\to\xi,\ Y\to\eta$)すると $\mathrm{pr}(\partial w/\partial x)$ が得られる。
- $F'/F''$ は $\theta'=(x,y)$ 上階数 1 自由、$\mathrm{pr}(\partial\theta'/\partial x)=-\eta$、$\mathrm{pr}(\partial\theta'/\partial y)=\xi$ ⟹
  $$\mathrm{pr}(h(w))=\frac{\mathrm{pr}(\partial w/\partial x)}{-\eta}=\frac{\mathrm{pr}(\partial w/\partial y)}{\xi}\qquad(\textbf{2 経路を毎回突合}).$$
- **ad$(x)\leftrightarrow\underline x-1$ も加群論も使っていない。**

**結果**:

| 入力 | $\mathrm{pr}(h)$(実測) |
|---|---|
| 群語 $\theta'=[x,y]$ | $1$ |
| 群語 $[[x,y],x]$ / $[[x,y],y]$ | $-\xi$ / $-\eta$ |
| 群語 $[[[x,y],x],x]$ / $[[[x,y],x],y]$ / $[[[x,y],y],y]$ | $\xi^2$ / $\xi\eta$ / $\eta^2$ |
| ★ **$\exp$ 分裂**: $\exp(u),\exp(u_1),\exp(u_2),\exp(v_1),\exp(v_2),\exp(v_3)$ | $1,\ -\xi,\ -\eta,\ \xi^2,\ \xi\eta,\ \eta^2$ |

$$\boxed{\ \textbf{naive-dictionary match : 6/6 True。線型性 }F\mapsto\mathrm{pr}(h(\exp F))\ \textbf{も混合サンプルで True。}\ }$$

> ★ **群語版と $\exp$ 分裂版が一致した**ことが重要。私が §2.4 で疑った「分裂の取り違え」は**存在しなかった**(群交換子べきと $\exp$ が、この量に関しては同じ値を与える)。**原因②は棄却。**

**ACDIK との連立**(同スクリプト): $\mathrm{pr}(h)=0+\tfrac{k}{2}(\xi+\eta)-\tfrac{k}{2}(\xi^2+\xi\eta+\eta^2)$($k=\kappa^*_3$)を解くと
$$c_2=0,\quad a=b=-\tfrac k2,\quad (\alpha,\beta,\gamma)=-\tfrac k2(1,1,1)\qquad(\textbf{rank 6・consistent}).$$
すなわち **$F_4=a\,(1,1,1)$** — §2.4 と同一の値が、独立実装で再現された。

---

## 2. 実験 2 — ★ 「正解基準 $F_4=0$」の反証

深さ 4 の判定は「$F_4$ が斉次条件を満たすか」だと**暗に仮定していた**。$\theta$($x\!\leftrightarrow\!y$)は Magnus 上でも次数保存だが、$\tau$($x\mapsto y,\ y\mapsto z=(xy)^{-1}$)は
$$Y\ \longmapsto\ \bigl((1+X)(1+Y)\bigr)^{-1}-1=-(X+Y)+\cdots$$
で**次数保存でない**。ゆえに $F_3\ne0$ なら深さ 4 の (3.11) は**非斉次**になる。

**機械確認**(`scratchpad/tau_inhom.py`・$a=1$):

| $F_4$ | (3.10) の次数 $\le4$ 残差 | (3.11) の次数 4 残差 |
|---|---|---|
| $0$ | **ZERO** | ★ **非零** |
| $a(1,4,1)$ | **ZERO** | ★ **非零で、$F_4=0$ と同一** |
| $a(1,1,1)$ | **ZERO** | 非零(別の値) |
| $-a(1,1,1)$ | **ZERO** | 非零(別の値) |

> - $F_4=0$ と $a(1,4,1)$ の残差が**同一** ⟹ $\mathrm{span}(1,4,1)$ が確かに**斉次核**(D4-POWER (a) の再確認)。
> - しかしどちらも残差**非零** ⟹ $$\boxed{\ \textbf{「}F_4=0\ \textbf{が正解」は偽。真の解は非斉次系の特殊解 }+\ \mathrm{span}(1,4,1)\ \textbf{である。}\ }$$
> - $(3.10)$ は 4 例すべてで ZERO ⟹ $\theta$ 側は斉次で正しく、$\alpha=\gamma$ だけが効いている。
>
> ★ **これが原因④である**: §2.4 も本委嘱も「深さ 4 は斉次」を前提にしていた。**前提が偽だった。**

---

## 3. 残った不整合(**縮小したが未閉**)

同スクリプトで非斉次系 $F_4=(\alpha,\beta,\gamma)$ を解こうとすると、$a\ne0$ で **`solvable: False`(rank 1)** が出る。
**これは正しくありえない** — $\mathfrak h_3=\sigma_3$ 方向は GT 元へ持ち上がる(古典)。ゆえに:

> ### 【BSY-GAP-1′】(更新後の唯一の未閉点)
> **非斉次版 $\tau$ の実装/規約に残留誤りがある。** 候補: (i) (3.11) の因子順($f(z,x)f(y,z)f(x,y)$ か逆順か)(ii) $z$ の取り方($z=(xy)^{-1}$ か $(yx)^{-1}$ か)(iii) 群語としての $f$ と Lie 元 $\exp(F)$ の代入規約(**罠 D-6 族**)。
> **判別実験(提案・未実行)**: $\lvert H_W\rvert=42$ の $m\equiv0$ 層 7 元のうち 1 元の $\mathrm{gr}_4$ 座標を実測し、$a(1,1,1)$ と突合する(既在の窓データ・封印外)。一致すれば ACDIK 側は正しく、残りは (i)–(iii) の 3 択に確定する。

---

## 4. ★ E-DIM への非波及(**明記**)

本 GAP は**深さ 4 の非斉次項**に関する話であり、E-DIM5/6 が測った $\dim\mathcal S_k$ は
$$\textbf{非斉次系の解集合 = (特殊解) + (斉次解空間)}$$
の**後者の次元**である。層ごとの解の個数は $p^{\dim\mathcal S_k}$ か $0$ のいずれかで、**$\dim\mathcal S_k$ の値も較正 4 項も本 GAP に一切依存しない**(較正の $\dim\mathcal S_3=1,\dim\mathcal S_4=0$ は斉次量として D3-BLIND / D4-POWER と一致済)。
⟹ **裁定 645 ② の k=7,8 延長は本 GAP と独立に進めてよい。**

---

## 5. 原因表の更新

| # | 候補 | 状態 |
|---|---|---|
| ~~①~~ | ACDIK 転記の不完全 | 棄却(400dpi pin) |
| ~~①′~~ | 偶数 Bernoulli 因子・(6.4.2) 補正の欠落 | 棄却(前 addendum) |
| ~~②~~ | $\mathrm{pr}$ 経由の $\mathrm{gr}_4$ 辞書の誤り | ★ **棄却(本ノート §1・独立 Fox ルートで 6/6 一致)** |
| ~~基準~~ | 「正解は $F_4=0$」 | ★ **偽と判明(本ノート §2)= 新原因④** |
| **③** | 層対応($m\equiv0\leftrightarrow\chi\equiv1$)・補題 BR-1 の同一視 | 未検査(優先度低下) |
| **④** ★ | **非斉次 $\tau$ の実装/規約**(【BSY-GAP-1′】) | ★ **現在の唯一の焦点** |

> ### ★ 教材の更新(前 addendum の上申を強化)
> 「外部を疑う → 自前の辞書を疑う → **自分の判定基準を疑う**」。今回は**辞書が無罪で、基準が有罪**だった。
> ⟹ 規約台帳への上申を 1 項目追加: **「斉次(graded)条件と非斉次(ungraded)条件を混同しない」** — $\theta$ は次数保存だが $\tau,\rho$ は保存しない。**graded で立てた定理を ungraded の判定に使うな。**(D2/D3/D4-BLIND 系はすべて graded の言明である。)

---

**窓ゼロ・GAP ゼロ・封印非接触。機械は分数演算 2 本のみ。**
