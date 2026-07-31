# interp 追補 (o) v12 — EP registry の A/B bundle atomic resolve(resolve_bundle 新設・W92-6 閉鎖、F92-6.2 3点対応)(Sol 便92 P92-6)

状態: interpretation / candidate(v2〜v11 は履歴として非上書き)。本追補は Sol 便92
(`sol/sol_reply_92_math19.md` §6「EP v11 generation commit」— F92-6.1 総合判定
FAIL・W92-6「同一 freeze・異世代混成 race」・P92-6「必須修理」・F92-6.2「設計判断
3 件」)が指摘した blocker を実装担当タスクとして修理する。

## W92-6 が指摘した TOCTOU の構造

Sol 便91 の generation-commit 再設計(v11 追補)は「1 generation は 1 つの
freeze_id を共有し、`resolve()` は常に CURRENT が指す generation 1 個だけを
検証つきで読む」という構造で 11 blocker を閉じたが、**consumer が A/B 2 個の
artifact を欲しいとき `reg.resolve()` を 2 回、別々に呼ぶ**という使い方自体は
残っていた。各 `resolve()` 呼び出しは独立に `CURRENT.json` を読み直す(意図的な
設計 — 常に最新を読む)ため、次の interleaving が構造的に許される:

1. `CURRENT=G0` の状態で consumer が `resolve("race_a")` を呼ぶ → G0 の
   `race_a` を得る。
2. publisher が(無関係な、正当な)新しい generation `G1` を atomic に publish
   する(`CURRENT` を G0 → G1 へ差替)。
3. consumer が `resolve("race_b")` を呼ぶ → **G1** の `race_b` を得る。
4. schema は `freeze_id` の一意性を generation 間で強制していない
   (`FREEZE_ID_RE` は形式だけを検査する)ため、G0 と G1 が同じ `freeze_id`
   文字列を持つことは普通に起こり得る — その場合、consumer 側の
   freeze-一致チェック(便91 blocker 10、`freeze_id` **文字列**の比較)は
   何の異常も検出しない。

G0 の bundle receipt は G0 の artifact だけを、G1 の bundle receipt は G1 の
artifact だけを束縛する — **「G0 の race_a + G1 の race_b」という特定の混成
ペアを束縛する receipt はどこにも存在しない**。これは W92-6 が指摘した
reader atomicity の破れであり、旧負例(v11 §15j)は「freeze が食い違う」
ケースしか試しておらず、この「freeze は一致するが generation が違う」反例を
一切捕捉していなかった。

## 修理(P92-6 指定方式)— `resolve_bundle`

`search/ninfty-native-registry.py` に `resolve_bundle(artifact_ids,
registry_dir=None)` を新設した。設計は P92-6 の指定どおり「CURRENT・index・
bundle receipt を一回だけ読み、その同じ generation から全 artifact を返す」:

```python
def resolve_bundle(artifact_ids, registry_dir=None):
    if not isinstance(artifact_ids, (list, tuple, set, frozenset)):
        return None
    gen_id = _read_current(registry_dir)        # CURRENT.json を読むのはここ1回だけ
    if gen_id is None:
        return None
    generation = _load_and_verify_generation(registry_dir, gen_id)  # 1回だけ
    if generation is None:
        return None
    artifacts = {aid: generation["artifacts"].get(aid) for aid in artifact_ids}
    return {"generation_id": gen_id, "freeze_id": generation["freeze_id"], "artifacts": artifacts}
```

`gen_id` は関数ローカル変数として1回だけ捕捉され、以降の全 artifact 解決は
その1個の `generation_id` に対してのみ行われる。**関数の実行中(あるいは
実行後)に publisher が `CURRENT.json` を差し替えても、この呼び出しが返す
どの artifact もそれには一切影響されない**(次回の呼び出しにのみ影響する)。
これは「追加チェックで検出する」方式ではなく、「2回目の CURRENT 読み出しが
そもそもコード上に存在しない」という構造的な解消であり、P92-6 が求めた方式
そのもの。返り値には P92-6 の要求どおり `generation_id` を含める。

`resolve(artifact_id, registry_dir=None)`(単一 artifact 用)は変更していない
— 単一ルックアップとしては引き続き正しい。ただし docstring に
**CAUTION**(A/B ペア等、複数 artifact を同一世代から欲しい呼び出しはこの
関数を複数回呼んではならず `resolve_bundle` を使う旨)を追加した。

## consumer 側(`search/ninfty-evidence-union.py`)の置換

`_resolve_native_registry(raw)` の内部を2段に分離した:
1. well-shaped-ref ゲート(`native_registry_refs[native_a/native_b]` の形式
   検査のみ、registry access なし)— 変更なし、従来どおり側ごとに独立して
   MISSING を出せる。
2. ゲートを通った側の artifact_id を**まとめて1回**
   `reg.resolve_bundle([...])` へ渡し、その1個の返り値から各側の `entry`
   を取り出す。**side ごとに `reg.resolve(...)` を呼ぶ経路は削除した**
   (旧: `entry = reg.resolve(ref["artifact_id"])` を for ループ内で
   side ごとに実行 → 新: ループの外で `bundle = reg.resolve_bundle([...])`
   を1回実行してから、ループ内は `bundle["artifacts"].get(...)` を引くだけ)。

`FREEZE_MISMATCH` の cross-side チェック(便91 blocker 10、両 lane が個別に
PASS した後で解決済み `freeze_id` を突き合わせる)はそのまま維持した —
P92-6 は「防御的に残すこと」を明記しており、`resolve_bundle` 経由なら
同一 generation から来る以上この不一致は構造的に起こり得ないが、将来
consumer が別の `registry_dir`/generation ポインタへ2 lane を誤って
向けた場合の多層防御として残す判断は F92-6.2 の設計判断3件目とも整合する。

`reg.index_exists()` による MISSING/UNKNOWN の分岐(artifact_id が bundle
内で見つからなかった場合)は従来のまま独立した呼び出しとして残した —
この呼び出しは artifact の**内容**を返さないため(存在有無の粗い
probe のみ)、A/B 混成の攻撃面にはならない。

## race 負例(`search/test_ninfty_evidence_union.py` §16、新設)

同一 freeze_id ('freeze-race') を共有する3つの**別 generation**
(gen16_0/1/2、`publish=False` で明示的に段階公開を制御)を用意し、以下を
確認した:

- **§16a(バグ級の再現)**: `reg.resolve("race_a")` → 手動で
  `prov.publish_generation(gen16_1)` → `reg.resolve("race_b")` という、
  旧設計そのままの「side ごとに `resolve()` を呼ぶ」パターンを直接実行し、
  gen16_0 の `race_a` + gen16_1 の `race_b` という混成ペアが
  **同一 freeze_id を持ったまま**得られることを確認 — W92-6 が指摘した
  反例をコード上で再現し、既存の負例(v11 §15j)がこれを一切捕捉して
  いなかったことを実証した。
- **§16b(`resolve_bundle` の免疫、primitive レベル)**: `reg._read_current`
  を monkeypatch し、「CURRENT を読むその一瞬」に publisher が次の
  generation(gen16_2)を publish する、という最悪ケースの interleaving を
  注入した状態で `reg.resolve_bundle(["race_a","race_b"])` を実行。返り値の
  `generation_id` は読み出し時点で捕捉した gen16_1 のままであり、
  `race_a`/`race_b` の content もどちらも gen16_1 のもの(gen16_2 の値とは
  一切混ざらない)であることを確認 — CURRENT.json はこの時点で実際に
  gen16_2 を指しているにもかかわらず、である。
- **§16c(consumer 層での同じ確認)**: 同じ swap-during-read interleaving を
  `eu._registry()` が実際にロードしているモジュールインスタンスへ注入し、
  P92-6 が修理対象として指定した `_resolve_native_registry` を直接呼び出して
  overall PASS・native_a/native_b とも gen16_1 の内容のみであることを確認。
  primitive レベルだけでなく、修理された facade 自身が race に対して
  fail-safe であることを直接検証した。

3負例とも「混成受理が不可能」であることを示した(P92-6 が許容する2つの
帰結「不可能 or fail-closed」のうち、不可能の方を選んで実装・確認)。

## F92-6.2(設計判断3件)への対応

1. **旧 flat 3 ファイルの残置**: Sol は「production provisioning 時には
   quarantine/remove し、future fallback が再利用しないことを明示」を条件に
   一移行期間の残置を許容した。今回のタスクは production store の内容変更を
   スコープ外とする既存指示の下にあり、実ファイル操作は行っていない —
   **明記事項として**: `search/certs/ep_registry/{index.json, 092a...json,
   29d1...json, 06e7...json}`(旧 flat 形式)は、便91設計以降すでに新
   resolver からは構造的に無視されている(`resolve()`/`resolve_bundle()`
   ともに `CURRENT.json` + `generations/` 形式しか見ない)。**production
   provisioning(実データを `search/certs/ep_registry/` へ commit_generation
   する、研究者認可待ちの別タスク)を実施する際は、この3ファイルを
   quarantine(別ディレクトリへ退避)または削除してから行うこと** — 新
   generation-commit 形式が万一これらを参照する経路を将来のコード変更が
   誤って再開通させた場合の fallback 再利用を防ぐため。本追補をその
   時点の実施条件として記録する。
2. **旧 API の `NotImplementedError` stub**: `write_production_receipt`
   (`search/ninfty-native-registry-provisioning.py`)は Sol の言う
   「fail-fast migration として一時的に妥当」の対象そのもの — 変更なし
   (caller が完全に消滅した時点で stub 自体を削除する、という Sol の
   条件も維持)。**"旧 `write_entry` 記述" の docstring 修正**は別の
   場所にあった実際の不整合を修理した:
   `search/test_ninfty_evidence_union.py` 冒頭(旧 74-97 行目付近)の
   コメントブロックが、便91 で `write_entry` → `commit_generation` へ
   API が変わった後も「`prov.write_entry(...)` を呼ぶ」という**もはや
   事実でない**記述のまま残っていた(実際のコードは全箇所
   `prov.commit_generation(...)` を呼んでいる)。`commit_generation`/
   `resolve_bundle` を指す記述へ修正し、v11 での API 変更を明記する
   注記を追加した。
3. **generation 内を「同一 freeze の任意個 artifacts」に一般化すること
   自体は許容**: 変更不要 — `resolve_bundle` は `artifact_ids`(任意個の
   リスト)を受け取る一般設計にしてあり、EP consumer 側は引き続き
   native_a/native_b の2件だけを exact に要求する(`well_shaped_refs`
   に載った側の `artifact_id` のみを渡す)。registry 全体を2 lane に
   狭める変更は行っていない。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 227/227 checks passed. (exit 0; v11 時点 223/223 + 4 新規 §16)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰ゼロ)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
合計 555/555 全 green。
```

## 状態・逸脱

Sol 便92(P92-6/W92-6/F92-6.2)の是正として実装。変更ファイル:
`search/ninfty-native-registry.py`(`resolve_bundle` 新設・`resolve` の
docstring に CAUTION 追記)・`search/ninfty-evidence-union.py`
(`_resolve_native_registry` を「side ごとに `resolve()`」から「1回の
`resolve_bundle([...])`」へ置換 — well-shaped-ref ゲート自体は不変)・
`search/test_ninfty_evidence_union.py`(`_StubReg` に `resolve_bundle`
メソッド追加 — 便91 由来の consumer 層 FREEZE_MISMATCH 単体テストを
新しい呼び出し経路で維持するため・§16 新設(race 負例3件)・冒頭コメントの
`write_entry` 記述誤りを `commit_generation`/`resolve_bundle` へ訂正)。
4 suite 合計 555/555 全 green。commit していない(司令塔検分後)。

**逸脱・懸案**:
- production store の実 quarantine/削除は本タスクのスコープ外(F92-6.2
  項目1 は「production provisioning 時」を条件としており、今回は
  provisioning そのものを行っていない)— 上記「明記事項」として次回の
  production provisioning タスクの実施条件に記録するに留めた。実ファイル
  操作は行っていない(研究者認可待ちの別タスクの範囲)。
- W92-8(Sol の再入場条件 (a)〜(d))のうち、本タスクは (a) bundle
  resolver と同一-freeze race 負例、(b) 修理後の全 suite receipt、を
  満たす。(c) 実 A/B production artifacts と bundle receipt、(d) 実 CI
  run receipt、は依然として別タスク(production provisioning・Actions
  実走)の範囲であり、本追補では対応していない — EP registry の
  再発効判定はこれらが揃うまで保留のまま。
- F92-6.3(cake_lpr)は便91 追補(v11)で既に静的検証済みで、本便での
  追加指摘はなかった(実 CI run と production artifact/receipt が未実施
  という同じ懸案が継続)ため、本追補では再言及のみで再修理は行っていない。
