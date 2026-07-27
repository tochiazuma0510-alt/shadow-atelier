# 総合判定: **\(B_{\rm FC}\) 本体は PASS・two-mathematician 確定可／現 v2 artifact は修文つき受理／\(B\)-7\(^{\rm tw}\) の「無条件」定理化と GAP cross-checked 昇格は差戻し**

主定理 B-7 の定理文・証明について、便 43 の R1–R6 は load-bearing な箇所に反映されている。従って

\[
\boxed{
B_{\rm FC}
=
\texttt{paper-proof (framework-conditional on TB1--TB4) /
two-mathematician audit PASS}
}
\]

を**主定理の状態札として確定してよい**。これは (TB1)–(TB4) を前件として採用した紙上定理への判定であり、Lean `verified` ではない。exact \(b=1\) の文献上の向きは引き続き (TB4) 関所にある。

ただし、v2 全文と追加 GAP checker には、主定理を壊さないが最終 artifact・provenance としては閉じるべき残差がある。とくに

- \(B\)-7\(^{\rm tw}\) は B-8 だけから「無条件」には出ない。
- 付録 A の \(b\) の定義は Rule 1・(10.1) と逆数が食い違う。
- GAP 第二系統は \(rs\) 規約を移送したのに \(z\) だけ移送しておらず、同一 marked object の照合器になっていない。
- v2 を `_v1.md` に上書きしており、versioned 規律に反する。

従って、**B-7 本体の昇格と、v2 artifact／有限計算 bundle の最終受理を分離する**。

---

## F1. 対象・再現状態

| artifact | SHA-256 |
|---|---|
| `docs/week4-BFC攻略_opus_v1.md`（内容は v2） | `d6e5fbae7fcd082ded4c761a10964379621256668a9aa08b06500fcd4e5729b2` |
| `search/week4-bfc-antecedents.mjs` | `97621fdb488e92fd4b13e5a7ce7d1665e239dc08ebee4b441b7736973d4ec7d7` |
| `search/bfc-antecedents-check.g` | `daaeb277146157968f5e986674264275f576a47ea80d2a1845d11435c1237d0c` |
| `certificates/bfc/bfc-antecedents.json` | `ff95533c324e312587c970feb57f013c43132a97756b5376a5694ca725981155` |

Node 系は再走して

```text
=== 13/13 PASS ===
V3: 該当 H = 12, 反例 = 0
V7: |Aut(G3)| = 1296, Lambda stabilizer = 432
```

を得た。

GAP 証明書は

```json
{
  "pass_count": 17,
  "fail_count": 0,
  "aut_G3_order": 1296,
  "aut_G3_lambda_stabilizer_count": 432,
  "gt_k3_element_count": 12
}
```

を記録する。GAP wrapper の本便での再走は、起動前段で

```text
fatal error - couldn't create signal pipe, Win32 error 5
```

となったため、私は committed certificate とスクリプト全 319 行をソース監査した。その結果 F6 の fidelity blocker を発見したので、17/17 という表示だけから `cross-checked` へ上げない。

---

## F2. R1–R6 の差分検収

### F2.1 R1 — **PASS**

B-2 は

\[
|\Lambda|=M
\iff
\bigl([P:H]=M\ \text{かつ}\ N_P(H)=H\bigr)
\tag{B2-corr}
\]

と

\[
P/H\longrightarrow\Lambda\text{ が全単射}
\iff N_P(H)=H
\tag{B2-bij}
\]

に正しく分離された。反例 \(S_3\times C_2\) も全仮定を含め正しく採録されている。「(W4) の下で (W3) \(\iff|\Lambda|=M\)」という副産物の射程も正しい。

### F2.2 R2 — **本文 PASS、付録に残差**

B-3 の前件へ (W3) が戻り、第 4 段は

\[
(W3)+(W4)\Longrightarrow\tau(\mu_M)
\text{ が }\Lambda\text{ 上 regular}
\]

として正しく修理された。\(C_M\times C_2\) の反例も適切である。

ただし付録 A の

```text
c : 定理 B-3 で無条件に存在
```

は R2 と矛盾する。「**B-3 の (W1)–(W5) の下で存在**」へ直すこと。これは主証明の残欠ではなく、記号表の stale statement である。

### F2.3 R3 — **PASS**

B-4b と B-4 は \(K\)-版／\(\mathbb Q\)-版に分かれ、

\[
\begin{array}{ll}
K\text{-版}:&(W1)(W2)(W3)(W5)+(CAL),\\
\mathbb Q\text{-版}:&(W1)(W3)(W5^{\mathbb Q})+(CAL)
\end{array}
\]

となった。後者が (W2) を要しない理由も正しい。部分群の pointed 一意性から、\(N_{\widehat F_2}(\widetilde H)/\widetilde H=1\) を介して非標識被覆の一意性へ渡す一段も入った。

compact 閉部分半群の補題も使ってよい。より直接には、正整数 \(n_i\) で \(a^{n_i}\to1\) を取り \(a^{n_i-1}\to a^{-1}\) と書けば一行で閉じる。

### F2.4 R4 — **主線 PASS、用語 1 件**

B-4c は

\[
\pi_1/\mathcal H,\qquad
\widehat F_2/\widetilde H
\]

の左剰余類と左作用へ統一され、stabilizer 公式

\[
\operatorname{Stab}(g\widetilde H)
=g\widetilde Hg^{-1}
\]

および §8 の向きと整合した。R4 の load-bearing 修理は閉じた。

一方、(6.1) の

\[
C_\gamma=\widetilde Hc_\gamma
\]

は**右剰余類**である。本文 6.2 は後段で正しく
\(\widetilde H\backslash\widehat F_2\) を右剰余類と説明しているが、(6.1) の直後だけ「左剰余類」と残っている。そこを「右剰余類」に直すこと。式と cocycle 計算は正しい。

### F2.5 R5 — **主定理 PASS、局所補題の依存をもう一段分けよ**

§4 の表には (TB3)(TB4) が戻り、所与の \(W_0\) と窓からの構成が分離された。B-7 の総前件は正しい。

ただし B-5(ii) は一つの文で

1. uniformizer を替えても \([u]_M\) が不変、
2. \(K\)-モデルを替えても \([u]_M\) が不変、

を主張し、証明の 2 は定理 B-4 の一意性を明示的に使う。従って

- B-5\(_{\rm loc}\): 所与の \(W_0\) に対する (i)(iii) と uniformizer 不変性、
- B-5\(_{\rm win}\): B-4 を加えたモデル不変性、

に分けるか、B-5 の「モデルにも依らない」節へ B-4 の間接依存を明記すること。現状の「B-5 全体の前件は TB1–TB4+(W4)」はその一節について強すぎる。主定理は B-4 の全仮定を既に持つので B-7 には影響しない。

### F2.6 R6 — **PASS**

六層表は便 43 の区別を正しく反映している。

- (W5) failure は \(K\)-モデル非存在でなく `SCHEMA-OUT`。
- 証明書未取得は `MODEL-UNKNOWN`。
- exact 反対証明書だけが `MODEL-MISMATCH`。
- bridge conflict は `THEOREM/CONVENTION/RECORD-CONSISTENCY-FAIL`。

この表は数学稿に要約を残し、運用正本は manifest / Rule 1 へ移すのがよい。

---

## F3. S1–S4 と (W3) 一般化

| 項目 | 判定 |
|---|---|
| **S1** | PASS。TB1–TB4 を global framework、TB4 を exact \(b=1\) の orientation gate とする区別は正しい |
| **S2** | PASS。(W5) は 3/12 元の包含条件であり、432/1296 は周囲データ |
| **S3** | PASS。V6 の寄与を K3 (P7) の非標識 \(\mathbb Q\)-descent 部分へ限定できている |
| **S4** | PASS。A-1 は閉鎖、A-2 は TB4 の向きに条件つき閉鎖 |

\(A=N_P(H)/H\ne1\) の場合に \(H^2(G_K,A)\) の存在障害が残り、\(H^1\) は一つの descent が存在した後の twists を分類する、という F3.4 の採録も正しい。現 B-7 から (W3) を外さない裁定を維持する。

---

## F4. \(K\)-モデルと \(\mathbb Q\)-モデルの stale 文言

R3 の定理文は正しいが、旧説明の一部が追随していない。

現 §3・§13.2 の

```text
明示 Q-model / Q-rational cusp
  <- (W3)+(W4)+(W5)
```

は偽である。(W5) から得るのは \(K=\mathbb Q(\zeta_{2M})\) 上のモデルであり、\(\mathbb Q\)-モデルには (W5\(^{\mathbb Q}\)) が要る。また (W4) 単独から cusp の \(\mathbb Q\)-有理性は出ず、

\[
\begin{array}{ll}
K\text{-有理 cusp}:&
B\text{-4(a)}+(W4),\\
\mathbb Q\text{-有理 cusp}:&
B\text{-4(b)}+(W4)
\end{array}
\]

である。

橋 B-7 は \(G_K\) 上の比較なので、旧い「明示 \(\mathbb Q\)-モデル」を前件から落とす判断自体は正しい。ただし理由は

> **B-7 には \(K\)-モデルで足り、(W1)(W2)(W3)(W5)+(CAL) からそれが出る。追加の (W5\(^{\mathbb Q}\)) があれば \(\mathbb Q\)-モデルまで強化できる**

と書くこと。§6 の見出しも「\(K\)-モデルは帰結、\(\mathbb Q\)-モデルは (W5\(^{\mathbb Q}\)) の帰結」が正確である。

---

## F5. 主定理 B-7 — **PASS**

上の残差はいずれも B-7 の合成に使う仮定を弱めていない。修理後の主線は

\[
\rho_\Lambda(\mathrm{Ih}_N(\gamma))
=
c_\Lambda\,
(\gamma\text{-action on Fib})\,
c_\Lambda^{-1}
=
c_\Lambda m(\kappa_{u^{-1}}(\gamma))c_\Lambda^{-1}
=
\tau(\kappa_{u^{-1}}(\gamma))
\]

で閉じる。

従って、B-7 については追加の数学 blocker はない。次を正式に区別する。

| 主張 | 状態 |
|---|---|
| (TB1)–(TB4) を前件とする B-7 | **paper-proof / two-mathematician PASS** |
| (TB4) の原典番号・exact orientation | **FRAMEWORK-UNKNOWN の文献関所** |
| Lean | 未着手、`verified` ではない |
| B-9 モデル認識 | B-7 の外、素描のまま |

---

## F6. GAP 第二系統 — **17/17 表示は受領、cross-checked 昇格は保留**

### F6.1 marking が同じでない

GAP の `MakeGn` は、論文の左作用規約における \(rs\) を GAP の右作用表現で `s*r` と実装する。これは便 1 で既に裁定済みであり、逆読みを使うなら

\[
\Phi=(\phi_1,\mathrm{id},\phi_3),\qquad
\phi_1(s)=r^{-2}s,\quad
\phi_3(r)=r^{-1}
\]

によって **\(x,y,z,f_{m,k}\) を全部移送しなければならない**。

ところが `search/bfc-antecedents-check.g` は

```gap
y  := (s*r, r, s*r);             # 移送側
zg := (r^2*s, r^-1*s, r);        # 未移送の生座標
```

と混在させている。\(n=3\) で紙上計算すると

\[
x_g\,y_g\,z_g=(r,1,r^2)\ne1.
\]

従って、現在の `zg` は \(z=(xy)^{-1}\) ではない。安全な定義は

```gap
zg := (xg * yg)^-1;
```

であり、座標では

\[
\Phi(r^2s,r^{-1}s,r)
=(s,r^{-1}s,r^{-1})
\]

となる。

現 checker はこの誤った `zg` を target passport の選択に使い、しかも
\(x_gy_gz_g=1\) を fixture として検査していない。出力数が Node と一致したことは強い支持だが、「**同じ marked object を helper 非共有で照合した**」という cross-check の型をまだ満たさない。

### F6.2 \(\kappa\) の符号は結論こそ正しいが、根拠を差し替えよ

GAP 側は第三座標を

```gap
kapExp := -kap mod 3
```

とし、「この符号なら 12 元が自己同型になった」という較正で選んでいる。符号自体は、上の明示移送

\[
\phi_3(r)=r^{-1}
\]

から

\[
(r^{2k},r^{-2k},r^{\kappa(m)})
\longmapsto
(r^{2k},r^{-2k},r^{-\kappa(m)})
\]

と紙上で導ける。従って `-kap` は採用してよいが、「全単射になる符号を選んだ」を根拠にせず、\(\Phi\) による marked transport を証明書へ入れること。自己同型性はその後の反証テストにする。

### F6.3 certificate の不足

次回 certificate では少なくとも次を fail-closed にすること。

1. \(x_gy_gz_g=1\)。
2. V3 の `v3n = 12`（現コードは `v3n > 0` しか assert せず、JSON に件数を保存しない）。
3. Sol F2.1 反例で \(\langle X\rangle\) が \(P/H\) 上推移的であること（現コードは位数・指数・normalizer だけ）。
4. \(\Phi\) による \(x,y,z,f_{m,k}\) の同時移送。
5. script/input digest と上記各値の JSON 記録。

この修理・再走で 17/17（追加 fixture 後は分母増）を再現した時点で、V1–V8 bundle を `cross-checked` へ上げてよい。それまでは

\[
\boxed{\text{Node 13/13 + GAP certificate 17/17 = strong corroboration,
but marked-fidelity gate 未閉鎖}}
\]

とする。とくに 1296/432 の一致は有力だが、bundle 全体の公式札はまだ `source-audited candidate` を維持する。

---

## F7. \(B\)-7\(^{\rm tw}\) — **別番号化には賛成、ただし「無条件」は不可**

### F7.1 B-8 は twisted bridge の存在を証明していない

B-8 は

\[
\rho_\Lambda(\mathrm{Ih}_N(\gamma))
=\tau(\kappa_{u^{-1}}(\gamma)^b)
\tag{10.1}
\]

を**仮定したとき**、像の位数・kernel・固定体が \(b\) で変わらないことを示す補題である。従って B-8 から

\[
\exists b\in(\mathbb Z/M)^\times:\ (10.1)
\]

は出ない。現 v2 の「単位 \(b\) 版は無条件」という文言は循環している。

### F7.2 正しい orientation-free 定理

exact (TB4) を次の弱い仮定へ分けるとよい。

> **(TB4\(^{\rm u}\))** 局所慣性
> \(I_0=\operatorname{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\)
> の \(\pi_1\) への像は \(\overline{\langle x\rangle}\) で、作用は
> \(\Omega\) への後合成である。ただし、選んだ生成元
> \(\sigma_\zeta\) と \(x\) の exact equality は要求しない。

\(x\) と \(\sigma_\zeta\) は同じ procyclic inertia の位相的生成元だから、一意な

\[
\varepsilon\in\widehat{\mathbb Z}^{\times}
\]

があり

\[
x=\iota(\sigma_\zeta^\varepsilon).
\]

\(b\equiv\varepsilon^{-1}\pmod M\) と置くと、局所 torsor 上で

\[
x=m(\zeta_M^\varepsilon),\qquad
c_\Lambda x c_\Lambda^{-1}=\tau(\zeta_M).
\]

従って

\[
c_\Lambda m(\xi)c_\Lambda^{-1}
=\tau(\xi^b)
\qquad(\xi\in\mu_M),
\]

そして

\[
\boxed{
\rho_\Lambda(\mathrm{Ih}_N(\gamma))
=
\tau\!\left(\kappa_{u^{-1}}(\gamma)^b\right).
}
\tag{B7tw}
\]

これを

- 補題 B-6\(^{\rm tw}\): orientation-free torsor comparison、
- 定理 B-7\(^{\rm tw}\): twisted comparison bridge、

として別番号に立てることには賛成する。

ただし状態は

> **TB4 の exact generator equality を要しないが、(TB4\(^{\rm u}\)) という局所慣性比較には条件つき**

である。TB1+TB3 の「inertia generator」という語から (TB4\(^{\rm u}\)) が既に出ると主張するなら、その導出を一段書くこと。少なくとも現在の B-8 だけを根拠に「無条件」とは呼べない。

exact (TB4) は \(\varepsilon=1\)、従って \(b=1\) を与える特殊化である。

### F7.3 \(b\) と \(b^{-1}\) を Rule 1 に合わせよ

Rule 1 (7.1) と §10 (10.1) は

\[
c_i\ell_i c_i^{-1}=\tau_i(\zeta_M^{b_i}),
\qquad
\rho_i=\tau_i\circ[b_i]\circ\kappa_i
\]

という規約である。一方、v2 付録 A は

\[
c_\Lambda m(\zeta_M)c_\Lambda^{-1}
=\tau(\zeta_M^{b^{-1}})
\]

と定義しながら、§10 では \(\kappa^b\) を使う。これは同じ \(b\) ではない。

Rule 1 は既に凍結済みなので、BFC 側を

\[
\boxed{
c_\Lambda m(\zeta_M)c_\Lambda^{-1}
=\tau(\zeta_M^b)
}
\]

へ統一すること。上の導出では \(b=\varepsilon^{-1}\bmod M\) である。逆数規約を残すなら、(10.1) と \(a_{\rm eff}\) 側を全部逆に直す必要が生じるので採らない。

この \(b\) は本来、窓ごとの自由な補正値でなく、同じ \(x\)・\((\zeta_n)\)・局所比較から来る**枠組みレベルの一つの単位**の mod \(M\) 還元である。同じ \(M\) の二 dessin では数学上

\[
b_{\rm sq}=b_{\rm ns}
\]

となる。Rule 1 で両方を記録するのは、実装 transport が同じ規約を実現したかを検査するためであり、引き続き正しい。

---

## F8. versioning と artifact finality

便 43 で監査した v1 の SHA-256 は

```text
659a9570118df503b5cd88b03562954cb6fac1ece9150c2908c8327915c36100
```

だった。同じ path `docs/week4-BFC攻略_opus_v1.md` の現在値は

```text
d6e5fbae7fcd082ded4c761a10964379621256668a9aa08b06500fcd4e5729b2
```

で、本文見出しも v2 になっている。git 履歴上も v1 commit `9b08ee3` の同一 path を v2 commit `ad74d13` が上書きしている。

これは「versioned・上書きしない」という工房規律に反する。最終正本は

```text
docs/week4-BFC攻略_opus_v2.md
```

として新規固定し、v1 は v1 の内容・digest をもつ記録として復元または archive 参照を明示すること。数学判定は変わらないが、現 path のまま `final artifact` として封印してはならない。

併せて次の軽微な finality 修理を行うこと。

1. 付録 A の \(c\) の「無条件」を削除。
2. (6.1) の \(\widetilde Hc_\gamma\) を右剰余類と呼ぶ。
3. B-5 のモデル不変性へ B-4 の依存を付す。
4. §3・§13.2 の \(K/\mathbb Q\) を分離。
5. 付録 A の \(b^{-1}\) を Rule 1 の \(b\) 規約へ統一。
6. 付録 B 冒頭の旧 3 列 header と新 5 列 header の重複を除く。
7. GAP 第二系統完了後も残る「single-system candidate」「第二系統を発注」の stale 文言は、F6 の修理完了後の状態に合わせる。

---

## F9. 最終裁定

### 数学定理

\[
\boxed{
B_{\rm FC}\text{ (B-7) は PASS。
two-mathematician 状態へ確定してよい。}
}
\]

便 43 で見つけた主証明の四欠陥は閉じており、今回の残差は B-7 の真偽を動かさない。

### 付随 artifact

- 現 v2 文書: **修文つき受理**。F4・F7.3・F8 を次の versioned file で直す。
- \(B\)-7\(^{\rm tw}\): **現状差戻し**。(TB4\(^{\rm u}\)) と B-6\(^{\rm tw}\) を明記すれば別番号化可。「無条件」でなく orientation-free framework-conditional。
- GAP 第二系統: **17/17 certificate は受領するが cross-checked 札は保留**。marked \(z\)・\(\Phi\) transport・件数 assert を直して再走すること。
- K3 (P7) 第二証明: V6 の GAP fidelity が閉じるまでは、Node 側 source-audited candidate のまま。閉じた後に非標識 \(\mathbb Q\)-descent 部分だけへ登録する。

以上をもって、**B-7 本体の theorem gate は閉鎖、twisted 版・finite provenance・artifact finality は別札で継続**と裁定する。
