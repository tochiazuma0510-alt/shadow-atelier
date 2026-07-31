# 便 92 返信 — 数学便第 19 号

## 総合判定

**分割判定**とする。PENT の衝突解消は **PASS** であり、F91-2.2 の `fine-lift = 4` は撤回する。正値は、型を「粗 shadow の集合への還元」と限定すれば **20/20** である。これに基づき、衝突を理由に掛けた v4 算術鎖および集合的全射の suspension は解除する。一方、`GT(K_π)` という群の型付け・PB₄ source kernel の isolated 性・還元の群準同型性は未証明であり、こちらは解除対象に含めない。

CENT/GEN-2 は **PASS**、T3-N0′ は「重み付き個数」として **PASS**、MIX-12 は既存の K3/Thm 5.3 前件付きで **条件付き PASS**、SURJ-K7 は定理部だけ **条件付き PASS** とする。S4 の測定値そのものは紙上二経路で一致するが、repository-grade の `cross-checked` 格上げと C1′ は **差戻し**。EP v11 は世代を跨いだ A/B 混成を許す TOCTOU が残るため **FAIL / 再発効不可**。壁族 2 件は数値 payload を NOTE として受領するが、現状の cert/result は正式受理しない。

**F92-0.1（監査範囲）**　便 92 の §1–§7 を順に監査した。指定された 13 個の正本・証明書の SHA-256 はすべて便記載値と一致した。併せて v3 実行源、EP registry/resolver/consumer/workflow、関連 cert の内容を検分した。

---

## 1. PENT 衝突の決着

**F92-1.1（「4」の明示撤回）**　F91-2.2 の独立計算も、粗側の label と精側の word evaluation を対応させる段で、実質的に同じ `f` 対 `f^{-1}` の辞書を共有していた。したがって、次の二主張を撤回する。

- `fine-lift = 4`。
- 生存行を各 $m$ について自己逆元 2 個だけとした行別記述。

生存 4 行が、10 個の粗 $f$ のうち自己逆な 2 個と 2 個の $m$ の直積に正確に一致することは、この共有仕様バグの強い指紋である。精 evaluator 自体は著者の 20 words を無変更で 20/20 受理し、word reversal を施すと 4/20 に落ちる。ゆえに誤りは関係式 (2.18), (2.19) や `Chk6` ではなく、fiber を選ぶ前段にあった。

**F92-1.2（修正値）**　v3 の各 20 行について

\[
(c_1,c_2,c_3,c_4,c_5)=(5,5,5,1,125),
\]

全 6 条件 pass であり、著者 witness 20 個も同じ順序で一致する。さらに Dolgushev `PackageGT` の較正値 $N_{19}=216/36$、$N_{34}=486$、窓不変量、および 20 個の charming elements が、20 個の forward 粗 class を一つずつ覆う結果と一致する。したがって次を採択する。

> 著者の 20 個の精元は精条件を満たし、それぞれ異なる 20 個の forward 粗 target に還元する。よって、この 20 元で指定された target-shadow 集合への還元は集合として全射である。

これは `cross-checked` の数値結論として扱ってよい。診断 v1 の C-DEG と LIFT-INDEP は生存し、「上限 12」だけを撤回する。

**F92-1.3（suspension 解除の型）**　解除するのは次の二点である。

1. 衝突を理由に停止した v4 の算術値 20。F91-2.6 の算術鎖と矛盾しない。
2. 上記 20 witness による、20-element target-shadow 集合への集合的全射。

ただし、ここから直ちに `red : GT(K_π) → ...` という**群準同型**を作ってはならない。`coarse_of(WordOf(q))` は GAP representative に依存して記述されており、$q$-level の well-defined map はまだ証明されていない。また source-kernel 計算は PB₄ 水準の isolated 性を閉じていない。従って `GT(K_π)` の群、kernel quotient、および群としての全射は引き続き UNKNOWN である。

**W92-1（型付け残件）**　F91-2.5 の isolated/source-kernel 問題は残す。優先度は、v4 の数値定理および「20 個の target lift の存在」だけを述べる間は **中**、`GT(K_π)`・fiber cardinality・群全射へ昇格する直前には **最優先 blocker** とする。順序は `(i)` representative 非依存性、`(ii)` source kernel の PB₄ isolated 性、`(iii)` multiplication compatibility が自然である。

**W92-2（v3 provenance）**　数学的結論と archival cert の完成度は分ける。v3 cert の `source_digest_sha256` と `base_probe_digest_sha256` は literal `PENDING_POSTPROCESS` のままである。実行源 `search/probe/wac_v1/pent_t2t3_v3_20260731.g` の実 SHA-256 は `e6e1f67dd903a25dfc9a86fdb8b1419f37e54f39e7ddb7115e0e3b4546afcddf` である。また源の冒頭コメントには旧 `redMap` shortcut を正当化する記述が残り、後段の正しい実装と矛盾する。`unit_test_4element.reduction_image_equals_f=false` も canonical reduction ではなく `legacy_redMap_*` と明記すべきである。公開固定前に versioned cert とコメントを修理せよ。

**P92-1（再発防止）**　今後の二層 probe は、粗 class の番号ではなく、各代表 word $w$ に対して次の三角形を非自己逆元で必須試験にする。

\[
w \longrightarrow \Psi(w) \longrightarrow \operatorname{coarse}(\Psi(w))
\quad = \quad
\operatorname{forwardCoarse}(w).
\]

最低一つの $f\ne f^{-1}$ を fixture とし、fiber 選択の前後双方で assert する。自己逆元だけの unit test はこの種類のバグを不可視化する。

**★教材採択**

1. 「独立実装の一致は、独立な仕様解釈を意味しない。共有辞書の誤りは全実装を同方向へ倒す。」
2. 「evaluator が正しいことと、evaluator を正しい対象/fiber に当てていることは別物である。」

PENT はこの二命題の非常に良い実例なので、誤った 4 と修正後 20 を共に残す教材化に賛成する。

---

## 2. CENT erratum と T3-N0′

**F92-2.1（CENT erratum）— PASS**　`docs/notes/sat_l1_v2.md` §2 の置換を採択する。hand 座標と $q=f_{\rm hand}^{-1}$ の衝突は解消され、

\[
\bar x^{a_1}=(gh)^2,\qquad (\bar y^f)^{a_1}=(hg)^2
\]

が正しい。$A_n\le \langle g,h\rangle$ は前件でなく、shadow surjectivity と sign の議論から得る結論である。

**F92-2.2（GEN-2）— PASS**　$H=\langle v^2,(v^2)^g\rangle$ と置く。`ord(v)` が奇なら $v\in\langle v^2\rangle\le H$、かつ $H^g=H$ なので $H\triangleleft K=\langle v,g\rangle$。$A_n\le K\le S_n$ であり、$H\cap A_n\triangleleft A_n$。単純性から、交わりが $A_n$ でないと仮定すれば $H\hookrightarrow K/A_n$、従って $|H|\le2$、さらに $|K|\le4$ となり矛盾する。ゆえに $A_n\le H$。これは `p=s=0`、すなわち当該 odd-order 範囲の GAP-S1 を閉じる。`p,s>0` へは拡張しない。

**F92-2.3（T3-N0′）— PASS、ただし重み付き**　葉の dart への自己同型作用は自由であり、任意葉根付けの個数は

\[
(m+1)\sum_D \frac1{|\operatorname{Aut}D|}
\]

となる。$R=(u+z)Y+\lambda W^2$ から

\[
R=sW-2\lambda(u+z)-\lambda^2

\]

を得て、総次数 $m+1\ge3$ では補正項が消える。最後に $m+1$ で割る導出は $t=0$ を含めて一様である。さらに $t=0$ のとき $m\ge2$ は自動なので、旧来の特別根付け条件は不要である。

**W92-3（T3 の語義）**　解除できるのは T3-N0 の「$t=0$ 未処理」という条件である。一般に得た量は

\[
\sum_D 1/|\operatorname{Aut}D|
\]

であり、無重みの Nielsen class 数 $N$ とは限らない。従って T3-CLASS を全範囲で「連結被覆の個数」と読むなら未採択である。自己同型が自明になる generation/Jordan 範囲では両者が一致するため、T3-WALL はその範囲で定理として採択してよい。「T3 系完全採択」は、全域を weighted theorem と書き、無重み化に `Aut=1` を付けることを条件とする。

---

## 3. MIX-12 と (U2)

**F92-3.1（MIX-12）— 条件付き PASS**　直接経路は正しい。K3/K4 の固定体を $L_3,L_4$ とし、既監査の交わり $L_3\cap L_4=\mathbf Q(i)$ を使えば、compositum の次数は target order 24 に等しい。独立には

\[
L_3L_4=\mathbf Q(\zeta_{24},\sqrt[3]{2}),
\]

かつ $3\nmid [\mathbf Q(\zeta_{24}):\mathbf Q]=8$ なので $X^3-2$ は cyclotomic field 上既約、従って同じ次数 24 を得る。D6 の fibre-product 単射と D7 の自然性を合わせれば kernel intersection も従う。P-e/P-f は MIX-12 の依存から除去してよい。

この判定は K3 および Thm 5.3/D7 の既存の framework 前件を継承する。その意味で suspension は **MIX 固有の欠落について解除**し、絶対定理への昇格とはしない。

**P92-2（U2 要請票）**　(R1) 実際の有限 quotient $G_{2^\alpha}$、(R2) 基点・内外作用の規約、(R3) 実際の有限 Galois extension、の三点を固定してから文献照合する設計を承認する。抽象的な pro-$2$ 記述だけで finite-level map を補うことは禁止する。

---

## 4. q7 修文と class number

**F92-4.1（SURJ-K7）— 定理部のみ条件付き PASS**　SURJ-K7 と SURJ-K7-APPLY の分離は適切である。SURJ-K7 は明示された framework antecedents の下の定理として採択する。実窓への適用は G-1 C1′、G-2 C5、G-3 model binding、G-4 provenance が閉じるまで UNKNOWN のままである。従って「実際に全射」はまだ主張できない。

**F92-4.2（G7-NOGO′ と LB-RES）— PASS**　NOGO の射程を「裸の二本の (T) だけから行う一様消去」に限定した修文は正しい。LB-RES の三段

\[
\text{valuation}\longrightarrow \mathrm{Cl}(F_7)[7]
\longrightarrow \mathcal O_{F_7}^{\times}/(\mathcal O_{F_7}^{\times})^7
\]

も正しい。中段は、$(\alpha)=\mathfrak a^7$ から $[\mathfrak a]\in\mathrm{Cl}(F_7)[7]$ を取り出す段である。従って M2⁻ の空振りだけでは単数段を何も決めない。

**F92-4.3（G7-3 の出典）**　$F_7=\mathbf Q(\zeta_{28})$ の class number は 1 である。正典出典として、Masley–Montgomery, *Cyclotomic fields with unique factorization*, J. reine angew. Math. 286/287 (1976), 248–256, [DOI 10.1515/crll.1976.286-287.248](https://doi.org/10.1515/crll.1976.286-287.248) を採用できる。同論文の class-number-one cyclotomic fields の分類に conductor 28 が含まれる。従って、とくに $7\nmid h(F_7)$ であり、class obstruction は消える。

**W92-4（残る単数段）**　class number 1 は下界を自動的に閉じない。$F_7$ は次数 12、完全虚で unit rank 5、torsion は $\mu_{28}$ だから

\[
\mathcal O_{F_7}^{\times}/(\mathcal O_{F_7}^{\times})^7
\simeq C_7^6.
\]

1 次元は torsion、5 次元は free units から来る。残余単数のこの 6 座標を計算・証明しなければならない。

**P92-3（G7-3′）**　principal generator を一つ固定し、残余単数を $\zeta_{28}$ と 5 個の fundamental units の基底で表し、その指数ベクトルを mod 7 に落とす。このベクトルと model binding を同一 cert に束縛するのが次の最短路である。

---

## 5. S4 の $u$ 測定

**F92-5.1（厳密局所値）— 紙上 PASS**　与えられた曲線と係数は 6 本の分岐条件を厳密に満たす。指定 cusp ∞₊、parameter $s=1/x$ では、局所展開の最高項は $c_{\rm lead}=8c_9=1423828125/256$ であり、U-LOC の規約から

\[
u_0^{-1}=-c_{\rm lead}
=-\frac{1423828125}{256}
=-\frac{3^6 5^9}{2^8}.
\]

ノルム側でも $\delta^2=-27/4$、$\kappa=-c_{\rm lead}\delta$ から $\kappa/\delta=-c_{\rm lead}$ となり、同じ値を得る。したがって数式としての値は採択する。

**F92-5.2（`cross-checked` 格上げ請求）— 差戻し**　`u_meas_m7b_20260731.json` は第二経路を記述しているが、生成プログラム、再現 command、source/input digest を含まない。追加 commit にも cert と ledger しかなく、`machine-piped/helper-disjoint` を第三者が再実行できない。M7-B4 の 12 素点は曲線の整合性確認であって $u_0^{-1}$ の値の独立計算ではない。

従って現段階の grade は「二つの紙上恒等式が一致した強い candidate」であり、リポジトリ規約上の `cross-checked` には上げない。B1 の versioned checker、厳密 input/source digest、再現 command と raw log を追加し、U-LOC 経路と helper を共有しないことを示せば格上げできる。Belyi DB の検索結果 `ABSENT` は、その明記された収録範囲内の不在としてだけ受領し、新規性・世界的不在の根拠にはしない。

**F92-5.3（M6 の算術）— 条件付き PASS**　上の有理数は $v_2=-8\not\equiv0\pmod3$ なので $\mathbf Q$ の立方ではない。もし $\mathbf Q(\zeta_9)$ で立方になれば、その純三次根が作る三次部分体は abelian extension の部分体として Galois でなければならないが、非自明な pure cubic field は Galois でない。従ってこの値は $\mathbf Q(\zeta_9)^\times/(\cdot)^9$ で位数 9 を持つ。この算術 implication 自体は正しい。

**W92-5（C1′）— blocker、未証明**　U-LOC cert 自身が `c_C1prime.status = NOT PROVED HERE` と申告しており、必要な `(j-table, class_vector)`、とくに対象 diagonal class `[0,0,0]` との照合がない。240 個の Frobenius cycle type が PΓL(2,8) の許容型内にあり 7-cycle が出たことは、primitivity/整合性の強い evidence にはなるが、有限標本から geometric monodromy が正確に 9T27 = PΓL(2,8) であること、まして 6 個の $W$-dessin のうち指定した diagonal lift であることは証明できない。

従って、測定した $u_0$ と判定表の intrinsic $u$ の同一視は UNKNOWN、`Ih_{S4}` 全射は依然 candidate であり、定理候補へは上げない。さらに既存の `surj_s4_v2` が持つ A3/Z18-link 等の framework 前件も別途残る。

**P92-4（C1′を閉じる証明書）**　最低限、次を一体で束縛する。

1. exact degree-9 cover と geometric monodromy 9T27 の証明（resolvent または明示 permutation representation）。
2. branch-cycle $j$-table と class vector、指定 diagonal `[0,0,0]`。
3. quotient dessin から当該 $W$-lift への一意な binding。
4. curve/model/cusp/parameter と U-LOC cert の全 digest。

**P92-5（n=7 転用）**　転用してよいのは、exact model → gate → preregistration → 全付値付き U-LOC → helper-disjoint norm checker、という装置の順序だけである。S4 の数値・quotient rigidity は転用しない。n=7 では先に $H_{2,1,0}$/α-orbit、C1′(7) の class vector、cusp/parameter、M0 の mod 2 と mod 7 の双方を凍結してから測定を発火せよ。

---

## 6. EP v11 generation commit

**F92-6.1（総合判定）— FAIL / 再発効不可**　generation directory、bundle receipt、path confinement、`samefile/realpath`、consumer の freeze 必須化など、F91 の多数の blocker は正しい方向に修理されている。しかし A/B の atomic bundle 解決に blocking race が残る。

**W92-6（同一 freeze・異世代混成 race）**　consumer の `_resolve_native_registry()` は A と B について `registry.resolve()` を別々に呼ぶ。各 `resolve()` はその都度 `CURRENT.json` を再読するが、返り値には generation ID がなく、consumer が比較するのは `freeze_id` だけである。次の interleaving が許される。

1. `CURRENT=G0` で A₀ を解決する。
2. publisher が `CURRENT` を G1 へ atomic replace する。
3. B₁ を G1 から解決する。
4. G0 と G1 が同じ freeze ID を使えば、A₀/B₁ は freeze 一致検査を通る。

各 entry と各 generation receipt が個別に正しくても、混成 pair A₀+B₁ を束縛する一つの receipt は存在しない。これは generation commit が提供すべき reader atomicity を破る TOCTOU であり、blocker 9 の閉鎖にはならない。現行の負例は「異なる freeze」の混成しか試しておらず、この反例を捕捉しない。

**P92-6（必須修理）**　registry に `resolve_bundle([A_ref,B_ref])` を設け、`CURRENT`、index、bundle receipt を一回だけ読み、その同じ generation から両 artifact を返すこと。返り値にも generation ID を含める。代案として generation ID を最初に pin して全 lane を同じ ID で引く実装でもよいが、lane ごとに `CURRENT` を再読してはならない。二世代が**同じ freeze ID**を持ち、第一 lookup 後に CURRENT を差し替える race test を追加し、混成受理が不可能または fail-closed になることを示せ。

**F92-6.2（設計判断 3 件）**

- 旧 flat 3 ファイルは runtime から完全に inert なら、一移行期間の残置を NOTE として許容する。ただし production provisioning 時には quarantine/remove し、future fallback が再利用しないことを明示する。
- 旧 API の `NotImplementedError` stub は fail-fast migration として一時的に妥当。docstring の旧 `write_entry` 記述を直し、caller 消滅後に stub も削除する。
- generation 内を「同一 freeze の任意個 artifacts」に一般化すること自体は許容する。EP consumer が必要な A/B role を exact に要求し、上記の**同一 bundle resolve**を行うことが条件であり、registry 全体を二 lane に狭める必要はない。

**F92-6.3（cake_lpr）**　manifest 欠品の fail-closed、拒否 token の厳密化、TIMEOUT/CRASHED/LOADER_FAILURE の分離は、静的 inspection では PASS。ただし実 Actions run と production A/B artifact/receipt がまだなく、EP 結果の発効根拠にはならない。

**W92-7（テスト再実行）**　こちらでも suite 再実行を試みたが、最初の registry suite が sandbox の `%TEMP%` 配下で `PermissionError [WinError 5]` となったため、551/551 を独立確認できなかった。これはコード反例とは数えないが、こちらから再実行済みとも記録しない。上記 race はテスト環境とは独立な静的反例である。

**W92-8（再入場条件）**　EP 再発効には、少なくとも `(a)` bundle resolver と同一-freeze race 負例、`(b)` その修理後の全 suite receipt、`(c)` 実 A/B production artifacts と bundle receipt、`(d)` 実 CI run receipt、が必要である。

---

## 7. 壁族 4/4 の情報受領

**F92-7.1（数値 payload）— NOTE**　cert 内の wall36 `3720/3720`、wall37 `22320/22320`、hexagon/generation failure 0、`eq_centralizer_w0=true` は確認した。数値内容を否定する反例は見ていない。ただし本便では informational scope に留め、再計算監査や claims promotion は行わない。

**W92-9（schema と verdict は cosmetic ではない）**　両 cert の schema が `wac_v1-wall28-cert/v1` であり、対応する `result.txt` が literal `verdict=failed` である以上、fail-closed consumer にとっては正式失敗である。完走 marker 名の不一致が算術値を変えないことと、成果物が gate を通ることは別問題である。

窓別 schema の versioned cert を生成し、正しい completion marker を用いた driver で再走して `verdict=passed` の receipt を得るまで、「壁族 4/4 完結」を provenance/CLAIMS の確定主張には記載しない。現 payload は修理再走の照合対象として保存してよい。

---

## 最終裁定一覧

**F92-8.1**　PENT: `4` を撤回、target-shadow の `20/20` を採択。v4 算術と集合的全射の suspension を解除。`GT(K_π)` の群型付けは保留。

**F92-8.2**　CENT/GEN-2: 採択。T3-N0′: $t=0$ を含む weighted theorem として採択。無重み化は `Aut=1` 条件付き。

**F92-8.3**　MIX-12: framework 条件付き採択、P-e/P-f を依存から削除。

**F92-8.4**　SURJ-K7: conditional theorem を採択、APPLY は保留。$h(\mathbf Q(\zeta_{28}))=1$ を採択し、残件を $C_7^6$ の unit stage に絞る。

**F92-8.5**　S4 $u_0^{-1}$: 値の紙上式を採択するが `cross-checked` 格上げは差戻し。C1′未成立につき全射は candidate のまま。

**F92-8.6**　EP v11: bundle race により FAIL、再発効不可。

**F92-8.7**　wall36/37: 数値 NOTE のみ。schema/verdict 修理再走まで正式完結としない。
