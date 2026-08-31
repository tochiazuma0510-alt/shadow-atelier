#############################################################################
## Task437 v2 ABI adapter hotfix. The generic workflow supplies the preamble.
#############################################################################
D437Producer:="search/d972_r07_a0_actual_b72_first_active_v2.py";;
D437Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v2.py";;
D437Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v2.json";;
D437Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v2_output.checkpoint";;
D437PL:="ci/out/d972_r07_a0_actual_b72_first_active_v2_producer.log";;
D437CL:="ci/out/d972_r07_a0_actual_b72_first_active_v2_checker.log";;
D437ProducerBytes:=2352;;D437ProducerSHA:="9355647447c004483d63b827bc95929ad8432a443f166ccdadcf5f054b7bbc17";;D437CheckerBytes:=1767;;D437CheckerSHA:="d72c65136d6f8f821031a1fda6b5c11a4d1bca84ae5c91c8146883d68ff82312";;
D437Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task437 missing ",p);fi;return x;end;;
D437Pin:=function(p,n,s)local x;x:=D437Read(p);if n=0 or s="PENDING" then Error("task437 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task437 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2_RUN<>true then Error("task437 external preamble required");fi;;
D437Pin(D437Producer,D437ProducerBytes,D437ProducerSHA);;D437Pin(D437Checker,D437CheckerBytes,D437CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D437Artifact) or IsExistingFile(D437Checkpoint) then Error("task437 output path is not fresh");fi;;
Exec(Concatenation("python3 -u -B ",D437Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D437Artifact," --checkpoint ",D437Checkpoint," 2>&1 | tee ",D437PL));;
if not IsExistingFile(D437Artifact) then Error("task437 artifact missing");fi;;
if PositionSublist(D437Read(D437PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2")=fail then Error("task437 producer marker");fi;;
Exec(Concatenation("python3 -u -B ",D437Checker," ",D437Artifact," 2>&1 | tee ",D437CL));;
if PositionSublist(D437Read(D437CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2_CHECKER_PASS")=fail then Error("task437 checker marker");fi;;
Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V2_DRIVER_PASS\n");;
