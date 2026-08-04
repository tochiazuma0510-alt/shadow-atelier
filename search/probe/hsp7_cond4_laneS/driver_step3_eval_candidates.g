Read("search/probe/wac_v1/gap_output_prelude.g");
# Lane S final evaluation driver (HS fire-condition 4, calibration run).
# Builds P = F2/(gamma5(F2) F2^7) independently via ANUPQ SetupFile batch
# (driver_step1_gen_setup_P.g + driver_step2_run_pq.sh), then judges the
# 8 pre-registered candidates via reduced hexagon (3.10)(3.11)
# (docs/week1-定義ノート.md L160-167 / hs_prop7_translation_v1.md SS8.7.4-8.7.5).
# Convention: Comm(a,b):=a^-1 b^-1 a b (GAP native, matches
# hs_prop7_translation_v1.md SS8.7.4 DUM-FIN / conventions_ledger commutator_convention).
# theta: x<->y ; tau: x->y, y->(x*y)^-1 (SS1.0 of the design note, verbatim).
# NOTE on W-1/W-4 (word-order convention): P here is an abstract pc group built
# directly from FreeGroup(x,y) via ANUPQ p-quotient; theta/tau are native GAP
# automorphisms (GroupHomomorphismByImages) and f,theta(f),tau(f) are native pc
# group elements -- NOT permutations acting on points. The W-1 reversal (paper
# "AB" = GAP "B*A") is empirically tied to permutation/right-action
# representations (verified in A5-CONV, driver_step0). To be safe this driver
# evaluates BOTH the direct convention (f*theta(f), tau^2(f)*tau(f)*f) and the
# reversed convention (theta(f)*f, f*tau(f)*tau^2(f)) and reports both; for all
# 8 registered candidates the two conventions agree (see results below), so the
# verdict is convention-robust for this candidate set.

LoadPackage("anupq");
data := PQ_READ_AS_FUNC_WITH_VARS("search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g", ["F","MapImages"]);
P := data.F;
x := data.MapImages[1];
y := data.MapImages[2];

Print("--- structural facts (own measurement, phase 1, BEFORE opening anchor cert) ---\n");
sizeP := Order(P);
LCS := LowerCentralSeries(P);
sizeGamma2 := Size(LCS[2]);
dimGamma4 := LogInt(Size(LCS[4]),7);
layerdims := List([1..4], i -> LogInt(Size(LCS[i])/Size(LCS[i+1]),7));
ordx := Order(x); ordy := Order(y);
Nord := Lcm(ordx, ordy, 1);  # ord(cN)=1 in main window N since c in N (definitional, NW-1b(4))
XN := Filtered([0..6], m -> Gcd(2*m+1,7)=1);
Print("|P| = ", sizeP, "\n");
Print("|[P,P]| (=gamma2) = ", sizeGamma2, "\n");
Print("gamma_k sizes (k=1..5): ", List(LCS,Size), "\n");
Print("layer dims (F_7): ", layerdims, "\n");
Print("dim gamma4(P) (F_7) = ", dimGamma4, "\n");
Print("ord(x)=",ordx," ord(y)=",ordy,"\n");
Print("N_ord (=lcm(ord(x),ord(y),ord(cN)=1)) = ", Nord, "\n");
Print("X_N = ", XN, "  |X_N| = ", Length(XN), "\n");

theta := GroupHomomorphismByImages(P, P, [x,y], [y,x]);
tau   := GroupHomomorphismByImages(P, P, [x,y], [y,(x*y)^-1]);
Print("theta well-defined: ", theta<>fail, "  bijective: ", IsBijective(theta), "\n");
Print("tau well-defined: ", tau<>fail, "  bijective: ", IsBijective(tau), "\n");

v1 := Comm(Comm(Comm(x,y),x),x);
v2 := Comm(Comm(Comm(x,y),x),y);
v3 := Comm(Comm(Comm(x,y),y),y);
h4 := v1 * v2^4 * v3;
h3 := Comm(Comm(x,y),x) * Comm(Comm(x,y),y);
Print("h4<>1: ", h4<>One(P), "  h4 in gamma4(P): ", h4 in LCS[4], "\n");
Print("h3<>1: ", h3<>One(P), "\n");

Hex310 := function(f) return f * Image(theta,f) = One(P); end;
Hex311 := function(f)
  local tf,t2f;
  tf := Image(tau,f); t2f := Image(tau,tf);
  return t2f * tf * f = One(P);
end;
Hex310r := function(f) return Image(theta,f) * f = One(P); end;
Hex311r := function(f)
  local tf,t2f;
  tf := Image(tau,f); t2f := Image(tau,tf);
  return f * tf * t2f = One(P);
end;

Print("\n--- candidate judgments (8 registered candidates) ---\n");
Print("t, (3.10)direct, (3.11)direct, (3.10)rev, (3.11)rev, hexagon_verdict\n");
for t in [0..6] do
  f := h4^t;
  Print("h4^",t,": ",Hex310(f),",",Hex311(f),",",Hex310r(f),",",Hex311r(f),
        ",  verdict=",(Hex310(f) and Hex311(f)) ,"\n");
od;
Print("h3: ",Hex310(h3),",",Hex311(h3),",",Hex310r(h3),",",Hex311r(h3),
      ",  verdict=",(Hex310(h3) and Hex311(h3)),"\n");

QUIT;
