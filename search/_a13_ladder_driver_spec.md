# A13 梯子 driver 仕様(司令塔抽出版・実装用)

**この文書は駆動側(implementer/CI)に渡してよい唯一の仕様である。予言ファイル(凍結済み・commit 41b8698)は読まないこと(接触遮断)。**
判定は測定完了後に司令塔が行う。driver は生の測定値だけを出力する(期待値・比較対象をコードに書かない — 例外は下記の較正ゲートと fail-closed 上界のみ)。

## 対象: 13 窓(canonical 4 + 兄弟 9)

各窓の生成対 (a1,b1)・judge preamble。w := b1^-1*a1。全窓 N_ord=9 系。

### canonical 4 窓

```gap
## W-E-A10-9t1  (n=10, degree(E)=13)
a1 := ( 1, 2)( 3, 5)( 4,10)( 6, 9);;
b1 := ( 2, 9, 5)( 3, 4,10)( 6, 8, 7);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(11,12);;
JUDGE_S2_IMG := ( 1, 5,10, 3, 9, 7, 8, 6, 2)(12,13);;
JUDGE_ID := "W-E-A10-9t1";;

## W-E-A11-9t2  (n=11, degree(E)=14)
a1 := ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10);;
b1 := ( 1, 9,11)( 2,10, 8)( 3, 7, 5);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13);;
JUDGE_S2_IMG := ( 1,11, 8, 5, 4, 7, 6, 3,10)( 2, 9)(13,14);;
JUDGE_ID := "W-E-A11-9t2";;

## W-E-A12-9t3  (n=12, degree(E)=15)
a1 := ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10);;
b1 := ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(13,14);;
JUDGE_S2_IMG := ( 1, 2, 9,11, 7,12, 5,10, 3)( 4, 8)(14,15);;
JUDGE_ID := "W-E-A12-9t3";;

## W-E-A13-9t4  (n=13, degree(E)=16)
a1 := ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11);;
b1 := ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6);;
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13)(14,15);;
JUDGE_S2_IMG := ( 1,10, 8,12, 6, 5,13, 3,11)( 2, 9)( 4, 7)(15,16);;
JUDGE_ID := "W-E-A13-9t4";;
```

### 兄弟 9 窓(a1 のみ列挙。b1 := a1*w0^-1。judge preamble は同 t の canonical と同型に構成 — s1/s2 像は同一手順で作る)

```gap
## w0 = (1,2,3,4,5,6,7,8,9)  (t=1 系・n=10)  ID は W-E-A10-9t1-o2 .. -o6
#o2  a1 := ( 3, 9)( 4, 6)( 5,10)( 7, 8);;
#o3  a1 := ( 2, 3)( 4, 9)( 6, 8)( 7,10);;
#o4  a1 := ( 2, 3)( 4, 9)( 5, 7)( 6,10);;
#o5  a1 := ( 2, 4)( 3,10)( 5, 9)( 6, 7);;
#o6  a1 := ( 2, 6)( 3, 4)( 7, 9)( 8,10);;
## w0 = (1..9)(10,11)  (t=2 系・n=11)  ID は W-E-A11-9t2-o2 .. -o3
#o2  a1 := ( 2, 3)( 4, 9)( 5,10)( 6, 7)( 8,11);;
#o3  a1 := ( 2, 7)( 3,10)( 4, 5)( 6,11)( 8, 9);;
## w0 = (1..9)(10,11)  (t=3 系・n=12)  ID は W-E-A12-9t3-o2 .. -o3
#o2  a1 := ( 2, 4)( 3,12)( 5, 9)( 6,10)( 8,11);;
#o3  a1 := ( 2, 6)( 3,10)( 5,11)( 7, 9)( 8,12);;
```

## canonical ID(fail-closed・最初の assert)

canonical 文字列 = `<ID>|n=<n>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>`(GAP 印字形・UTF-8)の SHA-256。canonical 4 窓の期待値(これは同定情報であり測定値ではない — 一致しなければ Error で停止):

| 窓 | SHA-256 |
|---|---|
| W-E-A10-9t1 | 6092f5f0bae86188d1f46ede81e1dad2aebbb097d6d3c9cae46229b67e853f4b |
| W-E-A11-9t2 | ddc23c556d760adeab1dcdab24887719b5ab0a0b8e137fcea4b2df8077984649 |
| W-E-A12-9t3 | b127a9048c4659b74f5c2c9257e5e3dedfab66761b7ce3947195ef21c3749c79 |
| W-E-A13-9t4 | a11f207d3a6e31d118830ac94cad6fc2e9429582c49620efb52e8b268b7f941f |

兄弟窓は同じ処方で ID 文字列と SHA を**計算して証明書に記録**(期待値照合なし — 初出のため)。

## 窓 assert(全窓・A18 driver = search/strike-a18.g の 16 項 assert 様式を踏襲)

braid / c=(s1s2)^3=1 / |E|=6|A_n| または相応(ε=1 系はファイバー積 — |E| は機械で確認し記録) / P=ker(E→S3) の位数 / ord(x̄)=ord(ȳ)=9・ord(c̄)=1 / 転記一致 assert(preamble ↔ a1,b1 の再構成一致)。

## Ξ-制限走査の fail-closed 上界(実測 > 上界 で Error)

| 窓系 | Ξ 上界(c_m·|C_P(ȳ)|·|Stab|) |
|---|---|
| t=1 系(6 窓) | 486 |
| t=2 系(3 窓) | 972 |
| t=3 系(3 窓) | 8,748 |
| t=4(1 窓) | 139,968 |

## 測定欄(全窓・機械出力 JSON・1 窓 1 証明書)

期待値なし・生値のみ。judge は Ξ-制限実装版(kerchi-judge v1.3 以降)・`JUDGE_SKIP_LEGACY_CROSSCHECK := true`。

```text
0.  canonical_id
1.  group_order              = |GTSh(N,N)|
2.  ker_size                 = |ker chi~|
3.  ker_odd_part_order
4.  ker_2_part_order
5.  ker_odd_part_primes
6.  K_struct                 = StructureDescription(ker chi~)
6b. K_idgroup                = IdGroup(ker chi~)
7.  K_is_direct_product      = ker = (奇部分) x Syl_2(ker) の内部直積か
8.  chi_image_order          = |Q|
9.  Q_struct                 = Q の不変因子
10. Q_action_faithful_on_A   = Q -> Aut(奇部分) が単射か
11. xi_count_measured
12. xi_count_bound(上表)     # 11 > 12 で Error
13. S_struct                 = StructureDescription(Syl_2(ker chi~))
14. ZS_order                 = |Z(S)|
15. G_over_CG_S              = |G / C_G(S)|
16. Inn_S_order              = |S/Z(S)|
17. H3_holds                 = (15 == 16)
18. compl_classes_all        = # ComplementClassesRepresentatives(G, ker chi~)
19. compl_classes_in_CG_S    = # ComplementClassesRepresentatives(C_G(S), C_G(S) ∩ ker chi~)
20. epsilon_zero             = (19 > 0)
21. z_in_Frattini            = z ∈ Phi(Syl_2(C_G(S)/A)) か(S≠1 のとき)
22. central_product_witness  = (20 が false のとき)明示 witness
23. split_but_not_direct     = (18 > 0) and (19 == 0)
24. gtsh_idgroup             = IdGroup(G)・|G| が SmallGroup 圏外なら StructureDescription と主要不変量(導来列位数・中心・Sylow)
25. u_minus1_involutions     = 2m+1 ≡ -1 (mod 9) の層の、位数 2 かつ Syl_2(ker) を中心化する shadow の個数(f≠1 も走査)
```

### W-E-A10-9t1(canonical のみ)追加 — 較正ゲート

```text
26. naive_shadow_digest      = 素の経路(c_m·|[P,P]| = 1.09e7 走査)の shadow 正準リスト SHA-256
27. xi_shadow_digest         = Ξ-制限経路の同一 digest
28. naive_elapsed_sec / xi_elapsed_sec
```

**ゲート則(凍結済みの撃ち順の実装)**: A10-9t1 canonical を最初に処理し、**欄 26 ≠ 欄 27 なら残り 12 窓を撃たずに Error 終了**(fail-closed)。一致すれば続行。

## 実行

- 1 窓 1 GAP プロセス相当の分離(CI 上では順次でよいが、窓間で状態を持ち越さない — 各窓を独立関数+明示リセットで)。
- CI: `.github/workflows/gap-run.yml`(inputs: script/preamble/out_dir/timeout_min)。全 13 窓で timeout 60 min 見込み(A10 naive 1.09e7 走査が支配項)。
- 証明書: `search/certs/a13_ladder_<JUDGE_ID>_20260730.json` ×13 + 総括 manifest(全証明書 SHA-256 一覧)。
- driver 名: `search/strike-a13-ladder.g`(strike-a14.g 骨格 → strike-a18.g 規約で転用)。
- provenance: GAP version・script SHA・elapsed・入力仕様書(本ファイル)の SHA。
```
