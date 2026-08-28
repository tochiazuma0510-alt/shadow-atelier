# R07 explicit-lift 全証明再監査と前進路線 v220

Author: Sol / 2026-08-28

Status: 紙上再監査・路線固定稿。`sol/` にある `proof_r07_*` / `audit_r07_*`
194 本の題名・status・依存関係を機械的に棚卸しし、そのうち現在の明示リフトに
荷重を持つ証明鎖を本文まで再読した。以下で「定理」と呼ぶものは紙上定理であり、
Lean による verified を意味しない。新しい有限群計算結果、compatible R07 lift、
fake 証明書、Ihara 反例は本稿では宣言しない。

## 0. 結論

現在いちばん有望なのは、**各段を別々に探索する路線ではない**。最初の pointed
解から一つの有限 word-pair

\[
 M=\sum_i a_i(U_i-V_i),\qquad \pi(U_i)=\pi(V_i),
\tag{0.1}
\]

を作り、それについて H1, H2, P の三つの exact PB endpoint を一度だけ消す路線で
ある。

この路線が有望な理由は次の三点である。

1. v191 により、(0.1) の一つの universal boundary identity は同じ相対 pro-3
   Frattini 塔の全段へ同時に降りる。
2. v194 と v198 により、その identity の存在判定は巨大な全 \(D_2\) 行列探索では
   なく、H1, H2, P の三つの exact endpoint の消滅に等価である。
3. endpoint が零なら、v197 により境界係数 \(q\) は有限 van Kampen コンパイラで
   必ず抽出できる。ここに新しい存在予想は要らない。

したがって主障害は、もはや「無限個の \(c_n\) をどう整合的に選ぶか」ではない。
主障害は、**正しく型付けされた最初の actual word と actual first kernel から
\(M\) を作り、その三 endpoint が零になることを示すこと**である。

v216--v217 の single/three-seed 定理はこの主線を置き換えない。これは endpoint
像を一個または高々三個の orbit seed に圧縮する安価な前処理であり、非零なら早く
落とし、零なら exact PB endpoint 計算へ送るための gate である。

## 1. 目標と既知の有限屋根を固定する

### 1.1 証人側の目標

目標は、有限屋根 R07 の非算術点を起点として、全ての有限 GT-shadow へ整合的に
降りる一つの profinite GT element を構成することである。これが成立して初めて
Ihara の反例候補になる。B3 のみ、あるいは選んだ有限個の B4 窓のみを満たす語は
まだ証人ではない。

### 1.2 算術 324 と非算術点

現行の有限屋根の算術像 \(A\) は位数 324 で、二つの候補 \(A_9,A_{12}\) の
unordered pair に入る。両者の位数は 324、交わりは 108、共通の外側は 432 点で
ある。row 36 はその共通外側にあるので、orientation を決めなくても有限屋根で
非算術である。この有限主張の証拠階級は v76 の accepted arithmetic package と
cross-check であり、Lean verified ではない。

「648 が非算術」という表現には orientation が混ざる。証人側に必要なのは 648
全点の名指しではなく、固定した非算術起点が一つあればよい。現在は row 36 がその
役を果たす。

### 1.3 現在の actual word

現在の exact-word 計算の基準語は

\[
 g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108},
\tag{1.1}
\]

であり、長さ 760、指数和 \((0,0)\) を持つ。task192 が成功したとき次へ渡す語は
\(g_{760}c_{\mathrm{exact}}\) である。

一方

\[
 \chi_{07}=[x,y][y,z]^{-1}
\tag{1.2}
\]

は初期 nilpotent/normalizer 構成の核である。(1.2) が何度現れても、それだけでは
task192 の actual word を置き換えず、現在の first-edge solution を与えない。

## 2. 「一様」の三つの意味を分離する

これまでの後戻りの最大原因は、次の三命題を同じ「一様リフト」と呼んだことにある。

### U1: 各段で同じ有限アルゴリズムを使える

v217 は各相対 pro-3 rung の projected endpoint image を高々三個の invariant-orbit
seed から生成する。これは uniform finite compiler である。

### U2: 一つの有限恒等式を全段へ同時に降ろせる

v191 と v194 は、一つの word-pair \(M\) が universal boundary identity を満たせば、
その同じ有限データが全 matched pro-3 rung に作用することを示す。v169 と v98 は、
有限段で actual corrections が存在した後の compatibility/word materialization を
処理する。

### U3: その有限恒等式を満たす actual word-pair が存在する

これはまだ証明されていない。現在の中心課題は U3 である。U1 または U2 を引用して
「一様な明示リフトが完成した」と言ってはならない。

## 3. 初期 explicit/nilpotent 鎖の再監査

v7--v11 は \(\chi_{07}\) を核にした marked R07 代表を明示し、filtered/class-4 の
整合を与える。v12 は ordered pentagon を degree 4 まで閉じ、degree 5 を有限方程式へ
還元する。v13--v16 は scalar family の class-five lift を閉じ、v16 で 3-adic unit を
得る。

これらは genuine な低次数の土台である。しかし結論は次に限定される。

- B3/B4 の全有限 refinement を同時に満たす theorem ではない。
- actual 11-occurrence PB endpoint を計算していない。
- perfect relative kernel と mixed-prime actual membership を処理していない。
- \(g_{760}c_{\mathrm{exact}}\) の代わりに \(\chi_{07}\) を採用する根拠にならない。

v17, v20, v41, v45, v46 の「all degree」「all prime」型の記述は、各稿に明記された
core-matched/pronilpotent/conditional scope では有効であるが、original B4 R07 の
unrestricted compatible lift と読んではならない。

## 4. 相対 dihedral Hensel 鎖

### 4.1 立っている部分

v71 は diagram-chief typing と exact abelian Fox linearization を与える。unit-forest
block はここで解ける。v82 は HT1--HT5 を仮定した逆極限 Hensel theorem である。

その後 v98 は、各 edge で actual correction value が存在すれば、短い ordinary
commutator representative を選んで compatible infinite product にできることを示す。
従って自然な word section の不存在は障害ではない。

v99 は nested matched diagram-chief ladder に対して structural HT1, structural HT2,
および HT5 の residual/Jacobian 部分を閉じる。したがって「HT1--HT5 が全部未証明」
という古い要約も誤りである。

### 4.2 残る障害

残る abelian obstruction は actual-image contraction/target membership と side-gate
admissibility である。v71 の全 block が forest なのではない。純 dihedral
antisymmetrizer \(1-\theta\) は return-odd 部分しか自動的に殺さず、actual
field-outer/full-pair の return-even survivor が残る。

従って正しい一般化は

\[
 \text{dihedral antisymmetrizer}
 +\text{actual-class-specific relative homotopy}
\tag{4.1}
\]

である。v174 と v191 は (4.1) の第二項を pointed actual class に対して作る候補で
ある。

### 4.3 BRUN-DEF の正確な位置

`proof_relative_dihedral_b3_and_b4_small_window_v3.md` の BRUN-DEF は pentagon residual
を Brunnian image に局在させる。これは重要だが、joint hexagon/pentagon equation と
side gates を解く theorem ではない。従って「B3 の明示 lift があれば B4 は小窓で
自動補正できる」という推論には、なお actual correction-image membership が要る。

## 5. Recursive relative Frattini 鎖

v145 の塔は

\[
 \Phi_p(K)=K^p[K,K]
\tag{5.1}
\]

による relative Frattini tower である。Jennings depth と混同しない。

v168 の relative Magnus/Fox compiler で得る \(P/\Phi_p(K)\) は、affine ambient
\(M\rtimes E\) 全体ではなく、marked generators が生成する subgroup である。完全な
translated boundary orbit を省いてはならない。

v169 は、全ての finite actual membership が成立すれば completed coefficient を一つ
選べる compactness theorem である。非線形 side gates には finite accepted-set tree と
König を使う。これは choices の compatibility を解くが、各 level の nonemptiness を
作らない。

従ってこの鎖は健全であるが、これを再証明しても証人には近づかない。必要なのは
input である finite actual membership の確立である。

## 6. Pointed Neumann と universal word-pair

### 6.1 条件付き section から actual vector へ

v171 の section \(s\) は条件付きであり、構成されていない。v173 の cyclic diagonal
contraction には annihilator、deeper error、side gates の条件が残る。

v174 は一つの actual vector \(\beta\) について、

\[
 \beta-Ba=\mu\beta,\qquad \mu\in\mathfrak j
\tag{6.1}
\]

なら nilpotent Neumann sum により pointed correction を作る。これは abstract module
全体の splitting を要求しない。v184 は first pointed equation

\[
 e_1=\alpha d_1+\beta e_1,
 \qquad \mu_1=(1-\beta)^{-1}\alpha
\tag{6.2}
\]

を有限 nilpotence から解く。ここまでの algebra は sound である。

ただし finite \(\mu_1\) だけでは completed word identity でも B4 side gates でもない。

### 6.2 v191 が与える本当の飛躍

pointed ancestry を fibre differences に展開すると

\[
 M=\sum_i a_i(U_i-V_i),\qquad \pi(U_i)=\pi(V_i)
\tag{6.3}
\]

を得る。この \(M\) について

\[
 \widetilde e-M\widetilde d=\widetilde D_2q
\tag{6.4}
\]

が common source で成立すれば、同じ \(M\) は全 matched pro-3 rung へ降りる。
これが「一成功段から全段へ飛ばす」の正確な theorem である。

v191 は (6.4) を自動では証明しない。しかし (6.4) が未証明であることと、全段ごとに
再探索が必要であることは同じではない。一つの \(M\) の三 endpoint だけを判定すれば
よい。

## 7. Endpoint 鎖

v193 は七 block を別々に cycle と要求したため強すぎ、v194 に全面的に supersede
された。正しい判定は、11 occurrences を printed order と fixed prefixes/signs で
H1, H2, P の三 relation block に合成した後の endpoint

\[
 E_{H1}(M),\quad E_{H2}(M),\quad E_P(M)
\tag{7.1}
\]

が全て零であることだけである。

完全 presentation 2-complex の universal cover は simply connected なので

\[
 \ker D_1=\operatorname{im}D_2.
\tag{7.2}
\]

ここで asphericity は不要である。従って (7.1) が零なら (6.4) の \(q\) は存在する。
v197 は graph fundamental cycles と relator van Kampen trace から \(q\) を有限に抽出
する total algorithm を与える。v198 は (7.1) を PB group-word values だけから直接
集計し、最初の判定に巨大な translated \(D_2\) column generation を不要にする。

同じ successor を保ったまま endpoint を直す必要がある場合、v195--v196 は
\(M_0+J_1\) の exact repair torsor と one-sided Schreier orbit dovetail を与える。
positive search は完全、有限 cutoff の negative は UNKNOWN である。また v212 により
同じ \(\mu_1\) fibre 上では exponent-nine projection は一定なので、その projection で
落ちたものは exact repair では救えない。

## 8. First successor の圧縮

v188 は complete roof presentation の relator defects の roof-action closure が exact
successor kernel \(K\) を与えることを示す。v189 は 10 typed coordinates、11 literal
occurrences、7 old blocks の型対応を固定する。E3 の重複 occurrence と、同じ registry
label `C21` を持つ E3/E4 を同一視してはならない。

v190 の complete presentation は 6,441 relators、内訳は 6,318 \(\Gamma\)-edge loops、
104 action loops、19 \(Q_0\) relatorsである。入力の完全性と型が認証されれば finite
extension presentation lemma は sound である。

v208/v211 は exponent-nine quotient を

\[
 D_1\cong H_2(9),\qquad |D_1|=729,
\tag{8.1}
\]

と同定し、中心 \([x,y]^3\) による quotient の位数は 243 である。v213 は全 rung で
\(H_2(3^{n+1})\) への canonical quotient と pro-Heisenberg quotient を与え、
one-power-ahead image rank を高々 3 に抑える。

最初の edge では v216 により

\[
 I(R_0)=k[D_1](z-1),\qquad \dim_k I(R_0)=486,
\tag{8.2}
\]

で、endpoint image は一つの seed

\[
 u_0=(z-1)\odot w
\tag{8.3}
\]

の invariant closure である。v217 は全 rung で高々三 seed に一般化する。

これは大幅な高速化であるが、(8.3) の actual \(w\) と corrected residual を作り、
target が orbit span に入るかを判定する必要は残る。positive でも projected seed を
得るだけで、exact PB endpoint は v198 で再確認する。

## 9. Formation と mixed-prime 鎖

v147 は formation kernel の finite formation residual への像と purification criterion
を与える。v148 は extension descent、v149 は coarse residual
\(R_S(G)\cong PSL(2,8)\) と complement を扱う。v151 は superperfect residual に対し

\[
 V\cap R_S(H)=[R,V]
\tag{9.1}
\]

を与える。

v153 の all-rung formula は

\[
 R_S(F/\Omega_n)=P_n/\Omega_n,
 \qquad V_n/V_{S,n}\cong P_n/P_{n+1},
 \qquad \rho_n([w])=[w]\bmod P_{n+1}
\tag{9.2}
\]

である。鍵となる residual-perfectness argument も再点検し、formation residual の
最小性から成立する。

v155 は全 prime が無限回現れる mixed-prime Frattini schedule が、solvable relative
kernels を持つ全有限 refinement に cofinal であることを示す。v156--v158 は exponent
lattice と charming selector が formation selector を通ることを示す。

この theory は構造的には十分進んでいる。未解決なのは actual joint
\((B_n,\rho_n)\)-membership である。さらに formation residual に残る nontrivial
perfect relative kernel は mixed-prime abelian tower だけでは消えない。

従って次に abstract formation theorem を増やす優先度は低い。まず pro-3 actual
word-pair と endpoint を確定し、その後に同じ finite word の mixed-prime image を
判定する。

## 10. Perfect-core / nonabelian 鎖

v21--v23 の perfect-factor、three-kernel、Goursat--Schur decoupling は、four-forget
または single-factor lane の仮定下で sound である。genuinely coupled PB4 refinement
全体を自動で解くものではない。

v35 により small active nonabelian factor では \(t\le 6\) なら
\(PSL(2,8)\) だけが残り、別型には少なくとも \(t\ge 7\) が要る。v36 は pure PSL core
上の central abelian layer を処理する。v48 の factor graph、v52 の leaf peeling、v79
の characteristic-3 diagonal elimination は広い範囲を閉じる。

しかし v81 の mixed field-outer/full-pair return-even lane は残る。abstract module の
countermodel は actual occurrence を証明しない一方、pure dihedral theorem だけで
全て消えるという主張も許さない。ここは pro-3 endpoint が閉じた後の独立 gate として
残す。

## 11. fake / 小窓路線

既存の 972 棚では C11--C14 型の局所有限 NO/settled 結果はそれぞれの scope 内で
成立する。しかし condition (iv)、すなわち全 coupled chief 段で correction を返す
閉形式 selector は未証明である。

これが閉じれば index-3 collapse により、算術外 648 を fake/\(\neg B4\)-witness と
する路線が強くなる。しかしそれは Ihara witness ではなく、明示 lift が存在しない側の
結論である。

古い \(m_1=6,j=7\) sweep は正しい TYPE-M / KEY-BIJ / complete fibre coverage / side
gates を測っていない。BRUN-DEF も局在化までである。従って fake 路線は並列 fallback
として保持するが、現在の主線にはしない。

## 12. 撤回・supersede・隔離台帳

今後、次を現行根拠として再利用しない。

- v54 は v55 に supersede。
- 648 typing は v67 を経て v76 を現行とする。
- v74 は v95 に supersede。その後の checkpoint 文書は theorem 自体でなく routing。
- v97 は contaminated lane として隔離。
- v101 の actual A3 binding は未形式化。v102 の型分離を優先。
- v111 の natural transfer は強すぎ、v114 が遮断。
- v136 の resource claim は v138 で修正。
- task186 の exponent mismatch は v162 で修正。
- v193 は v194 に全面撤回。
- v204--v206 の roof-abelian screen は v207 の canary に限る。
- 古い \(j=9,\ldots,12\) Jennings/\(g_{760}\) 計算は fixed-prefix over-approximation lane
  で、resource stop のため答えを持たず、現在の主線ではない。

## 13. task219 実装の静的拒否

v216 の紙上定理は維持する。しかし現在の
`luna_reply_219_r07_first_edge_single_seed_endpoint_pregate_v1.md` に対応する実装は、
単に入力待ちなのではなく ABI と数学の両方で不適格である。production に投入しない。

静的に確認した欠陥は次の通りである。

1. word-independent な task198 receipt に `occurrence_values`, `fixed_residual`, word
   ancestry を要求している。actual word-specific data は task192 側から来るべきである。
2. task198 の ten typed hex blobs を \(H_2(9)\) Malcev triples `[a,b,r]` と誤読する。
3. task198 evaluator の `entry_points` / `section_cocycle` ABI を、存在しない
   `bindings` / `cocycle` として読む。
4. production prefix を全て identity にし、load-bearing `fox_prefix_occurrences` を
   捨てる。
5. 必要な \(w_o=\sigma_op_o\bar\xi_o\) を作らず、各 occurrence を一個の signed
   group-basis point に置き換える。
6. modulus 9 で `x_inv=(2,0,0)`, `y_inv=(0,2,0)` と hard-code する。正しい逆元座標は
   8 である。
7. transversal sanity で \(c=h^3\) の冪でなく `(0,0,j)`, \(j=0,1,2\) を掛け、
   \(D_1/\langle c\rangle\) cosets を検査していない。
8. reduction の初期 ancestry を消費せず、literal coefficient recovery を保証しない。

正しい後継は二入力 specializer でなければならない。

\[
 \boxed{
 \text{task192 actual word}
 +\text{task198 word-independent occurrence/evaluator ABI}
 +\text{v213 static }H_2(9)\text{ maps}
 \longrightarrow (w,\bar\epsilon_1,\text{ancestry})}
\tag{13.1}
\]

word-specific fields を task198 に逆流させない。

## 14. 正しい依存鎖

今後の証明と計算の依存関係を次に固定する。

```text
row 36 / g760
      |
      v
task192: exact first-edge common word
      |                         task198: complete roof presentation/evaluator
      +-----------------------------+
                                    v
                 two-input actual specializer
                 (11 prefixes, values, w, residual, ancestry)
                                    |
                     +--------------+--------------+
                     |                             |
                     v                             v
              v216 one-seed pre-gate        v188 actual K
                     |                             |
                     +--------------+--------------+
                                    v
                         v214 pointed joint gate
                                    |
                                    v
                           v191 compile mu1 -> M
                                    |
                                    v
                         v198 three exact endpoints
                            /               \
                         zero              nonzero
                          |                   |
                          v                   v
                 v197 extract q       v195/v196 same-mu repair
                          |
                          v
                 v174 relative pro-3 lift
                          |
                          v
             mixed-prime actual (B_n,rho_n) gates
                          |
                          v
                 perfect-core actual gates
                          |
                          v
                  compatible R07 witness
```

注意すべき論理は次の通りである。

- v191 は sufficient theorem であり、必要条件とは証明していない。
- compiled \(M\) の endpoint 非零はその \(M\) を落とすが、v195--v196 repair の余地を
  残す。
- v216 の projected negative は固定した first correction の全 first multipliers を
  落とすが、task192 の別 lower correction まで落とすには fibre coverage が要る。
- 一個の task192 candidate の失敗を branch 全体または fake の証明に昇格しない。

## 15. 優先順位

### Priority A: actual universal word-pair route

task192 と task198 の正しい出力から (13.1) を作り、v214 で actual pointed solution を
得て v191 の \(M\) にする。その三 exact endpoint を v198 で判定する。これが最短で
「一有限成功から全 pro-3 段」へ到達する路線である。

### Priority B: single-seed pre-gate

同じ actual data に v216 を先に適用する。486 directions を一 seed の orbit closure
に圧縮できるため、exact PB work の前に安く reject できる。ただしこれを主定理と
呼ばない。

### Priority C: mixed-prime actual membership

pro-3 universal word が得られた後、v153--v158 の既成 selector 上で同じ word の
actual \((B_n,\rho_n)\) membership を調べる。新しい formation theory の分類から
始めない。

### Priority D: perfect-core gate

最後に v21--v23, v35--v36, v48, v52, v79--v81 の範囲を使い、残る actual
field-outer/full-pair class を判定する。抽象 module 全分類を先に完成させるより、
actual class に限定する。

### Parallel fallback: fake condition (iv)

TYPE-M と complete fibre coverage を明示した accepted-set tree としてのみ進める。
小窓 canary の成功・失敗を condition (iv) と同一視しない。

## 16. 後戻り禁止規則

1. \(\chi_{07}\) の再発見を actual first-edge word の進捗として数えない。
2. U1/U2 を U3 と呼ばない。
3. compactness を nonemptiness の証明に使わない。
4. BRUN-DEF を correction-image surjectivity と呼ばない。
5. projected exponent-nine pass を exact PB endpoint pass と呼ばない。
6. roof presentation data と actual word data を同じ artifact に混ぜない。
7. finite cutoff の空集合を nonexistence と呼ばない。
8. pro-3 lift を all-prime/perfect-core lift と呼ばない。
9. fake/\(\neg B4\) witness と Ihara witness を混同しない。
10. endpoint zero の後に巨大な \(D_2\) 探索へ戻らず、v197 を使う。

## 17. 2026-08-28 現在の計算状態

- task192 production: GHA run `33129456772`, commit
  `08d23f0e19b2c8692ba320cac75f419dac4c8dcc`。10:48 JST 時点で GAP 本計算が
  `in_progress`。positive/negative/UNKNOWN のいずれもまだ宣言しない。
- task198 SELFTEST: GHA run `33133058026`, commit
  `a491bd3aad45c2bba8428e17edbbc8b5788e73a8`。`CreateDirectory` が GAP 4.16.0
  環境で未定義のため producer 前に停止。数学・producer・checker は未実行で、
  negative evidence ではない。
- task219 current implementation: §13 の理由で STATIC REJECTED。実行待ちではない。

## 18. 証人までの正直な距離

現在は「一様リフトを作る理論が何もない」段階ではない。次は紙上で立っている。

- finite actual corrections があれば compatible inverse-limit choice にする機構;
- 一つの finite word-pair identity を全 pro-3 rungs へ降ろす機構;
- universal boundary identity を三 endpoint に落とす機構;
- endpoint zero から boundary certificate を抽出する機構;
- solvable mixed-prime refinements を一塔で尽くす formation framework。

未完成なのは次である。

1. task192 の actual first correction;
2. task198 と結合した正しい actual first kernel/occurrence specialization;
3. pointed \(\mu_1\)、word-pair \(M\)、三 exact endpoints の positive;
4. その同じ word の mixed-prime actual target membership;
5. 残る perfect-core/field-outer actual gate。

従って感覚的な進捗は、**無限整合性の設計はかなり進んだが、証人そのものはまだ
最初の actual universal identity を一つも通過していない**、である。ここを通る前に
「あと一補題」とは言わない。一方、ここで必要な判定は既に有限で具体的な三 endpoint
まで縮んでおり、以前の「各段無限探索」より明確に強い位置にいる。

## 19. 次の実行命令

1. task192 run を妨げず terminal artifact まで待つ。
2. task198 は `CreateDirectory` portability だけを versioned repair し、SELFTEST を
   再実行する。これは機械実装なので Luna 範囲とする。
3. task192/task198 の accepted schema が揃った後、§13 の two-input specializer を
   新 task として実装する。現 task219 を部分修正して production に流さない。
4. actual data が出たら、v216 pre-gate、v214、v191、v198 の順に同じ object を通す。
5. 三 endpoint が零なら v197 で直ちに \(q\) を抽出し、v174 の relative pro-3
   theorem に接続する。非零なら初めて v195--v196 repair に移る。
6. それまでは新しい抽象 dihedral/formation 分類を増やさない。

これを次回以降の固定 checkpoint とする。新しい結果は、この依存鎖のどの矢印を
閉じたかを明記しない限り「証人の進捗」に数えない。

## 20. v220 基準の追記専用進捗台帳

研究者指示（2026-08-28）により、今後の進捗報告は全て本稿 v220 を基準にする。
各報告は少なくとも次の三分類を明記する。

- **CLOSED**: v220 の依存鎖の一矢印を、指定された証拠階級で実際に閉じた。
- **ADVANCED**: 実装、入力契約、資源障害などは前進したが、その矢印の数学的結論は
  まだ閉じていない。
- **UNCHANGED**: v220 から証人/fake への数学的距離は変わっていない。

「コードを書いた」「SELFTEST が通った」「quotient screen が通った」は、それぞれ
対応する actual mathematical gate が閉じない限り CLOSED に昇格しない。更新履歴は
下へ追記し、古い判定を消さない。

### v220-Δ1 — 2026-08-28 11:05 JST

1. **CLOSED（紙上 interface）**:
   `proof_r07_actual_first_edge_endpoint_specializer_v221.md` により、positive task192
   actual word と word-independent task198 interface から
   \((P_o,\xi_o,\epsilon_B,w,\bar\epsilon_1,u_0)\) を一意に作る二入力
   specialization contract を定理化した。task198 に word-specific fields を加える
   誤接続を除去した。
2. **ADVANCED（実装準備）**: task198 の GHA run `33133058026` を止めた未定義
   `CreateDirectory` に対する限定 portability patch を Luna が静的に作成した。
   producer/checker/GHA は未実行なので、v220 §14 の task198 矢印はまだ OPEN。
3. **UNCHANGED（actual mathematics）**: task192 はまだ production 中。actual
   \(w,\bar\epsilon_1,u_0\)、v216 membership、actual \(K\)、pointed \(\mu_1\)、
   word-pair \(M\)、三 exact PB endpoints は未計算。compatible pro-3 lift、
   mixed-prime gate、perfect-core gate、fake condition (iv)、Ihara witness は全て OPEN。

従って v220-Δ1 の証人距離の変化は「二入力 ABI の数学的曖昧さを一つ除去した」まで
であり、actual gate の positive はまだ 0 件である。

### 進捗報告形式の補正 — 研究者指示 2026-08-28 11:14 JST

以後は CLOSED/ADVANCED/UNCHANGED だけでなく、必ず次の二層を同時に報告する。

1. **個別進捗**: run、証明、修理、計算が具体的に何を返したか。
2. **v220 内進捗**: その結果が下の固定 task のどの小段階を完了し、現在
   何段階中の何段階か。

曖昧な総合 percentage は使わず、認証可能な milestone の分数を使う。実行中は
分子に入れず `RUNNING` を添える。紙上定理と actual positive は別 milestone とする。

| v220 ID | 固定 task | 完了 milestone |
|---|---|---|
| A0 | task192 actual exact word | positive terminal + independent acceptance: 0/1 |
| A1 | task198 complete roof interface | driver / producer SELFTEST / checker SELFTEST / production acceptance: 3/4 |
| A2 | actual two-input specializer | paper contract / implementation SELFTEST / actual specialization: 1/3 |
| A3 | v216 single-seed pre-gate | actual package / orbit closure / membership-or-dual: 0/3 |
| A4 | v188 actual successor kernel | presentation input / invariant closure / accepted word-bearing \(K\): 0/3 |
| A5 | v214 simultaneous pointed gate | joint rows / membership / accepted \(\mu_1\) ancestry: 0/3 |
| A6 | v191 word-pair | ancestry expansion / roof-fibre check / accepted \(M\): 0/3 |
| A7 | v198 exact PB endpoints | H1 / H2 / P exact endpoint zero: 0/3 |
| A8 | v197 boundary certificate | \(q_{H1}\) / \(q_{H2}\) / \(q_P\) extracted and replayed: 0/3 |
| A9 | v174 relative pro-3 lift | pointed Neumann / side gates / all-rung descent: 0/3 |
| B | mixed-prime actual membership | formation target / selector membership / solvable-cofinal descent: 0/3 |
| C | perfect-core actual gate | actual class / field-outer gate / coupled PB4 acceptance: 0/3 |
| W | compatible witness | compatible finite shadows / nonarithmetic roof binding / Ihara conclusion: 0/3 |
| F | fake fallback | TYPE-M / full fibre coverage / condition (iv): 0/3 |

#### v220-Δ2 — 2026-08-28 11:14 JST

**個別進捗**:

- task198 GHA run `33135147622` は修正済み driver を通過し、producer SELFTEST marker
  まで到達した。
- independent checker は `checker toy presentation semantics` で receipt を拒否した。
  従って checker の独立意味論差分を特定・修理する必要がある。
- 先行 run `33135060343` は JSON でない CLI dispatch が `"SELFTEST"` の引用符を
  落とした pre-driver STOP であり、task198 の milestone に数えない。

**v220 内進捗**:

- A1 は旧 0/4 から **2/4** へ前進。driver と producer SELFTEST は完了したが、
  checker SELFTEST と production acceptance は未完。
- A2 は v221 により **1/3**。paper contract のみ完了。
- A0 は **0/1 RUNNING**。run `33129456772` に positive terminal はまだない。
- A3--A9, B, C, W, F は全て **0 のまま**。

従って actual witness 主鎖の complete gate はまだ 0 件であるが、A1 の実装検収は
半分、A2 の設計は三分の一まで進んだ、というのが v220-Δ2 の正確な報告である。

#### v220-Δ3 — 2026-08-28 11:22 JST

**個別進捗**:

- task198 GHA SELFTEST run `33135595754`、immutable head
  `4b9a575618c6ea762f04039f30c9049e5446f6ec` は success。
- producer marker は `presentation_rows=9` で一回、independent checker marker は
  `mutation_attempted=44 mutation_rejected=44` で一回出現した。
- artifact id `9671905417`、ZIP digest
  `sha256:92c6f17655237cd94ec2d1164a06a113ce74ec86fbeafdce01c92f7e24ccf72f`。
- ダウンロード再読で receipt は 37,832 bytes / SHA-256
  `44e9fd741b96c84bc05dcb0e3071f97d90e208f73450afc859132cf09cd1c207`、
  `SELFTEST_COMPLETE`, `presentation_rows=9`。verdict は 455 bytes / SHA-256
  `4c128e404a5686b89fa6ebe2f5f08808780ebc8c6033bfc122319ab728503ddd`、
  `accepted=true`, `independent=true`, 44/44 rejection。

**v220 内進捗**:

- A1 は **2/4 → 3/4**。driver、producer SELFTEST、independent checker SELFTEST が
  完了。残る milestone は actual 6,441-row production acceptance の 1 件。
- A0 は **0/1 RUNNING**、A2 は **1/3** のまま。
- A3--A9, B, C, W, F は全て **0 のまま**。

この success は task198 実装の production-shaped SELFTEST 検収であり、actual roof
presentation、actual \(K\)、single-seed membership、または witness の positive ではない。

#### v220-Δ4 — 2026-08-28 11:27 JST

**個別進捗**:

- v222 で task176 cross-checked artifact run `33044121344` の payload を再取得・再hashし、
  task198 が要求する production-only `ci/in` receipt と artifact manifest を commit
  `3d8063d0c96165141347849fdae758dcf9371f26` に固定した。
- task198 actual PRODUCTION を GHA run `33135921512` として開始した。workflow hard
  timeout は 300 分、driver の registered wall cap は 14,400 秒、process は一つ。

**v220 内進捗**:

- A1 は **3/4 RUNNING**。production input availability は閉じたが、6,441-row producer
  と independent checker の acceptance がまだないので 4/4 には上げない。
- A0 は **0/1 RUNNING**、A2 は **1/3**、A3--A9, B, C, W, F は全て **0**。

従って v220-Δ4 は A1 最終 milestone の実行開始であり、actual witness gate の完了数は
まだ 0 件である。

#### v220-Δ5 — 2026-08-28 11:31 JST

**個別進捗**:

- task198 production run `33135921512` は producer の typed `UNKNOWN_INPUT` で
  6,441-row 計算前に停止した。checker は同じ nonpositive terminal を受理したが、
  driver は positive production 以外を fail-closed にした。
- v223 の静的監査で、task176 payload ではなく v222 staging manifest の nested key
  layout が producer の exact seven-key dictionary と不一致だったと同定し、同じ
  immutable values を strict schema へ修正した。

**v220 内進捗**:

- A1 は **3/4** のまま。production milestone は未完で、再実行待ち。
- A0 は **0/1 RUNNING**、A2 は **1/3**、A3--A9, B, C, W, F は **0**。

これは入力包装の STOP であり、roof presentation、single-seed gate、または witness の
negative evidence ではない。
