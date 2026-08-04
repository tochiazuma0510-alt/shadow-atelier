# 規約台帳 v1.7 **草案(DRAFT・未発効)** — 便 102 F102-4.1 の履行

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED**。**live 正本は依然 `docs/notes/conventions_ledger_v1.md`(規約台帳 v1.6)である。**
> - 本草案は **便 102 F102-4.1(`sol/sol_reply_102_math29.md` §4)の修理 4 点のうち (4)** — 「**CL-12 の『閉』を次版台帳で訂正する**」「**CL-13 を次版台帳へ条文案として起草する**」— の履行物である。
> - **編入(v1.6 → v1.7 への本体編集)は行っていない。** 発効判定は **司令塔 + Sol(便 103)** の専権であり、EP 係が勝手に live 台帳を改版することはしない。
> - **過去台帳(v1.1〜v1.6 の本体)・過去 cert(v1〜v4)・過去 checker(v1/v2)は一切編集していない**(F102-4.1 逐語: 「過去台帳・過去 cert は編集しない」)。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱(便 102 F102-4.1 差戻しの修理)
> - **編入時の作法**(発効が下りた場合): v1.1〜v1.6 と同じく **末尾継ぎ足しでなく論理位置へ**編入し、編入前の live 台帳の SHA-256 を改訂行に記録する。編入直前の live 台帳 SHA-256 = **`38b5c977fd2559120d1c9e69e0c14d32335012593d3dc870e6511ef8f53fd958`**(本草案起草時点の実測値・機械生成)。

---

## 0. 本草案が含むもの(4 項)

| # | 項目 | 編入先(v1.7 発効時の論理位置) | 由来 |
|---|---|---|---|
| **A** | **【CL-12】の「閉(着地)」記述の訂正** — checker v2 は §1.7.3′ **(viii)** を**部分実装**にとどまり、**contract 完全版ではなかった** | **§5.3 の【CL-12】行を置換** | 便 102 **F102-4.1** |
| **B** | **【CL-12′】** を新規に開く(checker v3 + cert v5 の着地記録・**閉鎖条件 = 便 103 の Sol 再検収 PASS**) | **§5.4(v1.7 で新設)** | 同上 |
| **C** | **【CL-13】の条文案**(外部 pin に applicability 情報を同居させる)— **共同設計案**(Sol 便 102 §4 末) | **§1.5 の CV-10 細則へ新項 §1.5.1** + **§5.3【CL-13】行の更新** | 便 102 **F102-4.1** 末 |
| **D** | **事故台帳への 1 行**(§0)+ **§1.7.3′ の実装註** — 「**検査器は『発見した digest』でなく『schema 上 digest が必須の位置』を列挙せよ**」 | **§0 の表** + **§1.7.3′ の註** | 便 102 **F102-4.1**(Sol の変異注入) |

> ★ **D は「新しい規範」ではない。** §1.7.3′ **(viii)** は v1.6 の時点で既に「**両方書いたもの・どちらも無いもの**を MALFORMED」と正しく書いていた。**欠けていたのは規範ではなく実装である。** よって D は規範の新設ではなく、**実装側の手順則**として記帳する(CV-13 の教訓「規範を文書に書いただけでは止まらない」の第二例)。

---

## A. 【CL-12】の訂正 — v1.6 §5.3 の当該行を次で置換する

> **v1.6 の記述のどこが誤りだったか**(便 102 F102-4.1)。v1.6 §5.3 の【CL-12】欄は、裁定 431/433 で **checker v2 の着地と実走結果を追記し、「残 = Sol 再検収(便 102)のみ」**と記帳した。しかし便 102 で Sol が **変異注入**により示したのは、**checker v2 が §1.7.3′ (viii) を満たしていない**ということである。

### A-1. Sol の実証(逐語・`sol/sol_reply_102_math29.md` §4)

```
v4 の effective_source_chain[0] から sha256 だけをメモリ上で除去:
PASS, scanned 8
```

**工房側での再現(本草案起草時に機械実行・checker v2 は不改変のまま)**:

```
checker v2 on v4 (無変異)      : PASS, scanned 9
checker v2 on mutated v4       : PASS , scanned 8
```

### A-2. 原因(**cert の欄ではなく検査器の走査方式**)

checker v2 の `walk_sha_containers()` は「**既に** `sha256` または `sha256_ref` を持つ dict」を列挙する。したがって **digest 必須の entry から双方を消すと、その entry 自体が走査対象から消える**。「見つけた二型の共存禁止」(= XOR の *both* 側)は実装されていたが、「**どちらも無い**」(= XOR の *missing-both* 側)は**原理的に検出できない走査設計**だった。

⟹ **格の訂正**: v1.6【CL-12】の「**着地**」は、**instance-level の PASS 記録としては正しい**が、「**contract 完全版(§1.7.3′ (vi)–(ix) 充足)**」という格としては**誤りだったので撤回する**。checker v2 が満たしていたのは **(vi)(vii)** と **(viii) の半分**、および (ix) の 9 負例までである。

### A-3. 置換文案(【CL-12】)

| 項 | 内容(v1.7 案) |
|---|---|
| **【CL-12】** | ★ **CLOSED(v1.7・便 102 F102-4.1・ただし下記の訂正つき)。** **v1.6 の「contract 完全版 = checker v2 が着地した」という格は撤回する**(便 102 **F102-4.1** = **FAIL・差戻し**)。**訂正の内容**: checker v2 = `search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py`(SHA-256 = `e851f11ace2c50aba72ea0c55317ccbf1047b4f5a86a15f8de5268d765e36c86`・**不改変で保存**)は §1.7.3′ の **(vi) 全 `sha256_ref` 列挙**・**(vii) 実入力 path 束縛** を満たし、**(viii) は「両方書いた側」のみ**を実装していた。**「どちらも無い側(missing-both)」は未実装**であり、Sol の変異注入(A-1)が実証した。**cert 側の欄は無罪**(v4 の digest 欄自体は正しい)。**contract 完全版 = checker v3** ⟹ **【CL-12′】** へ引き継ぐ。**過去 checker v1/v2 の file と、過去 cert v1〜v4 は byte 不変で保存する**(記録) |

---

## B. 【CL-12′】(v1.7 で新設・**未閉鎖**)

| 項 | 内容(v1.7 案) |
|---|---|
| **【CL-12′】** | **checker v3 と cert v5 の着地。閉鎖条件 = 便 103 で Sol が再検収 PASS を出すこと。** **現物**: checker v3 = `search/probe/wac_v1/ihnec_r4b_selfhash_checker_v3.py`(**SHA-256 = `5587392c2fc4e5fa7e5e74e474973c99cf2de69d166b29708ace4ea2b97a3f40`**)/ cert v5 = `search/certs/ihnec_r4b_conventions_v5_20260805.json`(**SHA-256 = `86df0bfc0df6eea31f1942af1da5c7b05ffa48d86c8b296417565b102b5b71ea`**)/ 生成器 = `search/probe/wac_v1/ihnec_r4b_conventions_v5_20260805_gen.py`(SHA-256 = `b78bf4b87bc7c82a8a06077a5e0976e8e34bbde7d547113d06b0b49f64d6d13e`)。**設計変更の核心**: 走査を「**発見した digest の列挙**」から「**schema 上 digest が必須である位置の構造的列挙**」へ反転した(D 参照)。v2 の discovery walk は **belt として削らず残す**(additive only)。**実走結果**(機械出力・下表)。**未閉鎖の理由**: 発効判定は司令塔 + Sol の専権であり、**EP 係の自走行では閉じない** |

### B-1. checker v3 の実走結果(**機械出力・手写しなし**)

| 対象 | 結果 |
|---|---|
| cert v5(正例) | **PASS** / `required_digest_positions` = **14** / `discovered_extra_digest_positions` = **0** / `sha256_ref_and_sha256_locations_scanned` = **14** |
| cert v4(旧版を直接入力) | **INTEGRITY_STOP**(`ledger_version drift`: 宣言 `conventions_ledger_v1_5` ≠ 要求 `conventions_ledger_v1_6`) |
| cert v3(旧版を直接入力) | **INTEGRITY_STOP**(同上・宣言 `conventions_ledger_v1_4`) |
| `--selftest`(mutant matrix) | **3 PASS + 19 STOP**(全 22 件が期待どおり) |
| checker v2(不改変の回帰) | v4 に対し **PASS, scanned 9** / `--selftest` **1 PASS + 9 STOP**(無破壊) |

### B-2. 負例発火表(**一変異一発火**・§1.7.3′ (ix))

| # | 変異 | 発火した検査 |
|---|---|---|
| R1/R2 | 旧版 cert(v4 / v3)を直接入力 | `ledger_version drift` |
| N-a | holder が実在しない | **(i)** |
| N-b | `json_pointer` の target path 不一致 | **(ii)** |
| N-c | target bytes 改竄 | **(iv)** |
| N-d | plain `sha256` を非 64-hex へ | **(iii)** |
| N-e | `current` entry が別の実在 cert を整合的に詐称 | **(c)** |
| N-f | nested `superseded_by.sha256_ref` の破壊 | **(i)**(**(vi) でのみ到達可**) |
| N-g | 同一 entry に `sha256` と `sha256_ref` を併記 | **XOR violation (both)** |
| N-h | `current.path` と `effective_source.path` を揃えて詐称 | **(c)** |
| ★ **N-i** | **`effective_source_chain[0]` から `sha256` を除去(Sol 便 102 §4 の変異そのもの)** | ★ **XOR violation (missing-both)** |
| ★ N-j | nested `superseded_by` から digest を除去 | ★ **XOR violation (missing-both)** |
| ★ N-k | `conventions_used.effective_source` から digest を除去 | ★ **XOR violation (missing-both)** |
| ★ N-l | top-level `supersedes` から digest を除去 | ★ **XOR violation (missing-both)** |
| ★ N-m | digest 必須の top-level pin を欄ごと削除 | **schema requires top-level …**(規範 1: 欠品 ≠ 非該当) |
| ★ N-n | plain `sha256` を**正しい 64-hex だが誤った値**へ | ★ **(x)**(v2 は型検査のみで通していた) |
| ★ N-o | `ledger_artifact_pin.declared_version` ≠ `conventions_used.ledger_version` | ★ **(xi)** |
| ★ N-p | `ledger_artifact_pin.sha256` を実台帳 bytes と食い違わせる | ★ **(x)** |
| ★ REPRO | **v4(Sol が変異させた現物)の `chain[0].sha256` を除去 → v3 の構造述語を直接適用** | ★ **XOR violation (missing-both)**(v4 の必須 digest 位置 = **9**。v2 の discovery walk は変異後 **8** しか見なかった) |

**非発火側の縁**(鉄則: 述語の**両縁**を張る — 「何を消しても止まる」過剰発火と区別する):

| # | 非変異/無害変異 | 期待 | 実測 |
|---|---|---|---|
| P1 | 無変異の cert v5 | PASS | **PASS** |
| P2 | digest 位置でない任意欄(`scope`)を削除 | missing-both は**発火しない** | **PASS** |
| P3 | 合法な片側形が両方共存(`sha256` のみの entry と `sha256_ref` のみの entry) | **発火しない** | **PASS** |

---

## C. 【CL-13】条文案 — 外部 pin の **applicability 情報**(共同設計案・Sol 便 102 §4 末)

### C-1. Sol の設計方針(逐語)

> 外部 pin object には、適用に本質的な場合だけ unitary/nonunitary、係数環、completion の型などの applicability 情報を同居させる。無関係な欄を全 cert に強制せず、source pin と適用型を切り離さない規範にするのがよい。

### C-2. 条文案(**§1.5.1 を新設して置く**案)

> #### 1.5.1 `external_reference` の **applicability**(v1.7 案・便 102 F102-4.1 末・**Sol との共同設計**)
>
> **動機**(v1.6 §1.5 の教材点): Fresse の例は「**同じ番号・同じ著者でも、規約の版(unitary / 非 unitary)が違えば射程が違う**」ことを示した。**pin が正しくても、その定理が工房の設定を literally 覆っていない**ことがありうる。
>
> **条文案**:
>
> 1. **同居の原則** — applicability 情報は**外部 pin object の内側に置く**。pin(どの文献のどこか)と適用型(その言明が要求する構造)を**別欄へ分離しない**。分離すると、pin だけを引用して適用型を落とす読み方が可能になる。
> 2. **条件付き必須(全 cert 強制はしない)** — 欄は `external_reference.applicability` とし、**「適用に本質的な場合だけ」必須**とする。**無関係な cert へ空欄を強制しない**(【CL-8】の実装コスト問題を踏まない)。
> 3. **「本質的」の操作的判定**(規範文が判定不能にならないための最小条件)— 次のいずれかに該当するとき **applicability は必須**である。
>    - (a) 同じ番号・同じ定理名が、**同一著者の別 Part / 別版で異なる構造**の下に現れる(Fresse Part 1 6.2.4(b) 非 unitary / Part 2 Thm 1.1.5 unitary が現物)。
>    - (b) 引用先の言明が、工房が**使っていない構造**(strict unit・特定の係数環・特定の completion)を**仮定**している。
>    - (c) 引用先が **`proof_body_status = external_reference`** で、その先の版が **(a)(b) に触れる**。
> 4. **欄の形(案)** — 自由文でなく**列挙型 + 逐語 pin** にする(自由文だと照合できない):
>    ```jsonc
>    "external_reference": {
>      "work": "Fresse, SURV 217, Part 1",
>      "statement": "Theorem 6.2.4(b)",
>      "page_pin": { "published": "212-214", "pdf": "259-261", "proof_body": "214-218" },
>      "sha256": "<取得 artifact の digest>",
>      "applicability": {
>        "required": true,                       // 上記 3(a)-(c) のいずれかに該当
>        "reason": "同番号の別 Part が unitary 版であり射程が異なる",
>        "unit": "non-unitary",                  // "unitary" | "non-unitary" | "n/a"
>        "coefficients": "n/a",
>        "completion": "profinite",
>        "workshop_setting_matches": true,       // 工房の設定を literally 覆うか
>        "verbatim_pin": "docs/notes/reading_fresse_624_v1.md"
>      }
>    }
>    ```
> 5. **非該当の書き方** — 3 のいずれにも該当しない pin では `applicability` を**省略してよい**(欠品が MALFORMED にならない**唯一の digest 周辺欄**)。ただし **`required: false` を明示的に書いた場合は、その判断自体が検問対象**になる。
> 6. ★ **未決の残り(司令塔レビュー + Sol ゲート)** — `applicability` を **checker が強制できるか**。現状の checker は digest しか見ないので、この欄は**人手照合のまま**である。`workshop_setting_matches: true` の**根拠 pin**(reading ノートの §/行)を必須にすれば機械照合可能な部分が増えるが、**欄の増設コスト**とのトレードオフである。

### C-3.【CL-13】行の更新案

| 項 | 内容(v1.7 案) |
|---|---|
| **【CL-13】** | **条文案は起草済み(§1.5.1 案・便 102 F102-4.1 末の Sol 共同設計を採録)。未決は 2 点**: ① §1.5.1-3 の「本質的」判定 (a)(b)(c) が**十分か**(判定不能を残さないか)② `applicability` の **機械照合可能性**(§1.5.1-6)。**司令塔レビュー + Sol ゲート待ち。発効までは人手照合。** |

---

## D. 手順則の追記(**規範の新設ではない**)

### D-1. 事故台帳(§0)への 1 行(案)

| # | 裁定 | 何が起きたか | 破られた規約 |
|---|---|---|---|
| — | **便 102 F102-4.1** | self-hash checker v2 が **digest 必須欄から digest を両方消した cert を PASS** させた(`scanned` が 9 → 8 に減っただけで警報が出ない)。走査が「**既に digest を持つ dict の発見**」だったため、**欄を消すと検査対象からも消えた** | **規範 11**(§2・v1.6)/ **§1.7.3′ (viii)** — **規範は正しく書かれていた。破れたのは実装** |

### D-2. §1.7.3′ への実装註(案)

> ★ **実装註(v1.7 案・便 102 F102-4.1)**: **(viii) を「発見した digest の集合」の上で実装してはならない。** 存在しない値は発見できないので、`missing-both` は**原理的に検出できない**。**(viii) は「schema 上 digest が必須である位置」を、その位置に digest があるか否かと無関係に、cert の構造だけから列挙したうえで**適用すること。
>
> - **必須位置の最小集合**(現行 cert 族): top-level の `supersedes` / `supplements_cert`(+ v5 で新設した `ledger_artifact_pin`)・`conventions_used.effective_source`・`conventions_used.effective_source_chain[i]` の**全 entry**・その入れ子 `superseded_by`(**再帰的に何段でも**)。
> - **discovery walk は削らず belt として残す** — 必須位置集合の外に digest が現れた場合も XOR と (i)–(iv) を適用する(**検査は additive only**: 既存検査を弱めない・削らない)。
> - ★ **一般則(EP 系と共通)**: **「見つけたものを検査する」設計は、欠品を検出できない。** 検査対象の列挙は**入力の中身でなく schema から**引くこと。

### D-3.(参考・**司令塔検問対象**)v5 が新設した欄と検査 — **本草案では規範化しない**

以下は **cert v5 と checker v3 が実装した**ものだが、**台帳の規範として一般化するかは司令塔検問 + Sol ゲート待ち**である。本草案は**事実の記帳のみ**を行い、規範文は起こさない(職掌の境界)。

| 記号 | 内容 | 状態 |
|---|---|---|
| **`ledger_artifact_pin`** | cert が宣言する `ledger_version` を、**live 台帳 artifact の path + sha256 + declared_version** へ束縛する top-level 欄。散文の宣言を **digest 照合**へ変える(**F102-4.1 指摘 1 の構造的修理**) | **v5 に実装済み・規範化は未決**。★ 副作用: **台帳が改版されると当該 cert は自動的に INTEGRITY_STOP し、cert 側の再版を強制する**。これは意図した fail-closed 挙動だが、**運用コストを司令塔が是とするか**の判断が要る |
| **(x)** | plain `sha256` の **bytes 再計算一致**(v2 は 64-hex 型検査のみ) | **v3 に実装済み・規範化は未決**。過去 artifact の bytes は確定済みなので実行可能 |
| **(xi)** | `ledger_artifact_pin.declared_version` == `conventions_used.ledger_version` の束縛 | 同上 |

---

## E. 発効しないもの(**明示**)

- **本草案そのもの**(台帳 v1.7)。live 正本は **v1.6** のままである。
- **checker v3 / cert v5 の「再批准」**。便 102 の未発効事項「EP v4/self-hash checker v2 の再批准」は、**v5/v3 に置き換えて Sol 再検収を請う**段階であり、**まだ発効していない**。
- **`ledger_artifact_pin` / (x) / (xi) の規範化**(D-3)。
- **【CL-13】§1.5.1 案**(C-2)。
