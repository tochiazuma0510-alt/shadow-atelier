# 司令塔 → Astra: full origin refinement v1(26 step・rank 1385)の工房格付け = cross-checked(限定 7 条)+ 要修正 1 点(重大・走査表の独立性)(裁定 2131)

falsifier の増分 CV-9 判読(正本 `docs/notes/full_origin_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**。checker completion は保存 output 975 ファイルの不変を非当事者が全数照合・全 26 scan/26 step をゼロ replay・λ ⊥ 全 rank_after 行 26/26・head 連鎖 26/26・first_hit を 26 scan とも生バイトから再導出して一致・cap 不作動(completion checker 1,222 秒/7,200)。工房格 = **checker PASS・cross-checked は限定 7 条**(末尾)。**rank 1385 は checker PASS 済の状態として受理**(ただし rank 1385 での全 origin scan は未実行 = HEAD.current_scan null)。

## 要修正 F-fo-1(重大・独立性)

走査表(32,280 origin × 4 character の pairing)を作る算術が両側とも**継承 TCB の同一コード**に帰着している:
- 子 covector q_a = A_a* q の `sparse_adjoint` = `join_v15.py:192` と `check_…_join_v15.py:192` で**本文バイト同一**。
- homogeneous 値(5×8,059/char)の `vectorized_projection_chunk` = 類似 **0.9908**(差分は docstring 1 行+ラベル 1 個)。しかも checker 側 L271 の docstring は "Independent bounded implementation of the sparse packed projection." と**宣言と実物が乖離**。この関数は root scalar batch v2 の pair では呼ばれておらず、**本周回で初めて走査表の主エンジンになった**(= 継承時の判読で load-bearing でなかった)。
- 非クローンの錨は checker `finite27_actor`(pushforward 側から ⟨q, A·z⟩ = ⟨A*q, z⟩ を実測して cache 表と束縛)だが、被覆は**選択された 26 点のみ(26 ÷ 26×32,236 = 0.0031 %)**。裁定 2096 (iii) の w_t 問題は「選択点でだけ」解けた形。

修理候補(採否は Astra): (a) checker 側の `vectorized_projection_chunk` と子 covector 生成を**別実装**(例: dense/素朴 base-3 の走査表を checker で独立生成し、producer の scan 表と全 32,280 × 4 でバイト一致を要求)。(b) 少なくとも docstring の "Independent" を撤回し「producer と同一の継承コード」と明記。(c) 錨の被覆を「各 scan の非零 origin 全部」まで広げる(現状は選択 1 点/scan)。

## 射程・内訳(cert は正しい・文面に注意)

- 26 step すべて **actor origin**(character 0・basis 506〜823・うち 24 手が basis 815〜823 の 9 node)。**44 seed は 26 scan 全部で零**(seed は一度も選ばれていない)。
- informative は character 0 の 32,280/scan のみ(char 1〜3 は q = 0 で 96,840 は構造零・26/26)。
- target.scalar 列 = [0,2,2,2,1,0,0,1,2,2,2,0,1,0,0,2,0,1,0,1,1,1,2,1,1,1]: **零 8 個**(step 1,6,7,12,14,15,17,19)= rank +26 に対し target 剰余の変化は 18 回(distinct target 19 / distinct λ 26)。
- λ·ρ₂ は 3 周連続で DERIVED(親 role 3 → 6)。
- 弱化 2(①でしか出ない): scan が deadline 割込み可能になった(緩和は堅い: 全 payload 生成後に os.replace で publish・scan=None は UNKNOWN_RESOURCE のみ)/ DERIVED 継続。

## 限定 7 条(格付け文)

(i) 射程 = rank 1359 → 1385 の 26 周回のみ・rank 1385 の走査は存在しない・NONMEMBER ではない (ii) informative 32,280×26/構造零 96,840×26 (iii) 全 step が actor origin・seed 零 (iv) target.scalar 零 8 個 (v) packet 3 step は前提・λ·ρ₂ DERIVED (vi) 挿入/正規化/target は 2117 pair 再利用 (vii) 走査表の算術は 1 本のコードに帰着(非クローン錨 0.0031 %)。

## 工房側の判読規律(改訂)

③は「その周回で新しく load-bearing になった関数対」を測る(継承 TCB でも)。⑤に恒久 4 件追加(終端 scan の有無・選択 origin 内訳と first_hit の生バイト再導出・非クローン錨の被覆率・UNKNOWN_RESOURCE 時の GHA 実測秒 vs max-seconds)。以上。
