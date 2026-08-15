# 返書 134 — 非可換核細分の棚卸し・事前スクリーン・元単位 survival

- 対象: `ops/inbox_codex/sol_task_134_survival.txt`
- 実行日: 2026-08-15
- 基準 HEAD: `288d0aaaa334d9380f8a4269fe55a65c71b6f02e`
- 到達段: §4 完走
- 状態: **UNKNOWN 維持**

## 0. 一行への回答

非可換性だけでは盲 7 族の外へ出ない。実際、屋根商と共通商を持たない非可換有限商を足すだけなら純商は直積となり、族 1 に入る。このため探索域を

\[
\boxed{\text{非可換 }W_{\rm ker}\quad\text{かつ非自明な共通商を持つ fiber product}}
\]

へ縮小した。その最小の構成的候補として、標数 2・Magnus 次数 cutoff を小さい順に調べ、最初に非可換核が現れる cutoff 5 を採った。この候補で frozen 972 元を全走査した結果、各元の survival 数は一様に 16、零 survival 元は 0 だった。この有限窓から反対側への推論は行わない。

## 0.1 論理 pin の監査

便の 5 段は正しい。

1. isolated 性から (GT(M)) と 𝔊\(_{\rm gen}) が群・部分群になる。
2. (A\le 𝔊_{\rm gen}\le GT(M)) と ([GT(M):A]=3) に指数の乗法性を使えば、中間部分群は (A) と (GT(M)) の二つだけである。正規性は不要。
3. Cor. 5.4 の易しい向きの対偶により、一つでも持ち上げ 0 の元があれば 𝔊\(_{\rm gen}\ne GT(M)) となり、上の二択が閉じる。
4. 従って検定元を算術部分群の外から選ぶ必要はない。また survival を持つ元が 324 未満なら実装停止、という内蔵対照は妥当。
5. 全元が有限深度で survive することから逆向きの結論は出ない。

今回の生値は `target_nonzero_count=972` なので、内蔵対照の停止条件には触れなかった。

## 1. 盲 7 族の前提監査

まず「非可換核なら自動的に全 7 族を抜ける」は成り立たない。たとえば (Q=PB_3/M) と共通商を持たない非可換 (p)-商 (U) を足すと、像は (Q\times U) になり族 1 へ戻る。本走候補については次の通り。

| 族 | 本走候補に適用 | 一行理由 |
|---:|:---:|---|
| 1 分裂屋根 | false | source は (C_2^2) 上の非自明 fiber product。位数は直積位数の (1/4) |
| 2 (K^{(l)}\cap N_{S4}) | false | 新しい (K) は Magnus dimension subgroup との交わりで、この族ではない |
| 3 perfect (E) | false | 追加商は有限 2 群 |
| 4 可換 (C_3) 橋 | false | 共通商は (C_2^2)、かつ (W_{\rm ker}) は非可換 |
| 5 片側自明 (V) | false | 一方で自明な可換加群を用いていない |
| 6 tensor-only (mathbf F_3) | false | (mathbf F_3) tensor module を用いていない |
| 7 (p\ne3) 係数 | false | 既在定理の構造前提は可換正規核。本候補の全核は非可換 |

従って本走候補は既在 7 族の逐語仮定には当たらない。ただし今回の一様 survival は、族 7 に非可換 coprime-kernel 版があり得ることを示すデータにはなっている。定理化はしていない。

## 2. 細分の在庫棚卸しと構成

### 2.1 明示構成

記号衝突を避け、追加商を (U_5) と書く。次数 5 以上を切った非可換多項式環

\[
R_5=\mathbf F_2\langle X,Y\rangle/(\text{degree}\ge5)
\]

の単元群で

\[
U_5:=\langle1+X,1+Y\rangle,qquad
D_5:=\ker(F_2\to U_5)
\]

と置いた。ここで (D_5=\{g:g-1\in I^5\}) は augmentation-ideal dimension subgroup なので characteristic。さらに機械上も

\[
\theta:x\mapsto y, y\mapsto x,qquad
\tau:x\mapsto y, y\mapsto(xy)^{-1}
\]

が (U_5) に降り、θ²=1、τ³=1 を全 8,192 元で確認した。従って

\[
N_{\rm Mag,5}=D_5\times\langle c\rangle,qquad
K:=M\cap N_{\rm Mag,5}
\]

は (B_3)-正規・有限指数で (K\subseteq M) である。

(G_9) は別実装で

```text
|G9| = 2916
|[G9,G9]| = 729
G9^ab = C2 x C2
```

を再構成した。PSL 因子は perfect。(U_5^{\rm ab}=C_8^2) から mod 2 への標識付き商を取ると、(F_2) の像は

\[
PB_3/K\cong
(G_9\times\operatorname{PSL}(2,8))\times_{C_2^2}U_5.
\]

従って (PB_3/K\twoheadrightarrow PB_3/M) は明示的に存在し、

\[
|PB_3/K|=\frac{1,469,664\cdot8,192}{4}
=3,009,871,872.
\]

相対核は

\[
W_{\rm ker}=M/K\cong\ker(U_5\to C_2^2)=\Phi(U_5).
\]

生の構造量は次の通り。

| 量 | 値 |
|---|---:|
| |(W_{\rm ker})| | 2,048 |
| 可換 | false |
| nilpotency class | 2 |
| exponent | 4 |
| 最小生成元数 | 5 |
| |([W_{\rm ker},W_{\rm ker}])| | 8 |
| |(Z(W_{\rm ker}))| | 256 |
| (W_{\rm ker}^{\rm ab}) | (C_4^3\times C_2^2) |
| 元位数分布 | (1:1, 2:255, 4:1792) |
| SmallGroup id | `null`。位数 2,048 は完全 ID 在庫外 |

### 2.2 cutoff 在庫

標数 2、cutoff を 2,3,4,5 の順で固定して調べた。

| cutoff | |(U_d)| | generator order | |(W_{\rm ker})| | 可換 | |(PB_3/K_d)| |
|---:|---:|---:|---:|:---:|---:|
| 2 | 4 | 2 | 1 | true | 1,469,664 |
| 3 | 32 | 4 | 8 | true | 11,757,312 |
| 4 | 128 | 4 | 32 | true | 47,029,248 |
| 5 | 8,192 | 8 | 2,048 | false | 3,009,871,872 |

選択規約は「標数 2、cutoff 昇順、最初の非可換 (W_{\rm ker})」で、cutoff 5 に一意に止まる。

### 2.3 他の探索路

| 路 | 到達 | 理由 |
|---|---|---|
| `lins` | 未構成 | (M\cap F_2) の index は 1,469,664、Schreier rank は 1,469,665。これを表示して内側の低指数正規部分群を列挙する規模ではない。有限商 (Q) の部分群列挙は (M) の上側を見てしまい、向きも違う |
| `GQuotients` / PSL 拡大 | 未構成 | 既存在庫の位数 32,256 の非分裂拡大は相対核 (C_2^6) で本便の標的外。中心拡大は task の Schur multiplier pin で消え、非中心・非可換核の bounded target list は未供給 |
| `ANUPQ` | GAP 実行前停止 | `gap.ps1` を 2 回起動したが、いずれも script 読込前に `couldn't create signal pipe, Win32 error 5`、exit 1。群構成の失敗ではない |

公式成果は `Pq` の出力ではなく、二つの独立な truncated-Magnus 実装による。

## 3. (W_{\rm ker}^{ab}) 事前スクリーン


\[
W_{\rm ker}^{\rm ab}\cong C_4^3\times C_2^2,qquad |W_{\rm ker}^{\rm ab}|=256.
\]

同じ量を体上で定義するため

\[
V:=W_{\rm ker}^{\rm ab}/2W_{\rm ker}^{\rm ab}\cong\mathbf F_2^5
\]

とした。この (V) 上での生値は

| 量 | cardinality | dimension |
|---|---:|---:|
| |(ker(1+\theta^*))| | 8 | 3 |
| |(ker(1+\tau^*+\tau^{*2}))| | 16 | 4 |
| 交わり | 4 | **(d=2)** |

である。(W_{\rm ker}^{\rm ab}) そのものでは対応する cardinality が 32、64、8。従って abelianization 段での全消滅強制は `false` で、§4 へ進む条件を満たした。

## 4. 元単位 survival 全数検定

### 4.1 元の選択と非盲申告

入力は

```text
search/certs/nf972_sourcemap_a_tuples_v2_20260804.json
sha256 cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801
```

の **972 元全部**、格納順、`k=972` とした。選び直し・除外はない。ただし小規模 engineering probe が versioned freeze より先行したため、cert には

```text
engineering_probe_before_versioned_freeze = true
preregistration_blind = false
outcome_adaptive = false
```

と正直に記録した。全宇宙を使うため、元選択の適応性は残らない。

### 4.2 fiber と正典座標

共通 (C_2^2) は可換で、([Q,Q]) は (C_2) 商を持たず、([U_5,U_5]) は 2 群なので、Goursat から

\[
[PB_3/K,PB_3/K]=[Q,Q]\times[U_5,U_5].
\]

よって各 (f) の derived-fiber はちょうど

\[
[U_5,U_5],qquad |[U_5,U_5]|=128,qquad [U_5,U_5]\text{ は可換}
\]

であり、全候補が fine quotient の derived subgroup に入る。従って Prop. 3.4 の二式縮約を使い、full (3.3)(3.4) には切り替えなかった。

重要な座標修理として、旧 Phase 1 型の (2m+1) だけの一致は使っていない。正典 (3.60) に従い

\[
m_{\rm fine}\equiv m\pmod{18}
\]

を課した。fine order は 72 なので各元に compatible な (m_{\rm fine}) は 4 個、従って pair denominator は (4\cdot128=512)。初回 engineering probe の mod 9 条件は候補を二重計数する瑕疵で、正式 cert 前に mod 18 へ修理した。

### 4.3 SURJ 前件

H8′ を全 source 群へ直接適用してはいない。各候補で (u=2m_{\rm fine}+1) は奇数なので、(U_5/\Phi(U_5)=C_2^2) 上の二生成元像は標準基底となり、(U_5) 射影が全射になる。target (Q) 射影は入力が (GT(M)) の元なので全射。両群の最大共通 2 商が固定 (C_2^2) だけであることから source fiber product 全体への全射が従う。

これは全 (48=12\ m\text{-cells}\times4) cells について、実 subgroup closure が毎回 8,192 元になることでも照合した。さらに全 128 fiber 元ごとに Frattini quotient の rank 2 を検査した。

### 4.4 生値

各 compatible (m_{\rm fine}) で同じ値だった。

| denominator | (3.10) | (3.11) | 両式 + SURJ |
|---:|---:|---:|---:|
| 128 | 32 | 16 | **4** |

従って各 target 元について

| 量 | 値 |
|---|---:|
| compatible (m_{\rm fine}) | 4 |
| pair denominator | 512 |
| survival 数 | **16** |

972 元全体の分布は

```text
{16: 972}
zero_survival_target_count = 0
target_nonzero_count = 972
positive_control_minimum = 324
positive_control_pass = true
```

である。零 survival の有限証明書はこの (K) からは得られなかった。全元がこの一窓で survive した、という生値だけを保存し、それ以上の結論は付けない。

## 5. 証明書・再現・格

再現コマンド:

```powershell
python search/d972_survival_noncomm_v1.py --hard-timeout-seconds 120
python crosscheck/check_d972_survival_noncomm_v1.py --hard-timeout-seconds 120
```

- producer: packed-bit Magnus 元 + dihedral triple (G_9)、wall 16,373 ms。
- checker: literal monomial frozenset + degree-27 permutation (G_9)、producer import なし、wall 26,226 ms。
- 一致項: |(G_9)|、|(G_9')|、|(U_5)|、(W_{\rm ker}) の位数・中心・導来群・可換化、(d)、derived-fiber、48 generation fixtures、全 survival 分布。
- 格: **cross-checked**。Lean certificate はなく、`verified` ではない。

| artifact | SHA-256 |
|---|---|
| `search/d972_survival_noncomm_inventory_v1.g` | `e74986a9903724f249dc8d5dc55061aed61ecbd2be5613355c2868dccc91f7af` |
| `search/d972_survival_noncomm_v1.py` | `5686cd3d88cac6de6a904c36aa34fee5e07885158135de2e7f55824b16b5e8e3` |
| `crosscheck/check_d972_survival_noncomm_v1.py` | `bdcafe90ffe2dc3a331e966e34b02058653096f559253b756f81ff3d2f495bfd` |
| `search/certs/d972_survival_noncomm_v1_20260815.json` | `2b79438f7bfe574103bfcf6e30d9c873aa358dec7d254c98088a7003b5a25df3` |
| `search/certs/.d972_survival_noncomm_v1_checkpoint.json` | `8478e29e4cb550ea76a0fc17240b60b030d0d039db65ef06b666b53e7a68a238` |
| `crosscheck/verdicts/d972_survival_noncomm_v1_20260815.json` | `8006d83db4fca54cf735b92d4a3b236af9c26cef105e14d6eccfcd6b7824c3f5` |
| `crosscheck/verdicts/.d972_survival_noncomm_v1_checkpoint.json` | `8adc11a33307b8afc5ce3b12e7a05bf57ca12a0759927bea5826660d53961f31` |

## 6. 終盤勘定

本走は gentle 側の有限測定だけである。raw cert の `endgame_scope` に、B4 層では `PENT_W-PASS` を先に要求し、その後に指定された B4/U-10 鎖へ進む、という順序を保存した。今回その昇格は行っていない。

## 7. 規律・novelty receipt

- `W=PB3/N_W`、`Wbar=B3/N_W` と区別し、相対核は全箇所 (W_{\rm ker}) とした。
- hard timeout 120 秒、atomic checkpoint を producer/checker 双方で使用。
- 封印 3 量、`u/c`、sealed payload は非接触。
- `.git` は read-only。commit/push/workflow dispatch は行っていない。
- GAP は 2 回とも runtime 起動層で止まり、別経路の成功として数えていない。
- novelty grep（新規 artifact を除外）の件数:

```text
3009871872             0
truncated_magnus_F2    0
D_5(F2)                0
W_ker.*2048            0
survival.*16.*972      1  (別対象の既存 one-line cert)
```

最後の一般 pattern は別対象への既存ヒットであり、本便の新規性主張には用いない。外部文献検索も行っていない。
