# hexagon 判定式「非等価」の決着 — **両方正しい。$f$ と $f^{-1}$ の径数付けの違い**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 司令塔・緊急裁定案件(壁 P4 の土台・便 89 発送前)
- 結論: **judge も私の手書き式も正しい。両者は同じ $m=0$ 層を $f$ と $f^{-1}$ で径数付けている。既存測定への影響はゼロ。壁は無傷。**

---

## 0. 判定(3 点)

| 委嘱の問い | 判定 |
|---|---|
| **① どちらが (3.3)(3.4) の正しい $m=0$ 形か** | **どちらも正しい**。judge 式 $\mathcal J$ と手書き式 $\mathcal M$ の解集合は $\mathcal J=\{f^{-1}: f\in\mathcal M\}$(**集合として厳密に一致**・$A_{10}$ 全域 $1{,}814{,}400$ 元の悉皆で確認)。位数は常に等しい |
| **② 非等価の原因** | 等式の反転ではなく、**$\bar y$ を $f$ で共役する向き**。judge は paper 語 $f^{-1}\bar yf$ を `AbstractProd` の反転規約で GAP `f*ybar*f^-1`(= 左共役 ${}^{f}\bar y$)と書く。私は GAP 語順で $\bar y^{\,f}=f^{-1}\bar yf$(右共役)。**同一の shadow を $f$ と $f^{-1}$ という別のラベルで呼んでいる** |
| **③ 既存測定への影響** | **ゼロ**。$f\mapsto f^{-1}$ は層の全単射なので $\lvert\ker\widetilde\chi\rvert$・$\lvert\mathrm{GTSh}\rvert$・構造・$\Xi$ 像はすべて不変。梯子 17/17・r=4 両枝・I10-1 の再測定は**不要**。judge は内部で一貫、私の probe も内部で一貫 — **危険なのは両者を混ぜること**(今回の cert 化がまさにそれ) |

**壁 P4 は無傷**: 向きを揃えると judge の実物条件が **2280/2280**(P-WALL-2)・**162/162**(W-CENT-B)を生成条件込みで通過する(§3)。

---

## 1. 原因の特定(§委嘱 2)

### 1.1 二つの式の代数的な差

judge(`search/kerchi-judge.g` 146–165 行を **sed で機械抽出**して実行。転記の余地なし):
```
Dlt := AbstractProd([s1,s2,s1]) = GAP s1*s2*s1        (= a, 対合)
dlt := AbstractProd([s1,s2])    = GAP s2*s1           (b = s1*s2 では**ない**)
(3.10):  AbstractProd([f, TH(W,f)]) = 1               TH(g)=AbstractProd([Dlt,g,Dlt^-1]) = g^Dlt
(3.11):  RtOf(W,m,f) = c^m,  RtOf = AbstractProd([TT(TT(Wd)),TT(Wd),Wd]),  Wd = y^m f
```
$m=0$ で整理すると
$$\mathcal J:\quad (f\,a)^2=1\ \wedge\ (f\,\mathrm{dlt}^{-1})^3=1,\qquad \mathrm{dlt}=s_2s_1 .$$
私の手書き式(literal (3.3)(3.4) を GAP 語順で)は `sat_l1_v1` §2 の定理 RED で
$$\mathcal M:\quad (f\,a)^2=1\ \wedge\ (f\,b^{-1})^3=1,\qquad b=s_1s_2 .$$
**差は $\mathrm{dlt}=s_2s_1$ と $b=s_1s_2$ の一点のみ**($\mathrm{dlt}=b^{\,s_1}$・機械確認済)。$(H\text{-}a)$ 側は $a$ が対合ゆえ両者同一(規約 W-4 の「(H-a) は向きに鈍感」の再現)。

### 1.2 どちらが $\tau$ か — **どちらも $\tau$ である**(ただし $z$ の読みが違う)

$\tau:x\mapsto y\mapsto z\mapsto x$、$z=(xy)^{-1}$。窓上で 4 候補を直接検査(`sat_l1_probe14.g`):

| 候補 | $x\mapsto y$ | $y\mapsto z$ | $z\mapsto x$ | どの $z$ |
|---|---|---|---|---|
| $u\mapsto b\,u\,b^{-1}$(左共役 $b$) | ✓ | ✓ | ✓ | $z_1=(\bar x\bar y)^{-1}$(GAP 語順) |
| $u\mapsto \mathrm{dlt}^{-1}u\,\mathrm{dlt}$(右共役 dlt) | ✓ | ✓ | ✓ | $z_2=(\bar y\bar x)^{-1}$(paper "xy" の反転読み) |
| 残り 2 候補 | ✗ | — | — | — |

**両方とも位数 3 で $x\to y\to z\to x$ を回す正当な $\tau$** であり、違いは「$z$ をどちらの積と読むか」= 規約 W-1 そのもの。したがって**規約の一貫性の問題であって、どちらかが誤りではない**。

### 1.3 決定実験 — 悉皆で $\mathcal J=\mathcal M^{-1}$

`sat_l1_probe16.g`(judge core を機械抽出してロード・$P=A_{10}$ の全 $1{,}814{,}400$ 元を走査):

| 判定 | hexagon のみ | +生成条件 |
|---|---|---|
| $\mathcal J$(judge 実物) | **65** | **50** |
| $\mathcal M$(私の literal) | **65** | **50** |
| $\mathcal J=\mathcal M$ ? | **false** | — |
| **$\mathcal J=\{f^{-1}:f\in\mathcal M\}$ ?** | **TRUE** | — |

**⟹ 非等価ではなく、径数の反転。** これが implementer の「W-CENT-B の非自明 witness 1 件で真偽が食い違う」の正体である($f^2\ne1$ の元では $f$ と $f^{-1}$ が別物になるため)。

**補足(較正)**: この $65$ は私の Frobenius 計数 $T_{\rm all}([10])=65$ と一致、$50$ は生成分解数と一致(`sat_l1_v1` §10.6.2 の表)。**指標計算・judge・手書き式の三系統が同じ数に落ちる**。

### 1.4 なぜ shadow としては同一物か

judge の $T$ は $\bar y\mapsto \mathrm{AbstractProd}([f^{-1},\bar y,f])=f\,\bar y\,f^{-1}$、私の $T$ は $\bar y\mapsto\bar y^{\,f}=f^{-1}\bar y f$。
$f_{\rm judge}=f_{\rm mine}^{-1}$ とおけば
$$f_{\rm judge}\,\bar y\,f_{\rm judge}^{-1}=f_{\rm mine}^{-1}\,\bar y\,f_{\rm mine}=\bar y^{\,f_{\rm mine}}$$
で**写像 $T_{0,f}$ が完全に一致する**。$\Xi$ の値 $\alpha$($\bar x^\alpha=\bar x$、$\bar y^\alpha=T(\bar y)$ で一意)も同一。**同じ shadow を別の名札で呼んでいるだけ。**

---

## 2. 影響範囲(§委嘱 3)— **ゼロ**

- $f\mapsto f^{-1}$ は $m=0$ 層の**全単射**(かつ層ごとに閉じる)。よって **shadow の個数・群構造・$\Xi$ 像・$\ker\widetilde\chi$ の同型類はすべて不変**。
- 梯子 17/17・r=4 両枝・I10-1・D 族・norm_embedding — **すべて judge 経由で内部一貫**。再測定不要。
- 私の `sat_l1_probe1..13` — すべて手書き式で内部一貫。**個数・構造の結論はすべて不変**。
- **唯一の実害は「混ぜること」**。今回の cert 化は「私の $f$ を judge の式で検査した」ため 1/162 になった。**混用禁止をルール化すべき**(§4)。

---

## 3. 壁の再確認(向きを揃えた judge 実物条件での全数検算)

`sat_l1_probe17.g`(judge core 機械抽出をロードし、SURV の $f_z$ の**逆元**に judge 条件を当てる):

| 窓 | $\lvert C_{S_n}(v)\rvert$ | judge 条件を $f_z$ に | judge 条件を $f_z^{-1}$ に(生成込) | $\Xi$ 像 |
|---|---|---|---|---|
| **W-CENT-B**(n=18) | 162 | 1 / 162 ← implementer の観測と一致 | **162 / 162** | $C_9\times D_{18}$(162) |
| **P-WALL-2**(n=24) | 2280 | 120 / 2280 | **2280 / 2280** | $C_{19}\times S_5$(2280)**非可解** |

> ### 訂正版 定理 SURV(judge 規約)
> $$\boxed{\ f_z:=a_1\cdot\bigl(a_1^{\,z}\bigr)\qquad(z\in C_{S_n}(v))\ }$$
> (従来の $f_z=(a_1^{\,z})a_1$ の逆元。両者とも $a_1$ と $a_1^z$ の積で、順序だけが違う。)
> $\Xi([0,f_z])=z^{a_1}$、$C_{S_n}(w)\subseteq\Xi(\ker\widetilde\chi)\subseteq C_{S_n}(\bar x)$ は**そのまま成立**(§1.4 により写像は同一)。
> **⟹ 壁の主張「$\mathrm{GTSh}(N,N)$ は非可解」は無傷。** cert は $f_z$ の向きを judge 規約に揃えて再発行すればよい(値は全て同じ)。

---

## 4. 規範の提案(司令塔裁可事項)

1. **工房の正本規約は judge 側(`AbstractProd` 経由 = 規約 W-1 準拠)とする。** 数学者の紙も以後この向きで書く。
2. **私の `sat_l1_v1.md` の $f$ は judge の $f^{-1}$** である旨を同ノート冒頭に注記する(結論は不変・§1.4 の対応で読み替え可能)。定理 RED は判定式としてはそのまま正しい(`sat_l1_probe16` で $\mathcal M$ が実際に層を与えることを確認済)。
3. **混用禁止のルール化**: 「手書き式で得た $f$ を judge の式に入れない/その逆もしない」。証明書には **`f_orientation: "judge" / "handwritten"`** の欄を必ず立てる(今回の cert の note 欄の運用を欄に格上げ)。
4. **回帰テスト**: 新規 probe は `_judge_core_extract.g` を読んで judge 実物条件で検算する(手書き式は補助)。抽出は `sed -n '146,165p' search/kerchi-judge.g` で機械的に行う。

---

## 5. 検算

| スクリプト | 内容 | 結果 |
|---|---|---|
| `search/probe/wac_v1/sat_l1_probe14.g` | $\theta,\tau$ の同定(4 候補)+ 5 通りの判定式の解集合 | $b$ 左共役と dlt 右共役の双方が $\tau$・$z$ の読みだけが違う |
| `search/probe/wac_v1/_judge_core_extract.g` | `kerchi-judge.g` 146–165 行の **sed 逐語抽出** | — |
| `search/probe/wac_v1/sat_l1_probe16.g` | judge 実物 vs 手書き式($A_{10}$ 悉皆 1.8M) | $\lvert\mathcal J\rvert=\lvert\mathcal M\rvert=65/50$・**$\mathcal J=\mathcal M^{-1}$** |
| `search/probe/wac_v1/sat_l1_probe17.g` | 向きを揃えた judge 条件での壁・判別窓の全数検算 | **2280/2280・162/162**・$\Xi$ 像不変 |

**GAP 4.16.0 単系統。cross-checked ではない(ただし judge 実物・手書き式・Frobenius 指標計算の三者が同じ数に落ちる点は独立性の高い一致)。**
