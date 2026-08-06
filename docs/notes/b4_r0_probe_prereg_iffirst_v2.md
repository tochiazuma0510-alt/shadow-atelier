# B₄ 低指数窓 R0 probe — 事前登録票 **v2(方法変更版)**・IF-FIRST・**発火前**

**状態札: `prereg (pre-firing) / 走行ゼロ / GAP 未実行 / cert 未生成 / 封印非接触 / 発火は司令塔が別途`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔 **裁定 651**(v1 の方法 = `LINS(B₄, 240)` が標準 runner で **2 連 FAIL-CLOSED**(フラグ到達確認済みの早期死 = 環境起因濃厚)につき **STOP 確定**。方法を差し替えた v2 を起票せよ)
- **v1 との関係(重要)**: 本票は **v1 の自動移行ではない**。v1(`docs/notes/b4_r0_probe_prereg_iffirst_v1.md`)は **方法ごと STOP** で確定・**再発火しない**。本票は **標的だけを引き継いだ独立の登録**であり、登録集合・手順・依存・停止規則を**すべてここで新規に凍結**する。**v1 の §1.2(LINS 呼び出し)は本票では無効**。
- 入力正本(すべて既在):
  - `docs/notes/b4_mirror_transfer_design_v1.md` **v1.2 §13**(補題 TRI-ABEL・命題 NO-SMALL-NONAB・**系 INDEX-LB**)/ §4.3(層定義・記号衝突 W-1)
  - `docs/notes/b4_r0_probe_prereg_iffirst_v1.md`(**標的・予言・禁止語・停止規則の型紙**)
  - `docs/notes/b4_original_gtshadows_extraction_v1.md`(窓の定義 $\mathrm{NFI}_{PB_4}(B_4)$・**(A.2)** $x_{ij}$ の語)

> ## 非接触・規律の申告(本票作成時点)
> **機械ゼロ**(GAP 起動なし・SmallGroups 掃引なし・cert 生成なし)。封印 3 量非接触・$\mathrm{Im}\,R$/$d_N$ 非接触・B₃ 側 L3 層非接触。本票は**発火請求ではなく登録**である。

---

## 0. 一枚まとめ(7 行)

1. **標的は v1 と同一の 1 点**: $B_4$-指数 **192**($\lvert Q\rvert=\lvert PB_4/\widetilde N\rvert=8$)の**非可換窓**が存在するか。
2. **方法を差し替える**: 「$B_4$ 側から下降(LINS)」→ **「有限群側から上昇(SmallGroups(192) の掃引 + 全射の存在判定)」**。
3. **標的の射程は変わらない**(§2 で証明): 指数 $\le240$ で非可換窓がありうるのは $\lvert Q\rvert=8$ **のみ** ⟹ **指数 192 の判定は「指数 $\le240$ に非可換窓があるか」の完全な判定と等価**。
4. **窓条件は群の言葉に翻訳できる**: $\ker\psi\le PB_4\iff \psi(PB_4)\trianglelefteq G$ が指数 24 で $G/\psi(PB_4)\cong S_4$(§3.1)。
5. ★ **安価な必要条件(SG-AB)**: $\boxed{G^{\rm ab}\in\{C_2,C_4\}}$(§3.2 で証明)。10,494 群のほぼ全部をここで落とす。
6. **v1 に無かった長所**: 掃引は **shard 可能・再開可能**(LINS の all-or-nothing と違い、途中終了でも「未検群リスト付き PARTIAL」という**正直な UNKNOWN** が出せる)。依存も **SmallGroups ライブラリ + GQuotients の完全性**に替わる(LINS 悉皆性への依存が消える)。
7. **走らない**。凍結後に司令塔が発射(実装の担い手は臨機応変)。

---

## 1. 標的(v1 から逐語で引き継ぎ)

$$\boxed{\ \exists\,\widetilde N\in\mathrm{NFI}_{PB_4}(B_4):\quad [B_4:\widetilde N]=192\ \wedge\ Q:=PB_4/\widetilde N\ \text{が非可換}\ ?\ }$$

紙の根拠(設計 v1.2 §13・**再掲・本票では証明しない**): 補題 TRI-ABEL / 命題 NO-SMALL-NONAB / **系 INDEX-LB**(非可換窓 ⟹ $\lvert Q\rvert\ge8$ ⟹ 指数 $\ge192$)。

---

## 2. 射程の同値性(**方法変更が標的を狭めないことの証明**)

指数 $\le240$ の窓は $\lvert Q\rvert=[PB_4:\widetilde N]\le10$。

| $\lvert Q\rvert$ | 指数 | 非可換の可能性 | 理由 |
|---:|---:|---|---|
| 1–5 | $\le120$ | **なし** | 位数 $\le5$ の群は可換 |
| 6 | 144 | **なし** | $S_3$ は命題 NO-SMALL-NONAB で排除 |
| 7 | 168 | **なし** | 素数位数 ⟹ 巡回 |
| **8** | **192** | **あり**($D_4$ / $Q_8$) | ← **唯一の候補** |
| 9 | 216 | **なし** | 位数 $p^2$ ⟹ 可換 |
| 10 | 240 | **なし** | $D_5$ は命題 NO-SMALL-NONAB で排除 |

$$\Longrightarrow\ \boxed{\ \text{「指数 192 に非可換窓があるか」}\iff\text{「指数 }\le240\text{ に非可換窓があるか」}\ }$$
⟹ **v2 の標的は v1 と厳密に同一**(v1 の主判定と同値)。**失われるのは付随在庫だけ**(§5.3)。

---

## 3. 方法(scope ①)— 群側からの上昇

### 3.1 窓条件の群論的翻訳(**本票の設計の核**)

> ### 補題 R0-TRANS(candidate・本稿)
> $\psi:B_4\twoheadrightarrow G$、$\lvert G\rvert=192$ とする。$Q:=\psi(PB_4)$ と置くと
> $$\boxed{\ \ker\psi\ \text{が窓}\ (\ker\psi\le PB_4)\iff \lvert Q\rvert=8\iff G/Q\cong S_4\ \text{(かつ }Q\trianglelefteq G)\ }$$
> **証明.** $PB_4\trianglelefteq B_4$、$B_4/PB_4\cong S_4$ ⟹ $Q\trianglelefteq G$ は常に成立。$\ker\psi\le PB_4$ なら $G/Q\cong B_4/PB_4=S_4$ ⟹ $\lvert Q\rvert=192/24=8$。逆に $\lvert Q\rvert=8$ なら $[G:Q]=24=[B_4:PB_4]$ で $\psi^{-1}(Q)=PB_4\ker\psi=PB_4$ ⟹ $\ker\psi\le PB_4$。∎
> **⟹ 判定は「$\psi(PB_4)$ の位数を測る」だけ**($PB_4$ の 6 生成元 $x_{ij}$ は (A.2) の語で与える)。

### 3.2 ★ 安価な必要条件 **SG-AB**(掃引の主フィルタ)

> ### 補題 SG-AB(candidate・本稿)
> 上の状況で窓かつ $Q$ 非可換($\lvert Q\rvert=8$)なら
> $$\boxed{\ G^{\rm ab}\ \text{は巡回で}\ \lvert G^{\rm ab}\rvert\in\{2,4\}\ }$$
> **証明.** (i) $B_4^{\rm ab}=\mathbf Z$ ⟹ $G^{\rm ab}$ は巡回。(ii) $G/Q\cong S_4$ ⟹ $G^{\rm ab}/\mathrm{im}(Q)\cong S_4^{\rm ab}=C_2$ ⟹ $\lvert G^{\rm ab}\rvert=2\lvert\mathrm{im}(Q)\rvert$。(iii) $\mathrm{im}(Q)=Q[G,G]/[G,G]$ は $Q^{\rm ab}$ の商 ⟹ $Q\in\{D_4,Q_8\}$ より $Q^{\rm ab}\cong C_2\times C_2$ の商 ⟹ 位数 $\le4$;かつ巡回群 $G^{\rm ab}$ の部分群ゆえ**巡回** ⟹ $C_2\times C_2$ の巡回商は位数 $\le2$ ⟹ $\lvert\mathrm{im}(Q)\rvert\in\{1,2\}$。∎

**補助の必要条件(すべて安価・順に効く)**:
- **F2**: $\exists N\trianglelefteq G$, $\lvert N\rvert=8$, **$N$ 非可換**, $G/N\cong S_4$(= `IdGroup(G/N)=[24,12]`)。
- **F3**: $\psi(\Delta_4^2)\in Z(G)\cap Q$($\Delta_4^2\in Z(B_4)\cap PB_4$)⟹ **$Z(G)\cap N\ne1$ が必要**($D_4,Q_8$ の中心は $C_2$ ⟹ $Z(G)\supseteq$ その $C_2$ になりうるかの検査)。
- **F4**: $\psi(\sigma_1),\psi(\sigma_2),\psi(\sigma_3)$ は**互いに共役**で braid 関係を満たす(⟹ 同位数)。これは §3.3 の `GQuotients` が自動で担う。

### 3.3 手順(**凍結・この順序が仕様**)

> **P0(準備・サニティ)**: `B4fp := F/[braid×2, far-commute]`(§4.1 の表示を**バイト単位で**使用)。$x_{ij}$ 6 語を (A.2) で定義。`Index(B4fp, PB4sub) = 24` を機械で確認(落ちたら STOP)。
> **P1(SG-AB フィルタ)**: `for i in [1..NrSmallGroups(192)]`: `G:=SmallGroup(192,i)`;`A:=G/DerivedSubgroup(G)`;**`IsCyclic(A) and Size(A) in [2,4]`** で選別。**通過数を記録**。
> **P2(構造フィルタ)**: P1 通過群について `N in NormalSubgroups(G)` で `Size(N)=8 and not IsAbelian(N) and IdGroup(G/N)=[24,12]` を満たす $N$ の存在で選別(位数 192 の群はすべて可解 ⟹ `NormalSubgroups` は軽い)。**通過数と `IdGroup(N)`($D_4$/$Q_8$)の内訳を記録**。
> **P3(全射の存在判定)**: P2 通過群について `epis := GQuotients(B4fp, G)`(Aut(G) を法とした全射の完全リスト)。各 $\psi$ について $Q_\psi:=\langle\psi(x_{ij})\rangle$ を計算し **`Size(Q)=8 and not IsAbelian(Q)`** を判定。
> **P4(窓の確定)**: 該当 $\psi$ について $\widetilde N:=\ker\psi$、`Index(B4fp,Ñ)=192`・$\widetilde N\le PB_4$(= P3 の位数条件・補題 R0-TRANS)・`IdGroup(Q)`・`delta2_in_N`($\psi(\Delta_4^2)=1$ か)を記録。

### 3.4 記録欄(発火前に固定)

`smallgroup_id` / `Gab_invariants` / `passes_P1` / `passes_P2`(+ `N_idgroup`)/ `n_epis` / `Q_order` / `Q_idgroup` / `Q_is_abelian` / `delta2_in_N` / `sigma_orders`(3 生成元の位数・全て同一のはず)/ `Nt_index`。

### 3.5 コスト見積り(ローカル GAP・`gap.ps1 -o 2g` 第一候補)

| 段 | 対象数 | 見積り | 根拠 |
|---|---:|---|---|
| P0 | — | 数秒 | coset enumeration(既在 `stage1_pb4.g` の実績: $[B_4:PB_4]=24$ を確認済) |
| **P1** | 10,494 | **1–3 分** | `SmallGroup` 生成 + `DerivedSubgroup` のみ。SmallGroups(192) はライブラリ収録(1024 以外は 2000 まで完全) |
| **P2** | P1 通過(**予言: $\le$ 数百**) | **1–5 分** | 可解群の `NormalSubgroups` |
| **P3** | P2 通過(**予言: $\le$ 数十**) | **5–20 分** | `GQuotients` が主コスト。1 群あたり数秒〜数十秒 |
| 合計 | | **目安 30 分** | |

- **壁時計 cap = 40 分**(段別: P1 ≤ 10 分 / P2 ≤ 10 分 / P3 ≤ 20 分)。
- ★ **shard 可能**: P1/P2 は `i` の区間で分割でき、P3 は群ごとに独立。**cap 到達時は「未検群 ID のリスト付き PARTIAL」**で終える(§6 S-R0-8)。

---

## 4. 登録の詳細

### 4.1 底群と表示(**v1 §1.1 と同一・後から変えない**)

$$B_4=\langle\sigma_1,\sigma_2,\sigma_3\mid \sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2,\ \sigma_2\sigma_3\sigma_2=\sigma_3\sigma_2\sigma_3,\ \sigma_1\sigma_3=\sigma_3\sigma_1\rangle$$
GAP 生成元名 `a,b,c`($a=\sigma_1$)。⚠ **中心は `Delta4sq` と命名**($\Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4$)— リポジトリの `c₄` は `Chk6` の別条件、GAP 生成元 `c` は $\sigma_3$(設計 v1 §1.2 警告 W-1)。
$PB_4$ の生成元(A.2): $x_{12}=a^2,\ x_{23}=b^2,\ x_{34}=c^2,\ x_{13}=b a^2 b^{-1},\ x_{24}=c b^2 c^{-1},\ x_{14}=c b a^2 b^{-1} c^{-1}$。

### 4.2 依存(**v1 とは別物**・登録と同時に固定)

| # | 依存 | 破れたときの影響 |
|---|---|---|
| **D-v2-1** | **SmallGroups ライブラリの完全性**(位数 192 = 10,494 群) | 「非発見」の意味が消える。**存在の主張は無傷** |
| **D-v2-2** | **`GQuotients` の完全性**(Aut(G) を法とした全射の網羅) | 同上。⚠ **v1 の LINS 悉皆性依存(D-R0-1)は消滅** |
| **D-v2-3** | 補題 R0-TRANS(窓 ⟺ $\lvert\psi(PB_4)\rvert=8$)と補題 SG-AB(フィルタの必要性) | **フィルタが必要条件でなければ偽陰性**。⟹ §6 S-R0-9 に検査を置く |
| **D-v2-4** | $x_{ij}$ の語(A.2)の正しさ | $Q_\psi$ の位数が誤る ⟹ P0 のサニティで検出 |
| **D-v2-5** | 紙の補題(INDEX-LB / NO-SMALL-NONAB / 位数 $p^2$ 可換) | **§2 の射程同値性だけ**に効く。指数 192 の判定自体は無傷 |

---

## 5. 出力規則(**文言を発火前に固定**)

### 5.1 非発見のとき(**この文言以外を書かない**)

> 「位数 192 の全 10,494 群を掃引し、$B_4\twoheadrightarrow G$ かつ $\ker\psi\le PB_4$ かつ $PB_4/\ker\psi$ が非可換となる組は **存在しない**(SmallGroups ライブラリと `GQuotients` の完全性に条件つき)。」
> **許される追加の一文**(紙の補題を明示的に引く場合のみ): 「系 INDEX-LB・命題 NO-SMALL-NONAB・位数 $p^2$ 可換より、$B_4$-指数 $\le240$ の窓で非可換なものは**存在しない**。」

### 5.2 ★ 禁止語(書いたら `OVERCLAIM / STOP`)— v1 から逐語で引き継ぎ+追加

- 「**指数 1000 まで非可換窓は存在しない**」「$[PB_4:\widetilde N]\le41$ の窓はすべて可換」— **P-B4-1 は依然として予想**。本 probe は **240 までしか言えない**。
- 「鏡映双子はゼロ」「$\iota$-固定である」— 本 probe は **$\iota$ を計算しない**。
- 「GT-shadow / settled / isolated / genuine」— **述語を一切評価しない**。
- **【v2 追加】**「$B_4$ の指数 192 の**正規部分群を悉皆列挙した**」— **していない**。掃引したのは**商の側**(位数 192 の群)であり、$\ker\psi\le PB_4$ でない指数 192 の正規部分群(= 窓でないもの)は**見ていない**。
- **【v2 追加】**「$G^{\rm ab}\notin\{C_2,C_4\}$ の群には窓がない」を**フィルタの実行結果として**書くこと — それは**補題 SG-AB(紙)から従う**のであって測定結果ではない。出典を紙に帰す。

### 5.3 ★ v1 から**失われる情報**(明記義務)

v1(LINS)は指数 $\le240$ の窓を**全部**列挙するはずだった。v2 は**指数 192 の非可換窓だけ**を見る。ゆえに:
$$\boxed{\ \textbf{P-R0-2}(\lvert Q\rvert\ \text{の分布})\ \textbf{と}\ \textbf{P-R0-4}(\texttt{delta2\_in\_N}\ \text{の層の非空性})\ \textbf{は v2 では検定できない}\ }$$
⟹ 両予言は **v1 と共に凍結・未検定のまま保留**(取り下げではない)。v2 の結果からこの 2 件について何かを言うことを**禁止**する。

---

## 6. 停止規則(発火前に登録)

| # | trigger | verdict |
|---|---|---|
| **S-R0-1′** | `NrSmallGroups(192) ≠ 10494` | `LIBRARY_MISMATCH / STOP`(ライブラリ版差) |
| **S-R0-2′** | P0 のサニティ `Index(B4fp,PB4sub) = 24` が落ちる | `PRESENTATION_BROKEN / STOP` |
| **S-R0-3′** | 発見された非可換窓が設計 v1.2 §13.2 の (T1) 同位数 / (T2) 遠可換 / (T3) 三角の中心 のどれかに反する | `PAPER_CONFLICT / STOP`(**先に紙を疑う**) |
| **S-R0-4′** | 壁時計 40 分超過(または段別 cap 超過) | `TIME_CAP / PARTIAL`(§6 S-R0-8 の様式で終える。**`NOT_FOUND` とは書かない**) |
| **S-R0-5′** | 出力に §5.2 の禁止語 | `OVERCLAIM / STOP` |
| **S-R0-6′** | 本票に無い量($\iota$・双子・GT-shadow 述語・封印量)を計算した | `SCOPE_CREEP / STOP` |
| **S-R0-7′** | **フィルタで落とした群に窓があった**(下の抜き取り検査で判明) | `FILTER_UNSOUND / STOP`(補題 SG-AB を再検分) |
| **S-R0-8′** | P3 が cap 内に終わらない | `PARTIAL`:**未検群 ID の全リストを cert に載せる**。verdict は `UNKNOWN(partial)` |
| **S-R0-9′** | P1/P2 の通過数が 0 | `FILTER_TOO_STRONG / STOP`(必要条件の導出ミスを疑う。**通過 0 は「窓なし」の証拠にしてよいが、まず補題を疑う**) |

> ### ★ フィルタ健全性の抜き取り検査(**必須・S-R0-7′ の入力**)
> P1 で落ちた群から**無作為に 20 個**、P2 で落ちた群から**無作為に 20 個**を選び、`GQuotients(B4fp, G)` を直接走らせて **窓が出ないこと**を確認する(出たら S-R0-7′)。⟹ **補題 SG-AB / F2 の必要性を実測で担保**する安価な保険。

---

## 7. IF-FIRST 予言(**発火前に固定・反証可能**)

> - **P-R0-1′(主予言・v1 から継承)**: **指数 192 に非可換窓は無い**(`verdict = NOT_FOUND_AT_192`)。弱い予言であり、**外れたら良い知らせ**(紙で追えない構造が最小指数に居る)。
> - **P-R0-5(新・フィルタ効率)**: **P1 通過は 10,494 群中 $\le$ 300、P2 通過は $\le$ 30**。大きく外れたらフィルタの設計かライブラリの理解が誤っている。
> - **P-R0-6(新・型の内訳)**: P2 を通る $N$ の型は **$Q_8$ 側が優勢**($\mathrm{Aut}(Q_8)\cong S_4$ で $S_4$ 作用が自然に載る一方、$\mathrm{Out}(D_4)=C_2$ で $S_4$ の作用は符号を経由せざるを得ない)。
> - **P-R0-7(新・コスト)**: 総所要 **30 分以内**(cap 40 分に当たらない)。
> - **予言が外れたときの扱い**: P-R0-1′ が外れる(= 非可換窓発見)⟹ **STOP しない・大成功**として §7.1 へ。P-R0-5/6/7 が外れる ⟹ **STOP しない**が、cert に実測値を記録し、フィルタ設計の再検分を起票。

### 7.1 発見のとき(v1 §4.3 を逐語で引き継ぎ)

(a) `Q_idgroup` で $D_4$/$Q_8$ を同定、(b) 設計 v1.2 §13.2 の (T1)(T2)(T3) と矛盾しないか照合(矛盾 ⟹ S-R0-3′)、(c) **その窓 1 個についてのみ** $\iota$ 判定(語の生成元反転)を**別タスクとして**起票する(本票では実行しない)。

---

## 8. 出力 cert(schema・発火前に固定)

`search/certs/b4_r0_probe_v2_<date>.json`:
```
{ prereg_doc_sha256, prereg_version: "v2 (SmallGroups-192 sweep; supersedes-method-only of v1)",
  gap_version, smallgrp_version, nr_small_groups_192,
  base_group: "B4 = <a,b,c | aba=bab, bcb=cbc, ac=ca>",
  pb4_generators: ["a^2","b^2","c^2","b*a^2*b^-1","c*b^2*c^-1","c*b*a^2*b^-1*c^-1"],
  sanity: { index_B4_PB4: 24 },
  wall_cap_ms: 2400000, stage_caps_ms: {P1:600000, P2:600000, P3:1200000},
  p1_passed: [ids...], p2_passed: [{id, N_idgroup}...],
  p3: [ { smallgroup_id, n_epis, Q_order, Q_idgroup, Q_is_abelian, delta2_in_N, sigma_orders } ],
  filter_soundness_spotcheck: { p1_rejected_sampled: [...], p2_rejected_sampled: [...], all_clear: true },
  nonabelian_windows: [ ... ],              # 空でもよい(空であること自体が結果)
  untested_ids: [ ... ],                    # PARTIAL のときのみ非空
  verdict: "NONABELIAN_WINDOW_FOUND | NOT_FOUND_AT_192 | UNKNOWN(partial) | STOP(<reason>)",
  grade: "candidate / single-system / not cross-checked / not verified (no Lean)" }
```

---

## 9. 【GAP】・格・v1 との差分表

| # | 内容 |
|---|---|
| **【R0v2-GAP-1】** | **単一系統**(GAP のみ)⟹ **格は candidate 止まり**。非可換窓が**発見された場合のみ**第二系統(python で語→置換表現の再検査)を別タスクで起票 |
| **【R0v2-GAP-2】** | 「非発見」は **D-v2-1/2(ライブラリと `GQuotients` の完全性)に条件つき**。工房で独立検証していない |
| **【R0v2-GAP-3】** | **フィルタの必要性**(補題 SG-AB・F2)は紙で証明したが、実装の取り違え(例: `AbelianInvariants` の読み違い)は §6 の抜き取り検査でしか捕まらない |
| **【R0v2-GAP-4】** | P-B4-1(帯 1000 まで可換)の完全解決は**依然として射程外** |

### 9.1 v1 → v2 の差分(**自動移行ではないことの明示**)

| 項目 | v1(STOP 確定) | **v2(本票)** |
|---|---|---|
| 方法 | `LINS(B₄, 240)`・単一呼び出し | **SmallGroups(192) 掃引 + `GQuotients`** |
| 走査の向き | $B_4$ から下降(部分群側) | **有限群から上昇(商側)** |
| 実測範囲 | 指数 $\le240$ の全正規部分群 | **指数 192 の窓のみ** |
| 標的 | 非可換窓の存在 | **同一**(§2 で射程同値) |
| 主依存 | LINS 悉皆性 | **SmallGroups + GQuotients の完全性** |
| 失敗様式 | all-or-nothing(実際に 2 連 FAIL-CLOSED) | **shard 可能・PARTIAL を出せる** |
| 付随在庫 | $\lvert Q\rvert$ 分布・`delta2_in_N` 層 | **取れない**(P-R0-2/4 は保留・§5.3) |
| 壁時計 cap | 15 分 | **40 分**(段別 10/10/20) |
| 予言 | P-R0-1〜4 | **P-R0-1′ を継承・P-R0-2/4 は保留・P-R0-5/6/7 を新規** |

**格の宣言**: 本 probe の出力は **candidate / single-system / not cross-checked / not verified (no Lean)**。**GT-shadow の述語には一切触れない**ので `isolated` / `settled` / `genuine` を出力に書いてはならない。**R1 以降(指数 480/720/1000)へは自動で進まない** — 進むなら本票の versioned 後継(v3)で再登録する。
