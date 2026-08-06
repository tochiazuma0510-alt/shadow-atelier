# CAL-B4 C-8(Package GT `penta` 突合)代替 gate — waiver 事前登録票 v1

**状態札: `candidate(waiver 起票のみ・発効ゼロ・司令塔裁定+Sol ゲート未通過・旧 S-Q46-0 の読み替えなし)`**

- 起草: 影工房 実装係(implementer)/ 2026-08-06
- 委嘱: 司令塔(CAL-B4 最終仕上げタスク ③)— Sol 便 112 の R-6c 条件に従い起草
- 根拠: `sol/sol_reply_112_math38.md` §F112-5「R-6c: 条件つき PASS、現時点は発火 HOLD」
  > 「C-8 を同等の独立 checker に置き換えるなら、その waiver と代替意味論を **新しい versioned prereg** で明記し、旧 v1 の S-Q46-0 を黙って読み替えない。」
- 対象: `docs/notes/q46_charming_fake_prereg_iffirst_v1.md` §5 の **S-Q46-0**(「CAL-B4(§6)が全 PASS していない ⟹ 発火禁止」)が P0 として要求する **C-1〜C-6 と C-8**(sol_reply_112_math38.md §193 の明記)のうち、**C-8 のみ**を対象とする局所的な waiver。C-1〜C-6/C-6b は本票の対象外(別途 authoritative integrated cert で PASS/FAIL を報告)。

---

## 0. なぜ C-8 に waiver が要るか(事実関係の確認)

`search/probe/b4_cal_v1/c8_packagegt_crosscheck.py` および `.github/workflows/b4-cal.yml` の `c8_packagegt` ジョブに記録されている、環境由来の genuine なブロッカー2件:

| 環境 | 症状 | 原因 |
|---|---|---|
| ローカル Windows/Git-Bash | `import PaB` → `import Aux` が `ModuleNotFoundError` | `search/thirdparty/PackageGT/Aux.py` のファイル名が Windows 予約デバイス名 `AUX`(CON/PRN/AUX/NUL/COM1-9/LPT1-9)と衝突し、ファイルが存在するにもかかわらず import が失敗する(`c8_packagegt_crosscheck.py` 冒頭コメントに確認記録あり) |
| GHA ubuntu-latest | `search/thirdparty/PackageGT` が checkout に存在しない | `.gitignore` line 6 により `search/thirdparty/`(Dolgushev パッケージ GT 等の第三者コード)は**意図的に** gitignore されている(著作権・将来の公開可否のため。ハッシュのみ `provenance/LEDGER.md` に記録)。`b4-cal.yml` の `c8_packagegt` ジョブは、この不在を検知すると **clean SKIP**(PASS でも FAIL でもない)として報告する設計 |

→ **C-8 は「実行して FAIL した」のではなく「現行の 2 環境(ローカル Windows / GHA ubuntu-latest 標準)のいずれでも実行不能」という genuine な環境ブロッカーであり、SKIP は PASS の代用にはならない**(`c8_packagegt.yml` コメント自身がこの区別を明記済み)。これが Sol R-6c が waiver 手続きを要求した理由である。

---

## 1. waiver の内容(本票が提案する代替)

### 1.1 恒久修理ではなく PENDING 扱い

Package GT `penta` との実突合(C-8 本来の内容 = PackageGT 自身の `penta`/`generWComm` を使った、本工房の GAP 実装からは完全に独立な第三者実装によるクロスチェック)は、以下のいずれかの環境が整うまで **明示的に PENDING** とする。恒久的な代替物には**しない**。

- (a) ローカル Linux 環境(WSL2 または Docker コンテナ)を用意し、`AUX` ファイル名衝突を回避して `search/thirdparty/PackageGT` をローカルで import・実行する。
- (b) 将来、`search/thirdparty/PackageGT` を GHA 側に vendor 化する(現状の gitignore 方針・著作権判断を司令塔が改めて裁定した上で、リポジトリまたは CI キャッシュに同梱する)。

★ **この waiver は「C-8 は不要である」という主張ではない。** 上記いずれかが整い次第、C-8 を実走し authoritative integrated cert に組み込むことを本票は要求し続ける。waiver は「(a)/(b) が整うまでの間、C-8 の不在を理由に CAL-B4 系列の全 gate を無条件に止めない」という**手続き上の逃し弁**に限定する。

### 1.2 当面の代替根拠(C-8 が本来担保する性質の部分的代用)

C-8 が本来検証する性質は「本工房の GAP 実装(psi 構成・N19 の pentagon/hexagon 判定)が、完全に独立な第三者実装(PackageGT)と一致する」という**第三者クロスチェック**である。この性質そのものは C-8 なしには得られないが、当面の代替として次を根拠に据える。

> **N19 の pentagon 通過数 216 は、本工房の GAP 実装内で既に「二方式交差済み」である(= C-4 の内訳)。**

具体的には `search/probe/b4_cal_v1/cal_b4_n19_pentagon.g` に以下の**構造的に異なる 2 つの実装**が存在し、両方とも 216 を報告している:

1. **主方式**(diagonal-Sym(45) 構成): 5 つの pentagon 余面 $\varphi_{123},\varphi_{234},\varphi_{1,23,4},\varphi_{1,2,34},\varphi_{12,3,4}$ を Sym(45) 上の対角作用として一括構成し、`P19 := Image(combinedHom)` の全 7776 元を悉皆して pentagon (2.20) を評価する経路(C-4 節、`pentPassSet`)。
2. **c5.g 移植方式**(数学者#2 設計・独立変数名・独立実装): PB3 の 3 生成元(Y12, Y23, Y13 相当の Av/Bv/Cv)を保持する `Gc5 := Group(gXc5, gYc5)` 上で、独立に定義した `compC5` ブロック抽出関数を使い pentagon を再評価する経路(`passC5`)。

両者は「同じ GAP プロセス内・同じ司令塔設計」という限界はあるものの、**変数・関数・ブロック割り当てを独立に再実装**しており、単純な `Print` の重複ではない(cal_b4_n19_pentagon.g 内の `Error("STOP -- c5.g-method pentagon cross-check <> 216, ...")` が fail-closed で両者の不一致を検出する設計になっている点も、実装が独立であることの傍証)。

★★ **ただしこれは C-8 の代用として不十分であることを明記する(格下げの申告)**:

| 観点 | C-8(Package GT 突合) | C-4 の二方式交差(本票の代替根拠) |
|---|---|---|
| 実装の来歴 | 完全に独立な第三者(Dolgushev グループ)のコード | 同一セッション・同一実装者(司令塔設計・implementer 実装)による 2 つの経路 |
| 検出できるバグの型 | **論文の定義そのものの誤読**(本工房と PackageGT が独立に同じ誤読をする可能性は低い) | **実装のケアレスミス**(添字ずれ・ブロック順序の取り違え等)。**論文解釈の系統的誤り(規約取り違え等)は検出できない** — 両方式とも同じ psi 構成・同じ論文解釈を前提にしている |
| falsifier 型の独立第三実装としての格 | 該当する | **該当しない**(CV-9 の意味での「非当事者による判読」ではなく、同一当事者内の二重実装) |

→ 「C-4 の二方式交差 = falsifier 型の独立第三実装」という言い方は**誤解を招く**ため、本票では採用しない。正確には「**同一実装者による構造的に異なる二重実装の一致**」であり、これは論文解釈の誤り(規約取り違え等、`cal_b4_n19_pentagon.g` 冒頭で司令塔・数学者が現に一度検出・訂正した種類のバグ)への保険にはならない。この点は R-6c が要求する「代替意味論」の**弱さ**として明記する(§2)。

---

## 2. 代替意味論(格付けの正確な記述)

CAL-B4 の統合 cert において、C-8 のステータスは以下のいずれかの語でのみ記述してよい。

- `"SKIP (environment blocker, see cal_b4_c8_waiver_prereg_v1.md)"` — 現状のデフォルト。
- `"PENDING (WSL/container or GHA vendor-ize, not yet scheduled)"` — waiver 発効後の標準表記。

以下の語は **C-8 の代替として使用禁止**(格の水増しを防ぐ):

- 「C-8 相当」「C-8 を満たす」「第三者クロスチェック済み」— C-4 の二方式交差はこれらを意味しない。
- 「cross-checked」の語を C-4 の二方式交差だけに対して単独で使う場合は、必ず「同一実装者内の二重実装」であることを併記する(CLAUDE.md の「探索器と照合器の分離」則 — 二方式が同じ司令塔設計・同じセッションの派生である以上、独立照合とは呼べない)。

---

## 3. 旧 S-Q46-0 との関係(黙って読み替えない)

`docs/notes/q46_charming_fake_prereg_iffirst_v1.md` §5 の **S-Q46-0** は「CAL-B4(§6)が全 PASS していない ⟹ 発火禁止」であり、`sol_reply_112_math38.md` §197 は CAL-B4 の P0 を **C-1〜C-6 と C-8** と明記している。

本票は **S-Q46-0 の文言を書き換えない**。本票が提案するのは:

> **もし司令塔が本票を裁定で採択した場合に限り**、S-Q46-0 の「C-8」要件は、CAL-B4 統合 cert 上で「PENDING(本票 §1.1 の (a)/(b) いずれかが整うまで)」かつ「§1.2 の代替根拠(格は §2 のとおり弱いと明記)を伴う」状態を以て**暫定的に充足したとみなす**、という**新しい versioned な追加条件**を S-Q46-0 に**上乗せする**(既存の文言を消去・改変しない)。

- 本票が採択されても、**C-8 の実走(§1.1 (a)/(b))を不要にする効果は一切生じない**。
- 本票は `q46_charming_fake_prereg_iffirst_v1.md` を 1 バイトも書き換えない(read-only)。両票の関係は「本票が発効すれば S-Q46-0 の運用に暫定の追加条件を与える」という**別文書からの参照**にとどめる。
- 本票自体は **候補札のまま**(発効ゼロ)であり、次のいずれの発火判断にも使用してはならない: (i) Q4.6 prereg の R0(CAL-B4 全 PASS 確認)、(ii) R-6e の前件 1(P0 = C-1〜C-6/C-8 PASS)。

---

## 4. 発効条件(未発効を明記)

本票は以下がすべて揃うまで **candidate のまま**であり、CAL-B4 統合 cert・Q4.6 prereg のいずれの gate にも使用してはならない。

1. 司令塔裁定(本票の内容を承認するか、修正指示を出すか)。
2. Sol ゲート(R-6c が要求する「新しい versioned prereg」としての監査 — §1.2 の弱さの申告が十分かを含む)。
3. 統合 cert(`search/certs/cal_b4_integrated_v1_20260806.json`)側で C-8 のステータス表記が §2 の代替意味論に厳密に従っていることの機械的な突合(独立 checker での確認)。

---

## 5. 規律申告

- 本票は machine を走らせていない(紙のみ・GAP 未実行)。
- C-4 の「二方式交差」の事実(216 = 216)は `search/probe/b4_cal_v1/logs/cal_b4_n19_run31078897925.log` 既存ログの引用であり、本票のための新規実行はしていない。
- 本票は S-Q46-0 の文言を書き換えていない(read-only)。
- 「初」「新規」の語は使用していない(該当なし)。
- 本票の格: **candidate**(waiver 提案のみ)。発効主張はしない。

---

## 6. 司令塔への確認事項

- §1.2 で「C-4 の二方式交差は C-8 の代用として不十分」と自己申告したが、**それでも暫定 gate として採用するか、それとも C-8 実走(§1.1 (a)/(b))が整うまで CAL-B4 統合 cert の C-8 欄は無条件に SKIP のまま(暫定 gate なし)にするか**は判断が分かれ得る。本票は前者(暫定 gate あり・格は弱いと明記)を提案するが、後者(暫定 gate なし)の方が保守的である。どちらを採るかは司令塔裁定事項として明記し、実装係が独断で選ばない。
