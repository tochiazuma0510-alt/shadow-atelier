# r=4 判別窓 driver 仕様(司令塔抽出版・実装用)

**この文書は駆動側(implementer/CI)に渡してよい唯一の仕様である。予言ファイル(凍結済み・commit `fd5aab9`)は読まないこと(接触遮断)。**
判定は測定完了後に司令塔が行う。driver は生の測定値だけを出力する(期待値・比較対象をコードに書かない — 例外は下記の入口ゲートと fail-closed 上界のみ)。
構造の照合は **IdGroup の生出力**で行う(名前つき群との一致判定をコードに書かない)。

---

## 0. 入口条件 — 較正ゲート 2 本の回帰(**先頭・fail-closed**)

本測定の 2 窓は **素の経路が $4.9\times10^{18}$ で実行不能**であり、$\Xi$-制限実装の健全性を窓内で検証できない。したがって**既存の較正ゲート 2 窓を先に回帰させる**。

| 順 | 窓 | 素経路の走査数 | $\Xi$ 経路の走査数 | ゲート |
|---|---|---|---|---|
| G1 | `W-E-A10-9t1` | 10,886,400 | 486 | `naive_shadow_digest == xi_shadow_digest` |
| G2 | `W-E-A10-5x2t0` | 7,257,600 | 5,000 | 同上 |

- 窓の同定情報は `search/_a13_ladder_driver_spec.md`(G1)および `search/_i10_1_driver_spec.md`(G2)の該当節をそのまま使う。
- 正準リストの正規化手順(ソート規約・表示規約)は**両経路で同一**であること。digest はリスト全体に 1 回だけ取る。
- **G1 または G2 が不一致なら、本仕様の 2 窓を 1 シャードも撃たずに Error 終了する。**
- G1/G2 の結果は本測定の manifest に併記する(`entry_gate` 節)。

---

## 1. 対象: 2 窓

$\bar x$ の型 $(5,5,5,5)$、$n=20$、$\ell=5$、$r=4$、$t=0$、$N_{\rm ord}=5$。$\mathsf w:=b_1^{-1}a_1$、$\bar x=\mathsf w^2$。
**2 窓は $\mathsf w$ の型が異なり、$E$ の構成が異なる**(§2 の注意)。

```gap
## W-E-A20-5x4t0-C   (n=20, degree(E)=23, eps=0 : DIRECT product)
a1 := ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18);;
b1 := ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15,16,17,18,19,20)(21,22);;
JUDGE_S2_IMG := ( 1, 2,13,18,17,12,20,11,19,16)( 3,14,15,10, 4, 9, 7, 6, 8, 5)(22,23);;
JUDGE_ID := "W-E-A20-5x4t0-C";;

## W-E-A20-5x4t0-B   (n=20, degree(E)=23, eps=1 : FIBRE product)
a1 := ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16);;
b1 := ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17,18,19,20)(21,22);;
JUDGE_S2_IMG := ( 1,18,16, 6, 3)( 2,14, 5, 4,13,20, 9, 8,19,15)( 7,12,17,11,10)(22,23);;
JUDGE_ID := "W-E-A20-5x4t0-B";;
```

### 1.1 窓の諸元(同定情報。$\Xi$ 上界の監査用 — 測定値ではない)

| 窓 | $n$ | $\ell$ | $r$ | $t$ | $N_{\rm ord}$ | $c_m=\varphi(2N_{\rm ord})$ | $\lvert C_P(\bar y)\rvert$ | $\lvert\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)\rvert$ | $\lvert N_{S_{20}}(\langle\bar x\rangle)\rvert$ |
|---|---|---|---|---|---|---|---|---|---|
| W-E-A20-5x4t0-C | 20 | 5 | 4 | 0 | 5 | 4 | 7,500 | 15,000 | 60,000 |
| W-E-A20-5x4t0-B | 20 | 5 | 4 | 0 | 5 | 4 | 7,500 | 15,000 | 60,000 |

charming $m$ の集合 $=\{0,1,3,4\}$(両窓)。

### 1.2 canonical ID(fail-closed・窓ごとの最初の assert)

canonical 文字列 $=$ `<ID>|n=<n>|ell=<ell>|r=<r>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>`(GAP 印字形・UTF-8)の SHA-256。**`search/_i10_1_driver_spec.md` と同一書式**(`|ell=|r=` を含む)。

| 窓 | SHA-256 |
|---|---|
| W-E-A20-5x4t0-C | `d49d2556efa837b5f811072c42b06271ffab900f7240319ad87c000041ccdb84` |
| W-E-A20-5x4t0-B | `093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586` |

一致しなければ Error で停止。

---

## 2. 窓 assert(両窓・`search/strike-a18.g` の 16 項 assert 様式を踏襲)

`a1^2 = b1^3 = 1` / braid `s1*s2*s1 = s2*s1*s2` / `c = (s1*s2)^3 = 1` / `P = <s1^2, s2^2> = Kernel(E -> S3)` の位数 / `ord(xbar) = ord(ybar) = 5`・`ord(cbar) = 1` / 転記一致 assert(preamble ↔ `a1,b1` からの再構成が一致)。

参考値(assert 用・機械で再計算すること):

| 項目 | 値(両窓共通) |
|---|---|
| $\lvert E\rvert=[B_3:N]$ | 7,298,706,024,529,920,000 $=6\lvert A_{20}\rvert$ |
| $\lvert P\rvert$ | 1,216,451,004,088,320,000 $=\lvert A_{20}\rvert$ |
| $\mathrm{ord}(s_1)=\mathrm{ord}(s_2)$ | 10 |

> ### 【実装上の必須注意】**2 窓で $E$ の構成が違う**
> - **C 枝**: `sign(a1) = +1`、$\langle a_1,b_1\rangle=A_{20}$。$E=A_{20}\times S_3$(**直積**)。
> - **B 枝**: `sign(a1) = -1`、$\langle a_1,b_1\rangle=S_{20}$。$E=S_3\times_{C_2}S_{20}\subsetneq S_3\times S_{20}$(**ファイバー積**)。
>
> **B 枝で `E = DirectProduct(S3, S20)` と比較する assert を書いてはならない** — false になるがそれはスクリプトの誤りであって窓の欠陥ではない(`docs/notes/wac_tail8_v1.md` §3.3【assert の訂正】と同型の事故)。
> **両窓に共通して正しい assert は次の 3 本**:
> 1. `Size(E) = 6*Size(AlternatingGroup(20))`
> 2. `Size(P) = Size(AlternatingGroup(20))`、`P = Kernel(E -> S3)`
> 3. `E = Group(a1*(21,23), b1*(21,23,22))`(degree 23 の置換群として構成)
>
> **同一 driver で両枝を扱うので、`eps_branch` フラグ(`"eps0_direct"` / `"eps1_fibre"`)を証明書に必ず記録すること。**

---

## 3. $\Xi$-制限走査の fail-closed 上界

| 単位 | 上界 |
|---|---|
| **1 窓あたり(全 $m$ 層合計)** | $c_m\cdot\lvert C_P(\bar y)\rvert\cdot\lvert\mathrm{Stab}\rvert=4\times7{,}500\times15{,}000=\mathbf{450{,}000{,}000}$ |
| **charming $m$ 1 層あたり** | $\lvert C_P(\bar y)\rvert\cdot\lvert\mathrm{Stab}\rvert=7{,}500\times15{,}000=\mathbf{112{,}500{,}000}$ |
| **$\alpha\in\mathrm{Stab}$ 1 個あたり** | $\lvert C_P(\bar y)\rvert=\mathbf{7{,}500}$ |

**実測 $>$ 上界で Error**(層ごと・窓ごとの両水準で記録)。

---

## 4. シャーディング指示

### 4.1 二段の分割

- **第 1 段 = charming $m$ 層**: $m\in\{0,1,3,4\}$ の **4 層**。**1 層 = 1 CI run 以上**に分ける(層をまたぐ run を作らない)。
- **第 2 段 = $\alpha\in\mathrm{Stab}$**($\lvert\mathrm{Stab}\rvert=15{,}000$)。$\alpha$ を連続チャンクに切る。1 $\alpha$ につき走査は $\lvert C_P(\bar y)\rvert=7{,}500$。

$$\text{1 run の走査数}=(\text{チャンクの }\alpha\text{ 数})\times7{,}500 .$$

**推奨**: チャンク幅 $1{,}500$ ⟹ 1 run $=1{,}500\times7{,}500=1.125\times10^7$ 走査、1 層 $=10$ run、**1 窓 $=40$ run、2 窓 $=80$ run**。
600 秒 cap に収まらない場合はチャンク幅を半減する(幅は 15,000 の約数を取ること)。各 run の証明書に `m`、`alpha_chunk = [lo, hi]`、`chunk_scan_bound = (hi-lo+1)*7500` を必ず記録する。

### 4.2 結合

- 層内の run 出力を $\alpha$ の昇順で連結 → 層の shadow リスト。層を $m$ の昇順で連結 → 窓の shadow リスト。**JoinC は G1★ 工程の既存線形化をそのまま流用**。
- 結合後に窓単位で 1 回だけ `shadow_total`・群演算・`IdGroup` 等(§5 の欄 2 以降)を計算する。**層ごとに群を作らない**(合成則 (3.53) は層をまたぐ)。
- 結合の健全性: $\sum_{\text{run}}(\text{run の accepted 数})=$ 窓の `shadow_total`、および $\sum_{\text{run}}\text{chunk\_scan\_bound}=450{,}000{,}000$ を assert。

### 4.3 実行規律

- 1 run 1 GAP プロセス、`-o 2g`。run 間で状態を持ち越さない。
- **C 枝を先に完走させてから B 枝を撃つ**(B 枝はファイバー積の事故型を抱えるため、主測定の経路から外す)。
- CI: `.github/workflows/gap-run.yml`(inputs: script/preamble/out_dir/timeout_min)。

---

## 5. 測定欄(窓ごと・機械出力 JSON・期待値なし・生値のみ)

judge は $\Xi$-制限実装版(`kerchi-judge.g` v1.3 以降)・`JUDGE_SKIP_LEGACY_CROSSCHECK := true`。
$G:=\mathrm{GTSh}(N,N)$、$K:=\ker\widetilde\chi$($m=0$ 層)、$A:=O_{2'}(K)$(= $K$ の**正規部分群のうち奇位数のもの全体の積**。GAP では奇位数の正規部分群を列挙して最大のものを取れば足りる)、$S:=\mathrm{Syl}_2(K)$、$z:=Z(S)$ の生成元。

```text
##  同定・分岐
0.   canonical_id                = SHA-256(canonical 文字列)
1.   eps_branch                  = "eps0_direct" | "eps1_fibre"
1b.  stage1_asserts              = §2 の全項の ok フラグ配列

##  基本
2.   group_order                 = |G|
3.   ker_size                    = |K|                       # m=0 層
4.   ker_odd_part_order          = |K| の奇部分
5.   ker_2_part_order            = |K| の 2 部分
6.   ker_odd_part_primes         = 奇部分の素因子の集合
7.   K_struct                    = StructureDescription(K)
7b.  K_idgroup                   = IdGroup(K)（圏外なら "out-of-range"）
8.   K_is_direct_product         = K = A x S の内部直積か
9.   A_order, A_idgroup          = |A|, IdGroup(A)
10.  S_struct, S_order           = Syl_2(K) の構造と位数
11.  chi_image_order, Q_struct   = |Q| = |im chi~|, Q の不変因子
12.  Q_action_faithful_on_A      = Q -> Aut(A) が単射か
13.  gtsh_idgroup                = IdGroup(G)（圏外なら StructureDescription と
                                   主要不変量: 導来列の各位数・|Z(G)|・各 Sylow の位数）
14.  derived_length_G            = DerivedLength(G)
15.  derived_series_G            = |G'|, |G''|, |G'''| （1 に達するまで）

##  Xi 像と base 座標
16.  Stab_order                  = |Stab_Aut(P)(xbar)|
16b. Syl2_Stab_struct, order     = Syl_2(Stab) の構造と位数
17.  xbar_normalizer_order       = |N_{S_20}(<xbar>)|
18.  xi_alpha_well_defined       = 全 shadow で alpha が一意（norm_embedding.g 様式:
                                   xbar^alpha = xbar^(2m+1) かつ ybar^alpha = (ybar^(2m+1))^f）
19.  xi_hom_left / xi_hom_right  = 準同型規約の判定（両規約を試して生出力）
20.  xi_kernel_trivial           = 相異なる alpha の個数 == shadow 総数
21.  xi_image_order              = |Xi(G)|
21b. xi_image_in_normalizer      = Xi(G) <= N_{S_20}(<xbar>) か
22.  Bx_order                    = |B_x|（B_x := xbar の 4 巡回が生成する群）
22b. A_coords_in_Bx              = Xi(K) の奇部の各元を B_x 座標 (v1,v2,v3,v4) mod 5 で全列挙
                                   （B_x の生成元は xbar の巡回を出現順に取る。順序を証明書に明記）
23.  S_block_action              = Syl_2(Xi(K)) の 4 ブロックへの置換像と軌道分割

##  STR-1 系（t=4 梯子欄の踏襲。S ≠ 1 のときのみ意味をもつ）
24.  ZS_order                    = |Z(S)|
25.  G_over_CG_S                 = |G / C_G(S)|
26.  Inn_S_order                 = |S / Z(S)|
27.  H3_holds                    = (25 == 26)
28.  compl_classes_all           = # ComplementClassesRepresentatives(G, K)
29.  compl_classes_in_CG_S       = # ComplementClassesRepresentatives(C_G(S), C_G(S) ∩ K)
30.  epsilon_zero                = (29 > 0)
31.  z_in_Frattini               = z ∈ Phi(Syl_2(C_G(S)/A)) か
32.  central_product_witness     = (30 が false のとき) G = S ∘_{<z>} C_G(S) の明示 witness
33.  split_but_not_direct        = (28 > 0) and (29 == 0)

##  u = -1 層
34.  u_minus1_involutions        = 2m+1 ≡ -1 (mod 5) の層で、位数 2 かつ Syl_2(K) を
                                   中心化する shadow の個数（f ≠ 1 も走査すること）

##  fail-closed 会計
35.  xi_count_measured_per_m     = m 層ごとの実測 |C_m| の総和（4 値）
35b. xi_count_bound_per_m        = 112,500,000（4 値・§3）
36.  xi_count_measured_total     = 窓の総和
36b. xi_count_bound_total        = 450,000,000                # 36 > 36b で Error
37.  shard_manifest              = [{m, alpha_chunk, chunk_scan_bound, accepted}] の一覧
```

---

## 6. 実行と成果物

- 証明書: `search/certs/r4_<JUDGE_ID>_<date>.json` ×2 + 総括 manifest(全 run 証明書の SHA-256 一覧 + `entry_gate` 節に §0 の G1/G2 結果)。
- driver 名: `search/strike-r4.g`(`search/strike-i10-1.g` から転用 — canonical 文字列書式は同一、差し替えは (i) 窓データ (ii) $\varepsilon$ 分岐の assert (iii) $m$/$\alpha$ の二段シャード引数の 3 点)。
- provenance: GAP version・script SHA・elapsed・入力仕様書(本ファイル)の SHA-256・入口ゲート G1/G2 の digest。
- **本仕様のどの欄にも期待値は書かれていない。** driver は比較を行わず生値のみを出力する(例外は §0 の入口ゲート・§1.2 の canonical ID・§3 の $\Xi$ 上界・§4.2 の結合 assert)。
