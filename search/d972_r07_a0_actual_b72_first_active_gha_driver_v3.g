#############################################################################
## Task438 v3 p176/base loader ABI hotfix. Generic workflow supplies preamble.
#############################################################################
D438Producer:="search/d972_r07_a0_actual_b72_first_active_v3.py";;
D438Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v3.py";;
D438Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v3.json";;
D438Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v3_output.checkpoint";;
D438PL:="ci/out/d972_r07_a0_actual_b72_first_active_v3_producer.log";;
D438CL:="ci/out/d972_r07_a0_actual_b72_first_active_v3_checker.log";;
D438ProducerBytes:=2964;;D438ProducerSHA:="27b0bf8baf22ed815870d45716e813a2646c3e470d03510be0ca2c71fcaccb88";;D438CheckerBytes:=2298;;D438CheckerSHA:="f7aeeac29fb8a376bc8935124b16b10d085e9d825ea6f2a88cf4cfba37766281";;
D438Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task438 missing ",p);fi;return x;end;;
D438Pin:=function(p,n,s)local x;x:=D438Read(p);if n=0 or s="PENDING" then Error("task438 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task438 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V3_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V3_RUN<>true then Error("task438 external preamble required");fi;;
D438Pin(D438Producer,D438ProducerBytes,D438ProducerSHA);;D438Pin(D438Checker,D438CheckerBytes,D438CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D438Artifact) or IsExistingFile(D438Checkpoint) then Error("task438 output path is not fresh");fi;;
Exec(Concatenation("python3 -u -B ",D438Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D438Artifact," --checkpoint ",D438Checkpoint," 2>&1 | tee ",D438PL));;
if not IsExistingFile(D438Artifact) then Error("task438 artifact missing");fi;;if PositionSublist(D438Read(D438PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V3")=fail then Error("task438 producer marker");fi;;
Exec(Concatenation("python3 -u -B ",D438Checker," ",D438Artifact," 2>&1 | tee ",D438CL));;if PositionSublist(D438Read(D438CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V3_CHECKER_PASS")=fail then Error("task438 checker marker");fi;;Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V3_DRIVER_PASS\n");;
