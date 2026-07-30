# 裁定 237 — ideas_013(採掘場 mine)検分・v0 採用・実装発注

日付: 2026-07-30
裁定者: 司令塔
入力: `ideas/ideas_013_solver_platform.md`(発案係・Fable 5 再走版)・研究者指示「作らないの?」= 実装 go

## 検分

1. 棚卸し(§1)は実ファイル確認と明記・G1〜G8 のギャップ同定は研究者の問題意識(点在・やり直し)と一致。外部調査(§2)は URL つき・「この工房のどの仕事の型に効くか」軸で評価・落選理由明記(Magma 不要の明言を含む)。
2. 設計(§4)は既存規律との互換表(§4.8)を持ち、探索器/照合器分離・ソルバー哲学(claim_class 二値)・prediction-first・machine-piped を**規範から機構へ**降ろす方向 — 工房の設計思想と整合。
3. 自己監査(§7)が誠実(官僚化リスク筆頭・「カード化は走った後でよい」の逃げ道明文化)。

## 採用(v0 — §6 のとおり・修正 2 点つき)

- **v0 範囲**: mine-dispatch.yml(mb-search 複製改造・backend gap-ci のみ)+ mine-job/v1 schema + preflight + collector 最小 + 梯子テンプレ。名称 `mine/` 採用。
- **第一号ジョブ = 梯子走査の較正再走**(修正 1): 新窓でなく**既存 13 窓の CI 再発車**とし、collector が「artifact の新 cert ⟷ repo 収蔵済み cert(GAP 側)・既存 python recheck cert(checker 側)」の対付け集計を出すこと。結果が既知なので基盤のバグが即見える = v0 受け入れ試験。実弾(t=5,6 延長・q=7・S>D₈)は v0 検収後。
- **shard(修正 2)**: driver(strike-a13-ladder.g)に preamble での窓選択 knob が既にあればそれで窓 shard・無ければ v0 は非分割 1 job で可(driver 改変は禁止 — shard knob 追加は v1)。
- 官僚化防止条項(§7-1)を明文採用: exploration ジョブの preflight は schema 検査のみ・カード化は走った後でよい。
- 新規ツール導入(CaDiCaL/cake_lpr/ganak/Vole)は v0 に含めない(v2/v3 のとおり)。
- 実行係(miner 係)の職務規程ファイル起草も v0 に含める(.claude/agents/miner.md・次セッションから有効・§5 の境界表どおり)。

## 発注(implementer・worktree 隔離)

境界: `mine/` 新設+`.github/workflows/mine-dispatch.yml`+`.claude/agents/miner.md` のみ。**判定ロジック(kerchi-judge.g・strike-*.g・照合器 .py)と search/certs/ は不可侵**。push は司令塔が検分後に実施(push = 第一号ジョブ発車のため)。

## 関連

- EP は接続点予約のみ(§1.8)・封印/金庫は不可触(§4.8)— 発注にも同条件を明記。
- v1(述語台帳の棚入れ 10〜15 枚)は v0 検収後に別発注。カード起草は数学の行為につき数学者+司令塔レビュー(§4.2 の三段)。
