#############################################################################
## R07 task338 v13 serial SELFTEST/PRODUCTION driver. ASCII only.
#############################################################################
if not IsBound(D338Mode) then Error("task338 MODE required"); fi;
if D338Mode<>"SELFTEST" and D338Mode<>"PRODUCTION" then Error("task338 MODE"); fi;
D338Producer:="search/d972_r07_joint_slice_kernel_general_v13.py";;
D338Checker:="crosscheck/check_d972_r07_joint_slice_kernel_general_v13.py";;
D338Fixture:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v13_20260829.json";;
D338Source:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json";;
D338Receipt:="ci/out/d972_r07_joint_slice_kernel_general_v13.json";;
D338Verdict:="ci/out/d972_r07_joint_slice_kernel_general_v13.verdict.json";;
D338PLog:="ci/out/d972_r07_joint_slice_kernel_general_v13.producer.log";;
D338CLog:="ci/out/d972_r07_joint_slice_kernel_general_v13.checker.log";;
D338PTerm:="ci/out/d972_r07_joint_slice_kernel_general_v13.producer.terminal";;
D338CTerm:="ci/out/d972_r07_joint_slice_kernel_general_v13.checker.terminal";;
D338Sh:="ci/out/d972_r07_joint_slice_kernel_general_v13.sh";;
D338OK:="ci/out/d972_r07_joint_slice_kernel_general_v13.ok";;
D338Pins:=[
[D338Producer,79617,"feb69c5ab8e1b4db21ff5df05dac1690718310dc4c99cf4b67fc439ca9bc4268"],
[D338Checker,73233,"dc344638ae42110f7cd028164c3ac5f6b5e1a908bdc596e5b4718c21db3cad07"],
[D338Fixture,11163,"60a3e1449f911fcfc3946373bcb471ea8efbaed4f1a2064e9ffbfba527fae50d"],
[D338Source,12964,"cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058"]
];;
D338Read:=function(path) local value;
  value:=StringFile(path);
  if value=fail or Length(value)=0 then Error("task338 missing ",path); fi;
  return value;
end;;
D338Pin:=function(row) local value;
  value:=D338Read(row[1]);
  if Length(value)<>row[2] or HexSHA256(value)<>row[3] then
    Error("task338 pin drift ",row[1]);
  fi;
end;;
for D338PinRow in D338Pins do D338Pin(D338PinRow); od;
D338Stale:=[
"ci/out/d972_r07_joint_slice_kernel_general_v7.json",
"ci/out/d972_r07_joint_slice_kernel_general_v7.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v7.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v7.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v7.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v7.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v7.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v7.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v7.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v7.verdict.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v8.json",
"ci/out/d972_r07_joint_slice_kernel_general_v8.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v8.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v8.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v8.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v8.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v8.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v8.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v8.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v8.verdict.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v9.json",
"ci/out/d972_r07_joint_slice_kernel_general_v9.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v9.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v9.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v9.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v9.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v9.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v9.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v9.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v9.verdict.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v10.json",
"ci/out/d972_r07_joint_slice_kernel_general_v10.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v10.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v10.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v10.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v10.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v10.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v10.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v10.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v10.verdict.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v11.json",
"ci/out/d972_r07_joint_slice_kernel_general_v11.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v11.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v11.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v11.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v11.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v11.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v11.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v11.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v11.verdict.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v12.json",
"ci/out/d972_r07_joint_slice_kernel_general_v12.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v12.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v12.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v12.producer.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v12.checker.terminal",
"ci/out/d972_r07_joint_slice_kernel_general_v12.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v12.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v12.json.seal",
"ci/out/d972_r07_joint_slice_kernel_general_v12.verdict.json.seal",
Concatenation(D338Receipt,".seal"),Concatenation(D338Verdict,".seal"),
D338Receipt,D338Verdict,D338PLog,D338CLog,D338PTerm,D338CTerm,D338Sh,D338OK
];;
for D338StalePath in D338Stale do
  if IsExistingFile(D338StalePath) then Error("task338 stale output ",D338StalePath); fi;
od;
D338S:=OutputTextFile(D338Sh,false);; SetPrintFormattingStatus(D338S,false);;
PrintTo(D338S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D338Mode="SELFTEST" then
  PrintTo(D338S,"timeout 180s python3 -u -B \"",D338Producer,"\" --mode SELFTEST --fixture \"",D338Fixture,"\" --output \"",D338Receipt,"\" > \"",D338PLog,"\" 2>&1 || { cat \"",D338PLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_SELFTEST_PASS' \"",D338PLog,"\")\" = \"1\" || { cat \"",D338PLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test -s \"",D338Receipt,"\"\ntest -s \"",D338PLog,"\"\n");
  PrintTo(D338S,"timeout 30s python3 -B -c 'import json,hashlib,sys; p=sys.argv[1]; x=json.load(open(p,encoding=\"utf-8\")); s=x.pop(\"self_digest_sha256\",None); y=json.dumps(x,sort_keys=True,separators=(\",\",\":\"),ensure_ascii=True).encode(\"ascii\"); assert isinstance(s,str) and s==hashlib.sha256(y).hexdigest(); print(s)' \"",D338Receipt,"\" > \"",D338Receipt,".seal\"\ntest -s \"",D338Receipt,".seal\"\n");
  PrintTo(D338S,"timeout 180s python3 -u -B \"",D338Checker,"\" --mode SELFTEST --fixture \"",D338Fixture,"\" --receipt \"",D338Receipt,"\" --output \"",D338Verdict,"\" > \"",D338CLog,"\" 2>&1 || { cat \"",D338CLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_SELFTEST_PASS mutation_attempted=44 mutation_rejected=44' \"",D338CLog,"\")\" = \"1\" || { cat \"",D338CLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test -s \"",D338Verdict,"\"\ntest -s \"",D338CLog,"\"\n");
  PrintTo(D338S,"timeout 30s python3 -B -c 'import json,hashlib,sys; p=sys.argv[1]; x=json.load(open(p,encoding=\"utf-8\")); s=x.pop(\"verdict_digest_sha256\",None); y=json.dumps(x,sort_keys=True,separators=(\",\",\":\"),ensure_ascii=True).encode(\"ascii\"); assert isinstance(s,str) and s==hashlib.sha256(y).hexdigest(); print(s)' \"",D338Verdict,"\" > \"",D338Verdict,".seal\"\ntest -s \"",D338Verdict,".seal\"\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL SELFTEST_COMPLETE' \"",D338PLog,"\")\" = \"1\"\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL SELFTEST_COMPLETE' \"",D338CLog,"\")\" = \"1\"\n");
  PrintTo(D338S,"sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL //p' \"",D338PLog,"\" > \"",D338PTerm,"\"\nsed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL //p' \"",D338CLog,"\" > \"",D338CTerm,"\"\ntest -s \"",D338PTerm,"\"\ntest -s \"",D338CTerm,"\"\ntest \"$(cat \"",D338PTerm,"\")\" = \"$(cat \"",D338CTerm,"\")\"\n");
else
  PrintTo(D338S,"timeout 180s python3 -u -B \"",D338Producer,"\" --mode PRODUCTION --fixture \"",D338Fixture,"\" --output \"",D338Receipt,"\" > \"",D338PLog,"\" 2>&1 || { cat \"",D338PLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test -s \"",D338Receipt,"\"\ntest -s \"",D338PLog,"\"\n");
  PrintTo(D338S,"timeout 30s python3 -B -c 'import json,hashlib,sys; p=sys.argv[1]; x=json.load(open(p,encoding=\"utf-8\")); s=x.pop(\"self_digest_sha256\",None); y=json.dumps(x,sort_keys=True,separators=(\",\",\":\"),ensure_ascii=True).encode(\"ascii\"); assert isinstance(s,str) and s==hashlib.sha256(y).hexdigest(); print(s)' \"",D338Receipt,"\" > \"",D338Receipt,".seal\"\ntest -s \"",D338Receipt,".seal\"\n");
  PrintTo(D338S,"timeout 180s python3 -u -B \"",D338Checker,"\" --mode PRODUCTION --fixture \"",D338Fixture,"\" --receipt \"",D338Receipt,"\" --output \"",D338Verdict,"\" > \"",D338CLog,"\" 2>&1 || { cat \"",D338CLog,"\"; exit 1; }\n");
  PrintTo(D338S,"test -s \"",D338Verdict,"\"\ntest -s \"",D338CLog,"\"\n");
  PrintTo(D338S,"timeout 30s python3 -B -c 'import json,hashlib,sys; p=sys.argv[1]; x=json.load(open(p,encoding=\"utf-8\")); s=x.pop(\"verdict_digest_sha256\",None); y=json.dumps(x,sort_keys=True,separators=(\",\",\":\"),ensure_ascii=True).encode(\"ascii\"); assert isinstance(s,str) and s==hashlib.sha256(y).hexdigest(); print(s)' \"",D338Verdict,"\" > \"",D338Verdict,".seal\"\ntest -s \"",D338Verdict,".seal\"\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D338PLog,"\")\" = \"1\"\n");
  PrintTo(D338S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D338CLog,"\")\" = \"1\"\n");
  PrintTo(D338S,"sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL //p' \"",D338PLog,"\" > \"",D338PTerm,"\"\nsed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL //p' \"",D338CLog,"\" > \"",D338CTerm,"\"\ntest -s \"",D338PTerm,"\"\ntest -s \"",D338CTerm,"\"\ntest \"$(cat \"",D338PTerm,"\")\" = \"$(cat \"",D338CTerm,"\")\"\n");
fi;
PrintTo(D338S,"printf 'R07_JOINT_SLICE_KERNEL_GENERAL_V13_OK\\n' > \"",D338OK,"\"\n");
CloseStream(D338S);;
Exec(Concatenation("bash ",D338Sh));
if not IsExistingFile(D338OK) or Length(D338Read(D338OK))=0 then Error("task338 missing completion"); fi;
Print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_DRIVER_PASS\n");
