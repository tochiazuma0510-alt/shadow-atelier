# Sol 便 148 返信

## 進行記帳 0 — 受領と範囲固定

- 受信便 `ops/inbox_codex/sol_task_148_dovetail.txt` は、先頭から末尾まで全番号節を受領した。
- 受信便 SHA-256: `8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9`。
- 第 1 節（A 側）は、無上限の有限商 dovetail の数学仕様・完全性条件・停止証明書をここで裁定し、Sol の役割契約に従って実装作業を Luna 指示書へ切り出す。
- 第 2 節（B 側）は、既知の dihedral 明示式と kernel $C_2$ の nonsplit lift を初期データとして、outside-$A_{\rm ar}$ 元一つの全深度互換 lift が構成できるかを監査する。
- 未達を成功扱いせず、Lean 証明書のない結果に `verified` を用いない。

## 1. A 側 — dovetail の数学仕様

### 1.1 列挙対象を巨大乗法表から relative extension へ替える

\[
Q_0:=PB_3/M,\qquad |Q_0|=1{,}469{,}664,\qquad
\bar Q:=B_3/M,\qquad |\bar Q|=6|Q_0|=8{,}817{,}984
\]

と置く。kernel order $k$ の一候補は、marked-over-$\bar Q$ 同型類

\[
(\bar E,s_1,s_2,\rho),\qquad
\rho:\bar E\twoheadrightarrow\bar Q
\tag{1}
\]

であって、$\bar E=\langle s_1,s_2\rangle$、$s_1s_2s_1=s_2s_1s_2$、
$\rho(s_i)=\bar\sigma_i$、$|\ker\rho|=k$ を満たすものとする。
$B_3\to\bar E$ の kernel を $L$ とすれば $L\le M$ であり、
$\bar E\to\bar Q\to S_3$ の kernel は $PB_3/L$ である。従って

\[
|PB_3/L|=k|Q_0|,\qquad [M:L]=k.
\tag{2}
\]

逆に委嘱中の任意の $B_3$-安定 marked extension は $\bar E=B_3/L$ として
(1) に現れる。生成対を固定する同型は高々一つなので、base と二生成元を保つ同型で
割れば

\[
\{\text{(1) の marked-over-base 同型類}\}
\longleftrightarrow
\{L\triangleleft B_3:L\le M,[M:L]=k\}
\tag{3}
\]

は一対一である。これが「重複なし」の正確な semantic key である。

`d972_phase2_cofinal_execution_v1.md` §1 の全乗法表列挙は再帰的列挙の存在証明としては
正しい。しかし $k=3$ だけで

\[
|\bar E|=6\cdot3\cdot1{,}469{,}664=26{,}453{,}952
\]

であり、その乗法表を展開する producer は GHA の実運転にならない。実装は
$H=\ker\rho$（$|H|=k$）を先に取り、$\bar Q$ の $H$ による全拡大を列挙する
relative-extension engine にしなければならない。具体的には、位数 $k$ の全 $H$、
$\bar Q\to\operatorname{Out}(H)$ の全 abstract kernel、obstruction-zero の全拡大類、
標準二生成元の全 lift、base-fixing automorphism による marked orbit、の順である。
central/split/solvable 拡大だけに狭めては (3) の完全性を失う。

### 1.2 各候補の有限 gate

候補 $L$ ごとに次をこの順に行う。

1. 正典の charming universe を有限悉皆する。
2. full $B_3/L$ 上で (3.3), (3.4)、$T_{m,f}$ の全射性、source kernel を計算する。
3. 全 shadow の source が $L$ と一致するときだけ isolated とする。
4. isolated の場合だけ (3.60) を exact $m\bmod M_{\rm ord}$ で適用し、canonical 972 target keys の全 fiber を作る。

$c\notin L$ の場合は $\theta,\tau$ を quotient element へ直接作用させず、自由群語へ
作用させてから評価する `word_level_required` を使う。旧来の
$m\bmod(M_{\rm ord}/2)$ 判定も禁止する。

独立 checker は producer の helper、候補 shadow list、presentation settlement 判定を共有せず、
lossless extension witness から group/marking/factor map を再構成し、charming、full hexagon、
generation、synchronized Cayley/Schreier traversal による settlement、972 fiber vector を再計算する。

開始前 calibration は次で固定した。

| kernel order | marked orbit | isolated | $|GT(L)|$ | image | zero fiber |
|---:|---:|---|---:|---:|---:|
| 1 | 1（base） | yes | 972 | 972 | 0 |
| 2 split | 1 | yes | 972 | 972 | 0 |
| 2 nonsplit | 2 | yes | 1,944 / orbit | 972 | 0 |

この $k=1,2$ を二系統が再現して初めて $k=3$ を unlock する。§5.4 の kernel-2
分類は紙の列挙で独立 checker が無かったため、この calibration は単なる unit test ではなく
欠品していた第二系統にもなる。

### 1.3 空 fiber の停止証明

isolated $L\le M$ で一つでも

\[
R_{L,M}^{-1}(g)=\varnothing
\tag{4}
\]

なら、自然性により

\[
P_M:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})
\subseteq\operatorname{Im}R_{L,M}
\]

なので $g\notin P_M$ である。一方
$A_{\rm ar}\le P_M\le GT(M)$、$[GT(M):A_{\rm ar}]=3$ だから
$P_M=A_{\rm ar}$。従ってこの一件で 648 元全部が fake 側と決まる。
逆に 972/972 が有限個続いても B 側は何も決まらない。

停止札は、両系統が同じ isolatedness、$|GT(L)|$、image set、972 fiber vector、
zero-key set を再計算したときだけ `A_WITNESS_CROSSCHECKED` とする。Lean 証明書がないため
`verified` とは呼ばない。中間 image size、二系統不一致、state hash fork は witness ではなく
fail-closed STOP である。

### 1.4 無期限 GHA の意味

GHA の一 job は無期限にはできない。従って正しい workflow は、定期 schedule が有限時間 slice
を起動し、各 slice が hash-chain 付き checkpoint artifact を読み、最後の両系統一致 cursor から
再開する列である。単一 job の timeout 延長ではない。terminal state 後は同じ digest を返す
no-op とし、workflow 自身は commit/push/self-dispatch を行わない。

上記の producer/checker/workflow 実装契約を
`sol/luna_task_148_dovetail.md` に書いた。Sol は数学監査・設計のみという `AGENTS.md`
の役割契約に従い、本便で `search/` や `.github/workflows/` を変更してはいない。
従って A 側の現状態は **`IMPLEMENTATION_DISPATCHED_NOT_EXECUTED`** であり、実装済み・運転開始済みとは
報告しない。

## 2. B 側 — outside 元一つの逆極限構成を実際に試す

### 2.1 一元を固定する

canonical 972 tuple の順序を固定し、

\[
g_\star:=\min\bigl(GT(M)\setminus A_{\rm ar}\bigr)
\tag{5}
\]

とする。以下の障害は $g_\star$ の座標に依存しないので、648 元を列挙する必要はない。
現台帳には $A_{\rm ar}$ の 324 個の canonical key を lossless に並べた artifact が無いため、
(5) を未登録の具体 tuple に置き換えて捏造はしない。

### 2.2 dihedral 方向には明示的な互換 thread が作れる

\[
D_r:=K^{(9\cdot3^r)}\cap N_{S4}\qquad(r\ge0),\qquad D_0=M
\tag{6}
\]

と置く。$g_\star$ の $K^{(9)}$ 成分を Thm 4.3 の
$(m,(r^{2k},r^{-2k},r^{\varkappa(m)}))$ 座標で書く。同じ整数代表 $m,k$ を各
$9\cdot3^r$ で取れば、unit 条件と reduction compatibility を保つ。$N_{S4}$ 成分はそのまま
固定し、roof 等式

\[
GT(D_r)=GT(K^{(9\cdot3^r)})
\times_{(\mathbf Z/18)^\times}GT(N_{S4})
\]

で貼れば

\[
d_r\in GT(D_r),\qquad R_{D_r,M}(d_r)=g_\star,\qquad
R_{D_{r+1},D_r}(d_{r+1})=d_r
\tag{7}
\]

という明示的な部分 thread を得る。従って dihedral 方向そのものは障害ではない。

### 2.3 nonsplit $C_2$ 方向にも一段の lift はある

§5.4 の二つの nonsplit marked window の一つを $L$ とする。
$|GT(L)|=1{,}944$、image size 972 であり、各 target fiber は 2 点である。従って

\[
\ell_\star\in GT(L),\qquad R_{L,M}(\ell_\star)=g_\star
\tag{8}
\]

を二点のうち canonical に小さい方として選べる。ここまでは便 148 が指摘した二資源を
実際に一元へ適用できた。

### 2.4 二方向は別々には cofinal でない

奇数 $n$ で $|G_n|=4n^3$ なので (6) について

\[
[M:D_r]=\frac{|G_{9\cdot3^r}|}{|G_9|}=3^{3r}.
\tag{9}
\]

一方 $[M:L]=2$。もし $D_r\le L$ なら $2\mid3^{3r}$ となり矛盾する。従って
dihedral chain は $L$ の下へ一度も入らない。逆に kernel-$C_2$ step だけを反復して得る
index $2^s$ の chain は $D_1$ の下に入れない（$27\nmid2^s$）。従って両方向とも
単独では $M$ 以下の isolated refinements に cofinal でない。

### 2.5 `COPRIME-GLUE-148` — 最初の mixed intersection は通過できる

Prop. 3.15 により

\[
J_r:=D_r\cap L
\tag{10}
\]

は isolated である。最終監査では、ここは停止点ではなかった。相対 kernel の位数が互いに素な
ため、(7) と (8) は実際に貼れる。

$H^F:=H\cap F_2$ と書く。$D_r,M$ は $c$ を含み、§5.4 の nonsplit $E_1$ は
$x,y$ の lift だけで生成されるので

\[
[M^F:D_r^F]=3^{3r},\qquad [M^F:L^F]=2.
\tag{11}
\]

従って $D_rL=M$、$D_r^FL^F=M^F$ であり、full pure quotient と $F_2$ quotient は
それぞれ対応する fiber product に等しい。$m$ の法は

\[
D_{r,\mathrm{ord}}=18\cdot3^r,\qquad L_{\mathrm{ord}}=36,\qquad
\gcd(18\cdot3^r,36)=18=M_{\mathrm{ord}},
\]

なので、$M$ で一致する二つの $m$ は CRT で $J_r$ の法へ一意に貼れ、unit 条件も保たれる。

残る charming 条件も互いに素な kernel で閉じる。一般に

\[
P=A\times_C B,\qquad
|\ker(P\to A)|=2,\qquad |\ker(P\to B)|=3^{3r}
\]

とし、$(a,b)\in A'\times_{C'}B'$ を取る。その $P_{\rm ab}$ での像は
$P_{\rm ab}\to A_{\rm ab}$ と $P_{\rm ab}\to B_{\rm ab}$ の両 kernel に入る。前者は
2-primary、後者は 3-primary なので交叉は零、従って $(a,b)\in P'$ である。これを
$P=F_2/J_r^F$ へ適用すると、(7), (8) の二つの $f$ は一つの
$f_{J_r}\in(F_2/J_r^F)'$ に貼れる。

二 hexagon は二因子で成立するので fiber product でも成立する。二つの settled map は
$M$ 上で同じ $g_\star$ に reduce し、componentwise inverse を持つ fiber-product
automorphism を定めるので generation と settlement も保たれる。よって一意な

\[
j_r\in GT(J_r),\qquad
R_{J_r,D_r}(j_r)=d_r,\qquad R_{J_r,L}(j_r)=\ell_\star
\tag{12}
\]

が得られる。一意性から $j_{r+1}$ は $j_r$ へ reduce する。従って既知資源は
dihedral と一つの nonsplit $C_2$ を同時に含む互換 thread まで明示的に延びる。
これは紙の補題であり、独立 checker も Lean 証明書も無い。

### 2.6 中央 kernel-$C_2$ の三窓は一つにまとめられる

§5.4 の三つの index-2 kernel を、split を $L_{\rm s}$、nonsplit で
$c\mapsto1,z$ のものを $L_0,L_1$ と書く。§5.4 の標準 marking では

\[
PB_3/L_{\rm s}=E_0=Q_0\times C_2,\qquad
PB_3/L_0=E_1,\qquad
PB_3/L_1=E_1,
\]

split 側では $x,y$ が $Q_0$ 成分に入り $c$ が新しい中心元を生成し、nonsplit 側では
$x,y$ の lift が既に $E_1$ 全体を生成する。従って

\[
K_2:=L_{\rm s}\cap L_0,\qquad
PB_3/K_2\cong E_1\times C_2,\qquad [M:K_2]=4.
\tag{13}
\]

この表示で $x,y\mapsto(\widetilde x,1),(\widetilde y,1)$、$c\mapsto(1,z_{\rm s})$。
写像

\[
E_1\times C_2\longrightarrow E_1,\qquad
(e,z_{\rm s}^{\epsilon})\longmapsto e z^\epsilon
\]

は $c\mapsto z$ の第三 marking へ factor するので $K_2\le L_1$。よって
$K_2=L_{\rm s}\cap L_0\cap L_1$ である。

$g_\star$ の $L_{\rm s}$-lift は一意、$L_0$-lift は二点から一つ選べる。両者の
fiber product の $F_2$ quotient は

\[
E_1\times_{Q_0}Q_0\cong E_1
\]

なので、nonsplit 側の charming $f\in E_1'$ がそのまま共通 lift になる。$m$ は
法 36 と法 18 で既に整合し、二 hexagon と settlement は componentwise に貼れる。
従って

\[
k_\star\in GT(K_2),\qquad R_{K_2,M}(k_\star)=g_\star
\tag{14}
\]

を明示的に得る。これは三つの central kernel-$C_2$ window 全てへ reduce する。

### 2.7 dihedral thread と中央 $2^2$ 座標も貼れる

\[
C_r:=D_r\cap K_2.
\tag{15}
\]

相対 kernel orders は $3^{3r}$ と $4$ で互いに素く、$F_2$ 側でも
$3^{3r}$ と $2$ で互いに素い。従って §2.5 と同じ CRT・可換化・componentwise
automorphism の証明により一意な

\[
c_r\in GT(C_r),\qquad
R_{C_r,D_r}(c_r)=d_r,\qquad R_{C_r,K_2}(c_r)=k_\star
\tag{16}
\]

があり、$c_{r+1}$ は $c_r$ へ reduce する。また

\[
[M:C_r]=4\cdot3^{3r}.
\tag{17}
\]

従って Thm 4.3 の全 dihedral $3$-tower と、§5.4 の central kernel-order-2 event
三行全てを同時に含む明示的互換 thread までは構成できた。

### 2.8 次の具体的な未閉鎖点 — 非中央 $C_2^6$ 窓

`docs/notes/d972_phase2b_nonsplit_report_v1.md` の

\[
W:=K^{(9)}\cap N_E,\qquad
1\to C_2^6\to PB_3/W\to Q_0\to1
\]

を取る。これは isolated、$|GT(W)|=7{,}776$、reduction image 972 なので、各 target
fiber は 8 点である。従って $g_\star$ の lift $w_\star\in GT(W)$ は存在する。一方

\[
[M:W]=64.
\tag{18}
\]

もしある $C_r\le W$ なら $64\mid4\cdot3^{3r}$ となり矛盾する。従って $(C_r)$ は
この既知 isolated refinement に対してすら cofinal でない。

次に必要なのは

\[
H_r:=C_r\cap W,\qquad
R_{H_r,M}^{-1}(g_\star)\ne\varnothing.
\tag{19}
\]

ここでは両相対 kernel が非自明な 2-part を持つので `COPRIME-GLUE-148` は使えない。
また $W$ の $C_2^6$ は非中央・非分裂であり、§5.4 の central $C_2$ 座標へ分解できない。
既存計算は $C_r$ と $W$ を別々に全射としただけで、その交叉 (19) の
`REL-VANISH` / `CHAR-LIFT` / generation compatibility を与えていない。
Prop. 3.15 は $H_r$ の isolatedness を与えるが、fiber の非空性を与えない。

全 isolated refinements $N_1,N_2,\ldots$ を列挙して

\[
K_d=M\cap N_1\cap\cdots\cap N_d,\qquad
Y_d(g_\star)=R_{K_d,M}^{-1}(g_\star)
\]

とすれば $(K_d)$ は cofinal になる。だが各 $Y_d(g_\star)\ne\varnothing$ を示すことは
まさに B 側の全深度 survival である。これを仮定すれば有限集合の compactness から逆極限は
非空になるが、その仮定は既知の central-$(2^2)$ plus dihedral thread からは出ない。

### 2.9 B 側裁定

素指数 3 は「一つの genuine outside 元で 648 元全部が B 型になる」ことを与えるが、
その一元を全深度へ持ち上げる transition/gluing を与えない。今回構成できたのは

\[
\text{Thm 4.3 dihedral thread}
\quad+\quad
\text{central }C_2\text{ 三窓}
\quad\xrightarrow{\ \mathrm{COPRIME\mbox{-}GLUE\ }\quad}
\text{互換な central-}(2^2)\text{ plus dihedral thread}
\]

までである。非中央 $C_2^6$ 窓との交叉 (19) から先は現入力では構成できない。
従って **`NO_COMPATIBLE_INVERSE_LIMIT_CONSTRUCTION_FROM_CURRENT_INPUTS`** と裁定する。
これは逆極限元の非存在証明でも A 型の証明でもない。

## 3. 全番号節への回答

| 受信節 | 実行結果 | 格 |
|---|---|---|
| 1. A 側 producer/checker/workflow | 完全な relative-extension universe、dedup、二系統、checkpoint、terminal rule を固定し、許可された Luna 指示書へ実装発注 | `IMPLEMENTATION_DISPATCHED_NOT_EXECUTED` |
| 2. B 側一元 inverse limit | Thm 4.3 thread と central $C_2$ 三窓を一つの互換 thread に貼った。非中央 $C_2^6$ 窓との交叉が未閉鎖 | `UNKNOWN`, partial compatible thread only |

## provenance

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_148_dovetail.txt` | `8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9` |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |
| `docs/notes/d972_phase2_cofinal_execution_v1.md` | `97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e` |
| `docs/notes/d972_phase2b_nonsplit_report_v1.md` | `56f2465ed73c6299026c129fc70fcbe9ebbab028342687d8a18d0e625e1e27e7` |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` |
| `sol/luna_task_148_dovetail.md` | `e2ec32d145e86e22e26b7d8bdab276c325993629d76738ec4a273e1a5ec1aad2` |

- 新しい機械計算、commit、push、workflow dispatch は行っていない。
- 本便で変更したのは指定返信と、Sol 契約が明示的に許す Luna 実装指示書だけである。
- Lean certificate は無く、`verified` の語は用いていない。

FINAL: `A_IMPLEMENTATION_DISPATCHED; B_STOPS_AT_NONCENTRAL_C2^6_INTERSECTION; DICHOTOMY_REMAINS_UNKNOWN`
