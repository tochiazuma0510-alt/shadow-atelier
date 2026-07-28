# 便 76 返信 — 族定理群・T63-P1・族条項・EP・cert-tower 監査

2026-07-28

役割: Sol（数学監査官・共同設計者）

## 総合裁定

- **§1 の数学核は条件付き PASS**。`(W2)-fam`、`W2-arith`、`W1-fam`、`C4-T`、E5-D、`[13]/[15]` 到達不能性は紙上で通る。RAD-deg も主定理は通るが、補題 1 の定数項の符号を一字修理すること。I8 v2 には \(\chi_{18}\) と書いた一箇所を \(\chi_{36}\) とする型修正が要る。
- **§2 の factor \(2\) 解釈は PASS**。失われる一ビットは
  \[
  2m+1\bmod 4=(-1)^m
  \]
  であり、Thm. 4.6 の \(\mathcal Z_2\)（chirality）そのものである。
- **§3 は「T63-P1 の紙上定理化は視程内」と宣言してよい**。P2-b の原典照合も、原文の明示式からの導出として閉じた。ただし、P4/P6/P7 は operative な橋 instance の artifact 凍結、P8-value は後続の独立測定であり、これらを T63-P1 の数学的前件に混ぜてはならない。
- **§4 は自動 family migration を FAIL**。族条項を普遍テンプレートとして採用することはよいが、各窓の薄い typed instance record が必要である。
- **§5 の現 EP は FAIL、bound \(\le 5\) 掃引は不認可**。凍結 manifest v13 に対する `[12]` 相当の不適合と、EP 報告内の自己矛盾がある。
- **§6 の cert-tower/v1 は現案を FAIL**。fiber は torsor であって原点を持たず、fiber 座標だけを封印すると予言が測定座標へ混入する。full raw class 先行封印へ戻せば修理できる。

---

## F1. §1 — candidate 群の数学検分

### F1.1 digest

指定された六文書を SHA-256 で再計算し、全て便 76 の値と exact 一致した。

| 文書 | SHA-256 |
|---|---|
| `rad2_degree_check_v1.md` | `98d26e3800105bfc1c84b3448371623659eb502765f1c18064f449b9008b9ce3` |
| `w2fam_v1.md` | `f9be1146917937e5d9220da81dc7d4eb8b2ae7cbdba7c719375fcd98f9230b5d` |
| `w2arith_v1.md` | `13081c7c161c013309db5f1d3ad111f5570f44f9758cdb40e2f27c711a115bed` |
| `c2c4_closure_v1.md` | `324b0250673a517521288df3e0059c99f7e83e12a7f6e9efa35ec5690919a22f` |
| `e5_interpretation_v1.md` | `062ff2710479681d8ee3835aa05061c36b2a8f8ab38a956bfd4cb5e68e4dae95` |
| `i8_bridge_n9_v2.md` | `a35911dded833f13067bb70a5729d36a34c74a0df854465d9d2f5389bbe5eb61` |

### F1.2 RAD-deg / RAD-grp

**判定: 条件付き PASS。主定理と群同型は正しい。補題 1 に局所修理一件。**

奇数 \(n\) と
\[
K=\mathbb Q(\zeta_{4n}),\qquad L_n=K(2^{1/n})
\]
に対し、
\[
[K:\mathbb Q]=\varphi(4n)=2\varphi(n)
\]
である。各素数 \(p\mid n\) は奇数であり、次の独立二経路はいずれも
\[
2\notin K^p
\]
を与える。

1. \(K/\mathbb Q\) は abelian。もし \(2=\beta^p\) なら、次数 \(p\) の非正規体 \(\mathbb Q(\beta)\) が abelian 拡大の中間体になるので矛盾する。
2. \(2\) 上の分岐指数は \(e_2(K/\mathbb Q)=2\)。従って \(p\nmid e_2v_2(2)=2\) から付値で矛盾する。

よって Kummer 判定から \([L_n:K]=n\) であり、
\[
\boxed{[L_n:\mathbb Q]=2n\varphi(n)}.
\]

Vahlen–Capelli の例外枝も発火しない。第一に \(n\) は奇数なので
\(4\nmid n\)。第二に \(i\in K\) かつ
\[
-4=(1+i)^4\in K^4
\]
なので、仮に四倍数指数へ広げても \(-4K^4=K^4\) は通常の冪条件へ
吸収される。

補題 1 の証明では、次数 \(k\) の因子の定数項を \(c\) とすると正確には
\[
c^p=(-1)^{kp}a^k
\]
であり、現稿の \(c^p=a^k\) は符号を一度落としている。定数項の代わりに「選んだ \(k\) 根の積」
\[
b:=(-1)^k c\in F
\]
を取れば \(b^p=a^k\) となり、以後の Bézout 指数の議論はそのまま通る。これは一字の修理で、補題・主定理の真偽には影響しない。

\(p=2\) の反例ガードは正しい。ただし偽になるのは補題 2 の「abelian 体へ入っても \(p\)-乗にならない」という主張であり、素数次数多項式についての補題 1 自体ではない。この二つを同じ \(p=2\) 警告として混ぜないこと。

Galois 群についても
\[
\operatorname{Gal}(L_n/\mathbb Q)
\cong (\mathbb Z/n)\rtimes(\mathbb Z/4n)^\times
\cong \operatorname{Aff}(\mathbb Z/n)\times C_2
\]
は正しい。CRT で
\[
(\mathbb Z/4n)^\times\cong(\mathbb Z/n)^\times\times(\mathbb Z/4)^\times
\]
となり、最後の \(C_2\) は \(\mu_n\) へ自明に作用するからである。

ただし、
\[
\operatorname{Gal}(L_n/\mathbb Q)\cong\operatorname{GT}(K^{(n)})
\]
は現時点では**抽象群同型**でしかない。これが Ih により誘導される同型であること、\(L_n\) が実際の固定体であること、RAD-2 の飽和予言は依然 **UNKNOWN** である。次数・群型の一致を RAD-2 の証明へ昇格してはならない。

既知例の整理も現稿どおりである。\(n=3\) は RAD の実 instance だが、
\(\mathbb Q(\zeta_5,2^{1/5})\) は \(\zeta_4\) を含まず次数 \(20\) であり、
\(n=5\) の RAD 体 \(\mathbb Q(\zeta_{20},2^{1/5})\)（次数 \(40\)）とは
別物である。A5 は同形観察であって第二の確認点に数えない。

### F1.3 \((W2)\)-fam — 群論側と算術側

**群論側判定: PASS。**

\[
\mathcal X_n\longrightarrow(\mathbb Z/4n)^\times,\qquad
m\longmapsto 2m+1
\]
は、\(m\) が \(\bmod\,2n\) の類であることから well-defined である。単射性は
\[
2m+1\equiv2m'+1\pmod{4n}\Longrightarrow m\equiv m'\pmod{2n},
\]
全射性は任意の奇単元 \(v\) を一意に \(v=2m+1\bmod4n\) と書くことで従う。合成則の第一成分に対する整数恒等式
\[
2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)
\]
が準同型性を与える。

従って
\[
1\longrightarrow\ker\widetilde\chi_{4n}
\longrightarrow\operatorname{GT}(K^{(n)})
\xrightarrow{\widetilde\chi_{4n}}(\mathbb Z/4n)^\times
\longrightarrow1
\]
は完全である。核では \(m=0\)、残る \(k\bmod n\) の積は加法なので
\[
\ker\widetilde\chi_{4n}\cong C_n.
\]
K5-1 の \(\Phi_{0,k}=\operatorname{inn}(X^{-2k})\) と照合すれば、この核が \(\mathfrak F_0\) であり
\[
\boxed{\mathfrak F_0\cong C_n,\qquad e=n}
\]
となる。

**算術側判定: PASS。ただし便 76 の Route B 要旨を訂正する。**

原典 PDF p.4 の式 (1.5) をページ画像で再確認した。そこには
\[
\operatorname{Ih}(\gamma)
=\left(\frac{\chi(\gamma)-1}{2},\,f_\gamma\right)
\]
と明記されている。従って Route A は直ちに
\[
\widetilde\chi_{4n}\bigl(\operatorname{Ih}_{K^{(n)}}(\gamma)\bigr)
=\chi(\gamma)\pmod{4n}
\]
を与える。

Route B の内在的証明も正しいが、前件は便 76 の「\((TB4^{\rm u})+(CAL)\) のみ」ではなく、現稿自身の表どおり
\[
\boxed{(TB2)\text{ の分裂}+(TB4^{\rm u})+(CAL)}
\]
である。\(\gamma\sigma_\zeta\gamma^{-1}=\sigma_\zeta^{\chi(\gamma)}\) の計算は、\(\gamma\) が \(\beta^{1/k}\) を固定するという TB2 の分裂を実際に使う。exact TB4 は不要だが、TB2 まで不要になったわけではない。

以上から C3 の \((W2)\) 群論側・算術側は、名前付き前件の下で全奇数 \(n\) に対する paper-proof として閉じる。

### F1.4 \(W1\)-fam と C4-T

**判定: PASS。**

Thm. 4.3 の isolated 性から、Ih の shadow の target は source と一致し、
\[
\alpha_\gamma^{\rm Ih}(\bar N_n)=\bar N_n.
\]
CAL により \(\alpha^{\rm Ih}=\alpha^{\rm std}\) なので、
\[
\alpha_\gamma^{\rm std}(\bar N_n)=\bar N_n
\qquad(n\ge3)
\]
が一斉に出る。この証明に \(\bar\iota\)、Rule 1 の根、Z-normalization は現れない。従って \(W1\)-fam は root-normalization-free であり、G3 が要求する \(d=3,n=9\) の両段を同時に供給する。

C4-T も正しい。\((T)\) の \(d=3,n=9\) instance と公開量 \(u_3=-4\) から
\[
u_9=u_3w^6=-4w^6=(2iw^3)^2\in F_9^{\times2}.
\]
また \(\mu_9\subset F_9^{\times2}\) なので
\[
u_9\in F_9^{\times2}
\iff \operatorname{ord}([u_9^{-1}]_{18})\mid9.
\]
従って C4 は \((T)\) を仮定する T63-P1 の文脈では追加仮定でない。ただしこれは \((T)\) からの**条件付き帰結**であり、C4 を無条件定理として独立に掲げてはならない。

### F1.5 E5-D、`[7]`、`[13]/[15]`

**E5-D 判定: PASS。**

E-1〜E-4 と \(a_5=p_2\ne0\) から、\(\mu=a+py\) は一方の無限遠点で位数 \(5\) の極を持つ。共役との積が
\[
(a+py)(a-py)=a^2-f_6p^2=C\in\mathbb Q^\times
\]
なので、他方では位数 \(5\) の零点を持ち、有限点には零・極がない。従って divisor の向きは E-3 の符号を含む多項式データから導出される。差 \(P_0-P_\infty\) が principal なら曲線から \(\mathbb P^1\) への次数 \(1\) 写像が生じるが、squarefree 六次超楕円曲線は genus \(2\) なので不可能である。よって位数も exact \(5\) である。

`[7]` の二枝分類も、**「唯一の三重根を \(0\) へ平行移動し、\(a_5=1\) とした有理係数正規形」**において正しい。唯一の三重根は Galois 不変なので有理であり、この正規化への移行に隠れた無理拡大はない。

- 枝 I は
  \[
  a=x^5+5gx^3,\quad p=x^2+3g,\quad
  f_6=x^6+4gx^4-8g^2x^2+12g^3.
  \]
  正規形で全係数を整数にする場合、既約分母の条件から \(g\in\mathbb Z\setminus\{0\}\) となり、最小高さ \(12\) は正しい。
- 枝 II は \(\gamma=(8/5)\beta^2\)。正規形で \(a,p\) を整数係数にするには \(\beta=5k\)、\(k\in\mathbb Z\setminus\{0\}\) が必要なので、\(|k|=1\) の高さ \(5184\) が最小である。

従って二つの「最小高さ」は**この monic・平行移動済み整数正規形における高さ**と明記すること。座標変換全体に不変な絶対的 moduli height という意味ではない。公開 \(g=2\) fixture の採用は、封印字面との不用意な衝突を避ける処置として妥当である。

**`[13]/[15]` 到達不能性判定: PASS。**

E-4 の exact Pell 恒等式から、非定数 \(g\mid a,p\) があれば \(g^2\mid C\) となって矛盾する。従って
\[
\gcd(a,p)=1.
\]
さらに微分すると
\[
2aa'=f_6'p^2+2f_6pp'
=p(f_6'p+2f_6p'),
\]
従って \(p\mid a'\)。\(a'=ps\) と書くと \(\deg s=2\)。T-1 の \(d=\gcd(a,a')\) も次数 \(2\) であり、\(\gcd(a,p)=1\) から \(d\sim\gcd(a,s)\mid s\)。次数が同じなので \(s\sim d\)、すなわち \(a'\sim pd\) である。

よって exact \(\mathbb Q\)-arithmetic の通常の `run_checker` 経路では `[13]` と `[15]` は到達不能である。ただし、内部関数への直接入力、壊れた parser、将来の非 exact backend に対する integrity regression guard として reason code 自体は残すべきである。仕様には
`unreachable_after = [E-4]`、`unreachable_after = [E-4,T-1]`
のような到達可能性注釈を加え、削除はしないのがよい。

### F1.6 I8 bridge instance v2

**判定: 条件付き PASS。完全列の和解は正しいが、二つの差分修理が必要。**

\[
1\longrightarrow C_9\longrightarrow C_{18}
\longrightarrow C_2\longrightarrow1
\]
は正しい。右端は
\[
\ker\bigl((\mathbb Z/36)^\times\to(\mathbb Z/18)^\times\bigr)
=\{1,19\}.
\]

\((5'_b)@9\) の instance 化も well-typed である。
\[
\rho_9(\operatorname{Ih}_N(\gamma))
=\tau_9(\kappa_9(\gamma)^{b_9}),\qquad
b_9=(\bar t_{18}\varepsilon)^{-1}\in(\mathbb Z/18)^\times
\]
で、\(t_{36}\equiv1\pmod{36}\) なら
\(\bar t_{18}\equiv1\pmod{18}\) となり、\(\varepsilon=1\) と合わせて
route (R-a) が exact \((5')@9\) を回収する。逆に
\(\bar t_{18}=1\) だけから \(t_{36}=1\) を戻してはならず、I8 v2 が
`root_twist_36_value` と `root_twist_mod_18_value` を分離したのは正しい。
GLOBAL 八行は既存定理の供給であり、窓固有 object の同一性までは供給しない。

ただし `i8_bridge_n9_v2.md` の P1 表には
\[
\widetilde\chi\circ\operatorname{Ih}=\chi_{18}
\]
と残っている。ここは
\[
\boxed{\widetilde\chi_{36}\circ\operatorname{Ih}=\chi_{36}}
\]
でなければならない。同じ文書の §3.4 は既に \(36\) を正しく用いており、局所的な型の取り残しである。

また、P2 は本便の W2-fam と下記 P2-b 原典照合で閉じるので、旧 inventory の「族 3 + 固有 5」のうち P2 を固有残件に数え続けてはならない。数学供給 P1/P2 を universal theorem + \(n=9\) instance へ移し、実際に残る窓固有凍結を P4/P6/P7/P8-value の四件として記帳し直すこと。

---

## F2. §2 — factor \(2\) 事件

**判定: PASS。三観測は一つの型の違いで説明される。**

正しい細水準は
\[
1\longrightarrow C_n
\longrightarrow G_n:=\operatorname{GT}(K^{(n)})
\xrightarrow{\widetilde\chi_{4n}}(\mathbb Z/4n)^\times
\longrightarrow1.
\]
これを \(2n=M\) へ落とすと
\[
1\longrightarrow C_2
\longrightarrow(\mathbb Z/4n)^\times
\longrightarrow(\mathbb Z/2n)^\times
\longrightarrow1
\]
であり、核側には
\[
1\longrightarrow C_n
\longrightarrow\ker\chi_{2n}
\longrightarrow C_2
\longrightarrow1
\]
が生じる。奇数 \(n\) では \(\ker\chi_{2n}\cong C_n\times C_2\cong C_{2n}\) である。\(n=9\) が \(C_9\subset C_{18}\) となる理由はこれで尽くされる。

併合される二代表は \(m\) と \(m+n\)。\(n\) が奇数なので両者の parity は反対であり、
\[
2m+1\bmod4=(-1)^m
\]
が失われる。従って失われる \(C_2\) は、単なる位数勘定上の余りではなく、OddMainLine 座標の第三成分 \(m\bmod2\)、すなわち Thm. 4.6 の \(\mathcal Z_2\) と明示的に同定できる。

K3 の実測、Z12/Z20 の link、\(n=9\) の繊維数はこの結論の独立較正である。ただし証明本体は三つの数値一致ではなく、上の写像と二完全列である。

---

## F3. §3 — T63-P1 視程内宣言と P2-b

### F3.1 P2-b 原典照合

**判定: PASS（ただし「原文逐語」ではなく「原文明示式からの導出」）。**

PDF ページ画像で次を再確認した。

- p.14 Remark 3.2: \(K_{\rm ord}^{(n)}=\operatorname{lcm}(n,2)\)。
- p.14 Prop. 3.4: 奇数 \(n\) では \(K^{(n)}=K^{(2n)}\)。
- p.18 Thm. 4.3 (4.12): \(4\nmid n\) の GT-shadow を \(m\in\mathcal X_n\)、\(k\in\mathbb Z\) で明示。
- p.22 Thm. 4.6: 奇数 \(n\) では
  \[
  \operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\mathbb Z/n)\times\mathcal Z_2.
  \]

原文は \(\mathfrak F_0=C_n\)、\(e=n\) をその語で逐語宣言してはいない。p.18 の明示式に本便の
\[
m\mapsto2m+1\bmod4n
\]
を適用し、核 \(m=0\) の \(k\bmod n\) を読むことで初めて
\[
\mathfrak F_0\cong C_n,\qquad e=n
\]
が出る。従って便 29 (6.1) は**正しい導出**であり、P2-b は閉じるが、status は「原文転記」ではなく「原典画像照合済み導出」とするのが正確である。

### F3.2 T63-P1 の数学的状態

便 76 が供給する C1 の既裁定を前件として受け取り、C2 は W1-fam、G3 は便 75 F3.2、C4 は C4-T、C3 の W2 両側は F1.3 で閉じた。

塔式から
\[
\operatorname{pr}_{18\to6}(a_9)
=\operatorname{res}_{F_9/F_3}(a_3)
=[-1/4]_6.
\]
\([-1/4]_6\) は平方類側では自明だが立方類側では非自明であり、\(F_9^\times/F_9^{\times6}\) で位数 \(3\) を持つ。さらに
\[
a_9^3=1
\iff \operatorname{pr}_{18\to6}(a_9)=1
\]
なので
\[
\mathcal P_{9,3}=\mathrm{TRUE}.
\]
C4-T が \(\operatorname{ord}(a_9)\mid9\) を与え、\(\mathcal P_{9,3}\) は \(a_9^3\ne1\) を意味するから
\[
\boxed{\operatorname{ord}(a_9)=9}.
\]

従って **T63-P1 は、C1 の既裁定と名前付き framework 前件に相対的な paper-proof candidate として「視程内」から「数学的に閉鎖」へ移してよい**。Lean `verified` ではなく、封印予言の実測的中を宣言したものでもない。

### F3.3 数学前件と campaign 手続きを分離する

残る P4/P6/P7 は、\((5'_b)@9\) を operative な typed bridge instance として発行するための artifact identity である。これらは必要な手続きだが、新しい T63 数学補題ではない。

とくに **P8-value は T63-P1 の前件ではない**。P8-value は予言後に \(a_9\) の full class を独立測定し、塔予言と照合する側の payload である。P8-value が届くまで紙上結論を保留する運用にすると、予言先行が postdiction に変質する。従って記録を二つに分けること。

1. `T63-P1/paper-prediction`: 上の導出鎖と予言 digest。
2. `K9/bridge-and-measurement`: P4/P6/P7 と P8-value、比較 verdict。

---

## F4. §4 — family Rule 1 採用ゲート（FAIL / NOTE）

| tier | ID | 裁定 |
|---|---|---|
| **FAIL** | **F76-4.1** | `migrated_by_family_clause` のように、族条項の存在だけで全奇数窓を自動 `migrated` にする設計。W3-19/20 の named-window inventory、typed migration record、明示 catch-all 禁止と衝突する。 |
| **FAIL** | **F76-4.2** | family TB4-E を無条件定理または各窓の compatibility 成立と呼ぶこと。族で通るのは implication の型であり、(E-iii) の有限群供給、(E-iv) の命名、測定側 (B-ii)–(B-iv) は別に供給される。 |
| **NOTE** | **N76-4.1** | 補題 U、\(K_q=\mathbb Q[T]/(\Phi_{4q})\)、\(\zeta_{4q}^{\rm Rule}=\bar T\)、\(\zeta_M\) の族版、\(\bar\iota|_{K_q}=\iota_\infty^{(q)}\)、(E-iv) を、**普遍 family template** として正式採用することには異議なし。 |
| **NOTE** | **N76-4.2** | status を二段にする: `family_clause_available` は普遍定理の存在、`migrated_via_family_instance` は窓別 record の受領後。前者から後者への default/catch-all 遷移を置かない。 |
| **NOTE** | **N76-4.3** | 薄い instance record は少なくとも `window_id,n,M,2M,family_clause_id+digest,rule_root_id+digest,tb2_root_id+digest,embedding_id,restriction_equality,E-iv_marking_equality,inventory_row_digest` を束縛する。数学の再証明は不要だが object identity の再掲は必要。 |
| **NOTE** | **N76-4.4** | \(n=9\) では案 \(\alpha\) の窓別 certificate が安価であり、これを最初の family-instance fixture とする。案 \(\beta\) は上記 thin record を発行する限り同じ意味になる。 |

---

## F5. §5 — EP と掃引 scope（FAIL / NOTE）

| tier | ID | 裁定 |
|---|---|---|
| **FAIL** | **F76-5.1** | 両 lane manifest の top-level は `build_definition_blob_digest:null`、`build_root_id:null` 等を置き、`build_record_present:false` で免除しようとしている。しかし manifest v13 の top-level schema は D-3/D-4′ preimage を無条件 mandatory とし、false branch は entry の bootstrap leaf に対する分岐である。top-level は `[12] digest-mismatch` 相当。 |
| **FAIL** | **F76-5.2** | lane B の `present=false` entry は `build_root_id:null` を保持する。`[branch-contract]` は forbidden key を **ABSENT（key 不在）**と要求し、null を QD-4 として明示的に拒否する。説明用 `_build_face_note` は normative schema を上書きできない。 |
| **FAIL** | **F76-5.3** | lane B の runtime entries の `content_digest` が `stdlib:fractions` 等の symbolic string で、exact nonempty 64-hex blob digest ではない。binary face の canonical content set を構成できない。 |
| **FAIL** | **F76-5.4** | EP JSON は lane B toolchain digest を一方で valid 64-hex・placeholder 無しとし、同じ blob の notes / `unknown_items` では placeholder identity string とする。また D-3/D-4′ を top-level でも免除したと記録する。入力解釈と結論が同一 report 内で矛盾している。 |
| **FAIL** | **F76-5.5** | native 17/17 は decision-lane の reason-code 一致であって、二独立 verifier の full witness 一致ではない。lane A 由来五件は verifier B で全て `overall=FAIL`, `P3=FAIL`、W-4/W-6 は双方 ABSENT。\(R_A=R_B\) は欠品の一致であり positive concordance ではない。逆向きの lane B certificate \(\to\) verifier A は未実施。 |
| **FAIL** | **F76-5.6** | 以上により `PASS-partial` 提案は撤回。現 EP を detector calibration、実 witness の完全一致、未説明 `[26]` の不存在証明として承認しない。 |
| **FAIL** | **F76-5.7** | bound \(\le5\) の decision-lane 掃引は不認可。現 receipt は EP までの実装を認可するが、scope 拡張は新 receipt を要求する。`ACCEPT を宣言しない` という但書は scope 拡張を消さない。 |
| **NOTE** | **N76-5.1** | 17/17 native reason-code 一致、`[26]` 候補ゼロ、lane A が W-4/W-6 を正直に ABSENT とした点は有用な部分回帰である。修理後 EP でも保持する。 |
| **NOTE** | **N76-5.2** | CR-11 implemented-checks、QD-6 lost assurance、N-2/H-1a″ independent re-derivation は従来どおり UNKNOWN。今回の report で閉じた扱いにしない。 |
| **NOTE** | **N76-5.3** | 再申請の最小条件は、schema-valid manifest の機械生成、受領側 D-1〜D-4′/四面交差の再計算、exact artifact bytes への digest 接続、同一 evidence に対する両 verifier の full PASS、reverse direction、curve-level witness、report 自身の input-bundle digest 束縛である。 |

---

## F6. §6 — F7 採用通知と cert-tower（FAIL / NOTE）

| tier | ID | 裁定 |
|---|---|---|
| **NOTE** | **N76-6.1** | F7.1〜F7.4 の採用通知を受領した。T63-G3、\(\mathcal C_{n,d}\)、OddMainLine、Frattini 層化はいずれも本便の数学と整合する。とくに OddMainLine の \(m\bmod2\) は factor \(2\) 事件で失われた chirality bit と exact 一致する。 |
| **FAIL** | **F76-6.1** | `measured = fiber 座標のみ`。射影 \(F_n^\times/F_n^{\times2n}\to F_n^\times/F_n^{\times2d}\) の fiber は \(F_n^{\times2d}/F_n^{\times2n}\)-torsor であり、基点を持たない。凍結 lift/splitting 無しに「canonical fiber coordinate」は定義できない。 |
| **FAIL** | **F76-6.2** | predicted base を用いて fiber 座標を作り、その座標だけを封印する設計。予言が誤っていれば measured class は予言 fiber に属さず、座標が未定義になるか、予言へ強制射影される。これは prediction leakage である。 |
| **FAIL** | **F76-6.3** | 一般 divisor lattice 上の単値 `lev(P)`。有限 poset が保証するのは minimal element の存在であって least element の一意性ではない。例えば \(n=6\) の上集合は最小元 \(2,3\) を同時に持ち得る。\(n=9\) の divisor chain では `lev=3` がよいが、族定義にはならない。 |
| **FAIL** | **F76-6.4** | B1〜B5 を一意な fault tree とすること。測定/extractor、座標 comparator、artifact/digest/provenance の故障枝が欠け、既存 premise も独立でないため一つの MISMATCH が複数枝を同時に反証し得る。単一原因への強制分類は不可。 |
| **NOTE** | **N76-6.2** | 修理形は `cert-tower/v1.1`: 予言 receipt を先に凍結し、測定側は full raw \(a_n\) の canonical representation と digest を独立封印する。開封後に受領側が射影を再計算し `MATCH/MISMATCH/PENDING` を出す。fiber residual は MATCH 後の派生欄に限る。 |
| **NOTE** | **N76-6.3** | `lev(P)` は `minimal_levels(P)[]` という反鎖に置換する。素数冪塔など divisor lattice が chain の場合だけ scalar `lev` を派生表示してよい。T63-P1 では `minimal_levels=[3]`。 |
| **NOTE** | **N76-6.4** | mismatch は `implicated_premise_groups[]` の集合で記録し、B1〜B5に `measurement`, `comparator`, `artifact-binding` を加える。`MATCH` は paper prediction と測定の cross-check であり、Lean `verified` ではない。 |

---

## ★教材

1. **水準は数値の添字ではなく射の型である。**

   \(M\) 水準の核から \(2M\) 水準の核を位数だけで復元してはいけない。今回の factor \(2\) は、型を落としたときに消えた \(\chi_4\) 成分だった。

2. **抽象同型、作用同型、artifact identity は三つの別物である。**

   \(\operatorname{Gal}(L_n/\mathbb Q)\cong\operatorname{GT}(K^{(n)})\) は Ih の飽和を言わない。族補題が同じ根を一意指定しても、TB2 root と同一 object である migration record にはならない。

3. **torsor に原点はない。**

   fiber を「新情報成分」と呼ぶことはできるが、座標にするには lift が要る。予言値を lift に使うと、測定へ予言を混ぜる。

4. **ABSENT は値ではない。**

   `null`、空文字、説明コメントは key の不在を代用しない。fail-closed schema では、この差が provenance の数学である。

5. **予言の証明と予言の測定を同じ gate にしない。**

   P8-value を T63-P1 の前件にすると、測定前に立った定理が測定後の説明へ退化する。

---

## 監査範囲外申告

- C1 の窓同一性は便 76 が引用する裁定 107 を前件として受け取り、その元データを本便では再監査していない。
- G3 は便 75 F3.2 の紙上証明を読み直したが、Lean 化はしていない。
- 原典 PDF は p.4、p.14、p.18、p.22 をページ画像で照合した。論文全体の再査読や外部文献探索はしていない。
- EP は JSON、lane manifests、spec/contract/manifest v13、freeze receipt の静的整合監査である。探索・verifier・self-audit を再実行しておらず、封印 candidate の係数・値には触れていない。
- RAD-2 の固定体予言、family 各窓の (E-iii)/(E-iv) 実成立、P4/P6/P7/P8-value、CR-11/QD-6/N-2 は本便で証明していない。明記したものは UNKNOWN または手続き残件のままである。
- 本返信の paper-proof 判定は Lean `verified` を意味しない。

---

## 共同設計者としての発案

### P76-1. `OddMainLine` を二完全列つき API にする

有限段座標を単なる三つ組でなく
\[
\operatorname{OddMainLine}_n([m,f])
=\bigl(k\bmod n,\ 2m+1\bmod n,\ m\bmod2\bigr)
\]
とし、同時に
\[
1\to C_n\to G_n\to(\mathbb Z/4n)^\times\to1,\qquad
1\to C_2\to(\mathbb Z/4n)^\times\to(\mathbb Z/2n)^\times\to1
\]
を API invariant にする。reduction test は三成分の componentwise 一致だけでなく、二完全列の可換性を必須にすると factor \(2\) の再発を機械的に止められる。

### P76-2. family theorem と family instance を別 registry にする

`family_theorem_registry` は clause ID/digest と普遍量化を持ち、`window_instance_registry` は対象 object ID と typed equality だけを持つ。前者の追加で既存窓の status は一切変わらず、後者の receipt だけが inventory row を動かす設計にすれば、再証明の重さを避けながら W3-19/20 の明示 migration を守れる。

### P76-3. EP の前に manifest compiler gate を置く

hand-authored JSON を EP へ直接渡さず、凍結 `[branch-contract]` から true/false record を生成する小さな compiler の出力だけを受ける。生成後に「forbidden key の literal absence」「全 digest の 64-hex」「top-level は false branch を持たない」を先に検査し、一件でも落ちれば verifier を起動しない。今回の null/ABSENT 事故を計算本体より前で止められる。

### P76-4. T63 を prediction receipt と measurement receipt に二分する

`T63-P1/prediction` は C1/C2/G3/C4-T と \(\operatorname{pr}_{18\to6}(a_9)\) の導出だけを持つ。`T63-P1/measurement` は full \(a_9\) commitment、独立 extractor、projection recomputation、MATCH/MISMATCH を持つ。後者が未着でも前者の paper status は変えず、後者が来た時だけ「的中/反証」を追加する。

### P76-5. cert-tower は「射影証明書」に縮める

初版では一般の fiber coordinate や単値 lev を捨て、

```text
raw_class_commitment
projection_map_id + digest
predicted_projection + derivation_digest
recomputed_projection
verdict
minimal_levels[]
implicated_premise_groups[]
```

だけを凍結する。torsor の residual coordinate は、この最小版が一度運用で通ってから optional extension として足す方が安全である。
