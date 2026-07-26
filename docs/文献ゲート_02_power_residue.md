# 文献ゲート 02 — 円分体での冪剰余 exact 判定(文献要請 2 の関所処理・2026-07-27 司令塔)

経路: ①要請駆動(Opus・Rule 1 §11.6)。検索: paper-scout(docs/scout/scout_20260727_power_residue.md・候補 6 件・最有力 2 件は一次 PDF 読了済)。

## 採否

- **採用(第一正典)**: H. Cohen, *Advanced Topics in Computational Number Theory*(GTM 193, Springer 2000)— **定理 10.2.9(Hecke)**: v_𝔭(α) mod ℓ による分解型の完全判定(証明つき)= Rule 1 §8.3 の obstruction (O-a) の正典形。**アルゴリズム 10.2.14/10.2.15**(ℓ 乗剰余判定・正当性証明つき)+ §5.2(ζ_ℓ ∈ K での巡回拡大の特徴づけ)。
- **採用(補助)**: X.-F. Roblot, "Polynomial Factorization Algorithms over Number Fields"(J. Symb. Comput. 2002)— T^n − a の既約判定の一般ルート(定理 3.2/4.1/4.2・系 4.4・証明つき)= Rule 1 §8.3 (O-b)(O-c) の実装裏付け。
- 空振り申告の受理: Belabas 個別論文・certified computation 専門文献は未達(scout の予算切れ・報告書に明記)。必要になれば追加検索。

## 翻訳(一工夫)— 便 32 で Rule 1 §8 に添付

- K = ℚ(ζ₂₀)・n = 10 = 2·5 は **CRT 分解(Rule 1 (8.1))後、ℓ = 2, 5 のどちらも ζ_ℓ ∈ K が自明に成立**するため、Cohen の Kummer 理論設定(ζ_ℓ ∈ K を仮定)が**そのまま**適用できる — 一般数体用の重い機構は不要。
- (O-a) の証明書は Hecke 判定の形「(v) のイデアル分解を厳密に取り、v_𝔭(v) ≢ 0 (mod ℓ) の 𝔭 を一つ提示」で書く — Rule 1 の「探索失敗は証明書でない」と整合。
- 【注意】Cohen のアルゴリズムは「正当性証明つきの記述」であり、実装(どのライブラリで再現するか)は §8.6 の版固定の対象。文献は仕様の裏取りであって実装の免罪符ではない。

## 台帳

scout 報告と本メモを commit。数学者への降ろしは便 32(Rule 1 §8 の出典欄として)。
