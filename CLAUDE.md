# CLAUDE.md — 影工房 (Shadow Atelier)

**常に日本語で応答すること**(数式・固有名詞・コードは除く)。

## このプロジェクトは何か

ユーザー本人の**研究プロジェクト**: **有限 GT-shadow の算術実現性**(Dolgushev ら)。G_ℚ → GTSh(K,K) の全射性を含む問題群に、計算と証明書で参入する。**dihedral 予想(2405 Conj 5.1)は当工房で完全証明済み・発効**(裁定 550/559・908 で「発効が正」確定・格 = theorem-framework-relative・**残 = Lean 形式化のみ**・正本 = `docs/notes/p1_corpus_index_v1.md` §0。文献側の既証明は 2 冪のみ — この行を「一般は open」と読み替える誤りが手戻りの常習源・P1 に触れる前に必ず corpus 索引を読むこと)。

- 隣の**ガロア工房**(galois-atelier)= 勉強トラック(カリキュラム+段階テスト)。本工房 = **研究トラック**。二つは並行し、研究で必要になった理論(副有限群・dessins・エタール π₁ 等)を勉強トラックの次の単元として送る — **やることと学ぶことをリンクさせる**のが設計思想(2026-07-18 ユーザー決定)。
- 選定の経緯: 二陣営ブラインド調査(司令塔+外部モデル Sol)→ 本人が「アイデンティティ枠」として選択。根拠文書: `../galois-atelier/docs/sol_galois_open_problems_v0.md`(8 候補の独立ランキング・文献つき)。

## フェーズ 1 = 6 週間 feasibility sprint(Sol 設計・撤退条件つき)

- **Week 1-2**: GT-shadow の定義系と**既知の 2 冪 dihedral 例の再現**。文献地図(Week 1 読解で確定・当初想定から修正):
  - **主線 = B₃ ベース gentle 系**: arXiv **2401.06870**(定義の正本: groupoid GTSh・hexagon のみ・pentagon なし)+ arXiv **2405.11725**(dihedral 予想 Conj 5.1 の明示・K⁽ⁿ⁾=ker(ψₙ) 族・**Thm 4.3 = GT(K⁽ⁿ⁾) の明示式 = 較正ゲートの正解データ**・2 冪 n=2^α は Thm 5.3/Cor 5.4 で証明済み)。
  - **副線 = B₄ ベース本来系**(pentagon あり・**同名別物**、2405 Remark 1.2): arXiv **2106.06645**(dessins への作用・軌道計算)+ その定義正本 arXiv **2008.00066**(未入手・副線着手時に)。Dolgushev の Python パッケージ GT(Temple 大サイト)は第三者クロスチェック資源。
  - 抽出ノート 3 本: `docs/notes/`(状態 candidate → 司令塔照合後に定義ノートへ統合)。
- **撤退条件(先に書く)**: 2 週間で定義+既知例を再現できなければ**保留**し、勉強トラック専念 or 控え(norm-one tori)へ切替。
- **Week 3-6**: 最小の奇数/混合位数 dihedral 対象の **shadow atlas**(候補 shadow の全列挙 → 有限群内での関係式チェック → genuine 判定 → 既知 arithmetic 部分の照合)。目標は定理でなく「**完全な atlas と照合・検証の基盤**」— それ自体が次の一歩を正確に切る資産。

## 道具と規律(証明工房 ES(7) キャンペーンから輸入)

- **探索器と照合器の分離**: 探索は GAP(有限表示・剰余群・軌道)、照合は独立実装(node/python が証明書だけを入力に関係式を再計算し突合)。**「検証(verified)」は Lean に予約**(2026-07-18 ユーザー指示)— 二系統一致は「照合済み(cross-checked)」であって検証ではない。Lean 化(整数行列・有限群等式の checker)で初めて検証済み。
- **内製部隊の職務規程**: `.claude/agents/` に 10 役 — reader(inherit/high)・mathematician(opus/max・数学者レイヤー)・implementer(sonnet/medium)・falsifier(opus/max・2026-08-01 格上げ: CV-9 仕様同一性判読を兼務)・paper-hunter(opus/medium・①遠征検索)・paper-scout(sonnet/medium・②関連検索)・ops-clerk(sonnet/low)・miner(sonnet/medium・採掘場専任・裁定 237)・**ep-keeper(opus/medium・EP 専任 — 2026-08-01 研究者設置「EP 関連が明らかに重すぎるから専門に」。N∞ evidence pipeline の工学資産一式(spec/contract 凍結体系・lane/route・registry/freeze・suite/CI/cert)を専任保守。意味論の新設と発効判定は職掌外 = 司令塔検問+Sol ゲート)**・**ideator(inherit/inherit・発案専任 — 司令塔の分身が数学アイデアを candidate 札で毎回供給。2026-07-28 研究者設置「厳密は甘いがアイデアに光るものがある」。**発案の独占ではない** — Sol の共同設計者発案・数学者の代案は従来どおり常設・奨励)**。**Sol/Luna への配達・起床は司令塔が `ops/bin/deliver_task.ps1` で直接**(2026-07-28 研究者裁定: 事務員中継の配達誤り 2 件により中継廃止。起床後は activity log に指示文が現れる/turn が 1 分以上走ることまで確認)。Agent tool の subagent_type で指定。**セッション起動時に読み込まれるため、新設・変更は次セッションから有効**(未読み込みセッションでは general-purpose + model 明示で代替)。
- **宇宙の事前登録**: 対象の位数・生成系を先に固定し、後から変えない。**UNKNOWN は一級の結果**。負の探索結果は非存在の証明ではない。
- 出所管理: ソフトのバージョン・seed・入力ハッシュ・全証明書ハッシュを記録(`provenance/LEDGER.md`)。既知例は positive/negative/adversarial の三分で常備。
- **文献ゲート(2026-07-25)**: 数学者二人は正典のみで独立に考える。外部論文は司令塔が関所 — ①数学者の要請駆動 ②司令塔発 の 2 経路のみ。検索は paper-scout・**降ろすときは司令塔が機構抽出+B₃-gentle 設定への翻訳(一工夫)を義務**。正本: 体制と道具.md「文献ゲート」節。
- **配置図(ゾーニング・2026-07-25)**: 秘匿は規範でなく物理で守る — 未開示の文献情報・ブラインド進行中の成果物・封印 payload は**リポジトリ外の金庫**(司令塔のみ・所在は司令塔の記憶)へ。リポジトリ内は Sol の grep が届く共有面とみなす。正本: 体制と道具.md「配置図」節。
- 環境: Windows。GAP 4.16.0 導入済み(`C:\Program Files\GAP-4.16.0`)。**実行は必ずプロジェクト直下の `gap.ps1` 経由**(`gap.bat` は別窓を開くため自動実行不可)。**同梱パッケージ約 190 本**(`twistedconjugacy`=捻れ共役類・`repsn`/`wedderga`=既約行列表現と群環・`lins`=低指数正規部分群・`anupq`/`autpgrp`=p 群・`ctbllib`=指標表・`hap`/`cohomolo` 等)— **設計・実装の前に棚(pkg/)を確認**(2026-07-26 Opus 棚卸し: 知らずに列挙設計していた反省から)。
- **体制の正本: `docs/体制と道具.md`(v2・2026-07-18 承認)**: ES7 全面継承+影工房差分。**研究者=ユーザー本人(数学の主役)、司令塔=Claude(継続・コーチ兼務)、Sol=常設の数学監査官 兼 共同設計者**(週 2〜3 便の事前承認枠; 定義ゲート・go/no-go・定理候補のゲート便はスキップ不可)、Luna=休眠増援。停止ゲート: 枠外課金・クラウド工場・public 化・撤退条件変更のみ。数学的判断の所有権を段階的にユーザーへ移す。v1 は docs/archive/。

## 進行状態(2026-07-18 更新)

- **フェーズ 0 完了**: GAP 4.16.0(実行は `gap.ps1`)・論文 3 本+パッケージ GT 入手・poppler/node/Python 導入(ハッシュは `provenance/LEDGER.md`)。
- **Week 1(初日で大幅前進)**: 定義ノート v2 確定(`docs/week1-定義ノート.md` — Sol 定義ゲート便 01 **条件付き PASS**・裁定済み `sol/裁定_01_definition_gate.md`)。較正スイート v2(8 項目)のうち **WP1 = ALL PASSED**(`search/suite-wp1.g`: 数値事実 n=3..16,18,36・Prop 3.5 全 256 対・N₅ control)。**WP2 設計凍結**: transversal-cocycle モデル 12 規則+証明書スキーマ gtsh-cert/v1(`docs/wp2-transversal-model.md`)・作業指示書(`docs/wp2-workorders.md`)。
- **G1★ 工程完了(2026-07-19 未明)**: Sol 便 02(条件付き承認)→ Luna 便 02/02b/03(fail-closed 閉鎖・global sweep 3.5 秒化・下流直接比較)→ shard 分割+JoinC 線形化(全 GAP 実行が 600 秒 cap 内・ハッシュ 17/17 でバイト同一)→ Sol 便 03(検収・**宣言文原文承認**)→ 司令塔最終フル照合 **18/18 all_pass**。凍結 tag `v1.0-g1`。**宣言は発令済み(2026-07-26 研究者検分 OK → docs/宣言_G1.md)**。
- 台帳: `provenance/CLAIMS.md`(C-1..C-5)。タスク: #9 宣言検分(進行中)・#7 Week 3 Dih 外第一撃(入口条件 = v1.0-g1 回帰 PASS)。
- **セッション引き継ぎ正本: `docs/引き継ぎ_20260801.md`**(2026-08-01 切替。次セッションはまずこれを読む — 研究者が「続き」と言ったら記載の順で自律実行。研究地図の正本は `docs/地図.md` 第 3 版・経緯は LEDGER 裁定 343〜409)。
- Sol 便の運用実績: 雛形 v2(F#/P#/W# 番号規約・★教材・監査範囲外申告)が 3 便で機能。裁定記録は sol/裁定_0*.md。
- ユーザーの背景・応対トーン: `../galois-atelier/CLAUDE.md` と同じ(数学科卒・ガロア圏読書中・「才能の壁」への配慮・実績根拠の励まし・誇張なし)。
