# CLAUDE.md — 影工房 (Shadow Atelier)

**常に日本語で応答すること**(数式・固有名詞・コードは除く)。

## このプロジェクトは何か

ユーザー本人の**研究プロジェクト**: **有限 GT-shadow の算術実現性**(Dolgushev ら)。G_ℚ → GTSh(K,K) の全射性(dihedral 予想: 2 冪位数は証明済み・一般は明示予想)を含む問題群に、計算と証明書で参入する。

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
- **内製部隊の職務規程**: `.claude/agents/` に 4 役 — reader(inherit/high)・implementer(sonnet/medium)・falsifier(sonnet/medium)・ops-clerk(haiku/low)。Agent tool の subagent_type で指定。**セッション起動時に読み込まれるため、新設・変更は次セッションから有効**(未読み込みセッションでは general-purpose + model 明示で代替)。
- **宇宙の事前登録**: 対象の位数・生成系を先に固定し、後から変えない。**UNKNOWN は一級の結果**。負の探索結果は非存在の証明ではない。
- 出所管理: ソフトのバージョン・seed・入力ハッシュ・全証明書ハッシュを記録(`provenance/LEDGER.md`)。既知例は positive/negative/adversarial の三分で常備。
- 環境: Windows。GAP 4.16.0 導入済み(`C:\Program Files\GAP-4.16.0`)。**実行は必ずプロジェクト直下の `gap.ps1` 経由**(`gap.bat` は別窓を開くため自動実行不可)。
- **体制の正本: `docs/体制と道具.md`(v2・2026-07-18 承認)**: ES7 全面継承+影工房差分。**研究者=ユーザー本人(数学の主役)、司令塔=Claude(継続・コーチ兼務)、Sol=常設の数学監査官 兼 共同設計者**(週 2〜3 便の事前承認枠; 定義ゲート・go/no-go・定理候補のゲート便はスキップ不可)、Luna=休眠増援。停止ゲート: 枠外課金・クラウド工場・public 化・撤退条件変更のみ。数学的判断の所有権を段階的にユーザーへ移す。v1 は docs/archive/。

## 進行状態

- **フェーズ 0 完了(2026-07-18)**: GAP 4.16.0 インストール+動作確認(`search/smoke-test.g`)、論文 3 本入手(`papers/`、テキスト版 `papers/txt/`、ハッシュは `provenance/LEDGER.md`)。
- **次: Week 1** — 2401.06870(定義の正本)で GTSh の定義系を読み、2106.06645 の実装入口と突き合わせ、既知の 2 冪 dihedral 例の再現に着手。
- ユーザーの背景・応対トーン: `../galois-atelier/CLAUDE.md` と同じ(数学科卒・ガロア圏読書中・「才能の壁」への配慮・実績根拠の励まし・誇張なし)。
