# 便 60 返信 — `Z-norm-seal/v1` draft v2 差分検収 / \(N_\infty\) stage-2 spec v2 再監査

## F1. 総合判定

| Part | 判定 | 裁定 |
|---|---|---|
| **Part A — `Z-norm-seal/v1` draft v2** | **条件付き PASS — 小版イベントの発効許可を出す** | P59-A1–A4 の差分は閉じた。新たな定理候補ゲートは不要であり、F5 の 8 項 payload による小版イベントを進めてよい。ただし、現 draft blob はそのまま operative にはできない。F4 の発効時修理・実 artifact digest の記入・新 hash・receipt を一つの transaction とすること。 |
| **Part B — \(N_\infty\) stage 2 spec v2** | **差戻し** | `N∞-fix`、`N∞-swap`、`N∞-red`、`N∞-div` の数学核は通った。しかし `N∞-N` の divisor 等式が標準記法では偽、`N∞-1:1` の multiplicity 証明が欠け、ACCEPT の必要十分定理・T-2 の型・T-6/T-7 の状態遷移・divisor の canonical serialization・sealed/public 境界がまだ閉じていない。**freeze ID は発行しない。searcher/checker の実装認可も出さない。** |

Part A の許可は Part B の freeze、Freeze 2、A3 の閉鎖、Lean
`verified`、または \(N_\infty\) Model-Builder の再開を含意しない。

---

## F2. 対象 blob・digest・形式検収

委嘱全文、対象二文書、便 59 の現行裁定、TB4 導出 v2.4 の該当節、
S5 設計の命題 S5-1/S5-2/系 S5-2a/命題 S5-3∞、および対話帳の
T-17 までを読んだ。

対象は委嘱指定 commit `595e3b1` の次の二 blob である。

| 対象 | LF 行数 | SHA-256 | 委嘱値との照合 |
|---|---:|---|---|
| `docs/znorm_seal_draft.md` | 156 | `5b071429df5c72db95ee60ab2a88ba4efb05ff1b7ee32de349959bdeb39360eb` | 一致 |
| `docs/week4-NInfty_stage2_spec_v2.md` | 390 | `813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4` | 一致 |

両 blob とも CR = 0、TAB = 0、LF 以外の C0 制御文字 = 0。
seal の §1 に `level_20` は 0 件、§2 に `for every n` は 0 件であり、
申告された逆向き/順方向 scope lint も再現した。

これは blob 同一性と形式の照合であって、数学的裁定とは別である。

---

# Part A — `Z-norm-seal/v1`

## F3. P59-A1–A4 差分検収

### F3.1 P59-A1 — PASS

次の二 edge は別 ID・別 rhs・別 scope として正しく分離された。

```text
tb2-canonical-root-equality/profinite-v1
    lhs   = root_system_tb2_id
    rhs   = canonical_root_system_id
    scope = profinite

rule1-tb2-root-equality/v1
    lhs   = restrict(root_system_tb2_id, n=20)
    rhs   = rule1_root_2M_id
    scope = level_20
```

前者の certificate を「無限個の値を列挙した digest」でなく、

\[
\forall n\ge1,\qquad
\zeta_n^{\rm TB2}
=\bar\iota^{-1}(e^{2\pi i/n})
=\zeta_n^{\rm can}
\]

という一つの proof artifact とその digest にした点も正しい。既存 finite
edge ID を改名せず、lhs だけを `restrict(..., n=20)` で型付けした点も
P59-A1 を満たす。

### F3.2 P59-A2 — PASS

§2 (2-b) は

```text
Z-norm.bar_iota_id
    = Z20-link.bar_iota_id

restrict(Z-norm.root_system_tb2_id, n=20)
    = Z20-link.root_system_tb2_id

derived_level20_edge_id
    = "rule1-tb2-root-equality/v1"
```

の三 identity を固定した。「同じ値を与える」だけでは二本の extension
artifact が同時に存在できる、という理由も記載されている。値等式から
artifact identity への無断昇格は残っていない。

### F3.3 P59-A3 — PASS

window inventory は五欄を持ち、

```text
migrated | pending | not_assessed
```

を閉じた enum とし、欠落・未知値の fallback を禁止している。K5、K3、
A5 と明示 catch-all の四行で total である。A5 は `pending` であり、
grep の負の観測を「非存在の証明」に昇格させていない。K3 も
`pending` のままで、seal 採用だけによる自動昇格を禁じている。

K5 の `migrated_record_digest` が空なのは、現 blob が **draft** である
限りは申告どおりである。ただし schema 自身が `migrated` なら
REQUIRED と定めるので、これは F4 の発効 transaction で必ず実値に
置換されなければならない。

### F3.4 P59-A4 — PASS

K3 行は正しく

\[
\begin{aligned}
&\text{TB4-E package}\Longrightarrow b_{\rm op}=1
   &&\text{(root-link-free)},\\
&t_{12}=1\Longrightarrow
  \varepsilon\equiv1\pmod {12},\
  b_{\rm cmp}=1,\
  b_{\rm cmp}=b_{\rm op}
   &&\text{(explicit migration edge が必要)}
\end{aligned}
\]

を分けた。現 BFC proof artifact が link 前件を保持することと、定理の
最小前件が root-link-free であることの混同も明示的に禁止された。

従って **P59-A1–A4 の差分そのものは全部 PASS** である。

---

## F4. Part A の発効 transaction に残る機械的条件

これは P59-A1–A4 の再差戻しではなく、「draft を operative artifact に
変える瞬間」に満たすべき apply 条件である。一つでも欠ければ発効は
fail-closed とする。

### F4.1 K5 migration record と proof artifact

最終 seal を hash する前に、

1. profinite \(\forall n\) equality proof artifact と digest;
2. K5 の typed migration/identity record と digest;
3. 実在する `bar_iota_id`、root-system IDs、二 named edge IDs

を発行し、K5 行の `migrated_record_digest` を実値で埋めること。
`migrated` と空 digest の組合せを final artifact に残してはならない。

自己参照 hash を避ける安全な順序は

```text
proof artifact / migration record
    -> final seal にその digest を埋める
    -> final seal を hash
    -> event receipt が final seal hash と全 component を束縛
```

である。final seal 自身に、それを含む receipt の digest を要求して
循環させてはならない。

### F4.2 「commit していない」の状態文を final へ持ち越さない

§8 の

```text
status/CLAIMS 全域更新前・commit していない
```

は、対象 blob が commit `595e3b1` に存在する現在の事実と一致しない。
履歴 draft の起草時状態と、現時点の repository 状態を分け、

```text
committed as draft / unapproved / non-operative
```

相当へ直すこと。final artifact ではさらに event receipt に対応する
`approved / operative` 状態と発効時刻を固定すること。

### F4.3 \(n\nmid20\) の「どこにも現れない」は過大

§1 の

> \(n\nmid20\) の \(\zeta_n\) は現行正典のどこにも現れない純粋な空白

はそのままでは偽である。TB2/TB4 は抽象的な全 root system を既に使い、
K3 正典にも \(\zeta_{12}\) という field object は現れる。空白なのは
**root の存在や記号**ではなく、

> \(n\nmid20\) における
> \(\zeta_n^{\rm TB2}\) の具体値、および各 window の Rule-side object
> との typed comparison/equality record

である。便 59 F2.1 も「未指定だった比較データ」とだけ述べており、
この狭い文へ戻すこと。これなら「新しい算術仮定でなく規約選択」という
結論は不変である。

### F4.4 explicit catch-all を「既定」と呼ばない

§3 は default fallback を禁止する一方、最終行と出所表で
`not_assessed (既定)` / `最終行の既定` と書く。最終行は

```text
上記以外のすべての window を明示的に捕捉する catch-all rule
```

であって default 値ではない。final では `明示 catch-all` に統一すること。
未知 enum 値や行欠落をこの catch-all で救済してはならない。

### F4.5 final hash

F4.1–F4.4 と status/CLAIMS 同期を適用した **新しい versioned final
artifact** を hash し、その full SHA-256 を receipt に置くこと。本便で
照合した draft hash

```text
5b071429df5c72db95ee60ab2a88ba4efb05ff1b7ee32de349959bdeb39360eb
```

を発効 seal の digest として使うことを明示的に禁止する。

---

## F5. Part A — 小版イベント payload の発効許可

上の F4 を同一 transaction で満たすことを条件に、便 59 F4.2 の
**8 項 payload を変更なく認可する**。

1. 現 draft を履歴として残し、修理済み final seal を versioned artifact
   として新設する。status、seal ID、full SHA-256 を固定する。
2. P59-A1 の二 named edge、P59-A2 の restriction/identity certificate、
   P59-A3 の window inventory を event receipt に束縛する。
3. TB4-B の札を
   `root-normalization-relative paper theorem / A3-framework-conditional`
   へ更新する。TB4-A20 の有限札は変更しない。
4. TB4 dictionary の `root_normalization_level=profinite` は、
   `znorm_seal_id` と profinite equality edge が存在する record にだけ
   許可する。
5. \(B_{\rm FC}\) draft が列挙した 8 箇所を同期する。ただし
   exact \(\varepsilon=1\) を bridge theorem の無条件化または Lean
   `verified` と書かない。
6. Rule 1 / manifest は旧版を上書きせず次 version を作る。既存
   `Z20-link-seal/v1` と既存 finite edge ID は保存し、full seal への
   typed reference を追加する。
7. `provenance/CLAIMS.md` では「root convention の採用手続き」と
   「TB4-B の相対定理化」を分けて記録し、W3-19 を書き換えない。
8. receipt の `non_implications` に少なくとも

   ```text
   A3_closed = false
   lean_verified = false
   freeze2_established = false
   ninfty_reopened = false
   finite_Z20_status_replaced = false
   ```

   を置く。

**Part A 最終裁定**:

```text
P59-A1..A4 differential = PASS
small release event      = AUTHORIZED subject to F4 atomic apply
current draft operative  = false
new theorem gate         = not required
```

---

# Part B — \(N_\infty\) stage-2 spec v2

## F6. 新補題群の紙上監査

以下では \(\hat c_\mu\) を \(C\) と略記する。

### F6.1 `N∞-N` — norm 恒等式 PASS、divisor 定理文は FAIL

\[
H_v=(v-\mu)(v-\mu^\iota)
=(v-a)^2-p^2f_6
=v^2-2va+C
\]

は正しい。しかし §1.2 の

\[
\operatorname{div}(H_v)=\pi_*(\mu^{-1}(v))
\tag{v2-N}
\]

は標準的な `div` の意味では成立しない。左辺は次数 0 の principal
divisor であり、右辺は次数 5 の effective fiber divisor だからである。
正確には、\(v\ne0,\infty\) に対し

\[
\boxed{
\operatorname{div}_{\mathbf P^1_x}(H_v)
=\pi_*\operatorname{div}_{C}(v-\mu)
=\pi_*[\mu^{-1}(v)]-5[\infty_x]
}
\tag{60.1}
\]

または零 divisor だけを取って

\[
\boxed{(H_v)_0=\pi_*[\mu^{-1}(v)]}
\tag{60.2}
\]

と書くべきである。証明も「二乗消去」だけでなく
`norm -> divisor pushforward` を明示すること。

従って **factorization/norm の核は PASS** だが、freeze 対象の
定理文 (v2-N) は修理必須である。

### F6.2 `N∞-1:1` — 主張 PASS、multiplicity 証明が未完

\(Q\in\mu^{-1}(v)\) なら

\[
\mu^\iota(Q)=\frac{C}{v}.
\]

従って

\[
\boxed{\ \iota Q\in\mu^{-1}(v)\iff v^2=C\ }.
\tag{60.3}
\]

これは \(Q=\iota Q\)、すなわち \(y(Q)=0\) の場合も同じである。その場合
\(\mu(Q)^2=\mu(Q)\mu^\iota(Q)=C\) だから、そもそも \(v^2\ne C\)
の fiber には Weierstrass point がいない。

\(v^2\ne C\) では \(\pi\) は fiber 上で unramified かつ単射であり、
\[
(v-\mu^\iota)(Q)=v-\frac Cv=\frac{v^2-C}{v}\ne0.
\]
よって norm の他方の因子は単元で、

\[
\operatorname{ord}_{x(Q)}H_v
=\operatorname{ord}_{Q}(v-\mu).
\tag{60.4}
\]

これが multiplicity partition 一致の必要な一行である。現証明は集合の
単射までしか示さず (60.4) を書いていないため、**statement は PASS、
proof artifact は未完**と判定する。

### F6.3 `N∞-fix` — PASS

\(v^2=C\) なら fiber 全体で \(py=0\)。三場合は exhaustive である。

- \(y=0,\ p\ne0\): \(y\) が uniformizer、\(py\) の位数が 1 なので
  \(e=1\)。
- \(p=0,\ y\ne0\): \(x-x_0\) が uniformizer。
  \(m=\operatorname{ord}_{x_0}p\) とすると
  \(\operatorname{ord}(a-v)=2m\) と
  \(\operatorname{ord}(py)=m\) から \(e=m\)。
- \(p=y=0\): \(y\) が uniformizer で
  \[
  \operatorname{ord}_Q(p)=2m,\quad
  \operatorname{ord}_Q(py)=2m+1,\quad
  \operatorname{ord}_Q(a-v)=4m+2,
  \]
  ゆえに \(e=2m+1\)。

特に (iii) から \(e=2\) は出ない。

### F6.4 `N∞-swap` — PASS

有限調和対 \(\{s,-s\}\) は \(j(v)=C/v\) の下で

1. 二点とも fixed、従って \(s^2=C\);
2. 二点を swap、従って \(s^2=-C\)

の二場合しかない。

fixed fiber で \(e=2\) が出るのは `N∞-fix` (ii) の \(m=2\) だけである。
\(\deg p=2\) なら double root は一つしかなく、その \(x_0\) が与える
fixed value \(a(x_0)\) も一つである。従って二つの fixed fiber の双方を
\([2,2,1]\) にはできない。ゆえに target は swap され、

\[
\boxed{j(s)=-s,\qquad s^2=-C}.
\]

起草者の三場合は網羅的であり、F8.3 の独立再構成は通った。

### F6.5 `N∞-red` — PASS

\(s^2=-C\) なら

\[
H_s=-2s\,a,\qquad H_{-s}=2s\,a.
\]

\(a(x_0)=0\) では

\[
p(x_0)^2f_6(x_0)=-C=s^2\ne0,
\]

従って \(p(x_0)f_6(x_0)\ne0\)。また
\(s^2=-C\ne C\) なので `N∞-1:1` の non-fixed 条件も満たす。
よって

\[
\operatorname{part}\mu^{-1}(s)
=\operatorname{part}\mu^{-1}(-s)
=\operatorname{rootpart}(a)
\]

は正しい。

### F6.6 `N∞-div` — PASS、ただし T-2 の読み替えが必要

Pell を微分すると

\[
2aa'=p(f_6'p+2f_6p').
\]

\(\gcd(a,p)=1\) より \(p\mid a'\) は正しい。

一方、\(d:=\operatorname{monic}\gcd(a,a')\) と置き、
\(\operatorname{rootpart}(a)=[2,2,1]\) とすると
\(\deg d=2\)、\(d\) は squarefree である。\(\gcd(p,a)=1\) なので
\(\gcd(p,d)=1\)、かつ \(\deg a'=4=\deg p+\deg d\)。従って exact な
整合式は

\[
\boxed{\ a'\doteq p\,d,\qquad \frac{a'}p\doteq d\ }.
\tag{60.5}
\]

現 T-2 の「\(a'/p\) が \(p\) と比例しない場合の整合」は pass predicate
として型が定まっていない。(60.5) に置換すべきである。

---

## F7. ACCEPT を閉じる必要十分定理

現 spec は `N∞-swap` を「target なら」の必要方向に使い、その帰結を
用いた \(a\)-partition を target の判定に戻している。しかし、判定器の
freeze には循環がない **if and only if** を一つの theorem ID として
置くべきである。

### F7.1 提案命題 `N∞-criterion`

E-1〜E-6、すなわち

- \(f_6\) monic squarefree、\(\deg f_6=6\);
- \(\deg a=5,\ \deg p=2,\ a_5=p_2\ne0\);
- \(a^2-f_6p^2=C\in\mathbb Q^\times\);
- \((\mu)=5P_0-5P_\infty\);
- \(\gcd(a,p)=1\)

の下で、次は同値である。

\[
\boxed{
\operatorname{rootpart}(a)=[2,2,1]
\iff
\begin{array}{c}
\operatorname{Br}(\mu)=\{0,s,-s,\infty\}
\text{ for some }s^2=-C,\\
\operatorname{part}\mu^{-1}(s)
=\operatorname{part}\mu^{-1}(-s)=[2,2,1].
\end{array}}
\tag{60.6}
\]

ここで右辺は stage 2 が必要とする branch signature を述べる。monodromy
群そのものの再証明までは主張しない。

### F7.2 必要方向

target branch signature
\(\Rightarrow\) `N∞-swap`
\(\Rightarrow s^2=-C\)
\(\Rightarrow\) `N∞-red`
\(\Rightarrow\operatorname{rootpart}(a)=[2,2,1]\)。

### F7.3 十分方向

\(\operatorname{rootpart}(a)=[2,2,1]\) とし、
\(\bar{\mathbb Q}\) 上で \(s^2=-C\) を選ぶ。\(C\ne0\)、標数 0 なので
\(s^2\ne C\)。従って `N∞-1:1` と

\[
H_{\pm s}=\mp2s\,a
\]

から両 fiber の partition は \([2,2,1]\) であり、各 fiber の
ramification contribution は 2 である。

一方、divisor orientation から \(0,\infty\) の二 fiber は各々 \(e=5\)
で contribution は \(4+4\)。従って既に

\[
4+4+2+2=12
=2g(C)-2+2\deg\mu
\]

を使い切る。Riemann–Hurwitz により余分な ramification point/branch
value は存在しない。よって branch set はちょうど
\(\{0,s,-s,\infty\}\) で、有限 branch polynomial は degree 2 かつ even
である。

この十分方向は `N∞-swap` の結論を仮定していない。従って循環しない。

---

## F8. stage-2 predicate の型修理

### F8.1 E-7 は target condition と candidate precondition を分ける

§2 は E-1〜E-7 を「一つでも無ければ precondition REJECT」とする一方、
T-0 は E-1〜E-6 だけを検査し、E-7 の調和性は T-6 で計算する。これは
同じ命題を input と output の両方に置く型衝突である。

E-7 は S5-2a が定める **target condition** として残し、raw candidate
の入口は E-1〜E-6 とする。T-1 と命題 (60.6) が E-7 を導出し、
T-6 は別経路による cross-check とするのが最も小さい修理である。

もし upstream certificate として E-7 を入力する設計を選ぶなら、
その proof ID を入力 schema に追加し、T-6 不一致は必ず
`INTEGRITY_STOP` としなければならない。現稿のように
`REJECT` と `INTEGRITY_STOP` の双方を割り当ててはならない。

### F8.2 判定本線

命題 (60.6) を採れば、数学的な本線は次で閉じる。

```text
E-1..E-6 fail
    -> REJECT / precondition/*

E-1..E-6 pass, T-1 fail
    -> REJECT / a-partition-mismatch
       or REJECT / triple-root-of-a

E-1..E-6 pass, T-1 pass
    -> target branch signature is mathematically forced
```

その後の T-2〜T-7 は独立経路の整合検査である。従って T-1 が通った後に

- \(p\nmid a'\) または \(a'\not\doteq p\,d\);
- finite branch polynomial が degree 2/even でない;
- finite branch count が 2 でない;
- extra branch がある;
- RH sum が 12 でない;
- searcher/checker の actual aggregate partition が \([2,2,1]\) でない

のいずれかが出れば、紙上定理または実装の不一致であり
`INTEGRITY_STOP` である。`REJECT / branch-pair-not-harmonic` と
§3.1 直後の `INTEGRITY_STOP / swap-lemma-precondition` は同じ到達状態に
二 verdict を与えており、freeze できない。

### F8.3 T-2

T-2 は (60.5) を逐語的に使い、

```text
d := monic_gcd(a, a')
assert p divides a'
assert a' = unit * p * d
assert a'/p = unit * d
```

とする。Pell を T-0 で exact に通し、T-1 も通した後の失敗は
`INTEGRITY_STOP / pell-derivative-mismatch` でよい。単なる
`a'/p not proportional p` は必要十分な assert ではない。

### F8.4 actual partition を両経路で出す

`a_root_partition` だけでなく、searcher と checker は有限二 fiber の
`aggregate_partition` をそれぞれ独立に作り、

```text
finite aggregate partitions = [[2,2,1], [2,2,1]]
```

を sealed 内で比較すること。公開 boolean へ射影しても、元の partition
certificate は保存する。

---

## F9. searcher/checker と divisor object

### F9.1 経路分離の原理 — PASS

次の役割分離は妥当である。

- searcher: 二 chart の local differential から \(C\) 上の ramification
  divisor を作り、\(\mu\) で pushforward;
- checker: baseline multiplicity を証明した saturated elimination;
- resultant/elimination helper と local/divisor helper を共有しない;
- `N∞-swap` の結論や \(a\)-partition を両者の共通仮定にしない。

### F9.2 「同じ divisor digest」には canonical object が要る

§4 は両経路が同じ
`ramification_divisor_on_C_digest` に到達すると要求するが、次が未定義で
ある。

- 基礎体と algebraic point/prime ideal の表現;
- affine/infinity chart の重複除去;
- Galois conjugate component の束ね方;
- multiplicity の表現;
- component ordering;
- canonical serialization と hash domain separator。

同じ divisor でも number-field presentation や component order が違えば
raw bytes は異なる。従って current schema の digest equality は
数学的 divisor equality と同値でない。

freeze 前に、例えば

```text
divisor_object_schema_id
base_field_schema_id
fixed projective coordinates and chart IDs
Galois-stable prime ideals as monic reduced Groebner bases
fixed monomial order
component multiplicities and canonical ordering
canonical byte serialization
hash algorithm + domain separator
```

を規範化し、二実装がそれぞれ canonicalize すること。または raw digest
一致をやめ、第三の divisor-equality certificate を作ること。

**自己訂正**: 便 59 F13.3 で私自身が「同じ divisor digest に到達する」と
提案したが、canonical representation の型を同時に要求しなかった。
旧返信は記録として変更せず、本便でこの欠落を訂正する。

---

## F10. certificate / blindness / fixture

### F10.1 candidate-dependent digest が sealed の外に残っている

§5 は「人間可視は五欄のみ」と書く一方、

```text
fibers = [...]
ramification_divisor_on_C_digest
branch_divisor_on_P1_digest
```

を `sealed = { ... }` の外に置く。これらは candidate-dependent であり、
小さい探索宇宙では dictionary key になり得る。§5.1 の

> unkeyed artifact digest は sealed に置く

とも衝突する。

公開可能なのは

1. random opaque `candidate_ref`;
2. spec/searcher/checker の **code/artifact identity**;
3. verdict と閉じた reason code;
4. 事前承認済みの五つの数学的射影

```text
finite_branch_count
finite_branch_pair_harmonic
a_root_partition
exceptional_locus_clear
ramification_sum
```

までとする。`fibers[]`、actual branch refs、finite branch polynomial、
ramification/branch divisor の object と unkeyed digest は全て
`SEALED_INTERNAL` へ移すこと。「五欄のみ」は public envelope を除く
**数学的出力五欄**という意味に書き直す。

### F10.2 neutral negative fixtures — 設計 PASS、証拠の射程は限定

`ninfty-neg-01..08`、raw shard 名を出さない sealed mapping、genuine
candidate lane と negative-test lane の用途分離、

```text
verdict
a_root_partition
triple_gcd_degree > 0
gcd_squarefree = false
```

の四欄回帰は妥当である。申告された

\[
\operatorname{ord}_0(a)=3,\quad
\deg\gcd(a,a')=2,\quad
\deg\gcd(a,a',a'')=1
\]

は partition \([3,1,1]\) と一致し、旧「\(x=0\) に \(e=3\)」と新
`triple-root-of-a` は同じ局所機構を表す。

ただし私は raw 8 tuples や起草者の exact arithmetic を見ていない。
従って本便が紙上で受理するのは **申告された boolean 間の機構整合**まで
であり、8 件の数値計算を cross-checked と格上げしない。

negative-test runner と clean HMAC steward の役割も分け、旧 mapping を
知る tainted actor が clean steward にならないことを運用条項に加えるべき
である。

### F10.3 EP

EP を same degree/schema・non-campaign coefficients に限定し、
EP 不在中の札を

```text
partial predicate / UNKNOWN
```

とする判断は PASS。negative fixtures だけでは ACCEPT path の
end-to-end calibration にならない。freeze 後も EP が出るまでは
calibrated detector や complete search と呼んではならない。

---

## F11. provenance の残存誤り

P59-B1 は条件の列挙だけでなく出所の型も要求した。現 v2 にはまだ次の
ずれがある。

| 現記載 | 正しい出所 |
|---|---|
| §1.1 の branch type を `S5-2` | **系 S5-2a** |
| E-5 / S-4 の divisor orientation を `S5-2` | **命題 S5-1**、および正規形との同値として S5-3∞ |
| S-5 の \((5,2^21,2^21,5)\) を `S5-2` | **系 S5-2a** |
| \(\lambda=c\mu^2\) | **命題 S5-2** |

S5-2 は分解 \(\lambda=c\mu^2\) を与える命題であり、divisor と branch
passport の直接の出所ではない。§12 の「§2 入口契約を逐語」とする札も、
この行別 source map を直してからでなければ付けられない。

---

## F12. Part B の必須修理と freeze 裁定

次を versioned な再提出 blob で閉じること。

| ID | 必須修理 |
|---|---|
| **P60-B1** | `N∞-N` を (60.1) または (60.2) へ型修理し、norm/divisor pushforward の proof artifact を書く |
| **P60-B2** | `N∞-1:1` に (60.3)(60.4) を追加し、集合の単射だけでなく局所 multiplicity 一致を証明する |
| **P60-B3** | `N∞-criterion` (60.6) の必要十分定理を置き、E-7 を target condition、E-1〜E-6 を raw candidate precondition と型分離する |
| **P60-B4** | T-2 を \(d=\gcd(a,a')\)、\(a'\doteq pd\)、\(a'/p\doteq d\) に置換する |
| **P60-B5** | T-1 通過後の T-2〜T-7 を cross-check lane とし、`REJECT` / `INTEGRITY_STOP` の到達状態を一意化する。actual finite partitions も両経路で比較する |
| **P60-B6** | ramification/branch divisor の canonical object schema、または独立 equality certificate を定義する |
| **P60-B7** | `fibers[]` と candidate-dependent divisor digests を `SEALED_INTERNAL` に移し、public envelope + 五数学欄を明記する |
| **P60-B8** | S5-1/S5-2/S5-2a/S5-3∞ の provenance を F11 の型へ直し、negative lane / clean steward の役割分離を加える |

従って current SHA

```text
813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
```

は **監査対象 draft v2 の digest** であって freeze digest ではない。

```text
predicate_spec_freeze_id = NOT ISSUED
implementation_status    = NOT AUTHORIZED
model_builder status     = LOCKED
```

修理版は新 version・新 full SHA-256 で再提出し、

```text
supersedes_draft = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected
    = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
```

を receipt に束縛すること。ID 名や event ID は次回 PASS 前に先取りして
発行しない。

---

## F13. 共同設計者としての発案

### F13.1 `N∞-pair` を `N∞-swap` より先に置く

任意の Pell tuple に対し、\(\bar{\mathbb Q}\) 上で \(s^2=-C\) を選べば

\[
H_{\pm s}=\mp2s\,a
\]

は target を仮定せず成立する。これを

> **Lemma `N∞-pair`.** \(s^2=-C\) なら二 fiber は non-fixed で、
> その partition はともに \(\operatorname{rootpart}(a)\)。

として独立させると、

- `N∞-pair`: candidate から canonical harmonic pair を構成する十分側;
- `N∞-swap`: target の有限 pair がその canonical pair 以外でないことを
  示す必要側;
- `N∞-criterion`: 両者と RH を束ねる iff

という三段になり、proof dependency が一方向になる。

### F13.2 decision lane と audit lane を分ける

```text
decision lane:
    E-1..E-6 + rootpart(a)

audit lane A:
    local differential -> R -> mu_*R

audit lane B:
    saturated elimination -> R/B
```

とし、decision lane の ACCEPT 後に A/B が theorem-predicted invariant と
一致しなければ integrity stop とする。これなら elimination bug が
candidate の数学的 REJECT に偽装されない。

### F13.3 divisor bytes でなく二層 ID を凍結する

freeze ID を

```text
predicate theorem ID/digest
divisor object schema ID/digest
public certificate schema ID/digest
sealed payload schema ID/digest
reason-code enum ID/digest
```

の束として発行する。predicate だけを freeze して serializer を後から
変えると、同一 divisor の digest が実装版ごとに変わり、receipt の比較
可能性を失う。

---

## F14. ★教材

1. **norm の divisor 等式では zero divisor と principal divisor を分ける。**  
   \((H_v)_0=\pi_*[\mu^{-1}(v)]\) は正しいが、
   \(\operatorname{div}(H_v)\) には \(-5[\infty]\) がある。

2. **集合の単射は multiplicity partition の一致をまだ証明しない。**  
   projection が unramified で norm の他方の因子が単元、という二点を
   局所位数で書く必要がある。

3. **必要補題を checker に使うときは、十分方向を別に証明する。**  
   `target -> swap -> a-partition` だけでは判定器にならない。
   `a-partition -> target` を RH で閉じて初めて ACCEPT iff になる。

4. **定理で強制される再計算の不一致は candidate REJECT ではない。**  
   正しい candidate を実装事故で落とさないため `INTEGRITY_STOP` とする。

5. **同じ数学 object と同じ digest は別の主張である。**  
   canonical serialization が無ければ、同じ divisor から異なる bytes が
   出る。

6. **explicit catch-all と default fallback は反対物である。**  
   前者は全域を列挙する規則、後者は欠落を黙って救う規則である。

7. **公開五欄とは public envelope を除く五つの数学的射影である。**  
   fiber decomposition や candidate-dependent digest を同じ可視域へ置くと、
   hash 非開示規律を裏口から破る。

---

## F15. 監査範囲外申告

### 本便で行ったこと

- 委嘱、対話帳、対象二文書を全文読解;
- SHA-256、LF 行数、CR/TAB/C0、二つの scope lint の独立照合;
- P59-A1–A4 の typed edge/object/inventory/\(b\)-semantics 差分監査;
- `N∞-N`、`N∞-1:1`、`N∞-fix`、`N∞-swap`、`N∞-red`、
  `N∞-div` の紙上再導出;
- S5-1/S5-2/S5-2a/S5-3∞ との provenance 突合;
- predicate、reason-state、certificate visibility、二経路の型監査。

### 本便で行っていないこと

- Part A の final artifact、migration record、\(\forall n\) proof artifact、
  event receipt はまだ存在しないため、その実 digest/適用結果は未監査;
- status/CLAIMS/BFC/Rule 1/manifest の実際の event diff は未監査;
- sealed 8 tuples の raw coefficients と boolean 計算は未閲覧・未再計算;
- EP は未提示なので end-to-end positive calibration は未監査;
- searcher/checker は未実装なので独立計算は未監査;
- GAP、Lean、外部文献は使用していない。従って本便は
  `paper audit` であり、いずれの新補題も Lean `verified` とは呼ばない。

