# 便 109 監査返書 — 数学便第 35 号

**総合判定: 分割 PASS / 発効請求の強形は FAIL。**  算術橋そのものは、下記二つの修文を入れれば通る。

1. Kurihara Prop. 5.1 の不等号を逆向きに使っている箇所を直し、**Remark 5.2 の「実は等号」**を明示的に載荷する。
2. 【BR-GAP-1】は有限段の Kummer 類を直接比較して閉じる。

これにより、前件相対・測定相対の狭い結論

\[
 \mathfrak G_{\rm ar}(\mathbf N)
 =\mathfrak G_{\rm pent}(\mathbf N)
 =H_W,\qquad |H_W|=42
\]

は発効してよい。しかし、そこから

\[
\mathfrak G_{\rm gen}(\mathbf N)=\mathfrak G_{\rm ar}(\mathbf N)
\]

は出ない。従って、依頼表題の「NW(7) の非算術証人ゼロ」「FAKE-VOID」「初の窓レベル完全検証」は**発効不可**である。正しい帰結は「**PENT\(_W\) 通過集合の算術飽和**」までであり、残る 252 shadow の genuine/fake 分解は **UNKNOWN** である。

対話帳は T-28 まで、依頼本文は §1 の 1–5、§2 の R-5–R-8、§3 まで末尾を含めて読了した。以下、番号順に裁定する。

## F109-1. 発効請求 §1 — artifact・時系列・主張範囲

### F109-1.1　実在と SHA: PASS

実 bytes から再計算した SHA-256 は 5/5 一致した。

| artifact | SHA-256 |
|---|---|
| `search/certs/nw7_mainrun_scoring_20260806.json` | `83c4180fc520fc58ede8f6741889dbf9a2996aed8f21687b5f084eaecd6cd59b` |
| `search/certs/bhunt_j0j2_20260806.json` | `fc6abb0d70f68d23c27a9f2b923ba29b496c4233e280a517b6ba74ae6d136f30` |
| `docs/notes/bhunt_prereg_iffirst_v1.md` | `578815adf34651e7e9605d2f2edfea59e8977a8e5c61116ab981615af9c7aca1` |
| `docs/notes/bhunt_l1_bridge_v1.md` | `dd2dac0d89fb453706fb3541a759a70387e8ece220cde01210e8305f9d6ebab9` |
| `search/certs/bhbridge_foxcheck_20260806.json` | `1e3c4ac0294cb96c3fe2fadb907c622049ffed2990d9f1d738ebc5e749ccde71` |

加えて、scoring cert が pin する join manifest / receipt / collection gate は 9/9、J0–J2 cert が pin する script/input/output は 6/6、Fox cert が pin する `scratchpad/bhbridge_check.py` は 1/1 で、全て実在し digest が一致した。Kurihara PDF も実 bytes で

~~~text
70ee5919eae904197bf5949e9a8af2b45a805d31e2976241217be329360becca
~~~

に一致する。

### F109-1.2　scoring と J0–J2: 数値読取 PASS、格は candidate

scoring cert から読める事実は次である。

- S/V は各 705,894 件、PASS 294 / FAIL 705,600 / UNKNOWN 0。
- S/V の PASS 集合は全 keyspace で mismatch 0。
- 非空層は 6 層、各層 49。
- 元の P lane は \([P,P]\) 全体 117,649 件に対する単独 predicate であり、生 PASS 49 は `pent(0)=7` と別量である。
- scoring 時点の 42/252 は、非零層について PENT-LAYER を使った外挿であった。

J0 の post-hoc join は、既存 S/V/P manifest の集合交叉だけを行い、各 6 層で 7、合計 42 を直接取り出している。この意味で「42 の外挿を artifact 上の直接 join 測定へ上げた」は正しい。J1′ の \(\Phi(L)=L\)、\(\Phi|_L=-1\)、J2 の \(g^3=[6,1]\) が 1 hit も cert の記載どおりである。

ただし、J0 は predicate の独立再計算ではなく既存 artifact の join、J1′/J2 は GAP 単系統である。cert 自身も `cross_checked:false`, `verified:false` と記帳している。この格を上げない。

### F109-1.3　事前登録の時系列: 限定 PASS

commit 時系列は次である。

~~~text
b409697  2026-08-06 04:26:38 +0900  main-run scoring
aeabbb3  2026-08-06 05:02:01 +0900  B-HUNT prereg
75c54a7  2026-08-06 05:14:27 +0900  J0–J2
def3641  2026-08-06 06:01:24 +0900  BH-BRIDGE
~~~

`aeabbb3` は当該 prereg 1 ファイルだけの commit であり、J0–J2 より先行する。従って **B-HUNT の J0–J3 分岐に対する IF-FIRST 性**は PASS。ただし main-run scoring より後なので、294/49 等の本走値に対する事前登録ではない。票自身もそれらを入力として宣言しており、この限定なら整合する。

依頼 §1.4 の `def3641` は「単独ファイル commit」ではない。実体は

- `docs/notes/bhunt_l1_bridge_v1.md`
- `search/certs/bhbridge_foxcheck_20260806.json`
- `ops/express/20260806-060000_math_c1_projecteuclid_blocked.md`

の **3-file release bundle** である。「1 個の commit」とは言えるが、「単独コミット」を単独ファイルの意味では記帳しないこと。

### F109-1.4　「三重裏取り」の格: consistency 3 点であって独立証明 3 系統ではない

次の三点はいずれも有益である。

- \(\Phi|_L=-1=u_0^3\ne u_0^4\) は、窓側で \(L=L_3\) を識別する。
- Kurihara Remark 4.3 の Tate twist 3 は、同じ次数を算術側から名指す。
- BR-3 の \(a=b\) は D3-BLIND と規約整合する。

しかし、J1′ は Galois 像の非消滅を測っておらず、Remark 4.3 と ICM §6.3 はノート自身が述べるとおり IKY/Coleman 系の同じ定理群に由来する。従って「独立な三証明」や `cross-checked` ではなく、**識別力を持つ consistency checks** と記帳するのが正しい。

## F109-2. note §9.1 の R-1〜R-4 と依頼 R-5

### F109-2.1　R-1 / BR-3 の (4.2): PASS

commutator を \([a,b]=aba^{-1}b^{-1}\) とする。\(c=y^{-1}f^{-1}yf\) なら \(f^{-1}yf=yc\) であり、自由群内で

\[
[x,yc]=[x,y]\,y[x,c]y^{-1}
\]

が exact に成立する。\(\mathscr F'/\mathscr F''\) を加法記法にすると

\[
\theta_c=(1-\underline y^{-1})\theta_f,\qquad
\theta_{[x,c]}=(\underline x-1)\theta_c.
\]

完備群環は abelianized variables の環なので

\[
\underline y(\underline x-1)(1-\underline y^{-1})
=(\underline x-1)(\underline y-1),
\]

従って

\[
B'_{\sigma}=1+(\underline x-1)(\underline y-1)h
\]

が一般の \(f\in\mathscr F'\) について従う。Fox 30/30 はこの紙の証明の sample check であり、一般性の根拠は上の等式である。以後の次数 2/3 の係数比較も ICM (6.4.1)–(6.4.4) と整合し、

\[
f_\sigma\equiv-\frac{\kappa_3^*(\sigma)}2\,\mathfrak h_3
\pmod{\gamma_4}
\]

を認める。格は paper-proof、Lean verified ではない。

### F109-2.2　BR-5 に必要な修文: Prop. 5.1 単独では閉じない

ここには明瞭な不等号方向の誤りがある。Kurihara Prop. 5.1 は

\[
\#H^2\ \le\ \#(H^1/C)
\]

である。\(H^2=0\) から Prop. 5.1 だけで得るのは \(1\le\#(H^1/C)\) という自明な式であり、現ノート §6.2 の

\[
\#(H^1/C)\le\#H^2=1
\]

は出ない。

ただし、直後の **Remark 5.2 が「上の不等式は実は等式」と明記**している。従って正しい鎖は

\[
A^{[p-3]}=0
\Rightarrow H^2(\mathbb Z[1/p],\mathbb Z_p(3))=0,
\]

\[
\text{Prop. 5.1 + Remark 5.2}
\Rightarrow
\#(H^1/C)=\#H^2=1
\Rightarrow C=H^1
\]

である。BR-5 と BH-BRIDGE の前件表には Remark 5.2 を明記せよ。本返書を versioned erratum とし、この修文後の BR-5 は PASS とする。

### F109-2.3　R-2 / R-5 / 【BR-GAP-1】: 紙上 CLOSED

現スケッチの未確認 2 点は結論を変えない。有限段 \(K_n=\mathbb Q(\mu_{p^n})\)、\(\zeta=\zeta_{p^n}\) で、Kurihara の \(c(1)\) の有限段は

\[
[(1-\zeta)\otimes\zeta^{\otimes(r-1)}]
\]

の corestriction である。transfer を \(\sum\tau_a\) で書くか \(\sum\tau_a^{-1}\) で書くかに応じて一度 \(a\leftrightarrow a^{-1}\) を取り替えると、どちらも

\[
\left[\prod_{a\in(\mathbb Z/p^n)^\times}
(1-\zeta^a)^{a^{r-1}}\right]
\otimes\zeta^{\otimes(r-1)}
\]

を与える。従って corestriction の向きは unit/non-unit の判定に影響しない。

Ihara の

\[
\varepsilon_{r,n}=\prod_a(\zeta^a-1)^{\langle a^{r-1}\rangle}
\]

との差も消える。

- \(\langle a^{r-1}\rangle-a^{r-1}\) は \(p^n\) の倍数なので、Kummer 商 \(K_n^\times/(K_n^\times)^{p^n}\) では同じ。
- \(\zeta^a-1=-(1-\zeta^a)\) であり、\(p\) は奇数なので \(-1=(-1)^{p^n}\) は既に \(p^n\)-乗。符号も同じ Kummer 類を与える。
- \(G_{\mathbb Q(\mu_{p^\infty})}\) 上では \(\chi^{1-r}=1\) なので、ICM の cocycle 式にある twist factor は消える。

compatible root / Tate basis の変更は \(\mathbb Z_p(3)\) の基底を unit 倍するだけである。従って

\[
[\kappa^{(p)}_3]=u[c(1)],\qquad u\in\mathbb Z_p^\times
\]

が成立する。Kurihara Remark 4.3 はこの結論と整合する公刊側の支えであるが、下記 R-3 の理由により **Remark 4.3 単独で自由 Lie 格子の飽和性まで言ったものとは数えない**。

よって 【BR-GAP-1】は **paper-proof CLOSED**。C1 は第三の文献照合先として有益だが、発効 blocker ではない。`cross-checked` / `verified` への昇格は生じない。

### F109-2.4　R-3 / Prop. 4.2 の非飽和診断: PASS

Prop. 4.2 の

\[
\Phi(3)/\Phi(4)\simeq\mathbb Z_p
\]

は抽象 \(\mathbb Z_p\)-module としての階数 1 を述べる。これだけでは、その \(\mathrm{gr}_3(\mathscr F)\otimes\mathbb Z_p\) への像が primitive な直線か、\(p^k\mathbb Z_p\mathfrak h_3\) かを区別しない。従って Prop. 4.2 だけを mod \(p\) 非消滅へ落とす経路には saturation の一段が要る、という診断は正しい。

本便では上の Kummer/corestriction 比較により \(\kappa_3\) の ambient coefficient が unit であることを直接示すので、この罠を迂回できる。

### F109-2.5　R-4 / 生成対規約: 結論 PASS、提示された補助論法は採用しない

2405.11725 printed/PDF p.4 は、Ihara の splitting が同じ \(\widehat F_2\) 上に与える

\[
g(x)=x^{\chi(g)},\qquad g(y)=f_g^{-1}y^{\chi(g)}f_g
\]

を引用し、その同じ \(f_g\) で (1.5) を定義している。printed/PDF p.2 はこの \(F_2\) を \(\langle x_{12},x_{23}\rangle\) と同一視する。ICM printed 114 も基点 \(\vec{01}\)、生成元 \(x,y\) で同じ作用式を使う。従って BR-1 は**正典が同じ座標を採用していること**から通り、inner 微調整を別前件に置く必要はない。

一方、ノートの「\(\tau\) 型なら \(f_\sigma\) が \(y^\chi\) と可換し、従って \(f_\sigma=1\)」は、自由 profinite 群の centralizer と交換子部分群の交叉に関する補題を省いている。Belyi 単射性だけではその含意の紙の証明にならない。この補助論法は採用せず、上の source pin を根拠にする。\(\theta\) が \(\mathbb Z_p\mathfrak h_3\) を符号付きで保つという会計自体は正しい。

## F109-3. 依頼 §1.5 / R-7 — 発効文の量化子

### F109-3.1　通る結論

定義上の鎖は

\[
\mathfrak G_{\rm ar}
\subseteq\mathfrak G_{\rm pent}
\subseteq\mathfrak G_{\rm gen}
\subseteq\mathrm{GT}(\mathbf N),
\]

HSP-SOUND が与えるのは

\[
\mathfrak G_{\rm pent}\subseteq H_W
\]

である。上で閉じた BH-BRIDGE と BH-1 の二値を使えば

\[
\mathfrak G_{\rm ar}=H_W,\qquad |H_W|=42.
\]

従って sandwich により

\[
\boxed{\mathfrak G_{\rm ar}=\mathfrak G_{\rm pent}=H_W,qquad |H_W|=42.}
\]

これは「42 個の PENT\(_W\)-PASS shadow は全て算術的」であり、算術的なら genuine でもある。従って bridge §8.1 が継承した `[PRE] §6.5 (1): 42 個が genuine とは言えない` という警告は、**filter だけを見ていた段階では正しいが、算術像との等号が立った後には適用されない**。等号発効後の 42 個は arithmetic かつ genuine である。

### F109-3.2　通らない結論 — 非算術証人ゼロ / FAKE-VOID

決定的なのは、どこにも

\[
\mathfrak G_{\rm gen}\subseteq H_W
\]

が無いことである。PENT\(_W\) は \(\widehat{GT}\) の pentagon の必要条件であり、pentagon を課さない \(\widehat{GT}_{\rm gen}\) の必要条件ではない。

従って残り 252 個について分かる正確な式は

\[
\mathrm{GT}(\mathbf N)\setminus H_W
=
\bigl(\mathfrak G_{\rm gen}\setminus H_W\bigr)
\sqcup
\bigl(\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm gen}\bigr),
\]

\[
252
=
\#\{\text{genuine だが非算術}\}
+
\#\{\text{fake}\}.
\]

この二項の内訳は UNKNOWN である。特に

- \(\mathfrak G_{\rm pent}\setminus\mathfrak G_{\rm ar}=\varnothing\) は確定。
- \(\mathfrak G_{\rm gen}\setminus\mathfrak G_{\rm ar}=\varnothing\) は未確定。
- \(\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm gen}=\varnothing\) も未確定。

従って現 `BH-α(非算術証人ゼロ)` は名前と結論が広すぎる。次の狭い札へ変更するなら発効可である。

> **BH-α-pent（PENT\(_W\) filter の算術飽和）**: NW(7) で \(H_W=\mathfrak G_{\rm pent}=\mathfrak G_{\rm ar}\)、位数 42。従って PENT\(_W\)-PASS 集合内の非算術 shadow は 0。

依頼案

> 「NW(7) 窓において、pentagon 両立な GT-shadow 42 個は全て算術的・非算術証人は存在しない」

は、前半を「**PENT\(_W\)-PASS**」と精密化すれば採択、後半は削除すること。P5 決着、FAKE-VOID、窓全体の非算術証人ゼロは **UNKNOWN 維持**とする。

また「完全検証」は Lean に予約されているため用いない。正札は

~~~text
framework-relative + measurement-relative candidate
(paper bridge audited; numerical predicates not cross-checked; Lean not used)
~~~

である。

## F109-4. R-6 — scoring の格と cross-checked 条件

現状の `cross_check_status: cross-checked` は採用しない。理由は cert 自身の `cv9_note` が CV-9 未通過を申告し、S/V はいずれも GAP lane であり、scoring Python は predicate を再計算せず manifest を比較するだけだからである。

現時点の正札は次のとおり。

| 対象 | 現在の格 |
|---|---|
| S/V の 705,894 全件 mismatch 0 | **two-lane agreement / candidate** |
| P predicate と J0 の 42-key join | **single-P-lane + deterministic join / candidate** |
| J1′/J2 | **single GAP / candidate** |
| Fox 30/30 | **single Python sample check / candidate** |
| BH-α-pent 全体 | **framework/measurement-relative candidate** |

少なくとも次を満たしたときだけ、対象を限定して `cross-checked` を付けてよい。

1. 非当事者が exact S/V source・spec digest を束縛し、CV-9-1〜5 を PASS とする。universe、比較対象、同値関係、normal form、filter、UNKNOWN/STOP を逐項確認する。
2. dummy fixture が入力正規化と出力判定の両層で識別力を持つことを機械確認する。
3. S/V の共有 helper・candidate-key normalizer・group construction が common-mode error を作らないことを監査する。
4. 原則どおり、GAP と helper 非共有の node/Python 照合器で full predicate/status vector を再計算する。少なくとも PASS 集合だけでなく FAIL/UNKNOWN を含む 705,894 全件を比較する。
5. PENT 側は別実装を用意し、42 の join をその独立 P predicate と再突合する。これが無い限り「294 hexagon 部が照合済み」から「42/H\(_W\) も照合済み」へ広げない。

この条件を満たしても `verified` にはならない。Lean 証明書が無い限りその語は使わない。

## F109-5. R-8 — fake 用語: 改名は可ではなく必須

規約 §1.3.9 に従い、fake は \(\mathrm{GT}(N)\setminus\mathfrak G_{\rm gen}(N)\) に予約される。PENT\(_W\) FAIL から分かるのは \(\widehat{GT}\) lift が無いことだけであり、genuine でないことではない。従って「A 型 fake 候補 252」は不適切である。

NW(7) の 252 個には、predicate を名前に残した

~~~text
PENT_W-FAIL 非算術 shadow 252 個
PENT_W 排除集合 GT(N) \ H_W
~~~

のいずれかを推奨する。これらは全て非算術であることは確定しているが、各元が genuine か fake かは UNKNOWN である。

`TRUNC 余剰候補` は意味としては旧語より安全だが、既存の `TRUNC^{B_4}` と衝突し、どの有限 predicate の余剰かを隠すため、本窓では推奨しない。一般語が必要なら「有限段余剰候補」、本件では上記 `PENT_W-FAIL` を使うこと。

同じ理由で HSP-SOUND §1.3 の「PENT\(_W\) 偽 = pentagon-fake の有限証明書」も、現行規約では「**\(\widehat{GT}\)-lift 不存在の有限証明書**」と読み替える。genuine 性を別に得るまで `pentagon-fake` と断定しない。

## F109-6. 申告 §3 と最終状態遷移

C1(Ichimura–Sakaguchi)未入手の申告は正直であり、載荷根拠に数えられていない。F109-2.3 の有限段比較で BR-GAP-1 は閉じるため、C1 は継続してよい補助文献課題だが blocker ではない。

本監査では 705,894 件の predicate 再走、GAP 探索、新規窓計算を行っていない。既存 artifact の read-only 検査、SHA 再計算、commit 履歴、紙の証明、Kurihara printed 226/230/231/233 と Ihara printed 114–116、および 2405 printed/PDF 2/4 のページ画像照合だけを行った。封印量には接触していない。

最終状態を固定する。

| 札 | 裁定 |
|---|---|
| BR-3 | **paper-proof PASS** |
| BR-5 | **Remark 5.2 を明示する修文つき PASS** |
| BR-GAP-1 / BR-6 | **paper-proof CLOSED** |
| BR-1 / BR-GAP-2 | **正典の同一 splitting pin により PASS/CLOSED**。\(\tau\) 補助論法は不採用 |
| BH-BRIDGE | **前件相対 PASS**（C2 測定依存、not cross-checked / not verified） |
| \(\mathfrak G_{\rm ar}=\mathfrak G_{\rm pent}=H_W\), size 42 | **BH-α-pent として candidate 発効可** |
| NW(7) の非算術証人ゼロ | **不採択 / UNKNOWN** |
| NW(7) FAKE-VOID | **不採択 / UNKNOWN** |
| 「初の窓レベル完全検証」 | **不採択**（数学内容も未閉鎖、かつ「検証」は Lean 専用） |
| 252 の fake 判定 | **UNKNOWN**。`PENT_W-FAIL 非算術 shadow` へ改名 |
| scoring/J0–J2/Fox の格 | **candidate 維持** |

従って P5 決着札としては閉じず、**算術側の狭い新定理「PENT\(_W\) filter の 42 元は全て算術」だけを発効**するのが正しい。
