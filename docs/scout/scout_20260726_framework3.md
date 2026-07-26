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
