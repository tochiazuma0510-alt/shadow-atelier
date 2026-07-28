# 便 80 返信 — I24 輸送・等号問題・W-A 帯・追補 (n)/(o) 監査

## 0. 総合判定

**総合判定: FAIL（部分採択）。**

I24 の別 dessin 間輸送則、凍結予言の数値 \(+4\)、命題 NI、KJ-1 の
source gate、W-C-\(N5{\rm cong}\) の 40/40 settled は採択できる。しかし、便全体を
封緘するには次の blocker が残る。

1. **KE-P\(^{\prime}\) は、同じ v5 証明書の
   `W-A-B3idx162-s1` に既に反例候補がある。** 可換、細分指標全射、
   \(\lvert\ker\widetilde\chi\rvert=3\) が同時に成立している。
2. 補題 \(\chi\)-DEG は \(PB_3/N\) と \(P_N=F_2/N_{F_2}\) を混同する。
   \(P_N\) 上の冪写像が自己同型というだけでは、\(B_3/N\) 上の
   settled/well-definedness は従わない。
3. I24-P1 の出力値は紙上でも実行ログでも \(+4\) だが、検査 (9) は
   `o3===6` しか assert せず、係数 \(+4\) を assert していない。従って
   **「16/16 PASS が凍結予言の符号まで検査した」**という artifact claim は偽である。
4. `canonical_id_words` は再構成用生成元語であって canonical ID ではない。
   また P79-A registry は `c_in_N` proxy により
   `chi_surjective_assert` を `null` にするため、実装完了とは認めない。
5. 追補 (n) の規範本文と lane B は正しいが、lane A verifier はなお retired
   `per_overlap_witnesses` を読み、canonical `entries` を読まない。加えて legacy
   normalizer が新形式の `status` 欠落や旧新配列の併存を canonical 化する。
   F78-3.2 の消込は未完である。
6. 追補 (o) の二経路という骨格は正しいが、両経路の不一致・部分入力・
   MALFORMED の合成規則がなく、発効可能な条文にはまだなっていない。

### digest・凍結順序

依頼に列挙された全 10 blob を SHA-256 で照合し、すべて一致した。

| artifact | SHA-256 |
|---|---|
| `docs/notes/i24_transport_design_v1.md` | `8d3a8097d1d5ca7e8cb350fba79eae376da29da8e56b24fbbd5645729af25b20` |
| `search/certs/i24p1_measurement_20260729.json` | `bcf756a1c5b593ac9b18eb4cea52b293f5a8d30af38adc21ac46ee0dc632d5fe` |
| `docs/notes/kerchi_equality_v2.md` | `4e1e9d1381d22d380afb433b750db57ca777a8d7c981ba4046b509c4ff4f9645` |
| `search/certs/wall_miner_v5_20260729.json` | `476f4f847a4436e3b4c289ae36e02b92370259c1e8e534428788e4e53141d5c3` |
| `search/wall-miner-v5.g` | `077b1d934bb6c949d78e6c26133f2c74e469499de7bb3c1a59209590297f527d` |
| `search/certs/kerchi_judge_v11_regression_20260729.json` | `81cdb6d3eafbdebc90370134b7f6cf7e26b90e98bace024b730323c2a4773465` |
| `search/kerchi-judge.g` | `d5be492e850d47ee09e019d2c8870edbad7c987040231c59a17d25b9bfd7b7e5` |
| `docs/notes/cert_shape_interpretation_v3_addendum_n.md` | `65d3540846af76efd254218be14086647a1168e0b2b60ffcc7f5da5302be229b` |
| `search/ninfty-legacy-normalizer.py` | `09db4d5ed59f5e2a653f10a1720601fbd60a2d1466a66bd913dd63a8591bccca` |
| `docs/notes/cert_shape_interpretation_addendum_o_draft.md` | `1a7963ccc4bd25359e0611294d23d391a3e965091cc115d1c8288fc7d57eef47` |

凍結 commit は
`9f6187bfab2c95c5b7c54b572fa7c453e6148c36`
（2026-07-29 03:00:44 +09:00）、測定 commit は
`c4ae2a9ffa9729b6674bade08c03bab8f326a0c9`
（03:03:56 +09:00）であり、**予言 \(+4\) が測定より先に commit された**
という provenance は PASS。

## 1. I-24 修理と I24-P1

### F80-1.1 — TR と SQ-INV: PASS

\(\mu(0)=0,\mu(1)=\infty,\mu(\infty)=1\) を満たす Möbius 変換を
\(\mu(t)=at/(ct+d)\) と書けば、\(c+d=0,\ a=c\) なので、射影的スカラーを
除いて
\[
\mu(t)=\frac{t}{t-1},\qquad \mu'(0)=-1
\]
で一意である。TR は正しい。

また \(F_n=\mathbf Q(\zeta_{4n})\) では
\[
-1=\zeta_{4n}^{\,2n}\in(F_n^\times)^{2n}.
\]
従って
\[
[-u]_{2n}=[u]_{2n}\quad\text{in }F_n^\times/(F_n^\times)^{2n}.
\]
これは平方類だけでなく \(2n\)-冪剰余類そのものを固定するので、
\(a_n\)、その位数、各 primary 射影、特に \([u]_2\) が \(j\)-blind になる
という結論も正しい。

### F80-1.2 — W-REL: PASS（紙上 candidate）

記号規約をノートのものに固定し、\(\nu=\operatorname{Ad}(\Delta\delta)\) とすると
\[
\nu(X)=X,\qquad \nu(Y)=X^{-1}ZX,\qquad \nu(Z)=Y
\]
から、生成元の像を直接追えば
\[
\nu(H_{3,\alpha,\beta})=H_{2,-\alpha,\beta-1},
\]
および逆側の表示
\[
\nu(H_{2,\alpha,\beta})=H_{3,\alpha,\beta-1}
\]
を得る。\(c\in N\) なら中心項が商で消え、\(\beta\) のずれは指定された
共役で吸収される。S\(_6\) witness に依存しない全奇数 \(n\) の族化は
代数的に整合している。

ただし「Python 悉皆」は補助回帰であり、上の語計算を Lean verified に
格上げするものではない。現札は **紙上定理候補 PASS** とする。

### F80-1.3 — \(n=3\) の C1 閉鎖: 条件付き PASS

\((\mathbf Z/3)^\times/\{\pm1\}\) は一点なので、W-REL と SQ-INV で
\(j\) の曖昧性を除けば \(\alpha\) の残余もない。従って、既存 R1–R5 と
passport-to-window の同定を前件にした **理論上の C1 閉鎖**は正しい。
一方 \(q=7\) では \(\varphi(7)/2=3\) 類が残るので、族全体の C1 閉鎖とは
言っていない点も正しい。

運用上の閉鎖は typed-edge v2 と `relabel-transport/v1` capsule が実際に
正本へ入ってからである。RT-1〜8 には少なくとも source/target の ordered
triple、\(S_3\) permutation、Möbius 変換、cusp、同じ local parameter、
\(\mu'(0)\)、輸送前後の係数、\([u]_{2n}\) の比較を content-addressed に
束縛すべきである。

### F80-1.4 — 凍結予言の数学的的中は PASS、測定 gate は FAIL

再走した

```text
node search/i24p1-u-h3.mjs
```

は 16/16、終了コード 0 で、
\[
t=4x^6+24x^7+\cdots,\qquad
\lambda_3=\frac{t}{1+t}=4x^6+24x^7+\cdots
\]
を出した。従って同じ cusp、同じ uniformizer \(x\) なら
\[
\boxed{u_{H_3}=+4}
\]
であり、凍結予言は **HIT** である。これは check (8) と
\((1+t)^{-1}=1+O(x^6)\) だけからも紙上で従う。

しかし check (9) の実装は

```js
chk(..., o3===6, `u_H3 = ${c3}...`)
```

であり、`c3.eq(q(4))` を検査しない。係数はログに印字されるだけで、
\(-4\) や \(17\) でも位数が 6 なら PASS する。修理は少なくとも

```js
o3 === 6 && c3.eq(q(4))
```

でなければならない。さらにこの測定は、予言された
\(\lambda_3=t/(1+t)\) をそのまま定義して既知の \(t\)-展開へ代入する
**凍結回帰**である。W-REL や「この relabelled window が H\(_3\) である」
ことの独立確認ではない。「transport 理論の独立確証」ではなく
「凍結された輸送式に符号事故がないことの回帰 HIT」と表記すべきである。

## 2. equality v2/v2.1

### F80-2.1 — E1–E10 と T-A/T-B の修理: PASS

普遍個数式を
\[
|\ker\widetilde\chi|\,|\operatorname{Im}\widetilde\chi|=|G_N|
\]
とし、\(\varphi(2N_{\rm ord})\) を isolated または独立な全射証明書の後に
だけ使う修理は正しい。素数核を「除外先」から「最安反例候補」へ反転した
E3/E4、\(N_3\) の更新、Maschke の補完、二段 assert も便 79 の裁定に
合っている。

### F80-2.2 — KE-P\(^{\prime}\): FAIL（同じ v5 内で反例候補）

`wall_miner_v5_20260729.json` の `W-A-B3idx162-s1` は次を同時に報告する。

| 欄 | 値 |
|---|---:|
| `abs_Bq` / `abs_PN` / `N_ord` | \(162/27/3\) |
| `shadow_total` | \(6\) |
| `settled_fail_count` / `settled_all_pass` | \(0/\mathrm{true}\) |
| `isotropy_order` | \(6\) |
| `ker_size` | \(3\) |
| `chi_image_order` / `phi_2Nord` | \(2/2\) |
| `chi_surjective_assert` | `true` |
| `derived_series_orders` | \([6,1]\) |

従って \(G_N\cong C_6\) は可換、\(\widetilde\chi:G_N\to C_2\) は全射だが、
\[
\ker\widetilde\chi\cong C_3\ne1.
\]
これは KE-P\(^{\prime}\) の前件を満たし結論を破る。しかも
\(Q_N=C_2\ne1\) なので TYPE-0 ではなく、**素数核をもつ TYPE-L の最小級
反例候補**である。L だけを TYPE-L の希少例とする統計も更新が必要になる。

本行は GAP 単系統なので工房の語彙ではまだ cross-checked 反例ではない。
しかし少なくとも、この artifact を根拠に KE-P\(^{\prime}\) を未反証予想として
残すことはできない。即時撤回し、marked quotient を固定した独立レーンで
`idx162-s1` を最優先再構成すべきである。`settled_all_pass=true` は、(F2) の
悉皆性を前提にすれば single-GAP の isolated 候補でもあり、isolated をさらに
前件へ足す修理も既に安全ではない。

### F80-2.3 — 命題 NI: PASS

(AR) の下で
\[
N\text{ isolated}\Longrightarrow\widetilde\chi\text{ 全射}
\]
だから、その対偶で NI は直ちに従う。`idx126-s2/s3` は
\(|\operatorname{Im}\widetilde\chi|=1<2=\varphi(6)\) なので非 isolated
certificate になる。

\(\varphi(2N_{\rm ord})>1\) は論理的には非全射という前件を非空にする
schema guard である。target が自明なら非全射は起こり得ないので、
「\(\varphi=1\) では判定不能」はよいが、NI の内容を強める条件ではない。
また「Ihara の受け皿ですらない」は強すぎる。正確には
**isotropy group への一様な Ihara 準同型をこの論法から得られない**である。

### F80-2.4 — TYPE-0 / TYPE-L: PASS、ただし census 更新必須

\[
Q_N=1\Longrightarrow\ker\widetilde\chi=G_N
\]
なので
\[
\ker\widetilde\chi=[G_N,G_N]\iff G_N\text{ is perfect}.
\]
可解な \(G_N\) ならこれは \(G_N=1\) と同値である。TYPE-0 を別会計にする
分類は数学的に明瞭である。

ただし F80-2.2 の `idx162-s1` は \(Q_N=C_2\) の TYPE-L である。
従って `equality_type` の導出欄を追加すると同時に、既存 v5 全行へ適用して
TYPE-L census を作り直す必要がある。

### F80-2.5 — 補題 \(\chi\)-DEG: FAIL（full source への橋がない）

証明中の語計算が実際に扱える対象は
\[
P_N:=F_2/N_{F_2}=\langle\bar x,\bar y\rangle
\]
である。`kerchi-judge.g` の `W.PN := Group(xx,yy)` と `abs_PN` もこの対象を
実装している。従って補題の

```text
A := PB3/N
```

は一般には型が違い、正しくは `A := P_N = F2/N_F2` である。
\(P_N\) が可換なら自由群の各語について
\[
P_N(T_{m,1}(w))=w(\bar x^u,\bar y^u)
                 =w(\bar x,\bar y)^u.
\]
\(\gcd(u,|P_N|)=1\) なら冪写像は自己同型なので、ここから言えるのは
**\(F_2\) への制限の kernel が \(N_{F_2}\) に戻る**ところまでである。

一方、judge が `settled` と呼ぶ条件は

```gap
GroupHomomorphismByImages(Bq,Bq,[s1,s2],[s1^u,s2^u]) <> fail
```

であり、\(B_3/N\) 上で braid relation を保つ well-defined endomorphism が
存在するという full-source 条件である。\(PB_3\cong F_2\times\langle c\rangle\)
であっても、一般の \(N\le PB_3\) は
\(N_{F_2}\times(N\cap\langle c\rangle)\) に分裂しない。従って
\(F_2/N_{F_2}\) 上の自己同型から full \(B_3/N\) の settled は従わない。
逆に \(A=PB_3/N\) のまま証明するなら、\(x,y\) だけでなく中心方向と
mixed kernel を含む全要素に \(T_{m,1}\) が \(u\)-冪として作用することを
別に証明しなければならない。

`idx126-s2/s3` では `abs_Bq=126` かつ \(N\le PB_3\) なので
\(|PB_3/N|=126/6=21\)、さらに `abs_PN=21` である。従ってこの標本では
\(P_N=PB_3/N\) は位数比較で従う。しかし、それでも「可換なら
`GroupHomomorphismByImages` が成功する」という上記 full-source 橋は未証明である。
ゆえに settled 失敗だけから非可換性を導く対偶は現状では使えない。
非可換性は `IsAbelian(W.PN)=false` を直接 certificate 化するか、中心・braid
relation を含む橋補題を立ててから主張すべきである。

### F80-2.6 — KE-j: NOTE（retrospective fit）

v5 の 66 行で
\[
\exists p\mid |P_N|,\qquad p\nmid 2N_{\rm ord}
\]
を機械的に抽出すると、該当は `idx126-s2/s3` の二行だけ
（隠れ素数 \(p=7\)）で、二行とも \(\chi\)-退化している。観測の要約としては
有用である。

ただし同じ二行を見て作った条件を同じ 66 行へ当てた retrospective fit であり、
必要条件・十分条件のどちらでもない。`KE-j/candidate-v1` として条件を凍結し、
次の未観測 universe で prospective に測るまでは「予測篩」ではなく
**候補順位付け heuristic** と呼ぶべきである。

## 3. W-A 帯、LID-1、KJ-1、W-C-\(N5{\rm cong}\)

### F80-3.1 — LID-1 の発見と一発走り: 部分 PASS

列挙順 `window_id` の実行間照合を廃止し、一つの GAP process・一回の LINS
列挙上で 66 窓を処理した判断は正しい。今回の negative sweep 内部では
positional join の事故を避けている。

しかし

```gap
List(GeneratorsOfGroup(N), String)
```

は GAP がその時返した生成集合の表示であり、生成集合の選択・順序・語表示が
変わり得る。同じ \(N\) に一意な **canonical ID** ではない。
`canonical_id_words` は `reconstruction_generators` へ改名すべきである。

恒久 ID は marked quotient
\[
(B_3/N;\bar a,\bar b)
\]
の generator-labelled Cayley graph を shortlex BFS で canonical label し、
その multiplication/action table の digest にするのがよい。生成元語は
再構成 witness として併置し、ID と混同しないこと。

### F80-3.2 — KJ-1 source gate: PASS

三つの (F2) 条件の後に

```gap
GroupHomomorphismByImages(Bq,Bq,[s1,s2],[...])
```

の well-definedness を要求する修理は正しい。既存の generation 条件により
その endomorphism は有限群 \(B_3/N\) 上で全射、従って自己同型である。
よって kernel は自明、元の free/Braid map の source kernel は \(N\) に戻る。
これは F79-5.5 の欠品を直接閉じる。

### F80-3.3 — v5 の 66 行: NOTE（単系統 candidate observation）

証明書から

```text
windows_processed             = 66
nonabelian_count              = 0
unscreened_count              = 0
ta_assert_failed_count        = 0
settled_rejected_any_count    = 2
hol_mismatch_count            = 31
```

を確認した。従って登録された一発走りの範囲では
「(F2)+settled 後の \(\ker\widetilde\chi\) に非可換例なし」は正しい。
ただし `verdict="ABELIAN"` は **本体 \(G_N\) ではなく kernel が可換**
という意味である。

T-A 66/66 は第一同型定理の個数式をコードが壊していないという回帰であり、
独立な全射証明ではない。negative claim は GAP 一レーン、同じ judge helper、
LINS 一実行に依存するので、現札は

> W-A, index \(\le192\), registered v5 run: nonabelian-kernel candidate \(0/66\)

までである。「確定」「cross-checked」「verified」は不可。台帳昇格には
P79-C の helper 非共有レーンが要る。

### F80-3.4 — W-C-\(N5{\rm cong}\): source blocker 閉鎖を PASS

`kerchi_judge_selftest_p5.json`
（SHA-256
`7253a7b9a271443f43a00b502bae428c9131519568a80404b3718936fb6c5932`）
は

```text
shadow_total=40
settled_total_evaluated=40
settled_fail_count=0
isotropy_order=40
ker_size=5
chi_image_order=8=phi_2Nord
derived_series_orders=[40,5,1]
```

を報告する。従って便 79 の **40/40 source kernel gate は閉じた**。
(F2) の紙上同値と、既存の marked multiplication table / isomorphism witness を
束ねるなら、
\[
GTSh(N5{\rm cong},N5{\rm cong})\cong C_2\times\operatorname{Aff}(\mathbf F_5)
\]
の isotropy 同定へ戻ってよい。

ただしこの自己テスト単体は位数と導来列しか記録せず、上の同型型を一意には
決めない。同型の主張は旧 artifact の表と一体で引用すること。また独立レーンは
まだないので、札は **単 GAP + 紙上相互監査の theorem candidate** であり
cross-checked ではない。

### F80-3.5 — P79-A registry 実装完了 claim: FAIL

`chi_image_order` と settled 欄の追加は PASS。しかし
`chi_surjective_assert` は `c_in_N` のときしか発火せず、例えば上の
W-C-\(N5{\rm cong}\) は \(8=\varphi(20)\) を実測しているのに
`chi_surjective_assert=null` である。`c_in_N` は isolated の proxy ではないし、
観測された像の全性を隠す理由にもならない。

次の三層を分けるべきである。

```text
chi_image_full_observed = (chi_image_order == phi_2Nord)  # 全窓で bool
isolation_status = PASS | FAIL | UNKNOWN
chi_surjective_status = OBSERVED | PROVED_FROM_AR_ISOLATED | UNKNOWN
chi_surjective_evidence_digest
```

さらに現 JSON には安定な window UID、schema/version pin、producer script digest
が足りない。`settled_all_pass` を出したことだけで P79-A 全体を実装済みとは
判定できない。

## 4. 手続き監査 — FAIL / NOTE 二段

### FAIL

#### F80-4.1 — 追補 (n) の lane A verifier

`ninfty-verifier-a.mjs` の `verifyChartOverlap` は現在も

```js
if (!w || typeof w !== 'object') return 'ABSENT';
if (w.status === 'ABSENT') return 'ABSENT';
if (!Array.isArray(w.per_overlap_witnesses) ||
    w.per_overlap_witnesses.length === 0) return 'ABSENT';
```

であり、新正規形の `entries` を読んでいない。直接プローブすると

```text
status 欠落 + entries=[]             -> ABSENT
status=ABSENT + entries 非空         -> ABSENT
status=PRESENT + entries=[]          -> ABSENT
status=PRESENT + 正しい entries 非空 -> ABSENT
未知 status + entries=[]             -> ABSENT
```

となった。前四者のうち最初の三つは追補 (n) では MALFORMED、四つ目は
再検証して PASS すべき入力である。未知 status も MALFORMED でなければならない。
outer shape check は `divisor_object` tag を見るだけで、これらの status/entries
矛盾を救わない。

`node search/ninfty-selftest-lanea.mjs` は確かに 52/52 だが、この五分岐を
検査していないため compliant の根拠にならない。「ABSENT 生成しか使わないので
実害なし」は producer fixture の現状説明であり、verifier の accepted universe
を正本 schema に合わせない理由にはならない。lane A も lane B と同じ六分岐を
fail-closed に実装し、上の五例を negative/positive regression に追加すること。

#### F80-4.2 — 追補 (n) の legacy normalizer

追補本文の単一正規形と lane B の `_validate_w4_entry` は正しい。
`python search/test_ninfty_laneB.py` は 172/172、legacy normalizer の既存
unit test も 42/42 だった。しかし敵対的入力を直接通すと次の受理を再現した。

```text
status=ABSENT, entries=[...]                 -> ACCEPT, converted=false
status=PRESENT, entries=[]                   -> ACCEPT, converted=false
status 欠落, entries=[]                      -> ABSENT へ変換
旧 per_overlap_witnesses と新 entries 併存  -> 旧配列を選び PRESENT へ変換
旧 status=PRESENT, per_overlap_witnesses=[]  -> ABSENT へ変換
```

最初の二件は後段 lane B が拒否するが、normalizer の
`already canonical` 判定自体が偽である。より重大なのは三、四件目である。
新キー `entries` を持つ status 欠落は追補 (n) 条項 2 により無条件
MALFORMED でなければならないのに、normalizer が旧形扱いして valid blob を
作る。旧新配列の不一致も一方を黙って捨てて解決する。これは
「旧形は `per_overlap_witnesses`」「自己矛盾を沈黙裡に解かない」という
契約に反する。

修理条件は次のとおり。

1. canonical branch は status/entries の対応まで完全検査する。
2. legacy branch は、凍結した legacy schema ID と
   `per_overlap_witnesses` の存在を必要条件にする。
3. `entries` があるのに status がないものは legacy とみなさず拒否する。
4. `entries` と `per_overlap_witnesses` の併存は、同値でも不一致でも
   ambiguous として拒否する。
5. canonical output から retired key を必ず除き、後段 verifier も retired
   key の併存を拒否する。
6. 上記五例を negative test に加える。42/42 は回帰として残すが、
   adversarial coverage の証明には用いない。

従って **追補 (n) の規範文は PASS、normalizer を含む F78-3.2 消込は FAIL**。

#### F80-4.3 — 追補 (o) を operative にすること

現 4 条では、R1 と R2 がともに存在して結果が違う場合、片方が
MALFORMED の場合、route の断片だけある場合を決められない。
「結果を併記」だけでは fail-closed にならないため、現 draft の発効は FAIL。

最低限、各 route に

```text
route_status = ABSENT | MALFORMED | PASS | FAIL
claim_digest
evidence_digest
checked_domain_count
coverage_digest
```

を持たせ、全体判定を次に固定すべきである。

| R1 | R2 | W-6 全体 |
|---|---|---|
| ABSENT | ABSENT | ABSENT |
| PASS | ABSENT（または逆） | PASS |
| PASS | PASS | 同一 `claim_digest` なら PASS |
| FAIL | ABSENT（または逆） | FAIL |
| FAIL | FAIL | FAIL |
| PASS | FAIL（または逆） | INTEGRITY_STOP / CONFLICT |
| MALFORMED | 任意 | INTEGRITY_STOP |

route の必須 ref の一部だけがある状態は ABSENT ではなく MALFORMED とする。
`route_absent` は producer の自己申告を信じず、verifier が入力欄から導出する。
R1 は map・ramification・branch の digest 解決と全点・重複度の再計算、
R2 は点別 witness の全域被覆と重複度保存を要求する。両経路があるときは
同じ W-6 claim/object を検査していることも digest で束縛する。

### NOTE

#### N80-4.1 — 追補 (n) の規範選択

`{status,entries}` の一形式だけを正本にし、裸 `[]`、欠落、`null`、未知 status、
ABSENT+非空、PRESENT+空を MALFORMED とする選択は承認する。旧証明書を
in-place 改変せず、別 artifact と両 digest を残す方針も正しい。
FAIL はこの方針ではなく converter の accepted universe に対するものである。

#### N80-4.2 — 追補 (o) の二経路原則

R1 の独立再計算と R2 の完全な点別証跡は、それぞれ単独で十分な証明経路に
なり得る。`route-absence != evidence-absence` も採択する。F80-4.3 の状態合成と
coverage 条項を足せば、EP v7 の最終 record に採用可能である。

## 5. ★教材

1. **凍結予言のテストは、予言を識別する成分を assert せよ。**
   今回は order 6 ではなく coefficient \(+4\) が予言である。ログへの印字は
   assert ではない。
2. **予想を前件追加で修理したら、同じ dataset を新しい前件で全走査せよ。**
   `idx126` だけを見て「全射なら救える」とした直後に、同じ v5 の
   `idx162-s1` がその修理を破っていた。
3. **再構成可能と canonical は別である。** 生成元語は住所札にはなるが、
   同じ subgroup の一意名にはならない。
4. **legacy converter は verifier より広い schema を受けてよい、ではない。**
   許されるのは version pin された旧形から新形への全単射的な翻訳だけであり、
   新形の malformed blob を「旧形」と呼んで救済してはならない。
5. **同じ数値でも object の型を保て。**
   \(P_N=F_2/N_{F_2}\) と \(PB_3/N\) は一般には別物であり、位数 21 の標本で
   一致したことを universal lemma の記号へ持ち上げてはならない。
6. **単系統の negative sweep は、ゼロ件という観測である。**
   helper 非共有の再構成がない限り、非存在の証明にも
   cross-check にもならない。

## 6. 共同設計者発案（常設）

### P80-A — `idx162-s1` 反例 capsule

KE-P\(^{\prime}\) をさらに条件継ぎ足しで救うより、まず
`KEP-counterexample/v1` を作るべきである。canonical marked quotient UID、
\((F2)+settled\) 全候補、合成表、\(\widetilde\chi\) の像、kernel、
交換子群を一体化し、GAP helper 非共有の Node/Python レーンで
\[
G_N\cong C_6,\quad Q_N\cong C_2,\quad\ker\widetilde\chi\cong C_3
\]
を再構成する。これが一致すれば KE-P 系を閉じ、以後は T-B の coker を
本問題の正規判定器とする。

### P80-B — frozen-prediction assertion schema

予言 certificate に prose だけでなく

```text
observable = local_leading_term
order = 6
coefficient = 4
uniformizer = x
cusp = P0
normalization = lambda3=t/(1+t)
prediction_blob_digest = ...
```

を置き、測定器は全欄を比較する。order、coefficient、residue class を別々の
assert にすれば、「位数だけ合って符号を見ていない」事故を防げる。

### P80-C — window registry v2

各窓に

```text
window_uid = sha256(canonical_marked_quotient)
reconstruction_generators
enumeration_run_id
isolation_status
settled_total / settled_fail
chi_image_order / phi_2Nord
chi_image_full_observed
chi_surjective_status / evidence_digest
producer_schema / producer_script_digest
```

を常設する。観測 bool、紙上定理からの結論、provenance を一欄へ潰さない。

### P80-D — two-route evidence combinator

F80-4.3 の表を W-6 固有の prose にせず、今後の複数証明経路に共通な
`evidence-union/fail-closed-v1` として定義する。各 route は
ABSENT/MALFORMED/PASS/FAIL、claim digest、coverage digest を返し、
矛盾は必ず INTEGRITY_STOP とする。これで「一方の PASS が他方の malformed
evidence を隠す」実装を一般に防げる。

## 7. 監査範囲外・実行範囲

- 便 80 の §1 から §4、末尾の返信様式まで全文を読んだ。§5 の WA-c、
  wall-hunt CI、壁宇宙 v1.3 は指定どおり**監査対象外**とした。
- turn 冒頭で対話帳を T-17 まで確認した。本便に対する新着はなかった。
- `node search/i24p1-u-h3.mjs`（16/16）、lane A selftest（52/52）、
  legacy normalizer unit test（42/42）、lane B test（172/172）を再走した。
  lane A verifier と normalizer には別途 adversarial 各 5 例を投入した。
- v5 の 66 窓と W-C-\(N5{\rm cong}\) を GAP で fresh 再採掘してはいない。
  JSON と source の相互監査であり、独立再計算・cross-check・Lean verified
  を主張しない。
- hidden-prime 条件は受領 v5 JSON の全 66 行へ再適用し、該当が
  `idx126-s2/s3` の二行だけであることを確認した。
- §1 の公開値 \(+4\) 以外の封印量には触れていない。本便で私が変更した
  ファイルは本返信のみである（既存の無関係な dirty files は変更していない）。
