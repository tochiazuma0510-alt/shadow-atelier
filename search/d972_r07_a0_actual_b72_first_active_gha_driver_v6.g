#############################################################################
## Task441 v6 checker context closure. Generic workflow supplies preamble.
#############################################################################
D441Producer:="search/d972_r07_a0_actual_b72_first_active_v4.py";;
D441Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v6.py";;
D441Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v6.json";;
D441Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v6_output.checkpoint";;
D441PL:="ci/out/d972_r07_a0_actual_b72_first_active_v6_producer.log";;D441CL:="ci/out/d972_r07_a0_actual_b72_first_active_v6_checker.log";;
D441ProducerBytes:=3619;;D441ProducerSHA:="6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f";;D441CheckerBytes:=3556;;D441CheckerSHA:="f9da121330c7b98ce1ef5f0705f0efad504ef6cdfb6873d1d81b7d124598e379";;
D441Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task441 missing ",p);fi;return x;end;;
D441Pin:=function(p,n,s)local x;x:=D441Read(p);if n=0 or s="PENDING" then Error("task441 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task441 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V6_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V6_RUN<>true then Error("task441 external preamble required");fi;;D441Pin(D441Producer,D441ProducerBytes,D441ProducerSHA);;D441Pin(D441Checker,D441CheckerBytes,D441CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D441Artifact) or IsExistingFile(D441Checkpoint) then Error("task441 output path is not fresh");fi;;Exec(Concatenation("python3 -u -B ",D441Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D441Artifact," --checkpoint ",D441Checkpoint," 2>&1 | tee ",D441PL));;
if not IsExistingFile(D441Artifact) then Error("task441 artifact missing");fi;;if PositionSublist(D441Read(D441PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4")=fail then Error("task441 producer marker");fi;;Exec(Concatenation("python3 -u -B ",D441Checker," ",D441Artifact," 2>&1 | tee ",D441CL));;if PositionSublist(D441Read(D441CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V6_CHECKER_PASS")=fail then Error("task441 checker marker");fi;;Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V6_DRIVER_PASS\n");;
