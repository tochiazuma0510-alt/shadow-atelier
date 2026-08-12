#############################################################################
## u6_routeD_gating.g -- 路D gating測定(裁定1112フォロー・数学者裁定1114推奨)。
##
## 数学者推薦(docs/notes/u63_iset4_p2_reading_v1.md 経由・司令塔中継): 非marked
## 核計数 #C(N) <= #Epi(B3, B3/N) / |Aut(B3/N)| は等式が正当。もし |B3/N| が
## 扱える規模なら #Epi/|Aut| の直接計算で #C=1 が「測定」でなく「証明」で閉じる
## 可能性がある。本 script はその GATE のみを測る: 4 壁窓の |B3/N| を計算し、
## その規模で #Epi(B3,B3/N) や Aut(B3/N) の直接計算が現実的かどうかの生値を出す。
## #Epi/Aut 自体はまだ計算しない(gating 先行、と司令塔指示)。
##
## Bq = B3/N はここでは wall_crown_census_v1.g と同じ witness 構成で得られる
## W.Bq (=Group(s1,s2), s1,s2 は braid 関係を満たす S_(n+3) 内の置換) から
## Size(W.Bq) を直接計算する(既存 census cert には |Bq| フィールドが無いため、
## 独立に計算)。
##
## u/c 非接触・封印非接触・prereg量非計算・NAME-COLLIDE: wall-window instances。
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;

AbstractProdW := function(l)
  local p, i;
  p := l[1];
  for i in [2 .. Length(l)] do p := p * l[i]; od;
  return p;
end;;

MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProdW([s1, s2, s1]);  dd := AbstractProdW([s1, s2]);
  cc := DD^2;  zz := AbstractProdW([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

BuildW := function(n, a1, b1)
  local aE, bE, s1, s2;
  aE := a1 * (n+1, n+3);
  bE := b1 * (n+1, n+3, n+2);
  s1 := bE^-1 * aE;
  s2 := aE * bE^2;
  if s1*s2*s1 <> s2*s1*s2 then Error("BuildW: braid assertion failed for n=", n); fi;
  return MakeWindow(s1, s2);
end;;

JBool := function(b) if b then return "true"; else return "false"; fi; end;;
JStrU := function(s)
  s := ReplacedString(s, "\\", "\\\\");
  s := ReplacedString(s, "\"", "\\\"");
  return Concatenation("\"", s, "\"");
end;;

## engineering feasibility threshold, clearly labeled as such (not a
## mathematical claim): above this order, AutomorphismGroup/IdGroup/#Epi-style
## direct computation on a general (non-permutation-optimized) finite group is
## not attempted in this campaign (GAP's SmallGroup/AutomorphismGroup library
## machinery is built for orders well below this; 10^7 is a generous, still
## clearly-labeled-arbitrary cutoff, open to revision).
FEASIBILITY_THRESHOLD := 10^7;;

AnalyzeGating := function(label, n, a1, b1)
  local W, bqOrder, feasible, elapsed;
  elapsed := Runtime();
  W := BuildW(n, a1, b1);
  bqOrder := Size(W.Bq);
  feasible := (bqOrder <= FEASIBILITY_THRESHOLD);
  return rec(label := label, n := n,
             bq_order := bqOrder,
             feasibility_threshold := FEASIBILITY_THRESHOLD,
             direct_epi_aut_computation_feasible := feasible,
             elapsed_ms := Runtime() - elapsed);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"label\":", JStrU(r.label), ",\"n\":", String(r.n),
    ",\"bq_order\":", String(r.bq_order),
    ",\"feasibility_threshold\":", String(r.feasibility_threshold),
    ",\"direct_epi_aut_computation_feasible\":", JBool(r.direct_epi_aut_computation_feasible),
    ",\"elapsed_ms\":", String(r.elapsed_ms), "}");
end;;

Print("############################################################\n");
Print("# u6_routeD_gating.g -- 路D gating (|B3/N|・#Epi/Aut直接計算の可否)\n");
Print("############################################################\n");

t0Global := Runtime();;

results := [];;
Add(results, AnalyzeGating("wall24", 24,
  (1,13)(2,9)(3,5)(4,24)(6,8)(7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
  (1,12,9)(2,8,5)(3,4,24)(6,7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23)));;
Add(results, AnalyzeGating("wall28", 28,
  (1,8)(2,4)(3,24)(5,7)(6,27)(9,11)(10,25)(12,23)(13,14)(15,22)(16,18)(17,28)(19,21)(20,26),
  (1,7,4)(2,3,24)(5,6,27)(8,23,11)(9,10,25)(12,22,14)(15,21,18)(16,17,28)(19,20,26)));;
Add(results, AnalyzeGating("wall36", 36,
  (1,3)(2,34)(4,29)(5,25)(6,16)(7,9)(8,35)(10,15)(11,12)(13,14)(17,24)(18,20)(19,32)(21,23)(22,33)(26,28)(27,36)(30,31),
  (1,2,34)(3,31,29)(4,28,25)(5,24,16)(6,15,9)(7,8,35)(10,14,12)(17,23,20)(18,19,32)(21,22,33)(26,27,36)));;
Add(results, AnalyzeGating("wall37", 37,
  (1,30)(2,11)(3,7)(4,5)(8,10)(9,35)(12,29)(13,15)(14,32)(16,28)(17,19)(18,36)(20,27)(21,23)(22,33)(24,26)(25,37)(31,34),
  (1,29,11)(2,10,7)(3,6,5)(8,9,35)(12,28,15)(13,14,32)(16,27,19)(17,18,36)(20,26,23)(21,22,33)(24,25,37)(30,31,34)));;

for r in results do
  Print(r.label, ": |B3/N|=", r.bq_order,
        " feasible(<=", r.feasibility_threshold, ")=", r.direct_epi_aut_computation_feasible,
        " elapsed_ms=", r.elapsed_ms, "\n");
od;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/u6_routeD_gating_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/u6_routeD_gating.g\",",
  "\"order\":\"裁定1112フォロー・数学者裁定1114推奨(路D gating)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"method_note\":\"gating measurement only: |B3/N|=|Bq| computed directly from the wall-window ",
  "generator construction (independent of any existing cert). #Epi(B3,B3/N)/|Aut(B3/N)| itself is ",
  "NOT computed here (per coordinator's instruction: gating value first). ",
  "direct_epi_aut_computation_feasible is an ENGINEERING judgement against an explicitly-labeled, ",
  "arbitrary threshold (10^7), not a mathematical claim -- see FEASIBILITY_THRESHOLD comment in the ",
  "script.\",",
  "\"walls\":[", JoinStringsWithSeparator(List(results, ResultToJson), ","), "],",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(Runtime() - t0Global),
  "}"
);;

outPath := "search/certs/u6_routeD_gating_v1_20260813.json";;
outStream := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, cert);;
CloseStream(outStream);;
Print("\nwrote ", outPath, "\n");
Print("U6_ROUTED_GATING_DONE\n");
QUIT;
