#############################################################################
## Task439 v4 exact-section guard hotfix. Generic workflow supplies preamble.
#############################################################################
D439Producer:="search/d972_r07_a0_actual_b72_first_active_v4.py";;
D439Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v4.py";;
D439Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v4.json";;
D439Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v4_output.checkpoint";;
D439PL:="ci/out/d972_r07_a0_actual_b72_first_active_v4_producer.log";;D439CL:="ci/out/d972_r07_a0_actual_b72_first_active_v4_checker.log";;
D439ProducerBytes:=3619;;D439ProducerSHA:="6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f";;D439CheckerBytes:=2633;;D439CheckerSHA:="fb66a78d83d1bf712fdcb2bd9e3f7c98726aeadd97345e39c372b86d0550b640";;
D439Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task439 missing ",p);fi;return x;end;;
D439Pin:=function(p,n,s)local x;x:=D439Read(p);if n=0 or s="PENDING" then Error("task439 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task439 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4_RUN<>true then Error("task439 external preamble required");fi;;D439Pin(D439Producer,D439ProducerBytes,D439ProducerSHA);;D439Pin(D439Checker,D439CheckerBytes,D439CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D439Artifact) or IsExistingFile(D439Checkpoint) then Error("task439 output path is not fresh");fi;;Exec(Concatenation("python3 -u -B ",D439Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D439Artifact," --checkpoint ",D439Checkpoint," 2>&1 | tee ",D439PL));;
if not IsExistingFile(D439Artifact) then Error("task439 artifact missing");fi;;if PositionSublist(D439Read(D439PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4")=fail then Error("task439 producer marker");fi;;Exec(Concatenation("python3 -u -B ",D439Checker," ",D439Artifact," 2>&1 | tee ",D439CL));;if PositionSublist(D439Read(D439CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4_CHECKER_PASS")=fail then Error("task439 checker marker");fi;;Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4_DRIVER_PASS\n");;
