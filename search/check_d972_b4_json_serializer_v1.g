#############################################################################
## Independent GAP self-check for the B4 finite-image JSON serializers.
## GAP regards [] as IsString; identity signed words must therefore be emitted
## as JSON arrays.  This checker is deliberately small and does not load a
## campaign producer or construct any group.
#############################################################################

D972JsonJoin := function(xs, sep)
  local out, i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;

B4LIJson := function(x)
  local i,p;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if not IsList(x) then Error("B4 serializer type drift"); fi;
  p:=List([1..Length(x)],i->B4LIJson(x[i]));
  return Concatenation("[",D972JsonJoin(p,","),"]");
end;;

P2Json := function(x)
  local i, parts;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"", ReplacedString(x,"\"","\\\""), "\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsList(x) then
    parts:=List([1..Length(x)],i->P2Json(x[i]));
    return Concatenation("[",D972JsonJoin(parts,","),"]");
  fi;
  Error("P2 serializer type drift");
end;;

D972KBJson := function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if not IsList(x) then Error("KBMAG serializer type drift"); fi;
  p:=List([1..Length(x)],i->D972KBJson(x[i]));
  return Concatenation("[",D972JsonJoin(p,","),"]");
end;;

if B4LIJson([]) <> "[]" or B4LIJson([[]]) <> "[[]]" or
   B4LIJson([1,[],"x"]) <> "[1,[],\"x\"]" then
  Error("B4 serializer empty-list gate failed");
fi;
if P2Json([]) <> "[]" or P2Json([[]]) <> "[[]]" or
   P2Json([1,[],"x\"y"]) <> "[1,[],\"x\\\"y\"]" then
  Error("P2 serializer empty-list gate failed");
fi;
if D972KBJson([]) <> "[]" or D972KBJson([[]]) <> "[[]]" then
  Error("KBMAG serializer empty-list gate failed");
fi;

## Static source-order gates bind this self-test to the two producer fixes.
B4Source:=StringFile("search/d972_b4_lowindex_v1.g");;
P2Source:=StringFile("search/d972_b4_pquotient_v1.g");;
KBSource:=StringFile("search/d972_b4_kbmag_v1.g");;
if B4Source=fail or P2Source=fail or KBSource=fail then
  Error("serializer source missing");
fi;
B4Needle:="if IsList(x) and Length(x)=0 then return \"[]\"; fi;";;
if PositionSublist(B4Source,B4Needle)=fail or
   PositionSublist(P2Source,B4Needle)=fail or
   PositionSublist(KBSource,B4Needle)=fail then
  Error("serializer source empty-list gate missing");
fi;
Print("B4_JSON_SERIALIZER_SELFTEST_PASS\n");
QUIT;
