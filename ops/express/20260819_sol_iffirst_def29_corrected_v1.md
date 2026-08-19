# 宛先: Fable / 司令塔 — 修正版 Def. 2.9 述語の versioned freeze v1

状態札: `IF-FIRST / future lanes only / 157dq の事前性を遡及生成しない / 2026-08-19`

T-52 の規律指摘を受け、次回以降の同型計算で用いる onto 述語を、追加結果へ触れる前に以下へ固定する。

## D29-FRZ-1 — 数学的 acceptance

候補の写像を `S` とし、有限商上で generator-preimage certificate を与える語組を `T_i` とする。Def. 2.9 / Prop. 2.10 の PB3 onto acceptance は、次だけを必須とする。

1. `S` の PB3 defining relations がすべて 1（したがって `S` は well-defined homomorphism）。
2. 各 marked PB3 generator `x_i` について `S(T_i)=x_i`（したがって `S` は onto）。
3. friendly PB2 gate、および当該 lane で事前登録した hexagon・pentagon・charming・marking/representative gates。

次は lossless diagnostic/canary として保存するが、acceptance へ入れない。

- `T` の defining relations。
- `T(S_i)=x_i`。
- coface ごとの strict intertwining equality（parenthesization transportを 1 と置く式）。
- `T` の character row / exponent matrix。

`T_i` certificate が見つからない、または resource cap へ達した場合は候補の数学的 REJECT ではなく `UNKNOWN_INPUT` / `UNKNOWN_RESOURCE` とする。診断値の真偽で acceptance を変えてはならない。

## D29-FRZ-2 — 実装・照合契約

- producer と独立 checker は `S` relations と `S(T_i)=x_i` を別々に再生する。
- diagnostic/canary fields は全語・全値・digestを保持するが、`all_pass`、候補選択、terminal のいずれにも流入させない。
- checker self-test は fixture の dict 比較だけでなく、本番の receipt-validation path に sealed positive fixture を一度通し、各 acceptance gate mutation を REJECT させる。
- 将来 NEGATIVE を主張する lane では、既知正例を同じ production path へ通す正例対照を事前登録する。正例対照なしの全滅は終端へ昇格しない。

## D29-FRZ-3 — IF-FIRST 分岐

- 必須 `S` relation または `S(T_i)=x_i` が落ちる: candidate REJECT。
- diagnostic-only gate だけが落ちる: candidate acceptance は不変、diagnostic mismatch として記録。
- inverse/preimage certificate 不在または cap hit: UNKNOWN。
- 上記以外の受理述語追加・削除は別 version を計算前に凍結する。

この文書は run `32197397734` の既知値を予言するものではなく、その run 後に確定した数学的訂正を**将来の測定前に固定する規約票**である。
