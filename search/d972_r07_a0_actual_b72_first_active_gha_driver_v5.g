#############################################################################
## Task440 v5 checker dual-bind hotfix. Generic workflow supplies preamble.
#############################################################################
D440Producer:="search/d972_r07_a0_actual_b72_first_active_v4.py";;
D440Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v5.py";;
D440Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v5.json";;
D440Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v5_output.checkpoint";;
D440PL:="ci/out/d972_r07_a0_actual_b72_first_active_v5_producer.log";;D440CL:="ci/out/d972_r07_a0_actual_b72_first_active_v5_checker.log";;
D440ProducerBytes:=3619;;D440ProducerSHA:="6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f";;D440CheckerBytes:=2579;;D440CheckerSHA:="32aa780f4f74daec48f4e851dd89da20ef63418f9fa267d3eb1504ffb56fba08";;
D440Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task440 missing ",p);fi;return x;end;;
D440Pin:=function(p,n,s)local x;x:=D440Read(p);if n=0 or s="PENDING" then Error("task440 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task440 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V5_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V5_RUN<>true then Error("task440 external preamble required");fi;;D440Pin(D440Producer,D440ProducerBytes,D440ProducerSHA);;D440Pin(D440Checker,D440CheckerBytes,D440CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D440Artifact) or IsExistingFile(D440Checkpoint) then Error("task440 output path is not fresh");fi;;Exec(Concatenation("python3 -u -B ",D440Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D440Artifact," --checkpoint ",D440Checkpoint," 2>&1 | tee ",D440PL));;
if not IsExistingFile(D440Artifact) then Error("task440 artifact missing");fi;;if PositionSublist(D440Read(D440PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V4")=fail then Error("task440 producer marker");fi;;Exec(Concatenation("python3 -u -B ",D440Checker," ",D440Artifact," 2>&1 | tee ",D440CL));;if PositionSublist(D440Read(D440CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V5_CHECKER_PASS")=fail then Error("task440 checker marker");fi;;Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V5_DRIVER_PASS\n");;
