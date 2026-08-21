if GAPInfo.Version<>"4.16.0" then Error("GAP 4.16.0 required"); fi;;
if LoadPackage("smallgrp")<>true then Error("smallgrp LoadPackage failed"); fi;;
if LoadPackage("autpgrp")<>true then Error("autpgrp LoadPackage failed"); fi;;
if LoadPackage("anupq")<>true then Error("anupq LoadPackage failed"); fi;;
if LoadPackage("json")<>true then Error("json LoadPackage failed"); fi;;
D972_B345_Q3_RUN:=true;;
D972_B345_Q3_OUTPUT:="ci/out/d972_b345_q3_chief_v1.json";;
Read("search/d972_b345_q3_gha_driver_v1.g");;
QUIT_GAP(0);;
