# Task1126: existing gap-run.yml, empty preamble, independent C6 selftest only.
T1126Bash := Filename(DirectoriesSystemPrograms(), "bash");;
if T1126Bash = fail then
  Print("TASK1126_GAP_FINAL bash-not-found\n");
  QUIT_GAP(1);
fi;
T1126Status := Process(DirectoryCurrent(), T1126Bash, InputTextNone(), OutputTextUser(),
  ["-c", "set -eu; test -f \"$1\"; test ! -L \"$1\"; test \"$(wc -c < \"$1\")\" -eq \"$2\"; actual=$(sha256sum -- \"$1\"); test \"${actual%% *}\" = \"$3\"; exec bash -- \"$1\"",
   "task1126-fixed-bootstrap", "search/d972_r07_C6_artifact_identity_selftest_gha_v1.sh",
   "2064", "766ef48e25298154ea7691c1e3714ef5415242adf1fd0bc277bdabfe32a4e77d"]);;
Print("TASK1126_GAP_PROCESS_STATUS=", T1126Status, "\n");
if not IsInt(T1126Status) or T1126Status <> 0 then
  Print("TASK1126_GAP_FINAL FAIL\n");
  QUIT_GAP(1);
fi;
Print("TASK1126_GAP_FINAL PROCESS_ZERO_ROOT_RECEIPT_REVIEW_REQUIRED\n");
QUIT_GAP(0);
