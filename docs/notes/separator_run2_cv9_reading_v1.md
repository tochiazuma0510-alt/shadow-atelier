# grade-two physical-state Separator run 2 CV-9 判読(falsifier 逐語・裁定 2060 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 4c762deb17dbdfbe)を逐語転記(2026-09-04)。

**工房裁定(2060)**: CV-9 = **同一対象**(限定 3 条)。工房格 = **checker PASS(Separator・S₀ rank 1,354・λ(S₀)=0・λ(ρ₂)=1・free coordinate 1417・target reductions 884)・cross-checked は限定つき** — (i) λ の直交検査は還元後 1,354 行のみで原本 Conn 行への直接検査がない (ii) 両実装は同一コミット・同一著者で F₃ 演算核が逐語クローン(核は falsifier が素朴実装で全数照合済み・retire)(iii)「lower が消える」性質は v11 親からの継承(裁定 2048 の射程)。射程 = **ρ₂ ∉ S₀ = span(Conn) のみ**で GRADE2 NONMEMBER ではない。verified=false(Lean 未)。

---

# CV-9 仕様同一性判読 — R07 grade-two physical state / canonical Separator v2

判読者: falsifier(反証前哨・非当事者)
対象: GHA run 33891714539(success)/ commit 7b7b9de2
日付: 2026-09-05
先例: physical connection v11 判読(`docs/notes/physconn_v11_cv9_reading_v1.md`・裁定 2048)

---

## 0. 裁定

**同一対象(SAME OBJECT)。**

producer と checker は「v11 connection artifact のうち lower が消えた 1,354 offer の top 行を
挿入順 echelon に入れて得られる S₀ に対する、ρ₂ v17 の canonical separator(v536 補題 2.1)」を
計算している。選択規則・還元順序・正規化・自由座標規則・separator 構成のすべてが同一で、
かつ両者は互いの親 manifest ハッシュを相互に束縛している。別対象・判定不能の余地は見つからなかった。

ただし **cross-checked の射程には 3 つの限定**が付く(§3)。

---

## 1. 同一対象と判定した根拠(すべて確認済み・file:line)

| # | 規約 | producer | checker | 一致 |
|---|---|---|---|---|
| 1 | 行の選択規則(`kind != "connection"` を skip = 独立 6,705 行を捨て従属 1,354 行を使う) | `search/d972_r07_grade2_physical_state_separator_v2.py:833` | `search/check_d972_r07_grade2_physical_state_separator_v2.py:403` | 同文 |
| 2 | 還元順序(挿入順 sweep・数値的に小さい自由座標で打ち切らない) | `:760-774`(`_physical_reduce`) | `:418-423`(`_replay_connection`) | 同一 |
| 3 | echelon 不変条件 s_i[p_j]=0 (j<i) の強制 | `:773` `unreduced_pivot_coordinate` | `:423` `checker_unreduced` | 同一 |
| 4 | 正規化(σ=2 なら 2 倍して lead 値 1) | `:879-882` | `:426` | 同一 |
| 5 | target 還元(同じ挿入順 sweep) | `:1030-1051`(`_target_reduce`) | `:485-490`(`_target_reduction`) | 同一 |
| 6 | 自由座標 f = 剰余 u の最小非零座標・f は pivot lead でない | `:1067-1070` | `:496-497` | 同一 |
| 7 | 逆代入 λ[p_i] = -Σ_{j≠p_i} s_i[j]λ[j](i = r-1..0)・各行で内積 0 を明示検査 | `:1078-1090` | `:499-502` | 同一 |
| 8 | λ(ρ₂)=1 の明示検査(全 48,384 座標の内積) | `:1092-1093` | `:505` | 同一 |
| 9 | live pin(v11 の offers/rank/dependent/reduction_count/final_rolling_head) | `:542-544` | `:329-331` | 同一定数 |
| 10 | ρ₂ 親 pin(artifact id 9925190479・manifest sha・7 ファイル受領証) | `:90-124` | `:82-107` | AST 正規化で完全一致 |

**相互束縛**: state manifest の `connection_manifest_sha256` を checker が自前で再計算して等値要求
(`check_...:446`)、target reduction の `target_parent_manifest_sha256` も同様(`:533`)、
最終的に terminal 全体を自前構築物と等値要求(`:550` `checker_terminal_semantics`)。
したがって「producer が読んだ親」と「checker が読んだ親」がバイト単位で同一であることは検査済み。

**紙との一致**: `sol/proof_r07_canonical_separator_joined_driver_v536.md:44-79`(補題 2.1)の
定義 — f = u の最小非零座標、λ[f]=u[f]⁻¹、逆代入 (2.2)、λ(S)=0 ∧ λ(ρ₂)=1 — と実装は逐条一致。
F₃ では x⁻¹=x なので `lambda_dense[free[0]] = free[1]`(producer `:1072`)は u[f]⁻¹ と等しい(1⁻¹=1, 2⁻¹=2)。
§1 (1.1) の一方向 echelon 規約(pivot 座標は数値増加でなくてよい)も両実装が守っている。

**事前登録**: workflow `.github/workflows/d972-r07-grade2-physical-state-separator-v2.yml` の env で
親 run/artifact/digest/bytes・`PHYSICAL_CONNECTIONS=1354`・`PHYSICAL_REDUCTION_BOUND=915981`
(=1354·1353/2、検算一致)を計算前に固定。**出力側(rank・自由座標・還元数)は pin されていない**
= 答えを先に書いていない。silent cap なし: 8,059 行の全消費を trailing 空検査で強制
(`check_...:323`, `:476`)。cap は producer/checker 各 30 分・job 75 分、超過時は
UNKNOWN_RESOURCE を落として final artifact を publish しない(行き先が決まっている)。

**較正の非空虚性**: ConnectionMember 分岐・Separator 分岐・σ=2 分岐・physical_dependent 分岐・
非単調挿入(fixture leads [100,10,300])・「自由座標が既存 lead より数値的に小さい」場合
(fixture free=5 < lead 100)がすべて fixture で実際に通る。実データ側でも lead は
0,3,1,4,2,… と非単調(sol_reply_907)、free=1417 は複数の lead より大きい。
「仮定を満たす事例が存在しないテスト項目」は見つからなかった。

---

## 2. 独立性の実体

**checker は再計算している(中間状態の読み直しではない)。** `_replay_connection`
(`check_...:397-437`)は connection artifact の `top.bin`/`coefficient.bin` から
1,354 行を自前で消去し、`physical.bin` とバイト一致を要求(`:467` `checker_state_rows`)、
instruction 全 8,059 行を自前構築物と等値要求(`:473` `checker_state_record`)。
λ も自前構築して `lambda.bin` とバイト一致を要求(`:545`)。

**実測による確認(当哨が撃った)**: manifest と HEAD まで再ハッシュした**整合改竄**
(`state/physical.bin` の 1 トリット反転 + 全受領証の再計算)を投入したところ、
`checker_state_rows` で棄却された。意味論ゲートは実在し機能する。

**ただし共有面がある(確認済み)**: AST 正規化 diff で、両者の top-level 単位のうち
**44 件が正規化後に完全一致**。定数 pin(同一であるべき)に加えて、F₃ 演算核が逐語クローン:
`DIGITS`(prod:249 / chk:169)、`PACKED_AXPY`(250 / 170)、`SCALE_TWO`(257-259 / 177-179)、
`FIRST_TRIT`/`FIRST_VALUE`(260-261 / 180-181)、`_digits`、`validate_packed`、
`sha_file`、`_read_json`、`canonical`。`pack`/`unpack`/`first_nonzero`/`packed_trit`/`axpy` は
改名・整形のみの差。両ファイルは**同一コミット 7b7b9de2 で同時に入った**。

→ 核のバグは二系統一致では検出できない。**当哨が素朴実装(基数 3 直書き)で全数照合した**:
`PACKED_AXPY` 全 2×81×81 通り、`DIGITS`/`SCALE_TWO`/`FIRST_*` 全 81 通り、
`pack`/`unpack`/`first_nonzero`/`axpy` を幅 48,384・8,059・4・5・7 でランダム照合 —
**不一致ゼロ**。このリスクは retire 済みと報告してよい。

**Sol 907 の第三 replay** は「標準 base-3 デコーダ・packer・rolling replay・内積」を自前で書いた
もので、physical rows 全 1,354 行に対する直接内積 0 と ρ₂ に対する 1 を確認している
(`sol/sol_reply_907_audit_r07_physical_state_separator_run2.md` の "Direct dot check" 行)。
ただし **producer・checker・第三 replay はいずれも Sol の実装**であり、
「三系統独立」ではなく「一著者三実装」。非当事者判読が要る所以はここ。

---

## 3. 主張の射程

**cross-checked と呼べる範囲(certificate 付き)**

- v11 の 8,059 offer 指示鎖が内部整合で pin 済み rolling head に到達し、6,705 pivot / 1,354 connection に分類される。
- S₀ = 1,354 本の connection top 行を挿入順に還元した echelon の張る空間、rank 1,354、dependent 0。
- red_{S₀}(ρ₂) = u ≠ 0(884 回の非零還元・最小非零座標 1417・値 2)。
- λ が存在し、**格納された 1,354 本の還元後行すべてに対して λ·s = 0、λ·ρ₂ = 1**。

この否定的主張(ρ₂ ∉ S₀)は「探索して見つからなかった」型ではなく、**λ という肯定的証明書**に
支えられている。数値 rank の正しさに全面依存する形にはなっていない — ここは通常の失敗型ではない、
と明記しておく価値がある。

**限定 1【要修正】: λ の直交検査は「還元後の行」に対してのみ。**
必要な主張は ρ₂ ∉ span(原本 Conn 行 T_0..T_1353)だが、検査されているのは λ ⊥ {還元後行 R_i}
(producer `:1085` / checker `:501`)。span(R) = span(T) は還元が可逆三角(R_j = σ_j(T_j − Σ_{i<j} s_{ji}R_i)、
σ_j ∈ {1,2} は F₃ で可逆)であることからの**推論**であり、checker が自前で R を T から構成している
ので構成的ではあるが、直接検査ではない。
→ **λ·T_j = 0 を 1,354 本の原本 top 行に対して直接撃つだけで、証明書は echelon 機構全体から独立になる。**
コストは 1,354 × 48,384 の内積 1 回(既存の逆代入と同オーダー)。Sol 907 の direct dot check も
還元後行に対してのみなので、この穴は現状どの層でも塞がれていない。

**限定 2【軽微】: 「その 1,354 行の lower が消えている」は v11 親からの継承で、本 run では再検証されない。**
connection 行は lower 行を持たない(`lower = {"offset": None, ...}`; producer `:506` / checker `:310`)ため、
原理的に本 checker からは再導出不能。v11 側の意味論(`search/d972_r07_canonical_p1_physical_connection_v6.py:610-616`:
`lower_zero = (first_nonzero(lower_acc) is None)`、`top.bin` は対応する accumulated top)に依存する。
裁定 2048 の射程。
なお安い追加 pin を探したが、`ell_sha256` は**使えない**: v11 は `sha(ell)`(還元前の生入力)を記録しており
(同 `:616`)、還元後の零 lower の固定ハッシュではない。ここに固定値検査は置けない。

**限定 3【軽微】: 演算核が逐語クローン**(§2)。当哨の素朴実装照合で retire 済み。

**主張していないこと(正しく保持されている)**

- GRADE2 MEMBER/NONMEMBER は `NOT_DECIDED`(両ファイル `CLAIM_FALSE`; prod `:129-134` / chk `:108-113`)。
  v536 §3 (3.2) は S₀ ⊆ M₂ かつ後続 S_n ⊋ S₀ なので、S₀ の separator は M₂ の非所属を与えない。正しい。
- `ACTUAL_CONNECTION_STATE=false`、A0/COMMON/COFINAL_LIFT/FAKE/IHARA は `NOT_DECLARED`。
- `verified=false` = Lean 未形式化(工房規律で "verified" は Lean 予約)。二系統一致は cross-checked どまり。

---

## 4. 付随所見(装置の穴ではなく試験集合の穴)

**【要修正】ミューテーション試験 3 件が意図したゲートに当たっていない(空虚性)。**
checker selftest を実行し 20 件の棄却理由を採取した結果:

```
lead_mutation                -> checker_state_instruction_rolling
scale_mutation               -> checker_state_instruction_rolling
physical_reduction_mutation  -> checker_state_instruction_rolling
```

意味論再導出ゲート `checker_state_record`(`:473`)・`checker_state_rows`(`:467`)には
**一件も当たっていない**。整合ハッシュという安いゲートが先に吸収してしまうため、
この試験集合は「fail-closed であること」は示すが「意味論ゲートが発火すること」は示さない。
整合改竄(rolling 鎖まで作り直した改竄)を 1 件足せば塞がる。
当哨が実際に整合改竄を撃った結果は §2 のとおり **棄却(`checker_state_rows`)** — 装置は健全。

**【軽微】checker は `launch["resume"]` を検査しない**(producer `:409` は live で False を要求)。
state は checker が全面再導出するので数学的被覆は落ちない = 非 load-bearing な非対称。

**【軽微】stager は演算をしない**ことを確認(`search/stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py`:
`copy_stream` が元ファイルを streaming hash して pin 済み sha256 と照合してからコピー・
manifest/verdict/acquisition を書くだけ・roster 厳密一致・atomic rename)。
GH artifact digest → 個別ファイル pin sha256 → 両実装が同じ pin を再照合、で鎖は繋がっている。

---

## 5. 破れなかった観点(正直な範囲報告)

以下は撃ったが穴を見つけられなかった。保証ではない。

- F₃ 演算核の正しさ(素朴実装で全数/ランダム照合・不一致ゼロ)。
- 逆代入の数学的健全性(echelon 不変 (1.1) により、後段で λ[p_j] (j<i) を書き換えても行 i の方程式は壊れない。両実装が (1.1) を明示検査している)。
- λ·ρ₂ = 1 の必然性(λ·ρ₂ = λ·u = u[f]·u[f]⁻¹ = 1。剰余 u は全 pivot lead で零なので他項は消える)。
- 意味論ゲートの実在(整合改竄で発火を確認)。
- silent cap / 事前登録違反(見つからず)。
- producer と checker の規約差(AST diff・pin 全比較で差分なし)。

---

## 6. 格付け案(一行・v11 と同書式)

> checker PASS(Separator・S₀ rank 1,354・λ(S₀)=0・λ(ρ₂)=1・free coordinate 1417・target reductions 884)・
> **cross-checked は限定つき**: (i) 直交検査は還元後 1,354 行に対してのみで原本 Conn 行への直接検査がない、
> (ii) 両実装は同一コミット・同一著者で F₃ 演算核が逐語クローン(核は当哨が素朴実装で全数照合済み・retire)、
> (iii) 「lower が消える」性質は v11 親からの継承。射程は **ρ₂ ∉ S₀ = span(Conn)** のみで
> GRADE2 NONMEMBER ではない(NOT_DECIDED を正しく保持)。verified=false = Lean 未形式化。
