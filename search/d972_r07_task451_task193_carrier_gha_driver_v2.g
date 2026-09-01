#############################################################################
## Task455: Task453 batch-64 positive to task193 literal carrier v2.
#############################################################################
if not IsBound(D972_R07_TASK451_TASK193_CARRIER_V2_RUN) or D972_R07_TASK451_TASK193_CARRIER_V2_RUN<>true then Error("task455 external preamble required");fi;;
D455P:="search/d972_r07_task451_task193_carrier_v2.py";;D455C:="crosscheck/check_d972_r07_task451_task193_carrier_v2.py";;D455PB:=3530;;D455PS:="abe7d2ad15a48d641a41f51fb69c1d989224e96d024b688859a6ab141b176bf3";;D455CB:=3584;;D455CS:="8a27b06155bf94a99a38a8fd891bb811e2c0958db5ac7f39312403337a8c878b";;
if not IsBound(D455Task451Result) or not IsBound(D455Task451Checkpoint) or not IsBound(D455Task451CheckerLog) or not IsBound(D455SourceHead) or not IsBound(D455RunId) or not IsBound(D455ArtifactId) then Error("task455 input preamble");fi;;
D455Read:=function(p)local x;x:=StringFile(p);if x=fail then Error("task455 missing ",p);fi;return x;end;;D455Pin:=function(p,n,s)local x;x:=D455Read(p);if Length(x)<>n or HexSHA256(x)<>s then Error("task455 pin drift ",p);fi;end;;D455Pin(D455P,D455PB,D455PS);;D455Pin(D455C,D455CB,D455CS);;
D455Out:="ci/out/d972_r07_task451_task193_carrier_v2.json";;D455Check:="ci/out/d972_r07_task451_task193_carrier_v2_checker.json";;D455PL:="ci/out/d972_r07_task451_task193_carrier_v2_producer.log";;D455CL:="ci/out/d972_r07_task451_task193_carrier_v2_checker.log";;
Exec("mkdir -p ci/out");;if IsExistingFile(D455Out) or IsExistingFile(D455Check) then Error("task455 stale output");fi;;
Exec(Concatenation("python3 -u -B ",D455P," --task451-result ",D455Task451Result," --task451-checkpoint ",D455Task451Checkpoint," --task451-checker-log ",D455Task451CheckerLog," --source-head ",D455SourceHead," --run-id ",String(D455RunId)," --artifact-id ",String(D455ArtifactId)," --output ",D455Out," 2>&1 | tee ",D455PL));;
if PositionSublist(D455Read(D455PL),"R07_TASK451_TASK193_CARRIER_V2 status=ACCEPTED")=fail then Error("task455 producer terminal");fi;;
Exec(Concatenation("python3 -u -B ",D455C," --carrier ",D455Out," --task451-result ",D455Task451Result," --task451-checkpoint ",D455Task451Checkpoint," --task451-checker-log ",D455Task451CheckerLog," --output ",D455Check," 2>&1 | tee ",D455CL));;
if PositionSublist(D455Read(D455CL),"R07_TASK451_TASK193_CARRIER_V2_CHECKER_PASS")=fail then Error("task455 checker terminal");fi;;Print("R07_TASK451_TASK193_CARRIER_V2_DRIVER_PASS\n");;
