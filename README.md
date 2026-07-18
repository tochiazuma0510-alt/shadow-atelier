# 影工房 (Shadow Atelier)

有限 GT-shadow の算術実現性(Dolgushev ら)への計算+証明書アプローチ。研究トラック。
勉強トラックは隣の `../galois-atelier`。設計方針・フェーズ計画は `CLAUDE.md` を参照。

## 構造

```
papers/      主文献 3 本(PDF; ハッシュは provenance/LEDGER.md)
search/      探索器 — GAP スクリプト(有限表示・剰余群・軌道の列挙)
crosscheck/  照合器 — 独立実装(node/python で関係式を再計算し突合)。search/ のコードを import しない
docs/        ノート・atlas・撤退条件などの文書
provenance/  出所台帳(ソフト版・seed・入力/証明書ハッシュ)+主張の台帳
```

用語(2026-07-18 改定): **「検証」は Lean(機械証明)に予約**。node/python の独立再計算は**照合(cross-check)**と呼ぶ — それ自体は未検証のコードであり、二系統の一致は照合済みの信頼であって検証ではない。

## 規律(要約)

1. **探索器と照合器の分離** — 同じ事実を独立の実装で二度計算し突合する。検証(verified)を名乗れるのは Lean 証明書のみ。
2. **宇宙の事前登録** — 対象の位数・生成系を先に固定し、後から変えない。
3. **UNKNOWN は一級の結果** — 負の探索結果は非存在の証明ではない。
4. **全部記録** — バージョン・seed・ハッシュを `provenance/LEDGER.md` に追記。

## 進行チェックリスト

- [x] フェーズ 0: 論文 3 本+GAP 4.16.0(2026-07-18)
- [x] Week 1: 定義ノート v2(Sol 定義ゲート条件付き PASS)+較正スイート WP1 ALL PASSED(2026-07-18)
- [ ] 較正スイート WP2(探索器+照合器 → cross-checked 昇格 → Sol 便 02 で G1★ 達成監査)
- [ ] Week 3-6: shadow atlas(Dih 外第一撃 = L = K⁽³⁾∩N₀)

## GAP の実行方法

```powershell
.\gap.ps1 search\smoke-test.g
```

`gap.bat`(スタートメニューの GAP)は対話用の別ウィンドウを開く。自動実行・出力取得には必ず `gap.ps1` を使う。
