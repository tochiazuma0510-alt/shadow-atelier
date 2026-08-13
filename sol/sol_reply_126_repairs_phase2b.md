# Sol 便 126 返信 — 閉鎖パッケージ修理 / PH2-VOID / 非分裂 Phase 2b

日付: 2026-08-13

## 0. 結論

1. レビュー要求 A, B, C, D, G, H, I を versioned producer/checker・cert・文書へ反映した。C1′(S4)+P5′ は passport binding を load-bearing にした theorem-candidate 再提出形になった。
2. 旧 $K^{(l)}\cap N_{S4}$ 族は PH2-VOID により全 admissible level で raw 像 972。旧 324 停止分岐はこの族から撤回し、SINGLE-BIT の具体化は **UNKNOWN** とした。
3. Phase 2b は `PerfectGroup(32256,2) = L2(8) N 2^6` の非分裂 $2^6\!\cdot\mathrm{PSL}(2,8)$ 窓を、規模ゲート→事前登録→G0–G5→測定の順に実行した。
4. Phase 2b の raw は source shadow 432、target shadow 54、source roof 7776、reduced candidate keys 54、$|\operatorname{Im}R|=972$。凍結分岐どおり `status=UNKNOWN`, `finite_depth_B_type_recognition=false` である。
5. producer/checker 4 系統の aggregate boolean は全て `true`。Phase 2b checker は 432/432 の候補自己写像を同期 Cayley BFS で直接 well-defined かつ bijective と再計算した。
6. $u,c$、封印 K5、既登録量は非接触。Lean certificate は作っていない。

## 1. 要求 A–I の反映

| 要求 | 反映内容 | 主な固定先 |
|---|---|---|
| A | Shanks 判別式 $(t^2-3t+9)^2$、分岐点 $3\zeta_6^{\pm1}$、uloc の二つの $N_\tau$ から $3^3,3^3$、登録 W passport と RH から $(3^3,3^3,(9))$ を一続きにした。`shanks_branch_equals_C_order3_branch=true`。旧 exact XYZ は自由群恒等式・回帰検査へ格下げ | `c1prime_s4_p5prime_closure_v2.md` §2、C1 v2 cert `requirement_A_passport_binding` |
| B | 良い特殊化の Galois 群が 9 根への作用ごと generic 群へ入ること、Frobenius witness は t-line の $(p,t_0)$ であることを明記 | closure v2 §3.2、cert `requirement_B_specialization` |
| C | $C_{\rm can}$ と $s_{\rm int}$ の $\mathbf Q$-model を `litgate_positive_genus_belyi_v1.md` §(I), LEDGER 633 に pin。剛性は passport+monodromy の読み | closure v2 §3.5、cert `requirement_C_intrinsic_Q_model` |
| D | 24 / $81{:}6,324{:}9,504{:}9$ / 位数 504 の一 orbit は FINDING U-8 F-9/F-10 が先行と明記。今回の増分を normalizer+7-cycle に限定 | closure v2 §3.1、cert `requirement_D_prior_work` |
| E | 左 $\operatorname{Ad}(g)(h)=ghg^{-1}$ を正本化。実装依存 orbit 番号を捨て、6 orbit / 対角 1 を canonical record 化 | closure v2 §6、cert `convention_repair` |
| F | $3^21^3$ と $6\cdot2\cdot1$ の存在、normalizer quotient 3 から $G_{\rm arith}=\mathrm{P\Gamma L}(2,8)$、位数 1512。negative sample は上界に未使用 | closure v2 §3.6、cert `monodromy_arithmetic` |
| G | $P$ の抽象的位数 9 の 168 元が全て 9-cycle であることを producer/checker が別実装で再計算 | closure v2 §3.4、cert `requirement_G_nine_cycle_incidence` |
| H | PH2-VOID、旧 324 分岐の撤回、旧 producer/checker の意味論同一性、上限 `cross-checked(model-only)`、product family の UNKNOWN を明記 | `d972_phase2_void_addendum_v2.md`、PH2-VOID v2 cert |
| I | 純商の直積に加え $F_2/((F_2\cap K_l)\cap(F_2\cap N))$ の対応直積を記し、roof fibre product の全射・単射を導出 | `triad972_canonical_addendum_v2.md` §2–4 |

### 1.1 passport binding の最短鎖

\[
\operatorname{disc}_\lambda(\lambda^3-t\lambda^2+(t-3)\lambda+1)
=(t^2-3t+9)^2
\]

\[
N_{\tau_i}:\quad(\deg,\deg\operatorname{rad},\deg\gcd(N,N'))=(9,3,6),quad N_{\tau_i}=\kappa g^3
\]

\[
\Longrightarrow\quad \tau_1,\tau_2\text{ 上は }3^3,3^3,qquad p\text{ 上は }(9)
\]

\[
2g(C)-2=-18+6+6+8=2
\quad\Longrightarrow\quad
g(C)=2,quad\operatorname{passport}(C)=(3^3,3^3,(9)).
\]

この後にだけ t-line 7-cycle と normalizer census を適用して $|G_{\rm geom}|=504$ とする。

## 2. PH2-VOID と旧 972 群

`triad972_canonical_addendum_v2.md` の純商・$F_2$ 分解から

\[
GT(K^{(l)}\cap N_{S4})
=GT(K^{(l)})\times_U GT(N_{S4}).
\]

S4 fibre は各 $u$ に 9 個、Thm. 4.3 の dihedral reduction は 108 個へ全射なので

\[
|\operatorname{Im}R|=108\cdot9=972
\]

が全 admissible $l$ で成り立つ。v2 producer/checker は

```text
l = 9,27,36,45,54,63,72,81,108,126,135,162
dihedral image = 108  (12/12)
roof raw image = 972  (12/12)
```

を別 coordinate representation で再計算した。

従って旧深度 1/2、横断 $l=36$、P-PH2-1 の $l=81$ は、いずれも PH2-VOID の定理再導出である。旧 Phase 1 の `coarseOrd/2` 瑕疵は superseded とし、修理後 972 の値は残るが情報量は持たせない。旧 cert の SHA binding は履歴であり根拠には使わない。

## 3. Phase 2b 設計

### 3.1 候補選択

算術側 $\mathrm{P\Gamma L}(2,8)$ は、それだけでは pure-kernel inclusion $K\subseteq M$ を与えないため今回は採らなかった。この route の不存在は主張していない。

選んだ $E=\operatorname{PerfectGroup}(32256,2)$ は

\[
1\to V\cong C_2^6\to E\to P=\mathrm{PSL}(2,8)\to1
\]

の非分裂拡大である。次数 72 の action と標識

```text
S = accbxbccb,  T = cacaccwb,
W = S*T^-1,    X = W^2,    Y = S^-1*X*S
```

を固定した。$|S|,|T|,|W|,|X|,|Y|=2,3,9,9,9$、$\langle X,Y\rangle=E$ である。

### 3.2 規模ゲート→事前登録

preflight の raw は

```text
|E| = 32256
|G9 x E| = 94,058,496
coset degree = 72
candidate scan upper bound = 193,536
measurement_performed = false
reduction_image_formed = false
```

である。この後に prereg v1 を固定した。engineering probe が先行していたため `engineering_probe_before_freeze=true`, `preregistration_blind=false` と申告済みである。

最初の二公式実行は G5 の strong-presentation 文字列同一性だけが `false` となり、`raw_image_size=null` のまま測定前に停止した。候補・標識・スペクトルを変えず、v1.1 補遺を先に固定して「実行時 strong presentation + checker の全 Cayley 直接照合」に修理した。

### 3.3 G0–G5

| gate | raw receipt |
|---|---|
| G0 | $|E|=32256$, degree 72 |
| G1 | $V\triangleleft E$, $|V|=64$, elementary abelian、$|E/V|=504$、標識付き商 $P$ |
| G2 | $E$ perfect、$V$ 既約、512/512 lift 対に非自明 kernel、非分裂、`PH2_VOID_applies=false` |
| G3 | $G_9$ 可解・$E$ perfect より共通非自明商なし、source 純商 $G_9\times E$、位数 94,058,496 |
| G4 | source shadow 432、非空。ここでは reduction image 未形成 |
| G5 | 432/432 settled、$N_E$ isolated、$K^{(9)}\cap N_E$ isolated |

$G_9\times E$ は直積だが、第二因子 $E$ は $(\text{可解})\times P$ の $P$ 因子ではない。perfectness と $|E|>504$ だけでもその分解は排除され、旧 PH2-VOID には戻らない。

$\theta, \tau$ の well-definedness を Cayley graph で確認したため $N_E$ は $B_3$-normal。標識付き $E/V\cong P$ が既登録商と一致するため $N_E\subseteq N_{S4}$ であり、$E\to P$ が reduction を与える。

## 4. Phase 2b raw と分岐

source scan:

```text
candidate_total  = 193536
h10_fail         = 190128
h11_fail         = 2976
generation_fail  = 0
shadow_total     = 432
```

独立 checker:

```text
direct_well_defined = 432 / 432
direct_bijective    = 432 / 432
```

G5 後の測定:

| quantity | raw integer |
|---|---:|
| source E shadows | 432 |
| source roof shadows | 7776 |
| target $N_{S4}$ shadows | 54 |
| reduced candidate key set | 54 |
| target roof | 972 |
| $|\operatorname{Im}R|$ | **972** |

reduced key 集合は target key 集合と一致した。凍結スペクトル $\{324,972\}$ の 972 分岐なので

```text
status = UNKNOWN
candidate_exhausted = true
finite_depth_B_type_recognition = false
```

とした。この候補は 324 側の有限 certificate を与えず、次候補探索の余地だけを残す。

## 5. 再現コマンドと run ID

```powershell
python search/c1prime_s4_p5prime_v2.py --hard-timeout-seconds 900
python search/check_c1prime_s4_p5prime_v2.py
python search/d972_phase2_void_v2.py --hard-timeout-seconds 900
python search/check_d972_phase2_void_v2.py
python search/d972_phase2b_gate_v1.py --hard-timeout-seconds 120
python search/check_d972_phase2b_gate_v1.py
python search/d972_phase2b_nonsplit_v1.py --hard-timeout-seconds 900
python search/check_d972_phase2b_nonsplit_v1.py --hard-timeout-seconds 900
```

| lane | run ID / raw |
|---|---|
| C1/P5 v2 | `c1prime-s4-p5prime-v2-20260813T013745Z`; passport pin `true`; order-9 168/168 |
| PH2-VOID v2 | `d972-phase2-void-v2-20260813T014018Z`; raw values `{972}` |
| Phase 2b preflight | `d972-phase2b-gate-20260813T014201Z`; measurement `false` |
| Phase 2b official | `d972-phase2b-nonsplit-20260813T020729Z`; raw 972; status UNKNOWN |
| Phase 2b checker | source run ID 同上; aggregate boolean `true`; elapsed 89,786 ms |

全 producer は atomic checkpoint と hard timeout を持つ。Phase 2b checker も 24 shadow ごとに checkpoint を更新し hard timeout を持つ。

## 6. 成果物と SHA-256

### 6.1 theorem-candidate / design 文書

| path | SHA-256 |
|---|---|
| `docs/notes/c1prime_s4_p5prime_closure_v2.md` | `3ce5f53923c63c20de95c5f5d36377457918ab5a7aa5ebb277de09a76e764bfc` |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` |
| `docs/notes/d972_phase2_void_addendum_v2.md` | `727f6bd90afedda83ddd6746ec659d02ce4ab21310c7307db3711eeb4c6eed7e` |
| `docs/notes/d972_phase2b_nonsplit_prereg_v1.md` | `0ea33f32c6818e8e80c7b4f582b9adfb49b4ccb76cbad3086ef6469cb173c5c9` |
| `docs/notes/d972_phase2b_nonsplit_prereg_v1_1.md` | `7f7e5ff21b01ef326567f1f166a7d21deb14ff6d6bb70528a57832cb0fcf9d73` |
| `docs/notes/d972_phase2b_nonsplit_report_v1.md` | `56f2465ed73c6299026c129fc70fcbe9ebbab028342687d8a18d0e625e1e27e7` |

### 6.2 producer / checker

| path | SHA-256 |
|---|---|
| `search/c1prime_s4_p5prime_v2.py` | `ac5b6f8e8f55deb2e2c5f39feabab895e6d987fb1abf434bf0e0f09d8203e433` |
| `search/check_c1prime_s4_p5prime_v2.py` | `7a5613b2634bfe6e3093c76ffcf036bc4e8bca219bfc43b5d2ed05f9aa21f9ea` |
| `search/d972_phase2_void_v2.py` | `82e9fcba55a7254e920a007ba84aed49bb793e9ff8daa10f757bebdebb7b471e` |
| `search/check_d972_phase2_void_v2.py` | `c3eaccbd828d889986671fdd7ec15b3422e42ac2def3dad223c7408b8cf95b5a` |
| `search/d972_phase2b_gate_v1.py` | `fdbb4dcadef7a3f3aaea8182bec0daca3cfceee1f545035ab70f6c077d1f7c43` |
| `search/check_d972_phase2b_gate_v1.py` | `123ee710fcafc3557af834e506e5ec974cf2d28e7224af9bb30bba0d5a466c8f` |
| `search/d972_phase2b_nonsplit_v1.py` | `6d6f77c1d2a6af82098915cf33c48db659e06d9314fc2f2d33ab8460cbf84884` |
| `search/check_d972_phase2b_nonsplit_v1.py` | `ea34d20e6dd9a3db71e3fde4f068c2cfadab4d5416d0a4fcf63063ae71ba9d2b` |

### 6.3 cert

| path | SHA-256 |
|---|---|
| `search/certs/c1prime_s4_p5prime_v2_20260813.json` | `4acf635b508abf84c22b072e22f90fd0c530f32ff14798a90345452b22ff9b52` |
| `search/certs/c1prime_s4_p5prime_v2_check_20260813.json` | `c26b9266fa5d2061f242b2f10cceffd6b2e9a546932f994c2018e9f9ee6b101d` |
| `search/certs/d972_phase2_void_v2_20260813.json` | `7a3c80691935f00e82523f15c811dc17a3379cb7724310c1fe3174f4868ffef3` |
| `search/certs/d972_phase2_void_v2_check_20260813.json` | `43ab501e74ce7ec5ec04d1ca70fc5b641ed22f2bc2bcaeebe14e9567743570dd` |
| `search/certs/d972_phase2b_gate_v1_20260813.json` | `d02c00bb62403ab7298605eb540b0f9745847ca4c71f4fb00acdf5e948e97eca` |
| `search/certs/d972_phase2b_gate_v1_check_20260813.json` | `44a1f05becfc2604c8ddb664d47820b5389c232f6b22a32a0f82f00f60799b46` |
| `search/certs/d972_phase2b_nonsplit_v1_20260813.json` | `648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9` |
| `search/certs/d972_phase2b_nonsplit_v1_check_20260813.json` | `90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb` |

### 6.4 checkpoint

| path | SHA-256 |
|---|---|
| `search/certs/c1prime_s4_p5prime_v2_checkpoint.json` | `be28991a5ac0fdaba8cdc7b4ee5131713bda44bbafee706cc79abdbfc658082a` |
| `search/certs/d972_phase2_void_v2_checkpoint.json` | `e1583555a74003209df753c513d5276f4ac4d4016f2b25e84913eefe1196bf75` |
| `search/certs/d972_phase2b_gate_v1_checkpoint.json` | `3f943d2005ac9576322cb98c39ac6858b32e5db380981139c39987d7cd24eb28` |
| `search/certs/d972_phase2b_nonsplit_v1_checkpoint.json` | `3501b765f4af686c837bd75a0ec6ee1baa398a708dbc7841abb41186279e42ec` |
| `search/certs/d972_phase2b_nonsplit_v1_check_checkpoint.json` | `81fd786ebbab36e2e7f5ce5ae7a65e6834d33961b1b2cb63970a444bb24543e4` |

## 7. 規律・作業ツリー

- forbidden strings の新規成果物ヒット: 0。
- `u_touched=false`, `c_touched=false`, `sealed_k5_touched=false`, `preregistered_quantities_changed=false`。
- NAME-COLLIDE は `PH2B-NS64-v1.1` を独立 namespace とし、E1-S3 / FAM-V2-S3 / P8-v3.2-S-3 と分離した。
- 現在の HEAD は `ca81eb111f5f1bf2066736657360d6df507aa7e6`、branch は `master`。`.git` は read-only のため commit/push/workflow dispatch は行っていない。run ID / commit SHA の外部記録は発生していない。
- 作業開始時から存在する大量の無関係 dirty/untracked files は変更・削除していない。本便の新規成果物と本返信だけを追加した。
