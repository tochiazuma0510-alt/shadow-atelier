# family-window-w5.g -- (W5) regression: Lambda(H の P_n-共役全体) の
# Phi(F_0)-安定性(Sol 便 73 Q1.5 (1.14) の紙上予言に対する GAP regression)
#
# 実行: .\gap.ps1 search\family-window-w5.g
#
# 位置づけ: これは selector 探索ではない。命題 K5-1(Phi_{0,k} = inn(X^{-2k}))
# と Sol 便 73 (1.13)(1.14) により、Phi(F_0) = inn(<X^2>) は全ての P_n-共役類を
# 保つことが紙上で示されている。本スクリプトはその「全類 PASS」という予言への
# regression チェックであり、値を見て一つの類を選ぶことはしない。
#
# 事前登録(このタスクの指示で固定・拡大縮小しない):
#   宇宙: n in {3, 5, 7, 9, 11}(family-window-survey.g / provenance/registered/
#         universe_I1_I3.md と同一の宇宙・同一の述語(1)(2)(3))。
#   検査対象 H: family-window-survey.g と同じ述語 ①[P_n:H]=2n ②N_Pn(H)=H
#         ③<X_n> が P_n/H 上推移的 を満たす H 全体(= 各 n の qualifying
#         conjugacy classes)。命題 ODD-H(Sol 便 73 Q1.2)により各類は
#         all-or-nothing である(観測でも再確認する)。
#   (W5): Lambda_n = (ある qualifying class に属する H の実個体すべて) が
#         Phi(F_0) = inn(<X^2>) の作用で安定 -- 具体的には、Lambda_n の各元 H に
#         ついて H^(X^2) がやはり Lambda_n の元であること。
#   期待: 全 n・全 qualifying class で PASS(Sol 便 73 (1.14))。
#
# 規律: 宇宙は事前登録どおり固定。u・c 平方類・c_mu には触れない。
#       observation の解釈はしない(該当有無の記録に徹する)。
#
# 実装上の注記: MakeDn/MakeGn/expectedSize は search/suite-wp1.g および
# search/family-window-survey.g と無変更で同一(逐語再掲・出典コメントも同じ)。
# qualifying class の列挙アルゴリズムも family-window-survey.g と同一(自己
# 正規化な代表 -> RightTransversal で共役 2n 個を厳密展開 -> 各共役に述語③を
# 個別判定)。本スクリプトはその出力に (W5) 判定を追加する拡張である。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

# ------------------------------------------------------------------
# MakeDn / MakeGn -- search/suite-wp1.g / family-window-survey.g より再掲(無変更)
# ------------------------------------------------------------------
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  # x̄ = (r, s, s), ȳ = (rs, r, rs)  ※ rs は「s のち r」= GAP では s*r
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_w5.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

universe := [3, 5, 7, 9, 11];;
Print("宇宙 (事前登録どおり固定): ", universe, "\n");

resultsPerN := [];;

for n in universe do
  Print("\n############################################################\n");
  Print("# n = ", n, "\n");
  Print("############################################################\n");

  gn := MakeGn(n);;
  Pn := gn.G;;
  sz := Size(Pn);;
  okSize := (sz = expectedSize(n));;
  Print("[", PF(okSize), "] |P_", n, "| = ", sz, " (期待 ", expectedSize(n), ")\n");

  if not okSize then
    Print("[UNKNOWN] n=", n, ": 較正ゲート assert |P_n|=4n^3 が FAIL。この n は UNKNOWN として次へ。\n");
    Add(resultsPerN, rec(
      n := n, calibration_pass := false, status := "UNKNOWN",
      pn_size := sz, expected_pn_size := expectedSize(n)
    ));
  else
    t0 := Runtime();;

    twoN := 2*n;;
    targetOrder := sz / twoN;;

    # Phi(F_0) = inn(<X^2>) の生成元: X^2
    Xsq := gn.x^2;;

    repsAll := SubgroupsSolvableGroup(Pn);;
    repsFiltered := Filtered(repsAll, H -> Size(H) = targetOrder);;

    classRecords := [];;   # 各自己正規化クラスの詳細(Lambda_n の候補材料)

    for H0 in repsFiltered do
      Nz := Normalizer(Pn, H0);;
      selfNorm := (Size(Nz) = Size(H0));;
      if selfNorm then
        T := RightTransversal(Pn, Nz);;
        conjs := List(T, t -> H0^t);;
        classFullSize := Length(conjs);;
        okClassSize := (classFullSize = twoN);;
        passingHs := [];;
        for H in conjs do
          phi := FactorCosetAction(Pn, H);;
          xim := Image(phi, gn.x);;
          orb := Orbit(Group(xim), 1);;
          transitive := (Length(orb) = twoN);;
          if transitive then
            Add(passingHs, H);
          fi;
        od;
        Add(classRecords, rec(
          class_full_size := classFullSize,
          class_full_size_matches_2n := okClassSize,
          passing_in_class := Length(passingHs),
          all_or_nothing := (Length(passingHs) = 0 or Length(passingHs) = classFullSize),
          passingHs := passingHs,
          representative_generators := List(GeneratorsOfGroup(H0), String)
        ));
      fi;
    od;

    qualifyingClasses := Filtered(classRecords, r -> r.passing_in_class > 0);;

    Print("qualifying classes (述語①②③すべて満たす H が属する P_n-共役類): ",
          Length(qualifyingClasses), "\n");

    # ---------------- (W5) 判定: 各 qualifying class の Lambda_n について
    #  H in Lambda_n ならば H^Xsq もまた Lambda_n の元であること(全元について)。
    w5Records := [];;
    allClassesPass := true;;
    for qc in qualifyingClasses do
      LambdaSet := qc.passingHs;;
      w5Pass := ForAll(LambdaSet, H -> ForAny(LambdaSet, Hp -> Hp = H^Xsq));;
      if not w5Pass then allClassesPass := false; fi;
      Add(w5Records, rec(
        class_full_size := qc.class_full_size,
        passing_in_class := qc.passing_in_class,
        all_or_nothing := qc.all_or_nothing,
        w5_pass := w5Pass,
        representative_generators := qc.representative_generators
      ));
      Print("  類(サイズ ", qc.class_full_size, ", 該当 ", qc.passing_in_class,
            ", all-or-nothing=", PF(qc.all_or_nothing), "): (W5) = ", PF(w5Pass), "\n");
    od;

    t3 := Runtime();;
    elapsedMs := t3 - t0;;
    Print("n=", n, " 総括: qualifying classes=", Length(qualifyingClasses),
          "  (W5) 全類一致=", PF(allClassesPass), "  経過時間=", elapsedMs, "ms\n");

    Add(resultsPerN, rec(
      n := n,
      calibration_pass := true,
      status := "OBSERVED",
      pn_size := sz,
      target_index_2n := twoN,
      target_H_order := targetOrder,
      qualifying_conjugacy_class_count := Length(qualifyingClasses),
      w5_records := w5Records,
      w5_all_classes_pass := allClassesPass,
      elapsed_cpu_ms := elapsedMs
    ));
  fi;
od;

# ####################################################################
# 総括表
# ####################################################################
Print("\n############################################################\n");
Print("# 総括表(W5 regression)\n");
Print("############################################################\n");
Print("n | 較正 | qualifying類数 | (W5)全類一致\n");
overallAllPass := true;;
for r in resultsPerN do
  if r.status = "UNKNOWN" then
    Print(r.n, " | FAIL(UNKNOWN) | - | -\n");
    overallAllPass := false;;
  else
    Print(r.n, " | PASS | ", r.qualifying_conjugacy_class_count, " | ",
          PF(r.w5_all_classes_pass), "\n");
    if not r.w5_all_classes_pass then overallAllPass := false; fi;
  fi;
od;
Print("\n総合(全 n・全 qualifying class で (W5) PASS か): ", PF(overallAllPass), "\n");

# ####################################################################
# 証明書 JSON
# ####################################################################
GensToJsonArr := function(gensStrings)
  local parts, g;
  parts := [];
  for g in gensStrings do
    Add(parts, Concatenation("\"", g, "\""));
  od;
  return Concatenation("[", JoinStringsWithSeparator(parts, ","), "]");
end;;

W5RecordsToJson := function(recList)
  local parts, r;
  parts := [];
  for r in recList do
    Add(parts, Concatenation(
      "{\"class_full_size\":", String(r.class_full_size),
      ",\"passing_in_class\":", String(r.passing_in_class),
      ",\"all_or_nothing\":", JB(r.all_or_nothing),
      ",\"w5_pass\":", JB(r.w5_pass),
      ",\"representative_generators\":", GensToJsonArr(r.representative_generators), "}"
    ));
  od;
  return Concatenation("[", JoinStringsWithSeparator(parts, ","), "]");
end;;

PerNToJson := function(r)
  if r.status = "UNKNOWN" then
    return Concatenation(
      "{\"n\":", String(r.n),
      ",\"calibration_pass\":false",
      ",\"status\":\"UNKNOWN\"",
      ",\"pn_size\":", String(r.pn_size),
      ",\"expected_pn_size\":", String(r.expected_pn_size), "}"
    );
  else
    return Concatenation(
      "{\"n\":", String(r.n),
      ",\"calibration_pass\":true",
      ",\"status\":\"OBSERVED\"",
      ",\"pn_size\":", String(r.pn_size),
      ",\"target_index_2n\":", String(r.target_index_2n),
      ",\"target_H_order\":", String(r.target_H_order),
      ",\"qualifying_conjugacy_class_count\":", String(r.qualifying_conjugacy_class_count),
      ",\"w5_records\":", W5RecordsToJson(r.w5_records),
      ",\"w5_all_classes_pass\":", JB(r.w5_all_classes_pass),
      ",\"elapsed_cpu_ms\":", String(r.elapsed_cpu_ms), "}"
    );
  fi;
end;;

perNParts := [];;
for r in resultsPerN do
  Add(perNParts, PerNToJson(r));
od;

scriptSha256 := ComputeSha256File("search/family-window-w5.g");;
universeDocSha256 := ComputeSha256File("provenance/registered/universe_I1_I3.md");;

cert := Concatenation(
  "{\"schema\":\"w5-regression/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/family-window-w5.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":[3,5,7,9,11]",
  ",\"claim_under_test\":\"(W5): Lambda_n(H の P_n-共役全体、述語(1)(2)(3)を満たすものすべて) は",
  " Phi(F_0)=inn(<X^2>) の作用で安定(命題K5-1・Sol便73(1.13)(1.14)の紙上予言の regression)\"",
  ",\"predicates\":{\"p1\":\"[P_n:H]=2n\",\"p2\":\"N_Pn(H)=H\",\"p3\":\"<X_n> transitive on P_n/H\"}",
  ",\"note\":\"selector 探索ではない。値を見て一つの類を選ぶことはしない。期待は全類PASS。\"",
  ",\"results\":[", JoinStringsWithSeparator(perNParts, ","), "]",
  ",\"overall_all_pass\":", JB(overallAllPass),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
  ",\"universe_doc_sha256\":\"", universeDocSha256, "\"",
  ",\"universe_doc_path\":\"provenance/registered/universe_I1_I3.md\"}",
  "}"
);;

outPath := "search/certs/w5_regression_20260728.json";;
WriteFile(outPath, cert);;
Print("\n証明書を書き出した: ", outPath, "\n");

Print("\nW5 REGRESSION DONE\n");
QUIT;
