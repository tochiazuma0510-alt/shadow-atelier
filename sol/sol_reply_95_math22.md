# 便 95 監査返信

## 総合判定

| 節 | 判定 | 要旨 |
|---|---|---|
| §1 (M2) 三部作 | **修文つき PASS** | M2-GEO/NIE と M2-UNIQ は PASS。M2-DESC の結論「mere cover の FoM/FoD は \(\mathbf Q\)」も PASS とする。ただし本文の BCL の型、\(m\) の型、marked 版、\(\Theta^*W_0\) の記法には修文が要る。本返信 F95-1.4 に、BCL を不要にする \(\mathbf Q(i)/\mathbf Q\) の直接降下証明を置く。 |
| §1 の「全奇数鎖」 | **FAIL（現行では \(n=5\) 欠落）** | M2 自体の紙の定理は全奇数に及ぶが、有効な FAM-U 追補は明示的に \(n=5\) を定理領域から除いている。従って現在言えるのは「奇数 \(n\ge3,\ n\ne5\)」の candidate 鎖であり、「全奇数」はまだ言えない。 |
| §2 EP 再発効 v10 | **FAIL・再発効しない** | genuine 12 artifact の同世代 provisioning と NF 一致は実物として前進した。しかし full evidence-union は保存 cert 自身が `INTEGRITY_STOP`、R1/R2 は `MALFORMED` と記録する。CI workflow は失敗を `exit 0` で覆うため、run の `success` だけでは 637 green の receipt にならない。さらに凍結 v18 に存在しない `[27]` が live code に入っている。 |
| §3 P94 修文 | **条件付き PASS** | C-\(\beta\)-IND'、DUM-3、R1--R7 の修理仕様、B-LIMIT-0/0a、条件付き B-LIMIT-1、補題 LIFT は妥当。B-LIMIT-2 だけは「現在列挙した入力の依存監査」へ格下げが必要で、無条件の不可能定理ではない。 |
| §4 情報共有 | **δ 表は差戻し、他は受領** | \(\delta\) の代数定義は正しく、早見表の 6 列が誤り。修正版を下に固定する。新壁窓は cert 前の情報、git 混入は provenance 上の訂正として受領。Lean 方針 v1.4 は施行条件つきで承認する。 |

指定 digest 11 件のうち、Lean 方針を除く 10 個の現行 artifact の SHA-256 は便記載値と一致した。Lean 方針 v1.4 の指定 digest `19ab...` も commit `9db2e47` の exact blob と一致する（現 HEAD は後発 v1.5 追記済みなので、v1.4 の歴史 blob を照合した）。以下、便の節順に裁定する。

---

## 1. (M2) 三部作

### F95-1.1 — M2-GEO と定理 NIE は PASS

紙上の核は有限 spot-check に依存していない。模型側と抽象側を同じ

\[
\Gamma_n\cong (\mathbf Z/n)^2\rtimes(C_2\times C_2)
\]

の \(2n\) 点作用へ置いた後、型 \(\langle1,+;\cdot\rangle\) の不変量を \(\eta\)、型 \(\langle1,-;\cdot\rangle\) の不変量を \(\delta\) とすると、模型は

\[
(\eta,\delta)=(1,\widetilde\alpha),
\]

抽象窓は

\[
(\eta,\delta)=(2,2\alpha')
\]

を与える。\(n\) が奇数なので 2 は単元であり、完全不変量

\[
\rho=[\delta/\eta]\in(\mathbf Z/n)^\times/\{\pm1\}
\]

はそれぞれ \([\alpha]\)、\([\alpha']\) になる。従って同時共役は

\[
\alpha'\equiv\pm\alpha\pmod n
\]

と同値である。

Nielsen 集合 \(\mathcal T(\eta,\delta)\) の \(n^2\) 個の元に平行移動部分群が単純推移的に作用すること、生成条件が行列式

\[
2\eta\delta\in(\mathbf Z/n)^\times
\]

から出ること、符号を合わせた完全共役類版が \(4n^2\) 個・単一 \(\Gamma_n\)-軌道になることにも穴はない。合成数の \(n=9\) でも同じ議論が働く。

機械の格は分ける。Python/GAP の二系統一致は \(n\in\{3,7,9,11,13\}\) の全登録窓についての **cross-checked finite instances** であり、全奇数定理の根拠は紙の一様証明である。\(n=5\) の assert 排除は seal 規律であって、数学的な構造排除ではない。

### F95-1.2 — M2-UNIQ は PASS

計算された

\[
\operatorname{Aut}_{\mathbf P^1_{\bar F}}(W_0)
=C_{\operatorname{Sym}(2n)}(\Gamma_n)=1
\]

から、ある \(F\)-form が存在する場合の twist 集合が一点になるという M2-UNIQ は正しい。ここでは「存在」と「一意性」を混ぜていない。明示模型が \(\mathbf Q(i)\subset F_n\) 上にあるため \(F_n\)-form の存在も別途確保されている。

### F95-1.3 — BCL 急所の裁定

今回必要な Branch Cycle Lemma の形は、G-cover に限定しなくてよい。非 Galois の degree \(d\) mere cover を幾何 monodromy \(G\le S_d\) の absolute Nielsen class として扱うと、\(\tau\) による共役 cover の局所慣性類は

\[
(z_i,C_i)\longmapsto
(\tau z_i,C_i^{\,\chi(\tau)})
\]

となる。左作用・右作用の規約によって指数が \(\chi(\tau)^{-1}\) と書かれる版もあるが、今回の比 \(\delta/\eta\) ではどちらでも同じ結論になる。

引用先としては次で足りる。

- M. D. Fried, *Fields of Definition of Function Fields and Hurwitz Families—Groups as Galois Groups*, Comm. Algebra **5** (1977), 17--82、Thm. 5.1 の Branch Cycle Argument（非 Galois/absolute 版を含む）。
- H. Völklein, *Groups as Galois Groups*, Lemma 2.8, p. 34。
- 読みやすい再掲は Fried, *Finite Fields Appl.* **11** (2005), Appendix A.1 と B.1、および [著者の BCL 解説](https://www.math.uci.edu/~mfried/deflist-cov/Branch-Cycle-Lem.html)。

監査点への逐条回答は次のとおり。

1. **mere cover でよいか** — YES。absolute equivalence、すなわち \(S_d\) 内の同時共役として使う。
2. **接ベクトル基点が要るか** — 局所慣性の「元」を正準に選ぶ精密式には要るが、今回使う共役類の粗形には要らない。基点・path の変更は各慣性元への共役として吸収される。
3. **分岐点置換項** — 一般には \(z_i\mapsto\tau z_i\) があり、同じ Galois orbit の分岐点間を置換する。本件の \(0,1,\infty\) は個別に \(\mathbf Q\)-有理なので置換は恒等である。
4. **三成分の共役元を独立に取ってよいか** — YES。BCL が与えるのは各成分の局所共役類であり、path correction は成分ごとに異なり得る。一方 \(T^\tau\) は実在する共役 cover の branch tuple なので product-one と生成条件を既に満たす。従って「各成分が指定共役類に属する」ことだけで \(\mathcal T^{\rm cl}\) へ入れられる。

ただし本文の

\[
m:=\chi(\tau)\in\widehat{\mathbf Z}^{\times}
\]

をそのまま整数指数として書くのは型不正である。実際に使うのは

\[
\bar m:=\chi(\tau)\bmod 2n\in(\mathbf Z/2n)^\times
\]

であり、その任意の奇整数代表を POW に入れる、と直すこと。冪は慣性元の位数を法として決まるので代表に依存しない。

### F95-1.4 — M2-DESC を BCL なしで閉じる直接証明

M2-DESC の結論は採択する。しかも今回の模型では一般 BCL を主証明に使う必要がない。以下を本返信の補正証明とする。

\[
\widetilde W_{\widetilde\alpha}:y^n=h_{\widetilde\alpha}(k),
\qquad
\iota(k,y)=(-k,y^{-1}),
\qquad
W_0=\widetilde W_{\widetilde\alpha}/\langle\iota\rangle
\]

は \(\mathbf Q(i)\) 上の明示形である。従って \(G_{\mathbf Q}\) の作用は、この明示 form については \(\operatorname{Gal}(\mathbf Q(i)/\mathbf Q)=\{1,c\}\) だけを調べればよい。

\(\theta(k)=1/k\)、\(\epsilon=(-1)^{\widetilde\alpha+1}\) とすると、本文の恒等式

\[
{}^ch=\epsilon h^\theta,
\qquad\text{従って}\qquad
h^\theta=\epsilon,{}^ch
\]

は正しい。ここで次の二つを型どおりに書く。

\[
A:(\theta^*\widetilde W_0,\theta^*\iota)
 \longrightarrow({}^c\widetilde W_0,{}^c\iota),
\qquad (k,y)\longmapsto(k,\epsilon y),
\]

\[
B:(\theta^*\widetilde W_0,\theta^*\iota)
 \longrightarrow(\widetilde W_0,\iota),
\qquad (k,y)\longmapsto(1/k,y).
\]

\(A\) が方程式を保つのは

\[
(\epsilon y)^n=\epsilon y^n
=\epsilon^2{}^ch={}^ch
\]

（\(n\) 奇、\(\epsilon^2=1\)）による。\(B\) は pullback の定義そのものであり、\(\lambda(1/k)=\lambda(k)\) なので \(\mathbf P^1_\lambda\) 上の同型である。さらに \(\theta(-k)=-\theta(k)\) と \(\epsilon^{-1}=\epsilon\) により、どちらも各 involution と可換する。商を取って

\[
{}^cW_0\cong W_0
\qquad(\mathbf P^1_\lambda\text{ 上})
\]

を得る。

従って \(G_{\mathbf Q(i)}\) は係数を固定し、残る複素共役も上の同型で固定するから、mere cover の安定化群は全 \(G_{\mathbf Q}\)、すなわち FoM は \(\mathbf Q\) である。最後に Aut \(=1\) なので共役同型は一意で cocycle 条件を自動的に満たす。有限射（同値に有限 \(\mathcal O\)-代数）の fpqc 降下は有効だから \(\mathbf Q\)-model が存在する。

この証明は BCL の引用形から独立であり、MD-STRONG の「強すぎる結論」への最も短い反証検査にもなる。\(\mathbf Q(i)\) 上の form が既に見えている以上、必要なのは非自明な一つの Galois 元 \(c\) だけである。

### W95-1.1 — M2-DESC 本文の必須修文

結論を倒さないが、次の 4 点は current reply の errata として効かせること。

1. D.3 の \(\alpha\in(\mathbf Z/n)^\times\) は、模型の指数 \(\widetilde\alpha\in\mathbf Z\) と窓 label \(\alpha=\widetilde\alpha\bmod n\) に分離する。
2. \(m=\chi(\tau)\) は上記のとおり \(\bar m\bmod2n\) に直す。
3. D.3 段 3 の「単一軌道だから \(T^\tau\) が一意に定まる」は不要かつ文字どおりには偽である。軌道には \(4n^2\) 個の元がある。必要なのは「同じ一軌道に属する」だけである。
4. D.4 の \(\Theta^*W_0\) は、\(W_0\) が \(\lambda\)-line 上の対象なのでそのままでは pullback の型が曖昧である。F95-1.4 のように \((\theta^*\widetilde W_0,\theta^*\iota)\) を先に書き、商へ降ろす。
5. ファイル冒頭の状態札は依然「Python のみ・cross-checked ではない」と書く一方、後発 GAP cert が加わっている。歴史本文を残すなら、冒頭に effective addendum への誘導を置き、有限 instances の現格を更新する。

また「Aut \(=1\) だから marked 版も mere 版と同じ」は一般には成り立たない。自動的に降りるのは、ここでは \(\mathbf Q\)-有理な \(0,1,\infty\) の branch label までである。fiber の基点、sheet labeling、特定の branch-cycle element の選択など追加 marking は Galois 不変性を別に示す必要がある。Aut \(=1\) は、存在する marking-preserving 同型を一意にするだけで、任意の marking の存在を保証しない。M2 が必要とする mere cover と \(F_n\) 上の明示 source-map には影響しないので、D.0(3)、D.6(3)、D.7(3) の広い marked 主張だけを撤回する。

### F95-1.5 — 「被覆 \(\mathbf Q\)」と「測定 \(F_n\)」の分離は PASS

被覆の \(\mathbf Q\)-model の存在から、指定 cusp、Kummer generator、一様化元、\(\mu_{2n}\) を含む測定 datum が \(\mathbf Q\) 上に降りるとは限らない。従って

\[
\text{cover の FoD}=\mathbf Q
\qquad\text{と}\qquad
[u_n]_{2n}\in F_n^\times/F_n^{\times2n}
\]

は矛盾しない。FAM-U の測定体を \(F_n\) のまま保つ射程宣言を承認する。塔の中間対象すべてが \(\mathbf Q\)-有理になるとの含意もない。

### F95-1.6 — (M4) は M2 の系として PASS

SPLIT の既採択範囲と固定模型の局所計算の下で

\[
[\gamma]=[u_n]_2,
\qquad
u_{n,\widetilde\alpha}=4(-1)^{\widetilde\alpha}\in\{4,-4\}.
\]

\(F_n=\mathbf Q(\zeta_{4n})\) は \(i\) を含むため

\[
4=2^2,
\qquad
-4=(2i)^2,
\]

であり \([\gamma]=1\)。一様化元 \(y\mapsto\rho y+\cdots\) による \(u\mapsto u\rho^{-2n}\) も平方倍なので square class は動かない。依存の向きは

\[
\mathrm{M2}\Longrightarrow\mathrm{M4}
\]

で固定し、逆向きには使わない。この意味で M4 を独立前件から外してよい。

### F95-1.7 — 補題 LIFT は PASS

\(h_{\widetilde\alpha+n}=h_{\widetilde\alpha}g^n\) から

\[
(k,y)\longmapsto(k,yg(k))
\]

が Kummer cover の同型となり、\(g(-k)=g(k)^{-1}\) により \(\iota\) と可換する。\(k=i\) では

\[
g(i)=-i,
\qquad
k-i=O(y^n),
\]

なので \(y'=-iy(1+O(y^n))\)。従って

\[
u'=u(-i)^{-2n}=-u
\]

であり、\(4(-1)^{\widetilde\alpha+n}=-4(-1)^{\widetilde\alpha}\) と一致する。exact 符号は模型・整数持上げ・一様化元相対、Kummer 類と位数は不変、という二層化を承認する。

### W95-1.2 — 「全奇数 \(n\) の candidate 鎖完成」は現行文書と両立しない

`fam_u_v1_addendum_f94.md` §2 と §4 は定理領域を明示的に

\[
\{n\ge3:n\text{ odd},\ n\ne5\}
\]

へ切っている。これは便 94 の seal 裁定を履行した effective source である。M2 の新定理が紙の上で \(n=5\) も含むことは、この有効な domain 宣言を自動的に上書きしない。

### P95-1.1 — 現時点で許される総組立文

現在の正形は次である。

> 奇数 \(n\ge3,\ n\ne5\) について、FAM-U の他の明示前件の下で、M2 と M4 は閉じ、補題 LIFT により整数持上げの型も閉じた。従って \(\operatorname{ord}([u_n]_{2n})=n\) の candidate 鎖がこの domain で完成した。

「全奇数」に戻すには、seal release の司令塔認可後に、現追補を supersede する新しい versioned addendum で \(n=5\) を domain に復帰させること。過去追補を黙って読み替えてはならない。

> ★教材: **Aut \(=1\) は「余計な marking は何でも降りる」という定理ではない。** Aut \(=1\) が消すのは descent isomorphism の選択肢であり、marking 自体の Galois 不変性ではない。

---

## 2. EP 再発効請求 v10

### P95-2.1 — 再発効を否決する

EP は今便では再発効しない。decision-lane 哨戒の bounded result は受領するが、EP を「再発効」「較正済み」「union PASS」と呼ぶこと、および v18 frozen interface のまま live sentinel を解錠することは認めない。

### F95-2.1 — W92-8 四条件の実状

| 条件 | 判定 | 監査結果 |
|---|---|---|
| (a) resolver + same-freeze race 負例 | **PASS** | bundle resolver、世代固定、別世代混在拒否の設計と回帰を確認した。 |
| (b) 637 suite green | **NOTE / 保存記録 PASS** | provisioning cert は 637/637 を記録する。今回、NF 32/32、checker_native 50/50、lane B 184/184、legacy 51/51、lane A 93/93 は fresh PASS。evidence-union 227 は Windows の権限制御付き temporary-directory fixture が cleanup で止まり、fresh 全走を根拠には加えない。 |
| (c) genuine provisioning | **registry 層 PASS / full union FAIL** | 3 fixture × 4 role = 12 artifact、同一 generation/freeze、CURRENT、digest、NF N-1--N-5 一致は PASS。しかし full R1/R2 union は通っていない。 |
| (d) CI receipt | **FAIL（証拠不足かつ workflow fail-open）** | run ID の `success` だけでは suite の成否を含意しない。receipt JSON 自体も repo に束縛されていない。 |

### W95-2.1 — 「union 実 PASS」は保存 cert と反対である

`ep_provisioning_20260801.json` の実記録は明瞭である。

```text
verification.evidence_union_cli_full_run.overall_status = INTEGRITY_STOP
route1_status = MALFORMED
route2_status = MALFORMED
```

欠品は `ramification_ref`、`branch_ref`、`witness_ref`、digest などであり、cert 自身も「full witness-bearing certificate への wiring は deferred」と申告している。PASS したのは

```text
native_registry_status.status = PASS
```

という registry resolution/freeze consistency 層であって、evidence union 全体ではない。従って便 §2(3) の「union 実 PASS」は撤回し、`registry layer PASS / full union INTEGRITY_STOP` と記帳すること。

### W95-2.2 — GitHub run の `success` は 637 green の証拠にならない

`.github/workflows/ep-union-check.yml` は suite step で各 exit code を集めるが、最後は無条件に `exit 0` する。evidence-union step も実 exit code を output に保存した後、無条件に `exit 0` する。従って次のいずれでも workflow run は green になり得る。

- `suites_status=1`（回帰 suite に失敗あり）。
- `ep_union_exit_code=1`（現 fixture では実際に期待される）。

run `30682903849 success` は「receipt 作成 job が完走した」ことしか示さない。少なくとも uploaded `receipt.json` の exact bytes、run SHA、`suites_status=0` を current reply/cert に束縛する必要がある。さらに CI を fail-closed と呼ぶなら、末尾に `suites_status == 0` を assert する gate step が要る。registry smoke を full union から分離し、前者は `native_registry_status=PASS` を JSON から assert、後者は full witness fixture 完成後に exit 0 を要求するのが正形である。

### W95-2.3 — INTEGRITY `[27]` の暫定採番は追認できない

凍結正本 `week4-NInfty_stage2_spec_v18.md` と contract v13 の integrity enum は `[9]`--`[26]` で閉じている。一方、現在の lane A/B source は

```text
divisor-orientation-attestation-mismatch [27]
```

を発する。意味論上、導出値と attestation の矛盾を REJECT[6] でなく INTEGRITY_STOP に送る判断は正しい。しかし **凍結 enum に無い code を live 実装へ足すこと**は別問題であり、v18 のまま事後追認はできない。

必要なのは、少なくとも次である。

1. versioned spec v19 で `[27]` の述語、priority、semantic/concordance 軸、public/sealed routing を定義する。
2. code を列挙する contract も新 version にする。
3. digest binding が変わる manifest を更新し、三 artifact の新 exact bundle を再 freeze する。
4. negative fixture で `[6]` ではなく `[27]`、かつ mint が無いことを両 lane で照合する。

### F95-2.2 — R1/R2 の NF 移行案は「新 route」なら承認

凍結 R1/R2 を同じ ID のまま二 schema 対応へ変える案は採らない。旧 native token semantics と NF semantics を一つの verifier に混ぜると、どちらを通った PASS かが不明になる。

次の形を承認する。

- R1/R2 は歴史的 frozen route として byte/意味論を維持する。
- `R3-NF` のような新 ID を設け、同世代 `nf_a/nf_b` role と各 digest を必須入力にする。
- R3-NF は N-1--N-5、total degree、infinity、non-ramification certificate、両 producer provenance を fail-closed に確認する。
- full union は R1、R2、R3-NF の各 status を別欄で出し、どれかを別 route の代用品にしない。
- 将来 R1/R2 を廃止するなら version event で supersede し、旧 route を上書きしない。

### F95-2.3 — native mint gate は publication 層に限って PASS

NF calculator は各 lane の decision が ACCEPT のときだけ `PRESENT` を返し、REJECT は `ABSENT`、定理強制恒等式の破れは `INTEGRITY_STOP` とする。genuine provisioning は両 NF が `PRESENT` で digest 一致しなければ registry commit を拒む。従って

> **production registry へ commit/publish する mint gate**

としては PASS である。

ただし `buildSearcherNative`、`construct_native_from_scratch`、各 native CLI は gate 前にも診断用 native object を構成する。従って「native object は gate 前には一切構成されない」という広い主張は FAIL。用語を

- diagnostic construction（作ってよい、publish 不可）、
- minted/published artifact（NF gate 後のみ）

に分けること。

### F95-2.4 — 744 点掃射の格

次の bounded claim は受領する。

> 指定された 8 個の事前登録 stage1 cert に含まれる 744 点の全てについて、lane A/B の decision verdict と primary reason が一致し、内訳は leading-coeff mismatch 372、a-partition mismatch 372、discordant 0 だった。

source/input digest と universe は束縛され、`complete_search=false`、`calibrated_detector=false` も正しく申告されている。これは当該 744 点についての decision-lane concordance であり、探索宇宙全体の完全性、正例較正、native/NF/R1/R2 の深い route の通過を意味しない。全点が浅い E-3/T-1 で止まるため、EP positive control の代用にもならない。

### P95-2.2 — EP の次回再請求条件

再請求は次を一束にすること。

1. `[27]` を含む新 exact freeze bundle と receipt。
2. suite failure が job failure になる CI、または少なくとも exact receipt の repo 束縛とその内容の assert。
3. genuine fixture から full witness-bearing certificate を作り、registry resolution だけでなく R1/R2（および認可後の R3-NF）が期待 status に達すること。
4. 少なくとも一つの full-path positive control。存在しないなら EP は `uncalibrated/UNKNOWN` のままにする。
5. 旧 synthetic quarantine と same-generation four-role invariant の維持。

この条件が閉じるまで、744 cert の保存・解析はよいが「EP 再発効」「calibrated detector」「operational sentinel unlocked」は不可とする。

> ★教材: **green workflow と green test は別物である。** exit code を receipt に書くだけで job 自体を成功させる workflow では、Actions の緑色は receipt の中身を証明しない。

---

## 3. P94 修文群

### F95-3.1 — C-\(\beta\)-IND' と DUM-3 は PASS

C-\(\beta\) の正しい入力を

\[
(n;r_0,r_\infty)
\]

という datum とし、source/dependency audit と input digest を正式な独立性条件に置く修理は正しい。「任意の有理関数 \(h\)」という旧操作条項の撤回も妥当である。RUN-ADM/SEP/REJ は正式条件そのものではなく、識別力を持つ補助試験として扱うのがよい。

DUM-3 \((9;3,-1)\) は実在する fail-open を突く。因子 character の span は

\[
|\bar A|=\frac{n^2}{\gcd(r_0,n)}
=\frac{81}{3}=27
\]

であり、現行の無条件 \((\mathbf Z/9)^2\) 構成は別の群を列挙してしまう。不合格を列挙前の `KUMMER_RANK_DEFICIENT` へ送る必要がある。既存 \(n=7,r_0=1\) の結果はこの欠陥の影響を受けない。

### P95-3.1 — R1--R7 は修理仕様として承認、実装済みとは数えない

signature の一般化、因子行列からの rank 計算、action faithfulness、構造化 reject、cert schema、GAP 側独立実装、既存 CTRL の bit-identical regression という R1--R7 の順序は妥当である。ただし今便の artifact は **修理設計**であり、R1--R7 の履行 cert ではない。履行までは一般 C-\(\beta\) runner の DUM-3 fail-open は OPEN のままにする。

### F95-3.2 — B-LIMIT-0/0a と条件付き B-LIMIT-1 は PASS

枠組みの橋を前提として

\[
\operatorname{ord}([u_n]_2)=|b(\operatorname{Im}\mathrm{Ih}_N)|,
\qquad
\operatorname{ord}([u_n]_n)=|t(\operatorname{Im}\mathrm{Ih}_N)|
\]

までは忠実性なしで正しい。\(b\equiv1\) は \(\Phi(\mathfrak F_0)=\operatorname{inn}\langle X^2\rangle\) が二ブロックを保つこと、または \(\mathfrak F_0\) が奇位数で \(C_2\) への準同型を持たないことから出る。従って 2-part の自明性は image を知らずに従う。

\(t\) が単射という FAITH の下では

\[
|t(\operatorname{Im}\mathrm{Ih}_N)|
=|\operatorname{Im}\mathrm{Ih}_N|
\]

なので B-LIMIT-1 も正しい。この条件下で route B が位数 \(n\) を示すことは Ihara image の全射性と同値になり、独立な迂回路にはならない。

passport から \(X^2\) が各 \(n\)-点 block に regular に作用して \(t\) が全射であることも正しい。従って橋 F-c 相対で

\[
\mathrm{FAITH}\Longleftrightarrow |\mathfrak F_0|=n
\]

という還元を認める。

### W95-3.1 — B-LIMIT-2 は「無条件命題」ではない

\(\mathcal P\) の各文が image を名指しで制約していないことから、直ちに

> 全ての \(H\le\mathfrak F_0\) について「\(\operatorname{Im}\mathrm{Ih}_N=H\)」という算術シナリオが \(\mathcal P\) と無矛盾

とは言えない。非導出 \(\mathcal P\nvdash\operatorname{ord}([u_n]_n)=n\) を定理として主張するには、各 \(H\) を実現するモデルまたは少なくとも二つの反対モデルを構成する必要がある。「入力一覧に制約が書かれていない」はその代用にならない。

正しい格は次である。

> **依存監査**: 現在列挙された route-B の式では \(H=\operatorname{Im}\mathrm{Ih}_N\) が未決のまま残り、\(|t(H)|\) を計算できていない。従って現行 route B は \(n\)-part の第二系統になっていない。新たな arithmetic image/quotient 入力が加われば再監査する。

この bounded design conclusion は有用だが、「FAITH の真偽によらず、考え得るどの route B も原理的に不可能」という無条件構造定理へ拡張してはならない。

### F95-3.3 — 規約台帳 v1.1 は番号配置を含め条件付き PASS

CV-9 の 5 条は便 94 の規範文どおりである。CV-10（effective source chain）と CV-11（seal recoverability）は単なる cert field でなく、旧正本誤引用と sealed mapping 喪失を防ぐ独立の手続規約なので、トップレベル番号を与えてよい。派生表則を CV-12 へ改番した衝突解消も承認する。

今回の \(\delta\) 表事故は CV-12 の必要性を直接示している。CV-12 は次の三点を一束にすること。

1. 定義から表を生成する script。
2. script/input/output の digest。
3. 文書 build 時に表と定義を再照合し、不一致を fail-closed にする check。

台帳自身の状態札はまだ `candidate` なので、司令塔検分までは「工房正典」と呼ばない。`"n/a"` を全型で許すなら、将来の JSON schema では各 field を文字列との union にするか、型つき `{status:"n/a", reason:...}` に統一し、object/array 欄へ bare string を入れて schema が壊れないようにすること。

---

## 4. 情報共有・訂正

### W95-4.1 — \(\delta(n)\) 早見表は代数側を正とし、表を差し替える

定義

\[
\delta(n)=\frac{n\bmod4}{2}+\frac23(n\bmod3)
\]

から

\[
6\delta(n)=3(n\bmod4)+4(n\bmod3)
\]

である。従って正しい表は次である。

| \(n\bmod12\) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(6\delta(n)\) | **0** | **7** | **14** | 9 | 4 | **11** | **6** | 13 | 8 | **3** | **10** | 17 |

旧表との差は剰余 1, 2, 5, 6, 9, 10 の 6 列である。導出

\[
2\lfloor n/4\rfloor+2\lfloor n/3\rfloor
=\frac76n-\delta(n)
\]

および

\[
5t\le \ell+6-6\delta(\ell+t)
\]

は正しい。列挙された 8 本の \(\ell\) 行も元の floor 式から再計算して一致したため、86/86 の境界主張は、実際に definition/floor 式を使った照合である限り無傷である。

追加で §2.3 の \(n=30\) の文も同じ表事故を含む。正しくは

\[
6\delta(30)=6,
\qquad
5t=25=25+6-6,
\]

で予算は等号可行である。現行の `6δ(30)=11` と `25≤20?` は削除すること。\(n=24,36\) の \(\delta=0\) と \(n=23,35\) の \(6\delta=17\) を使う非単調例は影響を受けない。

### F95-4.1 — 新壁窓二件は情報として受領

\(C_{37}\times S_3\) の位数 \(37\cdot6=222\)、\(C_{41}\times S_4\) の位数 \(41\cdot24=984\) は中央化群の予測と整合する。ただし便自身が述べるとおり cert 化は次波なので、現時点では CLAIMS へ機械事実として昇格しない。S\(_7\) 型 GEN_FAIL も非存在ではなく UNKNOWN のままにする。

### F95-4.2 — git 混入訂正を受領

commit `6395c99` の EP quarantine rename 4 件は内容の数学的誤りでなく attribution の誤属として扱う。pathspec 化という再発防止を受領する。commit message だけを theorem provenance にせず、CV-10 の effective source chain と content digest を正とすること。

### F95-4.3 — Lean 公理化方針 v1.4 は施行条件つき PASS

T1（古典）/T2（論文固有）だけを axiom boundary とし、T2b の足場公理と T3 の未証明仮説を入れず、完成した紙の鎖だけ着工する方針は首尾一貫している。`verified-modulo-axioms` を無印 `verified` と分ける表記も承認する。

ただし Lean kernel が確認するのは「公理から結論が導かれたこと」であって、公理の数学的真偽ではない。従って T1/T2 の格は provenance 層であり、次を必須とする。

### P95-4.1 — Lean 着工時の具体的ゲート

1. axiom ごとに原典の exact theorem/頁、PDF 画像照合の裁定、使用する最弱形、sanity instance を束縛する。
2. Mathlib 不在の主張は Mathlib commit/toolchain を pin し、その版に相対化する。
3. `#print axioms` は `ShadowAxioms` 名前空間だけを見るのでなく、出力の全 axiom を取得し、許可した Lean baseline と生成 manifest の和以外を拒否する。`sorryAx` は常に FAIL。
4. project 全体の manifest は superset でもよいが、各主定理 receipt には実際に出た **exact sorted axiom set** を束縛する。
5. doc-comment から生成する台帳には、説明文だけでなく axiom declaration の正規化した型またはその digest も入れ、説明と Lean proposition の drift を防ぐ。
6. M2-DESC を Lean 化するなら、広い BCL を axiom 化するより F95-1.4 の二次拡大に沿った明示同型と有限降下を形式化する方が axiom boundary を小さくできる。

条件付き定理を一切形式化しないという v1.4 の選択は数学的必然ではなく研究運用上の選択だが、一貫して適用する限り異議はない。

### W95-4.2 — v1.5 は今便の指定 blob 外

今便が指定した `19ab...` は v1.4 exact blob である。現 HEAD の同ファイルには後発 v1.5（裁定 338）が追記され SHA-256 が変わっている。v1.5 の内容を否定するものではないが、本返信の正式判定対象は v1.4 までであり、v1.5 をこの便の digest に遡及混入させない。

### F95-4.4 — C-\(\beta\) 最終 cert の参照格

`u7_cbeta_final_20260801.json` の SHA-256 は指定 `57e26d...` と一致した。三窓 cross-table 等の既存結果を指す original cert として保持してよい。ただし同 cert の `c_beta_ind_dummy_h_selfcheck` は裁定 319 と今便の C-\(\beta\)-IND' により独立性根拠から失効している。CV-10 の effective source chain では、同 cert だけで止めず `u7_fire_log_v1_addendum_grade.md` 追記 4 を erratum/effective source として必ず併記すること。

---

## 5. 監査範囲と再計算

### F95-5.1 — 読了・照合範囲

便 95 の全 numbered section、対話帳の最新 T-21、LEDGER 裁定 319--336、指定 note/cert/source、M2 の GAP/Python source、EP registry/NF/provisioning/sweep source、workflow、frozen spec v18/contract v13、\(\delta\) ノート、Lean 方針 v1.4 blob を読んだ。

実施した小再計算は次のとおり。

- `m2_family_check.py` の \(n=3,7,9\): 模型/抽象 \(\Gamma_n\)、Nielsen 軌道、cross-table が全 PASS。
- `m2_desc_check.py` の \(n=3,7\): 全 \(m\in(\mathbf Z/2n)^\times\) で元の class に戻り全 PASS。
- `m2_symbolic_ext.py`: \(\widetilde\alpha=1,\ldots,8\) の変換恒等式が全 PASS。
- EP: NF 32/32、checker_native 50/50、lane B 184/184、legacy 51/51、lane A 93/93 が fresh PASS。evidence-union 227 の fresh run は上記 Windows temporary-directory 権限問題により根拠へ加えていない。
- GitHub run `30682903849` は `gh run view` で receipt の外部取得を試みたが、この実行環境の network proxy が接続を拒み取得不能だった。従って task/LEDGER の `success` 申告を超える外部 artifact 内容は独立根拠に数えていない。
- \(\delta\) 表は定義から 12 剰余を独立再計算し、列挙された \(\ell\) 8 行を floor 式から再計算した。

GAP cert は source、入力 universe、保存 digest、orbit fields を照合したが、今便で fresh GAP run は行っていない。Lean proof の実行も今便の範囲外である。

## 最終宣言

- **M2 三部作**: 本返信の修文・直接降下証明を effective erratum として **PASS**。M2-GEO、M2-UNIQ、mere-cover M2-DESC は theorem 格でよい。
- **M4 / LIFT**: 上記依存・相対性の下で **PASS**。
- **FAM-U 総組立**: 現行は **奇数 \(n\ge3,\ n\ne5\)**。`全奇数` は封印解除と versioned domain 復帰まで禁止。
- **EP v10**: **再発効 FAIL**。`[27]` の再 freeze、fail-closed CI receipt、full witness-bearing union、positive control が残る。
- **744 sweep**: 指定 universe に相対する bounded decision-lane concordance として受領。較正・完全探索・EP 解錠の根拠にはしない。
