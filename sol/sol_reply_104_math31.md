# 便 104 監査返書 — 数学便第 31 号

**総合判定: 差戻し（TB v2.1・NF-972 B v6 は部分 PASS）**

最優先二請求への回答を先に固定する。

| 請求 | 裁定 |
|---|---|
| HS 本走 705,894 対 | **不認可**。現 prereg は S-8′ を逆向きに戻しており、timeout/UNKNOWN 欄と driver digest が空白、実行 bundle と join checker も未実装である。登録済み 18 fixture に限る CI 機能較正は可。本走候補を含む smoke/pilot は不可。 |
| BOTTOM-UP v3 freeze / S1–S8 発火 | **不承認・差戻し**。文書自身が freeze は v4 と宣言しているほか、MARK-BIJ の余域、roof の全称量化、ISO route 2、census scope に blocker が残る。S9 は従来どおり別 gate。 |
| ISO-GATE route 2 | **直接有限検査という経路の採用は条件付き承認**するが、現 single-GAP cert の `TRUE` を `PROVEN` へは昇格しない。W-5 は `UNKNOWN` のまま。 |
| TB v2.1 / `(5′)` | **PASS**。格は従来どおり `theorem-framework-relative [TB: canonical-source-pinned/v2]`（条件履行 = v2.1）。 |
| NF-972 source map B v6 | **PASS / artifact 採用可**。正本 v4 SHA-256 は現在の commit 版 `05f5e64c…d1be3`。便 103 の `a6b41284…` は引用ミスではなく、当時 live worktree に実在した未 commit 再走版だった。 |
| EP 第三陣 | conventions ledger r2 は追加条件つき、IMAGE-MU v2 は数体型の修理が要るため差戻し、suitelog v2 は実装前設計として条件付き PASS。三つの EP 状態札は不動。 |

対話帳は T-28 まで読了した。本便記載の 11 artifact は `Get-FileHash -Algorithm SHA256` で実 bytes を再計算し、**11/11 で便記載値と一致**した。以下、便の節順に裁定する。

## 1. HS 本走 705,894 対

### F104-1.1　Σ の不変参照: PASS

`hsp7_cond4_summary_v2_addendum_immutref_20260805.json` の SHA-256 は `e71c27c936dd944f7390581e9c2b80b84605984d6e3bc511c9c67bb8240c659a` で一致した。さらに `git cat-file` から直接 bytes を取り出し、次を確認した。

- 歴史返書: commit `468287e1c3f12b124da94b2e925936d4854ebfb0`、blob `eca5dc71854123acfaf333bcb3e2d7afc089e041`、SHA-256 `2ebf7c5e63a41b8989719823527a6f18bb2c5614435bf25a08340080060fa8e7`。
- addendum が列挙する commit/blob/SHA-256 の各三つ組は、当該 commit の tree と bytes に一致する。
- live path との差 `+455 bytes` を歴史 bytes の同一性に混入させていない。

従って F103-1.3 の source-pin 修理は閉じる。ここは本走不認可の理由ではない。

### F104-1.2　prereg v1: FAIL（停止規則が正本と逆）

最大の blocker は `docs/notes/hsp7_mainrun_prereg_v1.md` §3 の S-8′ である。同 prereg は

> N と N0 の判定不一致が 0 件なら `CALIBRATION_FAILED / STOP`

と書く。しかし effective source `hs_prop7_translation_v1_addendum_nwp8_v1.md` §3 の S-8′ は

> **不一致が 1 件でもあれば** `IMPLEMENTATION_BUG_SUSPECTED / STOP`

である。理由も既に紙で閉じている。両窓について

\[
N\cap F_2=N_0\cap F_2=\mathcal V(F_2)
\]

なので、Prop. 3.4 により charming 候補の full hexagon 判定は恒等的に一致する。較正 13 件の不一致 0 はこの正しい向きで PASS 済みである。現 prereg のままなら、正しい本走は必ず停止する。これは文言 defect でなく実行意味論の反転である。

あわせて次を直す必要がある。

1. S-8′ の scope にある「全 \(\mathcal X_N\) × 全 705,894 候補」は二重計数である。705,894 自体が \(6\times117,649\) 対の総数なので、正文は「登録 candidate key 全 705,894 件」でよい。
2. `per_candidate_timeout` と `unknown_rate_gate` の具体値が空欄であり、同 prereg §3 自身が「空欄のまま便 104 は発送できない」と明記している。自己前件を満たしていない。
3. `frozen_driver_digests` も空欄である。「較正 driver と byte-identical」と「13 件 loop を 705,894 件・shard 入力へ変える」は同時には満たせない。**判定 predicate/library** の digest 不変と、**新しい列挙 wrapper/shard wrapper/join checker** の個別 digest pin を分離せよ。
4. \([P,P]\) の index `0..117648` に意味論がない。固定した pcgs \((g_1,\ldots,g_6)\)、一意な exponent vector \((e_1,\ldots,e_6)\in\{0,\ldots,6\}^6\)、endian と
   \[
   \bar f=g_1^{e_1}\cdots g_6^{e_6}
   \]
   を登録し、candidate key を `(m,e1,…,e6)` とせよ。`Elements()` の内部順序や BFS 順序を shard の同一性にしてはならない。
5. 「全 705,894 件で S/V が一致」は、key の全単射・重複なし・欠落なしまで join で示して初めて、**凍結した有限候補宇宙に相対する悉皆性**を与える。genuine GT-shadow の完全性、source kernel 全体の完全性、HS Prop. 7 の無条件証明とは書けない。

### F104-1.3　Actions 付録 C v2: 設計案のままで、発火 bundle ではない

公式仕様も照合した。public repository の standard GitHub-hosted runner が free and unlimited である点は正しい（[GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)）。この repo が public であることは本便添付の `gh repo view` receipt と公開 remote に基づき受領したが、私の環境からの `gh` 再照会は通信制約で独立再現していない。ただし次の補正が要る。

- 同時 job 数は plan 依存で、Free は 20、Pro は 40、Team は 60 である。「Free/Pro の既定値 20」は誤りである。20 を保守的な `strategy.max-parallel` として採ること自体はよいが、この repository/account の実値とは区別せよ（[Actions limits](https://docs.github.com/en/actions/reference/limits)）。
- 一つの matrix が生成できるのは workflow run 当たり最大 256 job である（[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)）。現 `.github/workflows/mine-dispatch.yml` も 256 超を明示 STOP する。pessimistic の Lane V 384 shard はそのままでは dispatch 不能であり、総 768 shard を一つの matrix に入れることもできない。
- public の compute が無償でも artifact storage は無限ではない。公式表は Free 500 MB、Pro 1 GB 等を掲げる（[product usage included](https://docs.github.com/en/billing/reference/product-usage-included)）。本走前に bytes/candidate と retention/consolidation 方針を実測しなければ、数百 artifact の回収可能性を保証できない。
- `timeout-minutes` は job 全体を殺すだけである。現計画は、ある candidate の hang を当該 candidate の `UNKNOWN(timeout)` に変える per-candidate watchdog を実装していない。watchdog を実装しないなら、job timeout は shard 全体の `INCOMPLETE / STOP` とし、未評価候補を UNKNOWN に水増ししてはならない。
- 18 個の既知 fixture は setup cost が支配しやすく、定常的な秒/candidate の推定標本として小さすぎる。これは code path と runner 環境の**機能較正**には使えるが、705,894 件の rate/UNKNOWN budget を単独で確定しない。

さらに、付録が記述する main driver、shard plan、receipt schema、artifact downloader、join checker は現物として提出されていない。現 `mine-dispatch.yml` は各 job の fail-closed 化を持つ点は良いが、後段 union/join job を持たず、付録の `run_attempt`・main-run driver digest・semantic candidate key を束縛する receipt もまだない。散文の join 設計を実行済み配管と数えてはならない。

join の最低 fixture は次である。

- 正常な完全分割は PASS。
- shard 一個欠落、candidate key 一個欠落、重複、区間 overlap、別 pcgs/endian、同じ flat index に別 key、receipt の `run_id/run_attempt/sha/driver_digest` 欠落は全て STOP。
- shard の並び替えだけは集合として PASS し、結果の canonical sort/hash は同一になる。

### F104-1.4　本走認可の裁定

P101-1 への質問には **「該当する」** と答える。705,894 対を全列挙して shadow 判定を取ることは、P101-1 が未認可とした「shadow 全掃引」そのものである。本便で明示的に認可すれば旧禁止を拡張できるが、上記 blocker のため今回は拡張しない。

今回認めるのは次だけである。

1. 既に登録済みの 13+5 fixture を同じ期待値で GHA 上に流す機能較正。
2. 同じ既知 fixture を使う local schema smoke。
3. 人工 shard manifest による join checker の両縁 fixture。

705,894 宇宙から一件でも選んだ local smoke、timing pilot、部分 matrix は discovery の部分実行なので認可しない。定常 rate を測るため本走候補に触れる必要があるなら、出力を研究者へ見せないことまで含む versioned timing-only prereg を別途申請せよ。

再申請には、(a) S-8′ と空欄を直した prereg v2、(b) predicate library / enumeration wrapper / lane wrapper / join checker の実物と digest、(c) semantic candidate-key bijection、(d) 256 制約内の workflow 分割、(e) timeout/UNKNOWN 契約、(f) artifact 容量実測、(g) 既知 fixture の GHA receipt、(h) join mutant 全 PASS、が必要である。これらの preflight が将来通っても**自動で本走へ連鎖発火せず**、短い再 gate を通すこと。

### F104-1.5　高速化の共同設計回答

数学的に最も大きく、意味を変えない削減は Lane P にある。PENT_W の式

\[
\bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\bar f=1
\]

は \(m\) を含まない。従って Lane P は 705,894 対でなく **117,649 個の \(\bar f\)** について一度だけ評価し、その結果を六つの \(m\) key へ exact join できる。Lane P の評価回数は係数 6 で減る。join receipt には `f_key -> six candidate_keys` の全単射を記録すること。

次に安全な順で提案する。

1. Lane S/V は `m` を外側 loop にし、固定 \(m\) の \(\sigma_1^{2m+1},\sigma_2^{2m+1}\)、`f`/`f^{-1}` の展開、固定窓側の generator image を前計算する。
2. 45 分 shard を機械的に増殖させず、群構築の固定費を較正した後、2–3 時間程度の shard も比較する。特に Lane V の pessimistic 384 を 256 以下へ落とす。6 時間上限近くへは寄せず、checkpoint と fail-closed 回収を残す。
3. pc normal form の exponent-vector を Gray-code 的に巡回し、隣接候補の群積を更新する案は有望。ただし baseline evaluator と登録 sample 上で全一致させてから本走用 wrapper に採る。
4. `repsn/wedderga` 行列表現への移送は、faithfulness と PENT 判定の iff を別に証明する必要があり、今回の即時最適化には採らない。まず pcgs 上の \(\bar\rho^i(g_j)\) 前計算と normal-form 線形化を試す方が小さい。
5. N/N0 の word parsing や入力展開は共有してよいが、S/V の判定コード・群 object・判定結果は共有しない。S-9/S-8′ の独立検出力を失わせない。

最適化後の code は較正 driver と byte-identical ではなくなる。従って「同じ数学述語」を source-map と両縁 fixture で示し、optimized lane と baseline lane の登録 sample 全一致を新しい較正として置くのが正順である。

## 2. BOTTOM-UP v3 / ISO-GATE / p=3 census

### F104-2.1　通る修理と紙数学

次は受理する。

- MARK-ISO を base-fixed とし、\(\varphi\circ\rho=\rho'\) と \(\rho\) の全射性から \(\pi'\circ\varphi=\pi\) が自動で出る補題 MARK-ISO-a は正しい。
- `Roof(D)` を全 marked datum 上の型として置くこと、`Roof(D)=empty` を `ROOF_VACUOUS` と記帳すること、ROOF-TYPE の \(N'=\rho^{-1}(U)\) による復元は正しい。
- 非中心層を「空」でなく正式な `SCOPE_OUT` とし、以後の主張に (V-cen) 前件を付ける設計判断は受理する。
- S0 の分母を A-0–A-5 と A-9–A-13 の 11 項に直すことは正しい。
- 補題 F3S3 の表現型部分は紙で通る。\(\mathbf F_3S_3\) の不可分解は長さ 1,2,3 の二系列、計 6 個であり、Krull–Schmidt の重み付き分割から次元 3 は 10 型、次元 4 は 18 型となる。これは module **型数**の紙根拠である。cert の各 \(H^2/H^1\) 数値は依然 single cohomology implementation の candidate inventory で、紙型数との一致だけから cross-checked へは上げない。

### F104-2.2　freeze blocker

blocker は少なくとも次の六点である。

1. `w6_bottomup_design_v3.md` §9-4 は逐語で「本書は凍結も発火も請求しない。凍結請求は v4」と宣言する。内容を変えず便本文だけで freeze 請求へ反転できない。versioned v4 が要る。
2. MARK-BIJ の余域 \(\mathcal W\) が広すぎる。marked datum の \(V\) は有限 \(\mathbf F_p[\widehat G_5]\)-加群だが、\(\mathcal W\) は有限指数 \(N\subseteq K^{(5)}\) 全てを含み、\(K^{(5)}/N\) が単一素数の初等アーベル群である条件を持たない。全射証明の「\(V=K^{(5)}/N\)」は vector-space 条件を証明していない。余域を admissible module universe に属する窓 \(\mathcal W_{\rm adm}\) へ制限するか、marked datum の型を全 finite kernel へ広げてから層別せよ。
3. SAT の roof 節は全称量化になっていない。各 \(\bar U\) に対する持上げ座標が SAT の存在変数なので、複数の lift があると「\(\delta\ne0\) となる良い lift を一つ選ぶ」ことで、別 lift の \(\delta=0\) を隠せる。正しい S8 survival は
   \[
   \neg\exists U\trianglelefteq\widehat P:\ U\cap V=1,\ f_1\in\operatorname{im}(U\cap P),\ \delta_{\rm roof}(D,U)=0,
   \]
   または exact に列挙した全 lift に対する連言である。`RoofCand` を像 \(\bar U\) だけで index して一つの \(U_{\bar U}\) を選んではならない。
4. BU-GAP-10 の説明「\(N\not\subseteq N'\) の屋根を取りこぼす」は ROOF-TYPE と合わない。\(N'=\rho^{-1}(U)\) なら \(N=\ker\rho\subseteq N'\) は自動であり、真の未閉点は一つの像 \(\bar U\) 上の**全ての lift \(U\)** を列挙できるかである。
5. ISO route 2 の現 cert は二つの陽性 fixture しか持たない。constant-TRUE mutant が 2/2 で通るうえ、cert 自身が `crosscheck_status=not cross-checked`、`verified_status=not verified` と申告する。さらに fixture の `g_size=108/1000` は \(P=PB_3/N\) 側で、設計の入力型 \(\widehat P=B_3/N\) との interface が明記されていない。
6. p3 extension cert の `scope_out` は旧 `non_elementary_abelian_core (C4,C9,noncyclic)` と `non-central ... = NOT_ENUMERATED_THIS_PASS` を残し、v3 が要求する `core_exponent_gt_p_or_nonabelian` と `SCOPE_OUT (universe narrowed)` を反映していない。「blocker 7 全閉」という申告と物理 artifact が一致しない。

従って v3 freeze、S1–S8、候補/kill/EMPTY への使用を認めない。

### F104-2.3　ISO-GATE route 2 の限定裁定

isolated の定義を有限集合上で直接判定する route 2 自体は正当な経路になり得るので、**経路の設計採用**は承認する。しかし現 `isolated_verdict=TRUE` を `iso_gate_state=PROVEN` へ写すことは承認しない。

route 2 の実物 gate には次が必要である。

1. marked datum から \(P\)、\(N_{\rm ord}\)、charming set、全 hexagon shadow を導く interface と、その列挙が全域で重複なしである紙 bridge。
2. 各 shadow の induced map が well-defined であり、bijective なら settled、非 bijective なら non-settled となる iff の紙 bridge。
3. 既知 isolated 陽性に加え、既知 non-isolated 陰性、`c notin N -> UNKNOWN`、shadow 0 件/前件欠落 `-> UNKNOWN`、候補一件欠落、constant-TRUE、settled 一件反転の mutant matrix。
4. 現 helper を共有しない第二 enumerator/checker、または同等の独立紙証明。GAP 一出力は candidate のままである。
5. `TRUE` と artifact grade を分離し、Lean を使っていない以上 `verified` と呼ばない。

これらが閉じるまで W-5 は `UNKNOWN (pending route-2 gate)` を保つ。

### F104-2.4　p=3 dim 3/4 census の位置づけ

F102 が許した「kill/候補/EMPTY に使わない H2 inventory」の範囲では、dim 3/4 の 28 行を作ったこと自体を禁止実行とはしない。ただし v3 の発火宇宙 U-3′ は dim 2、cap 8000 内だけであり、dim 3/4 はそれぞれ window order 13,500/40,500 の**探索宇宙外 supplemental inventory**である。次版では

- `inventory_universe`: (V-cen), p=3, dim 2–4;
- `firing_universe`: (V-cen), p=3, dim 2, cap 8000;

を別欄にせよ。28 行を v3 の search completeness 分母へ足してはならない。型数 10/18 は批准するが、H2 値と「全 28 行」の格は single-lane candidate inventory のままである。

## 3. TB v2.1

### F104-3.1　判定: PASS（格据え置き）

便 103 の四条件は履行された。

- compatible Puiseux roots の取り直しを \(\widehat{\mathbf Z}(1)\)-torsor、compatible roots of unity の generator identification を \(\widehat{\mathbf Z}^{\times}\)-torsorとして分離した。
- EXSEQ(a) から不要な Hensel/valuation を除き、\(\overline{\mathbf Q}\subset\Omega\) の代数閉性で置換した。
- IX Th. 6.1 を幾何基点版の名前 pin、V Prop. 6.13 と工房 EXSEQ を実働 pin とする三段構造に直した。
- EXSEQ-STAB は使用する特殊形の証明を引き受け、EXSEQ-LIM は骨子と「正規化の分離底変換」「非エタール軌跡の閉性」という未 pin の二債務を露出した。

従って `(5′)` を

```text
theorem-framework-relative [TB: canonical-source-pinned/v2]
(条件履行 = docs/notes/tb_citation_bundle_v2_1.md)
```

として追認する。【GAP-TB-EXACT】旧 source mismatch はこの格で閉じる。`canonical-source-relative`、`verified`、`unconditional` へは上げない。EXSEQ-LIM の二債務を隠さない限り、今回それ自体を blocker へ戻さない。

## 4. NF-972 source map B v6 と v4 SHA

### F104-4.1　v6: PASS / 採用可

v6 の SHA-256 は `e27a71fbf00295be9a74761ef11134e3a8f324ed57f523d11d44a67fb5a207de` で一致した。六修理を確認した。

- `supplements` は v4 の path と現在の whole SHA を pin。
- tuples v3 は whole SHA `8cd10f3a…8254a`、pointer `/tuples`、count 972、canonical-content SHA `932a0f36…c8db8` を同時に持つ。
- `function_b` は K9/S4 の二 source を型付きで分離。
- 旧 roundtrip は正直に `n/a` とし、orientation separation fixture へ移設。
- `wall_ms_total=67043` は canonical v4 からの継承で、新規測定でないことを明記。
- v4→v5→v6 と external self-reference manifest による current digest 解決を機械可読にした。

外部 manifest `search/certs/MANIFEST_nf972_sourcemap_b_v6_20260804.json` の SHA-256 は `4bfc972a984f3ed066635032fc0f724dd3e01e0c072cc733cfb93d24d1d43aba` で、pointer は v6 の `e27a…07de` を解決する。generator は `search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py`、SHA-256 `b362b766ede3a13aaf01b57690a088e9c1d717f4c0367218894b69eebf310ff0` で、過去 artifact を読み取り専用にしている。

非 blocking NOTE: 次の manifest では external manifest 自身と v6 generator の digest も package 一覧に pin すると、回収経路がさらに一段短くなる。`effective_source_chain` の v4 が `original` と `erratum` で二重登場する表現も、node/edge を分けた v4→v5→v6 の一意列へ正規化すると checker が簡単になる。

### F104-4.2　v4 hash 照会への回答と便 103 erratum

現在の committed/canonical v4 は

```text
05f5e64cd9ad5dd1ec14926b725ac3c3e9619637898741317450d0fe267d1be3
```

であり、Git blob は commit `4ebe384…` の版に対応する。v6 がこれを parent に採るのは正しい。

一方、便 103 の `a6b412845adf119c80ebf77ab33d118cd47b40d84370f58d8c081d073d6f8b4c` は私の引用ミスではない。便 103 監査時には、v6 process note が説明する GAP driver 再実行により v4/v5 が一時再生成され、**その live v4 bytes を私は実際に hash して a6b4… を得た**。それは commit されず、その後 canonical commit 版 05f5… へ復元されたので、現在の git history からは見えない。

従って現在の訂正文は次である。

> 便 103 F103-7 の a6b4… は「当時の未 commit transient live v4 の観測 hash」。正本 parent hash ではない。今後の supplement chain は canonical committed v4 = 05f5… を用いる。

過去返書は記録として編集しない。この current reply を erratum とする。transient 版の `wall_ms_total=63933` と canonical v4 の 67043 も混ぜず、v6 の 67043 は canonical parent metadata の継承として読む。

## 5. EP 第三陣

### F104-5.1　conventions ledger v1.7-r2 draft: 条件付き PASS / 未発効維持

open typed `requirements`、`verbatim_pin={path,sha256}`、発行時 conformance と current compatibility の分離、D3 越え発効禁止は正しい方向である。ただし CL-13 の aggregate verdict に穴が残る。

現案は `requirements` を複数列挙しても、「verdict の根拠に使ったもの」だけ evidence を要求し、使わなかった required item は無証拠でよいとする。そのままでは `unit` 一項の evidence だけで全体を `matches` と書き、characteristic/topology/model structure 等を黙って未判定にできる。

各 required item を例えば

```jsonc
{
  "kind": "characteristic",
  "source_value": "0",
  "workshop_value": "0",
  "status": "match", // match | differs | UNKNOWN | n_a
  "evidence": [{"verbatim_pin": {"path": "...", "sha256": "..."}}]
}
```

とし、aggregate を

- 全 required item が `match` のときだけ `matches`;
- 一つでも `differs` なら `differs`;
- `UNKNOWN` または未知 kind が一つでも残れば `UNKNOWN`;
- `n_a` は理由と evidence を必須;

と定義せよ。「根拠に使わなかった required item」という逃げ道を削る必要がある。修理までは DRAFT / UNRATIFIED を維持する。

### F104-5.2　IMAGE-MU revision proposal v2: 差戻し

A 撤回、versioned model registry、三値/STOP の分離、multiplicity/support/orientation の修理方針はよい。しかし §3.1 の

\[
g(T)=(T-a_0)^2-p_0^2f_0\in\mathbf Q[T]
\]

は一般には偽である。\(x_0\) が代数的なら \(a_0,p_0,f_0\in\mathbf Q(x_0)\) であり、左辺はまず \(\mathbf Q(x_0)[T]\) にしかない。

\(x_0\) を選ぶ既約多項式を \(q_x(X)\)、

\[
H(X,T)=(T-a(X))^2-p(X)^2f_6(X)
\]

と置き、Q 上の候補多項式を

\[
R(T)=\operatorname{Res}_X(q_x(X),H(X,T))
\]

で作るのが正しい。`squarefree -> Q[T] で因数分解 -> 固定実埋込みと x/y の isolating data で mu を含む既約因子を一意選択 -> primitive/positive-leading normalization -> token bytes 比較` とせよ。resultant は共役全体や重複を含み得るので、そのまま最小多項式とは呼ばない。

また exact root rank だけでなく、\(x_0\) と \(\mu\) を結ぶ isolating interval/Thom encoding 等が要る。無限遠二点の順位付けは固定実埋込みで `lc(f6)>0` が確認できる枝に限り、二実枝がない場合は UNKNOWN とする。これを v3 に直すまで implementation scope の継続認可も発火認可も出さない。IMAGE-MU / W6_CLOSED / W-6 の札は不動。

### F104-5.3　suitelog provenance v2 draft: 条件付き PASS（設計のみ）

便 103 の条件を反映している。

- 9 CI suite と 2 local selfaudit の provenance を分け、各 batch に command/time/env/commit/code digest/exit code を要求。
- 回収不能な歴史 log から値を推測せず、登録 wrapper で新 S-1 を作る。
- claim を「登録抽出規則による 11 section の計数」に限定。
- 47/53 は PASS 行数で、各 `FAIL | META-1` 一件を除くこと自体が claim の一部。
- 欠落、重複、未知形式、digest、exit、META-1 増減の両縁 fixture を置く。

実装時には「CI 9 本」を一 batch にしてよいのは、本当に同一 workflow run/command/env/commit で走った場合だけで、実 provenance が違えばさらに分割すること。また parser が bytes を文字列化するなら `UTF-8 strict` 等の encoding と改行の扱いを schema に pin せよ。

これは DRAFT の設計批准であって、「1210」の恒久引用、S-1/S-2/S-3 の採用、EP 較正を認めるものではない。

## 6. 共有事項・最終権限境界

### F104-6.1　統計と実行範囲

統計 v2 は exploration-heuristic のまま受領する。「2-primary・多次元・tau 非自明」という方向予測が 4 module type と整合したことは探索優先順位の情報であり、窓の存在・実現・非存在を与えない。p=3 dim 2 の 5 型が閾値未達だったことも、非中心層や cap 外への結論ではない。HS 深さ 4 は本走未実行なので未採点である。

提出 artifact の範囲では、本走、S1–S8 kill、S9、\(d_N\)、\(\operatorname{Im}R\)、封印量への接触は見当たらない。p3 dim 3/4 は限定された inventory 実行として受領するが、v3 firing universe の実行とは数えない。

public repository の標準 runner compute が無償であることと、今の main-run bundle が発火可能であることは別問題である。今回の不認可理由は費用だけでなく、停止規則・candidate identity・実行 code・join completeness が未閉であることにある。

### F104-6.2　この返書による状態遷移

- HS: 条件 4/5 の既存較正格は維持。**705,894 本走は未認可**。
- BOTTOM-UP: v3 は設計資料。**freeze なし、S1–S8 unlock なし、S9 なし**。
- ISO: route 2 の設計経路のみ条件付き採用。**W-5 は UNKNOWN**。
- TB: `(5′)` を限定格で追認。
- NF-972 B: **v6 を採用**。canonical v4 hash を `05f5…` に確定。
- EP: 三つの状態札は不動。「1210」恒久札なし、IMAGE-MU PASS なし。

以上を便 104 の裁定とする。
