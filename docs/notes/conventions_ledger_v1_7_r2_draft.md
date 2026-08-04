# 規約台帳 v1.7-**r2** **草案(DRAFT・未発効)** — 便 103 F103-6.2 条件の反映

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED**。**live 正本は依然 `docs/notes/conventions_ledger_v1.md`(規約台帳 v1.6)である。**
> - **前版 `docs/notes/conventions_ledger_v1_7_draft.md`(v1.7-r1・SHA-256 `6f6b1e8c4c1dbae39ddf1027ad8234e7bc9ae3d8689324833099efed4d1d211c`)は byte 不変で保存する**(versioned supersede・凍結規律)。本書は r1 を置き換える改版であって、r1 への追記ではない。
> - 由来: **便 103 F103-6.2** — 「A/B/D の方向は批准可、**CL-13 は条件付き**」。本書は付された 5 条件を反映する。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**発効判定は司令塔 + Sol の専権。**
> - ★ **格の限定(便 103 F103-6.1 逐語)**: checker v3 が照合するのは **pin bytes と版宣言**であって、`h1_verbatim` 文字列そのものではない。**「H1 逐語検査済み」とは書かない。** 本書でも `h1_verbatim` は**参考欄**として扱う。

---

## 0. r1 → r2 の変更点(**5 件・すべて便 103 F103-6.2 由来**)

| # | r1 の記述 | r2 での修理 | 節 |
|---|---|---|---|
| **r2-1** | CL-13 条文案の `applicability` が `unit` / `coefficients` / `completion` の **3 欄固定**(閉じた列挙) | **open typed `requirements`** へ。`characteristic`/`base_field`・`topology`・`finite`/`connectivity`・`operadic`/`model_structure`・`equivariance` 等を受けられる型にし、**列挙を閉じない** | §C |
| **r2-2** | `verbatim_pin` が **bare path** | **`{path, sha256}`** の typed object へ | §C |
| **r2-3** | `workshop_setting_matches: true` が**自己申告 boolean** | **evidence pin を要求**(boolean 単独では書けない) | §C |
| **r2-4** | `ledger_artifact_pin` が「現在の台帳と一致するか」の**単層**だった ⟹ **無関係な台帳追記が過去 cert を遡及失効させる** | **`conformance_at_issue`(発行時適合の不変 digest)と `compatibility_check`(現在版との照合)を分離** | §D-3′ |
| **r2-5** | D3(`ledger_artifact_pin` / (x) / (xi) の規範化)の扱いが「未決」とだけ | ★ **D3 を越えて発効させない**ことを明文化(v1.7 自身が未規範化と宣言した範囲を、発効時に黙って踏み越えない) | §E |

**r1 から引き継ぎ、内容を変更しない部分**: §A(【CL-12】の訂正)・§B(【CL-12′】)・§D-1/D-2(事故台帳の 1 行・§1.7.3′ 実装註)。便 103 F103-6.1 で **CL-12′ は閉じた**ので、§B の閉鎖条件欄のみ更新する(§B′)。

---

## A. 【CL-12】の訂正 — **r1 §A を逐語で引き継ぐ**(変更なし)

v1.6 §5.3【CL-12】の「contract 完全版 = checker v2 が着地した」という**格は撤回**する。checker v2 が満たしていたのは §1.7.3′ の **(vi)(vii)** と **(viii) の半分**(both 側のみ)、および (ix) の 9 負例まで。**missing-both は原理的に検出できない走査設計だった。cert 側の欄は無罪。** 過去 checker v1/v2・過去 cert v1〜v4 は byte 不変で保存する。

---

## B′. 【CL-12′】— **CLOSED**(便 103 F103-6.1)

| 項 | 内容(v1.7-r2 案) |
|---|---|
| **【CL-12′】** | ★ **CLOSED(便 103 F103-6.1・Sol 再批准)。** **現物**: checker v3 = `search/probe/wac_v1/ihnec_r4b_selfhash_checker_v3.py`(SHA-256 `5587392c2fc4e5fa7e5e74e474973c99cf2de69d166b29708ace4ea2b97a3f40`)/ cert v5 = `search/certs/ihnec_r4b_conventions_v5_20260805.json`(SHA-256 `86df0bfc0df6eea31f1942af1da5c7b05ffa48d86c8b296417565b102b5b71ea`)/ 生成器 = `…_v5_20260805_gen.py`(SHA-256 `b78bf4b87bc7c82a8a06077a5e0976e8e34bbde7d547113d06b0b49f64d6d13e`)。**Sol 側の独立再実行**: 通常走行 = required digest position **14**・extra **0**・PASS / `--selftest` = **正例 3 PASS + 変異 19 STOP**(`sha256` 欄除去と missing-both の**双方**を停止)/ checker v2 回帰 = 9 scanned PASS・selftest 1 PASS + 9 STOP(無破壊)。**閉鎖の根拠**: 必須位置を **schema から列挙**する修理により §1.7.3′ (viii) が両側とも実装された。★ **格の限定**: `ledger_artifact_pin` について checker が照合するのは **pin bytes と版宣言**であり、**`h1_verbatim` 文字列そのものは照合していない**。⟹ **「H1 逐語検査済み」とは書かない** |

---

## C. 【CL-13】条文案 **r2** — `external_reference` の applicability

### C-0. r1 からの設計変更(便 103 F103-6.2 の 3 条件)

r1 案は Fresse の現物(unitary / 非 unitary)に引きずられ、**3 欄の閉じた列挙**になっていた。これは「今回の事故の形」だけを塞ぐ設計であり、**次に来る別型の射程ずれ**(標数・基礎体・位相・有限性/連結性・オペラッド/モデル構造・同変性)を受けられない。⟹ **open typed `requirements`** へ改める。

### C-1. 条文案(**§1.5.1 を新設して置く**案・r2)

> #### 1.5.1 `external_reference` の **applicability**(v1.7-r2 案・便 102 F102-4.1 末 + 便 103 F103-6.2・**Sol との共同設計**)
>
> **動機**: pin が正しくても、**その定理が工房の設定を literally 覆っていない**ことがありうる。Fresse の例(同じ番号・同じ著者で unitary / 非 unitary)は**その一型**にすぎない。
>
> **条文案**:
>
> 1. **同居の原則**(r1 から不変)— applicability 情報は**外部 pin object の内側**に置く。pin(どこか)と適用型(何を要求するか)を**分離しない**。
> 2. **条件付き必須**(r1 から不変)— 「適用に本質的な場合だけ」必須。**無関係な cert へ空欄を強制しない**(【CL-8】)。
> 3. **「本質的」の操作的判定** — 次のいずれかで applicability は必須。
>    - (a) 同じ番号・同じ定理名が、**同一著者の別 Part / 別版で異なる構造**の下に現れる。
>    - (b) 引用先の言明が、工房が**使っていない構造**を**仮定**している。
>    - (c) 引用先が `proof_body_status = external_reference` で、その先の版が (a)(b) に触れる。
>    - ★ **(d)(r2 新設・catch-all)**: 上記に当たらなくても、**引用の射程が工房の設定と一致することを示すのに、書誌 pin 以外の情報が要る**とき。**この列挙は閉じない**(判定不能を「非該当」へ倒さない)。
> 4. ★ **欄の形(r2・open typed `requirements`)** — **固定 3 欄をやめ、`kind` つきの要求項目の配列**にする。**未知の `kind` は禁止ではなく登録対象**であり、**checker は未知 `kind` を素通りさせず記帳する**。
>    ```jsonc
>    "external_reference": {
>      "work": "Fresse, SURV 217, Part 1",
>      "statement": "Theorem 6.2.4(b)",
>      "page_pin": { "published": "212-214", "pdf": "259-261", "proof_body": "214-218" },
>      "sha256": "<取得 artifact の digest>",
>      "applicability": {
>        "required": true,
>        "reason": "同番号の別 Part が unitary 版であり射程が異なる",
>        "requirements": [                       // ★ open typed・閉じた列挙にしない
>          { "kind": "unit",              "value": "non-unitary" },
>          { "kind": "characteristic",    "value": "0" },
>          { "kind": "base_field",        "value": "Q" },
>          { "kind": "topology",          "value": "profinite" },
>          { "kind": "finiteness",        "value": "n/a" },
>          { "kind": "connectivity",      "value": "n/a" },
>          { "kind": "operadic_structure","value": "PaB / truncated arity<=4" },
>          { "kind": "model_structure",   "value": "n/a" },
>          { "kind": "equivariance",      "value": "symmetric group action" }
>          // 新しい kind の追加は versioned supersede。既存 kind の意味は変えない
>        ],
>        "workshop_setting_matches": {          // ★ 自己申告 boolean を禁止
>          "verdict": "matches",                // "matches" | "differs" | "UNKNOWN"
>          "evidence": [                        // ★ verdict には evidence pin が必須
>            { "requirement_kind": "unit",
>              "verbatim_pin": { "path": "docs/notes/reading_fresse_624_v1.md",
>                                "sha256": "<64hex>" },   // ★ bare path 禁止
>              "locator": "§4 第2段" }
>          ]
>        }
>      }
>    }
>    ```
> 5. **非該当の書き方**(r1 から不変)— 3 のいずれにも当たらない pin では `applicability` を省略してよい。ただし **`required:false` を明示した場合、その判断自体が検問対象**。
> 6. ★ **fail-closed 則(r2 新設)**:
>    - `workshop_setting_matches.verdict` は **evidence が空なら書けない**。evidence 無しの `matches` は **MALFORMED**。
>    - 各 `requirements[i]` のうち **verdict の根拠に使ったもの**には、対応する evidence が要る。**根拠に使わなかった項目**は evidence 不要だが、その旨が verdict へ効いてはならない。
>    - **`UNKNOWN` は一級の結果**である。判定不能を `matches` へ倒さない。
>    - 未知 `kind` は **STOP ではなく記帳 + `UNKNOWN` 方向**へ倒す(規範の成長を止めない設計)。
> 7. ★ **未決(司令塔レビュー + Sol ゲート)** — `requirements` の `kind` 語彙をどこで管理するか(台帳内の登録表 / 別 registry artifact)。**現状は人手照合**であり、機械照合できるのは `verbatim_pin.sha256` の実在と bytes 一致までである。

### C-2.【CL-13】行の更新案(r2)

| 項 | 内容 |
|---|---|
| **【CL-13】** | **条文案 r2 を起草済み(§1.5.1 案)。便 103 F103-6.2 の 3 条件(open typed `requirements` / `verbatim_pin={path,sha256}` / `workshop_setting_matches` の evidence pin 要求)を反映。残る未決 2 点**: ① `kind` 語彙の管理場所(§1.5.1-7)② 機械照合の射程(現状は `verbatim_pin` の bytes 一致まで)。**司令塔レビュー + Sol ゲート待ち。発効までは人手照合。** |

---

## D. 手順則(r1 §D-1/D-2 を引き継ぎ、D-3 を r2 で改める)

### D-1 / D-2 — **r1 から変更なし**

事故台帳への 1 行(「規範は正しく書かれていた。破れたのは実装」)と、§1.7.3′ への実装註(「**(viii) を『発見した digest の集合』の上で実装してはならない**」「**検査対象の列挙は入力の中身でなく schema から引く**」「discovery walk は belt として削らず残す = additive only」)は r1 のまま。

### D-3′. ★ **`ledger_artifact_pin` の二層化**(r2 新設・便 103 F103-6.2)

**r1 の設計欠陥**: r1 の `ledger_artifact_pin` は「**現在の live 台帳の bytes と一致するか**」の単層だった。この設計では、**IMAGE-MU とも self-hash とも無関係な台帳追記**(例: §1.3.10 の用語追加)が起きただけで、過去の全 cert が INTEGRITY_STOP になる。⟹ **無関係な追記が過去 cert の意味を遡及的に失効させる。** これは fail-closed ではなく **過剰発火**であり、「何を消しても止まる」型と同じく述語の識別力を落とす。

**r2 の修理 — 二層に分ける**:

| 層 | 欄 | 意味 | 性質 |
|---|---|---|---|
| **層 1** | **`conformance_at_issue`** | **発行時**に、この cert がどの台帳 bytes に対して適合していたか。`{ledger_path, ledger_sha256, declared_version, issued_at}` | ★ **不変(immutable)**。後の台帳改版で**変化しない**。過去 cert の意味を保存する |
| **層 2** | **`compatibility_check`** | **現在の** live 台帳に対して、この cert がまだ整合しているか。checker が**実行時に計算**する | ★ **cert に書かない**(書けば古くなる)。checker の**出力**として `compatible` / `superseded_ledger` / `incompatible` の三値 |

**三値の割当(案)**:

- **`compatible`**: 現 live 台帳の版名 = cert の `declared_version`、かつ bytes 一致。
- **`superseded_ledger`**: 版名が進んでいる(cert は古い台帳に対して**正しく発行された**)。⟹ ★ **INTEGRITY_STOP にしない**。**NOTE として報告**し、cert の再版が必要かは**規範の差分**で判断する(無関係な追記では再版を強制しない)。
- **`incompatible`**: cert の `declared_version` と同名の台帳の bytes が**食い違う**(= 台帳が版名を上げずに改変された)。⟹ **INTEGRITY_STOP**(これが本来塞ぎたかった型)。

> ★ **r1 との差**: r1 は上記三値をすべて STOP に潰していた。r2 は **`incompatible` のみ STOP**、`superseded_ledger` は NOTE。**「宣言と実物の食い違い」(F102-4.1 指摘 1)は `incompatible` として依然 STOP する** — 検出力は落ちていない。
>
> ★ **cert v5 への波及**: 現行 cert v5 は r1 型の単層 `ledger_artifact_pin` を持つ。**cert v5 は byte 不変で保存**し、r2 が発効した場合は **cert v6 で二層化**する(versioned supersede)。**cert v5 の再批准(便 103 F103-6.1)は取り消さない** — v5 は v1.6 台帳に対して正しく発行されている。

### D-3″.(参考・**司令塔検問対象**)v5/v3 が実装済みで **規範化は未決**の 3 件

| 記号 | 内容 | 状態 |
|---|---|---|
| `ledger_artifact_pin` | 版宣言の digest 束縛 | **v5 に単層で実装済み**。**規範化は未決**。r2 の二層化案は §D-3′ |
| **(x)** | plain `sha256` の bytes 再計算一致 | **v3 に実装済み・規範化は未決** |
| **(xi)** | `declared_version` == `ledger_version` の束縛 | **v3 に実装済み・規範化は未決** |

---

## E. ★ 発効の範囲(**D3 越え発効の禁止**・便 103 F103-6.2 逐語)

> **v1.7 自身が未規範化とする D3 を越えて発効させない。**

これを条文として明記する:

1. §D-3″ の 3 件(`ledger_artifact_pin` / (x) / (xi))は、**v1.7-r2 が発効しても規範にならない**。実装済みという**事実の記帳**のみである。
2. したがって **他の cert 族へこれらを要求してはならない**。要求するには**別途の規範化(v1.8 以降 + Sol ゲート)**が要る。
3. 「v1.7 が発効したので `ledger_artifact_pin` は必須になった」という読みは**誤り**であり、そう書いた cert / 報告は**格の誤り**として差し戻す。
4. 同様に、§C の【CL-13】条文案も **v1.7-r2 の発効では規範化されない**(§C-2 のとおり Sol ゲート待ち)。

---

## F. 発効しないもの(明示)

- **本草案そのもの**(台帳 v1.7-r2)。live 正本は **v1.6** のまま。
- **§C の【CL-13】条文案**(§1.5.1)。
- **§D-3′ の二層化**(cert v6 は未作成)。
- **§D-3″ の 3 件の規範化**(§E-1 により、発効しても規範にならない)。
- **cert v5 の格の変更**: 便 103 F103-6.1 の再批准はそのまま。ただし **「H1 逐語検査済み」とは書かない**。
