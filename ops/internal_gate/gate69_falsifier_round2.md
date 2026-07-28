# 内部前哨ゲート第 2 巡報告(falsifier・v6/v6/v11 限定再ゲート・2026-07-28)

## 判定サマリ
- **FINDING-1 の閉鎖 = 設計として成立**(狭めた正直な主張へ・overclaim なし・SB-6 は I-3d の検出力を毀損しない)。c,b,P,r 一括捏造は D-R4 自認済みの既知限界(新欠陥ではない)。
- **24 件の歴史移設 = 全件正当**(義務消失ゼロ・後継条項全実在)。
- **重大 2 件(新規・cross-document 同期類型)**:
  1. contract §7 の clause-ID 版遅れ — C-1′/C-6‴ が I-0c′(旧)・D-4・D-R2″・SB-1〜SB-3 を参照(現行は D-4′・D-R2‴・I-0c″・SB-5/6 は言及ゼロ)。実装者が contract だけ読むと**修理前の壊れた binding 概念で実装する経路**が残る。
  2. contract §10 live_authority_refs[] が manifest を "v5" とラベルしたまま **v6 の digest** を貼付 — LA-1 が「live 版束縛はここのみ」と定めた block 自身の label-digest 不整合。
- 要修正 2: SB-3′ 直後に D-R4 同水準の限界宣言 / build_record_present 虚偽宣言への R-6+I-3a 補償論法が未明文(N-1 型の証明なし・実装依存部は UNKNOWN)。
- 軽微 2: LA-3 の [historical] ラベルは意味的に不正確(実体は現行 sweep 定義)/【chg】masking の理論的悪用余地(観測なし)。
- script v2 の構造的盲点(自認): cross-doc clause-ID 同期・authblock 内 label↔digest 対応は 11 check のどれも見ていない。

## 教材
「修理の自己完結 ≠ 体系の整合」— 単一文書内で完結した修理でも、参照する側の文書に旧概念が残れば体系としては矛盾仕様。同期は文書単位でなく **clause-ID 単位**で機械検査する必要がある。
