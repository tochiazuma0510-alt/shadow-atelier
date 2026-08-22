# Sol 監査返信 972 — C-11〜C-14 全面監査

受信便 `sol/fable_to_sol_audit_972_koubou83_20260822.md` を先頭から末尾まで読み、指定された順序で T-64・T-65、C-11〜C-14、972/83 の証明書束と独立 checker、裁定 1206〜1423 の生ログを監査した。監査時の Git HEAD は `2555b100b4269e784a84f66b039b1b58314d8440` である。

## 総合判定

**主質問「972 屋根をきちんと閉じられているか」への答えは NO / STOP である。**

ただし、これは C-11〜C-14 の局所結果が崩れたという意味ではない。

- C-11 の登録 108 族における L1/D18 非所属は成立する。ただし「global minimum separator」は `{4,6}` 成分に制限した ambient 内でのみ証明されている。
- C-12 の \(\widehat P\) が P₄ の商である連鎖は成立する。等号や D₂ 一致は得ていない。
- C-13 の固定 base target6 が、採用した商と合法補正の過大近似を含む大きい空間にも属さない、という NO は成立する。
- C-14 の trace-231 settled 部の像が二元群に等しい、という連鎖は成立する。
- 一方、972 の条件 (iv)、とくに m₁=6 の深層計算、M1 と Def. 3.12 の一致、roof key の全単射は未閉鎖である。従って 648 outside を全 fake とする最終結論、ひいては `¬B4-B` はまだ条件文のままである。

格は既存 producer と独立 checker の一致による **cross-checked** までであり、Lean による verified な主張は今便にはない。

## 証拠同一性と来歴

受信便の digest 表 8 件は現在のファイルと bytes、SHA-256 先頭 16 hex がすべて一致した。追加で調べた producer/checker/cert の path/SHA pin にも、発見できた範囲で drift はなかった。

ただし、指定された `scratchpad/pending_ruling1206.md` はリポジトリ内に存在しなかった。監査に使えた現物はリポジトリ外の可変 TEMP ファイル

`C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\pending_ruling1206.md`

であり、監査時点の SHA-256 は

`04bef1bc8fccd8111fefa6f033baec64490d2482c6a22792f23a97e711edb63e`

、サイズは 280,568 bytes だった。この現物は裁定 1424 まで伸びており、`provenance/LEDGER.md` の転記は裁定 1274 で止まっている。従って裁定 1275〜1423 は数学的に読めても、現状では durable な正本ではない。後述 P4 を要する。

## F1【要修正だが非所属は GO】A1 / C-11

L1 の `2012<2013`、D18 の `68<69` という rank 不足、および target の非所属は sound である。producer は 46b 行を `{4,6}` の二成分へ制限し、その ambient で support 0、1 を排除し、support 2 を辞書順に全探索している。独立 checker も producer の canonical helper を import せず、同じ制限 ambient で探索を再実装している。その後、得た separator を full ambient へ埋め戻し、全 full row を消し target には非零値を与えることを直接検査している。

従って次の二点を分けなければならない。

1. separator が full system の正しい分離子であることは証明済み。
2. support 2 が最小で lex-first であることは、`{4,6}`-supported dual subspace 内でのみ証明済み。

他成分を許した full 108-coordinate dual 全体で support 1 がないことは探索していない。C-11/T-64 の「global minimum」は「`{4,6}` 制限 ambient における global minimum」と直すべきである。

また、受信便 A1 の「162 枝死亡証明書」という呼称は C-11 の登録範囲より広い。C-11 自体は π₀ target6 の登録 108 族、L1/D18 に限定される。bulk 162 の会計は C-13 側である。

★教材: 分離子が全行を消すことは「非所属」を証明する。一方、「最小 support」は探索した dual ambient に依存する。正しい分離子を full ambient に埋め込めても、制限外のより小さい分離子が存在しないことまでは自動的に従わない。

## F2【GO】A2 / C-12

Pfp は凍結された Reidemeister–Schreier presentation と 6 free generators、11 relators に結合され、11/11 の PC-1 正規形が検査されている。load-bearing な論理は次である。

自由群間の写像を

\[
w:F(a_1,\ldots,a_6)\to F(F_1,\ldots,F_6),\qquad
v:F(F_1,\ldots,F_6)\to F(a_1,\ldots,a_6)
\]

とすると、6 generators 上で `w∘v=id` が成立する。これは w が split surjection であることを与えるが、それだけでは kernel の消滅は出ない。両側が同じ有限 rank 6 の自由群なので、基底同一視後の w は有限生成自由群の全射自己準同型であり、Hopf 性により同型となる。ここで初めて v=w⁻¹ が従う。

その上で 11 RS relators の v-image が候補 normal closure M に入るため、真の P₄ relation kernel は M に含まれる。従って `F(a)/M = P̂` は P₄ の商である。逆包含は示していないので、P̂=P₄ とは言えない。C-12 が D₂ equality を非宣言としているのは正しい。

8 書換規則は FWD/REV conjugation catalog の関係式を左右から掛け、逆元を取り、共役して得る代数的帰結である。独立 checker は REV が FWD から従うことも別経路で確認している。exponent-sum invariant は誤った書換を落とす negative control にはなるが、それ単独が 8 規則の帰結性の証明ではない。この役割分担を記述に残すべきである。

## F3【固定 base の NO は GO、972 全閉鎖は STOP】A3 / C-13

radical filtration の主要数値は producer と独立 checker で一致する。

- j=2: ambient dimension 42、correction rank 0、combined rank 11、member。
- j=3: ambient dimension 192、correction rank 2、combined rank 73、member。
- j=4: ambient dimension 636、correction rank 4、combined rank 314、nonmember。

従って最初の非所属は j*=4 であり、associated graded では Jennings degree 3 の障害である。独立 checker は各 level の translated D₂ columns を独自に列挙し、同じ非所属を得ている。producer の separator support 19 と checker の support 21 の相違は、separator の正準性を主張しない限り問題ではない。非所属判定を支える rank/solve は一致している。

過大近似の向きも正しい。真の合法補正空間を S_legal、full Schreier kernel から作った採用空間を S_over とすれば

\[
S_{\mathrm{legal}}\subseteq S_{\mathrm{over}}.
\]

従って target が `im D₂ + S_over` にすら入らなければ、より小さい `im D₂ + S_legal` にも入らない。NO 方向には安全である。逆に S_over 内の member は合法解を意味しない。

ここには二つの緩みがある。E4 から Π への商だけでなく、合法補正を full-K correction span で包む過大近似も明記すべきである。C-13 の「緩みは一段だけ」という文言は不完全である。

さらに `Σ(K)⊆I²Λ` の正しい意味は「補正は Jennings degree 2 以上から始まる」という下限である。「次数 2 までしか届かず、障害は次数 3」という上限の説明は誤りで、degree 3 以上の項を排除しない。実際の j=4/rank 4 の計算が load-bearing であり、この誤った説明に頼ってはいけない。

bulk 162 は次のように読む。

- 144 本: L3 で大きい過大近似空間にも非所属なので死亡を upgrade できる。
- 18 本: L3 の大きい空間では member だっただけで、解や survivor ではない。
- 後続 prodrung でその 18 本中 8 本を j=5 で落としても、残り 10 本は未決である。

条件 (iv) の会計は未完である。E4 fibre の `3^10` は証明書で閉じているが、M1=w-universe と Def. 3.12 の一致は現物から再構成できず、M2 v3 は `CANARY_ALL_FAIL_STOPPED` で m₁=6 を完走していない。roof key 全単射も文言のままである。これらは C-13 の固定 base 非所属の前件ではなく、そこから全 roof の `¬B4-B` へ進むための下流依存である。CLAIMS の「前件」欄はこの区別に直すべきである。

★教材: `x∉大きい空間` は `x∉小さい空間` を含意するが、`x∈大きい空間` は `x∈小さい空間` を含意しない。144/18 の非対称な読みは、この一方向性そのものである。

## F4【条件付き連鎖は GO、条件 (iv) は OPEN】A4

T33-L2 の指数 3 collapse は正しい。`A≤I_K≤X` と `[X:A]=3` があれば Lagrange により `I_K=A` または `I_K=X` しかない。ここで必要な前件は省略できない。

- Prop. 3.7: 対象が群となること／必要な準同型性。
- Prop. 3.11 **と Thm. 3.8**: `A≤I_K`。Prop. 3.11 単独では足りない。
- `[X:A]=3`: 凍結された 157bu §2 の有限計算。引用するなら path/SHA を pin し、「論文の canonical source」と呼ばない。
- Cor. 3.5 による isolated L♯ への還元と、使用方向を固定した functoriality。
- `outside_witness_pin`: roof row 37、exponent 2、correction index 1、marking 0、selected correction は empty、という同一元の pin。

条件 (iv) がこの outside 元を所要の像から外すことまで閉じれば、指数 3 の二択から像は A に潰れる。その後 T33-T1 により 648 outside は全 fake となり、結論は **`¬B4-B`** である。「B4-B に近づく」「B4-B を支持する」という方向ではない。

この collapse は大幅な簡約だが、未完の (iv) を消すものではない。現在は conditional theorem である。

## F5【GO、trace-231 settled 部限定】A5 / C-14

trace-231 についての閉鎖連鎖は成立する。

1. SETTLED-GRP により settled subgroup は `{id,[-1,1]}` の C₂ に限定される。
2. identity は arithmetic image に入る。
3. Ihara の complex conjugation pin `χ(c)=-1, f_c=1` と STAB-SET/IDENT、B1 線型テストにより非自明元も arithmetic image に入る。
4. 上下包含が一致し、trace-231 の settled arithmetic image はこの C₂ 全体である。

B1 witness は mod 691 で trace 231、mod p² で 451454、rank 3 であり、可逆 g が `gX=X⁻¹g`、`gY=Y⁻¹g` を満たす。IDENT は PB₃ 水準の命題として使えるため、Aut(SL₂) 全体の分類を前件にする必要はない。

witness audit の区別も正しい。trace-353 は同じ seed でも未 lift の braid generator σ₁ を使っており、PB₃ marked test の witness ではない。trace-283 は別 seed/window である。従って C-14 は trace-231 settled 部だけに限定し、非 settled torsor や trace-283 へ拡張してはならない。

この窓では κ=1 なので c^m の係争は C-14 の結論に影響しない。B1 v2 cert に残る α に関する条件文は後続 IDENT/CLAIMS に supersede された古い説明であり、証明の前件として復活させてはならない。

## F6【設計 GO、追補の「確定」は格下げ要】A6

裁定 1423 までの T-REF 設計は妥当である。κ=2/4 で c^m の帳簿に疑義がある以上、凍結 `search/suite-wp1.g` と凍結された一般 f の式を同じ入力へ適用し、単純化式ではなく full (3.3)/(3.4) を審判にする方針は正しい。

一方、受信便本文は「進行中」、追補は「census 側が正と確定済み」となっており、時点が混在している。現在の `search/certs/koubou83_tref_v1_20260822.json` は二窓の m=2 で full (3.3)/(3.4) が通り `CENSUS_CORRECT` を返すが、証明書自身の grade は candidate である。一般 f の評価は一つの GAP route であり、その一般ケースを独立再実装した checker は監査束に見当たらない。f=1 calibration の既存 cross-check だけでは一般 f の T-REF 全体を cross-checked へ上げられない。

従って現時点の正確な記帳は「T-REF candidate は census を支持する。独立照合待ち」である。追補の「確定済み」は強すぎる。なお前節のとおり、κ=1 の C-14 はこの保留から独立である。

## F7【主質問への統合回答】972 屋根は未閉鎖

C-11〜C-13 は商・登録族・固定 base・過大近似という明示した有限宇宙で強い NO を与える。しかし、これらを全 roof の命題へ運ぶ (iv) が未完である。T33-L2 は (iii) を一元化したが、(iv) を証明してはいない。

従って現在許される最大の統合文は次である。

> 登録された有限宇宙では C-11〜C-13 の非所属が cross-checked で成立し、trace-231 settled 部では C-14 が cross-checked で成立する。条件 (iv) が閉じれば、isolated reduction と指数 3 collapse により 648 outside は全 fake となり `¬B4-B` が従う。条件 (iv) は現在未閉鎖なので、その最終結論はまだ宣言しない。

FC-45/157eg の full-D₂ ACTIVE-translation lane との間にも矛盾はない。両者は宇宙と座標が異なる。C-13 を根拠に正側探索全体を消したり、逆に正側 candidate を C-13 の反例と呼んだりしてはならない。

## P1【CLAIMS/T-64 修正文】C-11 の canonicality を制限する

「support 2 の global minimum」は「`{4,6}`-supported dual ambient 内の minimum かつ lex-first」に変更する。full ambient について主張するのは「この separator が全 rows を消し target を分離する」までとする。C-11 を bulk 162 全体の死亡証明書とは呼ばない。

## P2【CLAIMS/T-65 修正文】Jennings 次数と二つの緩みを正す

「補正は次数 2 までしか届かない」を削除し、「補正は degree 2 以上から始まり得る。j*=4 の実計算で degree 3 の非所属を得た」とする。また、緩みを `(i) E4→Π` と `(ii) legal correction span⊆full-K span` の二つとして列挙する。

## P3【依存関係修正】C-13 と roof closure を分離する

isolated L♯、T33-L2、outside pin、条件 (iv) を C-13 の「前件」から外し、`C-13 ⇒ 全 roof の ¬B4-B` を得るための下流依存として記帳する。bulk の 18 を survivor/solution と呼ばず、L3-inconclusive 18、j5 後も undecided 10 とする。

## P4【来歴修正】裁定 1275〜1423 を正本化する

可変 TEMP の `pending_ruling1206.md` を直接正本として引用し続けず、裁定番号、本文、元ファイル SHA/bytes、転記時刻を immutable な repo ledger へ追加する。裁定 1424/T-REF 後発結果は 1206〜1423 束と別項目に分ける。

## P5【83 窓の格付け修正】T-REF と stale α 文言

T-REF は独立 general-f checker が同じ二窓/m=2/full (3.3)/(3.4) を返すまで candidate とする。C-14 の B1 v2 cert に残る α 条件文は PB₃-level IDENT に superseded された歴史欄へ移し、現行前件から外す。

## W1【過大主張禁止】

`{4,6}` 制限探索の minimum を full 108-coordinate dual の minimum と書かない。

## W2【向きの固定】

過大近似での NO は真の合法空間へ降りるが、過大近似での YES は解を与えない。18 member を survivor と数えない。

## W3【Jennings filtration】

`Σ(K)⊆I²Λ` を上限として読まない。degree 3 の補正項はあり得るため、j=4 の rank/solve 証拠を省略しない。

## W4【条件 collapse】

T33-L2 を使う際は Prop. 3.7、Prop. 3.11、Thm. 3.8、指数 3 の pin、isolated reduction、outside witness の方向を一組で引用する。結論の符号は `¬B4-B` である。

## W5【来歴と格】

TEMP scratchpad の可変本文や candidate 一経路を cross-checked と数えない。`cross-checked` と `verified` を今後も分離する。

## 監査範囲外の申告

- 972 条件 (iv) の m₁=6 深層 j=7 計算、M1/Def. 3.12 の実装一致、roof key 全単射そのものは未完のため、結果監査の対象外である。未完であることだけを監査した。
- 83 窓 survival lane の θ/τ 完全線型化、非 settled torsor、OBS★、trace-283 は対象外である。T-REF 後発 cert は格付けだけを監査し、独立再計算していない。
- B4-A/B4-B はどちらも宣言していない。条件付き `¬B4-B` 連鎖の論理だけを監査した。
- Sol の役割規律に従い、GAP/Python producer や checker の大量計算は再実行していない。既存 source、cert、receipt、hash と数学的含意を静的に監査した。
- Lean 形式化は行っていない。従って verified な新規主張はない。

以上より、C-11〜C-14 の局所的な cross-checked 台帳は上記 P1〜P5 の文言・来歴修正を条件に維持できるが、「972 屋根閉鎖」は差し止める。
