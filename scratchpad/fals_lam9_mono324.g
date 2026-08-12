# falsifier: lambda_9 の passport から monodromy 群の可能な位数を悉皆で出す
# passport (r1_branch_decision_v1.md §1 / R-0 cert):
#   deg 18, branch {0,1,inf}
#   x (around 0)   : [[18,1]]        -> cycle type [18]
#   y (around 1)   : [[1,2],[2,8]]   -> cycle type [1,1,2^8]
#   z=(xy)^-1(inf) : [[18,1]]        -> cycle type [18]
#   G = <x,y> transitive on 18 points
# 問い: |G| = 324 は可能か(ノート p1d2_r1_canonicalization_v1.md §4.1 の目標値)
deg := 18;;
cyc := function(p) return SortedList(List(Cycles(p,[1..deg]), Length)); end;;
tX := [18];;
tY := [1,1,2,2,2,2,2,2,2,2];;

N := NrTransitiveGroups(deg);;
Print("NrTransitiveGroups(18) = ", N, "\n");

# まず位数 324 の推移群を列挙
c324 := [];;
sizes := [];;
for k in [1..N] do
  G := TransitiveGroup(deg,k);
  Add(sizes, Size(G));
  if Size(G) = 324 then Add(c324, k); fi;
od;
Print("degree-18 transitive groups with |G|=324 : ", c324, "\n");
Print("  (their TransitiveIdentification names: ",
      List(c324, k -> TransitiveGroup(deg,k)), ")\n");

# 悉皆掃引: |G| <= CAP の推移群すべてについて (x,y) の存在を判定
CAP := 60000;;
ok := [];;
for k in [1..N] do
  G := TransitiveGroup(deg,k);
  if Size(G) <= CAP then
    els := AsSSortedList(G);
    xs  := Filtered(els, p -> cyc(p) = tX);
    if Length(xs) > 0 then
      ys := Filtered(els, p -> cyc(p) = tY);
      if Length(ys) > 0 then
        # x は G-共役を除いて 1 本ずつでよい
        reps := [];
        for cc in ConjugacyClasses(G) do
          if cyc(Representative(cc)) = tX then Add(reps, Representative(cc)); fi;
        od;
        found := false;
        for x in reps do
          for y in ys do
            if cyc(x*y) = tX and Size(Group(x,y)) = Size(G) then
              found := true; break;
            fi;
          od;
          if found then break; fi;
        od;
        if found then
          Add(ok, [k, Size(G), TransitiveGroup(deg,k)]);
          Print("  HIT  T", k, "  |G|=", Size(G), "  ", TransitiveGroup(deg,k), "\n");
        fi;
      fi;
    fi;
  fi;
od;

Print("\n=== 掃引結果 (|G| <= ", CAP, ") ===\n");
Print("passport を実現する推移群 (T番号, 位数): ",
      List(ok, r -> [r[1], r[2]]), "\n");
Print("実現される位数の集合: ", SSortedList(List(ok, r -> r[2])), "\n");
Print("324 は実現されるか: ", 324 in List(ok, r -> r[2]), "\n");
Print("未検査(|G| > ", CAP, ")の推移群の個数: ",
      Number(sizes, s -> s > CAP), "\n");
Print("未検査の位数リスト: ", SSortedList(Filtered(sizes, s -> s > CAP)), "\n");
QUIT;
