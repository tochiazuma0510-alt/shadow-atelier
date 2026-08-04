# scratchpad/w5_charming_check.py
# 検算(整数のみ・群計算なし): W-5 erratum の charming 会計。
# X_N := { m mod N_ord : gcd(2m+1, N_ord) = 1 }  (定義ノート §3 / campaign §2.3 DF-3)
# T1 走査候補数 = #{ m in X_N : m = 0 mod 10 } x |W|,  W := V ∩ [P_N,P_N]
# 突合アンカー: N_ord=30 -> (16,2) = campaign §4.3 W-4 行 / N_ord=50 -> (40,5) = W-2 行
# 封印非接触・Im R 非測定。
from math import gcd

def X(nord):
    return [m for m in range(nord) if gcd(2 * m + 1, nord) == 1]

print("=== charming set の会計 ===")
for nord in (10, 20, 30, 40, 50):
    S = X(nord)
    T = [m for m in S if m % 10 == 0]
    print(f"N_ord={nord:3d}  |X_N|={len(S):3d}  #{{m in X_N : m=0 mod 10}}={len(T)}  ->{T}")

print("\n=== 既存 2 行との突合(campaign §4.3) ===")
assert (len(X(30)), len([m for m in X(30) if m % 10 == 0])) == (16, 2), "W-4 行と不一致"
assert (len(X(50)), len([m for m in X(50) if m % 10 == 0])) == (40, 5), "W-2 行と不一致"
print("[PASS] W-4 (N_ord=30): |X_N|=16, T1 = 2 x |<Z>|=3 -> 6")
print("[PASS] W-2 (N_ord=50): |X_N|=40, T1 = 5 x |5A_25|=125 -> 625")

print("\n=== W-5 (|[P_N,P_N]|=250, |W|=|V|=2) ===")
for nord, label in ((20, "corrected (裁定 473)"), (40, "campaign v1 (誤値)")):
    S = X(nord)
    T = [m for m in S if m % 10 == 0]
    print(f"  N_ord={nord}  {label:22s}: |X_N|={len(S):2d}  "
          f"T1 = {len(T)} x 2 -> {len(T)*2}   full-enum raw = {len(S)} x 250 -> {len(S)*250}")

print("\nW5_CHARMING_CHECK_DONE")
