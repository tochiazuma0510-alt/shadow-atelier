#############################################################################
## R07 task345 v10 observed-inventory repair transport. ASCII only.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then Error("task345 v10 PRODUCTION required"); fi;
D345V10Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v9.g";;
D345V10Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v10.generated.g";;
D345V10Raw:=StringFile(D345V10Base);;
if D345V10Raw=fail or Length(D345V10Raw)<>4096 or
   HexSHA256(D345V10Raw)<>"e53789883fbe91b59e0ccdf2e7de883231603a4b029a0abd1dc6990fe39116a6" then
 Error("task345 v10 pinned v9 driver drift");
fi;
D345V10ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then Error("task345 v10 replacement count"); fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;
D345V10Raw:=D345V10ReplaceOnce(D345V10Raw,
 "search/d972_r07_word_independent_successor_kernel_v8.py",
 "search/d972_r07_word_independent_successor_kernel_v9.py");;
D345V10Raw:=D345V10ReplaceOnce(D345V10Raw,
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v8.py",
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v9.py");;
D345V10Raw:=D345V10ReplaceOnce(D345V10Raw,
 "[D345Producer,1599,\\\"dc22270e3c36c5025c495c012d68d702277979fb3446cb4051459502936ac5ea\\\"],",
 "[D345Producer,1598,\\\"9982d1dc9c7bce4763fdd44ed12acc802a4c77440241e25bb98b1af4ed5d6ad9\\\"],");;
D345V10Raw:=D345V10ReplaceOnce(D345V10Raw,
 "[D345Checker,1614,\\\"c6099b732db86803ceeef66fb5db4c050828d0d7da4e3bfc92a66534d035cd84\\\"],",
 "[D345Checker,1908,\\\"c092bd1b543b13304dba6f0765de143d5090f3cea4d48de69cbbf80e4d590003\\\"],");;
PrintTo(D345V10Generated,D345V10Raw);;
Read(D345V10Generated);;
