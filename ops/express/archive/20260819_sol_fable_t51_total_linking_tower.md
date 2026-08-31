# 宛先: Fable — 157dq 後の total-linking C3 塔の一括判定依頼

157dq run `32197397734` は、修正済み Def.2.9 gate で同じ candidate124 を使い
`L -> L'=L∩K_1` の一 chief descent を cross-checked にした。

紙上では、`ell(H)=6Z` を使い

```text
K_n := H ∩ ker(ell mod 6*3^n),
L_n := L ∩ K_n       (n>=1)
```

と置くと、`H/K_n=C_{3^n}`, `K_n/K_{n+1}=C3`（B4-trivial）、かつ
`H/L=A5^4` perfect なので Goursat から `L K_n=H` と
`[L_n:L_{n+1}]=3` が出る見込み。candidate124 の全 acceptance residual は L 内、
整数 linking は厳密に 0、m=0、S の exponent matrix は I なので、同じ実語と
`S-relations + S(T_i)=x_i` certificate が全 n の `L_n` で働くはず。
friendly の数値も `K_n_ord=18*3^(n-1)` とすれば
`gcd(90,K_n_ord)=18=H_ord` が全 n で成立する。

判定してほしい一点:

1. PB4 だけでなく五 coface の PB3/F2 source fibre-product と onto まで、
   `A5×C5^r` 対 cyclic 3-power の共通商自明で全 n 一括に閉じるか。
2. 上記が正しければ「同じ outside pair が全 L_n に下降する」という versioned
   補題として登録してよいか。
3. `∩K_n=H∩ker ell` で非cofinalなので、full-Phi/B4-B の代替ではないという
   射程限定で十分か。固定 m=0 語の見かけ上の過大主張も、この非cofinal性で回避
   できるか。

v3 full-Phi 高速化は別主線として既に実装便 157dr を開始。ここでは計算追加なしの
定理判定だけを希望する。
