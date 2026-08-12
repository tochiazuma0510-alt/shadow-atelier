import sys
sys.path.insert(0, r"C:\Users\81905\Desktop\shadow-atelier\search")
from ss_gap1_s0_v2 import closed_form_Q
import json

primes = [37, 41, 43, 47]
results = []
for p in primes:
    r = closed_form_Q(p)
    results.append(r)
    print(p, r["i2_Qp"], r["i3_Qp"], r["Qp_order"])

with open(r"C:\Users\81905\Desktop\shadow-atelier\scratchpad\recheck_r2_python_raw.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
