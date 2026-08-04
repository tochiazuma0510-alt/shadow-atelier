# 「1210」provenance 束縛 **v2** 草案(DRAFT・未発効・未実装)— 便 103 F103-6.4 条件の反映

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED / 未実装**。**凍結 artifact・既存 receipt・既存 CI workflow は一切触っていない。**
> - **前版 `docs/notes/ep_suitelog_provenance_binding_v1_draft.md`(v1)は byte 不変で保存**(versioned supersede)。
> - 由来: **便 103 F103-6.4** — 「**設計方向は条件付き PASS**」。Sol は保存 log(SHA-256 `7d15896dc94d083cea66ceb795c4ee90e32c4b25d4a133bcb68cc5679c622030`)から 44/50/194/228/51/117/285/48/93/47/53 = **1210** を独立に再計数した(工房側の実測と一致)。ただし**条件 4 群**が付いた。
> - ★ **現時点で「1210」を恒久札として引用する認可は出ていない**(便 103 逐語)。**S-1〜S-3 と negative fixture の実物を Sol が再監査してから**である。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**EP は引き続き `uncalibrated/UNKNOWN`。**

---

## 1. v1 → v2 の変更点(**すべて便 103 F103-6.4 由来**)

| # | v1 | v2 |
|---|---|---|
| **v2-1** | S-3 が **単一の** `exec_command` / `executed_at` / `execution_env` を持つ | ★ **9 CI suite と 2 local selfaudit は実行 provenance が異なる。** 単一の command/time/env を 11 本へ**流用しない**。**suite または execution batch ごと**に command・time・environment・**commit/code digest**・**exit code** を拘束 |
| **v2-2** | 歴史 log をそのまま S-1 にする前提 | ★ **command/time/env が回収不能なら推測で埋めない。** **登録 wrapper で再走して新 S-1 を発行**する |
| **v2-3** | claim = 「この log に記録された 11 suite の**自己申告本数**の合計は 1210」 | ★ claim = 「**この log の登録抽出規則による 11 section の計数が 1210**」。「11 suite の自己申告 total」とも「1210 検査の内容を本 receipt が保証」とも**書かない** |
| **v2-4** | 末尾 47/53 を「PASS 行計数(既知例外)」とだけ | ★ **47/53 は selfaudit v11/v12 の `PASS \|` 行数であって suite の自己申告 total ではない**ことを **cert の欄として明示**。**意図的 `FAIL \| META-1` 各 1 本を除外する規則も claim の一部**として書く |
| **v2-5** | fail-closed 縁が 5 項目 | ★ **section 名・重複・footer・exit contract・raw byte encoding・suite code/version・意図的 FAIL の増減**を fail-closed に(§4) |

---

## 2. claim の正確な文(**§2 が本書の核心**)

### 2.1 書いてよい唯一の文

> **「保存 log `<path>`(SHA-256 `<64hex>`)に対し、S-2 に登録された抽出規則を適用したとき、11 section の計数の合計は 1210 である。」**

### 2.2 書いてはならない文(**逐語で禁止**)

| 禁止文 | なぜ |
|---|---|
| ~~「11 suite の**自己申告 total** の合計が 1210」~~ | **末尾 2 section(selfaudit v11/v12)は自己申告 total を持たない**。47/53 は `PASS \|` **行数**である |
| ~~「1210 検査の**内容**を本 receipt が保証する」~~ | 本 cert が保証するのは**転記と集計**。検査の中身ではない |
| ~~「FAIL は 0 だった」~~ | **意図的 `FAIL \| META-1` が各 1 本・計 2 本ある**。除外規則は claim の一部 |
| ~~「11 suite が CI で走った」~~ | **CI receipt が束縛するのは 9 suite**。selfaudit 2 本は**ローカル実行**(§3.1) |
| ~~「1210 本 green ゆえ EP は健全」~~ | **本数は較正ではない**。**EP=uncalibrated/UNKNOWN** は不動 |
| ~~「green workflow = green test」~~ | 鉄則 2 |

### 2.3 section の内訳(**機械集計・手写しなし**・Sol と工房で独立に一致)

| # | section | 計数 | 抽出形式 | ★ 種別 |
|---|---|---|---|---|
| 1 | `test_ninfty_nf` | 44 | `N checks, M FAIL` | 自己申告 total |
| 2 | `test_ninfty_checker_native` | 50 | `N/N checks passed.` | 自己申告 total |
| 3 | `test_ninfty_laneB` | 194 | `N/N checks passed.` | 自己申告 total |
| 4 | `test_ninfty_evidence_union` | 228 | `N/N checks passed.` | 自己申告 total |
| 5 | `test_ninfty_legacy_normalizer` | 51 | `N/N checks passed.` | 自己申告 total |
| 6 | `test_ninfty_r3nf` | 117 | `N checks, M FAIL` | 自己申告 total |
| 7 | `test_ninfty_w6key` | 285 | `N checks, M FAIL` | 自己申告 total |
| 8 | `test_ninfty_poscontrol` | 48 | `N checks, M FAIL` | 自己申告 total |
| 9 | `ninfty-selftest-lanea.mjs` | 93 | `=== summary: N/N passed ===` | 自己申告 total |
| 10 | `bundle_selfaudit_v11` | 47 | ★ **`PASS \|` 行数**(自己申告 total 無し) | **行計数**・意図的 `FAIL \| META-1` 1 本を除外 |
| 11 | `bundle_selfaudit_v12` | 53 | ★ **`PASS \|` 行数**(自己申告 total 無し) | **行計数**・意図的 `FAIL \| META-1` 1 本を除外 |
| — | **合計** | **1210** | — | **9 自己申告 + 2 行計数の混成**(この混成自体が claim の一部) |

> ★ **v1 で報告した参考値の再掲**: PASS 行の素朴な総数 193 / `N checks` 行の総和 494 / 単純和 687。**いずれも 1210 ではない。** ⟹ **集計規則そのものが provenance の一部**である。

---

## 3. S-1 / S-2 / S-3(**v2**)

### 3.1 ★ 実行 provenance の分離(**v2-1**)

**9 CI suite と 2 local selfaudit は実行系が違う。** 単一 batch として扱わない。

```jsonc
"execution_batches": [
  { "batch_id": "ci-9-suites",
    "sections": ["test_ninfty_nf", "…", "ninfty-selftest-lanea.mjs"],
    "command":      "<逐語>",
    "executed_at":  "<ISO8601 UTC>",
    "environment":  { "runner": "github-actions/…", "os": "…", "python": "…", "node": "…" },
    "commit_sha":   "<40hex>",
    "code_digests": [ { "path": "search/test_ninfty_nf.py", "sha256": "<64hex>" }, … ],
    "exit_code":    0,
    "ci_receipt_binding": { "path": "search/certs/ep_ci_receipt_run….json", "sha256": "<64hex>",
                            "run_id": "…" } },
  { "batch_id": "local-selfaudit",
    "sections": ["bundle_selfaudit_v11", "bundle_selfaudit_v12"],
    "command":      "<逐語>",
    "executed_at":  "<ISO8601 UTC>",
    "environment":  { "runner": "local", "os": "…", "python": "…" },
    "commit_sha":   "<40hex>",
    "code_digests": [ { "path": "search/bundle-selfaudit-v11.py", "sha256": "<64hex>" },
                      { "path": "search/bundle-selfaudit-v12.py", "sha256": "<64hex>" } ],
    "exit_code":    0 }
]
```

- **batch が 1 つしかない S-3 は MALFORMED**(11 本を一括りにした過去の書き方を再演させない)。
- 各 section は**ちょうど 1 つの batch に属する**(所属無し・重複所属は STOP)。

### 3.2 ★ 歴史 log の扱い(**v2-2**)

現行 `scratchpad/ep_suites_20260802_ben100.log`(SHA-256 `7d15896d…22030`)は、**command / executed_at / environment / exit_code が回収不能**である。

- ⟹ **推測で埋めない。** この log から S-3 を発行**しない**。
- ⟹ **登録 wrapper**(`ops/bin/run_ep_suites_v1.ps1`(仮)= command・time・env・commit・exit code を自ら記録して log を吐く)で **再走**し、**新しい S-1** を `provenance/suite_logs/` へ発行する。
- 歴史 log は **参考資料**として残してよいが、**恒久記帳の source にしない**。
- ★ **再走で総数が 1210 と変わりうる**(suite が増減していれば当然変わる)。**「1210 を再現すること」を目標にしない** — 期待値を先に置くのは較正の逆(鉄則 5)。**出た数をそのまま記帳する。**

### 3.3 三点セット(v1 から不変・要件のみ更新)

| # | 成果物 | 更新点 |
|---|---|---|
| **S-1** | `provenance/suite_logs/ep_suites_<YYYYMMDD>_<tag>.log` | ★ **登録 wrapper の出力**であること。以後 byte 不変 |
| **S-2** | `search/ep_suitelog_tally_v1.py` | ★ 抽出規則を**登録表**として持ち、**section 種別(自己申告 total / 行計数)を出力へ明記** |
| **S-3** | `search/certs/ep_suitelog_receipt_<YYYYMMDD>.json` | ★ `execution_batches`(§3.1)+ `claim_text`(§2.1 の逐語)+ `forbidden_claims`(§2.2)を持つ |

---

## 4. ★ fail-closed の縁(**v2-5**・便 103 の列挙を全採録)

| # | 縁 | 挙動 |
|---|---|---|
| 1 | **section 名** | 事前登録された 11 section 名と**厳密一致**。未知名は **STOP**(PASS 行計数へ黙って fallback しない) |
| 2 | **重複** | 同一 section が 2 回現れたら **STOP**(再走ログの連結を黙って合算しない) |
| 3 | **欠落** | 11 section に**過不足があれば STOP**(1 本落ちても総数が減るだけ、を塞ぐ) |
| 4 | **footer** | 各 section の footer(自己申告 total 行)が**期待形式で存在しない**場合、**種別が「行計数」として事前登録された section 以外は STOP** |
| 5 | **exit contract** | 各 batch の `exit_code` が事前登録値と違えば **STOP**。**exit 0 で失敗を覆う型を塞ぐ** |
| 6 | **raw byte encoding** | log の bytes を**そのまま**hash。デコード不能 byte は**置換して読み飛ばさない**(置換が起きたら STOP)。改行コードの正規化も禁止 |
| 7 | **suite code / version** | `code_digests` が事前登録と食い違えば **STOP**(同じ section 名で別の code が走った、を塞ぐ) |
| 8 | **意図的 FAIL の増減** | `FAIL \| META-1` の期待件数を **section ごとに事前登録**し、**増えても減っても STOP**。「意図的 FAIL だから無視」を無条件にしない |
| 9 | **未知形式** | 5 抽出形式のいずれにも当たらない footer は **STOP**(規則の穴を 0 本や推測値で埋めない) |
| 10 | **log digest** | S-3 発行時と検証時の双方で S-1 の bytes を再計算。不一致は **STOP** |

### 4.1 negative fixture(**両縁**)

**発火側**: ① 総数行の改竄 / ② section を 1 本削除 / ③ section の重複 / ④ `META-1` 行を 1 本増加 / ⑤ 同 1 本減少 / ⑥ 未知形式 section の追加(**STOP であって 0 本 fallback でない**)/ ⑦ `exit_code` 改竄 / ⑧ `code_digests` 改竄 / ⑨ batch を 1 つに潰す。
**非発火側**: ⑩ 正規 log(**PASS**)/ ⑪ 意図的 `FAIL \| META-1` が**期待どおり各 1 本**ある log(**発火しない**— これが無いと「FAIL があれば必ず止まる」過剰発火と区別できない)。

---

## 5. checker v3 / cert v5 束との整合(v1 から継承・v1.7-r2 へ追従)

| 論点 | 整合 |
|---|---|
| **digest 必須位置の構造的列挙** | S-3 の必須位置 = `suite_log` / `tally_rule` / 各 `execution_batches[i].code_digests[j]` / `ci_receipt_binding` / `effective_source(_chain)`。**「発見した digest」でなく「schema 上必須の位置」から列挙**(便 102 F102-4.1 の型を最初から塞ぐ) |
| **XOR / missing-both** | 各必須位置は `sha256` と `sha256_ref` の**ちょうど一方**(規範 11)。**欄ごと落とした S-3 が素通りしない**ことを fixture で固定 |
| **台帳 pin** | ★ **台帳 v1.7-r2 §D-3′ の二層化に従う** — `conformance_at_issue`(発行時適合の**不変** digest)と `compatibility_check`(現在版との照合・**checker の出力**)を分離。**無関係な台帳追記で過去の S-3 を遡及失効させない** |
| **checker 実装** | `ihnec_r4b_selfhash_checker_v3.py` の `enumerate_required_digest_positions()` / `check_xor()` の**設計を移植**(コード共有ではなく設計共有。EP 側は独立実装) |
| **格の分離** | 「suite log の**転記**が正しい」と「suite の**検査**が正しい」を分けて書く(§2) |

---

## 6. 実装順序(**認可後**・片方だけ先行させない)

1. 登録 wrapper の実装 → 2. **再走して新 S-1 を発行**(§3.2)→ 3. S-2(抽出規則登録表 + negative fixture 11 種)→ 4. S-3(cert 発行)→ 5. Sol 再監査 → 6. **認可が出て初めて**恒久記帳側で数を引用し、**S-3 の path + SHA-256 を必ず併記**する。

**CI workflow は変更しない**(receipt が本数を書かない設計は正しい)。**発火依頼も不要。**

---

## 7. 発効しないもの(明示)

- **本書そのもの**(S-1/S-2/S-3・登録 wrapper はいずれも**未実装**)。
- ★ **「1210」の恒久札としての引用**(便 103 で**認可は出ていない**)。S-3 と negative fixture の実物を Sol が再監査するまで、**便・LEDGER・地図で 1210 を無条件に引用しない**。
- **EP の札**: `EP=uncalibrated・UNKNOWN` は不動。**本数は較正ではない。**
