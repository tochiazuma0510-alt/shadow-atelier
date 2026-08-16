#############################################################################
## d972_b4_kbmag_v2.g -- exact six-generator pentagon norm KBMAG lane.
##
## v1 reduced the two-generator F2 representative directly in U_M and was
## invalid: j(y)=U4, not U2, and the rho^4...rho^0 norm was absent.  This
## version retains the bounded/candidate-only policy but constructs the exact
## F6 norm before every ReducedForm call.
#############################################################################

if LoadPackage("kbmag") <> true then
  Print("B4_KBMAG_V2_PACKAGE_FAIL kbmag\n");
  Error("d972_b4_kbmag_v2: KBMAG package unavailable");
fi;
Print("B4_KBMAG_V2_PACKAGE_PASS kbmag\n");

D972KBV2Join := function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;

D972KBV2Json := function(x)
  local p,i;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if not IsList(x) then Error("KBMAG v2 JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972KBV2Json(x[i]));
  return Concatenation("[",D972KBV2Join(p,","),"]");
end;;
D972KBV2Maybe := function(x)
  if x=fail then return "null"; fi;
  return D972KBV2Json(x);
end;;

D972KBV2Output := "ci/out/d972_b4_kbmag_v2.json";;
if IsBound(D972_B4_KBMAG_V2_OUTPUT) then
  D972KBV2Output:=D972_B4_KBMAG_V2_OUTPUT;
fi;
D972KBV2MaxEqns := 50000;;
D972KBV2MaxStates := 50000;;
D972KBV2MaxWdiffs := 50000;;
D972KBV2MaxStored := [100,100];;
if IsBound(D972_B4_KBMAG_V2_MAXEQNS) then
  D972KBV2MaxEqns:=D972_B4_KBMAG_V2_MAXEQNS;
fi;
if IsBound(D972_B4_KBMAG_V2_MAXSTATES) then
  D972KBV2MaxStates:=D972_B4_KBMAG_V2_MAXSTATES;
fi;
if IsBound(D972_B4_KBMAG_V2_MAXWDIFFS) then
  D972KBV2MaxWdiffs:=D972_B4_KBMAG_V2_MAXWDIFFS;
fi;
if IsBound(D972_B4_KBMAG_V2_MAXSTORED) then
  D972KBV2MaxStored:=D972_B4_KBMAG_V2_MAXSTORED;
fi;

## Reuse only the low-index definition prefix.  The truncation marker is
## before LowIndexSubgroupsFpGroup, so no bounded subgroup search is started.
D972KBV2LoadPrefix := function()
  local src,at,tmp;
  src:=StringFile("search/d972_b4_lowindex_v1.g");;
  if src=fail then Error("KBMAG v2: low-index source missing"); fi;
  ## Cut before the producer's optional relator-only QUIT branch.  Cutting
  ## at the low-index call alone would leave that QUIT in the generated
  ## prefix, which GAP rejects at top level before continuing.
  at:=PositionSublist(src,"\nif IsBound(D972_B4_RELATOR_ONLY)");;
  if at=fail then Error("KBMAG v2: low-index prefix marker drift"); fi;
  tmp:=Filename(DirectoryTemporary(),"d972_b4_kbmag_v2_prefix.g");;
  FileString(tmp,src{[1..at-1]});;
  Read(tmp);;
end;;

D972KBV2LoadPrefix();;
if not IsBound(Ufp) or not IsBound(roofWords) or not IsBound(relWords) then
  Error("KBMAG v2: canonical U_M prefix is incomplete");
fi;
if Length(relWords)<>158 or Length(roofWords)<>972 then
  Error("KBMAG v2: canonical input count drift");
fi;
if targetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" or
   relDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" then
  Error("KBMAG v2: canonical input digest drift");
fi;

## Free six-generator model of U_M.  fugen is used for all exact word
## substitutions; ug is the corresponding fp-group generating tuple used by
## KBMAG's ReducedForm.  This keeps the F2 and F6 alphabets distinct.
D972KBV2FreeGens:=GeneratorsOfGroup(fu);;
D972KBV2Ugens:=ug;;
D972KBV2RhoFree:=[
  (D972KBV2FreeGens[3]*D972KBV2FreeGens[5]*D972KBV2FreeGens[6])^-1,
  D972KBV2FreeGens[3], D972KBV2FreeGens[5],
  (D972KBV2FreeGens[1]*D972KBV2FreeGens[2]*D972KBV2FreeGens[3])^-1,
  (D972KBV2FreeGens[1]*D972KBV2FreeGens[4]*D972KBV2FreeGens[5])^-1,
  D972KBV2FreeGens[1] ];;

D972KBV2NormWord:=function(sw)
  local jf,a,orb,v,z,t;
  ## Exact j map: F2 letter 1 -> U1 and letter 2 -> U4.
  jf:=One(D972KBV2FreeGens[1]);;
  for a in sw do
    if a=1 then jf:=jf*D972KBV2FreeGens[1];
    elif a=2 then jf:=jf*D972KBV2FreeGens[4];
    elif a=-1 then jf:=jf*D972KBV2FreeGens[1]^-1;
    elif a=-2 then jf:=jf*D972KBV2FreeGens[4]^-1;
    else Error("KBMAG v2: roof row is not an F2 signed word");
    fi;
  od;
  orb:=[];; v:=jf;;
  for t in [1..5] do
    Add(orb,v);;
    v:=MappedWord(v,D972KBV2FreeGens,D972KBV2RhoFree);
  od;
  ## Required pentagon order is rho^4,...,rho^0.
  z:=One(D972KBV2FreeGens[1]);;
  for t in Reversed([1..5]) do z:=z*orb[t]; od;
  return z;
end;;

D972KBV2SignedToU:=function(w)
  local z,a;
  z:=One(D972KBV2Ugens[1]);;
  for a in D972SignedWord(w) do
    if a>0 then z:=z*D972KBV2Ugens[a];
    else z:=z*D972KBV2Ugens[-a]^-1;
    fi;
  od;
  return z;
end;;

normWords:=List(roofWords,D972KBV2NormWord);;
normSigned:=List(normWords,D972SignedWord);;
normDigest:=HexSHA256(D972KBV2Json(normSigned));;
if normDigest<>"ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e" then
  Error("KBMAG v2: exact roof norm digest drift: ",normDigest);
fi;
Print("B4_KBMAG_V2_INPUT_PASS relators=158 roof=972 j=(1->1,2->4)",
  " norm_order=[4,3,2,1,0] norm_digest=",normDigest,"\n");

rws:=KBMAGRewritingSystem(Ufp);;
SetOrderingOfKBMAGRewritingSystem(rws,"shortlex");;
opts:=OptionsRecordOfKBMAGRewritingSystem(rws);;
opts.maxeqns:=D972KBV2MaxEqns;;
opts.maxstates:=D972KBV2MaxStates;;
opts.maxwdiffs:=D972KBV2MaxWdiffs;;
opts.maxstoredlen:=D972KBV2MaxStored;;
Print("B4_KBMAG_V2_BEGIN maxeqns=",D972KBV2MaxEqns,
  " maxstates=",D972KBV2MaxStates,
  " maxwdiffs=",D972KBV2MaxWdiffs,
  " maxstored=",D972KBV2MaxStored,"\n");
KnuthBendix(rws);;
confluent:=IsConfluent(rws);;
reducedAvailable:=IsBound(rws!.reduced) and rws!.reduced=true;;
Print("B4_KBMAG_V2_DONE confluent=",confluent,
  " reduced_available=",reducedAvailable,"\n");

roofBits:=[];; reducedWords:=[];;
if reducedAvailable then
  for ii in [1..Length(normWords)] do
    if GAPLIB_WallElapsedMs()/1000.0 > 600.0 then
      Print("B4_KBMAG_V2_CAP_EXCEEDED at norm index ",ii,"\n");
      break;
    fi;
    rw:=ReducedForm(rws,D972KBV2SignedToU(normWords[ii]));;
    Add(reducedWords,D972SignedWord(rw));;
    Add(roofBits,IsOne(rw));
  od;
fi;
if Length(roofBits)=972 then
  zeroCount:=Number(roofBits,x->x=false);;
else
  zeroCount:=fail;;
fi;
if Length(roofBits)=972 and zeroCount=0 and confluent then
  status:="CONFLUENT_ALLPASS_CANDIDATE";
elif Length(roofBits)=972 and zeroCount>0 and confluent then
  status:="B4_A_SIDE_CANDIDATE_NEEDS_REPLAY";
else
  status:="NO_TERMINAL_ROOF_RESULT";
fi;

json:=Concatenation(
  "{\"schema\":\"d972-b4-kbmag/v2\",",
  "\"status\":\"",status,"\",",
  "\"relator_count\":158,\"roof_count\":972,",
  "\"target_key_digest\":\"",targetDigest,"\",",
  "\"relator_digest\":\"",relDigest,"\",",
  "\"roof_norm_digest\":\"",normDigest,"\",",
  "\"roof_bits\":",D972KBV2Json(roofBits),",",
  "\"roof_bits_count\":",String(Length(roofBits)),",",
  "\"roof_zero_count\":",D972KBV2Maybe(zeroCount),",",
  "\"confluent\":",D972KBV2Json(confluent),",",
  "\"reduced_available\":",D972KBV2Json(reducedAvailable),",",
  "\"j_map\":\"F2_1->U1,F2_2->U4\",",
  "\"norm_order\":[4,3,2,1,0],",
  "\"proof_level\":\"CANDIDATE_NEEDS_INDEPENDENT_REPLAY\"}");;
f:=OutputTextFile(D972KBV2Output,false);;
SetPrintFormattingStatus(f,false);;
PrintTo(f,Concatenation(json,"\n"));;
CloseStream(f);;
Print("B4_KBMAG_V2_RECEIPT status=",status,
  " roof_bits=",Length(roofBits)," zero_count=",D972KBV2Maybe(zeroCount),
  " output=",D972KBV2Output,"\n");
QUIT;
