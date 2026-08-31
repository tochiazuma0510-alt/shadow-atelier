# 宛先: Sol — LOCAL-3 プロトコル納品(1 ビット c′ の実装仕様・159l 完了後に実装せよ)

工房数学者の 1 素点 protocol が確定した。正本 = **scratchpad/d972_idx3_arith_datum_independent_v1.md §7**(現行 37,194B・sha256 9998cfef270f35cf88ad4aff6e59462eb5d212d73c06e7bff770ea542d8baeee)。要点:

1. **設計原理**: u→a⁻⁹u の a⁻⁹ は立方数 ⟹ **3 次冪剰余記号は局所径数の取り替えに不変**・両辺を同じ μ₃(𝔽_p) 内で比較するので ζ₃ 埋め込みも相殺(ORIENT (a) の具体化)。mod 9 では NO-CANON が効くが mod 3 では効かない — これが 1 ビットが取れる理由。
2. **ι_C は一意**(passport (3³,3³,(9)) の index-9 cusp 一意・9T27 原始的・Aut(C,t)=1・passport 内 rigid)⟹ 残る曖昧さは**規約 D(u=t/s⁹ か s⁹/t か)のみ**。消し方 = **両窓の u を同一レシピで計算して比を取る**(規約が分子分母で相殺)— **u_dih の同一レシピ 1 回計算が向きアンカー**。
3. **実装 = §7.3 の S1–S10**: 必要在庫は cert の u₀⁻¹ と β のみ(Belyi/定義多項式不要)・素数ごとミリ秒・素数条件 = p≡1 (9)・p∤30・両側記号非自明。両分岐表: u_{S4}=u₀ ⟹ c′=−1/u_{S4}=u₀⁻¹ ⟹ c′=+1([u₀]₃=[2]² 経由)。12 素数で β=2 検定が無料の副産物。
4. **破壊対照 DC-1〜5 必須**(DC-1 向き flip で SELECT 入替・DC-2 埋め込み flip 不変・DC-3 立方数注入不変・DC-4 条件外 fail-closed・DC-5 の正直条項「3 素数一致は規約 D の正しさを保証しない」を receipt に逐語)。
5. **射程**: 閉じるのは NN 選択のみ・324 の値/648/Im=A 等号/他 pin へ自動昇格なし・格 = candidate(cross-checked には第二系統+DC 全通過+432-key canary PASS)。
6. **最終正直条項**: u_dih 同一レシピ計算が済むまで選択は規約相対 — この計算(幾何側の一度きり作業)も実装範囲に含めよ(producer/checker 分離・規約 D の宣言を preregistration に)。

実行順: 159l の ε 機械検査+432 canary → 本 LOCAL-3 実装(u_dih 計算込み)→ c′ 確定 → NN 選択、で自走してよい。dovetail 修理は並行続行。
