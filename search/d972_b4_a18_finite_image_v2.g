#############################################################################
## d972_b4_a18_finite_image_v2.g
##
## Versioned fail-closed adapter for the v1 raw-A.18 finite-image producer.
## v1 is SHA-pinned and never overwritten.  The adapter materializes a
## byte-faithful ci/out copy with exactly one replacement: the D-tilde norms
## digest uses a dedicated list-of-signed-word JSON serializer.  GAP's
## IsString([])=true means the generic v1 serializer is not safe for an empty
## word; the dedicated serializer distinguishes the required word grammar.
#############################################################################

if LoadPackage("json")<>true then Error("A18 finite v2: JSON package unavailable"); fi;;

D972A18FV2Source:="search/d972_b4_a18_finite_image_v1.g";;
D972A18FV2SourceSha:="f76571a14580bf27639677d7fa171e8e8f852f636cbf4c841ff2cbfde548af08";;
D972A18FV2Temp:="ci/out/d972_b4_a18_finite_image_v2_patched.g";;
D972A18FV2Needle:="if Length(norms)<>972 or HexSHA256(D972A18FJson(norms))<>D972A18FDtildeSha then";;
D972A18FV2Replacement:="if Length(norms)<>972 or HexSHA256(D972A18FV2WordRowsJson(norms))<>D972A18FDtildeSha then";;
D972A18FV2DtildeSha:="32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;

D972A18FV2Join:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;;
  out:=xs[1];;
  if Length(xs)>1 then
    for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  fi;
  return out;
end;;

## This serializer accepts only the signed-word grammar used by norms.
## Empty [] is intentionally handled before any IsString-sensitive generic
## serializer.  A nonempty string cannot pass the signed-integer checks.
D972A18FV2WordJson:=function(word)
  local parts,i,x;
  if not IsList(word) then Error("A18 finite v2 word is not a list"); fi;;
  for x in word do
    if not IsInt(x) or x=0 then Error("A18 finite v2 signed-word type drift"); fi;
  od;
  if Length(word)=0 then return "[]"; fi;;
  parts:=List([1..Length(word)],i->String(word[i]));;
  return Concatenation("[",D972A18FV2Join(parts,","),"]");
end;;

D972A18FV2WordRowsJson:=function(rows)
  local parts,i;
  if not IsList(rows) then Error("A18 finite v2 word rows are not a list"); fi;
  parts:=List([1..Length(rows)],i->D972A18FV2WordJson(rows[i]));;
  return Concatenation("[",D972A18FV2Join(parts,","),"]");
end;;

## Static/selftest gate for the exact root cause and canonical fixture.
if not IsString([]) then Error("A18 finite v2 IsString([]) probe drift"); fi;;
if D972A18FV2WordJson([])<>"[]" or
   D972A18FV2WordJson([-1,2])<>"[-1,2]" or
   D972A18FV2WordRowsJson([[],[-1,2]])<>"[[],[-1,2]]" or
   HexSHA256(D972A18FV2WordRowsJson([[],[-1,2]]))<>
     "35de003eb84224aa2e5318dcd8ff125d9833ac5850b48b4367b224d82b1eb5eb" then
  Error("A18 finite v2 signed-word serializer selftest drift");
fi;;
Print("D972_B4_A18_FINITE_IMAGE_V2_SERIALIZER_SELFTEST_PASS empty=[] nonempty=[-1,2]\n");

D972A18FV2SourceRaw:=StringFile(D972A18FV2Source);;
if D972A18FV2SourceRaw=fail or HexSHA256(D972A18FV2SourceRaw)<>D972A18FV2SourceSha then
  Error("A18 finite v2 pinned v1 source SHA drift");
fi;;
D972A18FV2Pos:=PositionSublist(D972A18FV2SourceRaw,D972A18FV2Needle);;
if D972A18FV2Pos=fail then Error("A18 finite v2 norms digest needle missing"); fi;;
D972A18FV2TailPos:=PositionSublist(
  D972A18FV2SourceRaw{[D972A18FV2Pos+Length(D972A18FV2Needle)..Length(D972A18FV2SourceRaw)]},
  D972A18FV2Needle);;
if D972A18FV2TailPos<>fail then
  Error("A18 finite v2 norms digest needle is not unique");
fi;;
D972A18FV2Prefix:=D972A18FV2SourceRaw{[1..D972A18FV2Pos-1]};;
D972A18FV2Suffix:=D972A18FV2SourceRaw{[D972A18FV2Pos+Length(D972A18FV2Needle)..Length(D972A18FV2SourceRaw)]};;
D972A18FV2Patched:=Concatenation(D972A18FV2Prefix,
  D972A18FV2Replacement,D972A18FV2Suffix);;

FileString(D972A18FV2Temp,D972A18FV2Patched);;
D972A18FV2TempRaw:=StringFile(D972A18FV2Temp);;
if D972A18FV2TempRaw=fail or
   D972A18FV2TempRaw<>D972A18FV2Patched or
   PositionSublist(D972A18FV2TempRaw,D972A18FV2Replacement)=fail or
   PositionSublist(D972A18FV2TempRaw,D972A18FV2Needle)<>fail then
  Error("A18 finite v2 patched temp materialization drift");
fi;;
if HexSHA256(D972A18FV2TempRaw)=D972A18FV2SourceSha then
  Error("A18 finite v2 patched temp unexpectedly equals v1");
fi;;
Print("D972_B4_A18_FINITE_IMAGE_V2_PATCH_PASS source_sha256=",
  D972A18FV2SourceSha," temp=",D972A18FV2Temp," dtilde_sha256=",
  D972A18FV2DtildeSha,"\n");

Read(D972A18FV2Temp);;
Print("D972_B4_A18_FINITE_IMAGE_V2_FINAL_MARKER status=PASS source_sha256=",
  D972A18FV2SourceSha," temp=",D972A18FV2Temp,"\n");
