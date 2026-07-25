# 影工房 第 8 便返信 — バッテリー検収・20 と 48 の構造・文献と道具

## 結論

### (a) 証明書の検収判定

**主数値は合格、証明書束全体としては条件付き合格**と裁定する。

- A1/A2 の
  \[
  240=176+44+0+20
  \]
  と、段 3 の
  \[
  1728=1440+240+0+48
  \]
  は排他的 staged count と候補別判定の双方で一致している。各 \(m\) に分けても A1/A2 は
  \[
  60=44+11+0+5,
  \]
  M\(_3\) は
  \[
  216=180+30+0+6
  \]
  で一様である。探索器と独立照合器の主列挙が一致しているので、**総数 20, 20, 48 と staged counts は cross-checked**として受領してよい。
- R\(_6\): A2 \(\to\) A1 は、20 元から 20 元への像が全 20 元を一度ずつ取る。独立照合器も source/target 20/20 と全射性を再構成しているので、**集合全単射は cross-checked**である。
- R\(_7\), R\(_8\) の**全射性と像サイズ 12/12, 8/8 は cross-checked**である。一方、照合器は繊維ヒストグラムを検査していない。証明書の raw map は一様 \(4,6\) を示し、紙上導出も同じ値を与えるが、現状の「繊維一様 4/6」を**二系統照合済みと呼ぶのは一段強すぎる**。
- 局所修正が必要である。特に `3.v2.json` の `isolated: UNKNOWN` は、K\({}^{(3)}\), N\(_3\) が isolated で Prop. 3.15 を適用できるという事前登録と矛盾する。数学上は `true`。また A1 の `layer_id: BLOCKED`、A2 \(\to N_5\) の reduction 欠落、R\(_7\)/R\(_8\) の `fibre`/`kernel_order` 空欄を補うべきである。

従って「全 7 段 all_pass」は、**主列挙・主 reduction の verdict が all_pass**という意味なら正しい。しかし certificate schema の全欄、全 fixture、全繊維構造まで照合済みという意味には読まない。

### (b) 「20」の説明骨子

A1 では
\[
q:=sf,\qquad r:=t^{-1}Y^m f,\qquad v_m:=t^{-1}Y^m s
\]
と置くと、二つの hexagon は
\[
q^2=1,\qquad r^3=1,\qquad rq=v_m
\]
になる。四つの charming \(m=0,1,3,4\) で \(v_m\) はすべて 5-cycle である。A\(_5\) の類積係数は、固定した 5-cycle \(v\) に対し
\[
\#\{(r,q)\in 3A\times2A:rq=v\}=5
\]
を与える。従って各 \(m\) に 5 解、合計
\[
\boxed{20=4\cdot5}.
\]

この 5 元集合には \(C_{A_5}(v_m)=\langle v_m\rangle\cong C_5\) が共役で自由推移的に作用する。したがって **5 の正体は中心 torsor でも円分 \(C_4\) でもなく、5-cycle の Sylow-\(5\) 中心化群による局所的な類分解 torsor**である。

さらに
\[
N_{\operatorname{Aut}(A_5)}(\langle X\rangle)
=N_{S_5}(\langle X\rangle)\cong C_5\rtimes C_4
\]
も位数 20 であり、商 \(C_4\cong\mathbf F_5^\times\) は四つの \(u=2m+1\) に一致する。これは強い構造候補である。ただし A1 の全 20 shadow が settled とはまだ証明されておらず、`isolated` も UNKNOWN なので、**GT(A1) をこの Frobenius 群 \(F_{20}\) と同一視するのは現時点では UNKNOWN**である。

---

## 検収の詳細

### F1【条件付き合格】独立照合が実際に覆う範囲

三 verdict の `ok: true` は空疎ではない。

- A1 は独立な置換実装で A\(_5\) marking、生成位数 60、derived 60、240 候補、全 candidate の h10/h11/generation stage を再構成している。
- A2 は独立な \(A_5\times C_5\) 構成と prepend 語評価で 240 候補を再列挙し、R\(_6\) の集合全単射を再構成している。
- M\(_3\) は独立な
  \[
  G_3\times_{C_2^2}P_3
  \]
  の構成から 1728 候補を再列挙し、K\({}^{(3)}\), N\(_3\) への像を再構成している。

一方、`check-v2.mjs` の最終 `ok` は次を検査していない、または値の型だけを確認している。

- R\(_7\)/R\(_8\) の繊維ヒストグラム、joint image、`kernel_order`。
- M\(_3\) の `isolated`、A1 の具体的 `layer_id`。
- `s3_marking`、`triangle_marking.exact_order_binv_a`、`derived_product_check`、`full_hexagon_double_check`。
- `max_rss_bytes`、`torsion_generation_agrees`、`frobenius_zero`、`m_missing`。
- A2 の `quotient_eval_diff_count=0`。

従って状態札は欄ごとに付ける必要がある。

### F2【合格】staged counts は排他的で、各 \(m\) に一様

| 対象 | 1 個の \(m\) 当たり候補 | h10 fail | h11 fail | generation fail | pass | 全 \(m\) の pass |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 60 | 44 | 11 | 0 | 5 | 20 |
| A2 | 60 | 44 | 11 | 0 | 5 | 20 |
| M\(_3\) | 216 | 180 | 30 | 0 | 6 | 48 |

A1/A2 の 20 は「一部の \(m\) に偏った 20」ではない。四つの charming class の各々に正確に 5 個ある。M\(_3\) も八つの charming class の各々に 6 個ある。`generation_fail=0` は、hexagon 通過後の候補が生成性で一つも落ちていないという意味であり、総数だけからの逆算ではない。

### F3【合格】R\(_6\) は集合全単射

A2 証明書の raw image は target index \(0,\dots,19\) を各一度取る。独立照合器も A2 の 20 shadow を prepend 規約で再構成し、A1 の 20 shadow への射影が全射、かつ source/target がともに 20 と確認している。従って集合としての単射性も従う。

ここから言えるのは
\[
\mathrm{GTSh}(M_{A,5},M_{A,5})
\;\xrightarrow[\text{set}]{\sim}\;
\mathrm{GTSh}(N_A,N_A)
\]
という集合全単射である。両側の isolated が UNKNOWN の間、`kernel_order=1` や「群同型」は使わない方がよい。現在の証明書が `kernel_order:null` としたこと自体は、この語彙規律に照らせば安全側である。

ただし canonical manifest が要求した A2 \(\to N_5\) の全射 reduction は証明書に無い。R\(_6\) の正しさには影響しないが、「manifest の reductions を完走した」という完全性は満たしていない。

### F4【要補強】M\(_3\) の raw map は一様だが verdict は一様性を検査していない

既存 JSON の像配列をそのまま集計すると、

- R\(_7\): target index 12 個が各 4 回。
- R\(_8\): target index 8 個が各 6 回。
- \((R_7,R_8)\) の 48 組はすべて相異なる。

従って GAP 証明書の raw observation は、一様繊維 \(4,6\) と joint injectivity を含んでいる。しかし独立照合器は各 reduction について `seen.size` しか判定せず、多重度も joint pair も verdict に出していない。一般に「48 元から 12 元へ全射」だけでは繊維一様 4 は従わない。

紙上では後述 F12 により一様性が導ける。状態は現在、

- 全射・像サイズ: **cross-checked**。
- 一様繊維 4/6: **GAP raw map + 紙上導出が一致**。
- 独立照合器による一様性: **未実装**。

と三分するのが正確である。

### F5【要修正】証明書束の局所欠損

1. **M\(_3\) の isolated**  
   `UNKNOWN` は誤り。K\({}^{(3)}\) は Thm. 4.3、N\(_3\) は verbal/補題 H2 で isolated、したがって Prop. 3.15 により M\(_3\) も isolated である。`true` に直し、checker もこの欄を検査すべきである。

2. **A1 の layer**  
   \(A=P=A_5\)、\(Q/A\cong S_3\) で
   \[
   \bar g=\bar\Delta=(12),\qquad
   \bar r=\bar\delta^{-1}=(132)
   \]
   が指定 layer である。\(Y^m\in A\) なので \(m\) に依らない。`BLOCKED` を pass 条件にするのでなく、この対を記録できる。

3. **M\(_3\) の reduction 欄**  
   raw map があるのに `fibre.note` のみ、`kernel_order:null` である。isolated を `true` に直した後は、R\(_7\) に `fibre=4, kernel_order=4`、R\(_8\) に `fibre=6, kernel_order=6` を記録できる。群構造だけを UNKNOWN に残す。

4. **A2 \(\to N_5\)**  
   manifest にある第二 reduction が欠落している。A2A1 の主検収とは独立だが、certificate completeness のため追加する。

5. **schema drift**  
   schema は `f_hash` を要求するが、三証明書は `f_word` を canonical とする司令塔注記で置換している。方針は合理的だが `gtsh-cert/v2` の文面と実物がずれている。v2.1 で `f_word` を正式に許すか、canonical word の hash を併記するべきである。

6. **cap 証拠**  
   wall time は十分小さいが `max_rss_bytes:null` であり、2GB cap の遵守を証明書自身は証明していない。数学結果は傷つかないが、P83 の四条件を「全て機械可読で完走」とは言えない。

7. **A2 の diff count**  
   `quotient_eval_diff_count=0` は興味深い観測だが checker 未照合である。また 0 は「c が生きても商内近道が安全」を意味しない。最終 240 候補上で今回一致した、までに留める。

---

## 「20」の独立攻撃

### F6【紙上導出】hexagon を A\(_5\) の \((2,3,5)\)-分解へ落とす

A1 では
\[
(sf)^2=1,\qquad (g_mf)^3=1,\qquad g_m=t^{-1}Y^m.
\]
そこで
\[
q:=sf,\qquad r:=g_mf,\qquad v_m:=g_ms=t^{-1}Y^ms
\]
と置く。\(f=sq\) なので
\[
r=v_mq,\qquad rq=v_m.
\]

paper の積規約で直接追うと
\[
\begin{array}{c|c}
m&v_m\\ \hline
0&(1\,4\,3\,5\,2)\\
1&(1\,5\,4\,2\,3)\\
3&(1\,3\,2\,4\,5)=X\\
4&(1\,2\,5\,3\,4)
\end{array}
\]
で、すべて 5-cycle である。従って hexagon 解は、固定 5-cycle \(v_m\) の
\[
v_m=rq,\qquad r\in3A,\quad q\in2A
\]
という分解と一対一に対応する。\(q=1\) や \(r=1\) は \(v_m\) の位数 5 と両立しないので退化項は無い。

### F7【紙上定理】A\(_5\) の類積係数が 5

A\(_5\) の共役類を \(2A,3A,5A,5B\) と書く。固定した \(v\in5A\cup5B\) に対する分解数は Frobenius の類積公式で
\[
\nu(v)=
\frac{|3A|\,|2A|}{|A_5|}
\sum_{\chi\in\operatorname{Irr}(A_5)}
\frac{\chi(3A)\chi(2A)\overline{\chi(v)}}{\chi(1)}.
\]
括弧の位置を明確に書けば
\[
\nu(v)=
\frac{20\cdot15}{60}
\left(
\sum_{\chi\in\operatorname{Irr}(A_5)}
\frac{\chi(3A)\chi(2A)\overline{\chi(v)}}{\chi(1)}
\right).
\]
この総和では自明指標の寄与が 1、他はすべて 0 である。二つの 3 次元指標は \(3A\) で 0、4 次元指標は \(2A\) で 0、5 次元指標は \(5A,5B\) で 0 だからである。従って、標準形で書けば
\[
\boxed{
\nu(v)=\frac{20\cdot15}{60}\cdot1=5
}.
\]

よって h10 は \(q^2=1\) の 16 元を残し、h10 fail は \(60-16=44\)。その 16 元のうち h11 まで通るものが 5 元なので h11 fail は \(16-5=11\)。これは証明書の各 \(m\) の staged count を紙上で説明する。

### F8【紙上定理】5 は Sylow-\(5\) 中心化群 torsor

\[
\mathcal D(v):=\{q\in2A:vq\in3A\}
\]
と置く。\(C_{A_5}(v)=\langle v\rangle\cong C_5\) は
\[
q\longmapsto v^j qv^{-j}
\]
で \(\mathcal D(v)\) に作用する。実際
\[
v(v^jqv^{-j})=v^j(vq)v^{-j}
\]
なので位数 3 条件を保つ。

非自明な \(v^j\) が \(q\in2A\) を固定すれば、位数 5 の元と位数 2 の元が可換することになるが、
\[
C_{A_5}(v)=C_5
\]
には involution が無い。従って作用は自由。F7 で \(|\mathcal D(v)|=5\) なので自由推移的である。

これは L の \(Z(P)\cong C_3\) torsor、M\(_5\) の円分 \(C_4\) torsor と異なる第三の型である。

- L: **中心の \(f\)-方向**。
- M\(_5\): **円分指標の \(m\)-方向**。
- A1: **torsion factorization の局所 Sylow-\(5\) 方向**。

A\(_5\) 自身の中心は自明なので、「中心 torsor」と呼んではならない。

### F9【紙上定理】五つの torsion 解はすべて生成性を通る

F7 の 5 分解について、\(q^2=1\), \(r^3=1\), \(rq=v_m\) とする。torsion 再定式化では transformed \(\delta^{-1},\Delta\) の A\(_5\) 成分がそれぞれ \(r,q\) なので、transformed \(\sigma_1=\delta^{-1}\Delta\), \(\sigma_2=\Delta\delta^{-1}\) の平方は
\[
(rq)^2=v_m^2=X^u,\qquad
(qr)^2=qv_m^2q=f^{-1}Y^uf.
\]

もし \(\langle v_m^2\rangle=\langle qv_m^2q\rangle\) なら、\(q\) は Sylow-\(5\) 群 \(H:=\langle v_m\rangle\) を正規化する。すると
\[
r=v_mq\in N_{A_5}(H)\cong D_{10},
\]
しかし \(D_{10}\) に位数 3 の元は無く、\(r^3=1\ne r\) に反する。従って二つの transformed 5-cycle は異なる Sylow-\(5\) 群に属する。A\(_5\) の 5-cycle を含む proper maximal subgroup は \(D_{10}\) であり、そこには Sylow-\(5\) 群が一つしかない。ゆえに二つは A\(_5\) 全体を生成する。

従って generation fail は紙上でも 0。F6–F9 により
\[
\boxed{|GTSh(N_A,N_A)|=4\cdot5=20}
\]
が、今回の探索値を使わず A\(_5\) の類積から再導出できた。

### F10【構造候補】\(20=|N_{S_5}(C_5)|\) だが、同型はまだ UNKNOWN

固定 Sylow-\(5\) 群 \(H=\langle X\rangle\) に対し
\[
N_{A_5}(H)\cong D_{10},\qquad
N_{S_5}(H)\cong C_5\rtimes\operatorname{Aut}(C_5)
\cong C_5\rtimes C_4
\]
である。後者の位数は 20。商 \(C_4=\mathbf F_5^\times\) は
\[
u=2m+1\bmod5\in\{1,3,2,4\}
\]
の四値と一致する。

さらに
\[
\operatorname{Out}(A_5)=S_5/A_5\cong C_2
\]
は \(C_4\) 全体ではなく、その平方剰余指標
\[
\mathbf F_5^\times\longrightarrow
\mathbf F_5^\times/(\mathbf F_5^\times)^2\cong C_2
\]
だけを見る。既知四 witness が \(u=1,4\) で inner、\(u=2,3\) で outer なのはこの像と一致する。

ただし現在の 20 shadow には automorphism witness が付いていない。全 20 が settled なら、各 \(u\) の 5 元と normalizer の各 \(u\)-coset を結ぶ見込みが高い。その確認前に
\[
GT(A1)\cong C_5\rtimes C_4
\]
と書くことはできない。そもそも isolated 未確定なので左辺を群として扱えない。

A2 は補題 A2A1 により candidate、hexagon、生成性が A1 と stage ごとに対応する。従って A2 の同じ \(44/11/0/5\) は偶然ではなく、A\(_5\) の上記構造が \(C_5\) 成分へ一意に持ち上がったものと説明できる。

---

## M\(_3=48\) の構造

### F11【紙上構造】非直交だが derived は直積

\[
P_M:=PB_3/M_3
\cong G_3\times_{C_2^2}P_3
\]
は共通商 \(C_2^2\) をもつので直交直積ではない。一方、
\[
[P_M,P_M]=[G_3,G_3]\times[P_3,P_3],
\qquad |[P_M,P_M]|=27\cdot8=216
\]
は紙上で閉じている。従って \(f=(f_G,f_P)\) の derived 座標は独立に動き、hexagon は両成分へ射影して判定できる。

charming parameter も
\[
\mathcal X_{12}
\xrightarrow{\sim}
\mathcal X_6\times_{\mathbf Z/2}\mathcal X_4,
\qquad
m\longmapsto(m\bmod6,m\bmod4)
\]
である。右辺の fiber 条件は二つの剰余が同じ parity をもつこと。CRT によりこれは全単射で、
\[
|\mathcal X_{12}|=8.
\]

K\({}^{(3)}\) 側は各 \(m\bmod6\) に 3 shadow、N\(_3\) 側は H9 により各 \(m\bmod4\) に 2 shadow。従って
\[
\boxed{|GT(M_3)|=8\cdot3\cdot2=48}.
\]

より精密には、まず集合として
\[
\boxed{
GT(M_3)\cong GT(K^{(3)})\times_{C_2}GT(N_3)
}
\]
である。二つの \(C_2\) への写像は \(m\bmod2\)。M\(_3\) の isolated を Prop. 3.15 で入れれば reduction は群準同型なので、この記述は群の fiber product に昇格する。ただしこれは紙上候補であり Lean verified ではない。

### F12【紙上説明】staged count と二つの繊維

各 \(m\) の 216 候補について、

- K\({}^{(3)}\) 側: H-a 通過 9、両 hexagon 通過 3。
- P\(_3\) 側: H9 により H-a 通過 4、両 hexagon 通過 2。

よって積側では
\[
216\longrightarrow 9\cdot4=36
\longrightarrow 3\cdot2=6.
\]
従って
\[
h10\_fail=216-36=180,\qquad
h11\_fail=36-6=30.
\]
八つの \(m\) で 1440, 240, 48 となり、証明書と一致する。

生成性についても、この対象専用の Goursat 論法が使える。transformed generators の生成群 \(S\) が G\(_3\), P\(_3\) の両方へ全射なら、その共通商 \(D'\) は G\(_3^{ab}=C_2^2\) の商なので \(|D'|\le4\)。一方 \(S\subseteq G_3\times_{C_2^2}P_3\) から \(|D'|\ge4\)。従って \(D'=C_2^2\) で \(S=P_M\)。ゆえに generation fail は 0。

R\(_7\) の一つの K\({}^{(3)}\)-shadowを固定すると、

- \(m\bmod12\) の lift が 2 個。
- 各 lift に P\(_3\) 解が 2 個。

ゆえに繊維は \(2\cdot2=4\)。

R\(_8\) の一つの N\(_3\)-shadowを固定すると、

- \(m\bmod12\) の compatible lift が 2 個。
- 各 lift に K\({}^{(3)}\) 解が 3 個。

ゆえに繊維は \(2\cdot3=6\)。これは
\[
48=12\cdot4=8\cdot6
\]
を同じ CRT/fiber-product 機構から同時に説明する。

### F13【atlas 登録案】最初の「非直交・derived-split・class-3」点

最低限、次を一組として記録すべきである。

| invariant | 値・状態 |
|---|---|
| 対象 | \(M_3=K^{(3)}\cap N_3\) |
| quotient | \(G_3\times_{C_2^2}P_3\), order 3456 |
| abelianization / derived | \(C_4^2\) / \(G_3'\times P_3'\), derived order 216 |
| non-orthogonality | 共通 marked 商 \(C_2^2\) |
| charming gluing | \(\mathcal X_{12}\cong\mathcal X_6\times_{C_2}\mathcal X_4\) |
| local solution | 各 \(m\) に \(3\times2=6\) |
| staged vector | \(1728\to288\to48\to48\), 排他的 fail \(1440,240,0\) |
| Prop. C defect | \(192/48=4=|P_3'|/2\) |
| reductions | K\({}^{(3)}\): 12/12, fibre 4; N\(_3\): 8/8, fibre 6 |
| joint map | 48 個の compatible pair へ全単射 |
| isolated | **true**（現 certificate は要訂正） |
| kernel structure | order 4 / 6、群型は UNKNOWN |
| fake | この二 reduction について欠落なし。全塔 genuine は未主張 |

fiber-product 記述からさらに
\[
\ker R_7\cong\ker(GT(N_3)\to C_2),\qquad
\ker R_8\cong\ker(GT(K^{(3)})\to C_2)
\]
まで絞れる。前者は位数 4、後者は位数 6。ただし前者が \(C_4\) か \(C_2^2\) か、後者が \(C_6\) か \(S_3\) かは、群 law を読まずに決めてはならない。

---

## 文献配達 03 の消化

### F14【修正付き採用】類和 scalar 化の第一段は「full Q-class union」のときだけ

F13 の
\[
n_m=\frac1{|Q|}
\sum_\chi S_3(\chi)
\operatorname{Tr}\!\left(
\rho_\chi(z_{2,C})\rho_\chi(v_m^{-1})
\right)
\]
で、\(C\cap T_2\) が **Q-共役類の和**なら、各類和は中心的になり character table だけへ落ちる。この第一段は正しい。

ただし任意の coset \(C=\bar\Delta A\) を「Q-共役類に分解」できるわけではない。一般には一つの Q-class と \(C\) の交わりが proper subset になり、full class sum は使えない。従って配達 03 §1-1 の式には

> \(C\cap T_2\) が Q-共役類の disjoint union である場合

という仮定を明記すべきである。

A1 はこの注意の最小 fixture である。
\[
Q=A_5\times S_3,\quad A=A_5,\quad
C=A_5\times\{(12)\}
\]
なので、\(C\) は Q-共役不変ではない。一方
\[
z_{2,C}=z_2(A_5)\otimes(12)
\]
と直積分解でき、A\(_5\) 類和と S\(_3\) の 2 次元行列を分ければ exact に処理できる。F7 の「5」は、この direct-product scalar 化の答えを先に与える良い unit test になる。

### F15【採用】第二段は centralizer algebra。ただし multiplicity-free の意味を固定する

\(z_{2,C}\) は A-共役で不変なので
\[
\rho_\chi(z_{2,C})\in
\operatorname{End}_A(\operatorname{Res}^Q_A\rho_\chi)
\]
である。Curtis–Fossum / CST の centralizer・Hecke 路線は正しい次の一手である。

ただし「multiplicity-free なら scalar」と一語で済ませない方がよい。

- \(\operatorname{Res}^Q_A\rho_\chi\) が multiplicity-free なら commutant は可換になる。
- それでも \(\rho_\chi(z_{2,C})\) は \(\rho_\chi\) 全体で一つの scalar とは限らず、A-type ごとの scalar block になる。
- multiplicity があれば、その multiplicity space 上の小行列が残る。
- `Ind_A^Q(λ)` の Gelfand 性と、今回必要な各 `Res_A ρ_χ` の multiplicity-free 性が同じ仮定かは、引用する定理の形を原文で固定する必要がある。

従って go/no-go は単なる yes/no ではなく、各寄与 \(\chi\) について restriction multiplicity と block size を出すのが正確である。

### F16【採用】Kawanaka–Matsuyama は一方の marginal、coset 正値性の本丸ではない

K–M の twisted Frobenius–Schur 型公式は
\[
\#\{g:\sigma(g)=g^{-1}\}
\]
すなわち \(\bar\Delta f\) が involution になる側、今回の H-a / \(z_{2,C}\) の総量を scalar に数える道具として位置づけるのが正しい。

しかし欲しいのはさらに
\[
(v_mg)^3=1
\]
を同時に課した coefficient である。K–M 単独から \(n_m>0\) は出ない。これは「marginal が正」から「結合分布の指定セルが正」を結論できないのと同じである。

配達の「指定 coset 正値性の一般理論は見つからない」は重要な hunt 結果だが、未保有原文が多い現段階では

> 今回の探索範囲では該当一般定理を確認できず、UNKNOWN

と記帳する。文献全体に存在しないという非存在定理にはしない。

E2 前線の次の一手は次の順がよい。

1. A1 \(=A_5\times S_3\) で F13 行列式から各 \(m\) の 5 を再現する。
2. 各対象で \(\operatorname{Res}_A^Q\rho_\chi\) の multiplicity と commutant block size を出す。
3. multiplicity-free 対象だけ球関数へ scalar 化する。
4. 非 multiplicity-free 対象は小行列のまま exact trace を計算する。
5. K–M の値を H-a marginal の独立 fixture として突き合わせる。

---

## 道具の聴取

現時点で最も欲しいのは、新しい巨大探索器ではなく次の四点である。

1. **既存 GAP package の目的別使用**  
   `repsn`/`wedderga` は F13 の exact matrix と Wedderburn block、`twistedconjugacy` は H-a の twisted orbit/coboundary パラメータ、`lins` は exact-order 条件付き三角群商の事前登録掃引に使いたい。順序は小さい A1 \(\to\) restriction multiplicity \(\to\) 大対象とする。
2. **独立な exact representation 系**  
   GAP と helper を共有しない SageMath を希望する。利用可能なら Magma を第三系統にし、character table の同じキャッシュを読むだけの擬似独立を避けたい。
3. **計算資源**  
   order 20736 級の matrix block と triangle quotient 掃引用に、4 core・16GB 以上の Actions runner と中間 artifact の保存が欲しい。A1 order 360 の既知値 5 を再現するまでは大型段へ進まない。
4. **一次文献**  
   Curtis–Fossum、CST/LNM 2267、Kawanaka–Matsuyama、Dokchitser–Dokchitser の PDF が必要である。とくに multiplicity-free の対象が `Res` か `Ind` かを翻訳メモだけで決めたくない。

これらは P103–P107 に実行可能な形で再掲する。

---

## ★ 教材

1. **発見数の素因子は、群の中心とは限らない。** A1 の 5 は \(Z(A_5)\) でなく、固定 5-cycle の中心化群 \(C_5\) が類分解集合に作用することから出る。
2. **同じ 20 でも「集合の 4 本の \(C_5\)-torsor」と「群 \(C_5\rtimes C_4\)」は別主張。** settled/isolated を埋めるまでは後者へ飛ばない。
3. **surjective 48 \(\to\) 12 は fibre 4 を意味しない。** 一様性にはヒストグラム、群準同型+kernel、または紙上 fiber-product のいずれかが必要。
4. **非直交でも derived が split することはある。** M\(_3\) の本質は「商は \(C_2^2\) で糊付け、commutator 座標は独立」という二層構造にある。
5. **all_pass は checker の量化範囲内の語。** checker が読まない `isolated` や `fibre` まで自動的に pass したことにはならない。
6. **marginal の正値性は指定 coset convolution の正値性ではない。** K–M が H-a を数えても、H-b′ との同時解は F13 の coefficient に残る。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。既存 JSON の欄と像配列を読み、PowerShell では既存 index の度数を表示しただけで、群の再列挙はしていない。
- `check-v2.mjs` は実行せず、R\(_6\)/R\(_7\)/R\(_8\) が何を再計算し、何を判定していないかをコードから監査した。
- A\(_5\) の 5 は標準 character table と subgroup structure を用いて紙上導出した。これは Lean verified ではない。
- M\(_3\) の fiber-product 説明は Thm. 4.3、H9、Prop. 3.15、既監査の reduction/groupoid functoriality を前提とする紙上導出である。
- 外部検索は行っていない。文献配達 03 と開示済み scout note を読んだ。`papers/delivered/` の Goursat/Guillot 3 PDF は今回の scalar 化三文献そのものではないため、再度のページ画像照合は行っていない。
- Curtis–Fossum、CST/LNM 2267、Kawanaka–Matsuyama、Dokchitser–Dokchitser の原文は未供与なので、配達メモを超える定理の量化子・仮定は未監査である。
- 今便に Lean verified の新主張はない。

---

## 考察と提案

P89【検収台帳】A1/A2/M\(_3\) の主総数と staged counts、R\(_6\) 全単射、R\(_7\)/R\(_8\) 全射を受領し、欄ごとの照合範囲を併記する。

W61【all_pass】`verdict.ok=true` を certificate schema の全欄合格と読まない。checker が実際に量化した claim のみ cross-checked とする。

P90【A5 類積命題】「固定 5-cycle の \(3A\cdot2A\) 分解は 5 通り」を A1 の紙上命題として起票し、\(20=4\cdot5\) の説明を CLAIMS に添える。

P91【staged 導出】A1 の \(60\to16\to5\to5\) と、A2 への stagewise 持ち上げを【GAP-M1】の A1/A2 閉鎖として本文に入れる。

W62【torsor 語彙】A1 の \(C_5\)-torsor は \(Z(A_5)\)、reduction kernel、GT 群の部分群のいずれともまだ同一視しない。

P92【settled 20】A1 の全 20 exact \((m,f)\) について automorphism witness \(h\in S_5\) の有無を出す小仕事を最優先にする。全通過なら A1 isolated を閉じる。

W63【群語彙】P92 完了前は GT(A1), GT(A2) を群と呼ばず、20 元の shadow 集合と呼ぶ。

P93【F20 仮説】P92 が全通過した場合だけ、\((m,f)\mapsto h\) が \(N_{S_5}(\langle X\rangle)\cong C_5\rtimes C_4\) への全単射または群同型を与えるか検査する。

W64【cardinality trap】\(|N_{S_5}(C_5)|=20\) と shadow 数 20 の一致だけで F\(_{20}\) 同定を宣言しない。

P94【Out の記録】settled witness の outer class は \(u\bmod5\) の平方剰余指標で層別できるか、各 \(m\) の 5 元すべてで確認する。

W65【Out の射程】Out\((A_5)=C_2\) は四つの \(m\) を二層に潰すだけで、5 元繊維そのものを説明しない。

P95【M3 fiber product】  
\[
GT(M_3)\cong GT(K^{(3)})\times_{C_2}GT(N_3)
\]
を「非直交・derived-split」atlas 命題として起票し、集合版と群版の仮定を分ける。

P96【reduction checker】R\(_7\)/R\(_8\) で独立に全 image index の histogram、joint pair 48 個、各 source の \(m\bmod6/4\) を再計算し verdict に出す。

W66【一様性の状態】P96 前は一様 fibre 4/6 を「raw map + 紙上一致」と書き、二系統数値照合済みとは書かない。

P97【certificate 修正】`3.v2.json` の `isolated=true`、R\(_7\)/R\(_8\) の `fibre=4/6`, `kernel_order=4/6`、A1 の layer \((\bar g,\bar r)=((12),(132))\) を次版で正式欄にする。

W67【kernel 型】order 4 を直ちに \(C_2^2\)、order 6 を直ちに \(C_6\) または \(S_3\) と決めない。

P98【M3 群型】GT(N\(_3\)) の composition table と parity character を出し、\(\ker R_7\) が \(C_4/C_2^2\) のどちらか、\(\ker R_8\) が \(C_6/S_3\) のどちらかを決着する。

P99【A2 完全性】A2 \(\to N_5\) の reduction を追加し、A2A1 の全単射と N\(_5\) m-full の二方向を同じ証明書に収める。

P100【F13 最小 fixture】`repsn`/`wedderga` で A1 の \(Q=A_5\times S_3\) を exact matrix 表現に落とし、F13 から各 \(m\) の 5 を再現する。

W68【第一 scalar 化】\(C\cap T_2\) が full Q-class union でない対象へ、類和 scalar 式をそのまま適用しない。

P101【multiplicity scan】各対象・各寄与 \(\chi\) について \(\operatorname{Res}_A^Q\rho_\chi\) の multiplicity と最大 block size を表にし、scalar / small-matrix / infeasible の三分類を作る。

W69【可換≠一 scalar】commutant が可換でも、\(\rho_\chi(z_{2,C})\) が \(\rho_\chi\) 全体で単一 scalar とは限らない。A-isotypic block を残す。

P102【K–M の使い所】Kawanaka–Matsuyama の値を \(|T_2\cap C|\) または H-a candidate count の独立 fixture として使い、F13 の同時係数とは別欄にする。

W70【marginal】H-a の解が多いことから H-a∧H-b′ の解の存在を推論しない。

P103【GAP 棚の使用順】第一に `repsn`/`wedderga` で F13、第二に `twistedconjugacy` で \(\mathcal B_\theta\) の orbit/coboundary パラメータ、第三に `lins` で exact-order 付き \(\Delta(2,3,2k)\) 掃引を使う。

P104【独立系の希望】GAP と helper 非共有の exact representation cross-check 用に SageMath を希望する。利用可能なら Magma を第三者系にし、同じ character table データの単なる再包装にならないよう構成法を分ける。

P105【計算資源】F13 の order 20736 級と triangle quotient 掃引には、4 core・16GB 以上の Actions runner と成果物 retention を希望する。A1 order 360 を通すまでは大規模段へ進まない。

P106【文献要請】Curtis–Fossum (1968)、CST/LNM 2267（arXiv:1811.09526）、Kawanaka–Matsuyama (1990)、Dokchitser–Dokchitser (arXiv:2105.07247) の原文 PDF を次便までに `papers/delivered/` へ供与してほしい。

W71【文献非存在】hunt で見つからないことを「一般理論は存在しない」と断定せず、「探索範囲で未確認」と記帳する。

P107【原文照合順】P106 受領後は、(i) centralizer ring の正確な対象、(ii) 非自明線形指標の induction、(iii) multiplicity-free の必要十分条件、(iv) K–M の量化子、の順にページ画像で照合する。

W72【diff count 0】A2 の `quotient_eval_diff_count=0` を語レベル評価不要の証拠にしない。規約トリップワイヤーは恒久的に残す。

P108【schema coverage】各 certificate field に `checked_by_gap / checked_by_independent / paper_only / blocked` の provenance bitmap を付け、`ok` の量化範囲を機械可読にする。

W73【cap】`max_rss_bytes=null` のまま 2GB memory cap を「計測 PASS」と記帳しない。wall time PASS と memory UNKNOWN を分ける。

P109【Lean 初弾追加】既存 T2(iii)/E1/A5-Q に加え、A\(_5\) の類積係数 5 と \(\mathcal X_{12}\) の CRT fiber-product を有限和・有限集合の Lean 初弾候補にする。

W74【状態】今便の新規構造説明は紙上導出であり、数値の cross-check と Lean verified を混同しない。
