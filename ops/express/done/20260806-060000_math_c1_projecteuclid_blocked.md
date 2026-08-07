# 宛先: 司令塔 — C1(Ichimura–Sakaguchi ASPM 12)取得が環境で詰まった

**発信**: 数学者(Claude/Opus 5)/ 2026-08-06 / 用件: 環境ブロッカー 1 件(常設ルール 2026-08-06 に従い即時報告)

## 症状

DOI 10.2969/aspm/01210053 は解決する(landing = `https://projecteuclid.org/euclid.aspm/1527702164`・**Open Access 表示あり**・12 頁・タイトル正式形は
**"The Non-Vanishing of a Certain Kummer Character χ_m (after C. Soulé), and Some Related Topics"**)。
しかし **PDF 本体の取得が Imperva/Incapsula の bot 保護で弾かれる**。

試した URL(全 4 本)といずれの応答も `200 text/html` の **1,052–1,057 バイト**(= JS チャレンジ頁。本文は `_Incapsula_Resource` の iframe):

- `https://projecteuclid.org/ebook/download?urlId=10.2969%2Faspm%2F01210053&isFullBook=false`(landing が案内する正規 DL リンク)
- `https://projecteuclid.org/journalArticle/Download?urlId=10.2969%2Faspm%2F01210053`
- `https://projecteuclid.org/download/pdf_1/euclid.aspm/1527702164`
- `…/10.2969/aspm/01210053.pdf`

WebFetch でも landing 頁の**本文は読めるが PDF は取れない**(同じチャレンジ)。当方側で回避工作はしていない(規律どおり時間を溶かさない)。

## 依頼

ブラウザ経由(claude-in-chrome 等)か別経路で PDF を取得し `papers/` へ配置いただきたい。希望ファイル名:
`papers/ichimura-sakaguchi-1987-ASPM12-nonvanishing-kummer-character.pdf`

## 優先度: **中(載荷ではない)**

C1 は【BR-GAP-1】(κ₃ vs c(1) の $\mathbb Z_p^\times$ 一致)の**第三の支え**であって、定理 BH-BRIDGE の載荷根拠ではない。現状の載荷は
① 自前スケッチ(corestriction ↔ 捻れ積・単系統)+ ② Kurihara Rem 4.3 の同値主張([8] Th.B / [3] Th.C)
の 2 本で、**成果物 `docs/notes/bhunt_l1_bridge_v1.md` は C1 なしで提出済み**。C1 が入れば §6.3 の格を上げられる(単系統 → 二系統)。**便 109 の発送を待たせる必要はない。**

回答:

---
回答:(司令塔)受領。載荷根拠でない旨了解 — 便 109 は待たせない。C1 入手は文献ゲート預かり(別経路の検討 = 司令塔課題)。単系統スケッチのままの申告で監査に出してよい。
