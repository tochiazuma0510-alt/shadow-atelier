# BelyiDB/Belyi 公開パイプライン実地調査 v1 — 札 1 option C(自前計算)の実現性判定

`DIR: proper 側計器の外部入力調達 / FRAME: 札 1 §2.2″ 自前計算経路の facts-finding`

**委嘱**: 裁定 1777(一体型実地調査・Fable(max) 単独)。**著者**: 数学者(Fable 5)/ 2026-08-29。
**対象**: group 9T27 = PSL(2,8)・passport [[9],[9],[9]]・種数 4・rigid・定義体 Q(ζ9)⁺ = LMFDB 3.3.81.1(要求仕様 = `scratchpad/fuda1_select_closure_v1.md` §2.2′/§2.2″)。
**方法**: 公開リポジトリ 2 本の clone・実ファイル読解・LOC/grep 機械計測・GAP 検算 1 本(§5)・論文テキスト照合(kmsv.txt / mssv.txt 在庫)。**Magma 不在のため実行はしていない**(構文解析・依存 grep・データ census まで)。

---

## §0 三値判定(結論先出し)

> ### 判定 = **(B) 移植プロジェクト級 — ただし限定形(「CAS 間移植」は不要)**
>
> 必要なのは移植ではなく、次の 3 点である:
> 1. **Magma 環境の確保**(前提条件・工房外資源。パイプラインは Magma 言語 17,700 行+C 拡張で、フル移植は非現実的(§7)。逆に Magma さえあれば下記 2. 以外は完備)
> 2. **種数 ≥3 non-hyperelliptic 枝(canonical embedding)の追加実装** — 目的の枝はコードに存在しない(逐語: `Code/belyi_main.m` **L210** `error "not implemented for nonhyperelliptic genus > 2.";`)。ただし必要部品(冪級数基底・数値カーネル・数体認識・検証)は全て genus 非依存で完備しており、論文(KMSV)には一段手前の完動例(**Ex 5.27 = rigid (7,7,7)・PSL(2,7)・genus 3**)が式まで書かれている。追加分は既存 hyperelliptic 枝(473 行)の同型パターン **~300–600 行**。
> 3. **較正**(9T27 の computed 済 6 passport 再現 → Ex 5.27 再現 → 本番)。
>
> **分岐**: 我々の曲線が hyperelliptic なら(確率 UNKNOWN・数値テスト 1 発で判明・§4.3)2. が不要になり **(A) リファクタリング級に降格**する。Magma 環境が確保できなければフル移植で **(C) 寄りの大型 (B)**(10–20 便超・非推奨)。
>
> **便数見積り(Magma 環境確保後)**: **4–7 便**。成功確率(主観・根拠 §8.3): 6 便以内 60–70%・12 便で ~80%。

**論点への裁定材料**(研究者「コードは公開済みでリファクタリングするだけ」vs 司令塔「CAS 間移植は数週級・種数 ≥2 枝が frontier」):
- 研究者の直観は**半分正しい**: コードは公開・**現役保守中**(両リポジトリとも最終 commit **2026-08-27** = 調査 2 日前)・2026-08 に AI 支援で工学強化済(§3.4)・我々の passport の**骨組みエントリまで既に DB に存在**し、我々の marked pair が pointed passport の **T2 と S9 同時共役であることを機械確認した**(§5)。
- 司令塔の「種数 ≥2 枝が frontier」も**数字で正しい**: 完成データは genus 2 で 15/269(5.6%)・**genus 3 以上はゼロ**(0/42+0/6)・9T27 に限れば genus 2 の 4 passport も全滅(§6)。ただし「CAS 間移植」は不要という点で構図が違う — 戦場は Magma 内の欠落枝追加である。

---

## §1 リポジトリの同定(作業 1)

| repo | URL | 最終 commit(実測) | 規模 |
|---|---|---|---|
| **BelyiDB**(データベース+wrapper) | github.com/michaelmusty/BelyiDB | `aa663d2` 2026-08-27 "Eval -> Evaluate" | belyi_db/ 2,042 ファイル(次数 9 は 1,207)・code/ 4,473+163 行 |
| **Belyi**(計算エンジン本体) | github.com/michaelmusty/Belyi | `0cd768d` 2026-08-27 "Read TrialDivision's residue divisor as an integer (Magma >= V2.29-9)" | Code/ **17,700 行**(.m 総計)+ Cext/(C 拡張)+ Tests/ |

- 接続の逐語根拠: `BelyiDB/scripts/r_nonhyp.m` **L2** `AttachSpec("../Belyi/Code/spec");` — BelyiDB は兄弟ディレクトリの Belyi エンジンを Attach する 2 リポジトリ構成。
- 著者: Musty–Schiavone–Sijsling–Voight(MSSV)。Sijsling の GitHub に Belyi 専用 repo はない(17 repo 走査・関連は RiemannSurfaces fork のみ)。Musty の projects ページの Belyi 関連は BelyiDB と 2groupdessins(2-群専用・我々には不適)のみ。
- clone 先(セッション scratchpad): `...\scratchpad\BelyiDB`・`...\scratchpad\BelyiEngine`。
- ⚠ 誤読防止: `scripts/r_nonhyp.m` の "nonhyp" は **non-hyperbolic**(球面/ユークリッド型)の略であり non-hyperelliptic ではない(L14 が χ<1 = hyperbolic を skip する)。

## §2 パイプラインの段構成(作業 2(a)・実ファイル・実関数)

MSSV 論文 §3.1 の 5 段(mssv.txt L296-311)にコードを対応させる:

| 段 | 論文の記述 | 実装(ファイル:関数) | genus 依存性 |
|---|---|---|---|
| 1 | triangle subgroup Γ ≤ Δ(a,b,c)・coset graph | `triangle.m: TriangleSubgroup`(+ `cosets.m`・`hackobj.m` の自前型 `GrpPSL2Tri`・「KMNSV-351, June 2013」ヘッダ) | なし |
| 2 | S_k(Γ) の数値冪級数基底(Hejhal 法+Arnoldi) | `powser_iter_arfed.m: PowerSeriesBasis(Gamma, k)`(dim: `basics.m:83 SkDimension`、k=2 で dim=g)+ **C 高速版 `Cext/powser_arnoldi.c`**(`PowserAl:="CArnoldi"`) | **なし**(genus 4 なら weight-2 形式 4 本を返す。belyi_main.m L203 で genus>2 でも現に呼ばれる) |
| 3 | 曲線方程式と φ の数値決定(数値線形代数+Riemann–Roch) | genus 0: `genuszero.m`/`newton.m`・genus 1: `genusone.m`/`newton.m`・genus 2/hyperelliptic: `hyperelliptic.m`(`TriangleHyperellipticTest`→`TriangleHyperellipticNumericalCoefficients`)・`newton_hyperelliptic*.m` | **あり — ここだけ genus 分岐**(§4) |
| 4 | 正規化・係数の代数的認識(数体 K の同定) | `theta.m: MakeK / MakeKBatch / RecognizeOverK` + `recognition.m: TriangleRecognizeAlgebraicCoefficients`・LLL/PowerRelation ベース+ **C 認証版 `Cext/makek_relfinder.c`**(`ExactAl:="Certified"`) | なし(任意次数の数体を認識。三次体 3.3.81.1 は楽な射程) |
| 5 | 検証(ramification+monodromy) | `belyi_main.m L331: BelyiMapSanityCheck`(φ, φ−1, 1/φ の divisor 構造と σ の cycle structure を突合・Magma の Crv/Divisor 機械) | なし |

- **monodromy 対応の由来**(我々の「マーク付きファイバー整合ラベル」要求に直結): KMSV L2880-2887 — 「it is enough to verify that the cover computed is a three-point cover; ... the way that the cover was constructed **guarantees that it has the correct monodromy** ... identifies the embedding of the number field yielding the specific monodromy triple」。**σ ↔ 数値解の対応は構成そのものが与える**(MSSV L323-324 も同旨「we obtain the bijection between triples and Belyi maps by the very construction」)。LMFDB の完成データだけでは失われる対応が、自前で回すと構成ごと手に入る — 札 1 の要求仕様に対する本質的な利点。
- 厳密性の格: KMSV Remark 5.31(L2892)「At the present time, **our method is not rigorous**」— 数値法+事後検証であり、収束保証はない(終われば正しい: mssv L292-293)。

## §3 種数分岐の実装地図(作業 2(b)・行番号つき)

### 3.1 単体 σ 経路(`Code/belyi_main.m`, intrinsic BelyiMap(Gamma), L69-224)

```
L107 if Genus(Gamma) eq 0 then        … 完備(Newton 含む・既定 Al:="Newton")
L127 elif Genus(Gamma) eq 1 then      … 完備(Newton / NumericalKernel+MakeK)
L169 elif Genus(Gamma) eq 2 then      … 完備(NumericalKernel=hyperelliptic 型+MakeK)
L201 else  -- genus >= 3:
L202   vprint "Testing if hyperelliptic...";
L203   Sk := PowerSeriesBasis(Gamma, 2 : ...);           ← genus 任意で動く
L204   hyp_bool, ... := TriangleHyperellipticTest(Sk, Gamma);
L205   if hyp_bool then … hyperelliptic 枝(L206-208: NumericalCoefficients
         → TriangleRecognizeAlgebraicCoefficients → TriangleMakeBelyiMap)
L210   else error "not implemented for nonhyperelliptic genus > 2.";   ← ★ 欠落点
```

### 3.2 passport 一括経路(GaloisOrbits 認識・L253-328 + `recognition.m`)

```
belyi_main.m L319 elif Genus eq 2 …(Record→Recognize→Make)
belyi_main.m L324-325 else error "Not implemented for genus greater than 2.";
recognition.m L139-140(TriangleRecordCoefficients も genus>2 で error)
```
- BelyiDB 側 wrapper `code/database_code/query.m` **L434-440** は genus>1 で `BelyiMap(Gammas : Al := "NumericalKernel", ExactAl := "GaloisOrbits")` を呼ぶが、行き先が上記 L325 で死ぬ — **現状 dead path**(genus 2 単体は生きている)。
- 帰結: **我々は passport 一括(GaloisOrbits・6 本全部計算)ではなく、単体 T2 + `ExactAl:="AlgebraicNumbers"`(MakeK・数体直接認識)路線を採るべき**。genus 2 単体枝(L190-197)が現にこの形で、三次体上の認識は MakeK の標準機能。rigid ゆえ解は一意で「1 本だけ計算」に数学的欠損はない(向き・fibre ラベルは §5 の conjugator で翻訳)。

### 3.3 hyperelliptic 枝の完成度(genus ≥3 で hyp だった場合に通る道)

- `hyperelliptic.m` L62-112 `RiemannRochBasisHyperellipticAnalytic` — L(m·∞) の解析基底。**L76 に「// this is the odd case TODO test this case」**(奇数次モデル未テスト)。
- genus ≥3 hyperelliptic の**完成データは DB にゼロ**(§6)— コードパスはあるが実戦実績なし。

### 3.4 2026 年の工学強化(現役性の証拠)

GitHub API 実測(直近 commit 履歴):
- 2026-08-27: Magma V2.29-9 の TrialDivision 返値変更対応(3 箇所・**Co-Authored-By: Claude Opus 5** — AI 支援開発が入っている)
- 2026-08-21: PR #37/#38 マージ = **外部 C 認証認識器 makek_relfinder**(fmpz_lll 一括+arb 認証・「observed: 15+ CPU-hours of doomed MakeK calls on an **M24 genus-0 run** at prec := 400」→ 秒で fail-fast 化)
- 2026-08-04: PR #39 common zero fix(genus 1 Newton)
- README 実測値: C ソルバーで KMSV Ex 5.15(deg 7・prec 100)が end-to-end **~23 s**(vs 純 Magma ~170 s)。Tests/ に回帰スイート(`sh Tests/run_tests.sh`・数分)。
- 含意: M23/M24 級の 2026 年計算(工房 memory の M₂₃ 逆ガロア 2026-08 と整合)を支えている基盤であり、「10 年前の論文付属コード」ではない。**genus 0 方向の次数フロンティアに投資が向いており、種数方向は手つかず** — 我々の需要(小次数・高種数)と直交していて、衝突しない。

## §4 我々の入力は想定内か(作業 2(d))

### 4.1 入力形式・エントリの実在

- 入力 = 置換三つ組そのもの: `BelyiMap(sigma::SeqEnum[GrpPermElt])`(belyi_main.m L38)。
- **我々のエントリは骨組みとして既に DB に存在する**: `BelyiDB/belyi_db/9/9T27-[9,9,9]-9-9-9-g4.m`(4,299 bytes)。`BelyiDBSize := 6`・`BelyiDBPointedSize := 6`・自己同型自明・monodromy 群位数 504。**Base Field Data / Belyi Maps / Powser Bases の各セクションは空**(未計算)— LMFDB 不在(遠征 1)と整合。
- 較正正解データもすぐ隣にある: 9T27 の 14 passport 中 **computed 6 件**([7,2,3]g0, [7,7,2]g0, [7,3,3]g1, [7,7,3]g1, [9,2,3]g1, [9,7,2]g1)— LMFDB の 9 orbits とパスポート単位で一致。

### 4.2 定義体 Q 以外・rigidity・descent

- 定義体: MakeK は任意次数の数体を認識(theta.m L145-)。GaloisOrbits 路線だけが「over the rationals」前提だが採らない(§3.2)。**三次体は想定内**。
- rigidity: コードに rigid の特別扱いは**ない**(grep 0 hit)— ただし恩恵(解一意=数値収束先一点)は自動で受ける。
- descent: MSSV §4.1(mssv L351-353)「if σ has trivial automorphism group Aut(σ), then σ descends」— 我々は Aut(σ)=1(骨組みファイル L24-25 で空生成・仕様 §1.8 の中心化自明と一致)⟹ **field of moduli = 定義体 = 3.3.81.1 への降下が文献側でも保証**。

### 4.3 唯一の分水嶺 = hyperelliptic 性(UNKNOWN・一級)

- 我々の genus 4 曲線が hyperelliptic か否かは**未知**(群論のみからは決まらない。一般論では genus 4 の generic は non-hyperelliptic だが我々は特殊曲線であり適用不可)。
- **実測 1 発で決まる**: `PowerSeriesBasis(Γ,2)`(4 本)→ `TriangleHyperellipticTest`(belyi_main.m L203-204 がそのまま走る)。hyp なら既存枝(§3.3・未テスト注意)・non-hyp なら L210 → 追加実装(§8.1)。
- 数学的中身: non-hyp genus 4 の canonical model は P³ の (2,3) 完全交差。KMSV L2594-2600(General case)が「the ideal ... is generated in degree 2 and 3」まで明示(genus 4 を正面からカバーする記述)。

## §5 機械検算 — 我々の被覆は BelyiDB pointed passport の T2(逐語・GAP 実測)

`gate: scratchpad/belyidb_match_probe_v1.g`(本便で作成・実行済)。骨組みファイルの 6 triples を逐語転記し、`search/drophunt_checker_producer_v2.g` の DCP2X4/DCP2Y4 と突合:

```
T1..T6  soo*s1*s0 = 1 : true(6/6)     s0*s1*soo = 1 : false(6/6)
T1..T6  group order 504(6/6)
OURS orders [9,9,9]  group 504   s0*s1*soo = 1 : true
MATCH T2   conjugator (1,5,7,8,6)(2,3)(4,9)     HITS [ 2 ]
T2 class pattern [8,8,8]   (他 5 本は [8,9,7],[8,7,9],[8,9,9],[8,8,7],[8,7,8])
```

1. **規約凡例(要台帳化)**: KMSV/BelyiDB の三つ組規約は **σ∞σ1σ0 = 1**(kmsv.txt L139-140 逐語「such that σ∞σ1σ0 = 1」)。工房規約(σ0σ1σ∞=1・fuda1 §1.8)と**積順が逆**。marked pair (σ0,σ1) レベルの対応は規約非依存なので下記 2. は有効だが、第三成分・fibre ラベルの翻訳時は要注意。
2. **同定**: 我々の marked pair (X4,Y4) は pointed passport の **T2 と S9 同時共役・conjugator (1,5,7,8,6)(2,3)(4,9)・一意**(中心化自明ゆえ 0 ビット曖昧性 — 仕様 §1.8 と整合)。T2 の class pattern [8,8,8] = rigid (C,C,C)・クラス #8(仕様 §1.8 の「同一クラス #8」と一致)。
3. 副産物: pointed passport 6 本 = (C,C,C) 型 1 本(=T2)+ 混合クラス型 5 本。「計算したら T2 の解を取り、この conjugator で我々の fibre ラベルに翻訳する」ところまで仕様が閉じた。

## §6 副次確認 — genus ≥2 の完成データ census(作業 5・機械集計)

belyi_db/ 全 2,042 ファイルの `BelyiDBBelyiCurves`(計算済みの印)保有数:

| genus | エントリ総数 | **computed** | 率 |
|---|---|---|---|
| 0 | 993 | 837 | 84% |
| 1 | 732 | 205 | 28% |
| 2 | 269 | **15** | 5.6% |
| 3 | 42 | **0** | 0% |
| 4 | 6 | **0** | 0% |

- genus 2 computed 15 件は全て次数 5–7(hyperelliptic 枝・7T5-[7,7,3] 等 = KMSV/MSSV 論文の例と対応)。**9T27 は genus 2 の 4 passport も全て未計算**([7,7,7]-g1 も未計算)。
- **解釈**: 「general-curve 枝の実戦投入度」はデータとしてゼロ。パイプラインの実戦領域は genus 0(次数 9 まで一括+M23/M24 級の単発)と genus 1 の一部。種数方向のフロンティアは genus 2 の手前で止まっており、genus 4 は**世界的にも前例なし**(遠征 2b の「次数 9 で種数 ~3 まで」= KMSV Ex 5.27 の genus 3 が文献最高到達点、と本調査は整合。なお Ex 5.27 は論文では完動しているがパッケージには入っていない — 論文射程 ⊋ コード射程)。

## §7 Magma 固有機能の分類と移植性(作業 2(c)・grep 実測)

エンジン Code/*.m の使用機械(hit 数は grep -o 計):

| カテゴリ | 実測 | Sage | OSCAR/Hecke | Julia+Arb | 備考 |
|---|---|---|---|---|---|
| 双曲三角群・コセット・FD reduction | **自前層**(hackobj 353 + triangle 565 + cosets 280 行・「inheritance is broken」と自認する独自型 GrpPSL2Tri) | 既製品なし | なし | なし | Magma 固有機能への依存は薄い(複素数+2×2 行列)が**移植対象としては最大の塊** |
| 冪級数環 | LaurentSeriesRing 16 / PowerSeriesRing 9 | 可 | 可 | Nemo 可 | 汎用 |
| 数値線形代数(Arnoldi・SVD・NumericalKernel 26 hit) | **既に C 化済**: `Cext/powser_arnoldi.c`(FLINT acb・DFT 構造利用・マルチスレッド・residual 検証) | — | — | **そのまま流用可(Magma 非依存バイナリ)** | 最重量段が CAS 中立になっている |
| 整関係発見・数体認識(LLL 14 / MakeK 27 / PowerRelation 9) | **既に C 化済**: `Cext/makek_relfinder.c`(fmpz_lll+fmpz_poly_factor+arb 認証) | PARI algdep | Hecke | **そのまま流用可** | 同上 |
| 数体(NumberField 41) | Magma | 可 | 可 | Nemo 可 | 三次体は軽い |
| 曲線・関数体・因子(FunctionField 48 / Divisor 23)= exact 検証側 | Magma | 可 | 可 | 限定的 | sanity check の移植は中規模 |
| Groebner / リーマン面 pkg / モジュラー形式 pkg / theta / 周期・AnalyticJacobian | **全て 0 hit(不使用)** | — | — | — | 重量級固有機械に依存していない |

- **結論**: フル移植は「自前双曲層+glue 数千行の書き直し+全較正」で 10–20 便超(数ヶ月級)— **不要かつ非推奨**。合理的経路は Magma 環境の確保(パイプラインの要求 Magma バージョンは >= V2.29-9・2026-08-27 commit が明言)。C 拡張は FLINT >= 3.0 を要求(Linux なら libflint-dev・`build_deps.sh` で非 root 構築可)— **GHA レーン化の素性は良い(Magma ライセンスだけが障壁)**。
- 参考: Pari/GP(polredabs)は optional submodule(README「will still run if you do not have Pari/GP installed」)。

## §8 推奨計画(作業 4)

### 8.1 欠落枝(non-hyp genus 4)の追加実装 — 数学仕様の骨子

論文レシピ(KMSV L2594-2606 + Ex 5.27)を既存コードの型に流し込む:
1. **canonical ideal**: S₂(Γ) の 4 本 f₁..f₄(段 2 の出力)から、二次単項式 10 個・三次単項式 20 個の冪級数を作り NumericalKernel → **quadric 1 本 + cubic 1 本**(genus 4 の (2,3) 交差)。`TriangleHyperellipticTest`(hyperelliptic.m L159-)と同型の処理・~150 行。
2. **φ の表示**: φ = A/B(A,B = f_i の三次形式)。次元勘定: deg(3K−9P∞) = 18−9 = 9 ≥ 0 で H⁰(3K−9P∞) ≠ 0(B の存在)・dim H⁰(3K) = 15 = 三次単項式 20 − 関係 5。φ·B − A = 0 を weight-6 冪級数の数値カーネルで解く・~200 行(genusone.m / hyperelliptic.m の φ 構成が手本)。
3. **認識**: 係数列 → 既存 `TriangleRecognizeAlgebraicCoefficients` / MakeK(単体・AlgebraicNumbers 路線)を流用・追加実装ほぼゼロ。
4. **検証**: (2,3) 交差を Crv として作れば既存 `BelyiMapSanityCheck`(divisor vs cycle structure)がそのまま動く。
- 予想実装量 **300–600 行**(すべて Magma 内・同型パターンの複写に近い)。precision 既定は L103 式で 30+5·(4+1)·9 = **255 桁**(C ソルバー圏内・M24 で prec 400 の実績)。Newton 精密化(genus 0/1 用)は canonical 枝に無いので、初期 prec を上げて直接認識(Ex 5.27 方式)— 失敗時は prec 引き上げでリトライ。

### 8.2 段取り(便単位)

- **便 0(工房内・Magma 不要・今すぐ可能)**: (a) 本報告の T2/conjugator/規約凡例の台帳化(§5・完了)(b) computed 6 件の係数の独立検算(GAP/Python で mod p monodromy 再計算 — 較正正解データの品質確認)(c) §8.1 の数学仕様書の起草。
- **便 1**: Magma 環境疎通・FLINT/C 拡張ビルド・`Tests/run_tests.sh` PASS・9T27 computed 6 件の再現(較正ゲート 1)。
- **便 2**: **hyperelliptic 判定の実測**(L203-204 を genus 4 で走らせるだけ)+ Ex 5.27(PSL(2,7)・g3)の canonical 枝プロトタイプ実装と論文の式(kmsv L2622-2624 の quartic・φ の p₀,p₁,p₂)との突合(較正ゲート 2)。
- **便 3–4**: genus 4 版実装(§8.1)+ 我々の T2 で本番実行。
- **便 5**: 検証と翻訳 — sanity check・GAP による独立 monodromy 照合(数値 fibre の接続 or mod p 分解)・conjugator (1,5,7,8,6)(2,3)(4,9) による fibre ラベル翻訳・fuda1 §2.1 のフィールド 4/5 への接続。
- 予備 1–2 便: precision/conditioning リトライ。
- **計 4–7 便**。hyperelliptic と判明した場合は便 3–4 が「既存枝の odd-case TODO 修理」に置き換わり **3–4 便**に短縮。

### 8.3 成功確率(主観・正直申告)

- 上振れ材料: rigid で解一意(収束先一点)・定義体が判別式 81 の三次体で小さい(認識が軽い)・論文に同構造の完動例(Ex 5.27: rigid・(7,7,7)・PSL(2,7)・g3)・monodromy 対応が構成から自動で付く(§2)・2026 年の C 化で計算余力が大きい。
- 下振れ材料: genus 4 は**世界前例なし**(§6)・g≥3 は hyperelliptic 枝ですら実戦ゼロ・canonical 枝に Newton がなく高 prec 直接認識の条件数は未知・KMSV 自身が「not rigorous」(収束保証なし)。
- **見積り: Magma 環境を所与として 6 便以内 60–70%・12 便で ~80%**。Magma 環境が確保できない場合は路線ごと再設計(フル移植 10–20 便超・成功確率さらに低下)につき非推奨。

### 8.4 最初の 1 便で何をすべきか

**Magma 環境の確保可否の確定が全てに先行する**(研究者判断事項: 所属機関ライセンス・共同利用環境の有無。作者接触は禁止のまま不要 — 公開コードだけで完結する)。並行して工房内で便 0(§8.2)を消化する。環境が確保でき次第、便 1(疎通+較正ゲート 1)へ。

## §9 UNKNOWN 一覧(一級)

| # | 項目 | 決まる時期 |
|---|---|---|
| U-A | 我々の曲線の hyperelliptic 性 | 便 2 の数値テスト 1 発 |
| U-B | Magma 環境の確保可否 | 研究者判断(最初の 1 便) |
| U-C | genus 4 での認識に要する実 precision(既定 255 桁で足りるか) | 便 3–4 |
| U-D | g≥3 hyperelliptic 枝(odd case「TODO test this case」hyperelliptic.m L76)の実働性 | hyp だった場合の便 3 |
| U-E | canonical 枝での条件数(Arnoldi 基底の直交性が genus 4 で劣化しないか) | 便 2 の Ex 5.27 再現で先行測定 |

## §10 参照 sha(機械出力)

```
belyidb_match_probe_v1.g                                    3192  7390540dd8b1d8b6
fuda1_select_closure_v1.md (入力仕様)                       34780  a247dba524b14113
9T27-[9,9,9]-9-9-9-g4.m (BelyiDB 骨組み・clone 内)           4299  26bc39a21b1936b5
BelyiDB HEAD  aa663d2aded41c6844f3237ac26f687f7382bda3  (2026-08-27)
Belyi  HEAD   0cd768d5762aedb61618020d331da77634503987  (2026-08-27)
```

**完**(BelyiDB/Belyi 実地調査 v1)
