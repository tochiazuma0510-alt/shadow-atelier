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

本文書は §8.6「版の固定」の実体化である。**便 36 時点で訂正(自己申告の
陳腐化・便 35 F4 と同型の欠陥を自己点検で発見)**: v2 起草時点(便 34)の
「まだ git commit していない」という記述は、**§2-§4 のドライバ・checker・
fixture ファイルについては便 36 の時点で既に事実と異なっていた**
(`git log -1 --format=%H -- <path>` が commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`
を返し、working tree と `git status`/`git diff` の差分が無いことを実測で
確認 — つまりこれらのファイルは司令塔により commit 済みだったが、本文書の
プローズは「未コミット」のまま更新されていなかった)。**§1 の library
3 ファイルは本便(便 36)の編集により working tree が commit 済み内容から
再び変化しており、これらは実際に現時点で未コミットである**(実装担当は
git commit しない規律のため)。したがって:
- §2–§4(driver・checker・fixture、便 36 で変更していないもの)は
  **commit ID を値として記入**(下表)。
- §1(library、便 36 で変更したもの)・§9 の便 36 新設ファイルは
  blob hash のみ(`git hash-object`)を記録し、commit ID は司令塔の commit
  後に本表を更新する。commit しても blob hash 自体は変わらない。

## 1. library ファイル(凍結対象)

| # | ファイル | 役割 | blob hash (`git hash-object`, 2026-07-27) |
|---|---|---|---|
| 1 | `search/u-extract-pathA.g` | 経路 A library(GAP・K[[t]] 冪級数・Hensel/Newton 持ち上げ・model_digest 計算。**便 36 で R-5: `ExtractPathA_Ninf`/`ReportToJSON_Ninf` を追加**) | `e0bf9c72844bf4e88b9e4385a15b79fd576f189c`(便36) |
| 2 | `crosscheck/u-extract-pathB-lib.mjs` | 経路 B library(node・多項式係数評価・Taylor 係数のみ・級数不使用・model_digest 計算。**便 36 で R-5: `loadModelNinf`/`extractPathB_Ninf` を追加**) | `b4ba23f63c4255ab29ee6c31516c0820808bf999`(便36) |
| 3 | `search/kummer-decide.g` | exact Kummer 判定器 library(GAP・`AlgebraicExtension` 上 `Factors`・minimality obstruction 収集。**`KummerCovariance3Check` は便 36 で撤回(dead code として残置・呼び出し停止 — 下記 §9 参照)**) | `47d49f97ec53c3b3e342434ab058663861ffd5e3`(便36) |
| 12 | `search/kummer-cov3-actual.g`(**便 36 新設**) | 第三 covariance 後継 library+driver(rho_0/tau/j の実値 covariance のみ・射程限定を明記 — 下記 §9) | `32f800a3edf2fd1e2bf46c8d0377ff37c9c99e07` |

## 2. driver ファイル(K3 較正専用・凍結対象ではない)

将来の K5 driver は library を変更せず、以下と同型の新しい driver ファイル
を追加する。

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 4 | `search/u-extract-pathA-k3-driver.g` | 経路 A・K3 較正 driver(model literal・実行・QUIT) | `99875a3bcbae08825217e83aef55ee46c22d3778`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 5 | `crosscheck/u-extract-pathB-k3-driver.mjs` | 経路 B・K3 較正 driver | `979a227866bc70f02e408765b98172a8f7708223`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 6 | `search/kummer-decide-k3-driver.g` | Kummer 判定器・K3 較正 driver(RunK3Calibration。**便 36 で covariance-3 呼び出しを削除 — 下記 §9**) | `d7f1b9a436a6340e0a2136945e5c6295295c0318`(便36) |
| 13 | `search/u-extract-pathA-ninf-toy-driver.g`(**便 36 新設・R-5**) | 経路 A∞・(N∞) 玩具較正 driver(Rule 1 §0.4-3 の M=n=3 玩具族・SYNTHETIC) | `415491c64e0dc9c8b63b7c87fcde2468e859d0bd` |
| 14 | `crosscheck/u-extract-pathB-ninf-toy-driver.mjs`(**便 36 新設・R-5**) | 経路 B-iii・(N∞) 玩具較正 driver(同上・SYNTHETIC) | `b635401961469281a7ab9e2d14a46519a5a71609` |

## 3. 第三 checker(照合器・crosscheck/)

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 7 | `crosscheck/u-compare.mjs` | 経路 A/B raw の第三 checker(全フィールド一致・model_digest 独立再計算・curve_residual_zero・u≠0・u^(A)=u^(B)) | `7f64ac0229d35850e64f63557ea9bd5f164a0d03`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 8 | `crosscheck/check-kummer.mjs` | Kummer 判定の独立照合器(node・factorization 不使用・別アルゴリズム・minimality obstruction 独立再判定・witness 等式独立再検算) | `d8c28b5d167e7ac90046f82dacb4a28e600c198e`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 9 | `crosscheck/check-kummer-cov3.mjs` | **撤回(便 36・下記 §9)**。旧第三 covariance 照合器(GaloisCyc 相当を node で独立再構成していたが、要求された Kummer character ではない)。dead code として残置・呼び出し停止 | `fdcf28cf28f43d937a0fb02c910649b4e8d198fa`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・無変更) |
| 10 | `crosscheck/cyclo-ring-lib.mjs` | 円分多項式の環演算(共有インフラ・#8 と旧#9 が使用・GAP コードは import しない) | `4509985e3ab269342cf182bf72c4a0f358f852b1`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 15 | `crosscheck/check-kummer-cov3-actual.mjs`(**便 36 新設**) | 第三 covariance 後継の独立照合器(node・rho_0/tau/j の実値のみで再構成・GAP スクリプトと非共有) | `a2dda3173c5f4bbb432e942559cd36e584569f5a` |
| 16 | `crosscheck/u-compare-ninf-toy.mjs`(**便 36 新設・R-5**) | 経路 A∞/B-iii 玩具較正の第三 checker(SYNTHETIC) | `0910df0b7f10e7e5b7d40a839f8325274bc2a1b9` |

## 4. fixture

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 11 | `certificates/k5fixture/K3-regression-model.json` | K3-regression の派生 `y^2=f(x)` モデル(model-spec/v1・無変更) | `d4b5c60aa362b010446e8f0add7fc4f842640a58`(commit `f35e7e69bb00ec135019ef579fc7cd81ec5359ba`・便36 実測) |

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
| ~~`certificates/k5pipeline/K3-regression-kummer-cov3.json`~~ | **撤回(便 36)** → `certificates/k5pipeline/retracted/K3-regression-kummer-cov3.v1.json` |
| ~~`certificates/k5pipeline/K3-regression-kummer-cov3-checkcov3.json`~~ | **撤回(便 36)** → `certificates/k5pipeline/retracted/K3-regression-kummer-cov3-checkcov3.v1.json` |
| `certificates/k5pipeline/K3-regression-kummer-cov3-actual.gap.json`(便36新設) | (GAP raw・§9 参照) |
| `certificates/k5pipeline/K3-regression-kummer-cov3-actual.json`(便36新設) | (node raw+cross-check・§9 参照) |
| `certificates/k5pipeline/ninf-exclusion.gap.json`(便36で v2 に更新) | (§9 参照) |
| `certificates/k5pipeline/ninf-exclusion.json`(便36で v2 に更新) | (§9 参照) |
| `certificates/k5pipeline/toy-ninf-M3-pathA.json`(便36新設・R-5・SYNTHETIC) | (§9 参照) |
| `certificates/k5pipeline/toy-ninf-M3-pathB.json`(便36新設・R-5・SYNTHETIC) | (§9 参照) |
| `certificates/k5pipeline/toy-ninf-M3-u-compare.json`(便36新設・R-5・SYNTHETIC) | (§9 参照) |

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
| ~~KummerCovariance3Check(GAP・GaloisCyc): τ∘[d']+κ 逆冪の同時変換で不変~~ | **撤回(便36・下記 §9)** |
| ~~check-kummer-cov3(node・独立の円分環演算・GaloisCyc 不使用): 同上の独立再検算~~ | **撤回(便36・下記 §9)** |

全 raw 出力: `certificates/k5pipeline/` 配下(§5 参照。cov3 の 2 ファイルは §9 の後継に置換)。

---

## 9. 便 36(裁定 36_ben35)の修理 — Sol 便 35(`sol/sol_reply_35_freeze1r4.md`)対応

**背景**: 便 35 F1.5 は `search/k5-ninf-exclusion.g`/`crosscheck/check-k5-ninf.mjs`
(v1)が誤った Nielsen 変換((35.2) の素朴交換)を検査していたと指摘し、F3 は
`KummerCovariance3Check`/`crosscheck/check-kummer-cov3.mjs` が要求された
Kummer character(`G_K` 上の `kappa_w(gamma)=gamma(w^{1/M})/w^{1/M}`)ではなく
`Gal(K/Q)` の `K` 内自己同型(`GaloisCyc`)を検査していたと指摘した。裁定
36_ben35 は両者の撤回と再実装、および R-5((N∞) パイプライン拡張)を実装へ
配分した。

### 9.1 (N∞) 排除証明書の再実装(v1 → v2 → v3)

- v2: `search/k5-ninf-exclusion.g` / `crosscheck/check-k5-ninf.mjs` を、正しい
  述語 (35.4)(`g s0 g^-1 = sInf`・`g s1 g^-1 = s1`・
  `g sInf g^-1 = s1^-1 s0 s1`)で書き直した(全 $S_{10}$ を検査する
  `RepresentativeAction`/brute force 3,628,800 通り)。
- **v3(司令塔中継・Rule 1 v1.3 補題 R1-N∞-W の反映)**: 数学者検分済み仕様に
  従い書き直し。
  1. 判定述語は (35.4) の E1(`g s0 g^-1=sInf`)・E2(`g s1 g^-1=s1`)のみを
     decisive とし、第三式 E3 は E1 から自動的に従うとして「冗長確認」に
     格下げ(証明書には記録するが判定に使わない)。
  2. $\sigma_0$ が単一の 10-サイクルであることを使い、E1 を満たす $g$ は
     $g(0)$ の値一つ(10 候補)で完全に決まることを利用(cycle 上を伝播
     させて構成 — $10!$/3,628,800 通りの総当りは不要)。
  3. 定理由来の自己検査を実装: 各 fixture でちょうど 1 個の survivor(破れ
     たら integrity stop・UNKNOWN ではない)・$g^2=\sigma_1$((35.6))。
  4. 旧述語 (35.3) の撤回を自己完結化: $\sigma_0\sigma_1\ne\sigma_1\sigma_0$
     を直接計算で確認し、(35.3) が E1 のもとで (35.4)∧$[\sigma_0,\sigma_1]=1$
     と同値かつ恒真に充足不能であることを証明書内で示した。
- 結果: **両 fixture(sq/ns)で `ninf_excluded=false`**。Sol (35.5) の witness
  `g_sq=[1,0,3,8,5,6,7,4,9,2]`・`g_ns=[6,3,2,7,8,1,4,5,0,9]` を GAP・node の
  二系統(いずれも独立な 10-候補法の実装)が確認し、`g^2 = sigma_1`
  ((35.6))も両系統で確認した(GAP 20/20 PASS・node 20/20 PASS・
  cross-check 11/11 PASS)。結論札: 「排除されず・対称性充足・(N$_\infty$)
  の存否は UNKNOWN・witness は cross-checked」。
- 旧証明書(`ninf_excluded=true` の誤結論)は `certificates/k5pipeline/retracted/`
  へ退避(`ninf-exclusion.gap.v1.json`・`ninf-exclusion.v1.json`・
  理由は同ディレクトリの `NOTE.md`)。
- **帰結**: R-4/R-5/R-6 は launch blocker に復帰(裁定36どおり)。R-6 は
  上記のとおり実装済(数学者検分待ち)。

### 9.2 第三 covariance の再実装

- 旧 `KummerCovariance3Check`(`search/kummer-decide.g`)・
  `crosscheck/check-kummer-cov3.mjs` は撤回(dead code として残置・呼び出し
  停止。`search/kummer-decide-k3-driver.g` から呼び出し箇所を削除)。
- 後継: `search/kummer-cov3-actual.g` + `crosscheck/check-kummer-cov3-actual.mjs`。
  K3 fixture の実値(`certificates/k5fixture/K3-regression.json`
  `tau_rho0_j_orientation` ブロックの `rho_0` 生成元像・`tau` 生成元作用・
  `j` の表)のみを入力に、生成元の取り替え `zeta_6[3] -> zeta_6[3]^{d'}`
  (`d' in (Z/3)^x = {1,2}`)の下で `j` の対応表が transformation law
  `t' = d'^{-1} t (mod 3)` のとおりに独立再構成できることを、置換の実値
  等式として検査した。結果: GAP 6/6 PASS・node 6/6 PASS・cross-check 5/5
  PASS・`all_covariance_match=true`(両 `d'` で一致)。
- **射程の限定(UNKNOWN として申告・弱めていない)**: 実測の `b_i`(Rule 1
  §7.1: 実際の局所モノドロミー生成元 `ell_i` と FC-3 intertwiner `c_i` から
  測る量)は、K3 fixture に証明書として存在しないため実装できない
  (K3 の `tau` は局所 Kummer 規約 `s^{1/M}->zeta_M s^{1/M}` から直接定義され
  ており、`b=1` はこの構成では定義上のものであって独立測定値ではない)。
  formal `a=1`(Rule 1 (1.11))は K5 の sq/ns 比較指数であり K3 単体の
  dessin には定義されないため再導出していない。詳細は
  `certificates/k5pipeline/retracted/NOTE.md` 後半・各証明書の
  `scope_limitation_UNKNOWN` フィールドを参照。この二点は司令塔/数学者
  レイヤーへの差し戻し事項である。

### 9.3 R-5: (N∞) 用パイプライン拡張(経路 A∞・B-iii)— SYNTHETIC 較正

K^(5) の実 fixture(K5-sq/K5-ns)には (N∞) 型の dessin が存在しないため、
較正は Rule 1 §0.4-3 が明示する **M=n=3 の合成玩具族**でのみ行った(K^(5)
の個別モデル・係数・数値近似ではない — 各証明書 JSON に `synthetic_note`
として明記)。

- 玩具構成: $A_3(x):=x^3+x+1$(モニック 3 次)、$\hat c:=2$、
  $f_6:=A_3(x)^2-\hat c$、$B(x):=1$、$\lambda:=A_3(x)+y$。$f_6$ の平方非因子性
  (6 根が相異なる)は Durand–Kerner 数値根探索で事前確認(最小根間距離
  約 0.80・非公式チェック)。
- **経路 A∞**(`search/u-extract-pathA.g` の `ExtractPathA_Ninf` +
  `search/u-extract-pathA-ninf-toy-driver.g`): $s=1/x$ チャート・
  $W^2=F(s)$・$W(0)=1$ の Hensel/Newton 持ち上げ(精度 $s^{2n+4}=s^{10}$)から
  $u^{(A)}=[s^{2n}]G_-=1$。$W^2=F$ 検算・下位次数消滅検算とも `true`。
- **経路 B-iii**(`crosscheck/u-extract-pathB-lib.mjs` の `extractPathB_Ninf` +
  `crosscheck/u-extract-pathB-ninf-toy-driver.mjs`): 級数不使用・多項式
  演算のみで $N(\lambda)=A^2-B^2f_6=\hat c=2$(定数・非零)・$\deg A=n=3$・
  $b_{n-3}=a_n=1$(構造検査 (N∞-1)(N∞-2)(N∞-3) 相当・全て `true`)から
  $u^{(B)}=\hat c/(2a_n)=1$。
- **第三 checker**(`crosscheck/u-compare-ninf-toy.mjs`): 全フィールド一致・
  構造検査・$u^{(A)}=u^{(B)}$ の厳密等号を検査し、**`result:"ACCEPT"`**
  ($u^{(A)}=u^{(B)}=1$)。
- **帰結**: 経路 A∞/B-iii/第三 checker の実装・二経路一致は合成玩具例で
  較正済み。K^(5) 実データへの適用には、実 fixture が (N∞) 型を持つ場合の
  model literal(driver)を新設するだけでよく、library(`ExtractPathA_Ninf`/
  `extractPathB_Ninf`)自体は変更不要。

### 9.4 R-1〜R-5 の状態(便 36 時点)

| # | 項目 | 状態(便36 時点) |
|---|---|---|
| R-1 | §8.6/§10-3 の実装版・commit・checker ID | 本表が blob hash として維持(**git commit は司令塔の作業 — 実装担当は commit しない規律**。commit 後の `git log` 差し替えは司令塔 P7) |
| R-2 | 本文書+付録 A の新 digest 再取得・再提出 | 未(司令塔 P7・本便のテキスト変更を含め再取得要) |
| R-3 | 親 manifest 側の whitelist/stop への反映 | 別便(司令塔 P1+P3・実装担当の範囲外) |
| R-4 | S5 設計 §3.3.4 への N-0 追記 | 未(数学者・実装担当の範囲外 — 裁定36の配分どおり) |
| R-5 | (N∞) 用パイプライン拡張(経路 A∞・B-iii・構造検査) | **実装済(便36・§9.3)**。SYNTHETIC 較正で二経路一致(ACCEPT)確認 |
