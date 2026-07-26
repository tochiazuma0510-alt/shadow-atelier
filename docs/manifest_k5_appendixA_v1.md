# manifest_k5_v1.md 付録 A — fixture 実データ表(v1・2026-07-27・実装担当)

> 便 31 P1(裁定 29)の実装物。manifest 本文(`docs/manifest_k5_v1.md`)が要求する
> 「fixture の実体(§宇宙・fixture の実体)」「較正三層 1・2」を、**値として**埋める。
> **★教材 19 の遵守**: すべての数値はここに手で書き写す前に `search/k5-fixture-serialize.mjs`
> が計算し、`certificates/k5fixture/*.json` に書き出し、その sha256 を機械計算している。
> 本稿の数値は、その出力を機械転写したものであり、独立に打ち直してはいない。
>
> **射程の宣言**: 本稿は manifest 付録 A の要求項目を埋めるものであり、(4d)(5′)・u・
> 固定体・算術側には一切触れない。K5 側の群論構成は D1(`docs/week4-K5橋_D1_opus_v1.md`)
> と `search/week4-k5-bridge-d1.mjs`/`.g` が既に二系統(node+GAP)で確立した対象であり、
> 本稿の役目は「新しい定理の独立導出」ではなく「fixture 実データの切り出しと canonical
> serialization」である。したがって本稿の `search/k5-fixture-serialize.mjs` は D1 の座標系
> をそのまま再利用しており、**「探索器と照合器の分離」における独立クロスチェックには
> 数えない**(D1 mjs/g の二系統一致がその役目を既に果たしている)。

---

## 0. canonical serialization 規約(すべての fixture に共通・固定)

`search/k5-fixture-serialize.mjs` が実装する規約:

| 項目 | 規約 |
|---|---|
| 文字コード | UTF-8(BOM なし) |
| 改行 | LF のみ |
| JSON キー順序 | オブジェクトのキーをコードポイント昇順に**再帰的に**正規化(`Object.keys().sort()`)。配列の要素順序はそのまま保持する(位置に意味があるため — 例えば `perm_triple` の配列は「点 i の像」という位置情報そのもの) |
| 区切り文字 | コンパクト形式(`JSON.stringify` の第 2/第 3 引数を使わない・余分な空白なし) |
| ファイル末尾 | LF 1 個 |
| sha256 対象 | 上記直列化バイト列(UTF-8)全体(末尾の LF を含む) |

出力先: `certificates/k5fixture/{K5-sq,K5-ns,K3-regression}.json`(canonical 直列化そのもの — 別途「読みやすい版」は作らない。ハッシュの対象と保存物を一致させるため)。

**envelope の明記(便 32 F1.2)**: `sha256` は当然ながら自己 hash される JSON payload 内には置けない。したがって各 fixture の実体は「payload の 6(K3-regression は 8)field」+「その外側の envelope の digest」という構成であり、`sha256` の値そのものは payload に含まれない外部添付(このドキュメントの表・付録 A §1–2)としてのみ存在する。循環 hash を避けるための型の区別であって、payload の完全性は変わらない(Sol 便 32 F1.2)。

---

## 1. K5 finite fixture(二類代表)

### 1.1 共通の marking_version

- 正本参照: `docs/notes/抽出_Kn定義_D1.md` (3.6)、$n=5$。
- 座標: $X = \bar x = (r,s,s)$、$Y = \bar y = (rs,r,rs)$、$Z = \bar z = (r^2s, r^{-1}s, r)$ in $D_5^3$。
- $D_5$ の符号化: $r^a s^e$ を `code = 2a+e (mod 10)` で表す(`search/week4-k5-bridge-d1.mjs` 冒頭と同一)。
- $D_5^3$ の符号化: 元 = `c0 + 10*c1 + 100*c2` (0..999)。$G_5 := \langle X,Y\rangle$(500 元)。
- 作用規約: 部分群 $H$ に対し $\Lambda := \{H$ の $G_5$-共役$\}$。coset 作用は**左剰余類** $gH$ 上、$g \mapsto (Xg)H$ の左乗算。

### 1.2 K5-sq(代表・$\alpha = 1$、平方剰余類 $\{1,4\}$)

**H_generators**(D_5^3 の三つ組表記 $(r^{a_1}s^{e_1}, r^{a_2}s^{e_2}, r^{a_3}s^{e_3})$):

- $U_{25}$(R 内の 2 次元部分空間)の基底: $\{(1,\ r^1,\ 1),\ (r^1,\ 1,\ r^1)\}$
- $H\setminus R$ の対合生成元: $(r^0s,\ 1,\ r^0s)$
- $H = \langle U_{25}\text{-基底},\ \text{対合生成元}\rangle$(位数 50)

**perm_triple**(one-line・0-indexed・積の規約 $(p\circ q)(i) = p(q(i))$):

- $\sigma_0 = [1,2,3,4,5,6,7,8,9,0]$(標準 10-サイクル)
- $\sigma_1 = [0,1,8,9,6,7,4,5,2,3]$(型 $2^41^2$)
- $\sigma_\infty = [3,0,1,8,9,6,7,4,5,2]$(標準 10-サイクル)
- 検算: $\sigma_0\sigma_1\sigma_\infty = \mathrm{id}$(S7 PASS)

**normalization_algorithm**:

1. **クラス代表の選択(tie-break)**: $\Lambda_{\rm sq}$ に属する 10 個の共役部分群のうち、要素集合(0..499 の整数)を昇順ソートした配列を**数値辞書式比較**して最小のものを代表 $H$ とする(一意・決定的)。
2. **点のラベル付け**: 基点 $p_0 := H$ 自身の coset。ラベル $\mathrm{label}(gH) := i$ s.t. $X^i H = gH$($\langle X\rangle$ は $\Lambda$ 上単純推移ゆえ矛盾なく一意)。$\sigma_0$ の方向は「$X$ による左乗算」($X^{-1}$ ではない)に固定。
3. **残る自由度**: 基点と方向を両方固定した時点で回転・鏡映の自由度は残らない。追加の tie-break は不要。

**tie-break の定義追記(便 32 F1.3・裁定 31 P4)**:

1. 上記「要素 $0,\ldots,499$」は、昇順に並べた raw $D_5^3$ code の $G_5$-list($G_5=\langle X,Y\rangle$ を `search/k5-fixture-serialize.mjs` が構成する際の配列、コード $0$..$999$ のうち $G_5$ に属するものを昇順ソートしたもの)における **index**(0-indexed の通し番号)である。$H$ の「要素集合」とは、この index の集合を指す。
2. coset $gH$ と、manifest 本文・付録 A が共役類作用として使う $H\mapsto gHg^{-1}$ を結ぶ写像は
   $$ gH\ \longmapsto\ gHg^{-1} $$
   である。$N_{G_5}(H)=H$(good 側の判定条件そのもの)により、$g_1H=g_2H \iff g_1Hg_1^{-1}=g_2Hg_2^{-1}$ が成り立つのでこの写像は well-defined かつ全単射であり、$X$ による coset の左乗算($gH\mapsto (Xg)H$)と $X$ による共役($K\mapsto XKX^{-1}$)を **intertwine** する(すなわち上記写像は $\langle X\rangle$-同変)。

**ρ₀・j_i・a**: $\rho_0$ は $\Lambda_{\rm sq}$ 上で忠実(5 元が相異なる・S11 PASS)。$j_{\rm sq}(k$ を $F_0$ の添字として$) = [0,4,3,2,1]$(S12 で全域定義を確認)。**a_sealed = 1**(S13 PASS)。

**passport**: 次数 10・$(10,\ 2^41^2,\ 10)$・種数 2・$\mathrm{Aut}(\text{dessin}) = 1$。

**evidence_ids**: D1-search-{D3,D4,D6,D7,D8,D9-(3a),D9-(3b),D9-(3c),D9-(3d),D13,D14,D15}(`search/week4-k5-bridge-d1.mjs`)/ D1-gap(`search/week4-k5-bridge-d1.g` の対応項目・52/52 PASS 中)/ D1-{I1,I2,I3,I4}(同 mjs)/ D1-gap-I1I3(同 .g)/ k5-fixture-serialize-S1..S13(本便・下記 §4 の実行結果)。

**sha256(canonical serialization)**:
```
a49252af8a09031137ee2a5621b7a1eb9c2a6506849afad14dfe74a38a876716
```
格納先: `certificates/k5fixture/K5-sq.json`

### 1.3 K5-ns(代表・$\alpha = 2$、非剰余類 $\{2,3\}$)

**H_generators**:

- $U_{25}$ の基底: $\{(1,\ r^1,\ 1),\ (r^2,\ 1,\ r^1)\}$
- $H\setminus R$ の対合生成元: $(r^0s,\ 1,\ r^0s)$
- $H = \langle U_{25}\text{-基底},\ \text{対合生成元}\rangle$(位数 50)

**perm_triple**:

- $\sigma_0 = [1,2,3,4,5,6,7,8,9,0]$
- $\sigma_1 = [4,7,2,5,0,3,8,1,6,9]$(型 $2^41^2$)
- $\sigma_\infty = [9,4,7,2,5,0,3,8,1,6]$
- 検算: $\sigma_0\sigma_1\sigma_\infty = \mathrm{id}$(S7 PASS)

**normalization_algorithm**: K5-sq(§1.2)と同一規則(クラスを $\Lambda_{\rm ns}$ に読み替え)。

**ρ₀・j_i・a**: $\rho_0$ は $\Lambda_{\rm ns}$ 上で忠実(S11 PASS)。$j_{\rm ns} = [0,4,3,2,1]$(K5-sq と字面まで同一 — 命題 K5-a の帰結、S12/S13)。**a_sealed = 1**。

**passport**: K5-sq と同一(次数 10・$(10,2^41^2,10)$・種数 2・$\mathrm{Aut}=1$)。

**evidence_ids**: K5-sq と同一リスト(下記 §4)。

**sha256(canonical serialization)**:
```
0ce28a6d6b7a3687dc07811f66a05fede464bc3a30efb1a126a913adfa2ccd81
```
格納先: `certificates/k5fixture/K5-ns.json`

---

## 2. K3 regression fixture

| 項目 | 値 | 出所 |
|---|---|---|
| モデル | $t^2+(x-1)^2(4x-1)t+4x^6=0$(LMFDB 6T9-6_6_2.2.1.1-a plane model) | `search/week4-u-k3.mjs` 冒頭コメント |
| branch 割当 | $\lambda = -t$: $t=0\mapsto\lambda=0$(型 $[6]$)・$t=-1\mapsto\lambda=1$(型 $[2,2,1,1]$)・$t=\infty\mapsto\lambda=\infty$(型 $[6]$) | 同スクリプト §5 コメント・検算 (5)(6) |
| 節点(分岐点でない) | $(x,t)=(1/3,-2/27)$ は平面モデルの特異点 | 検算 (3) |
| **exact conjugator** | $h = [2,3,5,6,4,1]$(one-line・1-indexed) | **裁定_28_f29_conjugator.md 裁定 1**(正典値)・再計算 `search/week4-19a19e.mjs` 検算 (3) = 一意(S₆ 全 720 悉皆) |
| 規約 (i) | $\bar x,\bar y,\bar z$ は good[0] 剰余類(次数 6・6 点)への左作用の固定ラベル付け | 裁定 28 裁定 1 |
| 規約 (ii) | $\sigma$ 三つ組は 6T9 辞書式最小代表を $\lambda$ 割当に整列済みのもの(LMFDB ラベルの生の順ではない) | 同上 |
| 規約 (iii) | $(p\circ q)(i) = p(q(i))$・共役は $hxh^{-1}$ | 同上 |
| $\sigma_0,\sigma_1,\sigma_\infty$(6T9 標準代表) | $\sigma_0=[2,3,4,5,6,1]$、$\sigma_1=[1,2,5,6,3,4]$、$\sigma_\infty=[4,1,2,5,6,3]$ | `search/week4-19a19e.mjs` 実行出力(本便で再実行し確認・検算 (3)(3b)(3c) = 7/7 PASS) |
| $G_3$ 側次数 6 表現($h$ で共役される前) | $\bar x=[2,5,4,6,3,1]$、$\bar y=[1,3,2,5,4,6]$、$\bar z=[6,1,4,2,3,5]$ | 同上 |
| cusp / uniformizer | $P_0 = (x,t)=(0,0)$(全分岐 cusp・$\lambda=0$ 上)、uniformizer $= x$(ℚ-有理)、$t = 4x^6+O(x^7)$ | `search/week4-u-k3.mjs` 検算 (7)(8) |
| その正規化での $u$ | $u = -4$ | 検算 (9) |
| $\mathrm{ord}([u^{-1}]_6)$ | $3$ | 検算 (10)(11)(12) |
| covariance control $u'$ | $u' = -256/729$($t=\infty$ 側のもう一方の全分岐 cusp) | 検算 (13)(14)(15)(16) |
| Möbius 不変性 | $[u]_3 = [u']_3 = [2^2]$($u\ne u'$ だが 3-剰余類は同じ) | 検算 (16) |
| $\tau$ の向き | $\langle\bar x\rangle\to\mu_M$: 全分岐 cusp の ℚ-有理局所助変数 $s$ に対し $s^{1/M}\mapsto\zeta_M s^{1/M}$。生成元の向きの曖昧さは判定にも固定体にも影響しない | `docs/week4-K3飽和_opus_v3.md` 「$\tau$ の $\mu_M$ 側の同定」節 |
| $\rho_0$ の定義 | $\rho_0:\mathfrak F_0\to\mathrm{Sym}(\Lambda)$。$\mathfrak F_0=\ker\tilde\chi\cong C_3\subset\mathrm{Aut}(G_3)$($G_3\le D_3^3$、$\lvert G_3\rvert=108$、D1 (3.6) $n=3$ 座標)。$\Lambda=H$ の $G_3$-共役類(6 元、ordered passport $(6,2^21^2,6)$ 側) | `docs/week4-K3飽和_opus_v3.md` §5.2.3・表(§0 の定義表)/ `search/week4-k3-v2-repairs.mjs` T7-T8 |
| $\Lambda$ の列挙順 | `conjClass(H)`($G_3$ を昇順 0..107 で走査し重複除去)の順。$H$ は target クラス(6 個の共役部分群)のうち要素集合の数値辞書式最小で一意固定(K5 と同じ tie-break 規則。good[0] のような列挙順依存ではない) | `search/k5-fixture-serialize.mjs` PART 2c(K3x2) |
| $\rho_0$ の生成元・像(実値) | $F_0$ の生成元 $\Phi_{(m{=}0,k{=}1)}$(位数 3): $\rho_0(\Phi_{0,1}) = [1,2,0,4,5,3]$(one-line, 0-indexed、型 $3.3$)。$\rho_0(\Phi_{0,2}) = [2,0,1,5,3,4]$。$\rho_0(\Phi_{0,0}) = \mathrm{id} = [0,1,2,3,4,5]$ | `search/k5-fixture-serialize.mjs` PART 2c(K3x5)= `search/week4-k3-v2-repairs.mjs` T8d(実値一致を本便で突合) |
| $\tau$ の生成元作用(実値) | $\tau_{tt} := (X$ の $\Lambda$ 上の共役作用$)^{tt}$($tt=0..5$)。$\mu_6[3]$ の生成元 $\tau_2 = [2,0,1,5,3,4]$($\rho_0(\Phi_{0,2})$ と字面一致) | `search/k5-fixture-serialize.mjs` PART 2c(K3x6) |
| $j$ の表(実値) | $j(\tau_{2\cdot tt\bmod 6}):=k$ s.t. $\rho_0(\Phi_{0,k})=\tau_{2\cdot tt\bmod 6}$。$tt=0\mapsto k=0$、$tt=1\mapsto k=2$、$tt=2\mapsto k=1$(全域定義・(1.1) の実値化) | `search/k5-fixture-serialize.mjs` PART 2c(K3x7) |
| 向きの注(便 32 F1.4) | 生成元(★$X$ の向き・$F_0$ の $k=1/2$ のどちらを「正」とするか)の選択は $j$ の見た目(どの $tt$ にどの $k$ が対応するか)を入れ替えるが、$\rho_0$ の忠実性・固定体の同定には無影響。上表は $\tau_2:=(X$-共役作用$)^2$ を正の向きとする一つの明示的選択のもとでの値 | `docs/week4-K3飽和_opus_v3.md` 同節・注 4 |

**evidence_ids**: K3-19a19e(`search/week4-19a19e.mjs`・7/7 PASS 本便再実行済)/ K3-u-k3(`search/week4-u-k3.mjs`・16/16 PASS 本便再実行済)/ K3-裁定28(`sol/裁定_28_f29_conjugator.md` 裁定 1-5)/ K3x0-K3x7(`search/k5-fixture-serialize.mjs` PART 2c・本便新設・$\rho_0$/$\tau$/$j$ の実値生成と `search/week4-k3-v2-repairs.mjs` T8d との突合)。

**sha256(canonical serialization)**:
```
71c609ed75b00737b6d163a922340001593379d64b28d6479ac553845f515776
```
格納先: `certificates/k5fixture/K3-regression.json`

**ハッシュ履歴**:

| 版 | sha256 | 変更内容 |
|---|---|---|
| v1(便 31) | `70f2a6040d0bff85e4c597a6059cfb7151193f1de0c23d20a53f0dc9b2529ed9` | 初版。`tau_rho0_j_orientation` は $\tau$ のみ(Sol 便 32 F1.4 が欠品と指摘) |
| v2(本便・便 32 P4) | `71c609ed75b00737b6d163a922340001593379d64b28d6479ac553845f515776` | $\rho_0$ の生成元/像・$\tau$ の生成元作用・$j$ の表(実値)を追加。`exact_conjugator` に good[0] の provenance 降格 note を追加。K5-sq/K5-ns の sha256 は不変(`node search/k5-fixture-serialize.mjs` 再実行で確認済み) |

---

## 3. 検証(D1 既存検算との再照合)

`search/k5-fixture-serialize.mjs` は D1 の座標系(`search/week4-k5-bridge-d1.mjs` と同一の $D_5^3$ 符号化)を独立に書き直し、以下を**再計算**して D1 の該当項目と一致することを確認した(2026-07-27 実行・**14/14 PASS**):

| 検算 | 内容 | D1 対応項目 |
|---|---|---|
| S0 | $\lvert G_5\rvert = 500$・$\bar x\bar y\bar z=1$ | A1・A3 |
| S1 | $R$ の位数 25 部分群 31 個・位数 50 部分群の全列挙(93 個) | D1・D2 |
| S2 | qualifying 50・good 40・target(passport $(10,2^41^2,10)$)20 | D3・D4・D6 |
| S3 | 2 共役類の $\alpha$ 不変量 $\{1,4\}$ / $\{2,3\}$ | D7・D8 |
| S4 | クラス代表の tie-break で $\alpha(H_{\rm sq})=1$, $\alpha(H_{\rm ns})=2$ を一意固定 | (本便で新設した正規化規則) |
| S5・S6 | 標準ラベルで $\sigma_0$ = 標準 10-サイクル | (本便で新設) |
| S7 | $\sigma_0\sigma_1\sigma_\infty=\mathrm{id}$ | D9-(3c 相当) |
| S8 | $\sigma_1$ の型 $= 2^41^2$ | D6 |
| S9 | H_generators が実際に $H$(位数 50)を再生成する | D1・D2 の構成手続き |
| S10 | $F_0$ が 5 元 | B5 |
| S11 | $\rho_0$ が両クラスで忠実 | E3・E9 |
| S12 | $j_{\rm sq}, j_{\rm ns}$ が全域定義 | I1 |
| S13 | 封印値 $a=1$ | I2・I3(node)・I1-I3(GAP) |

実行コマンド(v1・便 31): `node search/k5-fixture-serialize.mjs` → `=== 14/14 PASS ===`。

**追加(v2・便 32 P4)**: `search/k5-fixture-serialize.mjs` に PART 2c(K3x0-K3x7 の 8 項目・K3-regression の $\rho_0$/$\tau$/$j$ 実値生成)を追加し、`=== 22/22 PASS ===`(14 + 8)。K3x5 で `search/week4-k3-v2-repairs.mjs` T8d の $\rho_0$ 実値(置換 `012345 | 120453 | 201534`)との一致を assertion として確認した。K5-sq/K5-ns の PART 1/S0-S13 は無変更(sha256 不変で裏付け)。

`search/week4-19a19e.mjs` と `search/week4-u-k3.mjs` も本便で再実行し、それぞれ **7/7 PASS**・**16/16 PASS** を確認した(§2 の出所欄に反映済み)。

---

## 4. 検算項目数まとめ

| 表 | 項目数(fixture_id / marking_version / H_generators / perm_triple / normalization_algorithm / evidence_ids / sha256 の 7 フィールドで数えると) |
|---|---|
| K5-sq | 7 フィールド + passport・rho0_and_j・class_invariant の補助 3 = 計 10 |
| K5-ns | 同上 10 |
| K3-regression | fixture_id・model・exact_conjugator・cusp_and_uniformizer・u・covariance_control・tau_rho0_j_orientation・evidence_ids の 8 |

---

## 5. 懸念・報告事項(実装担当より)

1. **sha256 の桁数確認**: 3 個の digest はいずれも 64 桁(`node -e` で `.length` を実測して確認済み)。転記前の自己点検で一度桁数を誤読したが、実測により 64 桁で正常と確定した。
2. K3-regression fixture の $\sigma$ 三つ組・$G_3$ 側次数 6 表現は `search/week4-19a19e.mjs` の**この 1 回の実行**での出力である(good[0] の選び方は部分群列挙順に依存するため、環境やバージョンが変わると `good[0]` 自体が変わりうる——ただし裁定 28 が pin した $h$ の値自体は変わらないので、$h$ の正典性には影響しない)。**便 32 F1.4・裁定 31 P4 により格下げを明文化**: authoritative value は本稿・fixture JSON 内の明示三つ組($\sigma_0,\sigma_1,\sigma_\infty$・$\bar x,\bar y,\bar z$)と明示 $h$ であり、`good[0]` という選び方自体は再現 recipe ではなく provenance(どの実行から転記したかの記録)である。この降格 note を `certificates/k5fixture/K3-regression.json` の `exact_conjugator.good0_authoritative_note` として fixture 本体にも記入した。
3. 本稿は u・固定体・算術側には触れていない。§2 の $u=-4$・$u'=-256/729$ は「K3 の既知回帰データの引用」であり、K5 側の新しい u 抽出ではない(K5-sq/K5-ns fixture には u を含めていない)。**同じ理由で本便で追加した $\rho_0$/$\tau$/$j$ の実値(PART 2c)も、既存の `search/week4-k3-v2-repairs.mjs`(T7・T8・cross-checked 43/43)が確立した対象の値の切り出しであり、新しい独立クロスチェックとしては数えない**(§0 冒頭の射程宣言と同じ扱い)。

---

## 6. 版表(§8.6 下準備・便 32 P4)

manifest 本文 §8.6/§10 が要求する「実装版・commit・checker ID」欄への値の下準備。**本便では git commit を行っていない**(実装担当の規律)ため、下表の commit hash は「本便の編集直前(working tree 変更前)の HEAD」であり、`search/k5-fixture-serialize.mjs` は本便で内容を変更したため次回コミット後にハッシュが変わる。司令塔が P7(便 34 再提出)で確定値に更新すること。

| component | 役割 | 直前 commit(便 32 時点) | 備考 |
|---|---|---|---|
| `search/k5-fixture-serialize.mjs` | fixture 実体化・canonical serialization 生成器(PART 1/2/2c/3) | `25c37e209b655d29af707b6fe0bbc25730b70300` | **本便で PART 2c を追加・未コミット**(git status で確認)。コミット後に新 hash へ更新要 |
| `search/k5-blocks-check.g` | K5-sq/K5-ns の GAP 側ブロック系検算(34/34) | `3eb0a70a48be9b897db08cb5a08ad907a3b03ae4` | 本便で無変更 |
| `crosscheck/check-k5-blocks.mjs` | 同上の node 独立照合器(36/36・突合 13/13) | `3eb0a70a48be9b897db08cb5a08ad907a3b03ae4` | 本便で無変更 |
| `search/week4-k3-v2-repairs.mjs` | K3 側 $\rho_0$/$\mathfrak F_0$ の独立検算(43/43・PART 2c の突合先) | `174dd5a967b6db1d496fc1fe79f7406143769183` | 本便で無変更(本便で再実行し 43/43 PASS を再確認) |
| P6 $u$ 二経路・exact Kummer 判定パイプライン(library+driver+checker 10 ファイル・便 34 blocker 2-5 修理) | 経路 A/B・第三 checker・Kummer 判定器・第三 covariance の library/driver/checker 一式 | (working tree・便 34 時点。個別ファイル・blob hash は下記参照) | 詳細版表は `docs/week4-K5_Rule1_impl_versions.md`(v2・便 34)を正本とする。library=`search/u-extract-pathA.g`・`crosscheck/u-extract-pathB-lib.mjs`・`search/kummer-decide.g`(凍結対象)。driver=`search/u-extract-pathA-k3-driver.g`・`crosscheck/u-extract-pathB-k3-driver.mjs`・`search/kummer-decide-k3-driver.g`(K3 較正専用)。checker=`crosscheck/u-compare.mjs`・`crosscheck/check-kummer.mjs`・`crosscheck/check-kummer-cov3.mjs`・`crosscheck/cyclo-ring-lib.mjs`。**本便でも git commit を行っていない**ため commit ID は同ドキュメント §0 の手順(`git log -1 --format=%H -- <path>`)で司令塔が commit 後に確定させること。blob hash(`git hash-object`)は commit の有無によらず不変。
