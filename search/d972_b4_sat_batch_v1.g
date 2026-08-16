#############################################################################
## d972_b4_sat_batch_v1.g
##
## Safe default-branch gap-run wrapper for the canonical-v2 finite SAT batch.
## The only caller-controlled values are four GAP integers.  All paths,
## solver commits, input SHA-256 pins, and shard size live in the versioned
## Python launcher that this wrapper executes.
##
## Example gap-run preamble (all values are integers):
##   D972_B4_SAT_DEGREE:=8;;
##   D972_B4_SAT_SHARD_START:=0;;
##   D972_B4_SAT_SHARD_END:=29;;
##   D972_B4_SAT_MAX_WORD_LENGTH:=40;;
#############################################################################

D972_B4_SAT_BATCH_LAUNCHER_PATH :=
  "search/sat/run_d972_b4_sat_batch_v1.py";;
D972_B4_SAT_BATCH_LAUNCHER_SHA256 :=
  "233f88ab51527f9df8d9e026b626fc98920c8321e9ad1850a2fa7b89605e1fd0";;
D972_B4_SAT_BATCH_LAUNCHER_SOURCE :=
  StringFile(D972_B4_SAT_BATCH_LAUNCHER_PATH);;
if D972_B4_SAT_BATCH_LAUNCHER_SOURCE=fail then
  Error("SAT batch: pinned Python launcher missing");
fi;
if HexSHA256(D972_B4_SAT_BATCH_LAUNCHER_SOURCE) <>
   D972_B4_SAT_BATCH_LAUNCHER_SHA256 then
  Error("SAT batch: pinned Python launcher SHA-256 drift");
fi;

if not IsBound(D972_B4_SAT_DEGREE) then
  Error("SAT batch: D972_B4_SAT_DEGREE is required");
fi;
if not IsBound(D972_B4_SAT_SHARD_START) then
  Error("SAT batch: D972_B4_SAT_SHARD_START is required");
fi;
if not IsBound(D972_B4_SAT_SHARD_END) then
  Error("SAT batch: D972_B4_SAT_SHARD_END is required");
fi;
if not IsBound(D972_B4_SAT_MAX_WORD_LENGTH) then
  Error("SAT batch: D972_B4_SAT_MAX_WORD_LENGTH is required");
fi;
if not IsInt(D972_B4_SAT_DEGREE) or
   not IsInt(D972_B4_SAT_SHARD_START) or
   not IsInt(D972_B4_SAT_SHARD_END) or
   not IsInt(D972_B4_SAT_MAX_WORD_LENGTH) then
  Error("SAT batch: all preamble values must be integers");
fi;
if D972_B4_SAT_DEGREE < 2 or D972_B4_SAT_DEGREE > 8 then
  Error("SAT batch: degree outside [2,8]");
fi;
if D972_B4_SAT_SHARD_START < 0 or
   D972_B4_SAT_SHARD_END < D972_B4_SAT_SHARD_START or
   D972_B4_SAT_SHARD_END > 60 then
  Error("SAT batch: shard range outside [0,60] or empty");
fi;
if D972_B4_SAT_MAX_WORD_LENGTH < 1 or
   D972_B4_SAT_MAX_WORD_LENGTH > 94 then
  Error("SAT batch: max word length outside [1,94]");
fi;

D972_B4_SAT_BATCH_CMD := Concatenation(
  "python3 \"",D972_B4_SAT_BATCH_LAUNCHER_PATH,
  "\" --degree ",
  String(D972_B4_SAT_DEGREE),
  " --shard-start ", String(D972_B4_SAT_SHARD_START),
  " --shard-end ", String(D972_B4_SAT_SHARD_END),
  " --max-word-length ", String(D972_B4_SAT_MAX_WORD_LENGTH));;
Print("D972_B4_SAT_BATCH_LAUNCH degree=",D972_B4_SAT_DEGREE,
  " shards=",D972_B4_SAT_SHARD_START,"-",D972_B4_SAT_SHARD_END,
  " max_word_length=",D972_B4_SAT_MAX_WORD_LENGTH,"\n");;
Exec(D972_B4_SAT_BATCH_CMD);;

## Exec() diagnostics are intentionally not trusted as a verdict.  The
## launcher must leave this marker only after writing its authenticated batch
## receipt; a hard launcher error therefore cannot false-green gap-run.
D972_B4_SAT_BATCH_MARKER_FILE :=
  "ci/out/d972_b4_sat_batch_v1/final.marker";;
D972_B4_SAT_BATCH_MARKER := StringFile(D972_B4_SAT_BATCH_MARKER_FILE);;
if D972_B4_SAT_BATCH_MARKER=fail then
  Error("SAT batch: launcher final marker missing");
fi;
if PositionSublist(D972_B4_SAT_BATCH_MARKER,
    "D972_B4_SAT_BATCH_FINAL_MARKER")=fail then
  Error("SAT batch: launcher marker malformed");
fi;
if PositionSublist(D972_B4_SAT_BATCH_MARKER,
    "status=UNKNOWN_BATCH_ERROR")<>fail then
  Error("SAT batch: launcher reported hard failure");
fi;
Print(D972_B4_SAT_BATCH_MARKER);
Print("D972_B4_SAT_BATCH_WRAPPER_PASS\n");;
