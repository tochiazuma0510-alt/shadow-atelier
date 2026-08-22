import cProfile
import pstats
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\81905\Desktop\shadow-atelier")
sys.path.insert(0, str(ROOT / "search"))
import json
import koubou158_L3_core_v1_1 as core
import koubou158_L3_core_completebfs_v1 as cbfs

full = ROOT / core.Q3_CHIEF
q3 = json.loads(full.read_text(encoding="utf-8"))
e4 = core.E4(q3)

pr = cProfile.Profile()
pr.enable()
ech_combined, idx, sp, info = cbfs.build_V_and_D2bar_from_q3_complete(e4, q3, 4)
pr.disable()
print("dim", info["dim_Lambda_over_Ij"], "rank", info["rank_V_plus_D2bar_combined"])
print("total_vectors_explored", info["total_vectors_explored"])
stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(20)
stats.sort_stats("tottime")
stats.print_stats(20)
