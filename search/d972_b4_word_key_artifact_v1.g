## Exact B4 roof word/key producer (versioned, bounded output only).
## The independent Python checker owns the frozen tuple digest and the final
## pin.  This GAP side reconstructs compact f from the exact calibration rows,
## obtains one natural FreeGroup word per f, and checks the epi round-trip.

D972WKLoadPrefix := function(path, marker)
  local src, at, tmp;
  src:=StringFile(path);
  if src=fail then Error("word/key producer: missing source ",path); fi;
  at:=PositionSublist(src,marker);
  if at=fail then Error("word/key producer: worker marker missing"); fi;
  tmp:=Filename(DirectoryTemporary(),"d972_b4_word_key_worker.g");
  FileString(tmp,src{[1..at-1]});
  Read(tmp);
end;;
if not IsBound(GetEnv) then GetEnv:=name->fail; fi;
Read("search/gaplib_common.g");;
D972WKLoadPrefix("search/d972_dovetail_worker_v1.g",
  "\nif D972Mode = \"selftest\" then");;

if not IsBound(D972BuildBase) or not IsBound(D972ScanCalibrationBase) then
  Error("word/key producer: D972 worker definitions unavailable");
fi;

## Numeric/list comparator matching Python tuple/list lexicographic order.
D972WKLess := function(a,b)
  local i, av, bv;
  if IsInt(a) and IsInt(b) then return a < b; fi;
  if not (IsList(a) and IsList(b)) then Error("word/key comparator type drift"); fi;
  for i in [1..Minimum(Length(a),Length(b))] do
    av:=a[i]; bv:=b[i];
    if av=bv then continue; fi;
    return D972WKLess(av,bv);
  od;
  return Length(a)<Length(b);
end;;

D972WKJson := function(x)
  local i,parts;
  if IsInt(x) then return String(x); fi;
  if not IsList(x) then Error("word/key JSON value type drift"); fi;
  parts:=List([1..Length(x)],i->D972WKJson(x[i]));
  return Concatenation("[",D972Join(parts,","),"]");
end;;

Print("B4_WORD_KEY_BASE_BEGIN\n");
B4WKBase:=D972BuildBase(false);;
B4WKRes:=D972ScanCalibrationBase(B4WKBase);;
if B4WKRes.shadow_count<>972 or
   B4WKRes.target_key_set_sorted_sha256<>
     "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
  Error("word/key producer: exact frozen 972 calibration gate failed");
fi;
Print("B4_WORD_KEY_BASE_PASS count=",B4WKRes.shadow_count,"\n");

B4WKF2:=FreeGroup("x","y");;
B4WKEpi:=GroupHomomorphismByImages(B4WKF2,B4WKBase.compact_pure,
  [B4WKF2.1,B4WKF2.2],[B4WKBase.compact_x,B4WKBase.compact_y]);;
if B4WKEpi=fail then Error("word/key producer: compact marked epi failed"); fi;

B4WKRows:=[];;
for B4WKSh in B4WKRes.shadows do
  B4WKf:=B4WKSh.f;;
  B4WKword:=PreImagesRepresentative(B4WKEpi,B4WKf);;
  if B4WKword=fail or Image(B4WKEpi,B4WKword)<>B4WKf then
    Error("word/key producer: PreImagesRepresentative round-trip failed");
  fi;
  B4WKfirst:=D972BlockRestrict(B4WKf,0,27);;
  B4WKsecond:=D972BlockRestrict(B4WKf,27,9);;
  B4WKkey:=[B4WKSh.m,D972Can9(B4WKfirst),D972Can4(B4WKsecond)];;
  Add(B4WKRows,rec(key:=B4WKkey,m:=B4WKSh.m,word:=D972SignedWord(B4WKword)));
od;
if Length(B4WKRows)<>972 then Error("word/key producer: row count drift"); fi;
Sort(B4WKRows,function(a,b) return D972WKLess(a.key,b.key); end);
if Length(Set(List(B4WKRows,r->r.key)))<>972 then
  Error("word/key producer: duplicate reconstructed target key");
fi;

B4WKRowJson:=List(B4WKRows,r->D972WKJson([r.m,r.key,r.word]));;
B4WKRowsJson:=Concatenation("[",D972Join(B4WKRowJson,","),"]");;
B4WKDigest:=HexSHA256(B4WKRowsJson);;
## gap-run.yml can bind this as a GAP global in its preamble.  This is
## necessary on Linux because the generic workflow preamble is GAP source,
## not a shell environment assignment.
B4WKOut:=fail;;
if IsBound(D972_B4_WORD_KEY_OUTPUT) then
  B4WKOut:=D972_B4_WORD_KEY_OUTPUT;
else
  B4WKOut:=GetEnv("D972_B4_WORD_KEY_OUTPUT");
fi;
if B4WKOut=fail or B4WKOut="" then
  B4WKOut:=Filename(DirectoryTemporary(),"d972_b4_word_key_artifact_v1.json");
fi;
B4WKJson:=Concatenation(
  "{\"schema\":\"d972-b4-word-key-artifact/v1\",",
  "\"count\":972,",
  "\"source_target_key_digest\":\"",
  B4WKRes.target_key_set_sorted_sha256,"\",",
  "\"canonical_bytes_sha256\":\"",B4WKDigest,"\",",
  "\"rows\":",B4WKRowsJson,"}");
WriteFile(B4WKOut,Concatenation(B4WKJson,"\n"));;
Print("B4_WORD_KEY_ARTIFACT_PASS count=972 digest=",B4WKDigest,
  " output=",B4WKOut,"\n");
QUIT;
