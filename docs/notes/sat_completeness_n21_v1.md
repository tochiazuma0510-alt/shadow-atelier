# SAT-COMP-21 完全性補題ノート v1 — n=21 tail-8 CNF#2(transitive)の completeness 方向

作成: 司令塔(裁定 214 工程 4・実装担当への委譲実施分を反映)・2026-07-30
出典: `sol/sol_reply_85_math12.md` §8(F85-8.2・F85-8.3・F85-8.4)。証明本体は **Sol が起草・供給**(数学者による再導出ではない — F85-8.2 の証明文をこのノートへそのまま正典転記し、記法のみ本工房の慣例に合わせた)。
状態: **paper-proof PASS(Sol 供給・便 85 §8 で提示、司令塔・実装担当は転記と CI artifact との突合のみ実施。数学者による独立監査は未実施)**。
関連: `search/sat/README.md`(SAT パイプライン一般)・`search/sat/manifest_tail8_n21.json`(encoder マニフェスト、`audit_status.completeness_direction: "NOT AUDITED HERE"` の記述を本ノートが埋める)・`search/sat/runs/RUNS_LEDGER.md`(CI artifact 収蔵)。

---

## 0. 語法注意(CLAUDE.md 準拠)

**「DRAT 照合済み」と「検証済み(verified)」は同義ではない**。本ノートが扱う completeness 補題は紙の上の命題であり、Lean 化されていない。CI artifact に対する `drat-trim` の `s VERIFIED`(`search/sat/runs/n21_transitive/drat_verify.txt`)は「この CNF から矛盾が導ける」ことの **DRAT 照合**であって、それ自体は「n=21 tail-8 の数学的主張が正しい」ことの検証ではない。両者を合成して初めて

> transitive CNF の UNSAT(DRAT 照合済み)+ completeness 補題(paper-proof)
> ⟹ 「固定 u に対し a∈2¹⁰1, b=au⁻¹∈3⁷ で ⟨a,b⟩ が S₂₁ で推移的なものは存在しない」の **cross-checked** な非存在主張

が言える。**「検証済み」の語は Lean 化まで使わない**(CLAUDE.md 鉄則 2)。以下の状態表記を正本とする:

```text
encoding completeness = paper-proof PASS(Sol 供給・数学者未監査)
CI DRAT verification   = artifact 収蔵・再照合済み(search/sat/runs/RUNS_LEDGER.md)
独立 LRAT checker       = 実装済み・実行済み・VERIFIED(search/sat/lrat_check.py)
Lean 検証済み            = no
```

---

## 1. 対象と記法

固定 $u=(1\,2\,\dots\,13)(14\,15)(16\,17)(18\,19)(20\,21)\in S_{21}$(`search/sat/manifest_tail8_n21.json` の `fixed_u` と同一)。

`search/sat/encode_tail8_n21.py` が生成する CNF#2(`tail8_n21_transitive.cnf`)の変数族:
- $X_{ij}$($i<j$): $a(i)=j$(かつ involution 対称性で $a(j)=i$)。
- $D_i$: $a(i)=i$。
- $B_{ik}$: $b(i)=k$(規約 $b:=a\,u^{-1}$、すなわち $b(i)=u^{-1}(a(i))$)。
- $E_{ij}$($i<j$): $\{a,b,b^{-1}\}$ による無向 Schreier graph の隣接。
- $R_{t,v}$($t=0,\dots,20$): 頂点 1 から $v$ まで距離 $\le t$。
- $\mathrm{STEP}_{t,w,v}=E_{wv}\wedge R_{t-1,w}$(Tseitin AND ゲート、$w\ne v$)。

節群は `search/sat/manifest_tail8_n21.json` の `clause_groups.transitive_cnf` を正本とする(節番号レンジは実装が自己生成、手打ち転記なし)。

---

## 2. 補題 SAT-COMP-21(completeness 方向)

> **補題 SAT-COMP-21.** 固定した $u$ に対し、$a$ が型 $2^{10}1$ の involution、$b=au^{-1}$ が型 $3^7$、$\langle a,b\rangle$ が $\{1,\dots,21\}$ 上推移的なら、`tail8_n21_transitive.cnf` は充足可能である。

### 証明(Sol、`sol/sol_reply_85_math12.md` F85-8.2 §証明 の転記)

1. $X_{ij}=1$($i<j$)を $a(i)=j$(したがって $a(j)=i$)のとき、$D_i=1$ を $a(i)=i$ のときと定める。$a$ は involution なので各 row exactly-one を満たし、型 $2^{10}1$ なので $D_i$ は全体で exactly-one。
2. $B_{ik}=1\iff b(i)=k$ と置く。規約 $b(i)=u^{-1}(a(i))$ より $B_{ik}=1\iff a(i)=u(k)$、したがって encoder の $B$-Tseitin biconditional を全て満たす。
3. $b$ は型 $3^7$ なので fixed-point-free かつ $b^3=1$。$B$ は permutation matrix であるため、encoder の全 $b^3$-implication と diagonal negative clause を満たす。
4. $i<j$ に対し $E_{ij}=1\iff j\in\{a(i),b(i),b^{-1}(i)\}$ と定める。これは $\{a,b,b^{-1}\}$ による無向 Schreier graph の adjacency そのもので、$E$ の biconditional を満たす。
5. $R_{t,v}=1$ を「頂点 1 から $v$ まで距離 $\le t$」と定め、$\mathrm{STEP}_{t,w,v}=E_{wv}\wedge R_{t-1,w}$ と定める。すると base case、AND Tseitin、recurrence biconditional を全て満たす。
6. $\langle a,b\rangle$ が推移的ならこの graph は連結。21 頂点の連結 graph では点 1 からの距離は高々 20 なので、全 $v$ に対し $R_{20,v}=1$。最後の goal clauses も満たす。

以上で genuine witness から CNF assignment を構成できる。$\square$

同じ構成の手順 1–3 だけで class CNF(`tail8_n21_class.cnf`)の completeness も従う(transitivity 部分を除いた同一構成)。

---

## 3. 固定代表 $u$ で十分な理由(F85-8.3 の転記)

対象 cycle type の全 $u'$ は $S_{21}$ で共役である。$u'=huh^{-1}$ に対する witness $(a',b')$ を同時共役すれば、固定 $u$ に対する witness を得る。cycle type と推移性は同時共役で保存される。したがって固定 representative の transitive CNF が UNSAT なら、同 cycle class の全 $u$ に対して transitive witness は存在しない。

A21-generation は推移性を含意するので、

$$\text{transitive UNSAT}\Longrightarrow\text{A}_{21}\text{-generating pair なし}.$$

これで encoding fidelity の「数学 witness $\Rightarrow$ assignment」方向は閉じた。

---

## 4. この補題の射程外(soundness 方向・完全性の逆)

本補題は **completeness 方向のみ**(genuine witness ⟹ SAT assignment、対偶で UNSAT ⟹ no genuine witness)を扱う。**soundness 方向**(decoded SAT model ⟹ genuine witness、すなわち CNF が"ゴミ"を SAT と誤答しないこと)は別監査であり、`search/sat/check_model_n21.mjs`(独立実装・encoder 非 import)が担当する。CNF#2 は UNSAT なので soundness 方向はこの run では直接は問題にならないが、CNF#1(class, SAT)の model については `search/sat/runs/n21_class/model_vlines.txt` を `check_model_n21.mjs --mode class` で再照合済み(§5 参照・全 check `ok:true`)。

---

## 5. CI artifact との突合(裁定 214 工程 4 実施分)

- `search/sat/runs/n21_class/`(run 30454823288)・`search/sat/runs/n21_transitive/`(run 30454826413)を `gh run download` で収蔵。CNF の SHA-256 は `search/sat/manifest_tail8_n21.json` の値と一致(§ RUNS_LEDGER.md 参照)。
- `node search/sat/check_model_n21.mjs --mode class --model search/sat/runs/n21_class/model_vlines.txt` → `ok:true`(class SAT witness の独立再照合)。
- `search/sat/lrat_check.py`(本便で新規実装、drat-trim 非 import の独立 LRAT checker)を `search/sat/runs/n21_transitive/proof.lrat.gz` に対して実行 → `s VERIFIED`(33626 行、3.3 秒、`search/sat/runs/RUNS_LEDGER.md` に機械出力を記録)。drat-trim 自身の `drat_verify.txt`(`s VERIFIED`)と**独立実装で一致**——ここまでで「cross-checked」と呼べる(「検証済み」ではない、§0 参照)。

---

## 6. 未実施(残務)

- 数学者による本補題の独立監査(F85-8.2 は Sol 供給のまま、本工房内での再導出は未実施)。
- soundness 方向の CNF#2(transitive)側の一般化された紙上証明(class 側 model は照合済みだが、transitive UNSAT の"もし SAT だったら"に対応する soundness チェックは該当なし——UNSAT なので model 自体が存在しない)。
- Lean 化(CLAUDE.md の語法規約により「検証済み」を名乗るための必須工程、未着手)。
