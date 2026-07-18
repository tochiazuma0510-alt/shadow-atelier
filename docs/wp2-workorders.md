# WP2 作業指示書(implementer = Sonnet/medium 向け・2026-07-18 司令塔設計)

前提資料(必読): `docs/wp2-transversal-model.md`(12 規則とスキーマの正本)・`docs/week1-定義ノート.md` §2–4・`sol/sol_reply_01_definition_gate.md` §6(罠 12 件)・`AGENTS.md` の規律。

## WP2a — GAP 探索器(`search/suite-wp2-explorer.g`)

対象: dihedral K⁽ⁿ⁾(n ∈ {3..16})+ control N₅。出力: `certificates/<id>.v1.json`(スキーマ gtsh-cert/v1 どおり)。

1. 群構成: 12 規則で Q×T(12n 点 / N₅ は 30 点)上の σ̂₁, σ̂₂ を組む(`search/wp2-rules-verify.g` の実装を流用可)。起動時自己検査: braid・σ̂ᵢ²・ĉ = φc・|⟨σ̂₁,σ̂₂⟩| = 6|Q の PB₃ 像|。
2. 列挙(探索側): f 候補 = [F₂/N_F₂, F₂/N_F₂] の全元(**F₂/N_F₂ = ⟨x̂,ŷ⟩ の導来部分群** — 罠 6: full quotient の導来ではない)。各元に**代表語**(x,y の語)を BFS で付与。m ∈ {0..N_ord−1} で gcd(2m+1, N_ord) = 1。判定は簡約 hexagon (3.10)(3.11) + 全射性(Prop 3.6 の F₂ 版)。
3. double-check(探索器内): 通った (m,f) に full hexagon (3.3)(3.4) を Q×T 上でも検査(不一致は即 FAIL 報告 — 簡約形の前提バグ検出)。
4. kernel_cert: dihedral は Lemma 4.2 の (h₁,h₂,h₃)(b = affine j↦(2m+1)j、h₁ = r^{−2k−m}b, h₂ = b, h₃ = b(m 偶)/bs(m 奇))を各 shadow に付け、(4.11) の 2 等式を GAP で検査してから書き出す。N₅ は type=brute(kernel を直接計算し index 30 を確認)。
5. composition_table(全対・(3.53) で)・inverse_map((3.54))・reduction(K⁽⁸⁾→K⁽⁴⁾, K⁽³⁶⁾→K⁽¹²⁾, K⁽¹²⁾→K⁽⁴⁾, K⁽¹⁸⁾→K⁽³⁾, K⁽⁹⁾→K⁽³⁾ — q 側 n=18,36 も構成)・ls_witness(3|n: 全許容 (m,k)、Thm 5.2 証明の式で g,h を構成し (5.1) を検査してから書き出す)。
6. counts は全段を記録(silent cap 禁止)。Thm 4.3 の閉じた式との比較は**書き出すだけ**(判定は照合器の仕事 — 期待値に合わせにいかない)。
7. 実行: `.\gap.ps1 search\suite-wp2-explorer.g`。10 分 cap 超過や候補爆発は実装せず報告。

## WP2b — node 照合器(`crosscheck/check.mjs`)

**独立実装**: GAP スクリプトを読まない・流用しない(仕様は wp2-transversal-model.md のみ)。依存ゼロ(node 標準のみ)。

1. Q×T モデルを整数演算で自前実装(Dₙ 元 = [a,e]、積 (a,e)(b,δ) = (a+(−1)^e b mod n, e+δ mod 2)※左作用の合成順に注意 — 起動時自己検査で σ̂ᵢ² などを必ず確認)。
2. `certificates/*.v1.json` を読み、スキーマの検査項目 ①〜⑩(wp2-transversal-model.md 記載)を全実行。
3. Thm 4.3 の閉じた式(𝒳ₙ・ϰ・4|n の parity 条件・k の法 n₁ — 罠 8 の正準化)を自前実装し、証明書の shadow 集合と**集合として**比較。
4. Thm 4.6 の群構造(Aff(ℤ/n₀)×𝒵₂ / ×H̃_α)との同型検査: 写像 ϱ (4.15) を実装し composition_table と突合(u の法 2n — 罠 7)。
5. 出力: `crosscheck/verdicts/<id>.v1.verdict.json`(項目別 PASS/FAIL+個数+所要時間)。**全項目 PASS の対象だけが cross-checked** — 1 個でも FAIL なら理由つきで報告。
6. 実行: `node crosscheck\check.mjs`。

## 完了条件(両 WP)

- 全対象(K3..K16+N5)で explorer が証明書を出し、checker の verdict が全項目 PASS。
- 不一致が出たら**どちらが正しいか決めない**で司令塔に差し戻す(数学判断は上位の仕事)。
- 報告: 変更ファイル・実行コマンド・counts 表・verdict 要約・逸脱と懸念。
