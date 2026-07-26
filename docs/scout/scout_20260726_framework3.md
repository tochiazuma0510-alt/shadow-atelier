# scout_20260726_framework3.md — 直接補題の枠組み出典 3 本(A₅ 戦線)

- 検索係: paper-scout
- 発注: 司令塔(直接補題の枠組み出典 3 本・A₅ 戦線)
- 採否判断はしていない。数学者への直接配達もしていない。

## 冒頭表

| 目標 | 候補 | 入手可否 | 該当 §/頁/定理番号 | 実在確認 |
|---|---|---|---|---|
| 1 | Deligne 1989, "Le groupe fondamental de la droite projective moins trois points" | **PDF入手済み** | §15「Points base à l'infini」、印字頁 151–176(次節§16開始=177の直前まで)。PDF内頁(オフセット)では 73–98 頁目 | 実在確認済み(IAS公式サイト・目次画像照合) |
| 2 | Szamuely, "Galois Groups and Fundamental Groups" (CUP 2009) | **本文PDF入手不可**(目次・正誤表のみ入手) | §4.7「The Outer Galois Action」、印字頁 130–135(次節§4.8開始=136の直前)。Cor. 4.7.3/Example 4.7.4 はこの範囲内のはず(節末尾寄りと推定・未確認) | 目次・書誌は実在確認済み(著者公式ページ)。**Cor./Example の頁内位置はUNVERIFIED**(節全体の頁範囲のみ確定) |
| 3 | Herfort–Ribes 1985, "Torsion elements and centralizers in free products of profinite groups", J. reine angew. Math. 358 | **PDF入手不可**(EUDML 403・GDZ本文未取得) | pp.155–161(複数独立情報源で一致) | 書誌情報は実在確認済み(EUDML書誌レコード・独立検索3回で頁一致)。**本文未取得のため定理番号はUNKNOWN** |
| 3b(補助) | Ribes–Zalesskii, "Profinite Groups" (Springer Ergebnisse) — 同事実の教科書版命題 | 本文未取得 | UNKNOWN(章は「自由副有限積/中心化群」周辺と推定) | **UNVERIFIED** — 命題番号の特定に至らず |

---

## 目標 1: Deligne 1989 — 詳細

- **確認方法**: MSRI/IAS(Institute for Advanced Study — Deligne の公式出版リスト)に掲載された公式PDFスキャンを取得。URL: https://publications.ias.edu/sites/default/files/61_LeGroupeFondamentalDroite.pdf
- **取得物**: `papers/delivered/deligne_1989_groupe_fondamental_P1_moins_3points.pdf`
  - SHA-256: `689b516faf3a05c657920d21a74f68fdc7d0adbd4f7c75d78928e5356c636e44`
  - 全219頁(印字頁79–297と一致)
- **目次画像照合(実施済み)**: 冒頭5頁を画像取得し目次を直接確認。
  - §15「Points base à l'infini」= 印字頁151(小節: Théorie classique 153・Théorie profinie 159・Théorie algébrique 164・Compatibilités 168・Théorie motivique 174)
  - §16「P¹ moins trois points: un quotient du π₁ motivique」= 印字頁177 開始
  - → **§15 は印字頁151–176(PDF内頁オフセットは印字頁−78、すなわちPDF頁73–98)**
- **本丸(§15)の内容位置は確定**。ページ内の具体的な定理番号(tangential basepoint の較正式そのもの)までは今回未読解(トリアージ止まり — 深読みは司令塔/reader の仕事)。

## 目標 2: Szamuely — 詳細

- 出版社(CUP)版の無料ドラフトPDFは**見つからず**。著者(Tamás Szamuely、現ピサ大学)の公式ページ(https://pagine.dm.unipi.it/tamas/publ.html)には**目次PDF(`fgtoc.pdf`)と正誤表PDF(`erratafg.pdf`)のみ**公開。本文フルテキストは非公開(CUP著作権)。
- 取得した目次から確認:
  - Chapter 4「Fundamental Groups of Algebraic Curves」pp.101–147
    - §4.6「The Algebraic Fundamental Group」p.126
    - **§4.7「The Outer Galois Action」p.130**
    - §4.8「Application to the Inverse Galois Problem」p.136
  - → **§4.7 は pp.130–135**。表題「The Outer Galois Action」は正典 2405.11725/2401.06870 が引く Ihara embedding / f_g の構成の文脈と機構的に一致(=正しい節を引いていることの傍証)。Cor. 4.7.3・Example 4.7.4 はこの6頁の範囲内にあるはずだが、**具体的にどの頁かは本文未読のため未確認(UNVERIFIED)**。
  - 正誤表(`erratafg.pdf`)は取得したが§4.7周辺の訂正の有無は未読解(バイナリのまま — 深読みは司令塔判断)。
- **代替候補(参考・未採用)**: 同著者の無料ノート "Heidelberg Lectures on Fundamental Groups"(J. Stix ed., *The Arithmetic of Fundamental Groups (PIA 2010)*, Springer 2012, pp.53–73)は全文無料(http://pagine.dm.unipi.it/tamas/pia.pdf)。ただし**独立した短いノートで章立て・定理番号が本と異なる**ため、Cor.4.7.3/Example 4.7.4 の代替出典にはならない(番号ズレどころか対応する定理自体が同一構成か要検証)。深読み時に「代用できるか」を検討する価値はあるが、今回はトリアージ対象外として報告のみ。
- **取得物**:
  - `papers/delivered/szamuely_2009_toc.pdf`(目次) — SHA-256: `524c46c7c17fd833b4e072df88665f946cbc69bb0efc88a634416b525dc27712`
  - `papers/delivered/szamuely_2009_errata.pdf`(正誤表) — SHA-256: `0b7d80bece7f67b0f7e7420d52b94b8e94c8c0d4b57be80069fb610f69c1553a`

## 目標 3: 中心化群の事実 — 詳細

- **一次出典候補**: W. Herfort, L. Ribes, "Torsion elements and centralizers in free products of profinite groups", *J. reine angew. Math.* **358** (1985), **pp.155–161**。
  - 頁範囲は EUDML 書誌レコード(https://eudml.org/doc/152727)と複数回の独立検索で一致 — **書誌情報としては実在確認済み**。
  - **本文PDFは未取得**: EUDML は本文ページが403(認証要求)、GDZ(ゲッティンゲン大学デジタル化センター、Crelle誌全巻を電子化済み)はトップページのみ取得できボリューム358の直接リンクに到達できず。De Gruyter(現発行元)は購読制。
  - 本文が読めなかったため、**「非自明元の中心化群 = procyclic」という言明が本論文のどの命題番号にあたるかは UNKNOWN**。ただし論文の主題(自由積・捻れ元・中心化群)は司令塔の求める事実と機構的に直結しており、誤同定の可能性は低い。
- **二次出典(教科書)候補**: L. Ribes, P. Zalesskii, *Profinite Groups* (Springer, Ergebnisse der Mathematik, 2000/2010第2版)。この事実(自由副有限群の非自明元 x の中心化群が procyclic、基底元なら C(x)=x^Ẑ)は同書のどこかに命題として収録されているはずだが、**本文への到達手段が今回見つからず(Google Books プレビュー・出版社サイトとも本文非公開)、命題番号は特定できなかった**。
  - 副産物として、この事実を引用する周辺文献(Shumyatsky–Zalesskii, arXiv:1910.04838; Zalesskii–Zapata, arXiv:1711.01500; Casals-Ruiz–Pintonello–Zalesskii, arXiv:2311.13439)を確認したが、いずれも今回読んだ範囲(冒頭数頁)では該当の一次言明・命題番号への直接引用箇所には行き当たらなかった(negative result — 下記参照)。
- **入手不能時の経路候補**: (a) GDZ で PPN243919689 配下のボリューム一覧から358巻を手動ブラウズ(URL構造の推測に留まり今回は解決せず)。(b) ResearchGate 経由の著者アップロード版(Herfort の ResearchGate プロフィールを発見済み: https://www.researchgate.net/profile/Wolfgang-Herfort — 本論文自体のアップロードは今回未確認)。(c) Ribes–Zalesskii 本の該当章について reader が図書館アクセス等で本文を直接確認。

---

## 空振りだった角度・使ったクエリ

- **(a) 直当て**: `Deligne "groupe fondamental de la droite projective moins trois points" MSRI pdf slmath` → 成功(IAS版発見)。`Szamuely "Galois Groups and Fundamental Groups" draft pdf` → 空振り(ドラフト非公開の確認のみ)。
- **(b) 機構名**: `"Cor. 4.7.3" OR "Corollary 4.7.3" Szamuely Ihara embedding f_g tangential` → 空振り(該当ヒットなし、無関係な Kerodon/msp の "4.7.3" ヒットのみ)。`"centralizer" "free profinite group" "is procyclic" nontrivial element theorem` → 部分成功(事実の存在自体は複数の周辺論文で言い回しとして確認できたが、一次命題番号には未到達)。
- **(c) 著者系譜**: `Herfort Ribes "Torsion elements and centralizers in free products of profinite groups" pdf` → 書誌確認のみ(本文PDFなし)。`mat.unb.br/~pz/publication.html`(Zalesskii 個人ページ)確認 → 該当論文へのリンクなし(空振り)。
- **(d) 逆引き**: `1910.04838`(Shumyatsky–Zalesskii)・`1711.01500`(Zalesskii–Zapata)・`2311.13439`(Casals-Ruiz–Pintonello–Zalesskii)を辿ったが、冒頭数頁の読解では目標3の一次言明への直接引用箇所を発見できず(空振り — ただし全文は読んでおらず、深読み時に再訪の価値あり)。
- **GDZ(ゲッティンゲン)ボリューム直接アクセス**: `gdz.sub.uni-goettingen.de/id/PPN243919689_0358` 等のURL推測 → 到達せず(トップページのみ)。

## 総括

- 目標1(Deligne)は**完全達成**: 実PDF入手・§15の頁範囲確定。
- 目標2(Szamuely)は**部分達成**: 本自体は入手不可(商業書籍)だが、正しい節(§4.7 pp.130–135)であることを目次で確認・目次と正誤表は取得。
- 目標3(中心化群)は**書誌確認止まり**: Herfort–Ribes 1985 pp.155–161 の実在は複数独立に確認したが、本文入手・命題番号特定は今回不能(UNKNOWN として報告)。Ribes–Zalesskii 教科書側の命題番号も特定できず。

---

## 目標 3 再挑戦(2026-07-26・司令塔再発注)

### 冒頭表(再挑戦分)

| 経路 | 結果 | 詳細 |
|---|---|---|
| ① GDZ 巻レベルブラウズ | **不達**(前任と同じ壁) | `gdz.sub.uni-goettingen.de/id/PPN243919689_0358` へ到達したが、返るのはヘッダー/フッターのみの JS 殻(目次・PDF リンクとも取得不可)。URL 構造自体は存在確認(PPN243919689 = 誌の親 ID)したが本文への経路は開けず。 |
| ② De Gruyter DOI 10.1515/crll.1985.358.155 | **未再訪**(前任確認済みの壁を追認するに留め、今回は時間を③④に配分) | — |
| ③ 代替(番号特定・独立引用) | **部分成功** — ただし**本丸(centralizer procyclic の直接言明)には未到達**。関連する構造定理の番号を 2 系統で確認 | 下記詳細 |
| ④ 教科書・ノート | Ribes–Zalesskii "Profinite Groups" (Springer, 2000/2010) の該当章 = **第9章(自由積)・§9.1** に絞り込めた(番号 9.1.12 等を2独立引用で確認) | 下記詳細 |

**本文 PDF は今回も入手不可**(GDZ・De Gruyter とも壁)。**Herfort–Ribes 1985 (Crelle 358) そのものの定理番号は依然 UNKNOWN**。以下は経路③④で見つかった「近傍成果」の報告(候補・懸念つき)。

### 経路③④で見つかった具体的な引用(実在確認済み・PDF取得済み)

**(A) Ribes–Zalesskii "Profinite Groups" Theorem 9.1.12 ― 2独立ソースで番号確認**

1本目: J.W. MacQuarrie 系列の先行論文 **W. Herfort, P.A. Zalesskii, "Virtually Free pro-p groups whose Torsion Elements have finite Centralizer"**(arXiv:0712.4244, published version: J. reine angew. Math. 相当の作業に近い pro-p 論文)の **Theorem 2.9**:
> "Let G = ∐ⁿᵢ₌₁ Gᵢ be a free profinite (pro-p) product. Then Gᵢ ∩ Gᵢᵍ = 1 for either i≠j or g∉Gⱼ. Every finite subgroup of G is conjugate to a subgroup of a free factor."
> — 引用元: **[[6], Theorems 9.1.12 and 9.5.1]**。文献[6] = **L. Ribes, P.A. Zalesskii, *Profinite groups*, (Springer, Berlin, 2000)** と巻末で確認(実在確認済み)。

2本目(独立): **P. Zalesskii, T. Zapata, "Profinite extensions of centralizers and the profinite completion of limit groups"**(arXiv:1711.01500)p.13:
> "...for otherwise Γ is a free product, and hence G is a free profinite product and thus a centreless group (cf. **[RZ00b, Thm. 9.1.12]** or [ZM88, Thm. 2.13])."
> — [RZ00b] = 巻末で **L. Ribes and P. Zalesskii, *Profinite groups*, Springer-Verlag, Berlin, 2000** と確認。

→ **2独立ソースが同じ番号(Thm. 9.1.12)を同じ書(RZ00b)に帰属させている**(番号特定は成立)。ただし言明内容は「自由副有限積の有限部分群は自由因子の共役」「自由副有限積は中心が自明」であって、**「非自明元の中心化群が手続き巡回」そのものではない**(隣接する性質・同じ第9章の可能性が高いが、9.1.12 自体がそれとイコールではない)。

**(B) 同論文(1711.01500)本文中の直接言及(番号なし・地の文)**

Introduction §3 (p.5):
> "In the discrete case, the centralizer of each non-trivial element in a free group is infinite-cyclic and... In the profinite case, **the centralizer of each non-trivial element that generates Ẑ in a free profinite group is meta-procyclic**, and, after performing an extension of centralizer, the centralizer becomes either meta-abelian, or (non-trivial procyclic)-by-(infinite dihedral pro-π), or contains a non-abelian free pro-p subgroup. See Lemma 4.2 and Theorem 4.3, and Proposition 4.7."

→ **懸念(重要)**: この文は「procyclic」ではなく **"meta-procyclic"**(procyclic を法とする拡大、つまり procyclic-by-procyclic 型)と書いている。しかも対象は「Ẑ を生成する非自明元」に限定した言い方に読める。当工房が求める言明(「非自明元の中心化群 = procyclic」)と**完全には一致しない可能性がある**(meta-procyclic ⊋ procyclic)。この論文はこの事実の**一次出典を明示引用していない**(地の文で述べるのみ・直前の文献リストにも Herfort–Ribes 1985 は現れず)。**深読み時に要検証**: (i) 「procyclic」と「meta-procyclic」の食い違いが記法の緩さか、実際に異なる主張かの切り分け、(ii) 対象元の限定(「Ẑ を生成する」)が実質的にすべての非自明元を指すのか特殊な部分集合かの確認。

**(C) 近接するが別論文と判明したもの(誤同定回避のため報告)**

- **W. Herfort, L. Ribes, "Solvable subgroups of free products of profinite groups"**, Group theory (Singapore, 1987), 391–403, de Gruyter, Berlin, **1989**(1985年 Crelle 論文とは**別の論文**・同著者ペア)。R. Guralnick, D. Haran, "Frobenius subgroups of free profinite products"(arXiv:1001.3599)がこの **Theorem 3.2** を引用:
  > "Herfort and Ribes show in [8, Theorem 3.2] that a closed solvable subgroup of the free product of a family of profinite groups {Aₓ} must be one of the following: (1) a conjugate of a subgroup of one of the free factors; (2) isomorphic to Ẑ_σ ⋊ Ẑ_σ'...; (3) free pro-C product of two copies of the group of order 2...; (4) a profinite Frobenius group of the form Ẑ_σ ⋊ C..."
  - 実在確認: 巻末文献[8]で書誌一致(Group theory (Singapore, 1987))。**これは目標のCrelle 1985論文ではない**(同著者・隣接主題の**別論文**)ため、目標3の直接的な代替出典としては不採用。ただし機構的には極めて近い(可解部分群の分類が中心化群procyclicの一般化になっている可能性)ため、深読み時の参考として記録。
- **W. Herfort, L. Ribes, "Frobenius subgroups of free products of prosolvable groups"**, Monatsh. Math. 108 (1989), 165–182。同じく1985年論文とは別物(参考記録のみ)。

### 取得物(今回追加分・papers/delivered/)

- `herfort_zalesskii_0712.4244_virtually_free_prop_finite_centralizer.pdf`
  - SHA-256: `187cf9313bf9a397b2ff7250951d28d84685492e933531cef76c907d666d821d`
  - Theorem 2.9(RZ00b Thm 9.1.12/9.5.1 引用元)を含む。
- `guralnick_haran_1001.3599_frobenius_subgroups_free_profinite_products.pdf`
  - SHA-256: `5c75c7ea7f88a8afa873c7ecb7403ec1349b652c745cb43297960e12539e8ccf`
  - Herfort–Ribes 1989(別論文)Theorem 3.2 の引用を含む。
- `zalesskii_zapata_1711.01500_profinite_extensions_centralizers.pdf`
  - SHA-256: `6f42e953267170b7c48629d2d8bee4427add24f437faf49b6629b9dc424cb21b`
  - "meta-procyclic" 地の文言明・RZ00b Thm 9.1.12 引用を含む。

### 結論(目標3再挑戦)

- **本文未達は変わらず**(GDZ・De Gruyter とも壁 ― 経路①②は前任と同じ結果)。
- **前進**: Ribes–Zalesskii 教科書の該当箇所を「第9章・§9.1 周辺(Thm 9.1.12 が2独立引用で確定)」まで絞り込めた。これは「番号特定(二次)」の**部分達成**であり、**完全達成ではない**(9.1.12 自体の言明は「自由積の有限部分群共役性・中心が自明」であって「中心化群 procyclic」ではないため)。
- **新規の懸念**: 独立に見つかった地の文言明が "procyclic" ではなく "meta-procyclic" と書いており、当工房の求める言明と字面が食い違う。これが同じ事実の言い換えか、実際に異なる主張かは**司令塔・数学者による深読みが必要**(UNKNOWN として明示)。
- **次の一手の候補**(未実施・提案のみ): (a) Ribes–Zalesskii 本の第9章目次(節タイトル一覧)だけでも取得できれば、9.1.12 近傍の節タイトルから「centralizer」の節番号が絞れる可能性。(b) Herfort–Ribes 1989 論文("Solvable subgroups...")の本文が入手できれば、Theorem 3.2 から中心化群 procyclic 性が系として導けるかを機構的に確認できる(この論文も本文未取得)。

### 空振り・追加クエリ(再挑戦分)

- `gdz.sub.uni-goettingen.de "Journal für die reine und angewandte Mathematik" Band 358 PPN` → 親PPN(243919689)は特定できたが巻レベル到達せず(空振り)。
- `Herfort Ribes 1985 crelle 358 pdf sci-hub OR semanticscholar OR zbmath` → De Gruyter 公式ページ(壁)以外ヒットなし。
- `zbmath.org` の当該レビューページへの直接アクセス → HTTP 403(空振り)。
- `"Theorem 9.1.19" OR "Proposition 9.1.19" Ribes Zalesskii centralizer procyclic free profinite group` → 該当なし(空振り、ただし検索エンジンの要約が「centralizer of each non-trivial element that generates Ẑ in a free profinite group is meta-procyclic」という言い回し自体を提示 — 上記(B)と符合)。
- arXiv 1910.04838(Shumyatsky–Zalesskii, centralizers virtually procyclic)を全文確認 → Herfort–Ribes 1985 への直接引用なし(その論文が引く「procyclic centralizer of infinite-order element」は双曲群論(Alonso et al., 参考文献[1])からの一般論であり、自由副有限群固有の話ではなかった ― 誤誘導注意)。
- arXiv 1305.4887(Weigel–Zalesskii, Virtually free pro-p products)を全文確認 → Herfort–Ribes 1985 への引用なし(空振り)。
- arXiv 1807.02429(Shumyatsky–Zalesskii–Zapata, centralizers abelian)→ WebFetch 要約では検出できず(バイナリ深読み未実施・時間の都合で見送り、深読み時に再訪の価値あり)。

---

## 目標 3 差し替え(因子交叉定理・2026-07-26 Opus 裁定による訂正発注)

### 訂正の経緯

司令塔より: 目標3(旧)は Herfort–Ribes 1985 の**中心化群定理**(捻れ元の中心化群が procyclic 等)を狙っていたが、Opus の裁定でこれは**狙い違い**と判明。真に欲しいのは、自由副有限積 ∐ Gᵢ における「**相異なる自由因子の共役は自明にしか交わらない**」(malnormality 型)の定理番号。

### 結論(先出し): 前回調査で既に取得済みの資料の中に、本丸がそのまま含まれていた

前任(私自身の前回セッション)が目標3(旧・中心化群)の調査中に取得した **arXiv:0712.4244**(Herfort–Zalesskii, "Virtually Free pro-p groups whose Torsion Elements have finite Centralizer")の **Theorem 2.9** が、訂正後の目標(因子交叉定理)の**逐語的な言明そのもの**だった。前回は「中心が自明・有限部分群の共役」という別の帰結に気を取られ、この定理の中心部分(交叉が自明という命題)が今回の本丸と一致することを見落としていた。**これは前任の誤トリアージであり、今回改めて機構ベースで照合し直して確認した。**

### 冒頭表(差し替え分)

| 候補 | 出典 | 実在確認 | 定理番号 | 版 |
|---|---|---|---|---|
| **本丸** | Ribes–Zalesskii, *Profinite Groups* (Springer Ergebnisse 40) | 直接入手不可・**孫引き 2 独立ソースで番号確認済み** | **Theorem 9.1.12**(合わせて 9.5.1 も関連) | **2000年第1版**(RZ00 / RZ00b と引用される版) |
| 引用元1 | Herfort–Zalesskii, arXiv:0712.4244, Theorem 2.9 | **PDF入手済み・全文確認**(papers/delivered/ に既存) | 「[6], Theorems 9.1.12 and 9.5.1」として引用 | — |
| 引用元2 | Zalesskii–Zapata, arXiv:1711.01500, p.13 | **PDF入手済み・全文確認**(papers/delivered/ に既存) | 「[RZ00b, Thm. 9.1.12]」として引用 | — |

### 逐語(0712.4244, Theorem 2.9 — 実物 PDF から直接確認)

> **Theorem 2.9** [([6], Theorems 9.1.12 and 9.5.1)] Let G = ∐ⁿᵢ₌₁ Gᵢ be a free profinite (pro-p) product. Then Gᵢ ∩ Gⱼᵍ = 1 for either i ≠ j or g ∉ Gⱼ.
> Every finite subgroup of G is conjugate to a subgroup of a free factor.

([6] = L. Ribes, P.A. Zalesskii, *Profinite Groups*, Springer, Berlin, 2000 — 巻末文献表で確認済み)

**機構照合(命題の同値変形)**: 目標の言明は「1 ≠ u ∈ Gᵢ かつ g u g⁻¹ ∈ Gⱼ ならば i=j かつ g ∈ Gᵢ」。これは Theorem 2.9 の対偶にほかならない ― u ∈ Gᵢ ∩ (Gⱼ)^{g⁻¹} が非自明なら、Theorem 2.9 より「i≠j または g⁻¹∉Gⱼ」は偽、すなわち i=j かつ g⁻¹∈Gⱼ=Gᵢ、ゆえに g∈Gᵢ。**式変形だけで完全に一致する(同じ命題の書き方違い)** — 別命題への横滑りではない。

前段の Theorem 2.9 は本文中で 2 回、実際の証明(Lemma 3.2 の Claim・Proposition 4.1 の冒頭)に使われており、著者自身がこの命題を「自由因子の共役の交叉が自明」という意味で運用していることも確認済み(0712.4244 本文 p.6, p.6-7)。

### 第二独立ソース(1711.01500, p.13 — 前回取得分の再確認)

> "...for otherwise Γ is a free product, and hence G is a free profinite product and thus a centreless group (cf. **[RZ00b, Thm. 9.1.12]** or [ZM88, Thm. 2.13])."

こちらは「中心が自明」という**帰結**の引用だが、同じ番号(9.1.12)・同じ書(RZ00b = Ribes–Zalesskii 2000)を指しており、番号の独立確認としては十分(中心が自明という帰結は、自由因子の自明交叉から容易に従う — g が中心元なら任意の Gᵢ と可換 = Gᵢ の共役 Gᵢᵍ=Gᵢ に u∈Gᵢ が交わる形になり、Theorem 2.9 型の議論で g∈Gᵢ 各因子に対して成立 → g は全因子の共通部分 → 通常 g=1)。

### 懸念・未解決点

1. **本文 PDF は今回も未入手**(RZ の本自体・GDZ・De Gruyter とも壁は前回と同じ)。9.1.12 の逐語は **孫引き(0712.4244 の Theorem 2.9 の記述)経由の再構成であり、RZ00 の原文そのものではない**。0712.4244 の著者(Zalesskii は RZ00 の共著者本人)による引用なので誤引用の可能性は低いが、**一次確認(RZ00 原文)は依然 UNVERIFIED**。
2. **版の特定**: 引用は 2 件とも **2000年 Springer 初版**(RZ00 / RZ00b)を指している。**2010年第2版で章立て・定理番号が変わっている可能性は未確認**(2版は「3つの新しい付録」を追加という情報は取得したが、既存章の番号繰り下げ・繰り上げの有無は未確認 — 付録追加なら本体の番号は保存される可能性が高いが、断定はできない)。深読み時に 2010 版の該当箇所を直接確認する必要あり。
3. 9.5.1 側の言明(「有限部分群は自由因子の共役」)は今回の本丸(交叉定理)そのものではなく隣接命題 — 誤って 9.5.1 を主命題として引用しないよう注意。**主命題は 9.1.12**。
4. 章内での 9.1.12 の直前直後(節タイトルが「malnormal」等かどうか)は未確認 — 前回調査で得た情報では第9章§9.1 は Kurosh 部分群定理まわり(0712.4244 内でも「Theorem 9.1.9 in [6]」= pro-p 版 Kurosh 部分群定理として引用されている・本文 p.3, p.5)。9.1.12 はその節内の系列にあると推定(未確認)。

### 使ったクエリ・角度

- **(d) 逆引き優先**(前回取得済み PDF の再点検): `papers/delivered/herfort_zalesskii_0712.4244...` を Read ツールで全文取得 → Theorem 2.9 の逐語発見(直当てでなく手持ち資料の読み直しで解決 — 前回のトリアージ誤りに気づいた)。
- **(b) 機構名直当て**: `Ribes Zalesskii "Profinite Groups" "9.1.12" free product intersect trivially conjugate`(WebSearch)→ 空振り(該当ヒットなし、一般的な文脈情報のみ)。
- **版差の確認**: `"Ribes" "Zalesskii" "Profinite Groups" second edition 2010 chapter 9 free products theorem numbering changed`(WebSearch)→ 部分成功(2版に新付録3本追加という情報は得たが、章9番号の異同は未確認)。
- **第三独立ソース探索**: arXiv:1305.4887(Weigel–Zalesskii, Virtually free pro-p products)の PDF 冒頭3頁を確認 → 9.1.12 への直接引用は発見できず(空振り、圧縮 PDF のテキスト抽出限界の可能性もあり深読み時に再訪の価値あり)。arXiv:1001.3599(Guralnick–Haran)冒頭3頁も確認 → 該当引用なし(文献[12]=RZ本と推定されるが番号までは言及なし・空振り)。

### 総括(目標3差し替え)

- **番号特定(二次)は達成**: Theorem 9.1.12(Ribes–Zalesskii, *Profinite Groups*, Springer 2000年版)が、2 独立ソース(0712.4244・1711.01500)により確認された。
- **命題内容の機構一致は代数的に確認済み**(対偶変形で完全一致 — 別命題への誤爆ではない)。
- **一次原文(RZ00 直接確認)・2010年版での番号保存の有無は UNVERIFIED として持ち越し**。
- 追加取得物なし(既存の papers/delivered/ 内 0712.4244・1711.01500 を再利用・再確認したのみ)。
