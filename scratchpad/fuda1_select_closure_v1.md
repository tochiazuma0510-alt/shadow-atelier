# 札 1(D972 idx3 SELECT)完結索引 v1 — 測定済みと precise open の分離

`DIR: proper 側計器 / FRAME: D972 idx3 census × 二面体 Kummer 側`

**委嘱**: 司令塔・裁定 1755(研究者事前合意による札 1 SELECT 追跡の完結)。
**著者**: 数学者(Opus 5)/ 2026-08-29。**規約 (R-1)(R-2) 準拠。**
**位置づけ**: 本書は**完結索引**である。後続(将来の再開・文献要請)は §2 の第一歩から一意に再開できる。
**格の語法**: 「検証(verified)」は Lean に予約(2026-07-18 研究者指示)。本書で使うのは `cross-checked`(二系統一致)・`paper-proof`・`candidate` のみ。

---

## §0 一行結論

> **$c'=+1$ は測定済み(cross-checked)。しかし $c'$ を census の roster ラベルへ翻訳するビットは、census の内部からは原理的に取得できない(PG-1 = 構成上の不在)。SELECT は「翻訳ビット = census 外部入力を要する precise open」として完結する。**

---

## §1 測定済み(格つき)

### 1.1 $c'=+1$ — 算術側の測定

| 項目 | 値 | 格 |
|---|---|---|
| $c'$($=\Psi/\mathcal K_3$ の符号) | $+1$ | **cross-checked** |
| **実使用素数** | **3 素数 $p=19,37,73$**(S1–S9/S10 経路) | 裁定 1750 の事実訂正に従う |
| アンカー | $u_{\rm dih}=2^{-7}$、`anchor_source:"u_dih"`(規約台帳 D-2) | 確定 |
| $\mu_3$ フレーム | $\omega=g^{(p-1)/3}$ | — |

⚠ **同名別ゲートの区別(私の過去の混線を明記)**: `scratchpad/math_s4norm_v1.py`(sha16 `5ee59665c67235c3`)が 8 素数 $\{19,37,73,163,181,199,271,373\}$ で走らせたのは
「$c'(u_{S4}=u_0)==c'(u_{S4}=\text{normalised})$ が 8/8」という**3 点正規化不変性ゲート**であって、$\psi_p$ の実測そのものではない。**「8 素数で $c'$ を測った」と書いた過去の私の記述は誤り**(裁定 1750 受諾済)。

**フレーム非依存性(補題・私)**: $\mu_3$ フレームを $\omega\mapsto\omega^2$ に取り替えると $\Psi$ と $\mathcal K_3$ が**同時に**同じ単元倍を受ける ⟹ **比 $c'$ は不変**。規約 D の残存自由度は $c'$ に効かない。

### 1.2 ★ 補題 SIGN-VAC — $u_{\rm dih}$ の符号は mod 3 Kummer に効かない

> **補題.** $p$ を奇素数、$p\equiv1\pmod 3$ とする。このとき $\dfrac{p-1}{3}$ は**常に偶数**であり、したがって
> $$(-1)^{(p-1)/3}=1 .$$
> **系.** $u_{\rm dih}=\pm2^{-7}$ の符号は、任意のそのような $p$ における mod 3 Kummer 記号
> $\log_\omega\!\bigl(u_{\rm dih}^{(p-1)/3}\bmod p\bigr)$ に**一切影響しない**。

**証明.** $p$ が奇ゆえ $p-1$ は偶数。$p-1=3\cdot\frac{p-1}{3}$ で $3$ は奇数だから、積が偶であるためには $\frac{p-1}{3}$ が偶でなければならない。∎

**格 = paper-proof**(初等・自己完結)。**効用**: §7 系列で私が積み残していた $\pm$ 曖昧性を**全素数で**消す。以後 $u_{\rm dih}$ の符号を UNKNOWN として持ち回る必要はない。
⚠ **射程**: mod 3 のみ。**mod 9 アンカー(γ 案)では $\zeta_9$ が入るため本補題は適用できない** — γ を使うなら符号は再び論点になる。

### 1.3 ★ (E) $\Psi$ の類関数閉鎖 — 一級の負結果

`gate: scratchpad/psi_classfn_probe_v1.g` (bytes 1792, sha16 `c24855009aa434db`)
```
G_ORDER 504   N_ORDER 1512
PSL_CONJ_PAIRS 37    PSI_VIOLATIONS 27   PSI_IS_PSL_CLASS_FUNCTION     false
PGammaL_CONJ_PAIRS 101  PSI_VIOLATIONS 73  PSI_IS_PGammaL_CLASS_FUNCTION false
CYCLETYPE_TO_PSI
  [[1,1],[2,4]] -> {0}     [[1,2],[7,1]] -> {0,1,2}   [[1,9]] -> {0}
  [[3,3]]       -> {1,2}   [[9,1]]       -> {0,1,2}
ORDER3_IN_T 4  all_PSL_conjugate true  their_Psi [ 2, 1, 2, 1 ]
```

> **決定打**: $T$(27 個の π 値)の中の**位数 3 の元 4 個は $PSL(2,8)$ で互いに共役**であるのに $\Psi$ は $[2,1,2,1]$ と割れる。$P\Gamma L$ 共役でも同様。

**帰結**: $\mathrm{Frob}_p$ は素点の選択について**共役類までしか定まらない**。Dedekind(9 次多項式の mod $p$ 分解型)が返すのは cycle type = 共役類の粗い情報のみ。cycle type → $\Psi$ は 5 型中 3 型が $\{0,1,2\}$ 全体に散る。
**⟹ どんな被覆・多項式・conjugator を用意しても、π 経由で $\Psi(\mathrm{Frob}_p)$ を決めることはできない。**
**格 = cross-checked**(裁定 1750 [S4] で昇格)。

### 1.4 ★★ PG-1 — π 列は帳簿ラベル。担い手は**構成上不在**

`gate: scratchpad/pg1_pi_semantics_v1.g` (bytes 2182, sha16 `f9867c657da9d149`)
```
PG1_BLOCK_GROUP_ORDER 504   PG1_BLOCK_DEGREE 9
PG1_ALL_PI_IN_BLOCK_GROUP true
PG1_PI_COUNT 27  generate_order 504  equals_block_group TRUE   <- 共役でなく等号
PG1_G9_ORDER 2916 x PSL_ORDER 504 = 1469664   |PB3/M| = 1469664
PG1_ROOF_IS_DIRECT_PRODUCT_27x9 true
PG1_BLOCK_INDEX_IN_PGammaL 3
PG1_BLOCK_NORMALISER_IN_Sym9 1512 (= PGammaL, 窓の外)
PG1_VERDICT carrier_absent_by_construction true
```

**逐語根拠 1** — `search/d972_b4_word_key_artifact_v1.g`(bytes 4462, sha16 `1eac38915e1a2915`)L68-70:
```gap
B4WKfirst :=D972BlockRestrict(B4WKf,0,27);;
B4WKsecond:=D972BlockRestrict(B4WKf,27,9);;
B4WKkey   :=[B4WKSh.m, D972Can9(B4WKfirst), D972Can4(B4WKsecond)];;
```
**逐語根拠 2** — `search/d972_dovetail_core_v2.g`(bytes 10592, sha16 `1c3348003805df87`)L171-173:
```gap
D972Can4 := function(perm9)
  return List([1..9],j->j^perm9);
end;;
```
**逐語根拠 3** — `search/drophunt_checker_producer_v2.g`(bytes 16393, sha16 `0e2d2ec14cfe4ff3`)L76-89: roof 窓は degree-27 ブロック($G_9$, 位数 2916)と degree-9 ブロック($\langle X_4,Y_4\rangle=PSL(2,8)$, 位数 504)の直和として構成され、producer 自身が L84 で `if Size(DCP2P4) <> 504 then Error(...)` と位数を検査している。

> ### 判定(PG-1)= **(B) 原理的に不在**
> 「π 列」は、シャドウ元 $f$(GT-対 $(m,f)$ の $f$)を roof 窓 36 点のうち **28..36 番ブロックへ制限**し、像リストとして直列化したものである。**producer は monodromy とも Galois とも書いていない** — 「π」は工房が後から付けた呼称。
> 窓 $M$ は degree-9 ブロック群を **$PSL(2,8)$ そのものとして構成**しており、$P\Gamma L(2,8)$ は窓の構成のどこにも現れない($N_{\mathrm{Sym}(9)}(PSL)=1512$ は**窓の外**)。ゆえに「27 値のコセットが全て 0」は**観測ではなく恒等式**であり、機械側も `Group(PIV) = P4` を**共役でなく等号**で返した。
> **⟹ required field「PSL 側 Frobenius コセット」は census 側に担い手を持たない。(i) joint marked Frobenius row と (ii) P5′ 比較写像は同時に死ぬ。**

**★ 「衝突」の正体**: 私が 3 便前に提示した「census コセット 0 vs $\psi_p=2$ の衝突」は矛盾ではなかった。**$\psi_p$ は $f$ の degree-9 ブロックの $P\Gamma L/PSL$ コセットではない**。両者は別の対象であり、**§7.1/§7.2 の橋(π ↦ $P\Gamma L/PSL$)は最初から圏の取り違え**だった。**census に欠陥はなく、橋が誤りだった。**

⚠ **(B) の射程**: 本判定は**この窓 $M$ のこの census** についてのもの。「翻訳ビットは*何らかの*有限窓のシャドウの関数か」は別問題(実質 Ihara 単射性の一部)で **open のまま**。(B) が確定させるのは「**札 1 のこの追跡は census 内では完結不能**」である。

### 1.5 ORIENT 型付けの**存在** — candidate(向き情報は持たない)

roster から当てはめた $\Psi'$ について:
- $\Psi'$ は **π の関数**(27 fibre・pure)、fibre サイズ 9/9/9、全 486 行で $R_1=\ker(\Psi'-\mathcal K_3)$, $R_2=\ker(\Psi'+\mathcal K_3)$。
- 生存する主張 = 「**順序なし対の π-fibre 化**」= ORIENT 型付けの**存在**。**格 = candidate。**

> ⚠ **向きの情報はゼロ(裁定 1750 [S2] 受諾)**: $\Psi'$ が π の関数なら $-\Psi'$ もそう。ヒストグラムも自由 108 行の $\Psi\ne0$ も**すべて符号反転不変**。⟹ **争点(どちらの符号か)についての情報量は 0**。
> 私が提示した確率 $3^{-351}$ は独立性を誤仮定した**過大評価であり撤回**する(実パラメータ 27・自由制約 18)。

参照: `scratchpad/pi_psi_table.g`(bytes 1283, sha16 `aa92667512ab5c6e`)/ `scratchpad/psi_full_v1.json`(bytes 4769, sha16 `b7485d9d8159cdc7`)。

### 1.6 δ = $D_9$ 座標三つ組(MapB 不変につき**選別力なし**)

`D972Can9` は 27 点ブロックを 3 つの 9 点部分ブロックに分け、各々を $D_9$ 正規形 $r^a s^e$ の座標 $[a,e]$ で返す(`d972_dovetail_core_v2.g` L164-169)。観測された「δ の第 2 列が全 0」は **3 成分すべてが回転部分群 $\langle r\rangle\cong C_9$ に居る**ことを意味する。

機械実測(artifact sha16 `564a921be8114bde`):
```
d10 == -d00 mod 9      : 972/972
d20 == kappa(m) mod 9  : 972/972      kappa(m)= m+1 (m odd) / -m (m even)
distinct (m,d00) pairs : 108  (= 12 * 9)
```
⟹ δ は 2405 Thm 4.3 の $(r^{2k},r^{-2k},r^{\kappa(m)})$ に一致。

> ⚠ **選別力ゼロ(裁定 1750 [S1] 受諾)**: **MapB**: $(d_{00},d_{10},d_{20})\mapsto(-d_{00},-d_{10},d_{20})$ は roster を入替えつつ上記 2 恒等式を保つ(私自身の再検算: `under MapB: d10==-d00 mod 9 : 972/972`, `d20==kappa(m) : 972/972`, `MapB flips K3 on 972/972 rows`)。
> **私の誤り**: **$r$-再スケール($k,\kappa$ を同時に動かす)と roster 入替($k\to-k$ のみで $\kappa$ を固定)は別の自由度**である点を見落とし、前者の pin から後者を導いた。これは ORIENT (e)(私自身の定理)が禁じる「**census 無料 1 ビット**」の取得だった。

### 1.7 odd-$\kappa$ ill-typed の実証(D-13 canary の訂正)

機械実測:
```
d20 residue histogram: {0:162, 1:162, 3:162, 4:162, 6:162, 7:162}
odd residues: [1, 3, 7]   rows with odd d20: 486/972
kappa integer representative even for all 12 values of m: True
```

> **D-13 の正しい形**: 「$\kappa(m)$ は常に偶数」は**正準整数代表**($m+1$ または $-m$)についての**真の命題**である(12/12)。しかし **mod 9 の剰余代表には保存されない**(9 が奇数ゆえ $-2\equiv7$)。実測 **486/972 行で剰余が奇**。
> **⟹ D-13 を「mod 9 residue の偶数性」として canary に使うと 486 行で偽陽性の警報が出る。**登録形を「正準整数代表に限る」と再述すること。**canary 穴 = 奇残差 $\{1,3,7\}$**(裁定 1750 [S5] が指摘。私も独立に同じ集合を得た)。
> これは私の登録ミス(裁定 1732(b) で承認された形が ill-typed だった)。

---

## §2 precise open — 翻訳ビットは **census 外部入力**を要する

### 2.1 5 必須フィールドの「向き構造」

joint marked Frobenius row が要求する 5 フィールドを、**向き情報($c'$ の符号)を持つか**で分類する:

| # | フィールド | 工房内で閉じるか | **向き情報** | 工数目安 |
|---|---|---|---|---|
| 1 | 素点 $\mathfrak p\mid p$ / $\zeta_9$ 規約 | **可**($\mathbb Z[\zeta_9]$・次数 6) | **なし** | 0.5 便 |
| 2 | $k$ 正規化 | **可**(γ 案が効く箇所) | **なし** | 1 便 |
| 3 | PSL 側 Frobenius コセット | — | **なし** | **PG-1 = 担い手不在** |
| 4 | $a_M(\mathrm{Frob}_p)$ の実現 row | **不可** | **あり** | 外部入力 |
| 5 | 共通制限値(4 成分が同一 $\sigma$ のものである証明) | **不可** | **あり** | 外部入力 |

> **★ 構造的所見**: 工房内で閉じる 3 つは**すべて向き情報を持たない**。向きを持つ 2 つが**ちょうど外部入力を要求する**。この配置自体が、裁定 1750 の指摘が偶然ではなく構造的であることの傍証である。

### 2.2 外部入力の候補(2 本)

1. **$\mathrm{Ih}_M$ の明示モデル** — $\sigma\mapsto(m(\sigma),f(\sigma))$ を窓 $M$ で実際に計算する手続き。文献にあるか否かは**私は知らない**(文献ゲート経由の要請事項)。
2. **明示 Belyi 構成** — degree 9・$PSL(2,8)$ passport の Belyi 写像 + その算術降下データ。工房に機械(Gröbner)がなく、外部文献取得が要る。
   ⚠ **前提リスク**: PG-1 により census の π は幾何的対象ではない。候補 2 を採る場合、**接続先を census 以外に用意する必要がある**(census の π へは繋がらない)。

### 2.3 恒久規則(裁定 1750・転記)

> **翻訳ビットの census 内導出の提案は以後禁止。提案には外部入力の特定を必須とする。**

### 2.4 再開時の第一歩

**外部入力の特定**から始めること。具体的には「どの文献 / どの計算が $a_M(\mathrm{Frob}_p)$ の実現 row を供給しうるか」を決める問題であり、**測定の設計ではない**。§2.2 の候補 1 について文献要請を起こすのが最短。

**【文献要請】**(規律 6 準拠)
- **困難の記述**: 有限窓 $M$(ここでは $PB_3/M\cong G_9\times PSL(2,8)$, 位数 1,469,664)に対し、$G_{\mathbb Q}\to GT(M)$ の像を**具体的な $\sigma$(例: $\mathrm{Frob}_p$)で明示的に計算**する手続きが要る。
- **欲しい結果の型**: 「$\widehat{GT}$ / GT-shadow の Galois 像を、有限商で明示的に評価する計算可能な記述」。dessins の Galois 作用の明示計算、あるいは $\pi_1$ の pro-$\ell$ 商上の Galois 作用の Frobenius における明示公式。

---

## §3 死んだ経路の registry(再訪防止)

| # | 経路 | 死因 | 格 |
|---|---|---|---|
| **1** | **π 経路**($\mathrm{Frob}_p\mapsto\pi$ を分解型で決める) | $\Psi$ が $PSL(2,8)$ の**類関数でない**(位数 3 の 4 元が共役なのに $\Psi=[2,1,2,1]$)⟹ 共役類までしか定まらない Frobenius では決まらない | cross-checked(§1.3) |
| **2** | **K1–K5**($c$ を通らない再定式化) | $\Psi$ 側の $\mathbb F_3$ 同一視を固定する**比較写像(P5′)の欠如**。§7.0 で私自身が撤回 | 撤回済 |
| **3** | **(C) $r$-pin**(δ = Thm 4.3 三つ組から $r$ を pin) | **MapB 不変**(972/972)。pin される自由度($r$)と争点の自由度(roster 入替)が別物 | 否(裁定 1750 [S1]) |
| **4** | **(B) $\Psi'$ 当てはめ** | roster からの fit で**循環**。3 証拠すべて**符号反転不変** ⟹ 争点情報ゼロ | 否(裁定 1750 [S2]) |
| **5** | **(D) 記号すり替え** | ORIENT の正準 $\Psi$ ≠ 当てはめ $\Psi'$。正準 $\Psi$ での V4 は **FAIL(1512/1512)のまま** | 否(裁定 1750 [S3]・1726 と同型) |

> ### 共通死因(一行)
> **いずれも「census の内部構造から算術の向きを読もうとした」— 外部入力なしに翻訳ビットを得ようとしたことが唯一かつ共通の死因である。**

⚠ 経路 1・2 は**私自身が正しく殺した**(一級の負結果)。経路 3・4・5 は**私が提案し falsifier が殺した**。この非対称は記録に値する。

---

## §4 未読・未解決の申告

| # | 項目 | 状態 |
|---|---|---|
| **U-1** | `sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md`(sha16 `6512e810011105f8`) | **在庫あり・未読**。pointed gate の正否・retained ancestry($\{w_i\}$ と $(\alpha,\beta)$)がここにある。$M=\sum a_i(U_i-V_i)$ の構成に必須 |
| **U-2** | `sol/audit_r07_roof_abelian_screens_are_canaries_v207.md` | **未読**。題名は「abelian screen は canary」の裁定を示唆 — 私の 40 検査の格付けに直結 |
| **U-3** | v216 / v217 の single/three-seed pre-gate 仕様 | **未読**。v220 §0 が唯一の合法な安価スクリーンとして挙げる |
| **U-4** | **[WDICT-5]** 語↔元の規約不一致(v1/v2 共通) | **修理待ち**。実測 `fwd ok=79 / rev ok=158`(計 237)— どちらの規約でも全行は再現しない。falsifier 再前哨の verdict と待ち合わせて implementer B に一括発注(裁定 1750) |
| **U-5** | **F6-SALVAGE**(charming $\Rightarrow \mathrm{ord}(\bar c)\mid e(w)$ は定理か) | **判定保留**。構造論証は「一般には定理でない」($L\subseteq\{a+b\equiv0\}$ は従わない)。実測は 12 窓・charming 104 行で **104/104 成立**(この数は語反転不変ゆえ [WDICT-5] の影響を受けない)。ただし twist 公式が 531/1062 でしか成立せず**計器が壊れている** ⟹ U-4 修理後に再判定 |
| **U-6** | 「翻訳ビットは*何らかの*有限窓のシャドウの関数か」 | **open**(§1.4 の射程注記)。実質 Ihara 単射性の一部 |

---

## §5 Sol 接続(配達判断は研究者)

**要旨(1 段落・Sol へ伝える場合の文面案)**:

> 影工房は D972 idx3 census の SELECT 追跡を完結した。算術側の $c'=+1$ は 3 素数($p=19,37,73$)・2 系統・アンカー $u_{\rm dih}=2^{-7}$・3 点正規化不変性で cross-checked に測定済みである。しかし census の鍵第 3 成分(工房が「π 列」と呼んでいたもの)は、逐語確認の結果、**シャドウ元 $f$ の roof 窓 degree-9 ブロックへの制限を直列化した帳簿ラベル**であり、窓の degree-9 ブロック群は構成上 $PSL(2,8)$ そのものである($\langle\text{27 値}\rangle=\langle X_4,Y_4\rangle$ が**等号**で成立)。したがって $P\Gamma L/PSL$ コセットを担う対象は census 側に**構成上存在しない**。加えて、roster から当てはめた $\mathbb F_3$ 指標は符号反転不変であり向きの情報を持たず、δ の Thm 4.3 一致は MapB 不変で選別力を持たない。**⟹ $c'$ を census の roster ラベルへ翻訳するビットは census 外部入力(= $\mathrm{Ih}_M$ の明示モデル、または明示 Belyi 構成+算術降下)を要する precise open として残る。** その帰結として、**$\Delta_{36}$ の 216 行はこの precise open に条件付きのまま**である。**432 行の無条件非算術は不変**(本件の影響を受けない)。

---

## §6 参照 sha 一覧(機械出力)

```
pg1_pi_semantics_v1.g                                    2182  f9867c657da9d149
psi_classfn_probe_v1.g                                   1792  c24855009aa434db
pi_group_probe_v1.g                                       622  ed6bf9e0936a984b
pi_psi_table.g                                           1283  aa92667512ab5c6e
psi_full_v1.json                                         4769  b7485d9d8159cdc7
math_s4norm_v1.py                                        2589  5ee59665c67235c3
math_kerpi_probe_v1.g                                    2175  4588803eae759955
joint_marked_frobenius_design_v1.md                     25178  5a2ef97868f4e315
local3_udih_anchor_and_s9_conventions_v2.md             15564  10518b1abb261cfe
d972_b4_word_key_artifact_v1.g                           4462  1eac38915e1a2915
d972_dovetail_core_v2.g                                 10592  1c3348003805df87
drophunt_checker_producer_v2.g                          16393  0e2d2ec14cfe4ff3
d972_b4_word_key_artifact_v1_20260816.json             176474  564a921be8114bde
d972_idx3_arithmetic_receipt_v2_20260823.json          249817  1fca084f396605a8
d972_local3_v14_orient_v1_20260828.json                  5512  773324eb387f1d4d
```

---

## §7 用語の衝突(台帳登録要請)

**$\pi$ は本プロジェクト内で 2 つある。混同は事故を生んだので登録を要請する。**

| 記号 | 正体 | 出所 |
|---|---|---|
| $\pi:\mathcal G\twoheadrightarrow\Delta_0$ | 共通ソース群 → **roof 群**の射影($\ker\pi$ はこちら) | v191 (1.1) |
| 「π 列」 | D972 key 第 3 成分 = $f$ の degree-9 ブロック座標 | `d972_b4_word_key_artifact_v1.g` L70 |

**本書での用法**: §2 以降の $\ker\pi$ は**前者**。「π 列」は常に鍵括弧つきで**後者**。

---

**完**(札 1 SELECT 追跡・完結索引 v1)
