# S3.5 v2 CV-9 判読(falsifier 逐語・裁定 615 で正本化)

著者: falsifier(opus/max)。司令塔指示により ops-clerk が transcript から逐語抽出(2026-08-06)。

---
# S3.5 v2 判読 — TC-GAP-4 / 分布指紋 / F-2 記載

## S1【CV-9 三値裁定】= **同一対象**(条件 1 件つき)

- 数学者側の作動的判定式(P-L3-4): **L-3 ⟺ |im ρ| = 3000·|V|**(§B.4「M_R→V↠head V 全射」から導かれる形)。
- driver 側 PART D: `Hp := Subgroup(pb.Phat,[rho1,rho2]); if Size(Hp) = pb.sizePhat then <L-3>`。
- 実測データから独立確認: **73 の accepted class 全てで `sizePhat` = 3000·p^dim = 3000·|V|**(例外ゼロ)。ゆえに driver の述語は文字どおり |im ρ| = 3000·|V|。**同一対象。**
- 内部整合も独立確認: 全 17 行で「sizeH が 3000|V| に等しい lift 数」= `L3_surjective_lifts`(17/17)。判定器と診断欄に帳簿ずれなし。

### 「同じ誤解を二人で共有」経路の掃討

**【重大・構造的 SM-1】marked lift の規約誤りは L-3 では原理的に検出不能。**
ρ₁ = W_b⁻¹U_a、ρ₂ = U_a⁻¹W_b² に対し
$$\rho_1\rho_2 = W_b^{-1}U_a\,U_a^{-1}W_b^{2} = W_b \implies W_b\in\langle\rho_1,\rho_2\rangle,\quad U_a = W_b\rho_1\in\langle\rho_1,\rho_2\rangle$$
すなわち **⟨ρ₁,ρ₂⟩ = ⟨U_a,W_b⟩ が任意の (a,b)・任意の群で恒等的に成立**。L-3 も像位数指紋も ⟨U_a,W_b⟩ のみの関数であり、**marking 規約に完全に盲**。共通の孫引き元 `bu_s35_embedding_v1.md` EMB-BRAID から両者が σ↦(U,W) の marking 誤り(語の取り違え・twist・役割交換)を継承していても、L-3 の数値も指紋も**一切変わらない**。⟹ 17/17 は **⟨U,W⟩ についての証拠であって ρ についての証拠ではない**。marking の担保は L-1/L-2(N_θ(a)=−ε_Δ、N_τ(b)=−ε_δ)と F-2 fixture 側にあり、本走は検査していない。**これが唯一生き残る留保。**

**【ほぼ閉 SM-2】Phat 構成の共有誤り**: 数学者は Hom_{Ĝ5}(M_R,S) の次元と Bass–Serre 分解から、driver は GAP の fiber product から — 経路が構造的に別。しかも一致は 2 スカラーでなく多重度つき 4 値分布(S2)。**ただしこれは指紋を照合して初めて言える。** 裁定 606 に届いた「17/17」だけではこの経路は開いたままだった。

**【機械錨あり SM-3】|Ĝ5| = 3000**: 共有定数だが `Chk("F-1.5: |Ghat5|", Size(Ghat5), 3000)` + `fails_total = 0` で錨。

**【要修正 SM-4】** 両述語を同一にしている当の錨 `size_Phat_eq_3000_times_V` が cert ではハードコード `true`(S3)。私が実測 73/73 で裏を取ったので事実は成立するが、cert 自身の証拠能力はゼロ。

## S2【分布指紋】—【重大】照合器は分布を一度も比較していない

`crosscheck/compare_l3_pred_vs_meas.py` の分布比較は**両側同時のキー不一致で黙って飛んでいる**:

- 予言側: `pdist = pr.get("image_order_dist") or pr.get("dist")` → ノートの JSON ブロックのキーは **`"image_orders"`** ⟹ `pdist = None`
- cert 側: 行レベルで `image_order_dist|order_dist|im_order|image_orders|diagnostic` を探すが、分布は **`rows[].class_detail[].sizeH_distribution`**(一段深い・別名)⟹ `mrow["dist"] = None`
- ガード `if pdist is not None and mrow["dist"] is not None:` が**両側で偽** ⟹ 警告なしでスキップ

⟹ `l3_pred_vs_meas_20260806.txt` の「rows: match=17 mismatch=0」が実照合したのは **`affine_solution_pairs` と `L3_surjective_lifts` の 2 スカラーのみ**。予言 17 行中 **12 行が L3=0** で、L3 列単独は低エントロピー — 「17/17」は見た目よりはるかに弱い証拠だった。

**欠落分を私が実施 — 17/17 完全一致(多重度まで)**:

| 行 | 予言 = 実測 |
|---|---|
| `p2_d3_a1b0c1` | {3000:16, 6000:16, 12000:16, 24000:16} |
| `p2_d4_a2b0c1` | {3000:32, 6000:96, 12000:32, 24000:96} |
| `p2_d4_a4b0c0` | {3000:16, 6000:240}(ご指定例)|
| `p3_d2_bruteforce_1` | {3000:9, 27000:18} |
| 他 13 行 | 全一致 |

付随して独立確認:
- **P-L3-1 成立**: p=2 の像位数は厳密に {3000, 6000, 12000, 24000} の 4 値のみ、かつ**4 値とも実現**(5 値目なし)。p=3 は {3000, 9000, 27000}。
- **P-L3-2 / P-L3-3 成立**: 類内で割れる行は `p3_d2_bruteforce_1`(1 類・27 lift → 18)**ただ一つ**。p=2 の全類は均一 — 予言どおり。
- **帳簿閉包**: Σ`lane_a_count` = 1263 = `affine_solution_pairs` 合計、Σ`class_detail.L3_surjective` = 42 = 合計、Σ全 `sizeH` 多重度 = 1263。**lift の取りこぼしゼロ。**

⟹ 指紋照合が SM-2 を実質的に潰す。**本任務で回収した最大の価値はここ。**

## S3【F-2 記載漏れの重大度】— 前提 2 件が誤り、別の重大 1 件を発見

**前提訂正 (i)「cert 項目なし」は誤り。** `f_fixtures.F_2_1_sigma1sq_eq_x` / `F_2_2_sigma2sq_eq_y` として**記載あり**。文書は `F-2.1`、cert は `F_2_1_` — `F-2.1` で grep すると当たらない。**命名不統一であって記載漏れではない。**

**前提訂正 (ii)「Chk の fail-hard 性」は誤り。** `Chk`(55 行)は `FAILS` に append して Print し bool を**返すだけ**。全呼び出し側が戻り値を捨てている(`Chk(...);;`)。`Error()` なし。⟹ **fail-soft。錨が落ちても走行は止まらない。** 安全網は `fails_total`/`fails` の cert 出力(実測 `fails_total = 0`, `fails = []`)。

**【要修正】cert の boolean 7 個がハードコード literal**(Grep で現存確認・行番号つき):
```
560: "    \"size_Phat_eq_3000_times_V\":true,\n",
567: "  \"F_1_all_pass\":true,\n",
568: "  \"F_2_1_sigma1sq_eq_x\":true,\"F_2_2_sigma2sq_eq_y\":true,\n",
572: "  \"F_3_5_negative_fixture_pass\":true\n",
```
(加えて 561–562 の `piE_U0_eq_theta_and_piE_W0_eq_tau` / `order_Uhat0_times_What0_...`)。対照的に `F_2_5_pass` / `F_2_6_pass` は正しく `JB(f25_pass)` / `JB(f26_pass)` を出している。⟹ **前者 7 個は検査が落ちても `true` と書かれる = 証拠能力ゼロ。** 双子走の `wb_charming := true` と同一の反パターンの再発。

**【要修正】`fails_total = 0` に分母がない。** 失敗数は記録されるが**実行検査本数も名簿も記録されない**。cert 単独では「全錨が走って通った」と「錨ブロックが走らなかった」を区別できない。

**⟹ 重大度: 記載漏れとしては【軽微】(名前違いのみ)、記載の証拠能力としては【要修正】。【重大】ではない** — (a) 値は実際に真(`fails_total=0`、Chk は失敗時必ず append)、(b) stdout ログ現存(`scratchpad/v2_run_full.log` 他)。

### 【重大・新規】`shard_provenance.self_sha256` が全 3 shard で同一かつ誤り(現存)

| ファイル | cert 記載 | 実 sha256 | サイズ |
|---|---|---|---|
| `…_shardA.json` | `02e8ac0bfd30…` | `6c0409ab51a6…` | 25,997 B |
| `…_shardB.json` | `02e8ac0bfd30…` | `b70bc459ac7e…` | 32,421 B |
| `…_shardC.json` | `02e8ac0bfd30…` | `4059638c99ac…` | 8,810 B |

`02e8ac0b…` の正体は **driver スクリプト自身の sha256**(531 行 `selfSha := ComputeSha256File(<driver>)`)。これが各 shard の `path` の隣に `self_sha256` として 3 回書かれている。⟹ 値は本物だが**ラベルと配置が誤り**で、**shard ファイルの完全性はどこにも記録されていない**のに記録されているように読める。進行中の self-hash 修理束に合流させるべき。

## 総括

**S1 = 同一対象**(条件: α SM-1 の盲点を cert と裁定に明記し marking の担保先を分離、β `size_Phat_eq_3000_times_V` を実測値に差し替え)。

**「予言 vs 実測 17/17」の cross-checked 付与を支持する — ただし私が実施した指紋照合を証跡に含めることを条件とする。** 裁定 606 に届いた 17/17 は 2 スカラー/行のみで SM-2 を潰せていない。4 値・多重度つき・全 17 行の指紋を含めて初めて「同じ誤解の共有」経路が実質的に閉じる。

**支持しない**: L-3 が marking を検証したという読み(SM-1 により不可能)、`f_fixtures` のハードコード 7 項目を「検査済み」と数えること。

**修理項目(優先順)**: ① 照合器のキー整合を直し、**スキップ時に緑を返さず失敗する** fail-closed 化 ② `shard_provenance.self_sha256` を各 shard の実ハッシュへ ③ literal boolean 7 個を実測変数へ ④ cert に実行検査本数/名簿を追加し `fails_total` に分母を与える ⑤ `Chk` の fail-soft 性を cert に明記(または fail-hard 化)⑥ `F-2.1` と `F_2_1_` の命名統一。

参照: `C:\Users\81905\Desktop\shadow-atelier\docs\notes\theorem_check_mirrorall_l3vacuous_v1.md` / `...\search\probe\w6_bu_s1_s3\w6_bu_s35_driver_v2.g` / `...\search\certs\w6_bu_s35_v2_20260806.json`(+shardA/B/C) / `...\crosscheck\compare_l3_pred_vs_meas.py` / `...\search\certs\l3_pred_vs_meas_20260806.txt`。対象物は不改変・封印非接触。検算スクリプトは scratchpad 内。