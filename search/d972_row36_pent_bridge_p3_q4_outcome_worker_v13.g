#############################################################################
## P3 fixed-row36 v13 Q4 worker warning-only repair.
##
## The frozen v11 worker uses the current top-level loop word inside a GAP
## anonymous function.  GAP evaluates it correctly, but emits an unbound-global
## syntax warning while parsing that function.  This wrapper authenticates v11
## and inserts one outcome-neutral prebinding immediately before the loop.
#############################################################################

P159OR36P3W13Base:=
  "search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g";;
P159OR36P3W13BaseBytes:=3258958;;
P159OR36P3W13BaseSha:=
  "3838da922ddd7117e2d134a5c773a6ed606b2e656f8ce6c70ee82e6f7b9e691c";;
P159OR36P3W13Effective:=
  "ci/out/d972_row36_pent_bridge_p3_q4_outcome_worker_effective_v13.g";;
P159OR36P3W13Result:=
  "ci/out/d972_row36_pent_bridge_p3_q4_results_v11_20260824.json";;
P159OR36P3W13Old:=Concatenation(
  "P159OR36P3W11Results:=[];;\n",
  "for P159OR36P3W11i in [1..17496] do");;
P159OR36P3W13New:=Concatenation(
  "P159OR36P3W11Results:=[];;\n",
  "P159OR36P3W11word:=fail;;\n",
  "for P159OR36P3W11i in [1..17496] do");;

P159OR36P3W13RequireSha:=function(path,expectedBytes,expectedSha)
  local raw,actual;
  raw:=StringFile(path);;
  if raw=fail then
    Error("PENT159O_ROW36_P3_WORKER_V13: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);;
  if Length(raw)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_WORKER_V13: immutable pin mismatch ",path,
      " expected_bytes=",expectedBytes," actual_bytes=",Length(raw),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_WORKER_V13_PIN_PASS path=",path,
    " bytes=",Length(raw)," sha256=",actual,"\n");
  return raw;
end;;

P159OR36P3W13Count:=function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("PENT159O_ROW36_P3_WORKER_V13: occurrence input drift");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

P159OR36P3W13WriteExact:=function(path,raw,expectedBytes,expectedSha)
  local stream,readback,actual;
  if StringFile(path)<>fail then
    Error("PENT159O_ROW36_P3_WORKER_V13: pre-existing effective worker ",path);
  fi;
  stream:=OutputTextFile(path,false);;
  if stream=fail then
    Error("PENT159O_ROW36_P3_WORKER_V13: cannot open effective worker ",path);
  fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,raw);;
  CloseStream(stream);
  readback:=StringFile(path);;
  if readback=fail or readback<>raw then
    Error("PENT159O_ROW36_P3_WORKER_V13: effective worker readback drift");
  fi;
  actual:=HexSHA256(readback);;
  if Length(readback)<>expectedBytes or actual<>expectedSha then
    Error("PENT159O_ROW36_P3_WORKER_V13: generated worker pin drift",
      " expected_bytes=",expectedBytes," actual_bytes=",Length(readback),
      " expected_sha256=",expectedSha," actual_sha256=",actual);
  fi;
  Print("PENT159O_ROW36_P3_WORKER_V13_EFFECTIVE_PIN path=",path,
    " bytes=",Length(readback)," sha256=",actual,"\n");
end;;

Print("PENT159O_ROW36_P3_WORKER_V13_START repair=prebind_loop_word math_change=false universe_change=false\n");
P159OR36P3W13Raw:=P159OR36P3W13RequireSha(
  P159OR36P3W13Base,P159OR36P3W13BaseBytes,P159OR36P3W13BaseSha);;
if P159OR36P3W13Count(P159OR36P3W13Raw,P159OR36P3W13Old)<>1 or
   P159OR36P3W13Count(P159OR36P3W13Raw,
     "c->P159OR36P3W11Eval(P159OR36P3W11word,c)")<>1 or
   P159OR36P3W13Count(P159OR36P3W13Raw,
     "P159OR36P3W11word:=fail;;")<>0 then
  Error("PENT159O_ROW36_P3_WORKER_V13: warning repair cardinality drift");
fi;
P159OR36P3W13Patched:=ReplacedString(
  P159OR36P3W13Raw,P159OR36P3W13Old,P159OR36P3W13New);;
if P159OR36P3W13Count(P159OR36P3W13Patched,P159OR36P3W13Old)<>0 or
   P159OR36P3W13Count(P159OR36P3W13Patched,P159OR36P3W13New)<>1 or
   P159OR36P3W13Count(P159OR36P3W13Patched,
     "c->P159OR36P3W11Eval(P159OR36P3W11word,c)")<>1 then
  Error("PENT159O_ROW36_P3_WORKER_V13: effective warning repair drift");
fi;

Exec("mkdir -p 'ci/out'");;
P159OR36P3W13WriteExact(P159OR36P3W13Effective,P159OR36P3W13Patched,
  3258984,"8a7d1cd0d12ef68d87601aa083893209712bf4b99b9bcf4cbc3cbb81fc472a32");;
Print("PENT159O_ROW36_P3_WORKER_V13_WARNING_REPAIR_PASS prebound_before_lambda=true lambda_and_order_unchanged=true\n");
Read(P159OR36P3W13Effective);;
P159OR36P3W13RequireSha(P159OR36P3W13Result,14729301,
  "ce7951c374c1dad4fe36e240dd6289e1e5f410c3111ceb892891b1521eac1480");;
Print("PENT159O_ROW36_P3_WORKER_V13_RESULT_SEMANTIC_DIGEST_PASS words=17496 bytes=14729301 sha256=ce7951c374c1dad4fe36e240dd6289e1e5f410c3111ceb892891b1521eac1480\n");
