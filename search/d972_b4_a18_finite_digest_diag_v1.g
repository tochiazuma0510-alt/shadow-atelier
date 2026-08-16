#############################################################################
## d972_b4_a18_finite_digest_diag_v1.g
##
## Independent GAP-side row diagnostic for the raw-A.18 D-tilde digest.
## This is not imported by, and does not alter, the production finite-image
## producer.  It compares all 972 reconstructed rows with a frozen Python
## fixture and stops at the first mismatch with detailed intermediate data.
##
## Intended invocation through gap-run.yml:
##   script=search/d972_b4_a18_finite_digest_diag_v1.g
##   preamble= (empty)
#############################################################################

if LoadPackage("json")<>true then Error("A18 digest diagnostic: JSON package unavailable"); fi;;

D972A18DiagInput:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972A18DiagWords:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972A18DiagFixture:="search/certs/d972_b4_a18_finite_dtilde_rows_fixture_v1_20260817.json";;
D972A18DiagSourceSha:="c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9";;
D972A18DiagWordsSha:="564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972A18DiagRelSha:="12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e";;
D972A18DiagDtildeSha:="32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef";;
D972A18DiagFixtureSha:="aab097b31c2e4a85aab28c6ebb5f3853d7b5b99ef4eb8b331a1faf6626d4bfa6";;
D972A18DiagFixtureMaxBytes:=2000000;;
D972A18DiagSchema:="d972-b4-a18-finite-dtilde-rows-fixture/v1";;

D972A18DiagJoin:=function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;;
  out:=xs[1];;
  if Length(xs)>1 then
    for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  fi;
  return out;
end;;

D972A18DiagJson:=function(x)
  local names,parts,i,key,t;
  if x=fail then return "null"; fi;;
  if x=true then return "true"; fi;;
  if x=false then return "false"; fi;;
  if IsInt(x) then return String(x); fi;;
  if IsString(x) then
    t:=ReplacedString(x,"\\","\\\\");;
    t:=ReplacedString(t,"\"","\\\"");;
    t:=ReplacedString(t,"\n","\\n");;
    t:=ReplacedString(t,"\r","\\r");;
    return Concatenation("\"",t,"\"");
  fi;
  if IsList(x) then
    if Length(x)=0 then return "[]"; fi;;
    parts:=List([1..Length(x)],i->D972A18DiagJson(x[i]));;
    return Concatenation("[",D972A18DiagJoin(parts,","),"]");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));; parts:=[];;
    for key in names do
      Add(parts,Concatenation(D972A18DiagJson(key),":",
        D972A18DiagJson(x.(key))));
    od;
    return Concatenation("{",D972A18DiagJoin(parts,","),"}");
  fi;
  Error("A18 digest diagnostic JSON type drift");
end;;

D972A18DiagReduce:=function(w)
  local out,x,n;
  out:=[];;
  for x in w do
    if not IsInt(x) or x=0 then Error("A18 digest diagnostic signed word drift"); fi;;
    n:=Length(out);;
    if n>0 and out[n]=-x then Remove(out,n); else Add(out,x); fi;
  od;
  return out;
end;;

D972A18DiagInverse:=function(w)
  return List(Reversed(w),x->-x);
end;;

D972A18DiagMarkedRaw:=function(w,a,b)
  local out,x,img;
  out:=[];;
  for x in w do
    if not IsInt(x) or (AbsInt(x)<>1 and AbsInt(x)<>4) then
      Error("A18 digest diagnostic marked alphabet drift");
    fi;
    if AbsInt(x)=1 then img:=a; else img:=b; fi;
    if x<0 then Append(out,D972A18DiagInverse(img));
    else Append(out,img); fi;
  od;
  return out;
end;;

D972A18DiagMarked:=function(w,a,b)
  return D972A18DiagReduce(D972A18DiagMarkedRaw(w,a,b));
end;;

D972A18DiagRead:=function(path,maxbytes,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail then Error("A18 digest diagnostic missing ",label,": ",path); fi;;
  if Length(raw)>maxbytes then Error("A18 digest diagnostic ",label,
    " exceeds bounded byte limit"); fi;;
  return raw;
end;;

D972A18DiagInputRaw:=D972A18DiagRead(D972A18DiagInput,10000000,"input");;
if HexSHA256(D972A18DiagInputRaw)<>D972A18DiagSourceSha then
  Error("A18 digest diagnostic source SHA drift");
fi;;
D972A18DiagInputObj:=JsonStringToGap(D972A18DiagInputRaw);;
if D972A18DiagInputObj=fail or
   D972A18DiagInputObj.schema<>"d972-b4-p2-magnus-input/v2" or
   D972A18DiagInputObj.relator_count<>158 or
   Length(D972A18DiagInputObj.all_relators)<>158 or
   D972A18DiagInputObj.all_relators_sha256<>D972A18DiagRelSha or
   HexSHA256(D972A18DiagJson(D972A18DiagInputObj.all_relators))<>D972A18DiagRelSha then
  Error("A18 digest diagnostic source contract drift");
fi;;

D972A18DiagWordsRaw:=D972A18DiagRead(D972A18DiagWords,10000000,"word artifact");;
if HexSHA256(D972A18DiagWordsRaw)<>D972A18DiagWordsSha then
  Error("A18 digest diagnostic word-artifact SHA drift");
fi;;
D972A18DiagWordsObj:=JsonStringToGap(D972A18DiagWordsRaw);;
if D972A18DiagWordsObj=fail or
   D972A18DiagWordsObj.schema<>"d972-b4-word-key-artifact/v1" or
   D972A18DiagWordsObj.count<>972 or Length(D972A18DiagWordsObj.rows)<>972 then
  Error("A18 digest diagnostic word-artifact contract drift");
fi;;

D972A18DiagFixtureRaw:=D972A18DiagRead(D972A18DiagFixture,
  D972A18DiagFixtureMaxBytes,"fixture");;
if HexSHA256(D972A18DiagFixtureRaw)<>D972A18DiagFixtureSha then
  Error("A18 digest diagnostic fixture SHA drift");
fi;;
D972A18DiagFixtureObj:=JsonStringToGap(D972A18DiagFixtureRaw);;
if D972A18DiagFixtureObj=fail or
   D972A18DiagFixtureObj.schema<>D972A18DiagSchema or
   D972A18DiagFixtureObj.source_sha256<>D972A18DiagSourceSha or
   D972A18DiagFixtureObj.word_artifact_sha256<>D972A18DiagWordsSha or
   D972A18DiagFixtureObj.dtilde_sha256<>D972A18DiagDtildeSha or
   D972A18DiagFixtureObj.row_count<>972 or
   Length(D972A18DiagFixtureObj.rows)<>972 then
  Error("A18 digest diagnostic fixture contract drift");
fi;;

## Validate the frozen fixture before using it as an oracle.
for D972A18DiagI in [1..972] do
  D972A18DiagExpected:=D972A18DiagFixtureObj.rows[D972A18DiagI];;
  if not IsRecord(D972A18DiagExpected) or
     D972A18DiagExpected.index<>D972A18DiagI or
     not IsList(D972A18DiagExpected.word) or
     D972A18DiagExpected.sha256<>
       HexSHA256(D972A18DiagJson(D972A18DiagExpected.word)) then
    Error("A18 digest diagnostic frozen fixture row contract drift at row ",
      D972A18DiagI);
  fi;
od;;

D972A18DiagNorms:=[];;
for D972A18DiagI in [1..972] do
  D972A18DiagSourceRow:=D972A18DiagWordsObj.rows[D972A18DiagI];;
  if not IsList(D972A18DiagSourceRow) or Length(D972A18DiagSourceRow)<>3 then
    Error("A18 digest diagnostic source row shape drift at row ",D972A18DiagI);
  fi;
  D972A18DiagF2:=D972A18DiagSourceRow[3];;
  if D972A18DiagF2="" then D972A18DiagF2:=[]; fi;;
  if not IsList(D972A18DiagF2) then
    Error("A18 digest diagnostic source F2 type drift at row ",D972A18DiagI);
  fi;
  D972A18DiagMapped:=[];;
  for D972A18DiagX in D972A18DiagF2 do
    if not IsInt(D972A18DiagX) or
       (AbsInt(D972A18DiagX)<>1 and AbsInt(D972A18DiagX)<>2) then
      Error("A18 digest diagnostic source F2 alphabet drift at row ",
        D972A18DiagI);
    fi;
    if AbsInt(D972A18DiagX)=1 then
      Add(D972A18DiagMapped,SignInt(D972A18DiagX)*1);
    else
      Add(D972A18DiagMapped,SignInt(D972A18DiagX)*4);
    fi;
  od;
  D972A18DiagMapped:=D972A18DiagReduce(D972A18DiagMapped);;

  D972A18DiagRaw1:=D972A18DiagMarkedRaw(D972A18DiagMapped,[-6,-5,-3],[6]);;
  D972A18DiagRaw2:=D972A18DiagMarkedRaw(D972A18DiagMapped,[1],[-3,-2,-1]);;
  D972A18DiagRaw3:=D972A18DiagMarkedRaw(D972A18DiagMapped,[4],[6]);;
  D972A18DiagRaw4:=D972A18DiagMarkedRaw(D972A18DiagMapped,
    [-6,-5,-3],[-3,-2,-1]);;
  D972A18DiagRaw5:=D972A18DiagMarkedRaw(D972A18DiagMapped,[1],[4]);;
  D972A18DiagPart1:=D972A18DiagInverse(D972A18DiagReduce(D972A18DiagRaw1));;
  D972A18DiagPart2:=D972A18DiagInverse(D972A18DiagReduce(D972A18DiagRaw2));;
  D972A18DiagPart3:=D972A18DiagReduce(D972A18DiagRaw3);;
  D972A18DiagPart4:=D972A18DiagReduce(D972A18DiagRaw4);;
  D972A18DiagPart5:=D972A18DiagReduce(D972A18DiagRaw5);;
  D972A18DiagActual:=D972A18DiagReduce(Concatenation(D972A18DiagPart1,
    D972A18DiagPart2,D972A18DiagPart3,D972A18DiagPart4,D972A18DiagPart5));;
  Add(D972A18DiagNorms,D972A18DiagActual);;

  D972A18DiagExpected:=D972A18DiagFixtureObj.rows[D972A18DiagI];;
  D972A18DiagActualSha:=HexSHA256(D972A18DiagJson(D972A18DiagActual));;
  if D972A18DiagActual<>D972A18DiagExpected.word or
     D972A18DiagActualSha<>D972A18DiagExpected.sha256 then
    Print("D972_B4_A18_FINITE_DIGEST_DIAG_MISMATCH row=",D972A18DiagI,
      " key=",D972A18DiagJson(D972A18DiagSourceRow[2]),"\n");
    Print("source_f2=",D972A18DiagJson(D972A18DiagF2),"\n");
    Print("mapped_word=",D972A18DiagJson(D972A18DiagMapped),"\n");
    Print("component1_raw=",D972A18DiagJson(D972A18DiagRaw1),
      " reduced=",D972A18DiagJson(D972A18DiagReduce(D972A18DiagRaw1)),"\n");
    Print("component2_raw=",D972A18DiagJson(D972A18DiagRaw2),
      " reduced=",D972A18DiagJson(D972A18DiagReduce(D972A18DiagRaw2)),"\n");
    Print("component3_raw=",D972A18DiagJson(D972A18DiagRaw3),
      " reduced=",D972A18DiagJson(D972A18DiagReduce(D972A18DiagRaw3)),"\n");
    Print("component4_raw=",D972A18DiagJson(D972A18DiagRaw4),
      " reduced=",D972A18DiagJson(D972A18DiagReduce(D972A18DiagRaw4)),"\n");
    Print("component5_raw=",D972A18DiagJson(D972A18DiagRaw5),
      " reduced=",D972A18DiagJson(D972A18DiagReduce(D972A18DiagRaw5)),"\n");
    Print("actual_serialization=",D972A18DiagJson(D972A18DiagActual),"\n");
    Print("expected_serialization=",D972A18DiagJson(D972A18DiagExpected.word),"\n");
    Print("actual_row_sha256=",D972A18DiagActualSha,
      " expected_row_sha256=",D972A18DiagExpected.sha256,"\n");
    Print("expected_global_dtilde_sha256=",D972A18DiagDtildeSha,"\n");
    Print("type_sign_diagnostics:\n");
    for D972A18DiagX in D972A18DiagF2 do
      Print("  x=",D972A18DiagX," IsInt=",IsInt(D972A18DiagX),
        " TypeObj=",TypeObj(D972A18DiagX)," SignInt=",SignInt(D972A18DiagX),
        " SignInt_times_4=",SignInt(D972A18DiagX)*4,"\n");
    od;
    Error("A18 digest diagnostic first row mismatch");
  fi;
od;;

D972A18DiagActualGlobal:=HexSHA256(D972A18DiagJson(D972A18DiagNorms));;
if D972A18DiagActualGlobal<>D972A18DiagDtildeSha then
  Error("A18 digest diagnostic global D-tilde digest mismatch: ",
    D972A18DiagActualGlobal);
fi;;
Print("D972_B4_A18_FINITE_DIGEST_DIAG_PASS rows=972 dtilde_sha256=",
  D972A18DiagActualGlobal," fixture_sha256=",D972A18DiagFixtureSha,"\n");
Print("D972_B4_A18_FINITE_DIGEST_DIAG_FINAL_MARKER status=PASS rows=972\n");
