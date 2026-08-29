#############################################################################
## R07 pre-A0 A3 v11 checker-path pin repair. ASCII only.
#############################################################################
D363V11Base:="search/d972_r07_pre_a0_single_target_a3_gha_driver_v9.g";;
D363V11Generated:="ci/out/d972_r07_pre_a0_single_target_a3_gha_driver_v11.generated.g";;
D363V11Raw:=StringFile(D363V11Base);;
if D363V11Raw=fail or Length(D363V11Raw)<>3293 or
   HexSHA256(D363V11Raw)<>"18849b9d903d29f2d33777a6d1f89d326aa6bf4bcaab7d5e9c0872e55903ce81" then
 Error("A3/v11 pinned v9 driver drift");
fi;
D363V11ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then Error("A3/v11 replacement count"); fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;
D363V11Raw:=D363V11ReplaceOnce(D363V11Raw,
 "crosscheck/check_d972_r07_pre_a0_single_target_a3_v7.py",
 "crosscheck/check_d972_r07_pre_a0_single_target_a3_v8.py");;
D363V11Raw:=D363V11ReplaceOnce(D363V11Raw,
 "[D363Checker,\\\"2ea78b0e4d48de18b518fd93dbc37bb28de922a9c7b4dc4b9c356969bb3923c0\\\",1224]",
 "[D363Checker,\\\"38f7da77423a88a23609996e3b55ed7644e12e359e49e858d7a4467f1096cafe\\\",1429]");;
PrintTo(D363V11Generated,D363V11Raw);;
Read(D363V11Generated);;
