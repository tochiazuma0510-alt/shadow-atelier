#!/usr/bin/env bash
# Task1126 fixed checkout bootstrap; no preamble or user code argument.
set -euo pipefail
out=ci/out/task1126
stem=search/d972_r07_C6_artifact_identity_selftest_gha_v1
if [ "$#" -ne 0 ] || [ -L ci ] || [ -L ci/out ] || [ -L "$out" ] || [ ! -d "$out" ]; then
  printf '%s\n' 'TASK1126_BOOTSTRAP_REJECT output-root-or-arguments' >&2
  exit 2
fi
contents=$(find "$out" -mindepth 1 -maxdepth 1 -print -quit) || exit 2
if [ -n "$contents" ]; then
  printf '%s\n' 'TASK1126_BOOTSTRAP_REJECT nonempty-output-root' >&2
  exit 2
fi
set -o noclobber
: > "$out/bootstrap-claim" || exit 2
started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
reason=bootstrap-started
finish() {
  rc=$?
  trap - EXIT
  finished=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf '{"schema":"task1126.shell-end.v1","returncode":%s,"reason":"%s","started_utc":"%s","finished_utc":"%s","fullA0":false,"candidate":false,"cross_checked":false,"verified":false}\n' \
    "$rc" "$reason" "$started" "$finished" > "$out/shell-end.json" || rc=1
  printf 'TASK1126_SHELL_FINAL returncode=%s reason=%s\n' "$rc" "$reason"
  exit "$rc"
}
trap finish EXIT
check_pin() {
  file=$1
  bytes=$2
  hash=$3
  [ -f "$file" ] && [ ! -L "$file" ] || return 1
  actual_size=$(wc -c < "$file") || return 1
  actual_hash=$(sha256sum -- "$file") || return 1
  actual_hash=${actual_hash%% *}
  [ "$actual_size" -eq "$bytes" ] && [ "$actual_hash" = "$hash" ] || return 1
  printf '%s  %s\n' "$actual_hash" "$file" >> "$out/bootstrap-sources.sha256"
}
reason=outer-source-pin-failure
check_pin "$stem.py" 25914 1d5d45debb1708f79af5c6ad3cb72a16a2282e641fbcd7735b1dee9b517e12e7 || exit 1
check_pin "$stem.json" 37389 5b3163083d8e2e684a3bc7f82900c1179827f343202d75296360949e864deead || exit 1
reason=python3-not-found
python=$(command -v python3) || exit 127
printf '%s\n' "$python" > "$out/python3-command.txt"
printf '%s\0' "$python" '-B' "$stem.py" > "$out/outer-argv.nul"
reason=outer-running
if PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$python" -B "$stem.py"; then
  rc=0
else
  rc=$?
fi
reason=outer-returned
exit "$rc"
