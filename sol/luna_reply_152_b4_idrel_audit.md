# IdRel 2.49 / GAP 4.16 静的監査（U6/158）

## 監査範囲と結論

ローカルの GAP 4.16.0 に同梱された `idrel` の `PackageInfo.g`（Version
2.49, Date 02/10/2025, lines 9--12）と、`lib/logrws.gi`、`lib/idrels.gi`、
`lib/logrws.gd`、`doc/chap3.txt` をソースレベルで照合した。重い GAP 実行は
していない。

結論は二つある。

1. `LoggedReduceWordKB` の行ログを元の 158 relator に戻し、自由群で再生する
   方式は sound な最小 certificate になる。ただし `LoggedReduceWordKB` の戻り値
   自体は candidate であり、GAP の rule/log を信頼して terminal にしてはならない。
2. `LoggedOnePassKB` の **type-1 critical pair の log 組み立ては、文書化された
   恒等式と静的に一致しない**。したがって OnePassKB/RewriteReduce の結果を
   rule certificate として受け入れるなら全 triple を独立自由簡約で検査する必要が
   ある。最終 norm 行の独立検査が通る場合に限り、その norm identity certificate
   自体を terminal の根拠にできる。

## 正本となる log 規約

IdRel の文書 `doc/chap3.txt:4--10` は logged rule を

```text
[ lhs, [ [n1,w1],...,[nk,wk] ], rhs ]
```

とし、恒等式を

```text
lhs = (n1^w1) ... (nk^wk) rhs,
n^w = w^-1 n w.
```

と定めている。`n>0` は `GroupRelatorsOfPresentation(mG)[n]`、`n<0` は
`GroupRelatorsOfPresentation(mG)[-n]^-1` であり、負号は conjugator の逆では
ない。この対応は `idrels.gi:359--370` (`ExpandLogSequence`) と
`idrels.gi:580--587` (`ConjugatingWordOfLoggedTerm`) でも明示されている。

`InverseLogSequence` は `idrels.gi:553--566` の通り、項を逆順にして index の
符号だけを反転し、conjugator はそのままにする。従って `P(inv(L))=P(L)^-1`
である。

## 4 API の厳密な戻り値

宣言は `lib/logrws.gd:142--170` にある。

### `InitialLoggedRulesOfPresentation(mG)`

`logrws.gi:1225--1247`。戻り値は **triple のリスト**である。

* `InverseRulesOfPresentation(mG)` の各 `[lhs,rhs]` は `[lhs,[],rhs]`。
* `j` 番目の `GroupRelatorsOfPresentation(mG)` は
  `[ rel[j], [[j,id]], id ]`。
* `j+Length(invrules)` ではない。`i+leni` の旧コードは
  `logrws.gi:1242` でコメントアウトされ、実行コードは `[[i,id]]`。
* 最後に `BetterLoggedRuleByReductionOrLength` で sort されるので、出力 list の
  位置は relator index ではない。`igrel` は計算されるがこのメソッドの戻り値には
  使われない。

### `LoggedOnePassKB(mG,rules)`

`logrws.gi:771--984`。戻り値は「新規分だけ」ではなく、入力を shallow-copy
して critical-pair の rule を append、sort、**完全一致する triple**を除いた
後の **全 rule リスト**である。type-1（contained）と type-2（overlap）を
処理する。

各 critical word は `LoggedReduceWordKB` で得た `[log,red]` に分解され、
`logrws.gi:838--855`（type-1）または `:919--935`（type-2）で向きを選ぶ。
同じ signed index と同じ conjugator の隣接 inverse 項だけを消す
（type-1 `:863--877`、type-2 `:946--965`）。これは全体の恒等式検査ではない。

### 重要な type-1 静的不一致

type-1 で `l1 = u*l2*v`、`c2u` を source の定義（各 conjugator を
`w*u^-1` にする）とする。`crit1=u*r2*v`、`crit2=r1` なので、文書の invariant
から、reduction logs を `log1`（crit1）と `log2`（crit2）とすると

```text
P(log1) red1 = P(inv(c2u)) P(c1) P(log2) red2.
```

従って正しい向きの log は

```text
red1 -> red2 : inv(log1) + inv(c2u) + c1 + log2
red2 -> red1 : inv(log2) + inv(c1) + c2u + log1.
```

しかし source は `logrws.gi:842--843` で

```text
L  := inv(log2) + inv(c2u) + c1 + log1;
iL := inv(log1) + inv(c1)  + c2u + log2;
```

を作る。これは type-2 の式（`:923--924`）には一致するが、type-1 の上記式
とは一致しない（特に `c1` と `c2u` の inverse/位置が違う）。向きの選択
`:847--855` もこの誤った式をそのまま採用する。よって OnePassKB が生成した
type-1 rule を無検査で再利用してはならない。この指摘はソース恒等式の代数的
照合であり、GAP の重い実行結果ではない。

### `LoggedRewriteReduce(mG,rules)`

`logrws.gi:988--1074`。戻り値は **reduced rule の全リスト**で、log/event の
リストではない。現在 rule と同じ lhs を持つ rule を除いた `newrules` で lhs/rhs
を `LoggedReduceWordKB` し、

```text
c13 = inv(log1) + old_log + log3
c31 = inv(log3) + inv(old_log) + log1
```

（`:1012--1023`）を作って、順序に応じて `[r1,c13,r3]` または
`[r3,c31,r1]` に置換する。reduced lhs と rhs が等しければ rule を omit
（`:1038--1051`）。最後の重複除去は `lhs` と `rhs` だけを比較し、log は比較し
ない（`:1067--1073`）。同じ普通の rule に異なる log がある場合、残った一方の
logを独立に検査しなければ provenance は確定しない。

### `LoggedReduceWordKB(word,rules)`

`logrws.gi:749--767`。戻り値は **2 要素**

```text
[ full_chronological_log, final_word ]
```

であり、record や word 単体ではない。内部の one-pass は `:713--745` の通り、
rule リストを一度だけ順番に走査し、各 rule の最初の occurrence を現在 word
から置換する。prefix を `u` とすると log 項の conjugator は必ず
`w -> w*u^-1`（`:725--741`）。その後、word が変化しなくなるまで pass を
繰り返し、各 pass の log を順に Concatenation する。rule が循環すれば戻らず、
内部に pass cap はない。

## U6/158 norm identity の最小 certificate

terminal を証明するのに必要なのは、GAP の rule list そのものではなく、各 norm
について次の自由群恒等式が独立 checker で再生できることだ。

```text
original_norm = P(log) * reduced
P(log) = product( rel[abs(i)]^(conjugator) )
```

最小の JSON 契約は次の形とする（word は全て original 6-generator の signed
integer list、index は 1-based）。

```json
{
  "schema": "d972-b4-u-idrel-norm-proof/v1",
  "source_sha256": "<frozen 158-relator/972-roof input bytes>",
  "relator_sha256": "<exact ordered 158 relators>",
  "roof_word_sha256": "<exact ordered 972 roofs>",
  "norm_sha256": "<exact ordered 972 norms>",
  "generator_count": 6,
  "relator_count": 158,
  "norm_count": 972,
  "unique_norm_count": 486,
  "duplicate_map": [1, 2, "... 972 entries ..."],
  "rows": [
    {"unique_index": 1, "original": ["..."],
     "reduced": ["..."],
     "log": [[-17, ["... conjugator ..."]], [4, []]],
     "log_length": 2, "identity": true}
  ],
  "status": "COMPLETE"
}
```

`rows` は 486 unique rows でよいが、`duplicate_map` を正本の 972 行に対して
完全照合すること。各 row について Python は、負 index なら relator を先に
反転し、conjugator `w` に対して `inverse(w)+relator+w` を連結して free-reduce
し、最後に `reduced` を連結して `original` と比較する。`identity` は入力値を
信頼せず `reduced == []` から再計算する。terminal は 486/486 rows 完了、全て
恒等、入力/relator/roof/norm digest と map が一致した場合だけ許す。

現在の direct lane が pin している値は、`search/d972_b4_u_idrel_direct_logged_v1.g`
の lines 57--70 にある source `c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`、
relator `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`、
roof `3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8`、
norm `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`、
target `9c77e6768ebf7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62` である。
この lane の checker は既に `search/check_d972_b4_u_idrel_direct_logged_v1.py:161--177`
で上記の自由簡約を再実装しており、これは rule identity を GAP に再委譲しない
最小形になっている。

rule/trace まで再演したい場合だけ、上記に `rule_digest`、全 triple
`[lhs,log,rhs]`、各 event の `before/after/prefix/suffix/position` を追加する。
event は `before=prefix*lhs*suffix`、`after=prefix*rhs*suffix`、各 log conjugator
の `w*prefix^-1` を独立確認し、mutable GAP list の参照を共有しない snapshot と
する。terminal の norm identity だけが目的なら rule trace は必須ではないが、
trace を出す場合は毎 rule triple の invariant も検査する。

## GAP 側が誤って terminal を出す failure modes

* raw log の 1-based relator index を 0-based にする、sort 後の rule list position
  を relator index とする、または旧 `+leni` convention を使う。
* 負 index を「conjugator inverse」と解釈する。正しくは `rel[abs(i)]^-1` を先に
  取り、その後 `w^-1 rel w`。
* `w^-1rw` と `wrw^-1`、または prefix shift `w*u^-1` と `u^-1*w` を取り違える。
* `LoggedOnePassReduceWord` の一 pass を full normal-form reduction とみなす、または
  rule 適用順に依存する log を canonical とみなす。
* `LoggedOnePassKB` の type-1 log（上記 `:842--843`）を検査せず使う。
* `LoggedRewriteReduce` の omit/dedup を、reduced lhs/rhs と log の自由群恒等式を
  検査せず「冗長 rule の消去」とみなす。dedup は log を見ない。
* `CheckLoggedKnuthBendix` を raw integer-index log に直接渡す。実装
  `logrws.gi:1113--1129` は `c[1]^c[2]` を計算するだけで relator index の
  frozen 158 list への mapping をしない。さらに `ShallowCopy` 後に inner triple
  を書き換えるため、呼び出し前の deep snapshot が必要。これは全行 bool を返す
  checker ではなく、expanded triple の list を返す。
* GAP の `GroupRelatorsOfPresentation(mG)` の順序/符号が入力の frozen 158 行と
  同じかを確認せず、個数 158 だけを確認する。producer はこの ordered equality
  も gate にすべきである。
* 空 rule list、未束縛変数、JSON/`fail`、GAP process timeout、rule/log/word cap、
  KBMAG の generator refusal を空 word/terminal と扱う。`LoggedOnePassReduceWord`
  は `rules[1][1]` を参照するので空 list に terminal semantics はない。
* `LoggedKnuthBendix` の list fixed point を有限群の order、kernel triviality、または
  972 norm identity と同一視する。fixed point は rewrite computation の状態であり、
  別の free-group certificate が必要。
* GAP の shallow list を receipt/event に保存し、後続 in-place 更新で過去 stage の
  log/map を変える。各 stage、rule、event、map は serialization 時点の deep copy と
  digest を固定する。
* `reduced=[]` だけを見て log identity、original norm、relator source digest、972 行
  map を検査しない。bounded nonidentity は A ではなく UNKNOWN である。

以上から、今回の最短安全判定は「IdRel は norm rows を生成する候補器、Python
free-reduction checker が 158 relator/486 unique/972 map を再生し、全 reduced が
空のときだけ B4-B terminal」。GAP の logged rule completion 自体の成功表示や
`CheckLoggedKnuthBendix` の未変換出力を terminal gate に使わない。

## 追加監査: 全 rule に対する F6 invariant filter

### filter の正確な契約

`LoggedOnePassKB` の戻り値を次の純粋な検査器に通す。producer 側で filter しても、
同じ検査を Python checker が再実行する。

1. presentation の ordered 158 relators と、GAP の
   `GroupRelatorsOfPresentation(mG)` を **signed word の列として完全一致**させる。
   個数だけ一致する場合は reject。monoid arrangement も
   `[1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]` に固定し、GAP の 12 monoid generator word
   を original F6 signed word に変換する。
2. 各 rule が `[lhs, log, rhs]` の長さ 3 であること、lhs/rhs が 12-generator
   word、log が `[signed_index, conjugator_word]` の列であることを検査する。index は
   `1..158` または `-1..-158` のみ。`0`、rule list position、`+leni` は不可。
3. `toF6` で lhs/rhs/conjugator を original six-generator word に直す。各 log 項
   `[n,w]` は `rel[abs(n)-1]`（n<0 ならその free inverse）を
   `inverse(w)+relator+w` にする。項を元の順番で連結し、free-reduce する。
4. 次を byte-for-byte で検査する。

   ```text
   toF6(lhs) == free_reduce(P(log) + toF6(rhs))
   ```

   空 log の inverse/cancellation rule もこの式を通らなければ reject。GAP の
   `CheckLoggedKnuthBendix` は raw integer index を relator word に解決しないので、
   filter はそれに依存しない。
5. filter 結果には `input_rule_sha256`、`valid_rule_sha256`、`rejected_rule_count`、
   各 rejected rule の stable index/理由を保存する。inner GAP list を参照共有せず、
   全 triple/log/word を serialization 前に deep-copy する。完全一致 triple の dedup
   はしてよいが、同じ lhs/rhs で log だけ違う triple を lhs/rhs だけで潰さない。

`rejected_rule_count=0` は rule candidate の F6 soundness を意味するが、完備性・
termination・有限性を意味しない。1 件でも reject した場合はその pass を
`UNKNOWN_INVALID_RULES_REJECTED` と記録する。以後の norm reduction は、reject された
rule を一度も使わず valid rule リストから再実行する。invalid rule を使った後に
filter するだけでは、その reduction log の provenance を救済しない。valid-only
list で全 norm の独立 F6 proof が完了して空になった場合、norm identity 自体は
sound だが、出力は「公式 OnePass の完全な replay」ではなく filtered lane と明記
する。

### 極小 type-1 regression（式の実発火）

type-1 constructor の kernel を、3 generator `a,b,c` と 2 relator

```text
rel[1] = a b c = [1,2,3],   rel[2] = b = [2]
```

で固定する。次の二つの入力 rule はそれぞれ invariant を満たす。

```text
R1 = [ a b c, [ [ 1, id ] ], id ]
R2 = [ b c,   [ [ 2, id ] ], c   ]
```

実際、`abc=(abc)·1` と `bc=b·c` である。`R1` の lhs に `R2` の lhs が
`u=a,v=id` で含まれるので、source の type-1 branch は

```text
crit1 = u*r2*v = a c,
crit2 = r1 = id,
c2u = [ [ 2, a^-1 ] ].
```

この toy では両 critical word にさらに適用できる rule がなく、`log1=log2=[]`。
従って source が作る列は

```text
L  = [ [ -2, a^-1 ], [ 1, id ] ],
iL = [ [ -1, id ], [ 2, a^-1 ] ].
```

文書 invariant を F6 free-reduction すると、正しい rule は

```text
[ ac, L, id ]       (またはその逆 [ id, iL, ac ]).
```

一方、通常の GAP word order（`id < ac`）で source の `:847--855` が選ぶ
`[ac,iL,id]` は、右辺の展開が `c^-1 a^-1` となり lhs `ac` と一致しない。
反対向きの branch `[id,L,ac]` も、右辺の展開が `acac` となり lhs `id` と
一致しない。従って word order に依存せず、type-1 source 式の少なくとも一方は
F6 filter に落ちる。この計算は GAP の大規模実行ではなく、source の critical
pair locals をそのまま代入した整数 word toy regression である。q8 程度の実 GAP
toy を再演する場合も、最初に `LoggedOnePassKB` の全戻り rule を dump し、filter
前後の rejected row を比較すること。

この fixture は「入力 rules が valid でも公式 type-1 constructor が invalid
candidate を append し得る」ことを分離して検出する。filter で candidate を捨てる
ことは、真の equality の集合から偽の equality を除くだけなので soundness を壊さ
ない。ただし rewrite coverage は弱くなり得るため、completion/terminal ではなく
必ず UNKNOWN または valid-only ルールでの独立 norm proof として扱う。
