# interp 追補 (o) v9 — test/production registry の物理分離・version ID 必須+形式検証(Sol 便89 差戻し3)

状態: interpretation / candidate(v2〜v8 は履歴として非上書き)。本追補は Sol 便89
(`sol/裁定_246_便89検収と定理CENT.md` 差戻し3「(o) v8 = FAIL(再)」)が指摘した v8 registry
の 3 blocker を実装担当タスクとして修理する。**便89 の Sol 原文
(`sol/sol_reply_89_math16.md`)は本ワークツリーに存在しなかった**(委嘱書はテキストが確認
できず、裁定 246 の要約と司令塔タスク文面を一次資料として実装 — 逸脱として最終報告に明記)。

## 便89 が指摘した 3 blocker(裁定246 差戻し3 の原文)

> 「production registry を test が上書きできる・version ID が任意・省略でも PASS。EP v7 は
> NO-GO 継続。」

## 修理内容

### ① production registry を test が上書きできる → 物理分離

`search/ninfty-native-registry.py`:

- `PRODUCTION_REGISTRY_DIR`(旧 `REGISTRY_DIR`、後方互換のためエイリアスとして残置)= 従来通り
  `search/certs/ep_registry/`。
- `write_entry(...)` の `registry_dir` を **キーワード専用・デフォルト無し**の必須引数に変更
  — 呼び出し側は必ずどの物理ストアかを明示しなければならない(黙って production に書けない)。
- 解決後の `registry_dir` が `PRODUCTION_REGISTRY_DIR` と一致する場合、環境変数
  `NINFTY_EP_ALLOW_PRODUCTION_WRITE=1` が設定されていない限り `PermissionError` で拒否(将来の
  operator 用 CLI が明示的に立てる想定・テスト実行では絶対に設定しない)。
- `resolve()`/`index_exists()`/`_load_index()`/`index_path()` は `registry_dir` 引数を受け付け、
  省略時は環境変数 `NINFTY_EP_REGISTRY_DIR` → 無ければ `PRODUCTION_REGISTRY_DIR` の順で解決
  (`_resolve_dir`)。`search/ninfty-evidence-union.py` 側の `_registry().resolve(artifact_id)`
  呼び出し自体は無変更(dir 引数を渡さない)— そのため実運用(env 変数未設定)では常に
  production を読み、テストプロセスが `NINFTY_EP_REGISTRY_DIR` を隔離テンポラリに設定した場合
  だけそちらを読む。
- `search/test_ninfty_evidence_union.py`: `TEST_REGISTRY_DIR = tempfile.mkdtemp(...)` を実行冒頭
  で生成し `os.environ["NINFTY_EP_REGISTRY_DIR"]` にセット。全 4 箇所の `reg.write_entry(...)`
  呼び出しに `registry_dir=TEST_REGISTRY_DIR` を明示追加。`reg.INDEX_PATH` 直接参照(13e の
  registry-absent テスト)は `reg.index_path(TEST_REGISTRY_DIR)` に置換。

### ② version ID が任意 → 形式検証つき必須化

`write_entry` の `version_id` を `VERSION_ID_RE = ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` で検証
(非文字列・空文字・65 文字超・パターン外文字は `ValueError`)。従来は型チェックすら無く任意の
値(`None` 含む)を受理していた。

### ③ version を省略しても PASS する → 必須フィールド化・省略は INTEGRITY_STOP

`search/ninfty-evidence-union.py` の `_resolve_native_registry`:

- well-shaped ref の判定に `version_id`(非空文字列)を追加(従来は `artifact_id`/
  `whole_artifact_digest` の 2 項目のみ必須で `version_id` は完全省略可能だった)。省略時は
  `MISSING`(artifact_id 省略と同じバケツ)。
- `claimed_version is not None` という無条件バイパス分岐を削除し、常に厳密一致比較(`STALE`)。

`MISSING` は既存の gating ロジックにより overall が PASS になろうとしていた場合
`INTEGRITY_STOP` へ強制降格(便89 の要求「省略は INTEGRITY_STOP」を満たす)。

## 新負例 3 種(search/test_ninfty_evidence_union.py §14)

| 負例 | 実装 | 期待 | 実測 |
|---|---|---|---|
| 14a: test→production 書き込み試行 | `write_entry(..., registry_dir=PRODUCTION_REGISTRY_DIR)`(`NINFTY_EP_ALLOW_PRODUCTION_WRITE` 未設定を assert で確認) | `PermissionError` かつ production ディレクトリのファイル一覧が書き込み試行前後でバイト同一 | PASS(PermissionError 送出・ファイル一覧不変・`resolve` も None) |
| 14b: version 省略 | raw の `native_registry_refs` から `version_id` を欠落させた claim | `native_registry_status=MISSING`・overall≠PASS | PASS |
| 14c: 不正 version 形式 | `None`/空文字/空白のみ/スペース混じり/パストラバーサル風/65 文字/非文字列(int)の 7 パターンを `write_entry` に通す | 全て `ValueError`・store に痕跡なし | PASS(7/7 ValueError・漏洩なしも確認) |

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 185/185 checks passed. (exit 0; v8 時点 173/173 + 12 新規)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰ゼロ)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

production ディレクトリ(`search/certs/ep_registry/`)は本テスト実行前後で `git status`/`git diff
--stat` 共に無変更(ファイル数 4 のまま)— 分離設計が実際に機能していることの直接証拠。

## source digest(機械出力)

```text
ninfty-native-registry.py       sha256 = c679c3096b2c20a35e2b51bb5ef96546a860bc5a83f34daf6892b50255088598
ninfty-evidence-union.py        sha256 = 4ce3b8143e9b3ad748c0d57af24b18cc11722498daf21df7143e6316660a75db
test_ninfty_evidence_union.py   sha256 = 842f67980a1368a74e846e09d23720f8b90a880a5cc540e46764e25afc45f0ee
```

## v8 → v9 差分まとめ

| 項目 | v8 | v9 |
|---|---|---|
| write_entry の registry_dir | 無し(常に REGISTRY_DIR = production) | キーワード専用・必須・production への書き込みは env var opt-in が無ければ PermissionError |
| version_id (write_entry) | 無検証(任意値・型チェックすら無し) | `VERSION_ID_RE` で形式検証、非空文字列必須 |
| version_id (raw の native_registry_refs claim) | 省略可能(省略時は比較自体をスキップ) | 必須(省略は MISSING → gating で INTEGRITY_STOP) |
| test store と production store | 物理的に同一ディレクトリ | 物理的に分離(テストは tempdir・env var 経由で resolve も追随) |
| evidence-union suite | 173/173 | 185/185(+12: 便89 負例 3 種) |

## 状態

Sol 便89(裁定246 差戻し3)の是正として実装。変更ファイル(`search/ninfty-native-registry.py`・
`search/ninfty-evidence-union.py`・`search/test_ninfty_evidence_union.py`)。4 スイート合計
513/513(185+184+93+51)全 green。production registry ディレクトリは本作業で一切変更されていない
(git diff で確認)。コミットは未実施(実装担当タスクの指示により司令塔の検分待ち)。

**懸案**: `sol/sol_reply_89_math16.md` が本ワークツリーに存在せず、Sol 原文でなく裁定246の要約
から修理内容を起こした。§5(o の FAIL 理由)の原文確認は司令塔検分時に別途必要。
