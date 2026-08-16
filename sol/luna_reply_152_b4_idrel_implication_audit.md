# B4 direct IdRel receipt から何が従うか：含意監査

## 0. 範囲と仮定

ここでは、direct receipt が実際に

```text
U = F_6 / <<158 relators>>
```

における 972 個（486 個の unique row と完全な duplicate map）の exact `rho`-norm を全て恒等元にした、という仮定だけを置く。このファイルは receipt の成立を主張するものではない。GAP の再実行、重い計算、既存 lane の変更はしていない。

結論を先に言うと、`H_norm`（972 norm の恒等性）単独から得られるのは、固定された自由群表示における有限な norm/pentagon 候補の証明書までである。PB4 に型付けした有限 pentagon の帰結にするには別の presentation/word bridge が必要であり、B4 genuine、cofinal lift、まして非算術的 genuine shadow や Ihara の非全射性は従わない。

## 1. 2008 年の型を固定する

2008 論文の Definition 2.6 は、`N ∈ NFI_{PB4}(B4)` に対する GT-pair を、(2.18), (2.19) の二つの hexagon と (2.20) の pentagon を満たす `(m,f)` と定義する（`papers/txt/2008.00066-what-are-gt-shadows.txt:925-933`、印刷 p.13）。その後の Corollary 2.7 は、この pair から B2, B3, B4、特に PB2, PB3, PB4 の準同型を得ることを記している（同 `:936-952`）。従って、`f` の一つの関係を消しただけでは GT-pair でも GT-shadow でもない。

Definition 2.19（印刷 p.25、`papers/txt/2008.00066-what-are-gt-shadows.txt:2009-2025`）は、まず `[(m,f)] ∈ GT(N)` を仮定した上で、genuine を「`Aut(\widehat{PaB})` から来る」と定義する。fake はその否定である。同じ定義の charming 条件は、`f N_{PB3}` が `[F_2,F_2]` の代表を持ち、かつ `T^{F2}_{m,f}` が onto であることに過ぎない。したがって

```text
genuine  ⇒ charming、しかし charming ⇒ genuine は未確定
```

であり、`charming` を genuine の同義語にしてはいけない。

さらに Corollary 3.13（印刷 p.38、`papers/txt/2008.00066-what-are-gt-shadows.txt:3022-3029`）は、`[(m,f)] ∈ GT^♥(N)` について

```text
genuine ⇔ every K ∈ NFI_{PB4}(B4) with K ≤ N に survive
```

とする。survive とは、ある `(m1,f1) ∈ GT^♥(K)` が存在して、`m1 ≡ m (mod N_ord)` かつ `f1 N_F2 = f N_F2` となること（同 `:3022-3025`）である。一つの `K` への lift や、元の `N` での一つの計算は、この全称量化を置き換えない。

なお、pentagon から hexagon への有限版の自動性も仮定ではない。2008 年の Property 4.2/4.3 は、その性質を持つ `N` について初めて「pentagon を満たす `f` に適切な `m` が存在し、二つの hexagon も満たす」と要求する（同 `:3507-3516`）。実例では `N^(19)` の pentagon 解 216 個のうち hexagon まで lift するのは 36 個だけ、`N^(34)` では 4096 個のうち 243 個だけである（同 `:3524-3546`）。従って norm=1 の列を hexagon や `m` の存在へ読み替えることはできない。

## 2. direct receipt が実際に固定しているもの

`search/d972_b4_u_idrel_direct_logged_v1.g` 自身の契約は、固定六生成元・158 relator の `U` に対する bounded IdRel lane である（同 `:4-19`）。各 row について producer は自由群内の

```text
product(rel_i^conjugator) * reduced = original norm
```

を確認し、Python checker も同じ等式を再生する。同スクリプトは、非恒等 reduced word を A witness としないこと、全 486 unique row と 972-row duplicate map が恒等のときだけ terminal を出すことを明記している（同 `:9-19`, `:514-515`）。最終 receipt の `proof_level` も `F6_FREE_GROUP_LOG_REPLAY_CANDIDATE` である（同 `:530-540`）。これは証明書の射程を自ら限定している。

norm の構成も PB4 の全ての refinement を列挙するものではない。`D972IDLExactNorm` は F2 の文字 1,2 を六生成元の 1,4 に写し、`rho` の五つの orbit を作り、逆順に連結する（同 `:154-169`）。入力の 972 roof word から 972 個のこの特定の cyclic norm を作り、486 個へ重複除去している（同 `:244-260`）。一方、固定表示 `U` の構成は `FreeGroup(6)` と 158 relator の quotient である（同 `:262-268`）。そこには、

* `U` がどの `PB4/N` と同じ quotient か、
* 六生成元がどの `x_{ij}` か、
* `rho` が PB4 の Hurwitz/cyclic map と一致するか、
* 各 roof row が 2008 の (2.20) のどの `f` の評価か、
* `K ≤ N` のどの refinement と reduction map を表すか

を型付けするフィールドはない。

## 3. 含意グラフ

以下で `H_norm` は上記 receipt の全 972 norm 恒等性、`H_bridge` は PB4 への正確な型付けを意味する。

### (a) `H_norm` のみ

確実に従うのは

```text
各 selected norm n_i ∈ <<r_1,…,r_158>> ⊂ F_6
```

という有限自由群の normal-closure certificate だけである。これは選ばれた row の関係であって、PB4 の定義関係、finite quotient の kernel、GT-shadow の operad morphism をまだ主張しない。

### (b) `H_norm + H_bridge + H_roof`

次の三つを独立に証明できるなら、初めて「typed finite B4 pentagon consequence」と呼べる。

1. `U` の six-generator presentation が、ある `N ∈ NFI_{PB4}(B4)` に対する `PB4/N`（または明示的なその quotient）と正確に同定され、generator map と全 relator の soundness/completeness がある。
2. `rho` と五つの substitution が PB4 の `A.18` の対応と一致する。
3. 972 roof rows が、主張したい candidate の全 pentagon defect を漏れなく表す。

repo の B4 note は、`S_0=[P,P]` では (2.20) と `Dtilde=1`、`S_1` では (2.20) と `PENT_W` の同値を分けている（`docs/notes/b4_direct_adjudication_feasibility_v1_2.md:145-159`）。同 note の `PENT_W` は五項 `f_5 f_4 f_3 f_2 f_1` の defect として書かれている（同 `:117-120`）。従って `H_bridge` があれば、receipt は「その candidate/その window の pentagon defect が消える」という有限 B4 関係の帰結になり得る。しかしこれはまだ GT-pair ではない。

### (c) 有限 B4 GT-pair / GT-shadow

さらに次を要する。

* `N ∈ NFI_{PB4}(B4)`、有限指数、及び `N_{PB3},N_{PB2}` を伴う正確な対象の同定。
* `m` と `f` の candidate の同定、`2m+1` が `Z/N_ord` の unit であること。
* 二つの hexagon (2.18),(2.19) の独立な検証。pentagon receipt からは出ない。
* 2008 の `T^{PB2},T^{PB3},T^{PB4}` が well-defined かつ onto であること。これが GT-shadow の onto 条件である（2008 定義の repo 抽出 `docs/notes/b4_original_gtshadows_extraction_v1.md:26-43`、特に同 `:41-43`）。
* 2008 の B4 charming を使うなら、Definition 2.19 の `[F2,F2]` representative と `T^{F2}` onto も確認する（同 `:48-52`）。

以上が揃えば「有限 B4 GT-shadow」、さらに `[F2,F2]` 条件までなら「有限 B4 charming shadow」と言える。`H_norm` だけでここまで進めることはできない。

### (d) B4 genuine / cofinal lift

genuine には、candidate がまず `GT^♥(N)` に属し、Cor. 3.13 の全ての `K≤N` について上記の同じ residue class が survive することが必要かつ十分である。isolated quotient が cofinal であることは 2008 の構造（repo 抽出 `docs/notes/b4_original_gtshadows_extraction_v1.md:68-72`）だが、Prop. 3.9 の cofinality は refinement の存在定理であり、今回の 158 relator presentation に対する lift recipe ではない（`docs/notes/b4_direct_adjudication_feasibility_v1_2.md:56-58`）。

したがって必要な追加物は、少なくとも次のいずれかである。

* 全ての relevant `K≤N` を型付けし、各 K で `GT^♥(K)` の lift と congruence を certificate 化して、Cor. 3.13 の全称を閉じる。
* あるいは、独立の cofinal-lift theorem により、この有限 receipt が全 isolated system へ一貫して延長することを証明する。

元の `N` 又は一つの isolated `K` での norm=1、さらには一つの successful survival は、genuine を意味しない。repo もこの点を明示しており、Cor. 3.13 の survival 判定は現在 UNKNOWN と記載されている（`docs/notes/b4_direct_adjudication_feasibility_v1_2.md:185-189,319-329`）。

## 4. 「972 norm が全 PB4 refinement を encode しているか」の敵対的検査

答えは **否** である。

`H_norm` の添字は固定された 972 roof row と 486 unique norm にしか及ばず、`K`、`N`、reduction、`(m_1,f_1)`、及び residue congruence を添字に持たない。`K` を小さくすると quotient の同値関係と candidate の lift 条件が変わるため、同じ F6 word の恒等性を全 K の survival と同一視できない。norm family が encode しているのは、`rho` の五周期を使った選択された pentagon defect（bridge 後には選択された (2.20)/`PENT_W`）だけである。

さらに固定 N の中でも pentagon-only と full B4 は別である。2008 の 216→36、4096→243 の実験値は、pentagon rows を全て恒等にしても `m` と hexagon の lift が自動で付かないことを直接示す（`papers/txt/2008.00066-what-are-gt-shadows.txt:3507-3516,3524-3546`）。repo の比較表も、2008 B4 は「hexagon 2 本 + pentagon」、2401 の B3-gentle 側は pentagon を外した系として区別している（`docs/notes/b4_direct_adjudication_feasibility_v1_2.md:19-25,242-252`）。

従って、全 972 norm が恒等でも、結論の上限は

```text
固定 U 内の selected pentagon/norm certificate
→（PB4 presentation と rho/roof bridge があれば）typed finite pentagon consequence
```

であり、全 PB4 refinement の cofinal lift ではない。

## 5. 「genuine nonarithmetical」と Ihara 非全射性までに必要なもの

これは B4 genuine よりさらに別の層である。必要条件を分解すると次の通り。

1. 上記 (a)--(d) を満たす、対象が本当に `\widehat{GT}=Aut(\widehat{PaB})` から来る B4 genuine shadow であること。`GT_gen`/B3-gentle の element だけでは足りない。repo の対応表も 2008 の B4 と 2401 の gentle を別の court としている（`docs/notes/b4_direct_adjudication_feasibility_v1_2.md:19,245`）。
2. 同じ finite quotient における arithmetic image、すなわち Ihara の `G_Q`（またはその指定された有限像）の写像を定義し、candidate の像との compatibility を証明する。単なる shadow の個数や norm defect では arithmetic/nonarithmetic を判定できない。
3. candidate がその arithmetic image の外にあることを、独立な不変量、完全な有限像の計数、又は算術的 orbit の分離で証明する。
4. その finite separation が profinite の Ihara 写像 `G_Q → \widehat{GT}` の非全射性へ反映する、という target/map compatibility を明記する。

fake charming shadow はこの目的の candidate にはならない。fake はそもそも `Aut(\widehat{PaB})` から来ないため、非算術的な genuine element ではない。一方、もし `GT_gen` のみに属する fake/non-lift を得たとしても、それは（追加の比較定理があれば）`\widehat{GT}→\widehat{GT}_{gen}` の非全射性を示す方向の情報であって、直ちに `G_Q→\widehat{GT}` の非全射性ではない。Galois/Ihara の位置付けは `docs/notes/b4_original_gtshadows_extraction_v1.md:74-76` に整理されている。

## 最終判定

`H_norm` を仮定しても、現時点で安全に言えるのは「固定 F6/158 quotient における 972 selected `rho`-norm の free-group log certificate」である。PB4 presentation/`rho`/roof の完全な bridge を追加できれば、そこから **有限・型付き B4 の selected pentagon consequence** までは進める余地がある。しかし、hexagon、onto、charming、全 isolated refinement の survival（2008 Cor. 3.13）、genuine、算術像からの分離、Ihara 非全射性は、それぞれ別の仮定または証明書を要する。

従って、この receipt だけを「B4 genuine/cofinal lift」や「genuine nonarithmetical shadow」と読むのは不許可であり、結論はその段階では UNKNOWN である。
