# `ep-positive-control-design/v1-DRAFT` — full-path positive control の設計案(**未着工・実装認可待ち**)

2026-08-01 起草: ep-keeper(EP 専任係)。**起点は Sol 便96 F96-2.3 item 4 / P96-2.2 末尾。**

> **本稿の格**: **設計案のみ。実装は司令塔認可 + Sol ゲート後。**
> **採否が未決の設計判断**(盲検注入 vs 不在論証)は**継続諮問中**であり、本稿はそれを決めない — **盲検注入を採る場合に何を作ることになるか**を先に書き出したものである。
> **本稿の存在は positive control の存在ではない。** EP は `uncalibrated/UNKNOWN` のまま。

---

## 1. 便96 が閉鎖条件として specified したこと

Sol 便96 から機械的に読み取れる要件は次の 4 点である(P96-2.2 末尾・F96-2.3 item 4)。

| # | 要件 | 逐語根拠 |
|---|---|---|
| **PC-1** | **測る対象は full-path の感度**、とりわけ **false negative**。 | 「full-path の感度、特に false negative を測った『calibrated detector』と呼ぶには」 |
| **PC-2** | **盲検注入**(blind injection)であること。 | 「盲検注入 positive control がなお必須である」 |
| **PC-3** | **不在論証は代替にならない。** 「自然な positive が存在しない」を将来証明できても、それで PC-1 は満たされない。 | 「不在論証が将来得られても、それは detector sensitivity の較正を代替しない」 |
| **PC-4** | **他 campaign の positive を流用できない。** $n=3,\ u=-4$ は N∞ の full-path positive control ではない。 | 「別 campaign の $n=3,\ u=-4$ は N∞ の full-path positive control ではない」 |

**帰結**: 閉鎖には「**N∞ の full path に、正解を知らない側が検出できるか**を測る器」が要る。**器そのものは、注入内容の設計とは独立に作れる** — 以下はその器の設計案である。

---

## 2. 器の設計(実装可能な部分)

### 2.1 二役分離(blind の物理的担保)

| 役 | できること | できないこと |
|---|---|---|
| **injector**(注入者) | fault カタログから 1 件を選び、genuine fixture へ適用して **注入済み artifact 束**を作る。選択と適用の記録を **封印 envelope** へ書く | pipeline を走らせない・判定に関与しない |
| **detector**(被験側 = EP pipeline) | 与えられた artifact 束を通常経路で処理し、verdict / reason vector を出す | 封印 envelope を読まない・注入の有無を知らない |
| **adjudicator**(照合者) | run 完了後に封印を開き、**注入 ⇔ 検出**の対応表を作る | 注入も検出もしない |

**blind の担保は規範ではなく物理**(工房の配置図規律): 封印 envelope は **リポジトリ外の金庫**に置き、detector が走る作業木からは到達不能にする。**pipeline の source にも fixture にも「正解値」を書かない**(較正は fixture 経由・鉄則5)。

### 2.2 注入カタログ(全経路をまたぐこと = full-path)

各 fault は「**どの check が捕まえるべきか**」を宣言する。宣言と実際の検出の差が **false negative**。

| 群 | 注入点 | 期待検出 |
|---|---|---|
| **F-pre** | precondition(degree / monic / squarefree / leading coeff / Pell) | REJECT `[1]`–`[5]` |
| **F-thm** | 定理強制恒等式(E-6 の gcd / (Or) / (60.5)) | INTEGRITY `[13]` / `[14]` / `[15]` |
| **F-att** | E-5 attestation を導出値と矛盾させる | INTEGRITY `[27]`(発火縁)/ attestation 欠落は**無反応**(非発火縁) |
| **F-nat** | native の finite partition / branch count / harmonicity | `[22]`–`[24]` |
| **F-w6** | **ramification → branch の incidence を入れ替える**(便96 W96-2.3 の★最小反例の型) | **W-6 FAIL** — **現状は検出不能**(§4) |
| **F-nf** | NF の N-1〜N-5 / total degree / infinity / non-ramification | R3-NF FAIL |
| **F-reg** | registry 世代・freeze・four-role・era | 四 role 非 PASS / `payload_era_matrix` FAIL |
| **F-con** | 片 lane だけを壊す(cross-lane 不一致) | `[26]` concordance |

**両縁必須**: 各 fault について**発火側と非発火側**の対を張る(既に `[27]` で実施済みの型を全群へ広げる)。

### 2.3 出力(receipt schema 案)

```json
{
  "schema_id": "mb/ninfty-ep-positive-control/v1",
  "blind": true,
  "envelope_digest": "<封印 envelope の sha256(中身は書かない)>",
  "trials": [{"trial_id": "...", "detector_verdict": "...", "detector_reason_vector": ["..."]}],
  "adjudication": {
    "true_positive": 0, "false_negative": 0, "false_positive": 0, "true_negative": 0,
    "per_fault_group": {"F-pre": {...}, "...": {}},
    "undetectable_by_construction": ["F-w6"]
  },
  "calibrated_detector": false,
  "ep_status": "uncalibrated/UNKNOWN"
}
```

**`calibrated_detector` は adjudication 完了かつ Sol ゲート通過まで `false` 固定。**器が動いただけでは札は変わらない。

---

## 3. 実装可能な部分 / 不可能な部分の切り分け

| 部分 | 状態 |
|---|---|
| 二役分離の器・封印 envelope・trial runner・adjudicator | **実装可能**(認可待ち) |
| F-pre / F-thm / F-att / F-nat / F-nf / F-reg / F-con の注入子 | **実装可能**(認可待ち) |
| **F-w6 の注入子** | **実装しても検出不能** — §4 |
| 「盲検注入 vs 不在論証」の採択 | **継続諮問中・係の一存で決めない** |

---

## 4. 先に潰さないと positive control が成り立たない依存

**W-6 が閉じていないと、F-w6 群は構造的に false negative になる。**

便96 W96-2.3 のとおり R3-NF は incidence を忘れるので、incidence を入れ替えた注入は NF 側で**必ず**素通りする。かつ現在 R1/R2 は genuine fixture に対して `MALFORMED` であり、W-6 述語がそもそも評価されていない。**この状態で positive control を走らせると、F-w6 の false negative は「detector の感度が低い」ではなく「その経路が存在しない」という別の事実を測ってしまう。**

**よって順序は: W-6(option (a) / `UNKNOWN W6-KEY`)の閉鎖 → positive control 本走。** それ以前に走らせる場合は、**F-w6 群を `undetectable_by_construction` として receipt に明示**し、感度の主張から除外する(そして「full-path の較正」とは呼べない)。

---

## 5. 未決事項(司令塔・Sol へ)

1. **盲検注入 vs 不在論証**の採択(継続諮問中)。
2. injector 役を**誰が務めるか**(別セッションの係か、外部か)。同一 context 内で injector と detector を兼ねると blind が名目化する。
3. **封印 envelope の所在**(金庫のどこ)と、run 中に到達不能であることの機械的担保方法。
4. W-6 閉鎖前に器だけ先行実装してよいか(§4 の順序)。

---

## 6. 出所

- Sol 便96 P96-2.2 末尾・F96-2.3 item 4(`sol/sol_reply_96_math23.md`)。
- governing spec `docs/week4-NInfty_stage2_spec_v19.md` §5.3.5(W-6)・§5.3.6(telemetry)。
- 便95 P95-2.2 item 4(positive control が open であること)。
