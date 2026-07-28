# $K^{(5)}$ typed migration / identity record **v1**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱・裁定 71。
**身分**: `Z-norm-seal/v1` §3 window inventory の `K5` 行が参照する **migration record 本体**(component 2)。便 60 F4.1-2 の要求物。
**状態**: `drafted / unapproved / non-operative`。

> **本 record が主張すること**: $K^{(5)}$ 窓の root object は、**既存の finite edge `rule1-tb2-root-equality/v1`(scope = `level_20`)を経由して、`Z-norm-seal/v1` の profinite root system と同一 object 化済み**である。
> **本 record が主張しないこと**: $K^{(5)}$ 窓の `root_normalization_level` を `profinite` へ昇格させること(§5 参照)。

---

## 1. record 本体(typed)

```text
migration_record_id   = "k5-root-migration/v1"
window_id             = K5                       # M = 10, 2M = 20
previous_level        = level_20
target_seal_id        = "Z-norm-seal/v1"
compatibility_status  = migrated

# --- identity binding(便 59 P59-A2 の三式を K5 窓へ実体化)---
bar_iota_id           : Z-norm.bar_iota_id = Z20-link.bar_iota_id
root_system_id        : restrict(Z-norm.root_system_tb2_id, n=20) = Z20-link.root_system_tb2_id
derived_edge_id       : "rule1-tb2-root-equality/v1"

# --- 経由する finite edge(既存 ID・改名しない)---
edge_id               = "rule1-tb2-root-equality/v1"
lhs                   = restrict(root_system_tb2_id, n=20)
rhs                   = rule1_root_2M_id          # zeta_20^Rule1(K の体生成元)
scope                 = level_20
proof                 = Z-norm(1)(2) + Rule 1 (1.6)   # = docs/znorm_forall_proof_v1.md 系 ZP-2
```

---

## 2. 根拠(出所つき)

| # | 根拠 | 出所 | 身分 |
|---|---|---|---|
| G1 | `Z20-link-seal/v1`(scope = `level_20`・atomic・4 条)が $K^{(5)}$ 窓で採用済み | **Rule 1 v1.4 §1.4.1** | **operative**(便 58 F5.1: `docs/week4-K5_Rule1_v1_4.md` = operative) |
| G2 | 「finite `Z20-link-seal/v1` を採用」が発効規約に含まれる | **便 58 F5.2** | operative |
| G3 | $\zeta_{20}^{\rm Rule1}=\bar T\in K=\mathbb Q[T]/(\Phi_{20})$ と $\iota_\infty(\zeta_{20}^{\rm Rule1})=e^{2\pi i/20}$(**一意**) | Rule 1 (1.5)(1.6) | 凍結済 |
| G4 | $\mathrm{restrict}(\zeta_\bullet^{\rm TB2},n=20)=\zeta_{20}^{\rm Rule1}$、すなわち $t_{20}=1$ | **`docs/znorm_forall_proof_v1.md` 系 ZP-2** | component 1 |
| G5 | $\bar\iota|_K=\iota_\infty$ | `Z-norm-seal/v1` (1) | component 3 |

> **同一 object 化の論証(1 段)**: G5 と G3 より $\bar\iota\bigl(\zeta_{20}^{\rm Rule1}\bigr)=\iota_\infty\bigl(\zeta_{20}^{\rm Rule1}\bigr)=e^{2\pi i/20}$。他方 `Z-norm-seal/v1` (2) の $n=20$ 成分は $\bar\iota^{-1}\bigl(e^{2\pi i/20}\bigr)$。$\bar\iota$ は単射だから両者は $\bar{\mathbb Q}$ の**同一の元**である。**G1/G2 により、その元を指す artifact ID は $K^{(5)}$ 窓ですでに `rule1_root_2M_id` として operative に固定されている** — ゆえに値の一致ではなく **object identity** が成立する(便 59 F3.2 の要求)。

---

## 3. 本 record が閉じる欄

| 欄 | 値 |
|---|---|
| `Z-norm-seal/v1` §3 inventory の `K5` 行 `compatibility_status` | `migrated` |
| 同 `migrated_record_digest` | **本 record の sha256**(§6 の枠・司令塔記入) |
| `derived_level20_edge_id` | `"rule1-tb2-root-equality/v1"` |

---

## 4. 本 record が**変更しないもの**

1. **`b_op` の最小前件**: TB4-E package(**root-link-free**)のまま。root compatibility を最小前件へ追加しない(便 59 P59-A4)。
2. **定理 TB4-A20 の札**: `finite theorem (M|20), conditional on Z20-link` のまま**据え置く**(profinite seal へ書き換えない = scope 逆行の禁止)。
3. **測定規律**: Rule 1 (7.1) の $b_i$ 実測、fitting 禁止、二段コミット、integrity quarantine。
4. **operative bridge predicate** $(5'_b)$、`b_semantics="op"`、`b_value_i = b_op_value`。
5. **A3 gate**: 本 record は A3 を証明しない。

---

## 5. `migrated` の意味の限定(**昇格ではない**)

$$ \boxed{\ \texttt{compatibility\_status = migrated}\ \ne\ \texttt{root\_normalization\_level = profinite}\ } $$

本 record は「**$K^{(5)}$ の root object が profinite seal の root system と同一 object である**」ことを固定するだけである。$K^{(5)}$ の comparison が `root_normalization_level = profinite` を**主張してよいか**は、`Z-norm-seal/v1` §1 (4) と dictionary 規則文(`docs/znorm_apply_patches_v1.md` P-2)が別途定める。**本 record を昇格の根拠として単独で用いてはならない。**

---

## 6. identity 欄と digest authority(**便 61 A61-2 で自己 SHA 欄を撤去**)

```text
artifact_id      = "k5-root-migration/v1"
artifact_path    = docs/k5_migration_record_v1.md
bound_seal_id    = "Z-norm-seal/v1"
bound_edge_id    = "rule1-tb2-root-equality/v1"
depends_on       = "tb2-canonical-root-equality/profinite-v1#proof"   # component 1(ID 参照・digest は埋めない)

artifact_sha256_authority              = external final seal + event receipt
do_not_write_self_digest_into_this_artifact = true
```

### 状態(**外部状態として宣言**・本 record 内では変化しない)

```text
immutable candidate blob;
operative iff bound by the approved event receipt
```

> **⚠ v1 の欠陥(自認・便 61 F5 blocker A61-2)**: v1 §6 は `artifact_sha256 = ____ # 司令塔が本ファイル確定後に記入` という**自己 SHA 記入枠**を置いていた。**記入した瞬間に bytes が変わり、その値は自分自身の hash でなくなる。自認。**
> **⇒ 修文後の規律**: 本 record の digest は**外部**(`Z-norm-seal/v1` §3 の `K5` 行 `migrated_record_digest` と event receipt)が保持する。**本ファイルは自らの digest を含まない**ので確定後は byte 不変。
> **⇒ `depends_on` は ID 参照であって digest 参照ではない** — component 1 の digest を本 record へ埋め込むと、component 1 の修文のたびに本 record の hash が連鎖して動く。**ID で束ね、digest は final seal に一元化する。**
> **⇒ 順序(便 60 F4.1・不変)**: `component 1 → component 2 → final seal → receipt`。**`migrated` と空 digest の組合せを final artifact に残してはならない**(final seal §3 の `K5` 行は本 record の実 digest で埋める)。
