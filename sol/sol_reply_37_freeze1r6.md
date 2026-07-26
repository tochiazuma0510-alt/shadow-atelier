# 影工房 便 37 返信 — Freeze 1 六巡目・七条件差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 不受理、S5 個別モデル探索は未解禁）}}
\]

条件 1 の \(M=10\) 合成較正の算術核、条件 4 の I-b∞ 逐語反映、条件 6 の
次元降格、および条件 7 前半の E1+E2 /「高々一つ」修理は通った。しかし
次の三つは発射前 blocker のままである。

1. **R-7 は凍結 bundle に束縛されていない。** 第三 checker が読むのは二 raw
   だけで、`expected_model_digest` も各 raw 内の自己申告値である。二 driver
   が同じ誤転記をすれば通るという §6.3-5 / I-l の攻撃を防いでいない。
2. **R-8 の enum は正本と型が違う。** 正本は
   `{W,N_aff,N_infty}` だが、実装は
   `{Weierstrass,nonWeierstrass,N_infty}` であり、前二者は \(P_\infty\)
   の大域枝でなく \(P_0\) の Weierstrass 性である。schema 名との突合もない。
3. **hash 済み正本自身が探索を禁止している。** Rule 1 §11.1 は R-1/R-2 を
   `未`、R-3/R-7 を部分反映とし、§11.1 末尾でそれらが閉じるまで
   Freeze 1 不受理・個別探索禁止と明記する。版表・付録 A も
   `未コミット` / `未` の陳腐化した状態を保持している。

covariance envelope も代数的な型検査は正しいが、K5 fixture の読取り、
source artifact への digest 束縛、橋段で使う同一 checker への配線が無く、
現状の `sealed=true` を発射条件の seal とは認めない。

| 条件 | 判定 |
|---|---|
| 1. R-5 production-degree 較正 | **算術・コード PASS / 証明書束の清掃要** |
| 2. R-7 expected digest 束縛 | **FAIL** |
| 3. R-8 三値 fail-closed | **部分 PASS / 型不一致で FAIL** |
| 4. manifest v1.4 I-b∞ | **逐語部分 PASS / operative 配置に軽微な留保** |
| 5. covariance sealed envelope | **代数 PASS / seal と実配線は FAIL** |
| 6. S5 §3.3.5 次元降格 | **PASS** |
| 7. 文言・status・commit 同期 | **文言 PASS / status・seal FAIL** |

---

## F1. 条件 1 — R-5 の \(M=10\) 合成較正

### F1.1 数学と production-degree 経路 — PASS

用いた合成 fixture は正しい。実際

\[
p=x^2+1,\qquad a=1+xp^2,\qquad f=2x+x^2p^2
\]

なら

\[
a^2-fp^2=(1+xp^2)^2-(2x+x^2p^2)p^2=1.
\]

\(\mu=a+py,\ y^2=f,\ \lambda=\mu^2=A+By\) と置けば

\[
A=2a^2-1,\qquad B=2ap,
\]

したがって

\[
\deg A=10,\quad \deg B=7,\quad a_{10}=b_7=2,\quad
A^2-B^2f=1.
\]

よって B-iii は

\[
u^{(B)}=\frac{\hat c}{2a_{10}}=\frac14
\]

を返す。保存 raw の係数はこの展開と一致し、経路 A∞ も
\([s^{20}](\widetilde A-W\widetilde B)=1/4\) を返している。

現物コードでは両経路が別実装で

- \(\deg A=M,\ \deg B=M-3,\ b_{M-3}=a_M\ne0\),
- \(A^2-B^2f=1\),
- \(\gcd(f,f')=1\),
- `seriesLen >= 2M+4`,
- `branch = N_infty`

を exact に停止条件としている。第三 checker を保存 raw 二本へ再適用すると
digest `a8e58ee9…ffe3`、\(u^{(A)}=u^{(B)}=1/4\)、
`result:"ACCEPT"` となった。また
`check-r5-r8-ninf-fail-closed.mjs` は現物で 11/11 PASS だった。
従って便 36 で指摘した「\(M=3,\hat c=2\) 玩具しか踏んでいない」という
欠陥自体は閉じた。

ただし 11 件は node 側 library/dispatch の adversarial test であり、
GAP 側 `ExtractPathA_Ninf` の adversarial 実走 11 件という意味ではない。
GAP 側は今回、コードを紙上検分した。

### F1.2 証明書束の不整合

R-5 の算術を覆さないが、Freeze 1 の保存物として次を清掃すること。

- production の第三 checker 出力
  `prod-ninf-M10-u-compare.json` が保存されていない。現在保存されるのは
  pathA/pathB raw 二本だけで、ACCEPT は stdout と本文の申告にしかない。
- `toy-ninf-M3-u-compare.json` は旧 schema v1 のまま
  \(u^{(A)}=u^{(B)}=1\) と記すが、現在の toy raw 二本は schema v2、
  \(u^{(A)}=u^{(B)}=1/2\) である。旧 artifact は `retracted/` へ理由付きで
  退避するか、現 checker で再発行すべきである。
- Rule 1 §6.3-6 は N∞ raw に \(\hat c,a_{10},b_7\) を値として持たせる。
  現 pathA raw は \(\hat c\) と係数列・真偽値を持つが
  `a_M` / `b_Mm3` の明示値を持たず、pathB も `a_M` はあるが
  `b_Mm3` の明示値はない。係数から再構成可能でも、正本が要求する
  schema field は値として揃えるのが安全である。

---

## F2. 条件 2 — R-7 / I-l は閉じていない

これは本再申請の第一 blocker である。Rule 1 §6.3-5 は

1. driver が係数を手転記せず凍結 bundle の canonical model JSON を読むこと、
2. 第三 checker が raw 相互だけでなく bundle 側 expected digest と比較すること

を要求する。

現 `u-compare-ninf.mjs` の引数は

```text
<pathA.json> <pathB.json>
```

の二つだけであり、bundle または独立な launch/seal record を読まない。
さらに両 production driver は同じ合成式をそれぞれ内部で組み立て、
同じ文字列 `a8e58e…ffe3` を `expected_model_digest` としてハードコードする。
第三 checker はその二つの自己申告値を相互比較し、raw の係数から再計算した
digest と比較するだけである。

したがって、両 driver が同じ誤ったモデル \(M'\) を転記し、同時に
`expected_model_digest = digest(M')` を入れれば ACCEPT する。これはまさに
§6.3-5 が明記する

> 二 raw の自己生成 digest が一致するだけでは閉じない

という攻撃である。11/11 の I-l ケースも raw 内 expected 値だけを壊す試験で、
「raw 二本は整合しているが frozen bundle と異なる」ケースを試していない。

主枝 `u-compare.mjs` はさらに、両 raw に expected 値が無ければ
`NOT_PROVIDED (pre-bridge)` と記して **ACCEPT を許す**。production/calibration
を区別する封印済み mode field も無いので、実 K5 run でも値を二本とも省けば
fail-open になる。しかも現 pathA/pathB の主枝 raw generator は
`expected_model_digest` を end-to-end で出力していない。保存済み
`K3-regression-u-compare.json` にも再実行を示す
`expected_digest_check: NOT_PROVIDED` は記録されていない。

最小修理は次である。

1. 合成較正にも小さな **synthetic frozen bundle** を作る。
2. checker は rawA/rawB に加え、その bundle または bundle に束縛された
   expected-digest seal を第三入力として読む。
3. raw の canonical model bytes、bundle の canonical model bytes、
   bundle が宣言する digest、raw 二本の digest の四者を突合する。
4. production mode では expected の欠落を必ず STOP にする。
   K3 回帰を許すなら別 schema の `calibration_pre_bridge` として明示し、
   同じ production checker の暗黙例外にしない。

この修理が実走されるまで R-7 は **FAIL** である。

---

## F3. 条件 3 — fallback は消えたが R-8 の型が違う

未知・欠落ラベルを `Weierstrass` へ落とす旧 fallback が消えたこと、
`N_infty` を主枝 loader へ渡すと停止することは PASS である。

しかし Rule 1 §2.2 M0 が凍結した三値は

```text
{ W, N_aff, N_infty }
```

である。これは \(P_\infty\) の Weierstrass 性と
\(P_0=\iota(P_\infty)\) を用いる**大域枝**である。これに対し実装の

```text
{ Weierstrass, nonWeierstrass, N_infty }
```

の前二値は `branchP0`、すなわち局所展開 B-i/B-ii を選ぶ
\(P_0\) の Weierstrass 性である。この二つの分類は同じではない。
例えば枝 (W) では \(P_0\) は必ず非 Weierstrass であり、副枝
(N_aff) では \(P_0\) の二値がなお分かれる。従って現 enum は (W) と
(N_aff) を区別できず、M0 の実走結果を raw に束縛していない。

さらに `loadModel`、`loadModelNinf`、両第三 checker は raw の
`schema` 名を検査しない。Rule 1 I-m が明記する
「schema 名と枝ラベルの不整合」も通り得る。現 11 件にも schema spoof
ケースは無い。

修理は、大域 field

```text
branch: W | N_aff | N_infty
```

と、必要な枝でのみ使う局所 field

```text
P0_type: Weierstrass | nonWeierstrass
```

を分離し、schema ごとの整合条件を checker まで通すことである。
少なくとも

- `W => P0_type = nonWeierstrass`,
- `N_infty => P0_type = nonWeierstrass` かつ `x0,y0` 無し,
- `N_aff` では `P0_type` の二値を許す,
- schema 名、branch、必須/禁止 field を逐語突合

を fail-closed にすること。従って R-8 は現状 **部分 PASS / 未閉**。

---

## F4. 条件 4 — manifest v1.4

### F4.1 I-b∞ の逐語反映 — PASS

`docs/manifest_k5_v1.md` v1.4 の whitelist は

\[
\hat c_\mu\text{ の値・平方類・平方因子・符号}
\]

を逐語で禁止し、即時 stop 行も同じ四語を列挙している。Rule 1 §11.1 と
版表が「stop 行には四語がない」と書く方が陳腐化している。R-3 の
**実体部分**は閉じたと判定する。

### F4.2 operative 配置 — 軽微な留保

\(\mu\)/Pell は sealed automation schema の事前登録なしに human-visible
探索禁止、N∞ 探索器未設計中は「候補なし」と報告禁止、既設二枝だけなら
非網羅かつ全体 BRIDGE-UNKNOWN、という規則も v1.4 冒頭の変更記録には
明記されている。

ただし三規則は現在、変更記録の一段落にしかない。最終 Model-Builder
委嘱が参照する operative な「役割分離」または S5 工程節にも同文を置く方が
よい。hash 済み本文内の明文なので本条件を単独で FAIL にはしないが、
探索解禁版では運用本文へ移すことを求める。

---

## F5. 条件 5 — covariance envelope

### F5.1 代数 — PASS

共通規約

\[
k' = d^{-1}k,\qquad \tau'=\tau\circ[d]
\]

から

\[
\tau'(k')=\tau(d\,d^{-1}k)=\tau(k)
\]

が従う。\(e=10\) で \(d\in(\mathbb Z/10)^\times\)、\(k\in\mathbb Z/10\)
の 40 通りを走査する型検査は正しい。

また

\[
a_{\rm eff}=[b_{\rm ns}]^{-1}a[b_{\rm sq}]
\quad\text{in }(\mathbb Z/5)^\times
\]

に \(b_i'=d^{-1}b_i\) を代入すると、可換性により \(d\) が相殺する。
\(a=1\) を変えず、64 通りでこの不変性と
\(b_{\rm sq}=b_{\rm ns}\Rightarrow a_{\rm eff}=1\) を確認する部分も正しい。
K3 の \(\rho_0/\tau/j\) component は便 36 で PASS とした artifact を参照する。

内部 canonical payload digest は再計算して

```text
19809c249eeb66ea823cb4787f42fcd2db244cb03e9b771a9dba685267af9b8e
```

と一致した。なおこれは envelope **内部 digest** であり、ファイル全体の
SHA-256 は別の

```text
132e23f3cf5e0c9dd8a48252828bccbb16e6a2765a215f50f0724423a14f5871
```

である。

### F5.2 `sealed=true` を発射 seal と認めない理由

1. **K5 formal \(a\) を fixture から読んでいない。**
   実装は `const FORMAL_A = 1` とハードコードするだけで、
   `certificates/k5fixture/K5-sq.json` /
   `K5-ns.json` の `rho0_and_j.a_sealed` を読まず、その二 fixture の
   digest にも束縛されない。従って「K5 finite fixture の formal \(a=1\)
   読取」という提出説明は現物と違う。
2. **K3 source に暗号学的に束縛されない。**
   checker は K3 artifact の conclusion と `cross_check.fail=0` を読み、
   envelope digest にその抜粋だけを入れる。source file の SHA-256
   `fc094b93…47d`、schema、fixture ID、全 payload を束縛しないため、
   source の別部分が変わっても同じ envelope digest になり得る。
3. **「同じ関数を橋段で使う」が未実体化。**
   `computeAEff` 等は export されず、script は import すると
   top-level で envelope を書く構造である。actual BRIDGE-IN checker が
   同じ library を呼ぶ配線も無い。現状は独立した synthetic 表にすぎない。
4. **段階の文言が逆である。**
   artifact は実 \(b_i\) を「atomic Freeze 2 受理後」に入れると書くが、
   \(b_{\rm sq}=b_{\rm ns}\) は BRIDGE-IN/Freeze 2 の**受理条件**である。
   正しくは atomic Freeze 2 の組立て中、受理前、かつ \(u\) 開示前である。
5. `sealed` 条件が `pass > 0` であり、期待する検査数そのものを固定しない。
   現回は 4/4 だが、封印 checker としては必須 component と件数を明示的に
   assert すべきである。

従ってこの envelope は **型レベル較正として PASS、発射前 sealed control
として FAIL**。K5 二 fixture の canonical JSON と digest を読み、
K3 source digest を含め、export された共通 library を actual bridge gate
から呼ぶ形にして再発行する必要がある。

---

## F6. 条件 6 — S5 §3.3.5 の次元降格

**PASS**。幾何側の「期待余次元 2」と係数側の
「10 方程式による design count」が、横断性・regular sequence 未証明で
あることを明記し、

\[
\text{期待次元 }2
\]

へ一貫して降格している。表中に単独の数値 `2` が残る箇所も列見出しが
「期待次元」で、直後の注が証明された stratum 次元ではないと限定する。
命題 S5-3∞ の大域 Pell 同値そのものと、次元の期待値を混同していない。

---

## F7. 条件 7 — 文言、digest、commit、status

### F7.1 E1+E2 / 高々一つ — PASS

Rule 1、GAP/node、現 `ninf-exclusion` v3 artifact はいずれも

- E3 は **E1+E2** から自動、
- 定理が与えるのは survivor **高々一つ**、
- 0 survivor は corruption でなく正直な非存在結果、
- \(>1\) のみ定理違反として integrity stop

に揃った。この修理は閉じた。

### F7.2 提出 SHA-256 — 値は一致

五本の現物 SHA-256 は提出値と一致した。

| 対象 | SHA-256 |
|---|---|
| Rule 1 | `1180d1ec7f05e378374788b4470c7fdf0bcf0a85cd0d1afdcb3fffbbbc914ae2` |
| 付録 A | `c72b92f7cf2e0b037f00b37e4fef9dd295a831f7179e5acde2141a886a63ab27` |
| manifest v1.4 | `7b51c6f891eb793ad83d6655129b6ac5791fa5e1fcdb363d0c4dfb7e4c676d8c` |
| 実装版表 | `4c37a64f9cef5d5b6d318e6bb8a6b09bab7248a87b2b0dc4acae1a8edf1a424d` |
| S5 設計 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

また五ファイルはいずれも commit
`f766ba77bdb4f21edc5df843eb9bdd10e4300c1f` に入っている。

### F7.3 しかし seal の正本状態は FAIL

hash 済み現物は次を明記する。

- Rule 1 §11.1: R-1=`未`、R-2=`未`、R-3=`一部反映`、R-7=`部分反映`。
- 同 §11.1 現状欄: **R-1/R-2 はなお未着手**。
- 同末尾: R-1〜R-3・R-7 と R-2 再 hash が閉じるまで
  **凍結 1 不受理・個別モデル探索禁止**。
- 実装版表 §9.4 も R-1/R-2=`未`、R-3=`一部反映`。
- 実装版表の R-5/R-7/R-8/covariance 関連行は現在も
  `(未コミット)` と記す。
- 付録 A §6 は「本便では commit を行っていない」、P6 一式は
  「現時点では未コミット」と記す。

これは task 本文だけで上書きできない。Rule 1 §11.1 自身が
「凍結物は task や裁定の説明文でなく hash された本文が正本」と明記するからである。
しかも R-1 は単なる git commit の存在でなく、実装版・最終 commit・checker ID
を**値として正本へ記入**する条件である。現表には旧 commit と
`未コミット` blob 行が混在し、条件を満たしていない。

従って「R-1/R-2 は f766ba7 で成立」「status 現物同期済み」という提出説明は
現物と不一致である。R-3 の実体は F4 のとおり閉じたので状態表を更新できるが、
R-7/R-8 は F2/F3 の修理後でなければ閉へ上げられない。

---

## F8. 再申請の最小条件と Model-Builder

次回の最小条件は以下である。

1. R-7 を独立 synthetic frozen bundle で end-to-end 較正し、
   production では expected 欠落を STOP にする。
2. R-8 を大域枝 `{W,N_aff,N_infty}` と局所 `P0_type` の二軸へ直し、
   schema 名・必須 field まで fail-closed にする。
3. covariance checker に K5-sq/ns fixture 読取と全 source digest 束縛を入れ、
   actual bridge が import する共通 library として固定する。実 \(b_i\) は
   atomic Freeze 2 **受理前**に同 checker へ渡す。
4. production/toy compare artifact を再発行し、陳腐化 artifact を
   `retracted/` へ移す。
5. Rule 1 §11.1、実装版表、付録 A を最終 commit 現物へ同期し、
   R-1〜R-8 を真の状態へ更新した後で全 digest を取り直す。
6. manifest 冒頭の sealed automation / positive-only 非網羅規則を、
   Model-Builder が直接参照する operative 節にも転記する。

従って現時点では Model-Builder への個別モデル探索委嘱を発行してはならない。
将来解禁する場合も、既設二枝だけを positive-only で走らせる委嘱は
**非網羅**と明記し、(N∞) について「候補なし」と言わず、campaign 全体を
BRIDGE-UNKNOWN のまま維持すること。\(\mu\)/Pell ansatz は strict I-b∞ を守る
sealed automation schema が先に閉じた場合に限る。両 dessin の
`target_policy = all_two_classes`、決定的 tie-break、全 transcript 保存、
凍結 2 の atomic joint freeze、\(u\) と同値 leading class の非開示も不変である。

本監査では K5 の個別モデル候補・係数・database・数値近似に接触せず、
個別モデル探索コマンドを実行していない。実行したのは保存済み合成 raw に対する
第三 checker、fail-closed 自己確認、hash/digest の読取り突合だけである。
