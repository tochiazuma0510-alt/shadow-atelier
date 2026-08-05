# ISO-GATE R3/R4 再走 — IF-FIRST 凍結文書 v1(CV-9-1・主検問)

**状態札: freeze / 計算前 / 本書の GAP・Python 実行ゼロ**

- 起草: implementer(司令塔委嘱・裁定 535 ⑥「再走前に本書を起草せよ」)。
- 目的: `docs/notes/conventions_ledger_v1.md` §1.3.1 (CV-9-1) の主検問を、**計算(再走)前に**通す。これまで CV-9-1 は未実施だった(falsifier 判読 `docs/notes/iso_r3r4_cv9_reading_v1.md` §0 の指摘)。本書がその欠落を埋める。
- 対象: `search/probe/w6_bu_s0/iso_gate_r3r4_driver.g`(GAP・v2 へ改版予定)と `search/probe/w6_bu_s0/r4_second_system.py`(Python・v2 へ改版予定)。
- 入力根拠: 裁定 535(司令塔)・`docs/notes/iso_r3r4_cv9_reading_v1.md`(falsifier CV-9-2 判読)・`docs/notes/auto_settled_check_v1.md` 付録 A(数学者 v1.1 addendum)。

---

## 1. 入力 universe(①)

両系統とも同一の marked datum 3 種を対象とする(v2 でも変更しない):

| datum | 生成 | 期待 `\|G\|` |
|---|---|---|
| K^(3) | `MakeGn(3)`(Dn タワー、9 点) | 108 |
| W-5 | `MakeGn(5)` × `MakeQ8` のファイバー積(23 点) | 1000 |
| N5-control | `BuildQTGeneral(Q5,...)` | 30(c∉N ⟹ precondition で停止) |
| Q3-a | `BuildQTGeneral(Q3,...)` | 18(θ/τ 非拡張で停止) |

M-ISO-2 の witness(v2 で経路層へ復元): K^(3) の実列挙中の h11_fail 候補 1 件(m=0, f 実元 = BFS 元 (7,9,8))。**v2 では witness を shadow バケツへ実際に移して SettledCheckGeneral の実経路へ通す**(旧 v1 のようにカウンタ層だけを迂回しない)。

## 2. 比較対象(②・CV-7 as_function_of)

比較は次の **5 量の関数**として宣言する(パラメータ = datum):

1. `g_size = |G|`(BFS 閉包の位数)
2. `n_ord = lcm(ord(x),ord(y))`
3. `shadow_total`(hexagon(3.10)(3.11) + SURJ を通過した candidate 数)
4. `settled_count / settled_total`(`SettledCheckGeneral` 相当の実経路を通した判定)
5. **`verdict`**(★ v2 で新たに比較対象に追加 — v1 は比較していなかった。GAP `ComputeVerdict(shadowSumOk, total, settled)` と同型の **3 変数関数**を Python 側にも実装し、入力 3 つ組そのものを突合する)

`comparison_target.function_a` = GAP `IsoGateCheck`/`ComputeVerdict`(`search/probe/w6_bu_s0/iso_gate_r3r4_driver.g`)。`function_b` = Python `run_fixture`/`compute_verdict`(`search/probe/w6_bu_s0/r4_second_system.py`)。

## 3. 同値関係(③)

両系統は「同じ marked datum に対し同じ 5 量を出す」ことをもって一致とする。個々の値の**同値関係は等号**(整数・文字列の完全一致)。`shadow_sum_check`(恒等式 `|D|×|charming| − h10 − h11 − genfail = shadow_total`)は**両系統で同一の帳簿単位**(= (f,m) 対ごと)を使わない限り比較不能 — これが R-A の修理対象。

## 4. 正規形(④・NF)

`conventions_used` ブロックへ両系統とも以下を事前宣言する(⑤ の実装値はこの節の予定どおりにする):

| 規約 | GAP(予定) | Python(予定) |
|---|---|---|
| `perm_composition`(CV-1) | `gap_native_right`(`i^(p*q)=(i^p)^q`) | 同型実装 `compose(p,q)` = 同じ規約(モジュール docstring に明記済み) |
| `AbstractProd` 反転 | 添字降順(`AbstractProd([a,b,c])=c*b*a`、falsifier 確認済み・§2.1 逐条) | 同一の反転を適用(genB/ymf/z の 3 箇所、falsifier 確認済み) |
| 語の格納規約(BFSWords) | prepend(裁定166) | witness は `f_word` でなく raw `f_images` を経由(語規約に依存しない) |
| 列挙域 | `D = DerivedSubgroup(G)` | `D` = 全対の交換子閉包(同一部分群、falsifier `\|D\|` 一致確認済み) |
| θ/τ | `GroupHomomorphismByImages` の fail 検査 | BFS 矛盾検出(同一の数学的事実、falsifier §2.4 確認済み) |
| `h10_fail` 帳簿単位 | **(f,m) 対ごと**(m ループの内側でカウント) | ★ v2 で **(f,m) 対ごとへ統一**(v1 は f ごとで不一致だった — R-A) |

## 5. filter(⑤)

- 列挙フィルタは hexagon(3.10)(3.11) + SURJ のみ(descent は使わない — AS-GAP-3 で確定済み・不変)。
- `shadow_sum_check` 不整合時は **verdict の gate として最優先**(`CANDIDATE_ENUM_INCONSISTENT`)。Python も同じ 3 変数関数で実装する(R-A)。

## 6. 失敗状態(⑥)

| 状態 | 発火条件 | 両系統で同型か |
|---|---|---|
| `UNKNOWN(C_NOT_IN_N)` | precondition_ok=false | ○(GAP のみ実装・Python は該当 datum を実行しない) |
| `UNKNOWN(THETA_TAU_NOT_WELLDEFINED)` | θ/τ 非拡張 | ○(GAP: graceful catch。Python: `theta_ok`/`tau_ok`=false で早期 return) |
| `UNKNOWN(NO_SHADOWS)` | shadow_total=0 | ○ |
| `UNKNOWN(CANDIDATE_ENUM_INCONSISTENT)` | shadow_sum_check=false | ★ v2 で Python にも実装(R-A) |
| **`UNKNOWN(NONSHADOW_IN_DATUM)`** ★新設 | witness(非 shadow 候補)が settled=false を返した datum | ★ v2 で両系統に新設(R-B)。**この状態のとき verdict は FALSE ではなく UNKNOWN** — 「shadow でない候補が紛れ込んだ」ことを示す fail-closed 停止であり、isolated=FALSE の主張ではない |

## 7. 期待値(凍結・再走前に書く)

| 量 | K^(3) | W-5 | M-ISO-2(v2 版) |
|---|---|---|---|
| `g_size` | 108 | 1000 | (K^(3) 由来) |
| `n_ord` | 6 | 20 | — |
| `shadow_total`(修理前) | 12 | 80 | — |
| `shadow_total`(M-ISO-2 移設後) | — | — | **13**(12 真 shadow + witness 1 件を shadow バケツへ) |
| `h11_fail`(M-ISO-2 移設後) | — | — | **23**(24→23) |
| 恒等式 | `108-72-24-0=12` | `4000-3200-720-0=80` | `108-72-23-0=13` ✓ |
| `settled_count/total` | 12/12 | 80/80 | **12/13**(witness だけ false) |
| `verdict` | TRUE | TRUE(iso_gate_state は UNKNOWN のまま) | **UNKNOWN(NONSHADOW_IN_DATUM)**(FALSE ではない) |
| M-ISO-8(settled:=true 固定変異) | — | — | mutant 出力 TRUE ≠ 実 verdict UNKNOWN(NONSHADOW_IN_DATUM) ⟹ killed |

この表と食い違う再走結果が出た場合、**副検問(CV-9-2)で救済せず本書へ差し戻す**(CV-9-4)。

---

**非接触宣言**: Im R・封印 3 量・W-5 の iso_gate_state(UNKNOWN 不変)・705,894 宇宙は本書でも非接触。AS-GAP-6(真の non-isolated witness 取得)は本書の射程外(引き続き UNKNOWN)。
