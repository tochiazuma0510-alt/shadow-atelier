# HS 発火条件 4 — helper 非共有三レーンの発注設計書(v1.2)

- 起草: 実装担当(短命)・2026-08-04(v1)/ 改版(v1.1・全指摘採択)/ 改版(v1.2・再前哨 条件付きGO・blocking6件+non-blocking4件を反映)
- 委嘱: 司令塔(裁定435「発火条件4の発注設計書を起草せよ」/ falsifier前哨1差戻し「全指摘採択・v1.1へ」/ falsifier再前哨「条件付きGO・C-1〜C-6+D-1〜D-4を反映してv1.2へ」)
- 正本参照: `sol/sol_reply_101_math28.md` P101-1 / `docs/notes/hs_prop7_translation_v1.md` §5.3項目2・§8.3.2〜8.3.4・§8.6・§8.7・§9(**§9 は前版で未読了、本改版で通読**)/ `docs/week1-定義ノート.md` §1.5(語規約W-1〜W-4)・§1.5.3・**§1.5.4(発注書に必記)**・§4較正スイートv2 / `docs/notes/conventions_ledger_v1.md` CV-9・CV-13
- **判読書**: `docs/notes/hsp7_cond4_lanespec_falsifier_v1.md`(反証前哨1=差戻し・再前哨=条件付きGO)。本版は再前哨の blocking 6件(C-1〜C-6)+non-blocking 4件(D-1〜D-4)を全て反映する。**司令塔が本版でC-1〜C-6の充足を機械確認してから発注**(第3の前哨は不要 — 再設計を伴わない修正のため)。
- 本稿は**発注設計書**。実装・実行はしない。

## 変更履歴(v1.1 → v1.2、再前哨 C-1〜C-6・D-1〜D-4)

| # | 変更 | 対応 |
|---|---|---|
| 1 | §1.5.4 警告文5項+適合テストA5-CONVを逐語貼付。各レーンの初手fail-closed検査に指定。定義式が paper 積である旨の注意も転記 | C-1(N-1 較正スイート全体が語規約反転に盲目、への唯一の防波堤) |
| 2 | S-8/NW-P8 の評価領域として m≠0 の小掃引(m値は付録A-2に事前登録)を追加。N₀側は evaluation_mode=word_level_required を明記。Sol異議時のfallback(not_evaluated・本走送り)を明記 | C-2(N-2 m=0固定スコープではS-8が定義上必ず発火する事故、の解消) |
| 3 | Lane P を新規インスタンスに固定(「発火条件2インスタンスの続き」を全箇所から削除) | C-3(transcript経由の恒真化経路を閉じる) |
| 4 | conventions_used を実値記入に変更(evaluation_mode・f_word並び順を含む)。§5.1の「予定値は§1・§4が既にその内容」という虚偽記述を削除 | C-4 |
| 5 | h₃代表元(負例)と候補鍵リストを発注時点の値で確定記載 | C-5 |
| 6 | NW-P7 着手 = 付録A-1(NW(5)票)の司令塔によるversioned発効後、という順序ゲートを明記 | C-6 |
| 7 | stop_rulesを正本§9.4のjsoncで逐語収載(S-6/S-7'/S-8)+S-9/S-3を同形式で追加 | D-1 |
| 8 | worktree隔離の実操作(作成→当該ディレクトリ削除→削除後一覧をcertに束縛)を明記 | D-2 |
| 9 | Lane Σ: 判定する/しないの矛盾解消・自己較正fixture(全一致/1鍵不一致)・実行隔離・falsifier提出物への登載 | D-3 |
| 10 | §10に非承認スタンプ+「Sol認可を便で得てから」に訂正+誤字(hexaogn)修正+§1図に主検問追記+§8 Lane V出典をpinへ差替(委譲文削除) | D-4 |
| 11 | R-19: 司令塔pin(定義ノートL160-161・(3.3)(3.4)逐語)を正式採用。rider3点(W-1〜W-4・evaluation_mode・§1.5.4必記)を同時記載 | R-19 |
| 12 | ★司令塔レビュー修正(発注前機械確認・裁定453): §1 Lane P の継承範囲「stage1-3」→「stage1-2」(v1.1残骸。§2表・§2.5・§3・§8はstage1-2で一貫しており、stage3はP/Q両側pc構築setupを含むため表側が正) | 充足確認 |

---

## 0. 位置づけと認可境界

`hs_prop7_translation_v1.md` §8.6 の HS本走・発火前チェックリスト(5条)は不変(v1.1 §0 参照・省略)。条件4(helper非共有三レーン)が本稿の主題。

### 0.1 二段ゲート(R-1、不変)+ 順序ゲート(★ C-6 新設)

> **本lanespecが発注するのは「レーン構築 + 較正走」までである。窓NW(7)内の悉皆列挙(候補705,894対)は「本走」であり§10へ隔離、本稿の認可範囲に含まれない。**

較正走の中身(確定): dummy family(h₄ᵗ, t=0..6, NW-P6)+ 𝔥₃負例(C-5で確定)+ NW-P8のm小掃引(C-2、付録A-2)+ ★ **NW-P7(p=5 control, 付録A-1)は下記の順序ゲートの下でのみ着手可**。

> ★★ **C-6 順序ゲート**: NW-P7 の着手は **付録A-1(NW(5)登録票)が司令塔によりversioned発効された後**に限る。**発効行為(=着手可の判定)は司令塔が発注時に行う** — 本lanespec自体は発効を行わない(付録A-1が既に「着手前に確認を要する」と自己申告している草案であることの帰結)。発効前に Lane P が NW-P7 に着手した場合、それは P101-1 (1)「別素数を混ぜない」の違反として扱う。

### 0.2 ★★ C-1: 実装者への警告文+適合テスト A5-CONV(発注書に必記・全レーン共通の初手fail-closed検査)

`docs/week1-定義ノート.md` §1.5.4 は「発注書に必記」と明示している。本lanespecは発注書である。以下、**逐語貼付**する。

> #### ⚠ 警告(workorder に貼る文面・§1.5.4 逐語)
> **語の掛け算の向きを自分で決めてはならない。** 規約 W-1〜W-4 に従うこと。
> 1. **GAP で置換・行列を扱うときは、paper 語 "AB" が `B*A` になる**($i^{B*A} = (i^B)^A$)。逆順に掛けると補題 W1 の形($\iota$ + 逆元)の誤りが入る。
> 2. **hexagon の判定式の積も paper 積である**(W-4)。$(sf)^2 = 1$ は GAP では `(f*s)^2 = One(P)`。
> 3. **可換な商・単一生成元の冪・空語では規約バグが見えない。**「小さい対象で通ったから正しい」は**根拠にならない**。**「値が対合だから安全」も根拠にならない**(§1.5.3(c) の反例)。
> 4. **証明書の `f_word` を書き出す実装と読み込む実装が別なら、必ず適合テストを先に通す**こと。
> 5. 規約を変更したくなったら、**変更せずに司令塔へ差し戻す**(全証明書のハッシュが変わるため)。

> #### 適合テスト A5-CONV(**全実装必須**・§1.5.4 逐語)
> $A_5$ を fixture に使う(`certificates/A1.v2.json` の marking をそのまま採る)。
> $$ t = (1\,2\,3),\quad a = (1\,4\,5),\quad X = a t^{-1} = (1\,3\,2\,4\,5),\quad Y = tXt^{-1} = (1\,3\,4\,5\,2),\quad s = tX^3 = (1\,4)(3\,5). $$
> **主判定(3 行・便 09 F10 合格)**: paper 語 $\;y\,x^{-1}\;$ を評価して
> $$ \mathrm{ev}(y x^{-1}) = (1\,2\,4) \quad(\text{GAP では } \texttt{X\^{}-1 * Y}) $$
> を得ること。**$(2\,5\,3)$ が出たら規約が逆**である(それは $\mathrm{ev}^{\rm bad}$ の値)。
>
> 補助判定(20語のhexagon一致率)は node単系統fixtureであり、本lanespecでは**任意**(必須項目に含めない、falsifier再前哨の申告どおり)。

> ★ **貼るときの注意(再前哨が数値で捕獲・正本§1.5.4の記述上の穴)**: 定義式 $X=at^{-1}$、$Y=tXt^{-1}$、$s=tX^3$ は **paper積**であり、GAPに**そのまま打つと違う置換になる**。実測: GAPで `a*t^-1` は $(1\,4\,5\,3\,2)$(正本の $X$ ではない)、`t^-1*a` が $(1\,3\,2\,4\,5)$ = 正本の $X$。同様に `t*X^3` は $(1\,5)(2\,4)$、正本の $s=(1\,4)(3\,5)$ は `X^3*t`。**定義式も W-1 で反転して打つこと**を各レーンのdriverにコメントで明記する。literal に打つと $X^{-1}Y=(2\,4\,3)$ という第三の値が出て fixture 自体は自己検出するが、実装者が理由が分からず迷うため。

> **主検問済み**(falsifier再前哨が独立に数値検証): GAP右作用 $i^{(A*B)}=(i^A)^B$ で、正本の値 $X=(1\,3\,2\,4\,5)$, $Y=(1\,3\,4\,5\,2)$ を取ると $X^{-1}*Y=(1\,2\,4)$(正本の正しい規約の値・一致)・$Y*X^{-1}=(2\,5\,3)$(規約が逆の値・一致)。**⟹ A5-CONVは健全かつ識別力を持つ**(N-1で示された較正スイート全体の規約反転盲目性に対する唯一の外部anchor)。

> **運用**: 各レーンの driver は**最初に**A5-CONVを走らせ、`conventions_used.a5_conv_result`("correct"|"reversed"|"other")に値を記録する。`"correct"` 以外なら**fail-closedで停止し、cert を出さない**(以降の較正走の結果を一切生成しない)。

---

## 1. 三レーンの定義(較正走の範囲に限定)

### Lane S(探索・Search)

- **0手目(全レーン共通)**: A5-CONV(§0.2)。
- **入力**: 窓定義NW(7)(`hs_prop7_translation_v1.md` §8.7.3)。
- **やること**: exact pc presentation of P = F₂/(γ₅(F₂)F₂⁷) を自前で構築(stage1-4非継承、§2/§3)。簡約hexagon **(3.10)(3.11)** で dummy family(m=0, f̄=h₄ᵗ, t=0..6)・𝔥₃負例(C-5で確定、下記)を判定。**悉皆列挙は行わない**(§10)。
- **出力**: PASS/FAIL/UNKNOWNの三値(§6)。
- **やらないこと**: full B₃/N上の(3.3)(3.4)は評価しない。K(0,5)/Wに触れない。全候補列挙。

### Lane V(検証・Verify)

- **0手目**: A5-CONV。
- **入力**: 窓定義NW(7)・control窓N₀(NW-P8用)を自前で構築。Lane Sのcertから候補値(m,x-y語)のみ受領。
- **やること**:
  1. dummy family・𝔥₃負例について、**full B₃/N**上で**(3.3)(3.4)**(★ R-19 pin・下記§1.5参照)を評価し独立再判定。
  2. **Lane Sの全申告(PASS/FAIL両方)に対して独立判定**(R-8)。4区分表(PASS/PASS, FAIL/FAIL, PASS/FAIL, FAIL/PASS)をcertに残す。
  3. ★ **C-2: NW-P8のm小掃引**を担当(付録A-2)。N₀窓では **`evaluation_mode = word_level_required`**(下記§1.5・rider②)を用いる — θ/τを自由群の語レベルで適用してからφで評価する(c∉N₀ゆえ商上の近道が壊れる、`hs_prop7_translation_v1.md` §2の2026-07-25注記)。N窓では`quotient_ok`でよい。
- **出力**: 候補ごとのPASS/FAIL/UNKNOWN(N・N₀両方)。Lane Sとの4区分突合表。NW-P8のm小掃引結果(§4.2で詳述、既定は「存在主張」であり `CALIBRATION_FAILED` の暫定発火はscope注記つき)。
- **やらないこと**: K(0,5)/Wに触れない。Lane Sの中間コードを読まない。

### Lane P(pentagon・PENT)

- **0手目**: A5-CONV。
- **著者**: ★★ **C-3: 新規インスタンス固定**(「発火条件2インスタンスの続き」は不採用。継承はファイルのみ、著者は他2レーン同様すべて新規、§2/§3/§8)。
- **入力**: 窓定義NW(7)。Lane S/Vのcertから候補値(x,y語のみ)。
- **やること**: K(0,5)/W(W=γ₅(K(0,5))K(0,5)⁷)上で
  \[ \mathrm{PENT}_W([m,\bar f]) \iff \bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\bar f=1 \ \text{in}\ Q,\qquad \bar f:=j(f)W\in Q,\ j(x)=x_{12},\ j(y)=x_{23} \]
  K(0,5)の構成は**stage1-2のみ継承**(stage3-4は継承禁止、§2/§3。★司令塔修正 2026-08-04: 本行は v1.1 残骸で「stage1-3」とあったが、stage3_gen_setup.g は P/Q 両側の pc 商構築 setup を含み「K(0,5) の構成のみ」を超えるため、§2 表・§2.5 手順 5・§3・§8 と同じ stage1-2 に統一)。
- **出力**: NW-P6(h₄ᵗ family, t=0..6)・NW-P7(付録A-1発効後のみ、p=5 control, t=0..4)・NW-P8のPENT側該当欄・𝔥₃負例のPENT(UNKNOWNでよい、§8.3.3はhexagon側の非exactさのみを述べる)。
- **やらないこと**: hexagon判定はしない。B₃/N側の(3.3)(3.4)を再評価しない。ρ/N_ρの評価コードをstage4から流用しない(新規実装)。

### interface図(★ D-4: CV-9主検問を追記)

```
   NW(7)/NW(5)/N0 の紙の定義(SS8.7・定義ノートSS1.5・SS2)
           |         |         |
      SS5 CV-9 主検問(発注前・仕様同一性の判読)
           |         |         |
      (各レーンが独自に P/B3N,B3N0/K05W を実装。0手目=A5-CONV)
           |         |         |
       [Lane S]  [Lane V]  [Lane P]
           |         |         |
   candidates(x,y語のみ) --> Lane V が全候補を独立判定(R-8)+ m小掃引(C-2)
           |                     |
   candidates(x,y語のみ) --------------------> Lane P が PENT 判定
                                               |
                                    Lane Σ: 機械合成スクリプト(SS7)
                                               |
                            CV-9 副検問(3cert+集約certの事後整合性確認)
```

Lane間を流れるのは候補の値(m の整数値・f を x,y の語で表した文字列。正規形不可、R-4a)のみ。

### ★ R-19 rider ①: 語の並び順の規約(W-3)

正本 **規約W-3**: 「証明書 `f_word=[[letter,exponent],…]` は**paper語の順序**で並べる。読み手は必ずW-2の手続きで評価する。**書き手と読み手が別実装のときは§1.5.4の適合テストを先に通すこと。**」本件は書き手1(Lane S)・読み手2(Lane V, Lane P)の三実装であり、A5-CONV(§0.2)がまさにこの要求への対応である。`conventions_used.f_word_order = "paper"` を全レーンのcertに明記する(C-4)。

---

## 2. import 禁止境界

| 対象 | Lane S | Lane V | Lane P |
|---|---|---|---|
| `hs_prop7_translation_v1.md`(§8.7・§9)・`docs/week1-定義ノート.md`(§1.5・(3.3)(3.4)) | ○ | ○ | ○ |
| `sol/sol_reply_101_math28.md`・`sol/sol_reply_100_math27.md`(W100-1.4正本) | ○ | ○ | ○ |
| 他レーンのdriverスクリプト本体・GAPセッション内オブジェクト | ✗ | ✗ | ✗ |
| 他レーンのcert(候補の値のみ) | (該当なし) | ○値のみ | ○値のみ |
| `search/probe/hsp7_gap_v1/stage1_pb4.g`・`stage2_k05.g`(K(0,5)構成) | ✗ | ✗ | ○ **継承可**(§3) |
| `stage3_gen_setup.g`(バッチ生成**コード**) | ✗ | ✗ | ✗(手順の文章記述=付録Bのみ共有) |
| `stage4_eval.g`(ρ/N_ρ評価コード) | ✗ | ✗ | ✗(R-6・NW-P6恒真化防止のため全レーン禁止) |
| `search/probe/hsp7_v1/*.py`(Lie環側検算) | ✗ | ✗ | ✗ |
| GAP共通utility・ANUPQ SetupFile**手順**(付録B) | ○ | ○ | ○ |

### ★ D-2: worktree隔離の実操作(R-9の完成)

自己申告boolean(`imports_forbidden_check`)は補助情報に留め、判定根拠は次の**物理事実**とする:

1. Lane S・Lane V の実装インスタンスに対し、`Agent(isolation: "worktree")` で新規worktreeを作成する。
2. worktree作成**直後**に `search/probe/hsp7_gap_v1/`(stage資産)を**削除**する(`rm -rf`)。
3. 削除後のディレクトリ一覧(`ls search/probe/` の出力・当該パスが存在しないことを示す)を**cert の `execution_isolation.post_delete_listing` に束縛**する(digest付き)。
4. driver は削除後の状態で実行し、実行ログにタイムスタンプを残す(削除→実行の順序が事後に検証できるように)。
5. Lane P は stage1-3のみを残した縮小コピー(stage3のコードは§2表により禁止なので、実際にはstage1-2のみ残す縮小worktree)で実行する。

---

## 3. 既存stage1-4資産の継承先 — Lane Pにstage1-2のみ限定継承

★ **C-3反映**: 継承可否はファイル単位(stage1_pb4.g・stage2_k05.gのみ)であり、**著者の連続性は一切認めない**(v1.1にあった「発火条件2インスタンスの続き」という選択肢を削除)。継続インスタンスはstage4のロジックを文脈に保持しているためファイル禁止だけでは恒真化経路を塞げない、というR-6残課題への対応。Lane Pの起草者は他2レーン同様、**新規インスタンス**とする。

継承しないもの(stage3のコード・stage4全体)、理由(P構築の要件化・CV-9観点・fail-closedアンカーの再利用理由・較正アンカーの二相利用)は v1.1 §3 の内容を維持(著者連続性の記述のみ削除)。

---

## 4. NW-P6/P7/P8・S-6/S-7′/S-8/S-9/S-3・DUM-1/p family・負例 の担当割り当て

### 4.1 NW-P6/P7

| 項目 | 担当 | 内容 |
|---|---|---|
| **NW-P6**(h₄ᵗ family, t=0..6) | Lane P(新規実装) | cond2既測値からの代数的系(コード整合性の較正、新規の数学的発見ではないと明記) |
| **NW-P7**(p=5 control) | Lane P | ★ **C-6順序ゲート必須**(付録A-1発効後のみ着手)。予言=「5元すべてPENT PASS」(正本どおり、v1.1のR-5修理を維持) |

### 4.2 ★★ C-2: NW-P8/S-8 のスコープ確定(N-2への対応)

**問題(再前哨N-2)**: 較正走の候補がm=0固定の家族のみだと、c^m=c^0=1となりNとN₀の差が原理的に現れず、S-8(不一致0件で`CALIBRATION_FAILED`)が着手した瞬間に発火する設計になっていた。

**司令塔裁定(採用)**: 較正走に **m∈𝒳_N の小掃引** を追加する。

> #### NW-P8 較正走スコープ(付録A-2に事前登録・m値集合を確定)
> - **候補**: m ∈ {1, 2, 4, 5, 6}(= 𝒳_N \ {0, 3}。𝒳_N = {m mod 7 : gcd(2m+1,7)=1} = {0,1,2,4,5,6}、m=0はdummy familyで既出のため除外、m=3はgcd(7,7)=7≠1で𝒳_N外)。各mについて **f̄ = 1**(自明charming元、[P,P]に自明に属す)固定。**family外の探索はしない**(司令塔裁定)。
> - **評価**: Lane V が full (3.3)(3.4) を N・N₀ 両窓で評価し、5件の (N判定, N₀判定) 対を得る。
> - **N₀側の評価様式**: ★ **`evaluation_mode = word_level_required`**(c∉N₀、rider②)。θ/τは自由群の語レベルで適用してからφで評価する。
> - **予言**: 「5件のうち少なくとも1件でN・N₀の判定が食い違う」(**存在主張のみ**。どのmで食い違うかは事前登録しない=探索結果として報告、v1.1のR-14と同じ理由 — 予言に混ぜて後から件数を予言だったことにできないようにする)。
> - **この小掃引の位置づけ**: ★ **正本§9.3のS-8(𝒳_N**全体**を掃いたうえで判定)の縮小scope版**である。全候補(f̄も含めた悉皆)を掃く本来のS-8は§10の本走に属する。本節の小掃引は「N₀が実際にNと異なる挙動をしうる窓であること」を安価に確認する**先行指標**であり、これ単体でS-8を`PASS`扱いにしない(下記verdict規約)。
> - **verdict規約**: 5件全てが一致(不一致0件)なら、cert の `stop_rules.S8` は `"fired": true, "scope": "reduced(m-sweep only)", "note": "縮小scopeでの不一致0件。正本§9.3の完全なS-8(全X_N x 全候補)は未評価。本走(SS10)へ持ち越し。CALIBRATION_FAILEDとして直ちに較正走全体を止めるかは司令塔判断"`。1件以上不一致があれば `"fired": false, "scope": "reduced(m-sweep only)"` とし、正の較正指標として記録。**縮小scopeでの発火は較正走全体の即時停止を自動的には意味しない**(正本のS-8は全数を要求するため、縮小scopeでの発火は「情報不足」の表明であって「証明された較正失敗」ではない)。
> - **Sol異議時のfallback**: もしSolが便102で本スコープ限定に異議を出せば、S-8は `"fired": "not_evaluated", "note": "Sol異議によりNW-P8評価を全数悉皆(SS10本走)まで延期"` に置き換え、当該較正走からNW-P8の実質評価を完全に外す。**この分岐をLane Vのdriver設計に事前に組み込んでおく**(条件フラグで両モードを切替可能にする)。

---

## 5. CV-9 主検問の位置(不変・R-2/R-3)

台帳§1.3.1のCV-9-1(主検問=計算前)・CV-9-4(差戻し規律)に従い、**仕様凍結→主検問→発注→副検問→(差戻しなら主検問へ戻る)**の順を守る(v1.1 §5内容を維持)。

★ **C-4反映**: 主検問が読む対象は本稿§1・§4・§6の**実値**(conventions_used等のplaceholderではない具体的な値)である。「本稿の§1・§4が既にその内容」という誘導的な記述はここでは行わない — 主検問担当者は本稿全文を実際に読んで判定すること。

---

## 6. 各レーンのcert様式

### ★ C-4: conventions_used を実値で記入する

cert骨格の`conventions_used`は**placeholderのまま発注しない**。以下、各レーン共通で埋めるべき実値の例(実装時にレーンごとの具体的な選択を確定させて記入):

```jsonc
"conventions_used": {
  "ledger_version": "conventions_ledger_v1_6",   // 実行時点の生きた台帳を都度確認
  "commutator_convention": "Comm(a,b):=a^-1 b^-1 a b (GAP native, 左正規化)",
  "generator_symbols_and_order": "x=F.1, y=F.2 (P側) / X12,X13,X14,X23,X24,X34 (K(0,5)側, stage1由来)",
  "theta_tau_rho_orientation": "theta: x<->y, tau: x->y->z->x (z=(xy)^-1), rho: T1->T4->T2->T5->T3->T1 (SS8.7 逐語)",
  "j_image": "j(x)=x12, j(y)=x23 (Lane Pのみ)",
  "f_word_order": "paper (W-3)",                  // R-19 rider1
  "a5_conv_result": "correct",                    // C-1, 0手目の実測値
  "evaluation_mode": {"N": "quotient_ok", "N0": "word_level_required"},  // R-19 rider2, Lane Vのみ必須
  "sphere_row_relation": "ker p_i 行積=1, j昇順 (Lane Pのみ)",
  "K05_eq_PB4_mod_center": "K(0,5)=PB4/<Delta4^2> (Lane Pのみ)"
}
```

各レーンは上記の**実測値**(placeholderでない)をcertに書く。

### stop_rules: 正本§9.4を逐語収載+S-9/S-3を同形式で追加(★ D-1)

```jsonc
"stop_rules": {
  "S-6":  { "trigger": "NW-P3 または NW-P5 が偽",
            "verdict": "TARGET_PREMISE_BROKEN / STOP",
            "note":    "p=7 本走を止める。p=11,13 への移送判断は司令塔" },
  "S-7'": { "trigger": "NW-P2 の 4 欄(|P|,|[P,P]|,N_ord,|X_N|)のいずれかが不一致",
            "verdict": "PREREGISTRATION_FALSIFIED / INTEGRITY_STOP",
            "note":    "即時停止・部分結果は保存・同一 run/同一登録内で予言を書き換えない・構成 bug と数学予言の偽を別検分・続きは別 version 事前登録から" },
  "S-8":  { "trigger": "X_N 全掃引で N と N_0 の hexagon 判定の不一致が 0 件",
            "verdict": "CALIBRATION_FAILED / INTEGRITY_STOP",
            "note":    "NW-P8 は較正予想。後から期待値を弱めない。★本較正走では SS4.2 の縮小scope(m-sweepのみ)で評価し、正本の完全形とは区別して記録する" },
  "S-9":  { "trigger": "同一窓 N 上で Lane S と Lane V の項目別判定(候補ごとPASS/FAIL/UNKNOWN)が1件でも食い違う",
            "verdict": "LANE_DISAGREEMENT / INTEGRITY_STOP",
            "note":    "多数決・片方優先の自動解決をしない。3レーン全体のcert発行を停止し人手切り分けまで前進しない。N0側(S-8)とは比較対象が異なり競合しない(SS4参照)" },
  "S-3":  { "trigger": "NW-P7(p=5 control family, 付録A-1発効後)が5元中5元PASSにならない",
            "verdict": "IMPLEMENTATION_BUG_SUSPECTED / STOP",
            "note":    "実装バグと判定して較正走を止める(SS8.3.4のfamily限定読み替え版)" }
},
"prediction_source": { "frozen_at": "<本ノート該当節のdigest>", "codegen_uses_expected_values": false }
```

### ★ C-5: h₃負例と候補鍵リストを発注時点の値で確定

- **h₃代表元(負例fixture)**: `hs_prop7_translation_v1.md` §8.3.3 の𝔥₃=u₁+u₂に対応する群語として **h₃ := [[x,y],x] · [[x,y],y]**(定義DUM-FINと同じ左正規化交換子の積、Lieの和を群の積に翻訳)を確定採用する。族は h₃ᵘ(u=0のみ、単一代表元 — 𝔥₃は「hexagonがexactに成立しない」ことを示すための1点fixtureであり、familyを持つ必要はない、DUM-1/pのようなt-parametrized familyとは性格が異なる)。
- **較正走の候補鍵リスト(全体・事前登録)**:
  1. dummy family: `(m=0, f=h4^t)` for t∈{0,1,2,3,4,5,6}(7件)
  2. 負例: `(m=0, f=h3)`(1件)
  3. NW-P8 m-sweep: `(m, f=1)` for m∈{1,2,4,5,6}(5件、N窓・N₀窓それぞれで評価するので実質10評価)
  4. NW-P7(付録A-1発効後のみ): `(m=0, f=h4^t)` for t∈{0,1,2,3,4}(NW(5)宇宙、5件)
- 合計、較正走の候補は **13件(NW-P7除く)+ 5件(NW-P7、発効後)= 18件**。§9の予算表と整合させること。
- Lane Sの鍵漏れ検出機構は「事前登録された候補リストとの突合」である(上記リストそのもの)。R-8の「UNKNOWN側で検出できる」という記述は不正確だった(Lane Sが鍵を一切出さなければLane Vは気付けない)ため、この事前登録リストを実際の検出機構として明記する。

### ★ R-20: `candidates_in`自身のdigest(不変・維持)

```jsonc
"candidates_in": [...他レーンから受け取った値のみ(x,y語)...],
"candidates_in_source_cert_sha256": "...",
"candidates_in_own_digest_sha256": "..."   // 自分が実際に読み込んだ値列そのもののdigest
```

### execution_isolation(★ D-2反映)

```jsonc
"execution_isolation": {
  "worktree_created": true,
  "stage_dir_deleted_before_run": true,
  "post_delete_listing": "<ls search/probe/ の出力テキスト>",
  "post_delete_listing_sha256": "..."
}
```

### UNKNOWN の置き場(R-13、不変)

`lane_specific_results` の各候補の値はPASS/FAIL/UNKNOWNの三値。UNKNOWNの理由(timeout/pc群評価失敗/代表元取り直し要)を併記。

---

## 7. 司令塔突合の手順 — Lane Σ(★ D-3で4点修正)

1. Lane Σ(3レーンとは別著者・cert[JSON値]のみ読み driverコードは読まない・実行隔離もworktree、D-3③)が3cert(+Lane VのN₀内訳)を入力に機械合成する。
2. ★ **D-3①「判定する/しない」の矛盾を解消**: Lane Σは**新たな判定基準を作らない**。S-9(候補ごとの一致/不一致)・S-8(N vs N₀の不一致件数)は本lanespecの§4.2・§6で**事前確定済みの述語**であり、Lane Σはそれを**機械的に評価するのみ**(選択の自由を持たない)。出力の集約cert(`hsp7_cond4_summary_YYYYMMDD.json`)は「新たな判定を行わない」のではなく「**本稿が既に定めた述語を適用した結果を転記する**」ものである(この言い換えで矛盾を解消する)。
3. ★ **D-3② Lane Σの自己較正fixture**: 合成cert 2組を用意する。①全候補で(Lane S判定, Lane V判定)が一致するfixture cert組 → Lane Σは`LANE_DISAGREEMENT`を発火しないことを確認。②ちょうど1鍵だけ不一致のfixture cert組 → Lane Σは`LANE_DISAGREEMENT`を発火することを確認。この2件をLane Σ自身のcertに`self_calibration`欄として記録する。
4. ★ **D-3④** falsifierへの提出物一覧(§8末)にLane Σのdriver+cert+自己較正fixtureの結果を追加する。
5. 完全性主張は選択肢(iii)を採用(較正走の範囲では「Lane Sの判定(候補ごと)はLane Vと二系統で一致する」までしか書かない、悉皆列挙時=§10で改めて選び直す)。
6. 集約certをfalsifierへ提出し副検問(§5)を受ける。ここで初めてcross-checkedを名乗れる。

---

## 8. CV-9 判読に耐える独立性 — 著者・helper・規約の分離表

| | Lane S | Lane V | Lane P |
|---|---|---|---|
| **起草者** | 新規インスタンス#1(worktree隔離) | 新規インスタンス#2 | ★ **新規インスタンス#3**(C-3: 「発火条件2インスタンスの続き」は不採用。継承はstage1-2ファイルのみ) |
| **数学的定義の出典** | §8.7(簡約hexagon(3.10)(3.11)) | ★★ **R-19採用: `docs/week1-定義ノート.md` L160-161(司令塔pin、【画像照合済】)の(3.3)(3.4)逐語 + 同ブロックの実装注(§2、2026-07-25)**。「次版で式番号を確認」という実装者への委譲文は**削除**(主検問が殺すべき仕様曖昧さのため) | §1.2-1.3(PENT-NORM)・§8.7.3(sphere row-product辞書) |
| **GAP構築** | Lane S独自(Pのみ) | Lane V独自(B₃/N・B₃/N₀) | stage1-2継承(K(0,5)構成のみ)。stage3-4は継承禁止 |
| **停止規則の実装者** | driver内(S-7′部分) | driver内(S-7′+S-8+m-sweep) | driver内(S-7′+S-3) |
| **falsifier提出物** | driver+cert+run log+imports_declared+worktree削除痕跡 | 同左 | 同左 |

★ **Lane Σ の falsifier 提出物**(D-3④・上表に無い第4の主体として別掲): driver+集約cert(`hsp7_cond4_summary_YYYYMMDD.json`)+自己較正fixture結果(全一致/1鍵不一致の2組とその判定結果)。

### R-19 rider ②: evaluation_mode(不変・§1で既述、再掲)

`hs_prop7_translation_v1.md` §2 の実装注: 「θ/τを商F₂/N_F₂上の準同型として評価する近道はN_F₂のθ,τ-不変性を要し、これはbraid共役のc-因子が消えること(**c∈N**)に依存する。c∉Nの対象では近道が壊れる…θ/τは自由群の**語レベル**で適用してからφで評価すること。」定義ノート§1.5.3の表はこれを`evaluation_mode=word_level_required`(c∉N)=「規約が決定的に効く唯一の経路」と分類する。**N₀はまさにc∉N₀** ⟹ S-8/NW-P8の評価はこの最も規約敏感な経路の上に乗る。`conventions_used.evaluation_mode`必須欄(§6)。

### R-19 rider ③: §1.5.4は発注書に必記(§0.2で既に履行)

判読可能な軸(生成元記号・交換子規約・向き・jの像・serialization)はv1.1 §8のR-17対応を維持(表は上記に統合)。CV-13(外部anchor必須)への言及もv1.1同様維持: 3レーンとも同じ一次資料から向きを取るため3レーン一致自体はCV-13の外部anchorにならない。**A5-CONV(§0.2)こそがCV-13の要求する外部anchor/独立source-map routeである**(N-1の修理そのものがCV-13充足でもある)。

**CV-9判読でfalsifierが確認すべき核心**(不変): (1)3レーンが別セッションで書かれ相互import無し(worktree隔離+削除痕跡で裏取り、D-2) (2)`imports_declared`が§2禁止表と矛盾しない (3)3レーンの判定が独立導出でありながら一致することが「同じ間違いの3回コピー」でない(CV-13対応=A5-CONV結果の確認を含む)。

---

## 9. 計算量予算・撤退条件

| 量 | 値 | 効く先 | cap/撤退 |
|---|---|---|---|
| \|P\| | 5,764,801=7⁸ | Lane S/V pc群構築 | GAP `-o 2g`(既定cap) |
| 較正走候補数(NW-P7除く) | **13件**(§6 C-5のリスト) | Lane S/V/Pの判定ループ | 数十秒オーダー、cap目安600秒 |
| NW-P7候補数(発効後) | **5件** | Lane P(NW(5)) | 同上 |
| \|Q\| | 7⁴⁰≈6.37×10³² | Lane P pc群構築(stage1-2継承) | cond2で完走実績あり(pq batch数十ms) |
| Lane S の候補件数(悉皆列挙時) | 705,894(6×117,649) | 本走(§10)のみ | 較正走の発注には含めない |

Lane Sの較正走候補数(13件)は**予言ではなく事前登録された固定リスト**(§6 C-5)である。

---

## 10. ★★ 認可外・別章隔離: 「本走」(★ D-4反映)

> ★★ **本章は再前哨の審査対象外であり、前哨通過は本章の内容に対するいかなる承認も与えない。**

本節は**発注しない**。

- **対象**: NW(7)の窓P内の全charming candidate(6×117,649=705,894対)の悉皆列挙+3レーンでのhexagon/PENTの全数判定。
- **現状**: `hs_prop7_translation_v1.md` §7.1格付け表・P101-1末尾の「shadow全掃引は許可しない」に照らし未認可。
- **前提条件**(発注前に要確定): (a)「窓内悉皆列挙」がP101-1の言う「shadow全掃引」に該当するか一行確定(W101-6の読みの割れを解消)。(b) §9の計算量予算を本走の規模(70万対)向けに再設計。(c) §7の完全性主張の扱いを(i)(ii)(iii)から選び直す。加えて (d) 較正スイートv2項目3(source kernel証明書=「個数一致・指数一致では不足」)は完全性主張の際に必ず戻る論点なので明記しておく。
- ★★ **(a)〜(d)の確定・および本章の発注自体は、司令塔単独では行えない — P101-1はSolの認可文であり、認可拡大はSolの専権である。「Sol の認可を便で得てから」着手すること**(v1.1の「将来 P101-1 の認可拡大(司令塔/Sol)を得てから」という記述は不正確であり本版で訂正した)。

---

## 付録 A-1. NW(5) 事前登録票(草案・NW-P7 用)

★ 本票は草案であり、司令塔によるversioned発効(§0.1 C-6)を経るまでLane Pは着手しない。

| 項目 | 内容 |
|---|---|
| **宇宙ID** | NW(5)(NW(7)とは別version) |
| **窓対** | N=𝒱(F₂)×⟨c⟩, N₀=𝒱(F₂)×⟨c⁵⟩(p=5, e=1) |
| **窓の役割** | control専用。discovery標的ではない |
| **対象family** | h₄ᵗ(t=0..4)。族の大きさ=ord(h₄)=p=5(𝒳_Nの元数=4とは無関係、R-15) |
| **予言** | 「h₄ᵗ family(t=0..4)は5元すべてがPENT PASSする」(ν₄(j𝔥₄)≡0 mod5の直接帰結。「𝔥₄-座標のfiber内分離が死ぬ」はこの予言の説明であり別の弱い言い換えではない) |
| **停止規則** | S-6/S-7′+S-3(§6逐語)。NW(7)側の発火と独立(宇宙が違うので伝播させない) |
| **cert命名** | `search/certs/hsp7_cond4_laneP_p5control_YYYYMMDD.json` |
| **識別力の理由** | NW-P7だけが非自明なPENT PASSを含む事前登録予言である(NW-P6のPASSはt=0=恒等元の1点のみ)。「PENT PASS⟺入力が自明」という誤実装ではNW-P7の5元中5元PASSを再現できない |
| **未決事項** | (a) NW(5)のP/Qをp=7と同じ手順で再構築するか、p=7で構築したK(0,5)のpresentation(pに依存しない)を再利用しp-quotientのみp=5で取り直すか — 後者が自然(Lane P内部の話)。(b) 発効は司令塔/Solの追認を要する |

## 付録 A-2. ★ NW-P8 m小掃引 事前登録票(新設・C-2)

| 項目 | 内容 |
|---|---|
| **宇宙** | NW(7)(N・N₀とも既存の窓対、別宇宙登録は不要) |
| **候補** | m∈{1,2,4,5,6}、各m で f̄=1 固定(5件)。詳細は§4.2 |
| **evaluation_mode** | N: quotient_ok / N₀: word_level_required(R-19 rider②) |
| **予言** | 「5件のうち少なくとも1件でN・N₀の判定が食い違う」(存在主張のみ、どのmかは事前登録しない) |
| **stop rule** | S-8(§6逐語)。ただし本掃引は正本§9.3の完全形(全𝒳_N×全候補)の**縮小scope**であり、縮小scopeでの発火(不一致0件)は較正走の即時停止を自動的には意味しない(§4.2 verdict規約) |
| **Sol異議時のfallback** | S-8を`not_evaluated`とし、NW-P8の実質評価を§10本走まで延期。Lane Vのdriverはこの分岐を切替可能な設計にしておく |

## 付録 B. 環境ノート(全レーン共有可・裁定432/435・falsifier確認済み=裏口として機能しない)

ANUPQの対話iostream(`InputOutputLocalProcess`経由の`PqStart`/`Pq`)はこのWindows/Cygwin GAP 4.16.0環境で`Error, failed to find any more of line (iostream dead?)`により機能しない。回避策として、ANUPQ純正の`SetupFile`オプション(`Pq(G : ..., SetupFile := path)`)でコマンド列をファイルへ書き出し、`pq -i -k -g < setupfile > log`の一方向stdinリダイレクトでpq.exeを実行し、出力`PQ_OUTPUT`(GAP形式2)を`Read()`でそのまま読み込む。この手順はANUPQ自身が生成・読解するものであり自作プロトコルではない。全レーンがこの**手順**を使ってよい(環境事実であり判定ロジックではないためhelper非共有の対象外)。各レーンは自分の窓定義から自分でsetup fileを生成すること(生成済みファイルの使い回しは禁止・`stage3_gen_setup.g`のコード自体も読まない)。

---

以上、実装・実行は行っていない。本版(v1.2)の完成をもって、司令塔がC-1〜C-6の充足を機械確認し、3レーン+Lane Σを発注する(第3の前哨は不要)。
