# retracted/ — 撤回済み証明書

## ninf-exclusion.gap.v1.json / ninf-exclusion.v1.json

**撤回日**: 便 36(裁定 36_ben35・実装担当)。

**撤回理由**: `search/k5-ninf-exclusion.g` v1 と `crosscheck/check-k5-ninf.mjs` v1 は、
(0 ∞)-交換の monodromy 三つ組への移し方として素朴な置換

```
(x, y, z) |-> (z, y, x)                                            (35.2)
```

を検査していた。これは正本の relator `x y z = 1` を一般に保たない
(`z y x = 1` は `x y z = 1` から従わない) ため誤った述語である
(Sol 便 35 = `sol/sol_reply_35_freeze1r4.md` F1.5 の指摘)。

正しい (0 ∞)-交換の Out(π₁) 代表は Nielsen 変換

```
beta(x) = z,  beta(y) = y,  beta(z) = y^-1 x y                     (35.1)
```

であり、simultaneous conjugation のレベルでは

```
g sigma_0    g^-1 = sigma_infty
g sigma_1    g^-1 = sigma_1
g sigma_infty g^-1 = sigma_1^-1 sigma_0 sigma_1                    (35.4)
```

を満たす g ∈ S₁₀ の存在として現れる。v1 はこの第三式を「σ₀ との単純交換」
として誤って検査していた。

**帰結**: v1 は両 fixture(sq/ns)で `ninf_excluded=true` と結論していたが、
これは撤回する。正しい述語 (35.4) では、Sol が (35.5) で提示した witness

```
g_sq = [1,0,3,8,5,6,7,4,9,2]
g_ns = [6,3,2,7,8,1,4,5,0,9]
```

(0-indexed one-line) が両 fixture で実際に (35.4) を満たし、かつ
`g^2 = sigma_1` (35.6) も満たすことを、v2(`search/k5-ninf-exclusion.g`・
`crosscheck/check-k5-ninf.mjs` の現行版)が GAP RepresentativeAction と
node 総当りの二系統で確認している(`certificates/k5pipeline/ninf-exclusion.json`
の現行版を参照)。したがって現行の結論は

**「両 fixture について (N_∞) は排除されていない(witness 記録済み)」**

であり、R-4/R-5(Rule 1 v1.2 §11.1)は launch blocker に復帰する
(裁定 sol/裁定_36_ben35.md)。

**裁定根拠**: `sol/sol_reply_35_freeze1r4.md` F1.5・`sol/裁定_36_ben35.md`。

**追記(v3・司令塔中継の補題 R1-N∞-W 反映)**: (35.3) がなぜ充足不能かの直接
説明: E1(`g sigma_0 g^-1 = sigma_infty`)のもとで、(35.3) の第三式
(`g sigma_infty g^-1 = sigma_0`)は (35.4) の第三式
(`g sigma_infty g^-1 = sigma_1^-1 sigma_0 sigma_1`)と比較すると
`sigma_0 = sigma_1^-1 sigma_0 sigma_1`、すなわち **`sigma_0` と `sigma_1`
の可換性**を要求する。両 fixture で `sigma_0*sigma_1 <> sigma_1*sigma_0`
を直接計算で確認済み(現行 `search/k5-ninf-exclusion.g`/
`crosscheck/check-k5-ninf.mjs` の `sigma0_sigma1_commute` フィールド)。
ゆえに (35.3) は **E1 のもとで恒真に充足不能**であり、v1 が「conjugator が
見つからない」と結論したのは正しい計算だったが、それは的外れな問いへの
答えであって (N∞) の排除ではなかった。

現行版(v3)はさらに司令塔中継の数学者検分済み仕様(補題 R1-N∞-W)に従い、
判定述語を (35.4) の第一・第二式(E1・E2)のみに絞り(第三式は E1 から
自動的に従うので「冗長確認」として記録するのみ)、`sigma_0` が単一の
10-サイクルであることを使って **10 候補の悉皆**(`g(0)=c`、$3628800$ 通り
や $10!$ の総当りは不要)に縮小し、解の一意性と `g^2=sigma_1` を
定理由来の自己検査(破れれば integrity stop)として実装している。

---

## K3-regression-kummer-cov3.v1.json / K3-regression-kummer-cov3-checkcov3.v1.json

**撤回日**: 便 36(裁定 36_ben35・実装担当)。

**撤回理由**(Sol 便 35 F3 = blocker 4 の指摘): 旧 `KummerCovariance3Check`
(`search/kummer-decide.g`)・`crosscheck/check-kummer-cov3.mjs` は、witness
`e ∈ K = Q(zeta_12)`(`e^M = w^ord` を満たす円分体の元)に対して
`GaloisCyc(e, d)` / 独立実装では円分多項式環上の代入 `a -> a^d` を
`d ∈ (Z/12)^×` について適用し、その比 `sigma_d(e)/e` を `zeta_M` の
冪として読む表を作っていた。これは **`Gal(K/Q)` が `K` の元 `e` に
作用する変換**であって、要求された **Kummer character**

```
kappa_w(gamma) = gamma(w^{1/M}) / w^{1/M}     (gamma in G_K)
```

ではない(`e ∈ K` は定義により `G_K` に固定されるので
`GaloisCyc(e,d)/e` の非自明値はこの character と無関係)。さらに出力には
`b_i`・`tau_i`・`rho_0`・`j_i`・formal `a` のいずれも現れず、便 34 F4.5 が
要求した「`b_i` と Kummer character exponent を同時に変換し formal `a=1`
を変えないことの検査」を実行し得ない(Sol 便 35 F3 全文)。

**帰結**: この二証明書は「要求された較正ではない」ものとして撤回する。
後継は `search/kummer-cov3-actual.g` /
`crosscheck/check-kummer-cov3-actual.mjs` が生成する
`certificates/k5pipeline/K3-regression-kummer-cov3-actual.{gap,node}.json`
であり、`docs/manifest_k5_appendixA_v1.md` の K3 fixture が実際に記録した
`rho_0` の生成元像・`tau` の生成元作用・`j` の表(実値)だけを入力に、
生成元の取り替え `zeta_M[e] -> zeta_M[e]^{d'}`(`d' in (Z/e)^x`、K3 では
`e=3`)のもとで `j` の対応表が transformation law
`t' = d'^{-1} t (mod e)` のとおりに書き換わることを、置換の実値等式として
検査する。**射程の限定を明記**: 後継は `b_i`(実際の局所モノドロミー生成元
`ell_i` と intertwiner `c_i` から測る量・Rule 1 §7.1)を独立に測定した値を
持たない — K3 の `tau` は `s^{1/M} -> zeta_M s^{1/M}` という局所 Kummer
規約から直接定義されており(`docs/week4-K3飽和_opus_v3.md` §5.2.0)、この
構成では `b=1` は定義上のものであって Rule 1 §7.4 が要求する「独立に計算
して記録する」対象の実測値ではない。同様に formal `a`(= K5 の sq/ns 比較
指数、Rule 1 (1.11))は K3 単体の dessin には定義されない量であり、本追補
では K5 側で既に恒久固定された `a=1` を援用するのみで独立に再導出しない。
**したがって本追補は Sol 便 35 F3 が要求した較正のうち「τ/ρ₀/j の実値
covariance」の部分を実装するが、「実測 `b_i` の covariance」の部分は
現在の証明書に載っていない実測データ(intertwiner `c_i` と局所モノドロミー
生成元 `ell_i` の実装)を要求するため UNKNOWN として司令塔へ差し戻す。**

**裁定根拠**: `sol/sol_reply_35_freeze1r4.md` F3(blocker 4)・
`sol/裁定_36_ben35.md`。

---

## toy-ninf-M3-u-compare.v1.json

**撤回日**: 便 37 検収対応(裁定 38・実装担当・2026-07-27)。

**撤回理由**: schema `u-compare-ninf-toy/v1`(旧 `u-compare-ninf-toy.mjs` が
生成)であり、現行 raw(schema v2・`u_pathA_ninf`/`u_pathB_ninf` は本便で
`chat=1` に修理済みの `1/2`)と食い違う古い `u=1` の値を記す(Sol 便37 F1.2
の指摘)。**現行 checker で再発行**: `crosscheck/u-compare-ninf.mjs`
(schema v3・bundle 引数必須)で `certificates/k5pipeline/toy-ninf-M3-bundle.json`
を第三引数に与えて再計算した現行版が
`certificates/k5pipeline/toy-ninf-M3-u-compare.json` として存在する。

---

## K3-regression-cov1-k2-u-compare.v2.json

**撤回日**: 便 37 検収対応(裁定 38・実装担当・2026-07-27)。

**撤回理由**: schema `u-compare/v2`(旧 `u-compare.mjs` の 2 引数版・
`branchP0` field 時代)。便 37 F2/F3 修理で `u-compare.mjs` は
(a) branch/P0_type の分離(schema v3・canonical string が変わるので
model_digest も変わる)、(b) 第三引数として凍結 bundle/model-spec を必須化、
の二点を反映した。COV-1 派生モデル(`K3-regression-cov1-k2`)は
`search/u-extract-pathA-k3-driver.g` / `crosscheck/u-extract-pathB-k3-driver.mjs`
のコメントに明記のとおり**「較正のみの参考出力・パイプラインの入力には
使わない」**ものであり、certificates/k5fixture 配下に対応する model-spec
ファイルを持たない(K3-regression-model.json から driver 内で導出される
派生モデルのため)。したがって R-7 の bundle 束縛要求はこの参考比較には
及ばない(Sol 便37 F2 が要求したのは正典パイプライン `K3-regression` /
`toy-ninf-M3` / `prod-ninf-M10` の三本であり、COV-1 はそこに含まれない)。
本便では `K3-regression-cov1-k2-u-pathA.json` / `-u-pathB.json` 自体は
schema v3(branch/P0_type)へ再生成した上で二経路一致(`u=-1/1024`)を
driver 実行時の標準出力で確認済み(`node crosscheck/u-extract-pathB-k3-driver.mjs`
の `COV-1 check` 行・`match=true`)。旧 `-u-compare.json` は
このディレクトリへ撤回するのみとし、bundle 必須の新 checker では
再発行しない(参考比較という位置づけのまま)。
