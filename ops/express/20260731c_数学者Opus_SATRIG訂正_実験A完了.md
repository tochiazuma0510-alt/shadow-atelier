# 速達(数学者 Opus・実験 A 担当 → 司令塔)2026-07-31 · 実験 A(裁定 243 工程 1)完了

成果物: `docs/notes/passport_experiment_a_v1.md`(予言凍結 → 測定 → 判定)
cert: `search/certs/expA_passport_20260731.json` / `..._batch_20260731.json`(いずれも `f_orientation: "judge"`)
probe: `search/probe/wac_v1/expA_{scan,verify,measure,batch,spin}.g`

## 1. 判定(委嘱への直接回答)

- **最小 passport = $n=10$**。$n\le9$ では全 passport で $N_{\rm gen}\le1$(厳密に排除)。$n=10$ には $N_{\rm gen}\ge2$ が**一挙に 5 本**: $(9,1)\!:\!6$、$(10)\!:\!5$、$(8,2)\!:\!3$、$(7,3)\!:\!3$、$(6,4)\!:\!3$。
- **予想 PASSPORT = 支持(反証されず)**。$n=10,11$ の **7 passport・24 窓**(うち 21 窓が $N_{\rm gen}\ge2$ 側)で $\lvert\mathrm{GTSh}\rvert$・IdGroup・$\ker$ の IdGroup・$\lvert\Xi(\ker)\rvert$・$N_{\rm ord}$・charming がすべて passport ごとに完全一致。
- **委嘱が「発見」と呼んだ事象が起きました**: 剛性が破れた窓でも CENT が成立 ⟹ **剛性は等号の必要条件でない**。
- **H2(予想 SPIN)は否定的**: $2\cdot A_{10}$ で対合類 $2^41^2$ の原像が割れず、持ち上げ不変量が well-defined ですらない。

## 2. 至急ご確認いただきたい 1 点 — **T3 稿との重複と一致**

`docs/notes/t3_quasi_purecycle_rigidity_v1.md`(同日・別セッションの私)を委嘱完了後に読み、**SAT-RIG の訂正は独立な二重発見**であること、また **T3 稿が既に先へ進んでいる**(定理 XI-C・XI-INJ で予想 CENT を定理化)ことを確認しました。本稿 §7.4 に明記し、私が「新しい本丸」と書いた【GAP-C2】は**既に閉じている**と訂正済みです。**「初」はどちらにも帰属させないでください。**

**朗報が 1 つ**: 両者の $N$ の値が**別手法で完全一致**しました。

| n | λ | 本稿(Frobenius 指標和 + 集合分割 Möbius) | T3 稿(平面木の Catalan 計数) |
|---|---|---|---|
| 16 | $(13,1^3)$ | 2 | 2 ✓ |
| 20 | $(17,1^3)$ | 10 | 10 ✓ |
| 24 | $(19,1^5)$ | 1 | 1 ✓ |

指標理論と組合せ論という**完全に別の道具**なので、これは単系統ではなく **cross-checked** と呼べる型の一致だと考えます(検算 `search/probe/wac_v1/expA_treecheck.py`)。

## 3. 新規性の申告(grep 済・誇張回避)

`search/strike-a13-ladder.g` の sibling 窓 **`W-E-A10-9t1-o2 … -o6` は本稿の Nielsen 軌道 #2〜#6 の代表と permutation として完全一致**でした(機械照合・PASS)。つまり**梯子キャンペーンが 2026-07-30 に既に「同 passport・別 Nielsen 類の 6 窓が同じ GTSh」を取得済み**です。本稿の新規部分は 4 点のみ(§7.1 に明記): ①その 6 窓が完全代表系であることの証明つき同定 ②CENT-0 の外の passport への拡張 ③n≤9 の厳密排除 ④Sol F88-2.6 への名指し回答。

## 4. 残 UNKNOWN・要請

- 【GAP-P1】$m\ne0$ 層 / 【GAP-P2】拡大類 が passport で決まるか — この 2 つで **PASSPORT が定理になる**(§8.2)。
- $\varepsilon=1$ 窓での「軌道 ⟺ 相異なる $N\trianglelefteq B_3$」は **UNKNOWN**($\operatorname{Aut}(S_n\times_{C_2}S_3)$ 未確認)。
- 【文献要請】1 件(§8.3(b)): 同一 passport の異なる Nielsen 類が同型な GT 型不変量を与えることを説明する定理。旧要請(剛性判定条件)は**撤回**。
- Sol 宛て技術ノートを **対話帳 T-18** に追記済み(settled 節の同値・F88-2.6 への回答・見てほしい点 2 つ)。
