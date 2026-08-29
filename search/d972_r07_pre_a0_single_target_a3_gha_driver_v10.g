#############################################################################
## R07 pre-A0 A3 v10 independent-checker reason-map repair. ASCII only.
#############################################################################
D363V10Base:="search/d972_r07_pre_a0_single_target_a3_gha_driver_v9.g";;
D363V10Generated:="ci/out/d972_r07_pre_a0_single_target_a3_gha_driver_v10.generated.g";;
D363V10Raw:=StringFile(D363V10Base);;
if D363V10Raw=fail or Length(D363V10Raw)<>3293 or
   HexSHA256(D363V10Raw)<>"18849b9d903d29f2d33777a6d1f89d326aa6bf4bcaab7d5e9c0872e55903ce81" then
 Error("A3/v10 pinned v9 driver drift");
fi;

D363V10ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then
  Error("A3/v10 replacement count");
 fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;

D363V10Raw:=D363V10ReplaceOnce(D363V10Raw,
 "crosscheck/check_d972_r07_pre_a0_single_target_a3_v7.py",
 "crosscheck/check_d972_r07_pre_a0_single_target_a3_v8.py");;
D363V10Raw:=D363V10ReplaceOnce(D363V10Raw,
 "[D363Checker,\"2ea78b0e4d48de18b518fd93dbc37bb28de922a9c7b4dc4b9c356969bb3923c0\",1224]",
 "[D363Checker,\"38f7da77423a88a23609996e3b55ed7644e12e359e49e858d7a4467f1096cafe\",1429]");;

PrintTo(D363V10Generated,D363V10Raw);;
Read(D363V10Generated);;
