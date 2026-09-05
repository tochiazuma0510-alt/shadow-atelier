# 司令塔 → Astra: resume64(64 step・rank 1450)の工房格付け = cross-checked(限定 8 条)・**rank 1450 を受理**・**前進率の実測(F-r64-1)= 戦略判断案件**(裁定 2154)

falsifier の増分 CV-9 判読(正本 `docs/notes/cegar_resume64_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(20 source が repo とバイト一致・source-receipt 前周回と同一・交差辺 0・head 連鎖 64/64(前 32 は受理済 run と 32/32 一致)・row_pairings 64/64・λ_j·target_j = 1 と λ_j ⊥ 新規行を 64/64 再現・新 32 target.scalar は申告列と完全一致・ZIP 7,916 entry 不一致 0・旧不変 2,582/新 5,145/親 completion 2,699 file 全一致)。追加 3 項: ω 分布 0:29/1:20/2:15・cen_pow = sr(ω) 64/64・三因子 x 41/y 40/**central 35(単独実走 7 step = F-cy-1 完全閉鎖)**・λ の台は 64/64 で character 0 のみ・failed_chord 10 → 122・basis 不変・lead は新 32 が連続 {1530…1561}。**非空虚性の収穫**: target 減算の符号規約が実データで判別される(scalar ≠ 0 の 40 step が逆符号読みを棄却)— 次周回もこの検算を必須にする。工房格 = **checker PASS・cross-checked 限定 8 条 → rank 1450/gen 8155 を受理**。

## F-r64-1(重大・数学/戦略・拡大判断は司令塔と研究者)

CEGAR の**前進率を初めて実測**した:
- 弦は毎段 **全 54,433 が評価**されている(探索 cap ではない — 2149 (vi) の工房の書き方を訂正)。狭いのは witness の選び方 = **roster 順の先頭失敗弦 1 本**。
- 64 段で roster index は 4 → 69(**+1.03/段**・63 遷移中 18 回は後退)・消化率 0.127 %。
- **失敗弦の総数は 66〜67 % で横ばい**(step 0 36,134 → step 63 36,259・正味 +125)= **減っていない**。
- 線形外挿(予言ではない): roster を消し切るには ≈ 5.3×10⁴ 段(rank ≈ 5.5×10⁴)、append 単価 ≥ 25 s で上昇中 → producer 実時間だけで ≥ 15 日。非存在の証明ではない(失敗集合は λ ごとに再計算され一斉零化は排除されない)が、64 観測に収束の兆候なし。

**工房からの上申と候補(採否・設計は Astra)**:
1. 撤退/切替条件を「段数 cap(128/256)」でなく**実測前進率と失敗弦総数の趨勢**で書き直す(例: 次 32 段で失敗総数が有意に減らなければ同 oracle の反復を止める)。
2. **候補(工房発案・candidate 札)**: 各 λ で失敗弦は ≈ 36,000 本あるのに 1 段で 1 本しか materialize していない。**1 つの λ に対し失敗弦を多数(例: roster 先頭から k 本・または basis を変える k 本)同時に Ω 語化 → P1 減算 → lower-zero → 行の線形独立分だけ一括追加**すれば rank の前進は段あたり k 近くになり得る(各行は同じ λ の下で得た独立な violation なので、追加後の Separator 再計算は 1 回で済む)。origin scan の full-origin refinement が 30 分で 26 pivot 出せたのと同じ「λ を固定して多数を刈る」型。CV-9 の射程は「同一 λ 下の k 行の独立性」を⑤に足せば増分で回せる。
3. 代替 oracle の再検討: dual orbit 経路(新 λ で 504 閉包を取り直す・全 32,280 origin)/ v538 ladder(grade 2〜6 を一様に)の紙経路の実装優先度。

## その他

- F-r64-2: workflow jq gate の 13 連言は checker v2 L1493-1500 のリテラルで PASS 側恒真だが、等価な非空虚検査が v2 L894-897/L941-942 にあり**冗長であって根拠欠落ではない**(2149 の工房記述を訂正)。
- 軽微: `new_physical_appends: 64` は累積値(本 run の実 append 32)= 下流の誤読源 / alias 逆対照は sha pin 継承(falsifier が start 33 親凍結・current 97 の動的証拠を実測 — こちらを根拠に)/ target.scalar = 0 は 64 中 23 段。
- 限定 8 条は正本を参照。以上。
