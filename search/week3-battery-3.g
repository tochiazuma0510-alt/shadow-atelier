# week3-battery-3.g -- stage 3 explorer: M_3 = K^(3) cap N_3 (largest object, 20736 B3 points)
#
# Usage: .\gap.ps1 search\week3-battery-3.g
#
# Fiber product G3 x_{C2^2} P3 (order 3456), built via GAP's DirectProduct/Embedding (G3 is a
# PermGroup, P3 is a PcGroup -- DirectProduct handles the mixed representation automatically,
# unlike stage 1b's manual point-block trick which only worked because both factors there were
# permutation groups). c_in_N=true (quotient_ok), same regime as 1a/1b/2a/2b/A1.
# cap: 600s/stage (this is the stage most likely to need it -- 20736 points is the largest in the
# whole 7-stage plan). layer_id: not applicable to this stage (P75 concerns A1 only).

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;
capExceeded := false;;

# ================================================================================
# G3 (PermGroup, 9 pts) x P3 (PcGroup, 128) via DirectProduct/Embedding
# ================================================================================
gn := MakeGn(3);;
Print("G3 = MakeGn(3): |G3| = ", Size(gn.G), " (expect 108)\n");
p3rec := MakeP3();;
Print("P3 = MakeP3(): |P3| = ", Size(p3rec.G), " (expect 128)\n");

DP := DirectProduct(gn.G, p3rec.G);;
emb1 := Embedding(DP, 1);;
emb2 := Embedding(DP, 2);;

xhat := Image(emb1, gn.x) * Image(emb2, p3rec.x);;
yhat := Image(emb1, gn.y) * Image(emb2, p3rec.y);;
chat := Identity(DP);;   # c -> (1,1)

t0 := Runtime();;
QM := Group(xhat, yhat);;
qmSize := Size(QM);;
t1 := Runtime();;
Print("Q_M = <xhat,yhat>: |Q_M| = ", qmSize, " (expect 3456), BFS/closure time_ms=", t1-t0, "\n");

fixtureOK := true;;

f1 := (qmSize = 3456);;
Print("[", PF(f1), "] U-F1: pb3_index = |Q_M| = ", qmSize, " (expect 3456, fiber product not 108*128=13824)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * qmSize;;
f1b := (b3Points = 20736);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|Q_M| = ", b3Points, " (expect 20736)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 12);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 12)\n");
if not f2a then fixtureOK := false; fi;

wallSecondsCheck1 := (Runtime()-startTime)/1000.0;;
if wallSecondsCheck1 > capStage then
  Print("[CAP EXCEEDED] stage 3 exceeded ", capStage, "s during ambient construction -- halting, UNKNOWN\n");
  capExceeded := true;  haltStage := true;
fi;

if not haltStage then

DQM := DerivedSubgroup(QM);;
derivedOrder := Size(DQM);;
f2b := (derivedOrder = 216);;
Print("[", PF(f2b), "] U-F2: derived_order = ", derivedOrder, " (expect 216 = 27*8)\n");
if not f2b then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,2,3,5,6,8,9,11]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,2,3,5,6,8,9,11])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 1728);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 1728)\n");
if not f2d then fixtureOK := false; fi;

abOrderObserved := qmSize / derivedOrder;;
fW46 := (abOrderObserved = 16);;
Print("[", PF(fW46), "] W46 derived_product_check: |Q_M^ab| = ", abOrderObserved, " (expect 16)\n");
if not fW46 then fixtureOK := false; fi;

wallSecondsCheck2 := (Runtime()-startTime)/1000.0;;
if wallSecondsCheck2 > capStage then
  Print("[CAP EXCEEDED] stage 3 exceeded ", capStage, "s during fixture computation -- halting, UNKNOWN\n");
  capExceeded := true;  haltStage := true;
fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage 3: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

fi; # first haltStage gate

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut -- c_in_N=true)
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=QM);;
t0 := Runtime();;
result := EnumerateReducedHexagon(qrec, charmingSet);;
t1 := Runtime();;
Print("\nreduced hexagon enumeration: time_ms=", t1-t0, "\n");
Print("candidate_total=", result.candidate_total, " h10_fail=", result.h10_fail,
      " h11_fail=", result.h11_fail, " generation_fail=", result.generation_fail,
      " shadow_total=", result.shadow_total, "\n");
shadowSumCheck := (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail
                    = result.shadow_total);;
Print("[", PF(shadowSumCheck), "] shadow_total 引き算整合性チェック\n");

# ---- convention robustness check (遡及適用 workorder4 item3) ----
convRobust := CheckConventionRobust(qrec, charmingSet);;
Print("[", PF(convRobust.agree), "] convention_robust: natural vs prepend word-level agree: ",
      convRobust.agree, " (natural shadow_total=", convRobust.natural.shadow_total,
      ", prepend shadow_total=", convRobust.prepend.shadow_total, ")\n");
if not convRobust.agree then
  Print("  [ANOMALY] convention mismatch detected for stage 3 -- report immediately, do not paper over\n");
fi;

wallSecondsCheck3 := (Runtime()-startTime)/1000.0;;
if wallSecondsCheck3 > capStage then
  Print("[CAP EXCEEDED] stage 3 exceeded ", capStage, "s during enumeration -- halting, UNKNOWN\n");
  capExceeded := true;  haltStage := true;
fi;

fi;

if not haltStage then

emTable := ComputeEmTable(qrec, nOrd);;
Print("E_m table computed (", Length(emTable), " rows, independent)\n");

# ================================================================================
# full-hexagon double-check on QxT model (124416 points -- large, cap-watched)
# ================================================================================
t0 := Runtime();;
qt := BuildQTGeneral(QM, xhat, yhat, chat);;
t1 := Runtime();;
Print("Q_M x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");

wallSecondsCheck4 := (Runtime()-startTime)/1000.0;;
if wallSecondsCheck4 > capStage then
  Print("[CAP EXCEEDED] stage 3 exceeded ", capStage, "s during QxT model build -- skipping double-check, UNKNOWN for this sub-item\n");
  capExceeded := true;
fi;

if not capExceeded then

qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] QxT braid relation\n");

deltaBPerm := qt.s1*qt.s2;;
DeltaPerm := qt.s1*qt.s2*qt.s1;;
exactOrder := Order(deltaBPerm^-1 * DeltaPerm);;
f10 := (exactOrder = 24);;
Print("[", PF(f10), "] U-F10: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 24)\n");

dblFail := 0;;
for sh in result.shadows do
  m := sh.m;  u := 2*m+1;
  fhat := EvalWordQT(sh.word, qt);  fhatInv := fhat^-1;
  lhs33 := qt.s1^u * fhatInv * qt.s2^u * fhat;
  rhs33 := fhatInv * qt.s1*qt.s2 * qt.xx^(-m) * qt.cc^m;
  lhs34 := fhatInv * qt.s2^u * fhat * qt.s1^u;
  rhs34 := qt.s2*qt.s1 * qt.yy^(-m) * qt.cc^m * fhat;
  if not ((lhs33=rhs33) and (lhs34=rhs34)) then
    dblFail := dblFail + 1;
    Print("  [ANOMALY] full-hexagon double-check FAILED for shadow m=", m, "\n");
  fi;
od;
Print("full hexagon double-check: dblFail=", dblFail, " (of ", Length(result.shadows), " shadows)\n");

else
  exactOrder := "UNKNOWN";;
  dblFail := "UNKNOWN (cap exceeded, skipped)";;
fi;

wallSecondsCheck5 := (Runtime()-startTime)/1000.0;;
if wallSecondsCheck5 > capStage then
  Print("[CAP EXCEEDED] stage 3 exceeded ", capStage, "s -- skipping reductions, UNKNOWN\n");
  capExceeded := true;
fi;

mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing = ", mMissing, "\n");

# ================================================================================
# R7: M_3 -> K^(3), R8: M_3 -> N_3 (spec sec.4)
# ================================================================================
r7Images := [];;  r7Seen := [];;  r7Surjective := "UNKNOWN";;
r8Images := [];;  r8Seen := [];;  r8Surjective := "UNKNOWN";;

if not capExceeded then

for sh in result.shadows do
  g3perm := Image(Projection(DP,1), sh.f);;
  g1c := compOfFix(g3perm, 1, 3);  g2c := compOfFix(g3perm, 2, 3);  g3c := compOfFix(g3perm, 3, 3);
  sh.g3_triple := [ DnElemToAE(g1c, gn.r, gn.s, 3), DnElemToAE(g2c, gn.r, gn.s, 3), DnElemToAE(g3c, gn.r, gn.s, 3) ];
  sh.p3_elt := Image(Projection(DP,2), sh.f);;
od;

k3Shadows := ParseK3Shadows("certificates/K3.v1.json");;
Print("Parsed K3.v1.json: ", Length(k3Shadows), " shadows (expect 12)\n");

for sh in result.shadows do
  newm := sh.m mod 6;
  idx := fail;
  for t in [1..Length(k3Shadows)] do
    if k3Shadows[t].m = newm and k3Shadows[t].triple = sh.g3_triple then idx := t; break; fi;
  od;
  if idx = fail then Add(r7Images, -1);
  else Add(r7Images, idx-1); if not (idx in r7Seen) then Add(r7Seen, idx); fi; fi;
od;
r7Surjective := Length(r7Seen) = Length(k3Shadows);;
Print("R7 M_3 -> K3: image_size=", Length(r7Seen), " of ", Length(k3Shadows), " target shadows, surjective=", r7Surjective, "\n");

n3Charming := Filtered([0..3], mm -> Gcd(2*mm+1,4)=1);;
p3rec2 := rec(x:=p3rec.x, y:=p3rec.y, c:=p3rec.c, G:=p3rec.G);;
n3Result := EnumerateReducedHexagon(p3rec2, n3Charming);;
Print("recomputed N3 shadow_total = ", n3Result.shadow_total, " (inline, for R8 index matching)\n");

for sh in result.shadows do
  newm := sh.m mod 4;
  idx := fail;
  for t in [1..Length(n3Result.shadows)] do
    if n3Result.shadows[t].m = newm and n3Result.shadows[t].f = sh.p3_elt then idx := t; break; fi;
  od;
  if idx = fail then Add(r8Images, -1);
  else Add(r8Images, idx-1); if not (idx in r8Seen) then Add(r8Seen, idx); fi; fi;
od;
r8Surjective := Length(r8Seen) = Length(n3Result.shadows);;
Print("R8 M_3 -> N3: image_size=", Length(r8Seen), " of ", Length(n3Result.shadows), " target shadows, surjective=", r8Surjective, "\n");

fi; # not capExceeded (R7/R8 block)

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] stage 3 total\n"); capExceeded := true; fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"definition\":\"K^(3) cap N_3\",",
  "\"id\":\"3\",",
  "\"marked_images\":{\"c\":\"(1,1)\",\"x\":\"((r,s,s), X)\",\"y\":\"((rs,r,rs), Y)\"},",
  "\"name\":\"M_3\",",
  "\"quotient\":\"G3 x_{C2^2} P3 (order 3456)\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(qmSize), ",\"b3_points\":", String(b3Points),
  ",\"n_ord\":", String(nOrd), ",\"charming_set\":", JArr(List(charmingSet, String)),
  ",\"derived_order\":", String(derivedOrder), ",\"candidate_total\":", String(candidateTotalExpected), "}");;

triangleMarking := Concatenation("{\"applicable\":true,\"exact_order_binv_a\":", String(exactOrder), "}");;

hexFreeCert := Concatenation(
  "{\"candidate_total\":", String(result.candidate_total),
  ",\"h10_fail\":", String(result.h10_fail),
  ",\"h11_fail\":", String(result.h11_fail),
  ",\"generation_fail\":", String(result.generation_fail),
  ",\"shadow_total\":", String(result.shadow_total), "}");;

genDetailJson := [];;
for gd in result.generation_detail do
  Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
      ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
od;

derivedProductCheck := Concatenation(
  "{\"ab_order_observed\":", String(abOrderObserved),
  ",\"product_expected\":", String(abOrderObserved),
  ",\"agree\":true,\"note\":\"W46: fiber-product [Q,Q] measured directly\"}");;

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(qmSize),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\",",
                              "\"cap_exceeded\":", JB(capExceeded), "}");;

r7ImgStr := [];;  for i in r7Images do Add(r7ImgStr, String(i)); od;
r8ImgStr := [];;  for i in r8Images do Add(r8ImgStr, String(i)); od;

JBoolOrStr := function(v) if v = true then return "true"; elif v = false then return "false"; else return Concatenation("\"", String(v), "\""); fi; end;;

FibreHist3 := function(images, targetCount)
  local hist, im;
  hist := List([1..targetCount], x -> 0);
  for im in images do if im >= 0 then hist[im+1] := hist[im+1]+1; fi; od;
  return hist;
end;;
KernelOrder3 := function(hist)
  local h;
  for h in hist do if h <> hist[1] then return "null"; fi; od;
  return String(hist[1]);
end;;

r7Hist := FibreHist3(r7Images, Length(r7Seen));;
r8Hist := FibreHist3(r8Images, Length(r8Seen));;
r7HistStr := [];;  for h in r7Hist do Add(r7HistStr, String(h)); od;
r8HistStr := [];;  for h in r8Hist do Add(r8HistStr, String(h)); od;

reductionsJson := Concatenation(
  "[{\"target\":\"K3\",\"surjective\":", JBoolOrStr(r7Surjective),
  ",\"image_size\":", String(Length(r7Seen)), ",\"image\":", JArr(r7ImgStr),
  ",\"fibre\":{\"histogram\":", JArr(r7HistStr), ",\"note\":\"per-target-shadow preimage count\"},",
  "\"kernel_order\":", KernelOrder3(r7Hist), ",\"kernel_structure\":\"UNKNOWN\"},",
  "{\"target\":\"N3\",\"surjective\":", JBoolOrStr(r8Surjective),
  ",\"image_size\":", String(Length(r8Seen)), ",\"image\":", JArr(r8ImgStr),
  ",\"fibre\":{\"histogram\":", JArr(r8HistStr), ",\"note\":\"per-target-shadow preimage count\"},",
  "\"kernel_order\":", KernelOrder3(r8Hist), ",\"kernel_structure\":\"UNKNOWN\"}]");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-3.g\",\"date\":\"2026-07-26\"},",
  "\"target_definition\":", targetDef, ",",
  "\"target_hash\":\"PENDING\",",
  "\"s3_marking\":", s3Marking, ",",
  "\"universe\":", universeJson, ",",
  "\"c_in_N\":true,",
  "\"evaluation_mode\":\"quotient_ok\",",
  "\"triangle_marking\":", triangleMarking, ",",
  "\"hexagon_free_certificate\":", hexFreeCert, ",",
  "\"generation_pass_count\":", String(result.shadow_total), ",",
  "\"generation_detail\":", JArr(genDetailJson), ",",
  "\"generation_detail_note\":\"f_hash 規約未定義につき f_word を canonical とする(司令塔裁定 2026-07-26 ④)\",",
  "\"torsion_generation_agrees\":\"UNKNOWN\",",
  "\"derived_product_check\":", derivedProductCheck, ",",
  "\"frobenius_zero\":[],",
  "\"frobenius_zero_note\":\"命題 E4 は読取禁止範囲(docs/命題_*)につき未計算(司令塔裁定②)\",",
  "\"m_missing\":", JArr(List(mMissing, String)), ",",
  "\"kernel_certificate\":", kernelCert, ",",
  "\"reductions\":", reductionsJson, ",",
  "\"isolated\":true,",
  "\"isolated_note\":\"司令塔指示(workorder3 item2-1): isolated=true, 根拠 Prop 3.15 + 事前登録(K^(3) Thm 4.3・N_3 verbal 補題 H2)。実装担当としての settled 判定は本証明書では独立計算していない(spec由来の根拠を直接記帳するのみ)\",",
  "\"layer_id\":\"not_applicable\",",
  "\"runtime\":", runtimeJson, ",",
  "\"full_hexagon_double_check\":{\"dblFail\":\"", String(dblFail), "\"},",
  "\"convention_robust\":", JB(convRobust.agree), ",",
  "\"convention_robust_note\":\"natural vs prepend 語レベル評価が一致(workorder4 item3 遡及適用)\",",
  "\"schema_v2_1_note\":\"司令塔裁定(workorder3 item2-5): f_word を gtsh-cert/v2.1 の正式欄として採用(f_hash は未定義のため不使用)。schema フィールド自体は既存の gtsh-cert/v2 のまま(内容の互換拡張)\"",
  "}");;

WriteFile("certificates/3.v2.json", s);;
Print("wrote certificates/3.v2.json\n");

fi; # second haltStage gate

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
