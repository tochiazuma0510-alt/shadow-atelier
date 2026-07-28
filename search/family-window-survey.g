# family-window-survey.g -- I-1 族窓観測(観測であって定理主張ではない)
#
# 実行: .\gap.ps1 search\family-window-survey.g
#
# 事前登録: provenance/registered/universe_I1_I3.md 「I-1 族窓観測」節。
# 出典: arXiv 2405.11725(dihedral poset)。P_n := Im psi_n の生成元像は
#       docs/week1-定義ノート.md §3(2405 (3.1))から逐語転記(MakeGn 内コメント参照・
#       search/suite-wp1.g の MakeGn と無変更で同一)。
#
# 対象(事前登録どおり固定・拡大縮小しない): n in {3, 5, 7, 9, 11}
# 較正ゲート(事前登録): assert |P_n| = 4n^3(n=3 で 108)。fail なら当該 n を UNKNOWN
#   として記録し、次の n へ進む(全体を中断しない)。
# 列挙述語(事前固定):
#   (1) [P_n : H] = 2n
#   (2) N_{P_n}(H) = H (自己正規化)
#   (3) <X_n> (X_n = 正典の x̄ = (r,s,s)) が P_n/H 上推移的
# 記録する観測量: 該当 H の個数・P_n-共役類の数と各類のサイズ・各類代表の生成系。
#
# 実装上の工夫(証明書に記録):
#   部分群格子全体(LatticeSubgroups)は n=11 (|P_n|=5324) で重くなり得るため、
#   P_n が可解であることを利用し SubgroupsSolvableGroup で軽量に列挙する。
#   ただし GAP 4.16.0 では SubgroupsSolvableGroup の IndexEqual/OrderEqual オプション
#   キーワードは(検証済み)フィルタとして機能せず全部分群を返すため、Size による
#   事後フィルタを併用する(この事実を scratchpad で確認済み・本スクリプトのコメントに記録)。
#   自己正規化 (2) が成り立つ代表は N_{P_n}(H)=H よりその P_n-共役類のサイズが
#   ちょうど [P_n:H]=2n であることが保証されるので、RightTransversal で厳密に
#   2n 個の共役を展開してから各共役について (3) を個別に検査する
#   (条件(3)は X_n を固定するため共役不変ではない — 共役類内で一部だけ通ることがある)。
#
# 規律: 宇宙は事前登録どおり固定。u・c 平方類・ĉ_μ には触れない。観測の解釈はしない。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;   # JB/WriteFile 等の共通ヘルパー(gaplib/v1・新規スクリプト規約)

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

# ------------------------------------------------------------------
# MakeDn / MakeGn -- search/suite-wp1.g より再利用(無変更でコピー)
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
  tmp := "search/.tmp_sha256_out_i1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

universe := [3, 5, 7, 9, 11];;
Print("宇宙 (事前登録どおり固定): ", universe, "\n");

resultsPerN := [];;   # JSON 組立用: 各 n の rec を格納

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
    Print("目標: [P_n:H]=", twoN, " すなわち |H|=", targetOrder, "\n");

    repsAll := SubgroupsSolvableGroup(Pn);;
    t1 := Runtime();;
    repsFiltered := Filtered(repsAll, H -> Size(H) = targetOrder);;
    t2 := Runtime();;
    Print("SubgroupsSolvableGroup: 全代表 ", Length(repsAll), " 件 (", t1-t0, "ms)、",
          "位数 ", targetOrder, " の代表 ", Length(repsFiltered), " 件へ事後フィルタ (",
          t2-t1, "ms)\n");

    # 各代表クラスについて: (2) 自己正規化を判定 → 自己正規化なら P_n-共役類を
    # 厳密に 2n 個展開 → 各共役について (3) 推移性を判定
    classRecords := [];;   # 自己正規化クラスごとの詳細記録
    totalSelfNormConjugates := 0;;
    totalPassing := 0;;

    for H0 in repsFiltered do
      Nz := Normalizer(Pn, H0);;
      selfNorm := (Size(Nz) = Size(H0));;
      if selfNorm then
        T := RightTransversal(Pn, Nz);;
        conjs := List(T, t -> H0^t);;
        classFullSize := Length(conjs);;   # = 2n の想定(自己正規化ゆえ)
        okClassSize := (classFullSize = twoN);;
        passingInClass := 0;;
        passingGens := [];;
        for H in conjs do
          totalSelfNormConjugates := totalSelfNormConjugates + 1;
          phi := FactorCosetAction(Pn, H);;
          xim := Image(phi, gn.x);;
          orb := Orbit(Group(xim), 1);;
          transitive := (Length(orb) = twoN);;
          if transitive then
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

    t3 := Runtime();;

    # 「該当 H(条件①②③の全てを満たす）」の P_n-共役類構造:
    # 自己正規化クラス内で「通った成分」だけを取り出すと、それらは互いに(同一の
    # 自己正規化クラスに属する限り)P_n 内で共役であるため、passing_in_class > 0 の
    # クラスの個数が「該当 H の P_n-共役類の数」、その passing_in_class が「類のサイズ」
    # となる(条件③は共役不変ではないため、フルサイズ 2n の一部だけが該当し得る)。
    qualifyingClasses := Filtered(classRecords, r -> r.passing_in_class > 0);;

    Print("自己正規化な代表クラス数(条件①②を満たす代表): ", Length(classRecords), "\n");
    Print("自己正規化な共役(実個体)総数: ", totalSelfNormConjugates, "\n");
    Print("条件①②③すべてを満たす H の個数: ", totalPassing, "\n");
    Print("該当 H が属する P_n-共役類の数(passing_in_class>0 のクラス数): ",
          Length(qualifyingClasses), "\n");
    Print("各該当共役類のサイズ(該当 H の個数のみ・フルサイズ ", twoN, " のうちの内訳):\n");
    for i in [1..Length(qualifyingClasses)] do
      Print("  類 ", i, ": フル共役類サイズ=", qualifyingClasses[i].class_full_size,
            " のうち該当 ", qualifyingClasses[i].passing_in_class, " 個  代表生成系=",
            qualifyingClasses[i].representative_generators, "\n");
    od;

    hyp4n := 4*n;;
    Print("事前登録した観測仮説(該当個数=4n=", hyp4n, "): 実測=", totalPassing,
          "  一致=", PF(totalPassing = hyp4n), "\n");
    if n = 3 then
      Print("n=3 較正(既知値 12): 実測=", totalPassing, "  一致=", PF(totalPassing = 12), "\n");
    fi;

    elapsedMs := t3 - t0;;
    Print("経過時間(このn): ", elapsedMs, "ms\n");

    Add(resultsPerN, rec(
      n := n,
      calibration_pass := true,
      status := "OBSERVED",
      pn_size := sz,
      target_index := twoN,
      target_H_order := targetOrder,
      self_normalizing_rep_class_count := Length(classRecords),
      self_normalizing_conjugate_total := totalSelfNormConjugates,
      passing_H_count := totalPassing,
      qualifying_conjugacy_class_count := Length(qualifyingClasses),
      qualifying_classes := qualifyingClasses,
      hypothesis_4n := hyp4n,
      hypothesis_matches := (totalPassing = hyp4n),
      elapsed_cpu_ms := elapsedMs
    ));
  fi;
od;

# ####################################################################
# 総括表
# ####################################################################
Print("\n############################################################\n");
Print("# 総括表\n");
Print("############################################################\n");
Print("n | |P_n| assert | 個数 | 4n仮説 | 一致 | 該当共役類数\n");
for r in resultsPerN do
  if r.status = "UNKNOWN" then
    Print(r.n, " | FAIL(UNKNOWN) | - | - | - | -\n");
  else
    Print(r.n, " | PASS | ", r.passing_H_count, " | ", r.hypothesis_4n, " | ",
          PF(r.hypothesis_matches), " | ", r.qualifying_conjugacy_class_count, "\n");
  fi;
od;

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
      ",\"target_index_2n\":", String(r.target_index),
      ",\"target_H_order\":", String(r.target_H_order),
      ",\"self_normalizing_rep_class_count\":", String(r.self_normalizing_rep_class_count),
      ",\"self_normalizing_conjugate_total\":", String(r.self_normalizing_conjugate_total),
      ",\"passing_H_count\":", String(r.passing_H_count),
      ",\"qualifying_conjugacy_class_count\":", String(r.qualifying_conjugacy_class_count),
      ",\"qualifying_classes\":", QualClassesToJson(r.qualifying_classes),
      ",\"hypothesis_4n\":", String(r.hypothesis_4n),
      ",\"hypothesis_matches\":", JB(r.hypothesis_matches),
      ",\"elapsed_cpu_ms\":", String(r.elapsed_cpu_ms), "}"
    );
  fi;
end;;

perNParts := [];;
for r in resultsPerN do
  Add(perNParts, PerNToJson(r));
od;

scriptSha256 := ComputeSha256File("search/family-window-survey.g");;
universeDocSha256 := ComputeSha256File("provenance/registered/universe_I1_I3.md");;

cert := Concatenation(
  "{\"schema\":\"i1-family-window-survey/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/family-window-survey.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":[3,5,7,9,11]",
  ",\"predicates\":{\"p1\":\"[P_n:H]=2n\",\"p2\":\"N_Pn(H)=H\",\"p3\":\"<X_n> transitive on P_n/H\"}",
  ",\"implementation_note\":\"SubgroupsSolvableGroup の IndexEqual/OrderEqual オプションは",
  " GAP 4.16.0 でフィルタとして機能しない(実測確認済み)ため Size による事後フィルタを併用。",
  " 条件(3)は共役不変でないため自己正規化クラスを RightTransversal で厳密展開し個体ごとに検査。\"",
  ",\"results\":[", JoinStringsWithSeparator(perNParts, ","), "]",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
  ",\"universe_doc_sha256\":\"", universeDocSha256, "\"",
  ",\"universe_doc_path\":\"provenance/registered/universe_I1_I3.md\"}",
  "}"
);;

outPath := "search/certs/i1_survey_20260728.json";;
WriteFile(outPath, cert);;   # WriteFile は生バイト書出し(PrintTo/OutputTextFile は
                              # 長い行を "\<改行>" で折り返し JSON を破壊するため不使用)
Print("\n証明書を書き出した: ", outPath, "\n");

Print("\nI1 SURVEY DONE\n");
QUIT;
