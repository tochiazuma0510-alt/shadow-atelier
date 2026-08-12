# search/q3_r1_lift_v1.g -- [Q3-R1-LIFT]+[Q3-R1] mod 691^2 リフト+共役類前フィルタ(裁定1062)
#
# 正本: docs/notes/q3r1_lift_spec_v1.md(数学者・80bcbe72)。
# 入力: search/certs/s2_3_pre_gen23_v1_20260812.json の witness a,b in SL^pm(2,691)。
#
# 手順: det調整つきリフト(§1)→ Teichmuller冪リフト(§2)→ braid対(§3、関係式は自動だが
#   fail-closedでassert)→ x̄=σ1²・ȳ=σ2²(§4訂正: σi自身ではなくσi²がPB3/N'の生成元)
#   → N_ord=lcm(ord(x̄),ord(ȳ))=47679 → charming u = (Z/47679)^× 30360個
#   → 各uについて x̄^u の trace(mod 691^2) が x̄ の trace と一致するか(共役の必要条件、
#     前フィルタ)を判定。SETTLE-AUTOによりkernel計算は不要(well_defined判定のみ)。
# [L14](生成性のSize計算)は仕様どおり実行しない(紙で確定済み・規模2.2e17)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

p := 691;;
p2 := p^2;;   # 477481
Zp2 := Integers mod p2;;

# witness a,b from search/certs/s2_3_pre_gen23_v1_20260812.json
ahat := [[483,28],[59,208]] * One(Zp2);;
bhat := [[245,158],[69,445]] * One(Zp2);;

DetMod := function(M) return M[1][1]*M[2][2] - M[1][2]*M[2][1];; end;;

detA := DetMod(ahat);;
detB := DetMod(bhat);;
Print("det ahat = ", Int(detA), " (期待 98812)\n");
Print("det bhat = ", Int(detB), " (期待 98123)\n");

lamA := -(detA^-1);;
lamB := detB^-1;;
Print("lambda_a = ", Int(lamA), " (期待 98814)\n");
Print("lambda_b = ", Int(lamB), " (期待 379360)\n");

DiagMod := function(d1, d2) return [[d1, Zero(Zp2)], [Zero(Zp2), d2]];; end;;

a0 := DiagMod(lamA, One(Zp2)) * ahat;;
b0 := DiagMod(lamB, One(Zp2)) * bhat;;

detA0 := DetMod(a0);;
detB0 := DetMod(b0);;
Print("det a0 = ", Int(detA0), " (期待 477480 = -1 mod 477481)\n");
Print("det b0 = ", Int(detB0), " (期待 1)\n");

l1 := (detA0 = -One(Zp2));;
l2 := (detB0 = One(Zp2));;
Print("[", PF(l1), "] [L1] det a0 == -1: ", l1, "\n");
Print("[", PF(l2), "] [L2] det b0 == 1: ", l2, "\n");

pOne := One(Integers mod p);;
ReduceModP := function(M)
  return List(M, row -> List(row, x -> Int(x) mod p));;
end;;
aModP := ReduceModP(ahat);;
a0ModP := ReduceModP(a0);;
bModP := ReduceModP(bhat);;
b0ModP := ReduceModP(b0);;
l3 := (a0ModP = aModP) and (b0ModP = bModP);;
Print("[", PF(l3), "] [L3] a0 == a, b0 == b (mod 691): ", l3, "\n");

# ---- Teichmuller power lift: a~ := a0^691, b~ := b0^691 (mod 691^2) ----
atilde := a0^p;;
btilde := b0^p;;
Print("atilde = ", List(atilde, r -> List(r, Int)), "\n");
Print("btilde = ", List(btilde, r -> List(r, Int)), "\n");
Print("(期待 atilde=[[466908,379387],[59,10573]], btilde=[[221365,197784],[456129,256115]])\n");

IdMod := IdentityMat(2, Zp2);;
l5 := (atilde^2 = IdMod);;
l6 := (btilde^3 = IdMod);;
Print("[", PF(l5), "] [L5] atilde^2 == I: ", l5, "\n");
Print("[", PF(l6), "] [L6] btilde^3 == I: ", l6, "\n");

detAtilde := DetMod(atilde);;
detBtilde := DetMod(btilde);;
l7 := (detAtilde = -One(Zp2)) and (detBtilde = One(Zp2));;
Print("[", PF(l7), "] [L7] det atilde == -1, det btilde == 1: ", l7, "\n");

atildeModP := ReduceModP(atilde);;
btildeModP := ReduceModP(btilde);;
l8 := (atildeModP = aModP) and (btildeModP = bModP);;
Print("[", PF(l8), "] [L8] atilde == a, btilde == b (mod 691): ", l8, "\n");

# ---- braid pair ----
sigma1 := btilde^-1 * atilde;;
sigma2 := atilde * btilde^2;;
Print("sigma1 = ", List(sigma1, r -> List(r, Int)), "\n");
Print("sigma2 = ", List(sigma2, r -> List(r, Int)), "\n");
Print("(期待 sigma1=[[158625,469515],[262365,86342]], sigma2=[[96915,106060],[215057,148052]])\n");

l9lhs := sigma1*sigma2*sigma1;;
l9rhs := sigma2*sigma1*sigma2;;
l10 := (l9lhs = l9rhs);;
Print("[", PF(l10), "] [L10] sigma1 sigma2 sigma1 == sigma2 sigma1 sigma2: ", l10, "\n");
l10b := (l9lhs = atilde);;
Print("  (追加確認) sigma1 sigma2 sigma1 == atilde: ", l10b, "\n");

detSigma1 := DetMod(sigma1);;
detSigma2 := DetMod(sigma2);;
l11 := (detSigma1 = -One(Zp2)) and (detSigma2 = -One(Zp2));;
Print("[", PF(l11), "] [L11] det sigma1 == det sigma2 == -1: ", l11, "\n");

# ---- x-bar, y-bar (SECTION 0 CORRECTION: sigma_i^2, not sigma_i) ----
xbar := sigma1^2;;
ybar := sigma2^2;;
detXbar := DetMod(xbar);;
detYbar := DetMod(ybar);;
l12 := (detXbar = One(Zp2)) and (detYbar = One(Zp2));;
Print("[", PF(l12), "] [L12] xbar := sigma1^2, ybar := sigma2^2 ; det xbar == det ybar == 1: ", l12, "\n");
Print("xbar = ", List(xbar, r -> List(r, Int)), "\n");
Print("ybar = ", List(ybar, r -> List(r, Int)), "\n");
Print("(期待 xbar=[[9115,57725],[391912,442339]], ybar=[[144005,26367],[434427,307449]])\n");

# ---- order of xbar, ybar in SL(2,Z/691^2) (matrix group, small enough to compute via GAP Order) ----
ordXbar := Order(xbar);;
ordYbar := Order(ybar);;
Print("ord(xbar) = ", ordXbar, " (期待 47679)\n");
Print("ord(ybar) = ", ordYbar, " (期待 47679)\n");
Nord := Lcm(ordXbar, ordYbar, 1);;
l13 := (ordXbar = 47679) and (ordYbar = 47679) and (Nord = 47679);;
Print("[", PF(l13), "] [L13] ord(xbar)==ord(ybar)==47679, N_ord==47679==3*23*691: ", l13, "\n");
Print("N_ord check: 3*23*691 = ", 3*23*691, "\n");

allLiftOk := l1 and l2 and l3 and l5 and l6 and l7 and l8 and l10 and l11 and l12 and l13;;
Print("\n[", PF(allLiftOk), "] ★★★ 全assert([L1]-[L13], [L14]は仕様により未実施) PASS: ", allLiftOk, "\n");

if not allLiftOk then
  Error("q3_r1_lift_v1: LIFT ASSERTIONS FAILED -- refusing to proceed to prefilter (fail-closed)");
fi;

# ==== [Q3-R1] prefilter: charming u -> trace(xbar^u) =? trace(xbar) ====
Print("\n============================================================\n");
Print("# [Q3-R1] 前フィルタ: charming u in (Z/47679)^x での x̄^u ~ x̄ 判定\n");
Print("============================================================\n");

TraceMod := function(M) return M[1][1] + M[2][2];; end;;
traceXbar := TraceMod(xbar);;
Print("trace(xbar) = ", Int(traceXbar), "\n");

charmingU := Filtered([1..47678], uu -> Gcd(uu, 47679) = 1);;
Print("charming u count = ", Length(charmingU), " (期待 30360)\n");
charmingCountOk := (Length(charmingU) = 30360);;
Print("[", PF(charmingCountOk), "] charming count == 30360: ", charmingCountOk, "\n");

t0 := GAPLIB_WallElapsedMs();;
survivedCount := 0;;
droppedCount := 0;;
survivedUs := [];;
for uu in charmingU do
  xu := xbar^uu;;
  traceXu := TraceMod(xu);;
  if traceXu = traceXbar then
    survivedCount := survivedCount + 1;;
    Add(survivedUs, uu);;
  else
    droppedCount := droppedCount + 1;;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();;
Print("survived (trace matches) = ", survivedCount, "\n");
Print("dropped (trace differs)  = ", droppedCount, "\n");
Print("elapsed_ms = ", t1-t0, "\n");
sumCheckOk := (survivedCount + droppedCount = Length(charmingU));;
Print("[", PF(sumCheckOk), "] survived+dropped == charming total: ", sumCheckOk, "\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_q3r1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/q3_r1_lift_v1.g");;

MatJson := function(M)
  return Concatenation("[[", String(Int(M[1][1])), ",", String(Int(M[1][2])), "],[",
                        String(Int(M[2][1])), ",", String(Int(M[2][2])), "]]");
end;;

survivedSample := survivedUs{[1..Minimum(50,Length(survivedUs))]};;

cert := Concatenation(
  "{\"schema\":\"q3_r1_prefilter/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/q3_r1_lift_v1.g\",\"order\":\"裁定1062 [Q3-R1-LIFT]+[Q3-R1] / docs/notes/q3r1_lift_spec_v1.md\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"p\":691,\"p2\":477481",
  ",\"lift_asserts\":{",
    "\"L1\":", JB(l1), ",\"L2\":", JB(l2), ",\"L3\":", JB(l3), ",\"L5\":", JB(l5),
    ",\"L6\":", JB(l6), ",\"L7\":", JB(l7), ",\"L8\":", JB(l8), ",\"L10\":", JB(l10),
    ",\"L11\":", JB(l11), ",\"L12\":", JB(l12), ",\"L13\":", JB(l13),
    ",\"L14_note\":\"生成性のSize計算は仕様§5により未実施(紙で確定済み・規模2.2e17)\"",
    ",\"all_pass\":", JB(allLiftOk),
  "}",
  ",\"xbar\":", MatJson(xbar), ",\"ybar\":", MatJson(ybar),
  ",\"ord_xbar\":", String(ordXbar), ",\"ord_ybar\":", String(ordYbar), ",\"N_ord\":", String(Nord),
  ",\"charming_count\":", String(Length(charmingU)), ",\"charming_count_ok\":", JB(charmingCountOk),
  ",\"prefilter\":{",
    "\"method\":\"trace(xbar^u) == trace(xbar) mod 691^2 (necessary condition for conjugacy, not proven sufficient here)\"",
    ",\"trace_xbar\":", String(Int(traceXbar)),
    ",\"survived_count\":", String(survivedCount), ",\"dropped_count\":", String(droppedCount),
    ",\"sum_check_ok\":", JB(sumCheckOk),
    ",\"survived_u_sample\":", JArr(List(survivedSample, String)),
    ",\"survived_u_sample_truncated\":", JB(Length(survivedUs) > 50),
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"prefilter_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/q3_r1_prefilter_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
