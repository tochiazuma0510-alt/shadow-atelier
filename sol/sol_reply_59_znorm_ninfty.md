# 便 59 返信 — `Z-norm-seal/v1` 採用ゲート / \(N_\infty\) stage-2 spec v1 監査

## 総合判定

| 部 | 判定 | 結論 |
|---|---|---|
| **Part A — `Z-norm-seal/v1`** | **条件付き PASS** | full profinite normalization を独立 seal として採る数学的原理、`Z-norm` \(\Rightarrow\) `Z20-link`、逆を断つ witness、A3/有限札との分離は正しい。ただし現 draft のままの発効は不可。**profinite canonical edge と既存 level-20 Rule edge の型分離、既存 seal との object identity、全窓量化、K3 の \(b_{\rm op}/b_{\rm cmp}\) の 4 点を直した差分**を発効条件とする。 |
| **Part B — \(N_\infty\) stage 2 spec v1** | **差戻し** | (F-1) の norm 恒等式と、非退化な degree-5 多項式に対する gcd 判定核は正しい。しかし **N∞-F の「fiber と根が重複度込み 1:1」は一般には偽**、**N∞-L の「有限二値は各々 \(\iota\)-固定」は偽**である。さらに target の調和条件 \(\{s,-s\}\) が ACCEPT 述語から落ち、現 §2.3 は誤った固定場合だけを強制する。**spec freeze ID は発行しない。実装着手禁止を維持する。** |

従って二部を独立に進めるなら、Part A の小版イベントは下記 P59-A1–A4 の機械的修理後に進めてよい。Part B は数学述語を v2 として再提出する必要がある。**Part A の採用は Freeze 2 成立、\(N_\infty\) 再開、A3 閉鎖を一切含意しない。**

---

## F1. 対象・digest・改行の検収

委嘱は配達先

```text
ops/inbox_codex/sol_task_59_znorm_ninfty.txt
```

から読み、対象二 blob は委嘱指定 commit `eaea1780612ae2f99759b807d98da8bbb3587e18` と現 HEAD で無差分であることを確認した。

| 対象 | 行数 | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/znorm_seal_draft.md` | 100 | `c1ba4d16be08b741dde01daddd5d4ebb8b12b3d624a6d3422e5855b39f7d8a68` | 委嘱値と一致 |
| `docs/week4-NInfty_stage2_spec_v1.md` | 375 | `77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2` | 委嘱値と一致 |

両ファイルとも CR = 0、TAB = 0、LF 以外の C0 制御文字 = 0。これは内容判定とは独立の blob 検収である。

---

# Part A — `Z-norm-seal/v1`

## F2. 数学的な採用原理は PASS

### F2.1 全 root 系の選択

\(\bar\iota:\overline{\mathbb Q}\hookrightarrow\mathbb C\) を
\(\iota_\infty\) の延長として選び、

\[
\zeta_n^{\rm TB2}:=
\bar\iota^{-1}\!\left(e^{2\pi i/n}\right)
\qquad(n\ge1)
\]

と置けば

\[
(\zeta_{mn}^{\rm TB2})^m=\zeta_n^{\rm TB2}
\]

である。従って compatible root system は実在する。これは算術的存在仮定の追加でなく、従来 \(n\nmid20\) で未指定だった比較データの**規約選択**である。TB4 v2.4 §8.1 の本体を保存している。

### F2.2 finite seal への含意

\(\bar\iota|_K=\iota_\infty\) と Rule 1 (1.6) より

\[
\zeta_{20}^{\rm TB2}
=\bar\iota^{-1}(e^{2\pi i/20})
=\zeta_{20}^{\rm Rule1}.
\]

従って

\[
\texttt{Z-norm-seal/v1}\Longrightarrow
\texttt{Z20-link-seal/v1}
\]

は正しい。

逆向きを断つ \(\widehat{\mathbb Z}^{\times}\) の unit、すなわち
2-adic・5-adic 成分が \(1\)、3-adic 成分が \(-1\)、他が \(1\)
である witness も正しい。level 20 では恒等だが profinite には恒等でない。
従って両 seal を別 ID・別 scope とし、finite theorem の前件を
profinite seal へ置き換えない判断も PASS である。

### F2.3 発効後の theorem status

次の区別は正しい。

- TB4-B は
  `paper theorem relative to Z-norm-seal/v1 and the TB4 framework`
  となる。
- \(\varepsilon=1\) は Lean `verified` ではない。
- A3 は別の framework/orientation gate のまま残る。
- TB4-A20 は `conditional on Z20-link-seal/v1` の有限札を保つ。
- `root_normalization_level=profinite` は、その seal と object IDs を
  実際に参照する record にだけ許される。
- Rule 1 (7.1) の実測、二段コミット、観測後 fitting 禁止、
  `(5′_b)` は不変である。

この意味で、研究者意向である「全 root normalization を工房規約として
選んで TB4-B を相対定理化する」こと自体は採用してよい。

---

## F3. 現 draft をそのまま発効できない 4 条件

### F3.1 P59-A1 — profinite edge と既存 Rule edge を分離する

現 §1(3) は

```text
edge_id       = rule1-tb2-root-equality/profinite-v1
lhs           = root_system_tb2_id
rhs           = canonical_root_system_id
canonical     = bar_iota^{-1}(exp(2*pi*i/n))
```

である。ところが既存 `Z20-link-seal/v1` の named edge は

```text
edge_id       = rule1-tb2-root-equality/v1
lhs           = root_system_tb2_id
rhs           = rule1_root_2M_id
scope         = level_20
```

である。新 edge の rhs は Rule object ではなく canonical profinite
root system であり、しかも lhs と rhs は同じ \(\bar\iota\) の同じ式で
同時に定義される。これは profinite normalization の**定義的等式**
としてはよいが、`rule1-...` と名付けると既存の独立な Rule edge と型が
衝突する。

次の二辺を別々に保たなければならない。

```text
edge_id  = "tb2-canonical-root-equality/profinite-v1"
lhs      = root_system_tb2_id
rhs      = canonical_root_system_id
scope    = profinite
proof    = forall n, both sides are bar_iota^{-1}(exp(2*pi*i/n))

edge_id  = "rule1-tb2-root-equality/v1"       # 既存 ID を維持
lhs      = restrict(root_system_tb2_id, n=20)
rhs      = rule1_root_2M_id
scope    = level_20
proof    = Z-norm(1)(2) + Rule 1 (1.6)
```

profinite edge の equality certificate は「無限列を列挙した digest」でなく、
上の \(\forall n\) の証明 artifact とその digest でなければならない。

### F3.2 P59-A2 — 既存 finite seal の object identity を固定する

§2 の含意証明は値の等式を示すが、版イベントに必要なのは artifact の
identity まで含む typed extension である。少なくとも

```text
Z-norm.bar_iota_id = Z20-link.bar_iota_id
restrict(Z-norm.root_system_tb2_id, n=20)
    = Z20-link.root_system_tb2_id
derived_level20_edge_id = "rule1-tb2-root-equality/v1"
```

を固定すること。単に「どちらも \(\iota_\infty\) を延長する」だけでは、
別の extension ID が二本並び、finite result record と profinite result
record が別 object を参照できてしまう。

### F3.3 P59-A3 — 「全窓」と「既存窓を上書きしない」を同時に total 化する

§1(4) は「すべての窓・すべての \(M\)」が同一 edge を参照すると全称する。
一方 §3-5 は、独立に凍結済みの埋め込みを持つ窓を自動的には
上書きしないとする。この二文は現状では同時に operative にできない。

安全な条文は次である。

> `root_normalization_level=profinite` を主張する全 TB4 comparison は、
> この `bar_iota_id`、profinite root-system ID、profinite canonical edge
> を参照しなければならない。既存窓は migration/compatibility certificate
> が出るまで従来の normalization level に留まり、seal 採用だけで
> `profinite` に昇格しない。

小版イベントには window inventory を付け、

```text
window_id / previous_level / rule_root_id /
compatibility_status / migrated_record_digest
```

を列挙すること。競合 object が無いことと、同一 object が記録されたことは
別の主張である。

### F3.4 P59-A4 — K3 行の \(b\) の型を直す

§3-5 の

> \(b_{\rm op}=1\) には当該窓の Rule 側生成元が同じ
> \(\bar\iota\) を通して定まっていることが要る

は、TB4 v2.4 §3.5.1a/§3.5.2 の辞書と衝突する。共通 package の下では

\[
b_{\rm op}=1
\]

は TB4-E により root-link-free である。Rule 側 root の compatibility が
必要なのは

\[
t_{12}=1,\qquad
\varepsilon\equiv1\pmod{12},\qquad
b_{\rm cmp}=1,\qquad
b_{\rm cmp}=b_{\rm op}
\]

の側である。

従って K3 行は次へ直すべきである。

> TB2 側の profinite root は本 seal で確定する。K3 の Rule 側
> \(\zeta_{12}\) に同じ object を採用する explicit migration edge が出れば
> \(t_{12}=1\)、\(\varepsilon\equiv1\pmod{12}\)、
> \(b_{\rm cmp}=b_{\rm op}=1\) が従う。
> \(b_{\rm op}=1\) 自体の最小前件は従来どおり TB4-E package であり、
> root compatibility を最小前件へ追加しない。

現行 BFC proof artifact が link 前件を保持することと、定理の最小前件が
root-link-free であることも混同しないこと。

---

## F4. Part A の発効条件と小版イベント payload

### F4.1 条件付き認可

P59-A1–A4 を**逐語的に満たす差分**なら、full `Z-norm-seal/v1` の
数学的採用について新たな定理候補ゲートは不要である。ただし current
digest は draft の digest であり、**発効 seal の digest として使っては
ならない**。修理後 blob を新たに hash し、差分検収を通すこと。

### F4.2 payload

小版イベントの最小 payload は次である。

1. `docs/znorm_seal_draft.md` を履歴として残し、修理済み final seal を
   versioned artifact として新設する。status、seal ID、full SHA-256 を固定。
2. P59-A1 の二 named edge、P59-A2 の restriction/identity certificate、
   P59-A3 の window inventory を event receipt に束縛する。
3. TB4-B の札を
   `root-normalization-relative paper theorem / A3-framework-conditional`
   へ更新する。TB4-A20 の有限札は変更しない。
4. TB4 dictionary の `root_normalization_level=profinite` を、
   `znorm_seal_id` と profinite equality edge が存在する record に限り許可する。
5. \(B_{\rm FC}\) の draft が列挙した 8 箇所を同期する。ただし
   exact \(\varepsilon=1\) が bridge theorem の無条件化や Lean verification
   を意味する文言は入れない。
6. Rule 1 / manifest は旧版を上書きせず次 version を作り、
   既存 `Z20-link-seal/v1` と既存 edge ID を保存したまま、
   full seal への typed reference を追加する。
7. `provenance/CLAIMS.md` には「root convention の採用手続き」と
   「TB4-B の相対定理化」を区別して追記する。W3-19 を書き換えない。
8. receipt の `non_implications` に少なくとも

   ```text
   A3_closed = false
   lean_verified = false
   freeze2_established = false
   ninfty_reopened = false
   finite_Z20_status_replaced = false
   ```

   を置く。

---

# Part B — \(N_\infty\) stage-2 spec v1

## F5. 入口契約で二つの S5 条件が落ちている

S5 の \(N_\infty\) 正規形は単に
\(\deg f_6=6,\deg a=5,\deg p=2\) ではない。少なくとも

\[
f_6\ \text{monic squarefree},\qquad
a_5=p_2\ne0,\qquad
a^2-f_6p^2=\hat c_\mu\in\mathbb Q^\times
\tag{5.1}
\]

であり、これが

\[
(\mu)=5\infty_- - 5\infty_+
\]

の向きを固定する。現 P-1 は monic と \(a_5=p_2\) を持たない。
Pell の最高次項だけから出るのは、monic の下でも
\(a_5=\pm p_2\) までであり、符号は cusp の向きを入れ替える。
§2.6 の後段 assert に委ねず、入口の typed precondition に入れるべきである。

さらに S5 系 S5-2a の target は passport だけでなく

\[
\boxed{\ \operatorname{Br}(\mu)=\{0,s,-s,\infty\}\ }
\tag{5.2}
\]

という**調和条件**を含む。現 §1.1 はこれを「有限非零値が 2 個」へ弱め、
§2.8 も二値の和が 0 であることを検査しない。passport が同じでも
\(\{v_1,v_2\}\ne\{s,-s\}\) なら \(\lambda=c\mu^2\) の二値が同じ Belyi
branch value へ落ちず、campaign の候補ではない。

出所も次へ直すこと。

- divisor \(5P_0-5P_\infty\): S5-1;
- 分解 \(\lambda=c\mu^2\): S5-2;
- \(\mu\) の調和 branch data: **S5-2a**;
- \(N_\infty\) Pell 正規形: S5-3∞、およびその後の Sol 便 36 F2.1。

現出所表の「S5-2 が divisor と branch type の双方を与える」は粗すぎる。

---

## F6. 補題 N∞-F — 恒等式 PASS、1:1/partition は FAIL

### F6.1 正しい核

\[
H_v=(v-a)^2-p^2f_6
=v^2-2va+\hat c_\mu
\tag{6.1}
\]

と

\[
H_v=-2v(a-w),\qquad
w=\frac{v^2+\hat c_\mu}{2v}
\tag{6.2}
\]

は正しい。さらに本質的な意味は

\[
\boxed{\ H_v=
(v-\mu)(v-\mu^\iota)
=N_{\mathbb Q(C)/\mathbb Q(x)}(v-\mu)\ }
\tag{6.3}
\]

である。従って \(H_v\) の零 divisor は、fiber divisor の
hyperelliptic projection \(\pi:C\to\mathbb P^1_x\) による
**norm/pushforward** である。

### F6.2 反例機構

\(p(x_0)=0\)、\(f_6(x_0)\ne0\)、\(v=a(x_0)\) とする。Pell より
\(a(x_0)^2=\hat c_\mu\) で、\(x_0\) 上の相異なる二点 \(Q,\iota Q\) は
どちらも \(\mu=v\) へ写る。一方

\[
H_v=(v-a)^2
\]

は \(x_0\) に二重点を持ち得る。これは fiber 上の「一つの \(e=2\) 点」
でなく、二つの単純点の multiplicity の**和**である。

従って

> \(\deg H_v=\deg\mu=5\) だから根が重複度込みで fiber と 1:1

という証明は成立しない。同じ総次数は、projection が二点を同じ
\(x\)-座標へ畳むことを排除しない。

### F6.3 正しい適用範囲

\(Q\in\mu^{-1}(v)\) で
\[
\mu^\iota(Q)=\frac{\hat c_\mu}{v}\ne v
\]
なら、(6.3) の他方の因子は \(Q\) で単元である。特に
\[
v^2\ne\hat c_\mu
\tag{6.4}
\]
なら fiber は \(p=0\) と Weierstrass locus を避け、
\(\pi\) は fiber 上で 1:1 となり、\(H_v\) の根 multiplicity と
\(\mu^{-1}(v)\) の ramification multiplicity は一致する。

逆に
\[
v^2=\hat c_\mu
\tag{6.5}
\]
なら、fiber の全点で
\(\mu=\mu^\iota\)、従って \(p\,y=0\) である。すなわち spec が
「別扱い」とした exceptional locus に**fiber 全体**が乗る。

従って N∞-F は次へ直すべきである。

> \(H_v\) は常に fiber divisor の norm/pushforward を与える。
> \(v^2\ne\hat c_\mu\) のときだけ、その根 partition は fiber
> partition と一致する。\(v^2=\hat c_\mu\) のときは
> \(p=0\) / Weierstrass の局所 divisor を \(C\) 上で直接計算する。

現 warning (F-a)–(F-c) を後置するだけでは、boxed lemma の全称と
「1:1」の証明を救えない。

---

## F7. 系 N∞-P — 狭い多項式補題としては PASS

標数 0、\(\deg F=5\) の一つの多項式について

\[
\deg\gcd(F,F')=2,\qquad \gcd(F,F')\ \text{squarefree}
\tag{7.1}
\]

なら、根 multiplicity の excess
\(\sum_r(m_r-1)\) は 2 で、各 \(m_r\le2\) である。従って根 partition は
\([2,2,1]\)。逆も正しい。

\[
\gcd(F,F',F'')=1
\tag{7.2}
\]

も正しい安全検査だが、(7.1) の squarefree 条件があれば数学的には
冗長である。冗長な独立 alarm として残すことには賛成する。

ただし現 N∞-P を \(\mu\)-fiber へ適用できるのは、

1. \(F=H_v\) が degree 5 の一つの affine polynomial であること、
2. 全 root が F6.3 の非退化 locus にあること、
3. infinity component や二点の projection aggregation が無いこと

を証明した後だけである。「chart ごとの divisor を貼り合わせたもの」には
そのまま \(\gcd(H,H')\) は定義されない。homogeneous divisor の local
multiplicity を使うか、aggregate 後の単一 polynomial を明示する必要がある。

また \(w\) は一般には algebraic である。`a-w` の gcd を
「exact 有理演算だけ」で行うなら、
\(\mathbb Q[W]/(g(W))\) 上の subresultant、既約因子ごとの residue field、
重複 critical value の primary component の仕様が必要である。
現 §2.3 はこれを定義していない。

結論は次である。

- **degree-5 polynomial lemma として N∞-P は PASS**;
- **現 N∞-F と組み合わせた global fiber criterion としては FAIL**。

---

## F8. 補題 N∞-L — \(\iota\)-固定性の論証は偽

### F8.1 二値集合には二つの orbit type がある

\[
j(v):=\frac{\hat c_\mu}{v}
\]

とする。二つの有限 branch values \(\{v_1,v_2\}\) が \(j\)-安定なら、

1. \(j(v_i)=v_i\) が両方で成り立つ **fixed case**;
2. \(j(v_1)=v_2,\ j(v_2)=v_1\) の **swapped case**

の二場合がある。

swapped case では

\[
H_{\hat c_\mu/v}
=\frac{\hat c_\mu}{v^2}H_v.
\tag{8.1}
\]

従って二 fiber は同じ \(x\)-root divisor を持つが、各 \(x\)-root 上で
一方の fiber point とその \(\iota\)-共役が別々の branch value へ写る。
同じ二つの \(x\)-coordinates が、

- \(v\) 上の二つの \(e=2\) 点;
- \(\hat c_\mu/v\) 上の二つの \(e=2\) 点

を同時に担える。有限部の ramification contribution は
\[
2+2=4
\]
であり、\(0,\infty\) の \(4+4\) と合わせて RH の 12 に**ちょうど一致**
する。

従って

> 同じ \(w\) なら \(a'\) の根を二つしか消費せず、ramification sum が不足

という §1.5 の数え上げは、\(x\)-root と \(C\) 上の ramification point を
混同している。二つの \(x\)-roots は二つの conjugate fibers で四つの
ramification points を表す。

### F8.2 target の調和条件を入れると、正しい一般結論は \(\pm\)

S5-2a の有限 branch set は \(\{s,-s\}\) である。この集合が \(j\)-安定なら

\[
\begin{array}{ll}
\text{fixed case}: & s^2=\hat c_\mu,\\
\text{swapped case}: & s^2=-\hat c_\mu.
\end{array}
\tag{8.2}
\]

従って便 54 F12.4 の正しい leakage lemma は

\[
\boxed{\ s^2=\pm\hat c_\mu\ }.
\tag{8.3}
\]

\(-1=i^2\in K^{\times2}\) なので、どちらの場合も

\[
[s^2]=[\hat c_\mu]\in K^\times/K^{\times2}.
\tag{8.4}
\]

sealing の結論は維持されるが、exact sign を \(+\) に固定してはならない。
現 §10 の

> 便 54 F12.4 と同内容

も誤った provenance である。便 54 は明示的に \(\pm\) と述べており、
本稿はそれを強化したのでなく、偽の fixedness を追加している。

### F8.3 この \(N_\infty\) 正規形では target は swapped case を強制する

さらに \(\deg p=2\)、\(f_6\) squarefree を使うと、この campaign の
target では fixed case を排除できる。

fixed value \(v\) なら \(v^2=\hat c_\mu\) で、fiber 全点は \(py=0\) にある。

- \(y=0,\ p\ne0\) では \(y\) を uniformizer として
  \(\mu-v=p(x_0)y+O(y^2)\)、従って \(e=1\)。
- \(p(x_0)=0,\ y(x_0)\ne0\) で \(m=\operatorname{ord}_{x_0}p\) とすると、
  \[
  (a-v)(a+v)=f_6p^2
  \]
  から \(\operatorname{ord}(a-v)=2m\)、一方
  \(\mu-v=(a-v)+py\) の先頭は \(py\) なので、\(Q,\iota Q\) の双方で
  \(e=m\)。
- \(p=y=0\) なら \(y\) を uniformizer として \(e=2m+1\) であり、
  \(e=2\) にはならない。

従って fixed fiber に二つの \(e=2\) 点を作るには、\(p\) が一つの
double root を持たねばならない。それは \(\deg p=2\) の全てを使い、
\(a(x_0)\) は \(v,-v\) の片方にしかならない。よって**二つの fixed
fibers の双方**を \([2,2,1]\) にすることはできない。

従って所望 target では二値は交換され、

\[
\boxed{\ j(s)=-s,\qquad s^2=-\hat c_\mu\ }.
\tag{8.5}
\]

これは現 N∞-L の結論と逆である。

---

## F9. 正しい target では stage 2 はさらに単純化できる

### F9.1 現 §2.3 は誤った場合だけを強制している

現 §2.3-3 は

\[
w^2=\hat c_\mu,\qquad v=w
\]

を要求する。これは fixed case である。しかし F6.3 より fixed fiber は
全て exceptional locus にあり、直後の N∞-P の非退化仮定を満たさない。

すなわち現 spec は

1. §2.3 で全 fiber を exceptional にし、
2. §2.4 で non-exceptional な \(a-w\) gcd criterion を適用する

という内部矛盾を持つ。

また、調和条件 (5.2) を検査しないため、仮に partition/count が通っても
campaign target でない二値を ACCEPT し得る。

### F9.2 swapped case の紙上簡約

正しい target では \(s^2=-\hat c_\mu\) なので

\[
H_s=s^2-2sa+\hat c_\mu=-2s\,a,\qquad
H_{-s}=2s\,a.
\tag{9.1}
\]

\(a(x_0)=0\) なら Pell より

\[
p(x_0)^2f_6(x_0)=-\hat c_\mu=s^2\ne0.
\]

従って両 finite fibers は自動的に \(p\ne0,\ f_6\ne0\) の非退化 locus にあり、

\[
\boxed{\
\operatorname{part}\mu^{-1}(s)
=\operatorname{part}\mu^{-1}(-s)
=\operatorname{rootpart}(a).
\ }
\tag{9.2}
\]

よって target の有限二 fiber に必要な gcd test は、algebraic な全 critical
values \(w\) を列挙するのでなく、**有理係数多項式 \(a\) 一本**について

\[
\deg\gcd(a,a')=2,\qquad
\gcd(a,a')\ \text{squarefree},\qquad
\gcd(a,a',a'')=1
\tag{9.3}
\]

を検査すればよい。

Pell を微分すると

\[
2aa'=p(f_6'p+2f_6p'),
\]

\(\gcd(a,p)=1\) なので

\[
p\mid a'.
\tag{9.4}
\]

\(a\) が \([2,2,1]\) なら、\(a'\) の残る二根は \(p\)-locus である。
ここを局所計算し、余分な ramification が無いことを二 chart/RH で
assert すれば全 branch set が閉じる。

### F9.3 v2 述語の候補

次の順なら、値を開かず \(\mathbb Q\) 上の exact arithmetic で閉じられる。

1. (5.1)、curve smoothness、Pell、divisor orientation を検査。
2. (9.3) により \(a\) の root partition が \([2,2,1]\) であることを検査。
3. \(p\)-locus、Weierstrass locus、二 infinity を \(C\) 上で局所検査。
4. finite branch polynomial が degree 2 かつ even、すなわち
   \[
   B_{\rm fin}(V)=V^2-\sigma
   \]
   であることを sealed に検査し、人間可視には
   `finite_branch_pair_harmonic=true` の boolean だけを出す。
5. \(\sum(e_Q-1)=12\)、有限 branch count 2、余分な branch 0 を検査。

この置換は \(\Delta_a(W)\) の algebraic roots、固定/交換の誤判定、
individual branch-value digest を全て不要にする可能性がある。
ただし v2 で命題として明文化し、もう一度 differential audit を受けること。

---

## F10. searcher/checker・fixture・EP の設計判定

### F10.1 二経路設計

「searcher と checker が同じ predicate を別経路で実装する」原理は
**条件付き PASS**。しかし現 §2.1 は searcher を
「resultant を使わない divisor 経路」と呼びながら、§2.3 で
\(\operatorname{Res}_x(a-W,a')\) を使う。さらに両者が偽の N∞-L と
critical-value reduction を共有するので、現状では共通の predicate bug を
独立に見逃す。

推奨する分離は次である。

- **Searcher**: \(C\) 上で \(d\mu\) の ramification divisor を二 chart の
  local expansion から直接作り、\(\mu\) で pushforward する。
- **Checker**: discriminant/resultant の baseline multiplicity と saturation
  を一般補題で証明した上で使う。searcher の local/divisor helper を共有しない。

この二つなら geometry と elimination の真の別経路になる。

### F10.2 negative regression の 3 欄

`verdict + multiplicity_partition + triple_gcd_degree` の 3 欄一致は
verdict 単独より強く、**設計判断として PASS**。可能なら
`gcd_squarefree=false` も alarm として記録するとよい。

ただし現 §4 は

> 照合器入力にしてはならない

としながら、§6 V-8 は v2 全域再走の出力を checker が検査するとする。
v2 全域で旧 tuple が再出現した場合の扱いが矛盾する。正しくは

> 旧 hit を genuine candidate の救済入力・順位付け入力にしてはならない。
> quarantine された negative-test lane では、neutral fixture ID の下で
> searcher/checker の双方が同じ rejection mechanism を再現してよい。

と用途を分けるべきである。

8 件の `triple-fiber-at-x0` 証明は、便 54 F6 が確認した
\(p(0)\ne0,\ f_6(0)\ne0\) まで proof ID に含めること。現 §1.4 の説明は
\(p(0)\ne0\) しか再掲せず、N∞-F の Weierstrass 例外を閉じていない。

### F10.3 EP

実曲線・実写像の end-to-end positive control と、EP 不在中の
`partial predicate / UNKNOWN` は PASS。

ただし

> 別の \((f_6,\deg)\) 設定

が次数そのものを変えてよいという意味なら、P-1 で REJECT されるので
calibration にならない。EP は**本番でない係数**を持つが、

```text
deg f6 = 6, deg a = 5, deg p = 2,
f6 monic squarefree, a5 = p2 != 0,
same N_infty predicate schema
```

を満たさなければならない。「same schema / non-campaign coefficients」
と明記すること。

### F10.4 schema の小さな不整合

freeze 前に次も直すこと。

1. §2.0 の reason code は `degree-mismatch` 等、§7 は
   `precondition/degree-mismatch` 等で不一致。
2. `fibers[]` が branch fiber と chart component を同じ一行に潰す。
   `fiber_id -> chart_components[] -> aggregate_partition` の二層にする。
3. `predicate_spec_id` の参照先を「§8」とするが、§8 は whitelist で
   freeze ID の定義が無い。
4. §2.1 の checker 参照「§5」は実際には §6。
5. §10 の条件番号が本文の §2.3/§2.4 とずれている。

---

## F11. leakage / whitelist 監査

### F11.1 literal 非開示

本 spec に、便 54 で問題となった具体値、具体 tuple の係数、
明示の branch value は転記されていない。この literal grep の点は PASS。
`aliases_blocked` を非網羅列挙とし、新 field の挙証責任を追加側へ置く
原理も PASS である。

### F11.2 shard 名が sign を符号化している

§4 の human-visible table は

```text
a5m / a5p / p21 / p2m1
```

を含む raw shard filenames を掲載する。これは直後の

> fixture 名に値・符号を含めない

と両立しない。neutral `ninfty-neg-01` … `08` だけを公開し、
raw shard との対応は quarantine/taint ledger の sealed mapping に移すこと。

### F11.3 SHA-256 は concealment ではない

**本便での自己訂正**: 便 54 F12.2 で私が「人間可視には digest と
partition だけ」と提案したうち、**raw deterministic digest を secrecy
境界として扱う部分は不十分だった**。旧返信は記録として変更せず、
本便でこの一点を訂正する。

SHA-256 は値を平文表示しないが、値の関数である。bound \(\le5\) の有限な
探索宇宙では dictionary attack が可能なので、

```text
candidate_id = sha256(canonical tuple)
branch_value_digests = sha256(canonical branch value)
```

を pre-Freeze-2 human-visible に出しても「値を含まない」とは言えない。
特に branch value は canonical algebraic-number serialization、
共役の順序、基礎体表現も未定義で、再現可能な digest にすらなっていない。

安全な分離は次である。

- sealed 区画: unkeyed artifact digest を保持して integrity binding に使う;
- human-visible: 高 entropy の random opaque `candidate_id` /
  `fiber_ref` のみ;
- どうしても事前 commitment が必要なら、
  secret nonce または HMAC key を clean steward が Freeze 2 後まで保持し、
  reveal 時に binding を検証する;
- branch value の deterministic digest は pre-Freeze-2 には出さない。

dependency audit は量そのものだけでなく、その deterministic
commitment にも適用しなければならない。

---

## F12. Part B の差戻し条件と freeze 裁定

次の P59-B1–B7 を満たす v2 を再提出すること。

| ID | 必須修理 |
|---|---|
| **P59-B1** | S5-3∞ の monic・\(a_5=p_2\ne0\)・divisor orientation と、S5-2a の調和条件 \(\{s,-s\}\) を入口/ACCEPT に復元 |
| **P59-B2** | N∞-F を norm/pushforward lemma と、\(v^2\ne\hat c_\mu\) の 1:1 corollary に分割。fixed fiber は局所 divisor へ |
| **P59-B3** | 現 N∞-L の fixedness を撤回し、少なくとも \(s^2=\pm\hat c_\mu\) へ戻す。本正規形では F8.3 の swapped lemma \(s^2=-\hat c_\mu\) を独立命題として検分 |
| **P59-B4** | §2.3 の \(w^2=\hat c_\mu,\ v=w\) 強制を撤回。F9 の \(a\)-partition 経路、または fixed/swapped を total に扱う別の正しい述語へ置換 |
| **P59-B5** | searcher/checker の真の別経路、exceptional charts、harmonic boolean、余分な branch の排除を schema 化 |
| **P59-B6** | raw digest 公開、sign-bearing shard 名、fixture/checker 用途矛盾、EP の degree、reason/cross-reference/schema grouping を修理 |
| **P59-B7** | 修理版の end-to-end positive control と 8 negative fixtures の機構一致を、実装前の spec と分離して事前登録 |

現 SHA

```text
77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
```

は**監査対象 draft の digest**にすぎず、freeze digest ではない。

```text
predicate_spec_id = mb/ninfty-stage2-predicate/v1
```

その他の frozen ID は**発行しない**。実装認可も出さない。

再提出 v2 が PASS した場合の発行形式は、例えば

```text
predicate_spec_id      = "mb/ninfty-stage2-predicate/v2"
predicate_spec_digest  = "sha256:<full repaired blob digest>"
freeze_event_id        = "<commander-assigned event id>"
supersedes_draft       = "sha256:77ed7131..."
implementation_status  = "authorized only after freeze receipt"
```

とし、ID と digest を一体で参照すること。

---

## F13. 共同設計者としての発案

### F13.1 `N∞-swap` を独立補題にする

F8.3 を

> **Lemma N∞-swap.**  
> \(N_\infty\) Pell 正規形、\(\deg p=2\)、\(f_6\) squarefree、
> finite branch fibers が二つとも \([2,2,1]\)、branch pair が
> \(\{s,-s\}\) なら target involution は二値を交換し、
> \(s^2=-\hat c_\mu\)。

として切り出す。この補題は、

- leakage の正しい根拠;
- \(H_{\pm s}\propto a\) の簡約;
- 8 fixture の triple-root rejection;
- fixed/swapped の分岐漏れ防止

を一つの paper proof ID へ束ねる。

### F13.2 branch value を作らない certificate

人間可視 certificate は branch values/digests でなく

```text
finite_branch_count = 2
finite_branch_pair_harmonic = true
a_root_partition = [2,2,1]
exceptional_locus_clear = true
ramification_sum = 12
```

だけでよい。exact branch polynomial と値は sealed proof object 内に置く。
これは whitelist を守るだけでなく、algebraic-number serialization の
未定義も消す。

### F13.3 ramification divisor を第一 object にする

fiber ごとの ad hoc gcd でなく、

```text
ramification_divisor_on_C
branch_divisor_on_P1
fiber_decomposition_by_branch_ref
```

を certificate の第一 object とする。searcher は local differential、
checker は saturated elimination で同じ divisor digest に到達する。
「resultant の指数」と「fiber partition」の再融合を schema が防げる。

---

## F14. ★教材

1. **norm polynomial は fiber そのものではなく fiber の押し出しである。**  
   同じ \(x\)-座標上の conjugate points は一つの根 multiplicity に合算される。

2. **passport と branch-value geometry は別の条件である。**  
   \((5,2^21,2^21,5)\) だけでは \(\{0,s,-s,\infty\}\) の調和条件は戻らない。

3. **二点の対称集合は「二点とも固定」と「二点を交換」を必ず場合分けする。**  
   \(x\)-root 二つを \(C\) 上の ramification point 二つと数えると、
   conjugate fiber の寄与を半分落とす。

4. **例外処理を付記しても、定理文の全称は直らない。**  
   主経路自身が fixed case を強制し、その fiber 全体が exceptional なら、
   「必要時に別扱い」ではなく述語を二枝化しなければならない。

5. **hash は commitment であって暗号化ではない。**  
   小さい探索宇宙の deterministic digest は、辞書照合により値の別名になる。

6. **seal の edge 名は rhs の型まで含む。**  
   `rule1-*` edge の rhs が canonical root system なら、名前だけでなく
   provenance graph も嘘になる。

7. **定理の最小前件と現行 proof artifact の前件を分ける。**  
   \(b_{\rm op}=1\) の root-link-free 性と、現 BFC proof が link を保持する
   ことは両立する。

---

## F15. 監査範囲

### 読んで突合したもの

- `ops/inbox_codex/sol_task_59_znorm_ninfty.txt` 全文;
- `docs/znorm_seal_draft.md` 全文;
- `docs/week4-NInfty_stage2_spec_v1.md` 全文;
- `docs/week4-TB4導出_opus_v1.md` の §3.5.1a、§8.1、§8.2、§8.5、
  §8.6、§8.6a;
- `docs/week4-K5_Rule1_v1_4.md` §1.4.1;
- `docs/week4-K5_S5設計_opus_v1.md` の S5-1/S5-2/S5-2a、
  §3.3.5、S5-4∞;
- `sol/sol_reply_36_freeze1r5.md` F2、`sol/sol_reply_54_event_candidates.md`
  F6–F12、`sol/裁定_66_ben54.md`;
- `provenance/CLAIMS.md` の W3-19 と現行非含意。

### 実行・閲覧していないもの

- quarantine 済み 8 tuple の係数、生 certificate、具体 branch values;
- bound \(\le5\) の探索再走;
- searcher v1/v2 の実装、resultant helper、独立 checker の実行;
- GAP、Node/Python による候補計算、Lean;
- 外部文献。

従って本返信の Part B は、正典の式と spec 本文に対する**紙上数学監査・
schema 監査**である。候補の存在/非存在、bound \(\le5\) の探索結果、
陽性例の存在は主張しない。campaign 全体は従来どおり
`BRIDGE-UNKNOWN`、\(N_\infty\) は hard stop のままである。
