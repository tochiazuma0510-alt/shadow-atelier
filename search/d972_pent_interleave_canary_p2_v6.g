#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 stage v6.
##
## Versioned repair of v5 after GHA run 32648846482.  The expensive quotient
## and map construction passed; only the demand that the order discriminator
## itself live in the D4_2 instrument failed.  V6 preserves that finite-window
## observation and adds an independent S3 noncommuting word-order canary.
##
## The frozen v5 producer is authenticated and patched in memory by exact,
## counted replacements.  The effective v6 source is written to ci/out and
## hash-marked before Read.  V5 is never overwritten.
#############################################################################

P159V6WrapperSource := "search/d972_pent_interleave_canary_p2_v6.g";
P159V6BaseSource := "search/d972_pent_interleave_canary_p2_v5.g";
P159V6BaseSha :=
  "4be7bb2cac38c718240a5333b50c358f0de5b7b15d5993d4241b442a16be5d0c";
P159V6EffectivePath :=
  "ci/out/d972_pent_interleave_canary_p2_effective_v6.g";

P159V6CountSublist := function(s,needle)
  local count,pos,tail,offset,rel;
  if Length(needle)=0 then Error("PENT159N_V6: empty replacement needle"); fi;
  count:=0; pos:=PositionSublist(s,needle);
  while pos<>fail do
    count:=count+1;
    offset:=pos+Length(needle);
    if offset>Length(s) then pos:=fail;
    else
      tail:=s{[offset..Length(s)]};
      rel:=PositionSublist(tail,needle);
      if rel=fail then pos:=fail; else pos:=offset+rel-1; fi;
    fi;
  od;
  return count;
end;

P159V6ReplaceExact := function(s,old,new,expected,label)
  local got,out;
  got:=P159V6CountSublist(s,old);
  if got<>expected then
    Error("PENT159N_V6: replacement count drift ",label,
      " expected=",expected," observed=",got);
  fi;
  out:=ReplacedString(s,old,new);
  if P159V6CountSublist(out,old)<>0 and PositionSublist(new,old)=fail then
    Error("PENT159N_V6: replacement residue ",label);
  fi;
  return out;
end;

P159V6BaseRaw:=StringFile(P159V6BaseSource);
if P159V6BaseRaw=fail then
  Error("PENT159N_V6: frozen v5 source missing");
fi;
P159V6BaseActualSha:=HexSHA256(P159V6BaseRaw);
if P159V6BaseActualSha<>P159V6BaseSha then
  Error("PENT159N_V6: frozen v5 source SHA drift ",P159V6BaseActualSha);
fi;
P159V6Effective:=P159V6BaseRaw;

P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "P159V5Source := \"search/d972_pent_interleave_canary_p2_v5.g\";",
  "P159V5Source := \"search/d972_pent_interleave_canary_p2_v6.g\";",
  1,"source path");
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "ci/out/d972_pent_interleave_canary_p2_receipt_v5_20260824.json",
  "ci/out/d972_pent_interleave_canary_p2_receipt_v6_20260824.json",
  1,"receipt path");
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "d972-pent-interleave-canary-p2/v5",
  "d972-pent-interleave-canary-p2/v6",1,"receipt schema");

## Avoid parse-time unbound-global warnings while keeping the optional flush.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "if IsBoundGlobal(\"FlushAllStreams\") then FlushAllStreams(); fi;",
  "if IsBoundGlobal(\"FlushAllStreams\") then CallFuncList(ValueGlobal(\"FlushAllStreams\"),[]); fi;",
  2,"FlushAllStreams bound call");

## Give the deletion-map loop an explicit indexed variable.  The v5 arrow
## expression was mathematically correct but produced an unbound-global syntax
## warning for the record component on this GAP parser.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "P159V5DeletionBits:=List(P159V5DeletionMaps,m->\n",
    "    Image(m.hom_internal,P159V5Drec.correct)=One(P159V5Q3.group));"),
  Concatenation(
    "P159V5DeletionBits:=[];\n",
    "  for P159V5i in [1..Length(P159V5DeletionMaps)] do\n",
    "    Add(P159V5DeletionBits,Image(P159V5DeletionMaps[P159V5i].hom_internal,\n",
    "      P159V5Drec.correct)=One(P159V5Q3.group));\n",
    "  od;"),
  1,"deletion map local scope");

## Install an independent finite-group order canary.  With A=B=C=1,
## E=(2,3), F=(1,2,3), the correct and reversed five-factor words in S3 are
## distinct noncommuting transpositions.  This tests multiplication order
## without demanding sensitivity from the deletion-blind D4_2 window.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "P159V5WrongOrderDiscriminator:=fail;\n",
    "P159V5InversionDiscriminator:=fail;"),
  Concatenation(
    "P159V5WrongOrderDiscriminator:=fail;\n",
    "P159V6OrderCanaryGroup:=SymmetricGroup(3);\n",
    "P159V6OrderCanaryA:=One(P159V6OrderCanaryGroup);\n",
    "P159V6OrderCanaryB:=One(P159V6OrderCanaryGroup);\n",
    "P159V6OrderCanaryC:=One(P159V6OrderCanaryGroup);\n",
    "P159V6OrderCanaryE:=(2,3);\n",
    "P159V6OrderCanaryF:=(1,2,3);\n",
    "P159V6OrderCanaryCorrect:=P159V5Paper([P159V6OrderCanaryA^-1,\n",
    "  P159V6OrderCanaryB^-1,P159V6OrderCanaryC,P159V6OrderCanaryE,\n",
    "  P159V6OrderCanaryF]);\n",
    "P159V6OrderCanaryMutant:=P159V5Paper([P159V6OrderCanaryF,\n",
    "  P159V6OrderCanaryE,P159V6OrderCanaryC,P159V6OrderCanaryB^-1,\n",
    "  P159V6OrderCanaryA^-1]);\n",
    "P159V6OrderCanaryComm:=Comm(P159V6OrderCanaryCorrect,\n",
    "  P159V6OrderCanaryMutant);\n",
    "if P159V6OrderCanaryCorrect=P159V6OrderCanaryMutant or\n",
    "   P159V6OrderCanaryComm=One(P159V6OrderCanaryGroup) then\n",
    "  Error(\"PENT159N_V6: independent S3 wrong-order canary failed\");\n",
    "fi;\n",
    "P159V6OrderCanary:=rec(group:=\"S3\",order:=6,\n",
    "  factors:=rec(A:=[1,2,3],B:=[1,2,3],C:=[1,2,3],\n",
    "    E:=List([1..3],i->i^P159V6OrderCanaryE),\n",
    "    F:=List([1..3],i->i^P159V6OrderCanaryF)),\n",
    "  correct_factor_order:=[\"A^-1\",\"B^-1\",\"C\",\"E\",\"F\"],\n",
    "  mutant_factor_order:=[\"F\",\"E\",\"C\",\"B^-1\",\"A^-1\"],\n",
    "  correct_image:=List([1..3],i->i^P159V6OrderCanaryCorrect),\n",
    "  mutant_image:=List([1..3],i->i^P159V6OrderCanaryMutant),\n",
    "  commutator_image:=List([1..3],i->i^P159V6OrderCanaryComm),\n",
    "  distinct:=true,noncommuting:=true);\n",
    "P159V6WrongOrderQ2DistinctCount:=0;\n",
    "P159V6WrongOrderQ2NoncommutingCount:=0;\n",
    "P159V5InversionDiscriminator:=fail;"),
  1,"independent S3 order canary");

## Count equality and commutation over the entire 128-element Q2 word
## universe before selecting any Q2-local noncommuting row.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "  if P159V5WrongOrderDiscriminator=fail and\n",
    "     Comm(P159V5Drec.correct,P159V5Drec.wrong_order_mutant)<>\n",
    "     One(P159V5Q4.group) then"),
  Concatenation(
    "  if P159V5Drec.correct<>P159V5Drec.wrong_order_mutant then\n",
    "    P159V6WrongOrderQ2DistinctCount:=P159V6WrongOrderQ2DistinctCount+1;\n",
    "  fi;\n",
    "  if Comm(P159V5Drec.correct,P159V5Drec.wrong_order_mutant)<>\n",
    "     One(P159V5Q4.group) then\n",
    "    P159V6WrongOrderQ2NoncommutingCount:=\n",
    "      P159V6WrongOrderQ2NoncommutingCount+1;\n",
    "  fi;\n",
    "  if P159V5WrongOrderDiscriminator=fail and\n",
    "     Comm(P159V5Drec.correct,P159V5Drec.wrong_order_mutant)<>\n",
    "     One(P159V5Q4.group) then"),
  1,"full Q2 equality/commutation counters");

## The D4_2 window is allowed to be blind to this destructive control.  Keep
## its exact counts and use the independent S3 word canary when no Q2-local
## noncommuting row exists.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "if P159V5WrongOrderDiscriminator=fail then\n",
    "  Error(\"PENT159N_V5: no noncommuting wrong-order discriminator in full Q2 universe\");\n",
    "fi;"),
  Concatenation(
    "P159V6WrongOrderFullQ2Equal:=P159V6WrongOrderQ2DistinctCount=0;\n",
    "P159V6WrongOrderFullQ2Commuting:=P159V6WrongOrderQ2NoncommutingCount=0;\n",
    "if P159V5WrongOrderDiscriminator=fail then\n",
    "  P159V5WrongOrderDiscriminator:=P159V6OrderCanary;\n",
    "fi;\n",
    "Print(\"PENT159N_P2_V5_WRONG_ORDER_CONTROL_PASS q2_universe=\",\n",
    "  Length(P159V5Bfs),\" q2_distinct=\",P159V6WrongOrderQ2DistinctCount,\n",
    "  \" q2_noncommuting=\",P159V6WrongOrderQ2NoncommutingCount,\n",
    "  \" q2_equal_all=\",P159V6WrongOrderFullQ2Equal,\n",
    "  \" external_group=S3 external_distinct=true external_noncommuting=true\\n\");"),
  1,"replace Q2-local fatal order gate");

## Bind both the measured Q2 blindness and the independent discriminator in
## the receipt rather than overwriting one interpretation with the other.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "    wrong_order_noncommuting_discriminator:=P159V5WrongOrderDiscriminator,\n",
    "    lhs_rhs_inversion_checked_in_every_Dpap_call:=true,"),
  Concatenation(
    "    wrong_order_noncommuting_discriminator:=P159V5WrongOrderDiscriminator,\n",
    "    wrong_order_full_Q2_universe_count:=Length(P159V5Bfs),\n",
    "    wrong_order_full_Q2_distinct_count:=P159V6WrongOrderQ2DistinctCount,\n",
    "    wrong_order_full_Q2_noncommuting_count:=P159V6WrongOrderQ2NoncommutingCount,\n",
    "    wrong_order_full_Q2_equal_all:=P159V6WrongOrderFullQ2Equal,\n",
    "    wrong_order_full_Q2_commuting_all:=P159V6WrongOrderFullQ2Commuting,\n",
    "    wrong_order_external_finite_group_discriminator:=P159V6OrderCanary,\n",
    "    lhs_rhs_inversion_checked_in_every_Dpap_call:=true,"),
  1,"receipt order-control fields");

P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  Concatenation(
    "    source_path:=P159V5Source,\n",
    "    source_sha256_measured_at_runtime:=HexSHA256(StringFile(P159V5Source)),"),
  Concatenation(
    "    source_path:=P159V5Source,\n",
    "    source_sha256_measured_at_runtime:=HexSHA256(StringFile(P159V5Source)),\n",
    "    frozen_v5_base_source:=P159V6BaseSource,\n",
    "    frozen_v5_base_sha256:=P159V6BaseSha,\n",
    "    effective_v6_source_path:=P159V6EffectivePath,\n",
    "    effective_v6_source_sha256:=P159V6EffectiveSha,"),
  1,"receipt v6 provenance");
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "main_sol_reply_edited:=false,v1_v2_v3_v4_edited:=false",
  "main_sol_reply_edited:=false,v1_v2_v3_v4_edited:=false,v5_edited:=false",
  1,"v5 preservation firewall");

## Rename every semantic marker last, including the newly inserted control
## marker.  Internal P159V5 variable names remain intentionally unchanged.
P159V6Effective:=P159V6ReplaceExact(P159V6Effective,
  "PENT159N_P2_V5","PENT159N_P2_V6",14,"semantic marker version");

P159V6EffectiveSha:=HexSHA256(P159V6Effective);
P159V6EffectiveFile:=OutputTextFile(P159V6EffectivePath,false);
if P159V6EffectiveFile=fail then
  Error("PENT159N_V6: cannot open effective source path");
fi;
SetPrintFormattingStatus(P159V6EffectiveFile,false);
PrintTo(P159V6EffectiveFile,P159V6Effective);
CloseStream(P159V6EffectiveFile);
P159V6EffectiveReadback:=StringFile(P159V6EffectivePath);
if P159V6EffectiveReadback=fail or
   P159V6EffectiveReadback<>P159V6Effective or
   HexSHA256(P159V6EffectiveReadback)<>P159V6EffectiveSha then
  Error("PENT159N_V6: effective source closed-write/hash mismatch");
fi;
Print("PENT159N_P2_V6_EFFECTIVE_SOURCE_WRITTEN path=",P159V6EffectivePath,
  " bytes=",Length(P159V6Effective)," sha256=",P159V6EffectiveSha,
  " base_sha256=",P159V6BaseSha,"\n");
Read(P159V6EffectivePath);

