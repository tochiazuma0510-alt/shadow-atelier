# interp 追補 (o) v10 — (o) 残 4 項の修理・cake_lpr 一般 fail-closed 契約の修理(Sol 便90 F90-4.1/F90-4.4)

状態: interpretation / candidate(v2〜v9 は履歴として非上書き)。本追補は Sol 便90
(`sol/sol_reply_90_math17.md` F90-4.1「(o) v9 の残 4 項、EP v7 は NO-GO 継続」・
F90-4.4「cake_lpr workflow の一般 fail-closed 契約 FAIL 継続」)が指摘した項目を
実装担当タスクとして修理する。

## F90-4.1 が指摘した (o) 残 4 項(および関連する v9 未閉鎖項目)

原文(`sol/sol_reply_90_math17.md` F90-4.1)から:

1. production store は依然 `native_a`, `native_b`, `native_b_alt`, version `v1` の
   synthetic fixture であり、EP v7 の実 artifact / freeze receipt ではない。
2. resolver と provisioning は同じ runtime module に同居する。
3. opt-in 後の同一 ID 上書きは既定拒否されない。
4. entry と index の更新は atomic / locked でない。
5. production snapshot digest を固定した receipt がない。
6. malformed JSON / I/O 例外は `resolve()` 内で構造化 MISSING/MALFORMED に落ちず、
   `json.load` から外へ出る。
7. role/schema/status/whole digest と実 freeze ID を束ねた production provisioning
   がない。
8. suite は production tree の全 byte digest を実行前後で assert せず、負例 14a の
   前後 file-name list だけを比較する。
9. suite 完了後の実 production positive 再評価がない。

## 修理内容

### ① 実体化(item 1・9)— 機構は完成、実データの登録は未実施

**実体化には司令塔の指定が必要**(正直な報告 — task の許容どおり):この
ワークツリー内を検索した限り、「EP v7 の実 artifact」として確定的に指せる
native_a/native_b のペアは見つからなかった。候補として最も近いのは
`search/certs/full_witness_fixture_01.json` — 自己記述(`_description`)によれば
「lane A's own real `generateCertificate()` on the genuine Pell fixture
`checker_pos_01.json`」から取った base fields を持つ、`ep_registry/` の玩具的
placeholder(`pt-x1`/`pt-x2` の 2 点)よりはるかに実データに近い内容。ただし
ファイル名自体が "fixture" であり、`provenance/ninfty_freeze_receipt_sol75.md`
(F8.5)自身が「EP まで partial predicate / UNKNOWN。calibrated detector・complete
search 宣言は EP 前 NOT AUTHORIZED」と明記している — このプロジェクトの
freeze 系列としては、EP 配線そのものがまだ authorize されていない。

したがって本タスクでは production store の中身を推測で差し替えることはせず、
**機構(登録スクリプト・受領書生成)だけを完成させた**。司令塔が実 artifact を
指定した時点で `search/ninfty-native-registry-provisioning.py` の CLI
(`--production --freeze-id ...`)で即座に登録できる。

### ② resolver / provisioning の分離(item 2)

`search/ninfty-native-registry.py` を **resolver 専用**に縮小(`resolve`・
`index_exists`・`index_path`・新規 `production_snapshot_digest` のみ)。
`write_entry` と、それが単独で必要とする一切(production 書き込みガード・
artifact_id→filename 導出・ロック/atomic write 機構・上書き/supersede 方針)を
新規 `search/ninfty-native-registry-provisioning.py` へ完全に移動。
`search/ninfty-evidence-union.py` の `_registry()` は resolver モジュールしか
ロードしない(grep 可能: provisioning モジュール名は同ファイルに一切出現しない)。
構造テスト(§15i)が両方向(no-load・`hasattr(reg, 'write_entry') is False`)を
確認する。

### ③ 同一 ID 上書きの既定拒否(item 3)

`write_entry` は既存 entry と role または content(whole_artifact_digest)が
異なる同一 artifact_id への上書きを既定で `ValueError` 拒否する。`supersede=True`
を明示した場合のみ許可し、旧 entry ファイルを `<registry_dir>/_superseded/` へ
バイト同一のまま archive してから新 content を書き込み、index の
`artifacts[artifact_id]["superseded"]` 履歴(古い順)に旧 version_id/freeze_id/
digest/`superseded_at` を追記する(削除ではなく供養)。同一 role・同一 digest の
再書き込みは「内容変更ではない」として supersede 不要で idempotent に許可、
履歴も追加しない(過去の履歴は保持したまま — idempotent 再書き込みで履歴が
消える回帰は §15 のテストで検出・修理済み)。

### ④ atomic / locked 更新(item 4)

`write_entry` の read-check-write 全体を `registry_dir` スコープの排他ロック
(`index.json.lock`、`O_CREAT|O_EXCL` ベース、タイムアウトつきリトライ、
Windows/POSIX 双方で動作)で囲む。実際のファイル書き込み(entry ファイル・
archive コピー・index.json)はすべて `<path>.tmp-<pid>-<token>` へ書いてから
`os.replace`(POSIX/Windows とも同一ボリューム内で atomic)で差し替える —
中断が起きても中途半端な entry/index ファイルは残らず、`.tmp-*` の残骸のみ
(digest 計算から除外済み)。

### 関連して閉じた v9 未閉鎖項目

- **item 5/7**(freeze ID・production snapshot digest の receipt): entry
  schema に `freeze_id` を追加、production への書き込みは `freeze_id`
  必須(形式検証つき、省略/不正形式は `ValueError`)。新規
  `production_snapshot_digest(registry_dir=None)`(resolver 側、registry
  ディレクトリ全体のファイル集合を sha256 で束ねた単一 digest)と
  `write_production_receipt(...)`(provisioning 側、entry の
  role/version_id/freeze_id/digest と production_snapshot_digest を
  一つの receipt にまとめて atomic 書き込み)を実装。
- **item 6**(malformed JSON): `resolve()`/`_load_index()` は
  `(OSError, ValueError)` を捕捉して `None` を返す(fail-closed)。
  従来は `json.load` の例外がそのまま呼び出し元へ漏れていた。
- **item 8**(suite の production digest assert): 新負例 §15g が
  `production_snapshot_digest(PRODUCTION_REGISTRY_DIR)` を suite 実行の
  最初と最後で比較する(旧 14a のファイル名リスト比較より厳密 — 同名
  ファイルの中身だけが書き換わるケースも検出できる)。

item 9(実 production positive 再評価)は、実 artifact が未登録のため
今回は実施できていない — 司令塔の実体化判断後の宿題として残す。

## 新負例(search/test_ninfty_evidence_union.py §15、13 種)

| 負例 | 確認内容 |
|---|---|
| 15a | 既存と異なる内容での同一 artifact_id 上書きが supersede なしで `ValueError`・既存 entry は無変更 |
| 15b | `supersede=True` は成功し新内容を返す・旧内容は index 履歴 + archive ファイルに保存 |
| 15c | 同一内容の再書き込みは idempotent(`superseded=False`)・既存履歴は保持 |
| 15d | 保持中のロックが 2 本目の取得をタイムアウトで拒否・解放後は即座に成功 |
| 15e | 正常書き込み後に `.tmp-*` の残骸が残らない |
| 15f | 壊れた entry JSON / 壊れた index.json のいずれも `resolve()` が例外なく `None` を返す |
| 15g | production ディレクトリの `production_snapshot_digest` が suite 実行の最初と最後で一致 |
| 15h | production 書き込みは opt-in ありでも `freeze_id` 省略で `ValueError`・ファイル一覧無変更 |
| 15i | `ninfty-evidence-union.py` 含め他ファイルが provisioning モジュールを一切ロードしない・resolver モジュールに `write_entry` 属性が存在しない |

## F90-4.4 — cake_lpr の一般 fail-closed 契約(`.github/workflows/lrat-recheck.yml`)

原文の未閉鎖 5 項目のうち、コードで閉じられる 4 項目を修理(3 項目目「manifest
欠落 / file 未掲載を NOTE で継続する」は Sol の裁定どおり NOTE のまま維持 — 修理
対象ではなく現状維持の指示)。

1. **accepted token を厳密一致へ**: `"VERIFIED UNSAT" in stdout` の部分文字列
   一致(`"s NOT VERIFIED UNSAT"` のような拒否メッセージにもマッチしうる)を、
   出力行の EXACT 一致 `"s VERIFIED UNSAT"` に変更(build sanity・本採録・負例の
   3 箇所すべて)。
2. **最上位 verdict の語彙**: `verdict=VERIFIED`/`NOT_VERIFIED` を
   `verdict=CROSS_CHECKED_PASS`/`CROSS_CHECKED_FAIL` に改名 —「検証(verified)」は
   Lean 専用という CLAUDE.md 規律との衝突を、この workflow が採択判定に使う語彙
   からは除去した(cake_lpr 自身が出す生の stdout 文字列 `"s VERIFIED UNSAT"` は
   ツール自身の語彙なので変更していない)。
4. **負例の rejection token と exit semantics を固定**: 旧稿は「accepted token が
   無いだけ」で `CORRECTLY_REJECTED` としていた(タイムアウト・クラッシュ等で
   たまたま何も出なかった場合まで無差別に「正しく拒否」と読み違える余地があった)。
   修理後は「EXACT accepted line が無い」**かつ**「終了コードが非ゼロ」の両方を
   要求し、終了コードが 0 なのに accepted line が無い場合は `AMBIGUOUS_REJECTION`
   として workflow を fail させる。
5. **負例artifact の独立検収・TCB 限定文**: `negative_test_result.txt` に
   `corrupted_lrat_sha256`/`negative_problem_cnf_sha256`(独立監査用の receipt)と
   `tcb_note`(この負例が示すのは「この一種類の破壊パターンに対する拒否」であって
   一般的健全性の証明ではなく、破壊生成スクリプトと cake_lpr バイナリ自体はこの
   負例テスト自身の TCB の一部である、という限定文)を追加。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 204/204 checks passed. (exit 0; v9 時点 185/185 + 19 新規)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰ゼロ)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

`.github/workflows/lrat-recheck.yml` は GitHub Actions ランナー(cake_lpr の
clone/build を要する)でしか実走できない — 本タスクでは YAML 構文
(`yaml.safe_load`)・埋め込み Python 3 ブロック全 3 本の `py_compile`・埋め込み
bash 5 ステップ全ての `bash -n` を通し、静的には壊れていないことを確認した。実
CI 走行での再検証は次の push/`workflow_dispatch` へ持ち越し。

## 状態・逸脱

Sol 便90(F90-4.1/F90-4.4)の是正として実装。変更ファイル:
`search/ninfty-native-registry.py`(resolver 専用へ縮小)・新規
`search/ninfty-native-registry-provisioning.py`・
`search/ninfty-evidence-union.py`(コメントのみ、機能無変更)・
`search/test_ninfty_evidence_union.py`(§15 追加・既存 write_entry 呼び出し
7 箇所を `prov.write_entry` へ移行・13f に `supersede=True` 追加)・
`.github/workflows/lrat-recheck.yml`。4 スイート合計 532/532
(204+184+93+51)全 green。R1/R2 検証器(`ninfty-verifier-b.py`・
`ninfty-verifier-w6-r2.py`)はバイト単一維持(無変更・grep で確認)。push は
していない。

**逸脱・懸案**:
- item 1(実体化)は機構のみ完成・実データ登録は未実施(司令塔の指定待ち)。
- item 9(実 production positive 再評価)は item 1 未完のため未着手。
- cake_lpr workflow の修理は静的検証止まり(実 CI 走行は未実施 — GitHub
  Actions 環境が必要なため、このワークツリー内では検証できない)。
