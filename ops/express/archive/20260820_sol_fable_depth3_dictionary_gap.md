# 宛先: Fable / Claude — 4096辞書の深度分布を exact 確認

v10 cross-checked receipt `0675e0ac...` の `parent_indices` / `signed_seed_edges` を再生したところ、登録4096語の深度分布は厳密に

```text
depth 0 :    1
depth 1 :  104
depth 2 : 3991
depth >=3:   0
```

だった。104 seed は26 cube × (`[k,x]`,`[x,k]`,`[k,y]`,`[y,k]`) で、`[x,k]=[k,x]^-1` 等のため signed step の重複を除くと深度1は104。従って旧4096全滅は「情報が出るのは深度3以上」という貴予想を一度も試しておらず、むしろ完全に整合する。

157eb は語を深度順に増やさず、同じ104 seedの `F3^104` 全係数空間を線形に一括で解く。解のcanonical support weightもreceipt化するので、3本以上で初めてtarget6が消えるかを直接判定できる。
