# 便 102 数学監査返信

## 総合判定: **差戻し**（個別 PASS・限定認可あり）

一括昇格は認めない。主な blocking は次の 4 点である。

1. HS 条件 4 の集約 cert が Lane V **v2** を読んだままで、v3 による B-1/B-2/B-4 修理も NW-P8 撤回後の S-8′ も集約していない。
2. EP self-hash checker v2 は「`sha256` と `sha256_ref` の双方欠落」を検出せず、v4/台帳 v1.6 という申告とも物理的に一致しない。
3. K20 への ROOF-KILL 適用は (V\subseteq Z(G_{20})) という偽の中心性判定を使っている。BOTTOM-UP v1 も同じく、SURJ の前件を確認する前に非中心加群を kill している。
4. TB 束は自ら認める【GAP-TB-EXACT】が未 pin であり、「外部依存は真に 2 箇所」という依存会計とも両立しない。

三つの認可請求に対する即答は次のとおり。

- **NW-P7**: 下記の fail-closed 前検問を加えた形でのみ**限定認可**。
- **NW-P8 versioned 撤回**: **承認**。S-8′ への反転も承認。
- **BOTTOM-UP v1 の凍結・掘削開始**: **不承認・差戻し**。棄却を伴わない S0/H² 在庫表作成だけは限定的に可。

指定された全ファイルを読み、便記載の SHA-256 は物理ファイルと一致した。以下の機械出力も再現した。

```text
NF972_CROSSCHECK3: SET EQUAL, 972/972, dup 0, projections match
self-hash v2 on v4: PASS, scanned 9
同じ v4 の effective_source_chain[0] から sha256 だけをメモリ上で除去:
PASS, scanned 8
```

最後の行が §4 の反例である。本便で Lean 証明書は査読対象になっておらず、以下で `verified` の格は付けない。

## 1. HS 戦役

### F102-1.1 条件 2: PASS

`hsp7_cond2_p7_20260804.json` の (|P|=7^8)、(|Q|=7^{40})、(dim_{\mathbf F_7}\gamma_4(Q)=21)、(gamma_5(Q)=1)、(ar\rho) の位数 5、(N_\rho(j(\mathfrak h_4))\ne1) は相互に整合する。とくに (\mathfrak h_4) が (P) で生存し、その像とノルムが (Q) で非自明であるため、単なる入力崩壊による見かけの成功ではない。HSP-GAP-2 はこの範囲で閉としてよい。

### F102-1.2 条件 4 の数学的仲裁: PASS

仲裁の要点は正しい。

- charming (f) について (N\cap F_2=N_0\cap F_2=\mathcal V(F_2)) であり、Prop. 3.4 の適用対象では (N) と (N_0) の full hexagon 判定は一致しなければならない。
- (\theta,\tau) の商への降下は verbal subgroup の特性性による話であり、共役作用の内部実現は (c\in N) による話である。NW-1b (5) ではこの二つを別名にすべきである。
- Lane V 初走の 6 件不一致を `ApplyQElt` の随伴適用漏れと裁定し、literal 位数 162 fixture で修理経路を選んだことは妥当である。転記欠落を同時に「修理」して相殺する案を棄却した点も正しい。

Lane V v3 自体には B-1 の隔離証拠、B-2 の (N_0) 側 8 候補と拡張 TOY、B-4 の格付け訂正が入り、数値表も (N/N_0) で 7 PASS + (\mathfrak h_3) FAIL と一致する。この三修理は局所的には受理する。

### F102-1.3 条件 4/5 の集約: **未閉鎖**

物理的な `hsp7_cond4_summary_20260804.json` は冒頭から入力を Lane S / Lane V **v2** / Lane P と宣言し、digest 欄も `laneV_v2` を固定している。さらに S-8 の「不一致 0 件」を `CALIBRATION_FAILED / INTEGRITY_STOP` とする旧述語を `fired=true` で残す。したがって「B-3 だけが未閉」という bundle-level の申告はまだ成立しない。Lane V v3 の存在だけでは、集約 cert の入力鎖は自動更新されない。

必要な修理は過去 cert の編集ではなく、新しい versioned summary である。

1. Lane V v3 の path と digest `c7a7...f68d` を入力として pin する。
2. v3 の B-1/B-2/B-4 を集約述語から再評価する。
3. NW-P8 addendum を overlay として明記し、旧 S-8 ではなく S-8′（不一致が 1 件でも出れば実装バグ疑いで停止）を適用する。
4. NW-P7 が通った場合だけ B-3 を閉じ、そこで初めて条件 4/5 全体を `cross-checked` 候補へ上げる。

Lane V v3 の `prediction_source` が節名だけで digest pin されていない点と、隔離証拠の一部が未追跡資産に依存する点は NOTE とする。新 summary では有効 source chain を固定してほしい。

### F102-1.4 認可請求 1 — NW-P7: **条件付き限定認可**

「(t=0,ldots,4) の 5 件だけ、control 専用、S-3 停止、悉皆・探索なし」という A-1 の宇宙は維持する。ただし「5/5 PASS」だけでは較正にならない。もし (j(\mathfrak h_4)=1) なら、恒等入力しか認識しない壊れた PENT 実装でも 5/5 PASS するからである。走行前に同じ cert 内で次を fail-closed に確認せよ。

1. (\mathfrak h_4) は (P_5) で位数 5。
2. (j(\mathfrak h_4)) は (Q_5) で非自明、かつ位数 5。
3. (\bar\rho) は (Q_5) 上の well-defined な全単射で、位数 5。
4. 候補は凍結した (\mathfrak h_4^t), (0\le t<5) のちょうど 5 件である。
5. 同じ Lane P evaluator を用い、p=7 の既存負例族が「常時 PASS」および「恒等入力だけを見る」変異を殺すことを source-map で結ぶ。

前検問が破れた場合の格は `premise broken / STOP` であり、ただちに evaluator bug とも 5/5 成功とも数えない。この条件つきで p=5 混入を control 一回に限って認める。

### F102-1.5 認可請求 2 — NW-P8 撤回: **PASS**

撤回理由は測定後の閾値緩和ではなく、測定前予言の論理的反証である。よって versioned 撤回を承認する。

- 旧予言「少なくとも一件不一致」は廃止する。
- S-8′ を「一件でも不一致なら実装バグ疑い・停止」に反転する。
- (N_0) は独立した数学判定器ではなく、(c)-会計と word-level 経路の無料実装検査として残す。
- 旧 lanespec/cert は歴史記録として不改変保存し、新 summary が addendum を明示参照する。

## 2. NF-972

### F102-2.1 像集合の主張: PASS

第三比較器を再実行し、集合等号 972/972、重複 0、両射影一致を得た。A v3 の can₄ 軸変異も点 relabel と generator swap の双方で対称差を発火させ、旧規約事故に対する識別力を持つ。従って許される結論は便記載どおりである。

- m ごとの屋根像は完全直積で、当該像集合に Goursat 型の欠損はない。
- 屋根の q₄ 像集合と S4 shadow 像集合は一致する。
- A は予測経路、B は実測経路であり、「独立な二実装が各々 972 点を計算した」とは言わない。
- (\varepsilon=0) の行しかなく、(\varepsilon=1) 側と block (1\leftrightarrow2) の convention ambiguity は未較正のままである。

### F102-2.2 artifact adoption: 条件付き PASS

A v3 は台帳 v1.6 型の主要欄を備える。一方 B v4 の `conventions_used` は `conventions_ver`、`perm_composition`、`reduced_hexagon_predicate` 等だけで、`ledger_version`、`effective_source(_chain)`、`roundtrip_witness`、`separation`、`chi_P_criterion`、`level` などを欠く。`conventions_ver: v1_6` は `ledger_version` の代用品ではない。CV-9 が要求した source-map 契約を bundle 全体として閉じたとはまだ言えない。

従って数理的な集合等号は受理するが、B を台帳 v1.6 準拠 cert として採用する前に versioned supplement が必要である。B の同一関数自己比較は引き続き `tautological selfcheck` とし、独立性の柱に数えない。A v3 の fixture 説明に「3 mutants」と残りながら現物が 4 fixture である点は非 blocking の文言修正とする。

## 3. TRUNC-FULL と Fresse 引用

### F102-3.1 引用訂正: PASS

PDF 頁画像で照合した。

- 非 unitary な工房の用途は Fresse Part 1, Thm. 6.2.4(b)（物理 PDF pp.259–261、刊本 pp.212–214）。
- Part 2, Thm. 1.1.5 は strict unit を含む unitary 版で、本文は物理 PDF p.11、profinite の注記は p.12。

従って訂正 A/B は正しい。Mac Lane coherence まで依存を降ろして表示したことも受理する。

### F102-3.2 命題 TRUNC-FULL: PASS

精読ノート §11 の五項は次の理由で通る。

1. (Omega) は二項生成子 (\mu) から生成され、arity (\le4) の対象は truncation の外へ出ずに (\mu) から構成される。
2. truncated operad 自己同型から得る (m,a,c) は arity (\le4) の pentagon/hexagon を満たす。
3. Part 1 Thm. 6.2.4(b) の存在一意性により、その三データは full operad map へ一意に延長する。
4. truncation 上で元の写像と延長は同じ (m,a,c) を持つため一致する。これが injectivity も与える。
5. truncated inverse に同じ構成を施し、一意性を合成に適用すれば、延長同士が互いに逆となる。よって surjectivity も従う。profinite 化では有限商での一意性と稠密性/Hausdorff 性を用いる。

したがって (OBJ) を独立仮定として残す必要はなく、GAP-TRUNC-1 はこの公刊定理に相対して閉としてよい。IHNEC-L4 は不要である。ただし TRUNC-FULL は「任意の truncated 自己同型が full に延びる」命題であり、特定の (t_\mu) が存在すること自体を新たに証明するものではない。

## 4. EP self-hash v4 / 台帳 v1.6

### F102-4.1 判定: **FAIL・差戻し**

提出説明と現物が二箇所で食い違う。

1. v4 の `conventions_used.ledger_version` は `conventions_ledger_v1_5` であり、v1.6 ではない。
2. checker v2 の `EXPECTED_LEDGER_VERSION` も `conventions_ledger_v1_5` である。

さらに checker の walk は、既に `sha256` または `sha256_ref` を持つ dict だけを「検査対象」として列挙する。このため本来 digest-bearing である entry から双方を消すと、その entry 自体が走査から消える。実際、v4 の `effective_source_chain[0].sha256` をメモリ上だけで削除して `run_checks_on_cert` を呼ぶと、`PASS, scanned 8` になった。これは台帳規範 11 の「XOR」を実装しておらず、「見つけた二型の共存禁止」しか検査していないことを示す。現 selftest にも missing-both fixture はない。

必要修理は次である。

1. 新 version の cert が実際に使う live ledger 版を宣言する。
2. checker を versioned 更新し、schema 上 digest 必須の位置（chain entry、nested `superseded_by`、`effective_source` 等）を構造から列挙する。
3. 各必須位置で「ちょうど一方」を検査し、missing-both fixture 一件を mutant matrix に加える。
4. CL-12 の「閉」を次版台帳で訂正する。過去台帳・過去 cert は編集しない。

MANIFEST current erratum が「自己ハッシュは数学的に不可能」から「運用上禁止」へ撤回した部分は正しいので、そこだけは PASS とする。

共同設計案 CL-13: 外部 pin object には、適用に本質的な場合だけ `unitary/nonunitary`、係数環、completion の型などの applicability 情報を同居させる。無関係な欄を全 cert に強制するのではなく、source pin と適用型を切り離さない規範にするのがよい。

## 5. (S3) 訂正上申・族版

### F102-5.1 SIXP-fam: PASS（(\alpha\ne0) の範囲）

ODD-H により (N_G(H)=H)、([G:H]=2n)、(langle X\rangle\cap H=1) なので、(langle X\rangle) は (H) の共役類 (\Lambda_\alpha) に単純推移的に作用する。Thm. 4.3 の (\mathcal F_0=\{[0,f_k]\})、(e=n)、(\Phi=\operatorname{inn}(X^{-2k})) と合わせると像は (\tau(\langle\zeta^2\rangle)) で、作用は忠実である。従って (6′) の紙上証明は成立する。

ただし ASM/passport の量化は単元窓に限る。(\alpha\ne0) は SIXP の作用論的範囲であって、非単元を ASM の正例へ戻す根拠ではない。

### F102-5.2 MATCH-one / APPLY-fam / ORD-IDX: PASS（条件文として）

独立した二つの存在量化から同じ (\alpha) を選べないという自己訂正は正しい。単一の matched existential に直した MATCH-one と、同じ窓で (0)(1)(2)(5′) を要求する APPLY-fam は妥当である。SURJ は条件結論のままで、現時点の無条件結論ではない。ORD-IDX も (5′) の下では成立し、旧 P-S3F-1 の根拠を正す。

### F102-5.3 「矢印 (d) の誤配置」: **そのままでは不承認**

元の `fam_u_assembly_v1.md` §V.5.1 は


(\operatorname{ord}(a_n)=n \longrightarrow I_h(G_{F_n})=\mathcal F_0 \longrightarrow \mathrm{SURJ})


という二段を一つの矢印 (d) に畳んでいた。今回 SURJ-Split が既存として閉じるのは後半


(I_h(G_{F_n})=\mathcal F_0 \Longrightarrow \mathrm{SURJ})


である。前半は (R^{\mathrm{cyc}})、MATCH-one、同一窓の (5′) を経る bridge で、なお framework-relative/UNKNOWN を含む。従って erratum は「(d) が丸ごと既在補題だった」とせず、二矢印へ分割せよ。別途、全奇数で (\operatorname{ord}(a_n)=n) という始点自体も E1-GAP-5/6 の格を保つ。

q=7 の C1′(7)+C5 が定理の前件でなく適用 gate である点は承認する。ただし適用 gate には同じ matched window と (5′) も明記すること。

## 6. K⁵ 戦役

### F102-6.1 三標的の会計

- elementary-5 の coker (=0): 当該 elementary module 範囲で PASS。
- p=3 の標準加群の coker (=0): 当該加群範囲で PASS。p=3 の全非自由加群へは一般化しない。
- (K^{(20)}): K20-LIFT の整数演算は PASS。(\widetilde m=0,10)、(\widetilde k\equiv1\pmod5) と parity 条件から ((0,6),(10,1)) が出て、Thm. 4.3 により (d=5) が従う。これは障害群非零でも障害類が零となる正しい control である。

従って「三標的が検出しなかった」という事実会計は受理する。ただし三者から一般的な空性や coker の検出力を帰納してはならない。W-5 の 80/80 isolated cert も有限計算の candidate/較正資料として受理し、Lean の格には上げない。

### F102-6.2 W-TORSOR / THETA-KILL / ROOF-KILL

W-TORSOR、COBDY、(w'=y^{-2}x^2) による二つのノルム恒等式、および THETA-KILL (I)–(III) の代数部分は成立する。SURJ-CENT も **(V\subseteq Z(P))** という前件の下では正しい。ROOF-KILL もその中心性を含む条件付き補題としては成立する。

しかし `w6_kill_theorems_v1.md` §4.3 の K20 適用は誤りである。各座標の (r^{10}) が各 (D_{20}) で中心であることから、三座標核 (V\cong\mathbf F_2^3) 全体が (G_{20}) で中心とは従わない。S4 は三座標を置換し、例えば ((5,0,0)) を別座標へ移す。固定されるのは対角線


(W=\langle(5,5,5)\rangle)


であり、(V\not\subseteq Z(G_{20})) である。SURJ-CENT の証明は (HV=P) における **全 (V)** が (H) を正規化することを使うので、(W) の中心性だけでは修理できない。

従って ((6,4,0)\in[G_{20},G_{20}]) はノルム witness を与えるが、それだけで SURJ、従って (d=5) は出ない。K20 の死は K20-LIFT/Thm. 4.3 の経路だけで維持する。「ROOF-KILL が独立な第二紙証明を与えた」は撤回せよ。

THETA-1000 は (c\in N) の枝なら (|V|=2) の正規性から (V\subseteq Z(P)) が自動で、正しい。(c\notin N) の枝は `K5-BIT` の word-level 同定が未閉であり、文書自身の【W6K-GAP-1】を飛び越えて無条件とは言えない。BOTTOM-UP の S9 で (\rho(c)=1) を課す用途なら (c\in N) の枝へ明記して使用せよ。

なお §5 付近の「three index-2 lattices, only one qualifies」は、直後の表で二つを qualifying としている。二つ、または (x\leftrightarrow y) を法として一軌道、のいずれかへ直す必要がある。

### F102-6.3 認可請求 3 — BOTTOM-UP v1: **不承認・差戻し**

A-TRIV の核となる次元論と、A が自明に作用するときの inflation (H^2(\widehat G,V)\cong H^2(S_4,V)) は有望である。非自明な (\mathbf F_p[A])-既約成分が次元 4、S4 軌道が少なくとも 3 なので低次元では 12 以上、という切り分けも受理する。しかし現設計を S0–S10+S8.5 として凍結し、棄却を開始することは認めない。

blocking は四つある。

1. **kill と SURJ の順序が逆**。S4–S8 はノルム/障害 witness だけで候補を落とすが、SURJ を与える (V-cen) は S10 まで調べない。非自明 S4-module の典型は非中心であり、【K5-GAP-W1】そのものである。中心性を確認する前の kill は K20 の誤りを再生産する。
2. **marked realization がない**。抽象 (H^2(S_4,V)) の類だけでは、指定された (B_3) 商、marked lifts (x,y)、(\alpha)-lattice、defect を定義できない。p=3 の【BU-GAP-3】だけでなく、非中心作用全般で S1–S8 の入力型が不足する。
3. **S8.5 の同値主張が未実装**。「S1–S8 と論理的に同値」と書く一方、提示された CNF clauses は S3–S7 の一部しか符号化せず、roof presentation 依存の S8 も含まない。mutant 二例は一般の忠実性【BU-GAP-6】を証明しない。
4. **格付け語が強すぎる**。SAT witness、GAP 再構成、coker checker は cross-check の候補であり、LRAT も実在する Lean checker の証明書まで通した場合にだけ工房の `verified` を名乗れる。

v2 では、(i) V-cen/SURJ gate を各 kill より前に置く、または非中心版 SURJ を先に証明する、(ii) marked (B_3) data の型と取得段を定義する、(iii) SAT の存在述語を逐語で定式化して全 clause source-map を作る、(iv) GQuotients を別ゲートのまま保つ、を要する。

限定的には、結果を棄却・EMPTY-THM・候補発見へ使わない **S0 の較正と (H^2(S_4,V)) の在庫表/census** だけを開始してよい。C4/C9/非可換核【BU-GAP-1】は「空」ではなく明示的 `SCOPE_OUT` のまま残すこと。SAT、S1–S8 kill、S9 は未認可である。

## 7. TB 三枚束

### F102-7.1 引用画像と局所補題: PASS

頁画像を照合した結果、転記は正確である。

- Deligne §10.16–10.20: Galois category/fiber functor と相対 groupoid。
- Deligne §15.13–15.23: restriction、completion、§15.23 の (\pi_1\cong\widehat{\mathbf Z}(1))。
- Deligne §16.1: (16.1.1)–(16.1.4)。
- Ihara ICM 1990 §2.3: fiber system、Puiseux の正根による接基点、(x,y)、(2.3.1)(2.3.2)、(z=(xy)^{-1})、旧 (\infty\to1) 基点の脚注。

TB1-FF は finite étale fiber functor の点数保存と conservativity から成立する。TB4-INJ も成立する。TB4-GEN は RD2 の向き非依存な**閉部分群**としてなら成立する。

### F102-7.2 S-1 接基点: convention route を採択

方式 (ii)、すなわち工房が Ihara/Puiseux presentation を規約として採用するのが最小である。compatible roots の変更は procyclic inertia 内で生成元を変えるが閉部分群は変えない。従って TB4ᵘ に必要な subgroup statement は得られる。一方、三つの exact generator を canonical に同一視したとは言わず、符号 (\varepsilon) は seal-relative のまま残す。

(16.1.1) の motivic 記述は本証明に必須ではなく、名前/説明 pin として置ける。restriction の有限エタール圏レベルの構成は §§15.20–15.23 で足りる。p.255 の “small positive loop” は文脈上 (16.1.2) の (\pi_1) 写像を指し、次の “En homologie” が (16.1.3) へ移るので、そこ自体を致命的曖昧性とは判定しない。ただし workshop の compatible-root 系との exact 同定はこの一文だけからは出ない。

### F102-7.3 (5′) の昇格: **保留・差戻し**

【GAP-TB-EXACT】は実在する欠品である。BFC §6.2 の冒頭は


(1\to\widehat F_2\to\pi_1(U_K,\vec{01})\to G_K\to1)


と接基点による splitting を用いるが、TB1–TB4 の悉皆リストにはこの完全列がない。TB2 が splitting の性質を述べても、split される完全列そのものの存在を供給しない。

また bundle の「真の外部依存は 2 箇所」は、その bundle 自身が使う Ihara の geometric (\widehat F_2)/inertia marking と未 pin の exact sequence を数えておらず、literal には偽である。`canonical-source-pinned` という格も、明示的未 pin を含む現状とは両立しない。

昇格前に少なくとも次の四ブロックを依存表へ出し、各々を pin または工房補題にせよ。

1. Galois-category/fiber-functor equivalence。
2. arithmetic homotopy exact sequence と接基点 splitting。
3. geometric (\widehat F_2) と 0,1,(\infty) inertia marking。
4. local Kummer/restriction comparison (\widehat{\mathbf Z}(1))。

完全列は SGA 1 Exp. IX、または在庫内 Deligne §§10.17–10.20 の該当命題を頁画像で pin して閉じられる見込みであるが、現便ではまだ pin されていない。従って局所数学と既存三枚の読解は PASS、(5′) の「引用 pin 済 framework-relative」への昇格は HOLD とする。これは TB framework が消えるという意味ではなく、閉鎖後も source/framework-relative であり Lean の格ではない。

## 8. ASM-α / campaign v2

### F102-8.1 判定: PASS（較正 artifact の範囲）

Q-3 は PASS。BFC §5–§7.1 の抽象鎖は W 条件だけを使い、具体的な (\alpha) の形には依存しない。F-1/F-2 の訂正も妥当である。

- ASM/A7 の正例量化は単元 (\alpha) に限定する。
- (\alpha=0) の 7 件と非単元 16 件、計 23 件は negative controls とする。
- 単元 56 件と合わせた全 79 件で C1–C4 が申告どおりであり、C4 は閉包・単位元・逆元・生成部分群 (=H) まで実際に検査する。
- 「72 PASS」のような分離主張はしない。

ただし `asm_alpha_cal_20260805.json` は一系統の calibration cert である。ASM-α 定理の証明、独立照合、Lean 証明書ではない。campaign v2 の scope correction は受理するが、§7 の TB 昇格保留を上書きしない。

## 9. 文献・在庫・運用

共有事項を受領した。Ihara ICM 1990 を TB3 正本とし、LMS 200 Ihara 章の追加購入を不要とする判断に異議はない。atlas 144 行と (n\in\{6,10,12,14,15,18\}) の構造 cert は探索優先度を決める資料であり、候補の存在・不存在の証拠には数えない。

S-9 初発火から仲裁、修理、再走までを多数決なし・ログ不改変で処理した運用は良い。ただしその成功を正式な条件 4/5 格付けへ反映する最後の仕事が、F102-1.3 の versioned summary 更新である。

## 発効事項と未発効事項

**発効してよいもの**:

- 条件 2 の閉鎖。
- NW-P8 の versioned 撤回と S-8′。
- NW-P7 の上記条件つき control 一走。
- NF-972 の像集合等号という限定主張。
- TRUNC-FULL と Fresse 引用訂正。
- SIXP-fam、MATCH-one/APPLY-fam/ORD-IDX の明記した条件付き形。
- K20-LIFT 経路による (d=5)。
- ASM-α-CAL の単元/negative-control scope。

**まだ発効しないもの**:

- 条件 4/5 の最終 `cross-checked` 格付け。
- NF B v4 の台帳 v1.6 完全準拠という主張。
- EP v4/self-hash checker v2 の再批准。
- 「矢印 (d) 全体が既在補題で閉じた」という erratum。
- K20 への ROOF-KILL、THETA-1000 の無条件形。
- BOTTOM-UP v1 の凍結、SAT、kill、本掘削。
- TB 束による (5′) の citation-pinned 昇格。

