#############################################################################
## Exact D972 shadow power/order spectrum v3.
##
## v3 keeps the audited construction but binds every GAP source read by the
## worker, and publishes the square/cube maps and exponent.
#############################################################################

Read("search/d972_dovetail_core_v2.g");;

## The workflow binds these globals before Read().  GAP 4.12 has no
## dependable environment lookup interface, so an absent binding is the only case
## where a deterministic default is permitted.
if IsBound(D972_POWER_MODE) then
  DPS3Mode := D972_POWER_MODE;
else
  DPS3Mode := "full";
fi;;
if not IsString(DPS3Mode) or not (DPS3Mode in ["selftest", "full"]) then
  Error("D972 power spectrum v3: invalid D972_POWER_MODE");
fi;;
if IsBound(D972_POWER_OUTPUT) then
  DPS3Output := D972_POWER_OUTPUT;
else
  DPS3Output := "ci/out/d972_power_spectrum_v3.json";
fi;;
if not IsString(DPS3Output) or Length(DPS3Output) = 0 then
  Error("D972 power spectrum v3: empty D972_POWER_OUTPUT");
fi;;

DPS3RuntimeManifest :=
  "{\"search/d972_dovetail_core_v2.g\":\"1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae\",\"search/probe/wac_v1/gap_output_prelude.g\":\"2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece\",\"search/gaplib_common.g\":\"f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911\",\"search/week3-battery-common.g\":\"aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998\",\"search/week3-psl-common.g\":\"e48e50d55562983415b5691d07e3d893182620b1f73b8fe35ea77815ad9695c4\"}";

DPS3JsonString := function(s)
  local t;
  t := ReplacedString(s, "\\", "\\\\");
  t := ReplacedString(t, "\"", "\\\"");
  t := ReplacedString(t, "\n", "\\n");
  t := ReplacedString(t, "\r", "\\r");
  return Concatenation("\"", t, "\"");
end;;

DPS3Write := function(s)
  local f;
  f := OutputTextFile(DPS3Output, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, Concatenation(s, "\n"));
  CloseStream(f);
end;;

DPS3PermLine := function(p, n)
  return List([1..n], i -> i^p);
end;;

DPS3IntListText := function(xs)
  return Concatenation("[", D972Join(List(xs, String), ","), "]");
end;;

DPS3Compact := function(p, fromFull, toFull)
  local compact;
  compact := Image(fromFull, p);
  if compact = fail or Image(toFull, compact) <> p then
    Error("v3 marked full/compact round trip failed");
  fi;
  return compact;
end;;

DPS3Key := function(m, p)
  return D972NFTargetKey(m,
    D972BlockRestrict(p, 0, 27),
    D972BlockRestrict(p, 27, 9));
end;;

DPS3DigestLines := function(lines)
  local z;
  if Length(lines) = 0 then z := "";
  else z := Concatenation(D972Join(lines, "\n"), "\n"); fi;
  return HexSHA256(z);
end;;

DPS3SelfTest := function()
  local p, q, id, prod;
  p := PermList([2,3,1]); q := PermList([1,3,2]);
  id := PermList([1,2,3]);
  prod := AbstractProd([p,q]);
  if prod <> q*p or AbstractProd([id,p]) <> p then
    Error("power-spectrum v3 orientation canary failed");
  fi;
  if 2*(2*1*2+1+2)+1 <> (2*1+1)*(2*2+1) mod 18 then
    Error("power-spectrum v3 cyclotomic canary failed");
  fi;
  Print("D972_POWER_SPECTRUM_V3_GAP_SELFTEST_PASS\n");
  DPS3Write("{\"schema\":\"d972-power-spectrum/v3\",\"mode\":\"selftest\",\"all_pass\":true,\"final_marker\":\"D972_POWER_SPECTRUM_V3_GAP_SELFTEST_PASS\"}");
end;;

DPS3IntDigest := function(xs)
  return HexSHA256(Concatenation(D972Join(List(xs,String),","), "\n"));
end;;

DPS3SquareClosure := function(identity, gens, table)
  local seen, queue, head, cur, gen, nxt, trace;
  seen := List([1..Length(table)], i -> false);
  seen[identity+1] := true;
  queue := [identity]; trace := []; head := 1;
  while head <= Length(queue) do
    cur := queue[head]; head := head + 1;
    for gen in gens do
      nxt := table[cur+1][gen+1];
      if not seen[nxt+1] then
        seen[nxt+1] := true;
        Add(queue, nxt);
        Add(trace, [cur, gen, nxt]);
      fi;
    od;
  od;
  return rec(members:=Set(queue), trace:=trace);
end;;

DPS3Run := function()
  local B, S, raw, keys, targetDigest, keyMap, rows, row, i, j, m1, m2,
        fullF2, toFull, fromFull, compactf, u2, f1, f2, hom, sub, g, key, pos,
        products, orders, inverses, identity, power, n, hist, histRows,
        rowLines, productLines, rowDigest, productDigest, identityKey, inv,
        canary, jsonRows, jsonProducts, jsonOrders, jsonInverses, jsonHist,
        x, y, C, targetSet, squareMap, cubeMap, exponent, squareClosure,
        squareMembers, squareTrace, squareImageSize, squareGeneratedOrder,
        squareMemberDigest, squareObservation, jsonSquareTrace;

  B := D972BuildBase(false);
  S := D972ScanCalibrationBase(B);
  ## This is the exact marked inverse of the core's compact -> full map.
  ## It is built from the pinned generators, never by block restriction or
  ## an unmarked isomorphism search.
  fullF2 := Group(B.s1^2, B.s2^2);
  toFull := GroupHomomorphismByImages(B.compact_pure, fullF2,
    [B.compact_x, B.compact_y], [B.s1^2, B.s2^2]);
  fromFull := GroupHomomorphismByImages(fullF2, B.compact_pure,
    [B.s1^2, B.s2^2], [B.compact_x, B.compact_y]);
  if toFull = fail or fromFull = fail or not IsBijective(toFull) or
     not IsBijective(fromFull) or
     Image(fromFull, B.s1^2) <> B.compact_x or
     Image(fromFull, B.s2^2) <> B.compact_y or
     Image(toFull, B.compact_x) <> B.s1^2 or
     Image(toFull, B.compact_y) <> B.s2^2 then
    Error("v3 marked full/compact isomorphism gate failed");
  fi;
  raw := S.shadows; keys := S.target_keys;
  targetSet := Set(keys);
  targetDigest := HexSHA256(Concatenation(D972Join(keys, "\n"), "\n"));
  if Length(raw) <> 972 or Length(targetSet) <> 972 or
     targetDigest <> "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" or
     not ForAll(raw, r -> r.settled) then
    Error("D972 power spectrum v3: frozen settled 972-row roof gate failed");
  fi;

  keyMap := NewDictionary("", true);
  for i in [1..Length(keys)] do AddDictionary(keyMap, keys[i], i); od;
  rows := List([1..972], i -> fail);
  for row in raw do
    pos := LookupDictionary(keyMap, row.key);
    if pos = fail or rows[pos] <> fail then Error("duplicate/missing roof key"); fi;
    compactf := DPS3Compact(row.f, fromFull, toFull);
    if DPS3Key(row.m, compactf) <> row.key then
      Error("v3 marked transport changed frozen target key");
    fi;
    rows[pos] := rec(m:=row.m, key:=row.key,
      f:=compactf, settled:=row.settled);
  od;
  if not ForAll(rows, r -> r <> fail) then Error("incomplete frozen row order"); fi;

  C := B.compact_pure; x := B.compact_x; y := B.compact_y;
  products := List([1..972], i -> List([1..972], j -> -1));
  for i in [1..972] do
    f1 := rows[i].f;
    for j in [1..972] do
      f2 := rows[j].f; m2 := rows[j].m; u2 := 2*m2+1;
      hom := GroupHomomorphismByImages(C, C, [x,y],
        [x^u2, AbstractProd([f2^-1, y^u2, f2])]);
      if hom = fail then Error("(2.55) substitution did not descend"); fi;
      sub := Image(hom, f1);
      g := AbstractProd([f2, sub]);
      m1 := (2*rows[i].m*rows[j].m + rows[i].m + rows[j].m) mod 18;
      key := DPS3Key(m1, g);
      pos := LookupDictionary(keyMap, key);
      if pos = fail then Error("shadow product left frozen v3 972-set"); fi;
      products[i][j] := pos-1;
    od;
  od;
  if not ForAll(products, r -> ForAll(r, z -> z >= 0 and z < 972)) then
    Error("shadow product closure failed");
  fi;

  identity := PositionProperty(rows, r -> r.m = 0 and r.f = One(C));
  if identity = fail then Error("shadow identity missing"); fi;
  orders := []; inverses := [];
  for i in [1..972] do
    ## GAP row/column indices are 1-based; serialized table values are 0-based.
    power := identity-1; n := 0;
    while n < 973 do
      n := n+1; power := products[power+1][i];
      if power = identity-1 then break; fi;
    od;
    if power <> identity-1 then Error("row has no finite exact order"); fi;
    Add(orders, n);
    inv := Position(products[i], identity-1);
    if inv = fail or products[inv][i] <> identity-1 then
      Error("two-sided shadow inverse gate failed");
    fi;
    Add(inverses, inv-1);
  od;

  squareMap := List([1..972], i -> products[i][i]);
  cubeMap := List([1..972], i -> products[squareMap[i]+1][i]);
  exponent := 1;
  for n in orders do exponent := Lcm(exponent, n); od;
  if not ForAll(squareMap, z -> z >= 0 and z < 972) or
     not ForAll(cubeMap, z -> z >= 0 and z < 972) then
    Error("power map range gate failed");
  fi;

  squareImageSize := Length(Set(squareMap));
  squareClosure := DPS3SquareClosure(identity-1, squareMap, products);
  squareMembers := squareClosure.members;
  squareTrace := squareClosure.trace;
  squareGeneratedOrder := Length(squareMembers);
  squareMemberDigest := DPS3IntDigest(squareMembers);
  if not (identity-1 in squareMembers) or
     Length(squareTrace) <> squareGeneratedOrder-1 then
    Error("square closure witness gate failed");
  fi;
  for i in squareMembers do
    if not (inverses[i+1] in squareMembers) then
      Error("square subgroup inverse closure failed");
    fi;
    for j in squareMembers do
      if not (products[i+1][j+1] in squareMembers) then
        Error("square subgroup product closure failed");
      fi;
    od;
  od;
  if squareGeneratedOrder = 243 then
    squareObservation := "SQUARE_GENERATED_ORDER_243";
  else
    squareObservation := Concatenation("SQUARE_GENERATED_ORDER_OTHER_",
      String(squareGeneratedOrder));
  fi;
  jsonSquareTrace := Concatenation("[",
    D972Join(List(squareTrace, t -> DPS3IntListText(t)), ","), "]");

  canary := AbstractProd([x,y]) = y*x and
    (2*(2*1*2+1+2)+1) mod 18 = ((2*1+1)*(2*2+1)) mod 18;
  if not canary then Error("orientation/virtual-cyclotomic gate failed"); fi;

  hist := Set(orders); histRows := [];
  for n in hist do Add(histRows, Concatenation("[",String(n),",",
    String(Number(orders, z -> z=n)), "]")); od;
  rowLines := List(rows, r -> Concatenation(String(r.m), "|", r.key, "|",
    DPS3IntListText(DPS3PermLine(r.f,36))));
  productLines := List(products, r -> D972Join(List(r,String), ","));
  rowDigest := DPS3DigestLines(rowLines);
  productDigest := DPS3DigestLines(productLines);
  identityKey := rows[identity].key;
  jsonRows := D972Join(List([1..972], i -> Concatenation(
    "{\"row_index\":",String(i-1),",\"m\":",String(rows[i].m),
    ",\"target_key\":",DPS3JsonString(rows[i].key),
    ",\"f\":",String(DPS3PermLine(rows[i].f,36)),
    ",\"order\":",String(orders[i]),",\"inverse_index\":",String(inverses[i]),
    ",\"settled\":true}")), ",");
  jsonProducts := D972Join(List(products, r -> Concatenation("[",D972Join(List(r,String),","),"]")), ",");
  jsonOrders := String(orders); jsonInverses := String(inverses);
  jsonHist := Concatenation("[",D972Join(histRows, ","), "]");
  DPS3Write(Concatenation(
    "{\"schema\":\"d972-power-spectrum/v3\",\"final_marker\":\"D972_POWER_SPECTRUM_V3_GAP_FINAL\"",
    ",\"status\":\"POWER_SPECTRUM_V3_COMPLETE\",\"row_count\":972",
    ",\"target_key_digest\":",DPS3JsonString(targetDigest),
    ",\"target_key_order\":",DPS3JsonString("lexicographic frozen set"),
    ",\"source_artifact\":\"search/certs/d972_b4_word_key_artifact_v1_20260816.json\"",
    ",\"source_artifact_sha256\":\"564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9\"",
    ",\"source_artifact_rows_sha256\":\"283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930\"",
    ",\"runtime_source_sha256\":",DPS3RuntimeManifest,
    ",\"semantic_roof\":\"M=K^(9) intersect N_S4 via D972BuildBase; compact degree 36\"",
    ",\"roof_order\":1469664,\"pure_quotient_order\":1469664",
    ",\"factor_roof_degrees\":[27,9],\"factor_group_orders\":[2916,504],\"factor_descent_count\":972",
    ",\"direct_product_certificate\":{\"section_factor\":\"G9\",\"section_order\":2916,\"other_order\":504,\"schreier_edge_count\":11664,\"kernel_generated_order\":504}",
    ",\"composition_source\":\"2008.00066 Prop.2.14 formulas (2.52),(2.55)\"",
    ",\"orientation_canaries\":{\"paper_product_is_gap_reverse\":true,\"lambda_product\":true,\"identity\":true}",
    ",\"associativity_method\":\"independent checker verifies generator-action composition for every pair\",\"associativity_pair_count\":945441",
    ",\"identity_index\":",String(identity-1),",\"identity_key\":",DPS3JsonString(identityKey),
    ",\"inverse_indices\":",jsonInverses,",\"orders\":",jsonOrders,
    ",\"order_histogram\":",jsonHist,
    ",\"square_map\":",String(squareMap),",\"cube_map\":",String(cubeMap),",\"exponent\":",String(exponent),
    ",\"square_generators\":",String(squareMap),
    ",\"square_image_size\":",String(squareImageSize),
    ",\"square_generated_order\":",String(squareGeneratedOrder),
    ",\"square_generated_members\":",String(squareMembers),
    ",\"square_member_digest_sha256\":",DPS3JsonString(squareMemberDigest),
    ",\"square_closure_seed\":",String(identity-1),
    ",\"square_closure_trace\":",jsonSquareTrace,
    ",\"square_observation\":",DPS3JsonString(squareObservation),
    ",\"marked_full_compact_isomorphism\":{\"source\":\"Group(B.s1^2,B.s2^2)\",\"target\":\"B.compact_pure\",\"source_generators\":[\"B.s1^2\",\"B.s2^2\"],\"target_images\":[\"B.compact_x\",\"B.compact_y\"],\"bijective\":true,\"row_round_trip_count\":972,\"block_restriction_on_full_rows\":false}",
    ",\"row_digest_sha256\":",DPS3JsonString(rowDigest),
    ",\"product_table_sha256\":",DPS3JsonString(productDigest),
    ",\"rows\":",Concatenation("[",jsonRows,"]"),
    ",\"product_table\":",Concatenation("[",jsonProducts,"]"),
    ",\"outside_label_status\":\"UNKNOWN_MISSING_AUTHENTICATED_LABEL\",\"outside_rows\":null,\"outside_order_histogram\":null,\"outside_inference_forbidden\":true}"
  ));
  Print(squareObservation,"\n");
  Print("D972_POWER_SPECTRUM_V3_GAP_FINAL\n");
  Print("status=POWER_SPECTRUM_V3_COMPLETE output=",DPS3Output,
    " square_generated_order=",String(squareGeneratedOrder),"\n");
end;;

if DPS3Mode = "selftest" then DPS3SelfTest(); else DPS3Run(); fi;;
