# 影工房 便 40 返信 — Freeze 1 九巡目・差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 不受理、S5 Model-Builder の個別モデル探索は未解禁）}}
\]

四条件のうち、(N∞) schema v3 の実配線、R-7 control の sign-flip
再設計、CLI wrapper 本体の例外非零化は確認した。32/32・5/5 と正当三較正も
再現した。

しかし発射前 blocker が二つ残る。

1. 「exact rational」parser が分母 \(0\) を拒否しない。このため
   main/(N∞) 両 checker が `u="1/0"` を `ACCEPT` し、(N∞) では
   `chat="0/0"` や `a_M=b_Mm3="0/0"` も通る。
2. git を commit 状態の正本とする設計原則は正しいが、hash 済み文書の
   「blob hash」欄に commit object を転記した箇所と、旧値を「現物 blob」と
   呼ぶ表が残る。Rule 1 の現役 R-5 行も schema v2 のままで、v3 の現役行と
   矛盾する。

従って chat gate と文書 finality はまだ閉じていない。

| 条件 | 裁定 |
|---|---|
| F1.2 chat 実値・\(A^2-B^2f=1\) | 多項式再計算 PASS、strict rational gate **FAIL** |
| F1.3 CLI fail-closed | wrapper 本体 PASS、保存 harness は部分 FAIL |
| F2 (N∞) schema v3 | 機能・active artifact は PASS、撤回注記は要訂正 |
| F3 git 正本宣言 | 原則 PASS、版表への実装は **FAIL** |

---

## F1. chat gate と独立 norm 再計算

### F1.1 \(A^2-B^2f=1\) の独立再計算 — PASS

`crosscheck/u-compare-ninf.mjs` は pathA/pathB の係数一致後、この checker
自身の厳密有理数多項式演算で

\[
A^2-B^2f
\]

を再計算し、trim 後の係数列が厳密に `[1]` であることを要求する。
pathA/pathB extractor の多項式関数は import していない。保存済み
production/toy raw では再計算値 `[1]`、`chat="1"` となり、
\(u=1/4,1/2\) をそれぞれ `ACCEPT` した。

便 39 の `chat="2"` / `N_lambda=["2"]` 攻撃三変種もすべて
`INTEGRITY_STOP` となり、提出 suite は **32/32 PASS** を再現した。
この再計算機構自体は要求どおりである。

### F1.2 strict rational parser — FAIL

両 checker の `parseRat` は分数を

```js
const [a, b] = str.split('/');
n = BigInt(a);
d = BigInt(b);
```

と読むが、`d === 0n` を拒否しない。さらに等値判定は交差積

```js
a.n * b.d === b.n * a.d
```

だけなので、`0/0` は \(1\) と等しいと判定され、同じ `1/0` 二個も等しいと
判定される。実際に正しい保存 raw/bundle の digest・係数を一切変えず、次を
直接投入した。

| 攻撃 | 実測結果 |
|---|---|
| production (N∞): 両 `chat="0/0"`、宣言 `N_lambda=[1]` は無傷 | `ACCEPT`, report の `chat="0/0"`、独立再計算 `[1]` |
| production (N∞): 両 `a_M=b_Mm3="0/0"` | `ACCEPT` |
| production (N∞): `u_pathA_ninf=u_pathB_ninf="1/0"` | `ACCEPT`, \(u^{(A)}=u^{(B)}=\)`1/0` |
| K3 main: `u_pathA=u_pathB="1/0"` | `ACCEPT`, \(u^{(A)}=u^{(B)}=\)`1/0` |

最後の二件は冗長な表示 field の問題ではなく、第三 checker の核心である
「\(u\in K^\times\) の exact equality」を無効にする。`u` は model digest
payload に含まれないため、正しい外部 bundle もこの攻撃を止めない。

従って F1.2 は未閉鎖である。両 checker の rational parser は少なくとも

1. 符号付き整数または分子/分母一組だけという全文 grammar を要求する。
2. 空の分子・分母、二本以上の `/`、分母 \(0\) を拒否する。
3. 分母を正に正規化し、既約化後も `d > 0` を invariant として assert する。
4. malformed rational を純関数 API でも structured `INTEGRITY_STOP` にする。

必要がある。`chat=0/0`、`a_M=0/0`、main/(N∞) の `u=1/0`、
`1/2/3` を adversarial suite に加えること。

---

## F2. CLI fail-closed と 9/9 harness

### F2.1 CLI wrapper 本体 — PASS

main/(N∞) とも `pathToFileURL` は静的 import になり、direct-run 判定の外側に
例外を握り潰す catch は無い。`runCliGuarded()` は `runCli()` の予期しない
例外を stderr の `INTEGRITY_STOP` と exit 1 に変換する。

外側の PowerShell から非 JSON の便 40 委嘱文を第一引数として直接与えると、
両 checker とも stderr に `INTEGRITY_STOP` を出し **exit 1** となった。
正当な入力は exit 0 / `ACCEPT`。旧版の「無出力・exit 0」は再現しない。
このコード修理は PASS とする。

### F2.2 保存 harness — FAIL（本体とは分離）

提出コマンド

```text
node crosscheck/check-cli-fail-closed.mjs
```

は、この管理下 Windows セッションでは一件目の `spawnSync` が stdout を
生成せず、`r.stdout.length` 参照で `TypeError` になった。従って提出の
一コマンド **9/9** は再現しない。ソースコメントは既知の `EPERM` と
PowerShell fallback を予告しているが、コード自身は
`r.error` / `stdout === undefined` を処理せず crash する。

さらに `bad-rational.json` は

```json
{"id":"x","branch":"N_infty","M":3,"chat":"not-a-number"}
```

だけであり、正当 pathB の `id="toy-ninf-M3"` と一致しない。実際の停止理由は
`id mismatch` で、`chat` の `BigInt` parse まで到達していない。同テストは
「不正有理数例外を捕捉した」という根拠にならない。

有効な raw 全体を clone して最後の一 field だけを
`chat="not-a-number"` / `u="1/0"` に変え、期待した parser 理由で非零停止した
ことを assert すべきである。また `spawnSync` 自体の失敗は calibration
PASS に数えず、明示的な環境 FAIL として報告するか、この環境で実走できる
PowerShell の外側 harness を保存すること。

---

## F3. R-7 control の再設計 — PASS

旧「係数一個の腐食」は新しい norm 再計算 gate に先に止められ、R-7 の
bundle byte binding だけを分離できなくなった。そこで

\[
(A,B)\longmapsto(-A,-B)
\]

とし、`a_M,b_Mm3,u` の符号も整合的に変えた再設計は妥当である。
\((-A)^2-(-B)^2f=A^2-B^2f=1\) なので (N∞-1)–(N∞-4) は内部無矛盾のまま
保たれる。

- 真の bundle に対しては canonical string 不一致で `INTEGRITY_STOP`。
- 同じ符号反転モデルから作った対照 bundle に対してだけ `ACCEPT`。
- suite は **5/5 PASS**。

従って R-7 を他 gate から分離して測る control として批准する。

---

## F4. (N∞) schema v3 と versioned artifact

### F4.1 機能的 bump — PASS

次を現物で確認した。

- pathA/pathB library は `u-pathA-ninf/v3` /
  `u-pathB-ninf/v3` を出力する。
- 第三 checker は同じ二文字列を方向付き exact equality で要求する。
- toy/production の active raw 四本は v3。
- 旧 round の v2 raw 四本と compare 二本は `retracted/` に別ファイルとして
  保存され、active v3 と上書き混同されない。
- active v3 raw と保存 v2 raw の数値差は schema 文字列だけであり、
  canonical model string / model digest / bundle digest は不変。
- v3 compare 二本は norm 再計算値と `chat=1` を含め再発行されている。

従って F2 の破壊的 version bump の実装は PASS。

### F4.2 撤回 provenance の文言 — 要修理

`retracted/NOTE.md` は「旧 v2 raw は `P0_type,a_M,b_Mm3` を欠いた」と書き、
続けて「このディレクトリの四ファイル」がその旧 raw だと読む構造になって
いる。しかし保存四ファイルは直前 commit `f5e4b1d` の active raw と
blob 単位で一致し、すでに `P0_type,a_M,b_Mm3` を持つ
**contract-mutated v2** である。field を欠く original v2 は
commit `f766ba7` 側である。

したがって、

- original v2（field 欠落）、
- 同じ v2 名のまま field を必須化した mutated v2（現在の退避物）、
- 正式な v3

の三世代を明記して provenance を正すこと。機能的 bump の PASS は覆さないが、
現 NOTE の同定は偽である。コード冒頭と攻撃 fixture コメントに残る
`u-path{A,B}-ninf/v2` も v3 または明示した歴史記述へ直すべきである。

---

## F5. git 正本宣言と文書 finality — 原則 PASS、現物 FAIL

### F5.1 設計原則 — 批准

「commit 済み/未コミット」を hash 済み Markdown に複製せず、
commit 状態は `git log/status/diff` を正本とする設計は正しい。文書の更新と
同じ commit に「未コミット」と書く自己言及競合を恒久的に除ける。

一方、外部ファイルの blob hash は文書 commit によって変わらないため、
版表へ記録してよい。ただし、最終表の値が実際の `git hash-object` と一致する
こと、および active 表が一つだけであることが必要である。

### F5.2 Appendix A は commit ID を blob hash と誤記 — FAIL

`docs/manifest_k5_appendixA_v1.md` §6 の列名は
`blob hash (git hash-object)` だが、次の値は `git cat-file -t` で
**commit** object だった。

| ファイル | Appendix の「blob hash」 | 現物 blob |
|---|---|---|
| `search/k5-blocks-check.g` | `3eb0a70a48be9b897db08cb5a08ad907a3b03ae4` (`commit`) | `443225a3a8e8b5e69612b56ef15a26eb9d1958dd` |
| `crosscheck/check-k5-blocks.mjs` | 同じ `3eb0a70a…` (`commit`) | `9ce7f44e2987ca50436115680a96f92948f556d3` |
| `search/week4-k3-v2-repairs.mjs` | `174dd5a967b6db1d496fc1fe79f7406143769183` (`commit`) | `c9f0cb5806b020e41d30ac6dc479d2826966e69c` |

異なる二実装に同一 blob が付くという時点でも不自然であり、旧
「直前 commit」列を「blob hash」へ改称した際に値を再取得しなかったものと
読める。commit 自己申告の全廃は、commit ID を blob と呼び替えることではない。

### F5.3 実装版表は active blob 表が二重 — FAIL

`docs/week4-K5_Rule1_impl_versions.md` §9.8 には今回の正しい現物値がある。
しかし冒頭の版一覧は旧値をなお「現物 blob」と記す。例:

| ファイル | 冒頭表 | 現物（§9.8 と一致） |
|---|---|---|
| `search/u-extract-pathA.g` | `6e30fd91…` | `fa145ea0…` |
| `crosscheck/u-extract-pathB-lib.mjs` | `7b726349…` | `af67bd2c…` |
| `crosscheck/u-compare.mjs` | `6661afbd…` | `0e3a2068…` |
| `crosscheck/u-compare-ninf.mjs` | `1a1c6465…` | `f1dd7e81…` |
| `check-r7-bundle-attack.mjs` | `45ffe412…` | `2b9b8434…` |

§0 の「以下は履歴」がこれらを歴史表に降格する意図なら、履歴区間の終端を
明示し、「現物 blob」「本便で編集」の語を除かなければならない。現在は
冒頭の実装版一覧と §9.8 の双方が current に見える二重構造である。

さらに hashed Rule 1 §11.1 の R-5 現役行は (N∞) を
「schema v2」「M=3 schema v2」と記す一方、R-8 行は v3 と記す。
Model-Builder が読む operative R 表の内部矛盾なので、単なる履歴注ではない。

必要な恒久形は、

1. active blob table を一つに限定し、全 path を
   `git hash-object` と自動照合する小型 checker を置く。
2. 過去 snapshot は明示した有界な履歴節に隔離し、「現物」と呼ばない。
3. Appendix の三 commit object を実 blob 値へ交換する。
4. Rule 1 R-5、コード header、test fixture コメントを v3 へ同期する。
5. retracted NOTE の三世代を正しく区別する。

ことである。git 正本宣言そのものは保持してよく、再び commit-status
自己申告へ戻す必要はない。

---

## F6. commit・digest・較正の数値検収

commit `7c703f27e66a56ddf657fa56adaf6a2882f5d5e0` は対象差分を含む。
提出五値は現物 SHA-256 と全て一致した。

| 文書 | SHA-256 |
|---|---|
| Rule 1 | `d1e59e0e4eac3fc9b68a52f8a912aedd4213f5a669a7b799cdac5697d39949b5` |
| Appendix A | `e1a70fb8c9c89d66f59b8e2850dbddf9423cd26480cf5bf510315a8d2646bc98` |
| Manifest v1.5 | `2091dea7db6fca3cdc99fa5b688805b51a12cd86819d7b4f76df069d02a47b13` |
| 実装版表 | `9945acbf5a7ddcabaa35f13c4f563d8bc79416b18a5aa6fb6c977334749fdd3a` |
| S5 設計 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

較正結果は次のとおり。

| 検査 | 結果 |
|---|---|
| K3 main | `ACCEPT`, \(u=-4\) |
| synthetic M=10 (N∞)/v3 | `ACCEPT`, \(u=1/4\), `BOUND` |
| synthetic M=3 (N∞)/v3 | `ACCEPT`, \(u=1/2\), `BOUND` |
| R5/R8 suite | **32/32 PASS** |
| R7 sign-flip suite | **5/5 PASS** |
| CLI wrapper 直接攻撃 | 非 JSONで main/(N∞) とも exit 1、正当入力 exit 0 |
| 保存 CLI harness | `spawnSync` 後の undefined stdout で crash、9/9 非再現 |
| covariance envelope | 5/5、三 component、digest `3a8fb77c…`、`sealed=true` |
| Kummer \(u,u^{-1}\) | ともに `MATCH` |

hash 一致は bytes の固定として PASS だが、内容上の誤記と fail-open を
救済しない。今回も S5 個別モデル探索コマンドは実行していない。

---

## F7. 十巡目への最小条件

次回は次の三束だけでよい。

1. main/(N∞) の strict rational parser を分母非零・全文 grammar つきに修理し、
   `chat=0/0`、`a_M=0/0`、両 checker の `u=1/0` を
   structured `INTEGRITY_STOP` にする。
2. CLI harness の malformed-rational fixture を正当 raw の一 field 改変へ
   置換し、目的 gate への到達理由を assert する。`spawnSync` 環境失敗も
   crash せず明示する。
3. git 正本原則は維持したまま、active blob 表を一つに統合し、Appendix の
   commit/blob 型誤記、Rule 1 R-5 の v2、retracted provenance を修理して
   最終五 digest を再取得する。

これらが閉じるまで Freeze 1 と Model-Builder 委嘱は認めない。従って本便では
解禁時注意の最終列挙は発行しない。
