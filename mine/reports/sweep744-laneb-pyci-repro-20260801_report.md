# mine 検収レポート -- sweep744-laneb-pyci-repro-20260801

- 生成: 2026-08-01T05:19:09.778484+00:00(UTC)
- plan: `mine/jobs/queue/sweep744-laneb-pyci-repro-20260801.json`
- artifact-dir: `scratchpad/mine_dl/sweep744-laneb-pyci-repro-20260801`
- claim_class: `exploration`
- checker cert 出所: (plan.crosscheck.checker_certs_glob 未指定)

machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。

## 分類不能な json (1 件 -- artifact-dir 内の無関係な cert。内容は表示しない、パスのみ)

- `scratchpad/mine_dl/sweep744-laneb-pyci-repro-20260801\mine-run-sweep744-laneb-pyci-repro-20260801\mine\out\sweep744-laneb-pyci-repro-20260801\laneb_results_744.json` (schema/generated_by が本ジョブの様式と一致しない)

## (a) 再現照合 -- artifact cert ⟷ repo 収蔵済み cert(同名ファイル)

較正再走の合否: 主要欄が全一致すれば `REPRO_MATCH`、1つでも不一致があれば `REPRO_MISMATCH`。volatile 欄(elapsed_sec 等)は参考列で判定には数えない。

(artifact 内に GAP explorer window cert が見つからなかった)


## (b) 対付け集計 -- GAP explorer cert ⟷ python checker cert

(対付け対象の窓が見つからなかった)

## 集計まとめ

- 再現照合: 0/0 REPRO_MATCH
- 対付け: agreement 0/0(全窓数 0)

(この集計は候補表記であり、裁定・LEDGER 貼付・地図 delta の確定は人が行う。)

## 付記(collector v0 未対応スキーマの直接抽出 -- machine-piped)

collect.py v0 の `classify()` は本 job の cert(schema フィールドを持たない role_note/entry_point 形式)を未対応のため上記 (a)/(b) は 0/0(tmax-scan 系ジョブと同様の既知の限界)。以下は cert JSON をその場で python で再パースした値(手入力なし)。

### CI run / result.txt(machine-piped key=value)

| 項目 | 値 |
|---|---|
| verdict | done |
| backend | py-ci |
| py_contract | generic |
| py_exit_code | 0 |
| py_done_marker | PY_DRIVER_DONE |
| run_id | 30685471824 |
| sha | e77edae400a0c073e638260bd574d0cbf4931e65 |

汎用契約(commit ad253b4・裁定340)の初実戦判定: `py_contract=generic` で `verdict=done`・`py_exit_code=0` -- args なし・既定 done_marker のみで完走判定が機能した。

### artifact ⟷ repo 収蔵済み cert の突合(laneb_results_744.json)

- artifact: `mine/out/sweep744-laneb-pyci-repro-20260801/laneb_results_744.json`(sha256 = `4901648509cc2243b1dbe410874ba844b95f47527fc4ec6eddad9dbf37e2d63c`)
- repo 収蔵済み: `search/certs/ep_sweep744/laneb_results_744.json`(sha256 = `a50774b876f1e185a6ff995c44e21e54ae599ae30d4583530a2750d8dfa0c1c8`)
- **生バイト(sha256)は不一致** -- 改行コード差(Windows チェックアウト環境と CI の LF/CRLF 差)によるものと推定(diff は全行が差分として出るが、各行の実内容は同一)。**JSON を構造的に再パースして突合した結果は完全一致**:
  - `entry_point_sha256` 一致(`082f4ec2afc95bf5cb46f2a49ce8bc7f22cb3df20aea3be6b9d66c3bf0abfc0c` -- artifact/repo とも同一。search/ninfty-checker.py の同一性が cert 自己記録から確認できた)
  - `input_candidates_sha256` 一致(candidates_744.json の同一性確認)
  - `total` 一致(744/744)
  - `results` 配列 -- **744/744 要素が Python `==` で完全一致(differing indices = 0 件)**

### stage / primary_reason_code 内訳(artifact 側・機械集計)

| stage | 件数 |
|---|---|
| REJECT | 744 |

| primary_reason_code | 件数 |
|---|---|
| precondition/leading-coeff-mismatch | 372 |
| a-partition-mismatch | 372 |

(ops/inbox_codex/sol_task_95_math22.txt に記載の「372=E-3・372=T-1」という 372/372 分割と件数が一致する形 -- ラベル対応は数学的解釈であり miner は判定しない。)

### 結論(事実記載のみ -- 的中/外れ・二環境化成立の裁定は司令塔)

- **verdict=done・exit 0・PY_DRIVER_DONE 検出**(汎用契約 py-ci の初実戦、構造的完走)。
- **artifact の 744 件結果は repo 収蔵済み laneb_results_744.json(ローカル/元環境生成)と構造的に完全一致(0 differing)** -- entry_point_sha256(checker 同一性)・input_candidates_sha256(入力同一性)・744 件の stage/reason_codes すべて一致。
- 生バイト sha256 不一致は改行コード起因と推定される旨、上申する(内容一致は上記の構造比較で確認済み・生バイト同一性の最終確認は司令塔/機械的な改行正規化比較に委ねる)。
