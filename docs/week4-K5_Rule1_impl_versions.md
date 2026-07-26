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
| 1 | `search/u-extract-pathA.g` | 経路 A library(GAP・K[[t]] 冪級数・Hensel/Newton 持ち上げ・model_digest 計算。**便 36 で R-5: `ExtractPathA_Ninf`/`ReportToJSON_Ninf` を追加。裁定 37 対応(条件 1)で schema v2 へ production 化: `ExactPolyMul/Sub/Scale/Trim`・`PolyGcdIsUnit`・(N∞-1)–(N∞-4) の fail-closed 検査・model digest/expected digest 束縛を追加**) | `c9cb0e4ed22f76c827c9e85d94c51cdedc8b6007`(裁定37対応・未コミット) |
| 2 | `crosscheck/u-extract-pathB-lib.mjs` | 経路 B library(node・多項式係数評価・Taylor 係数のみ・級数不使用・model_digest 計算。**便 36 で R-5: `loadModelNinf`/`extractPathB_Ninf` を追加。裁定 37 対応(条件 1・3)で schema v2 へ production 化(gcd 検査・expected digest 束縛)+ `loadModel` の R-8/I-m fail-closed 修理(無条件 Weierstrass fallback バグの除去)**) | `7829b582ff4f71af35995ef54970ee39f3754588`(裁定37対応・未コミット) |
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
| 13 | `search/u-extract-pathA-ninf-toy-driver.g`(便 36 新設・R-5) | 経路 A∞・(N∞) **library unit test**(M=3・schema v2・chat=1 の passing fixture に更新 — 裁定 37 条件 1。**R-5 の production 較正ではない**、位置づけはファイル内コメントに明記) | `bce1f65d54957020795246d5fad04f10b0328905`(裁定37対応・未コミット) |
| 14 | `crosscheck/u-extract-pathB-ninf-toy-driver.mjs`(便 36 新設・R-5) | 経路 B-iii・(N∞) **library unit test**(同上・SYNTHETIC・M=3・chat=1) | `70c37e29561ad2ceaa6385207723bf122510e3b2`(裁定37対応・未コミット) |
| 17 | `search/u-extract-pathA-ninf-production-driver.g`(**裁定37新設・R-5**) | 経路 A∞・(N∞) **production 較正 driver**(M=10・Sol 提供 exact synthetic fixture・$p,a,f$ から $A,B$ をその場で導出・SYNTHETIC) | `01f6ba4058214549910be1c79ec06bdb9d99afee`(未コミット) |
| 18 | `crosscheck/u-extract-pathB-ninf-production-driver.mjs`(**裁定37新設・R-5**) | 経路 B-iii・(N∞) **production 較正 driver**(同上・独立実装・SYNTHETIC) | `d11093038fe4b0a37d98cc62b5944e9186839413`(未コミット) |

## 3. 第三 checker(照合器・crosscheck/)

| # | ファイル | 役割 | blob hash |
|---|---|---|---|
| 7 | `crosscheck/u-compare.mjs` | 経路 A/B raw の第三 checker(全フィールド一致・model_digest 独立再計算・curve_residual_zero・u≠0・u^(A)=u^(B)。**裁定 37 対応(条件 2・R-7)で expected_model_digest 束縛を追加**: 両 raw に値があれば相互一致+独立再計算 digest との一致を fail-closed に検査、K3 の凍結済み raw のように両方とも値を持たない場合は `NOT_PROVIDED (pre-bridge)` と記録し判定に使わない(K3 の既存 ACCEPT は無傷 — 再実行で確認済み)) | `aec91efababfa16dfcf46f743b0bef230e7dc871`(裁定37対応・未コミット) |
| 8 | `crosscheck/check-kummer.mjs` | Kummer 判定の独立照合器(node・factorization 不使用・別アルゴリズム・minimality obstruction 独立再判定・witness 等式独立再検算) | `d8c28b5d167e7ac90046f82dacb4a28e600c198e`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 9 | `crosscheck/check-kummer-cov3.mjs` | **撤回(便 36・下記 §9)**。旧第三 covariance 照合器(GaloisCyc 相当を node で独立再構成していたが、要求された Kummer character ではない)。dead code として残置・呼び出し停止 | `fdcf28cf28f43d937a0fb02c910649b4e8d198fa`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・無変更) |
| 10 | `crosscheck/cyclo-ring-lib.mjs` | 円分多項式の環演算(共有インフラ・#8 と旧#9 が使用・GAP コードは import しない) | `4509985e3ab269342cf182bf72c4a0f358f852b1`(commit `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd`・便36 実測) |
| 15 | `crosscheck/check-kummer-cov3-actual.mjs`(**便 36 新設**) | 第三 covariance 後継の独立照合器(node・rho_0/tau/j の実値のみで再構成・GAP スクリプトと非共有) | `a2dda3173c5f4bbb432e942559cd36e584569f5a` |
| 16 | ~~`crosscheck/u-compare-ninf-toy.mjs`~~(便 36 新設・R-5) | **裁定 37 対応で `crosscheck/u-compare-ninf.mjs`(#19)に supersede・削除**(schema v2 統一・M=3/M=10 共用の第三 checker へ一本化。旧ファイルは working tree から削除済み) | — |
| 19 | `crosscheck/u-compare-ninf.mjs`(**裁定37新設・R-5/R-7**) | 経路 A∞/B-iii の第三 checker(schema v2・M=3 unit test と M=10 production 較正の両方に使う。model_digest 相互一致+独立再計算に加え **expected_model_digest 束縛(R-7/I-l)** を fail-closed に検査) | `4a13f49ad8756416671bb4767d07b9ea826d7058`(未コミット) |
| 20 | `crosscheck/check-r5-r8-ninf-fail-closed.mjs`(**裁定37新設・R-5/R-8**) | R-5((N∞-1)–(N∞-4)・gcd・I-l)と R-8(`loadModel`/`loadModelNinf` の三値 fail-closed dispatch)の adversarial 自己確認(意図的に壊した入力が正しく throw することを実行して確認。11/11 PASS) | `6758fa1ec30ba28e293b9e2c3b79629f7d4837f3`(未コミット) |
| 21 | `crosscheck/check-covariance-envelope.mjs`(**裁定37新設・条件5**) | covariance の sealed calibration envelope(便 36 F4.2 の 3 点構成: (1) K3 actual rho0/tau/j artifact を JSON として取り込み (2) b/k の型レベル covariance(e=10・悉皆 40 通り) (3) formal a=1(Rule 1 §7.2・再導出しない)+ a_eff の d-reparametrization 不変性(悉皆 4x4x4=64 通り)) | `7a7dd50f4959ec0e1ca7021619cc4e19cea32167`(未コミット) |

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
| `certificates/k5pipeline/toy-ninf-M3-pathA.json`(便36新設・裁定37で schema v2/chat=1 に更新・SYNTHETIC unit test) | (§9 参照) |
| `certificates/k5pipeline/toy-ninf-M3-pathB.json`(同上) | (§9 参照) |
| `certificates/k5pipeline/prod-ninf-M10-pathA.json`(**裁定37新設・R-5 production・SYNTHETIC**) | (§9 参照) |
| `certificates/k5pipeline/prod-ninf-M10-pathB.json`(**裁定37新設・R-5 production・SYNTHETIC**) | (§9 参照) |
| `certificates/k5pipeline/covariance-sealed-envelope.json`(**裁定37新設・条件5**) | (§9 参照。envelope_digest はファイル内に記載) |

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
     decisive とし、第三式 E3 は **E1・E2 の両方**から自動的に従うとして
     「冗長確認」に格下げ(証明書には記録するが判定に使わない。**裁定37
     条件7前半の文言修理: 「E1 だけから」ではない**)。
  2. $\sigma_0$ が単一の 10-サイクルであることを使い、E1 を満たす $g$ は
     $g(0)$ の値一つ(10 候補)で完全に決まることを利用(cycle 上を伝播
     させて構成 — $10!$/3,628,800 通りの総当りは不要)。
  3. 定理由来の自己検査を実装(**裁定37条件7前半の文言修理**): R1-N∞-W が
     証明するのは解が**高々一つ**であること(> 1 は integrity stop・理論
     違反)。「ちょうど 1 個存在する」ことは定理から出ないので、0 survivors
     は fixture corruption 扱いしない(honest に「witness なし」と記録)。
     survivor が実在する場合は $g^2=\sigma_1$((35.6))も理論由来の
     self-check として検査する。
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

**便 36 時点(unit test のみ)**: K^(5) の実 fixture(K5-sq/K5-ns)には (N∞) 型
の dessin が存在しないため、較正は Rule 1 §0.4-3 が明示する **M=n=3 の合成
玩具族**でのみ行った(K^(5) の個別モデル・係数・数値近似ではない — 各証明書
JSON に `synthetic_note` として明記)。この時点の chat=2 玩具は Sol 便 36
F3.2 により「library の局所的な unit test としては有効だが、production
schema・(N∞-4)・gcd 検査・digest 束縛を欠く」と判定された(裁定 37 条件 1)。

**裁定 37 対応(2026-07-27)**: schema を v2 へ更新し、以下を fail-closed で
追加した。

- `ExtractPathA_Ninf`(GAP)/`extractPathB_Ninf`(node)ともに (N∞-1)–(N∞-4)
  ($\deg A=M$・$\deg B=M-3$・$b_{M-3}=a_M\ne0$・$A^2-B^2f_6$ が定数 $\hat c$・
  $\hat c=1$)を明示的に検査し、破れたら `Error`/`throw`(§9.2 I-j)。
- `gcd(f,f')$ が単元であること(f の平方非因子性)を exact 多項式演算で検査
  (GAP: `PolyGcdIsUnit`(indeterminate 上の `Gcd`)。node: 独立実装の
  Euclid 互除法)。
- 必要級数長 $\ge 2M+4$ の fail-closed 検査(`ExtractPathA_Ninf` のみ該当)。
- raw schema を三値 branch label(`branch:"N_infty"`)・`M`(旧 `n` を置換)・
  `model_digest`・`expected_model_digest` に統一。
- 旧 chat=2 の M=3 玩具は **library unit test** として schema v2 に合わせて
  更新し、位置づけを「R-5 の production 較正ではない」とファイル内コメント
  に明記(f の定数項を -1→0 に変えて chat=1 の passing fixture へ修理)。
  旧 chat=2 入力で `Error`/`throw` することは
  `crosscheck/check-r5-r8-ninf-fail-closed.mjs` で自動確認(11/11 PASS)。

**production 較正(Sol 提供 exact synthetic fixture・裁定 37 条件 1)**:
$p:=x^2+1$、$a:=1+x(x^2+1)^2$、$f:=2x+x^2(x^2+1)^2=x^6+2x^4+x^2+2x$。
$a^2-fp^2=1$($\hat c_\mu$)、$\gcd(f,f')=1$。$\lambda=\mu^2=A+By$ で
$A=2a^2-1$、$B=2ap$: $\deg A=10$、$\deg B=7$、$b_7=a_{10}=2$、
$A^2-B^2f=1$(=$\hat c$、(N∞-4) を満たす)。

- **経路 A∞**(`search/u-extract-pathA-ninf-production-driver.g`): $A,B$ を
  $a,p,f$ から `ExactPolyMul`/`ExactPolySub`/`ExactPolyScale` でその場で導出
  (手転記しない)。$s=1/x$ チャート・$W^2=F(s)$ の Hensel/Newton 持ち上げ
  (精度 $\ge s^{2M+4}=s^{24}$、実行では $s^{30}$)から
  $u^{(A)}=[s^{2M}]G_-=1/4$。(N∞-1)–(N∞-4)・$\gcd(f,f')$・digest 束縛の
  すべてが `true`。
- **経路 B-iii**(`crosscheck/u-extract-pathB-ninf-production-driver.mjs`):
  独立実装で同じ $p,a,f$ の定義から $A,B$ を再導出し、級数不使用・多項式
  演算のみで $N(\lambda)=1$・(N∞-1)–(N∞-4) 全て `true` から
  $u^{(B)}=\hat c/(2a_{10})=1/4$。
- **第三 checker**(`crosscheck/u-compare-ninf.mjs`・schema v2 統一版):
  全フィールド一致・(N∞-1)–(N∞-4)・$\gcd$・model_digest 相互一致+独立再計算・
  **expected_model_digest 束縛(R-7)**・$u^{(A)}=u^{(B)}$ の厳密等号を検査し
  `result:"ACCEPT"`($u^{(A)}=u^{(B)}=1/4$)。
- **帰結**: R-5 は production schema・(N∞-1)–(N∞-4)・gcd 検査・digest 束縛の
  すべてを M=10・$\hat c=1$ の exact synthetic fixture で通した。K^(5) 実
  データへの適用には、実 fixture が (N∞) 型を持つ場合の model literal
  (driver)を新設するだけでよく、library 本体は変更不要。

### 9.4 R-1〜R-8 の状態(裁定 38 対応後・2026-07-27)

| # | 項目 | 状態 |
|---|---|---|
| R-1 | §8.6/§10-3 の実装版・commit・checker ID | **閉**(content commit `16b18a7dc05fe94ec3b48967f1adad5a8a35013c` — 司令塔記入) |
| R-2 | 本文書+付録 A の新 digest 再取得・再提出 | **閉**(status commit 後の digest 5 本を便 38 に記載 — 司令塔取得) |
| R-3 | 親 manifest 側の whitelist/stop への反映 | **実体は閉(便37 F4.1・Sol 検分済み)**。`docs/manifest_k5_v1.md` v1.4 の whitelist・即時 stop 節はいずれも「$\hat c_\mu$ の値・平方類・平方因子・符号」の四語を逐語列挙。残る留保は operative 節への転記(便37 F4.2・単独では非 FAIL) |
| R-4 | S5 設計 §3.3.4 への N-0 追記 | **閉(2026-07-27)**(数学者・裁定36の配分どおり。§3.3.5 の次元断定は裁定37条件6でさらに「期待次元/design count」へ降格済み) |
| R-5 | (N∞) 用パイプライン拡張(経路 A∞・B-iii・構造検査) | **production 較正済み(裁定37条件1・§9.3)**。M=10・$\hat c=1$ の exact synthetic fixture で (N∞-1)–(N∞-4)・gcd・digest 束縛のすべてを通し二経路一致(ACCEPT)確認。旧 M=3 玩具は library unit test に位置づけ直し |
| R-6 | (N∞) 排除証明書の再発行(補題 R1-N∞-W) | **数学 PASS・文言修理済み(裁定37条件7前半)**。「E1 だけから」→「E1+E2 から」、「ちょうど一つ」→「高々一つ」(0 survivors は corruption 扱いしない)に修理し GAP/node とも再実行・同結果(20/20+11/11)を確認 |
| R-7 | model_digest の凍結 bundle expected digest への束縛(I-l) | **閉(便37 F2/裁定38 条件1・§9.6)**。raw 二本の自己申告 expected digest 同士の比較を、第三の独立 bundle ファイル(`build-frozen-bundles.mjs` 生成 or 凍結 model-spec)との canonical-string 逐語一致 + digest 束縛へ修理。`check-r7-bundle-attack.mjs`(5/5 PASS)で「二 driver 同一誤転記」攻撃の遮断を確認 |
| R-8 | 枝ラベルの三値 fail-closed(I-m) | **閉(便37 F3/裁定38 条件2・§9.6)**。旧 `branchP0` の大域/局所混同(Sol 便37 F3 の指摘)を `branch`(大域・$\{{\tt W},{\tt N\_aff},{\tt N\_infty}\}$)/`P0_type`(局所)の二軸へ分離し、`branch='W'⇒P0_type='nonWeierstrass'` 等の整合規則と schema 名突合を fail-closed に実装。`check-r5-r8-ninf-fail-closed.mjs` で確認(18/18 PASS) |

### 9.5 裁定 37(便 36 検収)最小 7 条件のうち実装担当分(条件 1–3・5–7)の状態

| 条件 | 内容 | 状態 |
|---|---|---|
| 1 | R-5 production 化 | 閉(§9.3・§9.4) |
| 2 | R-7(第三 checker を expected digest に束縛) | (N∞) 副枝は閉・主枝は機構配線済み/K3 は pre-bridge のため保留(§9.4) |
| 3 | R-8(loadModel 三値 fail-closed) | 閉(§9.4) |
| 4 | 親 manifest への I-b∞ 逐語反映 | 司令塔担当(範囲外)。manifest v1.4 で一部反映済み(§9.4 R-3 参照) |
| 5 | covariance の型レベル固定(sealed envelope) | 閉。`crosscheck/check-covariance-envelope.mjs` — K3 actual artifact(既存 PASS)を取り込み + b/k 型検査(e=10・40 通り悉皆)+ formal a=1(再導出せず)+ a_eff の d-reparametrization 不変性(64 通り悉皆)。envelope_digest はファイル出力を参照 |
| 6 | S5 §3.3.5 の次元降格 | 閉。`docs/week4-K5_S5設計_opus_v1.md` の「余次元 2」「次元 2」「(N) 内余次元 1」を「期待次元 2 / design count」へ一貫して降格・出典(便36 F2.2・裁定37条件6)を行内明記 |
| 7 | 文言修理 + status 同期 | 文言修理は閉(R-6 参照)。status 同期は本節+§11.1 R 表+付録 A(§10 参照)で反映。R-1・R-2 は司令塔が content commit 16b18a7 で閉鎖(本行は司令塔記入) |

### 9.6 便 37(裁定 38 検収)残 3 blocker の修理(2026-07-27・実装担当)

**対応 blocker**: 裁定_38_ben37.md の 1(R-7 外部束縛)・2(R-8 正本型)・3 前半
(covariance envelope の実配線・証明書束の清掃)。R-1/R-2・commit・最終
digest・status 文言の**最終**同期は司令塔の作業(裁定38 配分どおり)。

#### R-7(bundle 外部束縛)

- **修理**: `crosscheck/u-compare-ninf.mjs`・`crosscheck/u-compare.mjs` は
  第三引数(bundle ファイル)を**必須**にした。(N$_\infty$) 副枝は新設
  `crosscheck/build-frozen-bundles.mjs`(pathA/pathB のどちらのコードとも
  独立な第三実装 -- 有理数・多項式演算を自前で再実装)が生成する
  `certificates/k5pipeline/toy-ninf-M3-bundle.json`(mode=`calibration`)・
  `certificates/k5pipeline/prod-ninf-M10-bundle.json`(mode=`production`)。
  主枝(W/N$_{\rm aff}$)は凍結済み model-spec ファイル自身
  (`certificates/k5fixture/K3-regression-model.json`。`bridge_mode:
  "calibration_pre_bridge"` を明記 -- Freeze 2 以前で expected digest の
  事前登録がまだ無いことを型で表現する)。
- checker は (i) raw 二本から再構成した canonical model string が
  bundle の canonical model string と**逐語一致**すること、(ii) bundle
  自身の canonical string から取り直した sha256 が bundle の
  `expected_model_digest` と一致すること(bundle 自己整合)、(iii)
  production/calibration モードでは `expected_model_digest` の欠落を必ず
  INTEGRITY_STOP にすること、を検査する。raw 内の自己申告
  `expected_model_digest` は `raw_self_reported_expected_model_digest` として
  参考記録するのみで判定根拠にしない。
- **driver 側修理**(§6.3-5 item 1 完全化): 4 driver
  (`search/u-extract-pathA-ninf-{production,toy}-driver.g`・
  `crosscheck/u-extract-pathB-ninf-{production,toy}-driver.mjs`)はいずれも
  `expected_model_digest` のハードコード転記をやめ、bundle ファイルから
  読む(GAP 側は新設 `ReadJsonStringField`(`search/gaplib_common.g` 追加)
  による最小 JSON field 読取り)。
- **adversarial 較正(新設)**: `crosscheck/check-r7-bundle-attack.mjs`。
  Sol 便37 F2 が明記した攻撃(「両 driver が同じ誤ったモデルを転記し、
  同時に expected_model_digest = digest(誤モデル) を入れれば ACCEPT する」)
  を実際に構成し、正しい bundle と照合すると INTEGRITY_STOP になることを
  確認(5/5 PASS)。対照実験として、bundle 側も同じ誤りに合わせれば
  ACCEPT することも確認(機構が「モデルが正しいか」ではなく
  「bundle と raw の bytes が一致するか」を検査していることの裏付け)。

#### R-8(branch/P0_type 分離)

- **修理**: `crosscheck/u-extract-pathB-lib.mjs`(`loadModel`/
  `canonicalModelString`/`extractPathB`)・`search/u-extract-pathA.g`
  (`ExtractPathA`/`PathA_CanonicalModelString`/`ReportToJSON`)の main-path
  schema を v2→**v3** へ上げ、旧 `branchP0` を大域 `branch`
  ($\{{\tt W},{\tt N\_aff}\}$。$N_\infty$ はこのスキーマでは不正 -- 別
  loader を使うこと)と局所 `P0_type`($\{{\tt Weierstrass},{\tt
  nonWeierstrass}\}$)へ分離。整合規則: `branch='W'` は
  `P0_type='nonWeierstrass'` を要求(S5-W 補題・Rule 1 SS4.1「v1.2 の
  絞り込み」)、`branch='N_aff'` のみ両値を許す(「$P_0$ も Weierstrass」が
  発火しうるのは副枝 (N$_{\rm aff}$) だけ -- Rule 1 同節)。$N_\infty$
  schema(`loadModelNinf`/`ExtractPathA_Ninf`)にも `P0_type` field を追加
  (常に `'nonWeierstrass'` -- 補題 R1-M0 3.、与えられれば fail-closed に
  検査)。
- 第三 checker(`u-compare.mjs`/`u-compare-ninf.mjs`)は raw の `schema`
  文字列(`u-pathA/v3`・`u-pathB/v3`・`u-pathA-ninf/v2`・
  `u-pathB-ninf/v2`)を許可リストと突合し、`branch`/`P0_type` の整合規則
  も再検査する(I-m)。
- model-spec ファイル(`certificates/k5fixture/K3-regression-model.json`)も
  同じ field 名(`branch`/`P0_type`)へ改名。
- **F1.2 清掃(便37 が指摘した schema field の明示値化)**: (N$_\infty$)
  raw に `a_M`・`b_Mm3` の明示値フィールドを追加(pathA/pathB とも)。
- **adversarial 較正**: `crosscheck/check-r5-r8-ninf-fail-closed.mjs` に
  `branch='W'`+`P0_type='Weierstrass'` の拒否・`branch='N_aff'`+
  `P0_type='Weierstrass'` の受理・`P0_type` 欠落/不正値の拒否などを追加し
  18/18 PASS(旧 11/11 から拡張)。

#### covariance envelope の実配線(F5)

- `crosscheck/covariance-lib.mjs`(新設)へ `computeAEff`/`invMod`/
  `mulMod`/`unitsMod`/`gcd`/`restrict10to5` を切り出し、
  `crosscheck/check-covariance-envelope.mjs` と新設
  `crosscheck/covariance-bridge-in.mjs`(橋段 driver スタブ -- CLI 引数
  `<b_sq> <b_ns>` を受け取り同じ `computeAEff` を呼ぶ。未配線時は
  `BRIDGE-UNKNOWN` を正直に返し fail-open しない)の**両方**が import する。
- **formal a の実読取り**(便37 F5.2 (1)): `FORMAL_A` のハードコードをやめ、
  `certificates/k5fixture/K5-sq.json`/`K5-ns.json` の
  `rho0_and_j.a_sealed` を読み、両 fixture の値が一致することを
  fail-closed に検査してから使う。
- **source digest 束縛**(便37 F5.2 (2)): K3 covariance artifact
  (`K3-regression-kummer-cov3-actual.json`)・K5-sq/K5-ns fixture の
  **ファイル全体**の SHA-256 を envelope へ記録する(従来は conclusion
  抜粋のみで、source の他部分が変わっても同じ envelope digest になり
  得た)。
- **段階の文言訂正**(便37 F5.2 (4)): 「実 $b_i$ は atomic Freeze 2
  **受理後**に代入」という誤記を「**受理前**・$u$ 開示前」へ訂正
  ($b_{\rm sq}=b_{\rm ns}$ は受理条件そのものであり、受理後に代入する
  ものではない)。
- **明示的な component/件数 assert**(便37 F5.2 (5)): `sealed` は
  従来 `pass > 0` だったが、`components_present === 3`・
  `covk_combinations_actual === 40`・`aeff_combinations_actual === 64`・
  `a_sealed(sq) === a_sealed(ns)` を明示的に assert する形へ強化。
  schema を `k5pipeline/covariance-sealed-envelope/v2` へ上げ、
  再実行して `sealed=true`・`envelope_digest =
  3a8fb77c727c4ad31270ccfa1b1ccff51ea1a6160baf7c6d6aaed35d1bb31b5a`
  を得た。

#### 証明書束の清掃(F1.2・裁定38条件3後半)

- `certificates/k5pipeline/toy-ninf-M3-u-compare.json`(旧 schema v1・
  $u=1$ の陳腐化した値)→ `retracted/toy-ninf-M3-u-compare.v1.json` へ退避
  し、現行 checker(bundle 引数つき)で再発行。
- `certificates/k5pipeline/K3-regression-cov1-k2-u-compare.json`(旧
  `u-compare.mjs` 2 引数版・schema v2)→
  `retracted/K3-regression-cov1-k2-u-compare.v2.json` へ退避。COV-1 派生
  モデルは driver コメントに明記のとおり「較正のみの参考出力・パイプライン
  の入力に使わない」ため、bundle 必須の新 checker では再発行しない(退避
  理由は `certificates/k5pipeline/retracted/NOTE.md` 追記済み)。
- `prod-ninf-M10-u-compare.json`(未保存だった production 較正の第三
  checker 出力)を新規保存。
- (N$_\infty$) raw に `a_M`/`b_Mm3` の明示値を追加(上記 R-8 節参照)。

#### 変更・新設ファイル一覧(blob hash・`git hash-object`・2026-07-27 実測・未コミット)

| ファイル | 種別 | blob hash |
|---|---|---|
| `search/u-extract-pathA.g` | library(R-8 分離・schema v3) | `6e30fd91897d4a91455bfc4d0449a281f7073bfa` |
| `crosscheck/u-extract-pathB-lib.mjs` | library(R-8 分離・schema v3) | `7b7263498a96e0431eca940b2bc57520d5852a08` |
| `crosscheck/u-compare.mjs` | 第三 checker(R-7 bundle 化・R-8 突合・schema v3) | `7f623a64669615099d25d071eef8cad639df3734` |
| `crosscheck/u-compare-ninf.mjs` | 第三 checker(R-7 bundle 化・schema v3) | `797dc48a652bee0c184a1deed46572257387b783` |
| `crosscheck/check-r5-r8-ninf-fail-closed.mjs` | adversarial 較正(拡張・18/18) | `fa6ceb49e68c421314b5e38c893859cae9624ef4` |
| `crosscheck/check-r7-bundle-attack.mjs`(新設) | adversarial 較正(R-7 攻撃再現・5/5) | `204ecb37e023955943021856873454ead1094d89` |
| `crosscheck/build-frozen-bundles.mjs`(新設) | 独立 bundle 生成器 | `d2a37fd630c38f3156e73c7a3b29324a2509af47` |
| `crosscheck/covariance-lib.mjs`(新設) | 共有 covariance library | `690de2e5c910cdce6a1bb1f774eecbec1fda684f` |
| `crosscheck/covariance-bridge-in.mjs`(新設) | 橋段 driver スタブ | `9fc7b9a12bc7487b29b8f3f0ae9a1b0dc10d2a79` |
| `crosscheck/check-covariance-envelope.mjs` | covariance envelope(実配線・v2) | `7bdee13dcecee6f417c5cb24364a1c3ab9b88fd5` |
| `search/gaplib_common.g` | 共通 GAP infra(`ReadJsonStringField` 追加) | `12fb309d83721744dcc764969133a6e8257ffa12` |
| `search/u-extract-pathA-k3-driver.g` | K3 較正 driver(field 名更新) | `ae54238485ab58b235af939f876062081cb777bb` |
| `crosscheck/u-extract-pathB-k3-driver.mjs` | K3 較正 driver(無変更) | `979a227866bc70f02e408765b98172a8f7708223` |
| `search/u-extract-pathA-ninf-production-driver.g` | production driver(bundle 読取り化) | `a33b52a2fc289f0e9d5e22c06ffbd1e6f1c6a8d1` |
| `crosscheck/u-extract-pathB-ninf-production-driver.mjs` | production driver(bundle 読取り化) | `99e160cc2d278f9ebabda18542d4f4cf5be7618d` |
| `search/u-extract-pathA-ninf-toy-driver.g` | toy driver(bundle 読取り化) | `6e08cfc7211c0b0b1fe0659ff0dedcbb261c8d9b` |
| `crosscheck/u-extract-pathB-ninf-toy-driver.mjs` | toy driver(bundle 読取り化) | `85b65ab876a0bd8ec40c2ab2c8733fdefcc9b898` |
| `certificates/k5fixture/K3-regression-model.json` | model-spec(field 名更新・bridge_mode 追加) | `9d6c5c0fe359d6701ea0711557a5b1d51f95e777` |

**全較正の再実行結果(2026-07-27)**:

- K3 回帰(主枝): `node crosscheck/u-compare.mjs
  certificates/k5pipeline/K3-regression-u-pathA.json
  certificates/k5pipeline/K3-regression-u-pathB.json
  certificates/k5fixture/K3-regression-model.json` → `result: "ACCEPT"`
  (`u=-4`・`expected_digest_check: "NOT_PROVIDED (calibration_pre_bridge,
  explicit ...)"`)。
- synthetic M=10 production((N$_\infty$)): `u-compare-ninf.mjs` →
  `result: "ACCEPT"`(`u=1/4`・`bundle_mode: "production"`・
  `expected_digest_check: "BOUND (bundle-external, ...)"`)。
- synthetic M=3 unit test((N$_\infty$)): 同上 → `result: "ACCEPT"`
  (`u=1/2`・`bundle_mode: "calibration"`)。
- `check-r5-r8-ninf-fail-closed.mjs`: **18/18 PASS**。
- `check-r7-bundle-attack.mjs`: **5/5 PASS**。
- `check-covariance-envelope.mjs`: `sealed=true`・
  `envelope_digest=3a8fb77c727c4ad31270ccfa1b1ccff51ea1a6160baf7c6d6aaed35d1bb31b5a`。
