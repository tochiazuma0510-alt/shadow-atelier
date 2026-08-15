# Sol 便 150 返信 — 非中央 \(C_2^6\) 窓との接着と共終性再監査

## 0. 受領と結論

`ops/inbox_codex/sol_task_150_bside.txt` の第 1 節から第 2 節までを順に全文処理した。受信便の SHA-256 は
`94881f9bb86bf1e4b9dfc590d842f9a9f7a71c9a66d109da392d1525ea3da11f` である。

結論は二段に分かれる。

1. 便 148 §2.8 の名指しされた停止点
   
   \[
   H_r=C_r\cap W
   \]
   
   は越えられる。相対 2-kernel の位数は互いに素ではないが、その \(Q_0\)-加群型が分離している。
   新しい紙上補題 `MODULE-SEPARATED-GLUE-150` により、全 \(g\in GT(M)\) について
   \(R_{H_r,M}^{-1}(g)\ne\varnothing\) であり、各 \(g\) には \(r\) に関して互換な lift thread がある。

2. これは 972 屋根の大域 A/B を決着しない。族 \((H_r)\) は isolated refinements 全体に共終でなく、
   実際には dihedral-roof 部分族の中ですら 2-primary 深さが頭打ちである。従って正確な大域裁定は
   **`UNKNOWN`** のままである。空 fiber は得ていないので A ではなく、全 isolated 細分を通る outside 元も
   得ていないので B でもない。

新補題とその \(H_r\) への適用は **paper candidate** である。Phase 2b の \(E,V\) に関する有限群入力は
cross-checked だが、便 143/148 の \(K_2\) marked model と本便の接着証明には独立 checker も Lean
certificate もない。従って全体を `cross-checked` または `verified` へ昇格しない。

## 1. Continue B

### 1.1 入力と記号

以下では \(N^F:=N\cap F_2\) と書き、

\[
Q_0:=PB_3/M\cong G_9\times P,\qquad P:=\mathrm{PSL}(2,8)
\tag{1}
\]

とする。便 143/148 の三つの central kernel-order-2 窓の交叉を \(K_2\)、Phase 2b の窓を

\[
W:=K^{(9)}\cap N_E,\qquad
1\longrightarrow V\longrightarrow E\longrightarrow P\longrightarrow1,\qquad
V\cong C_2^6
\tag{2}
\]

とする。既受理入力は

\[
\begin{aligned}
PB_3/K_2&\cong E_1\times C_{2,s},
&M/K_2&\cong C_2^2,\\
F_2/K_2^F&\cong E_1,
&M^F/K_2^F&\cong C_2,\\
PB_3/W&\cong G_9\times E,
&M/W&\cong V,\\
F_2/W^F&\cong G_9\times E,
&M^F/W^F&\cong V.
\end{aligned}
\tag{3}
\]

ここで \(M/K_2\) と \(M^F/K_2^F\) は central、従って自明 \(Q_0\)-加群である。一方 \(V\) は
非自明既約 \(Q_0\)-加群であり、\(E\) は perfect である。最後の \(F_2\) 行では \(c\in W\) を使った。
実際、\(Z(P)=1\) かつ \(V^P=0\) なので \(Z(E)=1\) であり、中心元 \(c\) の marked image は \(E\) で
自明になる。

法は

\[
(K_2)_{\rm ord}=36,\qquad W_{\rm ord}=M_{\rm ord}=18.
\tag{4}
\]

### 1.2 同じ 2-primary でも共通商は零である


\[
D:=M/(K_2W)
\]

と置く。これは \(M/K_2\cong C_2^2\) の商であると同時に、\(M/W\cong V\) の
\(Q_0\)-加群商である。\(D\ne1\) なら、\(V\) の既約性から \(D\cong V\) でなければならないが、
前者から \(|D|\le4\)、後者から \(|D|=64\) となり矛盾する。従って

\[
\boxed{K_2W=M.}
\tag{5}
\]

\(F_2\) 側でも、共通商は自明 \(C_2\) の商かつ非自明既約 \(V\) の商なので

\[
\boxed{K_2^FW^F=M^F.}
\tag{6}
\]

これは単なる位数の互いに素性ではなく、二つの 2-kernel が異なる \(Q_0\)-support を持つことによる
分離である。

### 1.3 `MODULE-SEPARATED-GLUE-150`


\[
J:=K_2\cap W
\tag{7}
\]

と置く。(5), (6) と normal-subgroup fiber-product 定理から、marked 同型として

\[
\begin{aligned}
PB_3/J
 &\cong (E_1\times C_{2,s})\times_{Q_0}(G_9\times E),\\
F_2/J^F
 &\cong E_1\times_{Q_0}(G_9\times E).
\end{aligned}
\tag{8}
\]

より明示的には

\[
\widetilde G_9:=G_9\times_{V_4}Q_8,\qquad
E_1\cong\widetilde G_9\times P
\]

と書けば

\[
PB_3/J\cong\widetilde G_9\times E\times C_{2,s},\qquad
F_2/J^F\cong\widetilde G_9\times E.
\tag{9}
\]

従って

\[
[M:J]=2^8,\qquad [M^F:J^F]=2^7,\qquad J_{\rm ord}=36.
\tag{10}
\]

> **`MODULE-SEPARATED-GLUE-150`.** 自然な reduction は GT shadow class の同型
> \[
> \boxed{
> GT(J)\ \cong\ GT(K_2)\times_{GT(M)}GT(W)
> }
> \tag{11}
> \]
> を与える。

**証明。** \(K_2,W\) 上の二つの shadow class が \(M\) 上で一致するとする。

まず \(m\) は法 \(36,18\) で整合し、両法の gcd が \(18=M_{\rm ord}\) なので、CRT により法
\(J_{\rm ord}=36\) の class へ一意に貼れる。unit 条件も \(K_2\) 成分から保たれる。

次に

\[
P_F:=F_2/J^F,\qquad
V=\ker(P_F\longrightarrow F_2/K_2^F)
\]

とする。\(V\) は非自明既約であるため \([Q_0,V]=V\)、従って \([P_F,V]=V\) であり
\(V\subseteq P_F'\) である。このため射影

\[
P_F^{\rm ab}\longrightarrow(F_2/K_2^F)^{\rm ab}
\tag{12}
\]

は同型になる。互換な二つの charming \(f\)-class が (8) に定める元を \(p\in P_F\) とすると、
その \(K_2\) 成分は導来群に属するので、(12) から \(p\in P_F'\) である。従って全射

\[
[F_2,F_2]\twoheadrightarrow P_F'
\]

により、一つの実際の \(f\in[F_2,F_2]\) を選べる。

ここでは \(c\notin K_2\)、従って \(c\notin J\) であることが重要である。商元へ
\(\theta,\tau\) を直接作用させる略式や reduced hexagon は用いない。選んだ literal \(f\)-word について
paper の full product relations (3.3), (3.4) を評価する。両射影では元の二 shadow により成立し、
(8) の fiber product への埋込みが単射なので \(J\) 上でも成立する。

最後に二つの settled automorphism は \(Q_0\) 上で同じ写像を誘導する。その componentwise map は
componentwise inverse を持つので (8) の fiber product の自己同型であり、source kernel はちょうど
\(J\) である。従って charming、full hexagon、SURJ、settlement が同時に貼れる。

逆に \(J\)-shadow の二射影は当然互換である。\(m\)-class は CRT、\(f\)-class は (8) の単射性で決まるので、
(11) は単射でもある。以上で (11) を得る。∎

一意性は shadow **class** に関するものである。入力された raw word strings を canonical に貼るという意味では
ない。上で選ぶ literal \(f\) は \(J^F\) を法としてのみ一意であり、代表語自体は非標準である。

Phase 2b で \(R_{W,M}\) は全 972 元上に像を持ち、便 148 の \(K_2\) 構成も各 \(M\)-target に適用できる。
従って (11) の系として

\[
\operatorname{Im}R_{J,M}=GT(M).
\tag{13}
\]

### 1.4 dihedral thread との再接着

便 148 の

\[
D_r:=K^{(9\cdot3^r)}\cap N_{S4},\qquad
C_r:=D_r\cap K_2
\tag{14}
\]

を使うと

\[
H_r=C_r\cap W=D_r\cap J.
\tag{15}
\]

\(D_r\) と \(J\) の \(M\) に対する相対 kernel orders はそれぞれ \(3^{3r}\) と \(2^8\)、
\(F_2\) 側では \(3^{3r}\) と \(2^7\) である。今度は互いに素なので、既受理の
`COPRIME-GLUE-148` が適用できる。また

\[
(D_r)_{\rm ord}=18\cdot3^r,\qquad J_{\rm ord}=36,\qquad
\gcd(18\cdot3^r,36)=18=M_{\rm ord}.
\]

従って

\[
\boxed{
GT(H_r)\cong GT(D_r)\times_{GT(M)}GT(J)
}
\tag{16}
\]

であり、

\[
\boxed{
[M:H_r]=2^8\,3^{3r},\qquad (H_r)_{\rm ord}=36\cdot3^r.
}
\tag{17}
\]

任意の \(g\in GT(M)\) を固定する。Thm. 4.3 から得る互換な \(d_r\in GT(D_r)\) と、(11) から得る
一つの \(j\in GT(J)\) を (16) で貼れば \(h_r\in GT(H_r)\) が得られる。一意性により
\(k:=R_{J,K_2}(j)\)、\(w:=R_{J,W}(j)\) と置き、\(d_r,k\) の便 148 型の glue を \(c_r\) と書けば、

\[
R_{H_{r+1},H_r}(h_{r+1})=h_r,\qquad
R_{H_r,C_r}(h_r)=c_r,\qquad
R_{H_r,W}(h_r)=w
\tag{18}
\]

である。特に

\[
\boxed{
\operatorname{Im}R_{H_r,M}=GT(M)\quad\text{for every }r\ge0.
}
\tag{19}
\]

よって固定した genuine outside 元 \(g_\star\) について、便 148 の停止点を越えた restricted compatible
thread

\[
(h_r)_r\in\varprojlim_r GT(H_r)
\tag{20}
\]

が存在する。これは一元だけでなく全 972 target に一様な紙上結論である。

### 1.5 共終性の反監査 — (20) は大域 B ではない

委嘱の「remaining stop」が大域 A/B の最後の停止点である、という前提は成立しない。反例として

\[
L_{144}:=K^{(144)}\cap N_{S4}\le M
\tag{21}
\]

を取る。Thm. 4.3 と Prop. 3.15 により \(L_{144}\) は isolated であり、偶数 level の
\(|G_n|=4(n/2)^3\) から

\[
[M:L_{144}]
=\frac{|G_{144}|}{|G_9|}
=\frac{4\cdot72^3}{4\cdot9^3}
=2^9.
\tag{22}
\]

もしある \(r\) で \(H_r\le L_{144}\) なら、有限指数の塔から \(2^9\mid[M:H_r]\) が必要である。しかし
(17) の 2-part は常に \(2^8\) であり矛盾する。従って

\[
\boxed{(H_r)_{r\ge0}\text{ は dihedral-roof 窓族に対してすら共終でない。}}
\tag{23}
\]

\(L_{144}\) 単独は `PH2-VOID` の admissible dihedral 窓なので像 972 であり、A witness ではない。
その役割は (23) の共終性反例である。次の未閉鎖交叉の一例は

\[
X_r:=H_r\cap L_{144}.
\tag{24}
\]

\(H_r\) と \(L_{144}\) の相対 kernel は 2-part を共有するため `COPRIME-GLUE-148` は使えず、
本便の module-separation 前件も \(L_{144}\) 側について証明されていない。二つの個別像が 972 であることから
\(X_r\) の像が 972 とは従わない。これは `MONO-CNF-139` / `NO-FINITE-B-140` の交叉 no-shortcut
そのものである。

従って (20) が与えるのは restricted inverse limit の元だけである。大域 B には、例えば
`d972_phase2_cofinal_execution_v1.md` の全 isolated refinements の累積交叉 chain 上で、同じ outside 元の
全 fiber 非空性を示す必要がある。現在はその定理がない。一方、本便は空 fiber を一つも与えないので A も
発火しない。

本節の正確な裁定は

```text
NAMED_W_STOP_CROSSED
H_r_REDUCTION_SURJECTIVE_FOR_ALL_972
H_r_RESTRICTED_COMPATIBLE_THREAD_EXISTS
H_r_NOT_COFINAL
GLOBAL_972_ROOF_A_B_REMAINS_UNKNOWN
```

である。

## 2. Operational — freeze 後は追記専用

- 便 150 §2 の指摘を受領した。凍結済みの返信 134, 135, 139, 140, 148 は本便で一切変更していない。
- 本返信 `sol/sol_reply_150_bside.md` は引渡し時点で本文を凍結する。以後訂正が必要な場合、既存本文を
  書き換えず、末尾に `## Erratum / 追補` を追加する。
- 本便では新しい実装・機械探索・commit・push・workflow dispatch を行っていない。Sol の作業は紙上の
  数学監査に限定した。
- 作業開始前から worktree には本件外の変更と未追跡物が多数存在した。本便が新規作成したのは指定返信
  ファイルだけであり、それら既存変更には触れていない。
- 数値や分類を新規に独立計数したとは報告しない。Phase 2b の cross-checked 入力と、新しい paper-only
  gluing 結論の格を混同していない。

## provenance

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_150_bside.txt` | `94881f9bb86bf1e4b9dfc590d842f9a9f7a71c9a66d109da392d1525ea3da11f` |
| `sol/sol_reply_148_dovetail.md` | `217132170d7330d208bff07dfde17ca680b57700699d7e814790ce4701089abc` |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` |
| `docs/notes/d972_phase2b_nonsplit_report_v1.md` | `56f2465ed73c6299026c129fc70fcbe9ebbab028342687d8a18d0e625e1e27e7` |
| `docs/notes/d972_phase2b_nonsplit_prereg_v1_1.md` | `7f7e5ff21b01ef326567f1f166a7d21deb14ff6d6bb70528a57832cb0fcf9d73` |
| `docs/notes/d972_phase2_cofinal_execution_v1.md` | `97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e` |
| `sol/sol_reply_140_finish.md` | `3463fe6ca0d876b2b512a270e907c32ea82afa6183848c92de63fee8a0ba0da2` |
| `sol/sol_reply_147_settle.md` | `66b14b6321dda92aeaafd79f575e9eccb8ab0e0f4f269bba7ea264458835b941` |

作業時 HEAD: `c46d1c73fa2fd6a648d7e86cf8d83b0ab30b49ee`。

FINAL: `H_r_W_STOP_CROSSED_PAPER_CANDIDATE; H_r_RESTRICTED_972_SURJECTIVE_THREAD; H_r_NOT_COFINAL; ROOF_A_B_UNKNOWN`
