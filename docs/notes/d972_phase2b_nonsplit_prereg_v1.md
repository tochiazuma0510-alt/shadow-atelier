# D972 Phase 2b — 非分裂 $2^6\!\cdot\mathrm{PSL}(2,8)$ 窓の事前登録 v1

- 凍結日: 2026-08-13
- 実験 ID: `PH2B-NS64-v1`
- 対象: $M=K^{(9)}\cap N_{S4}$ への reduction
- 候補: GAP perfect-groups library の `PerfectGroup(32256,2)`、表示名 `L2(8) N 2^6`
- 状態境界: 本書の固定時点では公式 producer による shadow 像を作っていない。

## 0. 非盲検であること

実装可能性を調べる engineering probe が本書より前に行われ、候補の生の像サイズも作業者には見えている。したがって

```text
engineering_probe_before_freeze = true
preregistration_blind = false
```

である。本書は予測の成功を主張するための登録ではなく、公式走査で候補・順序・分岐をすり替えないための固定票である。

## 1. 先行する規模ゲート

測定を含まない preflight は次に固定した。

| artifact | SHA-256 |
|---|---|
| `search/d972_phase2b_gate_v1.py` | `fdbb4dcadef7a3f3aaea8182bec0daca3cfceee1f545035ab70f6c077d1f7c43` |
| `search/check_d972_phase2b_gate_v1.py` | `123ee710fcafc3557af834e506e5ec974cf2d28e7224af9bb30bba0d5a466c8f` |
| `search/certs/d972_phase2b_gate_v1_20260813.json` | `d02c00bb62403ab7298605eb540b0f9745847ca4c71f4fb00acdf5e948e97eca` |
| `search/certs/d972_phase2b_gate_v1_check_20260813.json` | `44a1f05becfc2604c8ddb664d47820b5389c232f6b22a32a0f82f00f60799b46` |

固定した規模は

\[
|E|=32256=64\cdot504,
\quad |G_9\times E|=2916\cdot32256=94{,}058{,}496,
\]

候補走査の上限は $6|E|=193{,}536$ 組、ライブラリ置換作用の次数は 72、hard timeout は 900 秒である。preflight cert の `measurement_performed` と `reduction_image_formed` はともに `false` である。

## 2. 候補と標識の固定

### 2.1 群

GAP 4.16.0 の `grp/perf5.grp` にある 9 生成元表示

\[
E=\langle a,b,c,u,v,w,x,y,z\rangle,
\qquad V=\langle u,v,w,x,y,z\rangle
\]

を使う。ライブラリ指定の部分群 $\langle avw,c,x\rangle$ による次数 72 の coset action を構成する。$V$ は位数 64 の核、$E/V$ は位数 504 の商でなければその場で終了する。

probe 後のラベル選択を次の語に固定する。

```text
S = accbxbccb
T = cacaccwb
W = S*T^-1
X = W^2
Y = S^-1*X*S
```

ここで通常の群積を左から評価し、paper の列積を実装する `AbstractProd` だけはリストを反転して評価する。要求する次数は $|S|=2,|T|=3,|W|=9,|X|=|Y|=9$、かつ $\langle X,Y\rangle=E$ である。

### 2.2 商の標識

$E/V$ 上の $(\bar X,\bar Y)$ を 9 点作用の既登録 $\mathrm{PSL}(2,8)$ 標識へ送る。位数 9 の生成対の総数が 1512 で、標識の自己同型軌道も 1512 であることを再計算し、この同定を固定する。これにより $N_E\subseteq N_{S4}$ として reduction を定義する。

## 3. 測定前ゲート — この順序を変更しない

公式 producer は次の段階を checkpoint に書き、G0 から G5 までの raw boolean がすべて `true` になった後だけ像集合を作る。

1. **G0/library-action**: ライブラリ SHA、coset degree 72、$|E|=32256$。
2. **G1/kernel-quotient**: $V\triangleleft E$、$|V|=64$、全非単位元の位数 2、$|E/V|=504$、標識付き商が既登録 $P=\mathrm{PSL}(2,8)$ と一致。
3. **G2/PH2-VOID**: $E$ が perfect、$V$ が既約、固定商標識の 512 個の位数 $(2,3)$ lift 対のどれも $V$ と自明に交わる補群を生成しないことを再計算する。perfect な $E$ は $(\text{可解})\times P$ にはなり得ないため、旧 PH2-VOID の完全分離条件は `false` でなければならない。
4. **G3/source-roof**: $G_9$ は可解、$E$ は perfect なので共通の非自明商はない。従って純商を $G_9\times E$ とする。これは $(\text{可解})\times P$ ではない。
5. **G4/nonempty**: $E$ の reduced-hexagon shadow を全列挙し、個数が正であることを記録する。この段階では reduction 像の集合化・個数化をしない。
6. **G5/isolated**: 下記の標識付き表示を使って全 source shadow の自己写像を settled とし、$N_E$ が isolated であることを有限検査する。既知の isolated $K^{(9)}$ との交叉命題から $K^{(9)}\cap N_E$ も isolated とする。

G0–G5 のいずれかが `false` または未確定なら `raw_image_size=null` のまま終了する。

## 4. isolatedness 用の固定表示

$X=x_0,Y=x_1$ とし、公式 producer/checker は次の 10 語を関係語として固定する。

```text
x_0^9
x_1^9
x_1^-1*x_0^4*x_1^-1*x_0^4
x_1^4*x_0^-1*x_1^4*x_0^-1
x_1^-1*x_0^-2*x_1^-1*x_0^-1*x_1*x_0^-1*x_1*x_0^-1*x_1*x_0^-1*x_1^-1*x_0^-2
x_1^-2*x_0^-2*x_1^-2*x_0^2*x_1^-1*x_0^-1*x_1^-1*x_0^-1*x_1^2*x_0^-2
x_1*x_0*x_1^-1*x_0*x_1*x_0*x_1^-1*x_0*x_1*x_0*x_1^-1*x_0*x_1*x_0^-3
x_1*x_0*x_1*x_0^-1*x_1^-1*x_0^-1*x_1^-2*x_0*x_1^2*x_0^-2*x_1^-1*x_0^2
x_1^3*x_0*x_1*x_0^-1*x_1^-1*x_0*x_1*x_0^-1*x_1^-2*x_0^4
x_1*x_0^-2*x_1^-1*x_0*x_1^-1*x_0^2*x_1^-1*x_0*x_1^-1*x_0^2*x_1^-1*x_0^-3
```

まずこれらが $E$ をちょうど位数 32256 で表示することを coset action と照合する。各 source shadow $(m,f)$ の像

\[
X\longmapsto X^{2m+1},\qquad
Y\longmapsto \operatorname{AbstractProd}(f^{-1},Y^{2m+1},f)
\]

が 10 関係を満たすことを検査する。像が $P$ を生成し、拡大が非分裂で $V$ が既約なら像は $E$ 全体である。従って得られる自己準同型は有限群 $E$ の自己同型であり、対応 shadow は settled である。この論証を全 shadow に適用する。

## 5. 公式測定と凍結スペクトル

G0–G5 の後に限り、$E\to E/V\cong P$ で source shadow を $N_{S4}$ の 54 shadow へ送る。屋根の $K^{(9)}$ fibre は各 $u$ に 18 個なので

\[
|\operatorname{Im}R_{K^{(9)}\cap N_E,M}|
=18\,|\operatorname{Im}(GT(N_E)\to GT(N_{S4}))|.
\]

事前登録スペクトルは

\[
\boxed{\{324,972\}}
\]

だけとする。分岐は次のとおり。

- raw integer が 324: 対応する有限 A 側 certificate を保存する。ただし上位の定理候補前件を別記する。
- raw integer が 972: `status=UNKNOWN` とし、この候補を尽くした旨だけを記録する。次候補探索は可能だが、有限深度から B 型を認定しない。
- それ以外の整数: raw integer と全ゲートを保存し、意味づけをせず終了する。
- null: 測定前ゲートの終了理由だけを保存する。

旧 $K^{(l)}\cap N_{S4}$ 族の 324 分岐は PH2-VOID により到達不能なので撤回済みである。この Phase 2b のスペクトルは、完全直積でないことと isolatedness を先に確定した別候補にだけ適用する。

## 6. 検疫と名前

- $u,c$ および封印 K5 の数値を読まない。
- 既登録量を書き換えない。
- `PH2B-NS64-v1` は E1-S3、FAM-V2-S3、P8-v3.2-S-3 のどれとも別 namespace とする。
- `verified` は用いず、producer/checker の一致は `cross-checked` とだけ記す。
