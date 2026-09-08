#!/usr/bin/env bash
# Task1128 fixed checkout bootstrap; no preamble or user code argument.
set -euo pipefail
out=ci/out/task1128
stem=search/d972_r07_P6_public_selftest_gha_v1
if [ "$#" -ne 0 ] || [ -L ci ] || [ -L ci/out ] || [ -L "$out" ] || [ ! -d "$out" ]; then
  printf '%s\n' 'TASK1128_BOOTSTRAP_REJECT output-root-or-arguments' >&2
  exit 2
fi
contents=$(find "$out" -mindepth 1 -maxdepth 1 -print -quit) || exit 2
if [ -n "$contents" ]; then
  printf '%s\n' 'TASK1128_BOOTSTRAP_REJECT nonempty-output-root' >&2
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
  printf '{"schema":"task1128.shell-end.v1","returncode":%s,"reason":"%s","started_utc":"%s","finished_utc":"%s","mathematical_parent_admission":false,"full_run":false,"candidate":false,"cross_checked":false,"verified":false}\n' \
    "$rc" "$reason" "$started" "$finished" > "$out/shell-end.json" || rc=1
  printf 'TASK1128_SHELL_FINAL returncode=%s reason=%s\n' "$rc" "$reason"
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
check_pin "$stem.py" 34142 8aa03dc7e62e51af9b5c9878bb05ead094c317b094473aaadea46fb4561dc631 || exit 1
check_pin "$stem.json" 24360 1ed4e223722800f3b7d3fd76ee569e0926df4e9574a1b8f6f150a80280d69545 || exit 1
reason=python3-not-found
python=$(command -v python3) || exit 127
printf '%s\n' "$python" > "$out/python3-command.txt"
printf '%s\0' "$python" '-B' "$stem.py" > "$out/outer-argv.nul"
reason=outer-running
if PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$python" -B "$stem.py" > "$out/outer.stdout.bin" 2> "$out/outer.stderr.bin"; then
  rc=0
else
  rc=$?
fi
reason=outer-returned
cat -- "$out/outer.stdout.bin"
cat -- "$out/outer.stderr.bin" >&2
exit "$rc"
