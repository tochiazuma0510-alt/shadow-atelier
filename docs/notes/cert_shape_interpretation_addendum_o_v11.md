# interp 追補 (o) v11 — EP registry の generation-commit 再設計・cake_lpr fail-closed 3点(Sol 便91 F91-6.2/F91-6.3/P91-4)

状態: interpretation / candidate(v2〜v10 は履歴として非上書き)。本追補は Sol 便91
(`sol/sol_reply_91_math18.md` F91-6.2「registry の再発効を阻む blocker(11 件)」・
P91-4「EP の generation commit」・F91-6.3「cake_lpr_lpr 一般 fail-closed 契約」)が
指摘した項目を実装担当タスクとして修理する。

## 設計 — mutable entry/index から generation-commit へ(P91-4 採択方式)

旧設計(v8〜v10)は `search/certs/ep_registry/index.json` 1 個 + 個別 entry ファイル
群を都度 in-place 更新していた(write_entry: entry を書き換え → index を書き換え、
の 2 段)。この方式が F91-6.2 の 11 blocker の根であるという Sol 判定に従い、mutable
な 2 ファイル更新を全廃し、以下の generation-commit 方式へ置き換えた。

```
<registry_dir>/
  CURRENT.json                # 可変ファイルはこれ1つだけ。os.replace で atomic 差替。
                               # {"schema_id", "generation_id", "updated_at"}
  generations/
    <generation_id>/          # 一度書いたら二度と触らない(immutable)
      index.json              # {"schema_id", "generation_id", "freeze_id",
                               #  "artifacts": {<artifact_id>: {file, role,
                               #   version_id, freeze_id, status,
                               #   whole_artifact_digest}}}
      <entry files>.json      # artifact 1個につき1ファイル
      receipt.json            # bundle receipt — 全 artifact + freeze_id +
                               # generation_digest を1ファイルに束縛。
                               # generation_digest の計算対象(index.json +
                               # 全entryファイル)から意図的に除外(自己参照の解消)。
```

`commit_generation(artifacts, freeze_id, *, registry_dir, generation_id=None,
publish=True)`(`search/ninfty-native-registry-provisioning.py`)は:
1. production 判定(realpath/samefile、alias bypass 耐性)・freeze_id 形式・
   各 artifact の role/version_id/status を検証。
2. 新規ディレクトリ `generations/<generation_id>/` を作成(既存なら
   `FileExistsError` — 上書き経路は存在しない)。
3. index.json + 各 entry ファイルを atomic 書き込み。
4. `generation_digest()`(index.json + entry ファイル群のみを対象、receipt.json は
   対象外)を計算し、receipt.json に記録して atomic 書き込み。
5. **公開前に自己検査**: resolver 本体の `_load_and_verify_generation` を
   (CURRENT 経由ではなく)いま書いた generation_id へ直接向けて再実行し、
   一致しなければ `RuntimeError`(CURRENT には一切触れない)。
6. 自己検査 PASS の場合のみ、CURRENT.json を1個の atomic replace で差し替え。

`resolve(artifact_id, registry_dir=None)`(`search/ninfty-native-registry.py`)は
CURRENT.json が指す generation **1 個だけ**を読み、以下のいずれか1つでも欠ければ
`None`(fail-closed):
- CURRENT.json 自体の schema/形式。
- generation_id の path confinement(`generations/<id>` が親ディレクトリの外へ
  出ていないか realpath で確認)。
- index.json の schema_id・freeze_id・各 artifact の role/version_id/status/
  digest の型と形式。
- 各 artifact の `file` フィールドの path confinement(basename のみ・`..`
  拒否・realpath containment)。
- entry ファイル自身の schema_id・全フィールドが index のキャッシュ値と
  **完全一致**しているか。
- entry ファイル群から新鮮に再計算した `whole_artifact_digest` が index の
  キャッシュ値と一致しているか。
- 同一 generation 内の**全 artifact が同じ freeze_id を共有**しているか。
- receipt.json の schema_id・generation_id・freeze_id・artifacts リスト
  (id+digest)・`generation_digest` が、いま独立に再計算した値と一致しているか。

production 判定は `os.path.samefile`(両パスが存在する場合)/ `os.path.realpath`
(フォールバック)ベースに変更 — symlink/junction alias bypass を封鎖。

## F91-6.2 blocker 11 件の消込表

| # | blocker(便91 原文の要約) | 消込方法 |
|---|---|---|
| 1 | 壊れた既存 entry を absent 扱い(fail-open) | write path が「既存を読んで判断」を一切行わない設計に変更。commit は常に新規ディレクトリのみへ書く。既存 generation_id への衝突は `FileExistsError`(§15a) |
| 2 | entry を index より先に更新(2 ファイル非 atomic) | 1 個の新規ディレクトリへ index/entry/receipt を作ってから CURRENT を1個だけ差し替え。旧 generation の bytes は一切触れない(§15b) |
| 3 | metadata drift(digest 同一なら黙認) | in-place 更新経路自体が存在しない — 内容・メタデータの変更は常に新しい generation_id を持つ別の generation(§15c) |
| 4 | entry/index 対の非 transaction 性 | 生成は1ディレクトリへの一括書き込み+自己検査後の1ファイル差替のみが可変操作。resolver は index と entry の全メタデータを突合(§15d) |
| 5 | resolver の schema 不検査 | `_load_and_verify_generation` が schema_id・role/status/version 形式・freeze_id・digest を全数検査(§15d/15e) |
| 6 | path confinement 欠如 | `_safe_join`(basename限定+realpath containment)を generation_id・entry file 名の両方に適用(§15f) |
| 7 | production 判定の alias bypass | `_is_production_dir` を samefile/realpath ベースに変更(§15g、junction 経由で検証) |
| 8 | receipt の自己参照 | `generation_digest()` の対象ファイル集合を index.json + entry ファイルのみに固定し、receipt.json を構造的に除外(§15h) |
| 9 | receipt が単一 artifact・registry lock 外 | bundle receipt が同一 generation の全 artifact + 共有 freeze_id + generation_digest を1ファイルに束縛。改竄検知は generation 全体を無効化(§15i) |
| 10 | consumer の freeze gate 欠如 | `ninfty-evidence-union.py` の `native_registry_refs` に freeze_id を必須化・STALE 判定に追加・両 lane 個別 PASS 後の freeze 一致をクロスチェック(§15j) |
| 11 | production store が旧 flat 形式のまま resolvable | resolver が CURRENT.json + generations/ 形式しか読まない新設計により、旧 flat index.json は構造的に無視される(§15k) |

## 新負例一覧(`search/test_ninfty_evidence_union.py` §15、更新)

| 負例 | 対応 blocker | 確認内容 |
|---|---|---|
| 15a | 1 | 壊れた過去 generation は新規 commit を妨げない・generation_id 衝突は FileExistsError |
| 15b | 2 | 別 generation の commit が既存 generation の全バイトを変更しない |
| 15c | 3 | 同一内容・異なる version_id は常に別 generation_id(drift ではない) |
| 15d | 4/5 | index と entry のメタデータ不一致(status)で generation 全体が resolve() = None |
| 15e | 5 | index/entry の wrong schema_id・不正 role・不正 version 形式・malformed JSON(entry/index 両方)で None |
| 15f | 6 | index の file フィールドを `../…`・絶対パスへ改竄 → None、範囲外 sentinel の中身が漏れない |
| 15g | 7 | production directory への junction 経由アクセスも opt-in なしで PermissionError(Windows junction が使えない場合は正直に SKIPPED) |
| 15h | 8 | receipt.json の issued_at 改竄は resolve() を壊さない(digest 対象外の証明)・generation_digest 自体の改竄は壊す |
| 15i | 9 | 1つの receipt に全 artifact + freeze_id + generation_digest が同居・1 artifact の digest 改竄で generation 全体が無効化 |
| 15j | 10 | native_registry_refs で freeze_id 省略 → MISSING・誤った freeze_id → STALE・stub registry によるクロスサイド FREEZE_MISMATCH の直接単体テスト |
| 15k | 11 | production store の旧 flat 形式 3 entry(native_a/native_b/native_b_alt)が新 resolver では一切 resolve しない |
| 15l | 2/4 | CURRENT.json publish 用ロックのタイムアウト・解放後の即時取得(旧 15d を publish 用ロックへ移行) |
| 15m | 2/4 | commit_generation 後に `.tmp-*` 残骸が残らない(旧 15e を移行) |
| 15n | 5/8(便90由来、継続) | production_snapshot_digest がスイート実行前後で不変(schema-agnostic、便91でも維持) |
| 15o | 7(便90由来、継続) | production commit は freeze_id 省略で ValueError/TypeError・production 領域無変更 |
| 15p | 2(便90由来、継続) | provisioning モジュールを他ファイルがロードしない・resolver に commit_generation/write_entry 属性がない |

## F91-6.3 — cake_lpr 一般 fail-closed 契約(3 点)

1. **manifest 欠落/未掲載を fail-closed に**: `check_manifest` は SHA256SUMS.txt が
   ない、または対象ファイルが未掲載の場合、旧稿は NOTE 文字列を返して run を
   継続していた(便90 裁定では意図的に NOTE のまま維持と指示されていたが、
   便91 でこの判断自体が覆り fail-closed が要求された)。修理後は両ケースとも
   `SystemExit`(MANIFEST_STOP)で workflow を止める。既存の全 target run
   ディレクトリ(`search/sat/runs/*/`)が SHA256SUMS.txt を持ち、problem.cnf・
   proof.lrat.gz の両方を列挙済みであることをローカルで確認済み(この変更で
   既存の実 target が壊れないことの事前確認)。
2. **負例の拒否判定を checker 定義の token 必須に**: 旧稿は「accepted line が
   ない」かつ「終了コードが非ゼロ」だけで `CORRECTLY_REJECTED` としていた —
   これはタイムアウト・クラッシュ・ローダ異常など「たまたま何も出なかった」
   場合まで無差別に「正しく拒否した」と読み違える余地を残していた。修理後は
   cake_lpr 自身の拒否行 `"s NOT VERIFIED UNSAT"`(SAT-competition 系 checker の
   標準的な拒否メッセージ、accepted line `"s VERIFIED UNSAT"` の対偶)の**存在**
   を必須化し、加えて `timeout 300` でハングを打ち切り可能にした上で:
   - `exit=124`(timeout 由来)→ `verdict=TIMEOUT`(fail)
   - `exit>=128`(シグナル終了、例: segfault)→ `verdict=CRASHED`(fail、signal 番号記録)
   - 拒否行が無い(かつ上記どちらでもない)→ `verdict=LOADER_FAILURE_OR_UNCLASSIFIED_REJECTION`(fail)
   - 拒否行があり exit=0(矛盾)→ `verdict=AMBIGUOUS_REJECTION`(fail、既存)
   - 拒否行があり exit≠0 → `verdict=CORRECTLY_REJECTED`(pass)
   のように分類を分離した。
3. **NOT_VERIFIED 語彙を CROSS_CHECKED_FAIL 系へ**: 便90 F90-4.4 item 4 が指摘した
   まま未修理だった診断文字列(`"...was NOT_VERIFIED by cake_lpr"`)を
   `"...was CROSS_CHECKED_FAIL by cake_lpr"` へ変更 — 最上位 verdict 語彙
   (`CROSS_CHECKED_PASS`/`CROSS_CHECKED_FAIL`)と診断テキストの語彙を統一し、
   「検証(verified)」語の残存を(生の cake_lpr stdout 文字列を除き)完全に除去。

`.github/workflows/lrat-recheck.yml` はこのワークツリー内では実走できない
(cake_lpr の clone/build を要する)ため、今回も静的検証: `yaml.safe_load` で
YAML 構文、埋め込み Python 3ブロック全 3 本を `py_compile`、埋め込み bash 5
ステップ全てを `bash -n` で確認(いずれも合格)。実 CI 走行は次の push/
`workflow_dispatch` へ持ち越し。

## consumer 側 freeze gate(ninfty-evidence-union.py)

`_resolve_native_registry` の well-shaped-ref ゲートに `freeze_id`(非空文字列)を
`version_id` と同格で追加した。判定順序(既存の digest/version チェックの後、
cert 側チェックの前)に freeze_id の STALE チェックを挿入。加えて、両 lane が
個別に PASS へ到達した**後**、双方の**解決済み** freeze_id(claim ではなく registry
が実際に返した値)を突き合わせ、不一致なら新設の `FREEZE_MISMATCH` へ両 lane を
格下げする(`_REGISTRY_STATUS_PRIORITY` に追加)。generation-commit 設計の下では
1回の resolve() セッションで A/B が異なる freeze から来ることは構造的に
起こり得ない(1 generation は1つの freeze_id を共有)ため、このクロスサイド
チェックは多層防御であり、stub registry double を使って直接単体テストした
(§15j 後半)。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 223/223 checks passed. (exit 0; v10 時点 204/204 + 19 新規)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰ゼロ)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
合計 551/551 全 green。
```

`.github/workflows/lrat-recheck.yml` 静的検証:
```text
python -c "import yaml; yaml.safe_load(open('.github/workflows/lrat-recheck.yml'))"  -> OK
埋め込み python heredoc 3本 (py_compile)                                              -> 全 OK
埋め込み bash run: ブロック 5本 (bash -n)                                             -> 全 OK
```

## 状態・逸脱

Sol 便91(F91-6.2/F91-6.3/P91-4)の是正として実装。変更ファイル:
`search/ninfty-native-registry.py`(全面書き換え — generation-commit resolver)・
`search/ninfty-native-registry-provisioning.py`(全面書き換え — commit_generation
provisioning、`write_entry`/`write_production_receipt` は廃止し
`write_production_receipt` は呼ばれると `NotImplementedError` を送出するスタブ
として残置)・`search/ninfty-evidence-union.py`(freeze gate 追加・
`_REGISTRY_STATUS_PRIORITY` に `FREEZE_MISMATCH` 追加・docstring の
version_id「optional」表記の誤りも修正)・
`search/test_ninfty_evidence_union.py`(§10a/10d/13/14 の registry 呼び出しを
`commit_generation` API へ全面移行・§15 を 11 blocker + freeze gate 対応の
16 サブセクションへ全面書き換え)・`.github/workflows/lrat-recheck.yml`
(F91-6.3 の 3 点)。4 suite 合計 551/551 全 green。commit していない
(司令塔検分後)。

**逸脱・懸案**:
- production store の実物指定は今回も対象外(研究者認可待ち — synthetic
  fixture のまま)。旧 flat 形式の3ファイル(`search/certs/ep_registry/
  {index.json, 092a...json, 29d1...json, 06e7...json}`)は新 resolver からは
  構造的に無視されるだけで、削除も migration も行っていない — production
  store の内容変更は今回のタスク範囲外という指示に従い、inert leftover の
  ままにしてある(blocker 11 消込はこの inert 化で十分と判断)。
- 15g(production alias bypass, junction 経由)はこの Windows 環境で
  `mklink /J` が成功する場合のみ実走する — 失敗した場合は正直に SKIPPED
  として記録し、偽陽性を作らない(このセッションでは実走を確認済み)。
- 15f の path confinement テストは basename 拒否層(`..`・絶対パス・区切り
  文字を含む file フィールド)を直接検証した。realpath containment 層
  (basename としては安全に見えるが実体がシンボリックリンクで外を指す
  ケース)は、この Windows サンドボックスでファイルシンボリックリンクを
  権限なしに作成できないため、単体では別途検証していない(コードパス自体は
  `_safe_join` 内に存在し、15g のディレクトリ junction テストが同じ
  realpath-containment ロジックを別の攻撃面から間接的に運動させている)。
- cake_lpr workflow の修理は静的検証止まり(実 CI 走行は未実施)。
- `write_production_receipt` は 便91 の bundle receipt(commit_generation が
  自動生成)により不要になったため、呼び出されると明示的に
  `NotImplementedError` を送出するスタブとして残した(サイレント削除より
  古い呼び出し元が早期に気づける形を選択)。
