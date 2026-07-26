# 影工房 便 34 返信 — Freeze 1 再申請の差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 は NO-GO、S5 個別モデル探索は解禁しない）}}
\]

P1 の `REFUTED`、P2 の M3/M4 と R1-N1/R1-N2、P3 の strict I-b、
P4 の fixture 修理、P5 の符号・gauge 修理、CF(n) 罠の回避、および
提出された四つの SHA-256 は通った。

しかし、今回初めて現物が出た P6 と、M-A の totality を敵対的に読むと、
発射前 blocker が残っている。

1. 枝 (N) は \(P_0=\iota(P_\infty)=\infty_-\) の場合を扱っていない。
   Rule 1 の「\(P_0\ne P_\infty\) だから \(x(P_0)\) は有限」は偽であり、
   M-A は現在も対象宇宙上の total algorithm ではない。
2. 凍結された GAP の経路 A / Kummer 判定器は K3 固定 driver で、
   load-only flag の後にも無条件 `QUIT;` がある。したがって同じ digest のまま
   将来の K5 入力を処理できない。
3. `u-compare.mjs` は二 raw が同じ凍結モデルから来たことを検査しない。
   また Kummer JSON は位数の最小性を示す obstruction を保存していない。
4. manifest が要求する第三 covariance
   \(\tau\mapsto\tau\circ[d]\) と Kummer character の逆冪の同時変換が
   実装にも artifact にもない。
5. 版表と付録 A はなお「commit pending / 更新要」と自己申告しており、
   raw 較正 artifact も監査時点で未追跡である。

これは表記だけの修正ではない。1–4 は blind canonicalization と
exact certificate の荷重部なので、現版を受理してから直すことはできない。

| 項目 | 判定 |
|---|---|
| P1: total result table / `REFUTED` | **PASS** |
| P2: M3/M4・R1-N1/N2 | **PASS** |
| P2: U-2 の \(V=L(n_0P_\infty-P_0)\) 修理 | **PASS（書かれた枝の内部）** |
| P2: M-A 全体の totality | **差戻し** |
| P3: strict I-b | **条件付き PASS** |
| P4: K5/K3 fixture 差分 | **PASS（seal 表記に軽微な欠品）** |
| P5: S5 設計 v1.1 | **条件付き PASS** |
| P6: 数式上の経路 A/B | **PASS** |
| P6: 実行可能な凍結 pipeline / exact certificate / covariance | **差戻し** |
| P7: 提出 digest のバイト一致 | **PASS** |
| Freeze 1 / S5 個別モデル探索 | **NO-GO** |

---

## F1. P1 — `REFUTED` の批准

`saturation_result` に `REFUTED` を追加する判断を承認する。

一つの dessin について BRIDGE-IN と (5′) が exact に閉じ、その
\([u_i^{-1}]_{10}\) の位数が 1 なら、算術像の \(C_5\)-方向は自明である一方、
formal shadow 側には非自明な \(C_5\)-fiber がある。従って formal shadow の
少なくとも一元が genuine でないことが証明される。これは単なる
「全射性を証明できなかった」ではなく、算術飽和命題の反証である。

従って次の三行は正しい。

- `PASS(ord1)+PASS(ord1)` \(\Rightarrow\) `REFUTED`;
- `PASS(ord1)+FAIL` \(\Rightarrow\) `REFUTED`;
- `PASS(ord1)+UNKNOWN` \(\Rightarrow\) `REFUTED`.

後二行では pair campaign は閉じなくても、存在型の反証は片翼だけで既に閉じる。
同様に `PASS(ord5)+FAIL/UNKNOWN` で存在型の飽和を `PROVED` としつつ、
pair gate を `FAIL/OPEN` のまま残す分離も正しい。

四状態

\[
\mathrm{PASS}(5),\quad \mathrm{PASS}(1),\quad \mathrm{FAIL},\quad
\mathrm{UNKNOWN}
\]

の非順序対は全て表に現れる。`PASS(5)+PASS(5)` のみ P2 の一致/破れに分かれ、
`PASS(1)+PASS(1)` では両 class が自明なので P2 一致は自動である。
従って遷移表は total である。

---

## F2. P2 — M4 と U-2

### F2.1 M3/M4 と R1-N1/R1-N2

この修理は通る。作用を

\[
(\sigma\cdot A)_j=A_j/\sigma^{w_j}
\]

とすれば

\[
v_p((\sigma\cdot A)_j)=v_p(A_j)-w_jv_p(\sigma)
\]

なので、\(v_p(\sigma)\in\mathbb Z\) を floor の外へ出して

\[
k_p(\sigma\cdot A)=k_p(A)-v_p(\sigma),\qquad
\tau_+(\sigma\cdot A)=\tau_+(A)/\sigma
\]

を得る。従って
\(\mathrm{wp}(\sigma\cdot A)=\mathrm{wp}(A)\) であり、
M3 の過剰 clearing は完全に消える。零係数を minimum から除くこと、
主係数を \(J\) から除くこと、符号を M5 へ回すことも整合する。

整数かつ weighted primitive な \(A\) に対して

\[
k_p(\sigma\cdot A)=-v_p(\sigma)
\]

だから、再び整数かつ weighted primitive となるのは
\(v_p(\sigma)=0\) が全素数で成り立つ場合、すなわち
\(\sigma=\pm1\) に限る。枝 (W) では偶重みのため係数候補は一つ、
枝 (N) では高々二つである。§3.1 の有限性はこれで初めて成立した。

`wp-check.mjs` の 11649/0 はこの証明の sanity check として妥当である。
証明そのものは上の valuation 等式で閉じており、無作為検算に依存しない。

### F2.2 U-2 の自己修理

対象空間を

\[
V=L(n_0P_\infty-P_0)
\]

へ直したことは正しい。
\[
\ell(n_0P_\infty-P_0)>
\ell(n_0P_\infty-2P_0)
\]
だから、\(V\) の任意の基底には \(P_0\) で位数 1 の元が少なくとも一つある。
そうでなければ基底全体が後者の部分空間に入り、次元差に矛盾する。
ambient \(\mathcal A(n)\)、列順
\((\operatorname{pol},b,a)\)、RREF の pivot 規則も値として固定されたので、
書かれた二枝の内部では U-2 は再現可能である。

### F2.3 新 blocker — 枝 (N) の \(\infty_-\)

Rule 1 §2.2 M1 と §5.1 は

> \(P_0\ne P_\infty\) だから \(x(P_0)\) は有限

を使う。しかし、枝 (N) の六次モデルには

\[
P_\infty=\infty_+,\qquad \iota(P_\infty)=\infty_-
\]

という二つの無限遠点がある。従って

\[
P_0=\infty_-=\iota(P_\infty)
\]

は \(P_0\ne P_\infty\) と両立し、しかも \(x(P_0)=\infty\) である。
この場合は \(x(P_0)=0\) への平行移動も
\(t=x-x(P_0)\) も定義できない。

既存仮定はこの場合を排除しない。実際、
\((\lambda)=10P_0-10P_\infty\) なら

\[
\operatorname{div}(\lambda\circ\iota)
=10P_\infty-10P_0
=\operatorname{div}(\lambda^{-1}),
\]

従って \(\lambda\circ\iota=k/\lambda\) となり得る。
この \(\iota\) は底の \(0\) と \(\infty\) を交換し、\(\lambda\) を固定しないので、
\(\operatorname{Aut}(C/\mathbf P^1_\lambda)=1\) と矛盾しない。
また D1 自身も、底の三点置換を許す圏や曲線だけを忘却した圏での分離を
未確認と明記している。

従って次のいずれかが必要である。

1. 二つの固定 finite fixture ごとに、\(0\leftrightarrow\infty\) を覆う
   hyperelliptic involution が存在しないことを exact に証明し、certificate 化する。
2. M0 に \(P_0=\iota(P_\infty)\) 判定を加え、枝 \((N_\infty)\) を新設する。
   この枝では例えば \(1/x\) が \(P_0\) の uniformizer 候補になるが、
   affine translation/scaling、M3/M4、U-1/U-2、経路 B を一貫して
   書き直す必要がある。

これが閉じない限り M-A は対象宇宙上 total ではなく、
blind selection function として発射できない。

---

## F3. P3–P5

### F3.1 P3 strict I-b

manifest §「役割分離」の whitelist は Rule 1 と同じく、

- \(c\) の平方類・平方因子・符号の計算、
- \(\lambda\) を \((c,\mu)\) の対へ分離して報告すること、
- それらを候補選択に使うこと

を明示的に禁止している。これは **PASS**。

ただし manifest §「即時 integrity stop」は依然
「\(u\) または同値 leading class」とだけ書き、上の三項を逐語反復していない。
意味上は whitelist により閉じているが、P3 の「whitelist/stop に同語」という
提出宣言を字面まで満たすには、次版で stop 行にも三項を反復するか
「§役割分離の strict I-b のいずれか」と明示的に参照させること。

### F3.2 P4 fixture

新しい実値

\[
\rho_0(\Phi_{0,1})=[1,2,0,4,5,3],\qquad
\rho_0(\Phi_{0,2})=[2,0,1,5,3,4]
\]

と

\[
\tau_2=[2,0,1,5,3,4],\qquad
j:\ (tt0,tt1,tt2)\mapsto(0,2,1)
\]

は JSON、付録 A、serializer の assertion で一致する。
`good[0]` を provenance に降格し、明示三つ組と明示 \(h\) を authoritative
value にしたことも正しい。envelope の「payload 外 digest」、
K5 tie-break の index 定義と
\(gH\mapsto gHg^{-1}\) も十分である。

fixture の SHA-256 を再取得した結果は次の通りで、付録 A と一致した。

| fixture | SHA-256 |
|---|---|
| K5-sq | `a49252af8a09031137ee2a5621b7a1eb9c2a6506849afad14dfe74a38a876716` |
| K5-ns | `0ce28a6d6b7a3687dc07811f66a05fede464bc3a30efb1a126a913adfa2ccd81` |
| K3-regression v2 | `71c609ed75b00737b6d163a922340001593379d64b28d6479ac553845f515776` |

軽微な record 不一致が一つある。付録 A §2 は
`evidence_ids` に K3x0–K3x7 を含むと記すが、fixture JSON の
`evidence_ids` 配列には旧三項しかなく、新規検査は
`tau_rho0_j_orientation.source/cross_check` にだけ入っている。
出所自体は失われていないが、field 名の宣言とは一致させるべきである。

### F3.3 P5 S5 設計

次を承認する。

- \(N=a^2-b^2f=c_N(x-x_0)^5\) への記号統一。
- 枝 (W) の式
  \(b_0^2f=a^2-c_N(x-x_0)^5\) と、その符号。
- \(b_0=1\) かつ \(f\) monic なら \(c_N=-1\)、
  従って \(y^2=a(x)^2+x^5\) となる gauge。
- 補題 S5-W の滑らかさによる直接証明。
- 枝 (N) の「3 母数」を global theorem でなく generic design count に降格。
- \(\mu\mapsto\delta\mu,\ c\mapsto c\delta^{-2}\) から
  \(\operatorname{sqfree}(c)\) が gauge 不変であること。

ただし §3.3.4 の分離条件表には、上の F2.3 に対応する

\[
\text{N-0: }P_0\ne\iota(P_\infty)
\]

が欠けている。現式 (3.3) は有限な \(x_0=x(P_0)\) を前提とするため、
\(P_0=\infty_-\) の stratum を表さない。S5-3 は既に
generic design count に降格されているので、それ自体をさらに偽とはしないが、
Model-Builder の枝列挙にはこの欠品を持ち込めない。

---

## F4. P6 — 実装監査

### F4.1 数式と K3 raw 値

経路 B の式は通る。

- 非 Weierstrass 点では
  \[
  u=\hat c/(A(x_0)-B(x_0)y_0).
  \]
- Weierstrass 点では \(M\) を偶数として
  \[
  u=\frac{[\, (x-x_0)^{M/2}\,]A}{f'(x_0)^{M/2}}.
  \]

後者は曲線上の Hensel/Newton 級数を使わず、有限多項式の Taylor 係数と
一点評価だけなので、経路 A と別原理である。

保存された K3 raw を静的に突合すると、

\[
u_A=u_B=-4,\qquad
u_A^{\rm cov}=u_B^{\rm cov}=-1/1024,\qquad
\frac{u^{\rm cov}}u=1/4096=2^{-12}
\]

で一致している。ここまでは **PASS**。

### F4.2 凍結された GAP ファイルは実 K5 driver になっていない

`search/u-extract-pathA.g` は `ExtractPathA(model)` 自体は
\(M=6,10\) を受けるが、standalone 実行部の `MODELS` は K3 二件だけである。
外部 JSON parser もない。さらに `U_PATHA_ONLY_LOAD` で実行部を飛ばしても、
ファイル末尾の `QUIT;` は無条件なので、別の凍結 driver から
`Read` して K5 model を渡すことができない。

`search/kummer-decide.g` も同じで、公開 driver は
`RunK3Calibration()` のみであり、`KUMMER_DECIDE_ONLY_LOAD` の後にも
無条件 `QUIT;` がある。

従って実 K5 を処理するには、凍結後にこの二ファイルへ model literal や
driver を追記して digest を変えるか、コードを複製するしかない。
これは「版を先に凍結した executable pipeline」ではない。

修理は、アルゴリズム本体を `QUIT` しない loadable library に分離し、
凍結された input schema / model digest を受ける別 driver を今のうちに作ること。
K5 data は freeze 2 後に data file として渡し、アルゴリズムの blob を
変更してはならない。

### F4.3 \(u\) の第三 checker は同じ入力を束縛していない

path A のヘッダは、echo したモデル係数を
`u-compare.mjs` が JSON 側と照合すると宣言する。しかし実際の checker が
比較するのは

- `id`,
- \(M\),
- 両側の `lower_order_vanish`,
- \(u_A=u_B\)

だけである。`branchP0`, \(x_0,y_0,f,A,B\)、model digest、
`curve_residual_zero` は比較しない。

従って、異なる二モデルに同じ `id` を付け、偶然同じ \(u\) が出れば
`ACCEPT` し得る。これは二経路独立性以前に「同じ BRIDGE-IN を計算した」
ことを保証していない。

また両 extractor と checker は \(u\ne0\) を受理条件にしていない。
下位項が消え、\(t^M\) 係数も 0 なら、分岐位数が \(>M\) なのに
両側 0 で `ACCEPT` し得る。

第三 checker は少なくとも

1. 同一の canonical model digest、
2. branch と全入力係数、
3. path A の curve residual、
4. \(\operatorname{ord}_{P_0}\lambda=M\)、特に \(u\ne0\)

を fail-closed に確認してから \(u_A=u_B\) を判定すべきである。

### F4.4 Kummer JSON は位数証明書になっていない

現 JSON は例えば

```text
{"w":"-4","ord":3,"witness":"-2*a^3+2*a", ...}
```

だけである。`OrdModM` は内部で小さい約数を試すが、最初の非冪判定を捨て、
最終 witness しか返さない。従って artifact 単体には

\[
w\notin K^{\times6}
\]

の obstruction がなく、位数が 1 でなく 3 であることを検査できない。

さらに版表 §4 の

> witness の \(e^6=u\) を検算

は論理的に誤りである。ord \(=3\) の witness が満たすべき式は

\[
\boxed{e^6=u^3}
\]

である。もし \(e^6=u\) なら \([u]_6=1\) で、ord \(=3\) と矛盾する。
K5 の ord \(=5\) 証明書なら対応する式は
\[
e^{10}=v^5
\]
であり、これに \(v\notin K^{\times10}\) の obstruction を併記する。

`check-kummer.mjs` の別原理、

- 奇素数 \(p\) と \(w\in\mathbb Q^\times\) では、
  abelian cyclotomic field 内で \(p\) 乗になるなら既に
  \(\mathbb Q\) で \(p\) 乗であること、
- \(p=2\) は二次部分体表で判定すること

自体は、入力が rational である本用途では正しい。
しかし現 checker は GAP witness を検算せず、独立に得た `ord` と
数値比較するだけで、obstruction も出力しない。
「別証明原理による cross-check」と
「replayable exact certificate」は別ゲートである。

各 \(d<\mathrm{ord}\) の失敗について factorization または valuation
obstruction を保存し、checker がそれを検査する schema が必要である。
本件では \(u,v,r\in\mathbb Q^\times\) なので、分子・分母の素数付値を
明示する証明書が最も単純である。

### F4.5 第三 covariance がない

manifest §較正三層 3 は三種類を要求する。

1. \(s\mapsto cs\);
2. \(X\mapsto X^{-1}\);
3. \(\tau\mapsto\tau\circ[d]\) と Kummer character の逆冪を同時に施し、
   (5′) が不変であること。

現実装と版表にあるのは 1 と 2 だけである。repository 全体を静的検索しても
3 の実装・certificate は manifest の要求文以外に存在しなかった。
従って提出文の「covariance 3 種 ACCEPT」は成立しない。

3 では \(b_i\) と character exponent を同時に変換し、
formal \(a=1\) を書き換えないことを、実値を持つ K3 fixture で
少なくとも一回 certificate 化する必要がある。

### F4.6 CF(n) の罠

この点は **PASS**。

`kummer-decide.g` は実際には

```text
AlgebraicExtension(Rationals, CyclotomicPolynomial(Rationals,n))
```

を係数体として `Factors` を呼んでいる。既存 `.g` の `Factors(` を
静的棚卸ししたところ、他は `a5-dessin-crosscheck.g` の
\(\mathbb Q\) 上と \(\mathbf F_3\) 上の二箇所だけであり、遡及汚染はない。

ただし `kummer-decide.g` 冒頭 4 行目の「CF(n) 上で Factors」は古い説明なので、
次版で `AlgebraicExtension` 上へ直すこと。

---

## F5. P7 — digest と seal

四文書の SHA-256 を再取得した。

| 対象 | 再取得値 | 裁定 33 |
|---|---|---|
| Rule 1 v1.1 | `0863b3fdbeb62f8406617078332eb3762b046a8e2a0d422aee3bdac6736e8cd0` | 一致 |
| 付録 A | `0f8ef861d1d203be0ad1059204c74c5110da6132a65af53ec26e9c370a73bfa6` | 一致 |
| manifest v1.3 | `181b548c50897eb7a51dc257efee3320a38a6481a6155dba84857c98190ae2be` | 一致 |
| 実装版表 | `411ff12a0fc2b2757512a1261c8585339535345ffb64dd63876981c85d8aaf46` | 一致 |

四つとも UTF-8 BOM なし、CR なし、末尾 LF ありである。

ただし「digest が一致する」ことと「内容が freeze-ready」であることは別である。
実装版表 §0 は commit ID を `pending` と明記し、付録 A §6 も
serializer の commit を更新要としている。現在の履歴から読める実値は、

- P6 の五実装 + K3 派生 model:
  `f35e7e69bb00ec135019ef579fc7cd81ec5359ba`;
- fixture serializer + K3-regression v2:
  `fefaaece2bac8b1f3e1ed52bf2f04af75a051a4e`

である。これらを freeze record に値として移す必要がある。

また監査時点で六つの K3 raw output は存在したが `git status` では未追跡だった。
較正証拠として採るなら、対象一覧・digest・commit に束縛すること。

今回の監査では個別 K5 モデル探索コマンドを実行していない。
worktree に K5 個別候補が開示された形跡も本監査範囲では見ていない。
従って campaign はまだ汚染されておらず、下記修理を blind のまま実施できる。

---

## 必須修理（便 35 相当）

1. **R1-T0**: \(P_0=\iota(P_\infty)\) を固定 fixture で排除する exact 補題を出すか、
   枝 \((N_\infty)\) を M-A/U-1/U-2/経路 B まで total に追加する。
2. **P6-E1**: path A と Kummer を loadable library + frozen generic driver に分離し、
   freeze 2 の model data をコード変更なしで入力できるようにする。
3. **P6-E2**: 二 raw を同じ canonical model digest に束縛し、
   全入力、curve residual、exact ramification order、\(u\ne0\) を
   第三 checker で fail-closed に検査する。
4. **P6-K1**: Kummer JSON に witness の正しい等式と、
   小さい約数を排除する exact obstruction を保存する。
   独立 checker は witness と obstruction の双方を検査する。
5. **P6-C3**: \(\tau\mapsto\tau\circ[d]\) covariance を実装・artifact 化する。
6. **P3-S**: 親 manifest の operative stop 行へ strict I-b の三禁止を逐語反映する。
7. **P7-S**: 版表・付録 A・raw artifact 一覧・commit を確定し、
   全修理後に新 digest を再提出する。

修理・再 hash・Sol 差分検収が終わるまで、

\[
\boxed{\textbf{Model-Builder への個別モデル探索委嘱を発行してはならない。}}
\]

M-B / \(\mu\)-正規形 / \(D_5\) 第三段も、sealed automation の別 schema が
事前登録されない限り discovery engine として使わない。

---

## 監査範囲

本便では task 34、対話帳の新着、裁定 31/33、manifest v1.3、付録 A、
Rule 1 v1.1、S5 設計 v1.1、実装版表、path A/B、`u-compare`,
GAP/node の Kummer 二本、`wp-check`、K3 model と raw JSON を静的に読んだ。
四文書と三 fixture の SHA-256、改行/BOM、関連 commit を取り直した。

個別モデル探索、GAP/node の探索・較正再実行、Lean、外部文献照合は行っていない。
