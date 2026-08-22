import cProfile
import pstats
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
sys.path.insert(0, str(ROOT / "search"))
import json
import koubou158_L3_core_v1_1 as core
import koubou158_L3_core_completebfs_v1 as cbfs
import koubou158_L3_core_fastkernel_v1 as fast

full = ROOT / core.Q3_CHIEF
q3 = json.loads(full.read_text(encoding="utf-8"))
e4 = core.E4(q3)

t0 = time.perf_counter()
proj_cache: dict = {}
mul_cache: dict = {}
canary = fast.PurityCanary(sample_rate=1000)
pr = cProfile.Profile()
pr.enable()
ech_fast, idx_fast, sp_fast, info_fast = fast.build_V_and_D2bar_from_q3_complete_fast(
    e4, q3, 4, proj_cache, mul_cache, canary)
pr.disable()
t1 = time.perf_counter()
print(f"FAST j=4: {t1-t0:.2f}s dim={info_fast['dim_Lambda_over_Ij']} "
      f"rank={info_fast['rank_V_plus_D2bar_combined']} "
      f"total_explored={info_fast['total_vectors_explored']} "
      f"depth_ok={info_fast['depth_requirement_satisfied']} "
      f"canary_checked={canary.checked} canary_mismatches={canary.mismatches}")

stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(15)

# cross-check against ORIGINAL (uncached) builder for exact agreement
t2 = time.perf_counter()
ech_orig, idx_orig, sp_orig, info_orig = cbfs.build_V_and_D2bar_from_q3_complete(e4, q3, 4)
t3 = time.perf_counter()
print(f"ORIG  j=4: {t3-t2:.2f}s dim={info_orig['dim_Lambda_over_Ij']} "
      f"rank={info_orig['rank_V_plus_D2bar_combined']} "
      f"depth_ok={info_orig['depth_requirement_satisfied']}")

match = (info_fast["dim_Lambda_over_Ij"] == info_orig["dim_Lambda_over_Ij"] and
         info_fast["rank_V_plus_D2bar_combined"] == info_orig["rank_V_plus_D2bar_combined"] and
         info_fast["depth_requirement_satisfied"] == info_orig["depth_requirement_satisfied"])
print(f"MATCH: {match}  speedup={((t3-t2)/(t1-t0)):.2f}x")
