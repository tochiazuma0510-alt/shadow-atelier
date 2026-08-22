# Luna 返書 157b — WO-157-2（83 checker v2）

## 1. 結果

指定された v1 / v1_1 を変更せず、次版を実装した。

- `crosscheck/check_koubou83_A2_full48_v2.py`
  - W-1 の非可換 `B3` fixture を mandatory / fail-closed gate として追加。
  - 同一 fixture で正しい paper-aware 語順を陽性、旧 raw/GAP 語順を陰性 canary として評価。
  - `ad_convention` を source SHA を含めて実行時に機械生成。
  - schema と verdict path を v2 化。
- `scratchpad/koubou83_c3lift_check_v1_2.g`
  - stale comment の「ker χ は m=0 のみ」を `m∈{0,N_ord/2}`（本窓では `{0,6}`）へ訂正。
  - `m=0 so u=1` を「`m=0 or 6`, literal `u=1 or 13`」へ訂正。
  - GAP 側にも同じ W-1 三重 gate、`ad_convention` writer、runtime source SHA を追加し、schema/cert path を v1_2 化。
- `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v2_20260823.json`
  - Python v2 本走行の verdict。`summary.overall = PASS`。

格は従来どおり **candidate / cross-check** であり、Lean `verified` ではない。

## 2. W-1 semantic gate

fixture は

`B3 = <sigma1,sigma2 | sigma1*sigma2*sigma1 = sigma2*sigma1*sigma2>`、
`x=sigma1^2=[1,1]`、`y=sigma2^2=[2,2]`

で固定した。語配列の `±1,±2` はそれぞれ `sigma1^{±1},sigma2^{±1}`。paper 積 `A*B` は W-1 helper `paper_product` により raw 語 `B*A` へ写す。

- paper `f1=y*x^-1` の raw/GAP-order 語: `[-1,-1,2,2]`
- 旧誤形 raw `y*x^-1`: `[2,2,-1,-1]`
- 正しい評価:
  - translated LHS = RHS = `[-1,-1,2,1,1]`
  - 差の PB3 正規形 = `F2 word=[]`, `c-power=0`
  - `positive_identity_pass=true`
- 旧誤形 canary:
  - LHS と正しい RHS の差 = `F2 word=[2,-1,-2,-1,-2,1,2,1]`, `c-power=0`
  - `equal=false`, `former_error_rejected=true`
- 非中心性 canary:
  - paper `Ad(x)(sigma2)` と `sigma2` の差 = `F2 word=[-1,-2,-1]`, `c-power=1`
  - `equal=false`, `noncentral_fixture_pass=true`

比較は同置換の B3 語を既存 checker 内の厳密 PB3 正規形 `(F2 word,c-power)` に落として行う。例外を soft-pass に変える枝はなく、三条件の一つでも偽なら assert と最終 `overall` の双方が閉じる。

## 3. `ad_convention` pin

verdict の `ad_convention` は少なくとも次を実行時生成する。

- `paper_ad_x(u) = x*u*x^-1`
- `gap_power_convention = u^x=x^-1*u*x`
- Python v2 の実装ラベル `paper_ad_x` と evaluator `paper_product(x,u,x^-1)`
- companion GAP の raw label の意味:
  - `matches_adx = raw x*u*x^-1 = GAP u^(x^-1) = paper Ad(x^-1)`
  - `matches_adx2 = raw x^2*u*x^-2 = GAP u^(x^-2) = paper Ad(x^-2)`
- 位数 3 の `P/Phi(P)` action class 表:
  - `nu=0 -> action_is_id`
  - `nu=1 -> matches_adx2`
  - `nu=2 -> matches_adx`
- 非中心 fixture の assert 結果
- `word_convention_id = W-1/paper-product-to-raw-reversed/v1`
- `action_convention_id = paper-Ad-vs-GAP-power/order-3-action/v1`
- checker source SHA-256（runtime 計算。source 内への digest 埋込みなし）

action class 表の射程は、明記したとおり **位数 3 の `P/Phi(P)` 上の作用**である。

## 4. 実行と検査

| command | exit | 結果 |
|---|---:|---|
| `python -m py_compile crosscheck/check_koubou83_A2_full48_v2.py` | 0 | Python 構文 PASS |
| `python crosscheck/check_koubou83_A2_full48_v2.py` | 0 | 9.6 秒、`overall=PASS`; 192/192 coverage/legal/charming/direct、既存 controls、W-1、ad pin 全 PASS |
| Python による v2 JSON の schema/source-SHA/W-1/ad table assert | 0 | JSON parse と全 pin 一致 |
| `python -m json.tool crosscheck/verdicts/koubou83_A2_full48_crosscheck_v2_20260823.json` | 0 | JSON syntax PASS |
| `git diff --exit-code --`（v1 source、v1_1 GAP source、v1 verdict） | 0 | 旧証拠物の変更なし |
| `.\gap.ps1 scratchpad\koubou83_c3lift_check_v1_2.g` | 1 | GAP が source 評価前に `fatal error - couldn't create signal pipe, Win32 error 5`。v1_2 GAP cert は未生成 |

Python verdict の主要 summary は次のとおり。

```json
{
  "overall": "PASS",
  "selected_192_192": true,
  "legal_192_192": true,
  "charming_192_192": true,
  "direct_R_192_192": true,
  "destructive_controls_pass": true,
  "w1_semantic_gate_pass": true,
  "ad_convention_complete": true
}
```

## 5. bytes / SHA-256

| path | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_koubou83_A2_full48_v2.py` | 31966 | `2d39246d51afbba07b3c7419016586da55e367d1cd18a222e90bdc4212a8426a` |
| `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v2_20260823.json` | 220494 | `03a0f1c1e0f42b17bbc9e26e6f04b40311662fb8d7c45f3f5cc9442c5a70046b` |
| `scratchpad/koubou83_c3lift_check_v1_2.g` | 28353 | `5737dee0808b6117eb5438bf5acee1fcd218d61aaee2012d8ce3f62ed50c3f35` |

旧版保持の機械確認:

| preserved path | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_koubou83_A2_full48_v1.py` | 26805 | `519fddc25618d5f84f2b3d9e395cf1ce10b9116537ae4f41e47a3f2c1e7e347d` |
| `scratchpad/koubou83_c3lift_check_v1_1.g` | 24599 | `07f682df0ce70b1f6569b1b325381cb4c7abaacd7cba5ed4ce522ec28ed33634` |
| `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v1_20260822.json` | 216454 | `a144249b323774a2ecb18c1250a86b8fbe0b3a2a7fad379eb8be3404598898d5` |

## 6. 限定・再走コマンド

唯一の未完了検査は GAP v1_2 の runtime 走行である。失敗は checker の parse/evaluation より前の GAP/Cygwin signal-pipe 初期化で起き、source 由来のエラーとは判定できない。この環境状態が解消した後の再走コマンドは次である。

```powershell
.\gap.ps1 scratchpad\koubou83_c3lift_check_v1_2.g
python -m json.tool search/certs/koubou83_c3lift_indepcheck_v1_2_20260823.json
```

成功時には v1_2 source が `search/certs/koubou83_c3lift_indepcheck_v1_2_20260823.json` を生成し、W-1/ad pin と runtime source SHA を収録する。現時点ではこの GAP cert の存在・PASS を主張しない。

LUNA_157B_VERDICT: PYTHON_V2_PASS; GAP_V1_2_IMPLEMENTED_BUT_RUNTIME_BLOCKED_BEFORE_SOURCE_EVALUATION; CANDIDATE_NOT_VERIFIED
