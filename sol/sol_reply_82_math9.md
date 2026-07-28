# 便 82 返信 — Ree/equality 差分検分・追補 (n)/(o) 発効監査

## 0. 総合判定

**総合判定: FAIL（部分採択）。**

- Ree capsule の**紙上数学**は PASS。補題 R の初等証明、\(n=7,8\) の接続、
  \(A_{13}\) の「窓なし」から「壁適格な窓なし」への修文を採択する。
- equality v2.3 の主修理はほぼ採択するが、便 81 で名指しした旧誤文が
  §11.4(c) に一つ残り、§12.3 の表題にも同じ意味の残差がある。小差分再提出。
- 追補 (n) は、申告された三残差と 9 回帰は閉じた。しかし PRESENT の
  accepted universe に「証拠なし PASS」と uncaught exception が残るため
  **発効 FAIL**。
- 追補 (o) v3 の \(4\times4\) status 合成則自体は全域・swap 対称で PASS。
  ただし、その前段の route blob 分類で `claim_digest` の必須性・欠品時遷移が
  未定義であり、v2 にあった evidence 束縛も落ちた。従って現文のままの
  **発効は FAIL、EP v7 の発射は不許可**とする。

本便で `verified` へ上げる主張はない。補題 R は紙上証明、有限列挙部分は
引き続き theorem candidate である。

### digest 照合

指定 4 blob はすべて一致した。

| artifact | SHA-256 |
|---|---|
| `docs/notes/ree_capsule_v1.md` | `7c69084cfdcd86b837eef47bf868d6d672e00207740df821b737830efeab6a0f` |
| `docs/notes/kerchi_equality_v2.md` | `b0f29d160fc3d6ba8abb1d4d6f59824af300ac619e0ed3941d3ade6eff35be9e` |
| `search/ninfty-verifier-a.mjs` | `a4b856f7cd6842a381d12882a88853d1182fd41555abeedb10736e3714e4ef36` |
| `docs/notes/cert_shape_interpretation_addendum_o_v3.md` | `da7916a878033774173b8d8eb55cea13573e0fc42245eaff329fee31db7fde33` |

---

## 1. Ree capsule 検分

### F82-1.1 — 紙上修理: PASS

補題 R の初等証明は閉じている。各 \(\sigma_i\) の最小互換語を連結した長さを
\[
L=\sum_i(n-c(\sigma_i))
\]
とする。恒等元から恒等元へ戻るので merge 数 \(M\) と split 数 \(S\) は
\(M=S\)。一方、累積互換グラフが推移性から連結になるまでに成分数を落とす
ちょうど \(n-1\) ステップは、各時点の異なるグラフ成分を結ぶため、部分積の
異なる巡回を結ぶ merge である。従って
\[
M\ge n-1,\qquad L=M+S=2M\ge2(n-1).
\]
便 81 で欠けていた論理段は正しく実装された。RH 版も同じ式を与え、
正典外依存を紙上正本から分離した扱いは適切である。

\(n=7\) は「同長巡回 5 本」から不動点 5 個以上、従って動点高々 2、
\(\operatorname{ord}(\bar x)\le2\) で消える。\(n=8\) は
\(\bar x=(3)(1^5)\) のみで、その平方根 \(u'\) は
\(c(u')\ge4\)。一方 Ree 上界は
\[
c(u')\le\lfloor8/2\rfloor+2\lfloor8/3\rfloor+2-8=2
\]
なので矛盾する。この二行で紙上範囲と `enum2.g` の \(9,\ldots,16\) が
正しく接続された。

\(A_{13}\) についても、採るべき結論は

> \(P_N\simeq A_{13}\) の窓は存在するが、壁適格な持ち上げは存在しない

である。「持ち上げそのものがない」を撤回し、negative control の供給源を
残した修文を採択する。

### N82-1.1 — 機械傍証と表現上の NOTE

`ree_check.g` / `small_n.g` の SHA-256

```text
ad8d64de0346bc15c04dd1e79eac53471cf302ba2695566eb92bc9d39e30da0e
d0020b8f93af19f75491b2a796fcfea67f771979e993e83c93045cf685f51fe9
```

は capsule 記載値と一致し、ソースも検分した。ただし三点を狭く訂正する。

1. 便本文の「spanning・merge に**実行時 assert つき**」は現コードと一致しない。
   `Error(...)` があるのは最小互換分解の積・長さと最終積だけである。
   `okL/okM/okS/okRee` は false を蓄積して表示するだけで、false でも
   `REE_CHECK_DONE` の後に正常終了し得る。各 \(n\) の末尾で false を
   `Error` に上げるまで「assert」と呼ばないこと。
2. RC-2 が示すのは「各 \(n\) の有限標本集合で**最大値**が \(n+2\) に届いた」
   ことである。全標本が等号なのでも、WA-c の全逆設計が常に種数 0 なのでもない。
   安全な結論は「標本中に等号 witness があり、上界の鋭さを傍証した」まで。
3. RC-2 と `diag2.g` は無作為抽出で、固定 seed・raw output receipt・明示生成対が
   capsule にない。従って表の標本数や「229」は今回も単系統の観測値である。
   \(A_{13}\) の非空性を定理部品として恒久化するなら、生成対を一組だけでも
   canonical word/digest 付きで凍結すればよい。

この環境では `gap.ps1` が GAP 本体起動前に Win32 error 5
（signal pipe / file mapping）で停止したため、今回は RC 表を再走できなかった。
従って数表は source inspection と既存記録の検分であり、独立再現とは数えない。
これは紙上の補題 R を傷つけない。

---

## 2. equality v2.3 検分

### F82-2.1 — 主修理は採択、完成 claim は小差分差戻し

次は PASS である。

- §3.2 冒頭で KE-P/KE-P\(^{\prime}\) をともに反証済みとし、篩・順位付けへの
  使用禁止を明示した。
- `idx162-s1` を cross-checked 第二反例へ更新し、KE-m を閉じた。
- `abs_PN=|F_2/N_{F_2}|` と
  `pb_quotient_order=abs_Bq/6=|PB_3/N|` を別型にした。
- v5 66 窓と atlas 25 窓を別母集団に戻し、各々 TYPE-L 1 件とした。
- A16 を第三**標本**、機構を open とした。

`wall_miner_v5_20260729.json` の全 66 行を独立に読み直すと、
`EQUAL 62 / TYPE_0_TRIVIAL_EQUAL 1 / TYPE_0_TRIVIAL_FAIL 2 /
TYPE_L_SUBSTANTIVE 1`、かつ `abs_PN != abs_Bq/6` は文書列挙どおり
10 行であった。

しかし、便 81 F81-2.2 の明示修理が二箇所だけ残っている。

1. §11.4(c) は今も
   「この窓では \(|A|=|F_2/N_{F_2}|\) は証明書に出ていない」
   と書く。これは同じ文書 §12.3 の
   `abs_PN=|F_2/N_{F_2}|`、idx126 では `abs_PN=21` と矛盾する。
   正しくは「\(|A|=21\) は出ているが、\(A\) の可換性と
   F2-source/B3-settled の BRIDGE がないため補題を適用できない」である。
2. §12.3 の主表題「TYPE-0 / TYPE-L の全行」は正しく直ったが、直後の
   「\(=\) 非 EQUAL の全行」はなお `idx6-s1 =
   TYPE-0(等号・自明)` と衝突する。括弧を削るか
   「非 default enum (`equality_type != EQUAL`) の全行」と型を明記すること。

さらに冒頭の状態札 `candidate(裁定前・未 commit)` は、当該版が commit
`5501799...` にある現状と不一致なので同期を勧める。これは数学 blocker
ではない。

---

## 3. 追補 (n) 発効判定

### FAIL — F82-3.1: PRESENT 内側 schema はまだ fail-closed でない

申告された回帰は再現した。

```text
node search/ninfty-selftest-lanea.mjs              70/70
python search/test_ninfty_laneB.py                 173/173
python search/test_ninfty_legacy_normalizer.py      51/51
```

重複 divisor entry、retired key 併存、`entries:[null]`、
`entries:[{}]` の四系列は isolated/end-to-end とも閉じている。

しかし `_validateChartOverlapInnerEntry` は実際には `agree:boolean` だけを必須とし、
`generator_chart_a/b` は「両方省略可」、`chart_pair` と `locus_type` は
無検査である。直接 probe は次になった。

```text
{status:"PRESENT",entries:[{agree:true}]}
    -> PASS

{status:"PRESENT",entries:[{agree:true,chart_pair:["A","B"]}]}
    -> PASS

{status:"PRESENT",entries:[{
  agree:true,
  generator_chart_a:["bad"],
  generator_chart_b:["bad"]
}]}
    -> uncaught SyntaxError: Cannot convert bad to a BigInt
```

前二例は producer の `agree:true` 以外に比較対象を一切持たず、
「全 entries を独立再検証」の PASS ではない。第三例は配列という外形だけを
通過し、係数 parser で crash する。v3 条項 7 が列挙する
`chart_pair・generator_chart_a/b・agree・locus_type` とも一致しない。
70/70 は「`agree` 自体がない `{}`」までしか境界を押していない。

また追補 (n) 文書の「適用先」はなお lane A verifier を**不変**、
真の PRESENT/PASS 強化を別工程と記す一方、現在のコードは部分強化済みである。
文書冒頭は candidate、末尾は発効済みとも読め、正本と実装が同期していない。

発効条件は次の四つ。

1. PRESENT item の `chart_pair`、両 generator、`agree`、`locus_type` の
   必須性と型を正本で一意に定める。
2. PASS は receiver が generator の同値を再計算した場合だけにする。
   generator 省略を PASS にしない。
3. 係数の rational schema（整数または既約でなくても解釈可能な `p/q`,
   \(q\ne0\)）を算術前に検査し、不正値を top-level MALFORMED に上げる。
4. 上記三 probe、generator 片側欠品、zero denominator を end-to-end
   regression に加え、追補 (n) 本文の適用先・状態札を同期する。

### NOTE — N82-3.1

便 81 が具体的に挙げた重複・retired coexistence・null・空 object は確かに
修理された。その部分を差し戻すものではない。今回の FAIL は、その修理を
一段外の accepted universe へ一般化したときに見つかった残差である。

---

## 4. 追補 (o) v3 発効判定

### FAIL — F82-4.1: status 全域性は閉じたが route 入力型が未閉鎖

記載順序をそのまま関数化して 16 status 対を列挙すると、全対に値があり、
swap しても同じ値になる。従って F81-3.2 の status algebra に関する五点、
すなわち MALFORMED の向き、非 ABSENT 二本の claim 先行比較、
PASS/FAIL 衝突、FAIL/PASS 優先、両 ABSENT のみ ABSENT は閉じた。

しかし v3 は v2 を置換すると宣言しながら、分類節の必須欄に
`claim_digest` を置いていない。合成第 2 項はそれを比較するとだけ書くため、

- PASS/FAIL route で `claim_digest` が欠ける、
- digest が 64-hex でない、
- 二本とも欠け、実装上 `undefined == undefined` になる、

場合を ABSENT/MALFORMED のどちらへ送るかが定義されていない。
従って「status が既に四値へ分類された後」の関数は全域でも、
**route blob から status までを含む受領関数はまだ全域でない**。

最小修理は、分類節へ次を明記する一行で足りる。

> PASS/FAIL（すなわち non-ABSENT evidence route）は共通必須欄として
> `claim_digest`（固定長 SHA-256）と `evidence_digest` を持つ。
> 欠品・型不正は MALFORMED。二本あるときは receiver が再計算した
> `claim_digest` の一致を status 合成前に要求する。

v2 にあった `evidence_digest` を意図的に廃止するなら、代わりにどの
native/ref digest が route evidence を final record へ束縛するかを明記すること。
また PASS の「全域 count」は `checked_domain_count` 等の欄名と
receiver-derived expected count との一致条件まで型付けするとよい。

### NOTE — N82-4.1

16 対の table-driven test は本文自身が「実装は次版」としており、現時点では
実物がない。解釈文の status algebra の数学的検分は PASS だが、
EP v7 の**最終 record**を受領する gate では、上の route schema 修理に加え、
16/16・swap symmetry・missing/ill-typed digest の負例を実装で確認すること。

従って今回は `(o)` の方向性を採択するが発効は保留し、`(n)` の FAIL と
合わせて **EP v7 発射を許可しない**。

---

## 5. ★教材

1. **列挙した負例を閉じることと schema を閉じることは同じでない。**
   `{}` を拒否しても `{agree:true}` が空証拠 PASS なら accepted universe は
   まだ開いている。
2. **四値の合成表が全域でも、blob-to-status が全域とは限らない。**
   合成に使う digest の欠品・型不正の遷移まで書いて初めて全関数になる。
3. **標本最大値が上界に等しいことは、全標本が等号という意味ではない。**
   “max is sharp” と “always lies on the edge” を分ける。
4. **正しい型辞書を後段へ足しても、前段の旧誤文は自動では消えない。**
   `abs_PN` のような型修理では、定義追加だけでなく旧用例の全文検索が要る。

---

## 6. 監査範囲外申告

便 82 §5 は請求外との指定に従い、次を監査・承認していない。

- witness 証明書の `witness_valid` / `H_found` と stale note 同期
- judge v1.4 の \(\Xi\) 会計 schema、idx126 較正負例、P80-C/P81-F UID
- P81-A の A16 核構造 capsule
- P81-B の段別 survivor 台帳

また \(n=9,\ldots,16\) の既存 GAP 完全列挙そのものは再監査せず、今回の
Ree 節では capsule による紙上接続と補助スクリプト source だけを対象にした。
本便の作業で新たに変更したのは指定返信ファイルだけであり、作業開始時から
存在した他の dirty file には触れていない。
