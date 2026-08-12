# 【P8-CORR】$a_9$ ↔ $u_0$(wac_v1)の対応判定・BRIDGE-IN の所在・prereg 儀式案

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 941
**格**: candidate(紙・単系統・**Sol 未監査**)。
⚠ **ord の値は計算していない**(委嘱の禁止事項を遵守)。素因子台の観察は**対応判定に必要な範囲**に限り、**的中判定には一切用いていない**。

> ## ★★★ 判定(三値)
> $$\boxed{\ \textbf{別対象}\ }$$
> wac_v1 の $u_0$ は **$N_{S4}$ 窓(monodromy $=PSL(2,8)=$ 9T27)**の測定であり、私の $a_9$ は **$K^{(9)}$(dihedral 窓)**の量である。**窓・法・規約の三点すべてが異なる。**
> ⟹ **$u_0$ を $a_9$ の receipt に流用することはできない**。正しい receipt = **P8-value 線**(§3)。

---

## §1 第四の $u$ を加えた全数照合(NAME-COLLIDE の拡張)

`k9_p1_recon_v2.md` §2 で摘出した三重衝突に、**第四の対象 $u_0$** が加わる。

| # | 記号 | 窓 / 対象 | 法 | 基礎体 | 型 | 出所 |
|---|---|---|---|---|---|---|
| 1 | **私の $a$**(K9-KUMMER) | $K^{(9)}$ の $\rho_{9,\mathrm{Aff}}$ の translation コサイクルの Kummer 類 | $9$ | $\mathbf Q$ | (4) kernel field 側 | `r1_k9_bridge_v1.md` |
| 2 | **$a_9=[u_9^{-1}]_{18}$**(E1 §5.1) | ★ **$K^{(9)}$**(dihedral)。$M=2n=18$ | **18** | $F_9=\mathbf Q(\zeta_{36})$ | 窓の局所 Kummer torsor 類 | `E1_gt_odd_dih_canonical_v1.md` |
| 3 | **u9bit の $u_9$** | $L_9$ 内の次数 9 Kummer 層 | $9$ | $\mathbf Q$ | 算術側・⚠ **$d_9=9$ を暗黙前件** | `u9bit_spec_v1.md` §1.2 |
| 4 | **FAM-U の $u_n$** | 窓の局所 Kummer torsor 類(族) | $2n$ | $F_n$ | (1) marked target 側 | `fam_u_assembly_v1.md` |
| ★ **5** | ★ **$u_0$(wac_v1)** | ★ **$N_{S4}$ 窓** — monodromy $PSL(2,8)=$ **9T27**・cover $C\to\mathbf P^1_t$ **degree 9 / genus 2**・分岐型 $(3^3,3^3,9)$ | ★ **9**(cert の `ord([u^{-1}]_9)` 表記) | $\mathbf Q$(`field_of_definition = Q (Prop U-Q)`) | 窓の局所 Kummer 類 | `search/certs/u_meas_uloc_v2_20260731.json` |

**$u_0$ の値**(cert 逐語・**司令塔の伝達と一致することを検算**): `measurement.u_0_inverse = -1423828125/256`。
$3^6=729$、$5^9=1953125$、$729\times1953125=1423828125$、$2^8=256$ ⟹ $u_0^{-1}=-3^6\cdot5^9/2^8$ ✔ **一致**。
(`squarefree_part_of_u_0_inverse = -5`・`model.curve = y^2=(x^3-x/5)^2-512/421875`・`u_touched = True`。)

---

## §2 判定の根拠(**三点すべて不一致**)

| 比較軸 | $a_9$(E1・私の標的) | $u_0$(wac_v1) | 判定 |
|---|---|---|---|
| **(A) 窓** | $K^{(9)}$ — dihedral poset の対象。$PB_3/K^{(9)}=G_9$、$\lvert G_9\rvert=4\cdot9^3=2916$ | ★ **$N_{S4}$** — $PB_3/N_{S4}\cong PSL(2,8)$、位数 **504**。cert の `monodromy = PSL(2,8) = 9T27` | ✘ **別窓** |
| **(B) 法** | $M=2n=\mathbf{18}$(E1 §5.1 の $a_n:=[u_n^{-1}]_M$) | ★ **9**(cert `preregistration` の `ord([u^{-1}]_9)`) | ✘ **別法** |
| **(C) 基礎体** | $F_9=\mathbf Q(\zeta_{2M})=\mathbf Q(\zeta_{36})$ | $\mathbf Q$(`field_of_definition = Q`) | ✘ **別体** |

### 2.1 ★ 構造的な理由(**規約がそもそも適用外**)

E1 §5.1 の標準機械 (S1)–(S4) と $a_n:=[u_n^{-1}]_{2n}$ の規約は、**$K^{(n)}$(dihedral)専用**である:
- (S1) は $1\to\mathfrak F_0(\cong C_n)\to T\to(\mathbf Z/4n)^\times\to1$ を使う ⟹ **$\mathfrak F_0$ が巡回であること**が前提。
- $N_{S4}$ は $PB_3/N_{S4}\cong PSL(2,8)$(**非可換単純**)で、dihedral poset の対象ではない。
$$\boxed{\ \Longrightarrow\ E1\ \textbf{の }a_n\ \textbf{規約は }N_{S4}\ \textbf{窓には}\textbf{そもそも適用できない}\ }$$

### 2.2 ★ 傍証(**判定の確認のみ**・的中判定には使わない)

$u_0^{-1}=-3^6\cdot5^9/2^8$ の素因子台は $\{2,3,5\}$。⚠ 私の **P-K9U-1**($L_{9,\mathrm{Aff}}=\mathbf Q(\zeta_9,\sqrt[9]3)$・3 の外で不分岐)は台 $\{3\}$ を予言する。
$$\boxed{\ \textbf{台が食い違うこと自体が「別対象」判定と}\textbf{整合}\ }$$
⚠⚠ **これを P-K9U-1 の不的中と読んではならない** — **別対象なのでそもそも判定にならない**。cert 自身も `preregistration.d_no_interpretation` で「**no verdict on `ord([u^{-1}]_9)`, on surjectivity, or against any prediction**」と明記している。**本ノートもその規律を継承する。**

### 2.3 ⚠ ただし $u_0$ は**無価値ではない**

$N_{S4}$ は **972 屋根 $M=K^{(9)}\cap N_{S4}$ の第二成分**である。⟹ $u_0$ は **$N_{S4}$ 側の receipt** として意味を持ちうる(【ENT-GAP-7】S4-RAM-SUPPORT 系)。⚠ ただし **$N_{S4}$ の isolated が閉じるまで $\rho_{S4}$ 自体が未定義**(B118-1)なので、**現時点では算術像への橋がない**。

---

## §3 ★ 正しい receipt = **P8-value 線**(必要作業と見積り)

### 3.1 測るべきもの

$$\boxed{\ \textbf{$K^{(9)}$ 窓($H_9^{\rm fun}$)の局所 Kummer データ }u_9\in F_9^\times=\mathbf Q(\zeta_{36})^\times,\ \textbf{そして }a_9=[u_9^{-1}]_{18}\ }$$

### 3.2 工程(t63 §2 の設定に厳密に沿う)

| 段 | 内容 | 依拠 | 担当 |
|---|---|---|---|
| **R-1** | $H_9^{\rm fun}$ 窓の**幾何モデル $W_9$** を構成($\lambda_9:W_9\to\mathbf P^1$) | HF-1/HF-2・(TB1) | Model-Builder(実装係) |
| **R-2** | cusp $P_0^{(9)}$ の**有理 uniformizer $s_9$** を取る($\lambda_9^{-1}(0)=\{P_0^{(9)}\}$・全分岐 $e=18$) | t63 §2.1・A6 | 同 |
| **R-3** | 局所展開 $\lambda_9=u_9\,s_9^{18}(1+O(s_9))$ の**主係数 $u_9$** を厳密に抽出 | BFC 補題 B-5(ii-loc)・A7 | 同 |
| **R-4** | $c_9,\ell_9$ から **(7.1)** で `b_value_9` を算出 ⟹ **P8-value / 凍結 2 の commitment** | `i8_bridge_n9_v3.md` §3.2 P8 | 同 |
| **R-5** | $a_9=[u_9^{-1}]_{18}\in F_9^\times/F_9^{\times18}$ の**位数**を計算 | E1 §5.1 | 同 |
| **R-6** | **的中判定**(★ **§5 の prereg カード凍結後にのみ実行**) | 本ノート §5 | 司令塔 |

### 3.3 見積り(**candidate・私の見立て**)

- wac_v1 の $u_0$ 測定は、degree 9 / genus 2 の cover を**厳密に解いて**($y^2=(x^3-x/5)^2-512/421875$)主係数を出した実績がある(裁定 268–272・1 サイクル規模)。
- $K^{(9)}$ 側は $\lvert G_9\rvert=2916$ で $\lvert PSL(2,8)\rvert=504$ の **約 5.8 倍**。分岐型も $M=18$ で全分岐。
$$\boxed{\ \textbf{見積り} = \textbf{wac_v1 と}\textbf{同規模〜数倍}\ \textbf{(「秒〜分」ではない)}\ }$$
⚠★ **司令塔の「receipt = 埋め込み+ord 計算(秒〜分)」という見積りは、$u_0$ が流用できる場合のもの**である。**別対象と判定された以上、$K^{(9)}$ 窓の $u_9$ を新規に測る必要があり、工数は 1 サイクル規模に戻る。**
★ **朗報**: wac_v1 が**手法(厳密モデル → cusp 展開 → 主係数)を確立済み**なので、**設計は流用でき、対象を差し替えるだけ**である。

---

## §4 「凍結 2 / BRIDGE-IN bundle」の一次定義の所在(委嘱 2)

**特定できた**。

| 項目 | 内容 | 所在(逐語) |
|---|---|---|
| **札の名** | **P8**(§3.2 表)/ **P8-value**(§4 表) | `docs/notes/i8_bridge_n9_v3.md` |
| **中身** | 「**`b_value_9` の value commitment(凍結 2 / BRIDGE-IN)**| Model-Builder が $c_9,\ \ell_9$ から **(7.1)** で計算 | **未着手(窓 campaign 待ち)**」 | 同 §3.2 表 P8 行 |
| **凍結対象** | 「`b_value_9` / `b_value_source` | **$n=9$ 窓の凍結 2 / BRIDGE-IN bundle**(Model-Builder が $c_9,\ell_9$ から算出)」 | 同 §4 表 P8-value 行 |
| ★ **順序要件** | 「条文案 A (F2)「actual 値は個別モデル依存」。★ **(F3) の順序要件($u$ 開示・$G_K$ 観測より前)**も窓ごと」 | 同 §4 表 P8-value 行 |
| **位置づけ** | 「窓固有凍結 = **P4・P6・P7・P8-value の 4 件**。… 4 件はいずれも**手続き**(object identity の凍結と value commitment)であり、**数学の未決は残っていない**」 | 同 §4 末尾 |

> ### ★★ 最重要の発見 —(F3)の順序要件が **prereg の正典的根拠**である
> $$\boxed{\ \textbf{`b_value_9` の commitment は }\mathbf{u\ \textbf{の開示より前}}\ \textbf{に行わねばならない((F3))}\ }$$
> ⟹ **§5 の prereg カードは「儀式」ではなく、i8_bridge の (F3) を履行する手続きそのもの**である。⟹ **儀式なしに測ると P8-value が無効になる。**

⚠ **(7.1) の一次定義**($c_9,\ell_9\mapsto$ `b_value_9` の式)は `i8_bridge_n9_v3.md` の**参照先**であり、**本ノートでは所在未特定**(BFC v2.15 §7 と推定・**UNKNOWN**)⟹ ★ **R-4 着手前に確定が要る**【P8-GAP-1】。

---

## §5 ★ prereg 儀式カードの案文(委嘱 3)

**先例**: t63 の凍結予言(`82ca6b7`)/ ★ **`u_meas_uloc_v2` cert の `preregistration` ブロック**(工房に実績のある様式 — `frozen_before_measurement=true`・`d_no_interpretation`)。

```
=== PREREG CARD: P8-VALUE / a_9 RECEIPT (案) ===
card_id            : prereg-a9-receipt/v1
frozen_at          : <commit hash>            # 測定スクリプト実行「前」に commit
authorisation      : 司令塔裁定 <番号>
supersedes         : なし

[1] 測定対象(型を先に固定)
  window           : K^(9)  (dihedral poset・PB_3/K^(9) = G_9, |G_9| = 2916)
  object           : a_9 := [u_9^{-1}]_M  ∈ F_9^× / F_9^{×M}
  M                : 18   (= 2n, n = 9)
  F_9              : Q(zeta_36)
  ⚠ NOT            : u_0 (wac_v1・N_S4 窓・PSL(2,8)・法 9・体 Q) — 別対象(P8-CORR §2)

[2] 判定基準(★ 計算前に凍結する)
  的中   (HIT)     : ord(a_9) = 9
  不的中 (MISS)    : ord(a_9) ∈ {1, 3}
  UNKNOWN          : 次のいずれか —
                     (u1) モデル構成が R-1〜R-3 のいずれかで停止
                     (u2) u_9 が F_9 上で厳密に決まらない(近似のみ)
                     (u3) 窓が H_9^fun でないと判明(C1 相当の窓取り違え)
                     (u4) 法・体の規約が E1 §5.1 と食い違う
  ⚠ 部分情報       : pr_{18→6}(a_9) のみ得られた場合は HIT/MISS を宣告せず
                     「部分一致(位数 3 の射影を確認)」と記録する

[3] 同時に判定される予言(★ 事前に全部列挙する)
  P-K9U-1          : L_{9,Aff} = Q(zeta_9, 3^{1/9})
                     → a_9 の台が {3} に限ることと同値(UNRAM v2 §3.2)
  T63-P1 / W3-24   : ord(a_9) = 9(紙上確定・framework-conditional)
  K9-COMPOSE       : d_9 = ord(a_9)(RECON v2.1)⟹ d_9 = 9 = Conj 5.1@n=9
  ⚠ これらは「同じ 1 つの測定」で同時に判定される — 事後の選り好み禁止

[4] 禁止事項(measurement hygiene)
  - 測定前に ord を計算しない(本カード凍結までは値に触れない)
  - 測定後に判定基準を書き換えない
  - 部分結果で HIT を宣告しない
  - u_0(wac_v1)の値を a_9 の判定に流用しない  ★ P8-CORR の帰結
  - 結果の格は cross-checked 止まり(独立照合器が一致した場合)
    verified は Lean に予約

[5] 出力(cert に必ず載せる)
  u_touched                 : true/false
  frozen_before_measurement : true
  d_no_interpretation       : "machine values only; verdict は司令塔"
  window_assert             : H_9^fun であることの機械確認
  M_assert / F_assert       : M = 18, F_9 = Q(zeta_36) の機械確認
  b_value_9 / b_value_source: (7.1) による値と出所  ★ (F3) 順序要件の履行証跡
=== END ===
```

> ### ★ カード設計の 3 原則(私の起草意図)
> 1. **型を先に固定**([1] で窓・法・体を書く)— 本 P8-CORR で $u_0$ との取り違えが実際に起きかけたため。
> 2. **UNKNOWN を一級で用意**([2] の (u1)–(u4))— **測れなかったことを MISS と混同しない**。
> 3. **同時判定される予言を全部先に列挙**([3])— **事後の選り好み**(1 つの測定から都合のよい予言だけ拾う)を封じる。

---

## §6 【GAP】と次の一手

| # | 内容 | 重さ |
|---|---|---|
| ★ **【P8-GAP-1】** | **(7.1)** の一次定義($c_9,\ell_9\mapsto$ `b_value_9`)の所在。BFC v2.15 §7 と推定だが **UNKNOWN** ⟹ **R-4 着手前に確定が要る** | ★ 中 |
| **【P8-GAP-2】** | $H_9^{\rm fun}$ 窓の幾何モデル $W_9$ が**未構成**(i8_bridge が「窓 campaign 待ち」と記す当のもの) | ★★ 大(**receipt の本体**) |
| — | $u_0$ の $N_{S4}$ 側での活用 | ⚠ $\rho_{S4}$ 未定義(B118-1)ゆえ **ISO-S4 の後** |

### 推薦
1. ★ **prereg カード([5] の出力仕様込み)を先に凍結**する — **(F3) の順序要件がそれを要求している**(§4)。
2. **【P8-GAP-1】の (7.1) 所在確定**を実装係へ(小・文書 grep)。
3. **R-1〜R-3(モデル構成)** は wac_v1 の**手法を流用**して設計を書き、実装係へ。⚠ 見積りは **1 サイクル規模**(「秒〜分」ではない)。

---

## §7 帰属・依存申告

- **$u_0$ の測定** = wac_v1 campaign(2026-07-31・裁定 268–272・実装係)。**cert 値の伝達と棚卸し** = 司令塔(裁定 941)。
- **本ノートの新規部分**: ① **三値判定 = 別対象**(窓・法・体の三点不一致 + E1 規約の適用外性)② **第四の $u$ を加えた NAME-COLLIDE 全数表** ③ **$u_0^{-1}=-3^6\cdot5^9/2^8$ の検算**(司令塔の伝達と cert 値の一致確認)④ **正しい receipt = P8-value 線の工程 R-1〜R-6 と見積り訂正**(「秒〜分」→ **1 サイクル規模**)⑤ **「凍結 2/BRIDGE-IN」= P8-value の所在特定**と ★ **(F3) 順序要件が prereg の正典的根拠**であることの発見 ⑥ **prereg カード案文**(型先出し・UNKNOWN 一級・同時判定予言の全列挙)。
- **検算**: $3^6\cdot5^9/2^8$ の一致確認のみ(整数演算)。⚠ **$\operatorname{ord}$ は計算していない**。
- **未実施**: (7.1) の所在確定・$W_9$ の構成・**Sol 未監査**。⟹ **verified ではない**。


---

# 【v1.1 追記】prereg カード v2 — falsifier 前哨の修正一式(裁定 957)

**日付**: 2026-08-12 / **委嘱**: 裁定 957(falsifier 前哨 B-1 blocker + S-1〜S-4 + N-1)
**方式**: **additive addendum**(本文 §1–§7 は不改変)/ ★ **積荷同期: 便発送済みにつき通常 commit 通知**
**位置**: 本ノート §5 の prereg カード案を **v2 へ差し替える**(§5 の v1 案は履歴として残す)。

> ## ★ 修正の要点
> **B-1(blocker)= MISS 側の非対称の穴**を塞いだ。原則 3(同時判定される予言を全部先に列挙)は **HIT 側だけを守っていて MISS 側の「どれを先に疑うか」を凍結していなかった** — falsifier の指摘は正しい。

---

## A. prereg カード **v2**(★ これが正本)

```
=== PREREG CARD: P8-VALUE / a_9 RECEIPT (v2) ===
card_id            : prereg-a9-receipt/v2
supersedes         : prereg-a9-receipt/v1 (p8_corr_v1.md §5)
frozen_at          : <commit hash>            # 測定スクリプト実行「前」に commit
authorisation      : 司令塔裁定 <番号>

[0] 前件(prerequisites)  ★ S-1 で新設
  (7.1) の所在      : 確定済(裁定 943)
                      = docs/week4-K5_Rule1_v1_5.md L719
                        c_i ℓ_i c_i^{-1} = τ_i(ζ_10^{b_i})   [K^(5) 実例]
                      L791-792 の F1/F2 が i8_bridge P8-value 行と文言一致
  ⚠ NAME-COLLIDE   : 「BFC §7 の (7.1)」は同ラベル別式(式番号衝突)
                      ⟹ 引用時は必ずファイル名+行番号で指す
  ⚠ 残余(未判定)  : ★ n=9 特化の形。K^(5) は M=10・ζ_10 だが
                      n=9 では M=18 ⟹ ζ_18^{b_9} の形になるはず。
                      b_9 ∈ Z/18 のどの部分集合を走るか(単数か否か)は
                      ★ 数学者の宿題(本カード凍結の前件ではない
                        — R-4 着手の前件)

[1] 測定対象(型を先に固定)
  window           : K^(9)  (dihedral・PB_3/K^(9) = G_9, |G_9| = 2916)
  object           : a_9 := [u_9^{-1}]_M  ∈ F_9^× / F_9^{×M}
  M                : 18   (= 2n, n = 9)
  F_9              : Q(zeta_36)
  ⚠ NOT            : u_0 (wac_v1・N_S4 窓・PSL(2,8)・法 9・体 Q) — 別対象
  ⚠ NOT            : 「g:4→2 の商曲線」(litgate 覚書 = S4 窓・不分岐巡回 3 次)

[2] 判定基準(★ 計算前に凍結・★ MISS 側の再開順序まで凍結)
  的中   (HIT)     : ord(a_9) = 9
  不的中 (MISS)    : ord(a_9) ∈ {1, 3}
    ★ B-1: MISS のときの帰結(Sol F3(f) 逐語の転記)
      「値 9 は紙上鎖の独立支持であって証明の代用ではなく、9 以外なら
        紙上鎖・比較・measurement の少なくとも一つを fail-closed で再開する」
    ★ 再開順序(★ 測定前に凍結する — 事後の選り好み防止):
      第 1 に疑う : measurement (R-1〜R-6)
        理由 = 唯一の新規実装であり、他二者は Sol 監査を経ている
        具体 = モデルの厳密性 / cusp 同定 / uniformizer / 主係数抽出
      第 2 に疑う : 比較 (RECON: d_9 = ord(a_9))
        理由 = framework-conditional(M119-5)で (5′)・MATCH-one/
               BRIDGE-one・named framework を継承しており、
               前件のどれかが n=9 で破れうる
      第 3 に疑う : 紙上鎖 (T63-P1 / K9-COMPOSE)
        理由 = W3-24 は Sol 便 76 F3.2 検分済で最も硬い。
               ただし K9-COMPOSE は現在 HOLD(M119-6)なので、
               TOWER-α-INV の修理形が誤っていた可能性は残る
      ⚠ この順序は測定結果を見てから入れ替えない
  UNKNOWN          : ★ N-1: UNKNOWN は MISS に優先する
                     (下記いずれかに該当したら MISS を宣告しない)
                     (u1) モデル構成が R-1〜R-3 のいずれかで停止
                     (u2) u_9 が F_9 上で厳密に決まらない(近似のみ)
                     (u3) 窓が H_9^fun でないと判明(C1 相当の窓取り違え)
                     (u4) 法・体の規約が E1 §5.1 と食い違う
                     (u5) ★ S-4: ord(a_9) ∉ {1,3,9}
                          ⟹ K9-FULLPRE(A_9 は d_9 一つで決まる)の破れ
                          ⟹ MISS ではなく UNKNOWN。座標系の再検査へ
  ⚠ 部分情報       : pr_{18→6}(a_9) のみ得られた場合は HIT/MISS を宣告せず
                     「部分一致(位数 3 の射影を確認)」と記録する

[3] 同時に判定される予言(★ 事前に全部列挙する)
  P-K9U-1          : L_{9,Aff} = Q(zeta_9, 3^{1/9})
    ★ S-2: 残前件は「framework 層のみ」ではなく
            ① 修理済み K9-COMPOSE(fixed-window comparison を含む)
            ② K9-UNRAM
            の二系統(Sol 便 119 F3(f))
  T63-P1 / W3-24   : ord(a_9) = 9(紙上確定・framework-conditional)
  K9-COMPOSE       : d_9 = ord(a_9) ⟹ d_9 = 9 = Conj 5.1@n=9
                     ⚠ 現在 HOLD(TOWER-α-INV 撤回・M119-6)
  ★ S-3 追加
  TOWER-α-INV      : 測定値が uniformizer / marking の選択に依存したら falsify
                     依拠 = (T) の不変性(t63 §2.2・gap2_audit §3.2 で
                     両側機械検算済)。⟹ R-2(d) の 2 通りの s_9 で
                     ord(a_9) が変わったら TOWER-α-INV 系は誤り
                     ⚠ w 自体は不変でない(W-45)— 不変なのは (T) と類の等式
  ⚠ これらは「同じ 1 つの測定」で同時に判定される — 事後の選り好み禁止

[4] 禁止事項(measurement hygiene)
  - 測定前に ord を計算しない(本カード凍結までは値に触れない)
  - 測定後に判定基準・再開順序を書き換えない        ★ B-1 で追加
  - 部分結果で HIT を宣告しない
  - UNKNOWN 条項に該当するのに MISS を宣告しない    ★ N-1
  - u_0(wac_v1)の値を a_9 の判定に流用しない
  - 「g:4→2」など他窓の幾何量を a_9 の判定に流用しない  ★ 型境界 4 度目の教訓
  - 結果の格は cross-checked 止まり(独立照合器が一致した場合)
    verified は Lean に予約

[5] 出力(cert に必ず載せる)
  u_touched                 : true/false
  frozen_before_measurement : true
  d_no_interpretation       : "machine values only; verdict は司令塔"
  window_assert             : H_9^fun であることの機械確認
  M_assert / F_assert       : M = 18, F_9 = Q(zeta_36) の機械確認
  b_value_9 / b_value_source: (7.1) による値と出所  ★ (F3) 順序要件の履行証跡
  s9_variants               : ★ S-3: 2 通りの uniformizer での結果(両方記録)
=== END ===
```

---

## B. ★ 修正の反映一覧(裁定 957 の 6 項)

| # | 指摘 | 反映箇所 | 私の受諾 |
|---|---|---|---|
| **B-1** | MISS 側の**再開順序**が未凍結(原則 3 の非対称の穴) | ★ **[2] MISS 欄に Sol F3(f) 逐語 + 再開順序 3 段** | ★ **全面受諾**。原則 3 は「同時判定の列挙」で **HIT 側だけを守っていた** — **MISS のとき何を先に疑うかを凍結しなければ、事後に都合のよい犯人を選べてしまう**。falsifier の指摘は正しい |
| **S-1** | (7.1) 所在は裁定 943 で解消済 | ★ **[0] prerequisites 欄を新設**(ファイル名+行番号で pin・NAME-COLLIDE 警告つき) | 受諾。⚠ **私の §6【P8-GAP-1】は解消**(本追記で閉じる) |
| **S-2** | P-K9U-1 の残前件 = 二系統 | [3] の P-K9U-1 行 | 受諾 |
| **S-3** | TOWER-α-INV を同時判定命題へ | [3] + [5] の `s9_variants` | ★ **受諾**。しかも**測定が TOWER 系の反証機会にもなる**という設計は良い |
| **S-4** | $\operatorname{ord}\notin\{1,3,9\}$ は UNKNOWN | [2] の (u5) | 受諾(K9-FULLPRE の破れ ⟹ 座標系の再検査) |
| **N-1** | UNKNOWN は MISS に優先 | [2] 冒頭 + [4] | 受諾 |

---

## C. ★ 残余(**私の宿題**)— (7.1) の $n=9$ 特化

$K^{(5)}$ 実例(L719)は
$$c_i\,\ell_i\,c_i^{-1}=\tau_i\bigl(\zeta_{10}^{\,b_i}\bigr),\qquad 10=2\cdot5=M\ (n=5).$$
⟹ $n=9$ では $M=2\cdot9=18$ ゆえ $\zeta_{18}^{\,b_9}$ の形になるはず。

| 問い | 状態 |
|---|---|
| $b_9$ が走る集合($\mathbf Z/18$ 全体か・$(\mathbf Z/18)^\times$ か・別の部分集合か) | ✘ **未判定**(★ **私の宿題**) |
| $b_9$ と $a_9$ の関係(P8-value が $\operatorname{ord}(a_9)$ をどう拘束するか) | ✘ **未判定** |

$$\boxed{\ \textbf{⟹ カード凍結の前件では}\textbf{ない}\ \textbf{(凍結は今すぐ可)。}\textbf{R-4 着手の前件}\ \textbf{である}\ }$$
⚠ **この区別は重要**: (F3) の順序要件が要求するのは「**$u$ 開示より前に commitment を置く**」ことであって、「commitment の式を完全に理解してから凍結する」ことではない。⟹ **B-1 が塞がった今、凍結は執行可能**。

---

## D. 帰属

- **前哨監査**(B-1 blocker + S-1〜S-4 + N-1)= **falsifier**。**(7.1) の所在確定** = 裁定 943(実装係の grep)。**委嘱** = 司令塔(裁定 957)。
- **本追記の新規部分**: ① **MISS 側の再開順序 3 段の起草**(measurement → 比較 → 紙上鎖・各段に理由)② **prerequisites 欄の設計**(式番号 NAME-COLLIDE 警告つき)③ **(u5) の位置づけ**(K9-FULLPRE の破れ = 座標系の再検査)④ **$n=9$ 特化の残余を「凍結の前件ではなく R-4 の前件」と分離**。
- **申告**: ⚠ **$\operatorname{ord}$ は計算していない**。走行ゼロ。**Sol 未監査**。
