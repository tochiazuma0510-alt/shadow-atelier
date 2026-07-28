# 裁定 169 — kerchi-judge v1 検収+FINDING KJ-1(2026-07-29)

## 受理
- kerchi-judge v1(入力 2 方式・(F2)→閉性→T-A→核可換性→witness→導来列・CI 使用例つき)。self-test FAILS = 0(W-C-p5 = ABELIAN 40・c∈N 対照 = ABELIAN 12・crosscheck 一致)。
- K(3) 代用の判断 = 承認(全 B₃ marking の K⁽ⁿ⁾ 構築は未実装 — 捏造で静かに誤 PASS するより検証済み窓で代用が正しい)。「K⁽ⁿ⁾ の B₃-marking 構築」は小型委嘱として待ち行列へ(dihedral 族は理論確定済みのため低優先)。

## FINDING KJ-1: (F2) 述語に settled(well-definedness)条項の欠落
- 判定器の新設チェック(全 m の (3.53) 正則表現構築)が W-A-B3idx126-s2(c∈N・P_N = C7:C3)で発火: (F2) 全項目 PASS の候補 (m=2, f=1) が**そもそも自己準同型として well-defined でない**(x↦x², y↦y² が fail)。
- 正体: (F2) 実装は生成(全射)を見るが**準同型性(settled)を見ていない** — 監査 札B 修正が処方した一行(GroupHomomorphismByImages ≠ fail)が (F2) 実装に未配線だった。v1〜v4 のどのチェックにも捕まらず、判定器の閉性 assert で初めて表面化。**fail-closed 積層の三匹目**(T-A×2・閉性×1)。
- 影響評価: v4 の 17 窓と W-C-p5 は閉性が成立していたため実害なしの見込み — ただし settled 条項追加後の再走で確認する。
## 処置
①(F2) に settled 一行を追加 ②idx126-s2 再判定+v4 17 窓+W-C-p5 の回帰確認 ③判定器 v1.1 へ。地図 delta: 補給線に kerchi-judge(前線)・帯 1 の道具箱に KJ-1 の教訓を追記。
