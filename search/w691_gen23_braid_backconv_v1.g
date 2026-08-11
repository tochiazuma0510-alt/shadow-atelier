## search/w691_gen23_braid_backconv_v1.g -- direct braid-pair back-conversion check (裁定836).
## Uses the witness pairs (a,b) already PROVEN to (2,3)-generate H_2/H_6
## (search/certs/w691_gen23_witness_v1_20260812.json, commit 86b3439). Per
## docs/notes/w691_scan_gen23_spec_v1.md §4's bijection ((x,y) |-> (u,v)=(xyx,xy), inverse
## x=v^-1*u, y=u^-1*v^2), constructs x,y from (u,v):=(a,b) and DIRECTLY machine-checks
## (i) x*y*x = y*x*y (the actual braid relation) and (ii) <x,y> = H_d (same order, via the fast
## projective-line-action method from search/w691_gen23_witness_v1.g -- NOT re-derived from
## first principles here, reused verbatim since it was already independently cross-checked for
## that script). This makes the "理論上自明" claim from the earlier report a MACHINE-CONFIRMED
## fact for these two specific witnesses, not merely a citation of the bijection.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

p := 691;;
Fp := GF(p);;

## witness matrices (verbatim from search/certs/w691_gen23_witness_v1_20260812.json)
aH2 := [[608,300],[364,83]] * One(Fp);;
bH2 := [[192,158],[6,498]] * One(Fp);;
aH6 := [[540,503],[283,151]] * One(Fp);;
bH6 := [[490,398],[454,639]] * One(Fp);;

slOrder := Size(SL(2,p));;
h2Order := 2*slOrder;;
h6Order := 6*slOrder;;

## ---- fast projective-line (692 points) machinery (verbatim from w691_gen23_witness_v1.g) ----
Canon := function(v)
  if v[1] <> Zero(Fp) then return v / v[1]; else return v / v[2]; fi;
end;;
projPts := [];;
for x in Fp do Add(projPts, Canon([x, One(Fp)])); od;
Add(projPts, Canon([One(Fp), Zero(Fp)]));
projPts := Set(projPts);;
ActOnProjPt := function(v, M) return Canon(M * v); end;;
posOf := function(v) return Position(projPts, v); end;;
PermOfMatrix := function(M)
  return PermList(List(projPts, v -> posOf(ActOnProjPt(v, M))));
end;;
FastGroupOrder := function(x, y)
  local px, py;
  px := PermOfMatrix(x);  py := PermOfMatrix(y);
  return Size(Group(px, py));
end;;
DetSubgroupOrder := function(x, y)
  return Size(Group(DeterminantMat(x), DeterminantMat(y)));
end;;

## ---- back-conversion: u:=a, v:=b, x:=v^-1*u, y:=u^-1*v^2 ----
BackConvertAndCheck := function(label, u, v, targetOrder, targetD)
  local x, y, xyx, yxy, braidOk, sizePerm, detOrd, genOk;
  x := v^-1 * u;;
  y := u^-1 * v^2;;
  xyx := x*y*x;;
  yxy := y*x*y;;
  braidOk := (xyx = yxy);;
  sizePerm := FastGroupOrder(x,y);;
  detOrd := DetSubgroupOrder(x,y);;
  genOk := (sizePerm = slOrder) and (detOrd = targetD);;
  Print(label, ": braid_ok=", braidOk, " size_perm=", sizePerm, " (expect ", slOrder,
        ") det_order=", detOrd, " (expect ", targetD, ") generates_H_d=", genOk, "\n");
  return rec(label:=label, x:=x, y:=y, braid_ok:=braidOk, size_perm:=sizePerm,
             det_order:=detOrd, generates_H_d:=genOk, target_order:=targetOrder, target_d:=targetD);
end;;

resH2 := BackConvertAndCheck("H_2", aH2, bH2, h2Order, 2);;
resH6 := BackConvertAndCheck("H_6", aH6, bH6, h6Order, 6);;

## ============ JSON output ============
JMatFp := function(m)
  return Concatenation("[[", String(IntFFE(m[1][1])), ",", String(IntFFE(m[1][2])), "],[",
                        String(IntFFE(m[2][1])), ",", String(IntFFE(m[2][2])), "]]");
end;;

JResult := function(r)
  return Concatenation("{",
    "\"label\":", JStr(r.label), ",",
    "\"x\":", JMatFp(r.x), ",",
    "\"y\":", JMatFp(r.y), ",",
    "\"braid_relation_ok\":", JB(r.braid_ok), ",",
    "\"size_perm\":", String(r.size_perm), ",",
    "\"det_order\":", String(r.det_order), ",",
    "\"target_d\":", String(r.target_d), ",",
    "\"generates_H_d\":", JB(r.generates_H_d), ",",
    "\"target_order\":", String(r.target_order),
    "}");
end;;

allOk := resH2.braid_ok and resH2.generates_H_d and resH6.braid_ok and resH6.generates_H_d;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/w691_gen23_braid_backconv_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a836 -- \\u76f4\\u63a5\\u9006\\u5909\\u63db\\u78ba\\u8a8d\\u3001docs/notes/w691_scan_gen23_spec_v1.md \\u00a74 \\u306e\\u5168\\u5358\\u5c04(x,y)->(xyx,xy)\\u306e\\u9006\\u5199\\u50cf\",",
  "\"source_witnesses\":\"search/certs/w691_gen23_witness_v1_20260812.json (commit 86b3439)\",",
  "\"method_note\":\"x:=v^-1*u, y:=u^-1*v^2 with (u,v):=(a,b) the already-proven (2,3)-generating witness pair. Directly checks x*y*x=y*x*y (actual braid relation, matrix computation over F_691) AND <x,y>=H_d (same fast projective-line-action method used for the witness search).\",",
  "\"results\":[", JResult(resH2), ",", JResult(resH6), "],",
  "\"all_ok\":", JB(allOk), ",",
  "\"no_verdict_note\":\"raw matrix/order data and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/w691_gen23_braid_backconv_v1_20260812.json", out);;
Print("Wrote search/certs/w691_gen23_braid_backconv_v1_20260812.json\n");
Print("W691_GEN23_BRAID_BACKCONV_DONE\n");
QUIT;
