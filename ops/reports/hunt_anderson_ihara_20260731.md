# hunt_20260731_anderson_ihara — (U2) 律速文献の本文取得遠征

遠征係 / 2026-07-31。採否判断はしない。配達もしない(ops/inbox_hunter/ 止め)。

## 0. 結論(先出し)

- **Anderson–Ihara 1988(Annals 128, 271–293)の本文 PDF は取得できず。** 合法経路はすべて有料壁または bot 遮断。`ops/inbox_hunter/anderson_ihara_1988.pdf` は**作成していない**(捏造・不完全ファイルを置かない方針)。
- 代わりに **著者本人による同内容のサーベイ**と**専門家による解説論文**を実体取得した(下表)。**(U2) の分岐命題そのものは、この 2 本で文言レベルまで押さえられる**(§3 参照)。
- **Vogel 2005 は本文テキスト取得成功**(著者版 PDF・31 頁・pdftotext 全文抽出可)。

## 1. 取得できたファイル(ops/inbox_hunter/ — 未配達)

| ファイル | 実体 | 頁 | bytes | SHA-256 |
|---|---|---|---|---|
| `vogel_2ext_2005.pdf` | Vogel, *On the Galois group of 2-extensions with restricted ramification*(著者版 preprint, 日付 2004-03-17) | 31 | 343286 | `86b9b610bd683a9b6e4a4dd057a3bf1c7b39e76d0ceea861c4aac4eedb0a20a6` |
| `ihara_ICM1990_braids_galois.pdf` | Ihara, *Braids, Galois Groups, and Some Arithmetic Functions*, ICM Kyoto 1990, Vol. I, 99–120(ICM 公式 OCR 版から該当 22 頁を抽出) | 22 | 2111565 | `914fc32e394fe1d2ffc69f22b83b91ec072dfeb026f58deb63be83aa647a4284` |
| `coleman_1989_ASPM17_anderson_ihara_theory.pdf` | R. F. Coleman, *Anderson–Ihara Theory: Gauss Sums and Circular Units*, Adv. Stud. Pure Math. 17 (1989), 55–72 | 18 | 1208944 | `df8a5941a2f074a71654db5f415532944be60fe21cd49b2fc81be0c88b8eca7f` |

出所 URL:
- Vogel: https://www.mathi.uni-heidelberg.de/~vogel/2ext.pdf (Heidelberg 著者ページ・公開)
- Ihara ICM: https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1990.1/ICM1990.1.ocr.pdf (IMU 公式・全巻 85 MB、pdf 頁 187–208 = 印刷頁 99–120 を抽出)
- Coleman: https://doi.org/10.2969/aspm/01710055 (Project Euclid・ASPM 旧巻は open。素の curl は Cloudflare で HTML を返す。**ブラウザ UA + Referer を付けると PDF が取れる**)

## 2. Anderson–Ihara 1988 の同定と、塞がっていた経路

**同定(実在確認済み)**
- DOI **10.2307/1971443**(Crossref 実取得: Ann. Math. (2) **128**, No. 2, **271–293** (1988))
- JSTOR stable: https://www.jstor.org/stable/1971443
- zbMATH **Zbl 0692.14018**(https://zbmath.org/4132333、評者 W. Kleinert)/ MathSciNet MR 960948(未実取得 = 引用のみ、**UNVERIFIED**)
- 続編 Part 2: Internat. J. Math. **1** (1990), 119–148、DOI **10.1142/s0129167x90000095**(Crossref 実取得)

**塞がっていた経路(すべて実地に叩いた)**

| 経路 | 結果 |
|---|---|
| annals.math.princeton.edu 該当号 | 号の目次は取得(記事 5 番目・271–293 を確認)。**記事 PDF のホスティング無し**。同サイトは「1884–2019 は JSTOR、2017–2025 は Project Euclid」と明記 |
| annals の直 PDF URL パターン (`wp-content/uploads/annals-v128-n2-p0*.pdf`) | 全て **404** |
| JSTOR | WebFetch **HTTP 403**(bot 遮断)。JSTOR の無料閲覧枠はログイン必須・オンライン閲覧のみで DL 不可 |
| Project Euclid | Annals は 2017 年以降のみ。1988 年分は**非収録** |
| OpenAlex / Semantic Scholar の OA 探索 | 双方 `oa_status: closed` / `openAccessPdf: CLOSED`、リポジトリ全文 **無し** |
| fatcat / scholar.archive.org | API は非 JSON 応答、Web は "Session Verification" 壁。IA advancedsearch は該当 0 件 |
| Internet Archive(本体) | Annals vol.128 の item 無し |
| HathiTrust(全文検索で節見出しだけでも拾う試み) | **HTTP 403**(bot 遮断)。そもそも 1988 年は in-copyright で search-only |
| 著者サイト | Ihara の RIMS 名誉教授ページ(kurims.kyoto-u.ac.jp/~kenkyubu/emeritus/ihara/papers.html)に**項目 31 として掲載されているが PDF リンク無し**(PDF が付くのは項目 50 以降 = 2000 年代の Euler–Kronecker 系のみ)。G. Anderson(Minnesota・2018 年に退官/物故)側の配布ページも見つからず |
| GDZ / DigiZeitschriften | Annals 自体が非収録。ついでに探した Inventiones 86 (1986, Ihara の姉妹論文) も GDZ は SPA シェルのみ返し、METS/PDF エンドポイントは 404、DigiZeitschriften は全リクエストがトップへ 302(要ログイン) |
| pre-arXiv | 1988 年・arXiv 開設(1991)以前。preprint の電子版は原理的に存在しない |

**方針上の除外**: DuckDuckGo 結果には Sci-Hub の該当ページが 2 件出たが、海賊サイトのため使用しなかった(報告のみ)。

## 3. (U2) 関連の当たり付け(目次レベル・深読みはしない)

### 3-a. AI1988 本体の構造(zbMATH レビュー本文からの間接情報)

zbMATH Zbl 0692.14018 のレビュー本文(実取得)より、主定理の内容は:

> S₀ ⊂ P¹(C) を 0,1,∞ を含む有限集合、ℓ を素数とする。圏 X(S₀) = 「Galois 閉包の次数が ℓ 冪で S₀ の外で不分岐な有限分岐被覆 f: Y → P¹」を考える。X(S₀) の全対象・全射に共通の**最小の定義体 Ω = Ω(S₀)** が存在する。**主定理は、この Ω が、Q(μ_{ℓ^∞}) 上の明示的に構成可能な無限・非アーベル pro-ℓ 拡大であって ℓ の外で不分岐、かつ円分 ℓ-単数群を含むものと一致すること。**
> 証明の要は「X(S₀) 内に f: P¹ → P¹ 型の *elementary object* が十分多く存在する」ことを示し、その cusp における **Puiseux 展開**を調べる点。系として Fermat 曲線(level ℓⁿ)・Heisenberg 曲線(level ℓⁿ)・モジュラー曲線(level 2ⁿ)の Jacobian の ℓ 冪等分点の有理性が従う。

→ **(U2) が「有限商の分岐」を要求するなら、その源はこの主定理**(有限 ℓ 群を Galois 群にもつ P¹ の分岐被覆の族 = 有限商の塔、その定義体の分岐が ℓ に局在する)。**節番号・定理番号は本文未入手のため UNVERIFIED**。

### 3-b. Ihara ICM1990(取得済み)での対応箇所 — **ここが最短の代替読み口**

抽出 PDF の該当箇所(印刷頁で言うと §5・§6.5):

- **§5(印刷 p.111 付近)**: 「合併体 Ω^(ℓ)(∞) は Xₙ (n ≥ 4) に対する φ^X の核に対応する。**これは Q(μ_{ℓ^∞}) 上の pro-ℓ(非アーベル)拡大であって ℓ の外で不分岐である。**各 m ≥ 1 に対し Gal(Ω^(ℓ)(m+1)/Ω^(ℓ)(m)) は有限階数の自由 Z_ℓ 加群で、Gal(Ω^(ℓ)(m+1)/Ω^(ℓ)(1)) により中心化され、Gal(Ω^(ℓ)(1)/Q) 加群として Tate 捻り m をもつ」 ← **(U2) の分岐言明はここに一文で出ている**
- **§6.5「ψ_σ(ξ,η) and Higher Circular ℓ-Units (Anderson–Ihara [AI₁,₂])」(印刷 p.118)**:
  - *ℓ-elementary* 集合の定義(S₀={0,1,∞} から S ↦ S^{1/ℓ}(全 ℓ 乗根)と S ↦ T_{a,b,c}(S)(a,b,c を 0,1,∞ に送る射影変換)の有限回操作で得られる S)
  - **Definition 6.5.1**: E^(ℓ) = S∖{0,∞} の元(S は全 ℓ-elementary 集合を走る)で生成される C^× の部分群 = **higher circular ℓ-units**
  - **Theorem [A-I₂]**: ψ_σ(ξ,η) の各係数 (mod ℓⁿ) は σ の E^(ℓ) 上の作用で明示的に書ける
  - **Corollary [A-I₁]**(= AI1988 の帰結): **Ω^(ℓ)(∞) = Q(E^(ℓ))**
  - **Question 6.5.2 (i)**: Ω^(ℓ)(∞) は Q(μ_{ℓ^∞}) 上 ℓ の外不分岐な**最大**の pro-ℓ 拡大か?(= 未解決問題として明示)

→ 照合観点: (U2) が要るのが「不分岐性そのもの」なら ICM §5 の一文 + AI1988 主定理で足り、「最大性」まで要るなら **Question 6.5.2(i) は 1990 年時点で未解決**である点が効く。ここは司令塔の翻訳判断待ち。

### 3-c. Coleman 1989(取得済み)の守備範囲

Ihara の beta 級数 → Anderson の hyperadelic gamma → Gauss 和・円分単数、という軸の解説。§I「Ihara's "Beta" series」から始まり Theorem A (Ihara: T は principal A-加群) 等。**分岐命題(U2)そのものより「higher circular ℓ-units が何であるか」の実体側**を厚く扱う。AI1988 の Ω の分岐議論そのものは薄い見込み(目次レベル判断・深読みせず)。

## 4. 代替候補(本文が取れる後続/解説文献)

| # | 文献 | 実在確認 | 取得性 | (U2) への効き |
|---|---|---|---|---|
| A1 | Ihara, *Braids, Galois Groups, and Some Arithmetic Functions*, ICM 1990 Kyoto Vol. I, 99–120 | ICM 公式 PDF 実取得(本文確認済み) | **取得済み** | **最有力**。著者本人による AI1988 の帰結の要約 + 不分岐言明 + 未解決 Question 6.5.2 |
| A2 | Coleman, *Anderson–Ihara Theory: Gauss Sums and Circular Units*, ASPM 17 (1989) 55–72, DOI 10.2969/aspm/01710055 | Project Euclid 実取得(本文確認済み) | **取得済み** | ℓ-単数側の実体解説。分岐命題は薄い |
| A3 | Sharifi, *Relationships between conjectures on the structure of pro-p Galois groups unramified outside p*, arXiv:math/0104116 | arXiv 実取得・本文冒頭確認 | 自由 | 冒頭一文が (U2) の型の再掲: 「φ: G_Q → Out(π₁^{pro-p}(P¹∖{0,1,∞})) の固定体 Ω は Q(μ_p) の pro-p 拡大で p の外不分岐 [Ihara]」。**さらに Gal(Ω/Q(μ_p)) の構造・最大性との差を扱う**ので、(U2) が最大性寄りなら本命 |
| A4 | Nagaraj, *Higher Circular ℓ-units of Anderson and Ihara*, in *Current Trends in Number Theory*, Hindustan Book Agency 2002, **pp. 125–128**, DOI 10.1007/978-93-86279-09-5_11 | Crossref 実取得(著者・頁・巻を確認) | **× 有料・Springer ログイン壁**(303 → IdP)。4 頁の短い解説 | AI1988 の専用解説だが分量が小さく、かつ本文未取得 |
| A5 | Anderson–Ihara **Part 2**, Internat. J. Math. 1 (1990) 119–148, DOI 10.1142/s0129167x90000095 | Crossref 実取得 | **× World Scientific 有料** | 本編の続き。ICM §6.5 の Theorem [A-I₂] の出典 |
| A6 | Kodani–Morishita–Terashima, *Arithmetic topology in Ihara theory*, arXiv:1608.07926 | arXiv 実取得(参考文献に [AI] 確認) | 自由 | Ihara 理論の Milnor 不変量/Johnson 準同型的な再構成。分岐命題は主題外だが「有限商の塔」の機構語彙は近い |

## 5. Vogel 2005(再挑戦・成功)

- 出版版: **J. reine angew. Math. 581 (2005), 117–150, DOI 10.1515/crll.2005.2005.581.117**(Crossref 実取得)。De Gruyter 本体は有料。
- 取得したのは **Heidelberg の著者版 PDF**(2ext.pdf、日付 17.03.04、31 頁)。scout がバイナリ止まりだったのは poppler を通していなかったためと思われ、**pdftotext で全文(約 60 k 文字)が問題なく抽出できる**。
- 節構成(pdftotext -layout で確認):
  1. Introduction / 2. Algebraic prerequisites / 3. The maximal 2-extension of Q with restricted ramification / 4. The 2-class field tower of a quadratic number field
- 内容: Frohlich–Koch の最小表示 1 → R → F → G_S(2) → 1 を出発点に、**Zassenhaus filtration の第 4 段 mod での関係式構造**を Massey 積/Milnor 三重不変量(Rédei 記号・Legendre 記号 e_{i,j,m})で決定。末尾に「G mod F_(m+1) の関係式構造は Massey 積で計算できる」という一般定理。
- **注意**: これは著者版であり出版版との頁対応・番号対応は未照合(**UNVERIFIED**)。引用時は preprint 版であることを明記されたい。

## 6. 使ったクエリと空振り(負の結果)

- WebSearch: `Anderson Ihara "Pro-l branched coverings of P^1 and higher circular l-units" Annals of Mathematics 1988` / `"higher circular l-units" Anderson Ihara Annals 128 1988 pdf 1971444 jstor` / `"Pro-l branched coverings" Anderson Ihara pdf download annals 1988 full text` / `"Anderson" "Ihara" 1988 "271" annals "branched coverings" filetype:pdf mirror course notes scan` → **全て引用文献のヒットのみ。本文 PDF ゼロ**
- DuckDuckGo HTML: `"Pro-l branched coverings" Ihara pdf` → Semantic Scholar(全文なし)・Sci-Hub 2 件(不使用)・無関係ポスター 1 件
- Google 直叩き(WebFetch) → エラーページ(bot 遮断)
- API: Crossref(○ DOI 特定)、OpenAlex(closed)、Semantic Scholar(CLOSED)、zbMATH(○ レビュー本文取得)、fatcat(非 JSON)、IA advancedsearch(0 件)
- URL 直撃: annals 4 パターン(全 404)、GDZ 3 パターン(SPA/404)、DigiZeitschriften 2 パターン(302 トップ送り)、HathiTrust 2 パターン(403)

## 7. 司令塔への引き渡しメモ

- `anderson_ihara_1988.pdf` は**存在しない**。ファイル名の空約束を避けるため置いていない。
- 本文が本当に必要なら残る現実的手段は **(a) 大学図書館の ILL / 論文複写依頼、(b) JSTOR 個人無料アカウント(オンライン閲覧のみ)、(c) 著者所属機関(Minnesota / RIMS)への直接照会** の 3 つ。いずれも自動取得の範囲外。
- 判定・採否は書かない。翻訳(B₃-gentle 設定への持ち込み)は司令塔の専権。
