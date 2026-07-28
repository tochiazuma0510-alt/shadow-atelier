# `family-Rule1/template/v1`(普遍 family Rule 1 条項)— **seal v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱(便 76 **N76-4.1** を受けた seal 化・便 77 の主請求)。
**系譜**: `docs/notes/i2_family_rule1_memo_v1.md`(裁定 101)→ **`docs/notes/i2_family_rule1_memo_v2.md`(便 73 Q3 裁定反映・本 seal の正本)**→ 本 seal。書式は `docs/znorm_seal_final_v1.md`(minted ID・効力範囲・non_implications)に倣う。
**依拠**: TB4 導出 v2.5・Rule 1 v1.5 §1.4・BFC v2.15・`docs/notes/hfun_functoriality_v1.md`・`docs/notes/w2fam_v1.md`・`docs/notes/w2arith_v1.md`・便 73 Q3・**便 76 N76-4.1/N76-4.2・F76-4.1/F76-4.2・P76-2**。**外部文献なし。$u$・封印量に触れていない。**

### 状態欄

```text
# 現況(起草時点・起草者が記入)
status_now       = drafted / unapproved / non-operative
clause_provenance = docs/notes/i2_family_rule1_memo_v2.md   (便 73 Q3 裁定反映済)

# 発効時(司令塔が event receipt と同時に記入)
status_on_apply  = ____________________   # "approved / operative"
applied_at       = ____________________
event_receipt_id = ____________________
```

> **⚠ digest 自己参照禁止**(便 61 A61-2 と同じ規律): 本 seal は**自らの digest を含まない**。digest の authority は **external event receipt** にある。
> ```text
> seal_sha256_authority                  = external event receipt
> do_not_write_self_digest_into_this_seal = true
> ```

---

## 1. 条項本体(scope = `family` / 全奇数 $q\ge3$ に普遍量化)

```text
family-Rule1/template/v1  (scope = family, quantifier = "for all odd q >= 3"):

  (FR-1) [補題 U による ι_∞ の指定]
         任意の N >= 3 について、Φ_N の複素根のうち Im > 0 かつ Re 最大のものは
         e^{2πi/N} ただ一つである(補題 U)。
         Φ_N が T-bar の最小多項式であることにより、この根の指定は埋め込み
         Q[T]/(Φ_N) -> C を一意に定める。

  (FR-2) [数体と体生成元]
         K_q := Q[T]/(Φ_{4q}),        zeta_{4q}^Rule := T-bar
         iota_infty^{(q)} := (FR-1) を N = 4q に適用して得る一意の埋め込み
                             (すなわち iota_infty^{(q)}(zeta_{4q}^Rule) = e^{2πi/(4q)})

  (FR-3) [(1.7) 族版 — zeta_M 部のみ]
         M := 2q,   2M := 4q
         zeta_M^Rule := (zeta_{2M}^Rule)^2,     ord(zeta_M^Rule) = M
         # 便 73 Q3.4: TB4-E の load-bearing はこの一条のみ。式へ inline してもよい。

  (FR-4) [制限]
         bar_iota|_{K_q} = iota_infty^{(q)}
         # 便 73 Q3.4-1: 必須。完全な制限等式を「生成元 1 個の上の等式」へ弱めることは
         #               可能だが、何らかの typed compatibility は必須。

  (FR-5) [(E-iv) 命名条項]
         iota : mu_M --~--> <X_q>,   zeta_M^Rule |--> X_q
         したがって  tau(zeta_M^Rule) = tau(X_q)
         # 位数条件 ord(X_q) = M = 2q は HF-1(b) が全奇 q >= 3 で証明済。
         # 命名そのものは群論から出ない(便 73 Q3.3)ため、本条項が供給する。
```

### 1.1 各条の身分と出所

| 条 | 内容 | 身分 | 出所 |
|---|---|---|---|
| **FR-1** | 補題 U | **証明済**(paper-proof) | `i2_family_rule1_memo_v2.md` §1・**便 73 Q3.1 PASS** |
| **FR-2** | $K_q$・$\zeta_{4q}^{\rm Rule}$・$\iota_\infty^{(q)}$ | **規約(自由選択)** | 同 §2.1・Rule 1 (1.5)(1.6) の族版 |
| **FR-3** | $\zeta_M$ 部のみ | **規約 + 原始性の証明**($\mathrm{ord}((\zeta_{4q})^2)=2q$) | 同 §2.3・**便 73 Q3.4 で $\zeta_q$ 部は降格** |
| **FR-4** | $\bar\iota$ の制限 | **規約(必須)** | 同 §2.3・**便 73 Q3.4-1** |
| **FR-5** | (E-iv) | **規約(命名)** | 同 §2.4・**便 73 Q3.3(I-2 残留と確定)** |

> **★ FR-3 の降格の記録**: 初版が併記していた $\zeta_q^{\rm Rule}:=(\zeta_{4q}^{\rm Rule})^4$ は **TB4-E の証明で使わない**ため本条項から外した。後続の族 Rule 1 が必要とするなら別条項として追加すること(**この seal に黙って足さない**)。
> **★ FR-1 の型注意**: 補題 U が決めるのは「どの根か」まで。**それが埋め込みを一意に決めるのは $\Phi_N$ が $\bar T$ の最小多項式だから**であり、(FR-1) の第 2 文がその一段を明示している。

### 1.2 本条項が**普遍に**与えるもの / **与えないもの**

| | |
|---|---|
| **与える** | 全奇 $q\ge3$ で $K_q$・$\zeta_{4q}^{\rm Rule}$・$\iota_\infty^{(q)}$・$\zeta_M^{\rm Rule}$・$\bar\iota$ の制限・(E-iv) 命名 の**型と指定方法** |
| **与えない** | **窓固有 object の同一性**(どの artifact ID がその $\zeta$ か)・**(E-iii) の有限群供給**・**測定側 (B-ii)–(B-iv)**・各窓の migration |

$$ \boxed{\ \textbf{本 seal は「指定の仕方」を普遍化する。「指定された object が何か」は窓別 record が供給する。}\ } $$

---

## 2. 二段 status の条文化(**N76-4.2**)

```text
[two-stage-status]
family_clause_available      : 本 seal の受領で true になる。
                               *窓の* 状態ではない — 全奇 q で同一の値をとる普遍量。
migrated_via_family_instance : 各 window-instance record の receipt 受領によってのみ true。
                               本 seal は一切これを動かさない。
```

| # | 条項 |
|---|---|
| **FS-1** | **本 seal が立てるのは `family_clause_available` のみ。** いかなる窓の `inventory_row_status` も動かさない。 |
| **FS-2** | **`family_clause_available` から `migrated_via_family_instance` への default / catch-all 遷移を置かない**(N76-4.2)。遷移は window-instance record の receipt によってのみ起きる。 |
| **FS-3** | **`migrated_by_family_clause` という語・設計を禁止する**(**F76-4.1**)。族条項の存在だけで全奇数窓を自動 `migrated` にすることは、W3-19/20 の named-window inventory・typed migration record・明示 catch-all 禁止と衝突する。 |
| **FS-4** | **family TB4-E を「無条件定理」または「各窓の compatibility 成立」と呼ばない**(**F76-4.2**)。族で通るのは **implication の型**であり、**(E-iii) の有限群供給・(E-iv) の命名・測定側 (B-ii)–(B-iv) は別に供給される**。 |
| **FS-5** | **未受領の欄を本 seal で埋め合わせない。** 空欄は「未供給」であって「族条項で満たされた」ではない。 |

---

## 3. registry の二分(**P76-2**)

```text
family_theorem_registry            # <- 本 seal はこの registry の *初項*
  entry_id      = "family-Rule1/template/v1"
  quantifier    = "for all odd q >= 3"
  clause_digest = <receipt で記入>
  effect        = family_clause_available := true
  window_effect = NONE                      # 既存窓の status を一切変えない

window_instance_registry           # <- 本 seal はこの registry に触れない
  entry per window (K9, K3, A5, ...)
  effect = inventory_row_status の遷移(receipt 受領時のみ)
```

> **★ 二分の意味**(P76-2): **前者への追加で既存窓の status は一切変わらず、後者の receipt だけが inventory row を動かす。** これで再証明の重さを避けつつ W3-19/20 の明示 migration を守る。

---

## 4. minted ID と依存の digest 束縛

```text
[minted-ids]
clause_id                = "family-Rule1/template/v1"
registry                 = family_theorem_registry
scope                    = family
quantifier               = "for all odd q >= 3"

[dependency-digests]   # すべて receipt で埋める(本 seal は自らの digest を持たない)
lemma_U_proof_id         = "i2-family-rule1-memo/v2"
lemma_U_proof_path       = docs/notes/i2_family_rule1_memo_v2.md
lemma_U_proof_sha256     = ____________________________________

w2_fam_id                = "W2-fam/group-side/v1"
w2_fam_path              = docs/notes/w2fam_v1.md
w2_fam_sha256            = ____________________________________

w2_arith_id              = "W2-1/arith-side/v1"
w2_arith_path            = docs/notes/w2arith_v1.md
w2_arith_sha256          = ____________________________________

hfun_id                  = "hfun-functoriality/v1"          # FR-5 の ord(X_q) = 2q
hfun_path                = docs/notes/hfun_functoriality_v1.md
hfun_sha256              = ____________________________________
```

> **⚠ ID の整合(起草者からの申告)**: 委嘱は minted ID の案として `family-rule1-clause/v1` を挙げたが、**既存の `docs/notes/k9_window_instance_v1.md` §2 が `family_clause_id = "family-Rule1/template/v1"` を既に参照している**。**参照先が食い違うと二段 status が接続しない**ので、**本 seal は既存 record が指す `family-Rule1/template/v1` を採る**。委嘱の案を採るなら **K9 record 側の同時修正が要る**(司令塔の裁定事項)。
> **⚠ (W2) 系の依存の位置づけ**: `w2fam` / `w2arith` は **(W2) を全奇 $n$ で閉じる**もので、**本条項 (FR-1)–(FR-5) の証明には使わない**。**下流((5′) の組立)が本 seal と併用する**ため依存欄に載せる。**本 seal の受領条件ではない。**

---

## 5. non_implications(**本 seal が含意しないもの**)

```text
non_implications = [
  "各窓の (E-iii) 供給 —— c_Lambda の x-同変性は B-4c 経路で窓ごとに供給される
                          (I-1 が与えるのは (W3)(W4)(W5) の有限群側だけ・便 73 Q3.3)",
  "P8-value —— a_9 の full class の独立測定。T63-P1 の前件ではなく、予言後の照合側 payload
                (便 76 §3: 前件に混ぜると予言先行が postdiction に変質する)",
  "A3 —— 位相 forward transport <-> 代数 後合成左作用。framework gate として未閉のまま
          (文献要請 13(ii))。本 seal は A3 を証明しない",
  "Lean verified —— 本 seal は paper-proof candidate。verified は Lean 到達まで予約",
  "任意の窓の migrated —— FS-1/FS-2/FS-3",
  "family TB4-E の無条件性 —— FS-4",
  "測定側 (B-ii)-(B-iv) の族化 —— 較正条項だけでは届かない(i2 memo v2 §2.5)",
  "(5') の任意の窓での instance —— 本 seal は前件の一部を供給するにすぎない"
]
```

---

## 6. window-instance record との接続

`docs/notes/k9_window_instance_v1.md` §2 の欄と本 seal の対応:

| K9 record の欄 | 本 seal での対応 |
|---|---|
| `family_clause_id = "family-Rule1/template/v1"` | **§4 の `clause_id`**(一致 ✓) |
| `family_clause_digest` | receipt が本 seal の digest を記入(**本 seal 自身は保持しない** — §0 の自己参照禁止) |
| コメント「補題 U ・ $K_q$ ・ $\zeta_{4q}^{\rm Rule}$ ・ $\zeta_M$ の族版 ・ $\bar\iota$ 制限 ・ (E-iv)」 | **(FR-1)–(FR-5) と 1:1** ✓ |
| `restriction_equality = "iota-bar\|_{K_9} = iota_infty^{(9)}"` | **(FR-4) の $q=9$ 適用宣言**。本 seal は型を、record は object を与える |
| `E-iv_marking_equality = "tau(zeta_18^Rule) = tau(X_9)"` | **(FR-5) の $q=9$ 適用宣言**(同上) |
| `rule_root_id` / `tb2_root_id` / `embedding_id` | **本 seal は供給しない**(§1.2)。**窓別 record の存在理由** |

> **★ WR-1(複製禁止)との整合**: K9 record は本 seal を**参照のみ**する。**本 seal も K9 の object ID を持たない。** 双方向に複製がないので二重正本は生じない。

---

## 7. 出所対応表(便 56 P56-1 の 5 欄)

| transfer_mode | source_range | target_range | approval_id | change_summary |
|---|---|---|---|---|
| `normative-only` | `i2_family_rule1_memo_v2.md` §1(補題 U) | (FR-1) | — | 版履歴注記・自認説明を省略。規範内容と型注意は保存 |
| `normative-only` | 同 §2.1(族条項) | (FR-2) | — | 同上 |
| `adapted` | 同 §2.3($\zeta_M$ 部・$\bar\iota$ 制限) | (FR-3)(FR-4) | 便 73 **Q3.4** | **$\zeta_q$ 部を条項から除去**(降格)。$\bar\iota$ 制限は必須のまま |
| `adapted` | 同 §2.4((E-iv)) | (FR-5) | 便 73 **Q3.3** | (E-iv) が I-2 残留であることを条項として明示。位数条件の出所を HF-1(b) と明記 |
| `adapted` | (新設) | §2 二段 status | 便 76 **N76-4.2 / F76-4.1 / F76-4.2** | 二段 status・catch-all 禁止・無条件視の禁止を条文化 |
| `adapted` | (新設) | §3 registry 二分 | 便 76 **P76-2** | `family_theorem_registry` の初項として登録する形を規定 |
| `verbatim` | `znorm_seal_final_v1.md` §0 の自己参照禁止規律 | §0 の digest authority | — | 便 61 A61-2 の規律を逐語で継承 |

---

## 8. 検証欄(実測値)

| 項目 | 結果 |
|---|---|
| CR(0x0D)・C0 制御文字・TAB | **0**(§9 のコマンドで実測) |
| 自己 digest 欄(live) | **0**(§0 の authority 宣言のみ) |
| `migrated_by_family_clause` の語 | **0**(F76-4.1 遵守 — §2 の禁止条項での言及を除く) |
| `family_clause_id` の K9 record との一致 | **一致**(`family-Rule1/template/v1`・§6) |
| $u$・封印量への言及 | **0** |
| 状態 | `drafted / unapproved / non-operative` — **Sol ゲート前・receipt 未発行・commit していない** |

## 9. 検査コマンド(再現用)

```sh
grep -Pc '\r' docs/family_rule1_seal_v1.md                              # CR = 0
grep -Pc '[\x00-\x08\x0B\x0C\x0E-\x1F]' docs/family_rule1_seal_v1.md    # C0 = 0
grep -Pc '\t' docs/family_rule1_seal_v1.md                              # TAB = 0
grep -c 'family-Rule1/template/v1' docs/notes/k9_window_instance_v1.md  # >= 1(接続確認)
```
