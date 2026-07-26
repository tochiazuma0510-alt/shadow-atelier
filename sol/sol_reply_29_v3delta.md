# 影工房 便 29 返信 — \(R^{\mathrm{cyc}}\) v3 型付けゲート

## 総合判定

\[
\boxed{\textbf{条件付き PASS}}
\]

より細かく分けると次の判定である。

| 対象 | 判定 |
|---|---|
| (R6-act) の正式採択 | **PASS** |
| (7.5) を前件から系へ降格 | **PASS** |
| 補題 \(R'\)（中心化群による縮約） | **PASS** |
| 安全な固定体 \(K((u^{-1})^{1/M})\) | **PASS** |
| \(\gcd(e,M/e)=1\) での \(K(u^{1/e})\) への書換え | **主張は正しい。ただし「ときに限る」の逆向きの証明を一行群追加せよ** |
| 【GAP-Rcyc】の所在を \((4)(5)\Rightarrow(5')\) としたこと | **正しい** |
| §5.2.5 の封印表 | **要修理** |
| v3 の \(R^{\mathrm{cyc}}\) 正本昇格 | **下記 P1–P3 の反映後に可** |

条件は三つである。

1. 証明済みの形式命題（補題 R）と、未証明の比較橋
   \((4)(5)\Rightarrow(5')\) に**別名・別札**を与える。
2. 系 (7.5) の未宣言な \(\iota\) を、\(\tau,\rho_0,q\) から一意に定義する。
3. §5.2.5 の「反証条件」を、形式命題の整合性検査と
   未証明の比較橋の falsifier に分ける。

これは定理 \(K3\) への差戻しではない。§0–§4 の定理 \(K3\) と
便 28 の紙上相互監査 PASS は不変である。

---

## F1. (R6-act) の型付けと (7.5) の降格

### F1.1 (R6-act)

\[
\rho_0:\mathfrak F_0\longrightarrow\operatorname{Sym}(\Lambda),
\qquad
\tau:\mu_M\hookrightarrow\operatorname{Sym}(\Lambda)
\]
を先に宣言し、
\[
\boxed{
\rho_0\text{ は忠実},\qquad
\rho_0(\mathfrak F_0)=\tau(\mu_M[e])
}
\tag{R6-act}
\]
としたのは、便 28 F7.3 の意図を正確に実装している。

両辺は同じ群 \(\operatorname{Sym}(\Lambda)\) の部分群であり、

- domain/codomain が明示されている、
- \(q\) の商写像を translation subgroup の埋込みと混同しない、
- \(P,H,X,\Phi\) という有限データだけで判定できる、

という三点で v2 の (6) より明確に強い。

§5.2.4 の五理由も全て妥当である。

1. **有限判定可能性**は正式前件を (R6-act) にする決定的理由である。
2. (7.5) を前件にすると算術比較そのものを前件へ書くことになり、
   族の構造条件としての情報量が小さい。
3. \(q\) は quotient map であって、一般には
   \(\mu_M[e]\) への retraction ではない。
4. (R6-act) \(+(5')\) は既存二例の証明鎖をそのまま抽象化している。
5. 補題 \(R'\) による「忠実性一ビット」への縮約が可能である。

従って、**(R6-act) 採択と (7.5) の系降格は PASS** と裁定する。

### F1.2 系 (7.5) に残った小さな型穴

ただし、現在の
\[
\operatorname{Ih}_N|_{G_K}
 =\iota\circ q\circ\kappa_{u^{-1}}
\tag{7.5}
\]
では \(\iota:\mu_e\to\mathfrak F_0\) が宣言されていない。
「何らかの抽象同型」を選ぶだけでは、作用の向きが合うとは限らない。

一意な修理は次である。まず (R6-act) から
\[
j:=
\bigl(\rho_0|_{\mathfrak F_0}\bigr)^{-1}
\circ
\tau|_{\mu_M[e]}
:\mu_M[e]\xrightarrow{\sim}\mathfrak F_0
\tag{1.1}
\]
を定める。\((5')\) と \(\tau,\rho_0\) の忠実性から
\[
\kappa_{u^{-1}}(G_K)\subseteq\mu_M[e]
\]
なので、\(\kappa_e\) をこの codomain への corestriction とすれば、
coprime 条件なしで
\[
\boxed{
\operatorname{Ih}_N|_{G_K}=j\circ\kappa_e
}
\tag{1.2}
\]
が従う。これが \(q\) を使わない正準な cocycle 系である。

\(r:=M/e\)、\(q(z):=z^r:\mu_M\twoheadrightarrow\mu_e\) と置く。
\(\gcd(e,r)=1\) のときだけ
\[
q_e:=q|_{\mu_M[e]}:\mu_M[e]\xrightarrow{\sim}\mu_e
\]
であるから、
\[
\boxed{\iota:=j\circ q_e^{-1}}
\tag{1.3}
\]
と定義すれば (7.5) が厳密に従う。

従って (7.5) の**降格判断は PASS** だが、
正本には (1.1)–(1.3) の型を一行で入れる必要がある。

---

## F2. 補題 \(R'\) — 中心化群論法

**PASS。三段とも正しい。**

\(\varphi\in\mathfrak F_0=\ker\widetilde\chi\) とする。
shadow の定義から
\[
\widetilde\chi(\varphi)=2m+1\equiv1\pmod{2M},
\]
従って
\[
\Phi_\varphi(X)=X^{2m+1}=X
\tag{2.1}
\]
である。

\(\Lambda\) の \(\Phi(\mathfrak F_0)\)-安定性を仮定しているので、
任意の \(H'\in\Lambda\) について
\[
\begin{aligned}
\rho_0(\varphi)\tau(\zeta_M)(H')
 &=\Phi_\varphi(XH'X^{-1})\\
 &=X\Phi_\varphi(H')X^{-1}\\
 &=\tau(\zeta_M)\rho_0(\varphi)(H').
\end{aligned}
\tag{2.2}
\]
従って
\[
\rho_0(\mathfrak F_0)
\le C_{\operatorname{Sym}(\Lambda)}(\tau(\mu_M)).
\tag{2.3}
\]

ここで (3) により \(T:=\tau(\mu_M)\) は \(\Lambda\) 上 regular である。
基点を一つ選び \(\Lambda\cong T\) と同一視すると、
左正則作用の中心化群は右正則作用である。一般の regular 群なら
ここで得るのは反対群の右作用だが、今回は
\(T\cong C_M\) が可換なので左作用と右作用が同じ部分群になる。従って
\[
C_{\operatorname{Sym}(\Lambda)}(T)=T.
\tag{2.4}
\]
(2.3)(2.4) から
\[
\rho_0(\mathfrak F_0)\le\tau(\mu_M)
\]
が従う。

さらに \(\mathfrak F_0\cong C_e\)、\(e\mid M\) であり、
\(\rho_0\) が忠実なら像の位数は \(e\) である。
巡回群 \(C_M\) の位数 \(e\) の部分群は一意だから
\[
\rho_0(\mathfrak F_0)=\tau(\mu_M[e]).
\]
逆向きは (R6-act) の定義に忠実性が含まれているので自明である。
従って
\[
\boxed{\text{(R6-act)}\iff\rho_0\text{ が忠実}}
\]
という縮約は正しい。

適用条件も v3 に書かれている。

- \(\Lambda\) が \(\Phi(\mathfrak F_0)\)-安定でなければ
  \(\rho_0\) 自体が定義されない。
- regular 性がなければ中心化群は大きくなり得る。
- regular でも作用群が非可換なら中心化群は同じ左正則部分群とは限らない。

本件では安定性を (6′) に、regular 性を (3) に、
可換性を \(\mu_M\) に置いており、隠れた仮定はない。

また、\(S_6\) の cycle type \(3.3\) だけから
\(\tau(\mu_6[3])\) を同定せず、(2.1) の可換性から同定した点は
便 28 W2 を正しく修理している。

---

## F3. 補題 R と安全な固定体

### F3.1 全射判定

補題 R の群論は閉じている。
\[
A:=\operatorname{Ih}_N(G_{\mathbf Q})
\]
と置くと、完全列と円分指標から
\[
A\cap\mathfrak F_0=\operatorname{Ih}_N(G_K).
\tag{3.1}
\]
\((5')\)、\(\rho_0\) の忠実性、\(\tau\) の忠実性により
\[
\begin{aligned}
|\operatorname{Ih}_N(G_K)|
 &=|\rho_0(\operatorname{Ih}_N(G_K))|\\
 &=|\tau(\kappa_{u^{-1}}(G_K))|\\
 &=\operatorname{ord}([u^{-1}]_M).
\end{aligned}
\tag{3.2}
\]
また (R6-act) から右辺は \(e\) を割る。
商への像は \((\mathbf Z/2M)^\times\) 全体なので
\[
|A|
=\operatorname{ord}([u^{-1}]_M)
 \cdot|(\mathbf Z/2M)^\times|.
\]
\(|\operatorname{GT}(N)|=e|(\mathbf Z/2M)^\times|\) と比較して
\[
\boxed{
\operatorname{Ih}_N\text{ 全射}
\iff \operatorname{ord}([u^{-1}]_M)=e
}
\]
が従う。循環はない。

### F3.2 固定体

\(\gamma\in G_{\mathbf Q}\) に対して
\[
\operatorname{Ih}_N(\gamma)=1
\iff
\gamma\in G_K\ \text{かつ}\ 
\kappa_{u^{-1}}(\gamma)=1.
\tag{3.3}
\]
逆向きで使うのは \(\rho_0|_{\mathfrak F_0}\) の忠実性である。
従って、全射か否かによらず
\[
\boxed{
\operatorname{Fix}(\ker\operatorname{Ih}_N)
=K\bigl((u^{-1})^{1/M}\bigr)
}
\tag{3.4}
\]
である。これは一般形として安全で、v3 の差替えは正しい。

さらに v3 注 3 の区別も正しい。
\[
\operatorname{Fix}\ker(\Phi\circ\operatorname{Ih}_N)
\]
まで (3.4) と同定するには、\(\Phi\) の単射性を別に要する。

### F3.3 coprime 書換えの「必要」方向

v3 の十分方向の証明は正しい。しかし本文は

> \(K((u^{-1})^{1/M})=K(u^{1/e})\) となるのは
> \(\gcd(e,M/e)=1\) のときに限る

と主張しているのに、書かれた三行証明は
\(\gcd(e,M/e)=1\Rightarrow\) 等号しか示していない。
主張自体は正しく、逆向きも短く閉じる。

\(v=u^{-1}\)、\(r=M/e\) とし、
\(\operatorname{ord}([v]_M)=e\) とする。
ある \(a\in K^\times\) が存在して
\[
v^e=a^M=(a^r)^e.
\]
従って \(v/a^r\in\mu_e\) である。
\(\mu_M\to\mu_e,\ \xi\mapsto\xi^r\) は全射なので、
ある \(\xi\in\mu_M\) に対して
\[
v=(a\xi)^r.
\tag{3.5}
\]
もし \(d:=\gcd(e,r)>1\) なら、指数 \(e\) の群
\(K^\times/K^{\times e}\) において \([v]_e\) は \(r\) 倍元だから
\[
\operatorname{ord}([v]_e)\mid e/d<e.
\]
従って
\[
[K(v^{1/e}):K]<e=[K(v^{1/M}):K],
\]
両体は等しくない。これで「ときに限る」の逆向きが閉じる。

正本ではこの逆向きを追記するか、現証明のままなら文言を
「\(\gcd(e,M/e)=1\) なら一致する」に弱めるべきである。

---

## F4. 未証明部の所在と命題の札

v3 の数学的認識、
\[
\boxed{\text{未証明部は }(4)(5)\Longrightarrow(5')\text{ である}}
\]
には同意する。旧 (6) の \(q\) を一般に導くことは、もはや本丸ではない。

ただし現在は同じ \(R^{\mathrm{cyc}}\) という名前が、

1. \((5')\) を前件に含む**証明済みの形式命題**（補題 R）と、
2. \((4)(5)\) から \((5')\) を出す**未証明の比較橋**と、
3. 両者を合わせた研究プログラム

の三つを指している。このままでは「定理候補・未証明」と
「補題 R 自体は証明済み」が同じ札の下に並ぶ。

正本では例えば次のように分けることを提案する。

- **定理 \(R^{\mathrm{cyc}}_{\mathrm{formal}}\)**:
  \((0)(1)(2)(3)(5')(6')\) から (R6-full) と (3.4)。
  これは v3 の証明で **paper-proof**。
- **比較橋 \(B_{\mathrm{FC}}\)（【GAP-Rcyc】）**:
  精密化した \((4)(5)\) から \((5')\)。
  これは **candidate / UNKNOWN**。
- **\(R^{\mathrm{cyc}}\) スキーマ**:
  \(B_{\mathrm{FC}}\) と
  \(R^{\mathrm{cyc}}_{\mathrm{formal}}\) を接続する設計図。

この分離をすれば「未証明の所在が移動した」という v3 の改善が
状態札にも反映される。

---

## F5. §5.2.5 の封印表

### F5.1 良い部分

次はそのまま採用してよい。

- \((3)\) の破れ、\(\Lambda\) の不安定、\(\rho_0\) の非忠実、
  \(\mathfrak F_0\) の非巡回を **scope-out** とし、
  \(R^{\mathrm{cyc}}\) の反例と混同しない。
- repeated-primary で旧 \(q\)-版と安全形を比較する。
- regular 性が破れた場合は補題 \(R'\) を使わず、
  (R6-act) を直接判定する。

### F5.2 修理が必要な部分

現在の scope-in は \((5')\) を含む。それにもかかわらず、
その同じ行の下で

> \(\operatorname{ord}([u^{-1}]_M)=e\) だが非全射

を \(R^{\mathrm{cyc}}\) の実験的 falsifier としている。
しかし \((5')\) と (R6-act) を本当に確認済みなら、
この不一致は F3 の有限群論により既に不可能である。
起きた場合に分かるのは「補題 R の紙上証明に誤りがある」か
「前件の確認札が誤っている」のいずれかであり、
未証明の比較橋を直接 falsify したことにはならない。

第三例用には次の五札へ分けるのが運用可能である。

| 札 | 封印する内容 | 判定 |
|---|---|---|
| **FORMAL-IN** | \((0)(1)(2)(3)(5')(6')\) | 補題 R の適用条件。結論との不一致は proof/record consistency failure |
| **BRIDGE-IN** | 結果を見る前に固定したモデル、cusp、局所助変数、actual marking、FC 比較規約 \((4)(5)\) | ここから (5′) が出るかを検査 |
| **BRIDGE-FAIL** | BRIDGE-IN を独立に満たすのに (7.3) が破れる | \(B_{\mathrm{FC}}\) の真の falsifier |
| **BRIDGE-UNKNOWN** | \((4)(5)\) から actual Galois 作用との比較を閉じられない | scope-out ではなく UNKNOWN |
| **SCHEMA-OUT** | regular detector 不在、不安定、非忠実、非巡回 | 現スキーマの射程外 |

さらに現表の「\(q\)-版の反証条件」は、既に撤回した v2 表記の
**legacy regression test** と改名するのが正確である。
これは live な v3 安全形の falsifier ではない。

以上を反映すれば、§5.2.5 を \(n=5\) campaign manifest に
組み込んでよい。

★ **前件に比較等式そのものを置いた瞬間、その先の結論試験は
未証明の橋の試験ではなく、形式系の整合性試験になる。**
「橋」と「橋を渡った後の群論」を別々に封印しないと、
何が反証されたかを後から選べてしまう。

---

## F6. 奇数族と \(K^{(5)}\) の事前値

通知 2 の

> 奇数族では \(\gcd(e,M/e)=1\) の見込み

は、少なくとも D1 の \(K^{(n)}\) 族では「見込み」より強く、
構造式から確定できる。

\(n\) が奇数なら
\[
M=K_{\mathrm{ord}}^{(n)}=\operatorname{lcm}(n,2)=2n.
\]
Thm 4.3 の \(m\mapsto2m+1\) は
\(\mathcal X_n\) から \((\mathbf Z/4n)^\times\) への全単射で、
その kernel では \(m=0\) である。残る \(k\bmod n\) が
Thm 4.6 の affine translation 部分 \(C_n\) を与える。従って
\[
\mathfrak F_0\cong C_n,\qquad e=n,\qquad M/e=2,
\]
ゆえに
\[
\boxed{\gcd(e,M/e)=\gcd(n,2)=1.}
\tag{6.1}
\]

\(n=5\) では事前値は次である。

| 項目 | \(K^{(5)}\) |
|---|---|
| \(M\) | \(10\) |
| \(P=G_5\) の位数 | \(4\cdot5^3=500\) |
| \(\operatorname{GT}(K^{(5)})\) | \(\operatorname{Aff}(\mathbf Z/5)\times C_2\)、位数 \(40\) |
| 円分商 | \((\mathbf Z/20)^\times\)、位数 \(8\) |
| \(\mathfrak F_0,e\) | \(C_5,\ e=5\) |
| \(M/e\) | \(2\) |
| \(K\) | \(\mathbf Q(\zeta_{20})\) |

Prop. 3.4 により \(K^{(5)}=K^{(10)}\) であることも
manifest に明記し、二つの独立例として二重計上しないこと。

この例は奇数族の横方向の安定性と \((5')\) を試すにはよい。
一方、(6.1) により repeated-primary や旧 \(q\)-版の弱点は
**全く試さない**。その役割を \(n=12\) まで保留するという
研究者裁定は筋が通っている。

---

## F7. \(K^{(5)}\) 橋 D1 の設計

### F7.1 計算前に封印すべき順序

1. **群論宇宙を固定する。**
   \(P=G_5\)、marking \(X,Y,Z\)、index \(10\) の部分群全体を
   探索宇宙とし、\(u\) を見る前に候補の採否規則を固定する。
2. **degree \(M=10\) detector を選ぶ。**
   必要なのは kernel の位数 \(e=5\) に合わせた degree 5 作用ではなく、
   \(\mu_{10}\)-torsor を見る degree \(10\) 作用である。
3. 各 \(H\) について
   \[
   N_P(H)=H,\qquad |\Lambda|=10,\qquad
   \langle X\rangle\text{ が }\Lambda\text{ 上 regular}
   \]
   を別々に判定する。最後の条件は、全 coset での
   \(H^g\cap\langle X\rangle=1\) まで確認する。
4. \(\Lambda\) の \(\Phi(\mathfrak F_0)\)-安定性を確認する。
   別の \(P\)-共役類へ送られる場合、都合よく和集合へ広げると
   \(|\Lambda|=M\) を壊すので、scope-out として記録する。
5. \(\rho_0\) の忠実性を確認する。
   \(\mathfrak F_0=C_5\) なので、指定 generator が一一点でも動かせば
   忠実である。そこから補題 \(R'\) により
   \[
   \rho_0(\mathfrak F_0)=\tau(\mu_{10}[5])
   \]
   が自動で従う。
6. その後にのみ、明示 \(\mathbf Q\)-モデル、
   \(\mathbf Q\)-有理な全分岐 cusp、actual marking、
   局所助変数を固定する。\(\operatorname{Aut}=1\) だけから
   field of moduli \(=\mathbf Q\) としない。
7. \((5')\) には独立の provenance を付ける。
   \(u\) の抽出と actual Galois action の同定を同じ等式で
   相互定義しない。
8. \(\Phi\) の単射性は別ゲートにする。
   補題 R の固定体は \(\ker\operatorname{Ih}\) の固定体であり、
   \(\ker(\Phi\circ\operatorname{Ih})\) の固定体まで述べるなら
   全 \(\operatorname{GT}(K^{(5)})\) 上の単射性が必要である。

### F7.2 予想値を証拠にしない

補題 \(R'\) が成立した後、\(\mathfrak F_0\) の generator は
10 点上で cycle type \(5^2\) になる。しかし

\[
\text{cycle type }5^2
\]
だけで \(\tau(\mu_{10}[5])\) を同定してはならない。
同定の証拠は \(X\) を固定することから来る中心化群包含である。
これは K3 の \(3.3\) と同じ落とし穴である。

また \(X,Y,Z\) が \(P\) の元として位数 \(10\) であることと、
degree 10 の coset 作用で三つとも 10-cycle になることは別である。
実際 \(XYZ=1\) なのに 10-cycle 三つはいずれも奇置換なので、
三つ全部を 10-cycle とする passport は符号だけで不可能である。
\(R^{\mathrm{cyc}}\) が要求するのは選んだ cusp の \(X\) が
regular であることであり、\((10,10,10)\) を先入観にしないこと。

### F7.3 強い整合性検査

\((5')\) と (R6-act) が成立すれば
\[
\operatorname{ord}([u^{-1}]_{10})\mid5.
\]
従って \(K^{(5)}\) では結果は二値である。

- 位数 \(5\): \(\operatorname{Ih}\) は全射。
- 位数 \(1\): 円分商だけでは kernel \(C_5\) を埋めず、非全射。

位数 \(2\) または \(10\) が出たなら、それを「新しい kernel 成分」と
解釈してはならない。\((5')\)、marking、局所 \(u\)、
または有限作用札のどれかが破れているという強い alarm である。

---

## F8. 状態札と追加証明書

§7.1 の射程分けは便 28 F9 を正しく採用しており **PASS**。

- \(\Lambda\) と \(\mathfrak F_0\)-作用: GAP/node `cross-checked`。
- \(\Phi\) 単射と Aut-融合: 紙上 + node、既存 GAP 証明書の
  直接射程外。
- 定理全体: paper-proof / two-mathematician audit PASS。
- Lean `verified` ではない。

\(\Phi\) 単射と Aut-融合の GAP 側再発注は、
定理 \(K3\) の数学ゲートには不要である。証拠札をさらに強めるという
provenance 上の任意作業であり、【GAP-Rcyc】より優先しない。
一方 \(K^{(5)}\) では、最初から load-bearing な有限項目を
GAP と helper 非共有の独立照合器に分けて記録すると、
後から同じ射程修正を繰り返さずに済む。

---

## F9. 通知 1 への短評（監査対象外）

\[
\mathcal L_m^{(j)}\ne\varnothing
\iff
\binom{m+1}{3}\equiv0\pmod{2^j}
\]
は、\(j=2\) の紙上証明と \(j=3\) の全 64 系観測が一致したので、
塔の candidate として保持する価値が高い。ただし現時点で
\(j\ge4\) へ量化しないという札を維持すべきである。

\(a\)-bit の
\[
m\equiv1\pmod8
\]
則は可解律とは別 candidate に保つのがよい。
「full \(=\) linear」と「どの affine lift が正規発火するか」は
異なる現象であり、一つの法則へまとめると
\(+1/-1\) 非対称の情報が消える。

本便では走査証明書・solver・64 系 witness を再監査していないため、
以上は通知に対する所見に限る。

---

## 提案

- **P1**: (1.1) の \(j\) を正準な作用同型として宣言し、
  q-free な系 (1.2) を先に書く。coprime 時だけ (1.3) で
  (7.5) へ書き換える。
- **P2**: \(R^{\mathrm{cyc}}_{\mathrm{formal}}\) と
  比較橋 \(B_{\mathrm{FC}}\)（【GAP-Rcyc】）を別札にする。
- **P3**: §5.2.5 を FORMAL-IN / BRIDGE-IN /
  BRIDGE-FAIL / BRIDGE-UNKNOWN / SCHEMA-OUT に分けてから
  \(n=5\) manifest に組み込む。
- **P4**: (7.2) の「ときに限る」を残すなら F3.3 の逆向きを追記する。
- **P5**: \(K^{(5)}\) では index 10 の \(H\) の宇宙と選択規則を
  \(u\) の開示前に封印する。
- **P6**: \(K^{(5)}\) の finite gate は
  「\(\Lambda\)-安定」と「\(\rho_0\) 忠実」を分けて記録し、
  後者だけを補題 \(R'\) の一ビット入力にする。
- **P7**: repeated-primary の legacy \(q\)-test は
  \(n=12\) manifest に予約し、\(n=5\) の成功で消化済みにしない。

## 警告

- **W1**: 未宣言の \(\iota\) を「指定された同型」で済ませると、
  v2 の「作用と一致する」という型穴が系の側へ再侵入する。
- **W2**: \((5')\) を scope-in に入れた試験は、
  \((4)(5)\Rightarrow(5')\) の falsifier ではない。
- **W3**: \(K^{(5)}\) で \(e=5\) だからと degree 5 detector を選ぶと、
  \(M=10\) の局所 Kummer torsor を失う。
- **W4**: \(\Phi(\mathfrak F_0)\) が二つの \(P\)-共役類を融合したとき、
  結果を見て \(\Lambda\) を和集合へ広げない。
- **W5**: cycle type \(5^2\) は部分群の同定証拠ではない。
- **W6**: \(n=5\) は coprime regime であり、
  repeated-primary の安全性試験には一票も加えない。

---

## ★教材

1. **regular abelian subgroup は self-centralizing だが、
   regular だけでは self-centralizing とは限らない。**
   左正則作用の中心化群は右正則作用であり、
   今回それが同じになる代金は可換性である。
2. **商への射 \(q\) と、regular 群内の部分群
   \(\mu_M[e]\) は別の型である。**
   coprime 条件は「商を部分群の座標として使える」ための条件で、
   部分群そのものの存在条件ではない。
3. **証明済みの形式帰結と未証明の比較橋を同じ候補名で呼ぶと、
   falsifier の宛先が失われる。**
   前件・橋・帰結の三札を分けて初めて、第三例が何を試したかが残る。

---

## 監査範囲外申告

本便では `sol/sol_task_29_v3_delta.txt`、
`docs/week4-K3飽和_opus_v3.md` 全文、
D1 抽出ノートの \(K^{(n)}\) 構造式、便 28 の自分の返信、
および対話帳の新着を紙上照合した。

定理 \(K3\) の不変部分（§0–§4）の全再監査、
GAP/node の 10/10 再走、j=3 の 64 系 witness、
LMFDB モデル、原論文 PDF、Lean 証明は本便では再検査していない。
従って本判定は v2 \(\to\) v3 の
\(R^{\mathrm{cyc}}\) 型付け差分と、その論理的波及に限る。
