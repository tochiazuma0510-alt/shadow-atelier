# Luna 委嘱 106-BU — BOTTOM-UP freeze blocker 修理束

## 0. 役割・目的

あなたは Luna（実装・計算増援）。`ops/inbox_codex/sol_task_106_math33.txt` §3 と `sol/sol_reply_105_math32.md` F105-3.2 の freeze blocker を物理成果物まで修理する。探索・kill・候補生成は行わない。

## 1. 正式な意図

FREEZE-2 の exact universe は現 17 行:

~~~text
p=2: dim in {2,3,4}
p=3: dim={2}
window_order <= 8000
~~~

この集合を prose、schema、manifest、fixture、分母で一意にする。M-ISO-8 は verdict mismatch ではなく、real/mutant とも `UNKNOWN(NONSHADOW_IN_DATUM)` のまま detail の `settled=false` 対 `true` が mutant を kill する、という v2.1 の機構へ versioned erratum を作る。

## 2. 要求成果物

1. 既存文書を上書きせず、BOTTOM-UP design の versioned correction/addendum を作る。
2. IF-FIRST M-ISO-8 の versioned erratum を作る。
3. exact 17-row universe を列挙・再導出できる、発火 cert schema と manifest を物理化する。
4. 正 fixture と、p=2 dim 0/1、p=3 dim 0/1/3/4、order cap 超過、欠落/重複、旧 M-ISO-8 読み等を拒絶する mutant fixture/check を作る。
5. source-map、schema version、digest、STOP/UNKNOWN、traversed_count と accepted_count の区別、禁止された claim（isolated=FALSE 等）を manifest に束縛する。

## 3. 六点 delegation envelope

1. **入力**: 既存 v4/v2.1/CV-9/17-row 資料と登録 fixture のみ。
2. **出力**: versioned docs、schema/manifest/checker/fixture/receipt、`sol/luna_reply_106_bu.md`。
3. **禁止**: S1–S3.5 発火、S9、掘削、候補/kill/EMPTY の実データ生成、封印量接触、workflow dispatch、git commit/push、credential 読取/出力。
4. **停止条件**: 17 行が既存資料から一意に再構成不能、または数学仕様変更が必要なら BLOCKED。
5. **検収**: positive と全 mutant-negative、exit code、再現コマンド、SHA-256、変更一覧を記録。
6. **権限**: 実装のみ。freeze ID/PASS/S1 unlock は Sol の再監査事項。

## 4. 書込範囲

- BOTTOM-UP 用の新規 versioned `docs/notes/w6_bottomup_*` / `docs/notes/iso_r3r4_*`
- `search/probe/w6_bu_s0/**`
- BOTTOM-UP 用の新規 schema/manifest/fixture/receipt (`search/certs/w6_bu_*` 等)
- `sol/luna_reply_106_bu.md`

範囲外、特に `.github/**`、HS、Lean、既存裁定・既存 reply は変更しない。

## 5. 納品

全 numbered item を処理し、未完は OPEN/BLOCKED とする。`git diff --check` と対象 status を確認。commit/push はしない。
