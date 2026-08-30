#############################################################################
## Task428 diagnostic: one pinned v9 bootstrap call, no owner search driver.
#############################################################################
D428Wrapper:="search/d972_r07_a0_pb34_direct_quotient_bootstrap_trace_v1.py";; D428Bytes:=2716;; D428SHA:="7407e2b97623fef949955db432f31c64ec51a523da1686e007f380c19d785b94";;
D428Receipt:="ci/out/d972_r07_a0_v9_bootstrap_trace_v1.json";;D428Log:="ci/out/d972_r07_a0_v9_bootstrap_trace_v1.log";;
if not IsBound(D972_R07_A0_V9_BOOTSTRAP_TRACE_V1_RUN) or D972_R07_A0_V9_BOOTSTRAP_TRACE_V1_RUN<>true then Error("task428 external preamble required");fi;;
D428Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task428 missing ",p);fi;return x;end;;
D428Pin:=function()local x;x:=D428Read(D428Wrapper);if Length(x)<>D428Bytes or Length(D428SHA)<>64 or HexSHA256(x)<>D428SHA then Error("task428 wrapper pin drift");fi;return true;end;;
if D428SHA="PENDING" then Error("task428 pin pending");fi;;D428Pin();;Exec("mkdir -p ci/out");;
Exec(Concatenation("python3 -u -B ",D428Wrapper," --mode PRODUCTION 2>&1 | tee ",D428Log));;
D428L:=D428Read(D428Log);;D428R:=D428Read(D428Receipt);;
D428Ready:=PositionSublist(D428L,"R07_A0_V9_BOOTSTRAP_TRACE_V1 READY")<>fail;;D428Trace:=PositionSublist(D428L,"R07_A0_V9_BOOTSTRAP_TRACE_V1 TRACE_CAPTURED")<>fail;;
if D428Ready=D428Trace then Error("task428 expected exactly one terminal marker");fi;;if PositionSublist(D428R,"\"status\"")=fail then Error("task428 receipt missing");fi;;
Print("R07_A0_V9_BOOTSTRAP_TRACE_GHA_DRIVER_V1_PASS receipt_sha256=",HexSHA256(D428R),"\n");;
