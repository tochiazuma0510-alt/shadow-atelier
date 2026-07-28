# 裁定 127 — verifier 相互非互換の発見と修理方針(2026-07-28)

## 発見(curve-witness 最小実装の前哨で・実測)
- **両 verifier は同一 field 名に非互換な形状を要求**(A = object-keyed 辞書 / B = フラット配列)— どんな generator でも「両 full PASS」は JSON 構造上不可能。
- **verifier B は lane A の実形状でクラッシュ**(W-2/2′/3/4)し、**W-1/W-6 は欠落キーの既定値同士の空虚な一致で見かけ PASS(fail-open 欠陥)**。
- 実装者は「不正確な生成物で目標を装う」ことを拒否して停止・裁定要請 — **模範対応として採録**(見かけの進捗より構造ブロッカーの報告)。

## 裁定
- **権威は spec v18 §4.1 の certificate schema のみ**(lane A の形も B の形も権威でない)。「B を A に合わせる」案は棄却 — 両 lane が凍結 spec から独立に形状を導出し、逸脱側(両方の可能性)を修理する。
- **fail-open の禁止**: 欠落キーは明示 ABSENT か FAIL — 既定値による空虚 PASS は契約の fail-closed 哲学違反として両 verifier で点検。
- **P76-3 パターンの拡張**: 受領側に certificate-schema validator gate を新設(manifest compiler と同型 — schema 不適合の証明書は verifier に到達させない)。schema ファイルは共有入力(実装共有ではない — manifest v13 の入力/実装分離則に適合)。
- 凍結との関係: 凍結は文書であり実装でない — 実装を凍結文書へ適合させる修理は receipt の認可範囲内。

## 配分
①lane A: spec §4.1 から形状導出・verifier A/generator の逸脱修理。②lane B: 同・特に fail-open 除去とクラッシュ耐性。③EP runner: certificate-schema validator gate。修理後に witness generator 再着手 → EP 再申請。
