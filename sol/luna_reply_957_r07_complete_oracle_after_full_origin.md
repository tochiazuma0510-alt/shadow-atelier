# Task957 — v548 の joint kappa / source-edge ABI

F0. **設計のみ。** reply953、Tasks954/955、v548/v543/v546/v547/v459、両系 v15 と実 Task554 JSON を読んだ。進行中 run33967668257/1 の新しい rank・terminal・lambda・成否は前提にしていない。受理済み開始点は Task954 に記載された rank1359/gen8064 であり、新しい oracle の snapshot は root が実出力を受理してから固定する。本便は指定返信だけを作成した。Python/GAP/import/AST の実行、network、git、credential、dispatch、追加 agent はない。

**A–D の単一 snapshot scalar oracle を E の materializer より先に実装してよい。** A–D が同じ complete-source/Conn 前提、下記の正しい source adapter、全8059 kappa 等式、二 auxiliary 値、全54433 chord 等式を満たせば、v548 の完全な零判定の定理は変わらない。非零時には合法 cycle/aux と scalar の証明書を `MATERIALIZATION_PENDING` として封印できる。E はそれを実際の lower-zero physical row・rank rise にする consumer である。これは今回の数値判定の宣言ではない。

F1. **reply953 の補間順序を具体化し、誤読を訂正する。** 公開済み reply953 は変更しない。そこでの「保存された insertion order と actual prior-pivot 零条件」の説明を、source の逆代入順序として使ってはいけない。

`search/d972_r07_a0_first_rung_grade1_v3.py:662` の `PackedEchelon` は、行 ID を insertion order のまま保存する一方、`ordered_pivots` を `(lead,pivot)` の昇順に保つ。`reduce_packed`（683行）は最初の未使用 lead で止まる。そのため、後から挿入された小さい lead の行には、先に挿入された大きい pivot の成分が残り得る。`separating_dual`（760行）は `reversed(self.pivot_order())` を使う。2985行の非単調 lead fixture もこの契約を明示している。読んだ同ファイルの SHA256 は `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`。

実 JSON の例は次の通りである。

- prepare の `old_blocks[0].record.dag_nodes` の先頭 `(pivot,lead,scale)` は `(0,6054,1),(1,6055,2),(2,0,2)`。
- block0 の `pivot_leads` の先頭は `[0,1,3,504,5,4,7,6]`。`dag_nodes[p].lead == pivot_leads[p]` である。
- old の lead は width6056 の元座標。old に全 d1 companion を付けた full96776 行の `first_nonzero` で置換しない。

したがって **canonical row ID と chi の添字は保存し、双対補間は埋め込んだ元 lead の降順**で行う。これは Task954/955 の受理済み physical insertion-order basis の処理とは別の契約である。

F2. **A: Q2 と edge の固定配列。** 既存 v15 の `_SeedContext.psels/psidx` を P の順序とする。producer は `_seed_group`（553行）、checker は `_checker_seed_group`（1934行）。どちらも identity から P の右積を `(x,y,x^-1,y^-1)` の順に BFS する。P の新しい別順序を作らない。

`p=0..503`, `e=(e0,e1)` は `((0,0),(0,1),(1,0),(1,1))`、`k=(k0,k1,k2)` は各0..2とし、以下の **新しい Q2 export の順序**を固定する。

```text
eid_parity(e) = 2*e0+e1
kid(k)       = 9*k0+3*k1+k2
qid(p,e,k)   = ((eid_parity(e)*27+kid(k))*504+p)
N            = 54432
edge(q,g)    = 2*q+g,  g=0:X, 1:Y
```

| 配列 | 型・shape | 意味 |
|---|---|---|
| `next_pos` | little-endian uint32 `[N,2]` | `q -> qX,qY` |
| `prev_pos` | little-endian uint32 `[N,2]` | 上記二 permutation の逆 |
| `phi` | little-endian uint32 `[6,N]` | 同じ qid 宇宙内の各 tag の置換 |
| `tag_fox` | 12個の小さい順序つき list | `J(phi_j(X)), J(phi_j(Y))` の `(component,prefix_qid,coefficient)` |
| `parent,parent_edge,bfs_order` | uint32 `[N]` 各一本 | 後述の固定 tree。root の parent は明示 sentinel |
| `carry` | uint8 `[2*N,5]` | 正 edge の五 legality cochain、値0..2 |

group 座標は既存の section-left/kernel-right で、`S(e)=diag((-1)^e1,(-1)^e0,(-1)^(e0+e1))` とする。

```text
(p,e,k)*(p',e',k') = (pp', e+e', S(e')k+k')
```

根拠は producer v15 `_seed_perm_mul:443`, `_seed_affine_mul:511`, `_seed_affine_inv:518`、checker の対応箇所1889/1897。permutation は `right[left[i]]` の GAP 順である。正 edge の後続は **右積**なので、kernel は `S(e_g)k+k_g`。既存 `context.pmap(g)`（producer626/checker2005）は `p -> gp` の **左積**であり、`next_pos` として呼べない。右 P map は `psidx[perm_mul(psels[p],g_P)]` から新たに作る。

六 tag の generator words は v15 `SEED_OO:56` のまま固定する。

| j | phi_j(X) | phi_j(Y) |
|---:|---|---|
|0|`(1)`|`(2)`|
|1|`(1)`|`(-1,-2)`|
|2|`(2)`|`(-1,-2)`|
|3|`(-2,-1)`|`(1)`|
|4|`(1)`|`(2)`|
|5|`(-2,-1)`|`(2)`|

`phi[j,0]=0` から tree に沿って、同じ generator word の actual affine endpoint を掛けて vertex map を作る。**全 q と二正 generator** で `phi_j(qg)=phi_j(q)phi_j(g)`、全 map の bijectivity、`phi[0]=phi[4]=identity` を確認・封印する。A-character transport だけから phi の存在を代用しない。v459 の19 relator/五 Nielsen map が同じ Q0 に下降し、characteristic な `3 O_3(Q0)` を保つという前提に対応する実配列の gate である。0/4 の重複を source の六 occurrence の一つへまとめて消さない。

F3. **B: joint kappa の二段階 ABI。** source lower は以下の固定 flatten とする。

```text
b = concat(d0[4,6048], d1[4,18144], aux[8]) : F3[96776]
z = d2[4,36288]
O=(0,505,1008,1511),        old ranks=(505,503,503,503)
H=(2014,3523,5035,6547),    new ranks=(1509,1512,1512,1512)
```

canonical P1 cache の行 `i` は z_i 全四 character、145152 trits / 36288 bytes。`q:uint8[4,36288]` と current scan の `p1-cA.u8` の shape `[5,8059]` の第0行から、全四 character を足して

```text
chi:uint8[8059],  chi[i] = sum_a dot(q[a],z_i[a]) mod3
```

を作る。各 q と P1 値は同じ snapshot の lambda/source/owner/scan manifest に結ぶ。新しい prefix に old rank1355 の contraction 値を流用しない。current scan がない場合には own `fresh_vectors/p1_contract` または checker の対応する contraction を新たに呼ぶ契約とし、旧固定 character assertions は呼ばない。

保存された行は既に normalized である。`dag_nodes[p].scale` は元の生成 instruction の係数であり、blob row にもう一度掛けない。

**段1: new d1。** owner a の `basis_blob` は packed width18144、行 p の global ID は `H[a]+p`。lead は実 `pivot_leads[p]` と `dag_nodes[p].lead` を接続する。`k1:uint8[4,18144]` を0で初期化し、各 owner で **lead 降順**に

```text
k1[a,lead_p] = chi[H[a]+p] - sum_(j != lead_p) k1[a,j]*new_row[a,p,j] mod3
```

を代入する。入力として normalized pivot 値1、元 lead より前の成分が零、lead の重複なしを確認する。free coordinates は0のまま。行の物理 offset は常に `p*(18144/4)` で、sorted traversal の序数に変更しない。

**段2: old d0＋共有 aux。** old a,p の二 payload は `lower_basis_blob` width6056 と `lifted_grade_blob` width72576。後者は `[4,18144]` に戻す。まず

```text
beta[O[a]+p] = chi[O[a]+p] - dot(k1,old_grade[a,p]) mod3.
```

old lower を `E=F3^(4*6048+8)=F3^24200` に埋め込み、d0 を owner a に置き、最後の8 aux は共有する。元 lead l の E 座標は

```text
embed_old_lead(a,l) = a*6048+l               if l<6048
                    = 24192+(l-6048)         otherwise.
```

`kE:uint8[24200]` を0で初期化し、この埋込 lead の **全 old 行を通じた降順**で `kE[lead]=beta_i-dot(kE,row_i)` を代入する（更新前の当該 lead は0）。元 lead を別の first_nonzero で作り直さない。old0 の aux6/7 は E の24198/24199、返す full lower の96774/96775である。old 非自明 character の aux は0という保存型は grade1_v3 `projected_seed_pair:468` と `associated_lower_actor:497` に現れる。埋込 row の元 lead・正規化・重複なしも実読込で確認する。

返値は `kappa=(kE[:24192].reshape(4,6048),k1,kE[24192:])`。shared aux を四組に複製しない。値を封印する最終条件は次の**全8059等式**である。

```text
for every a,p in new:
  dot(k1[a],new_row[a,p]) == chi[H[a]+p]
for every a,p in old:
  dot(kE,embed_old_lower[a,p]) + dot(k1,old_grade[a,p]) == chi[O[a]+p]
```

`chi[8059]`, `beta[2014]`, `kappa[96776]`, 全8059 dot/result または residual bytes、元 row ID/lead/order、12 blob pins を receipt に持つ。kappa の full packed bytes は同じ four-trits-per-byte とする。物理 lower rank6705 の multiplier を求める段階は不要である。

F4. **C: raw edge への具体的 pullback。** 座標を次の view に戻す。

```text
q  : [4,6,2,6,504]     (degree2 monomials)
k0 : [4,6,2,504]
k1 : [4,6,2,3,504]
kA : [8]
degree1 order = (u0,u1,u2)
degree2 order = (u0^2,u0*u1,u0*u2,u1^2,u1*u2,u2^2)
```

`chi_{j,a}(e)=(-1)^(context.transport[j][CHARACTERS[a]] dot e)`、`C_mu(k)=prod_i binom(k_i,mu_i) mod3` とする。`score:uint8[6,2,N]` を

```text
score[j,c,(p,e,k)] = sum_a chi_(j,a)(e) * (
    sum_(|mu|=2) q[a,j,c,mu,p]*C_mu(k)
    - k0[a,j,c,p]
    - sum_i k1[a,j,c,i,p]*k_i) mod3
```

で定義する。これは `sum_a q_a Psi2[a]-kappa Psi1` の regular 部分の adjoint である。producer は `_seed_e_poly:644` と実 transport を再利用できる。checker は own ordinary27/binomial extraction から十係数を作るなど、別の算術経路で全 score/edge 値を作る。homogeneous Task712 T だけからこの source map を生成しない。

raw positive edge `(q,g)` の tag j への Fox push は

```text
sum_(h,c,d in J(phi_j(g))) d * (component=c, vertex=phi_j(q)*h).
```

`tag_fox` は producer `_seed_affine_fox:534` / checker `:1914` に **短い substituted generator word** を渡して得る。この helper は endpoint-one を要求しない。正 letter は進む前の prefix、負 letter は逆元で進んだ後の prefix に符号−を置く。左積 `phi_j(q)*h` の kernel は **入力 h の parity** による `S(e_h)k_phi+k_h`。左側 phi_j(q) の parity をここへ入れない。

その後の右 qnorm は `_seed_qnorm:743` / checker `:2118` の式そのものだが、既存関数は closed word 専用である。したがって raw edge 用には **新しい線形 gradient-to-qnorm helper** が要る。actual `B=(YX)^-1` を使い、Fox term `(c,s,d)` を

```text
c=0:  (PB3 component0, sX, -d), (component1, sXB, -d), aux_j += d
c=1:  (PB3 component1, s,  +d)
```

へ送る。`X B=Y^-1` なので第二 vertex は `prev_pos[s,1]` とも照合できる。これで edge cochain は明示的に

```text
f[edge(q,g)] = sum_j sum_(c,h,d in tag_fox[j,g])
  if c=0: d*(-score[j,0,sX]-score[j,1,sXB]-kA[j])
  if c=1: d*score[j,1,s]
  where s=phi_j(q)*h, all mod3.

b_aux = (-kA[6],-kA[7]) mod3.
```

となる。返値は `f:uint8[108864]`, `b_aux:uint8[2]`。aux0..5 は各 tag の Fox x-augmentation、aux6/7 は **独立な eta 入力**である。後者を raw edge augmentation から18で割って作る操作はない。forward の `Psi_edge` は同じ stencil の scatter 版、`Psi(z,eta)` は同じ z を全六 tag に通し aux6/7へ eta を加える版として新たに作れる。forward の返値は `d0[4,6048],d1[4,18144],d2[4,36288],aux[8]`。これは既存 full source word evaluator と比較するためにも使えるが、その export はまだない。

F5. **A/D: marked tree/carry と完全 EOF。** Q2 の qid 順序と独立に、identity から正 generator `(X,Y)` の順だけで BFS tree を作る。有限生成群なのでこの正 edge graph は到達可能であり、実装では全N頂点、N−1本の tree edge、重複なしを確認する。`T_v=T_parent(v)*letter(parent_edge(v))` を tree SLP とする。chord は tree edge 以外の正 edge を `edge_id` 昇順に全54433本保存する。

carry は v546 §3 の **rotation-left** で計算する。v15 の k をそのまま入れず、vertex で `v=S(e)k mod3` とし各座標を0,1,2で代表する。既存 `scratchpad/fuda1_a0_rmax_data.g:3`–4 の **36点 Q0 permutation 自体**を読む。最初の9点が P、残る9点 block をそれぞれ局所座標 `u=0..8` で読むと、X は `(u+1,-u,-u)`、Y は `(1-u,u+1,1-u)`（mod9）である。新しい geometry gate は元の全36点をこの first-P/three-affine-block 記述から再構成して exact equality を要求する。これが section/kernel 座標で

```text
X: e=(1,0), k9=(1,0,0)
Y: e=(0,1), k9=(1,1,1)
```

を与える（点 n の像は `S(e)n+k9`）。**Q2 の mod3 値を勝手に0..2へ持ち上げたのではない。** この actual Q0 marking から rotation-left generator の0..8代表 `vX9=(1,0,0)`, `vY9=(8,1,8)` を得る。新 adapter は上記36点 equality を通してから、実際の整数符号で

```text
carry[edge(q,g),i] = (v_i + S_i(e)*vG9_i - [v_i+S_i(e)*vG9_i]_3)/3 mod3,
carry[edge(q,0),3:5]=(1,0),  carry[edge(q,1),3:5]=(0,1).
```

を作る。除算は整数の割算である。負 edge を読む場合は `-carry[edge(q*g^-1,g)]`。section を変えた別 marking の generator 値を混ぜない。

tree の親順に `pot_f[head]=pot_f[tail]+f[tree_edge]`、`pot_tau[head]=pot_tau[tail]+carry[tree_edge]`、rootで0とする。各 chord e について

```text
r_e = f[e]+pot_f[tail]-pot_f[head]
t_e = carry[e]+pot_tau[tail]-pot_tau[head] : F3^5
z_e = path(root,tail)+e-path(root,head)
```

を全 roster に保存する。返値は `r:uint8[54433]`, `tau:uint8[54433,5]` と tree potentials。chord順に、五座標を0..4の順で消去して最初の五つの独立な t を選ぶ。`T[:,j]=t_(e_j)` として `a*T=(r_(e_1),...,r_(e_5))` を解く。五本集まらなければ prerequisite failure とし、tau の次元を黙って下げない。

二 auxiliary を x,y の順で調べ、全54433の `r_e-a*t_e` を比較・封印する。first hit のみで EOF を代替しない。`b_aux=0` と全 residual零のときに初めて、v548(5.4)の有限 identity の入力がそろう。ここで保存する零判定は full-origin の root EOF とは別の証明書である。

非零の場合の固定 witness 順は、aux x、aux y、それらが零なら最初の failed chord。後者では `d=T^-1*t_e` として

```text
z = z_e - sum_(j=1)^5 d_j*z_(e_j),
tau(z)=0, f(z)=r_e-a*t_e !=0.
```

五つの基準 chord と failed chord の ID、d、全 scalar/tau 等式を seal する。六 cycle は項数の上限であり、展開 word 長や実行時間の上限ではない。A–D はここで止めてもよい。

F6. **E: sealed witness からの新 consumer。** 次の手順は未作成であり、Task954 の seed/actor materializer を cycle 用機能と呼ばない。

1. failed chord の `W_e=T_tail*g*T_head^-1` を先頭に置き、その後に基準 chord を選択順 j=1..5で置く。係数 `-d_j` は0,1,−1の signed representative とし、0を省略する。この順序で `w=W_e product_j W_(e_j)^(-d_j)` を SLP 化する。tau零から w は N0、整数 exponent A,B は6の倍数と分かる。
2. SLP に `(A,B,omega)` を持たせ、`omega(uv)=omega(u)+omega(v)+B(u)A(v)`、`omega(u^-1)=-omega(u)+A(u)B(u)`、`omega(u^m)=m*omega(u)+m(m-1)/2*B(u)A(u) mod3` を使う。A,B と冪指数は整数のまま保つ。
3. v459 の固定 `r_x=q1*q6^-2*q7^4*q9`, `r_y=q8^-1*q4^-1` から、v547 の固定順
   `C(z)=w*(r_x^3)^(-A/6)*(r_y^3)^(-B/6)*[r_x,r_y]^sign(omega(w))`
   を作る。commutator は `u^-1 v^-1 u v`。`C(z)` は Omega、exact exponent(0,0)、Q2 Fox=z、eta=0という契約である。27-element endpoint table は不要。
4. aux branch は `(z,eta)=(0,e_x)` または `(0,e_y)` とし、literal は `c_x=r_x^9` / `c_y=r_y^9`。**ここで先に exact exponent を0へ正規化してはいけない。** 選んだ eta 方向そのものを消すためである。
5. 新しい raw-Fox SLP evaluator は product `J(uv)=J(u)+u J(v)`、inverse `J(u^-1)=-u^-1 J(u)` を持ち、endpoint と raw Q2 chain を出す。v15 の signed-letter affine/Fox primitives は bounded atom に再利用できるが、任意 SLP export は存在しない。closed-word-only `_seed_qnorm` を非閉 tree prefix へ渡さない。raw chain が sealed z と一致し、eta が指定値であることを接続して F4 の complete source tuple u を得る。
6. **primal P1 reduction は双対補間と段順も方向も違う。** 先に old joint d0/shared-aux を埋込元 lead の昇順で消去し、同じ係数でその old 行の全 d1 companion も引く。old ID は O[a]+p のまま。次に各 new d1 block を元 lead の昇順で消去する。返値は `alpha:uint8[8059]` と ordered reduction events。末尾の全96776 lower零を要求し、`b_u=sum_i alpha_i*b_i` を照合する。
7. 同じ alpha と accepted canonical P1 index/cache で `z'=u.d2-sum_i alpha_i*z_i` を作る。producer の `subtract_lifts`（Task954:753）や checker の `source_lift`（Task955:644）の row/blob/receipt primitives は再利用できるが、cycle用 selection/SLP/segment consumer は新設する。literal は u の word の後ろに canonical P1 words の負係数因子を **reduction-event 順**で付け、数値係数集約で literal ancestry を書き換えない。
8. **物理行は `G=sum_a B_a(z'[a])`。** full cochain の scalar は四 character の和なので、Task954 の一 character 選択 wrapper をそのまま使って他の三つを落とさない。全 lower-zero、`lambda(G)=sum_a dot(q_a,z'[a])=F(u)!=0` を要求する。physical reduction/normalized append/target/new lambda は新しい origin type の wrapper から own retained arithmetic に渡す。E が終わるまで新しい rank rise は宣言しない。

v547 の word normalization と v548 の linear section subtraction は別の R である。P1 word 因子を付けた後は integer exponent を改めて記録する。source lower-zero からは nu=0 mod3 が分かるが、exact exponent零を自動的に主張しない。必要な exact normalization はその後の literal consumer で、同じ source bytes を保つことまで接続する。十一 physical slot、他 grade、full A0 の完成は本設計に含めない。

F7. **追加入力と実在／未作成の区別。** 新データを発明して追加する必要はないが、新しい export は必要である。

| 入力 | 既存 path / pin と読取契約 |
|---|---|
| current snapshot | Task954 output の `HEAD`, `start.json`, `owner.json`, `source.json`, `canonical-index.json`, `steps/NNNNNN/manifest.json` とその rows/target/lambda。latest `scans/NNNNNN/manifest.json` が HEAD にあれば `root-cA.bin`, `p1-cA.u8` を同じ lambda に接続。新 run の exact pins は未受領であり本便では作らない。Memberでlambdaがなければ本 separator oracle の入力型ではない。原rho2の新しい直接読込は要求しない。 |
| canonical P1 | run33851744070/1、artifact9931437113、commit `6673eb2ea15ca6022acc2ddc5a8a204a0380172f`。`manifest.json` 17472 bytes / `86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb`、`degree2.cache.bin` 292444992 / `b88edb9b12753cdb7a3629403f8ac14206595e03525fa2a201b6b00b985c1abf`、`instructions.jsonl` 349055442 / `8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae`。accepted v9 parent である。 |
| Task554 lower | run33677346616/1、commit `22c6dddb43d107c05e65f53ad898823ae8ebe276`。prepare body `prepare.1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865.json` と `block-0.9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74.json`, `block-1.d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6.json`, `block-2.a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac.json`, `block-3.642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01.json`。各 basename の digest が body SHA。12 lower blobs の正確な file/width/rows/bytes/SHA は pinned batch の `OLD_BLOB_PINS / NEW_BLOB_PINS`（checker96–144行）をそのまま使う。総67011332 bytes。 |
| 実物を読んだ場所 | `%TEMP%/task554-prepare-33677346616-1-pinextract/`、`%TEMP%/r07_grade1_blocks_33677346616/b0/`。prepare は top-level `old_blocks`、new は top-level `pivot_leads/dag_nodes/basis_blob`。`.body` は loader の返値 wrapper であり JSON 内にはない。 |
| marking | `scratchpad/fuda1_a0_rmax_data.g` 4709 / `625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba`。既に v15 の source data pin。Q0三9点 block→mod9座標の接続は新 export。 |
| 44-word dictionary | `scratchpad/a0_paper_words_v1.json` 115928 / `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893`。既存 actual source word/PC dictionary。 |
| 19-word normalizer dictionary | `scratchpad/a0_v2_words.json` 106133 / whole-file SHA `fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612`。`raw_q0_relators` の canonical list SHA は別の `dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a`。この list digest は compact ASCII JSON、LFなし。`scratchpad/a0_v2_words.py` 4868 / `3f605fedbdc6b3167388d775c31c8fdb879c405cae711435715fabf352e4b742` は独立抽出の根拠で、今回再実行していない。 |
| Task712 | 現 snapshot owner の四つの manifest/forward B/actor table の exact descriptors を継承する。A–Dで必要な数値 map は B と current q、E は四つの B を合計する。physical full mixed C/6705-row mu の新 export は不要。 |

v459 の literal check digest は `r_x`=`82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c`、`r_y`=`88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0`、`c_x`=`2935d479d5896360e71b66aa95bcb964cdb04d9716f27c06f492034b5ac98abb`、`c_y`=`c1f3ebec1ef6c448b854b216f8473e674a67a3b5d3a3059888af016293a1a6dd`。これも compact signed-letter list の digest であり、future SLP JSON の seal と取り違えない。

算術系統の既存 pin は producer/checker v15 がそれぞれ `76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632` / `8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662`、root scalar batch v2 が `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` / `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6`。既存 source/metadata primitive は各自の系統で使い、新しい補間、graph、adjoint、tree solve を相手から共有しない。

F8. **最小の実装単位と出力境界。** A=`geometry_inputs`（Q2右 edge、phi/tag Fox、qnorm stencil、tree、carry）、B=`current_section`（同一 snapshot の q/chi/kappa と全8059式）、C=`source_cochain`（全 score/f/b_aux）、D=`complete_tree_test`（五 independent columns、全 chord arrays/EOF、sealed witness）を paired scalar oracle の四つの境界にする。E=`selected_readout` はその後の独立した word/P1/physical consumer とする。これらの関数名は **提案 ABI** であり、既存 export の名前ではない。

新 checker は新 full-origin `check_actual` を単なる state loader として呼ばない（それは scan/insert の再生器である）。受理済み snapshot の hash/payload/chain を読む薄い loader を別途書き、現在の lambda を全保存 physical 行と受理済み target に接続する。先行 source、Conn、canonical P1 の completeness premises を数値再構築する作業へ拡張しない。

各小単位で full array と identity receipts を比較できる。raw edge の左右規約、mixed degree0/1→2、shared eta、非単調 lead は今回変更される具体的境界の canary 対象である。全8059式と全54433式は省略できない本体条件であり、旧504や過去の character sparsity は利用しない。今回の成果は実装可能な設計であり、新しい numerical gate、NONMEMBER/MEMBER、rank、fullword、cross-checked、verified は宣言しない。

AUDIT_957_VERDICT: DESIGN_COMPLETE — A–D may precede E; source kappa uses descending embedded original leads, and no new runtime outcome is claimed.
