# 規約台帳 v1.7-**r3** **草案(DRAFT・未発効)** — 便 104 F104-5.1 条件の反映

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED**(便 104 F104-5.1 逐語: 「**修理までは DRAFT / UNRATIFIED を維持する**」)。**live 正本は依然 `docs/notes/conventions_ledger_v1.md`(規約台帳 v1.6)である。**
> - **前版は byte 不変で保存**(versioned supersede): r1 = `docs/notes/conventions_ledger_v1_7_draft.md`(SHA-256 `6f6b1e8c4c1dbae39ddf1027ad8234e7bc9ae3d8689324833099efed4d1d211c`)/ r2 = `docs/notes/conventions_ledger_v1_7_r2_draft.md`。本書は **r2 の差替**であって追記ではない。
> - 由来: **便 104 F104-5.1** — 「open typed `requirements`、`verbatim_pin={path,sha256}`、発行時 conformance と current compatibility の分離、D3 越え発効禁止は**正しい方向**である。ただし **CL-13 の aggregate verdict に穴が残る**。」
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**発効判定は司令塔 + Sol の専権。**
> - ★ **格の限定**(便 103 F103-6.1): checker v3 が照合するのは **pin bytes と版宣言**であり、`h1_verbatim` 文字列そのものではない。**「H1 逐語検査済み」とは書かない。**

---

## 0. r2 → r3 の変更点(**1 件・便 104 F104-5.1 由来**)

| # | r2 の穴(Sol 指摘・逐語) | r3 での修理 |
|---|---|---|
| **r3-1** | 「`requirements` を複数列挙しても、**『verdict の根拠に使ったもの』だけ evidence を要求し、使わなかった required item は無証拠でよい**とする。そのままでは **`unit` 一項の evidence だけで全体を `matches` と書き、characteristic/topology/model structure 等を黙って未判定にできる**」 | ★ **「根拠に使わなかった required item」という逃げ道を削除**。各 required item を **per-item 判定つきの構造**にし、**aggregate は per-item status からのみ機械的に決まる**(§C-1 の 4 と 6) |

**r2 から引き継ぎ、内容を変更しない部分**: §A(【CL-12】の訂正)・§B′(【CL-12′】= CLOSED)・§D-1/D-2(事故台帳の 1 行・§1.7.3′ 実装註)・§D-3′(`conformance_at_issue` / `compatibility_check` の二層化)・§D-3″・§E(**D3 越え発効の禁止**)。以下では **§C(CL-13)のみ**を差し替える。

> ★ **便 104 F104-5.1 が明示的に「正しい方向」と認めた 4 点は r3 でも不変**: ① open typed `requirements` ② `verbatim_pin={path,sha256}` ③ 発行時 conformance と current compatibility の分離 ④ D3 越え発効禁止。

---

## A / B′ / D / E — **r2 から逐語で引き継ぐ**(変更なし)

- **§A**: v1.6【CL-12】の「contract 完全版 = checker v2 が着地した」という**格は撤回**。checker v2 が満たしていたのは (vi)(vii) と (viii) の **both 側のみ**。**cert 側の欄は無罪。** 過去 checker v1/v2・過去 cert v1〜v4 は byte 不変。
- **§B′**: 【CL-12′】= **CLOSED**(便 103 F103-6.1)。checker v3 = `5587392c2fc4e5fa7e5e74e474973c99cf2de69d166b29708ace4ea2b97a3f40` / cert v5 = `86df0bfc0df6eea31f1942af1da5c7b05ffa48d86c8b296417565b102b5b71ea`。Sol 独立再実行 = required 14 / extra 0 / PASS、selftest 正例 3 PASS + 変異 19 STOP、checker v2 回帰無破壊。**「H1 逐語検査済み」とは書かない。**
- **§D-1/D-2**: 事故台帳の 1 行(「**規範は正しく書かれていた。破れたのは実装**」)+ §1.7.3′ 実装註(「**(viii) を『発見した digest の集合』の上で実装してはならない**」「**検査対象の列挙は入力の中身でなく schema から引く**」「discovery walk は belt として削らず残す」)。
- **§D-3′**: `ledger_artifact_pin` の二層化 — **`conformance_at_issue`(発行時適合の不変 digest)** と **`compatibility_check`(現在版との照合・checker の出力・三値)**。`incompatible` のみ **STOP**、`superseded_ledger` は **NOTE**(無関係な台帳追記で過去 cert を遡及失効させない)。**cert v5 は byte 不変で保存し、二層化は cert v6 で**。
- **§D-3″**: v5/v3 が実装済みで**規範化は未決**の 3 件(`ledger_artifact_pin` / (x) / (xi))。
- **§E**: ★ **D3 越え発効の禁止**。§D-3″ の 3 件は **v1.7 が発効しても規範にならない**。他 cert 族へ要求してはならない。§C の【CL-13】条文案も **v1.7-r3 の発効では規範化されない**。

---

## C. 【CL-13】条文案 **r3** — `external_reference` の applicability

### C-0. r2 → r3 の設計変更(**aggregate の穴を塞ぐ**)

r2 は「`workshop_setting_matches.verdict` には evidence pin が必須」までは書いたが、**どの required item に evidence が要るか**を「verdict の根拠に使ったもの」と限定していた。これは **判定者が『根拠に使った』と申告する範囲を自分で決められる**ということであり、**`unit` 一項の evidence だけで全体を `matches` と書ける**。

⟹ r3 では **aggregate を人が書く欄から外す**。**per-item の status を全 required item について書かせ、aggregate はそこから機械的に決まる関数**にする。「使わなかった項目」という概念自体を消す。

### C-1. 条文案(**§1.5.1 を新設して置く**案・r3)

> #### 1.5.1 `external_reference` の **applicability**(v1.7-r3 案・便 102 F102-4.1 末 + 便 103 F103-6.2 + **便 104 F104-5.1**・**Sol との共同設計**)
>
> **動機**: pin が正しくても、**その定理が工房の設定を literally 覆っていない**ことがありうる。Fresse の例(同じ番号・同じ著者で unitary / 非 unitary)は**その一型**にすぎない。
>
> **条文案**:
>
> 1. **同居の原則**(r1 から不変)— applicability 情報は**外部 pin object の内側**に置く。pin(どこか)と適用型(何を要求するか)を**分離しない**。
> 2. **条件付き必須**(r1 から不変)— 「適用に本質的な場合だけ」必須。**無関係な cert へ空欄を強制しない**(【CL-8】)。
> 3. **「本質的」の操作的判定**(r2 から不変)— (a) 同番号・同定理名が同一著者の別 Part / 別版で**異なる構造**の下に現れる / (b) 引用先が工房の**使っていない構造**を仮定 / (c) `proof_body_status = external_reference` でその先が (a)(b) に触れる / ★ (d) **catch-all**: 書誌 pin 以外の情報が射程一致の説明に要るとき。**この列挙は閉じない。**
> 4. ★ **`requirements` は per-item 判定つきの配列**(**r3 の核心**)— **open typed**(`kind` の列挙を閉じない)。**各 required item は次の 5 欄をすべて持つ。**
>    ```jsonc
>    {
>      "kind": "characteristic",              // open typed。未知 kind は禁止でなく登録対象
>      "source_value": "0",                   // 引用先が要求する値(逐語)
>      "workshop_value": "0",                 // 工房の設定の値
>      "status": "match",                     // match | differs | UNKNOWN | n_a
>      "evidence": [ { "verbatim_pin": { "path": "docs/notes/reading_fresse_624_v1.md",
>                                        "sha256": "<64hex>" },
>                      "locator": "§4 第2段" } ]
>    }
>    ```
>    - **`evidence` は全 required item に必須**。★ **「verdict の根拠に使わなかった required item は無証拠でよい」という逃げ道は削除する。**
>    - `verbatim_pin` は **bare path 禁止**、**`{path, sha256}`** の typed object(r2 から不変)。
>    - `status: "n_a"` は ★ **理由(`reason`)と evidence の双方が必須**。「該当しない」という判断も**証拠を要する判断**である。
>    - `source_value` / `workshop_value` は**両方書く**。片方欠落は **MALFORMED**(比較していない判定を `match` と書けなくする)。
> 5. **`kind` の例(閉じない・r2 から不変)** — `unit` / `characteristic` / `base_field` / `topology` / `finiteness` / `connectivity` / `operadic_structure` / `model_structure` / `equivariance` / …。**新しい `kind` の追加は versioned supersede。既存 `kind` の意味は変えない。**
> 6. ★ **aggregate verdict は per-item status からの関数**(**r3 の核心・人が直接書かない**)—
>    | 条件 | `workshop_setting_matches.verdict` |
>    |---|---|
>    | **全 required item が `match`** | **`matches`** |
>    | **一つでも `differs`** | **`differs`** |
>    | **`UNKNOWN` が一つでも残る、または未知 `kind` が一つでも残る** | **`UNKNOWN`** |
>    | 上記以外(= `match` と `n_a` のみ) | **`matches`**(ただし `n_a` の理由 + evidence が揃っているときに限る。欠ければ **MALFORMED**) |
>
>    - **優先順位**: `differs` > `UNKNOWN` > `matches`。★ **`differs` が一つでもあれば `UNKNOWN` へ丸めない**(不一致を「不明」に薄めない)。
>    - ★ **cert に aggregate を書く場合、それは per-item から再計算した値と一致しなければならない**。不一致は **MALFORMED / INTEGRITY_STOP**(§1.7.3′ 実装註と同じ流儀 — **申告値は入力でなく照合対象**)。
> 7. **非該当の書き方**(r1 から不変)— §3 のいずれにも当たらない pin では `applicability` を省略してよい。ただし **`required:false` を明示した場合、その判断自体が検問対象**。
> 8. ★ **fail-closed 則(r3)**:
>    - **`evidence` が空の required item は MALFORMED**(status が何であれ)。
>    - **`UNKNOWN` は一級の結果**。判定不能を `match` へ倒さない。
>    - **未知 `kind`** は STOP ではなく **記帳 + aggregate を `UNKNOWN` へ倒す**(規範の成長を止めず、かつ黙って通さない)。
>    - **required item が 0 件の `applicability` は MALFORMED**(`required:true` と宣言しながら中身が無い形を塞ぐ)。
>    - ★ **両縁**: aggregate 述語の負例 fixture は**発火側**(`differs` を 1 件混ぜる / `UNKNOWN` を 1 件残す / evidence を 1 件空にする / 未知 `kind` を 1 件混ぜる / aggregate を per-item と食い違わせる)と**非発火側**(全 `match` + evidence 完備 / `n_a` が理由 + evidence つき)の**双方**を置く。
> 9. ★ **未決(司令塔レビュー + Sol ゲート)** — ① `kind` 語彙の管理場所(台帳内の登録表 / 別 registry artifact)② 機械照合の射程。**現状 checker が機械照合できるのは `verbatim_pin.sha256` の実在と bytes 一致、および §6 の aggregate 再計算まで**であり、`source_value` / `workshop_value` の**意味的**一致は人手照合である。

### C-2.【CL-13】行の更新案(r3)

| 項 | 内容 |
|---|---|
| **【CL-13】** | **条文案 r3 を起草済み(§1.5.1 案)。便 103 F103-6.2 の 3 条件(open typed `requirements` / `verbatim_pin={path,sha256}` / evidence pin 要求)に加え、★ 便 104 F104-5.1 の per-item 構造と aggregate 関数を反映**(「根拠に使わなかった required item」の逃げ道を削除)。**残る未決 2 点**: ① `kind` 語彙の管理場所 ② 機械照合の射程(現状は `verbatim_pin` bytes 一致 + aggregate 再計算まで)。**司令塔レビュー + Sol ゲート待ち。発効までは人手照合。** |

---

## F. 発効しないもの(明示)

- **本草案そのもの**(台帳 v1.7-r3)。live 正本は **v1.6** のまま。**便 104 F104-5.1 逐語により DRAFT / UNRATIFIED を維持。**
- **§C の【CL-13】条文案**(§1.5.1)。
- **§D-3′ の二層化**(cert v6 は未作成)。
- **§D-3″ の 3 件の規範化**(§E-1 により、発効しても規範にならない)。
- **cert v5 の格の変更**: 便 103 F103-6.1 の再批准はそのまま。ただし **「H1 逐語検査済み」とは書かない**。
