# `ep-telemetry-sentinel-ops/v1` — bounded decision-lane concordance sentinel の運用規程

2026-08-01 起草: ep-keeper(EP 専任係)。**起点は Sol 便96 P96-2.2**(`sol/sol_reply_96_math23.md`)。

> **本稿の格**: **運用ノート**であり数学的主張ではない。**normative な条項の正本は governing spec `docs/week4-NInfty_stage2_spec_v19.md` §5.3.6**(TS-1〜TS-7)。本稿はそれを運用手順へ落としたものであり、**両者が食い違った場合は spec §5.3.6 が勝つ。**

---

## 0. これは何か・何ではないか

**何か**: positive control が未閉鎖のまま(便96 F96-2.3 item 4 = open)でも Sol が **telemetry-only なら許可**した、有限宇宙上の **bounded decision-lane concordance sentinel**。裁定345 で受領した bounded 744 concordance と**同格**。

**何ではないか**(この 5 行を報告文の冒頭から外してはならない):

1. **EP 発効ではない。** EP は `uncalibrated/UNKNOWN` のまま(便96 F96-2.3)。
2. **calibrated detector ではない。** full-path の感度、特に false negative は測られていない(TS-7)。
3. **NF / W-6 / positive control の代用ではない。** 便95 P95-2.2 の item 3(full witness union)・item 4(positive control)を**閉じない**(TS-5)。
4. **minted / published artifact ではない。** これは **diagnostic construction** であり、mint は NF gate 通過後の provisioning 経路だけが行う(便95 F95-2.3 の用語分離)。
5. **「union PASS」ではない。** full union は現に `INTEGRITY_STOP`(R1/R2 = MALFORMED)。

---

## 1. 事前登録(TS-1)— 走らせる前に固定する

哨戒を 1 本走らせる前に、以下**すべて**を receipt へ書き、以後変更しない。

| 欄 | 内容 |
|---|---|
| `universe.definition` | 有限宇宙の定義(パラメータ域・生成規則) |
| `universe.bound` | 上限(件数・次数・係数域) |
| `universe.enumeration_order` | 列挙順(決定的でなければならない) |
| `input_digest` | 宇宙定義 blob の sha256 |
| `lane_a_code_digest` | `search/ninfty-searcher-v2.mjs` の sha256 |
| `lane_b_code_digest` | `search/ninfty-checker.py` の sha256 |
| `governing_era` | governing spec §5.3.4 の `decision_lane_predicate` plane の era |

**宇宙を後から広げない。絞る場合は silent cap にせず報告する**(工房の事前登録規律)。

---

## 2. 表示規律(TS-2)— 常に付ける札

```json
{
  "artifact_class": "diagnostic",
  "calibrated_detector": false,
  "ep_status": "uncalibrated/UNKNOWN",
  "complete_search": false,
  "finite_universe_exhausted": { "value": true, "scope": "<この有限宇宙のみ>" }
}
```

- `complete_search` は **常に `false`**。有限宇宙を尽くしたことは **別欄** `finite_universe_exhausted` に、**その有限宇宙に限る scope 注記つきで**置く。
- **数学宇宙全体へ外挿しない。**「この範囲に反例なし」は**非存在の証明ではない**。

---

## 3. 不一致の扱い(TS-3)— fail-closed

- lane ごとの `verdict` と `reason_codes[]` **vector** を保存する(overall verdict だけの保存は不可 — 便66 F4.2 と同じ理由)。
- **不一致は即 `INTEGRITY_STOP`。**
- **多数決・片側採用は禁止。** 「lane A が通ったから採る」は許されない。
- **S2 帯の累積規律**(spec §5.3.3 X-1a・便96 W96-2.1)により、両 lane は同一入力に対し**同一の S2 集合**を出すはずである。差が出たらそれ自体が bug 信号であり、`[26]` concordance の対象。

---

## 4. ACCEPT の扱い(TS-4)— hold-for-review 止まり

ACCEPT は **`hold-for-review`** に留める。以下へ**使わない**:

- mint(registry への artifact 発行)
- 候補の採択・棄却
- SURJ / N∞ に関する主張
- **sealed 値への接触**(ALLOWED_N assert を外さない・n=5 立入禁止)

---

## 5. public 面(TS-6)

**件数と状態だけ**を出す。blind / sealed payload を漏らさない。具体的には:

- 出してよい: 走査件数・ACCEPT/REJECT/INTEGRITY_STOP の件数・不一致件数・宇宙の bound。
- 出さない: 個々の候補の係数・sealed 欄・deterministic digest(spec §5.3.2 [10] のリスク型)。

---

## 6. 較正について(TS-7)— 恒久の但し書き

> full-path の感度、特に **false negative** を測った "calibrated detector" と呼ぶには、**盲検注入 positive control がなお必須**である。「自然な positive が存在しない」という**不在論証が将来得られても、それは detector sensitivity の較正を代替しない**。別 campaign の $n=3,\ u=-4$ は N∞ の full-path positive control では**ない**。(便96 P96-2.2 逐語)

**この段落は哨戒 receipt に毎回そのまま同梱する。**

---

## 7. 発火手順

1. 事前登録 receipt を書く(§1)。
2. 司令塔の認可を得る(**哨戒の発火は司令塔の権限**。CI の `workflow_dispatch` も同様)。
3. 走らせ、**exit code と結果 JSON を原文のまま保存**する(exit 0 で失敗を覆わない)。
4. §2 の札と §6 の但し書きを付けて報告する。

---

## 7.9 receipt 引用規約【追記 2026-08-01・Sol 便98 F98-6.1】

**receipt が直接束縛するのは receipt 本文が明記する欄(`suites_status` と各 gate 欄)だけであり、「N checks green」のような手集計値は receipt 本文に含まれない — 検査本数を引用するときは必ず suite log の別 provenance(実行コマンド・log の sha256・実行日時・実行系)を添える**(便98 F98-6.1 逐語)。**exit code を検査本数と読まない。** 条文の正本は **spec v20 draft §5.3.7(RC-1〜RC-4)**であり、**その trio が freeze receipt で発効するまでは本節が運用正本**である(先行して運用してよい — 引用規律を緩める方向の変更ではないため)。

---

## 8. 出所

- Sol 便96 P96-2.2(`sol/sol_reply_96_math23.md`)— 6 条件の原文。
- governing spec `docs/week4-NInfty_stage2_spec_v19.md` §5.3.6 — normative 転記(TS-1〜TS-7)。
- 裁定345 — bounded 744 concordance の受領(同格の先例)。
- Sol 便98 F98-6.1(`sol/sol_reply_98_math25.md`)— §7.9 receipt 引用規約の原文。
