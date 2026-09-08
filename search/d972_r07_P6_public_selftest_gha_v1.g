# Task1128: existing gap-run.yml, empty preamble, public P6 selftest only.
T1128Bash := Filename(DirectoriesSystemPrograms(), "bash");;
if T1128Bash = fail then
  Print("TASK1128_GAP_FINAL bash-not-found\n");
  QUIT_GAP(1);
fi;
T1128Status := Process(DirectoryCurrent(), T1128Bash, InputTextNone(), OutputTextUser(),
  ["-c", "set -eu; test -f \"$1\"; test ! -L \"$1\"; test \"$(wc -c < \"$1\")\" -eq \"$2\"; actual=$(sha256sum -- \"$1\"); test \"${actual%% *}\" = \"$3\"; exec bash -- \"$1\"",
   "task1128-fixed-bootstrap", "search/d972_r07_P6_public_selftest_gha_v1.sh",
   "2212", "115aba035d7c5c4a6ab03520c5598a8d303fa05df1364cd5ac060c7c9db39206"]);;
Print("TASK1128_GAP_PROCESS_STATUS=", T1128Status, "\n");
if not IsInt(T1128Status) or T1128Status <> 0 then
  Print("TASK1128_GAP_FINAL FAIL\n");
  QUIT_GAP(1);
fi;
Print("TASK1128_GAP_FINAL PROCESS_ZERO_ROOT_RECEIPT_REVIEW_REQUIRED\n");
QUIT_GAP(0);
