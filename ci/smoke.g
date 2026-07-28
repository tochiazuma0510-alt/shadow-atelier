# ci/smoke.g — Actions 工場の煙試験: GAP 版数・lins API の確認+B3 の極小列挙
# 主張なし(サイズ測定と API 発見のみ)。出力は ci/out/smoke.json。

out := rec();;
out.gap_version := GAPInfo.Version;;
out.arch := GAPInfo.Architecture;;

lins_ok := LoadPackage("lins");;
out.lins_loaded := lins_ok = true;;
out.lins_version := "unknown";;
if IsBound(GAPInfo.PackagesLoaded.lins) then
  out.lins_version := GAPInfo.PackagesLoaded.lins[2];;
fi;

cand := Filtered(["LowIndexNormalSubgroupsSearch","LowIndexNormalSubgroupsSearchForAll",
                  "LowIndexNormalSubs","LinsSearch"], IsBoundGlobal);;
out.lins_api := cand;;

f := FreeGroup("a","b");;
b3 := f / [ f.1*f.2*f.1*(f.2*f.1*f.2)^-1 ];;

out.search := "not-run";;
if "LowIndexNormalSubgroupsSearch" in cand then
  r := CALL_WITH_CATCH(function()
    local gr, lst;
    gr := ValueGlobal("LowIndexNormalSubgroupsSearch")(b3, 24);
    lst := ValueGlobal("List")(gr);
    return Length(lst);
  end, []);;
  if r[1] = true then
    out.search := Concatenation("count_le_24=", String(r[2]));;
  else
    out.search := "api-shape-differs (see log)";;
    Print("raw result probe follows:\n");
    gr := ValueGlobal("LowIndexNormalSubgroupsSearch")(b3, 24);;
    Print(gr, "\n");
  fi;
fi;

s := Concatenation("{\"gap_version\":\"", out.gap_version,
  "\",\"lins_loaded\":", String(out.lins_loaded),
  ",\"lins_version\":\"", String(out.lins_version),
  "\",\"lins_api\":\"", JoinStringsWithSeparator(out.lins_api, ","),
  "\",\"search\":\"", out.search, "\"}\n");;
PrintTo("ci/out/smoke.json", s);
Print("SMOKE: ", s);
QUIT_GAP(0);
