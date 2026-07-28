# 内部前哨ゲート報告(便 69 発送前・falsifier・2026-07-28)

対象: docs/mb_dependency_manifest_v5.md / docs/mb_ninfty_verifier_contract_v5.md / docs/week4-NInfty_stage2_spec_v10.md + search/bundle-selfaudit.py。self-audit 9/9 ALL PASS の**外側**を敵対監査した結果。判定は司令塔裁定 84 で確定。

## FINDING-1(重大・freeze-blocking)— B68-3 修理の entry 粒度での再発

I-0c′ 手順 (3)「D-4 を対応 build record を持つ各 entry についても再計算し top-level と相互照合」は実行不能:
- `subject_code_digest` は top-level record にのみ存在し、**manifest_entry スキーマ(§2)に無い**。E-10 は entry 側 D-4 の第一成分の出所を定義していない。
- 読み (a) top-level 値の流用 → entry の build_definition/pinned_inputs は top-level と異なるため「相互照合」が恒常不一致(一致するのは build artifact 共有 = 本来 I-3d が [11] で弾くケースのみ)。読み (b) entry の content_digest 代入 →「top-level と相互照合」が無意味。どちらも破綻。
- R-1〜R-6 は依然「X が import/link/load する dependency」だけを entry 化し、**subject X 自身の entry が存在しない**ため「対応 build record を持つ entry」の参照先が未定義。
- 帰結: SB-3 の「Q1 反例は閉じる」は top-level についてのみ真。entry レベルでは「c を計算に含めず binding を自称する」同型反例が再構成できる。

## FINDING-2(要修正)— spec §4.1 の未定義フィールド `verifier_evidence`

certificate schema 最終欄 `verifier_evidence` はどこにも定義されない。§4.4 が定義するのは `independence_evidence` であり、§5.2 SEALED_INTERNAL でも certificate と並列の別オブジェクト。contract v5 に `verifier_evidence` は一度も出現せず、**検査契約がこの欄を検査しない**。

## FINDING-3(要修正)— covered_procedure_checks に完全性保証が無い

CR-1/2 の registry 再生成+集合等式は clause 側のみ。check 側(D-*/U-*/P-*/W-*/S*)には母集合を機械確定する規則が無く、**check を黙って落としても CR-2/3/4 のどれも検出しない** — 「procedure check への分離」が義務の格下げになっている。現行 3 文書の check 列挙は手作業で網羅されているが機構は守っていない。

## FINDING-4(script 要修正)— 除外域が構造でなく部分文字列

- HIST 除外は「記録」「自認」等 15 語の**行内部分一致** — contract v5:42(§0.1 の operative 本文)が「記録」を含むだけで sweep 対象外。この行自体 LA-2 の配置規約(historical ID は差分表・supersedes・自認文のみ)に違反。
- live_authority_refs[]/historical_quotation_refs[] の 14 行ウィンドウ除外も文字列出現位置ベース(spec 内 6 箇所)— コードフェンス境界に基づかず、将来の版で語が本文に出れば無審査ゾーンが生じる。
- `【v4 新設】` 型の裸 v トークンは 7 pattern の探索対象外(除外でなく不可視)。

## PASS(確認済み)

pin 値=実ファイル sha256 一致(stale 0)・契約↔manifest 相互条項 26 ID 実在一致・nominal typing 再発なし・日本語別名 0・§参照の実在一致。

## UNKNOWN(一級で記録)

procedure_checks を欠落させた悪意 record の実機実験は未実施(紙上論証のみ)。S5 側の内容照合は対象外。receipt プレースホルダは freeze 前につき対象外。便 65〜67 で PASS 済み項目の再攻撃は B68-3 の深掘りのみ。
