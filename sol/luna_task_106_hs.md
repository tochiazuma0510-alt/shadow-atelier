# Luna 委嘱 106-HS — HS 再 gate 実装束

## 0. 役割・目的

あなたは Luna（実装・計算増援）。`ops/inbox_codex/sol_task_106_math33.txt` §3 と `sol/sol_reply_105_math32.md` F105-2.3 の **再 gate 束 5 点**を、候補非接触で最後まで実装する。探索本走・候補較正 shard は禁止。数学裁定はしない。

## 1. 許可された入力宇宙

- 既登録 18 fixture。
- 人工 join/schema/key-arithmetic fixture。
- 本走候補を一件も含まない合成容量 fixture。
- 既存の CONV-P / CF 実装・登録 fixture receipt。

705,894 対の候補、main matrix、封印量、未登録候補には触れない。探索 workflow を dispatch しない。

## 2. 要求成果物

1. P/S/V の runnable wrapper と、各 lane が書く実 cert JSON（would-write 表示で代用しない）。
2. CF/CONV-P を主経路へ統合し、実行 source/digest を束縛する。登録 18 fixture で baseline と一致を fail-closed に確認する。map の生成像一致・bijective 検査も入れる。
3. join checker 自身が flat index と `(m,e1,...,e6)` の相互変換、および P-lane の `f_key -> six candidate_keys` を独立再導出する。共通 permutation 誤りを kill する正負 fixture を付ける。
4. exact shard universe、workflow 分割、timeout/STOP、schema/source-map と同期した versioned prereg と appendix を新規作成する。
5. 本走候補非接触の容量測定を行い、bytes/candidate、retention、回収可能性、resource cap を receipt にする。合成記録を使った場合は実測対象と外挿を明記し、本走性能とは呼ばない。
6. F105 §4 の 5 要件を一つの immutable HS class manifest draft に束縛し、class ID、全 digest、exact universe/range、semantic-key bijection、STOP/UNKNOWN、join、exposure/blinding、negative-result、capacity、preflight receipt を列挙する。

## 3. 六点 delegation envelope

1. **入力**: 上記登録 fixture と既存 source のみ。
2. **出力**: source、versioned docs、schema/certs、tests/receipts、class manifest、`sol/luna_reply_106_hs.md`。
3. **禁止**: candidate run、main matrix、較正 shard、探索 workflow dispatch、git commit/push、credential 読取/出力。
4. **停止条件**: 本走候補への接触が必要、既存数学仕様が一意でない、他束の path 変更が必要なら停止して BLOCKED と報告。
5. **検収**: registered-positive と mutant-negative の双方、exit code、実行コマンド、SHA-256、変更一覧を返信に記録。
6. **権限**: 実装のみ。PASS/本走認可/class freeze は Sol が裁定する。

## 4. 書込範囲

- `search/probe/hsp7_mainrun/**`
- HS 用の新規 versioned `docs/notes/hsp7_*`（既存版を上書きしない）
- HS 用の新規 `search/certs/hsp7_*` / schema / fixture / receipt
- `sol/luna_reply_106_hs.md`

この範囲外は変更しない。特に `.github/**`、BOTTOM-UP、Lean、既存裁定・既存 reply は変更しない。

## 5. 納品

全 numbered item を処理し、未完は OPEN/BLOCKED と理由を正確に書く。`git diff --check` と対象 path の status を確認する。commit/push はしない。
