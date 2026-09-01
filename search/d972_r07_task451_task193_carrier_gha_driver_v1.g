#############################################################################
## Task452: accepted Task451 positive to task193 literal carrier.
#############################################################################
if not IsBound(D972_R07_TASK451_TASK193_CARRIER_V1_RUN) or D972_R07_TASK451_TASK193_CARRIER_V1_RUN<>true then Error("task452 external preamble required");fi;;
D452P:="search/d972_r07_task451_task193_carrier_v1.py";;D452C:="crosscheck/check_d972_r07_task451_task193_carrier_v1.py";;D452PB:=8553;;D452PS:="18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644";;D452CB:=8516;;D452CS:="82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73";;
if not IsBound(D452Task451Result) or not IsBound(D452Task451Checkpoint) or not IsBound(D452Task451CheckerLog) or not IsBound(D452SourceHead) or not IsBound(D452RunId) or not IsBound(D452ArtifactId) then Error("task452 input preamble");fi;;
D452Read:=function(p)local x;x:=StringFile(p);if x=fail then Error("task452 missing ",p);fi;return x;end;;D452Pin:=function(p,n,s)local x;x:=D452Read(p);if Length(x)<>n or HexSHA256(x)<>s then Error("task452 pin drift ",p);fi;end;;D452Pin(D452P,D452PB,D452PS);;D452Pin(D452C,D452CB,D452CS);;
D452Out:="ci/out/d972_r07_task451_task193_carrier_v1.json";;D452Check:="ci/out/d972_r07_task451_task193_carrier_v1_checker.json";;D452PL:="ci/out/d972_r07_task451_task193_carrier_v1_producer.log";;D452CL:="ci/out/d972_r07_task451_task193_carrier_v1_checker.log";;
Exec("mkdir -p ci/out");;if IsExistingFile(D452Out) or IsExistingFile(D452Check) then Error("task452 stale output");fi;;
Exec(Concatenation("python3 -u -B ",D452P," --task451-result ",D452Task451Result," --task451-checkpoint ",D452Task451Checkpoint," --task451-checker-log ",D452Task451CheckerLog," --source-head ",D452SourceHead," --run-id ",String(D452RunId)," --artifact-id ",String(D452ArtifactId)," --output ",D452Out," 2>&1 | tee ",D452PL));;
if PositionSublist(D452Read(D452PL),"R07_TASK451_TASK193_CARRIER_V1 status=ACCEPTED")=fail then Error("task452 producer terminal");fi;;
Exec(Concatenation("python3 -u -B ",D452C," --carrier ",D452Out," --task451-result ",D452Task451Result," --task451-checkpoint ",D452Task451Checkpoint," --task451-checker-log ",D452Task451CheckerLog," --output ",D452Check," 2>&1 | tee ",D452CL));;
if PositionSublist(D452Read(D452CL),"R07_TASK451_TASK193_CARRIER_V1_CHECKER_PASS")=fail then Error("task452 checker terminal");fi;;Print("R07_TASK451_TASK193_CARRIER_V1_DRIVER_PASS\n");;
