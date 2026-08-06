# B₄ 低指数窓 R0 probe — 事前登録票 v1(IF-FIRST・**発火前**)

**状態札: `prereg (pre-firing) / 走行ゼロ / LINS 未実行 / census 未生成 / 封印非接触 / 発火は司令塔が別途`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔 **裁定 637 ③**(便 112 返書の宿題)。標的の同定は **裁定 635 の帰結**(= 本票 §2 の紙の下界)。
- 入力正本(すべて既在):
  - `docs/notes/b4_mirror_transfer_design_v1.md` **v1.2 §13**(補題 TRI-ABEL・命題 NO-SMALL-NONAB・**系 INDEX-LB**)/ **§4.3**(帯の梯子 R0–R3・層定義・記号衝突 W-1)/ **§4.1**(補題 FIXED-B4)
  - `docs/notes/b4_original_gtshadows_extraction_v1.md`(窓の定義 $\mathrm{NFI}_{PB_4}(B_4)$・(A.2)(A.5))
  - `search/lins-twin-census-v1.g` + `search/certs/lins_twin_census_v1_20260806.json`(**B₃ 版の実測コスト** = 唯一のコスト錨)
  - `docs/notes/twin_witness_prereg_iffirst_v1.md`(**prereg の型紙**: §1 登録・§5 出力規則・§6 停止規則)
- **本票の位置づけ**: 登録集合・手順・出力文言・停止規則を**機械実行の前に固定する**。本票のコミットをもって凍結とし、**発火(LINS 実行)は司令塔が別途行う**。数学者は走らせない。

> ## 非接触・規律の申告(本票作成時点)
> **機械ゼロ**(GAP 起動なし・LINS なし・python なし・cert 生成なし)。封印 3 量非接触・705,894 対宇宙非接触・$\mathrm{Im}\,R$/$d_N$ 非接触・B₃ 側 L3 層非接触。本票は**発火請求ではなく登録**である。

---

## 0. 一枚まとめ(6 行)

1. **標的は 1 点**: $B_4$-指数 **192**(= $\lvert PB_4/\widetilde N\rvert=8$)の**非可換窓**が存在するか。
2. なぜ 1 点か: 紙で **非可換窓 ⟹ 指数 $\ge192$**(系 INDEX-LB)、かつ $\lvert Q\rvert\in\{6,10\}$ 型は**排除済**(命題 NO-SMALL-NONAB)。⟹ 上界 240 の走査で実際に検定されるのは $\lvert Q\rvert=8$ ちょうど。
3. **走るのは LINS 1 回だけ**($B_4$・指数上界 **240**・単一プロセス・単一呼び出し = LID-1)。
4. **壁時計 cap 15 分**。超過は `TIME_CAP / STOP`(**R1 以降へ自動拡張しない**)。
5. **R0 で非発見でも「指数 1000 まで非可換窓は無い」とは結論しない**(§6 の禁止語)。
6. IF-FIRST 予言 **P-R0-1〜4** を発火前に固定(§5)。外れた場合の扱いも先に決める。

---

## 1. 登録(scope ①)— 宇宙・道具・記録欄

### 1.1 底群と表示(**後から変えない**)

$$B_4=\langle\sigma_1,\sigma_2,\sigma_3\mid \sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2,\ \ \sigma_2\sigma_3\sigma_2=\sigma_3\sigma_2\sigma_3,\ \ \sigma_1\sigma_3=\sigma_3\sigma_1\rangle$$

GAP 生成元名は `a,b,c`($a=\sigma_1,b=\sigma_2,c=\sigma_3$)。**中心は $\Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4$ と書く**(⚠ 記号 `c₄` は本リポジトリでは `Chk6` の第 4 条件を指す別物 — 設計 v1 §1.2 の警告 W-1。GAP 生成元 `c` と混同しないよう、中心は必ず `Delta4sq` と命名する)。

### 1.2 探索(**これ 1 回だけ**)

| 項目 | 値(**凍結**) |
|---|---|
| 呼び出し | `LowIndexNormalSubgroupsSearch(B4fp, 240)` — **単一プロセス・単一呼び出し(LID-1)** |
| `census_index_hi` | **240** |
| 反復・段階的引き上げ | **禁止**(R1=480 以降へ自動で進まない。別票 v2 が要る) |
| 壁時計 cap | **15 分**(超過で中断・部分結果は「未完」と明記して破棄しない) |
| メモリ | `gap.ps1 -o 2g` |

### 1.3 各 node に記録する欄(**発火前に固定**)

`index` / `in_PB4`($\widetilde N\le PB_4$ ⟺ 指数が 24 の倍数 **かつ** 生成元語がすべて純)/ `delta2_in_N`($\Delta_4^2\in\widetilde N$)/ `Q_order` $=[PB_4:\widetilde N]=$ `index`$/24$ / `Q_is_abelian` / `Q_id_group` / `Q_structure` / `canonical_id_words` / `Qhat_id_group`($B_4/\widetilde N$)。

> **★ 判定の核**: `in_PB4 = true` かつ **`Q_is_abelian = false`** の node が 1 つでもあるか。それが本 probe の**唯一の主判定**である。

### 1.4 依存(登録と同時に固定)

| # | 依存 | 破れたときの影響 |
|---|---|---|
| **D-R0-1** | LINS の指数 $\le240$ 悉皆性 | 「未発見」の意味が消える(**存在の主張は無傷**) |
| **D-R0-2** | 上界 240 | 結論は**この上界つきでのみ**有効 |
| **D-R0-3** | `in_PB4` 判定の正しさ(24 の倍数だけでは不十分・語の純性で確認) | 窓の同定が壊れる ⟹ S-R0-2 |
| **D-R0-4** | 紙の入力(INDEX-LB・NO-SMALL-NONAB)= 設計 v1.2 §13 | **標的の絞り込みだけ**に効く。走査自体は無傷 |

---

## 2. 標的の紙の根拠(裁定 635 の帰結・**再掲**)

窓 $\widetilde N\in\mathrm{NFI}_{PB_4}(B_4)$、$Q:=PB_4/\widetilde N$、$[B_4:\widetilde N]=24\lvert Q\rvert$。

- **補題 TRI-ABEL**: $Q$ 非可換 $\iff$ ある三つ組 $\{i,j,k\}$ で $T_{ijk}=\langle a_{ij},a_{ik},a_{jk}\rangle$ が非可換。
- **命題 NO-SMALL-NONAB**: $Q\ne S_3,\ D_5$(および奇二面体群・$\mathrm{Dih}(C_3^2)$ 型)。
- **系 INDEX-LB**: $$\textbf{非可換窓が存在するなら }\lvert Q\rvert\ge8\iff[B_4:\widetilde N]\ge\mathbf{192}.$$

$$\Longrightarrow\ \boxed{\ \text{上界 240 の走査で検定されるのは }\lvert Q\rvert=8\ (\text{指数 }192)\ \textbf{ちょうど 1 点}\ }$$

($\lvert Q\rvert=9$ は可換のみ(位数 $p^2$)、$\lvert Q\rvert=10$ は排除済 ⟹ 240 以下で残る非可換候補は 8 のみ。$\lvert Q\rvert=8$ は $D_4$ か $Q_8$。)

---

## 3. 出力 cert(schema・発火前に固定)

`search/certs/b4_r0_probe_v1_<date>.json`:
```
{ prereg_doc_sha256, gap_version, package_versions,
  base_group: "B4 = <a,b,c | aba=bab, bcb=cbc, ac=ca>",
  census_index_hi: 240, lins_calls: 1, lins_nodes_total_this_call, lins_elapsed_ms, total_elapsed_ms,
  wall_cap_ms: 900000, cap_hit: false,
  nodes: [ { index, in_PB4, delta2_in_N, Q_order, Q_is_abelian, Q_id_group, Q_structure,
             Qhat_id_group, canonical_id_words } ],
  windows_total, windows_abelian, windows_nonabelian,
  nonabelian_windows: [ ... ],                  # 空でもよい(空であること自体が結果)
  verdict: "NONABELIAN_WINDOW_FOUND | NOT_FOUND_WITHIN_240 | STOP(<reason>)",
  grade: "candidate / single-system / not cross-checked / not verified (no Lean)" }
```

---

## 4. 出力規則(**文言を発火前に固定**)

### 4.1 非発見のとき(**この文言以外を書かない**)

> 「$B_4$ の指数 $\le240$ の正規部分群の悉皆探索において、$\widetilde N\le PB_4$ かつ $PB_4/\widetilde N$ が**非可換**であるものは**未発見**である。」

### 4.2 ★ 禁止語(書いたら `OVERCLAIM / STOP`)

- 「**指数 1000 まで非可換窓は存在しない**」「$[PB_4:\widetilde N]\le41$ の窓はすべて可換」— **R0 は 240 までしか見ていない**。P-B4-1(設計 v1 §4.3.4)は**依然として予想のまま**であり、R0 の非発見はその**部分的支持**にすぎない。
- 「鏡映双子はゼロ」— 本 probe は**双子も $\iota$ も計算しない**(§1.3 の欄に無い)。
- 「$B_4$ 窓には exotic が無い」「GT-shadow が無い」— **GT-shadow の述語($T_{m,f}$・hexagon・pentagon・charming・settled/isolated)は一切評価しない**。
- 「Ñ_core / Ñ\* に関する何か」— 現用 2 窓は本 probe の対象外(そもそも指数が桁違い)。

### 4.3 発見のとき

$\lvert Q\rvert=8$ の非可換窓が出たら: (a) `Q_id_group` で $D_4$/$Q_8$ を同定、(b) 設計 v1 §13.2 の (T1)(T2)(T3) と**矛盾しないか**を照合(矛盾すれば実装バグの信号 ⟹ S-R0-3)、(c) **その窓 1 個について**のみ $\iota$ 判定(語の生成元反転)を**別タスクとして**起票する(本票では実行しない)。

---

## 5. IF-FIRST 予言(**発火前に固定・反証可能**)

> - **P-R0-1(主予言)**: 指数 $\le240$ に**非可換窓は無い**(`verdict = NOT_FOUND_WITHIN_240`)。
>   - 根拠: $PB_4^{\rm ab}=\mathbf Z^6$ は小さい可換商を大量に供給する一方、$\lvert Q\rvert=8$ の非可換商が $B_4$-正規性(= $S_4$-安定性)と両立するかは未知。**弱い予言**であり、**外れたら良い知らせ**(紙で追えない構造が帯内に居る)。
> - **P-R0-2**: 見つかる窓(可換)の $\lvert Q\rvert$ は **$2^a3^b$ 型に偏る**($[B_4:PB_4]=24$ の整除性と $\mathbf Z^6$ の $S_4$-加群構造から)。**$\lvert Q\rvert=5,7$ が出たら注目**($q\ge5$ の Sylow は MIRROR-ODD-B4 の標的層)。
> - **P-R0-3(コスト)**: LINS 本体は **B₃ の指数 1000(149 秒)より短い**。$B_4$ は生成元が 1 本多いが**上界が 1/4 以下**であるため。⟹ 15 分 cap には**当たらない**。
> - **P-R0-4**: `delta2_in_N = false` の窓が存在する(= 中心荷重が非ゼロの層が $B_4$ でも空でない)。B₃ の混在対の $B_4$ 版が見えるかの前哨。
> - **予言が外れたときの扱い**: P-R0-1 が外れる(= 非可換窓発見)⟹ **STOP しない・大成功として §4.3 へ**。P-R0-3 が外れる(cap 到達)⟹ `TIME_CAP / STOP` で終了し、**R1 へは進まない**(別票)。

---

## 6. 停止規則(発火前に登録)

| # | trigger | verdict |
|---|---|---|
| **S-R0-1** | LINS 呼び出しが 2 回以上・または `census_index_hi ≠ 240` | `LID_VIOLATION / STOP` |
| **S-R0-2** | `in_PB4` 判定が「指数が 24 の倍数」だけで行われた(語の純性検査なし) | `WINDOW_TEST_BROKEN / STOP` |
| **S-R0-3** | 発見された非可換窓が (T1) 同位数 / (T2) 遠可換 / (T3) 三角の中心 のどれかに反する | `PAPER_CONFLICT / STOP`(紙か実装のどちらかが誤り。**先に紙を疑う**) |
| **S-R0-4** | 壁時計 15 分超過 | `TIME_CAP / STOP`(**R1 へ進まない**) |
| **S-R0-5** | 出力に §4.2 の禁止語が現れた | `OVERCLAIM / STOP` |
| **S-R0-6** | 本票に無い量(双子・$\iota$・GT-shadow 述語・封印量)を計算した | `SCOPE_CREEP / STOP` |

---

## 7. 実行チェックリスト(発火時にこの順で・**司令塔が実施**)

1. 本票の sha256 を cert の `prereg_doc_sha256` に書く(**本票のコミット後に確定**)。
2. $B_4$ の表示を §1.1 と**バイト単位で**一致させる(生成元順・関係式順)。
3. サニティ: $[B_4:PB_4]=24$ を機械で確認(既知値との突合)。落ちたら STOP。
4. LINS を **1 回**走らせる(cap 15 分)。
5. 各 node に §1.3 の欄を付す。**主判定は `in_PB4 ∧ ¬Q_is_abelian` の有無ただ 1 つ**。
6. §4 の文言規則で結論を書く。§5 の予言との突合表を必ず添える。
7. **R1 以降には自動で進まない。** 進むなら本票の versioned 後継(v2)で再登録する。

---

## 8. 【GAP】・格

| # | 内容 |
|---|---|
| **【R0-GAP-1】** | 本 probe は **単一系統**(GAP のみ)。二系統一致は取らない ⟹ **格は candidate 止まり**(cross-checked ではない)。非可換窓が**発見された**場合のみ、第二系統(python での語→置換表現の再検査)を別タスクで起票する |
| **【R0-GAP-2】** | 「非可換窓が無い」の主張は **D-R0-1(LINS 悉皆性)に条件つき**。LINS 自体の悉皆性は工房で独立検証していない(B₃ 版でも同じ依存) |
| **【R0-GAP-3】** | P-B4-1(帯 1000 まで可換)の**完全解決は本票の射程外**。R0 は下端 1 点の検定にすぎない |

**格の宣言**: 本 probe の出力は **candidate / single-system / not cross-checked / not verified (no Lean)**。**GT-shadow の述語には一切触れない**ので、`isolated` / `settled` / `genuine` の語を出力に書いてはならない。
