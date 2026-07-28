# $K^{(9)}$ window-instance record(案 α)v1 — family-instance の初 fixture

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 124-2)。状態 = candidate。commit していない。**
**根拠**: 便 76 **N76-4.1**(普遍 family template の採用)・**N76-4.2**(二段 status)・**N76-4.3**(thin record の必須欄)・**N76-4.4**($n=9$ を最初の family-instance fixture に)・**F76-4.1**(catch-all 禁止)・**F76-4.2**(family TB4-E を無条件定理と呼ばない)・**P76-2**(registry の二分)。
**射程**: **数学の再証明はしない。** 本 record が束縛するのは **object identity と typed equality だけ**である(便 76 F1.6「GLOBAL 八行は既存定理の供給であり、**窓固有 object の同一性までは供給しない**」)。
**規律**: $u$ の値・平方類・封印量に触れていない。lane 実装・freeze 線文書(N∞ spec / contract / manifest)には触れていない。

---

## 0. この record が何であって何でないか(4 行)

1. **であるもの**: `window_instance_registry` に載る **$n=9$ の 1 行**。**普遍定理の $n=9$ への適用宣言**と、**窓固有 object の同一性の再掲**。
2. **でないもの**: 定理の再証明・family clause の再掲・`family_theorem_registry` への追加(**P76-2 の二分**に従う)。
3. **status を動かすのは本 record の receipt だけ**(N76-4.2)。**family clause の存在だけでは `migrated` にならない**(F76-4.1)。
4. **未受領の欄は空欄で出す。** 埋まっていない欄を「族条項があるから満たされている」と読んではならない(catch-all 禁止)。

---

## 1. 二段 status(N76-4.2)

```text
[window-status]
family_clause_available      = true       # 普遍定理(family Rule 1 template)が存在する
                                          #   -> これは *窓の* 状態ではない。全奇 n で同一の値。
migrated_via_family_instance = false      # 本 record の receipt 受領後に true
                                          #   -> 現在 false。default/catch-all 遷移は存在しない。
inventory_row_status         = not_assessed
```

| # | 条項 |
|---|---|
| **WS-1** | **`family_clause_available` から `migrated_via_family_instance` への自動遷移を置かない。** 遷移は **本 record の receipt** によってのみ起きる(N76-4.2)。 |
| **WS-2** | **`migrated_by_family_clause` という語を使わない。** 族条項の存在だけで窓を `migrated` にする設計は W3-19/20 の named-window inventory と衝突する(F76-4.1)。**I8 memo §6 の案 β の語もこの語では書かない。** |
| **WS-3** | **本 record は「family TB4-E が各窓で compatibility を成立させた」とは主張しない。** 族で通るのは implication の型であり、(E-iii) の有限群供給・(E-iv) の命名・測定側 (B-ii)–(B-iv) は別に供給される(F76-4.2)。 |

---

## 2. 必須欄(N76-4.3)— thin record 本体

```text
[window-instance-record]                   # window_instance_registry の 1 行
schema_id            = "mb/window-instance/v1"
schema_digest        = <64 hex — 発行時に記入>

# --- 窓の同定 ---
window_id            = "K9"
n                    = 9
M                    = 18                  # = 2n
2M                   = 36                  # = 4n ・ (W2) の完全列と link の水準

# --- 普遍側(family_theorem_registry への参照・値は複製しない)---
family_clause_id     = "family-Rule1/template/v1"          # N76-4.1 で採用された普遍 template
family_clause_digest = <64 hex — 発行時に記入>
                       #   含む: 補題 U ・ K_q = Q[T]/(Phi_{4q}) ・ zeta_{4q}^Rule = T-bar
                       #        ・ zeta_M の族版 ・ iota-bar|_{K_q} = iota_infty^{(q)} ・ (E-iv)

# --- 窓固有 object の同一性(本 record の実質)---
rule_root_id         = <2M=36 の Rule 1 field-generator object の ID>     # I8 memo P7
rule_root_digest     = <64 hex>
tb2_root_id          = <M=18 の (TB2) 根系 artifact の ID>                 # I8 memo P6
tb2_root_digest      = <64 hex>
embedding_id         = <K_9 = Q[T]/(Phi_36) -> C の埋め込み object の ID>

# --- typed equality(再証明ではなく「どの object の間の等式か」の宣言)---
restriction_equality   = "iota-bar|_{K_9} = iota_infty^{(9)}"    # 制限の一致(族 template の (1.7) 族版)
E-iv_marking_equality  = "tau(zeta_18^Rule) = tau(X_9)"          # I8 memo §5 の (E-iv)@9

# --- inventory との束縛 ---
inventory_row_digest = <64 hex: W3-19/20 の named-window inventory の K9 行の digest>
```

| # | 条項 |
|---|---|
| **WR-1** | **`family_clause_*` は参照のみ**。普遍 template の内容を本 record に**複製しない**(複製は二重正本を作る — P76-2 の registry 二分の趣旨)。 |
| **WR-2** | **`rule_root_*` / `tb2_root_*` / `embedding_id` は窓固有 object**であり、**普遍定理からは出てこない**。**本 record の存在理由はここにある。** |
| **WR-3** | **`restriction_equality` と `E-iv_marking_equality` は typed equality の宣言**であって証明ではない。**証明は普遍 template 側にあり、ここでは「どの object 間で主張するか」を固定する。** |
| **WR-4** | **`inventory_row_digest` は受領時に受領側が再計算して照合する。** producer の申告値を信じない。 |
| **WR-5** | **欄の欠落は「未供給」であって「族条項で満たされた」ではない。** 空欄のまま `migrated_via_family_instance = true` にしてはならない。 |

---

## 3. $n=9$ で埋まる値と埋まらない値(現状)

| 欄 | 状態 | 出所 / 待ち |
|---|---|---|
| `window_id` / `n` / `M` / `2M` | **埋まる**(`K9` / 9 / 18 / 36) | I8 memo §1 の助変数表 |
| `family_clause_id` | **埋まる**(N76-4.1 で採用済) | 便 76 N76-4.1 |
| `family_clause_digest` | **待ち** | family Rule 1 template の凍結 |
| `rule_root_id` / `_digest` | **待ち** | I8 memo **P7**($2M=36$ の field-generator object) |
| `tb2_root_id` / `_digest` | **待ち** | I8 memo **P6**($M=18$ の (TB2) 根系) |
| `embedding_id` | **待ち** | $K_9=\mathbb Q[T]/(\Phi_{36})$ の埋め込み object |
| `restriction_equality` | **文言は確定**・object 未束縛 | 族 template の $\bar\iota|_{K_q}=\iota_\infty^{(q)}$ を $q=9$ へ |
| `E-iv_marking_equality` | **文言は確定**・object 未束縛 | I8 memo §5(HF-1(b) が $\mathrm{ord}(X_9)=18$ を与えるが**名前は与えない**) |
| `inventory_row_digest` | **待ち** | W3-19/20 の `K9` 行 |

> **⇒ 本 record が閉じるために要るのは object の凍結だけ**であり、**数学の未決は無い**(I8 memo v3 §7-6)。
> **⇒ ただし I8 memo の P4($(Z_{36}$-link$)$)と P8-value($b_9$ の value commitment)は本 record の欄ではない** — 前者は seal / 族条項の供給(I8 memo §6 の案 α/β)、後者は**凍結 2 / BRIDGE-IN bundle** の欄(条文案 A (F2)(F3))。**混ぜない。**

---

## 4. I8 memo の窓固有 4 件との対応

| I8 memo | 本 record が束縛するか | 置き場所 |
|---|---|---|
| **P4** $(Z_{36}$-link$)$ | **しない** | `Z-norm-seal/v1` の migration certificate(案 α)/ 族条項(案 β) |
| **P6** `tb2_root_id` | **する** | 本 record §2 |
| **P7** `rule_root_id` | **する** | 本 record §2 |
| **P8-value** `b_value_9` | **しない** | 凍結 2 / BRIDGE-IN bundle(順序要件 (F3) つき) |

> **⇒ thin record は 4 件のうち 2 件(P6・P7)を束縛する。** 残る P4・P8-value は**別 receipt**。**「この record が出れば窓が閉じる」と読んではならない。**

---

## 5. 受領側の検査手順(案)

```text
WI-1  schema_id / schema_digest が window_instance_registry の型と一致
WI-2  family_clause_id が family_theorem_registry に実在し、digest が一致
        -> 実在しなければ INTEGRITY_STOP(参照先の不在)
WI-3  rule_root_* / tb2_root_* / embedding_id が実在 object を指し、digest が一致
WI-4  restriction_equality / E-iv_marking_equality の左右が WI-3 の object を参照している
        -> 文字列だけの等式宣言(object を指さない)は不受理
WI-5  inventory_row_digest を受領側が再計算して照合(WR-4)
WI-6  空欄が 1 つでもあれば migrated_via_family_instance を true にしない(WR-5)
```

---

## 6. 規律の自己申告

- **本 record は数学を 1 行も再証明していない。** 束縛するのは object identity と typed equality のみ(N76-4.3 の趣旨どおり)。
- **未確定を空欄で出している**(§3 の「待ち」8 欄)。**空欄を族条項で埋めたと読ませない**(WR-5・F76-4.1)。
- **`migrated_by_family_clause` の語を使っていない**(WS-2)。I8 memo §6 の案 β を採る場合も、**thin record を発行する限り案 α と同じ意味になる**(N76-4.4)ので、**案 β 側の語も本 record 経由で書く。**
- **UNKNOWN**: 本 record の schema そのもの(`mb/window-instance/v1`)は**未凍結**であり、`window_instance_registry` の実体も未作成。**P76-2 の registry 二分が採用されるまで、本稿は「案」である。**
