#############################################################################
## d972_b4_original_automatic_v2.g -- configurable direct 6/158 lane.
##
## This is a versioned wrapper around the frozen, independently audited v1
## canonical producer.  It pins the v1 source SHA, checks that source has no
## Read-context QUIT, and changes only the KBMAG configuration call/options.
## The canonical source/word/norm gates and all FSA/reduced-word logic remain
## the v1 code.  The receipt is extended with a typed v2_settings object.
#############################################################################

D972OA2V1Path:="search/d972_b4_original_automatic_v1.g";;
D972OA2V1Sha:="fcb32175837412bbce9bf117fbe0eb8c4f8cc1b11f9fa921b46acf133ecc6874";;
D972OA2Raw:=StringFile(D972OA2V1Path);;
if D972OA2Raw=fail or HexSHA256(D972OA2Raw)<>D972OA2V1Sha then
  Error("ORIGINAL automatic v2: pinned v1 source SHA drift");
fi;
if PositionSublist(D972OA2Raw,"QUIT")<>fail then
  Error("ORIGINAL automatic v2: v1 source contains forbidden QUIT");
fi;

## All controls are deliberately numeric/bool preamble bindings.  Defaults
## reproduce the v1 direct lane exactly, while every override is type-gated.
D972OA2Large:=true;;
D972OA2Filestore:=true;;
D972OA2Diff1:=false;;
D972OA2ComputeSize:=true;;
D972OA2MaxEqns:=250000;;
D972OA2MaxStates:=250000;;
D972OA2MaxWdiffs:=250000;;
D972OA2MaxStored:=[4000,4000];;
D972OA2PostReplay:=false;;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_LARGE) then D972OA2Large:=D972_B4_ORIGINAL_AUTOMATIC_V2_LARGE; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_FILESTORE) then D972OA2Filestore:=D972_B4_ORIGINAL_AUTOMATIC_V2_FILESTORE; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1) then D972OA2Diff1:=D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_COMPUTE_SIZE) then D972OA2ComputeSize:=D972_B4_ORIGINAL_AUTOMATIC_V2_COMPUTE_SIZE; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_MAXEQNS) then D972OA2MaxEqns:=D972_B4_ORIGINAL_AUTOMATIC_V2_MAXEQNS; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTATES) then D972OA2MaxStates:=D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTATES; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_MAXWDIFFS) then D972OA2MaxWdiffs:=D972_B4_ORIGINAL_AUTOMATIC_V2_MAXWDIFFS; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTOREDLEN) then D972OA2MaxStored:=D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTOREDLEN; fi;
if IsBound(D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY) then D972OA2PostReplay:=D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY; fi;
if not IsBool(D972OA2Large) or not IsBool(D972OA2Filestore) or
   not IsBool(D972OA2Diff1) or not IsBool(D972OA2ComputeSize) or
   not IsBool(D972OA2PostReplay) then
  Error("ORIGINAL automatic v2: boolean setting drift");
fi;
if not IsInt(D972OA2MaxEqns) or D972OA2MaxEqns<=0 or
   not IsInt(D972OA2MaxStates) or D972OA2MaxStates<=0 or
   not IsInt(D972OA2MaxWdiffs) or D972OA2MaxWdiffs<=0 or
   not IsList(D972OA2MaxStored) or Length(D972OA2MaxStored)<>2 or
   not ForAll(D972OA2MaxStored,x->IsInt(x) and x>0) then
  Error("ORIGINAL automatic v2: numeric setting drift");
fi;

D972OA2Json:=function(x)
  local p,i;
  if IsBool(x) then if x then return "true"; else return "false"; fi; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if not IsList(x) then Error("ORIGINAL automatic v2: JSON type drift"); fi;
  if Length(x)=0 then return "[]"; fi;
  p:=List([1..Length(x)],i->D972OA2Json(x[i]));
  return Concatenation("[",JoinStringsWithSeparator(p,","),"]");
end;;
D972OA2Settings:=Concatenation(
  "{\"producer\":\"d972_b4_original_automatic_v2\",",
  "\"large\":",D972OA2Json(D972OA2Large),",",
  "\"filestore\":",D972OA2Json(D972OA2Filestore),",",
  "\"diff1\":",D972OA2Json(D972OA2Diff1),",",
  "\"compute_size\":",D972OA2Json(D972OA2ComputeSize),",",
  "\"maxeqns\":",D972OA2Json(D972OA2MaxEqns),",",
  "\"maxstates\":",D972OA2Json(D972OA2MaxStates),",",
  "\"maxwdiffs\":",D972OA2Json(D972OA2MaxWdiffs),",",
  "\"maxstoredlen\":",D972OA2Json(D972OA2MaxStored),",",
  "\"post_replay\":",D972OA2Json(D972OA2PostReplay),",",
  "\"v1_source_sha256\":\"",D972OA2V1Sha,"\"}");;

## Bind v1's existing size switch from the v2-typed control.
D972_B4_ORIGINAL_AUTOMATIC_COMPUTE_SIZE:=D972OA2ComputeSize;;
D972OA2CallOld:="D972OAResult:=AutomaticStructure(D972OARws,true,true,false);;";;
D972OA2CallNew:="D972OAResult:=AutomaticStructure(D972OARws,D972OA2Large,D972OA2Filestore,D972OA2Diff1);;";;
D972OA2Raw:=ReplacedString(D972OA2Raw,D972OA2CallOld,D972OA2CallNew);;
D972OA2CapsOld:="D972OAOpts.maxeqns:=250000;; D972OAOpts.maxstates:=250000;; D972OAOpts.maxwdiffs:=250000;;";;
D972OA2CapsNew:=Concatenation(
  "D972OAOpts.maxeqns:=D972OA2MaxEqns;; D972OAOpts.maxstates:=D972OA2MaxStates;; ",
  "D972OAOpts.maxwdiffs:=D972OA2MaxWdiffs;;");;
D972OA2Raw:=ReplacedString(D972OA2Raw,D972OA2CapsOld,D972OA2CapsNew);;
D972OA2Raw:=ReplacedString(D972OA2Raw,
  "D972OAOpts.maxstoredlen:=[4000,4000];;",
  "D972OAOpts.maxstoredlen:=D972OA2MaxStored;;");;
if PositionSublist(D972OA2Raw,D972OA2CallOld)<>fail or
   PositionSublist(D972OA2Raw,D972OA2CapsOld)<>fail or
   PositionSublist(D972OA2Raw,"D972OAOpts.maxstoredlen:=[4000,4000];;")<>fail or
   PositionSublist(D972OA2Raw,D972OA2CallNew)=fail then
  Error("ORIGINAL automatic v2: source configuration splice failed");
fi;

D972OA2Temp:=Filename(DirectoryTemporary(),"d972_b4_original_automatic_v2_exec.g");;
FileString(D972OA2Temp,D972OA2Raw);;
Print("B4_ORIGINAL_AUTOMATIC_V2_CONFIG_PASS large=",D972OA2Large,
  " filestore=",D972OA2Filestore," diff1=",D972OA2Diff1,
  " maxeqns=",D972OA2MaxEqns," maxstates=",D972OA2MaxStates,
  " maxwdiffs=",D972OA2MaxWdiffs," compute_size=",D972OA2ComputeSize,"\n");
Read(D972OA2Temp);;

## v1 writes the canonical receipt.  Add the typed settings without changing
## any canonical field, then require that the producer did write a receipt.
if not IsBound(D972OAOutput) then
  Error("ORIGINAL automatic v2: v1 output binding missing");
fi;
D972OA2ReceiptRaw:=StringFile(D972OAOutput);;
if D972OA2ReceiptRaw=fail then
  Error("ORIGINAL automatic v2: producer receipt missing");
fi;
D972OA2Rev:=Reversed(D972OA2ReceiptRaw);;
D972OA2Last:=PositionSublist(D972OA2Rev,"}");;
if D972OA2Last=fail then Error("ORIGINAL automatic v2: malformed receipt"); fi;
D972OA2At:=Length(D972OA2ReceiptRaw)-D972OA2Last+1;;
D972OA2ReceiptRaw:=Concatenation(
  D972OA2ReceiptRaw{[1..D972OA2At-1]},
  ",\"v2_settings\":",D972OA2Settings,"}\n");;
D972OA2Out:=OutputTextFile(D972OAOutput,false);;
SetPrintFormattingStatus(D972OA2Out,false);;
PrintTo(D972OA2Out,D972OA2ReceiptRaw);;
CloseStream(D972OA2Out);;
Print("B4_ORIGINAL_AUTOMATIC_V2_SETTINGS_PASS output=",D972OAOutput,"\n");
Print("B4_ORIGINAL_AUTOMATIC_V2_FINAL_MARKER output=",D972OAOutput,
  " diff1=",D972OA2Diff1," post_replay=",D972OA2PostReplay,"\n");
if D972OA2PostReplay then
  ## Keep the producer and independent replay in one Linux job: FSA paths
  ## emitted by v1 remain addressable, and the replay receipt lands in ci/out.
  D972_B4_ORIGINAL_REPLAY_V2_RECEIPT:=D972OAOutput;;
  D972_B4_ORIGINAL_REPLAY_V2_SOURCE:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
  D972_B4_ORIGINAL_REPLAY_V2_WORDS:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
  D972_B4_ORIGINAL_REPLAY_V2_OUTPUT:="ci/out/d972_b4_original_automatic_replay_v2.json";;
  D972_B4_ORIGINAL_REPLAY_V2_LARGE:=D972OA2Large;;
  D972_B4_ORIGINAL_REPLAY_V2_FILESTORE:=D972OA2Filestore;;
  D972_B4_ORIGINAL_REPLAY_V2_DIFF1:=D972OA2Diff1;;
  D972_B4_ORIGINAL_REPLAY_V2_COMPUTE_SIZE:=D972OA2ComputeSize;;
  D972_B4_ORIGINAL_REPLAY_V2_MAXEQNS:=D972OA2MaxEqns;;
  D972_B4_ORIGINAL_REPLAY_V2_MAXSTATES:=D972OA2MaxStates;;
  D972_B4_ORIGINAL_REPLAY_V2_MAXWDIFFS:=D972OA2MaxWdiffs;;
  D972_B4_ORIGINAL_REPLAY_V2_MAXSTOREDLEN:=D972OA2MaxStored;;
  D972_B4_ORIGINAL_REPLAY_V2_POST_REPLAY:=true;;
  Read("search/check_d972_b4_original_automatic_replay_v2.g");;
  if StringFile(D972_B4_ORIGINAL_REPLAY_V2_OUTPUT)=fail then Error("ORIGINAL automatic v2: post-replay receipt missing"); fi;
  Print("B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY_PASS output=",D972_B4_ORIGINAL_REPLAY_V2_OUTPUT,"\n");
fi;
