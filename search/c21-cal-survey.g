# search/c21-cal-survey.g -- n=21 較正 survey (裁定208 発注)
#
# 実行: .\gap.ps1 search\c21-cal-survey.g
#
# 発注: 司令塔(実装担当への指示・裁定208 C-21較正)。
# 正本:
#   docs/notes/hfun_functoriality_v1.md -- H_n^fun = H_{2,1,0} = <a2, a1*a3, q2> (1.1)、
#                                           命題 HF-1(a-d)(一般奇 n での |H|=2n^2, [P:H]=2n,
#                                           ord(X)=2n, <X>∩H=1, N(H)=H の証明)。
#   sol/sol_reply_73_math.md Q1.1        -- P_n = A_n rtimes Q の座標辞書。
#   search/k9-package.g                  -- 同型の BuildPn(n) 実装(n=9 版)の一般化(無変更コピー)。
#   search/family-window-survey.g        -- 述語 ①[P:H]=2n ②N(H)=H ③<X>推移 の good-H 悉皆列挙
#                                           (同一述語をここでも使う)。
#
# 対象(事前登録どおり固定): n = 21 のみ。
#
# 規律(厳守・発注書より):
#   - 予言値をスクリプトに書かない・docs/notes/c21_draft_v1.md を読まない(接触遮断)。
#   - sanity assert は |P_n|=4n^3 の一般式のみ可。
#   - 解釈しない・観測の記録に徹する。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

Print("############################################################\n");
Print("# c21-cal-survey.g -- n=21 P_21 / H_{2,1,0} 較正窓 survey\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# BuildPn(n) -- search/k9-package.g より一般化(無変更コピー・n を汎化しただけ)
# ====================================================================
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("BuildPn: D_n relations failed for n = ", n);
  fi;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  # X = a1 q1 (直接構成、ブロックを共有しないため素朴な積で正しい)
  # Y = a1 a2 a3 q2 の paper-word は MakeGn 慣例では tr(s*r,1)*tr(r,2)*tr(s*r,3) にあたる
  # (k9-package.g のコメント参照)。今回は X のみ測るので Y は MakeGn 慣例直接構成で作る。
  X := a1 * q1;;
  Y := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y,
             G:=Group(a1, a2, a3, q1, q2));
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

n := 21;;
Print("宇宙(事前登録どおり固定): n = ", n, "\n");

P21 := BuildPn(n);;

# ---- 量1: |G_21| ----
sz21 := Size(P21.G);;
okSize21 := (sz21 = expectedSize(n));;
Print("[", PF(okSize21), "] |G_21| = ", sz21, " (sanity: 4n^3 = ", expectedSize(n), ")\n");

# ---- H_{2,1,0} = <a2, a1*a3, q2> ----
H := Group(P21.a2, P21.a1*P21.a3, P21.q2);;

# ---- 量2: |H_{2,1,0}| ----
sizeH := Size(H);;
Print("[量2] |H_{2,1,0}| = ", sizeH, "\n");

# ---- 量3: [G_21:H] ----
idxH := sz21 / sizeH;;
Print("[量3] [G_21:H] = ", idxH, "\n");

# ---- 量4: ord(X_21)  (X = a1 q1) ----
ordX := Order(P21.X);;
Print("[量4] ord(X_21) = ", ordX, "\n");

# ---- 量5: |<X> ∩ H| ----
XX := Group(P21.X);;
interXH := Intersection(XX, H);;
sizeInterXH := Size(interXH);;
Print("[量5] |<X>∩H| = ", sizeInterXH, "\n");

# ---- 量6: N_G(H) = H ? ----
NgH := Normalizer(P21.G, H);;
selfNorm := (Size(NgH) = Size(H));;
Print("[量6] N_G(H) = H : ", selfNorm, " (|N_G(H)|=", Size(NgH), ", |H|=", Size(H), ")\n");

# ---- 量8: ordered passport (X, Y, Z=(XY)^-1 の cycle passport on G/H) ----
PassportOf := function(perm, deg)
  local lens, coll;
  lens := List([1..deg], i -> CycleLength(perm, i));
  coll := Collected(lens);
  return List(coll, e -> [e[1], e[2]/e[1]]);
end;;

phiAction := FactorCosetAction(P21.G, H);;
Ximg := Image(phiAction, P21.X);;
Yimg := Image(phiAction, P21.Y);;
Zimg := (Ximg * Yimg)^-1;;
transitiveX := (Length(Orbit(Group(Ximg), 1)) = idxH);;
passX := PassportOf(Ximg, idxH);;
passY := PassportOf(Yimg, idxH);;
passZ := PassportOf(Zimg, idxH);;
Print("[量8] <X> が G/H 上推移的: ", transitiveX, " (軌道長=", Length(Orbit(Group(Ximg), 1)), " / ", idxH, ")\n");
Print("[量8] passport(X) = ", passX, "\n");
Print("[量8] passport(Y) = ", passY, "\n");
Print("[量8] passport(Z) = ", passZ, "\n");

t1 := GAPLIB_WallElapsedMs();;
Print("経過(タスク1-6,8): ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 量7: good H の個数と共役類数(family-window-survey.g と同一述語)
#   ①[P:H]=2n ②N(H)=H ③<X>推移 の悉皆(P_21 の可解性を利用し
#   SubgroupsSolvableGroup で位数 sz21/2n の代表を列挙、Size で事後フィルタ)
# ====================================================================
Print("\n############################################################\n");
Print("# 量7: good H の悉皆(述語①②③、family-window-survey.g と同一)\n");
Print("############################################################\n");

twoN := 2*n;;
targetOrder := sz21 / twoN;;
Print("目標: [P_21:H]=", twoN, " すなわち |H|=", targetOrder, "\n");

t2a := GAPLIB_WallElapsedMs();;
repsAll := SubgroupsSolvableGroup(P21.G);;
t2b := GAPLIB_WallElapsedMs();;
repsFiltered := Filtered(repsAll, HH -> Size(HH) = targetOrder);;
t2c := GAPLIB_WallElapsedMs();;
Print("SubgroupsSolvableGroup: 全代表 ", Length(repsAll), " 件 (", (t2b-t2a)/1000.0, "s)、",
      "位数 ", targetOrder, " の代表 ", Length(repsFiltered), " 件へ事後フィルタ (",
      (t2c-t2b)/1000.0, "s)\n");

classRecords := [];;
totalSelfNormConjugates := 0;;
totalPassing := 0;;

for H0 in repsFiltered do
  Nz := Normalizer(P21.G, H0);;
  selfNormH0 := (Size(Nz) = Size(H0));;
  if selfNormH0 then
    T := RightTransversal(P21.G, Nz);;
    conjs := List(T, t -> H0^t);;
    classFullSize := Length(conjs);;
    okClassSize := (classFullSize = twoN);;
    passingInClass := 0;;
    for HC in conjs do
      totalSelfNormConjugates := totalSelfNormConjugates + 1;
      phiC := FactorCosetAction(P21.G, HC);;
      Xc := Image(phiC, P21.X);;
      orbC := Orbit(Group(Xc), 1);;
      transC := (Length(orbC) = twoN);;
      if transC then
        passingInClass := passingInClass + 1;
        totalPassing := totalPassing + 1;
      fi;
    od;
    Add(classRecords, rec(
      class_full_size := classFullSize,
      class_full_size_matches_2n := okClassSize,
      passing_in_class := passingInClass,
      representative_generators := List(GeneratorsOfGroup(H0), String)
    ));
  fi;
od;

t2d := GAPLIB_WallElapsedMs();;

qualifyingClasses := Filtered(classRecords, r -> r.passing_in_class > 0);;

Print("自己正規化な代表クラス数(条件①②を満たす代表): ", Length(classRecords), "\n");
Print("自己正規化な共役(実個体)総数: ", totalSelfNormConjugates, "\n");
Print("条件①②③すべてを満たす H の個数: ", totalPassing, "\n");
Print("該当 H が属する P_21-共役類の数: ", Length(qualifyingClasses), "\n");
for i in [1..Length(qualifyingClasses)] do
  Print("  類 ", i, ": フル共役類サイズ=", qualifyingClasses[i].class_full_size,
        " のうち該当 ", qualifyingClasses[i].passing_in_class, " 個  代表生成系=",
        qualifyingClasses[i].representative_generators, "\n");
od;
Print("量7 探索 経過: ", (t2d-t2c)/1000.0, " s\n");

# H_{2,1,0} 自身がこの悉皆に含まれるか(整合性チェック・観測のみ、解釈しない)
hIsSelfNorm := selfNorm;;
hIsTransitive := transitiveX;;
Print("参考(整合性チェック): H_{2,1,0} 自身は selfNorm=", hIsSelfNorm,
      " transitive(X)=", hIsTransitive, "\n");

t3 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計・全体): ", (t3-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_c21.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

PassportToJson := function(p)
  local parts, e;
  parts := [];
  for e in p do
    Add(parts, JPair(e[1], e[2]));
  od;
  return JArr(parts);
end;;

GensToJsonArr := function(gensStrings)
  local parts, g;
  parts := [];
  for g in gensStrings do
    Add(parts, JStr(g));
  od;
  return JArr(parts);
end;;

QualClassesToJson := function(qcList)
  local parts, r;
  parts := [];
  for r in qcList do
    Add(parts, Concatenation(
      "{\"class_full_size\":", String(r.class_full_size),
      ",\"class_full_size_matches_2n\":", JB(r.class_full_size_matches_2n),
      ",\"passing_in_class\":", String(r.passing_in_class),
      ",\"representative_generators\":", GensToJsonArr(r.representative_generators), "}"
    ));
  od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/c21-cal-survey.g");;

cert := Concatenation(
  "{\"schema\":\"c21-cal-survey/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/c21-cal-survey.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n\":21}",
  ",\"q1_pn_size\":", String(sz21),
  ",\"q1_pn_size_sanity_expected\":", String(expectedSize(n)),
  ",\"q1_pn_size_sanity_pass\":", JB(okSize21),
  ",\"q2_h210_size\":", String(sizeH),
  ",\"q3_index\":", String(idxH),
  ",\"q4_ord_X\":", String(ordX),
  ",\"q5_size_X_cap_H\":", String(sizeInterXH),
  ",\"q6_normalizer_eq_H\":", JB(selfNorm),
  ",\"q6_normalizer_size\":", String(Size(NgH)),
  ",\"q8_transitive_X_on_G_over_H\":", JB(transitiveX),
  ",\"q8_orbit_length_X\":", String(Length(Orbit(Group(Ximg), 1))),
  ",\"q8_passport_X\":", PassportToJson(passX),
  ",\"q8_passport_Y\":", PassportToJson(passY),
  ",\"q8_passport_Z\":", PassportToJson(passZ),
  ",\"q7_good_H_survey\":{",
    "\"predicate_1\":\"[P_21:H]=2n=42\"",
    ",\"predicate_2\":\"N_P21(H)=H\"",
    ",\"predicate_3\":\"<X_21> transitive on P_21/H\"",
    ",\"target_H_order\":", String(targetOrder),
    ",\"subgroups_solvable_group_total_reps\":", String(Length(repsAll)),
    ",\"order_filtered_reps\":", String(Length(repsFiltered)),
    ",\"self_normalizing_rep_class_count\":", String(Length(classRecords)),
    ",\"self_normalizing_conjugate_total\":", String(totalSelfNormConjugates),
    ",\"passing_H_count\":", String(totalPassing),
    ",\"qualifying_conjugacy_class_count\":", String(Length(qualifyingClasses)),
    ",\"qualifying_classes\":", QualClassesToJson(qualifyingClasses),
    ",\"h210_included_check\":{\"self_normalizing\":", JB(hIsSelfNorm),
      ",\"transitive\":", JB(hIsTransitive), "}",
  "}",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
  ",\"elapsed_wall_ms\":", String(t3-t0), "}",
  "}"
);;

outPath := "search/certs/c21_cal_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nC21-CAL-SURVEY DONE\n");
QUIT;
