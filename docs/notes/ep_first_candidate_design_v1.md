# EP 初回実候補の選定設計 — **循環は「単発実走」で破れる(探索でなく)**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 委嘱: 司令塔(次波 5)「裁定 292 方針 (A)。N∞ 枝の事前登録宇宙を読み、初の本番哨戒の対象とすべき候補(最小・pinned)を 2〜3 案、選定理由つきで提案(**決定は司令塔**)」
- 入力: `provenance/ninfty_freeze_receipt_sol75.md`(全文)/ `docs/week4-NInfty_stage2_spec_v18.md` §1.1 §2 §3 §7 / `docs/mb/委嘱3_報告.md` §4 / `certificates/mb/ninfty-branch-search-bound3.json` ほか 8 本 / `search/mb-ninfty-branch-search.mjs` L362–390
- **状態札: design(candidate)。決定は司令塔。本書は候補の指定と、選定の法的・数学的根拠のみ。**

---

## 0. ★ 本書の核心(先に 1 段) — 循環の解き方は「候補選び」より前にある

裁定 292 が同定した循環:
$$\text{EP 発効}\ \Longleftarrow\ \text{実物}\ \Longleftarrow\ \text{本番探索}\ \Longleftarrow\ \text{EP}$$

**この 3 番目の矢印は、実は成立していない。** sol75 receipt L55 の禁止条項は
> 「EP まで partial predicate / UNKNOWN。**calibrated detector・complete search 宣言は EP 前 NOT AUTHORIZED**」

であって、**「lane を走らせること」を禁じていない**。禁じられているのは *宣言* — すなわち「較正済み検出器である」「網羅探索を完了した」と**主張すること**である。spec v18 L653 も同文
> 「EP 不在中は `partial predicate / UNKNOWN`。freeze 後も `calibrated detector` / `complete search` と呼ばない」

> ### ⟹ 設計上の結論
> **初回の「実物」は探索(search)であってはならない。事前登録済みの 1 個の入力に対する「単発実走(unit run)」であるべきである。** 単発実走は
> - `complete search` を主張しない(1 点しか見ていないと cert に明記する)
> - `calibrated detector` を主張しない(判定は `partial predicate / UNKNOWN` 格のまま)
>
> したがって **receipt の禁止条項に一切触れずに、lane A / lane B の実出力と bundle receipt を生成できる**。循環は「新しい認可」ではなく「**探索と実走の区別**」で解ける。
> **これが本書の第一の提言であり、候補の選定はその下位の問題である。**

---

## 1. 事前登録された宇宙(確認)

**★ 用語の訂正**: 裁定 292 の「**W-6 系の事前登録宇宙**」という名前の条文は **repo に存在しない**(`W-6` は N∞ verifier の witness 記号 = `pushforward_compatibility_witness`、`mb_ninfty_verifier_contract_v13.md` L135)。実体は次の 2 つである。

**(U-1) 数学核の宇宙**(`week4-NInfty_stage2_spec_v18.md` §1.1):
$$C_{\rm crv}: y^2=f_6(x)\ (\deg f_6=6,\ \text{monic squarefree}),\qquad \mu=a(x)+p(x)y\ (\deg a=5,\ \deg p=2,\ a_5=p_2\ne0)$$
$$\textbf{(Pell)}\ a^2-f_6p^2=C\in\mathbf Q^\times,\qquad \textbf{(Or)}\ (\mu)=5P_0-5P_\infty .$$
入口契約 E-1〜E-6、target 条件 E-7(有限 branch 値が調和対 $\{s,-s\}$)。判定 lane の門 **T-1**: $\deg\gcd(a,a')=2$・$\gcd(a,a')$ squarefree・$\deg\gcd(a,a',a'')=0$・`rootpart(a)=[2,2,1]`。prediction field $K=\mathbf Q(\zeta_{20})$。

**(U-2) 走査した整数格子**(`search/mb-ninfty-branch-search.mjs` L362–390):
$\lvert a_0..a_4\rvert,\lvert p_0,p_1\rvert\le\text{BOUND}$、$a_5\in\{\pm1\}$、$p_2\ne0$。**実走済**: bound=3 全域(9,882,516 tested)+ bound=4 の 7 分割(計 86,410,020 tested)。**hits = 0**、stage1_passes = 744。

**★ 決定的な事実**: `docs/mb/委嘱3_報告.md` L113 —
> 「stage1 と stage2 を**同時に**満たす実際の $(a,p)$ タプル(genuine な positive control)は、探索範囲内(bound≤4)に見つかっていない」

**⟹ 事前登録宇宙の中に正例は 1 つも無い。** 初回実候補を「正例」から選ぶことは**不可能**であり、宇宙を広げれば事前登録の変更(= 新 receipt が必要)になる。**⟹ 初回実候補は負例側または中間(stage1 通過)側から選ぶしかない。** これが選定の数学的制約である。

---

## 2. 候補 3 案

### 【案 α】(最小・法的に最も安全) 事前登録済み negative fixture `ninfty-neg-01`

- **対象**: spec v18 §7 の negative fixtures `ninfty-neg-01..08`(期待 `REJECT`・理由コード `triple-root-of-a` / `a_root_partition=[3,1,1]` / `triple_gcd_degree>0` / `gcd_squarefree=false` の 4 欄回帰)。そのうち **01** を採る。
- **選定理由**:
 1. **宇宙の変更ゼロ**(既に spec 本文に凍結されている入力)。新 receipt 不要。
 2. **判定が決定的**(期待値が spec に書いてある)ので、lane A / lane B の**不一致がそのまま INTEGRITY_STOP** として意味を持つ。EP の目的(A/B 独立性の実証)に対して最も鋭い。
 3. **fail-closed 経路を通す**: `resolve_bundle` の race 修理(裁定 288)が守るのは「同一世代から A/B を取る」ことであり、REJECT 経路でもそれは同じく検査される。
- **弱点**: **T-1 の門で早期に落ちる**ため、lane A の幾何計算(local differential → $R$ on $C$ → $\mu_*R$)と lane B の飽和消去が**深くまで走らない**。「実物」としての情報量が薄い。
- **格**: 単発実走・`partial predicate / UNKNOWN`・`complete search` 非主張。

### 【案 β】(★ 推奨・本命) bound=3 走査の **stage1 通過 288 個のうち辞書順最小の 1 個**

- **対象**: `certificates/mb/ninfty-branch-search-bound3.json` に収蔵された `stage1_passes = 288` の中から、**係数ベクトル $(a_5,a_4,a_3,a_2,a_1,a_0,p_2,p_1,p_0)$ の辞書順最小**の 1 個を**機械抽出**して pin(cert の SHA-256 と抽出 command を receipt に束縛)。
- **選定理由**:
 1. **E-1〜E-6 と(少なくとも)stage1 を通る**ので、**両 lane が実際に幾何計算まで走る**。lane A の「local differential → $R$ on $C$ → $\mu_*R$」も lane B の「proven-baseline saturated elimination」も本番の深さで動き、**T-8(両 lane の finite aggregate partitions 比較)まで到達する**。「実物」として案 α より圧倒的に情報量が高い。
 2. 最終判定は stage2 で `REJECT`(hits=0 が保証)なので、**偽の positive 主張が生じる危険がゼロ**。EP 前に `calibrated detector` を主張してしまう事故が構造的に起きない。
 3. 選定規則が**機械的**(辞書順最小)なので、司令塔・数学者の恣意が入らない = **事前登録の精神に適う**。
 4. **宇宙の変更ゼロ**(bound=3 は実走済・cert 収蔵済)。
- **弱点**: 288 個の実体は cert の中にあり、**辞書順最小の 1 個を取り出す抽出器が新規に要る**(数行)。抽出規則自体を receipt に書いて束縛すれば恣意性は消える。
- **格**: 同上。

### 【案 γ】(較正の穴を埋める・中期) **人工正例の生成**は宇宙外 ⟹ **採らない**。代わりに「stage2 の型だけ満たす対象」

- 正例が宇宙内に無い以上、正例を作るには (i) bound を上げる (ii) 係数体を広げる (iii) 逆算構成(分岐データ $\{s,-s\}$ から $(a,p,f_6)$ を復元)のいずれかが要り、**(i)(ii)(iii) いずれも事前登録の変更**にあたる(新 receipt)。
- **⟹ 初回には採らない。** ただし**中期の課題として名指ししておく**: 「genuine positive control が宇宙内に存在しない」ことは、EP とは独立に **較正の穴**である(委嘱3 報告 L113 が自認済)。EP が発効した後の最初の仕事は、bound 拡大か逆算構成による正例の確保であるべき。
- **本書での位置**: **候補ではなく、EP 後の第一課題としての申し送り。**

---

## 3. 推奨と、実走の設計

> ### 推奨: **案 β を主、案 α を副として「2 点 bundle」で撃つ**
>
> **理由**: EP v11 の blocker だったのは **A/B bundle の原子性**(W92-6 の TOCTOU)であり、その修理(`resolve_bundle`・裁定 288)を実物で検証するには、**同一世代に複数の artifact が入っている**状況が要る。1 点だけでは bundle の意味が薄い。
> **⟹ 同一 freeze_id の 1 世代に、案 β(深い経路)と案 α(fail-closed 経路)の 2 対象を入れる。** 各対象について lane A / lane B が独立に走り、計 4 本の artifact + 1 本の bundle receipt が出る。これが W92-8 (c) の「実 A/B production artifacts と bundle receipt」の**最小かつ十分な形**である。

**実走設計(司令塔・implementer 向けの骨子)**:

| # | 段 | 内容 | 禁止事項の遵守 |
|---|---|---|---|
| 1 | 対象 pin | 案 β の抽出器(辞書順最小)を書き、その **source digest と出力係数ベクトルを receipt に固定**。案 α は spec の fixture id をそのまま引く | 探索ではない(1 個を取り出すだけ)✓ |
| 2 | lane A 実走 | searcher-v2 を**単発モード**で。出力に `run_mode: "unit_run"`、`complete_search: false`、`calibrated_detector: false` を必須欄として刻む | receipt L55 の 2 つの禁止宣言をしていない ✓ |
| 3 | lane B 実走 | checker + verifier-b。**別 runtime / 別 toolchain**(receipt の `separate implementations / runtimes / toolchains+build steps` = REQUIRED)| ✓ |
| 4 | bundle | 新 `freeze_id` で 4 artifact を 1 世代に commit。`resolve_bundle` で A/B を**一回の読みで**取得できることを実物で確認 | W92-8 (c) 充足 |
| 5 | CI | EP union を回す最小 workflow を新設(現在 7 workflow 全てに経路なし) | W92-8 (d) 充足 |
| 6 | 判定 | 両 lane の結果を T-8 で突き合わせ。**不一致は INTEGRITY_STOP**(spec §3)。一致しても判定格は `partial predicate / UNKNOWN` のまま | ✓ |

---

## 4. 予言(先出し・実走の答え合わせ用)

- **P-EP-1**: 案 β の対象は **T-1 を通過し、stage2(E-7 の調和対条件)で REJECT** になる。両 lane が同じ理由コードを返す。
- **P-EP-2**: 案 α の対象は **T-1 で REJECT**。lane A / lane B とも `a_root_partition` 欄で落ちる(4 欄回帰のうち 1 つ)。
- **P-EP-3**: 288 個の stage1 通過は $a_5=\pm1$ について**対称**(符号反転で写り合う)なので、辞書順最小を取ると $a_5=-1$ 側が選ばれる。
- **P-EP-4**(**外れてほしい予言**): 実走で lane A と lane B が**同じ finite aggregate partition を返さない**箇所が 1 つ以上出る。**もし出たら、それこそが EP を作った目的**(独立実装の食い違いの検出)であり、初回実走の最大の収穫になる。**出なければ機構の健全性の証拠**。

---

## 5. 数学者としての留保(正直に)

1. **本書は N∞ 枝の数学(命題 S5-3∞ とその周辺)を検分していない。** 読んだのは宇宙の定義・入口契約・走査記録・receipt であって、S5 系の証明ではない。**したがって「この候補が数学的に興味深い」とは主張していない** — 主張しているのは「**EP の機構を実物で検証するのに適した pinned 入力である**」ことだけである。
2. **正例が宇宙内に 1 つも無い**という事実(§1)は、EP とは独立に **N∞ 枝そのものへの警報**である。86,410,020 個を調べて stage1 通過 744・stage2 通過 0 という分布は、「探索範囲が狭い」か「条件が両立しない(= 命題 S5-3∞ の前件を満たす対象が実は稀/不在)」のどちらかを示唆する。**後者なら EP の先に何も無い。** 【要判断: 司令塔】— EP の完成に資源を投じる前に、**「正例が存在しうるか」を紙で押さえる**ほうが順序として正しい可能性がある。
3. **「W-6 系の事前登録宇宙」という条文は存在しない**(§1)。裁定 292 の文言は次の裁定で訂正しておくのがよい。

---

## 6. 格付け

| 項目 | 格 |
|---|---|
| §0 の「禁止されているのは宣言であって実走ではない」 | **設計提案(新規)**。receipt L55 と spec L653 の逐語に基づく。**法的解釈なので司令塔の裁定が要る** |
| §1 の宇宙の同定(U-1/U-2)と「正例ゼロ」 | **事実**(既存 cert と報告書の読み出し) |
| 案 α / β / γ | **提案**(決定は司令塔) |
| §3 の 2 点 bundle 推奨 | **提案** |
| §4 の予言 | **凍結予言**(未測定) |
| §5-2 の「N∞ 枝そのものへの警報」 | **candidate(要判断)** |
| N∞ 枝の数学的内容 | **未検分**(本書の射程外・正直申告) |
