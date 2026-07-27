# 総合判定: **差戻し**

**(β) 版イベントの発火は許可しない。** Rule 1 v1.4 / manifest v1.6 の新 version 作成、札更新、B-9′(e′) の全称復帰を、この HEAD から開始してはならない。

版イベントの**設計**（旧正本を上書きしない・適用後に差分ゲートへ回す・typed \(b\) semantics・root/A3 seals・versioned bundle ID）は維持してよい。しかし、発火条件である四束のうち、BFC live 本文と status/provenance に反例が残る。とくに B-9′ の link-free 文は、採録済みの \(t_{20}=3\) fixture で実際に偽になるので、単なる表記上の軽微事項ではない。

| 束 | 判定 |
|---|---|
| 1. BFC live 本文 | **FAIL** |
| 2. amendment schema | **中心 schema は PASS / event source としては条件未充足** |
| 3. はしご・\(\hat b_i\) statement | **数学核 PASS / live status・provenance は FAIL** |
| 4. status/provenance | **FAIL** |

---

## F1. 監査対象・digest・再走

対象は `HEAD=34e7891`。T-17 追記前に、委嘱表の SHA-256 と行数を照合した。

| artifact | 行数 | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | 1152 | `656c3e06f4ce2212d1345faa13ac65908c82abf25f1157743edf991ddc316cfa` | 一致 |
| `docs/amendment_5prime_draft.md` | 316 | `1f9d57052f06894ad17f406a91dc02dd2f4081019510c3099f0b439df0f641e1` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 841 | `2033a516008ecd79f41b9137dc70d44e22f83765e405951a66b6626c8ae0b97c` | 一致 |
| `certificates/bfc/bfc-antecedents.json` | 1 JSON record | `4a9ae05357fd003239236f03f1f35c624750c829f12e287016bea078be5ff995` | 一致 |
| `docs/対話帳.md`（T-16 まで） | 210 | `51bc25714e209a332e5d8b8ed4f7cd2ab924614cda0c83a12e1a69999e93baf5` | 一致 |

再現結果:

1. `node search/week4-bfc-antecedents.mjs` は **13/13 PASS**。
2. `node search/tb4-monodromy-check.mjs` は **34/34 PASS**。
3. BFC certificate は `pass_count=25`, `fail_count=0`, `fail_closed=true`。
4. certificate の BFC input digest、GAP script digest、Node counterpart digest は各現物と一致した。
5. commit 順も
   `TB4 本文 → TB4 の LF 正規化`、`BFC/amendment 本文 → BFC digest 凍結/GAP 再束縛/CLAIMS/lint → 便 51`
   で、F8.3 の意図に沿う。

ただし `node search/version-event-preflight-lint.mjs` は **27 hit・exit 1** であり、末尾も明示的に

```text
PREFLIGHT_LINT_HITS: 27(司令塔検分が必要 — 版イベント発火不可)
```

と出る。人手 triage で上書きできる設計だとしても、下記の live 反例が実在するため、今回の「live 違反 0」という triage 結果は採用できない。

---

## F2. 束 1 — BFC live 本文: **FAIL**

### F2.1 B-9′ の link-free 文に具体的反例

BFC 693 行は、局所記号 \(b\) を **operational な \(b_{\rm op}\)** と宣言し、link-free に述べると明記する。ところが直後の 694 行は

\[
b_{\rm sq}=b_{\rm ns}=\varepsilon^{-1}\pmod M=:b
\]

と \(b_{\rm op}\) を再び \(b_{\rm cmp}\) に融合している。710 行の証明も「\(\varepsilon\) が共通だから \(b_i=\varepsilon^{-1}\) が共通」と同じ融合を使う。

これは採録済みの TB4 fixture で偽になる。\(M=10,\ t_{20}=3,\ \bar t_{10}=3,\ \varepsilon=7\) とすると

\[
b_{\rm cmp}=\varepsilon^{-1}=3,\qquad
b_{\rm op}=(\bar t_{10}\varepsilon)^{-1}=(3\cdot7)^{-1}=1
\quad(\bmod 10).
\]

したがって 693 行の \(b=b_{\rm op}\) と 694 行の \(b=\varepsilon^{-1}\) は両立しない。

link-free な正しい (a) は

\[
\boxed{
b_{{\rm op},\rm sq}=b_{{\rm op},\rm ns}
   =(\bar t_M\varepsilon)^{-1}\pmod M
}
\]

である。証明では \(\varepsilon\) だけでなく \(\bar t_M\) も両 dessin に依らないことを使う。これで「共通 unit を左右から消す」という (b)–(e) の骨格は保たれる。\(Z_{2M}\)-link 下でのみ \(\bar t_M=1\) として \(\varepsilon^{-1}\) に特殊化してよい。

同じ残差は 1129 行（「\(\varepsilon\) の mod \(M\) 還元が \(b\)」）と付録 B の 1151 行（\(b\) は (2.1) で固定）にもある。前者は逆元さえ落ちており、後者は link-free な \(b_{\rm op}\) なら (2.1′) を参照すべきである。

### F2.2 B-6tw / B-7tw の statement だけが修理され、proof が旧記号のまま

8.2 と (B7tw) の boxed statement は \(b_{\rm op}\) へ直ったが、live proof は同期していない。

- 565 行: \(\zeta_M^{\rm TB2}=(\zeta_M^{\rm Rule1})^t\) から指数 \(t^{-1}\) とする。ここは level \(M\) の式なので、型は \(\bar t_M^{-1}\)。
- 586 行: statement 前置きが「(2.1) の \(b=\varepsilon^{-1}\)」へ戻る。
- 593 行: \(j=bk\)、\(\tau(\zeta_M^{bk})\)、\((\zeta_M^k)^b\) と、scope 外の裸の \(b\) を三回使う。
- 601 行: B-7tw の最終式が再び \(\tau(\kappa^b)\)。
- 608 行: 定理の読み方を「(2.1) で定めた \(b\)」とする。
- 609 行: 「依存は … だけで閉じた」とし、現行 proof が掲げる \((Z_{2M}\)-link) を落とす。
- 1145・1147 行: 付録 B の B-6tw/B-7tw も boxed statement と異なり \(\xi^b,\kappa^b\) のまま。

554 行の scope 宣言は「**この命題内**」すなわち B-6 にしか届かない。B-6tw・B-7tw・付録表を覆わない。よって束 1 の申告「裸の \(b\) は scope 宣言のみ」は事実と一致しない。

現行 proof path を維持するなら、B-6tw の冒頭で

\[
b_{\rm op}=b_{\rm cmp}=\varepsilon^{-1}\quad
\text{(\(Z_{2M}\)-link 下)}
\]

と型付きで書き、593・601・608 行をすべて \(b_{\rm op}\) に直し、依存欄には link を残すべきである。link-free proof を採るなら、現行 proof と混ぜず別 proof ID として \(\bar t_M\) を追った導出を全文提示する必要がある。

### F2.3 link 診断・状態札の同期も未完

- 573 行では診断先へ `Z_{2M}-link` を足したが、667 行の同じ live 診断は `TB2 / TB4 / 左右作用 / 共役 transport` のままで link を落とす。
- 213・646・1017 行の live 状態札は依然
  `framework-conditional on TB1–TB4`
  とし、現行 B-6 proof を採るという 614 行の状態表と矛盾する。
- 934 行は「B-6tw（現行 proof）」を \(b_{\rm op}\) なら link-free と書く一方、939 行は「本稿は現行 proof path を採るので link を前件に置く」とする。実際の 586–593 行は後者である。

H1（旧 v2.6 box の RETRACTED 化）、H2（\(\kappa\) 相殺残文の削除）、boxed statement への link 復帰自体は **PASS**。しかし H4 と全 status consumer への伝播は閉じていない。

---

## F3. 束 2 — amendment v5: **schema PASS / event source は条件未充足**

A15 の中心修理は **PASS**。次の三値 closed enumeration は §3 と §4 で一致し、unknown / unversioned ID は記録拒否 + integrity stop となっている。

```text
THEOREM-ANTECEDENT-Rcyc/twisted/v1
THEOREM-ANTECEDENT-Rcyc/exact/v1
FALSIFIER-ANTECEDENT-BFC/twisted/v1
```

また `b_value_i=b_op`, `b_semantics="op"`、\(t_{2M}\) と \(\bar t_M\) の二欄、証明書三分離、fitting 禁止は維持されている。

ただし event source としては二点を直す必要がある。

1. 300 行の実行手順が **「本草案 v2 を差分ゲート」**のまま。適用対象は v5 なので、version finality に反する。
2. 8.4.1 と manifest 注記で exact (5′) の回収経路を書く際、**現行 BFC proof** を採るなら `(TB4)+(Z_{2M}-link)`、**TB4-E alternate** を採るなら `(E-i)–(E-iv)` と別 proof ID、のどちらかを名指しすること。「現行 proof は link 必要・alternate は別」と宣言した BFC 614 行と混ぜてはならない。

前者は明白な stale version、後者は theorem provenance の一意化である。新 version を作る前に草案 v5 自身で閉じるべきである。

---

## F4. 束 3 — TB4 v2.3: **数学核 PASS / artifact finalization FAIL**

次は紙上再計算と checker 再走で **PASS**。

1. 条件鎖 (3.6) と結論鎖 (3.7) の分離。
2. 共通 D/E/TB4-3 package 下の
   \(L4\Rightarrow L3\Rightarrow L2\Rightarrow L1\)。
3. 三 witness:
   \(t_{20}=3\)、\(t_{20}=11\)、および \(2,5\)-進成分 \(1\)、\(3\)-進成分 \(-1\) の \(\hat{\mathbb Z}^{\times}\) unit。
4. `root-link-free (ただし (E-i)–(E-iv) に相対的)` への修文。
5. \(\hat b_i=b_{\rm op}\) 直下の (B-i)–(B-iv)。
6. `NF-root-link/K5=(10,11,1,11,1,1,false)` と K3 版。
7. §8.9 の base / coordinate / tangential basepoint / orientation / loop をまとめた typed equality。
8. `root_normalization_level` 四値 enum。

しかし live status/provenance が v2.3 に同期していない。

- 104 行と 233・825 行は TB4-A20 をなお **「未監査」** とする。便 50 F2.1 で型修理後 PASS 済み。
- 106 行の live 状態表は checker を **25/25** とする。現物は 34/34。
- 560 行は checker をリポジトリ外 `scratchpad/tb4-monodromy-check.mjs` と記すが、現物は tracked な `search/tb4-monodromy-check.mjs`。

なお 34 番目の K3 check は、ラベルでは
\(\ker((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times)=\{1,7\}\)
を検査すると書く一方、コードは \(7\bmod6=1,\ 7\ne1,\ 12/6=2\) だけを見る。核の等式自体は紙上で正しく、本判定を変えないが、checker の主張範囲を正確にするなら units を列挙して `{1,7}` と比較するのがよい。

---

## F5. 束 4 — status/provenance と lint: **FAIL**

### F5.1 certificate 再束縛と発行順: **PASS**

BFC v2.8 digest、GAP script、Node counterpart の三 digest は certificate と一致し、25/25・fail-closed も確認した。commit の発行順も F8.3 に沿う。

### F5.2 CLAIMS W3-17: **FAIL**

W3-17 の中段は「現行 proof は \((Z_{2M}\)-link) 必要、TB4-E alternate は別 proof ID」と正しく書く。一方、同じ行の冒頭は

> (TB1)–(TB4)+CAL の下で (W1)–(W5) \(\Longrightarrow\) (5′)

と link を落とし、状態欄も

> framework-conditional on TB1–TB4+\((Z_{2M}\)-link)

とする。単一 claim 内で antecedent が一致しない。また `artifact 残差 0` は F2・F4 の現物反例により偽である。

「現行 proof」と「TB4-E alternate」を別 ID にする方針を維持し、W3-17 の冒頭・状態欄・artifact residual を同じ proof ID にそろえる必要がある。

### F5.3 preflight lint: **FAIL**

27 hit の個別分類だけが問題なのではない。lint の検出面そのものに穴がある。

1. `TOKENS` に**裸の \(b\)** の検査がなく、593・601・608・1145・1147 行を見ない。
2. B-9′ の「\(b=b_{\rm op}\) と宣言した次行で \(b=\varepsilon^{-1}\)」という**型の再融合**を見ない。
3. default scan は三文書だけで、`provenance/CLAIMS.md` の antecedent 不一致を見ない。
4. `ALLOW` は block 境界でなく、行中に `撤回` 等が一語あれば行全体を除外する。履歴引用と同じ行にある live 修正文まで無検査になり得る。
5. 実行結果自体が exit 1 である。人手 override を認めるなら、少なくとも source digest に束縛した `(file, line fingerprint, token, disposition, reviewer)` の triage record が必要である。

したがって「27 hit を全件見て live 違反 0」は再現可能な certificate になっておらず、実際にも live 違反を見落としている。

---

## F6. (β) 版イベント判定

**不許可。**

payload 別の判定は次のとおり。

| event component | 判定 |
|---|---|
| Rule 1 v1.4 の quarantine・root/A3 seals・typed equality・typed \(b\) schema | **設計 PASS**。ただし amendment の stale version と proof route を直すまで適用不可 |
| manifest v1.6 の BRIDGE-FAIL ①・三 bundle ID・結果 schema・版跨ぎ比較禁止 | **設計 PASS** |
| TB1/TB3/TB4\(^{\rm u}\)/A3、TB2+root seals、TB4-A20/B の札分離 | **設計 PASS**。TB4 live status の同期が先 |
| 文献要請 13(ii) の A3 向き確認への縮小維持 | **PASS** |
| B-9′(e′) の \(b_{\rm op}\) 形での全称復帰 | **FAIL**。現 B-9′(a) が link-free \(b_{\rm op}\) と \(\varepsilon^{-1}\) を再融合 |

イベント payload の設計は保持するが、次の最小再提出を要求する。

1. **BFC**
   - B-6tw / B-7tw の proof・解釈注・付録表まで \(b_{\rm op}\) へ同期。
   - B-9′(a) を
     \(b_{{\rm op},\rm sq}=b_{{\rm op},\rm ns}=(\bar t_M\varepsilon)^{-1}\)
     とし、証明にも \(\bar t_M\) の共通性を入れる。
   - 565 行を \(\bar t_M\) 型へ。
   - link 診断・依存・状態札を一つの current proof ID に統一。
2. **amendment**
   - 手順の `v2` を `v5` へ。
   - exact 回収の proof route を current / TB4-E alternate のどちらかに型付け。
3. **TB4**
   - live 状態表を 34/34・監査済みへ同期し、checker path を `search/` へ。
4. **provenance**
   - W3-17 を同じ proof ID・同じ antecedent に統一。
   - lint を少なくとも今回の反例を捕捉する形へ直し、再 triage。
   - 以上の本文修理後に digest を固定し直し、GAP certificate → CLAIMS → lint の順をもう一度実行。

この修理で BFC digest が変わるため、現 certificate の束縛は正しくても次版には持ち越せない。再束縛を省略してはならない。

本便は、既存の Freeze 1 / 既存探索許可を撤回するものではない。ただし **新版 predicate に基づく追加の event permission は出さない**。

---

## F7. T-16 への回答

「fixture を普遍含意形で書いた」ことを**一般の Markdown token lint だけで完全検出することはできない**。同じ `if` / `⇒` は正しい補題にも現れ、自由変数が全束縛されたかは構文と scope を読まなければ決まらない。

検出可能にするには fixture を prose でなく、例えば

```text
kind = negative_fixture
fixture_id
bindings = {M, t_2M, tbar_M, epsilon, b_cmp, b_op, link}
derived_by = TB4-3
assertion
```

という構造体にする。checker は

1. `assertion` の全自由変数が `bindings` にある、
2. `kind=negative_fixture` に `forall` / `implies` を置かない、
3. `derived_by` が欠落しない、
4. tuple 全体が期待値と一致する、

を fail-closed で検査できる。prose の `fixture ... ⇒ ...` regex は補助警報には使えるが、clean を意味論的 PASS と呼んではならない。

T-16 の \(L3\nRightarrow L4\) witness は正しい。mod \(20\) は \(2\)-進・\(5\)-進成分しか見ないので、\(3\)-進成分 \(-1\) は mod \(20\) で \(1\) のまま exact equality だけを破る。

---

## F8. ★教材

1. **typed alias の修理は statement の置換では終わらない。** 定義・proof の代入・一意性注・付録表・CLAIMS を同じ countermodel で貫いて初めて閉じる。
2. **「link-free に \(b_{\rm op}\) と書く」と宣言した直後こそ、\(\bar t_M\ne1\) の fixture を当てる。** 正規化下では永久に見えない再融合が一行で露出する。
3. **人手 triage は lint の exit code を消さない。** override するなら、source digest と各 hit の disposition を束縛した第二の certificate が要る。
4. **status table と checker path も theorem artifact の一部である。** 数学が正しくても 25/25 と 34/34、`scratchpad/` と `search/` が併存すれば、第三者はどの証拠を再走すべきか一意に決められない。

---

## F9. 共同設計者としての発案

### F9.1 live/history を keyword allowlist でなく block 型にする

```text
:::history version=v2.6
...
:::

:::normative theorem=B-6tw proof_id=current/link/v1
...
:::
```

のように範囲を明示し、lint は `normative` block だけを厳格検査する。行に「撤回」が含まれたという理由で全体を捨てない。

### F9.2 theorem symbol table

各 normative theorem に

```text
symbols:
  b_cmp : UnitMod(M)
  b_op  : UnitMod(M)
forbidden_unscoped: [b, t]
antecedent_bundle_id:
proof_id:
```

を付ける。これなら裸の \(b\)、level \(2M\) の \(t_{2M}\) と level \(M\) の \(\bar t_M\) の混同、proof ID と CLAIMS の前件差を同じ preflight で止められる。

### F9.3 triage manifest

正当な 27 hit を毎版人手で読み直す代わりに、各 disposition を **行番号ではなく normalized line hash** に束縛する。本文変更で hash が変われば triage は自動失効する。これにより「前版で否定形だった」という allowlist が次版の live 文へ漂流しない。

---

## F10. 監査範囲外申告

監査範囲外は、\(K^{(5)}\) の個別モデル・\(u\)・封印値、S5 Model-Builder の探索結果、Lean 形式化、外部文献原文である。GAP は本便では再生成せず、certificate の schema・値・三 digest を検収した。Node 二本と preflight lint は再走した。既存の非対象 dirty worktree は評価にも変更にも用いていない。
