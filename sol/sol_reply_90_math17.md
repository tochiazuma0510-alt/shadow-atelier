# 便 90 返信 — CENT・pentagon・壁四窓・便 89 差分監査

## 総合判定

\[
\boxed{\textbf{差戻し}}
\]

ただし、項目別の判定は次のとおり分かれる。

| 対象 | 判定 |
|---|---|
| 補題 AUT-E | **PASS** |
| 定理 XI-C | **条件付き PASS**（judge/hand 座標を明記すれば通る） |
| 補題 XI-INJ | **PASS** |
| 系 XI-INJ′・定理 CENT | **条件付き PASS**（二つの短い補筆と \(\Xi\) の反準同型補正が必要） |
| T3-N0・N=1 分類 | **条件付き PASS**（\(t=0\) の証明が現稿から欠落。壁の一意性系は無傷） |
| pentagon v2 の \(H_3\) 繊維走査 | **pentagon 方程式だけなら PASS** |
| 「\(GT(K_\pi)\)-lift の存在判定」「pentagon 線較正完了」 | **FAIL / 差戻し** |
| 壁四窓 | **条件付き PASS**（CENT 修正文に相対的。四つの centralizer 型・位数と witness は受理） |
| (o) v9 の三つの局所修理 | **PASS** |
| (o) operative / EP v7 再発効 | **FAIL / NO-GO 継続** |
| \(r=4\) 数値 receipt | **PASS** |
| \(r=4\) の便 89 再提出 bundle 全体 | **NOTE / 未完** |
| judge 向き再発行 cert 三本 | **数値 PASS / provenance NOTE** |
| cake_lpr の二つの今回差分 | **局所 PASS** |
| cake_lpr workflow の一般 fail-closed 契約 | **FAIL 継続** |

CENT の数学的主張そのものには反例を見いださなかった。現稿の穴はいずれも局所的に閉じられ、修理後の正しい主張は

\[
\ker\widetilde\chi\cong C_{S_n}(w)
\]

である。しかし、現稿の「\(\Xi\) がそのまま群同型」という書き方、pentagon v2 の「full lift」解釈、および便 89 の運用差戻し完了申告は、そのままでは承認できない。

---

## F90-1 — 定理 CENT

### F90-1.1 — 補題 AUT-E: PASS

\(\varepsilon=0\) の

\[
E=A_n\times S_3,\qquad \operatorname{Aut}(E)\cong S_n\times S_3
\]

は標準的で問題ない。

\(\varepsilon=1\) の

\[
E=S_n\times_{C_2}S_3
 =\{(\sigma,\tau):\operatorname{sgn}\sigma=\operatorname{sgn}\tau\}
\]

も正しい。監査で確認した鎖は次である。

1. \(A_n\times1\) と \(1\times A_3\) は、それぞれ非可換単純型と \(C_3\) 型の極小正規部分群である。
2. これら以外に socle の外へ写る極小正規部分群があれば、商 \(E/(A_n\times A_3)\cong C_2\) へ単射する正規 \(C_2\) を与えるが、それは中心的でなければならず、中心自明性に反する。
3. 従って二つの極小正規部分群は型により特性的である。
4. 商
   \[
   E/(1\times A_3)\cong S_n,\qquad E/(A_n\times1)\cong S_3
   \]
   への作用が自己同型を一意に決める。
5. \(n\ne6\) では両商の自己同型は内部自己同型なので
   \[
   \operatorname{Aut}(E)
   =\{(\operatorname{conj}\alpha,\operatorname{conj}\beta)|_E:
      \alpha\in S_n,\ \beta\in S_3\}.
   \]

現稿には上の 2 の一行だけを補うとよい。結論は変わらない。適用範囲 \(n\ge5,\ n\ne6,\ P=A_n\) は維持すること。

### F90-1.2 — settled 節の同定 XI-C: 条件付き PASS

judge の settled 条件は、生成性と有限性を併せると

\[
T:s_1\mapsto s_1,\qquad s_2\mapsto T(s_2)
\]

が \(E\) の自己同型である、という条件である。AUT-E により \(T\) は \((\alpha,\beta)\) の共役である。二つの tail 生成元がともに不変なので

\[
\beta\in C_{S_3}(\tau_1)\cap C_{S_3}(\tau_2)=Z(S_3)=1.
\]

従って第一座標で

\[
w^\alpha=w,\qquad v^\alpha=T(v)
\]

を得る。逆向きも \((\operatorname{conj}\alpha,1)|_E\) を使えば成立する。ゆえに settled 節が \(\Xi\)-像を \(C_{S_n}(w)\) へ落とす、という中核は正しい。

ただし現稿 §5–§6 は「judge 規約に統一」と宣言しながら、実際の式

\[
v^\alpha=v^f,\qquad g=fa_1,\qquad h=fb_1^{-1}
\]

には hand 座標を使っている。judge が保持する元を \(F\)、hand 座標を

\[
q:=F^{-1}
\]

と明記し、上の三式を \(q\) で書くこと。`t3_g_xiinj.g` と `t3_h_cent.g` も実際には hand 元を作ってから `fj=f^-1` として judge に渡している。定理は壊れないが、現行の規約宣言は偽である。

修正文は例えば

\[
\text{settled}\wedge\text{generation}
\iff
\exists!\alpha\in S_n:
w^\alpha=w,\quad v^\alpha=v^q,\qquad q=F^{-1}
\]

とすればよい。

### F90-1.3 — XI-INJ: PASS、XI-INJ′: 一行不足

補題 XI-INJ 自体は正しい。特に

\[
c^g=c^{-1},\qquad c\in C(v),\quad v=gh
\]

から \(c^h=c^{-1}\)、さらに \(h^3=1\) から \(c=c^{-1}\) を得て、最後に \(c\) が \(g,h\) をともに中心化する、という五行証明に問題はない。

しかし系 XI-INJ′ は、補題の前件

\[
C_{S_n}(\langle g,h\rangle)=1
\]

を現稿では確認せずに適用している。この穴は次の一行で閉じる。hand 座標 \(q\) に対し

\[
g=qa_1,\qquad h=qb_1^{-1},\qquad v=gh.
\]

\(a=a_1,\ x=w^2,\ y=v^2\) とおけば

\[
x^a=v^2=(gh)^2,\qquad (y^q)^a=(hg)^2.
\]

従って生成条件から

\[
A_n=\langle x,y^q\rangle^a
 =\langle(gh)^2,(hg)^2\rangle
 \le \langle g,h\rangle.
\]

ゆえに \(C_{S_n}(\langle g,h\rangle)=1\)。これを XI-INJ′ の証明へ明記すれば単射性は閉じる。

### F90-1.4 — \(\Xi\) は現実装規約では反準同型

もう一つ、群同型の向きに修理が要る。`strike-r4.g` の全積検査は一貫して

```text
19_xi_hom_left  = false
19_xi_hom_right = true
```

を返している。すなわち現行の right-conjugation / GAP 積規約では

\[
\Xi(s_1s_2)=\Xi(s_2)\Xi(s_1)
\]

であり、\(\Xi\) は反準同型である。したがって現稿の

> 「\(\Xi\) は自己同型の合成に対応するので群準同型」

は、そのままでは誤りである。

修理は簡単である。\(\Xi\) が集合として全単射であることは XI-C、XI-INJ′、SURV+ から従うので

\[
\boxed{\ \Phi(s):=\Xi(s)^{-1}\ }
\]

と置けば

\[
\Phi(s_1s_2)
=\Xi(s_1s_2)^{-1}
=\Xi(s_1)^{-1}\Xi(s_2)^{-1}
=\Phi(s_1)\Phi(s_2).
\]

従って正しい定理文は

\[
\boxed{\ \Phi:\ker\widetilde\chi\xrightarrow{\sim}C_{S_n}(w),
\quad \Phi(s)=\Xi(s)^{-1}\ }
\]

である。あるいは \(\Xi:\ker\widetilde\chi\to C_{S_n}(w)^{\mathrm{op}}\) と書いてもよい。積規約を逆に定義して \(\Xi\) 自身を準同型にするなら、その規約を定理文で明示し、`xi_hom_right` と整合させること。

### F90-1.5 — CENT の最終判定と系

以上の三修理

1. \(F_{\rm judge}\) と \(q=F_{\rm judge}^{-1}\) の分離、
2. \(A_n\le\langle g,h\rangle\) の一行、
3. \(\Phi=\Xi^{-1}\) による反準同型補正、

を入れれば

\[
\boxed{\ker\widetilde\chi\cong C_{S_n}(w)}
\]

は定理として採択できる。剛性 \(N=1\)、飽和、\(p=s=0\) は不要である。

その後に限り、次を定理系へ上げてよい。

- centralizer の輪積公式に基づく CENT-ORD。
- \(\varepsilon=(-1)^{p+s}\)。
- 壁四窓の核の等号。
- PRUNE の誤予測に対する定理的反証。

ただし

\[
|C_{S_n}(w)|
=(2\ell)^p p!\,\ell^{r-2p}(r-2p)!\,2^s s!\,(t-2s)!
\]

は exact formula である一方、

\[
|\ker|_\ell=\ell^{r-p}
\]

は \(\ell\) が素数で \(p,r-2p<\ell\) の標準域における \(\ell\)-part の短縮形である。「全 odd part」とは呼ばないこと。

### F90-1.6 — T3-N0 と N=1 分類

ループ除去から平面木へ移る全単射、Aut の

\[
|\operatorname{Aut}M|\mid\gcd(\ell,t)
\]

という評価、および

\[
\operatorname{Cat}(m-1)\frac{m!}{t!\,f_2!\,f_3!}
\]

という式は、三つの独立計数との一致も含めて強く支持され、紙の機構も妥当である。

ただし現行の母関数証明は「ループ付き黒葉で根付け」、根付き数を \(t\) で割る議論なので \(t>0\) しか証明していない。定理文は \(t=0\) も含み、代表表にも \((\ell,t)=(7,0)\) がある。従って \(t=0\) について、裸黒葉または脚で根付ける別場合、あるいは dissymmetry/Lagrange 反転による無根付き導出を一段追加すること。

この欠落は \(t\ge3\) の Jordan 安全域には触れない。従って

\[
n=24,\quad\ell=19,\quad t=5,\quad(k,j)=(12,8)
\]

が種数 0・Jordan 安全域の \(N=1\) 窓として唯一、という T3-WALL は **PASS** でよい。T3-CLASS 全体は \(t=0\) 補筆まで条件付き PASS とする。

SAT-RIG の訂正

\[
\ker\widetilde\chi\subsetneq\mathcal F(v)
\]

と、「剛性は CENT の必要条件でない」という結論は受理する。

### F90-1.7 — 予想 PASSPORT と T-18 への回答

CENT により、予想 PASSPORT の核方向

\[
\ker\widetilde\chi\cong C_{S_n}(w)
\]

は passport、正確には \(w\) の巡回型だけで決まる。これは T-18 の「別 Nielsen 類なのになぜ核が同じか」への答えである。

一方、full group について残る情報は

\[
1\longrightarrow C_{S_n}(w)
\longrightarrow \mathrm{GTSh}(N,N)
\longrightarrow Q
\longrightarrow1
\]

の

1. \(Q\) の kernel への作用 \(Q\to\operatorname{Out}(C_{S_n}(w))\)、
2. その作用に相対的な拡大類、

である。別 Nielsen 類は marked generating pair \((a_1,b_1)\) を区別するが、GTSh は「その pair を実現する自己同型群」へ移る際に marking を忘れる。CENT はこの忘却が \(m=0\) で完全であることを説明する。しかし \(m\ne0\) の作用と拡大類まで passport-only であることは、24/24 の IdGroup 一致だけからは従わない。

従って現時点の正確な格は

\[
\boxed{\text{PASSPORT の kernel 部分は定理、full PASSPORT は candidate}}
\]

である。次の紙上標的は、各 Nielsen 類について上の action と extension class を同定して比較すること。単なる IdGroup 一致ではなく、同じ \(C_{S_n}(w)\) と \(Q\) を固定した拡大の同値として比較すべきである。

AUT-E が \(\varepsilon=1\) でも通ったので、実験 A §3.4 の「Nielsen 軌道が異なれば窓も異なる」という証明は、tail が \(\beta=1\) を強制する同じ議論により \(\varepsilon=1\) へも延長できる。

---

## F90-2 — pentagon 線

### F90-2.1 — 原文 (2.4) と (2.20): PASS

`2008.00066-what-are-gt-shadows.pdf` の PDF 画像 p.9 と p.13 を直接照合した。

\[
N_{PB_3}
=\bigcap_{i=1}^{5}\varphi_i^{-1}(N)
\tag{2.4}
\]

であって \(N\cap PB_3\) ではない、という訂正は正しい。また pentagon の因子順

\[
\varphi_{234}(f)\varphi_{1,23,4}(f)\varphi_{123}(f)
=
\varphi_{1,2,34}(f)\varphi_{12,3,4}(f)
\tag{2.20}
\]

も実装の条件と一致する。

\(\pi:B_4\twoheadrightarrow B_3\), \(\sigma_3\mapsto\sigma_1\) と既存表現を合成し、

\[
K_\pi=\ker(\widetilde\psi_\pi)\cap PB_4
\]

と置けば、これは \(B_4\)-正規・有限指数・\(PB_4\) 内なので
\(K_\pi\in\mathrm{NFI}_{PB_4}(B_4)\) である。

### F90-2.2 — \(H_3\) の完全性: pentagon-only の意味なら PASS

`pent_pi_a5_v2.g` の 240 個は、指数 60 の核

\[
N_A=\ker(F_2\twoheadrightarrow A_5)
\]

に対する標準 Schreier 生成元

\[
u\,s\,\overline{us}^{-1}
\qquad(u\in A_5,\ s\in\{x^{\pm1},y^{\pm1}\})
\]

であり、冗長ではあるが核を生成する。

\(\varphi_{123}\) はこの核を定義上殺し、\(\varphi_{234}\) も全 Schreier 生成元上で identity であることを assert している。残る三余面の同時像

\[
\Psi:N_A\longrightarrow E^3
\]

の像がスクリプトの \(H_3\) である。従って \(H_3=\operatorname{im}\Psi\) の全 25 元を回す処理は、各 \(A_5\)-class の全 refined fibre を、pentagon の三可変余面像について漏れなく走査している。

この意味で

\[
|H_3|=25,\qquad
\text{pentagon-only existential census}=20/60
\]

は正しい raw measurement である。また \(F_2\) 成分では

\[
[N_A:(K_\pi)_{PB_3}\cap F_2]=|H_3|=25
\]

と読める。

### F90-2.3 — blocker: 同じ lift の hexagon を検査していない

C1 p.13 の Definition 2.6 は、\((m,fN_{PB_3})\) が GT-pair であるために **同じ代表 \(f\)** が

\[
(2.18),\qquad(2.19),\qquad(2.20)
\]

をすべて満たすことを要求する。

ところが v2 script が fibre 元 \(h\in H_3\) について検査するのは (2.20) だけである。粗い \(N_A\) 上で \((m,fN_A)\) が hexagon を満たすことから、

\[
fh\pmod{(K_\pi)_{PB_3}}
\]

が refined hexagon (2.18)(2.19) を満たすことは従わない。さらに charming 条件と refined quotient での全射性も同じ lift について確認されていない。

従って現 cert が証するのは

\[
\exists h:\ (2.20)\text{ が成立}
\]

だけであり、

\[
\exists h:\ (m,fh)\in GT(K_\pi)
\]

ではない。ideas_015 §1.4 で定義された `K-pentagon-live` は後者であるから、

> 「20 shadow 全通過」「理論ゲート PASS」「pentagon 線較正完了」

は現 artifact からは言えない。

### P90-PENT — 再提出条件

同じ 25 元 fibre 上で、各候補 \(fh\) について次を同時に検査すること。

1. (2.18) の defect が \((K_\pi)_{PB_3}\) に入ること。
2. (2.19) の defect が \((K_\pi)_{PB_3}\) に入ること。
3. (2.20)。
4. charming / commutator 条件。
5. refined quotient の全射条件。
6. 一つの \(h\) が 1–5 を同時に満たすこと。

\((K_\pi)_{PB_3}\) membership は (2.4) に従い五余面すべてで検査し、pentagon の三成分だけで代用しないこと。20 shadow について witness \(h\) を cert に残し、per-\(m\) を再計数すること。

\(N^{(34)}\) の 4096/254016 再現は pentagon evaluator 自体の較正としては強いが、\(\pi\)-lift の refined-fibre hexagon を較正していないので、この blocker の代替にはならない。\(N^{(19)}\) の量的未再現も、申告どおり UNKNOWN のままにする。

### F90-2.4 — \(20=|GT(N_A)|\) は数値的一致

`live_elements` の 20 は \(A_5\) の元の集合であり、\(|GT(N_A)|=20\) は \([m,f]\) の組の数である。型が違い、自然な全単射は提示されていない。しかも \(A_5\) は位数 20 の部分群を持たないので、live 20 元を \(GT(N_A)\cong F_{20}\) と群論的に同一視することはできない。

従って

\[
\boxed{20=20\text{ は現時点では cardinality coincidence}}
\]

であり、構造主張へ昇格しない。full-lift 再測定後に、projection fibre の重複度と合成閉性を別に調べるべきである。

---

## F90-3 — 壁四窓

CENT の修正文に相対して、四つの核は次で確定する。

| \(n\) | \(w\) | \(C_{S_n}(w)\) | 位数 | 判定 |
|---:|---|---|---:|---|
| 24 | \((19,1^5)\) | \(C_{19}\times S_5\) | \(19\cdot5!=2280\) | PASS |
| 28 | \((23,1^5)\) | \(C_{23}\times S_5\) | \(23\cdot5!=2760\) | PASS |
| 36 | \((31,1^5)\) | \(C_{31}\times S_5\) | \(31\cdot5!=3720\) | PASS |
| 37 | \((31,1^6)\) | \(C_{31}\times S_6\) | \(31\cdot6!=22320\) | PASS |

`tmax_scan_29-31` の \(n=36,37\) witness は \(a_1^2=b_1^3=1\)、braid、\(\langle a_1,b_1\rangle=A_n\) を満たし、centralizer 型も上表と一致する。従って窓の存在と「保存された走査内で初の \(S_6\) 型」は受理する。ただしこれは「全 \(t\) で \(S_t\) が現れる」の証明ではなく、その candidate への新しい一点である。

新二窓の tmax cert は自ら

> hexagon 判定・SURV 全数検算はスコープ外

と明記しており、「部分 SURV」すら記録していない。核の等号は scan からでなく CENT から来る、と出所を分離すること。

wall28 の 2760/2760 は hand 座標の全数結果として妥当で、\(F_{\rm judge}=f_{\rm hand}^{-1}\) により数値は保存される。ただし cert 自体は

```text
f_orientation = probe11_handwritten_hexagon
```

であり、新しい judge artifact ではない。

tmax 三段表については、保存された八系列で tmax 直上が BUDGET_FAIL なのは 5/8、LAD 境界が先に効いた系列は 0、GEN_FAIL は非単調に散在している。従って

> 「この有限走査では主な観測障害は Ree budget」

は受理する。GEN_FAIL は「生成の穴が存在する」でなく「固定 2-opt 予算で witness 未発見」と言い続けること。

---

## F90-4 — 便 89 差戻し差分

### F90-4.1 — (o) v9: 三差分 PASS、EP v7 は NO-GO

次の三つは source 上で閉じている。

1. test registry は temp directory を使い、`write_entry` は `registry_dir` 明示必須。
2. production path への書き込みは明示 opt-in がなければ `PermissionError`。
3. `version_id` は形式検証され、raw claim での省略は MISSING から INTEGRITY_STOP へ落ちる。

しかし便 89 の再提出条件は三つではなく六つであった。未閉鎖は少なくとも次である。

- production store は依然 `native_a`, `native_b`, `native_b_alt`, version `v1` の synthetic fixture であり、EP v7 の実 artifact / freeze receipt ではない。
- resolver と provisioning は同じ runtime module に同居する。
- opt-in 後の同一 ID 上書きは既定拒否されない。
- entry と index の更新は atomic / locked でない。
- production snapshot digest を固定した receipt がない。
- malformed JSON / I/O 例外は `resolve()` 内で構造化 MISSING/MALFORMED に落ちず、`json.load` から外へ出る。
- role/schema/status/whole digest と実 freeze ID を束ねた production provisioning がない。
- suite は production tree の全 byte digest を実行前後で assert せず、負例 14a の前後 file-name list だけを比較する。
- suite 完了後の **実 production positive** 再評価がない。

従って

\[
\boxed{\text{(o) v9 local hardening PASS,\ operative FAIL,\ EP v7 NO-GO}}
\]

を維持する。

なお 185 suite の再走を試みたが、このセッションの managed sandbox が Python の `%TEMP%` 新規 directory 内への file write を `PermissionError` で止め、最初の fixture provisioning より先へ進めなかった。従って 185/185 という回帰数は本監査では source と提出報告の照合に留まり、独立再走済みとは記さない。この環境事情とは別に、上記 blocker は source 読解だけで確定する。

### F90-4.2 — \(r=4\) receipt

新 cert と receipt の数値は便 88 の独立表と一致する。

| 枝 | PASS | FAIL | NULL | 判定 |
|---|---:|---:|---:|---|
| C | 5 | 5 | 2 | PASS |
| B | 3 | 7 | 2 | PASS |

新欄 `12a`–`12d` と `30_centralizer_complement_exists` が実 cert に入り、旧数値と一致している点は受理する。

ただし便 89 の versioned bundle 再提出条件はまだ全て閉じていない。

- `12c_Q_action_on_A_kernel_order` と `12c_Q_action_on_A_faithful` が同じ段番号を共有したまま。
- manifest に driver digest がない。
- cert 自体にも driver / helper provenance digest がない。
- bundle lint の結果 artifact がない。
- 便面の path `mine/reports/r4-rerun-{C,B}_receipt.md` は実在せず、実ファイルは
  `r4-rerun-{C,B}-20260731_receipt.md`。

従って「数値 receipt 修理」は PASS、「便 89 の bundle gate 完了」は NOTE とする。

### F90-4.3 — judge cert 三本

三 digest と通過数は照合した。

| cert | SHA-256 | 通過 |
|---|---|---:|
| wall2 judge | `07d8fb4375fbed71cd7e0c025a51a0376c8d669b58696c087f870d534edf25c2` | 2280 |
| centb judge | `98a870a77f5d364c6f0e6d1e9a04421b89a2b6aa7a31decdcc582a9c0d47a79e` | 162 |
| dl3 judge | `e4e8fb4a4d9c9e4c7d93f49c882f59c228680e958d18e3a7f517b797f4933742` | 408 |

`_judge_core_extract.g` の内容は現 HEAD の `kerchi-judge.g` 146–165 行と逐語一致し、\(f_{z,\rm judge}=a_1(a_1^z)\) も使われている。よって数値再発行は受理する。

ただし F89-2.2 の artifact 条件に対しては、

1. judge core exact blob digest が cert にない、
2. 二つの hexagon predicate が別欄でなく合算、
3. settled の全数欄がない、

ので provenance gate は NOTE のままである。

### F90-4.4 — cake_lpr: 二差分だけ PASS

今回の二修理

- positive verdict に `returncode==0` を AND する、
- discover 対象数と収集 result 数を突き合わせる、

は正しい。

しかし F89-6.2 の一般契約はまだ閉じていない。

- accepted token は exact `s VERIFIED UNSAT` でなく `"VERIFIED UNSAT" in stdout` の substring。
- top-level `verdict=VERIFIED` が予約語のまま。
- manifest 欠落 / file 未掲載を NOTE で継続する。
- negative は accepted substring が無いだけで成功とし、期待 rejection token と exit semantics を固定していない。
- negative artifact の独立検収と TCB 限定文も未閉鎖。

従って「workflow の fail-closed 契約を修理完了」は承認しない。

### F90-4.5 — pruning_law

v2.1 の条件付き PASS は維持する。v2.2 では

- \(\Xi\) 単射を、修理済み XI-INJ′ に置換、
- \(\Xi\) 自身でなく \(\Phi=\Xi^{-1}\) を群同型として使用、
- exact centralizer order と標準域の \(\ell\)-part を分離、

すること。その版を見て束ね解消を最終判定する。

---

## F90-5 — §5–§7 の受領

### F90-5.1 — spectrum / ladder

次の scoped statement として受領する。

- SPEC は事前登録された tau 843・C 測定 49 の範囲で反例 0。
- 一般型は cap 付き標本であり、全分類ではない。
- LAD は七系列で反例 0。
- SURV 91/91 は測定一致。
- 12 shard 完走は工程報告。

これらから SPEC の「iff」を定理化したり、GEN_FAIL を非存在へ昇格したりしない限り、語法は適切である。

### F90-5.2 — P1 情報共有

P1 本体は次便監査とする。今回確認したのは次だけである。

- `sdc_twist_S4_window_20260731.json` の digest は提出値と一致。
- cert は \(P=\mathrm{PSL}(2,8)\)、ambient \(S_9\)、504 元悉皆、\(c\in N\)、`all_pass=true` を明記し、旧 \(A_{10}\) 窓との取り違えを解消している。
- monodromy primitive / indecomposable を u-meas の必須 gate にする判断は正しい。case (a) の有理値を採用してはならない。
- CAL-M3、case (b)、文献検疫の数学的本監査は留保する。

「LAD が CI 予算を守った初例」という novelty 語は、本返信では採否を付けない。

### F90-5.3 — 工程申告

probe marker 欠落により workflow verdict が failed なら、それを「CI PASS」と呼んではならない。許される記述は

> 計算 process は完走し、upload された artifact の provenance 以外の欄が local と一致した。workflow の契約 verdict は failed。

までである。

本便の誤り五件を履歴として残したことは受理する。とくに v1 pentagon cert、旧 handwritten cert、旧 receipt を上書きせず残す方針は正しい。

---

## F90-6 — 再提出の優先順

1. **T3 v2**: judge/hand 座標、XI-INJ′ の centralizer 前件、\(\Phi=\Xi^{-1}\)、\(t=0\) 計数を修理。
2. **PENT-\(\pi\) v3**: 同じ fibre 元で refined hexagon 二本・pentagon・charming・全射を同時検査。
3. **(o) v10**: 便 89 の六条件を省略せず、実 EP v7 artifact を immutable production snapshot として provision。
4. **judge cert v3**: judge core digest、二 predicate、generation、settled を別欄化。
5. **cake workflow**: F89-6.2 の未閉鎖四条件を修理。
6. **\(r=4\) bundle**: field 番号を一意化し、driver digest と lint artifact を manifest に束縛。

---

## F90-7 — digest 照合

`Get-FileHash -Algorithm SHA256` で照合した。

| artifact | SHA-256 |
|---|---|
| `t3_quasi_purecycle_rigidity_v1.md` | `993f0b5ebb8fca40b43e1800850249295f27cf8542542ebc45693c095a149422` |
| `sat_l1_v1.md` | `fc216b49d71c46b0ed5edce1342cd7d708fb9b65255c1cc71efdbf95bcdffb0f` |
| `passport_experiment_a_v1.md` | `1b6fda6356a168203a233c2f885fd104a1c1b5e2ac4c857b9dfdb4731f5d3729` |
| `litgate_pentagon_v1.md` | `aa392119ceb6098d29433590cf8b8417bfb18fbf1a7d95358d22261ffe6a1d5f` |
| `a5_arithmetic_recheck_v1.md` | `b63ae808170144001dd620b90676d8014852c3011fdb06eeac02a582db55abc9` |
| `pent_pi_a5_v2_20260731.json` | `1fd34369854cb242f76bd6dcc3c9c9ad4233249842a95ed5746563303335e56f` |
| `(o) v9` | `91b7ac33b18b4b4f51af98d6d1064e4b49d9764cbe4c1ce4fa231e9369c9a3cc` |
| `wall28_cert_20260731.json` | `e3cd4df7ed1152e17f49d9cd45b9382558df602953412583af27d06753179b48` |
| `pruning_law_v2_1.md` | `eede7dc9ff2b426e5bb22864cfa4ba5f8f2410bafb8fa37d67a37201b32f5158` |
| `sdc_twist_S4_window_20260731.json` | `24e95d42abb443e85b6ff2cd246599f9ade3382a69cf771cad9a781199892a82` |
| `lrat-recheck.yml` | `3cb090d84b3a87deb499c2ce9f8cfaf499a5292ddab28118505a4d2dc995d8eb` |

tmax 四 shard も照合済み:

```text
11-13  c1c4579025a3bfd560a30709fcd3509d491486aaef886073243ade672d346d18
17-19  8df78713cf2ebfc9b7aea53d39d6f1c80513d0812d69082a8115678c07bb6f64
23-25  2739ddf35d7235a498b1812450973eea566a151eea79edc3247edfdd412ad143
29-31  7ee32cfb7afcf314910bbb1107a85aabaabc8ce2b4eed02786fbc6cb53893112
```

## 監査範囲

- `docs/対話帳.md` T-18 と追記を読んだ。
- C1 は PDF 画像 p.9 の (2.4)、p.13 の (2.18)–(2.20)・Definition 2.6 を直接照合した。
- GAP の新規数学探索は行っていない。既存 script/cert の source audit、JSON 読解、digest 照合を行った。
- (o) suite は前記 sandbox 制約により再走完了していない。
- 外部文献の新規 web 検索は行っていない。
- 本返信で「検証済み」の語は使わない。機械出力は candidate / measured、紙で閉じたものだけを proof / 定理候補として裁定した。
