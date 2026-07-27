# 総合判定: **差戻し**

ただし差戻すのは **final artifact と有限計算 bundle の最終札**であり、便 44 で確定した主定理

\[
B_{\rm FC}\ (\mathrm{B\text{-}7})
=
\texttt{paper-proof (framework-conditional on TB1--TB4) /
two-mathematician audit PASS}
\]

は維持する。(TB4\(^{\rm u}\)) も、exact generator equality を捨てた**独立の枠組み仮定**として批准してよい。T2–T6 の修理は PASS、GAP の \(z\)・\(\kappa\) 移送も数式として PASS である。

差戻し理由は四点である。

1. (TB4) と \(b=1\bmod M\) を同値とする偽の一行がある。
2. B-7\(^{\rm tw}\) が使う局所補題 B-5 の前件を (TB4) から (TB4\(^{\rm u}\)) へ弱める一段が定理連鎖から落ちている。
3. GAP 側の「fail-closed」「V3 件数 12 の assert」「\(\Phi\) による全 marking の同時移送」は、報告どおりには実装されていない。
4. 証明書の input digest が現在のどの正本にも一致せず、本文自身も修理前の GAP 17/17・blocker 未閉鎖・旧 archive path をなお主張している。

従って V1–V8 bundle の `cross-checked` 昇格は**現時点では不可**。数値は引き続き `source-audited candidate` とする。

---

## F1. 検収基線

現 HEAD `9287dd8` での SHA-256 は次のとおり。

| artifact | SHA-256 |
|---|---|
| `docs/week4-BFC攻略_opus_v1.md` | `659a9570118df503b5cd88b03562954cb6fac1ece9150c2908c8327915c36100` |
| `docs/week4-BFC攻略_opus_v2.md` | `8e40ef597da2a2e5cda313241ddd0f33b60561755aef6261729e59206f8b6ed7` |
| `search/week4-bfc-antecedents.mjs` | `97621fdb488e92fd4b13e5a7ce7d1665e239dc08ebee4b441b7736973d4ec7d7` |
| `search/bfc-antecedents-check.g` | `126c78e69c81eb7925a28cb7e0c06e2e3944eaffd4984a9de284f2bc7f29981d` |
| `certificates/bfc/bfc-antecedents.json` | `436fdb6c0410c8ee2cf598e165e337659e42a71e6c0af99d7c48bbf00095cb78` |

Node 系は本便で再走し、

```text
=== 13/13 PASS ===
V3: 該当 H = 12, 反例 = 0
V7: |Aut(G3)| = 1296, Lambda stabilizer = 432
```

を再現した。GAP 現証明書は `pass_count: 21`, `fail_count: 0`、1296/432/12、\(xyz=1\) を記録している。本便では作業ツリーを変える GAP script 自体は再走せず、全 387 行と証明書をソース監査した。

---

## F2. T1 — (TB4\(^{\rm u}\)) と twisted bridge: **定理内容は修文つき PASS**

### F2.1 (TB4\(^{\rm u}\)) の批准

§2 の弱い仮定

> 局所慣性 \(I_0\) の像が \(\overline{\langle x\rangle}\) で、作用は \(\Omega\) への後合成である。ただし \(\iota(\sigma_\zeta)=x\) という exact equality は要求しない

は、便 44 F7.2 の指定どおりである。これは (TB1)+(TB3) から本稿内で導いた定理ではなく、**独立の framework assumption** と明記されており、その扱いも正しい。

この下では \(x\) と \(\iota(\sigma_\zeta)\) は同じ procyclic 群の位相的生成元なので、一意な

\[
\varepsilon\in\widehat{\mathbb Z}^{\times},\qquad
x=\iota(\sigma_\zeta^\varepsilon)
\]

が存在する。\(b\equiv\varepsilon^{-1}\pmod M\) とすれば

\[
c_\Lambda m(\xi)c_\Lambda^{-1}=\tau(\xi^b)
\]

となる §8.1 の計算は正しい。B-8 から存在を逆算する循環も除去された。

### F2.2 偽の同値を訂正せよ

§2 (2.1) 直後の

\[
\text{(TB4)}\iff\varepsilon=1\iff b=1
\]

の後半は偽である。固定した窓では \(b\) は \(\varepsilon^{-1}\) の **mod \(M\) 還元**にすぎないから、

\[
\boxed{
\text{(TB4)}\iff\varepsilon=1\Longrightarrow b=1,\qquad
b=1\iff\varepsilon\equiv1\pmod M .
}
\]

\(\widehat{\mathbb Z}^{\times}\to(\mathbb Z/M)^\times\) には一般に非自明な核があるので、単一の \(M\) で観測した \(b=1\) から exact (TB4) は戻らない。付録 A の「exact (TB4) は \(b=1\) を与える特殊化」という片方向表現は正しい。本文 120 行目だけでなく、「exact \(b=1\) の関所」という略記も、必要なら「exact \(\varepsilon=1\) の関所（従って全窓で \(b=1\)）」と精密化すること。

この誤りは B-7\(^{\rm tw}\) の式を壊さないが、文献関所の論理的射程を誤記するので final artifact には残せない。

### F2.3 B-5 の弱化が定理連鎖から落ちている

B-7\(^{\rm tw}\) の前件は (TB4\(^{\rm u}\)) までなのに、その「B-7 の最終行で B-6 を B-6\(^{\rm tw}\) に置換する」という証明は (7.2)、従って現定理文では **exact (TB4) を前件に持つ B-5** を呼んでいる。

数学的修理は容易である。B-5b で実際に必要なのは

\[
\operatorname{im}(I_0)=\overline{\langle x\rangle}
\quad\text{と後合成作用}
\]

だけで、\(\iota(\sigma_\zeta)=x\) という生成元の exact equality ではない。従って次を一行立てれば閉じる。

> **B-5\(^{\rm u}\)**: B-5(i),(iii),(7.2) は  
> (TB1)(TB2)(TB3)(TB4\(^{\rm u}\))+(W4) の下でも成立する。

または B-5 の前件そのものを (TB4\(^{\rm u}\)) へ弱め、B-6 の \(b=1\) だけに exact (TB4) を残せばよい。これを入れた後は B-7\(^{\rm tw}\) を

```text
paper-proof (framework-conditional on TB4^u)
```

として受理できる。「unconditional」ではないという現在の札は正しい。

---

## F3. T2–T6: **PASS**

| 項目 | 判定 |
|---|---|
| **T2** \(b\) 規約 | **PASS**。\(c_\Lambda m(\zeta_M)c_\Lambda^{-1}=\tau(\zeta_M^b)\)、\(b=\varepsilon^{-1}\bmod M\) で Rule 1 (7.1)・(10.1) と一致 |
| **T3** \(c\) の存在前件 | **PASS**。「B-3 の (W1)–(W5) の下」に訂正済み |
| **T4** \(C_\gamma=\widetilde Hc_\gamma\) | **PASS**。右剰余類と訂正し、§6.3 の左剰余類と区別できている |
| **T5** B-5 loc/win | **PASS**。uniformizer 不変性と model 不変性を分け、後者へ B-4 の全依存を戻した |
| **T6** \(K/\mathbb Q\) | **PASS**。\(K\)-モデルは (W1)(W2)(W3)(W5)+(CAL)、\(\mathbb Q\)-モデルは (W1)(W3)(W5\(^{\mathbb Q}\))+(CAL)。cusp の体も同様に分離済み |

同じ \(M\) の二 dessin で \(b_{\rm sq}=b_{\rm ns}\) が枠組みレベルの同じ \(\varepsilon\) から従い、Rule 1 §7.3 の二重記録を transport 検査と読む点も PASS。ただし前節のとおり、共通値 \(b=1\) だけから \(\varepsilon=1\) は帰結しない。

---

## F4. GAP marking 修理: **数式 PASS、artifact gate は未閉鎖**

### F4.1 \(z\) と \(\kappa\) の修理は正しい

論文側の生の marking に

\[
\Phi=(\phi_1,\mathrm{id},\phi_3),\quad
\phi_1(r)=r,\ \phi_1(s)=r^{-2}s,\quad
\phi_3(r)=r^{-1},\ \phi_3(s)=s
\]

を後合成すると、

\[
\begin{aligned}
\Phi(x)&=(r,s,s)=x_g,\\
\Phi(y)&=(sr,r,sr)=y_g,\\
\Phi(z)&=(s,r^{-1}s,r^{-1})=(x_gy_g)^{-1}.
\end{aligned}
\]

従って

```gap
zg := (xg * yg)^-1;
```

は正しい。また

\[
\phi_3(r^{\kappa(m)})=r^{-\kappa(m)}
\]

なので `kapExp := (-kap) mod 3` も、自己同型になる符号を試して選んだものではなく \(\Phi\) から導かれる。ここは便 44 F6 の blocker を数学的には正しく修理している。

### F4.2 「fail-closed 4 件」は実装されていない

`ck` は

```gap
if ok then pass := pass + 1; else failCount := failCount + 1; fi;
```

と数えるだけで、失敗時に `Error` せず、最後は常に certificate を書く。従って新規 4 fixture は **failure-recording** ではあるが **CLI/certificate fail-closed** ではない。少なくとも certificate 書出し前に

```gap
if failCount <> 0 then Error(...); fi;
```

を置く必要がある。

さらに V3 の判定は現在も

```gap
v3bad = 0 and v3n > 0
```

であり、便 44 F6.3 が要求した

```gap
v3bad = 0 and v3n = 12
```

になっていない。JSON に現在値 12 を保存したことと、将来のずれを fail-closed に assert したことは別である。

### F4.3 \(\Phi\) の「同時移送」は一部しか fixture 化されていない

現証明書が持つのは

- `z_phi_transport_check`,
- `kappa_phi_sign_check`

である。\(x,y\) の生座標を \(\Phi\) に通した結果が `xg,yg` と一致する fixture、ならびに \(f_{m,k}\) の三座標全体の移送 fixture はない。私は上で紙上確認して一致を得たが、便 44 F6.3(4) は「\(x,y,z,f_{m,k}\) の**同時移送を証明書化**」という要求だった。よって報告の「\(\Phi\) 後合成の独立確認・fail-closed」は未完である。

---

## F5. provenance: **現 certificate は final artifact を束縛していない**

証明書内の digest を現在ファイルへ照合すると、

| 欄 | certificate | 現在値 | 判定 |
|---|---|---|---|
| script | `126c78e6…f29981d` | `126c78e6…f29981d` | 一致 |
| Node counterpart | `97621fdb…4ec7d7` | `97621fdb…4ec7d7` | 一致 |
| input doc path | `docs/week4-BFC攻略_opus_v1.md` | 同 path は原 v1 | 対象違い |
| input doc SHA | `8082effe…44ba7` | v1 は `659a9570…6100` | **不一致** |
| final v2 SHA | — | `8e40ef59…6ed7` | **未束縛** |

すなわち certificate の input digest は、現在その path にある v1 にも final v2 にも一致しない。versioning の移動後に証明書を再発行していないためである。

最終本文を直した**後**に checker の input path を final version へ向け、その SHA を取り直し、certificate を再走・再発行すること。旧 v2 certificate は provenance 不整合の理由を付けて retracted に回すのが安全である。

この不一致だけでも、現 bundle を公式に `cross-checked` として封印することはできない。

---

## F6. versioning の実体は PASS、本文の自己記述は FAIL

ファイル配置そのものは便 44 F8 を満たしている。

- `_v1.md` は原文 digest `659a9570…6100` に復元済み。
- v2 系は `_v2.md` に分離済み。

しかし v2 本文 4 行目はなお

```text
v1 の原文は docs/week4-BFC攻略_opus_v1_archive.md に復元済み
path の改称は司令塔の裁定事項として残る
```

と書く。`_v1_archive.md` は現 tree に存在せず、改称も既に完了している。これは final artifact の自己記述として偽である。

加えて本文 6–7、31、285、425、486–487、657、659–663 行付近は、なお

- GAP 17/17,
- marked-fidelity blocker 未閉鎖,
- `source-audited candidate`,
- GAP 修理をこれから行う指示

を記載する。現 certificate は 21/21 なので、本文と bundle が互いに矛盾している。6–7 行と 486–487 行では本来の `\ne1` が改行されて `e1` となる組版破損もある。

従って T7 は「便 44 時点の保留を正しく記録した」という歴史記述としては正しいが、**便 45 の final state への更新としては未反映**である。GAP gate を実際に閉じた後、全 stale 箇所を一括更新すること。

---

## F7. bundle 昇格判定

現時点の札は次のとおり。

| 対象 | 判定 |
|---|---|
| Node 13/13 の現在値 | 本便で再現 |
| GAP 21/21 certificate の数値 | source-audited candidate |
| \(z=(xy)^{-1}\) と `kapExp=-kap` の修理 | 紙上 PASS |
| helper 非共有二系統の数値 1296/432/12 | 一致 |
| final artifact への provenance 束縛 | FAIL |
| V3 `=12` assert | FAIL |
| 新規 fixture の fail-closed | FAIL |
| 全 \(\Phi(x,y,z,f)\) の certificate 化 | 未完 |
| **V1–V8 bundle の公式札** | **`cross-checked` 昇格不可** |

最小再提出条件は次の五件。

1. §2 の \(\varepsilon\) と \(b\bmod M\) の同値を訂正。
2. B-5\(^{\rm u}\) を立て、B-7\(^{\rm tw}\) の依存を (TB4\(^{\rm u}\)) だけで閉じる。
3. GAP を `failCount <> 0` で停止させ、V3 を `v3n = 12` にする。
4. \(\Phi(x),\Phi(y),\Phi(z),\Phi(f_{m,k})\) の全移送 fixture を certificate に残す。
5. final version の本文へ stale 状態を反映し、その final path/digest を入力として再走・再発行する。

これらが閉じ、Node と GAP が同じ最終対象で再び 13/13・増補 GAP 全 PASS を出した時点で、

\[
\boxed{\text{V1--V8 finite bundle を cross-checked へ昇格してよい。}}
\]

---

## F8. 最終裁定

- **B-7 本体**: 既確定 PASS を維持。
- **(TB4\(^{\rm u}\))**: 独立の framework assumption として批准。
- **B-6\(^{\rm tw}\)/B-7\(^{\rm tw}\)**: 数学内容は条件つき PASS。ただし F2.2–F2.3 を定理文へ反映するまで final artifact としては未受理。
- **T2–T6**: PASS。
- **GAP 数式修理**: PASS。
- **GAP/certificate finality と T7**: 差戻し。
- **bundle `cross-checked` 昇格**: 保留。
- **artifact 全体**: 上記五件を閉じた再提出を要する。

主定理の theorem gate を開け直す必要はない。今回残ったのは、twisted 版の量化子を正確に閉じる二行と、有限計算 bundle が「同じ最終対象を fail-closed に照合した」ことを provenance まで含めて確定する作業である。
