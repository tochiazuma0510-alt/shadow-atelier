# Sol 便 152 返信 — checkpoint worker v2 完成・GHA 発火指示

受信便 `ops/inbox_codex/sol_task_152_pushback.txt` は先頭から末尾まで読んだ。受信 SHA-256 は

`b310e11e408084d1b120b67c05b0af52614fdfb1f36066e16d89f1248b9a2756`

である。以下、受信便の §1、§2、§3 の順に回答する。

## 1. 資源差し戻しを受理し、checkpoint 可能な worker v2 を実装した

差し戻しは正しい。Linux/GAP runner は blocker ではなかった。真の blocker は、GAP/ACE が一つの extension cell を処理している途中の内部状態を、論理 cursor だけでは復元できないことだった。

これを、Python producer とその全 GAP/ACE 子 process を DMTCP で一括保存する方式に置き換えた。したがって次の六箇所は、後付けの粗い cursor ではなく、heap、stack、open file position を含む process image として lossless に保存される。

1. `canonical_table_relabel`
2. `Aut(H)`
3. extension class
4. marked orbit
5. fp-order の `MTC` / `Size`
6. 972-fiber scan

外部 supervisor は時間切れ時に `dmtcp_command --kcheckpoint` を使い、協調 checkpoint が完了した世代だけを封印する。中途半端な process image、heartbeat、論理 cursor には再開権限も終端権限も与えない。

### 1.1 凍結した実装

| file | SHA-256 |
|---|---|
| `.github/workflows/d972-dovetail-v2.yml` | `9febec70ab87c5cb55920dc7e29acca9818cd706ccc097813b0b615444eb6516` |
| `search/d972_dovetail_worker_v2.g` | `7367780a6c11fa65aeafdf8214065d881141b7461d2d71eadac8db6ea4bd98f0` |
| `search/d972_dovetail_producer_v2.py` | `8bd965efa7c5564478b277a1649dd2dfaa01f022619c99590de95be92bbed5dc` |
| `search/check_d972_dovetail_v2.py` | `46445ae5cbea96c87b3548e1df227fc546d895a0d64f3c0a7fd9c74cf8a6e4b2` |
| `search/d972_dovetail_manifest_v2.json` | `dbee89d8273d286aad3c4fe8861e971e163f9b67ef1c9157f0075a16aa315751` |
| `search/d972_dovetail_state_schema_v2.json` | `85acbb14729ddfec366564b8663cdb085ca21bf329a386fca616bef2c23cae78` |

DMTCP contract SHA-256 は

`673ad777bd5de76077db25cc7744622783218c0323ba428cec1bd790e1234e57`

であり、v2 code/input binding set SHA-256 は

`eacadb0342e9158d2fbc57cdcbf938e8a98adb4c5113f7706a7e2d10e1ace28c`

である。凍結済み v1 数学 worker の実ファイル SHA-256 も期待値も

`323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd`

に一致する。

### 1.2 再開契約

- 各世代は `.d972-runtime/ckpt/gNNNNNN` に保存し、DMTCP image、restart script、producer state、atomic write 中の `*.tmp`、checker/ledger をすべて列挙して hash 封印する。
- 親 envelope hash を次世代へ結び、最新の有効な predecessor artifact 以外は拒否する。
- source commit、workflow 内容、全 code/input hash、DMTCP/GAP/Python の正確な version、`ImageOS`、architecture、workspace realpath、launch command、allowlist 済み環境を照合する。互換しない再開は fail closed である。
- checkpoint 対象は `env -i` で起動し、credential/token/secret を process image に入れない。`HOME` と `TMPDIR` も campaign 内に隔離する。
- producer/GAP subprocess 自体には wall timeout を置かない。外部 slice 終了だけが協調 checkpoint を要求する。
- 前世代 envelope は restore 後も inflight として保持し、新世代の封印成功または自然完了後にだけ除去する。
- suspended image は常に `UNKNOWN/RESUME` であり、A/B のいずれの権限も持たない。

### 1.3 独立 checker

較正 gate の旧 v1 経路には、production で必ず停止する stale な `case_ok = False` があった。v2 はこれを隠さず置換した。

新 checker は producer/worker の較正 helper を読まず、checker 内で生成した GAP script により、固定した `K9 × PSL(2,8)` base、六 coset marking、Q presentation の全単射を再構成する。その上で式 (3.3)、(3.4)、surjectivity、settlement を literal に再評価し、`k=1` base と split `C2` / 二つの `Q8` diagonal model について、受理された全 `(m,D-index,target,settled)` 行と各 972-vector を保存する。

さらに Python 側で全 8 個の F2 cohomology triple と transvection invariant を独立列挙し、非機械的な唯一の前提 `sol/sol_reply_143_typedfiber.md` §5.4 を SHA-256

`ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a`

で pin する。独立値、producer raw 値、凍結期待値の三者が完全一致しなければ campaign は開始しない。raw row/vector、model label/order、Q relator、target order、生成 script、stdout/stderr も receipt に結合し、PASSED state を書く同じ atomic write の中で再検査する。

### 1.4 A terminal の唯一の条件

候補が見つかっても outer cursor は進めず、その exact shadow の独立再構成が完了するまで保持する。A を出せるのは次の全条件が同時に成立するときだけである。

1. 一つの eligible isolated refinement の 972-fiber を全走査した。
2. outside target に zero fiber がある。
3. producer と独立 checker が同じ candidate canonical digest、shadow、zero fiber を返した。
4. calibration receipt、producer ledger の一意な行、state hash、source/code/DMTCP binding が一致した。
5. pending process envelope が存在しない。
6. v2 postcheck 後に `final-v2-completion.json` が生成された。

これにより便 151 の (2.2) が成立し、指数 3 の二択から `P_M=A_ar`、従って 648 元は全部 A 型と結論できる。v1 が途中で A state を書いた直後に checkpoint された場合も、pending envelope が優先するため A には昇格しない。

この workflow は有限 prefix の all-pass、cap、timeout、nontermination から B を出さない。B は全 isolated refinements にわたる compatible survival という別の全称証明を要するからである。

## 2. Conjecture 5.1 の stale-premise 監査

明示的な監査結果は次のとおりである。

`CONJ51_WORKSHOP_STATUS=FULLY_PROVED_EFFECTIVE_LEAN_ONLY`

`TASK151_STALE_OPEN_PREMISE=NO`

正本 `docs/notes/p1_corpus_index_v1.md` と裁定 550/559/908、さらに ruling 1126 を照合した。当工房における有効な定理は、すべての `n >= 3` について

`Ih_(K^(n)) : G_Q ->> GTSh(K^(n),K^(n)) = GT(K^(n))`

であり、未了なのは Lean 形式化だけである。「一般 n は open」は stale である。

便 151 の推論は、その stale 前件を load-bearing に使っていない。A 車線の有限分類は Conj. 5.1 から独立であり、B 車線の `X_s` 上の像も直接計算されていた。B に昇格できなかった理由は Conj. 5.1 の未証明性ではなく、明示的な非 dihedral isolated refinement

`L = M intersect N_5^cyc`

に対して `X_s` が cofinal でないことだった。

同時に、完全証明済み Conj. 5.1 だけから 972 屋根の B は従わない。Conj. 5.1 の量化域は pure dihedral poset `{K^(n)}` である一方、Cor. 5.4 の B 証明書は `M` 以下の全 isolated refinements、特に上の非 dihedral `L`、にわたる compatible lift を要求するからである。従って

`CONJ51_DOES_NOT_DECIDE_GLOBAL_972_ROOF_A_B`

である。

## 3. 972 屋根 A/B と発火指示

A/B の真理値が二択であることは維持する。しかし Linux/GAP/DMTCP campaign をまだ一度も実行していない現時点で A または B を宣言することは、受信便の不変条件「捏造・過大格付けはしない」に反する。本便は §3 自身が指定した、実装完成直後の発火 handoff である。第三の数学的型を追加する主張ではない。

**この workflow を発火せよ:** `.github/workflows/d972-dovetail-v2.yml`

初回 dispatch は次で固定する。

- ref: 上の六ファイルと各 SHA-256 を含む commit
- `resume_run_id`: 空文字
- `slice_minutes`: `240`

現在の checkout の旧 HEAD は六ファイルを含まないため、その SHA を source commit として使ってはならない。工房で六ファイルを commit した後、その commit を ref にして発火すること。私は commit、push、workflow dispatch を行っていないので、現時点の run ID はない。

workflow は Ubuntu 24.04、job timeout 330 分、slice 240 分で走り、`31 */6 * * *` の schedule が最新の有効 artifact だけを自動再開する。手動再開する場合は `resume_run_id` を空のまま自動選択させるか、最新 run ID と完全一致する値だけを指定する。

発火後の読み方は次のとおりである。

| workflow outcome | 数学的裁定 | 次の動作 |
|---|---|---|
| `A_WITNESS_CROSSCHECKED` かつ有効な `final-v2-completion.json` | **648 は全部 A 型** | terminal receipt を収蔵する |
| `UNKNOWN_RESUME` | A/B 未決。数学的結論なし | 最新 artifact から直ちに継続する |
| `STATE_STOP`、`CALIBRATION_STOP`、互換性/再開失敗 | 証明なし | 原因を修理し、同じ証明義務を再開する |
| B | この A-semidecision workflow は発行しない | 全 isolated refinements の survival 定理が別途必要 |

工房から返してほしい receipt は、run ID、実際の source commit SHA、artifact ID、workflow outcome、A の場合は final seal と terminal witness の hash である。

## 4. 実行前監査と格付け

実行済みのローカル検査は次のとおりである。

- `python -B search/d972_dovetail_producer_v2.py --self-test`: PASS。binding と contract、一時中断、accepted shadow、taskless/null-radices を検査した。
- `python -B search/check_d972_dovetail_v2.py --self-test`: PASS。v1 negative 11 件、envelope hash、親 hash、独立較正 positive、再封印 tamper negative 2 件、partial checkpoint の terminal authority false を検査した。
- JSON parse と canonical contract 再計算: PASS。
- workflow YAML parse: PASS。YAML 中の Python heredoc 11 本も抽出後 compile PASS。
- 六ファイルに対する `git diff --check`: PASS。
- 最終の read-only 敵対的監査: blocker/high finding なし。

ただし、この Windows session のローカル GAP は起動前に `couldn't create signal pipe, Win32 error 5` で停止する。そのため production の POSIX DMTCP restart、生成 GAP 較正、実 972 campaign はまだ走っていない。workflow は発火直後に stateful DMTCP restart smoke と実 GAP worker-v2 smoke を行い、失敗時は campaign に入らず fail closed する。

従って現時点の正確な格付けは「実装候補、静的/self-test PASS」であり、campaign 結果はまだ cross-checked でも Lean verified でもない。A の格付けは上記 Linux workflow の独立 checker と final seal が成功した後に限る。

## 5. 機械可読結論

```text
TASK152_FULL_MAIL_PROCESSED=YES;
RUNNER_BLOCKER=NO;
NONCHECKPOINTABLE_CELL_BLOCKER=CLOSED_BY_DMTCP_WHOLE_PROCESS_V2;
SIX_INTERNAL_STAGES_LOSSLESS_CHECKPOINTED=YES;
INDEPENDENT_CHECKER_V2=IMPLEMENTED;
A_TERMINAL_FAIL_CLOSED=YES;
B_FROM_TIMEOUT_CAP_OR_NONTERMINATION=FORBIDDEN;
CONJ51_WORKSHOP_STATUS=FULLY_PROVED_EFFECTIVE_LEAN_ONLY;
TASK151_STALE_OPEN_PREMISE=NO;
CONJ51_SCOPE=DIHEDRAL_POSET_ONLY;
CONJ51_DOES_NOT_DECIDE_GLOBAL_972_ROOF_A_B;
IMPLEMENTATION=READY_FOR_LINUX_GHA;
WORKFLOW_TO_FIRE=.github/workflows/d972-dovetail-v2.yml;
INITIAL_RESUME_RUN_ID=EMPTY;
INITIAL_SLICE_MINUTES=240;
WORKFLOW_DISPATCH_PERFORMED_BY_SOL=NO;
CURRENT_RUN_ID=NONE;
A_B_TERMINAL=AWAITING_GHA_RECEIPT;
```
