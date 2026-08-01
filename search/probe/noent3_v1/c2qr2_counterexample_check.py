#!/usr/bin/env python3
"""c2qr2_counterexample_check.py -- 系 C2-QR2 の反例の独立検算(数学者 Opus 5 / 2026-08-02)

便 99 W99-3.4(Sol)の反例 (d=5, c2=3) と (d=15, c2=3) を再現し、
さらに 1<=d<=60 の全 (d, c2) で
  (P) ある m が存在して 3*c2 = m(m+1)/2 (mod d)
  (Q) 1 + 24*c2 が mod 8d の平方
の同値(= 系 C2-QR)と、C2-QR2 の主張「常に (P)」の反例の個数を数える。
整数演算のみ。K^{(5)} 非接触(窓の値には触れない・純粋な合同計算)。
"""

def solvable_for_m(d, c2):
    """ある m in Z/(2d) が 3*c2 == m(m+1)/2 (mod d) を満たすか。"""
    for m in range(2 * d):
        if (m * (m + 1) // 2 - 3 * c2) % d == 0:
            return True
    return False


def is_square_mod(a, n):
    a %= n
    return any((k * k) % n == a for k in range(n))


def main():
    # --- (1) Sol の反例 2 件の逐点再現 -------------------------------------
    for (d, c2) in [(5, 3), (15, 3)]:
        val = (1 + 24 * c2) % (8 * d)
        print(f"[case] d={d} c2={c2}: 1+24c2 = {1 + 24 * c2} = {val} (mod {8 * d})")
        print(f"        square mod {8 * d}? {is_square_mod(1 + 24 * c2, 8 * d)}")
        print(f"        exists m with 3c2 = m(m+1)/2 mod d? {solvable_for_m(d, c2)}")
        print(f"        3 | d ? {d % 3 == 0}")

    # --- (2) 系 C2-QR(同値)の全数確認 + C2-QR2 の反例計数 ----------------
    mismatch = 0
    counterexamples = []
    for d in range(1, 61):
        for c2 in range(d):
            p = solvable_for_m(d, c2)
            q = is_square_mod(1 + 24 * c2, 8 * d)
            if p != q:
                mismatch += 1
            if not p:
                counterexamples.append((d, c2))
    print(f"\n[QR ] 1<=d<=60 の全 (d,c2) で (P) <=> (Q) の不一致 = {mismatch} (expect 0)")
    print(f"[QR2] 「常に可解」の反例 (d,c2) の個数 = {len(counterexamples)}")
    print(f"       うち 3|d のもの = {len([1 for d, _ in counterexamples if d % 3 == 0])}")
    print(f"       うち 3 not| d のもの = {len([1 for d, _ in counterexamples if d % 3 != 0])}")
    print(f"       最小の d(3 not| d): {min([d for d, _ in counterexamples if d % 3 != 0], default=None)}")
    print(f"       最小の d(3 | d)   : {min([d for d, _ in counterexamples if d % 3 == 0], default=None)}")
    print(f"       先頭 12 件: {counterexamples[:12]}")

    # --- (3) 逆向き(m を与えて c2 を解く)は 3 が可逆なら常に可能 ---------
    #     = C2-QR2 の証明が実際に示していた向き。
    bad = 0
    for d in range(1, 61):
        if d % 3 != 0:
            inv3 = pow(3, -1, d) if d > 1 else 0
            for m in range(2 * d):
                c2 = (inv3 * (m * (m + 1) // 2)) % d if d > 1 else 0
                if (3 * c2 - m * (m + 1) // 2) % d != 0:
                    bad += 1
    print(f"\n[DIR] 3 not| d のとき m から c2 を解く向きの失敗 = {bad} (expect 0)")


if __name__ == "__main__":
    main()
