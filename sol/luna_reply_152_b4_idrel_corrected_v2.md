# Luna reply 152 — B4 corrected direct IdRel v2

## 実装

IdRel 2.49 の installed package は変更せず、logrws.gi:771--984 の
LoggedOnePassKB を repo-local に複製した。

変更は type-1 log の二式だけである。l1=u*l2*v、c2u は source と同じ
w*u^-1 shift、crit1=u*r2*v、crit2=r1 とすると、

    red1 -> red2 : inv(log1) + inv(c2u) + c1 + log2
    red2 -> red1 : inv(log2) + inv(c1) + c2u + log1

従って corrected copy は

    L  := Concatenation(ilog2,ic1,c2u,log1);
    iL := Concatenation(ilog1,ic2u,c1,log2);

とする。type-2 branch、rule sort/dedup、その他の OnePass algorithm は
installed source と同じである。higher-rank method はこの GAP process 内だけに
install し、package file は書き換えない。v2 direct source は v1 の frozen-input
gate、all-rule F6 filter、row replay、caps、receipt を再利用し、LoggedOnePassKB
呼出しだけ corrected method に dispatch させる。

なお、GHA run 31946020641 の v1 pass0 は initial rules=182、invalid=0、rows=486、
identity=1 まで通過したが、pass1 は約13秒後に  の第1引数 fail で停止した。
そのため v2 copy には
Subword / ReduceWordKB / LoggedReduceWordKB、inverse、critical word、orientation
の fail-closed guards を追加した。正常入力では algorithm の挙動を変えず、同じ
異常なら明示的な GAP Error（UNKNOWN）で止め、stale receipt を terminal にしない。

## Regression

3 generator / 2 relator fixture

    rel[1] = abc, rel[2] = b
    R1 = [abc, [[1,id]], id]
    R2 = [bc,  [[2,id]], c]

の type-1 contained pair (u=a, v=id) で、upstream candidate
[[-1,id],[2,a^-1]] は F3 replay reject、corrected candidate
[[-2,a^-1],[1,id]] は accept となる。さらに copied constructor 自体も tiny
monoid rules に対して実行した。

実行（本番 U ではない）:

    .\gap.ps1 search\d972_b4_idrel_corrected_type1_regression_v2.g
    D972_B4_CORRECTED_TYPE1_REGRESSION_PASS upstream=REJECT corrected=ACCEPT copied_constructor_rules=3 lhs=ac rhs=id

U6/158 production や pass0/pass1 は実行していない。A/B の主張もしていない。

## GHA 起動例

既存 producer の --source で v2 source を指定する。

    python search/d972_b4_u_idrel_direct_logged_producer_v1.py --source search/d972_b4_u_idrel_direct_logged_corrected_v2.g --output ci/out/d972_b4_u_idrel_direct_logged_corrected_v2.json --max-passes 1 --max-rules 20000 --max-log-length 8192 --max-conjugator-length 16384 --max-log-letters 200000 --max-reduced-length 4096 --max-wall-seconds 1800

## Provenance / SHA-256

Installed source provenance:

    IdRel 2.49, Date 02/10/2025
    C:/Program Files/GAP-4.16.0/runtime/opt/gap-4.16.0/pkg/idrel/lib/logrws.gi
    2836dd6aca49ed7fe0e51d07abb5efb1b7f3ff6b70f17fd1070c6dd44d35ed5e

New files:

search/d972_b4_idrel_logged_onepass_corrected_v2.g
      7c0190cd42dd8dbd63e9551b5934072073e36901feb42f657d5b81187c05bd83
search/d972_b4_u_idrel_direct_logged_corrected_v2.g
      35b8798779f43e09230c980bb905f3d1e6c1e4d556be96ac09a18495dfd485a3
search/d972_b4_idrel_corrected_type1_regression_v2.g
      0b593e0ac23c1ec9948078b06a45544537f871c24d71f05b8310ba3fd22ea64e
