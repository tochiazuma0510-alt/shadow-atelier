# [P1-D2] 実装直結仕様 — $E$ 上の 3 次被覆(裁定 1073・[CP] ① 線の律速)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(実装係の「§5 は計算手順まで降りていない」への回答)
前提 = `t3_gap12_resolution_v1.md`($\deg\mathcal E=3$・$\delta=0$)・`w9_E_model_v1.md`(+v1.1)
⚠ $u$/$c$ 非接触・prereg 非抵触。**格: candidate**。

---

## §0 ★★★ 結論 — 走査は **4 点**・系は **線形**(秒級)

前版の「$\mathcal E$-moduli 走査(Atiyah 3 型)」は**過大な枠**でした。分岐条件を入れると:

$$\boxed{\ \textbf{(i) 先決の 1 行検査}:\ B_1\oplus B_2\overset{?}{=}Q_0\quad(\text{群法則}) }$$
$$\boxed{\ \textbf{(ii) YES なら}\ P\in\{P:[2]P=Q_0\}\ \textbf{の}\ \textbf{4 点走査}\ \textbf{・各点で系は}\ \textbf{線形}\ \textbf{(未知数の比 1 個)}\ }$$
$$\boxed{\ \textbf{(iii) NO なら}\ z\ \textbf{が直線束の切断にならない} \Longrightarrow \textbf{Miranda 形(非分解 }\mathcal E\textbf{)= 重量級}\ \Longrightarrow\ \textbf{Sol 便}\ }$$

★ **規模判定の材料は (i) の 1 行**で決まります。

---

## §1 $E$ の明示座標(司令塔の Weierstrass 形を検証)

$$E:\quad Y^2+3\zeta_3XY+2Y=X^3,\qquad Q_\infty=O\ (\text{無限遠点}),\quad Q_0=(0,0)$$

**検証(私の独立計算)**
| 量 | 値 | 突合 |
|---|---|---|
| $c_4$ | $\tfrac{63}{2}-\tfrac{63\sqrt3}{2}i$ | — |
| $c_6$ | $351$ | — |
| $\Delta$ | $\mathbf{-216}=-2^3\cdot3^3$ | ★ 悪い還元 $\subseteq\{2,3\}$ ✔(前版 $-2^{27}3^3$ より最小に近い) |
| $j$ | $\mathbf{9261/8}$ | ★ **`E_identification_and_cofinality_v1.md` の $j$ と一致** ✔ |
| $Q_0=(0,0)$ | 曲線上 ✔ | ★ $Y^2+a_1XY+a_3Y=X^3$ 型では $(0,0)$ は **3-torsion**(標準)⟹ $[3]Q_0=O$ ✔ = $\mathrm{ord}(Q_0-Q_\infty)=3$ と整合 |

## §2 ★ $L(kQ_\infty)$ の明示基底

$\mathrm{ord}_{Q_\infty}(X)=-2$、$\mathrm{ord}_{Q_\infty}(Y)=-3$ ⟹

$$\boxed{\ L(kQ_\infty)=\bigl\langle\,X^iY^j\ :\ j\in\{0,1\},\ 2i+3j\le k\,\bigr\rangle\ }$$

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| dim | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 基底 | $1$ | $1$ | $1,X$ | $1,X,Y$ | $+X^2$ | $+XY$ | $+X^3$ | $+X^2Y$ |

★ $\dim L(kQ_\infty)=k$($k\ge1$)⟹ **隠れ玉なし** ✔

### 2.1 ★ 一般点 $P$ での基底(平行移動で作る)
$\tau_{-P}:R\mapsto R\ominus P$(群法則の有理式)とすると
$$\boxed{\ L(kP)=\bigl\{\,f\circ\tau_{-P}\ :\ f\in L(kQ_\infty)\,\bigr\}\ }$$
⟹ **基底 $\{1,\ X\circ\tau_{-P},\ Y\circ\tau_{-P},\ X^2\circ\tau_{-P},\dots\}$** — $E$ の加法公式を代入するだけで**明示式**になります。
($f\circ\tau_{-P}$ の極は $R\ominus P=Q_\infty$、すなわち $R=P$ ✔)

---

## §3 ★★★ パラメータ化の決定的な絞り込み(前版の置換)

### 3.1 $\deg M=1$($\mathcal E$-moduli ではなく **1 点**)
$z$ を直線束 $M$ の切断に取ると $A\in H^0(M^{\otimes2})$、$B\in H^0(M^{\otimes3})$、$\mathcal D:=-4A^3-27B^2\in H^0(M^{\otimes6})$。
$\delta=0$(既導出)⟹ $\deg\mathcal D=6$(分岐 $2+2+1+1$)⟹ $6\deg M=6$ ⟹
$$\boxed{\ \deg M=1\ \Longrightarrow\ M=\mathcal O(P),\quad P\in E\ \text{の}\textbf{1 点}\ }$$

### 3.2 ★ 主因子条件が $P$ を 6-torsion の torsor に落とす
$$\mathrm{div}(\mathcal D)=2Q_0+2Q_\infty+B_1+B_2-6P\ \ (\deg=0)$$
群法則($Q_\infty=O$、$[3]Q_0=O$ ⟹ $[2]Q_0=\ominus Q_0$):
$$\boxed{\ [6]P=B_1\oplus B_2\ominus Q_0\ }\qquad\Longrightarrow\ P\ \text{は }E[6]\ \text{の coset}\ (\le36\ \text{点})$$

### 3.3 ★★ 分岐条件が **4 点**に絞る
$A(Q_0)=A(Q_\infty)=0$ ⟹ $A\in L(2P-Q_0-Q_\infty)$、$\deg=0$ ⟹
$$A\ne0\iff 2P\sim Q_0+Q_\infty\iff \boxed{[2]P=Q_0}$$
($A=0$ は $z^3=-B$ = **巡回被覆** ⟹ 非巡回性(検分 §3.1)に反し**排除**)
$[2]P=Q_0$ かつ $[3]Q_0=O$ ⟹ $[6]P=O$ ⟹ §3.2 と併せて
$$\boxed{\ \textbf{★ 先決条件}:\quad B_1\oplus B_2=Q_0\ }$$
$$\boxed{\ \textbf{★ 走査}:\quad P\in\{P\in E:[2]P=Q_0\}\quad\textbf{— ちょうど 4 点}(E[2]\ \text{の coset})\ }$$

### 3.4 ★ 各 $P$ での系は**線形**
$$A\in L(2P-Q_0-Q_\infty)\ (\dim=1),\qquad B\in L(3P-Q_0-Q_\infty)\ (\deg=1\Rightarrow\dim=1)$$
⟹ 未知数 **2**(各 1 次元の係数)− ゲージ $z\mapsto\mu z$($A\mapsto\mu^{-2}A,\ B\mapsto\mu^{-3}B$)**1** ⟹
$$\boxed{\ \textbf{実質の未知数 = }A^3/B^2\ \textbf{の比 1 個 ⟹ }\textbf{線形}\ }$$
★ **Gröbner は不要**。残りは**検算**((iii) 以下)。

### 3.5 ⚠ Atiyah 3 型との関係(前版の枠の位置づけ)
| 場合 | 状態 |
|---|---|
| **$z$ が直線束 $M$ の切断**(= 上記) | ★ **4 点・線形・秒級** |
| **$\mathcal E$ 非分解** | ⚠ $z$ の大域切断が取れない ⟹ **Miranda 形**($\mathrm{Sym}^3\mathcal E\otimes\det\mathcal E^{-1}$ の切断)⟹ **重量級** |

⟹ ★ 前版の「分解型 $(0,3)/(1,2)$・非分解型」の 3 分類は、**分岐条件を入れると上の 2 分類に潰れます**($(0,3)$ 型は $A$ の消滅条件で落ちる)。

---

## §4 実装手順書 [P1-D2 v2](実装係へ直結)

```
=== [P1-D2 v2] E 上の 3 次被覆(4 点走査・線形)===
根拠: docs/notes/p1d2_concrete_spec_v1.md
土台: E: Y^2 + 3ζ_3 XY + 2Y = X^3、Q_∞ = O、Q_0 = (0,0)(3-torsion)
係数体: F_9 = Q(ζ_36)(★厳密・浮動小数点禁止)

[D2-0] ★ 既走(実装係並行中): δ=0 恒等式 deg(disc) = 6 の確認
        ⟹ 本仕様の §3.1(deg M = 1)の前提

[D2-1] ★★ 先決の 1 行検査(数分)
        B_1, B_2 の (X,Y) 座標を確定(w9_E_model_v1 §4 の 4 特別点表)
        ★ 群法則で B_1 ⊕ B_2 を計算し、Q_0 = (0,0) と一致するか
        ・一致 ⟹ [D2-2] へ(秒級ルート)
        ・不一致 ⟹ ★ 直線束 M が存在しない ⟹ Miranda 形(重量級)⟹ 司令塔へ報告して停止
        ⚠ この 1 行で ①線の規模判定が決まる — 最優先

[D2-2] P の 4 点を出す: {P : [2]P = Q_0}
        (E[2] は 2-除算多項式の根 ⟹ 4 点。F_9-有理性も同時に記録)

[D2-3] 各 P について線形系を解く
        基底(§2.1): L(kP) = { f ∘ τ_{-P} : f ∈ L(kQ_∞) }、τ_{-P}(R)=R⊖P は加法公式
        A: L(2P - Q_0 - Q_∞) の生成元(1 次元)を求める ⟹ A = α·(その生成元)
        B: L(3P - Q_0 - Q_∞) の生成元(1 次元)⟹ B = β·(その生成元)
        ゲージ z↦μz で (α,β) は α^3/β^2 の比のみが本質 ⟹ ★1 パラメータ

[D2-4] ★ 見張り(走らせる前から確定・fail-closed)
  (V1) deg(disc) = 6 ちょうど([D2-0] と突合)。7 以上なら M の取り方が誤り ⟹ 即停止
  (V2) δ = 0(conductor なし)
  (V3) ★ ord_{Q_0}(B) = ord_{Q_∞}(B) = 1(全分岐の Newton 条件)
       ⟹ B の生成元が Q_0, Q_∞ で *単純零* であること
  (V4) ★ disc の残り 2 零点が ちょうど B_1, B_2(位置・単純零)
       ⟹ ★これが本走の判定(1 パラメータの方程式 1 本)
  (V5) 得た W_9 の genus = 4(重複度公式 D8 の条件付き形)
  (V6) ord(P_0 - P_∞) = 9([P1-0b] からの予言)
  (V7) ★ 解ゼロ(4 点すべてで (V4) 不成立)⟹ 「z が直線束の切断となる 3 次被覆は存在しない」
       = 一級の否定的結果 ⟹ Miranda 形へ(重量級)

[D2-5] 実装条件・検疫(不変)
  ★ B_3 + B_4(e_C=2 の 2 点)は *個点を取らず F_9-有理因子として扱う*
     (w9_E_model_v1 §7: 座標は F_9 内だが式が膨らむ ⟹ 因子扱いが計算量上有利)
  封印検疫 4 行(裁定 1007):
     name_collide_note : "本仕様の平方類/立方類は F_9(E) の函数体類。封印『c 平方類』
                          (K^(5) 窓インスタンス)とは別対象。"
     n5_value_computed : false
     derivation_bridge_found : false
     b34_handled_as_divisor : true
出力: cert (schema r13-p1d2/v2)。記録: B_1⊕B_2 の値・P の 4 点・各 P の (α:β)・
      (V1)-(V7) の PASS/FAIL・u_touched=false ; c_touched=false
```

---

## §5 ★ 規模の見積り(司令塔の判定材料)

| 段 | 変数 | 方程式 | 規模 |
|---|---|---|---|
| [D2-1] 先決検査 | 0 | 群法則 1 回 | ★ **秒**(数分の座標確定込み) |
| [D2-2] $P$ の 4 点 | — | 2-除算多項式(4 次) | ★ **秒** |
| [D2-3] 各 $P$ の線形系 | **1**($\alpha^3/\beta^2$) | RR 基底の構成(加法公式の代入) | ★ **秒〜分** |
| [D2-4] (V4) の判定 | 1 | **1 本** | ★ **秒** |
| **合計(分解ルート)** | — | — | $\boxed{\textbf{★ 秒級 — 実装係で完結}}$ |
| ⚠ Miranda 形(先決検査 NO のとき) | $\mathrm{Sym}^3\mathcal E\otimes\det\mathcal E^{-1}$ の切断 | 非線形 | ⚠ **重量級 ⟹ Sol 便 115 相当** |

$$\boxed{\ \textbf{★ 判定}:\ \textbf{[D2-1] が YES なら実装係で秒級。NO なら Sol 便へ}\ }$$

---

## §6 GAP・記帳

- **【D2-GAP-1】(小・新)** §3.4 の $\dim L(3P-Q_0-Q_\infty)=1$ は $\deg=1$ の楕円曲線上の一般論。⚠ ただし**その生成元が $Q_0,Q_\infty$ で単純零**であることは別途((V3))。
- **【D2-GAP-2】(小・新)** $B_1,B_2$ の $(X,Y)$ 座標の確定が [D2-1] の前提。`w9_E_model_v1.md` §4 の所在表は「$s=\pm1$ の各ファイバーの単根側」までで、**Weierstrass 座標への変換は未実施** ⟹ [D2-1] の最初の作業。
- **【D2-GAP-3】(中・新)** Miranda 形(非分解 $\mathcal E$)の仕様は本書に**含みません**。[D2-1] が NO のときに別途起草。
- ★ **本仕様の新規部分**: ① 司令塔の Weierstrass 形の独立検証($j=9261/8$ 一致・$\Delta=-216$)② $L(kQ_\infty)$ の明示基底と**平行移動による $L(kP)$ の構成** ③ ★★ **$\deg M=1$ ⟹ 1 点 ⟹ 主因子条件で $E[6]$ torsor ⟹ 分岐条件で 4 点**という三段の絞り込み ④ ★★★ **先決条件 $B_1\oplus B_2=Q_0$**(1 行で規模判定が決まる)⑤ **系が線形($\alpha^3/\beta^2$ の比 1 個)**であること ⑥ Atiyah 3 分類が分岐条件で 2 分類に潰れること。
- ⚠ **前版の訂正**: `t3_gap12_resolution_v1.md` §3 の「$\mathcal E$-moduli 上の 1 次元走査」は、**分岐条件を入れる前の枠**でした。入れると**有限 4 点**に落ちます ⟹ **本書が置換**(暫定札 **m1073-1**)。
- **申告**: 私の側は sympy の記号計算のみ(GAP 走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
