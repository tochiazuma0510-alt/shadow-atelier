# `Z-norm-seal/v1` 発効に伴う適用パッチ案 **v1**(component 4・5)

2026-07-28 起草: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱・裁定 71。
**身分**: **パッチ案であり、適用は司令塔が行う。** 本ファイルは他文書を変更しない。
**状態**: `drafted / unapproved / non-operative`。**発効 transaction の中でのみ適用可**(便 60 F4.1 の順序で final seal が hash された後)。

---

## P-1(component 4)— TB4-B 札更新パッチ(適用先: `docs/week4-TB4導出_opus_v1.md` v2.4)

**適用先の候補箇所**: §0 状態札の表・§3.3 定理 TB4-B・§8.5 状態札の更新案・付録 A の `TB4-B` 行。

### 差し替え文

| 主張 | **現行(v2.4)** | **適用後** |
|---|---|---|
| **TB4-B**($\varepsilon=1$) | `paper-proof / conditional on (Z-norm)` | **`root-normalization-relative paper theorem / A3-framework-conditional`**(relative to **`Z-norm-seal/v1`**) |
| **TB4-A20**($\varepsilon\equiv1\ (20)$) | `paper-proof / conditional on (Z20-link)`(便 50 F2.1 で型修理後 PASS) | **不変**(**据え置く**) |

### 添える注(そのまま貼る想定)

> **【`Z-norm-seal/v1` 発効に伴う札更新】** 定理 TB4-B の $\varepsilon=1$ は、`Z-norm-seal/v1` の下で **root-normalization-relative な紙上定理**になった。
> **1. `verified`(Lean)ではない。**
> **2. A3-framework-conditional のまま** — `Z-norm` は A3(位相 forward transport $\leftrightarrow$ 代数 後合成左作用)を**証明しない**(TB4 導出 v2.4 §8.2・component 3 §6-4)。【GAP-TB】は残る。
> **3. 「無条件」と呼ばない**(★教材 T11:「無条件」は空の前件を意味する)。正しくは「`Z-norm-seal/v1` に相対的」。
> **4. 定理 TB4-A20 の札は据え置く。** `Z-norm` が `Z20-link` を含意しても、**有限定理の前件を profinite seal へ書き換えてはならない**(scope 逆行 = 便 55 P55-2 lint 違反)。
> **5. 四段のはしご (3.6)(3.7) は不変。** $L3\nRightarrow L4$ の witness($2,5$ 進成分 $1$・$3$ 進成分 $-1$ の $\hat{\mathbb Z}^\times$ unit)は、**seal が発効しても「$L3$ から $L4$ は出ない」という論理事実**として残る — seal は $L4$ を**仮定**として供給するのであって、$L3$ から**導出**するのではない。
> **6. `NF-root-link` 系 negative fixture は存続。** seal は「$t_{20}=11$ が起こらない」ことを保証するが、**「起こっても検出できる」ことは保証しない**(測定の盲点は seal では消えない・§3.5.4)。

### 適用しないもの(明示)

- **§3.5.2 命題 TB4-E**(**$b_{\rm op}=1$ は root-link-free**)の前件・札は**一切変更しない**(便 59 P59-A4)。
- **§8.4 の測定規律・integrity quarantine**、**§8.7 の amendment 非削減条項**は不変。
- **§12.1 文献要請 13(ii)**(A3 の comparison orientation)は**縮小維持のまま存続**。

---

## P-2(component 5)— dictionary 規則文(適用先: TB4 導出 v2.4 §8.6a / Rule 1 の `TB4-b-dictionary` 系 schema)

### 追加する条文

```text
root_normalization_level = profinite を宣言できるのは、当該 record が次を
すべて満たすときに限る:

  (R1) znorm_seal_id           が実在し、operative な Z-norm-seal を指す;
  (R2) profinite_equality_edge が実在し、
         edge_id = "tb2-canonical-root-equality/profinite-v1"
         scope   = profinite
       であり、その certificate digest が解決できる;
  (R3) 当該 window が Z-norm-seal の window inventory で
         compatibility_status = migrated
       であり、migrated_record_digest が実値で解決できる。

いずれかを欠く record が profinite を宣言した場合は fail-closed で停止する
(既定値へ落とさない)。
```

### 四段との対応(**変更しない**・TB4 導出 v2.4 §8.6a の再掲)

```text
none       -> b_op = 1 only          # 命題 TB4-E(root-link-free)          = L1
mod_M      -> b_cmp = 1              # t_bar_M = 1                          = L2
level_2M   -> epsilon = 1 mod 2M     # (Z_{2M}-link)・定理 TB4-A20           = L3
profinite  -> epsilon = 1            # (Z-norm)・定理 TB4-B                  = L4
```

### 添える注

> **1. `migrated` は昇格ではない。** window inventory の `compatibility_status = migrated` は **root object の同一性**を言うだけで、その window の `root_normalization_level` を `profinite` にはしない。**昇格には (R1)(R2)(R3) の三つが揃うことが要る**(component 2 §5)。
> **2. `level_2M` を宣言した record が $\varepsilon=1$ を主張したら従来どおり fail-closed。** 本条文は逆向き(`profinite` の乱用)を塞ぐもので、既存の順方向 lint を置き換えない。
> **3. `b_semantics="op"` / `b_value_i = b_op_value` は不変**(便 49 F4.3)。`b_cmp_value` は `root_system_tb2_id` を伴う別欄でのみ許す。
> **4. `pending` / `not_assessed` の window は (R3) を満たさない**ので、**seal 発効だけでは `profinite` を宣言できない**($K^{(3)}$・$A_5$ が該当)。

---

## 出所対応表(便 56 P56-1 の 5 欄)

| transfer_mode | source_range | target_range | approval_id | change_summary |
|---|---|---|---|---|
| `adapted` | TB4 導出 v2.4 §0 状態札・§3.3・§8.5・付録 A | P-1 の差し替え表 | 裁定 71(委嘱 4) | 札を `root-normalization-relative paper theorem / A3-framework-conditional` へ。**TB4-A20 は不変**と明記 |
| `verbatim` | TB4 導出 v2.4 §8.2 の A3 seal・★教材 T11 | P-1 の注 2・3 | — | 逐語 |
| `adapted` | TB4 導出 v2.4 §8.6a の enum | P-2 の条文 | 裁定 71(委嘱 5) | `profinite` 宣言の必要条件 (R1)(R2)(R3) を新設。**四段の対応表は再掲のみで変更なし** |
| `normative-only` | component 2 §5 | P-2 の注 1 | — | 「`migrated` $\ne$ 昇格」を再掲 |

---

## 検証欄(**実測値**)

| 項目 | 結果 |
|---|---|
| CR(0x0D)・C0 制御文字・TAB | **0** |
| 本ファイルが他文書を変更していないこと | **変更なし**(パッチ案のみ・適用は司令塔) |
| 状態 | `drafted / unapproved / non-operative` |

```sh
grep -Pc '\r' docs/znorm_apply_patches_v1.md                              # CR = 0
grep -Pc '[\x00-\x08\x0B\x0C\x0E-\x1F]' docs/znorm_apply_patches_v1.md    # C0 = 0
grep -Pc '\t' docs/znorm_apply_patches_v1.md                              # TAB = 0
```
