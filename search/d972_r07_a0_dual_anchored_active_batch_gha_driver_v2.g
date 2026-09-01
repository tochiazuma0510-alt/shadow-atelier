#############################################################################
## Task453 batch-cap 64 wrapper for the exact Task451 v1 driver.
## External preamble required; ASCII only.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_RUN) or
   D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_RUN<>true then
 Error("task453 external preamble required");
fi;

D453Owner:="search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g";;
D453OwnerBytes:=2569;;
D453OwnerSHA:="6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000";;
D453ResultBytes:=2569;;
D453ResultSHA:="07ec885b719aea17e382a8dc9d5a1d94026c627c6d9c1f535842ebbb3fb41cf6";;
D453Inner:="ci/out/a0_task453_inner.g";;
D453Old:="--batch-cap 16";;
D453New:="--batch-cap 64";;

D453Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task453 missing input ",path); fi;
 return raw;
end;;
D453Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task453 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;

D453Raw:=D453Read(D453Owner);;
if Length(D453Raw)<>D453OwnerBytes or HexSHA256(D453Raw)<>D453OwnerSHA then
 Error("task453 frozen v1 driver drift");
fi;
if D453Count(D453Raw,D453Old)<>1 or D453Count(D453Raw,D453New)<>0 then
 Error("task453 batch-cap patch cardinality");
fi;
D453Raw:=ReplacedString(D453Raw,D453Old,D453New);;
if D453Count(D453Raw,D453Old)<>0 or D453Count(D453Raw,D453New)<>1 or
   Length(D453Raw)<>D453ResultBytes or HexSHA256(D453Raw)<>D453ResultSHA then
 Error("task453 patched v1 driver drift");
fi;

Exec("mkdir -p ci/out");;
D453Stream:=OutputTextFile(D453Inner,false);;
if D453Stream=fail then Error("task453 inner driver open"); fi;
SetPrintFormattingStatus(D453Stream,false);;
PrintTo(D453Stream,D453Raw);;
CloseStream(D453Stream);;
if D453Read(D453Inner)<>D453Raw then Error("task453 inner readback"); fi;

## The v2 guard is the only external launch authority.  The exact v1 guard is
## satisfied internally only after all byte/cardinality gates above pass.
D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V1_RUN:=true;;
Read(D453Inner);;
Print("R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_DRIVER_PASS\n");;
