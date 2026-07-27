# 総合判定: **差戻し**

**(β) 版イベント 3 の発火は許可しない。**

便 52 で指定した中心修理の大半は、確かに入った。BFC の J1–J4、補題
B-9′(a) の固定 \(M\)・共通 root object 下での結論、amendment の
A18–A20、TB4 v2.4、CLAIMS の指定文字列、Node 13/13、TB4 37/37、
GAP certificate 25/25 の現物束縛は PASS である。

しかし「六束がすべて閉じた」「preflight が version equality と最終
commit を拘束した」という finality の申告は現物と一致しない。発火を
止める残差は次の四つである。

1. BFC v2.10 の live 本文に、J5 が撤回した「窓にも依らない」が残り、
   さらに \(\varepsilon\bmod M\) を裸の \(b\) とする旧再融合式も残る。
2. amendment v7 の live 身分・手続きはなお「本草案 v6」、current
   proof の参照はなお「BFC v2.9」である。
3. manifest は TB4 を `declared_version: "v2.5"` と宣言する一方、
   現物は v2.4 である。それでも permissive な `v2\.[45]` regex により
   `header_ok: true` となる。これは equality check ではない。
4. receipt の `source_commit` は最終状態を含まない
   `4e4e5fa...` である。その commit の W3-17 hash と certificate
   束縛は receipt の記録と実際に異なり、receipt から提出状態を再現
   できない。

| 束 | 判定 |
|---|---|
| 1. BFC v2.10 / J1–J5 | **J1–J4 と B-9′ の数学核 PASS / J5 の live 波及漏れにより FAIL** |
| 2. amendment v7 / A18–A20 | **条文の数学・union 設計 PASS / current version identity FAIL** |
| 3. TB4 v2.4 + checker | **PASS** |
| 4. CLAIMS + BFC certificate | **指定同期・現物束縛 PASS** |
| 5. preflight v3 + manifest + triage | **triage 機構は PASS / version equality と closure coverage が FAIL** |
| 6. receipt + F8.3 | **13/13・37/37・25/25 は PASS / reproducible finality が FAIL** |
| **(β)** | **発火不許可** |

---

## F1. 監査 anchor・digest・独立再走

判定対象は委嘱どおり `master` の
`2fa343e6107a982a8683538d79a1433c9bc538be` に固定した。本便対象
artifact はすべてその commit と一致する。作業木にあった対話帳および
過去便の未追跡ファイルは対象外とし、判定にも変更にも用いていない。

| artifact | LF / logical records | SHA-256 |
|---|---:|---|
| `docs/week4-BFC攻略_opus_v2.md` | 1199 / 1199 | `b546b77fdbb04b3f585e4a46a4bc27af55b3adc4e7eb1386442a9da5f1fd3416` |
| `docs/amendment_5prime_draft.md` | 351 / 351 | `84af2e0101a0561b9e6e958319ee2d96d32c04fd543b1e70c722c168e8d3f9a8` |
| `docs/week4-TB4導出_opus_v1.md` | 852 / 852 | `ff71e9fbc162ee613713d9ad317e8fbea635c7e4fadeae189cff1656b52634f4` |
| `search/tb4-monodromy-check.mjs` | 249 / 249 | `6847a76bf5683048bf53531b541cdbc7942645c83207787afb5d1bb2fd454cbd` |
| `certificates/bfc/bfc-antecedents.json` | 0 / 1 | `4e8b8dbd5bfc816edd3d3ca454bc795251ae910ab0e31e66e3821c34dbd78dab` |
| `search/version-event-preflight-lint.mjs` | 124 / 124 | `2aa4cccd9551c6e2fc7315405a0b5f2d7a28fd6ff49b458c1d70842ed89686b7` |
| `search/version-event-manifest.json` | 35 / 35 | `61a49b1ed69c2eb538d17056cc587ca7ab06e10561d20be22a765b1a2a50a11c` |
| `search/preflight-triage.json` | 361 / 362 | `d08e454d403c363a88f075588b18d5f318c46d6add28145b5fcf534e39a19766` |
| `search/preflight-receipt.json` | 46 / 47 | `a446d903bad07709b1e3571a15b0d1242e431706b564c357158b02a2b3e36b82` |

委嘱表の主要 digest はすべて一致する。triage と receipt は末尾 LF が
ないため、最後の二行だけ LF count と logical records が一つずれる。

対象内容を一時 snapshot に複写して再走した結果は次のとおり。

1. `node search/week4-bfc-antecedents.mjs` — **13/13 PASS**。
2. `node search/tb4-monodromy-check.mjs` — **37/37 PASS**。
3. `node search/version-event-preflight-lint.mjs` —
   **CLEAN(open 0 / triaged 45 / orphans 0)**。
4. BFC certificate は `pass_count=25`, `fail_count=0`,
   `fail_closed=true`。
5. certificate の input BFC、GAP script、Node counterpart の三 digest
   は各現物と一致。

したがって `CLEAN` の再現自体には疑義がない。問題は、下記の実在する
不一致を `CLEAN` が許すことである。

---

## F2. 束 1 — BFC v2.10

### F2.1 J1–J4: **PASS**

次を確認した。

- 冒頭 boxed status は
  `TB1–TB4 + (Z_2M-link), 現行 proof ID` へ同期し、current 正本を
  §9 / §13.1 と名指しした。
- B-9′ の状態札と statement は operational \(b_{\rm op}\) の出所を
  \((2.1')\) とした。
- 付録 A は
  \[
  (\mathrm{TB4})\iff\varepsilon=1\Longrightarrow b_{\rm cmp}=1
  \]
  と型付けし、link なしに \(b_{\rm op}\) と読めない理由も正しい。
- §13.1 の link-free proof ID 行は blockquote table 内へ戻った。

### F2.2 J5 の局所修理と数学結論: **PASS**

§10.1.2 の (a-2)(a-3) は、固定した \(M=10\) と共通の Rule 1 root
object の下で \(\bar t_M,\varepsilon\) が二 detector に共通である、
という必要十分な射程へ直った。従って

\[
b_{{\rm op},{\rm sq}}
=b_{{\rm op},{\rm ns}}
=(\bar t_M\varepsilon)^{-1}\pmod M
\]

およびそこからの消去計算は動かない。B-9′ の数学核を開け直す必要は
ない。

### F2.3 J5 の live 波及漏れ: **FAIL**

ところが J5 自身が「異なる \(M\) では所属する unit 群が異なるため、
窓を跨ぐ同一性は型として書けない」と認めた後も、次が live に残る。

1. 299 行は current 定義として
   「枠組みレベルの単位は二つ、**どちらも窓にも dessin にも依らない**」
   とする。これは \(t_{2M}\) について J5 の訂正文と矛盾する。
2. 632 行の B-7tw statement は \(b_{\rm op}\) を
   「**窓にも dessin にも依らず**」とする。正しく必要なのは、固定
   \(M\)・共通 root object の二 detector に対する共通性である。
3. 749 行の B-9′ 証明冒頭はなお
   「両因子がともに**窓にも dessin にも依らない**ことを示せばよい」
   と書く。752 行が直後にこれを過大と訂正しても、証明中の偽の前提文
   が live のままであることは変わらない。
4. より重大に、657 行は
   「\(\varepsilon\) の \(\bmod M\) 還元が裸の \(b\)」とする。これは
   v2.8 型の再融合であり、現行の正形
   \[
   b_{\rm op}=(\bar t_M\varepsilon)^{-1}\pmod M
   \]
   から逆元と \(\bar t_M\) の両方を落としている。同じ行の
   \(b_{\rm sq}=b_{\rm ns}\) は結論として正しいが、その理由付けと記号
   が誤っている。

155 行等の明示的な版差分・履歴はその身分のまま保存してよい。修理が
必要なのは current 定義・statement・proof の上記 live 箇所である。
よって束 1 は **数学核 PASS / artifact finality FAIL**。

---

## F3. 束 2 — amendment v7

### F3.1 A18–A20 の内容: **PASS**

- 8.4.1 の normative 差し替え本文に、R-a =
  `(TB4)+(Z_2M-link)+current BFC proof ID` と、R-b =
  `(E-i)–(E-iv)+alternate proof ID` が転記された。
- 8.4.4 は二 detector の共通性を
  \(b_{\rm op}=(\bar t_{10}\varepsilon)^{-1}\) から正しく説明する。
- result schema は `antecedent_bundle_id` を discriminator とし、
  `/exact/v1` でだけ `exact_recovery_path` を必須化する。R-a と R-b
  の evidence 欄を branch ごとに分け、非 exact bundle では同欄を
  prohibited とした。

これは便 52 F9.2 の union 設計を満たす。数学・schema 方針は PASS。

### F3.2 current version identity: **FAIL**

ただし、イベントの転記元となる live 本文に次が残る。

- 4 行: **「本草案(v6)が PASS してから」**。
- 335 行の司令塔手順 1: **「本草案 v6 を差分ゲート」**。
- 192 行: **「現行 BFC proof」**を **BFC v2.9** と参照。

文書自身は v7、現行 BFC は v2.10 である。A17 がまさに「適用対象
version の古さ」を修理した履歴を持つのに、その修理が次の bump で再び
stale になった。157・329 行の live 参照も限定結論の出所を BFC v2.4
のまま指すため、current source を示す意図なら v2.10 へ揃えるべきで
ある。

これは数学の反例ではないが、版イベントの source artifact としては
blocker である。v7 を PASS したのか v6 を PASS したのか、どの BFC
proof を Rule 1 v1.4 に転記したのかが live 本文だけでは一意にならない。

---

## F4. 束 3・4 — TB4、CLAIMS、certificate

### F4.1 TB4 v2.4: **PASS**

title と冒頭版履歴はいずれも v2.4 を名乗り、指定 digest と一致する。
37/37 は再現し、K3/K5 の核の完全列挙、full tuple、有限/profinite
regression の射程も前便から不変である。

### F4.2 CLAIMS: **指定同期 PASS**

W3-17 は現物で BFC v2.10、TB4 v2.4、checker 37/37、便 53 を参照する。
W3-18 は

\[
b_{{\rm op},{\rm sq}}=b_{{\rm op},{\rm ns}}
=(\bar t_M\varepsilon)^{-1}
\]

と source \((2.1')\) に同期した。

W3-17 末尾の「artifact 残差は便 52 F7 の最小修理を処理中」は、便 53
の監査が終わる前の状態札としては過大な完了宣言を避けており、本判定
では虚偽とはしない。本便が差戻しになったため、結果としても現在の
状態と整合する。

### F4.3 certificate: **PASS**

certificate は BFC v2.10 digest `b546b77f...` に束縛され、GAP script
digest `104e748b...`、Node counterpart digest `f7429890...` も各現物と
一致する。25/25、fail count 0、fail-closed も確認した。

従って束 3 と束 4 の現物は PASS。以下で問題にするのは、これらを
preflight/receipt が将来も同じ状態として拘束できるかである。

---

## F5. 束 5 — preflight v3 / manifest / triage

### F5.1 triage closure: **現データについて PASS**

現 triage は 45 records、reviewer 空 0、disposition 空 0。独立再走でも
active 45、open 0、orphan 0 となった。hash 失効と orphan 強制、reviewer
必須を入れた方向は正しい。

### F5.2 manifest の version equality: **FAIL**

manifest の TB4 record は次である。

```json
{
  "path": "docs/week4-TB4導出_opus_v1.md",
  "declared_version": "v2.5",
  "header_re": "v2\\.[45]"
}
```

現物 header は **v2.4** であり、委嘱も v2.4 を対象とする。それにも
かかわらず lint 48–52 行は `declared_version` と parsed header を比較
せず、単に `header_re` が header のどこかに match するかを見る。
従って receipt は

```text
declared_version = v2.5
header_ok = true
```

という自己矛盾をそのまま出す。コメントと manifest note の
「equality 照合」は実装されていない。

これは便 52 で発見した「TB4 本文 v2.3 / 外部申告 v2.4」と同型の事故を、
値だけ変えて再現した実反例である。mutant を作らなくても、提出現物
そのものが falsifier になっている。

### F5.3 closure coverage の不足

さらに次は `CLEAN` の意味を狭くする。

1. W3-17 の `must_contain` は TB4 v2.4 と 37/37 は見るが、今回
   「同期済み」と申告した **BFC v2.10** と **便 53** を要求しない。
2. BFC 657 行の \(\varepsilon\bmod M\to b\) 再融合、BFC 299/749 行の
   窓射程、amendment の live `v6` / current `BFC v2.9` は token
   集合の外なので 0 open のまま通る。
3. certificate check は input path/digest しか見ない。
   `pass_count=25`, `fail_count=0`, `fail_closed=true`、GAP script と
   Node counterpart の digest を assert しない。
4. TB4 checker の path/digest/期待件数 37 は manifest にない。
   CLAIMS の文字列 `checker 37/37` は、checker 現物の実行結果や digest
   の代用にならない。

現物を人手で見た結果は正しいが、「manifest/claims/cert failures 0」
を version-event closure certificate と呼べる実装にはまだ達して
いない。

---

## F6. 束 6 — receipt と F8.3 finality

### F6.1 `source_commit` は提出状態を指さない: **FAIL**

tracked receipt は

```text
source_commit = 4e4e5fa42937b3a5beba4e11c4bba53d0414bda6
```

を記録する。しかし CLAIMS、最終 certificate、追加 triage、receipt
自身を入れた F8.3 commit は
`3360d600077165b1bf732bf803804628b25294aa`、本便 HEAD はその後の
`2fa343e...` である。

これは単なる「一つ前の commit」ではない。`4e4e5fa` の実内容と
receipt を照合すると、

| 項目 | `source_commit=4e4e5fa` | receipt / 現提出 |
|---|---|---|
| W3-17 normalized row hash | `ab63da93d206fa3e` | `63eb0b52b6d2b9fd` |
| certificate input BFC digest | `9cd1e01c1f273f...` | `b546b77fdbb04b3...` |

となる。すなわち lint は `4e4e5fa` を HEAD とする **dirty state** で
最終 CLAIMS/certificate を読み、親 commit の hash を receipt に書いた。
`git checkout 4e4e5fa` しても receipt の CLEAN 状態は再現せず、むしろ
certificate binding は旧 BFC を指す。

### F6.2 receipt の digest coverage

receipt が保存する digest は三つの文書だけである。manifest、lint
script、triage、certificate、二 checker の digest はなく、
certificate は boolean `certificate_ok`、triage は件数だけである。
このため `source_commit` が不正確な現状では、後から「どの gate と
どの 25/25 certificate が CLEAN を出したか」を復元できない。

Node 13/13、TB4 37/37、現 certificate 25/25 はそれぞれ PASS である。
それでも F8.3 の最後の矢印

```text
clean committed payload
  -> preflight
  -> source identity を持つ immutable receipt
```

は閉じていない。よって F8.3 全体は **計算結果 PASS / finality FAIL**。

---

## F7. (β) 版イベント 3 の裁定と最小再提出

**不許可。**

Rule 1 v1.4 / manifest v1.6、三 seal、typed \(b\) semantics、union
schema、文献要請 13(ii) の縮小、B-9′(e′) の復帰というイベント設計
自体は維持してよい。必要なのは数学の再設計ではなく、次の finality
修理である。

1. BFC の current 箇所を一掃する。
   - \(\varepsilon\) は framework-global。
   - \(t_{2M},\bar t_M,b_{\rm op}\) は **固定 \(M\)・固定 Rule 1 root
     object 下で二 detector に共通**。
   - 裸の \(b\) と「\(\varepsilon\bmod M\) が \(b\)」を
     \(b_{\rm op}=(\bar t_M\varepsilon)^{-1}\) へ直す。
2. amendment の live `v6` を `v7`、current `BFC v2.9` を
   `BFC v2.10` へ同期する。current source を意図する v2.4 参照も同時
   点検する。
3. manifest の TB4 `declared_version` を v2.4 とし、canonical header
   から parse した値との **文字列 equality** を強制する。`header_re`
   を残すなら exact anchor とし、二版を同時に許さない。
4. manifest に checker digest/期待件数、certificate digestと
   `25/0/fail_closed`、CLAIMS W3-17 の BFC v2.10 を加える。
5. BFC digest が変わるため certificate を再束縛し、必要な CLAIMS
   同期と triage 更新を行う。
6. **二段 commit** にする。
   - commit \(C\): 文書・CLAIMS・certificate・manifest・lint・triage
     の完全な clean payload。
   - clean な \(C\) で preflight を走らせ、receipt の
     `source_commit=C` と全 digest を生成。
   - receipt だけを後続 commit \(R\) に入れる。

この順なら receipt が自分自身を含む commit hash を当てるという不可能
な自己参照を避けつつ、検査対象は commit \(C\) から完全再現できる。
その再提出で上記四 blocker が閉じれば、数学核を開け直さず (β) 発火
を再判定できる。

---

## F8. ★教材

1. **regex match は version equality ではない。** `declared_version`
   を読まず、二版を許す regex を通した時点で、manifest は正本でなく
   コメントになっている。
2. **訂正文の直前に旧い偽文を残してはいけない。** 後段で「過大だった」
   と説明しても、current proof の前提文は自動で history にならない。
3. **版 bump は title だけで終わらない。** live 身分、current proof
   citation、適用手順までが version identity の一部である。
4. **receipt と検査対象 commit は二段に分ける。** receipt を生成する
   dirty state の親 commit を `source_commit` と呼んでも、その状態は
   再現できない。
5. **`open 0` は登録した predicate に対する全称でしかない。**
   semantic invariant、version reference、checker/certificate の結果を
   manifest に昇格しなければ、token lint の外側に実違反が残る。

---

## F9. 共同設計者としての発案

### F9.1 version identity を regex から typed parser へ

artifact ごとに canonical header の version token を一つだけ parse し、

```text
parsed_version === manifest.input_version
```

を検査する。イベント後の予定版が必要なら
`input_version` と `output_version` を別欄にし、一つの `header_re` へ
v2.4/v2.5 を混在させない。

### F9.2 receipt を二段 provenance object にする

receipt に少なくとも次を持たせる。

```text
source_commit
source_tree
manifest_sha256
lint_sha256
triage_sha256
certificate_sha256
checker_sha256 + observed/expected count
CLAIMS row hash
ordered_steps
verdict
```

`source_commit` の worktree が clean であることも lint 開始時に
fail-closed で確認する。receipt 自身は後続 commit に置く。

### F9.3 preflight の falsifier fixture を常設する

少なくとも次の三 mutant を一時 copy 上で作り、すべて BLOCKED になる
ことを preflight 自身の regression にする。

1. TB4 header v2.4 / manifest declared v2.5。
2. amendment header v7 / live 手続き v6。
3. certificate の `pass_count` または checker expected count を一つ変更。

今回の提出現物は mutant 1 そのものなので、この fixture は直ちに価値を
持つ。

### F9.4 BFC の parameter-scope invariant

prose lint に次の型付き invariant を一項として持たせる。

```text
epsilon: framework-global
tbar_M, b_op: fixed-M/fixed-root-object, detector-common
b_op = (tbar_M * epsilon)^(-1) mod M
```

「窓にも依らない」と「同じ \(M\) の二 detector に依らない」を別 token
にすれば、J5 の局所修理後に current summary が逆戻りする事故を止められる。

---

## F10. 監査範囲外申告

監査範囲は、便 53 の対象 commit と六束、BFC v2.10、amendment v7、
TB4 v2.4、CLAIMS W3-17/W3-18、BFC certificate、Node checker 二本、
preflight v3、manifest、triage、receipt、および便 52 からの差分である。
SHA-256、13/13、37/37、certificate の三 provenance digest、preflight
45/45 を検収した。preflight は receipt を書くため、リポジトリ外の
一時 snapshot で再走し、作業木は変更していない。

範囲外は、まだ作成されていない Rule 1 v1.4 / manifest v1.6 の実
artifact、適用後の便 54 差分、個別 Model-Builder 探索、封印値、
Freeze 2、外部文献原文、Lean 形式化である。本便では GAP を再生成せず、
既存 25/25 certificate の schema・値・fail-closed・三 digest 束縛を
監査した。本判定は既存 Freeze 1 や従来の Model-Builder 許可を撤回せず、
この未閉鎖 source 群からの **version event 3 (β)** だけを止める。
