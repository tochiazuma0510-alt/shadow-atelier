# search/sg_gap1_v1.g -- [SG-GAP-1] C_Q(ybar) の同定 + [0,f] shadow 判定(裁定1067)
#
# 正本: docs/notes/settled_grp_proof_v1.md §5.1/§7。
# 問い: f_bar in C_Q(ybar)\{1} (Q=SL(2,Z/691^2)) で [0,f] が shadow(hexagon通過)になり
#   得るか。C_Q(ybar)は標準構造(ybarが正則なら巡回、SL2の分裂/非分裂torus)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/probe/wac_v1/gap_output_prelude.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

p := 691;;
p2 := p^2;;
Zp2 := Integers mod p2;;

# ---- reconstruct sigma1, sigma2, xbar, ybar as in q3_r1_lift_v1.g ----
ahat := [[483,28],[59,208]] * One(Zp2);;
bhat := [[245,158],[69,445]] * One(Zp2);;
DetMod := function(M) return M[1][1]*M[2][2] - M[1][2]*M[2][1];; end;;
detA := DetMod(ahat);;  detB := DetMod(bhat);;
lamA := -(detA^-1);;  lamB := detB^-1;;
DiagMod := function(d1, d2) return [[d1, Zero(Zp2)], [Zero(Zp2), d2]];; end;;
a0 := DiagMod(lamA, One(Zp2)) * ahat;;
b0 := DiagMod(lamB, One(Zp2)) * bhat;;
atilde := a0^p;;
btilde := b0^p;;
sigma1 := btilde^-1 * atilde;;
sigma2 := atilde * btilde^2;;
xbar := sigma1^2;;
ybar := sigma2^2;;
Print("ybar = ", List(ybar, r -> List(r, Int)), "\n");
Print("(期待 [[144005,26367],[434427,307449]])\n");
ybarOk := (ybar = [[144005,26367],[434427,307449]]*One(Zp2));;
Print("[", PF(ybarOk), "] ybar 再構成一致: ", ybarOk, "\n");
if not ybarOk then Error("sg_gap1_v1: ybar reconstruction mismatch"); fi;

Nord := 47679;;
ordYbar := Order(ybar);;
Print("ord(ybar) = ", ordYbar, " (期待 47679)\n");

# ---- eigenvalue structure of ybar: solve x^2 - tr(ybar) x + 1 = 0 (mod p^2) ----
trY := ybar[1][1] + ybar[2][2];;
Print("trace(ybar) = ", Int(trY), "\n");
discY := trY^2 - 4*One(Zp2);;
Print("discriminant = tr^2-4 = ", Int(discY), "\n");

# check if discY is a square mod p first (Hensel: if sqrt exists mod p and disc is a unit mod p,
# lifts uniquely mod p^2)
Zp := Integers mod p;;
discYmodP := Int(discY) * One(Zp);;
sqrtModP := fail;;
if discYmodP <> Zero(Zp) then
  for cand in Elements(Zp) do
    if cand^2 = discYmodP then sqrtModP := cand; break;; fi;
  od;
fi;
splitCase := (sqrtModP <> fail);;
Print("[", PF(splitCase), "] disc is a nonzero square mod 691 (split torus case): ", splitCase, "\n");

if not splitCase then
  Print("[HALT-STYLE] ybar は非分裂型(または特異)-- 別扱いが必要。詳細解析は本scriptの範囲外として報告。\n");
fi;

# Hensel lift sqrt(discY) from mod p to mod p^2 (since gcd(2*sqrtModP, p) = 1 generically):
# Newton step: s1 = s0 - (s0^2 - discY)/(2*s0) computed mod p^2, s0 = naive lift of sqrtModP
s0 := Int(sqrtModP) * One(Zp2);;
numerator := s0^2 - discY;;
denom := 2*s0;;
s1 := s0 - numerator * denom^-1;;
sqrtCheck := (s1^2 = discY);;
Print("[", PF(sqrtCheck), "] Hensel-lifted sqrt(disc) squares back to disc (mod 691^2): ", sqrtCheck, "\n");
if not sqrtCheck then
  Error("sg_gap1_v1: Hensel lift of sqrt(discriminant) failed -- refusing to proceed");
fi;

# eigenvalues: (trY +- s1)/2
half := (2*One(Zp2))^-1;;
eig1 := (trY + s1) * half;;
eig2 := (trY - s1) * half;;
Print("eigenvalues of ybar: ", Int(eig1), ", ", Int(eig2), "\n");
eigCheck := (eig1*eig2 = One(Zp2)) and (eig1+eig2 = trY);;
Print("[", PF(eigCheck), "] eigenvalues satisfy product=1, sum=trace: ", eigCheck, "\n");

# order of eig1 in (Z/p^2)^x should equal ord(ybar) if ybar is regular semisimple split
ordEig1 := Order(eig1);;
Print("multiplicative order of eig1 = ", ordEig1, " (期待 47679, matching ord(ybar))\n");
ordMatch := (ordEig1 = ordYbar);;
Print("[", PF(ordMatch), "] ord(eig1) == ord(ybar): ", ordMatch, "\n");

# full unit group (Z/p^2)^x order = p(p-1)
unitGroupOrder := p*(p-1);;
Print("|(Z/691^2)^x| = ", unitGroupOrder, " (= split torus order in SL2)\n");
torusIndex := unitGroupOrder / ordYbar;;
Print("index of <ybar> in full split torus = ", torusIndex, "\n");

# ---- is C_Q(ybar) equal to the FULL split torus (order p(p-1)), or just <ybar>? ----
# For a regular (distinct eigenvalues) semisimple element, the centralizer in SL2 IS the full
# maximal torus through it (standard fact) -- verify eig1 <> eig2 (distinct, i.e. regular).
regularCheck := (eig1 <> eig2);;
Print("[", PF(regularCheck), "] eigenvalues distinct (ybar is regular): ", regularCheck, "\n");

Print("\n=> C_Q(ybar) = full split maximal torus through ybar, order ", unitGroupOrder,
      " (standard fact for regular semisimple elements)\n");

# ---- construct the full torus as powers of a generator of (Z/p^2)^x ----
genUnit := PrimitiveRootMod(p2);;
Print("generator of (Z/691^2)^x = ", genUnit, "\n");
genUnitMod := genUnit * One(Zp2);;
genOrderCheck := Order(genUnitMod);;
Print("order of generator = ", genOrderCheck, " (期待 ", unitGroupOrder, ")\n");

# eigenbasis: diagonalizing matrix P such that P^-1 ybar P = diag(eig1,eig2). Since ybar has
# eigenvector for eig1 satisfying (ybar - eig1*I) v = 0.
M1 := ybar - eig1*IdentityMat(2,Zp2);;
# find a nonzero column vector in the "kernel" -- for a 2x2 matrix over Z/p^2 with eig1 as an
# eigenvalue, the first row gives a linear relation; use it directly (works when entries are units)
# M1 = [[a,b],[c,d]] with a*x+b*y=0 => (x,y) = (b,-a) if a<>0 or b<>0 generically
eigVec1 := fail;;
if M1[1][2] <> Zero(Zp2) then
  eigVec1 := [ -M1[1][2], M1[1][1] ];;
elif M1[1][1] <> Zero(Zp2) then
  eigVec1 := [ M1[2][2], -M1[2][1] ];;
else
  eigVec1 := [ One(Zp2), Zero(Zp2) ];;
fi;
checkEigVec1 := (ybar * eigVec1 = eig1 * eigVec1);;
Print("[", PF(checkEigVec1), "] eigenvector for eig1 verified: ", checkEigVec1, "\n");

M2 := ybar - eig2*IdentityMat(2,Zp2);;
eigVec2 := fail;;
if M2[1][2] <> Zero(Zp2) then
  eigVec2 := [ -M2[1][2], M2[1][1] ];;
elif M2[1][1] <> Zero(Zp2) then
  eigVec2 := [ M2[2][2], -M2[2][1] ];;
else
  eigVec2 := [ One(Zp2), Zero(Zp2) ];;
fi;
checkEigVec2 := (ybar * eigVec2 = eig2 * eigVec2);;
Print("[", PF(checkEigVec2), "] eigenvector for eig2 verified: ", checkEigVec2, "\n");

Pmat := TransposedMat([eigVec1, eigVec2]);;
detP := DetMod(Pmat);;
Print("det(P) = ", Int(detP), " (must be a unit mod 691^2 for P invertible)\n");
Pinvertible := (Gcd(Int(detP), p) = 1);;
Print("[", PF(Pinvertible), "] P is invertible (det is a unit mod p): ", Pinvertible, "\n");
if not (checkEigVec1 and checkEigVec2 and Pinvertible) then
  Error("sg_gap1_v1: diagonalization failed -- refusing to proceed to torus enumeration");
fi;
Pinv := Pmat^-1;;

TorusElement := function(t)
  return Pmat * DiagMod(t, t^-1) * Pinv;;
end;;

# sanity: TorusElement(eig1) should equal ybar
sanityYbar := (TorusElement(eig1) = ybar);;
Print("[", PF(sanityYbar), "] TorusElement(eig1) == ybar: ", sanityYbar, "\n");
if not sanityYbar then
  Error("sg_gap1_v1: torus parametrization sanity check failed");
fi;

# ====================================================================
# self-caught 修正(実装中に発見): 最初の版は「well_defined」(settled判定用の後段概念)を
# チェックしていたが、SG-GAP-1が問うのは「[0,f]がshadowになり得るか」(hexagon通過=定義の
# 手前の条件: hex310・hex311・生成)であり、別の概念を混同していた。正しくQ上でtheta/tauを
# 構成し(c-image=1・m=0固定)、実際のhexagon条件(f*theta(f)=1・RtOf(0,f)=c^0=1)を検算する。
#
# theta(g):=DeltaMat*g*DeltaMat^-1 (DeltaMat=atilde=sigma1*sigma2*sigma1)
# tau(g):=delta*g*delta^-1   (delta=sigma2*sigma1、AbstractProd([s1,s2])の規約に対応)
# hex310: f * theta(f) = 1 (Q内の単位元)
# hex311(m=0): tau^2(y^0*f) * tau(y^0*f) * (y^0*f) = c^0 = 1、y^0=I なので y^0*f=f に簡約
#   => tau^2(f)*tau(f)*f = 1
# 生成条件: <xbar^1, f^-1 ybar^1 f> = Q。f in C_Q(ybar) ゆえ f^-1 ybar f = ybar 恒等的 ⟹
#   <xbar,ybar> = Q(紙で確定済み・q3r1_lift_spec_v1 §5)⟹ 生成条件は全fで自動的にPASS。
# ====================================================================
Print("\n============================================================\n");
Print("# [0,f] shadow 判定(正しいhexagon条件・self-caught修正後): f in C_Q(ybar)\\{1}\n");
Print("============================================================\n");

DeltaMat := sigma1 * sigma2 * sigma1;;
deltaSmall := sigma2 * sigma1;;
Print("DeltaMat = sigma1*sigma2*sigma1 == atilde: ", DeltaMat = atilde, "\n");
deltaCubeCheck := (deltaSmall^3 = IdentityMat(2,Zp2));;
Print("[", PF(deltaCubeCheck), "] delta^3 == I (c-image=1 の帰結): ", deltaCubeCheck, "\n");

ThetaFn := function(g) return DeltaMat * g * DeltaMat^-1;; end;;
TauFn := function(g) return deltaSmall * g * deltaSmall^-1;; end;;

IdQ := IdentityMat(2, Zp2);;
HexagonCheckZeroF := function(f)
  local hex310, tauF, tau2F, hex311lhs, hex311;
  hex310 := (f * ThetaFn(f) = IdQ);;
  tauF := TauFn(f);;
  tau2F := TauFn(tauF);;
  hex311lhs := tau2F * tauF * f;;
  hex311 := (hex311lhs = IdQ);;
  return rec(hex310 := hex310, hex311 := hex311, is_shadow := hex310 and hex311);;
end;;

# self-check f=1 (identity, EXCLUDED by hypothesis f<>1, but useful as positive control:
# [0,1] should certainly be a shadow, matching the trivial/base shadow)
checkTrivial := HexagonCheckZeroF(IdQ);;
Print("f=1 (対照): hex310=", checkTrivial.hex310, " hex311=", checkTrivial.hex311,
      " is_shadow=", checkTrivial.is_shadow, " (期待 true -- 陽性対照)\n");

sampleKs := [1, 2, 3, 10, 100, 1000, 10000, unitGroupOrder-1];;
shadowResults := [];;
anyShadowFound := false;;
for k in sampleKs do
  fk := TorusElement(genUnitMod^k);;
  res := HexagonCheckZeroF(fk);;
  Print("k=", k, ": hex310=", res.hex310, " hex311=", res.hex311, " is_shadow=", res.is_shadow, "\n");
  Add(shadowResults, rec(k := k, hex310 := res.hex310, hex311 := res.hex311, is_shadow := res.is_shadow));;
  if res.is_shadow then anyShadowFound := true;; fi;
od;

Print("\n[サンプル", Length(sampleKs), "個中] shadowになったf<>1の個数 = ",
      Length(Filtered(shadowResults, r -> r.is_shadow)), "\n");

# full sweep over the WHOLE centralizer (order unitGroupOrder = 476790) -- feasible size
Print("\n=== 全数探索: C_Q(ybar) 全", unitGroupOrder, "元について hexagon 判定 ===\n");
t0full := GAPLIB_WallElapsedMs();;
fullShadowCount := 0;;
fullCheckedCount := 0;;
firstNontrivialShadow := fail;;
for k in [1..unitGroupOrder-1] do
  fk := TorusElement(genUnitMod^k);;
  res := HexagonCheckZeroF(fk);;
  fullCheckedCount := fullCheckedCount + 1;;
  if res.is_shadow then
    fullShadowCount := fullShadowCount + 1;;
    if firstNontrivialShadow = fail then
      firstNontrivialShadow := rec(k := k, f := fk);;
    fi;
  fi;
  if k mod 100000 = 0 then
    Print("  progress: ", k, "/", unitGroupOrder-1, " (", GAPLIB_WallElapsedMs()-t0full, "ms)\n");
  fi;
od;
t1full := GAPLIB_WallElapsedMs();;
Print("全数探索完了: checked=", fullCheckedCount, " shadow_count(f<>1)=", fullShadowCount,
      " elapsed_ms=", t1full-t0full, "\n");

sgGap1Answer := (fullShadowCount > 0);;
Print("\n[SG-GAP-1] 答え: f<>1 in C_Q(ybar) で [0,f] が shadow になり得るか = ", sgGap1Answer, "\n");
if sgGap1Answer then
  Print("  ==> Psi は N' 上で単射ではない(非自明な kernel 元が存在)\n");
  Print("  最初の非自明witness: k=", firstNontrivialShadow.k, "\n");
else
  Print("  ==> Psi は N' 上で単射(真の埋入) -- C_Q(ybar) の全", unitGroupOrder,
        "元中、f=1以外にshadowになるものは存在しなかった\n");
fi;

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_sggap1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

MatJson := function(M)
  return Concatenation("[[", String(Int(M[1][1])), ",", String(Int(M[1][2])), "],[",
                        String(Int(M[2][1])), ",", String(Int(M[2][2])), "]]");
end;;

witnessJson := "null";;
if firstNontrivialShadow <> fail then
  witnessJson := Concatenation("{\"k\":", String(firstNontrivialShadow.k),
    ",\"f\":", MatJson(firstNontrivialShadow.f), "}");
fi;

scriptSha256 := ComputeSha256File("search/sg_gap1_v1.g");;

cert := Concatenation(
  "{\"schema\":\"sg_gap1/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/sg_gap1_v1.g\",\"order\":\"裁定1067 [SG-GAP-1] / docs/notes/settled_grp_proof_v1.md 5.1/7\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"ord_ybar\":", String(ordYbar),
  ",\"eigenvalues_distinct_regular\":", JB(regularCheck),
  ",\"split_torus_case\":", JB(splitCase),
  ",\"unit_group_order_p2\":", String(unitGroupOrder),
  ",\"centralizer_C_Q_ybar_order\":", String(unitGroupOrder),
  ",\"centralizer_is_cyclic\":true",
  ",\"centralizer_structure_note\":\"regular semisimple元の中心化群=分裂maximal torus(=(Z/p^2)^xと同型・巡回、pが奇素数ゆえ(Z/p^2)^xは巡回)\"",
  ",\"diagonalization_verified\":", JB(checkEigVec1 and checkEigVec2 and Pinvertible and sanityYbar),
  ",\"trivial_positive_control\":{\"hex310\":", JB(checkTrivial.hex310),
    ",\"hex311\":", JB(checkTrivial.hex311), ",\"is_shadow\":", JB(checkTrivial.is_shadow), "}",
  ",\"full_sweep\":{",
    "\"centralizer_order_swept\":", String(unitGroupOrder-1),
    ",\"checked_count\":", String(fullCheckedCount),
    ",\"shadow_count_f_nontrivial\":", String(fullShadowCount),
    ",\"answer_SG_GAP_1\":", JB(sgGap1Answer),
    ",\"first_nontrivial_witness\":", witnessJson,
    ",\"elapsed_ms\":", String(t1full-t0full),
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/sg_gap1_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
