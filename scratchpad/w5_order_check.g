#############################################################################
## scratchpad/w5_order_check.g
## 検算1点(30分級・司令塔小委嘱): 発案札2-D[W5-AUDIT]の即時上申を検算する。
##
## 対象: docs/notes/k5_genuine_campaign_v1.md SS3.7 W-5行 = N := K^(5) cap N_Q
##   (N_Q = ker(psi_Q: PB3 -> Q8), x->i, y->j, c->1; docs/notes/ideas_020_w6_target.md
##    付録A SS0規約と同一)。
## 上申: campaign記載の |PB3/N|=4000 は分裂上限(=full direct product |G5|*|Q8|)であり、
##   G5とQ8が共通のC2^2商(x,yのmod-2類)を共有するため実際は 1000 (=|G5|*|Q8|/4) の疑い。
##
## 方法: search/week3-battery-1b.g の M_Q=K^(3) cap N_Q 構成をそのまま流用し、
##   K^(3)をK^(5)に差し替える(MakeGn(5)・15点、MakeQ8()・8点、直和埋め込みで23点)。
##   MakeGn/MakeQ8 は search/week3-battery-common.g の既存共有ヘルパー(改造禁止・逐語再利用)。
## 独立性: certificates/*.json は一切読まない。PB3/K^(5)・PB3/N_Q ともGAPで生成器から新規構築。
## 規律: gap.ps1経由・-o 2g。乗算規約AbstractProd(本スクリプトは素の群位数計算のみで
##   AbstractProd自体は不要 -- 単語評価もhexagon走査もしない)。cert不要・生出力のみ。
## 宇宙の事前登録: 対象は (K^(5), N_Q) の1対・窓Nのみ。封印非接触・Im R非接触・hexagon走査なし。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/week3-battery-common.g");;

Print("=== W5-AUDIT: N := K^(5) cap N_Q の直接検算 ===\n");

# ---- G5 = PB3/K^(5) (MakeGn(5), 逐語再利用) ----
gn5 := MakeGn(5);;
g5Size := Size(gn5.G);;
Print("|G5| = |PB3/K^(5)| = ", g5Size, "  (campaign boxed formula: expect 500)\n");
g5ord := Lcm(Order(gn5.x), Order(gn5.y));;
Print("K^(5)_ord (established convention: Lcm(Order(x),Order(y))) = ", g5ord,
      "  (campaign boxed formula: expect 10)\n");

# ---- Q8 = PB3/N_Q (MakeQ8, 逐語再利用: x->i, y->j, c->1) ----
q8rec := MakeQ8();;
q8Size := Size(q8rec.G);;
Print("|Q8| = |PB3/N_Q| = ", q8Size, "  (expect 8)\n");

# ---- fiber-product embedding on 15+8=23 points (week3-battery-1b.g のパターンを逐語流用) ----
xhat := PermList(Concatenation(List([1..15], j -> j^gn5.x), List([1..8], j -> 15 + (j^q8rec.x))));;
yhat := PermList(Concatenation(List([1..15], j -> j^gn5.y), List([1..8], j -> 15 + (j^q8rec.y))));;

QW5 := Group(xhat, yhat);;
qw5Size := Size(QW5);;
Print("\n|PB3/N| = |Group(xhat,yhat)| = ", qw5Size,
      "  (campaign W-5 行: 4000 / 札2-D上申: 1000 / 直積上限: ", g5Size*q8Size, ")\n");

nOrd := Lcm(Order(xhat), Order(yhat));;
Print("N_ord = Lcm(Order(xhat),Order(yhat)) = ", nOrd, "  (campaign W-5 行: expect 40)\n");

# ---- 直積上限との比較 ----
directProductBound := g5Size * q8Size;;
Print("\nfull direct product bound |G5|*|Q8| = ", directProductBound, "\n");
Print("観測 |PB3/N| / direct product bound = ", qw5Size, "/", directProductBound,
      " = ", qw5Size/directProductBound, "\n");

# ---- 機構説明の真偽: G5とQ8が共通C2^2商を共有するか ----
Print("\n=== 機構説明の検算: G5側とQ8側のC2^2商の一致 ===\n");
DG5 := DerivedSubgroup(gn5.G);;
dg5Size := Size(DG5);;
g5abSize := g5Size / dg5Size;;
Print("|[G5,G5]| = ", dg5Size, "   |G5^ab| = |G5|/|[G5,G5]| = ", g5abSize, "\n");

DQ8 := DerivedSubgroup(q8rec.G);;
dq8Size := Size(DQ8);;
q8abSize := q8Size / dq8Size;;
Print("|[Q8,Q8]| = ", dq8Size, "   |Q8^ab| = |Q8|/|[Q8,Q8]| = ", q8abSize, "\n");

# ---- projection homomorphisms QW5 -> G5, QW5 -> Q8 ----
projG5 := GroupHomomorphismByImages(QW5, gn5.G, [xhat,yhat], [gn5.x, gn5.y]);;
projQ8 := GroupHomomorphismByImages(QW5, q8rec.G, [xhat,yhat], [q8rec.x, q8rec.y]);;
if projG5 = fail or projQ8 = fail then
  Error("w5_order_check: projection homomorphism construction failed -- refusing to proceed");
fi;
Print("[", PF(Size(Image(projG5)) = g5Size), "] projG5 surjective onto G5 (|Image|=", Size(Image(projG5)), ")\n");
Print("[", PF(Size(Image(projQ8)) = q8Size), "] projQ8 surjective onto Q8 (|Image|=", Size(Image(projQ8)), ")\n");

# ---- K^(5)の像(ker projG5)をQ8側へ射影 -- 付録A手順2の直接検算 ----
kerK5inQW5 := Kernel(projG5);;
kerK5size := Size(kerK5inQW5);;
Print("\n|Kernel(QW5 -> G5)| (= |N/(N cap ... )| relative, this is K^(5)'s image inside QW5) = ", kerK5size, "\n");
imgK5inQ8 := Image(projQ8, kerK5inQW5);;
imgK5inQ8Size := Size(imgK5inQ8);;
Print("|psi_Q(K^(5))| = |Image(projQ8, Kernel(projG5))| = ", imgK5inQ8Size,
      "  (付録A手順2の予言: expect 2 = {+-1})\n");

# ---- 逆向き: N_Qの像(ker projQ8)をG5側へ射影 ----
kerNQinQW5 := Kernel(projQ8);;
kerNQsize := Size(kerNQinQW5);;
Print("|Kernel(QW5 -> Q8)| (= N_Q's image inside QW5) = ", kerNQsize, "\n");
imgNQinG5 := Image(projG5, kerNQinQW5);;
imgNQinG5Size := Size(imgNQinG5);;
Print("|psi_5(N_Q)| = |Image(projG5, Kernel(projQ8))| = ", imgNQinG5Size, "\n");

# ---- 分裂判定(SPLIT/直積判定への参考データ、命題K5-SPL0の(SPL)条件そのものは判定しない
##      -- ここでは |PB3/N| が |G5|*|Q8| に一致するか否かの直接観測のみ) ----
Print("\n=== 判定 ===\n");
if qw5Size = 4000 then
  Print("*** |PB3/N| = 4000 -- campaign W-5 行と一致。直積(4000)が正しい ***\n");
elif qw5Size = 1000 then
  Print("*** |PB3/N| = 1000 -- 札2-D上申と一致。4000は分裂上限で実際は1000 ***\n");
else
  Print("*** |PB3/N| = ", qw5Size, " -- 4000でも1000でもない第三の値 ***\n");
fi;

Print("\nW5_ORDER_CHECK_DONE\n");
QUIT;
