# Luna 157c 返書 — P-GRT-1 凍結事前登録

WO-157-3 を完了した。作成物は

- `docs/notes/p_grt1_prereg_l7_w5_v1.md`

である。状態は明示的に **`PREREGISTERED / UNMEASURED`** とし、ℓ=7・重み≤5・一窓

\[
N=(\gamma_6(F_2)F_2^7)\times\langle c\rangle,qquad
P=F_2/(\gamma_6(F_2)F_2^7)
\]

だけを登録した。後発測定の v1/payload への輸入は禁止し、別素数・別重み・別窓は v2 以降を測定前に新設する規則にした。

## 1. 登録した仕様

- verbal power を `G^7=<g^7:g∈G>` と逐語定義。
- Lazard–BCH の 14 次元有限座標 presentation、marked `x,y`、Hall generator `b1..b14`、second-kind 正常形の左→右順を pin。
- `N_ord=7`, `X=[0,1,2,4,5,6]`、LEGAL/charming side gate、full (3.3)(3.4)、reduced (3.10)(3.11)、SURJ を分離。
- PENT frame を `Q5=K(0,5)/(gamma_6(K(0,5))K(0,5)^7)`、generator order、sphere rows、`j`、`rho` 像、5 因子の積順まで pin。
- `PENT_W` を **raw f-only norm 通過集合ではなく `GT(N)` との交差**として定義。raw PENT 個数は `UNKNOWN / NOT_PREDICTED`。
- f-key を Hall exponent 12 桁の big-endian、pair-key を `m_index*7^12+f_index` とし、exact-cover/UNKNOWN policy を固定。
- 予言を変更せず、`|GT(N)|/|X|=2401`, `|PENT_W|/|X|=49` と登録。miss branch は `MOD7_RANK_STEP` と `BRIDGE_OR_NONLINEAR_LIFTING_FAILURE` の二段。
- char-0/mod-7 canary を重み 2–5 の `dim L`, `dim H`, `dim S`, hex rank, restricted-PENT rank で固定。char-0 exact observation と mod-7 observation はともに `UNMEASURED`、不一致は fail closed。

## 2. bytes / digest

| 対象 | bytes | SHA-256 |
|---|---:|---|
| 登録文書全体 | 19,125 | `84a29afa11f16a21aae0e91b5eb1257737fb16030940322ba23b112d55cb1fc4` |
| fenced canonical payload（terminal LF 込み） | 4,050 | `dc7ee417cb2dbfef3a813f62890766afbafb76dce886d0a6b1b693a5d0e57630` |

payload digest は文書内にも同値を記載し、PowerShell による UTF-8/BOM なしの再現手順を添えた。

## 3. 静的チェック

実施したのは読取りと静的整合検査だけである。

1. fenced payload 抽出: PASS。
2. `ConvertFrom-Json`: PASS。
3. literal payload SHA の再計算と文書内宣言値: 一致。
4. UTF-8 BOM: false。
5. placeholder (`TO_BE_FILLED`, `PLACEHOLDER`, `TBD`): 0。
6. scope fields: `ell=7`, `weight_max=5`, `one_window_only=true`, `measurement=none`。
7. `X` と row の `m_order`: ともに `0,1,2,4,5,6`。
8. prediction fields: `GT_N_per_m=2401`, `PENT_W_per_m=49`。
9. `char0_exact_observation=UNMEASURED`, `mod7_observation=UNMEASURED`。
10. 旧 class-4 NW(7) の測定個数を payload に入れていない。

**実行していないもの**: `gap.ps1`、GAP/ANUPQ、Python/Node の群構築・列挙、GT/hexagon/SURJ/PENT 判定、char-0 rank、mod-7 rank、有限窓の個数測定。git 操作も行っていない。

## 4. open assumptions / 格境界

1. `H_w` の char-0 reference は便 156 の裁定どおり candidate。二大素数一致を有理 rank の証明へ昇格していない。
2. graded `H_w/S_w` と有限 `GT(N)/PENT_W` の自由度を対応させる D3(iv) 型 bridge は candidate。拡大類・非線形 lifting・層の貼り合わせは未閉。
3. `Q5` の位数、pc presentation、raw PENT 通過数は UNKNOWN であり、予言の既知入力にしていない。
4. future measurement には marked-presentation 同定、full/reduced hexagon の独立照合、`P→Q5` の `j`、`rho^5`、exact row coverage、UNKNOWN 件数の cert pin が必要。
5. 本登録は有限個数だけを予言し、profinite genuine 性、算術像、全細分 survival、`GT-hat=GT-hat_gen` を主張しない。

LUNA_157C_STATUS: COMPLETE / PREREGISTERED_UNMEASURED
