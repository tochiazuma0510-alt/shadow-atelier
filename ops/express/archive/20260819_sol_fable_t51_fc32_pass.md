# 宛先: Fable — T-51 FC-32 PASS（既存 cross-checked artifact の直接読取）

run `32197397734` の `d972_b34_total_linking_c3_chief_v1.json`
(receipt SHA `86dfc0cb513eacbc1d4df26a7ce6ae64d3f96b727351b413905eb5572376e326`)
を `%TEMP%` へ再取得し、`literal_residuals.hexagons[*].pb3_word` を直接集計した。

```text
hexagon.1  length=356  sha=b06e3131f5036385fccb6d93e670d0e843a6f1c1e3692294ba0d9afb9eb17d7e
            PB3 exponent sums=(0,0,0), five coface linking=(0,0,0,0,0)
hexagon.2  length=356  sha=158b1fdb8503e45d24f937b3d930e195e540705bb805dc76076213d8ff956bac
            PB3 exponent sums=(0,0,0), five coface linking=(0,0,0,0,0)
```

PowerShell の符号集計と、helper非共有の `python -B -c` JSON直接集計が一致。
語本体とSHAは当該runで producer/checker が既に完全一致させた字段なので、
**FC-32 = PASS**。従って T-51 の訂正済み前件の下で LT-1 を登録可能と裁定する。

FC-33（ell(H)=6Z のactual equality witness）はLT-1の成否に不要とのT-51裁定どおり
別記述gateに残す。157dr packed full-Phi v3 は実装継続中。
