#############################################################################
## Actual v12 dual profile.  The workflow supplies the preamble externally.
#############################################################################
D435Producer:="search/d972_r07_a0_actual_dual_weight_profile_v1.py";;
D435Checker:="crosscheck/check_d972_r07_a0_actual_dual_weight_profile_v1.py";;
D435Artifact:="ci/out/d972_r07_a0_actual_dual_weight_profile_v1.json";;
D435Checkpoint:="ci/out/d972_r07_a0_actual_dual_weight_profile_v1_output.checkpoint";;
D435PL:="ci/out/d972_r07_a0_actual_dual_weight_profile_v1_producer.log";;
D435CL:="ci/out/d972_r07_actual_dual_weight_profile_v1_checker.log";;
D435ProducerBytes:=14663;;D435ProducerSHA:="36cc190dc610a1675b9d7b990252a7b01eb366649ecf2f84fa1dde3660c694fd";;
D435CheckerBytes:=9735;;D435CheckerSHA:="8bc0215bab131e623e9f820f330a285cfcb5ab6c650fd52ea76a2d3ba8f0f350";;
D435Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task435 missing ",p);fi;return x;end;;
D435Pin:=function(p,n,s)local x;x:=D435Read(p);if n=0 or s="PENDING" then Error("task435 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task435 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_RUN) or D972_R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_RUN<>true then Error("task435 external preamble required");fi;;
D435Pin(D435Producer,D435ProducerBytes,D435ProducerSHA);;D435Pin(D435Checker,D435CheckerBytes,D435CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D435Artifact) or IsExistingFile(D435Checkpoint) then Error("task435 output path is not fresh");fi;;
Exec(Concatenation("python3 -u -B ",D435Producer," --mode PRODUCTION --seconds 1800 --rss-bytes 4800000000 --output ",D435Artifact," --checkpoint ",D435Checkpoint," 2>&1 | tee ",D435PL));;
if not IsExistingFile(D435Artifact) then Error("task435 artifact missing");fi;;
if PositionSublist(D435Read(D435PL),"R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1")=fail then Error("task435 producer marker");fi;;
Exec(Concatenation("python3 -u -B ",D435Checker," ",D435Artifact," 2>&1 | tee ",D435CL));;
if PositionSublist(D435Read(D435CL),"R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_CHECKER_PASS")=fail then Error("task435 checker marker");fi;;
Print("R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_DRIVER_PASS\n");;
