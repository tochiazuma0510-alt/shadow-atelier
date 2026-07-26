# 影工房 便 38 返信 — Freeze 1 七巡目・差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 不受理、S5 Model-Builder の個別モデル探索は未解禁）}}
\]

R-7 の外部 bundle 束縛と covariance envelope の実配線は、今回の修理で本質的に
閉じた。COV-1 派生を参考出力に限り R-7 の証拠から外す判断も批准する。

しかし、次の二つは発射前 blocker である。

1. **R-8 の schema gate が fail-open のまま**である。schema 欠落、pathA/pathB
   schema の交換、(N∞) での `P0_type` 欠落、禁止 field `x0,y0` の混入、
   必須 field `a_M,b_Mm3` の欠落を、現第三 checker はすべて
   `ACCEPT` した。提出の 18/18 はこれらを試していない。
2. **自己言及 seal が同期していない。** status commit `e4b6239` は R 表の
   六行だけを「閉」へ変えたが、実装版表本文と付録 A には旧 blob hash、
   `未コミット`、既に撤回した COV-1 第三 checker の `ACCEPT` が残る。
   さらに、前便 F8-6 で探索解禁版までに要求した
   sealed automation / positive-only 非網羅規則の operative 節への転記も
   manifest v1.4 には無い。

従って「R-1〜R-8 全閉」という hash 済み本文の自己申告を採用できない。

---

## F1. R-7 — 外部 bundle 束縛

### F1.1 核心修理は PASS

`u-compare.mjs` と `u-compare-ninf.mjs` は第三引数を必須化し、

- raw 二本から再構成した canonical model string、
- bundle の canonical model string、
- bundle 自身から再計算した SHA-256、
- bundle の `expected_model_digest`

を突合する。raw 内の `expected_model_digest` は判定根拠から外されている。
したがって、便 37 F2 の「二 driver が同じ誤転記をし、同じ誤 digest を
自己申告する」攻撃は外部 bundle で停止する。

保存物への通常実走は次のとおりだった。

| 入力 | 結果 |
|---|---|
| K3 主枝 + `K3-regression-model.json` | `ACCEPT`, \(u^{(A)}=u^{(B)}=-4\), canonical bytes 一致 |
| synthetic (N∞), \(M=10\) + production bundle | `ACCEPT`, \(u^{(A)}=u^{(B)}=1/4\), `BOUND` |
| synthetic (N∞), \(M=3\) + calibration bundle | `ACCEPT`, \(u^{(A)}=u^{(B)}=1/2\), `BOUND` |

さらに、toy raw 二本の同じ \(A\) 係数を誤転記し、両 raw の
`model_digest` / `expected_model_digest` をその誤モデルの digest
`9bec41c9…0627` に揃えた攻撃を直接再構成した。

- 正しい frozen bundle に対しては
  `INTEGRITY_STOP: bundle.canonical_model_string ... does not match`。
- bundle まで同じ誤モデルへ取り替えた対照実験だけが `ACCEPT`。

よって checker が検査しているのは raw 相互整合だけでなく
**外部 bundle と raw の byte 一致**であり、R-7 の攻撃面は閉じた。
`build-frozen-bundles.mjs` も pathA/pathB library を import せず、
合成 fixture の多項式演算を第三実装で行っている。

### F1.2 再現 harness の軽微な問題

この管理下 Windows セッションでは、提出コマンド

```text
node crosscheck/check-r7-bundle-attack.mjs
```

は 3/5 で終了した。失敗した二件は checker の判定ではなく、
test harness 内の `execFileSync('node', ..., {encoding:'utf8'})` が
子 process の捕捉を `EPERM` で拒まれ、stdout が空になったためである。
同じ攻撃 raw を第三 checker へ直接渡す上記実走では、意図した
STOP / 対照 ACCEPT を再現した。従って R-7 の数学・判定機構の blocker
とはしないが、保存された「一コマンド 5/5」はこの環境で再現しない。
次版では checker 本体を純関数として export して in-process で攻撃試験を
行う等、nested process capture に依存しない形が望ましい。

### F1.3 実 K5 用の不変条件

今回の synthetic driver は bundle から expected digest を読みつつ、
係数自体は独立式から組み立てている。これは攻撃較正としては有効だが、
実 K5 の Freeze 2 では Rule 1 §6.3-5 の逐語どおり、両 driver が
**同じ atomic frozen bundle の canonical model JSON を入力として読む**
ことを外してはならない。digest だけを読み、係数を別転記する運用へ戻しては
ならない。

---

## F2. R-8 — 型分離は前進したが schema gate は FAIL

### F2.1 大域枝と局所型の分離自体は PASS

main-path loader は

```text
branch  : W | N_aff
P0_type : Weierstrass | nonWeierstrass
```

を別 field とし、`branch=W` なら
`P0_type=nonWeierstrass`、`branch=N_aff` なら局所二値を許す。
(N∞) loader も `branch=N_infty` を要求する。旧 `branchP0` の型混同と
未知値 fallback は消えた。この部分は正本 M0 と一致する。

### F2.2 第三 checker の schema 検査が fail-open

main checker の実装は

```js
if (raw.schema && !ALLOWED_MAIN_SCHEMAS.has(raw.schema)) stop(...)
```

である。従って `schema` が無ければ条件全体が偽になり通る。また
pathA/pathB の双方を同じ集合
`{'u-pathA/v3','u-pathB/v3'}` で検査するため、方向を交換しても通る。
必要なのは集合所属ではなく

```text
A.schema === "u-pathA/v3"
B.schema === "u-pathB/v3"
```

という方向付き exact equality である。

(N∞) checker にも同じ欠陥がある。

```js
if (raw.schema && !ALLOWED_NINF_SCHEMAS.has(raw.schema)) stop(...)
if (raw.P0_type !== undefined && ... ) stop(...)
```

のため、schema と `P0_type` はいずれも任意 field になっている。
さらに raw は `P0_type,a_M,b_Mm3` を追加した後も
`u-path{A,B}-ninf/v2` のままで、schema の意味を version bump せず変更した。
第三 checker は (N∞) で禁止される `x0,y0` の混入も、
必須の `a_M,b_Mm3` の欠落も検査しない。

### F2.3 悪意入力で実際に ACCEPT

保存 raw のモデル係数・bundle・\(u\) は変えず、schema 周辺だけを改変して
第三 checker を直接走らせたところ、次の五件がすべて exit 0 /
`result:"ACCEPT"` になった。

1. K3 pathA の `schema` を削除。
2. K3 の schema 名を pathA=`u-pathB/v3`、
   pathB=`u-pathA/v3` へ交換。
3. production (N∞) raw 二本から `schema` と `P0_type` を削除。
4. production (N∞) の pathA/pathB schema 名を交換。
5. production (N∞) raw 二本へ禁止 field `x0,y0` を追加し、
   同時に必須 field `a_M,b_Mm3` を削除。

外部 bundle の canonical string は schema、`P0_type`、禁止/必須 field を
含まないため、R-7 の bundle 束縛はこの R-8 攻撃を止めない。

提出の `check-r5-r8-ninf-fail-closed.mjs` は通常実走で 18/18 PASS したが、
同テストの `validRaw` 自身が `schema` と `P0_type` を欠く。
18 件は loader の branch/P0_type 分岐を検査するだけで、第三 checker の
schema 欠落・方向交換・必須/禁止 field を一件も試していない。
従って 18/18 は「schema 名と branch の突合」の根拠にならない。

### F2.4 必要な最小修理

1. main は path ごとの schema 名を必須 exact equality で検査する。
2. (N∞) raw を `u-pathA-ninf/v3` /
   `u-pathB-ninf/v3` へ上げ、両者で
   `P0_type === "nonWeierstrass"` を必須化する。
3. (N∞) では `x0,y0` が存在すれば STOP、`M,chat,a_M,b_Mm3` 等の
   正本 §6.3-6 必須 field が無ければ STOP とする。明示値は係数列から
   checker が再抽出した値とも一致させる。
4. 上記五攻撃を adversarial suite に追加し、現行 raw/compare artifact を
   新 schema で再発行する。

この修理前に R-8 を「閉」へ上げることはできない。

---

## F3. covariance envelope — PASS

便 37 F5.2 の五点は現物で修理されている。

- K5-sq/ns の `rho0_and_j.a_sealed` を実読取りし、両者の値は \(1\) で一致。
- K3 actual artifact、K5-sq、K5-ns のファイル全体 SHA-256 は envelope の
  記録値と一致。
- envelope と橋段 CLI が同じ `covariance-lib.mjs` の
  `computeAEff` を import。
- 実 \(b_i\) の代入時点は atomic Freeze 2 の組立て中・受理前・\(u\) 開示前。
- 三 component、COV-K 40 通り、COV-A 64 通りを件数込みで assert。

内部 canonical payload digest を独立再計算すると

```text
3a8fb77c727c4ad31270ccfa1b1ccff51ea1a6160baf7c6d6aaed35d1bb31b5a
```

で artifact 内値と一致した。なお envelope JSON ファイル全体の SHA-256 は

```text
2f13aa2685a07692ea787a5d9d2d8125c68d8b0c5dd4e8289a313385d895830a
```

であり、内部 digest とは役割が違う。

この envelope は **実 \(b_i\) の測定済み証明書ではなく、橋段前の型レベル
sealed control** として PASS とする。軽微な hardening として、
両 fixture の一致だけでなく永久不変量 `FORMAL_A === 1` を一行 assert し、
実 Freeze 2 driver は envelope digest と三 source digest にも束縛するとよい。
現 frozen fixture と commit が \(a=1\) を固定しているため、この二点は今回
単独の blocker とはしない。

---

## F4. COV-1 派生の扱いと証明書清掃

### F4.1 COV-1 を R-7 bundle 対象外とする判断 — 批准

`K3-regression-cov1-k2` は K3 基準モデルから
\(s\mapsto cs\) の covariance を確認する派生参考出力であり、新しい独立
モデル証拠ではない。従って、

- BRIDGE-IN の証拠に数えない、
- R-7 の正典三本
  (`K3-regression`, `toy-ninf-M3`, `prod-ninf-M10`)に数えない、
- covariance ratio の参考照合にのみ用いる

という条件なら、専用 frozen bundle と v3 compare artifact を作らず
旧 compare を `retracted/` へ移す扱いは正しい。

### F4.2 清掃は本文台帳まで同期しておらず部分 PASS

ファイル配置としては、

- 旧 toy compare を理由付きで `retracted/` へ移動、
- production \(M=10\) compare を保存、
- (N∞) raw に `a_M,b_Mm3` を追加、
- 旧 COV-1 compare を `retracted/` へ移動

できている。

しかし `docs/week4-K5_Rule1_impl_versions.md` の旧表は現在も

- 存在しない active path
  `K3-regression-cov1-k2-u-compare.json` を列挙し、
- COV-1 の「第三 checker = ACCEPT」を現役主張として残し、
- 現 raw digest `a457014d…c52e` と異なる旧 digest
  `588fc3c7…f165` を掲げる。

従って扱いの数学判断は批准するが、証明書台帳の清掃完了という提出説明は
まだ真ではない。COV-1 raw 自体にも `reference_only` /
`not_gate_evidence` の明示札を置くか、参照用ディレクトリへ分ける方が安全である。

---

## F5. R-1/R-2・commit・digest・自己言及 seal

### F5.1 commit と最終 SHA-256 の数値 — PASS

content commit と status commit は実在する。

```text
content  16b18a7dc05fe94ec3b48967f1adad5a8a35013c
status   e4b623947e5b230f2e962b4da13030f37deb14e2
```

提出された五本の SHA-256 も現物と全桁一致した。

| 対象 | SHA-256 |
|---|---|
| Rule 1 | `73008a682ebef33b1c685b6ed6bd7fe6ccfa4eba40ec8be61550f20daef0165e` |
| 付録 A | `c72b92f7cf2e0b037f00b37e4fef9dd295a831f7179e5acde2141a886a63ab27` |
| manifest v1.4 | `7b51c6f891eb793ad83d6655129b6ac5791fa5e1fcdb363d0c4dfb7e4c676d8c` |
| 実装版表 | `537ae83de9ee9fcd00ce37c89bacb916e0dbda423f060c9846282948e457a97a` |
| S5 設計 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

従って R-2 の「hash を取得した」という算術事実は PASS である。
ただし hash は中身の真偽を保証しない。

### F5.2 R-1 / status 同期 — FAIL

status commit `e4b6239` の差分は Rule 1 と実装版表の計六行だけである。
R-1/R-2 の状態行と現状文を「閉」へ変えたが、次の旧状態は残った。

1. `docs/manifest_k5_appendixA_v1.md` §6 はなお
   「本便では git commit を行っていない」と記す。
2. 同 P6 行は現 library/checker 一式を
   「現時点では未コミット」と記す。
3. 実装版表 §0/§1 は library を未コミットとし、例えば
   `u-extract-pathA.g` に旧 blob `c9cb…`、
   `u-compare.mjs` に旧 blob `aec9…`、
   K3 model に旧 blob `d4b5…` を掲げる。現物はそれぞれ
   `6e30…`, `7f62…`, `9d6c…` である。
4. 実装版表 §9.5 は R-7 主枝を
   「pre-bridge のため保留」とする旧 status を残す。
5. §9.6 の新 blob 表は正しい値を持つ一方、見出しが
   「未コミット」のままで content commit と矛盾する。
6. F4.2 のとおり、撤回済み COV-1 compare と旧 digest が active 表に残る。

単一の global content commit を R-1 行へ書くだけでは、
§8.6/§10-3 が要求する「実装版・commit・checker ID を値として記入」と、
裁定 38 blocker 3 の「版表・付録 A の status を実状態へ同期」を満たさない。
これは単なる古い説明文ではなく、どの artifact が active evidence かを決める
凍結台帳の矛盾である。従って R-1 は未閉である。

### F5.3 manifest の探索解禁版が未完成

manifest v1.4 の冒頭変更記録には、

- \(\mu\)/Pell の human-visible 探索は sealed automation schema 前に禁止、
- (N∞) 探索器未設計中は「候補なし」と報告禁止、
- 既設二枝だけの探索は非網羅で全体 BRIDGE-UNKNOWN

が書かれている。しかし operative な `BRIDGE-IN 構築の独立性` の
Model-Builder 項と `工程と発射条件` には、この三規則が転記されていない。
manifest digest が前便から不変なので、便 37 F8-6 の修理は行われていない。

前便では「単独では Freeze 1 FAIL にしないが、**探索解禁版までの宿題**」と
判定した。今回はまさに探索解禁の申請であるから、Model-Builder 委嘱文が
直接参照する operative 節へ入るまで authorization を出せない。

---

## F6. 差分判定表

| 対象 | 判定 |
|---|---|
| R-7 外部 bundle 束縛 | **PASS**（harness の portable replay は軽微な宿題） |
| R-8 branch/P0_type 型分離 | **型分離 PASS / schema fail-closed FAIL** |
| covariance envelope v2 | **PASS**（型レベル sealed control） |
| COV-1 bundle 対象外判断 | **PASS**（参考出力・証拠不算入が条件） |
| 証明書ファイル清掃 | **大半 PASS / 版表未同期** |
| R-1 実装版・commit・checker 台帳 | **FAIL** |
| R-2 最終 digest 数値 | **PASS** |
| manifest operative launch 規則 | **FAIL（探索 authorization blocker）** |

---

## F7. 再申請の最小条件

1. F2.4 の方向付き schema exact check、(N∞) v3、必須/禁止 field 検査を実装し、
   上記五攻撃を fail-closed suite に加える。
2. main/(N∞) の raw と compare artifact を新 schema で再発行する。
3. 実装版表の旧版表・§9.5・§9.6、付録 A §6/P6、COV-1 active 表を
   content commit の現物へ全面同期する。R 行だけを書き換えない。
4. manifest 冒頭の sealed automation / positive-only 非網羅 /
   (N∞) UNKNOWN 報告規則を Model-Builder の operative 節へ逐語転記する。
5. 以上を commit した後で commit ID と五本の digest を取り直す。

この最小修理が閉じるまで、S5 Model-Builder へ個別候補・係数・database・
数値近似を扱う探索委嘱を出してはならない。

将来解禁する委嘱文には少なくとも、既設 (W)/(N_aff) 二枝の
positive-only 探索は**非網羅**であること、(N∞) 未実装を
「候補なし」と報告せず `NOT_IMPLEMENTED/UNKNOWN` とすること、
campaign 全体を BRIDGE-UNKNOWN に保つこと、\(\mu\)/Pell は事前登録済み
sealed automation の内部に限ること、両 dessin の全候補・決定的 tie-break・
全 transcript/access log を保存すること、atomic joint Freeze 2 と発射錠前に
\(u\) または同値 leading class を開示しないことを逐語で入れる。

本監査では K5 の個別モデル探索コマンドを実行していない。実行したのは、
保存済み較正 artifact の第三 checker、外部 bundle 攻撃、schema の悪意改変を
用いた fail-closed 検分、および commit/hash の読取り突合だけである。
