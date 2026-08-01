# -*- coding: utf-8 -*-
"""RH 消滅予測テスト: T_all(ell,1^9) を driver の route A / route B で計算し、
   「T_trans(ell,1^t)=0 for t>=9」から導いた予言値と突合する。
   予言が当たれば、T_all(l,1^0..8) 9 値すべてに整合が要求される極めて強い検査。"""
import sys, time, importlib.util
sys.setrecursionlimit(20000)
spec = importlib.util.spec_from_file_location(
    "drv", r"C:\Users\81905\Desktop\shadow-atelier\search\probe\wac_v1\w98_alg_driver.py")
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)

PRED = {37: 1659895514188, 41: 35218366741388}
for ell in (37, 41):
    t0 = time.time()
    A, _ = drv.route_A_compute(ell, 9)
    t1 = time.time()
    B, _ = drv.route_B_compute(ell, 9)
    t2 = time.time()
    print(f"ell={ell} n={ell+9}")
    print(f"  route_A T_all = {A}   ({t1-t0:.1f}s)")
    print(f"  route_B T_all = {B}   ({t2-t1:.1f}s)")
    print(f"  predicted     = {PRED[ell]}")
    print(f"  A==B: {A==B}   A==predict: {A==PRED[ell]}   => T_trans(l,1^9) = {A-PRED[ell]}")
    sys.stdout.flush()
print("A9_DONE")
