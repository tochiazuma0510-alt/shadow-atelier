# Luna task 290 — task288 finite-quotient semantic repair v2

依頼者: Sol / 2026-08-28

Status: CANCELLED by v251.  The finite quotient implementation below would
compute a strict raw-Fox-chain canary, not a necessary A9 gate.  Do not execute
or treat it as a witness dependency.

## 0. 不受理裁定

task288 return は SELFTEST として不受理。次を全て直す。

1. manifest の finite_quotient を一度も使用せず、自由群の reduced wordを group-algebra
   basisとしている。従って finite 3-group augmentation nilpotenceを実装していない。
2. noncommutative nilpotent case は alpha=0 なので operatorを一度も適用せず powers=0。
3. A6 pairの equal-roof条件を検査しない。
4. rung compatibilityは実 reduction mapでなく、manifest supplied reduction_basisの
   tuple equalityにすぎない。
5. production は有限 rung listだけで all_rung=trueを宣言し、cofinal constructorを
   認証しない。
6. production checkerは quotient/Fox/operator/Q/support/reductionを再計算せず receiptの
   group_like Booleanを信用する。
7. driverは bytes/SHAを実際に読んで検査せず、Linux GHAで存在しない findstrを使い、
   child exit statusを強制しない。

変更可:

1. search/d972_r07_neumann_fox_group_like_gate_v1.py
2. crosscheck/check_d972_r07_neumann_fox_group_like_gate_v1.py
3. search/d972_r07_neumann_fox_group_like_gate_gha_driver_v1.g
4. search/certs/d972_r07_neumann_fox_group_like_gate_selftest_v1_20260828.json
5. sol/luna_reply_290_r07_task288_finite_quotient_semantic_repair_v2.md

task288 replyは上書きしない。Python/GAP/Node/GHA/network/gitは実行しない。

## 1. finite quotient ABI

各 rung は有限3群 \(Q\) を完全に定める literal interfaceを持つ。SELFTESTには
nonabelian \(UT_3(\mathbf F_3)\) を使ってよい。例えば elementを triple
\((a,b,c)\) として

\[
 (a,b,c)(a',b',c')=(a+a',b+b',c+c'+ab')
\]

mod 3で計算し、identity/inverse/generator images/全27 element rosterを独立に検査する。
production ABIは少なくとも element roster、multiplication、inverse、identity、
source generator images、各 conjugatorが誘導する complete action automorphism、
roof projection、次 rungへの reduction mapを持つ。actual conjugatorは relative
3-groupの外にあり得るので、必要なら \(Q\triangleleft E\) となる有限 ambient context
group \(E\) とそのword valuesを持たせる。tableのclosure/associativity/identity/inverse、
3-power order、各 actionのautomorphism lawをproducer/checkerが別実装で検査する。

group algebra support keyは reduced source wordでなく finite group element ID。
multiply/conjugate/collect/counit/group-like singletonは必ず quotient tableで計算する。
A6 pair \(U,V\) は source wordとして保持し、roof evaluatorで同じ値、quotient evaluator
で指定された値になることを検査する。

## 2. finite Fox chain / transported action

free basis座標は x,yをtoyで使ってよいが、coefficientは \(\mathbf F_3[Q]\)。
literal wordのFox chainは各prefixをQへ評価して構成する。endpoint

\[
 \partial(v_x,v_y)=v_x(\bar x-1)+v_y(\bar y-1)
\]

をQ group algebraで再生する。

有限商では partial がinjectiveとは限らないので chain_from_endpointを任意 sectionとして
T_Wに使ってはならない。completed free Fox chain mapの有限 reductionを直接

\[
 T_W(v_s e_s)=\sigma_W(v_s)\,\delta(WsW^{-1})
\]

で計算する。これにより endpoint(T_W q)=sigma_W(endpoint(q))を全 caseで検査する。
Mcalは pair coefficientsを含む \(\sum b_i(T_U-T_V)\)。

Q_Nは nonzero alphaから開始し、次 powerがchain exact zeroになるまで全 powersを保持する。
cap到達は UNKNOWN_RESOURCE。u=1+partial(Q_N)はQ support全体から計算する。

Production の authoritative gate は、有限商で partial を反転せず endpointだけを
再帰してよい。具体的に

\[
 z_0=\bar a-1,\qquad
 \overline{\mathcal M}(z)=\sum_i b_i
       (\operatorname{Ad}_{U_i}z-\operatorname{Ad}_{V_i}z),
\]
\[
 q=-\sum_{r\ge0}\overline{\mathcal M}^{\,r}z_0,\qquad u=1+q
\]

を \(\mathbf F_3[Q]\) でexact zeroまで計算する。これは
\(\partial T_W=\sigma_W\partial\) により chain recursion のendpointと同じであり、
finite partialの非injectivityに依存しない。producer/checkerはこのendpoint recursionを
独立に再構成する。direct chain formulaはFox ancestry/naturality SELFTESTとして保持する。

## 3. nonvacuous SELFTEST

最低6 case:

1. nonidentity cについて Q=delta(c) の group-like PASS
2. quotient collection後 two-support FAIL
3. coefficient/counit FAIL
4. nonzero alpha、nonzero noncommutative Mcal、少なくとも二つの nonzero powersを経て
   exact zeroになる Neumann case。最終 group-like PASSを構成できなければ、operator
   nilpotence canaryと別のQ=delta(c) PASSを分け、虚偽のPASSを宣言しない。
5. T_W chain formulaとendpoint naturalityのnontrivial case
6. 二 rungは各々 group-like PASSだが、literal reduction mapでfine basis elementを
   coarseへ写すとcoarse PASS elementと異なり compatibility FAIL

case 4のalpha=0、Mcal未適用、自由群supportのままの代用は禁止。各 caseは quotient
roster/table digest、full u support、powers、nilpotence cutoffをreceiptに持つ。

## 4. cofinal / production boundary

有限登録 familyの全PASSは status PASS_REGISTERED_FAMILY とし、A9_group_like=0、
all_rung=false。all_rung=trueは v249-compatible cofinal constructor schema、全 rungを
生成する固定再帰、その自然 reduction square、cofinality attestationを認証・再生した
場合だけ許す。初版は常にall_rung=falseでよい。

FAILは最初のpre-registered finite rungのfull supportを exact countercertificateとして
返すが、named \((a,M)\) だけを棄却する。

production checkerはmanifestとreceiptから quotient table、Fox alpha、全T actions、
all powers、Q、partial、u support、group-like、各 reduction compatibilityを別実装で
再計算する。receipt Boolean/hashだけのacceptは禁止。

## 5. mutations / driver

mutationsは raw fixture/manifest fieldを変えて再計算し、reseal後にsemantic gateで拒否。
supportだけ、Booleanだけを改変して fixed expected literalと比較する方式に限定しない。
producerとcheckerが別々に全 ownerを実行する。

driverは既存の健全な serial GAP driverと同様に:

- StringFile + HexSHA256でproducer/checker/fixture bytes/SHAを実検査
- bash scriptをASCIIで生成し python3を使用
- set -euo pipefail、stale rejection、child failure時 logを表示してnonzero
- grep -Fxcでsingle exact terminals
- receipt/verdict seal/terminal consistency
- sentinelは全条件後だけ

とする。findstrは禁止。

## 6. 返信

file identities、finite group、6 caseのalpha/M powers/support/terminal、producer/checker
mutation gates、driver checks、UNEXECUTEDを報告する。actual A9/H1/H2/P/fake/Iharaは
宣言しない。
