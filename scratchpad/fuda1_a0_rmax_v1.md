# 札 1 実行報告: A0 occurrence closure の終端 rank 上界 r_max — 数学者 2026-08-31

状態: **candidate 格の見積りメモ**(cert 級ではない)。数値はすべて機械出力
(GAP / python・本文末尾の sha16 つきファイル)からの転記。verified(Lean)や
cross-checked(独立二系統)の主張はしない。

## 0. 判定(結論)

**r_max = 58,569,049,736(≈ 5.86×10^10)** — closure が到達しうる occurrence rank の
証明可能上界(下記仮定 A/B の下)。有限なので「原理的に終わらない構造」ではない。
しかし予算(10^4〜10^5)を 5〜6 桁超過しており、**「予算内 r_max による closure 完走
保証(GO)」は出ない = 札 1 の GO 側シナリオは死亡・NO-GO 側の裁定材料**。

- 完了率: 1,655 / 58,569,049,736 = **2.83×10^-8**
- 実測成長率(rank 3.16/親・Sol 現況 1,655/523 から)で r_max 到達に必要な親処理
  ≈ 1.85×10^10 個 — 1 親/秒でも約 587 年。
- ambient(キー空間全体)= 4.02×10^29。rank 1,316 時点の実測登場キー 4,284,963
  (v12 L30 PARENT_REPAIR_KEYS)は ambient の 1.07×10^-23 — 「キー空間はまだ
  ほぼ手つかず」と整合し、frontier 増加中(906→1,132)とも矛盾しない。

## 1. Step 1: 構造の同定(Sol コードの読み取り・行番号つき)

### 1.1 行のキー空間

正本: search/d972_r07_a0_pb34_direct_quotient_owner_v12.py(以下 v12)と
その pin 先 …_v3.py(以下 v3)・d972_r07_positive_common_word_colgen_v1.py
(AllSevenModel)・d972_b345_seedspan_triple4_v1.py(群の実体)。

- キー = `b"N"+i`(指数和 2 個)または `b"O"+ordinal+qkey`。
  qkey = `b"Q"+block+len+label+b":"+blob`(v3 L110-111 qkey / L102-103 parse)。
- ordinal = **11 occurrence**(AllSevenModel L637-666: raw_specs = E3 型 6 個
  〔H1_fxy, H1_fxz, H1_fyz, H2_fux, H2_fxy, H2_fuy・block 1,2〕+ E4 型 5 個
  〔P_b1, P_b2, P_b3, P_b5_inverse, P_b4_inverse・block 3〕)。
  docstring「Eleven literal Fox occurrences」。
- label: block<3 は {b,c,u0,u1,tau}、block=3 は {b,c,p,q,r,u0,u1,tau}
  (v12 contract L150-173)。tau は blob なしの 1 キー/block。
- blob = 群元の transversal 代表のエンコード(中心 z による coset 代表・
  h0 が z^j を分離: v12 L142-148)。係数は mod 3。

### 1.2 群の実体(e3/e4)

d972_b345_seedspan_triple4_v1.py L2529-2553 reconstruct_quotients:
- e3 = MatchedQuotient: **(Q0 perm 群 deg 36)×(pc3)の部分群**、
  生成元 3 対 (q0[a12],u1),(q0z,u2),(q0[a23],u3)。
- e4 = 同 **(Q4 perm 群 deg 144)×(pc4)**、生成元 6 対(a12,a13,a14,a23,a24,a34)。
- pc3/pc4 = PB3/PB4 の class-2・exponent-3 pc 商(q3_chief receipt:
  order_decimal 81 / 59049・全相対位数 3・power 関係自明)。

GAP 実測(§3): **どちらも fibre = pc 全体、すなわち e3 = Q0×pc3・e4 = Q4×pc4 の
全直積**。
- |e3| = 119,042,784(= 1,469,664×81・Q0 = 2^5·3^8·7)
- |e4| = 34,434,579,550,012,856,658,927,157,248 ≈ 3.44×10^28
  (Q4 = 2^17·3^32·7^4 = 5.83×10^23、×3^10)

### 1.3 生成規則(「親を開く」)= 固定群元の左 translation

v12 の queue ループ(L474-479): 親 pivot p に対し letter ∈ {1,-1,2,-2} で
`actor_v12` を適用し echelon に add(CONJUGATE family)。

actor_v12(v12 L237-254)は occurrence o のキーに対し
```
aa=g.eval(model._substitute([letter],spec["left"],spec["right"],spec["lift"]))
p=spec["occurrence_prefix"];cache[ck]=g.mul(p,g.mul(aa,g.inverse(p)))    # L247
...  g.mul(cache[ck],val)                                                # L248
```
すなわち **t_{o,l} = prefix_o·φ_o(l)·prefix_o^{-1} による blob 群元への左掛け**
+ normal_section / contract(商正規化)。N キーは素通し(L240-243)。

φ_o(1)=eval(left_o), φ_o(2)=eval(right_o), φ_o(-l)=φ_o(l)^{-1}。よって
occurrence o の translation 群は(prefix 共役を除き)
**T_o = ⟨eval(left_o), eval(right_o)⟩ ≤ G_o(= e3 or e4)**。

E3 側 6 occurrence の (left,right) は F2 語 (x,y),(x,z),(y,z),(u,x),(x,y),(u,y)
(z=(pp[x,y])^{-1}, u=(pp[y,x])^{-1}・AllSevenModel L643-657)を
embed_f2_pb3(1↦a12, 2↦a23・seedspan L914-916)で送ったもの — 6 つとも
群としては **同一の T3 = ⟨ā12, ā23⟩**(z,u が両生成元の語のため生成系変換で一致)。
E4 側 5 occurrence は PB4 marked 生成元の語ペア(pcontexts L646-649):
P_b1=⟨ā23,ā34⟩, P_b2=⟨ā13ā12, ā34ā24⟩, P_b3=⟨ā12,ā23⟩,
P_b5_inv=⟨ā23ā13, ā34⟩, P_b4_inv=⟨ā12, ā24ā23⟩。

### 1.4 44 seed の実体

pres["relators"] の 44 本(v3 L284: compact_relator_count==44・roster sha pin
7612682d…)。v12 seed ループ L463-467(LEAF family・seed_v12)。
44 の出所 = compact_pc_invariant_owner_v1(Γ の index-3 PC chain の Tietze 置換
relator 系・同ファイル docstring)。seed は N1/N2(指数和/18)も供給(v12 L263-265)。

## 2. 上界の導出

### 2.1 仮定(全部明示)

- **仮定 A(加群構造)**: actor_v12 は各 occurrence 成分上で「左 translation の
  商表現」ρ_o: G_o → GL(Q_block) を実現しており、合成が群の積に対応する
  (A_l∘A_{l'} = ρ(t_l·t_{l'}))。根拠 = コード構造: 作用は blob 群元への
  **左掛け**(L248)、contract の正規化は **右掛け**(gens[c]・z を右から:
  L161 `g.mul(g.mul(h0,pw[j]),gens[c])`)および中心 z の分離であり、
  左掛けと右掛け/中心操作は可換 — よって contract が定める商(核)は
  左 translation 不変。**コードの逐行の数学的検証はしていない**(candidate 格の
  読み取り)。この仮定の下で closure V の o 成分は F_3[T_o]-部分加群。
- **仮定 B(キー空間の形)**: blob は z-coset transversal 代表で、block b の
  キー総数 = (labels 数)×|G_b|/3 + 1(tau)。z3/z4 の位数 3 は GAP で確認済
  (perm 部分恒等・pc 部分位数 3・central=true)。
- **仮定 C(供給系)**: occurrence phase の行供給は LEAF(44 seed)と
  CONJUGATE(4 letter actor)のみ(v12 L463-479 で確認・six_action は
  physical 帳簿で occurrence rank に入らない)。
- 実行環境側の前提: Sol 報告値(rank 1,655・親 523・frontier 1,132・
  rank≤1,316 に正解なし)は研究者経由 2026-08-31 の伝聞値。

### 2.2 上界式

V ⊆ F_3² (N) ⊕ ⊕_{o=1..11} M_o、M_o = Σ_{i=1..44} F_3[T_o]·(seed_i の o 成分)。

- cyclic 上界: dim F_3[T]·v ≤ |T|(正則加群)。
- ambient 上界: dim M_o ≤ dim Q_block(o)。

r_max = 2 + Σ_o min(dim Q_block(o), 44·|T_o|)
- dim Q_{1,2} = 4·(|e3|/3)+1 = 158,723,713(E3 側 6 occurrence 共通)
- dim Q_3 = 7·(|e4|/3)+1 ≈ 8.03×10^28(E4 側 5 occurrence 共通)
- E3 側: 44·|T3| = 44×39,680,928 = 1,745,960,832 > dim Q_{1,2} → cap 発動、
  各 158,723,713
- E4 側: 44·|T_o| ≪ dim Q_3 → 44×357,128,352 ×3 本・44×119,042,784 ×2 本

**r_max = 2 + 6×158,723,713 + 3×15,713,647,488 + 2×5,237,882,496
= 58,569,049,736**

(physical/six_action 帳簿の rank も untag 集約が線形なので同オーダーの上界に
収まる — six_action 供給行も e4-translation orbit 内・別勘定だが桁は不変。)

## 3. GAP 計算の要点(機械出力)

- データ生成: fuda1_gen_gapdata.py が q3_chief_v1.json(sha256 = pin
  3d37c8c5f1fae47c… 一致確認済)から perm one-line・pc conjugate 表を
  機械変換(marked 生成元が単位ベクトルであることも assert)。
- v1(fuda1_a0_rmax_v1.g): fp 化 fibre 法。e3 は完了(fibre 81)、e4 の
  IsomorphismFpGroupByGenerators が |Q4|=5.8×10^23 で停止せず → kill(教訓)。
- v2(…_v2.g): e4 を [proj, proj×3^10] で挟み込み。r_max ∈ [1.7×10^10, 10^15]。
- v3(…_v3.g・確定版): pc3/pc4 を IsomorphismPermGroup(deg 12/39)で置換群化し
  DirectProduct 内で Schreier-Sims — 全て正確値。走行 ≈ 数十秒。
  - e3 = 119,042,784(fibre 81)・e4 = 3.44×10^28(fibre 59,049)
  - T3 = 39,680,928 = |e3|/3
  - T4: P_b1/b2/b3 = 357,128,352(= 3×|e3|・strands{2,3,4} の PB3 コピー像として
    自然)、P_b5_inv/b4_inv = 119,042,784
  - r_max_exact = 58,569,049,736
- 派生量(python 検算・fuda1 派生計算): e4 = Q4×pc4 の直積等式 assert PASS・
  完了率 2.826×10^-8・親所要 1.851×10^10。

## 4. 「closure 路線は終わるのか」への含意

1. **終わる(有限)が、予算内完走の保証は出ない。** 証明可能上界 5.86×10^10 は
   GHA 予算の 5〜6 桁上。完走保証を回復するには「V の真の次元が小さい」ことを
   別の構造(seed stabilizer の巨大性・不変 filtration)で示す必要があるが、
   その材料は現状ない(UNKNOWN)。
2. 実測傍証も飽和と逆向き: frontier 906(rank 1,316)→ 1,132(rank 1,655)増加中・
   登場キーは ambient の 10^-23。
3. よって「rank を伸ばして positive probe の命中を待つ」は上界の保護がない賭け。
   **完走なしで結論を出す路線(札 3 深さ障壁 negative・札 4 商の階段・札 6
   dual 番人)の相対優先度が上がる**、が本計算の運用的含意。
4. 逆に、本計算の副産物は positive 側にも使える: T_o と orbit 構造が確定したので
   札 7(target 側 cyclic module)の費用見積り(≤|T_o| ≈ 3.6×10^8 — これも重い)
   が即座に出る。

## 5. Sol への確認 1 問(送るかは司令塔判断)

「44 seed の occurrence 成分の T_o-stabilizer(または生成 cyclic 加群の次元)を
|T_o| より桁で小さくする構造(不変 filtration・stabilizer の下界)を現行設計で
把握しているか。なければ occurrence closure の終端 rank は上界 5.86×10^10 の
下で無保証となる — 完走前提の計画(probe の rank 面選択)に影響するか。」

## 6. 破れの正直な申告

- 仮定 A はコード読み(左掛け/右正規化の可換性)による。contract の 12 規則
  レベルの逐行検証はしていない —【GAP: A の厳密証明は未実施・falsifier/Sol の
  照合で閉じられる形】。ただし仮定 A が破れる場合、上界は「軌道が群作用で
  閉じない」方向に**緩む**のではなく生成規則自体が translation でなくなる方向で、
  その場合も ambient 上界 4.02×10^29 は残る(判定の向きは不変)。
- 44 seed の行そのもの(supp)は計算していない(runtime 一式のロードが必要)。
  そのため orbit-support による r_max の精密化(重なり・stabilizer)は未実施。
  上界としての正しさには影響しない。
- Sol 報告値(1,655/523/1,132)は伝聞。完了率等の分母 r_max は本計算値。

## 7. 成果物(すべて scratchpad/・sha16)

- fuda1_gen_gapdata.py 5c250549cc092189(データ機械変換)
- fuda1_a0_rmax_data.g 625b4d11ca882c94(GAP 入力・q3 receipt 由来)
- fuda1_a0_rmax_v1.g 06c6d80d193a5aad / v1 出力 96e1fb0ee3b33e45(e3 確定・e4 fp 中断)
- fuda1_a0_rmax_v2.g 2ee298287f117cf7 / v2 出力 81b7e30491933ec6(挟み込み版)
- fuda1_a0_rmax_v3.g 0e8ff22fbff1fd75 / v3 出力 ca94a5e1c47f4f62(**確定値**)
- 本メモ fuda1_a0_rmax_v1.md
