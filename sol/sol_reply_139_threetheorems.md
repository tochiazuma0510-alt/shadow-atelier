# 返書 139 — cofinal への三本

- 対象: `ops/inbox_codex/sol_task_139_threetheorems.txt`
- 実行日: 2026-08-15
- 観測 HEAD: `18d545649766f1592bf3c67622b6efc812d395e6`
- 証拠格: 本書の新規部分は紙上証明。Lean certificate はない
- 実行順: (a) → (b) → (c) → 小回収

## 0. 結論

| 項目 | 出口 | 結論 |
|---|---|---|
| (a) 一様吸収 | **部分定理 + UNKNOWN** | base-change の正確な移送補題 `ABSORB-BC-139` は立つ。しかし任意の非分裂・非可換・modular 非自由・多段 roof に対する一様な chain homotopy は、各 refinement で新しく生じる cokernel-kernel (D_{L/K,t}) の消滅と自然な lift を供給できず停止。包含不成立の具体例は得ていない。GEN-AFF も独立前件のまま |
| (b) split MCOV | **定理** | `MCOV-CRT-139` と `MCOV-ISO-139` を得た。isolated な (N') を用いる `SPLIT-NULL` の全設定で (MCOV) は自動。従って split 枝には MCOV 欠落は起こらない |
| (c) normal form | **no-shortcut 定理 + UNKNOWN** | `MONO-CNF-139` により、全射族が cofinal なら任意の isolated 細分の reduction は既に全射である。従ってこれは INT だけから作れる前処理ではなく、目標の全称結論そのものの強さを持つ。現行の covered family への所属を強制する比較定理は無い |

したがって、三本のうち split 枝は族定理として閉じた。(a) は移送障害を一点に同定したが全消滅を得ず、(c) は独立な近道にならないことを確定した。

## 1. (a) 一様吸収 — base-change の正確な停止点

### 1.1 basis-free な障害写像

一つの marked roof (K) と roof 行 (t) に対し、補正空間、cocycle 空間、relation-defect 空間をそれぞれ

\[
U_K,qquad \mathcal Z_K:=Z^1(\Gamma,V_K),\qquad \mathcal R_{K,t}
\]

と書き、線型化を

\[
A_{K,t}:U_K\longrightarrow\mathcal R_{K,t},
\qquad
C_{K,t}:\mathcal Z_K\longrightarrow\mathcal R_{K,t}
\]

とする。基底に依らない本体は

\[
\omega_{K,t}:=\pi_{K,t}C_{K,t}:
\mathcal Z_K\longrightarrow\operatorname{coker}A_{K,t}
\]

である。`COCYCLE-ABSORB-137` の有限結論は、凍結した 1,620 行で \(\omega_{K,t}=0\) だったことに等しい。

### 1.2 定理 `ABSORB-BC-139`

> **定理（base-change 移送）.** (L\subseteq K) が線型化に
> \[
> q_U:U_L\to U_K,\qquad q_Z:\mathcal Z_L\to\mathcal Z_K,
> \qquad q_R:\mathcal R_{L,t}\to\mathcal R_{K,t}
> \]
> を誘導し、
> \[
> q_RA_{L,t}=A_{K,t}q_U,qquad q_RC_{L,t}=C_{K,t}q_Z
> \tag{1.1}
> \]
> とする。すると (q_R) は
> \[
> \bar q_R:\operatorname{coker}A_{L,t}\longrightarrow
> \operatorname{coker}A_{K,t}
> \]
> を誘導し、
> \[
> \bar q_R\omega_{L,t}=\omega_{K,t}q_Z.\tag{1.2}
> \]
> 特に \(\omega_{K,t}=0\) なら
> \[
> \operatorname{Im}\omega_{L,t}\subseteq
> D_{L/K,t}:=\ker\bar q_R.\tag{1.3}
> \]
> よって (D_{L/K,t}=0) なら \(\omega_{L,t}=0\) である。

**証明.** (1.1) の第一式から (q_R(\operatorname{Im}A_{L,t})\subseteq\operatorname{Im}A_{K,t}) なので \(\bar q_R\) が定義される。第二式を cokernel へ送れば (1.2)。残りは直ちに従う。∎

これは有限 rank の言い換えではなく、refinement が新たに作る障害の居場所を

\[
\boxed{D_{L/K,t}=\ker\bigl(\operatorname{coker}A_{L,t}
\to\operatorname{coker}A_{K,t}\bigr)}
\]

へ限定する族定理である。広い一様吸収定理に必要なのは、全 isolated base change と全 roof 行でこの群が零、又は少なくとも \(\omega_{L,t}\) がこの群へ零写像になることの証明である。

### 1.3 何が閉じ、何が閉じないか

| 操作 | 結論 | 必要条件 |
|---|---|---|
| block-diagonal 有限直和 | 各成分の \(\omega_t=0\) から総 \(\omega_t=0\) | (A_t,C_t,\mathcal Z) が同じ直和を保つ |
| 係数体の flat extension | 既存の包含と (T_t) は tensor 後も保たれる | word linearization が scalar extension と可換 |
| 一段 refinement | `ABSORB-BC-139` で移送できる | (1.1) と (D_{L/K,t}=0) |
| 多段 (L_r\subset\cdots\subset L_0) | 各段で移送できれば帰納的に閉じる | 全 (i,t) で (D_{L_i/L_{i-1},t}=0) |
| 交叉 (L=K\cap H) | isolated 性は INT で得るが、吸収は自動でない | INT は cokernel map の単射性を含意しない |
| GEN-AFF | relation 吸収からは出ない | 補正後の生成性を一様に与える別定理が必要 |

特に quotient/intersection の base change は係数体の flat extensionではない。新しい cocycle が粗い段から降りず、新しい relation-defect class が (D_{L/K,t}) に残り得る。非半単純・modular 非自由・非可換下位項が問題になる場所は、まさにこの新規部分である。

### 1.4 「包含」と「自然な chain homotopy」は別

各有限次元ベクトル空間で

\[
C_t(\mathcal Z)\subseteq\operatorname{Im}A_t
\]

なら、基底を選んで (A_tT_t=-C_t) を解ける。しかし RREF で選んだ (T_t) は module morphism、marking 変更、roof reduction と可換するとは限らない。自然な (T_t) は、functor category で (C_t) を (A_t) の手前へ lift する追加データである。modular な非半単純圏では短完全列の自然な splitting は一般には供給されないため、objectwise な rank 一致だけではこの lift を作れない。

従って本項の停止点は曖昧な「一般化不足」ではなく、次の三件である。

1. 全 refinement で (D_{L/K,t}) を消す構造式が無い。
2. objectwise solver (T_t) を自然変換へ上げる lift が無い。
3. それらが立っても GEN-AFF は独立に残る。

広い一様吸収の真偽は **UNKNOWN**。包含不成立の具体的な module/marking/roof を構成していないので、§1 の許可に基づく新規測定へは進んでいない。

## 2. (b) split 枝 — MCOV の族判定

### 2.1 CRT による必要十分条件

(a:=2n)、(b:=N'_{\rm ord})、(d:=\gcd(a,b)) とする。交叉 roof では

\[
M_{\rm ord}=\operatorname{lcm}(a,b).
\]

また ρ_d を各剰余環から \(\mathbb Z/d\) への写像とする。

> **定理 `MCOV-CRT-139`.** `SPLIT-NULL` の記号で
> \[
> \mathrm{(MCOV)}
> \quad\Longleftrightarrow\quad
> \rho_d(\mathcal X_n)\subseteq\rho_d\bigl(\mathfrak m(N')\bigr).
> \tag{2.1}
> \]

**証明.** 固定した (m\in\mathcal X_n) と (s\in\mathfrak m(N')) に対し

\[
\widetilde m\equiv m\pmod a,qquad
\widetilde m\equiv s\pmod b
\]

が解を持つ必要十分条件は一般 CRT により (m\equiv s\pmod d) であり、解は法 \(\operatorname{lcm}(a,b)=M_{\rm ord}\) で一意である。全 (m) を量化すれば (2.1)。∎

従って split roof の通過・非通過は二つの有限集合の (d)-剰余だけで完全に決まる。

### 2.2 isolated 窓の (m)-像は full charming set


\[
\mathcal X_b:=\{s\bmod b:\gcd(2s+1,b)=1\}
\]

と置く。写像

\[
\lambda_b:\mathcal X_b\longrightarrow(\mathbb Z/2b)^\times,
\qquad s\longmapsto2s+1
\tag{2.2}
\]

は全単射である。逆写像は、奇数単元 (u) に (s=(u-1)/2\bmod b) を対応させる。

isolated な (N') では `SURJ-Split`（`sol/sol_reply_86_math13.md` F86-4.1.1、裁定 227）の W1 を満たし、

\[
\widetilde\chi\circ\mathrm{Ih}_{N'}=\chi_{2b},
\qquad
\chi_{2b}(G_{\mathbf Q})=(\mathbb Z/2b)^\times.
\]

従って \(\widetilde\chi(\mathrm{GT}(N'))\) は全単元群であり、(2.2) の全単射性から

\[
\boxed{\mathfrak m(N')=\mathcal X_b.}\tag{2.3}
\]

### 2.3 `MCOV-ISO-139`

> **定理 `MCOV-ISO-139`.** (n\ge3) を奇数、(N'\in I=\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)) とする。すると
> \[
> \rho_d(\mathcal X_n)\subseteq\rho_d(\mathcal X_b),
> \]
> よって (MCOV) が成り立つ。

**証明.** (m\in\mathcal X_n) を固定する。各素数冪 (q^e\Vert b) ごとに (s\bmod q^e) を選ぶ。

- (q\mid d) なら (s\equiv m\pmod{q^{v_q(d)}}) とする。(q) が奇なら (q\mid n) なので (2m+1\not\equiv0\pmod q)。(q=2) なら (2s+1) は常に奇数である。従ってこの合同を保つ任意の lift は (q) に関して charming である。
- (q\nmid d) なら (s\equiv0\pmod{q^e}) と選べば (2s+1\equiv1\pmod q)。

素数冪間で CRT を取ると (s\in\mathcal X_b) かつ (s\equiv m\pmod d) を得る。(2.1) と (2.3) から (MCOV)。∎

### 2.4 split 枝への帰結

`SPLIT-NULL` の全仮定、すなわち (n) 奇数、(N') isolated、(M=K^{(n)}\cap N')、pure 商に共通の非自明商が無い、を満たす全 roof で (MCOV) は自動である。従って差替版 `SPLIT-NULL″` と合わせて

\[
R_{M,K^{(n)}}:\mathrm{GT}(M)\twoheadrightarrow\mathrm{GT}(K^{(n)})
\]

が族として従う。

裁定 388 が退けた「split の有限群構造だけから (MCOV) が出る」という証明機構は、ここでも採用しない。今回回収したのは、isolated typing と円分商全射を明示的に輸入する別証明による結論である。証明機構の不成立と結論の成否をここで分離した。

したがって族判定は次のように閉じる。

| 族 | (MCOV) |
|---|---|
| `SPLIT-NULL` の isolated split 族 | **常に成立** (`MCOV-ISO-139`) |
| isolated/Ihara typing を外した抽象 split datum | (2.1) が必要十分。\(\rho_d(\mathcal X_n)\nsubseteq\rho_d(\mathfrak m(N'))\) のとき不成立 |
| entangled / 共通商非自明 | `SPLIT-NULL` 自体の射程外。MCOV だけでは像を決めない |

よって canonical isolated poset 内で、split roof の MCOV 欠落を有限排除側の標的にする路は閉じる。split 族全体が isolated poset に cofinal である、という結論はここからは出ない。

### 2.5 既走 119 組の較正

既存 cert `search/certs/ihnec_gap4_mcov_scan_20260801.json`（SHA-256 `fff0cee85e0e8a23c979fa74aba977660a816f44b75c3fadbf806879d9a09872`）は 7 個の (K^{(n)}) 窓と 17 個の非 dihedral 窓、計 119 組を収める。既存 producer は単一 Python 実装だった。

本便ではその `pairs` だけを入力に、PowerShell の別実装で

1. 法 (M_{\rm ord}) の brute-force、
2. (2.1) の (d)-剰余判定、
3. 記録された \(\mathfrak m(N')\) と \(\mathcal X_b\) の一致、
4. 保存 status との一致

を再計算した。生出力は

```json
{"pairs":119,"brute_failure_pairs":0,"crt_equivalence_mismatches":0,"m_image_not_full_Xb":0,"stored_status_mismatches":0}
```

である。これは 119 組の整数比較層の cross-check であり、17 個の source cert からの窓データ抽出を第三実装で再実施したものではない。また族定理 `MCOV-ISO-139` はこの 119 組に依存しない。

再現の核は各 pair について次を評価するだけである。

```powershell
$d = gcd $pair.two_n $pair.N_prime_ord
$brute = $pair.X_n | ForEach-Object {
  $m = [int]$_
  0..($pair.M_ord-1) | Where-Object {
    ($_ % $pair.two_n) -eq ($m % $pair.two_n) -and
    $pair.m_image_N_prime -contains ($_ % $pair.N_prime_ord)
  } | Select-Object -First 1
}
$crt = $pair.X_n | ForEach-Object {
  $m = [int]$_
  $pair.m_image_N_prime | Where-Object { (($_-$m) % $d) -eq 0 } | Select-Object -First 1
}
```

## 3. (c) `COFINAL-NORMAL-FORM`

### 3.1 単調性が与える no-shortcut

> **定理 `MONO-CNF-139`.** (L\subseteq K\subseteq M) なら
> \[
> R_{L,M}=R_{K,M}\circ R_{L,K},
> \qquad
> \operatorname{Im}R_{L,M}\subseteq\operatorname{Im}R_{K,M}.
> \tag{3.1}
> \]
> 従って、各 (L\in\mathcal U\subseteq\mathcal I_M) で (R_{L,M}) が全射であり、\(\mathcal U\) が cofinal、すなわち
> \[
> \forall K\in\mathcal I_M\ \exists L\in\mathcal U:\ L\subseteq K
> \]
> なら、全 (K\in\mathcal I_M) で (R_{K,M}) は全射である。

**証明.** reduction の合成則が (3.1) を与える。任意の (K) の下に全射な (L) があれば

\[
\mathrm{GT}(M)=\operatorname{Im}R_{L,M}
\subseteq\operatorname{Im}R_{K,M}\subseteq\mathrm{GT}(M),
\]

なので全て等号。∎

この向きはさらに強い。もしある (K) の像が真部分集合なら、その下の **どの** (L\subseteq K) も全射になれない。従って refinement によって悪い段を covered な全射正規形へ「逃がす」ことはできない。

### 3.2 INT からは出ない

固定した covered roof (H) を取り (L=K\cap H) とすれば、補題 INT は (L) の isolated 性を与える。しかし

\[
\operatorname{Im}R_{L,M}\subseteq
\operatorname{Im}R_{K,M}\cap\operatorname{Im}R_{H,M}
\]

であり、(H) の全射性は (L) の全射性を与えない。さらに交叉は

- split/common-quotient-trivial 性、
- `ABSORB-BC-139` の (D_{L/K,t}=0)、
- GEN-AFF、
- 一段・半単純という形

のいずれも保存すると証明されていない。

従って `COFINAL-NORMAL-FORM` は、(a)(b) より先に置ける純 order-theoretic な比較定理ではない。現行の named family の合併についてこれを示せば、その瞬間に全 isolated reduction の全射性まで示したことになる。

### 3.3 出口

本項で結論の否定は得ていない。真偽は **UNKNOWN** である。立たないのは「INT と既知 family を交叉すれば正規形が自動で得られる」という証明機構であり、正確な停止点は次である。

1. split 枝は §2 で閉じたが、entangled / Goursat mixed、非分裂、非可換核、modular 非自由、多段、S4 側同時深化を split 枝へ送る構造分類が無い。
2. covered family への所属が arbitrary intersection で保たれる定理が無い。
3. (3.1) により、全射 family の cofinality 自体が既に全称全射の強さを持つ。

従って (c) を建てるために残る仕事は「normal form の形式」を書くことではなく、各任意 (K) が既に全射となるだけの (a) 型一様定理、又は mixed roof を覆う別の族定理を与えることである。

## 4. 小回収 — (T_t) family cert

既存 checkpoint からの export 可否を read-only で監査したが、今回は `search/certs/` へ新規 cert を置いていない。

理由は明確である。

1. 便 137 の五つの factor-family SHA-256 を `search/certs/ search/ crosscheck/` で exact grep した結果は `NO_ARTIFACT_HITS`。値は `sol/sol_reply_137_whyvoid.md` にしか残っていない。
2. `search/certs/escape28_mainrun_v1_checkpoint.json` は completion/count/output digest だけで、(A_t,C_t,Z,T_t) を持たない。
3. `search/certs/escape28_mainrun_raw_v1_20260813.json` と `search/certs/escape2_mainrun_v1_20260815.json` は obstruction/outcome の集約を持つが (T_t) 行列を持たない。
4. `search/certs/campaign138_compact_preflight_v1_checkpoint.json` も rank template 件数だけである。

従って五つの (T_t) family を再現可能に収蔵するには、relation symbol から (A_t,C_t,Z) を再構成し、全 1,620 template で (A_tT_t=-C_tZ) を再度解いて payload を書き出す必要がある。これは「既存 checkpoint からの書き出し」ではなく再走に当たるため、委嘱 §5 の停止規則どおり実行しなかった。SHA だけから行列を復元したかのような cert は作っていない。

## 5. 射程・規律・provenance

### 5.1 cofinal 台帳の差分

| 旧未閉鎖 | 本便後 |
|---|---|
| MCOV 不明の isolated split roof | **閉鎖**。`MCOV-ISO-139` により自動 |
| split family 自体の cofinality | **UNKNOWN**。MCOV の閉鎖からは出ない |
| base-change 安定な一様吸収 | **UNKNOWN**。新規部分を (D_{L/K,t}) に局在化 |
| S4/mixed を含む normal form | **UNKNOWN**。`MONO-CNF-139` により独立な近道ではない |

### 5.2 novelty grep

実行後に

```text
rg -n -S 'MCOV-CRT-139|MCOV-ISO-139|ABSORB-BC-139|MONO-CNF-139' docs sol search crosscheck --glob '!sol_reply_139_threetheorems.md'
NO_PREEXISTING_HITS
```

を得た。これは工房内で定理名が未使用だったという receipt に限り、数学的優先権の主張ではない。

### 5.3 入力 digest

| 入力 | SHA-256 |
|---|---|
| `docs/notes/surj_d4_t1_v1.md` | `b05f83521aef962063cde147c940bbc3a2903bdf761ee116b1f4a875507006d5` |
| `docs/notes/ihnec_v1.md` | `498b24ef9e907b0708c0915c36aa3e2a13bf07e63c753967e920d4731bfe663f` |
| `sol/sol_reply_137_whyvoid.md` | `d8ba0431a8ea5e738b49a0a46b394b4fbb86515c2c37f34ade3ce5f64db5199f` |
| `sol/sol_reply_138_campaign.md` | `63053ab9613bec1a6ed1fcdb0d2b902c77581cbb11fcd406e79917fff8b70ed6` |
| `search/certs/ihnec_gap4_mcov_scan_20260801.json` | `fff0cee85e0e8a23c979fa74aba977660a816f44b75c3fadbf806879d9a09872` |

### 5.4 noncontact / endgame

- sealed three quantities: opened = false
- \(u\): opened = false
- \(c\): opened = false
- sealed K5: opened = false
- NAME-COLLIDE: 本便では核 \(W_{\rm ker}\)、\(W=PB_3/N_W\)、\(\bar W=B_3/N_W\) のいずれも計算対象にしていない
- `endgame_scope`: gentle side only; B₄ `PENT_W` = NOT_RUN; 後続の B₄/U-10 段 = NOT_RUN; finite-depth type adjudication = NONE
- `.git` は read-only。commit、push、workflow dispatch は行っていない
- 指定返書以外の作業ツリーを変更していない

BUILD_STATUS: PARTIAL
