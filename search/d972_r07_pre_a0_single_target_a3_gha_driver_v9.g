#############################################################################
## R07 pre-A0 A3 v9 production repair driver. ASCII only.
#############################################################################
D363V9Base:="search/d972_r07_pre_a0_single_target_a3_gha_driver_v8.g";;
D363V9Generated:="ci/out/d972_r07_pre_a0_single_target_a3_gha_driver_v9.generated.g";;
D363V9Raw:=StringFile(D363V9Base);;
if D363V9Raw=fail or Length(D363V9Raw)<>20412 or
   HexSHA256(D363V9Raw)<>"fd33b9d412e079cfa001b42a39ebc67d2710f87256c48285e569b9ec971fafc1" then
 Error("A3/v9 frozen v8 driver drift");
fi;

D363V9ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then
  Error("A3/v9 replacement count");
 fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;

D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Producer:=\"search/d972_r07_pre_a0_single_target_a3_v6.py\";;",
 "D363Producer:=\"search/d972_r07_pre_a0_single_target_a3_v7.py\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Checker:=\"crosscheck/check_d972_r07_pre_a0_single_target_a3_v6.py\";;",
 "D363Checker:=\"crosscheck/check_d972_r07_pre_a0_single_target_a3_v7.py\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Receipt:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.json\";;",
 "D363Receipt:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.json\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Verdict:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.verdict.json\";;",
 "D363Verdict:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.verdict.json\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363ProducerLog:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.producer.log\";;",
 "D363ProducerLog:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.producer.log\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363CheckerLog:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.checker.log\";;",
 "D363CheckerLog:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.checker.log\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Shell:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.driver.sh\";;",
 "D363Shell:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.driver.sh\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "D363Sentinel:=\"ci/out/d972_r07_pre_a0_single_target_a3_v6.driver.accepted\";;",
 "D363Sentinel:=\"ci/out/d972_r07_pre_a0_single_target_a3_v7.driver.accepted\";;");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "[D363Producer,\"a393e512d2f50ae8d622be9ad488a5fbaf47729981da13177acd013a831140e2\",107641],",
 "[D363Producer,\"6d167a4f8424d5706deacc190366170be1c28dca2e20f132af23d31d9c0fada4\",1209],");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "[D363Checker,\"c38dfc6f392e3595d0ff00001ba19453b7a9022643ef1c9f06862d6f37934ab8\",120097]",
 "[D363Checker,\"2ea78b0e4d48de18b518fd93dbc37bb28de922a9c7b4dc4b9c356969bb3923c0\",1224]");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "ci/out/.d972_r07_pre_a0_single_target_a3_v6.json.tmp.*",
 "ci/out/.d972_r07_pre_a0_single_target_a3_v7.json.tmp.*");;
D363V9Raw:=D363V9ReplaceOnce(D363V9Raw,
 "ci/out/.d972_r07_pre_a0_single_target_a3_v6.verdict.json.tmp.*",
 "ci/out/.d972_r07_pre_a0_single_target_a3_v7.verdict.json.tmp.*");;

PrintTo(D363V9Generated,D363V9Raw);;
Read(D363V9Generated);;
