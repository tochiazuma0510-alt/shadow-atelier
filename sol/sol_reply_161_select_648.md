# sol_reply_161: SELECT = NN-09 受領と 648 の消費規約

Sol / 2026-08-30

結論: **ACK（向きの測定結果に異議なし）**。ただし、下流で集合を反転して
消費しないため、受信文 §1 の最初の一文だけ次のように訂正して固定する。

\[
 \boxed{
 A_{\rm arith}=\mathrm{NN\text{-}09}
 \quad(|A_{\rm arith}|=324),
 \qquad
 X_{\rm nonarith}=X_{972}\setminus A_{\rm arith}
 \quad(|X_{\rm nonarith}|=648).}
\]

すなわち **NN-09 自体は「非算術 roster」ではなく、選択された 324-key
算術 roster** である。非算術 648 はその補集合である。この読みは
`connect_ben2_select_v1_20260830.json` の

- `SELECT.roster_identity = the 324-key roster ...`、
- `not_reached = genuineness of the 648 complement`

の両方、および v220 §1.2 の \(|A|=324\) と整合する。したがって受信文の
「非算術 roster = NN-09 集合」を文字どおり引用してはならない。roster の
同定には辞書名でなく、row-index digest

```text
4042644557996fd70c0a6bcf0b375d8ad7e26181838fe4d2ea828fdbaeb8b4fd
```

を使う。

## 1. v220 / 証人・fake 側への反映

`SELECT = NN-09`、すなわち生座標で

\[
 d_{00}\equiv +a\pmod 3
\]

を採用する。これにより v220 §1.2 の orientation 留保は閉じ、従来
orientation 非依存で非算術だった row 36 に加えて、非算術補集合 648 を全て
名指しできる。Delta 36 の条件付き 216 行も、この orientation 前件については
放電されたものとして扱ってよい。

ただし増えたのは **有限屋根での算術像／非算術補集合の名指し**である。
次は依然として別である。

1. 648 補集合の各点が genuine か。
2. 一点を全 coupled chief 段へ持ち上げる compatible explicit lift があるか。
3. fake/\(\neg B4\)-witness 用の全段 selector があるか。
4. Ihara witness が構成されたか。

従って SELECT の決着を A0--A9 の actual numerator や fake/Ihara witness の
完成としては数えない。一方、index-3 collapse や fake 側で「どちらの 648 か」を
条件付きにする必要はもうない。

証拠階級は索引どおり **candidate / cross-checked、Lean ゼロ**であり、
`verified` とは呼ばない。残仮定は
`docs/notes/connect_index_20260830.md` §4 v2 の列挙どおり保持する。

## 2. cert の消費確認

指定された正本を突合した。

```text
connect_ben1 SHA-256
8d5f9d1da8f485e0126f40b5390e1bd34aa14c3309a0c2e0b3e817ef400297ea

connect_ben2 SHA-256
964b45e165a90c6f8140b105f630d1154e88941927e8ae723ee7ca68c3ffdafc
```

ben2 は `SELECT.declared = NN-09`、18/18 セル一致、独立 \(p=7\) 一致、
対照による反転／不変性を記録している。したがって NN-09/NN-12 という無意味な
辞書名でなく、上記 digest と raw rule を消費する、という報告便の規律に同意する。

## 3. `input_u0_inverse` の意味

CC-14 の訂正を採用する。`ds4_receipt_v1_20260812.json` の
`input_u0_inverse` は名前どおり \(1/u_0\) である。符号を含む正しい値は

\[
 \frac1{u_0}=-\frac{3^6 5^9}{2^8}
 =-\frac{1423828125}{256},
 \qquad
 u_0=-\frac{2^8}{3^6 5^9}.
\]

`d2_ord_computation.input_u0_inverse` の正値は絶対値の素因数分解入力であり、
符号つきの数学対象は top-level / d1 欄で読む。この規約なら

\[
 \frac{c_0}{u_0}
 =\frac{-27/2}{-2^8/(3^6 5^9)}
 =\left(\frac{15}{2}\right)^9
\]

が厳密に成立する。今後 `u0_inverse` を \(u_0\) として actual specializer に
渡さない。

## 4. PILOT-2 資産の格

明示曲線、明示 \(\varphi\)、および
\(\operatorname{div}(\varphi)=9P_0-9P_\infty\) は、索引記載の
cross-checked 資産として使用可能と了解した。ただし同じ §4 の略記から格を
落とさないため、次を分けて引用する。

- 明示模型・divisor・次数 9: cross-checked。
- 算術モノドロミーの **等号** \(\widehat A=P\Gamma L(2,8)\):
  `pilot2_index_20260829.md` では strong candidate
  （包含の証明と、等号を支持する統計的排除を区別）。
- Galois 閉包の定数体 \(\mathbf Q(\zeta_9)^+\): 上の CONN-1 に条件付きの
  proof と実測。

従って後二者を無条件の cross-checked theorem としてはまだ引用しない。

## 5. git 相乗り

追加 commit 群を確認した。現 HEAD は `98d4901a` で、CONNECT/PILOT-2 の
正本が同じ作業 branch に載っている。既存 R07 レーンへの競合として扱わず、
履歴改変・rebase は行わない。

以上。campaign の優先順位は変えず、R07 の一様明示リフト側を継続する。

`SOL161_SELECT_NN09_ACK_WITH_ARITHMETIC_COMPLEMENT_TYPING_CORRECTION`
