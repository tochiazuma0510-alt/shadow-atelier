# I10-1 判別窓 driver 仕様(司令塔抽出版・実装用)

**この文書は駆動側(implementer/CI)に渡してよい唯一の仕様である。予言ファイル(凍結済み・commit 0586b0f)は読まないこと(接触遮断)。**
判定は測定完了後に司令塔が行う。driver は生の測定値だけを出力する(期待値・比較対象をコードに書かない — 例外は下記の較正ゲートと fail-closed 上界のみ)。
構造の照合は **IdGroup の生出力**で行う(名前つき群との一致判定をコードに書かない)。

## 対象: 2 窓

各窓の生成対 (a1,b1)・judge preamble。w := b1^-1*a1、xbar := w^2。**全窓 N_ord=5 系**。

```gap
## W-E-A10-5x2t0  (n=10, degree(E)=13)
a1 := ( 1, 2)( 3, 6)( 7,10);;
b1 := ( 2,10, 6)( 3, 5, 4)( 7, 9, 8);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12);;
JUDGE_S2_IMG := ( 1, 6, 4, 5, 3,10, 8, 9, 7, 2)(12,13);;
JUDGE_ID := "W-E-A10-5x2t0";;

## W-E-A15-5x3t0  (n=15, degree(E)=18)
a1 := ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11);;
b1 := ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17);;
JUDGE_S2_IMG := ( 1, 9,15,13,11, 5,10, 4, 2, 3)( 6, 8,12, 7,14)(17,18);;
JUDGE_ID := "W-E-A15-5x3t0";;
```

### 窓の諸元(同定情報。Ξ 上界の監査用 — 測定値ではない)

| 窓 | n | ell | r | t | N_ord | c_m=phi(2·N_ord) | \|C_P(ybar)\| | \|Stab_Aut(P)(xbar)\| |
|---|---|---|---|---|---|---|---|---|
| W-E-A10-5x2t0 | 10 | 5 | 2 | 0 | 5 | 4 | 25 | 50 |
| W-E-A15-5x3t0 | 15 | 5 | 3 | 0 | 5 | 4 | 375 | 750 |

## canonical ID(fail-closed・最初の assert)

canonical 文字列 = `<ID>|n=<n>|ell=<ell>|r=<r>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>`(GAP 印字形・UTF-8)の SHA-256。
**注意: A13 梯子の文字列書式とは異なる**(`|ell=|r=` が入る)。梯子の driver コードを流用する場合はここを差し替えること。

| 窓 | SHA-256 |
|---|---|
| W-E-A10-5x2t0 | 5848b4bffe7878f048a34379cd4042d1efbed1df6596aa0b5106694f46589df4 |
| W-E-A15-5x3t0 | 47d73376614720d4cc4b14bdbbc83ef77ba984b71bd2100fcaf9709f59fe26f0 |

一致しなければ Error で停止。

## 窓 assert(両窓・A18 driver = `search/strike-a18.g` の 16 項 assert 様式を踏襲)

braid s1s2s1=s2s1s2 / c=(s1s2)^3=1 / P=⟨s1²,s2²⟩=ker(E→S3) の位数 / ord(xbar)=ord(ybar)=5・ord(cbar)=1 / 転記一致 assert(preamble ↔ a1,b1 からの再構成が一致)。

> ### 【実装上の必須注意】**両窓とも ε=1(奇枝)= ファイバー積である**
> sign(a1) = −1(a1 は奇置換)・sign(b1) = +1。したがって
> $$E \;=\; S_3\times_{C_2}S_n \;=\;\{(z,\sigma)\ :\ \mathrm{sign}(z)=\mathrm{sign}(\sigma)\}\ \subsetneq\ S_3\times S_n .$$
> **`E = DirectProduct(S3, Sn)` と比較する assert を書いてはならない** — false になるがそれはスクリプトの誤りであって窓の欠陥ではない(`docs/notes/wac_tail8_v1.md` §3.3【assert の訂正】と同型の事故)。
> 正しい assert は次の 3 本:
> 1. `Size(E) = 6*Size(AlternatingGroup(n))`(機械で確認し証明書に記録)
> 2. `Size(P) = Size(AlternatingGroup(n))`、`P = Kernel(E -> S3)`
> 3. `E = Group(a1*(n+1,n+3), b1*(n+1,n+3,n+2))`(degree = n+3 の置換群として構成)
>
> 参考値(assert 用・機械で再計算すること): |E| = 10,886,400(n=10)/ 3,923,023,104,000(n=15)。

## Ξ-制限走査の fail-closed 上界(実測 > 上界 で Error)

| 窓 | Ξ 上界(c_m·\|C_P(ybar)\|·\|Stab\|) |
|---|---|
| W-E-A10-5x2t0 | **5,000** |
| W-E-A15-5x3t0 | **1,125,000** |

## 測定欄(両窓・機械出力 JSON・1 窓 1 証明書)

期待値なし・生値のみ。judge は Ξ-制限実装版(kerchi-judge v1.3 以降)・`JUDGE_SKIP_LEGACY_CROSSCHECK := true`。
G := GTSh(N,N)、K := ker chi~、A := O_{2'}(K)(= K の**正規部分群のうち奇位数のもの全体の積**。GAP では奇位数の正規部分群を列挙して最大のものを取れば足りる)、S := Syl_2(K)。

```text
0.  canonical_id
1.  group_order              = |G|
2.  ker_size                 = |K|
3.  ker_odd_part_order       = |K| の奇部分(位数の奇成分)
4.  ker_2_part_order         = |K| の 2 部分
5.  ker_odd_part_primes      = 奇部分の素因子の集合
6.  K_struct                 = StructureDescription(K)
6b. K_idgroup                = IdGroup(K)(圏外なら "out-of-range" と記録)
7.  K_is_abelian             = IsAbelian(K)
7b. K_is_direct_product      = K = A x S の内部直積か
8.  A_order                  = |A|
8b. A_derived_order          = |[A,A]|(A が非可換なら > 1)
8c. A_idgroup                = IdGroup(A)(圏外なら StructureDescription)
9.  chi_image_order          = |Q|,  Q := im chi~ = G/K
10. Q_struct                 = Q の不変因子
11. Q_action_faithful_on_A   = Q -> Aut(A) が単射か
12. gtsh_idgroup             = IdGroup(G)。SmallGroup 圏外なら StructureDescription と
                               主要不変量(導来列の各位数・|Z(G)|・各 Sylow の位数)
13. derived_length_G         = DerivedLength(G)
14. derived_series_G         = |G'|, |G''|, |G'''| （1 に達するまで)
15. xbar_normalizer_order    = |N_{S_n}(<xbar>)|(Aut(P) = S_n 内で計算)
16. gorder_divides_norm      = (欄 1) が (欄 15) を割るか
17. xi_count_measured        = 実測 |C_m| の総和
18. xi_count_bound           = 上表の値      # 17 > 18 で Error
```

### W-E-A10-5x2t0 のみ追加 — 較正ゲート

この窓は **素の経路(全 [P,P] 列挙)も実行可能**である。

```text
19. naive_shadow_digest      = 素の経路(c_m·|[P,P]| = 4 × 1,814,400 = 7,257,600 走査)の
                               shadow 正準リストの SHA-256
20. xi_shadow_digest         = Ξ-制限経路(5,000 走査)の同一 digest
21. naive_elapsed_sec / xi_elapsed_sec
```

正準リストの作り方は A13 梯子 driver(`W-E-A10-9t1` 段)と**同一の正規化手順**を使うこと — 両経路で同じソート規約・同じ表示規約であることが digest 一致の前提。

**ゲート則(凍結済みの撃ち順の実装)**: `W-E-A10-5x2t0` を最初に処理し、**欄 19 ≠ 欄 20 なら `W-E-A15-5x3t0` を撃たずに Error 終了**(fail-closed)。一致すれば続行。

## 実行

- 1 窓 1 GAP プロセス相当の分離(CI 上では順次でよいが、窓間で状態を持ち越さない — 各窓を独立関数+明示リセットで)。
- CI: `.github/workflows/gap-run.yml`(inputs: script/preamble/out_dir/timeout_min)。2 窓で timeout 45 min 見込み(n=10 窓の素経路 7.26e6 走査が支配項。Ξ 経路は 5,000 と 1,125,000 で軽い)。
- メモリ: n=10 窓の素経路は `Elements(DerivedSubgroup(P))` = |A₁₀| = 1,814,400 元を保持する。8GB 機・`-o 2g` の制約下で走るはずだが、必要なら charming m(4 層)でシャード分割してよい(digest は層ごとの部分リストを結合してから 1 回取ること)。
- 証明書: `search/certs/i10_1_<JUDGE_ID>_20260730.json` ×2 + 総括 manifest(全証明書 SHA-256 一覧)。
- driver 名: `search/strike-i10-1.g`(`search/strike-a13-ladder.g` から転用 — canonical 文字列書式と ε=1 の assert 2 点だけ差し替え)。
- provenance: GAP version・script SHA・elapsed・入力仕様書(本ファイル)の SHA-256。
