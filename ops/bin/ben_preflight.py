# ben_preflight.py - commander letter preflight (2026-07-28, after B71-1).
# Rule: no 64-hex value ships in a letter unless it is machine-reproduced NOW.
# Usage: python ops/bin/ben_preflight.py ops/inbox_codex/sol_task_NN_x.txt
# Exit 0 = PASS (safe to deliver). Exit 1 = STOP with offending tokens.
import hashlib, re, subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
letter_path = sys.argv[1]
letter = open(os.path.join(ROOT, letter_path), encoding="utf-8").read()

# 1. every repo path mentioned in the letter -> recompute sha256 now
paths = set(re.findall(r"(?:docs|search|provenance|sol|ops)/[\w\-./]+\.(?:md|py|mjs|txt|g|json)", letter))
allowed = {}
for p in sorted(paths):
    fp = os.path.join(ROOT, p)
    if os.path.isfile(fp):
        allowed[hashlib.sha256(open(fp, "rb").read()).hexdigest()] = p

# 2. if a self-audit script is mentioned, run it and harvest every digest it prints
audit = next((p for p in paths if "selfaudit" in p), None)
if audit:
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, audit)],
                             capture_output=True, text=True, timeout=300,
                             encoding="utf-8", errors="replace")
        for h in re.findall(r"\b[0-9a-f]{64}\b", (out.stdout or "") + (out.stderr or "")):
            allowed.setdefault(h, f"(displayed by {audit})")
        if out.returncode != 0:
            print(f"STOP: {audit} exit={out.returncode} (must be 0 before shipping)")
            sys.exit(1)
    except Exception as e:
        print(f"STOP: could not run {audit}: {e}")
        sys.exit(1)

# 3. every 64-hex token in the letter must be reproduced, or explicitly historical
HIST = re.compile(r"supersedes|旧|歴史|historical|不変|前版|再現値")
bad = []
for line in letter.splitlines():
    for h in re.findall(r"\b[0-9a-f]{64}\b", line):
        if h in allowed:
            continue
        if HIST.search(line):
            continue  # explicitly marked as a historical/quoted value
        bad.append((h[:16] + "…", line.strip()[:80]))

if bad:
    print("STOP: letter contains hex values not reproduced by any current file/run:")
    for h, l in bad:
        print(f"  {h}  in: {l}")
    sys.exit(1)
print(f"PASS: {len(allowed)} reproduced digests cover all non-historical hex tokens "
      f"({len(paths)} files scanned{', audit rerun OK' if audit else ''})")
