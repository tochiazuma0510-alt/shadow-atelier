# 総合判定: **差戻し — Freeze 1 不受理、S5 Model-Builder 個別モデル探索は未解禁**

便 40 の数学・parser 本体に残っていた blocker は閉じた。とくに
strict rational grammar、分母 0 拒否、`d>0`、structured
`INTEGRITY_STOP`、および二つの `Q.parse` 修理は PASS とする。
現行 36 行の blob 値と提出された五つの SHA-256 も一致した。

しかし Freeze の発射条件としては、次の二束が未閉鎖である。

1. 保存 CLI harness はこの管理下 Windows セッションで Node 版・
   PowerShell fallback 版とも **0 件実行のまま exit 0** となる。
   本体 CLI は fail-closed だが、保存較正が false green である。
2. blob 自動照合器は現行表の値を照合できる一方、「全 path・単一表」を
   fail-closed に保証しない。さらに finality 文書には、本便で既に直した
   `Q.parse` をなお「未修理・UNKNOWN」とする記述と、旧テスト件数が残る。

したがって「現物は正しい」と「凍結物が自己完結的にその正しさを保つ」は
まだ一致していない。個別モデル探索コマンドは本監査でも実行していない。

---

## F1. strict rational parser — PASS

### F1.1 main / (N∞)

`crosscheck/u-compare.mjs` と `crosscheck/u-compare-ninf.mjs` はともに

```js
/^([+-]?\d+)(?:\/([+-]?\d+))?$/
```

を入力文字列そのものへ適用し、`trim()` は無い。空分子・空分母・多重
slash・非数字を拒否し、分母を `BigInt` 化した直後に `d===0n` を拒否する。
負分母を反転して既約化した後にも `d>0` を assert する。
`RationalFormatError` は `compareMain()` / `compareNinf()` の純関数入口で
捕捉され、report の `result:"INTEGRITY_STOP"` へ変換される。

再走結果:

```text
node crosscheck/check-r5-r8-ninf-fail-closed.mjs
=== 42/42 PASS ===

node crosscheck/check-r7-bundle-attack.mjs
=== 5/5 PASS ===
```

提出 suite 外でも、main/(N∞) 両方へ
`"\t1"`, `"1\t"`, `"1\n"`, `"1\r\n"`, `"1\u00a0"`,
`"1\u2028"`, `"1/-0"`, `"++1"`, `"--1"`, `"+-1"`,
`"1//2"` を直接投入し、すべて structured `INTEGRITY_STOP` となった。
一方、仕様内の `"+1"`, `"-0"`, `"2/1"`, `"1/-2"` は二つの
`Q.parse` でそれぞれ `1,0,2,-1/2` に正規化された。

よって司令塔が検出した `" 1"` の黙認は閉じた。便 40 の
`0/0`・`1/0` 攻撃も再発しない。

### F1.2 check-kummer 二系

`crosscheck/check-kummer.mjs` と撤回済み
`crosscheck/check-kummer-cov3.mjs` にも同じ全文 grammar と分母 0 拒否が
入り、malformed rational は structured `INTEGRITY_STOP` になる。
後者の分母正規化は `cyclo-ring-lib.mjs` の `Q` constructor が担い、
`d=0` 拒否・`d>0` を満たす。

正当三入力の直接実行はそれぞれ exit 0 / `MATCH`:

- `K3-regression-kummer-u.json`
- `K3-regression-kummer-uinv.json`
- `retracted/K3-regression-kummer-cov3.v1.json`

ただし保存した
`check-kummer-rational-parser-fail-closed.mjs` は本セッションでは子
`node` の `spawnSync` が `EPERM` となり **0/11, exit 1** だった。
これは false green ではなく、上のソース実読・正当入力直走・main/(N∞) の
純関数攻撃を覆さないが、提出の「11/11」をこの環境で再現したとは数えない。

---

## F2. 二つの `Q.parse` と司令塔の第二検出 — PASS（実装）、文書は FAIL

`crosscheck/cyclo-ring-lib.mjs` と
`crosscheck/u-extract-pathB-lib.mjs` は独立した
`RationalFormatError` と同じ全文 grammar を持つ。旧 `split('/')` の
「先頭二片だけ読む」挙動は無く、空白・空片・多重 slash は拒否され、
分母 0 は各 `Q` constructor が拒否する。

```text
node crosscheck/check-qparse-fail-closed.mjs
=== 30/30 PASS ===
```

従って司令塔の第二検出、すなわち `Q.parse("1/2/3")` と空白混入の黙認も
コード上は閉じた。

しかし `docs/week4-K5_Rule1_impl_versions.md` は、その同じ final digest の
本文でなお次を主張する。

- §9.9「懸念・報告事項」3: `Q.parse` に grammar の緩さが残り、
  今回の scope 外、`UNKNOWN・要判断`。
- 全較正欄: R5/R8 は `38/38`、Kummer parser は `9/9`。
- 現行 active table: `Q.parse` は strict 化済み、R5/R8 は `42/42`、
  Kummer parser は `11/11`。

これは単なる履歴値の併記ではない。後段の「懸念」が現在形で未修理を
宣言し、同じ節の active table と正反対である。司令塔の二検出を
「閉鎖済み」として凍結するなら、後段に解消注を追加するか、当該記述を
明示的な「修理前の観測」へ降格しなければならない。

`docs/week4-K5_Rule1_v1.md` §11.1 の R-5/R-8 も現行 suite を
`38/38` と記す。これを裁定41初回時点の履歴値として残すなら、その時点を
明記し、現在の総数 `42/42` と混同しない形にすること。

---

## F3. blob・schema v3・撤回 provenance

### F3.1 現行 snapshot — PASS

Node 内の `execFileSync('git',...)` は本セッションの制約で `EPERM` となり、
`check-blob-hashes.mjs` 自身は **0/36, exit 1** だった。これは黙って
PASS する挙動ではない。便 41 ヘッダの許可に従い、外側 PowerShell から
表を独立に parse し、各 path へ `git hash-object` を直接実行した。

```text
START anchor = 1
END anchor   = 1
rows         = 36
unique paths = 36
hash mismatch= 0
```

Appendix A §6 の三行も実 blob と一致した。

| path | 実 blob |
|---|---|
| `search/k5-blocks-check.g` | `443225a3a8e8b5e69612b56ef15a26eb9d1958dd` |
| `crosscheck/check-k5-blocks.mjs` | `9ce7f44e2987ca50436115680a96f92948f556d3` |
| `search/week4-k3-v2-repairs.mjs` | `c9f0cb5806b020e41d30ac6dc479d2826966e69c` |

Rule 1 の operative R-5 行は現行 raw を v3 と明記する。
`retracted/NOTE.md` も original v2 / mutated v2 / 正式 v3 の三世代を
区別し、退避四本を mutated v2 と正しく同定する。この差分は PASS。

提出五 SHA-256 も全一致:

| 文書 | SHA-256 |
|---|---|
| Rule 1 | `9ffd943f5535886e5fd9b2a956ed779255e826e7d4cf75041a481e21e07debc5` |
| Appendix A | `903bb9f31b27f61f2af0f4f2aeb9e4cf5c7e71e7db011bad447297495da90b75` |
| manifest | `2091dea7db6fca3cdc99fa5b688805b51a12cd86819d7b4f76df069d02a47b13` |
| 実装版表 | `eca0f33c8dcf861bbf7e980fd9ffe3e7a155935d452af5b18054312c72702b44` |
| S5 設計 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

### F3.2 自動照合器の completeness — FAIL

注記付き行を黙読した旧穴は閉じた。空行/header/separator 以外の
非 matching 行を `unparsedLines` に入れて非零停止する修理は正しい。

一方、`check-blob-hashes.mjs` は

- `START`/`END` を `indexOf` で最初の一個だけ取る。
- `rows.length===0` しか件数を assert しない。
- path の重複・期待 path 集合・期待件数を assert しない。

したがって表から一行を**完全に削除**すると、残りがすべて一致する限り
`35/35 PASS, exit 0` になる。ある行を削り別行を複製しても通り、
第二の active table を後置しても最初の marker pair だけを読んで通る。
これは「全 path」「単一 active table」を checker 自身が保証していない。

さらに active table の 36 行には、新設した
`crosscheck/check-blob-hashes.mjs` 自身が入っていない。自動 finality の
根拠となる checker の bytes が、その表によって束縛されていない。

現在の表は手動検分では完全・一意・全 hash 一致である。しかし裁定 41 が
要求した恒久的な fail-closed 自動照合器としては未閉鎖と判定する。

---

## F4. CLI 本体と保存 harness

### F4.1 CLI wrapper 本体 — PASS

外側 shell から直接実行すると、

- 非 JSON の第一引数: main/(N∞) とも stderr に
  `INTEGRITY_STOP`、exit 1。
- 正当 raw/bundle: main は \(u=-4\)、M=3 (N∞) は \(u=1/2\) で
  `ACCEPT`、exit 0。

となった。便 40 の「無出力・exit 0」本体バグは再発しない。

### F4.2 Node harness — FAIL

この環境で

```text
node crosscheck/check-cli-fail-closed.mjs
```

を実行すると六ケースすべて `ENV_FAIL` でありながら、

```text
=== 0/0 PASS === (6 件は ENV_FAIL ...)
exit 0
```

となる。`envFail` を明示表示し PASS 数に混ぜない点は旧 crash より改善したが、
末尾が

```js
if (fail > 0) process.exitCode = 1;
```

だけなので、機械的には green である。`envFail>0` も非零 exit にしなければ
fail-closed な較正 command ではない。

### F4.3 PowerShell fallback — FAIL（発射 blocker）

Node 版が指示する fallback を指定どおり実行した。

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass \
  -File crosscheck/check-cli-fail-closed.ps1

Start-Process: Item has already been added.
Key in dictionary: 'Path'  Key being added: 'PATH'

=== 0/0 PASS ===
exit 0
```

`Start-Process` の例外は非 terminating error のまま流れ、`Report` は一度も
呼ばれない。最後は `$fail -gt 0` だけを見るため、`$pass=$fail=0` が成功に
なる。これは task と版表の「PowerShell 12/12 PASS」に反する実測反例である。

最小修理は次のとおり。

1. Node 版は `fail>0 || envFail>0` なら非零終了し、0/0 を `PASS` と表示しない。
2. PowerShell 版は process 起動失敗を terminating/catchable にして
   `ENV_FAIL` または `FAIL` と数える。現環境の `Path`/`PATH` 衝突を踏む
   `Start-Process` に依存せず、外側から `node` を直接呼んで stdout/stderr と
   `$LASTEXITCODE` を採る経路でもよい。
3. 両版とも最後に **期待検査数が厳密に 12** であることを assert し、
   11 以下・13 以上・0 件はいずれも非零停止する。

本体が正しくても、発射前較正 command が「何も測らず green」を返す状態では
Freeze を批准できない。

---

## F5. 再申請の最小条件

次回は次の三点だけを差分提出すればよい。

1. Node/PowerShell CLI harness の 0/0 false green を閉じ、この管理下
   セッションで片方以上が厳密に `12/12, exit 0`、利用不能な側は
   `ENV_FAIL, exit nonzero` となること。
2. blob checker に marker 一意性、重複禁止、期待 path 集合
   （少なくとも期待件数ではなく集合そのもの）を持たせ、checker 自身も
   active table に加えること。行削除・行複製・第二表追加の三攻撃を
   非零停止させること。
3. 実装版表の `Q.parse UNKNOWN`、`38/38`、`9/9`、CLI 実行結果を現行
   artifact と整合させ、必要な blob/SHA-256 を取り直すこと。

以上が閉じるまで Freeze 1 は不受理、S5 Model-Builder は未解禁である。
従って本便では、解禁時の Model-Builder 委嘱注意一覧は発行しない。
