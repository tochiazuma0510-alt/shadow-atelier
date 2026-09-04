# R07 endpoint signature の有限生成 cache 補題（v495）

## 0. 境界

本紙は Task640 A0 producer の endpoint-signature 部分だけを扱う。A0 の
MEMBER/NONMEMBER、COMMON、cofinal lift、fake、Ihara は主張しない。
実 run `33813729918/1` は `endpoint_minimal_step_7_zero_word_canary`
の内部で外側 45 分 timeout（exit 124）になり、rho2 artifact を残していない。

## 1. 記号

固定した 31 個の context のうち Task640 が使う十座標を

\[
 q_i:F_2\longrightarrow E_3\quad(0\le i<5),\qquad
 q_i:F_2\longrightarrow E_4\quad(5\le i<10)
\]

と書く。前半は `delete \circ E4.eval`、後半は `E4.eval` である。
Task176 の認証済み deletion が準同型であることを前提に、各 \(q_i\) は群準同型である。
raw endpoint と occurrence signature を

\[
 Q(w)=(q_0(w),\ldots,q_9(w)),
\]

\[
 S(w)=(q_0(w),q_1(w),q_2(w),q_3(w),q_0(w),q_4(w),
       q_5(w),\ldots,q_9(w))
\]

と置く。二度現れる \(q_0\) は、六本の B3 occurrence と五本の B4
occurrence を並べる `TEN=(0,1,2,3,0,4,5,6,7,8,9)` そのものである。

## 2. 補題（空語と右 recurrence）

成分積を \(\odot\) と書けば、任意の語 \(u,v\in F_2\) に対して

\[
 Q(1)=(1_{E_3})^5\times(1_{E_4})^5,
 \qquad Q(uv)=Q(u)\odot Q(v),
\]

および

\[
 S(1)=(1_{E_3})^6\times(1_{E_4})^5,
 \qquad S(uv)=S(u)\odot S(v)
\]

が成り立つ。

### 証明

`MatchedQuotient.eval` は語を左から読み、現在値の右へ各 marked image
を掛けるので `eval(uv)=eval(u)eval(v)` である。空語では loop が空で
identity を返す。後半五座標は従って主張を満たす。前半五座標はさらに
認証済み準同型 `delete:E4->E3` を合成したものなので同じ等式を満たす。
座標の反復と並べ替えは成分積を保つため、\(S\) にも同じ等式が従う。□

## 3. 系（四 atom だけで全 trie を決める）

自由簡約 path の alphabet は

\[
 A=\{-2,-1,1,2\}
\]

である。最初に四本 \(S(a)\;(a\in A)\) を一度ずつ直接評価する。
trie root を上の明示 identity とし、edge \(p\to pa\) に対し

\[
 S(pa):=S(p)\odot S(a)
\]

と定義すれば、深さに関する帰納法により全 node で直接評価値と一致する。

従って production で必要な generic endpoint evaluation 回数は、trie
構築について次で十分である。

```text
empty word                         0
four actor atoms                   4
all-prefix direct comparison       0
```

四 atom の正しさと成分積の向きは bounded fixture で独立に検査できる。
全 prefix を再び `signature(prefix,...)` で直接評価することは、帰納法で既に
保証された等式を node 数だけ再計算するだけであり、探索の完全性を増さない。

## 4. seed endpoint との分離

Task640 の reached relator seed（高々44本）に対する endpoint-identity gate
は、trie path の評価とは別の数学条件である。これは削除せず各 seed を一度
直接評価する。また `direct_column` と precision-2 aggregation も本紙の
cache 置換では変更しない。

従って v495 の置換は候補宇宙、係数、bucket 同値関係、lower-zero 条件、
rho2 を変えず、冗長な evaluator 呼出しだけを有限生成 recurrence に置き換える。

## 5. 昇格条件

実装は最低限次を満たす必要がある。

1. raw empty endpoint は identity から直接構成する。
2. atom 四本を一回ずつ cache する。
3. `extend_signature` は cache の atom を右から掛ける。
4. production の全-prefix direct replay はゼロ回にする。
5. toy direct evaluation と recurrence の固定小例一致を selftest する。
6. 実 parent 上の rho2 は別 checker が再生する。

これは A0 producer の runtime 補題であり、A0 自体の判定ではない。
