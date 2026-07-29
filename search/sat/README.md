# SAT 線(W6): 証明書つき SAT パイプライン

ES7(`atelier_lean/ES7/abstract_sat/` + `.github/workflows/es7_abstract_sat.yml` /
`es7_sat_matrix.yml`)からの輸入。器のみ — encoder(F2 三条件/巡回型制約の CNF 化)は
まだ未着手(標的選定は Sol 便 84 ⑥ の返答待ち、2026-07-29 時点)。

## パイプライン

workflow: `.github/workflows/sat-run.yml`(`workflow_dispatch` 手動発火・push はしない)。

```
CNF(.cnf / .cnf.gz)
  -> sha256 ゲート(cnf_sha256 を渡した場合のみ照合。改竄・取り違え防止)
  -> kissat 実行(--no-binary で proof.drat を出力)
  -> exit 10 (SAT) : "^v " 行を model_vlines.txt に抽出
     exit 20 (UNSAT): drat-trim で proof.drat を独立検証
                       -> "s VERIFIED" が出なければ即 fail
                       -> core.cnf(UNSAT core)と proof.lrat(LRAT 証明)を保存
     それ以外        : verdict=UNKNOWN として証明書化(何も検証せずに終わらせない)
  -> 全成果物の SHA-256 を SHA256SUMS.txt に記録
  -> out_dir + ci/out/ を artifact upload
```

### 入力(inputs)

`gap-run.yml` の作法(script/preamble/out_dir/timeout_min)に合わせている。

| input | 必須 | 既定値 | 意味 |
|---|---|---|---|
| `cnf_path` | ○ | — | CNF の repo 相対パス(`.cnf` または `.cnf.gz`) |
| `cnf_sha256` | – | `""` | 展開後 CNF の期待 SHA-256。空なら整合ゲートをスキップ(その場合は run.log に出る sha256sum の値を後から手動で台帳に記録すること) |
| `solver_args` | – | `""` | kissat への追加 CLI 引数(空白区切りでそのまま末尾に付与) |
| `out_dir` | – | `search/sat/out` | 成果物を集約するディレクトリ |
| `timeout_min` | – | `60` | job のタイムアウト分 |

kissat / drat-trim は毎回ソースから clone してビルドする(ES7 の yml と同じ方式。
バイナリキャッシュはしていない — 変えたい場合は明示的に相談)。

## 証明書の読み方

出力(`ci/out/` および `out_dir/`)は以下の一式:

- `result.txt` — `exit=<code>` と `verdict=SAT|UNSAT|UNKNOWN`
- `kissat_out.txt` / `kissat_time.txt` — solver の標準出力と `/usr/bin/time -v` の資源使用ログ
- `model_vlines.txt`(SAT 時のみ)— kissat が出した `v ...` 行(充足割り当て)。**これは
  未検証の主張** — 独立照合器で CNF に代入して全節を満たすか再計算するまでは
  「照合済み」と呼ばない
- `proof.drat.gz`(UNSAT 時のみ)— DRAT 反駁証明(生ログ、gzip 圧縮)
- `drat_verify.txt`(UNSAT 時のみ)— drat-trim の検証出力。`s VERIFIED` が必須(なければ
  workflow が fail する設計 — UNSAT 主張が検証なしで通ることはない)
- `core.cnf.gz`(UNSAT 時のみ)— drat-trim が抽出した UNSAT core
- `proof.lrat.gz`(UNSAT 時のみ)— LRAT 形式の証明(将来 Lean 側の checker に渡す想定の
  正本フォーマット)
- `SHA256SUMS.txt` — 上記全ファイルの SHA-256(出所管理・`provenance/LEDGER.md` へ転記
  する際の一次ソース)

## 急所: UNSAT 主張は encoding 忠実性が生命線

drat-trim の `s VERIFIED` は「この CNF から矛盾が導ける」ことしか保証しない。
**元の数学的主張(F2 三条件・巡回型制約など)が正しく CNF にエンコードされているか
は、この pipeline の外側の話**であり、SAT ソルバーも drat-trim も一切関知しない。
エンコードにバグがあれば、無意味な CNF に対して完璧に検証された UNSAT 証明が出る
(= 偽陰性/偽陽性の温床)。したがって:

- encoder を書いたら、**独立実装の照合器**(node/python、encoder のコードを import
  しない別実装)で「小さな具体例をエンコードして手計算/全探索と突き合わせる」テスト
  を先に通すこと(探索器と照合器の分離規律。CLAUDE.md 参照)。
- SAT の場合も同様: `model_vlines.txt` の割り当てを、encoder とは独立に元の数学的
  対象へ逆変換し、求める性質を満たすか再確認するまでは結果を確定させない。
- この意味で「照合済み(cross-checked)」は名乗れるが「検証済み(verified)」は
  Lean 化して初めて名乗れる(CLAUDE.md の語法規約)。

## 煙試験(smoke test)

`search/sat/smoke/` に自明な CNF を 2 本置いてある(workflow の動作確認用。数学的な
主張は何もない):

- `trivial_sat.cnf` — `p cnf 1 1` / `1 0`(x1=true で充足。SAT のはず)
- `trivial_unsat.cnf` — `p cnf 1 2` / `1 0` / `-1 0`(x1 と ¬x1 を同時要求。UNSAT のはず)

SHA-256(このリポジトリに commit された内容に対する値。workflow 発火時に
`cnf_sha256` として渡せば整合ゲートを試せる):

```
trivial_sat.cnf:   ba9b246dc0b01a6b5cb936d521bd426feb79b84df2f921103b0c07ba4c29a3dc
trivial_unsat.cnf: ab97e6c2fc8e5717bf279716a4f333951300385bf188b90ac1749fdd9fd6910d
```

### 動作確認手順(CI 発射は司令塔が行う — 実装担当はここまで用意する)

1. GitHub Actions の `sat-run` workflow を `workflow_dispatch` で手動発火。
2. SAT 側の確認: `cnf_path=search/sat/smoke/trivial_sat.cnf`,
   `cnf_sha256=ba9b246dc0b01a6b5cb936d521bd426feb79b84df2f921103b0c07ba4c29a3dc` を指定。
   → `result.txt` に `verdict=SAT`、`model_vlines.txt` に `v 1 0`(または同等)が
   出ることを確認。
3. UNSAT 側の確認: `cnf_path=search/sat/smoke/trivial_unsat.cnf`,
   `cnf_sha256=ab97e6c2fc8e5717bf279716a4f333951300385bf188b90ac1749fdd9fd6910d` を指定。
   → `result.txt` に `verdict=UNSAT`、`drat_verify.txt` に `s VERIFIED`、
   `core.cnf.gz` と `proof.lrat.gz` が artifact に含まれることを確認。
4. どちらも `SHA256SUMS.txt` が出力に含まれ、成果物一式のハッシュが揃っていることを
   確認してから `provenance/LEDGER.md` へ転記する。

## 第一標的 n=21(裁定 210 工程 1-B・Sol 便 84 sec 6.2)

標的選定は Sol 便 84 ⑥ の回答(優先順 (c) n=21 UNSAT calibration → (b) ℓ=17,n=25
existence → (a) dl≥3 shadow witness)に従い、(c) を実装した。設計は
`sol/sol_reply_84_math11.md` sec 6.2/6.5 準拠(節の丸写しでなく、以下の実装ファイル
のドキュメント文字列内に一次設計根拠として引用している)。

### 成果物

- `encode_tail8_n21.py` — 探索器側。固定 u=(1..13)(14 15)(16 17)(18 19)(20 21) の
  もとで、a を involution (matching 変数 X_ij=X_ji + 対角 D_i)、b=a·u⁻¹ を Tseitin
  導出の 21×21 行列 B、b³=1・fixed-point-free で型 3⁷ を強制し、推移性は点 1 からの
  bounded BFS (t=0..20 の reachability 変数 R、STEP Tseitin 変数)で符号化する。
  2 本の DIMACS を出力: `out/tail8_n21_class.cnf`(class 制約のみ・SAT 期待、
  672 変数・14806 節)と `out/tail8_n21_transitive.cnf`(+ 推移性・UNSAT 期待、
  9723 変数・50128 節)。構造定数 4160 や C(u)-軌道は公理に入れない(外部 oracle)。
  `--manifest-out` で `manifest_tail8_n21.json` を自己生成する(手打ち転記なし)。
- `manifest_tail8_n21.json` — 上記 encoder が自分の内部状態から機械生成した証明書
  マニフェスト(宇宙・固定 u・積順規約・変数族ごとの ID 範囲・制約グループごとの
  節番号範囲・symmetry reduction の申告・encoder ソース SHA-256)。
  `completeness 補題は別監査(未)` と明記(Sol 6.5 点 7)。
- `check_model_n21.mjs` — 照合器側(node、**encoder を import しない**独立実装・
  言語も分離)。kissat の `v ...` 行を読み、decode した a,b について
  involution 型 2¹⁰1・b=u⁻¹(a(·)) の再計算・b³=1・fixed-point-free・型 3⁷・
  (transitive モードのみ)点 1 からの独自 BFS 推移性、を全て**モデルの
  B/E/STEP/R 変数を信用せず**再計算して検査する。`--self-test` で
  `fixtures/witness_n21_nontransitive.json`(GAP の bounded random search で
  機械抽出した実 witness、`scratchpad/extract_witness_n21.g` 由来、手写しなし)を
  読み、class 制約は満たし・推移性は GAP 報告どおり false になることを較正する。
- `mutants_n21.json` — Sol 6.5 の変異列挙(b=au⁻¹ 左右反転・u⁻¹ 落とし・
  対角 exactly-one 落とし・b³=1/fpf 落とし・推移性丸ごと落とし・BFS depth 1-off・
  settled 落とし=第三標的なので N/A)を、期待 SAT/UNSAT と根拠(PROVEN/REASONED/
  UNKNOWN の確信度つき)・decoded 反例に期待する性質まで事前登録した。UNKNOWN の
  行は「ソルバー結果が出ても単独では信用しない・小規模オラクルで裏取りが要る」と
  明記してある。
- `fixtures/witness_n21_nontransitive.json` — 上記較正専用の GAP 機械抽出 witness
  (悉皆census である `tail8_exact.g` の代替にはならない。5 軌道代表の 1 個ではなく、
  bounded random search で独立に見つけた 1 個で、たまたま同じ軌道分割 [6,15] を
  持つことを確認した — この一致自体が非独立な `tail8_exact.g` 依存ではないことの
  傍証)。

### ローカル煙試験で確認したこと(kissat 実行なし・CI 側で実施)

```
python search/sat/encode_tail8_n21.py --manifest-out search/sat/manifest_tail8_n21.json
  -> class_cnf:      672 vars, 14806 clauses
  -> transitive_cnf: 9723 vars, 50128 clauses
  (manifest の各 clause group start/end と一致)

node search/sat/check_model_n21.mjs --self-test
  -> pass:true (witness fixture を class 制約 OK・推移性 false=GAP 報告と一致
     と判定)
```

さらに、encoder が実際に書き出した DIMACS ファイル(生成されたコード経由ではなく
ファイルそのもの)を、fixture から独立に構築した割当てで評価する追加スクリプトを
scratchpad に置いて実行した(node、encoder 非 import):

- `tail8_n21_class.cnf` 全 14806 節 → 0 節違反(fixture が真に生成 CNF#1 を
  充足することを確認)。
- `tail8_n21_transitive.cnf` 全 50128 節 → 違反はちょうど 6 節、かつ
  transitivity goal 節群(節番号 50108-50128 のうち末尾 6 本)に一致し、
  独立 BFS が報告する未到達点 [16,17,18,19,20,21] と 1 対 1 対応した。
  推移性以外の 50122 節は honest な割当てで全て充足 — class+BFS の配線が
  ソルバーを一切呼ばずに整合していることの強い状況証拠。

kissat/drat-trim のローカル実行は RAM 8GB 制約により行っていない(CI で実施)。

## workflow 硬化(2026-07-29)

`.github/workflows/sat-run.yml` を Sol 便 84 sec 6.5 点 1-3 に従い改修した:

1. kissat / drat-trim / actions/checkout / actions/upload-artifact を tag でなく
   commit SHA に pin(2026-07-29 時点の各 `master`/`v4` HEAD)。
2. 新規 `run_label` 入力(`calibration` / `theorem`)。`theorem` を選ぶと
   `cnf_sha256` 空欄で fail-fast する検証ステップを追加(理論的主張に使う run は
   改竄検知ゲートを迂回できない)。
3. `cnf_path` / `out_dir` / `solver_args` を allowlist 正規表現で検証したうえで
   bash 配列(`read -ra`)経由で kissat に渡すよう変更 — 自由な shell 展開・
   コマンド注入・パス脱出を防ぐ。

未着手(Sol 6.5 点 4): drat-trim 自身とは別の独立 LRAT checker で証明を再読する
工程はまだ配線していない。

## 未着手(次段)

- 標的 (b) ℓ=17,n=25 existence: 同じ encoder family を 2-transitive BFS へ
  parameter 変更するだけで済む(Sol 6.3)。
- 標的 (a) dl≥3 shadow witness: settled/well-definedness・(3.53) composition・
  二重交換子非自明性を含む別世代の encoder が必要(Sol 6.4)。着手していない。
- kissat/drat-trim バイナリのキャッシュ化(現状は毎回ソース clone + ビルド)。
- drat-trim とは独立な LRAT checker(Sol 6.5 点 4)。
- completeness 方向(数学 witness ⇒ CNF assignment)の紙上補題の別監査
  (manifest に「未」と明記済み・数学者担当)。
