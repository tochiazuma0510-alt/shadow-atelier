# search/s2_3_pre_gen23_v1.g -- [S2-3-PRE] SL^pm(2,691) の (2,3)-生成 witness 探索(裁定1055/1056)
#
# 正本: docs/notes/w691_scan_gen23_spec_v1.md §3(発注 W691-GEN23)。
#
# 方法(司令塔緊急指導 + 実装係の追加最適化): 行列群のまま Size(<a,b>) を取ると汎用経路で
#   遅い(matrix Size()・GroupHomomorphismByImages+Kernel(自由群からの引き戻し)はいずれも
#   実地で低速/メモリ死と判明・下記「試行錯誤」節に記録)。
#   最終方式: 非零ベクトル F_691^2\{0} を「F_691^x の平方部分群」で割った商(1384点)への
#   作用で <a,b> を直接、置換群として構成する。P^1(692点、スカラー全体で割る)だと
#   -I が自明に作用してしまい核 {±I} の補正が別途必要になるが、-1 が 691 を法として
#   平方非剰余である(691 mod 4 = 3)ことを使うと、「平方部分群で割る」商(スカラー全体の
#   半分でしか割らない)では -I が非自明(位数2・不動点なし)に作用する ⟹ この1384点表現
#   だけで Size() が直接 |<a,b>| そのものを返す(核の別途補正が不要)。1384点の
#   Schreier-Sims は瞬時(実測 109ms)。
#
# 対象: H_2 = SL^pm(2,691) = {M in GL(2,691) : det M in {1,-1}}、位数 659,877,360。
# 手順:
#   a := g * diag(1,-1) * g^-1(g in GL(2,691) 乱択)⟹ a^2=I・det a=-1(構成保証)。
#   b := h * diag(omega,omega^-1) * h^-1(h in GL(2,691) 乱択、omega=GF(691)の原始3乗根)
#        ⟹ b^3=I・det b=1(構成保証)。
#   1384点表現で Size(Group(permA,permB)) を計算、= 659,877,360 なら陽性witness(証明終了)。
# 停止: 陽性1対で即終了・記録。2000対で打切りならUNKNOWN。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

q := 691;;
F := GF(q);;
slOrder := q*(q^2-1);;
h2Order := 2*slOrder;;
Print("q=", q, " |SL(2,691)|=", slOrder, " |H_2|=", h2Order, " (期待 329938680, 659877360)\n");
Print("(q-1)/2 = ", (q-1)/2, "  q mod 4 = ", q mod 4, " (期待 3, -1が平方非剰余)\n");

omega := fail;;
for cand in Elements(F) do
  if cand <> Zero(F) and cand^3 = One(F) and cand <> One(F) then omega := cand; break;; fi;
od;
if omega = fail then Error("no primitive cube root -- theory violated"); fi;
Print("omega = ", omega, " (omega^3=1, omega<>1: ", omega^3=One(F), ")\n");

Dmat := [[One(F), Zero(F)], [Zero(F), -One(F)]];;
Bmat := [[omega, Zero(F)], [Zero(F), omega^-1]];;

MyRandomInvertibleMat := function(F)
  local M, det;
  repeat
    M := RandomMat(2, 2, F);;
    det := DeterminantMat(M);;
  until det <> Zero(F);
  return M;;
end;;

# ---- 1384点表現(F_691^2\{0} を平方部分群で割った商) ----
euler := (q-1)/2;;
IsSquareF := function(x, F) return x^euler = One(F);; end;;

nonSq := fail;;
for cand in Elements(F) do
  if cand <> Zero(F) and not IsSquareF(cand, F) then nonSq := cand; break;; fi;
od;
if nonSq = fail then Error("no nonsquare found -- theory violated"); fi;

oneIsSquare := IsSquareF(One(F), F);;   # = true always

ClassOf := function(v, F)
  if v[2] <> Zero(F) then return [v[1]/v[2], IsSquareF(v[2], F)];;
  else return [infinity, IsSquareF(v[1], F)];; fi;;
end;;

RepOfClass := function(cls, F)
  local t, s, v;
  t := cls[1];;  s := cls[2];;
  if t = infinity then v := [One(F), Zero(F)];;
  else v := [t, One(F)];; fi;;
  if s <> oneIsSquare then v := nonSq * v;; fi;;
  return v;;
end;;

pts2 := [];;
for t in Elements(F) do
  Add(pts2, [t, true]);;
  Add(pts2, [t, false]);;
od;
Add(pts2, [infinity, true]);;
Add(pts2, [infinity, false]);;
n2 := Length(pts2);;
Print("action set size = ", n2, " (期待 1384)\n");
ptIndex2 := NewDictionary(pts2[1], true);;
for i in [1..n2] do AddDictionary(ptIndex2, pts2[i], i);; od;

MatToPerm2 := function(M, F)
  local images, i, cls, v, w, wcls, idx;
  images := [];;
  for i in [1..n2] do
    cls := pts2[i];;
    v := RepOfClass(cls, F);;
    w := [M[1][1]*v[1] + M[1][2]*v[2], M[2][1]*v[1] + M[2][2]*v[2]];;
    wcls := ClassOf(w, F);;
    idx := LookupDictionary(ptIndex2, wcls);;
    if idx = fail then Error("MatToPerm2: class not found -- bug"); fi;
    images[i] := idx;;
  od;
  return PermList(images);;
end;;

# self-check: -I must act as a nontrivial fixed-point-free involution on this 1384-point set
negI := -IdentityMat(2, F);;
permNegI := MatToPerm2(negI, F);;
negICheckOk := (permNegI <> ()) and (Order(permNegI) = 2) and (NrMovedPoints(permNegI) = n2);;
Print("[self-check] -I acts as fixed-point-free order-2 permutation: ", negICheckOk, "\n");
if not negICheckOk then
  Error("s2_3_pre_gen23_v1: -I self-check FAILED -- method assumption violated, refusing to proceed");
fi;

seed := 20260812;;
Reset(GlobalMersenneTwister, seed);;
Print("random seed = ", seed, " (GlobalMersenneTwister)\n");

MAX_TRIALS := 2000;;
witness := fail;;
t0 := GAPLIB_WallElapsedMs();;

for trial in [1..MAX_TRIALS] do
  g := MyRandomInvertibleMat(F);;
  h := MyRandomInvertibleMat(F);;
  a := g * Dmat * g^-1;;
  b := h * Bmat * h^-1;;
  aOk := (a*a = IdentityMat(2,F)) and (DeterminantMat(a) = -One(F));;
  bOk := (b*b*b = IdentityMat(2,F)) and (DeterminantMat(b) = One(F));;
  if not (aOk and bOk) then
    Error("construction guarantee violated at trial ", trial);
  fi;

  permA := MatToPerm2(a, F);;
  permB := MatToPerm2(b, F);;
  Ggrp := Group(permA, permB);;
  S := Size(Ggrp);;

  if trial <= 10 or trial mod 50 = 0 then
    Print("trial ", trial, ": Size(<a,b>) = ", S, "\n");
  fi;

  if S = h2Order then
    witness := rec(trial := trial, a := a, b := b, size := S);;
    Print("\n*** POSITIVE WITNESS: trial=", trial, " Size(<a,b>)=", S, " ***\n");
    break;;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();;
triedCount := MAX_TRIALS;;
if witness <> fail then triedCount := witness.trial;; fi;;
Print("\n試行 = ", triedCount, " / ", MAX_TRIALS, "  経過 = ", t1-t0, " ms\n");

status := "UNKNOWN_CAP_REACHED";;
if witness <> fail then status := "POSITIVE_WITNESS_FOUND"; fi;
Print("status = ", status, "\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_s23pre.txt";;
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

scriptSha256 := ComputeSha256File("search/s2_3_pre_gen23_v1.g");;

witnessJson := "null";;
if witness <> fail then
  witnessJson := Concatenation("{\"trial\":", String(witness.trial),
    ",\"a\":", MatJson(witness.a), ",\"b\":", MatJson(witness.b),
    ",\"size_verified\":", String(witness.size), "}");
fi;

cert := Concatenation(
  "{\"schema\":\"s2-3-pre-gen23/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/s2_3_pre_gen23_v1.g\",\"order\":\"裁定1055/1056 [S2-3-PRE] / docs/notes/w691_scan_gen23_spec_v1.md 3\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"q\":691,\"target_group\":\"H_2=SL^pm(2,691)\",\"target_order\":", String(h2Order),
  ",\"sl_order\":", String(slOrder),
  ",\"method\":\"action_on_1384pt_quotient_of_nonzero_vectors_by_square_scalars(detects_-I_directly)\"",
  ",\"neg_I_self_check_ok\":", JB(negICheckOk),
  ",\"random_seed\":", String(seed), ",\"random_source\":\"GlobalMersenneTwister\"",
  ",\"max_trials\":", String(MAX_TRIALS),
  ",\"status\":\"", status, "\"",
  ",\"witness\":", witnessJson,
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/s2_3_pre_gen23_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
