#############################################################################
## A4 v41 wrapper: repair only v40's self-containing post-replacement gate.
## ASCII only.  v40 artifact paths, seeds, and execution remain unchanged.
#############################################################################
if not IsBound(D386Mode) then Error("task449 MODE required"); fi;
if D386Mode<>"RESUME" then Error("task449 v41 requires RESUME"); fi;

D449Owner:="search/d972_r07_word_independent_successor_kernel_gha_driver_v40.g";;
D449OwnerBytes:=16871;;
D449OwnerSHA:="0c87000b7b3b26012b2d68f40e0029e591722aa79f2d6fda37f115fd027b6457";;
D449ResultBytes:=16973;;
D449ResultSHA:="d03eec3d4d954929774516979467f15244a76cd7099e85ce60755c746bb5f7ce";;
D449Inner:="ci/out/a4_task449_inner.g";;

D449Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task449 missing input ",path); fi;
 return raw;
end;;
D449Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task449 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D449ReplaceOnce:=function(raw,old,new)
 if D449Count(raw,old)<>1 then Error("task449 patch cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D449Old:=Concatenation(
 "for D446Pair in D446Pairs do\n",
 " if D446Count(D446Raw,D446Pair[1])<>0 or D446Count(D446Raw,D446Pair[2])<>1 then\n",
 "  Error(\"task446 post-replacement gate\");\n",
 " fi;\n",
 "od;");;
D449New:=Concatenation(
 "for D446Pair in D446Pairs do\n",
 " if (D446Pair=D446Pairs[7] and D446Count(D446Raw,D446Pair[1])<>1) or\n",
 "    (D446Pair<>D446Pairs[7] and D446Count(D446Raw,D446Pair[1])<>0) or\n",
 "    D446Count(D446Raw,D446Pair[2])<>1 then\n",
 "  Error(\"task446 post-replacement gate\");\n",
 " fi;\n",
 "od;");;

D449Raw:=D449Read(D449Owner);;
if Length(D449Raw)<>D449OwnerBytes or HexSHA256(D449Raw)<>D449OwnerSHA then
 Error("task449 frozen v40 driver drift");
fi;
D449Raw:=D449ReplaceOnce(D449Raw,D449Old,D449New);;
if D449Count(D449Raw,D449Old)<>0 or D449Count(D449Raw,D449New)<>1 or
   Length(D449Raw)<>D449ResultBytes or HexSHA256(D449Raw)<>D449ResultSHA then
 Error("task449 patched v40 source drift");
fi;

Exec("mkdir -p ci/out");;
D449Stream:=OutputTextFile(D449Inner,false);;
if D449Stream=fail then Error("task449 inner driver open"); fi;
SetPrintFormattingStatus(D449Stream,false);;
PrintTo(D449Stream,D449Raw);;
CloseStream(D449Stream);;
if D449Read(D449Inner)<>D449Raw then Error("task449 inner readback"); fi;
D386Mode:=D386Mode;;
Read(D449Inner);;
