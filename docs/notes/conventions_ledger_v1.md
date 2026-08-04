# 規約台帳 v1.6(conventions ledger)— 工房の大域規約と cert 宣言欄

- **状態札: candidate**(司令塔検分待ち・**Sol 便 94 §5 で方向承認 + CV-9 の規範文条件を受領**・**便 99 F99-7.1 / 便 100 F100-7.1 で v1.4 の意味内容が adopted と追認**)。★ **便 101 W101-3.2**: v1.5 の**配置・規範内容は PASS**、しかし **artifact は最終批准差戻し**(【CL-9】の「checker 未実装」が現物と矛盾)。**本 v1.6 が P101-3 (5) の履行**である
- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01 / 司令塔委嘱(研究者発案の制度化)
- **改訂 v1.1**: 2026-08-01・便 94 修文波(裁定 319)。**F94-5.2(CV-9 の規範文)+ P94-5.1(型強化 9 項)を正位置へ編入**。編入前の本ファイルの SHA-256 = `9cde70bdfc4494e6a9180a370bed81a65af3a388c22e8d0f4bf3c5268bed9087`(git 履歴に旧状態あり)。
- **改訂 v1.2**: 便 95 F95-3.3。CV-12 施行三点(§1.4)+ "n/a" の型(object/array 欄への bare string 禁止・§2「"n/a" の型」節)を追加。
- **改訂 v1.3**: 裁定 354・便 97 P97-1.2(1)〜(6) で確定。**live JSON schema block(§2)を四原則へ全面同期**: ① `path` は参照対象 artifact 自身 ② ハッシュキー名は `sha256` に統一(`digest` は CV-10 範囲で不使用)③ `effective_source` は object `{path,sha256}` ④ `superseded_by:{path,sha256}` の入れ子欄で旧→新を機械可読に表現(`supersedes` 役は廃止)。**title・revision block・`ledger_version` も本改訂で同期**(便 97 W97-1.2 が指摘した「四原則を宣言した直後の live schema が v1.1 のまま」という自己矛盾の修理)。v1.1 形は §2 に「歴史形・新規禁止」として残す(遡及なし・【CL-2】)。
- **改訂 v1.4**: 2026-08-02・裁定 412(便 99 検収)。便 99 **F99-7.1 / P99-7.1 / P99-7.2** を正位置へ編入 — **§1.5(CV-10 細則: 正典 pin の「証明本文の有無」欄。`proof_body_status` 三値 + `omission_kind` + 外部引用 pin)**と **§1.6(CV-11 細則: 封印状態の正本・二鍵 AND・双方向 digest 束縛)**を新設。**便 100 F100-7.1 で「proof_body_status 三値・omission_kind・外部引用 pin・封印二鍵 AND・双方向 digest 束縛という意味内容の adopted 記録」は追認された。**
- **改訂 v1.5**: 2026-08-02・**裁定 422(便 100 検収)**。★ **W100-7.2 の version drift を一回で解消**した改訂である。便 100 は「裁定上 v1.4 内容が adopted」は正しいが「**artifact が v1.4 として同期済み**」は偽(H1 = v1.3・改訂履歴の最終行 = v1.3・live schema の `ledger_version` = `conventions_ledger_v1_3`)と指摘した。本改訂で **H1・改訂履歴・live schema(§2)・positive fixture(§2.1)を一括で v1.5 へ同期**する。あわせて次の 2 件を**末尾追記でなく論理位置へ**編入した:
  - **(i) self-digest(自己 digest)の正形**(**P100-4.1**・W100-4.1)⟹ **§1.7(CV-10 細則・新設)** + **§2 の CV-10 ブロック(`sha256_ref` 型)** + **§2 規範 10** + **§2.1 negative fixture C / positive fixture(自己参照形)**。
  - **(ii) $\mathfrak h_3/\mathfrak h_4$ の用語登録**(**F100-4.3**)⟹ **§1.3.10(用語規約・新設)**(§1.3.9「fake」の語と同じ位置)。
  - v1.4 細則(§1.5/§1.6)は**内容不変**のまま版下に整理統合し、**裁定 412(adopted)/ 裁定 422(便 100 F100-7.1 追認)の記録を各節の見出しに保持**する。
  - **編入前の本ファイルの SHA-256 = `a7c9b27dbf6db852bac2d7a839c297e96bd7a95a38e5b6ad584459951b4caa7b`**(git 履歴に旧状態あり)。
  - **判断の申告(数学者の起草判断・司令塔レビュー対象)**: (i) は新規約 CV を立てず **CV-10 の細則(§1.7)**として置いた — 自己 digest は「有効出所連鎖の entry がどう自分を指すか」の問題であり、CV-10 の内側だからである。(ii) は §1.3.9 と同じ**用語規約**の系列に置いた。**別配置(例: CV-14 の新設)を司令塔が選ぶなら差し替える**(【CL-7】と同流儀)。
- **改訂 v1.6**: 2026-08-04・**裁定 428(便 101 検収)**。★ **W101-3.2 / W101-3.3 (c) / 裁定 428 (a) の 3 件を一回で編入**した改訂である。**H1・改訂履歴・live schema(§2)の `ledger_version` を v1.6 へ同期**したうえで:
  - **(i) 【CL-9】の全面書き換え**(**W101-3.2**)⟹ **§5.2**。v1.5 の「5 検査 checker の実装が**存在しない**」は**現況と矛盾**する(checker v1 は同じ納品束に実在し、便 101 で Sol が再実走した)。**checker v1 の path/SHA-256/実走結果**と、**v1 に残る未実装事項の正確な範囲(4 件)**を記す形へ置換し、**contract 完全版 = checker v2(製作中)**を **【CL-12】** として新規に開く。
  - **(ii) `sha256` XOR `sha256_ref` の排他規範を明文化**(**W101-3.3 (c) / P101-3 (3)**)⟹ **§2 規範 11(新設)** + **§2 冒頭の第五原則への 1 行** + **§1.7.3 の checker v2 追加契約 (vi)–(ix)**。v1.5 は「**両方書いたら** MALFORMED」までしか書いておらず、「**どちらも無い entry**」と「**checker が排他を強制すること**」が抜けていた。
  - **(iii) §1.5 の外部引用例の引用先訂正**(**裁定 428 (a)**・Fresse 訂正 A/B)⟹ **§1.5 動機欄**。`2008 Thm A.1` の `external_reference` 先を **Fresse SURV 217 Part 1 Theorem 6.2.4(b)(刊行版・証明本文あり)**へ、頁 pin を **p.11** へ訂正。
  - **編入前の本ファイルの SHA-256 = `783a6be187c519570d05dbb11cbfb353db534b0463b39a96e1a6d8050c833a78`**(git 履歴に旧状態あり)。
  - **判断の申告(数学者の起草判断・司令塔レビュー対象)**: XOR を **新 CV を立てず §2 の規範 11** として置いた — 排他性は `effective_source_chain` の**欄の型の規則**であり、CV-10 五原則⑤の直接の系だからである。**別配置(例: §1.7.4 の禁止項へ一本化)を司令塔が選ぶなら差し替える**(【CL-7】と同流儀)。
- **正典との関係**: `docs/week1-定義ノート.md` §1.5.1(規約 W-1〜W-4)+ §1.5.2 補題 W1 が唯一の**ゲート通過済み正本**。本台帳はそれを内包し、以後に発見された規約を同形式で中央化する。**正典と食い違う記述が本台帳にあれば正典が勝つ**。
- 先行文書: `docs/notes/convention_dictionary_W_v1.md`(candidate・(W-\*)(W-^)(W-nf)(W-perm))— 本台帳は同 4 項目を CV-1/CV-2 に吸収する上位集合。**正典への番号付与(W-5/W-6)は v1.1 で決着**(【CL-3】closed・CV-2 一本化)。

> ### v1.1 改訂記録(何をどこへ入れたか)
> **原則: 末尾継ぎ足し禁止 — 生きた正本は論理位置へ**(研究者指示)。
> | 由来 | 内容 | **編入先(正位置)** |
> |---|---|---|
> | **F94-5.2** | CV-9 の規範文(主検問・副検問・三値・差戻し・検問記録) | **§1.3(全面改訂)** |
> | **W94-5.1** | 非当事者性は肩書でなく記録で判定 | **§1.3.3** |
> | **P94-5.1 (1)(2)(3)(4)(5)(9)** | 型強化(多層 character・comparison target・separation・round-trip・coset/action 型・representative/invariant) | **§2 schema(全面改訂)** |
> | **P94-5.1 (6)** | CV-8 に既定値を置かない | **§1 表 CV-8 行 + §2** |
> | **P94-5.1 (7)** | effective source chain(errata 運用) | ★ **§1 表 CV-10(新設)+ §2** |
> | **P94-5.1 (8)** | seal recoverability | ★ **§1 表 CV-11(新設)+ §2** |
> | — | 【CL-3】【CL-4】【CL-5】【CL-6】の閉鎖 | **§5(未閉鎖項)** |
>
> **判断の申告**: (7)(8) は「欄の型強化」ではなく**新しい規約**なので、正位置は §1 の規約表と判断して **CV-10 / CV-11** を新設した(§2 の欄だけに置くと、規約表を読んだ者が存在に気づけない)。**この番号付与は数学者の起草判断であり、司令塔レビューの対象**である。

> **一行**: 今週の計器事故は例外なく「**規約が probe の頭の中にだけあり、文書にも cert にも現れていなかった**」型である。台帳は規約を**外在化**し、cert 欄で**照合可能**にする。

---

## 0. 事故台帳(教材リンク)— 何をこの制度で潰すのか

| # | 裁定 | 何が起きたか | 破られた規約 |
|---|---|---|---|
| 1 | **275→278** | 著者パッケージ = 20 に対し我々 3 系統 = 4。真犯人は粗↔精の**語順規約の食い違い**(Psi は語を反転して代入・粗列挙は順方向 ⟹ 同じ精元に $f$ と $f^{-1}$ の二つの粗ラベル)。Sol の独立器も同じ辞書規約を共有していたため検出できなかった | CV-3 / CV-4 |
| 2 | **282→298** | settled = 4/8/8 を構造として報告 → 実体は「ラベル著者側 × 共役我々側」の**混成規約の artifact**。整合規約 $T'$ で 20/20/0 | CV-2 / CV-6 |
| 3 | **306(a)** | $2m+1\equiv1 \pmod{2^a}$ の偽解 $m=2^{a-1}$ が**粗い指標 $\chi_{\rm vir}$ には不可視** | CV-5 |
| 4 | **306(b) 補題 OPP** | 数学者指定の assert 式が 160/240 で偽。正形は $\ell=\tau\circ\rho$($P^{\rm op}$ への準同型)— $\tau$ が**反準同型**であることの未宣言 | CV-6 |
| 5 | **312→313** | $\alpha=2,3$ 不一致。**当初診断「左右規約の取り違え(f/f⁻¹ 族 4 例目)」は裁定 313 で撤回** — 実体は S6 が固定 $\alpha'=1$ 窓とだけ比較していた**比較相手の未宣言**。二実装は一度も食い違っていなかった | CV-7 / CV-8 |
| 6 | **319**(便 94 W94-2.1) | C-β-IND の dummy 自己検査が**識別力ゼロ**。$\alpha=99$ は $\bmod7$ で $1$、$\alpha=5$ は $\pm$ 同値で窓 $[2]$ — **どちらも登録済み宇宙の内側**。さらに条文が要求する「任意の有理関数 $h$ に替える」操作は**実装の入力スキーマに存在しなかった** | CV-9(§1.3.2 識別力)/ CV-10(erratum) |
| 7 | **319**(便 94 F94-4.3) | 初荷 $\alpha$ が **sealed mapping の永続化欠品**で NOT_EXECUTED。数学的陰性ではなく工程 defect | CV-11 |
| 8 | **422**(便 100 W100-4.1) | ★ CV-10 正形化のつもりで作った cert の `sha256` 欄に **placeholder 文字列**(`SEE_MANIFEST(...)`)が入り、しかもその holder は**実在しない拡張子**(`.sha256`。実在は `.json`)を指していた ⟹ **fail-closed resolver が解決できない** = 正形化は完了していなかった。**「自己 digest を自分の bytes に埋める」という解けない自己参照を、型のない欄が受け入れてしまった**型 | CV-10(§1.7) |

> **申し送り(訂正)**: 委嘱文の「f/f⁻¹ 族 4 件」のうち **4 件目(裁定 312(c))は裁定 313 で機構主張ごと撤回済み**。確定している f/f⁻¹ 族は #1・#2・#4 の 3 件で、#5 は **comparison_target 欠落**が真因である。この訂正は制度の必要性を弱めない — むしろ「規約違反に見えた事故の一部は**比較相手の未宣言**だった」ことを示し、CV-7 の重みを上げる。

---

## 1. 大域規約(正本候補 CV-1〜CV-12)

| ID | 宣言(工房標準) | 格 | 事故 |
|---|---|---|---|
| **CV-1** | **置換・語の合成順序**。GAP native は**右作用** $i^{\,p*q}=(i^{p})^{q}$。工房標準(paper)は**左作用** $(AB)\cdot i=A\cdot(B\cdot i)$。ゆえに $\boxed{\text{paper 語 }AB\ \leftrightarrow\ \text{GAP }\texttt{q*p}\ \text{型}}$。**時間語(先に掛ける/後で掛ける)を正本に置かない** | **正典 W-1** | 裁定 109(F10)・`i24-u3-recheck`(自己捕獲) |
| **CV-2** | **作用の側・共役・剰余類の側**。GAP `X^g` $=g^{-1}Xg$(GAP 積)は CV-1 を 2 回通して**紙面の $\mathrm{inn}(g)(X)=gXg^{-1}$ そのもの** — $g$ を反転しない。剰余類の側は共役規約から**導出**される: $\bar y^{f}=f^{-1}\bar y f$ の下では $\bar y^{f}=\bar y^{f_0}\iff f\in C(\bar y)f_0$ = **左**剰余類 | candidate | SGN-ĉ・S2 / `pruning_law_v2` §6.3 の右剰余類 → `sat_l1_v1` §3.1 で左へ訂正(草稿内自己捕獲・cert 未汚染) |
| **CV-3** | **語の評価向き(層ごとに宣言)**。正典 W-2(prepend)は**紙面由来の語**の評価手続。GAP 内部で生成・保存された語(`PreImagesRepresentative` の出力等)には別途 `Rev` の要否があり、**同一対象にラベルを付ける二つの層は同じ向きでなければならない**。向きは「正しい向きが一つある」のではなく「**層ごとに宣言し、突き合わせる層の間で一致させる**」ものである | candidate | 裁定 278/280 |
| **CV-4** | **粗ラベル写像 coarse_of**。正本 = `coarse_of(w) := MappedWord(w,[gx,gy,gc],[xb,yb,()])`(**forward・`Rev` を掛けない**)。fiber ラベルは合成 `coarse_of ∘ WordOf`、`WordOf(q) := Rev(PreImagesRepresentative(epiP,q))`。**`Rev` は `WordOf` 側に 1 個だけ**置く(Psi が反準同型であることの帰結・裁定 278)— `coarse_of` 側に二重に掛けない | candidate(裁定 280 で発効) | 裁定 278/280 |
| **CV-5** | **$\chi$ の水準**。$\chi_N([m,f]):=2m+1 \bmod N_{\rm ord}$ は**粗い射影**(定義ノートの $\chi_{\rm vir}$・**$m$ を復元しない**)。$\tilde\chi_N([m,f]):=2m+1 \bmod 2N_{\rm ord}$ が**忠実**($\mathcal X_N\leftrightarrow(\mathbb Z/2N_{\rm ord})^\times$)。**指標から $m$ を復元する箇所では $\tilde\chi_N$ を使う**。$N$ が isolated のときに限り $\tilde\chi_N$ は群準同型 | **定理**(命題_円分持ち上げ_v2 補題 B4) | 裁定 306(a)・一斉点検 = 裁定 307 |
| **CV-6** | **反準同型の扱い(補題 OPP)**。写像が反準同型なら**終域を $P^{\rm op}$ と型付けて宣言する**。$\tau(g):=\hat c(g)^{-1}$ は生成元を固定する反自己同型で、正典の合成則 (3.53) $f_{12}=f_1E_{m_1,f_1}(f_2)$ は $\tau$-座標で $\boxed{g_{12}=\Phi'_{m_1,g_1}(g_2)\cdot g_1}$ と**逆順の積**になる。**素朴座標で準同型形の恒等式を assert してはならない** | **定理 + 機械 9600 対** | 裁定 306(b)・裁定 280(「redMap 準同型の近道」= 旧バグと代数的に同一) |
| **CV-7** | **比較相手の明示(comparison_target)**。二実装の照合は「**何と何を**」比べるかを、パラメータの**関数として**宣言する。固定既定値(例: $\alpha'=1$)との比較を「対応窓との比較」と呼ばない。**合格形には分離条件を含める**: 一致だけの試験は「何にでも当たる試験」でありうる | 手続き(裁定 313 で必須欄化) | 裁定 312/313 |
| **CV-8** | **判定基準の粒度(chi_P_criterion)**。$\chi_P$ の階層 $7\subset14\subset42$ のうち、厳密一致(7)と**完全共役類(14)は同答**、「同じ直線」(42)は**完全 fail-open**(3 窓全一致)。許容値 = `exact` / `conjugacy_class`、**`line` は禁止値**。★ **既定値は置かない**(P94-5.1(6)): **完全共役類は不変形**、**exact element は generator / orientation を固定した場合にのみ許す** — どちらを使ったかを cert が**必ず明示**する | 手続き(裁定 312(b) + **便 94 P94-5.1(6)**) | 裁定 310(fail-open の実地発見)・312(b) |
| **CV-9** | **仕様同一性判読(二検問・三値・差戻し)**。二系統一致を cross-checked と格付けする前に、**どちらの実装も書いていない者**が両側の仕様を判読し **PASS / FAIL / UNKNOWN** を裁定する。**規範文の正本は §1.3**(便 94 F94-5.2 逐条) | 手続き(裁定 316/318 + **便 94 F94-5.2**) | 裁定 312(a) stub の True・裁定 313 comparison_target 未宣言・裁定 319 識別力ゼロの dummy |
| **CV-10** | ★ **有効出所連鎖(effective source chain)**。文書・cert・定理を引用するときは **original / supersedes / errata・addenda** と各 digest を連鎖として記録し、**「その主張の現在有効な出所」が一意に定まる**ようにする。旧正本の冒頭には後継への誘導を置く。**旧証明だけを引用させない**。**細則: §1.5(正典 pin の証明本文有無欄)・§1.7(自己 digest の正形)** | 手続き(**便 94 P94-5.1(7)**・新設。細則は便 99 P99-7.1 / **便 100 P100-4.1**) | U2 の旧 cyclotomic-lift 本文(W94-1.1)・`c_beta_ind_dummy_h_selfcheck` の撤回(W94-2.1)・**self-hash 二段方式の現物が MALFORMED(W100-4.1)** |
| **CV-11** | ★ **封印 fixture の回収可能性(seal recoverability)**。封印・退避する fixture は **ID・digest・金庫参照・復元 preflight の結果**を残す。**「封印した」だけでは回収可能性の記録にならない** | 手続き(**便 94 P94-5.1(8)**・新設) | 初荷 $\alpha$ の sealed mapping 喪失 ⟹ NOT_EXECUTED(F94-4.3) |
| **CV-12** | ★ **派生表の機械生成則**。定義・閉形から導出可能な表は機械生成(生成スクリプト+SHA-256 併記)か定義との機械照合つきのみ・手展開禁止(詳細 = §1.4) | 手続き(裁定 323/324・研究者発案) | δ(n) 早見表の定義乖離(裁定 322) |
| **CV-13** | ★ **生成器・受理器の向き自己検査(orientation self-assert)**。候補生成器と受理判定式が同一対象を扱う probe では、**生成した各候補 f が受理式の方程式を実際に満たすことを生成直後に assert**(向き関数 YImg 等を 1 箇所だけ定義し生成・受理・生成条件の全てが同一関数を呼ぶ・鏡像切替は同時差替のみ)。新規 probe の必須テンプレ。規約メモでは止まらないことが 4 例で実証済 — 止まるのは実行時 assert のみ。★ **射程限定(便 98 F98-4.5・裁定 388 で追記)**: CV-13 は **internal orientation consistency gate** であって **canonical-fidelity gate ではない** — **生成器と受理器が同じ誤った `YImg` を共有すれば、一様な鏡像は素通りする**(自己整合は正典忠実性を含意しない)。⟹ CV-13 を満たす probe には、**外部 anchor**(既知集合との**集合等号** — 先例 = カナリア $m=0$ の 2280 集合等号)**または独立 source-map route(正典から独立に構成した期待表)を必ず併置する**。**併置なしに「向きが正典と一致」と書かない** | 手続き(裁定 382・数学者提案・司令塔鋳造 candidate)。**便 98 F98-4.5 で条件付き承認**(採択してよい・ただし上の射程限定と外部 anchor 併置義務つき) | 向き混用 4 例: kerchi v1.3 較正(8 vs 40)・07-31 cert 化(1/162)・pent 診断 v2・**カナリア anchor 120 vs 2280(裁定 377→382)** |

### 1.1 CV-3/CV-4 の運用判定(唯一の合否)— 往復 assert

規約の正否を地の文で議論しない。**操作的判定はただ一つ**:

> **往復 assert**: 精元 $q$ に対し `coarse_of(WordOf(q))` が、粗列挙側が同じ $q$ に付けるラベルと一致すること。
> **証人は自己逆元でない粗 $f$ を取ること**(裁定 278 の指紋 = 生存 4 行がちょうど自己逆元の粗 $f$ 2 種 × 2 $m$ だった。**自己逆元の証人はこの罠を原理的に検出できない** — 既存 unit test 3 元が全滅した理由)。
> ★ **記録の型**(v1.1・P94-5.1(4)): 証人は「自己逆でない**具体例**・**期待 label**・**出所**」の三つ組で記録する(`roundtrip_witness`・§2)。**一例で足りない小宇宙では全列挙(`mode: "exhaustive"`)を優先する** — 宇宙が小さいのに標本で済ませる理由は通常ない。

### 1.2 CV-7 の合格形(分離つき)— C-β S6 の型

> **(a) 一致**: model$(\alpha)$ は**対応する**抽象窓 $H_{2,\alpha,0}$ と共役。
> **(b) 分離**: $\alpha'\neq\alpha$ の全窓と**非共役**。
> 合格形 = $3\times3$ の**単位行列**。(a) のみは fail-open になりうる(実例 = CV-8 の「直線」基準)。

---

### 1.3 CV-9 仕様同一性判読(規範文・**便 94 F94-5.2 の条文で固定**)

> **起源**: 司令塔追記 2026-08-01・裁定 316/318・研究者発案。**v1.1 で Sol F94-5.2 の規範文をそのまま採用**(「CV-9 は次の規範文なら PASS とする」)。以下 §1.3.1 の 5 条は **Sol 指定の逐条**である。

**宣言**: 新発明量の二系統一致を cross-checked と格付けする前に、**どちらの実装も書いていない者**(既定 = falsifier(opus/max)・代替 = 第三数学者インスタンス)が両側の仕様を判読し、**「同一対象 / 別対象 / 判定不能」を三値で裁定する**。

#### 1.3.1 規範文(5 条・F94-5.2 逐条)

> **(CV-9-1) 主検問(計算前)**: **IF-FIRST 凍結時**に、非当事者が二系統の
> ① **入力 universe** ② **比較対象** ③ **同値関係** ④ **正規形(NF)** ⑤ **filter** ⑥ **失敗状態**
> を照合する。目的 = 無駄な計算の前に仕様齟齬を殺すこと。
>
> **(CV-9-2) 副検問(格付け直前)**: **cross-checked 格付けの直前**に、**凍結宣言と実際の二 artifact の diff** を照合する(大半は機械 diff)。実装中のズレ(stub 型)の網。
>
> **(CV-9-3) 三値**: 判定は **PASS / FAIL / UNKNOWN**。**PASS 以外では cross-checked に上げない。**
>
> **(CV-9-4) 差戻し**: **主検問後に仕様または normalizer が変われば、副検問で救済せず主検問へ差し戻す。**
>
> **(CV-9-5) 検問記録の束縛**: 記録には **両 source / spec digest**、**target**、**competitor universe**、**識別力を持つ dummy fixture** を束縛する。

#### 1.3.2 「識別力を持つ dummy fixture」の要件(CV-9-5 の操作化)

dummy は **raw label ではなく、仕様が採用する同値関係を通した後**に既存 fixture と異なることを **machine-check** せねばならない(Sol ★教材 1)。**二層の正規化**(入力層 = datum、出力層 = 判定対象)を各々明示し、**各層の外に出る dummy を 1 個以上**含めること。

- **先例(実装形)**: `docs/notes/u7_fire_log_v1_addendum_grade.md` §4.2.6.5–§4.2.6.7(C-β の二層正規化と DUM-1〜DUM-5)。
- **反例(識別力ゼロ)**: `u7_cbeta_final_20260801.json` の `c_beta_ind_dummy_h_selfcheck` — $\alpha=99\equiv1$、$\alpha=5\sim[2]$ で**両方とも登録済み宇宙の内側**(裁定 319 で証拠から撤回)。

#### 1.3.3 非当事者性の判定(W94-5.1)

**model label(opus/max 等)や担当名で CV-9 PASS にしてはならない。** 判定は次の**記録**による:

1. 当該**仕様・実装・一次 grading に関与していない**こと(関与の有無を明示的に申告)。
2. **参照した provenance**(読んだ source / cert / 凍結文書とその digest)の列挙。

#### 1.3.4 スコープ制限と格

**スコープ**: 判読は「**同一対象か**」の一点のみ — 仕様の数学的監査・実装レビュー・追加テスト発案・計画監査への拡大は**禁止**(気づきは 1 行で司令塔へ・展開判断は司令塔)。原則 1 走・三値 + 根拠数行。
**格**: 主検問をすり抜けた仕様齟齬の最終防衛は従来どおり外部アンカー・Sol・Lean(§4 の射程宣言は CV-9 にも適用)。

**事故**: stub の True(裁定 312(a) — 仕様相違でも値が偶然一致し比較の瞬間には誰も気づけない型)・comparison_target 未宣言(裁定 313)・識別力ゼロの dummy(裁定 319 / W94-2.1)。

### 1.3.9 用語規約: 「fake」の語(司令塔追記 2026-08-01・裁定 374/375・candidate・番号付与は Sol ゲート後)

- **fake** = 正典 2008/2401 Def 4.2 準拠の **A 型(非 genuine)** のみを指す。**B 型(genuine だが非算術)は「非算術証人」**と呼び fake と呼ばない(A 型は P1/P2 を殺すが P6 は殺さない・B 型が FAKE-KILL の証人)。
- 工房語 **pentagon-fake / arith-fake は正典語でない** — 使用時は「工房語(正典の fake = hexagon-fake に相当するのは A 型)」と注記。cert/ノートの新規記載はこの規約に従う(遡及不要・発見次第 erratum)。

### 1.3.10 用語規約: $\mathfrak h_3$ / $\mathfrak h_4$(**v1.5 新設**・便 100 **F100-4.3**・裁定 422)

**宣言**: $\mathfrak h_3,\mathfrak h_4$ は **group element ではなく、明示した bracket convention における homogeneous Lie element** として登録する。

| 記号 | 定義 | 住む場所 |
|---|---|---|
| $\mathfrak h_3$ | $[[x,y],x]+[[x,y],y]$ | $\mathrm{gr}_3(F_2)$ |
| $\mathfrak h_4$ | $[[[x,y],x],x]+4\,[[[x,y],x],y]+[[[x,y],y],y]$ | $\mathrm{gr}_4(F_2)$ |

**必須の併記 4 点**(これを欠く記載は不完全):
1. **係数環**(既定 = $\mathbb Z$。$\otimes\mathbb Q$ / $\bmod\,p$ 還元はそのつど明示)。
2. **bracket convention**(**左括弧**: $[[[x,y],x],x]$ は $\bigl[[[x,y],x],x\bigr]$)。
3. **$\bmod\,p$ 還元**を使う場合はその素数。
4. ★ **$\mathrm{Exp}$ した群元と同一視しない。** 有限群の中の元を指すときは別記号(例: $h_4\in\gamma_4(P)$)を立て、**どの同一視($\gamma_4(P)=\mathrm{gr}_4(P)$ 等)で対応させているかを書く**。

**禁止**:
- ★ **$\psi_4$ / $\sigma_3$ の記号でこの 2 元を書かないこと。** $\psi_n$ は正典 2405 (3.1) の dihedral 写像 $PB_3\to D_n^3$、$\sigma_1,\sigma_2$ は braid 生成元であり、**grep 事故の実例が既にある**(`hs_prop7_translation_v1.md` 危険箇所 D-9)。
- 「$\mathfrak h_4$ を通す/破る」を**群元の性質としてだけ**書くこと(どの層 — $\mathrm{gr}_4$ か $\gamma_4(Q)$ か — の主張かを明示する)。

**施行**: 新規文書・code・cert から必須。★ **既存 script(`search/probe/hsp7_v1/` の 5 本)の出力にはまだ `psi4`/`sigma3` が残っているので、次版 code/cert で $\mathfrak h_4/\mathfrak h_3$ へ改名する**(F100-4.3 の指示。過去 artifact は不改変・遡及不要)。

**格**: 用語規約(取り決め)。**番号付与(CV への昇格)は司令塔レビュー + Sol ゲート後**(§1.3.9 と同じ扱い)。

### 1.4 CV-12 派生表の機械生成則(司令塔追記 2026-08-01・研究者発案・裁定 324 で CV-10 衝突を改番)

**宣言**: 定義・閉形から導出可能な表(早見表・数値表・対応表)を文書に載せる場合、**機械生成**(生成スクリプトのパス+SHA-256 を表の直下に併記)か、**定義との機械照合**(checker スクリプト+照合結果)のいずれかを必須とする。人手展開の派生表は禁止。既存文書の手展開表は発見次第 erratum(定義側が正)。

**施行三点(v1.2・Sol 便 95 F95-3.3 で確定)**: CV-12 の履行は次の三点を**一束**にする — ①定義から表を生成する script ②script/input/output の digest ③文書 build 時に表と定義を再照合し不一致を fail-closed にする check。①だけ(生成したが照合が回らない)は不履行。

**格**: machine-piped 規律(cert の値の手写し禁止)の文書内派生物への拡張。同一文書内に定義と展開が併存する冗長表現は、機械照合がない限り「二重管理の事故源」とみなす。

**事故**: tmax_budget_and_holes_v1.md の δ(n) 早見表が同ノートの代数定義と 6 剰余類で不一致(裁定 322・CI 実測は定義側と整合)。照合スクリプトは定義から直接計算していたため 86/86 は無傷 — 表は機械に読まれない「飾り」として腐り、読む者だけを騙す位置にいた(stub 事件と同じ派生物ドリフト族)。

### 1.5 CV-10 細則: 正典 pin の「証明本文の有無」欄(司令塔追記 2026-08-01・裁定 399/406 採択 → **便 99 F99-7.1/P99-7.1 修文を反映し adopted(裁定 412・v1.4)** → ★ **便 100 F100-7.1 で意味内容を追認(裁定 422)。v1.5 で版下に整理統合 — 内容不変**)

- **宣言**: 正典の定理・命題を pin する読解ノート(reading_\*)・依存表は、pin ごとに次の欄を必須とする(Sol P99-7.1 の正形):
  - `proof_body_status = present | omitted | external_reference`
  - `omitted` の場合は追加で **`omission_kind = reader_exercise | silent_omission`** と **`source_wording`**(該当箇所の逐語 or null+理由)を必須 — 「読者演習」と「単に無い」を一値で潰さない。
  - `external_reference` の場合は**引用先定理・版・頁画像 pin・取得 digest** を必須。
- **動機(事故型)**: 「正典の定理」という格付けが証明本文の実在を含意しない事例が**系統的に 5 例**(2401 Prop 3.15 = omitted/reader_exercise・2405 Thm 4.4 奇分岐 = omitted/reader_exercise・2008 Thm A.1 = **external_reference**[★ **v1.6 訂正**(裁定 428 (a)): 引用先は **Fresse, SURV 217 Part 1, Theorem 6.2.4(b)**(刊行版・**刊行頁 212–214**・証明本文 **214–218** ⟹ **`proof_body_status = present`**・現物 `papers/Fresse_SURV217_Part1.pdf`)。**Part 2 Thm 1.1.5 は unitary 版**(strict unit 必須)につき**非 unitary** の工房使用を literally 覆わず**補助参照**、頁 pin も **p.11**(旧記載 pp.9-10 は誤り・profinite 注記は p.12)。精読正本 = `docs/notes/reading_fresse_624_v1.md`]・ほか 2405 Prop 4.1 偶/2008 Cor 3.13 = omitted[kind の確定は各 reading ノートの pin 欄が正本])。欄がないと依存の梯子の格上げ(未解決予想→記述の穴→外部引用 — 裁定 406 の 2 段格上げが実例)が台帳に現れない。★ **v1.6 の教材点**: この 1 件は **`external_reference` の鎖が `present` に着地した最初の例**であると同時に、**「版が違えば同じ番号でも射程が違う」**(unitary / 非 unitary)という**引用先の版まで pin する必要**を示した実例である。⟹ `external_reference` の必須 4 点(引用先定理・**版**・頁画像 pin・取得 digest)の「版」は**書名の版**だけでなく**規約の版**(unitary か否か等、言明が要求する構造)を含むと読む。
- **適用**: 新規 reading ノートから必須・既存は発見次第追記(遡及一括は不要・【CL-2】と同流儀)。「present」以外の pin に荷重を掛ける定理は、依存表にその値を伝播させ、自前補完 or 引用先言明の確認を検討対象として明示する。

### 1.6 CV-11 細則: 封印状態の正本・二鍵(司令塔追記 2026-08-01・裁定 410 → **便 99 F99-7.1/P99-7.2 修文を反映し adopted(裁定 412・v1.4)** → ★ **便 100 F100-7.1 で意味内容を追認(裁定 422)。v1.5 で版下に整理統合 — 内容不変**)

- **宣言**: 封印の開封状態は次の **AND 二鍵**で決める(Sol P99-7.2 の正形):
  1. リポジトリ `provenance/seals/` の `*.opened.json` の**存在**、かつ
  2. LEDGER の**開封イベント項**。
  - 単なる存在では弱い: opened JSON は**元 seal ID/digest・開封 blob digest・開封イベント/receipt ID を束縛**し、LEDGER 側も **opened artifact の digest を pin** する(双方向束縛)。
  - **二鍵のどちらかが欠ける・digest が食い違う場合は OPENED/SEALED を推測せず `INTEGRITY_STOP / UNKNOWN`**。
  - 金庫 `sealed/` ディレクトリの在庫から状態を推論することを**禁止**(開封プロトコルは「リポジトリへ複写公開・金庫原本は残置」— 残置は未開封を意味しない)。
- **事故**: 裁定 398 が seal_PSL_v1(2026-07-26 開封・7/7 的中・CLAIMS W3-6)を「封印維持」と誤記帳 — 金庫の残置原本から状態を誤読。裁定 410 で決着(三者ハッシュ一致・実質判断は無傷)。既存 seal_PSL_v1 の双方向 digest 束縛は充足済み(LEDGER 7/26 項がハッシュを pin・opened.json は封印体と byte-identical)。

### 1.7 CV-10 細則: **自己 digest(self-hash)の正形**(**v1.5 新設**・便 100 **P100-4.1 / W100-4.1**・裁定 422)

#### 1.7.1 問題の型(**主張の水準を間違えない**)

artifact が**自分自身の SHA-256** を自分の bytes の中へ通常の 64-hex 値として埋め、その bytes を再度 hash する運用は**循環する**。

> ★ **書いてよい正しい文**: 「これは**通常の生成・再現手順では解けない自己参照**であり、**schema として禁止する**。」
> ★ **書いてはならない文**: ~~「SHA-256 の不動点は**数学的に不可能**である」~~ — **そこまでは主張しない**(W100-4.1)。禁止の根拠は「数学的不可能性」ではなく「**運用上解けない + 機械照合が壊れる**」である。

#### 1.7.2 正形(**型つき参照**)

**`sha256` を union 型の自由文字列にしない。** 通常 entry は `path` と **64 桁 lowercase hex** の `sha256` を持つ。**自己参照のときだけ**、`sha256` の**代わりに**次の typed object を持たせる。

| 欄 | 意味 |
|---|---|
| `sha256_ref.holder_path` | 外部 manifest の**実在する** JSON path(**その拡張子で実在するファイルを指すこと**) |
| `sha256_ref.json_pointer` | target の `final_sha256` を指す**一意な** JSON pointer |
| `sha256_ref.resolution` | 固定値 `"external-postwrite"` |

#### 1.7.3 checker の 5 検査(**全て必須・一つでも欠ければ MALFORMED / INTEGRITY_STOP**)

| # | 検査 |
|---|---|
| **(i)** | `holder_path` の **holder が実在**すること |
| **(ii)** | `json_pointer` が指す **target path が一致**すること |
| **(iii)** | そこにある値が **64-hex** であること |
| **(iv)** | **target bytes の再計算が一致**すること |
| **(v)** | **current entry と `effective_source` の同一性** |

> ★ **fail-closed**: 一つでも欠ければ **MALFORMED / INTEGRITY_STOP**。**推測して PASS にしない。**

##### 1.7.3′ ★ **checker v2 の追加契約(v1.6 新設・便 101 P101-3 (2)(3)(4))**

上の 5 検査は **1 個の `sha256_ref` に対する検査**である。**resolver contract として完全であるためには、次の 4 項が要る**(便 101 W101-3.3 = 現 checker v1 は「一般に 5 検査を保証する」とは言えない、の指摘への正形)。

| # | 追加契約 | 何を塞ぐか |
|---|---|---|
| **(vi)** | cert 内の **全 `sha256_ref` を列挙**(**nested `superseded_by.sha256_ref` を含む**)し、**各々に (i)–(iv) を適用**する | 旧 erratum entry の参照が未走査のまま通る |
| **(vii)** | `current.path` = `effective_source.path` = **実入力 cert の repo-relative path** を強制する | 両 path を同じ偽値に変え holder を正しく保てば (v) は通りうる |
| **(viii)** | 各 entry につき **`sha256` XOR `sha256_ref`** を強制(**両方書いたもの・どちらも無いもの**を MALFORMED) | 排他型違反の素通り(§2 規範 11) |
| **(ix)** | 上の各述語について **一変異一発火の負例 fixture** を置く | 「負例が薄いので検査の実効性が未検証」型 |

> ★ **格の書き方**: (vi)–(ix) が入るまでは、**「checker が一般に 5 検査を保証する」と書かない**。書いてよいのは「**この cert のこの参照については 5 検査が PASS した**」までである(**instance-level の PASS と contract の完全性は別**)。実装状況は **【CL-9】/【CL-12】**(§5.2)。

#### 1.7.4 禁止(新規 cert から)

1. ★ **placeholder(`SEE_MANIFEST(...)` 等の非 64-hex 文字列)を `sha256` 欄へ入れる方式は新規禁止。**
2. `superseded_by.sha256` / `effective_source.sha256` に 64-hex 以外を入れた cert は **MALFORMED**。
3. **holder の拡張子違い**(`.sha256` を指しているが実在するのは `.json`)は **fail-closed resolver が参照を解決できない** ⟹ MALFORMED。

#### 1.7.5 事故(現物・**過去 file は編集しない**)

- **`ihnec_r4b_conventions_v2_20260802.json`**(便 99 の CV-10 正形化の現物): (1) `superseded_by.sha256` と `effective_source.sha256` に 64-hex でない `SEE_MANIFEST(...)` が入っており、v1.3/v1.4 schema では **MALFORMED**。(2) placeholder は `search/certs/MANIFEST_sol99_w99_2_1_20260802.sha256` を指すが、**実在する外部 holder は `.json`** ⟹ fail-closed resolver は参照を解決できない。
- ★ **格の記帳**: 本 file は「**逸脱を正直に申告した record**」として**保存する**。ただし **CV-10 正形化完了とは数えない**(W100-4.1)。
- ★ **修理の方法**: **過去 file は編集せず、v3 supplement で直す**(CV-10 の erratum 運用そのもの)。

## 2. cert 必須ブロック `conventions_used`(schema)

**適用**: 新規 cert から。**既存 cert への遡及は不要**(⟹ 本欄の不在は旧 cert について何の情報も与えない・【CL-2】)。

**型付けの原則(v1.1・P94-5.1)**: **boolean と自由文だけの欄は弱い。** 「宣言した」ことが「機械で突き合わせられる」ことを意味するように、**比較・分離・多層・出所・封印**の各欄は**構造化して束縛する**。

**"n/a" の型(v1.2・F95-3.3)**: 全型で "n/a" を許すなら、将来の JSON schema では各 field を文字列との union にするか、型つき `{status:"n/a", reason:...}` に統一する — object/array 欄へ bare string を入れて schema が壊れる事故を防ぐ。

**CV-10 出所連鎖の schema 統一(v1.3・裁定 354・ASM v2 §V.4.3 の未同期 4 点を確定)**: 新規 cert/ノートから適用(遡及不要)。①`path` は**リポジトリ root 相対で参照対象 artifact 自身**を指す(生成 script や親文書ではない)②ハッシュのキー名は **`sha256`**(Sol 語彙に統一・`digest` は不使用)③`effective_source` は**文字列でなく object** `{path, sha256}` ④supersede 関係は入れ子欄 **`superseded_by: {path, sha256}`** で機械可読に持つ(散文の「失効」注記は人間用の副)。混在は機械照合を壊すため、以後この 4 点が正。

★ **第五原則(v1.5・便 100 P100-4.1・裁定 422)**: ⑤ **`sha256` は 64 桁 lowercase hex に限る**。**自己参照のときだけ** `sha256` の代わりに typed object **`sha256_ref: {holder_path, json_pointer, resolution:"external-postwrite"}`** を置く(**規範文と checker 5 検査は §1.7**)。**placeholder 文字列を `sha256` 欄へ入れる方式は新規禁止。** ★ **v1.6 追記(便 101 W101-3.3 (c))**: ⑤の「代わりに」は **排他的 OR** の意味である — **各 entry はちょうど一方を持つ**(**規範 11**)。

```jsonc
"conventions_used": {
  "ledger_version": "conventions_ledger_v1_6",

  // ---- CV-1 / CV-2: 合成順序・作用の側 ----
  "perm_composition":  "gap_native_right" | "paper_left",   // CV-1
  "conjugation":       "gap_caret_g_inv_X_g" | "paper_inn_g_X_g_inv", // CV-2
  "coset_object":      "left_coset_gH" | "right_coset_Hg",  // CV-2 / P94-5.1(5) 型分離
  "action_side":       "OnLeft" | "OnRight",                // CV-2 / P94-5.1(5) 自由文で代用しない
  "coset_side_derivation": "<共役規約からの導出を一文で>",   // CV-2(導出であって独立選択ではない)

  // ---- CV-3 / CV-4: 語の向きと粗ラベル ----
  "word_eval": [                                            // CV-3: 層ごとに 1 entry
    { "layer": "psi", "direction": "reversed", "word_source": "internal_gap" },
    { "layer": "coarse_enumeration", "direction": "forward", "word_source": "internal_gap" }
  ],
  "coarse_of":         "MappedWord_forward_no_rev",         // CV-4
  "word_of":           "Rev(PreImagesRepresentative)",      // CV-4(Rev の置き場所)

  // ---- §1.1: 往復 assert(P94-5.1(4) 型強化)----
  "roundtrip_witness": {                                    // 一例だけで足りない小宇宙では全列挙を優先
    "mode":            "exhaustive" | "sampled",
    "witnesses":       [ { "element": "<具体例>", "is_self_inverse": false,
                           "expected_label": "<期待値>", "source": "<出所+digest>" } ],
    "result":          true
  },

  // ---- CV-5: 多層 character(P94-5.1(1) 型強化: 単一 enum を廃止)----
  "characters": [                                           // 配列。層ごとに 1 entry
    { "layer": "chi_vir", "purpose": "coarse_projection", "modulus": "N_ord",
      "faithful": false, "source": "<定義ノート §/式番号>" },
    { "layer": "chi_tilde_N", "purpose": "recover_m", "modulus": "2*N_ord",
      "faithful": true,  "source": "<同上>" }
  ],

  // ---- CV-6: 反準同型 ----
  "opposite":          { "map": "tau", "antihomomorphism": true, "codomain": "P^op" },

  // ---- CV-7: 比較相手(P94-5.1(2) 型強化: prose だけでは不可)----
  "comparison_target": {
    "as_function_of":  "<パラメータの関数として一文で>",      // 裁定 313
    "function_a":      { "name": "<関数/実装>", "domain": "<定義域>", "source_digest": "<sha256>" },
    "function_b":      { "name": "<関数/実装>", "domain": "<定義域>", "source_digest": "<sha256>" },
    "normalization_digest": "<NF 仕様の sha256>"
  },

  // ---- §1.2: 分離条件(P94-5.1(3) 型強化: included=true では不可)----
  "separation": {
    "included":            true,
    "competitor_universe": [ "<比較対象の全列挙>" ],
    "result":              { "matrix": "<比較行列>" } | { "result_digest": "<sha256>" },
    "forbidden_values":    { "handling": "MALFORMED" | "reject_with_reason", "list": [ "line" ] },
    "dummy_fixture":       {                                // CV-9-5 / §1.3.2
      "id": "<ID>", "normalised_input": "<入力層の正規化値>",
      "normalised_output": "<出力層の正規化値>",
      "discriminating_power": { "input_layer_novel": true, "output_layer_novel": true },
      "expected": "<事前登録の期待値>", "observed": "<実測>", "verdict": "PASS"
    }
  },

  // ---- CV-8: 判定粒度(P94-5.1(6): 既定値なし)----
  "chi_P_criterion": {
    "value":   "exact" | "conjugacy_class",                 // "line" は禁止値・既定値は置かない
    "justification": "<conjugacy_class = 不変形 / exact = generator・orientation を固定した場合のみ>",
    "generator_fixed":   true | "n/a",                      // value=="exact" のとき必須
    "orientation_fixed": true | "n/a"                       // 同上
  },

  // ---- P94-5.1(9): 代表元と不変量の分離 ----
  "representative_vs_invariant": {
    "exact_representative": { "value": "<値>", "depends_on":
        { "model_id": "<sha256>", "uniformizer_id": "<記号>", "orientation": "<向き>",
          "lift": "<整数持上げ等>" } },
    "invariants":           { "class": "<類>", "order": "<位数>" }   // これらは上記に依存しない
  },

  // ---- CV-10: 有効出所連鎖(v1.3・裁定 354・便 97 P97-1.2(1)-(4)/ v1.5・裁定 422・便 100 P100-4.1)----
  // 五原則: ①path=参照対象 artifact 自身(生成 script や親文書ではない)
  //         ②ハッシュキー名は sha256(digest は不使用)
  //         ③effective_source は object {path,sha256}(string 不可)
  //         ④supersede 関係は各 entry の superseded_by:{path,sha256} で「旧→新」を表す
  //           (role:"supersedes" は廃止・新エントリを role:"current" として置く)
  //   ★ v1.5 ⑤sha256 は 64 桁 lowercase hex のみ。自己参照時だけ sha256 の代わりに
  //           sha256_ref:{holder_path, json_pointer, resolution:"external-postwrite"} を置く。
  //           placeholder 文字列(SEE_MANIFEST(...) 等)を sha256 欄へ入れるのは新規禁止(§1.7)。
  "effective_source_chain": [
    { "role": "original", "path": "<最初の artifact の path>", "sha256": "<64-hex>" },
    { "role": "erratum",  "path": "<訂正した旧 artifact の path>", "sha256": "<64-hex>",
      "scope": "<何を撤回/訂正したか>",
      "superseded_by": { "path": "<後継 artifact の path>", "sha256": "<64-hex>" } },
    { "role": "current",  "path": "<現在有効な artifact の path>", "sha256": "<64-hex>" }
  ],
  "effective_source": { "path": "<連鎖の role:\"current\" entry と同じ path>", "sha256": "<同 64-hex>" },

  // ★ v1.5: 自己参照 entry の正形(この cert 自身を連鎖に載せる場合のみ)。
  //   sha256 と sha256_ref は排他 — 両方書いた entry は MALFORMED。
  //   checker 5 検査(§1.7.3): (i) holder 実在 (ii) target path 一致 (iii) 64-hex
  //                            (iv) target bytes の再計算一致 (v) current entry と effective_source の同一性
  //   一つでも欠ければ MALFORMED / INTEGRITY_STOP(推測して PASS にしない)。
  // { "role": "current", "path": "<この cert 自身の path>",
  //   "sha256_ref": { "holder_path":  "<実在する外部 manifest の JSON path>",
  //                   "json_pointer": "<target の final_sha256 を指す一意な JSON pointer>",
  //                   "resolution":   "external-postwrite" } },
  // "n/a" 型(v1.2 F95-3.3・便97 P97-1.2(5)で確定): cross-checked を主張しない cert では
  // effective_source_chain / effective_source は bare "n/a" ではなく
  // { "status": "n/a", "reason": "<この cert は単系統探索であり cross-checked を主張しない>" } を書く。

  // ---- CV-11: 封印回収可能性(P94-5.1(8))----
  // 注: このブロックの digest キーは CV-11 の欄であり CV-10 の sha256 統一(v1.3)の対象外
  // (P97-1.2(2) は「当該 CV-10 範囲」に限定・CV-11 の改名は別途裁定が要る)。
  "seal_recoverability": [
    { "fixture_id": "<ID>", "digest": "<sha256>", "vault_reference": "<金庫内の参照子>",
      "restore_preflight": "PASS" | "FAIL" | "NOT_RUN", "checked_utc": "<ISO8601>" }
  ],
  // 封印 fixture を使わない cert では bare "n/a" ではなく
  // { "status": "n/a", "reason": "<この cert は封印 fixture を使用しない>" } を書く(v1.2 F95-3.3)。

  // ---- 水準 ----
  "level":             "PB3" | "PB4"                        // 水準の混同禁止(p93 追補 §3.3)
}
```

**規範**:
1. 該当しない欄は**省略でなく `"n/a"`** と書く(欠品と非該当を区別する)。**ただし scalar(string/boolean)欄に限る**。object/array 欄は規範 8 に従う(v1.2 F95-3.3・便97 P97-1.2(5))。
2. `chi_P_criterion.value: "line"` を含む cert は **MALFORMED**。**`chi_P_criterion` を省略した cert も MALFORMED**(既定値を置かないため・P94-5.1(6))。
3. `roundtrip_witness` に自己逆元の witness しか無いものは**証拠として無効**(§1.1)。小宇宙では `mode: "exhaustive"` を優先する。
4. 二実装照合の cert では `comparison_target` の欠落を **MALFORMED** とする(裁定 313)。**prose のみ(`as_function_of` だけ)で `function_a/b` と digest を欠くものも MALFORMED**(P94-5.1(2))。
5. `separation.included: true` だけで `competitor_universe` と結果(行列 or digest)を欠くものは **MALFORMED**(P94-5.1(3))。
6. **cross-checked を主張する cert** は `effective_source_chain`(CV-10)と、封印物を使うなら `seal_recoverability`(CV-11)を**必須**とする。
7. **`representative_vs_invariant` の混記を禁止**: 代表元の値を不変量の欄に書いた cert は **MALFORMED**(格の過大表示の直接原因・CV-7 の記法規律)。
8. **object/array 欄の "n/a" は型つき**(v1.2 F95-3.3): bare string `"n/a"` を object/array 欄(`effective_source_chain`・`effective_source`・`seal_recoverability` 等)に入れることを禁止し、`{ "status": "n/a", "reason": "<理由>" }` の形で書く。bare string を object/array 欄に入れた cert は **MALFORMED**。
9. **CV-10 は五原則(§2 冒頭・v1.3 の四原則 + v1.5 の第五原則)で書く**: `digest` キー・string 型 `effective_source`・`role:"supersedes"` を使った cert(§2.1 の v1.1 歴史形)は新規 cert では **MALFORMED**。旧 cert への遡及は不要(【CL-2】)。
10. ★ **自己 digest は §1.7 の正形でのみ書く**(v1.5・P100-4.1): `sha256` 欄は **64 桁 lowercase hex のみ**。自己参照は `sha256_ref`(typed object)で表し、**`sha256` と `sha256_ref` を同一 entry に両方書いたものは MALFORMED**。**placeholder 文字列を `sha256` 欄へ入れた cert は新規では MALFORMED**。checker 5 検査(§1.7.3)のいずれかが欠ければ **MALFORMED / INTEGRITY_STOP**(推測して PASS にしない)。旧 cert への遡及は不要(【CL-2】)。
11. ★★ **`sha256` XOR `sha256_ref`(排他規範)**(**v1.6 新設**・便 101 **W101-3.3 (c) / P101-3 (3)**): **digest を持つ全ての欄**(`effective_source_chain` の各 entry・`effective_source`・入れ子の `superseded_by`)は、**`sha256` と `sha256_ref` の ちょうど一方**を持つ。
    - **両方を持つ entry は MALFORMED**(規範 10 の再掲)。
    - ★ **どちらも持たない entry も MALFORMED**(v1.6 で明文化。「欄を落として素通りさせる」型を塞ぐ — 欠品と非該当を区別する規範 1 の digest 版)。
    - ★ **これは checker が強制すべき述語である**(§1.7.3′ (viii))。**規範を文書に書いただけでは止まらない**(CV-13 の教訓)。⟹ **checker v2 が入るまでは、排他違反は人手照合で見るしかない**ことを **【CL-12】** に記帳する。
    - **旧 cert への遡及は不要**(【CL-2】)。

### 2.1 CV-10 の v1.1 歴史形(新規禁止)と v1.5 の positive/negative fixture(便 97 P97-1.2(6)・**便 100 P100-4.1 で自己参照形を追加**)

**v1.1 歴史形**(参照専用・**新規 cert での使用禁止**・遡及なしのため既存 cert は無罪):

```jsonc
// MALFORMED(v1.3 以降の新規 cert では禁止)
"effective_source_chain": [
  { "role": "original",  "path": "<path>", "digest": "<sha256>" },
  { "role": "supersedes","path": "<path>", "digest": "<sha256>" },
  { "role": "erratum",   "path": "<path>", "digest": "<sha256>", "scope": "<...>" }
],
"effective_source": "<string>"
```

**negative fixture A**(v1.1 形そのまま・`digest` キー + string `effective_source` + `role:"supersedes"`): 上記と同一。**MALFORMED**(規範 9)。

**negative fixture B**(便 96 F96-1.5 の旧例と同じ**逆向き** `supersedes`: 新 entry が旧 entry を指す形。便 97 W97-1.2 でこの向きは erratum と訂正された): 例えば `{"role":"current","path":"new.md","sha256":"NEW"},{"role":"supersedes","path":"old.md","sha256":"OLD","supersedes":{"path":"new.md","...}}` のように新→旧を指す構造。**MALFORMED**(旧→新の `superseded_by` でなければならない・§2 CV-10 四原則④)。

★ **negative fixture C**(**v1.5 新設**・便 100 W100-4.1 の現物型 = **placeholder を `sha256` 欄へ入れた self-hash 二段方式**):

```jsonc
// MALFORMED(v1.5 以降の新規 cert では禁止・規範 10)
"effective_source_chain": [
  { "role": "erratum", "path": "docs/.../old.json", "sha256": "<64-hex>",
    "superseded_by": { "path": "docs/.../new.json", "sha256": "SEE_MANIFEST(search/certs/MANIFEST_xxx.sha256)" } },
  { "role": "current", "path": "docs/.../new.json", "sha256": "SEE_MANIFEST(search/certs/MANIFEST_xxx.sha256)" }
],
"effective_source": { "path": "docs/.../new.json", "sha256": "SEE_MANIFEST(search/certs/MANIFEST_xxx.sha256)" }
```
**MALFORMED の理由(2 つとも独立に致命)**: ① `sha256` 欄が **64-hex でない**(規範 10・§1.7.4-1)。② holder として指した `...MANIFEST_xxx.sha256` が**実在せず、実在する holder は `.json`** ⟹ **fail-closed resolver が参照を解決できない**(§1.7.4-3)。
**現物**: `ihnec_r4b_conventions_v2_20260802.json`(**過去 file は編集しない**。「逸脱を正直に申告した record」として保存し、**CV-10 正形化完了とは数えない** — 修理は **v3 supplement** で・§1.7.5)。

**positive fixture A**(**通常形**・v1.5 正形・§2 の live schema と同型):

```jsonc
"effective_source_chain": [
  { "role": "erratum", "path": "docs/notes/fam_u_v1_addendum_f94.md", "sha256": "<OLD_64hex>",
    "scope": "<撤回/訂正した内容>",
    "superseded_by": { "path": "docs/notes/fam_u_v1_addendum_f96.md", "sha256": "<NEW_64hex>" } },
  { "role": "current", "path": "docs/notes/fam_u_v1_addendum_f96.md", "sha256": "<NEW_64hex>" }
],
"effective_source": { "path": "docs/notes/fam_u_v1_addendum_f96.md", "sha256": "<NEW_64hex>" }
```
**PASS**: `path` は各 entry 自身の artifact、`sha256` キー統一かつ **64-hex**、`superseded_by` は旧→新、`effective_source` は object で current entry と一致。

★ **positive fixture B**(**v1.5 新設・自己参照形**・P100-4.1 の typed object):

```jsonc
"effective_source_chain": [
  { "role": "erratum", "path": "docs/.../old.json", "sha256": "<OLD_64hex>",
    "scope": "<撤回/訂正した内容>",
    "superseded_by": { "path": "docs/.../this_cert.json",
                       "sha256_ref": { "holder_path":  "search/certs/MANIFEST_xxx.json",
                                       "json_pointer": "/entries/3/final_sha256",
                                       "resolution":   "external-postwrite" } } },
  { "role": "current", "path": "docs/.../this_cert.json",
    "sha256_ref": { "holder_path":  "search/certs/MANIFEST_xxx.json",
                    "json_pointer": "/entries/3/final_sha256",
                    "resolution":   "external-postwrite" } }
],
"effective_source": { "path": "docs/.../this_cert.json",
                      "sha256_ref": { "holder_path":  "search/certs/MANIFEST_xxx.json",
                                      "json_pointer": "/entries/3/final_sha256",
                                      "resolution":   "external-postwrite" } }
```
**PASS の条件 = §1.7.3 の 5 検査すべて**: (i) `search/certs/MANIFEST_xxx.json` が**実在**(拡張子まで一致)(ii) `json_pointer` の指す entry の path が `docs/.../this_cert.json` と一致 (iii) そこにある値が **64-hex** (iv) その 64-hex が `this_cert.json` の bytes の**再計算と一致** (v) `current` entry と `effective_source` が**同一**。
**一つでも欠ければ MALFORMED / INTEGRITY_STOP**(§1.7.3)。

---

## 3. 手順則 **IF-FIRST**(interface first)

> **二実装が突き合う場面では、実装の前に比較インターフェースを凍結する。**

1. **凍結対象** = ①比較する対象 ②**正規形(NF)** ③合否等式の一覧 ④合格形(**分離条件を含む**・§1.2) ⑤両側の `conventions_used` 宣言。
2. **生比較の禁止**。先例 = EP の **NF 方式**(裁定 311): 生 field 比較を禁じ、正規形 NF(4 欄)を spec §4.1 に凍結、各 lane が**独立に** NF を計算し NF 同士を 5 等式(N-1〜N-5)で比較。
3. **独立性は壊れない**。「**NF は形式契約であって共有実装ではない**」(`lanea_native_semantics_v1.md` §4)。逆に共有 helper 実装を配ると独立性偽装になる(裁定 305 (a) 禁止・sol75 精神)。
4. **条項は両側へ同時に降ろす**(裁定 311 C-5)。片側耳打ちは独立性違反。
5. **合格形の先例** = C-β の **S6 二条件**(裁定 313・§1.2)。
6. **順序**: インターフェース凍結 → 各側実装 → 照合。**不一致が出てから機構を推測しない** — 先に両側の入出力仕様を突き合わせる(裁定 313 ★教材)。

---

## 4. 限界(射程宣言)

- **完全仕様ではない**。**未発明の概念の規約は事前列挙できない** — 本台帳は「**既知規約の中央化 + 初接触時の即文書化**」であって、これを満たせば規約事故が起きないという主張では**ない**。
- **宣言は正しさを含意しない**。`conventions_used` が全欄埋まった cert は「規約が**監査可能**」なだけで「規約が**正しい**」ことは意味しない。裁定 278 では**両層とも内部的には整合**していた — 台帳が買うのは「二つの宣言を 1 回の diff で突き合わせられる」ことだけである。
- **格の差**。CV-1 のみゲート通過済み正典、CV-5/CV-6 は定理、残りは candidate または手続き。**candidate 項目を「工房が証明した」と引用しない**。
- **規約は取り決めであって定理ではない**(CV-1/CV-2/CV-4)。台帳はどれが数学的に正しいかを決めない — **一貫性**だけを要求する。
- **遡及なし**ゆえ、旧 cert の規約は本台帳では保証されない。
- ★ **事故台帳(§0)は悉皆調査ではない**(旧【CL-5】をここへ移設・**恒久の射程宣言**)。§0 は「今週分 + grep で確認した既知例」であり、同型の未発見事故がありうる(`convention_dictionary_W_v1` 【WDICT-3】と同じ留保)。**§0 の件数を「工房で起きた規約事故の総数」として引用してはならない。** これは調査すれば閉じる種類の項目ではなく(非存在の証明になる)、**常に付す留保**である。

---

## 5. 未閉鎖項(v1.1 で更新・**v1.5 で §5.2 を追加**)

| # | 状態 | 内容 |
|---|---|---|
| **【CL-1】** | ★ **格下げ(部分閉鎖)** | 本稿は **candidate** のまま。ただし **Sol 便 94 F94-5.1 で CV-1〜8 の方向は承認**され、**F94-5.2 の CV-9 規範文は v1.1 §1.3.1 に逐条で採用**、**P94-5.1 の 9 項は §1.3/§1 表/§2 に編入済**。⟹ 残るのは**司令塔検分**と**次便での条件履行確認**のみ。正典としての引用は引き続き不可 |
| **【CL-2】** | **未閉鎖(先鋭化)** | `conventions_used` の**遡及なし**。v1.1 で問いを絞る: 遡及の価値があるのは「**cross-checked 以上の格を主張している既存 cert**」に限られる(それ以外は遡及しても格が変わらない)。⟹ 決めるべきは「その集合を列挙して CV-10 の `effective_source_chain` だけ後付けするか」の一点。**司令塔裁定待ち** |
| **【CL-3】** | ★ **CLOSED(v1.1)** | 正典 §1.5.1 へ **W-5/W-6 を追記しない**。(W-^)(W-nf) は **CV-2 に一本化**する。**理由**: (i) 正典はゲート通過済みの凍結面であり、candidate 由来の番号を足すと「ゲートを通った番号」と「通っていない番号」が同じ体系に混在する、(ii) 番号体系の二重化それ自体が新しい事故源(【CL-3】原文の懸念)、(iii) v1.1 で台帳が**生きた正本**として機能する体裁が整ったので、追記先を台帳に一本化できる。**⟹ 正典は凍結・台帳が増える、という一方向を規約とする。**(数学者の起草判断 — 司令塔レビュー対象) |
| **【CL-4】** | ★ **CLOSED(CV-6 へ吸収)** | `Rev` の置き場所の必然性は、**CV-6(反準同型の型付け)の特例**として説明が閉じる: $\Psi$ が反準同型であることは「精 → 粗のラベル経路上に**順序反転がちょうど 1 個**必要」を意味し、`Rev` はその反転を置く**境界の指定**である(2 個置けば打ち消し、0 個なら型が合わない)。**移植条件**も同時に定まる: 別の窓へ移植してよいのは、**その窓の $\Psi$ が再び反準同型であることを cert の `opposite` 欄で宣言・検査した場合に限る**。⟹ 「どこに置くか」は規約、「1 個必要」は定理(CV-6)、「移植可否」は検査可能な条件 |
| **【CL-5】** | ★ **CLOSED(§4 へ移設)** | 悉皆調査していないという留保は**閉じる種類の未閉鎖項ではない**(閉じるには非存在証明が要る)。⟹ **恒久の射程宣言**として §4 へ移設した |
| **【CL-6】** | ★ **CLOSED(P94-5.1(6))** | CV-8 の **既定値は置かない**。`conjugacy_class` は不変形、`exact` は **generator / orientation を固定した場合にのみ**許す。既存 cert(`u7_cbeta_final_20260801.json` の `"exact"`)は裁定 312(b) の「同答」により**実害なし**だが、v1.1 以後は `chi_P_criterion.justification` と `generator_fixed` / `orientation_fixed` の記入が必須 |

### 5.1 v1.1 で新たに開いた項

| # | 内容 |
|---|---|
| **【CL-7】** | **CV-10 / CV-11 の番号付与**は数学者の起草判断(§0 冒頭の改訂記録参照)。「型強化を新規約として立てる」境界は一般には自明でない — 司令塔が別配置(例: §2 の欄のみ)を選ぶなら差し替える |
| **【CL-8】** | **schema の実装コスト**。v1.1 の `conventions_used` は v1 より欄が増えた。**全欄必須にすると小さな probe cert が書けなくなる** — 「cross-checked を主張する cert は全欄必須 / 単系統の探索 cert は縮約版」という**二層適用**が要るかもしれない。未検討 |

### 5.2 v1.5 で新たに開いた項(裁定 422)・**v1.6 で更新**(裁定 428)

| # | 内容 |
|---|---|
| **【CL-9】** | ★ **CLOSED(v1.6・裁定 428・便 101 P101-3 (5) の履行)。** ★ **v1.5 の記述「5 検査 checker の実装が存在しない・未実装」は撤回する** — **checker は実在し**、便 101 で Sol が再実走した(W101-3.2 の指摘は正しい)。**現物**: `search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py`(**SHA-256 = `659043405b34503f1b0ee6a20884e2766c6bd419af1a018f7faed2e3ad2c2864`**)。**実走結果**(便 101 F101-0.1・Sol 側の独立再実行): 現 v3 cert に対し **5 項目 PASS**、`--selftest` は **1 PASS + 3 STOP**、旧 v2 を直接入力すると **INTEGRITY_STOP**。★ **checker v1 に残る未実装事項の正確な範囲(4 件・便 101 W101-3.3)**: ① **全 `sha256_ref` を走査しない**(解決するのは `role=current` と `effective_source` の 2 つのみ・**nested `superseded_by.sha256_ref` は未走査**)② (v) は `current.path == effective_source.path` **しか見ず**、両者が**実入力 cert の repo-relative path** と一致することを検査しない(両方を同じ偽値に変え holder を正しく保てば通りうる)③ 同一 entry の **`sha256` / `sha256_ref` 併記(排他型違反)を拒否しない**(規範 11)④ **負例が 3 件のみ**(holder 欠落・target path 違い・bytes 違い)で、**64-hex 型違反・current/effective 不一致・上記①②③を発火させる負例がない**。⟹ ★ **「checker が一般に 5 検査を保証する」とは書かない**(便 101 W101-3.3 = **FAIL**)。**contract 完全版 = checker v2**(製作中)= **【CL-12】**。**v2 が着地するまでは、自己参照形の cert に positive fixture B への手照合記録を添える**(v1.5 からの継続) |
| **【CL-10】** | ★ **§1.3.10 の改名(`psi4`/`sigma3` → $\mathfrak h_4/\mathfrak h_3$)が既存 script に未反映。** 対象 = `search/probe/hsp7_v1/` の 5 本(出力キー名)。**過去 artifact は不改変・遡及不要**だが、**次版 code/cert で改名する**という約束が守られたかを次の便で確認する必要がある(F100-4.3)。確認しないと「規約は書いたが誰も従っていない」型の腐りに入る |
| **【CL-11】** | **v1.5 の 2 件の配置は数学者の起草判断**(§0 改訂 v1.5 の「判断の申告」)。(i) 自己 digest を **CV-10 細則 §1.7** に置いたこと、(ii) $\mathfrak h_3/\mathfrak h_4$ を **§1.3.10 の用語規約**に置いたこと。**司令塔が別配置(CV-14 の新設等)を選ぶなら差し替える**(【CL-7】と同流儀)。**Sol ゲート未了** |

### 5.3 v1.6 で新たに開いた項(裁定 428)

| # | 内容 |
|---|---|
| **【CL-12】** | ★ **checker v2(contract 完全版)が未着地。** §1.7.3′ の **(vi)–(ix)**(全 `sha256_ref` の列挙[nested 含む]・実入力 path との一致強制・`sha256` XOR `sha256_ref` の強制・各述語への一変異一発火の負例)を満たす resolver を **実装係が並行製作中**。★ **path / SHA-256 / 実走結果は着地後に司令塔が本欄へ追記する**(**数学者が予測値を書かない** — machine-piped 規律)。**未着地の間は**: ① 「fail-closed resolver 完備」と記帳しない(便 101 P101-3 末)② 自己参照形の cert には positive fixture B への**手照合記録**を添える ③ 排他違反(規範 11)は人手照合で見る。**この項が閉じる条件** = v2 の実走結果と負例発火表が本欄に入り、**Sol が再検収で PASS を出すこと**(便 101 P101-3 (2)(3)(4) の充足)。→ **着地・司令塔記入(裁定 431/433)**: checker v2 = `search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py`(**SHA-256 = `e851f11ace2c50aba72ea0c55317ccbf1047b4f5a86a15f8de5268d765e36c86`**)。**実走結果(司令塔追試込み)**: v4 cert = **PASS(9 参照走査・(vi) 充足)**・`--selftest` = **1 PASS + 9 STOP**(負例発火表: holder 欠落/json_pointer target path 不一致/target bytes 改竄/64-hex 型違反/実入力 cert path 詐称[(vii) 発火]/**nested `superseded_by.sha256_ref` 破壊[(vi) でのみ検出可]**/XOR 併記[(viii) 発火]/current・effective_source 同時偽装[W101-3.3(2) 想定]/plain sha256 型違反)・**旧 v3 は ledger_version drift を fail-open にせず INTEGRITY_STOP**・checker v1 は無破壊(再実走 PASS)。**残 = Sol 再検収(便 102)のみ** |
| **【CL-13】** | **`external_reference` pin の「版」の粒度**(v1.6 §1.5 の教材点から)。Fresse の例は「**同じ番号・同じ著者でも、unitary / 非 unitary という規約の版が違えば射程が違う**」ことを示した。⟹ `external_reference` の必須 4 点に「**言明が要求する構造(unit の有無・係数環・完備化の型など)**」を明示させるべきか、それとも各 reading ノートの逐語 pin に委ねるかは**未決**。**司令塔レビュー + Sol ゲート待ち**(過剰な欄の増設は【CL-8】の実装コスト問題に触れる) |
