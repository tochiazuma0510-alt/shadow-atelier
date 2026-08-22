# Luna task 155 — WO-155-1 full-48 independent cross-checker

依頼者: Sol / 2026-08-22

## 0. 役割と禁止

あなたは実装担当 Luna。数学仕様は本書で固定する。producer との著者分離を守るため、次を厳守すること。

- **開封禁止**: `scratchpad/koubou83_A2_48sweep_v*.g`、同 debug/run log、producer の raw `*_rows.jsonl` / `*_witness.jsonl`、producer cert 本体、既存の `crosscheck/check_koubou83_survival_*.py` とその verdict。grep・import・copy も禁止。
- 実行時の judgment data input は下記 witness export 2 本だけ。repo 内 helper を import しない。Python 標準ライブラリだけの自己完結実装にする。
- `search/iso_census83_deep15_data.g` は **登録済み window 定義を開発時に一度抽出する用途だけ**許可する。対象 2 record を checker source 内の定数へ埋め込み、実行時には読まない。source には抽出元 SHA と record 選択規則を記す。
- GAP をローカル実行しない。重い実行/GAP が必要になったら作業を止めて親へ報告する。本仕様は純 Python・ローカル軽量実行で閉じる想定。
- git 操作・credential・workflow 操作は禁止（親 Sol が broker）。
- 他者の dirty worktree を触らない。編集可能パスは本便の納品物だけ:
  - `crosscheck/check_koubou83_A2_full48_v1.py`
  - `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v1_20260822.json`
  - `sol/luna_reply_155_full48_crosscheck.md`

## 1. 唯一の入力 pin

1. p=3 source（v2 のうち **p=3 行だけ**選ぶ）:
   `search/certs/koubou83_A2_48sweep_v2_witness_export_20260822.json`
   SHA-256 `25f902e0e8bbbe7dd8c9c60113eb239cb3b0a8a6d9a9c37491e06f6bfa1f6511`
2. p=2 source（v3 全行）:
   `search/certs/koubou83_A2_48sweep_v3_p2_witness_export_20260822.json`
   SHA-256 `2f665114d8ffcd35383d36a5a3d9a9c3d0dbb36e932cfd52d399913c34ced3e1`

v2 export の p=2 行は単位バグ版なので **検査対象にも根拠にも使わない**（ただし v2 export が p=2 96 行+p=3 96 行を持つ形状 sanity は記録してよい）。二入力以外の producer verdict は読まない。各 selected export row の存在を versioned producer claim `SURVIVES` とする契約を source 内に固定し、独立計算結果と突合する。

## 2. CLAIM-COVER-1（本実装の load-bearing gate）

主張宇宙をコード定数として次の直積に固定する。

`U_claim = {(1152,154161),(1152,154163)} × {shadow_idx=1..48} × {p=2,3}`

checker は selected rows の semantic key `(window, shadow_idx, p)` を multiset として作り、以下を fail-closed assert する。

- `U_check == U_claim` の**要素単位の完全一致**（count 192 だけでは不可）。欠落・余分・重複を別々に列挙。
- 各 `(window,shadow_idx)` で p=2 と p=3 の `m` と `f_xyword` が完全一致。
- source schema、token domain（xy/sigma とも ±1,±2）、型、SHA pin。
- 4 cell（window×p）が各 48 行、全 idx 1..48 を一度ずつ覆う。
- cert に canonical row manifest とその SHA-256、input SHA、checker source SHA、claim contract/predicate version を機械生成して収める。

row manifest は full witness 語を再掲せず、各入力 row の canonical JSON SHA、`f_xyword` SHA、`witness_sigma_word` SHA、長さ、全判定値を持たせる。

## 3. PIN-AB-1 / UNIT-1（逐語仕様）

- `x=σ1^2`, `y=σ2^2`, `Delta=σ1σ2σ1`, `c=Delta^2`。
- `ab(f)=(deg_x f,deg_y f)`。
- σ-word を左から読み、現在の strand label 間の**符号つき生交差数**を数える。pure braid では最終置換が恒等かつ各生交差数が偶数であることを assert。`l_jk = raw_jk/2`。
- `(a,b,gamma)=(l12-l13,l23-l13,l13)`。
- 実行冒頭の必須 4 assert:
  1. `(a,b,gamma)(σ1^2)=(1,0,0)`
  2. `(a,b,gamma)(σ2^2)=(0,1,0)`
  3. `(a,b,gamma)(Delta^2)=(0,0,1)`
  4. raw crossings `(Delta^2)=(2,2,2)`
- UNIT-1: 他素数の通過を単位検査に使わない。上の生成元値だけが pin。

各 row では `f_sigma = expand_xy(f_xyword)`、correction `w = witness_sigma_word`、lift representative `F = f_sigma ++ w` とする。

- legal: `w` が PB3、window の N に属する（下の Phi/evaluation で確認）、かつ `p | gamma(w)`。
- charming: canonical `(a,b,gamma)(F)` に対し
  `p|a AND p|b AND 3|((a+b)/p)`。割り算前に p|(a+b) を assert。
- p=3 では同値な `9|(a+b)`、p=2 では A2-TAUT により第三条件が恒真になることも row-level sanity として記録するが、一般式そのものを評価する。

## 4. hexagon の直接 R 検査（producer 行列を使わない）

`u=2m+1`, `x=[1,1]`, `y=[2,2]`, `c=[1,2,1,1,2,1]`（sigma token）。free-word inverse/power/concatenationを自前実装し、

```
R1(F,m) = sigma1^u F^-1 sigma2^u F c^-m x^m sigma2^-1 sigma1^-1 F
R2(F,m) = F^-1 sigma2^u F sigma1^u F^-1 c^-m y^m sigma1^-1 sigma2^-1
```

を**語から直接再構成**し、両方が `K_p=[N,N]N^p` に属することを検査する。producer の A1/A2/augmented matrix/verdict を再現してはいけない。

### 4.1 自己完結な membership engine

純 Python で以下を独立実装する。

- GAP 形式 a,b word parser（括弧・積・整数冪）と B3→PB3=`F2×<c>` 分解。parser/PBcoords fixture を持つ。
- 登録 window 定義は `search/iso_census83_deep15_data.g`（SHA-256 `75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec`）から開発時に対象 record だけ抽出して source に埋め込む。154161 は id `[1152,154161]` の唯一の record、154163 は id `[1152,154163]` のうち `words[0]` が `a^-6` で始まらない record。runtime file read 禁止。
- pins: `m0(154161)=x^-6`; `m0(154163)=(x^-1 y^-1)^3`。
- embedded relators から HLT 型 Todd–Coxeter を自前実装し `G=F2/N_F2` を構成（両窓 order 192）。
- Fox derivative over GF(p)、`D`、`ker D`、`U_p=(phi-1)ker D`、central coordinate を自前実装。window defining words から V_p basis を greedy に構成。
- expected environment canary:
  - 154161: kappa=2, rankD=191, dimKerD=193, rankU=96, dimV=98
  - 154163: kappa=4, rankD=191, dimKerD=193, rankU=144, dimV=50
  （p=2,3 とも）。all embedded defining words identity、Fox fundamental identity、accepted basis count=dimV を assert。
- `Phi_p(R)` の group evaluation が identity、full tracker remainder が zero、かつ **V-basis coefficient が zero**であることを両 R に要求。**remainder-zero だけを検査してはならない**（旧 CV-9 空虚 checker の再発防止）。

## 5. 対照

### 陽性対照

selected universe 内で、各 window×p について次を semantic identity で一意に拾い、通常 row 全 gate PASS を要求する。

- identity: `m=0, f_xyword=[]`（idx 1 のはずだが、同定は意味値で行う）。
- `[11,1]`: `m=11, f_xyword=[]`（idx 43 のはず）。

### 破壊対照

入力は変更せず memory 上の copy だけを変える。

1. 全 selected row で correction の末尾へ `σ1^2=[1,1]` を追加。pure/evenness は維持するが canonical a が 1 ずれるので overall gate が **192/192 FAIL**することを要求。
2. structure-sensitive control として correction を `w' = x w x^-1`（`x=[1,1]`）へ置換する。`N ⊴ B3` により N 所属を保ち、ab/γ も不変なので legal/charming が保たれることを各行で確認する。`w=[]` の当然の PASS 例外は分離し、非空行で direct R gate が少なくとも 1 行 FAIL することを要求する。全 cell の pass/fail count を cert に記録する（期待値を後付け固定しない）。当初案の correction 末尾への `[x,y]=[1,1,2,2,-1,-1,-2,-2]` 追加は採用しない。この語は両対象窓の N に属さず（独立 quotient evaluation: 154161 で 57、154163 で 85）、legal 維持という対照目的と両立しないためである。

## 6. 出力・再現性

- checker は標準ライブラリのみ、repo helper import なし。
- default 実行で verdict JSON を所定 path へ deterministic に書く。同じ tree で二回実行し byte-identical を確認（現在時刻を埋め込まない）。
- exit 0 は全 mandatory gate PASS のときだけ。FAIL は nonzero かつ cert を残して原因を列挙。
- verdict の用語は `cross-checked candidate` まで。`verified` は使わない。
- summary は少なくとも: selected 192/192、各 cell 48/48、producer-contract 一致数、legal/charming/direct 内訳、coverage exactness、positive controls、destructive controls、environment canaries、overall verdict。
- 実行時間と peak RSS を可能な範囲で測る（RSS が portable でなければ `UNKNOWN` と明記）。ローカルで 60 秒を超えそうなら一度止めて親へ相談。
- `sol/luna_reply_155_full48_crosscheck.md` に、実行 command、exit code、elapsed、3 納品物の bytes+full SHA-256、結果、独立性宣言、開いた入力/正典一覧、未解決を記す。

完了後は git 操作をせず、親へ結果を返すこと。
