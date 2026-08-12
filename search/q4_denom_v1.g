# search/q4_denom_v1.g -- [Q4-DENOM] GT^settled(N') の位数決定(裁定1070キュー・裁定1068)
#
# 正本: docs/notes/gt_settled_identification_v1.md §5。
# 前提: xbar,ybar,sigma1,sigma2 は q3r1_lift_spec_v1 §3-4 の実測値(mod 691^2)。
# SG-GAP-1 = NO(既に確立済み)。
#
# [D-1] C := C_PGL(xbar) を構成(xbarは分裂半単純・中心化群=分裂torus位数p(p-1)=476790)
# [D-2] 各g in Cについてf_g:=g^-1(g^-1 ybar g = f_g^-1 ybar f_g を直接満たす自明な選択)、
#       [0,f_g]がshadowか(hex310・hex311)を全数判定(476790元、SG-GAP-1と同規模)
# [D-3] u=-1成分: [-1,1]がshadowか(=iota(N')=N'か)をGS-GAP-1(裁定1064のQ3-M1と別物、
#       ここでは(m,f)=(-1,1)の直接判定)
# [D-4] 見張り: |GT^settled(N')|は476790の約数(u=+1)またはその2倍。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/probe/wac_v1/gap_output_prelude.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

p := 691;;
p2 := p^2;;
Zp2 := Integers mod p2;;

# ---- reconstruct sigma1, sigma2, xbar, ybar (identical to q3_r1_lift_v1.g/sg_gap1_v1.g) ----
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
Print("xbar = ", List(xbar, r -> List(r, Int)), "\n");
xbarOk := (xbar = [[9115,57725],[391912,442339]]*One(Zp2));;
Print("[", PF(xbarOk), "] xbar 再構成一致: ", xbarOk, "\n");
if not xbarOk then Error("q4_denom_v1: xbar reconstruction mismatch"); fi;

Nord := 47679;;

# ---- [D-1] C := C_Q(xbar): diagonalize xbar, get split torus ----
trX := xbar[1][1] + xbar[2][2];;
Print("trace(xbar) = ", Int(trX), "\n");
discX := trX^2 - 4*One(Zp2);;
Zp := Integers mod p;;
discXmodP := Int(discX) * One(Zp);;
sqrtModP := fail;;
for cand in Elements(Zp) do
  if cand^2 = discXmodP then sqrtModP := cand; break;; fi;
od;
splitCase := (sqrtModP <> fail) and (discXmodP <> Zero(Zp));;
Print("[", PF(splitCase), "] disc(xbar) is nonzero square mod 691 (split case): ", splitCase, "\n");
if not splitCase then Error("q4_denom_v1: xbar is not split semisimple -- design assumption violated"); fi;

s0 := Int(sqrtModP) * One(Zp2);;
numerator := s0^2 - discX;;
denom := 2*s0;;
s1sqrt := s0 - numerator * denom^-1;;
sqrtCheck := (s1sqrt^2 = discX);;
Print("[", PF(sqrtCheck), "] Hensel-lifted sqrt(disc(xbar)) verified: ", sqrtCheck, "\n");
if not sqrtCheck then Error("q4_denom_v1: Hensel lift failed"); fi;

half := (2*One(Zp2))^-1;;
eig1 := (trX + s1sqrt) * half;;
eig2 := (trX - s1sqrt) * half;;
Print("eigenvalues of xbar: ", Int(eig1), ", ", Int(eig2), "\n");

M1 := xbar - eig1*IdentityMat(2,Zp2);;
eigVec1 := fail;;
if M1[1][2] <> Zero(Zp2) then eigVec1 := [ -M1[1][2], M1[1][1] ];;
elif M1[1][1] <> Zero(Zp2) then eigVec1 := [ M1[2][2], -M1[2][1] ];;
else eigVec1 := [ One(Zp2), Zero(Zp2) ];; fi;
checkEigVec1 := (xbar * eigVec1 = eig1 * eigVec1);;

M2 := xbar - eig2*IdentityMat(2,Zp2);;
eigVec2 := fail;;
if M2[1][2] <> Zero(Zp2) then eigVec2 := [ -M2[1][2], M2[1][1] ];;
elif M2[1][1] <> Zero(Zp2) then eigVec2 := [ M2[2][2], -M2[2][1] ];;
else eigVec2 := [ One(Zp2), Zero(Zp2) ];; fi;
checkEigVec2 := (xbar * eigVec2 = eig2 * eigVec2);;

Pmat := TransposedMat([eigVec1, eigVec2]);;
detP := DetMod(Pmat);;
Pinvertible := (Gcd(Int(detP), p) = 1);;
Print("[", PF(checkEigVec1 and checkEigVec2 and Pinvertible), "] diagonalization of xbar verified: ",
      checkEigVec1 and checkEigVec2 and Pinvertible, "\n");
if not (checkEigVec1 and checkEigVec2 and Pinvertible) then
  Error("q4_denom_v1: diagonalization failed");
fi;
Pinv := Pmat^-1;;

TorusElementX := function(t) return Pmat * DiagMod(t, t^-1) * Pinv;; end;;
sanityXbar := (TorusElementX(eig1) = xbar);;
Print("[", PF(sanityXbar), "] TorusElementX(eig1) == xbar: ", sanityXbar, "\n");
if not sanityXbar then Error("q4_denom_v1: torus parametrization sanity check failed"); fi;

unitGroupOrder := p*(p-1);;
Print("|C_Q(xbar)| = ", unitGroupOrder, " (期待 476790)\n");
genUnit := PrimitiveRootMod(p2);;
genUnitMod := genUnit * One(Zp2);;

# ---- hexagon machinery (identical to sg_gap1_v1.g) ----
DeltaMat := sigma1 * sigma2 * sigma1;;
deltaSmall := sigma2 * sigma1;;
Print("DeltaMat == atilde: ", DeltaMat = atilde, "\n");
Print("delta^3 == I: ", deltaSmall^3 = IdentityMat(2,Zp2), "\n");

ThetaFn := function(g) return DeltaMat * g * DeltaMat^-1;; end;;
TauFn := function(g) return deltaSmall * g * deltaSmall^-1;; end;;
IdQ := IdentityMat(2, Zp2);;

# general hexagon check for [m,f] (not just m=0): E_{m,f}(x)=x^u, E_{m,f}(y)=f^-1 y^u f
# where u=2m+1. hex310: f*theta(f)=1. hex311: tau^2(y^m f)*tau(y^m f)*(y^m f) = c^m = 1
# (c-image=1 in this N' setting, per q3r1_lift_spec/settled_grp_proof).
HexagonCheckGeneral := function(m, f)
  local hex310, ymf, tauYmf, tau2Ymf, hex311lhs, hex311;
  hex310 := (f * ThetaFn(f) = IdQ);;
  ymf := ybar^m * f;;
  tauYmf := TauFn(ymf);;
  tau2Ymf := TauFn(tauYmf);;
  hex311lhs := tau2Ymf * tauYmf * ymf;;
  hex311 := (hex311lhs = IdQ);;
  return rec(hex310 := hex310, hex311 := hex311, is_shadow := hex310 and hex311);;
end;;

# self-check against sg_gap1_v1 result (m=0, f=1 should be a shadow)
checkTrivial := HexagonCheckGeneral(0, IdQ);;
Print("陽性対照 [0,1]: hex310=", checkTrivial.hex310, " hex311=", checkTrivial.hex311,
      " is_shadow=", checkTrivial.is_shadow, " (期待 true)\n");

# ====================================================================
# [D-2] full sweep over C = C_Q(xbar) (476790 elements), f_g := g^-1
# ====================================================================
Print("\n============================================================\n");
Print("# [D-2] C_Q(xbar) 全数探索: f_g=g^-1 で [0,f_g] が shadow か\n");
Print("============================================================\n");
t0 := GAPLIB_WallElapsedMs();;
shadowCount := 0;;
shadowKs := [];;
for k in [0..unitGroupOrder-1] do
  g := TorusElementX(genUnitMod^k);;
  fg := g^-1;;
  res := HexagonCheckGeneral(0, fg);;
  if res.is_shadow then
    shadowCount := shadowCount + 1;;
    if Length(shadowKs) < 20 then Add(shadowKs, k);; fi;
  fi;
  if (k+1) mod 100000 = 0 then
    Print("  progress: ", k+1, "/", unitGroupOrder, " (", GAPLIB_WallElapsedMs()-t0, "ms) shadowCount so far=", shadowCount, "\n");
  fi;
od;
t1 := GAPLIB_WallElapsedMs();;
Print("D-2 完了: checked=", unitGroupOrder, " shadow_count(u=+1成分)=", shadowCount,
      " elapsed_ms=", t1-t0, "\n");

isDivisor := (unitGroupOrder mod shadowCount = 0);;
if shadowCount = 0 then isDivisor := false;; fi;
Print("[", PF(shadowCount > 0 and (unitGroupOrder mod shadowCount = 0)), "] shadow_count は0でなく",
      unitGroupOrder, "の約数: shadow_count=", shadowCount, "\n");

# ====================================================================
# [D-3] u=-1 成分: [-1,1] が shadow か
# ====================================================================
Print("\n============================================================\n");
Print("# [D-3] u=-1 成分: [-1,1] が shadow か(=iota(N')=N'か)\n");
Print("============================================================\n");
resMinus1 := HexagonCheckGeneral(-1, IdQ);;
Print("[-1,1]: hex310=", resMinus1.hex310, " hex311=", resMinus1.hex311,
      " is_shadow=", resMinus1.is_shadow, "\n");

# ====================================================================
# [D-4] final size determination
# ====================================================================
sizePlus := shadowCount;;
sizeTotal := sizePlus;;
if resMinus1.is_shadow then sizeTotal := sizePlus * 2;; fi;
Print("\n|GT^settled,+(N')| = ", sizePlus, "\n");
Print("u=-1 成分は空でない(shadow): ", resMinus1.is_shadow, "\n");
Print("|GT^settled(N')| = ", sizeTotal, " (", PF(sizeTotal >= 1), ")\n");

divisorCheckOk := (sizePlus > 0) and (unitGroupOrder mod sizePlus = 0);;
Print("[", PF(divisorCheckOk), "] [D-4] 見張り: |GT^settled,+| は 476790 の約数: ", divisorCheckOk, "\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_q4denom.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

FloatJson := function(x)
  local s;
  s := String(x);;
  if Length(s) > 0 and s[Length(s)] = '.' then s := Concatenation(s, "0");; fi;
  return s;;
end;;

scriptSha256 := ComputeSha256File("search/q4_denom_v1.g");;

cert := Concatenation(
  "{\"schema\":\"q4_denom/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/q4_denom_v1.g\",\"order\":\"裁定1070キュー [Q4-DENOM] / docs/notes/gt_settled_identification_v1.md 5\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"C_Q_xbar_order\":", String(unitGroupOrder),
  ",\"trivial_positive_control\":{\"is_shadow\":", JB(checkTrivial.is_shadow), "}",
  ",\"D2_full_sweep\":{",
    "\"checked_count\":", String(unitGroupOrder),
    ",\"shadow_count_u_plus1\":", String(shadowCount),
    ",\"elapsed_ms\":", String(t1-t0),
    ",\"sample_shadow_ks\":", JArr(List(shadowKs, String)),
  "}",
  ",\"D3_u_minus1\":{\"is_shadow\":", JB(resMinus1.is_shadow), "}",
  ",\"D4_result\":{",
    "\"size_GT_settled_plus\":", String(sizePlus),
    ",\"size_GT_settled_total\":", String(sizeTotal),
    ",\"divisor_check_ok\":", JB(divisorCheckOk),
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/q4_denom_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
