# Rule 1 抽出・判定パイプライン 実装版一覧

2026-07-27 実装(implementer)。委嘱: 便 32 P6 後半(司令塔発注)。仕様正本:
`docs/week4-K5_Rule1_v1.md` §6(u の二経路)・§8(exact Kummer 判定器)。

## 0. 身分

本文書は §8.6「版の固定」の実体化である。**この時点ではまだ `git commit` していない**
(委嘱の規律「git commit しない」に従う)。したがって以下のハッシュは
`git log -1 --format=%H -- <file>` ではなく `git hash-object <file>`
(working tree のバイト内容から算出される blob ハッシュ)を暫定値として記録する。
凍結時に実際に commit した後、この文書は commit ID(`git log -1 --format=%H`)へ
差し替える必要がある(**値は現時点では pending**)。

## 1. 実装ファイルと版

| # | ファイル | 役割 | blob hash (git hash-object・2026-07-27 時点) |
|---|---|---|---|
| 1 | `search/u-extract-pathA.g` | 経路 A(GAP・K[[t]] 冪級数・Hensel/Newton 持ち上げ) | `c01eb5273f41d376fe0ba38477d778231b52693d` |
| 2 | `crosscheck/u-extract-pathB.mjs` | 経路 B(node・多項式係数評価・Taylor 係数のみ・級数不使用) | `1138f62224fe0086b2c22387a80ef37109df7040` |
| 3 | `crosscheck/u-compare.mjs` | 第三 checker(raw JSON 二つの厳密突合のみ) | `cb2a535f805e06baf39c87e896c92c661fa546b8` |
| 4 | `search/kummer-decide.g` | exact Kummer 判定器(GAP・`AlgebraicExtension` 上 `Factors`) | `b64102588c18a2353e51718c0f3be529ff3eb8cf` |
| 5 | `crosscheck/check-kummer.mjs` | Kummer 判定の独立照合器(node・factorization 不使用・別アルゴリズム) | `c3f16a8ffc4b2b78f22c0a54c1850f0177f82965` |
| 6 | `certificates/k5fixture/K3-regression-model.json` | K3-regression の派生 `y^2=f(x)` モデル(model-spec/v1) | `d4b5c60aa362b010446e8f0add7fc4f842640a58` |

## 2. 実行環境版

- GAP: 4.16.0(`C:\Program Files\GAP-4.16.0`、実行は `gap.ps1` 経由・`-o 2g`)。
- node: v24.16.0。
- 数体演算ライブラリ: GAP 組み込み `Cyclotomics` / `AlgebraicExtension`(外部パッケージ不使用)。
- 因数分解アルゴリズム: GAP 組み込み `Factors`(体は `AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals, n))` として構成 -- §3 の罠参照)。
- イデアル分解アルゴリズム: 本実装では未使用(obstruction は (O-b)/(O-c) のみ実装。(O-a) は今回のスコープ外)。

## 3. 実装上の発見(罠・報告事項)

**GAP の `CF(n)` は `Factors` に対して体として正しく振る舞わない。**

`Indeterminate(CF(12), "T")` 上で `T^2+4` を `Factors` にかけると `[T^2+4]`
(既約)と誤って返す。しかし `Value(T^2+4, 2*E(4))` = 0(2i は明らかに根)であり、
`2*E(4) in CF(12)` は `true`。すなわち `CF(n)` は「乗法群を含む Cyclotomics の
緩い collection」であって、`Factors` はその上で有理係数の範囲でしか分解を
試みず、非有理な(が K の元である)根を見逃す。

正しい構成は `AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals, n))`
で体として認識させること。実測: この構成では `T^2+4` を正しく
`(T-2a^3)(T+2a^3)` に分解する(`a` = 定義多項式の根)。`search/kummer-decide.g`
はこの構成を正本として採用している。**もし他のスクリプトが `CF(n)` 上で直接
`Factors` を呼んでいるなら、その結果は非有理根の見逃しにより信頼できない
可能性がある**(今回の便では新規 2 ファイルのみでこの罠を踏んだが、既存の
GAP スクリプト全体をこの観点で棚卸しする価値があるかもしれない -- 司令塔判断)。

## 4. K3 regression fixture 較正結果(§6.4/§8.3 raw 再計算)

`certificates/k5fixture/K3-regression.json`(既存・司令塔管理下)に記録された
既知値 u=−4・ord([u⁻¹]₆)=3 を、モデルからの raw 再計算として全パイプラインで
再現した(期待値のハードコード比較ではなく、モデル係数から独立に再導出)。

| 検査 | 結果 |
|---|---|
| 経路 A: u_pathA (K3-regression) | `-4` |
| 経路 B: u_pathB (K3-regression) | `-4` |
| 第三 checker: u^(A) = u^(B) | `ACCEPT` |
| COV-1(s→cs, k=2 の M2 残余群作用モデル): u_pathA | `-1/1024` |
| COV-1: u_pathB | `-1/1024` |
| COV-1: 第三 checker | `ACCEPT` |
| COV-1: u_cov1/u_base = k^(-2M) の厳密検算 | `1/4096 = 1/4096` 一致 |
| kummer-decide: ord(u=-4) mod 6 | `3`(witness 明示、`e^6=u` 検算込み) |
| COV-2(X→X⁻¹, class 反転): ord(u) = ord(u⁻¹) | `true`(u⁻¹=-1/4, ord=3) |
| check-kummer(独立照合・factorization 不使用): ord(u), ord(u⁻¹) | `MATCH`, `MATCH` |

全 raw 出力: `certificates/k5fixture/K3-regression-u-pathA.json`,
`K3-regression-u-pathB.json`, `K3-regression-cov1-k2-u-pathA.json`,
`K3-regression-cov1-k2-u-pathB.json`, `K3-regression-kummer-u.json`,
`K3-regression-kummer-uinv.json`。
