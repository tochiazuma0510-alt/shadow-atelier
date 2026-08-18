# Luna reply 157do — FC-8* `A5^4` chief certificate

## 判定

指定された 3 code files を新規実装した。GAP/GHA/git は実行していないため、実 receipt の終端

```text
FC8_A5_FOUR_CHIEF_CROSSCHECKED
```

はまだ宣言しない。producer は全 gate が通った場合に限ってこの token を出し、数学的前件が落ちた場合は対応する `FC8_UNKNOWN_*` を出す。checker は terminal/UNKNOWN の双方を schema ごと fail-closed に検査する。

## 作成ファイルと固定 SHA256

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_b4_fc8_a5four_v1.g` | 26713 | `d482315bb0abc54e9707651a8fb73e73a4a569f101f51c232b76a73fbf57e804` |
| `search/check_d972_b4_fc8_a5four_v1.py` | 41994 | `5b2f54b7adbddbff914fe2d28786327df9109d4e91fa53b1be03114eed5a65d4` |
| `search/d972_b4_fc8_a5four_gha_driver_v1.g` | 4307 | `806d8bfa32ecb1f24f0873147da9e13b56fa171294f081cdd321894b77c545af` |

driver 内 pin は上の producer/checker SHA と一致する。

主な frozen pin は次のとおり。

- coarse core: `577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c`
- four deletion fixture: `6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2`
- deletion checker: `eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032`
- A1 marking / v2.2 extension: `24c42967...d8a02` / `a348b504...e8d6`
- T-40 screening: `9e69838f923a77385ce191244c57e88dc24d95b3c9ae9d5d0f9b0cd0c148cad8`

## 実装した有限証明書

### 1. `rhoA:PB4 -> A5^4`

canonical marking

```text
X=(1 3 2 4 5),  Y=(1 3 4 5 2),  Z=X^-1 Y^-1
```

と frozen four-deletion table から、canonical order

```text
(x12,x13,x14,x23,x24,x34)
```

の 6×4 marked rows を再構成する。recursive Fadell–Neuwirth presentation の 11 relators を faithful Artin representation でも再導出し、全 row で identity を要求する。

全射証明は `A5^4` の 12,960,000 元を列挙しない。次の 4 literal commutators を使う。

```text
[-4,-6,4,6], [-2,-6,2,6], [-1,-5,1,5], [-1,-4,1,4]
```

各 word はちょうど 1 coordinate にだけ非自明な `[X,Y]` を持つ。各 coordinate projection が order 60、各 single-support value の `A5` 内 normal closure が order 60 であることを個別に certificate 化した。これで `im(rhoA)=A5^4` が構造的に閉じる。

### 2. B4 action と kernel normality

`c_(sigma_i^-1)(v)=sigma_i^-1 v sigma_i` の 3 action tables を canonical six rows 上で再構成した。各 source word は braid word の faithful Artin actionと直接比較される。各 finite action は一意な

```text
output coordinate <- source coordinate, followed by conjugation in S5=Aut(A5)
```

へ分解される。factor permutations は `(12),(23),(34)`、生成像は transitive `S4`。8 本の coordinate `X/Y` basis 上で 2 braid relations と distant commutation も replay する。この exact intertwining により `ker(rhoA)` の B4-normalityを label inference なしで閉じる。

### 3. frozen `rho0` と Goursat

同一の canonical six PB4 generators に対し、frozen core から `P^4` blocks と actual `H9<=G9^4` blocks を再構成して `rhoA` rows と一行ずつ束縛する。

- `P=PSL(2,8)`: order 504、perfect、prime support `{2,3,7}`
- `G9`: order 2916、derived-series orders `2916,729,1`
- `H9`: order `32*3^24 = 9037745167392`、prime support `{2,3}`
- `P^4`: order `504^4 = 64524128256`
- `Q0=P^4 x H9`: order `583152628325845597028352`、prime support `{2,3,7}`

producer では `P^4` も four single-support normal-closure certificates で閉じる。`H9` は six marked rows の image として定義される。`P^4` は perfect、`H9` は solvable なので両 projection の共通 Goursat quotient は trivial、従って frozen joint image は `P^4 x H9`。

checker は producer の `direct_product=true` を信用しない。標準 GF(8) projective model から `P` を、dihedral three-block formula から `G9` を独立再構成する。`G9'=C9^3`、six H9 commutators の mod-3 Nakayama rank 12、および `(G9/G9')^4` 内 quotient image order 32 を計算し、`|H9|=32*3^24` と solvability を独立に得る。

`5` は `|Q0|` を割らない。一方、`A5^4` の任意の非自明 quotient は order が 5 で割れる。したがって `Q0` と `A5^4` は非自明共通 quotient を持たず、joint PB4 image は Goursat により `Q0 x A5^4` 全体となる。

### 4. chief 結論

```text
M = ker(rho0)
K = M intersection ker(rhoA)
```

とすると joint surjectivity より `rhoA|M` は `A5^4` へ全射で、kernel は `K`。従って first isomorphism theorem により

```text
M/K ~= A5^4.
```

非可換単純群の direct power の normal subgroups は coordinate factors の積である。B4 の coordinate action は transitive S4 なので、B4-stable factor subset は empty/all だけである。よって `M/K` は `S=A5,t=4` の B4-chief factor。

### 5. T-40 / FC-8** sanity gate

各 `sigma_i` の 4 個の `S5` conjugators の parity から base total outer bit を、factor permutation から S4-sign bit を独立計算する。これらの

```text
Q -> (Out(A5)^4 semidirect S4)^ab = C2^2
```

image の F2-rank が高々 1、すなわち cyclic であることを terminal gate に追加した。2 characters が独立な `C2^2` を作れば `FC8_UNKNOWN_CB3_COUPLING` で停止する。

FV-5 に従い、登録する `A5^4` window / `K` の isolatedness は本 certificate の前件にしていない。監査窓の isolatedness は Cor. 3.5 側で供給される。`K` 自体の isolatedness は `NOT_ESTABLISHED_AND_NOT_REQUIRED_BY_FV5` と記録した。

## 独立 checker と mutation gates

checker は producer helper を import しない。次を独立再構成する。

- A5 marking、order/simple/perfect certificate
- PB4 11 relatorsと faithful Artin orientation
- four projections / four single-support normal closures
- 3 induced factor automorphisms、braid/commutation、transitive S4
- CB-3 の 2 characters
- canonical `PSL(2,8)` / `G9` / structural `H9` order
- Q0–A5^4 no-common-quotient と chief lemma premises

mutation suite は deletion letter、coordinate、support image、Artin transport、P order/type、H9 solvability/order/prime support、`t`、CB-3 character、terminal relabel の 12 種を reject するよう実装した。

許可された単発 local checker selftest は、実装途中の古い簡略 Artin table を正しく検出して

```text
FC8_A5_FOUR_CHECKER_FAIL faithful source Artin orientation
```

で停止した。その後、既存 cross-checked row18 implementation の exact natural-action words

```text
sigma2: x12 -> [-4,2,4]
sigma3: x13 -> [-6,3,6], x23 -> [-6,5,6]
```

を producer/checker 双方へ反映した。task の「one lightweight selftest」上限を消費したためローカル再実行はしていない。修正後は Python AST PASS、placeholder なし、producer/checker SHA chain と driver pin 一致を静的確認した。その後、下記 GHA canary で修正後の全 selftest を実行し、12 mutation を含め PASS した。

## 性能契約

source-only estimate は selftest/full とも数十秒以内、保守的上限 2 分。主な有限操作は次のとおり。

- frozen coarse core read: 1 回
- core 内 actual H9 image order: 1 回、coordinate-law preimage: 4 回
- producer: `NormalClosure(A5)` 4 回、`NormalClosure(P)` 4 回
- producer: 4 A5 projections + 4 P projections、bounded `S5` 120 元 search
- checker: A5/P/G9 を各 1 回だけ cache、H9 全元列挙なし、12-dimensional mod-3 linear algebraのみ
- `Elements(A5^4)`: 0、`Size(Group(tuple_generators_in_A5^4))`: 0、A5^4 Cayley table: 0

## 残る境界

この便が与えるのは登録された concrete FC-8* (`S=A5,t=4`) のみであり、canonical/unique first nonabelian factor や B4-B は主張しない。

- OBS-NA / D1 / NA-5: 未供給
- D4/D6 の 5-primary friendly 条件: `5 | |A5|` のため未閉 (`MISSING`)
- full-verbal tower への乗換え: 実施していない
- `K` の isolatedness: 未証明。ただし FV-5 によりこの登録/NA-5適用の前件ではない

## GHA 実行記録（2026-08-19 JST）

- 実装登録 commit: `016cc6560d8f7f1e5680e49a9e6b15fbcf5ed812`
- pinned T-40 正本追加後の実行 commit: `6c5eb06ad4e7745ddb1d9021897c9c24aee233ee`
- 初回 canary run `32153199365`: failure。数学コードへ入る前に、pinned `docs/notes/fullverbal_tower_screening_v1.md` が当該 commit に未収録だったため fail-closed。正本を上記 successor commit に追加した。
- 再 canary run `32153625886`: success。
  - `D972_B4_FC8_CHECKED_IO_SELFTEST_PASS`
  - `D972_B4_FC8_CHECKER_SELFTEST_PASS mutations=12 h9_nakayama_rank=12`
  - `FC8_A5_FOUR_GHA_DRIVER_PASS mode=selftest`
- full run `32153799126`: success。
  - producer terminal: `FC8_A5_FOUR_CHIEF_CROSSCHECKED`
  - independent checker: `S=A5 t=4 CB3=cyclic`
  - producer runtime: `601 ms`
  - receipt SHA-256: `558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584`

従ってこの便の正確な終端は次である。

```text
FC8_A5_FOUR_CHIEF_CROSSCHECKED
```
