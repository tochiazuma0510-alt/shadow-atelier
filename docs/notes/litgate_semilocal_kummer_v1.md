# 文献ゲート翻訳メモ — 半局所 Kummer(TAIL-OBS 超えの機構)v1

**状態札: 司令塔翻訳・candidate**(2026-07-30。きっかけ = ①要請駆動: `docs/notes/surj_d4_t1_v1.md` の【文献要請】。出典 = `docs/scout/scout_report_semilocal_kummer_20260730.md`(配達済みアーカイブ)。**配達の形**: 本覚書+原文 6 本 = `papers/delivered/arxiv_{1301.4429, 0809.0017, 1507.07208, 2408.13108, 1504.02814, 2506.11310}.pdf`(ハッシュは LEDGER)。Jacobson–Vélez 1990(manuscripta math. 67, 271–284・DOI 10.1007/BF02568433)は誌面のみ — 書誌+入手経路注記。**原著は資料庫・全読義務なし**・読んだ範囲は申告)

## 1. 困難の再述(TAIL-OBS の言葉で)

尾部 t≥1 の窓では cusp λ⁻¹(0) が単一 K-有理点でなく**複数点**に割れ、(W4)(全分岐)が空 ⟹ 橋 B_FC の u 同定が止まる(裁定 217)。問い: 多点の主係数たちから K の Kummer 類を**正準に**切り出せるか。

## 2. 機構の抽出(一工夫 — B₃-gentle への翻訳)

- **(型 A・本命)ノルム関手**: cusp 集合を点の集合でなく**有限エタール K-代数 E**(= 各 cusp の剰余体の積)と読む。主係数は自然に [u]_E ∈ E^×/E^{×M} に住み、K へ降ろす正準写像は **corestriction/ノルム**しかない(束ね方の恣意性は「ノルム関手の一意性」問題に転化)。**候補定義 NORM-U**: [u]_K := N_{E/K}([u]_E) ∈ K^×/K^{×M}。Borne–Emsalem–Stix(1301.4429)の境界 **packet+トーラス torsor** がこの処方の幾何的正当化の最有力・前身 = Stix 0809.0017(cuspidal sections の Kummer 構成)。
- **(型 B・代替)マーキング**: Sijsling–Voight(1504.02814)型 —「cusp を 1 点 mark すれば moduli 体上に降下する」。我々には **canonical 生成対(LID-1)が既にある** ⟹ 正準マーキングは規約として実装可能。**候補定義 MARK-U**: canonical 対が指す cusp の局所 u。NORM-U との一致/不一致自体が測定項目になる。
- **(型 C・警戒)束ねないのが正解の可能性**: field of moduli/definition の局所版として「cusp ごとの類の族」が本体で、単一類への圧縮は情報を落とす — 検証は NORM-U と MARK-U の判別窓で。
- **(語彙翻訳)**: divisorial inertia の cyclotomic 作用を非彩色ブレイドで扱う流儀(1507.07208)は Garside 元 Δ² = 我々の中心 c と語彙一致 — 「非全分岐 = 彩色を落とした divisor」の読み替えで、B₃-gentle の hexagon-only 設定への持ち込み口。接基点の正準化は log 構造の virtual morphism(2408.13108・parenthesized braids)が翻訳コスト最小。

## 3. 新規性警報(義務事項)

**層 II(Hol 値表現 ⟺ 捻れ Kummer 指標)の辞書は古典既決の疑い**: O'Dorney 2506.11310(H¹ ⇄ Hol のエタール代数辞書)+ Jacobson–Vélez 1990(x^N−a の Galois 群 = holomorph 部分群の明示)。**surj ノート次版では層 II を「新規」と書かず、この 2 本との突合の上で引用に切り替えること**(novelty grep 規律の文献版)。

## 4. 数学者への設問

- **【LG-3】** NORM-U と MARK-U を W-E-A10-9t1(尾部 t=1・cusp 2 点: 9 点軌道+固定点)で具体的に書き下し、(ii-loc)/(ii-win) 型の well-defined 性がどちらで立つか判定せよ。両者が一致する/しないの判別も。
- **【LG-4】** NORM-U 採用時、B_FC の四段(型・剛性 descent・局所 Kummer・torsor 比較)のどの段がそのまま通り、どの段に E/K ノルムの挿入が要るか — 「橋 B_FC^sl(半局所版)」の要修理箇所リストを作れ(証明はまだよい・設計図まで)。

**注意**: 型 C が正なら【LG-4】は空振りになる — その判定を【LG-3】が先に行う設計。凍結済み予言(i10_1 の 11 欄・41b8698)には非接触。
