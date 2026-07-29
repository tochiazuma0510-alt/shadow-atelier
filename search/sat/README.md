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

## 未着手(次段)

- encoder(F2 三条件/巡回型制約 → DIMACS CNF)。標的選定は Sol 便 84 ⑥ 待ち。
- encoder 完成後: 独立照合器(node/python、encoder 非 import)の実装。
- kissat/drat-trim バイナリのキャッシュ化(現状は毎回ソース clone + ビルド。ES7 と
  同じ流儀を踏襲しているだけで、高速化が必要になったら別途相談)。
