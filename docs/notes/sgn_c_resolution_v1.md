# FINDING SGN-ĉ の解決 — 予測 $+1$ と実測 $-1$ はどちらが正しいか(v1)

**状態札: candidate(裁定前・未 commit)**
起草: 数学者(Opus 5)/ 2026-07-29 ・ 裁定 158(委嘱)
正典: `docs/week1-定義ノート.md`(§3 の $\psi_n$、L189 の Thm 4.3)
監査対象: `docs/notes/oddH_full_proof_v1.md` §11.1–11.2 / `docs/notes/phifam_v1.md` §4 FINDING Φ1(予測式)、`search/ihc-fixture-v2.g` + `search/certs/ihc_fixture_v2_20260729.json`(測定系)

**状態札の内訳**

| 内容 | 札 |
|---|---|
| §2(第一原理の導出)・§3(予測式の再演)・§4(規約辞書と符号差の同定) | **紙上証明**(paper-proof)。Lean の意味の verified ではない |
| §6 の機械検算(GAP・全 $n\in\{3,5,7,9,11\}$、全 $k$) | **cross-checked**(手計算と GAP の二系統一致) |
| §7 修理仕様・§8 カナリア強化仕様 | 提案(実装前) |

**記法注**: 本稿の $u$ は正典 Thm 4.3 / oddH §11.1 の $u:=2m+1$(GT-shadow のパラメータ)である。**封印対象の $u$・平方類・$\widehat c_\mu$ には一切触れていない。**

---

## 0. 判定(結論先出し)

> **(ii) が正しい。測定経路に符号差がある。予測式 $\bigl((1-2k)e_1\bigr)q_3$ に疵はない。**

不一致の座標を一点に特定した:

> **fixture の分解手続き `v := conj * Inverse(q)`(GAP の生の積)は、規約 W-4 の下では紙面の $q^{-1}\!\cdot\!\mathrm{conj}$ を計算している。したがって得られる三つ組は「紙面正規形 $\mathrm{conj}=a\cdot q$ の $a$」ではなく「$\mathrm{conj}=q\cdot a'$ の $a'$」である。両者は $a'=q\cdot a$(= $q$ の $A$ 上の線形作用)で結ばれ、$q=q_3=\mathrm{diag}(-1,-1,+1)$ ゆえ**
> $$(\mathrm{dv}_1,\mathrm{dv}_2,\mathrm{dv}_3)_{\text{fixture}}=(-\mathrm{dv}_1,\,-\mathrm{dv}_2,\,+\mathrm{dv}_3)_{\text{paper}} .$$
> **本件は $\mathrm{dv}_2=\mathrm{dv}_3=0$ なので、ちょうど $\mathrm{dv}_1$ の符号だけが反転して見えた。**

$k=0$ で予測 $\mathrm{dv}_1^{\text{paper}}=1-2\cdot0=+1$、よって fixture の報告値は $-1\equiv n-1$ — **全奇数窓で一貫して $n-1$ が出たのはこの通りの帰結**であり、真の不一致ではない。erratum は oddH / phifam ではなく **fixture(測定系)側**に要る。

**副次の疵(独立の第二点)**: v2 の修理 (1)「$h=g^{-1}$」も前提が逆である。規約 W-4 の下では GAP の `X^g` はすでに**紙面の $\mathrm{inn}(g)(X)=gXg^{-1}$** であって $g^{-1}Xg$ ではない(§4.2)。したがって v2 が `nativeG` と呼んでいる元こそが紙面の conjugator $h$ であり、`paperG := nativeG^-1` は逆向きの補正である。**本件では $h$ が対合なので無害**だが、対合でない conjugator($m=0$ 族の $\mathrm{inn}(a_1^{-2k})$、$k\ne0$)では誤る — §6 の対照実験で機械確認した。

---

## 1. 記法(正典からの座標)

$G_n=A\rtimes Q$、$A=\bigoplus_{i=1}^3(\mathbf Z/n)e_i$($e_i\leftrightarrow a_i$)、$Q=\{1,q_1,q_2,q_3\}\cong C_2^2$、
$$q_1=\mathrm{diag}(+,-,-),\quad q_2=\mathrm{diag}(-,+,-),\quad q_3=\mathrm{diag}(-,-,+)\quad(\text{$A$ 上の作用})$$
(oddH 補題 A)。元は**紙面正規形** $(a,q)\leftrightarrow a\cdot q$ で書く。積と逆元は
$$(a,q)(b,p)=(a+q\!\cdot\!b,\;qp),\qquad (a,q)^{-1}=(-q\!\cdot\!a,\;q)\quad(q^2=1).$$
$X=(e_1,q_1)$、$Y=(e_1+e_2+e_3,\,q_2)$、$\operatorname{ord}X=\operatorname{ord}Y=2n$。

> **補題 0(内部自己同型の閉形式).** 紙面規約 $\mathrm{inn}(h)(w)=hwh^{-1}$ の下で、$h=(v,q)$ に対し
> $$\boxed{\ \mathrm{inn}\bigl((v,q)\bigr)\,(a,p)=\bigl(q\!\cdot\!a+(1-p)v,\ p\bigr)\ }$$

**証明.** $(v,q)(a,p)=(v+q\!\cdot\!a,\,qp)$、これに $(v,q)^{-1}=(-q\!\cdot\!v,q)$ を右から掛けて
$(v+q\!\cdot\!a+(qp)\!\cdot\!(-q\!\cdot\!v),\,qpq)=\bigl(v+q\!\cdot\!a-p\!\cdot\!v,\;p\bigr)$($Q$ 可換・$q^2=1$)。∎

(参考・対比用)GAP 流の向き $\mathrm{conj}_g(w)=g^{-1}wg$ の閉形式は $\bigl(q\!\cdot\!a+q(p-1)v,\;p\bigr)$。**$h=(v,q)$ が対合ならこの二つは一致する**(下の補題 1)。

---

## 2. 第一原理からの導出($\widehat c=[2n-1,1]$)

### 2.1 $\Phi$ の像

$m=2n-1$、$u=2m+1=4n-1$、$f=1$(恒等コセット)。$u\equiv-1\pmod{2n}$ かつ $\operatorname{ord}X=\operatorname{ord}Y=2n$ なので
$$\Phi(X)=X^u=X^{-1},\qquad \Phi(Y)=Y^u=Y^{-1}$$
— **$\widehat c$ は marked 生成系上の「反転写像」である**。座標で書けば($u$ 奇より)
$$X^{u}=(u\,e_1)q_1=(-e_1)q_1,\qquad Y^{u}=(e_1+u\,e_2+e_3)q_2=(e_1-e_2+e_3)q_2\quad(u\equiv-1\bmod n).$$
($X^{2t}=2te_1$, $X^{2t+1}=((2t+1)e_1)q_1$;$Y^{2t}=2te_2$, $Y^{2t+1}=(e_1+(2t+1)e_2+e_3)q_2$ — 補題 A(3) の直接計算。)

### 2.2 $h$ を解く

$\Phi|_A=\mathrm{diag}(u,u,(-1)^mu)$(oddH §11.1)に $u\equiv-1$、$m$ 奇を入れると $\Phi|_A=\mathrm{diag}(-1,-1,+1)=q_3$。補題 0 より $\mathrm{inn}((v,q))|_A=q$ だから、**$q=q_3$ が強制される**(他の $q$ は $A$ 上の作用が合わない)。$v=(v_1,v_2,v_3)$ として:

* **$X$ の条件**: $q_3\!\cdot\!e_1+(1-q_1)v=-e_1$。$1-q_1=\mathrm{diag}(0,2,2)$ ゆえ $(-1,\,2v_2,\,2v_3)=(-1,0,0)$、**$n$ 奇より $v_2=v_3=0$**。
* **$Y$ の条件**: $q_3\!\cdot\!(e_1+e_2+e_3)+(1-q_2)v=(1,-1,1)$。$q_3\!\cdot\!(1,1,1)=(-1,-1,1)$、$1-q_2=\mathrm{diag}(2,0,2)$、$v_3=0$ ゆえ左辺 $=(-1+2v_1,\,-1,\,1)$。したがって $2v_1=2$、**$n$ 奇より $v_1=+1$**。

$$\boxed{\ h=(e_1,q_3)=a_1q_3\quad(\text{紙面正規形});\qquad \mathrm{dv}_1=+1\ }$$

$X,Y$ が $G_n$ を生成するので $h$ は一意 —(より正確には $Z(G_n)$ を法として一意で、$n$ 奇のとき $Z(G_n)=1$:$(a,q)$ が中心なら $q$ が $A$ 上自明ゆえ $q=1$、$a$ が $q_1,q_2$ で不変ゆえ $2a=0$、$a=0$)。

### 2.3 $n=3$ の $D_3^3$ 内での手計算(委嘱指定)

$h=a_1q_3=(r,1,1)(s,s,1)=(rs,\,s,\,1)$。$X=(r,s,s)$、$Y=(rs,r,rs)$、$srs^{-1}=r^{-1}$。

| | 第 1 座標 | 第 2 座標 | 第 3 座標 |
|---|---|---|---|
| $hXh^{-1}$ | $(rs)r(rs)^{-1}=r(srs^{-1})r^{-1}=r^{-1}$ | $s\,s\,s^{-1}=s$ | $1\cdot s\cdot1=s$ |
| $X^{-1}$ | $r^{-1}$ | $s$ | $s$ |
| $hYh^{-1}$ | $(rs)(rs)(rs)^{-1}=rs$ | $s\,r\,s^{-1}=r^{-1}$ | $1\cdot rs\cdot 1=rs$ |
| $Y^{-1}$ | $(rs)^{-1}=rs$ | $r^{-1}$ | $(rs)^{-1}=rs$ |

**一致。** 一方 $h'=a_1^{-1}q_3=(r^{-1}s,\,s,\,1)$ では第 1 座標が
$$(r^{-1}s)(rs)(r^{-1}s)^{-1}=(r^{-1}s)(rs)(sr)=r^{-1}s\,r\,s^2r=r^{-1}(sr)r=r^{-1}(r^{-1}s)r=r^{-2}(sr)=r^{-3}s\ \overset{n=3}{=}\ s\ \ne\ rs=\bigl(Y^{-1}\bigr)_{(1)} .$$
**$a_1^{-1}q_3$ は $\Phi$ を実現しない。** すなわち紙面正規形での係数は $+1$ であって $-1$ ではない。

### 2.4 「$g$ は鏡映か」「対合性と $\mathrm{dv}_1$ の関係」(委嘱の設問)

$h=(rs,s,1)$ は 3 座標のうち 2 座標が $D_n$ の鏡映・1 座標が恒等。より構造的には:

> **補題 1.** $(v,q_3)^2=\bigl((1-q_3)^{-}\text{の寄与}\bigr)$ を計算すると $(v+q_3\!\cdot\!v,\,1)=(0,0,2v_3)$。ゆえに
> $$\bigl((v)q_3\bigr)^2=1\iff v_3=0 .$$

**$v_1$ には何の条件もつかない。** これが重要である:**対合性テストは $\mathrm{dv}_1$ の符号に対して完全に盲目**であり、しかもその理由(「$q_3$ が $e_1$ を反転する」)は、§0 の規約差が $\mathrm{dv}_1$ を反転させる理由と**同一**である。したがって $g=g^{-1}$ から「規約変換では符号が説明できない」と結論するのは論理の飛躍だった — 対合性が消しているのは $g\leftrightarrow g^{-1}$ の軸だけで、$a\cdot q\leftrightarrow q\cdot a$ の軸は消していない(§5)。

なお $h$ が対合であるため、補題 0 の二つの向き($hwh^{-1}$ と $h^{-1}wh$)は**この場合に限り**同じ元を与える。

---

## 3. oddH §11.2 / phifam の $(1-2k)$ の再演 — 予測式は正しい

一般の $f$(Thm 4.3: $F=(2k,-2k,\varkappa(m))$、$\varkappa(m)=m+1$($m$ 奇)ゆえ $\varkappa(2n-1)=2n\equiv0\bmod n$、すなわち $F=(2k,-2k,0)$)について:

1. $F^{-1}Y^uF$:$A$ の元による共役は補題 0 で $q=1$ の場合、$\bigl(a+(q_2-1)F,\;q_2\bigr)$。$q_2-1=\mathrm{diag}(-2,0,-2)$ ゆえ
 $$F^{-1}Y^uF=(1-2F_1,\;u,\;1-2F_3)\,q_2=(1-4k,\;-1,\;1)\,q_2\pmod n .$$
 (oddH §11.1 の式 — 再導出して一致。)
2. $\Phi|_A=q_3$ は $k$ に依らない($F$ は $A$ の元なので $A$ 上の作用に寄与しない)ゆえ $q=q_3$。
3. $X$ の条件は $k$ を含まないので前と同じく $v_2=v_3=0$。
4. $Y$ の条件: $(-1+2v_1,\,-1,\,1)=(1-4k,\,-1,\,1)$、すなわち $2v_1=2-4k$、**$n$ 奇より** $v_1=1-2k$。

$$\boxed{\ \Phi_{2n-1,f}=\mathrm{inn}\bigl(((1-2k)e_1)\,q_3\bigr)\ }$$

**`phifam_v1.md` L77 / L131 の予測式は、紙面正規形 $a\cdot q$・紙面 $\mathrm{inn}$ 規約の下で厳密に正しい。$k$ の扱いにも $\varkappa$ の扱いにも符号疵はない。** $k=0$ で係数 $+1$。

> **付随して確認**: `phifam_v1.md` §6 の独立実装(node)の実測行「$m=17$ の conjugator = $((1)e_1)q_3,((2)e_1)q_3,\dots$」は**紙面正規形で報告されており正しい**。すなわち node 実装と GAP fixture は**同じ元を別の正規形で報告していた** — 二系統は矛盾していない。

---

## 4. 測定経路の突合 — 符号差の座標

### 4.1 規約 W-4 の辞書

`search/week3-battery-common.g` L46–54:

```gap
# abstract product "f1 f2 ... fk" (paper notation, left to right) -> GAP form (reversal convention)
AbstractProd := function(list) ... for i in [Length(list), Length(list)-1 .. 1] do val := val * list[i]; od; ...
```

すなわち置換群 $P$(GAP の生の積 `*`)と紙面群 $G_n$ の対応は
$$\boxed{\ w_1*_{\rm raw}w_2=w_2\cdot_{\rm paper}w_1\ }\tag{W}$$
— $P$ は $G_n$ の**反対群**であり、生成元のラベルだけが共通である。(検算: $\psi_n(y)$ の第 1 座標は紙面で "$rs$"、`MakeGn` はこれを `tr(s*r,1)` で作る。)

### 4.2 帰結 1 — GAP の `^` は紙面の $\mathrm{inn}$ である

(W) を 2 回使うと $a*_{\rm raw}b*_{\rm raw}c=c\cdot b\cdot a$。よって
$$\texttt{X\^{}g}\ =\ g^{-1}*_{\rm raw}X*_{\rm raw}g\ =\ g\cdot X\cdot g^{-1}\ =\ \mathrm{inn}_{\rm paper}(g)(X).$$
恒等式として `X^g = AbstractProd([g, X, g^-1])`(§6 で機械確認: 全 $n$ で `true`)。

> したがって `ihc-fixture-v2.g` L183–187 のブルートフォース探索は、**すでに紙面の方程式 $\mathrm{inn}(g)(X)=X^u$ を解いている**。v2 冒頭のコメント(L7–8)と `notation_note` の「native_conjugator = GAP規約 $X^g=g^{-1}Xg$」は、$G_n$ の元としての意味を取り違えている。`paperG := nativeG^-1`(L199)は不要かつ逆向き。**本件は $g$ が対合ゆえ無害。**

### 4.3 帰結 2 — 分解の向き(これが SGN-ĉ の正体)

`DecomposeConjugator`(L84):`v := conj * Inverse(qp[2])`。(W) より
$$\mathrm{conj}*_{\rm raw}q^{-1}=q^{-1}\cdot_{\rm paper}\mathrm{conj}.$$
これが $A$ の元 $a'$ に等しいという判定は、紙面で
$$\mathrm{conj}=q\cdot a'\qquad(\text{$a$ が }q\text{ の }\textbf{左})$$
を意味する。一方 oddH / phifam の予測は紙面正規形 $\mathrm{conj}=a\cdot q$($a$ が $q$ の**右**)で書かれている。両者を等置すると
$$a\cdot q=q\cdot a'\iff a'=q^{-1}aq=q\!\cdot\!a\quad(\text{$q$ の $A$ 上の線形作用}),$$
$$\boxed{\ q=q_3:\quad (a'_1,a'_2,a'_3)=(-a_1,\,-a_2,\,+a_3)\ }$$

$k=0$:予測 $a=(1,0,0)$ ⟹ fixture は $a'=(-1,0,0)=(n-1,0,0)$ を報告する。**実測と逐語一致**($n=3,5,7,9,11$ すべて)。

$q$ ラベルは影響を受けない($A\trianglelefteq G_n$ ゆえ $\pi(\mathrm{conj})$ は左右いずれの正規形でも同じ)。

### 4.4 一般 $k$ での照合(より強い証拠)

予測 $a=((1-2k),0,0)$ に対し fixture 流の報告値は $-(1-2k)=2k-1$。§6 の機械検算は $n=3,5,7,9$・全 $k$ でこの**関数関係**を再現した(単に $\pm1$ が一致するだけでなく、$k$ を動かしたときの値の対応が完全に付く)。$k=(n+1)/2$($1-2k\equiv0$)では両者が一致 — 反転の不動点であり、これも観測と合う。

---

## 5. なぜ「規約ドリフトのカナリア」が自分の規約ドリフトを検出できなかったか

設計上の教訓として記録する。この fixture は 3 つの独立な「向きの軸」を持つ:

| 軸 | 内容 | v2 が検査したもの | 本件で効いた軸 |
|---|---|---|---|
| (A) | $g$ か $g^{-1}$ か(共役の向き) | ○(`discrimination` で 3 分類) | **効かない**($g$ が対合) |
| (B) | $a\cdot q$ か $q\cdot a$ か(正規形の向き) | **×(未検査)** | **これ** |
| (C) | 語の積の向き($\texttt{*}$ vs `AbstractProd`) | 部分的(生成元構成のみ) | (B) の原因 |

v2 は (A) を厳密化したが (B) を素通りした。さらに悪いことに、**(A) と (B) は本件では同じ症状(`dv1` だけの符号反転)を出す**ため、`discrimination` の分類 `dv1_negated_only` が「(A) の規約変換で説明がつく」と読めてしまう構造になっていた。実際にはこの症状は (B) 由来であり、(A) は対合性ゆえ何も起こしていない。

さらに `dv1_negated_only` という分類名自体が誤導的である。(B) の真の規則は $(-,-,+)$ であって「$\mathrm{dv}_1$ のみ反転」ではない。$\mathrm{dv}_2\ne0$ の conjugator が来れば同じ (B) が `irregular_pattern` に落ちる。

---

## 6. 機械検算(GAP 4.16.0・二系統一致)

スクリプト(未 commit・診断用): `C:\Users\81905\Desktop\shadow-atelier\search\sgnc-diag-1.g`(sha256 `f74575b2ec7c5249587067fd747f5eafcd6159f91942eefefd8361ae10706412`)、`C:\Users\81905\Desktop\shadow-atelier\search\sgnc-diag-2.g`(sha256 `43fff69795b538e9379ae5b08dd468fbedb5960170dc452443ba47f766dd832a`)。いずれも自己完結(プロジェクトの lib を `Read` せず、`AbstractProd` は逐語コピー)。

### 6.1 `sgnc-diag-1.g`(fixture と同一の $\widehat c$ 設定)

```
n | rawdec(fixture: g = a^raw * q)  | paperNF(g = a .paper q) | g=paper a1*q3? | g=paper a1^-1*q3? | involution
3 | (2,0,0)*q3 | (1,0,0).q3 | true | false | g^2=1: true
    paper inn(a1 q3) realises Phi: true   |  paper inn(a1^(n-1) q3) realises Phi: false   |  paper h^-1 X h with h=a1q3: true
    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): true
5 | (4,0,0)*q3 | (1,0,0).q3 | true | false | g^2=1: true
    paper inn(a1 q3) realises Phi: true   |  paper inn(a1^(n-1) q3) realises Phi: false   |  paper h^-1 X h with h=a1q3: true
    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): true
7 | (6,0,0)*q3 | (1,0,0).q3 | true | false | g^2=1: true
    paper inn(a1 q3) realises Phi: true   |  paper inn(a1^(n-1) q3) realises Phi: false   |  paper h^-1 X h with h=a1q3: true
    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): true
9 | (8,0,0)*q3 | (1,0,0).q3 | true | false | g^2=1: true
    paper inn(a1 q3) realises Phi: true   |  paper inn(a1^(n-1) q3) realises Phi: false   |  paper h^-1 X h with h=a1q3: true
    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): true
11 | (10,0,0)*q3 | (1,0,0).q3 | true | false | g^2=1: true
    paper inn(a1 q3) realises Phi: true   |  paper inn(a1^(n-1) q3) realises Phi: false   |  paper h^-1 X h with h=a1q3: true
    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): true

-- control: non-involutive conjugator, does native/paper distinction bite? --
n=5 k=1: native g = h ? true   native g = h^-1 ? false   (h involution? false)
n=5 k=2: native g = h ? true   native g = h^-1 ? false   (h involution? false)
n=9 k=1: native g = h ? true   native g = h^-1 ? false   (h involution? false)
n=9 k=2: native g = h ? true   native g = h^-1 ? false   (h involution? false)
```

読み方:
* 第 1 列 = fixture の分解手続きの再現(実測 `(n-1,0,0)*q3` を再現 — 証明書と一致)。第 2 列 = 紙面正規形での同じ元の分解 = **$(1,0,0)$**。**同一の元の二つのラベル**である。
* 「$g$ = 紙面 $a_1q_3$?」= `true`、「$g$ = 紙面 $a_1^{-1}q_3$?」= `false` — §2.3 の手計算と一致。
* **対照実験**(非対合 conjugator $h=a_1^{-2k}$、$m=0$ 族):GAP の native 探索が返すのは $h$ であって $h^{-1}$ ではない。**v2 の `paperG := nativeG^-1` は誤り**(本件では無害)。

### 6.2 `sgnc-diag-2.g`(一般 $k$・予測式 $(1-2k)$ の直接検査)

$n=3,5,7,9$、全 $k\in\{0,\dots,n-1\}$ で `inn_paper(((1-2k)e1)q3) = Phi_{2n-1,f}` が **ALL k PASS: true**。抜粋($n=9$):

```
n = 9
  k=0 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(1,0,0)   fixture-raw=(8,0,0)   [(1-2k) mod n = 1 , -(1-2k) mod n = 8]
  k=1 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(8,0,0)   fixture-raw=(1,0,0)   [(1-2k) mod n = 8 , -(1-2k) mod n = 1]
  k=2 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(6,0,0)   fixture-raw=(3,0,0)   [(1-2k) mod n = 6 , -(1-2k) mod n = 3]
  k=3 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(4,0,0)   fixture-raw=(5,0,0)   [(1-2k) mod n = 4 , -(1-2k) mod n = 5]
  k=4 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(2,0,0)   fixture-raw=(7,0,0)   [(1-2k) mod n = 2 , -(1-2k) mod n = 7]
  k=5 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(0,0,0)   fixture-raw=(0,0,0)   [(1-2k) mod n = 0 , -(1-2k) mod n = 0]
  k=6 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(7,0,0)   fixture-raw=(2,0,0)   [(1-2k) mod n = 7 , -(1-2k) mod n = 2]
  k=7 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(5,0,0)   fixture-raw=(4,0,0)   [(1-2k) mod n = 5 , -(1-2k) mod n = 4]
  k=8 : inn_paper(((1-2k)e1)q3)=Phi ? true   paperNF=(3,0,0)   fixture-raw=(6,0,0)   [(1-2k) mod n = 3 , -(1-2k) mod n = 6]
  ALL k PASS: true
```

`paperNF` 列は常に $(1-2k)\bmod n$、`fixture-raw` 列は常に $-(1-2k)\bmod n$ — §4.3 の $(-,-,+)$ 規則の $k$ 依存まで含めた確認。

---

## 7. 修理仕様(実装者向け・`search/ihc-fixture-v3.g` として。v2 は不変)

1. **分解の向きを紙面正規形に揃える(本丸)**。`DecomposeConjugator` L84 を
 ```gap
 v := AbstractProd([conj, Inverse(qp[2])]);   # = 紙面 conj . q^-1 (生の GAP では Inverse(q) * conj)
 ```
 に置換する。これは oddH §11.4 の lint 規則 4「**paper 由来の式を GAP で書くときは必ず `AbstractProd` を通す**」の直接適用であり、同じ規則が k9-package L221 の F10 バグも捕まえる。修理後の期待値は全 $n$ で `paper_decomp = (1,0,0)*q3`、`matches_predicted_form_exact = true`。
2. **`paperG := nativeG^-1` を撤去**(L199)。規約 W-4 の下では GAP の `^` がすでに紙面 $\mathrm{inn}$ である(§4.2)。「native / paper conjugator」という二欄立て自体が phantom なので、欄名を **`conjugator`(紙面 $\mathrm{inn}(h)$ を満たす $h$)一本**に改め、`notation_note` を書き換える。
3. **`discrimination` の 3 分類を差し替える**。現行の `dv1_negated_only` は (A) 軸の分類名だが本件で効いたのは (B) 軸である。新分類は「紙面 NF と生 GAP NF の差」を $(a'=q\!\cdot\!a)$ の**規則そのもの**として assert する:$q=q_3$ なら $(-,-,+)$、$q=q_1$ なら $(+,-,-)$、$q=q_2$ なら $(-,+,-)$。規則から外れたら `irregular`。
4. **証明書に規約欄を立てる**:`"normal_form": "a·q (paper)"`、`"inn_convention": "inn(h)X = h X h^-1"`、`"product_convention": "W-4 (AbstractProd = reversed GAP product)"` を機械可読フィールドとして持たせる。**規約は文章の註ではなくフィールドにする**(本件はまさに註が読み違えられた事故)。

## 8. カナリア強化仕様(3 軸を分離して検出できるようにする)

現行の $\widehat c$ 単独($k=0$・$\mathrm{dv}_2=\mathrm{dv}_3=0$・$h$ 対合)は 3 軸のいずれに対しても縮退している。次の 3 本を追加すれば軸ごとに切り分く:

| 追加 fixture | 検出する軸 | 縮退が解ける理由 |
|---|---|---|
| $m=2n-1$、$k\ge2$($f=a_1^{2k}a_2^{-2k}$) | (B) 正規形 | $\mathrm{dv}_1=1-2k\ne\pm1$ なので符号反転が値として区別可能($k\ne(n+1)/2$) |
| $m=0$、$k\ne0$(conjugator $a_1^{-2k}$) | (A) 共役の向き | $h$ が**非対合**($h^{-1}=a_1^{2k}\ne h$) |
| $\mathrm{dv}_2\ne0$ となる conjugator(例:$q_1$ または $q_2$ ラベルの内部元) | (B) の**規則の形** | 「$\mathrm{dv}_1$ のみ反転」でなく $(-,-,+)$ であることが見える |

---

## 9. FINDING

| # | 種別 | 箇所 | 内容 |
|---|---|---|---|
| **S1** | **測定系の疵(確定)** | `search/ihc-fixture-v2.g` L84 `DecomposeConjugator` | 分解を生の GAP 積で行うため、報告される三つ組は紙面正規形 $a\cdot q$ の $a$ ではなく $q\cdot a'$ の $a'$。$a'=q\!\cdot\!a$、$q=q_3$ で $(-,-,+)$。**FINDING SGN-ĉ の全体がこれで説明される。** 予測式に疵はない |
| **S2** | **測定系の疵(独立・本件では無害)** | 同 L7–8, L199, `notation_note` | 規約 W-4 の下では GAP の `X^g` は**紙面の $gXg^{-1}$**。「native = $g^{-1}Xg$」は誤読で、`paperG := nativeG^-1` は逆向きの補正。$h$ が対合ゆえ本件は無傷だが、非対合 conjugator では誤る(§6.1 対照実験) |
| **S3** | **証明書の記述に偽の主張** | `search/certs/ihc_fixture_v2_20260729.json` `notation_note` | 「変換式は $g^{-1}Xg=hXh^{-1}$ より $h=g^{-1}$」は W-4 の下で偽。値そのもの(`native_*`/`paper_*` の 5 行)は**正しい元を報告している**が、ラベルの意味づけが誤り。上書きせず v3 で訂正(oddH ODD-H-4 と同じ扱い) |
| **S4** | **正しさの確認(予測側)** | `phifam_v1.md` L77/L131, `oddH §11.1–11.2` | $\Phi_{2n-1,f}=\mathrm{inn}(((1-2k)e_1)q_3)$、$\Phi|_A=\mathrm{diag}(u,u,(-1)^mu)$、$F^{-1}Y^uF=(1-2F_1,u,1-2F_3)q_2$ を第一原理から再導出し、全て正しいことを確認。**erratum 不要** |
| **S5** | **二系統は矛盾していなかった** | `phifam_v1.md` §6(node 実装) | node 実装の「$m=17$ conjugator $=((1)e_1)q_3$」と GAP の `(n-1,0,0)*q3` は**同一の元の別ラベル**。node 側が紙面正規形、GAP 側が生 GAP 正規形。cross-check の突合は「元」でなく「ラベル」で行われていたため衝突に見えた |
| **S6** | **カナリアの設計上の縮退** | fixture 全体 | $\widehat c$ 単独では 3 つの向きの軸((A) $g/g^{-1}$、(B) $a\cdot q/q\cdot a$、(C) 語の積)が全て縮退または不可視。とくに**対合性 $g^2=1$ は $\mathrm{dv}_1$ の符号に対して原理的に盲目**(補題 1)— この盲目性の原因($q_3$ が $e_1$ を反転する)は、(B) が $\mathrm{dv}_1$ を反転させる原因と同一。§8 の 3 本追加を推奨 |

---

## 10. 未閉鎖項・射程

* 【SGN-1】本稿は**紙上証明 + GAP 二系統一致**。**Lean の意味の verified ではない。** 内容は有限群 $(\mathbf Z/n)^3\rtimes C_2^2$ の等式のみなので Lean 化候補としては素直(ODD-H-1 と同じ層)。
* 【SGN-2】爆風半径の確認: 同型の分解パターン(`conj * Inverse(q)` を紙面正規形と読む)を持つのは `search/ihc-fixture.g`(v1・L158)と `search/ihc-fixture-v2.g`(L84)の **2 か所のみ**(`grep` 済み)。**両者とも $\widehat c$ fixture であり、下流の数学的主張には接続していない**(この fixture は較正専用)。ただし v1 の証明書 `ihc_fixture_20260728.json` も同じラベル誤りを含む。
* 【SGN-3】§8 の 3 本のうち $m=0$ 族は $[0,f]$ が GT-shadow であることの確認が要る(Thm 4.3 で $m=0\in\mathcal X_n$ は $\gcd(1,K_{\rm ord})=1$ より自明・$f$ の族は $F=(2k,-2k,0)$)。実装前に $\mathcal X_n$ 所属の assert を入れること。
* 【SGN-4】本稿は $\widehat c=[2n-1,1]$ の**内部実現**のみを扱った。$\widehat c$ の GT-群としての性質(位数 2・$\widetilde\chi_{2M}$ 値 $-1$・複素共役との対応)には触れていない — それらは `phifam_v1.md` §4 の管轄で、本件の符号差の影響を受けない($\Phi|_A$ も $\mathrm{Out}$ 像の位数も conjugator のラベルに依存しない)。
* 【SGN-5】**規約辞書 (W) を独立文書に昇格させることを提案する**。現状 W-4 は `week3-battery-common.g` の 1 行コメントと定義ノート §1.5.1 に散在し、「$\texttt{*}$ の向き」は書かれているが「**$\texttt{\^{}}$ の向き**」と「**正規形 $a\cdot q$ の向き**」は明文化されていない。本件は後者 2 つで起きた。§4.1–4.3 の 3 つの boxed 式が最小の辞書である。
