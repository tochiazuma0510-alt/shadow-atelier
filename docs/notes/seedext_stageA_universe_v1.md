# SEED-EXT 段階 A — 宇宙凍結票

**状態札: prospective / prereg(run 前凍結)・数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-20 / 委嘱 = 司令塔(Sol T-57)
入力: old104(26 cube × 4 交換子型)rank 50 / nullity 54、**full108 rank 54 / nullity 54**(+4 seed → +4 rank)、157ed(順序付き $26^3$ triple-cube census 17,576 組・typed 15 組すべて raw-lambda 0・INERT)。
格: 予言のみ。機械計算ゼロ。封印非接触。**B4-A / B4-B いずれも非宣言。**

---

## 1. 前置測定 Step 0(これを先に走らせる・安価)

$$\mathrm{gr}_1\ :=\ H_{PB_3}\big/D_2,\qquad D_2:=[H_{PB_3},H_{PB_3}]\cdot H_{PB_3}^{\,3},$$
すなわち **$\mathrm{gr}_1=H_1(H_{PB_3};\mathbf F_3)$ = 相対 Frattini 商そのもの**(157dl lane の既存装置で計算可)。
$$\boxed{r:=\dim_{\mathbf F_3}\mathrm{gr}_1}$$
**出力要求**: $r$ と、$\mathrm{gr}_1$ の基底の**語による持ち上げ** $u_1,\dots,u_r\in H_{PB_3}$。

### 1.1 「26」と「4」の身分(Q1 への回答)

**26 は $r$ ではなく登録 cube 生成子リストの本数**と判定する(実装由来)。診断は次の 1 行で付く:
- old104 の cube 側が $\mathrm{gr}_1$ で張る次元を $a$、相手側(4 交換子型)が張る次元を $b\ (\le4)$ とすると、その像は $[\,\cdot,\cdot\,]$ の双線型像で
$$\mathrm{rank}_{104}\ \le\ ab\ -\ (\text{反対称・Jacobi 重複}).$$
$\mathrm{rank}_{104}=50$ は例えば $(a,b)=(13,4)$、$52-2=50$ と整合する。
> **⟹ 診断: $b\le4\ll r$ ならば old104/full108 は「相手側の被覆が致命的に不足」しており、これが rank が飽和しない理由である。** Step 0 で $r$ が出れば即断できる。

---

## 2. 完全 seed 族の構成子(Q2 への回答・凍結対象)

$$\boxed{\ \mathcal S_2\ :=\ \underbrace{\bigl\{\,[u_i,u_j]\ :\ 1\le i<j\le r\,\bigr\}}_{\binom r2\ \text{本}}\ \cup\ \underbrace{\bigl\{\,u_i^{\,3}\ :\ 1\le i\le r\,\bigr\}}_{r\ \text{本}}\ }\qquad |\mathcal S_2|=\binom r2+r=\frac{r(r+1)}2 .$$

**規約(決定・両論併記しない)**
1. **$i<j$ のみ**。順序付き対は不要 — $\mathrm{gr}_2$ で $[u_j,u_i]=-[u_i,u_j]$ ゆえ**新しい方向をひとつも生まない**(rank は 1 も上がらず span だけ 2 倍になる)。**157ed の $26^3$ 順序付き census が inert だったことと同じ理由**である。
2. **$[a,b]:=aba^{-1}b^{-1}$** に固定(W-FORM カードと同一規約)。取り違えは符号反転として現れる(c2q「24 の由来」型の検算)。
3. **制限冪は $u_i^{3}$**($\mathrm{gr}_2$ の $[3]$-作用)。$u_i^{3}$ と $[u_i,u_j]$ の両方が要る — $\mathrm{gr}$ は**制限** Lie 代数なので交換子だけでは $\mathrm{gr}_2$ を張らない。

**本数の目安**

| $r$ | $\binom r2+r$ |
|---:|---:|
| 10 | 55 |
| 12 | 78 |
| 16 | 136 |
| 20 | 210 |
| 26 | 351 |

**既存 108 との扱い(推奨をひとつに)**
> **包含して 1 本で再走する**: 走査宇宙 $=\mathcal S_2\ \cup\ (\text{old108})$。
> 理由: (i) rank/nullity の比較は**同一 target・同一 D2-prefix** の上でしか意味がない、(ii) old108 の seed が $\mathcal S_2$ に含まれる保証がない(cube 生成子リストと $u_i$ が別物なら)、(iii) 余分な列は rank を下げないので**害がない**。差分走行は比較不能になるので**採らない**。
**規模**: 列数 $\le\frac{r(r+1)}2+108$($r=26$ でも 459)、行数 33,293。$\mathbf F_3$ 上の疎線形代数として**実行可能性の懸念なし**。

---

## 3. 予言の数値化と receipt 直読述語(Q3 への回答)

**予言 A-1(rank)**
$$\mathrm{rank}_A\ =\ \operatorname{rank}\bigl(\text{作用}:\mathrm{gr}_2\to\text{target6 空間}\bigr)\ \le\ \dim\mathrm{gr}_2\ \le\ \frac{r(r+1)}2 .$$
**検証可能な核心は不等式ではなく増分**:
$$\boxed{\ \textbf{A-1: }\ \mathrm{rank}_A\ >\ 54\ }$$
(full108 の 54 より**真に大きい**。被覆説が正しければ必ず増える。)

**予言 A-2(整合化)**
$$\boxed{\ \textbf{A-2: }\ \mathcal S_2\cup\text{old108}\ \text{の span 内で target6 が整合し、lift が出る}\ }$$

**receipt 直読述語**

| 予言 | 字段 | PASS | FAIL |
|---|---|---|---|
| A-1 | target6 の `rank` | `rank` > 54 | `rank` = 54 |
| A-2 | target6 の `consistent` / `classification` | 整合(lift 発見) | 不整合継続 |
| 補助 | `nullity` | $=\lvert\text{seed}\rvert-\mathrm{rank}$ の恒等式で自己検算 | 破れたら実装エラー |
| 補助 | $\dim\mathrm{gr}_2$(Step 0 から別途算出) | `rank` $\le\dim\mathrm{gr}_2$ | 超えたら実装エラー |

**棄却条件(明示)**
- **`rank` = 54 のまま** ⟹ **被覆説を棄却**。target6 の障害は $\mathrm{gr}_2$ の像の中にない ⟹ 段階 B(次数 3)へ。**このとき札 6 が生き返る。**
- **`rank` > 54 だが不整合継続** ⟹ **A-1 生存・A-2 棄却**。被覆は効いたが足りない ⟹ 段階 B へ。
- **`rank` > 54 かつ整合** ⟹ **SEED-EXT 的中**。**札 6 棄却・札 8 は「被覆不足の別名」へ格下げ**。
- **`rank` > $\dim\mathrm{gr}_2$** ⟹ 実装エラー(棄却でなく再検)。

---

## 4. full108 データ点との整合検算(Q3 後半)

- $50+54=104$ ✓、$54+54=108$ ✓ — **両方で rank–nullity が成立**、seed は線形独立 ✓。
- **seed 4 本追加 → rank ちょうど +4・nullity 不変(54)** ⟹ 追加 4 本は**旧像の外に一次独立に出た** ⟹ **像は 104 の時点で飽和していなかった** ✓✓。
> **これは被覆説の直接の裏付けである**: 飽和していれば追加は +0 だった。**被覆を増やせば rank が増える**という予言が、既に 1 データ点で確認されている。
- **157ed(順序付き triple-cube 17,576 組が INERT)との整合** ✓: §2 規約 1 のとおり順序付き反復は $\mathrm{gr}_2$ で新方向を生まない。**157ed の inert は被覆説と矛盾せず、むしろ「順序付き反復では被覆は増えない」という予言の確認**である。⟹ **必要なのは反復数ではなく $\mathrm{gr}_1$ 基底の完全性**。

---

## 5. FC-40 の組込み(Q4 への回答)— 基底の選び方まで指定

**弱 W-FORM($PB_3^{ab}$ 像ゼロ)の生死は、解が $u_i^{3}$ を使うかではなく、使う $u_i$ が $PB_3^{ab}$ で消えるかで決まる。**
$u_i^{3}$ の $PB_3^{ab}$ 像は $3\overline{u_i}$。$H_{PB_3}$ の $PB_3^{ab}=\mathbf Z^3$ での像は階数 $\le3$ ⟹ **$\mathrm{gr}_1$ の基底のうち $PB_3^{ab}$-内容を持つのは高々 3 本**。

> **基底選択規約(凍結対象)**: $u_1,\dots,u_{r-s}\in[PB_3,PB_3]\cap H_{PB_3}$($s\le3$)、残り $u_{r-s+1},\dots,u_r$ のみが $PB_3^{ab}$-内容を持つように基底を取る。
> **receipt 要求字段**:
> - `solution_support_cubes`: 整合解が使う $u_i^{3}$ の添字集合
> - `dangerous_cube_used`: その添字集合が $\{r-s+1,\dots,r\}$ と交わるか(bool)
> - `pb3ab_image_of_solution`: 解の補正語の $x_{12},x_{23},x_{13}$ 指数和(3 整数)
> **判定**: `pb3ab_image_of_solution` $=(0,0,0)$ ⟹ **弱 W-FORM 生存**、FC-32 / LT-1 (P4) の自動性維持。非零 ⟹ **弱形破れ**、LT-1 (P4) は個別検査へ差し戻し。

---

## 6. 札 6 の現在の格(Q5 への回答・一行)

> **札 6 SOULE-BAND(深さ 3 が本質)= 条件付き保留。棄却していない。** 157ed は**部分的否定証拠**にとどまる — 順序付き triple-cube は Witt 基底の次数 3 元と別物であり、§2 規約 1 の理由で inert は必然だったから。**段階 A の `rank` 字段が 54 のままなら札 6 は復活、54 を超えて整合すれば札 6 は棄却。**

---

## 7. 実行仕様(Sol がそのまま IF-FIRST に使える形)

```text
STEP 0  compute r = dim_F3 H_1(H_PB3; F3), lift basis u_1..u_r
        (choose u_1..u_{r-s} inside [PB3,PB3], s<=3)          ← §5 規約
        report r, dim gr_2
STEP 1  seeds := { [u_i,u_j] : i<j } ∪ { u_i^3 : i } ∪ old108  ← §2(包含再走)
        report |seeds| = C(r,2)+r+108 (重複除去後)
STEP 2  solve target6 over F3, same base pair / same D2-prefix as 157eb
        report rank, nullity, consistent, classification
STEP 3  if consistent: report solution_support_cubes,
        dangerous_cube_used, pb3ab_image_of_solution           ← §5
PREREG  A-1: rank > 54 ;  A-2: consistent = true
        REJECT if rank == 54  (⟹ coverage説棄却・札6復活)
        REJECT A-2 only if rank > 54 and not consistent (⟹ 段階B)
```

---

## 8. 申告

- 手計算で検証: $\mathrm{gr}_1=H_1(H_{PB_3};\mathbf F_3)$、$\mathcal S_2$ の本数 $\binom r2+r$、順序付き対が rank を増やさないこと、$50+54=104$ / $54+54=108$、$u^3$ の $PB_3^{ab}$ 像 $=3\bar u$、$H_{PB_3}$ の $PB_3^{ab}$ 像の階数 $\le3$。
- **$r$ と $\dim\mathrm{gr}_2$ は未測定**(Step 0)。従って rank の予言は**「> 54」という増分形**で固定した — 絶対値の予言は Step 0 の後に確定させること。
- **26 の身分は診断待ち**($r$ と比較して即断)。
- **UNKNOWN**: $r$、$\dim\mathrm{gr}_2$、A-1/A-2 の成否、札 6 の最終格。
- 157ed は陰性を主張していない(scope 正直)⟹ **A 側にも B 側にも動いていない**。
- **B4-A / B4-B いずれも宣言していない。**
