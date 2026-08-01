# `ep-positive-control-design/v2-DRAFT` — full-path positive control(**器のみ先行実装・本走不認可**)

2026-08-01 起草: ep-keeper(EP 専任係)。**起点は Sol 便97 §4(F97-4.1・W97-4.1 の 10 項・P97-4.1)。**

> **本稿の格**: **v1 を supersede する draft。v1(`docs/ep_positive_control_design_draft_v1.md`)は byte 凍結のまま記録として残す**(v1 への追記・訂正はしない)。
> **認可(P97-4.1 逐語)**: harness schema・catalog schema・**非盲検 unit fixture**・commit/reveal/adjudication の scaffolding は**先行実装してよい**。
> **不認可(P97-4.1 逐語)**: secret trial の本走・**F-w6 を含む full-path calibration**・`calibrated_detector=true`・**EP status 変更**。これらは **W-6 gate PASS 後に versioned campaign を再請求**する。
> **EP は `uncalibrated/UNKNOWN` のまま。器の存在は positive control の存在ではない。**

---

## 0. 前版差分(v1 → v2)

| ID | v1 | v2 | 出所 |
|---|---|---|---|
| **A** | §2.1 の見出しが **二役分離**(表は三役) | **三役分離**へ訂正。役は injector / detector / adjudicator | W97-4.1 item 1 |
| **B** | §5 item 1「**盲検注入 vs 不在論証**の採択(継続諮問中)」 | **閉じた。** `calibrated detector` を名乗るには**盲検注入が必要**。不在論証は別の数学結果であり**代替ではない** | W97-4.1 item 2 |
| **C** | receipt 案の `envelope_digest = sha256(封印 envelope)` | **高 entropy nonce を含む HMAC commitment** へ。小さな選択肢集合の digest は**辞書攻撃で注入内容を漏らす** | W97-4.1 item 3 |
| **D** | injector の記録を封印するだけ | **adjudicator が clean base から mutation を replay し、mutated artifact digest を再計算**する。自己申告は証拠でない | W97-4.1 item 4 |
| **E** | 期待検出が `[1]`–`[5]` のような**範囲** | **trial ごとに exact な stage・primary・sealed/public reason vector・exit code を事前封印**。範囲・集合は**拒否** | W97-4.1 item 5 |
| **F** | 注入 trial のみ | **no-injection null trial を混ぜ false positive も測る**。**trial 順序と injection bit を detector から隠す** | W97-4.1 item 6 |
| **G** | 「full path」の定義が曖昧 | **public ingress → schema/digest → registry → 二 lane → W-6 → composition → public receipt** の 8 段を全通過した trial のみ full-path。**内部関数への直接 mutation は unit test** | W97-4.1 item 7 |
| **H** | `F-con` が単一群 | **data-plane one-lane fault と code-plane tamper を別 family** に分割(`F-con-data` / `F-con-code`)。期待 code も別々に固定 | W97-4.1 item 8 |
| **I** | 8 family の被覆を感度と読める書き方 | **有限 catalog の coverage であり一般の false-negative rate ではない**。主張は **`catalog-calibrated under <catalog_digest>`** に限定 | W97-4.1 item 9 |
| **J** | dry run receipt に `undetectable_by_construction:[F-w6]` | **可。ただし最終 full-path calibration receipt と混ぜない** — schema id を分け、**merge 禁止条項**を receipt 自身に書く | W97-4.1 item 10 |

---

## 1. 三役分離(item 1・blind の物理的担保)

| 役 | できること | できないこと |
|---|---|---|
| **injector** | fault catalog から 1 件を選び genuine fixture へ適用し、注入済み artifact 束を作る。選択と適用を**封印 commitment** へ束縛する | pipeline を走らせない・判定に関与しない |
| **detector**(被験側 = EP pipeline) | 与えられた artifact 束を通常経路で処理し verdict / reason vector を出す | **封印を読まない・注入の有無・順序・期待値を知らない** |
| **adjudicator** | run 完了後に封印を開き、**mutation を clean base から replay** して注入を確認し、注入 ⇔ 検出の対応表を作る | 注入も検出もしない |

**blind の担保は規範でなく物理**: 封印 key と envelope は**リポジトリ外の金庫**に置き、**detector の作業木・context から到達不能**にする。三役の人/セッション・code digest・dependency closure・read/write ACL を receipt に記録する(P97-4.1)。**adjudication 後も秘密値そのものを public 面へ出さない。**

---

## 2. 封印 commitment(item 3・P97-4.1 逐語)

```text
HMAC_K(canonical({
  campaign_id, trial_id, catalog_digest, base_artifact_digest,
  mutation_id, mutation_parameters, mutated_artifact_digest,
  exact_expected_vector, null_or_injected, nonce
}))
```

- **`K` と envelope は detector から到達不能。**
- **10 欄すべて必須**(欠けた欄は「束縛したつもり」になる)。実装は欠落を**例外で拒否**する。
- **nonce は CSPRNG 由来の高 entropy**。小さな選択肢集合の sha256 は不可(item 3)。

---

## 3. 注入 catalog(item 8 の分割を反映)

| family | plane | 注入点 | 期待検出 |
|---|---|---|---|
| `F-pre` | data | precondition(degree / monic / squarefree / leading coeff / Pell) | REJECT `[1]`–`[5]` |
| `F-thm` | data | 定理強制恒等式(E-6 の gcd /(Or)/(60.5)) | INTEGRITY `[13]`/`[14]`/`[15]` |
| `F-att` | data | E-5 attestation と導出値の矛盾 | `[27]`(発火縁)/ attestation 欠落は非発火縁 |
| `F-nat` | data | native の finite partition / branch count / harmonicity | `[22]`–`[24]` |
| `F-w6` | data | ramification → branch incidence の入替 | **W-6 FAIL — W-6 未閉鎖の間は検出不能**(§5) |
| `F-nf` | data | NF の N-1〜N-5 / total degree / infinity / non-ramification | R3-NF FAIL |
| `F-reg` | data | registry 世代 / freeze / four-role / era | 四 role 非 PASS / `payload_era_matrix` FAIL |
| **`F-con-data`** | data | **片 lane の data のみ**を壊す | `[26]` concordance |
| **`F-con-code`** | **code** | **片 lane の code を改竄** | **code-digest gate `[12]`** — これは data-plane 感度とは**別の主張** |

**両縁必須**: 各 fault について**発火側と非発火側**の対を張る。

---

## 4. full path の定義(item 7)

```text
public_ingress -> schema_and_digest -> registry_resolution -> lane_a
   -> lane_b -> w6 -> composition -> public_receipt
```

**この 8 段を全通過した trial のみ full-path。**内部関数への直接 mutation は unit test であり full-path control に数えない。**経路が記録されていない trial は full-path でない**(fail-closed)。

---

## 5. 先に潰さないと成り立たない依存(不変・v1 §4 を維持)

**W-6 が閉じていないと `F-w6` は構造的に false negative になる。**便96 W96-2.3 のとおり R3-NF は incidence を忘れ、現 R1/R2 は genuine fixture に対し `MALFORMED` で W-6 述語が評価されていない。この状態で走らせると **「detector の感度が低い」ではなく「その経路が存在しない」**という別の事実を測る。

**順序: W-6 閉鎖 → positive control 本走。** 事前に走らせる場合は **dry-run receipt**(別 schema)に `undetectable_by_construction:["F-w6"]` を明示し、**感度の主張から除外**する。**dry-run receipt を最終 calibration receipt と混ぜてはならない**(item 10)。

---

## 6. 主張の格(item 9)

較正が成立しても、主張できるのは

```text
catalog-calibrated under <catalog_digest>
```

であり、**一般の false-negative rate ではない**。一般の rate を主張するには **sampling distribution と trial 数の事前登録**が要る。

---

## 7. 実装状態

| 部分 | 状態 |
|---|---|
| harness schema・catalog schema・commit/reveal/adjudication scaffolding | **実装済**(`search/ninfty-ep-poscontrol-harness.py`) |
| 非盲検 unit fixture(item 1–10 の 1:1 検査) | **実装済**(`search/test_ninfty_poscontrol.py`) |
| secret trial 本走・full-path calibration・`calibrated_detector=true`・EP 発効 | **不認可 — code が実行時に拒否**(`run_blind_campaign` は `NotAuthorised` を送出) |
| 封印 key / envelope の金庫配置と到達不能性の機械的担保 | **未着手**(所在は司令塔の職掌) |
| injector 役を誰が務めるか(別セッション/外部) | **未決 — 司令塔へ** |

---

## 8. 出所

- Sol 便97 §4(`sol/sol_reply_97_math24.md`)・便96 P96-2.2 / F96-2.3 item 4・便95 P95-2.2 item 4。
- v1: `docs/ep_positive_control_design_draft_v1.md`(**byte 凍結・記録**)。
