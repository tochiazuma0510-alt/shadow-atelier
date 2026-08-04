# 「1210」恒久記帳の provenance 束縛 v1 **草案(DRAFT・未発効・未実装)** — 便 101 W101-4.1 への回答形

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED / 未実装**。**凍結 artifact・既存 receipt・既存 CI workflow は一切触っていない。**
> - 由来: **便 101 W101-4.1**(逐語)— 「CI receipt 自身が束縛するのは 9 suite の `suites_status=0` であり、**検査本数 1210 は意図的に receipt に含まれない**。RC-2 に従い、**1210 を恒久記帳で引用するなら suite log の versioned path、SHA-256、実行コマンド、日時・実行系を別 provenance として束縛すること**。これは M-7 修理の合否を変えない NOTE である。」
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**発効判定は司令塔 + Sol の専権。**
> - **checker v3 / cert v5 束(裁定 492 検収済)との整合**: §4。台帳 v1.7 草案 = `docs/notes/conventions_ledger_v1_7_draft.md`。

---

## 1. 問題の正確な形(**receipt は無罪**)

現行 CI receipt(例 `search/certs/ep_ci_receipt_run30729135900.json`)は、**自分が本数を書かない理由を自分の `note` に明記している**(逐語):

> The per-suite check counts are in `ci/out/suites.log`, which each suite prints itself; they are not restated here, because **a hand-restated total is exactly the kind of claim a receipt must not carry**.

これは正しい設計である。**壊れているのは receipt ではなく、「1210」という数を恒久記帳(便・LEDGER・地図)へ持ち出す側**である。現状 1210 は、

1. **どの log から** 出た数か、
2. **どの規則で** 集計した数か、

のどちらも束縛されていない。**とくに 2 が致命的**である(§2)。

---

## 2. ★ 本作業で判明した事実 — **「1210」は素朴な規則では再現しない**

保存 log `scratchpad/ep_suites_20260802_ben100.log` に対する機械実測(本草案起草時):

```
PASS 行の素朴な総数            : 193
"N checks, 0 FAIL" 行の総和    : 494
両者の単純和                   : 687      <-- 1210 ではない
```

**11 suite はそれぞれ別の形式で自分の本数を印字している**(5 形式)。suite ごとに正しい抽出規則を当てて初めて 1210 が出る:

| suite | 本数 | 抽出形式 |
|---|---|---|
| `test_ninfty_nf` | 44 | `N checks, M FAIL` |
| `test_ninfty_checker_native` | 50 | `N/N checks passed.` |
| `test_ninfty_laneB` | 194 | `N/N checks passed.` |
| `test_ninfty_evidence_union` | 228 | `N/N checks passed.` |
| `test_ninfty_legacy_normalizer` | 51 | `N/N checks passed.` |
| `test_ninfty_r3nf` | 117 | `N checks, M FAIL` |
| `test_ninfty_w6key` | 285 | `N checks, M FAIL` |
| `test_ninfty_poscontrol` | 48 | `N checks, M FAIL` |
| `ninfty-selftest-lanea.mjs` | 93 | `=== summary: N/N passed ===` |
| `bundle-selfaudit-v11` | 47 | **自己申告の総数行を持たない** ⟹ PASS 行計数 |
| `bundle-selfaudit-v12` | 53 | **自己申告の総数行を持たない** ⟹ PASS 行計数 |
| **合計** | **1210** | (機械集計・手写しなし) |

`FAIL | META-1` 行は selfaudit v11/v12 に **各 1 行**(計 2 行)。**意図的 false が footer/exit contract へ伝播することを検査する fixture** であり、suite verdict は exit 0 — Sol の記述と一致する。

⟹ **結論**: 1210 は「log の digest を貼れば足りる数」**ではない**。**集計規則そのものが provenance の一部**である。規則を持たずに log digest だけを貼ると、「同じ log から別の数が出る」余地が残り、RC-2 の要求を満たさない。

---

## 3. 提案 — **suite-log receipt** を別 provenance artifact として発行する

### 3.1 三点セット(**片方だけ先行させない**)

| # | 成果物 | 役割 |
|---|---|---|
| **S-1** | **versioned suite log**: `provenance/suite_logs/ep_suites_<YYYYMMDD>_<tag>.log` | 現在 `scratchpad/`(**未追跡**)にある log を **versioned path へ置く**。以後 **byte 不変**(修正は新 log の発行のみ) |
| **S-2** | **集計器**: `search/ep_suitelog_tally_v1.py` | log の bytes だけを入力に、§2 の per-suite 抽出規則で本数を再導出し、**cert を機械生成**する。**手写し禁止**。log を import しない・suite を再実行しない(**照合器であって実行器ではない**) |
| **S-3** | **cert**: `search/certs/ep_suitelog_receipt_<YYYYMMDD>.json` | S-1 と S-2 と CI receipt を **digest で相互束縛**した恒久記帳用 artifact |

### 3.2 S-3 が束縛する欄(**RC-2 の 4 要求 + 3 追加**)

```jsonc
{
  "schema": "ep-suitelog-receipt/v1",
  // --- RC-2 が明示的に要求した 4 点 ---
  "suite_log":      { "path": "provenance/suite_logs/…log", "sha256": "<64hex>" },  // ① versioned path + ② SHA-256
  "exec_command":   "…",                                                            // ③ 実行コマンド(逐語)
  "executed_at":    "2026-08-__T__:__:__Z",                                         // ④ 日時
  "execution_env":  { "platform": "…", "python": "…", "node": "…", "gap": "n/a" },  // ④ 実行系
  // --- 追加 3 点(§2 の発見に基づく) ---
  "tally_rule":     { "script": "search/ep_suitelog_tally_v1.py", "sha256": "<64hex>",
                      "per_suite_extraction": [ { "suite": "…", "format": "…" } ] }, // ⑤ 集計規則の束縛
  "per_suite":      [ { "suite": "…", "checks": 0, "extraction": "…" } ],            // ⑥ 内訳(総数だけを貼らない)
  "total_checks":   1210,                                                            // 機械生成
  "intentional_fail_lines": [ { "suite": "bundle_selfaudit_v11", "tag": "META-1", "count": 1 } ],
  "ci_receipt_binding": { "path": "search/certs/ep_ci_receipt_run…json", "sha256": "<64hex>",
                          "run_id": "…", "commit_sha": "…" },                        // ⑦ CI receipt との対応
  "conventions_used": { "ledger_version": "conventions_ledger_v1_6", … }             // 台帳 CV-10 準拠
}
```

### 3.3 ★ 用語規律(**この cert が主張してよいこと・いけないこと**)

| 書いてよい | 書いてはならない |
|---|---|
| 「**この log に記録された 11 suite の自己申告本数の合計は 1210 である**」 | ~~「1210 本の検査が PASS したことを本 cert が保証する」~~ — 本 cert が保証するのは**転記と集計**であって、**検査の中身ではない** |
| 「`suites_status=0` は CI receipt が束縛する」 | ~~「green workflow = green test」~~(鉄則 2) |
| 「`FAIL \| META-1` 2 行は意図的 fixture である」 | ~~「FAIL が 0 だった」~~ — 実際には**意図的 FAIL 行が 2 行ある** |
| 「11 suite = 9 regression suite + selfaudit v11/v12」 | ~~「11 suite が CI で走った」~~ — **CI receipt が束縛するのは 9 suite** である。selfaudit 2 本はローカル実行 |
| **EP=uncalibrated/UNKNOWN**(不動) | ~~「1210 本 green ゆえ EP は健全」~~ — 本数は較正ではない |

### 3.4 fail-closed 設計(S-2 の要件)

1. **未知形式で止まる**: §2 の 5 形式のいずれにも一致しない suite 見出しに出会ったら **PASS 行計数へ黙って fallback しない** — **`INTEGRITY_STOP`** を出す(規則の穴を「0 本」や「推測値」で埋めない)。selfaudit v11/v12 の PASS 行計数は**明示的に列挙された既知例外**としてのみ許す。
2. **事前登録された suite 集合**: 11 suite の名前を S-2 に**事前登録**し、log 中に**過不足があれば STOP**(suite が 1 本落ちても総数が減るだけで警報が出ない、という型を塞ぐ)。
3. **意図的 FAIL の両縁**: `FAIL | META-1` は **期待される件数を事前登録**し、**増えても減っても STOP**。「意図的 FAIL だから無視」を無条件にしない。
4. **log digest の再計算**: S-3 発行時と検証時の双方で S-1 の bytes を再計算し、不一致は STOP。
5. **negative fixture(両縁)**: ① 総数行を改竄した log(**発火側**)② 正規 log(**非発火側**)③ suite を 1 本削った log(発火)④ `META-1` 行を 1 本増やした log(発火)⑤ 未知形式の suite を足した log(**STOP であって 0 本 fallback でない**)。

---

## 4. checker v3 / cert v5 束(裁定 492 検収済)との整合

| 論点 | 整合のとり方 |
|---|---|
| **CV-10 / 台帳 v1.6 準拠** | S-3 は `conventions_used` を持ち、`ledger_version = conventions_ledger_v1_6` を宣言する。**cert v5 が導入した `ledger_artifact_pin` と同じ流儀**で live 台帳へ digest 束縛する(規範化は未決 = 台帳 v1.7 草案 §D-3) |
| **digest 必須位置の構造的列挙** | S-3 の digest 必須位置は **`suite_log` / `tally_rule` / `ci_receipt_binding` / `effective_source(_chain)`**。checker は **「発見した digest」でなく「schema 上必須の位置」から列挙**する(便 102 F102-4.1 と同型の穴を最初から塞ぐ) |
| **XOR / missing-both** | 各必須位置は `sha256` と `sha256_ref` の**ちょうど一方**(規範 11)。**欄ごと落とした S-3 が素通りしない**ことを negative fixture で固定 |
| **checker の再利用** | `search/probe/wac_v1/ihnec_r4b_selfhash_checker_v3.py` の **`enumerate_required_digest_positions()` と `check_xor()` の設計をそのまま移植**する(コードの共有ではなく**設計の共有**。EP 側 checker は独立実装として書く) |
| **格の分離** | 「registry 層 PASS」と「full union PASS」を区別する既存規律と同じく、**「suite log の転記が正しい」と「suite の検査が正しい」を分けて書く**(§3.3) |

---

## 5. 実装順序(**認可後**・片方だけ先行させない)

1. S-1(log の versioned 化)→ 2. S-2(集計器 + negative fixture 5 種)→ 3. S-3(cert 発行)→ 4. 恒久記帳側(便・LEDGER・地図)の「1210」に **S-3 の path + SHA-256 を併記**する。
5. 以後、**S-3 を伴わない「1210」の引用を禁止**する(machine-piped 規律の suite log 版)。

**CI workflow の変更は本案に含まない**(receipt が本数を書かない設計は正しいので変えない)。**発火依頼も不要**。

---

## 6. 発効しないもの(明示)

- **本書そのもの**(S-1/S-2/S-3 はいずれも**未実装**)。
- **「1210」の恒久記帳**(S-3 が発行されるまで、便・LEDGER・地図で 1210 を**無条件に引用しない**)。
- **EP の札**: `EP=uncalibrated・UNKNOWN` は不動。**本数は較正ではない。**
