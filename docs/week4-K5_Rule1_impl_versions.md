# Rule 1 抽出・判定パイプライン 実装版一覧(v2)

2026-07-27 実装(implementer)。委嘱: 便 32 P6 後半(司令塔発注)+ 便 34
blocker 2-5 修理(Sol 便 34 差戻し `sol/sol_reply_34_freeze1.md` P6-E1/E2/K1/C3
+ seal 完全化)。仕様正本: `docs/week4-K5_Rule1_v1.md` §6(u の二経路)・
§8(exact Kummer 判定器)・manifest `docs/manifest_k5_v1.md` §較正三層。

**この版で解消した Sol 便 34 blocker**:
1. **P6-E1(blocker 2)**: 経路 A(GAP)・Kummer 判定器(GAP)を「library(関数
   定義のみ・QUIT なし)+ 薄い driver(K3 較正専用・QUIT は driver 側)」に
   再構成した。node 側の経路 B も同型に分離した(lib + driver)。将来の K5
   driver は library を `Read`/`import` して呼ぶだけで良く、library の
   digest は変更しない。
2. **P6-E2(blocker 3 前半)**: 経路 A/B の raw 出力 JSON に
   `model_digest`(sha256(canonical_model_string))を embed した。
   `crosscheck/u-compare.mjs` は id/M だけでなく branchP0・x0・y0・f・A・B の
   全フィールド一致・model_digest 一致・**この checker 自身による独立再計算
   での digest 一致**・pathA の curve_residual_zero・u≠0 を fail-closed に
   検査してから u^(A)=u^(B) を判定する。
3. **P6-K1(blocker 3 後半)**: `search/kummer-decide.g` の `OrdModM` が試した
   全ての(失敗した)約数について obstruction を収集し、証明書 JSON に
   `minimality_obstructions` として保存するようにした。witness が満たす式を
   `witness^M = w^ord` と明示し(旧版表の「e^6=u を検算」という誤記を修正
   — 正しくは `e^6=u^3` である)、witness の基底係数
   (`witness_coeffs_basis_powers_of_root`)も証明書に保存した。
   `crosscheck/check-kummer.mjs` はこの obstruction リストと witness 等式を
   独立(`crosscheck/cyclo-ring-lib.mjs`・円分多項式の環演算・GAP 非依存)に
   再検算する。
4. **P6-C3(blocker 4)**: `KummerCovariance3Check`(GAP・`GaloisCyc` ベース)
   と `crosscheck/check-kummer-cov3.mjs`(node・円分多項式環演算による独立
   再構成、GAP の `GaloisCyc`/`AlgebraicExtension` は不使用)の二系統で、
   τ↦τ∘[d'](μ_M の生成元の取り替え)と Kummer character の逆冪
   κ↦d'⁻¹κ を同時に施しても (5′) 相当の等式が不変であることを K3 較正
   ケースで artifact 化した。
5. **seal 完全化(blocker 5)**: 本表を全ファイル確定後の blob hash で更新し、
   raw 較正 artifact(u_pathA/u_pathB/compare/kummer/cov3 の JSON、計算器
   出力含む)を `certificates/k5pipeline/` に保存した(旧 `certificates/
   k5fixture/*-u-pathA.json` 等の schema v1 出力は本表 §5 の理由で削除し、
   `k5pipeline/` の schema v2 出力に一本化した)。

**引き続き未着手(本便の範囲外・parent 発注により明示的に除外)**:
Sol 便 34 の blocker 1(R1-T0: 枝 (N) の P0=ι(P∞) 排除・Rule 1 総体性)は
**本便の対象外**(K⁽⁵⁾ の個別モデル・u に触れない規律により、Rule 1 の
数学的修理は司令塔/数学者の担当)。したがって本表の更新だけでは Freeze 1
の NO-GO は解除されない — blocker 1 の解消が別途必要。

## 0. 身分

本文書は §8.6「版の固定」の実体化である。**この時点ではまだ `git commit`
していない**(委嘱の規律「git commit しない」に従う)。したがって以下の
ハッシュは `git log -1 --format=%H -- <file>` ではなく
`git hash-object <file>`(working tree のバイト内容から算出される blob
ハッシュ)を確定値として記録する(2026-07-27 blocker 2-5 修理完了時点の
working tree バイト内容から実測・再現可能)。

**司令塔が commit した後に行うこと**: 各ファイルについて
`git log -1 --format=%H -- <path>` を実行し、下表の「commit ID(要取得)」欄
を実値に差し替える。commit しても blob hash(`git hash-object`)自体は
変わらない(commit は blob への参照を作るだけ)ので、下表の blob hash 列は
そのまま検証に使える。

## 1. library ファイル(凍結対象)

| # | ファイル | 役割 | blob hash (`git hash-object`, 2026-07-27) |
|---|---|---|---|
| 1 | `search/u-extract-pathA.g` | 経路 A library(GAP・K[[t]] 冪級数・Hensel/Newton 持ち上げ・model_digest 計算) | `abbc1b3904adb5631d1cd09d740358d2f02bbc33` |
| 2 | `crosscheck/u-extract-pathB-lib.mjs` | 経路 B library(node・多項式係数評価・Taylor 係数のみ・級数不使用・model_digest 計算) | `a064d1e69d2e7f2c8924de28adaf04b938458101` |
| 3 | `search/kummer-decide.g` | exact Kummer 判定器 library(GAP・`AlgebraicExtension` 上 `Factors`・minimality obstruction 収集・`KummerCovariance3Check`) | `f6971844744382f0a757369b617dbc33b1a9f2d8` |

## 2. driver ファイル(K3 較正専用・凍結対象ではない)

将来の K5 driver は library を変更せず、以下と同型の新しい driver ファイル
を追加する。

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 4 | `search/u-extract-pathA-k3-driver.g` | 経路 A・K3 較正 driver(model literal・実行・QUIT) | `99875a3bcbae08825217e83aef55ee46c22d3778` |
| 5 | `crosscheck/u-extract-pathB-k3-driver.mjs` | 経路 B・K3 較正 driver | `979a227866bc70f02e408765b98172a8f7708223` |
| 6 | `search/kummer-decide-k3-driver.g` | Kummer 判定器・K3 較正 driver(RunK3Calibration + covariance-3) | `202dbca26cb651434814d659315729913584362c` |

## 3. 第三 checker(照合器・crosscheck/)

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 7 | `crosscheck/u-compare.mjs` | 経路 A/B raw の第三 checker(全フィールド一致・model_digest 独立再計算・curve_residual_zero・u≠0・u^(A)=u^(B)) | `7f64ac0229d35850e64f63557ea9bd5f164a0d03` |
| 8 | `crosscheck/check-kummer.mjs` | Kummer 判定の独立照合器(node・factorization 不使用・別アルゴリズム・minimality obstruction 独立再判定・witness 等式独立再検算) | `d8c28b5d167e7ac90046f82dacb4a28e600c198e` |
| 9 | `crosscheck/check-kummer-cov3.mjs` | 第三 covariance(τ∘[d']+κ 逆冪)の独立照合器(GAP の GaloisCyc/AlgebraicExtension 不使用) | `fdcf28cf28f43d937a0fb02c910649b4e8d198fa` |
| 10 | `crosscheck/cyclo-ring-lib.mjs` | 円分多項式の環演算(共有インフラ・#8/#9 が使用・GAP コードは import しない) | `4509985e3ab269342cf182bf72c4a0f358f852b1` |

## 4. fixture

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 11 | `certificates/k5fixture/K3-regression-model.json` | K3-regression の派生 `y^2=f(x)` モデル(model-spec/v1・無変更) | `d4b5c60aa362b010446e8f0add7fc4f842640a58` |

## 5. raw 較正 artifact(`certificates/k5pipeline/`・追跡保存)

旧版(`certificates/k5fixture/*-u-pathA.json` 等・schema v1)はこの便で
`certificates/k5pipeline/` の schema v2(model_digest・minimality_obstructions
等を含む)に置き換え、旧ファイルは削除した(2026-07-27 監査時点で git
未追跡だったため、履歴の破壊ではない — `sol_reply_34_freeze1.md` F5 参照)。

| ファイル | blob hash |
|---|---|
| `certificates/k5pipeline/K3-regression-u-pathA.json` | `ff631aa17270c67c736cbb831c4b4380b76104dd` |
| `certificates/k5pipeline/K3-regression-u-pathB.json` | `23de147a1a6c10ffa0e0faa4dcc166cf6a056aaf` |
| `certificates/k5pipeline/K3-regression-u-compare.json` | `7d3e86f5ef4b05ae68a7fd818325985f50e74a83` |
| `certificates/k5pipeline/K3-regression-cov1-k2-u-pathA.json` | `60cd4fd618af0fb0c5f5e05c4dad07a5ab7e7e9d` |
| `certificates/k5pipeline/K3-regression-cov1-k2-u-pathB.json` | `b84b49e67ac55d116075e6112eaaf0d1e1537136` |
| `certificates/k5pipeline/K3-regression-cov1-k2-u-compare.json` | `f3871ed8895d1b93dbd435d646c523b50fed4b2a` |
| `certificates/k5pipeline/K3-regression-kummer-u.json` | `d3a675831e49fff8f582f7624cb2dc3a23bb10c0` |
| `certificates/k5pipeline/K3-regression-kummer-u-checkkummer.json` | `abc4cb7d2490d272c4b44fbd17d1a50ea6e83eb7` |
| `certificates/k5pipeline/K3-regression-kummer-uinv.json` | `ec74c579627c6fdccec9e482a56344fef1499937` |
| `certificates/k5pipeline/K3-regression-kummer-uinv-checkkummer.json` | `fbd9f257931c9ae1a478379662d319f6aa0dc236` |
| `certificates/k5pipeline/K3-regression-kummer-cov3.json` | `3ed5ca04a4b96135e3d6af3d3015f071e069f3a2` |
| `certificates/k5pipeline/K3-regression-kummer-cov3-checkcov3.json` | `26a1ca62fa6b6616d010aaad874c43720c3034f7` |

## 6. 実行環境版

- GAP: 4.16.0(`C:\Program Files\GAP-4.16.0`、実行は `gap.ps1` 経由・`-o 2g`)。
- node: v24.16.0。
- 数体演算ライブラリ: GAP 組み込み `Cyclotomics` / `AlgebraicExtension`(外部パッケージ不使用)。第三 covariance の Galois 作用は GAP 組み込み `GaloisCyc`(native `Cyclotomics` 上・`Factors` を経由しない別機能)。
- 因数分解アルゴリズム: GAP 組み込み `Factors`(体は `AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals, n))` として構成 -- §7 の罠参照)。
- model digest: sha256。GAP 側は `Exec` 経由 `sha256sum`(既存 `search/e2c6-sweep.g` `ComputeSha256File` と同方式)、node 側は組み込み `node:crypto`。両実装は独立でありながら同一 canonical_model_string に対して同一 digest を実測で確認済み(§8)。
- イデアル分解アルゴリズム: 本実装では未使用(obstruction は (O-b)/(O-c) のみ実装。(O-a) は今回のスコープ外)。

## 7. 実装上の発見(罠・報告事項、便 32 から継続)

**GAP の `CF(n)` は `Factors` に対して体として正しく振る舞わない。**

`Indeterminate(CF(12), "T")` 上で `T^2+4` を `Factors` にかけると `[T^2+4]`
(既約)と誤って返す。しかし `Value(T^2+4, 2*E(4))` = 0(2i は明らかに根)であり、
`2*E(4) in CF(12)` は `true`。すなわち `CF(n)` は「乗法群を含む Cyclotomics の
緩い collection」であって、`Factors` はその上で有理係数の範囲でしか分解を
試みず、非有理な(が K の元である)根を見逃す。

正しい構成は `AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals, n))`
で体として認識させること。実測: この構成では `T^2+4` を正しく
`(T-2a^3)(T+2a^3)` に分解する(`a` = 定義多項式の根)。`search/kummer-decide.g`
はこの構成を正本として採用している。

**第三 covariance の実装上の発見**: 上記の罠は `Factors`(根探索)に固有で
あり、`GaloisCyc`(Galois 作用の適用)には影響しない。witness の座標
(`ExtRepOfObj`)は `AlgebraicExtension` の生成元 `a` と native `Cyclotomics`
の `E(n)` が(同じ定義多項式 `CyclotomicPolynomial(Q,n)` の根として)同じ
基底表現を持つため、`c0+c1*a+...` を `c0+c1*E(n)+...` にそのまま読み替えて
native 側の演算(`GaloisCyc`)に持ち込める。この変換だけで根探索
(`Factors`)を経由せずに Galois 作用を計算できる。

## 8. K3 regression fixture 較正結果(§6.4/§8.3 raw 再計算・v2)

`certificates/k5fixture/K3-regression.json`(既存・司令塔管理下)に記録された
既知値 u=−4・ord([u⁻¹]₆)=3 を、モデルからの raw 再計算として全パイプラインで
再現した(期待値のハードコード比較ではなく、モデル係数から独立に再導出)。

| 検査 | 結果 |
|---|---|
| 経路 A: u_pathA (K3-regression) | `-4` |
| 経路 B: u_pathB (K3-regression) | `-4` |
| model_digest(GAP 独立算出) | `066eb85eeebbdeac4d5190abaf63325fc32d1a80d29e2b0cb81d6fc38fecedb7` |
| model_digest(node 独立算出) | `066eb85eeebbdeac4d5190abaf63325fc32d1a80d29e2b0cb81d6fc38fecedb7`(GAP と一致) |
| 第三 checker(全フィールド+digest+curve_residual_zero+u≠0+u^(A)=u^(B)) | `ACCEPT` |
| COV-1(s→cs, k=2 の M2 残余群作用モデル): u_pathA / u_pathB | `-1/1024` / `-1/1024` |
| COV-1: model_digest(GAP/node 独立算出一致) | `588fc3c7562ce8297721a27135f7d468db8ecd4563b3244e109ddd148567f165` |
| COV-1: 第三 checker | `ACCEPT` |
| COV-1: u_cov1/u_base = k^(-2M) の厳密検算 | `1/4096 = 1/4096` 一致 |
| kummer-decide: ord(u=-4) mod 6 | `3`(witness 明示・`witness^6=u^3` 検算込み) |
| kummer-decide: minimality_obstructions(u) | divisor 1・2 とも obstruction_prime=3(irreducible T^3-w) |
| COV-2(X→X⁻¹, class 反転): ord(u) = ord(u⁻¹) | `true`(u⁻¹=-1/4, ord=3) |
| check-kummer(独立・factorization 不使用・obstruction 独立再判定・witness 等式独立再検算) | `MATCH`(u), `MATCH`(u⁻¹) |
| KummerCovariance3Check(GAP・GaloisCyc): τ∘[d']+κ 逆冪の同時変換で不変 | `all_match=true`(全 (Z/12)^x × (Z/6)^x = 4×2 = 8 通り) |
| check-kummer-cov3(node・独立の円分環演算・GaloisCyc 不使用): 同上の独立再検算 | `all_match=true`・GAP の kappa_table と完全一致・`MATCH` |

全 raw 出力: `certificates/k5pipeline/` 配下 12 ファイル(§5 参照)。
