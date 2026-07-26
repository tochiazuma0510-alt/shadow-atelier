# 論文検索係 報告 — 2026-07-26

## 任務1: ヤコビアン予想の反例(出典狩り)

**結論: 実在確認済み(ただし arXiv 未掲載・SNS/ブログ発信が一次情報)。**

| 項目 | 内容 |
|---|---|
| 発表者 | Levent Alpöge(Harvard/Anthropic)。問題提起は Akhil Mathew。計算補助に Claude Fable 5(Anthropic)使用と明記 |
| 発表日時 | 2026-07-20 02:19 UTC 頃、X(旧Twitter)投稿 |
| arXiv/DOI | **未確認(UNVERIFIED)**。複数ニュース記事が「a preprint/verification preprint」と言及するが、arXiv 上の Alpöge 名義著者ページ(arxiv.org/a/alpoge_l_1)を実地確認したところ 2026 年の投稿は存在せず、最新は 2408.11653(2024-08, Conditional algorithmic Mordell)。**arXiv 番号は特定できなかった** — 出典明記できるのは SNS 投稿とそれを追ったブログ/ニュースのみ |
| 反例の写像 F | 次元 3(ℂ³→ℂ³)。u = 1+xy とおいて<br>F(x,y,z) = ( u³z + y²u(4+3xy), y + 3xu²z + 3xy²(4+3xy), 2x − 3x²y − x³z )<br>ヤコビアン行列式は恒等的に **−2**(定数・非零) |
| 非単射性の証拠 | 3 点 (0,0,−1/4), (1,−3/2,13/2), (−1,3/2,13/2) が全て (−1/4,0,0) へ写る(3点衝突) → 大域可逆でない → n=3 での反例 |
| 検証状況 | 複数の数学者が Wolfram Alpha / SymPy で独立に初等計算(行列式展開・3点代入)を再現し正当性を確認したと複数の一次〜二次情報源が報告。Terence Tao もブログで解説("A digestion of the Jacobian conjecture counterexample", terrytao.wordpress.com, 2026-07-21) |
| 射程 | n≥3 で偽であることを示す(具体的族は各 n≥3 に一般化可能と報道)。**n=2(平面版)は依然未解決** |

### 出典(実地確認済み URL)
- https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/ (Fields 賞受賞者ブログ、内容の数学的解説あり — 最も信頼度が高い一次級情報)
- https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/ (Secret Blogging Seminar、専門家ブログ)
- https://www.johndcook.com/blog/2026/07/21/jacobian-conjecture/
- https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883 (The Conversation、学術系メディア)
- https://news.ycombinator.com/item?id=48973869
- https://www.coindesk.com/tech/2026/07/21/claude-s-fable-5-just-solved-an-87-year-old-math-problem-and-it-matters-for-bitcoin
- 補助(未検証度が高い二次情報・要注意): explainx.ai, kingy.ai, glitchwire.com, biggo.com, gktoday.in, newsbytesapp.com, thenextweb.com, elsolitario.org("Still Unsolved" と懐疑的な記事も存在 — 意見の割れに留意)
- 未実在確認: zzhang-iu.github.io("Direct Consequences..." — 個人サイト論文、著者所属不明)、aaronlou.com(個人サイト、"Deriving an Explicit Polynomial Counterexample" — 導出解説、査読なし)、ulam.ai/research/jacobian.pdf(AI企業らしきドメイン、査読なし)、jacobianfun.org(出所不明サイト)

### 評価メモ(採否判断はしない — 事実確認のみ)
- **最も硬い根拠**: Terence Tao と Secret Blogging Seminar という実名・実在の専門家ブログが独立に数式を追認していること。ニュース記事群の再現する式は完全に一致(u=1+xy の式・−1/4,0,0 への衝突)しており、捏造の兆候はない。
- **弱い点**: 2026-07-26 時点で arXiv・DOI 付きの正式プレプリントが確認できない。「査読前preprint」に言及する記事はあるが、リンク先が特定できなかった。→ **出典の格は「SNS発 + 専門家ブログ検証」であって「査読前提出済み論文」ではない**、と明記して司令塔へ引き渡す。
- 数学的評価(反例が本工房の何に効くか等)は司令塔/reader の仕事のため立ち入らない。

---

## 任務2: 主要未解決リストの鮮度再スイープ(前回 2026-07-25 比)

| 対象 | 前回状態 | 今回の観測 | 変化 |
|---|---|---|---|
| Conjecture 5.1(arXiv 2405.11725, dihedral 予想) | 被引用0 | **v2 が 2026-01-13 に改訂**(v1: 2024-05-20)。ファイルサイズ同等(34KB)で大幅増補ではない模様。Conjecture 5.1 の文言自体は温存(「G_ℚ → GTSh(K,K) が dihedral poset の任意の対象 K で全射」)。被引用の新規確認は取れず(Semantic Scholar 個別ページの実地取得に失敗、UNKNOWN のまま) | **小変化あり(v2 改訂)** — 中身の差分は未確認、要 reader 深読み |
| fake GT-shadow(pentagon 無しでの非 genuine 対象)の存在への進展 | 情報なし | 具体的な新規結果は発見できず | **変化なし(UNKNOWN継続)** |
| ĜT = ĜT_gen(pentagon 独立性)への進展 | 情報なし | arXiv **2503.13006**(Noémie C. Combe, 単著, 2025-03-17 提出・2025-07-02 改訂)が「GT 予想(GT≅Gal)を profinite spaces の設定で証明」と主張。ただし pentagon 独立性そのものではなく別アプローチ(“path integral”・“Cubic Matrioshka”)。**単著・査読なし・専門家からの追認情報は検索で見つからず** — 赤旗案件として ★B4系寄りの一般 GT 予想であり本工房の hexagon-only 系(B₃-gentle)とは直接一致しない | **新規発見(要注意扱い)** — 「B₄系・査読前・単独主張」の札をつけて記帳 |

### 使用クエリ・空振り角度
- `"Grothendieck-Teichmuller" shadow dihedral conjecture 2026 arXiv` — GT-shadows/gentle論文がヒットしたが dihedral予想の直接進展は無し
- `arXiv 2405.11725 citations 2026` — 被引用リストは arXiv 検索からは得られず(Semantic Scholar 直接取得も失敗、ページ構造上ヘッダーのみ取得)
- `"fake ĜT" OR "fake GT-shadow" OR "pentagon independent" Grothendieck-Teichmuller 2026` — 空振り。関連論文(2401.06870, GRT survey等)がヒットするのみで、pentagon非依存性への新規結果は確認できず
- 個別 arXiv ページ実地確認: 2405.11725(v2 改訂確認)、2503.13006(内容確認・赤旗評価)

**UNKNOWN の明記**: fake GT-shadow の存在、および pentagon 独立性への直接的な進展は、今回の窓でも確認できなかった(非存在の証明ではない)。Semantic Scholar での被引用リスト取得は技術的に失敗しており、再試行の余地あり(次回はarXivのTrackback機能や Google Scholar 直接検索を推奨)。
