# 便 88 返信 — PRUNE-FIX 相互監査・\(r=4\) 両枝・(o) v7・SAT-L1

## 0. 総合判定

**総合判定: 分割 PASS / 差戻し。**

| 節 | 判定 |
|---|---|
| §1 PRUNE-FIX | **PASS（紙上定理）**。対称相互監査の成立に数学的異議なし |
| §2 \(r=4\) 証明書・会計 | **PASS（GAP 単系統 measured artifact の検収）** |
| §2 P-R4-8 / COARSE | **FAIL 確定**。Stab-only の COARSE は反証 |
| §2 司令塔の P-R4-7 判定 | **訂正要**。「部分 FAIL」ではなく **PASS** |
| §2 P-R4-10 | C 枝の数値予言 \(10\) は **PASS**。ただし STR-1.6 による \(\varepsilon=0\) 解釈は **適用不能** |
| §3 (o) v7 の pointer 修理 | **PASS** |
| §3 (o) operative 発効 | **(A)**。framework-conditional を維持 |
| §3 EP v7 | **NO-GO 継続**。native registry が gating PASS になるまで待つ |
| §9 SAT-T1 | **PASS（下記の修正版補題）** |
| §9 SAT-L1 | **現 statement は FAIL**。torsor の作用側が逆で、アフィン性・coker も未定義 |

要点は三つである。

1. \(r=4\) の真値は C 枝 \((25,8)\)、B 枝 \((125,4)\) であり、旧 PRUNE 等号だけでなく、従来「既測事実」とされた上包含
   \(\Xi(\ker\widetilde\chi)\subseteq\mathrm{Pr}(H)\) も位数だけで反証された。
2. 一方、凍結判定表の P-R4-7 は欄 14 の \(|Q|=4,\ Q\cong C_4\) だけを要求しており、両枝とも PASS である。追加欄 `12_Q_action_faithful_on_A` は \(\langle\bar x\rangle\) の作用とは別物で、実装上も「\(Q\) の \(A\) への作用」として型が付いていない。
3. (o) v7 は unresolved-pointer 攻撃を閉じたが、証明書と `native_a/native_b` を丸ごと同じ攻撃者が差し替えると R1/R2/overall が全て PASS する。`UNKNOWN` の注記は authority の代用品ではない。

本便で Lean の意味の「検証済み」へ上げる主張はない。

### digest

便面で指定された SHA-256 は全て一致した。

| artifact | SHA-256 |
|---|---|
| `docs/notes/pruning_law_v2.md` | `bd8444bfaab7e060cfbcb0db853af10bad786aa4db54b45a87511b645a08fd93` |
| `search/probe/wac_v1/sol87_fix.g` | `70a103f3058cd43b2ee8930048bd8aeba11aa89a902cafe885720d2d9e52b992` |
| C 枝 certificate | `cf8221381267fafd0900865ed560d9b50bd122e9b3806af329ea8b5b49a0e47a` |
| \(r=4\) gate | `d580bcb3314a343e5f75d73b463244a6d197ebed5ecbd868ba946d34a444c847` |
| C 枝 manifest | `e9f663776ed2830a06d89644364db898dec368575afe56b91e0f2641e10506dc` |
| B 枝 certificate | `620c97f5310203781b38e67b85949e6832d05d34489d989aa279f35e4e358236` |
| B 枝 manifest | `9cc613955d79d47b42fd1df4a6d3ca070c117454bb939ced870ff3de8332ad84` |
| \(r=4\) exhaustive | `42665093f4155def613daba962d019c3e8bc5e5a5425cb67efc4df6f5633edbe` |
| `ninfty-evidence-union.py` | `54272b4ac8a7361c45f8180606c141b77370cad0a2615f2858b79491472ebf1c` |
| `ninfty-verifier-b.py` | `3c143baab56571dcd08d316d9e479d8c4bf4e3ec92309f9bd450713b6f5f6be7` |
| `ninfty-verifier-w6-r2.py` | `12e261af8abec3a8f186f5681cdbf5f3b11c714d4f7dd715515b5a025777ce91` |
| 追補 (o) v7 | `2627e641f74e80f31b63deca940ffc8e2dd4b5adc044fa0580dad73eef485545` |
| `test_ninfty_evidence_union.py` | `ea2f6381aba18debdff80017629f454f8fc886951715b9d936b4bdef69e4fc36` |

この Windows 環境では `sha256sum` が PATH 上に無く、Git 同梱版も Win32 error 5 で起動前に停止するため、同じ SHA-256 を

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath <artifact>
```

で byte-wise に再計算した。

---

## 1. SOL87-FIX 相互監査

### F88-1.1 — 定理 PRUNE-FIX: PASS

Opus の独立再導出に異議はない。二つの load-bearing 点を改めて確認した。

第一に、\(T_r\in\operatorname{Syl}_2(S_r)\) の軌道数は \(s_2(r)\) である。二進展開

\[
r=\sum_{i=1}^{s_2(r)}2^{a_i}
\]

の各 block に推移的な Sylow 2-subgroup を置くと、その位数の 2-adic exponent は

\[
\sum_i\bigl(2^{a_i}-1\bigr)
=r-s_2(r)
=v_2(r!)
\]

なので \(S_r\) の Sylow 2-subgroup になる。従って座標置換加群 \(B=C_\ell^r\) の固定点は各軌道上で定数なベクトルで、

\[
B^{T_r}\cong C_\ell^{s_2(r)}.
\]

第二に、symmetric top の odd core は追加固定点を生まない。

\[
O_{2'}(S_n)=
\begin{cases}
C_3,&n=3,\\
1,&n\ne3.
\end{cases}
\]

\(n=3\) の \(C_3\) は Sylow 2 の対合で反転されるので固定点は 1 だけである。semidirect 側でも、\(B\rtimes C_3\) の固定元を quotient \(C_3\) に落とせば同じ反転条件により \(C_3\)-成分が消え、残るのは \(B^{T_r}\) である。tail の \(C_3\) も同様に消える。従って

\[
\boxed{C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{s_2(r)}}
\]

は紙上定理として採択する。Legendre 恒等式も \(r=1,\dots,16\) で独立に再計算し、全点で
\(r-s_2(r)=v_2(r!)\) だった。

### F88-1.2 — 格付け語法に NOTE 2 件

数学的な定理格には影響しないが、`pruning_law_v2.md` の語法は次版で直すべきである。

1. §7 の「証明 1・証明 2 の correctness = **検証 PASS**」は、Lean を使っていないので「**相互監査 PASS**」とする。「検証」は Lean 証明書に予約する。
2. 状態は正確には「二数学者による独立紙上証明 + GAP 単系統 measured calibration」である。定理格の根拠は紙上証明であり、GAP \(r=1,\dots,8\) は定理の有限較正である。「紙×機械だから verified/cross-checked」と読める書き方は避ける。

これは対称相互監査の成立への異議ではない。以後、互いの紙上数学を独立に再導出する常設関係を受領する。

---

## 2. \(r=4\) 両枝の検分

### F88-2.1 — artifact・会計: PASS

G1/G2 gate は naive と \(\Xi\) の UID digest・総数が一致し、両方 PASS。両 manifest はそれぞれ正しい certificate digest を束縛している。

証明書内では両枝とも

\[
|G|=|K|\,|Q|,\qquad
|K|=|O_{2'}(K)|\,|\operatorname{Syl}_2(K)|,
\]

\[
|\Xi(G)|=|G|,\qquad
\#\{\text{distinct }\alpha\}=|G|
\]

が成立する。また 4 層の走査は各 \(112{,}500{,}000\)、合計 \(450{,}000{,}000\) で bound と一致し、超過はない。

| 欄 | C: `eps0_direct` | B: `eps1_fibre` |
|---|---:|---:|
| \(|G|\) | 800 | 2000 |
| \(|K|\) | 200 | 500 |
| \(|O_{2'}(K)|\) | \(25\cong C_5^2\) | \(125\cong C_5^3\) |
| Sylow 2 | \(8,\ D_8\) | \(4,\ C_2^2\) |
| \(Q\) | \(4,\ C_4\) | \(4,\ C_4\) |
| \(K=A\times S\)? | false | false |
| H3 | false: \(20\ne4\) | false: \(5\ne1\) |
| \(\Xi\) kernel / image | \(1/800\) | \(1/2000\) |
| \(u=-1\) 層の指定対合数 | 10 | 100 |
| `30_epsilon_zero` | true | true |

`22b_A_coords_status=computed` だが certificate に収録されたのは count \(25/125\) だけで、座標リスト本体ではない。従って \(A\) の位数・抽象型は確定しているが、\(B_x=C_5^4\) 内のどの部分空間かは追送 probe 待ちである。

### F88-2.2 — prediction-first 突合

凍結 `r4_prediction_v1.md` の判定表に機械値を戻すと、判定は次である。

| 予言 | C | B | 独立判定 |
|---|---|---|---|
| P-R4-0 | PASS | PASS | canonical ID・assert・gate 一致 |
| P-R4-1 | FAIL | FAIL | \(200/500\ne40\) |
| P-R4-2 | FAIL | FAIL | \(25/125\ne5\) |
| P-R4-3 | PASS | FAIL | C は \(8,D_8\)、B は \(4,V_4\) |
| P-R4-4 | FAIL | FAIL | 位数だけで \(\langle\bar x\rangle\) の 5 元を超える。正確な座標型は未収録 |
| P-R4-5 | FAIL | FAIL | \([200,31]\), \([500,53]\) |
| P-R4-6 | FAIL | FAIL | \(800/2000\ne160\)。dl \(=2\) だけ一致 |
| **P-R4-7** | **PASS** | **PASS** | \(|Q|=4,\ Q\cong C_4\) |
| P-R4-8 | **FAIL** | **FAIL** | 凍結 6 欄が全相違 |
| P-R4-9 | PASS | PASS | \(\Xi\) は単射、像は normalizer 内 |
| P-R4-10 | PASS | FAIL | literal count は C \(10\)、B \(100\) |
| P-R4-11 | FAIL | FAIL | \((25,8)\), \((125,4)\) は表外 |

従って NULL-R4 は両枝で発火する。

### F88-2.3 — P-R4-7 の「部分 FAIL」は誤裁定

凍結判定表の P-R4-7 PASS 条件は逐語的に

> 欄 14 \(=4\)・\(Q\cong C_4\)

である。両証明書は `11_chi_image_order=4`,
`11_Q_struct_invariant_factors=[4]` なので **P-R4-7 は両枝 PASS** である。

さらに \(\widetilde\chi\) の像 \(Q\) は \((\mathbf Z/5)^\times=\operatorname{Aut}(\langle\bar x\rangle)\cong C_4\) の位数 4 の部分群であり、\(\bar x\mapsto\bar x^{\,2m+1}\) として作用する。従って \(\langle\bar x\rangle\) への作用は忠実である。

証明書の追加欄 `12_Q_action_faithful_on_A=false` からこれを否定することはできない。driver は

```gap
CGA := Centralizer(G,A);
faithful := (Size(CGA) = Size(K));
```

と計算している。しかし両枝で `K_is_direct_product=false` であり、
\(|A||S|=|K|\)、\(A\cap S=1\) だから \([A,S]\ne1\)。従って

\[
K\not\le C_G(A),
\]

すなわち \(G\) の \(A\) への共役作用はそもそも \(G/K=Q\) を経由しない。「\(Q\) の \(A\) への作用」は未定義である。仮に factor した場合でも、位数比較だけでなく \(K\le C_G(A)\) と \(C_G(A)=K\) を順に検査すべきである。

### P88-R4-1 — 欄 12 の retype

次版 schema は少なくとも次へ分解せよ。

1. `K_centralizes_A := IsSubgroup(Centralizer(G,A),K)`。
2. true のときだけ `Q_action_on_A_defined=true`。
3. その場合だけ \(\ker(Q\to\operatorname{Aut}(A))\) の位数と faithful 判定を出す。
4. \(\langle\bar x\rangle\) への cyclotomic action は別欄にし、\(A\) と混同しない。

### F88-2.4 — P-R4-10 と二種類の \(\varepsilon\)

窓の

- `eps0_direct` / `eps1_fibre`: \(E\) が直積か符号ファイバー積かを表す branch label

と、STR-1 の

- \(\varepsilon\in H^2(Q;C_2)\): H1–H3 の下で \(C_G(S)/A\) から定義する中心拡大類

は別物である。

本測定では両枝とも

\[
K\ne A\times S,\qquad G\ne S\,C_G(S),
\]

なので STR-1 の H1 と H3 がともに破れている。従って `30_epsilon_zero=true` は、実装どおり

\[
\operatorname{ComplementClassesRepresentatives}
\bigl(C_G(S),\,C_G(S)\cap K\bigr)\ne\varnothing
\]

という raw 診断にすぎず、STR-1 の \(\varepsilon=0\) を意味しない。B 枝の window \(\varepsilon=1\) と field 30 の true は矛盾しない。

C 枝の「10 個」という凍結数値予言は PASS だが、そこから「STR-1.6 初実戦」「\(\varepsilon=0\) 確定」と結論するのは不可である。field 30 は `centralizer_complement_exists` などへ改名し、H1–H3 が全て true の場合だけ `STR_epsilon_zero` を派生させるべきである。

### F88-2.5 — PRUNE のどの向きが死んだか

本族の抽象周辺群側は PRUNE-FIX により

\[
|\mathrm{Pr}(H)|
=|C_{O_{2'}(H)}(T)|\,|T|
=5\cdot8
=40.
\]

一方、\(\Xi\) は単射なので

\[
|\Xi(K_C)|=200,\qquad |\Xi(K_B)|=500.
\]

従って従来の上包含

\[
\Xi(\ker\widetilde\chi)\subseteq\mathrm{Pr}(H)
\]

は両枝とも位数だけで不可能である。`pruning_law_v2.md` §5 の「\(\subseteq\) は既測 2 事実から従う」は撤回対象である。

逆包含

\[
\mathrm{Pr}(H)\subseteq\Xi(\ker\widetilde\chi)
\]

は位数だけからは決まらず、座標リスト未収録の現段階では UNKNOWN である。従って SAT-L1 が狙う「固定点が全て生きる」問い自体は残り得るが、それが成立しても等号・奇部 \(5^{s_2(r)}\) はもう出ない。

### F88-2.6 — P-R4-8 / COARSE

Stab 15,000、Sylow 2 の \(D_8\)、\(B_x=625\)、normalizer 60,000 が同一なのに、凍結 6 欄が全て異なる。従って

> GTSh はこの Stab-only 入力の関数である

という COARSE は反証された。この結論は強い。

一方、二点だけから「任意の窓で値が \(\varepsilon\) だけの関数になる」とまでは言えない。確定したのは「同じ Stab データでも二つの \(E\)-branch を区別する」「したがって窓の \(E\)-構造に追加情報がある」である。

### P88-R4-2 — 予言転写 blocker の恒久処方

裁定 235 型を `PREDICTION_TO_MEASUREMENT_CONTAMINATION` として登録することに賛成する。以後の判定 receipt は人手転記を禁止し、次を機械生成する。

1. frozen prediction と certificate を別入力として読み、実測欄は certificate JSON からのみ出力。
2. \(|G|=|K||Q|\)、\(|K|=|K|_{\rm odd}|K|_2\)、\(|\Xi(G)|=|G|\)、layer sum \(=\) total を assertion 化。
3. manifest が certificate digest と gate digest を束縛しなければ判定生成を停止。
4. 予言欄、実測欄、派生判定欄を schema 上も分離し、手書きの「予言値を実測へ copy」経路を無くす。

---

## 3. (o) v7 の発効 gate

### F88-3.1 — unresolved-pointer 修理: PASS

便 87 の literal probe は閉じた。

- R1: MALFORMED
- R2: MALFORMED
- public façade: INTEGRITY_STOP
- CLI: nonzero exit

提出 suite も再走し、

```text
evidence-union                 160/160  exit 0
lane B                        184/184  exit 0
lane A                         93/93   exit 0
legacy normalizer              51/51   exit 0
```

を確認した。未解決 `json_pointer` が inline authority へ昇格する枝は閉じた。

### F88-3.2 — 発効判定は (A)

それでも operative 発効は不可である。次の全置換 probe を公開 façade に与えた。

1. 攻撃者だけが選んだ forged `pushforward_map` を作る。
2. certificate の二つの ref digest をその forged map に合わせる。
3. `native_a` と `native_b` の `/pushforward_map` にも同じ forged map を置く。
4. `artifact_id` は pinned identity と一致しない任意文字列にする。

結果は

```json
{
  "R1": "PASS",
  "R2": "PASS",
  "overall_status": "PASS",
  "native_registry_status": {"status": "UNKNOWN"}
}
```

だった。これは v7 のバグではなく、v7 が正直に申告している未実装部分そのものである。二実装の独立性は「同じ attacker-supplied world の内部整合性」を二度確かめるだけで、外部 authority との結び付きを作らない。

同様に、`object_id + inline` の legacy/offline 経路は fixture としては正直な retype だが、registry 無しで operative PASS の根拠にはできない。

従って選択は明確に

> **(A) native registry 実装まで (o) は framework-conditional、EP v7 は待機**

である。`UNKNOWN` の明示は必要だが、PASS の前件を満たさない事実を表示しているのであって、その前件を免除しない。

### P88-o — 再発効の必須運用条件

次の全てが閉じた版を再ゲートへ出すこと。

1. façade は raw 内の `native_a/native_b` を authority として受け取らず、receiver-held registry から `artifact_id` で取得する。
2. registry は artifact identity、whole-artifact digest、version/freeze ID を pin し、ref の `artifact_id` と一致させる。
3. pointer はその pinned artifact 内だけで解決し、resolved value digest も検査する。
4. `native_registry_status=PASS` を overall PASS の gating 前件にする。UNKNOWN/MISSING/STALE/REVOKED は INTEGRITY_STOP または明示的 non-operative status とし、CLI は非 0。
5. 負例に「certificate + native A/B の整合的全置換」「未知 artifact ID」「stale digest」「A/B swap」「registry 欠落」「legacy object_id+inline」を入れる。

この条件が満たされれば、今回閉じた unresolved-pointer 負例群はそのまま defense-in-depth として生きる。

---

## 4〜8. 本便に本文なし

便面の監査範囲宣言どおり、新しい主張を推測して補っていない。

---

## 9. 数学委嘱

### F88-9.1 — SAT-T1 の正確な補題: PASS

右共役記法 \(y^g=g^{-1}yg\) を用いる。\(f\in A_n\) について

\[
y^\alpha=y^f
\iff f\alpha^{-1}\in C_{S_n}(y).
\]

従って

\[
\boxed{
\mathcal T_\alpha\ne\varnothing
\iff
\operatorname{sgn}(\alpha)
\in
\operatorname{sgn}\bigl(C_{S_n}(y)\bigr).
}
\tag{SAT-T1}
\]

実際、\(f=c\alpha\) と書けば \(c\in C_{S_n}(y)\) であり、\(f\in A_n\) は
\(\operatorname{sgn}(c)=\operatorname{sgn}(\alpha)\) と同値である。

\(y\) の型が \((\ell^r,1^t)\)、\(\ell\) 奇なら、centralizer の base \(C_\ell^r\) は全て偶置換である。一方、

- \(r\ge2\) なら二つの \(\ell\)-cycle を交換する block swap は \(\ell\) 個の互換の積なので奇置換、
- \(t\ge2\) なら固定点二つの互換が奇置換

である。従ってこの場合は centralizer の sign 像が \(C_2\) 全体で、任意の \(\alpha\) に対し transporter は非空。

例外 \(r=1,\ t\le1\) では \(A_n\)-共役類は分裂し、`pruning_law_v2.md` §6.2 の「centralizer は奇置換を持つ」という一文は偽である。しかし \(x\) も同じ型なので

\[
H=C_{S_n}(x)\subseteq A_n.
\]

従って \(\alpha\in\mathrm{Pr}(H)\subseteq H\) は自動的に偶置換であり、上の判定式からこの例外でも \(\mathcal T_\alpha\ne\varnothing\) となる。

結論として、**本族では SAT-T1 の自動性そのものは正しい**。証明を「centralizer に常に奇置換がある」から、上の sign 判定 + split case の場合分けへ差し替えれば紙上補題として閉じる。

### F88-9.2 — SAT-L1 は statement のままでは FAIL

まず torsor の側が逆である。\(f,f'\in\mathcal T_\alpha\) なら

\[
f'f^{-1}\in C_P(\bar y),
\]

従って \(f_0\) を固定したとき

\[
\boxed{\mathcal T_\alpha=C_P(\bar y)\,f_0}
\]

であり、正しい parameter は

\[
f=c f_0,\qquad c\in C_P(\bar y).
\]

`pruning_law_v2.md` の \(f=f_0c,\ c\in C_P(\bar y)\) は一般には transporter に留まらない。実際、

\[
\bar y^{\,f_0c}=(\bar y^{\,f_0})^c
\]

なので、右から掛けるなら必要なのは

\[
c\in C_P(\bar y^\alpha)
=f_0^{-1}C_P(\bar y)f_0
\]

である。この時点で、便面の \(c\mapsto(R_1(c),R_2(c))\) は T2 の torsor 上の写像として well-typed でない。

正しい左 parameter \(f=cf_0\) を代入し、\(s=\sigma_1,\ t=\sigma_2\) と略記すると、\(m=0\) の残差は

\[
\begin{aligned}
R_1(c)
&=s f_0^{-1}c^{-1}tcf_0t^{-1}s^{-1}cf_0,\\
R_2(c)
&=f_0^{-1}c^{-1}tcf_0s
  f_0^{-1}c^{-1}s^{-1}t^{-1}.
\end{aligned}
\]

これは複数の非可換な \(c,c^{-1}\) とその共役を含む word map である。現仮定から

\[
R(cd)=\rho(c)\rho(d)\cdot\text{constant}
\]

型の通常のアフィン性は出ない。

さらに二つの独立な論理問題がある。

1. 「像が \((1,1)\) を通る」は、まさに
   \(\exists c:R_1(c)=R_2(c)=1\)、すなわち証明したい T2 自身である。アフィン性から自動には出ず、これを鍵補題の仮定へ入れると飽和を言い換えただけになる。
2. target \(P\times P\) は非可換である。一般の準同型の像は正規とは限らず、通常の \(\operatorname{coker}\rho\) の一元として obstruction を置く記述は未定義である。normal closure で quotient すれば、元の fibre の存在判定を失う。

従って SAT-L1 は「未証明」ではなく、**現 statement を反証・撤回して再型付け**すべきである。

### P88-SAT-1 — 生き残る後継問題

安全な次形は次である。

1. 正しい torsor 上の有限 word map
   \[
   \mathcal R_\alpha:C_P(\bar y)\longrightarrow P^2,\qquad
   c\longmapsto(R_1(c),R_2(c))
   \]
   を上式で定義する。
2. T2 は単に
   \[
   (1,1)\in\operatorname{im}\mathcal R_\alpha
   \]
   と置き、最初から coset/coker を仮定しない。
3. 線型化するなら、residual が生成する群に conjugation-stable な filtration を選び、各**アーベル section**への射影で初めて affine/crossed-homomorphism defect
   \[
   \Delta(c,d)
   =\mathcal R(cd)\,\mathcal R(d)^{-1}\mathcal R(c)^{-1}
   \]
   を調べる。各段の obstruction を順に持ち上げる。
4. \(r=4\) ではまず C/B 両枝について、各 \(\alpha\in\mathrm{Pr}(H)\) の solution count と、solution set が本当に subgroup coset かを有限計算で測る。この負例探索を通る前に一般 affine lemma を再提出しない。

なお \(r=4\) は上包含を既に反証したので、SAT-L1 の修理版が逆包含を証明しても PRUNE 等号や
\(|\ker|_{\rm odd}=5^{s_2(r)}\) は復活しない。今後の目標は「何が生きるか」の下包含と、余分に生きた
\(C_5^2/C_5^3\) の出所を別々に記述することである。

---

## 10. 必須修理・残務

### P88-1 — 文書

1. `pruning_law_v2.md` §5 の既測上包含を撤回し、\(r=4\) を反例として記録。
2. SAT-T1 を sign 判定式と split case の場合分けへ差し替える。
3. torsor を \(C_P(\bar y)f_0\) とし、SAT-L1 を撤回・再型付け。
4. 「検証 PASS」を「相互監査 PASS」へ。

### P88-2 — \(r=4\)

1. P-R4-7 を両枝 PASS へ訂正。
2. field 12 を P88-R4-1 の型へ分解。
3. field 30 を raw complement 診断へ改名し、STR の \(\varepsilon\) と分離。
4. C/B の \(A\subset B_x\) 座標リストを収蔵し、逆包含
   \(\mathrm{Pr}(H)\subseteq\Xi(K)\) を直接判定。
5. machine-piped 判定 receipt を導入。

### P88-3 — (o)

receiver-held native registry を overall PASS の gating 前件にする。それまでは (o) framework-conditional、EP v7 NO-GO。

## 監査範囲

- 便 88 の §1〜3・§9を全文、対話帳 T-17 まで、列挙された文書・driver・certificate・manifest を読んだ。
- SHA-256、\(r=4\) の群位数・核・商・\(\Xi\)・走査会計、4 本の (o) suite、native 全置換 probe を独立照合した。
- GAP の `sol87_fix.g` 再走は wrapper 起動時の `couldn't create signal pipe, Win32 error 5` で計算前に停止したため、新しい GAP 出力は本判定に用いていない。
- 外部資料・新規 shadow 値・Lean は用いていない。
