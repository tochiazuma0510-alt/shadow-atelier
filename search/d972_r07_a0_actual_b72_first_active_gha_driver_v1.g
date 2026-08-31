#############################################################################
## Task436 actual 72-point adjoint / selective S0-S2 fibre owner.
## The generic workflow supplies the external preamble.
#############################################################################
D436Producer:="search/d972_r07_a0_actual_b72_first_active_v1.py";;
D436Checker:="crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py";;
D436Artifact:="ci/out/d972_r07_a0_actual_b72_first_active_v1.json";;
D436Checkpoint:="ci/out/d972_r07_a0_actual_b72_first_active_v1_output.checkpoint";;
D436PL:="ci/out/d972_r07_a0_actual_b72_first_active_v1_producer.log";;
D436CL:="ci/out/d972_r07_a0_actual_b72_first_active_v1_checker.log";;
D436ProducerBytes:=24643;;D436ProducerSHA:="5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc";;D436CheckerBytes:=13834;;D436CheckerSHA:="3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916";;
D436Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task436 missing ",p);fi;return x;end;;
D436Pin:=function(p,n,s)local x;x:=D436Read(p);if n=0 or s="PENDING" then Error("task436 pins pending");fi;if Length(x)<>n or HexSHA256(x)<>s then Error("task436 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_RUN) or D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_RUN<>true then Error("task436 external preamble required");fi;;
D436Pin(D436Producer,D436ProducerBytes,D436ProducerSHA);;D436Pin(D436Checker,D436CheckerBytes,D436CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D436Artifact) or IsExistingFile(D436Checkpoint) then Error("task436 output path is not fresh");fi;;
Exec(Concatenation("python3 -u -B ",D436Producer," --mode PRODUCTION --seconds 2400 --rss-bytes 4800000000 --output ",D436Artifact," --checkpoint ",D436Checkpoint," 2>&1 | tee ",D436PL));;
if not IsExistingFile(D436Artifact) then Error("task436 artifact missing");fi;;
if PositionSublist(D436Read(D436PL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1")=fail then Error("task436 producer marker");fi;;
Exec(Concatenation("python3 -u -B ",D436Checker," ",D436Artifact," 2>&1 | tee ",D436CL));;
if PositionSublist(D436Read(D436CL),"R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_CHECKER_PASS")=fail then Error("task436 checker marker");fi;;
Print("R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_DRIVER_PASS\n");;
