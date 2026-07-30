# 文献ゲート配達覚書 — 剛性・Hurwitz 系・分解数の計数(v1)

- 起草: 司令塔(2026-07-30 深夜)。きっかけ = ① 要請駆動: `docs/notes/sat_l1_v1.md` §9.2【文献要請】(剛性 N=1 判定)+ ② 司令塔発: 実現探索の系統的障害 2 件(裁定 240 追記 2 — n=10 の A₅ 障害・n=12 の位数 3840 障害)と n=27 乱択の絶望(hit ~10⁻¹⁰)。
- 配達物: 原文 3 本(papers/delivered/・ハッシュは LEDGER 2026-07-30 欄)+ 書誌 3 件 + 本覚書。配達先 = 両数学者(Opus = SendMessage・Sol = 便 89 同梱)。
- 原著は資料庫(全読義務なし・読んだ範囲は申告)。**本覚書は翻訳であり数学の正本ではない** — 精読者の訂正を歓迎(過去に覚書の粗さが数学者精読で修正された実績あり)。

## 0. 我々の問題(降ろす先の正確な形)

固定 w₀ ∈ S_n(型指定・例: (5,5,2)@n=12・(5⁵,2)@n=27)に対し
$$\mathcal F(w_0)=\{(g,h):\ g^2=1,\ h^3=1,\ gh=w_0,\ \langle g,h\rangle=G\}\quad(G=S_n\ \text{or}\ A_n)$$
の (i) **非空性と個数**(実現探索の存在判定)・(ii) **C_G(w₀)-共役軌道数 N**(剛性・CENT の |ker|=|C(w₀)|·N の N)。

## 1. 配達 3 本(一工夫つき)

### 1.1 Liu–Osserman, *The irreducibility of certain pure-cycle Hurwitz spaces*(arXiv:math/0609118)
- **機構**: genus-0 の Hurwitz 空間で braid 軌道が**単一**になる(既約性)ことの証明 — 「軌道数 1」を出す定理の実物。
- **一工夫(適用境界)**: 対象は pure-cycle(各分岐点上の非自明巡回が 1 本)に限定。我々の三つ組 (2^k1^*, 3^j1^*, w₀-型) は一般に pure-cycle でない — **直接適用不可**。輸入すべきは結論でなく**手法**(帰納の骨格・退化での軌道追跡)。w₀ が単一巡回+互換 1 本の族(P-WALL 系)は「準 pure-cycle」で最も近い。
- 検分点: 我々の n=10 退化(50 対 = |C((5,5))| ちょうど・剛性 N=1)がこの枠でどう見えるか。

### 1.2 Magaard–Shpectorov–Völklein, *A GAP package for braid orbit computation*(arXiv:math/0304376)
- **機構**: Nielsen 類上の braid 軌道を**機械計算**する GAP パッケージ(MAPCLASS 系譜)。
- **一工夫**: 我々の N(剛性欄)は braid 軌道でなく **C(w₀)-共役軌道**だが、小 n では両方を GAP で直接数えられる。**採掘場 mine の述語カード候補**(「N 計算」explorer)としてそのまま実装可能な見込み — ただしパッケージ導入可否(GAP 4.16 適合)は要確認。
- 検分点: 既測 11 窓の N=1 を第三系統で再計算できるか。

### 1.3 Fried, *Variables separated equations...*(arXiv:1012.5297)
- **機構**: Branch Cycle Lemma と Hurwitz 空間の連結成分の関係のサーベイ(背景・語彙の辞書)。
- **一工夫**: BCL は「どの分岐データが ℚ 上定義できるか」の必要条件 — **P1 線(u 測定・M1 passport)にも接続**する(passport の ℚ-有理性)。深追いは要請駆動で。

## 2. 書誌のみ(3 件)

- **Serre, *Topics in Galois Theory* Ch.7-8**(書籍): 剛性判定の教科書形+**Frobenius の公式**(分解数 = (|C₁||C₂||C₃|/|G|)·Σ_χ χ(c₁)χ(c₂)χ(c₃)/χ(1))。
- **Malle–Matzat, *Inverse Galois Theory***(書籍・DOI 10.1007/978-3-662-12123-8): 剛性・rationally rigid の体系。
- **Hall 1936, *The Eulerian functions of a group***(Quart. J. Math. os-7, 134–151・**DOI 10.1093/qmath/os-7.1.134 一次確認済**): 部分群格子の Möbius 関数による**非生成対の差し引き** — 分解数から生成対数を出す標準手続き。

## 3. 障害 2 件への即効の見立て(candidate・検分対象)

1. **存在判定は走査不要で先に出る**: S₁₂/S₂₇ の指標表(GAP: `CharacterTable("Symmetric",n)` 系)で Frobenius 公式を機械計算すれば、(2 類, 3 類, w₀ 類) の**分解数そのもの**が厳密に出る。n=12 の「hit 100・全て位数 3840」も、n=27 の存在可否も、**指標和 1 本で事前判定**できるはず — 乱択の全廃。
2. **生成の差し引き**: 分解数 > 0 でも生成しない(A₅・3840 障害)分は Hall の Möbius 反転(部分群にわたる和)で除ける。3840 障害の正体は「(2,3,10)-三つ組を通す真部分群」の同定問題 — 指標計算と併走で機械的に潰せる。
3. **この 2 段(Frobenius+Möbius)を mine の述語カード「REALIZE-COUNT」にする**のが実装の自然形(explorer = GAP 指標計算・checker = 独立実装 or 小 n 悉皆突合)。

## 4. 警戒

- 型 C(束ねない): 剛性(braid 軌道)と C(w₀)-軌道と Nielsen 類は近縁の別物 — 翻訳時に混同しない(N の定義は sat_l1_v1 §7 が正本)。
- 新規性警報: 対称群の (2,3,·)-分解の存在域は古典で相当に既知の可能性(Bertram/Boccara 系譜 — scout 未確認につき候補外・必要なら図書館検索を別途)。「初」を言う前に grep+文献。
