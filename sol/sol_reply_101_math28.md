# 便 101 返信 — 数学便第 28 号・全面再検問

## 総合判定

**条件付き PASS。**　最優先二件のうち、HS の NW-1/DUM-HEX と SURJ 訂正は通り、**発火条件 2 の \(p=7\) 構造確認走行だけを下記の修正済み IF-FIRST 契約で認可する**。M-7 の required-set 修理も再実走を含め **PASS**、W6KEY 二 plane の adoption consumer を最終批准する。

ただし self-hash v3 + 台帳 v1.5 束は無条件批准できない。現 v3 の参照値そのものは一致しているが、(i) v3 が `ledger_version = conventions_ledger_v1_4` を宣言したまま v1.5 の新型 `sha256_ref` を使う、(ii) 台帳 CL-9 が実在する checker を「未実装」と記す、(iii) checker が全 `sha256_ref` を走査せず path の同一性にも fail-open を残す、(iv) MANIFEST に W100-4.1 が禁じた fixed-point 不可能断定が current erratum なしで残る、という四件を捕獲した。過去 file は編集せず、v4/checker v2/台帳次版で閉じること。

| 対象 | 判定 |
|---|---|
| NW-1a/NW-1b・HSP-GAP-1 | **PASS / CLOSED（紙）** |
| DUM-FIN・DUM-HEX・DUM-1/p | **PASS**（DUM-1/p は NW-P5 相対） |
| P100-1.1 SURJ 理由の訂正 | **訂正上申を採択**。旧理由は撤回、結論は H8′ で維持 |
| 発火条件 2 | **限定認可**。\(p=7,e=1\) の構造確認だけ。本走・shadow 掃引は未認可 |
| K5-MOD/NO-ENT(3) 修文 | **PASS** |
| self-hash v3 現物 | **手照合では整合**、ただし schema 宣言と checker contract は **差戻し** |
| 台帳 v1.5 | 配置・規範内容は **PASS**、artifact 批准は **差戻し** |
| M-7 修理 | **PASS / 最終批准** |
| Fresse Part 1 | 収蔵・番号・言明・証明本体の実在を **確認**。GAP-TRUNC-1 は OPEN |

### F101-0.1　入力・digest・検証格

便 101 を §1 から §6 の末尾まで読み、指定 11 artifact は **11/11 で記載 SHA-256 と一致**した。再実行した主なものは次のとおり。

- `hs_prop7_dumhex_check.py`: 14 検査、`FAILS = 0`。
- `ihnec_r4b_v3_selfhash_checker.py`: 現 v3 は 5 項目 PASS、`--selftest` は 1 PASS + 3 STOP。旧 v2 を直接入力すると INTEGRITY_STOP。
- `bundle-selfaudit-v12.py`: 通常 25 項目 ALL PASS。
- `bundle-selfaudit-v12.py --mutate`: M100-1..5 を含め mutation failure 0、exit 0。

これらは有限・厳密計算の再現であり、Lean の意味の verified ではない。本便で **verified は 0 件**。HS の 14 検査と Schur 乗数値は引き続き single lane である。

---

## 1. HS 修文束・NW-1・SURJ 訂正

### F101-1.1　補題 NW-1a/NW-1b

**PASS。HSP-GAP-1 を CLOSED（紙）としてよい。**

語集合を

\[
\mathcal W_{4,p}=\{[x_1,x_2,x_3,x_4,x_5],x_1^p\}
\]

のちょうど二語に固定したとき、verbal subgroup は確かに

\[
\mathcal V(G)=\gamma _5(G)G^p
\]

である。既知の直積 \(PB_3=F_2\times\langle c\rangle\) の中では

\[
\gamma _5(PB_3)=\gamma _5(F_2)\times1,\qquad
(F_2\times\langle c\rangle)^p=F_2^p\times\langle c^p\rangle.
\]

後式は \((a,1)^p\) と \((1,c)^p\) が各因子を個別に生成するためであり、従って

\[
\mathcal V(PB_3)=\mathcal V(F_2)\times\langle c^p\rangle.
\]

よって

\[
\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\qquad
\mathbf N_0=\mathcal V(F_2)\times\langle c^p\rangle
\]

は箱型で、両者の \(F_2\) との交わりは \(\mathcal V(F_2)\)。\(\mathcal V(PB_3)\) の完全不変性と \(PB_3\trianglelefteq B_3\)、および \(Z(B_3)\trianglelefteq B_3\) から両窓の \(B_3\)-正規性も従う。

ここで使った分裂は **既知の群同型 \(PB_3=F_2\times Z(B_3)\)** だけであり、未知の屋根や拡大が分裂すると仮定してはいない。この意味で罠 #5 は回避されている。

また

\[
P=F_2/(\gamma _5(F_2)F_2^p),\quad P^{ab}\cong C_p^2
\]

なので \(\bar x,\bar y\) の位数はともに \(p\)。\(\mathbf N\) では \(\bar c=1\)、\(\mathbf N_0\) では \(\operatorname{ord}(\bar c)=p\) だから、両方で

\[
N_{\rm ord}=p,\qquad |\mathcal X_N|=p-1.
\]

Witt 数からの \(|P|\le p^8\)、\(|[P,P]|\le p^6\) と、\(Q\) の \(|Q|\le p^{40}\) も上界として正しい。等号は予言であって、本項の紙証明に混ぜていない。

### F101-1.2　DUM-FIN・DUM-HEX・DUM-1/p

**PASS。**　明示語

\[
h_4=[[[x,y],x],x]\,[[[x,y],x],y]^4\,[[[x,y],y],y]\in\gamma _4(P)
\]

は Exp/Lazard を用いない有限群元である。類 \(\le4\)・指数 \(p\) の \(P\) では

\[
\gamma _4(P)=\gamma _4(P)/\gamma _5(P)\subseteq Z(P)
\]

が初等アーベルなので、最上層での群積・\(\theta,\tau\) の作用は次数付き \(\mathbb F_p\)-線型計算と exact に一致する。従って

\[
\theta(h_4)=h_4^{-1},\qquad
h_4\tau(h_4)\tau^2(h_4)=1
\]

が \(P\) 内の等式となり、\(f_t=h_4^t,m=0\) は簡約二 hexagon を exact に満たす。

同様に \(Q=K(0,5)/(\gamma _5K(0,5))K(0,5)^p\) の最上層で

\[
\mathrm{PENT}_W([0,f_t])\iff
t\,\nu _4(j\mathfrak h_4)=0.
\]

従って NW-P5、すなわち \(\nu _4(j\mathfrak h_4)\ne0\) が標的商で成立すれば、明示 family の \(p\) 元のうち \(t=0\) だけが PASS となる。「ちょうど \(1/p\)」の射程をこの family に限定した修理は完全である。

### F101-1.3　★ P100-1.1 の SURJ 理由づけ訂正

**訂正上申を全面採択する。私の旧理由は撤回する。**

\(\gamma _4(P)\subseteq Z(P)\) は \(PB_3/N\) 内の中心性であり、\(B_3/N\) 内で \(\sigma _2\) と可換することを意味しない。実際、外側の \(S_3\)-作用は

\[
\theta_*(\mathfrak h_4)=-\mathfrak h_4\ne\mathfrak h_4
\]

なので、一般に

\[
T_{0,f_t}(\sigma _2)=f_t^{-1}\sigma _2f_t\ne\sigma _2.
\]

従って「中心だから \(T_{0,f_t}\) は恒等」は偽である。

正しい根拠は既在の系 H8′。両窓の純部分商はそれぞれ \(P\)、\(P\times C_p\) という有限 \(p\)-群で、charming 条件は \(f\in[P,P]\subseteq\Phi(P)\) と \(u=2m+1\in\mathbb F_p^\times\) を与える。Frattini 商上の生成元像は可逆な \(u\) 倍なので全射であり、Prop. 3.6 により所要の SURJ と同値である。

これは \(m=0\) に限らず \(m\in\mathcal X_N\) 全体で成立する。従って本窓族では **SURJ は識別力ゼロ**であり、その PASS を detector の証拠として数えてはならない。

### F101-1.4　R-5 と PREC-1

両訂正を **PASS** とする。

- \(h_3\in\gamma _3\) は \(\gamma _3/\gamma _4\) で norm が消えるだけで、有限 class-4 窓では積が \(\gamma _4\) に残りうる。しかも代表語変更でその剰余が動く。従って exact hexagon/PENT PASS は言えず、A-HSP-2′ の「mod \(\gamma _4\) で PASS」が正形。
- 一般形は
  \[
  (1+\tau+\tau^2)(\alpha v_1+\beta v_2+\gamma v_3)
  =(2\alpha-\beta+2\gamma)(v_1+v_2+v_3).
  \]
  \(\alpha=\gamma\) 上だけで \(4\alpha-\beta\) となる。二条件の交わりが \(\mathbb Q(1,4,1)\) なので D4-POWER (a) の結論は保たれる。

### W101-1.1　IF-FIRST の S-7 は差戻し

現 S-7 の

> NW-P2 の等号が破れたら、次元の実測値で全予言を書き直す

は事後的な予言改稿であり、宇宙を変えなくても preregistration を壊す。これを本返信で次へ置換する。

> **S-7′**: NW-P2 のいずれかが不一致なら `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP` として直ちに停止する。結果を保存し、構成 bug と数学予言の偽のどちらかを別検分する。同じ run/同じ登録の中で実測次元へ予言を書き換えない。実測値を入力にした次の研究を行うなら、旧予言が外れた事実を明記した別 version の事前登録から開始する。

NW-P8 も「較正予想」であって定理ではない。これを gate として走らせるなら、\(\mathbf N\) と \(\mathbf N_0\) の不一致が一つも出なかった場合は較正失敗として停止し、後から期待値を弱めない。

### W101-1.2　DUM checker の一行 erratum

`hs_prop7_dumhex_check.py` の実コードと出力は正しく \(2a-b+2c\) を使うが、冒頭コメント (3) だけが旧式 \(4a-b\) を一般形として残している。数値結果を傷つけない文書 defect だが、次版でコメントを直すこと。現 file は記録として編集しない。

### P101-1　発火条件 2 の限定認可

**\(p=7,e=1\) の条件 2 構造確認を認可する。**　ただしこれは HS 本走の認可ではない。認可範囲は次だけである。

1. 窓は本稿の \(\mathbf N,\mathbf N_0\)、\(P,Q\) に固定し、別素数・別指数・別 verbal subgroup を混ぜない。
2. exact pc presentation から \(|P|\)、LCS 各層、\(|Q|\)、\(\dim\gamma _4(Q)\) を出す。
3. 上記の交換子語 \(h_4\) をそのまま評価して \(h_4\ne1\) を判定する。
4. \(j(h_4)\) と \(\rho\) を presentation から評価し、\(\prod_{i=0}^4\rho^i(j(h_4))\ne1\) を直接判定する。期待値をコード生成に使わない。
5. S-6、上の S-7′、NW-P8 の停止規則を cert に明記し、script/input/output/GAP version と digest を束縛する。
6. この一走の結果は single-lane candidate。通過後に初めて、探索・full \(B_3/N\) hexagon・\(K(0,5)/W\) PENT の helper 非共有三レーン（条件 4）を発注する。CV-9 前に cross-checked と呼ばない。

条件 2 が通っても許可されるのは次段の実装設計までであり、shadow 全掃引、\(p=11,13\) への拡張、FV-WALL 解凍は許可しない。

---

## 2. K5-MOD・NO-ENT(3)

### F101-2.1　K5-MOD §A.13

**PASS。**　便 100 の射程修理は保持されている。

- \(62{,}500\) は elementary-5 kernel class 内だけの下界で、一般 W-6 の最小位数は UNKNOWN。
- \(\mathbb F_3\) 上の \(S_4\) 標準三次元 module は kernel order \(27\)、群位数 \(13{,}500\) の **module candidate** を与えるが、\(K^{(5)}/N\) としての実現性は未証明。従ってこれは一般下界そのものの反例ではなく、表現論だけで \(62{,}500\) を一般化する推論への反例である。
- EQUIV は固定 \(\widehat G_5\)-module 上の extension equivalence までであり、marked subgroup \(N\) の一意復元ではない。
- K5-1/K5-2 の二つが cert-read 例外であるとの erratum、および K5-GAP-6（他素数・非初等核）と既存 2-primary GAP の分離は妥当。

### F101-2.2　NO-ENT(3) §10

**PASS。登録文を批准する。**　証明の正順は

\[
S_3\text{-不変作用}\Rightarrow\text{自明作用}
\Rightarrow H^2=0\text{ で split},\ H^1=0\text{ で補群一意}
\Rightarrow\Gamma=Z\times C\Rightarrow C\trianglelefteq\Gamma
\Rightarrow B_3\text{-安定}
\]

であり、正規性と外側 \(B_3\)-安定性の根拠を混同していない。射程は「\(N'\trianglelefteq B_3\)、\(N'\subseteq K^{(3)}\)、指数 3」に固定する。Schur multiplier `[2]` は論法の異なる single-lane 裏取りに留める。

---

## 3. self-hash v3・規約台帳 v1.5

### F101-3.1　現 v3 の instance-level 整合

現物の三つの `sha256_ref` は同じ実在 JSON holder と pointer を指し、holder の path と digest は対象 v3 の bytes に一致した。`current` と `effective_source` も一致し、MANIFEST 差分は既存 v2 記録の意味内容を変えず v3 entry/addendum を加える形である。従って **現 v3 の参照値それ自体に改竄・不一致はない**。

### W101-3.1　v3 の ledger version drift

しかし v3 の

```json
"ledger_version": "conventions_ledger_v1_4"
```

は、その同じ block が v1.5 で初めて定義された `sha256_ref` を使うことと両立しない。P100-4.1 を散文で参照しても schema version の型不一致は消えない。**v3 は記録として不改変**とし、v4 で `conventions_ledger_v1_5`（またはその後継版）を宣言すること。

### W101-3.2　台帳 v1.5 の CL-9 は現況と矛盾

台帳 §1.7、live schema、positive/negative fixture、\(\mathfrak h_3/\mathfrak h_4\) の配置は妥当で、H1・改訂履歴・live `ledger_version` の同期もできている。

一方、末尾 **CL-9** は「5 検査 checker の実装が存在しない・未実装」と断言する。checker は同じ納品束に実在し、実走も可能であるため、この文は現在の artifact 内で偽。台帳 v1.5 artifact はこのままでは最終批准しない。

### W101-3.3　checker は全 `sha256_ref` に fail-closed ではない

現 checker の positive run が PASS することと、resolver contract が完全であることは別である。source を読むと次の穴がある。

1. v3 には `sha256_ref` が三つあるが、checker が解決するのは `role=current` と `effective_source` の二つだけ。旧 erratum entry の `superseded_by.sha256_ref` は走査されない。
2. (v) は `current.path == effective_source.path` しか見ず、両方が **実際に入力された cert path と一致すること**を見ない。両 path を同じ偽値へ変えて holder を正しく保てば、この条件は通りうる。
3. 同一 entry に `sha256` と `sha256_ref` を併記した排他型違反を拒否しない。
4. selftest の負例は holder 欠落、target 違い、bytes 違いだけで、64-hex 型、current/effective 不一致、上記の未走査 ref/path/XOR を発火させていない。

現 v3 ではこれらの値を手で照合して全て正しいことを確認したが、**checker が一般にそれを保証するとの主張は FAIL**である。

### W101-3.4　MANIFEST に旧 fixed-point 断定が live のまま残る

MANIFEST の `known_deviation_disclosed` は今も「後継 artifact が自己 SHA-256 を自己 bytes に含むことは**構造的に不可能**」と書く。これは W100-4.1 が退けた数学的過剰主張であり、正形は「通常の生成・再現手順では解けず、運用 schema として禁止」である。歴史文を byte 保存すること自体はよいが、今回の `w100_4_1_addendum` は placeholder の失効しか明記せず、この理由づけを明示撤回していない。次の versioned addendum で旧文を historical claim と指定し、正しい限定文を current erratum として置くこと。

### P101-3　再提出条件

1. v3 を編集せず、ledger 宣言を同期した v4 supplement を出す。
2. checker v2 は cert 内の全 `sha256_ref`（nested `superseded_by` を含む）を列挙し、各々に (i)–(iv) を適用する。
3. `current.path = effective_source.path = 実入力 cert の repo-relative path` と、`sha256` XOR `sha256_ref` を強制する。
4. 上の各述語について一変異一発火の負例を置く。
5. 台帳次版で CL-9 を CLOSED にし、checker path/digest、実走結果、未実装事項が残るならその正確な範囲を記す。
6. MANIFEST の fixed-point 不可能断定を、旧記録を消さず current addendum で撤回・限定する。

この束が閉じるまで「v3 + 台帳 v1.5 を批准済み」「fail-closed resolver 完備」とは記帳しない。採択してよいのは **self-digest を CV-10 §1.7 に置く設計判断**と **\(\mathfrak h_3/\mathfrak h_4\) を用語規約に置く判断**までである。

---

## 4. M-7 required-set 修理

### F101-4.1　P100-5.1 の逐条検収

**PASS。便 100 の blocker は閉じた。**

- required map は receipt を読む前に consumer 側で固定されている。
- 必須集合は spec v20、contract v15、manifest v15、selfaudit v11 のちょうど四対象。receipt の `authorized_scope` を黙って縮めない。
- `bound_artifacts` は path 一意 map となり、missing/duplicate/unexpected の全てを FAIL にする。supporting material は binding 欄と分離。
- 必須各項で local digest、receipt digest、receipt artifact_id、local structural artifact_id が一致する。
- freeze triple は local 三文書の digest から再計算され、receipt_id/freeze_id の形と digest 64-lowercase-hex 型を検査する。
- marker regex は `[a-z0-9_]+`、7 plane と新二 plane の四 source を列挙する。
- coverage 欠品と required-set の実 fail-open を v12 header で別事故として記帳している。

### F101-4.2　実走結果

`bundle-selfaudit-v12.py` の check 25 は実 consumer に対して次を返した。

| fixture | verdict |
|---|---|
| 無変異 receipt | `ADOPTED` |
| 必須一件欠品 | `FAIL` |
| path 重複 | `FAIL` |
| artifact_id 改変 | `FAIL` |
| digest 改変 | `FAIL` |

`--mutate` でも M100-1..5 は全て退行を捕捉した。実 witness を consumer に通すと payload-era matrix は `ok=true`、W6KEY 二 plane は `ADOPTED/PASS`、missing/duplicate/unexpected は全て空である。

CI receipt の commit `0597903686f95d1ea3eb5abca38b2e47507e215e` は local object として実在し、`suites_status=0`、7 plane PASS、`ep_status=uncalibrated/UNKNOWN`、`calibrated_detector=false` を保持する。`overall_full=INTEGRITY_STOP` は R1/R2 の既知 MALFORMED を正直に残した結果で、M-7 failure ではない。

### W101-4.1　「11 suite・1210」の provenance

ローカル保存 log では、9 regression suite に selfaudit v11/v12 を加えた 11 本について **PASS 行 1210** を再集計できた。二つの `FAIL | META-1` 行は意図的 false が footer/exit contract に伝播することを検査する fixture で、suite verdict は exit 0 である。

ただし CI receipt 自身が束縛するのは 9 suite の `suites_status=0` であり、検査本数 1210 は意図的に receipt に含まれない。RC-2 に従い、1210 を恒久記帳で引用するなら suite log の versioned path、SHA-256、実行コマンド、日時・実行系を別 provenance として束縛すること。これは M-7 修理の合否を変えない NOTE である。

### P101-4　最終批准と次版 move

**M-7 adoption consumer と W6KEY 二 plane の採用を最終批准する。**　次の freeze receipt が selfaudit v12 を束縛するときは、旧 receipt を編集せず新 receipt を発行し、consumer の required map の v11 literal を v12 へ同一 versioned move で更新する。この二変更の片方だけを先行させない。

本批准が動かさない札は次のとおり。

- AGGREGATE plane: closed。
- IMAGE-MU: UNKNOWN。
- W-6: OPEN。
- EP: uncalibrated/UNKNOWN、非発効。
- positive-control event、candidate acceptance、Freeze 2: 未認可。

---

## 5. Fresse Part 1 刊行版

### F101-5.1　収蔵・番号・現物

PDF digest は記載値と一致した。ページ画像で、PDF 物理頁 259–261（刊行頁 212–214）に **Theorem 6.2.4** の (a) と (b)(c)、pentagon/hexagon coherence、unitary extension と strict unit 条件、および証明開始が存在することを確認した。PDF 物理頁 265（刊行頁 218）には証明終端と **Lemma 6.2.5** およびその証明が実在する。

従って「Part 2 manuscript の番号だけを引用していた」という bibliography drift は閉じ、2008 Thm A.1 から刊行版 Fresse I.6.2.4 への原典 pin を採用してよい。

### W101-5.1　GAP-TRUNC-1 は閉じない

今回は刊行版の言明・番号・証明本体の実在確認であり、truncated/full operad への適用に必要な証明全体の精読ではない。従って **GAP-TRUNC-1 は OPEN**、TRUNC-PAIR や U-10/FAKE-KILL の格は上げない。

---

## 6. 情報共有と最終記帳

### F101-6.1　§6 の受領

§6 は監査対象外として末尾まで受領した。PackageGT、便 100 で済んだ fixture/27–30 訂正、既存 seal の状態を本便で再昇格しない。

### P101-6　直ちに記帳してよいもの

1. NW-1a/NW-1b と HSP-GAP-1 CLOSED（紙）。
2. DUM-FIN/DUM-HEX、および NW-P5 相対の DUM-1/p。
3. P100-1.1 の理由づけ撤回と、H8′ による SURJ 自動・本窓族で識別力ゼロ。
4. R-5/PREC-1 の訂正。
5. K5 §A.13 と NO-ENT(3) §10 の修文批准。
6. M-7 blocker CLOSED、W6KEY 二 plane adoption PASS。
7. Fresse I.6.2.4/Lemma 6.2.5 の刊行版 pin。

### W101-6　閉じるまで昇格しないもの

1. self-hash v3/checker/台帳 v1.5 束の最終批准。
2. HS 条件 2 の計算結果、三レーン cross-check、CV-9、本 shadow 掃引。
3. 一般 W-6 の \(62{,}500\) 下界、W-6 closure、IMAGE-MU、EP 発効、Freeze 2。
4. GAP-TRUNC-1。
