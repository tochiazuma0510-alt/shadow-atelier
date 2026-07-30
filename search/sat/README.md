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

## 三段 checker 体制と solver 選択(2026-07-31 追加・ideas_013 §2.1/§2.2)

UNSAT 主張は三段構えで独立に確かめる(どの段も他段のコード・中間状態を import しない
— 探索器/照合器の分離規律のまま三段に拡張しただけ):

1. **drat-trim**(`sat-run.yml`、現用)— proof.drat を生成した直後に自分自身の
   DRAT checker で検証(`s VERIFIED`)。生成側と同じツールなので「自己検証」の域。
2. **`lrat_check.py`**(このディレクトリ、現用)— drat-trim が出した proof.lrat
   だけを入力に、drat-trim のコードを一切読まない自前 python 実装で再検算。
3. **cake_lpr**(`.github/workflows/lrat-recheck.yml`、新規・`workflow_dispatch`)—
   CakeML でバイナリまで形式検証された checker(SAT Competition 2025 公式)で
   `search/sat/runs/` に収蔵済みの UNSAT run を遡及的に再検査する。commit SHA pin
   に加え、upstream 同梱の `cake_lpr.sha256` でソースファイル自体の sha256 も検証
   してからビルドする(二重ピン)。fail-closed 負例(hint id を存在しないクローズ
   ID に書き換えた破壊 LRAT)が正しく `NOT_VERIFIED` になることも同 workflow 内で
   確認する。判定は各 run ディレクトリの `cakelpr_result.txt` に
   `verdict=VERIFIED|NOT_VERIFIED` として記録(3 系統一致でも語彙は
   cross-checked どまり — 「検証済み(verified)」は Lean 専用)。

`sat-run.yml` の solver 選択(`workflow_dispatch` の `solver` 入力、既定 `kissat`):

- `kissat`(既定・無変更): 従来どおり DRAT を出して drat-trim で LRAT に変換。
- `cadical`: CaDiCaL 2.x(commit SHA pin)を `--lrat` オプション付きで実行し、
  LRAT を **solver から直接**出力(drat-trim 変換段を飛ばす)。出力先の
  `proof.lrat.gz` は kissat 経路と同じファイル名・同じ SHA256SUMS.txt 規約なので、
  `lrat_check.py` にも `lrat-recheck.yml` の cake_lpr 段にもそのまま渡せる。
  UNSAT 時の core 抽出は cadical 経路では省略(native LRAT があるため drat-trim
  自体を呼ばない)。incremental(iCNF)配線は未着手(次の実弾の encoder
  fragment 化と同時に設計 — `sat-run.yml` 冒頭コメントの TODO 参照)。

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

Sol 6.5 点 4(drat-trim 自身とは別の独立 LRAT checker)は裁定 214 工程 4 で実装済み
(`search/sat/lrat_check.py`、下記「CI artifact の収蔵と n=21 の cross-check」節)。
CI workflow への自動配線(theorem run で必須段にする)はまだ未着手 — 現状は手動実行。

## CI artifact の収蔵と n=21 の cross-check(裁定 214 工程 4・2026-07-30)

Sol 便 85 §8(`sol/sol_reply_85_math12.md` F85-8.1〜8.5・P85-6)への対応:

- **artifact 収蔵**: run `30454823288`(class, SAT)・`30454826413`(transitive, UNSAT、
  同一 commit `0b148018a058efdbdd2737a375de76853189e0f6`)を `gh run download` で取得し
  `search/sat/runs/n21_class/` / `search/sat/runs/n21_transitive/` に配置。ハッシュ・
  kissat/drat-trim の pin commit・CNF sha256 の manifest との一致は
  `search/sat/runs/RUNS_LEDGER.md` に機械出力で記録。
- **completeness 補題の収蔵**: Sol が便 85 §8.2/8.3 で供給した証明(witness ⟹ CNF
  assignment の 6 段+固定 u で十分な理由)を `docs/notes/sat_completeness_n21_v1.md` に
  正典転記(paper-proof PASS・Sol 供給・数学者未監査、と明記)。
- **独立 LRAT checker**: `search/sat/lrat_check.py`(drat-trim を import しない、
  ゼロから実装した LRAT checker。reference `lrat-check.c` のアルゴリズム — leading
  RUP hint による直接証明を先に試み、失敗したら pivot の RAT ブロックを"累積 trail"
  (leading run の結果を全ブロックで共有し、各ブロック固有の追加仮定だけをロールバック)
  で検査、negative marker の完全性は文字通り信用せず literal occurrence index で
  独立に確認 — を踏襲)。`--self-test` で 3 ケース(純 RUP・意図的に壊れた証明の拒否・
  fresh pivot の vacuous RAT)を確認済み。実物の
  `search/sat/runs/n21_transitive/proof.lrat.gz`(33626 行)に対し実行し
  `s VERIFIED`(3.3 秒)を得た — drat-trim 自身の `drat_verify.txt` の `s VERIFIED`
  と**独立実装で一致**。改竄コントロール(1 ヒント id を破壊したコピー)では
  即座に `s NOT VERIFIED` を返すことも確認(fail-closed の動作確認)。
  **theorem run(`run_label=theorem`)の必須段として、この独立 LRAT checker を
  proof.lrat に対して実行し合格することを要求する**(まだ `.github/workflows/sat-run.yml`
  への自動配線はしていない — 現状は手動実行。配線は次段)。
- **mutant matrix の増強**: `search/sat/mutants_n21.json` に M8〜M12 を追加
  (Sol P85-6 の優先順どおり): M8/M9 = reverse-clause-drop mutant(reachability/edge、
  `search/sat/gen_mutants_reverse_drop.py` でローカル生成)、
  M10 = 21 頂点 path の合成 diameter-20 境界 fixture(`search/sat/encode_diam20_path21.py`、
  M6 を置換 — M6 自体は削除せず「弱い」との Sol 評価つきで歴史行として保持)、
  M11 = n=5,7 の itertools 悉皆較正
  (`search/sat/calibrate_small_n.py`、ローカル実走・秒単位、n=5 は encoding-fidelity
  spot check 0 節違反、n=7 は u=7-cycle でのこの制約下で witness 皆無という悉皆の
  誠実な陰性結果)、M12 = 独立 LRAT checker そのものの登録(上記)。
  **M8/M9/M10(depth19・depth20)は 2026-07-29 に `sat-run` workflow で実走済み**
  (run ID `30462013453`/`30462017651`/`30462021827`/`30462026033`、head SHA
  `5be1f07b579c01c1537725f61f79b64f56e5a3f1`)— M8 SAT・M9 SAT・M10-depth19
  UNSAT(drat-trim + 独立 `lrat_check.py` の両方が `s VERIFIED`)・M10-depth20 SAT、
  4/4 とも紙上 PROVEN prediction と一致。artifact は
  `search/sat/runs/n21_m8_reach_drop/`・`n21_m9_edge_drop/`・`n21_m10_depth19/`・
  `n21_m10_depth20/` に収蔵、台帳は `search/sat/runs/RUNS_LEDGER.md`(裁定 227・
  Sol `sol_reply_86_math13.md` P86-4 への対応。同便 F86-3.3 は先行版の「4/4
  完走」claim を artifact 未収蔵につき FAIL としていた — 本収蔵で解消)。
  M8/M9 は `check_model_n21.mjs --mode transitive` を実 model に対して実行し、
  事前登録どおり「decoded a,b は妥当だが生成群が非推移的(orbits [6,15])」という
  caught-bug signature を確認。M10-depth20 は checker のフィールド前提
  (X/D/B が実 witness に配線されている)が成立しないため対象外(理由は
  `check_model_output.txt` に明記)。
- **depth20 の独立 clause checker(2026-07-31・P87-5 item 3・
  `sol/sol_reply_87_math14.md` F87-1.6)**: `check_model_n21.mjs` が対象外の
  M10-depth20 について、意味論を一切知らない汎用 DIMACS clause 評価器
  `search/sat/tools/verify_generic_cnf_model.mjs` を追加した(`problem.cnf` の
  `p cnf`/節と kissat の `v` 行だけを読み、全節を独立に再評価する。X/D/B の
  配線状態には依存しない)。`node search/sat/tools/verify_generic_cnf_model.mjs
  search/sat/runs/n21_m10_depth20/problem.cnf
  search/sat/runs/n21_m10_depth20/model_vlines.txt` の出力
  (`nvars=9723, declared_clauses=34692, parsed_clauses=34692, assigned=9723,
  missing_vars=0, unsatisfied_count=0`)を
  `search/sat/runs/n21_m10_depth20/clause_checker_output.txt` に収蔵し、
  `SHA256SUMS.txt` / `search/sat/runs/RUNS_LEDGER.md` に反映した。この数値は
  Sol が便 87 監査で独自に報告した値と一致する(Sol のチェッカーコードは
  import していない — 問題設定だけを共有する独立実装)。

## 第二標的 n=25, ℓ=17(裁定 214 系・commander task・Sol 便 84 sec 6.3)

n=21 encoder(`encode_tail8_n21.py`)を Sol 便 84 sec 6.3 の passport へ転用した。固定
u=(1..17)(18,19)(20,21)(22,23)(24,25)、a: 型 2¹²1、b=a·u⁻¹: 型 3⁸1(**n=21 と違い
fixed-point-free でなく厳密に固定点 1 個** — b の対角に a の D[i] と同型の
global exactly-one 制約を張って強制)。目標は単純推移性でなく **2-transitivity**
(順序対 600 個への対角作用の推移性) — Sol 6.3 の議論(u² が 17-cycle・Jordan の
定理・a,b が偶置換)により、この passport では 2-transitive ⟺ ⟨a,b⟩=A₂₅。

### 重要な先行結果: witness が SAT パイプライン外で既に見つかった

encoder 実装前の較正として一様ランダム探索(`tools/extract_witness_a25.g`、
n=21 の `extract_witness_n21.g` と同型)を budget 5,000,000 で試したが
NOT_FOUND だった。原因を GAP の指標表(`CharacterTable("Symmetric",25)`、1958
類)で厳密計算したところ、この固定 u に対する class-only 解の個数は
**厳密に 82688 個**(`tools/structure_const_a25.g`、class multiplication
coefficient 由来)、|class(2¹²1)|=7,905,853,580,625 に対する的中率
≈1.05×10⁻⁸ — 一様ランダムでは 10⁸ 回超必要と判明した。そこで
simulated-annealing 局所探索(`tools/local_search_a25.g`、12 対の組み替え+
固定点移動を近傍とし、b の非 3-cycle 点数を目的関数に)に切り替えたところ
**16824 手で収束**。

この witness は class 制約だけを狙ったにもかかわらず、**副産物として
2-transitive でもあった**: GAP は ⟨a,b⟩ の位数を
7,755,605,021,665,492,992,000,000 = 25!/2 = |A₂₅| と報告し(=⟨a,b⟩=A₂₅)、
これと完全に独立な Python(`scratchpad/verify_a25_witness.py`、GAP 非依存・
非 import)による無制限(depth cap なし・fixpoint まで反復)BFS が、
点対 (1,2) から出発して 600 個の順序対**全て**に到達することを確認した
(真の BFS 直径 43)。つまり **n=25, ℓ=17 の存在問題(標的 (b))は、SAT/DRAT
パイプラインを介さずに、直接構成+独立照合という自己完結した形で既に解決
している**(`fixtures/witness_a25_2transitive.json` に機械記録)。

### CNF 生成物と depth 上界の sizing 分析

- `encode_a25.py` — class 制約 CNF(`out/a25_class.cnf`、950 変数・25002
  節・SAT 期待・厳密解数 82688)と、2-transitivity 付き CNF
  (`out/a25_2transitive_depth{D}.cnf`)の 2 本を出す。後者は n=21 の
  E[i,j]+STEP 方式(N 頂点の**任意対**隣接)をそのまま 600 頂点(順序対)へ
  拡大すると O(N⁴) 変数に爆発するため、**座標を 1 つずつ relabel する
  2 段 Tseitin 分解**(生成元ごとに TEMP[i'][j] → RNEW[i'][j'])で
  O(N³)/生成元/timestep に抑えた自前設計を実装した。
- **depth 上界は「保守的完全性」を保てなかった**: 厳密に完全な上界は
  N(N-1)-1=599(600 頂点の任意連結グラフの直径上界)だが、実測クレーズ数は
  1 timestep あたり約 374,375 節・約 96,250 変数(3 生成元合計) — depth=48
  で総節数 ≈1800 万・変数 ≈462 万・生の CNF ファイルサイズ推定 ≈325MB
  (GitHub の 1 ファイル 100MB 上限を超過)。depth=43(実測されたただ 1 個の
  witness の真の直径)でも同程度の規模になる。したがって **depth=48(あるいは
  それに近い値)を「完全性を保った上界」として commit することはできなかった**
  — これは CLAUDE.md の「宇宙の事前登録・絞りが必要なら実装せず報告」に該当する
  局面であり、司令塔へ報告済み(下記)。
- 実際に commit したのは **depth=5**(`out/a25_2transitive_depth5.cnf`、
  482825 変数・1,898,102 節・35MB)— これは真の直径 43 よりはるかに浅く、
  **existence を判定する目的では情報量がない**(depth 不足による UNSAT は
  非存在の証拠にならない)。目的はもっぱら encoder+checker のパイプライン
  疎通確認(machinery calibration)であり、`mutants_a25.json` の
  M5 に明記した。
- `manifest_a25.json` — 上記 encoder が自己生成。`depth_bound` 節に
  「REASONED, NOT PROVEN」の完全性ステータスと sizing 根拠を明記。
- `check_model_a25.mjs` — 照合器(node、encoder 非 import)。class 側は
  n=21 と同型の再計算(a 型 2¹²1・b=u⁻¹(a(·))・b³=1・**固定点ちょうど1個**)。
  2-transitive 側は CNF の depth-bounded な TEMP/RNEW/R 変数を一切読まず、
  **無制限(depth cap なし)の独自 BFS**で 600 順序対到達を再計算する —
  CNF の depth 上界が「REASONED, NOT PROVEN」である以上、この checker の
  無制限 BFS だけが 2-transitivity 判定の信頼できる審判である。
  `--self-test` で `fixtures/witness_a25_2transitive.json` を読み、
  class 制約 OK・2-transitive TRUE・直径 43 の一致を確認済み(pass:true)。
- `mutants_a25.json` — n=21 の M1-M5 相当を本標的の差分(b は
  fixed-point-free でなく exactly-one-fixed-point、推移性でなく
  2-transitivity)に合わせて再登録。M5 で depth=5 の非情報性を事前登録。
- `fixtures/witness_a25_2transitive.json` — 上記 witness 一式(a,b,u の
  images・GAP 群位数・Python 独立 BFS 結果・厳密解数 82688 の一次資料)。

### ローカルで確認したこと

```
python search/sat/encode_a25.py --class-only --manifest-out ... (fixture 検算込み)
  -> class_cnf: 950 vars, 25002 clauses

node search/sat/check_model_a25.mjs --self-test  -> pass:true

node scratchpad/verify_a25_class_cnf.mjs
  -> out/a25_class.cnf の実ファイルを fixture 由来の割当てで評価:
     25002/25002 節、違反 0

GAP: |<a,b>| = 7755605021665492992000000 = 25!/2 = |A_25|
Python(GAP 非依存): 順序対 BFS が 600/600 到達、真の直径 43
```

kissat/drat-trim のローカル実行は行っていない(RAM 8GB 制約・CI で実施)。

## 未着手(次段)

- 標的 (b) ℓ=17,n=25 existence: 同じ encoder family を 2-transitive BFS へ
  parameter 変更するだけで済む(Sol 6.3)。
- 標的 (a) dl≥3 shadow witness: settled/well-definedness・(3.53) composition・
  二重交換子非自明性を含む別世代の encoder が必要(Sol 6.4)。着手していない。
- kissat/drat-trim バイナリのキャッシュ化(現状は毎回ソース clone + ビルド)。
- 独立 LRAT checker(`search/sat/lrat_check.py`)を CI workflow の theorem run に
  自動配線する(裁定 214 工程 4 時点では実装済み・手動実行のみ)。
- completeness 方向(数学 witness ⇒ CNF assignment)の紙上補題は Sol 供給分が
  `docs/notes/sat_completeness_n21_v1.md` に収蔵済み(paper-proof PASS)だが、
  数学者による独立監査はまだ未実施。
- M8/M9/M10(reverse-clause-drop・synthetic diameter fixture)は 2026-07-29 に
  実走・4/4 とも紙上 PROVEN 予言と一致(上記・`search/sat/runs/RUNS_LEDGER.md`)。
  未着手として残るのは、M8/M9 の `check_model_n21.mjs` E 変数側の fabricated-edge
  直接照合(現状は生成群の非推移性という間接 signature のみ確認)と、
  独立 LRAT checker の CI workflow への自動配線(現状は手動実行)。
